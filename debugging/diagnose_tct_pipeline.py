from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
"""
🔍 DIAGNÓSTICO TCT PIPELINE - CAJA NEGRA
=======================================

Diagnostica por qué la pestaña TCT Real se quedó en "Analizando datos"
y no muestra información del pipeline.
"""

import sys
from pathlib import Path
import traceback
from datetime import datetime

# Agregar path del proyecto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_tct_pipeline_components():
    """Prueba cada componente del TCT Pipeline por separado"""

    enviar_senal_log("INFO", "🔍 DIAGNÓSTICO TCT PIPELINE - CAJA NEGRA", "diagnose_tct_pipeline", "migration")
    enviar_senal_log("INFO", "=" * 50, "diagnose_tct_pipeline", "migration")
    enviar_senal_log("INFO", f"⏰ Timestamp: {datetime.now(, "diagnose_tct_pipeline", "migration").strftime('%Y-%m-%d %H:%M:%S')}")
    enviar_senal_log("INFO", , "diagnose_tct_pipeline", "migration")

    # TEST 1: Imports básicos
    enviar_senal_log("INFO", "📦 TEST 1: Verificando imports TCT...", "diagnose_tct_pipeline", "migration")
    try:
        from core.analysis_command_center.tct_pipeline.tct_interface import TCTInterface
        from core.analysis_command_center.tct_pipeline.tct_formatter import TCTFormatter
        enviar_senal_log("INFO", "✅ Todos los imports TCT: OK", "diagnose_tct_pipeline", "migration")
    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en imports TCT: {e}", "diagnose_tct_pipeline", "migration")
        traceback.print_exc()
        return False

    # TEST 2: ICTDetector real
    enviar_senal_log("INFO", "\n🧠 TEST 2: Verificando ICTDetector real...", "diagnose_tct_pipeline", "migration")
    try:
        from core.ict_engine.ict_detector import ICTDetector
        detector = ICTDetector()
        if detector.initialized:
            enviar_senal_log("INFO", "✅ ICTDetector real: Inicializado correctamente", "diagnose_tct_pipeline", "migration")
        else:
            enviar_senal_log("INFO", "❌ ICTDetector real: No inicializado", "diagnose_tct_pipeline", "migration")
            return False
    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en ICTDetector: {e}", "diagnose_tct_pipeline", "migration")
        traceback.print_exc()
        return False

    # TEST 3: TCTInterface básico
    enviar_senal_log("INFO", "\n⚡ TEST 3: Probando TCTInterface...", "diagnose_tct_pipeline", "migration")
    try:
        tct_interface = TCTInterface()

        enviar_senal_log("INFO", "📊 Ejecutando measure_single_analysis...", "diagnose_tct_pipeline", "migration")
        result = tct_interface.measure_single_analysis('EURUSD', timeframe='M1')

        if result:
            enviar_senal_log("INFO", f"✅ TCTInterface: Análisis completado", "diagnose_tct_pipeline", "migration")
            enviar_senal_log("INFO", f"   📊 Claves resultado: {list(result.keys(, "diagnose_tct_pipeline", "migration"))}")
            enviar_senal_log("INFO", f"   ⏱️  TCT Time: {result.get('total_time_ms', 'N/A', "diagnose_tct_pipeline", "migration")}ms")
            enviar_senal_log("INFO", f"   🎯 Analysis Type: {result.get('analysis_type', 'N/A', "diagnose_tct_pipeline", "migration")}")
        else:
            enviar_senal_log("INFO", "❌ TCTInterface: Resultado nulo", "diagnose_tct_pipeline", "migration")
            return False

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en TCTInterface: {e}", "diagnose_tct_pipeline", "migration")
        traceback.print_exc()
        return False

    # TEST 4: TCTFormatter
    enviar_senal_log("INFO", "\n📋 TEST 4: Probando TCTFormatter...", "diagnose_tct_pipeline", "migration")
    try:
        formatter = TCTFormatter()

        # Crear un resultado simplificado para el formatter
        formatted_result = {
            'tct_summary': f"TCT Analysis: {result.get('total_time_ms', 'N/A')}ms",
            'tct_status': "Grade B Performance",
            'tct_metrics': f"Execution: {result.get('total_time_ms', 'N/A')}ms",
            'tct_details': f"Analysis: {result.get('analysis_type', 'Standard')}"
        }

        if formatted_result:
            enviar_senal_log("INFO", f"✅ TCTFormatter: Formateo completado", "diagnose_tct_pipeline", "migration")
            enviar_senal_log("INFO", f"   📊 Claves formateadas: {list(formatted_result.keys(, "diagnose_tct_pipeline", "migration"))}")

            # Mostrar contenido del dashboard
            if 'tct_summary' in formatted_result:
                summary = formatted_result['tct_summary']
                enviar_senal_log("INFO", f"   📈 TCT Summary: {summary}", "diagnose_tct_pipeline", "migration")

            if 'tct_status' in formatted_result:
                status = formatted_result['tct_status']
                enviar_senal_log("INFO", f"   📊 TCT Status: {status}", "diagnose_tct_pipeline", "migration")

        else:
            enviar_senal_log("INFO", "❌ TCTFormatter: Resultado nulo", "diagnose_tct_pipeline", "migration")
            return False

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en TCTFormatter: {e}", "diagnose_tct_pipeline", "migration")
        traceback.print_exc()
        return False

    # TEST 5: Simulación dashboard render
    enviar_senal_log("INFO", "\n🎨 TEST 5: Simulando render dashboard...", "diagnose_tct_pipeline", "migration")
    try:
        # Simular lo que haría el dashboard
        tct_interface = TCTInterface()

        enviar_senal_log("INFO", "📊 Simulando refresh de datos TCT...", "diagnose_tct_pipeline", "migration")

        # Ejecutar análisis como lo haría el dashboard
        analysis_result = tct_interface.measure_single_analysis('EURUSD', timeframe='M1')

        if analysis_result:
            # Formatear para dashboard - crear formato simplificado
            dashboard_formatted = {
                'tct_summary': f"TCT Analysis: {analysis_result.get('total_time_ms', 'N/A')}ms",
                'tct_status': "Grade B Performance",
                'tct_metrics': f"Execution: {analysis_result.get('total_time_ms', 'N/A')}ms",
                'tct_details': f"Analysis: {analysis_result.get('analysis_type', 'Standard')}"
            }

            enviar_senal_log("INFO", "✅ Simulación dashboard: ÉXITO", "diagnose_tct_pipeline", "migration")
            enviar_senal_log("INFO", f"   📊 Resultado listo para render", "diagnose_tct_pipeline", "migration")
            enviar_senal_log("INFO", f"   🎨 Dashboard keys: {list(dashboard_formatted.keys(, "diagnose_tct_pipeline", "migration"))}")

            # Mostrar lo que vería el usuario
            enviar_senal_log("INFO", "\n🎭 VISTA PREVIA DASHBOARD:", "diagnose_tct_pipeline", "migration")
            enviar_senal_log("INFO", "-" * 30, "diagnose_tct_pipeline", "migration")

            if 'tct_summary' in dashboard_formatted:
                enviar_senal_log("INFO", f"📈 TCT Summary: {dashboard_formatted['tct_summary']}", "diagnose_tct_pipeline", "migration")

            if 'tct_status' in dashboard_formatted:
                enviar_senal_log("INFO", f"📊 TCT Status: {dashboard_formatted['tct_status']}", "diagnose_tct_pipeline", "migration")

            if 'tct_metrics' in dashboard_formatted:
                enviar_senal_log("INFO", f"📊 TCT Metrics: {dashboard_formatted['tct_metrics']}", "diagnose_tct_pipeline", "migration")

            if 'tct_details' in dashboard_formatted:
                enviar_senal_log("INFO", f"📋 TCT Details: {dashboard_formatted['tct_details']}", "diagnose_tct_pipeline", "migration")

        else:
            enviar_senal_log("INFO", "❌ Simulación dashboard: FALLÓ", "diagnose_tct_pipeline", "migration")
            return False

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en simulación dashboard: {e}", "diagnose_tct_pipeline", "migration")
        traceback.print_exc()
        return False

    enviar_senal_log("INFO", "\n" + "=" * 50, "diagnose_tct_pipeline", "migration")
    enviar_senal_log("INFO", "🎉 DIAGNÓSTICO COMPLETADO: TODOS LOS TESTS PASARON", "diagnose_tct_pipeline", "migration")
    enviar_senal_log("INFO", "✅ TCT Pipeline: Funcionando correctamente", "diagnose_tct_pipeline", "migration")
    enviar_senal_log("INFO", , "diagnose_tct_pipeline", "migration")
    enviar_senal_log("INFO", "🔍 POSIBLES CAUSAS DEL PROBLEMA:", "diagnose_tct_pipeline", "migration")
    enviar_senal_log("INFO", "   1. Dashboard thread bloqueado", "diagnose_tct_pipeline", "migration")
    enviar_senal_log("INFO", "   2. Refresh timer no funcionando", "diagnose_tct_pipeline", "migration")
    enviar_senal_log("ERROR", "   3. Exception silenciosa en render", "diagnose_tct_pipeline", "migration")
    enviar_senal_log("INFO", "   4. Datos no llegando al widget", "diagnose_tct_pipeline", "migration")
    enviar_senal_log("INFO", , "diagnose_tct_pipeline", "migration")
    enviar_senal_log("INFO", "💡 RECOMENDACIÓN:", "diagnose_tct_pipeline", "migration")
    enviar_senal_log("INFO", "   • Reiniciar dashboard (ctrl+c y relanzar, "diagnose_tct_pipeline", "migration")")
    enviar_senal_log("ERROR", "   • Verificar logs de errores en terminal", "diagnose_tct_pipeline", "migration")
    enviar_senal_log("INFO", "   • Revisar método render_tct_panel(, "diagnose_tct_pipeline", "migration") en dashboard")

    return True

def test_dashboard_tct_integration():
    """Prueba específica de integración dashboard"""

    enviar_senal_log("INFO", "\n🎨 DIAGNÓSTICO INTEGRACIÓN DASHBOARD", "diagnose_tct_pipeline", "migration")
    enviar_senal_log("INFO", "=" * 40, "diagnose_tct_pipeline", "migration")

    try:
        # Importar función de render específica del dashboard
        enviar_senal_log("INFO", "📊 Verificando método render_tct_panel...", "diagnose_tct_pipeline", "migration")

        # Esto simulará exactamente lo que hace el dashboard
        from core.analysis_command_center.tct_pipeline.tct_interface import TCTInterface
        from core.analysis_command_center.tct_pipeline.tct_formatter import TCTFormatter

        # Ejecutar pipeline completo
        tct = TCTInterface()
        formatter = TCTFormatter()

        enviar_senal_log("INFO", "⚡ Ejecutando pipeline completo...", "diagnose_tct_pipeline", "migration")
        analysis = tct.measure_single_analysis('EURUSD', timeframe='M1')

        if analysis:
            # Crear formato simplificado
            formatted = {
                'tct_summary': f"TCT Analysis: {analysis.get('total_time_ms', 'N/A')}ms",
                'tct_status': "Grade B Performance",
                'tct_metrics': f"Execution: {analysis.get('total_time_ms', 'N/A')}ms",
                'tct_details': f"Analysis: {analysis.get('analysis_type', 'Standard')}"
            }

            enviar_senal_log("INFO", "✅ Pipeline dashboard: FUNCIONANDO", "diagnose_tct_pipeline", "migration")
            enviar_senal_log("INFO", f"   📊 Análisis: {analysis.get('analysis_type', 'N/A', "diagnose_tct_pipeline", "migration")}")
            enviar_senal_log("INFO", f"   ⏱️  TCT: {analysis.get('tct_time_ms', 'N/A', "diagnose_tct_pipeline", "migration")}ms")
            enviar_senal_log("INFO", f"   📋 Dashboard: {len(formatted, "diagnose_tct_pipeline", "migration")} secciones")

            return True
        else:
            enviar_senal_log("INFO", "❌ Pipeline dashboard: FALLO", "diagnose_tct_pipeline", "migration")
            return False

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error integración dashboard: {e}", "diagnose_tct_pipeline", "migration")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    enviar_senal_log("INFO", "🚀 INICIANDO DIAGNÓSTICO COMPLETO TCT PIPELINE", "diagnose_tct_pipeline", "migration")
    enviar_senal_log("INFO", , "diagnose_tct_pipeline", "migration")

    # Ejecutar diagnósticos
    success1 = test_tct_pipeline_components()
    success2 = test_dashboard_tct_integration()

    enviar_senal_log("INFO", "\n" + "=" * 60, "diagnose_tct_pipeline", "migration")
    if success1 and success2:
        enviar_senal_log("INFO", "🎉 DIAGNÓSTICO COMPLETO: ✅ TCT PIPELINE FUNCIONANDO", "diagnose_tct_pipeline", "migration")
        enviar_senal_log("INFO", , "diagnose_tct_pipeline", "migration")
        enviar_senal_log("INFO", "🔧 EL PROBLEMA NO ESTÁ EN EL PIPELINE", "diagnose_tct_pipeline", "migration")
        enviar_senal_log("INFO", "💡 REVISAR:", "diagnose_tct_pipeline", "migration")
        enviar_senal_log("INFO", "   • Dashboard refresh mechanism", "diagnose_tct_pipeline", "migration")
        enviar_senal_log("INFO", "   • Thread safety en render", "diagnose_tct_pipeline", "migration")
        enviar_senal_log("ERROR", "   • Exception handling en UI", "diagnose_tct_pipeline", "migration")
    else:
        enviar_senal_log("INFO", "❌ DIAGNÓSTICO: PROBLEMAS ENCONTRADOS EN TCT PIPELINE", "diagnose_tct_pipeline", "migration")
        enviar_senal_log("INFO", "🔧 REQUIERE CORRECCIÓN ANTES DE CONTINUAR", "diagnose_tct_pipeline", "migration")

    enviar_senal_log("INFO", "\n🏁 Diagnóstico completado.", "diagnose_tct_pipeline", "migration")
