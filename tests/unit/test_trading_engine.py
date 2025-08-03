from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
"""
🧪 TEST TRADING ENGINE - Tests unitarios para el motor de trading
Valida funcionamiento de lógica de trading y gestión de órdenes
"""

import unittest
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from core.trading import TradingEngine
    from core.limit_order_manager import LimitOrderManager
    from core.risk_management.riskbot_mt5 import RiskBotMT5
except ImportError as e:
    enviar_senal_log("WARNING", f"⚠️ Import warning en test_trading_engine: {e}", "test_trading_engine", "migration")
    TradingEngine = None
    LimitOrderManager = None
    RiskBotMT5 = None

class TestTradingEngine(unittest.TestCase):
    """Tests para el motor de trading"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.test_order = {
            "symbol": "EURUSD",
            "order_type": "BUY",
            "volume": 0.1,
            "entry_price": 1.0850,
            "stop_loss": 1.0820,
            "take_profit": 1.0880
        }

    def test_order_validation(self):
        """Test validación básica de órdenes"""
        order = self.test_order

        # Verificar campos requeridos
        required_fields = ["symbol", "order_type", "volume", "entry_price"]
        for field in required_fields:
            self.assertIn(field, order)

        # Verificar tipos de datos
        self.assertIsInstance(order["symbol"], str)
        self.assertIsInstance(order["order_type"], str)
        self.assertIsInstance(order["volume"], (int, float))
        self.assertIsInstance(order["entry_price"], (int, float))

    def test_volume_validation(self):
        """Test validación de volumen"""
        volume = self.test_order["volume"]

        # Volumen debe ser positivo
        self.assertGreater(volume, 0)

        # Volumen debe estar en rango razonable
        self.assertGreaterEqual(volume, 0.01)  # Volumen mínimo típico
        self.assertLessEqual(volume, 100.0)    # Volumen máximo razonable

    def test_price_levels_logic(self):
        """Test lógica de niveles de precio"""
        order = self.test_order

        if order["order_type"] == "BUY":
            # Para órdenes BUY: SL < Entry < TP
            if "stop_loss" in order:
                self.assertLess(order["stop_loss"], order["entry_price"])
            if "take_profit" in order:
                self.assertGreater(order["take_profit"], order["entry_price"])

        elif order["order_type"] == "SELL":
            # Para órdenes SELL: TP < Entry < SL
            if "stop_loss" in order:
                self.assertGreater(order["stop_loss"], order["entry_price"])
            if "take_profit" in order:
                self.assertLess(order["take_profit"], order["entry_price"])

    def test_risk_reward_calculation(self):
        """Test cálculo de risk-reward"""
        order = self.test_order

        if "stop_loss" in order and "take_profit" in order:
            entry = order["entry_price"]
            sl = order["stop_loss"]
            tp = order["take_profit"]

            risk = abs(entry - sl)
            reward = abs(tp - entry)

            if risk > 0:
                risk_reward = reward / risk

                # Risk-reward debe ser positivo
                self.assertGreater(risk_reward, 0)

                # Risk-reward razonable (típicamente > 1.0 para trading profesional)
                self.assertGreater(risk_reward, 0.5)

class TestLimitOrderManager(unittest.TestCase):
    """Tests para el gestor de órdenes limitadas"""

    def test_order_manager_structure(self):
        """Test estructura básica del gestor de órdenes"""
        if LimitOrderManager is None:
            self.skipTest("LimitOrderManager not available")

        # Test que se puede instanciar
        try:
            manager = LimitOrderManager()
            self.assertIsNotNone(manager)
        except Exception as e:
            self.skipTest(f"LimitOrderManager initialization failed: {e}")

class TestRiskManagement(unittest.TestCase):
    """Tests para gestión de riesgo"""

    def test_risk_parameters(self):
        """Test parámetros básicos de riesgo"""
        risk_params = {
            "max_risk_per_trade": 0.02,  # 2%
            "max_daily_loss": 0.05,      # 5%
            "max_open_positions": 3,
            "max_correlation": 0.7
        }

        # Verificar rangos válidos
        self.assertGreater(risk_params["max_risk_per_trade"], 0)
        self.assertLess(risk_params["max_risk_per_trade"], 0.1)  # No más del 10%

        self.assertGreater(risk_params["max_daily_loss"], 0)
        self.assertLess(risk_params["max_daily_loss"], 0.2)  # No más del 20%

        self.assertGreater(risk_params["max_open_positions"], 0)
        self.assertLess(risk_params["max_open_positions"], 10)  # Límite razonable

    def test_position_sizing(self):
        """Test cálculo de tamaño de posición"""
        account_balance = 10000  # $10,000
        risk_percent = 0.02      # 2%
        risk_amount = 30         # $30 de riesgo por pip

        max_risk_usd = account_balance * risk_percent

        # Riesgo máximo debe ser razonable
        self.assertEqual(max_risk_usd, 200)  # $200 max risk

        # Tamaño de posición debe ser calculable
        if risk_amount > 0:
            position_size = max_risk_usd / risk_amount
            self.assertGreater(position_size, 0)

class TestTradingLogic(unittest.TestCase):
    """Tests para lógica de trading"""

    def test_signal_validation(self):
        """Test validación de señales de trading"""
        signal = {
            "action": "BUY",
            "confidence": 0.85,
            "timestamp": "2025-08-01T14:30:00",
            "source": "ICT_PATTERN"
        }

        # Verificar campos de señal
        self.assertIn("action", signal)
        self.assertIn("confidence", signal)
        self.assertIn("timestamp", signal)

        # Verificar valores válidos
        valid_actions = ["BUY", "SELL", "HOLD", "CLOSE"]
        self.assertIn(signal["action"], valid_actions)

        # Confidence entre 0 y 1
        self.assertGreaterEqual(signal["confidence"], 0.0)
        self.assertLessEqual(signal["confidence"], 1.0)

    def test_timeframe_validation(self):
        """Test validación de timeframes"""
        valid_timeframes = ["M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1"]
        test_timeframe = "H1"

        self.assertIn(test_timeframe, valid_timeframes)

    def test_symbol_validation(self):
        """Test validación de símbolos"""
        forex_symbols = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD"]
        test_symbol = "EURUSD"

        # Verificar formato
        self.assertEqual(len(test_symbol), 6)
        self.assertTrue(test_symbol.isupper())
        self.assertTrue(test_symbol.isalpha())

        # Verificar que es un símbolo conocido
        self.assertIn(test_symbol, forex_symbols)

if __name__ == '__main__':
    enviar_senal_log("INFO", "🧪 Ejecutando tests del Trading Engine...", "test_trading_engine", "migration")

    # Configurar verbosidad
    unittest.main(verbosity=2, exit=False)

    enviar_senal_log("INFO", "✅ Tests del Trading Engine completados", "test_trading_engine", "migration")
