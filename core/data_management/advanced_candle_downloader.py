
from sistema.imports_interface import Dict, timedelta, List, field, datetime, dataclass, asdict, Any, Tuple, timezone, Optional, Union
from sistema.imports_interface import get_mt5_manager, get_candle_downloader, log_info, enviar_senal_log, get_logging, log_error
from sistema.imports_interface import asyncio, time, Path
import threading
import pandas as pd

#!/usr/bin/env python3
"""
📥 ADVANCED CANDLE DOWNLOADER - ICT ENGINE v5.0
==============================================

Downloader avanzado de velas que integra con:
- CandleCoordinator para orquestación
- CandleDownloaderWidget para UI
- MT5DataManager para datos reales
- Dashboard para control visual

Características:
- Descarga masiva de datos históricos
- Soporte para múltiples símbolos y timeframes
- Progress tracking en tiempo real
- Manejo robusto de errores
- Integración completa con el dashboard

Creado por: Sistema Sentinel v5.0
Fecha: 2025-08-05
"""

import asyncio
import threading
from sistema.sic import time
from sistema.sic import Dict, List, Optional, Callable, Any, Set
from sistema.sic import datetime
from sistema.sic import dataclass
from sistema.sic import Path
import pandas as pd
# Importaciones del sistema
from sistema.sic import enviar_senal_log
from utils.mt5_data_manager import get_mt5_manager
from core.data_management.candle_coordinator import CandleCoordinator, DownloadRequest, DownloadStatus

@dataclass
class DownloadStats:
    """Estadísticas de descarga"""
    symbol: str
    timeframe: str
    total_bars: int = 0
    downloaded_bars: int = 0
    download_speed: float = 0.0  # velas por segundo
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    success: bool = False
    error_message: str = ""

class AdvancedCandleDownloader:
    """
    📥 DOWNLOADER AVANZADO DE VELAS
    =============================

    Maneja descargas masivas de datos históricos con:
    - Progreso en tiempo real
    - Callbacks para UI updates
    - Manejo robusto de errores
    - Integración con coordinador
    """

    def __init__(self,
                 progress_callback: Optional[Callable] = None,
                 complete_callback: Optional[Callable] = None,
                 error_callback: Optional[Callable] = None):
        """
        Inicializa el downloader

        Args:
            progress_callback: Función llamada durante el progreso
            complete_callback: Función llamada al completar
            error_callback: Función llamada en errores
        """

        # Sistema de callbacks para UI
        self.progress_callback = progress_callback
        self.complete_callback = complete_callback
        self.error_callback = error_callback

        # Estado del downloader
        self.is_downloading = False
        self.active_downloads: Dict[str, DownloadStats] = {}
        self.download_queue: List[DownloadRequest] = []

        # Componentes del sistema
        self.mt5_manager = None
        self.coordinator = None

        # Configuración
        self.max_concurrent_downloads = 3
        self.download_batch_size = 10000  # velas por batch
        self.retry_attempts = 3
        self.retry_delay = 2.0  # segundos

        # Lock para thread safety
        self.lock = threading.Lock()

        # Worker thread
        self.worker_thread = None
        self.stop_event = threading.Event()

        enviar_senal_log("INFO", "AdvancedCandleDownloader inicializado", "advanced_candle_downloader", "initialization")

    def initialize(self) -> bool:
        """Inicializa el downloader y sus componentes"""
        try:
            # Inicializar MT5 Manager
            self.mt5_manager = get_mt5_manager()
            if not self.mt5_manager:
                enviar_senal_log("ERROR", "No se pudo obtener MT5Manager", "advanced_candle_downloader", "initialization")
                return False

            # Conectar MT5
            if not self.mt5_manager.connect():
                enviar_senal_log("ERROR", "No se pudo conectar a MT5", "advanced_candle_downloader", "initialization")
                return False

            # Inicializar coordinador
            self.coordinator = CandleCoordinator()
            if not self.coordinator.start_coordinator():
                enviar_senal_log("ERROR", "No se pudo iniciar CandleCoordinator", "advanced_candle_downloader", "initialization")
                return False

            enviar_senal_log("INFO", "AdvancedCandleDownloader inicializado exitosamente", "advanced_candle_downloader", "initialization")
            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"Error inicializando AdvancedCandleDownloader: {e}", "advanced_candle_downloader", "initialization")
            return False

    def start_batch_download(self,
                           symbols: List[str],
                           timeframes: List[str],
                           lookback_bars: int = 50000) -> bool:
        """
        Inicia descarga masiva de múltiples símbolos y timeframes

        Args:
            symbols: Lista de símbolos a descargar
            timeframes: Lista de timeframes
            lookback_bars: Cantidad de velas por descarga

        Returns:
            bool: True si se inició correctamente
        """

        if self.is_downloading:
            enviar_senal_log("WARNING", "Descarga ya en progreso", "advanced_candle_downloader", "download")
            return False

        try:
            # Limpiar estado anterior
            with self.lock:
                self.active_downloads.clear()
                self.download_queue.clear()
                self.stop_event.clear()

            # Generar solicitudes de descarga
            for symbol in symbols:
                for timeframe in timeframes:
                    request = DownloadRequest(
                        symbol=symbol,
                        timeframe=timeframe,
                        lookback=lookback_bars,
                        request_id=f"{symbol}_{timeframe}_{int(time.time())}"
                    )
                    self.download_queue.append(request)

            # Iniciar worker thread
            self.is_downloading = True
            self.worker_thread = threading.Thread(target=self._download_worker, daemon=True)
            self.worker_thread.start()

            enviar_senal_log("INFO", f"Descarga masiva iniciada: {len(symbols)} símbolos, {len(timeframes)} timeframes", "advanced_candle_downloader", "download")
            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"Error iniciando descarga masiva: {e}", "advanced_candle_downloader", "download")
            self.is_downloading = False
            return False

    def stop_download(self) -> None:
        """Detiene todas las descargas en progreso"""
        if not self.is_downloading:
            return

        enviar_senal_log("INFO", "Deteniendo descargas...", "advanced_candle_downloader", "download")
        self.stop_event.set()

        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=10.0)

        self.is_downloading = False
        enviar_senal_log("INFO", "Descargas detenidas", "advanced_candle_downloader", "download")

    def _download_worker(self) -> None:
        """Worker thread que procesa las descargas"""
        try:
            concurrent_downloads = 0

            while not self.stop_event.is_set() and self.download_queue:
                # Limitar descargas concurrentes
                if concurrent_downloads >= self.max_concurrent_downloads:
                    time.sleep(0.5)
                    continue

                # Obtener siguiente descarga
                with self.lock:
                    if not self.download_queue:
                        break
                    request = self.download_queue.pop(0)

                # Iniciar descarga en thread separado
                download_thread = threading.Thread(
                    target=self._download_single,
                    args=(request,),
                    daemon=True
                )
                download_thread.start()
                concurrent_downloads += 1

                # Pequeña pausa para evitar saturar
                time.sleep(0.1)

            # Esperar que terminen todas las descargas
            while concurrent_downloads > 0:
                time.sleep(1.0)
                # Contar threads activos (simplificado)
                # En implementación real, usar mejor tracking

        except Exception as e:
            enviar_senal_log("ERROR", f"Error en download_worker: {e}", "advanced_candle_downloader", "download")
        finally:
            self.is_downloading = False

    def _download_single(self, request: DownloadRequest) -> None:
        """
        Descarga un símbolo/timeframe específico

        Args:
            request: Solicitud de descarga
        """

        stats = DownloadStats(
            symbol=request.symbol,
            timeframe=request.timeframe,
            total_bars=request.lookback,
            start_time=datetime.now()
        )

        # Registrar descarga activa
        with self.lock:
            self.active_downloads[request.request_id] = stats

        try:
            # Verificar que el símbolo esté disponible
            if not self.mt5_manager.verificar_simbolo(request.symbol):
                raise Exception(f"Símbolo {request.symbol} no disponible")

            # Callback de inicio
            if self.progress_callback:
                self._safe_callback(self.progress_callback, request.symbol, request.timeframe, 0.0, stats)

            # Descarga por batches para mostrar progreso
            total_downloaded = 0

            while total_downloaded < request.lookback and not self.stop_event.is_set():
                # Calcular tamaño del batch
                remaining = request.lookback - total_downloaded
                batch_size = min(self.download_batch_size, remaining)

                # Descargar batch
                batch_start = time.time()
                batch_data = self.mt5_manager.get_historical_data(
                    request.symbol,
                    request.timeframe,
                    batch_size,
                    force_download=True
                )

                if batch_data is None or batch_data.empty:
                    raise Exception("No se pudieron obtener datos")

                # Actualizar estadísticas
                batch_time = time.time() - batch_start
                batch_bars = len(batch_data)
                total_downloaded += batch_bars

                stats.downloaded_bars = total_downloaded
                stats.download_speed = batch_bars / max(batch_time, 0.001)

                # Callback de progreso
                progress = (total_downloaded / request.lookback) * 100
                if self.progress_callback:
                    self._safe_callback(self.progress_callback, request.symbol, request.timeframe, progress, stats)

                # Pausa para no saturar
                if not self.stop_event.is_set():
                    time.sleep(0.1)

            # Marcar como exitoso
            stats.success = True
            stats.end_time = datetime.now()

            # Callback de completado
            if self.complete_callback:
                self._safe_callback(self.complete_callback, request.symbol, request.timeframe, stats)

            enviar_senal_log("INFO", f"Descarga completada: {request.symbol} {request.timeframe} - {total_downloaded} velas", "advanced_candle_downloader", "download")

        except Exception as e:
            # Marcar como fallido
            stats.success = False
            stats.error_message = str(e)
            stats.end_time = datetime.now()

            # Callback de error
            if self.error_callback:
                self._safe_callback(self.error_callback, request.symbol, request.timeframe, str(e))

            enviar_senal_log("ERROR", f"Error descargando {request.symbol} {request.timeframe}: {e}", "advanced_candle_downloader", "download")

        finally:
            # Limpiar descarga activa
            with self.lock:
                if request.request_id in self.active_downloads:
                    del self.active_downloads[request.request_id]

    def _safe_callback(self, callback: Callable, *args, **kwargs) -> None:
        """Ejecuta callback de forma segura"""
        try:
            callback(*args, **kwargs)
        except Exception as e:
            enviar_senal_log("ERROR", f"Error en callback: {e}", "advanced_candle_downloader", "callback")

    def get_download_progress(self) -> Dict[str, Dict]:
        """Obtiene progreso actual de todas las descargas"""
        with self.lock:
            progress_data = {}
            for request_id, stats in self.active_downloads.items():
                key = f"{stats.symbol}_{stats.timeframe}"
                progress_data[key] = {
                    'progress': (stats.downloaded_bars / stats.total_bars) * 100 if stats.total_bars > 0 else 0,
                    'bars_downloaded': stats.downloaded_bars,
                    'total_bars': stats.total_bars,
                    'speed': stats.download_speed,
                    'symbol': stats.symbol,
                    'timeframe': stats.timeframe
                }
            return progress_data

    def get_download_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas generales de descarga"""
        with self.lock:
            active_count = len(self.active_downloads)
            queued_count = len(self.download_queue)

            total_bars = sum(stats.total_bars for stats in self.active_downloads.values())
            downloaded_bars = sum(stats.downloaded_bars for stats in self.active_downloads.values())
            avg_speed = sum(stats.download_speed for stats in self.active_downloads.values())
            if active_count > 0:
                avg_speed /= active_count

            return {
                'is_downloading': self.is_downloading,
                'active_downloads': active_count,
                'queued_downloads': queued_count,
                'total_bars': total_bars,
                'downloaded_bars': downloaded_bars,
                'average_speed': avg_speed,
                'progress_percentage': (downloaded_bars / total_bars * 100) if total_bars > 0 else 0
            }

    def shutdown(self) -> None:
        """Cierra el downloader y libera recursos"""
        self.stop_download()

        if self.coordinator:
            self.coordinator.stop_coordinator()

        enviar_senal_log("INFO", "AdvancedCandleDownloader cerrado", "advanced_candle_downloader", "shutdown")

# Instancia global para uso en el sistema
advanced_candle_downloader = None

def get_advanced_candle_downloader() -> AdvancedCandleDownloader:
    """Obtiene la instancia global del downloader"""
    global advanced_candle_downloader
    if advanced_candle_downloader is None:
        advanced_candle_downloader = AdvancedCandleDownloader()
    return advanced_candle_downloader
