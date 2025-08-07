"""
Configuration Package
====================

Módulo de configuración del sistema Sentinel Grid.
"""

from .config_manager import config_manager, get_trading_config

__all__ = [
    'config_manager',
    'get_trading_config'
]
