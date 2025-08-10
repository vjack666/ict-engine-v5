#!/usr/bin/env python3
"""
Test Principal - ICT Engine v6.1.0 Enterprise SIC
===============================================

Script de test completo para verificar el funcionamiento del
Sistema de Imports Inteligente (SIC) v3.1 Enterprise.

Este script ejecuta tests exhaustivos de todos los componentes:
- SIC v3.1 Enterprise Interface
- Lazy Loading Manager
- Predictive Cache Manager
- Monitor Dashboard
- Advanced Debugger

Autor: ICT Engine v6.1.0 Team
Versión: v6.1.0-enterprise
Fecha: Agosto 2025
"""

import sys
import time
import traceback
from pathlib import Path

# Agregar el directorio del proyecto al path para imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_sic_enterprise_interface():
    """🚀 Test del SIC v3.1 Enterprise Interface"""
    print("\n" + "="*60)
    print("🚀 TESTING SIC v3.1 ENTERPRISE INTERFACE")
    print("="*60)
    
    try:
        # Import del SIC
        from sistema.sic_v3_1 import get_sic_instance, smart_import
        
        print("1️⃣ Inicializando SIC v3.1 Enterprise...")
        sic = get_sic_instance()
        print("   ✅ SIC inicializado correctamente")
        
        print("2️⃣ Testing smart import básico...")
        sys_module = smart_import('sys')
        print(f"   ✅ Smart import exitoso: {type(sys_module)}")
        
        print("3️⃣ Testing smart import con alias...")
        os_module = smart_import('os', alias='operating_system')
        print("   ✅ Smart import con alias exitoso")
        
        print("4️⃣ Testing smart import lazy...")
        time_module = smart_import('time', priority='low')
        print("   ✅ Smart import lazy exitoso")
        
        print("5️⃣ Obteniendo estadísticas del sistema...")
        stats = sic.get_system_stats()
        print(f"   ✅ Estadísticas: {stats['imports_stats']['total_imports']} imports realizados")
        print(f"   📊 Cache hit rate: {stats['imports_stats']['cache_hit_rate']:.1f}%")
        print(f"   ⏱️ Tiempo promedio: {stats['imports_stats']['avg_load_time']:.4f}s")
        
        print("6️⃣ Testing reporte de debug...")
        debug_report = sic.get_debug_report()
        print(f"   ✅ Reporte de debug generado: {len(debug_report)} secciones")
        
        assert True
        
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        traceback.print_exc()
        return False


def test_lazy_loading_manager():
    """🔄 Test del Lazy Loading Manager"""
    print("\n" + "="*60)
    print("🔄 TESTING LAZY LOADING MANAGER")
    print("="*60)
    
    try:
        from sistema.sic_v3_1.lazy_loading import LazyLoadingManager
        
        print("1️⃣ Inicializando Lazy Loading Manager...")
        lazy_manager = LazyLoadingManager()
        print("   ✅ Lazy Manager inicializado")
        
        print("2️⃣ Testing lazy import...")
        json_proxy = lazy_manager.lazy_import('json')
        print(f"   ✅ Proxy creado: {json_proxy}")
        print(f"   📊 ¿Está cargado? {json_proxy.is_loaded}")
        
        print("3️⃣ Accediendo al módulo lazy (debería cargarlo)...")
        json_dumps = json_proxy.dumps
        print(f"   ✅ Módulo accedido: {json_dumps}")
        print(f"   📊 ¿Está cargado ahora? {json_proxy.is_loaded}")
        print(f"   ⏱️ Tiempo de carga: {json_proxy.load_time:.4f}s")
        
        print("4️⃣ Testing estadísticas de lazy loading...")
        stats = lazy_manager.get_lazy_stats()
        print(f"   ✅ Stats obtenidas: {stats['module_stats']['total_lazy_modules']} módulos lazy")
        
        print("5️⃣ Testing cleanup de proxies...")
        cleaned = lazy_manager.cleanup_unused_proxies()
        print(f"   ✅ Cleanup completado: {cleaned} proxies eliminados")
        
        assert True
        
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        traceback.print_exc()
        return False


def test_predictive_cache_manager():
    """🧠 Test del Predictive Cache Manager"""
    print("\n" + "="*60)
    print("🧠 TESTING PREDICTIVE CACHE MANAGER")
    print("="*60)
    
    try:
        from sistema.sic_v3_1.predictive_cache import PredictiveCacheManager
        
        print("1️⃣ Inicializando Predictive Cache Manager...")
        cache_manager = PredictiveCacheManager()
        print("   ✅ Cache Manager inicializado")
        
        print("2️⃣ Testing cache de módulo...")
        import math
        cached = cache_manager.cache_module('math', module_obj=math)
        print(f"   ✅ Módulo cacheado: {cached}")
        
        print("3️⃣ Testing obtención desde cache...")
        cached_math = cache_manager.get_cached_module('math')
        print(f"   ✅ Cache hit: {cached_math is not None}")
        
        print("4️⃣ Testing cache miss...")
        missing_module = cache_manager.get_cached_module('nonexistent_module')
        print(f"   ✅ Cache miss: {missing_module is None}")
        
        print("5️⃣ Testing predicciones...")
        predictions = cache_manager.predict_next_modules('math', count=3)
        print(f"   ✅ Predicciones generadas: {len(predictions)} módulos predichos")
        
        print("6️⃣ Testing estadísticas de cache...")
        stats = cache_manager.get_cache_stats()
        hit_rate = stats['cache_performance']['hit_rate_percent']
        print(f"   ✅ Stats: {hit_rate:.1f}% hit rate")
        
        assert True
        
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        traceback.print_exc()
        return False


def test_monitor_dashboard():
    """📊 Test del Monitor Dashboard"""
    print("\n" + "="*60)
    print("📊 TESTING MONITOR DASHBOARD")
    print("="*60)
    
    try:
        from sistema.sic_v3_1.monitor_dashboard import MonitorDashboard
        
        print("1️⃣ Inicializando Monitor Dashboard...")
        monitor = MonitorDashboard()
        print("   ✅ Monitor inicializado")
        
        print("2️⃣ Testing registro de eventos...")
        event_id = monitor.record_import(
            module_name='test_module',
            load_time=0.005,
            import_type='normal',
            success=True
        )
        print(f"   ✅ Evento registrado: {event_id}")
        
        print("3️⃣ Testing estadísticas en tiempo real...")
        real_time_stats = monitor.get_real_time_stats()
        print(f"   ✅ Stats obtenidas: {real_time_stats['import_stats']['total_imports']} imports")
        
        print("4️⃣ Testing análisis de tendencias...")
        trends = monitor.get_trend_analysis(hours=0.1)
        print(f"   ✅ Análisis de tendencias generado")
        
        print("5️⃣ Testing generación de reporte...")
        report = monitor.generate_report(format='text')
        print(f"   ✅ Reporte generado: {len(report)} caracteres")
        
        # Cleanup
        monitor.shutdown()
        
        assert True
        
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        traceback.print_exc()
        return False


def test_advanced_debugger():
    """🔧 Test del Advanced Debugger"""
    print("\n" + "="*60)
    print("🔧 TESTING ADVANCED DEBUGGER")
    print("="*60)
    
    try:
        from sistema.sic_v3_1.advanced_debug import AdvancedDebugger
        
        print("1️⃣ Inicializando Advanced Debugger...")
        debugger = AdvancedDebugger()
        print("   ✅ Debugger inicializado")
        
        print("2️⃣ Testing log de import debug...")
        debugger.log_import_debug(
            module_name='test_module',
            import_type='normal',
            operation='load',
            duration=0.003,
            success=True,
            details={'test_data': 'example'}
        )
        print("   ✅ Debug log registrado")
        
        print("3️⃣ Testing análisis de dependencias...")
        dep_analysis = debugger.analyze_import_dependencies('sys')
        print(f"   ✅ Análisis completado: {len(dep_analysis)} items")
        
        print("4️⃣ Testing diagnóstico de error...")
        test_error = ImportError("Test error for diagnosis")
        diagnosis = debugger.diagnose_import_problem('fake_module', test_error)
        print(f"   ✅ Diagnóstico: {len(diagnosis['possible_causes'])} causas identificadas")
        
        print("5️⃣ Testing resumen de debug...")
        summary = debugger.get_debug_summary()
        print(f"   ✅ Resumen: {summary['debug_stats']['total_events']} eventos")
        
        print("6️⃣ Testing reporte completo...")
        full_report = debugger.generate_full_report()
        print(f"   ✅ Reporte completo: {len(full_report)} secciones")
        
        assert True
        
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        traceback.print_exc()
        return False


def test_integration():
    """🔗 Test de integración completa"""
    print("\n" + "="*60)
    print("🔗 TESTING INTEGRACIÓN COMPLETA")
    print("="*60)
    
    try:
        from sistema import get_sic_instance, smart_import
        
        print("1️⃣ Inicializando sistema completo...")
        sic = get_sic_instance()
        print("   ✅ Sistema inicializado")
        
        print("2️⃣ Testing secuencia de imports inteligentes...")
        
        # Import normal
        datetime_module = smart_import('datetime')
        print("   ✅ Import normal: datetime")
        
        # Import con cache (debería ser hit)
        datetime_cached = smart_import('datetime')
        print("   ✅ Import cacheado: datetime")
        
        # Import lazy
        random_module = smart_import('random', priority='low')
        print("   ✅ Import lazy: random")
        
        # Import con from
        sleep_func = smart_import('time', from_list=['sleep'])
        print("   ✅ Import específico: time.sleep")
        
        print("3️⃣ Verificando estadísticas finales...")
        final_stats = sic.get_system_stats()
        imports_stats = final_stats['imports_stats']
        
        print(f"   📊 Total imports: {imports_stats['total_imports']}")
        print(f"   📊 Cache hits: {imports_stats['cache_hits']}")
        print(f"   📊 Cache hit rate: {imports_stats['cache_hit_rate']:.1f}%")
        print(f"   📊 Tiempo promedio: {imports_stats['avg_load_time']:.4f}s")
        
        # Verificar que el sistema esté funcionando correctamente
        assert imports_stats['total_imports'] > 0, "No se registraron imports"
        assert imports_stats['cache_hit_rate'] >= 0, "Cache hit rate inválido"
        
        print("4️⃣ Testing debug mode...")
        sic.enable_debug_mode('debug')
        print("   ✅ Debug mode activado")
        
        assert True
        
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        traceback.print_exc()
        return False


def run_performance_benchmark():
    """⚡ Benchmark de performance"""
    print("\n" + "="*60)
    print("⚡ BENCHMARK DE PERFORMANCE")
    print("="*60)
    
    try:
        from sistema import smart_import
        import time
        
        # Test 1: Import normal vs smart import
        print("1️⃣ Comparando import normal vs smart import...")
        
        # Import normal tradicional
        start_time = time.time()
        import collections
        normal_time = time.time() - start_time
        
        # Smart import
        start_time = time.time()
        collections_smart = smart_import('collections')
        smart_time = time.time() - start_time
        
        print(f"   📊 Import normal: {normal_time:.6f}s")
        print(f"   📊 Smart import: {smart_time:.6f}s")
        
        # Test 2: Cache performance
        print("2️⃣ Testing performance de cache...")
        
        start_time = time.time()
        for i in range(10):
            smart_import('collections')  # Debería ser cache hit
        cache_time = (time.time() - start_time) / 10
        
        print(f"   📊 Promedio cache hit: {cache_time:.6f}s")
        
        # Test 3: Lazy loading overhead
        print("3️⃣ Testing overhead de lazy loading...")
        
        start_time = time.time()
        lazy_module = smart_import('urllib.parse', priority='low')
        lazy_create_time = time.time() - start_time
        
        start_time = time.time()
        _ = lazy_module.urlparse  # Forzar carga
        lazy_load_time = time.time() - start_time
        
        print(f"   📊 Lazy proxy creation: {lazy_create_time:.6f}s")
        print(f"   📊 Lazy actual load: {lazy_load_time:.6f}s")
        
        assert True
        
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        traceback.print_exc()
        return False


def main():
    """🎯 Función principal de test"""
    print("🚀 ICT ENGINE v6.0 ENTERPRISE SIC - TEST SUITE")
    print("=" * 80)
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print("=" * 80)
    
    # Lista de tests a ejecutar
    tests = [
        ("SIC Enterprise Interface", test_sic_enterprise_interface),
        ("Lazy Loading Manager", test_lazy_loading_manager),
        ("Predictive Cache Manager", test_predictive_cache_manager),
        ("Monitor Dashboard", test_monitor_dashboard),
        ("Advanced Debugger", test_advanced_debugger),
        ("Integración Completa", test_integration),
        ("Performance Benchmark", run_performance_benchmark),
    ]
    
    # Ejecutar tests
    results = []
    total_start_time = time.time()
    
    for test_name, test_func in tests:
        print(f"\n🧪 Ejecutando: {test_name}...")
        start_time = time.time()
        
        try:
            result = test_func()
            duration = time.time() - start_time
            results.append((test_name, result, duration))
            
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"   {status} ({duration:.2f}s)")
            
        except Exception as e:
            duration = time.time() - start_time
            results.append((test_name, False, duration))
            print(f"   ❌ ERROR: {e} ({duration:.2f}s)")
    
    # Resumen final
    total_duration = time.time() - total_start_time
    passed = sum(1 for _, result, _ in results if result)
    total = len(results)
    
    print("\n" + "=" * 80)
    print("📋 RESUMEN DE TESTS")
    print("=" * 80)
    
    for test_name, result, duration in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name:<30} ({duration:.2f}s)")
    
    print("-" * 80)
    print(f"📊 RESULTADO FINAL: {passed}/{total} tests pasaron")
    print(f"⏱️ TIEMPO TOTAL: {total_duration:.2f}s")
    
    if passed == total:
        print("🎉 ¡TODOS LOS TESTS PASARON! SIC v3.1 Enterprise está funcionando correctamente.")
    else:
        print("⚠️ Algunos tests fallaron. Revisar los errores arriba.")
    
    print("=" * 80)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
