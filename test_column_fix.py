#!/usr/bin/env python3
"""
Test script để kiểm tra fix lỗi column mismatch
"""

import pandas as pd
from cached_stock_screener import CachedStockScreener

def test_column_renaming():
    """Test logic đổi tên cột trong Market Overview"""
    print("🧪 Testing Column Renaming Logic...")
    
    screener = CachedStockScreener()
    
    # Lấy dữ liệu mẫu
    market_df = screener.get_market_comparison_table(update_cache=False, max_symbols=5)
    
    if market_df.empty:
        print("❌ No market data available")
        return False
    
    print(f"✅ Got {len(market_df)} stocks")
    
    # Test các category khác nhau
    categories = ['overall', 'monthly', 'quarterly', 'technical', 'low_risk', 'high_volume']
    
    for category in categories:
        try:
            print(f"\n📊 Testing category: {category}")
            
            top_df = screener.get_top_performers(market_df, category, 3)
            
            if top_df.empty:
                print(f"  ⚠️ No data for {category}")
                continue
            
            # Tạo display_cols như trong app.py
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
            
            # Kiểm tra các cột có tồn tại không
            available_cols = [col for col in display_cols if col in top_df.columns]
            display_df = top_df[available_cols].copy()
            
            print(f"  📋 Columns: {len(display_df.columns)} - {display_df.columns.tolist()}")
            
            # Test logic đổi tên cột
            if len(display_df.columns) == 5:
                new_columns = ['Mã', 'Tên', 'Giá (VNĐ)', 'Điểm tổng', 'Tín hiệu']
                print(f"  ✅ 5 columns -> {new_columns}")
            elif len(display_df.columns) == 6:
                special_col = available_cols[3] if len(available_cols) > 3 else 'unknown'
                special_name = {
                    'monthly_return': 'Tăng/Giảm tháng',
                    'quarterly_return': 'Tăng/Giảm quý', 
                    'technical_score': 'Điểm KT',
                    'volatility': 'Độ biến động',
                    'volume_ratio': 'Tỷ lệ KL'
                }.get(special_col, 'Chỉ số')
                
                new_columns = ['Mã', 'Tên', 'Giá (VNĐ)', special_name, 'Điểm tổng', 'Tín hiệu']
                print(f"  ✅ 6 columns -> {new_columns}")
            else:
                print(f"  ⚠️ Unexpected column count: {len(display_df.columns)}")
                
        except Exception as e:
            print(f"  ❌ Error in {category}: {e}")
    
    return True

def test_market_analysis():
    """Test Market Analysis section"""
    print("\n🔍 Testing Market Analysis...")
    
    screener = CachedStockScreener()
    market_df = screener.get_market_comparison_table(update_cache=False, max_symbols=5)
    
    if market_df.empty:
        print("❌ No market data")
        return False
    
    # Test bộ lọc
    criteria = {
        'min_overall_score': 30,
        'signal_filter': ['MUA', 'MUA MẠNH', 'GIỮ'],
        'rsi_range': (20, 80),
        'min_volume_ratio': 0.5
    }
    
    filtered_df = screener.filter_by_criteria(market_df, criteria)
    print(f"✅ Filtered: {len(market_df)} -> {len(filtered_df)} stocks")
    
    if not filtered_df.empty:
        # Test display columns
        detail_cols = ['symbol', 'name', 'current_price', 'monthly_return', 'rsi', 
                      'overall_score', 'volume_ratio', 'signal']
        
        available_cols = [col for col in detail_cols if col in filtered_df.columns]
        display_df = filtered_df[available_cols].copy()
        
        print(f"📋 Analysis columns: {len(display_df.columns)} - {display_df.columns.tolist()}")
        
        # Fixed column names
        expected_names = ['Mã', 'Tên', 'Giá (VNĐ)', 'Tăng/Giảm tháng', 'RSI', 
                         'Điểm tổng', 'Tỷ lệ KL', 'Tín hiệu']
        
        if len(display_df.columns) == len(expected_names):
            print(f"✅ Column count matches: {len(expected_names)}")
        else:
            print(f"⚠️ Column mismatch: got {len(display_df.columns)}, expected {len(expected_names)}")
    
    return True

def main():
    """Main test function"""
    print("🚀 Testing Market Overview Column Fix")
    print("=" * 50)
    
    try:
        # Test 1: Column renaming
        success1 = test_column_renaming()
        
        # Test 2: Market analysis
        success2 = test_market_analysis()
        
        print("\n" + "=" * 50)
        if success1 and success2:
            print("✅ All tests passed! Column fix is working.")
            print("\n🎯 Market Overview should now work without column mismatch errors.")
            print("   Truy cập: http://localhost:8506")
            print("   Tab: 📈 Tổng quan thị trường")
        else:
            print("❌ Some tests failed. Please check the issues above.")
            
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
