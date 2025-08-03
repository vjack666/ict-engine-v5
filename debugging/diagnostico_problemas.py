#!/usr/bin/env python3
"""
🔍 DIAGNÓSTICO DE PROBLEMAS - CAJA NEGRA
=========================================
Analiza y soluciona los problemas detectados por el sistema de diagnósticos.
"""

import sys
from datetime import datetime
from pathlib import Path

# Añadir el directorio raíz del proyecto al path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

def main():
    enviar_senal_log("INFO", "🔍 DIAGNÓSTICO DE PROBLEMAS - CAJA NEGRA", "diagnostico_problemas", "migration")
    enviar_senal_log("INFO", "=" * 50, "diagnostico_problemas", "migration")
    enviar_senal_log("INFO", f"📅 Fecha: {datetime.now(, "diagnostico_problemas", "migration").strftime('%Y-%m-%d %H:%M:%S')}")
    enviar_senal_log("INFO", , "diagnostico_problemas", "migration")

    # Verificar archivos principales
    enviar_senal_log("INFO", "📁 VERIFICANDO ARCHIVOS PRINCIPALES:", "diagnostico_problemas", "migration")
    archivos_criticos = [
        "poi_black_box_diagnostics.py",
        "dashboard/dashboard_definitivo.py",
        "core/poi_system/poi_detector.py",
        "core/poi_system/poi_scoring_engine.py",
        "utils/mt5_data_manager.py"
    ]

    archivos_existentes = []
    archivos_faltantes = []

    for archivo in archivos_criticos:
        ruta_completa = Path(archivo)
        if ruta_completa.exists():
            archivos_existentes.append(archivo)
            enviar_senal_log("INFO", f"   ✅ {archivo}", "diagnostico_problemas", "migration")
        else:
            archivos_faltantes.append(archivo)
            enviar_senal_log("INFO", f"   ❌ {archivo} - NO ENCONTRADO", "diagnostico_problemas", "migration")

    enviar_senal_log("INFO", , "diagnostico_problemas", "migration")
    enviar_senal_log("INFO", "🔍 INTENTANDO IMPORTAR SISTEMA DE DIAGNÓSTICOS:", "diagnostico_problemas", "migration")

    try:
        from utils.system_diagnostics import POIBlackBoxDiagnostics
        enviar_senal_log("INFO", "   ✅ Import exitoso - Sistema simplificado cargado", "diagnostico_problemas", "migration")

        # Crear instancia
        diagnostics = POIBlackBoxDiagnostics()
        enviar_senal_log("INFO", "   ✅ Instancia creada", "diagnostico_problemas", "migration")

        # Ejecutar diagnóstico
        enviar_senal_log("INFO", , "diagnostico_problemas", "migration")
        enviar_senal_log("INFO", "🔬 EJECUTANDO DIAGNÓSTICO COMPLETO:", "diagnostico_problemas", "migration")
        resultado = diagnostics.run_full_diagnostic(None)  # Sin dashboard instance por ahora

        enviar_senal_log("INFO", f"   📊 Issues detectados: {len(resultado.get('critical_issues', [], "diagnostico_problemas", "migration"))}")
        enviar_senal_log("INFO", f"   🔧 Soluciones disponibles: {len(resultado.get('solutions', [], "diagnostico_problemas", "migration"))}")

        if resultado.get('critical_issues'):
            enviar_senal_log("INFO", , "diagnostico_problemas", "migration")
            enviar_senal_log("INFO", "🚨 PROBLEMAS DETECTADOS:", "diagnostico_problemas", "migration")
            for i, issue in enumerate(resultado['critical_issues'], 1):
                enviar_senal_log("INFO", f"   {i}. {issue}", "diagnostico_problemas", "migration")

        if resultado.get('solutions'):
            enviar_senal_log("INFO", , "diagnostico_problemas", "migration")
            enviar_senal_log("INFO", "💡 SOLUCIONES PROPUESTAS:", "diagnostico_problemas", "migration")
            for i, solucion in enumerate(resultado['solutions'], 1):
                enviar_senal_log("INFO", f"   {i}. {solucion}", "diagnostico_problemas", "migration")

        # Verificar sistema de logging
        enviar_senal_log("INFO", , "diagnostico_problemas", "migration")
        enviar_senal_log("INFO", "📝 VERIFICANDO SISTEMA DE LOGGING:", "diagnostico_problemas", "migration")
        try:
            from sistema.logging_interface import enviar_senal_log
            enviar_senal_log("DEBUG", "Test de logging desde diagnóstico", __name__, "general")
            enviar_senal_log("INFO", "   ✅ Sistema de logging funcional", "diagnostico_problemas", "migration")
        except Exception as e:
            enviar_senal_log("INFO", f"   ⚠️ Problema con logging: {e}", "diagnostico_problemas", "migration")

        # Verificar importación POI
        enviar_senal_log("INFO", , "diagnostico_problemas", "migration")
        enviar_senal_log("INFO", "🎯 VERIFICANDO SISTEMA POI:", "diagnostico_problemas", "migration")
        try:
            from core.poi_system.poi_detector import POIDetector
            enviar_senal_log("INFO", "   ✅ POI Detector disponible", "diagnostico_problemas", "migration")
        except Exception as e:
            enviar_senal_log("ERROR", f"   ❌ Error POI Detector: {e}", "diagnostico_problemas", "migration")

        try:
            from core.poi_system.poi_scoring_engine import POIScoringEngine
            enviar_senal_log("INFO", "   ✅ POI Scoring Engine disponible", "diagnostico_problemas", "migration")
        except Exception as e:
            enviar_senal_log("ERROR", f"   ❌ Error POI Scoring: {e}", "diagnostico_problemas", "migration")

        # Verificar MT5 Data Manager
        enviar_senal_log("INFO", , "diagnostico_problemas", "migration")
        enviar_senal_log("INFO", "📊 VERIFICANDO MT5 DATA MANAGER:", "diagnostico_problemas", "migration")
        try:
            from utils.mt5_data_manager import MT5DataManager
            enviar_senal_log("INFO", "   ✅ MT5DataManager disponible", "diagnostico_problemas", "migration")
        except Exception as e:
            enviar_senal_log("ERROR", f"   ❌ Error MT5DataManager: {e}", "diagnostico_problemas", "migration")

        enviar_senal_log("INFO", , "diagnostico_problemas", "migration")
        enviar_senal_log("INFO", "✅ DIAGNÓSTICO COMPLETADO", "diagnostico_problemas", "migration")

        return resultado

    except ImportError as e:
        enviar_senal_log("ERROR", f"   ❌ Error de import: {e}", "diagnostico_problemas", "migration")
        enviar_senal_log("INFO", , "diagnostico_problemas", "migration")
        enviar_senal_log("INFO", "🔧 DIAGNÓSTICO DE IMPORTS:", "diagnostico_problemas", "migration")

        # Verificar ruta de poi_black_box_diagnostics
        archivos_poi = list(Path(".").glob("**/poi_black_box_diagnostics.py"))
        if archivos_poi:
            enviar_senal_log("INFO", f"   📁 Archivo encontrado en: {archivos_poi[0]}", "diagnostico_problemas", "migration")
        else:
            enviar_senal_log("INFO", "   ❌ Archivo poi_black_box_diagnostics.py no encontrado", "diagnostico_problemas", "migration")

        return None

    except Exception as e:
        enviar_senal_log("ERROR", f"   ❌ Error inesperado: {e}", "diagnostico_problemas", "migration")
        return None

if __name__ == "__main__":
    resultado = main()

    if resultado:
        enviar_senal_log("INFO", , "diagnostico_problemas", "migration")
        enviar_senal_log("INFO", "🎯 RESUMEN FINAL:", "diagnostico_problemas", "migration")
        enviar_senal_log("INFO", f"   📊 Total de problemas: {len(resultado.get('critical_issues', [], "diagnostico_problemas", "migration"))}")
        enviar_senal_log("INFO", f"   🔧 Total de soluciones: {len(resultado.get('solutions', [], "diagnostico_problemas", "migration"))}")

        if resultado.get('critical_issues'):
            enviar_senal_log("INFO", , "diagnostico_problemas", "migration")
            enviar_senal_log("INFO", "⚠️ ACCIÓN REQUERIDA: Se detectaron problemas que necesitan corrección", "diagnostico_problemas", "migration")
        else:
            enviar_senal_log("INFO", , "diagnostico_problemas", "migration")
            enviar_senal_log("INFO", "✅ SISTEMA SALUDABLE: No se detectaron problemas críticos", "diagnostico_problemas", "migration")
