#!/usr/bin/env python3
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
    
    def get_status(self) -> Dict:
        """Obtiene el estado actual del downloader"""
        if not self.downloader:
            return {"error": "Downloader no disponible"}
        
        # Usar el nuevo método enhanced_status del downloader
        enhanced_status = self.downloader.get_enhanced_status()
        
        # Añadir información específica del widget
        widget_status = {
            'widget': 'SimpleCandleWidget',
            'config': self.config.copy(),
            'session_active': getattr(self, 'session_active', False),
            'downloader_status': enhanced_status
        }
        
        return widget_status

# Instancia global
simple_candle_widget = SimpleCandleWidget()
