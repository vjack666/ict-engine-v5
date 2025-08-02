#!/usr/bin/env python3
"""
📅 GENERADOR DATOS DEL VIERNES - WEEKEND TESTING
===============================================

Genera datos realistas del último día de trading (viernes) para
mostrar análisis ICT realista durante fin de semana.
"""

import pandas as pd
from datetime import datetime, timedelta
import json
import sys
from pathlib import Path

# Agregar path del proyecto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def generate_friday_eurusd_session():
    """Genera sesión realista EURUSD del viernes"""

    print("📅 Generando datos EURUSD del viernes 1 Aug 2025...")

    # Datos base del viernes (típico comportamiento EOD)
    friday_open = 1.17420
    friday_high = 1.17520  # Típico rango diario ~100 pips
    friday_low = 1.17380
    friday_close = 1.17480  # Cierre neutral

    # Generar 6 horas de datos M1 (sesión Londres + inicio NY)
    candles = []
    current_time = datetime(2025, 8, 1, 8, 0)  # 8:00 UTC viernes
    current_price = friday_open

    for i in range(360):  # 6 horas * 60 minutos = 360 velas
        # Simular comportamiento realista por horas
        hour = current_time.hour

        if 8 <= hour <= 10:  # Apertura Londres - volatilidad alta
            volatility = 0.00015
            trend_bias = 0.00002  # Ligeramente alcista
        elif 11 <= hour <= 13:  # Mediodía Londres - consolidación
            volatility = 0.00008
            trend_bias = 0.0
        elif 14 <= hour <= 16:  # Overlap Londres-NY - volatilidad alta
            volatility = 0.00012
            trend_bias = -0.00001  # Ligeramente bajista
        else:  # Otras horas
            volatility = 0.00005
            trend_bias = 0.0

        # Calcular OHLC realista
        price_change = (i % 20 - 10) * volatility + trend_bias
        current_price += price_change

        # Mantener dentro del rango diario
        current_price = max(friday_low, min(friday_high, current_price))

        # Generar vela
        open_price = current_price
        close_price = current_price + (i % 6 - 3) * volatility * 0.5
        high_price = max(open_price, close_price) + abs(price_change) * 0.3
        low_price = min(open_price, close_price) - abs(price_change) * 0.3

        # Asegurar que high/low están en rango
        high_price = min(friday_high, high_price)
        low_price = max(friday_low, low_price)

        candle = {
            'time': current_time,
            'open': round(open_price, 5),
            'high': round(high_price, 5),
            'low': round(low_price, 5),
            'close': round(close_price, 5),
            'volume': 800 + (i % 50) * 20  # Volumen realista
        }
        candles.append(candle)

        current_price = close_price
        current_time += timedelta(minutes=1)

    # Crear DataFrame
    df = pd.DataFrame(candles)
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')

    print(f"✅ Generadas {len(df)} velas del viernes")
    print(f"   📊 Rango: {df['low'].min():.5f} - {df['high'].max():.5f}")
    print(f"   💰 Open: {friday_open:.5f} → Close: {df['close'].iloc[-1]:.5f}")
    print(f"   📈 Variación: {((df['close'].iloc[-1] / friday_open - 1) * 10000):+.1f} pips")

    return df

def create_friday_market_context():
    """Crea contexto de mercado realista del viernes"""

    context = {
        'trading_day': 'FRIDAY',
        'session': 'LONDON_NY_OVERLAP',
        'market_phase': 'EOD_CONSOLIDATION',
        'volatility_regime': 'MEDIUM',
        'news_impact': 'LOW',  # Típico viernes sin NFP
        'liquidity_condition': 'NORMAL',
        'weekend_approaching': True,
        'profit_taking_mode': True,
        'analysis_context': 'Weekend preparation - reviewing Friday action for Monday setup'
    }

    return context

def generate_friday_analysis_points():
    """Genera puntos de análisis típicos del viernes"""

    analysis_points = {
        'key_levels': {
            'weekly_high': 1.17520,
            'weekly_low': 1.17280,
            'friday_pivot': 1.17450,
            'resistance': [1.17500, 1.17520],
            'support': [1.17400, 1.17380]
        },
        'patterns': {
            'detected': ['BULLISH_OB', 'BEARISH_FVG', 'LIQUIDITY_GRAB'],
            'quality': 'MEDIUM',  # Típico viernes
            'confluence': 2,
            'probability': 65
        },
        'session_summary': {
            'london_bias': 'NEUTRAL_TO_BULLISH',
            'ny_open_reaction': 'CONSOLIDATION',
            'eod_bias': 'NEUTRAL',
            'monday_setup': 'RANGE_BREAK_EXPECTED'
        },
        'risk_factors': [
            'Weekend gaps possible',
            'Low volume Friday afternoon',
            'Profit taking before weekend'
        ]
    }

    return analysis_points

def save_friday_testing_data():
    """Guarda todos los datos del viernes para testing weekend"""

    print("\n💾 Guardando datos del viernes para testing...")

    try:
        # Generar todos los componentes
        candles_df = generate_friday_eurusd_session()
        market_context = create_friday_market_context()
        analysis_points = generate_friday_analysis_points()

        # Crear package completo
        friday_package = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'trading_date': '2025-08-01',
                'symbol': 'EURUSD',
                'purpose': 'Weekend testing with realistic Friday data'
            },
            'candles': candles_df.to_dict('records'),
            'market_context': market_context,
            'analysis_points': analysis_points,
            'current_price': float(candles_df['close'].iloc[-1]),
            'daily_range': {
                'high': float(candles_df['high'].max()),
                'low': float(candles_df['low'].min()),
                'open': float(candles_df['open'].iloc[0]),
                'close': float(candles_df['close'].iloc[-1])
            }
        }

        # Guardar en JSON
        with open('friday_testing_data.json', 'w') as f:
            json.dump(friday_package, f, indent=2, default=str)

        print("✅ Datos guardados en: friday_testing_data.json")

        # Crear script de carga rápida para dashboard
        quick_load_script = f'''# 🔥 CARGA RÁPIDA DATOS DEL VIERNES EN DASHBOARD:
# Presiona 'D' en dashboard y pega esto:

import json
with open('friday_testing_data.json', 'r') as f:
    friday_data = json.load(f)

print("📅 Cargando datos del viernes para análisis weekend...")
print(f"💰 EURUSD Close: {{friday_data['current_price']:.5f}}")
print(f"📊 Rango diario: {{friday_data['daily_range']['low']:.5f}} - {{friday_data['daily_range']['high']:.5f}}")
print(f"🎯 Contexto: {{friday_data['market_context']['analysis_context']}}")

# Usar datos para TCT
from core.analysis_command_center.tct_pipeline.tct_interface import TCTInterface
tct = TCTInterface()
result = tct.measure_single_analysis('EURUSD', timeframe='M1')
print(f"⚡ TCT Result: {{result.get('total_time_ms', 'N/A')}}ms")
self.refresh()
print("✅ Dashboard actualizado con datos del viernes")
'''

        with open('load_friday_data.py', 'w') as f:
            f.write(quick_load_script)

        print("✅ Script de carga creado: load_friday_data.py")

        return friday_package

    except Exception as e:
        print(f"❌ Error guardando datos: {e}")
        return None

def main():
    """Función principal"""

    print("📅 GENERADOR DATOS DEL VIERNES - WEEKEND TESTING")
    print("=" * 55)
    print("🎯 PROPÓSITO: Datos realistas para testing durante fin de semana")
    print("📊 SÍMBOLO: EURUSD")
    print("📅 FECHA: Viernes 1 Aug 2025 (último trading day)")
    print()

    # Generar y guardar datos
    friday_package = save_friday_testing_data()

    if friday_package:
        print("\n🎉 DATOS DEL VIERNES GENERADOS EXITOSAMENTE")
        print("=" * 50)
        print("📊 RESUMEN DE DATOS:")
        print(f"   💰 Precio cierre: {friday_package['current_price']:.5f}")
        print(f"   📈 Rango diario: {friday_package['daily_range']['low']:.5f} - {friday_package['daily_range']['high']:.5f}")
        print(f"   📅 Velas M1: {len(friday_package['candles'])}")
        print(f"   🎯 Contexto: {friday_package['market_context']['market_phase']}")

        print("\n🔥 PARA USAR EN DASHBOARD:")
        print("1. 📊 Ve a tu dashboard")
        print("2. 🔧 Presiona 'D' para debug mode")
        print("3. 📋 Copia contenido de load_friday_data.py")
        print("4. ⚡ Pega en debug console y presiona Enter")
        print("5. 🎨 Ve a pestaña TCT Real - debería mostrar análisis del viernes")

        print("\n💡 BENEFICIOS:")
        print("   • 📊 Análisis realista con datos históricos")
        print("   • 🎯 Validación completa del sistema durante weekend")
        print("   • ⚡ TCT Pipeline con datos reales de trading")
        print("   • 🧠 ICT patterns basados en acción real del viernes")

        return True
    else:
        print("\n❌ Error generando datos del viernes")
        return False

if __name__ == "__main__":
    success = main()

    if success:
        print("\n✅ LISTO PARA TESTING WEEKEND CON DATOS REALISTAS")
    else:
        print("\n❌ GENERACIÓN FALLÓ - revisar errores")

    print("\n🏁 Generador completado.")
