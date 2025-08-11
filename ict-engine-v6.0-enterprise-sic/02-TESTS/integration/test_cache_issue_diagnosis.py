#!/usr/bin/env python3
"""
🔍 DIAGNÓSTICO: CACHE VACÍO EN TODO #2
======================================

Investigar por qué el ICTDataManager muestra cache vacío cuando
AdvancedCandleDownloader SÍ está descargando datos reales de MT5.

SÍNTOMAS:
- ✅ MT5 conectado y descargando datos reales
- ✅ AdvancedCandleDownloader funciona (3000+ velas descargadas)
- ❌ ICTDataManager cache: 0 símbolos, 0% eficiencia
- ❌ Cobertura timeframes: 0.0% en todos

HIPÓTESIS:
1. Desconexión entre downloader y data manager
2. Los datos se descargan pero no se registran en el cache del manager
3. Issue en _update_data_status() o _execute_parallel_downloads()
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Configurar path para importaciones
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / '01-CORE'))

def main():
    """🔍 Diagnóstico completo del issue cache vacío"""
    
    print("🔍 DIAGNÓSTICO: CACHE VACÍO EN TODO #2")
    print("=" * 50)
    
    # Test 1: Verificar flujo de datos downloader -> manager
    print("\n📊 1. DIAGNÓSTICO FLUJO DE DATOS:")
    test_data_flow()
    
    # Test 2: Verificar warm_up cache
    print("\n🚀 2. TEST WARM-UP CACHE:")
    test_warmup_cache()
    
    # Test 3: Verificar método _update_data_status
    print("\n📈 3. TEST UPDATE DATA STATUS:")
    test_update_data_status()
    
    # Test 4: Test de warm_up con datos reales
    print("\n🔥 4. TEST WARM-UP CON DATOS REALES:")
    test_warmup_with_real_data()

def test_data_flow():
    """📊 Test del flujo de datos entre downloader y manager"""
    
    try:
        from core.data_management.ict_data_manager import ICTDataManager
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        
        print("   📥 Creando componentes...")
        downloader = AdvancedCandleDownloader()
        manager = ICTDataManager(downloader=downloader)
        
        print("   ✅ Componentes creados exitosamente")
        
        # Test directo del downloader
        print("   🔍 Test directo AdvancedCandleDownloader...")
        result = downloader.download_candles(
            symbol='EURUSD',
            timeframe='H4',
            bars_count=100,
            use_ict_optimal=True
        )
        
        if result and result.get('success', False):
            data_count = len(result.get('data', []))
            print(f"   ✅ Downloader directo: {data_count} velas descargadas")
            print(f"   📊 Source: {result.get('source', 'UNKNOWN')}")
            print(f"   📁 Saved to: {result.get('file_path', 'NO FILE')}")
        else:
            print(f"   ❌ Downloader directo falló: {result}")
        
        # Verificar estado del manager después del download directo
        print("   📊 Estado manager después de download directo:")
        cache_status = manager.get_multi_tf_cache_status()
        print(f"   📈 Símbolos en cache: {cache_status.get('total_symbols', 0)}")
        
        performance = manager.get_performance_summary()
        print(f"   📊 Data symbols count: {performance.get('data_symbols_count', 0)}")
        print(f"   🎯 System status: {performance.get('system_status', 'UNKNOWN')}")
        
    except Exception as e:
        print(f"   ❌ Error en test flujo de datos: {e}")

def test_warmup_cache():
    """🚀 Test específico del warm-up cache"""
    
    try:
        from core.data_management.ict_data_manager import ICTDataManager
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        
        print("   🚀 Ejecutando warm_up_cache...")
        downloader = AdvancedCandleDownloader()
        manager = ICTDataManager(downloader=downloader)
        
        # Ejecutar warm-up
        warmup_result = manager.warm_up_cache(
            symbols=['EURUSD'],
            timeframes=['H4']
        )
        
        print(f"   📊 Warm-up result:")
        print(f"     Success: {warmup_result.get('success', False)}")
        print(f"     Downloads: {warmup_result.get('successful_downloads', 0)}/{warmup_result.get('total_downloads', 0)}")
        print(f"     Time: {warmup_result.get('warm_up_time', 0):.2f}s")
        
        # Verificar resultados detallados
        if 'results' in warmup_result:
            print("   📋 Resultados detallados:")
            for key, result in warmup_result['results'].items():
                success = result.get('success', False)
                error = result.get('error', 'No error')
                print(f"     - {key}: {'✅' if success else '❌'} {error if not success else 'OK'}")
        
        # Verificar data_status interno
        print("   🔍 Verificando data_status interno...")
        if hasattr(manager, 'data_status'):
            print(f"   📊 data_status keys: {list(manager.data_status.keys())}")
            for symbol, timeframes in manager.data_status.items():
                print(f"     - {symbol}: {list(timeframes.keys())}")
                for tf, data_info in timeframes.items():
                    available = data_info.get('available', False)
                    bars = data_info.get('bars_count', 0)
                    print(f"       * {tf}: {'✅' if available else '❌'} ({bars} bars)")
        
    except Exception as e:
        print(f"   ❌ Error en test warm-up: {e}")

def test_update_data_status():
    """📈 Test específico de _update_data_status"""
    
    try:
        from core.data_management.ict_data_manager import ICTDataManager
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        
        print("   🔍 Test manual _update_data_status...")
        downloader = AdvancedCandleDownloader()
        manager = ICTDataManager(downloader=downloader)
        
        # Simular resultado de descarga exitosa
        mock_results = {
            'EURUSD_H4': {
                'success': True,
                'source': 'MT5_REAL',
                'task_info': {
                    'priority': 'CRITICAL',
                    'mode': 'test',
                    'bars_requested': 100,
                    'bars_received': 95
                },
                'data': ['dummy_data'] * 95  # Simular 95 velas
            }
        }
        
        print("   📊 Aplicando _update_data_status manualmente...")
        manager._update_data_status(mock_results)
        
        # Verificar que se actualizó
        print("   ✅ Verificando data_status después de update manual:")
        if 'EURUSD' in manager.data_status:
            eurusd_data = manager.data_status['EURUSD']
            if 'H4' in eurusd_data:
                h4_info = eurusd_data['H4']
                print(f"     ✅ EURUSD H4 registrado:")
                print(f"       - Available: {h4_info.get('available', False)}")
                print(f"       - Bars: {h4_info.get('bars_count', 0)}")
                print(f"       - Quality: {h4_info.get('quality', 'UNKNOWN')}")
                print(f"       - Source: {h4_info.get('source', 'UNKNOWN')}")
            else:
                print("     ❌ H4 no encontrado en EURUSD data")
        else:
            print("     ❌ EURUSD no encontrado en data_status")
        
        # Verificar cache status después del update
        cache_status = manager.get_multi_tf_cache_status()
        print(f"   📈 Cache status después de update manual:")
        print(f"     - Total symbols: {cache_status.get('total_symbols', 0)}")
        print(f"     - Cache efficiency: {cache_status.get('cache_efficiency', {}).get('efficiency_percentage', 0):.1f}%")
        
    except Exception as e:
        print(f"   ❌ Error en test update_data_status: {e}")

def test_warmup_with_real_data():
    """🔥 Test warm-up completo con verificación paso a paso"""
    
    try:
        from core.data_management.ict_data_manager import ICTDataManager
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        
        print("   🔥 Test warm-up con monitoreo completo...")
        
        # Crear instancias
        downloader = AdvancedCandleDownloader()
        manager = ICTDataManager(downloader=downloader)
        
        # Estado inicial
        print("   📊 Estado inicial:")
        initial_cache = manager.get_multi_tf_cache_status()
        print(f"     Símbolos iniciales: {initial_cache.get('total_symbols', 0)}")
        
        # Warm-up con debug
        print("   🚀 Ejecutando warm-up con debug...")
        
        # Verificar que el downloader está correctamente asignado
        print(f"   🔍 Downloader assigned: {manager.downloader is not None}")
        print(f"   🔍 Downloader type: {type(manager.downloader).__name__}")
        
        # Ejecutar warm-up
        warmup_result = manager.warm_up_cache(
            symbols=['EURUSD'],
            timeframes=['H4']
        )
        
        print("   📊 Resultado warm-up:")
        print(f"     Success: {warmup_result.get('success', False)}")
        print(f"     Warm-up completed: {manager.warm_up_completed}")
        
        # Estado final
        print("   📈 Estado final:")
        final_cache = manager.get_multi_tf_cache_status()
        print(f"     Símbolos finales: {final_cache.get('total_symbols', 0)}")
        
        final_performance = manager.get_performance_summary()
        print(f"     Data symbols count: {final_performance.get('data_symbols_count', 0)}")
        print(f"     Total timeframes: {final_performance.get('total_timeframes', 0)}")
        
        # Diagnóstico detallado si sigue vacío
        if final_cache.get('total_symbols', 0) == 0:
            print("   🔍 DIAGNÓSTICO CACHE VACÍO:")
            print(f"     - manager.data_status existe: {hasattr(manager, 'data_status')}")
            if hasattr(manager, 'data_status'):
                print(f"     - manager.data_status content: {manager.data_status}")
            
            print(f"     - Verificando método _execute_parallel_downloads...")
            # Verificar si el método existe y es callable
            has_method = hasattr(manager, '_execute_parallel_downloads')
            print(f"     - _execute_parallel_downloads existe: {has_method}")
            
            if has_method:
                method = getattr(manager, '_execute_parallel_downloads')
                print(f"     - _execute_parallel_downloads callable: {callable(method)}")
        
    except Exception as e:
        print(f"   ❌ Error en test warm-up completo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
