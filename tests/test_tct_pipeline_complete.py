#!/usr/bin/env python3
"""
🧪 TEST COMPLETO TCT PIPELINE - DÍA 2 SPRINT 1.2
==============================================

Validación completa del Time Cycle Tracking Pipeline después de las mejoras:
1. ✅ AggregatedTCTMetrics.to_dict() - Implementado correctamente
2. ✅ TCTAggregator.aggregate_recent_measurements() - Método crítico agregado
3. ✅ TCTInterface - TODOs reemplazados con lógica real
4. ✅ Integración con ICTDetector real del Sprint 1.2

Objetivo: Validar que el pipeline completo funciona end-to-end.
"""

import sys
from pathlib import Path
import time
import threading
import json

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    # 🔌 IMPORTS DEL TCT PIPELINE
    from core.analysis_command_center.tct_pipeline import (
        TCTInterface,
        TCTMeasurementEngine,
        TCTAggregator,
        TCTFormatter,
        TCTMetrics,
        AggregatedTCTMetrics
    )

    # 🔌 IMPORTS DEL ICT ENGINE
    from core.ict_engine import MarketContext
    from sistema.logging_interface import enviar_senal_log

    enviar_senal_log("INFO", "✅ Todos los imports del TCT Pipeline exitosos", "test_tct_pipeline_complete", "migration")

except ImportError as e:
    enviar_senal_log("ERROR", f"❌ Error en imports: {e}", "test_tct_pipeline_complete", "migration")
    sys.exit(1)

def test_aggregated_metrics_to_dict():
    """🧪 TEST 1: Validar que AggregatedTCTMetrics.to_dict() funciona correctamente"""
    enviar_senal_log("INFO", "\n" + "="*60, "test_tct_pipeline_complete", "migration")
    enviar_senal_log("INFO", "🧪 TEST 1: AggregatedTCTMetrics.to_dict(, "test_tct_pipeline_complete", "migration")")
    enviar_senal_log("INFO", "="*60, "test_tct_pipeline_complete", "migration")

    try:
        # Crear métricas de prueba
        metrics = AggregatedTCTMetrics()
        metrics.global_avg_tct_ms = 150.5
        metrics.global_max_tct_ms = 300.0
        metrics.global_min_tct_ms = 50.0
        metrics.tct_trend = "IMPROVING"
        metrics.performance_grade = "B"
        metrics.measurements_per_minute = 4.2
        metrics.analysis_frequency_hz = 0.07
        metrics.total_timeframes = 3
        metrics.active_sessions = ["LONDON", "NEWYORK"]

        # Ejecutar to_dict()
        result_dict = metrics.to_dict()

        # Validaciones
        assert isinstance(result_dict, dict), "El resultado debe ser un diccionario"
        assert result_dict['global_avg_tct_ms'] == 150.5, "Avg TCT incorrecto"
        assert result_dict['performance_grade'] == "B", "Grade incorrecto"
        assert result_dict['total_timeframes'] == 3, "Total timeframes incorrecto"
        assert len(result_dict['active_sessions']) == 2, "Active sessions incorrecto"

        enviar_senal_log("INFO", "✅ AggregatedTCTMetrics.to_dict(, "test_tct_pipeline_complete", "migration") funciona correctamente")
        enviar_senal_log("INFO", f"📊 Resultado: {len(result_dict, "test_tct_pipeline_complete", "migration")} campos en el diccionario")
        enviar_senal_log("INFO", f"🎯 Grade: {result_dict['performance_grade']}, Trend: {result_dict['tct_trend']}", "test_tct_pipeline_complete", "migration")

        return True

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en test AggregatedTCTMetrics.to_dict(, "test_tct_pipeline_complete", "migration"): {e}")
        return False

def test_tct_aggregator_recent_measurements():
    """🧪 TEST 2: Validar aggregate_recent_measurements()"""
    enviar_senal_log("INFO", "\n" + "="*60, "test_tct_pipeline_complete", "migration")
    enviar_senal_log("INFO", "🧪 TEST 2: TCTAggregator.aggregate_recent_measurements(, "test_tct_pipeline_complete", "migration")")
    enviar_senal_log("INFO", "="*60, "test_tct_pipeline_complete", "migration")

    try:
        aggregator = TCTAggregator()

        # Simular métricas para múltiples timeframes
        timeframes = ["M5", "H1", "H4"]

        for tf in timeframes:
            for i in range(10):  # 10 mediciones por timeframe
                metrics = TCTMetrics()
                metrics.avg_tct_ms = 100 + i * 10  # Variación realista
                metrics.max_tct_ms = metrics.avg_tct_ms + 50
                metrics.min_tct_ms = metrics.avg_tct_ms - 30
                metrics.measurements_taken = i + 1
                metrics.patterns_analyzed = i * 2
                metrics.pois_processed = i * 3

                aggregator.add_metrics(tf, metrics, session="LONDON")
                time.sleep(0.01)  # Pequeña pausa para timestamps diferentes

        # Test del método crítico
        recent_aggregated = aggregator.aggregate_recent_measurements(
            timeframe="ALL",
            max_age_minutes=5,  # Solo últimos 5 minutos
            min_samples=3       # Mínimo 3 samples
        )

        # Validaciones
        assert recent_aggregated is not None, "Debe retornar métricas agregadas"
        assert recent_aggregated.total_timeframes > 0, "Debe procesar al menos un timeframe"
        assert recent_aggregated.global_avg_tct_ms > 0, "Debe calcular promedio global"
        assert recent_aggregated.performance_grade in ["A", "B", "C", "D", "F"], "Grade debe ser válido"

        enviar_senal_log("INFO", "✅ aggregate_recent_measurements(, "test_tct_pipeline_complete", "migration") funciona correctamente")
        enviar_senal_log("INFO", f"📊 Timeframes procesados: {recent_aggregated.total_timeframes}", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", f"🎯 Avg TCT: {recent_aggregated.global_avg_tct_ms:.2f}ms", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", f"📈 Grade: {recent_aggregated.performance_grade}", "test_tct_pipeline_complete", "migration")

        return True

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en test aggregate_recent_measurements(, "test_tct_pipeline_complete", "migration"): {e}")
        return False

def test_tct_measurement_engine():
    """🧪 TEST 3: Validar TCTMeasurementEngine básico"""
    enviar_senal_log("INFO", "\n" + "="*60, "test_tct_pipeline_complete", "migration")
    enviar_senal_log("INFO", "🧪 TEST 3: TCTMeasurementEngine", "test_tct_pipeline_complete", "migration")
    enviar_senal_log("INFO", "="*60, "test_tct_pipeline_complete", "migration")

    try:
        engine = TCTMeasurementEngine()

        # Test de mediciones básicas
        measurement_id = engine.start_measurement(
            "test_measurement",
            context={"symbol": "EURUSD", "timeframe": "H1"}
        )

        assert measurement_id is not None, "Debe retornar ID de medición"
        assert len(engine._active_measurements) == 1, "Debe registrar medición activa"

        # Simular trabajo
        time.sleep(0.05)  # 50ms

        # Finalizar medición
        duration = engine.end_measurement(measurement_id, results={"patterns_found": 3})

        assert duration > 0, "Debe retornar duración positiva"
        assert len(engine._active_measurements) == 0, "Debe limpiar mediciones activas"

        # Validar métricas
        metrics = engine.get_current_metrics()
        assert metrics.measurements_taken == 1, "Debe contar 1 medición"
        assert metrics.avg_tct_ms > 0, "Debe calcular tiempo promedio"

        enviar_senal_log("INFO", "✅ TCTMeasurementEngine funciona correctamente", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", f"⏱️ Duración medida: {duration:.2f}ms", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", f"📊 Métricas: {metrics.measurements_taken} mediciones tomadas", "test_tct_pipeline_complete", "migration")

        return True

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en test TCTMeasurementEngine: {e}", "test_tct_pipeline_complete", "migration")
        return False

def test_tct_interface_real_analysis():
    """🧪 TEST 4: Validar TCTInterface con análisis ICT real"""
    enviar_senal_log("INFO", "\n" + "="*60, "test_tct_pipeline_complete", "migration")
    enviar_senal_log("INFO", "🧪 TEST 4: TCTInterface con ICTDetector real", "test_tct_pipeline_complete", "migration")
    enviar_senal_log("INFO", "="*60, "test_tct_pipeline_complete", "migration")

    try:
        tct_interface = TCTInterface(
            measurement_interval=0.5,  # Para test rápido
            aggregation_interval=2.0,
            enable_exports=False       # No exports en test
        )

        # Test de análisis único (el nuevo sin TODOs)
        result = tct_interface.measure_single_analysis(
            symbol="EURUSD",
            timeframe="H1",
            market_context=None  # Se creará automáticamente
        )

        # Validaciones del resultado real
        assert result is not None, "Debe retornar resultado de análisis"
        assert result['analysis_type'] == 'real_ict_analysis', "Debe usar análisis real (no simulado)"
        assert 'symbol' in result, "Debe incluir símbolo analizado"
        assert 'timeframe' in result, "Debe incluir timeframe"
        assert 'tct_ms' in result, "Debe incluir tiempo de análisis"
        assert 'pois_detected' in result, "Debe incluir POIs detectados"
        assert 'patterns_detected' in result, "Debe incluir patrones detectados"
        assert result['analysis_result']['analysis_type'] == 'real_ict_analysis', "Analysis result debe ser real"

        # Validar que el análisis usó ICTDetector real
        analysis_result = result['analysis_result']
        assert 'market_structure' in analysis_result, "Debe incluir estructura de mercado"
        assert 'market_bias' in analysis_result, "Debe incluir bias de mercado"
        assert 'confidence_score' in analysis_result, "Debe incluir score de confianza"

        enviar_senal_log("INFO", "✅ TCTInterface con ICTDetector real funciona correctamente", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", f"🚀 Análisis: {result['analysis_result']['analysis_type']}", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", f"📊 POIs detectados: {analysis_result['pois_detected']}", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", f"🧠 Patrones detectados: {analysis_result['patterns_detected']}", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", f"⏱️ TCT duration: {result['tct_ms']:.2f}ms", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", f"🎯 Confidence: {analysis_result['confidence_score']:.2f}", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", f"📈 Market structure: {analysis_result['market_structure']}", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", f"💰 Price analyzed: {analysis_result['price_analyzed']:.5f}", "test_tct_pipeline_complete", "migration")

        return True

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en test TCTInterface real analysis: {e}", "test_tct_pipeline_complete", "migration")
        import traceback
        traceback.print_exc()
        return False

def test_tct_formatter():
    """🧪 TEST 5: Validar TCTFormatter"""
    enviar_senal_log("INFO", "\n" + "="*60, "test_tct_pipeline_complete", "migration")
    enviar_senal_log("INFO", "🧪 TEST 5: TCTFormatter", "test_tct_pipeline_complete", "migration")
    enviar_senal_log("INFO", "="*60, "test_tct_pipeline_complete", "migration")

    try:
        formatter = TCTFormatter()

        # Crear métricas agregadas para formatear
        aggregated = AggregatedTCTMetrics()
        aggregated.global_avg_tct_ms = 180.5
        aggregated.performance_grade = "B"
        aggregated.total_timeframes = 2
        aggregated.tct_trend = "STABLE"

        # Test de formateo para dashboard
        dashboard_data = formatter.format_for_dashboard(aggregated)

        # Validaciones
        assert isinstance(dashboard_data, dict), "Debe retornar diccionario"
        assert 'tct_summary' in dashboard_data, "Debe incluir resumen TCT"
        assert 'tct_timeframes' in dashboard_data, "Debe incluir datos por timeframe"

        enviar_senal_log("INFO", "✅ TCTFormatter funciona correctamente", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", f"📊 Dashboard data keys: {list(dashboard_data.keys(, "test_tct_pipeline_complete", "migration"))}")
        enviar_senal_log("INFO", f"🎯 Grade en status: {dashboard_data['tct_status']['performance_grade']}", "test_tct_pipeline_complete", "migration")

        return True

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en test TCTFormatter: {e}", "test_tct_pipeline_complete", "migration")
        return False

def test_tct_pipeline_integration():
    """🧪 TEST 6: Validar integración completa del pipeline"""
    enviar_senal_log("INFO", "\n" + "="*60, "test_tct_pipeline_complete", "migration")
    enviar_senal_log("INFO", "🧪 TEST 6: Integración completa TCT Pipeline", "test_tct_pipeline_complete", "migration")
    enviar_senal_log("INFO", "="*60, "test_tct_pipeline_complete", "migration")

    try:
        # Crear todos los componentes
        tct_interface = TCTInterface(enable_exports=False)

        # Test de estado inicial
        status = tct_interface.get_current_tct_status()
        assert isinstance(status, dict), "Debe retornar estado como dict"
        assert 'is_running' in status, "Debe incluir estado de ejecución"

        # Test de data formateada para dashboard
        dashboard_data = tct_interface.get_formatted_dashboard_data()
        # Puede ser None si no hay datos aún, eso es válido

        enviar_senal_log("INFO", "✅ Integración completa del pipeline funciona", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", f"📊 Estado del pipeline: {status['is_running']}", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", f"📈 Total measurements: {status['total_measurements']}", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", f"🎯 Dashboard data disponible: {dashboard_data is not None}", "test_tct_pipeline_complete", "migration")

        return True

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en test integración completa: {e}", "test_tct_pipeline_complete", "migration")
        return False

def main():
    """Ejecutar todos los tests del TCT Pipeline"""
    enviar_senal_log("INFO", "🚀 INICIANDO TESTS COMPLETOS - TCT PIPELINE DÍA 2 SPRINT 1.2", "test_tct_pipeline_complete", "migration")
    enviar_senal_log("INFO", "=" * 80, "test_tct_pipeline_complete", "migration")

    tests = [
        ("AggregatedTCTMetrics.to_dict()", test_aggregated_metrics_to_dict),
        ("TCTAggregator.aggregate_recent_measurements()", test_tct_aggregator_recent_measurements),
        ("TCTMeasurementEngine", test_tct_measurement_engine),
        ("TCTInterface con ICTDetector real", test_tct_interface_real_analysis),
        ("TCTFormatter", test_tct_formatter),
        ("Integración completa", test_tct_pipeline_integration)
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error inesperado en {test_name}: {e}", "test_tct_pipeline_complete", "migration")
            results.append((test_name, False))

    # Resumen final
    enviar_senal_log("INFO", "\n" + "="*80, "test_tct_pipeline_complete", "migration")
    enviar_senal_log("INFO", "📋 RESUMEN DE TESTS - TCT PIPELINE COMPLETO", "test_tct_pipeline_complete", "migration")
    enviar_senal_log("INFO", "="*80, "test_tct_pipeline_complete", "migration")

    passed = 0
    total = len(results)

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        enviar_senal_log("INFO", f"{status} | {test_name}", "test_tct_pipeline_complete", "migration")
        if success:
            passed += 1

    enviar_senal_log("INFO", f"\n🎯 RESULTADO FINAL: {passed}/{total} tests pasaron", "test_tct_pipeline_complete", "migration")

    if passed == total:
        enviar_senal_log("INFO", "🎉 ¡TODOS LOS TESTS PASARON! TCT Pipeline Día 2 completado exitosamente", "test_tct_pipeline_complete", "migration")
        enviar_senal_log("INFO", "✅ Sprint 1.2 Día 2 - TCT Pipeline: 100% FUNCIONAL", "test_tct_pipeline_complete", "migration")
    else:
        enviar_senal_log("INFO", f"⚠️ {total - passed} tests fallaron. Revisar implementación.", "test_tct_pipeline_complete", "migration")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
