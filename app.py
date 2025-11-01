"""
Ứng dụng AI Trading - Hỗ trợ đầu tư chứng khoán Việt Nam
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import time
import os

from data_fetcher import DataFetcher
from technical_analysis import TechnicalAnalyzer
from fundamental_analysis import FundamentalAnalyzer
from trading_signals import TradingSignalGenerator
from stock_screener import StockScreener
from cached_stock_screener import CachedStockScreener
from data_cache import DataCache
from config import CHART_COLORS

# Import demo data functions
try:
    from demo_data import is_demo_mode
    DEMO_AVAILABLE = True
except ImportError:
    DEMO_AVAILABLE = False
    def is_demo_mode():
        return False

# Cấu hình trang
st.set_page_config(
    page_title="AI Trading - Đầu tư chứng khoán thông minh",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .signal-buy {
        color: #00ff00;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .signal-sell {
        color: #ff0000;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .signal-hold {
        color: #ffaa00;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .info-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .danger-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo session state
if 'data_fetcher' not in st.session_state:
    st.session_state.data_fetcher = DataFetcher()

if 'stock_screener' not in st.session_state:
    st.session_state.stock_screener = StockScreener()

if 'cached_screener' not in st.session_state:
    st.session_state.cached_screener = CachedStockScreener()

if 'data_cache' not in st.session_state:
    st.session_state.data_cache = DataCache()

def plot_candlestick_chart(df, symbol, indicators=True):
    """Vẽ biểu đồ nến với các chỉ báo kỹ thuật"""
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.6, 0.2, 0.2],
        subplot_titles=(f'{symbol} - Biểu đồ giá (Cập nhật: {datetime.now().strftime("%H:%M:%S")})', 'MACD', 'RSI')
    )
    
    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Giá',
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ),
        row=1, col=1
    )
    
    if indicators:
        # Moving Averages
        if 'sma_20' in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df['sma_20'], name='SMA 20',
                          line=dict(color='#ff7f0e', width=1)),
                row=1, col=1
            )
        
        if 'sma_50' in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df['sma_50'], name='SMA 50',
                          line=dict(color='#2ca02c', width=1)),
                row=1, col=1
            )
        
        if 'sma_200' in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df['sma_200'], name='SMA 200',
                          line=dict(color='#d62728', width=1)),
                row=1, col=1
            )
        
        # Bollinger Bands
        if 'bb_high' in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df['bb_high'], name='BB Upper',
                          line=dict(color='rgba(250, 128, 114, 0.5)', width=1, dash='dash')),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=df.index, y=df['bb_low'], name='BB Lower',
                          line=dict(color='rgba(250, 128, 114, 0.5)', width=1, dash='dash'),
                          fill='tonexty', fillcolor='rgba(250, 128, 114, 0.1)'),
                row=1, col=1
            )
        
        # MACD
        if 'macd' in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df['macd'], name='MACD',
                          line=dict(color='#1f77b4', width=1)),
                row=2, col=1
            )
            fig.add_trace(
                go.Scatter(x=df.index, y=df['macd_signal'], name='Signal',
                          line=dict(color='#ff7f0e', width=1)),
                row=2, col=1
            )
            
            # MACD Histogram
            colors = ['green' if val >= 0 else 'red' for val in df['macd_diff']]
            fig.add_trace(
                go.Bar(x=df.index, y=df['macd_diff'], name='Histogram',
                      marker_color=colors, opacity=0.3),
                row=2, col=1
            )
        
        # RSI
        if 'rsi' in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df['rsi'], name='RSI',
                          line=dict(color='#9467bd', width=2)),
                row=3, col=1
            )
            
            # RSI levels
            fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=3, col=1)
            fig.add_hline(y=50, line_dash="dash", line_color="gray", opacity=0.3, row=3, col=1)
    
    # Volume
    # fig.add_trace(
    #     go.Bar(x=df.index, y=df['volume'], name='Volume',
    #           marker_color='rgba(128, 128, 128, 0.3)'),
    #     row=4, col=1
    # )
    
    # Cập nhật layout với zoom/pan cải tiến
    fig.update_layout(
        height=900,
        xaxis_rangeslider_visible=False,
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        # Cải thiện zoom và pan
        dragmode='pan',  # Mặc định là pan mode
        # Thêm các nút zoom/pan
        modebar=dict(
            orientation='v',
            bgcolor='rgba(255,255,255,0.8)',
            color='rgba(0,0,0,0.5)',
            activecolor='rgba(0,0,0,0.9)'
        ),
        # Cấu hình xaxis với mốc thời gian
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            showspikes=True,
            spikecolor="orange",
            spikesnap="cursor",
            spikemode="across",
            # Hiển thị mốc thời gian rõ ràng
            tickformat='%d/%m<br>%H:%M',
            tickangle=0,
            nticks=10
        ),
        # Cấu hình yaxis
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            showspikes=True,
            spikecolor="orange",
            spikesnap="cursor",
            spikemode="across"
        )
    )
    
    # Cập nhật axes với grid và spike
    fig.update_yaxes(
        title_text="Giá (VNĐ)", 
        row=1, col=1,
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)',
        showspikes=True,
        spikecolor="orange",
        spikesnap="cursor",
        spikemode="across"
    )
    fig.update_yaxes(
        title_text="MACD", 
        row=2, col=1,
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)'
    )
    fig.update_yaxes(
        title_text="RSI", 
        row=3, col=1,
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)'
    )
    
    # Cập nhật xaxis cho tất cả subplot với mốc thời gian
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)',
        showspikes=True,
        spikecolor="orange",
        spikesnap="cursor",
        spikemode="across",
        tickformat='%d/%m %H:%M',
        tickangle=45
    )
    
    return fig

def show_analysis_page():
    """Trang phân tích mã chứng khoán"""
    st.markdown('<div class="main-header">📊 Phân tích mã chứng khoán</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Nếu đang auto-refresh, dùng giá trị từ session state
        if st.session_state.get('auto_refresh', False) and 'last_symbol' in st.session_state:
            default_symbol = st.session_state['last_symbol']
        else:
            default_symbol = "VNM"
        
        symbol = st.text_input("Nhập mã chứng khoán:", value=default_symbol, max_chars=10).upper()
    
    with col2:
        # Nếu đang auto-refresh, dùng giá trị từ session state
        if st.session_state.get('auto_refresh', False) and 'last_period' in st.session_state:
            default_period = st.session_state['last_period']
            period_options = ['1M', '3M', '6M', '1Y', '3Y', '5Y']
            default_index = period_options.index(default_period) if default_period in period_options else 3
        else:
            default_index = 3
        
        period = st.selectbox("Khung thời gian:", 
                             ['1M', '3M', '6M', '1Y', '3Y', '5Y'],
                             index=default_index)
    
    # Nếu đang auto-refresh, tự động phân tích
    should_analyze = False
    is_auto_refresh_mode = st.session_state.get('auto_refresh', False)
    
    if is_auto_refresh_mode:
        # Tự động phân tích khi đang ở chế độ auto-refresh
        should_analyze = True
    elif st.button("🔍 Phân tích", type="primary", width='stretch'):
        should_analyze = True
    
    if should_analyze:
        with st.spinner(f'Đang lấy dữ liệu cho {symbol}...'):
            # Lấy dữ liệu
            stock_data = st.session_state.data_fetcher.get_stock_data(symbol, period=period)
            
            if stock_data is None or len(stock_data) < 20:
                st.error(f"❌ Không thể lấy dữ liệu cho mã {symbol}")
                st.info(f"""
                **Nguyên nhân có thể:**
                - Mã chứng khoán không tồn tại hoặc đã ngừng giao dịch
                - Vấn đề kết nối mạng hoặc API tạm thời không khả dụng
                - Rate limit từ API (thử lại sau vài giây)
                
                **Giải pháp:**
                - Kiểm tra lại mã chứng khoán (VD: VNM, FPT, VIC)
                - Thử lại sau 10-15 giây
                - Kiểm tra kết nối internet
                """)
                return
            
            # Lấy thông tin công ty
            company_info = st.session_state.data_fetcher.get_company_overview(symbol)
            
            # Lấy chỉ số tài chính
            ratios_data = st.session_state.data_fetcher.get_financial_ratios(symbol)
            financial_data = st.session_state.data_fetcher.get_financial_report(symbol)
            
            # Phân tích
            signal_gen = TradingSignalGenerator(stock_data, financial_data, ratios_data)
            recommendation = signal_gen.get_recommendation()
            
            # Hiển thị thông tin công ty
            if company_info is not None and not company_info.empty:
                st.markdown("### 🏢 Thông tin công ty")
                info = company_info.iloc[0] if len(company_info) > 0 else company_info
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Sàn", info.get('exchange', 'N/A'))
                with col2:
                    st.metric("Ngành", info.get('industryName', 'N/A'))
                with col3:
                    st.metric("Vốn hóa", f"{info.get('marketCap', 0):,.0f} tỷ VNĐ" if 'marketCap' in info.index else 'N/A')
            
            st.markdown("---")
            
            # Tín hiệu tổng hợp
            st.markdown("### 🎯 Tín hiệu đầu tư")
            
            signal_info = recommendation['signal']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                signal_class = "signal-buy" if "MUA" in signal_info['signal'] else "signal-sell" if "BÁN" in signal_info['signal'] else "signal-hold"
                st.markdown(f'<p class="{signal_class}">{signal_info["color"]} {signal_info["signal"]}</p>', unsafe_allow_html=True)
            
            with col2:
                st.metric("Điểm tổng hợp", f"{signal_info['overall_score']:.1f}/100")
            
            with col3:
                st.metric("Điểm kỹ thuật", f"{signal_info['technical_score']:.1f}/100")
            
            with col4:
                st.metric("Điểm cơ bản", f"{signal_info['fundamental_score']:.1f}/100")
            
            # Xu hướng
            st.markdown(f"**Xu hướng:** {recommendation['trend']}")
            
            # Khung thời gian đầu tư
            timeframes = signal_gen.get_investment_timeframe()
            st.markdown(f"**Phù hợp với đầu tư:** {', '.join(timeframes)}")
            
            st.markdown("---")
            
            # Tín hiệu kỹ thuật chi tiết
            if recommendation['technical_signals']:
                st.markdown("### 📈 Tín hiệu kỹ thuật")
                
                buy_signals = [s for s in recommendation['technical_signals'] if s['type'] == 'BUY']
                sell_signals = [s for s in recommendation['technical_signals'] if s['type'] == 'SELL']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if buy_signals:
                        st.markdown("**🟢 Tín hiệu MUA:**")
                        for signal in buy_signals:
                            strength_emoji = "💪" if signal['strength'] == 'STRONG' else "👍"
                            st.markdown(f"- {strength_emoji} **{signal['indicator']}**: {signal['reason']}")
                    else:
                        st.info("Không có tín hiệu mua")
                
                with col2:
                    if sell_signals:
                        st.markdown("**🔴 Tín hiệu BÁN:**")
                        for signal in sell_signals:
                            strength_emoji = "💪" if signal['strength'] == 'STRONG' else "👍"
                            st.markdown(f"- {strength_emoji} **{signal['indicator']}**: {signal['reason']}")
                    else:
                        st.info("Không có tín hiệu bán")
            
            st.markdown("---")
            
            # Điểm vào và thoát lệnh
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📍 Điểm vào lệnh (Entry Points)")
                entry_points = recommendation['entry_points']
                if entry_points:
                    for point in entry_points:
                        st.success(f"**{point['type']}** tại giá **{point['price']*1000:,.0f}** VNĐ\n\n_{point['reason']}_")
                else:
                    st.info("Chưa xác định được điểm vào tối ưu")
            
            with col2:
                st.markdown("### 🎯 Điểm thoát lệnh (Exit Points)")
                exit_points = recommendation['exit_points']
                if exit_points:
                    for point in exit_points:
                        if point['type'] == 'CHỐT LỜI':
                            st.success(f"**{point['type']}** tại giá **{point['price']*1000:,.0f}** VNĐ (+{point.get('profit_pct', 0):.1f}%)\n\n_{point['reason']}_")
                        else:
                            st.error(f"**{point['type']}** tại giá **{point['price']*1000:,.0f}** VNĐ ({point.get('loss_pct', 0):.1f}%)\n\n_{point['reason']}_")
                else:
                    st.info("Chưa xác định được điểm thoát")
            
            # Risk/Reward Ratio
            if recommendation['risk_reward']:
                st.markdown("---")
                st.markdown("### ⚖️ Tỷ lệ Rủi ro/Lợi nhuận")
                rr = recommendation['risk_reward']
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Tỷ lệ R:R", f"1:{rr['ratio']:.2f}")
                with col2:
                    st.metric("Chốt lời", f"{rr['take_profit']*1000:,.0f} VNĐ")
                with col3:
                    st.metric("Cắt lỗ", f"{rr['stop_loss']*1000:,.0f} VNĐ")
                with col4:
                    color = "normal" if rr['ratio'] >= 2 else "inverse"
                    st.metric("Đánh giá", "Tốt ✅" if rr['ratio'] >= 2 else "Cân nhắc ⚠️", delta_color=color)
            
            # Phân tích cơ bản
            if 'fundamental' in recommendation:
                st.markdown("---")
                st.markdown("### 💼 Phân tích cơ bản")
                
                fund = recommendation['fundamental']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Định giá
                    st.markdown("**📊 Định giá**")
                    val = fund['valuation']
                    st.markdown(f"_Kết luận: **{val['valuation']}**_")
                    for detail in val['details']:
                        st.markdown(detail)
                    
                    st.markdown("")
                    
                    # Khả năng sinh lời
                    st.markdown("**💰 Khả năng sinh lời**")
                    prof = fund['profitability']
                    st.markdown(f"_Đánh giá: **{prof['profitability']}**_")
                    for detail in prof['details']:
                        st.markdown(detail)
                
                with col2:
                    # Sức khỏe tài chính
                    st.markdown("**🏥 Sức khỏe tài chính**")
                    health = fund['financial_health']
                    st.markdown(f"_Tình trạng: **{health['status']}**_")
                    for detail in health['details']:
                        st.markdown(detail)
                    
                    st.markdown("")
                    
                    # Tăng trưởng
                    st.markdown("**📈 Tăng trưởng**")
                    growth = fund['growth']
                    st.markdown(f"_Xu hướng: **{growth['trend']}**_")
                    for detail in growth['details']:
                        st.markdown(detail)
            
            st.markdown("---")
            
            # Biểu đồ với auto-refresh
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown("### 📈 Biểu đồ kỹ thuật")
            
            with col2:
                # Toggle auto-refresh
                auto_refresh = st.checkbox(
                    "🔄 Tự động cập nhật",
                    value=st.session_state.get('auto_refresh', False),
                    key='auto_refresh_checkbox'
                )
                st.session_state['auto_refresh'] = auto_refresh
            
            with col3:
                if auto_refresh:
                    refresh_interval = st.selectbox(
                        "⏱️ Tần suất:",
                        [5, 10, 30, 60],
                        index=1,  # Mặc định 10 giây
                        format_func=lambda x: f"{x}s",
                        key='refresh_interval'
                    )
                    st.session_state['refresh_interval'] = refresh_interval
                else:
                    refresh_interval = st.session_state.get('refresh_interval', 10)
            
            # Hiển thị thời gian cập nhật cuối
            if 'last_update_time' in st.session_state:
                last_update = st.session_state['last_update_time']
                time_diff = time.time() - last_update
                if time_diff < 60:
                    st.caption(f"⏰ Cập nhật lần cuối: {int(time_diff)} giây trước | 📊 Dữ liệu: {datetime.fromtimestamp(last_update).strftime('%H:%M:%S')}")
                else:
                    st.caption(f"⏰ Cập nhật lần cuối: {int(time_diff/60)} phút trước | 📊 Dữ liệu: {datetime.fromtimestamp(last_update).strftime('%H:%M:%S')}")
            
            # Lấy và hiển thị biểu đồ
            analyzer = TechnicalAnalyzer(stock_data)
            df_with_indicators = analyzer.add_all_indicators()
            
            fig = plot_candlestick_chart(df_with_indicators, symbol, indicators=True)
            
            # Container cho biểu đồ với cấu hình tương tác cải tiến
            chart_container = st.empty()
            
            # Cấu hình plotly với các tính năng tương tác nâng cao
            config = {
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToAdd': [
                    'drawline',
                    'drawopenpath',
                    'drawclosedpath',
                    'drawcircle',
                    'drawrect',
                    'eraseshape'
                ],
                'modeBarButtonsToRemove': [],
                'scrollZoom': True,  # Cho phép zoom bằng scroll wheel
                'doubleClick': 'reset+autosize',  # Double click để reset zoom
                'showTips': True,
                'responsive': True
            }
            
            chart_container.plotly_chart(
                fig, 
                width='stretch',  # Thay thế use_container_width
                config=config,
                key=f"chart_{symbol}_{int(time.time())}"  # Key unique để force update
            )
            
            # Auto-refresh logic cải tiến với st.rerun()
            if auto_refresh:
                # Lưu thời gian cập nhật
                current_time = time.time()
                st.session_state['last_update_time'] = current_time
                
                # Lưu symbol và period vào session state
                st.session_state['last_symbol'] = symbol
                st.session_state['last_period'] = period
                
                # Kiểm tra xem đã đến lúc refresh chưa
                last_refresh = st.session_state.get('last_refresh_time', 0)
                if current_time - last_refresh >= refresh_interval:
                    st.session_state['last_refresh_time'] = current_time
                    st.info(f"🔄 Đã cập nhật lúc {datetime.now().strftime('%H:%M:%S')} - Tự động cập nhật mỗi {refresh_interval}s")
                    time.sleep(1)  # Ngắt ngủ để user thấy thông báo
                    st.rerun()
                else:
                    # Hiển thị countdown
                    remaining = refresh_interval - int(current_time - last_refresh)
                    if remaining > 0:
                        st.info(f"🔄 Tự động cập nhật sau {remaining} giây... (Bỏ tick để tắt)")
                        time.sleep(1)
                        st.rerun()

def show_screener_page():
    """Trang tìm kiếm mã chứng khoán tiềm năng"""
    st.markdown('<div class="main-header">🔎 Tìm kiếm cổ phiếu tiềm năng</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🎯 Quét thị trường", "📊 Lọc theo tiêu chí", "🚀 Cổ phiếu đặc biệt"])
    
    with tab1:
        st.markdown("### Quét thị trường tìm cổ phiếu phù hợp")
        
        col1, col2 = st.columns(2)
        
        with col1:
            investment_type = st.selectbox(
                "Loại đầu tư:",
                ['SHORT_TERM', 'MEDIUM_TERM', 'LONG_TERM'],
                format_func=lambda x: {
                    'SHORT_TERM': '📅 Ngắn hạn (1-3 tháng)',
                    'MEDIUM_TERM': '📆 Trung hạn (3-12 tháng)',
                    'LONG_TERM': '📅 Dài hạn (> 1 năm)'
                }[x]
            )
        
        with col2:
            top_n = st.slider("Số lượng cổ phiếu:", 5, 50, 20)
        
        if st.button("🚀 Bắt đầu quét", type="primary", width='stretch'):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def update_progress(current, total, symbol):
                progress = current / total
                progress_bar.progress(progress)
                status_text.text(f"Đang quét: {symbol} ({current}/{total})")
            
            with st.spinner("Đang quét thị trường..."):
                results = st.session_state.stock_screener.scan_market(
                    investment_type=investment_type,
                    top_n=top_n,
                    progress_callback=update_progress
                )
            
            progress_bar.empty()
            status_text.empty()
            
            if results:
                st.success(f"✅ Tìm thấy {len(results)} cổ phiếu phù hợp!")
                
                # Hiển thị bảng kết quả
                df_results = pd.DataFrame(results)
                df_results = df_results[['symbol', 'name', 'exchange', 'price', 'overall_score', 
                                        'technical_score', 'fundamental_score', 'signal']]
                
                df_results.columns = ['Mã', 'Tên', 'Sàn', 'Giá', 'Điểm tổng', 'Điểm KT', 'Điểm CB', 'Tín hiệu']
                
                # Format
                df_results['Giá'] = df_results['Giá'].apply(lambda x: f"{x*1000:,.0f}")
                df_results['Điểm tổng'] = df_results['Điểm tổng'].apply(lambda x: f"{x:.1f}")
                df_results['Điểm KT'] = df_results['Điểm KT'].apply(lambda x: f"{x:.1f}")
                df_results['Điểm CB'] = df_results['Điểm CB'].apply(lambda x: f"{x:.1f}")
                
                st.dataframe(df_results, width='stretch', hide_index=True)
                
                # Top 3
                st.markdown("### 🏆 Top 3 cổ phiếu xuất sắc nhất")
                cols = st.columns(3)
                for idx, (i, row) in enumerate(df_results.head(3).iterrows()):
                    with cols[idx]:
                        st.markdown(f"""
                        <div class="success-box">
                            <h3>#{idx+1} {row['Mã']}</h3>
                            <p><strong>{row['Tên']}</strong></p>
                            <p>Giá: <strong>{row['Giá']} VNĐ</strong></p>
                            <p>Điểm: <strong>{row['Điểm tổng']}/100</strong></p>
                            <p>Tín hiệu: <strong>{row['Tín hiệu']}</strong></p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Không tìm thấy cổ phiếu phù hợp với tiêu chí.")
    
    with tab2:
        st.markdown("### Lọc cổ phiếu theo tiêu chí kỹ thuật")
        
        col1, col2 = st.columns(2)
        
        with col1:
            rsi_min, rsi_max = st.slider("RSI:", 0, 100, (30, 70))
            trend = st.selectbox("Xu hướng:", ['TẤT CẢ', 'TĂNG', 'GIẢM', 'SIDEWAY'])
        
        with col2:
            volume_spike = st.checkbox("Khối lượng tăng đột biến")
        
        if st.button("🔍 Lọc", type="primary", width='stretch'):
            criteria = {
                'rsi_range': (rsi_min, rsi_max),
                'volume_spike': volume_spike
            }
            
            if trend != 'TẤT CẢ':
                criteria['trend'] = trend
            
            with st.spinner("Đang lọc cổ phiếu..."):
                results = st.session_state.stock_screener.filter_by_technical_criteria(criteria)
            
            if results:
                st.success(f"✅ Tìm thấy {len(results)} cổ phiếu!")
                df_results = pd.DataFrame(results)
                st.dataframe(df_results, width='stretch', hide_index=True)
            else:
                st.warning("⚠️ Không tìm thấy cổ phiếu phù hợp.")
    
    with tab3:
        st.markdown("### Cổ phiếu có tín hiệu đặc biệt")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Tìm cổ phiếu đang Breakout", width='stretch'):
                with st.spinner("Đang tìm kiếm..."):
                    results = st.session_state.stock_screener.find_breakout_stocks()
                
                if results:
                    st.success(f"✅ Tìm thấy {len(results)} cổ phiếu breakout!")
                    df_results = pd.DataFrame(results)
                    st.dataframe(df_results, width='stretch', hide_index=True)
                else:
                    st.info("Không tìm thấy cổ phiếu breakout.")
        
        with col2:
            if st.button("📉 Tìm cổ phiếu quá bán", width='stretch'):
                with st.spinner("Đang tìm kiếm..."):
                    results = st.session_state.stock_screener.find_oversold_stocks()
                
                if results:
                    st.success(f"✅ Tìm thấy {len(results)} cổ phiếu quá bán!")
                    df_results = pd.DataFrame(results)
                    st.dataframe(df_results, width='stretch', hide_index=True)
                else:
                    st.info("Không tìm thấy cổ phiếu quá bán.")

def show_market_overview_page():
    """Trang tổng quan thị trường với cached data"""
    st.markdown('<div class="main-header">📈 Tổng quan thị trường</div>', unsafe_allow_html=True)
    
    # Cache stats
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        stats = st.session_state.data_cache.get_cache_stats()
        
        with col1:
            st.metric("Tổng số mã", f"{stats['total_symbols']:,}")
        with col2:
            st.metric("Dữ liệu records", f"{stats['total_records']:,}")
        with col3:
            st.metric("Kích thước DB", f"{stats['db_size_mb']} MB")
        with col4:
            st.metric("Khoảng thời gian", stats['date_range'].split(' to ')[1] if ' to ' in stats['date_range'] else 'N/A')
    except:
        st.warning("⚠️ Chưa có dữ liệu cache. Vui lòng cập nhật cache trước.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Cập nhật Cache (20 mã)", type="primary"):
                with st.spinner("Đang cập nhật cache..."):
                    success = st.session_state.data_cache.bulk_cache_update(max_symbols=20)
                    if success > 0:
                        st.success(f"✅ Đã cập nhật {success} mã thành công!")
                        st.rerun()
                    else:
                        st.error("❌ Cập nhật thất bại")
        
        with col2:
            if st.button("📊 Xem hướng dẫn Cache"):
                st.info("""
                **Cách cập nhật cache:**
                1. Mở terminal trong thư mục project
                2. Chạy: `python cache_manager.py --action update --max 50`
                3. Đợi hoàn thành và refresh trang này
                """)
        return
    
    st.markdown("---")
    
    # Tabs cho các chức năng
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Market Scanner", "🏆 Top Performers", "📊 Market Analysis", "⚙️ Cache Management"])
    
    with tab1:
        st.markdown("### 🔍 Market Scanner - Quét thị trường nhanh")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            max_symbols = st.slider("Số lượng mã quét", 10, 500, 50, 10)
        with col2:
            update_cache = st.checkbox("🔄 Cập nhật cache trước khi quét")
        with col3:
            analysis_type = st.selectbox("Loại phân tích", ["Tổng hợp", "Kỹ thuật", "Cơ bản"])
        
        if st.button("🚀 Bắt đầu quét thị trường", type="primary", width='stretch'):
            with st.spinner(f"Đang quét {max_symbols} mã chứng khoán..."):
                try:
                    # Tạo progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    def progress_callback(current, total, message):
                        progress = current / total
                        progress_bar.progress(progress)
                        status_text.text(f"[{current}/{total}] {message}")
                    
                    # Quét thị trường
                    market_df = st.session_state.cached_screener.get_market_comparison_table(
                        update_cache=update_cache,
                        max_symbols=max_symbols
                    )
                    
                    progress_bar.empty()
                    status_text.empty()
                    
                    if not market_df.empty:
                        st.success(f"✅ Hoàn thành quét {len(market_df)} mã chứng khoán!")
                        
                        # Lưu vào session state
                        st.session_state['market_df'] = market_df
                        st.session_state['scan_timestamp'] = pd.Timestamp.now()
                        
                        # Hiển thị kết quả tóm tắt
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            buy_count = len(market_df[market_df['signal'].isin(['MUA', 'MUA MẠNH'])])
                            st.metric("Tín hiệu MUA", buy_count, f"{buy_count/len(market_df)*100:.1f}%")
                        with col2:
                            avg_score = market_df['overall_score'].mean()
                            st.metric("Điểm TB thị trường", f"{avg_score:.1f}")
                        with col3:
                            top_score = market_df['overall_score'].max()
                            st.metric("Điểm cao nhất", f"{top_score:.1f}")
                        with col4:
                            high_vol_count = len(market_df[market_df['volume_ratio'] > 1.5])
                            st.metric("Khối lượng cao", high_vol_count)
                        
                    else:
                        st.error("❌ Không có dữ liệu. Vui lòng cập nhật cache.")
                        
                except Exception as e:
                    st.error(f"❌ Lỗi khi quét: {str(e)}")
    
    with tab2:
        st.markdown("### 🏆 Top Performers")
        
        if 'market_df' in st.session_state and not st.session_state['market_df'].empty:
            market_df = st.session_state['market_df']
            scan_time = st.session_state.get('scan_timestamp', 'Unknown')
            
            st.info(f"📊 Dữ liệu từ lần quét: {scan_time}")
            
            # Chọn category
            category = st.selectbox(
                "Chọn danh mục:",
                ["overall", "monthly", "quarterly", "technical", "low_risk", "high_volume"],
                format_func=lambda x: {
                    "overall": "🎯 Tổng hợp",
                    "monthly": "📈 Tăng trưởng tháng",
                    "quarterly": "📊 Tăng trưởng quý",
                    "technical": "🔧 Kỹ thuật",
                    "low_risk": "🛡️ Rủi ro thấp",
                    "high_volume": "📊 Khối lượng cao"
                }[x]
            )
            
            top_n = st.slider("Số lượng top", 5, 20, 10)
            
            # Lấy top performers
            top_df = st.session_state.cached_screener.get_top_performers(market_df, category, top_n)
            
            if not top_df.empty:
                # Hiển thị bảng
                display_cols = ['symbol', 'name', 'current_price', 'overall_score', 'signal']
                
                if category == 'monthly':
                    display_cols.insert(3, 'monthly_return')
                elif category == 'quarterly':
                    display_cols.insert(3, 'quarterly_return')
                elif category == 'technical':
                    display_cols.insert(3, 'technical_score')
                elif category == 'low_risk':
                    display_cols.insert(3, 'volatility')
                elif category == 'high_volume':
                    display_cols.insert(3, 'volume_ratio')
                
                # Format dữ liệu để hiển thị
                display_df = top_df[display_cols].copy()
                display_df['current_price'] = display_df['current_price'].apply(lambda x: f"{x*1000:,.0f}")
                
                if 'monthly_return' in display_df.columns:
                    display_df['monthly_return'] = display_df['monthly_return'].apply(lambda x: f"{x:+.1f}%")
                if 'quarterly_return' in display_df.columns:
                    display_df['quarterly_return'] = display_df['quarterly_return'].apply(lambda x: f"{x:+.1f}%")
                if 'volatility' in display_df.columns:
                    display_df['volatility'] = display_df['volatility'].apply(lambda x: f"{x:.1f}%")
                if 'volume_ratio' in display_df.columns:
                    display_df['volume_ratio'] = display_df['volume_ratio'].apply(lambda x: f"{x:.1f}x")
                
                # Đổi tên cột dựa trên số lượng cột thực tế
                if len(display_df.columns) == 5:
                    # Trường hợp cơ bản: symbol, name, price, score, signal
                    display_df.columns = ['Mã', 'Tên', 'Giá (VNĐ)', 'Điểm tổng', 'Tín hiệu']
                elif len(display_df.columns) == 6:
                    # Có thêm 1 cột đặc biệt
                    special_col = display_cols[3] if len(display_cols) > 3 else 'unknown'
                    special_name = {
                        'monthly_return': 'Tăng/Giảm tháng',
                        'quarterly_return': 'Tăng/Giảm quý', 
                        'technical_score': 'Điểm KT',
                        'volatility': 'Độ biến động',
                        'volume_ratio': 'Tỷ lệ KL'
                    }.get(special_col, 'Chỉ số')
                    
                    display_df.columns = ['Mã', 'Tên', 'Giá (VNĐ)', special_name, 'Điểm tổng', 'Tín hiệu']
                else:
                    # Fallback: giữ nguyên tên cột gốc
                    pass
                
                st.dataframe(display_df, width='stretch', hide_index=True)
                
                # Top 3 highlight
                st.markdown("### 🥇 Top 3 Nổi bật")
                cols = st.columns(3)
                for idx, (_, row) in enumerate(top_df.head(3).iterrows()):
                    with cols[idx]:
                        medal = ["🥇", "🥈", "🥉"][idx]
                        st.markdown(f"""
                        <div class="success-box">
                            <h3>{medal} {row['symbol']}</h3>
                            <p><strong>{row['name']}</strong></p>
                            <p>Giá: <strong>{row['current_price']*1000:,.0f} VNĐ</strong></p>
                            <p>Điểm: <strong>{row['overall_score']:.1f}/100</strong></p>
                            <p>Tín hiệu: <strong>{row['signal']}</strong></p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("📊 Chưa có dữ liệu. Vui lòng quét thị trường ở tab 'Market Scanner' trước.")
    
    with tab3:
        st.markdown("### 📊 Market Analysis - Phân tích chi tiết")
        
        if 'market_df' in st.session_state and not st.session_state['market_df'].empty:
            market_df = st.session_state['market_df']
            
            # Bộ lọc
            st.markdown("#### 🎯 Bộ lọc thông minh")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                min_score = st.slider("Điểm tối thiểu", 0, 100, 50)
                signals = st.multiselect("Tín hiệu", ['MUA MẠNH', 'MUA', 'GIỮ', 'BÁN', 'BÁN MẠNH'], 
                                       default=['MUA MẠNH', 'MUA'])
            
            with col2:
                rsi_range = st.slider("RSI Range", 0, 100, (20, 80))
                min_volume_ratio = st.slider("Tỷ lệ khối lượng tối thiểu", 0.5, 5.0, 1.0, 0.1)
            
            with col3:
                min_monthly_return = st.slider("Tăng trưởng tháng tối thiểu (%)", -50, 50, -10)
                trend_filter = st.multiselect("Xu hướng", ['TĂNG MẠNH', 'TĂNG', 'SIDEWAY', 'GIẢM', 'GIẢM MẠNH'])
            
            # Áp dụng bộ lọc
            criteria = {
                'min_overall_score': min_score,
                'signal_filter': signals,
                'rsi_range': rsi_range,
                'min_volume_ratio': min_volume_ratio,
                'min_monthly_return': min_monthly_return
            }
            
            if trend_filter:
                criteria['trend_filter'] = trend_filter
            
            filtered_df = st.session_state.cached_screener.filter_by_criteria(market_df, criteria)
            
            st.markdown(f"#### 📋 Kết quả lọc: {len(filtered_df)} mã")
            
            if not filtered_df.empty:
                # Hiển thị bảng chi tiết
                detail_cols = ['symbol', 'name', 'current_price', 'monthly_return', 'rsi', 
                             'overall_score', 'volume_ratio', 'signal']
                
                display_df = filtered_df[detail_cols].copy()
                display_df['current_price'] = display_df['current_price'].apply(lambda x: f"{x*1000:,.0f}")
                display_df['monthly_return'] = display_df['monthly_return'].apply(lambda x: f"{x:+.1f}%")
                display_df['rsi'] = display_df['rsi'].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "N/A")
                display_df['volume_ratio'] = display_df['volume_ratio'].apply(lambda x: f"{x:.1f}x")
                
                display_df.columns = ['Mã', 'Tên', 'Giá (VNĐ)', 'Tăng/Giảm tháng', 'RSI', 
                                    'Điểm tổng', 'Tỷ lệ KL', 'Tín hiệu']
                
                st.dataframe(display_df, width='stretch', hide_index=True)
                
                # Export Excel
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📥 Export Excel - Kết quả lọc", width='stretch'):
                        filename = f"filtered_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx"
                        success = st.session_state.cached_screener.export_to_excel(filtered_df, filename)
                        if success:
                            st.success(f"✅ Đã xuất file: {filename}")
                        else:
                            st.error("❌ Lỗi khi xuất file")
                
                with col2:
                    if st.button("📥 Export Excel - Toàn bộ", width='stretch'):
                        filename = f"market_overview_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx"
                        success = st.session_state.cached_screener.export_to_excel(market_df, filename)
                        if success:
                            st.success(f"✅ Đã xuất file: {filename}")
                        else:
                            st.error("❌ Lỗi khi xuất file")
            else:
                st.info("🔍 Không có mã nào thỏa mãn tiêu chí lọc.")
        else:
            st.info("📊 Chưa có dữ liệu. Vui lòng quét thị trường ở tab 'Market Scanner' trước.")
    
    with tab4:
        st.markdown("### ⚙️ Cache Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔄 Cập nhật Cache")
            
            update_symbols = st.number_input("Số lượng mã cập nhật", 10, 1000, 100, 10)
            
            if st.button("🔄 Cập nhật Cache Incremental", width='stretch'):
                with st.spinner(f"Đang cập nhật {update_symbols} mã..."):
                    success = st.session_state.data_cache.bulk_cache_update(max_symbols=update_symbols)
                    if success > 0:
                        st.success(f"✅ Đã cập nhật {success} mã thành công!")
                    else:
                        st.error("❌ Cập nhật thất bại")
            
            # Full Market Scan Section
            st.markdown("#### 🌍 Quét Toàn Bộ Thị Trường")
            
            # Settings
            batch_size = st.selectbox(
                "Kích thước batch:",
                options=[10, 20, 30, 50],
                index=1,  # Default 20
                help="Số lượng mã cập nhật mỗi lần"
            )
            
            delay_seconds = st.selectbox(
                "Thời gian nghỉ giữa batch (giây):",
                options=[5, 10, 15, 30],
                index=1,  # Default 10
                help="Thời gian nghỉ để tránh rate limit"
            )
            
            max_batches = st.number_input(
                "Số batch tối đa (0 = không giới hạn):",
                min_value=0,
                max_value=100,
                value=20,
                help="Giới hạn số batch để kiểm soát thời gian"
            )
            
            # Estimated stats
            estimated_symbols = max_batches * batch_size if max_batches > 0 else "Tất cả"
            estimated_time = max_batches * delay_seconds / 60 if max_batches > 0 else "Rất lâu"
            
            st.info(f"📊 Ước tính: {estimated_symbols} mã, ~{estimated_time:.1f} phút" if max_batches > 0 else f"📊 Ước tính: Tất cả mã, thời gian rất lâu")
            
            # Start Full Market Scan Button
            if st.button("🚀 Bắt đầu quét toàn bộ thị trường", 
                        type="primary", 
                        width='stretch',
                        key="start_full_scan"):
                
                # Initialize session state for scanning
                st.session_state.scanning_active = True
                st.session_state.scan_progress = 0
                st.session_state.scan_total = 0
                st.session_state.scan_success = 0
                st.session_state.scan_failed = 0
                st.session_state.current_batch = 0
                st.session_state.scan_logs = []
                st.session_state.scan_settings = {
                    'batch_size': batch_size,
                    'delay_seconds': delay_seconds,
                    'max_batches': max_batches
                }
                st.rerun()
            
            # Display scanning progress if active
            if st.session_state.get('scanning_active', False):
                st.markdown("#### 📊 Tiến độ quét thị trường")
                
                # Stop button
                if st.button("⏹️ Dừng quét", key="stop_scan", type="secondary"):
                    st.session_state.scanning_active = False
                    st.warning("Đã dừng quét thị trường!")
                    st.rerun()
                
                # Progress display
                if st.session_state.scan_total > 0:
                    progress = st.session_state.scan_progress / st.session_state.scan_total
                    st.progress(progress, 
                              text=f"Batch {st.session_state.current_batch}: {st.session_state.scan_progress}/{st.session_state.scan_total} mã")
                else:
                    st.progress(0, text="Đang khởi tạo...")
                
                # Stats during scanning
                scan_col1, scan_col2, scan_col3 = st.columns(3)
                
                with scan_col1:
                    st.metric("Thành công", st.session_state.scan_success)
                with scan_col2:
                    st.metric("Thất bại", st.session_state.scan_failed)
                with scan_col3:
                    if st.session_state.scan_progress > 0:
                        success_rate = (st.session_state.scan_success / st.session_state.scan_progress) * 100
                        st.metric("Tỷ lệ thành công", f"{success_rate:.1f}%")
                    else:
                        st.metric("Tỷ lệ thành công", "0%")
                
                # Logs
                if st.session_state.scan_logs:
                    st.markdown("**Log quét gần nhất:**")
                    for log in st.session_state.scan_logs[-3:]:  # Show last 3 logs
                        st.text(log)
                
                # Perform actual scanning work
                try:
                    # Get remaining symbols to scan
                    all_stocks = st.session_state.data_cache.get_all_symbols()
                    if all_stocks.empty:
                        st.error("Không thể lấy danh sách mã chứng khoán!")
                        st.session_state.scanning_active = False
                        st.rerun()
                    
                    # Get cached symbols
                    try:
                        cached_overview = st.session_state.data_cache.get_market_overview()
                        cached_symbols = set(cached_overview['symbol'].tolist()) if not cached_overview.empty else set()
                    except:
                        cached_symbols = set()
                    
                    # Get remaining symbols
                    all_symbols = set(all_stocks['symbol'].tolist())
                    remaining_symbols = list(all_symbols - cached_symbols)
                    
                    if not remaining_symbols:
                        st.success("🎉 Đã hoàn thành quét toàn bộ thị trường!")
                        st.session_state.scanning_active = False
                        st.rerun()
                    
                    # Initialize if first run
                    if st.session_state.scan_total == 0:
                        settings = st.session_state.scan_settings
                        max_symbols_to_scan = min(len(remaining_symbols), 
                                                settings['max_batches'] * settings['batch_size'] if settings['max_batches'] > 0 else len(remaining_symbols))
                        st.session_state.scan_total = max_symbols_to_scan
                        st.session_state.remaining_symbols = remaining_symbols[:max_symbols_to_scan]
                        
                        log_msg = f"🚀 Bắt đầu quét {max_symbols_to_scan} mã với batch size {settings['batch_size']}"
                        st.session_state.scan_logs.append(log_msg)
                    
                    # Process one batch
                    if st.session_state.scan_progress < st.session_state.scan_total:
                        settings = st.session_state.scan_settings
                        start_idx = st.session_state.scan_progress
                        end_idx = min(start_idx + settings['batch_size'], st.session_state.scan_total)
                        batch_symbols = st.session_state.remaining_symbols[start_idx:end_idx]
                        
                        st.session_state.current_batch += 1
                        
                        # Add log
                        log_msg = f"Batch {st.session_state.current_batch}: Đang xử lý {len(batch_symbols)} mã..."
                        st.session_state.scan_logs.append(log_msg)
                        
                        # Perform batch update
                        success_count = st.session_state.data_cache.bulk_cache_update(
                            symbols_list=batch_symbols,
                            max_symbols=None
                        )
                        
                        # Update progress
                        st.session_state.scan_progress = end_idx
                        st.session_state.scan_success += success_count
                        st.session_state.scan_failed += len(batch_symbols) - success_count
                        
                        # Add success log
                        success_log = f"✅ Batch {st.session_state.current_batch}: {success_count}/{len(batch_symbols)} thành công"
                        st.session_state.scan_logs.append(success_log)
                        
                        # Check if completed
                        if st.session_state.scan_progress >= st.session_state.scan_total:
                            st.session_state.scanning_active = False
                            final_log = f"🎉 Hoàn thành! {st.session_state.scan_success}/{st.session_state.scan_total} mã thành công ({(st.session_state.scan_success/st.session_state.scan_total*100):.1f}%)"
                            st.session_state.scan_logs.append(final_log)
                            st.success(final_log)
                        else:
                            # Auto refresh after delay
                            time.sleep(settings['delay_seconds'])
                        
                        st.rerun()
                    
                except Exception as e:
                    error_log = f"❌ Lỗi: {str(e)}"
                    st.session_state.scan_logs.append(error_log)
                    st.session_state.scanning_active = False
                    st.error(f"Lỗi trong quá trình quét: {e}")
                    st.rerun()
        
        with col2:
            st.markdown("#### 🧹 Bảo trì Cache")
            
            if st.button("🧹 Dọn dẹp dữ liệu cũ", width='stretch'):
                deleted = st.session_state.data_cache.cleanup_old_data()
                st.success(f"✅ Đã xóa {deleted} records cũ")
            
            if st.button("📊 Refresh Stats", width='stretch'):
                st.rerun()
        
        # Hiển thị thông tin chi tiết cache
        try:
            overview = st.session_state.data_cache.get_market_overview()
            if not overview.empty:
                st.markdown("#### 📋 Danh sách mã trong Cache")
                st.dataframe(overview.head(20), width='stretch', hide_index=True)
                
                if len(overview) > 20:
                    st.info(f"Hiển thị 20/{len(overview)} mã đầu tiên")
        except:
            st.info("Chưa có dữ liệu overview")

def show_about_page():
    """Trang giới thiệu"""
    st.markdown('<div class="main-header">ℹ️ Giới thiệu</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 📈 AI Trading - Hỗ trợ đầu tư chứng khoán thông minh
    
    ### 🎯 Tính năng chính:
    
    1. **Phân tích mã chứng khoán chi tiết**
       - Phân tích kỹ thuật với hơn 10 chỉ báo
       - Phân tích cơ bản về tài chính doanh nghiệp
       - Tín hiệu mua/bán tự động
       - Xác định điểm vào/thoát lệnh tối ưu
    
    2. **Tìm kiếm cổ phiếu tiềm năng**
       - Quét toàn bộ thị trường
       - Lọc theo tiêu chí kỹ thuật
       - Tìm cổ phiếu đang breakout
       - Tìm cổ phiếu quá bán (cơ hội mua)
    
    3. **Hỗ trợ đa khung thời gian**
       - Đầu tư ngắn hạn (1-3 tháng)
       - Đầu tư trung hạn (3-12 tháng)
       - Đầu tư dài hạn (> 1 năm)
    
    ### 📊 Chỉ số kỹ thuật:
    - RSI (Relative Strength Index)
    - MACD (Moving Average Convergence Divergence)
    - Bollinger Bands
    - Moving Averages (SMA 20, 50, 200)
    - ADX (Average Directional Index)
    - Stochastic Oscillator
    - Volume Analysis
    
    ### 💼 Phân tích cơ bản:
    - P/E Ratio (Price to Earnings)
    - P/B Ratio (Price to Book)
    - ROE (Return on Equity)
    - ROA (Return on Assets)
    - Debt to Equity
    - Profit Margin
    - EPS Growth
    
    ### ⚠️ Lưu ý:
    - Đây là công cụ hỗ trợ, không phải lời khuyên đầu tư
    - Luôn tự nghiên cứu và đánh giá rủi ro trước khi đầu tư
    - Kết hợp phân tích kỹ thuật và cơ bản để ra quyết định tốt nhất
    
    ### 🔧 Công nghệ:
    - Python 3.x
    - Streamlit (Giao diện)
    - vnstock3 (Dữ liệu thị trường)
    - TA-Lib (Phân tích kỹ thuật)
    - Plotly (Biểu đồ tương tác)
    
    ---
    
    💡 **Tip:** Sử dụng kết hợp cả phân tích kỹ thuật và phân tích cơ bản để đưa ra quyết định đầu tư tốt nhất!
    """)

# Main app
def main():
    # Chỉ hiển thị demo warning khi được kích hoạt rõ ràng
    if DEMO_AVAILABLE and os.getenv('FORCE_DEMO_MODE', 'false').lower() == 'true':
        st.info("🔧 **Chế độ Demo**: Ứng dụng đang sử dụng dữ liệu mẫu để demo. Để sử dụng dữ liệu thật, hãy tắt FORCE_DEMO_MODE.")
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/stocks.png", width=80)
        st.markdown("# 📈 AI Trading")
        st.markdown("Hỗ trợ đầu tư chứng khoán thông minh")
        st.markdown("---")
        
        page = st.radio(
            "Chọn chức năng:",
            ["📊 Phân tích mã CK", "🔎 Tìm kiếm CK tiềm năng", "📈 Tổng quan thị trường", "ℹ️ Giới thiệu"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 📌 Hướng dẫn nhanh")
        st.markdown("""
        1. **Phân tích mã CK:** Nhập mã và xem phân tích chi tiết
        2. **Tìm kiếm CK:** Quét thị trường tìm cơ hội đầu tư
        3. **Tổng quan thị trường:** Bảng so sánh toàn diện 1000+ mã
        4. **Giới thiệu:** Tìm hiểu về ứng dụng
        """)
        
        st.markdown("---")
        st.caption("© 2025 AI Trading App")
    
    # Main content
    if page == "📊 Phân tích mã CK":
        show_analysis_page()
    elif page == "🔎 Tìm kiếm CK tiềm năng":
        show_screener_page()
    elif page == "📈 Tổng quan thị trường":
        show_market_overview_page()
    else:
        show_about_page()

if __name__ == "__main__":
    main()

