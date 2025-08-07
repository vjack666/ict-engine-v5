# 🎯 POI LIFECYCLE - DOCUMENTACIÓN TÉCNICA

## 📋 **PROPÓSITO Y ALCANCE**

Esta carpeta almacena el ciclo de vida completo de los Points of Interest (POI) - desde su creación hasta su resolución o expiración. Los POIs son niveles clave donde el precio institucional tiene alta probabilidad de reaccionar.

## 🏗️ **ESTRUCTURA DE ARCHIVOS**

```
poi_lifecycle/
├── poi_lifecycle_2025-08-01.jsonl     # Eventos POI del día actual
├── poi_lifecycle_2025-07-31.jsonl     # Eventos POI del día anterior
├── README.md                           # Esta documentación
├── active_pois/
│   ├── active_pois_snapshot.json      # Snapshot de POIs activos
│   ├── poi_strength_evolution.json    # Evolución de fortaleza POI
│   └── poi_interaction_matrix.json    # Matriz de interacciones POI
├── historical/
│   ├── resolved_pois_monthly.json     # POIs resueltos por mes
│   ├── success_rate_analysis.json     # Análisis de tasa de éxito
│   └── poi_pattern_correlation.json   # Correlación POI-Patrones
└── analytics/
    ├── poi_performance_metrics.json   # Métricas de rendimiento POI
    ├── market_impact_analysis.json    # Análisis de impacto en mercado
    └── optimization_opportunities.json # Oportunidades de optimización
```

## 📊 **FORMATO DE DATOS (JSONL)**

### **Estructura base de cada línea:**
```json
{
    "timestamp": "2025-08-01T14:23:45.123456",
    "bitacora_type": "poi_lifecycle",
    "severity": "HIGH|MEDIUM|LOW|INFO",
    "component": "POI_DETECTOR|POI_SCORING|POI_MANAGER|POI_VALIDATOR",
    "event_id": "POI_CREATED|POI_UPDATED|POI_TESTED|POI_RESOLVED|POI_EXPIRED|POI_INVALIDATED",
    "description": "POI resistance level tested and holding strong",
    "poi_details": {
        "poi_id": "POI_EURUSD_RESISTANCE_1.0900_20250801",
        "poi_type": "RESISTANCE|SUPPORT|PIVOT|BREAKOUT|REVERSAL",
        "poi_subtype": "ORDER_BLOCK|FAIR_VALUE_GAP|IMBALANCE|INSTITUTIONAL_LEVEL|FIBONACCI|ROUND_NUMBER",
        "symbol": "EURUSD|GBPUSD|USDJPY|etc",
        "timeframe": "MONTHLY|WEEKLY|DAILY|H4|H1|M15|M5",
        "price_level": 1.0900,
        "precision_range": {"min": 1.0895, "max": 1.0905},
        "strength_score": 87.5,
        "confidence_level": "HIGH|MEDIUM|LOW",
        "creation_reason": "ORDER_BLOCK_DETECTED|STRUCTURE_BREAK|FIBONACCI_CONFLUENCE"
    },
    "lifecycle_stage": {
        "current_stage": "CREATED|ACTIVE|TESTED|VALIDATED|WEAKENING|BROKEN|EXPIRED",
        "stage_duration_hours": 24.5,
        "previous_stage": "ACTIVE",
        "stage_change_reason": "PRICE_TEST|TIME_DECAY|STRENGTH_INCREASE",
        "expected_next_stage": "TESTED|BROKEN|EXPIRED",
        "estimated_lifetime_hours": 72.0
    },
    "market_interaction": {
        "total_tests": 3,
        "successful_holds": 2,
        "failed_holds": 1,
        "average_reaction_pips": 25.4,
        "strongest_reaction_pips": 45.2,
        "last_test_timestamp": "2025-08-01T13:45:30.123456",
        "test_frequency_per_day": 1.2,
        "reaction_speed_seconds": 45.6
    },
    "technical_context": {
        "market_structure": "TRENDING_UP|TRENDING_DOWN|RANGING|CONSOLIDATION",
        "session_context": "LONDON|NEW_YORK|ASIA|OVERLAP|QUIET",
        "volatility_level": "HIGH|MEDIUM|LOW",
        "volume_profile": "HIGH|AVERAGE|LOW",
        "related_levels": {
            "support_levels": [1.0850, 1.0800],
            "resistance_levels": [1.0950, 1.1000],
            "pivot_points": [1.0875, 1.0925]
        },
        "fibonacci_alignment": {
            "retracement_level": "23.6|38.2|50.0|61.8|78.6",
            "extension_level": "127.2|161.8|200.0|261.8",
            "confluence_strength": 85.2
        }
    },
    "strength_metrics": {
        "base_strength": 75.0,
        "time_decay_factor": 0.95,
        "test_reinforcement": 12.5,
        "volume_confirmation": 8.3,
        "confluence_bonus": 15.7,
        "final_strength": 87.5,
        "strength_history": [75.0, 78.2, 85.1, 87.5],
        "strength_trend": "INCREASING|STABLE|DECREASING"
    },
    "confluence_factors": {
        "fibonacci_confluence": true,
        "order_block_confluence": true,
        "previous_structure_confluence": false,
        "round_number_confluence": true,
        "daily_level_confluence": true,
        "weekly_level_confluence": false,
        "confluence_count": 4,
        "confluence_score": 85.0
    },
    "risk_assessment": {
        "break_probability": 25.3,
        "hold_probability": 74.7,
        "risk_reward_potential": 2.8,
        "position_sizing_factor": 1.2,
        "max_acceptable_risk": 0.5,
        "stop_loss_buffer_pips": 15,
        "invalidation_level": 1.0915
    },
    "trading_implications": {
        "trade_setup_type": "REVERSAL|CONTINUATION|BREAKOUT",
        "entry_strategy": "LIMIT_ORDER|MARKET_ORDER|STOP_ORDER",
        "optimal_entry_range": {"min": 1.0895, "max": 1.0905},
        "stop_loss_level": 1.0915,
        "take_profit_levels": [1.0850, 1.0800, 1.0750],
        "position_size_recommendation": "NORMAL|REDUCED|INCREASED",
        "time_validity": "2025-08-02T14:23:45.123456"
    },
    "historical_performance": {
        "similar_pois_success_rate": 78.5,
        "average_hold_duration_hours": 48.2,
        "average_reaction_strength": 32.1,
        "break_pattern_analysis": "CLEAN_BREAK|FAKE_BREAK|GRADUAL_EROSION",
        "seasonal_tendency": "STRONGER_IN_LONDON|WEAKER_IN_ASIA",
        "correlation_with_news": 0.65
    },
    "related_patterns": {
        "associated_ict_patterns": ["ORDER_BLOCK", "FAIR_VALUE_GAP"],
        "pattern_confluence": true,
        "pattern_ids": ["SB_EURUSD_H1_20250801_142345"],
        "pattern_poi_synergy": 92.3,
        "combined_probability": 84.7
    },
    "monitoring_config": {
        "alert_on_test": true,
        "alert_on_break": true,
        "alert_on_strength_change": 10.0,
        "monitoring_timeframes": ["M5", "M15", "H1"],
        "notification_channels": ["DASHBOARD", "EMAIL", "PUSH"],
        "auto_update_frequency": 300
    },
    "validation_criteria": {
        "minimum_tests_required": 2,
        "minimum_strength_threshold": 70.0,
        "maximum_age_hours": 168.0,
        "volume_confirmation_required": true,
        "structure_alignment_required": true,
        "invalidation_conditions": ["CLEAN_BREAK", "TIME_EXPIRY", "STRENGTH_BELOW_50"]
    },
    "metadata": {
        "session_id": "ICT_20250801_142345_abc123",
        "poi_version": "v2.1.3",
        "calculation_time_ms": 67.8,
        "data_sources": ["MT5_LIVE", "HISTORICAL_DATABASE"],
        "analyst_notes": "Strong confluence with daily resistance and round number",
        "poi_image_path": "/images/pois/POI_EURUSD_1.0900_20250801.png",
        "related_analysis_ids": ["ANALYSIS_EURUSD_20250801_14234"]
    }
}
```

## 🎯 **TIPOS DE POI Y SUS CARACTERÍSTICAS**

### **1. RESISTANCE POI (🔴)**
- **Función:** Nivel donde el precio tiene dificultad para subir
- **Origen:** Order blocks bajistas, previous highs, fibonacci
- **Comportamiento:** Rechazo, reversal, eventual break alcista
- **Durabilidad:** Alta en estructuras mayores

### **2. SUPPORT POI (🟢)**
- **Función:** Nivel donde el precio encuentra soporte
- **Origen:** Order blocks alcistas, previous lows, institucional
- **Comportamiento:** Rebote, continuation, eventual break bajista
- **Durabilidad:** Muy alta en niveles probados múltiples veces

### **3. PIVOT POI (🟡)**
- **Función:** Nivel que puede actuar como soporte o resistencia
- **Origen:** Confluencia de múltiples factores técnicos
- **Comportamiento:** Direccional según contexto de mercado
- **Durabilidad:** Variable según confirmaciones

### **4. BREAKOUT POI (🔵)**
- **Función:** Nivel que al romperse confirma nuevo movimiento
- **Origen:** Estructuras clave, consolidaciones prolongadas
- **Comportamiento:** Explosión direccional tras ruptura
- **Durabilidad:** Baja una vez roto, alta como nuevo soporte/resistencia

### **5. REVERSAL POI (🟣)**
- **Función:** Nivel con alta probabilidad de cambio de dirección
- **Origen:** Extremos de mercado, divergencias, confluencias
- **Comportamiento:** Reversal agresivo del movimiento actual
- **Durabilidad:** Alta en estructuras de largo plazo

## 📈 **MÉTRICAS DE CICLO DE VIDA**

### **Estados del POI:**
```json
{
    "poi_lifecycle_states": {
        "CREATED": {
            "description": "POI recién identificado",
            "typical_duration_hours": 1-6,
            "strength_range": "60-80",
            "actions": ["VALIDATE", "MONITOR"]
        },
        "ACTIVE": {
            "description": "POI confirmado y monitoreándose",
            "typical_duration_hours": 12-72,
            "strength_range": "70-95",
            "actions": ["TEST", "TRADE", "UPDATE"]
        },
        "TESTED": {
            "description": "Price ha interactuado con el POI",
            "typical_duration_hours": 1-24,
            "strength_range": "65-100",
            "actions": ["ANALYZE_REACTION", "UPDATE_STRENGTH"]
        },
        "VALIDATED": {
            "description": "POI ha mostrado reacción positiva",
            "typical_duration_hours": 24-168,
            "strength_range": "80-100",
            "actions": ["CONTINUE_MONITORING", "TRADE_SETUP"]
        },
        "WEAKENING": {
            "description": "POI muestra signos de debilitamiento",
            "typical_duration_hours": 6-48,
            "strength_range": "30-70",
            "actions": ["REDUCE_CONFIDENCE", "PREPARE_INVALIDATION"]
        },
        "BROKEN": {
            "description": "POI ha sido decisivamente roto",
            "typical_duration_hours": 0,
            "strength_range": "0-20",
            "actions": ["INVALIDATE", "CREATE_NEW_POI"]
        },
        "EXPIRED": {
            "description": "POI ha llegado al final de su vida útil",
            "typical_duration_hours": 0,
            "strength_range": "0-50",
            "actions": ["ARCHIVE", "ANALYZE_PERFORMANCE"]
        }
    }
}
```

### **Métricas de rendimiento:**
```json
{
    "poi_performance_kpis": {
        "success_rate_by_type": {
            "RESISTANCE": 84.2,
            "SUPPORT": 88.7,
            "PIVOT": 72.3,
            "BREAKOUT": 76.1,
            "REVERSAL": 79.8
        },
        "average_lifetime_hours": {
            "H4_POI": 72.5,
            "H1_POI": 24.3,
            "M15_POI": 6.8,
            "DAILY_POI": 168.2
        },
        "strength_accuracy": {
            "high_strength_success": 91.3,
            "medium_strength_success": 76.8,
            "low_strength_success": 58.2
        }
    }
}
```

## 🔧 **ALGORITMOS DE GESTIÓN**

### **Cálculo de fortaleza POI:**
```python
def calculate_poi_strength(poi_data):
    base_strength = poi_data.initial_strength
    
    # Time decay factor
    age_hours = poi_data.age_hours
    decay_factor = max(0.5, 1.0 - (age_hours / 168.0) * 0.3)
    
    # Test reinforcement
    successful_tests = poi_data.successful_holds
    test_bonus = min(20.0, successful_tests * 5.0)
    
    # Confluence bonus
    confluence_bonus = poi_data.confluence_count * 3.5
    
    # Volume confirmation
    volume_bonus = 10.0 if poi_data.volume_confirmed else 0.0
    
    final_strength = (base_strength * decay_factor + 
                     test_bonus + confluence_bonus + volume_bonus)
    
    return min(100.0, max(0.0, final_strength))
```

### **Detección de invalidación:**
```python
def check_poi_invalidation(poi, current_price):
    invalidation_reasons = []
    
    # Clean break check
    if poi.type == "RESISTANCE":
        if current_price > poi.level + poi.break_threshold:
            invalidation_reasons.append("CLEAN_BREAK_ABOVE")
    elif poi.type == "SUPPORT":
        if current_price < poi.level - poi.break_threshold:
            invalidation_reasons.append("CLEAN_BREAK_BELOW")
    
    # Time expiry check
    if poi.age_hours > poi.max_lifetime_hours:
        invalidation_reasons.append("TIME_EXPIRY")
    
    # Strength degradation check
    if poi.current_strength < poi.minimum_strength:
        invalidation_reasons.append("STRENGTH_DEGRADATION")
    
    return invalidation_reasons
```

### **Optimización automática:**
```python
def optimize_poi_parameters():
    historical_data = load_poi_historical_data()
    
    # Analyze success rates by parameters
    success_by_timeframe = analyze_success_by_timeframe(historical_data)
    success_by_strength = analyze_success_by_strength(historical_data)
    success_by_confluence = analyze_success_by_confluence(historical_data)
    
    # Update optimal parameters
    optimal_params = {
        "minimum_strength_threshold": find_optimal_threshold(success_by_strength),
        "confluence_weight": find_optimal_weight(success_by_confluence),
        "time_decay_rate": find_optimal_decay_rate(historical_data)
    }
    
    return optimal_params
```

## 📊 **ANÁLISIS Y QUERIES ÚTILES**

### **Buscar POIs específicos:**
```bash
# POIs activos de alta fortaleza
jq 'select(.lifecycle_stage.current_stage == "ACTIVE" and .poi_details.strength_score > 80)' poi_lifecycle_2025-08-01.jsonl

# POIs que han sido testados exitosamente
jq 'select(.event_id == "POI_TESTED" and .market_interaction.successful_holds > .market_interaction.failed_holds)' poi_lifecycle_2025-08-01.jsonl

# Análisis de rendimiento por tipo
jq 'group_by(.poi_details.poi_type) | map({type: .[0].poi_details.poi_type, avg_strength: (map(.poi_details.strength_score) | add/length)})' poi_lifecycle_2025-08-01.jsonl
```

### **Scripts de análisis:**
```python
import json
import pandas as pd
from datetime import datetime, timedelta

def analyze_poi_performance(file_path):
    # Load POI data
    pois = []
    with open(file_path) as f:
        pois = [json.loads(line) for line in f]
    
    df = pd.DataFrame(pois)
    
    # Success rate analysis
    success_rate = calculate_success_rate(df)
    
    # Lifetime analysis
    avg_lifetime = calculate_average_lifetime(df)
    
    # Strength correlation
    strength_correlation = analyze_strength_correlation(df)
    
    return {
        "success_rate": success_rate,
        "average_lifetime": avg_lifetime,
        "strength_correlation": strength_correlation
    }

def generate_poi_report():
    # Daily POI summary
    active_pois = get_active_pois()
    resolved_pois = get_resolved_pois_today()
    expired_pois = get_expired_pois_today()
    
    report = {
        "date": datetime.now().date().isoformat(),
        "summary": {
            "active_count": len(active_pois),
            "resolved_count": len(resolved_pois),
            "expired_count": len(expired_pois),
            "success_rate": calculate_daily_success_rate()
        },
        "top_performing_pois": get_top_performing_pois(5),
        "alerts": get_poi_alerts(),
        "recommendations": generate_poi_recommendations()
    }
    
    return report
```

## 🎯 **INTEGRACIÓN CON TRADING**

### **Generación de señales:**
```python
def generate_poi_trading_signals():
    active_pois = get_active_pois()
    signals = []
    
    for poi in active_pois:
        if poi.strength_score > 80 and poi.confluence_count >= 3:
            signal = {
                "poi_id": poi.id,
                "signal_type": determine_signal_type(poi),
                "entry_price": poi.optimal_entry_range,
                "stop_loss": poi.stop_loss_level,
                "take_profit": poi.take_profit_levels,
                "position_size": calculate_position_size(poi),
                "confidence": poi.strength_score,
                "risk_reward": poi.risk_reward_potential
            }
            signals.append(signal)
    
    return signals
```

### **Risk management integration:**
```python
def adjust_risk_for_poi(poi, base_risk):
    # Adjust risk based on POI strength
    strength_multiplier = poi.strength_score / 100.0
    
    # Adjust based on confluence
    confluence_multiplier = min(1.5, 1.0 + (poi.confluence_count * 0.1))
    
    # Adjust based on historical performance
    historical_multiplier = poi.historical_success_rate / 100.0
    
    adjusted_risk = base_risk * strength_multiplier * confluence_multiplier * historical_multiplier
    
    return min(adjusted_risk, base_risk * 2.0)  # Cap at 2x base risk
```

---

**Última actualización:** 2025-08-01  
**Versión:** 2.1.3  
**Mantenido por:** POI Management System v5.0
