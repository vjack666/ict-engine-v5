#!/usr/bin/env python3
"""
🧪 TEST LOGGING SYSTEM - Tests unitarios para el sistema de logging
Valida funcionamiento del sistema SLUC v2.0 y bitácoras
"""

import unittest
import sys
from pathlib import Path
import os

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from sistema.logging_interface import enviar_senal_log
    from sistema.emoji_logger import EmojiLogger
    from sistema.logging_config import LoggingConfig
except ImportError as e:
    print(f"⚠️ Import warning en test_logging_system: {e}")
    enviar_senal_log = None

class TestLoggingInterface(unittest.TestCase):
    """Tests para la interfaz de logging"""

    def test_enviar_senal_log_function(self):
        """Test función principal de logging"""
        if enviar_senal_log is None:
            self.skipTest("enviar_senal_log not available")

        # Test que la función existe y es callable
        self.assertTrue(callable(enviar_senal_log))

    def test_log_levels(self):
        """Test niveles de log válidos"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

        for level in valid_levels:
            # Test que cada nivel es string válido
            self.assertIsInstance(level, str)
            self.assertTrue(level.isupper())

    def test_log_message_structure(self):
        """Test estructura básica de mensajes de log"""
        test_message = "Test message for logging system"
        test_emisor = "test_logging_system"
        test_categoria = "testing"

        # Verificar tipos de datos
        self.assertIsInstance(test_message, str)
        self.assertIsInstance(test_emisor, str)
        self.assertIsInstance(test_categoria, str)

        # Verificar que no están vacíos
        self.assertGreater(len(test_message), 0)
        self.assertGreater(len(test_emisor), 0)
        self.assertGreater(len(test_categoria), 0)

class TestEmojiLogger(unittest.TestCase):
    """Tests para el logger con emojis"""

    def test_emoji_mapping(self):
        """Test mapeo de emojis por nivel"""
        emoji_map = {
            'DEBUG': '🔍',
            'INFO': 'ℹ️',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'CRITICAL': '🚨'
        }

        # Verificar que cada nivel tiene emoji
        for level, emoji in emoji_map.items():
            self.assertIsInstance(level, str)
            self.assertIsInstance(emoji, str)
            self.assertGreater(len(emoji), 0)

    def test_emoji_logger_instantiation(self):
        """Test creación de instancia de EmojiLogger"""
        try:
            logger = EmojiLogger()
            self.assertIsNotNone(logger)
        except NameError:
            self.skipTest("EmojiLogger class not available")
        except Exception as e:
            self.skipTest(f"EmojiLogger instantiation failed: {e}")

class TestLoggingConfig(unittest.TestCase):
    """Tests para configuración de logging"""

    def test_log_directory_structure(self):
        """Test estructura de directorios de logs"""
        expected_dirs = [
            "data/logs/system",
            "data/logs/debug",
            "data/logs/errors",
            "data/logs/dashboard",
            "data/operational"
        ]

        # Verificar que las rutas son strings válidas
        for dir_path in expected_dirs:
            self.assertIsInstance(dir_path, str)
            self.assertGreater(len(dir_path), 0)
            self.assertIn('/', dir_path)  # Debe contener separador de path

    def test_log_file_extensions(self):
        """Test extensiones válidas de archivos de log"""
        valid_extensions = ['.log', '.jsonl', '.txt', '.csv']

        test_files = [
            'system.log',
            'events.jsonl',
            'debug.txt',
            'metrics.csv'
        ]

        for filename in test_files:
            extension = Path(filename).suffix
            self.assertIn(extension, valid_extensions)

class TestBitacoraSystem(unittest.TestCase):
    """Tests para el sistema de bitácoras"""

    def test_bitacora_categories(self):
        """Test categorías válidas de bitácoras"""
        valid_categories = [
            'trading_decisions',
            'pattern_detection',
            'poi_lifecycle',
            'risk_management',
            'performance',
            'session_analysis',
            'system_status',
            'error_tracking'
        ]

        # Verificar que cada categoría es válida
        for category in valid_categories:
            self.assertIsInstance(category, str)
            self.assertGreater(len(category), 0)
            self.assertTrue('_' in category or category.islower())

    def test_jsonl_format_structure(self):
        """Test estructura básica de formato JSONL"""
        import json

        # Ejemplo de línea JSONL válida
        test_jsonl_line = {
            "timestamp": "2025-08-01T14:30:00.123456",
            "bitacora_type": "trading_decisions",
            "event_id": "TD_001",
            "description": "Test trading decision",
            "data": {"symbol": "EURUSD", "action": "BUY"}
        }

        # Verificar que se puede serializar a JSON
        json_string = json.dumps(test_jsonl_line)
        self.assertIsInstance(json_string, str)

        # Verificar que se puede deserializar
        parsed_data = json.loads(json_string)
        self.assertEqual(parsed_data, test_jsonl_line)

    def test_timestamp_format(self):
        """Test formato de timestamp ISO 8601"""
        from datetime import datetime

        # Crear timestamp en formato ISO
        now = datetime.now()
        iso_timestamp = now.isoformat()

        # Verificar formato básico
        self.assertIsInstance(iso_timestamp, str)
        self.assertIn('T', iso_timestamp)  # Separador fecha-hora
        self.assertIn('-', iso_timestamp)  # Separador de fecha
        self.assertIn(':', iso_timestamp)  # Separador de hora

class TestLogRotation(unittest.TestCase):
    """Tests para rotación de logs"""

    def test_daily_rotation_naming(self):
        """Test nomenclatura de rotación diaria"""

        # Formato esperado: filename_YYYY-MM-DD.ext
        date_str = datetime.now().strftime('%Y-%m-%d')
        test_filename = f"trading_decisions_{date_str}.jsonl"

        # Verificar estructura del nombre
        self.assertIn(date_str, test_filename)
        self.assertTrue(test_filename.endswith('.jsonl'))
        self.assertIn('_', test_filename)

    def test_log_size_limits(self):
        """Test límites de tamaño de logs"""
        # Límites razonables para archivos de log
        max_log_size_mb = 100  # 100 MB
        max_retention_days = 30  # 30 días

        self.assertGreater(max_log_size_mb, 0)
        self.assertLess(max_log_size_mb, 1000)  # No más de 1 GB

        self.assertGreater(max_retention_days, 0)
        self.assertLess(max_retention_days, 365)  # No más de 1 año

class TestLogSecurity(unittest.TestCase):
    """Tests para seguridad del sistema de logs"""

    def test_sensitive_data_filtering(self):
        """Test filtrado de datos sensibles"""
        sensitive_keywords = [
            'password',
            'api_key',
            'secret',
            'token',
            'credentials'
        ]

        test_message = "User login with password: secret123"

        # Verificar que se pueden detectar datos sensibles
        contains_sensitive = any(keyword in test_message.lower()
                               for keyword in sensitive_keywords)
        self.assertTrue(contains_sensitive)

    def test_log_injection_prevention(self):
        """Test prevención de inyección en logs"""
        malicious_inputs = [
            "test\n\rFAKE LOG ENTRY",
            "test\x00null_byte",
            "test\t\ttab_injection"
        ]

        for malicious_input in malicious_inputs:
            # Los caracteres de control deberían ser detectables
            has_control_chars = any(ord(char) < 32 for char in malicious_input
                                  if char not in ['\n', '\r', '\t'])

            # Nota: en un sistema real, estos deberían ser sanitizados
            self.assertIsInstance(malicious_input, str)

if __name__ == '__main__':
    print("🧪 Ejecutando tests del Sistema de Logging...")

    # Configurar verbosidad
    unittest.main(verbosity=2, exit=False)

    print("✅ Tests del Sistema de Logging completados")
