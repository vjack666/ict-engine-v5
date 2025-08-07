# 🚨 ERROR TRACKING - DOCUMENTACIÓN TÉCNICA

## 📋 **PROPÓSITO Y ALCANCE**

Esta carpeta almacena todos los errores, excepciones y eventos críticos del sistema ICT Engine. Es fundamental para debugging, análisis post-mortem y mejora continua del sistema.

## 🏗️ **ESTRUCTURA DE ARCHIVOS**

```
error_tracking/
├── error_tracking_2025-08-01.jsonl    # Errores del día actual
├── error_tracking_2025-07-31.jsonl    # Errores del día anterior
├── README.md                           # Esta documentación
└── schemas/
    ├── error_schema.json              # Schema JSON para validación
    └── error_examples.json            # Ejemplos de errores típicos
```

## 📊 **FORMATO DE DATOS (JSONL)**

### **Estructura base de cada línea:**
```json
{
    "timestamp": "2025-08-01T14:23:45.123456",
    "bitacora_type": "error_tracking",
    "severity": "HIGH|MEDIUM|LOW|CRITICAL",
    "component": "DASHBOARD|ICT_ENGINE|POI_SYSTEM|MT5_CONNECTOR|CORE",
    "event_id": "ERROR_CODE_UNIQUE",
    "description": "Descripción humana del error",
    "error_details": {
        "exception_type": "ImportError|ValueError|ConnectionError|etc",
        "exception_message": "Mensaje exacto de la excepción",
        "traceback": "Stack trace completo",
        "file_path": "ruta/del/archivo/donde/ocurrio.py",
        "line_number": 123,
        "function_name": "nombre_de_la_funcion"
    },
    "context": {
        "session_id": "ICT_20250801_142345_abc123",
        "user_action": "Acción que desencadenó el error",
        "system_state": "Estado del sistema al momento del error",
        "mt5_connected": true|false,
        "active_patterns": ["SILVER_BULLET", "OTE"],
        "current_timeframe": "H1|M15|M5|etc"
    },
    "impact": {
        "severity_level": 1-5,
        "affected_components": ["DASHBOARD", "ANALYSIS"],
        "data_loss": true|false,
        "recovery_possible": true|false,
        "estimated_downtime": "00:02:30"
    },
    "resolution": {
        "status": "PENDING|IN_PROGRESS|RESOLVED|ESCALATED",
        "attempted_fixes": ["Restart MT5", "Clear cache"],
        "final_solution": "Descripción de la solución",
        "resolved_at": "2025-08-01T14:25:30.123456",
        "resolved_by": "SYSTEM|USER|ADMIN"
    },
    "metadata": {
        "python_version": "3.13.2",
        "os_info": "Windows 11 Pro",
        "memory_usage": "156.7 MB",
        "cpu_usage": "23.4%",
        "disk_space": "45.2 GB free"
    }
}
```

## 🔍 **TIPOS DE ERRORES REGISTRADOS**

### **1. CRITICAL (🔴 Críticos)**
- Sistema completamente inoperativo
- Pérdida de conexión MT5 permanente
- Corruption de datos críticos
- Fallos de seguridad

### **2. HIGH (🟠 Altos)**
- Fallos de módulos principales
- Errores de importación críticos
- Excepciones no manejadas en core
- Problemas de performance severos

### **3. MEDIUM (🟡 Medios)**
- Errores de validación de datos
- Timeouts de conexión temporales
- Fallos de módulos secundarios
- Warnings escalados

### **4. LOW (🟢 Bajos)**
- Errores de formato menores
- Warnings informativos
- Problemas de UI no críticos
- Errores de configuración menores

## 📈 **MÉTRICAS Y ANÁLISIS**

### **KPIs Tracked:**
- **Error Rate:** Errores por hora/día
- **MTTR (Mean Time To Resolution):** Tiempo promedio de resolución
- **Error Distribution:** Distribución por componente/severidad
- **Recurring Errors:** Errores que se repiten
- **Recovery Success Rate:** Tasa de recuperación exitosa

### **Queries útiles para análisis:**
```python
# Errores críticos del último día
jq 'select(.severity == "CRITICAL" and .timestamp > "2025-08-01")' error_tracking_2025-08-01.jsonl

# Top 5 componentes con más errores
jq -s 'group_by(.component) | map({component: .[0].component, count: length}) | sort_by(.count) | reverse | .[0:5]' error_tracking_*.jsonl

# Errores sin resolver
jq 'select(.resolution.status == "PENDING")' error_tracking_*.jsonl
```

## 🔧 **CONFIGURACIÓN Y MANTENIMIENTO**

### **Rotación de archivos:**
- **Frecuencia:** Diaria (00:00 UTC)
- **Retención:** 30 días para logs normales, 90 días para críticos
- **Compresión:** Automática después de 7 días
- **Backup:** Semanal a storage externo

### **Alertas automáticas:**
- CRITICAL: Notificación inmediata
- HIGH: Notificación en 5 minutos
- MEDIUM: Resumen cada hora
- LOW: Resumen diario

### **Integración con monitoreo:**
```python
# Ejemplo de uso en código
from sistema.logging_interface import enviar_senal_log

try:
    # Código que puede fallar
    process_ict_pattern()
except Exception as e:
    enviar_senal_log(
        "ERROR", 
        f"Error procesando patrón ICT: {str(e)}", 
        __name__, 
        "error_tracking",
        extra_data={
            "exception_type": type(e).__name__,
            "traceback": traceback.format_exc(),
            "context": get_current_context()
        }
    )
```

## 📋 **CHECKLIST DE MONITOREO DIARIO**

- [ ] ✅ Verificar que no hay errores CRITICAL sin resolver
- [ ] 📊 Revisar tendencias de errores (incremento/decremento)
- [ ] 🔄 Confirmar que la rotación diaria funcionó
- [ ] 📈 Analizar métricas de performance de errores
- [ ] 🔍 Investigar nuevos tipos de errores
- [ ] 📝 Documentar soluciones a errores recurrentes
- [ ] 🚨 Verificar que las alertas funcionan correctamente

## 🎯 **CASOS DE USO COMUNES**

### **Debugging de producción:**
```bash
# Buscar errores relacionados con MT5
grep -i "mt5" error_tracking_2025-08-01.jsonl | jq .

# Errores de las últimas 2 horas
jq 'select(.timestamp > "2025-08-01T12:00")' error_tracking_2025-08-01.jsonl
```

### **Análisis de patrones:**
```python
# Script para encontrar errores recurrentes
import json
from collections import Counter

errors = []
with open('error_tracking_2025-08-01.jsonl') as f:
    errors = [json.loads(line) for line in f]

# Top errores por mensaje
error_messages = [e['error_details']['exception_message'] for e in errors]
print(Counter(error_messages).most_common(5))
```

### **Reportes automáticos:**
```python
# Generar reporte diario de errores
def generate_daily_error_report(date):
    # Cargar errores del día
    # Agrupar por severidad
    # Calcular métricas
    # Generar visualizaciones
    # Enviar por email/Slack
    pass
```

---

**Última actualización:** 2025-08-01  
**Versión:** 1.0  
**Mantenido por:** Sistema ICT Engine v5.0
