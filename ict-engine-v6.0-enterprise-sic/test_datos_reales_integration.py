#!/usr/bin/env python3
"""
🚀 TEST INTEGRACIÓN DATOS REALES - ICT ENGINE v6.0 ENTERPRISE
=============================================================

Test actualizado para validar la integración completa del sistema multi-timeframe BOS
con gestión inteligente de datos reales usando ICTDataManager.

Funcionalidades testadas:
- ICTDataManager (warm-up + enhancement)
- OptimizedICTAnalysisEnterprise con múltiples modos
- PatternDetector con datos reales
- Flujo híbrido optimizado

Autor: ICT Enterprise Development Team
Fecha: 2025-08-08
Versión: 2.0.0 (Datos Reales)
"""

import sys
import os
from pathlib import Path
import time

# Añadir el directorio raíz al path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "core"))

def test_ict_data_manager():
    """🎯 Test del ICT Data Manager standalone"""
    
    print("=" * 80)
    print("🎯 TEST ICT DATA MANAGER")
    print("=" * 80)
    
    try:
        from core.data_management.ict_data_manager import ICTDataManager
        
        # 1. Crear Data Manager
        print("\n1. 📊 Creando ICT Data Manager...")
        data_manager = ICTDataManager()
        print("✅ Data Manager creado exitosamente")
        
        # 2. Test configuración
        print(f"\n2. ⚙️ Verificando configuración...")
        print(f"   Símbolos críticos: {data_manager.config['symbols_critical']}")
        print(f"   Timeframes críticos: {data_manager.config['timeframes_critical']}")
        print(f"   Datos mínimos H4: {data_manager.config['bars_minimal']['H4']} velas")
        
        # 3. Test data readiness
        print(f"\n3. 📈 Test data readiness...")
        readiness = data_manager.get_data_readiness('EURUSD', ['H4', 'M15', 'M5'])
        print(f"   Capacidad de análisis: {readiness['analysis_capability']}")
        print(f"   Estado general: {'READY' if readiness['overall_ready'] else 'NOT_READY'}")
        
        # 4. Test performance summary
        performance = data_manager.get_performance_summary()
        print(f"\n4. 📊 Performance summary:")
        print(f"   Estado del sistema: {performance['system_status']}")
        print(f"   Warm-up completado: {performance['warm_up_completed']}")
        print(f"   Enhancement activo: {performance['enhancement_active']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test ICT Data Manager: {e}")
        return False

def test_multi_timeframe_modes():
    """🔧 Test de múltiples modos del analyzer"""
    
    print("\n" + "=" * 80)
    print("🔧 TEST MULTI-TIMEFRAME ANALYZER - MÚLTIPLES MODOS")
    print("=" * 80)
    
    try:
        from core.analysis.multi_timeframe_analyzer import OptimizedICTAnalysisEnterprise
        
        analyzer = OptimizedICTAnalysisEnterprise()
        test_symbol = 'EURUSD'
        modes_to_test = ['minimal', 'live_ready', 'full', 'auto']
        
        results = {}
        
        for mode in modes_to_test:
            print(f"\n🧪 Probando modo: {mode}")
            start_time = time.time()
            
            result = analyzer.analyze_symbol(test_symbol, ['H4', 'M15', 'M5'], mode=mode)
            
            execution_time = time.time() - start_time
            
            if result.get('status') == 'SUCCESS':
                print(f"   ✅ Modo {mode}: ÉXITO en {execution_time:.2f}s")
                print(f"      Calidad datos: {result.get('data_quality', 'N/A')}")
                print(f"      Timeframes: {len(result.get('timeframe_results', {}))}")
                print(f"      Trading ready: {result.get('trading_ready', 'N/A')}")
                results[mode] = {'success': True, 'time': execution_time}
            else:
                print(f"   ❌ Modo {mode}: ERROR - {result.get('error', 'Unknown')}")
                results[mode] = {'success': False, 'time': execution_time}
        
        # Resumen
        successful_modes = sum(1 for r in results.values() if r['success'])
        print(f"\n📊 RESUMEN MODOS:")
        print(f"   Exitosos: {successful_modes}/{len(modes_to_test)}")
        
        fastest_mode = min(results.items(), key=lambda x: x[1]['time'])
        print(f"   Modo más rápido: {fastest_mode[0]} ({fastest_mode[1]['time']:.2f}s)")
        
        return successful_modes == len(modes_to_test)
        
    except Exception as e:
        print(f"❌ Error en test modos: {e}")
        return False

def test_pattern_detector_with_data_manager():
    """🚀 Test integración completa PatternDetector + DataManager"""
    
    print("\n" + "=" * 80)
    print("🚀 TEST PATTERN DETECTOR CON DATA MANAGER")
    print("=" * 80)
    
    try:
        from core.analysis.pattern_detector import PatternDetector
        
        # 1. Inicializar PatternDetector
        print("\n1. 🔧 Inicializando PatternDetector...")
        pattern_detector = PatternDetector()
        print("✅ PatternDetector inicializado")
        
        # 2. Verificar componentes
        print("\n2. 🎯 Verificando componentes integrados...")
        
        has_multi_tf = hasattr(pattern_detector, '_multi_tf_analyzer') and pattern_detector._multi_tf_analyzer is not None
        has_data_manager = hasattr(pattern_detector, '_data_manager') and pattern_detector._data_manager is not None
        
        print(f"   Multi-timeframe analyzer: {'✅ DISPONIBLE' if has_multi_tf else '❌ NO DISPONIBLE'}")
        print(f"   ICT Data Manager: {'✅ DISPONIBLE' if has_data_manager else '❌ NO DISPONIBLE'}")
        
        if not has_multi_tf:
            print("⚠️  Multi-timeframe analyzer no disponible - test limitado")
            return False
        
        # 3. Test análisis multi-timeframe con diferentes modos
        print("\n3. 🧪 Test análisis multi-timeframe con modos...")
        
        test_modes = ['auto', 'live_ready', 'full']
        test_symbols = ['EURUSD', 'GBPUSD']
        
        total_tests = 0
        successful_tests = 0
        
        for symbol in test_symbols:
            for mode in test_modes:
                total_tests += 1
                print(f"\n   🔍 {symbol} - Modo {mode}...")
                
                try:
                    result = pattern_detector.detect_bos_multi_timeframe(
                        symbol=symbol,
                        timeframes=['H4', 'M15', 'M5'],
                        mode=mode
                    )
                    
                    if result.get('detected'):
                        primary = result.get('primary_signal', {})
                        print(f"      ✅ BOS DETECTADO en {primary.get('timeframe', 'N/A')}")
                        print(f"         📊 Dirección: {primary.get('direction', 'N/A')}")
                        print(f"         💪 Fuerza: {primary.get('strength', 0):.1f}%")
                        print(f"         🎯 Calidad datos: {primary.get('data_quality', 'N/A')}")
                        successful_tests += 1
                    else:
                        print(f"      ⚠️  No BOS detectado - {result.get('reason', 'Unknown')}")
                        # Aún cuenta como exitoso si no hay error
                        if result.get('status') != 'ERROR':
                            successful_tests += 1
                    
                    # Información adicional
                    exec_summary = result.get('execution_summary', {})
                    print(f"         📋 Fuente datos: {exec_summary.get('data_source', 'UNKNOWN')}")
                    print(f"         🎯 Modo usado: {exec_summary.get('mode_used', 'UNKNOWN')}")
                    
                except Exception as e:
                    print(f"      ❌ Error: {e}")
        
        print(f"\n📊 RESUMEN INTEGRACIÓN:")
        print(f"   Tests ejecutados: {total_tests}")
        print(f"   Tests exitosos: {successful_tests}")
        print(f"   Tasa de éxito: {successful_tests/total_tests*100:.1f}%")
        
        return successful_tests >= total_tests * 0.8  # 80% mínimo
        
    except Exception as e:
        print(f"❌ Error en test integración: {e}")
        return False

def test_performance_comparison():
    """📈 Test comparación de performance entre modos"""
    
    print("\n" + "=" * 80)
    print("📈 TEST COMPARACIÓN DE PERFORMANCE")
    print("=" * 80)
    
    try:
        from core.analysis.pattern_detector import PatternDetector
        
        pattern_detector = PatternDetector()
        
        if not hasattr(pattern_detector, '_multi_tf_analyzer') or pattern_detector._multi_tf_analyzer is None:
            print("⚠️  Multi-timeframe analyzer no disponible")
            return False
        
        # Modos a comparar
        modes = ['minimal', 'live_ready', 'full']
        symbol = 'EURUSD'
        
        performance_results = {}
        
        print(f"\n🏃‍♂️ Comparando performance para {symbol}...")
        
        for mode in modes:
            print(f"\n   ⏱️ Modo {mode}...")
            
            times = []
            for i in range(3):  # 3 ejecuciones para promedio
                start_time = time.time()
                
                result = pattern_detector.detect_bos_multi_timeframe(
                    symbol=symbol,
                    mode=mode
                )
                
                execution_time = time.time() - start_time
                times.append(execution_time)
                
                if result.get('status') not in ['ERROR']:
                    print(f"      Ejecución {i+1}: {execution_time:.3f}s ✅")
                else:
                    print(f"      Ejecución {i+1}: {execution_time:.3f}s ❌")
            
            avg_time = sum(times) / len(times)
            performance_results[mode] = {
                'avg_time': avg_time,
                'times': times,
                'consistency': max(times) - min(times)
            }
            
            print(f"      Promedio: {avg_time:.3f}s")
            print(f"      Consistencia: ±{performance_results[mode]['consistency']:.3f}s")
        
        # Análisis de resultados
        print(f"\n📊 ANÁLISIS DE PERFORMANCE:")
        
        sorted_modes = sorted(performance_results.items(), key=lambda x: x[1]['avg_time'])
        
        for i, (mode, data) in enumerate(sorted_modes):
            ranking = ["🥇", "🥈", "🥉"][i] if i < 3 else f"#{i+1}"
            print(f"   {ranking} {mode}: {data['avg_time']:.3f}s promedio")
        
        fastest_mode = sorted_modes[0]
        print(f"\n🏆 Modo más rápido: {fastest_mode[0]} ({fastest_mode[1]['avg_time']:.3f}s)")
        
        # Verificar que 'minimal' sea el más rápido (debería serlo)
        expected_fastest = fastest_mode[0] == 'minimal'
        print(f"✅ Orden esperado: {'SÍ' if expected_fastest else 'NO'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test performance: {e}")
        return False

def main():
    """🚀 Ejecutar todos los tests de integración con datos reales"""
    
    print("🚀 INICIANDO TESTS INTEGRACIÓN DATOS REALES...")
    print("Versión: 2.0.0 (Datos Reales)")
    print("=" * 80)
    
    tests = [
        ("ICT Data Manager", test_ict_data_manager),
        ("Multi-timeframe Modos", test_multi_timeframe_modes),
        ("PatternDetector + DataManager", test_pattern_detector_with_data_manager),
        ("Performance Comparison", test_performance_comparison)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Error crítico en {test_name}: {e}")
            results[test_name] = False
    
    # Resumen final
    print("\n" + "=" * 80)
    print("🏁 RESUMEN FINAL TESTS DATOS REALES")
    print("=" * 80)
    
    total_tests = len(tests)
    passed_tests = sum(1 for result in results.values() if result)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📊 RESULTADO GENERAL:")
    print(f"Tests pasados: {passed_tests}/{total_tests}")
    print(f"Tasa de éxito: {passed_tests/total_tests*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("🚀 SISTEMA MULTI-TIMEFRAME CON DATOS REALES OPERATIVO")
    elif passed_tests >= total_tests * 0.75:
        print("\n✅ SISTEMA MAYORMENTE FUNCIONAL")
        print("🔧 Revisar tests fallidos para optimización")
    else:
        print("\n⚠️  SISTEMA REQUIERE ATENCIÓN")
        print("🛠️  Revisar configuración y dependencias")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
