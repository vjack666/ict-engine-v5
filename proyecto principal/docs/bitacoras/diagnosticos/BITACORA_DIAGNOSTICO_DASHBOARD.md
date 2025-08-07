# 🔍 Sistema de Diagnóstico Visual para Dashboard Textual - CHECKLIST COMPLETO

**Sistema:** TEXTUAL DASHBOARD DIAGNOSTIC FRAMEWORK
**Fecha de Creación:** 1 de Agosto 2025
**Objetivo:** Implementar herramientas de diagnóstico profesionales para resolver el problema de "letras desordenadas" y establecer un workflow de debugging robusto para el desarrollo del dashboard.

---

## 📋 RESUMEN DEL PROGRESO

- **Fases Completadas:** 0 / 3
- **Tareas Completadas:** 5 / 30
- **Tiempo Estimado Restante:** 4-6 horas de implementación

---

## ⚙️ COMPONENTES CENTRALES Y ESTADO ACTUAL

### **✅ INFRAESTRUCTURA EXISTENTE**
- [x] **Dashboard Textual:** `dashboard_definitivo.py` implementado y funcional
- [x] **Sistema de Logging:** SLUC v2.0 con logging estructurado activo
- [x] **Sistema de Señales:** `enviar_senal_log()` implementado y usado
- [x] **Debug Mode:** Binding "D" para toggle debug implementado
- [x] **🆕 Logging Centralizado:** Sistema de eventos JSONL funcionando

### **⚠️ PROBLEMAS IDENTIFICADOS**
- [x] **Print Statements:** 20+ usos de `print()` encontrados en dashboard
- [x] **Logging Directo:** Múltiples llamadas a `logging.getLogger()` y `logging.basicConfig()`
- [x] **Output Bypass:** Evidencia de texto desordenado por bypass del renderizado Textual
- [ ] **🆕 Sin Launcher Dedicado:** No hay script específico para modo debug
- [ ] **🆕 Sin DevTools Integration:** F12 y herramientas de desarrollador no configuradas

---

## 🔧 FASE 1: ACTIVACIÓN DE HERRAMIENTAS DE DESARROLLADOR NATIVAS

*Implementar las herramientas de debugging profesionales de Textual para diagnóstico en tiempo real.*

### **🧠 Configuración del Sistema (Backend)**

- [ ] **Script de Launcher Dedicado:** Crear `dashboard/debug_launcher.py` con argumentos `--dev`
- [ ] **Modificación App Principal:** Adaptar `SentinelDashboardDefinitivo` para aceptar modo console
- [ ] **Flag DevMode:** Implementar detección automática de `--dev` en argumentos de sistema
- [ ] **🆕 Console Mode:** Configurar `app.run(headless=False, console=True)` para modo debug
- [ ] **🆕 Screenshot Capability:** Integrar herramientas de captura de pantalla para documentación

### **🎨 Activación DevTools (Frontend)**

- [ ] **Tecla F12:** Verificar que F12 abre DevTools nativos de Textual
- [ ] **Dom Inspector:** Configurar inspector DOM para análisis de widgets
- [ ] **CSS Live Editor:** Activar editor de CSS en tiempo real
- [ ] **Console Logger:** Configurar redirección de logs al DevTools console
- [ ] **🆕 Performance Monitor:** Activar monitoreo de rendering en tiempo real

---

## 🔍 FASE 2: AUDITORÍA Y LIMPIEZA DE CÓDIGO

*Identificar y reemplazar sistemáticamente todo output directo que pueda causar corrupciones visuales.*

### **🧠 Búsqueda y Catalogación (Backend)**

- [x] **Búsqueda de Print:** 20+ ocurrencias de `print()` identificadas en dashboard
- [x] **Búsqueda de Logging:** Múltiples `logging.` directos encontrados
- [ ] **Categorización A:** Listar todos los `print()` de debugging para reemplazo
- [ ] **Categorización B:** Listar output de información para migrar a widgets
- [ ] **Categorización C:** Listar output de error para integrar al sistema de señales
- [ ] **🆕 Audit Report:** Generar reporte completo con líneas específicas y archivos

### **🎨 Implementación de Reemplazos (Frontend)**

- [ ] **Patrón de Reemplazo Estándar:** Definir template para migración `print()` → `enviar_senal_log()`
- [ ] **Reemplazo Sistemático:** Migrar todos los print de debugging encontrados
- [ ] **Widget Integration:** Convertir output de información a Static widgets
- [ ] **Error Integration:** Integrar errores al sistema de señales existente
- [ ] **🆕 Validation Script:** Crear script para verificar que no queden print() directos

---

## 🛠️ FASE 3: SISTEMA DE LOGGING INTEGRADO

*Implementar herramientas avanzadas de debugging y visualización para desarrollo futuro.*

### **🧠 Debug Widget Integrado (Backend)**

- [ ] **Debug Tab:** Crear nueva pestaña "🐞 Debug" en el dashboard principal
- [ ] **RichLog Widget:** Implementar `RichLog` de Textual para log viewer en tiempo real
- [ ] **Filtros de Log:** Sistema de filtros por nivel (DEBUG, INFO, WARNING, ERROR)
- [ ] **🆕 Filtros por Componente:** Filtrar logs por emisor específico
- [ ] **🆕 Performance Metrics:** Mostrar métricas de rendering y actualización

### **🎨 Herramientas de Desarrollo (Frontend)**

- [ ] **Log Viewer Interface:** Panel interactivo para navegar logs históricos
- [ ] **Real-time Updates:** Actualización automática del log viewer
- [ ] **Export Functionality:** Exportar logs filtrados para análisis externo
- [ ] **🆕 Screenshot Integration:** Capturar pantallas automáticamente en errores
- [ ] **🆕 Timeline View:** Vista temporal de eventos para análisis de secuencia

---

## 📊 CHECKLIST DETALLADO POR COMPONENTE

### ✅ **INFRAESTRUCTURA BASE**
- [x] Sistema Textual implementado (`SentinelDashboardDefinitivo`)
- [x] Sistema de logging SLUC v2.0 activo
- [x] Función `enviar_senal_log()` disponible y funcional
- [x] Debug mode binding ("D") implementado
- [x] Logs estructurados JSONL funcionando
- [x] Sistema de señales de logging centralizado
- [x] 20+ puntos de print() identificados para corrección

### ⏳ **HERRAMIENTAS DE DESARROLLADOR**
- [ ] Script `debug_launcher.py` creado
- [ ] Argument parsing para `--dev` implementado
- [ ] Modo console activado en Textual app
- [ ] DevTools F12 funcional y documentado
- [ ] DOM Inspector accesible y configurado
- [ ] CSS Live Editor activado
- [ ] Performance monitoring habilitado

### ⏳ **AUDITORÍA DE CÓDIGO**
- [x] Búsqueda sistemática de `print()` completada
- [x] Búsqueda de `logging.` directo completada
- [ ] Categorización completa de hallazgos
- [ ] Reporte de auditoría generado
- [ ] Patrón de reemplazo definido
- [ ] Script de validación automatizada
- [ ] Documentation de mejores prácticas

### ⏳ **LIMPIEZA Y MIGRACIÓN**
- [ ] Migración de prints de debugging a `enviar_senal_log()`
- [ ] Conversión de output informativo a widgets Static
- [ ] Integración de errores al sistema de señales
- [ ] Validación de zero prints directos
- [ ] Testing de rendering limpio
- [ ] Performance testing post-migración

### ⏳ **DEBUG WIDGET INTEGRADO**
- [ ] Tab "🐞 Debug" creada en dashboard
- [ ] `RichLog` widget implementado
- [ ] Sistema de filtros por nivel implementado
- [ ] Filtros por componente/emisor añadidos
- [ ] Real-time log updates funcionando
- [ ] Export de logs implementado
- [ ] Screenshots automáticos en errores

### ⏳ **HERRAMIENTAS AVANZADAS**
- [ ] Timeline view de eventos implementado
- [ ] Performance metrics dashboard
- [ ] Automated error detection
- [ ] Log analysis tools
- [ ] Development workflow documented
- [ ] Error reproduction scripts

---

## 🔧 SCRIPTS Y COMANDOS NECESARIOS

### **Scripts de Debug**
```powershell
# debug_dashboard.ps1
Set-Location "c:\Users\v_jac\Desktop\itc engine v5.0"
python dashboard\debug_launcher.py --dev

# audit_output.ps1
grep -r "print(" dashboard/ --include="*.py" | Out-File -FilePath "audit_print.txt"
grep -r "logging\." dashboard/ --include="*.py" | Out-File -FilePath "audit_logging.txt"

# validate_clean.ps1
$printCount = (Select-String -Pattern "print\(" -Path "dashboard\*.py" -Exclude "*debug*").Count
if ($printCount -eq 0) { Write-Host "✅ Zero prints directos" } else { Write-Host "❌ $printCount prints encontrados" }
```

### **Comandos de Validación**
```bash
# Búsqueda de problemas
python -c "import dashboard.dashboard_definitivo; print('✅ Import successful')"

# Screenshot para documentación
python -c "from textual.app import App; App().save_screenshot('dashboard_debug.svg')"

# Testing de rendering
python dashboard/debug_launcher.py --dev --test-rendering
```

---

## 📈 CRITERIOS DE ÉXITO Y MÉTRICAS

### **Fase 1 - Herramientas de Desarrollador**
- ✅ DevTools F12 funcionando
- ✅ Debug launcher ejecutándose sin errores
- ✅ Console mode mostrando logs en tiempo real
- ✅ Performance monitor activo y reportando métricas

### **Fase 2 - Auditoría y Limpieza**
- ✅ Zero apariciones de `print()` directo en código de producción
- ✅ Todos los outputs redirigidos al sistema de logging estructurado
- ✅ Rendering limpio durante 10+ ciclos de actualización consecutivos
- ✅ Tiempo de actualización mantenido < 200ms

### **Fase 3 - Sistema Integrado**
- ✅ Debug tab funcional con log viewer en tiempo real
- ✅ Filtros de logging operativos y eficientes
- ✅ Export de logs y screenshots automatizados
- ✅ Workflow de debugging documentado y validado

---

## 🎯 **PROBLEMAS ESPECÍFICOS IDENTIFICADOS**

### **🔴 CRÍTICOS (Prioridad Inmediata)**
```python
# dashboard_definitivo.py - Líneas problemáticas identificadas:
# Línea 67:   print(f"❌ ERROR CRÍTICO configurando paths de Python: {e}")
# Línea 312:  print("💼 Trading Core conectado exitosamente")
# Línea 314:  print(f"⚠️ Trading Core no disponible: {e}")
# Línea 327:  print("✅ Managers especializados conectados")
# Línea 344:  print("📊 Sistema de logging inteligente conectado")
# Línea 351-356: Múltiples prints de inventario de especialistas
```

### **🟡 MEDIOS (Prioridad Alta)**
```python
# Logging directo que puede causar conflictos:
# Línea 102-111: logging.basicConfig() conflictua con SLUC v2.0
# Línea 349: self.logger = logging.getLogger(__name__) duplica logging
```

### **🟢 BAJOS (Prioridad Media)**
```python
# ict_professional_widget.py:
# Línea 687: print(f"Error en sonda B: {e}") - error handling
```

---

## 🚀 PLAN DE IMPLEMENTACIÓN INMEDIATA

### **Sprint 1: Setup Herramientas (1-2 días)**
1. **Crear `debug_launcher.py`** con soporte para `--dev`
2. **Activar DevTools F12** y verificar funcionamiento
3. **Configurar console mode** en aplicación Textual
4. **Documentar workflow** de debugging

### **Sprint 2: Limpieza Crítica (1-2 días)**
1. **Migrar todos los prints críticos** a `enviar_senal_log()`
2. **Eliminar logging.basicConfig()** conflictivo
3. **Validar rendering limpio** sin corrupciones
4. **Testing intensivo** de actualizaciones

### **Sprint 3: Debug Widget (1-2 días)**
1. **Implementar tab Debug** con RichLog
2. **Añadir filtros** por nivel y componente
3. **Integrar export** de logs
4. **Screenshots automáticos** en errores

---

## 🔍 **VALIDACIÓN FINAL**

### **Tests de Aceptación**
- [ ] **Zero Corruption Test:** 50 actualizaciones consecutivas sin texto desordenado
- [ ] **Performance Test:** Tiempo de actualización consistente < 200ms
- [ ] **DevTools Test:** F12 abre herramientas funcionales
- [ ] **Debug Workflow Test:** Error reproduction reproducible en < 30 segundos

### **Documentación Requerida**
- [ ] **Debug Workflow Guide:** Paso a paso para debugging futuro
- [ ] **Tool Reference:** Referencia completa de herramientas disponibles
- [ ] **Troubleshooting Guide:** Soluciones a problemas comunes
- [ ] **Performance Benchmarks:** Métricas antes/después de implementación

---

## 💡 **VALOR AGREGADO DEL SISTEMA**

### **Beneficios Inmediatos**
- **🔧 Debugging Profesional:** Herramientas de desarrollador robustas
- **🎯 Resolución Rápida:** Identificación de problemas en < 30 segundos
- **📊 Monitoreo en Tiempo Real:** Visibilidad completa del sistema
- **🛡️ Prevención de Errores:** Workflow que previene problemas futuros

### **Beneficios a Largo Plazo**
- **🚀 Desarrollo Acelerado:** Debugging más eficiente
- **📈 Calidad Mejorada:** Menos bugs en producción
- **👥 Escalabilidad de Equipo:** Herramientas estándar para todos los desarrolladores
- **🔄 Mantenimiento Simplificado:** Herramientas de diagnóstico permanentes

---

*Última actualización: 1 de Agosto 2025*
*Estado: 17% Completado - Infraestructura Base Identificada*
*Próxima acción: Implementar debug_launcher.py y activar DevTools*
