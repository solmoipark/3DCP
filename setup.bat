@echo off
setlocal
cd /d "%~dp0"
echo === pmpredict setup ===
where py >nul 2>nul && (set "PY=py -3") || (set "PY=python")
%PY% --version 2>nul || (echo Python not found. Install Python 3.12 from python.org and tick "Add python.exe to PATH". & pause & exit /b 1)
if not exist ".venv\Scripts\python.exe" (
  echo creating virtual environment .venv ...
  %PY% -m venv .venv || (echo venv creation failed & pause & exit /b 1)
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip wheel >nul
echo installing runtime packages (a few minutes) ...
pip install -r requirements.txt || (echo pip install failed & pause & exit /b 1)
echo installing agent packages ...
pip install -e ".[agent]" || (echo agent install failed & pause & exit /b 1)
echo.
echo setup finished.
echo Next: codex_login.bat (ChatGPT subscription) or secrets.json (API key), then check_backend.bat and start_app.bat
pause
