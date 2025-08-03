#!/usr/bin/env python3
"""
🔧 DEBUG FRACTAL ANALYZER - Diagnóstico Específico
=================================================

Script para diagnosticar problemas específicos con el FractalAnalyzer.

Autor: ICT Engine Team
Fecha: 02 Agosto 2025
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Añadir el path del proyecto al PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# MIGRADO A SLUC v2.1
from sistema.logging_interface import enviar_senal_log

def crear_datos_simple():
    """Crea datos muy simples para debug"""

    # Crear solo 30 velas con patrón muy claro
    dates = pd.date_range(start='2025-08-01 08:00:00', periods=30, freq='15min')

    # Patrón simple: High en posición 15, Low en posición 10
    base_price = 1.0800
    prices = []

    for i in range(30):
        if i == 10:  # Swing Low claro
            price = base_price - 0.001
        elif i == 20:  # Swing High claro
            price = base_price + 0.001
        else:  # Precios normales
            price = base_price + np.random.uniform(-0.0001, 0.0001)

        prices.append(price)

    # Crear OHLC con swing points claros
    df_data = []
    for i, close_price in enumerate(prices):
        if i == 10:  # Low swing
            high = close_price + 0.00005
            low = close_price - 0.00005
            open_price = close_price + 0.00002
        elif i == 20:  # High swing
            high = close_price + 0.00005
            low = close_price - 0.00005
            open_price = close_price - 0.00002
        else:
            high = close_price + 0.00003
            low = close_price - 0.00003
            open_price = close_price

        volume = 500

        df_data.append({
            'open': open_price,
            'high': high,
            'low': low,
            'close': close_price,
            'volume': volume
        })

    df = pd.DataFrame(df_data, index=dates)
    return df

def debug_fractal_detection():
    """Debug paso a paso de detección de fractales"""

    enviar_senal_log("INFO", "🔧 === DEBUG: Detección de Fractales ===", __name__, "debug")

    try:
        from core.ict_engine.fractal_analyzer import FractalAnalyzer

        # Crear datos simples
        df_simple = crear_datos_simple()
        current_price = df_simple.iloc[-1]['close']

        enviar_senal_log("INFO", f"📊 Datos creados: {len(df_simple)} velas", __name__, "debug")
        enviar_senal_log("INFO", f"💰 Precio actual: {current_price:.5f}", __name__, "debug")
        enviar_senal_log("INFO", f"📈 Rango datos: H={df_simple['high'].max():.5f}, L={df_simple['low'].min():.5f}", __name__, "debug")

        # Debug del patrón creado
        for i in range(len(df_simple)):
            if i in [10, 20]:  # Nuestros swing points esperados
                enviar_senal_log("INFO", f"🎯 Swing esperado en vela {i}: H={df_simple.iloc[i]['high']:.5f}, L={df_simple.iloc[i]['low']:.5f}", __name__, "debug")

        # Crear analyzer
        analyzer = FractalAnalyzer()

        # DEBUG: Test paso a paso
        enviar_senal_log("INFO", "🔍 === PASO 1: Detección de Swing Points ===", __name__, "debug")

        # Llamar directamente al método interno para debug
        swing_highs, swing_lows = analyzer._detect_significant_swings(df_simple)

        enviar_senal_log("INFO", f"🔍 Swing Highs detectados: {len(swing_highs)}", __name__, "debug")
        for i, swing in enumerate(swing_highs):
            enviar_senal_log("INFO", f"   High {i}: Precio={swing.price:.5f}, Index={swing.index}, Fuerza={swing.strength:.5f}", __name__, "debug")

        enviar_senal_log("INFO", f"🔍 Swing Lows detectados: {len(swing_lows)}", __name__, "debug")
        for i, swing in enumerate(swing_lows):
            enviar_senal_log("INFO", f"   Low {i}: Precio={swing.price:.5f}, Index={swing.index}, Fuerza={swing.strength:.5f}", __name__, "debug")

        if not swing_highs or not swing_lows:
            enviar_senal_log("ERROR", "❌ No se detectaron swing points. Problema en algoritmo de detección.", __name__, "debug")
            return False

        enviar_senal_log("INFO", "🔍 === PASO 2: Análisis Fractal Completo ===", __name__, "debug")

        # Ejecutar análisis completo
        fractal_result = analyzer.analyze_fractal_range(df_simple, current_price)

        if fractal_result:
            enviar_senal_log("INFO", f"✅ Fractal calculado exitosamente:", __name__, "debug")
            enviar_senal_log("INFO", f"   🔺 High: {fractal_result.high:.5f}", __name__, "debug")
            enviar_senal_log("INFO", f"   🔻 Low: {fractal_result.low:.5f}", __name__, "debug")
            enviar_senal_log("INFO", f"   ⚖️ EQ: {fractal_result.eq:.5f}", __name__, "debug")
            enviar_senal_log("INFO", f"   📊 Confianza: {fractal_result.confidence:.1f}%", __name__, "debug")
            enviar_senal_log("INFO", f"   🏆 Grado: {fractal_result.grade.value}", __name__, "debug")
            enviar_senal_log("INFO", f"   ✅ Válido: {fractal_result.valid}", __name__, "debug")

            return True
        else:
            enviar_senal_log("ERROR", "❌ Análisis fractal falló - fractal_result es None", __name__, "debug")
            return False

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en debug de detección: {e}", __name__, "debug")
        import traceback
        enviar_senal_log("ERROR", f"Traceback: {traceback.format_exc()}", __name__, "debug")
        return False

def debug_market_context_integration():
    """Debug específico de integración con MarketContext"""

    enviar_senal_log("INFO", "🔧 === DEBUG: Integración MarketContext ===", __name__, "debug")

    try:
        from core.ict_engine.ict_detector import MarketContext

        # Crear contexto
        context = MarketContext()

        # Verificar inicialización del analyzer
        if hasattr(context, 'fractal_analyzer'):
            enviar_senal_log("INFO", f"✅ Atributo fractal_analyzer existe: {context.fractal_analyzer is not None}", __name__, "debug")
        else:
            enviar_senal_log("ERROR", "❌ Atributo fractal_analyzer NO existe", __name__, "debug")
            return False

        if context.fractal_analyzer is None:
            enviar_senal_log("ERROR", "❌ fractal_analyzer es None", __name__, "debug")
            return False

        # Test de actualización directa
        df_simple = crear_datos_simple()
        current_price = df_simple.iloc[-1]['close']

        enviar_senal_log("INFO", "🔍 Ejecutando actualización directa...", __name__, "debug")

        success = context.fractal_analyzer.update_fractal_context(context, df_simple, current_price)

        enviar_senal_log("INFO", f"📊 Resultado actualización: {success}", __name__, "debug")
        enviar_senal_log("INFO", f"📊 Estado fractal_range: {context.fractal_range}", __name__, "debug")

        return success

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en debug de integración: {e}", __name__, "debug")
        import traceback
        enviar_senal_log("ERROR", f"Traceback: {traceback.format_exc()}", __name__, "debug")
        return False

def main():
    """Ejecuta todos los debugs"""

    enviar_senal_log("INFO", "🔧 === INICIANDO DEBUG ESPECÍFICO FRACTAL ANALYZER ===", __name__, "debug")

    # Debug 1: Detección básica
    if debug_fractal_detection():
        enviar_senal_log("INFO", "✅ DEBUG 1 PASADO: Detección básica funciona", __name__, "debug")
    else:
        enviar_senal_log("ERROR", "❌ DEBUG 1 FALLIDO: Problema en detección básica", __name__, "debug")
        return False

    # Debug 2: Integración
    if debug_market_context_integration():
        enviar_senal_log("INFO", "✅ DEBUG 2 PASADO: Integración funciona", __name__, "debug")
    else:
        enviar_senal_log("ERROR", "❌ DEBUG 2 FALLIDO: Problema en integración", __name__, "debug")
        return False

    enviar_senal_log("INFO", "🎉 ¡TODOS LOS DEBUGS PASARON! Problema identificado y resuelto.", __name__, "debug")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
