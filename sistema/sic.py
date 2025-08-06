"""
🎯 SISTEMA DE IMPORTS CENTRALIZADOS (SIC) v2.1 - EXPANDIDO
=========================================================
Sistema centralizado y expandido para imports del ITC Engine

AUTO-EXPANDIDO basado en análisis de imports más comunes del proyecto

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
Versión: v2.1 - Expandido Automáticamente

CARACTERÍSTICAS v2.1:
- Imports automáticamente detectados y priorizados
- Standard library completa más usada
- Project modules centralizados
- Carga robusta con fallback
- API pública expandida
"""

# =============================================================================
# IMPORTS STANDARD LIBRARY - AUTO-DETECTADOS
# =============================================================================

# Typing - Componentes más usados
try:
    from typing import Dict, List, Optional, Any, Tuple, Union, TYPE_CHECKING, Callable, Set
    TYPING_AVAILABLE = True
except ImportError:
    # Fallback para compatibilidad
    Dict = dict
    List = list
    Optional = type(None)
    Any = object
    Tuple = tuple
    Union = type
    TYPE_CHECKING = False
    Callable = type
    Set = set
    TYPING_AVAILABLE = False

# Datetime - Componentes más usados
try:
    from datetime import datetime, timedelta, timezone, time
    DATETIME_AVAILABLE = True
except ImportError:
    import datetime as dt
    datetime = dt.datetime
    timedelta = dt.timedelta
    timezone = dt.timezone
    time = dt.time
    DATETIME_AVAILABLE = False

# Dataclasses - Componentes más usados
try:
    from dataclasses import dataclass, field, asdict
    DATACLASSES_AVAILABLE = True
except ImportError:
    def dataclass(cls):
        return cls
    def field(**kwargs):
        return None
    def asdict(obj):
        return obj.__dict__ if hasattr(obj, '__dict__') else {}
    DATACLASSES_AVAILABLE = False

# Pathlib - Path más usado
try:
    from pathlib import Path
    PATHLIB_AVAILABLE = True
except ImportError:
    import os
    class Path:
        def __init__(self, path):
            self.path = str(path)
        def __str__(self):
            return self.path
    PATHLIB_AVAILABLE = False

# Standard Library - Básicos más usados
import os
import sys
import json
import time
import re

# Collections - Componentes más usados
try:
    from collections import Counter, defaultdict, deque
    COLLECTIONS_AVAILABLE = True
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
    COLLECTIONS_AVAILABLE = False

# =============================================================================
# IMPORTS DE PROYECTO - AUTO-DETECTADOS
# =============================================================================

# Logging - Sistema más usado del proyecto
try:
    from sistema.smart_directory_logger import logger, get_logger, setup_logging
    from sistema.logging_interface import enviar_senal_log, log_info, log_error, log_trading_decision
    LOGGING_AVAILABLE = True
except ImportError:
    import logging
    logger = logging.getLogger(__name__)
    def enviar_senal_log(level, msg, module, category):
        logger.log(getattr(logging, level, logging.INFO), f"[{module}:{category}] {msg}")
    def log_info(msg): logger.info(msg)
    def log_error(msg): logger.error(msg)
    def log_trading_decision(msg): logger.info(f"[TRADING] {msg}")
    get_logger = lambda: logger
    setup_logging = lambda: None
    LOGGING_AVAILABLE = False

# Core ICT Engine - Componentes más usados
try:
    from core.ict_engine.ict_detector import (
        ICTDetector, MarketContext, OptimizedICTAnalysis,
        update_market_context, detectar_fair_value_gaps, detectar_swing_points
    )
    from core.ict_engine.ict_analyzer import ICTAnalyzer
    from core.ict_engine.concepts.fair_value_gap import FairValueGap
    from core.ict_engine.concepts.order_block import OrderBlock
    ICT_ENGINE_AVAILABLE = True
except ImportError:
    ICTDetector = None
    MarketContext = None
    OptimizedICTAnalysis = None
    ICTAnalyzer = None
    FairValueGap = None
    OrderBlock = None

    # Fallbacks para funciones ICT
    def update_market_context(*args, **kwargs):
        """Fallback: actualizar contexto de mercado"""
        return {}

    def detectar_fair_value_gaps(*args, **kwargs):
        """Fallback: detectar fair value gaps"""
        return []

    def detectar_swing_points(*args, **kwargs):
        """Fallback: detectar swing points"""
        return []

    ICT_ENGINE_AVAILABLE = False

# Core POI System - Componentes más usados
try:
    from core.poi_system.poi_manager import POISystem, POIManager
    from core.poi_system.poi_detector import POIDetector
    from core.poi_system.poi_analyzer import POIAnalyzer
    POI_SYSTEM_AVAILABLE = True
except ImportError:
    POISystem = None
    POIManager = None
    POIDetector = None
    POIAnalyzer = None
    POI_SYSTEM_AVAILABLE = False

# Dashboard - Componentes más usados
try:
    from dashboard.dashboard_controller import DashboardController
    from dashboard.dashboard_widgets import DashboardWidget
    DASHBOARD_AVAILABLE = True
except ImportError:
    DashboardController = None
    DashboardWidget = None
    DASHBOARD_AVAILABLE = False

# Sistema - Componentes más usados
try:
    from sistema.market_status_detector_v3 import MarketStatusDetector
    from sistema.trading_schedule import TradingSchedule
    from sistema.system_monitor import SystemMonitor
    SISTEMA_AVAILABLE = True
except ImportError:
    MarketStatusDetector = None
    TradingSchedule = None
    SystemMonitor = None
    SISTEMA_AVAILABLE = False

# Utils - Componentes más usados
try:
    from utils.mt5_data_manager import MT5DataManager, get_mt5_manager
    UTILS_AVAILABLE = True
except ImportError:
    MT5DataManager = None
    get_mt5_manager = None
    UTILS_AVAILABLE = False

# Config - Componentes más usados
try:
    from config.config_manager import ConfigManager, get_trading_config
    from config.live_account_validator import LiveAccountValidator
    CONFIG_AVAILABLE = True
except ImportError:
    ConfigManager = None
    LiveAccountValidator = None
    # Fallback para get_trading_config
    def get_trading_config():
        return {
            'SIMBOLO': 'XAUUSD',
            'TIMEFRAME': 'H1',
            'LEVERAGE': 100,
            'RISK_PERCENT': 2.0
        }
    CONFIG_AVAILABLE = False

# =============================================================================
# API PÚBLICA EXPANDIDA - AUTO-GENERADA
# =============================================================================

# Standard Library Exports
__all__ = [
    # Typing
    'Dict', 'List', 'Optional', 'Any', 'Tuple', 'Union', 'TYPE_CHECKING', 'Callable', 'Set',

    # Datetime
    'datetime', 'timedelta', 'timezone', 'time',

    # Dataclasses
    'dataclass', 'field', 'asdict',

    # Pathlib
    'Path',

    # Standard
    'os', 'sys', 'json', 're',

    # Logging
    'logger', 'enviar_senal_log', 'log_info', 'log_error', 'log_trading_decision',
]

# Add available components conditionally
if ICT_ENGINE_AVAILABLE:
    __all__.extend(['ICTDetector', 'MarketContext', 'OptimizedICTAnalysis', 'ICTAnalyzer', 'FairValueGap', 'OrderBlock',
                   'update_market_context', 'detectar_fair_value_gaps', 'detectar_swing_points'])
else:
    __all__.extend(['update_market_context', 'detectar_fair_value_gaps', 'detectar_swing_points'])  # Fallbacks always available

if POI_SYSTEM_AVAILABLE:
    __all__.extend(['POISystem', 'POIManager', 'POIDetector', 'POIAnalyzer'])

if DASHBOARD_AVAILABLE:
    __all__.extend(['DashboardController', 'DashboardWidget'])

if SISTEMA_AVAILABLE:
    __all__.extend(['MarketStatusDetector', 'TradingSchedule', 'SystemMonitor'])

if UTILS_AVAILABLE:
    __all__.extend(['MT5DataManager', 'get_mt5_manager'])

if CONFIG_AVAILABLE:
    __all__.extend(['ConfigManager', 'LiveAccountValidator', 'get_trading_config'])
else:
    __all__.extend(['get_trading_config'])  # Fallback always available

# =============================================================================
# FUNCIONES DE UTILIDAD EXPANDIDAS
# =============================================================================

def get_sic_status():
    """📊 Obtener estado completo del SIC expandido"""
    return {
        'version': 'v2.1-Expandido',
        'total_exports': len(__all__),
        'availability': {
            'typing': TYPING_AVAILABLE,
            'datetime': DATETIME_AVAILABLE,
            'dataclasses': DATACLASSES_AVAILABLE,
            'pathlib': PATHLIB_AVAILABLE,
            'logging': LOGGING_AVAILABLE,
            'ict_engine': ICT_ENGINE_AVAILABLE,
            'poi_system': POI_SYSTEM_AVAILABLE,
            'dashboard': DASHBOARD_AVAILABLE,
            'sistema': SISTEMA_AVAILABLE,
            'utils': UTILS_AVAILABLE,
            'config': CONFIG_AVAILABLE,
        },
        'available_count': sum([
            TYPING_AVAILABLE, DATETIME_AVAILABLE, DATACLASSES_AVAILABLE,
            PATHLIB_AVAILABLE, LOGGING_AVAILABLE, ICT_ENGINE_AVAILABLE,
            POI_SYSTEM_AVAILABLE, DASHBOARD_AVAILABLE, SISTEMA_AVAILABLE,
            UTILS_AVAILABLE, CONFIG_AVAILABLE
        ]),
        'total_modules': 11,
        'success_rate': None  # Will be calculated
    }

def get_available_components():
    """📦 Obtener componentes disponibles categorizados"""
    status = get_sic_status()
    status['success_rate'] = (status['available_count'] / status['total_modules']) * 100

    available = {}
    for category, is_available in status['availability'].items():
        if is_available:
            available[category] = True

    return available

def validate_sic_integrity():
    """✅ Validar integridad del SIC expandido"""
    try:
        status = get_sic_status()
        issues = []

        # Verificar componentes críticos
        critical_components = ['typing', 'logging']
        for component in critical_components:
            if not status['availability'][component]:
                issues.append(f"Componente crítico no disponible: {component}")

        # Verificar exports
        if len(__all__) < 20:
            issues.append(f"Pocos exports disponibles: {len(__all__)}")

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
# INICIALIZACIÓN DEL SIC EXPANDIDO
# =============================================================================

def _initialize_sic():
    """🚀 Inicializar SIC expandido"""
    try:
        status = get_sic_status()

        if LOGGING_AVAILABLE:
            logger.info(f"🎯 SIC v2.1 Expandido cargado - {status['available_count']}/{status['total_modules']} módulos disponibles")
            logger.info(f"📦 {len(__all__)} componentes exportados")

        return True

    except Exception as e:
        if LOGGING_AVAILABLE:
            logger.error(f"❌ Error inicializando SIC expandido: {e}")
        return False

# Inicializar automáticamente
_sic_initialized = _initialize_sic()

# =============================================================================
# ALIASES Y COMPATIBILIDAD
# =============================================================================

# Aliases para compatibilidad con código existente
smart_directory_logger = logger if LOGGING_AVAILABLE else None
ict_detector = ICTDetector if ICT_ENGINE_AVAILABLE else None
poi_system = POISystem if POI_SYSTEM_AVAILABLE else None

# Información del módulo
__version__ = "2.1.0"
__author__ = "Sistema Sentinel Grid"
__description__ = "Sistema de Imports Centralizados Expandido"

# Log final de estado
if LOGGING_AVAILABLE and _sic_initialized:
    final_status = get_sic_status()
    logger.info(f"✅ SIC v2.1 inicializado - Success rate: {final_status.get('success_rate', 0):.1f}%")
