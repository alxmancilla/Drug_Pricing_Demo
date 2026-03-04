@echo off
REM Drug Pricing AI Agent - Launcher Script (Windows)

:menu
echo.
echo ========================================
echo   Drug Pricing AI Agent Launcher
echo ========================================
echo.
echo Select an option:
echo   1) Run CLI Agent (Interactive)
echo   2) Run Streamlit Web UI
echo   3) Run Tests (All)
echo   4) Run Specific Test
echo   5) Install Dependencies
echo   6) Setup Database
echo   7) Exit
echo.
set /p choice="Enter choice [1-7]: "

if "%choice%"=="1" goto cli
if "%choice%"=="2" goto streamlit
if "%choice%"=="3" goto tests
if "%choice%"=="4" goto specific_test
if "%choice%"=="5" goto install
if "%choice%"=="6" goto setup
if "%choice%"=="7" goto exit
goto invalid

:cli
echo.
echo Starting CLI Agent...
echo.
python agent_app.py
goto end

:streamlit
echo.
echo Starting Streamlit Web UI...
echo Opening browser at http://localhost:8501
echo.
streamlit run agent_streamlit_app.py
goto end

:tests
echo.
echo Running All Tests...
echo.
python test_agent.py
goto end

:specific_test
echo.
echo Select test:
echo   1) Basic Search
echo   2) Preference Saving
echo   3) Search History
echo   4) Conversation Context
echo   5) Personalized Recommendations
echo.
set /p test_num="Enter test number [1-5]: "
python test_agent.py %test_num%
goto end

:install
echo.
echo Installing Dependencies...
echo.
pip install -r requirements.txt
echo.
echo Dependencies installed!
goto end

:setup
echo.
echo Setting up Database...
echo.
python setup_database.py
echo.
echo Database setup complete!
goto end

:invalid
echo.
echo Invalid choice. Please run again and select 1-7.
goto end

:exit
echo.
echo Goodbye!
exit /b 0

:end
pause

