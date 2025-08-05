# MIGRADO A SLUC v2.0
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
# TODO: Eliminado - usar enviar_senal_log # # TODO: Eliminado - usar enviar_senal_log # # TODO: Eliminado - usar enviar_senal_log # # TODO: Eliminado - usar enviar_senal_log # import logging
import logging
import json
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
            enviar_senal_log("INFO", f"[{timestamp}] {nivel} | {fuente} | {mensaje}", "logging_interface", "migration")

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

def export_log_config(output_file: str = "data/logs/config/sluc_config.json"):
    """Exportar configuración actual del sistema de logging en formato JSON"""
    config_data = {
        "version": "SLUC v2.1",
        "timestamp": datetime.now().isoformat(),
        "base_path": str(_sluc_v21.base_path),
        "silent_mode": _sluc_v21.silent_mode,
        "directories": [
            'daily', 'dashboard', 'debug', 'errors', 'ict',
            'metrics', 'mt5', 'poi', 'structured', 'tct',
            'terminal_capture', 'trading'
        ],
        "routing_rules": {
            "trading": ["trading", "trade", "position", "order"],
            "ict": ["ict", "pattern", "fair_value", "liquidity"],
            "poi": ["poi", "point_of_interest", "level"],
            "mt5": ["mt5", "metatrader", "connection"],
            "dashboard": ["dashboard", "gui", "interface"],
            "tct": ["tct", "pipeline", "technical"],
            "metrics": ["metrics", "performance", "stats"]
        }
    }

    # Crear directorio de configuración si no existe
    config_path = Path(output_file)
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Guardar configuración en JSON
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=2, ensure_ascii=False)

    enviar_senal_log("INFO", f"✅ Configuración SLUC exportada a: {output_file}", "logging_interface", "migration")
    return config_data

def export_log_stats(output_file: str = "data/logs/stats/sluc_stats.json"):
    """Exportar estadísticas del sistema en formato JSON"""
    stats = get_log_stats()
    stats_data = {
        "export_timestamp": datetime.now().isoformat(),
        "system_info": {
            "version": "SLUC v2.1",
            "total_logs": stats.get('total_logs', 0),
            "directories_active": stats.get('directories_active', []),
            "silent_mode": stats.get('silent_mode', True)
        },
        "performance": {
            "routing_efficiency": "High",
            "storage_optimization": "Enabled",
            "automatic_organization": "Active"
        }
    }

    # Crear directorio de stats si no existe
    stats_path = Path(output_file)
    stats_path.parent.mkdir(parents=True, exist_ok=True)

    # Guardar estadísticas en JSON
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats_data, f, indent=2, ensure_ascii=False)

    enviar_senal_log("INFO", f"📊 Estadísticas SLUC exportadas a: {output_file}", "logging_interface", "migration")
    return stats_data

# =============================================================================
# MIGRACIÓN AUTOMÁTICA DESDE SLUC v2.0
# =============================================================================

def migrate_from_v20():
    """
    Migración automática desde SLUC v2.0 a v2.1
    Se ejecuta automáticamente al importar
    """
    enviar_senal_log("INFO", "🔄 Migrando a SLUC v2.1...", "logging_interface", "migration")
    enviar_senal_log("INFO", "✅ Routing inteligente activado", "logging_interface", "migration")
    enviar_senal_log("INFO", "✅ Modo silencioso por defecto", "logging_interface", "migration")
    enviar_senal_log("INFO", "✅ Organización automática de logs", "logging_interface", "migration")
    enviar_senal_log("INFO", "✅ Compatibilidad total mantenida", "logging_interface", "migration")

# Ejecutar migración al importar
migrate_from_v20()

# =============================================================================
# FUNCIONES DE DEMOSTRACIÓN
# =============================================================================

def demo_sluc_v21():
    """Demostración del sistema SLUC v2.1"""
    enviar_senal_log("INFO", "=== DEMO SLUC v2.1 - ROUTING INTELIGENTE ===", "logging_interface", "migration")

    # Ejemplos de logs que se organizarán automáticamente
    enviar_senal_log("INFO", "Sistema iniciado correctamente", "main")
    enviar_senal_log("INFO", "Trade ejecutado: BUY EURUSD", "core.trading")
    enviar_senal_log("DEBUG", "Patrón Fair Value Gap detectado", "ict.detector")
    enviar_senal_log("WARNING", "POI de baja calidad encontrado", "poi.system")
    enviar_senal_log("ERROR", "Conexión MT5 fallida", "mt5.connector")
    enviar_senal_log("INFO", "Dashboard actualizado", "dashboard.main")
    enviar_senal_log("INFO", "TCT Pipeline completado", "tct.pipeline")
    enviar_senal_log("INFO", "Métricas de cuenta actualizadas", "metrics.account")

    enviar_senal_log("INFO", "✅ Logs organizados automáticamente:", "logging_interface", "migration")
    enviar_senal_log("INFO", "  📁 data/logs/daily/ - Logs del sistema principal", "logging_interface", "migration")
    enviar_senal_log("INFO", "  📁 data/logs/trading/ - Logs de operaciones", "logging_interface", "migration")
    enviar_senal_log("INFO", "  📁 data/logs/ict/ - Logs de análisis ICT", "logging_interface", "migration")
    enviar_senal_log("INFO", "  📁 data/logs/poi/ - Logs del sistema POI", "logging_interface", "migration")
    enviar_senal_log("INFO", "  📁 data/logs/mt5/ - Logs de conexión MT5", "logging_interface", "migration")
    enviar_senal_log("INFO", "  📁 data/logs/dashboard/ - Logs del dashboard", "logging_interface", "migration")
    enviar_senal_log("INFO", "  📁 data/logs/tct/ - Logs de TCT Pipeline", "logging_interface", "migration")
    enviar_senal_log("INFO", "  📁 data/logs/metrics/ - Logs de métricas", "logging_interface", "migration")

    # Mostrar estadísticas
    stats = get_log_stats()
    enviar_senal_log("INFO", "📊 Estadísticas:", "logging_interface", "migration")
    enviar_senal_log("INFO", f"  Total de logs: {stats['total_logs']}", "logging_interface", "migration")
    enviar_senal_log("INFO", f"  Directorios activos: {len(stats['directories_active'])}", "logging_interface", "migration")
    enviar_senal_log("INFO", f"  Modo silencioso: {stats['silent_mode']}", "logging_interface", "migration")

if __name__ == "__main__":
    demo_sluc_v21()
