# 🗂️ ANÁLISIS DE NODOS - Dependencias BOS Migration

## 📊 **INVENTARIO COMPLETO DE NODOS**

### **NODOS ORIGEN (Sistema Principal)**
```yaml
SOURCE_NODES:
  market_structure_v2.py:
    class: MarketStructureEngine
    methods:
      - _detect_swing_points()      # ✅ Funcional
      - _detect_structure_change()  # ✅ Funcional  
      - _is_range_bound()          # ✅ Funcional
      - _analyze_momentum()        # ✅ Funcional
    dependencies:
      - sistema.sic.enviar_senal_log
      - sistema.sic.datetime
      - sistema.sic.dataclass
      - ..ict_types.TradingDirection
    enums:
      - StructureType              # ✅ BOS_BULLISH, BOS_BEARISH
    dataclasses:
      - MarketStructureSignal      # ✅ Completo
      - FairValueGap              # ✅ Completo
      - OrderBlock                # ✅ Completo
```

### **NODOS DESTINO (Enterprise v6.0)**
```yaml
TARGET_NODES:
  market_structure_analyzer_v6.py:
    class: MarketStructureAnalyzerV6
    methods:
      - _detect_swing_points()      # ⚠️ Implementado básico
      - _detect_structure_change()  # ❌ VACÍO - MIGRAR AQUÍ
      - _is_range_bound()          # ❌ NO EXISTE - CREAR
      - _analyze_momentum()        # ❌ NO EXISTE - CREAR
    dependencies:
      - core.smart_trading_logger
      - datetime (stdlib)
      - dataclasses (stdlib)
      - core.ict_engine.ict_types.TradingDirection
    enums:
      - StructureTypeV6            # ✅ BOS_BULLISH, BOS_BEARISH
    dataclasses:
      - MarketStructureSignalV6    # ✅ Definido
      - FVGTypeV6                 # ✅ Definido
      - OrderBlockTypeV6          # ✅ Definido

  pattern_detector.py:
    class: PatternDetector  
    methods:
      - detect_bos()              # ❌ NO EXISTE - IMPLEMENTAR
      - detect_choch()            # ❌ NO EXISTE - IMPLEMENTAR
      - detect_fvg()              # ❌ NO EXISTE - IMPLEMENTAR
```

## 🔗 **MAPEO DE DEPENDENCIAS**

### **MATRIZ DE CONVERSIÓN**
| **Origen** | **Destino** | **Status** | **Acción** |
|------------|-------------|------------|------------|
| `sistema.sic.enviar_senal_log` | `SmartTradingLogger.debug()` | 🔄 Convertible | Reemplazar |
| `sistema.sic.datetime` | `datetime (stdlib)` | ✅ Directo | Cambiar import |
| `sistema.sic.dataclass` | `dataclasses (stdlib)` | ✅ Directo | Cambiar import |
| `..ict_types.TradingDirection` | `core.ict_engine.ict_types.TradingDirection` | ✅ Equivalente | Actualizar path |
| `StructureType` | `StructureTypeV6` | ✅ Compatible | Renombrar |
| `MarketStructureSignal` | `MarketStructureSignalV6` | ✅ Compatible | Adaptar campos |

### **DEPENDENCIAS CRÍTICAS IDENTIFICADAS**
```python
# === NODOS DE LOGGING ===
# ORIGEN:
from sistema.sic import enviar_senal_log
enviar_senal_log("DEBUG", f"🔍 BOS BULLISH detectado @ {break_level:.5f}", __name__, "market_structure")

# DESTINO:
from core.smart_trading_logger import SmartTradingLogger
self.logger = SmartTradingLogger(module_name='market_structure_v6')
self.logger.debug(f"🔍 BOS BULLISH v6.0 detectado @ {break_level:.5f}")

# === NODOS DE TIPOS ===
# ORIGEN:
from ..ict_types import TradingDirection
if self.current_trend == TradingDirection.SELL:

# DESTINO:  
from core.ict_engine.ict_types import TradingDirection
if self.current_trend == TradingDirection.BEARISH:

# === NODOS DE CONFIGURACIÓN ===
# ORIGEN:
swing_window = 5  # Hardcoded en sistema principal

# DESTINO:
from config.performance_config_enterprise import ANALYSIS_CONFIG
swing_window = ANALYSIS_CONFIG.get('structure', {}).get('swing_window', 5)
```

## 🔧 **ADAPTADORES ESPECÍFICOS**

### **Adaptador de Logging**
```python
class LoggingAdapter:
    """Convierte llamadas de logging del sistema principal al enterprise"""
    
    def __init__(self, logger: SmartTradingLogger):
        self.logger = logger
    
    def enviar_senal_log(self, level: str, message: str, module: str, category: str):
        """Emula la función enviar_senal_log del sistema principal"""
        formatted_message = f"[{category}] {message}"
        
        if level == "DEBUG":
            self.logger.debug(formatted_message)
        elif level == "INFO":
            self.logger.info(formatted_message)
        elif level == "WARNING":
            self.logger.warning(formatted_message)
        elif level == "ERROR":
            self.logger.error(formatted_message)
```

### **Adaptador de Enums**
```python
class EnumAdapter:
    """Convierte enums entre sistemas"""
    
    STRUCTURE_MAPPING = {
        'CHOCH_BULLISH': 'CHOCH_BULLISH',
        'CHOCH_BEARISH': 'CHOCH_BEARISH',
        'BOS_BULLISH': 'BOS_BULLISH',
        'BOS_BEARISH': 'BOS_BEARISH',
        'RANGE_BOUND': 'RANGE_BOUND',
        'CONSOLIDATION': 'CONSOLIDATION',
        'UNKNOWN': 'UNKNOWN'
    }
    
    DIRECTION_MAPPING = {
        'BUY': 'BULLISH',
        'SELL': 'BEARISH'
    }
    
    @classmethod
    def convert_structure_type(cls, old_type: str) -> str:
        return cls.STRUCTURE_MAPPING.get(old_type, 'UNKNOWN')
    
    @classmethod  
    def convert_trading_direction(cls, old_direction: str) -> str:
        return cls.DIRECTION_MAPPING.get(old_direction, 'NEUTRAL')
```

### **Adaptador de DataClasses**
```python
class DataClassAdapter:
    """Convierte dataclasses entre sistemas"""
    
    @staticmethod
    def convert_market_structure_signal(old_signal: dict) -> dict:
        """Convierte MarketStructureSignal a MarketStructureSignalV6"""
        return {
            'structure_type': EnumAdapter.convert_structure_type(old_signal.get('structure_type')),
            'confidence': old_signal.get('confidence', 0.0),
            'direction': EnumAdapter.convert_trading_direction(old_signal.get('direction')),
            'break_level': old_signal.get('break_level', 0.0),
            'target_level': old_signal.get('target_level', 0.0),
            'narrative': old_signal.get('narrative', ''),
            'timestamp': old_signal.get('timestamp'),
            'timeframe': old_signal.get('timeframe', 'M15'),
            'confluence_score': old_signal.get('confluence_score', 0.0),
            'fvg_present': old_signal.get('fvg_present', False),
            'order_block_present': old_signal.get('order_block_present', False),
            # Campos adicionales v6.0
            'liquidity_grab': False,
            'market_reversal': False,
            'session_context': 'unknown'
        }
```

## 📋 **CHECKLIST DE NODOS**

### **NODOS A MIGRAR**
- [ ] `_detect_swing_points()` - **Copiar lógica completa**
- [ ] `_detect_structure_change()` - **Migrar algoritmo BOS/CHoCH**
- [ ] `_is_range_bound()` - **Copiar función filtro**
- [ ] `_analyze_momentum()` - **Migrar análisis momentum**

### **NODOS A CREAR**
- [ ] `detect_bos()` en PatternDetector - **Crear desde lógica migrada**
- [ ] `detect_choch()` en PatternDetector - **Crear desde lógica migrada**
- [ ] Adaptadores de compatibilidad - **Crear nuevos**

### **NODOS A VALIDAR**
- [ ] Imports resueltos - **Verificar dependencias**
- [ ] Enums mapeados - **Verificar compatibilidad**
- [ ] Logging funcionando - **Verificar outputs**
- [ ] DataClasses adaptados - **Verificar estructura**

## 🎯 **PLAN DE EJECUCIÓN DE NODOS**

### **PASO 1: Preparación (30 min)**
1. Copiar `market_structure_v2.py` como referencia
2. Identificar todas las dependencias
3. Crear adaptadores base

### **PASO 2: Migración Core (3 horas)**
1. Migrar `_detect_swing_points()` completo
2. Migrar `_detect_structure_change()` con algoritmo BOS
3. Migrar funciones auxiliares (`_is_range_bound`, `_analyze_momentum`)

### **PASO 3: Implementación PatternDetector (2 horas)**
1. Crear `detect_bos()` usando lógica migrada
2. Crear `detect_choch()` usando lógica migrada
3. Integrar con MarketStructureAnalyzerV6

### **PASO 4: Validación y Testing (2 horas)**
1. Tests unitarios para cada nodo migrado
2. Tests de integración entre nodos
3. Validación con datos reales

---

**Estado**: 📋 PLAN DOCUMENTADO - LISTO PARA EJECUCIÓN  
**Próximo**: 🚀 Comenzar migración de nodos críticos
