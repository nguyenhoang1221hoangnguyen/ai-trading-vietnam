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
            
            # Lấy dữ liệu bằng vnstock - Quote cần symbol khi khởi tạo
            try:
                import time
                quote = Quote(symbol=symbol)
                
                # Thử với retry logic
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        df = quote.history(
                            start=start_date.strftime('%Y-%m-%d'),
                            end=end_date.strftime('%Y-%m-%d'),
                            interval=resolution
                        )
                        break  # Thành công, thoát vòng lặp
                    except Exception as retry_error:
                        if attempt < max_retries - 1:
                            time.sleep(1)  # Đợi 1 giây trước khi thử lại
                            continue
                        else:
                            raise retry_error
                
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
                        return df
                
            except Exception as e1:
                # Fallback: thử với yfinance
                try:
                    import yfinance as yf
                    ticker = f"{symbol}.VN"
                    df = yf.download(ticker, start=start_date, end=end_date, interval='1d', progress=False, auto_adjust=False)
                    
                    if df is not None and not df.empty:
                        df.columns = df.columns.str.lower().str.replace(' ', '_')
                        if 'adj_close' in df.columns:
                            df['close'] = df['adj_close']
                        df = df.sort_index()
                        return df
                except Exception as e2:
                    pass
                
                # Chỉ hiển thị warning nếu không phải là lỗi thông thường
                error_msg = str(e1)
                if 'RetryError' not in error_msg and 'ValueError' not in error_msg:
                    st.warning(f"Không thể lấy dữ liệu từ vnstock cho {symbol}: {error_msg[:100]}")
            
            return None
            
        except Exception as e:
            st.error(f"Lỗi khi lấy dữ liệu cho {symbol}: {str(e)}")
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
