# 🚀 Hướng dẫn Deploy lên Streamlit Cloud

## Chuẩn bị trước khi deploy

### 1. Kiểm tra repository
- ✅ Code đã được commit và push lên GitHub
- ✅ File `requirements.txt` có đầy đủ dependencies
- ✅ File `.streamlit/config.toml` đã được cấu hình

### 2. Tạo tài khoản Streamlit Cloud
1. Truy cập: https://share.streamlit.io/
2. Đăng nhập bằng GitHub account
3. Authorize Streamlit để truy cập repositories

## Các bước deploy

### Bước 1: Tạo app mới
1. Click **"New app"**
2. Chọn repository: `nguyenhoang1221hoangnguyen/ai-trading-vietnam`
3. Branch: `main`
4. Main file path: `app.py`
5. App URL: Chọn tên domain (VD: `ai-trading-vietnam`)

### Bước 2: Cấu hình Advanced settings (Tùy chọn)
```toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = true
fileWatcherType = "poll"

[browser]
gatherUsageStats = false

[runner]
fastReruns = true
magicEnabled = true

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Bước 3: Deploy
1. Click **"Deploy!"**
2. Đợi quá trình build (2-5 phút)
3. App sẽ tự động mở khi hoàn tất

## Xử lý lỗi thường gặp

### 1. Lỗi "Không thể lấy dữ liệu"
**Nguyên nhân:**
- API rate limiting trên cloud environment
- Network timeout
- 403 Forbidden errors

**Giải pháp:**
- App đã có retry logic và error handling tốt
- Thử lại sau 30-60 giây
- Sử dụng tính năng cache để giảm tải API

### 2. Console warnings (Có thể bỏ qua)
```
Unrecognized feature: 'ambient-light-sensor'
An iframe which has both allow-scripts and allow-same-origin...
Invalid color passed for widgetBackgroundColor...
```

**Giải thích:**
- Đây là warnings từ browser, không ảnh hưởng chức năng
- Liên quan đến Permissions Policy và iframe sandboxing
- App vẫn hoạt động bình thường

### 3. Lỗi build dependencies
**Kiểm tra:**
- File `requirements.txt` có đúng format
- Tất cả packages đều có version hợp lệ
- Không có conflicts giữa các packages

## Tối ưu hóa cho Streamlit Cloud

### 1. Caching
```python
@st.cache_data(ttl=3600)  # Cache 1 giờ
def get_stock_data(symbol):
    # Implementation
```

### 2. Error handling
- App đã có error handling chi tiết
- Thông báo lỗi thân thiện với user
- Retry logic cho network issues

### 3. Performance
- Sử dụng `st.cache_data` cho data fetching
- Lazy loading cho heavy computations
- Optimized imports

## Monitoring và Maintenance

### 1. Logs
- Xem logs tại Streamlit Cloud dashboard
- Monitor app performance
- Track error rates

### 2. Updates
- Push code changes lên GitHub
- Streamlit Cloud sẽ tự động redeploy
- Có thể trigger manual reboot nếu cần

### 3. Scaling
- Streamlit Cloud có giới hạn resources
- Cân nhắc upgrade plan nếu cần
- Monitor concurrent users

## Troubleshooting

### App không load
1. Kiểm tra logs tại Streamlit Cloud
2. Verify GitHub repository access
3. Check requirements.txt format

### Performance chậm
1. Optimize caching strategy
2. Reduce API calls
3. Use lighter computations

### API errors
1. Check rate limits
2. Implement exponential backoff
3. Add fallback mechanisms

## Liên kết hữu ích

- 📖 [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-cloud)
- 🐛 [Troubleshooting Guide](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/troubleshooting)
- 💬 [Community Forum](https://discuss.streamlit.io/)
- 📧 [Support](https://streamlit.io/contact)

---

## ✅ Checklist Deploy

- [ ] Code đã commit và push
- [ ] Requirements.txt updated
- [ ] Config.toml configured
- [ ] App tested locally
- [ ] GitHub repository public/accessible
- [ ] Streamlit Cloud account ready
- [ ] App deployed successfully
- [ ] Basic functionality tested
- [ ] Error handling verified
- [ ] Performance acceptable

**🎉 App URL sau khi deploy:** `https://your-app-name.streamlit.app`
