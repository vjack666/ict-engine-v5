"""
Configuration Management
=======================

Gestión centralizada de configuraciones del sistema Sentinel Grid.
"""

import json
from json import JSONDecodeError
# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log

from pathlib import Path
from typing import Dict, Any

# Rutas de configuración
CONFIG_DIR = Path(__file__).parent
TEMP_CONFIG_PATH = CONFIG_DIR / "config_temp.json"
MAIN_CONFIG_PATH = CONFIG_DIR / "config_main.json"
USER_CONFIG_PATH = CONFIG_DIR / "config_user.json"

class ConfigManager:
    """Gestor centralizado de configuraciones."""

    def __init__(self):
        self.configs = {}
        self.load_all_configs()

    def load_all_configs(self):
        """Carga todas las configuraciones disponibles."""
        # Configuración temporal (para testing)
        if TEMP_CONFIG_PATH.exists():
            self.configs['temp'] = self.load_config(TEMP_CONFIG_PATH)

        # Configuración principal
        if MAIN_CONFIG_PATH.exists():
            self.configs['main'] = self.load_config(MAIN_CONFIG_PATH)

        # Configuración de usuario
        if USER_CONFIG_PATH.exists():
            self.configs['user'] = self.load_config(USER_CONFIG_PATH)

    def load_config(self, path: Path) -> Dict[str, Any]:
        """Carga un archivo de configuración específico."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (JSONDecodeError, ValueError) as e:
            enviar_senal_log("ERROR", f"Error cargando configuración {path}: {e}", __name__, "sistema")
            return {}

    def get_config(self, config_type: str = 'temp') -> Dict[str, Any]:
        """Obtiene una configuración específica."""
        return self.configs.get(config_type, {})

    def save_config(self, config_data: Dict[str, Any], config_type: str = 'user'):
        """Guarda una configuración."""
        path_map = {
            'temp': TEMP_CONFIG_PATH,
            'main': MAIN_CONFIG_PATH,
            'user': USER_CONFIG_PATH
        }

        if config_type not in path_map:
            raise ValueError(f"Tipo de configuración no válido: {config_type}")

        path = path_map[config_type]

        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)

            # Actualizar cache
            self.configs[config_type] = config_data
            return True

        except (JSONDecodeError, ValueError) as e:
            enviar_senal_log("ERROR", f"Error guardando configuración {path}: {e}", __name__, "sistema")
            return False

# Instancia global del gestor de configuración
config_manager = ConfigManager()

def get_trading_config() -> Dict[str, Any]:
    """Obtiene la configuración de trading activa."""
    # Prioridad: user > main > temp
    for config_type in ['user', 'main', 'temp']:
        config = config_manager.get_config(config_type)
        if config:
            return config

    # Configuración por defecto si no hay ninguna
    return {
        "sesiones_operacion": ["24_HORAS"],
        "modalidad_operacion": "NORMAL",
        "riesgo_maximo_porcentaje": 2.0,
        "ganancia_maxima_usd": 60.0,
        "lotaje_inicial": 0.1
    }
