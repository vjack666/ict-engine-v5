"""
POI System - Sistema Consolidado de Puntos de Interés
=====================================================
Sistema unificado para toda la lógica de POI (Points of Interest).
Centraliza la lógica que anteriormente estaba dispersa entre analisis/poi y utils/.

Componentes:
- poi_system.py: Clase principal POISystem
- poi_detector.py: Detector principal de POIs
- poi_utils.py: Utilidades POI (versión de utils/, más completa)
- poi_utils_analisis.py: Utilidades POI (versión de analisis/, backup)
"""

# Importar clase principal POISystem
try:
    from .poi_system import POISystem, get_poi_system, POIResult
    # POI System cargado exitosamente
except ImportError:
    # Error al cargar POI System - modo degradado
    pass

try:
    from .poi_detector import encontrar_pois_multiples_para_dashboard
    # POI Detector cargado exitosamente
except ImportError:
    # Error al cargar POI Detector - modo degradado
    pass

try:
    from .poi_utils import *
    # POI Utils cargado exitosamente
except ImportError:
    # Error al cargar POI Utils - modo degradado
    pass

__version__ = "1.0.0"
__all__ = ["POISystem", "get_poi_system", "POIResult", "encontrar_pois_multiples_para_dashboard"]
