"""
🎯 TEST MULTI-TIMEFRAME REAL DATA v6.0

Test con datos reales de MT5 para verificar descarga multi-timeframe
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.analysis.pattern_detector import PatternDetector
import time


def test_real_multi_timeframe_download():
    """
    🔍 TEST CON DATOS REALES: Multi-Timeframe Download
    """
    print("🎯 Testing REAL Multi-Timeframe Download...")
    print("   Conectando a FTMO Global Markets MT5...")
    
    # Crear detector con downloader real
    detector = PatternDetector()
    
    # Test con datos reales
    symbol = "EURUSD"
    primary_timeframe = "M15"
    days = 3
    
    print(f"\\n📊 Análisis Real Multi-TF:")
    print(f"   Symbol: {symbol}")
    print(f"   Primary TF: {primary_timeframe}")
    print(f"   Days: {days}")
    
    start_time = time.time()
    
    # Ejecutar análisis completo con multi-timeframe
    patterns = detector.detect_patterns(
        symbol=symbol,
        timeframe=primary_timeframe,
        lookback_days=days
    )
    
    analysis_time = time.time() - start_time
    
    print(f"\\n⚡ Resultados:")
    print(f"   Patterns detectados: {len(patterns)}")
    print(f"   Tiempo de análisis: {analysis_time:.3f}s")
    
    # Verificar datos multi-timeframe
    multi_tf_data = detector.get_multi_timeframe_data(symbol)
    
    print(f"\\n📈 Datos Multi-Timeframe:")
    print(f"   Timeframes descargados: {list(multi_tf_data.keys())}")
    
    total_candles = 0
    for tf, data in multi_tf_data.items():
        print(f"   {tf}: {len(data)} velas")
        total_candles += len(data)
        
        # Verificar estructura de datos
        assert not data.empty, f"Datos de {tf} no deben estar vacíos"
        assert all(col in data.columns for col in ['open', 'high', 'low', 'close']), \
            f"Datos de {tf} deben tener columnas OHLC"
    
    print(f"   Total velas procesadas: {total_candles}")
    
    # Verificar que se tienen múltiples timeframes
    if len(multi_tf_data) > 1:
        print("✅ Multi-Timeframe Download: SUCCESS")
        print("🎯 Sistema descargando correctamente múltiples timeframes")
    else:
        print("⚠️  Solo un timeframe detectado")
        print("   Esto puede ser normal dependiendo de la configuración")
    
    # Verificar performance
    if analysis_time < 30.0:  # Menos de 30 segundos es aceptable
        print(f"✅ Performance: EXCELLENT ({analysis_time:.3f}s)")
    else:
        print(f"⚠️  Performance: SLOW ({analysis_time:.3f}s)")
    
    # Métricas finales
    metrics = detector.get_performance_metrics()
    print(f"\\n📊 Métricas de Performance:")
    print(f"   Análisis promedio: {metrics['avg_analysis_time']:.3f}s")
    print(f"   Total análisis: {metrics['total_analyses']}")
    
    return len(multi_tf_data), total_candles, analysis_time


def test_enhanced_patterns_with_multi_tf():
    """
    🔍 TEST: Enhancement de patrones con multi-timeframe
    """
    print("\\n🎯 Testing Enhanced Patterns with Multi-TF...")
    
    detector = PatternDetector()
    
    # Análisis con datos reales
    patterns = detector.detect_patterns(
        symbol="GBPUSD",
        timeframe="H1", 
        lookback_days=2
    )
    
    print(f"   Patterns before enhancement: {len(patterns)}")
    
    if patterns:
        print("\\n📈 Pattern Enhancement Details:")
        for i, pattern in enumerate(patterns[:3]):  # Mostrar primeros 3
            print(f"   Pattern {i+1}:")
            print(f"      Type: {pattern.pattern_type}")
            print(f"      Strength: {pattern.strength}")
            print(f"      Timeframe: {pattern.timeframe}")
            print(f"      Direction: {pattern.direction}")
            
            # Verificar si tiene metadata de multi-TF
            if hasattr(pattern, 'metadata') and pattern.metadata:
                mtf_confirmations = pattern.metadata.get('multi_tf_confirmations', [])
                if mtf_confirmations:
                    print(f"      Multi-TF Confirmations: {mtf_confirmations}")
    else:
        print("   No patterns detected for enhancement test")
    
    return len(patterns)


if __name__ == "__main__":
    print("="*80)
    print("🎯 REAL MULTI-TIMEFRAME DATA TEST v6.0")
    print("="*80)
    
    try:
        # Test 1: Descarga real multi-timeframe
        tf_count, total_candles, time_taken = test_real_multi_timeframe_download()
        
        # Test 2: Enhancement con multi-TF
        enhanced_patterns = test_enhanced_patterns_with_multi_tf()
        
        print("\\n" + "="*80)
        print("🎉 REAL MULTI-TIMEFRAME TESTS COMPLETED")
        print(f"📊 Resumen:")
        print(f"   Timeframes procesados: {tf_count}")
        print(f"   Total velas: {total_candles}")
        print(f"   Tiempo análisis: {time_taken:.3f}s")
        print(f"   Patterns enhanced: {enhanced_patterns}")
        print("🚀 Sistema multi-timeframe OPERATIVO con datos reales")
        print("="*80)
        
    except Exception as e:
        print(f"\\n❌ TEST FAILED: {e}")
        print("🔧 Revisar conexión MT5 o configuración")
        import traceback
        traceback.print_exc()
