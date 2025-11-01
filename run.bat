@echo off
chcp 65001 >nul
REM Script khởi chạy ứng dụng AI Trading cho Windows

echo 🚀 Đang khởi chạy AI Trading...
echo.

REM Di chuyển đến thư mục project
cd /d "%~dp0"

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Không tìm thấy Python. Vui lòng cài đặt Python 3.8 trở lên.
    echo.
    echo Hoặc chạy setup.bat để cài đặt tự động.
    pause
    exit /b 1
)

REM Kiểm tra virtual environment
if exist "venv\Scripts\activate.bat" (
    echo 📦 Đang kích hoạt virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Virtual environment chưa được tạo!
    echo.
    echo Vui lòng chạy setup.bat trước để cài đặt ứng dụng.
    pause
    exit /b 1
)

REM Chạy ứng dụng
echo ✅ Khởi động ứng dụng...
echo.
echo 🌐 Ứng dụng sẽ mở tại: http://localhost:8501
echo.
streamlit run app.py

pause

