#!/usr/bin/env python3
"""
🎯 TEST DE INTEGRACIÓN SIMPLE - SISTEMA ICT REAL
================================================

Test simplificado para verificar la integración con tu sistema ICT existente.
Este script prueba la conectividad básica con tus componentes reales.

Versión: v6.0.0
Fecha: 7 Agosto 2025
"""

import sys
import os
from pathlib import Path

# Configurar rutas para acceder a tu sistema
current_dir = Path(__file__).parent
project_root = current_dir.parent
main_project = project_root / "proyecto principal"

# Agregar rutas al path
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(main_project))

print("🚀 TEST DE INTEGRACIÓN - SISTEMA ICT REAL v6.0")
print("="*60)

def test_imports():
    """Probar importaciones de tu sistema"""
    
    test_results = {}
    
    # Test 1: Sistema de logging
    print("\n📝 PROBANDO SISTEMA DE LOGGING...")
    try:
        from sistema.logging_interface import enviar_senal_log
        enviar_senal_log("INFO", "✅ Sistema de logging cargado correctamente", "test", "integration")
        test_results["logging"] = "✅ DISPONIBLE"
    except ImportError as e:
        print(f"   ⚠️ Sistema de logging no encontrado: {e}")
        test_results["logging"] = "❌ NO DISPONIBLE"
        # Crear función dummy
        def enviar_senal_log(level, message, module="test", category="system"):
            print(f"[{level}] {category}.{module}: {message}")
    
    # Test 2: MT5 Data Manager
    print("\n📊 PROBANDO MT5 DATA MANAGER...")
    try:
        from utils.mt5_data_manager import MT5DataManager, get_mt5_manager
        mt5_manager = get_mt5_manager()
        print("   ✅ MT5DataManager importado correctamente")
        test_results["mt5_manager"] = "✅ DISPONIBLE"
    except ImportError as e:
        print(f"   ⚠️ MT5DataManager no encontrado: {e}")
        test_results["mt5_manager"] = "❌ NO DISPONIBLE"
    
    # Test 3: POI System
    print("\n🎯 PROBANDO SISTEMA POI...")
    try:
        from core.poi_system.poi_detector import POIDetector
        from core.poi_system.poi_scoring_engine import POIScoringEngine
        poi_detector = POIDetector()
        poi_scorer = POIScoringEngine()
        print("   ✅ Sistema POI importado correctamente")
        test_results["poi_system"] = "✅ DISPONIBLE"
    except ImportError as e:
        print(f"   ⚠️ Sistema POI no encontrado: {e}")
        test_results["poi_system"] = "❌ NO DISPONIBLE"
    
    # Test 4: ICT Engine
    print("\n🧠 PROBANDO ICT ENGINE...")
    try:
        from core.ict_engine.ict_detector import ICTDetector
        from core.ict_engine.pattern_analyzer import ICTPatternAnalyzer
        from core.ict_engine.confidence_engine import ConfidenceEngine
        from core.ict_engine.veredicto_engine_v4 import VeredictoEngine
        
        ict_detector = ICTDetector()
        pattern_analyzer = ICTPatternAnalyzer()
        confidence_engine = ConfidenceEngine()
        veredicto_engine = VeredictoEngine()
        
        print("   ✅ ICT Engine importado correctamente")
        test_results["ict_engine"] = "✅ DISPONIBLE"
    except ImportError as e:
        print(f"   ⚠️ ICT Engine no encontrado: {e}")
        test_results["ict_engine"] = "❌ NO DISPONIBLE"
    
    return test_results

def test_basic_functionality():
    """Probar funcionalidad básica de los componentes disponibles"""
    
    print(f"\n🔧 PROBANDO FUNCIONALIDAD BÁSICA...")
    
    functional_tests = {}
    
    try:
        # Test POI Detection
        from core.poi_system.poi_detector import POIDetector
        poi_detector = POIDetector()
        
        # Crear datos de prueba simples
        import pandas as pd
        import numpy as np
        
        # Datos OHLC de prueba
        test_data = pd.DataFrame({
            'time': pd.date_range('2024-01-01', periods=100, freq='15T'),
            'open': np.random.uniform(1.0900, 1.1100, 100),
            'high': np.random.uniform(1.0950, 1.1150, 100),
            'low': np.random.uniform(1.0850, 1.1050, 100),
            'close': np.random.uniform(1.0900, 1.1100, 100),
            'volume': np.random.uniform(1000, 5000, 100)
        })
        
        # Ajustar high/low para ser coherentes
        test_data['high'] = test_data[['open', 'close']].max(axis=1) + np.random.uniform(0, 0.001, 100)
        test_data['low'] = test_data[['open', 'close']].min(axis=1) - np.random.uniform(0, 0.001, 100)
        
        print("   📊 Datos de prueba creados")
        
        # Probar detección POI
        pois = poi_detector.detect_poi(test_data, 'M15')
        print(f"   🎯 POIs detectados: {len(pois) if pois else 0}")
        functional_tests["poi_detection"] = "✅ FUNCIONAL"
        
    except Exception as e:
        print(f"   ❌ Error en test POI: {e}")
        functional_tests["poi_detection"] = "❌ ERROR"
    
    try:
        # Test ICT Detection
        from core.ict_engine.ict_detector import ICTDetector
        ict_detector = ICTDetector()
        
        patterns = ict_detector.detect_patterns(test_data, 'M15')
        print(f"   🧠 Patrones ICT detectados: {len(patterns) if patterns else 0}")
        functional_tests["ict_detection"] = "✅ FUNCIONAL"
        
    except Exception as e:
        print(f"   ❌ Error en test ICT: {e}")
        functional_tests["ict_detection"] = "❌ ERROR"
    
    return functional_tests

def test_backtesting_readiness():
    """Verificar que el sistema está listo para backtesting"""
    
    print(f"\n⚡ VERIFICANDO PREPARACIÓN PARA BACKTESTING...")
    
    readiness_score = 0
    total_components = 6
    
    # Verificar componentes esenciales
    try:
        from sistema.logging_interface import enviar_senal_log
        print("   ✅ Sistema de logging: LISTO")
        readiness_score += 1
    except:
        print("   ⚠️ Sistema de logging: NO DISPONIBLE")
    
    try:
        from utils.mt5_data_manager import get_mt5_manager
        print("   ✅ MT5DataManager: LISTO")
        readiness_score += 1
    except:
        print("   ⚠️ MT5DataManager: NO DISPONIBLE")
    
    try:
        from core.poi_system.poi_detector import POIDetector
        print("   ✅ POIDetector: LISTO")
        readiness_score += 1
    except:
        print("   ⚠️ POIDetector: NO DISPONIBLE")
    
    try:
        from core.ict_engine.ict_detector import ICTDetector
        print("   ✅ ICTDetector: LISTO")
        readiness_score += 1
    except:
        print("   ⚠️ ICTDetector: NO DISPONIBLE")
    
    try:
        from core.ict_engine.confidence_engine import ConfidenceEngine
        print("   ✅ ConfidenceEngine: LISTO")
        readiness_score += 1
    except:
        print("   ⚠️ ConfidenceEngine: NO DISPONIBLE")
    
    try:
        from core.ict_engine.veredicto_engine_v4 import VeredictoEngine
        print("   ✅ VeredictoEngine: LISTO")
        readiness_score += 1
    except:
        print("   ⚠️ VeredictoEngine: NO DISPONIBLE")
    
    readiness_percentage = (readiness_score / total_components) * 100
    
    print(f"\n📊 PUNTUACIÓN DE PREPARACIÓN: {readiness_score}/{total_components} ({readiness_percentage:.1f}%)")
    
    if readiness_percentage >= 80:
        print("✅ SISTEMA LISTO PARA BACKTESTING REAL")
        return True
    elif readiness_percentage >= 50:
        print("⚠️ SISTEMA PARCIALMENTE LISTO - ALGUNOS COMPONENTES FALTAN")
        return False
    else:
        print("❌ SISTEMA NO LISTO - MUCHOS COMPONENTES FALTAN")
        return False

def main():
    """Función principal del test"""
    
    print("🔍 Iniciando verificación de tu sistema ICT...")
    print(f"📁 Directorio de trabajo: {Path.cwd()}")
    print(f"📁 Proyecto principal: {main_project}")
    
    # Test 1: Importaciones
    import_results = test_imports()
    
    # Test 2: Funcionalidad básica
    functional_results = test_basic_functionality()
    
    # Test 3: Preparación para backtesting
    is_ready = test_backtesting_readiness()
    
    # Resumen final
    print("\n" + "="*60)
    print("📋 RESUMEN DE RESULTADOS")
    print("="*60)
    
    print("\n🔧 COMPONENTES IMPORTADOS:")
    for component, status in import_results.items():
        print(f"   {component}: {status}")
    
    print("\n⚡ PRUEBAS FUNCIONALES:")
    for test, status in functional_results.items():
        print(f"   {test}: {status}")
    
    print(f"\n🎯 ESTADO GENERAL:")
    if is_ready:
        print("   ✅ SISTEMA LISTO PARA BACKTESTING REAL")
        print("   🚀 Puedes proceder con la integración completa")
    else:
        print("   ⚠️ SISTEMA REQUIERE AJUSTES")
        print("   🔧 Revisar componentes faltantes antes de continuar")
    
    print("\n" + "="*60)
    
    return is_ready

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("🎉 TEST DE INTEGRACIÓN COMPLETADO EXITOSAMENTE")
        else:
            print("⚠️ TEST COMPLETADO CON ADVERTENCIAS")
    except Exception as e:
        print(f"❌ ERROR DURANTE EL TEST: {e}")
        import traceback
        traceback.print_exc()
