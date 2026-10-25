@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (echo run setup.bat first & pause & exit /b 1)
call ".venv\Scripts\activate.bat"
set "PMPREDICT_LANG=en"
set "PYTHONIOENCODING=utf-8"
rem Optional overrides (remove "rem " to activate):
rem set "PMPREDICT_PROVIDER=codex"
rem set "PMPREDICT_CODEX_MODEL=gpt-5"
rem set "PMPREDICT_OPENAI_MODEL=gpt-5-mini"
echo starting pmpredict at http://localhost:8501  (close this window to stop)
python -m streamlit run app/streamlit_app.py --server.port 8501 --browser.gatherUsageStats false
pause
