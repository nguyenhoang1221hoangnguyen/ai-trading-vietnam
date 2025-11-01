# 🚀 Hướng dẫn Deploy Ứng dụng lên Cloud (Miễn phí)

## 📋 Tổng quan các nền tảng miễn phí

### 🥇 Streamlit Cloud (KHUYẾN NGHỊ)
- ✅ **Hoàn toàn miễn phí**
- ✅ Tích hợp GitHub trực tiếp
- ✅ Auto-deploy khi push code
- ✅ URL công khai: `https://your-app.streamlit.app`
- ✅ Không giới hạn bandwidth

### 🥈 Railway
- ✅ Free tier: $5 credit/tháng
- ⚠️ Cần thẻ tín dụng (nhưng không charge nếu dưới limit)
- ✅ Dễ deploy từ GitHub

### 🥉 Render
- ✅ Free tier nhưng có giới hạn
- ⚠️ App sẽ sleep sau 15 phút không dùng
- ✅ Dễ deploy

---

## 🌟 Hướng dẫn Deploy lên Streamlit Cloud (Khuyến nghị)

### Bước 1: Đảm bảo code đã trên GitHub
```bash
# Kiểm tra code đã push chưa
git status
git push
```

### Bước 2: Truy cập Streamlit Cloud
1. Mở trình duyệt: https://share.streamlit.io/
2. Click **"Sign up"** hoặc **"Sign in"**
3. Đăng nhập bằng **GitHub account** của bạn

### Bước 3: Deploy ứng dụng
1. Click **"New app"**
2. Chọn:
   - **Repository**: `nguyenhoang1221hoangnguyen/ai-trading-vietnam`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Click **"Deploy!"**

### Bước 4: Đợi deploy hoàn thành
- Streamlit sẽ tự động cài đặt dependencies từ `requirements.txt`
- Thời gian: ~2-3 phút
- URL sẽ có dạng: `https://ai-trading-vietnam.streamlit.app`

### Bước 5: Chia sẻ với mọi người
- Copy URL và chia sẻ
- Mọi người có thể truy cập trực tiếp từ trình duyệt
- **Không cần cài đặt gì!**

---

## 📝 Lưu ý quan trọng khi deploy

### 1. Database SQLite trên Cloud
- Database sẽ được tạo tự động khi chạy
- **Dữ liệu sẽ mất khi app restart** (vì ephemeral storage)
- **Giải pháp**: Sử dụng cloud database (nếu cần persistent data)

### 2. Rate Limiting
- Vnstock API có rate limit
- Nên cài đặt delay phù hợp khi quét thị trường
- Sử dụng cache để giảm số lượng request

### 3. Memory và Performance
- Streamlit Cloud free tier có giới hạn memory
- Khuyến nghị: Quét từng batch nhỏ (20-50 mã)

### 4. Environment Variables (Nếu cần)
- Trong Streamlit Cloud: **Settings** → **Secrets**
- Thêm các biến môi trường nếu cần (API keys, etc.)

---

## 🔧 Deploy lên Railway (Phương án 2)

### Bước 1: Tạo tài khoản
1. Truy cập: https://railway.app
2. Đăng nhập bằng GitHub
3. Click **"New Project"**

### Bước 2: Deploy từ GitHub
1. Chọn **"Deploy from GitHub repo"**
2. Chọn repository: `ai-trading-vietnam`
3. Railway tự động detect Streamlit

### Bước 3: Cấu hình
- **Build Command**: Để trống (Railway tự detect)
- **Start Command**: `streamlit run app.py --server.port $PORT`
- **Environment Variables**: Thêm nếu cần

### Bước 4: Lấy URL
- Railway sẽ cung cấp URL công khai
- Có thể setup custom domain

---

## 🔧 Deploy lên Render (Phương án 3)

### Bước 1: Tạo file `render.yaml`
```yaml
services:
  - type: web
    name: ai-trading-vietnam
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

### Bước 2: Deploy
1. Truy cập: https://render.com
2. Tạo **New Web Service**
3. Connect GitHub repository
4. Render sẽ tự động detect và deploy

---

## ✅ Checklist trước khi deploy

- [x] Code đã push lên GitHub
- [x] `requirements.txt` đã đầy đủ dependencies
- [x] Không có hardcoded secrets trong code
- [x] `.gitignore` đã loại trừ file nhạy cảm
- [x] Test chạy local thành công

---

## 🎯 Sau khi deploy

### Streamlit Cloud tự động:
- ✅ Cập nhật khi bạn push code mới lên GitHub
- ✅ Restart app nếu có lỗi
- ✅ Logs có thể xem trong dashboard

### Chia sẻ với người khác:
```
URL: https://ai-trading-vietnam.streamlit.app
```

Mọi người chỉ cần:
1. Mở URL trong trình duyệt
2. Sử dụng ngay, không cần cài đặt!

---

## 🐛 Xử lý lỗi thường gặp

### Lỗi: "Module not found"
- Kiểm tra `requirements.txt` đã đủ chưa
- Thêm module thiếu vào requirements.txt
- Push lại và deploy lại

### Lỗi: "App failed to start"
- Kiểm tra logs trong Streamlit Cloud dashboard
- Đảm bảo `app.py` là file chính
- Kiểm tra Python version compatibility

### App chạy chậm
- Giảm số lượng mã quét mỗi lần
- Tăng delay giữa các request
- Sử dụng cache hiệu quả hơn

---

## 📚 Tài liệu tham khảo

- Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud
- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs

---

## 🎉 Chúc mừng!

Sau khi deploy thành công, ứng dụng của bạn sẽ:
- ✅ Truy cập được từ bất kỳ đâu
- ✅ Chạy 24/7 (Streamlit Cloud)
- ✅ Tự động cập nhật khi push code mới
- ✅ Hoàn toàn miễn phí!

