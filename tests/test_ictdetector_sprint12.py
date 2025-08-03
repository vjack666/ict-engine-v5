from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
"""
🧪 TEST SPRINT 1.2 - ICTDetector IMPLEMENTACIÓN REAL
==================================================

Test completo para validar que la nueva implementación ICTDetector
funciona correctamente y está integrada en el sistema.

OBJETIVO: Verificar funcionalidad completa de producción
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Agregar paths del sistema
sys.path.append(str(Path(__file__).parent))

def test_ictdetector_integration():
    """Test de integración completa del ICTDetector real"""

    enviar_senal_log("INFO", "🧪 TEST SPRINT 1.2 - ICTDetector IMPLEMENTACIÓN REAL", "test_ictdetector_sprint12", "migration")
    enviar_senal_log("INFO", "=" * 65, "test_ictdetector_sprint12", "migration")
    enviar_senal_log("INFO", f"⏰ Timestamp: {datetime.now(, "test_ictdetector_sprint12", "migration").strftime('%Y-%m-%d %H:%M:%S')}")
    enviar_senal_log("INFO", , "test_ictdetector_sprint12", "migration")

    try:
        # 1. TEST IMPORT
        enviar_senal_log("INFO", "📦 1. Testeando imports...", "test_ictdetector_sprint12", "migration")
        from core.ict_engine.ict_detector import ICTDetector
        from core.ict_engine import ICTDetector as ICTDetector2  # Test desde __init__
        enviar_senal_log("INFO", "✅ ICTDetector importado correctamente desde ambas ubicaciones", "test_ictdetector_sprint12", "migration")

        # 2. TEST INICIALIZACIÓN
        enviar_senal_log("INFO", "\n🚀 2. Testeando inicialización...", "test_ictdetector_sprint12", "migration")
        detector = ICTDetector()
        assert detector.initialized == True, "Detector no inicializado correctamente"
        assert detector.analysis_count == 0, "Contador de análisis incorrecto"
        assert isinstance(detector.config, dict), "Configuración no es diccionario"
        enviar_senal_log("INFO", "✅ ICTDetector inicializado correctamente", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", f"   - Estado: {'Inicializado' if detector.initialized else 'No inicializado'}", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", f"   - Threshold: {detector.config['min_confidence_threshold']}", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", f"   - Max patterns: {detector.config['max_patterns_per_analysis']}", "test_ictdetector_sprint12", "migration")

        # 3. TEST DATOS SINTÉTICOS
        enviar_senal_log("INFO", "\n📊 3. Generando datos sintéticos de mercado...", "test_ictdetector_sprint12", "migration")
        # Generar datos OHLC sintéticos realistas
        np.random.seed(42)  # Para reproducibilidad
        n_candles = 100
        base_price = 1.1000

        dates = pd.date_range(start=datetime.now() - timedelta(hours=n_candles),
                             periods=n_candles, freq='h')  # Usar periods en lugar de end

        prices = []
        current_price = base_price

        for i in range(n_candles):
            # Simular movimiento de precio realista
            change = np.random.normal(0, 0.0005)  # Volatilidad realista para EURUSD
            current_price += change

            # Generar OHLC realista
            high_offset = abs(np.random.normal(0, 0.0002))
            low_offset = abs(np.random.normal(0, 0.0002))
            close_offset = np.random.normal(0, 0.0001)

            open_price = current_price
            high_price = current_price + high_offset
            low_price = current_price - low_offset
            close_price = current_price + close_offset

            prices.append({
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': np.random.randint(100, 1000)
            })

            current_price = close_price

        # Crear DataFrame
        df = pd.DataFrame(prices, index=dates)
        enviar_senal_log("INFO", f"✅ Generados {len(df, "test_ictdetector_sprint12", "migration")} velas sintéticas")
        enviar_senal_log("INFO", f"   - Rango de precios: {df['low'].min(, "test_ictdetector_sprint12", "migration"):.5f} - {df['high'].max():.5f}")
        enviar_senal_log("INFO", f"   - Precio actual: {df['close'].iloc[-1]:.5f}", "test_ictdetector_sprint12", "migration")

        # 4. TEST DETECT_PATTERNS
        enviar_senal_log("INFO", "\n🔍 4. Testeando detect_patterns(, "test_ictdetector_sprint12", "migration")...")
        test_data = {'candles': df}
        patterns = detector.detect_patterns(test_data)

        assert isinstance(patterns, list), "detect_patterns no retorna lista"
        enviar_senal_log("INFO", f"✅ detect_patterns ejecutado correctamente", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", f"   - Patrones detectados: {len(patterns, "test_ictdetector_sprint12", "migration")}")
        enviar_senal_log("INFO", f"   - Análisis #: {detector.analysis_count}", "test_ictdetector_sprint12", "migration")

        if patterns:
            pattern_types = [p['type'] for p in patterns]
            enviar_senal_log("INFO", f"   - Tipos encontrados: {set(pattern_types, "test_ictdetector_sprint12", "migration")}")

            # Verificar estructura de patrones
            sample_pattern = patterns[0]
            required_fields = ['type', 'confidence', 'analysis_id']
            for field in required_fields:
                assert field in sample_pattern, f"Campo requerido '{field}' faltante en patrón"
            enviar_senal_log("INFO", f"   - Estructura de patrones: ✅ Válida", "test_ictdetector_sprint12", "migration")

        # 5. TEST ANALYZE_STRUCTURE
        enviar_senal_log("INFO", "\n🏗️ 5. Testeando analyze_structure(, "test_ictdetector_sprint12", "migration")...")
        structure = detector.analyze_structure(df)

        assert isinstance(structure, dict), "analyze_structure no retorna dict"
        assert 'structure' in structure, "Campo 'structure' faltante"
        assert 'experimental' in structure, "Campo 'experimental' faltante"
        assert structure['experimental'] == False, "Debería ser implementación real, no experimental"

        enviar_senal_log("INFO", f"✅ analyze_structure ejecutado correctamente", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", f"   - Estructura detectada: {structure['structure']}", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", f"   - Experimental: {structure['experimental']}", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", f"   - Precio actual: {structure.get('current_price', 'N/A', "test_ictdetector_sprint12", "migration")}")
        enviar_senal_log("INFO", f"   - Zona P/D: {structure.get('premium_discount_zone', {}, "test_ictdetector_sprint12", "migration").get('zone', 'N/A')}")

        # 6. TEST DETECT_BIAS
        enviar_senal_log("INFO", "\n🎯 6. Testeando detect_bias(, "test_ictdetector_sprint12", "migration")...")
        bias = detector.detect_bias(df)

        assert isinstance(bias, dict), "detect_bias no retorna dict"
        assert 'bias' in bias, "Campo 'bias' faltante"
        assert 'experimental' in bias, "Campo 'experimental' faltante"
        assert bias['experimental'] == False, "Debería ser implementación real, no experimental"

        enviar_senal_log("INFO", f"✅ detect_bias ejecutado correctamente", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", f"   - Bias detectado: {bias['bias']}", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", f"   - Experimental: {bias['experimental']}", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", f"   - H4 Bias: {bias.get('h4_bias', {}, "test_ictdetector_sprint12", "migration").get('bias', 'N/A')}")
        enviar_senal_log("INFO", f"   - M15 Bias: {bias.get('m15_bias', {}, "test_ictdetector_sprint12", "migration").get('bias', 'N/A')}")
        enviar_senal_log("INFO", f"   - Confluencia: {bias.get('confluence_strength', 'N/A', "test_ictdetector_sprint12", "migration")}")

        # 7. TEST FIND_POIS
        enviar_senal_log("INFO", "\n📍 7. Testeando find_pois(, "test_ictdetector_sprint12", "migration")...")
        pois = detector.find_pois(df)

        assert isinstance(pois, list), "find_pois no retorna lista"
        enviar_senal_log("INFO", f"✅ find_pois ejecutado correctamente", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", f"   - POIs encontrados: {len(pois, "test_ictdetector_sprint12", "migration")}")

        if pois:
            # Verificar estructura básica de POIs
            sample_poi = pois[0]
            if 'analysis_id' in sample_poi:
                enviar_senal_log("INFO", f"   - Análisis ID: {sample_poi['analysis_id']}", "test_ictdetector_sprint12", "migration")

        # 8. TEST MÉTODOS DE UTILIDAD
        enviar_senal_log("INFO", "\n⚙️ 8. Testeando métodos de utilidad...", "test_ictdetector_sprint12", "migration")

        # Test get_analysis_summary
        summary = detector.get_analysis_summary()
        assert isinstance(summary, dict), "get_analysis_summary no retorna dict"
        assert 'status' in summary, "Campo 'status' faltante en summary"
        enviar_senal_log("INFO", f"✅ get_analysis_summary: {summary['status']}", "test_ictdetector_sprint12", "migration")

        # Test reset_cache
        detector.reset_cache()
        enviar_senal_log("INFO", "✅ reset_cache ejecutado", "test_ictdetector_sprint12", "migration")

        # Test get_detector_status
        status = detector.get_detector_status()
        assert isinstance(status, dict), "get_detector_status no retorna dict"
        assert status['initialized'] == True, "Status indica detector no inicializado"
        enviar_senal_log("INFO", f"✅ get_detector_status: detector inicializado = {status['initialized']}", "test_ictdetector_sprint12", "migration")

        # 9. TEST CON DATOS VACÍOS/ERRÓNEOS
        enviar_senal_log("ERROR", "\n⚠️ 9. Testeando manejo de errores...", "test_ictdetector_sprint12", "migration")

        # Test con datos vacíos
        empty_patterns = detector.detect_patterns({})
        assert empty_patterns == [], "Datos vacíos deberían retornar lista vacía"
        enviar_senal_log("INFO", "✅ Manejo de datos vacíos correcto", "test_ictdetector_sprint12", "migration")

        # Test con DataFrame vacío
        empty_df = pd.DataFrame()
        empty_structure = detector.analyze_structure(empty_df)
        assert 'error' in empty_structure, "DataFrame vacío debería generar error"
        enviar_senal_log("INFO", "✅ Manejo de DataFrame vacío correcto", "test_ictdetector_sprint12", "migration")

        # Test con None
        none_bias = detector.detect_bias(None)
        assert 'error' in none_bias, "None debería generar error"
        enviar_senal_log("INFO", "✅ Manejo de None correcto", "test_ictdetector_sprint12", "migration")

        # 10. RESUMEN FINAL
        enviar_senal_log("INFO", "\n" + "=" * 65, "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", "🎉 SPRINT 1.2 - DÍA 1 VALIDACIÓN COMPLETA", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", "=" * 65, "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", "🚀 ICTDetector: ✅ IMPLEMENTACIÓN REAL FUNCIONANDO", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", , "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", "📊 RESULTADOS DEL TEST:", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", f"   ✅ Imports: Correcto", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", f"   ✅ Inicialización: Correcto", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", f"   ✅ detect_patterns(, "test_ictdetector_sprint12", "migration"): {len(patterns)} patrones detectados")
        enviar_senal_log("INFO", f"   ✅ analyze_structure(, "test_ictdetector_sprint12", "migration"): {structure['structure']}")
        enviar_senal_log("INFO", f"   ✅ detect_bias(, "test_ictdetector_sprint12", "migration"): {bias['bias']}")
        enviar_senal_log("INFO", f"   ✅ find_pois(, "test_ictdetector_sprint12", "migration"): {len(pois)} POIs encontrados")
        enviar_senal_log("INFO", f"   ✅ Utilidades: Todas funcionando", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("ERROR", f"   ✅ Manejo de errores: Robusto", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", , "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", "🎯 CARACTERÍSTICAS CONFIRMADAS:", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", "   🔥 Implementación real (no placeholder, "test_ictdetector_sprint12", "migration")")
        enviar_senal_log("INFO", "   🔥 Sistema de logging SLUC v2.0 integrado", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", "   🔥 Configuración y gestión de estado", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("ERROR", "   🔥 Manejo robusto de errores", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", "   🔥 Integración completa con el ecosistema", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", , "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", "🚀 PRÓXIMOS PASOS SPRINT 1.2:", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", "   📅 Día 2: TCT Pipeline Completo", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", "   📅 Día 3: POI System v3.1 Integration", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", "   📅 Día 4: Confidence Engine Avanzado", "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", , "test_ictdetector_sprint12", "migration")
        enviar_senal_log("INFO", "🏆 SPRINT 1.2 DÍA 1: ¡COMPLETADO EXITOSAMENTE!", "test_ictdetector_sprint12", "migration")

        return True

    except Exception as e:
        enviar_senal_log("ERROR", f"\n❌ ERROR en el test: {e}", "test_ictdetector_sprint12", "migration")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ictdetector_integration()
    exit(0 if success else 1)
