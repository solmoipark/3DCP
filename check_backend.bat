@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (echo run setup.bat first & pause & exit /b 1)
call ".venv\Scripts\activate.bat"
set "PMPREDICT_LANG=en"
set "PYTHONIOENCODING=utf-8"
python -m pmpredict.cli agent --check
echo.
echo "ok" lines are usable backends; "chosen" is the one the app will start with.
pause
