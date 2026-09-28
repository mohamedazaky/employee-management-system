@echo off
cd /d "%~dp0"
echo Installing requirements (first run only takes a minute)...
python -m pip install -r requirements.txt --quiet
echo Opening the dashboard in your browser...
python -m streamlit run app.py
pause
