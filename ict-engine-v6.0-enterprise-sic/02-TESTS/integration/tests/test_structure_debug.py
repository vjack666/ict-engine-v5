"""
🔬 Test de Debug - Análisis de Estructuras de Mercado v6.0
Verificación específica de qué está retornando el analyzer
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from core.analysis.market_structure_analyzer_v6 import MarketStructureAnalyzerV6
from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
import pandas as pd

def debug_analyzer():
    """Debug específico del analizador"""
    print("🔬 DEBUG ANALYZER - VERIFICACIÓN DIRECTA")
    print("="*60)
    
    # Crear analyzer directo
    analyzer = MarketStructureAnalyzerV6()
    downloader = AdvancedCandleDownloader()
    
    # Test con EURUSD M15 usando bars_count
    print("📊 Obteniendo datos EURUSD M15...")
    result = downloader.download_candles("EURUSD", "M15", bars_count=500)
    
    print(f"🔧 Tipo de resultado: {type(result)}")
    print(f"🔧 Contenido: {result.keys() if isinstance(result, dict) else 'No es dict'}")
    
    if result is None:
        print("❌ No se pudieron obtener datos - result es None")
        return
    
    if isinstance(result, dict) and 'candles' in result:
        candles = result['candles']
        print(f"🔧 Tipo de candles: {type(candles)}")
    elif isinstance(result, dict) and 'data' in result:
        candles = result['data']
        print(f"🔧 Tipo de data: {type(candles)}")
    else:
        print("❌ Estructura de datos no reconocida")
        print(f"   Result: {result}")
        return
    if not isinstance(candles, pd.DataFrame) or candles.empty:
        print("❌ Datos inválidos")
        return
    
    print(f"✅ Datos obtenidos: {len(candles)} velas")
    print(f"   Rango: {candles.index[0]} a {candles.index[-1]}")
    
    # Análisis directo
    print("\n🔍 Ejecutando análisis directo...")
    signal = analyzer.analyze_market_structure(
        candles_m15=candles,
        current_price=candles.iloc[-1]['close'],
        symbol="EURUSD"
    )
    
    if signal is None:
        print("❌ No se devolvió señal")
        
        # Debug internal state
        print(f"\n🔧 Debug interno:")
        print(f"   Min confidence: {analyzer.min_confidence}%")
        print(f"   Lookback: {analyzer.structure_lookback}")
        print(f"   Current trend: {analyzer.current_trend}")
        print(f"   Structure history: {len(analyzer.structure_history)} elementos")
        
        # Test swing points y condiciones
        swing_highs, swing_lows = analyzer._detect_swing_points(candles)
        print(f"   Swing highs: {len(swing_highs)}")
        print(f"   Swing lows: {len(swing_lows)}")
        
        if len(swing_highs) >= 2:
            last_high = swing_highs[-1]['price']
            prev_high = swing_highs[-2]['price']
            print(f"     Último high: {last_high:.5f}")
            print(f"     Anterior high: {prev_high:.5f}")
            print(f"     Precio actual > último high: {candles.iloc[-1]['close'] > last_high}")
            print(f"     Último > anterior: {last_high > prev_high}")
            
        if len(swing_lows) >= 2:
            last_low = swing_lows[-1]['price']
            prev_low = swing_lows[-2]['price']
            print(f"     Último low: {last_low:.5f}")
            print(f"     Anterior low: {prev_low:.5f}")
            print(f"     Precio actual < último low: {candles.iloc[-1]['close'] < last_low}")
            print(f"     Último < anterior: {last_low < prev_low}")
            
        # Test estructura manual
        current_price = candles.iloc[-1]['close']
        print(f"   Precio actual: {current_price:.5f}")
        
        if len(swing_highs) >= 2 and len(swing_lows) >= 2:
            structure_score, structure_type, break_level, target_level = analyzer._detect_structure_change(
                candles, swing_highs, swing_lows, current_price
            )
            print(f"   Structure score: {structure_score}")
            print(f"   Structure type: {structure_type}")
            print(f"   Break level: {break_level}")
            print(f"   Target level: {target_level}")
            
            # Test componentes de confianza
            momentum_score = analyzer._analyze_momentum(candles, structure_type)
            volume_score = analyzer._analyze_volume_structure(candles)
            confluence_score = analyzer._analyze_confluence_v6(candles, None, structure_type)
            
            total_confidence = (
                structure_score * analyzer.structure_weight +
                momentum_score * analyzer.momentum_weight +
                volume_score * analyzer.volume_weight +
                confluence_score * analyzer.confluence_weight
            ) * 100
            
            print(f"   Momentum score: {momentum_score:.2f}")
            print(f"   Volume score: {volume_score:.2f}")
            print(f"   Confluence score: {confluence_score:.2f}")
            print(f"   Total confidence: {total_confidence:.1f}%")
            print(f"   Min confidence: {analyzer.min_confidence}%")
            print(f"   Pasa threshold: {'✅' if total_confidence >= analyzer.min_confidence else '❌'}")
            
    else:
        print("✅ SEÑAL DETECTADA!")
        print(f"   Tipo: {signal.structure_type.value}")
        print(f"   Confianza: {signal.confidence:.1f}%")
        print(f"   ICT Compliance: {signal.ict_compliance}")
        print(f"   Smart Money: {signal.smart_money_alignment}")
        print(f"   Break level: {signal.break_level:.5f}")
        print(f"   Target level: {signal.target_level:.5f}")
        
        # Verificar si es BOS o CHoCH por nombre
        is_bos = 'BOS' in signal.structure_type.value
        is_choch = 'CHOCH' in signal.structure_type.value
        
        print(f"   Es BOS: {'✅' if is_bos else '❌'}")
        print(f"   Es CHoCH: {'✅' if is_choch else '❌'}")

if __name__ == "__main__":
    debug_analyzer()
