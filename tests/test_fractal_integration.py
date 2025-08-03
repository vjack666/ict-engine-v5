#!/usr/bin/env python3
"""
🧪 TEST FRACTAL ANALYZER - Validación de Integración ICT
========================================================

Script de prueba para validar la integración del FractalAnalyzer
con el sistema ICT Engine v5.0 y MarketContext.

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

def crear_datos_test():
    """Crea datos sintéticos para prueba"""

    # Crear 100 velas de test con patrón fractal claro
    dates = pd.date_range(start='2025-08-01 08:00:00', periods=100, freq='15min')

    # Patrón sintético: tendencia alcista con swing high/low claros
    base_price = 1.0800
    prices = []

    for i in range(100):
        # Crear patrón con swing points claros
        if i < 20:  # Trending up
            price = base_price + (i * 0.0001) + np.random.normal(0, 0.00005)
        elif i < 40:  # Swing high
            price = base_price + 0.002 + np.random.normal(0, 0.00005)
        elif i < 60:  # Pullback (swing low)
            price = base_price + 0.001 + np.random.normal(0, 0.00005)
        elif i < 80:  # Recovery
            price = base_price + 0.0015 + np.random.normal(0, 0.00005)
        else:  # Current area
            price = base_price + 0.0012 + np.random.normal(0, 0.00005)

        prices.append(price)

    # Crear OHLC realista
    df_data = []
    for i, close_price in enumerate(prices):
        high = close_price + np.random.uniform(0.00001, 0.00005)
        low = close_price - np.random.uniform(0.00001, 0.00005)
        open_price = close_price + np.random.uniform(-0.00002, 0.00002)
        volume = np.random.randint(100, 1000)

        df_data.append({
            'open': open_price,
            'high': high,
            'low': low,
            'close': close_price,
            'volume': volume
        })

    df = pd.DataFrame(df_data, index=dates)
    return df

def test_fractal_analyzer_standalone():
    """Test del FractalAnalyzer de forma independiente"""

    enviar_senal_log("INFO", "🧪 === TEST 1: FractalAnalyzer Standalone ===", __name__, "test")

    try:
        from core.ict_engine.fractal_analyzer import FractalAnalyzer

        # Crear instancia
        analyzer = FractalAnalyzer()
        enviar_senal_log("INFO", "✅ FractalAnalyzer creado exitosamente", __name__, "test")

        # Crear datos de test
        df_test = crear_datos_test()
        current_price = df_test.iloc[-1]['close']

        enviar_senal_log("INFO", f"📊 Datos de test creados: {len(df_test)} velas, precio actual: {current_price:.5f}", __name__, "test")

        # Ejecutar análisis
        fractal_result = analyzer.analyze_fractal_range(df_test, current_price)

        if fractal_result:
            enviar_senal_log("INFO", f"✅ Fractal calculado: H={fractal_result.high:.5f}, L={fractal_result.low:.5f}, EQ={fractal_result.eq:.5f}", __name__, "test")
            enviar_senal_log("INFO", f"📈 Confianza: {fractal_result.confidence:.1f}% | Grado: {fractal_result.grade.value} | Estado: {fractal_result.status.value}", __name__, "test")

            # Test de niveles
            levels = analyzer.get_fractal_levels()
            if levels:
                enviar_senal_log("INFO", f"📊 Niveles obtenidos: {levels}", __name__, "test")

            # Test de equilibrium
            is_at_eq = analyzer.is_price_at_equilibrium(current_price)
            enviar_senal_log("INFO", f"🎯 ¿Precio en EQ? {is_at_eq}", __name__, "test")

            return True
        else:
            enviar_senal_log("WARNING", "⚠️ No se pudo calcular fractal con los datos de test", __name__, "test")
            return False

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en test standalone: {e}", __name__, "test")
        return False

def test_market_context_integration():
    """Test de integración con MarketContext"""

    enviar_senal_log("INFO", "🧪 === TEST 2: Integración con MarketContext ===", __name__, "test")

    try:
        from core.ict_engine.ict_detector import MarketContext, update_market_context

        # Crear MarketContext
        context = MarketContext()
        enviar_senal_log("INFO", "✅ MarketContext creado exitosamente", __name__, "test")

        # Verificar que el FractalAnalyzer está inicializado
        if hasattr(context, 'fractal_analyzer') and context.fractal_analyzer is not None:
            enviar_senal_log("INFO", "✅ FractalAnalyzer integrado en MarketContext", __name__, "test")
        else:
            enviar_senal_log("WARNING", "⚠️ FractalAnalyzer no disponible en MarketContext", __name__, "test")
            return False

        # Crear datos de test multi-timeframe
        df_test = crear_datos_test()
        current_price = df_test.iloc[-1]['close']

        df_by_timeframe = {
            'M15': df_test,
            'H4': df_test.resample('4h').agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        }

        enviar_senal_log("INFO", f"📊 Datos multi-timeframe preparados: M15={len(df_by_timeframe['M15'])}, H4={len(df_by_timeframe['H4'])}", __name__, "test")

        # Actualizar contexto (esto debería activar el análisis fractal)
        update_market_context(context, df_by_timeframe, current_price)

        # Verificar que el fractal se actualizó
        fractal_status = context.fractal_range.get('status', 'NO_CALCULADO')
        enviar_senal_log("INFO", f"📈 Estado fractal después de actualización: {fractal_status}", __name__, "test")

        if fractal_status != 'NO_CALCULADO':
            enviar_senal_log("INFO", f"✅ Fractal integrado: H={context.fractal_range.get('high', 0):.5f}, L={context.fractal_range.get('low', 0):.5f}, EQ={context.fractal_range.get('eq', 0):.5f}", __name__, "test")

            valid = context.fractal_range.get('valid', False)
            confidence = context.fractal_range.get('confidence', 0)
            grade = context.fractal_range.get('grade', 'N/A')

            enviar_senal_log("INFO", f"📊 Validez: {valid} | Confianza: {confidence:.1f}% | Grado: {grade}", __name__, "test")
            return True
        else:
            enviar_senal_log("WARNING", "⚠️ Fractal no se calculó en la integración", __name__, "test")
            return False

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en test de integración: {e}", __name__, "test")
        return False

def test_fractal_update_function():
    """Test de la función de conveniencia update_fractal_in_context"""

    enviar_senal_log("INFO", "🧪 === TEST 3: Función de Conveniencia ===", __name__, "test")

    try:
        from core.ict_engine.fractal_analyzer import update_fractal_in_context
        from core.ict_engine.ict_detector import MarketContext

        # Crear contexto limpio
        context = MarketContext()
        df_test = crear_datos_test()
        current_price = df_test.iloc[-1]['close']

        # Usar función de conveniencia
        success = update_fractal_in_context(context, df_test, current_price)

        if success:
            enviar_senal_log("INFO", "✅ Función de conveniencia ejecutada exitosamente", __name__, "test")

            fractal_status = context.fractal_range.get('status', 'NO_CALCULADO')
            enviar_senal_log("INFO", f"📈 Estado resultante: {fractal_status}", __name__, "test")
            return True
        else:
            enviar_senal_log("WARNING", "⚠️ Función de conveniencia falló", __name__, "test")
            return False

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en test de función de conveniencia: {e}", __name__, "test")
        return False

def main():
    """Ejecuta todos los tests de validación"""

    enviar_senal_log("INFO", "🚀 === INICIANDO TESTS DE VALIDACIÓN FRACTAL ANALYZER ===", __name__, "test")
    enviar_senal_log("INFO", "Validando integración completa con ICT Engine v5.0", __name__, "test")

    tests_passed = 0
    total_tests = 3

    # Test 1: FractalAnalyzer standalone
    if test_fractal_analyzer_standalone():
        tests_passed += 1
        enviar_senal_log("INFO", "✅ TEST 1 PASADO: FractalAnalyzer Standalone", __name__, "test")
    else:
        enviar_senal_log("ERROR", "❌ TEST 1 FALLIDO: FractalAnalyzer Standalone", __name__, "test")

    # Test 2: Integración con MarketContext
    if test_market_context_integration():
        tests_passed += 1
        enviar_senal_log("INFO", "✅ TEST 2 PASADO: Integración MarketContext", __name__, "test")
    else:
        enviar_senal_log("ERROR", "❌ TEST 2 FALLIDO: Integración MarketContext", __name__, "test")

    # Test 3: Función de conveniencia
    if test_fractal_update_function():
        tests_passed += 1
        enviar_senal_log("INFO", "✅ TEST 3 PASADO: Función de Conveniencia", __name__, "test")
    else:
        enviar_senal_log("ERROR", "❌ TEST 3 FALLIDO: Función de Conveniencia", __name__, "test")

    # Resultado final
    enviar_senal_log("INFO", f"🏁 === RESULTADO FINAL: {tests_passed}/{total_tests} TESTS PASADOS ===", __name__, "test")

    if tests_passed == total_tests:
        enviar_senal_log("INFO", "🎉 ¡TODOS LOS TESTS PASARON! FractalAnalyzer integrado exitosamente", __name__, "test")
        return True
    else:
        enviar_senal_log("ERROR", f"⚠️ {total_tests - tests_passed} test(s) fallaron. Revisar implementación.", __name__, "test")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
