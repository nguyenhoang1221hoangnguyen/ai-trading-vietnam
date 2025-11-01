# ▶️ Hướng dẫn chạy ứng dụng

## 🚀 Cách nhanh nhất (3 bước)

### 1️⃣ Mở Terminal/Command Prompt

**Windows**: 
- Nhấn `Win + R`, gõ `cmd`, nhấn Enter
- Hoặc search "Command Prompt"

**macOS**: 
- Nhấn `Cmd + Space`, gõ "Terminal", nhấn Enter

**Linux**: 
- Nhấn `Ctrl + Alt + T`

### 2️⃣ Di chuyển đến thư mục dự án

```bash
cd "đường/dẫn/đến/3110 aitrading "
```

**Ví dụ trên macOS/Linux**:
```bash
cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/3110 aitrading "
```

**Ví dụ trên Windows**:
```cmd
cd "C:\Users\YourName\Desktop\2025\hoc-tap code\vscode\3110 aitrading "
```

### 3️⃣ Chạy ứng dụng

**Cách 1 - Dùng script có sẵn (Khuyến nghị)**:

**macOS/Linux**:
```bash
chmod +x run.sh
./run.sh
```

**Windows**:
```cmd
run.bat
```

**Cách 2 - Chạy thủ công**:
```bash
# Cài đặt thư viện (chỉ cần làm 1 lần)
pip install -r requirements.txt

# Chạy ứng dụng
streamlit run app.py
```

### ✅ Xong!

Ứng dụng sẽ tự động mở trong trình duyệt tại: http://localhost:8501

Nếu không tự động mở, hãy mở trình duyệt và truy cập địa chỉ trên.

---

## 🐛 Xử lý lỗi thường gặp

### Lỗi: "python không được nhận dạng"

**Nguyên nhân**: Chưa cài Python hoặc chưa thêm vào PATH

**Giải pháp**:
1. Tải Python tại: https://www.python.org/downloads/
2. Khi cài, **nhớ check** "Add Python to PATH"
3. Khởi động lại Terminal/CMD

### Lỗi: "pip không được nhận dạng"

**Giải pháp**:
```bash
# Thử dùng python -m pip thay vì pip
python -m pip install -r requirements.txt
python -m streamlit run app.py

# Hoặc dùng python3 (trên macOS/Linux)
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

### Lỗi: "ModuleNotFoundError: No module named 'streamlit'"

**Nguyên nhân**: Chưa cài thư viện

**Giải pháp**:
```bash
pip install -r requirements.txt
```

### Lỗi: "Port 8501 is already in use"

**Nguyên nhân**: Cổng đang được sử dụng

**Giải pháp 1** - Dừng app cũ:
- Nhấn `Ctrl + C` trong Terminal đang chạy Streamlit

**Giải pháp 2** - Dùng cổng khác:
```bash
streamlit run app.py --server.port 8502
```

### Lỗi kết nối vnstock API

**Giải pháp**:
1. Kiểm tra Internet
2. Thử lại sau vài phút
3. Kiểm tra firewall
4. Thử VPN nếu cần

### Lỗi: "Permission denied" (macOS/Linux)

**Giải pháp**:
```bash
chmod +x run.sh
./run.sh
```

---

## 🧪 Test ứng dụng

### Test nhanh với demo script

```bash
python demo.py
```

Script này sẽ:
- ✅ Test kết nối API
- ✅ Test phân tích mã VNM
- ✅ Test tìm kiếm cổ phiếu
- ✅ Hiển thị kết quả mẫu

Thời gian: ~1-2 phút

### 🌍 Test tính năng quét toàn bộ thị trường (MỚI!)

1. **Test cache system**:
```bash
python cache_manager.py --action stats
```

2. **Test trong ứng dụng**:
   - Vào **"📈 Tổng quan thị trường"**
   - Tab **"⚙️ Cache Management"** 
   - Cài đặt test: 10 mã, 15 giây delay, 2 batch
   - Nhấn **"🚀 Bắt đầu quét toàn bộ thị trường"**
   - Kiểm tra tiến độ và logs

3. **Test Market Scanner**:
   - Tab **"🔍 Market Scanner"**
   - Quét 20 mã
   - Kiểm tra kết quả hiển thị nhanh

---

## 🎯 Sử dụng ứng dụng

### 1. Phân tích mã chứng khoán

1. Chọn "📊 Phân tích mã CK" ở menu bên trái
2. Nhập mã cổ phiếu (VD: VNM, FPT, VIC, HPG, VHM)
3. Chọn khung thời gian (VD: 1Y cho 1 năm)
4. Nhấn "🔍 Phân tích"
5. Đợi 3-5 giây để tải dữ liệu
6. Xem kết quả phân tích chi tiết

### 2. 🌍 Market Overview - Quét toàn bộ thị trường (TÍNH NĂNG MỚI!)

#### Bước 1: Chuẩn bị cache
1. Chọn **"📈 Tổng quan thị trường"**
2. Vào tab **"⚙️ Cache Management"**
3. Cài đặt quét:
   - **Batch size**: 20 mã (khuyến nghị)
   - **Delay**: 10 giây (an toàn)
   - **Max batches**: 20 (400 mã, ~3.5 phút)
4. Nhấn **"🚀 Bắt đầu quét toàn bộ thị trường"**
5. Theo dõi tiến độ real-time

#### Bước 2: Sử dụng các tính năng
- **🔍 Market Scanner**: Quét nhanh 50-200 mã trong vài giây
- **🏆 Top Performers**: Xem top cổ phiếu theo nhiều tiêu chí
- **📊 Market Analysis**: Lọc thông minh và export Excel

### 3. Tìm cổ phiếu tiềm năng (phương pháp cũ)

1. Chọn "🔎 Tìm kiếm CK tiềm năng"
2. Tab "🎯 Quét thị trường"
3. Chọn loại đầu tư (Ngắn hạn/Trung hạn/Dài hạn)
4. Nhấn "🚀 Bắt đầu quét"
5. Đợi quá trình quét hoàn tất (30-60 giây)
6. Xem danh sách cổ phiếu được đề xuất

### 4. Tìm cơ hội đặc biệt

1. Tab "🚀 Cổ phiếu đặc biệt"
2. Chọn:
   - "🚀 Tìm cổ phiếu đang Breakout" (đột phá lên)
   - "📉 Tìm cổ phiếu quá bán" (cơ hội mua)
3. Xem kết quả

---

## 📝 Checklist trước khi chạy

- [ ] Đã cài Python 3.8 trở lên
- [ ] Đã mở Terminal/CMD
- [ ] Đã cd vào thư mục dự án
- [ ] Có kết nối Internet
- [ ] Đã cài đặt thư viện (pip install -r requirements.txt)

---

## 💡 Tips

### Tăng tốc độ load
- Cache sẽ lưu dữ liệu trong 1 giờ
- Lần phân tích thứ 2 sẽ nhanh hơn

### Clear cache
Trong ứng dụng, nhấn:
- Phím `C` trong terminal để clear cache
- Hoặc chọn "Clear cache" trong menu Streamlit

### Dừng ứng dụng
Trong Terminal đang chạy Streamlit:
- Nhấn `Ctrl + C`
- Xác nhận `Y` (nếu được hỏi)

### Chạy background (macOS/Linux)
```bash
nohup streamlit run app.py &
```

### Xem log
```bash
# Log sẽ hiển thị trong Terminal
# Để debug, kiểm tra log khi có lỗi
```

---

## 🌐 Truy cập từ thiết bị khác

### Trong cùng mạng WiFi

1. Tìm IP của máy chạy ứng dụng:

**Windows**:
```cmd
ipconfig
```
Tìm "IPv4 Address"

**macOS/Linux**:
```bash
ifconfig | grep "inet "
```
Hoặc
```bash
hostname -I
```

2. Chạy Streamlit với network:
```bash
streamlit run app.py --server.address 0.0.0.0
```

3. Truy cập từ thiết bị khác:
```
http://[IP_CỦA_MÁY]:8501
```

Ví dụ: `http://192.168.1.100:8501`

---

## 🆘 Cần trợ giúp?

1. **Đọc tài liệu**:
   - README.md - Hướng dẫn chi tiết
   - QUICKSTART.md - Bắt đầu nhanh
   - INSTALL.md - Cài đặt chi tiết

2. **Chạy demo**:
   ```bash
   python demo.py
   ```

3. **Kiểm tra log** trong Terminal

4. **Báo lỗi**: Tạo issue trên GitHub với:
   - Mô tả lỗi
   - Cách tái hiện
   - Screenshot (nếu có)
   - Log lỗi

---

## ✅ Kiểm tra cài đặt

Chạy các lệnh sau để kiểm tra:

```bash
# Kiểm tra Python
python --version

# Kiểm tra pip
pip --version

# Kiểm tra Streamlit
streamlit --version

# Liệt kê thư viện đã cài
pip list
```

Phải có:
- streamlit
- vnstock3
- pandas
- numpy
- plotly
- ta

---

**🎉 Chúc bạn sử dụng thành công!**

**Nếu thấy hữu ích, hãy cho 1 ⭐ trên GitHub!**

