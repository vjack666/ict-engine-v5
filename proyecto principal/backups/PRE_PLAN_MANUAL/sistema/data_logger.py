# =============================================================================
# SISTEMA DE DATA LOGGER LIMPIO Y MODERNO
# MIGRADO COMPLETAMENTE A SLUC v2.1
# =============================================================================

from sistema.sic import os
from sistema.sic import sys
import csv
import pandas as pd
import traceback
from sistema.sic import Path
from sistema.sic import datetime
from sistema.sic import List, Optional, Dict, Any
import pytz

# SLUC v2.1 - Sistema de Logging Unificado y Centralizado
from sistema.sic import enviar_senal_log
from .config import SAFE_DATA_DIR, ZONA_HORARIA_LOCAL

# =============================================================================
# CONFIGURACIÓN DE DIRECTORIOS
# =============================================================================

# Directorio de velas (candles)
VELAS_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'candles')
TIMEFRAME_INTERVALS = {'M1': 60, 'M3': 180, 'M5': 300, 'M15': 900, 'H1': 3600, 'H4': 14400, 'D1': 86400}

# Directorios de logs
LOGS_DIR = os.path.join(SAFE_DATA_DIR, "data", "logs")
ERRORS_DIR = os.path.join(SAFE_DATA_DIR, "data", "logs", "errors")
CANDLES_DIR = os.path.join(SAFE_DATA_DIR, "data", "candles")

# Crear directorios si no existen
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(ERRORS_DIR, exist_ok=True)
os.makedirs(CANDLES_DIR, exist_ok=True)

# Rutas de archivos CSV
ANALISIS_LOG_PATH = os.path.join(LOGS_DIR, "analisis_periodico.csv")
ERROR_LOG_PATH = os.path.join(ERRORS_DIR, "errors_current.csv")
TRADE_DECISION_LOG_PATH = os.path.join(LOGS_DIR, "decisiones_trading.csv")
OPERACIONES_LOG_PATH = os.path.join(LOGS_DIR, "operaciones_ejecutadas.csv")
POSICIONES_CERRADAS_PATH = os.path.join(LOGS_DIR, "posiciones_cerradas.csv")
EVENTOS_LOG_PATH = os.path.join(LOGS_DIR, "eventos_sesion.csv")
DASHBOARD_ERRORS_LOG_PATH = os.path.join(LOGS_DIR, "dashboard_rendering_errors.csv")

# Buffer de errores para el dashboard
_error_buffer: List[str] = []
MAX_BUFFER_SIZE = 100

# =============================================================================
# SISTEMA DE INICIALIZACIÓN DE CANDLES
# =============================================================================

def inicializar_sistema_candles():
    """
    Verifica que existan los archivos CSV para cada timeframe.
    Si un archivo no existe, lo crea con las cabeceras correctas para evitar errores.
    """
    try:
        candles_dir = Path(VELAS_DIR)
        candles_dir.mkdir(parents=True, exist_ok=True)
        headers = ['time', 'open', 'high', 'low', 'close', 'volume']

        for tf in TIMEFRAME_INTERVALS.keys():
            archivo_tf = candles_dir / f"{tf}.csv"
            if not archivo_tf.exists():
                pd.DataFrame(columns=headers).to_csv(archivo_tf, index=False)
                enviar_senal_log("INFO", f"📁 Archivo {tf}.csv no encontrado. Creado archivo vacío.", __name__, "sistema")

        enviar_senal_log("INFO", "✅ Sistema de Candles verificado.", __name__, "sistema")

    except (FileNotFoundError, PermissionError, IOError) as e:
        enviar_senal_log("ERROR", f"❌ Error crítico al inicializar sistema de candles: {e}", __name__, "sistema")

# =============================================================================
# FUNCIONES DE LOGGING ESPECIALIZADAS
# =============================================================================

def log_event(evento: str, detalles: str = "") -> None:
    """Registra eventos importantes de la sesión en un archivo CSV."""
    try:
        os.makedirs(os.path.dirname(EVENTOS_LOG_PATH), exist_ok=True)
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')

        if not os.path.exists(EVENTOS_LOG_PATH):
            with open(EVENTOS_LOG_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'evento', 'detalles'])

        with open(EVENTOS_LOG_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, evento, detalles])

    except (FileNotFoundError, PermissionError, IOError) as e:
        enviar_senal_log("ERROR", f"Error al registrar evento: {str(e)}", "data_logger", "migration")
        add_error_to_buffer(f"Error al registrar evento: {str(e)}")

def log_checklist_evaluation(condiciones_cumplidas: int, total_condiciones: int,
                           veredicto: str, detalles_checklist: Optional[dict] = None) -> None:
    """Registra específicamente las evaluaciones del checklist ICT en un CSV dedicado."""
    try:
        checklist_log_path = os.path.join(LOGS_DIR, "checklist_evaluations.csv")
        os.makedirs(os.path.dirname(checklist_log_path), exist_ok=True)
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')

        if not os.path.exists(checklist_log_path):
            with open(checklist_log_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'condiciones_cumplidas', 'total_condiciones', 'veredicto',
                    'estructura_externa', 'estructura_interna', 'zona_precios',
                    'poi_relevante', 'confirmacion_momentum', 'sesion_trading'
                ])

        # Preparar datos del checklist
        if detalles_checklist and 'checklist' in detalles_checklist:
            checklist_data = detalles_checklist['checklist']
            estructura_externa = checklist_data.get('estructura_externa', False)
            estructura_interna = checklist_data.get('estructura_interna', False)
            zona_precios = checklist_data.get('zona_precios', False)
            poi_relevante = checklist_data.get('poi_relevante', False)
            confirmacion_momentum = checklist_data.get('confirmacion_momentum', False)
            sesion_trading = checklist_data.get('sesion_trading', False)
        else:
            estructura_externa = estructura_interna = zona_precios = False
            poi_relevante = confirmacion_momentum = sesion_trading = False

        with open(checklist_log_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, condiciones_cumplidas, total_condiciones, veredicto,
                estructura_externa, estructura_interna, zona_precios,
                poi_relevante, confirmacion_momentum, sesion_trading
            ])

        log_event("CHECKLIST_EVALUATION", f"{condiciones_cumplidas}/{total_condiciones} - {veredicto}")

    except (FileNotFoundError, PermissionError, IOError) as e:
        enviar_senal_log("ERROR", f"Error al registrar evaluación de checklist: {str(e)}", "data_logger", "migration")
        add_error_to_buffer(f"Error al registrar evaluación de checklist: {str(e)}")

def add_error_to_buffer(msg: object) -> None:
    """Añade un mensaje de error al buffer circular para el dashboard."""
    global _error_buffer
    try:
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%H:%M:%S')
        error_msg = str(msg).strip() if msg is not None else "Error desconocido"

        # Evitar duplicados consecutivos
        if _error_buffer and _error_buffer[-1].endswith(error_msg):
            return

        formatted_msg = f"{timestamp} - {error_msg}"
        _error_buffer.append(formatted_msg)

        # Mantener el tamaño del buffer
        while len(_error_buffer) > MAX_BUFFER_SIZE:
            _error_buffer.pop(0)

    except Exception as e:
        enviar_senal_log("ERROR", f"Error en add_error_to_buffer: {str(e)}", "data_logger", "migration")

def get_error_buffer() -> List[str]:
    """Obtiene la lista actual de errores en el buffer."""
    return _error_buffer.copy()

def clear_error_buffer():
    """Limpia el buffer de errores."""
    global _error_buffer
    _error_buffer.clear()

# =============================================================================
# GUARDADO DE VELAS (SISTEMA PRINCIPAL)
# =============================================================================

def guardar_velas(df: pd.DataFrame, timeframe: str, symbol: str) -> None:
    """Guarda las velas en un archivo CSV por mes, de forma segura y con logging robusto."""
    try:
        os.makedirs(CANDLES_DIR, exist_ok=True)

        # Nombre del archivo: EURUSD_M15_2025_08.csv
        fecha_actual = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL))
        nombre_archivo = f"{symbol}_{timeframe}_{fecha_actual.year}_{fecha_actual.month:02d}.csv"
        ruta_archivo = os.path.join(CANDLES_DIR, nombre_archivo)

        df_to_save = df.copy()

        # Normalizar precios para EURUSD si es necesario
        if symbol.upper() == "EURUSD":
            for price_col in ["open", "high", "low", "close"]:
                if price_col in df_to_save.columns:
                    col_data = df_to_save[price_col].astype(float)
                    while col_data.max() > 10:
                        col_data = col_data / 10
                    df_to_save[price_col] = col_data

        # Asegurar que la columna 'time' esté en formato datetime
        if 'time' in df_to_save.columns and not pd.api.types.is_datetime64_any_dtype(df_to_save['time']):
            df_to_save['time'] = pd.to_datetime(df_to_save['time'], unit='s')

        # Cargar datos existentes y fusionar
        if os.path.exists(ruta_archivo):
            df_existente = pd.read_csv(ruta_archivo, parse_dates=['time'])

            # Normalizar datos existentes si es necesario
            if symbol.upper() == "EURUSD":
                for price_col in ["open", "high", "low", "close"]:
                    if price_col in df_existente.columns:
                        col_data = df_existente[price_col].astype(float)
                        while col_data.max() > 10:
                            col_data = col_data / 10
                        df_existente[price_col] = col_data

            df_combinado = pd.concat([df_existente, df_to_save]).drop_duplicates(
                subset=['time'], keep='last').sort_values('time')
        else:
            df_combinado = df_to_save.sort_values('time')

        # Guardar en CSV
        df_combinado.to_csv(ruta_archivo, index=False)

        # Log exitoso
        log_event("GuardadoVelasExitoso", f"Velas {symbol} {timeframe} guardadas en {nombre_archivo} ({len(df_combinado)} registros)")

    except (FileNotFoundError, PermissionError, IOError) as e:
        error_msg = f"Error en guardar_velas ({timeframe}): {e}\n{traceback.format_exc()}"
        enviar_senal_log("ERROR", error_msg, __name__, "sistema")
        add_error_to_buffer(f"Error guardando velas {symbol} {timeframe}: {str(e)}")

def inicializar_directorio_candles():
    """Inicializa el directorio de velas en la ruta específica."""
    try:
        os.makedirs(CANDLES_DIR, exist_ok=True)
        log_event("InicializarDirectorioCandles", f"Directorio de velas inicializado: {CANDLES_DIR}")

        # Verificar que el directorio sea escribible
        test_file = os.path.join(CANDLES_DIR, "test_write.tmp")
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            log_event("VerificarDirectorioCandles", "Directorio de velas verificado como escribible")
        except (FileNotFoundError, PermissionError, IOError) as e:
            add_error_to_buffer(f"Error: Directorio de velas no es escribible: {str(e)}")

    except (FileNotFoundError, PermissionError, IOError) as e:
        add_error_to_buffer(f"Error creando directorio de velas: {str(e)}")

# =============================================================================
# LOGGING DE TRADING Y OPERACIONES
# =============================================================================

def inicializar_csvs_logger():
    """Inicializa los archivos CSV necesarios para el logging."""
    try:
        os.makedirs(SAFE_DATA_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(TRADE_DECISION_LOG_PATH), exist_ok=True)

        # Archivo de análisis periódico
        if not os.path.exists(ANALISIS_LOG_PATH):
            with open(ANALISIS_LOG_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'symbol', 'bid', 'ask', 'spread',
                    'k_value', 'd_value', 'k_prev', 'd_prev',
                    'cruce_k_d', 'cruce_d_k', 'sobreventa', 'sobrecompra',
                    'bb_upper', 'bb_sma', 'bb_lower', 'bb_width', 'bb_phase',
                    'account_balance', 'account_equity', 'floating_profit',
                    'open_positions', 'total_volume',
                    'suggested_action', 'no_trade_reason'
                ])

        # Archivo de eventos
        if not os.path.exists(EVENTOS_LOG_PATH):
            with open(EVENTOS_LOG_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'evento', 'detalles'])

        # Archivo de errores críticos
        if not os.path.exists(ERROR_LOG_PATH):
            with open(ERROR_LOG_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'module', 'function', 'error', 'stack_trace'])

        # Archivo de decisiones de trading
        if not os.path.exists(TRADE_DECISION_LOG_PATH):
            with open(TRADE_DECISION_LOG_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'symbol', 'current_price', 'spread',
                    'estoc_k', 'estoc_d', 'estoc_signal',
                    'bb_upper', 'bb_middle', 'bb_lower', 'bb_width', 'bb_phase',
                    'grid_conditions_met', 'grid_checklist',
                    'ict_m15_bias', 'ict_h1_bias', 'ict_h4_bias',
                    'final_decision', 'action_taken', 'rejection_reason'
                ])

        enviar_senal_log("INFO", "✅ Archivos CSV del logger inicializados correctamente", "data_logger", "migration")

    except (FileNotFoundError, PermissionError, IOError) as e:
        enviar_senal_log("ERROR", f"Error inicializando CSVs: {e}", "data_logger", "migration")
        raise

def log_trade_decision(symbol: str, current_price: float, spread: float,
                      estoc_data: dict, bb_data: dict, grid_data: dict,
                      ict_data: dict, final_decision: str, action_taken: str,
                      rejection_reason: str = "") -> None:
    """Registra una decisión de trading con toda la información relevante."""
    try:
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')
        os.makedirs(os.path.dirname(TRADE_DECISION_LOG_PATH), exist_ok=True)

        row_data = [
            timestamp, symbol, current_price, spread,
            estoc_data.get('k', 0), estoc_data.get('d', 0), estoc_data.get('signal', 'NEUTRAL'),
            bb_data.get('upper', 0), bb_data.get('middle', 0), bb_data.get('lower', 0),
            bb_data.get('width', 0), bb_data.get('phase', 'UNKNOWN'),
            grid_data.get('conditions_met', False), grid_data.get('checklist', '[]'),
            ict_data.get('M15', 'NEUTRAL'), ict_data.get('H1', 'NEUTRAL'), ict_data.get('H4', 'NEUTRAL'),
            final_decision, action_taken, rejection_reason
        ]

        with open(TRADE_DECISION_LOG_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row_data)

    except (FileNotFoundError, PermissionError, IOError) as e:
        enviar_senal_log("ERROR", f"Error al registrar decisión de trading: {str(e)}", "data_logger", "migration")
        add_error_to_buffer(f"Error al registrar decisión de trading: {str(e)}")

def log_posicion_cerrada(symbol: str, ticket: int, tipo: str, volumen: float,
                        precio_apertura: float, precio_cierre: float, profit: float,
                        motivo_cierre: str):
    """Registra una posición cerrada en el CSV de posiciones cerradas."""
    try:
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')

        # Asegurar que el archivo de posiciones cerradas existe
        if not os.path.exists(POSICIONES_CERRADAS_PATH):
            with open(POSICIONES_CERRADAS_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'symbol', 'ticket', 'tipo', 'volumen',
                               'precio_apertura', 'precio_cierre', 'profit', 'motivo_cierre'])

        with open(POSICIONES_CERRADAS_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, symbol, ticket, tipo, volumen,
                           precio_apertura, precio_cierre, profit, motivo_cierre])
    except (FileNotFoundError, PermissionError, IOError) as e:
        add_error_to_buffer(f"Error en log de posición cerrada: {e}")

def log_error_critico(modulo: str, funcion: str, error: str, stack_trace: Optional[str] = None):
    """Registra errores críticos en CSV y buffer."""
    try:
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')

        # Asegurar que el archivo de errores existe
        if not os.path.exists(ERROR_LOG_PATH):
            with open(ERROR_LOG_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'module', 'function', 'error', 'stack_trace'])

        with open(ERROR_LOG_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, modulo, funcion, error, stack_trace or ''])

        # Añadir al buffer para el dashboard
        add_error_to_buffer(f"[{modulo}] {error}")
    except (FileNotFoundError, PermissionError, IOError) as e:
        enviar_senal_log("ERROR", f"Error en log_error_critico: {e}", "data_logger", "migration")

# =============================================================================
# SISTEMA DE MANEJO GLOBAL DE EXCEPCIONES
# =============================================================================

def install_global_exception_handler():
    """Instala un manejador global para capturar todas las excepciones no controladas."""
    original_excepthook = sys.excepthook

    def custom_exception_handler(exc_type, exc_value, exc_traceback):
        """Manejador personalizado que registra y muestra todos los errores."""
        error_msg = str(exc_value) if exc_value else str(exc_type)
        full_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))

        enviar_senal_log("ERROR", f"EXCEPCIÓN NO CAPTURADA: {error_msg}\n{full_traceback}", __name__, "sistema")
        add_error_to_buffer(f"Excepción crítica: {error_msg}")

        # Llamar al manejador original
        original_excepthook(exc_type, exc_value, exc_traceback)

    sys.excepthook = custom_exception_handler
    enviar_senal_log("INFO", "Manejador global de excepciones instalado.", "data_logger", "sistema")

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def log_dashboard_error(panel_name: str, error: Exception):
    """Registra un error específico ocurrido durante el renderizado de un panel del dashboard."""
    try:
        os.makedirs(os.path.dirname(DASHBOARD_ERRORS_LOG_PATH), exist_ok=True)

        if not os.path.exists(DASHBOARD_ERRORS_LOG_PATH):
            with open(DASHBOARD_ERRORS_LOG_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'panel_name', 'error_type', 'error_message', 'traceback'])

        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')
        error_type = type(error).__name__
        error_message = str(error)
        full_traceback = ''.join(traceback.format_exception(type(error), error, error.__traceback__))

        with open(DASHBOARD_ERRORS_LOG_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, panel_name, error_type, error_message, full_traceback])

        add_error_to_buffer(f"Dashboard error en {panel_name}: {error_message}")

    except (FileNotFoundError, PermissionError, IOError) as e:
        enviar_senal_log("ERROR", f"Error en log_dashboard_error: {e}", "data_logger", "migration")
        add_error_to_buffer(f"Error crítico en logging de dashboard: {str(e)}")

def verificar_csv_fractal_actual():
    """Verifica que el CSV fractal del día tenga datos."""
    csv_fractal = os.path.join(
        "data", "logs", "fractal", f"fractal_analysis_{datetime.now().strftime('%Y%m%d')}.csv"
    )
    if not os.path.exists(csv_fractal) or os.path.getsize(csv_fractal) == 0:
        enviar_senal_log("ERROR", f"❌ El archivo {csv_fractal} no se está llenando correctamente.", __name__, "sistema")
        return False
    enviar_senal_log("INFO", f"✅ El archivo {csv_fractal} tiene datos.", __name__, "sistema")
    return True

# =============================================================================
# INICIALIZACIÓN AUTOMÁTICA
# =============================================================================

# Inicializar sistema al importar
try:
    inicializar_directorio_candles()
except Exception as e:
    print(f"Error en inicialización automática de data_logger: {e}")
