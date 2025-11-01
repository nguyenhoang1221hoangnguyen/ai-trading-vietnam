"""
Cấu hình cho ứng dụng AI Trading
"""

# Cấu hình chỉ số kỹ thuật
TECHNICAL_INDICATORS = {
    'RSI_PERIOD': 14,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_STD': 2,
    'SMA_SHORT': 20,
    'SMA_MEDIUM': 50,
    'SMA_LONG': 200,
    'EMA_SHORT': 12,
    'EMA_LONG': 26,
    'ADX_PERIOD': 14,
    'VOLUME_SMA': 20
}

# Ngưỡng tín hiệu
SIGNAL_THRESHOLDS = {
    'RSI_OVERSOLD': 30,
    'RSI_OVERBOUGHT': 70,
    'ADX_TREND': 25,
    'VOLUME_SPIKE': 1.5
}

# Cấu hình thời gian
TIME_PERIODS = {
    'SHORT_TERM': '3M',  # 3 tháng
    'MEDIUM_TERM': '1Y',  # 1 năm
    'LONG_TERM': '3Y'  # 3 năm
}

# Cấu hình điểm số
SCORING_WEIGHTS = {
    'TECHNICAL': 0.6,
    'FUNDAMENTAL': 0.4
}

# Màu sắc cho biểu đồ
CHART_COLORS = {
    'PRICE': '#1f77b4',
    'SMA_SHORT': '#ff7f0e',
    'SMA_MEDIUM': '#2ca02c',
    'SMA_LONG': '#d62728',
    'VOLUME': '#9467bd',
    'BUY_SIGNAL': '#00ff00',
    'SELL_SIGNAL': '#ff0000'
}

