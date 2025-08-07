# ⚙️ ICT ENGINE v6.0 ENTERPRISE - CONFIGURACIÓN DE DESARROLLO

**🔧 GUÍA COMPLETA DE SETUP Y CONFIGURACIÓN**

---

## 🚀 **SETUP INICIAL DEL ENTORNO**

### 📋 **Prerrequisitos del Sistema**

#### 💻 **Sistema Operativo**
```yaml
Soportado:
  - Windows 10/11 (Recomendado)
  - Windows Server 2019/2022
  
Requerido:
  - FundedNext MT5 Terminal instalado
  - Python 3.11+ (Recomendado 3.13)
  - Visual Studio Code (Recomendado)
  - Git para control de versiones
```

#### 🐍 **Python Requirements**
```yaml
Versión: Python 3.11+
Instalación:
  - Descargar desde python.org
  - Verificar PATH configurado
  - pip actualizado a última versión
  
Verificación:
  python --version  # Debe mostrar 3.11+
  pip --version     # Debe estar actualizado
```

### 📁 **Estructura de Desarrollo**

#### 🗂️ **Directorio Recomendado**
```
C:\Development\
└── ICT-Projects\
    └── ict-engine-v6.0-enterprise-sic\
        ├── sistema/
        ├── utils/
        ├── core/
        ├── dashboard/
        ├── tests/
        ├── docs/
        └── config/
```

### 🔧 **Configuración del Entorno Virtual**

#### 📦 **Crear Ambiente Virtual**
```powershell
# Navegar al directorio del proyecto
cd "C:\Development\ICT-Projects\ict-engine-v6.0-enterprise-sic"

# Crear ambiente virtual
python -m venv venv

# Activar ambiente virtual
.\venv\Scripts\Activate.ps1

# Verificar activación
python -c "import sys; print(sys.prefix)"
```

#### 📋 **Instalar Dependencias**
```powershell
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt

# Verificar instalación
pip list
```

---

## 🛠️ **CONFIGURACIÓN DE VS CODE**

### 📝 **Extensions Requeridas**

#### ✅ **Must-Have Extensions**
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.flake8",
    "ms-python.mypy-type-checker", 
    "ms-python.black-formatter",
    "ms-toolsai.jupyter",
    "ms-python.debugpy",
    "redhat.vscode-yaml",
    "yzhang.markdown-all-in-one",
    "streetsidesoftware.code-spell-checker"
  ]
}
```

#### 🔧 **Settings Óptimas para ICT Engine**
```json
{
  "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
  "python.terminal.activateEnvironment": true,
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": [
    "tests"
  ],
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/venv": true,
    "**/.mypy_cache": true
  },
  "editor.formatOnSave": true,
  "editor.rulers": [88],
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.autoImportCompletions": true,
  "python.analysis.completeFunctionParens": true
}
```

### 🐛 **Configuración de Debug**

#### 🔍 **launch.json para Debugging**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "ICT Engine Debug",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "console": "integratedTerminal",
      "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "ICT_ENGINE_ENV": "development"
      },
      "args": []
    },
    {
      "name": "MT5DataManager Test",
      "type": "python", 
      "request": "launch",
      "program": "${workspaceFolder}/utils/mt5_data_manager.py",
      "console": "integratedTerminal",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    },
    {
      "name": "Run Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
        "tests/",
        "-v",
        "--tb=short"
      ],
      "console": "integratedTerminal",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    }
  ]
}
```

### ⚙️ **Tasks Configuration**

#### 🔧 **tasks.json para Automatización**
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run All Tests",
      "type": "shell",
      "command": "python",
      "args": [
        "-m",
        "pytest",
        "tests/",
        "-v",
        "--tb=short"
      ],
      "group": {
        "kind": "test",
        "isDefault": true
      },
      "presentation": {
        "reveal": "always"
      },
      "problemMatcher": []
    },
    {
      "label": "Test MT5DataManager",
      "type": "shell", 
      "command": "python",
      "args": [
        "-m",
        "pytest",
        "tests/test_mt5_data_manager.py",
        "-v"
      ],
      "group": "test",
      "presentation": {
        "reveal": "always"
      }
    },
    {
      "label": "Format Code with Black",
      "type": "shell",
      "command": "python",
      "args": [
        "-m",
        "black",
        ".",
        "--line-length=88"
      ],
      "group": "build"
    },
    {
      "label": "Lint with Flake8",
      "type": "shell",
      "command": "python", 
      "args": [
        "-m",
        "flake8",
        ".",
        "--config=.flake8"
      ],
      "group": "build"
    },
    {
      "label": "Type Check with MyPy",
      "type": "shell",
      "command": "python",
      "args": [
        "-m",
        "mypy",
        ".",
        "--config-file=mypy.ini"
      ],
      "group": "build"
    }
  ]
}
```

---

## 🔧 **CONFIGURACIÓN DE LINTING Y FORMATTING**

### 📝 **Flake8 Configuration (.flake8)**
```ini
[flake8]
max-line-length = 88
extend-ignore = 
    E203,  # whitespace before ':'
    E501,  # line too long (handled by black)
    W503,  # line break before binary operator
    F401,  # imported but unused (handled by isort)
    E231,  # missing whitespace after ','
exclude = 
    .git,
    __pycache__,
    .pytest_cache,
    .mypy_cache,
    venv,
    .venv,
    build,
    dist
per-file-ignores =
    __init__.py:F401
    tests/*:S101,D103
max-complexity = 10
```

### 🎨 **Black Configuration (pyproject.toml)**
```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.pytest_cache
  | \.tox
  | \.venv
  | venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
```

### 🔍 **MyPy Configuration (mypy.ini)**
```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True
strict_equality = True

[mypy-tests.*]
disallow_untyped_defs = False

[mypy-MetaTrader5]
ignore_missing_imports = True

[mypy-pandas]
ignore_missing_imports = True

[mypy-numpy]
ignore_missing_imports = True
```

---

## 🧪 **CONFIGURACIÓN DE TESTING**

### 📋 **pytest Configuration (pytest.ini)**
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --tb=short
    --strict-markers
    --disable-warnings
    --color=yes
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    performance: marks tests as performance tests
    security: marks tests as security tests
```

### 🔧 **Coverage Configuration (.coveragerc)**
```ini
[run]
source = .
omit = 
    venv/*
    tests/*
    setup.py
    */migrations/*
    */settings/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    if settings.DEBUG
    raise AssertionError
    raise NotImplementedError
    if 0:
    if __name__ == .__main__.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod

[html]
directory = htmlcov
```

---

## 🗂️ **ESTRUCTURA DE ARCHIVOS DE CONFIGURACIÓN**

### 📁 **Archivos Requeridos en Raíz**

#### 📋 **requirements.txt - ACTUALIZADO**
```txt
# Core dependencies
MetaTrader5>=5.0.45
pandas>=2.0.0
numpy>=1.24.0
python-dateutil>=2.8.2

# Development tools
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.7.0
flake8>=6.0.0
mypy>=1.5.0
isort>=5.12.0

# Utilities
colorlog>=6.7.0
rich>=13.5.0
psutil>=5.9.0
requests>=2.31.0

# Optional but recommended
jupyter>=1.0.0
matplotlib>=3.7.0  # Solo para testing/análisis
plotly>=5.15.0     # Para gráficos avanzados
```

#### ⚙️ **setup.cfg - Configuración Global**
```ini
[metadata]
name = ict-engine-v6-enterprise-sic
version = 6.0.0
description = Sistema ICT Enterprise v6.0 con SIC v3.1
long_description = file: README.md
long_description_content_type = text/markdown
author = ICT Engine v6.0 Enterprise Team
author_email = dev@ictengine.com
url = https://github.com/ictengine/v6-enterprise
classifiers =
    Development Status :: 4 - Beta
    Intended Audience :: Financial and Insurance Industry
    Topic :: Office/Business :: Financial :: Investment
    License :: Proprietary
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.11
    Programming Language :: Python :: 3.12

[options]
packages = find:
python_requires = >=3.11
install_requires =
    MetaTrader5>=5.0.45
    pandas>=2.0.0
    numpy>=1.24.0

[options.packages.find]
exclude =
    tests*
    docs*
```

### 🔧 **Variables de Entorno (.env)**
```bash
# ICT Engine v6.0 Enterprise Configuration
ICT_ENGINE_VERSION=6.0.0-enterprise
ICT_ENGINE_ENV=development

# MT5 Configuration
FUNDEDNEXT_MT5_PATH=C:\Program Files\FundedNext MT5 Terminal\terminal64.exe
MT5_MAGIC_NUMBER=20250807
MT5_MAX_BARS=50000

# SIC v3.1 Configuration
SIC_VERSION=3.1
SIC_DEBUG_LEVEL=info
SIC_CACHE_ENABLED=true
SIC_LAZY_LOADING=true

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=detailed
LOG_TO_FILE=true
LOG_DIR=logs

# Performance Configuration
CACHE_SIZE_MB=256
MAX_THREADS=4
PERFORMANCE_MONITORING=true

# Security Configuration
SECURITY_LEVEL=MAXIMUM
AUDIT_LOGGING=true
CONNECTION_VALIDATION=strict
```

---

## 🚀 **SCRIPTS DE AUTOMATIZACIÓN**

### 🔧 **setup_dev.py - Script de Setup Automático**
```python
#!/usr/bin/env python3
"""
🔧 SETUP AUTOMÁTICO DEL ENTORNO DE DESARROLLO
=============================================

Script para configurar automáticamente el entorno de desarrollo
completo para ICT Engine v6.0 Enterprise.

Autor: ICT Engine v6.0 Enterprise Team
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command: str, description: str) -> bool:
    """Ejecutar comando con logging"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description}: Completado")
            return True
        else:
            print(f"❌ {description}: Error - {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description}: Excepción - {e}")
        return False

def setup_environment():
    """Setup completo del entorno"""
    print("🚀 ICT ENGINE v6.0 ENTERPRISE - SETUP DE DESARROLLO")
    print("=" * 60)
    
    # Verificar Python
    if not run_command("python --version", "Verificando Python"):
        print("❌ Python no encontrado. Instalar Python 3.11+")
        return False
    
    # Crear ambiente virtual si no existe
    if not Path("venv").exists():
        run_command("python -m venv venv", "Creando ambiente virtual")
    
    # Activar ambiente virtual
    if platform.system() == "Windows":
        activate_cmd = ".\\venv\\Scripts\\Activate.ps1"
        pip_cmd = ".\\venv\\Scripts\\pip"
        python_cmd = ".\\venv\\Scripts\\python"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "./venv/bin/pip"
        python_cmd = "./venv/bin/python"
    
    # Actualizar pip
    run_command(f"{pip_cmd} install --upgrade pip", "Actualizando pip")
    
    # Instalar dependencias
    run_command(f"{pip_cmd} install -r requirements.txt", "Instalando dependencias")
    
    # Configurar pre-commit hooks si existen
    if Path(".pre-commit-config.yaml").exists():
        run_command(f"{pip_cmd} install pre-commit", "Instalando pre-commit")
        run_command("pre-commit install", "Configurando pre-commit hooks")
    
    # Ejecutar tests para verificar setup
    run_command(f"{python_cmd} -m pytest tests/ -v", "Ejecutando tests de verificación")
    
    print("\n🎉 SETUP COMPLETADO")
    print("🔧 Ambiente de desarrollo listo para ICT Engine v6.0")
    print("\n📋 PRÓXIMOS PASOS:")
    print("   1. Activar ambiente virtual:")
    if platform.system() == "Windows":
        print("      .\\venv\\Scripts\\Activate.ps1")
    else:
        print("      source venv/bin/activate")
    print("   2. Abrir VS Code: code .")
    print("   3. Ejecutar tests: python -m pytest tests/ -v")

if __name__ == "__main__":
    setup_environment()
```

### 🧪 **run_tests.py - Script de Testing Completo**
```python
#!/usr/bin/env python3
"""
🧪 RUNNER DE TESTS COMPLETO ICT ENGINE v6.0
==========================================

Script para ejecutar toda la suite de tests con reportes detallados.

Autor: ICT Engine v6.0 Enterprise Team
"""

import sys
import subprocess
import time
from pathlib import Path

def run_test_suite():
    """Ejecutar suite completa de tests"""
    print("🧪 ICT ENGINE v6.0 ENTERPRISE - TEST SUITE")
    print("=" * 60)
    
    start_time = time.time()
    
    # Tests por módulo
    test_modules = [
        ("test_mt5_data_manager.py", "MT5DataManager - FUNDAMENTAL #1"),
        ("test_sic_complete.py", "SIC v3.1 Enterprise"),
        ("test_advanced_candle_downloader.py", "Advanced Candle Downloader")
    ]
    
    results = {}
    
    for test_file, description in test_modules:
        print(f"\n🎯 Ejecutando: {description}")
        print("-" * 40)
        
        cmd = f"python -m pytest tests/{test_file} -v --tb=short"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        results[test_file] = {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr,
            'description': description
        }
        
        if result.returncode == 0:
            print(f"✅ {description}: PASSED")
        else:
            print(f"❌ {description}: FAILED")
            print(result.stderr)
    
    # Resumen final
    duration = time.time() - start_time
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS ICT ENGINE v6.0")
    print("=" * 60)
    
    passed = sum(1 for r in results.values() if r['success'])
    total = len(results)
    
    print(f"⏱️  Duración total: {duration:.2f} segundos")
    print(f"✅ Tests pasados: {passed}/{total}")
    print(f"❌ Tests fallidos: {total-passed}/{total}")
    
    if passed == total:
        print("\n🏆 TODOS LOS TESTS PASARON - SISTEMA ESTABLE ✅")
        print("🚀 ICT Engine v6.0 Enterprise listo para desarrollo")
    else:
        print("\n⚠️  ALGUNOS TESTS FALLARON - REVISAR ANTES DE CONTINUAR")
        print("🔧 Verificar configuración y dependencias")
    
    return passed == total

if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1)
```

---

## 📋 **CHECKLIST DE VERIFICACIÓN**

### ✅ **Setup Completo Verificado**

#### 🔧 **Entorno Base**
```yaml
- [ ] Python 3.11+ instalado y configurado
- [ ] FundedNext MT5 Terminal instalado
- [ ] VS Code con extensions requeridas
- [ ] Git configurado para control de versiones
- [ ] Ambiente virtual creado y activado
- [ ] Dependencias instaladas correctamente
```

#### 📝 **Configuraciones**
```yaml
- [ ] .vscode/settings.json configurado
- [ ] .vscode/launch.json para debugging
- [ ] .vscode/tasks.json para automatización
- [ ] Linting (flake8, mypy) funcionando
- [ ] Formatting (black) configurado
- [ ] Testing (pytest) ejecutándose
```

#### 🧪 **Validación**
```yaml
- [ ] Tests de MT5DataManager pasando (20/20)
- [ ] Tests de SIC v3.1 funcionando
- [ ] Performance < 100ms en operaciones críticas
- [ ] Debugging en VS Code funcional
- [ ] Linting sin errores críticos
- [ ] Code formatting automático
```

### 🚀 **Ready for Development**

Cuando todos los items están ✅, el entorno está listo para:

1. 📊 **Desarrollo de Market Structure Analyzer**
2. 🎯 **Implementación de Pattern Detector**
3. 🏢 **Creación de Order Block Engine**
4. 🎯 **Sistema POI completo**

---

**🏆 ICT Engine v6.0 Enterprise - Development Setup**

*"Un entorno de desarrollo enterprise configurado correctamente es la base del éxito. Cada herramienta, cada configuración, cada script - todo optimizado para máxima productividad y calidad."*

---

**📅 Última Actualización**: Agosto 7, 2025  
**📝 Versión Setup**: v1.0  
**🔧 Maintainer**: ICT Engine v6.0 Enterprise Team
