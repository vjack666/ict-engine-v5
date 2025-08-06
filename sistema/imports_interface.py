"""
🎯 SISTEMA DE IMPORTS CENTRALIZADO (SIC) v2.0 - REACTIVADO
=========================================================

✅ ARCHIVO REACTIVADO: Sistema principal de imports centralizado

Este es el sistema principal de imports del ITC Engine v5.0.
Proporciona acceso unificado a todas las dependencias.

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
Estado: ACTIVO - Sistema Principal
Basado en: SLUC v2.0 (patrón exitoso)
"""

# === IMPORTS BÁSICOS SEGUROS ===
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime, timedelta, timezone
import logging
import json
import time
import asyncio
from dataclasses import dataclass, field, asdict
import re

# === CONFIGURAR PATHS PYTHON ===
# Asegurar que Python encuentre todos los módulos
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# =============================================================================
# IMPORTS ICT ENGINE - ANÁLISIS TÉCNICO
# =============================================================================
ict_engine_available = True
try:
    from core.ict_engine.ict_engine import ICTEngine, get_ict_engine
    from core.ict_engine.ict_detector import ICTDetector
    from core.ict_engine.ict_types import ICTPattern, TradingDirection, SessionType, PATTERN_EMOJIS
    from core.ict_engine.confidence_engine import ConfidenceEngine, CONFIDENCE_CONFIG
    from core.ict_engine.veredicto_engine_v4 import VeredictoEngine
    from core.ict_engine.pattern_analyzer import ICTPatternAnalyzer
    from core.ict_engine.fractal_analyzer import FractalAnalyzer
except ImportError:
    ict_engine_available = False
    print("⚠️  ICT Engine components no disponibles")

# =============================================================================
# IMPORTS POI SYSTEM - SISTEMA DE PUNTOS DE INTERÉS
# =============================================================================
poi_system_available = True
try:
    from core.poi_system.poi_detector import POIDetector
    from core.poi_system.poi_scoring_engine import POIScoringEngine
    from core.poi_system.poi_system import POISystem
except ImportError:
    poi_system_available = False
    print("⚠️  POI System components no disponibles")

# =============================================================================
# IMPORTS DASHBOARD - INTERFAZ DE USUARIO
# =============================================================================
dashboard_available = True
try:
    from dashboard.dashboard_definitivo import SentinelDashboardDefinitivo as SentinelDashboard
    from dashboard.dashboard_controller import DashboardController
    from dashboard.hibernacion_perfecta import render_hibernacion_perfecta, detectar_mt5_optimizado
    from dashboard.ict_professional_widget import ICTProfessionalWidget
except ImportError:
    dashboard_available = False
    print("⚠️  Dashboard components no disponibles")

# =============================================================================
# IMPORTS SISTEMA - INFRAESTRUCTURA
# =============================================================================
sistema_available = True
try:
    from sistema.logging_interface import enviar_senal_log, log_info, log_error, log_ict, log_poi, log_dashboard, log_mt5, log_tct
    from sistema.config import SAFE_DATA_DIR, ZONA_HORARIA_LOCAL
    from sistema.market_status_detector_v3 import MarketStatusDetector
except ImportError:
    sistema_available = False
    print("⚠️  Sistema components no disponibles")

# =============================================================================
# IMPORTS UTILS - UTILIDADES
# =============================================================================
utils_available = True
try:
    from utils.mt5_data_manager import get_mt5_manager, MT5DataManager
    from utils.logging_utils import get_logger
except ImportError:
    utils_available = False
    print("⚠️  Utils components no disponibles")

# =============================================================================
# IMPORTS ANÁLISIS - ACC SYSTEM
# =============================================================================
acc_available = True
try:
    from core.analysis_command_center import AnalysisOrchestrator
    from core.analysis_command_center.tct_pipeline import TCTFormatter, AggregatedTCTMetrics
    from core.analysis_command_center.acc_flow_controller import AccFlowController, FlowPriority
    from core.analytics.ict_analyzer import ICTAnalyzer
except ImportError:
    acc_available = False
    print("⚠️  ACC System components no disponibles")

# =============================================================================
# IMPORTS DATA MANAGEMENT - GESTIÓN DE DATOS
# =============================================================================
data_management_available = True
try:
    from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
    from core.data_management.candle_coordinator import CandleCoordinator, DownloadRequest, DownloadStatus
except ImportError:
    data_management_available = False
    print("⚠️  Data Management components no disponibles")

# =============================================================================
# IMPORTS RISK MANAGEMENT - GESTIÓN DE RIESGO
# =============================================================================
risk_management_available = True
try:
    # Placeholder para futuros componentes de risk management
    pass
except ImportError:
    risk_management_available = False
    print("⚠️  Risk Management components no disponibles")

# =============================================================================
# CLASE PRINCIPAL DEL SIC
# =============================================================================

class ImportsCentral:
    """
    🎯 CLASE PRINCIPAL DEL SISTEMA DE IMPORTS CENTRALIZADO

    Proporciona acceso unificado a todas las dependencias del sistema
    siguiendo el patrón Singleton, similar al SLUC v2.0.

    Características:
    - Punto único de acceso a todos los componentes
    - Cache interno para optimizar rendimiento
    - Inicialización lazy de componentes
    - API consistente y fácil de usar
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        """Implementación del patrón Singleton"""
        if cls._instance is None:
            cls._instance = super(ImportsCentral, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicialización lazy del sistema"""
        if not self._initialized:
            self._cache = {}
            self._components_status = {
                'ict_engine': ict_engine_available,
                'poi_system': poi_system_available,
                'dashboard': dashboard_available,
                'sistema': sistema_available,
                'utils': utils_available,
                'acc': acc_available,
                'data_management': data_management_available,
                'risk_management': risk_management_available
            }
            self._initialized = True

    def get_system_status(self) -> Dict[str, bool]:
        """Obtiene el estado de disponibilidad de todos los componentes"""
        return self._components_status.copy()

    def get_ict_components(self) -> Dict[str, Any]:
        """Obtener todos los componentes del motor ICT"""
        if not ict_engine_available:
            return {}

        if 'ict' not in self._cache:
            self._cache['ict'] = {
                'engine': ICTEngine,
                'detector': ICTDetector,
                'confidence': ConfidenceEngine,
                'veredicto': VeredictoEngine,
                'pattern_analyzer': ICTPatternAnalyzer,
                'fractal_analyzer': FractalAnalyzer,
                'patterns': ICTPattern,
                'directions': TradingDirection,
                'sessions': SessionType,
                'emojis': PATTERN_EMOJIS
            }
        return self._cache['ict']

    def get_poi_components(self) -> Dict[str, Any]:
        """Obtener componentes del sistema POI"""
        if not poi_system_available:
            return {}

        if 'poi' not in self._cache:
            self._cache['poi'] = {
                'detector': POIDetector,
                'scoring': POIScoringEngine,
                'system': POISystem
            }
        return self._cache['poi']

    def get_dashboard_components(self) -> Dict[str, Any]:
        """Obtener componentes del dashboard"""
        if not dashboard_available:
            return {}

        if 'dashboard' not in self._cache:
            self._cache['dashboard'] = {
                'main': SentinelDashboard,
                'controller': DashboardController,
                'ict_professional': ICTProfessionalWidget,
                'functions': {
                    'render_hibernacion': render_hibernacion_perfecta,
                    'detectar_mt5': detectar_mt5_optimizado
                }
            }
        return self._cache['dashboard']

    def get_sistema_components(self) -> Dict[str, Any]:
        """Obtener componentes del sistema de infraestructura"""
        if not sistema_available:
            return {}

        if 'sistema' not in self._cache:
            self._cache['sistema'] = {
                'logging': {
                    'enviar_senal_log': enviar_senal_log,
                    'log_info': log_info,
                    'log_error': log_error,
                    'log_ict': log_ict,
                    'log_poi': log_poi,
                    'log_dashboard': log_dashboard,
                    'log_mt5': log_mt5,
                    'log_tct': log_tct
                },
                'config': {
                    'data_dir': SAFE_DATA_DIR,
                    'zona_horaria': ZONA_HORARIA_LOCAL
                },
                'monitoring': {
                    'market_status': MarketStatusDetector
                }
            }
        return self._cache['sistema']

    def get_utils_components(self) -> Dict[str, Any]:
        """Obtener componentes de utilidades"""
        if not utils_available:
            return {}

        if 'utils' not in self._cache:
            self._cache['utils'] = {
                'mt5_manager': get_mt5_manager,
                'mt5_class': MT5DataManager,
                'get_logger': get_logger
            }
        return self._cache['utils']

    def get_acc_components(self) -> Dict[str, Any]:
        """Obtener componentes del Analysis Command Center"""
        if not acc_available:
            return {}

        if 'acc' not in self._cache:
            self._cache['acc'] = {
                'orchestrator': AnalysisOrchestrator,
                'tct_formatter': TCTFormatter,
                'tct_metrics': AggregatedTCTMetrics,
                'flow_controller': AccFlowController,
                'flow_priority': FlowPriority,
                'ict_analyzer': ICTAnalyzer
            }
        return self._cache['acc']

    def get_data_management_components(self) -> Dict[str, Any]:
        """Obtener componentes de gestión de datos"""
        if not data_management_available:
            return {}

        if 'data_management' not in self._cache:
            self._cache['data_management'] = {
                'candle_downloader': AdvancedCandleDownloader,
                'candle_coordinator': CandleCoordinator,
                'download_request': DownloadRequest,
                'download_status': DownloadStatus
            }
        return self._cache['data_management']

    def get_risk_management_components(self) -> Dict[str, Any]:
        """Obtener componentes de gestión de riesgo"""
        if not risk_management_available:
            return {}

        if 'risk_management' not in self._cache:
            self._cache['risk_management'] = {
                # Placeholder para futuros componentes
            }
        return self._cache['risk_management']

# =============================================================================
# INSTANCIA GLOBAL - SINGLETON PATTERN
# =============================================================================
_sic_instance = ImportsCentral()

# =============================================================================
# FUNCIONES DE CONVENIENCIA - API PÚBLICA
# =============================================================================

def get_ict_engine():
    """Obtener clase del motor ICT"""
    components = _sic_instance.get_ict_components()
    return components.get('engine') if components else None

def get_ict_detector():
    """Obtener clase del detector ICT"""
    components = _sic_instance.get_ict_components()
    return components.get('detector') if components else None

def get_poi_system():
    """Obtener clase del sistema POI"""
    components = _sic_instance.get_poi_components()
    return components.get('system') if components else None

def get_poi_detector():
    """Obtener clase del detector POI"""
    components = _sic_instance.get_poi_components()
    return components.get('detector') if components else None

def get_dashboard():
    """Obtener clase del dashboard principal"""
    components = _sic_instance.get_dashboard_components()
    return components.get('main') if components else None

def get_dashboard_controller():
    """Obtener clase del controlador de dashboard"""
    components = _sic_instance.get_dashboard_components()
    return components.get('controller') if components else None

def get_logging():
    """Obtener diccionario con todas las funciones de logging"""
    components = _sic_instance.get_sistema_components()
    return components.get('logging', {}) if components else {}

def get_mt5_manager():
    """Obtener función para obtener el manager MT5"""
    components = _sic_instance.get_utils_components()
    return components.get('mt5_manager') if components else None

def get_analysis_orchestrator():
    """Obtener clase del orquestador de análisis"""
    components = _sic_instance.get_acc_components()
    return components.get('orchestrator') if components else None

def get_candle_downloader():
    """Obtener clase del descargador de velas"""
    components = _sic_instance.get_data_management_components()
    return components.get('candle_downloader') if components else None

def get_system_status():
    """Obtener estado de disponibilidad de todos los componentes"""
    return _sic_instance.get_system_status()

# =============================================================================
# FUNCIONES DE LOGGING DIRECTO - COMPATIBILIDAD CON SLUC
# =============================================================================

def sic_log(message: str, level: str = "INFO", component: str = "SIC"):
    """Función de logging usando el sistema unificado"""
    logging_funcs = get_logging()
    if logging_funcs and 'enviar_senal_log' in logging_funcs:
        logging_funcs['enviar_senal_log'](message, level, component)
    else:
        print(f"[{level}] {component}: {message}")

# =============================================================================
# TIPOS COMUNES EXPORTADOS
# =============================================================================

# Importar tipos comunes para uso directo
SIC_TYPES = {
    'Dict': Dict,
    'List': List,
    'Optional': Optional,
    'Tuple': Tuple,
    'Any': Any,
    'Union': Union,
    'dataclass': dataclass,
    'field': field,
    'asdict': asdict,
    'datetime': datetime,
    'timedelta': timedelta,
    'timezone': timezone,
    'Path': Path,
    'asyncio': asyncio,
    'json': json,
    'time': time,
    'sys': sys,
    'os': os,
    're': re
}

# =============================================================================
# EXPORTACIONES PARA IMPORTACIÓN DIRECTA
# =============================================================================
__all__ = [
    # Instancia central
    'ImportsCentral', '_sic_instance',

    # Funciones de conveniencia principales
    'get_ict_engine', 'get_ict_detector', 'get_poi_system', 'get_poi_detector',
    'get_dashboard', 'get_dashboard_controller', 'get_logging', 'get_mt5_manager',
    'get_analysis_orchestrator', 'get_candle_downloader', 'get_system_status',

    # Función de logging del SIC
    'sic_log',

    # Tipos comunes
    'Dict', 'List', 'Optional', 'Tuple', 'Any', 'Union',
    'dataclass', 'field', 'asdict', 'datetime', 'timedelta', 'timezone',
    'Path', 'asyncio', 'json', 'time', 'sys', 'os', 're',

    # Tipos y enums ICT (si están disponibles)
    'ICTPattern', 'TradingDirection', 'SessionType', 'PATTERN_EMOJIS',

    # Logging directo (compatibilidad con SLUC)
    'enviar_senal_log', 'log_info', 'log_error',
    'log_ict', 'log_poi', 'log_dashboard', 'log_mt5', 'log_tct'
]

# =============================================================================
# INICIALIZACIÓN Y VERIFICACIÓN
# =============================================================================

def verify_sic_status():
    """Verifica el estado del SIC y muestra información de disponibilidad"""
    status = get_system_status()
    available_count = sum(1 for available in status.values() if available)
    total_count = len(status)

    print(f"🎯 SISTEMA DE IMPORTS CENTRALIZADO (SIC) v1.0")
    print(f"═══════════════════════════════════════════════")
    print(f"📊 Componentes disponibles: {available_count}/{total_count}")
    print(f"📍 Instancia: {id(_sic_instance)}")

    for component, available in status.items():
        status_icon = "✅" if available else "❌"
        print(f"   {status_icon} {component}")

    if available_count == total_count:
        print(f"🚀 SIC completamente funcional")
    elif available_count > 0:
        print(f"⚠️  SIC parcialmente funcional")
    else:
        print(f"❌ SIC con problemas de carga")

    return status

# Verificación automática al importar
if __name__ == "__main__":
    verify_sic_status()
else:
    # Logging silencioso de inicialización
    sic_log("Sistema de Imports Centralizado (SIC) v1.0 inicializado", "INFO", "SIC")
