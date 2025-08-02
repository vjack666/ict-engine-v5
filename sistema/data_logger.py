# =============================================================================
# SECCIÓN X: INICIALIZACIÓN DEL SISTEMA DE CANDLES (ROBUSTO Y MODULAR)
# =============================================================================

import os
from pathlib import Path
# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log

from typing import Optional

# Directorio de velas (candles)
VELAS_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'candles')
TIMEFRAME_INTERVALS = {'M1': 60, 'M3': 180, 'M5': 300, 'M15': 900, 'H1': 3600, 'H4': 14400, 'D1': 86400}

def inicializar_sistema_candles():
    """
    Verifica que existan los archivos CSV para cada timeframe.
    Si un archivo no existe, lo crea con las cabeceras correctas para evitar errores.
    Esta es la versión profesional y modularizada.
    """
    try:
        candles_dir = Path(VELAS_DIR)
        candles_dir.mkdir(parents=True, exist_ok=True)
        headers = ['time', 'open', 'high', 'low', 'close', 'volume']
        for tf in TIMEFRAME_INTERVALS.keys():
            archivo_tf = candles_dir / f"{tf}.csv"
            if not archivo_tf.exists():
                # Si el archivo no existe, lo creamos vacío pero con cabeceras
                pd.DataFrame(columns=headers).to_csv(archivo_tf, index=False)
                if 'force_log_and_print' in globals():
                    force_log_and_print("CANDLE_INIT", f"📁 Archivo {tf}.csv no encontrado. Creado archivo vacío.", False)
        if 'force_log_and_print' in globals():
            force_log_and_print("CANDLE_INIT", "✅ Sistema de Candles verificado.", False)
    except (FileNotFoundError, PermissionError, IOError) as e:
        if 'force_log_and_print' in globals():
            force_log_and_print("CANDLE_INIT", f"❌ Error crítico al inicializar sistema de candles: {e}", True)

# =============================================================================
# SECCIÓN 9: CAPTURA DE SALIDA ESTÁNDAR PARA DEBUGGING DE RICH
# =============================================================================
import sys
import pandas as pd
from datetime import datetime
import pytz
import csv

class StreamInterceptor:
    """
    Clase que simula un stream (como sys.stdout) y redirige la salida
    tanto al stream original (para que siga viéndose en consola) como a un
    archivo de log para una auditoría completa.
    """
    def __init__(self, original_stream, log_file_path):
        self.original_stream = original_stream
        self.log_file = open(log_file_path, 'a', encoding='utf-8')

    def write(self, buf):
        try:
            self.original_stream.write(buf)
            if buf.strip():
                timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S.%f')
                self.log_file.write(f"[{timestamp}] {buf}")
            self.flush()
        except (FileNotFoundError, PermissionError, IOError) as e:
            self.original_stream.write(f"\n[StreamInterceptor CRITICAL ERROR] {e}\n")

    def flush(self):
        self.original_stream.flush()
        self.log_file.flush()

    def __del__(self):
        if self.log_file:
            self.log_file.close()

def redirect_stdout_to_file(log_dir="../../data/logs/terminal_capture"):
    """
    Redirige sys.stdout y sys.stderr a un archivo para capturar toda la salida.
    Esto es crucial para depurar qué se está imprimiendo mientras Rich está activo.
    """
    try:
        os.makedirs(log_dir, exist_ok=True)
        date_str = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime("%Y-%m-%d")
        log_file_path = os.path.join(log_dir, f"full_terminal_output_{date_str}.log")

        original_stdout = sys.stdout
        original_stderr = sys.stderr

        sys.stdout = StreamInterceptor(original_stdout, log_file_path)
        sys.stderr = StreamInterceptor(original_stderr, log_file_path)

        print(f"\n✅ [DEBUG] Captura total de consola activada. Log en: {log_file_path}\n")
    except (FileNotFoundError, PermissionError, IOError) as e:
        sys.stdout.write(f"\n❌ [CRITICAL] No se pudo redirigir la salida de la consola: {e}\n")


def log_dashboard_error(panel_name: str, error: Exception):
    """
    Registra un error específico ocurrido durante el renderizado de un panel del dashboard.
    Este es el log "rich debug" que solicitaste.
    """
    try:
        # Asegurar que el directorio de logs existe
        os.makedirs(os.path.dirname(DASHBOARD_ERRORS_LOG_PATH), exist_ok=True)

        # Crear el archivo con encabezados si no existe
        if not os.path.exists(DASHBOARD_ERRORS_LOG_PATH):
            with open(DASHBOARD_ERRORS_LOG_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'panel_name', 'error_type', 'error_message', 'traceback'])

        # Registrar el error
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')
        error_type = type(error).__name__
        error_message = str(error)
        full_traceback = ''.join(traceback.format_exception(type(error), error, error.__traceback__))

        with open(DASHBOARD_ERRORS_LOG_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, panel_name, error_type, error_message, full_traceback])

    except (FileNotFoundError, PermissionError, IOError) as log_err:
        # Si el propio logger falla, lo imprimimos para no perder el error original.
        print(f"[CRITICAL LOGGER ERROR] No se pudo escribir en dashboard_errors.log: {log_err}")
        print(f"[ORIGINAL ERROR] Panel: {panel_name}, Error: {error}")
# data_logger.py

# =============================================================================
# SECCIÓN 1: IMPORTACIONES DE LIBRERÍAS
# =============================================================================
from typing import List, Optional
import traceback

from .config import SAFE_DATA_DIR, ZONA_HORARIA_LOCAL

# =============================================================================
# SECCIÓN 2: VARIABLES GLOBALES Y PATHS
# =============================================================================

# Nueva carpeta de logs (usando la estructura existente)
LOGS_DIR = os.path.join(SAFE_DATA_DIR, "data", "logs")
ERRORS_DIR = os.path.join(SAFE_DATA_DIR, "data", "logs", "errors")
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(ERRORS_DIR, exist_ok=True)

# Rutas de archivos CSV en la nueva carpeta
ANALISIS_LOG_PATH = os.path.join(LOGS_DIR, "analisis_periodico.csv")
ERROR_LOG_PATH = os.path.join(ERRORS_DIR, "errors_current.csv")
TRADE_DECISION_LOG_PATH = os.path.join(LOGS_DIR, "decisiones_trading.csv")
OPERACIONES_LOG_PATH = os.path.join(LOGS_DIR, "operaciones_ejecutadas.csv")
POSICIONES_CERRADAS_PATH = os.path.join(LOGS_DIR, "posiciones_cerradas.csv")
EVENTOS_LOG_PATH = os.path.join(LOGS_DIR, "eventos_sesion.csv")

# Ruta para el nuevo log de errores de la interfaz
DASHBOARD_ERRORS_LOG_PATH = os.path.join(LOGS_DIR, "dashboard_rendering_errors.csv")

# Buffer de errores para el dashboard
_error_buffer: List[str] = []
MAX_BUFFER_SIZE = 100

# =============================================================================
# SECCIÓN 3: FUNCIONES DE LOGGING
# =============================================================================

def log_checklist_evaluation(condiciones_cumplidas: int, total_condiciones: int, veredicto: str, detalles_checklist: Optional[dict] = None) -> None:
    """
    Registra específicamente las evaluaciones del checklist ICT en un CSV dedicado.
    
    Args:
        condiciones_cumplidas (int): Número de condiciones cumplidas
        total_condiciones (int): Total de condiciones evaluadas
        veredicto (str): Veredicto final del checklist
        detalles_checklist (dict): Detalles de cada condición (opcional)
    """
    try:
        checklist_log_path = os.path.join(LOGS_DIR, "checklist_evaluations.csv")
        os.makedirs(os.path.dirname(checklist_log_path), exist_ok=True)
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')
        
        # Crear archivo si no existe
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
        
        # Agregar la evaluación
        with open(checklist_log_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, condiciones_cumplidas, total_condiciones, veredicto,
                estructura_externa, estructura_interna, zona_precios,
                poi_relevante, confirmacion_momentum, sesion_trading
            ])
            
        # También registrar en el log general de eventos
        log_event("CHECKLIST_EVALUATION", f"{condiciones_cumplidas}/{total_condiciones} - {veredicto}")
            
    except (FileNotFoundError, PermissionError, IOError) as e:
        error_msg = f"Error al registrar evaluación de checklist: {str(e)}"
        add_error_to_buffer(error_msg)

def log_event(evento: str, detalles: str = "") -> None:
    """
    Registra eventos importantes de la sesión en un archivo CSV.
    
    Args:
        evento (str): Nombre o tipo del evento
        detalles (str): Detalles adicionales del evento
    """
    try:
        os.makedirs(os.path.dirname(EVENTOS_LOG_PATH), exist_ok=True)
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')
        
        # Crear archivo si no existe
        if not os.path.exists(EVENTOS_LOG_PATH):
            with open(EVENTOS_LOG_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'evento', 'detalles'])
        
        # Agregar el evento
        with open(EVENTOS_LOG_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, evento, detalles])
            
    except (FileNotFoundError, PermissionError, IOError) as e:
        error_msg = f"Error al registrar evento: {str(e)}"
        print(f"[ERROR] {error_msg}")
        add_error_to_buffer(error_msg)

def inicializar_csvs_logger():
    """Inicializa los archivos CSV necesarios para el logging."""
    try:
        os.makedirs(SAFE_DATA_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(TRADE_DECISION_LOG_PATH), exist_ok=True)
        
        # Crear o verificar archivo de análisis periódico
        if not os.path.exists(ANALISIS_LOG_PATH):
            with open(ANALISIS_LOG_PATH, 'w', newline='') as f:
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
        
        # Crear o verificar archivo de eventos
        if not os.path.exists(EVENTOS_LOG_PATH):
            with open(EVENTOS_LOG_PATH, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'evento', 'detalles'])
        
        # Crear o verificar archivo de errores críticos
        if not os.path.exists(ERROR_LOG_PATH):
            with open(ERROR_LOG_PATH, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'module', 'function', 'error', 'stack_trace'])
        
        # Crear o verificar archivo de operaciones ejecutadas
        if not os.path.exists(OPERACIONES_LOG_PATH):
            with open(OPERACIONES_LOG_PATH, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'symbol', 'ticket', 'type', 'volume',
                    'price_open', 'tp', 'sl', 'strategy', 'estoc_info', 
                    'grid_info', 'bollinger_info', 'error_details'
                ])

        # Crear o verificar archivo de decisiones de trading
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
        
    except (FileNotFoundError, PermissionError, IOError) as e:
        print(f"[CRITICAL] Error inicializando CSVs: {e}")
        raise

def log_analisis_periodico(symbol: str, bid: float, ask: float, spread: float,
                          k: float, d: float, k_prev: float, d_prev: float,
                          cruce_k_d: bool, cruce_d_k: bool, sobreventa: bool, sobrecompra: bool,
                          bb_upper: float, bb_sma: float, bb_lower: float, bb_width: float, bb_phase: str,
                          balance: float, equity: float, floating_profit: float,
                          open_positions: int, total_volume: float,
                          suggested_action: str, no_trade_reason: str):
    """Registra el análisis periódico del bot en CSV."""
    try:
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')
        with open(ANALISIS_LOG_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, symbol, bid, ask, spread,
                k, d, k_prev, d_prev,
                cruce_k_d, cruce_d_k, sobreventa, sobrecompra,
                bb_upper, bb_sma, bb_lower, bb_width, bb_phase,
                balance, equity, floating_profit,
                open_positions, total_volume,
                suggested_action, no_trade_reason
            ])
    except (FileNotFoundError, PermissionError, IOError) as e:
        add_error_to_buffer(f"Error en log periódico: {e}")

def log_error_critico(modulo: str, funcion: str, error: str, stack_trace: Optional[str] = None):
    """Registra errores críticos en CSV y buffer."""
    try:
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')
        with open(ERROR_LOG_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, modulo, funcion, error, stack_trace or ''])
        
        # Añadir al buffer para el dashboard
        add_error_to_buffer(f"[{modulo}] {error}")
    except (FileNotFoundError, PermissionError, IOError) as e:
        print(f"[CRITICAL] Error en log_error_critico: {e}")

def add_error_to_buffer(msg: object) -> None:
    """Añade un mensaje de error al buffer circular para el dashboard."""
    global _error_buffer
    try:
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%H:%M:%S')
        # Asegurarse de que el mensaje no sea None y sea una cadena
        if msg is None:
            error_msg = "Error desconocido"
        else:
            error_msg = str(msg).strip()
        
        # Evitar duplicados consecutivos
        if _error_buffer and _error_buffer[-1].endswith(error_msg):
            return
            
        formatted_msg = f"{timestamp} - {error_msg}"
        _error_buffer.append(formatted_msg)
        
        # Mantener el tamaño del buffer
        while len(_error_buffer) > MAX_BUFFER_SIZE:
            _error_buffer.pop(0)
    except (FileNotFoundError, PermissionError, IOError) as e:
        print(f"Error en add_error_to_buffer: {str(e)}")

def get_error_buffer() -> List[str]:
    """Obtiene la lista actual de errores en el buffer."""
    return _error_buffer.copy()

def clear_error_buffer():
    """Limpia el buffer de errores."""
    global _error_buffer
    _error_buffer.clear()

def log_operacion_ejecutada(symbol: str, ticket: int, tipo: str, volumen: float,
                          precio_apertura: float, tp: float, sl: float,
                          estrategia: str, estoc_info: Optional[dict] = None, grid_info: Optional[dict] = None,
                          bollinger_info: Optional[dict] = None, error_detalle: str = ""):
    """
    Registra una operación ejecutada en el CSV de operaciones.
    
    Args:
        symbol: Símbolo del instrumento
        ticket: Número de ticket de la orden
        tipo: Tipo de operación (BUY/SELL)
        volumen: Tamaño del lote
        precio_apertura: Precio de apertura
        tp: Take Profit
        sl: Stop Loss
        estrategia: Nombre de la estrategia
        estoc_info: Info del estocástico (opcional)
        grid_info: Info del grid (opcional)
        bollinger_info: Info de Bollinger (opcional)
        error_detalle: Detalles del error si la operación falló (opcional)
    """
    try:
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')
        with open(OPERACIONES_LOG_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, symbol, ticket, tipo, volumen,
                precio_apertura, tp, sl, estrategia,
                str(estoc_info) if estoc_info else '',
                str(grid_info) if grid_info else '',
                str(bollinger_info) if bollinger_info else '',
                error_detalle
            ])
    except (FileNotFoundError, PermissionError, IOError) as e:
        add_error_to_buffer(f"Error en log de operación: {e}")

def log_posicion_cerrada(symbol: str, ticket: int, tipo: str, volumen: float,
                        precio_apertura: float, precio_cierre: float, profit: float,
                        motivo_cierre: str):
    """Registra una posición cerrada en el CSV de posiciones cerradas."""
    try:
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')
        with open(POSICIONES_CERRADAS_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, symbol, ticket, tipo, volumen,
                precio_apertura, precio_cierre, profit, motivo_cierre
            ])
    except (FileNotFoundError, PermissionError, IOError) as e:
        add_error_to_buffer(f"Error en log de posición cerrada: {e}")

# =============================================================================
# SECCIÓN 5: LOG DE DECISIONES DE TRADING
# =============================================================================

def log_trade_decision(
    symbol: str,
    current_price: float,
    spread: float,
    estoc_data: dict,
    bb_data: dict,
    grid_data: dict,
    ict_data: dict,
    final_decision: str,
    action_taken: str,
    rejection_reason: str = ""
) -> None:
    """
    Registra una decisión de trading con toda la información relevante.
    
    Args:
        symbol: Símbolo del instrumento
        current_price: Precio actual del instrumento
        spread: Spread actual
        estoc_data: Diccionario con datos del estocástico (k, d, signal)
        bb_data: Diccionario con datos de Bollinger (upper, middle, lower, width, phase)
        grid_data: Diccionario con datos del grid (conditions_met, checklist)
        ict_data: Diccionario con sesgos ICT por timeframe (M15, H1, H4)
        final_decision: Decisión final tomada
        action_taken: Acción ejecutada
        rejection_reason: Razón por la que se rechazó la operación (si aplica)
    """
    try:
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')
        
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(TRADE_DECISION_LOG_PATH), exist_ok=True)
        
        # Preparar los datos para el CSV
        row_data = [
            timestamp, symbol, current_price, spread,
            estoc_data.get('k', 0), estoc_data.get('d', 0), estoc_data.get('signal', 'NEUTRAL'),
            bb_data.get('upper', 0), bb_data.get('middle', 0), bb_data.get('lower', 0),
            bb_data.get('width', 0), bb_data.get('phase', 'UNKNOWN'),
            grid_data.get('conditions_met', False), grid_data.get('checklist', '[]'),
            ict_data.get('M15', 'NEUTRAL'), ict_data.get('H1', 'NEUTRAL'), ict_data.get('H4', 'NEUTRAL'),
            final_decision, action_taken, rejection_reason
        ]
        
        # Escribir al CSV
        with open(TRADE_DECISION_LOG_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row_data)
            
    except (FileNotFoundError, PermissionError, IOError) as e:
        error_msg = f"Error al registrar decisión de trading: {str(e)}"
        print(f"[ERROR] {error_msg}")
        add_error_to_buffer(error_msg)

# =============================================================================
# SECCIÓN 6: GUARDADO DE VELAS
# =============================================================================


# =============================================================================
# SECCIÓN 6: GUARDADO DE VELAS (CORREGIDO Y ROBUSTO)
# =============================================================================

# Usar la ruta centralizada y robusta definida en config.py
CANDLES_DIR = os.path.join(SAFE_DATA_DIR, "data", "candles")

def guardar_velas(df: pd.DataFrame, timeframe: str, symbol: str) -> None:
    """
    Guarda las velas en un archivo CSV por mes, de forma segura y con logging robusto.
    """
    try:
        # Asegurar que el directorio de destino exista
        os.makedirs(CANDLES_DIR, exist_ok=True)

        # Nombre del archivo: EURUSD_M15_2025_07.csv
        fecha_actual = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL))
        nombre_archivo = f"{symbol}_{timeframe}_{fecha_actual.year}_{fecha_actual.month:02d}.csv"
        ruta_archivo = os.path.join(CANDLES_DIR, nombre_archivo)


        df_to_save = df.copy()

        # Normalizar precios para EURUSD: open, high, low, close a rango 1.xxxxx
        def normalize_price_col(col):
            if col.name in ["open", "high", "low", "close"]:
                # Solo normalizar si hay valores fuera de rango típico
                col = col.astype(float)
                while col.max() > 10:
                    col = col / 10
                return col
            return col
        if symbol.upper() == "EURUSD":
            for price_col in ["open", "high", "low", "close"]:
                if price_col in df_to_save.columns:
                    df_to_save[price_col] = normalize_price_col(df_to_save[price_col])

        # Asegurar que la columna 'time' esté en formato datetime
        if 'time' in df_to_save.columns and not pd.api.types.is_datetime64_any_dtype(df_to_save['time']):
            df_to_save['time'] = pd.to_datetime(df_to_save['time'], unit='s')

        # Cargar datos existentes y fusionar, evitando duplicados
        if os.path.exists(ruta_archivo):
            df_existente = pd.read_csv(ruta_archivo, parse_dates=['time'])
            # Normalizar también los datos existentes si es necesario
            if symbol.upper() == "EURUSD":
                for price_col in ["open", "high", "low", "close"]:
                    if price_col in df_existente.columns:
                        df_existente[price_col] = normalize_price_col(df_existente[price_col])
            df_combinado = pd.concat([df_existente, df_to_save]).drop_duplicates(subset=['time'], keep='last').sort_values('time')
        else:
            df_combinado = df_to_save.sort_values('time')

        # Guardar en CSV
        df_combinado.to_csv(ruta_archivo, index=False)

        # Log limpio en segundo plano
        log_event("GuardadoVelasExitoso", f"Velas {symbol} {timeframe} guardadas en {nombre_archivo} ({len(df_combinado)} regs)")

    except (FileNotFoundError, PermissionError, IOError) as e:
        # Logging robusto y visible
        error_completo = f"Error en guardar_velas ({timeframe}): {e}\n{traceback.format_exc()}"
        force_log_and_print("DATA_LOGGER", error_completo, es_error=True)

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
            log_event("VerificarDirectorioCandles", f"Directorio de velas verificado como escribible")
        except (FileNotFoundError, PermissionError, IOError) as e:
            error_msg = f"Error: Directorio de velas no es escribible: {str(e)}"
            add_error_to_buffer(error_msg)
    except (FileNotFoundError, PermissionError, IOError) as e:
        error_msg = f"Error creando directorio de velas: {str(e)}"
        add_error_to_buffer(error_msg)

# ...eliminada la versión duplicada y defectuosa de guardar_velas...

# =============================================================================
# SECCIÓN 7: SISTEMA DE CAPTURA GLOBAL DE EXCEPCIONES
# =============================================================================
def install_global_exception_handler():
    """Instala un manejador global para capturar todas las excepciones no controladas."""
    
    original_excepthook = sys.excepthook
    
    def custom_exception_handler(exc_type, exc_value, exc_traceback):
        """Manejador personalizado que registra y muestra todos los errores."""
        error_msg = str(exc_value) if exc_value else str(exc_type)
        full_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        
        # Forzar el log y la impresión para asegurar visibilidad
        force_log_and_print("GLOBAL_HANDLER", f"EXCEPCIÓN NO CAPTURADA: {error_msg}\n{full_traceback}", True)
        
        # Llamar al manejador original para no romper el flujo normal de salida de errores
        original_excepthook(exc_type, exc_value, exc_traceback)
    
    sys.excepthook = custom_exception_handler
    print("[LOGGER] OK Manejador global de excepciones instalado.")

def force_log_and_print(modulo: str, mensaje: str, es_error: bool = True):
    """
    Fuerza el logging a archivo y opcionalmente imprime en consola.
    NOTA: Cuando se usa Rich dashboard, solo loggea a archivo para evitar interferencias.
    """
    try:
        timestamp = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')
        prefix = "[ERROR]" if es_error else "[INFO]"
        
        # CAMBIO IMPORTANTE: NO imprimir para evitar interferir con Rich dashboard
        # Los mensajes importantes se envían al terminal del dashboard usando add_terminal_log()
        # print(f"\n{prefix} {timestamp} [{modulo}]: {mensaje}\n")
        
        # En su lugar, usar el sistema de captura CSV para logging manual
        global _terminal_capture
        if _terminal_capture:
            _terminal_capture._log_to_csv('FORCE_LOG', f"{prefix} {timestamp} [{modulo}]: {mensaje}")
        
        # Registrar en el archivo apropiado
        if es_error:
            add_error_to_buffer(f"{modulo}: {mensaje}")
            try:
                with open(ERROR_LOG_PATH, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, modulo, "FORCED_LOG", mensaje, ""])
            except (FileNotFoundError, PermissionError, IOError) as log_e:
                 # No print aquí tampoco para evitar loops
                 pass

    except (FileNotFoundError, PermissionError, IOError) as e:
        # No print aquí para evitar loops infinitos
        pass

# =============================================================================
# SECCIÓN 7: FUNCIONES DE LOGGING EXISTENTES (mantenidas)
# =============================================================================

# =============================================================================
# SECCIÓN 8: LOGGING DE MarketContext (para debug y auditoría)
# =============================================================================
def log_market_context_to_csv(market_context):
    """
    Registra el estado actual de MarketContext en un archivo CSV para auditoría/debug.
    El archivo se guarda en data/logs/market_context/YYYYMMDD_market_context.csv
    """
    try:

        # Directorio y archivo
        log_dir = Path("../data/logs/market_context")
        log_dir.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime("%Y%m%d")
        csv_file = log_dir / f"{date_str}_market_context.csv"

        # Convertir el MarketContext a un dict plano (serializable)
        def flatten_context(ctx):
            d = {}
            for k, v in ctx.__dict__.items():
                if hasattr(v, 'tolist'):
                    d[k] = v.tolist()
                elif isinstance(v, (dict, list, str, int, float, type(None))):
                    d[k] = v
                elif hasattr(v, '__dict__'):
                    d[k] = str(v)
                else:
                    d[k] = str(v)
            return d

        row = flatten_context(market_context)
        row['timestamp'] = datetime.now(pytz.timezone(ZONA_HORARIA_LOCAL)).strftime('%Y-%m-%d %H:%M:%S')

        # Escribir encabezado si el archivo no existe
        write_header = not csv_file.exists()
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(row.keys()))
            if write_header:
                writer.writeheader()
            writer.writerow(row)
    except (FileNotFoundError, PermissionError, IOError) as e:
        add_error_to_buffer(f"Error en log_market_context_to_csv: {e}")


# =============================================================================
# SECCIÓN: CAPTURA COMPLETA DE SALIDAS TERMINAL EN CSV
# =============================================================================

class TerminalCaptureCSV:
    """
    Captura TODAS las salidas del terminal (prints, errores, etc.) 
    excepto Rich y las guarda en CSV para análisis completo
    """
    def __init__(self, csv_dir="../data/logs/terminal_capture"):
        self.csv_dir = Path(csv_dir)
        self.csv_dir.mkdir(parents=True, exist_ok=True)
        
        # Importar zona horaria desde config
        try:
            from .config import ZONA_HORARIA_LOCAL
            self.timezone = ZONA_HORARIA_LOCAL
        except ImportError:
            self.timezone = 'America/Guayaquil'  # Fallback
        
        # Archivo CSV diario
        date_str = datetime.now(pytz.timezone(self.timezone)).strftime("%Y-%m-%d")
        self.csv_file = self.csv_dir / f"terminal_capture_{date_str}.csv"
        
        # Referencias originales
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        
        # Contador de mensajes
        self.message_count = 0
        
        # Inicializar CSV
        self._init_csv()
        
    def _init_csv(self):
        """Inicializa el archivo CSV con headers si no existe"""
        if not self.csv_file.exists():
            headers = ['timestamp', 'message_id', 'stream_type', 'content', 'length', 'is_rich_related']
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
    
    def _is_rich_output(self, content):
        """Detecta si el contenido es de Rich dashboard"""
        rich_indicators = [
            '\x1b[',  # Códigos ANSI de Rich
            '\033[',  # Códigos de escape
            '╭─', '╰─', '│',  # Caracteres de box de Rich
            '\r',  # Carriage return usado por Rich Live
        ]
        return any(indicator in content for indicator in rich_indicators)
    
    def _log_to_csv(self, stream_type, content):
        """Loggea el contenido al CSV"""
        try:
            if not content.strip():
                return  # No loggear líneas vacías
                
            self.message_count += 1
            timestamp = datetime.now(pytz.timezone(self.timezone)).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            
            is_rich = self._is_rich_output(content)
            
            # Solo loggear si NO es Rich
            if not is_rich:
                row = [
                    timestamp,
                    self.message_count,
                    stream_type,
                    content.strip().replace('\n', '\\n').replace('\r', '\\r'),
                    len(content),
                    'NO'
                ]
                
                with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(row)
        except (FileNotFoundError, PermissionError, IOError) as e:
            # Fallar silenciosamente para no crear loops infinitos
            pass
    
    def write_stdout(self, content):
        """Captura stdout"""
        self.original_stdout.write(content)
        self._log_to_csv('STDOUT', content)
        
    def write_stderr(self, content):
        """Captura stderr"""
        self.original_stderr.write(content)
        self._log_to_csv('STDERR', content)
        
    def flush_stdout(self):
        """Flush stdout"""
        self.original_stdout.flush()
        
    def flush_stderr(self):
        """Flush stderr"""
        self.original_stderr.flush()


class StdoutInterceptor:
    """Interceptor para stdout"""
    def __init__(self, capture_system):
        self.capture = capture_system
    
    def write(self, content):
        self.capture.write_stdout(content)
    
    def flush(self):
        self.capture.flush_stdout()


class StderrInterceptor:
    """Interceptor para stderr"""
    def __init__(self, capture_system):
        self.capture = capture_system
    
    def write(self, content):
        self.capture.write_stderr(content)
    
    def flush(self):
        self.capture.flush_stderr()


# Variable global para el sistema de captura
_terminal_capture = None

def install_terminal_capture_csv():
    """
    Instala el sistema de captura de terminal en CSV
    DEBE llamarse ANTES de cualquier print o Rich
    """
    global _terminal_capture
    
    try:
        _terminal_capture = TerminalCaptureCSV()
        
        # Redirigir stdout y stderr
        sys.stdout = StdoutInterceptor(_terminal_capture)
        sys.stderr = StderrInterceptor(_terminal_capture)
        
        # Loggear que el sistema está activo
        _terminal_capture._log_to_csv('SYSTEM', 'Terminal capture CSV iniciado correctamente')
        
        return True
    except (FileNotFoundError, PermissionError, IOError) as e:
        print(f"Error instalando terminal capture CSV: {e}")
        return False

def get_terminal_capture_stats():
    """Retorna estadísticas del sistema de captura"""
    global _terminal_capture
    if _terminal_capture:
        return {
            'csv_file': str(_terminal_capture.csv_file),
            'message_count': _terminal_capture.message_count,
            'is_active': True
        }
    return {'is_active': False}

def log_manual_message(message, message_type="MANUAL"):
    """Permite loggear mensajes manualmente al CSV"""
    global _terminal_capture
    if _terminal_capture:
        _terminal_capture._log_to_csv(message_type, message)

def verificar_csv_fractal_actual():
    """Verifica que el CSV fractal del día tenga datos."""
    csv_fractal = os.path.join(
        "data", "logs", "fractal", f"fractal_analysis_{datetime.now().strftime('%Y%m%d')}.csv"
    )
    if not os.path.exists(csv_fractal) or os.path.getsize(csv_fractal) == 0:
        force_log_and_print("MAIN", f"❌ El archivo {csv_fractal} no se está llenando correctamente.", True)
        return False
    force_log_and_print("MAIN", f"✅ El archivo {csv_fractal} tiene datos.", False)
    return True
