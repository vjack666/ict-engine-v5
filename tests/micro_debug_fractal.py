#!/usr/bin/env python3
"""
🔬 MICRO DEBUG FRACTAL - Análisis Granular
==========================================

Debug muy específico del algoritmo de detección de swing points.

Autor: ICT Engine Team
Fecha: 02 Agosto 2025
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Añadir el path del proyecto al PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sistema.logging_interface import enviar_senal_log

def crear_datos_ultra_simple():
    """Crear datos extremadamente simples para debug"""

    # Solo 15 velas con patrón obvio y rangos más grandes
    dates = pd.date_range(start='2025-08-01 08:00:00', periods=15, freq='15min')

    # Patrón con diferencias más grandes (500+ pips de diferencia)
    prices = [
        1.0800, 1.0750, 1.0700, 1.0650, 1.0600,  # Bajada fuerte al Low
        1.0650, 1.0700, 1.0750, 1.0850, 1.0900,  # Subida fuerte al High
        1.0850, 1.0800, 1.0750, 1.0725, 1.0750   # Bajada actual
    ]

    df_data = []
    for i, close_price in enumerate(prices):
        # Crear rangos realistas (10-20 pips por vela)
        high = close_price + 0.0010
        low = close_price - 0.0010
        open_price = close_price + np.random.uniform(-0.0005, 0.0005)
        volume = 100

        df_data.append({
            'open': open_price,
            'high': high,
            'low': low,
            'close': close_price,
            'volume': volume
        })

    df = pd.DataFrame(df_data, index=dates)

    # Log de los datos creados
    enviar_senal_log("INFO", "📊 Datos ultra-simples creados:", __name__, "debug")
    for i, row in df.iterrows():
        enviar_senal_log("INFO", f"   Vela {df.index.get_loc(i):2d}: H={row['high']:.5f}, L={row['low']:.5f}, C={row['close']:.5f}", __name__, "debug")

    return df

def debug_swing_detection_manual():
    """Debug manual del algoritmo de swing detection"""

    enviar_senal_log("INFO", "🔬 === MICRO DEBUG: Swing Detection Manual ===", __name__, "debug")

    df = crear_datos_ultra_simple()

    # Configuración ajustada para datos pequeños
    left_bars = 2  # Reducido de 5 a 2
    right_bars = 1  # Reducido de 2 a 1
    min_strength = 0.001  # Aumentado para ser más exigente

    enviar_senal_log("INFO", f"⚙️ Configuración: left_bars={left_bars}, right_bars={right_bars}, min_strength={min_strength}", __name__, "debug")

    swing_highs = []
    swing_lows = []

    # Rango de análisis
    start_idx = left_bars
    end_idx = len(df) - right_bars

    enviar_senal_log("INFO", f"🔍 Rango de análisis: desde índice {start_idx} hasta {end_idx}", __name__, "debug")

    for i in range(start_idx, end_idx):
        current_high = df.iloc[i]['high']
        current_low = df.iloc[i]['low']

        enviar_senal_log("INFO", f"🔍 Analizando vela {i}: H={current_high:.5f}, L={current_low:.5f}", __name__, "debug")

        # CHECK SWING HIGH
        is_swing_high = True

        # Verificar izquierda
        for j in range(i - left_bars, i):
            if df.iloc[j]['high'] >= current_high:
                is_swing_high = False
                enviar_senal_log("DEBUG", f"   ❌ High: vela {j} tiene high {df.iloc[j]['high']:.5f} >= {current_high:.5f}", __name__, "debug")
                break

        # Verificar derecha
        if is_swing_high:
            for j in range(i + 1, i + right_bars + 1):
                if df.iloc[j]['high'] >= current_high:
                    is_swing_high = False
                    enviar_senal_log("DEBUG", f"   ❌ High: vela {j} tiene high {df.iloc[j]['high']:.5f} >= {current_high:.5f}", __name__, "debug")
                    break

        if is_swing_high:
            enviar_senal_log("INFO", f"   ✅ SWING HIGH detectado en vela {i}: {current_high:.5f}", __name__, "debug")
            swing_highs.append({'index': i, 'price': current_high})

        # CHECK SWING LOW
        is_swing_low = True

        # Verificar izquierda
        for j in range(i - left_bars, i):
            if df.iloc[j]['low'] <= current_low:
                is_swing_low = False
                enviar_senal_log("DEBUG", f"   ❌ Low: vela {j} tiene low {df.iloc[j]['low']:.5f} <= {current_low:.5f}", __name__, "debug")
                break

        # Verificar derecha
        if is_swing_low:
            for j in range(i + 1, i + right_bars + 1):
                if df.iloc[j]['low'] <= current_low:
                    is_swing_low = False
                    enviar_senal_log("DEBUG", f"   ❌ Low: vela {j} tiene low {df.iloc[j]['low']:.5f} <= {current_low:.5f}", __name__, "debug")
                    break

        if is_swing_low:
            enviar_senal_log("INFO", f"   ✅ SWING LOW detectado en vela {i}: {current_low:.5f}", __name__, "debug")
            swing_lows.append({'index': i, 'price': current_low})

    enviar_senal_log("INFO", f"📊 RESUMEN: {len(swing_highs)} swing highs, {len(swing_lows)} swing lows", __name__, "debug")

    return len(swing_highs) > 0 and len(swing_lows) > 0

def debug_fractal_analyzer_step_by_step():
    """Debug usando el FractalAnalyzer real pero con datos simples"""

    enviar_senal_log("INFO", "🔬 === MICRO DEBUG: FractalAnalyzer Real ===", __name__, "debug")

    try:
        from core.ict_engine.fractal_analyzer import FractalAnalyzer

        df = crear_datos_ultra_simple()
        current_price = df.iloc[-1]['close']

        analyzer = FractalAnalyzer()

        # Debug configuración
        enviar_senal_log("INFO", f"⚙️ Config analyzer: {analyzer.config}", __name__, "debug")

        # Ejecutar detección manual
        enviar_senal_log("INFO", "🔍 Ejecutando _detect_significant_swings...", __name__, "debug")
        swing_highs, swing_lows = analyzer._detect_significant_swings(df)

        enviar_senal_log("INFO", f"📊 Resultado: {len(swing_highs)} highs, {len(swing_lows)} lows", __name__, "debug")

        if not swing_highs:
            enviar_senal_log("ERROR", "❌ No swing highs detectados", __name__, "debug")
        else:
            for i, swing in enumerate(swing_highs):
                enviar_senal_log("INFO", f"   High {i}: {swing.price:.5f} en índice {swing.index}", __name__, "debug")

        if not swing_lows:
            enviar_senal_log("ERROR", "❌ No swing lows detectados", __name__, "debug")
        else:
            for i, swing in enumerate(swing_lows):
                enviar_senal_log("INFO", f"   Low {i}: {swing.price:.5f} en índice {swing.index}", __name__, "debug")

        if swing_highs and swing_lows:
            # Continuar con el análisis
            enviar_senal_log("INFO", "🔍 Ejecutando análisis fractal completo...", __name__, "debug")
            result = analyzer.analyze_fractal_range(df, current_price)

            if result:
                enviar_senal_log("INFO", f"✅ Fractal exitoso: H={result.high:.5f}, L={result.low:.5f}, EQ={result.eq:.5f}", __name__, "debug")
                return True
            else:
                enviar_senal_log("ERROR", "❌ Análisis fractal falló en validación o confidence", __name__, "debug")
                return False
        else:
            enviar_senal_log("ERROR", "❌ No hay swing points suficientes", __name__, "debug")
            return False

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en analyzer: {e}", __name__, "debug")
        import traceback
        enviar_senal_log("ERROR", f"Traceback: {traceback.format_exc()}", __name__, "debug")
        return False

def main():
    """Ejecuta micro debug"""

    enviar_senal_log("INFO", "🔬 === MICRO DEBUG FRACTAL ANALYZER ===", __name__, "debug")

    # Debug 1: Manual
    if debug_swing_detection_manual():
        enviar_senal_log("INFO", "✅ DEBUG MANUAL: Algoritmo lógicamente correcto", __name__, "debug")
    else:
        enviar_senal_log("ERROR", "❌ DEBUG MANUAL: Problema en lógica", __name__, "debug")

    # Debug 2: FractalAnalyzer
    if debug_fractal_analyzer_step_by_step():
        enviar_senal_log("INFO", "✅ DEBUG ANALYZER: FractalAnalyzer funciona", __name__, "debug")
    else:
        enviar_senal_log("ERROR", "❌ DEBUG ANALYZER: Problema en implementación", __name__, "debug")

if __name__ == "__main__":
    main()
