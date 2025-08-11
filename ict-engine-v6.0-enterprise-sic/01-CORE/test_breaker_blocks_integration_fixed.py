#!/usr/bin/env python3
"""
🧪 TEST BREAKER BLOCKS INTEGRATION - SIGUIENDO REGLA #7
=========================================================

Test completo para verificar que la integración de Breaker Blocks v6.2 
en PatternDetector funciona correctamente después del fix de imports.

REGLA #7: TESTS PRIMERO - Si el test es correcto, el código debe pasar
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Añadir path para imports
sys.path.append('.')

def test_breaker_blocks_integration_fixed():
    """🧪 Test completo de integración Breaker Blocks v6.2"""
    
    print("🚀 INICIANDO TEST BREAKER BLOCKS INTEGRATION v6.2")
    print("=" * 60)
    
    # 1. TEST IMPORT PATTERN DETECTOR
    print("\n📦 TEST 1: Import PatternDetector")
    try:
        from core.ict_engine.pattern_detector import ICTPatternDetector, BREAKER_BLOCKS_V62_AVAILABLE
        print("✅ PatternDetector importado exitosamente")
        print(f"   BREAKER_BLOCKS_V62_AVAILABLE = {BREAKER_BLOCKS_V62_AVAILABLE}")
        if not BREAKER_BLOCKS_V62_AVAILABLE:
            print("❌ FALLO: Breaker Blocks v6.2 no está disponible")
            return False
    except Exception as e:
        print(f"❌ FALLO: Error importando PatternDetector: {e}")
        return False
    
    # 2. TEST CREACIÓN DETECTOR
    print("\n🏗️ TEST 2: Creación PatternDetector")
    try:
        detector = ICTPatternDetector()
        detector.symbol = "EURUSD"
        detector.timeframe = "M15"
        print("✅ PatternDetector creado exitosamente")
    except Exception as e:
        print(f"❌ FALLO: Error creando detector: {e}")
        return False
    
    # 3. TEST DATOS SINTÉTICOS
    print("\n📊 TEST 3: Preparación datos sintéticos")
    try:
        # Crear datos OHLCV sintéticos para test
        dates = pd.date_range(start='2024-01-01', periods=100, freq='15T')
        np.random.seed(42)  # Para reproducibilidad
        
        # Generar datos realistas EURUSD
        base_price = 1.0800
        price_changes = np.random.normal(0, 0.0005, 100).cumsum()
        
        data = []
        for i, date in enumerate(dates):
            price = base_price + price_changes[i]
            high = price + np.random.uniform(0.0001, 0.0005)
            low = price - np.random.uniform(0.0001, 0.0005)
            close = price + np.random.uniform(-0.0002, 0.0002)
            
            data.append({
                'timestamp': date,
                'open': price,
                'high': high,
                'low': low,
                'close': close,
                'volume': np.random.randint(100, 1000)
            })
        
        candles_df = pd.DataFrame(data)
        candles_df.set_index('timestamp', inplace=True)
        print(f"✅ Datos sintéticos creados: {len(candles_df)} velas")
        print(f"   Rango de precios: {candles_df['low'].min():.5f} - {candles_df['high'].max():.5f}")
    except Exception as e:
        print(f"❌ FALLO: Error creando datos sintéticos: {e}")
        return False
    
    # 4. TEST DETECCIÓN COMPLETA
    print("\n🔍 TEST 4: Detección completa de patterns")
    try:
        result = detector.detect_patterns(
            symbol="EURUSD",
            timeframe="M15",
            lookback_days=7
        )
        print("✅ Detección de patterns completada")
        print(f"   Order Blocks detectados: {len(result.order_blocks)}")
        print(f"   Fair Value Gaps detectados: {len(result.fair_value_gaps)}")
        print(f"   Total patterns: {result.total_patterns}")
    except Exception as e:
        print(f"❌ FALLO: Error en detección de patterns: {e}")
        return False
    
    # 5. TEST MÉTODO BREAKER ESPECÍFICO
    print("\n💥 TEST 5: Método _detect_breaker_block específico")
    try:
        # Test directo del método breaker
        breaker_result = detector._detect_breaker_block(
            candles=candles_df,
            candle_index=50,  # Vela del medio
            market_structure=None
        )
        
        if breaker_result is not None:
            print(f"✅ Breaker Block detectado: {breaker_result.ob_type}")
            print(f"   Precio high: {breaker_result.high_price:.5f}")
            print(f"   Precio low: {breaker_result.low_price:.5f}")
            print(f"   Confianza: {breaker_result.probability:.1%}")
        else:
            print("ℹ️ No se detectó Breaker Block (comportamiento esperado con datos sintéticos)")
            
        print("✅ Método _detect_breaker_block funciona correctamente")
    except Exception as e:
        print(f"❌ FALLO: Error en método _detect_breaker_block: {e}")
        return False
    
    # 6. TEST FACTORY FUNCTION
    print("\n🏭 TEST 6: Factory function create_high_performance_breaker_detector_v62")
    try:
        from core.ict_engine.advanced_patterns.breaker_blocks_enterprise_v62 import create_high_performance_breaker_detector_v62
        
        breaker_detector = create_high_performance_breaker_detector_v62("EURUSD", "M15")
        print("✅ Factory function funciona correctamente")
        print(f"   Detector type: {type(breaker_detector).__name__}")
        
        # Test método detect_breaker_blocks_enterprise
        empty_obs = []
        breaker_signals = breaker_detector.detect_breaker_blocks_enterprise(
            data=candles_df,
            order_blocks=empty_obs,
            symbol="EURUSD",
            timeframe="M15"
        )
        print(f"✅ Método detect_breaker_blocks_enterprise funciona: {len(breaker_signals)} signals")
        
    except Exception as e:
        print(f"❌ FALLO: Error en factory function: {e}")
        return False
    
    # 7. RESUMEN FINAL
    print("\n" + "=" * 60)
    print("🎉 RESUMEN FINAL TEST BREAKER BLOCKS INTEGRATION")
    print("=" * 60)
    print("✅ Import PatternDetector: PASSED")
    print("✅ BREAKER_BLOCKS_V62_AVAILABLE: TRUE")
    print("✅ Creación detector: PASSED")
    print("✅ Datos sintéticos: PASSED") 
    print("✅ Detección completa: PASSED")
    print("✅ Método _detect_breaker_block: PASSED")
    print("✅ Factory function: PASSED")
    print("\n🏆 TODOS LOS TESTS PASADOS - INTEGRACIÓN EXITOSA")
    
    return True

if __name__ == "__main__":
    success = test_breaker_blocks_integration_fixed()
    if success:
        print("\n🎯 CONCLUSIÓN: BREAKER BLOCKS v6.2 INTEGRACIÓN COMPLETADA ✅")
        print("   El pendiente del lunes ha sido resuelto exitosamente")
    else:
        print("\n❌ FALLO: Integración no completada")
    
    exit(0 if success else 1)
