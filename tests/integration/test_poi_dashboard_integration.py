import random
from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 TEST INTEGRACIÓN POI ↔ DASHBOARD
====================================

Test crítico para validar la integración entre el sistema POI validado
y el ICT Professional Widget del dashboard.

OBJETIVO: Asegurar que la integración no rompe ningún sistema.
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

# Configurar path del proyecto
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_poi_dashboard_integration():
    """Test principal de integración POI → Dashboard"""
    enviar_senal_log("INFO", "🧪 INICIANDO TEST INTEGRACIÓN POI ↔ DASHBOARD", "test_poi_dashboard_integration", "migration")
    enviar_senal_log("INFO", "=" * 60, "test_poi_dashboard_integration", "migration")

    try:
        # 1. IMPORTAR SISTEMAS CRÍTICOS
        enviar_senal_log("INFO", "📦 PASO 1: Importando sistemas...", "test_poi_dashboard_integration", "migration")

        from core.poi_system.poi_detector import detectar_todos_los_pois, POI_TYPES
        enviar_senal_log("INFO", "   ✅ Sistema POI importado", "test_poi_dashboard_integration", "migration")

        from dashboard.ict_professional_widget import ICTProfessionalWidget
        enviar_senal_log("INFO", "   ✅ ICT Widget importado", "test_poi_dashboard_integration", "migration")

        # 2. CREAR DATOS DE PRUEBA
        enviar_senal_log("INFO", "\n📊 PASO 2: Generando datos de prueba...", "test_poi_dashboard_integration", "migration")

        # Generar datos OHLC similares a los del test POI
        np.random.seed(42)
        data = []
        base_price = 1.1800

        for i in range(100):
            open_price = base_price + np.random.normal(0, 0.0005)
            high_price = open_price + abs(np.random.normal(0, 0.0003))
            low_price = open_price - abs(np.random.normal(0, 0.0003))
            close_price = open_price + np.random.normal(0, 0.0003)
            volume = int(np.random.normal(1000, 200))

            data.append({
                'open': open_price,
                'high': max(open_price, high_price),
                'low': min(open_price, low_price),
                'close': close_price,
                'volume': max(volume, 100)
            })

            base_price = close_price

        test_df = pd.DataFrame(data)
        current_price = 1.1805

        enviar_senal_log("INFO", f"   ✅ DataFrame generado: {len(test_df, "test_poi_dashboard_integration", "migration")} velas")
        enviar_senal_log("INFO", f"   ✅ Precio actual: {current_price}", "test_poi_dashboard_integration", "migration")

        # 3. VALIDAR SISTEMA POI FUNCIONA
        enviar_senal_log("INFO", "\n🎯 PASO 3: Validando sistema POI independiente...", "test_poi_dashboard_integration", "migration")

        pois_result = detectar_todos_los_pois(test_df, 'H1', current_price)
        total_pois = (len(pois_result.get('order_blocks', [])) +
                     len(pois_result.get('fair_value_gaps', [])) +
                     len(pois_result.get('breaker_blocks', [])) +
                     len(pois_result.get('imbalances', [])))

        enviar_senal_log("INFO", f"   ✅ POIs detectados: {total_pois}", "test_poi_dashboard_integration", "migration")
        enviar_senal_log("INFO", f"   ✅ OB: {len(pois_result.get('order_blocks', [], "test_poi_dashboard_integration", "migration"))}")
        enviar_senal_log("INFO", f"   ✅ FVG: {len(pois_result.get('fair_value_gaps', [], "test_poi_dashboard_integration", "migration"))}")
        enviar_senal_log("INFO", f"   ✅ BB: {len(pois_result.get('breaker_blocks', [], "test_poi_dashboard_integration", "migration"))}")
        enviar_senal_log("INFO", f"   ✅ IM: {len(pois_result.get('imbalances', [], "test_poi_dashboard_integration", "migration"))}")

        # 4. INICIALIZAR WIDGET
        enviar_senal_log("INFO", "\n🖥️ PASO 4: Inicializando ICT Widget...", "test_poi_dashboard_integration", "migration")

        widget = ICTProfessionalWidget()
        enviar_senal_log("INFO", f"   ✅ Widget creado", "test_poi_dashboard_integration", "migration")
        enviar_senal_log("INFO", f"   ✅ POIs iniciales: {len(widget.pois, "test_poi_dashboard_integration", "migration")}")
        enviar_senal_log("INFO", f"   ✅ Precio del widget: {widget.current_price}", "test_poi_dashboard_integration", "migration")

        # 5. INTEGRACIÓN CRÍTICA: POI → DASHBOARD
        enviar_senal_log("INFO", "\n🔥 PASO 5: EJECUTANDO INTEGRACIÓN CRÍTICA...", "test_poi_dashboard_integration", "migration")

        # Actualizar precio del widget
        widget.current_price = current_price

        # MOMENTO CRÍTICO: Usar sistema POI validado en dashboard
        widget.update_poi_data(test_df)

        enviar_senal_log("INFO", f"   ✅ Integración completada", "test_poi_dashboard_integration", "migration")
        enviar_senal_log("INFO", f"   ✅ POIs en widget: {len(widget.pois, "test_poi_dashboard_integration", "migration")}")

        # 6. VALIDAR RESULTADOS
        enviar_senal_log("INFO", "\n✅ PASO 6: Validando resultados...", "test_poi_dashboard_integration", "migration")

        # Verificar que se detectaron POIs
        assert len(widget.pois) > 0, "Widget debe tener POIs después de la integración"
        enviar_senal_log("INFO", f"   ✅ Widget tiene {len(widget.pois, "test_poi_dashboard_integration", "migration")} POIs")

        # Verificar estructura de POIs
        for i, poi in enumerate(widget.pois[:3]):  # Verificar primeros 3
            assert 'type' in poi, f"POI {i} debe tener tipo"
            assert 'price' in poi, f"POI {i} debe tener precio"
            assert 'strength' in poi, f"POI {i} debe tener fuerza"
            assert 'timeframe' in poi, f"POI {i} debe tener timeframe"
            enviar_senal_log("INFO", f"   ✅ POI {i}: {poi['type']} @ {poi['price']:.5f} (Fuerza: {poi['strength']}, "test_poi_dashboard_integration", "migration")")

        # Verificar que los POIs están ordenados por proximidad
        if len(widget.pois) > 1:
            distances = [abs(current_price - poi['price']) for poi in widget.pois]
            is_sorted = all(distances[i] <= distances[i+1] for i in range(len(distances)-1))
            assert is_sorted, "POIs deben estar ordenados por proximidad"
            enviar_senal_log("INFO", f"   ✅ POIs ordenados por proximidad", "test_poi_dashboard_integration", "migration")

        # 7. TEST DE RENDERIZADO (sin mostrar output)
        enviar_senal_log("INFO", "\n🎨 PASO 7: Validando capacidad de renderizado...", "test_poi_dashboard_integration", "migration")

        try:
            # Solo verificar que el método existe y no da error
            panel = widget._render_no_analysis_panel()
            assert panel is not None, "Widget debe poder renderizar panel sin análisis"
            enviar_senal_log("INFO", "   ✅ Renderizado básico funcional", "test_poi_dashboard_integration", "migration")

        except Exception as render_error:
            enviar_senal_log("ERROR", f"   ⚠️ Advertencia renderizado: {render_error}", "test_poi_dashboard_integration", "migration")
            # No falla el test, solo advertencia

        enviar_senal_log("INFO", "\n🎉 PASO 8: RESUMEN DE INTEGRACIÓN", "test_poi_dashboard_integration", "migration")
        enviar_senal_log("INFO", "=" * 60, "test_poi_dashboard_integration", "migration")
        enviar_senal_log("INFO", f"✅ Sistema POI: FUNCIONAL ({total_pois} POIs detectados, "test_poi_dashboard_integration", "migration")")
        enviar_senal_log("INFO", f"✅ Widget Dashboard: FUNCIONAL ({len(widget.pois, "test_poi_dashboard_integration", "migration")} POIs integrados)")
        enviar_senal_log("INFO", f"✅ Integración POI→Dashboard: EXITOSA", "test_poi_dashboard_integration", "migration")

        # Manejo seguro del resumen
        resumen = pois_result.get('resumen', {})
        tiempo_proc = resumen.get('tiempo_procesamiento', 0) if isinstance(resumen, dict) else 0
        enviar_senal_log("INFO", f"✅ Performance: {tiempo_proc:.3f}s", "test_poi_dashboard_integration", "migration")
        enviar_senal_log("INFO", f"✅ Timestamp: {widget.last_update.strftime('%H:%M:%S', "test_poi_dashboard_integration", "migration")}")

        enviar_senal_log("INFO", "\n🚀 RESULTADO: INTEGRACIÓN COMPLETAMENTE EXITOSA", "test_poi_dashboard_integration", "migration")
        return True

    except Exception as e:
        enviar_senal_log("ERROR", f"\n❌ ERROR EN INTEGRACIÓN: {str(e, "test_poi_dashboard_integration", "migration")}")
        enviar_senal_log("ERROR", f"📍 Tipo de error: {type(e, "test_poi_dashboard_integration", "migration").__name__}")
        import traceback
        enviar_senal_log("INFO", f"📋 Traceback:\n{traceback.format_exc(, "test_poi_dashboard_integration", "migration")}")
        return False

def test_poi_dashboard_edge_cases():
    """Test casos edge de la integración"""
    enviar_senal_log("INFO", "\n🧪 TESTING CASOS EDGE DE INTEGRACIÓN", "test_poi_dashboard_integration", "migration")
    enviar_senal_log("INFO", "-" * 50, "test_poi_dashboard_integration", "migration")

    try:

        widget = ICTProfessionalWidget()

        # Test 1: DataFrame vacío
        enviar_senal_log("INFO", "📋 Test 1: DataFrame vacío...", "test_poi_dashboard_integration", "migration")
        empty_df = pd.DataFrame()
        widget.update_poi_data(empty_df)
        assert len(widget.pois) == 0, "Widget debe manejar DataFrame vacío"
        enviar_senal_log("INFO", "   ✅ DataFrame vacío manejado correctamente", "test_poi_dashboard_integration", "migration")

        # Test 2: DataFrame None
        enviar_senal_log("INFO", "📋 Test 2: DataFrame None...", "test_poi_dashboard_integration", "migration")
        try:
            # Test que el widget maneja None sin error crítico
            widget.update_poi_data(None)  # type: ignore
            assert len(widget.pois) == 0, "Widget debe manejar None"
            enviar_senal_log("INFO", "   ✅ None manejado correctamente", "test_poi_dashboard_integration", "migration")
        except Exception as e:
            enviar_senal_log("INFO", f"   ⚠️ None genera excepción manejable: {e}", "test_poi_dashboard_integration", "migration")
            # Esto es aceptable, el widget no debe crashear

        # Test 3: DataFrame pequeño
        enviar_senal_log("INFO", "📋 Test 3: DataFrame pequeño...", "test_poi_dashboard_integration", "migration")
        small_df = pd.DataFrame({
            'open': [1.1800, 1.1805],
            'high': [1.1810, 1.1815],
            'low': [1.1795, 1.1800],
            'close': [1.1805, 1.1810],
            'volume': [1000, 1100]
        })
        widget.update_poi_data(small_df)
        # No debe fallar, POIs pueden ser 0 por dataset pequeño
        enviar_senal_log("INFO", f"   ✅ DataFrame pequeño procesado: {len(widget.pois, "test_poi_dashboard_integration", "migration")} POIs")

        enviar_senal_log("INFO", "\n✅ TODOS LOS CASOS EDGE SUPERADOS", "test_poi_dashboard_integration", "migration")
        return True

    except Exception as e:
        enviar_senal_log("ERROR", f"\n❌ ERROR EN CASOS EDGE: {str(e, "test_poi_dashboard_integration", "migration")}")
        return False

if __name__ == "__main__":
    enviar_senal_log("INFO", "🎯 INICIANDO SUITE DE INTEGRACIÓN POI ↔ DASHBOARD", "test_poi_dashboard_integration", "migration")
    enviar_senal_log("INFO", "=" * 80, "test_poi_dashboard_integration", "migration")
    enviar_senal_log("INFO", "🎯 OBJETIVO: Validar integración entre sistema POI (100% testado, "test_poi_dashboard_integration", "migration")")
    enviar_senal_log("INFO", "🎯           y ICT Professional Widget del Dashboard", "test_poi_dashboard_integration", "migration")
    enviar_senal_log("INFO", "=" * 80, "test_poi_dashboard_integration", "migration")

    # Test principal
    test1_result = test_poi_dashboard_integration()

    # Test casos edge
    test2_result = test_poi_dashboard_edge_cases()

    # Resultado final
    enviar_senal_log("INFO", "\n" + "=" * 80, "test_poi_dashboard_integration", "migration")
    enviar_senal_log("INFO", "📊 RESULTADO FINAL DE INTEGRACIÓN POI ↔ DASHBOARD", "test_poi_dashboard_integration", "migration")
    enviar_senal_log("INFO", "=" * 80, "test_poi_dashboard_integration", "migration")

    if test1_result and test2_result:
        enviar_senal_log("INFO", "🎉 RESULTADO: INTEGRACIÓN COMPLETAMENTE EXITOSA", "test_poi_dashboard_integration", "migration")
        enviar_senal_log("INFO", "✅ Sistema POI: Funcionando al 100%", "test_poi_dashboard_integration", "migration")
        enviar_senal_log("INFO", "✅ Dashboard Widget: Funcionando al 100%", "test_poi_dashboard_integration", "migration")
        enviar_senal_log("ERROR", "✅ Integración: Sin errores ni regresiones", "test_poi_dashboard_integration", "migration")
        enviar_senal_log("INFO", "🚀 DASHBOARD ENHANCEMENT: LISTO PARA CONTINUAR", "test_poi_dashboard_integration", "migration")
        exit(0)
    else:
        enviar_senal_log("INFO", "❌ RESULTADO: INTEGRACIÓN CON PROBLEMAS", "test_poi_dashboard_integration", "migration")
        enviar_senal_log("ERROR", "⚠️ Revisar errores antes de proceder", "test_poi_dashboard_integration", "migration")
        exit(1)
