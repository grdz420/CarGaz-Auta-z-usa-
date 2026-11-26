@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel% equ 0 (
  py -3 server.py --open
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo Zainstaluj Python 3 z python.org i uruchom ponownie.
    pause
    exit /b 1
  )
  python server.py --open
)
pause
