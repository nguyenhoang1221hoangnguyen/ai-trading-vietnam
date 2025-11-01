"""
Module lấy dữ liệu từ vnstock với fallback demo data
"""

from vnstock import Quote, Listing, Company
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import os
import time

# Import demo data cho fallback
try:
    from demo_data import (
        get_demo_stock_data, 
        get_demo_company_overview, 
        get_demo_financial_ratios,
        get_demo_all_stocks,
        is_demo_mode
    )
    DEMO_DATA_AVAILABLE = True
except ImportError:
    DEMO_DATA_AVAILABLE = False

class DataFetcher:
    def __init__(self):
        # Không khởi tạo Company và Listing ở đây vì chúng cần symbol
        pass
    
    def _get_yfinance_data(self, symbol, start_date, end_date):
        """Lấy dữ liệu từ yfinance (ưu tiên vì ổn định hơn)"""
        try:
            import yfinance as yf
            ticker = f"{symbol}.VN"
            
            df_yf = yf.download(
                ticker, 
                start=start_date, 
                end=end_date, 
                interval='1d', 
                progress=False, 
                auto_adjust=False
            )
            
            if df_yf is not None and not df_yf.empty:
                df_yf.columns = df_yf.columns.str.lower().str.replace(' ', '_')
                if 'adj_close' in df_yf.columns:
                    df_yf['close'] = df_yf['adj_close']
                df_yf = df_yf.sort_index()
                
                # Kiểm tra có đủ cột cần thiết
                required_columns = ['open', 'high', 'low', 'close', 'volume']
                if all(col in df_yf.columns for col in required_columns):
                    return df_yf
                    
        except Exception as e:
            pass
        return None
    
    @st.cache_data(ttl=3600)  # Cache trong 1 giờ
    def get_stock_data(_self, symbol, period='1Y', resolution='1D', start_date=None, end_date=None):
        """
        Lấy dữ liệu lịch sử giá cổ phiếu
        
        Args:
            symbol: Mã chứng khoán
            period: Khoảng thời gian (1M, 3M, 6M, 1Y, 3Y, 5Y)
            resolution: Độ phân giải (1D, 1W, 1M)
        """
        try:
            # Tính toán ngày bắt đầu và kết thúc
            end_date = datetime.now()
            
            if period == '1M':
                start_date = end_date - timedelta(days=30)
            elif period == '3M':
                start_date = end_date - timedelta(days=90)
            elif period == '6M':
                start_date = end_date - timedelta(days=180)
            elif period == '1Y':
                start_date = end_date - timedelta(days=365)
            elif period == '3Y':
                start_date = end_date - timedelta(days=1095)
            elif period == '5Y':
                start_date = end_date - timedelta(days=1825)
            else:
                start_date = end_date - timedelta(days=365)
            
            # 1. Thử yfinance trước (ổn định hơn vnstock)
            df = _self._get_yfinance_data(symbol, start_date, end_date)
            if df is not None and not df.empty:
                return df
            
            # 2. Nếu yfinance fail, thử vnstock với retry logic
            df = None
            last_error = None
            
            # Lấy dữ liệu bằng vnstock - Quote cần symbol khi khởi tạo
            try:
                import time
                
                # Thử với retry logic và delay tốt hơn cho cloud
                max_retries = 2  # Giảm retry cho vnstock vì thường fail
                
                for attempt in range(max_retries):
                    try:
                        # Khởi tạo Quote mới cho mỗi lần thử (tránh stale connection)
                        quote = Quote(symbol=symbol, source='VCI')
                        
                        # Thêm delay trước mỗi request để tránh rate limit
                        if attempt > 0:
                            time.sleep(2 ** attempt)  # Exponential backoff: 2s, 4s
                        
                        df = quote.history(
                            start=start_date.strftime('%Y-%m-%d'),
                            end=end_date.strftime('%Y-%m-%d'),
                            interval=resolution
                        )
                        
                        # Kiểm tra kết quả
                        if df is not None and not df.empty:
                            break  # Thành công, thoát vòng lặp
                        else:
                            # Nếu df rỗng, thử lại
                            if attempt < max_retries - 1:
                                time.sleep(1)
                                continue
                            
                    except Exception as retry_error:
                        last_error = retry_error
                        error_msg = str(retry_error)
                        
                        # Nếu là lỗi network hoặc timeout, thử lại
                        if any(keyword in error_msg.lower() for keyword in ['timeout', 'connection', 'network', 'retryerror', '429', 'rate limit', 'too many requests', '403', '502', '503', '504']):
                            if attempt < max_retries - 1:
                                # Kiểm tra environment để điều chỉnh wait time
                                is_cloud = os.getenv('STREAMLIT_SHARING_MODE') or os.getenv('STREAMLIT_CLOUD')
                                if is_cloud:
                                    wait_time = min(10 * (attempt + 1), 30)  # Cloud: chờ lâu hơn
                                else:
                                    wait_time = min(2 * (attempt + 1), 5)   # Local: chờ ngắn hơn
                                time.sleep(wait_time)
                                continue
                        else:
                            # Lỗi khác, không retry
                            break
                
                if df is not None and not df.empty:
                    # Chuẩn hóa tên cột
                    df.columns = df.columns.str.lower()
                    
                    # Đảm bảo có cột time hoặc dùng index
                    if 'time' in df.columns:
                        df['time'] = pd.to_datetime(df['time'])
                        df = df.sort_values('time')
                        df = df.set_index('time')
                    elif isinstance(df.index, pd.DatetimeIndex):
                        df = df.sort_index()
                    elif df.index.name == 'time':
                        df.index = pd.to_datetime(df.index)
                        df = df.sort_index()
                    
                    # Đảm bảo có đủ cột cần thiết
                    column_mapping = {
                        'open_price': 'open',
                        'high_price': 'high',
                        'low_price': 'low',
                        'close_price': 'close',
                        'trading_volume': 'volume'
                    }
                    df.rename(columns=column_mapping, inplace=True)
                    
                    required_columns = ['open', 'high', 'low', 'close', 'volume']
                    if all(col in df.columns for col in required_columns):
                        return df  # Trả về ngay nếu thành công
                
            except Exception as e1:
                last_error = e1
                # Tiếp tục để thử fallback
                
            # Bỏ qua fallback yfinance cũ vì đã được di chuyển lên trên
            
            # Nếu có dữ liệu từ bất kỳ nguồn nào, trả về
            if df is not None and not df.empty:
                required_cols = ['open', 'high', 'low', 'close', 'volume']
                if any(col in df.columns for col in required_cols):
                    return df
            
            # Chỉ sử dụng demo data khi được yêu cầu rõ ràng (không phải mặc định)
            if DEMO_DATA_AVAILABLE and os.getenv('FORCE_DEMO_MODE', 'false').lower() == 'true':
                try:
                    demo_df = get_demo_stock_data(symbol, period)
                    if demo_df is not None and not demo_df.empty:
                        st.info(f"🔧 **Chế độ demo được kích hoạt cho mã {symbol}**")
                        return demo_df
                except Exception as demo_error:
                    pass
            
            # Nếu không có demo data, hiển thị thông báo lỗi
            error_msg = str(last_error) if last_error else "Không thể kết nối API"
            
            # Hiển thị thông báo lỗi ngắn gọn hơn
            if any(keyword in error_msg.lower() for keyword in ['403', 'rate limit', 'too many requests']):
                st.error(f"🚫 **Rate limit cho mã {symbol}** - Thử lại sau 30-60 giây")
            elif any(keyword in error_msg.lower() for keyword in ['timeout', 'connection', 'network']):
                st.error(f"🌐 **Lỗi kết nối cho mã {symbol}** - Kiểm tra internet và thử lại")
            else:
                st.error(f"❌ **Không lấy được dữ liệu cho mã {symbol}** - Kiểm tra mã CK hoặc thử lại sau")
            
            return None
            
        except Exception as e:
            st.error(f"💥 **Lỗi hệ thống khi lấy dữ liệu cho {symbol}**\n\n"
                    f"Chi tiết: {str(e)}\n\n"
                    f"Vui lòng thử lại hoặc liên hệ hỗ trợ.")
            return None
    
    @st.cache_data(ttl=3600)
    def get_company_overview(_self, symbol):
        """Lấy thông tin tổng quan công ty"""
        try:
            company = Company(symbol=symbol)
            profile = company.profile()
            if profile is not None and not profile.empty:
                return profile
        except Exception as e:
            pass
        
        # Chỉ fallback demo khi được yêu cầu rõ ràng
        if DEMO_DATA_AVAILABLE and os.getenv('FORCE_DEMO_MODE', 'false').lower() == 'true':
            try:
                return get_demo_company_overview(symbol)
            except Exception:
                pass
        
        # Fallback cuối cùng
        return pd.DataFrame({
            'symbol': [symbol],
            'organName': [f'Công ty {symbol}'],
            'exchange': ['HOSE']
        }, index=[0])
    
    @st.cache_data(ttl=3600)
    def get_financial_report(_self, symbol, period='year', limit=4):
        """Lấy báo cáo tài chính"""
        try:
            from vnstock import Finance
            finance = Finance(symbol=symbol)
            return finance
        except Exception as e:
            return None
    
    @st.cache_data(ttl=3600)
    def get_financial_ratios(_self, symbol):
        """Lấy các chỉ số tài chính"""
        try:
            from vnstock import Finance
            finance = Finance(symbol=symbol)
            ratios = finance.ratio()
            if ratios is not None and not ratios.empty:
                return ratios
        except Exception as e:
            pass
        
        # Chỉ fallback demo khi được yêu cầu rõ ràng
        if DEMO_DATA_AVAILABLE and os.getenv('FORCE_DEMO_MODE', 'false').lower() == 'true':
            try:
                return get_demo_financial_ratios(symbol)
            except Exception:
                pass
        
        return None
    
    @st.cache_data(ttl=86400)  # Cache 24 giờ
    def get_all_stocks(_self):
        """Lấy danh sách tất cả mã chứng khoán"""
        try:
            listing = Listing()
            companies = listing.all_symbols()
            if companies is not None and not companies.empty:
                return companies
        except Exception as e:
            pass
        
        # Chỉ fallback demo khi được yêu cầu rõ ràng
        if DEMO_DATA_AVAILABLE and os.getenv('FORCE_DEMO_MODE', 'false').lower() == 'true':
            try:
                return get_demo_all_stocks()
            except Exception:
                pass
        
        # Fallback cuối cùng
        return pd.DataFrame({
            'symbol': ['VNM', 'FPT', 'VIC', 'HPG', 'VHM', 'VCB', 'VRE', 'MSN', 'PLX', 'TCB', 'GAS', 'MWG', 'SSI', 'VJC'],
            'organName': ['Vinamilk', 'FPT', 'Vingroup', 'Hoa Phat', 'Vinhomes', 'Vietcombank', 'Vincom Retail', 'Masan', 'Petrolimex', 'Techcombank', 'PV Gas', 'Mobile World', 'SSI', 'VietJet'],
            'exchange': ['HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE']
        })
