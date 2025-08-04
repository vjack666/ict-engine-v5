# 🤖 ICT ENGINE v5.0 - MODOS AUTOMÁTICOS

## 🚀 Opciones de Inicio Automático

El sistema ICT Engine v5.0 ahora incluye múltiples formas de inicio automático para diferentes necesidades:

### 1. 🎯 **Dashboard Directo** (Recomendado para uso rápido)
```bash
python dashboard_directo.py
```
- ✅ Inicio más rápido
- ✅ Va directo al dashboard
- ✅ Sin auto-descarga (usa datos existentes)
- ✅ Ideal para trading diario

### 2. 🤖 **Auto Start Completo**
```bash
python auto_start.py
```
- ✅ Auto-descarga de datos REALES
- ✅ Validación completa del sistema
- ✅ Configuración automática
- ✅ Ideal para primer uso del día

### 3. 📋 **Main Automático** (Modificado)
```bash
python main.py
```
- ✅ Ahora va directo al dashboard
- ✅ Sin menús interactivos
- ✅ Mantiene compatibilidad con parámetros
- ✅ `python main.py --utilities` para herramientas

### 4. 🖱️ **Archivo Batch para Windows**
```
Doble clic en: START_ICT_ENGINE.bat
```
- ✅ Inicio con un clic
- ✅ No requiere terminal
- ✅ Manejo automático de errores

### 5. 💻 **PowerShell Script**
```powershell
.\START_ICT_ENGINE.ps1
```
- ✅ Script nativo de Windows
- ✅ Mejor manejo de errores
- ✅ Output colorizado

## 🔧 Parámetros Disponibles

### Auto Start:
```bash
python auto_start.py --debug      # Modo debug
python auto_start.py --verbose    # Output detallado
```

### Main (modificado):
```bash
python main.py --dashboard        # Dashboard (por defecto ahora)
python main.py --debug           # Debug tools
python main.py --utilities       # Menú de utilidades
python main.py --tests           # Ejecutar tests
```

## 📊 Confirmación de Datos REALES

Todos los modos automáticos incluyen confirmación clara de que se usan datos REALES:

```
📊 CONFIRMACIÓN: TODOS los datos de mercado son REALES desde MT5
🔍 El sistema NUNCA simula precios - Solo obtiene datos directos del broker
```

## 🎯 Recomendaciones de Uso

### Para Trading Diario:
```bash
python dashboard_directo.py
```

### Para Primera Sesión del Día:
```bash
python auto_start.py
```

### Para Desarrollo/Debug:
```bash
python main.py --debug
```

### Para Windows (Inicio Rápido):
```
Doble clic en START_ICT_ENGINE.bat
```

## ⚡ Inicio Ultra-Rápido

Crea un acceso directo en tu escritorio que ejecute:
```
"C:\Users\v_jac\Desktop\itc engine v5.0\START_ICT_ENGINE.bat"
```

¡Un solo clic para iniciar todo el sistema ICT Engine!
