#!/usr/bin/env python3
"""
🔍 INVESTIGACIÓN PROFUNDA: BOS DETECTION CON DATOS REALES
=========================================================

Script de investigación que:
1. Descarga datos reales de FundedNext MT5
2. Ejecuta análisis BOS DIRECTO sin simulaciones
3. Analiza por qué no se detectan BOS en datos reales
4. Proporciona diagnósticos detallados y recomendaciones

Autor: ICT Engine v6.0 Enterprise  
Fecha: 2025-01-07
Propósito: Solucionar el problema de BOS non-detection
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
from core.analysis.multi_timeframe_analyzer import MultiTimeframeAnalyzer

def analyze_data_quality(df: pd.DataFrame, symbol: str) -> dict:
    """🔍 Analizar calidad y características de los datos reales"""
    
    if df is None or len(df) == 0:
        return {"error": "No data"}
    
    # Estadísticas básicas
    stats = {
        "symbol": symbol,
        "total_bars": len(df),
        "date_range": {
            "start": str(df.index[0]),
            "end": str(df.index[-1]),
            "days": (df.index[-1] - df.index[0]).days
        }
    }
    
    # Análisis de precios
    highs = df['high']
    lows = df['low']
    closes = df['close']
    
    # Calcular niveles y rangos
    max_high = highs.max()
    min_low = lows.min()
    current_price = closes.iloc[-1]
    
    # Calcular volatilidad
    price_changes = closes.pct_change().dropna()
    volatility = price_changes.std()
    
    # Análisis de tendencia reciente
    recent_bars = min(100, len(df))
    recent_data = df.tail(recent_bars)
    recent_trend = (recent_data['close'].iloc[-1] - recent_data['close'].iloc[0]) / recent_data['close'].iloc[0]
    
    stats.update({
        "price_analysis": {
            "current_price": round(current_price, 5),
            "max_high": round(max_high, 5),
            "min_low": round(min_low, 5),
            "total_range": round(max_high - min_low, 5),
            "range_percentage": round((max_high - min_low) / min_low * 100, 3)
        },
        "volatility": {
            "daily_volatility": round(volatility * 100, 4),
            "recent_trend": round(recent_trend * 100, 3)
        }
    })
    
    return stats

def detailed_bos_analysis(df: pd.DataFrame, symbol: str, analyzer: MultiTimeframeAnalyzer) -> dict:
    """🔬 Análisis detallado de por qué no se detectan BOS"""
    
    print(f"\n🔬 ANÁLISIS DETALLADO BOS PARA {symbol}")
    print("=" * 60)
    
    # Ejecutar análisis M15 con debug
    m15_result = analyzer.detectar_estructura_m15_optimizada(df)
    
    print(f"📊 Resultado M15: {m15_result}")
    
    # Análisis manual de breakouts
    recent_data = df.tail(50)  # Últimas 50 velas
    
    highs = recent_data['high']
    lows = recent_data['low']
    closes = recent_data['close']
    
    # Calcular niveles manualmente
    resistance_window = 10
    support_window = 10
    
    resistance_level = highs.rolling(window=resistance_window).max().iloc[-1]
    support_level = lows.rolling(window=support_window).min().iloc[-1]
    current_price = closes.iloc[-1]
    
    # Calcular umbrales
    resistance_break_threshold = 0.999  # 99.9%
    support_break_threshold = 1.001    # 100.1%
    
    resistance_target = resistance_level * resistance_break_threshold
    support_target = support_level * support_break_threshold
    
    print(f"\n📈 ANÁLISIS MANUAL DE NIVELES:")
    print(f"   💰 Precio actual: {current_price:.5f}")
    print(f"   🔴 Resistencia: {resistance_level:.5f}")
    print(f"   🟢 Soporte: {support_level:.5f}")
    print(f"   🎯 Target resistencia (99.9%): {resistance_target:.5f}")
    print(f"   🎯 Target soporte (100.1%): {support_target:.5f}")
    
    # Verificar condiciones de breakout
    bullish_break = current_price > resistance_target
    bearish_break = current_price < support_target
    
    print(f"\n🔍 CONDICIONES DE BREAKOUT:")
    print(f"   📈 Bullish break: {bullish_break} ({current_price:.5f} > {resistance_target:.5f})")
    print(f"   📉 Bearish break: {bearish_break} ({current_price:.5f} < {support_target:.5f})")
    
    # Calcular distancias
    distance_to_resistance = (resistance_target - current_price) / current_price * 100
    distance_to_support = (current_price - support_target) / current_price * 100
    
    print(f"\n📏 DISTANCIAS A NIVELES:")
    print(f"   📈 Distancia a resistencia: {distance_to_resistance:.3f}%")
    print(f"   📉 Distancia a soporte: {distance_to_support:.3f}%")
    
    # Análisis de rango
    range_size = (resistance_level - support_level) / support_level * 100
    print(f"   📊 Tamaño del rango: {range_size:.3f}%")
    
    # Análisis histórico de breakouts
    print(f"\n📜 ANÁLISIS HISTÓRICO DE BREAKOUTS:")
    
    # Buscar breakouts históricos en últimas 200 velas
    historical_data = df.tail(200)
    breakout_count = 0
    
    for i in range(20, len(historical_data)):
        window_data = historical_data.iloc[i-20:i]
        resistance = window_data['high'].max()
        support = window_data['low'].min()
        current = historical_data.iloc[i]['close']
        
        if current > resistance * 0.999 or current < support * 1.001:
            breakout_count += 1
    
    print(f"   🎯 Breakouts históricos (últimas 200 velas): {breakout_count}")
    print(f"   📊 Frecuencia de breakouts: {breakout_count/180*100:.1f}%")
    
    return {
        "manual_analysis": {
            "current_price": current_price,
            "resistance": resistance_level,
            "support": support_level,
            "bullish_break": bullish_break,
            "bearish_break": bearish_break,
            "distance_to_resistance": distance_to_resistance,
            "distance_to_support": distance_to_support,
            "range_size": range_size,
            "historical_breakouts": breakout_count
        },
        "analyzer_result": m15_result
    }

def test_threshold_sensitivity(df: pd.DataFrame, symbol: str) -> dict:
    """🎛️ Probar diferentes umbrales para detectar BOS"""
    
    print(f"\n🎛️ PRUEBA DE SENSIBILIDAD DE UMBRALES PARA {symbol}")
    print("=" * 60)
    
    recent_data = df.tail(50)
    highs = recent_data['high']
    lows = recent_data['low']
    closes = recent_data['close']
    
    resistance_level = highs.rolling(window=10).max().iloc[-1]
    support_level = lows.rolling(window=10).min().iloc[-1]
    current_price = closes.iloc[-1]
    
    # Probar diferentes umbrales
    thresholds = [
        {"name": "Muy Estricto", "resistance": 0.995, "support": 1.005},
        {"name": "Estricto (Actual)", "resistance": 0.999, "support": 1.001},
        {"name": "Moderado", "resistance": 0.9995, "support": 1.0005},
        {"name": "Relajado", "resistance": 1.0005, "support": 0.9995}
    ]
    
    results = []
    
    for threshold in thresholds:
        resistance_target = resistance_level * threshold["resistance"]
        support_target = support_level * threshold["support"]
        
        bullish_break = current_price > resistance_target
        bearish_break = current_price < support_target
        
        result = {
            "threshold_name": threshold["name"],
            "resistance_threshold": threshold["resistance"],
            "support_threshold": threshold["support"],
            "bullish_break": bullish_break,
            "bearish_break": bearish_break,
            "any_break": bullish_break or bearish_break
        }
        
        results.append(result)
        
        print(f"   📊 {threshold['name']:15} - Bullish: {bullish_break:5} | Bearish: {bearish_break:5} | Any: {bullish_break or bearish_break}")
    
    return results

def main():
    """🚀 Función principal de investigación"""
    
    print("=" * 80)
    print("🔍 INVESTIGACIÓN PROFUNDA: ¿POR QUÉ NO SE DETECTAN BOS?")
    print("=" * 80)
    
    # Configuración
    symbols = ['EURUSD', 'GBPUSD', 'USDJPY']
    data_periods = 5000
    
    # Inicializar componentes
    print("\n📊 Inicializando componentes...")
    downloader = AdvancedCandleDownloader()
    analyzer = MultiTimeframeAnalyzer()
    
    investigation_results = {}
    
    for symbol in symbols:
        print(f"\n{'='*80}")
        print(f"🔍 INVESTIGANDO {symbol}")
        print(f"{'='*80}")
        
        try:
            # Descargar datos reales
            print(f"⬇️  Descargando {data_periods} velas de {symbol}...")
            
            async def download_data():
                return await downloader.download_historical_data(
                    symbol=symbol,
                    timeframe='M15',
                    bars=data_periods,
                    source_priority=['fundednext_mt5']
                )
            
            data = asyncio.run(download_data())
            
            if data is None or len(data) == 0:
                print(f"❌ No se pudieron descargar datos para {symbol}")
                continue
            
            print(f"✅ Descargados {len(data)} registros para {symbol}")
            
            # Análisis de calidad de datos
            data_quality = analyze_data_quality(data, symbol)
            print(f"\n📊 CALIDAD DE DATOS:")
            print(f"   📅 Rango: {data_quality['date_range']['start']} a {data_quality['date_range']['end']}")
            print(f"   📊 Total velas: {data_quality['total_bars']}")
            print(f"   💰 Precio actual: {data_quality['price_analysis']['current_price']}")
            print(f"   📈 Rango total: {data_quality['price_analysis']['range_percentage']:.3f}%")
            print(f"   📊 Volatilidad diaria: {data_quality['volatility']['daily_volatility']:.4f}%")
            print(f"   📈 Tendencia reciente: {data_quality['volatility']['recent_trend']:.3f}%")
            
            # Análisis detallado de BOS
            bos_analysis = detailed_bos_analysis(data, symbol, analyzer)
            
            # Prueba de umbrales
            threshold_results = test_threshold_sensitivity(data, symbol)
            
            # Almacenar resultados
            investigation_results[symbol] = {
                "data_quality": data_quality,
                "bos_analysis": bos_analysis,
                "threshold_results": threshold_results
            }
            
        except Exception as e:
            print(f"❌ Error investigando {symbol}: {e}")
            import traceback
            traceback.print_exc()
    
    # Resumen final e investigación
    print(f"\n{'='*80}")
    print(f"📋 RESUMEN DE INVESTIGACIÓN")
    print(f"{'='*80}")
    
    total_symbols = len(investigation_results)
    symbols_with_breaks = 0
    
    for symbol, results in investigation_results.items():
        manual_analysis = results["bos_analysis"]["manual_analysis"]
        
        print(f"\n📊 {symbol}:")
        print(f"   🎯 BOS por analyzer: {results['bos_analysis']['analyzer_result'].get('bos_detected', False)}")
        print(f"   📈 Break manual bullish: {manual_analysis['bullish_break']}")
        print(f"   📉 Break manual bearish: {manual_analysis['bearish_break']}")
        print(f"   📏 Distancia a resistencia: {manual_analysis['distance_to_resistance']:.3f}%")
        print(f"   📏 Distancia a soporte: {manual_analysis['distance_to_support']:.3f}%")
        print(f"   📊 Tamaño de rango: {manual_analysis['range_size']:.3f}%")
        print(f"   📜 Breakouts históricos: {manual_analysis['historical_breakouts']}")
        
        if manual_analysis['bullish_break'] or manual_analysis['bearish_break']:
            symbols_with_breaks += 1
    
    print(f"\n🔍 CONCLUSIONES:")
    print(f"   📊 Símbolos analizados: {total_symbols}")
    print(f"   🎯 Símbolos con breaks manuales: {symbols_with_breaks}")
    print(f"   📊 Tasa de break manual: {symbols_with_breaks/total_symbols*100:.1f}%")
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    
    if symbols_with_breaks == 0:
        print(f"   1. 🎛️ Los umbrales actuales (99.9%/100.1%) son DEMASIADO ESTRICTOS")
        print(f"   2. 📊 Considerar usar umbrales más relajados (99.95%/100.05%)")
        print(f"   3. 🔍 El mercado está en consolidación real - NO hay breakouts significativos")
        print(f"   4. ⏰ Probar con timeframes diferentes (M5, H1, H4)")
        print(f"   5. 📈 Ajustar ventanas de cálculo de soporte/resistencia")
    else:
        print(f"   1. ✅ Los breakouts existen - problema en la lógica del analyzer")
        print(f"   2. 🔧 Revisar la implementación de detectar_estructura_m15_optimizada")
        print(f"   3. 🐛 Posible bug en el cálculo de umbrales o condiciones")
        print(f"   4. 📊 Verificar que el analyzer use los mismos datos reales")
    
    print(f"\n🏁 Investigación completada")
    return investigation_results

if __name__ == "__main__":
    main()
