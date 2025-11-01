"""
Demo script cho phân tích thị trường với cached data
"""

from cached_stock_screener import CachedStockScreener
import pandas as pd

def main():
    print("🚀 AI Trading - Market Analysis Demo")
    print("=" * 50)
    
    # Khởi tạo screener
    screener = CachedStockScreener()
    
    # Hiển thị stats cache hiện tại
    stats = screener.cache.get_cache_stats()
    print(f"📊 Cache Stats:")
    print(f"   - Symbols: {stats['total_symbols']}")
    print(f"   - Records: {stats['total_records']:,}")
    print(f"   - Date Range: {stats['date_range']}")
    print(f"   - Size: {stats['db_size_mb']} MB")
    print()
    
    # Tạo bảng so sánh thị trường
    print("🔍 Generating market comparison table...")
    market_df = screener.get_market_comparison_table(
        update_cache=False,  # Set True để cập nhật cache
        max_symbols=30  # Giới hạn để demo nhanh
    )
    
    if market_df.empty:
        print("❌ No data available. Try updating cache first:")
        print("   python cache_manager.py --action update --max 50")
        return
    
    print(f"✅ Generated analysis for {len(market_df)} stocks")
    print()
    
    # Hiển thị tổng quan
    print("📈 MARKET OVERVIEW (Top 10)")
    print("-" * 80)
    overview_cols = ['symbol', 'name', 'current_price', 'monthly_return', 
                    'rsi', 'overall_score', 'signal']
    print(market_df[overview_cols].head(10).to_string(index=False))
    print()
    
    # Top performers theo danh mục
    categories = {
        'overall': 'Overall Score',
        'monthly': 'Monthly Return',
        'technical': 'Technical Score',
        'low_risk': 'Low Risk (Low Volatility)'
    }
    
    for category, title in categories.items():
        print(f"🏆 TOP 5 - {title.upper()}")
        print("-" * 50)
        top_df = screener.get_top_performers(market_df, category, 5)
        
        if category == 'low_risk':
            display_cols = ['symbol', 'name', 'volatility', 'overall_score', 'signal']
        elif category == 'monthly':
            display_cols = ['symbol', 'name', 'monthly_return', 'quarterly_return', 'signal']
        else:
            display_cols = ['symbol', 'name', 'overall_score', 'technical_score', 'signal']
        
        print(top_df[display_cols].to_string(index=False))
        print()
    
    # Lọc theo tiêu chí cụ thể
    print("🎯 FILTERED RESULTS")
    print("-" * 50)
    
    # Cổ phiếu có tín hiệu mua
    buy_signals = screener.filter_by_criteria(market_df, {
        'signal_filter': ['MUA', 'MUA MẠNH'],
        'min_overall_score': 55
    })
    
    if not buy_signals.empty:
        print(f"📈 BUY SIGNALS ({len(buy_signals)} stocks):")
        buy_cols = ['symbol', 'name', 'current_price', 'overall_score', 
                   'entry_points_count', 'risk_reward_ratio', 'signal']
        print(buy_signals[buy_cols].head(10).to_string(index=False))
        print()
    
    # Cổ phiếu quá bán (RSI < 30)
    oversold = screener.filter_by_criteria(market_df, {
        'rsi_range': (0, 30),
        'min_overall_score': 50
    })
    
    if not oversold.empty:
        print(f"📉 OVERSOLD OPPORTUNITIES ({len(oversold)} stocks):")
        oversold_cols = ['symbol', 'name', 'current_price', 'rsi', 
                        'monthly_return', 'overall_score']
        print(oversold[oversold_cols].to_string(index=False))
        print()
    
    # Cổ phiếu có volume cao
    high_volume = screener.filter_by_criteria(market_df, {
        'min_volume_ratio': 1.5,
        'min_overall_score': 55
    })
    
    if not high_volume.empty:
        print(f"📊 HIGH VOLUME ACTIVITY ({len(high_volume)} stocks):")
        volume_cols = ['symbol', 'name', 'volume_ratio', 'monthly_return', 'signal']
        print(high_volume[volume_cols].head(5).to_string(index=False))
        print()
    
    # Xuất ra Excel
    print("💾 Exporting to Excel...")
    success = screener.export_to_excel(market_df, 'market_analysis_demo.xlsx')
    if success:
        print("✅ Exported to market_analysis_demo.xlsx")
    
    print()
    print("🎉 Demo completed!")
    print("💡 Tips:")
    print("   - Update cache regularly: python cache_manager.py --action update")
    print("   - View cache stats: python cache_manager.py --action stats")
    print("   - Clean old data: python cache_manager.py --action cleanup")

if __name__ == "__main__":
    main()
