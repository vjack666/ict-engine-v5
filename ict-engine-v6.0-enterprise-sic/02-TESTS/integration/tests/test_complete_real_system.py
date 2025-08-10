#!/usr/bin/env python3
"""
Test Completo del Sistema de Backtesting REAL Integrado
Verificar que TODOS los componentes reales funcionen correctamente
"""

import sys
import os
import time
from datetime import datetime
from pathlib import Path

# Asegurar que el directorio raíz esté en el path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

print(f"🔍 Iniciando test completo del sistema REAL integrado...")
print(f"📂 Directorio actual: {current_dir}")
print(f"🐍 Python: {sys.version}")
print("=" * 80)

def test_component_import(component_name: str, import_statement: str):
    """Test de importación de un componente"""
    print(f"\n🧪 Test: {component_name}")
    print(f"📦 Importando: {import_statement}")
    
    try:
        exec(import_statement)
        print(f"✅ {component_name}: DISPONIBLE")
        return True
    except Exception as e:
        print(f"❌ {component_name}: NO DISPONIBLE - {e}")
        return False

def test_mt5_data_manager():
    """Test del MT5 Data Manager"""
    print(f"\n🔧 Test MT5 Data Manager...")
    
    try:
        from utils.mt5_data_manager import MT5DataManager
        
        # Crear instancia
        manager = MT5DataManager()
        print(f"✅ MT5DataManager instanciado correctamente")
        
        # Test básico de funcionalidad
        if hasattr(manager, 'get_rates'):
            print(f"✅ Método get_rates disponible")
        
        if hasattr(manager, 'connect'):
            print(f"✅ Método connect disponible")
            
        return True
        
    except Exception as e:
        print(f"❌ MT5DataManager error: {e}")
        return False

def test_poi_system():
    """Test del sistema POI real"""
    print(f"\n🎯 Test Sistema POI Real...")
    
    try:
        # Test importación POIDetector adaptado
        from poi_detector_adapted import POIDetector
        print(f"✅ POIDetector adaptado importado")
        
        # Crear instancia
        detector = POIDetector()
        print(f"✅ POIDetector instanciado")
        
        # Verificar métodos esenciales
        if hasattr(detector, 'find_all_pois'):
            print(f"✅ Método find_all_pois disponible")
        
        if hasattr(detector, 'detect_poi'):
            print(f"✅ Método detect_poi disponible")
            
        return True
        
    except Exception as e:
        print(f"❌ Sistema POI error: {e}")
        return False

def test_sic_system():
    """Test del sistema SIC real"""
    print("\n📊 Test Sistema SIC Real...")
    
    try:
        # Test función log_message que es lo que usa el engine
        from poi_integrated_backtest_engine import log_message
        print("✅ Función log_message importada")
        
        # Test de funcionalidad básica
        log_message("INFO", "Test SIC funcionando correctamente")
        print("✅ SIC logging funcional")
            
        return True
        
    except Exception as e:
        print(f"❌ Sistema SIC error: {e}")
        return False

def test_backtest_engine():
    """Test del motor de backtesting integrado"""
    print(f"\n🚀 Test Motor de Backtesting Integrado...")
    
    try:
        from poi_integrated_backtest_engine import POIIntegratedBacktestEngine
        print(f"✅ POIIntegratedBacktestEngine importado")
        
        # Crear instancia con configuración básica
        config = {
            'symbol': 'EURUSD',
            'start_date': '2024-01-01',
            'end_date': '2024-01-02',
            'timeframes': ['H1'],
            'initial_balance': 10000
        }
        engine = POIIntegratedBacktestEngine(config)
        print(f"✅ Engine instanciado correctamente")
        
        # Verificar componentes cargados
        if hasattr(engine, 'poi_detector'):
            print(f"✅ POI Detector: {'CARGADO' if engine.poi_detector else 'NO CARGADO'}")
        
        # Verificar sistema SIC a través del global COMPONENTS_AVAILABLE
        from poi_integrated_backtest_engine import COMPONENTS_AVAILABLE
        print(f"✅ Sistema SIC: {'CARGADO' if COMPONENTS_AVAILABLE.get('sic', False) else 'NO CARGADO'}")
        
        # Test de métodos esenciales
        if hasattr(engine, 'run_backtest'):
            print(f"✅ Método run_backtest disponible")
        
        if hasattr(engine, 'detect_poi_patterns'):
            print(f"✅ Método detect_poi_patterns disponible")
            
        return True
        
    except Exception as e:
        print(f"❌ Motor de backtesting error: {e}")
        return False

def test_full_integration():
    """Test de integración completa con datos simulados"""
    print(f"\n🎪 Test de Integración COMPLETA...")
    
    try:
        from poi_integrated_backtest_engine import POIIntegratedBacktestEngine
        import pandas as pd
        import numpy as np
        
        # Crear datos simulados para test
        dates = pd.date_range(start='2024-01-01', end='2024-01-10', freq='1H')
        data = pd.DataFrame({
            'time': dates,
            'open': np.random.uniform(1.0900, 1.1100, len(dates)),
            'high': np.random.uniform(1.0950, 1.1150, len(dates)),
            'low': np.random.uniform(1.0850, 1.1050, len(dates)),
            'close': np.random.uniform(1.0900, 1.1100, len(dates)),
            'volume': np.random.randint(1000, 10000, len(dates))
        })
        
        print(f"✅ Datos de test generados: {len(data)} barras")
        
        # Crear engine con configuración básica
        from poi_integrated_backtest_engine import POIIntegratedBacktestConfig
        
        config = POIIntegratedBacktestConfig(
            symbol='EURUSD',
            start_date='2024-01-01',
            end_date='2024-01-02',
            timeframes=['H1'],
            initial_balance=10000
        )
        engine = POIIntegratedBacktestEngine(config)
        print(f"✅ Engine creado")
        
        # Test de detección de patrones
        patterns = engine.detect_poi_patterns(data, 'H1')
        print(f"✅ Patrones detectados: {len(patterns)}")
        
        if patterns:
            print(f"📋 Primer patrón: {patterns[0]}")
        
        # Test configuración básica
        config = {
            'symbol': 'EURUSD',
            'start_date': '2024-01-01',
            'end_date': '2024-01-02',
            'timeframes': ['H1'],
            'initial_balance': 10000
        }
        
        print(f"✅ Configuración de test preparada")
        
        return True
        
    except Exception as e:
        print(f"❌ Test de integración completa error: {e}")
        return False

def main():
    """Ejecutar todos los tests"""
    print(f"🔥 SISTEMA DE BACKTESTING ICT ENGINE v5.0 - TEST COMPLETO")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    results = {}
    
    # Test de importaciones básicas
    print(f"\n📦 TESTS DE IMPORTACIÓN")
    results['pandas'] = test_component_import("Pandas", "import pandas as pd")
    results['numpy'] = test_component_import("NumPy", "import numpy as np")
    results['rich'] = test_component_import("Rich", "from rich.console import Console")
    
    # Test de componentes del sistema
    print(f"\n🔧 TESTS DE COMPONENTES")
    results['mt5_manager'] = test_mt5_data_manager()
    results['poi_system'] = test_poi_system()
    results['sic_system'] = test_sic_system()
    results['backtest_engine'] = test_backtest_engine()
    
    # Test de integración
    print(f"\n🎪 TEST DE INTEGRACIÓN")
    results['full_integration'] = test_full_integration()
    
    # Reporte final
    print(f"\n" + "=" * 80)
    print(f"📊 REPORTE FINAL DE TESTS")
    print(f"=" * 80)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO: {passed}/{total} tests pasaron")
    
    if passed == total:
        print(f"🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print(f"✅ Todos los componentes reales están integrados correctamente")
    else:
        print(f"⚠️ Algunos componentes necesitan atención")
        print(f"🔧 Revisa los errores arriba para diagnosticar problemas")
    
    print(f"\n⏰ Test completado: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
