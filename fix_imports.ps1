# ==========================================
# ACTIVADOR RÁPIDO DEL CORRECTOR DE IMPORTS
# ==========================================

Write-Host ""
Write-Host "🎯===============================================🎯" -ForegroundColor Cyan
Write-Host "🚀     CORRECTOR DE IMPORTS NO UTILIZADOS     🚀" -ForegroundColor Yellow  
Write-Host "🎯===============================================🎯" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del script
Set-Location $PSScriptRoot

# Verificar que Python está disponible
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python disponible: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python no está disponible en el PATH" -ForegroundColor Red
    Write-Host "   Por favor instala Python o agrégalo al PATH" -ForegroundColor Red
    Read-Host "Presiona Enter para continuar"
    exit 1
}

Write-Host "📁 Directorio actual: $(Get-Location)" -ForegroundColor Blue
Write-Host ""

# Ejecutar el activador
try {
    python scripts\activate_import_fixer.py
} catch {
    Write-Host "❌ Error ejecutando el corrector: $_" -ForegroundColor Red
}

Read-Host "Presiona Enter para continuar"
