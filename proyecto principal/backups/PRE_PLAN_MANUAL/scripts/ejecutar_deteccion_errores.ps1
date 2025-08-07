#!/usr/bin/env pwsh
<#
🔍 ITC ENGINE v5.0 - EJECUTOR SISTEMA DETECCIÓN DE ERRORES JERÁRQUICO
=====================================================================

🎯 OBJETIVO: Script automatizado para ejecutar el Sistema de Detección de Errores
            con diferentes modos y opciones de configuración

📊 CARACTERÍSTICAS:
   - ✅ Modo rápido y completo
   - ✅ Integración con dashboard
   - ✅ Generación automática de reportes
   - ✅ Configuración flexible
   - ✅ Logging detallado

🚀 USO:
   .\scripts\ejecutar_deteccion_errores.ps1 [opciones]

   Opciones:
   -Quick         : Análisis rápido (solo archivos críticos)
   -Dashboard     : Modo integración dashboard
   -Output <path> : Archivo de salida personalizado
   -Verbose       : Modo verboso
   -Help          : Mostrar ayuda

📅 Fecha: 2025-08-06 | Versión: 1.0.0
👤 Autor: ITC Engine v5.0 System
#>

param(
    [switch]$Quick,
    [switch]$Dashboard,
    [string]$Output = "",
    [switch]$Verbose,
    [switch]$Help
)

# ===================================================================
# 🎨 CONFIGURACIÓN Y VARIABLES GLOBALES
# ===================================================================

$ErrorActionPreference = "Stop"
$VerbosePreference = if ($Verbose) { "Continue" } else { "SilentlyContinue" }

# Colores para output
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"
$ColorInfo = "Cyan"
$ColorHeader = "Magenta"

# Rutas importantes
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkspaceRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$ErrorDetectorScript = Join-Path $ScriptDir "error_detection\error_detector.py"
$LogsDir = Join-Path $WorkspaceRoot "data\logs"
$ExportsDir = Join-Path $WorkspaceRoot "data\exports"

# Configuración de timestamps
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = Join-Path $LogsDir "deteccion_errores_$Timestamp.log"

# ===================================================================
# 🛠️ FUNCIONES AUXILIARES
# ===================================================================

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White",
        [string]$Prefix = ""
    )

    $FullMessage = if ($Prefix) { "[$Prefix] $Message" } else { $Message }
    Write-Host $FullMessage -ForegroundColor $Color

    # También escribir al log
    if (Test-Path $LogsDir) {
        "$((Get-Date).ToString('yyyy-MM-dd HH:mm:ss')) - $FullMessage" | Add-Content $LogFile
    }
}

function Show-Header {
    Write-Host ""
    Write-ColorOutput "🔍 ITC ENGINE v5.0 - SISTEMA DETECCIÓN DE ERRORES JERÁRQUICO" $ColorHeader
    Write-ColorOutput "=================================================================" $ColorHeader
    Write-ColorOutput "🚀 Iniciando análisis automático del sistema..." $ColorInfo
    Write-ColorOutput "📅 Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" $ColorInfo
    Write-Host ""
}

function Show-Help {
    Write-Host ""
    Write-ColorOutput "🔍 SISTEMA DE DETECCIÓN DE ERRORES JERÁRQUICO - AYUDA" $ColorHeader
    Write-ColorOutput "======================================================" $ColorHeader
    Write-Host ""
    Write-ColorOutput "USO:" $ColorInfo
    Write-ColorOutput "  .\scripts\ejecutar_deteccion_errores.ps1 [opciones]" "White"
    Write-Host ""
    Write-ColorOutput "OPCIONES:" $ColorInfo
    Write-ColorOutput "  -Quick         Análisis rápido (solo archivos críticos)" "White"
    Write-ColorOutput "  -Dashboard     Modo integración con dashboard" "White"
    Write-ColorOutput "  -Output <path> Archivo de salida personalizado" "White"
    Write-ColorOutput "  -Verbose       Modo verboso con detalles" "White"
    Write-ColorOutput "  -Help          Mostrar esta ayuda" "White"
    Write-Host ""
    Write-ColorOutput "EJEMPLOS:" $ColorInfo
    Write-ColorOutput "  .\scripts\ejecutar_deteccion_errores.ps1 -Quick" "White"
    Write-ColorOutput "  .\scripts\ejecutar_deteccion_errores.ps1 -Dashboard -Verbose" "White"
    Write-ColorOutput "  .\scripts\ejecutar_deteccion_errores.ps1 -Output 'mi_reporte.json'" "White"
    Write-Host ""
    exit 0
}

function Test-Prerequisites {
    Write-ColorOutput "🔍 Verificando prerequisitos..." $ColorInfo

    # Verificar Python
    try {
        $PythonVersion = & python --version 2>&1
        Write-ColorOutput "✅ Python detectado: $PythonVersion" $ColorSuccess
    }
    catch {
        Write-ColorOutput "❌ ERROR: Python no encontrado en PATH" $ColorError
        Write-ColorOutput "💡 Instale Python o verifique la configuración del PATH" $ColorWarning
        exit 1
    }

    # Verificar script detector
    if (-not (Test-Path $ErrorDetectorScript)) {
        Write-ColorOutput "❌ ERROR: Script detector no encontrado" $ColorError
        Write-ColorOutput "📍 Ruta esperada: $ErrorDetectorScript" $ColorWarning
        exit 1
    }

    Write-ColorOutput "✅ Script detector encontrado" $ColorSuccess

    # Verificar/crear directorios
    $DirsToCheck = @($LogsDir, $ExportsDir)
    foreach ($Dir in $DirsToCheck) {
        if (-not (Test-Path $Dir)) {
            New-Item -ItemType Directory -Path $Dir -Force | Out-Null
            Write-ColorOutput "📁 Directorio creado: $Dir" $ColorInfo
        }
    }

    Write-ColorOutput "✅ Prerequisitos verificados correctamente" $ColorSuccess
}

function Install-PythonDependencies {
    Write-ColorOutput "📦 Verificando dependencias Python..." $ColorInfo

    # Lista de dependencias requeridas
    $RequiredPackages = @("rich")

    foreach ($Package in $RequiredPackages) {
        try {
            & python -c "import $Package" 2>$null
            Write-ColorOutput "✅ Dependencia OK: $Package" $ColorSuccess
        }
        catch {
            Write-ColorOutput "📦 Instalando dependencia: $Package" $ColorWarning
            try {
                & python -m pip install $Package --quiet
                Write-ColorOutput "✅ Dependencia instalada: $Package" $ColorSuccess
            }
            catch {
                Write-ColorOutput "⚠️ No se pudo instalar $Package (continuando sin Rich UI)" $ColorWarning
            }
        }
    }
}

function Invoke-ErrorDetection {
    param(
        [bool]$QuickMode = $false,
        [string]$OutputFile = ""
    )

    Write-ColorOutput "🚀 Ejecutando sistema de detección de errores..." $ColorInfo

    # Construir argumentos
    $Arguments = @()
    $Arguments += "--workspace"
    $Arguments += "`"$WorkspaceRoot`""

    if ($QuickMode) {
        $Arguments += "--quick"
        Write-ColorOutput "⚡ Modo rápido activado" $ColorInfo
    }

    if ($OutputFile) {
        $Arguments += "--output"
        $Arguments += "`"$OutputFile`""
        Write-ColorOutput "📁 Salida: $OutputFile" $ColorInfo
    }

    Write-ColorOutput "🔧 Comando: python `"$ErrorDetectorScript`" $($Arguments -join ' ')" $ColorInfo

    # Ejecutar detector
    try {
        $StartTime = Get-Date

        if ($Verbose) {
            & python $ErrorDetectorScript @Arguments
        } else {
            $DetectionOutput = & python $ErrorDetectorScript @Arguments 2>&1
        }

        $EndTime = Get-Date
        $Duration = ($EndTime - $StartTime).TotalSeconds

        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Análisis completado exitosamente" $ColorSuccess
            Write-ColorOutput "⏱️ Tiempo de ejecución: $([math]::Round($Duration, 2)) segundos" $ColorInfo
        } elseif ($LASTEXITCODE -eq 1) {
            Write-ColorOutput "⚠️ Análisis completado con problemas críticos detectados" $ColorWarning
            Write-ColorOutput "🚨 Revisar inmediatamente los errores críticos" $ColorError
        } else {
            throw "Error en la ejecución del detector (código: $LASTEXITCODE)"
        }

        if (-not $Verbose -and $DetectionOutput) {
            Write-ColorOutput "📋 Salida del detector:" $ColorInfo
            $DetectionOutput | ForEach-Object { Write-ColorOutput "   $_" "White" }
        }

        return $LASTEXITCODE

    }
    catch {
        Write-ColorOutput "❌ ERROR ejecutando detector: $($_.Exception.Message)" $ColorError
        return 2
    }
}

function Show-Summary {
    param(
        [int]$ExitCode,
        [string]$OutputFile = ""
    )

    Write-Host ""
    Write-ColorOutput "📊 RESUMEN DE EJECUCIÓN" $ColorHeader
    Write-ColorOutput "========================" $ColorHeader

    # Estado del análisis
    switch ($ExitCode) {
        0 {
            Write-ColorOutput "✅ Estado: Análisis completado sin problemas críticos" $ColorSuccess
        }
        1 {
            Write-ColorOutput "⚠️ Estado: Problemas críticos detectados - REVISAR URGENTE" $ColorWarning
        }
        default {
            Write-ColorOutput "❌ Estado: Error en la ejecución" $ColorError
        }
    }

    # Archivos generados
    Write-ColorOutput "📁 Archivos generados:" $ColorInfo
    Write-ColorOutput "   📄 Log de ejecución: $LogFile" "White"

    if ($OutputFile -and (Test-Path $OutputFile)) {
        Write-ColorOutput "   📊 Reporte JSON: $OutputFile" "White"
    }

    # Bitácoras automáticas
    $DiagnosticsDir = Join-Path $WorkspaceRoot "docs\bitacoras\diagnosticos"
    if (Test-Path $DiagnosticsDir) {
        $LatestDiagnostic = Get-ChildItem $DiagnosticsDir -Filter "deteccion_errores_*.json" |
                           Sort-Object LastWriteTime -Descending |
                           Select-Object -First 1

        if ($LatestDiagnostic) {
            Write-ColorOutput "   🔍 Bitácora diagnóstica: $($LatestDiagnostic.FullName)" "White"
        }
    }

    Write-Host ""

    # Recomendaciones
    if ($ExitCode -eq 1) {
        Write-ColorOutput "💡 RECOMENDACIONES:" $ColorWarning
        Write-ColorOutput "   🚨 Revisar problemas críticos inmediatamente" "White"
        Write-ColorOutput "   📊 Abrir dashboard para análisis detallado" "White"
        Write-ColorOutput "   🔧 Corregir errores antes de ejecutar en producción" "White"
    } elseif ($ExitCode -eq 0) {
        Write-ColorOutput "💡 RECOMENDACIONES:" $ColorInfo
        Write-ColorOutput "   ✨ Sistema en buen estado" "White"
        Write-ColorOutput "   📈 Considerar ejecutar análisis completo periódicamente" "White"
        Write-ColorOutput "   🔍 Revisar problemas menores cuando sea posible" "White"
    }

    Write-Host ""
}

function Open-DashboardIntegration {
    Write-ColorOutput "🎨 Iniciando integración con dashboard..." $ColorInfo

    # Buscar archivo del dashboard
    $DashboardScript = Join-Path $WorkspaceRoot "dashboard\dashboard_definitivo.py"

    if (Test-Path $DashboardScript) {
        Write-ColorOutput "📊 Ejecutando dashboard con pestaña de problemas..." $ColorInfo
        try {
            # Ejecutar dashboard en background
            Start-Process -FilePath "python" -ArgumentList "`"$DashboardScript`"" -NoNewWindow
            Write-ColorOutput "✅ Dashboard iniciado exitosamente" $ColorSuccess
            Write-ColorOutput "🎯 Buscar pestaña '🚨 Problemas' en el dashboard" $ColorInfo
        }
        catch {
            Write-ColorOutput "⚠️ No se pudo iniciar dashboard automáticamente" $ColorWarning
            Write-ColorOutput "💡 Ejecute manualmente: python `"$DashboardScript`"" $ColorInfo
        }
    } else {
        Write-ColorOutput "⚠️ Dashboard no encontrado en: $DashboardScript" $ColorWarning
    }
}

# ===================================================================
# 🚀 FUNCIÓN PRINCIPAL
# ===================================================================

function Main {
    # Mostrar ayuda si se solicita
    if ($Help) {
        Show-Help
    }

    # Mostrar header
    Show-Header

    # Verificar prerequisitos
    Test-Prerequisites

    # Instalar dependencias
    Install-PythonDependencies

    # Configurar archivo de salida
    $FinalOutput = if ($Output) {
        if ([System.IO.Path]::IsPathRooted($Output)) { $Output }
        else { Join-Path $ExportsDir $Output }
    } else {
        Join-Path $ExportsDir "deteccion_errores_$Timestamp.json"
    }

    # Ejecutar detección
    $ExitCode = Invoke-ErrorDetection -QuickMode:$Quick -OutputFile $FinalOutput

    # Mostrar resumen
    Show-Summary -ExitCode $ExitCode -OutputFile $FinalOutput

    # Integración con dashboard si se solicita
    if ($Dashboard) {
        Open-DashboardIntegration
    }

    Write-ColorOutput "🎯 Ejecución completada" $ColorHeader
    return $ExitCode
}

# ===================================================================
# 🎬 EJECUCIÓN
# ===================================================================

try {
    $FinalExitCode = Main
    exit $FinalExitCode
}
catch {
    Write-ColorOutput "💥 ERROR FATAL: $($_.Exception.Message)" $ColorError
    Write-ColorOutput "📍 En línea: $($_.InvocationInfo.ScriptLineNumber)" $ColorError

    if ($_.Exception.StackTrace) {
        Write-ColorOutput "📋 Stack trace:" $ColorInfo
        $_.Exception.StackTrace -split "`n" | ForEach-Object {
            Write-ColorOutput "   $_" "Gray"
        }
    }

    exit 99
}
