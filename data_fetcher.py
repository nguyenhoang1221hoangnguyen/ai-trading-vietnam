"""
Module lấy dữ liệu từ vnstock
"""

from vnstock import Quote, Listing, Company
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

class DataFetcher:
    def __init__(self):
        # Không khởi tạo Company và Listing ở đây vì chúng cần symbol
        pass
    
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
            
            # Khởi tạo biến
            df = None
            last_error = None
            
            # Lấy dữ liệu bằng vnstock - Quote cần symbol khi khởi tạo
            try:
                import time
                
                # Thử với retry logic và delay tốt hơn cho cloud
                max_retries = 3
                
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
                                wait_time = min(10 * (attempt + 1), 30)  # Tăng thời gian chờ cho cloud: tối đa 30 giây
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
                
            # Fallback: thử với yfinance nếu vnstock thất bại
            if (df is None or df.empty) or (hasattr(df, 'empty') and df.empty):
                try:
                    import yfinance as yf
                    ticker = f"{symbol}.VN"
                    
                    # Thử với retry cho yfinance
                    max_yf_retries = 2
                    for yf_attempt in range(max_yf_retries):
                        try:
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
                                
                                # Kiểm tra có đủ cột không
                                required_cols = ['open', 'high', 'low', 'close', 'volume']
                                if all(col in df_yf.columns for col in required_cols):
                                    return df_yf  # Trả về ngay nếu thành công
                                else:
                                    df = df_yf  # Vẫn lưu để có thể xử lý sau
                                    break
                        except Exception as yf_error:
                            if yf_attempt < max_yf_retries - 1:
                                time.sleep(2)
                                continue
                            else:
                                pass
                                
                except Exception as e2:
                    pass
            
            # Nếu có dữ liệu từ bất kỳ nguồn nào, trả về
            if df is not None and not df.empty:
                required_cols = ['open', 'high', 'low', 'close', 'volume']
                if any(col in df.columns for col in required_cols):
                    return df
            
            # Nếu không có dữ liệu, hiển thị thông báo thân thiện cho user
            error_msg = str(last_error) if last_error else "Không thể kết nối API"
            
            # Phân loại lỗi và đưa ra thông báo phù hợp
            if any(keyword in error_msg.lower() for keyword in ['403', 'rate limit', 'too many requests']):
                st.error(f"🚫 **Không thể lấy dữ liệu cho mã {symbol}**\n\n"
                        f"**Nguyên nhân có thể:**\n"
                        f"- API đang bị giới hạn tốc độ (rate limit)\n"
                        f"- Quá nhiều request cùng lúc\n\n"
                        f"**Giải pháp:**\n"
                        f"- Thử lại sau 30-60 giây\n"
                        f"- Kiểm tra mã chứng khoán (VD: VNM, FPT, VIC)\n"
                        f"- Sử dụng tính năng cache để giảm tải API")
            elif any(keyword in error_msg.lower() for keyword in ['timeout', 'connection', 'network']):
                st.error(f"🌐 **Lỗi kết nối mạng cho mã {symbol}**\n\n"
                        f"**Nguyên nhân có thể:**\n"
                        f"- Kết nối internet không ổn định\n"
                        f"- Server API tạm thời không khả dụng\n\n"
                        f"**Giải pháp:**\n"
                        f"- Kiểm tra kết nối internet\n"
                        f"- Thử lại sau vài phút\n"
                        f"- Sử dụng mã chứng khoán khác để test")
            else:
                st.error(f"❌ **Không thể lấy dữ liệu cho mã {symbol}**\n\n"
                        f"**Nguyên nhân có thể:**\n"
                        f"- Mã chứng khoán không tồn tại hoặc đã ngừng giao dịch\n"
                        f"- API tạm thời không khả dụng\n\n"
                        f"**Giải pháp:**\n"
                        f"- Kiểm tra lại mã chứng khoán (VD: VNM, FPT, VIC)\n"
                        f"- Thử lại sau 10-15 giây\n"
                        f"- Sử dụng tính năng 'Tổng quan thị trường' để xem danh sách mã hợp lệ")
            
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
            return None
        except Exception as e:
            # Trả về thông tin cơ bản
            return pd.DataFrame({
                'symbol': [symbol],
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
            return None
        except Exception as e:
            return None
    
    @st.cache_data(ttl=86400)  # Cache 24 giờ
    def get_all_stocks(_self):
        """Lấy danh sách tất cả mã chứng khoán"""
        try:
            listing = Listing()
            companies = listing.all_symbols()
            if companies is not None and not companies.empty:
                return companies
            return None
        except Exception as e:
            # Trả về danh sách mẫu nếu không lấy được
            return pd.DataFrame({
                'symbol': ['VNM', 'FPT', 'VIC', 'HPG', 'VHM', 'VCB', 'VRE', 'MSN', 'PLX', 'TCB', 'GAS', 'MWG', 'SSI', 'VJC'],
                'organName': ['Vinamilk', 'FPT', 'Vingroup', 'Hoa Phat', 'Vinhomes', 'Vietcombank', 'Vincom Retail', 'Microsoft', 'Petrolimex', 'Techcombank', 'PV Gas', 'Mobile World', 'SSI', 'VietJet'],
                'exchange': ['HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE', 'HOSE']
            })
