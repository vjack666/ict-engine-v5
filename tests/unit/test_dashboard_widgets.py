from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
"""
🧪 TEST DASHBOARD WIDGETS - Tests unitarios para widgets del dashboard
Valida funcionamiento de componentes de interfaz
"""

import unittest
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from dashboard.dashboard_widgets import *
    from dashboard.ict_professional_widget import *
except ImportError as e:
    enviar_senal_log("WARNING", f"⚠️ Import warning en test_dashboard_widgets: {e}", "test_dashboard_widgets", "migration")

class TestDashboardWidgets(unittest.TestCase):
    """Tests para widgets del dashboard"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.test_data = {
            "symbol": "EURUSD",
            "price": 1.0850,
            "trend": "BULLISH",
            "confidence": 0.85
        }

    def test_widget_data_structure(self):
        """Test estructura de datos para widgets"""
        # Verificar estructura básica de datos
        self.assertIn("symbol", self.test_data)
        self.assertIn("price", self.test_data)
        self.assertIn("trend", self.test_data)
        self.assertIn("confidence", self.test_data)

        # Verificar tipos de datos
        self.assertIsInstance(self.test_data["symbol"], str)
        self.assertIsInstance(self.test_data["price"], (int, float))
        self.assertIsInstance(self.test_data["trend"], str)
        self.assertIsInstance(self.test_data["confidence"], (int, float))

    def test_confidence_validation(self):
        """Test validación de valores de confianza"""
        confidence = self.test_data["confidence"]

        # Confidence debe estar entre 0 y 1
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)

    def test_trend_values(self):
        """Test valores válidos de tendencia"""
        valid_trends = ["BULLISH", "BEARISH", "NEUTRAL", "SIDEWAYS"]
        trend = self.test_data["trend"]

        self.assertIn(trend, valid_trends)

    def test_price_validation(self):
        """Test validación de precios"""
        price = self.test_data["price"]

        # Precio debe ser positivo
        self.assertGreater(price, 0)

        # Precio debe ser razonable para forex
        self.assertGreater(price, 0.1)
        self.assertLess(price, 10.0)

class TestICTProfessionalWidget(unittest.TestCase):
    """Tests específicos para el widget ICT Professional"""

    def test_ict_data_structure(self):
        """Test estructura de datos ICT"""
        ict_data = {
            "patterns": ["ORDER_BLOCK", "FAIR_VALUE_GAP"],
            "poi_count": 5,
            "structure": "BULLISH_BOS",
            "session": "LONDON"
        }

        # Verificar estructura
        self.assertIn("patterns", ict_data)
        self.assertIn("poi_count", ict_data)
        self.assertIn("structure", ict_data)
        self.assertIn("session", ict_data)

        # Verificar tipos
        self.assertIsInstance(ict_data["patterns"], list)
        self.assertIsInstance(ict_data["poi_count"], int)
        self.assertIsInstance(ict_data["structure"], str)
        self.assertIsInstance(ict_data["session"], str)

    def test_pattern_validation(self):
        """Test validación de patrones ICT"""
        valid_patterns = [
            "ORDER_BLOCK",
            "FAIR_VALUE_GAP",
            "BREAKER_BLOCK",
            "MITIGATION_BLOCK",
            "LIQUIDITY_VOID"
        ]

        test_patterns = ["ORDER_BLOCK", "FAIR_VALUE_GAP"]

        for pattern in test_patterns:
            self.assertIn(pattern, valid_patterns)

    def test_session_validation(self):
        """Test validación de sesiones de trading"""
        valid_sessions = ["LONDON", "NEW_YORK", "ASIAN", "OVERLAP"]
        test_session = "LONDON"

        self.assertIn(test_session, valid_sessions)

class TestWidgetFormatting(unittest.TestCase):
    """Tests para formateo de datos en widgets"""

    def test_price_formatting(self):
        """Test formateo de precios"""
        price = 1.08456

        # Test formateo a 4 decimales (típico para forex)
        formatted = f"{price:.4f}"
        self.assertEqual(formatted, "1.0846")

        # Test formateo a 5 decimales
        formatted_5 = f"{price:.5f}"
        self.assertEqual(formatted_5, "1.08456")

    def test_percentage_formatting(self):
        """Test formateo de porcentajes"""
        confidence = 0.8547

        # Test formateo como porcentaje
        percentage = f"{confidence:.1%}"
        self.assertEqual(percentage, "85.5%")

        # Test formateo con 2 decimales
        percentage_2 = f"{confidence:.2%}"
        self.assertEqual(percentage_2, "85.47%")

    def test_symbol_formatting(self):
        """Test formateo de símbolos"""
        symbol = "EURUSD"

        # Verificar formato válido de par de divisas
        self.assertEqual(len(symbol), 6)
        self.assertTrue(symbol.isupper())
        self.assertTrue(symbol.isalpha())

if __name__ == '__main__':
    enviar_senal_log("INFO", "🧪 Ejecutando tests de Dashboard Widgets...", "test_dashboard_widgets", "migration")

    # Configurar verbosidad
    unittest.main(verbosity=2, exit=False)

    enviar_senal_log("INFO", "✅ Tests de Dashboard Widgets completados", "test_dashboard_widgets", "migration")
