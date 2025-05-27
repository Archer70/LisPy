@echo off
REM LisPy Interpreter Launcher
REM Usage: bin\lispy [--repl] [file.lpy]

python "%~dp0lispy_interpreter.py" %*
exit /b %ERRORLEVEL% 