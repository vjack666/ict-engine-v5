# 🎯 ICT ENGINE v5.0 - Sistema de Trading Profesional

Sistema avanzado de análisis y trading basado en patrones ICT (Inner Circle Trader) con dashboard interactivo y gestión automatizada de posiciones.

## 🚀 Características Principales

- **🎯 Análisis ICT Completo**: Detección automática de patrones Silver Bullet, Judas Swing, Order Blocks, etc.
- **📊 Dashboard Interactivo**: Interface profesional con Textual UI para monitoreo en tiempo real
- **💹 Trading Automatizado**: Ejecución automática de señales con gestión avanzada de riesgo
- **🌙 Sistema de Hibernación**: Operación inteligente según horarios de mercado
- **📱 Notificaciones**: Alertas por Telegram, email y push notifications
- **🔧 Debug Tools**: Herramientas profesionales de debugging y desarrollo

## 📁 Estructura del Proyecto

```
ICT Engine v5.0/
├── 🚀 main.py                     # Launcher principal
├── 📋 requirements.txt            # Dependencias
├── 🧪 pytest.ini                 # Configuración de tests
├── 🚫 .gitignore                 # Archivos excluidos
├──
├── 📊 dashboard/                  # Dashboard principal
│   ├── dashboard_definitivo.py   # App principal
│   ├── dashboard_widgets.py      # Widgets modulares
│   └── dashboard_controller.py   # Controlador central
├──
├── 🧠 core/                       # Lógica principal
│   ├── ict_engine/               # Motor ICT
│   ├── poi_system/               # Sistema POI
│   ├── risk_management/          # Gestión de riesgo
│   └── trading.py                # Motor de trading
├──
├── ⚙️ sistema/                    # Sistema base
│   ├── logging_interface.py     # SLUC v2.0 Logging
│   └── emoji_logger.py          # Logger con emojis
├──
├── 📁 config/                     # Configuraciones
│   ├── config_manager.py        # Gestor de config
│   ├── config_main.json         # Config principal
│   └── config_user.json         # Config usuario
├──
├── 🛠️ utilities/                  # Herramientas
│   ├── debug/                    # Debug tools
│   ├── migration/                # Migración de código
│   └── sprint/                   # Gestión de sprints
├──
├── 🧪 tests/                      # Suite de tests
│   ├── unit/                     # Tests unitarios
│   ├── integration/              # Tests integración
│   └── fixtures/                 # Datos de prueba
├──
├── 📋 scripts/                    # Scripts utilidad
│   └── system_info.py           # Info del sistema
├──
├── 📚 docs/                       # Documentación
│   ├── README.md                 # Documentación general
│   └── architecture/             # Arquitectura
├──
├── 💾 data/                       # Datos del sistema
│   └── logs/                     # Logs estructurados
├──
└── 🗂️ temp/                       # Archivos temporales
```

## 🔧 Instalación y Configuración

### 1. **Clonar el Repositorio**
```bash
git clone [repository-url]
cd "itc engine v5.0"
```

### 2. **Instalar Dependencias**
```bash
# Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 3. **Configurar VS Code (Opcional)**
```bash
# Usar configuración menos estricta
# Ver: CONFIGURACION_VSCODE_MENOS_ESTRICTO.md
```

## 🚀 Uso del Sistema

### **Launcher Principal**
```bash
# 🎯 Menú interactivo
python main.py

# 🚀 Dashboard directo
python main.py --dashboard

# 🔧 Herramientas de debug
python main.py --debug

# 🛠️ Ver utilidades
python main.py --utilities

# 🧪 Ejecutar tests
python main.py --tests
```

### **Componentes Individuales**
```bash
# 📊 Dashboard principal
python dashboard/dashboard_definitivo.py

# 🔧 Debug tools
python utilities/debug/debug_launcher.py

# 📝 Migración de prints
python utilities/migration/print_migration_tool.py --scan-only

# 📊 Consolidador de sprint
python utilities/sprint/sprint_1_1_consolidator.py
```

## 🧪 Testing

### **Ejecutar Tests**
```bash
# 🧪 Todos los tests
python -m pytest tests/

# 📊 Tests con cobertura
python -m pytest tests/ --cov=core --cov=dashboard

# 🚀 Tests específicos
python -m pytest tests/unit/test_config_manager.py

# 🏷️ Tests por marker
python -m pytest -m "unit" tests/
python -m pytest -m "integration" tests/
```

### **Crear Nuevos Tests**
```bash
# 📁 Tests unitarios
tests/unit/test_nuevo_componente.py

# 🔗 Tests de integración
tests/integration/test_dashboard_integration.py
```

## 🛠️ Herramientas de Desarrollo

### **Debug Tools**
```bash
# 🔧 Debug Launcher con F12
python utilities/debug/debug_launcher.py

# 📸 Screenshots de debug
# Presiona 'S' en debug launcher

# 📋 DevTools F12
# Presiona F12 en debug launcher
```

### **Code Quality**
```bash
# 📝 Migración de prints
python utilities/migration/print_migration_tool.py --dry-run

# 🧹 Linting
pylint core/
pylint dashboard/

# 🎨 Formateo
black core/ dashboard/ sistema/
```

### **Sprint Management**
```bash
# 📊 Estado del sprint actual
python utilities/sprint/sprint_1_1_consolidator.py

# 📋 Validación completa
python utilities/sprint/sprint_1_1_consolidator.py --validation-only

# 🧪 Tests de integración
python utilities/sprint/sprint_1_1_consolidator.py --integration-only
```

## 📊 Roadmap de Desarrollo

### **🟢 Sprint 1.1: Debug System & Clean Code** *(COMPLETADO)*
- ✅ Debug Launcher con DevTools F12
- ✅ Migración de print statements a enviar_senal_log()
- ✅ Console mode para desarrollo
- ✅ Screenshot capability
- ✅ Testing de rendering limpio

### **🟡 Sprint 1.2: Trading Engine Foundation** *(EN PROGRESO)*
- 🔄 Trading engine con ejecución automática
- 🔄 Grid Trading básico
- 🔄 Position Manager para múltiples posiciones
- 🔄 Trailing stop avanzado

### **🟡 Sprint 2.1: Hibernación Inteligente** *(PLANIFICADO)*
- 🌙 Sistema de hibernación automática
- ⏰ Gestión de horarios de trading
- 🔄 Transiciones automáticas entre fases
- 📊 Monitoreo de recursos

### **🟡 Sprint 3.1: Trading Profesional** *(PLANIFICADO)*
- 💹 Ejecución automática de señales
- 📈 Analytics y performance
- 🎯 Risk management avanzado
- 📊 Portfolio management

## 📚 Documentación

- **📋 [Plan Completo](PLAN_TRABAJO_COMPLETO_ICT.md)**: Roadmap detallado del proyecto
- **🔧 [Config VS Code](BITACORA_CONFIGURACION_VSCODE.md)**: Configuración de desarrollo
- **📊 [Diagnóstico](BITACORA_DIAGNOSTICO_DASHBOARD.md)**: Diagnóstico del dashboard
- **📈 [Seguimiento](BITACORA_SEGUIMIENTO_ICT.md)**: Tracking del progreso
- **🛠️ [VS Code Simple](CONFIGURACION_VSCODE_MENOS_ESTRICTO.md)**: Config simplificada

## 🤝 Contribución

1. **Fork** el proyecto
2. **Crear** branch para feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** al branch (`git push origin feature/nueva-funcionalidad`)
5. **Crear** Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Contacto y Soporte

- **📧 Email**: [email del desarrollador]
- **💬 Discord**: [servidor de Discord]
- **📱 Telegram**: [canal de Telegram]

---

*🎯 ICT Engine v5.0 - Sistema de Trading Profesional*
*Última actualización: Agosto 2025*
