"""
POI System - Sistema Consolidado de Puntos de Interés
=====================================================
Sistema unificado para toda la lógica de POI (Points of Interest).
Centraliza la lógica que anteriormente estaba dispersa entre analisis/poi y utils/.

Componentes:
- poi_detector.py: Detector principal de POIs
- poi_utils.py: Utilidades POI (versión de utils/, más completa)
- poi_utils_analisis.py: Utilidades POI (versión de analisis/, backup)
- test_*.py: Tests del sistema POI
"""

# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log

try:
    from .poi_detector import encontrar_pois_multiples_para_dashboard
    enviar_senal_log("INFO", "poi_detector importado correctamente", __name__, "poi")
except ImportError as e:
    enviar_senal_log("ERROR", f"Error importando poi_detector: {e}", __name__, "poi")

try:
    from .poi_utils import *
    enviar_senal_log("INFO", "poi_utils importado correctamente", __name__, "poi")
except ImportError as e:
    enviar_senal_log("ERROR", f"Error importando poi_utils: {e}", __name__, "poi")

__version__ = "1.0.0"
__all__ = ["encontrar_pois_multiples_para_dashboard"]
