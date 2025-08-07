# ⚡ PERFORMANCE - DOCUMENTACIÓN TÉCNICA

## 📋 **PROPÓSITO Y ALCANCE**

Esta carpeta almacena todas las métricas de rendimiento del sistema ICT Engine, incluyendo tiempos de respuesta, uso de recursos, throughput de datos y optimizaciones. Es crucial para mantener el sistema funcionando en óptimas condiciones.

## 🏗️ **ESTRUCTURA DE ARCHIVOS**

```
performance/
├── performance_2025-08-01.jsonl      # Métricas del día actual
├── performance_2025-07-31.jsonl      # Métricas del día anterior
├── README.md                          # Esta documentación
├── benchmarks/
│   ├── system_benchmarks.json        # Benchmarks de referencia
│   ├── comparison_metrics.json       # Comparación con versiones anteriores
│   └── optimization_targets.json     # Objetivos de optimización
├── reports/
│   ├── daily_performance_report.json # Reporte diario automatizado
│   ├── weekly_trends.json            # Tendencias semanales
│   └── bottleneck_analysis.json      # Análisis de cuellos de botella
└── alerts/
    ├── performance_thresholds.json   # Umbrales de alertas
    └── alert_history.json            # Historial de alertas
```

## 📊 **FORMATO DE DATOS (JSONL)**

### **Estructura base de cada línea:**
```json
{
    "timestamp": "2025-08-01T14:23:45.123456",
    "bitacora_type": "performance",
    "severity": "INFO|WARNING|CRITICAL",
    "component": "SYSTEM|DASHBOARD|ICT_ENGINE|MT5_CONNECTOR|POI_SYSTEM|DB",
    "event_id": "PERF_MEASUREMENT|PERF_ALERT|PERF_OPTIMIZATION",
    "description": "Medición de rendimiento rutinaria",
    "performance_metrics": {
        "execution_time_ms": 145.67,
        "memory_usage_mb": 156.8,
        "cpu_usage_percent": 23.4,
        "disk_io_mb_s": 12.5,
        "network_io_kb_s": 45.2,
        "gpu_usage_percent": 0.0,
        "thread_count": 12,
        "open_file_descriptors": 89
    },
    "system_resources": {
        "total_memory_mb": 16384,
        "available_memory_mb": 8192,
        "memory_usage_percent": 50.0,
        "cpu_cores": 8,
        "cpu_frequency_mhz": 3200,
        "disk_space_total_gb": 512,
        "disk_space_free_gb": 256,
        "swap_usage_mb": 0
    },
    "component_specific": {
        "dashboard": {
            "ui_render_time_ms": 16.7,
            "data_refresh_time_ms": 89.4,
            "widget_count": 15,
            "active_subscriptions": 8,
            "fps": 60.0,
            "memory_leaks_detected": false
        },
        "ict_engine": {
            "pattern_detection_time_ms": 234.5,
            "patterns_processed_per_second": 145.2,
            "analysis_queue_size": 23,
            "confidence_calculation_time_ms": 67.8,
            "cache_hit_ratio": 0.87,
            "algorithm_efficiency": 92.3
        },
        "mt5_connector": {
            "connection_latency_ms": 45.2,
            "data_fetch_time_ms": 123.4,
            "tick_processing_rate": 567.8,
            "reconnection_count": 0,
            "data_integrity_check": true,
            "bandwidth_usage_kb_s": 34.6
        },
        "poi_system": {
            "poi_calculation_time_ms": 178.9,
            "active_poi_count": 45,
            "poi_update_frequency_s": 30.0,
            "scoring_algorithm_time_ms": 89.3,
            "cache_efficiency": 94.1
        },
        "database": {
            "query_response_time_ms": 12.3,
            "connection_pool_usage": 8,
            "transaction_rate_per_s": 45.6,
            "index_efficiency": 96.7,
            "lock_wait_time_ms": 0.5,
            "cache_hit_ratio": 0.92
        }
    },
    "throughput_metrics": {
        "ticks_processed_per_minute": 15420,
        "patterns_analyzed_per_hour": 8760,
        "poi_updates_per_day": 2340,
        "dashboard_refreshes_per_minute": 12,
        "api_calls_per_second": 23.4,
        "data_points_processed": 156789
    },
    "latency_metrics": {
        "end_to_end_latency_ms": 289.4,
        "data_ingestion_latency_ms": 45.2,
        "analysis_latency_ms": 167.8,
        "ui_update_latency_ms": 76.4,
        "alert_generation_latency_ms": 12.1,
        "p95_latency_ms": 456.7,
        "p99_latency_ms": 789.3
    },
    "quality_metrics": {
        "data_accuracy_percent": 99.97,
        "uptime_percent": 99.98,
        "error_rate_percent": 0.02,
        "sla_compliance_percent": 99.95,
        "user_satisfaction_score": 4.8,
        "system_stability_score": 95.6
    },
    "optimization_opportunities": {
        "bottlenecks_identified": ["PATTERN_ANALYSIS_QUEUE", "MT5_DATA_FETCH"],
        "memory_optimization_potential": 15.3,
        "cpu_optimization_potential": 8.7,
        "cache_improvements": ["ICT_PATTERNS", "POI_SCORES"],
        "algorithm_improvements": ["CONFIDENCE_ENGINE", "FIBONACCI_CALC"],
        "infrastructure_recommendations": ["SSD_UPGRADE", "RAM_INCREASE"]
    },
    "benchmarks": {
        "vs_previous_version": {
            "performance_improvement_percent": 23.4,
            "memory_reduction_percent": 12.8,
            "latency_reduction_percent": 18.5
        },
        "vs_industry_standard": {
            "relative_performance": 147.8,
            "ranking": "TOP_10_PERCENT",
            "competitive_advantage": "HIGH_FREQUENCY_ANALYSIS"
        }
    },
    "alerts": {
        "performance_alerts_triggered": 0,
        "threshold_breaches": [],
        "auto_optimizations_applied": ["CACHE_CLEANUP", "MEMORY_DEFRAG"],
        "manual_intervention_required": false,
        "alert_severity": "NONE|LOW|MEDIUM|HIGH|CRITICAL"
    },
    "metadata": {
        "session_id": "ICT_20250801_142345_abc123",
        "measurement_type": "SCHEDULED|ON_DEMAND|TRIGGERED",
        "measurement_duration_s": 60.0,
        "environment": "PRODUCTION|STAGING|DEVELOPMENT",
        "version": "v5.0.1",
        "configuration_hash": "abc123def456",
        "load_test_scenario": "NORMAL|STRESS|PEAK|BASELINE"
    }
}
```

## 📈 **MÉTRICAS CLAVE DE RENDIMIENTO**

### **1. SISTEMA GENERAL**
```json
{
    "response_time_targets": {
        "excellent": "< 100ms",
        "good": "100-300ms",
        "acceptable": "300-1000ms",
        "poor": "> 1000ms"
    },
    "resource_usage_targets": {
        "memory": "< 512MB normal operation",
        "cpu": "< 30% average, < 80% peak",
        "disk_io": "< 50MB/s sustained",
        "network": "< 100KB/s average"
    }
}
```

### **2. COMPONENTES ESPECÍFICOS**

#### **Dashboard Performance:**
- **UI Render Time:** < 16.7ms (60 FPS)
- **Data Refresh:** < 100ms
- **Memory Usage:** < 100MB
- **Widget Load Time:** < 50ms

#### **ICT Engine Performance:**
- **Pattern Detection:** < 200ms per analysis
- **Confidence Calculation:** < 50ms
- **Throughput:** > 100 patterns/second
- **Accuracy:** > 85% detection rate

#### **MT5 Connector Performance:**
- **Connection Latency:** < 50ms
- **Data Fetch:** < 100ms
- **Tick Processing:** > 500 ticks/second
- **Uptime:** > 99.9%

#### **POI System Performance:**
- **POI Calculation:** < 150ms
- **Scoring Update:** < 80ms
- **Cache Efficiency:** > 90%
- **Memory Usage:** < 50MB

## 🔧 **MONITOREO Y ALERTAS**

### **Umbrales de Alertas:**
```json
{
    "critical_thresholds": {
        "response_time_ms": 2000,
        "memory_usage_percent": 90,
        "cpu_usage_percent": 95,
        "error_rate_percent": 5,
        "disk_space_free_percent": 5
    },
    "warning_thresholds": {
        "response_time_ms": 1000,
        "memory_usage_percent": 70,
        "cpu_usage_percent": 70,
        "error_rate_percent": 1,
        "disk_space_free_percent": 20
    }
}
```

### **Tipos de Alertas:**
- **🔴 CRITICAL:** Sistema en riesgo inmediato
- **🟠 WARNING:** Degradación de rendimiento
- **🟡 INFO:** Información relevante para optimización
- **🟢 SUCCESS:** Mejoras de rendimiento detectadas

## 📊 **ANÁLISIS Y OPTIMIZACIÓN**

### **Queries útiles para análisis:**
```bash
# Encontrar picos de latencia
jq 'select(.latency_metrics.end_to_end_latency_ms > 500)' performance_2025-08-01.jsonl

# Análisis de uso de memoria
jq '.performance_metrics.memory_usage_mb' performance_2025-08-01.jsonl | jq -s 'add/length'

# Throughput promedio por hora
jq -s 'group_by(.timestamp[0:13]) | map({hour: .[0].timestamp[0:13], avg_throughput: (map(.throughput_metrics.ticks_processed_per_minute) | add/length)})' performance_2025-08-01.jsonl
```

### **Scripts de optimización:**
```python
# Análisis de bottlenecks
def analyze_bottlenecks(performance_data):
    bottlenecks = []
    
    # CPU bottlenecks
    if avg_cpu_usage > 80:
        bottlenecks.append("HIGH_CPU_USAGE")
    
    # Memory bottlenecks
    if memory_growth_rate > 10:  # MB/hour
        bottlenecks.append("MEMORY_LEAK_DETECTED")
    
    # I/O bottlenecks
    if disk_io_wait > 20:  # ms
        bottlenecks.append("DISK_IO_BOTTLENECK")
    
    return bottlenecks

# Auto-optimización
def auto_optimize():
    # Limpiar caché si uso de memoria > 70%
    if current_memory_usage > 70:
        cache_manager.cleanup_old_entries()
    
    # Ajustar frecuencia de análisis si CPU > 80%
    if current_cpu_usage > 80:
        analysis_scheduler.reduce_frequency(0.8)
    
    # Comprimir logs si espacio < 20%
    if disk_space_free < 20:
        log_manager.compress_old_logs()
```

## 🎯 **BENCHMARKING Y TESTING**

### **Escenarios de prueba:**
```json
{
    "load_test_scenarios": {
        "baseline": {
            "description": "Operación normal",
            "concurrent_users": 1,
            "data_rate": "normal",
            "duration_minutes": 60
        },
        "stress": {
            "description": "Carga máxima sostenible",
            "concurrent_users": 5,
            "data_rate": "high",
            "duration_minutes": 30
        },
        "peak": {
            "description": "Picos de actividad",
            "concurrent_users": 10,
            "data_rate": "maximum",
            "duration_minutes": 15
        },
        "endurance": {
            "description": "Prueba de resistencia",
            "concurrent_users": 2,
            "data_rate": "normal",
            "duration_hours": 24
        }
    }
}
```

### **Métricas de comparación:**
```python
def compare_performance(current_data, baseline_data):
    comparison = {
        "response_time_improvement": calculate_improvement(
            baseline_data.avg_response_time,
            current_data.avg_response_time
        ),
        "throughput_improvement": calculate_improvement(
            baseline_data.avg_throughput,
            current_data.avg_throughput
        ),
        "memory_efficiency": calculate_efficiency(
            baseline_data.memory_usage,
            current_data.memory_usage
        ),
        "cpu_efficiency": calculate_efficiency(
            baseline_data.cpu_usage,
            current_data.cpu_usage
        )
    }
    return comparison
```

## 📈 **REPORTES Y DASHBOARDS**

### **Reporte diario automatizado:**
```json
{
    "date": "2025-08-01",
    "summary": {
        "overall_performance": "EXCELLENT|GOOD|FAIR|POOR",
        "avg_response_time_ms": 156.7,
        "uptime_percent": 99.98,
        "error_count": 3,
        "optimization_opportunities": 5
    },
    "trends": {
        "performance_trend": "IMPROVING|STABLE|DEGRADING",
        "memory_trend": "INCREASING|STABLE|DECREASING",
        "cpu_trend": "INCREASING|STABLE|DECREASING"
    },
    "recommendations": [
        "Aumentar cache size para POI system",
        "Optimizar algoritmo de detección de patrones",
        "Considerar upgrade de RAM para mejor rendimiento"
    ]
}
```

### **Dashboard en tiempo real:**
- **Sistema overview:** CPU, memoria, disco en tiempo real
- **Component health:** Estado de cada componente
- **Performance graphs:** Tendencias de las últimas 24h
- **Alert center:** Alertas activas y historial
- **Optimization suggestions:** Recomendaciones automáticas

---

**Última actualización:** 2025-08-01  
**Versión:** 5.0.1  
**Mantenido por:** Performance Monitoring System
