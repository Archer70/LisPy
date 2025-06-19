@echo off
REM
REM LisPy Pre-Commit Hook (Windows)
REM 
REM This hook automatically updates the test count in README.md before each commit.
REM To install this hook, run: git config core.hooksPath .githooks
REM

echo Pre-commit: Updating test count in README.md...

REM Run the test count update script
python bin/update_test_count.py

REM Check if the script succeeded
if %ERRORLEVEL% neq 0 (
    echo Failed to update test count
    exit /b 1
)

REM If README.md was modified, add it to the commit
git diff --name-only | findstr "README.md" >nul
if %ERRORLEVEL% equ 0 (
    echo Adding updated README.md to commit
    git add README.md
)

echo Pre-commit checks completed successfully
exit /b 0 