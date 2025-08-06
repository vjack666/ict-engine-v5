"""
🎯 SISTEMA DE IMPORTS CENTRALIZADOS (SIC) v3.0 - LIMPIO
======================================================
Sistema centralizado y sin errores para imports del ITC Engine

Características:
- Sin referencias circulares
- Imports validados únicamente
- Logging centralizado funcional
- Fallbacks robustos

Autor: Sistema ITC Engine v5.0
Fecha: 2025-08-06
Versión: v3.0 - Estabilizado
"""

# =============================================================================
# IMPORTS STANDARD LIBRARY - SEGUROS
# =============================================================================

# Standard Library básicos
import os
import sys
import json
import time as time_module
import re
from pathlib import Path

# Typing - sin redefinir constantes
try:
    from typing import Dict, List, Optional, Any, Tuple, Union, TYPE_CHECKING, Callable, Set
    typing_available = True
except ImportError:
    Dict = dict
    List = list
    Optional = type(None)
    Any = object
    Tuple = tuple
    Union = type
    TYPE_CHECKING = False
    Callable = type
    Set = set
    typing_available = False

# Datetime
try:
    from datetime import datetime, timedelta, timezone, time
    datetime_available = True
except ImportError:
    import datetime as dt
    datetime = dt.datetime
    timedelta = dt.timedelta
    timezone = dt.timezone
    time = dt.time
    datetime_available = False

# Dataclasses
try:
    from dataclasses import dataclass, field, asdict
    dataclasses_available = True
except ImportError:
    def dataclass(cls):
        return cls
    def field(**kwargs):
        return None
    def asdict(obj):
        return obj.__dict__ if hasattr(obj, '__dict__') else {}
    dataclasses_available = False

# Collections
try:
    from collections import Counter as StdCounter, defaultdict as StdDefaultdict, deque as StdDeque
    Counter = StdCounter
    defaultdict = StdDefaultdict
    deque = StdDeque
    collections_available = True
except ImportError:
    class Counter(dict):
        def most_common(self, n=None):
            return sorted(self.items(), key=lambda x: x[1], reverse=True)[:n]

    class defaultdict(dict):
        def __init__(self, default_factory=None):
            super().__init__()
            self.default_factory = default_factory

        def __getitem__(self, key):
            if key not in self and self.default_factory:
                self[key] = self.default_factory()
            return super().__getitem__(key)

    deque = list
    collections_available = False

# =============================================================================
# SISTEMA DE LOGGING CENTRALIZADO - SIN CICLOS
# =============================================================================

logging_available = False
enviar_senal_log = None
log_info = None
log_error = None
logger = None

# Importar logging estándar para fallback
import logging as std_logging

try:
    # Importar dinámicamente para evitar ciclos
    import importlib.util

    # Cargar logging_interface dinámicamente
    logging_path = os.path.join(os.path.dirname(__file__), "logging_interface.py")
    if os.path.exists(logging_path):
        spec = importlib.util.spec_from_file_location("logging_interface", logging_path)
        if spec and spec.loader:
            logging_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(logging_module)

            # Extraer funciones principales
            if hasattr(logging_module, 'enviar_senal_log'):
                enviar_senal_log = logging_module.enviar_senal_log
                logging_available = True

            # Crear funciones de conveniencia
            def log_info(mensaje, fuente="sic", metadata=None):
                enviar_senal_log("INFO", mensaje, fuente, "general", metadata)

            def log_error(mensaje, fuente="sic", metadata=None):
                enviar_senal_log("ERROR", mensaje, fuente, "general", metadata)

            def log_warning(mensaje, fuente="sic", metadata=None):
                enviar_senal_log("WARNING", mensaje, fuente, "general", metadata)

except Exception as e:
    # Fallback completo si falla la carga dinámica
    pass

# Si no se pudo cargar, usar fallback básico
if not logging_available:
    logger = std_logging.getLogger(__name__)

    def enviar_senal_log(nivel, mensaje, fuente="sic", categoria="general", metadata=None):
        """Fallback: enviar señal de log"""
        level = getattr(std_logging, nivel.upper(), std_logging.INFO)
        logger.log(level, f"[{fuente}:{categoria}] {mensaje}")

    def log_info(mensaje, fuente="sic", metadata=None):
        """Fallback: log info"""
        logger.info(f"[{fuente}] {mensaje}")

    def log_error(mensaje, fuente="sic", metadata=None):
        """Fallback: log error"""
        logger.error(f"[{fuente}] {mensaje}")

    def log_warning(mensaje, fuente="sic", metadata=None):
        """Fallback: log warning"""
        logger.warning(f"[{fuente}] {mensaje}")

# =============================================================================
# IMPORTS DE PROYECTO - DINÁMICOS Y SEGUROS
# =============================================================================

# Variables para disponibilidad
ict_engine_available = False
poi_system_available = False
dashboard_available = False
utils_available = False

# ICT Engine - Solo componentes que existen
ICTDetector = None
MarketContext = None

try:
    # Importar ICTDetector si existe
    ict_detector_path = os.path.join(os.path.dirname(__file__), "..", "core", "ict_engine", "ict_detector.py")
    if os.path.exists(ict_detector_path):
        spec = importlib.util.spec_from_file_location("ict_detector", ict_detector_path)
        if spec and spec.loader:
            ict_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(ict_module)

            if hasattr(ict_module, 'ICTDetector'):
                ICTDetector = ict_module.ICTDetector
                ict_engine_available = True
                if enviar_senal_log:
                    enviar_senal_log("INFO", "ICTDetector cargado exitosamente", "sic", "ict")

except Exception as e:
    if enviar_senal_log:
        enviar_senal_log("WARNING", f"ICT Engine no disponible: {e}", "sic", "init")

# POI System
POIDetector = None

try:
    poi_detector_path = os.path.join(os.path.dirname(__file__), "..", "core", "poi_system", "poi_detector.py")
    if os.path.exists(poi_detector_path):
        spec = importlib.util.spec_from_file_location("poi_detector", poi_detector_path)
        if spec and spec.loader:
            poi_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(poi_module)

            if hasattr(poi_module, 'POIDetector'):
                POIDetector = poi_module.POIDetector
                poi_system_available = True
                if enviar_senal_log:
                    enviar_senal_log("INFO", "POIDetector cargado exitosamente", "sic", "poi")

except Exception as e:
    if enviar_senal_log:
        enviar_senal_log("WARNING", f"POI System no disponible: {e}", "sic", "init")

# Dashboard
DashboardController = None

try:
    dashboard_path = os.path.join(os.path.dirname(__file__), "..", "dashboard", "dashboard_controller.py")
    if os.path.exists(dashboard_path):
        spec = importlib.util.spec_from_file_location("dashboard_controller", dashboard_path)
        if spec and spec.loader:
            dashboard_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(dashboard_module)

            if hasattr(dashboard_module, 'DashboardController'):
                DashboardController = dashboard_module.DashboardController
                dashboard_available = True
                if enviar_senal_log:
                    enviar_senal_log("INFO", "DashboardController cargado exitosamente", "sic", "dashboard")

except Exception as e:
    if enviar_senal_log:
        enviar_senal_log("WARNING", f"Dashboard no disponible: {e}", "sic", "init")

# Utils
MT5DataManager = None

try:
    mt5_path = os.path.join(os.path.dirname(__file__), "..", "utils", "mt5_data_manager.py")
    if os.path.exists(mt5_path):
        spec = importlib.util.spec_from_file_location("mt5_data_manager", mt5_path)
        if spec and spec.loader:
            mt5_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mt5_module)

            if hasattr(mt5_module, 'MT5DataManager'):
                MT5DataManager = mt5_module.MT5DataManager
                utils_available = True
                if enviar_senal_log:
                    enviar_senal_log("INFO", "MT5DataManager cargado exitosamente", "sic", "utils")

except Exception as e:
    if enviar_senal_log:
        enviar_senal_log("WARNING", f"Utils no disponibles: {e}", "sic", "init")

# =============================================================================
# FUNCIONES FALLBACK PARA ICT
# =============================================================================

def update_market_context(*args, **kwargs):
    """Fallback: actualizar contexto de mercado"""
    return {}

def detectar_fair_value_gaps(*args, **kwargs):
    """Fallback: detectar fair value gaps"""
    return []

def detectar_swing_points(*args, **kwargs):
    """Fallback: detectar swing points"""
    return []

# =============================================================================
# CONFIG BÁSICA
# =============================================================================

def get_trading_config():
    """Configuración básica de trading"""
    return {
        'SIMBOLO': 'XAUUSD',
        'TIMEFRAME': 'H1',
        'LEVERAGE': 100,
        'RISK_PERCENT': 2.0
    }

# =============================================================================
# API PÚBLICA
# =============================================================================

__all__ = [
    # Standard Library
    'Dict', 'List', 'Optional', 'Any', 'Tuple', 'Union', 'TYPE_CHECKING', 'Callable', 'Set',
    'datetime', 'timedelta', 'timezone', 'time',
    'dataclass', 'field', 'asdict',
    'Path', 'os', 'sys', 'json', 're',
    'Counter', 'defaultdict', 'deque',

    # Logging
    'enviar_senal_log', 'log_info', 'log_error', 'log_warning',

    # ICT Engine
    'ICTDetector', 'MarketContext',
    'update_market_context', 'detectar_fair_value_gaps', 'detectar_swing_points',

    # POI System
    'POIDetector',

    # Dashboard
    'DashboardController',

    # Utils
    'MT5DataManager',

    # Config
    'get_trading_config',
]

# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def get_sic_status():
    """Obtener estado del SIC"""
    return {
        'version': '3.0-Limpio',
        'logging_available': logging_available,
        'typing_available': typing_available,
        'datetime_available': datetime_available,
        'dataclasses_available': dataclasses_available,
        'collections_available': collections_available,
        'ict_engine_available': ict_engine_available,
        'poi_system_available': poi_system_available,
        'dashboard_available': dashboard_available,
        'utils_available': utils_available,
        'total_exports': len(__all__),
    }

def get_available_components():
    """Obtener componentes disponibles"""
    status = get_sic_status()
    available = {}

    for key, value in status.items():
        if key.endswith('_available') and value:
            component_name = key.replace('_available', '')
            available[component_name] = True

    return available

def validate_sic_integrity():
    """Validar integridad del SIC"""
    try:
        status = get_sic_status()
        issues = []

        # Verificar componentes críticos
        if not status['logging_available']:
            issues.append("Sistema de logging no disponible")

        if not status['typing_available']:
            issues.append("Typing no disponible")

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'status': status
        }

    except Exception as e:
        return {
            'valid': False,
            'issues': [f"Error validando SIC: {e}"],
            'status': None
        }

# =============================================================================
# INICIALIZACIÓN
# =============================================================================

def _initialize_sic():
    """Inicializar SIC limpio"""
    try:
        status = get_sic_status()

        if enviar_senal_log:
            available_count = sum(1 for k, v in status.items() if k.endswith('_available') and v)
            total_modules = len([k for k in status.keys() if k.endswith('_available')])

            enviar_senal_log("INFO", f"🎯 SIC v3.0 Limpio inicializado", "sic", "init")
            enviar_senal_log("INFO", f"📦 {available_count}/{total_modules} módulos disponibles", "sic", "init")
            enviar_senal_log("INFO", f"📋 {len(__all__)} componentes exportados", "sic", "init")

        return True

    except Exception as e:
        if enviar_senal_log:
            enviar_senal_log("ERROR", f"❌ Error inicializando SIC: {e}", "sic", "init")
        return False

# Inicializar automáticamente
_sic_initialized = _initialize_sic()

# Información del módulo
__version__ = "3.0.0"
__author__ = "Sistema ITC Engine v5.0"
__description__ = "Sistema de Imports Centralizados Limpio"

# Log final si está disponible
if enviar_senal_log and _sic_initialized:
    status = get_sic_status()
    available_count = sum(1 for k, v in status.items() if k.endswith('_available') and v)
    total_modules = len([k for k in status.keys() if k.endswith('_available')])
    success_rate = (available_count / total_modules * 100) if total_modules > 0 else 0

    enviar_senal_log("INFO", f"✅ SIC v3.0 operativo - Tasa éxito: {success_rate:.1f}%", "sic", "status")
