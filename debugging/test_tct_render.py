#!/usr/bin/env python3
"""
🎨 TEST ESPECÍFICO: DASHBOARD TCT RENDER
======================================

Prueba exactamente la función render_tct_panel() que se está ejecutando
en la pestaña TCT Real del dashboard.
"""

import sys
from pathlib import Path
import traceback
from datetime import datetime
import time

# Agregar path del proyecto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_dashboard_render_method():
    """Prueba el método render_tct_panel() específicamente"""

    print("🎨 TEST DASHBOARD TCT RENDER METHOD")
    print("=" * 45)
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # TEST 1: Verificar que el método existe
    print("📋 TEST 1: Verificando método render_tct_panel...")
    try:
        from dashboard.dashboard_definitivo import SentinelDashboardDefinitivo

        # Crear instancia de dashboard (sin inicializar UI)
        dashboard = SentinelDashboardDefinitivo()

        # Verificar que el método existe
        if hasattr(dashboard, 'render_tct_panel'):
            print("✅ Método render_tct_panel: EXISTE")
        else:
            print("❌ Método render_tct_panel: NO EXISTE")
            return False

    except Exception as e:
        print(f"❌ Error verificando método: {e}")
        traceback.print_exc()
        return False

    # TEST 2: Simular datos del dashboard
    print("\n📊 TEST 2: Simulando datos del dashboard...")
    try:
        # Simular el estado del dashboard cuando llama a render_tct_panel
        dashboard.real_market_data = {
            'last_update': datetime.now(),
            'candles_m1': None,
            'candles_m5': None,
            'candles_h1': None,
            'current_price': 1.17480,
            'symbol': 'EURUSD'
        }

        dashboard.symbol = "EURUSD"
        dashboard.current_price = 1.17480

        print("✅ Estado dashboard simulado correctamente")

    except Exception as e:
        print(f"❌ Error simulando estado dashboard: {e}")
        traceback.print_exc()
        return False

    # TEST 3: Ejecutar render_tct_panel manualmente
    print("\n⚡ TEST 3: Ejecutando render_tct_panel()...")
    try:
        print("🔄 Llamando a dashboard.render_tct_panel()...")

        # Medir tiempo de ejecución
        start_time = time.time()

        # Llamar al método real del dashboard
        result = dashboard.render_tct_panel()

        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # en ms

        print(f"✅ render_tct_panel(): COMPLETADO en {execution_time:.2f}ms")

        # Analizar el resultado
        if result:
            if hasattr(result, 'renderable'):
                print(f"   📊 Tipo resultado: {type(result)}")
                print(f"   🎨 Renderable: {hasattr(result, 'renderable')}")
            else:
                print(f"   📊 Resultado: {result}")
        else:
            print("   ⚠️  Resultado: None")

    except Exception as e:
        print(f"❌ Error ejecutando render_tct_panel: {e}")
        traceback.print_exc()
        return False

    # TEST 4: Verificar componentes TCT específicos
    print("\n🔍 TEST 4: Verificando componentes TCT del dashboard...")
    try:
        # Verificar si el dashboard tiene instancias TCT
        tct_components = []

        if hasattr(dashboard, 'tct_interface'):
            tct_components.append("tct_interface")
        if hasattr(dashboard, 'tct_formatter'):
            tct_components.append("tct_formatter")
        if hasattr(dashboard, 'tct_measurement_engine'):
            tct_components.append("tct_measurement_engine")

        if tct_components:
            print(f"✅ Componentes TCT encontrados: {', '.join(tct_components)}")
        else:
            print("⚠️  No se encontraron componentes TCT instanciados")

            # Verificar si puede crearlos
            print("🔧 Intentando crear componentes TCT...")
            from core.analysis_command_center.tct_pipeline.tct_interface import TCTInterface
            from core.analysis_command_center.tct_pipeline.tct_formatter import TCTFormatter

            dashboard.tct_interface = TCTInterface()
            dashboard.tct_formatter = TCTFormatter()

            print("✅ Componentes TCT creados dinámicamente")

    except Exception as e:
        print(f"❌ Error verificando componentes TCT: {e}")
        traceback.print_exc()
        return False

    # TEST 5: Probar refresh automático
    print("\n🔄 TEST 5: Probando refresh automático...")
    try:
        print("🔄 Simulando auto-refresh del dashboard...")

        # Simular llamadas múltiples como haría el auto-refresh
        for i in range(3):
            print(f"   🔄 Refresh {i+1}/3...")
            start_time = time.time()

            result = dashboard.render_tct_panel()

            end_time = time.time()
            exec_time = (end_time - start_time) * 1000

            print(f"      ⏱️  Tiempo: {exec_time:.2f}ms")

            if exec_time > 1000:  # Más de 1 segundo
                print(f"      ⚠️  LENTO: Refresh tomó {exec_time:.2f}ms")

            time.sleep(0.1)  # Pequeña pausa

        print("✅ Auto-refresh: Funcionando correctamente")

    except Exception as e:
        print(f"❌ Error en auto-refresh: {e}")
        traceback.print_exc()
        return False

    print("\n" + "=" * 45)
    print("🎉 TODOS LOS TESTS DE RENDER PASARON")
    print()

    return True

def test_tct_data_flow():
    """Prueba el flujo de datos específico del TCT"""

    print("🔄 TEST FLUJO DE DATOS TCT")
    print("=" * 30)

    try:
        from core.analysis_command_center.tct_pipeline.tct_interface import TCTInterface
        from core.analysis_command_center.tct_pipeline.tct_formatter import TCTFormatter

        # Simular exactamente los datos que recibiría del dashboard
        dashboard_data = {
            'symbol': 'EURUSD',
            'current_price': 1.17480,
            'candles': None,
            'real_market_data': {
                'last_update': datetime.now(),
                'candles_m1': None
            }
        }

        print("📊 Datos de entrada preparados")

        # PASO 1: TCTInterface
        print("⚡ PASO 1: TCTInterface.measure_single_analysis()...")
        tct = TCTInterface()
        analysis_result = tct.measure_single_analysis(dashboard_data, timeframe='M1')

        if analysis_result:
            print(f"✅ Análisis TCT: {analysis_result.get('analysis_type', 'N/A')}")
            print(f"   ⏱️  TCT Time: {analysis_result.get('tct_time_ms', 'N/A')}ms")
        else:
            print("❌ Análisis TCT: FALLÓ")
            return False

        # PASO 2: TCTFormatter
        print("📋 PASO 2: TCTFormatter.format_for_dashboard()...")
        formatter = TCTFormatter()
        formatted_result = formatter.format_for_dashboard(analysis_result)

        if formatted_result:
            print(f"✅ Formateo dashboard: {len(formatted_result)} secciones")

            # Mostrar contenido real
            for key, value in formatted_result.items():
                print(f"   📊 {key}: {value}")
        else:
            print("❌ Formateo dashboard: FALLÓ")
            return False

        # PASO 3: Render final
        print("🎨 PASO 3: Render para UI...")

        # Simular lo que haría el dashboard con este dato
        tct_content = []

        if 'tct_summary' in formatted_result:
            tct_content.append(f"📈 Summary: {formatted_result['tct_summary']}")

        if 'tct_status' in formatted_result:
            tct_content.append(f"📊 Status: {formatted_result['tct_status']}")

        if 'tct_metrics' in formatted_result:
            tct_content.append(f"📊 Metrics: {formatted_result['tct_metrics']}")

        if 'tct_details' in formatted_result:
            tct_content.append(f"📋 Details: {formatted_result['tct_details']}")

        if tct_content:
            print("✅ Contenido UI generado:")
            for content in tct_content:
                print(f"   {content}")
        else:
            print("❌ No se pudo generar contenido UI")
            return False

        print("\n✅ FLUJO DE DATOS TCT: COMPLETAMENTE FUNCIONAL")
        return True

    except Exception as e:
        print(f"❌ Error en flujo de datos: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO DIAGNÓSTICO DASHBOARD TCT RENDER")
    print()

    # Ejecutar tests específicos
    success1 = test_dashboard_render_method()
    success2 = test_tct_data_flow()

    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 DIAGNÓSTICO: ✅ RENDER TCT FUNCIONANDO CORRECTAMENTE")
        print()
        print("🔍 POSIBLE CAUSA DEL PROBLEMA:")
        print("   • Timer/Refresh automático del dashboard bloqueado")
        print("   • Exception silenciosa en UI thread")
        print("   • Textual widget not updating")
        print()
        print("💡 SOLUCIONES RECOMENDADAS:")
        print("   1. Reiniciar dashboard completamente")
        print("   2. Verificar logs en terminal dashboard")
        print("   3. Presionar 'R' para refresh manual")
        print("   4. Verificar auto-refresh timer")
    else:
        print("❌ DIAGNÓSTICO: PROBLEMAS EN RENDER TCT")
        print("🔧 REQUIERE CORRECCIÓN EN DASHBOARD")

    print("\n🏁 Test completado.")
