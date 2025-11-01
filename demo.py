"""
Demo script - Test các chức năng chính của ứng dụng
Chạy: python demo.py
"""

import sys
from data_fetcher import DataFetcher
from technical_analysis import TechnicalAnalyzer
from fundamental_analysis import FundamentalAnalyzer
from trading_signals import TradingSignalGenerator

def print_header(text):
    """In header đẹp"""
    print("\n" + "="*80)
    print(f" {text}")
    print("="*80 + "\n")

def demo_stock_analysis(symbol="VNM"):
    """Demo phân tích mã chứng khoán"""
    print_header(f"🔍 DEMO: Phân tích mã chứng khoán {symbol}")
    
    # Khởi tạo data fetcher
    data_fetcher = DataFetcher()
    
    print(f"📊 Đang lấy dữ liệu cho {symbol}...")
    
    # Lấy dữ liệu giá
    stock_data = data_fetcher.get_stock_data(symbol, period='6M')
    
    if stock_data is None or len(stock_data) < 20:
        print(f"❌ Không thể lấy dữ liệu cho {symbol}")
        return
    
    print(f"✅ Đã lấy {len(stock_data)} ngày dữ liệu")
    
    # Lấy dữ liệu tài chính
    print(f"📈 Đang lấy dữ liệu tài chính...")
    ratios_data = data_fetcher.get_financial_ratios(symbol)
    financial_data = data_fetcher.get_financial_report(symbol)
    
    # Phân tích kỹ thuật
    print(f"\n🔧 Phân tích kỹ thuật...")
    analyzer = TechnicalAnalyzer(stock_data)
    df_analyzed = analyzer.add_all_indicators()
    
    latest = df_analyzed.iloc[-1]
    
    print(f"  • Giá hiện tại: {latest['close']*1000:,.0f} VNĐ")
    if 'rsi' in latest.index:
        print(f"  • RSI: {latest['rsi']:.2f}")
    if 'macd' in latest.index:
        print(f"  • MACD: {latest['macd']:.2f}")
    if 'sma_20' in latest.index:
        print(f"  • SMA 20: {latest['sma_20']*1000:,.0f} VNĐ")
    if 'sma_50' in latest.index:
        print(f"  • SMA 50: {latest['sma_50']*1000:,.0f} VNĐ")
    
    # Tín hiệu kỹ thuật
    technical_signals = analyzer.generate_signals()
    technical_score = analyzer.calculate_score()
    trend = analyzer.get_trend()
    
    print(f"\n  📊 Điểm kỹ thuật: {technical_score:.1f}/100")
    print(f"  📈 Xu hướng: {trend}")
    
    if technical_signals:
        print(f"\n  🎯 Tín hiệu kỹ thuật ({len(technical_signals)}):")
        for signal in technical_signals[:3]:  # Chỉ hiển thị 3 tín hiệu đầu
            emoji = "🟢" if signal['type'] == 'BUY' else "🔴"
            print(f"    {emoji} {signal['type']}: {signal['reason']}")
    
    # Phân tích cơ bản
    if ratios_data is not None and not ratios_data.empty:
        print(f"\n💼 Phân tích cơ bản...")
        fund_analyzer = FundamentalAnalyzer(financial_data, ratios_data)
        fund_score = fund_analyzer.calculate_score()
        
        print(f"  📊 Điểm cơ bản: {fund_score:.1f}/100")
        
        # Định giá
        valuation = fund_analyzer.get_valuation_analysis()
        print(f"  💰 Định giá: {valuation['valuation']}")
        
        # Sức khỏe tài chính
        health = fund_analyzer.get_financial_health()
        print(f"  🏥 Sức khỏe tài chính: {health['status']}")
    
    # Tín hiệu tổng hợp
    print(f"\n🎯 Tín hiệu tổng hợp...")
    signal_gen = TradingSignalGenerator(stock_data, financial_data, ratios_data)
    overall = signal_gen.get_overall_signal()
    
    print(f"  {overall['color']} Tín hiệu: {overall['signal']}")
    print(f"  📊 Điểm tổng: {overall['overall_score']:.1f}/100")
    
    # Điểm vào/thoát
    entry_points = signal_gen.get_entry_points()
    exit_points = signal_gen.get_exit_points()
    
    if entry_points:
        print(f"\n  📍 Điểm vào lệnh:")
        for point in entry_points[:2]:
            print(f"    • {point['type']} tại {point['price']*1000:,.0f} VNĐ - {point['reason']}")
    
    if exit_points:
        print(f"\n  🎯 Điểm thoát lệnh:")
        for point in exit_points[:2]:
            print(f"    • {point['type']} tại {point['price']*1000:,.0f} VNĐ - {point['reason']}")
    
    # Risk/Reward
    rr = signal_gen.get_risk_reward_ratio()
    if rr:
        print(f"\n  ⚖️ Tỷ lệ Risk/Reward: 1:{rr['ratio']:.2f}")
    
    # Khung thời gian đầu tư
    timeframes = signal_gen.get_investment_timeframe()
    print(f"\n  ⏰ Phù hợp với: {', '.join(timeframes)}")

def demo_stock_screener():
    """Demo tìm kiếm cổ phiếu tiềm năng"""
    print_header("🔎 DEMO: Tìm kiếm cổ phiếu tiềm năng")
    
    from stock_screener import StockScreener
    
    screener = StockScreener()
    
    print("🚀 Đang quét thị trường tìm cổ phiếu ngắn hạn...")
    print("(Quét 10 mã đầu tiên để demo nhanh)\n")
    
    # Tạm thời test với một số mã
    test_symbols = ['VNM', 'FPT', 'VIC', 'HPG', 'VHM']
    
    results = []
    for symbol in test_symbols:
        try:
            print(f"  Đang quét: {symbol}...", end=" ")
            
            data_fetcher = DataFetcher()
            stock_data = data_fetcher.get_stock_data(symbol, period='3M')
            
            if stock_data is None or len(stock_data) < 50:
                print("❌ Không đủ dữ liệu")
                continue
            
            signal_gen = TradingSignalGenerator(stock_data, None, None)
            overall = signal_gen.get_overall_signal()
            
            if overall['overall_score'] >= 55:
                print(f"✅ Điểm: {overall['overall_score']:.1f}")
                results.append({
                    'symbol': symbol,
                    'score': overall['overall_score'],
                    'signal': overall['signal']
                })
            else:
                print(f"➖ Điểm: {overall['overall_score']:.1f}")
        
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
    
    if results:
        print(f"\n📊 Kết quả: Tìm thấy {len(results)} cổ phiếu tiềm năng\n")
        print("  " + "-"*60)
        print(f"  {'Mã':<10} {'Điểm':<15} {'Tín hiệu':<20}")
        print("  " + "-"*60)
        
        for r in sorted(results, key=lambda x: x['score'], reverse=True):
            print(f"  {r['symbol']:<10} {r['score']:<15.1f} {r['signal']:<20}")
        
        print("  " + "-"*60)
    else:
        print("\n⚠️ Không tìm thấy cổ phiếu phù hợp")

def main():
    """Hàm main"""
    print("""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║                   📈 AI TRADING - DEMO SCRIPT 📈                             ║
    ║                                                                              ║
    ║              Ứng dụng hỗ trợ đầu tư chứng khoán Việt Nam                    ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print("\n🎯 Script này sẽ demo các chức năng chính của ứng dụng")
    print("⏱️  Thời gian ước tính: 1-2 phút\n")
    
    input("Nhấn Enter để bắt đầu...")
    
    # Demo 1: Phân tích mã chứng khoán
    try:
        demo_stock_analysis("VNM")
    except Exception as e:
        print(f"❌ Lỗi khi phân tích: {str(e)}")
    
    input("\nNhấn Enter để tiếp tục demo tìm kiếm cổ phiếu...")
    
    # Demo 2: Tìm kiếm cổ phiếu
    try:
        demo_stock_screener()
    except Exception as e:
        print(f"❌ Lỗi khi quét thị trường: {str(e)}")
    
    print_header("✅ HOÀN THÀNH DEMO")
    
    print("""
    🎉 Demo hoàn tất!
    
    📌 Để sử dụng đầy đủ chức năng, hãy chạy:
       streamlit run app.py
    
    📖 Đọc thêm:
       • README.md - Hướng dẫn chi tiết
       • QUICKSTART.md - Bắt đầu nhanh
       • INSTALL.md - Hướng dẫn cài đặt
    
    💡 Tips:
       • Kết hợp phân tích kỹ thuật và cơ bản
       • Luôn đặt lệnh cắt lỗ
       • Không all-in vào một mã
    
    ⚠️  Lưu ý: Đây chỉ là công cụ hỗ trợ, không phải lời khuyên đầu tư!
    
    Chúc bạn đầu tư thành công! 🚀📈
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Đã dừng demo. Hẹn gặp lại!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Lỗi không mong muốn: {str(e)}")
        sys.exit(1)

