# 🌙 HIBERNATION WIDGET v2.0 - BITÁCORA TÉCNICA COMPLETA

## 📋 **INFORMACIÓN GENERAL**

**Archivo**: `dashboard/hibernation_widget_v2.py`
**Versión**: v2.0 - Arquitectura Directa
**Fecha Creación**: Agosto 6, 2025
**Estado**: ✅ **COMPLETAMENTE OPERATIVO**
**Último Update**: Agosto 6, 2025 - Integración `registrar_accion` implementada

---

## 🎯 **PROPÓSITO Y FUNCIONALIDAD**

El **Hibernation Widget v2.0** es un componente especializado del dashboard que maneja:

- **🔍 Detección automática del estado del mercado** (abierto/cerrado/parcial)
- **🌙 Hibernación inteligente** durante horarios no operativos
- **📊 Monitoreo MT5** con verificación robusta de conexión
- **🎨 UI profesional** usando Rich components
- **📡 Coordinación con Dashboard Controller** mediante `registrar_accion`
- **📝 Logging exhaustivo** usando SLUC v2.0

---

## 🏗️ **ARQUITECTURA DIRECTA**

### **Principio de Diseño**
```
100% Infraestructura Existente - CERO Duplicación
```

### **Componentes Integrados**
```
└─► MT5 Manager (estado de conexión)
└─► Dashboard Controller (coordinación)
└─► Real Market Data (datos de mercado)
└─► SLUC Logging (monitoreo total)
└─► Rich UI (presentación profesional)
```

### **Patrón de Integración**
```python
# ✅ PATRÓN EXITOSO DEL POI INTEGRATION
from sistema.logging_interface import enviar_senal_log
from utils.mt5_data_manager import get_mt5_manager
from dashboard.dashboard_controller import get_dashboard_controller
```

---

## 🔧 **FUNCIONES PRINCIPALES**

### **1. `crear_panel_hibernacion_inteligente(dashboard_instance)`**

**Propósito**: Función principal que crea el panel de hibernación completo

**Flujo de Ejecución**:
1. 🔍 **Validación sistemas** (MT5 + Controller)
2. 📊 **Acceso a datos** (Real Market Data)
3. 🌐 **Estado MT5 y mercado**
4. 🎨 **Creación panel hibernación**
5. 📡 **Notificación al controller**

**Parámetros**:
- `dashboard_instance`: Instancia del dashboard principal con `real_market_data`

**Returns**: `Panel` - Panel Rich con estado de hibernación

### **2. `crear_contenido_hibernacion(market_status, trading_hours, current_price)`**

**Propósito**: Crea el contenido visual del panel con datos reales

**Estados Manejados**:
- 🌅 **MODO ACTIVO**: Sistema operativo - Trading habilitado
- 🌤️ **MODO PARCIAL**: Conexión parcial - Verificar MT5
- 🌙 **MODO HIBERNACIÓN**: Sistema en reposo - Esperando mercado

### **3. `determinar_horario_trading()`**

**Propósito**: Determina el horario de trading actual basado en hora y día

**Sesiones Detectadas**:
- 🌙 **Asia-Pacífico** (0-6h)
- 🌅 **Europea** (6-14h)
- 🌞 **Americana** (14-22h)
- 🌃 **Asia tardía** (22-24h)
- 📅 **Fin de semana** (sábados/domingos)

### **4. `crear_tabla_hibernacion_detallada(dashboard_instance)`**

**Propósito**: Alternativa tabular con diagnóstico completo del sistema

**Componentes Monitoreados**:
- MT5 Manager
- Dashboard Controller
- Market Data
- Sistema General

---

## 📊 **INTEGRACIÓN CON DASHBOARD CONTROLLER**

### **Método Clave: `registrar_accion`**

```python
controller.registrar_accion("HIBERNATION_STATUS_UPDATE", {
    'market_status': market_status,
    'current_price': current_price,
    'hibernation_active': True,
    'timestamp': datetime.now().isoformat(),
    'source': 'HIBERNATION_WIDGET_V2'
})
```

**Propósito de la Acción**:
- 📝 **Tracking** de cambios de estado del mercado
- 🔄 **Coordinación** del sistema hibernación
- 📊 **Métricas** de actividad del widget
- 🔍 **Debugging** de estados de hibernación

---

## 🌐 **ESTADOS DEL SISTEMA**

### **🟢 ACTIVO** (`market_status = "🟢 ACTIVO"`)
- **Condición**: MT5 conectado + Mercado operativo
- **UI**: Border verde, título verde
- **Acción**: "Sistema operativo - Trading habilitado"

### **🟡 PARCIAL** (`market_status = "🟡 PARCIAL"`)
- **Condición**: MT5 con errores + Mercado disponible
- **UI**: Border amarillo, título amarillo
- **Acción**: "Conexión parcial - Verificar MT5"

### **🔴 DESCONECTADO/NO DISPONIBLE**
- **Condición**: MT5 no disponible o sin conexión
- **UI**: Border azul, título azul
- **Acción**: "Sistema en reposo - Esperando mercado"

---

## 📝 **LOGGING EXHAUSTIVO**

### **Categorías de Logs**
```python
enviar_senal_log("INFO", "mensaje", __name__, "validation")      # Validación sistemas
enviar_senal_log("SUCCESS", "mensaje", __name__, "mt5_status")   # Estado MT5
enviar_senal_log("WARNING", "mensaje", __name__, "mt5_error")    # Errores MT5
enviar_senal_log("ERROR", "mensaje", __name__, "hibernation_error") # Errores críticos
enviar_senal_log("INFO", "mensaje", __name__, "controller_sync") # Sincronización
```

### **Eventos Monitoreados**
- ✅ Inicialización del módulo
- 🔍 Validación de sistemas
- 📊 Extracción de datos de mercado
- 🌐 Verificación estado MT5
- 🎨 Creación de paneles
- 📡 Sincronización con controller
- ❌ Manejo de errores

---

## 🔄 **MANEJO DE ERRORES**

### **Error Handling Robusto**
```python
try:
    # Operación principal
except Exception as e:
    error_msg = f"Error crítico en hibernación: {str(e)}"
    enviar_senal_log("CRITICAL", error_msg, __name__, "hibernation_error")
    return crear_panel_hibernacion_error(error_msg)
```

### **Fallbacks Implementados**
- **Panel de error** para problemas críticos
- **Tabla de error** para problemas de tabla
- **Estados por defecto** cuando no hay datos
- **Logging completo** de todos los errores

---

## 🎨 **COMPONENTES UI**

### **Panel Principal**
```python
Panel(
    content_text,
    title=f"🌙 Hibernación Inteligente",
    title_align="left",
    border_style=hibernation_color,
    padding=(1, 2),
    expand=False
)
```

### **Tabla Detallada**
```python
Table(
    title=f"🌙 Sistema Hibernación - {timestamp}",
    title_style="bold blue",
    header_style="bold white on blue",
    border_style="bright_blue",
    show_header=True,
    show_lines=True,
    expand=True
)
```

---

## ⚙️ **CONFIGURACIÓN Y DEPENDENCIAS**

### **Imports Esenciales**
```python
from sistema.logging_interface import enviar_senal_log
from utils.mt5_data_manager import get_mt5_manager
from dashboard.dashboard_controller import get_dashboard_controller
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
```

### **Dependencias del Sistema**
- ✅ **SLUC v2.0** - Logging centralizado
- ✅ **MT5 Data Manager** - Gestión MT5
- ✅ **Dashboard Controller** - Coordinación
- ✅ **Rich Library** - UI components
- ✅ **DateTime utilities** - Manejo temporal

---

## 📈 **MÉTRICAS Y PERFORMANCE**

### **Indicadores Clave**
- **Tiempo de respuesta** del widget
- **Tasa de éxito** en detección MT5
- **Frecuencia de cambios** de estado
- **Errores por sesión** de hibernación

### **Optimizaciones Implementadas**
- ✅ **Verificación lazy** de sistemas
- ✅ **Caching de estados** para UI responsiva
- ✅ **Error handling defensivo** para estabilidad
- ✅ **Logging selectivo** para performance

---

## 🔮 **ROADMAP Y MEJORAS FUTURAS**

### **Próximas Implementaciones**
- [ ] **Predicción inteligente** de próxima sesión
- [ ] **Alertas automáticas** de cambios de estado
- [ ] **Historial de hibernación** para análisis
- [ ] **Configuración personalizada** de horarios

### **Integraciones Planeadas**
- [ ] **WebSocket notifications** para tiempo real
- [ ] **Email alerts** para cambios críticos
- [ ] **Mobile push notifications**
- [ ] **Analytics dashboard** de hibernación

---

## ✅ **TESTING Y VALIDACIÓN**

### **Casos de Prueba**
- [x] ✅ **MT5 conectado + Mercado abierto**
- [x] ✅ **MT5 desconectado + Mercado abierto**
- [x] ✅ **MT5 cualquier estado + Mercado cerrado**
- [x] ✅ **Error en MT5 Manager**
- [x] ✅ **Error en Dashboard Controller**
- [x] ✅ **Sin datos de mercado**

### **Validación de Integración**
- [x] ✅ **SLUC Logging** funcionando
- [x] ✅ **Rich UI** renderizando correctamente
- [x] ✅ **Controller sync** operativo
- [x] ✅ **Error handling** robusto

---

## 📚 **DOCUMENTACIÓN RELACIONADA**

- [`DASHBOARD_H1_HIBERNACION.md`](./DASHBOARD_H1_HIBERNACION.md) - Pestaña hibernación principal
- [`REGISTRAR_ACCION_PROPOSITO_SISTEMA.md`](./REGISTRAR_ACCION_PROPOSITO_SISTEMA.md) - Integración controller
- [`DASHBOARD_IMPLEMENTACION_v6_PLAN_EJECUCION.md`](./DASHBOARD_IMPLEMENTACION_v6_PLAN_EJECUCION.md) - Roadmap general

---

**📊 Documentación actualizada por:** Hibernation Widget v2.0 Analysis System
**📅 Última actualización:** 6 de Agosto, 2025
**🎯 Estado:** DOCUMENTACIÓN COMPLETA Y ACTUALIZADA
**✅ Siguiente revisión:** Cuando se implementen mejoras v2.1
