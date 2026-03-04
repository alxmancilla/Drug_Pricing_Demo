@echo off
REM Drug Pricing Assistant - Streamlit Quick Start Script (Windows)

echo ======================================================================
echo 💊 Drug Pricing Assistant - Streamlit UI
echo ======================================================================
echo.

REM Check if .env file exists
if not exist .env (
    echo ❌ Error: .env file not found
    echo    Please create a .env file with your API keys and MongoDB URI
    echo    See .env.example for reference
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo 📥 Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo ❌ Error: Streamlit installation failed
    echo    Try manually: pip install streamlit
    pause
    exit /b 1
)

echo.
echo ✅ All dependencies installed
echo.
echo ======================================================================
echo 🚀 Starting Streamlit App...
echo ======================================================================
echo.
echo The app will open in your browser at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run Streamlit app
streamlit run streamlit_app.py

pause

