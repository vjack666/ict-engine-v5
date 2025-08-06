@echo off
REM ==========================================
REM ACTIVADOR RÁPIDO DEL CORRECTOR DE IMPORTS
REM ==========================================

echo.
echo 🎯===============================================🎯
echo 🚀     CORRECTOR DE IMPORTS NO UTILIZADOS     🚀  
echo 🎯===============================================🎯
echo.

cd /d "%~dp0"

REM Verificar que Python está disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está disponible en el PATH
    echo    Por favor instala Python o agrégalo al PATH
    pause
    exit /b 1
)

echo 📁 Directorio actual: %CD%
echo.

REM Ejecutar el activador
python scripts\activate_import_fixer.py

pause
