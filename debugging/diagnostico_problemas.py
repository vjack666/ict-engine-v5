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
    print("🔍 DIAGNÓSTICO DE PROBLEMAS - CAJA NEGRA")
    print("=" * 50)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Verificar archivos principales
    print("📁 VERIFICANDO ARCHIVOS PRINCIPALES:")
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
            print(f"   ✅ {archivo}")
        else:
            archivos_faltantes.append(archivo)
            print(f"   ❌ {archivo} - NO ENCONTRADO")

    print()
    print("🔍 INTENTANDO IMPORTAR SISTEMA DE DIAGNÓSTICOS:")

    try:
        from utils.system_diagnostics import POIBlackBoxDiagnostics
        print("   ✅ Import exitoso - Sistema simplificado cargado")

        # Crear instancia
        diagnostics = POIBlackBoxDiagnostics()
        print("   ✅ Instancia creada")

        # Ejecutar diagnóstico
        print()
        print("🔬 EJECUTANDO DIAGNÓSTICO COMPLETO:")
        resultado = diagnostics.run_full_diagnostic(None)  # Sin dashboard instance por ahora

        print(f"   📊 Issues detectados: {len(resultado.get('critical_issues', []))}")
        print(f"   🔧 Soluciones disponibles: {len(resultado.get('solutions', []))}")

        if resultado.get('critical_issues'):
            print()
            print("🚨 PROBLEMAS DETECTADOS:")
            for i, issue in enumerate(resultado['critical_issues'], 1):
                print(f"   {i}. {issue}")

        if resultado.get('solutions'):
            print()
            print("💡 SOLUCIONES PROPUESTAS:")
            for i, solucion in enumerate(resultado['solutions'], 1):
                print(f"   {i}. {solucion}")

        # Verificar sistema de logging
        print()
        print("📝 VERIFICANDO SISTEMA DE LOGGING:")
        try:
            from sistema.logging_interface import enviar_senal_log
            enviar_senal_log("DEBUG", "Test de logging desde diagnóstico", __name__, "general")
            print("   ✅ Sistema de logging funcional")
        except Exception as e:
            print(f"   ⚠️ Problema con logging: {e}")

        # Verificar importación POI
        print()
        print("🎯 VERIFICANDO SISTEMA POI:")
        try:
            from core.poi_system.poi_detector import POIDetector
            print("   ✅ POI Detector disponible")
        except Exception as e:
            print(f"   ❌ Error POI Detector: {e}")

        try:
            from core.poi_system.poi_scoring_engine import POIScoringEngine
            print("   ✅ POI Scoring Engine disponible")
        except Exception as e:
            print(f"   ❌ Error POI Scoring: {e}")

        # Verificar MT5 Data Manager
        print()
        print("📊 VERIFICANDO MT5 DATA MANAGER:")
        try:
            from utils.mt5_data_manager import MT5DataManager
            print("   ✅ MT5DataManager disponible")
        except Exception as e:
            print(f"   ❌ Error MT5DataManager: {e}")

        print()
        print("✅ DIAGNÓSTICO COMPLETADO")

        return resultado

    except ImportError as e:
        print(f"   ❌ Error de import: {e}")
        print()
        print("🔧 DIAGNÓSTICO DE IMPORTS:")

        # Verificar ruta de poi_black_box_diagnostics
        archivos_poi = list(Path(".").glob("**/poi_black_box_diagnostics.py"))
        if archivos_poi:
            print(f"   📁 Archivo encontrado en: {archivos_poi[0]}")
        else:
            print("   ❌ Archivo poi_black_box_diagnostics.py no encontrado")

        return None

    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        return None

if __name__ == "__main__":
    resultado = main()

    if resultado:
        print()
        print("🎯 RESUMEN FINAL:")
        print(f"   📊 Total de problemas: {len(resultado.get('critical_issues', []))}")
        print(f"   🔧 Total de soluciones: {len(resultado.get('solutions', []))}")

        if resultado.get('critical_issues'):
            print()
            print("⚠️ ACCIÓN REQUERIDA: Se detectaron problemas que necesitan corrección")
        else:
            print()
            print("✅ SISTEMA SALUDABLE: No se detectaron problemas críticos")
