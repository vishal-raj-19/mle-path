@echo off
REM Windows: double-click this file
cd /d "%~dp0"
where py >nul 2>nul && (py server.py) || (python server.py)
pause
