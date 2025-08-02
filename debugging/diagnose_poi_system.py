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
    print("🔍 TEST 1: Verificando imports POI...")

    try:
        from core.poi_system.poi_detector import (
            detectar_order_blocks,
            detectar_fair_value_gaps,
            detectar_breaker_blocks,
            detectar_imbalances,
            detectar_todos_los_pois
        )
        print("✅ Imports POI: OK")
        return True, {
            'detectar_order_blocks': detectar_order_blocks,
            'detectar_fair_value_gaps': detectar_fair_value_gaps,
            'detectar_breaker_blocks': detectar_breaker_blocks,
            'detectar_imbalances': detectar_imbalances,
            'detectar_todos_los_pois': detectar_todos_los_pois
        }
    except ImportError as e:
        print(f"❌ Imports POI fallaron: {e}")
        return False, {}

def test_ict_detector_imports():
    """Test 2: Verificar ICTDetector"""
    print("🔍 TEST 2: Verificando ICTDetector...")

    try:
        from core.ict_engine.ict_detector import ICTDetector
        detector = ICTDetector()
        print("✅ ICTDetector: OK")
        return True, detector
    except Exception as e:
        print(f"❌ ICTDetector falló: {e}")
        return False, None

def create_test_data():
    """Test 3: Crear datos de prueba realistas"""
    print("🔍 TEST 3: Creando datos de prueba...")

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

        print(f"✅ Datos de prueba creados: {len(df)} velas")
        print(f"   Rango precio: {df['low'].min():.5f} - {df['high'].max():.5f}")
        print(f"   Precio actual (último close): {df['close'].iloc[-1]:.5f}")

        return True, df

    except Exception as e:
        print(f"❌ Error creando datos de prueba: {e}")
        return False, None

def test_poi_functions_individually(poi_functions, test_df):
    """Test 4: Probar cada función POI individualmente"""
    print("🔍 TEST 4: Probando funciones POI individuales...")

    results = {}

    for func_name, func in poi_functions.items():
        try:
            print(f"   Probando {func_name}...")
            result = func(test_df, 'M15')

            if isinstance(result, list):
                results[func_name] = {
                    'success': True,
                    'count': len(result),
                    'sample': result[0] if result else None
                }
                print(f"   ✅ {func_name}: {len(result)} POIs detectados")

            else:
                results[func_name] = {
                    'success': False,
                    'error': f"Tipo inesperado: {type(result)}"
                }
                print(f"   ❌ {func_name}: Tipo inesperado {type(result)}")

        except Exception as e:
            results[func_name] = {
                'success': False,
                'error': str(e)
            }
            print(f"   ❌ {func_name}: Error - {e}")

    return results

def test_ict_detector_find_pois(ict_detector, test_df):
    """Test 5: Probar ICTDetector.find_pois()"""
    print("🔍 TEST 5: Probando ICTDetector.find_pois()...")

    try:
        current_price = float(test_df['close'].iloc[-1])
        print(f"   Precio actual: {current_price:.5f}")

        pois = ict_detector.find_pois(test_df)

        print(f"   ✅ find_pois() ejecutado: {len(pois)} POIs encontrados")

        if pois:
            print("   Muestra de POIs encontrados:")
            for i, poi in enumerate(pois[:3]):
                print(f"      {i+1}. {poi.get('type', 'N/A')} @ {poi.get('price_level', 'N/A'):.5f}")
        else:
            print("   ⚠️ No se encontraron POIs - investigando causas...")

            # Debug: Verificar métodos auxiliares
            print("   Depuración de métodos auxiliares:")

            ob_pois = ict_detector._find_order_block_pois_advanced(test_df, current_price)
            print(f"      Order Blocks: {len(ob_pois)}")

            liq_pois = ict_detector._find_liquidity_pois_advanced(test_df, current_price)
            print(f"      Liquidity: {len(liq_pois)}")

            sr_pois = ict_detector._find_support_resistance_pois_advanced(test_df, current_price)
            print(f"      Support/Resistance: {len(sr_pois)}")

            fvg_pois = ict_detector._find_fvg_pois_advanced(test_df, current_price)
            print(f"      FVG: {len(fvg_pois)}")

            hod_lod_pois = ict_detector._find_hod_lod_pois(test_df, current_price)
            print(f"      HOD/LOD: {len(hod_lod_pois)}")

        return True, pois

    except Exception as e:
        print(f"   ❌ Error en find_pois(): {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return False, []

def test_detectar_todos_los_pois(poi_functions, test_df):
    """Test 6: Probar función completa detectar_todos_los_pois"""
    print("🔍 TEST 6: Probando detectar_todos_los_pois()...")

    try:
        current_price = float(test_df['close'].iloc[-1])
        result = poi_functions['detectar_todos_los_pois'](test_df, 'M15', current_price)

        if isinstance(result, dict):
            total_pois = 0
            print(f"   ✅ detectar_todos_los_pois() ejecutado:")

            for poi_type, poi_list in result.items():
                if isinstance(poi_list, list) and poi_type != 'resumen':
                    total_pois += len(poi_list)
                    print(f"      {poi_type}: {len(poi_list)} POIs")

            print(f"   Total POIs: {total_pois}")
            return True, result
        else:
            print(f"   ❌ Tipo inesperado: {type(result)}")
            return False, {}

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, {}

def main():
    """Ejecutar diagnóstico completo"""
    print("🚀 INICIANDO DIAGNÓSTICO POI SYSTEM")
    print("=" * 50)

    # Test 1: Imports POI
    poi_imports_ok, poi_functions = test_poi_imports()
    if not poi_imports_ok:
        print("💀 ERROR CRÍTICO: No se pueden importar funciones POI")
        return

    # Test 2: ICTDetector
    ict_imports_ok, ict_detector = test_ict_detector_imports()
    if not ict_imports_ok:
        print("💀 ERROR CRÍTICO: No se puede importar ICTDetector")
        return

    # Test 3: Datos de prueba
    data_ok, test_df = create_test_data()
    if not data_ok:
        print("💀 ERROR CRÍTICO: No se pueden crear datos de prueba")
        return

    # Test 4: Funciones POI individuales
    print("\\n" + "=" * 50)
    poi_results = test_poi_functions_individually(poi_functions, test_df)

    # Test 5: ICTDetector.find_pois()
    print("\\n" + "=" * 50)
    ict_find_pois_ok, ict_pois = test_ict_detector_find_pois(ict_detector, test_df)

    # Test 6: detectar_todos_los_pois
    print("\\n" + "=" * 50)
    detectar_todos_ok, todos_result = test_detectar_todos_los_pois(poi_functions, test_df)

    # Resumen final
    print("\\n" + "=" * 50)
    print("📊 RESUMEN DE DIAGNÓSTICO:")
    print("=" * 50)

    print(f"✅ Imports POI: {'OK' if poi_imports_ok else 'FAIL'}")
    print(f"✅ ICTDetector: {'OK' if ict_imports_ok else 'FAIL'}")
    print(f"✅ Datos de prueba: {'OK' if data_ok else 'FAIL'}")

    # Resumen de funciones POI
    for func_name, result in poi_results.items():
        status = "OK" if result['success'] else "FAIL"
        count = result.get('count', 0) if result['success'] else 0
        print(f"   {func_name}: {status} ({count} POIs)")

    print(f"✅ ICTDetector.find_pois(): {'OK' if ict_find_pois_ok else 'FAIL'} ({len(ict_pois)} POIs)")
    print(f"✅ detectar_todos_los_pois(): {'OK' if detectar_todos_ok else 'FAIL'}")

    # Diagnóstico de causas
    if len(ict_pois) == 0:
        print("\\n🔍 ANÁLISIS DE CAUSA RAÍZ:")
        print("El problema find_pois() -> [] puede deberse a:")
        print("1. Métodos auxiliares ICTDetector devuelven listas vacías")
        print("2. Datos de entrada no cumplen criterios de detección")
        print("3. Umbrales de filtrado demasiado restrictivos")
        print("4. Error en integración ICTDetector <-> poi_detector")

        if any(result['success'] and result['count'] > 0 for result in poi_results.values()):
            print("\\n✅ SOLUCIÓN: Las funciones POI SÍ detectan POIs")
            print("El problema está en la integración ICTDetector")
            print("Recomendación: Verificar métodos auxiliares en ict_detector.py")
        else:
            print("\\n⚠️ PROBLEMA: Las funciones POI NO detectan POIs")
            print("Recomendación: Verificar datos de entrada y umbrales")

    print("\\n🎯 DIAGNÓSTICO COMPLETADO")

if __name__ == "__main__":
    main()
