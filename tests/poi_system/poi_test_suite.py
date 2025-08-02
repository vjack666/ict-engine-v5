#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST SUITE COMPLETO - SISTEMA POI VERIFICATION
Validación exhaustiva del sistema de detección POI basado en especificaciones
"""

import unittest
import pandas as pd
import numpy as np
import time
import json
from datetime import datetime, timedelta
import tracemalloc
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configurar path del proyecto
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# === IMPORTS DEL SISTEMA POI ===
try:
    from core.poi_system.poi_detector import (
        detectar_order_blocks,
        detectar_fair_value_gaps,
        detectar_breaker_blocks,
        detectar_imbalances,
        detectar_todos_los_pois,
        encontrar_pois_multiples_para_dashboard,
        POIDetector,
        POI_TYPES,
        POI_SCORING_CONFIG
    )
    from core.poi_system.poi_utils import crear_poi_estructura
    from sistema.logging_interface import enviar_senal_log
except ImportError as e:
    print(f"⚠️ Error importando módulos POI: {e}")
    print("📁 Verificar estructura del proyecto y paths")
    sys.exit(1)

class TestDataGenerator:
    """
    🏭 GENERADOR DE DATOS DE PRUEBA
    Crea datasets sintéticos para testing de POI
    """

    @staticmethod
    def create_basic_ohlc(num_candles: int = 100, base_price: float = 1.1800) -> pd.DataFrame:
        """Genera OHLC básico para testing"""
        np.random.seed(42)  # Reproducible

        data = []
        current_price = base_price

        for i in range(num_candles):
            # Simulación de movimiento aleatorio con bias
            change = np.random.normal(0, 0.0005)
            current_price += change

            # OHLC con spread realista
            open_price = current_price
            high_price = open_price + abs(np.random.normal(0, 0.0003))
            low_price = open_price - abs(np.random.normal(0, 0.0003))
            close_price = low_price + (high_price - low_price) * np.random.random()

            data.append({
                'open': round(open_price, 5),
                'high': round(high_price, 5),
                'low': round(low_price, 5),
                'close': round(close_price, 5),
                'volume': np.random.randint(100, 1000),
                'time': datetime.now() - timedelta(hours=num_candles-i)
            })

            current_price = close_price

        return pd.DataFrame(data)

    @staticmethod
    def create_order_block_pattern() -> pd.DataFrame:
        """Crea patrón específico de Order Block"""
        # Patrón: acumulación → movimiento fuerte → retorno al OB
        base_price = 1.1800
        data = []

        # Fase 1: Acumulación (5 velas)
        for i in range(5):
            data.append({
                'open': base_price,
                'high': base_price + 0.0005,
                'low': base_price - 0.0005,
                'close': base_price + np.random.uniform(-0.0002, 0.0002),
                'volume': 500,
                'time': datetime.now() - timedelta(hours=25-i)
            })

        # Fase 2: Movimiento institucional fuerte (3 velas)
        for i in range(3):
            open_price = data[-1]['close']
            high_price = open_price + 0.0050  # Movimiento fuerte
            close_price = high_price - 0.0005
            data.append({
                'open': open_price,
                'high': high_price,
                'low': open_price - 0.0002,
                'close': close_price,
                'volume': 1500,  # Alto volumen
                'time': datetime.now() - timedelta(hours=20-i)
            })

        # Fase 3: Retorno y test del OB (12 velas)
        current_price = data[-1]['close']
        for i in range(12):
            # Gradual retorno hacia el Order Block
            target_price = base_price + 0.0010
            change = (target_price - current_price) * 0.1 + np.random.uniform(-0.0003, 0.0003)
            current_price += change

            data.append({
                'open': current_price,
                'high': current_price + abs(np.random.normal(0, 0.0002)),
                'low': current_price - abs(np.random.normal(0, 0.0002)),
                'close': current_price + np.random.uniform(-0.0001, 0.0001),
                'volume': np.random.randint(200, 800),
                'time': datetime.now() - timedelta(hours=15-i)
            })

        return pd.DataFrame(data)

    @staticmethod
    def create_fvg_pattern() -> pd.DataFrame:
        """Crea patrón específico de Fair Value Gap"""
        base_price = 1.1750
        data = []

        # Vela 1: Normal
        data.append({
            'open': base_price,
            'high': base_price + 0.0008,
            'low': base_price - 0.0003,
            'close': base_price + 0.0005,
            'volume': 400,
            'time': datetime.now() - timedelta(hours=3)
        })

        # Vela 2: Gap creation (movimiento fuerte)
        data.append({
            'open': base_price + 0.0005,
            'high': base_price + 0.0025,  # Movimiento fuerte
            'low': base_price + 0.0012,   # Low > previous high = GAP
            'close': base_price + 0.0020,
            'volume': 1200,
            'time': datetime.now() - timedelta(hours=2)
        })

        # Vela 3: Continuación
        data.append({
            'open': base_price + 0.0020,
            'high': base_price + 0.0030,
            'low': base_price + 0.0015,
            'close': base_price + 0.0025,
            'volume': 600,
            'time': datetime.now() - timedelta(hours=1)
        })

        return pd.DataFrame(data)

class POIDetectionTests(unittest.TestCase):
    """
    🎯 TESTS DE DETECCIÓN POI
    Validación de funciones individuales de detección
    """

    def setUp(self):
        """Setup para cada test"""
        self.generator = TestDataGenerator()
        self.basic_df = self.generator.create_basic_ohlc(100)
        self.ob_pattern_df = self.generator.create_order_block_pattern()
        self.fvg_pattern_df = self.generator.create_fvg_pattern()
        self.test_timeframes = ['M15', 'H1', 'H4', 'D1']
        self.current_price = 1.1800

    def test_poi_types_constants(self):
        """Test validar que todas las constantes POI_TYPES están definidas"""
        expected_types = [
            'BULLISH_OB', 'BEARISH_OB',
            'BULLISH_FVG', 'BEARISH_FVG',
            'BULLISH_BREAKER', 'BEARISH_BREAKER',
            'LIQUIDITY_VOID', 'PRICE_IMBALANCE'
        ]

        for poi_type in expected_types:
            self.assertIn(poi_type, POI_TYPES, f"POI_TYPE {poi_type} no está definido")

        print("POI_TYPES constants validation: PASSED")

    def test_order_blocks_detection(self):
        """Test detección de Order Blocks"""
        for timeframe in self.test_timeframes:
            with self.subTest(timeframe=timeframe):
                # Test con patrón específico de OB
                pois = detectar_order_blocks(self.ob_pattern_df, timeframe)

                # Validaciones
                self.assertIsInstance(pois, list, "Order Blocks debe retornar lista")

                if pois:  # Si se detectaron POIs
                    for poi in pois:
                        # Validar estructura
                        required_fields = ['id', 'type', 'price', 'score', 'timeframe']
                        for field in required_fields:
                            self.assertIn(field, poi, f"Campo {field} faltante en POI")

                        # Validar tipos
                        self.assertIn(poi['type'], ['BULLISH_OB', 'BEARISH_OB'])
                        self.assertIsInstance(poi['score'], (int, float))
                        self.assertGreaterEqual(poi['score'], 0)
                        self.assertLessEqual(poi['score'], 100)

                print(f"Order Blocks detection {timeframe}: PASSED ({len(pois)} POIs)")

    def test_fvg_detection(self):
        """✅ Test detección de Fair Value Gaps"""
        for timeframe in self.test_timeframes:
            with self.subTest(timeframe=timeframe):
                # Test con patrón específico de FVG
                pois = detectar_fair_value_gaps(self.fvg_pattern_df, timeframe)

                # Validaciones básicas
                self.assertIsInstance(pois, list)

                if pois:
                    for poi in pois:
                        # Validar tipos FVG
                        self.assertIn(poi['type'], ['BULLISH_FVG', 'BEARISH_FVG'])
                        self.assertIsInstance(poi['price'], (int, float))
                        self.assertEqual(poi['timeframe'], timeframe)

                print(f"✅ FVG detection {timeframe}: PASSED ({len(pois)} POIs)")

    def test_breaker_blocks_detection(self):
        """✅ Test detección de Breaker Blocks"""
        for timeframe in self.test_timeframes:
            with self.subTest(timeframe=timeframe):
                pois = detectar_breaker_blocks(self.basic_df, timeframe)

                self.assertIsInstance(pois, list)

                if pois:
                    for poi in pois:
                        self.assertIn(poi['type'], ['BULLISH_BREAKER', 'BEARISH_BREAKER'])
                        self.assertIsInstance(poi['score'], (int, float))

                print(f"✅ Breaker Blocks detection {timeframe}: PASSED ({len(pois)} POIs)")

    def test_imbalances_detection(self):
        """✅ Test detección de Imbalances"""
        for timeframe in self.test_timeframes:
            with self.subTest(timeframe=timeframe):
                pois = detectar_imbalances(self.basic_df, timeframe)

                self.assertIsInstance(pois, list)

                if pois:
                    for poi in pois:
                        self.assertIn(poi['type'], ['LIQUIDITY_VOID', 'PRICE_IMBALANCE'])

                print(f"✅ Imbalances detection {timeframe}: PASSED ({len(pois)} POIs)")

class POIIntegrationTests(unittest.TestCase):
    """
    🔗 TESTS DE INTEGRACIÓN
    Validación del sistema completo POI
    """

    def setUp(self):
        """Setup para tests de integración"""
        self.generator = TestDataGenerator()
        self.comprehensive_df = self.generator.create_basic_ohlc(500)  # Dataset grande
        self.current_price = 1.1800
        self.test_timeframes = ['M15', 'H1', 'H4']

    def test_detectar_todos_los_pois(self):
        """✅ Test función principal de detección completa"""
        for timeframe in self.test_timeframes:
            with self.subTest(timeframe=timeframe):
                result = detectar_todos_los_pois(
                    self.comprehensive_df,
                    timeframe,
                    self.current_price
                )

                # Validar estructura de respuesta
                self.assertIsInstance(result, dict, "Debe retornar diccionario")

                expected_keys = ['order_blocks', 'fair_value_gaps', 'breaker_blocks', 'imbalances', 'resumen']
                for key in expected_keys:
                    self.assertIn(key, result, f"Clave {key} faltante en resultado")

                # Validar resumen
                resumen = result['resumen']
                self.assertIn('total_pois', resumen)
                self.assertIsInstance(resumen['total_pois'], int)

                print(f"✅ detectar_todos_los_pois {timeframe}: PASSED ({resumen['total_pois']} total POIs)")

    def test_poi_detector_class(self):
        """✅ Test clase unificada POIDetector"""
        detector = POIDetector()

        for timeframe in self.test_timeframes:
            with self.subTest(timeframe=timeframe):
                # Test find_all_pois
                all_pois = detector.find_all_pois(
                    self.comprehensive_df,
                    timeframe,
                    self.current_price
                )

                self.assertIsInstance(all_pois, list)

                # Test find_dashboard_pois
                dashboard_pois = detector.find_dashboard_pois(
                    self.comprehensive_df,
                    timeframe,
                    self.current_price,
                    max_pois=5
                )

                self.assertIsInstance(dashboard_pois, list)
                self.assertLessEqual(len(dashboard_pois), 5)

                print(f"✅ POIDetector class {timeframe}: PASSED")

class POIPerformanceTests(unittest.TestCase):
    """
    ⚡ TESTS DE RENDIMIENTO
    Validación de performance y escalabilidad
    """

    def setUp(self):
        """Setup para tests de performance"""
        self.generator = TestDataGenerator()
        self.current_price = 1.1800

        # Datasets de diferentes tamaños
        self.small_df = self.generator.create_basic_ohlc(50)
        self.medium_df = self.generator.create_basic_ohlc(200)
        self.large_df = self.generator.create_basic_ohlc(1000)

        # SLAs definidos (en segundos)
        self.sla_individual_detection = 0.5  # 500ms por tipo
        self.sla_complete_detection = 2.0    # 2s para detección completa
        self.sla_dashboard_pois = 1.0        # 1s para POIs de dashboard

    def test_individual_detection_performance(self):
        """⚡ Test performance de detectores individuales"""
        functions_to_test = [
            ('Order Blocks', detectar_order_blocks),
            ('FVGs', detectar_fair_value_gaps),
            ('Breakers', detectar_breaker_blocks),
            ('Imbalances', detectar_imbalances)
        ]

        for func_name, func in functions_to_test:
            with self.subTest(function=func_name):
                start_time = time.time()

                result = func(self.medium_df, 'H1')

                elapsed_time = time.time() - start_time

                # Validar SLA
                self.assertLess(
                    elapsed_time,
                    self.sla_individual_detection,
                    f"{func_name} excedió SLA: {elapsed_time:.3f}s > {self.sla_individual_detection}s"
                )

                print(f"⚡ {func_name} performance: {elapsed_time:.3f}s - PASSED")

    def test_complete_detection_performance(self):
        """⚡ Test performance de detección completa"""
        datasets = [
            ('Small (50 candles)', self.small_df),
            ('Medium (200 candles)', self.medium_df),
            ('Large (1000 candles)', self.large_df)
        ]

        for dataset_name, df in datasets:
            with self.subTest(dataset=dataset_name):
                start_time = time.time()

                result = detectar_todos_los_pois(df, 'H1', self.current_price)

                elapsed_time = time.time() - start_time

                # SLA ajustado por tamaño
                expected_sla = self.sla_complete_detection * (len(df) / 200)

                self.assertLess(
                    elapsed_time,
                    expected_sla,
                    f"Complete detection {dataset_name} excedió SLA: {elapsed_time:.3f}s > {expected_sla:.3f}s"
                )

                print(f"⚡ Complete detection {dataset_name}: {elapsed_time:.3f}s - PASSED")

    def test_memory_usage(self):
        """🧠 Test uso de memoria"""
        tracemalloc.start()

        # Operación que consume memoria
        large_df = self.generator.create_basic_ohlc(2000)
        result = detectar_todos_los_pois(large_df, 'D1', self.current_price)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Convertir a MB
        current_mb = current / 1024 / 1024
        peak_mb = peak / 1024 / 1024

        # Validar que no exceda límites razonables
        self.assertLess(peak_mb, 100, f"Uso de memoria excesivo: {peak_mb:.2f}MB")

        print(f"🧠 Memory usage: Current={current_mb:.2f}MB, Peak={peak_mb:.2f}MB - PASSED")

class POIDataValidationTests(unittest.TestCase):
    """
    📊 TESTS DE VALIDACIÓN DE DATOS
    Validación de edge cases y manejo de errores
    """

    def test_empty_dataframe(self):
        """📊 Test con DataFrame vacío"""
        empty_df = pd.DataFrame()

        result = detectar_todos_los_pois(empty_df, 'H1', 1.1800)

        # Debe manejar gracefully
        self.assertIsInstance(result, dict)
        self.assertEqual(result['resumen']['total_pois'], 0)

        print("📊 Empty DataFrame handling: PASSED")

    def test_insufficient_data(self):
        """📊 Test con datos insuficientes"""
        small_df = TestDataGenerator().create_basic_ohlc(2)  # Solo 2 velas

        result = detectar_todos_los_pois(small_df, 'H1', 1.1800)

        # Debe manejar sin errores
        self.assertIsInstance(result, dict)

        print("📊 Insufficient data handling: PASSED")

    def test_nan_values_in_data(self):
        """📊 Test con valores NaN en datos"""
        df = TestDataGenerator().create_basic_ohlc(50)

        # Introducir algunos NaN
        df.loc[10:15, 'high'] = np.nan
        df.loc[20:22, 'close'] = np.nan

        result = detectar_todos_los_pois(df, 'H1', 1.1800)

        # Debe manejar NaN gracefully
        self.assertIsInstance(result, dict)

        print("📊 NaN values handling: PASSED")

class POIScoringTests(unittest.TestCase):
    """
    🎯 TESTS DE SCORING
    Validación del sistema de puntuación POI
    """

    def test_score_ranges(self):
        """🎯 Test rangos de scores"""
        df = TestDataGenerator().create_basic_ohlc(200)

        result = detectar_todos_los_pois(df, 'H1', 1.1800)

        # Verificar todos los POIs detectados
        all_pois = []
        for poi_type in ['order_blocks', 'fair_value_gaps', 'breaker_blocks', 'imbalances']:
            all_pois.extend(result.get(poi_type, []))

        for poi in all_pois:
            score = poi['score']
            self.assertIsInstance(score, (int, float), "Score debe ser numérico")
            self.assertGreaterEqual(score, 0, "Score no puede ser negativo")
            self.assertLessEqual(score, 100, "Score no puede exceder 100")

        print(f"🎯 Score ranges validation: PASSED ({len(all_pois)} POIs checked)")

class POITestRunner:
    """
    🏃‍♂️ EJECUTOR DE TESTS
    Orquesta la ejecución de todos los tests
    """

    def __init__(self):
        self.test_suites = [
            ('🎯 POI Detection Tests', POIDetectionTests),
            ('🔗 Integration Tests', POIIntegrationTests),
            ('⚡ Performance Tests', POIPerformanceTests),
            ('📊 Data Validation Tests', POIDataValidationTests),
            ('🎯 Scoring Tests', POIScoringTests)
        ]
        self.report_data = {}

    def run_all_tests(self, verbose: bool = True):
        """🚀 Ejecuta todos los test suites"""
        print("🧪 INICIANDO TEST SUITE COMPLETO DEL SISTEMA POI")
        print("=" * 60)

        total_tests = 0
        total_failures = 0
        total_errors = 0
        suite_results = []

        start_time = time.time()

        for suite_name, suite_class in self.test_suites:
            print(f"\n{suite_name}")
            print("-" * len(suite_name))

            # Crear y ejecutar test suite
            suite = unittest.TestLoader().loadTestsFromTestCase(suite_class)
            runner = unittest.TextTestRunner(verbosity=2 if verbose else 1, stream=open(os.devnull, 'w'))
            result = runner.run(suite)

            # Acumular estadísticas
            total_tests += result.testsRun
            total_failures += len(result.failures)
            total_errors += len(result.errors)

            # Guardar resultado del suite
            suite_results.append({
                'name': suite_name,
                'tests': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'success_rate': ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
            })

        elapsed_time = time.time() - start_time

        # Generar datos del reporte
        self.report_data = {
            'timestamp': datetime.now().isoformat(),
            'execution_time': elapsed_time,
            'total_tests': total_tests,
            'total_failures': total_failures,
            'total_errors': total_errors,
            'success_rate': ((total_tests - total_failures - total_errors) / total_tests * 100) if total_tests > 0 else 0,
            'suite_results': suite_results
        }

        # Reporte final en consola
        print("\n" + "=" * 60)
        print("📊 REPORTE FINAL DEL TEST SUITE")
        print("=" * 60)
        print(f"⏱️  Tiempo total: {elapsed_time:.2f} segundos")
        print(f"🧪 Tests ejecutados: {total_tests}")
        print(f"✅ Tests exitosos: {total_tests - total_failures - total_errors}")
        print(f"❌ Fallos: {total_failures}")
        print(f"🚨 Errores: {total_errors}")

        success_rate = ((total_tests - total_failures - total_errors) / total_tests * 100) if total_tests > 0 else 0
        print(f"📈 Tasa de éxito: {success_rate:.1f}%")

        if total_failures == 0 and total_errors == 0:
            print("🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
        else:
            print("⚠️  Se encontraron issues que requieren atención")

        return self.report_data

    def generate_markdown_report(self, output_path: str):
        """📄 Genera reporte en Markdown"""
        if not self.report_data:
            print("❌ No hay datos de reporte para generar")
            return

        report_content = f"""# 🧪 REPORTE TEST SUITE - SISTEMA POI

**Fecha:** {datetime.now().strftime('%d %B %Y')}
**Sistema:** ICT Engine v5.0 - Sistema POI
**Ejecutor:** POI Test Suite Completo

---

## 📊 RESUMEN EJECUTIVO

```
======================== {self.report_data['total_tests']} tests, {self.report_data['total_failures']} failures, {self.report_data['total_errors']} errors in {self.report_data['execution_time']:.2f}s =========================
```

### 🎯 **ESTADÍSTICAS GENERALES**
- ✅ **Tests Pasados:** {self.report_data['total_tests'] - self.report_data['total_failures'] - self.report_data['total_errors']}/{self.report_data['total_tests']} ({self.report_data['success_rate']:.1f}%)
- ❌ **Tests Fallidos:** {self.report_data['total_failures']}/{self.report_data['total_tests']} ({self.report_data['total_failures']/self.report_data['total_tests']*100:.1f}%)
- 🚨 **Errores:** {self.report_data['total_errors']}/{self.report_data['total_tests']} ({self.report_data['total_errors']/self.report_data['total_tests']*100:.1f}%)
- ⏱️ **Tiempo Total:** {self.report_data['execution_time']:.2f}s

---

## 📋 DESGLOSE DETALLADO POR SUITE

"""

        for suite in self.report_data['suite_results']:
            status = "✅ COMPLETO" if suite['failures'] == 0 and suite['errors'] == 0 else "⚠️ CON ISSUES"
            report_content += f"""### {suite['name']}
**Status:** {status} ({suite['tests']} tests)
- ✅ Exitosos: {suite['tests'] - suite['failures'] - suite['errors']}
- ❌ Fallidos: {suite['failures']}
- 🚨 Errores: {suite['errors']}
- 📈 Tasa de éxito: {suite['success_rate']:.1f}%

"""

        report_content += f"""
---

## 🎯 ANÁLISIS DE CALIDAD

### 📊 **Score General de Salud del Sistema POI**
```
🎯 CALIDAD GENERAL: {self.report_data['success_rate']:.1f}% ({'EXCELENTE' if self.report_data['success_rate'] >= 95 else 'BUENA' if self.report_data['success_rate'] >= 80 else 'REGULAR' if self.report_data['success_rate'] >= 60 else 'CRÍTICA'})
🔧 ESTABILIDAD: {'ALTA' if self.report_data['total_errors'] == 0 else 'MEDIA' if self.report_data['total_errors'] <= 2 else 'BAJA'} ({self.report_data['total_errors']} errores)
⚡ VELOCIDAD: {'EXCELENTE' if self.report_data['execution_time'] < 30 else 'BUENA' if self.report_data['execution_time'] < 60 else 'REGULAR'} ({self.report_data['execution_time']:.2f}s)
```

### 🔄 **RECOMENDACIONES**

"""

        if self.report_data['success_rate'] >= 95:
            report_content += "✅ **Sistema en óptimas condiciones** - Mantener monitoreo regular\n"
        elif self.report_data['success_rate'] >= 80:
            report_content += "⚠️ **Sistema estable con mejoras menores** - Revisar fallos específicos\n"
        else:
            report_content += "🚨 **Sistema requiere atención inmediata** - Priorizar corrección de errores\n"

        if self.report_data['total_failures'] > 0:
            report_content += f"- Revisar y corregir {self.report_data['total_failures']} tests fallidos\n"

        if self.report_data['total_errors'] > 0:
            report_content += f"- Investigar y resolver {self.report_data['total_errors']} errores críticos\n"

        report_content += f"""
---

## 📈 MÉTRICAS DE PERFORMANCE

- **Throughput de testing:** {self.report_data['total_tests']/self.report_data['execution_time']:.1f} tests/segundo
- **Tiempo promedio por test:** {self.report_data['execution_time']/self.report_data['total_tests']:.3f}s
- **Eficiencia del sistema:** {self.report_data['success_rate']:.1f}% de tests exitosos

---

## 🔧 PRÓXIMOS PASOS

### **INMEDIATOS (24h):**
1. Revisar y corregir cualquier test fallido
2. Investigar errores reportados
3. Validar performance si excede SLAs

### **CORTO PLAZO (1 semana):**
1. Optimizar tests con performance subóptima
2. Expandir cobertura de edge cases
3. Implementar monitoreo automático

### **LARGO PLAZO (1 mes):**
1. Integrar tests en CI/CD pipeline
2. Establecer baseline de performance
3. Crear alertas automáticas para regresiones

---

**Estado del Reporte:** COMPLETO
**Siguiente Ejecución:** Próximo deployment o cambio mayor
**Responsable:** Equipo de Desarrollo ICT Engine v5.0

---
*Generado automáticamente por POI Test Suite v1.0*
"""

        # Escribir reporte
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"📄 Reporte generado: {output_path}")

# === EJECUCIÓN PRINCIPAL ===
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Test Suite Sistema POI')
    parser.add_argument('--quick', action='store_true', help='Ejecutar solo tests rápidos')
    parser.add_argument('--verbose', action='store_true', help='Output verbose')
    parser.add_argument('--report', action='store_true', help='Generar reporte en docs/')

    args = parser.parse_args()

    runner = POITestRunner()

    # Ejecutar tests
    if args.quick:
        print("⚡ Ejecutando Quick Test (tests críticos)")
        result_data = runner.run_all_tests(verbose=False)
    else:
        result_data = runner.run_all_tests(verbose=args.verbose)

    # Generar reporte si se solicita
    if args.report or not args.quick:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"REPORTE_POI_TEST_SUITE_{timestamp}.md"
        report_path = project_root / "docs" / "bitacoras" / report_filename

        # Asegurar que existe el directorio
        report_path.parent.mkdir(parents=True, exist_ok=True)

        runner.generate_markdown_report(str(report_path))
        print(f"📁 Reporte guardado en: {report_path}")
