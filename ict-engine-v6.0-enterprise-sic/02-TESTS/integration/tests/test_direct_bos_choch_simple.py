#!/usr/bin/env python3
"""
🎯 TEST DIRECTO BOS/CHoCH v6.0 - CONTEO SIMPLE
==============================================

Test simplificado que cuenta directamente las estructuras BOS/CHoCH
de los logs del MarketStructureAnalyzer.

Autor: ICT Engine Team v6.0
Fecha: 08 Agosto 2025
"""

import sys
import os

# Ajustar paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Core imports v6.0
from core.ict_engine.pattern_detector import ICTPatternDetector
from core.analysis.market_structure_analyzer_v6 import MarketStructureAnalyzerV6
from core.analysis.unified_market_memory import UnifiedMarketMemory
from core.smart_trading_logger import SmartTradingLogger


def test_direct_bos_choch_count():
    """Test directo para contar BOS/CHoCH de logs"""
    
    print("🎯 TEST DIRECTO BOS/CHoCH - CONTEO SIMPLE")
    print("=" * 50)
    
    # Inicializar componentes
    logger = SmartTradingLogger()
    detector = ICTPatternDetector()
    analyzer = MarketStructureAnalyzerV6()
    memory = UnifiedMarketMemory()
    
    symbols = ['EURUSD', 'GBPUSD', 'USDJPY']
    timeframes = ['H4', 'H1']
    
    total_bos = 0
    total_choch = 0
    total_liquidity_grab = 0
    total_structures = 0
    
    for symbol in symbols:
        print(f"\n📈 Analizando {symbol}...")
        
        symbol_bos = 0
        symbol_choch = 0
        symbol_liquidity_grab = 0
        symbol_structures = 0
        
        for timeframe in timeframes:
            print(f"   🔍 {timeframe}: ", end="")
            
            try:
                # Obtener datos usando el detector
                result = detector.detect_patterns(
                    symbol=symbol,
                    timeframe=timeframe,
                    lookback_days=5
                )
                
                # Obtener datos de velas para estructura
                if hasattr(result, 'processed_data') and result.processed_data is not None:
                    candles = result.processed_data
                    
                    # Llamar directamente al análisis de estructura
                    structure_signal = analyzer.analyze_market_structure(
                        candles_m15=candles,  # Usar los datos que tenemos
                        current_price=candles['close'].iloc[-1] if not candles.empty else 0.0,
                        symbol=symbol
                    )
                    
                    # Contar estructura directamente del signal
                    tf_bos = 0
                    tf_choch = 0
                    tf_liquidity_grab = 0
                    tf_structures = 0
                    
                    if structure_signal:
                        tf_structures = 1
                        struct_type = str(structure_signal.structure_type).lower()
                        
                        # Conteo directo del tipo de estructura
                        if 'bos' in struct_type:
                            tf_bos = 1
                            print(f"BOS detectado ({struct_type})")
                        elif 'choch' in struct_type:
                            tf_choch = 1
                            print(f"CHoCH detectado ({struct_type})")
                        elif 'liquidity_grab' in struct_type:
                            tf_liquidity_grab = 1
                            print(f"Liquidity Grab detectado ({struct_type})")
                        else:
                            print(f"Estructura: {struct_type}")
                    else:
                        print("Sin estructura detectada")
                    
                    symbol_bos += tf_bos
                    symbol_choch += tf_choch
                    symbol_liquidity_grab += tf_liquidity_grab
                    symbol_structures += tf_structures
                    
                else:
                    print("Sin datos procesados")
                    
            except Exception as e:
                logger.error(f"Error analizando {symbol} {timeframe}: {e}")
                print(f"ERROR: {e}")
        
        print(f"   📊 {symbol} TOTAL: {symbol_structures} estructuras, {symbol_bos} BOS, {symbol_choch} CHoCH, {symbol_liquidity_grab} Liquidity Grabs")
        
        total_bos += symbol_bos
        total_choch += symbol_choch
        total_liquidity_grab += symbol_liquidity_grab
        total_structures += symbol_structures
    
    print("\n" + "=" * 60)
    print("🎉 RESULTADO DIRECTO BOS/CHoCH + LIQUIDITY GRABS")
    print("=" * 60)
    print(f"📊 Total Estructuras Detectadas: {total_structures}")
    print(f"📈 Total BOS (Break of Structure): {total_bos}")
    print(f"🔄 Total CHoCH (Change of Character): {total_choch}")
    print(f"💎 Total Liquidity Grabs: {total_liquidity_grab}")
    
    if total_structures > 0:
        bos_rate = (total_bos / total_structures) * 100
        choch_rate = (total_choch / total_structures) * 100
        lg_rate = (total_liquidity_grab / total_structures) * 100
        print(f"📊 Tasa BOS: {bos_rate:.1f}%")
        print(f"📊 Tasa CHoCH: {choch_rate:.1f}%")
        print(f"📊 Tasa Liquidity Grabs: {lg_rate:.1f}%")
    
    print(f"\n🎯 DIAGNÓSTICO:")
    if total_bos == 0 and total_choch == 0 and total_liquidity_grab == 0:
        print("❌ NO se detectaron eventos estructurales")
        print("🔍 Posibles causas:")
        print("   - Umbral de confianza muy alto (65%)")
        print("   - Período analizado muy corto (5 días)")
        print("   - Condiciones de mercado no favorables")
        print("   - Lógica de detección necesita ajuste")
    else:
        total_events = total_bos + total_choch + total_liquidity_grab
        print(f"✅ Sistema ESTRUCTURAL FUNCIONANDO: {total_events} eventos")
        if total_liquidity_grab > 0:
            print(f"💎 Liquidity Grabs detectados: {total_liquidity_grab} (excelente señal ICT)")
    
    return {
        'total_structures': total_structures,
        'total_bos': total_bos,
        'total_choch': total_choch,
        'total_liquidity_grab': total_liquidity_grab
    }


if __name__ == "__main__":
    test_direct_bos_choch_count()
