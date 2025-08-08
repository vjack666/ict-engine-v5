#!/usr/bin/env python3
"""
🕯️ CANDLE COORDINATOR - ICT ENGINE v5.0
=========================================

Coordinador central para descargas de velas y gestión de datos de mercado.
Integra con el sistema existente de controladores y proporciona las funciones
que requiere el CandleDownloaderIntegration.

Basado en la arquitectura existente del sistema:
- AccFlowController para gestión de colas
- DashboardController para callbacks
- MT5DataManager para descargas

Creado por: Sistema de Integración v5.0
"""

import asyncio
import threading
import queue
from sistema.sic import Dict, List, Optional, Callable, Any
from sistema.sic import datetime, timedelta
from sistema.sic import dataclass, field
from enum import Enum
from sistema.sic import time
# Importaciones del sistema existente
from sistema.sic import enviar_senal_log
from utils.mt5_data_manager import get_mt5_manager
from core.analysis_command_center.acc_flow_controller import AccFlowController, FlowPriority

class DownloadStatus(Enum):
    """Estados de descarga"""
    PENDING = "PENDING"
    DOWNLOADING = "DOWNLOADING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

@dataclass
class DownloadRequest:
    """Solicitud de descarga de velas"""
    symbol: str
    timeframe: str
    lookback: int
    priority: FlowPriority = FlowPriority.NORMAL
    request_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    status: DownloadStatus = DownloadStatus.PENDING
    progress: float = 0.0
    error_message: str = ""

class CandleCoordinator:
    """
    🕯️ COORDINADOR CENTRAL DE VELAS

    Proporciona las funciones que requiere CandleDownloaderIntegration:
    - set_progress_callback
    - set_completion_callback
    - set_error_callback
    - queue_download
    - start_coordinator

    Integra con la arquitectura existente del sistema.
    """

    def __init__(self):
        self.is_running = False
        self.mt5_manager = None

        # Callbacks del sistema
        self.progress_callbacks: List[Callable[[str, float], None]] = []
        self.completion_callbacks: List[Callable[[str, bool], None]] = []
        self.error_callbacks: List[Callable[[str, Exception], None]] = []

        # Sistema de colas basado en AccFlowController
        self.download_queue = queue.PriorityQueue()
        self.active_downloads: Dict[str, DownloadRequest] = {}
        self.completed_downloads: Dict[str, DownloadRequest] = {}

        # Control de threading
        self.worker_thread = None
        self.stop_event = threading.Event()

        # Estadísticas
        self.stats = {
            'total_downloads': 0,
            'successful_downloads': 0,
            'failed_downloads': 0,
            'bytes_downloaded': 0
        }

        enviar_senal_log("INFO", "CandleCoordinator inicializado", "candle_coordinator")

    def set_progress_callback(self, callback: Callable[[str, float], None]) -> None:
        """
        Establece callback para actualizaciones de progreso

        Args:
            callback: Función que recibe (request_id, progress 0.0-1.0)
        """
        if callback and callable(callback):
            self.progress_callbacks.append(callback)
            enviar_senal_log("DEBUG", f"Progress callback registrado: {callback.__name__}", "candle_coordinator")

    def set_completion_callback(self, callback: Callable[[str, bool], None]) -> None:
        """
        Establece callback para completación de descargas

        Args:
            callback: Función que recibe (request_id, success)
        """
        if callback and callable(callback):
            self.completion_callbacks.append(callback)
            enviar_senal_log("DEBUG", f"Completion callback registrado: {callback.__name__}", "candle_coordinator")

    def set_error_callback(self, callback: Callable[[str, Exception], None]) -> None:
        """
        Establece callback para errores de descarga

        Args:
            callback: Función que recibe (request_id, exception)
        """
        if callback and callable(callback):
            self.error_callbacks.append(callback)
            enviar_senal_log("DEBUG", f"Error callback registrado: {callback.__name__}", "candle_coordinator")

    def start_coordinator(self) -> bool:
        """
        Inicia el coordinador de descargas

        Returns:
            bool: True si se inició correctamente
        """
        if self.is_running:
            enviar_senal_log("WARNING", "CandleCoordinator ya está ejecutándose", "candle_coordinator")
            return True

        try:
            # Inicializar MT5 Manager
            self.mt5_manager = get_mt5_manager()
            if not self.mt5_manager:
                enviar_senal_log("ERROR", "No se pudo inicializar MT5Manager", "candle_coordinator")
                return False

            # Iniciar worker thread
            self.stop_event.clear()
            self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
            self.worker_thread.start()

            self.is_running = True
            enviar_senal_log("INFO", "CandleCoordinator iniciado correctamente", "candle_coordinator")
            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"Error iniciando CandleCoordinator: {e}", "candle_coordinator")
            return False

    def stop_coordinator(self) -> None:
        """Detiene el coordinador de descargas"""
        if not self.is_running:
            return

        enviar_senal_log("INFO", "Deteniendo CandleCoordinator...", "candle_coordinator")
        self.stop_event.set()

        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=5.0)

        self.is_running = False
        enviar_senal_log("INFO", "CandleCoordinator detenido", "candle_coordinator")

    def queue_download(self, symbol: str, timeframe: str, lookback: int = 50000,
                      priority: FlowPriority = FlowPriority.NORMAL) -> str:
        """
        Encola una descarga de velas

        Args:
            symbol: Símbolo a descargar (ej: "EURUSD")
            timeframe: Marco temporal (ej: "H1", "M15")
            lookback: Cantidad de velas a descargar
            priority: Prioridad de la descarga

        Returns:
            str: ID único de la solicitud
        """
        # Generar ID único
        request_id = f"{symbol}_{timeframe}_{int(time.time() * 1000)}"

        # Crear solicitud
        request = DownloadRequest(
            symbol=symbol,
            timeframe=timeframe,
            lookback=lookback,
            priority=priority,
            request_id=request_id
        )

        # Asignar prioridad numérica para la cola
        priority_value = self._get_priority_value(priority)

        try:
            self.download_queue.put((priority_value, request))
            self.stats['total_downloads'] += 1

            enviar_senal_log("INFO",
                f"Descarga encolada: {symbol} {timeframe} (ID: {request_id})",
                "candle_coordinator")

            return request_id

        except Exception as e:
            enviar_senal_log("ERROR", f"Error encolando descarga: {e}", "candle_coordinator")
            return ""

    def download_immediate(self, symbol: str, timeframe: str, lookback: int = 50000) -> bool:
        """
        Descarga inmediata (sin cola)

        Args:
            symbol: Símbolo a descargar
            timeframe: Marco temporal
            lookback: Cantidad de velas

        Returns:
            bool: True si la descarga fue exitosa
        """
        if not self.mt5_manager:
            enviar_senal_log("ERROR", "MT5Manager no disponible para descarga inmediata", "candle_coordinator")
            return False

        request_id = f"immediate_{symbol}_{timeframe}_{int(time.time())}"

        try:
            enviar_senal_log("INFO", f"Descarga inmediata: {symbol} {timeframe}", "candle_coordinator")

            # Notificar inicio
            self._notify_progress(request_id, 0.1)

            # Realizar descarga
            df = self.mt5_manager.get_historical_data(symbol, timeframe, lookback, force_download=True)

            if df is not None and not df.empty:
                self._notify_progress(request_id, 1.0)
                self._notify_completion(request_id, True)
                self.stats['successful_downloads'] += 1

                enviar_senal_log("SUCCESS",
                    f"Descarga inmediata exitosa: {symbol} {timeframe} ({len(df)} velas)",
                    "candle_coordinator")
                return True
            else:
                raise Exception(f"No se pudieron obtener datos para {symbol} {timeframe}")

        except Exception as e:
            self._notify_error(request_id, e)
            self.stats['failed_downloads'] += 1
            enviar_senal_log("ERROR", f"Error en descarga inmediata: {e}", "candle_coordinator")
            return False

    def auto_update_stale_data(self, symbols: List[str], timeframes: List[str],
                              max_age_hours: int = 24) -> int:
        """
        Auto-actualiza datos obsoletos

        Args:
            symbols: Lista de símbolos
            timeframes: Lista de marcos temporales
            max_age_hours: Edad máxima en horas

        Returns:
            int: Número de descargas encoladas
        """
        downloads_queued = 0

        for symbol in symbols:
            for timeframe in timeframes:
                # TODO: Implementar lógica de verificación de edad de datos
                # Por ahora, encolar todas las combinaciones
                request_id = self.queue_download(symbol, timeframe, priority=FlowPriority.LOW)
                if request_id:
                    downloads_queued += 1

        enviar_senal_log("INFO",
            f"Auto-actualización: {downloads_queued} descargas encoladas",
            "candle_coordinator")

        return downloads_queued

    def get_status(self) -> Dict[str, Any]:
        """
        Obtiene estado del coordinador

        Returns:
            Dict con estado completo
        """
        return {
            'is_running': self.is_running,
            'queue_size': self.download_queue.qsize(),
            'active_downloads': len(self.active_downloads),
            'stats': self.stats.copy(),
            'callbacks_registered': {
                'progress': len(self.progress_callbacks),
                'completion': len(self.completion_callbacks),
                'error': len(self.error_callbacks)
            }
        }

    def _worker_loop(self) -> None:
        """Loop principal del worker thread"""
        enviar_senal_log("INFO", "Worker thread iniciado", "candle_coordinator")

        while not self.stop_event.is_set():
            try:
                # Obtener siguiente descarga (timeout de 1 segundo)
                try:
                    priority, request = self.download_queue.get(timeout=1.0)
                except queue.Empty:
                    continue

                # Procesar descarga
                self._process_download(request)
                self.download_queue.task_done()

            except Exception as e:
                enviar_senal_log("ERROR", f"Error en worker loop: {e}", "candle_coordinator")

        enviar_senal_log("INFO", "Worker thread terminado", "candle_coordinator")

    def _process_download(self, request: DownloadRequest) -> None:
        """
        Procesa una descarga individual

        Args:
            request: Solicitud de descarga
        """
        request_id = request.request_id

        try:
            # Marcar como activa
            request.status = DownloadStatus.DOWNLOADING
            self.active_downloads[request_id] = request

            enviar_senal_log("INFO",
                f"Procesando descarga: {request.symbol} {request.timeframe}",
                "candle_coordinator")

            # Notificar inicio
            self._notify_progress(request_id, 0.1)

            # Realizar descarga
            df = self.mt5_manager.get_historical_data(
                request.symbol,
                request.timeframe,
                request.lookback,
                force_download=True
            )

            # Actualizar progreso
            self._notify_progress(request_id, 0.8)

            if df is not None and not df.empty:
                # Descarga exitosa
                request.status = DownloadStatus.COMPLETED
                request.progress = 1.0

                self._notify_progress(request_id, 1.0)
                self._notify_completion(request_id, True)
                self.stats['successful_downloads'] += 1
                self.stats['bytes_downloaded'] += len(df) * 100  # Estimación

                enviar_senal_log("SUCCESS",
                    f"Descarga completada: {request.symbol} {request.timeframe} ({len(df)} velas)",
                    "candle_coordinator")
            else:
                raise Exception(f"No se pudieron obtener datos para {request.symbol} {request.timeframe}")

        except Exception as e:
            # Descarga fallida
            request.status = DownloadStatus.FAILED
            request.error_message = str(e)

            self._notify_error(request_id, e)
            self._notify_completion(request_id, False)
            self.stats['failed_downloads'] += 1

            enviar_senal_log("ERROR", f"Error en descarga: {e}", "candle_coordinator")

        finally:
            # Mover a completadas
            if request_id in self.active_downloads:
                del self.active_downloads[request_id]
            self.completed_downloads[request_id] = request

    def _notify_progress(self, request_id: str, progress: float) -> None:
        """Notifica progreso a todos los callbacks"""
        for callback in self.progress_callbacks:
            try:
                callback(request_id, progress)
            except Exception as e:
                enviar_senal_log("ERROR", f"Error en progress callback: {e}", "candle_coordinator")

    def _notify_completion(self, request_id: str, success: bool) -> None:
        """Notifica completación a todos los callbacks"""
        for callback in self.completion_callbacks:
            try:
                callback(request_id, success)
            except Exception as e:
                enviar_senal_log("ERROR", f"Error en completion callback: {e}", "candle_coordinator")

    def _notify_error(self, request_id: str, error: Exception) -> None:
        """Notifica error a todos los callbacks"""
        for callback in self.error_callbacks:
            try:
                callback(request_id, error)
            except Exception as e:
                enviar_senal_log("ERROR", f"Error en error callback: {e}", "candle_coordinator")

    def _get_priority_value(self, priority: FlowPriority) -> int:
        """Convierte prioridad a valor numérico"""
        priority_map = {
            FlowPriority.URGENT: 1,
            FlowPriority.HIGH: 2,
            FlowPriority.NORMAL: 3,
            FlowPriority.LOW: 4,
            FlowPriority.BACKGROUND: 5
        }
        return priority_map.get(priority, 3)

# Instancia global del coordinador
candle_coordinator = CandleCoordinator()

# Funciones de conveniencia para compatibilidad
def get_candle_coordinator() -> CandleCoordinator:
    """Obtiene la instancia global del coordinador"""
    return candle_coordinator

def start_candle_coordinator() -> bool:
    """Inicia el coordinador global"""
    return candle_coordinator.start_coordinator()

def stop_candle_coordinator() -> None:
    """Detiene el coordinador global"""
    candle_coordinator.stop_coordinator()
