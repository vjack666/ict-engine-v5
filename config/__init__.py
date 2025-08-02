"""
Configuration Package
====================

Módulo de configuración del sistema Sentinel Grid.
"""

from .config_manager import config_manager, get_trading_config

# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log

__all__ = [
    'config_manager',
    'get_trading_config'
]
