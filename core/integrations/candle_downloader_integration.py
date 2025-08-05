#!/usr/bin/env python3
"""
🔗 CANDLE DOWNLOADER INTEGRATION - ICT ENGINE v5.0
==================================================

Módulo de integración entre AdvancedCandleDownloader, Dashboard y ICT Engine
Proporciona funciones de conveniencia para integración completa

Creado por Sprint 1.2 Executor
"""

from typing import Dict, List, Optional, Callable
import sys
from pathlib import Path

# Importaciones seguras - Sistema ICT Engine v5.0
try:
    from core.data_management.candle_coordinator import candle_coordinator
except ImportError:
    try:
        from sistema.logging_interface import enviar_senal_log
        enviar_senal_log("WARNING", "No se pudo importar candle_coordinator", __name__, "init")
    except ImportError:
        # TODO: Migrar a enviar_senal_log("WARNING", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("WARNING", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("WARNING", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("WARNING", mensaje, __name__, "sistema") # print("Warning: No se pudo importar candle_coordinator")
    candle_coordinator = None

try:
    from dashboard.candle_downloader_widget import CandleDownloaderWidget
    # Crear instancia global del widget para compatibilidad
    candle_downloader_widget = CandleDownloaderWidget()
except ImportError:
    try:
        from sistema.logging_interface import enviar_senal_log
        enviar_senal_log("WARNING", "No se pudo importar CandleDownloaderWidget", __name__, "init")
    except ImportError:
        # TODO: Migrar a enviar_senal_log("WARNING", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("WARNING", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("WARNING", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("WARNING", mensaje, __name__, "sistema") # print("Warning: No se pudo importar CandleDownloaderWidget")
    candle_downloader_widget = None

# Sistema de logging del ICT Engine
from sistema.logging_interface import enviar_senal_log

class CandleDownloaderIntegration:
    """
    🔗 INTEGRACIÓN COMPLETA DEL CANDLE DOWNLOADER

    Coordina entre:
    - AdvancedCandleDownloader (descarga real)
    - CandleCoordinator (orquestación)
    - CandleDownloaderWidget (UI)
    - Dashboard (visualización)
    - ICT Engine (consumo de datos)
    """

    def __init__(self):
        self.coordinator = candle_coordinator
        self.widget = candle_downloader_widget
        self.is_integrated = False

        # Adapters para callbacks (compatibilidad de firmas)
        self._progress_adapter = None
        self._completion_adapter = None
        self._error_adapter = None

    def _create_callback_adapters(self):
        """Crea adaptadores para compatibilidad de callbacks"""
        if not self.widget:
            return

        # Adapter para progress callback
        def progress_adapter(request_id: str, progress: float):
            # Extraer symbol y timeframe del request_id
            parts = request_id.split('_')
            if len(parts) >= 2:
                symbol, timeframe = parts[0], parts[1]
                self.widget.on_progress_update(
                    symbol, timeframe, "downloading",
                    progress=progress, request_id=request_id
                )

        # Adapter para completion callback
        def completion_adapter(request_id: str, success: bool):
            parts = request_id.split('_')
            if len(parts) >= 2:
                symbol, timeframe = parts[0], parts[1]
                stats = {'success': success, 'request_id': request_id}
                self.widget.on_download_completed(symbol, timeframe, stats)

        # Adapter para error callback
        def error_adapter(request_id: str, error: Exception):
            parts = request_id.split('_')
            if len(parts) >= 2:
                symbol, timeframe = parts[0], parts[1]
                self.widget.on_download_error(symbol, timeframe, str(error))

        self._progress_adapter = progress_adapter
        self._completion_adapter = completion_adapter
        self._error_adapter = error_adapter

    def setup_integration(self) -> bool:
        """Configura integración completa"""
        try:
            if not self.coordinator or not self.widget:
                enviar_senal_log("ERROR", "Componentes no disponibles para integración", "candle_integration")
                return False

            # Crear adaptadores de callbacks
            self._create_callback_adapters()

            # Conectar callbacks adaptados del coordinador con el widget
            if self._progress_adapter:
                self.coordinator.set_progress_callback(self._progress_adapter)
            if self._completion_adapter:
                self.coordinator.set_completion_callback(self._completion_adapter)
            if self._error_adapter:
                self.coordinator.set_error_callback(self._error_adapter)

            # Iniciar coordinador
            if self.coordinator.start_coordinator():
                self.is_integrated = True
                enviar_senal_log("SUCCESS", "Integración configurada correctamente", "candle_integration")
                return True
            return False

        except Exception as e:
            enviar_senal_log("ERROR", f"Error en setup_integration: {e}", "candle_integration")
            return False

    def start_download_session(self, symbols: Optional[List[str]] = None,
                             timeframes: Optional[List[str]] = None,
                             lookback: int = 50000) -> bool:
        """Inicia sesión de descarga completa"""
        if not self.is_integrated:
            if not self.setup_integration():
                return False

        # Usar valores por defecto si no se especifican
        symbols = symbols or ["EURUSD"]
        timeframes = timeframes or ["H4", "H1", "M15", "M5"]

        try:
            # Configurar widget
            if self.widget:
                self.widget.configure_symbols(symbols)
                self.widget.configure_timeframes(timeframes)
                self.widget.configure_lookback(lookback)
                self.widget.start_download()

            # Iniciar descarga coordinada
            if self.coordinator:
                downloads_queued = 0
                for symbol in symbols:
                    for timeframe in timeframes:
                        request_id = self.coordinator.queue_download(symbol, timeframe, lookback)
                        if request_id:
                            downloads_queued += 1

                enviar_senal_log("INFO",
                    f"Sesión de descarga iniciada: {downloads_queued} descargas encoladas",
                    "candle_integration")

            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"Error iniciando descarga: {e}", "candle_integration")
            return False

    def stop_download_session(self):
        """Detiene sesión de descarga"""
        try:
            if self.widget:
                self.widget.stop_download()
            enviar_senal_log("INFO", "Sesión de descarga detenida", "candle_integration")
        except Exception as e:
            enviar_senal_log("ERROR", f"Error deteniendo descarga: {e}", "candle_integration")
        # El coordinador sigue corriendo en background

    def download_for_ict_analysis(self, symbol: str = "EURUSD") -> bool:
        """Descarga datos específicamente para análisis ICT"""
        # Timeframes prioritarios para ICT
        ict_timeframes = ["H4", "H1", "M15", "M5"]

        return self.start_download_session([symbol], ict_timeframes, 100000)

    def auto_update_stale_data(self, max_age_hours: int = 24) -> int:
        """Auto-actualiza datos obsoletos"""
        if not self.is_integrated:
            self.setup_integration()

        if not self.widget or not self.coordinator:
            return 0

        symbols = self.widget.selected_symbols
        timeframes = self.widget.selected_timeframes

        return self.coordinator.auto_update_stale_data(symbols, timeframes, max_age_hours)

    def get_integration_status(self) -> Dict:
        """Obtiene estado de la integración"""
        coordinator_status = self.coordinator.get_status() if self.coordinator else {}
        widget_stats = self.widget.download_stats if self.widget else {}

        return {
            'is_integrated': self.is_integrated,
            'coordinator_status': coordinator_status,
            'widget_downloading': self.widget.is_downloading if self.widget else False,
            'widget_stats': widget_stats
        }

    def trigger_emergency_download(self, symbol: str, timeframe: str) -> bool:
        """Descarga de emergencia (inmediata)"""
        if not self.is_integrated:
            self.setup_integration()

        if not self.coordinator:
            return False

        return self.coordinator.download_immediate(symbol, timeframe, 50000)

# Instancia global para usar desde cualquier parte del sistema
downloader_integration = CandleDownloaderIntegration()

# Funciones de conveniencia
def start_download(symbols: Optional[List[str]] = None, timeframes: Optional[List[str]] = None) -> bool:
    """Función de conveniencia para iniciar descarga"""
    return downloader_integration.start_download_session(symbols, timeframes)

def stop_download():
    """Función de conveniencia para detener descarga"""
    downloader_integration.stop_download_session()

def download_for_trading(symbol: str = "EURUSD") -> bool:
    """Función de conveniencia para descarga de trading"""
    return downloader_integration.download_for_ict_analysis(symbol)

def get_downloader_status() -> Dict:
    """Función de conveniencia para obtener estado"""
    return downloader_integration.get_integration_status()
