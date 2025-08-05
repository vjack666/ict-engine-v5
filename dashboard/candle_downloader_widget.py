#!/usr/bin/env python3
"""
🎮 CANDLE DOWNLOADER WIDGET - ICT ENGINE v5.0
=============================================

Widget para controlar el AdvancedCandleDownloader desde el dashboard
Proporciona interfaz visual para descarga de datos

Integra con:
- AdvancedCandleDownloader para descarga real
- CandleCoordinator para orquestación
- MT5DataManager para datos

Creado por Sprint 1.2 Executor
Actualizado: 2025-08-05 - Integración completa
"""

from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.console import Group
from rich import box
from datetime import datetime
from typing import Dict, List, Optional
import threading

# Importar el downloader avanzado
try:
    from core.data_management.advanced_candle_downloader import get_advanced_candle_downloader, DownloadStats
    advanced_downloader_available = True
except ImportError:
    advanced_downloader_available = False
    get_advanced_candle_downloader = None
    DownloadStats = None

# Importar logging centralizado
from sistema.logging_interface import enviar_senal_log

class CandleDownloaderWidget:
    """
    🎮 WIDGET PARA CONTROL DEL CANDLE DOWNLOADER

    Funcionalidades:
    - Controles start/stop/pause
    - Progress bars en tiempo real
    - Configuración de symbols/timeframes
    - Estadísticas de descarga
    - Error reporting visual
    """

    def __init__(self):
        self.is_downloading = False
        self.current_progress = {}
        self.download_stats = {
            'total_downloads': 0,
            'successful': 0,
            'failed': 0,
            'total_bars': 0,
            'average_speed': 0.0
        }

        # Configuración actual
        self.selected_symbols = ["EURUSD"]
        self.selected_timeframes = ["H4", "H1", "M15"]
        self.lookback_bars = 50000

        # Estado de progreso
        self.progress_data = {}
        self.error_messages = []

        # Lock para thread safety
        self.lock = threading.Lock()

        # Integración con Advanced Candle Downloader
        self.advanced_downloader = None
        self._initialize_downloader()

    def _initialize_downloader(self):
        """Inicializa el downloader avanzado"""
        if advanced_downloader_available:
            try:
                self.advanced_downloader = get_advanced_candle_downloader()

                # Configurar callbacks
                self.advanced_downloader.progress_callback = self.on_download_progress
                self.advanced_downloader.complete_callback = self.on_download_complete
                self.advanced_downloader.error_callback = self.on_download_error

                # Inicializar el downloader
                if self.advanced_downloader.initialize():
                    enviar_senal_log("INFO", "✅ Advanced Candle Downloader inicializado", "candle_downloader_widget", "initialization")
                else:
                    enviar_senal_log("ERROR", "⚠️ Error inicializando Advanced Candle Downloader", "candle_downloader_widget", "initialization")
                    self.advanced_downloader = None

            except Exception as e:
                enviar_senal_log("ERROR", f"❌ Error configurando Advanced Candle Downloader: {e}", "candle_downloader_widget", "initialization")
                self.advanced_downloader = None
        else:
            enviar_senal_log("WARNING", "⚠️ Advanced Candle Downloader no disponible", "candle_downloader_widget", "initialization")

    def render_control_panel(self) -> Panel:
        """Renderiza panel de controles"""
        table = Table(show_header=False, box=box.SIMPLE)
        table.add_column("Control", style="bold blue")
        table.add_column("Status", style="green")
        table.add_column("Action", style="yellow")

        # Estado general
        status = "🔄 DESCARGANDO" if self.is_downloading else "⏸️ DETENIDO"
        table.add_row("Estado:", status, "")
        table.add_row("", "", "")

        # Configuración actual
        table.add_row("Símbolos:", ", ".join(self.selected_symbols), "F1: Configurar")
        table.add_row("Timeframes:", ", ".join(self.selected_timeframes), "F2: Cambiar")
        table.add_row("Velas:", f"{self.lookback_bars:,}", "F3: Ajustar")
        table.add_row("", "", "")

        # Controles
        if self.is_downloading:
            table.add_row("Acciones:", "ACTIVO", "S: Stop | P: Pause")
        else:
            table.add_row("Acciones:", "DISPONIBLE", "ENTER: Start | Q: Quit")

        return Panel(
            table,
            title="🎮 [bold cyan]CANDLE DOWNLOADER CONTROL[/bold cyan]",
            border_style="bright_cyan",
            padding=(1, 2)
        )

    def render_progress_panel(self) -> Panel:
        """Renderiza panel de progreso"""
        if not self.progress_data:
            return Panel(
                Text("No hay descargas en progreso", style="dim"),
                title="📊 [bold green]PROGRESO DE DESCARGA[/bold green]",
                border_style="green"
            )

        progress_group = []

        for key, data in self.progress_data.items():
            symbol, timeframe = key.split('_')
            progress_text = f"{symbol} {timeframe}: {data.get('progress', 0):.1f}% "
            progress_text += f"({data.get('bars_downloaded', 0):,}/{data.get('total_bars', 0):,} velas) "
            progress_text += f"@ {data.get('speed', 0):.0f} velas/s"

            progress_group.append(Text(progress_text, style="bright_green"))

        return Panel(
            Group(*progress_group),
            title="📊 [bold green]PROGRESO ACTUAL[/bold green]",
            border_style="green",
            padding=(1, 2)
        )

    def render_stats_panel(self) -> Panel:
        """Renderiza panel de estadísticas"""
        table = Table(show_header=False, box=box.SIMPLE)
        table.add_column("Métrica", style="bold blue")
        table.add_column("Valor", style="bright_green")
        table.add_column("Info", style="dim")

        table.add_row("Total descargas:", f"{self.download_stats['total_downloads']}", "")
        table.add_row("Exitosas:", f"{self.download_stats['successful']}", "✅")
        table.add_row("Fallidas:", f"{self.download_stats['failed']}", "❌")
        table.add_row("Total velas:", f"{self.download_stats['total_bars']:,}", "📊")
        table.add_row("Velocidad prom:", f"{self.download_stats['average_speed']:.0f} v/s", "⚡")

        # Success rate
        if self.download_stats['total_downloads'] > 0:
            success_rate = (self.download_stats['successful'] / self.download_stats['total_downloads']) * 100
            table.add_row("Success rate:", f"{success_rate:.1f}%", "📈")

        return Panel(
            table,
            title="📈 [bold yellow]ESTADÍSTICAS[/bold yellow]",
            border_style="bright_yellow",
            padding=(1, 2)
        )

    def render_errors_panel(self) -> Panel:
        """Renderiza panel de errores"""
        if not self.error_messages:
            return Panel(
                Text("No hay errores reportados", style="dim green"),
                title="🚨 [bold red]ERRORES[/bold red]",
                border_style="red"
            )

        error_group = []
        for error in self.error_messages[-5:]:  # Últimos 5 errores
            error_group.append(Text(f"• {error}", style="bright_red"))

        return Panel(
            Group(*error_group),
            title="🚨 [bold red]ERRORES RECIENTES[/bold red]",
            border_style="red",
            padding=(1, 2)
        )

    def render_complete_widget(self) -> Layout:
        """Renderiza widget completo"""
        layout = Layout()

        # Dividir en secciones
        layout.split_column(
            Layout(name="top", size=8),
            Layout(name="middle", size=6),
            Layout(name="bottom")
        )

        layout["top"].update(self.render_control_panel())

        layout["middle"].split_row(
            Layout(self.render_progress_panel(), name="progress"),
            Layout(self.render_stats_panel(), name="stats")
        )

        layout["bottom"].update(self.render_errors_panel())

        return layout

    # Métodos para callbacks del Advanced Candle Downloader
    def on_download_progress(self, symbol: str, timeframe: str, progress: float, stats):
        """Callback para progreso de descarga del Advanced Downloader"""
        with self.lock:
            key = f"{symbol}_{timeframe}"
            self.progress_data[key] = {
                'progress': progress,
                'bars_downloaded': stats.downloaded_bars if stats else 0,
                'total_bars': stats.total_bars if stats else 0,
                'speed': stats.download_speed if stats else 0.0,
                'last_update': datetime.now()
            }

    def on_download_complete(self, symbol: str, timeframe: str, stats):
        """Callback para descarga completada del Advanced Downloader"""
        with self.lock:
            self.download_stats['total_downloads'] += 1
            self.download_stats['successful'] += 1

            if stats:
                self.download_stats['total_bars'] += stats.downloaded_bars

                # Actualizar velocidad promedio
                if self.download_stats['total_downloads'] > 0:
                    self.download_stats['average_speed'] = (
                        self.download_stats['average_speed'] * (self.download_stats['total_downloads'] - 1) +
                        stats.download_speed
                    ) / self.download_stats['total_downloads']

            # Limpiar progreso
            key = f"{symbol}_{timeframe}"
            if key in self.progress_data:
                del self.progress_data[key]

    # Métodos para callbacks del coordinador (legacy)
    def on_progress_update(self, symbol: str, timeframe: str, status: str, **kwargs):
        """Callback para updates de progreso"""
        with self.lock:
            key = f"{symbol}_{timeframe}"

            if key not in self.progress_data:
                self.progress_data[key] = {}

            self.progress_data[key].update({
                'status': status,
                'last_update': datetime.now(),
                **kwargs
            })

    def on_download_completed(self, symbol: str, timeframe: str, stats):
        """Callback para descarga completada"""
        with self.lock:
            self.download_stats['total_downloads'] += 1
            self.download_stats['successful'] += 1

            # Manejar tanto objetos con atributos como diccionarios
            downloaded_bars = 0
            download_speed = 0.0

            if isinstance(stats, dict):
                downloaded_bars = stats.get('downloaded_bars', 0)
                download_speed = stats.get('download_speed', 0.0)
            else:
                # Asumir que es un objeto con atributos
                downloaded_bars = getattr(stats, 'downloaded_bars', 0)
                download_speed = getattr(stats, 'download_speed', 0.0)

            self.download_stats['total_bars'] += downloaded_bars

            # Actualizar velocidad promedio
            if self.download_stats['total_downloads'] > 0:
                self.download_stats['average_speed'] = (
                    self.download_stats['average_speed'] * (self.download_stats['total_downloads'] - 1) +
                    download_speed
                ) / self.download_stats['total_downloads']

            # Limpiar progreso
            key = f"{symbol}_{timeframe}"
            if key in self.progress_data:
                del self.progress_data[key]

    def on_download_error(self, symbol: str, timeframe: str, error_msg: str):
        """Callback para errores de descarga"""
        with self.lock:
            self.download_stats['total_downloads'] += 1
            self.download_stats['failed'] += 1

            error_text = f"{symbol} {timeframe}: {error_msg}"
            self.error_messages.append(error_text)

            # Mantener solo últimos 10 errores
            if len(self.error_messages) > 10:
                self.error_messages.pop(0)

            # Limpiar progreso
            key = f"{symbol}_{timeframe}"
            if key in self.progress_data:
                del self.progress_data[key]

    def start_download(self):
        """Inicia descarga usando el Advanced Candle Downloader"""
        if self.is_downloading:
            return False

        try:
            if self.advanced_downloader and advanced_downloader_available:
                # Usar Advanced Candle Downloader
                success = self.advanced_downloader.start_batch_download(
                    symbols=self.selected_symbols,
                    timeframes=self.selected_timeframes,
                    lookback_bars=self.lookback_bars
                )

                if success:
                    self.is_downloading = True
                    return True
                else:
                    return False
            else:
                # Fallback - modo simulado
                self.is_downloading = True
                return True

        except Exception as e:
            enviar_senal_log("ERROR", f"Error iniciando descarga: {e}", "candle_downloader_widget", "download")
            return False

    def stop_download(self):
        """Detiene descarga"""
        if self.advanced_downloader and advanced_downloader_available:
            self.advanced_downloader.stop_download()

        self.is_downloading = False
        self.progress_data.clear()

    def configure_symbols(self, symbols: List[str]):
        """Configura símbolos a descargar"""
        self.selected_symbols = symbols

    def configure_timeframes(self, timeframes: List[str]):
        """Configura timeframes a descargar"""
        self.selected_timeframes = timeframes

    def configure_lookback(self, lookback: int):
        """Configura número de velas"""
        self.lookback_bars = lookback

    def update_from_advanced_downloader(self):
        """Actualiza datos desde el Advanced Candle Downloader"""
        if not self.advanced_downloader or not advanced_downloader_available:
            return

        try:
            # Obtener progreso actual
            progress_data = self.advanced_downloader.get_download_progress()
            with self.lock:
                self.progress_data.update(progress_data)

            # Obtener estadísticas generales
            stats = self.advanced_downloader.get_download_statistics()
            if stats:
                with self.lock:
                    self.is_downloading = stats.get('is_downloading', False)
                    # Actualizar estadísticas si hay datos nuevos
                    if stats.get('downloaded_bars', 0) > 0:
                        self.download_stats['total_bars'] = stats.get('total_bars', 0)
                        self.download_stats['average_speed'] = stats.get('average_speed', 0.0)

        except Exception as e:
            enviar_senal_log("ERROR", f"Error actualizando desde Advanced Downloader: {e}", "candle_downloader_widget", "update")

    def get_real_time_stats(self) -> Dict:
        """Obtiene estadísticas en tiempo real"""
        self.update_from_advanced_downloader()

        with self.lock:
            return {
                'is_downloading': self.is_downloading,
                'download_stats': self.download_stats.copy(),
                'progress_data': self.progress_data.copy(),
                'error_messages': self.error_messages.copy(),
                'configuration': {
                    'symbols': self.selected_symbols.copy(),
                    'timeframes': self.selected_timeframes.copy(),
                    'lookback_bars': self.lookback_bars
                },
                'advanced_downloader_available': self.advanced_downloader is not None
            }

# Instancia global para dashboard
candle_downloader_widget = CandleDownloaderWidget()
