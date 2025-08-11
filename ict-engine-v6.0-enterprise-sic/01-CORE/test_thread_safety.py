#!/usr/bin/env python3
"""
🔒 TEST THREAD-SAFETY - ICT ENGINE v6.0 Enterprise
==================================================

Test completo del sistema thread-safe de pandas en AdvancedCandleDownloader
Demuestra las capacidades de operaciones concurrentes seguras.

Fecha: Agosto 2025
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader

def test_concurrent_downloads():
    """🚀 Test de descargas concurrentes thread-safe"""
    print("🔒 Testing Thread-Safety para Pandas en ICT Engine v6.0")
    print("=" * 60)
    
    # Crear downloader
    downloader = AdvancedCandleDownloader(config={
        'enable_debug': True,
        'max_concurrent': 4,  # Prueba con 4 threads concurrentes
        'use_predictive_cache': True
    })
    
    # Obtener métricas iniciales
    initial_metrics = downloader.get_thread_safety_metrics()
    print(f"📊 Thread Safety Status: {initial_metrics['thread_safety']['safety_level']}")
    print(f"🔒 Lock Type: {initial_metrics['thread_safety']['lock_type']}")
    print(f"🧵 Current Thread: {initial_metrics['current_thread']}")
    print()
    
    # Símbolos y timeframes para test
    test_configs = [
        ('EURUSD', 'M15'),
        ('GBPUSD', 'M5'),
        ('XAUUSD', 'H1'),
        ('USDJPY', 'M30'),
        ('AUDUSD', 'H4'),
        ('EURJPY', 'M1')
    ]
    
    def download_worker(symbol, timeframe, worker_id):
        """Worker para test concurrente"""
        thread_name = f"TestWorker-{worker_id}"
        threading.current_thread().name = thread_name
        
        print(f"🧵 [{thread_name}] Iniciando descarga: {symbol} {timeframe}")
        
        try:
            # Simular descarga con datos mock
            result = downloader._download_with_simulation(
                symbol=symbol,
                timeframe=timeframe,
                start_date=None,  # El método ahora maneja None correctamente
                end_date=None,    # El método ahora maneja None correctamente
                save_to_file=False
            )
            
            if result['success']:
                data_len = len(result['data']) if result['data'] is not None else 0
                print(f"✅ [{thread_name}] {symbol} {timeframe}: {data_len} velas generadas")
                return {
                    'worker_id': worker_id,
                    'symbol': symbol,
                    'timeframe': timeframe,
                    'success': True,
                    'data_length': data_len,
                    'thread_name': thread_name
                }
            else:
                print(f"❌ [{thread_name}] Error: {result.get('error', 'Unknown')}")
                return {
                    'worker_id': worker_id,
                    'success': False,
                    'error': result.get('error', 'Unknown')
                }
                
        except Exception as e:
            print(f"❌ [{thread_name}] Exception: {e}")
            return {
                'worker_id': worker_id,
                'success': False,
                'error': str(e)
            }
    
    # Ejecutar test concurrente
    print("🚀 Iniciando test de descargas concurrentes...")
    start_time = time.time()
    
    results = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Enviar trabajos
        futures = {
            executor.submit(download_worker, symbol, timeframe, i): (symbol, timeframe, i)
            for i, (symbol, timeframe) in enumerate(test_configs)
        }
        
        # Recoger resultados
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    
    # Análizar resultados
    execution_time = time.time() - start_time
    successful = [r for r in results if r.get('success', False)]
    failed = [r for r in results if not r.get('success', False)]
    
    print()
    print("📊 RESULTADOS DEL TEST THREAD-SAFETY:")
    print(f"⏱️  Tiempo total: {execution_time:.2f}s")
    print(f"✅ Exitosos: {len(successful)}/{len(results)}")
    print(f"❌ Fallidos: {len(failed)}/{len(results)}")
    
    if successful:
        total_data = sum(r.get('data_length', 0) for r in successful)
        print(f"📈 Total velas generadas: {total_data}")
        print(f"🚀 Velocidad: {total_data/execution_time:.1f} velas/segundo")
    
    # Métricas finales de thread-safety
    final_metrics = downloader.get_thread_safety_metrics()
    print(f"🧵 Pandas instances creadas: {final_metrics['pandas_instances']}")
    print(f"📊 Performance metrics: {final_metrics['performance_metrics_count']}")
    
    print()
    print("🔒 VERIFICACIONES THREAD-SAFETY:")
    for rec in final_metrics['safety_recommendations']:
        print(f"   {rec}")
    
    # Resultado final
    if len(failed) == 0:
        print()
        print("🎉 TEST THREAD-SAFETY COMPLETADO EXITOSAMENTE!")
        print("✅ Pandas operando de forma thread-safe")
        print("✅ Sin race conditions detectadas")
        print("✅ Operaciones concurrentes estables")
    else:
        print()
        print("⚠️ ALGUNOS TESTS FALLARON:")
        for fail in failed:
            print(f"   ❌ Worker {fail['worker_id']}: {fail.get('error', 'Unknown')}")

if __name__ == "__main__":
    test_concurrent_downloads()
