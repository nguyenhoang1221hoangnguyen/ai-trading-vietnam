#!/usr/bin/env python3
"""
Script cập nhật dần dần toàn bộ thị trường
Tránh rate limit bằng cách sử dụng batch nhỏ và delay lớn
"""

import time
import sys
from datetime import datetime
from data_cache import DataCache

def gradual_market_update(batch_size=20, delay_minutes=2, max_batches=None):
    """
    Cập nhật dần dần thị trường với batch nhỏ và delay lớn
    
    Args:
        batch_size: Số lượng mã trong mỗi batch (khuyến nghị 10-30)
        delay_minutes: Thời gian nghỉ giữa các batch (phút)
        max_batches: Giới hạn số batch (None = không giới hạn)
    """
    print("🐌 Bắt đầu cập nhật dần dần thị trường...")
    print("=" * 60)
    
    cache = DataCache()
    
    # Lấy danh sách tất cả mã
    print("📋 Lấy danh sách tất cả mã chứng khoán...")
    all_stocks = cache.get_all_symbols()
    
    if all_stocks.empty:
        print("❌ Không thể lấy danh sách mã chứng khoán!")
        return False
    
    # Lấy danh sách mã đã có trong cache
    try:
        cached_overview = cache.get_market_overview()
        cached_symbols = set(cached_overview['symbol'].tolist()) if not cached_overview.empty else set()
        print(f"📊 Đã có {len(cached_symbols)} mã trong cache")
    except:
        cached_symbols = set()
        print("📊 Cache trống, bắt đầu từ đầu")
    
    # Lọc ra các mã chưa có trong cache
    all_symbols = set(all_stocks['symbol'].tolist())
    remaining_symbols = list(all_symbols - cached_symbols)
    
    print(f"🎯 Cần cập nhật thêm: {len(remaining_symbols)} mã")
    print(f"📦 Batch size: {batch_size} mã")
    print(f"⏱️ Delay giữa batch: {delay_minutes} phút")
    
    if not remaining_symbols:
        print("✅ Tất cả mã đã được cache!")
        return True
    
    # Chia thành các batch
    batches = [remaining_symbols[i:i + batch_size] for i in range(0, len(remaining_symbols), batch_size)]
    total_batches = len(batches)
    
    if max_batches:
        batches = batches[:max_batches]
        total_batches = len(batches)
        print(f"🔢 Giới hạn {max_batches} batch đầu tiên")
    
    print(f"📦 Tổng cộng: {total_batches} batch")
    print(f"⏱️ Thời gian ước tính: {total_batches * delay_minutes:.1f} phút")
    
    print(f"\n🎯 Bắt đầu cập nhật lúc {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    total_success = 0
    total_failed = 0
    start_time = time.time()
    
    for batch_idx, batch_symbols in enumerate(batches, 1):
        print(f"\n📦 Batch {batch_idx}/{total_batches} - {len(batch_symbols)} mã")
        print(f"   Thời gian: {datetime.now().strftime('%H:%M:%S')}")
        print(f"   Mã đầu tiên: {batch_symbols[0]}")
        print(f"   Mã cuối: {batch_symbols[-1]}")
        
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
        print(f"   ⏱️ Thời gian batch: {batch_time:.1f}s")
        print(f"   📊 Tổng tiến độ: {total_success}/{total_success + total_failed}")
        
        # Kiểm tra cache hiện tại
        try:
            current_stats = cache.get_cache_stats()
            print(f"   💾 Cache hiện tại: {current_stats['total_symbols']} mã, {current_stats['total_records']} records")
        except:
            print(f"   💾 Cache hiện tại: {total_success + len(cached_symbols)} mã (ước tính)")
        
        # Nghỉ giữa các batch (trừ batch cuối)
        if batch_idx < total_batches:
            delay_seconds = delay_minutes * 60
            print(f"   😴 Nghỉ {delay_minutes} phút để tránh rate limit...")
            print(f"   ⏰ Batch tiếp theo lúc: {datetime.fromtimestamp(time.time() + delay_seconds).strftime('%H:%M:%S')}")
            
            # Countdown
            for remaining in range(delay_seconds, 0, -30):
                if remaining > 30:
                    print(f"      Còn {remaining//60}:{remaining%60:02d} phút...")
                    time.sleep(30)
                else:
                    print(f"      Còn {remaining} giây...")
                    time.sleep(remaining)
                    break
    
    # Thống kê cuối
    total_time = time.time() - start_time
    print("\n" + "=" * 60)
    print("🎉 HOÀN THÀNH BATCH CẬP NHẬT!")
    print(f"✅ Thành công: {total_success} mã")
    print(f"❌ Thất bại: {total_failed} mã")
    print(f"📊 Tỷ lệ thành công: {total_success/(total_success + total_failed)*100:.1f}%")
    print(f"⏱️ Tổng thời gian: {total_time/60:.1f} phút")
    
    # Kiểm tra cache cuối cùng
    print("\n📊 Kiểm tra cache sau cập nhật...")
    try:
        stats = cache.get_cache_stats()
        print(f"   Tổng số mã trong cache: {stats['total_symbols']}")
        print(f"   Tổng số records: {stats['total_records']:,}")
        print(f"   Kích thước DB: {stats['db_size_mb']} MB")
        print(f"   Tiến độ: {stats['total_symbols']}/1725 ({stats['total_symbols']/1725*100:.1f}%)")
    except Exception as e:
        print(f"   ⚠️ Không thể lấy stats: {e}")
    
    return total_success > 0

def continue_update():
    """Tiếp tục cập nhật với cài đặt an toàn"""
    print("🔄 TIẾP TỤC CẬP NHẬT TOÀN BỘ THỊ TRƯỜNG")
    print("Cài đặt an toàn để tránh rate limit:")
    print("- Batch size: 20 mã")
    print("- Delay: 2 phút giữa các batch")
    print("- Chỉ chạy 5 batch mỗi lần (100 mã)")
    print()
    
    return gradual_market_update(
        batch_size=20,
        delay_minutes=2,
        max_batches=5
    )

def aggressive_update():
    """Cập nhật tích cực hơn (có thể bị rate limit)"""
    print("⚡ CẬP NHẬT TÍCH CỰC")
    print("Cài đặt nhanh hơn (có thể bị rate limit):")
    print("- Batch size: 50 mã")
    print("- Delay: 1 phút giữa các batch")
    print("- Chạy 10 batch (500 mã)")
    print()
    
    return gradual_market_update(
        batch_size=50,
        delay_minutes=1,
        max_batches=10
    )

def main():
    """Main function"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "continue":
            continue_update()
        elif sys.argv[1] == "aggressive":
            aggressive_update()
        else:
            print("Usage: python gradual_update.py [continue|aggressive]")
    else:
        # Interactive mode
        print("🎯 CHỌN CHIẾN LƯỢC CẬP NHẬT:")
        print("1. 🐌 An toàn (20 mã/batch, 2 phút delay, 5 batch)")
        print("2. ⚡ Tích cực (50 mã/batch, 1 phút delay, 10 batch)")
        print("3. 🎛️ Tùy chỉnh")
        print("4. ❌ Thoát")
        
        choice = input("\nNhập lựa chọn (1-4): ")
        
        if choice == "1":
            continue_update()
        elif choice == "2":
            aggressive_update()
        elif choice == "3":
            batch_size = input("Batch size (mặc định 20): ")
            batch_size = int(batch_size) if batch_size.isdigit() else 20
            
            delay = input("Delay giữa batch (phút, mặc định 2): ")
            delay = int(delay) if delay.isdigit() else 2
            
            max_batches = input("Số batch tối đa (mặc định 5): ")
            max_batches = int(max_batches) if max_batches.isdigit() else 5
            
            gradual_market_update(batch_size, delay, max_batches)
        else:
            print("👋 Thoát chương trình.")

if __name__ == "__main__":
    main()
