@echo off
REM Script khởi chạy ứng dụng AI Trading cho Windows

echo 🚀 Đang khởi chạy AI Trading...
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Không tìm thấy Python. Vui lòng cài đặt Python 3.8 trở lên.
    pause
    exit /b 1
)

REM Cài đặt dependencies
echo 📦 Đang kiểm tra dependencies...
pip install -q -r requirements.txt

REM Chạy ứng dụng
echo ✅ Khởi động ứng dụng...
echo.
streamlit run app.py

pause

