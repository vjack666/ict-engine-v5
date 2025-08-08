#!/usr/bin/env python3
"""
📊 LOGGING UTILS - Utilidades de logging para sistema Sentinel
"""

# MIGRACIÓN SIC v3.0 + SLUC v2.1
from sistema.sic import enviar_senal_log, log_info, log_warning

import csv
from sistema.sic import json
from json import JSONDecodeError
from sistema.sic import datetime
from sistema.sic import Path
from sistema.sic import Any, Dict, List, Optional
from rich.text import Text

# MIGRADO A SLUC v2.0
try:
    from sistema.sic import enviar_senal_log
except ImportError:
    def enviar_senal_log(*args, **kwargs):
        """Fallback para logging_interface no disponible"""
        pass

# Variables globales para logs del terminal
terminal_logs: List[Text] = []
MAX_TERMINAL_LOGS = 100

def save_adaptive_debug_to_csv(data: Any, filename: Optional[str] = None, directory: str = "../data/logs/debug") -> bool:
    """
    Guarda datos de debug adaptativos en CSV
    """
    try:
        # Crear directorio si no existe
        log_dir = Path(directory)
        log_dir.mkdir(parents=True, exist_ok=True)

        # Generar nombre de archivo si no se proporciona
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"debug_data_{timestamp}.csv"

        filepath = log_dir / filename

        # Convertir datos a formato CSV si es necesario
        if isinstance(data, dict):
            # Convertir dict a lista de filas
            rows = []
            for key, value in data.items():
                rows.append({"key": key, "value": str(value), "timestamp": datetime.now().isoformat()})
            data = rows
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            # Ya es lista de diccionarios
            pass
        else:
            # Convertir otros tipos a formato simple
            data = [{"data": str(data), "timestamp": datetime.now().isoformat()}]

        # Escribir CSV
        if data:
            fieldnames = data[0].keys()
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

        return True

    except (JSONDecodeError, ValueError) as e:
        enviar_senal_log("ERROR", f"Error guardando debug CSV: {e}", "logging_utils", "migration")
        return False

def log_critical_error(error_message: str) -> bool:
    """
    Log de errores críticos - CORREGIDO para aceptar solo 1 argumento
    """
    try:
        # Crear directorio de logs críticos
        log_dir = Path("../data/logs/critical")
        log_dir.mkdir(parents=True, exist_ok=True)

        # Preparar datos del error
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "error": error_message,
            "level": "CRITICAL"
        }

        # Guardar en JSON
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = log_dir / f"critical_errors_{timestamp}.json"

        # Leer errores existentes si el archivo existe
        existing_errors = []
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    existing_errors = json.load(f)
            except (FileNotFoundError, JSONDecodeError, UnicodeDecodeError):
                existing_errors = []

        # Agregar nuevo error
        existing_errors.append(error_data)

        # Guardar todos los errores
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(existing_errors, f, indent=2, ensure_ascii=False)

        enviar_senal_log("ERROR", f"❌ ERROR CRÍTICO REGISTRADO: {error_message}", "logging_utils", "migration")
        return True

    except (JSONDecodeError, ValueError) as e:
        enviar_senal_log("ERROR", f"Error registrando error crítico: {e}", "logging_utils", "migration")
        return False

def save_poi_analysis_log(pois: List[Dict], filename: Optional[str] = None) -> bool:
    """
    Guarda logs de análisis POI
    """
    try:
        if not pois:
            return True

        log_dir = Path("../data/logs/poi")
        log_dir.mkdir(parents=True, exist_ok=True)

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"poi_analysis_{timestamp}.json"

        filepath = log_dir / filename

        log_data = {
            "timestamp": datetime.now().isoformat(),
            "total_pois": len(pois),
            "pois": pois
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

        return True

    except (JSONDecodeError, ValueError) as e:
        enviar_senal_log("ERROR", f"Error guardando log POI: {e}", "logging_utils", "migration")
        return False

def get_latest_debug_logs(log_type: str = "debug", limit: int = 10) -> List[Dict]:
    """
    Obtiene los últimos logs de debug
    """
    try:
        log_dir = Path(f"../../data/logs/{log_type}")
        if not log_dir.exists():
            return []

        # Buscar archivos de log más recientes
        log_files = sorted(log_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)

        all_logs = []
        for log_file in log_files[:limit]:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_logs.extend(data[-limit:])
                    else:
                        all_logs.append(data)
            except (FileNotFoundError, JSONDecodeError, UnicodeDecodeError):
                continue

        return all_logs[:limit]

    except (JSONDecodeError, ValueError) as e:
        enviar_senal_log("ERROR", f"Error obteniendo logs: {e}", "logging_utils", "migration")
        return []


# =============================================================================
# FUNCIONES DE ACCESO A ESTADO GLOBAL - TERMINAL LOGS
# =============================================================================

def get_terminal_logs() -> List[Text]:
    """Devuelve la lista actual de logs del terminal"""
    return terminal_logs


def clear_terminal_logs():
    """Limpia el buffer de logs del terminal"""
    terminal_logs.clear()


def get_max_terminal_logs() -> int:
    """Devuelve el máximo número de logs a mantener"""
    return MAX_TERMINAL_LOGS


def set_max_terminal_logs(max_logs: int):
    """Establece el máximo número de logs a mantener"""
    # Note: MAX_TERMINAL_LOGS es una constante módulo, no se modifica en runtime
    pass  # Funcionalidad deshabilitada para evitar modificación de constante


# =============================================================================
# FUNCIONES DE LOGGING ESTRUCTURADO PARA ANÁLISIS
# =============================================================================

def json_serializer(obj):
    """Serializador JSON personalizado para manejar tipos no serializables"""
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif hasattr(obj, 'tolist'):
        return obj.tolist()
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    return str(obj)


def save_analysis_log_to_json(component_name: str, analysis_data: Dict) -> None:
    """
    Sistema de logging inteligente universal para TODOS los componentes.

    Componentes soportados:
    - poi_analysis, pois_detection, poi_multi_analysis (POI)
    - m15_dual_structure, h4_bias_analysis (ICT)
    - fractal_analysis (Fractales)
    - version_analysis (Sistema)
    - dashboard_analytics (Dashboard)
    - Cualquier componente futuro

    Args:
        component_name: Tipo de análisis/componente
        analysis_data: Datos del análisis
    """
    try:
        # Importar el sistema universal inteligente
        from sistema.sic import sys
        import importlib.util

        # Calcular la ruta al archivo universal_intelligent_logger.py
        current_file = Path(__file__)  # logging_utils.py
        sentinel_utils = current_file.parent  # SENTINEL_GRID_SYSTEM/utils/
        sentinel_root = sentinel_utils.parent  # SENTINEL_GRID_SYSTEM/
        project_root = sentinel_root.parent  # Directorio raíz del proyecto
        logger_file = project_root / 'utils' / 'universal_intelligent_logger.py'

        # Importar el módulo dinámicamente
        if logger_file.exists():
            spec = importlib.util.spec_from_file_location("universal_intelligent_logger", logger_file)
            if spec and spec.loader:
                logger_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(logger_module)
                universal_logger = logger_module.universal_logger
            else:
                raise ImportError("No se pudo cargar el spec del módulo")
        else:
            raise ImportError(f"Archivo no encontrado: {logger_file}")

        # Mapear nombres de componentes a tipos de análisis
        component_mapping = {
            'poi_analysis': 'poi',
            'pois_detection': 'poi',
            'poi_multi_analysis': 'poi',
            'm15_dual_structure': 'm15_structure',
            'h4_bias_analysis': 'h4_bias',
            'fractal_analysis': 'fractal',
            'version_analysis': 'version',
            'dashboard_analytics': 'dashboard',
            'ict_analysis': 'ict',
            'institutional_analysis': 'ict'
        }

        analysis_type = component_mapping.get(component_name, component_name)

        logged = universal_# Removido - usar enviar_senal_log

        if logged:
            enviar_senal_log("INFO", f"📊 {component_name}: Cambio significativo logueado", "logging_utils", "migration")
        # No mostrar mensaje para logs omitidos para evitar spam

    except (JSONDecodeError, ValueError) as e:
        enviar_senal_log("ERROR", f"⚠️ Error en logging inteligente {component_name}: {e}", "logging_utils", "migration")
        # Fallback al sistema tradicional solo en caso de error crítico
        _fallback_traditional_logging(component_name, analysis_data)

def _fallback_traditional_logging(component_name: str, analysis_data: Dict) -> None:
    """Sistema de fallback tradicional solo para emergencias"""
    try:

        # Crear directorio de logs si no existe
        logs_dir = Path(__file__).parent.parent / 'data' / 'logs' / 'analysis'
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Nombre del archivo basado en la fecha
        date_str = datetime.now().strftime('%Y%m%d')
        log_file = logs_dir / f"{component_name}_{date_str}_fallback.json"

        # Log de emergencia simplificado
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'component': component_name,
            'data': analysis_data,
            'note': 'Fallback logging - Sistema inteligente falló'
        }

        # Escribir solo la entrada actual (sin acumular)
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_entry, f, indent=2, ensure_ascii=False, default=json_serializer)

        enviar_senal_log("INFO", f"⚠️ Fallback logging para {component_name}", "logging_utils", "migration")

    except (JSONDecodeError, ValueError) as fallback_error:
        enviar_senal_log("ERROR", f"❌ Error crítico en fallback logging {component_name}: {fallback_error}", "logging_utils", "migration")

# =============================================================================
# FUNCIONES DE TRADING LOGGING (migradas desde important_logging)
# =============================================================================

def log_trading_event(action: str, symbol: str, price: float, volume: float, order_type: str = "") -> bool:
    """Log de eventos de trading estandarizado"""
    try:
        from sistema.sic import log_info
        log_trading("INFO", f"TRADING_EVENT: {action} {symbol} @ {price} | Volume: {volume} | Type: {order_type}", "logging_utils")
        return True
    except (JSONDecodeError, ValueError, ImportError) as e:
        enviar_senal_log("ERROR", f"Error en log_trading_event: {e}", "logging_utils", "migration")
        return False

def log_order_filled(order_type: str, symbol: str, price: float, volume: float):
    """Log cuando una orden es ejecutada exitosamente"""
    try:
        from sistema.sic import log_info
        log_trading("INFO", f"ORDER_FILLED: {order_type} {symbol} @ {price} | Volume: {volume}", "logging_utils")
        return True
    except (JSONDecodeError, ValueError, ImportError) as e:
        enviar_senal_log("ERROR", f"Error en log_order_filled: {e}", "logging_utils", "migration")
        return False

def log_order_rejected(order_type: str, symbol: str, reason: str):
    """Log cuando una orden es rechazada"""
    try:
        from sistema.sic import log_info
        log_trading("WARNING", f"ORDER_REJECTED: {order_type} {symbol} | Reason: {reason}", "logging_utils")
        return True
    except (JSONDecodeError, ValueError, ImportError) as e:
        enviar_senal_log("ERROR", f"Error en log_order_rejected: {e}", "logging_utils", "migration")
        return False
