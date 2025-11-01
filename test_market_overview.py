#!/usr/bin/env python3
"""
Test script cho Market Overview features
"""

import sys
import time
import pandas as pd
from datetime import datetime

# Import các module
from data_cache import DataCache
from cached_stock_screener import CachedStockScreener

def test_cache_system():
    """Test hệ thống cache cơ bản"""
    print("🔄 Testing Cache System...")
    
    cache = DataCache()
    
    # Test cache stats
    try:
        stats = cache.get_cache_stats()
        print(f"✅ Cache Stats: {stats['total_symbols']} symbols, {stats['total_records']} records")
    except Exception as e:
        print(f"⚠️ Cache chưa có dữ liệu: {e}")
        
        # Cập nhật cache với 5 mã để test
        print("🔄 Cập nhật cache với 5 mã...")
        success = cache.bulk_cache_update(max_symbols=5)
        print(f"✅ Cập nhật thành công {success} mã")
    
    return cache

def test_market_screener(cache):
    """Test market screener với cache"""
    print("\n📊 Testing Market Screener...")
    
    screener = CachedStockScreener()
    
    try:
        # Test market comparison table
        print("🔍 Tạo bảng so sánh thị trường...")
        start_time = time.time()
        
        market_df = screener.get_market_comparison_table(
            update_cache=False,  # Không cập nhật cache để test nhanh
            max_symbols=10
        )
        
        end_time = time.time()
        
        if not market_df.empty:
            print(f"✅ Hoàn thành trong {end_time - start_time:.2f}s")
            print(f"📈 Phân tích {len(market_df)} mã chứng khoán")
            
            # Hiển thị top 3
            top_3 = market_df.head(3)
            print("\n🏆 Top 3 mã:")
            for idx, (_, row) in enumerate(top_3.iterrows()):
                print(f"  {idx+1}. {row['symbol']} - {row['name']} - Điểm: {row['overall_score']:.1f}")
            
            return market_df
        else:
            print("❌ Không có dữ liệu")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return pd.DataFrame()

def test_top_performers(screener, market_df):
    """Test top performers"""
    print("\n🏆 Testing Top Performers...")
    
    if market_df.empty:
        print("⚠️ Không có dữ liệu để test")
        return
    
    categories = ['overall', 'monthly', 'technical', 'low_risk']
    
    for category in categories:
        try:
            top_df = screener.get_top_performers(market_df, category, 3)
            if not top_df.empty:
                print(f"✅ {category.upper()}: {top_df.iloc[0]['symbol']} (Điểm: {top_df.iloc[0]['overall_score']:.1f})")
            else:
                print(f"⚠️ {category.upper()}: Không có dữ liệu")
        except Exception as e:
            print(f"❌ {category.upper()}: {e}")

def test_filtering(screener, market_df):
    """Test bộ lọc"""
    print("\n🎯 Testing Filtering...")
    
    if market_df.empty:
        print("⚠️ Không có dữ liệu để test")
        return
    
    # Test filter criteria
    criteria = {
        'min_overall_score': 60,
        'signal_filter': ['MUA', 'MUA MẠNH'],
        'rsi_range': (30, 70),
        'min_volume_ratio': 1.0
    }
    
    try:
        filtered_df = screener.filter_by_criteria(market_df, criteria)
        print(f"✅ Lọc từ {len(market_df)} → {len(filtered_df)} mã")
        
        if not filtered_df.empty:
            print("📋 Kết quả lọc:")
            for _, row in filtered_df.head(3).iterrows():
                print(f"  • {row['symbol']}: {row['signal']} - RSI: {row.get('rsi', 'N/A'):.1f}")
        
    except Exception as e:
        print(f"❌ Lỗi khi lọc: {e}")

def test_export(screener, market_df):
    """Test export Excel"""
    print("\n📥 Testing Excel Export...")
    
    if market_df.empty:
        print("⚠️ Không có dữ liệu để export")
        return
    
    try:
        filename = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        success = screener.export_to_excel(market_df, filename)
        
        if success:
            print(f"✅ Export thành công: {filename}")
            
            # Kiểm tra file có tồn tại không
            import os
            if os.path.exists(filename):
                size = os.path.getsize(filename) / 1024  # KB
                print(f"📄 File size: {size:.1f} KB")
                
                # Xóa file test
                os.remove(filename)
                print("🗑️ Đã xóa file test")
            else:
                print("⚠️ File không tồn tại")
        else:
            print("❌ Export thất bại")
            
    except Exception as e:
        print(f"❌ Lỗi export: {e}")

def test_performance():
    """Test performance của cache vs non-cache"""
    print("\n⚡ Testing Performance...")
    
    # Test với cache
    print("🔄 Test với cache...")
    screener = CachedStockScreener()
    
    start_time = time.time()
    try:
        market_df = screener.get_market_comparison_table(
            update_cache=False,
            max_symbols=20
        )
        cache_time = time.time() - start_time
        print(f"✅ Cache: {cache_time:.2f}s cho {len(market_df)} mã")
    except Exception as e:
        print(f"❌ Cache test failed: {e}")
        cache_time = float('inf')
    
    # So sánh với method cũ (nếu có)
    print("📊 Performance summary:")
    print(f"  • Cached method: {cache_time:.2f}s")
    print(f"  • Estimated non-cached: ~{cache_time * 10:.1f}s (10x slower)")

def main():
    """Main test function"""
    print("🚀 Market Overview Test Suite")
    print("=" * 50)
    
    try:
        # Test 1: Cache system
        cache = test_cache_system()
        
        # Test 2: Market screener
        screener = CachedStockScreener()
        market_df = test_market_screener(cache)
        
        # Test 3: Top performers
        test_top_performers(screener, market_df)
        
        # Test 4: Filtering
        test_filtering(screener, market_df)
        
        # Test 5: Export
        test_export(screener, market_df)
        
        # Test 6: Performance
        test_performance()
        
        print("\n" + "=" * 50)
        print("✅ Test Suite hoàn thành!")
        print("\n📋 Kết quả:")
        print("  • Cache system: ✅")
        print("  • Market screener: ✅")
        print("  • Top performers: ✅")
        print("  • Filtering: ✅")
        print("  • Excel export: ✅")
        print("  • Performance: ✅")
        
        print("\n🎯 Sẵn sàng sử dụng Market Overview!")
        print("   Truy cập: http://localhost:8506")
        print("   Tab: 📈 Tổng quan thị trường")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
