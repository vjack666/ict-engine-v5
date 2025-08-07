# ICT Engine v5.0 - Auto Start PowerShell
# =====================================
# Inicia automáticamente el dashboard

Write-Host ""
Write-Host "🚀 ICT ENGINE v5.0 - INICIO AUTOMÁTICO" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

# Cambiar al directorio del proyecto
Set-Location "c:\Users\v_jac\Desktop\itc engine v5.0"

Write-Host "📊 Iniciando sistema con datos REALES..." -ForegroundColor Cyan

try {
    # Ejecutar auto-start
    python auto_start.py

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ ICT Engine finalizado correctamente" -ForegroundColor Green
    } else {
        Write-Host "⚠️ ICT Engine finalizado con código: $LASTEXITCODE" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error ejecutando ICT Engine: $_" -ForegroundColor Red
    Write-Host "Presiona cualquier tecla para continuar..."
    $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
