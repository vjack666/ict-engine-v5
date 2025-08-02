# Manual del Sistema de Bitácoras ICT Engine v3.44

## 🎯 Introducción

El Sistema de Bitácoras del ICT Engine proporciona registro completo y monitoreo en tiempo real de todas las operaciones del sistema. Está diseñado para rastrear decisiones de trading, estado de componentes, errores del sistema y métricas de rendimiento.

## 📋 Tipos de Bitácoras

### 1. **System Status** (`system_status`)
Registra el estado general del sistema y eventos de inicialización/shutdown.

**Eventos típicos:**
- Inicio y parada del sistema
- Cambios de configuración
- Updates de componentes
- Estados de conectividad

**Ejemplo:**
```json
{
  "timestamp": "2025-08-01T10:30:00.000Z",
  "bitacora_type": "system_status",
  "severity": "HIGH", 
  "component": "SYSTEM",
  "event_id": "SYSTEM_STARTUP",
  "description": "ICT Engine iniciado correctamente",
  "data": {"version": "v3.44", "components": ["core", "dashboard"]},
  "session_id": "ICT_20250801_103000_a1b2c3d4"
}
```

### 2. **Trading Decisions** (`trading_decisions`)
Registra todas las decisiones de trading tomadas por el sistema.

**Información registrada:**
- Patrón detectado
- Dirección del trade
- Precios de entrada y salida
- Risk:Reward ratio
- Razonamiento de la decisión

**Ejemplo:**
```json
{
  "timestamp": "2025-08-01T10:35:00.000Z",
  "bitacora_type": "trading_decisions",
  "event_id": "TRADE_DECISION_SILVER_BULLET",
  "description": "Decisión de trading: BUY SILVER_BULLET",
  "data": {
    "pattern": "SILVER_BULLET",
    "direction": "BUY",
    "strength": 85.5,
    "entry_price": 1.09234,
    "targets": [1.09674, 1.09904],
    "stop_loss": 1.09034,
    "risk_reward": 2.2,
    "reasoning": "Silver Bullet durante London session con Order Block BULLISH"
  }
}
```

### 3. **Pattern Detection** (`pattern_detection`)
Registra la detección de patrones ICT y análisis de estructura.

**Información registrada:**
- Tipo de patrón detectado
- Nivel de confianza
- Ubicación en el gráfico
- Confluencias identificadas

### 4. **Performance Metrics** (`performance`)
Registra métricas de rendimiento del sistema en tiempo real.

**Métricas incluidas:**
- Tiempo de respuesta de componentes
- Uso de CPU y memoria
- Throughput de procesamiento
- Latencia de señales

### 5. **Error Tracking** (`error_tracking`)
Registra errores del sistema para debugging y mejora continua.

**Información registrada:**
- Tipo de error
- Componente afectado
- Stack trace (cuando está disponible)
- Acciones de recuperación

### 6. **Session Analysis** (`session_analysis`)
Registra análisis completos por sesión de trading.

### 7. **POI Lifecycle** (`poi_lifecycle`)
Rastrea el ciclo de vida de los Puntos de Interés (POIs).

### 8. **Risk Management** (`risk_management`)
Registra eventos relacionados con la gestión de riesgo.

## 🔧 Uso Básico

### Inicialización del Sistema

```python
# Importar el sistema de bitácoras
from docs.bitacoras.bitacora_manager import bitacora_manager

# El sistema se inicializa automáticamente
# Verificar estado
summary = bitacora_manager.get_session_summary()
print(f"Sesión activa: {summary['session_id']}")
```

### Registrar Eventos Personalizados

#### 1. Eventos del Sistema
```python
from docs.bitacoras.bitacora_manager import bitacora_manager, SeverityLevel

bitacora_manager.log_system_event(
    severity=SeverityLevel.INFO,
    event_id="CUSTOM_EVENT",
    description="Evento personalizado del sistema",
    data={"custom_field": "valor"},
    context={"module": "mi_modulo"}
)
```

#### 2. Decisiones de Trading
```python
bitacora_manager.log_trading_decision(
    pattern="JUDAS_SWING",
    direction="SELL",
    strength=78.5,
    entry_price=1.09000,
    targets=[1.08600, 1.08300],
    stop_loss=1.09200,
    risk_reward=2.5,
    reasoning="Judas Swing confirmado con ruptura falsa"
)
```

#### 3. Detección de Patrones
```python
bitacora_manager.log_pattern_detection(
    pattern_type="ORDER_BLOCK",
    confidence=85.0,
    location_data={"price": 1.09500, "timeframe": "M15"},
    confluences=["High volume", "Previous resistance"],
    context={"session": "LONDON"}
)
```

### Funciones de Conveniencia

Para casos comunes, usa las funciones predefinidas:

```python
from docs.bitacoras.bitacora_manager import (
    log_system_startup,
    log_trading_signal, 
    log_poi_detected,
    log_critical_error
)

# Registro rápido de señal de trading
log_trading_signal(
    pattern="SILVER_BULLET",
    direction="BUY", 
    strength=90.0,
    entry_price=1.09234,
    targets=[1.09674],
    stop_loss=1.09034,
    risk_reward=2.2
)

# Registro rápido de POI
log_poi_detected(
    poi_type="ORDER_BLOCK_BULLISH",
    price=1.09500,
    strength="HIGH",
    timeframe="M15"
)

# Registro rápido de error crítico
log_critical_error("PATTERN_ANALYZER", ValueError("Invalid data"))
```

## 📊 Consulta de Datos

### Resumen de Sesión
```python
summary = bitacora_manager.get_session_summary()
print(f"Eventos totales: {summary['total_events']}")
print(f"Tipos de bitácora: {summary['bitacora_types']}")
```

### Reporte Diario
```python
from datetime import datetime

# Reporte de hoy
report = bitacora_manager.generate_daily_report()
print(f"Eventos críticos: {len(report['critical_events'])}")

# Reporte de fecha específica
specific_date = datetime(2025, 8, 1)
report = bitacora_manager.generate_daily_report(specific_date)
```

## 🔍 Monitoreo del Sistema

### Iniciar Monitoreo
```python
from docs.logs.system_monitor import system_monitor

# Iniciar monitoreo (se ejecuta en background)
system_monitor.start_monitoring()

# Obtener estado actual
status = system_monitor.get_system_summary()
print(f"Estado general: {status['overall_status']}")
```

### Consultar Estado de Componentes
```python
# Estado de un componente específico
details = system_monitor.get_component_details("pattern_analyzer")
if details:
    print(f"Estado: {details['status']}")
    print(f"Tiempo respuesta: {details['response_time_ms']}ms")
    print(f"Errores: {details['error_count']}")
```

### Obtener Alertas Recientes
```python
# Alertas de las últimas 24 horas
recent_alerts = system_monitor.get_recent_alerts(hours=24)
for alert in recent_alerts:
    print(f"{alert['timestamp']}: {alert['level']} - {alert['message']}")
```

### Generar Reporte de Salud
```python
health_report = system_monitor.generate_health_report()
print(health_report)
```

## 📁 Estructura de Archivos

Las bitácoras se almacenan en formato JSONL (JSON Lines) organizadas por tipo y fecha:

```
docs/bitacoras/
├── system_status/
│   ├── system_status_2025-08-01.jsonl
│   └── system_status_2025-08-02.jsonl
├── trading_decisions/
│   ├── trading_decisions_2025-08-01.jsonl
│   └── trading_decisions_2025-08-02.jsonl
├── pattern_detection/
│   └── pattern_detection_2025-08-01.jsonl
└── [otros tipos]/
```

### Lectura Manual de Archivos

```python
import json
from pathlib import Path

# Leer bitácora de trading decisions de hoy
today = datetime.now().strftime("%Y-%m-%d")
log_file = Path(f"docs/bitacoras/trading_decisions/trading_decisions_{today}.jsonl")

if log_file.exists():
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line.strip())
            print(f"{entry['timestamp']}: {entry['description']}")
```

## 🧹 Mantenimiento

### Limpieza Automática
```python
# Limpiar logs más antiguos de 30 días
bitacora_manager.cleanup_old_logs(retention_days=30)
```

### Configurar Umbrales de Monitoreo
```python
# Cambiar umbral de CPU
system_monitor.set_threshold("cpu_usage", 90.0)

# Cambiar umbral de memoria  
system_monitor.set_threshold("memory_usage", 80.0)
```

### Resolver Alertas
```python
# Marcar alerta como resuelta
system_monitor.resolve_alert(alert_index=0)
```

## 🚀 Inicialización Automática

Para inicializar todo el sistema de documentación:

```bash
cd "c:\Users\v_jac\Desktop\itc engine 3.44"
python docs\init_documentation_system.py
```

Este script:
- ✅ Crea estructura de directorios
- ✅ Inicializa sistema de bitácoras  
- ✅ Activa monitoreo del sistema
- ✅ Genera reporte inicial
- ✅ Configura logging especializado

## 📊 Dashboard de Monitoreo

El sistema incluye un dashboard de monitoreo accesible desde:

```python
from docs.logs.system_monitor import get_system_status, get_health_report

# Estado en tiempo real
status = get_system_status()

# Reporte completo de salud
health = get_health_report()
```

## 🔧 Integración con Componentes Existentes

El sistema de bitácoras se integra automáticamente con:

- **Pattern Analyzer**: Registra detección de patrones automáticamente
- **POI Detector**: Log de POIs detectados 
- **Risk Manager**: Eventos de gestión de riesgo
- **Dashboard**: Métricas de interfaz de usuario
- **Sistema de Logging**: Integración con SLUC v2.0

## ⚠️ Consideraciones Importantes

### Rendimiento
- Las bitácoras están optimizadas para mínimo impacto en rendimiento
- Operaciones thread-safe para concurrencia
- Escritura asíncrona cuando es posible

### Almacenamiento
- Rotación automática diaria de archivos
- Compresión automática de logs antiguos
- Limpieza configurable por política de retención

### Seguridad
- Logs encriptados para información sensible
- No se registran credenciales o datos privados
- Acceso controlado a archivos de bitácora

---

## 🆘 Troubleshooting

### Problema: Bitácoras no se crean
**Solución:** Verificar permisos de escritura en directorio `docs/bitacoras/`

### Problema: Monitor no inicia
**Solución:** Verificar dependencias `psutil` instalada

### Problema: Archivos de log muy grandes
**Solución:** Ajustar política de retención con `cleanup_old_logs()`

### Problema: Alertas falsas
**Solución:** Ajustar umbrales con `set_threshold()`

---

¡El Sistema de Bitácoras ICT Engine v3.44 está listo para proporcionar observabilidad completa de tu sistema de trading!
