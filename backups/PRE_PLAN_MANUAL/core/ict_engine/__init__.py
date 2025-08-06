"""
ICT Engine - Motor Consolidado de Análisis ICT
==============================================
Motor unificado para todo el análisis Inner Circle Trader.
"""

from sistema.logging_interface import enviar_senal_log

# Importar clase principal ICTEngine
try:
    from .ict_engine import ICTEngine, get_ict_engine, ICTEngineResult
    # ICT Engine cargado exitosamente
except ImportError:
    # Error al cargar ICT Engine - modo degradado
    pass

__version__ = "3.4.1"  # Versión actualizada tras refactorización

# --- Importar componentes clave desde los submódulos ---
try:
    from .ict_types import (
        ICTPattern, MarketPhase, SessionType, SignalStrength, TradingDirection,
        ICTSignal, MarketStructure, SessionCharacteristics, ICTAnalysisResult,
        PATTERN_EMOJIS, DIRECTION_COLORS, get_pattern_description
    )
    from .ict_detector import MarketContext, OptimizedICTAnalysis, ICTDetector, update_market_context
    enviar_senal_log("INFO", "Componentes ICT importados correctamente", __name__, "ict")
except ImportError as e:
    enviar_senal_log("WARNING", f"Error importando componentes ICT: {e}", __name__, "ict")
from .pattern_analyzer import ICTPatternAnalyzer
from .confidence_engine import ConfidenceEngine

# Manejo de errores tipo 'caja negra' para importación de VeredictoEngine
try:
    from .veredicto_engine_v4 import VeredictoEngine
except Exception as e:
    try:
        enviar_senal_log("ERROR", f"Error importando VeredictoEngine: {e}", __name__, "ict")
    except ImportError:
        enviar_senal_log("ERROR", f"ERROR: No se pudo importar VeredictoEngine: {e}", "__init__", "migration")
    VeredictoEngine = None
    try:
        enviar_senal_log("ERROR", "VeredictoEngine se asignó a None por fallo de importación.", __name__, "ict")
    except ImportError:
        enviar_senal_log("ERROR", "ERROR: VeredictoEngine se asignó a None por fallo de importación.", "__init__", "migration")

from .ict_historical_analyzer import ICTHistoricalAnalyzer

# --- Definir la API Pública del Paquete con __all__ ---
__all__ = [
    # Tipos y Enums
    'ICTPattern', 'MarketPhase', 'SessionType', 'SignalStrength', 'TradingDirection',
    'ICTSignal', 'MarketStructure', 'SessionCharacteristics', 'ICTAnalysisResult',
    'PATTERN_EMOJIS', 'DIRECTION_COLORS', 'get_pattern_description',

    # Clases Principales
    'MarketContext',
    'OptimizedICTAnalysis',
    'ICTDetector',  # ✅ NUEVO: Detector ICT real agregado
    'ICTPatternAnalyzer',
    'ConfidenceEngine',
    'VeredictoEngine',
    'ICTHistoricalAnalyzer',

    # Funciones de Conveniencia
    'update_market_context'
]

# Log de inicialización del paquete
try:
    enviar_senal_log("INFO", f"✅ Paquete 'core.ict_engine' v{__version__} cargado y API pública definida.", __name__, "ict")
except ImportError:
    enviar_senal_log("INFO", f"INFO: Paquete 'core.ict_engine' cargado.", "__init__", "migration")
