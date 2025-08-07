
"""
Dashboard Package - Sentinel Grid System v3.5.0
===============================================
Sistema de dashboard modular para el sistema Sentinel Grid.
Exporta las funciones principales para compatibilidad con app.py y main.py.
"""

from sistema.logging_interface import enviar_senal_log

# Funciones dummy para compatibilidad mientras se implementa el core
def crear_layout_inicial():
    """Función temporal de compatibilidad"""
    return None

def update_layout():
    """Función temporal de compatibilidad"""
    return None

def create_sleep_mode_layout():
    """Función temporal de compatibilidad"""
    return None

def update_sleep_mode_layout():
    """Función temporal de compatibilidad"""
    return None

# Exports para componentes ICT del dashboard
try:
    from core.ict_engine import ICTPattern, TradingDirection, SessionType, PATTERN_EMOJIS
    from core.ict_engine import ICTPatternAnalyzer
    from .ict_professional_widget import ICTProfessionalWidget
    from .dashboard_widgets import HibernationStatusWidget, CountdownWidget

    # Agregar a __all__
    __all__ = [
        'crear_layout_inicial',
        'update_layout',
        'create_sleep_mode_layout',
        'update_sleep_mode_layout',
        'ICTPattern',
        'TradingDirection',
        'SessionType',
        'PATTERN_EMOJIS',
        'ICTPatternAnalyzer',
        'ICTProfessionalWidget',
        'HibernationStatusWidget',
        'CountdownWidget'
    ]

except ImportError as e:
    enviar_senal_log("WARNING", f"⚠️ Warning: No se pudieron importar algunos componentes ICT: {e}", "__init__", "migration")

    # __all__ básico sin componentes ICT
    __all__ = [
        'crear_layout_inicial',
        'update_layout',
        'create_sleep_mode_layout',
        'update_sleep_mode_layout'
    ]

# Exportar componentes ICT de forma explícita - YA NO ES NECESARIO
# Los componentes ICT ahora están en core/ict_engine/
enviar_senal_log("INFO", "✅ ICT Engine consolidado en core/ict_engine/", "__init__", "migration")

__version__ = "3.5.0"
