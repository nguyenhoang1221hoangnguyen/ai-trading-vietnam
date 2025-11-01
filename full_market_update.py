#!/usr/bin/env python3
"""
Script cập nhật toàn bộ thị trường vào cache
Sử dụng cho việc cập nhật lần đầu hoặc full refresh
"""

import time
import sys
from datetime import datetime
from data_cache import DataCache

def full_market_update(batch_size=50, delay_between_batches=30):
    """
    Cập nhật toàn bộ thị trường với batch processing
    
    Args:
        batch_size: Số lượng mã trong mỗi batch
        delay_between_batches: Thời gian nghỉ giữa các batch (giây)
    """
    print("🚀 Bắt đầu cập nhật toàn bộ thị trường...")
    print("=" * 60)
    
    cache = DataCache()
    
    # Lấy danh sách tất cả mã
    print("📋 Lấy danh sách tất cả mã chứng khoán...")
    all_stocks = cache.get_all_symbols()
    
    if all_stocks.empty:
        print("❌ Không thể lấy danh sách mã chứng khoán!")
        return False
    
    total_symbols = len(all_stocks)
    print(f"📊 Tổng số mã cần cập nhật: {total_symbols:,}")
    
    # Chia thành các batch
    symbols_list = all_stocks['symbol'].tolist()
    batches = [symbols_list[i:i + batch_size] for i in range(0, len(symbols_list), batch_size)]
    total_batches = len(batches)
    
    print(f"📦 Chia thành {total_batches} batch, mỗi batch {batch_size} mã")
    print(f"⏱️ Thời gian ước tính: {total_batches * (batch_size * 2 + delay_between_batches) / 60:.1f} phút")
    
    # Xác nhận từ người dùng
    response = input(f"\n🤔 Bạn có chắc muốn cập nhật {total_symbols:,} mã? (y/N): ")
    if response.lower() != 'y':
        print("❌ Hủy bỏ cập nhật.")
        return False
    
    print(f"\n🎯 Bắt đầu cập nhật lúc {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    total_success = 0
    total_failed = 0
    start_time = time.time()
    
    for batch_idx, batch_symbols in enumerate(batches, 1):
        print(f"\n📦 Batch {batch_idx}/{total_batches} - {len(batch_symbols)} mã")
        print(f"   Mã đầu tiên: {batch_symbols[0]}, Mã cuối: {batch_symbols[-1]}")
        
        batch_start_time = time.time()
        
        # Cập nhật batch
        success_count = cache.bulk_cache_update(
            symbols_list=batch_symbols,
            max_symbols=None
        )
        
        batch_time = time.time() - batch_start_time
        total_success += success_count
        total_failed += len(batch_symbols) - success_count
        
        # Thống kê batch
        print(f"   ✅ Thành công: {success_count}/{len(batch_symbols)}")
        print(f"   ⏱️ Thời gian: {batch_time:.1f}s")
        print(f"   📊 Tổng cộng: {total_success}/{total_success + total_failed} ({total_success/(total_success + total_failed)*100:.1f}%)")
        
        # Nghỉ giữa các batch (trừ batch cuối)
        if batch_idx < total_batches:
            print(f"   😴 Nghỉ {delay_between_batches}s để tránh rate limit...")
            time.sleep(delay_between_batches)
    
    # Thống kê cuối
    total_time = time.time() - start_time
    print("\n" + "=" * 60)
    print("🎉 HOÀN THÀNH CẬP NHẬT TOÀN BỘ THỊ TRƯỜNG!")
    print(f"✅ Thành công: {total_success:,} mã")
    print(f"❌ Thất bại: {total_failed:,} mã")
    print(f"📊 Tỷ lệ thành công: {total_success/(total_success + total_failed)*100:.1f}%")
    print(f"⏱️ Tổng thời gian: {total_time/60:.1f} phút")
    print(f"⚡ Tốc độ trung bình: {(total_success + total_failed)/(total_time/60):.1f} mã/phút")
    
    # Kiểm tra cache cuối cùng
    print("\n📊 Kiểm tra cache sau cập nhật...")
    try:
        stats = cache.get_cache_stats()
        print(f"   Tổng số mã trong cache: {stats['total_symbols']:,}")
        print(f"   Tổng số records: {stats['total_records']:,}")
        print(f"   Kích thước DB: {stats['db_size_mb']} MB")
    except Exception as e:
        print(f"   ⚠️ Không thể lấy stats: {e}")
    
    return total_success > 0

def quick_update(max_symbols=100):
    """Cập nhật nhanh một số lượng mã nhất định"""
    print(f"⚡ Cập nhật nhanh {max_symbols} mã...")
    
    cache = DataCache()
    success = cache.bulk_cache_update(max_symbols=max_symbols)
    
    if success > 0:
        print(f"✅ Đã cập nhật {success} mã thành công!")
        return True
    else:
        print("❌ Cập nhật thất bại!")
        return False

def main():
    """Main function"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "quick":
            max_symbols = int(sys.argv[2]) if len(sys.argv) > 2 else 100
            quick_update(max_symbols)
        elif sys.argv[1] == "full":
            batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            delay = int(sys.argv[3]) if len(sys.argv) > 3 else 30
            full_market_update(batch_size, delay)
        else:
            print("Usage: python full_market_update.py [quick|full] [params...]")
    else:
        # Interactive mode
        print("🎯 CHỌN CHẾ ĐỘ CẬP NHẬT:")
        print("1. ⚡ Cập nhật nhanh (100 mã)")
        print("2. 🚀 Cập nhật toàn bộ thị trường (1,725 mã)")
        print("3. ❌ Thoát")
        
        choice = input("\nNhập lựa chọn (1-3): ")
        
        if choice == "1":
            max_symbols = input("Số lượng mã (mặc định 100): ")
            max_symbols = int(max_symbols) if max_symbols.isdigit() else 100
            quick_update(max_symbols)
        elif choice == "2":
            batch_size = input("Kích thước batch (mặc định 50): ")
            batch_size = int(batch_size) if batch_size.isdigit() else 50
            
            delay = input("Thời gian nghỉ giữa batch (giây, mặc định 30): ")
            delay = int(delay) if delay.isdigit() else 30
            
            full_market_update(batch_size, delay)
        else:
            print("👋 Thoát chương trình.")

if __name__ == "__main__":
    main()
