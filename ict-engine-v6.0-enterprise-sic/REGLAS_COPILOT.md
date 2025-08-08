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
- ✅ Timestamp y duración de implementación
- ✅ Lecciones aprendidas y mejoras
- ✅ Impacto en sistema general
- ✅ Próximos pasos sugeridos

🚨 CRÍTICO - NO CONTINUAR SIN:
- ❌ NO pasar a siguiente fase sin marcar checks
- ❌ NO implementar nuevo código sin test real
- ❌ NO cerrar tarea sin actualizar bitácora
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

### 🔢 **REGLA #6: CONTROL DE VERSIONES INTELIGENTE**
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

---

## 📞 **CONTACTO Y ESCALACIÓN**

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

**Creado por:** ICT Engine v6.0 Enterprise Team  
**Fecha:** Agosto 8, 2025  
**Versión:** 1.0  
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
