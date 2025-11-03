# Sử dụng Python 3.13 slim image để giảm kích thước
FROM python:3.13-slim

# Thiết lập working directory
WORKDIR /app

# Cài đặt các dependencies hệ thống
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements trước để tận dụng Docker cache layer
COPY requirements.txt .

# Cài đặt Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Tạo thư mục data_cache nếu chưa có
RUN mkdir -p /app/data_cache

# Expose port Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8501/_stcore/health')"

# Chạy Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]

