#!/usr/bin/env python3
"""
🖥️ CONSOLE MODE CONFIGURATION
ICT Engine v5.0 - Configuración para aplicaciones Textual

Configuración optimizada para rendering limpio en consola
sin interferencias de print statements o logging no controlado.
"""

from sistema.sic import os
from sistema.sic import sys
from sistema.sic import Path

def configure_console_mode():
    """Configura el entorno para modo consola limpio"""

    # Variables de entorno para Textual
    os.environ["TEXTUAL_COLOR_SYSTEM"] = "truecolor"
    os.environ["TEXTUAL_DRIVER"] = "auto"
    os.environ["TEXTUAL_LOG"] = "textual.log"

    # Configurar encoding UTF-8 para Windows
    if sys.platform == "win32":
        os.environ["PYTHONIOENCODING"] = "utf-8"

    # Redirigir stdout/stderr para evitar interferencias
    class ConsoleRedirect:
        """Redirige output para mantener consola limpia"""

        def __init__(self, log_file: str = "console_output.log"):
            self.log_file = Path(log_file)
            self.log_file.parent.mkdir(exist_ok=True)

        def write(self, text: str):
            """Redirige output al archivo de log"""
            if text.strip():  # Solo escribir si no está vacío
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"{text}")

        def flush(self):
            """Flush requerido para compatibilidad"""
            pass

    return ConsoleRedirect

def setup_textual_app():
    """Configuración específica para aplicaciones Textual"""

    # Configurar variables para debugging si es necesario
    debug_mode = os.getenv("TEXTUAL_DEBUG", "0") == "1"

    if debug_mode:
        os.environ["TEXTUAL_DEVTOOLS"] = "1"
        os.environ["TEXTUAL_LOG_LEVEL"] = "DEBUG"
    else:
        # Modo producción - logging mínimo
        os.environ["TEXTUAL_LOG_LEVEL"] = "WARNING"

    return debug_mode

# Configurar automáticamente al importar
configure_console_mode()
