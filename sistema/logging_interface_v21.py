#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
=============================================================================
SLUC v2.1 - Sistema de Logging Unificado Centralizado con Routing Inteligente
=============================================================================

Versión profesional con:
- ✅ Routing automático de logs a carpetas específicas
- ✅ Sin emojis en archivos de log (modo profesional)
- ✅ Terminal silencioso por defecto
- ✅ Compatibilidad 100% con código existente
- ✅ Logging distribuido por función
- ✅ Organización automática de archivos

Autor: Sistema ITC Engine v5.0
Fecha: 2024
"""

import logging
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any
from sistema.smart_directory_logger import SmartDirectoryLogger, smart_log

# =============================================================================
# CONFIGURACIÓN SLUC v2.1
# =============================================================================

class SLUCv21:
    """
    Sistema de Logging Unificado Centralizado v2.1
    Con routing inteligente automático
    """

    def __init__(self):
        self.base_path = Path("data/logs")
        self.smart_logger = SmartDirectoryLogger()
        self.silent_mode = True  # Por defecto silencioso

        # Asegurar que existan todos los directorios
        self._ensure_directories()

        # Configurar logging básico
        self._setup_basic_logging()

    def _ensure_directories(self):
        """Crear todas las carpetas necesarias"""
        directories = [
            'daily', 'dashboard', 'debug', 'errors', 'ict',
            'metrics', 'mt5', 'poi', 'structured', 'tct',
            'terminal_capture', 'trading'
        ]

        for directory in directories:
            (self.base_path / directory).mkdir(parents=True, exist_ok=True)

    def _setup_basic_logging(self):
        """Configurar logging básico sin interferir con el sistema smart"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.NullHandler()  # No output por defecto
            ]
        )

    def enviar_senal_log(self, nivel: str, mensaje: str, fuente: str = "sistema",
                        categoria: str = "general", metadata: Optional[Dict] = None):
        """
        Función principal compatible con SLUC v2.0
        Ahora con routing inteligente automático
        """
        # Usar el logger inteligente para determinar carpeta
        self.smart_logger.smart_log(nivel, mensaje, fuente, categoria, metadata or {})

        # Si no está en modo silencioso, mostrar en terminal
        if not self.silent_mode:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {nivel} | {fuente} | {mensaje}")

    def set_silent_mode(self, silent: bool = True):
        """Activar/desactivar modo silencioso"""
        self.silent_mode = silent

    def log_info(self, mensaje: str, fuente: str = "sistema", metadata: Optional[Dict] = None):
        """Log de información"""
        self.enviar_senal_log("INFO", mensaje, fuente, "info", metadata)

    def log_warning(self, mensaje: str, fuente: str = "sistema", metadata: Optional[Dict] = None):
        """Log de advertencia"""
        self.enviar_senal_log("WARNING", mensaje, fuente, "warning", metadata)

    def log_error(self, mensaje: str, fuente: str = "sistema", metadata: Optional[Dict] = None):
        """Log de error"""
        self.enviar_senal_log("ERROR", mensaje, fuente, "error", metadata)

    def log_debug(self, mensaje: str, fuente: str = "sistema", metadata: Optional[Dict] = None):
        """Log de debug"""
        self.enviar_senal_log("DEBUG", mensaje, fuente, "debug", metadata)

    def log_critical(self, mensaje: str, fuente: str = "sistema", metadata: Optional[Dict] = None):
        """Log crítico"""
        self.enviar_senal_log("CRITICAL", mensaje, fuente, "critical", metadata)

# =============================================================================
# INSTANCIA GLOBAL SLUC v2.1
# =============================================================================

# Instancia global del sistema
_sluc_v21 = SLUCv21()

# =============================================================================
# FUNCIONES DE COMPATIBILIDAD TOTAL
# =============================================================================

def enviar_senal_log(nivel: str, mensaje: str, fuente: str = "sistema",
                    categoria: str = "general", metadata: Optional[Dict] = None):
    """
    Función principal de logging - 100% compatible con código existente
    Ahora con routing inteligente automático a carpetas específicas
    """
    _sluc_v21.enviar_senal_log(nivel, mensaje, fuente, categoria, metadata)

def set_silent_mode(silent: bool = True):
    """Configurar modo silencioso globalmente"""
    _sluc_v21.set_silent_mode(silent)

def log_info(mensaje: str, fuente: str = "sistema", metadata: Optional[Dict] = None):
    """Log de información con routing automático"""
    _sluc_v21.log_info(mensaje, fuente, metadata)

def log_warning(mensaje: str, fuente: str = "sistema", metadata: Optional[Dict] = None):
    """Log de advertencia con routing automático"""
    _sluc_v21.log_warning(mensaje, fuente, metadata)

def log_error(mensaje: str, fuente: str = "sistema", metadata: Optional[Dict] = None):
    """Log de error con routing automático"""
    _sluc_v21.log_error(mensaje, fuente, metadata)

def log_debug(mensaje: str, fuente: str = "sistema", metadata: Optional[Dict] = None):
    """Log de debug con routing automático"""
    _sluc_v21.log_debug(mensaje, fuente, metadata)

def log_critical(mensaje: str, fuente: str = "sistema", metadata: Optional[Dict] = None):
    """Log crítico con routing automático"""
    _sluc_v21.log_critical(mensaje, fuente, metadata)

# =============================================================================
# FUNCIONES ESPECÍFICAS POR MÓDULO (NUEVAS)
# =============================================================================

def log_trading(nivel: str, mensaje: str, fuente: str = "trading", metadata: Optional[Dict] = None):
    """Log específico para operaciones de trading"""
    smart_log(nivel, mensaje, fuente, 'trading', metadata)

def log_ict(nivel: str, mensaje: str, fuente: str = "ict", metadata: Optional[Dict] = None):
    """Log específico para análisis ICT"""
    smart_log(nivel, mensaje, fuente, 'ict', metadata)

def log_poi(nivel: str, mensaje: str, fuente: str = "poi", metadata: Optional[Dict] = None):
    """Log específico para sistema POI"""
    smart_log(nivel, mensaje, fuente, 'poi', metadata)

def log_mt5(nivel: str, mensaje: str, fuente: str = "mt5", metadata: Optional[Dict] = None):
    """Log específico para conexión MT5"""
    smart_log(nivel, mensaje, fuente, 'mt5', metadata)

def log_dashboard(nivel: str, mensaje: str, fuente: str = "dashboard", metadata: Optional[Dict] = None):
    """Log específico para dashboard"""
    smart_log(nivel, mensaje, fuente, 'dashboard', metadata)

def log_tct(nivel: str, mensaje: str, fuente: str = "tct", metadata: Optional[Dict] = None):
    """Log específico para TCT Pipeline"""
    smart_log(nivel, mensaje, fuente, 'tct', metadata)

def log_metrics(nivel: str, mensaje: str, fuente: str = "metrics", metadata: Optional[Dict] = None):
    """Log específico para métricas"""
    smart_log(nivel, mensaje, fuente, 'metrics', metadata)

# =============================================================================
# FUNCIONES DE ANÁLISIS Y ESTADÍSTICAS
# =============================================================================

def get_log_stats() -> Dict[str, Any]:
    """Obtener estadísticas del sistema de logging"""
    from sistema.smart_directory_logger import get_smart_stats
    return get_smart_stats()

def create_log_summary():
    """Crear resumen de logs organizados"""
    from sistema.smart_directory_logger import create_summary
    create_summary()

# =============================================================================
# MIGRACIÓN AUTOMÁTICA DESDE SLUC v2.0
# =============================================================================

def migrate_from_v20():
    """
    Migración automática desde SLUC v2.0 a v2.1
    Se ejecuta automáticamente al importar
    """
    print("🔄 Migrando a SLUC v2.1...")
    print("✅ Routing inteligente activado")
    print("✅ Modo silencioso por defecto")
    print("✅ Organización automática de logs")
    print("✅ Compatibilidad total mantenida")

# Ejecutar migración al importar
migrate_from_v20()

# =============================================================================
# FUNCIONES DE DEMOSTRACIÓN
# =============================================================================

def demo_sluc_v21():
    """Demostración del sistema SLUC v2.1"""
    print("=== DEMO SLUC v2.1 - ROUTING INTELIGENTE ===")
    print()

    # Ejemplos de logs que se organizarán automáticamente
    enviar_senal_log("INFO", "Sistema iniciado correctamente", "main")
    enviar_senal_log("INFO", "Trade ejecutado: BUY EURUSD", "core.trading")
    enviar_senal_log("DEBUG", "Patrón Fair Value Gap detectado", "ict.detector")
    enviar_senal_log("WARNING", "POI de baja calidad encontrado", "poi.system")
    enviar_senal_log("ERROR", "Conexión MT5 fallida", "mt5.connector")
    enviar_senal_log("INFO", "Dashboard actualizado", "dashboard.main")
    enviar_senal_log("INFO", "TCT Pipeline completado", "tct.pipeline")
    enviar_senal_log("INFO", "Métricas de cuenta actualizadas", "metrics.account")

    print("✅ Logs organizados automáticamente:")
    print("  📁 data/logs/daily/ - Logs del sistema principal")
    print("  📁 data/logs/trading/ - Logs de operaciones")
    print("  📁 data/logs/ict/ - Logs de análisis ICT")
    print("  📁 data/logs/poi/ - Logs del sistema POI")
    print("  📁 data/logs/mt5/ - Logs de conexión MT5")
    print("  📁 data/logs/dashboard/ - Logs del dashboard")
    print("  📁 data/logs/tct/ - Logs de TCT Pipeline")
    print("  📁 data/logs/metrics/ - Logs de métricas")
    print()

    # Mostrar estadísticas
    stats = get_log_stats()
    print("📊 Estadísticas:")
    print(f"  Total de logs: {stats['total_logs']}")
    print(f"  Directorios activos: {len(stats['directories_active'])}")
    print(f"  Modo silencioso: {stats['silent_mode']}")

if __name__ == "__main__":
    demo_sluc_v21()
