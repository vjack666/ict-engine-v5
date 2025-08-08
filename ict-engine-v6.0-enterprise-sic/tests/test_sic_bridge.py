#!/usr/bin/env python3
"""
🧪 TEST SIC BRIDGE - VALIDACIÓN DE INTEGRACIÓN INTELIGENTE
==========================================================

Test exhaustivo del SIC Bridge que conecta:
- SIC v3.1 (proyecto principal) - Sistema probado
- SIC v3.1 Enterprise (nuevo) - Optimizaciones

Ejecutar: python test_sic_bridge.py
"""

import sys
import time
import traceback
from pathlib import Path
from datetime import datetime

# Configurar path para imports
project_root = Path(__file__).parent if hasattr(Path(__file__), 'parent') else Path.cwd()
sys.path.insert(0, str(project_root))

def test_bridge_import():
    """Test 1: Validar import del SIC Bridge"""
    print("🧪 TEST 1: Validando import SIC Bridge...")
    try:
        from sistema.sic_bridge import SICBridge, get_sic_bridge
        print("✅ Import SIC Bridge: SUCCESS")
        return True, SICBridge
    except Exception as e:
        print(f"❌ Import SIC Bridge: FAILED - {e}")
        traceback.print_exc()
        return False, None

def test_bridge_instantiation(BridgeClass):
    """Test 2: Validar instanciación del bridge"""
    print("\n🧪 TEST 2: Validando instanciación SIC Bridge...")
    try:
        bridge = BridgeClass()
        print("✅ Instanciación SIC Bridge: SUCCESS")
        print(f"   Sistema activo: {bridge.active_system}")
        print(f"   SIC v3.1 disponible: {bridge.sic_v30 is not None}")
        print(f"   SIC v3.1 disponible: {bridge.sic_v31 is not None}")
        return True, bridge
    except Exception as e:
        print(f"❌ Instanciación SIC Bridge: FAILED - {e}")
        traceback.print_exc()
        return False, None

def test_bridge_functionality(bridge):
    """Test 3: Validar funcionalidad del bridge"""
    print("\n🧪 TEST 3: Validando funcionalidad SIC Bridge...")
    
    tests = {
        'get_all_functions': False,
        'smart_import': False,
        'get_performance_stats': False,
        'get_system_health': False
    }
    
    # Test get_all_functions
    try:
        functions = bridge.get_all_functions()
        if isinstance(functions, dict):
            tests['get_all_functions'] = True
            print(f"✅ get_all_functions: SUCCESS ({len(functions)} funciones)")
        else:
            print(f"❌ get_all_functions: Retorna {type(functions)}, esperaba dict")
    except Exception as e:
        print(f"❌ get_all_functions: ERROR - {e}")
    
    # Test smart_import
    try:
        # Intentar importar un módulo estándar
        import_result = bridge.smart_import('sys')
        if import_result:
            tests['smart_import'] = True
            print("✅ smart_import: SUCCESS")
        else:
            print("❌ smart_import: Retorna None")
    except Exception as e:
        print(f"❌ smart_import: ERROR - {e}")
    
    # Test get_performance_stats
    try:
        stats = bridge.get_performance_stats()
        if isinstance(stats, dict) and 'active_system' in stats:
            tests['get_performance_stats'] = True
            print("✅ get_performance_stats: SUCCESS")
            print(f"   Active system: {stats['active_system']}")
            print(f"   V3.0 calls: {stats['v30_calls']}")
            print(f"   V3.1 calls: {stats['v31_calls']}")
        else:
            print("❌ get_performance_stats: Formato incorrecto")
    except Exception as e:
        print(f"❌ get_performance_stats: ERROR - {e}")
    
    # Test get_system_health
    try:
        health = bridge.get_system_health()
        if isinstance(health, dict) and 'bridge_status' in health:
            tests['get_system_health'] = True
            print("✅ get_system_health: SUCCESS")
            print(f"   Bridge status: {health['bridge_status']}")
            print(f"   Functionality test: {health.get('functionality_test', 'N/A')}")
        else:
            print("❌ get_system_health: Formato incorrecto")
    except Exception as e:
        print(f"❌ get_system_health: ERROR - {e}")
    
    success_count = sum(tests.values())
    return success_count, tests

def test_bridge_compatibility():
    """Test 4: Validar compatibilidad con código existente"""
    print("\n🧪 TEST 4: Validando compatibilidad...")
    
    compatibility_tests = {
        'get_all_functions_global': False,
        'smart_import_global': False,
        'get_bridge_status': False
    }
    
    try:
        from sistema.sic_bridge import get_all_functions, smart_import, get_bridge_status
        
        # Test función global get_all_functions
        try:
            functions = get_all_functions()
            if isinstance(functions, dict):
                compatibility_tests['get_all_functions_global'] = True
                print("✅ Compatibility get_all_functions: SUCCESS")
            else:
                print("❌ Compatibility get_all_functions: Formato incorrecto")
        except Exception as e:
            print(f"❌ Compatibility get_all_functions: ERROR - {e}")
        
        # Test función global smart_import
        try:
            sys_module = smart_import('sys')
            if sys_module:
                compatibility_tests['smart_import_global'] = True
                print("✅ Compatibility smart_import: SUCCESS")
            else:
                print("❌ Compatibility smart_import: Retorna None")
        except Exception as e:
            print(f"❌ Compatibility smart_import: ERROR - {e}")
        
        # Test get_bridge_status
        try:
            status = get_bridge_status()
            if isinstance(status, dict) and 'bridge_status' in status:
                compatibility_tests['get_bridge_status'] = True
                print("✅ Compatibility get_bridge_status: SUCCESS")
            else:
                print("❌ Compatibility get_bridge_status: Formato incorrecto")
        except Exception as e:
            print(f"❌ Compatibility get_bridge_status: ERROR - {e}")
    
    except ImportError as e:
        print(f"❌ Import compatibility functions: FAILED - {e}")
    
    success_count = sum(compatibility_tests.values())
    return success_count, compatibility_tests

def test_bridge_performance():
    """Test 5: Benchmark de performance del bridge"""
    print("\n🧪 TEST 5: Benchmark de performance...")
    
    try:
        from sistema.sic_bridge import get_sic_bridge
        bridge = get_sic_bridge()
        
        # Benchmark multiple calls
        iterations = 10
        start_time = time.time()
        
        for i in range(iterations):
            functions = bridge.get_all_functions()
            health = bridge.get_system_health()
        
        total_time = time.time() - start_time
        avg_time = total_time / iterations
        
        print(f"⚡ Total time ({iterations} iterations): {total_time:.4f}s")
        print(f"⚡ Average time per call: {avg_time:.4f}s")
        print(f"⚡ Calls per second: {1/avg_time:.2f}")
        
        # Performance validation
        if avg_time < 0.01:
            rating = "EXCELLENT"
            print("✅ Performance: EXCELLENT (<0.01s per call)")
        elif avg_time < 0.05:
            rating = "GOOD"
            print("✅ Performance: GOOD (<0.05s per call)")
        elif avg_time < 0.1:
            rating = "ACCEPTABLE"
            print("⚠️ Performance: ACCEPTABLE (<0.1s per call)")
        else:
            rating = "SLOW"
            print("❌ Performance: SLOW (>0.1s per call)")
        
        return rating, {
            'total_time': total_time,
            'avg_time': avg_time,
            'calls_per_second': 1/avg_time,
            'iterations': iterations
        }
        
    except Exception as e:
        print(f"❌ Performance Benchmark: FAILED - {e}")
        return "FAILED", None

def generate_bridge_report(test_results):
    """Generar reporte completo del SIC Bridge"""
    print("\n" + "="*70)
    print("📊 REPORTE FINAL - SIC BRIDGE INTEGRATION")
    print("="*70)
    
    # Calcular score general
    total_tests = 5
    passed_tests = 0
    
    # Test 1: Import
    if test_results['import_success']:
        passed_tests += 1
        print("✅ TEST 1 - Import: PASSED")
    else:
        print("❌ TEST 1 - Import: FAILED")
    
    # Test 2: Instantiation
    if test_results['instantiation_success']:
        passed_tests += 1
        print("✅ TEST 2 - Instantiation: PASSED")
    else:
        print("❌ TEST 2 - Instantiation: FAILED")
    
    # Test 3: Functionality
    functionality_success = test_results['functionality_success_count']
    total_functionality = len(test_results['functionality_tests'])
    if functionality_success >= total_functionality * 0.8:  # 80% success rate
        passed_tests += 1
        print(f"✅ TEST 3 - Functionality: PASSED ({functionality_success}/{total_functionality})")
    else:
        print(f"❌ TEST 3 - Functionality: FAILED ({functionality_success}/{total_functionality})")
    
    # Test 4: Compatibility
    compatibility_success = test_results['compatibility_success_count']
    total_compatibility = len(test_results['compatibility_tests'])
    if compatibility_success >= total_compatibility * 0.8:  # 80% success rate
        passed_tests += 1
        print(f"✅ TEST 4 - Compatibility: PASSED ({compatibility_success}/{total_compatibility})")
    else:
        print(f"❌ TEST 4 - Compatibility: FAILED ({compatibility_success}/{total_compatibility})")
    
    # Test 5: Performance
    if test_results['performance_rating'] in ['EXCELLENT', 'GOOD']:
        passed_tests += 1
        print(f"✅ TEST 5 - Performance: PASSED ({test_results['performance_rating']})")
    else:
        print(f"❌ TEST 5 - Performance: FAILED ({test_results['performance_rating']})")
    
    # Score final
    success_percentage = (passed_tests / total_tests) * 100
    print(f"\n📊 SCORE FINAL: {passed_tests}/{total_tests} ({success_percentage:.1f}%)")
    
    # Veredicto
    if success_percentage >= 90:
        verdict = "🟢 EXCELLENT - Bridge listo para integración completa"
    elif success_percentage >= 80:
        verdict = "🟡 GOOD - Bridge funcional con issues menores"
    elif success_percentage >= 60:
        verdict = "🟠 ACCEPTABLE - Bridge básico, necesita mejoras"
    else:
        verdict = "🔴 FAILED - Bridge no funcional"
    
    print(f"\n🎯 VEREDICTO: {verdict}")
    
    # Detalles del bridge
    if test_results.get('bridge_instance'):
        bridge = test_results['bridge_instance']
        print(f"\n🔧 DETALLES DEL BRIDGE:")
        print(f"   Sistema activo: {getattr(bridge, 'active_system', 'N/A')}")
        print(f"   SIC v3.1: {'✅' if getattr(bridge, 'sic_v30', None) else '❌'}")
        print(f"   SIC v3.1: {'✅' if getattr(bridge, 'sic_v31', None) else '❌'}")
    
    return success_percentage, verdict

def main():
    """Función principal del test"""
    print("🚀 INICIANDO TEST COMPLETO - SIC BRIDGE INTEGRATION")
    print("="*70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Project Root: {project_root}")
    print("="*70)
    
    test_results = {}
    
    try:
        # Test 1: Import
        import_success, BridgeClass = test_bridge_import()
        test_results['import_success'] = import_success
        test_results['bridge_class'] = BridgeClass
        
        if not import_success:
            print("\n❌ CRITICAL: Import failed. Cannot continue with bridge tests.")
            return False
        
        # Test 2: Instantiation
        instantiation_success, bridge_instance = test_bridge_instantiation(BridgeClass)
        test_results['instantiation_success'] = instantiation_success
        test_results['bridge_instance'] = bridge_instance
        
        if not instantiation_success:
            print("\n❌ CRITICAL: Instantiation failed. Cannot continue with bridge tests.")
            return False
        
        # Test 3: Functionality
        functionality_success_count, functionality_tests = test_bridge_functionality(bridge_instance)
        test_results['functionality_success_count'] = functionality_success_count
        test_results['functionality_tests'] = functionality_tests
        
        # Test 4: Compatibility
        compatibility_success_count, compatibility_tests = test_bridge_compatibility()
        test_results['compatibility_success_count'] = compatibility_success_count
        test_results['compatibility_tests'] = compatibility_tests
        
        # Test 5: Performance
        performance_rating, performance_results = test_bridge_performance()
        test_results['performance_rating'] = performance_rating
        test_results['performance_results'] = performance_results
        
        # Generar reporte final
        success_percentage, verdict = generate_bridge_report(test_results)
        
        return success_percentage >= 80
        
    except Exception as e:
        print(f"\n💥 ERROR CRÍTICO durante test del bridge: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 SIC BRIDGE TEST EXITOSO")
        print("🚀 Bridge listo para FASE 2: Advanced Patterns Fusion")
        sys.exit(0)
    else:
        print("\n💥 SIC BRIDGE TEST FALLIDO")
        print("🔧 Revisar issues antes de continuar")
        sys.exit(1)
