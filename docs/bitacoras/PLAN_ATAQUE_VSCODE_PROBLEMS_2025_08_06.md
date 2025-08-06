# 🎯 PLAN DE ATAQUE - RESOLUCIÓN VS CODE PROBLEMS

**Fecha:** 06 Agosto 2025
**Objetivo:** Llegar a **0 errores** en la pestaña Problems de VS Code
**Estado:** � **EJECUTANDO FASE 1** - Limpieza Arquitectural Iniciada
**Estrategia:** Arquitectura dual **SLUC v2.1 (Logs) + SIC v2.0 (Imports)**

---

## 📊 ANÁLISIS INICIAL - ESTADO DEL PROYECTO

### 🔍 DIAGNÓSTICO COMPLETO
- **Total errores VS Code:** 465 problemas críticos
- **Archivo principal:** `dashboard/dashboard_definitivo.py` (465 errores)
- **Causa raíz:** Referencias incorrectas a `sistema.sic.py` obsoleto
- **Sistema objetivo:** Usar `sistema.imports_interface.py` (ImportsCentral)

### 📋 BITÁCORA DE ARCHIVOS ACTUALIZADA

**✅ ARCHIVOS FUNCIONALES Y ESTABLES:**
- `sistema/imports_interface.py` - **SIC v2.0** (ImportsCentral) ✅
- `sistema/logging_interface.py` - **SLUC v2.1** (enviar_senal_log) ✅

**❌ ARCHIVOS PROBLEMÁTICOS IDENTIFICADOS:**
- `dashboard/dashboard_definitivo.py` - **465 errores** ❌
- `sistema/sic.py` - **Archivo obsoleto** causando conflictos ❌
- `dashboard/problems_tab_renderer.py` - **Referencias incorrectas** ❌
- `utils/system_diagnostics.py` - **Imports de sic.py obsoleto** ❌
- `utils/mt5_data_manager.py` - **Imports incorrectos** ❌

---

## 🚨 CLASIFICACIÓN DE ERRORES POR PRIORIDAD

### 🔴 CRÍTICO - ARQUITECTURA (20 errores principales)
1. **Import duplicado de sys** (línea 31)
2. **Import duplicado de Path** (línea 185)
3. **enviar_senal_log undefined** (múltiples líneas - más de 50 referencias)
4. **Referencias a sistema.sic obsoleto** en lugar de imports_interface.py
5. **get_ict_components missing** desde ImportsCentral

### 🟡 MEDIO - SINTAXIS (150+ errores)
6. **Textual components undefined** (App, Binding, etc.)
7. **TCT Interface syntax error** (línea 154)
8. **Logger import symbols** incorrectos
9. **Undefined variables** en cadenas de imports fallback

### 🟢 BAJO - LIMPIEZA (295+ errores)
10. **Imports no utilizados**
11. **Comentarios malformados**
12. **Variables sin definir** en secciones de fallback

---

## 🤖 HERRAMIENTAS DE AUTOMATIZACIÓN DISPONIBLES

### **🎯 ARSENAL DE SCRIPTS AUTOMATIZADOS IDENTIFICADOS:**

#### **⭐⭐⭐⭐⭐ NIVEL CRÍTICO - USO INMEDIATO**

**1. `scripts/activate_import_fixer.py` + `scripts/fix_unused_imports.py`**
```bash
# Activación automática con menú interactivo
./fix_imports.ps1
# O directamente:
python scripts/activate_import_fixer.py
```
- **Función:** Corrector automático de imports no utilizados con backup
- **Características:** Detección automática, corrección con backup, modo dry-run, reportes detallados
- **Aplicación:** **FASE 1** (checks 1.1, 1.2) - Eliminar imports duplicados automáticamente
- **Target esperado:** -100 errores (imports duplicados y no utilizados)

**2. `scripts/migrador_inteligente_v2.py`**
```bash
python scripts/migrador_inteligente_v2.py --target dashboard/dashboard_definitivo.py
```
- **Función:** Migración inteligente al SIC v2.0 con análisis semántico
- **Características:** Imports precisos basados en uso real, preservación de funcionalidad
- **Aplicación:** **FASE 2** (checks 2.1, 2.2, 2.5) - Migrar a ImportsCentral automáticamente
- **Target esperado:** -120 errores (migración a imports_interface.py)

**3. `scripts/corrector_imports_problematicos.py`**
```bash
python scripts/corrector_imports_problematicos.py
```
- **Función:** Corrige imports específicos que no existen en SIC
- **Características:** Mapeo automático de imports problemáticos, reemplazo masivo
- **Aplicación:** **FASE 1-2** (checks 1.4, 1.7, 2.8) - Corregir referencias incorrectas
- **Target esperado:** -50 errores (imports problemáticos corregidos)

#### **⭐⭐⭐⭐ NIVEL ALTO - USO ESTRATÉGICO**

**4. `scripts/fase3_eliminar_imports.py`**
```bash
python scripts/fase3_eliminar_imports.py --execute
```
- **Función:** Reemplazo masivo de imports dispersos con SIC
- **Características:** Patrones de reemplazo automático, backup y rollback
- **Aplicación:** **FASE 2-3** (checks 2.5, 3.1, 3.2, 3.3) - Unificar imports
- **Target esperado:** -80 errores (unificación de imports)

**5. `scripts/detectar_imports_viejos.py`**
```bash
python scripts/detectar_imports_viejos.py
```
- **Función:** Detecta archivos con imports obsoletos no migrados
- **Características:** Encuentra imports viejos, identifica archivos problemáticos
- **Aplicación:** **FASE 3** (checks 3.4, 3.6) - Detectar archivos pendientes
- **Target esperado:** -30 errores (archivos auxiliares detectados)

#### **⭐⭐⭐ NIVEL MEDIO - USO DIAGNÓSTICO**

**6. `scripts/check_os_imports.py` + `scripts/check_subprocess_imports.py`**
```bash
python scripts/check_os_imports.py
python scripts/check_subprocess_imports.py
```
- **Función:** Verificación específica de imports de módulos sistema
- **Aplicación:** **FASE 4** (checks 4.6, V5) - Validación final
- **Target esperado:** -10 errores (imports específicos verificados)

---

## 🚀 ESTRATEGIA DE AUTOMATIZACIÓN INTEGRADA

### **⚡ SECUENCIA DE AUTOMATIZACIÓN RECOMENDADA:**

#### **🔧 FASE 1 AUTOMATIZADA (15 min → 8 min):**
```bash
# 1. Análisis inicial y limpieza automática
python scripts/activate_import_fixer.py  # Opción 2: Dry-run
python scripts/activate_import_fixer.py  # Opción 3: Corrección automática

# 2. Corrección de imports problemáticos
python scripts/corrector_imports_problematicos.py

# Target: 465 → 315 errores (-150) [Mejor que manual: -200]
```

#### **🔗 FASE 2 AUTOMATIZADA (10 min → 5 min):**
```bash
# 1. Migración inteligente a ImportsCentral
python scripts/migrador_inteligente_v2.py --target dashboard/dashboard_definitivo.py

# 2. Reemplazo masivo de imports restantes
python scripts/fase3_eliminar_imports.py --execute

# Target: 315 → 115 errores (-200) [Mejor que manual: -150]
```

#### **📁 FASE 3 AUTOMATIZADA (8 min → 4 min):**
```bash
# 1. Detectar archivos con imports viejos
python scripts/detectar_imports_viejos.py

# 2. Procesar archivos auxiliares identificados
python scripts/migrador_inteligente_v2.py --target utils/system_diagnostics.py
python scripts/migrador_inteligente_v2.py --target utils/mt5_data_manager.py

# Target: 115 → 25 errores (-90) [Similar a manual: -100]
```

#### **✅ FASE 4 AUTOMATIZADA (5 min → 3 min):**
```bash
# 1. Validación automática de imports específicos
python scripts/check_os_imports.py
python scripts/check_subprocess_imports.py

# 2. Test funcional automatizado
python dashboard/dashboard_definitivo.py --test-mode

# Target: 25 → 0 errores (-25) [Mejor que manual: -15]
```

### **📊 MÉTRICAS DE AUTOMATIZACIÓN:**

#### **Tiempo Total:** 55 min → **20 min** (64% reducción)
#### **Precisión:** Manual vs Automatizada
- **Manual estimada:** 465 → 0 errores (465 correcciones)
- **Automatizada:** 465 → 0 errores (465+ correcciones + validaciones)
- **Ventaja:** Mayor precisión, menos errores humanos, backups automáticos

#### **Comandos de Ejecución Secuencial:**
```bash
# EJECUCIÓN COMPLETA AUTOMATIZADA (20 minutos)
echo "🚀 INICIANDO CORRECCIÓN AUTOMATIZADA VS CODE PROBLEMS"

# FASE 1: Limpieza Automática (8 min)
python scripts/activate_import_fixer.py --auto-fix
python scripts/corrector_imports_problematicos.py

# FASE 2: Migración Inteligente (5 min)
python scripts/migrador_inteligente_v2.py --target dashboard/dashboard_definitivo.py
python scripts/fase3_eliminar_imports.py --execute

# FASE 3: Archivos Auxiliares (4 min)
python scripts/detectar_imports_viejos.py
python scripts/migrador_inteligente_v2.py --batch-mode

# FASE 4: Validación Final (3 min)
python scripts/check_os_imports.py
python scripts/check_subprocess_imports.py
python dashboard/dashboard_definitivo.py --test-mode

echo "✅ CORRECCIÓN AUTOMATIZADA COMPLETADA"
```

---

## ⚡ ESTRATEGIA DE RESOLUCIÓN - 4 FASES

### **FASE 1: LIMPIEZA ARQUITECTURAL** 🔧 (20 min - Prioridad MÁXIMA)

#### **Objetivo:** Eliminar imports duplicados y configurar base sólida
#### **Archivos a modificar:**
- `dashboard/dashboard_definitivo.py` (archivo principal)

#### **Acciones específicas:**
1. **Eliminar import duplicado de sys** (línea 31)
2. **Eliminar import duplicado de Path** (línea 185)
3. **Reemplazar ALL referencias `from sistema.sic`** por `from sistema.imports_interface`
4. **Configurar enviar_senal_log** desde ImportsCentral correctamente
5. **Verificar configuración de paths Python** al inicio del archivo

#### **Resultado esperado:** -200 errores (de 465 a ~265)

---

### **FASE 2: CORRECCIÓN DE IMPORTS** 🔗 (15 min - Prioridad ALTA)

#### **Objetivo:** Unificar sistema de imports usando SOLO ImportsCentral
#### **Archivos a modificar:**
- `dashboard/dashboard_definitivo.py` (imports principales)
- Verificar referencias en otros archivos

#### **Acciones específicas:**
1. **Usar SOLO ImportsCentral** para todos los imports del sistema
2. **Eliminar fallbacks problemáticos** a sic.py
3. **Configurar Textual imports** con fallback robusto
4. **Corregir TCT Interface import** (línea 154)
5. **Agregar función get_ict_components** si falta en ImportsCentral

#### **Resultado esperado:** -150 errores (de ~265 a ~115)

---

### **FASE 3: ARCHIVOS AUXILIARES** 📁 (10 min - Prioridad MEDIA)

#### **Objetivo:** Actualizar archivos dependientes para usar la nueva arquitectura
#### **Archivos a modificar:**
- `utils/system_diagnostics.py`
- `dashboard/problems_tab_renderer.py`
- `utils/mt5_data_manager.py`

#### **Acciones específicas:**
1. **system_diagnostics.py:** Cambiar `from sistema.sic` → `from sistema.imports_interface`
2. **problems_tab_renderer.py:** Actualizar imports y referencias
3. **mt5_data_manager.py:** Corregir imports incorrectos
4. **Verificar sintaxis** en todos los archivos modificados

#### **Resultado esperado:** -100 errores (de ~115 a ~15)

---

### **FASE 4: VALIDACIÓN Y TESTING** ✅ (10 min - Prioridad CRÍTICA)

#### **Objetivo:** Verificar que el sistema funciona sin errores
#### **Acciones de validación:**
1. **Ejecutar dashboard** sin errores críticos
2. **Verificar contador Problems = 0** en VS Code
3. **Validar ambos sistemas** (SLUC + SIC) funcionando
4. **Testing funcional básico** del dashboard
5. **Documentar resultados** en bitácora

#### **Resultado esperado:** 0 errores - Sistema completamente funcional

---

## 📝 DIRECTRICES PARA CREACIÓN DE ARCHIVOS

**🚨 POLÍTICA:** Solo crear archivos nuevos si es ABSOLUTAMENTE necesario

**Condiciones para crear nuevo archivo:**
- **POR QUÉ:** Explicar problema específico que no se puede resolver con corrección
- **PARA QUÉ:** Describir exactamente qué funcionalidad proporcionará
- **ALTERNATIVAS:** Demostrar que la corrección directa no es viable

**Archivos que NO se crearán (salvo emergencia):**
- Wrappers de compatibilidad innecesarios
- Duplicados de funcionalidad existente
- Parches temporales que oculten problemas estructurales

---

## 🎯 MÉTRICAS DE ÉXITO

### **Indicadores Principales:**
- **VS Code Problems:** 0 errores
- **Dashboard startup:** Sin errores críticos
- **Import warnings:** Máximo 5 warnings aceptables
- **Functional testing:** 100% componentes básicos funcionando

### **Indicadores Secundarios:**
- **Performance:** Sin degradación en tiempo de carga
- **Memory usage:** Sin leaks de memoria detectados
- **Code quality:** Imports limpios y organizados
- **Documentation:** Bitácora actualizada con todos los cambios

---

## 📊 TRACKING DE PROGRESO

### **Estado Inicial:**
- ❌ **465 errores** en VS Code Problems
- ❌ Dashboard con errores de startup
- ❌ Referencias incorrectas a sistema obsoleto

### **Objetivo Final:**
- ✅ **0 errores** en VS Code Problems
- ✅ Dashboard iniciando correctamente
- ✅ Arquitectura dual SLUC + SIC funcionando

### **Checkpoints de Validación Específicos:**

#### 🔧 **FASE 1: LIMPIEZA ARQUITECTURAL**
- [ ] **1.1** Eliminar `import sys` duplicado (línea 31) - Target: -1 error
- [ ] **1.2** Eliminar `from pathlib import Path` duplicado (línea 185) - Target: -1 error
- [ ] **1.3** Reemplazar `from sistema.sic import` → `from sistema.imports_interface import` (5+ líneas) - Target: -50 errores
- [ ] **1.4** Configurar `enviar_senal_log` desde `get_logging()` de ImportsCentral - Target: -50 errores
- [ ] **1.5** Verificar paths Python al inicio del archivo funcionan correctamente - Target: -0 errores
- [ ] **1.6** Verificar que `sistema.imports_interface` se importa correctamente - Target: -20 errores
- [ ] **1.7** Eliminar todas las referencias a `sistema.sic` obsoleto - Target: -30 errores
- [ ] **1.8** Configurar logging fallback cuando ImportsCentral no esté disponible - Target: -48 errores
- [ ] **✅ CHECKPOINT FASE 1:** De 465 → ~265 errores (Reducción: 200 errores)

#### 🔗 **FASE 2: CORRECCIÓN DE IMPORTS**
- [ ] **2.1** Importar `ImportsCentral` desde `sistema.imports_interface` - Target: -20 errores
- [ ] **2.2** Usar `get_ict_components()` en lugar de imports directos ICT - Target: -30 errores
- [ ] **2.3** Configurar Textual imports con try/except robusto - Target: -25 errores
- [ ] **2.4** Corregir syntax error en TCT Interface línea 154 - Target: -1 error
- [ ] **2.5** Eliminar imports fallback problemáticos a sic.py - Target: -20 errores
- [ ] **2.6** Configurar `App`, `Binding`, etc. desde Textual correctamente - Target: -30 errores
- [ ] **2.7** Verificar que `get_dashboard_components()` funciona - Target: -10 errores
- [ ] **2.8** Configurar logging unificado con `sic_log()` - Target: -9 errores
- [ ] **✅ CHECKPOINT FASE 2:** De ~265 → ~115 errores (Reducción: 150 errores)

#### 📁 **FASE 3: ARCHIVOS AUXILIARES**
- [ ] **3.1** `utils/system_diagnostics.py`: Cambiar imports sic.py → imports_interface.py - Target: -30 errores
- [ ] **3.2** `dashboard/problems_tab_renderer.py`: Actualizar imports y referencias - Target: -25 errores
- [ ] **3.3** `utils/mt5_data_manager.py`: Corregir imports incorrectos - Target: -20 errores
- [ ] **3.4** Verificar sintaxis en todos los archivos modificados - Target: -10 errores
- [ ] **3.5** Eliminar imports circulares si existen - Target: -5 errores
- [ ] **3.6** Verificar que no hay referencias rotas entre archivos - Target: -5 errores
- [ ] **3.7** Confirmar que `SmartDirectoryLogger` se obtiene correctamente - Target: -5 errores
- [ ] **3.8** Validar que todos los archivos auxiliares cargan sin errores - Target: -15 errores
- [ ] **✅ CHECKPOINT FASE 3:** De ~115 → ~15 errores (Reducción: 100 errores)

#### ✅ **FASE 4: VALIDACIÓN Y TESTING**
- [ ] **4.1** Ejecutar `python dashboard/dashboard_definitivo.py` sin errores críticos
- [ ] **4.2** Verificar VS Code Problems panel = 0 errores
- [ ] **4.3** Confirmar que ImportsCentral carga correctamente
- [ ] **4.4** Verificar que `enviar_senal_log` funciona desde SLUC v2.1
- [ ] **4.5** Testing básico: Dashboard UI aparece sin crashes
- [ ] **4.6** Verificar que no hay import warnings críticos (máximo 5 aceptables)
- [ ] **4.7** Confirmar que la arquitectura dual SLUC+SIC funciona
- [ ] **4.8** Validar que `get_system_status()` retorna datos válidos
- [ ] **4.9** Testing funcional: Navegación básica en dashboard
- [ ] **4.10** Verificar que no hay memory leaks evidentes
- [ ] **4.11** Confirmar performance aceptable (carga < 10 segundos)
- [ ] **4.12** Documentar resultados finales en bitácora
- [ ] **✅ CHECKPOINT FASE 4:** 0 errores - 🎉 **ÉXITO TOTAL**

---

### **Métricas Específicas de Progreso:**

#### **Contadores de Errores por Categoría:**
```
Estado Inicial:
├── 🔴 Import Errors: ~150 errores
├── 🟡 Undefined Variables: ~200 errores
├── 🟢 Syntax Errors: ~50 errores
├── 🔵 Type Errors: ~35 errores
├── 🟣 Reference Errors: ~30 errores
└── 📊 TOTAL: 465 errores

Objetivo Final:
├── 🔴 Import Errors: 0 errores
├── 🟡 Undefined Variables: 0 errores
├── 🟢 Syntax Errors: 0 errores
├── 🔵 Type Errors: 0 errores
├── 🟣 Reference Errors: 0 errores
└── 📊 TOTAL: 0 errores ✅
```

#### **Validaciones Técnicas Específicas:**
- [ ] **V1** `from sistema.imports_interface import ImportsCentral` funciona
- [ ] **V2** `ImportsCentral().get_sistema_components()['logging']['enviar_senal_log']` disponible
- [ ] **V3** `from textual.app import App` sin errores
- [ ] **V4** `dashboard_definitivo.py` pasa validación sintáctica
- [ ] **V5** Todos los archivos en `utils/` cargan correctamente
- [ ] **V6** No hay referencias circulares en imports
- [ ] **V7** `sistema.sic.py` no se usa en ningún archivo activo
- [ ] **V8** Dashboard inicia en menos de 10 segundos

---

## 🧪 COMANDOS DE VERIFICACIÓN ESPECÍFICOS

### **Tests de Validación por Fase:**

#### **Comandos Fase 1:**
```bash
# Verificar import duplicados eliminados
grep -n "import sys" dashboard/dashboard_definitivo.py | wc -l  # Debe ser 1
grep -n "from pathlib import Path" dashboard/dashboard_definitivo.py | wc -l  # Debe ser 1

# Verificar referencias a sic.py eliminadas
grep -n "sistema.sic" dashboard/dashboard_definitivo.py | wc -l  # Debe ser 0

# Test básico de carga
python -c "from sistema.imports_interface import ImportsCentral; print('✅ ImportsCentral OK')"
```

#### **Comandos Fase 2:**
```bash
# Verificar imports de Textual funcionan
python -c "from textual.app import App; print('✅ Textual OK')"

# Verificar ICT components accesibles
python -c "from sistema.imports_interface import get_ict_components; print('✅ ICT Components OK')"

# Test logging unificado
python -c "from sistema.imports_interface import sic_log; sic_log('Test'); print('✅ Logging OK')"
```

#### **Comandos Fase 3:**
```bash
# Verificar archivos auxiliares
python -c "import utils.system_diagnostics; print('✅ System Diagnostics OK')"
python -c "import utils.mt5_data_manager; print('✅ MT5 Manager OK')"

# Verificar sin imports circulares
python -c "import dashboard.problems_tab_renderer; print('✅ Problems Tab OK')"
```

#### **Comandos Fase 4:**
```bash
# Test final completo
python dashboard/dashboard_definitivo.py --test-mode  # Debe iniciarse sin errores críticos

# Verificar VS Code Problems
code --list-extensions | grep -i python  # Verificar extensión Python activa

# Test de memoria y performance
time python -c "from dashboard.dashboard_definitivo import SentinelDashboardDefinitivo"
```

---

## 📋 CHECKLIST DE CALIDAD FINAL

### **Calidad de Código:**
- [ ] **Q1** Sin imports duplicados en ningún archivo
- [ ] **Q2** Sin referencias a archivos obsoletos (sic.py)
- [ ] **Q3** Imports organizados alfabéticamente por categoría
- [ ] **Q4** Documentación de imports actualizada
- [ ] **Q5** Sin warnings de imports circulares
- [ ] **Q6** Fallbacks robustos para imports opcionales
- [ ] **Q7** Logging consistente en todo el proyecto
- [ ] **Q8** Manejo de errores apropiado en imports

### **Funcionalidad:**
- [ ] **F1** Dashboard inicia correctamente
- [ ] **F2** Todas las pestañas son accesibles
- [ ] **F3** Sistema de logging funciona
- [ ] **F4** ImportsCentral proporciona todos los componentes
- [ ] **F5** No hay crashes al navegar en dashboard
- [ ] **F6** Performance aceptable (< 10s startup)
- [ ] **F7** Memoria estable (sin leaks detectados)
- [ ] **F8** Todos los componentes core responden

### **Integración:**
- [ ] **I1** SLUC v2.1 y SIC v2.0 trabajando juntos
- [ ] **I2** VS Code reconoce imports correctamente
- [ ] **I3** Pylance sin errores críticos
- [ ] **I4** Sistema de tipos consistente
- [ ] **I5** Autocompletado funciona en VS Code
- [ ] **I6** Debug mode funcional
- [ ] **I7** Hot reload funciona correctamente
- [ ] **I8** Extensions de VS Code compatibles

### **Documentación:**
- [ ] **D1** Bitácora actualizada con todos los cambios
- [ ] **D2** Comentarios de código actualizados
- [ ] **D3** README actualizado si es necesario
- [ ] **D4** Logs de cambios documentados
- [ ] **D5** Explicación de arquitectura dual clarificada

---

## 🔄 PROCEDIMIENTO DE ROLLBACK

**En caso de problemas críticos:**
1. **Git restore** de archivos modificados
2. **Verificar backup** de estado anterior funcional
3. **Analizar logs** de error específico
4. **Ajustar estrategia** y reintentar paso a paso
5. **Documentar lecciones** aprendidas en bitácora

---

## ⏱️ TIMING Y MÉTRICAS ESPECÍFICAS

### **Cronometraje Detallado AUTOMATIZADO:**
```
🔧 FASE 1: LIMPIEZA AUTOMATIZADA (8 min vs 20 min manual)
├── Auto-fix imports duplicados y no utilizados (4 min)
├── Corrección imports problemáticos automática (4 min)
└── ✅ Target: 465 → 315 errores (-150) [Mejora: +50 vs manual]

🔗 FASE 2: MIGRACIÓN INTELIGENTE (5 min vs 15 min manual)
├── Migración automática a ImportsCentral (3 min)
├── Reemplazo masivo de imports restantes (2 min)
└── ✅ Target: 315 → 115 errores (-200) [Mejora: +50 vs manual]

📁 FASE 3: PROCESAMIENTO AUXILIARES (4 min vs 10 min manual)
├── Detección automática archivos problemáticos (1 min)
├── Migración batch de archivos auxiliares (3 min)
└── ✅ Target: 115 → 25 errores (-90) [Similar a manual: -100]

✅ FASE 4: VALIDACIÓN AUTOMATIZADA (3 min vs 10 min manual)
├── Validación automática imports específicos (1 min)
├── Tests funcionales automatizados (2 min)
└── ✅ Target: 25 → 0 errores (-25) [Mejora: +10 vs manual]

📊 TOTAL AUTOMATIZADO: 20 minutos (vs 55 manual = 64% reducción)
🎯 PRECISIÓN: Superior (backups automáticos + validaciones)
```

### **Indicadores de Éxito AUTOMATIZADOS por Minuto:**
```
Min 0-8:   FASE 1 → 315 errores (32% progreso) [Acelerado]
Min 8-13:  FASE 2 → 115 errores (75% progreso) [Acelerado]
Min 13-17: FASE 3 → 25 errores (95% progreso) [Acelerado]
Min 17-20: FASE 4 → 0 errores (100% ÉXITO) [Acelerado]
```

### **Alertas de Progreso AUTOMATIZADAS:**
- **⚠️ Si Min 8 > 350 errores:** Revisar logs de activate_import_fixer.py
- **⚠️ Si Min 13 > 150 errores:** Revisar logs de migrador_inteligente_v2.py
- **⚠️ Si Min 17 > 30 errores:** Revisar detectar_imports_viejos.py output
- **🚨 Si Min 20 > 5 errores:** Ejecutar validación manual complementaria

---

**🎯 RESUMEN:** Este plan convertirá el estado actual de 465 errores en un sistema completamente funcional con 0 errores, utilizando la arquitectura dual SLUC v2.1 para logging e ImportsCentral SIC v2.0 para imports, sin crear archivos innecesarios y manteniendo la funcionalidad existente.

---

*Bitácora generada automáticamente - ICT Engine v5.0*
*Plan de Ataque VS Code Problems - 06 Agosto 2025*
