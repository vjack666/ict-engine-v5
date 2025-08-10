#!/usr/bin/env python3
"""
🔴 PROGRESS DASHBOARD INSTRUMENTADO CON BLACKBOX LOGGER
================================================================================
Version instrumentada del dashboard simple con logging ultra detallado
para diagnosticar exactamente por qué las pestañas no muestran contenido.

🎯 OBJETIVO: Detectar el problema específico de las velas/pestañas
🔍 INSTRUMENTACIÓN: Todos los métodos render_* y UI están monitoreados
================================================================================
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Rich imports for beautiful UI
from rich.console import Console

# Textual imports for tabbed interface
try:
    from textual.app import App, ComposeResult
    from textual.containers import Container
    from textual.widgets import Header, Footer, Static, Button, TabbedContent, TabPane
    from textual.binding import Binding
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False
    print("⚠️ Textual no disponible, usando modo Rich simple")

# Add core modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importar BlackBox Logger
try:
    from ict_dashboard_blackbox_logger import (
        bb_track_function, bb_track_render, bb_track_ui, 
        bb_track_data, bb_track_error, bb_track_tab, bb_generate_report,
        ict_blackbox
    )
    BLACKBOX_AVAILABLE = True
    print("🔴 BlackBox Logger cargado correctamente")
except ImportError as e:
    BLACKBOX_AVAILABLE = False
    print(f"❌ Error cargando BlackBox Logger: {e}")
    
    # Crear funciones dummy
    def bb_track_function(*args, **kwargs): pass
    def bb_track_render(*args, **kwargs): pass
    def bb_track_ui(*args, **kwargs): pass
    def bb_track_data(*args, **kwargs): pass
    def bb_track_error(*args, **kwargs): pass
    def bb_track_tab(*args, **kwargs): pass
    def bb_generate_report(): return None

@dataclass
class ModuleProgress:
    """Progreso de un módulo ICT"""
    name: str
    icon: str
    status: str = "PENDING"
    files_processed: int = 0
    total_files: int = 0
    signals_found: int = 0

class ProgressDashboard:
    """Dashboard de progreso básico INSTRUMENTADO"""
    
    def __init__(self):
        bb_track_function("ProgressDashboard.__init__")
        try:
            self.console = Console()
            self.session_id = f"ICT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.start_time = time.time()
            self.total_files = 24
            
            # Crear módulos de ejemplo
            self.modules = {
                "pattern_detector": ModuleProgress("Pattern Detector", "🔍", "COMPLETED", 24, 24, 12),
                "bos_detector": ModuleProgress("BOS Detector", "📈", "COMPLETED", 24, 24, 8),
                "choch_detector": ModuleProgress("CHOCH Detector", "🔄", "PROCESSING", 18, 24, 15),
                "breaker_blocks": ModuleProgress("Breaker Blocks", "🧱", "PROCESSING", 12, 24, 6),
                "silver_bullet": ModuleProgress("Silver Bullet", "🎯", "PENDING", 0, 24, 0),
                "liquidity_analysis": ModuleProgress("Liquidity Analysis", "💧", "PENDING", 0, 24, 0)
            }
            
            bb_track_ui("dashboard", "initialization", {"modules_count": len(self.modules)}, True)
            bb_track_data("dashboard_init", self.modules, f"session: {self.session_id}")
            
        except Exception as e:
            bb_track_error(e, "ProgressDashboard.__init__")
            raise
    
    def get_overall_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas generales INSTRUMENTADO"""
        bb_track_function("get_overall_stats")
        
        try:
            start_time = time.time()
            
            completed = len([m for m in self.modules.values() if m.status == "COMPLETED"])
            processing = len([m for m in self.modules.values() if m.status == "PROCESSING"])
            pending = len([m for m in self.modules.values() if m.status == "PENDING"])
            
            total_signals = sum(m.signals_found for m in self.modules.values())
            total_processed = sum(m.files_processed for m in self.modules.values())
            
            stats = {
                "total_modules": len(self.modules),
                "completed": completed,
                "processing": processing,
                "pending": pending,
                "total_signals": total_signals,
                "total_processed": total_processed,
                "completion_rate": (completed / len(self.modules)) * 100 if self.modules else 0
            }
            
            execution_time = time.time() - start_time
            bb_track_data("overall_stats", stats, f"execution_time: {execution_time:.3f}s")
            bb_track_function("get_overall_stats", result="success", execution_time=execution_time)
            
            return stats
            
        except Exception as e:
            bb_track_error(e, "get_overall_stats")
            return {}

class ProgressDashboardApp(App[None]):
    """Aplicación Textual INSTRUMENTADA"""
    
    CSS = """
    TabbedContent {
        height: 100%;
    }
    
    TabPane {
        padding: 1 2;
    }
    
    Static {
        height: 100%;
        overflow: auto;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("ctrl+s", "start_analysis", "Start Analysis"),
        Binding("ctrl+e", "export_report", "Export Report"),
    ]
    
    def __init__(self):
        bb_track_function("ProgressDashboardApp.__init__")
        try:
            super().__init__()
            self.dashboard = ProgressDashboard()
            bb_track_ui("textual_app", "initialization", {"dashboard_ready": True}, True)
        except Exception as e:
            bb_track_error(e, "ProgressDashboardApp.__init__")
            raise
    
    def compose(self) -> ComposeResult:
        """Crear la interfaz INSTRUMENTADA"""
        bb_track_function("compose")
        bb_track_ui("compose", "start", {"action": "creating_interface"}, True)
        
        try:
            yield Header()
            
            with TabbedContent(initial="overview"):
                with TabPane("📊 Overview", id="overview"):
                    yield Static(id="overview_display")
                
                with TabPane("🔍 Modules", id="modules"):
                    yield Static(id="modules_display")
                
                with TabPane("📈 Performance", id="performance"):
                    yield Static(id="performance_display")
                
                with TabPane("📋 Reports", id="reports"):
                    yield Static(id="reports_display")
            
            yield Footer()
            
            bb_track_ui("compose", "success", {"tabs_created": 4}, True)
            
        except Exception as e:
            bb_track_error(e, "compose method")
            bb_track_ui("compose", "failed", {"error": str(e)}, False, str(e))
            raise
    
    def on_mount(self) -> None:
        """Al montar la aplicación INSTRUMENTADO"""
        bb_track_function("on_mount")
        try:
            bb_track_ui("mount", "start", {"action": "initial_render"}, True)
            self.refresh_all_displays()
            bb_track_ui("mount", "completed", {"displays_refreshed": True}, True)
        except Exception as e:
            bb_track_error(e, "on_mount")
            bb_track_ui("mount", "failed", {"error": str(e)}, False, str(e))
    
    def render_overview(self) -> str:
        """Renderizar overview INSTRUMENTADO"""
        bb_track_function("render_overview")
        
        try:
            start_time = time.time()
            
            bb_track_ui("overview_tab", "render_start", {
                "modules_count": len(self.dashboard.modules)
            }, True)
            
            stats = self.dashboard.get_overall_stats()
            elapsed = time.time() - self.dashboard.start_time
            
            # Log datos de entrada
            bb_track_data("overview_input", stats, f"elapsed: {elapsed:.1f}s")
            
            content = f"""[bold cyan]🔧 ICT ENGINE PROGRESS DASHBOARD[/bold cyan]

[bold white]SESSION INFO:[/bold white]
• Session: [bold blue]{self.dashboard.session_id}[/bold blue]
• Running time: [bold green]{elapsed:.1f}s[/bold green]
• Total modules: [bold]{stats['total_modules']}[/bold]

[bold white]PROGRESS SUMMARY:[/bold white]
• ✅ Completed: [bold green]{stats['completed']}[/bold green]
• 🔄 Processing: [bold yellow]{stats['processing']}[/bold yellow]
• ⏳ Pending: [bold red]{stats['pending']}[/bold red]
• 📊 Completion: [bold blue]{stats['completion_rate']:.1f}%[/bold blue]

[bold white]ANALYSIS RESULTS:[/bold white]
• Total signals found: [bold green]{stats['total_signals']}[/bold green]
• Files processed: [bold blue]{stats['total_processed']}/{self.dashboard.total_files * len(self.dashboard.modules)}[/bold blue]
• Processing rate: [bold green]{stats['total_processed'] / elapsed if elapsed > 0 else 0:.1f} files/sec[/bold green]

[bold red]🔴 BLACKBOX OVERVIEW DEBUG:[/bold red]
• Session: {ict_blackbox.session_id if BLACKBOX_AVAILABLE else 'N/A'}
• Events tracked: {sum(ict_blackbox.counters.values()) if BLACKBOX_AVAILABLE else 'N/A'}
• Render time: {time.time() - start_time:.3f}s

[bold green]🎯 OVERVIEW TAB RENDERED SUCCESSFULLY[/bold green]

[bold white]NAVIGATION:[/bold white]
• Tab 1: 📊 Overview (current)
• Tab 2: 🔍 Modules details
• Tab 3: 📈 Performance metrics
• Tab 4: 📋 Reports & export
• R: Refresh all data
• Ctrl+S: Start analysis
• Ctrl+E: Export report
• Q: Quit"""

            execution_time = time.time() - start_time
            bb_track_render("render_overview", content[:200], True, None, len(content))
            bb_track_tab("overview", "render_overview", True, len(content))
            bb_track_function("render_overview", result="success", execution_time=execution_time)
            
            return content
            
        except Exception as e:
            bb_track_error(e, "render_overview")
            bb_track_render("render_overview", None, False, str(e), 0)
            bb_track_tab("overview", "render_overview", False, 0, str(e))
            return f"[bold red]ERROR OVERVIEW: {str(e)}[/bold red]"
    
    def render_modules(self) -> str:
        """Renderizar módulos INSTRUMENTADO"""
        bb_track_function("render_modules")
        
        try:
            start_time = time.time()
            
            bb_track_ui("modules_tab", "render_start", {
                "modules_to_process": len(self.dashboard.modules)
            }, True)
            
            content = """[bold cyan]🔍 ICT MODULES DETAILED STATUS[/bold cyan]

[bold white]MODULE STATUS TABLE:[/bold white]
┌─────────────────────┬─────────────┬─────────────┬─────────────┐
│ Module              │ Status      │ Progress    │ Signals     │
├─────────────────────┼─────────────┼─────────────┼─────────────┤"""
            
            modules_processed = 0
            for module in self.dashboard.modules.values():
                try:
                    # Colores según estado
                    if module.status == "COMPLETED":
                        status_color = "bold green"
                        status_text = "✅ DONE"
                    elif module.status == "PROCESSING":
                        status_color = "bold yellow" 
                        status_text = "🔄 PROC"
                    else:
                        status_color = "dim"
                        status_text = "⏳ PEND"
                    
                    progress_pct = (module.files_processed / module.total_files) * 100 if module.total_files > 0 else 0
                    progress_color = "bold green" if progress_pct >= 100 else "yellow" if progress_pct >= 50 else "red"
                    
                    content += f"""
│ {module.icon} {module.name:<17} │ [{status_color}]{status_text:<9}[/{status_color}] │ [{progress_color}]{module.files_processed:>2}/{module.total_files:<2} ({progress_pct:>5.1f}%)[/{progress_color}] │ [bold blue]{module.signals_found:>9}[/bold blue] │"""
                    
                    modules_processed += 1
                    
                except Exception as module_error:
                    bb_track_error(module_error, f"Processing module {module.name}")
                    content += f"""
│ ❌ {module.name:<17} │ [red]ERROR[/red]    │ [red]   ERROR[/red]   │ [red]    N/A[/red] │"""
            
            content += f"""
└─────────────────────┴─────────────┴─────────────┴─────────────┘

[bold white]MODULE DESCRIPTIONS:[/bold white]
• 🔍 Pattern Detector: Basic ICT pattern recognition
• 📈 BOS Detector: Break of Structure identification  
• 🔄 CHOCH Detector: Change of Character detection
• 🧱 Breaker Blocks: Breaker block analysis
• 🎯 Silver Bullet: Silver bullet setup detection
• 💧 Liquidity Analysis: Liquidity pool analysis

[bold red]🔴 BLACKBOX MODULES DEBUG:[/bold red]
• Modules processed: {modules_processed}/{len(self.dashboard.modules)}
• Render time: {time.time() - start_time:.3f}s
• Errors detected: {ict_blackbox.counters['errors'] if BLACKBOX_AVAILABLE else 'N/A'}

[bold green]🎯 MODULES TAB RENDERED SUCCESSFULLY[/bold green]"""
            
            execution_time = time.time() - start_time
            bb_track_render("render_modules", content[:200], True, None, len(content))
            bb_track_tab("modules", "render_modules", True, len(content))
            bb_track_function("render_modules", result="success", execution_time=execution_time)
            
            return content
            
        except Exception as e:
            bb_track_error(e, "render_modules")
            bb_track_render("render_modules", None, False, str(e), 0)
            bb_track_tab("modules", "render_modules", False, 0, str(e))
            return f"[bold red]ERROR MODULES: {str(e)}[/bold red]"
    
    def render_performance(self) -> str:
        """Renderizar performance INSTRUMENTADO"""
        bb_track_function("render_performance")
        
        try:
            start_time = time.time()
            
            elapsed = time.time() - self.dashboard.start_time
            stats = self.dashboard.get_overall_stats()
            
            content = f"""[bold cyan]📈 PERFORMANCE METRICS[/bold cyan]

[bold white]SYSTEM PERFORMANCE:[/bold white]
• Session duration: [bold green]{elapsed:.1f}s[/bold green]
• Processing speed: [bold blue]{stats['total_processed'] / elapsed if elapsed > 0 else 0:.2f} files/sec[/bold blue]
• Total throughput: [bold green]{stats['total_signals']} signals[/bold green]
• Success rate: [bold green]{(stats['completed'] / stats['total_modules']) * 100 if stats['total_modules'] > 0 else 0:.1f}%[/bold green]

[bold white]MEMORY & RESOURCES:[/bold white]
• Active modules: [bold blue]{stats['total_modules']}[/bold blue]
• Processing threads: [bold green]Active[/bold green]
• Memory usage: [bold green]Normal[/bold green]

[bold red]🔴 BLACKBOX PERFORMANCE METRICS:[/bold red]
• Function calls tracked: {ict_blackbox.counters['function_calls'] if BLACKBOX_AVAILABLE else 'N/A'}
• UI events tracked: {ict_blackbox.counters['ui_events'] if BLACKBOX_AVAILABLE else 'N/A'}
• Renders successful: {ict_blackbox.counters['renders_success'] if BLACKBOX_AVAILABLE else 'N/A'}
• Renders failed: {ict_blackbox.counters['renders_failed'] if BLACKBOX_AVAILABLE else 'N/A'}
• Total errors logged: {ict_blackbox.counters['errors'] if BLACKBOX_AVAILABLE else 'N/A'}

[bold green]📊 PERFORMANCE TAB RENDERED SUCCESSFULLY[/bold green]"""

            execution_time = time.time() - start_time
            bb_track_render("render_performance", content[:200], True, None, len(content))
            bb_track_tab("performance", "render_performance", True, len(content))
            bb_track_function("render_performance", result="success", execution_time=execution_time)
            
            return content
            
        except Exception as e:
            bb_track_error(e, "render_performance")
            bb_track_render("render_performance", None, False, str(e), 0)
            bb_track_tab("performance", "render_performance", False, 0, str(e))
            return f"[bold red]ERROR PERFORMANCE: {str(e)}[/bold red]"
    
    def render_reports(self) -> str:
        """Renderizar reports INSTRUMENTADO"""
        bb_track_function("render_reports")
        
        try:
            start_time = time.time()
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            content = f"""[bold cyan]📋 REPORTS & EXPORT[/bold cyan]

[bold white]SESSION INFORMATION:[/bold white]
• Session ID: [bold blue]{self.dashboard.session_id}[/bold blue]
• Timestamp: [bold green]{timestamp}[/bold green]
• Duration: [bold blue]{time.time() - self.dashboard.start_time:.0f} seconds[/bold blue]

[bold red]🔴 BLACKBOX LOGGING REPORTS:[/bold red]
• BlackBox Session: [bold blue]{ict_blackbox.session_id if BLACKBOX_AVAILABLE else 'N/A'}[/bold blue]
• Events captured: [bold green]{sum(ict_blackbox.counters.values()) if BLACKBOX_AVAILABLE else 'N/A'}[/bold green]
• Errors detected: [bold red]{ict_blackbox.counters['errors'] if BLACKBOX_AVAILABLE else 'N/A'}[/bold red]
• Renders successful: [bold green]{ict_blackbox.counters['renders_success'] if BLACKBOX_AVAILABLE else 'N/A'}[/bold green]
• Renders failed: [bold red]{ict_blackbox.counters['renders_failed'] if BLACKBOX_AVAILABLE else 'N/A'}[/bold red]

[bold white]AVAILABLE ACTIONS:[/bold white]
• Ctrl+E: Export standard report
• Ctrl+B: Generate BlackBox debug report
• Export performance metrics
• Export module status (JSON)

[bold white]LOG LOCATIONS:[/bold white]
• Standard logs: logs/
• BlackBox logs: logs/blackbox/{ict_blackbox.session_id if BLACKBOX_AVAILABLE else 'N/A'}/
• Debug reports: logs/blackbox/*/COMPREHENSIVE_DEBUG_REPORT.json

[bold green]💾 REPORTS TAB RENDERED SUCCESSFULLY[/bold green]"""

            execution_time = time.time() - start_time
            bb_track_render("render_reports", content[:200], True, None, len(content))
            bb_track_tab("reports", "render_reports", True, len(content))
            bb_track_function("render_reports", result="success", execution_time=execution_time)
            
            return content
            
        except Exception as e:
            bb_track_error(e, "render_reports")
            bb_track_render("render_reports", None, False, str(e), 0)
            bb_track_tab("reports", "render_reports", False, 0, str(e))
            return f"[bold red]ERROR REPORTS: {str(e)}[/bold red]"
    
    def refresh_all_displays(self) -> None:
        """Actualizar todas las pantallas INSTRUMENTADO"""
        bb_track_function("refresh_all_displays")
        
        try:
            bb_track_ui("refresh", "start", {"action": "refresh_all_displays"}, True)
            
            # Overview
            try:
                overview_display = self.query_one("#overview_display", Static)
                overview_display.update(self.render_overview())
                bb_track_ui("overview_display", "update", {"status": "success"}, True)
            except Exception as e:
                bb_track_error(e, "refresh_overview_display")
            
            # Modules
            try:
                modules_display = self.query_one("#modules_display", Static)
                modules_display.update(self.render_modules())
                bb_track_ui("modules_display", "update", {"status": "success"}, True)
            except Exception as e:
                bb_track_error(e, "refresh_modules_display")
            
            # Performance
            try:
                performance_display = self.query_one("#performance_display", Static)
                performance_display.update(self.render_performance())
                bb_track_ui("performance_display", "update", {"status": "success"}, True)
            except Exception as e:
                bb_track_error(e, "refresh_performance_display")
            
            # Reports
            try:
                reports_display = self.query_one("#reports_display", Static)
                reports_display.update(self.render_reports())
                bb_track_ui("reports_display", "update", {"status": "success"}, True)
            except Exception as e:
                bb_track_error(e, "refresh_reports_display")
            
            bb_track_ui("refresh", "completed", {"all_displays": "updated"}, True)
            
        except Exception as e:
            bb_track_error(e, "refresh_all_displays")
            bb_track_ui("refresh", "failed", {"error": str(e)}, False, str(e))
    
    async def action_refresh(self) -> None:
        """Acción refresh INSTRUMENTADA"""
        bb_track_function("action_refresh")
        try:
            self.refresh_all_displays()
            bb_track_ui("action", "refresh", {"status": "completed"}, True)
        except Exception as e:
            bb_track_error(e, "action_refresh")
    
    async def action_start_analysis(self) -> None:
        """Acción start analysis INSTRUMENTADA"""
        bb_track_function("action_start_analysis")
        try:
            bb_track_ui("action", "start_analysis", {"status": "triggered"}, True)
            # Simulación de análisis
            for module in self.dashboard.modules.values():
                if module.status == "PENDING":
                    module.status = "PROCESSING"
            
            self.refresh_all_displays()
            bb_track_ui("action", "start_analysis", {"status": "completed"}, True)
        except Exception as e:
            bb_track_error(e, "action_start_analysis")
    
    async def action_export_report(self) -> None:
        """Acción export report INSTRUMENTADA"""
        bb_track_function("action_export_report")
        try:
            # Generar reporte BlackBox
            if BLACKBOX_AVAILABLE:
                bb_generate_report()
                bb_track_ui("action", "export_report", {"blackbox_report": "generated"}, True)
            
            bb_track_ui("action", "export_report", {"status": "completed"}, True)
        except Exception as e:
            bb_track_error(e, "action_export_report")

def main_instrumented():
    """Función principal INSTRUMENTADA"""
    console = Console()
    
    try:
        console.print("[bold cyan]🔧 ICT PROGRESS DASHBOARD + BLACKBOX[/bold cyan]")
        console.print("[bold red]🔴 BlackBox Logger ACTIVO[/bold red]")
        if BLACKBOX_AVAILABLE:
            console.print(f"[dim]Session: {ict_blackbox.session_id}[/dim]")
            console.print(f"[dim]Logs: logs/blackbox/{ict_blackbox.session_id}/[/dim]")
        console.print()
        
        if not TEXTUAL_AVAILABLE:
            console.print("[bold red]❌ Error: Textual no disponible[/bold red]")
            return
        
        console.print("[bold green]🚀 Iniciando Progress Dashboard + BlackBox...[/bold green]")
        
        app = ProgressDashboardApp()
        
        try:
            app.run()
        finally:
            # Generar reporte final al cerrar
            if BLACKBOX_AVAILABLE:
                console.print("[bold red]🔴 Generando reporte final BlackBox...[/bold red]")
                report_file = bb_generate_report()
                console.print(f"[bold green]📊 Reporte BlackBox: {report_file}[/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Dashboard cerrado por usuario[/yellow]")
        if BLACKBOX_AVAILABLE:
            bb_generate_report()
    except Exception as e:
        console.print(f"\n[bold red]❌ Error crítico: {e}[/bold red]")
        if BLACKBOX_AVAILABLE:
            bb_track_error(e, "main_instrumented")
            bb_generate_report()
        raise

if __name__ == "__main__":
    main_instrumented()
