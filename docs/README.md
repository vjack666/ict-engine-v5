# ICT Engine v5.0 - Sistema de Trading Profesional ICT

## 🎯 Descripción General

ICT Engine v5.0 es un sistema profesional de análisis y trading basado en la metodología Inner Circle Trader (ICT). Combina detección automática de patrones, análisis de estructura de mercado y gestión avanzada de riesgo para proporcionar señales de trading de alta probabilidad.

## 📚 **DOCUMENTACIÓN ORGANIZADA**

### **🔧 CONFIGURACIÓN**
- [`CONFIGURACION_VSCODE_MENOS_ESTRICTO.md`](configuracion/CONFIGURACION_VSCODE_MENOS_ESTRICTO.md) - Configuración optimizada de VS Code

### **📊 BITÁCORAS**
- [`BITACORA_CONFIGURACION_VSCODE.md`](bitacoras/BITACORA_CONFIGURACION_VSCODE.md) - Bitácora de configuración del entorno
- [`BITACORA_DIAGNOSTICO_DASHBOARD.md`](bitacoras/BITACORA_DIAGNOSTICO_DASHBOARD.md) - Diagnóstico del sistema dashboard
- [`BITACORA_SEGUIMIENTO_ICT.md`](bitacoras/BITACORA_SEGUIMIENTO_ICT.md) - Seguimiento del progreso del proyecto

### **📈 PLANIFICACIÓN**
- [`PLAN_TRABAJO_COMPLETO_ICT.md`](planificacion/PLAN_TRABAJO_COMPLETO_ICT.md) - Plan completo de desarrollo del proyecto

## 📊 **ESTADO ACTUAL DEL SISTEMA**

### ✅ **ÚLTIMAS ACTUALIZACIONES (01 Agosto 2025 - 19:30 hrs)**

**🔧 LOGGING SYSTEM COMPLETAMENTE CORREGIDO**
- ✅ Todas las categorías de logging corregidas en POI Black Box Diagnostics
- ✅ Logs guardándose correctamente en `data/logs/poi/`
- ✅ Sin errores SLUC ERROR - Dashboard ejecuta limpiamente
- ✅ Sistema de diagnósticos automáticos 100% funcional

**🎨 INTERFAZ VISUAL RESTAURADA**
- ✅ Pantalla "🔧 DEVELOPMENT MODE" recuperada (formato original)
- ✅ Grid POI con datos completos y formateado preferido
- ✅ Dashboard Multi-POI funcionando al 100% con interfaz hermosa
- ✅ Sistema de caja negra conservado y funcional

**📈 MÉTRICAS DE SISTEMA**
```
✅ Sistema POI: Funcionando al 100%
✅ Multi-POI Dashboard: Funcionando al 100%
✅ Dashboard Principal: Ejecutándose sin errores
✅ Sistema de Logs: Guardándose en data/logs/poi/
✅ Caja Negra ICT: POIs completamente integrados
✅ Logging Categories: 24 correcciones aplicadas exitosamente
```

---

## 🏗️ Arquitectura del Sistema

### Componentes Principales

```
ICT Engine v3.44/
├── core/                           # Motor principal del sistema
│   ├── ict_engine/                 # Lógica ICT core
│   │   ├── pattern_analyzer.py     # Analizador de patrones ICT
│   │   ├── ict_detector.py         # Detector de setups ICT
│   │   ├── confidence_engine.py    # Motor de confianza
│   │   └── veredicto_engine_v4.py  # Motor de decisiones
│   ├── poi_system/                 # Sistema de Puntos de Interés
│   │   ├── poi_detector.py         # Detector de POIs
│   │   └── poi_scoring_engine.py   # Sistema de puntuación
│   ├── analysis_command_center/    # Centro de comando de análisis
│   │   └── tct_pipeline/           # Pipeline de análisis técnico
│   └── risk_management/            # Gestión de riesgo
├── dashboard/                      # Interfaz de usuario
├── sistema/                        # Sistema base y logging
├── config/                         # Configuraciones
└── utils/                          # Utilidades
```

## 🔥 Características Principales

### 1. Detección Automática de Patrones ICT
- **Silver Bullet**: Patrón de máxima probabilidad (10:00-11:00 GMT)
- **Judas Swing**: Detección de manipulación matutina
- **Liquidity Grab**: Identificación de barridos de liquidez
- **Optimal Trade Entry (OTE)**: Entradas óptimas en retrocesos
- **Power of Three**: Patrones de distribución de NY

### 2. Sistema de POIs (Puntos de Interés)
- Order Blocks (Bullish/Bearish)
- Fair Value Gaps (FVG)
- Zonas de liquidez institucional
- Niveles de soporte/resistencia dinámicos
- Sistema de puntuación automático

### 3. Análisis de Estructura de Mercado
- Identificación de fases de mercado (Acumulación, Manipulación, Distribución)
- Análisis de tendencia primaria y secundaria
- Evaluación de calidad estructural
- Detección de cambios de character

### 4. Gestión Avanzada de Riesgo
- Cálculo automático de Risk:Reward
- Ajuste dinámico de posiciones
- Múltiples niveles de take profit
- Stop loss inteligente basado en estructura

### 5. Sistema de Logging Centralizado (SLUC v2.0)
- Logging estructurado con categorías
- Registros de rendimiento en tiempo real
- Bitácoras de decisiones del sistema
- Logs de errores y debugging

## 🎮 Uso del Sistema

### Inicialización
```python
from core.ict_engine.pattern_analyzer import ICTPatternAnalyzer
from core.poi_system.poi_detector import POIDetector

# Inicializar componentes
analyzer = ICTPatternAnalyzer()
poi_detector = POIDetector()

# Actualizar datos
analyzer.update_data(current_price, pois, candles_data)

# Realizar análisis
result = analyzer.analyze_current_structure()
```

### Interpretación de Resultados
```python
# Acceder a señal principal
primary_signal = result.primary_signal
print(f"Patrón: {primary_signal.pattern.value}")
print(f"Dirección: {primary_signal.direction.value}")
print(f"Fortaleza: {primary_signal.strength}%")

# Plan de acción
for step in primary_signal.action_plan:
    print(step)
```

## 📊 Tipos de Señales

### Fortaleza de Señal
- **HIGH (80-95%)**: Señales de máxima confianza
- **MEDIUM (60-79%)**: Señales moderadas
- **LOW (40-59%)**: Señales de baja confianza

### Patrones Detectados
1. **Silver Bullet** (75-95% fortaleza)
2. **Judas Swing** (70-88% fortaleza)
3. **Liquidity Grab** (80-92% fortaleza)
4. **Optimal Trade Entry** (65-85% fortaleza)
5. **Power of Three** (70-90% fortaleza)

## 🕐 Contexto Temporal

### Sesiones de Trading
- **Asian Session**: 00:00-08:00 GMT (Acumulación)
- **London Session**: 08:00-16:00 GMT (Manipulación/Distribución)
- **NY Session**: 13:00-21:00 GMT (Distribución)
- **London-NY Overlap**: 13:00-16:00 GMT (Máxima liquidez)

### Ventanas Críticas
- **Silver Bullet**: 10:00-11:00 GMT
- **Judas Swing**: Primeras 2-3 horas de sesión principal
- **Power of Three**: 13:30-15:00 GMT (NY)

## ⚙️ Configuración

### Variables de Entorno
```python
# config/config.py
SYMBOL = "EURUSD"
TIMEFRAMES = ["M1", "M5", "M15", "H1"]
MIN_SIGNAL_STRENGTH = 60.0
MAX_SIGNALS_PER_ANALYSIS = 3
```

### Logging
```python
# sistema/logging_config.py
LOG_LEVEL = "INFO"
LOG_FORMAT = "structured"
ENABLE_EMOJI_LOGS = True
```

## 🔧 Mantenimiento

### Monitoreo del Sistema
- Verificar logs en `docs/logs/`
- Revisar bitácoras en `docs/bitacoras/`
- Monitorear rendimiento en dashboard

### Troubleshooting
1. **Señales débiles**: Verificar calidad de POIs
2. **Errores de conexión**: Revisar configuración MT5
3. **Logs faltantes**: Verificar permisos de escritura

## 📈 Métricas de Rendimiento

### KPIs del Sistema
- **Precisión de Señales**: Target >75%
- **Risk:Reward Promedio**: Target >1:2
- **Tiempo de Respuesta**: <500ms
- **Uptime del Sistema**: >99%

## 🚀 Roadmap

### v3.45 (Próxima)
- [ ] Integración con múltiples brokers
- [ ] ML para optimización de patrones
- [ ] API REST para acceso externo
- [ ] Dashboard web avanzado

### v4.0 (Futuro)
- [ ] Trading automatizado completo
- [ ] Backtesting histórico
- [ ] Optimización genética de parámetros
- [ ] Clustering de patrones

## 📞 Soporte

Para soporte técnico o reportar bugs:
- Revisar logs en `docs/logs/system_status.log`
- Consultar bitácoras en `docs/bitacoras/`
- Verificar documentación en `docs/architecture/`

---

**ICT Engine v5.0** - Desarrollado con metodología Inner Circle Trader
*Última actualización: 01 Agosto 2025 - Sistema de Logging Corregido*
