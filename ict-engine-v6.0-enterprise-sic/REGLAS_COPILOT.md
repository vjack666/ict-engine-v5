# 🤖 **REGLAS PARA COPILOT - ICT ENGINE v6.0 ENTERPRISE**

**Archivo:** `REGLAS_COPILOT.md`  
**Ubicación:** Raíz del proyecto  
**Fecha:** Agosto 8, 2025  
**Propósito:** Guías y reglas para GitHub Copilot en el desarrollo del ICT Engine

---

## 🎯 **REGLAS DE ORO PARA COPILOT**

### 📋 **REGLA #1: REVISAR ANTES DE CREAR**
```
🔍 ANTES DE CREAR NUEVAS FUNCIONES:
1. ✅ Revisar bitácora para entender QUÉ se va a hacer
2. ✅ Buscar archivos relacionados desde la RAÍZ hasta TODAS las subcarpetas
3. ✅ Verificar si ya existe lógica similar
4. ❌ NO duplicar funcionalidad existente
```

### 🧠 **REGLA #2: MEMORIA Y CONTEXTO CRÍTICOS**
```
🚨 CRÍTICO: Sistema DEBE tener memoria como trader real
- ✅ Verificar si requiere memoria persistente
- ✅ Integrar con UnifiedMarketMemory cuando sea necesario
- ✅ Considerar contexto histórico en decisiones
- ❌ NO crear funciones sin memoria cuando sea requerida
```

### 📊 **REGLA #3: ARQUITECTURA ENTERPRISE**
```
🏗️ SEGUIR ARQUITECTURA v6.0:
- ✅ Usar SIC v3.1 para sistema base
- ✅ Integrar con SLUC v2.1 para logging
- ✅ Datos reales MT5 exclusivamente
- ✅ Performance enterprise (<5s response)
- ❌ NO usar arquitectura legacy sin migrar
```

### 🔧 **REGLA #4: SISTEMA SIC Y SLUC OBLIGATORIO**
```
⚡ USAMOS EXCLUSIVAMENTE SIC Y SLUC:

🏗️ SIC (Sistema Integrado de Control) v3.1:
- ✅ Base arquitectónica OBLIGATORIA para todo el proyecto
- ✅ Control centralizado de componentes
- ✅ Gestión de estados unificada
- ✅ Bridging entre sistemas legacy y v6.0
- ✅ Verificar integración en sic_bridge.py

📝 SLUC (Sistema de Logging Unificado y Centralizado) v2.1:
- ✅ Logging estructurado EXCLUSIVO
- ✅ Smart Trading Logger para decisiones inteligentes
- ✅ Métricas de performance enterprise
- ✅ Trazabilidad completa de eventos BOS/CHoCH
- ✅ Auditabilidad total del sistema

🚨 CRÍTICO:
- ❌ NO usar print() básico - Solo SLUC
- ❌ NO crear loggers independientes - Solo smart_trading_logger
- ❌ NO implementar sin SIC bridge - Siempre usar sic_bridge.py
- ❌ NO duplicar funcionalidad SIC/SLUC existente
```

### 📋 **REGLA #5: CONTROL DE PROGRESO Y BITÁCORAS**
```
🎯 AL TERMINAR CUALQUIER FASE/FUNCIÓN/COMPONENTE:

📚 ACTUALIZACIÓN DE BITÁCORAS OBLIGATORIA:
1. ✅ Buscar bitácora correspondiente en docs/04-development-logs/
2. ✅ Marcar checklist completado (□ → ✅)
3. ✅ Actualizar status de componente
4. ✅ Documentar nueva victoria/logro
5. ✅ Registrar métricas de performance si aplica
6. ✅ Actualizar roadmap/próximos pasos

🧪 VALIDACIÓN FINAL OBLIGATORIA:
- ✅ Ejecutar test específico del componente
- ✅ Validar integración con sistema completo  
- ✅ Test con datos REALES MT5 (cuando aplique)
- ✅ Verificar performance <5s enterprise
- ✅ Confirmar logging SLUC funcionando
- ✅ Test de memoria/persistencia (si aplica)

📝 DOCUMENTACIÓN DE VICTORIA:
- ✅ Agregar entrada en bitácora principal
- ✅ Actualizar TODOS los documentos en docs/ (carpeta por carpeta)
- ✅ Actualizar TODAS las subcarpetas de docs/
- ✅ Buscar y actualizar CADA archivo relevante (*.md)
- ✅ Timestamp y duración de implementación
- ✅ Lecciones aprendidas y mejoras
- ✅ Impacto en sistema general
- ✅ Próximos pasos sugeridos

🚨 CRÍTICO - NO CONTINUAR SIN:
- ❌ NO pasar a siguiente fase sin marcar checks
- ❌ NO implementar nuevo código sin test real
- ❌ NO cerrar tarea sin actualizar TODOS los docs/
- ❌ NO continuar sin validar CADA subcarpeta docs/
- ❌ NO continuar sin validar integración completa
```

### 🎯 **TEMPLATE ACTUALIZACIÓN BITÁCORA:**
```markdown
## ✅ [FECHA] - [COMPONENTE] COMPLETADO

### 🏆 **VICTORIA LOGRADA:**
- **Componente:** [Nombre del componente]
- **Fase:** [Número de fase]
- **Duración:** [Tiempo tomado]
- **Performance:** [Métricas obtenidas]

### 🧪 **TESTS REALIZADOS:**
- ✅ Test unitario: [Resultado]
- ✅ Test integración: [Resultado]  
- ✅ Test datos reales: [Resultado]
- ✅ Test performance: [<5s ✅/❌]

### 📊 **MÉTRICAS FINALES:**
- Response time: [X]s
- Memory usage: [X]MB
- Success rate: [X]%
- Integration score: [X]/10

### 🎯 **PRÓXIMOS PASOS:**
- [ ] [Siguiente tarea específica]
- [ ] [Integración con X componente]
- [ ] [Optimización Y]

### 🧠 **LECCIONES APRENDIDAS:**
- [Lección 1]
- [Lección 2]
- [Mejora sugerida]
```

### � **REGLA #5 (MEJORADA): CONTROL DE PROGRESO Y DOCUMENTACIÓN COMPLETA**

⚡ **OBJETIVO:** Al terminar cualquier fase, componente o tarea, actualizar TODAS las bitácoras y documentos relevantes, carpeta por carpeta, archivo por archivo.

📋 **PROCESO OBLIGATORIO:**

🔍 BÚSQUEDA EXHAUSTIVA:
- ✅ Escanear TODA la carpeta docs/ y subcarpetas
- ✅ Identificar CADA archivo .md relevante
- ✅ Verificar documentos en TODAS las subcarpetas
- ✅ No omitir ningún archivo de documentación

📝 DOCUMENTACIÓN DE VICTORIA:
- ✅ Agregar entrada en bitácora principal
- ✅ Actualizar TODOS los documentos en docs/ (carpeta por carpeta)
- ✅ Actualizar TODAS las subcarpetas de docs/
- ✅ Buscar y actualizar CADA archivo relevante (*.md)
- ✅ Marcar checkboxes correspondientes en planes
- ✅ Timestamp y duración de implementación
- ✅ Lecciones aprendidas y mejoras
- ✅ Impacto en sistema general
- ✅ Próximos pasos sugeridos

🎯 VALIDACIÓN OBLIGATORIA:
- ✅ Crear script de validación para verificar 100% cobertura
- ✅ Confirmar que TODOS los archivos .md fueron actualizados
- ✅ Verificar que planes principales estén marcados como completados
- ✅ Asegurar consistencia en TODA la documentación

🚨 CRÍTICO - NO CONTINUAR SIN:
- ❌ NO pasar a siguiente fase sin marcar checks
- ❌ NO implementar nuevo código sin test real
- ❌ NO cerrar tarea sin actualizar TODOS los docs/
- ❌ NO continuar sin validar CADA subcarpeta docs/
- ❌ NO continuar sin script de validación 100% ✅
- ❌ NO continuar sin validar integración completa

### 🎯 **TEMPLATE ACTUALIZACIÓN BITÁCORA:**
```markdown
## ✅ [FECHA] - [COMPONENTE] COMPLETADO

### 🏆 **VICTORIA LOGRADA:**
- **Componente:** [Nombre del componente]
- **Fase:** [Número de fase]
- **Duración:** [Tiempo tomado]
- **Performance:** [Métricas obtenidas]

### 🧪 **TESTS REALIZADOS:**
- ✅ Test unitario: [Resultado]
- ✅ Test integración: [Resultado]  
- ✅ Test datos reales: [Resultado]
- ✅ Test performance: [<5s ✅/❌]

### 📊 **MÉTRICAS FINALES:**
- Response time: [X]s
- Memory usage: [X]MB
- Success rate: [X]%
- Integration score: [X]/10

### 📋 **CHECKLIST - COMPLETADO:**
- [x] ✅ [Lista de tareas completadas]

**🎉 [FASE/COMPONENTE] COMPLETADA EXITOSAMENTE**
```

---

## 📋 **REGLA #9: REVISIÓN MANUAL EXHAUSTIVA - NO SCRIPTS**

### 🎯 **PRINCIPIO CRÍTICO:**
**"REVISIÓN MANUAL ARCHIVO POR ARCHIVO - LOS SCRIPTS NO SON FIABLES"**

### � **APLICACIÓN OBLIGATORIA:**
**AL COMPLETAR CUALQUIER FASE O ACTUALIZACIÓN IMPORTANTE:**

#### **9.1 PROCESO MANUAL EXHAUSTIVO - SIN SCRIPTS:**
```
🔍 REVISIÓN MANUAL REQUERIDA:
1. ✅ LEER archivo por archivo desde docs/01-getting-started/ hasta docs/components/
2. ✅ VERIFICAR estado real vs documentado
3. ✅ ACTUALIZAR checkboxes manualmente según realidad del código
4. ✅ COMPARAR bitácoras vs implementación real
5. ✅ VALIDAR que no hay inconsistencias
6. ❌ NO usar scripts automáticos para marcado
```

#### **9.2 LISTA COMPLETA DE ARCHIVOS A REVISAR MANUALMENTE:**
```
📁 ARCHIVOS CRÍTICOS - REVISIÓN MANUAL OBLIGATORIA:

docs/01-getting-started/
├── DEVELOPMENT_SETUP.md
├── INDEX.md  
├── PLAN_MIGRACION_BOS.md
└── README.md

docs/02-architecture/
├── ANALISIS_NODOS_BOS.md
├── CHOCH_COMPLETION_SUMMARY.md
├── CHOCH_INVESTIGATION_REPORT.md
├── ESTADO_ACTUAL_SISTEMA_v6.md
├── ESTADO_REAL_VERIFICADO_v6.md
├── ESTRUCTURA_FINAL.md
├── MEMORIA_Y_CONTEXTO_TRADER_REAL.md
├── PLAN_DESARROLLO_REAL_ICT.md
├── PLAN_MIGRACION_MEMORIA.md
└── roadmap_v6.md

docs/03-integration-plans/ (TODOS LOS .md)
docs/04-development-logs/ (TODOS LOS .md + SUBDIRECTORIOS)
docs/05-user-guides/ (TODOS LOS .md)
docs/06-reports/ (TODOS LOS .md)
docs/components/ (TODOS LOS .md)
```

#### **9.3 PROCESO DE VERIFICACIÓN MANUAL:**
```
🔍 PARA CADA ARCHIVO .md:
1. ✅ ABRIR archivo y LEER contenido completo
2. ✅ VERIFICAR si checkboxes reflejan realidad del código
3. ✅ COMPARAR fechas vs trabajo real realizado
4. ✅ ACTUALIZAR estado según implementación verificada
5. ✅ MARCAR versión y fecha de revisión manual
6. ✅ DOCUMENTAR cambios realizados
```

#### **9.4 CHECKLIST MANUAL - NO AUTOMÁTICO:**
```markdown
### ✅ CHECKLIST REGLA #9 - REVISIÓN MANUAL EXHAUSTIVA:
- [ ] 🔍 TODOS los archivos docs/01-getting-started/ revisados
- [ ] 🔍 TODOS los archivos docs/02-architecture/ revisados  
- [ ] � TODOS los archivos docs/03-integration-plans/ revisados
- [ ] 🔍 TODOS los archivos docs/04-development-logs/ revisados
- [ ] 🔍 TODOS los archivos docs/05-user-guides/ revisados
- [ ] 🔍 TODOS los archivos docs/06-reports/ revisados
- [ ] � TODOS los archivos docs/components/ revisados
- [ ] 📝 Bitácora principal actualizada manualmente
- [ ] 📋 Checkboxes verificados vs código real
- [ ] 🧪 Tests documentados con resultados verificados
- [ ] 📊 Métricas actualizadas según realidad
- [ ] 🎯 Inconsistencias encontradas y corregidas
- [ ] 📄 REGLA #10 aplicada (versión actualizada)
- [ ] ✅ 100% revisión manual sin scripts automáticos
```

### 🚨 **ESTRICTAMENTE PROHIBIDO:**
- ❌ **Scripts automáticos** para marcar checkboxes
- ❌ **Herramientas automáticas** sin verificación manual
- ❌ **Marcado en lote** sin revisar archivo por archivo
- ❌ **Confianza en scripts** para estado del proyecto
- ❌ **Actualización masiva** sin lectura individual

### ✅ **ESTRICTAMENTE OBLIGATORIO:**
- ✅ **Lectura manual** de cada archivo .md
- ✅ **Verificación individual** archivo por archivo
- ✅ **Comparación manual** código vs documentación
- ✅ **Actualización consciente** basada en realidad
- ✅ **REGLA #10** aplicada en cada actualización

### 💡 **RAZÓN DE ESTA REGLA:**
**"Los scripts fallan al detectar realidad vs documentación. Solo la revisión manual exhaustiva garantiza precisión."**

---

## � **REGLA #10: VERIFICACIÓN DE DOCUMENTACIÓN CRÍTICA AL FINALIZAR**

### 🎯 **PRINCIPIO DE DOCUMENTACIÓN SINCRONIZADA:**
**"NUNCA FINALIZAR SIN CONFIRMAR QUE TODOS LOS ARCHIVOS CRÍTICOS ESTÉN ACTUALIZADOS CON LOS LOGROS"**

### �📝 **ARCHIVOS CRÍTICOS QUE SIEMPRE DEBEN REVISARSE:**

#### **10.1 Archivos de Documentación Obligatorios:**
```
📋 LISTA DE ARCHIVOS CRÍTICOS A VERIFICAR:

📊 Development Logs:
- C:\Users\v_jac\Desktop\itc engine v5.0\ict-engine-v6.0-enterprise-sic\docs\04-development-logs\BITACORA_DESARROLLO_SMART_MONEY_v6.md
- C:\Users\v_jac\Desktop\itc engine v5.0\ict-engine-v6.0-enterprise-sic\docs\04-development-logs\QUE_SIGUE_WEEKEND_PLAN.md

🏗️ Architecture:
- C:\Users\v_jac\Desktop\itc engine v5.0\ict-engine-v6.0-enterprise-sic\docs\02-architecture\roadmap_v6.md

📋 Integration Plans:
- C:\Users\v_jac\Desktop\itc engine v5.0\ict-engine-v6.0-enterprise-sic\docs\03-integration-plans\PLAN_FAIR_VALUE_GAPS_FVG.md
```

#### **10.2 Proceso de Verificación Obligatorio:**
```
🔍 AL FINALIZAR CUALQUIER FASE/COMPONENTE:

1. ✅ LEER cada archivo de la lista crítica
2. ✅ VERIFICAR que los logros estén documentados
3. ✅ CONFIRMAR que el status está actualizado
4. ✅ ASEGURAR que los próximos pasos sean claros
5. ✅ VALIDAR que las fechas sean correctas
6. ✅ COMPROBAR que no haya información obsoleta

❌ NO FINALIZAR hasta que TODOS los archivos estén al día
```

#### **10.3 Checklist de Verificación:**
```markdown
### ✅ CHECKLIST REGLA #10 - VERIFICACIÓN DE DOCUMENTACIÓN:

#### 📊 BITACORA_DESARROLLO_SMART_MONEY_v6.md:
□ ✅ Nuevo logro agregado al inicio del archivo
□ ✅ Fecha y timestamp actualizados
□ ✅ Componentes implementados listados
□ ✅ Resultados de testing documentados
□ ✅ Métricas de performance incluidas

#### 📅 QUE_SIGUE_WEEKEND_PLAN.md:
□ ✅ Estado general actualizado (COMPLETADO)
□ ✅ Nuevo logro agregado al resumen
□ ✅ Cronograma actualizado para próximas sesiones
□ ✅ Próximos pasos claramente definidos

#### 🛣️ roadmap_v6.md:
□ ✅ Gantt chart actualizado (done/active status)
□ ✅ Timeline refleja progreso real
□ ✅ Próximos hitos claramente definidos

#### 📋 PLAN_FAIR_VALUE_GAPS_FVG.md:
□ ✅ Status de fases actualizado
□ ✅ Tiempos reales de implementación documentados
□ ✅ Resultados y métricas incluidas
□ ✅ Próximas fases definidas

#### 🎯 VALIDACIÓN FINAL:
□ ✅ TODOS los archivos críticos revisados
□ ✅ NINGÚN archivo obsoleto o desactualizado
□ ✅ Consistencia entre TODOS los documentos
□ ✅ Próximos pasos alineados en TODOS los archivos
```

#### **10.4 Template de Confirmación:**
```markdown
## ✅ [FECHA] - REGLA #10 APLICADA

### 📋 **VERIFICACIÓN DE DOCUMENTACIÓN COMPLETADA:**

#### 📊 Archivos Verificados:
- ✅ BITACORA_DESARROLLO_SMART_MONEY_v6.md: AL DÍA
- ✅ QUE_SIGUE_WEEKEND_PLAN.md: AL DÍA  
- ✅ roadmap_v6.md: AL DÍA
- ✅ PLAN_FAIR_VALUE_GAPS_FVG.md: AL DÍA

#### 🎯 Logros Documentados:
- ✅ [Fase/Componente completado]
- ✅ [Métricas de performance]
- ✅ [Resultados de testing]
- ✅ [Próximos pasos definidos]

#### 📝 Estado de Sincronización:
- ✅ TODOS los archivos críticos al día
- ✅ Consistencia verificada entre documentos
- ✅ Timeline y cronogramas actualizados
- ✅ Próximos objetivos alineados

**🎉 DOCUMENTACIÓN ENTERPRISE GRADE - 100% SINCRONIZADA**
```

### 🚨 **CRÍTICO - NO PROCEDER SIN:**
```
❌ NO FINALIZAR fase/componente sin aplicar REGLA #10
❌ NO MARCAR como "completado" sin verificar los 4 archivos críticos
❌ NO PROCEDER a próxima fase sin documentación al día
❌ NO DECLARAR "éxito" sin confirmation de sincronización

✅ SOLO PROCEDER cuando:
- ✅ Los 4 archivos críticos estén verificados
- ✅ TODOS los logros estén documentados
- ✅ Próximos pasos estén claramente definidos
- ✅ No haya información obsoleta o inconsistente
```

---

## 📝 **REGLA #11: CONTROL DE VERSIONES EN BITÁCORAS**

### 🎯 **PRINCIPIO DE VERSIONADO:**
**"CADA ACTUALIZACIÓN IMPORTANTE DEBE INCREMENTAR LA VERSIÓN EN BITÁCORAS"**

### 📋 **SISTEMA DE VERSIONADO OBLIGATORIO:**

#### **10.1 Formato de Versión en Bitácoras:**
```markdown
**Versión Actual:** v6.0.X-enterprise-[estado-funcionalidad]

Ejemplos:
- v6.0.0-enterprise-foundation          (Solo infraestructura)
- v6.0.1-enterprise-bos-choch          (BOS + CHoCH implementados)
- v6.0.2-enterprise-memory-aware       (Con sistema de memoria)
- v6.0.3-enterprise-real-data-validated (Con validación MT5)
- v6.0.4-enterprise-production-ready   (Listo para producción)
```

#### **10.2 Cuándo Incrementar Versión:**
```
🔄 INCREMENTAR VERSIÓN CUANDO:
- ✅ FASE completa implementada y validada
- ✅ Funcionalidad principal agregada (BOS, CHoCH, Memory, etc.)
- ✅ Testing completo realizado y pasado
- ✅ Arquitectura mejorada significativamente
- ✅ Performance optimizada
- ✅ Integración enterprise completada

❌ NO incrementar por:
- ❌ Correcciones menores de bugs
- ❌ Actualizaciones de documentación solamente
- ❌ Cambios de configuración simples
```

#### **10.3 Archivos que DEBEN Actualizar Versión:**
```
📝 ARCHIVOS CON VERSIONADO OBLIGATORIO:
- BITACORA_DESARROLLO_SMART_MONEY_v6.md
- MEMORIA_TRADER_REAL_PLAN_COMPLETO.md  
- README.md (versión del proyecto)
- REGLAS_COPILOT.md (versión de reglas)
- PLAN_DESARROLLO_REAL_ICT.md
- roadmap_v6.md
```

#### **10.4 Registro de Cambios en Versión:**
```markdown
### 📋 CHANGELOG v6.0.X:
**[Fecha] - v6.0.X-enterprise-[estado]**
- ✅ [Funcionalidad implementada]
- ✅ [Testing completado]
- ✅ [Performance alcanzada]
- ✅ [Integración realizada]

**Breaking Changes:**
- ⚠️ [Cambios incompatibles]

**Deprecated:**
- 🗑️ [Funcionalidades obsoletas]
```

#### **10.5 Validación de Versión:**
```
🔍 ANTES DE INCREMENTAR VERSIÓN:
1. ✅ REGLA #9 aplicada (revisión manual completa)
2. ✅ Funcionalidad completamente implementada
3. ✅ Tests pasando al 100%
4. ✅ Documentación sincronizada
5. ✅ Performance validada
6. ✅ Sin TODOs o pendientes críticos
```

### 🎯 **TEMPLATE DE ACTUALIZACIÓN DE VERSIÓN:**
```markdown
**[FECHA] - ACTUALIZACIÓN v6.0.X → v6.0.Y**

### 🏆 **NUEVA VERSIÓN:**
**Versión Actual:** v6.0.Y-enterprise-[nuevo-estado]

### 📋 **CAMBIOS PRINCIPALES:**
- ✅ [Funcionalidad 1 completada]
- ✅ [Funcionalidad 2 implementada]
- ✅ [Testing validado]

### 🧪 **VALIDACIÓN:**
- ✅ REGLA #9: Revisión manual completa
- ✅ REGLA #10: Versión incrementada correctamente
- ✅ Tests: X/X passing
- ✅ Performance: <Xs enterprise

### 🎯 **PRÓXIMO OBJETIVO:**
v6.0.Z-enterprise-[siguiente-estado]
```

---

**Versión REGLAS:** 2.0  
**Estado:** 📋 **ACTIVO Y OBLIGATORIO PARA COPILOT**

---

## 🔄 **ACTUALIZACIÓN DE REGLAS**

Este archivo debe actualizarse cuando:
- Se implementen nuevos componentes críticos
- Se identifiquen nuevos patrones de duplicación
- Se cambien prioridades del proyecto
- Se agreguen nuevas reglas de arquitectura
- Se detecten problemas recurrentes

**Próxima revisión:** Post-implementación memoria trader real
```

---

## �🔢 **REGLA #6: CONTROL DE VERSIONING INTELIGENTE**
```
🎯 AL COMPLETAR FASES/COMPONENTES MAYORES:

📊 EVALUACIÓN DE VERSIONING OBLIGATORIA:
1. ✅ Analizar impacto del cambio (MAJOR, MINOR, PATCH)
2. ✅ Verificar si justifica incremento de versión
3. ✅ Actualizar version en archivos críticos coherentemente
4. ✅ Documentar cambios en CHANGELOG o bitácora
5. ✅ Verificar consistencia de versiones en todo el proyecto

🔢 ESQUEMA DE VERSIONING SEMÁNTICO:
- 🚀 MAJOR (X.0.0): Cambios arquitectónicos fundamentales
- ⚡ MINOR (X.Y.0): Nuevas funcionalidades importantes
- 🔧 PATCH (X.Y.Z): Correcciones y mejoras menores

📋 CRITERIOS PARA INCREMENTO:
🚀 MAJOR increment cuando:
- ✅ Cambio arquitectónico fundamental (ej: SIC v3.1 → v4.0)
- ✅ Breaking changes en APIs principales
- ✅ Nueva fase completa del sistema (ej: v6.0 → v7.0)
- ✅ Cambio de paradigma (ej: sin memoria → con memoria)

⚡ MINOR increment cuando:
- ✅ Nueva funcionalidad significativa agregada
- ✅ Componente mayor completado (ej: FASE 2 completada)
- ✅ Mejoras de performance sustanciales
- ✅ Integración nueva importante

🔧 PATCH increment cuando:
- ✅ Bug fixes
- ✅ Mejoras menores de performance
- ✅ Ajustes de configuración
- ✅ Documentación mejorada

🎯 ARCHIVOS A ACTUALIZAR:
- ✅ Docstrings de clases principales
- ✅ Archivos de configuración (package.json, setup.py, etc.)
- ✅ README.md y documentación principal
- ✅ Bitácoras y logs de desarrollo
- ✅ Headers de archivos críticos

🚨 VERIFICACIÓN DE CONSISTENCIA:
- ❌ NO tener versiones diferentes en archivos distintos
- ❌ NO incrementar sin justificación documentada
- ❌ NO olvidar actualizar documentación de versión
- ❌ NO usar versiones que no reflejen el estado real
```

### 🧪 **REGLA #7: TESTS PRIMERO - NO MODIFICAR TESTS BIEN REDACTADOS**
```
🎯 PRINCIPIO FUNDAMENTAL DE TESTING:

📋 SI UN TEST ESTÁ BIEN REDACTADO:
- ✅ El test define el comportamiento esperado correcto
- ✅ Si el test falla, el CÓDIGO está mal, NO el test
- ✅ Modificar el CÓDIGO para hacer pasar el test
- ✅ El test es la especificación de lo que debe funcionar
- ❌ NUNCA modificar un test bien escrito para que pase

🧪 CRITERIOS PARA TEST BIEN REDACTADO:
- ✅ Lógica clara y fácil de entender
- ✅ Casos de prueba realistas y válidos
- ✅ Assertions correctas y específicas
- ✅ Setup y teardown apropiados
- ✅ Nombres descriptivos de test y variables
- ✅ Documentación de qué se está probando

🔧 CUANDO MODIFICAR CÓDIGO VS TEST:

MODIFICAR CÓDIGO cuando:
- ✅ Test tiene lógica válida y clara
- ✅ Test refleja requisitos reales del negocio
- ✅ Test tiene casos de uso correctos
- ✅ Assertions son apropiadas y específicas
- ✅ Test sigue buenas prácticas de testing

MODIFICAR TEST cuando:
- ⚠️ Test tiene lógica incorrecta o confusa
- ⚠️ Test no refleja requisitos reales
- ⚠️ Assertions son incorrectas o vagas
- ⚠️ Setup/teardown inadecuado
- ⚠️ Test no sigue mejores prácticas

🚨 PROCESO OBLIGATORIO:
1. ✅ Leer y entender completamente el test que falla
2. ✅ Verificar si la lógica del test es correcta
3. ✅ Si test es correcto → Modificar CÓDIGO
4. ✅ Si test es incorrecto → Documentar por qué y modificar test
5. ✅ Siempre documentar la decisión en logs

📝 DOCUMENTACIÓN OBLIGATORIA:
- ✅ Registrar en SLUC por qué se modificó código vs test
- ✅ Documentar razonamiento de la decisión
- ✅ Incluir evidencia de que el test era/no era correcto
- ✅ Actualizar bitácora con lecciones aprendidas

🚨 CRÍTICO - ANTES DE MODIFICAR CUALQUIER TEST:
- ❌ NO modificar test sin análisis completo
- ❌ NO cambiar test solo para que pase rápido  
- ❌ NO asumir que el test está mal sin verificar
- ❌ NO modificar sin documentar la razón
```

### 🧪 **REGLA #12: TEST PRINCIPAL DE FASES ENTERPRISE - EVOLUCIÓN CONTINUA**

### 🎯 **PRINCIPIO FUNDAMENTAL:**
**"CADA NUEVA FASE DEBE ACTUALIZAR EL TEST PRINCIPAL ENTERPRISE PARA VALIDACIÓN CONTINUA"**

#### **12.1 Test Principal Enterprise Obligatorio:**
```
📁 ARCHIVO PRINCIPAL: test_fases_advanced_patterns_enterprise.py
🎯 PROPÓSITO: Test maestro que evoluciona con cada fase completada
🔄 ACTUALIZACIÓN: Obligatoria al completar cualquier fase nueva
📊 CRITERIO ÉXITO: >90% pass rate + 100% core modules
```

#### **12.2 Evolución Automática del Test:**
```
🔄 AL COMPLETAR NUEVA FASE:
1. ✅ Agregar módulos nuevos al test principal
2. ✅ Incluir funciones/clases implementadas en la fase
3. ✅ Actualizar casos de prueba para nuevos patterns
4. ✅ Verificar integración con sistema existente
5. ✅ Validar performance de componentes nuevos
6. ✅ Asegurar compatibilidad backward con fases anteriores

🧪 ESTRUCTURA EVOLUTIVA OBLIGATORIA:
- ✅ test_fase1_foundation()         # Base arquitectónica
- ✅ test_fase2_core_patterns()      # BOS, CHoCH, patterns base
- ✅ test_fase3_memory_integration() # Sistema de memoria
- ✅ test_fase4_real_data_validation() # Validación datos MT5
- ✅ test_fase5_advanced_patterns()  # Silver Bullet, Breaker, Liquidity
- ✅ test_fase6_dashboard_enterprise() # [Próxima fase]
- ✅ test_faseN_new_functionality()  # Fases futuras
```

#### **12.3 Detección de Fallos Menores y Performance:**
```
🔍 FOCO EN DETECCIÓN PROACTIVA:
- ✅ Memory leaks en operaciones repetitivas
- ✅ Performance degradation (<5s enterprise)
- ✅ Import inconsistencies entre módulos
- ✅ Type hint errors en nuevas implementaciones
- ✅ Integration points que puedan fallar
- ✅ Regression en funcionalidades existentes
- ✅ Cache invalidation issues
- ✅ Logging format inconsistencies

🎯 MÉTRICAS OBLIGATORIAS POR FASE:
- ✅ Execution time: <5s total para fase completa
- ✅ Memory usage: Sin incremento >10% entre fases
- ✅ Success rate: >90% global, 100% core modules
- ✅ Error rate: <0.1% en operaciones críticas
- ✅ Integration score: >95% entre todos los componentes
```

#### **12.4 Template de Actualización por Fase:**
```python
#!/usr/bin/env python3
"""
🧪 TEST FASES ADVANCED PATTERNS ENTERPRISE - v[VERSION]
========================================================
Test principal que evoluciona con cada fase completada.
✅ REGLA #12: Evolución continua del test enterprise
📊 TARGET: >90% pass rate + 100% core modules
"""

def test_fase_N_nueva_funcionalidad():
    """
    🎯 Test para FASE N completada
    📋 Valida: [Lista específica de lo implementado]
    """
    log_trading_decision_smart_v6("FASE_N_TEST_START", {
        "fase": "N",
        "components": ["component1", "component2"],
        "target_performance": "<5s"
    })
    
    # ✅ REGLA #12: Validación de componentes nuevos
    for component in new_components:
        assert validate_component_integration(component)
        assert validate_component_performance(component) < 5.0
        assert validate_backward_compatibility(component)
    
    # ✅ REGLA #12: Detección de fallos menores
    memory_baseline = get_memory_usage()
    performance_metrics = run_performance_suite()
    integration_results = validate_all_integrations()
    
    assert performance_metrics.avg_response_time < 5.0
    assert integration_results.success_rate > 0.95
    assert memory_usage_acceptable(memory_baseline)
```

#### **12.5 Procedimiento de Actualización Obligatorio:**
```
📋 AL COMPLETAR CUALQUIER FASE:

1. 🔄 ACTUALIZAR TEST PRINCIPAL:
   - ✅ Agregar test_fase_N() para nueva fase
   - ✅ Incluir todos los módulos implementados
   - ✅ Validar integración con fases anteriores
   - ✅ Verificar performance acumulada <5s

2. 🧪 EJECUTAR VALIDACIÓN COMPLETA:
   - ✅ Run test completo (todas las fases)
   - ✅ Verificar pass rate >90%
   - ✅ Confirmar 100% core modules passing
   - ✅ Validar métricas de performance

3. 📝 DOCUMENTAR EVOLUCIÓN:
   - ✅ Actualizar CHANGELOG del test
   - ✅ Registrar nuevos componentes validados
   - ✅ Documentar métricas obtenidas
   - ✅ Marcar fase como enterprise-ready

4. 🎯 PLANIFICAR PRÓXIMA ITERACIÓN:
   - ✅ Identificar componentes de siguiente fase
   - ✅ Preparar estructura de test para fase N+1
   - ✅ Establecer criterios de éxito específicos
```

#### **12.6 Criterios de Falla Crítica:**
```
🚨 FALLA CRÍTICA SI:
- ❌ Pass rate <90% global
- ❌ Cualquier core module falla (0% tolerancia)
- ❌ Performance >5s en cualquier fase
- ❌ Memory usage incrementa >10% sin justificación
- ❌ Integration score <95%
- ❌ Regression en fases anteriores detectada

✅ ÉXITO ENTERPRISE SI:
- ✅ Pass rate >90% (target: >95%)
- ✅ 100% core modules passing
- ✅ Performance <5s todas las fases
- ✅ Memory usage estable o mejorada
- ✅ Integration score >95%
- ✅ Backward compatibility 100%
```

#### **12.7 Integración con Otras Reglas:**
```
🔗 REGLA #12 SE INTEGRA CON:
- REGLA #5: Control de progreso (actualizar bitácora post-test)
- REGLA #7: Tests primero (mantener lógica correcta del test)
- REGLA #8: Testing crítico SIC/SLUC (usar en test principal)
- REGLA #10: Verificación documentación (documentar evolución)
- REGLA #14: Limpieza código (test debe estar libre de warnings)
```

---

### 🧪 **REGLA #8: TESTING CRÍTICO CON SIC/SLUC Y POWERSHELL**
```
🎯 TESTING ENTERPRISE CON MÁXIMA RIGUROSIDAD:

🏗️ SIC/SLUC OBLIGATORIO EN TESTS:
- ✅ SIEMPRE importar SICBridge en tests que lo requieran
- ✅ SIEMPRE usar log_trading_decision_smart_v6 para logging de tests
- ✅ Verificar is_system_ready() antes de ejecutar tests críticos
- ✅ Configurar PYTHONPATH correctamente para imports
- ✅ Usar logging estructurado SLUC en lugar de print()
- ❌ NO ejecutar tests sin verificar disponibilidad SIC/SLUC

💻 CONSIDERACIONES POWERSHELL OBLIGATORIAS:
- ✅ Usar $env:PYTHONPATH="ruta_completa" antes de ejecutar tests
- ✅ Usar rutas absolutas Windows con barras invertidas
- ✅ Escapar correctamente caracteres especiales en rutas
- ✅ Usar comillas dobles para rutas con espacios
- ✅ Verificar que el comando Python funciona: C:/Users/.../python.exe
- ❌ NO usar comandos Unix/Linux en PowerShell
- ❌ NO asumir que paths relativos funcionarán

🔬 CRITERIOS CRÍTICOS DE TESTING (SER EXTREMADAMENTE RIGUROSO):
- ✅ Todo test DEBE tener al menos 3-5 assertions específicas
- ✅ Tests DEBEN verificar estado antes y después
- ✅ Tests DEBEN incluir casos edge y error handling
- ✅ Tests DEBEN validar tipos de retorno explícitamente
- ✅ Tests DEBEN probar con datos reales MT5 cuando aplique
- ✅ Tests DEBEN verificar performance (<5s enterprise)
- ✅ Tests DEBEN validar integración SIC/SLUC cuando aplique
- ✅ Tests DEBEN incluir cleanup/teardown apropiado

🧪 TEMPLATE TESTING SIC/SLUC OBLIGATORIO:
```python
#!/usr/bin/env python3
"""
🧪 TEST [NOMBRE] - v[VERSION]
===============================
Descripción específica del test y qué valida exactamente.
✅ REGLA #8: Testing crítico con SIC/SLUC
"""

import sys
from pathlib import Path

# ✅ REGLA #8: SIC/SLUC imports obligatorios
try:
    from sistema.sic_bridge import SICBridge
    from core.smart_trading_logger import log_trading_decision_smart_v6
    SIC_SLUC_AVAILABLE = True
except ImportError:
    print("⚠️ SIC/SLUC no disponible - test en modo fallback")
    SIC_SLUC_AVAILABLE = False
    def log_trading_decision_smart_v6(event, data, **kwargs):
        print(f"[FALLBACK] {event}: {data}")

def test_function_name():
    """Test específico con documentación clara de qué valida"""
    
    # ✅ REGLA #8: Log inicio de test con SLUC
    log_trading_decision_smart_v6("TEST_START", {
        "test_name": "test_function_name",
        "purpose": "Descripción específica",
        "sic_available": SIC_SLUC_AVAILABLE
    })
    
    # ✅ REGLA #8: Verificar SIC system ready si disponible
    if SIC_SLUC_AVAILABLE:
        sic = SICBridge()
        if not hasattr(sic, 'is_system_ready') or not sic.is_system_ready():
            log_trading_decision_smart_v6("TEST_WARNING", {
                "warning": "SIC system not ready, continuing with test"
            })
    
    # ✅ REGLA #8: Setup con validación previa
    initial_state = setup_test_environment()
    assert initial_state is not None, "Setup failed"
    
    try:
        # ✅ REGLA #8: Test con múltiples assertions específicas
        result = function_under_test()
        
        # Assertion 1: Tipo de retorno
        assert isinstance(result, expected_type), f"Expected {expected_type}, got {type(result)}"
        
        # Assertion 2: Valores específicos
        assert result.property == expected_value, f"Expected {expected_value}, got {result.property}"
        
        # Assertion 3: Estado del sistema
        assert system_state_valid(), "System state invalid after operation"
        
        # Assertion 4: Performance
        execution_time = measure_execution_time()
        assert execution_time < 5.0, f"Performance failed: {execution_time}s > 5s"
        
        # ✅ REGLA #8: Log éxito con métricas
        log_trading_decision_smart_v6("TEST_SUCCESS", {
            "test_name": "test_function_name",
            "execution_time": execution_time,
            "assertions_passed": 4
        })
        
        return True
        
    except Exception as e:
        # ✅ REGLA #8: Log falla con contexto completo
        log_trading_decision_smart_v6("TEST_FAILURE", {
            "test_name": "test_function_name",
            "error": str(e),
            "error_type": type(e).__name__,
            "initial_state": initial_state
        })
        raise
        
    finally:
        # ✅ REGLA #8: Cleanup obligatorio
        cleanup_test_environment()

def main():
    """Main con configuración PowerShell y SIC/SLUC"""
    
    # ✅ REGLA #8: Verificar PYTHONPATH (PowerShell)
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Ejecutar tests con manejo de errores
    test_function_name()

if __name__ == "__main__":
    main()
```

🚨 VERIFICACIONES PRE-TEST OBLIGATORIAS:
- ✅ PYTHONPATH configurado correctamente
- ✅ SIC/SLUC disponibilidad verificada
- ✅ Rutas Windows validadas
- ✅ Python executable correcto identificado
- ✅ Permisos de escritura para logs verificados
- ✅ Dependencies críticas importables
- ✅ Performance baseline establecida

🔍 CRITERIOS DE FALLA DE TEST (SER CRÍTICO):
- ❌ FALLA si execution_time > 5s (enterprise requirement)
- ❌ FALLA si memory_usage excesivo (sin justificación)
- ❌ FALLA si assertions vagas o insuficientes (<3)
- ❌ FALLA si no hay cleanup apropiado
- ❌ FALLA si error handling inexistente
- ❌ FALLA si logging insuficiente o print() usado
- ❌ FALLA si setup/teardown inadecuados
- ❌ FALLA si test no refleja uso real del sistema

🚨 CRÍTICO - NO ACEPTAR TESTS QUE:
- ❌ NO tienen assertions específicas y múltiples
- ❌ NO validan tipos de retorno explícitamente
- ❌ NO incluyen error handling y edge cases
- ❌ NO usan SIC/SLUC cuando está disponible
- ❌ NO funcionan correctamente en PowerShell
- ❌ NO tienen performance <5s validada
- ❌ NO incluyen cleanup apropiado
- ❌ NO documentan qué exactamente están probando
```

---

## 📁 **ESTRUCTURA DE PROYECTO OBLIGATORIA**

### 🎯 **DIRECTORIOS PRINCIPALES:**
```
ict-engine-v6.0-enterprise-sic/
├── core/                    # Lógica principal del sistema
│   ├── analysis/           # Análisis de mercado y memoria
│   ├── data_management/    # Gestión de datos MT5
│   ├── ict_engine/        # Engine ICT y patterns
│   └── smart_money_concepts/ # Smart Money analysis
├── docs/                   # Documentación organizada
│   ├── 04-development-logs/ # Logs especializados
│   │   ├── memoria/        # Documentación memoria trader
│   │   ├── smart-money/    # Smart Money Concepts
│   │   ├── bos-choch/      # Patterns BOS/CHoCH
│   │   ├── performance/    # Optimización y métricas
│   │   ├── testing/        # Tests y validación
│   │   └── integration/    # Integración externa
├── tests/                  # Tests unitarios e integración
├── config/                 # Configuraciones enterprise
└── sistema/               # Sistema SIC v3.1
```

### 🔍 **BÚSQUEDA OBLIGATORIA:**
```
🎯 ANTES DE CREAR, BUSCAR EN:
├── core/analysis/           # ¿Ya existe análisis similar?
├── core/ict_engine/        # ¿Pattern ya implementado?
├── core/smart_money_concepts/ # ¿Smart Money ya cubierto?
├── docs/04-development-logs/ # ¿Ya documentado en bitácoras?
├── tests/                  # ¿Tests ya existen?
└── config/                 # ¿Configuración ya disponible?
```

---

## 🧠 **REGLAS DE MEMORIA Y CONTEXTO**

### 📋 **COMPONENTES DE MEMORIA CRÍTICOS:**
```
🧠 SIEMPRE VERIFICAR:
├── MarketContext          # ¿Necesita contexto de mercado?
├── ICTHistoricalAnalyzer  # ¿Requiere análisis histórico?
├── TradingDecisionCache   # ¿Debe cachear decisiones?
├── UnifiedMarketMemory    # ¿Necesita memoria unificada?
└── MemoryPersistence      # ¿Requiere persistencia?
```

### 🎯 **PREGUNTAS OBLIGATORIAS:**
```
❓ ANTES DE IMPLEMENTAR:
1. ¿Esta función necesita recordar estados anteriores?
2. ¿Debe aprender de experiencias pasadas?
3. ¿Requiere contexto entre sesiones?
4. ¿Debe evitar reprocesar estados similares?
5. ¿Funciona como trader real con memoria?
```

---

## 📊 **REGLAS DE INTEGRACIÓN**

### 🔗 **INTEGRACIÓN OBLIGATORIA:**
```
✅ SIEMPRE INTEGRAR CON:
├── SIC v3.1               # Sistema base obligatorio
├── MT5 Real Data          # Solo datos reales FundedNext
├── SLUC v2.1 Logging      # Logging estructurado
├── UnifiedMarketMemory    # Memoria de trader
├── Smart Trading Logger   # Logger inteligente
└── Performance Monitoring # Métricas enterprise
```

### ❌ **PROHIBIDO:**
```
🚫 NO HACER:
├── Datos simulados        # Solo datos reales MT5
├── Logging básico         # Solo SLUC v2.1
├── Funciones sin memoria  # Trader real requiere memoria
├── Duplicar lógica        # Buscar existente primero
├── Ignorar performance    # <5s response obligatorio
└── Arquitectura legacy    # Solo v6.0 enterprise
```

---

## ⚡ **IMPLEMENTACIÓN PRÁCTICA SIC Y SLUC**

### 🏗️ **TEMPLATE OBLIGATORIO SIC:**
```python
# ✅ CORRECTO - Implementación con SIC
from sistema.sic_bridge import SICBridge
from core.smart_trading_logger import log_trading_decision_smart_v6

def nueva_funcion_ict():
    """Nueva función ICT con SIC obligatorio"""
    
    # 1. Inicializar SIC Bridge
    sic = SICBridge()
    
    # 2. Verificar estado del sistema
    if not sic.is_system_ready():
        log_trading_decision_smart_v6("SYSTEM_ERROR", {
            "error": "SIC system not ready",
            "function": "nueva_funcion_ict"
        })
        return None
    
    # 3. Tu lógica aquí...
    result = tu_logica()
    
    # 4. Log con SLUC
    log_trading_decision_smart_v6("ICT_FUNCTION", {
        "function": "nueva_funcion_ict",
        "result": result,
        "status": "success"
    })
    
    return result
```

### 📝 **TEMPLATE OBLIGATORIO SLUC:**
```python
# ✅ CORRECTO - Logging con SLUC v2.1
from core.smart_trading_logger import (
    log_trading_decision_smart_v6,
    get_trading_decision_cache
)

def funcion_con_memoria():
    """Función con memoria y logging SLUC"""
    
    # 1. Verificar cache inteligente
    cache = get_trading_decision_cache()
    
    # 2. Log inicio con contexto
    log_trading_decision_smart_v6("FUNCTION_START", {
        "function": "funcion_con_memoria",
        "timestamp": datetime.now().isoformat(),
        "cache_stats": cache.get_cache_statistics()
    })
    
    # 3. Tu lógica...
    
    # 4. Log resultados con métricas
    log_trading_decision_smart_v6("FUNCTION_COMPLETE", {
        "function": "funcion_con_memoria",
        "execution_time": tiempo,
        "memory_used": memoria,
        "performance_ok": tiempo < 5.0
    })
```

### 🚨 **EJEMPLOS PROHIBIDOS:**
```python
# ❌ INCORRECTO - Sin SIC ni SLUC
def mala_funcion():
    print("Iniciando función")  # ❌ NO usar print
    # ... lógica sin SIC bridge
    return resultado

# ❌ INCORRECTO - Logging básico
import logging
logger = logging.getLogger(__name__)  # ❌ NO crear loggers independientes
logger.info("Mensaje")  # ❌ NO usar logging básico
```

---

## 🎯 **REGLAS DE PATTERNS ICT**

### 📋 **PATTERNS IMPLEMENTADOS (NO DUPLICAR):**
```
✅ YA IMPLEMENTADOS:
├── BOS (Break of Structure)     # core/ict_engine/pattern_detector.py
├── CHoCH (Change of Character)  # core/ict_engine/pattern_detector.py
├── Liquidity Grabs             # Detectando correctamente
├── Market Structure Analysis   # core/analysis/market_structure_analyzer_v6.py
└── Smart Money Concepts        # core/smart_money_concepts/
```

### 🚀 **PRÓXIMOS PATTERNS (CREAR CUANDO SEA NECESARIO):**
```
🎯 ROADMAP ICT:
├── Order Blocks               # Próxima prioridad
├── Fair Value Gaps (FVG)      # Después de Order Blocks
├── Displacement               # Momentum analysis
├── Liquidity Zones            # Support/Resistance
└── Institutional Order Flow   # Smart money flow
```

---

## 🧪 **REGLAS DE TESTING**

### ✅ **TESTING OBLIGATORIO:**
```
🧪 CADA NUEVA FUNCIÓN DEBE TENER:
├── Unit Tests                 # Tests unitarios
├── Integration Tests          # Tests de integración
├── Memory Tests              # Tests de memoria (si aplica)
├── Performance Tests         # Validación <5s
├── Real Data Tests           # Tests con datos MT5
└── Regression Tests          # Prevenir regresiones
```

### 📊 **MÉTRICAS OBLIGATORIAS:**
```
🎯 VALIDAR SIEMPRE:
├── Response Time: <5s         # Performance enterprise
├── Memory Usage: Optimizado   # Sin memory leaks
├── Accuracy: >70%            # Precisión mínima
├── Error Rate: <0.1%         # Robustez alta
└── Test Coverage: >90%       # Cobertura completa
```

---

## 📝 **REGLAS DE DOCUMENTACIÓN**

### 📋 **DOCUMENTACIÓN OBLIGATORIA:**
```
📄 CADA NUEVA FUNCIÓN REQUIERE:
├── Docstring completo        # Explicación detallada
├── Comentarios en código     # Lógica explicada
├── Actualización bitácora    # docs/04-development-logs/
├── README actualizado        # Si afecta estructura
└── Ejemplos de uso          # Para desarrolladores
```

### 🎯 **BITÁCORAS ESPECIALIZADAS:**
```
📚 ACTUALIZAR SEGÚN TEMA:
├── memoria/                  # Funciones de memoria
├── smart-money/             # Smart Money Concepts
├── bos-choch/               # Patterns BOS/CHoCH
├── performance/             # Optimizaciones
├── testing/                 # Nuevos tests
└── integration/             # Integraciones externas
```

---

## 🚨 **REGLAS DE EMERGENCIA**

### 🔥 **PRIORIDADES CRÍTICAS:**
```
🚨 SIEMPRE PRIORIZAR:
1. Memoria de trader real      # BLOQUEANTE actual
2. Performance <5s            # Enterprise obligatorio
3. Datos reales MT5           # Solo datos reales
4. Tests passing              # 100% tests exitosos
5. No duplicar lógica         # Buscar existente primero
```

### ⚠️ **SEÑALES DE ALERTA:**
```
🚨 DETENER SI:
├── Response time >5s         # Performance no enterprise
├── Tests fallan              # Regresión detectada
├── Memory leaks              # Uso memoria excesivo
├── Duplicación detectada     # Lógica ya existe
└── Sin memoria trader        # Cliente: "no me funciona"
```

---

## 🎯 **CHECKLIST PARA COPILOT**

### ✅ **ANTES DE CADA IMPLEMENTACIÓN:**
```
□ Revisar bitácora relevante
□ Buscar archivos relacionados en TODO el proyecto
□ Verificar si necesita memoria de trader
□ Confirmar integración con SIC v3.1
□ Validar uso de datos reales MT5
□ Asegurar logging SLUC v2.1
□ Verificar performance <5s
□ Planear tests correspondientes
□ Actualizar documentación
□ NO duplicar lógica existente
```

### 🚀 **DURANTE IMPLEMENTACIÓN:**
```
□ Seguir arquitectura v6.0 enterprise
□ Integrar memoria si es necesario
□ Usar datos reales exclusivamente
□ Implementar logging estructurado
□ Optimizar para performance
□ Crear tests comprehensivos
□ Documentar completamente
□ Actualizar bitácoras relevantes
```

### 📊 **DESPUÉS DE IMPLEMENTACIÓN:**
```
□ Ejecutar todos los tests
□ Validar performance <5s
□ Verificar memoria funciona
□ Confirmar integración completa
□ Actualizar documentación
□ Revisar no hay duplicación
□ Commit con mensaje descriptivo
□ Actualizar roadmap si aplica
```

---

## ✅ **CHECKLIST VERIFICACIÓN SIC/SLUC**

### 🔍 **ANTES DE CUALQUIER IMPLEMENTACIÓN:**
```
🏗️ VERIFICACIÓN SIC v3.1:
□ ¿Importé SICBridge desde sistema.sic_bridge?
□ ¿Verifiqué is_system_ready() antes de proceder?
□ ¿Usé el estado centralizado del sistema?
□ ¿Evité crear controles independientes?
□ ¿Integré con los componentes SIC existentes?

📝 VERIFICACIÓN SLUC v2.1:
□ ¿Importé log_trading_decision_smart_v6?
□ ¿Evité usar print() o logging básico?
□ ¿Incluí contexto relevante en logs?
□ ¿Loggué tanto inicio como resultados?
□ ¿Usé el cache inteligente de decisiones?

🧠 VERIFICACIÓN MEMORIA:
□ ¿Consideré si necesita memoria de trader?
□ ¿Integré con UnifiedMarketMemory si es necesario?
□ ¿Evité reprocesar estados similares?
□ ¿Mantuve contexto entre llamadas?

⚡ VERIFICACIÓN PERFORMANCE:
□ ¿Tiempo de respuesta <5s?
□ ¿Evité operaciones costosas innecesarias?
□ ¿Usé cache cuando es apropiado?
□ ¿Validé con datos reales MT5?
```

### 🚨 **CHECKLIST CRÍTICO - NO OMITIR:**
```
❗ OBLIGATORIO ANTES DE COMMIT:
□ ✅ SIC Bridge importado y usado correctamente
□ ✅ SLUC logging implementado (NO print/logging básico)
□ ✅ Memoria de trader considerada y aplicada
□ ✅ Performance <5s validada
□ ✅ Tests escritos y pasando
□ ✅ Documentación actualizada
□ ✅ Sin duplicación de lógica existente
□ ✅ Integración completa con v6.0 enterprise

📋 VERIFICACIÓN REGLA #5 - CONTROL DE PROGRESO:
□ ✅ Bitácora correspondiente identificada y actualizada
□ ✅ Checklist de fase/componente marcado como completado
□ ✅ Test con datos REALES ejecutado exitosamente
□ ✅ Métricas de performance documentadas
□ ✅ Victoria registrada con timestamp y duración
□ ✅ Lecciones aprendidas documentadas
□ ✅ Próximos pasos actualizados en roadmap
□ ✅ Impacto en sistema general evaluado

🔢 VERIFICACIÓN REGLA #6 - CONTROL DE VERSIONES:
□ ✅ Impacto del cambio evaluado (MAJOR/MINOR/PATCH)
□ ✅ Justificación para incremento de versión documentada
□ ✅ Versiones actualizadas coherentemente en todos los archivos
□ ✅ CHANGELOG o bitácora actualizada con cambios
□ ✅ Consistencia de versiones verificada en todo el proyecto
□ ✅ Docstrings y headers actualizados con nueva versión
□ ✅ README y documentación principal actualizada
□ ✅ No hay versiones contradictorias en archivos distintos

🧪 VERIFICACIÓN REGLA #7 - TESTS PRIMERO:
□ ✅ Test analizado completamente antes de cualquier modificación
□ ✅ Lógica del test verificada como correcta/incorrecta
□ ✅ Si test correcto → código modificado, NO el test
□ ✅ Si test incorrecto → razón documentada en SLUC
□ ✅ Decisión de modificar código vs test documentada
□ ✅ Evidencia del análisis registrada en bitácora
□ ✅ Test modificado solo cuando lógica era realmente incorrecta
□ ✅ Lecciones aprendidas sobre testing documentadas

🧪 VERIFICACIÓN REGLA #8 - TESTING CRÍTICO SIC/SLUC:
□ ✅ SICBridge importado en tests que lo requieren
□ ✅ log_trading_decision_smart_v6 usado para logging (NO print)
□ ✅ PYTHONPATH configurado correctamente para PowerShell
□ ✅ Rutas Windows absolutas utilizadas correctamente
□ ✅ Test tiene mínimo 3-5 assertions específicas
□ ✅ Tipos de retorno validados explícitamente
□ ✅ Error handling y edge cases incluidos
□ ✅ Performance <5s validada en test
□ ✅ Cleanup/teardown apropiado implementado
□ ✅ Test documenta exactamente qué está probando
□ ✅ Test funciona correctamente en entorno PowerShell
□ ✅ Setup inicial y estado final validados
```

📋 VERIFICACIÓN REGLA #10 - DOCUMENTACIÓN CRÍTICA:
```
□ ✅ BITACORA_DESARROLLO_SMART_MONEY_v6.md actualizada
□ ✅ QUE_SIGUE_WEEKEND_PLAN.md actualizada  
□ ✅ roadmap_v6.md actualizada
□ ✅ PLAN_FAIR_VALUE_GAPS_FVG.md actualizada
□ ✅ TODOS los logros documentados correctamente
□ ✅ Próximos pasos claramente definidos
□ ✅ Consistencia entre TODOS los documentos verificada
□ ✅ NO proceder sin documentación 100% al día
```

---

## � **REGLA #14: LIMPIEZA Y ESTILO DE CÓDIGO AUTOMÁTICO**

### 🎯 **OBJETIVO:**
**Mantener el código libre de advertencias de linting y siguiendo estándares de estilo enterprise automáticamente.**

### ✅ **COPILOT DEBE DETECTAR Y CORREGIR AUTOMÁTICAMENTE:**

#### **14.1 Detección Automática Obligatoria:**
```
🔍 DETECTAR INMEDIATAMENTE:
- ✅ Unused imports (W0611:unused-import)
- ✅ Wrong import order (C0411:wrong-import-order)  
- ✅ Trailing whitespace (C0303:trailing-whitespace)
- ✅ Variables in type expressions (reportInvalidTypeForm)
- ✅ Otros errores/advertencias de Pylint o Pylance
- ✅ Imports no usados por refactoring
- ✅ Definiciones duplicadas con nombres diferentes
```

#### **14.2 Correcciones Automáticas Requeridas:**
```
🛠️ APLICAR CORRECCIONES INMEDIATAS:
1. ✅ Eliminar imports no usados completamente
2. ✅ Ordenar imports correctamente:
   - Estándar (datetime, os, sys)
   - Terceros (pandas, numpy)  
   - Internos (core.*, sistema.*)
3. ✅ Eliminar espacios al final de líneas
4. ✅ Corregir type hints con variables por tipos válidos
5. ✅ Unificar nomenclatura inconsistente detectada
6. ✅ Registrar cambios en SLUC si son estructurales
```

#### **14.3 Orden de Imports Enterprise Standard:**
```python
# ✅ ORDEN CORRECTO OBLIGATORIO:

# 1. Estándar
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import os
import sys

# 2. Terceros
import pandas as pd
import numpy as np

# 3. Internos - SIC/SLUC Enterprise
from core.smart_trading_logger import SmartTradingLogger
from core.data_management.unified_memory_system import UnifiedMemorySystem
from core.ict_engine.ict_types import TradingDirection
```

#### **14.4 Integración con SLUC para Cambios Estructurales:**
```python
# 📝 TEMPLATE DE LOGGING PARA CORRECCIONES AUTOMÁTICAS:

if self.logger:
    self.logger.log_info(f"🧹 Auto-corrección aplicada: eliminados {removed_imports} imports no usados", "auto_lint")
    self.logger.log_debug(f"📐 Orden de imports corregido en {filename}", "auto_lint")
    if unified_names:
        self.logger.log_warning(f"🔗 Nomenclatura unificada: {old_name} → {new_name}", "auto_lint")
```

### 🚨 **REGLAS CRÍTICAS:**

#### **14.5 Prohibiciones Absolutas:**
```
❌ NUNCA HACER:
- ❌ Dejar warnings activos antes de commit
- ❌ Ignorar mensajes de Pylint/Pylance sin corregir
- ❌ Mezclar imports estándar con terceros sin separar
- ❌ Crear nuevas funciones con nombres diferentes para el mismo propósito
- ❌ Usar variables en type annotations en lugar de tipos
- ❌ Dejar espacios en blanco al final de líneas
```

#### **14.6 Validación Pre-Commit Obligatoria:**
```bash
# 🔍 COMANDO OBLIGATORIO ANTES DE CUALQUIER COMMIT:
pylint core/ tests/ --disable=C0103,R0913,R0914,R0915 --score=y
```

#### **14.7 Detección de Nomenclatura Inconsistente:**
```
🔗 UNIFICACIÓN DE DEFINICIONES CRÍTICA:
- ✅ Buscar funciones duplicadas con nombres diferentes
- ✅ Detectar clases que hacen lo mismo con nomenclatura distinta  
- ✅ Identificar variables/métodos que referencian el mismo concepto
- ✅ Proponer unificación siguiendo el patrón enterprise
- ✅ Mantener glosario central en DEFINICIONES_CLAVE.md
```

### 📋 **EJEMPLO DE CORRECCIÓN AUTOMÁTICA:**
```python
# ❌ ANTES (CON PROBLEMAS):
import pandas as pd
import numpy as np  # No usado
from datetime import datetime  # Mal ordenado

class BreakerDetector:
    def detect(self, data: precio_data):  # Variable en type hint
        pass    # Espacio al final

# ✅ DESPUÉS (CORREGIDO POR COPILOT):
from datetime import datetime
import pandas as pd

class BreakerDetector:
    def detect(self, data: pd.DataFrame):
        pass
```

### 🎯 **INTEGRACIÓN CON REGLAS EXISTENTES:**
```
🔗 ESTA REGLA SE INTEGRA CON:
- REGLA #4: Sistema SIC y SLUC obligatorio (logging de correcciones)
- REGLA #8: Testing con SLUC (tests limpios sin warnings)
- REGLA #10: Verificación de documentación (código limpio para commit)
- REGLA #12: Test principal de fases (tests enterprise evolutivos)
- REGLA #13: Control de evolución tests (eliminar fallos por imports)
```

---

### 🔄 **REGLA #13: CONTROL DE EVOLUCIÓN DE TESTS Y NOMENCLATURA ENTERPRISE**

### 🎯 **PRINCIPIO DE EVOLUCIÓN CONTINUA:**
**"LOS TESTS DEBEN EVOLUCIONAR CON EL SISTEMA Y USAR NOMENCLATURA ENTERPRISE RECONOCIBLE"**

#### **13.1 Nomenclatura Enterprise Obligatoria:**
```
📁 ARCHIVOS DE TEST ENTERPRISE - NOMENCLATURA ESTÁNDAR:
- ✅ test_fases_advanced_patterns_enterprise.py (PRINCIPAL)
- ✅ test_core_modules_enterprise.py
- ✅ test_integration_enterprise.py  
- ✅ test_performance_enterprise.py
- ✅ test_memory_enterprise.py

🎯 PATRÓN OBLIGATORIO: test_[scope]_[functionality]_enterprise.py
- scope: fases, core, integration, performance, memory
- functionality: específica del área (advanced_patterns, sic_sluc, etc.)
- enterprise: sufijo obligatorio para tests críticos
```

#### **13.2 Evolución Automática de Tests:**
```
🔄 CADA VEZ QUE SE IMPLEMENTE:
- ✅ Nueva fase → Actualizar test_fases_advanced_patterns_enterprise.py
- ✅ Nuevo módulo core → Actualizar test_core_modules_enterprise.py
- ✅ Nueva integración → Actualizar test_integration_enterprise.py
- ✅ Optimización → Validar en test_performance_enterprise.py
- ✅ Memoria nueva → Validar en test_memory_enterprise.py

🧪 CRITERIOS DE ACTUALIZACIÓN:
- ✅ Agregar tests para nueva funcionalidad inmediatamente
- ✅ Mantener backward compatibility con tests existentes
- ✅ Incrementar coverage sin degradar performance
- ✅ Asegurar que tests reflejen estado real del sistema
```

#### **13.3 Eliminación de Fallos por Imports y Dependencias:**
```
🔧 CORRECCIÓN AUTOMÁTICA OBLIGATORIA:
- ✅ Detectar imports obsoletos automáticamente
- ✅ Actualizar imports cuando módulos cambien de ubicación
- ✅ Verificar que todas las dependencias estén disponibles
- ✅ Corregir type hints inconsistentes en tests
- ✅ Eliminar referencias a módulos deprecados
- ✅ Unificar nomenclatura de funciones de test factory

🎯 TEMPLATE IMPORTS ENTERPRISE STANDARD:
```python
#!/usr/bin/env python3
"""
🧪 TEST [NOMBRE] ENTERPRISE - v[VERSION]
====================================
✅ REGLA #13: Nomenclatura y evolución enterprise
"""

# ✅ REGLA #13: Imports estándar enterprise
from datetime import datetime
from typing import Dict, List, Optional, Any
import sys
from pathlib import Path

# ✅ REGLA #13: SIC/SLUC enterprise obligatorio
try:
    from sistema.sic_bridge import SICBridge
    from core.smart_trading_logger import log_trading_decision_smart_v6
    ENTERPRISE_READY = True
except ImportError:
    ENTERPRISE_READY = False
    def log_trading_decision_smart_v6(event, data, **kwargs):
        print(f"[FALLBACK] {event}: {data}")

# ✅ REGLA #13: Tests factories unificados
from tests.test_factories.enterprise_test_factories import (
    create_test_market_data,
    create_test_trading_context,
    create_test_memory_state
)
```

#### **13.4 Migración de Tests Legacy a Enterprise:**
```
🚀 PROCESO DE MIGRACIÓN OBLIGATORIO:

📋 RENOMBRAR ARCHIVOS SEGÚN ESTÁNDAR:
- test_fase5_advanced_patterns_enterprise.py → test_fases_advanced_patterns_enterprise.py
- test_old_name.py → test_[scope]_[functionality]_enterprise.py
- Mantener historial de cambios en CHANGELOG

🔄 ACTUALIZAR CONTENIDO:
- ✅ Aplicar REGLA #12 (test principal de fases)
- ✅ Usar nomenclatura enterprise estándar
- ✅ Integrar con SIC/SLUC obligatoriamente
- ✅ Validar performance <5s enterprise
- ✅ Incluir detección de fallos menores
```

#### **13.5 Validación de Evolución:**
```
📊 MÉTRICAS DE EVOLUCIÓN OBLIGATORIAS:
- ✅ Test coverage no debe decrecer al evolucionar
- ✅ Performance debe mantenerse <5s al agregar tests
- ✅ Pass rate debe mantenerse >90% post-evolución
- ✅ Nuevos tests deben seguir template enterprise
- ✅ Imports deben estar limpios (sin warnings)
- ✅ Nomenclatura debe ser consistente enterprise-wide

🔍 VALIDACIÓN PRE-COMMIT:
- ✅ Ejecutar test_fases_advanced_patterns_enterprise.py completo
- ✅ Verificar que no hay imports rotos
- ✅ Confirmar nomenclatura enterprise en archivos nuevos
- ✅ Validar que tests evolucionaron correctamente
```

---
```

---

## �📞 **CONTACTO Y ESCALACIÓN**

### 🚨 **CUANDO ESCALAR:**
- Si encuentras lógica duplicada
- Si performance >5s no se puede resolver
- Si memoria de trader no está clara
- Si tests fallan sin solución clara
- Si arquitectura legacy se detecta

### 🎯 **RECURSOS DE AYUDA:**
- **Bitácoras:** `docs/04-development-logs/`
- **Arquitectura:** `docs/02-architecture/`
- **Config:** `config/` directory
- **Tests:** `tests/` directory  
- **Memoria:** `docs/04-development-logs/memoria/`

---

## 🧪 **REGLA #11: TESTING ESTRATÉGICO CON DATOS REALES MT5**

### 🎯 **PRINCIPIO FUNDAMENTAL:**
```
🚨 CRÍTICO: Testing con datos reales MT5 SOLO cuando módulos estén 100% completos

📊 ESTRATEGIA DE TESTING FASE A FASE:
- ✅ Completar 100% implementación del módulo
- ✅ Validar todos los métodos de detección  
- ✅ Verificar integración enterprise
- ✅ ENTONCES ejecutar testing con datos reales MT5
- ❌ NO testing prematuro con datos parciales
```

### 📋 **PROTOCOLO DE TESTING MODULAR:**

#### 🔍 **FASE 1: VALIDACIÓN DE COMPLETITUD**
```python
# CHECKLIST OBLIGATORIO ANTES DE TESTING REAL:
✅ Todos los métodos detect_* implementados
✅ Clases enterprise inicializadas correctamente  
✅ Integración con UnifiedMemorySystem verificada
✅ SIC v3.1 + SLUC v2.1 conectados
✅ Performance <5s enterprise validada
✅ Zero import errors o dependencias faltantes
```

#### 🎯 **FASE 2: ESTRATEGIA BOS (Break of Structure)**
```python
# MÓDULO BOS - INTEGRACIÓN OBLIGATORIA AL TESTING:
📦 Detectores a incluir:
   - ICTPatternDetector (detect_bos_with_memory)
   - ICTPatternDetector (detect_choch_with_memory) 
   - BreakerBlockDetectorEnterprise (detect_breaker_blocks)
   - Displacement + Structure analysis

📊 Métricas BOS específicas:
   - Precisión detección BOS vs CHOCH
   - Timeframe validation (H4→M15→M5)
   - Institutional vs Retail classification
   - Memory-enhanced detection rate
   - Multi-pattern confluence con BOS
```

#### ⚡ **FASE 3: TESTING REAL MT5 - PROTOCOLO**
```python
# EJECUTAR SOLO CUANDO 100% COMPLETO:
def run_enterprise_testing_protocol():
    """
    Protocol for real MT5 data testing - Enterprise Grade
    """
    # 1. Pre-validation
    validate_module_completeness()
    validate_enterprise_integration() 
    validate_memory_system_active()
    
    # 2. BOS-Specific Testing
    test_bos_detection_accuracy()
    test_bos_vs_choch_differentiation()
    test_bos_multi_timeframe_validation()
    test_bos_institutional_classification()
    
    # 3. Real Data Execution
    execute_detector_performance_dashboard()
    generate_bos_specific_metrics()
    validate_enterprise_performance_criteria()
    
    # 4. Results Validation
    ensure_precision_above_75_percent()
    ensure_coverage_meets_enterprise_standards()
    ensure_performance_under_5_seconds()
```

### 🔧 **IMPLEMENTACIÓN INMEDIATA:**

#### 📊 **AÑADIR BOS AL DETECTOR DASHBOARD:**
```python
# AGREGAR A detector_performance_dashboard.py:

"BOS Detector": ICTPatternDetector(),  # detect_bos_with_memory
"CHOCH Detector": ICTPatternDetector(), # detect_choch_with_memory

# Análisis específico BOS:
elif module_name == "BOS Detector":
    patterns = detector.detect_bos_with_memory(df, timeframe=timeframe, symbol=symbol)
    signals = len([p for p in patterns if p.get('bos_strength', 0) > 0.6])

elif module_name == "CHOCH Detector":
    patterns = detector.detect_choch_with_memory(df, timeframe=timeframe, symbol=symbol)
    signals = len([p for p in patterns if p.get('choch_confidence', 0) > 0.7])
```

### 🎯 **REGLAS DE EJECUCIÓN:**

#### ✅ **CUÁNDO EJECUTAR TESTING REAL:**
- ✅ Módulo 100% implementado y funcional
- ✅ Todos los detect_* methods operativos
- ✅ Zero errores de import o dependencias
- ✅ Integración enterprise verificada
- ✅ Performance pre-validada en tests unitarios

#### ❌ **CUÁNDO NO EJECUTAR:**
- ❌ Módulo parcialmente implementado
- ❌ Métodos detect_* retornando []
- ❌ Import errors o warnings críticos
- ❌ Performance >5s en tests básicos
- ❌ Memoria UnifiedMemorySystem no conectada

### 📈 **MÉTRICAS DE ÉXITO BOS:**
```yaml
🎯 BOS Detection Targets:
  Precisión_BOS: >80%
  Precisión_CHOCH: >75% 
  Diferenciación_BOS_vs_CHOCH: >85%
  Multi_timeframe_accuracy: >70%
  Institutional_classification: >80%
  Performance_enterprise: <5s
  Memory_enhanced_detection: +15% vs basic
```

---

**Creado por:** ICT Engine v6.0 Enterprise Team  
**Fecha:** Agosto 9, 2025  
**Versión:** 1.1 - BOS Testing Strategy Added  
**Estado:** 📋 **ACTIVO Y OBLIGATORIO PARA COPILOT**

---

## 🔄 **ACTUALIZACIÓN DE REGLAS**

Este archivo debe actualizarse cuando:
- Se implementen nuevos componentes críticos
- Se identifiquen nuevos patrones de duplicación
- Se cambien prioridades del proyecto
- Se agreguen nuevas reglas de arquitectura
- Se detecten problemas recurrentes

**Próxima revisión:** Post-implementación testing BOS real
