# 📊 04-DATA - Datos y Resultados

## 📂 Estructura de Datos

### 📁 **candles/** - Datos de Mercado (Velas)
```
📄 [Archivos de datos de mercado aquí]
```

### 📁 **backtest-results/** - Resultados de Backtesting
```
📄 [Resultados de backtesting organizados]
```

### 📁 **exports/** - Datos Exportados
```
📄 [Datos exportados del sistema]
```

### 📁 **cache/** - Sistema de Cache
```
📄 [Cache del sistema]
```

### 📁 **cache-original/** - Cache Original (Migrado)
```
📂 memory/                        # Cache de memoria
   ├── historical_analysis/       # Análisis histórico
   └── unified/                   # Cache unificado
```

### 📁 **data/** - Datos Principales del Sistema
```
📂 analysis/                      # Datos de análisis
📂 backtest_results/              # Resultados de backtest
   ├── modular_backtest_fractal_v62_20250810_122043.json  # ✅ Test completado
   ├── modular_backtest_fractal_v62_20250810_122233.json  # ✅ Test validado
   └── [Otros resultados]
📂 blackbox/                      # Datos blackbox
📂 candles/                       # Datos de velas
   ├── EURUSD_M5_*.csv           # Datos EURUSD M5
   ├── GBPUSD_H1_*.csv           # Datos GBPUSD H1
   ├── XAUUSD_H4_*.csv           # Datos XAUUSD H4
   └── [72+ archivos de datos MT5]
📂 dashboard_results/             # Resultados del dashboard
📂 exports/                       # Datos exportados
📂 logs/                         # Logs de datos
📂 memory_persistence/           # Persistencia de memoria
📂 patterns/                     # Datos de patrones
📂 regla10_results/             # Resultados REGLA #10
```

---

## 📊 **Datos Principales**

### 💹 **Datos de Mercado (MT5):**
- **Símbolos:** EURUSD, AUDUSD, GBPUSD, USDCHF, XAUUSD
- **Timeframes:** M5, M15, H1, H4
- **Archivos:** 72+ archivos CSV
- **Rango:** 2023-08-30 → 2025-08-10

### 🧪 **Resultados de Testing:**
- **Último Test:** `modular_backtest_fractal_v62_20250810_122233.json`
- **Patterns Detectados:** 65,577
- **Signals Generados:** 59,860
- **Success Rate:** 98.8%
- **Grade:** A+ (EXCELLENT - v6.2 Enhanced)

### 🧱 **Breaker Blocks v6.2 - Datos Validados:**
```json
{
  "🧱 Breaker Blocks": {
    "patterns_detected": 542,
    "signals_generated": 0,
    "success_rate": 100.0,
    "execution_time": 3.76,
    "data_points_analyzed": 297972,
    "status": "SUCCESS"
  }
}
```

---

## 🎯 **Acceso a Datos**

### 📈 **Datos de Mercado:**
```bash
cd 04-DATA/data/candles/
ls -la *EURUSD*M5*.csv  # Datos EURUSD M5
ls -la *GBPUSD*H1*.csv  # Datos GBPUSD H1
```

### 📊 **Resultados de Backtest:**
```bash
cd 04-DATA/data/backtest_results/
cat modular_backtest_fractal_v62_*.json | jq .
```

### 💾 **Cache del Sistema:**
```bash
cd 04-DATA/cache-original/
ls -la memory/
```

---

## 📋 **Estructura de Archivos de Datos**

### 📊 **Formato de Datos de Mercado:**
```csv
timestamp,open,high,low,close,volume
2025-01-10 00:00:00,1.12345,1.12380,1.12300,1.12350,1500
...
```

### 📈 **Formato de Resultados de Backtest:**
```json
{
  "summary": {
    "total_execution_time": 29.94,
    "total_data_points": 703390,
    "total_patterns": 65577,
    "total_signals": 59860,
    "overall_success_rate": 98.8
  },
  "module_results": {
    "🧱 Breaker Blocks": { ... },
    "📏 Fair Value Gaps": { ... },
    ...
  }
}
```

---

## ⚡ **Comandos Útiles**

### 🔍 **Análisis de Datos:**
```bash
# Contar archivos de datos
find 04-DATA/data/candles/ -name "*.csv" | wc -l

# Ver últimos resultados
ls -la 04-DATA/data/backtest_results/ | tail -5

# Análizar tamaño de datos
du -sh 04-DATA/data/candles/
```

### 📊 **Procesamiento de Resultados:**
```bash
# Ver resumen de último test
jq '.summary' 04-DATA/data/backtest_results/modular_backtest_fractal_v62_*.json

# Extraer métricas de Breaker Blocks
jq '.module_results."🧱 Breaker Blocks"' 04-DATA/data/backtest_results/modular_backtest_fractal_v62_*.json
```

---

## 🚀 **Datos Organizados y Optimizados**

### ✅ **Estado Actual:**
- ✅ **Datos MT5:** Completamente organizados
- ✅ **Resultados de Testing:** Validados y documentados
- ✅ **Cache:** Optimizado y estructurado
- ✅ **Exports:** Listos para análisis

### 📈 **Métricas de Datos:**
- **Total Data Points:** 703,390+
- **Archivos CSV:** 72+
- **Tests Ejecutados:** Múltiples validaciones
- **Success Rate:** 98.8%

---

**✅ SISTEMA DE DATOS COMPLETAMENTE ORGANIZADO Y VALIDADO** ✅
