#!/usr/bin/env python3
"""
🔧 PRUEBA RÁPIDA DE INTEGRACIÓN POI
===================================

Script simple para probar la integración ICTDetector + POI después de las correcciones.
"""

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np

def test_integration():
    print("🔧 PRUEBA RÁPIDA DE INTEGRACIÓN POI")
    print("=" * 40)

    # Crear datos mínimos
    np.random.seed(42)
    dates = pd.date_range(start='2025-01-28 10:00:00', periods=50, freq='15min')
    base_price = 1.17500

    opens = [base_price + np.random.normal(0, 0.0001) for _ in range(50)]
    closes = [opens[i] + np.random.normal(0, 0.0001) for i in range(50)]
    highs = [max(opens[i], closes[i]) + abs(np.random.normal(0, 0.0002)) for i in range(50)]
    lows = [min(opens[i], closes[i]) - abs(np.random.normal(0, 0.0002)) for i in range(50)]

    df = pd.DataFrame({
        'timestamp': dates,
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes,
        'volume': [500] * 50
    })

    print(f"✅ Datos de prueba: {len(df)} velas")
    current_price = float(df['close'].iloc[-1])
    print(f"   Precio actual: {current_price:.5f}")

    # Test ICTDetector
    try:
        from core.ict_engine.ict_detector import ICTDetector
        detector = ICTDetector()

        print(f"\\n🔍 Probando ICTDetector.find_pois()...")
        pois = detector.find_pois(df)

        print(f"✅ RESULTADO: {len(pois)} POIs encontrados")

        if pois:
            print("\\n📋 POIs detectados:")
            for i, poi in enumerate(pois[:5], 1):
                tipo = poi.get('type', 'N/A')
                precio = poi.get('price_level', 0)
                source = poi.get('source', 'N/A')
                print(f"   {i}. {tipo} @ {precio:.5f} (desde {source})")
        else:
            print("⚠️ No se detectaron POIs")

        return len(pois) > 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_integration()
    print(f"\\n🎯 Resultado final: {'✅ ÉXITO' if success else '❌ FALLO'}")
