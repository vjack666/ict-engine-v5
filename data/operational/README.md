# 📊 DATOS OPERACIONALES - README

## 🎯 **PROPÓSITO**
Esta carpeta contiene los **DATOS REALES** generados por el sistema ICT Engine v5.0 durante su operación.

## 📁 **ESTRUCTURA**

```
data/operational/
├── trading/               # Datos de trading operacionales
│   ├── decisions/        # Decisiones de trading (.jsonl)
│   ├── sessions/         # Análisis de sesiones (.jsonl)
│   └── risk/             # Gestión de riesgo (.jsonl)
├── analysis/             # Datos de análisis técnico
│   ├── patterns/         # Patrones ICT detectados (.jsonl)
│   ├── poi/              # Puntos de Interés (.jsonl)
│   └── performance/      # Métricas de rendimiento (.jsonl)
└── system_status/        # Estado del sistema (.jsonl)
```

## 📋 **FORMATO DE ARCHIVOS**

Todos los archivos son **JSONL** (JSON Lines) con formato:
- `nombre_YYYY-MM-DD.jsonl` para datos diarios
- Una línea JSON por evento/registro
- Timestamp ISO 8601 en cada línea

## 🔗 **DOCUMENTACIÓN**

La documentación técnica de cada tipo de datos está en `docs/bitacoras/`:
- `docs/bitacoras/trading_decisions.md`
- `docs/bitacoras/pattern_detection.md`
- `docs/bitacoras/poi_lifecycle.md`
- etc.

## 🎛️ **GENERADO POR**

- **Analysis Command Center (ACC)** - core/analysis_command_center/
- **ICT Engine** - core/ict_engine/
- **POI System** - core/poi_system/
- **Dashboard** - dashboard/

---
**Última actualización:** 2025-08-01
**Sistema:** ICT Engine v5.0
