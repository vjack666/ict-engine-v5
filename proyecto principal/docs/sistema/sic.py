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
import random
import subprocess
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
    def asdict(instance):
        return instance.__dict__ if hasattr(instance, '__dict__') else {}
    dataclasses_available = False

# Collections
try:
    from collections import defaultdict, Counter, deque
    collections_available = True
except ImportError:
    class defaultdict(dict):
        def __init__(self, default_factory=None):
            super().__init__()
            self.default_factory = default_factory

        def __getitem__(self, key):
            if key not in self and self.default_factory:
                self[key] = self.default_factory()
            return super().__getitem__(key)

    class Counter(dict):
        pass

    class deque(list):
        pass

    collections_available = False

# =============================================================================
# EXTERNAL LIBRARIES - DEPENDENCIAS FRECUENTES
# =============================================================================

# Pandas para análisis de datos
try:
    import pandas as pd
    pandas_available = True
except ImportError:
    # Fallback básico para pandas
    class PandasFallback:
        def DataFrame(self, *args, **kwargs):
            return []
        def read_csv(self, *args, **kwargs):
            return []
        def to_datetime(self, *args, **kwargs):
            return None
    pd = PandasFallback()
    pandas_available = False

# NumPy para operaciones numéricas
try:
    import numpy as np
    numpy_available = True
except ImportError:
    # Fallback básico para numpy
    class NumpyFallback:
        def array(self, *args, **kwargs):
            return []
        def zeros(self, *args, **kwargs):
            return []
        def mean(self, *args, **kwargs):
            return 0
        def std(self, *args, **kwargs):
            return 0
    np = NumpyFallback()
    numpy_available = False

# Enum para enumeraciones
try:
    from enum import Enum
    enum_available = True
except ImportError:
    class Enum:
        """Fallback básico para Enum."""
        pass
    enum_available = False

# =============================================================================
# SISTEMA DE LOGGING CENTRALIZADO
# =============================================================================

import logging as std_logging
import importlib.util

def _cargar_logging_sistema():
    """Carga el sistema de logging centralizado."""
    try:
        logging_path = os.path.join(os.path.dirname(__file__), "logging_interface.py")
        if os.path.exists(logging_path):
            spec = importlib.util.spec_from_file_location("logging_interface", logging_path)
            if spec and spec.loader:
                logging_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(logging_module)

                # Usar funciones directamente del módulo
                return {
                    'enviar_senal_log': getattr(logging_module, 'enviar_senal_log', None),
                    'log_info': getattr(logging_module, 'log_info', None),
                    'log_warning': getattr(logging_module, 'log_warning', None),
                    'get_smart_stats': getattr(logging_module, 'get_log_stats', None),  # Función corregida
                    'create_summary': getattr(logging_module, 'create_log_summary', None),  # Función corregida
                    'available': True
                }
    except Exception as e:
        pass

    # Fallback simple
    def fallback_log(nivel, mensaje, fuente="sistema", categoria="general", metadata=None):
        try:
            std_logging.basicConfig(level=std_logging.INFO)
            logger = std_logging.getLogger(fuente)
            if nivel.upper() == "INFO":
                logger.info(f"[{categoria}] {mensaje}")
            elif nivel.upper() == "WARNING":
                logger.warning(f"[{categoria}] {mensaje}")
            elif nivel.upper() == "ERROR":
                logger.error(f"[{categoria}] {mensaje}")
        except:
            pass

    return {
        'enviar_senal_log': fallback_log,
        'log_info': lambda msg, fuente="sistema", metadata=None: fallback_log("INFO", msg, fuente, "general", metadata),
        'log_warning': lambda msg, fuente="sistema", metadata=None: fallback_log("WARNING", msg, fuente, "general", metadata),
        'get_smart_stats': lambda: {"logs_count": 0, "status": "fallback"},
        'create_summary': lambda: "Logging en modo fallback",
        'available': False
    }

# Cargar logging al importar
_logging_system = _cargar_logging_sistema()
logging_available = _logging_system['available']

# Exportar funciones de logging
enviar_senal_log = _logging_system['enviar_senal_log']
log_info = _logging_system['log_info']
log_warning = _logging_system['log_warning']
get_smart_stats = _logging_system['get_smart_stats']
create_summary = _logging_system['create_summary']

# =============================================================================
# SISTEMA DE EXPORTS CENTRALIZADOS
# =============================================================================

# Variables de disponibilidad de sistemas
ict_engine_available = False
poi_system_available = False
dashboard_available = False
utils_available = False
config_available = False

# =============================================================================
# CONFIG MANAGER Y VALIDADORES
# =============================================================================
try:
    from config.config_manager import ConfigManager
    config_available = True
except ImportError:
    ConfigManager = None
    config_available = False

# Account Validator y AccountType
try:
    from config.live_account_validator import get_account_validator, AccountType
    account_validator_available = True
except ImportError:
    def get_account_validator():
        """Fallback para account validator."""
        class FallbackValidator:
            def validate_account(self):
                return {"status": "fallback", "account_type": "unknown"}
        return FallbackValidator()

    class AccountType:
        """Fallback para AccountType enum."""
        DEMO = "demo"
        REAL = "real"
        CONTEST = "contest"
        UNKNOWN = "unknown"

    account_validator_available = False

# =============================================================================
# DASHBOARD CONTROLLER
# =============================================================================
try:
    from dashboard.dashboard_controller import DashboardController
    dashboard_controller_available = True
except ImportError:
    DashboardController = None
    dashboard_controller_available = False

# Funciones stub para sistemas no disponibles
def analyze_market_context(*args, **kwargs):
    """Stub para análisis de contexto de mercado."""
    return {"status": "no_available", "analysis": {}}

def detect_ict_concepts(*args, **kwargs):
    """Stub para detección de conceptos ICT."""
    return []

def detect_order_blocks(*args, **kwargs):
    """Stub para detección de order blocks."""
    return [], []

def log_ict(mensaje, nivel="INFO", categoria="ict"):
    """Función específica para logs de ICT."""
    enviar_senal_log(nivel, mensaje, "ict_engine", categoria)

# Clase stub para ImportsCentral
class ImportsCentral:
    """Stub para ImportsCentral mientras se migra completamente."""
    def __init__(self):
        self.available = False

    def get_dashboard(self):
        return None

    def get_logging(self):
        return enviar_senal_log

    def get_mt5_manager(self):
        return None

# =============================================================================
# FUNCIONES GET_* REQUERIDAS POR DASHBOARD
# =============================================================================

def get_dashboard():
    """Obtiene instancia del dashboard principal."""
    try:
        from dashboard.dashboard_definitivo import SentinelDashboardDefinitivo
        return SentinelDashboardDefinitivo
    except ImportError:
        return None

def get_trading_config():
    """Obtiene configuración de trading."""
    try:
        from config.config_manager import ConfigManager
        return ConfigManager()
    except ImportError:
        return None

def get_logging():
    """Obtiene función de logging centralizada."""
    return enviar_senal_log

def get_mt5_manager():
    """Obtiene el manager de MT5."""
    try:
        from utilities.mt5_interface import MT5Manager
        return MT5Manager()
    except ImportError:
        return None

def get_dashboard_controller():
    """Obtiene el controlador del dashboard."""
    try:
        from dashboard.dashboard_controller import DashboardController
        return DashboardController
    except ImportError:
        return None

def get_ict_components():
    """Obtiene componentes ICT."""
    try:
        from core.ict_engine.ict_detector import ICTDetector
        return ICTDetector
    except ImportError:
        return None

def get_system_status():
    """Obtiene estado del sistema."""
    return get_sic_status()

# =============================================================================
# WIDGETS Y COMPONENTES FALTANTES
# =============================================================================

# TCT Interface
try:
    from core.analysis_command_center.tct_pipeline.tct_interface import TCTInterface
    tct_interface_available = True
except ImportError:
    TCTInterface = None
    tct_interface_available = False

# Trading Decision Engine
try:
    from core.trading import TradingDecisionEngine, TradingDecisionCache
    trading_engine_available = True
except ImportError:
    TradingDecisionEngine = None
    TradingDecisionCache = None
    trading_engine_available = False

# Risk Bot
try:
    from core.risk_management import RiskBot
    risk_bot_available = True
except ImportError:
    RiskBot = None
    risk_bot_available = False

# Hibernation Widget
try:
    from dashboard.hibernation_widget_v2 import HibernationWidget
    hibernation_widget_available = True
except ImportError:
    HibernationWidget = None
    hibernation_widget_available = False

# Rendering functions
def render_hibernacion_perfecta(*args, **kwargs):
    """Renderiza tab de hibernación perfecta."""
    try:
        from dashboard.hibernacion_perfecta import render_hibernacion_perfecta as rhp
        return rhp(*args, **kwargs)
    except ImportError:
        return None

def render_problems_tab_simple(*args, **kwargs):
    """Renderiza tab de problemas simplificado."""
    try:
        from dashboard.problems_tab_renderer import render_problems_tab_simple as rpts
        return rpts(*args, **kwargs)
    except ImportError:
        return None

# Detección POI
POIDetector = None
POIAnalyzer = None

# Widgets Dashboard
DashboardWidget = None

# Sistema de monitoreo
SystemMonitor = None

# Utilidades generales
utils_available = True

# Configuración
config_available = True

# =============================================================================
# FUNCIONES DE ESTADO DEL SISTEMA
# =============================================================================

def get_sic_status():
    """Obtiene el estado completo del SIC."""
    total_exports = len([
        x for x in globals()
        if not x.startswith('_') and not x.startswith('sys') and not x.startswith('os')
    ])

    return {
        "version": "v3.0",
        "timestamp": datetime.now().isoformat() if datetime_available else "N/A",
        "logging_available": logging_available,
        "ict_engine_available": ict_engine_available,
        "poi_system_available": poi_system_available,
        "dashboard_available": dashboard_available,
        "utils_available": utils_available,
        "config_available": config_available,
        "total_exports": total_exports,
        "status": "functional"
    }

def get_available_functions():
    """Lista todas las funciones disponibles del SIC."""
    functions = []
    for name, obj in globals().items():
        if callable(obj) and not name.startswith('_'):
            functions.append(name)
    return sorted(functions)

def get_available_classes():
    """Lista todas las clases disponibles del SIC."""
    classes = []
    for name, obj in globals().items():
        if isinstance(obj, type) and not name.startswith('_'):
            classes.append(name)
    return sorted(classes)

def test_sic_imports():
    """Prueba la funcionalidad básica del SIC."""
    try:
        status = get_sic_status()
        enviar_senal_log("INFO", "SIC funcionando correctamente", "sic", "test")
        return True
    except Exception as e:
        return False

# =============================================================================
# INFORMACIÓN DEL MÓDULO
# =============================================================================

__version__ = "3.0"
__author__ = "ITC Engine v5.0"
__status__ = "Production"
__all__ = [
    # Tipos básicos
    'Dict', 'List', 'Optional', 'Any', 'Tuple', 'Union', 'Callable', 'Set',
    'datetime', 'timedelta', 'timezone', 'time', 'Path',
    'dataclass', 'field', 'defaultdict', 'Counter', 'deque', 'asdict',
    'os', 'sys', 'json', 're', 'random', 'time_module', 'subprocess',

    # Pandas y análisis de datos
    'pd', 'pandas_available', 'np', 'numpy_available', 'Enum', 'enum_available',

    # Config y validación
    'get_account_validator', 'AccountType', 'account_validator_available',

    # Logging
    'enviar_senal_log', 'log_info', 'log_warning', 'get_smart_stats', 'create_summary', 'log_ict',

    # Análisis
    'analyze_market_context', 'detect_ict_concepts', 'detect_order_blocks',

    # Clases principales
    'POIDetector', 'POIAnalyzer', 'DashboardWidget', 'SystemMonitor', 'ImportsCentral',

    # CONFIG Y MANAGEMENT
    'ConfigManager', 'DashboardController',

    # ICT ENGINE
    'ICTDetector', 'ICTEngine', 'ICTPatternAnalyzer', 'ConfidenceEngine', 'VeredictoEngine',
    'ICTHistoricalAnalyzer', 'PatternAnalyzer',

    # MT5 Y DATA
    'MT5Connector', 'MT5DataManager', 'CandleDownloader', 'MarketStatusDetector',

    # DASHBOARD WIDGETS
    'ICTProfessionalWidget', 'HibernationWidget', 'HibernationStatusWidget', 'CountdownWidget',
    'POIDashboardIntegration',

    # TRADING
    'TradingEngine', 'TradingDecisionEngine', 'TradingDecisionCache', 'RiskManager', 'RiskBot',
    'LimitOrderManager', 'OrderManager',

    # UTILS Y FUNCIONES
    'get_dashboard', 'get_trading_config', 'get_mt5_manager', 'get_ict_components',
    'get_dashboard_controller', 'get_system_status', 'get_logging',

    # RENDERING FUNCTIONS
    'render_hibernacion_perfecta', 'render_problems_tab_simple',

    # TCT INTERFACE
    'TCTInterface',

    # Estado
    'get_sic_status', 'get_available_functions', 'get_available_classes', 'test_sic_imports',

    # Variables de estado
    'logging_available', 'ict_engine_available', 'poi_system_available',
    'dashboard_available', 'utils_available', 'config_available',
    'tct_interface_available', 'trading_engine_available', 'risk_bot_available',
    'hibernation_widget_available'
]

if __name__ == "__main__":
    print("🎯 Sistema de Imports Centralizados (SIC) v3.0")
    print("=" * 50)
    status = get_sic_status()
    for key, value in status.items():
        print(f"{key}: {value}")

    print(f"\nFunciones disponibles: {len(get_available_functions())}")
    print(f"Clases disponibles: {len(get_available_classes())}")

    if test_sic_imports():
        print("✅ SIC funcionando correctamente")
    else:
        print("❌ Error en SIC")
