# 🧪 Tests - ICT Engine v5.0

## 📋 **Descripción**

Directorio de pruebas y testing del sistema ICT Engine v5.0. Contiene scripts de verificación y validación de componentes del sistema.

## 📁 **Contenido**

### 🔬 **Tests de Integración**
- `test_candle_integration.py` - Pruebas completas del sistema de descarga de velas
- `test_ict_engine.py` - Pruebas del motor principal ICT

### 🚀 **Ejecución de Tests**

#### Ejecutar todos los tests
```bash
python -m pytest tests/
```

#### Ejecutar test específico
```bash
# Test de integración de velas
python tests/test_candle_integration.py

# Test del motor ICT
python tests/test_ict_engine.py
```

#### Desde directorio raíz
```bash
cd "c:\Users\v_jac\Desktop\itc engine v5.0"
python tests/test_candle_integration.py
```

## 📊 **Resultados Esperados**

### ✅ **test_candle_integration.py**
- **Pruebas**: 5 suites completas
- **Resultado**: 5/5 PASARON ✅
- **Componentes**: CandleCoordinator, CandleDownloaderWidget, Integration

### 🎯 **Cobertura de Tests**
- ✅ Importaciones de módulos
- ✅ Funcionalidad básica de coordinador
- ✅ Callbacks del widget
- ✅ Setup de integración
- ✅ Funciones de conveniencia

## 🔧 **Dependencias**

Los tests requieren que estén disponibles:
- Módulos del core ICT Engine
- Sistema de logging (`sistema.logging_interface`)
- Componentes de dashboard
- Utils y configuración

## 📝 **Notas**

- Los tests están diseñados para funcionar **sin MT5 conectado**
- Se usan mocks y stubs para componentes externos
- Los resultados incluyen warnings esperados para componentes opcionales

---

*📅 Última actualización: 4 de Agosto, 2025*
*🏗️ ICT Engine Development Team*
