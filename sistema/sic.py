"""
🎯 SISTEMA DE IMPORTS CENTRALIZADOS (SIC) v2.0 - REFINADO
========================================================
Sistema centralizado y optimizado para imports del ITC Engine

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
Versión: v2.0 - Quirúrgico

CARACTERÍSTICAS v2.0:
- Imports precisos y optimizados
- Sin sobre-importación
- Carga bajo demanda
- Robustez ante errores
- Compatibilidad total
"""

# === LOGGING Y SISTEMA ===
try:
    from sistema.smart_directory_logger import logger, get_logger, setup_logging
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

# === DATA MANAGEMENT ===
try:
    from core.data_management.candle_downloader import CandleDownloader
except ImportError:
    CandleDownloader = None

try:
    from core.data_pipeline.enhanced_data_pipeline import DataPipeline
except ImportError:
    DataPipeline = None

try:
    from core.data_management.velas_manager import VelasManager
except ImportError:
    VelasManager = None

# === ICT ENGINE ===
try:
    from core.ict_engine.ict_detector import ICTDetector
except ImportError:
    ICTDetector = None

try:
    from core.ict_engine.ict_analyzer import ICTAnalyzer
except ImportError:
    ICTAnalyzer = None

try:
    from core.ict_engine.concepts.fair_value_gap import FairValueGap
except ImportError:
    FairValueGap = None

try:
    from core.ict_engine.concepts.order_block import OrderBlock
except ImportError:
    OrderBlock = None

try:
    from core.ict_engine.concepts.liquidity_pool import LiquidityPool
except ImportError:
    LiquidityPool = None

# === POI SYSTEM ===
try:
    from core.poi_system.poi_manager import POISystem, POIManager
except ImportError:
    POISystem = None
    POIManager = None

try:
    from core.poi_system.poi_detector import POIDetector
except ImportError:
    POIDetector = None

try:
    from core.poi_system.poi_analyzer import POIAnalyzer
except ImportError:
    POIAnalyzer = None

# === ANALYTICS ===
try:
    from core.analytics.analytics_engine import AnalyticsEngine
except ImportError:
    AnalyticsEngine = None

try:
    from core.analytics.performance_analyzer import PerformanceAnalyzer
except ImportError:
    PerformanceAnalyzer = None

try:
    from core.analytics.market_analyzer import MarketAnalyzer
except ImportError:
    MarketAnalyzer = None

# === TRADING ===
try:
    from core.trading import TradingEngine
except ImportError:
    TradingEngine = None

try:
    from core.smart_trading_logger import SmartTradingLogger
except ImportError:
    SmartTradingLogger = None

try:
    from core.limit_order_manager import LimitOrderManager
except ImportError:
    LimitOrderManager = None

# === RISK MANAGEMENT ===
try:
    from core.risk_management.risk_manager import RiskManager
except ImportError:
    RiskManager = None

try:
    from core.risk_management.position_sizer import PositionSizer
except ImportError:
    PositionSizer = None

# === DASHBOARD Y UI ===
try:
    from dashboard.dashboard_controller import DashboardController
except ImportError:
    DashboardController = None

try:
    from dashboard.poi_dashboard_integration import POIDashboardIntegration
except ImportError:
    POIDashboardIntegration = None

# === CONFIGURACIÓN ===
try:
    from config.config_manager import ConfigManager
except ImportError:
    ConfigManager = None

try:
    from config.live_account_validator import LiveAccountValidator
except ImportError:
    LiveAccountValidator = None

# === SISTEMA ===
try:
    from sistema.market_status_detector_v3 import MarketStatusDetector
except ImportError:
    MarketStatusDetector = None

try:
    from sistema.trading_schedule import TradingSchedule
except ImportError:
    TradingSchedule = None

try:
    from sistema.system_monitor import SystemMonitor
except ImportError:
    SystemMonitor = None

# === INTEGRATIONS ===
try:
    from core.integrations.mt5_manager import MT5Manager
except ImportError:
    MT5Manager = None

try:
    from core.integrations.telegram_bot import TelegramBot
except ImportError:
    TelegramBot = None

# === ANALYSIS COMMAND CENTER ===
try:
    from core.analysis_command_center.tct_pipeline.tct_interface import TCTInterface
except ImportError:
    TCTInterface = None

try:
    from core.analysis_command_center.command_center import AnalysisCommandCenter
except ImportError:
    AnalysisCommandCenter = None

# === FUNCIONES DE UTILIDAD ===
def get_available_components():
    """📊 Obtener componentes disponibles en SIC"""
    components = {}

    for name, obj in globals().items():
        if not name.startswith('_') and obj is not None and name != 'get_available_components':
            components[name] = obj

    return components

def sic_status():
    """📊 Estado del Sistema SIC"""
    components = get_available_components()
    total = len([name for name in globals() if not name.startswith('_')])
    available = len(components)

    return {
        'version': 'v2.0-Quirúrgico',
        'total_components': total,
        'available_components': available,
        'success_rate': round((available / total) * 100, 2) if total > 0 else 0,
        'components': list(components.keys())
    }

# === LOG DE INICIALIZACIÓN ===
if logger:
    try:
        status = sic_status()
        logger.info(f"🎯 SIC v2.0 inicializado - {status['available_components']}/{status['total_components']} componentes ({status['success_rate']}%)")
    except:
        pass  # Silenciar errores de logging durante importación
