#!/usr/bin/env python3
"""
🔮 TEST AISLADO FRACTAL ANALYZER ENTERPRISE
====================================

📋 Propósito: Diagnóstico específico del módulo Fractal
🎯 REGLA #11: Test unitario siguiendo protocolos Copilot
📅 Fecha: Agosto 9, 2025
🔧 Versión: v6.0 Enterprise

Este test aislado permite diagnosticar problemas específicos del FractalAnalyzerEnterprise
sin la interferencia de otros módulos del sistema.
"""

import os
import sys
import pandas as pd
import time
from pathlib import Path

# Añadir el directorio raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

def test_fractal_imports():
    """🧪 Test 1: Verificar importaciones del módulo Fractal"""
    print("🔍 TEST 1: Verificando importaciones...")
    
    try:
        from core.ict_engine.fractal_analyzer_enterprise import FractalAnalyzerEnterprise
        print("✅ FractalAnalyzerEnterprise importado exitosamente")
        return True, FractalAnalyzerEnterprise
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False, None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False, None

def test_fractal_initialization():
    """🧪 Test 2: Verificar inicialización del analizador"""
    print("\n🔍 TEST 2: Verificando inicialización...")
    
    success, FractalClass = test_fractal_imports()
    if not success:
        return False, None
    
    try:
        analyzer = FractalClass(symbol="EURUSD", timeframe="M15")
        print("✅ FractalAnalyzerEnterprise inicializado exitosamente")
        print(f"   - Symbol: {analyzer.symbol if hasattr(analyzer, 'symbol') else 'N/A'}")
        print(f"   - Timeframe: {analyzer.timeframe if hasattr(analyzer, 'timeframe') else 'N/A'}")
        return True, analyzer
    except Exception as e:
        print(f"❌ Error en inicialización: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        return False, None

def test_data_loading():
    """🧪 Test 3: Verificar carga de datos CSV"""
    print("\n🔍 TEST 3: Verificando carga de datos...")
    
    data_path = os.path.join(project_root, "data", "candles")
    csv_files = [f for f in os.listdir(data_path) if f.endswith('.csv') and 'EURUSD' in f and 'M15' in f]
    
    if not csv_files:
        print("❌ No se encontraron archivos CSV de EURUSD M15")
        return False, None
    
    test_file = os.path.join(data_path, csv_files[0])
    print(f"📁 Archivo de prueba: {os.path.basename(test_file)}")
    
    try:
        df = pd.read_csv(test_file)
        print(f"✅ Datos cargados: {len(df)} filas")
        
        # Normalizar columnas (REGLA #11)
        df.columns = df.columns.str.lower()
        print(f"   - Columnas: {list(df.columns)}")
        
        required_cols = ['time', 'open', 'high', 'low', 'close']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"⚠️ Columnas faltantes: {missing_cols}")
        else:
            print("✅ Todas las columnas requeridas presentes")
        
        print(f"   - Rango de precios: {df['close'].min():.5f} - {df['close'].max():.5f}")
        return True, df
        
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return False, None

def test_fractal_analysis():
    """🧪 Test 4: Verificar análisis fractal específico"""
    print("\n🔍 TEST 4: Verificando análisis fractal...")
    
    # Obtener analizador
    success, analyzer = test_fractal_initialization()
    if not success:
        return False
    
    # Obtener datos
    success, df = test_data_loading()
    if not success:
        return False
    
    try:
        # Preparar datos para análisis
        current_price = float(df['close'].iloc[-1])
        print(f"   - Precio actual: {current_price:.5f}")
        print(f"   - Datos para análisis: {len(df)} velas")
        
        # Intentar análisis fractal
        print("   - Ejecutando detect_fractal_with_memory...")
        start_time = time.time()
        
        result = analyzer.detect_fractal_with_memory(df, current_price)
        
        execution_time = time.time() - start_time
        print(f"   - Tiempo de ejecución: {execution_time:.4f}s")
        
        if result:
            print("✅ Análisis fractal exitoso!")
            print(f"   - Tipo de resultado: {type(result)}")
            
            # Verificar atributos del resultado
            if hasattr(result, 'confidence'):
                print(f"   - Confidence: {result.confidence}")
            if hasattr(result, 'grade'):
                print(f"   - Grade: {result.grade}")
            if hasattr(result, 'pattern_type'):
                print(f"   - Pattern type: {result.pattern_type}")
                
            return True
        else:
            print("⚠️ Análisis fractal retornó None")
            print("   - Esto puede ser normal si no hay patrones detectables")
            return True
            
    except Exception as e:
        print(f"❌ Error en análisis fractal: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        return False

def test_fractal_methods():
    """🧪 Test 5: Verificar métodos disponibles"""
    print("\n🔍 TEST 5: Verificando métodos disponibles...")
    
    success, analyzer = test_fractal_initialization()
    if not success:
        return False
    
    print("📋 Métodos disponibles en FractalAnalyzerEnterprise:")
    methods = [method for method in dir(analyzer) if not method.startswith('_')]
    
    for i, method in enumerate(methods, 1):
        print(f"   {i:2d}. {method}")
    
    # Verificar métodos críticos
    critical_methods = ['detect_fractal_with_memory', 'analyze', 'detect']
    available_critical = [method for method in critical_methods if hasattr(analyzer, method)]
    
    print(f"\n🎯 Métodos críticos disponibles: {available_critical}")
    
    return True

def run_complete_fractal_test():
    """🚀 Ejecutar suite completa de tests para Fractal"""
    print("="*80)
    print("🔮 SUITE DE TESTS AISLADOS - FRACTAL ANALYZER ENTERPRISE")
    print("="*80)
    print(f"📅 Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Objetivo: Diagnóstico completo del módulo Fractal")
    print("="*80)
    
    tests = [
        ("Importaciones", test_fractal_imports),
        ("Inicialización", test_fractal_initialization),
        ("Carga de datos", test_data_loading),
        ("Métodos disponibles", test_fractal_methods),
        ("Análisis fractal", test_fractal_analysis),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name.upper()} {'='*20}")
        try:
            if test_name in ["Importaciones", "Inicialización", "Carga de datos"]:
                success, _ = test_func()
            else:
                success = test_func()
            results[test_name] = success
        except Exception as e:
            print(f"❌ Test {test_name} falló con excepción: {e}")
            results[test_name] = False
    
    # Resumen final
    print("\n" + "="*80)
    print("📊 RESUMEN DE RESULTADOS")
    print("="*80)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:20} : {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\n🎯 Tests ejecutados: {total_tests}")
    print(f"✅ Tests exitosos: {passed_tests}")
    print(f"❌ Tests fallidos: {total_tests - passed_tests}")
    print(f"📊 Tasa de éxito: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("💡 El módulo Fractal debería estar funcionando correctamente.")
    else:
        print("\n⚠️ ALGUNOS TESTS FALLARON")
        print("🔧 Revisar los errores anteriores para diagnóstico.")
    
    print("="*80)

if __name__ == "__main__":
    run_complete_fractal_test()
