# ============================================================================== 
# 🎯 CONFIGURACIÓN DE CONFIRMACIÓN DE ENTRADA v3.3.3 (NUEVO)
# ============================================================================== 
# Este diccionario controla la nueva estrategia de entrada de precisión,
# que utiliza la confirmación de estructura en una temporalidad baja (LTF).

ENTRY_CONFIRMATION_CONFIG = {
    # Activa (True) o desactiva (False) la necesidad de confirmación por estructura en LTF.
    'USE_LTF_CONFIRMATION': True,

    # Define qué temporalidad usará el "francotirador" para la confirmación final.
    # Opciones recomendadas: 'M1', 'M3', 'M5'
    'LTF_TIMEFRAME': 'M3',

    # Sensibilidad para la detección de puntos de giro en la temporalidad baja (LTF).
    # Un número más bajo (ej. 2) es más reactivo a la acción del precio inmediata.
    'LTF_SWING_SENSITIVITY': 2,

    # Activa (True) o desactiva (False) el bonus de puntuación por confluencia de indicadores.
    'USE_INDICATOR_CONFLUENCE': True,

    # Puntos extra que se añaden al score de un POI si hay una divergencia del estocástico a su favor.
    'INDICATOR_SCORE_BONUS': 15
}
# config.py

# =============================================================================
# SECCIÓN 1: IMPORTACIONES DE LIBRERÍAS
# =============================================================================
import MetaTrader5 as mt5
import pandas as pd
# MIGRADO A SLUC v2.0
from sistema.sic import enviar_senal_log

from sistema.sic import os
from sistema.sic import datetime

# =============================================================================
# SECCIÓN 2: CONFIGURACIÓN GENERAL Y PARÁMETROS INICIALES
# =============================================================================
SIMBOLO = "EURUSD"  # Símbolo principal para trading
ZONA_HORARIA_LOCAL = "America/Guayaquil"
VERBOSE = True

# Función para asegurar que el símbolo esté disponible

# Parámetros de Riesgo y Trading
COMISION_POR_LOTE = 7.0
GANANCIA_MINIMA = 10.0
GANANCIA_MAXIMA = 30.0
RIESGO_MAXIMO_PORCENTAJE = 2.0
LOTE_MINIMO = 0.2
MODO_ACTUAL = "M5"
BOLLINGER_TIMEFRAME = MODO_ACTUAL


LOOKBACK_BARS_GLOBAL = 1000  # Aumentado a 1000 velas para descarga inicial

# =============================================================================
# SECCIÓN 2.5: PARÁMETROS DE ESTRATEGIAS
# =============================================================================
# Parámetros para Grid Bollinger - INCLUYE M1
GRID_BOLLINGER_PARAMS = {
    'DIST_MIN': {'M1': 0.0005, 'M5': 0.0015, 'M15': 0.0012},
    'BANDWIDTH_MIN': {'M1': 0.0003, 'M5': 0.0008, 'M15': 0.0001},
    'SPREAD_MAX': 0.00100  # Aumentado a 10 pips para el backtest
}

# Timeframes soportados por el sistema (INCLUYE M1)
TIMEFRAMES_SOPORTADOS = ['M1', 'M3', 'M5', 'M15', 'H1', 'H4', 'D1']

# Rutas de Archivos Centralizadas
USER_DIR = os.path.expanduser("~")
SAFE_DATA_DIR = os.path.join(USER_DIR, "Documents", "GRID SCALP")
TRADING_LOGS_DIR = os.path.join(SAFE_DATA_DIR, "trading_logs")
# SAFE_DATA_DIR = os.path.join(USER_DIR, "Documents", "GRID SCALP")  # Constant redefinition
ERROR_LOGS_DIR = os.path.join(SAFE_DATA_DIR, "error_logs")
# TRADING_LOGS_DIR = os.path.join(SAFE_DATA_DIR, "trading_logs")  # Constant redefinition
LOG_DEBUG_PATH = os.path.join(SAFE_DATA_DIR, "log_debug.csv")
EVENTOS_SESION_PATH = os.path.join(SAFE_DATA_DIR, "eventos_sesion.csv")

# Asegurar que los directorios existan
os.makedirs(ERROR_LOGS_DIR, exist_ok=True)
os.makedirs(TRADING_LOGS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_DEBUG_PATH), exist_ok=True)

# =============================================================================
# SECCIÓN 3: FUNCIONES DE LOGGING (Básicas)
# =============================================================================
def log_debug(seccion, mensaje, nivel="INFO"):
    """Registra mensajes de depuración en un archivo CSV."""
    try:
        with open(LOG_DEBUG_PATH, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{timestamp},{seccion},{mensaje},{nivel}\n")
            f.flush()
    except (FileNotFoundError, PermissionError, IOError) as e:
        enviar_senal_log("ERROR", f"[CRITICAL ERROR] Fallo en log_debug: {e}", "config", "migration")

def log_event(evento, detalles=""):
    """Registra eventos importantes de la sesión."""
    try:
        os.makedirs(os.path.dirname(EVENTOS_SESION_PATH), exist_ok=True)
        with open(EVENTOS_SESION_PATH, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{timestamp},{evento},{detalles}\n")
            f.flush()
    except (FileNotFoundError, PermissionError, IOError) as e:
        enviar_senal_log("ERROR", f"[ERROR] Fallo al escribir evento en CSV: {e}", "config", "migration")

# =============================================================================
# SECCIÓN 4: FUNCIONES DE INICIALIZACIÓN Y CIERRE DE MT5
# =============================================================================


def obtener_precio_actual(simbolo):
    """Obtiene el precio actual de un símbolo."""
    tick = mt5.symbol_info_tick(simbolo)  # type: ignore
    if tick is None:
        return None
    return (tick.bid + tick.ask) / 2