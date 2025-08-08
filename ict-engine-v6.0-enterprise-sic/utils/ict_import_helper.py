#!/usr/bin/env python3
"""
🔧 HELPER DE IMPORTACIONES ICT v6.0
==================================

Módulo helper generado automáticamente para facilitar la importación
de todos los componentes ICT reales disponibles.

Uso:
    from ict_import_helper import *
    
    # Los componentes estarán disponibles automáticamente
    mt5_manager = get_mt5_manager()
    poi_detector = get_poi_detector()
    # etc.

Generado: {}
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

import sys
from pathlib import Path

# Configurar rutas automáticamente
base_path = Path(__file__).parent.parent.parent
paths_to_add = [
    str(base_path),
    str(base_path / "ict-engine-v6.0-enterprise-sic"),
    str(base_path / "proyecto principal"),
    # mt5_data_manager disponible en: utils.mt5_data_manager
]

for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)

# Importaciones automáticas de componentes disponibles
COMPONENTS_AVAILABLE = {}


# MT5_DATA_MANAGER
try:
    from utils.mt5_data_manager import *
    COMPONENTS_AVAILABLE['mt5_data_manager'] = True
    print(f"✅ mt5_data_manager: DISPONIBLE")
except ImportError as e:
    COMPONENTS_AVAILABLE['mt5_data_manager'] = False
    print(f"❌ mt5_data_manager: {e}")

# LOGGING_INTERFACE - No disponible
COMPONENTS_AVAILABLE['logging_interface'] = False

# POI_DETECTOR - No disponible
COMPONENTS_AVAILABLE['poi_detector'] = False

# POI_SCORING_ENGINE - No disponible
COMPONENTS_AVAILABLE['poi_scoring_engine'] = False

# ICT_DETECTOR - No disponible
COMPONENTS_AVAILABLE['ict_detector'] = False

# PATTERN_ANALYZER - No disponible
COMPONENTS_AVAILABLE['pattern_analyzer'] = False

# CONFIDENCE_ENGINE - No disponible
COMPONENTS_AVAILABLE['confidence_engine'] = False

# VEREDICTO_ENGINE - No disponible
COMPONENTS_AVAILABLE['veredicto_engine'] = False


def get_component_status():
    """Obtener estado de todos los componentes"""
    return COMPONENTS_AVAILABLE.copy()

def show_integration_status():
    """Mostrar estado de integración"""
    available = sum(1 for v in COMPONENTS_AVAILABLE.values() if v)
    total = len(COMPONENTS_AVAILABLE)
    
    print(f"\n🔧 ESTADO DE INTEGRACIÓN ICT v6.0")
    print(f"   Componentes disponibles: {available}/{total}")
    
    for component, status in COMPONENTS_AVAILABLE.items():
        icon = "✅" if status else "❌"
        print(f"   {icon} {component}")
    
    print(f"\n📊 Integración: {(available/total)*100:.1f}% completa")

if __name__ == "__main__":
    show_integration_status()
