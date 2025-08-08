# 📚 DOCUMENTACIÓN ICT ENGINE v5.0

**Última Actualización:** 03 Agosto 2025 - 16:45 hrs
**Estado:** ✅ **CONFIDENCE ENGINE v2.0 MIGRADO + SLUC v2.1 COMPLETO**
**Sistemas Operativos:** Dashboard Multi-POI + TCT Pipeline + Motor Confianza Avanzado

Bienvenido al sistema completo de documentación y bitácoras del ICT Engine. Este directorio contiene toda la información necesaria para operar, monitorear y mantener el sistema de trading profesional ICT.

## 📁 Estructura de la Documentación

```
docs/
├── README.md                          # Este archivo - Punto de entrada
├── MANUAL_BITACORAS.md               # Manual completo del sistema de bitácoras
├── init_documentation_system.py      # Script de inicialización
├── ejemplo_uso_bitacoras.py          # Ejemplo práctico de uso
├──
├── architecture/                      # Documentación de arquitectura
│   └── system_architecture.md        # Arquitectura completa del sistema
├──
├── bitacoras/                         # Documentación del sistema de bitácoras
│   └── bitacora_manager.py           # Gestor principal de bitácoras
├──
├── logs/                             # Logs del sistema y monitoreo
│   ├── system_monitor.py            # Monitor de estado del sistema
│   └── [archivos de log dinámicos]  # Logs generados automáticamente
└──
└── reports/                          # Reportes del sistema
    ├── daily/                       # Reportes diarios
    ├── weekly/                      # Reportes semanales
    └── monthly/                     # Reportes mensuales
```

## 📊 Sistema de Bitácoras Operacionales

La documentación del sistema de bitácoras está en `docs/bitacoras/` con la siguiente estructura:

```
docs/bitacoras/
├── README.md                    # Documentación general del sistema
├── error_tracking.md           # Seguimiento de errores del sistema
├── pattern_detection.md        # Análisis y detección de patrones ICT
├── performance.md              # Métricas de rendimiento del sistema
├── poi_lifecycle.md            # Gestión del ciclo de vida de POIs
├── risk_management.md          # Análisis y control de riesgos
├── session_analysis.md         # Análisis detallado de sesiones
├── system_status.md            # Estado y salud del sistema
└── trading_decisions.md        # Decisiones y señales de trading
```

Los **DATOS REALES** se almacenan en `data/operational/`:

```
data/operational/
├── trading/                    # Datos de trading (.jsonl)
│   ├── decisions/             # Decisiones de trading
│   ├── sessions/              # Análisis de sesiones
│   └── risk/                  # Gestión de riesgo
├── analysis/                  # Datos de análisis técnico (.jsonl)
│   ├── patterns/              # Patrones ICT detectados
│   ├── poi/                   # Puntos de Interés
│   └── performance/           # Métricas de rendimiento
└── system_status/             # Estado del sistema (.jsonl)
```

## 🚀 Inicio Rápido

### 1. Inicializar el Sistema (PRIMER USO)

```bash
# Navegar al directorio del ICT Engine
cd "C:\Users\v_jac\Desktop\itc engine v5.0"

# Ejecutar inicializador
python docs\init_documentation_system.py
```

Este comando:
- ✅ Crea toda la estructura de directorios
- ✅ Inicializa el sistema de bitácoras
- ✅ Activa el monitoreo del sistema
- ✅ Genera reportes iniciales
- ✅ Configura logging especializado

### 2. Ejecutar Ejemplo de Uso

```bash
# Ejecutar demostración completa
python docs\ejemplo_uso_bitacoras.py
```

Esta demostración muestra:
- 🎯 Detección de POIs
- 🧠 Análisis de patrones ICT
- 💹 Decisiones de trading
- 📊 Monitoreo en tiempo real
- 📄 Generación de reportes

### 3. Verificar Estado del Sistema

```python
from docs.logs.system_monitor import get_system_status, get_health_report

# Estado en tiempo real
status = get_system_status()
print(f"Estado: {status['overall_status']}")

# Reporte de salud completo
health = get_health_report()
print(health)
```

## 📋 Sistemas Disponibles

### 1. **Sistema de Bitácoras** 📋
Registro completo de todas las operaciones del sistema.

**Características:**
- 8 tipos de bitácoras especializadas
- Formato JSON estructurado
- Rotación automática diaria
- Thread-safe operations
- Búsqueda y filtrado avanzado

**Acceso rápido:**
```python
from docs.bitacoras.bitacora_manager import bitacora_manager

# Ver resumen de sesión
summary = bitacora_manager.get_session_summary()
print(f"Eventos totales: {summary['total_events']}")
```

### 2. **Monitor del Sistema** 📊
Monitoreo en tiempo real del estado y rendimiento.

**Características:**
- Monitoreo de componentes ICT
- Métricas de sistema (CPU, memoria, disco)
- Alertas automáticas
- Reportes de salud
- Dashboard de estado

**Acceso rápido:**
```python
from docs.logs.system_monitor import system_monitor

# Iniciar monitoreo
system_monitor.start_monitoring()

# Ver estado
status = system_monitor.get_system_summary()
```

### 3. **Generación de Reportes** 📄
Reportes automáticos y personalizados.

**Tipos de reportes:**
- Reportes diarios de bitácoras
- Reportes de salud del sistema
- Análisis de rendimiento
- Resúmenes de trading
- Métricas de componentes

## 🎯 Casos de Uso Principales

### Para Traders
- 📈 **Revisar señales**: Consultar decisiones de trading en `bitacoras/trading_decisions/`
- 🎯 **Analizar patrones**: Ver detección de patrones en `bitacoras/pattern_detection/`
- 📊 **Métricas de sesión**: Revisar análisis por sesión en `bitacoras/session_analysis/`

### Para Desarrolladores
- 🔍 **Debugging**: Consultar errores en `bitacoras/error_tracking/`
- 📊 **Performance**: Revisar métricas en `bitacoras/performance/`
- ⚙️ **Estado del sistema**: Monitorear componentes en `logs/system_monitoring_*.json`

### Para Administradores
- 🏥 **Salud del sistema**: Ejecutar `get_health_report()`
- 🚨 **Alertas**: Revisar `system_monitor.get_recent_alerts()`
- 📄 **Reportes**: Consultar `reports/` para análisis histórico

## 🔧 Configuración Avanzada

### Ajustar Umbrales de Monitoreo
```python
from docs.logs.system_monitor import system_monitor

# Cambiar umbral de CPU
system_monitor.set_threshold("cpu_usage", 85.0)

# Cambiar umbral de memoria
system_monitor.set_threshold("memory_usage", 80.0)
```

### Configurar Retención de Logs
```python
from docs.bitacoras.bitacora_manager import bitacora_manager

# Limpiar logs más antiguos de 30 días
bitacora_manager.cleanup_old_logs(retention_days=30)
```

### Personalizar Intervalos de Monitoreo
```python
from docs.logs.system_monitor import ICTSystemMonitor

# Monitor personalizado cada 15 segundos
custom_monitor = ICTSystemMonitor(monitoring_interval=15)
custom_monitor.start_monitoring()
```

## 📊 Dashboard y Visualización

### Estado en Tiempo Real
```python
# Resumen ejecutivo
from docs.logs.system_monitor import get_system_status

status = get_system_status()
print(f"""
🎯 Estado General: {status['overall_status']}
💻 CPU: {status['system_metrics']['cpu']['usage_percent']:.1f}%
🧠 Memoria: {status['system_metrics']['memory']['usage_percent']:.1f}%
⚠️ Alertas: {status['alerts']['active']}
""")
```

### Reporte de Salud Completo
```python
from docs.logs.system_monitor import get_health_report

health = get_health_report()
print(health)  # Reporte formateado completo
```

## 🔍 Análisis y Búsqueda

### Buscar Eventos Específicos
```python
import json
from pathlib import Path
from datetime import datetime

# Buscar todas las decisiones de trading de hoy
today = datetime.now().strftime("%Y-%m-%d")
trading_log = Path(f"docs/bitacoras/trading_decisions/trading_decisions_{today}.jsonl")

if trading_log.exists():
    with open(trading_log, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line.strip())
            if entry['data']['pattern'] == 'SILVER_BULLET':
                print(f"Silver Bullet: {entry['data']['direction']} @ {entry['data']['entry_price']}")
```

### Analizar Patrones Detectados
```python
# Ver todos los patrones detectados hoy
pattern_log = Path(f"docs/bitacoras/pattern_detection/pattern_detection_{today}.jsonl")

if pattern_log.exists():
    patterns = []
    with open(pattern_log, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line.strip())
            patterns.append(entry['data']['pattern_type'])

    print(f"Patrones detectados hoy: {set(patterns)}")
```

## 📚 Documentación Adicional

### Arquitectura del Sistema
📖 **[system_architecture.md](architecture/system_architecture.md)**
- Diagrama completo de componentes
- Flujos de datos
- Principios de diseño
- Guías de extensibilidad

### Manual de Bitácoras
📖 **[MANUAL_BITACORAS.md](MANUAL_BITACORAS.md)**
- Guía completa de uso
- Ejemplos de código
- Tipos de bitácoras
- APIs disponibles

### README Principal
📖 **[../README.md](../README.md)**
- Documentación general del ICT Engine
- Instalación y configuración
- Características principales
- Roadmap del proyecto

## 🆘 Troubleshooting

### Problema: No se crean bitácoras
```bash
# Verificar permisos
python -c "from pathlib import Path; Path('docs/bitacoras/test.txt').touch()"

# Re-inicializar sistema
python docs\init_documentation_system.py
```

### Problema: Monitor no inicia
```bash
# Instalar dependencias faltantes
pip install psutil

# Verificar imports
python -c "from docs.logs.system_monitor import system_monitor; print('OK')"
```

### Problema: Archivos de log muy grandes
```python
# Limpiar logs antiguos
from docs.bitacoras.bitacora_manager import bitacora_manager
bitacora_manager.cleanup_old_logs(retention_days=7)
```

## 📞 Soporte y Contacto

### Recursos de Ayuda
- 📊 **Estado del sistema**: `docs/logs/system_monitoring_*.json`
- 📋 **Bitácoras**: `docs/bitacoras/*/`
- 📄 **Reportes**: `docs/reports/`
- 🔍 **Logs de error**: `docs/bitacoras/error_tracking/`

### Reportar Problemas
1. 🔍 Revisar logs de error en `docs/bitacoras/error_tracking/`
2. 📊 Obtener estado del sistema con `get_health_report()`
3. 📋 Consultar bitácoras relevantes
4. 📄 Generar reporte de incidencia

---

## 🎉 ¡Sistema Listo!

Tu sistema de documentación ICT Engine v3.44 está completamente configurado y listo para usar.

**Próximos pasos recomendados:**
1. ✅ Ejecutar `init_documentation_system.py` (si no lo has hecho)
2. ✅ Probar con `ejemplo_uso_bitacoras.py`
3. ✅ Revisar el `MANUAL_BITACORAS.md`
4. ✅ Integrar con tu flujo de trading actual

**¡Happy Trading con ICT Engine! 🚀📈**
