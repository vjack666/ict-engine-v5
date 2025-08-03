from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
"""
🔍 DIAGNÓSTICO POI SYSTEM - FIND_POIS DEBUGGING
==============================================

Script para diagnosticar por qué find_pois() devuelve lista vacía []
y reparar la integración ICT + POI.

Verifica:
1. Imports y dependencias POI
2. Funciones de detección individuales
3. Integración ICTDetector <-> POI System
4. Generación de datos de prueba

Fecha: 2025-01-28
"""

import sys
from pathlib import Path

# Configurar paths
project_root = Path(__file__).parent.parent  # Subir un nivel desde debugging/
sys.path.insert(0, str(project_root))

# También agregar la carpeta debugging a sys.path
debug_root = Path(__file__).parent
sys.path.insert(0, str(debug_root))

import pandas as pd
import numpy as np
from datetime import datetime
import traceback

def test_poi_imports():
    """Test 1: Verificar que todos los imports POI funcionen"""
    enviar_senal_log("INFO", "🔍 TEST 1: Verificando imports POI...", "diagnose_poi_system", "migration")

    try:
        from core.poi_system.poi_detector import (
            detectar_order_blocks,
            detectar_fair_value_gaps,
            detectar_breaker_blocks,
            detectar_imbalances,
            detectar_todos_los_pois
        )
        enviar_senal_log("INFO", "✅ Imports POI: OK", "diagnose_poi_system", "migration")
        return True, {
            'detectar_order_blocks': detectar_order_blocks,
            'detectar_fair_value_gaps': detectar_fair_value_gaps,
            'detectar_breaker_blocks': detectar_breaker_blocks,
            'detectar_imbalances': detectar_imbalances,
            'detectar_todos_los_pois': detectar_todos_los_pois
        }
    except ImportError as e:
        enviar_senal_log("INFO", f"❌ Imports POI fallaron: {e}", "diagnose_poi_system", "migration")
        return False, {}

def test_ict_detector_imports():
    """Test 2: Verificar ICTDetector"""
    enviar_senal_log("INFO", "🔍 TEST 2: Verificando ICTDetector...", "diagnose_poi_system", "migration")

    try:
        from core.ict_engine.ict_detector import ICTDetector
        detector = ICTDetector()
        enviar_senal_log("INFO", "✅ ICTDetector: OK", "diagnose_poi_system", "migration")
        return True, detector
    except Exception as e:
        enviar_senal_log("INFO", f"❌ ICTDetector falló: {e}", "diagnose_poi_system", "migration")
        return False, None

def create_test_data():
    """Test 3: Crear datos de prueba realistas"""
    enviar_senal_log("INFO", "🔍 TEST 3: Creando datos de prueba...", "diagnose_poi_system", "migration")

    try:
        # Crear 100 velas de prueba con patrón claro
        np.random.seed(42)  # Para resultados reproducibles

        dates = pd.date_range(start='2025-01-28 10:00:00', periods=100, freq='15min')

        # Precio base EURUSD
        base_price = 1.17500

        # Crear movimiento realista con tendencia y volatilidad
        price_changes = np.cumsum(np.random.normal(0, 0.0002, 100))
        prices = base_price + price_changes

        # Crear OHLC con spreads realistas
        opens = prices
        closes = opens + np.random.normal(0, 0.0001, 100)
        highs = np.maximum(opens, closes) + np.abs(np.random.normal(0, 0.0002, 100))
        lows = np.minimum(opens, closes) - np.abs(np.random.normal(0, 0.0002, 100))

        # Crear algunos gaps claros para FVG
        for i in [20, 45, 70]:
            if i < 99:
                gap_size = 0.0005  # 5 pips de gap
                lows[i+1] = highs[i] + gap_size
                opens[i+1] = lows[i+1]
                closes[i+1] = opens[i+1] + 0.0003
                highs[i+1] = closes[i+1] + 0.0001

        df = pd.DataFrame({
            'timestamp': dates,
            'open': opens,
            'high': highs,
            'low': lows,
            'close': closes,
            'volume': np.random.randint(100, 1000, 100)
        })

        # Asegurar tipos correctos
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(int)

        enviar_senal_log("INFO", f"✅ Datos de prueba creados: {len(df, "diagnose_poi_system", "migration")} velas")
        enviar_senal_log("INFO", f"   Rango precio: {df['low'].min(, "diagnose_poi_system", "migration"):.5f} - {df['high'].max():.5f}")
        enviar_senal_log("INFO", f"   Precio actual (último close, "diagnose_poi_system", "migration"): {df['close'].iloc[-1]:.5f}")

        return True, df

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error creando datos de prueba: {e}", "diagnose_poi_system", "migration")
        return False, None

def test_poi_functions_individually(poi_functions, test_df):
    """Test 4: Probar cada función POI individualmente"""
    enviar_senal_log("INFO", "🔍 TEST 4: Probando funciones POI individuales...", "diagnose_poi_system", "migration")

    results = {}

    for func_name, func in poi_functions.items():
        try:
            enviar_senal_log("INFO", f"   Probando {func_name}...", "diagnose_poi_system", "migration")
            result = func(test_df, 'M15')

            if isinstance(result, list):
                results[func_name] = {
                    'success': True,
                    'count': len(result),
                    'sample': result[0] if result else None
                }
                enviar_senal_log("INFO", f"   ✅ {func_name}: {len(result, "diagnose_poi_system", "migration")} POIs detectados")

            else:
                results[func_name] = {
                    'success': False,
                    'error': f"Tipo inesperado: {type(result)}"
                }
                enviar_senal_log("INFO", f"   ❌ {func_name}: Tipo inesperado {type(result, "diagnose_poi_system", "migration")}")

        except Exception as e:
            results[func_name] = {
                'success': False,
                'error': str(e)
            }
            enviar_senal_log("ERROR", f"   ❌ {func_name}: Error - {e}", "diagnose_poi_system", "migration")

    return results

def test_ict_detector_find_pois(ict_detector, test_df):
    """Test 5: Probar ICTDetector.find_pois()"""
    enviar_senal_log("INFO", "🔍 TEST 5: Probando ICTDetector.find_pois(, "diagnose_poi_system", "migration")...")

    try:
        current_price = float(test_df['close'].iloc[-1])
        enviar_senal_log("INFO", f"   Precio actual: {current_price:.5f}", "diagnose_poi_system", "migration")

        pois = ict_detector.find_pois(test_df)

        enviar_senal_log("INFO", f"   ✅ find_pois(, "diagnose_poi_system", "migration") ejecutado: {len(pois)} POIs encontrados")

        if pois:
            enviar_senal_log("INFO", "   Muestra de POIs encontrados:", "diagnose_poi_system", "migration")
            for i, poi in enumerate(pois[:3]):
                enviar_senal_log("INFO", f"      {i+1}. {poi.get('type', 'N/A', "diagnose_poi_system", "migration")} @ {poi.get('price_level', 'N/A'):.5f}")
        else:
            enviar_senal_log("INFO", "   ⚠️ No se encontraron POIs - investigando causas...", "diagnose_poi_system", "migration")

            # Debug: Verificar métodos auxiliares
            enviar_senal_log("INFO", "   Depuración de métodos auxiliares:", "diagnose_poi_system", "migration")

            ob_pois = ict_detector._find_order_block_pois_advanced(test_df, current_price)
            enviar_senal_log("INFO", f"      Order Blocks: {len(ob_pois, "diagnose_poi_system", "migration")}")

            liq_pois = ict_detector._find_liquidity_pois_advanced(test_df, current_price)
            enviar_senal_log("INFO", f"      Liquidity: {len(liq_pois, "diagnose_poi_system", "migration")}")

            sr_pois = ict_detector._find_support_resistance_pois_advanced(test_df, current_price)
            enviar_senal_log("INFO", f"      Support/Resistance: {len(sr_pois, "diagnose_poi_system", "migration")}")

            fvg_pois = ict_detector._find_fvg_pois_advanced(test_df, current_price)
            enviar_senal_log("INFO", f"      FVG: {len(fvg_pois, "diagnose_poi_system", "migration")}")

            hod_lod_pois = ict_detector._find_hod_lod_pois(test_df, current_price)
            enviar_senal_log("INFO", f"      HOD/LOD: {len(hod_lod_pois, "diagnose_poi_system", "migration")}")

        return True, pois

    except Exception as e:
        enviar_senal_log("ERROR", f"   ❌ Error en find_pois(, "diagnose_poi_system", "migration"): {e}")
        enviar_senal_log("INFO", f"   Traceback: {traceback.format_exc(, "diagnose_poi_system", "migration")}")
        return False, []

def test_detectar_todos_los_pois(poi_functions, test_df):
    """Test 6: Probar función completa detectar_todos_los_pois"""
    enviar_senal_log("INFO", "🔍 TEST 6: Probando detectar_todos_los_pois(, "diagnose_poi_system", "migration")...")

    try:
        current_price = float(test_df['close'].iloc[-1])
        result = poi_functions['detectar_todos_los_pois'](test_df, 'M15', current_price)

        if isinstance(result, dict):
            total_pois = 0
            enviar_senal_log("INFO", f"   ✅ detectar_todos_los_pois(, "diagnose_poi_system", "migration") ejecutado:")

            for poi_type, poi_list in result.items():
                if isinstance(poi_list, list) and poi_type != 'resumen':
                    total_pois += len(poi_list)
                    enviar_senal_log("INFO", f"      {poi_type}: {len(poi_list, "diagnose_poi_system", "migration")} POIs")

            enviar_senal_log("INFO", f"   Total POIs: {total_pois}", "diagnose_poi_system", "migration")
            return True, result
        else:
            enviar_senal_log("INFO", f"   ❌ Tipo inesperado: {type(result, "diagnose_poi_system", "migration")}")
            return False, {}

    except Exception as e:
        enviar_senal_log("ERROR", f"   ❌ Error: {e}", "diagnose_poi_system", "migration")
        return False, {}

def main():
    """Ejecutar diagnóstico completo"""
    enviar_senal_log("INFO", "🚀 INICIANDO DIAGNÓSTICO POI SYSTEM", "diagnose_poi_system", "migration")
    enviar_senal_log("INFO", "=" * 50, "diagnose_poi_system", "migration")

    # Test 1: Imports POI
    poi_imports_ok, poi_functions = test_poi_imports()
    if not poi_imports_ok:
        enviar_senal_log("ERROR", "💀 ERROR CRÍTICO: No se pueden importar funciones POI", "diagnose_poi_system", "migration")
        return

    # Test 2: ICTDetector
    ict_imports_ok, ict_detector = test_ict_detector_imports()
    if not ict_imports_ok:
        enviar_senal_log("ERROR", "💀 ERROR CRÍTICO: No se puede importar ICTDetector", "diagnose_poi_system", "migration")
        return

    # Test 3: Datos de prueba
    data_ok, test_df = create_test_data()
    if not data_ok:
        enviar_senal_log("ERROR", "💀 ERROR CRÍTICO: No se pueden crear datos de prueba", "diagnose_poi_system", "migration")
        return

    # Test 4: Funciones POI individuales
    enviar_senal_log("INFO", "\\n" + "=" * 50, "diagnose_poi_system", "migration")
    poi_results = test_poi_functions_individually(poi_functions, test_df)

    # Test 5: ICTDetector.find_pois()
    enviar_senal_log("INFO", "\\n" + "=" * 50, "diagnose_poi_system", "migration")
    ict_find_pois_ok, ict_pois = test_ict_detector_find_pois(ict_detector, test_df)

    # Test 6: detectar_todos_los_pois
    enviar_senal_log("INFO", "\\n" + "=" * 50, "diagnose_poi_system", "migration")
    detectar_todos_ok, todos_result = test_detectar_todos_los_pois(poi_functions, test_df)

    # Resumen final
    enviar_senal_log("INFO", "\\n" + "=" * 50, "diagnose_poi_system", "migration")
    enviar_senal_log("INFO", "📊 RESUMEN DE DIAGNÓSTICO:", "diagnose_poi_system", "migration")
    enviar_senal_log("INFO", "=" * 50, "diagnose_poi_system", "migration")

    enviar_senal_log("ERROR", f"✅ Imports POI: {'OK' if poi_imports_ok else 'FAIL'}", "diagnose_poi_system", "migration")
    enviar_senal_log("ERROR", f"✅ ICTDetector: {'OK' if ict_imports_ok else 'FAIL'}", "diagnose_poi_system", "migration")
    enviar_senal_log("ERROR", f"✅ Datos de prueba: {'OK' if data_ok else 'FAIL'}", "diagnose_poi_system", "migration")

    # Resumen de funciones POI
    for func_name, result in poi_results.items():
        status = "OK" if result['success'] else "FAIL"
        count = result.get('count', 0) if result['success'] else 0
        enviar_senal_log("INFO", f"   {func_name}: {status} ({count} POIs, "diagnose_poi_system", "migration")")

    enviar_senal_log("INFO", f"✅ ICTDetector.find_pois(, "diagnose_poi_system", "migration"): {'OK' if ict_find_pois_ok else 'FAIL'} ({len(ict_pois)} POIs)")
    enviar_senal_log("INFO", f"✅ detectar_todos_los_pois(, "diagnose_poi_system", "migration"): {'OK' if detectar_todos_ok else 'FAIL'}")

    # Diagnóstico de causas
    if len(ict_pois) == 0:
        enviar_senal_log("INFO", "\\n🔍 ANÁLISIS DE CAUSA RAÍZ:", "diagnose_poi_system", "migration")
        enviar_senal_log("INFO", "El problema find_pois(, "diagnose_poi_system", "migration") -> [] puede deberse a:")
        enviar_senal_log("INFO", "1. Métodos auxiliares ICTDetector devuelven listas vacías", "diagnose_poi_system", "migration")
        enviar_senal_log("INFO", "2. Datos de entrada no cumplen criterios de detección", "diagnose_poi_system", "migration")
        enviar_senal_log("INFO", "3. Umbrales de filtrado demasiado restrictivos", "diagnose_poi_system", "migration")
        enviar_senal_log("ERROR", "4. Error en integración ICTDetector <-> poi_detector", "diagnose_poi_system", "migration")

        if any(result['success'] and result['count'] > 0 for result in poi_results.values()):
            enviar_senal_log("INFO", "\\n✅ SOLUCIÓN: Las funciones POI SÍ detectan POIs", "diagnose_poi_system", "migration")
            enviar_senal_log("INFO", "El problema está en la integración ICTDetector", "diagnose_poi_system", "migration")
            enviar_senal_log("INFO", "Recomendación: Verificar métodos auxiliares en ict_detector.py", "diagnose_poi_system", "migration")
        else:
            enviar_senal_log("INFO", "\\n⚠️ PROBLEMA: Las funciones POI NO detectan POIs", "diagnose_poi_system", "migration")
            enviar_senal_log("INFO", "Recomendación: Verificar datos de entrada y umbrales", "diagnose_poi_system", "migration")

    enviar_senal_log("INFO", "\\n🎯 DIAGNÓSTICO COMPLETADO", "diagnose_poi_system", "migration")

if __name__ == "__main__":
    main()
