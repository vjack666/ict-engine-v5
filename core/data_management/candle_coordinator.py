#!/usr/bin/env python3
"""
🎯 CANDLE COORDINATOR - ICT ENGINE v5.0
======================================

Coordinador inteligente para gestión de datos de mercado
Orquesta el AdvancedCandleDownloader con el dashboard y el ICT Engine

Creado por Sprint 1.2 Executor
"""

import time
import threading
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

# Importar el downloader existente
try:
    from utils.advanced_candle_downloader import AdvancedCandleDownloader
except ImportError:
    print("Warning: No se pudo importar AdvancedCandleDownloader desde utils")
    try:
        import sys
        sys.path.append(str(Path(__file__).parent.parent.parent))
        from utils.advanced_candle_downloader import AdvancedCandleDownloader
    except ImportError:
        print("Error: No se puede importar AdvancedCandleDownloader")
        AdvancedCandleDownloader = None

class CandleCoordinator:
    """
    🎯 COORDINADOR CENTRAL PARA GESTIÓN DE DATOS DE MERCADO

    Responsabilidades:
    - Orquestar AdvancedCandleDownloader
    - Gestionar prioridades de descarga
    - Coordinar con dashboard en tiempo real
    - Auto-trigger basado en necesidades ICT
    - Monitoreo de calidad de datos
    """

    def __init__(self, data_dir: str = "data/candles"):
        self.data_dir = Path(data_dir)

        # Inicializar downloader si está disponible
        if AdvancedCandleDownloader:
            self.downloader = AdvancedCandleDownloader(str(self.data_dir))
        else:
            self.downloader = None
            print("Warning: CandleCoordinator iniciado sin AdvancedCandleDownloader")

        # Estado del coordinador
        self.is_running = False
        self.current_downloads = {}
        self.download_queue = []
        self.last_update = datetime.now()

        # Callbacks para dashboard
        self.progress_callback: Optional[Callable] = None
        self.completion_callback: Optional[Callable] = None
        self.error_callback: Optional[Callable] = None

        # Thread para operaciones en background
        self.worker_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()

        # Configuración de prioridades
        self.timeframe_priorities = {
            "H4": 1,  # Mayor prioridad
            "H1": 2,
            "M15": 3,
            "M5": 4,
            "M1": 5   # Menor prioridad
        }

    def set_progress_callback(self, callback: Callable):
        """Establece callback para updates de progreso al dashboard"""
        self.progress_callback = callback

    def set_completion_callback(self, callback: Callable):
        """Establece callback para notificación de completado"""
        self.completion_callback = callback

    def set_error_callback(self, callback: Callable):
        """Establece callback para manejo de errores"""
        self.error_callback = callback

    def start_coordinator(self):
        """Inicia el coordinador en modo background"""
        if self.is_running:
            return False

        self.is_running = True
        self.stop_event.clear()

        # Iniciar thread de trabajo
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

        return True

    def stop_coordinator(self):
        """Detiene el coordinador"""
        if not self.is_running:
            return

        self.is_running = False
        self.stop_event.set()

        if self.worker_thread:
            self.worker_thread.join(timeout=5.0)

    def queue_download(self, symbol: str, timeframe: str, lookback: int = 50000, priority: int = None):
        """Añade descarga a la cola con priorización inteligente"""
        if priority is None:
            priority = self.timeframe_priorities.get(timeframe, 10)

        download_task = {
            'symbol': symbol,
            'timeframe': timeframe,
            'lookback': lookback,
            'priority': priority,
            'queued_at': datetime.now()
        }

        # Insertar en cola ordenada por prioridad
        inserted = False
        for i, task in enumerate(self.download_queue):
            if priority < task['priority']:
                self.download_queue.insert(i, download_task)
                inserted = True
                break

        if not inserted:
            self.download_queue.append(download_task)

        return len(self.download_queue)

    def download_immediate(self, symbol: str, timeframe: str, lookback: int = 50000) -> bool:
        """Descarga inmediata (bloquea hasta completar)"""
        if not self.downloader:
            print("Error: No hay downloader disponible")
            return False

        try:
            stats = self.downloader.download_symbol_timeframe(symbol, timeframe, lookback)

            if self.completion_callback and stats.success:
                self.completion_callback(symbol, timeframe, stats)
            elif self.error_callback and not stats.success:
                self.error_callback(symbol, timeframe, stats.error_message)

            return stats.success

        except Exception as e:
            if self.error_callback:
                self.error_callback(symbol, timeframe, str(e))
            return False

    def download_multiple_coordinated(self, symbols: List[str], timeframes: List[str],
                                    lookback: int = 50000) -> Dict:
        """Descarga múltiple con coordinación inteligente"""

        if not self.downloader:
            return {'error': 'No downloader available'}

        # Priorizar y crear tareas
        tasks = []
        for symbol in symbols:
            for timeframe in timeframes:
                priority = self.timeframe_priorities.get(timeframe, 10)
                tasks.append({
                    'symbol': symbol,
                    'timeframe': timeframe,
                    'lookback': lookback,
                    'priority': priority
                })

        # Ordenar por prioridad
        tasks.sort(key=lambda x: x['priority'])

        # Ejecutar descargas
        results = {
            'completed': [],
            'failed': [],
            'total_time': 0,
            'total_bars': 0
        }

        start_time = datetime.now()

        for task in tasks:
            if self.progress_callback:
                self.progress_callback(task['symbol'], task['timeframe'], 'starting')

            stats = self.downloader.download_symbol_timeframe(
                task['symbol'], task['timeframe'], task['lookback']
            )

            if stats.success:
                results['completed'].append(stats)
                results['total_bars'] += stats.downloaded_bars

                if self.completion_callback:
                    self.completion_callback(task['symbol'], task['timeframe'], stats)
            else:
                results['failed'].append(stats)

                if self.error_callback:
                    self.error_callback(task['symbol'], task['timeframe'], stats.error_message)

        results['total_time'] = (datetime.now() - start_time).total_seconds()
        return results

    def check_data_freshness(self, symbol: str, timeframe: str, max_age_hours: int = 24) -> bool:
        """Verifica si los datos están actualizados"""
        try:
            data_file = self.data_dir / f"{timeframe}.csv"
            if not data_file.exists():
                return False

            # Verificar edad del archivo
            file_age = datetime.now() - datetime.fromtimestamp(data_file.stat().st_mtime)
            if file_age > timedelta(hours=max_age_hours):
                return False

            # Verificar contenido
            df = pd.read_csv(data_file)
            if df.empty:
                return False

            return True

        except Exception:
            return False

    def auto_update_stale_data(self, symbols: List[str], timeframes: List[str],
                              max_age_hours: int = 24):
        """Auto-actualiza datos obsoletos"""
        stale_data = []

        for symbol in symbols:
            for timeframe in timeframes:
                if not self.check_data_freshness(symbol, timeframe, max_age_hours):
                    stale_data.append((symbol, timeframe))

        if stale_data:
            for symbol, timeframe in stale_data:
                self.queue_download(symbol, timeframe)

        return len(stale_data)

    def get_status(self) -> Dict:
        """Obtiene estado actual del coordinador"""
        return {
            'is_running': self.is_running,
            'queue_length': len(self.download_queue),
            'active_downloads': len(self.current_downloads),
            'last_update': self.last_update.isoformat(),
            'downloader_connected': self.downloader is not None and hasattr(self.downloader, 'is_connected')
        }

    def _worker_loop(self):
        """Loop principal del worker thread"""
        while not self.stop_event.wait(1.0):  # Check every second
            if not self.download_queue or not self.downloader:
                continue

            # Procesar próxima tarea
            task = self.download_queue.pop(0)

            try:
                # Registrar descarga activa
                task_id = f"{task['symbol']}_{task['timeframe']}"
                self.current_downloads[task_id] = task

                if self.progress_callback:
                    self.progress_callback(task['symbol'], task['timeframe'], 'downloading')

                # Ejecutar descarga
                stats = self.downloader.download_symbol_timeframe(
                    task['symbol'], task['timeframe'], task['lookback']
                )

                # Notificar resultado
                if stats.success and self.completion_callback:
                    self.completion_callback(task['symbol'], task['timeframe'], stats)
                elif not stats.success and self.error_callback:
                    self.error_callback(task['symbol'], task['timeframe'], stats.error_message)

            except Exception as e:
                if self.error_callback:
                    self.error_callback(task['symbol'], task['timeframe'], str(e))
            finally:
                # Limpiar descarga activa
                if task_id in self.current_downloads:
                    del self.current_downloads[task_id]

            self.last_update = datetime.now()

# Instancia global para usar desde dashboard
candle_coordinator = CandleCoordinator()
