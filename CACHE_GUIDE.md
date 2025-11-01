# 🗄️ Hướng dẫn sử dụng hệ thống Cache dữ liệu

## 📋 Tổng quan

Hệ thống cache giúp:
- ✅ **Lưu trữ dữ liệu lịch sử** từ ngày niêm yết đến hiện tại
- ✅ **Giảm thời gian quét thị trường** từ 10+ phút xuống < 1 phút
- ✅ **Tránh rate limiting** của vnstock API
- ✅ **Tạo bảng so sánh toàn diện** tất cả mã chứng khoán
- ✅ **Cập nhật incremental** - chỉ lấy dữ liệu mới

## 🏗️ Kiến trúc hệ thống

```
📁 data_cache/
├── stock_data.db          # SQLite database chính
├── data_cache.py          # Core cache engine
├── cache_manager.py       # Command line tool
├── cached_stock_screener.py # Screener sử dụng cache
└── market_analysis_demo.py  # Demo phân tích thị trường
```

### 🗃️ Database Schema

**stock_prices**: Dữ liệu giá hàng ngày
- symbol, date, open, high, low, close, volume

**stock_info**: Thông tin cơ bản
- symbol, name, exchange, listing_date, last_update

**technical_indicators**: Chỉ báo kỹ thuật (future)
- symbol, date, sma_20, sma_50, rsi, macd, etc.

## 🚀 Cách sử dụng

### 1. Cập nhật cache lần đầu

```bash
# Cập nhật 50 mã đầu tiên (khuyến nghị để test)
python cache_manager.py --action update --max 50

# Cập nhật toàn bộ thị trường (1700+ mã, mất ~2-3 giờ)
python cache_manager.py --action full-update --max 1000
```

### 2. Cập nhật hàng ngày

```bash
# Cập nhật dữ liệu mới (incremental)
python cache_manager.py --action update

# Cập nhật chỉ một số mã cụ thể
python cache_manager.py --action update --symbols VNM VCB FPT
```

### 3. Xem thống kê cache

```bash
python cache_manager.py --action stats
```

**Output mẫu:**
```
=== THỐNG KÊ CACHE ===
Tổng số mã: 50
Tổng số records: 45,230
Khoảng thời gian: 2022-01-01 to 2025-11-01
Kích thước DB: 15.2 MB

=== TỔNG QUAN THỊ TRƯỜNG (50 mã) ===
symbol                    name exchange  current_price  volume
   VNM      Vinamilk - CTCP Sữa VN     HOSE        57600.0  1250000
   VCB  Vietcombank - NH TMCP Ngoại     HOSE        59600.0   890000
   FPT        FPT - CTCP FPT     HOSE        89500.0  2100000
```

### 4. Dọn dẹp dữ liệu cũ

```bash
# Xóa dữ liệu cũ hơn 3 năm
python cache_manager.py --action cleanup
```

## 📊 Phân tích thị trường với Cache

### Demo phân tích toàn diện

```bash
python market_analysis_demo.py
```

**Kết quả:**
- 📈 **Market Overview**: Tổng quan 50+ mã
- 🏆 **Top Performers**: Top theo nhiều tiêu chí
- 🎯 **Filtered Results**: Lọc theo tín hiệu mua/bán
- 📉 **Oversold Opportunities**: Cơ hội mua vào
- 📊 **High Volume Activity**: Hoạt động khối lượng cao
- 💾 **Excel Export**: Xuất báo cáo chi tiết

### Sử dụng trong code

```python
from cached_stock_screener import CachedStockScreener

# Khởi tạo
screener = CachedStockScreener()

# Tạo bảng so sánh thị trường
market_df = screener.get_market_comparison_table(
    update_cache=False,  # True để cập nhật cache trước
    max_symbols=100      # Giới hạn số lượng mã
)

# Lọc theo tiêu chí
buy_signals = screener.filter_by_criteria(market_df, {
    'signal_filter': ['MUA', 'MUA MẠNH'],
    'min_overall_score': 60,
    'rsi_range': (20, 50)
})

# Top performers
top_monthly = screener.get_top_performers(market_df, 'monthly', 10)
top_technical = screener.get_top_performers(market_df, 'technical', 10)

# Xuất Excel
screener.export_to_excel(market_df, 'market_analysis.xlsx')
```

## 📈 Các metrics trong bảng so sánh

### 🔢 Thông tin cơ bản
- **symbol, name, exchange**: Thông tin mã
- **current_price, volume**: Giá và khối lượng hiện tại

### 📊 Performance
- **monthly_return**: Lợi nhuận 1 tháng (%)
- **quarterly_return**: Lợi nhuận 3 tháng (%)
- **ytd_return**: Lợi nhuận từ đầu năm (%)

### 📉 Chỉ báo kỹ thuật
- **rsi**: Relative Strength Index
- **macd**: MACD signal
- **sma_20, sma_50, sma_200**: Moving averages
- **bb_position**: Vị trí trong Bollinger Bands (0-1)

### 🎯 Price levels
- **high_52w, low_52w**: Đỉnh/đáy 52 tuần
- **dist_from_high, dist_from_low**: Khoảng cách từ đỉnh/đáy (%)

### ⚠️ Risk metrics
- **volatility**: Độ biến động annualized (%)
- **volume_ratio**: Tỷ lệ khối lượng vs trung bình 20 ngày

### 🎯 Trading signals
- **overall_score**: Điểm tổng hợp (0-100)
- **technical_score**: Điểm kỹ thuật (0-100)
- **signal**: Tín hiệu (MUA MẠNH, MUA, GIỮ, BÁN, BÁN MẠNH)
- **risk_reward_ratio**: Tỷ lệ rủi ro/lợi nhuận

## 🔄 Quy trình cập nhật tự động

### Crontab (Linux/Mac)
```bash
# Cập nhật hàng ngày lúc 18:00
0 18 * * 1-5 cd /path/to/project && python cache_manager.py --action update

# Dọn dẹp hàng tuần
0 2 * * 0 cd /path/to/project && python cache_manager.py --action cleanup
```

### Task Scheduler (Windows)
- Tạo task chạy `cache_manager.py --action update` hàng ngày
- Tạo task chạy `cache_manager.py --action cleanup` hàng tuần

## 🎯 Lợi ích so với phương pháp cũ

| Tiêu chí | Cũ (Real-time API) | Mới (Cached) |
|----------|-------------------|--------------|
| **Thời gian quét** | 10-15 phút | < 1 phút |
| **Rate limiting** | Thường xuyên | Không |
| **Dữ liệu lịch sử** | Giới hạn | Đầy đủ từ niêm yết |
| **So sánh thị trường** | Không | Có |
| **Reliability** | Thấp | Cao |
| **Offline analysis** | Không | Có |

## 🛠️ Troubleshooting

### Lỗi thường gặp

**1. "No cached data found"**
```bash
# Giải pháp: Cập nhật cache
python cache_manager.py --action update --max 50
```

**2. "Database locked"**
```bash
# Giải pháp: Đóng tất cả connections
pkill -f cache_manager.py
rm -f data_cache/stock_data.db-wal data_cache/stock_data.db-shm
```

**3. "Rate limiting from vnstock"**
```bash
# Giải pháp: Tăng delay hoặc giảm batch size
# Sửa trong data_cache.py: time.sleep(0.5) -> time.sleep(1.0)
```

### Tối ưu hóa

**1. Tăng tốc độ cập nhật:**
- Chạy parallel với nhiều process
- Sử dụng SSD thay vì HDD
- Tăng RAM cho SQLite cache

**2. Giảm dung lượng:**
- Chỉ lưu dữ liệu 2-3 năm gần nhất
- Nén database định kỳ
- Xóa các chỉ báo không cần thiết

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra logs trong terminal
2. Chạy `--action stats` để xem tình trạng cache
3. Thử cập nhật với số lượng mã nhỏ trước
4. Kiểm tra kết nối internet và vnstock API

---

💡 **Tip**: Bắt đầu với 20-50 mã để test, sau đó mở rộng dần lên toàn thị trường!
