@echo off
cd /d "%~dp0"
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)
call .venv\Scripts\activate.bat
pip install -r requirements.txt -q
echo.
echo Starting server at http://127.0.0.1:8000
echo Open http://127.0.0.1:8000/docs in your browser
echo Press Ctrl+C to stop
echo.
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
pause
