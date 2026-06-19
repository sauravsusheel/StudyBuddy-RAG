@echo off
echo ============================================
echo   StudyBuddy RAG - Starting...
echo ============================================
echo.

if not exist "venv" (
    echo Creating virtual environment...
    python3.14 -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install flask==3.1.0 flask-cors==5.0.0 werkzeug==3.1.3 pypdf==5.4.0 openai==1.82.0 numpy python-dotenv==1.1.0
) else (
    call venv\Scripts\activate.bat
)

echo.
echo ============================================
echo   Open http://localhost:5000 in your browser
echo ============================================
echo.

python app.py
