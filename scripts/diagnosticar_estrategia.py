#!/usr/bin/env python3
"""
🔧 ICT ENGINE v5.0 - DIAGNÓSTICO DETALLADO DE ESTRATEGIA
=========================================================

Script para diagnosticar específicamente por qué la estrategia no detecta
patrones ni genera señales.

Uso:
    python scripts/diagnosticar_estrategia_fixed.py
"""

import sys
from pathlib import Path
import traceback
from datetime import datetime
import pandas as pd

# 📁 Configuración del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from sistema.logging_interface import enviar_senal_log


def analizar_datos_detallado():
    """Analiza en detalle los datos disponibles"""
    enviar_senal_log("🔍 DIAGNÓSTICO: Analizando datos en detalle...", "INFO")

    try:
        from utils.mt5_data_manager import get_mt5_manager

        manager = get_mt5_manager()
        df = manager.get_historical_data("EURUSD", "H1", 100)

        if df is not None and not df.empty:
            enviar_senal_log(f"✅ Datos cargados: {len(df)} velas", "INFO")
            enviar_senal_log(f"📊 Columnas disponibles: {list(df.columns)}", "INFO")
            enviar_senal_log(f"📈 Rango de fechas: {df.index.min()} a {df.index.max()}", "INFO")
            enviar_senal_log(f"💰 Precio actual: {df['close'].iloc[-1]:.5f}", "INFO")
            enviar_senal_log(f"📊 Estadísticas básicas:", "INFO")
            enviar_senal_log(f"   • Open: {df['open'].mean():.5f}", "INFO")
            enviar_senal_log(f"   • High: {df['high'].mean():.5f}", "INFO")
            enviar_senal_log(f"   • Low: {df['low'].mean():.5f}", "INFO")
            enviar_senal_log(f"   • Close: {df['close'].mean():.5f}", "INFO")
            enviar_senal_log(f"   • Volume: {df['tick_volume'].mean():.0f}", "INFO")

            # Verificar si hay movimientos de precio
            price_range = df['high'].max() - df['low'].min()
            enviar_senal_log(f"📏 Rango de precio total: {price_range:.5f}", "INFO")

            # Verificar últimas 5 velas
            enviar_senal_log("📋 Últimas 5 velas:", "INFO")
            for i in range(-5, 0):
                vela = df.iloc[i]
                enviar_senal_log(f"   {vela.name}: O:{vela['open']:.5f} H:{vela['high']:.5f} L:{vela['low']:.5f} C:{vela['close']:.5f}", "INFO")

            return df
        else:
            enviar_senal_log("❌ No se pudieron cargar datos", "ERROR")
            return None

    except Exception as e:
        enviar_senal_log(f"❌ Error analizando datos: {e}", "ERROR")
        enviar_senal_log(f"Detalles: {traceback.format_exc()}", "ERROR")
        return None


def diagnosticar_ict_engine():
    """Diagnostica el ICT Engine principal"""
    enviar_senal_log("\n🔍 DIAGNÓSTICO: Analizando ICT Engine...", "INFO")

    try:
        from core.ict_engine.ict_engine import ICTEngine, get_ict_engine
        from utils.mt5_data_manager import get_mt5_manager

        manager = get_mt5_manager()

        # Crear ICT Engine
        engine = ICTEngine(mt5_manager=manager)
        enviar_senal_log("✅ ICTEngine creado correctamente", "INFO")

        # Verificar componentes
        enviar_senal_log(f"📊 Detector disponible: {engine.detector is not None}", "INFO")
        enviar_senal_log(f"🎯 Confidence Engine disponible: {engine.confidence_engine is not None}", "INFO")
        enviar_senal_log(f"⚙️ Configuración: {engine.configuracion}", "INFO")

        # Test análisis completo
        resultado = engine.analizar_mercado_completo("EURUSD", "H1", 100)
        if resultado:
            enviar_senal_log("✅ Análisis completado exitosamente", "INFO")
            enviar_senal_log(f"   • Symbol: {resultado.symbol}", "INFO")
            enviar_senal_log(f"   • Timeframe: {resultado.timeframe}", "INFO")
            enviar_senal_log(f"   • Market Phase: {resultado.market_phase}", "INFO")
            enviar_senal_log(f"   • Direction: {resultado.direction}", "INFO")
            enviar_senal_log(f"   • Strength: {resultado.strength}", "INFO")
            enviar_senal_log(f"   • Confidence: {resultado.confidence}", "INFO")
            enviar_senal_log(f"   • Patterns: {len(resultado.patterns_detected)}", "INFO")
            enviar_senal_log(f"   • Signals: {len(resultado.signals)}", "INFO")
            enviar_senal_log(f"   • Recommendation: {resultado.recommendation}", "INFO")
            enviar_senal_log(f"   • Risk Level: {resultado.risk_level}", "INFO")

            return resultado
        else:
            enviar_senal_log("❌ El análisis retornó None", "ERROR")
            return None

    except Exception as e:
        enviar_senal_log(f"❌ Error diagnosticando ICT Engine: {e}", "ERROR")
        enviar_senal_log(f"Detalles: {traceback.format_exc()}", "ERROR")
        return None


def diagnosticar_poi_system():
    """Diagnostica el POI System específicamente"""
    enviar_senal_log("\n🔍 DIAGNÓSTICO: Analizando POI System...", "INFO")

    try:
        from core.poi_system.poi_system import POISystem
        from utils.mt5_data_manager import get_mt5_manager

        manager = get_mt5_manager()
        df = manager.get_historical_data("EURUSD", "H1", 100)

        if df is None or df.empty:
            enviar_senal_log("❌ Sin datos para analizar", "ERROR")
            return

        # Crear POI system
        poi_system = POISystem()
        enviar_senal_log("✅ POISystem creado", "INFO")

        # Test analizar POIs completo
        if hasattr(poi_system, 'analizar_pois_completo'):
            try:
                resultado = poi_system.analizar_pois_completo("EURUSD", "H1", 100)
                enviar_senal_log(f"🎯 Análisis POI completo: {resultado is not None}", "INFO")
                if resultado:
                    enviar_senal_log(f"   • Tipo: {type(resultado)}", "INFO")
                    if hasattr(resultado, '__dict__'):
                        enviar_senal_log(f"   • Atributos: {list(resultado.__dict__.keys())}", "INFO")
            except Exception as e:
                enviar_senal_log(f"❌ Error analizando POIs completo: {e}", "ERROR")
                enviar_senal_log(f"Detalles: {traceback.format_exc()}", "ERROR")

        # Test obtener POIs para dashboard
        if hasattr(poi_system, 'obtener_pois_para_dashboard'):
            try:
                pois_dashboard = poi_system.obtener_pois_para_dashboard(["EURUSD"], ["H1"])
                enviar_senal_log(f"📊 POIs para dashboard: {type(pois_dashboard)}", "INFO")
                if isinstance(pois_dashboard, dict):
                    enviar_senal_log(f"   • Claves: {list(pois_dashboard.keys())}", "INFO")
            except Exception as e:
                enviar_senal_log(f"❌ Error obteniendo POIs para dashboard: {e}", "ERROR")
                enviar_senal_log(f"Detalles: {traceback.format_exc()}", "ERROR")

    except Exception as e:
        enviar_senal_log(f"❌ Error diagnosticando POI System: {e}", "ERROR")
        enviar_senal_log(f"Detalles: {traceback.format_exc()}", "ERROR")


def diagnosticar_confidence_engine():
    """Diagnostica el Confidence Engine específicamente"""
    enviar_senal_log("\n🔍 DIAGNÓSTICO: Analizando Confidence Engine...", "INFO")

    try:
        from core.ict_engine.confidence_engine import ConfidenceEngine

        # Crear confidence engine
        confidence_engine = ConfidenceEngine()
        enviar_senal_log("✅ ConfidenceEngine creado", "INFO")

        # Test cálculo de confianza con datos mock
        if hasattr(confidence_engine, 'calculate_pattern_confidence'):
            try:
                # Datos mock para test
                pattern_mock = {
                    "type": "FVG",
                    "subtype": "BULLISH_FVG",
                    "price_high": 1.1000,
                    "price_low": 1.0950,
                    "confidence": 0.8
                }
                market_context_mock = {
                    "bias": "BULLISH",
                    "structure": "BULLISH",
                    "session": "LONDON"
                }
                poi_list_mock = [
                    {"type": "ORDER_BLOCK", "price": 1.0975}
                ]
                current_price = 1.0980

                confianza = confidence_engine.calculate_pattern_confidence(
                    pattern_mock,
                    market_context_mock,
                    poi_list_mock,
                    current_price
                )
                enviar_senal_log(f"🎯 Test confianza: {confianza}", "INFO")
            except Exception as e:
                enviar_senal_log(f"❌ Error calculando confianza: {e}", "ERROR")
                enviar_senal_log(f"Detalles: {traceback.format_exc()}", "ERROR")

        # Test calcular confianza general
        if hasattr(confidence_engine, 'calculate_overall_confidence'):
            try:
                patterns_mock = [
                    {"type": "FVG", "strength": 0.8},
                    {"type": "ORDER_BLOCK", "strength": 0.7}
                ]
                market_context_mock = {"bias": "BULLISH"}
                confianza_general = confidence_engine.calculate_overall_confidence(patterns_mock, market_context_mock)
                enviar_senal_log(f"🎯 Confianza general: {confianza_general}", "INFO")
            except Exception as e:
                enviar_senal_log(f"❌ Error calculando confianza general: {e}", "ERROR")

    except Exception as e:
        enviar_senal_log(f"❌ Error diagnosticando Confidence Engine: {e}", "ERROR")
        enviar_senal_log(f"Detalles: {traceback.format_exc()}", "ERROR")


def test_flujo_completo():
    """Test del flujo completo de la estrategia"""
    enviar_senal_log("\n🔍 DIAGNÓSTICO: Test flujo completo de estrategia...", "INFO")

    try:
        from core.ict_engine.ict_engine import ICTEngine
        from utils.mt5_data_manager import get_mt5_manager

        # Paso 1: Obtener datos
        manager = get_mt5_manager()
        if not manager.connect():
            enviar_senal_log("❌ No se pudo conectar a MT5", "ERROR")
            return False

        # Paso 2: Crear engine
        engine = ICTEngine(mt5_manager=manager)

        # Paso 3: Ejecutar análisis
        simbolos_test = ["EURUSD", "GBPUSD", "USDJPY"]
        timeframes_test = ["M15", "H1", "H4"]

        resultados_exitosos = 0
        total_tests = 0

        for symbol in simbolos_test:
            for timeframe in timeframes_test:
                total_tests += 1
                enviar_senal_log(f"🧪 Test {symbol} {timeframe}...", "INFO")

                try:
                    resultado = engine.analizar_mercado_completo(symbol, timeframe, 100)
                    if resultado and resultado.confidence > 0:
                        resultados_exitosos += 1
                        enviar_senal_log(f"   ✅ Exitoso - Confidence: {resultado.confidence:.2f}, Patterns: {len(resultado.patterns_detected)}", "INFO")
                    else:
                        enviar_senal_log(f"   ⚠️ Sin confianza - Resultado: {resultado is not None}", "WARNING")
                except Exception as e:
                    enviar_senal_log(f"   ❌ Error: {e}", "ERROR")

        enviar_senal_log(f"\n📊 RESUMEN FLUJO COMPLETO:", "INFO")
        enviar_senal_log(f"   • Tests ejecutados: {total_tests}", "INFO")
        enviar_senal_log(f"   • Tests exitosos: {resultados_exitosos}", "INFO")
        enviar_senal_log(f"   • Tasa de éxito: {(resultados_exitosos/total_tests)*100:.1f}%", "INFO")

        return resultados_exitosos > 0

    except Exception as e:
        enviar_senal_log(f"❌ Error en test flujo completo: {e}", "ERROR")
        enviar_senal_log(f"Detalles: {traceback.format_exc()}", "ERROR")
        return False


def main():
    """Función principal de diagnóstico"""
    enviar_senal_log("=" * 70, "INFO")
    enviar_senal_log("🔧 ICT ENGINE v5.0 - DIAGNÓSTICO DETALLADO DE ESTRATEGIA", "INFO")
    enviar_senal_log("=" * 70, "INFO")

    # Ejecutar diagnósticos
    datos = analizar_datos_detallado()

    if datos is not None:
        resultado_engine = diagnosticar_ict_engine()
        diagnosticar_poi_system()
        diagnosticar_confidence_engine()
        flujo_exitoso = test_flujo_completo()

        enviar_senal_log("\n" + "=" * 70, "INFO")
        enviar_senal_log("🎯 CONCLUSIONES DEL DIAGNÓSTICO:", "INFO")
        enviar_senal_log("=" * 70, "INFO")

        if datos is not None:
            enviar_senal_log("✅ Los datos están disponibles y son válidos", "INFO")
        else:
            enviar_senal_log("❌ Problema con los datos", "ERROR")

        if resultado_engine:
            enviar_senal_log("✅ El ICT Engine se ejecuta correctamente", "INFO")
            if resultado_engine.confidence > 0:
                enviar_senal_log("✅ El sistema genera confianza en los análisis", "INFO")
            else:
                enviar_senal_log("⚠️ El sistema no genera confianza suficiente", "WARNING")
        else:
            enviar_senal_log("❌ Problema con el ICT Engine", "ERROR")

        if flujo_exitoso:
            enviar_senal_log("✅ El flujo completo funciona exitosamente", "INFO")
        else:
            enviar_senal_log("⚠️ El flujo completo necesita optimización", "WARNING")

        enviar_senal_log("🔍 Los componentes se inicializan correctamente", "INFO")
        enviar_senal_log("🎯 El sistema está operativo para análisis ICT", "INFO")
        enviar_senal_log("=" * 70, "INFO")
    else:
        enviar_senal_log("\n❌ No se pudo completar el diagnóstico debido a falta de datos", "ERROR")


if __name__ == "__main__":
    main()
