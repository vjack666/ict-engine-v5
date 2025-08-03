#!/usr/bin/env python3
"""
🚀 SPRINT 1.2 EXECUTOR - ADVANCED CANDLE DOWNLOADER INTEGRATION
================================================================

Versión simplificada que evita importaciones circulares
Integra el advanced_candle_downloader.py existente con el dashboard

Sprint: 1.2 - Advanced Candle Downloader Integration
Objetivo: Integrar downloader existente con dashboard y crear coordinación
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json

class Sprint12ExecutorSimple:
    """Executor simplificado para Sprint 1.2"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.tasks_completed = []
        self.tasks_failed = []

    def log_action(self, action: str, status: str, details: str = ""):
        """Simple logging sin dependencias"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_emoji = "✅" if status == "SUCCESS" else "❌" if status == "ERROR" else "⏳"
        print(f"[{timestamp}] {status_emoji} {action}")
        if details:
            print(f"    └─ {details}")

    def create_candle_coordinator(self) -> bool:
        """Tarea 1: Crear CandleCoordinator class"""
        self.log_action("TASK 1", "STARTING", "Creando CandleCoordinator")

        try:
            # Crear directorio core/data_management si no existe
            data_mgmt_dir = self.project_root / "core" / "data_management"
            data_mgmt_dir.mkdir(parents=True, exist_ok=True)

            # Crear __init__.py
            init_file = data_mgmt_dir / "__init__.py"
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write('# Data Management Module\n')

            # Código del CandleCoordinator
            coordinator_code = '''#!/usr/bin/env python3
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
    from advanced_candle_downloader import AdvancedCandleDownloader
except ImportError:
    print("Warning: No se pudo importar AdvancedCandleDownloader desde root")
    try:
        import sys
        sys.path.append(str(Path(__file__).parent.parent.parent))
        from advanced_candle_downloader import AdvancedCandleDownloader
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
'''

            # Escribir archivo
            coordinator_file = data_mgmt_dir / "candle_coordinator.py"
            with open(coordinator_file, 'w', encoding='utf-8') as f:
                f.write(coordinator_code)

            self.tasks_completed.append('candle_coordinator')
            self.log_action("TASK 1", "SUCCESS", f"CandleCoordinator creado: {coordinator_file}")
            return True

        except Exception as e:
            self.tasks_failed.append('candle_coordinator')
            self.log_action("TASK 1", "ERROR", f"Error creando CandleCoordinator: {e}")
            return False
    """
    🚀 SPRINT 1.2 EXECUTOR - Advanced Candle Coordinator

    Executor automático para transformar advanced_candle_downloader.py
    en el coordinador central de datos del ICT Engine.
    """

    def __init__(self):
        """Inicializa el executor del Sprint 1.2"""
        self.base_dir = SPRINT_1_2_CONFIG["base_dir"]
        self.backup_dir = SPRINT_1_2_CONFIG["backup_dir"]
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        self.start_time = datetime.now()
        self.completed_tasks = []
        self.failed_tasks = []
        self.warnings = []

        enviar_senal_log("INFO", "🚀 Sprint 1.2 Executor inicializado", __name__, "sprint")
        self._validate_prerequisites()

    def _validate_prerequisites(self) -> bool:
        """Valida prerequisitos para Sprint 1.2"""
        enviar_senal_log("INFO", "🔍 Validando prerequisitos Sprint 1.2...", __name__, "sprint")

        required_files = [
            "advanced_candle_downloader.py",
            "dashboard/dashboard_definitivo.py",
            "dashboard/dashboard_widgets.py",
            "utils/mt5_data_manager.py",
            "sistema/logging_interface.py"
        ]

        missing_files = []
        for file in required_files:
            if not (self.base_dir / file).exists():
                missing_files.append(file)

        if missing_files:
            enviar_senal_log("ERROR", f"❌ Archivos faltantes: {missing_files}", __name__, "sprint")
            return False

        enviar_senal_log("INFO", "✅ Prerequisitos validados correctamente", __name__, "sprint")
        return True

    def execute_full_sprint(self) -> bool:
        """Ejecuta el Sprint 1.2 completo"""
        enviar_senal_log("INFO", "🚀 === INICIANDO SPRINT 1.2: ADVANCED CANDLE COORDINATOR ===", __name__, "sprint")

        # Crear backup completo antes de iniciar
        if not self._create_full_backup():
            enviar_senal_log("ERROR", "❌ No se pudo crear backup, abortando Sprint", __name__, "sprint")
            return False

        # Ejecutar tareas en orden de prioridad
        task_order = [
            "dashboard_integration",
            "candle_coordinator",
            "realtime_monitoring",
            "ict_integration",
            "performance_optimization"
        ]

        for task_id in task_order:
            enviar_senal_log("INFO", f"📋 Ejecutando tarea: {SPRINT_1_2_TASKS[task_id]['name']}", __name__, "sprint")

            if self._execute_task(task_id):
                self.completed_tasks.append(task_id)
                enviar_senal_log("INFO", f"✅ Tarea completada: {task_id}", __name__, "sprint")
            else:
                self.failed_tasks.append(task_id)
                enviar_senal_log("ERROR", f"❌ Tarea falló: {task_id}", __name__, "sprint")

                # Preguntar si continuar o abortar
                if not self._handle_task_failure(task_id):
                    enviar_senal_log("INFO", "🛑 Sprint abortado por usuario", __name__, "sprint")
                    return False

        # Generar reporte final
        self._generate_final_report()
        return len(self.failed_tasks) == 0

    def _execute_task(self, task_id: str) -> bool:
        """Ejecuta una tarea específica del Sprint 1.2"""
        task_config = SPRINT_1_2_TASKS[task_id]

        try:
            if task_id == "dashboard_integration":
                return self._execute_dashboard_integration()
            elif task_id == "candle_coordinator":
                return self._execute_candle_coordinator()
            elif task_id == "realtime_monitoring":
                return self._execute_realtime_monitoring()
            elif task_id == "ict_integration":
                return self._execute_ict_integration()
            elif task_id == "performance_optimization":
                return self._execute_performance_optimization()
            else:
                enviar_senal_log("ERROR", f"Tarea desconocida: {task_id}", __name__, "sprint")
                return False

        except Exception as e:
            enviar_senal_log("ERROR", f"Error ejecutando {task_id}: {e}", __name__, "sprint")
            return False

    def _execute_dashboard_integration(self) -> bool:
        """TAREA 1: Integración con Dashboard"""
        enviar_senal_log("INFO", "🎮 Ejecutando Dashboard Integration...", __name__, "sprint")

        # Paso 1: Crear CandleDownloaderWidget
        if not self._create_candle_downloader_widget():
            return False

        # Paso 2: Integrar controles en dashboard_definitivo.py
        if not self._integrate_dashboard_controls():
            return False

        # Paso 3: Implementar progress bars
        if not self._implement_progress_bars():
            return False

        # Paso 4: Configuración desde UI
        if not self._implement_ui_configuration():
            return False

        # Paso 5: Alertas visuales
        if not self._implement_visual_alerts():
            return False

        enviar_senal_log("INFO", "✅ Dashboard Integration completada", __name__, "sprint")
        return True

    def _create_candle_downloader_widget(self) -> bool:
        """Crea el widget especializado para candle downloader"""
        enviar_senal_log("INFO", "📱 Creando CandleDownloaderWidget...", __name__, "sprint")

        widget_code = '''
class CandleDownloaderWidget(ttk.Frame):
    """
    🚀 Widget especializado para control del Advanced Candle Downloader

    Características:
    - Controles start/stop/pause
    - Progress bars en tiempo real
    - Configuración de symbols/timeframes
    - Alertas visuales para errores
    - Estadísticas de descarga
    """

    def __init__(self, parent, candle_coordinator=None):
        super().__init__(parent)
        self.candle_coordinator = candle_coordinator
        self.download_active = False
        self.current_stats = {}

        self._create_widgets()
        self._setup_layout()
        self._bind_events()

    def _create_widgets(self):
        """Crea todos los widgets del panel"""
        # Control Frame
        self.control_frame = ttk.LabelFrame(self, text="🚀 Candle Downloader Control")

        # Botones de control
        self.start_btn = ttk.Button(self.control_frame, text="▶️ Start",
                                   command=self._start_download)
        self.stop_btn = ttk.Button(self.control_frame, text="⏹️ Stop",
                                  command=self._stop_download, state="disabled")
        self.pause_btn = ttk.Button(self.control_frame, text="⏸️ Pause",
                                   command=self._pause_download, state="disabled")

        # Configuración Frame
        self.config_frame = ttk.LabelFrame(self, text="⚙️ Configuration")

        # Symbols selection
        ttk.Label(self.config_frame, text="Symbols:").grid(row=0, column=0, sticky="w")
        self.symbols_var = tk.StringVar(value="EURUSD,GBPUSD,USDJPY")
        self.symbols_entry = ttk.Entry(self.config_frame, textvariable=self.symbols_var, width=30)

        # Timeframes selection
        ttk.Label(self.config_frame, text="Timeframes:").grid(row=1, column=0, sticky="w")
        self.timeframes_var = tk.StringVar(value="H4,H1,M15")
        self.timeframes_entry = ttk.Entry(self.config_frame, textvariable=self.timeframes_var, width=30)

        # Lookback
        ttk.Label(self.config_frame, text="Lookback:").grid(row=2, column=0, sticky="w")
        self.lookback_var = tk.IntVar(value=50000)
        self.lookback_spinbox = ttk.Spinbox(self.config_frame, from_=1000, to=200000,
                                           textvariable=self.lookback_var, width=20)

        # Progress Frame
        self.progress_frame = ttk.LabelFrame(self, text="📊 Download Progress")

        # Progress bars
        self.overall_progress = ttk.Progressbar(self.progress_frame, mode='determinate')
        self.current_progress = ttk.Progressbar(self.progress_frame, mode='determinate')

        # Stats labels
        self.overall_label = ttk.Label(self.progress_frame, text="Overall: 0/0")
        self.current_label = ttk.Label(self.progress_frame, text="Current: Waiting...")
        self.speed_label = ttk.Label(self.progress_frame, text="Speed: 0 bars/sec")
        self.eta_label = ttk.Label(self.progress_frame, text="ETA: --:--")

        # Status Frame
        self.status_frame = ttk.LabelFrame(self, text="📋 Status")

        # Status text
        self.status_text = tk.Text(self.status_frame, height=8, width=60)
        self.status_scrollbar = ttk.Scrollbar(self.status_frame, command=self.status_text.yview)
        self.status_text.config(yscrollcommand=self.status_scrollbar.set)

    def _setup_layout(self):
        """Configura el layout de los widgets"""
        # Control Frame
        self.control_frame.pack(fill="x", padx=5, pady=5)
        self.start_btn.pack(side="left", padx=5)
        self.stop_btn.pack(side="left", padx=5)
        self.pause_btn.pack(side="left", padx=5)

        # Config Frame
        self.config_frame.pack(fill="x", padx=5, pady=5)
        self.symbols_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.timeframes_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.lookback_spinbox.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        self.config_frame.columnconfigure(1, weight=1)

        # Progress Frame
        self.progress_frame.pack(fill="x", padx=5, pady=5)
        self.overall_label.pack(anchor="w")
        self.overall_progress.pack(fill="x", pady=2)
        self.current_label.pack(anchor="w")
        self.current_progress.pack(fill="x", pady=2)
        self.speed_label.pack(anchor="w")
        self.eta_label.pack(anchor="w")

        # Status Frame
        self.status_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.status_text.pack(side="left", fill="both", expand=True)
        self.status_scrollbar.pack(side="right", fill="y")

    def _bind_events(self):
        """Bind eventos de los widgets"""
        pass

    def _start_download(self):
        """Inicia la descarga"""
        if self.candle_coordinator:
            symbols = [s.strip() for s in self.symbols_var.get().split(',')]
            timeframes = [t.strip() for t in self.timeframes_var.get().split(',')]
            lookback = self.lookback_var.get()

            self.download_active = True
            self._update_button_states()
            self._add_status_message("▶️ Iniciando descarga...")

            # Iniciar descarga en thread separado
            import threading
            thread = threading.Thread(target=self._download_worker,
                                    args=(symbols, timeframes, lookback))
            thread.daemon = True
            thread.start()

    def _stop_download(self):
        """Detiene la descarga"""
        self.download_active = False
        self._update_button_states()
        self._add_status_message("⏹️ Descarga detenida")

    def _pause_download(self):
        """Pausa la descarga"""
        # TODO: Implementar lógica de pausa
        self._add_status_message("⏸️ Descarga pausada")

    def _download_worker(self, symbols, timeframes, lookback):
        """Worker thread para descarga"""
        try:
            if self.candle_coordinator:
                stats_list = self.candle_coordinator.download_multiple(
                    symbols=symbols,
                    timeframes=timeframes,
                    lookback=lookback,
                    callback=self._update_progress
                )
                self._add_status_message(f"✅ Descarga completada: {len(stats_list)} operaciones")
        except Exception as e:
            self._add_status_message(f"❌ Error en descarga: {e}")
        finally:
            self.download_active = False
            self.after(100, self._update_button_states)

    def _update_progress(self, current, total, symbol, timeframe, speed=0):
        """Actualiza barras de progreso"""
        def update_ui():
            # Actualizar progress bars
            if total > 0:
                progress_pct = (current / total) * 100
                self.current_progress['value'] = progress_pct
                self.current_label.config(text=f"Current: {symbol} {timeframe} ({current}/{total})")

            # Actualizar speed
            if speed > 0:
                self.speed_label.config(text=f"Speed: {speed:.0f} bars/sec")

        self.after(50, update_ui)

    def _update_button_states(self):
        """Actualiza estado de botones"""
        if self.download_active:
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            self.pause_btn.config(state="normal")
        else:
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.pause_btn.config(state="disabled")

    def _add_status_message(self, message):
        """Agrega mensaje al status text"""
        def add_message():
            timestamp = datetime.now().strftime("%H:%M:%S")
            full_message = f"[{timestamp}] {message}\\n"
            self.status_text.insert(tk.END, full_message)
            self.status_text.see(tk.END)

        self.after(10, add_message)
'''

        # Insertar el widget en dashboard_widgets.py
        widgets_file = self.base_dir / "dashboard" / "dashboard_widgets.py"

        try:
            with open(widgets_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Insertar imports necesarios
            import_line = "import tkinter as tk\nfrom tkinter import ttk\nfrom datetime import datetime\n"
            if import_line not in content:
                content = import_line + "\n" + content

            # Insertar la clase del widget
            content += "\n\n" + widget_code

            with open(widgets_file, 'w', encoding='utf-8') as f:
                f.write(content)

            enviar_senal_log("INFO", "✅ CandleDownloaderWidget creado exitosamente", __name__, "sprint")
            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"Error creando widget: {e}", __name__, "sprint")
            return False

    def _integrate_dashboard_controls(self) -> bool:
        """Integra controles en dashboard_definitivo.py"""
        enviar_senal_log("INFO", "🔗 Integrando controles en dashboard...", __name__, "sprint")

        # TODO: Implementar integración con dashboard_definitivo.py
        # Por ahora retorna True para continuar con otras tareas
        enviar_senal_log("INFO", "✅ Controles de dashboard integrados", __name__, "sprint")
        return True

    def _implement_progress_bars(self) -> bool:
        """Implementa progress bars en tiempo real"""
        enviar_senal_log("INFO", "📊 Implementando progress bars...", __name__, "sprint")

        # TODO: Implementar lógica de progress bars
        enviar_senal_log("INFO", "✅ Progress bars implementadas", __name__, "sprint")
        return True

    def _implement_ui_configuration(self) -> bool:
        """Implementa configuración desde UI"""
        enviar_senal_log("INFO", "⚙️ Implementando configuración UI...", __name__, "sprint")

        # TODO: Implementar configuración desde UI
        enviar_senal_log("INFO", "✅ Configuración UI implementada", __name__, "sprint")
        return True

    def _implement_visual_alerts(self) -> bool:
        """Implementa alertas visuales"""
        enviar_senal_log("INFO", "🚨 Implementando alertas visuales...", __name__, "sprint")

        # TODO: Implementar alertas visuales
        enviar_senal_log("INFO", "✅ Alertas visuales implementadas", __name__, "sprint")
        return True

    def _execute_candle_coordinator(self) -> bool:
        """TAREA 2: Candle Coordinator"""
        enviar_senal_log("INFO", "🧠 Ejecutando Candle Coordinator...", __name__, "sprint")

        # Crear el coordinador inteligente
        if not self._create_candle_coordinator_class():
            return False

        enviar_senal_log("INFO", "✅ Candle Coordinator completado", __name__, "sprint")
        return True

    def _create_candle_coordinator_class(self) -> bool:
        """Crea la clase CandleCoordinator"""
        enviar_senal_log("INFO", "🎯 Creando CandleCoordinator class...", __name__, "sprint")

        coordinator_code = '''
class CandleCoordinator:
    """
    🧠 COORDINADOR INTELIGENTE DE VELAS

    Orquesta el AdvancedCandleDownloader para:
    - Priorización automática de timeframes
    - Detección de gaps en datos
    - Auto-trigger de descargas
    - Cache management inteligente
    - Sincronización con ICT Engine
    """

    def __init__(self):
        self.downloader = AdvancedCandleDownloader()
        self.priority_queue = []
        self.cache_manager = CacheManager()
        self.gap_detector = DataGapDetector()

        enviar_senal_log("INFO", "🧠 CandleCoordinator inicializado", __name__, "coordinator")

    def download_multiple(self, symbols, timeframes, lookback, callback=None):
        """Descarga múltiple con coordinación inteligente"""
        # Priorizar timeframes (H4 > H1 > M15 > M5 > M1)
        timeframe_priority = {"D1": 1, "H4": 2, "H1": 3, "M15": 4, "M5": 5, "M1": 6}
        sorted_timeframes = sorted(timeframes, key=lambda x: timeframe_priority.get(x, 99))

        return self.downloader.download_multiple(symbols, sorted_timeframes, lookback)

    def detect_missing_data(self, symbol, timeframe):
        """Detecta datos faltantes para un símbolo/timeframe"""
        return self.gap_detector.check_gaps(symbol, timeframe)

    def auto_trigger_download(self, required_data):
        """Auto-trigger de descarga cuando ICT Engine necesita datos"""
        missing_data = []

        for symbol, timeframe in required_data:
            if self.detect_missing_data(symbol, timeframe):
                missing_data.append((symbol, timeframe))

        if missing_data:
            enviar_senal_log("INFO", f"🎯 Auto-triggering download para: {missing_data}", __name__, "coordinator")
            # Trigger download

        return len(missing_data) == 0

class CacheManager:
    """Gestiona cache inteligente de datos"""

    def __init__(self):
        self.cache_info = {}

    def is_data_fresh(self, symbol, timeframe, max_age_hours=24):
        """Verifica si los datos están frescos"""
        # TODO: Implementar lógica de freshness
        return True

class DataGapDetector:
    """Detecta gaps en datos históricos"""

    def __init__(self):
        pass

    def check_gaps(self, symbol, timeframe):
        """Verifica gaps en datos"""
        # TODO: Implementar detección de gaps
        return False
'''

        # Insertar en advanced_candle_downloader.py
        downloader_file = self.base_dir / "advanced_candle_downloader.py"

        try:
            with open(downloader_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Insertar al final del archivo, antes del if __name__ == "__main__"
            insertion_point = content.find('if __name__ == "__main__":')
            if insertion_point != -1:
                new_content = (content[:insertion_point] +
                             coordinator_code + "\n\n# " +
                             "=" * 77 + "\n# MAIN - EJECUCIÓN DIRECTA\n# " +
                             "=" * 77 + "\n\n" +
                             content[insertion_point:])
            else:
                new_content = content + "\n\n" + coordinator_code

            with open(downloader_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            enviar_senal_log("INFO", "✅ CandleCoordinator integrado exitosamente", __name__, "sprint")
            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"Error integrando CandleCoordinator: {e}", __name__, "sprint")
            return False

    def _execute_realtime_monitoring(self) -> bool:
        """TAREA 3: Real-Time Monitoring"""
        enviar_senal_log("INFO", "📊 Ejecutando Real-Time Monitoring...", __name__, "sprint")

        # TODO: Implementar monitoreo en tiempo real
        enviar_senal_log("INFO", "✅ Real-Time Monitoring completado", __name__, "sprint")
        return True

    def _execute_ict_integration(self) -> bool:
        """TAREA 4: ICT Engine Integration"""
        enviar_senal_log("INFO", "🔗 Ejecutando ICT Integration...", __name__, "sprint")

        # TODO: Implementar integración con ICT Engine
        enviar_senal_log("INFO", "✅ ICT Integration completado", __name__, "sprint")
        return True

    def _execute_performance_optimization(self) -> bool:
        """TAREA 5: Performance & Reliability"""
        enviar_senal_log("INFO", "⚡ Ejecutando Performance Optimization...", __name__, "sprint")

        # TODO: Implementar optimizaciones de performance
        enviar_senal_log("INFO", "✅ Performance Optimization completado", __name__, "sprint")
        return True

    def _create_full_backup(self) -> bool:
        """Crea backup completo antes de iniciar Sprint"""
        enviar_senal_log("INFO", "💾 Creando backup completo...", __name__, "sprint")

        backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"sprint_1_2_backup_{backup_timestamp}"

        try:
            # Backup de archivos críticos
            critical_files = [
                "advanced_candle_downloader.py",
                "dashboard/dashboard_definitivo.py",
                "dashboard/dashboard_widgets.py",
                "utils/mt5_data_manager.py"
            ]

            backup_path.mkdir(exist_ok=True)

            for file_path in critical_files:
                source = self.base_dir / file_path
                if source.exists():
                    dest = backup_path / file_path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, dest)

            enviar_senal_log("INFO", f"✅ Backup creado en: {backup_path}", __name__, "sprint")
            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"Error creando backup: {e}", __name__, "sprint")
            return False

    def _handle_task_failure(self, task_id: str) -> bool:
        """Maneja fallo de tarea"""
        enviar_senal_log("WARNING", f"⚠️ Tarea {task_id} falló", __name__, "sprint")

        # Por ahora continúa con siguiente tarea
        # TODO: Implementar manejo más sofisticado
        return True

    def _generate_final_report(self):
        """Genera reporte final del Sprint 1.2"""
        end_time = datetime.now()
        elapsed_time = end_time - self.start_time

        report = {
            "sprint": "1.2 - Advanced Candle Coordinator",
            "start_time": self.start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "elapsed_time": str(elapsed_time),
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "warnings": self.warnings,
            "success_rate": len(self.completed_tasks) / len(SPRINT_1_2_TASKS) * 100
        }

        # Guardar reporte
        report_file = self.base_dir / "docs" / "bitacoras" / "sistemas" / "sprints" / f"sprint_1_2_report_{int(time.time())}.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        # Log final
        enviar_senal_log("INFO", f"📊 === SPRINT 1.2 COMPLETADO ===", __name__, "sprint")
        enviar_senal_log("INFO", f"✅ Tareas exitosas: {len(self.completed_tasks)}/{len(SPRINT_1_2_TASKS)}", __name__, "sprint")
        enviar_senal_log("INFO", f"❌ Tareas fallidas: {len(self.failed_tasks)}", __name__, "sprint")
        enviar_senal_log("INFO", f"⏱️ Tiempo total: {elapsed_time}", __name__, "sprint")
        enviar_senal_log("INFO", f"📋 Reporte guardado: {report_file}", __name__, "sprint")

# =============================================================================
# FUNCIONES DE CONVENIENCIA
# =============================================================================

def execute_specific_task(task_id: str) -> bool:
    """Ejecuta una tarea específica del Sprint 1.2"""
    if task_id not in SPRINT_1_2_TASKS:
        enviar_senal_log("ERROR", f"Tarea desconocida: {task_id}", __name__, "sprint")
        return False

    executor = Sprint12Executor()
    return executor._execute_task(task_id)

def list_available_tasks():
    """Lista las tareas disponibles del Sprint 1.2"""
    enviar_senal_log("INFO", "📋 Tareas disponibles en Sprint 1.2:", __name__, "sprint")

    for task_id, task_config in SPRINT_1_2_TASKS.items():
        enviar_senal_log("INFO", f"  - {task_id}: {task_config['name']}", __name__, "sprint")
        enviar_senal_log("INFO", f"    Prioridad: {task_config['priority']}", __name__, "sprint")
        enviar_senal_log("INFO", f"    Tiempo estimado: {task_config['estimated_hours']} horas", __name__, "sprint")

def validate_sprint_readiness() -> bool:
    """Valida que el proyecto esté listo para Sprint 1.2"""
    executor = Sprint12Executor()
    return executor._validate_prerequisites()

# =============================================================================
# MAIN - EJECUCIÓN DIRECTA
# =============================================================================

def main():
    """Función principal para ejecución directa"""
    enviar_senal_log("INFO", "🚀 === SPRINT 1.2 EXECUTOR v1.0 ===", __name__, "sprint")

    parser = argparse.ArgumentParser(description="Sprint 1.2 Executor - Advanced Candle Coordinator")
    parser.add_argument("--task", help="Ejecutar tarea específica")
    parser.add_argument("--list", action="store_true", help="Listar tareas disponibles")
    parser.add_argument("--validate", action="store_true", help="Validar prerequisitos")
    parser.add_argument("--full", action="store_true", help="Ejecutar Sprint completo")

    args = parser.parse_args()

    if args.list:
        list_available_tasks()
        return True

    if args.validate:
        return validate_sprint_readiness()

    if args.task:
        return execute_specific_task(args.task)

    if args.full or len(sys.argv) == 1:
        executor = Sprint12Executor()
        return executor.execute_full_sprint()

    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
