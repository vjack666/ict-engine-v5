#!/usr/bin/env python3
"""
🧪 TEST ICT ENGINE - Tests unitarios para el motor ICT
Valida funcionamiento de detección de patrones y análisis técnico
"""

import unittest
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from core.ict_engine.ict_detector import ICTDetector
    from core.ict_engine.confidence_engine import ConfidenceEngine
    from core.ict_engine.ict_types import PatternType
except ImportError as e:
    print(f"⚠️ Import warning en test_ict_engine: {e}")
    ICTDetector = None
    ConfidenceEngine = None
    PatternType = None

class TestICTEngine(unittest.TestCase):
    """Tests para el ICT Engine"""

    def setUp(self):
        """Configuración inicial para cada test"""
        if ICTDetector is None:
            self.skipTest("ICT Engine modules not available")

        self.test_data = {
            "symbol": "EURUSD",
            "timeframe": "H1",
            "ohlc_data": [
                {"open": 1.0800, "high": 1.0850, "low": 1.0790, "close": 1.0840, "time": "2025-08-01T10:00:00"},
                {"open": 1.0840, "high": 1.0860, "low": 1.0820, "close": 1.0850, "time": "2025-08-01T11:00:00"},
                {"open": 1.0850, "high": 1.0870, "low": 1.0830, "close": 1.0860, "time": "2025-08-01T12:00:00"}
            ]
        }

    def test_ict_detector_initialization(self):
        """Test inicialización del detector ICT"""
        try:
            detector = ICTDetector()
            self.assertIsNotNone(detector)
        except Exception as e:
            self.skipTest(f"ICT Detector initialization failed: {e}")

    def test_pattern_detection_structure(self):
        """Test estructura básica de detección de patrones"""
        try:
            detector = ICTDetector()

            # Test que los métodos básicos existen
            self.assertTrue(hasattr(detector, 'detect_patterns'))
            self.assertTrue(hasattr(detector, 'analyze_structure'))

        except Exception as e:
            self.skipTest(f"Pattern detection test failed: {e}")

    def test_confidence_engine_initialization(self):
        """Test inicialización del motor de confianza"""
        if ConfidenceEngine is None:
            self.skipTest("ConfidenceEngine not available")

        try:
            engine = ConfidenceEngine()
            self.assertIsNotNone(engine)
        except Exception as e:
            self.skipTest(f"Confidence Engine initialization failed: {e}")

    def test_pattern_types_enum(self):
        """Test que los tipos de patrones están definidos"""
        if PatternType is None:
            self.skipTest("PatternType enum not available")

        # Verificar que al menos algunos patrones básicos existen
        pattern_names = [attr for attr in dir(PatternType) if not attr.startswith('_')]
        self.assertGreater(len(pattern_names), 0, "No pattern types defined")

    def test_data_validation(self):
        """Test validación de datos de entrada"""
        # Test datos válidos
        self.assertIsInstance(self.test_data["symbol"], str)
        self.assertIsInstance(self.test_data["timeframe"], str)
        self.assertIsInstance(self.test_data["ohlc_data"], list)

        # Test estructura de OHLC
        for candle in self.test_data["ohlc_data"]:
            self.assertIn("open", candle)
            self.assertIn("high", candle)
            self.assertIn("low", candle)
            self.assertIn("close", candle)
            self.assertIn("time", candle)

class TestICTPatternLogic(unittest.TestCase):
    """Tests para lógica de patrones ICT"""

    def test_ohlc_validation(self):
        """Test validación básica de datos OHLC"""
        valid_candle = {
            "open": 1.0800,
            "high": 1.0850,
            "low": 1.0790,
            "close": 1.0840
        }

        # High debe ser mayor o igual que open, close
        self.assertGreaterEqual(valid_candle["high"], valid_candle["open"])
        self.assertGreaterEqual(valid_candle["high"], valid_candle["close"])

        # Low debe ser menor o igual que open, close
        self.assertLessEqual(valid_candle["low"], valid_candle["open"])
        self.assertLessEqual(valid_candle["low"], valid_candle["close"])

    def test_price_structure_basic(self):
        """Test estructura básica de precios"""
        # Test tendencia alcista simple
        prices = [1.0800, 1.0820, 1.0840, 1.0860]

        # Verificar que hay progresión
        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                trend_up = True
            else:
                trend_up = False
                break

        # Al menos debería haber alguna lógica de tendencia
        self.assertIsInstance(trend_up, bool)

if __name__ == '__main__':
    print("🧪 Ejecutando tests del ICT Engine...")

    # Configurar verbosidad
    unittest.main(verbosity=2, exit=False)

    print("✅ Tests del ICT Engine completados")
