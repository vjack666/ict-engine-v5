#!/usr/bin/env python3
"""
🚀 TEST FRACTAL ANALYZER - Con Datos Reales MT5
==============================================

Test del FractalAnalyzer usando datos reales descargados desde MT5
a través del sistema mt5_data_manager existente.

Autor: ICT Engine Team
Fecha: 02 Agosto 2025
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Añadir el path del proyecto al PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# MIGRADO A SLUC v2.1
from sistema.logging_interface import enviar_senal_log

def test_con_datos_reales_mt5():
    """Test del FractalAnalyzer con datos reales del MT5"""

    enviar_senal_log("INFO", "🚀 === TEST FRACTAL CON DATOS REALES MT5 ===", __name__, "test")

    try:
        # Importar sistema de datos
        from utils.mt5_data_manager import cargar_datos_historicos_unificado
        from core.ict_engine.fractal_analyzer import FractalAnalyzer

        enviar_senal_log("INFO", "📡 Descargando datos reales desde MT5...", __name__, "test")

        # Descargar datos M15 reales
        df_m15 = cargar_datos_historicos_unificado('M15', lookback=200, symbol='EURUSD')

        if df_m15 is None or len(df_m15) == 0:
            enviar_senal_log("ERROR", "❌ No se pudieron descargar datos M15 desde MT5", __name__, "test")
            return False

        enviar_senal_log("INFO", f"✅ Datos M15 descargados: {len(df_m15)} velas", __name__, "test")
        enviar_senal_log("INFO", f"📊 Rango temporal: {df_m15.index[0]} hasta {df_m15.index[-1]}", __name__, "test")
        enviar_senal_log("INFO", f"💰 Precio actual: {df_m15.iloc[-1]['close']:.5f}", __name__, "test")

        # Crear analyzer
        analyzer = FractalAnalyzer()
        current_price = df_m15.iloc[-1]['close']

        # Ejecutar análisis fractal
        enviar_senal_log("INFO", "🔮 Ejecutando análisis fractal con datos reales...", __name__, "test")
        fractal_result = analyzer.analyze_fractal_range(df_m15, current_price)

        if fractal_result:
            enviar_senal_log("INFO", "✅ ¡FRACTAL CALCULADO CON DATOS REALES!", __name__, "test")
            enviar_senal_log("INFO", f"🔺 High: {fractal_result.high:.5f}", __name__, "test")
            enviar_senal_log("INFO", f"🔻 Low: {fractal_result.low:.5f}", __name__, "test")
            enviar_senal_log("INFO", f"⚖️ Equilibrium: {fractal_result.eq:.5f}", __name__, "test")
            enviar_senal_log("INFO", f"📊 Confianza: {fractal_result.confidence:.1f}%", __name__, "test")
            enviar_senal_log("INFO", f"🏆 Grado: {fractal_result.grade.value}", __name__, "test")
            enviar_senal_log("INFO", f"✅ Válido: {fractal_result.valid}", __name__, "test")
            enviar_senal_log("INFO", f"⏰ Edad: {fractal_result.age_minutes} minutos", __name__, "test")

            # Test de niveles
            levels = analyzer.get_fractal_levels()
            if levels:
                enviar_senal_log("INFO", f"📈 Niveles disponibles: {levels}", __name__, "test")

            # Test de EQ
            is_at_eq = analyzer.is_price_at_equilibrium(current_price)
            distance_to_eq = abs(current_price - fractal_result.eq)
            enviar_senal_log("INFO", f"🎯 ¿En zona EQ? {is_at_eq} (distancia: {distance_to_eq:.5f})", __name__, "test")

            return True
        else:
            enviar_senal_log("WARNING", "⚠️ No se pudo calcular fractal con datos reales", __name__, "test")
            return False

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en test con datos reales: {e}", __name__, "test")
        import traceback
        enviar_senal_log("ERROR", f"Traceback: {traceback.format_exc()}", __name__, "test")
        return False

def test_integracion_market_context_real():
    """Test de integración completa con MarketContext usando datos reales"""

    enviar_senal_log("INFO", "🚀 === TEST INTEGRACIÓN COMPLETA CON DATOS REALES ===", __name__, "test")

    try:
        from utils.mt5_data_manager import cargar_datos_historicos_unificado
        from core.ict_engine.ict_detector import MarketContext, update_market_context

        # Descargar datos multi-timeframe reales
        enviar_senal_log("INFO", "📡 Descargando datos multi-timeframe reales...", __name__, "test")

        df_h4 = cargar_datos_historicos_unificado('H4', lookback=100, symbol='EURUSD')
        df_m15 = cargar_datos_historicos_unificado('M15', lookback=300, symbol='EURUSD')
        df_m5 = cargar_datos_historicos_unificado('M5', lookback=500, symbol='EURUSD')

        if any(df is None for df in [df_h4, df_m15, df_m5]):
            enviar_senal_log("ERROR", "❌ No se pudieron descargar todos los timeframes", __name__, "test")
            return False

        enviar_senal_log("INFO", f"✅ Datos descargados: H4={len(df_h4)}, M15={len(df_m15)}, M5={len(df_m5)}", __name__, "test")

        # Crear contexto y datos para actualización
        context = MarketContext()
        current_price = df_m15.iloc[-1]['close']

        df_by_timeframe = {
            'H4': df_h4,
            'M15': df_m15,
            'M5': df_m5
        }

        enviar_senal_log("INFO", "🔄 Ejecutando actualización completa de contexto...", __name__, "test")

        # Actualizar contexto (esto incluye análisis fractal)
        update_market_context(context, df_by_timeframe, current_price)

        # Verificar resultados
        fractal_status = context.fractal_range.get('status', 'NO_CALCULADO')
        enviar_senal_log("INFO", f"📊 Estado fractal final: {fractal_status}", __name__, "test")

        if fractal_status not in ['NO_CALCULADO', 'CALCULANDO']:
            enviar_senal_log("INFO", "✅ ¡INTEGRACIÓN EXITOSA!", __name__, "test")
            enviar_senal_log("INFO", f"🔺 Fractal High: {context.fractal_range.get('high', 0):.5f}", __name__, "test")
            enviar_senal_log("INFO", f"🔻 Fractal Low: {context.fractal_range.get('low', 0):.5f}", __name__, "test")
            enviar_senal_log("INFO", f"⚖️ Fractal EQ: {context.fractal_range.get('eq', 0):.5f}", __name__, "test")
            enviar_senal_log("INFO", f"📈 Confianza: {context.fractal_range.get('confidence', 0):.1f}%", __name__, "test")
            enviar_senal_log("INFO", f"🏆 Grado: {context.fractal_range.get('grade', 'N/A')}", __name__, "test")

            # Mostrar también otros aspectos del contexto
            enviar_senal_log("INFO", f"📊 Bias H4: {context.h4_bias}", __name__, "test")
            enviar_senal_log("INFO", f"📊 Bias M15: {context.m15_bias}", __name__, "test")
            enviar_senal_log("INFO", f"🎯 POIs totales: {len(context.pois_h4) + len(context.pois_m15) + len(context.pois_m5)}", __name__, "test")

            return True
        else:
            enviar_senal_log("WARNING", "⚠️ Fractal no se calculó en la integración completa", __name__, "test")
            return False

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en integración completa: {e}", __name__, "test")
        import traceback
        enviar_senal_log("ERROR", f"Traceback: {traceback.format_exc()}", __name__, "test")
        return False

def main():
    """Ejecuta todos los tests con datos reales"""

    enviar_senal_log("INFO", "🚀 === INICIANDO TESTS CON DATOS REALES MT5 ===", __name__, "test")
    enviar_senal_log("INFO", "Utilizando sistema mt5_data_manager existente", __name__, "test")

    tests_passed = 0
    total_tests = 2

    # Test 1: Fractal analyzer con datos reales
    if test_con_datos_reales_mt5():
        tests_passed += 1
        enviar_senal_log("INFO", "✅ TEST 1 PASADO: FractalAnalyzer con datos reales", __name__, "test")
    else:
        enviar_senal_log("ERROR", "❌ TEST 1 FALLIDO: FractalAnalyzer con datos reales", __name__, "test")

    # Test 2: Integración completa
    if test_integracion_market_context_real():
        tests_passed += 1
        enviar_senal_log("INFO", "✅ TEST 2 PASADO: Integración completa", __name__, "test")
    else:
        enviar_senal_log("ERROR", "❌ TEST 2 FALLIDO: Integración completa", __name__, "test")

    # Resultado final
    enviar_senal_log("INFO", f"🏁 === RESULTADO FINAL: {tests_passed}/{total_tests} TESTS PASADOS ===", __name__, "test")

    if tests_passed == total_tests:
        enviar_senal_log("INFO", "🎉 ¡TODOS LOS TESTS CON DATOS REALES PASARON!", __name__, "test")
        enviar_senal_log("INFO", "✅ FractalAnalyzer integrado y funcionando con datos MT5", __name__, "test")
        return True
    else:
        enviar_senal_log("ERROR", f"⚠️ {total_tests - tests_passed} test(s) fallaron con datos reales", __name__, "test")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
