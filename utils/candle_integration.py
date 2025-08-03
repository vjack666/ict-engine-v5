#!/usr/bin/env python3
"""
🔗 SIMPLE INTEGRATION FUNCTIONS - ICT ENGINE v5.0
=================================================

Funciones simples para integración sin capas innecesarias
Usa directamente AdvancedCandleDownloader mejorado

Creado por Sprint 1.2 Refactored
"""

from typing import List, Dict, Optional, Callable

# Imports seguros
try:
    from utils.advanced_candle_downloader import AdvancedCandleDownloader
except ImportError:
    print("Warning: No se pudo importar AdvancedCandleDownloader")
    AdvancedCandleDownloader = None

try:
    from dashboard.simple_candle_widget import simple_candle_widget
except ImportError:
    print("Warning: No se pudo importar simple_candle_widget")
    simple_candle_widget = None

# Instancia global del downloader
_global_downloader: Optional[AdvancedCandleDownloader] = None

def get_downloader() -> Optional[AdvancedCandleDownloader]:
    """Obtiene instancia global del downloader"""
    global _global_downloader
    
    if _global_downloader is None and AdvancedCandleDownloader:
        _global_downloader = AdvancedCandleDownloader()
        
        # Configurar callbacks con el widget si está disponible
        if simple_candle_widget and _global_downloader:
            _global_downloader.set_progress_callback(simple_candle_widget.on_progress)
            _global_downloader.set_completion_callback(simple_candle_widget.on_completion)
            _global_downloader.set_error_callback(simple_candle_widget.on_error)
    
    return _global_downloader

# === FUNCIONES DE CONVENIENCIA ===

def download_for_ict(symbol: str = "EURUSD", lookback: int = 100000) -> bool:
    """Descarga datos específicamente para análisis ICT"""
    downloader = get_downloader()
    if not downloader:
        return False
    
    # Timeframes prioritarios para ICT
    ict_timeframes = ["H4", "H1", "M15", "M5"]
    
    try:
        stats_list = downloader.download_with_coordination([symbol], ict_timeframes, lookback)
        successful = len([s for s in stats_list if s.success])
        return successful > 0
    except Exception:
        return False

def download_quick(symbol: str = "EURUSD", timeframe: str = "H4", lookback: int = 50000) -> bool:
    """Descarga rápida de un símbolo/timeframe"""
    downloader = get_downloader()
    if not downloader:
        return False
    
    try:
        stats = downloader.download_symbol_timeframe(symbol, timeframe, lookback)
        return stats.success
    except Exception:
        return False

def update_stale_data(symbols: List[str] = None, timeframes: List[str] = None, 
                     max_age_hours: int = 24) -> int:
    """Actualiza datos obsoletos"""
    downloader = get_downloader()
    if not downloader:
        return 0
    
    symbols = symbols or ["EURUSD"]
    timeframes = timeframes or ["H4", "H1", "M15", "M5"]
    
    try:
        return downloader.auto_update_stale_data(symbols, timeframes, max_age_hours)
    except Exception:
        return 0

def queue_download(symbol: str, timeframe: str, lookback: int = 50000) -> int:
    """Añade descarga a cola"""
    downloader = get_downloader()
    if not downloader:
        return 0
    
    try:
        return downloader.queue_download(symbol, timeframe, lookback)
    except Exception:
        return 0

def process_download_queue() -> bool:
    """Procesa toda la cola de descargas"""
    downloader = get_downloader()
    if not downloader:
        return False
    
    try:
        stats_list = downloader.process_download_queue()
        successful = len([s for s in stats_list if s.success])
        return successful > 0
    except Exception:
        return False

def get_download_status() -> Dict:
    """Obtiene estado del sistema de descarga"""
    downloader = get_downloader()
    if not downloader:
        return {
            'is_connected': False,
            'error': 'Downloader no disponible'
        }
    
    try:
        return downloader.get_enhanced_status()
    except Exception:
        return {
            'is_connected': False,
            'error': 'No se pudo obtener estado'
        }

def connect_to_mt5() -> bool:
    """Conecta a MT5"""
    downloader = get_downloader()
    if not downloader:
        return False
    
    try:
        return downloader.connect_mt5()
    except Exception:
        return False

def disconnect_from_mt5():
    """Desconecta de MT5"""
    downloader = get_downloader()
    if not downloader:
        return
    
    try:
        downloader.disconnect_mt5()
    except Exception:
        pass

# === FUNCIONES PARA DASHBOARD ===

def setup_dashboard_integration():
    """Configura integración con dashboard"""
    # Ya está configurado automáticamente via get_downloader()
    return True

def start_widget_session(symbols: List[str] = None, timeframes: List[str] = None) -> bool:
    """Inicia sesión desde widget"""
    if not simple_candle_widget:
        return False
        
    if symbols:
        simple_candle_widget.configure(symbols=symbols)
    if timeframes:
        simple_candle_widget.configure(timeframes=timeframes)
    
    return simple_candle_widget.start_download_session()

# === FUNCIONES PARA ICT ENGINE ===

def ensure_data_for_analysis(symbol: str = "EURUSD") -> bool:
    """Asegura que hay datos para análisis ICT"""
    downloader = get_downloader()
    if not downloader:
        return False
    
    # Verificar datos existentes
    required_timeframes = ["H4", "H1", "M15", "M5"]
    missing_data = []
    
    for tf in required_timeframes:
        if not downloader._check_data_freshness(symbol, tf, 6):  # 6 horas max
            missing_data.append(tf)
    
    if missing_data:
        # Descargar datos faltantes
        try:
            stats_list = downloader.download_with_coordination([symbol], missing_data, 50000)
            successful = len([s for s in stats_list if s.success])
            return successful == len(missing_data)
        except Exception:
            return False
    
    return True  # Todos los datos están frescos

def trigger_emergency_download(symbol: str, timeframe: str) -> bool:
    """Descarga de emergencia inmediata"""
    downloader = get_downloader()
    if not downloader:
        return False
    
    try:
        stats = downloader.download_symbol_timeframe(symbol, timeframe, 10000)
        return stats.success
    except Exception:
        return False
