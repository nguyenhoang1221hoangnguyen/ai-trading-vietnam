# 📦 Hướng dẫn cài đặt chi tiết

## Yêu cầu hệ thống

- **Python**: 3.8 trở lên
- **Hệ điều hành**: Windows, macOS, Linux
- **RAM**: Tối thiểu 4GB
- **Kết nối Internet**: Cần thiết để lấy dữ liệu

## Cách 1: Cài đặt nhanh (Khuyến nghị)

### Windows

1. Mở Command Prompt hoặc PowerShell
2. Di chuyển đến thư mục dự án:
```cmd
cd "đường/dẫn/đến/3110 aitrading "
```

3. Chạy file batch:
```cmd
run.bat
```

### macOS / Linux

1. Mở Terminal
2. Di chuyển đến thư mục dự án:
```bash
cd "/đường/dẫn/đến/3110 aitrading "
```

3. Cấp quyền thực thi và chạy:
```bash
chmod +x run.sh
./run.sh
```

## Cách 2: Cài đặt thủ công

### Bước 1: Kiểm tra Python

```bash
python --version
# hoặc
python3 --version
```

Nếu chưa có Python, tải tại: https://www.python.org/downloads/

### Bước 2: Tạo môi trường ảo (Khuyến nghị)

```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Bước 3: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Bước 4: Chạy ứng dụng

```bash
streamlit run app.py
```

### Bước 5: Mở trình duyệt

Ứng dụng sẽ tự động mở tại: http://localhost:8501

Nếu không tự động mở, hãy mở trình duyệt và truy cập địa chỉ trên.

## Xử lý lỗi thường gặp

### Lỗi 1: "ModuleNotFoundError"

**Nguyên nhân**: Thiếu thư viện

**Giải pháp**:
```bash
pip install -r requirements.txt --upgrade
```

### Lỗi 2: "vnstock3 not found"

**Nguyên nhân**: vnstock3 chưa được cài đặt đúng

**Giải pháp**:
```bash
pip uninstall vnstock3
pip install vnstock3==1.0.9
```

### Lỗi 3: "Port 8501 is already in use"

**Nguyên nhân**: Cổng đã được sử dụng

**Giải pháp**:
```bash
streamlit run app.py --server.port 8502
```

### Lỗi 4: Lỗi kết nối API

**Nguyên nhân**: Không thể kết nối đến vnstock API

**Giải pháp**:
- Kiểm tra kết nối Internet
- Thử lại sau vài phút
- Kiểm tra firewall

### Lỗi 5: Lỗi "ta" (TA-Lib)

**Nguyên nhân**: Thư viện ta (ta-lib) có thể cần cài đặt đặc biệt

**Giải pháp**:

**Windows**:
```bash
pip install ta
```

**macOS**:
```bash
brew install ta-lib
pip install ta
```

**Linux**:
```bash
sudo apt-get install ta-lib
pip install ta
```

## Kiểm tra cài đặt

Chạy lệnh sau để kiểm tra các thư viện đã cài đặt:

```bash
pip list
```

Đảm bảo có các thư viện sau:
- streamlit
- vnstock3
- pandas
- numpy
- plotly
- ta
- scipy

## Cập nhật ứng dụng

Để cập nhật lên phiên bản mới nhất:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Gỡ cài đặt

### Xóa môi trường ảo

```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

### Gỡ thư viện

```bash
pip uninstall -r requirements.txt -y
```

## Hỗ trợ

Nếu gặp vấn đề trong quá trình cài đặt:

1. Kiểm tra file README.md
2. Tạo issue trên GitHub
3. Liên hệ qua email

## Tips

1. **Sử dụng môi trường ảo**: Tránh xung đột thư viện
2. **Cập nhật pip**: `pip install --upgrade pip`
3. **Cache dữ liệu**: Streamlit sẽ cache dữ liệu để tăng tốc độ
4. **Clear cache**: Nhấn 'c' trong terminal nếu cần clear cache

---

**Chúc bạn cài đặt thành công! 🎉**

