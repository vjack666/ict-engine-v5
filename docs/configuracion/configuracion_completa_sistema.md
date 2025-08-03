# ⚙️ CONFIGURACIÓN COMPLETA - ICT ENGINE v5.0 INTEGRACIÓN
**Fecha:** 3 de Agosto 2025  
**Versión:** 5.0  
**Tipo:** Guía de Configuración Técnica  

---

## 🎯 CONFIGURACIÓN PRINCIPAL DEL SISTEMA

### **📂 Archivo: config/comprehensive_config.py**
```python
"""
Configuración maestra para ICT Engine v5.0
Integración completa: Candle Downloader + ICT + Fractales + Sesiones
"""

from datetime import time
from typing import Dict, List, Any

# =====================================
# CONFIGURACIÓN DE FUENTES DE DATOS
# =====================================

DATA_SOURCES_CONFIG = {
    "primary_source": "advanced_candle_downloader",
    "backup_sources": ["mt5_direct", "api_fallback"],
    
    "symbols": {
        "forex_majors": ["EURUSD", "GBPUSD", "USDJPY", "USDCHF"],
        "forex_minors": ["EURJPY", "GBPJPY", "EURGBP"],
        "active_symbols": ["EURUSD", "GBPUSD", "USDJPY"]  # Para iniciar
    },
    
    "timeframes": {
        "all_available": ["M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1"],
        "active_timeframes": ["M1", "M5", "M15", "H1", "H4", "D1"],
        "critical_timeframes": ["M5", "M15", "H1"]  # Para análisis principal
    },
    
    "update_intervals": {
        "M1": 5,      # Cada 5 segundos (tiempo real crítico)
        "M5": 30,     # Cada 30 segundos (importante)
        "M15": 60,    # Cada minuto (moderado)
        "H1": 300,    # Cada 5 minutos (relajado)
        "H4": 900,    # Cada 15 minutos (esporádico)
        "D1": 3600    # Cada hora (histórico)
    },
    
    "data_retention": {
        "memory_buffer_size": 1000,      # Velas en memoria por TF
        "historical_days": 30,           # Días de histórico
        "compression_threshold": 5000    # Velas antes de comprimir
    }
}

# =====================================
# CONFIGURACIÓN ANÁLISIS ICT
# =====================================

ICT_ANALYSIS_CONFIG = {
    "market_structure": {
        "bos_confirmation_candles": 3,
        "choch_confirmation_candles": 2,
        "structure_strength_threshold": 0.7,
        "multi_tf_confirmation": True,
        "higher_tf_bias_weight": 2.0
    },
    
    "fair_value_gaps": {
        "min_gap_size_pips": {
            "EURUSD": 5, "GBPUSD": 6, "USDJPY": 8, "default": 5
        },
        "max_gap_age_hours": 24,
        "displacement_strength_threshold": 0.8,
        "volume_confirmation_required": True,
        "session_context_weight": 0.3,
        "probability_calculation": {
            "session_multiplier": {"LONDON": 1.2, "NY": 1.5, "ASIAN": 0.8},
            "timeframe_weight": {"M15": 1.0, "H1": 1.3, "H4": 1.8}
        }
    },
    
    "order_blocks": {
        "min_reaction_pips": {
            "EURUSD": 15, "GBPUSD": 18, "USDJPY": 20, "default": 15
        },
        "volume_confirmation": True,
        "time_validity_hours": 48,
        "institutional_footprint_analysis": True,
        "confirmation_strength_calculation": {
            "volume_weight": 0.4,
            "price_action_weight": 0.3,
            "time_context_weight": 0.3
        }
    },
    
    "liquidity_levels": {
        "equal_highs_lows_tolerance_pips": {
            "EURUSD": 3, "GBPUSD": 4, "USDJPY": 5, "default": 3
        },
        "minimum_touches": 2,
        "strength_calculation": "volume_weighted",
        "hunt_detection": {
            "enabled": True,
            "max_hunt_distance_pips": 10,
            "reversal_confirmation_candles": 2
        }
    },
    
    "candle_range_theory": {
        "applicable_timeframes": ["H4", "D1", "W1"],
        "equilibrium_calculation": "midpoint",
        "premium_discount_zones": {
            "premium_threshold": 0.618,  # Fibonacci
            "discount_threshold": 0.382
        },
        "institutional_bias_indicators": [
            "opening_gap", "range_extension", "rejection_candles"
        ]
    },
    
    "session_analysis": {
        "timezone": "GMT",
        "kill_zones": {
            "london_open": {
                "start": "08:00", "end": "09:00", 
                "priority": "HIGH", "weight": 0.8
            },
            "london_close": {
                "start": "15:00", "end": "16:00",
                "priority": "MEDIUM", "weight": 0.5
            },
            "ny_open": {
                "start": "13:30", "end": "14:30",
                "priority": "VERY_HIGH", "weight": 1.0
            },
            "ny_lunch": {
                "start": "17:00", "end": "18:00",
                "priority": "LOW", "weight": 0.3
            },
            "silver_bullet": {
                "start": "10:00", "end": "11:00",
                "priority": "HIGH", "weight": 0.9
            },
            "power_of_three": {
                "start": "13:30", "end": "15:00",
                "priority": "HIGH", "weight": 0.85
            }
        },
        "session_characteristics": {
            "ASIAN": {
                "volatility": "LOW",
                "typical_range_pips": {"EURUSD": 30, "GBPUSD": 40},
                "recommended_strategies": ["RANGE_TRADING", "ACCUMULATION"]
            },
            "LONDON": {
                "volatility": "HIGH", 
                "typical_range_pips": {"EURUSD": 80, "GBPUSD": 120},
                "recommended_strategies": ["TREND_FOLLOWING", "BREAKOUTS"]
            },
            "NEW_YORK": {
                "volatility": "VERY_HIGH",
                "typical_range_pips": {"EURUSD": 100, "GBPUSD": 150},
                "recommended_strategies": ["MOMENTUM", "INSTITUTIONAL_FLOW"]
            }
        }
    }
}

# =====================================
# CONFIGURACIÓN DE FRACTALES
# =====================================

FRACTAL_ANALYSIS_CONFIG = {
    "williams_fractals": {
        "confirmation_candles": 2,
        "min_strength_threshold": {
            "M1": 5, "M5": 8, "M15": 12, 
            "H1": 15, "H4": 20, "D1": 25
        },
        "confluence_weight": 0.3,
        "invalidation_distance_pips": {
            "EURUSD": 5, "GBPUSD": 6, "USDJPY": 8
        }
    },
    
    "zigzag_filter": {
        "min_change_percentage": {
            "M1": 0.3, "M5": 0.5, "M15": 0.8,
            "H1": 1.0, "H4": 1.5, "D1": 2.0
        },
        "noise_reduction": True,
        "adaptive_threshold": True,
        "dynamic_adjustment": {
            "volatility_based": True,
            "session_based": True,
            "market_condition_based": True
        }
    },
    
    "multi_timeframe": {
        "alignment_analysis": True,
        "higher_tf_weight": 2.0,
        "alignment_bonus_multiplier": 1.5,
        "max_timeframes_analysis": 3,
        "timeframe_combinations": [
            ["M15", "H1", "H4"],
            ["M5", "M15", "H1"],
            ["H1", "H4", "D1"]
        ]
    },
    
    "trading_signals": {
        "fractal_reversal": {
            "min_confidence_score": 70,
            "required_confluences": 3,
            "stop_loss_calculation": "nearest_opposing_fractal",
            "take_profit_multiplier": 2.0
        },
        "fractal_break": {
            "confirmation_candles": 1,
            "momentum_threshold": 0.6,
            "continuation_probability": 0.75
        }
    },
    
    "confluence_factors": {
        "ict_level_proximity": {
            "weight": 0.4,
            "max_distance_pips": 10
        },
        "session_timing": {
            "weight": 0.3,
            "kill_zone_bonus": 0.2
        },
        "volume_confirmation": {
            "weight": 0.3,
            "min_volume_ratio": 1.2
        }
    }
}

# =====================================
# CONFIGURACIÓN POI ENRIQUECIDO
# =====================================

POI_ENHANCED_CONFIG = {
    "detection_thresholds": {
        "min_strength": 60.0,
        "confluence_requirement": 5.0,
        "time_validity_hours": 72,
        "max_active_pois": 50
    },
    
    "enrichment_weights": {
        "ict_context_weight": 0.4,
        "fractal_context_weight": 0.3,
        "session_context_weight": 0.3
    },
    
    "ict_integration": {
        "fvg_proximity_bonus": 2.0,
        "order_block_confluence_bonus": 1.5,
        "liquidity_level_bonus": 1.8,
        "session_timing_multiplier": {
            "KILL_ZONE": 1.5,
            "NORMAL_TIME": 1.0,
            "LOW_ACTIVITY": 0.7
        }
    },
    
    "fractal_integration": {
        "fractal_confluence_bonus": 1.3,
        "swing_point_alignment_bonus": 1.4,
        "multi_tf_fractal_bonus": 1.6
    },
    
    "narrative_generation": {
        "enabled": True,
        "include_probabilities": True,
        "include_risk_assessment": True,
        "include_recommended_actions": True
    },
    
    "quality_scoring": {
        "base_score": 5.0,
        "max_score": 10.0,
        "confluence_bonus_per_factor": 0.5,
        "session_timing_bonus": 1.0,
        "institutional_context_bonus": 1.5
    }
}

# =====================================
# CONFIGURACIÓN DE RIESGO
# =====================================

RISK_MANAGEMENT_CONFIG = {
    "base_settings": {
        "base_risk_per_trade": 0.02,        # 2% por trade
        "max_risk_per_day": 0.06,           # 6% máximo diario
        "max_concurrent_trades": 3,
        "max_correlation_exposure": 0.8      # 80% correlación máxima
    },
    
    "session_multipliers": {
        "ASIAN": 0.5,                       # Reducir riesgo 50%
        "LONDON": 1.0,                      # Riesgo normal
        "NEW_YORK": 1.2,                    # Aumentar 20%
        "LONDON_NY_OVERLAP": 1.5            # Aumentar 50%
    },
    
    "confluence_multipliers": {
        "LOW": 0.5,        # < 5 puntos confluencia
        "MEDIUM": 1.0,      # 5-7 puntos
        "HIGH": 1.5,        # 7-8 puntos  
        "EXTREME": 2.0      # > 8 puntos
    },
    
    "volatility_adjustments": {
        "LOW": 1.2,         # Aumentar en baja volatilidad
        "NORMAL": 1.0,      # Sin ajuste
        "HIGH": 0.8,        # Reducir en alta volatilidad
        "EXTREME": 0.5      # Reducir significativamente
    },
    
    "stop_loss_settings": {
        "use_fractal_stops": True,
        "min_stop_pips": {"EURUSD": 10, "GBPUSD": 12, "USDJPY": 15},
        "max_stop_pips": {"EURUSD": 100, "GBPUSD": 120, "USDJPY": 150},
        "atr_multiplier": 1.5,
        "dynamic_adjustment": True
    },
    
    "position_sizing": {
        "calculation_method": "fixed_fractional",
        "account_balance_percentage": True,
        "kelly_criterion": False,
        "martingale": False,
        "anti_martingale": True
    }
}

# =====================================
# CONFIGURACIÓN DE ALERTAS
# =====================================

ALERT_SYSTEM_CONFIG = {
    "enabled": True,
    "priorities": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
    
    "channels": {
        "dashboard": {"enabled": True, "all_priorities": True},
        "email": {"enabled": False, "min_priority": "HIGH"},
        "telegram": {"enabled": False, "min_priority": "MEDIUM"},
        "log_file": {"enabled": True, "all_priorities": True},
        "sound": {"enabled": True, "min_priority": "HIGH"}
    },
    
    "conditions": {
        "new_fvg": {
            "priority": "HIGH", 
            "enabled": True,
            "min_gap_size": 10,
            "session_filtering": True
        },
        "order_block_activation": {
            "priority": "MEDIUM",
            "enabled": True,
            "confirmation_required": True
        },
        "fractal_confluence": {
            "priority": "HIGH",
            "enabled": True,
            "min_confluence_score": 7
        },
        "kill_zone_entry": {
            "priority": "CRITICAL",
            "enabled": True,
            "immediate_notification": True
        },
        "high_confluence_poi": {
            "priority": "HIGH",
            "enabled": True,
            "min_poi_score": 8.0
        },
        "structure_break": {
            "priority": "CRITICAL",
            "enabled": True,
            "multi_tf_confirmation": True
        }
    },
    
    "rate_limiting": {
        "max_alerts_per_minute": 10,
        "duplicate_suppression_seconds": 30,
        "priority_override": {"CRITICAL": True}
    }
}

# =====================================
# CONFIGURACIÓN DE LOGGING
# =====================================

LOGGING_CONFIG = {
    "level": "INFO",
    "format": "structured",
    "enable_emoji": True,
    "enable_colors": True,
    
    "files": {
        "system": {
            "path": "logs/system.log",
            "level": "INFO",
            "max_size": "10MB",
            "backup_count": 5
        },
        "trading": {
            "path": "logs/trading.log", 
            "level": "INFO",
            "max_size": "50MB",
            "backup_count": 10
        },
        "errors": {
            "path": "logs/errors.log",
            "level": "ERROR", 
            "max_size": "20MB",
            "backup_count": 7
        },
        "performance": {
            "path": "logs/performance.log",
            "level": "DEBUG",
            "max_size": "30MB", 
            "backup_count": 3
        },
        "analysis": {
            "path": "logs/analysis.log",
            "level": "INFO",
            "max_size": "100MB",
            "backup_count": 15
        }
    },
    
    "rotation": {
        "interval": "daily",
        "when": "midnight",
        "utc": True
    },
    
    "structured_data": {
        "include_timestamp": True,
        "include_thread_id": True,
        "include_process_id": True,
        "include_module": True,
        "include_function": True
    }
}

# =====================================
# CONFIGURACIÓN DE RENDIMIENTO
# =====================================

PERFORMANCE_CONFIG = {
    "monitoring": {
        "enable_profiling": False,
        "memory_tracking": True,
        "cpu_tracking": True,
        "io_tracking": True,
        "network_tracking": True
    },
    
    "optimization": {
        "cache_size": 1000,
        "parallel_processing": True,
        "max_workers": 4,
        "memory_optimization": True,
        "cpu_optimization": True,
        "lazy_loading": True,
        "data_compression": True
    },
    
    "limits": {
        "max_memory_usage_mb": 512,
        "max_cpu_usage_percent": 25,
        "max_processing_time_ms": 500,
        "max_queue_size": 1000,
        "connection_timeout_seconds": 30
    },
    
    "targets": {
        "processing_time_per_analysis": 500,    # milliseconds
        "data_distribution_time": 100,          # milliseconds
        "alert_generation_time": 50,            # milliseconds
        "ui_update_time": 200,                  # milliseconds
        "uptime_percentage": 99.9
    }
}

# =====================================
# CONFIGURACIÓN DE DESARROLLO
# =====================================

DEVELOPMENT_CONFIG = {
    "debug_mode": False,
    "test_mode": False,
    "mock_data": False,
    "verbose_logging": False,
    
    "testing": {
        "unit_tests": True,
        "integration_tests": True,
        "performance_tests": True,
        "stress_tests": False,
        "mock_trading": True
    },
    
    "development_tools": {
        "hot_reload": False,
        "debug_dashboard": False,
        "performance_profiler": False,
        "memory_profiler": False
    }
}

# =====================================
# CONFIGURACIÓN MAESTRA
# =====================================

COMPREHENSIVE_CONFIG = {
    "data_sources": DATA_SOURCES_CONFIG,
    "ict_analysis": ICT_ANALYSIS_CONFIG,
    "fractal_analysis": FRACTAL_ANALYSIS_CONFIG,
    "poi_enhanced": POI_ENHANCED_CONFIG,
    "risk_management": RISK_MANAGEMENT_CONFIG,
    "alert_system": ALERT_SYSTEM_CONFIG,
    "logging": LOGGING_CONFIG,
    "performance": PERFORMANCE_CONFIG,
    "development": DEVELOPMENT_CONFIG
}

# =====================================
# FUNCIONES DE CONFIGURACIÓN
# =====================================

def get_config(section: str = None) -> Dict[str, Any]:
    """
    Obtiene configuración completa o por sección
    
    Args:
        section: Sección específica (opcional)
        
    Returns:
        Diccionario de configuración
    """
    if section:
        return COMPREHENSIVE_CONFIG.get(section, {})
    return COMPREHENSIVE_CONFIG

def update_config(section: str, updates: Dict[str, Any]) -> bool:
    """
    Actualiza configuración específica
    
    Args:
        section: Sección a actualizar
        updates: Nuevos valores
        
    Returns:
        True si actualización exitosa
    """
    if section in COMPREHENSIVE_CONFIG:
        COMPREHENSIVE_CONFIG[section].update(updates)
        return True
    return False

def validate_config() -> bool:
    """
    Valida configuración completa
    
    Returns:
        True si configuración válida
    """
    required_sections = [
        "data_sources", "ict_analysis", "fractal_analysis",
        "risk_management", "alert_system", "logging"
    ]
    
    for section in required_sections:
        if section not in COMPREHENSIVE_CONFIG:
            return False
    
    return True

# =====================================
# EXPORTAR CONFIGURACIÓN
# =====================================

__all__ = [
    'COMPREHENSIVE_CONFIG',
    'get_config', 
    'update_config',
    'validate_config'
]
```

---

## 🔧 PERFILES DE CONFIGURACIÓN ESPECIALIZADOS

### **📂 Archivo: config/trading_profiles.py**
```python
"""
Perfiles de trading especializados para diferentes estrategias
"""

# PERFIL CONSERVADOR
CONSERVATIVE_PROFILE = {
    "risk_per_trade": 0.01,              # 1% por trade
    "max_daily_risk": 0.03,              # 3% máximo diario
    "confluence_requirement": 7,          # Alta confluencia requerida
    "session_preference": ["LONDON", "NY_OVERLAP"],
    "timeframes": ["H1", "H4", "D1"],    # Timeframes altos
    "stop_loss_tight": True,
    "take_profit_conservative": True
}

# PERFIL AGRESIVO
AGGRESSIVE_PROFILE = {
    "risk_per_trade": 0.03,              # 3% por trade
    "max_daily_risk": 0.08,              # 8% máximo diario
    "confluence_requirement": 5,          # Confluencia moderada
    "session_preference": ["ALL"],
    "timeframes": ["M5", "M15", "H1"],   # Timeframes medios
    "stop_loss_tight": False,
    "take_profit_extended": True
}

# PERFIL SCALPING
SCALPING_PROFILE = {
    "risk_per_trade": 0.005,             # 0.5% por trade
    "max_daily_risk": 0.05,              # 5% máximo diario
    "confluence_requirement": 4,          # Confluencia baja
    "session_preference": ["LONDON", "NEW_YORK"],
    "timeframes": ["M1", "M5"],          # Timeframes bajos
    "quick_exits": True,
    "high_frequency": True
}

# PERFIL SWING TRADING
SWING_PROFILE = {
    "risk_per_trade": 0.02,              # 2% por trade
    "max_daily_risk": 0.04,              # 4% máximo diario
    "confluence_requirement": 8,          # Muy alta confluencia
    "session_preference": ["LONDON_OPEN", "NY_OPEN"],
    "timeframes": ["H4", "D1"],          # Timeframes altos
    "hold_duration_hours": 48,
    "trend_following": True
}
```

---

## 📋 CHECKLIST DE CONFIGURACIÓN

### **✅ Configuración Básica**
- [ ] Configurar símbolos activos
- [ ] Establecer timeframes de trabajo
- [ ] Definir intervalos de actualización
- [ ] Configurar fuentes de datos

### **⚙️ Configuración ICT**
- [ ] Ajustar umbrales de Fair Value Gaps
- [ ] Configurar detección de Order Blocks
- [ ] Establecer Kill Zones por sesión
- [ ] Calibrar análisis de estructura

### **📊 Configuración Fractales**
- [ ] Establecer umbrales de fuerza por TF
- [ ] Configurar filtrado ZigZag
- [ ] Ajustar confluencia multi-timeframe
- [ ] Calibrar generación de señales

### **🛡️ Configuración de Riesgo**
- [ ] Establecer riesgo base por trade
- [ ] Configurar multiplicadores por sesión
- [ ] Ajustar stops dinámicos
- [ ] Calibrar position sizing

### **🔔 Configuración de Alertas**
- [ ] Habilitar canales de notificación
- [ ] Establecer prioridades
- [ ] Configurar condiciones de alerta
- [ ] Ajustar rate limiting

---

**📅 Fecha de Configuración:** 3 de Agosto 2025  
**⚙️ Configurado por:** ICT Engine v5.0 Team  
**🎯 Estado:** READY FOR IMPLEMENTATION**

---

**Sistema ICT Engine v5.0 - Configuración Completa**  
*"Configuración inteligente para trading institucional"*
