# 📁 TESTE - Tests Futuros del ICT Engine v5.0

Este directorio está preparado para albergar todos los tests futuros del sistema.

## 📋 **Estructura Planificada**

```
teste/
├── __init__.py                    # Configuración base de tests
├── README.md                      # Esta documentación
├── conftest.py                    # Configuración pytest (futuro)
├── teste_dashboard.py             # Tests del dashboard
├── teste_ict_engine.py            # Tests del motor ICT
├── teste_poi_system.py            # Tests del sistema POI
├── teste_mt5_integration.py       # Tests de integración MT5
├── teste_candle_data.py           # Tests de datos de velas
├── teste_trading_logic.py         # Tests de lógica de trading
└── fixtures/                      # Datos de prueba (futuro)
```

## 🔧 **Convenciones de Naming**

- **Prefijo**: `teste_` para todos los archivos de test
- **Funciones**: `def teste_nombre_funcionalidad()`
- **Clases**: `class TesteClassName:`
- **Fixtures**: En directorio `fixtures/`

## 🚀 **Framework Seleccionado**

- **pytest** - Framework principal
- **Coverage** - Medición de cobertura
- **Mock** - Para simulaciones
- **Fixtures** - Datos de prueba

## 📊 **Tipos de Tests Planificados**

### 🧪 **Tests Unitarios**
- Funciones individuales
- Clases aisladas
- Componentes específicos

### 🔗 **Tests de Integración**
- Dashboard + ICT Engine
- MT5 + Data Pipeline
- POI System + Trading Logic

### 🎯 **Tests End-to-End**
- Flujo completo de trading
- Dashboard interactivo
- Conectividad MT5

## 📝 **Comandos Futuros**

```bash
# Ejecutar todos los tests
python -m pytest teste/

# Ejecutar tests específicos
python -m pytest teste/teste_dashboard.py

# Con cobertura
python -m pytest teste/ --cov=core --cov=dashboard

# Solo tests unitarios
python -m pytest teste/ -m "unit"

# Solo tests de integración
python -m pytest teste/ -m "integration"
```

## 🎯 **Estado Actual**

- ✅ Directorio creado
- ✅ Estructura planificada
- ✅ Documentación preparada
- ⏳ Tests pendientes de implementación

## 📅 **Creado**

- **Fecha**: 05 Agosto 2025
- **Propósito**: Preparación para tests futuros
- **Estado**: Listo para implementación

---

*Cuando estés listo para implementar tests, simplemente crea los archivos `teste_*.py` en este directorio siguiendo las convenciones establecidas.*
