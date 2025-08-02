# Tests Package
# Contiene todos los tests del proyecto ICT Engine v5.0

__version__ = "1.0.0"
__author__ = "ICT Engine Team"

# Configuración de testing
import sys
import pytest
from pathlib import Path

# Añadir el directorio raíz del proyecto al path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
