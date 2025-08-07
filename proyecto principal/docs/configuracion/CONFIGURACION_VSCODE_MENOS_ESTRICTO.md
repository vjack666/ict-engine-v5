# 🛠️ CONFIGURACIÓN VS CODE MENOS ESTRICTO - PROMPT PARA COPILOT

## 📋 **PROMPT PARA USAR EN CUALQUIER PROYECTO:**

```
Necesito configurar Visual Studio Code para que sea menos estricto con errores de Python y solo muestre errores críticos que realmente afecten la funcionalidad. Por favor:

1. Crea un archivo `.pylintrc` en la raíz del proyecto con configuración menos estricta
2. Crea/actualiza `.vscode/settings.json` con configuraciones optimizadas para Python
3. Configura para mostrar solo errores importantes y ocultar warnings menores

Quiero ver únicamente:
- Errores críticos que impidan ejecución
- Errores de sintaxis
- Imports faltantes o incorrectos
- Variables no definidas
- Problemas críticos de lógica

NO quiero ver:
- Líneas demasiado largas
- Documentación faltante
- Nombres de variables en snake_case
- Argumentos no utilizados
- Acceso a miembros protegidos
- Comentarios TODO/FIXME
- Warnings sobre complejidad de código
- Trailing whitespace
- Imports no utilizados (solo como info, no error)

Proporciona los archivos de configuración completos listos para usar.
```

## 🔧 **ARCHIVOS DE CONFIGURACIÓN GENERADOS:**

### **Archivo 1: `.pylintrc`** (Raíz del proyecto)

```ini
[MASTER]
# Python code to execute, usually for sys.path manipulation such as
# pygtk.require().
init-hook='import sys; sys.path.append(".")'

[MESSAGES CONTROL]
# Disable specific pylint warnings that are too strict for development
disable=
    C0103,  # Invalid name (snake_case, etc.)
    C0114,  # Missing module docstring
    C0115,  # Missing class docstring
    C0116,  # Missing function docstring
    C0301,  # Line too long
    C0303,  # Trailing whitespace
    R0903,  # Too few public methods
    R0913,  # Too many arguments
    R0914,  # Too many local variables
    R0915,  # Too many statements
    W0613,  # Unused argument
    W0622,  # Redefining built-in
    W0718,  # Catching too general exception
    W0719,  # Raising too general exception
    W0212,  # Access to protected member
    W0511,  # TODO/FIXME comments
    R0801,  # Similar lines in files
    R0902,  # Too many instance attributes
    R0912,  # Too many branches
    C0302,  # Too many lines in module
    W0102,  # Dangerous default value
    W0107,  # Unnecessary pass statement

# Only show errors and critical warnings
confidence=HIGH

[FORMAT]
# Maximum number of characters on a single line
max-line-length=120

[DESIGN]
# Maximum number of arguments for function / method
max-args=10

# Maximum number of locals for function / method body
max-locals=20

# Maximum number of return / yield for function / method body
max-returns=8

# Maximum number of branch for function / method body
max-branches=15

# Maximum number of statements in function / method body
max-statements=60

# Maximum number of parents for a class (see R0901).
max-parents=7

# Maximum number of attributes for a class (see R0902).
max-attributes=15

# Minimum number of public methods for a class (see R0903).
min-public-methods=1

# Maximum number of public methods for a class (see R0904).
max-public-methods=25

[BASIC]
# Good variable names which should always be accepted, separated by a comma
good-names=i,j,k,ex,Run,_,df,tf,logger,e,f
```

### **Archivo 2: `.vscode/settings.json`**

```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--disable=C0103,C0114,C0115,C0116,C0301,C0303,R0903,R0913,R0914,R0915,W0613,W0622,W0718,W0719,W0212,W0511,R0801,R0902,R0912,C0302,W0102,W0107",
        "--max-line-length=120",
        "--confidence=HIGH"
    ],

    "problems.defaultViewMode": "tree",
    "problems.showCurrentInStatus": true,
    "problems.decorations.enabled": true,

    "python.analysis.diagnosticMode": "workspace",
    "python.analysis.diagnosticSeverityOverrides": {
        "reportMissingImports": "error",
        "reportMissingTypeStubs": "none",
        "reportImportCycles": "error",
        "reportUnusedImport": "information",
        "reportUnusedClass": "information",
        "reportUnusedFunction": "information",
        "reportUnusedVariable": "information",
        "reportDuplicateImport": "warning",
        "reportOptionalSubscript": "none",
        "reportOptionalMemberAccess": "none",
        "reportOptionalCall": "none",
        "reportOptionalIterable": "none",
        "reportOptionalContextManager": "none",
        "reportOptionalOperand": "none",
        "reportTypedDictNotRequiredAccess": "none",
        "reportPrivateImportUsage": "none",
        "reportConstantRedefinition": "warning",
        "reportIncompatibleMethodOverride": "error",
        "reportIncompatibleVariableOverride": "error",
        "reportInconsistentConstructor": "none",
        "reportOverlappingOverloads": "warning",
        "reportMissingSuperCall": "none",
        "reportUninitializedInstanceVariable": "none",
        "reportInvalidStringEscapeSequence": "error",
        "reportUnknownParameterType": "none",
        "reportUnknownArgumentType": "none",
        "reportUnknownLambdaType": "none",
        "reportUnknownVariableType": "none",
        "reportUnknownMemberType": "none",
        "reportMissingParameterType": "none",
        "reportMissingTypeArgument": "none",
        "reportInvalidTypeVarUse": "warning",
        "reportCallInDefaultInitializer": "none",
        "reportUnnecessaryIsInstance": "none",
        "reportUnnecessaryCast": "none",
        "reportUnnecessaryComparison": "none",
        "reportUnnecessaryContains": "none",
        "reportAssertAlwaysTrue": "warning",
        "reportSelfClsParameterName": "warning",
        "reportImplicitStringConcatenation": "none",
        "reportUndefinedVariable": "error",
        "reportUnboundVariable": "error",
        "reportInvalidStubStatement": "none",
        "reportIncompleteStub": "none",
        "reportUnsupportedDunderAll": "warning",
        "reportUnusedCallResult": "none",
        "reportUnusedCoroutine": "error",
        "reportUnusedExpression": "warning",
        "reportUnnecessaryTypeIgnoreComment": "none",
        "reportMatchNotExhaustive": "none"
    },

    "python.analysis.autoImportCompletions": true,
    "python.analysis.completeFunctionParens": true,
    "python.analysis.autoSearchPaths": true,
    "python.analysis.extraPaths": [],
    "python.analysis.stubPath": "",
    "python.analysis.typeshedPaths": [],
    "python.analysis.useLibraryCodeForTypes": true,

    "editor.rulers": [120],
    "editor.wordWrap": "on",
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
    "files.trimFinalNewlines": true,

    "terminal.integrated.defaultProfile.windows": "PowerShell",

    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": false,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        },
        "editor.rulers": [120],
        "editor.tabSize": 4,
        "editor.insertSpaces": true
    }
}
```

## 🎯 **INSTRUCCIONES DE USO:**

### **Paso 1: Crear archivos**
1. Copia el contenido de `.pylintrc` y créalo en la raíz de tu proyecto
2. Crea la carpeta `.vscode` si no existe
3. Copia el contenido de `settings.json` en `.vscode/settings.json`

### **Paso 2: Aplicar configuración**
1. Reinicia VS Code completamente
2. Abre el Panel de Problemas (`Ctrl+Shift+M`)
3. Haz clic en el filtro (🔍) y selecciona solo "Errors" si quieres ser más específico

### **Paso 3: Verificar funcionamiento**
```bash
# Comando para verificar que funciona (en terminal de VS Code)
python -m pylint archivo.py --errors-only
```

## ✅ **RESULTADO ESPERADO:**

- **Solo errores críticos** que impidan la ejecución
- **Calificación Pylint alta** (>9.5/10 típicamente)
- **Panel de problemas limpio** sin warnings menores
- **Experiencia de desarrollo mejorada** sin distracciones

## 🌍 **COMPATIBILIDAD UNIVERSAL:**

Esta configuración es **100% genérica** y funciona en cualquier proyecto Python:

### ✅ **Tipos de proyectos compatibles:**
- 🌐 **Web Applications** (Django, Flask, FastAPI)
- 📊 **Data Science** (Jupyter, Pandas, NumPy)
- 🤖 **Machine Learning** (TensorFlow, PyTorch, Scikit-learn)
- 📱 **Desktop Apps** (Tkinter, PyQt, Kivy)
- 🔧 **Automation Scripts** (Selenium, BeautifulSoup)
- 💹 **Trading Bots** (como tu ICT Engine)
- 🐳 **Microservices** (Docker, Kubernetes)
- 📈 **Analytics** (Matplotlib, Seaborn)
- 🎮 **Game Development** (Pygame, Arcade)
- ⚡ **CLI Tools** (Click, Argparse)

### 🎯 **Por qué es universal:**
- ❌ **Sin dependencias específicas** - Solo configura linting
- ❌ **Sin rutas hardcodeadas** - Usa rutas relativas
- ❌ **Sin imports específicos** - Reglas generales de Python
- ✅ **Funciona desde el primer día** en cualquier proyecto

## 🚀 **COMANDO RÁPIDO PARA COPILOT:**

```
Configura VS Code para Python menos estricto: crea .pylintrc y .vscode/settings.json que solo muestren errores críticos, sin warnings de líneas largas, documentación faltante, argumentos no usados, etc. Quiero código funcional sin micro-management de estilo.
```

## 🧪 **EJEMPLOS DE USO EN DIFERENTES PROYECTOS:**

### **Proyecto Django:**
```bash
# En tu proyecto Django
cd mi_proyecto_django/
# Pega el prompt a Copilot → Archivos creados
# Reinicia VS Code → ¡Listo!
```

### **Proyecto Data Science:**
```bash
# En tu proyecto de ML
cd analisis_datos/
# Pega el prompt a Copilot → Archivos creados
# Reinicia VS Code → ¡Listo!
```

### **Script simple:**
```bash
# Cualquier carpeta con Python
cd mis_scripts/
# Pega el prompt a Copilot → Archivos creados
# Reinicia VS Code → ¡Listo!
```

**Resultado:** El mismo comportamiento limpio en todos los casos.

---
**Nota:** Esta configuración prioriza funcionalidad sobre estilo, ideal para desarrollo rápido y prototipado.
