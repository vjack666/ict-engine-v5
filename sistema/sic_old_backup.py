"""
🎯 SISTEMA DE IMPORTS CENTRALIZADOS (SIC) v3.0 - CORREGIDO
==========================================================
Sistema centralizado para imports del ITC Engine

CARACTERÍSTICAS v3.0:
- Sin referencias circulares
- Imports validados únicamente
- Tipos correctos
- Logging centralizado desde logging_interface
- Fallbacks robustos

Autor: Sistema ITC Engine v5.0
Fecha: 2025-08-06
Versión: v3.0 - Estabilizado
"""

# =============================================================================
# IMPORTS STANDARD LIBRARY - VALIDADOS
# =============================================================================

# Typing - Componentes más usados (sin redefinir constantes)
try:
    from typing import Dict, List, Optional, Any, Tuple, Union, TYPE_CHECKING, Callable, Set
    typing_available = True
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
    typing_available = False

# Datetime - Componentes más usados
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

# Dataclasses - Componentes más usados
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

# Pathlib - Path más usado
try:
    from pathlib import Path as PathLibPath
    Path = PathLibPath
    pathlib_available = True
except ImportError:
    import os
    class Path:
        def __init__(self, path):
            self.path = str(path)
        def __str__(self):
            return self.path
        def exists(self):
            return os.path.exists(self.path)
        def mkdir(self, parents=False, exist_ok=False):
            if not os.path.exists(self.path):
                os.makedirs(self.path)
    pathlib_available = False

# Standard Library - Básicos más usados
import os
import sys
import json
import time as time_module
import re

# Collections - Componentes más usados
try:
    from collections import Counter as CollectionsCounter, defaultdict as CollectionsDefaultdict, deque as CollectionsDeque
    Counter = CollectionsCounter
    defaultdict = CollectionsDefaultdict  
    deque = CollectionsDeque
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
# IMPORTS DE PROYECTO - VALIDADOS SIN CICLOS
# =============================================================================

# Logging - Sistema más usado del proyecto (VALIDADO)
logging_available = False
logger = None
enviar_senal_log = None
log_info = None
log_error = None

# Importar logging básico primero
import logging as standard_logging

# Intentar cargar el sistema de logging del proyecto
try:
    # Importar desde logging_interface sin crear ciclos
    import sys
    import importlib.util
    
    # Cargar logging_interface dinámicamente
    spec = importlib.util.spec_from_file_location(
        "logging_interface", 
        os.path.join(os.path.dirname(__file__), "logging_interface.py")
    )
    if spec and spec.loader:
        logging_interface = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(logging_interface)
        
        enviar_senal_log = logging_interface.enviar_senal_log
        if hasattr(logging_interface, 'log_info'):
            log_info = logging_interface.log_info
        if hasattr(logging_interface, 'log_error'):
            log_error = logging_interface.log_error
            
        logging_available = True
        
        # También intentar obtener logger desde smart_directory_logger
        try:
            spec2 = importlib.util.spec_from_file_location(
                "smart_directory_logger",
                os.path.join(os.path.dirname(__file__), "smart_directory_logger.py") 
            )
            if spec2 and spec2.loader:
                smart_logger_module = importlib.util.module_from_spec(spec2)
                spec2.loader.exec_module(smart_logger_module)
                if hasattr(smart_logger_module, 'logger'):
                    logger = smart_logger_module.logger
        except Exception:
            pass
            
except Exception as e:
    # Fallback completo
    logger = standard_logging.getLogger(__name__)
    
    def enviar_senal_log(nivel, mensaje, fuente="sistema", categoria="general", metadata=None):
        """Fallback: enviar señal de log"""
        level = getattr(standard_logging, nivel.upper(), standard_logging.INFO)
        logger.log(level, f"[{fuente}:{categoria}] {mensaje}")
    
    def log_info(mensaje, fuente="sistema", metadata=None):
        """Fallback: log info"""
        logger.info(mensaje)
        
    def log_error(mensaje, fuente="sistema", metadata=None):
        """Fallback: log error"""
        logger.error(mensaje)

# Core ICT Engine - Componentes validados únicamente
ict_engine_available = False
ICTDetector = None
MarketContext = None
OptimizedICTAnalysis = None

try:
    # Solo importar lo que sabemos que existe
    spec = importlib.util.spec_from_file_location(
        "ict_detector",
        os.path.join(os.path.dirname(__file__), "..", "core", "ict_engine", "ict_detector.py")
    )
    if spec and spec.loader and os.path.exists(os.path.join(os.path.dirname(__file__), "..", "core", "ict_engine", "ict_detector.py")):
        ict_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ict_module)
        
        # Extraer solo lo que existe
        if hasattr(ict_module, 'ICTDetector'):
            ICTDetector = ict_module.ICTDetector
        if hasattr(ict_module, 'MarketContext'):  
            MarketContext = ict_module.MarketContext
        if hasattr(ict_module, 'OptimizedICTAnalysis'):
            OptimizedICTAnalysis = ict_module.OptimizedICTAnalysis
            
        ict_engine_available = True
        
except Exception as e:
    if enviar_senal_log:
        enviar_senal_log("WARNING", f"ICT Engine no disponible: {e}", "sic", "init")

# Funciones ICT - Fallbacks
def update_market_context(*args, **kwargs):
    """Fallback: actualizar contexto de mercado"""
    return {}

def detectar_fair_value_gaps(*args, **kwargs):
    """Fallback: detectar fair value gaps"""
    return []

def detectar_swing_points(*args, **kwargs):
    """Fallback: detectar swing points"""
    return []

# Core POI System - Componentes validados
poi_system_available = False
POISystem = None
POIManager = None
POIDetector = None

try:
    # Solo lo que existe
    poi_detector_path = os.path.join(os.path.dirname(__file__), "..", "core", "poi_system", "poi_detector.py")
    if os.path.exists(poi_detector_path):
        spec = importlib.util.spec_from_file_location("poi_detector", poi_detector_path)
        if spec and spec.loader:
            poi_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(poi_module)
            
            if hasattr(poi_module, 'POIDetector'):
                POIDetector = poi_module.POIDetector
                poi_system_available = True
                
except Exception as e:
    if enviar_senal_log:
        enviar_senal_log("WARNING", f"POI System no disponible: {e}", "sic", "init")

# Dashboard - Solo controller que sabemos existe
dashboard_available = False
DashboardController = None

try:
    controller_path = os.path.join(os.path.dirname(__file__), "..", "dashboard", "dashboard_controller.py")
    if os.path.exists(controller_path):
        spec = importlib.util.spec_from_file_location("dashboard_controller", controller_path)
        if spec and spec.loader:
            dashboard_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(dashboard_module)
            
            if hasattr(dashboard_module, 'DashboardController'):
                DashboardController = dashboard_module.DashboardController
                dashboard_available = True
                
except Exception as e:
    if enviar_senal_log:
        enviar_senal_log("WARNING", f"Dashboard no disponible: {e}", "sic", "init")

# Sistema - Solo componentes que existen
sistema_available = False
MarketStatusDetector = None

try:
    # Market Status Detector - sabemos que existe
    market_detector_path = os.path.join(os.path.dirname(__file__), "market_status_detector_v3.py")
    if os.path.exists(market_detector_path):
        spec = importlib.util.spec_from_file_location("market_status_detector_v3", market_detector_path)
        if spec and spec.loader:
            market_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(market_module)
            
            if hasattr(market_module, 'MarketStatusDetector'):
                MarketStatusDetector = market_module.MarketStatusDetector
                sistema_available = True
                
except Exception as e:
    if enviar_senal_log:
        enviar_senal_log("WARNING", f"Sistema components no disponibles: {e}", "sic", "init")

# Utils - Solo MT5DataManager que sabemos existe
utils_available = False
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
                
except Exception as e:
    if enviar_senal_log:
        enviar_senal_log("WARNING", f"Utils no disponibles: {e}", "sic", "init")

# Config - Componentes básicos
config_available = False
ConfigManager = None

def get_trading_config():
    """Fallback para configuración de trading"""
    return {
        'SIMBOLO': 'XAUUSD',
        'TIMEFRAME': 'H1', 
        'LEVERAGE': 100,
        'RISK_PERCENT': 2.0
    }

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
