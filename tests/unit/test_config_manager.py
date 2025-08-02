"""
🧪 Test básico del sistema de configuración
==========================================

Test unitario para verificar que el config manager funciona correctamente.
"""

import pytest
import sys
from pathlib import Path

# Añadir project root al path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_config_manager_import():
    """Test que el config manager se puede importar"""
    try:
        from config.config_manager import ConfigManager
        assert ConfigManager is not None
    except ImportError as e:
        pytest.fail(f"No se pudo importar ConfigManager: {e}")

def test_config_manager_initialization():
    """Test que el config manager se puede inicializar"""
    try:
        from config.config_manager import ConfigManager
        config_manager = ConfigManager()
        assert config_manager is not None
        assert hasattr(config_manager, 'configs')
    except Exception as e:
        pytest.fail(f"Error inicializando ConfigManager: {e}")

def test_get_trading_config():
    """Test que se puede obtener la configuración de trading"""
    try:
        from config.config_manager import get_trading_config
        config = get_trading_config()
        assert config is not None
        assert isinstance(config, dict)

        # Verificar keys esperados
        expected_keys = [
            'sesiones_operacion',
            'modalidad_operacion',
            'riesgo_maximo_porcentaje',
            'ganancia_maxima_usd',
            'lotaje_inicial'
        ]

        for key in expected_keys:
            assert key in config, f"Key '{key}' faltante en config"

    except Exception as e:
        pytest.fail(f"Error obteniendo trading config: {e}")

def test_project_structure():
    """Test que la estructura del proyecto está correcta"""
    required_dirs = [
        'config',
        'core',
        'dashboard',
        'sistema',
        'utilities',
        'tests',
        'scripts'
    ]

    for dir_name in required_dirs:
        dir_path = PROJECT_ROOT / dir_name
        assert dir_path.exists(), f"Directorio '{dir_name}' no existe"
        assert dir_path.is_dir(), f"'{dir_name}' no es un directorio"

def test_main_launcher_exists():
    """Test que el launcher principal existe"""
    main_py = PROJECT_ROOT / "main.py"
    assert main_py.exists(), "main.py no existe"
    assert main_py.is_file(), "main.py no es un archivo"

@pytest.mark.integration
def test_logging_system():
    """Test de integración del sistema de logging"""
    try:
        from sistema.logging_interface import enviar_senal_log

        # Test básico de envío de log
        result = enviar_senal_log(
            "INFO",
            "Test del sistema de logging",
            "test_config_manager",
            "test"
        )

        # El resultado puede ser None si no hay error
        # Solo verificamos que no lance excepción
        assert True  # Si llegamos aquí, el test pasó

    except Exception as e:
        pytest.fail(f"Error en sistema de logging: {e}")

if __name__ == "__main__":
    # Ejecutar tests directamente
    pytest.main([__file__, "-v"])
