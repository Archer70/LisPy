@echo off
REM LisPy Code Formatter and Linter
REM Usage: scripts\format

cd /d "%~dp0.."

echo Installing dev requirements...
pip install -r requirements-dev.txt

echo Formatting code with Black...
python -m black lispy/ tests/ scripts/ bin/

echo Sorting imports with isort...
python -m isort lispy/ tests/ scripts/ bin/

echo Running Flake8 linter...
python -m flake8 lispy/ tests/ scripts/ bin/

echo ✅ Code formatting and linting complete!
exit /b %ERRORLEVEL% 