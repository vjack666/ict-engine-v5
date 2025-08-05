# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log
"""
🚀 CONFIGURACIÓN LIVE-ONLY - SPRINT LIVE.1
=========================================

Configuración exclusiva para modo live, eliminando completamente el modo demo.
Sistema optimizado para trading en vivo con datos reales únicamente.

Autor: Sistema Sentinel Grid
Fecha: 2025-08-03
Versión: Live-Only v1.0
"""

from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime
import os

@dataclass
class LiveOnlyConfig:
    """Configuración exclusiva para modo live"""
    mode: str = "LIVE_ONLY"
    demo_mode: bool = False
    fallback_to_demo: bool = False
    live_validation_required: bool = True
    connection_timeout: int = 30
    retry_attempts: int = 3
    real_time_validation: bool = True

# === CONFIGURACIÓN MT5 LIVE EXCLUSIVA ===
MT5_LIVE_CONFIG = {
    "executable_path": "C:/Program Files/FundedNext MT5 Terminal/terminal64.exe",
    "mode": "LIVE_ONLY",
    "login_required": True,
    "account_validation": True,
    "connection_settings": {
        "timeout": 30,
        "retry_attempts": 3,
        "keep_alive_interval": 60,
        "reconnect_on_disconnect": True
    },
    "data_settings": {
        "real_time_only": True,
        "no_simulated_data": True,
        "validate_data_freshness": True,
        "max_data_age_seconds": 30
    },
    "trading_settings": {
        "live_execution_only": True,
        "paper_trading": False,
        "real_account_required": True,
        "position_validation": True
    }
}

# === CONFIGURACIÓN DE DATOS LIVE ===
LIVE_DATA_CONFIG = {
    "sources": {
        "primary": "MT5_LIVE",
        "backup": None,  # Sin backup a demo
        "fallback": None  # Sin fallback
    },
    "validation": {
        "real_time_check": True,
        "data_freshness_check": True,
        "connection_health_check": True,
        "account_type_validation": True
    },
    "optimization": {
        "low_latency_mode": True,
        "priority_processing": True,
        "cache_optimization": True,
        "memory_efficient": True
    },
    "symbols": [
        "EURUSD", "GBPUSD", "USDJPY", "USDCHF",
        "AUDUSD", "USDCAD", "NZDUSD", "EURJPY"
    ],
    "timeframes": ["M1", "M5", "M15", "H1", "H4", "D1"]
}

# === CONFIGURACIÓN DEL DASHBOARD LIVE ===
LIVE_DASHBOARD_CONFIG = {
    "mode": "LIVE_ONLY",
    "demo_widgets_enabled": False,
    "live_widgets_only": True,
    "real_time_updates": True,
    "widgets": {
        "hibernation": {
            "enabled": True,
            "live_monitoring": True,
            "connection_status": True,
            "account_validation": True
        },
        "ict_professional": {
            "enabled": True,
            "live_analysis": True,
            "real_time_patterns": True,
            "live_signals": True
        },
        "pattern_analysis": {
            "enabled": True,
            "live_pattern_detection": True,
            "real_time_scoring": True,
            "live_alerts": True
        },
        "analytics": {
            "enabled": True,
            "live_metrics": True,
            "real_time_performance": True,
            "live_risk_monitoring": True
        }
    },
    "alerts": {
        "connection_loss": True,
        "data_quality_issues": True,
        "live_signal_alerts": True,
        "risk_management_alerts": True
    }
}

# === CONFIGURACIÓN DE MONITOREO LIVE ===
LIVE_MONITORING_CONFIG = {
    "connection_monitor": {
        "enabled": True,
        "check_interval": 5,  # segundos
        "alert_on_disconnect": True,
        "auto_reconnect": True,
        "max_reconnect_attempts": 5
    },
    "data_monitor": {
        "enabled": True,
        "freshness_check": True,
        "integrity_validation": True,
        "latency_monitoring": True,
        "max_acceptable_latency": 2.0  # segundos
    },
    "health_monitor": {
        "enabled": True,
        "system_resources": True,
        "memory_usage": True,
        "cpu_usage": True,
        "network_status": True
    },
    "performance_monitor": {
        "enabled": True,
        "analysis_speed": True,
        "signal_generation_time": True,
        "data_processing_speed": True,
        "overall_system_performance": True
    }
}

# === CONFIGURACIÓN DE ALERTAS LIVE ===
LIVE_ALERTS_CONFIG = {
    "alert_levels": ["INFO", "WARNING", "ERROR", "CRITICAL"],
    "alert_channels": {
        "dashboard": True,
        "console": True,
        "log_file": True,
        "system_notifications": True
    },
    "alert_types": {
        "connection_issues": {
            "enabled": True,
            "level": "ERROR",
            "immediate_alert": True
        },
        "data_quality": {
            "enabled": True,
            "level": "WARNING",
            "threshold_based": True
        },
        "trading_signals": {
            "enabled": True,
            "level": "INFO",
            "real_time_delivery": True
        },
        "system_performance": {
            "enabled": True,
            "level": "WARNING",
            "monitoring_based": True
        }
    }
}

# === FUNCIONES DE VALIDACIÓN LIVE ===

def validate_live_mode() -> bool:
    """Valida que el sistema esté configurado correctamente para modo live"""
    try:
        # Verificar que MT5 está configurado para live
        if not MT5_LIVE_CONFIG.get("mode") == "LIVE_ONLY":
            return False

        # Verificar que no hay configuraciones de demo habilitadas
        if MT5_LIVE_CONFIG.get("paper_trading", False):
            return False

        # Verificar que la validación de cuenta real está habilitada
        if not MT5_LIVE_CONFIG.get("account_validation", False):
            return False

        return True
    except Exception:
        return False

def get_live_config() -> Dict[str, Any]:
    """Obtiene la configuración completa para modo live"""
    return {
        "mt5": MT5_LIVE_CONFIG,
        "data": LIVE_DATA_CONFIG,
        "dashboard": LIVE_DASHBOARD_CONFIG,
        "monitoring": LIVE_MONITORING_CONFIG,
        "alerts": LIVE_ALERTS_CONFIG,
        "validation": {
            "live_mode_validated": validate_live_mode(),
            "timestamp": datetime.now().isoformat(),
            "version": "Live-Only v1.0"
        }
    }

def is_demo_mode_disabled() -> bool:
    """Confirma que el modo demo está completamente deshabilitado"""
    config = get_live_config()
    return (
        not config["mt5"]["trading_settings"]["paper_trading"] and
        not config["dashboard"]["demo_widgets_enabled"] and
        config["data"]["sources"]["backup"] is None
    )

# === CONFIGURACIÓN DE ENTORNO ===
ENVIRONMENT_CONFIG = {
    "environment": "PRODUCTION",
    "debug_mode": False,
    "logging_level": "INFO",
    "performance_monitoring": True,
    "security_validation": True,
    "data_encryption": True,
    "audit_trail": True
}

# === EXPORTAR CONFIGURACIÓN PRINCIPAL ===
LIVE_ONLY_SYSTEM_CONFIG = {
    **get_live_config(),
    "environment": ENVIRONMENT_CONFIG,
    "system_info": {
        "name": "Sentinel ICT Analyzer",
        "version": "Live-Only v1.0",
        "mode": "PRODUCTION_LIVE",
        "created": datetime.now().isoformat(),
        "author": "Sistema Sentinel Grid"
    }
}

if __name__ == "__main__":
    print("🚀 CONFIGURACIÓN LIVE-ONLY CARGADA")
    print(f"✅ Modo Demo Deshabilitado: {is_demo_mode_disabled()}")
    print(f"✅ Validación Live: {validate_live_mode()}")
    print(f"✅ Configuración: {len(LIVE_ONLY_SYSTEM_CONFIG)} secciones")
