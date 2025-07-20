@echo off
REM LisPy Test Suite Runner
REM Usage: scripts\test

cd /d "%~dp0.."
python -m unittest discover -s tests -p "*_test.py"
exit /b %ERRORLEVEL% 