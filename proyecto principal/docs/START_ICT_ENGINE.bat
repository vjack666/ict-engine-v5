@echo off
REM ICT Engine v5.0 - Auto Start Batch
REM ===================================
REM Inicia automáticamente el dashboard sin menús

echo.
echo 🚀 ICT ENGINE v5.0 - INICIO AUTOMÁTICO
echo ======================================
echo.

REM Cambiar al directorio del proyecto
cd /d "c:\Users\v_jac\Desktop\itc engine v5.0"

REM Ejecutar auto-start
echo 📊 Iniciando sistema con datos REALES...
python auto_start.py

REM Pausa para ver mensajes si hay error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Error detectado. Presiona cualquier tecla para continuar...
    pause > nul
)
