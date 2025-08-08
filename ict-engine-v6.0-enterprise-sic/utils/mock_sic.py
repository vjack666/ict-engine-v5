#!/usr/bin/env python3
"""
🎯 MOCK SISTEMA SIC PARA COMPATIBILIDAD
======================================

Mock del sistema.sic para permitir que el POIDetector funcione
sin depender de todo el sistema SIC completo.
"""

from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
import json
from pathlib import Path

def enviar_senal_log(level: str, message: str, module: str, categoria: str = "general"):
    """Mock de enviar_senal_log"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {categoria}.{module}: {message}")

def log_poi(level: str, message: str, module: str):
    """Mock de log_poi"""
    timestamp = datetime.now().strftime("%H:%M:%S") 
    print(f"[{timestamp}] [POI.{level}] {module}: {message}")

# Exportar las funciones
__all__ = ['enviar_senal_log', 'log_poi', 'List', 'Dict', 'Optional', 'Tuple', 'Any', 'datetime', 'json', 'Path']
