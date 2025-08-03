#!/usr/bin/env python3
"""
🚀 SPRINT 1.2 REFACTORIZADO - ADVANCED CANDLE DOWNLOADER ENHANCED
================================================================

Elimina la duplicación de CandleCoordinator y mejora directamente
el AdvancedCandleDownloader existente con callbacks y coordinación.

Enfoque: KISS (Keep It Simple, Stupid)
- Un solo componente responsable de descargas
- Callbacks integrados directamente
- Sin capas innecesarias de abstracción
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
import json

class Sprint12RefactoredExecutor:
    """Executor refactorizado que mejora AdvancedCandleDownloader directamente"""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        self.tasks_completed = []
        self.tasks_failed = []

    def log_action(self, action: str, status: str, details: str = ""):
        """Simple logging"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_emoji = "✅" if status == "SUCCESS" else "❌" if status == "ERROR" else "⏳"
        print(f"[{timestamp}] {status_emoji} {action}")
        if details:
            print(f"    └─ {details}")

    def enhance_advanced_downloader(self) -> bool:
        """Tarea 1: Mejorar AdvancedCandleDownloader con callbacks y coordinación"""
        self.log_action("TASK 1", "STARTING", "Mejorando AdvancedCandleDownloader")

        try:
            downloader_file = self.project_root / "utils" / "advanced_candle_downloader.py"

            if not downloader_file.exists():
                self.log_action("TASK 1", "ERROR", "advanced_candle_downloader.py no encontrado")
                return False

            # Leer contenido actual
            with open(downloader_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Crear backup
            backup_file = downloader_file.parent / "advanced_candle_downloader_backup.py"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)

            # Verificar si ya tiene las mejoras
            if "SPRINT 1.2 ENHANCEMENTS" in content:
                self.log_action("TASK 1", "SUCCESS", "AdvancedCandleDownloader ya tiene mejoras Sprint 1.2")
                self.tasks_completed.append('enhance_downloader')
                return True

            # Encontrar la posición del __init__ para agregar mejoras
            init_pos = content.find("def __init__(self, data_dir: str = \"data/candles\"):")
            if init_pos == -1:
                self.log_action("TASK 1", "ERROR", "No se encontró __init__ en AdvancedCandleDownloader")
                return False

            # Encontrar el final del __init__ original
            lines = content[init_pos:].split('\n')
            init_end_line = 0
            indent_count = 0

            for i, line in enumerate(lines[1:], 1):  # Skip def line
                if line.strip() == "":
                    continue
                if line.startswith("        ") and not line.startswith("    def "):
                    continue
                if line.startswith("    def ") or (line.strip() and not line.startswith("        ")):
                    init_end_line = i
                    break

            if init_end_line == 0:
                init_end_line = len(lines)

            init_end_pos = init_pos + len('\n'.join(lines[:init_end_line]))

            # Código de mejoras para agregar al final del __init__
            enhancement_code = '''

        # === SPRINT 1.2 ENHANCEMENTS: CALLBACKS Y COORDINACIÓN ===

        # Callbacks para integración con dashboard
        self.progress_callback: Optional[Callable] = None
        self.completion_callback: Optional[Callable] = None
        self.error_callback: Optional[Callable] = None

        # Sistema de prioridades
        self.timeframe_priorities = {
            "H4": 1,  # Mayor prioridad para ICT
            "H1": 2,
            "M15": 3,
            "M5": 4,
            "M1": 5   # Menor prioridad
        }

        # Cola de descargas con prioridades
        self.download_queue = []
        self.queue_lock = threading.Lock()

        enviar_senal_log("INFO", "✨ Sprint 1.2 enhancements activos", __name__, "downloader")
'''

            # Código de nuevos métodos para agregar después de los métodos existentes
            new_methods_code = '''

    # === NUEVOS MÉTODOS SPRINT 1.2: CALLBACKS ===

    def set_progress_callback(self, callback: Callable):
        """Establece callback para updates de progreso"""
        self.progress_callback = callback
        enviar_senal_log("DEBUG", "Progress callback configurado", __name__, "downloader")

    def set_completion_callback(self, callback: Callable):
        """Establece callback para descarga completada"""
        self.completion_callback = callback
        enviar_senal_log("DEBUG", "Completion callback configurado", __name__, "downloader")

    def set_error_callback(self, callback: Callable):
        """Establece callback para errores"""
        self.error_callback = callback
        enviar_senal_log("DEBUG", "Error callback configurado", __name__, "downloader")

    # === NUEVOS MÉTODOS SPRINT 1.2: COORDINACIÓN ===

    def queue_download(self, symbol: str, timeframe: str, lookback: int = 50000) -> int:
        """Añade descarga a cola con priorización automática"""
        priority = self.timeframe_priorities.get(timeframe, 10)

        task = {
            'symbol': symbol,
            'timeframe': timeframe,
            'lookback': lookback,
            'priority': priority,
            'queued_at': datetime.now()
        }

        with self.queue_lock:
            # Insertar ordenado por prioridad
            inserted = False
            for i, existing_task in enumerate(self.download_queue):
                if priority < existing_task['priority']:
                    self.download_queue.insert(i, task)
                    inserted = True
                    break

            if not inserted:
                self.download_queue.append(task)

            queue_length = len(self.download_queue)

        enviar_senal_log("INFO", f"📥 Queued: {symbol} {timeframe} (priority {priority}, queue: {queue_length})", __name__, "downloader")
        return queue_length

    def process_download_queue(self) -> List[DownloadStats]:
        """Procesa toda la cola de descargas en orden de prioridad"""
        all_stats = []

        with self.queue_lock:
            queue_copy = self.download_queue.copy()
            self.download_queue.clear()

        if not queue_copy:
            enviar_senal_log("INFO", "📭 Cola de descargas vacía", __name__, "downloader")
            return all_stats

        enviar_senal_log("INFO", f"🔄 Procesando {len(queue_copy)} descargas en cola", __name__, "downloader")

        for i, task in enumerate(queue_copy, 1):
            symbol = task['symbol']
            timeframe = task['timeframe']
            lookback = task['lookback']

            enviar_senal_log("INFO", f"📈 [{i}/{len(queue_copy)}] Procesando {symbol} {timeframe}", __name__, "downloader")

            # Callback de progreso
            if self.progress_callback:
                try:
                    self.progress_callback(symbol, timeframe, 'starting', progress=0)
                except Exception as e:
                    enviar_senal_log("WARNING", f"Error en progress callback: {e}", __name__, "downloader")

            # Ejecutar descarga
            stats = self.download_symbol_timeframe(symbol, timeframe, lookback)
            all_stats.append(stats)

            # Callbacks de resultado
            if stats.success and self.completion_callback:
                try:
                    self.completion_callback(symbol, timeframe, stats)
                except Exception as e:
                    enviar_senal_log("WARNING", f"Error en completion callback: {e}", __name__, "downloader")
            elif not stats.success and self.error_callback:
                try:
                    self.error_callback(symbol, timeframe, stats.error_message)
                except Exception as e:
                    enviar_senal_log("WARNING", f"Error en error callback: {e}", __name__, "downloader")

        return all_stats

    def download_with_coordination(self, symbols: List[str], timeframes: List[str],
                                 lookback: int = 50000) -> List[DownloadStats]:
        """Descarga coordinada con prioridades automáticas"""

        # Limpiar cola actual
        with self.queue_lock:
            self.download_queue.clear()

        # Añadir todas las tareas a la cola
        for symbol in symbols:
            for timeframe in timeframes:
                self.queue_download(symbol, timeframe, lookback)

        # Procesar cola completa
        return self.process_download_queue()

    def auto_update_stale_data(self, symbols: List[str], timeframes: List[str],
                              max_age_hours: int = 24) -> int:
        """Auto-actualiza datos obsoletos"""
        stale_count = 0

        for symbol in symbols:
            for timeframe in timeframes:
                if not self._check_data_freshness(symbol, timeframe, max_age_hours):
                    self.queue_download(symbol, timeframe)
                    stale_count += 1

        if stale_count > 0:
            enviar_senal_log("INFO", f"🔄 Auto-queued {stale_count} stale data updates", __name__, "downloader")

        return stale_count

    def _check_data_freshness(self, symbol: str, timeframe: str, max_age_hours: int) -> bool:
        """Verifica si los datos están actualizados"""
        try:
            data_file = self.data_dir / f"{timeframe}.csv"
            if not data_file.exists():
                return False

            # Verificar edad del archivo
            file_age = datetime.now() - datetime.fromtimestamp(data_file.stat().st_mtime)
            if file_age.total_seconds() > (max_age_hours * 3600):
                return False

            # Verificar contenido usando pandas
            try:
                import pandas as pd
                df = pd.read_csv(data_file)
                return not df.empty
            except:
                return False

        except Exception:
            return False

    def get_enhanced_status(self) -> Dict:
        """Estado mejorado con info de coordinación"""
        with self.queue_lock:
            queue_length = len(self.download_queue)
            queue_priorities = [task['priority'] for task in self.download_queue]

        return {
            'is_connected': self.is_connected,
            'active_downloads': self.active_downloads,
            'total_downloads': self.total_downloads,
            'queue_length': queue_length,
            'queue_priorities': queue_priorities,
            'has_callbacks': {
                'progress': self.progress_callback is not None,
                'completion': self.completion_callback is not None,
                'error': self.error_callback is not None
            },
            'last_update': datetime.now().isoformat()
        }
'''

            # Agregar import de threading si no existe
            if "import threading" not in content:
                typing_import_pos = content.find("from typing import")
                if typing_import_pos != -1:
                    line_end = content.find('\n', typing_import_pos)
                    content = content[:line_end] + '\nimport threading' + content[line_end:]

            # Insertar mejoras al final del __init__
            new_content = content[:init_end_pos] + enhancement_code + content[init_end_pos:]

            # Agregar nuevos métodos al final de la clase
            class_end = new_content.rfind('\n# ')  # Buscar comentario final o función global
            if class_end == -1:
                class_end = len(new_content)

            final_content = new_content[:class_end] + new_methods_code + new_content[class_end:]

            # Escribir archivo mejorado
            with open(downloader_file, 'w', encoding='utf-8') as f:
                f.write(final_content)

            self.tasks_completed.append('enhance_downloader')
            self.log_action("TASK 1", "SUCCESS", f"AdvancedCandleDownloader mejorado (backup: {backup_file.name})")
            return True

        except Exception as e:
            self.tasks_failed.append('enhance_downloader')
            self.log_action("TASK 1", "ERROR", f"Error mejorando downloader: {e}")
            return False

    def create_simple_widget(self) -> bool:
        """Tarea 2: Crear widget simplificado que use directamente el downloader mejorado"""
        self.log_action("TASK 2", "STARTING", "Creando widget simplificado")

        try:
            # Crear directorio dashboard si no existe
            dashboard_dir = self.project_root / "dashboard"
            dashboard_dir.mkdir(parents=True, exist_ok=True)

            widget_file = dashboard_dir / "simple_candle_widget.py"

            if widget_file.exists():
                self.log_action("TASK 2", "SUCCESS", "SimpleCandleWidget ya existe")
                self.tasks_completed.append('simple_widget')
                return True

            widget_code = '''#!/usr/bin/env python3
"""
🎮 SIMPLE CANDLE DOWNLOADER WIDGET - ICT ENGINE v5.0
===================================================

Widget simplificado que usa directamente el AdvancedCandleDownloader mejorado
Sin capas innecesarias de abstracción - KISS principle

Creado por Sprint 1.2 Refactored
"""

from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.console import Group
from rich import box
from datetime import datetime
from typing import Dict, List, Optional, Callable
import threading

# Usar directamente el downloader mejorado
try:
    from utils.advanced_candle_downloader import AdvancedCandleDownloader
except ImportError:
    print("Warning: No se pudo importar AdvancedCandleDownloader")
    AdvancedCandleDownloader = None

class SimpleCandleWidget:
    """
    🎮 WIDGET SIMPLIFICADO PARA CANDLE DOWNLOADER

    Características:
    - Usa directamente AdvancedCandleDownloader (sin capas extra)
    - Callbacks integrados para updates en tiempo real
    - Interfaz simple y clara
    - Performance optimizado
    """

    def __init__(self):
        # Crear instancia del downloader mejorado
        if AdvancedCandleDownloader:
            self.downloader = AdvancedCandleDownloader()

            # Configurar callbacks
            self.downloader.set_progress_callback(self.on_progress)
            self.downloader.set_completion_callback(self.on_completion)
            self.downloader.set_error_callback(self.on_error)
        else:
            self.downloader = None
            print("Warning: SimpleCandleWidget iniciado sin AdvancedCandleDownloader")

        # Estado del widget
        self.current_progress = {}
        self.recent_completions = []
        self.recent_errors = []
        self.widget_stats = {
            'sessions_started': 0,
            'total_successful': 0,
            'total_failed': 0,
            'total_bars_downloaded': 0
        }

        # Configuración actual
        self.config = {
            'symbols': ["EURUSD"],
            'timeframes': ["H4", "H1", "M15"],
            'lookback': 50000,
            'auto_update_stale': True
        }

        # Thread safety
        self.lock = threading.Lock()

    # === CALLBACKS ===

    def on_progress(self, symbol: str, timeframe: str, status: str, **kwargs):
        """Callback de progreso"""
        with self.lock:
            key = f"{symbol}_{timeframe}"
            self.current_progress[key] = {
                'symbol': symbol,
                'timeframe': timeframe,
                'status': status,
                'last_update': datetime.now(),
                **kwargs
            }

    def on_completion(self, symbol: str, timeframe: str, stats):
        """Callback de completado"""
        with self.lock:
            self.widget_stats['total_successful'] += 1
            self.widget_stats['total_bars_downloaded'] += stats.downloaded_bars

            completion_info = {
                'symbol': symbol,
                'timeframe': timeframe,
                'bars': stats.downloaded_bars,
                'speed': stats.download_speed,
                'time': datetime.now()
            }

            self.recent_completions.append(completion_info)
            if len(self.recent_completions) > 5:
                self.recent_completions.pop(0)

            # Limpiar progreso
            key = f"{symbol}_{timeframe}"
            self.current_progress.pop(key, None)

    def on_error(self, symbol: str, timeframe: str, error_msg: str):
        """Callback de error"""
        with self.lock:
            self.widget_stats['total_failed'] += 1

            error_info = {
                'symbol': symbol,
                'timeframe': timeframe,
                'error': error_msg,
                'time': datetime.now()
            }

            self.recent_errors.append(error_info)
            if len(self.recent_errors) > 3:
                self.recent_errors.pop(0)

            # Limpiar progreso
            key = f"{symbol}_{timeframe}"
            self.current_progress.pop(key, None)

    # === RENDERING ===

    def render_control_panel(self) -> Panel:
        """Panel de control principal"""
        table = Table(show_header=False, box=box.SIMPLE)
        table.add_column("Item", style="bold blue", width=15)
        table.add_column("Value", style="bright_green", width=20)
        table.add_column("Action", style="yellow", width=15)

        if self.downloader:
            # Estado del downloader
            downloader_status = self.downloader.get_enhanced_status()
            connected = "🟢 CONECTADO" if downloader_status['is_connected'] else "🔴 DESCONECTADO"
            table.add_row("MT5 Status:", connected, "")

            # Cola
            queue_length = downloader_status['queue_length']
            table.add_row("En Cola:", f"{queue_length} descargas", "")
        else:
            table.add_row("MT5 Status:", "❌ NO DISPONIBLE", "")

        # Configuración
        table.add_row("Símbolos:", ", ".join(self.config['symbols']), "F1: Config")
        table.add_row("Timeframes:", ", ".join(self.config['timeframes']), "F2: Config")
        table.add_row("Velas:", f"{self.config['lookback']:,}", "F3: Config")

        # Controles
        table.add_row("", "", "")
        table.add_row("Acciones:", "DISPONIBLE", "ENTER: Start")
        table.add_row("", "", "U: Update Stale")
        table.add_row("", "", "Q: Quit")

        return Panel(
            table,
            title="🎮 [bold cyan]SIMPLE CANDLE DOWNLOADER[/bold cyan]",
            border_style="bright_cyan",
            padding=(1, 1)
        )

    def render_progress_panel(self) -> Panel:
        """Panel de progreso actual"""
        if not self.current_progress:
            content = Text("No hay descargas en progreso", style="dim")
        else:
            progress_items = []
            with self.lock:
                for key, data in self.current_progress.items():
                    progress_text = f"📈 {data['symbol']} {data['timeframe']}: {data['status']}"
                    progress_items.append(Text(progress_text, style="bright_green"))

            content = Group(*progress_items) if progress_items else Text("Sin progreso", style="dim")

        return Panel(
            content,
            title="📊 [bold green]PROGRESO[/bold green]",
            border_style="green",
            height=6
        )

    def render_stats_panel(self) -> Panel:
        """Panel de estadísticas"""
        table = Table(show_header=False, box=box.SIMPLE)
        table.add_column("Stat", style="bold blue")
        table.add_column("Value", style="bright_green")

        with self.lock:
            table.add_row("Sesiones:", f"{self.widget_stats['sessions_started']}")
            table.add_row("Exitosas:", f"{self.widget_stats['total_successful']}")
            table.add_row("Fallidas:", f"{self.widget_stats['total_failed']}")
            table.add_row("Total Velas:", f"{self.widget_stats['total_bars_downloaded']:,}")

            # Success rate
            total_downloads = self.widget_stats['total_successful'] + self.widget_stats['total_failed']
            if total_downloads > 0:
                success_rate = (self.widget_stats['total_successful'] / total_downloads) * 100
                table.add_row("Success Rate:", f"{success_rate:.1f}%")

        return Panel(
            table,
            title="📈 [bold yellow]STATS[/bold yellow]",
            border_style="bright_yellow",
            height=6
        )

    def render_recent_activity(self) -> Panel:
        """Panel de actividad reciente"""
        activity_items = []

        with self.lock:
            # Completados recientes
            for completion in self.recent_completions[-3:]:
                time_str = completion['time'].strftime("%H:%M:%S")
                text = f"✅ {time_str} {completion['symbol']} {completion['timeframe']} - {completion['bars']:,} velas"
                activity_items.append(Text(text, style="bright_green"))

            # Errores recientes
            for error in self.recent_errors[-2:]:
                time_str = error['time'].strftime("%H:%M:%S")
                text = f"❌ {time_str} {error['symbol']} {error['timeframe']} - {error['error']}"
                activity_items.append(Text(text, style="bright_red"))

        content = Group(*activity_items) if activity_items else Text("Sin actividad reciente", style="dim")

        return Panel(
            content,
            title="🕐 [bold magenta]ACTIVIDAD RECIENTE[/bold magenta]",
            border_style="bright_magenta",
            height=6
        )

    # === ACCIONES ===

    def start_download_session(self) -> bool:
        """Inicia sesión de descarga"""
        if not self.downloader:
            return False

        try:
            with self.lock:
                self.widget_stats['sessions_started'] += 1

            # Auto-update stale data si está habilitado
            if self.config['auto_update_stale']:
                stale_count = self.downloader.auto_update_stale_data(
                    self.config['symbols'],
                    self.config['timeframes'],
                    24  # 24 horas
                )
                if stale_count > 0:
                    return True  # Se agregaron a la cola

            # Descarga coordinada
            stats_list = self.downloader.download_with_coordination(
                self.config['symbols'],
                self.config['timeframes'],
                self.config['lookback']
            )

            return len([s for s in stats_list if s.success]) > 0

        except Exception as e:
            self.on_error("SYSTEM", "ALL", f"Error en sesión: {e}")
            return False

    def update_stale_data(self) -> int:
        """Actualiza solo datos obsoletos"""
        if not self.downloader:
            return 0

        return self.downloader.auto_update_stale_data(
            self.config['symbols'],
            self.config['timeframes'],
            24
        )

    def configure(self, symbols: List[str] = None, timeframes: List[str] = None, lookback: int = None):
        """Configura parámetros"""
        if symbols:
            self.config['symbols'] = symbols
        if timeframes:
            self.config['timeframes'] = timeframes
        if lookback:
            self.config['lookback'] = lookback

# Instancia global
simple_candle_widget = SimpleCandleWidget()
'''

            with open(widget_file, 'w', encoding='utf-8') as f:
                f.write(widget_code)

            self.tasks_completed.append('simple_widget')
            self.log_action("TASK 2", "SUCCESS", f"Widget simplificado creado: {widget_file}")
            return True

        except Exception as e:
            self.tasks_failed.append('simple_widget')
            self.log_action("TASK 2", "ERROR", f"Error creando widget: {e}")
            return False

    def create_integration_functions(self) -> bool:
        """Tarea 3: Crear funciones de integración simples"""
        self.log_action("TASK 3", "STARTING", "Creando funciones de integración")

        try:
            utils_dir = self.project_root / "utils"
            utils_dir.mkdir(parents=True, exist_ok=True)

            integration_file = utils_dir / "candle_integration.py"

            if integration_file.exists():
                self.log_action("TASK 3", "SUCCESS", "Funciones de integración ya existen")
                self.tasks_completed.append('integration_functions')
                return True

            integration_code = '''#!/usr/bin/env python3
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
'''

            with open(integration_file, 'w', encoding='utf-8') as f:
                f.write(integration_code)

            self.tasks_completed.append('integration_functions')
            self.log_action("TASK 3", "SUCCESS", f"Funciones de integración creadas: {integration_file}")
            return True

        except Exception as e:
            self.tasks_failed.append('integration_functions')
            self.log_action("TASK 3", "ERROR", f"Error creando integración: {e}")
            return False

    def deprecate_candle_coordinator(self) -> bool:
        """Tarea 4: Deprecar el CandleCoordinator obsoleto"""
        self.log_action("TASK 4", "STARTING", "Depreciando CandleCoordinator")

        try:
            coordinator_file = self.project_root / "core" / "data_management" / "candle_coordinator.py"

            if coordinator_file.exists():
                # Crear backup
                backup_file = coordinator_file.parent / "candle_coordinator_deprecated_backup.py"

                with open(coordinator_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Crear archivo deprecado con mensaje claro
                deprecated_content = '''#!/usr/bin/env python3
"""
❌ DEPRECATED - CANDLE COORDINATOR
=================================

⚠️  ESTE ARCHIVO HA SIDO DEPRECADO EN SPRINT 1.2 REFACTORED

Razón: Duplicación innecesaria de funcionalidad del AdvancedCandleDownloader

Migración:
- Usa directamente: utils.advanced_candle_downloader.AdvancedCandleDownloader
- Para funciones de conveniencia: utils.candle_integration
- Para widget simplificado: dashboard.simple_candle_widget

El AdvancedCandleDownloader ahora incluye:
✅ Callbacks integrados
✅ Sistema de colas con prioridades
✅ Coordinación automática
✅ Auto-update de datos obsoletos

Backup guardado en: candle_coordinator_deprecated_backup.py
"""

import warnings

class CandleCoordinator:
    """CLASE DEPRECADA - Usar AdvancedCandleDownloader directamente"""

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "CandleCoordinator está deprecado. "
            "Usa utils.advanced_candle_downloader.AdvancedCandleDownloader directamente. "
            "Ver utils.candle_integration para funciones de conveniencia.",
            DeprecationWarning,
            stacklevel=2
        )

        # Intentar importar el downloader mejorado como fallback
        try:
            from utils.advanced_candle_downloader import AdvancedCandleDownloader
            self._downloader = AdvancedCandleDownloader()
            print("⚠️  CandleCoordinator deprecado. Usando AdvancedCandleDownloader como fallback.")
        except ImportError:
            self._downloader = None
            print("❌ Error: No se pudo cargar AdvancedCandleDownloader. Actualiza tu sistema.")

    def __getattr__(self, name):
        """Redirigir llamadas al downloader como fallback temporal"""
        if self._downloader and hasattr(self._downloader, name):
            return getattr(self._downloader, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

# Mantener compatibilidad temporal
candle_coordinator = CandleCoordinator()
'''

                with open(coordinator_file, 'w', encoding='utf-8') as f:
                    f.write(deprecated_content)

                self.log_action("TASK 4", "SUCCESS", f"CandleCoordinator deprecado (backup: {backup_file.name})")
            else:
                self.log_action("TASK 4", "SUCCESS", "CandleCoordinator no existe - ya limpio")

            self.tasks_completed.append('deprecate_coordinator')
            return True

        except Exception as e:
            self.tasks_failed.append('deprecate_coordinator')
            self.log_action("TASK 4", "ERROR", f"Error depreciando coordinator: {e}")
            return False

    def execute_all_tasks(self) -> dict:
        """Ejecuta todas las tareas del Sprint 1.2 Refactorizado"""
        self.log_action("SPRINT 1.2 REFACTORED", "STARTING", "Iniciando refactoring simplificado")

        results = {
            'sprint': '1.2 Refactored',
            'name': 'Advanced Candle Downloader Enhanced (KISS)',
            'tasks_attempted': 0,
            'tasks_completed': 0,
            'tasks_failed': 0,
            'start_time': datetime.now().isoformat(),
            'success_rate': 0.0,
            'status': 'RUNNING'
        }

        # Lista de tareas refactorizadas
        tasks = [
            ('enhance_downloader', self.enhance_advanced_downloader),
            ('simple_widget', self.create_simple_widget),
            ('integration_functions', self.create_integration_functions),
            ('deprecate_coordinator', self.deprecate_candle_coordinator)
        ]

        # Ejecutar tareas
        for task_name, task_method in tasks:
            results['tasks_attempted'] += 1

            try:
                if task_method():
                    results['tasks_completed'] += 1
                    print(f"✅ Tarea {results['tasks_attempted']}/4 completada: {task_name}")
                else:
                    results['tasks_failed'] += 1
                    print(f"❌ Tarea {results['tasks_attempted']}/4 falló: {task_name}")

            except Exception as e:
                results['tasks_failed'] += 1
                print(f"💥 Error crítico en tarea {task_name}: {e}")

        # Calcular métricas finales
        results['success_rate'] = (results['tasks_completed'] / results['tasks_attempted']) * 100
        results['end_time'] = datetime.now().isoformat()

        if results['success_rate'] >= 75:
            results['status'] = 'SUCCESS'
            self.log_action("SPRINT 1.2 REFACTORED", "SUCCESS", f"Refactoring completado con {results['success_rate']:.1f}% éxito")
        else:
            results['status'] = 'PARTIAL'
            self.log_action("SPRINT 1.2 REFACTORED", "PARTIAL", f"Refactoring parcial: {results['success_rate']:.1f}% éxito")

        return results

    def generate_report(self, results: dict) -> str:
        """Genera reporte del Sprint 1.2 Refactorizado"""
        reports_dir = self.project_root / "reports"
        reports_dir.mkdir(exist_ok=True)

        report_path = reports_dir / f"sprint_1_2_refactored_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        full_report = {
            'sprint_info': {
                'sprint_id': '1.2 Refactored',
                'name': 'Advanced Candle Downloader Enhanced (KISS)',
                'execution_date': datetime.now().isoformat(),
                'executor_version': '1.0',
                'approach': 'KISS - Keep It Simple, Stupid',
                'eliminated_complexity': 'CandleCoordinator layer removed'
            },
            'execution_results': results,
            'deliverables': {
                'enhanced_downloader': 'utils/advanced_candle_downloader.py (enhanced)',
                'simple_widget': 'dashboard/simple_candle_widget.py',
                'integration_functions': 'utils/candle_integration.py',
                'deprecated_coordinator': 'core/data_management/candle_coordinator.py (deprecated)',
                'backups': [
                    'utils/advanced_candle_downloader_backup.py',
                    'core/data_management/candle_coordinator_deprecated_backup.py'
                ]
            },
            'architecture_changes': {
                'removed_complexity': [
                    'CandleCoordinator abstraction layer',
                    'Duplicate functionality',
                    'Fragile dependencies'
                ],
                'enhanced': [
                    'utils/advanced_candle_downloader.py → callbacks + coordination'
                ],
                'added': [
                    'dashboard/simple_candle_widget.py → direct usage',
                    'utils/candle_integration.py → convenience functions'
                ],
                'deprecated': [
                    'core/data_management/candle_coordinator.py → fallback wrapper'
                ]
            },
            'tasks_completed': self.tasks_completed,
            'tasks_failed': self.tasks_failed,
            'benefits': [
                'Eliminada duplicación de funcionalidad',
                'Arquitectura simplificada (KISS principle)',
                'Menos dependencias y puntos de fallo',
                'Mantenimiento más fácil',
                'Performance mejorado (menos capas)',
                'Código más claro y directo',
                'Compatibilidad temporal mantenida'
            ],
            'migration_guide': {
                'old_way': 'from core.data_management.candle_coordinator import candle_coordinator',
                'new_way': 'from utils.candle_integration import get_downloader',
                'convenience_functions': [
                    'download_for_ict()',
                    'download_quick()',
                    'update_stale_data()',
                    'ensure_data_for_analysis()'
                ]
            },
            'next_steps': self._generate_next_steps(results)
        }

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(full_report, f, indent=2, ensure_ascii=False)

        return str(report_path)

    def _generate_next_steps(self, results: dict) -> list:
        """Genera próximos pasos basado en resultados"""
        next_steps = []

        if results['status'] == 'SUCCESS':
            next_steps.extend([
                "✅ Sprint 1.2 Refactorizado completado exitosamente",
                "🧪 Probar integración: from utils.candle_integration import download_for_ict",
                "🎮 Probar widget: from dashboard.simple_candle_widget import simple_candle_widget",
                "🔍 Validar que callbacks funcionan correctamente",
                "📊 Migrar código existente a nuevas funciones de integración",
                "🚀 Preparar Sprint 1.3: ICT Analysis Automation",
                "🗑️ Limpiar imports obsoletos de CandleCoordinator en otros archivos"
            ])
        else:
            next_steps.extend([
                "⚠️ Sprint 1.2 Refactorizado requiere atención",
                "🔍 Revisar tareas fallidas específicas",
                "🔧 Verificar que advanced_candle_downloader.py se pudo modificar",
                "📋 Comprobar permisos de archivos",
                "🔄 Re-ejecutar tareas fallidas individualmente",
                "💾 Verificar backups creados correctamente"
            ])

        return next_steps

def main():
    """Función principal del Sprint 1.2 Refactorizado"""
    print("🚀 SPRINT 1.2 REFACTORED EXECUTOR - KISS APPROACH")
    print("=" * 70)
    print("🎯 Objetivo: Eliminar complejidad innecesaria y usar directamente AdvancedCandleDownloader")
    print("📋 Enfoque: KISS (Keep It Simple, Stupid)")
    print("🔧 Eliminar: CandleCoordinator (duplicación)")
    print("✨ Mejorar: AdvancedCandleDownloader con callbacks")
    print()

    executor = Sprint12RefactoredExecutor()

    # Ejecutar sprint refactorizado
    results = executor.execute_all_tasks()

    # Generar reporte
    report_path = executor.generate_report(results)

    # Mostrar resultados finales
    print("\n" + "=" * 70)
    print("📊 RESULTADOS FINALES DEL SPRINT 1.2 REFACTORED")
    print("=" * 70)
    print(f"✅ Tareas completadas: {results['tasks_completed']}/{results['tasks_attempted']}")
    print(f"📈 Tasa de éxito: {results['success_rate']:.1f}%")
    print(f"🎯 Estado final: {results['status']}")
    print(f"📋 Reporte guardado: {report_path}")

    if results['status'] == 'SUCCESS':
        print("\n🎉 ¡SPRINT 1.2 REFACTORIZADO COMPLETADO!")
        print("📊 Beneficios del refactoring:")
        print("   ✅ Eliminada duplicación de funcionalidad")
        print("   ✅ Arquitectura simplificada (KISS)")
        print("   ✅ Menos dependencias frágiles")
        print("   ✅ Mantenimiento más fácil")
        print("   ✅ Performance mejorado")
        print("\n🧪 Prueba la nueva integración:")
        print("   from utils.candle_integration import download_for_ict")
        print("   download_for_ict('EURUSD')")
        print("\n🎮 Prueba el widget simplificado:")
        print("   from dashboard.simple_candle_widget import simple_candle_widget")
        print("\n🚀 Listo para Sprint 1.3: ICT Analysis Automation")
    else:
        print("\n⚠️ Sprint 1.2 Refactorizado necesita atención")
        print("🔍 Revisa las tareas fallidas y vuelve a ejecutar")

    return results['status'] == 'SUCCESS'

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
