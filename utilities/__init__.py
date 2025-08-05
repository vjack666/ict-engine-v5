# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log
# Utilities Package
# Herramientas y utilidades del proyecto

__version__ = "1.0.0"

from . import debug
from . import migration
from . import sprint

__all__ = ['debug', 'migration', 'sprint']
