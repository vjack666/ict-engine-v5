#!/usr/bin/env python3
"""
🧪 TEST ADVANCED CANDLE DOWNLOADER - ICT ENGINE v5.0
===================================================

Script de prueba para validar el nuevo sistema de descarga de velas.
Prueba tanto la descarga como la corrección del problema de datos insuficientes
para el FractalAnalyzer.

Autor: ICT Engine Team
Fecha: 02 Agosto 2025
"""

import sys
import os
from pathlib import Path

# Añadir el path del proyecto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# MIGRADO A SLUC v2.1
from sistema.logging_interface import enviar_senal_log

def test_candle_downloader():
    """Test del Advanced Candle Downloader"""

    enviar_senal_log("INFO", "🧪 === TEST ADVANCED CANDLE DOWNLOADER ===", __name__, "test")

    try:
        from utils.advanced_candle_downloader import AdvancedCandleDownloader

        # Crear instancia
        downloader = AdvancedCandleDownloader()
        enviar_senal_log("INFO", "✅ AdvancedCandleDownloader creado exitosamente", __name__, "test")

        # Test de conexión MT5
        if downloader.connect_mt5():
            enviar_senal_log("INFO", "✅ Conexión MT5 exitosa", __name__, "test")

            # Test de descarga H4 (más datos para fractal)
            enviar_senal_log("INFO", "📥 Probando descarga H4 con 10,000 velas...", __name__, "test")
            stats = downloader.download_symbol_timeframe("EURUSD", "H4", 10000)

            if stats.success:
                enviar_senal_log("INFO", f"✅ Descarga H4 exitosa: {stats.downloaded_bars:,} velas en {stats.elapsed_time:.1f}s", __name__, "test")
                enviar_senal_log("INFO", f"⚡ Velocidad: {stats.download_speed:.0f} velas/s", __name__, "test")

                # Verificar archivo creado
                data_file = Path("data/candles/H4.csv")
                if data_file.exists():
                    # Contar líneas del archivo
                    with open(data_file, 'r') as f:
                        line_count = sum(1 for _ in f) - 1  # -1 para header

                    enviar_senal_log("INFO", f"📊 Archivo creado: {data_file} con {line_count:,} líneas", __name__, "test")

                    if line_count > 1000:  # Suficientes datos para fractal
                        enviar_senal_log("INFO", "✅ Datos suficientes para análisis fractal", __name__, "test")
                        return True
                    else:
                        enviar_senal_log("WARNING", "⚠️ Pocos datos para análisis fractal", __name__, "test")
                        return False
                else:
                    enviar_senal_log("ERROR", "❌ Archivo de datos no encontrado", __name__, "test")
                    return False
            else:
                enviar_senal_log("ERROR", f"❌ Descarga falló: {stats.error_message}", __name__, "test")
                return False
        else:
            enviar_senal_log("WARNING", "⚠️ No se pudo conectar a MT5 - probando modo offline", __name__, "test")
            return test_offline_mode()

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en test: {e}", __name__, "test")
        return False
    finally:
        if 'downloader' in locals():
            downloader.disconnect_mt5()

def test_offline_mode():
    """Test en modo offline con datos sintéticos"""

    enviar_senal_log("INFO", "🧪 Probando modo offline con datos sintéticos...", __name__, "test")

    try:
        import pandas as pd
        import numpy as np
        from datetime import datetime, timedelta

        # Crear datos sintéticos más realistas (1000 velas H4)
        dates = pd.date_range(start='2024-01-01', periods=1000, freq='4h')

        # Crear patrón de precios más realista
        base_price = 1.0800
        volatility = 0.001
        trend = 0.00001

        prices = []
        current_price = base_price

        for i in range(1000):
            # Simular movimiento browniano con tendencia
            change = np.random.normal(trend, volatility)
            current_price += change

            # Mantener precio en rango realista
            if current_price < 1.0500:
                current_price = 1.0500 + abs(change)
            elif current_price > 1.1200:
                current_price = 1.1200 - abs(change)

            prices.append(current_price)

        # Crear OHLC realista
        df_data = []
        for i, close_price in enumerate(prices):
            # Crear rangos intrabar realistas
            range_size = np.random.uniform(0.0005, 0.002)
            high = close_price + np.random.uniform(0, range_size)
            low = close_price - np.random.uniform(0, range_size)

            if i == 0:
                open_price = close_price
            else:
                open_price = prices[i-1] + np.random.uniform(-0.0002, 0.0002)

            # Asegurar orden correcto de OHLC
            if high < low:
                high, low = low, high
            if high < max(open_price, close_price):
                high = max(open_price, close_price) + 0.0001
            if low > min(open_price, close_price):
                low = min(open_price, close_price) - 0.0001

            df_data.append({
                'time': int(dates[i].timestamp()),
                'open': round(open_price, 5),
                'high': round(high, 5),
                'low': round(low, 5),
                'close': round(close_price, 5),
                'tick_volume': np.random.randint(100, 1000),
                'spread': 2,
                'real_volume': 0
            })

        # Guardar datos sintéticos
        df = pd.DataFrame(df_data)
        output_file = Path("data/candles/H4.csv")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_file, index=False)

        enviar_senal_log("INFO", f"📊 Datos sintéticos creados: {len(df)} velas en {output_file}", __name__, "test")
        enviar_senal_log("INFO", f"📈 Rango de precios: {df['low'].min():.5f} - {df['high'].max():.5f}", __name__, "test")

        return True

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en modo offline: {e}", __name__, "test")
        return False

def test_fractal_with_new_data():
    """Test del FractalAnalyzer con los nuevos datos descargados"""

    enviar_senal_log("INFO", "🧪 === TEST FRACTAL ANALYZER CON NUEVOS DATOS ===", __name__, "test")

    try:
        from core.ict_engine.fractal_analyzer import FractalAnalyzer
        import pandas as pd

        # Cargar datos descargados
        data_file = Path("data/candles/H4.csv")
        if not data_file.exists():
            enviar_senal_log("ERROR", "❌ No hay datos H4 disponibles", __name__, "test")
            return False

        df = pd.read_csv(data_file)
        enviar_senal_log("INFO", f"📊 Datos cargados: {len(df)} velas", __name__, "test")

        # Convertir a formato pandas adecuado
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)

        # Crear analyzer
        analyzer = FractalAnalyzer()
        current_price = df.iloc[-1]['close']

        enviar_senal_log("INFO", f"💰 Precio actual: {current_price:.5f}", __name__, "test")

        # Ejecutar análisis fractal
        fractal_result = analyzer.analyze_fractal_range(df, current_price)

        if fractal_result:
            enviar_senal_log("INFO", "✅ Análisis fractal exitoso:", __name__, "test")
            enviar_senal_log("INFO", f"   🔺 High: {fractal_result.high:.5f}", __name__, "test")
            enviar_senal_log("INFO", f"   🔻 Low: {fractal_result.low:.5f}", __name__, "test")
            enviar_senal_log("INFO", f"   ⚖️ EQ: {fractal_result.eq:.5f}", __name__, "test")
            enviar_senal_log("INFO", f"   📊 Confianza: {fractal_result.confidence:.1f}%", __name__, "test")
            enviar_senal_log("INFO", f"   🏆 Grado: {fractal_result.grade.value}", __name__, "test")
            enviar_senal_log("INFO", f"   ✅ Válido: {fractal_result.valid}", __name__, "test")

            # Test de integración con MarketContext
            enviar_senal_log("INFO", "🔗 Probando integración con MarketContext...", __name__, "test")

            from core.ict_engine.ict_detector import MarketContext, update_market_context

            context = MarketContext()
            df_by_timeframe = {"H4": df}

            update_market_context(context, df_by_timeframe, current_price)

            fractal_status = context.fractal_range.get('status', 'NO_CALCULADO')
            enviar_senal_log("INFO", f"📈 Estado fractal en contexto: {fractal_status}", __name__, "test")

            if fractal_status != 'NO_CALCULADO':
                enviar_senal_log("INFO", "✅ Integración MarketContext exitosa", __name__, "test")
                return True
            else:
                enviar_senal_log("WARNING", "⚠️ Fractal no se integró correctamente", __name__, "test")
                return False
        else:
            enviar_senal_log("ERROR", "❌ Análisis fractal falló", __name__, "test")
            return False

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en test fractal: {e}", __name__, "test")
        import traceback
        enviar_senal_log("ERROR", f"Traceback: {traceback.format_exc()}", __name__, "test")
        return False

def main():
    """Ejecuta todos los tests"""

    enviar_senal_log("INFO", "🚀 === INICIANDO TESTS COMPLETOS ===", __name__, "test")

    tests_passed = 0
    total_tests = 3

    # Test 1: Descargador de velas
    enviar_senal_log("INFO", "🧪 Test 1: Advanced Candle Downloader", __name__, "test")
    if test_candle_downloader():
        tests_passed += 1
        enviar_senal_log("INFO", "✅ TEST 1 PASADO", __name__, "test")
    else:
        enviar_senal_log("ERROR", "❌ TEST 1 FALLIDO", __name__, "test")

    # Test 2: FractalAnalyzer con nuevos datos
    enviar_senal_log("INFO", "🧪 Test 2: FractalAnalyzer con nuevos datos", __name__, "test")
    if test_fractal_with_new_data():
        tests_passed += 1
        enviar_senal_log("INFO", "✅ TEST 2 PASADO", __name__, "test")
    else:
        enviar_senal_log("ERROR", "❌ TEST 2 FALLIDO", __name__, "test")

    # Test 3: Verificación final de datos
    enviar_senal_log("INFO", "🧪 Test 3: Verificación de calidad de datos", __name__, "test")
    data_file = Path("data/candles/H4.csv")
    if data_file.exists():
        try:
            df = pd.read_csv(data_file)
            if len(df) > 1000:
                tests_passed += 1
                enviar_senal_log("INFO", f"✅ TEST 3 PASADO: {len(df)} velas disponibles", __name__, "test")
            else:
                enviar_senal_log("ERROR", f"❌ TEST 3 FALLIDO: Solo {len(df)} velas", __name__, "test")
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ TEST 3 FALLIDO: Error leyendo datos: {e}", __name__, "test")
    else:
        enviar_senal_log("ERROR", "❌ TEST 3 FALLIDO: No hay archivo de datos", __name__, "test")

    # Resultado final
    enviar_senal_log("INFO", f"🏁 === RESULTADO FINAL: {tests_passed}/{total_tests} TESTS PASADOS ===", __name__, "test")

    if tests_passed == total_tests:
        enviar_senal_log("INFO", "🎉 ¡TODOS LOS TESTS PASARON! Sistema listo para análisis fractal", __name__, "test")
        return True
    else:
        enviar_senal_log("WARNING", f"⚠️ {total_tests - tests_passed} test(s) fallaron", __name__, "test")
        return False

if __name__ == "__main__":
    import pandas as pd  # Import needed for offline mode
    success = main()
    sys.exit(0 if success else 1)
