#!/usr/bin/env python3
"""
🧪 TEST DETECCIÓN PURA DE FRACTALES - REGLA #11
==============================================

Test específico para verificar que la detección básica de fractales
SIEMPRE encuentra swing points en cualquier conjunto de datos.

**OBJETIVO: FRACTAL DEBE DAR RESULTADOS SIEMPRE**
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

# Agregar paths necesarios
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Importar módulo original que funciona
original_path = os.path.join(os.path.dirname(__file__), '..', '..', 'proyecto principal', 'core', 'ict_engine')
sys.path.insert(0, original_path)

try:
    from fractal_analyzer import FractalAnalyzer
    FRACTAL_DISPONIBLE = True
except ImportError as e:
    print(f"❌ No se pudo importar FractalAnalyzer original: {e}")
    FRACTAL_DISPONIBLE = False
    FractalAnalyzer = None

def test_fractal_original_basico():
    """
    🧪 TEST 1: Verificar que el fractal original SIEMPRE encuentra algo
    """
    print("🧪 TEST 1: Fractal Original - Detección Básica")
    
    if not FRACTAL_DISPONIBLE:
        print("   ❌ FractalAnalyzer original no disponible")
        return False
    
    # Crear datos sintéticos simples
    dates = pd.date_range(start='2025-01-01', periods=100, freq='15min')
    
    # Crear movimiento obvio con swing high y swing low
    np.random.seed(42)
    prices = [1.0000]
    
    for i in range(99):
        if i < 20:
            prices.append(prices[-1] + np.random.uniform(0.0001, 0.0005))  # Subida clara
        elif i < 40:
            prices.append(prices[-1] + np.random.uniform(-0.0002, 0.0002))  # Consolidación
        elif i < 60:
            prices.append(prices[-1] + np.random.uniform(-0.0005, -0.0001))  # Bajada clara
        else:
            prices.append(prices[-1] + np.random.uniform(-0.0002, 0.0002))  # Consolidación
    
    # Crear DataFrame
    data = {
        'high': [p + np.random.uniform(0.0001, 0.0003) for p in prices],
        'low': [p - np.random.uniform(0.0001, 0.0003) for p in prices],
        'close': prices,
        'volume': [np.random.randint(100, 1000) for _ in range(100)]
    }
    
    # Asegurar que open esté entre low y high
    data['open'] = [np.random.uniform(data['low'][i], data['high'][i]) for i in range(100)]
    
    df = pd.DataFrame(data, index=dates)
    
    print(f"   📊 Datos creados: {len(df)} velas")
    print(f"   📈 Rango de precios: {df['low'].min():.5f} - {df['high'].max():.5f}")
    
    # Inicializar analizador original
    try:
        analyzer = FractalAnalyzer()
        print(f"   ✅ FractalAnalyzer inicializado")
        
        # Ejecutar análisis
        current_price = df['close'].iloc[-1]
        result = analyzer.analyze_fractal_range(df, current_price)
        
        if result is not None:
            print(f"   ✅ FRACTAL DETECTADO!")
            print(f"      🎯 High: {result.high:.5f}")
            print(f"      🎯 Low: {result.low:.5f}")
            print(f"      🎯 EQ: {result.eq:.5f}")
            print(f"      🎯 Confianza: {result.confidence:.1f}%")
            print(f"      🎯 Válido: {result.valid}")
            return True
        else:
            print(f"   ❌ FRACTAL NO DETECTADO - ESTO ES INCORRECTO")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR en análisis: {e}")
        return False

def test_fractal_datos_reales():
    """
    🧪 TEST 2: Usar datos reales del CSV
    """
    print("\n🧪 TEST 2: Fractal Original - Datos Reales CSV")
    
    if not FRACTAL_DISPONIBLE:
        print("   ❌ FractalAnalyzer original no disponible")
        return False
    
    # Buscar archivo CSV
    csv_path = None
    search_paths = [
        "../data/candles",
        "../data",
        "../../data/candles",
        "../../data"
    ]
    
    for search_path in search_paths:
        full_path = os.path.join(os.path.dirname(__file__), search_path)
        if os.path.exists(full_path):
            for file in os.listdir(full_path):
                if file.endswith('.csv') and 'EURUSD' in file:
                    csv_path = os.path.join(full_path, file)
                    break
            if csv_path:
                break
    
    if not csv_path:
        print("   ⚠️ No se encontró archivo CSV - usando datos sintéticos")
        return test_fractal_original_basico()
    
    try:
        df = pd.read_csv(csv_path)
        print(f"   📁 Archivo: {os.path.basename(csv_path)}")
        print(f"   📊 Datos cargados: {len(df)} filas")
        
        # Normalizar nombres de columnas
        df.columns = df.columns.str.lower()
        
        # Verificar columnas requeridas
        required_cols = ['high', 'low', 'close']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"   ❌ Columnas faltantes: {missing_cols}")
            return False
        
        print(f"   ✅ Columnas válidas: {list(df.columns)}")
        
        # Usar solo las primeras 200 filas para test rápido
        df_test = df.head(200).copy()
        
        # Asegurar tipos numéricos
        for col in ['high', 'low', 'close']:
            df_test[col] = pd.to_numeric(df_test[col], errors='coerce')
        
        # Crear índice temporal si no existe
        if 'time' in df_test.columns:
            try:
                df_test.index = pd.to_datetime(df_test['time'])
            except:
                df_test.index = pd.date_range(start='2025-01-01', periods=len(df_test), freq='15min')
        else:
            df_test.index = pd.date_range(start='2025-01-01', periods=len(df_test), freq='15min')
        
        print(f"   📈 Rango: {df_test['low'].min():.5f} - {df_test['high'].max():.5f}")
        
        # Inicializar y probar
        analyzer = FractalAnalyzer()
        current_price = df_test['close'].iloc[-1]
        result = analyzer.analyze_fractal_range(df_test, current_price)
        
        if result is not None:
            print(f"   ✅ FRACTAL DETECTADO EN DATOS REALES!")
            print(f"      🎯 High: {result.high:.5f}")
            print(f"      🎯 Low: {result.low:.5f}")
            print(f"      🎯 EQ: {result.eq:.5f}")
            print(f"      🎯 Confianza: {result.confidence:.1f}%")
            return True
        else:
            print(f"   ❌ FRACTAL NO DETECTADO EN DATOS REALES")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR cargando datos reales: {e}")
        return False

def main():
    """Ejecutar todos los tests de detección pura"""
    print("🔮 FRACTAL DETECTION - TEST PURO")
    print("=" * 50)
    
    results = []
    
    # Test 1: Datos sintéticos
    results.append(test_fractal_original_basico())
    
    # Test 2: Datos reales
    results.append(test_fractal_datos_reales())
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📋 RESUMEN FINAL:")
    
    if all(results):
        print("✅ TODOS LOS TESTS PASARON - FRACTAL ORIGINAL FUNCIONA")
        print("💡 El problema está en la versión enterprise, no en la lógica base")
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        print("⚠️ Revisar configuración del analizador original")
    
    print(f"\n🎯 Tests exitosos: {sum(results)}/{len(results)}")

if __name__ == "__main__":
    main()
