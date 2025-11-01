@echo off
chcp 65001 >nul
REM Script cài đặt tự động AI Trading Application cho Windows

echo ============================================================
echo  🚀 CAI DAT TU DONG - AI TRADING APPLICATION
echo ============================================================
echo.

REM Kiểm tra Python
echo [1/5] Kiem tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ KHONG TIM THAY PYTHON!
    echo.
    echo Vui long cai dat Python 3.8+ truoc:
    echo https://www.python.org/downloads/
    echo.
    echo Nho chon "Add Python to PATH" khi cai dat!
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Tim thay Python %PYTHON_VERSION%
echo.

REM Di chuyen den thu muc project
cd /d "%~dp0"
echo [2/5] Thu muc project: %CD%
echo.

REM Tao virtual environment
echo [3/5] Tao virtual environment...
if exist "venv" (
    echo ⚠️  Virtual environment da ton tai, bo qua...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Loi khi tao virtual environment!
        pause
        exit /b 1
    )
    echo ✅ Da tao virtual environment thanh cong
)
echo.

REM Kich hoat virtual environment
echo [4/5] Kich hoat virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Loi khi kich hoat virtual environment!
    pause
    exit /b 1
)
echo ✅ Da kich hoat virtual environment
echo.

REM Cai dat dependencies
echo [5/5] Cai dat dependencies (co the mat 2-5 phut)...
echo.
pip install --upgrade pip --quiet
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ Loi khi cai dat dependencies!
    echo Vui long kiem tra file requirements.txt
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  ✅ CAI DAT HOAN TAT!
echo ============================================================
echo.
echo De chay ung dung, su dung mot trong cac cach sau:
echo.
echo   1. Double-click vao file "run.bat"
echo   2. Hoac chay lenh: run.bat
echo   3. Hoac chay lenh: streamlit run app.py
echo.
echo Ung dung se mo tai: http://localhost:8501
echo.
pause

