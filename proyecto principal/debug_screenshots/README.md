# 📸 Debug Screenshots

Este directorio contiene screenshots automáticos tomados durante las sesiones de debugging.

## 🔧 Estructura:
- `dashboard_YYYYMMDD_HHMMSS.png` - Screenshots del dashboard
- `debug_session_YYYYMMDD_HHMMSS.png` - Screenshots de debug sessions
- `manual_YYYYMMDD_HHMMSS.png` - Screenshots manuales

## 🎮 Uso:
1. Ejecutar aplicación con Debug Launcher: `python utilities/debug/debug_launcher.py`
2. Presionar F12 para abrir DevTools
3. Screenshots se toman automáticamente durante el debugging

## 📋 Variables de entorno:
- `TEXTUAL_SCREENSHOT=1` - Habilita screenshots automáticos
- `TEXTUAL_DEVTOOLS=1` - Habilita DevTools F12
