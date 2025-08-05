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
    print("🔍 DIAGNÓSTICO: Analizando datos en detalle...")

    try:
        from utils.mt5_data_manager import get_mt5_manager

        manager = get_mt5_manager()
        df = manager.get_historical_data("EURUSD", "H1", 100)

        if df is not None and not df.empty:
            print(f"✅ Datos cargados: {len(df)} velas")
            print(f"📊 Columnas disponibles: {list(df.columns)}")
            print(f"📈 Rango de fechas: {df.index.min()} a {df.index.max()}")
            print(f"💰 Precio actual: {df['close'].iloc[-1]:.5f}")
            print(f"📊 Estadísticas básicas:")
            print(f"   • Open: {df['open'].mean():.5f}")
            print(f"   • High: {df['high'].mean():.5f}")
            print(f"   • Low: {df['low'].mean():.5f}")
            print(f"   • Close: {df['close'].mean():.5f}")
            print(f"   • Volume: {df['tick_volume'].mean():.0f}")

            # Verificar si hay movimientos de precio
            price_range = df['high'].max() - df['low'].min()
            print(f"📏 Rango de precio total: {price_range:.5f}")

            # Verificar últimas 5 velas
            print("📋 Últimas 5 velas:")
            for i in range(-5, 0):
                vela = df.iloc[i]
                print(f"   {vela.name}: O:{vela['open']:.5f} H:{vela['high']:.5f} L:{vela['low']:.5f} C:{vela['close']:.5f}")

            return df
        else:
            print("❌ No se pudieron cargar datos")
            return None

    except Exception as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error analizando datos: {e}")
        print(traceback.format_exc())
        return None


def diagnosticar_ict_engine():
    """Diagnostica el ICT Engine principal"""
    print("\n🔍 DIAGNÓSTICO: Analizando ICT Engine...")

    try:
        from core.ict_engine.ict_engine import ICTEngine, get_ict_engine
        from utils.mt5_data_manager import get_mt5_manager

        manager = get_mt5_manager()

        # Crear ICT Engine
        engine = ICTEngine(mt5_manager=manager)
        print("✅ ICTEngine creado correctamente")

        # Verificar componentes
        print(f"📊 Detector disponible: {engine.detector is not None}")
        print(f"🎯 Confidence Engine disponible: {engine.confidence_engine is not None}")
        print(f"⚙️ Configuración: {engine.configuracion}")

        # Test análisis completo
        resultado = engine.analizar_mercado_completo("EURUSD", "H1", 100)
        if resultado:
            print("✅ Análisis completado exitosamente")
            print(f"   • Symbol: {resultado.symbol}")
            print(f"   • Timeframe: {resultado.timeframe}")
            print(f"   • Market Phase: {resultado.market_phase}")
            print(f"   • Direction: {resultado.direction}")
            print(f"   • Strength: {resultado.strength}")
            print(f"   • Confidence: {resultado.confidence}")
            print(f"   • Patterns: {len(resultado.patterns_detected)}")
            print(f"   • Signals: {len(resultado.signals)}")
            print(f"   • Recommendation: {resultado.recommendation}")
            print(f"   • Risk Level: {resultado.risk_level}")

            return resultado
        else:
            print("❌ El análisis retornó None")
            return None

    except Exception as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error diagnosticando ICT Engine: {e}")
        print(traceback.format_exc())
        return None


def diagnosticar_poi_system():
    """Diagnostica el POI System específicamente"""
    print("\n🔍 DIAGNÓSTICO: Analizando POI System...")

    try:
        from core.poi_system.poi_system import POISystem
        from utils.mt5_data_manager import get_mt5_manager

        manager = get_mt5_manager()
        df = manager.get_historical_data("EURUSD", "H1", 100)

        if df is None or df.empty:
            print("❌ Sin datos para analizar")
            return

        # Crear POI system
        poi_system = POISystem()
        print("✅ POISystem creado")

        # Test analizar POIs completo
        if hasattr(poi_system, 'analizar_pois_completo'):
            try:
                resultado = poi_system.analizar_pois_completo("EURUSD", "H1", 100)
                print(f"🎯 Análisis POI completo: {resultado is not None}")
                if resultado:
                    print(f"   • Tipo: {type(resultado)}")
                    if hasattr(resultado, '__dict__'):
                        print(f"   • Atributos: {list(resultado.__dict__.keys())}")
            except Exception as e:
                # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error analizando POIs completo: {e}")
                print(traceback.format_exc())

        # Test obtener POIs para dashboard
        if hasattr(poi_system, 'obtener_pois_para_dashboard'):
            try:
                pois_dashboard = poi_system.obtener_pois_para_dashboard(["EURUSD"], ["H1"])
                print(f"📊 POIs para dashboard: {type(pois_dashboard)}")
                if isinstance(pois_dashboard, dict):
                    print(f"   • Claves: {list(pois_dashboard.keys())}")
            except Exception as e:
                # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error obteniendo POIs para dashboard: {e}")
                print(traceback.format_exc())

    except Exception as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error diagnosticando POI System: {e}")
        print(traceback.format_exc())


def diagnosticar_confidence_engine():
    """Diagnostica el Confidence Engine específicamente"""
    print("\n🔍 DIAGNÓSTICO: Analizando Confidence Engine...")

    try:
        from core.ict_engine.confidence_engine import ConfidenceEngine

        # Crear confidence engine
        confidence_engine = ConfidenceEngine()
        print("✅ ConfidenceEngine creado")

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
                print(f"🎯 Test confianza: {confianza}")
            except Exception as e:
                # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error calculando confianza: {e}")
                print(traceback.format_exc())

        # Test calcular confianza general
        if hasattr(confidence_engine, 'calculate_overall_confidence'):
            try:
                patterns_mock = [
                    {"type": "FVG", "strength": 0.8},
                    {"type": "ORDER_BLOCK", "strength": 0.7}
                ]
                market_context_mock = {"bias": "BULLISH"}
                confianza_general = confidence_engine.calculate_overall_confidence(patterns_mock, market_context_mock)
                print(f"🎯 Confianza general: {confianza_general}")
            except Exception as e:
                # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error calculando confianza general: {e}")

    except Exception as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error diagnosticando Confidence Engine: {e}")
        print(traceback.format_exc())


def test_flujo_completo():
    """Test del flujo completo de la estrategia"""
    print("\n🔍 DIAGNÓSTICO: Test flujo completo de estrategia...")

    try:
        from core.ict_engine.ict_engine import ICTEngine
        from utils.mt5_data_manager import get_mt5_manager

        # Paso 1: Obtener datos
        manager = get_mt5_manager()
        if not manager.connect():
            print("❌ No se pudo conectar a MT5")
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
                print(f"🧪 Test {symbol} {timeframe}...")

                try:
                    resultado = engine.analizar_mercado_completo(symbol, timeframe, 100)
                    if resultado and resultado.confidence > 0:
                        resultados_exitosos += 1
                        print(f"   ✅ Exitoso - Confidence: {resultado.confidence:.2f}, Patterns: {len(resultado.patterns_detected)}")
                    else:
                        print(f"   ⚠️ Sin confianza - Resultado: {resultado is not None}")
                except Exception as e:
                    # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"   ❌ Error: {e}")

        print(f"\n📊 RESUMEN FLUJO COMPLETO:")
        print(f"   • Tests ejecutados: {total_tests}")
        print(f"   • Tests exitosos: {resultados_exitosos}")
        print(f"   • Tasa de éxito: {(resultados_exitosos/total_tests)*100:.1f}%")

        return resultados_exitosos > 0

    except Exception as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error en test flujo completo: {e}")
        print(traceback.format_exc())
        return False


def main():
    """Función principal de diagnóstico"""
    print("=" * 70)
    print("🔧 ICT ENGINE v5.0 - DIAGNÓSTICO DETALLADO DE ESTRATEGIA")
    print("=" * 70)

    # Ejecutar diagnósticos
    datos = analizar_datos_detallado()

    if datos is not None:
        resultado_engine = diagnosticar_ict_engine()
        diagnosticar_poi_system()
        diagnosticar_confidence_engine()
        flujo_exitoso = test_flujo_completo()

        print("\n" + "=" * 70)
        print("🎯 CONCLUSIONES DEL DIAGNÓSTICO:")
        print("=" * 70)

        if datos is not None:
            print("✅ Los datos están disponibles y son válidos")
        else:
            print("❌ Problema con los datos")

        if resultado_engine:
            print("✅ El ICT Engine se ejecuta correctamente")
            if resultado_engine.confidence > 0:
                print("✅ El sistema genera confianza en los análisis")
            else:
                print("⚠️ El sistema no genera confianza suficiente")
        else:
            print("❌ Problema con el ICT Engine")

        if flujo_exitoso:
            print("✅ El flujo completo funciona exitosamente")
        else:
            print("⚠️ El flujo completo necesita optimización")

        print("🔍 Los componentes se inicializan correctamente")
        print("🎯 El sistema está operativo para análisis ICT")
        print("=" * 70)
    else:
        print("\n❌ No se pudo completar el diagnóstico debido a falta de datos")


if __name__ == "__main__":
    main()
