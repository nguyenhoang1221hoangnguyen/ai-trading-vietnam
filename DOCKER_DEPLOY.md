# 🐳 Hướng dẫn Deploy với Docker Compose

## 📋 Tổng quan

Ứng dụng AI Trading đã được đóng gói sẵn với Docker và Docker Compose, giúp việc triển khai trở nên đơn giản và nhất quán trên mọi môi trường.

## 🚀 Yêu cầu hệ thống

- **Docker Desktop** (Windows/macOS) hoặc **Docker Engine + Docker Compose** (Linux)
- Tối thiểu 2GB RAM
- 5GB dung lượng ổ cứng trống

## 📦 Cài đặt Docker

### Windows/macOS
1. Tải Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Cài đặt và khởi động Docker Desktop
3. Đảm bảo Docker Desktop đang chạy (icon Docker xuất hiện trong system tray)

### Linux (Ubuntu/Debian)
```bash
# Cài đặt Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Cài đặt Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

## 🎯 Cách sử dụng

### 1. Build và chạy ứng dụng

```bash
# Từ thư mục dự án
docker-compose up -d
```

Lệnh này sẽ:
- ✅ Build Docker image từ Dockerfile
- ✅ Tạo và khởi chạy container
- ✅ Mount volume cho database cache (persist data)
- ✅ Expose port 8501 cho Streamlit

### 2. Truy cập ứng dụng

Mở trình duyệt và truy cập:
- **Local:** http://localhost:8501
- **Network:** http://[IP_CỦA_MÁY]:8501

### 3. Xem logs

```bash
# Xem logs real-time
docker-compose logs -f

# Xem logs của service cụ thể
docker-compose logs -f ai-trading
```

### 4. Dừng ứng dụng

```bash
# Dừng container
docker-compose down

# Dừng và xóa volumes (xóa cache database)
docker-compose down -v
```

### 5. Khởi động lại

```bash
# Khởi động lại container
docker-compose restart

# Hoặc stop và start lại
docker-compose stop
docker-compose start
```

### 6. Rebuild sau khi thay đổi code

```bash
# Rebuild image và restart
docker-compose up -d --build

# Hoặc rebuild không cache
docker-compose build --no-cache
docker-compose up -d
```

## 📊 Quản lý Container

### Kiểm tra trạng thái
```bash
# Xem trạng thái các services
docker-compose ps

# Xem thông tin chi tiết
docker-compose ps -a
```

### Vào bên trong container
```bash
# Execute command trong container
docker-compose exec ai-trading bash

# Hoặc
docker exec -it ai-trading-app bash
```

### Xem resource usage
```bash
docker stats ai-trading-app
```

## 💾 Quản lý dữ liệu

### Database Cache

Database cache được lưu trong thư mục `./data_cache/` trên host và được mount vào container. Dữ liệu sẽ được persist giữa các lần restart.

```bash
# Backup database
cp -r ./data_cache/stock_data.db ./data_cache/stock_data.db.backup

# Restore database
cp ./data_cache/stock_data.db.backup ./data_cache/stock_data.db
docker-compose restart
```

### Volumes

Volumes được định nghĩa trong `docker-compose.yml`:
- `./data_cache:/app/data_cache` - Database cache

## 🔧 Tùy chỉnh

### Thay đổi port

Sửa file `docker-compose.yml`:

```yaml
ports:
  - "8502:8501"  # Thay đổi port host từ 8501 sang 8502
```

Sau đó restart:
```bash
docker-compose up -d
```

### Thêm environment variables

Sửa file `docker-compose.yml`:

```yaml
environment:
  - PYTHONUNBUFFERED=1
  - STREAMLIT_SERVER_PORT=8501
  - CUSTOM_VAR=value
```

### Sửa Dockerfile

Nếu cần cài thêm dependencies hoặc thay đổi cấu hình, sửa file `Dockerfile` và rebuild:

```bash
docker-compose build --no-cache
docker-compose up -d
```

## 🐛 Xử lý lỗi

### Lỗi: Port đã được sử dụng

**Giải pháp 1:** Dừng ứng dụng đang chạy ở port 8501
```bash
# Tìm process đang dùng port
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows

# Kill process
kill -9 [PID]  # macOS/Linux
taskkill /PID [PID] /F  # Windows
```

**Giải pháp 2:** Đổi port trong docker-compose.yml

### Lỗi: Permission denied (Linux)

```bash
# Thêm user vào docker group
sudo usermod -aG docker $USER
# Logout và login lại
```

### Lỗi: Out of memory

Tăng RAM cho Docker Desktop:
1. Mở Docker Desktop → Settings → Resources
2. Tăng Memory limit (khuyến nghị: 4GB+)

### Lỗi: Build failed

```bash
# Xóa cache và rebuild
docker-compose build --no-cache

# Hoặc xóa image cũ
docker rmi ai-trading-app
docker-compose build
```

## 🚀 Production Deployment

### Với Docker Compose Desktop

1. **Tối ưu Dockerfile:**
   - Sử dụng multi-stage build
   - Minimize image size
   - Thêm health checks

2. **Cấu hình nginx reverse proxy** (tùy chọn):
   ```yaml
   # Thêm service nginx vào docker-compose.yml
   nginx:
     image: nginx:alpine
     ports:
       - "80:80"
     volumes:
       - ./nginx.conf:/etc/nginx/nginx.conf
     depends_on:
       - ai-trading
   ```

3. **SSL/TLS với Let's Encrypt** (cho production):
   - Sử dụng certbot hoặc traefik
   - Cấu hình HTTPS

4. **Monitoring:**
   ```yaml
   # Thêm Prometheus/Grafana (tùy chọn)
   ```

## 📝 Best Practices

1. **Regular backups:**
   ```bash
   # Tạo script backup tự động
   #!/bin/bash
   docker-compose exec ai-trading cp /app/data_cache/stock_data.db /app/data_cache/backup_$(date +%Y%m%d).db
   ```

2. **Update dependencies:**
   ```bash
   # Cập nhật requirements.txt
   docker-compose exec ai-trading pip install -r requirements.txt --upgrade
   docker-compose restart
   ```

3. **Log rotation:**
   ```yaml
   # Thêm vào docker-compose.yml
   logging:
     driver: "json-file"
     options:
       max-size: "10m"
       max-file: "3"
   ```

4. **Health checks:**
   - Đã được cấu hình sẵn trong Dockerfile và docker-compose.yml

## 🎓 Tài liệu tham khảo

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)

## ✅ Checklist Deploy

- [ ] Đã cài đặt Docker Desktop/Engine
- [ ] Đã clone repository
- [ ] Đã kiểm tra file Dockerfile và docker-compose.yml
- [ ] Đã chạy `docker-compose up -d`
- [ ] Đã truy cập ứng dụng tại http://localhost:8501
- [ ] Đã kiểm tra logs không có lỗi
- [ ] Đã test các chức năng chính của ứng dụng

---

**🎉 Chúc bạn deploy thành công!**

*Nếu gặp vấn đề, hãy kiểm tra logs bằng `docker-compose logs -f`*

