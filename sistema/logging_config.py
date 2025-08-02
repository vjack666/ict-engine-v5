# sistema/logging_config.py
"""
Sistema de Logging Centralizado para Sentinel Grid System
=========================================================

Sistema de "caja negra" para registro granular de todas las operaciones.
Permite reconstruir cada decisión y estado del mercado.
"""

# Fix para emojis en logs Windows
import sys
import os
if sys.platform == "win32":
    os.environ['PYTHONIOENCODING'] = 'utf-8'

import logging
import logging.handlers
from pathlib import Path
import sys
import json
from datetime import datetime
from typing import Optional, Dict, Any

# Crear rutas de log de forma segura
log_dir = Path(__file__).resolve().parents[1] / "data" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

class JsonFormatter(logging.Formatter):
    """
    Formateador que convierte registros de log en JSON estructurado.
    Ideal para análisis de datos y consumo por IAs externas.
    """
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "emisor": getattr(record, 'emisor', record.name),
            "categoria": getattr(record, 'categoria', 'general'),
            "mensaje": record.getMessage(),
            "metadata": getattr(record, 'metadata', {}),
            "modulo": record.module,
            "funcion": record.funcName,
            "linea": record.lineno
        }
        return json.dumps(log_record, ensure_ascii=False)

class CsvMetricsFormatter(logging.Formatter):
    """
    Formateador especializado para métricas en formato CSV.
    """
    def format(self, record):
        # El timestamp se añade automáticamente
        return f"{self.formatTime(record, '%Y-%m-%d %H:%M:%S')},{record.getMessage()}"

def setup_logging():
    """
    Configura el sistema de logging de forma centralizada.
    
    NIVELES DE LOGGING:
    - DEBUG: "La última pulga" - todos los detalles internos
    - INFO: Operaciones normales, decisiones importantes
    - WARNING: Condiciones anómalas que no impiden operación
    - ERROR: Errores que afectan funcionalidad
    - CRITICAL: Errores que pueden parar el sistema
    """
    
    # 1. Formato de los logs: Incluye todo lo necesario para análisis forense
    # [NIVEL] [TIMESTAMP] [MÓDULO:FUNCIÓN:LÍNEA] MENSAJE
    log_format = logging.Formatter(
        '%(levelname)-8s | %(asctime)s | %(module)s:%(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 2. Obtener el logger raíz. Todos los demás loggers heredarán de este.
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Capturamos TODO, luego los handlers filtran

    # Evitar duplicación de handlers si la función es llamada múltiples veces
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # 3. Handler para la CONSOLA (MODO SILENCIOSO ACTIVADO)
    # 🔇 OPERACIÓN LIMPIEZA: Solo errores críticos en terminal para dashboard limpio
    # Seguimos el patrón SISTEMA_LOGGING_SILENCIOSO_CSV.md
    
    # Verificar si estamos en modo dashboard limpio (default)
    silent_mode = os.getenv('SENTINEL_SILENT_MODE', 'true').lower() == 'true'
    
    if not silent_mode:
        # Solo en modo debug: mostrar logs en terminal
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(log_format)
        # Configurar encoding UTF-8 para Windows
        if hasattr(console_handler.stream, 'reconfigure'):
            try:
                console_handler.stream.reconfigure(encoding='utf-8')  # type: ignore
            except:
                pass  # Si falla, continuar sin UTF-8
        root_logger.addHandler(console_handler)
    else:
        # Modo silencioso: Solo errores críticos en terminal
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.ERROR)  # Solo ERROR y CRITICAL
        console_handler.setFormatter(log_format)
        # Configurar encoding UTF-8 para Windows
        if hasattr(console_handler.stream, 'reconfigure'):
            try:
                console_handler.stream.reconfigure(encoding='utf-8')  # type: ignore
            except:
                pass  # Si falla, continuar sin UTF-8
        root_logger.addHandler(console_handler)

    # 4. Handler para el ARCHIVO GENERAL (logs de operación diaria)
    # Registra todo lo importante (INFO y superior) en un archivo diario.
    daily_log_path = log_dir / "daily" / "sentinel_runtime.log"
    daily_log_path.parent.mkdir(exist_ok=True)
    daily_handler = logging.handlers.TimedRotatingFileHandler(
        daily_log_path, when='midnight', interval=1, backupCount=30
    )
    daily_handler.setLevel(logging.INFO)
    daily_handler.setFormatter(log_format)
    root_logger.addHandler(daily_handler)

    # 5. Handler de DEBUG ("El log de la pulga")
    # Registra absolutamente TODO (nivel DEBUG) en un archivo separado que rota por tamaño.
    debug_log_path = log_dir / "debug" / "full_system_trace.log"
    debug_log_path.parent.mkdir(exist_ok=True)
    debug_handler = logging.handlers.RotatingFileHandler(
        debug_log_path, maxBytes=50*1024*1024, backupCount=10  # 50MB por archivo, 10 archivos
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(log_format)
    root_logger.addHandler(debug_handler)

    # 6. Handler de ERRORES CRÍTICOS
    # Un archivo separado que solo contiene WARNINGS, ERRORS y CRITICALS.
    error_log_path = log_dir / "errors" / "error.log"
    error_log_path.parent.mkdir(exist_ok=True)
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_path, maxBytes=10*1024*1024, backupCount=5
    )
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(log_format)
    root_logger.addHandler(error_handler)

    # 7. Handler especializado para TRADING (decisiones críticas)
    trading_log_path = log_dir / "trading" / "trading_decisions.log"
    trading_log_path.parent.mkdir(exist_ok=True)
    trading_handler = logging.handlers.TimedRotatingFileHandler(
        trading_log_path, when='midnight', interval=1, backupCount=90
    )
    trading_handler.setLevel(logging.INFO)
    trading_handler.setFormatter(log_format)
    
    # Crear logger específico para trading
    trading_logger = logging.getLogger('trading')
    trading_logger.addHandler(trading_handler)
    trading_logger.setLevel(logging.DEBUG)

    # 8. Handler especializado para ICT (análisis de patrones)
    ict_log_path = log_dir / "ict" / "ict_analysis.log"
    ict_log_path.parent.mkdir(exist_ok=True)
    ict_handler = logging.handlers.TimedRotatingFileHandler(
        ict_log_path, when='midnight', interval=1, backupCount=30
    )
    ict_handler.setLevel(logging.DEBUG)
    ict_handler.setFormatter(log_format)
    
    # Crear logger específico para ICT
    ict_logger = logging.getLogger('ict')
    ict_logger.addHandler(ict_handler)
    ict_logger.setLevel(logging.DEBUG)

    # 9. Handler especializado para POI (puntos de interés)
    poi_log_path = log_dir / "poi" / "poi_detection.log"
    poi_log_path.parent.mkdir(exist_ok=True)
    poi_handler = logging.handlers.TimedRotatingFileHandler(
        poi_log_path, when='midnight', interval=1, backupCount=30
    )
    poi_handler.setLevel(logging.DEBUG)
    poi_handler.setFormatter(log_format)
    
    # Crear logger específico para POI
    poi_logger = logging.getLogger('poi')
    poi_logger.addHandler(poi_handler)
    poi_logger.setLevel(logging.DEBUG)

    # 10. Handler especializado para MT5 (conexión y datos)
    mt5_log_path = log_dir / "mt5" / "mt5_operations.log"
    mt5_log_path.parent.mkdir(exist_ok=True)
    mt5_handler = logging.handlers.TimedRotatingFileHandler(
        mt5_log_path, when='midnight', interval=1, backupCount=30
    )
    mt5_handler.setLevel(logging.DEBUG)
    mt5_handler.setFormatter(log_format)
    
    # Crear logger específico para MT5
    mt5_logger = logging.getLogger('mt5')
    mt5_logger.addHandler(mt5_handler)
    mt5_logger.setLevel(logging.DEBUG)

    # 🚨 NUEVA CAJA NEGRA: Handler especializado para DASHBOARD DATA (FORENSE)
    # Registro detallado de cada paquete de datos recibido por el dashboard
    dashboard_data_log_path = log_dir / "dashboard" / "data_packets.log"
    dashboard_data_log_path.parent.mkdir(exist_ok=True)
    dashboard_data_handler = logging.handlers.TimedRotatingFileHandler(
        dashboard_data_log_path, when='midnight', interval=1, backupCount=60  # 60 días de historial
    )
    dashboard_data_handler.setLevel(logging.DEBUG)
    
    # Formato simplificado para análisis forense: TIMESTAMP | DATOS_JSON
    dashboard_data_format = logging.Formatter('%(asctime)s | %(message)s')
    dashboard_data_handler.setFormatter(dashboard_data_format)
    
    # Crear logger específico para la caja negra del dashboard
    dashboard_data_logger = logging.getLogger("dashboard_data")
    dashboard_data_logger.addHandler(dashboard_data_handler)
    dashboard_data_logger.setLevel(logging.DEBUG)
    dashboard_data_logger.propagate = False  # Evita que vayan al log general

    # 🌟 NUEVO: Handler para EVENTOS ESTRUCTURADOS (JSONL)
    # Registra eventos clave en formato JSON para análisis de máquinas
    structured_log_path = log_dir / "structured" / "events.jsonl"
    structured_log_path.parent.mkdir(exist_ok=True)
    structured_handler = logging.handlers.TimedRotatingFileHandler(
        structured_log_path, when='midnight', interval=1, backupCount=90
    )
    structured_handler.setLevel(logging.INFO)
    structured_handler.setFormatter(JsonFormatter(datefmt='%Y-%m-%d %H:%M:%S'))
    
    # Logger específico para eventos estructurados
    structured_logger = logging.getLogger("structured_events")
    structured_logger.addHandler(structured_handler)
    structured_logger.setLevel(logging.INFO)
    structured_logger.propagate = False

    # 🌟 NUEVO: Handler para MÉTRICAS DE CUENTA (CSV)
    # Series temporales de balance, equity, profit para análisis cuantitativo
    account_metrics_path = log_dir / "metrics" / "account_metrics.csv"
    account_metrics_path.parent.mkdir(exist_ok=True)
    account_handler = logging.handlers.TimedRotatingFileHandler(
        account_metrics_path, when='midnight', interval=1, backupCount=365  # 1 año de historial
    )
    account_handler.setLevel(logging.INFO)
    account_handler.setFormatter(CsvMetricsFormatter())
    
    # Logger específico para métricas de cuenta
    account_metrics_logger = logging.getLogger("account_metrics")
    account_metrics_logger.addHandler(account_handler)
    account_metrics_logger.setLevel(logging.INFO)
    account_metrics_logger.propagate = False
    
    # Escribir encabezado CSV si el archivo es nuevo
    if not account_metrics_path.exists() or account_metrics_path.stat().st_size == 0:
        account_metrics_logger.info("balance,equity,profit,margin,free_margin,positions_count")

    # 🌟 NUEVO: Handler para MÉTRICAS DE TRADING (CSV)
    # Series temporales de operaciones, P&L, drawdown
    trading_metrics_path = log_dir / "metrics" / "trading_metrics.csv"
    trading_metrics_path.parent.mkdir(exist_ok=True)
    trading_handler_csv = logging.handlers.TimedRotatingFileHandler(
        trading_metrics_path, when='midnight', interval=1, backupCount=365
    )
    trading_handler_csv.setLevel(logging.INFO)
    trading_handler_csv.setFormatter(CsvMetricsFormatter())
    
    # Logger específico para métricas de trading
    trading_metrics_logger = logging.getLogger("trading_metrics")
    trading_metrics_logger.addHandler(trading_handler_csv)
    trading_metrics_logger.setLevel(logging.INFO)
    trading_metrics_logger.propagate = False
    
    # Escribir encabezado CSV si el archivo es nuevo
    if not trading_metrics_path.exists() or trading_metrics_path.stat().st_size == 0:
        trading_metrics_logger.info("symbol,action,volume,price,profit,balance_after,equity_after")

    # 🌟 NUEVO: Handler para MÉTRICAS DE SISTEMA (CSV)
    # CPU, memoria, latencia, health checks
    system_metrics_path = log_dir / "metrics" / "system_metrics.csv"
    system_metrics_path.parent.mkdir(exist_ok=True)
    system_handler_csv = logging.handlers.TimedRotatingFileHandler(
        system_metrics_path, when='midnight', interval=1, backupCount=30
    )
    system_handler_csv.setLevel(logging.INFO)
    system_handler_csv.setFormatter(CsvMetricsFormatter())
    
    # Logger específico para métricas de sistema
    system_metrics_logger = logging.getLogger("system_metrics")
    system_metrics_logger.addHandler(system_handler_csv)
    system_metrics_logger.setLevel(logging.INFO)
    system_metrics_logger.propagate = False
    
    # Escribir encabezado CSV si el archivo es nuevo
    if not system_metrics_path.exists() or system_metrics_path.stat().st_size == 0:
        system_metrics_logger.info("cpu_percent,memory_percent,latency_ms,active_positions,mt5_connected,dashboard_connected")

    # Log inicial del sistema
    root_logger.info("=" * 80)
    root_logger.info(f"SENTINEL GRID SYSTEM - LOGGING ESTRUCTURADO INICIADO")
    root_logger.info(f"Timestamp: {datetime.now().isoformat()}")
    root_logger.info(f"Log Directory: {log_dir}")
    root_logger.info(f"Logging Estructurado: JSONL + CSV habilitado")
    root_logger.info("=" * 80)

def get_logger(name: Optional[str] = None):
    """
    Obtiene un logger configurado para un módulo específico.
    
    Args:
        name: Nombre del módulo. Si es None, usa el logger raíz.
    
    Returns:
        Logger configurado
    
    Ejemplo de uso:
        logger = get_logger(__name__)
        logger.info("Iniciando análisis ICT")
        logger.debug("Precio actual: 1.23456")
    """
    return logging.getLogger(name)

def get_specialized_logger(system: str):
    """
    Obtiene un logger especializado para un sistema específico.
    
    Args:
        system: 'trading', 'ict', 'poi', 'mt5', 'dashboard', 'sistema', 'general'
    
    Returns:
        Logger especializado
    
    Ejemplo:
        trading_logger = get_specialized_logger('trading')
        trading_logger.info("DECISIÓN: COMPRA EURUSD 0.01 lotes")
    """
    valid_systems = [
    'trading', 'ict', 'poi', 'mt5', 'dashboard', 'sistema', 'general', 'acc', 'tct',
    'analysis', 'startup', 'hibernation', 'widget', 'ui', 'experimental'
]
    if system not in valid_systems:
        raise ValueError(f"Sistema debe ser uno de: {valid_systems}")
    
    return logging.getLogger(system)

# Función de conveniencia para logs críticos de trading
def log_trading_decision(decision: str, price: float, symbol: str, details: Optional[Dict[str, Any]] = None):
    """
    Registra una decisión de trading de forma estandarizada.
    
    Args:
        decision: 'BUY', 'SELL', 'WAIT', 'CLOSE'
        price: Precio al que se toma la decisión
        symbol: Símbolo del instrumento
        details: Detalles adicionales de la decisión
    """
    trading_logger = get_specialized_logger('trading')
    details_str = f" | Detalles: {details}" if details else ""
    trading_logger.info("DECISIÓN: %s %s @ %s%s", decision, symbol, price, details_str)

def log_ict_pattern(pattern_type: str, confidence: float, timeframe: str, details: Optional[Dict[str, Any]] = None):
    """
    Registra detección de patrón ICT de forma estandarizada.
    
    Args:
        pattern_type: Tipo de patrón (FVG, ORDER_BLOCK, etc.)
        confidence: Nivel de confianza (0.0-1.0)
        timeframe: Marco temporal
        details: Detalles del patrón
    """
    ict_logger = get_specialized_logger('ict')
    details_str = f" | Detalles: {details}" if details else ""
    ict_logger.info(f"PATRÓN: {pattern_type} | Confianza: {confidence:.2f} | TF: {timeframe}{details_str}")

def log_poi_detection(poi_type: str, price: float, score: float, distance: Optional[float] = None):
    """
    Registra detección de POI de forma estandarizada.
    
    Args:
        poi_type: Tipo de POI
        price: Precio del POI
        score: Score del POI
        distance: Distancia al precio actual
    """
    poi_logger = get_specialized_logger('poi')
    distance_str = f" | Distancia: {distance:.5f}" if distance else ""
    poi_logger.info(f"POI: {poi_type} @ {price:.5f} | Score: {score:.2f}{distance_str}")

def log_mt5_operation(operation: str, success: bool, details: Optional[str] = None):
    """
    Registra operación de MT5 de forma estandarizada.
    
    Args:
        operation: Tipo de operación
        success: Si fue exitosa
        details: Detalles adicionales
    """
    mt5_logger = get_specialized_logger('mt5')
    status = "SUCCESS" if success else "FAILED"
    details_str = f" | {details}" if details else ""
    mt5_logger.info(f"MT5: {operation} | {status}{details_str}")

# =============================================================================
# 🌟 FUNCIONES DE LOGGING ESTRUCTURADO (NUEVO)
# =============================================================================

def log_structured_event(evento_tipo: str, datos: Dict[str, Any], emisor: str = "sistema", categoria: str = "general"):
    """
    Registra un evento en formato JSON estructurado para análisis de máquinas.
    
    Args:
        evento_tipo: Tipo de evento (poi_detected, pattern_found, trade_executed, etc.)
        datos: Diccionario con todos los datos del evento
        emisor: Módulo que genera el evento
        categoria: Categoría del evento
    """
    structured_logger = logging.getLogger("structured_events")
    
    # Enriquecer los datos con información del evento
    evento_completo = {
        "evento_tipo": evento_tipo,
        "datos": datos,
        "timestamp_unix": datetime.now().timestamp()
    }
    
    # Usar el sistema de extra para pasar metadatos al formateador
    structured_logger.info(
        f"Evento estructurado: {evento_tipo}",
        extra={
            'emisor': emisor,
            'categoria': categoria,
            'metadata': evento_completo
        }
    )

def log_account_metrics(balance: float, equity: float, profit: float, margin: float = 0.0, 
                       free_margin: float = 0.0, positions_count: int = 0):
    """
    Registra métricas de cuenta en formato CSV para análisis temporal.
    
    Args:
        balance: Balance actual
        equity: Equity actual
        profit: Profit/Loss actual
        margin: Margen usado
        free_margin: Margen libre
        positions_count: Número de posiciones abiertas
    """
    account_metrics_logger = logging.getLogger("account_metrics")
    account_metrics_logger.info(f"{balance},{equity},{profit},{margin},{free_margin},{positions_count}")

def log_trading_metrics(symbol: str, action: str, volume: float, price: float, 
                       profit: float, balance_after: float, equity_after: float):
    """
    Registra métricas de trading en formato CSV.
    
    Args:
        symbol: Símbolo del instrumento
        action: BUY/SELL/CLOSE
        volume: Volumen de la operación
        price: Precio de ejecución
        profit: Profit/Loss de la operación
        balance_after: Balance después de la operación
        equity_after: Equity después de la operación
    """
    trading_metrics_logger = logging.getLogger("trading_metrics")
    trading_metrics_logger.info(f"{symbol},{action},{volume},{price},{profit},{balance_after},{equity_after}")

def log_system_metrics(cpu_percent: float, memory_percent: float, latency_ms: float,
                      active_positions: int, mt5_connected: bool, dashboard_connected: bool):
    """
    Registra métricas del sistema en formato CSV.
    
    Args:
        cpu_percent: Porcentaje de CPU usado
        memory_percent: Porcentaje de memoria usado
        latency_ms: Latencia en millisegundos
        active_positions: Posiciones activas
        mt5_connected: Estado de conexión MT5
        dashboard_connected: Estado de conexión dashboard
    """
    system_metrics_logger = logging.getLogger("system_metrics")
    mt5_status = 1 if mt5_connected else 0
    dashboard_status = 1 if dashboard_connected else 0
    system_metrics_logger.info(f"{cpu_percent},{memory_percent},{latency_ms},{active_positions},{mt5_status},{dashboard_status}")

# =============================================================================
# 🎯 FUNCIONES DE CONVENIENCIA PARA EVENTOS ESTRUCTURADOS ESPECÍFICOS
# =============================================================================

def log_poi_structured(poi_data: Dict[str, Any]):
    """
    Registra detección de POI en formato estructurado.
    
    Args:
        poi_data: Diccionario completo del POI con todos sus campos
    """
    log_structured_event("poi_detected", poi_data, emisor="poi_detector", categoria="poi")

def log_pattern_structured(pattern_data: Dict[str, Any]):
    """
    Registra detección de patrón ICT en formato estructurado.
    
    Args:
        pattern_data: Diccionario completo del patrón con todos sus campos
    """
    log_structured_event("ict_pattern_detected", pattern_data, emisor="ict_analyzer", categoria="ict")

def log_trade_structured(trade_data: Dict[str, Any]):
    """
    Registra ejecución de trade en formato estructurado.
    
    Args:
        trade_data: Diccionario completo del trade con todos sus campos
    """
    log_structured_event("trade_executed", trade_data, emisor="trading_engine", categoria="trading")

def log_market_context_structured(context_data: Dict[str, Any]):
    """
    Registra cambio de contexto de mercado en formato estructurado.
    
    Args:
        context_data: Diccionario completo del contexto con todos sus campos
    """
    log_structured_event("market_context_updated", context_data, emisor="market_analyzer", categoria="market")
