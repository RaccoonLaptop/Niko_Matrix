@echo off
echo ========================================
echo   Build Niko_Matrix to .exe
echo ========================================
echo.

if not exist "venv" (
    echo Creating virtual environment...
    py -m venv venv
)

echo Activating and installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt -q

echo.
echo Creating icon from Niko_Matrix.png...
py create_icon.py

echo.
echo Converting CDPI icon (if needed)...
py convert_cdpi_icon.py

echo.
echo Building .exe (1-2 minutes)...
pyinstaller Niko_Matrix.spec --clean

echo.
if exist "dist\Niko_Matrix.exe" (
    echo ========================================
    echo   Done! File: dist\Niko_Matrix.exe
    echo ========================================
    explorer dist
) else (
    echo Build failed. Check if Python is installed.
    pause
)
