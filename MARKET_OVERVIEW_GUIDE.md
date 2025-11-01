# 📈 Hướng dẫn sử dụng Market Overview

## 🎯 Tổng quan
Tính năng **Market Overview** cho phép bạn phân tích toàn diện 1700+ mã chứng khoán trong vài giây nhờ hệ thống cache thông minh. **TÍNH NĂNG MỚI**: Quét toàn bộ thị trường qua giao diện web, không cần sử dụng terminal!

## 🚀 Cách sử dụng

### 1. Truy cập Market Overview
- Mở ứng dụng tại: http://localhost:8506
- Chọn tab "📈 Tổng quan thị trường"

### 2. Chuẩn bị dữ liệu Cache

#### 🌍 PHƯƠNG PHÁP MỚI - Quét qua giao diện web (KHUYẾN NGHỊ):
1. **Truy cập**: Vào tab "⚙️ Cache Management"
2. **Cài đặt quét**:
   - **Batch size**: 20 mã (khuyến nghị cho lần đầu)
   - **Delay**: 10 giây (an toàn, tránh rate limit)
   - **Max batches**: 20 (sẽ quét 400 mã, ~3.5 phút)
3. **Bắt đầu**: Click "🚀 Bắt đầu quét toàn bộ thị trường"
4. **Theo dõi**: Xem tiến độ real-time, có thể dừng bất kỳ lúc nào

#### Phương pháp cũ - Terminal (tùy chọn):
```bash
# Cập nhật cache 50 mã đầu tiên
python cache_manager.py --action update --max 50

# Hoặc cập nhật nhiều hơn
python cache_manager.py --action update --max 200
```

#### Cập nhật nhanh trong ứng dụng:
- Click "🔄 Cập nhật Cache Incremental" với số lượng tùy chọn

### 3. Các Tab chính

#### 🔍 Market Scanner
- **Quét nhanh**: Chọn số lượng mã (10-500)
- **Tự động cập nhật**: Tick để refresh cache trước khi quét
- **Kết quả**: Hiển thị tóm tắt thống kê thị trường

#### 🏆 Top Performers
- **6 danh mục**: Tổng hợp, Tăng trưởng tháng/quý, Kỹ thuật, Rủi ro thấp, Khối lượng cao
- **Top 3 nổi bật**: Hiển thị medal với thông tin chi tiết
- **Bảng chi tiết**: Dữ liệu đầy đủ với format VNĐ

#### 📊 Market Analysis
- **Bộ lọc thông minh**: 
  - Điểm tối thiểu (0-100)
  - Tín hiệu (MUA MẠNH, MUA, GIỮ, BÁN, BÁN MẠNH)
  - RSI Range (0-100)
  - Tỷ lệ khối lượng
  - Tăng trưởng tháng
  - Xu hướng
- **Export Excel**: Xuất kết quả lọc hoặc toàn bộ dữ liệu

#### ⚙️ Cache Management
- **Cập nhật Incremental**: Cập nhật số lượng mã tùy chọn (10-1000 mã)
- **🌍 QUÉT TOÀN BỘ THỊ TRƯỜNG** (TÍNH NĂNG MỚI):
  - **Cài đặt linh hoạt**: Batch size (10-50), delay (5-30s), số batch tối đa
  - **Tiến độ real-time**: Progress bar, logs, metrics thành công/thất bại
  - **Điều khiển dễ dàng**: Bắt đầu/dừng bất kỳ lúc nào qua giao diện
  - **Ước tính thông minh**: Thời gian và số lượng mã sẽ quét
- **Dọn dẹp**: Xóa dữ liệu cũ
- **Thống kê**: Xem danh sách mã trong cache

## 📊 Ưu điểm của Cache System

### Tốc độ
- **Trước**: 5-10 phút để quét 100 mã
- **Sau**: < 10 giây để phân tích 1000+ mã

### Độ tin cậy
- Retry mechanism tự động
- Fallback data sources
- Error handling thông minh

### Tính năng nâng cao
- **Bulk update**: Cập nhật hàng loạt
- **Incremental sync**: Chỉ cập nhật dữ liệu mới
- **Auto cleanup**: Tự động dọn dẹp dữ liệu cũ
- **Export Excel**: Xuất báo cáo chi tiết

## 🔧 Cấu hình Cache

### Thời gian cache
- **Intraday data**: 5 phút
- **Daily data**: 1 giờ
- **Company info**: 24 giờ

### Dung lượng
- **SQLite database**: Tự động tối ưu
- **Compression**: Nén dữ liệu thông minh
- **Cleanup**: Xóa dữ liệu > 30 ngày

## 🚨 Xử lý lỗi thường gặp

### "Chưa có dữ liệu cache"
```bash
# Giải pháp
python cache_manager.py --action update --max 20
```

### "Market scan bị stuck"
- Giảm số lượng mã quét (10-50)
- Tắt "Cập nhật cache trước khi quét"
- Restart ứng dụng

### "Export Excel thất bại"
- Kiểm tra quyền ghi file
- Đóng file Excel nếu đang mở
- Thử lại với tên file khác

## 📈 Best Practices

### 1. Cài đặt quét toàn bộ thị trường khuyến nghị

#### 🟢 An toàn (lần đầu sử dụng):
- **Batch size**: 10 mã
- **Delay**: 15 giây
- **Max batches**: 10 (100 mã, ~2.5 phút)

#### 🟡 Cân bằng (sử dụng thường xuyên):
- **Batch size**: 20 mã
- **Delay**: 10 giây  
- **Max batches**: 20 (400 mã, ~3.5 phút)

#### 🟠 Tích cực (có kinh nghiệm):
- **Batch size**: 50 mã
- **Delay**: 5 giây
- **Max batches**: 50 (2500 mã, ~4 phút)

### 2. Cập nhật Cache định kỳ

#### Qua giao diện web (khuyến nghị):
- **Hàng ngày**: Quét 200-400 mã qua UI
- **Cuối tuần**: Quét toàn bộ thị trường (1700+ mã)

#### Qua terminal (tùy chọn):
```bash
# Hàng ngày
python cache_manager.py --action update --max 100

# Cuối tuần (full update)
python cache_manager.py --action update --max 1000
```

### 3. Sử dụng bộ lọc hiệu quả
- Bắt đầu với điểm tối thiểu 60+
- Chọn tín hiệu MUA/MUA MẠNH
- RSI trong khoảng 30-70
- Tỷ lệ khối lượng > 1.2x

### 4. Export và phân tích
- Export Excel để phân tích offline
- Sử dụng pivot table trong Excel
- Tạo dashboard từ dữ liệu export

## 🎯 Workflow khuyến nghị

### Sáng (9:00 AM)
1. Cập nhật cache: `python cache_manager.py --action update --max 50`
2. Quét thị trường với 100-200 mã
3. Xem Top Performers trong từng danh mục
4. Export danh sách quan tâm

### Trưa (12:00 PM)
1. Quét lại với cache cũ (nhanh)
2. So sánh với kết quả sáng
3. Cập nhật watchlist

### Chiều (3:00 PM)
1. Cập nhật cache cuối ngày
2. Phân tích chi tiết với bộ lọc
3. Export báo cáo tổng kết
4. Chuẩn bị cho ngày hôm sau

## 🔗 Tích hợp với các tính năng khác

### Phân tích mã CK
- Từ Market Overview → Click mã → Chuyển sang tab "Phân tích mã CK"
- Copy/paste mã từ bảng kết quả

### Tìm kiếm CK tiềm năng
- Sử dụng kết hợp cả 2 tính năng
- Market Overview cho overview, Tìm kiếm CK cho deep dive

## 📞 Hỗ trợ

### Logs và Debug
```bash
# Xem logs cache
python cache_manager.py --action stats

# Debug mode
streamlit run app.py --logger.level debug
```

### Performance Monitoring
- Theo dõi thời gian response
- Monitor database size
- Check memory usage

---

**Lưu ý**: Tính năng này yêu cầu kết nối internet ổn định và có thể bị giới hạn bởi API rate limits của vnstock.
