# 🔧 Troubleshooting - Xử lý lỗi và cảnh báo

## ⚠️ Console Warnings (Cảnh báo trong Console)

### Các cảnh báo về Permissions Policy

Khi chạy ứng dụng trên Streamlit Cloud, bạn có thể thấy các cảnh báo trong console trình duyệt:

```
Unrecognized feature: 'ambient-light-sensor'
Unrecognized feature: 'battery'
Unrecognized feature: 'document-domain'
...
```

**Đây KHÔNG phải lỗi nghiêm trọng!** ✅

- ✅ **Ứng dụng vẫn hoạt động bình thường**
- ✅ **Không ảnh hưởng đến chức năng**
- ✅ **Chỉ là warnings từ trình duyệt**

**Nguyên nhân:**
- Streamlit cố gắng sử dụng các tính năng trình duyệt bị chặn bởi Permissions Policy
- Một số tính năng không được hỗ trợ trong môi trường iframe của Streamlit Cloud

**Giải pháp:**
- **Bỏ qua**: Các cảnh báo này an toàn và không cần xử lý
- Nếu muốn ẩn: Sử dụng Developer Tools để filter warnings

---

## ❌ Lỗi thực sự cần xử lý

### 1. "Không thể lấy dữ liệu cho mã VNM"

**Triệu chứng:**
- Thông báo lỗi khi phân tích mã chứng khoán
- Không hiển thị biểu đồ hoặc dữ liệu

**Nguyên nhân có thể:**
- API vnstock tạm thời không khả dụng
- Rate limit (quá nhiều request)
- Mã chứng khoán không tồn tại
- Vấn đề kết nối mạng

**Giải pháp:**
1. **Thử lại sau 10-15 giây** (đợi rate limit reset)
2. **Kiểm tra mã chứng khoán** (VD: VNM, FPT, VIC - các mã lớn thường ổn định)
3. **Giảm số lượng request**: Không quét quá nhiều mã cùng lúc
4. **Sử dụng cache**: Ứng dụng tự động cache dữ liệu để tránh request lại

**Code đã được tối ưu:**
- ✅ Auto-retry với exponential backoff
- ✅ Tự động fallback sang yfinance
- ✅ Delay giữa các request
- ✅ Suppress warnings không cần thiết

---

### 2. "Module not found" khi deploy

**Triệu chứng:**
- App không start trên Streamlit Cloud
- Lỗi trong logs: `ModuleNotFoundError`

**Giải pháp:**
1. Kiểm tra `requirements.txt` đã đầy đủ chưa
2. Đảm bảo tất cả dependencies đã được list
3. Push lại code và deploy lại

**Dependencies cần có:**
```
streamlit>=1.28.0
vnstock>=3.2.1
pandas>=2.1.0
numpy>=1.24.0
plotly>=5.17.0
ta>=0.11.0
scipy>=1.11.0
requests>=2.31.0
python-dateutil>=2.8.2
openpyxl>=3.1.0
yfinance>=0.2.28
```

---

### 3. App chạy chậm trên Streamlit Cloud

**Nguyên nhân:**
- Memory limit của free tier
- Quét quá nhiều mã cùng lúc
- API rate limiting

**Giải pháp:**
- ✅ Quét từng batch nhỏ (20-50 mã)
- ✅ Sử dụng cache thông minh
- ✅ Tăng delay giữa các request
- ✅ Ưu tiên sử dụng Market Overview (nhanh hơn)

---

### 4. Database SQLite không lưu dữ liệu

**Triệu chứng:**
- Cache bị mất sau khi app restart
- Phải quét lại từ đầu

**Nguyên nhân:**
- Streamlit Cloud sử dụng ephemeral storage
- Dữ liệu sẽ mất khi app restart hoặc rebuild

**Giải pháp:**
- **Hiện tại**: Chấp nhận dữ liệu tạm thời
- **Tương lai**: Tích hợp cloud database (PostgreSQL, MySQL) nếu cần persistent data

**Workaround:**
- Sử dụng Market Overview để cache trong session
- Export Excel để lưu dữ liệu offline

---

### 5. "AuthSessionMissingError"

**Triệu chứng:**
- Console hiển thị: `AuthSessionMissingError: Auth session missing!`

**Giải pháp:**
- ✅ **Đây là warning vô hại từ Streamlit**
- ✅ **Không ảnh hưởng đến chức năng**
- ✅ Code đã suppress warning này

---

## 🔍 Debug Mode

Để xem thông tin debug chi tiết hơn:

1. **Trong Streamlit Cloud:**
   - Vào **Settings** → **Secrets**
   - Thêm: `STREAMLIT_DEBUG = true`
   - App sẽ hiển thị thêm thông tin lỗi

2. **Trong code local:**
   ```bash
   export STREAMLIT_DEBUG=true
   streamlit run app.py
   ```

---

## 📊 Kiểm tra Logs trên Streamlit Cloud

1. Vào dashboard: https://share.streamlit.io/
2. Chọn app của bạn
3. Click **"Manage app"** → **"Logs"**
4. Xem các thông báo lỗi chi tiết

---

## ✅ Checklist Khi Gặp Lỗi

- [ ] Đã thử lại sau 10-15 giây?
- [ ] Đã kiểm tra mã chứng khoán có đúng không?
- [ ] Đã test với mã khác (VNM, FPT, VIC)?
- [ ] Đã kiểm tra logs trong Streamlit Cloud?
- [ ] Đã đảm bảo requirements.txt đầy đủ?
- [ ] Đã clear cache và thử lại?

---

## 🆘 Liên hệ Hỗ trợ

Nếu vẫn gặp vấn đề:

1. **Xem logs chi tiết** trong Streamlit Cloud dashboard
2. **Chụp screenshot** lỗi cụ thể
3. **Ghi lại** các bước tái hiện lỗi
4. **Kiểm tra** version của dependencies

---

## 💡 Tips Tối Ưu

### Cho Performance:
- ✅ Sử dụng cache (`@st.cache_data`)
- ✅ Quét batch nhỏ (20-50 mã)
- ✅ Tăng delay giữa requests (5-10s)
- ✅ Ưu tiên Market Overview thay vì scan từng mã

### Cho Reliability:
- ✅ Auto-retry với exponential backoff
- ✅ Fallback sang yfinance
- ✅ Error handling tốt
- ✅ Suppress warnings không cần thiết

---

**Lưu ý**: Hầu hết các "lỗi" bạn thấy trong console chỉ là **warnings vô hại** từ trình duyệt. Ứng dụng vẫn hoạt động bình thường! ✅

