"""
Script quản lý cache dữ liệu chứng khoán
"""

import argparse
from data_cache import DataCache
import time

def main():
    parser = argparse.ArgumentParser(description='Quản lý cache dữ liệu chứng khoán')
    parser.add_argument('--action', choices=['update', 'full-update', 'stats', 'cleanup'], 
                       default='update', help='Hành động cần thực hiện')
    parser.add_argument('--symbols', nargs='+', help='Danh sách mã cổ phiếu cụ thể')
    parser.add_argument('--max', type=int, help='Giới hạn số lượng mã cập nhật')
    parser.add_argument('--force', action='store_true', help='Cập nhật toàn bộ dữ liệu')
    
    args = parser.parse_args()
    
    cache = DataCache()
    
    if args.action == 'stats':
        # Hiển thị thống kê
        stats = cache.get_cache_stats()
        print("\n=== THỐNG KÊ CACHE ===")
        print(f"Tổng số mã: {stats['total_symbols']}")
        print(f"Tổng số records: {stats['total_records']:,}")
        print(f"Khoảng thời gian: {stats['date_range']}")
        print(f"Kích thước DB: {stats['db_size_mb']} MB")
        
        # Hiển thị tổng quan thị trường
        overview = cache.get_market_overview()
        if not overview.empty:
            print(f"\n=== TỔNG QUAN THỊ TRƯỜNG ({len(overview)} mã) ===")
            print(overview.head(10).to_string(index=False))
    
    elif args.action == 'cleanup':
        # Dọn dẹp dữ liệu cũ
        deleted = cache.cleanup_old_data()
        print(f"Đã xóa {deleted} records cũ")
    
    elif args.action in ['update', 'full-update']:
        # Cập nhật cache
        def progress_callback(current, total, message):
            percent = (current / total) * 100
            print(f"[{current}/{total}] {percent:.1f}% - {message}")
        
        start_time = time.time()
        
        if args.action == 'full-update':
            print("🔄 Bắt đầu cập nhật toàn bộ dữ liệu...")
            # Cập nhật toàn bộ (force)
            success = cache.bulk_cache_update(
                symbols_list=args.symbols,
                max_symbols=args.max or 50,  # Mặc định 50 mã
                progress_callback=progress_callback
            )
        else:
            print("📈 Bắt đầu cập nhật dữ liệu mới...")
            # Cập nhật incremental
            success = cache.bulk_cache_update(
                symbols_list=args.symbols,
                max_symbols=args.max or 100,  # Mặc định 100 mã
                progress_callback=progress_callback
            )
        
        elapsed = time.time() - start_time
        print(f"\n✅ Hoàn thành trong {elapsed:.1f}s - {success} mã thành công")
        
        # Hiển thị stats sau khi cập nhật
        stats = cache.get_cache_stats()
        print(f"📊 Cache hiện có: {stats['total_symbols']} mã, {stats['total_records']:,} records")

if __name__ == "__main__":
    main()
