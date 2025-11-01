"""
Demo data cho ứng dụng khi API không khả dụng
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_demo_stock_data(symbol='VNM', period='1Y'):
    """
    Tạo dữ liệu demo cho stock khi API không khả dụng
    """
    # Tính toán số ngày dựa trên period
    if period == '1M':
        days = 30
    elif period == '3M':
        days = 90
    elif period == '6M':
        days = 180
    elif period == '1Y':
        days = 365
    elif period == '3Y':
        days = 1095
    elif period == '5Y':
        days = 1825
    else:
        days = 365
    
    # Tạo date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Loại bỏ weekend (chỉ giữ ngày giao dịch)
    date_range = date_range[date_range.weekday < 5]
    
    # Giá cơ sở cho các mã phổ biến
    base_prices = {
        'VNM': 57.6,  # Vinamilk
        'FPT': 123.5, # FPT
        'VIC': 45.2,  # Vingroup
        'VCB': 89.3,  # Vietcombank
        'HPG': 25.8,  # Hoa Phat
        'MSN': 98.7,  # Masan
        'TCB': 28.4,  # Techcombank
        'VHM': 42.1,  # Vinhomes
        'BID': 52.3,  # BIDV
        'CTG': 35.6   # VietinBank
    }
    
    base_price = base_prices.get(symbol, 50.0)
    
    # Tạo dữ liệu giá với random walk
    np.random.seed(hash(symbol) % 2**32)  # Seed dựa trên symbol để consistent
    
    prices = []
    current_price = base_price
    
    for i, date in enumerate(date_range):
        # Random walk với trend nhẹ
        change_pct = np.random.normal(0.001, 0.02)  # Trung bình tăng 0.1%/ngày, volatility 2%
        current_price *= (1 + change_pct)
        
        # Đảm bảo giá không âm
        current_price = max(current_price, base_price * 0.5)
        
        # Tạo OHLC data
        daily_volatility = abs(np.random.normal(0, 0.015))
        
        open_price = current_price * (1 + np.random.normal(0, 0.005))
        high_price = max(open_price, current_price) * (1 + daily_volatility)
        low_price = min(open_price, current_price) * (1 - daily_volatility)
        close_price = current_price
        
        # Volume (random nhưng realistic)
        base_volume = 1000000 if symbol in ['VNM', 'FPT', 'VIC'] else 500000
        volume = int(base_volume * (0.5 + np.random.exponential(0.5)))
        
        prices.append({
            'date': date,
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume': volume
        })
    
    df = pd.DataFrame(prices)
    df.set_index('date', inplace=True)
    
    return df

def get_demo_company_overview(symbol='VNM'):
    """
    Tạo thông tin công ty demo
    """
    company_info = {
        'VNM': {
            'organName': 'Công ty Cổ phần Sữa Việt Nam',
            'organShortName': 'Vinamilk',
            'organTypeCode': 'CT',
            'icbName': 'Thực phẩm & Đồ uống',
            'comGroupCode': 'HOSE',
            'establishedYear': 1976,
            'noEmployees': 8500,
            'noShareholders': 45000,
            'marketCap': 138000000000000,  # 138 tỷ USD
            'sharesOutstanding': 2400000000
        },
        'FPT': {
            'organName': 'Công ty Cổ phần FPT',
            'organShortName': 'FPT Corporation',
            'organTypeCode': 'CT',
            'icbName': 'Công nghệ Thông tin',
            'comGroupCode': 'HOSE',
            'establishedYear': 1988,
            'noEmployees': 42000,
            'noShareholders': 35000,
            'marketCap': 89000000000000,
            'sharesOutstanding': 720000000
        },
        'VIC': {
            'organName': 'Tập đoàn Vingroup',
            'organShortName': 'Vingroup',
            'organTypeCode': 'CT',
            'icbName': 'Bất động sản',
            'comGroupCode': 'HOSE',
            'establishedYear': 1993,
            'noEmployees': 65000,
            'noShareholders': 28000,
            'marketCap': 210000000000000,
            'sharesOutstanding': 4650000000
        }
    }
    
    default_info = {
        'organName': f'Công ty Cổ phần {symbol}',
        'organShortName': symbol,
        'organTypeCode': 'CT',
        'icbName': 'Đa ngành',
        'comGroupCode': 'HOSE',
        'establishedYear': 2000,
        'noEmployees': 1000,
        'noShareholders': 5000,
        'marketCap': 10000000000000,
        'sharesOutstanding': 100000000
    }
    
    info = company_info.get(symbol, default_info)
    return pd.DataFrame([info])

def get_demo_financial_ratios(symbol='VNM'):
    """
    Tạo chỉ số tài chính demo
    """
    ratios_data = {
        'VNM': {
            'pe': 15.2,
            'pb': 2.8,
            'roe': 18.5,
            'roa': 12.3,
            'debtToEquity': 0.35,
            'currentRatio': 2.1,
            'quickRatio': 1.8,
            'grossMargin': 45.2,
            'netMargin': 22.1,
            'eps': 3.8,
            'bvps': 20.5,
            'dividendYield': 4.2
        },
        'FPT': {
            'pe': 18.7,
            'pb': 3.2,
            'roe': 17.1,
            'roa': 9.8,
            'debtToEquity': 0.28,
            'currentRatio': 1.9,
            'quickRatio': 1.6,
            'grossMargin': 38.5,
            'netMargin': 15.8,
            'eps': 6.6,
            'bvps': 38.5,
            'dividendYield': 2.8
        },
        'VIC': {
            'pe': 12.5,
            'pb': 1.9,
            'roe': 15.2,
            'roa': 6.8,
            'debtToEquity': 0.85,
            'currentRatio': 1.4,
            'quickRatio': 0.9,
            'grossMargin': 42.1,
            'netMargin': 18.5,
            'eps': 3.6,
            'bvps': 23.8,
            'dividendYield': 3.5
        }
    }
    
    default_ratios = {
        'pe': 16.0,
        'pb': 2.5,
        'roe': 15.0,
        'roa': 8.0,
        'debtToEquity': 0.5,
        'currentRatio': 1.8,
        'quickRatio': 1.4,
        'grossMargin': 35.0,
        'netMargin': 12.0,
        'eps': 2.5,
        'bvps': 25.0,
        'dividendYield': 3.0
    }
    
    ratios = ratios_data.get(symbol, default_ratios)
    return pd.DataFrame([ratios])

def get_demo_all_stocks():
    """
    Tạo danh sách các mã chứng khoán demo
    """
    stocks_data = [
        {'symbol': 'VNM', 'organName': 'Công ty Cổ phần Sữa Việt Nam', 'exchange': 'HOSE'},
        {'symbol': 'FPT', 'organName': 'Công ty Cổ phần FPT', 'exchange': 'HOSE'},
        {'symbol': 'VIC', 'organName': 'Tập đoàn Vingroup', 'exchange': 'HOSE'},
        {'symbol': 'VCB', 'organName': 'Ngân hàng TMCP Ngoại thương Việt Nam', 'exchange': 'HOSE'},
        {'symbol': 'HPG', 'organName': 'Công ty Cổ phần Tập đoàn Hoa Phát', 'exchange': 'HOSE'},
        {'symbol': 'MSN', 'organName': 'Công ty Cổ phần Tập đoàn Masan', 'exchange': 'HOSE'},
        {'symbol': 'TCB', 'organName': 'Ngân hàng TMCP Kỹ thương Việt Nam', 'exchange': 'HOSE'},
        {'symbol': 'VHM', 'organName': 'Công ty Cổ phần Vinhomes', 'exchange': 'HOSE'},
        {'symbol': 'BID', 'organName': 'Ngân hàng TMCP Đầu tư và Phát triển Việt Nam', 'exchange': 'HOSE'},
        {'symbol': 'CTG', 'organName': 'Ngân hàng TMCP Công thương Việt Nam', 'exchange': 'HOSE'},
        {'symbol': 'GAS', 'organName': 'Tổng Công ty Khí Việt Nam', 'exchange': 'HOSE'},
        {'symbol': 'SAB', 'organName': 'Công ty Cổ phần Sabeco', 'exchange': 'HOSE'},
        {'symbol': 'PLX', 'organName': 'Tập đoàn Xăng dầu Việt Nam', 'exchange': 'HOSE'},
        {'symbol': 'POW', 'organName': 'Tổng Công ty Điện lực Dầu khí Việt Nam', 'exchange': 'HOSE'},
        {'symbol': 'MWG', 'organName': 'Công ty Cổ phần Đầu tư Thế giới Di động', 'exchange': 'HOSE'},
    ]
    
    return pd.DataFrame(stocks_data)

def is_demo_mode():
    """
    Kiểm tra xem có đang ở demo mode không
    """
    import os
    return os.getenv('STREAMLIT_DEMO_MODE', 'false').lower() == 'true'
