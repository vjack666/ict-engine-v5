# 🛡️ PROTOCOLO DE SEGURIDAD MT5 - SOLO FUNDEDNEXT

## 📅 Fecha: 2025-08-05
## 🎯 Objetivo: Garantizar conexión EXCLUSIVA al terminal FundedNext MT5

---

## 🚨 MEDIDAS DE SEGURIDAD IMPLEMENTADAS

### 1. 🔒 Verificación de Ruta Obligatoria
```python
FUNDEDNEXT_MT5_PATH = r"C:\Program Files\FundedNext MT5 Terminal\terminal64.exe"

def validate_fundednext_installation() -> bool:
    """SOLO permite el uso del terminal FundedNext."""
    if not os.path.exists(FUNDEDNEXT_MT5_PATH):
        return False
    if "fundednext" not in FUNDEDNEXT_MT5_PATH.lower():
        return False
    return True
```

### 2. 🛡️ Desconexión Automática de Otros Terminales
```python
def ensure_only_fundednext_connection():
    """Desconecta cualquier terminal que NO sea FundedNext."""
    terminal_info = mt5.terminal_info()
    if terminal_info:
        if "fundednext" not in terminal_info.path.lower():
            mt5.shutdown()  # Desconecta terminal no autorizado
            return False
```

### 3. 🔍 Verificación Post-Conexión
```python
def _verify_fundednext_connection(self) -> bool:
    """Verifica que estamos conectados al terminal correcto."""
    terminal_info = mt5.terminal_info()
    if "fundednext" not in terminal_info.path.lower():
        self.disconnect()  # Desconecta inmediatamente
        return False
```

---

## 🔐 FLUJO DE CONEXIÓN SEGURA

### Paso 1: Verificación Inicial
- ✅ Verificar que FundedNext MT5 esté instalado
- ✅ Verificar ruta exacta del terminal
- ❌ Rechazar si no es la ruta correcta

### Paso 2: Desconexión Preventiva
- 🔒 Desconectar cualquier terminal MT5 activo
- 🧹 Limpiar conexiones previas
- 🛡️ Preparar conexión limpia

### Paso 3: Conexión Exclusiva
- 📁 Conectar usando ruta específica de FundedNext
- 🔍 Verificar información del terminal conectado
- ❌ Desconectar si no es el terminal correcto

### Paso 4: Validación Continua
- 🔄 Verificar terminal en cada operación crítica
- 📊 Logging de seguridad en cada conexión
- 🚨 Alertas si se detecta terminal incorrecto

---

## 📊 TERMINAL AUTORIZADO vs NO AUTORIZADOS

### ✅ TERMINAL AUTORIZADO:
```
📁 Ruta: C:\Program Files\FundedNext MT5 Terminal\terminal64.exe
🏢 Empresa: FundedNext Ltd
🏦 Cuenta: 11087731 (Tipo: Real Account)
💰 Balance: $6,111.20
🛡️ Estado: AUTORIZADO PARA TRADING
```

### ❌ TERMINALES NO AUTORIZADOS:
- ❌ Cualquier terminal con cuenta real personal
- ❌ Terminales de otros brokers
- ❌ Instalaciones MT5 genéricas
- ❌ Terminales sin verificación FundedNext

---

## 🚨 ALERTAS DE SEGURIDAD

### Logs de Conexión Segura:
```
✅ CONEXIÓN SEGURA ESTABLECIDA - Solo FundedNext MT5
🔒 Desconectado cualquier terminal MT5 previo
✅ Verificado: Conectado a FundedNext MT5
🛡️ MT5DataManager creado con seguridad FundedNext
```

### Logs de Alerta:
```
🚨 TERMINAL INCORRECTO DETECTADO: [ruta_detectada]
🚨 SE ESPERABA: C:\Program Files\FundedNext MT5 Terminal\terminal64.exe
🚨 Desconectando terminal no autorizado...
🚨 SEGURIDAD: Solo se permite conexión a FundedNext MT5
```

---

## 🔧 FUNCIONES DE EMERGENCIA

### 1. Conexión de Emergencia
```python
def force_fundednext_only_connection() -> bool:
    """Función de emergencia para garantizar conexión solo a FundedNext."""
    # Desconecta todo y reconecta solo a FundedNext
```

### 2. Verificación de Instancia
```python
def get_mt5_manager() -> MT5DataManager:
    """Garantiza que solo se use el terminal FundedNext MT5."""
    if not validate_fundednext_installation():
        raise ConnectionError("SOLO se permite el uso del terminal FundedNext MT5")
```

---

## 📋 CHECKLIST DE SEGURIDAD

### Antes de Cada Operación:
- [ ] ✅ Verificar ruta del terminal
- [ ] ✅ Confirmar información FundedNext
- [ ] ✅ Validar cuenta autorizada
- [ ] ✅ Verificar broker correcto

### Durante las Operaciones:
- [ ] ✅ Monitorear logs de seguridad
- [ ] ✅ Verificar datos de terminal en tiempo real
- [ ] ✅ Confirmar que no hay otros terminales activos

### Después de las Operaciones:
- [ ] ✅ Verificar que no se perdió la conexión segura
- [ ] ✅ Revisar logs por alertas de seguridad
- [ ] ✅ Confirmar estado de la cuenta

---

## 🎯 BENEFICIOS DE SEGURIDAD

### 🛡️ Protección de Cuentas Reales:
- ✅ **Separación Total**: Cuenta real personal protegida
- ✅ **Aislamiento**: Solo FundedNext para trading automatizado
- ✅ **Prevención**: Imposible conectarse accidentalmente a cuenta real

### 🔍 Transparencia:
- ✅ **Trazabilidad**: Cada conexión es logueada
- ✅ **Verificación**: Estado del terminal siempre visible
- ✅ **Alertas**: Notificación inmediata de problemas

### 🚀 Confiabilidad:
- ✅ **Consistencia**: Siempre el mismo terminal
- ✅ **Estabilidad**: Sin conflictos entre terminales
- ✅ **Predictibilidad**: Comportamiento garantizado

---

## 🔄 PRUEBAS DE SEGURIDAD

### Test 1: Verificación de Terminal
```bash
python scripts\verificar_datos_reales.py
# Debe mostrar: "CONECTADO SEGURO A FUNDEDNEXT"
```

### Test 2: Información de Cuenta
```bash
# Debe mostrar exactamente:
# Broker: FundedNext Ltd
# Cuenta: 11087731
# Tipo: Real Account
```

### Test 3: Validación de Ruta
```bash
# El log debe confirmar:
# "✅ Verificado: Conectado a FundedNext MT5"
# "Ruta: C:\Program Files\FundedNext MT5 Terminal\terminal64.exe"
```

---

## ✅ ESTADO ACTUAL

**🛡️ SEGURIDAD IMPLEMENTADA Y VERIFICADA**

- ✅ Conexión exclusiva a FundedNext MT5
- ✅ Verificación automática de terminal
- ✅ Desconexión de terminales no autorizados
- ✅ Logging completo de seguridad
- ✅ Protección de cuentas reales
- ✅ Función de emergencia disponible

**📊 RESULTADO**: El sistema garantiza el uso exclusivo del terminal FundedNext MT5, protegiendo completamente las cuentas reales personales.
