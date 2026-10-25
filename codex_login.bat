@echo off
setlocal
cd /d "%~dp0"
where npm >nul 2>nul || (echo npm not found. Install Node.js LTS from https://nodejs.org, open a new terminal and run this again. & pause & exit /b 1)
where codex >nul 2>nul || (echo installing the OpenAI Codex CLI ... & call npm i -g @openai/codex || (echo install failed & pause & exit /b 1))
echo A browser window will open: sign in with YOUR ChatGPT account.
call codex login
echo.
echo done. Now run check_backend.bat and confirm the codex line says ok.
pause
