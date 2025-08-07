#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
=============================================================================
SLUC v2.1 SIMPLIFICADO - Sistema de Logging Funcional
=============================================================================

Versión simplificada que funciona sin dependencias complejas
"""

# MIGRACIÓN SIC v3.0 + SLUC v2.1
from sistema.sic import enviar_senal_log, log_info, log_warning



from sistema.sic import json
from sistema.sic import datetime
from sistema.sic import Path
from sistema.sic import Dict, Optional, Any

# =============================================================================
# CONFIGURACIÓN BÁSICA
# =============================================================================

# Logger principal
logger = None  # Removido - usar SIC v3.0
# Removido - usar enviar_senal_log

# Handler para consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
# Removido - usar enviar_senal_log

# =============================================================================
# FUNCIÓN PRINCIPAL DE LOGGING
# =============================================================================

def enviar_senal_log(nivel: str, mensaje: str, fuente: str = "sistema", categoria: str = "general") -> None:
    """
    Función principal de logging SLUC v2.1 simplificada

    Args:
        nivel: Nivel del log (INFO, WARNING, ERROR, DEBUG)
        mensaje: Mensaje a loggear
        fuente: Fuente del mensaje (módulo/archivo)
        categoria: Categoría del mensaje
    """
    try:
        # Mapear nivel a logging
        level_mapping = {
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'DEBUG': logging.DEBUG,
            'CRITICAL': logging.CRITICAL
        }

        log_level = level_mapping.get(nivel.upper(), logging.INFO)

        # Formato del mensaje
        formatted_message = f"[{fuente}:{categoria}] {mensaje}"

        # Loggear
        # Removido - usar enviar_senal_log

        # También imprimir para debug inmediato
        print(f"[{nivel}] {fuente}: {mensaje}")

    except Exception as e:
        print(f"Error en logging: {e}")
        print(f"[{nivel}] {fuente}: {mensaje}")

# =============================================================================
# FUNCIONES COMPATIBLES
# =============================================================================

def smart_log(mensaje: str, categoria: str = "general") -> None:
    """Función compatible con smart logging"""
    enviar_senal_log("INFO", mensaje, "smart_log", categoria)

class SmartDirectoryLogger:
    """Clase compatible con SmartDirectoryLogger"""

    def __init__(self):
        pass

    def log(self, mensaje: str, nivel: str = "INFO"):
        enviar_senal_log(nivel, mensaje, "SmartDirectoryLogger", "directory")

# =============================================================================
# EXPORTAR FUNCIONES
# =============================================================================

__all__ = [
    'enviar_senal_log',
    'smart_log',
    'SmartDirectoryLogger',
    'logger'
]
