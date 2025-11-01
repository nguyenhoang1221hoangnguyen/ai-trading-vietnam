#!/bin/bash

# Script khởi chạy ứng dụng AI Trading

echo "🚀 Đang khởi chạy AI Trading..."
echo ""

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Không tìm thấy Python 3. Vui lòng cài đặt Python 3.8 trở lên."
    exit 1
fi

# Kiểm tra requirements
if [ ! -f "requirements.txt" ]; then
    echo "❌ Không tìm thấy file requirements.txt"
    exit 1
fi

# Cài đặt dependencies nếu cần
echo "📦 Đang kiểm tra dependencies..."
pip3 install -q -r requirements.txt

# Chạy ứng dụng
echo "✅ Khởi động ứng dụng..."
echo ""
streamlit run app.py

