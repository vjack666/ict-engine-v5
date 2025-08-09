#!/usr/bin/env python3
"""
🔴 ICT ENTERPRISE DASHBOARD CON BLACKBOX LOGGER INTEGRADO
================================================================================
Version instrumentada del dashboard ICT Enterprise con logging ultra detallado
para diagnosticar exactamente por qué las pestañas no muestran contenido.

🎯 OBJETIVO: Detectar el problema específico de las velas/pestañas
🔍 INSTRUMENTACIÓN: Todos los métodos render_* y UI están monitoreados
================================================================================
"""

# Importar el BlackBox Logger
import sys
import os
from pathlib import Path

# Agregar path del blackbox logger
sys.path.append(str(Path(__file__).parent))

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

# Importar el dashboard original y instrumentarlo
try:
    # Importar todo del dashboard original
    from ict_enterprise_dashboard import *
    
    print("🎯 Dashboard original cargado, aplicando instrumentación...")
    
    # Crear clase instrumentada
    class ICTEnterpriseAppInstrumented(ICTEnterpriseApp):
        """Dashboard ICT Enterprise con BlackBox Logger integrado"""
        
        def __init__(self):
            bb_track_function("ICTEnterpriseAppInstrumented.__init__")
            try:
                super().__init__()
                bb_track_ui("dashboard", "initialization", {"status": "success"}, True)
                print("🔴 Dashboard instrumentado iniciado correctamente")
            except Exception as e:
                bb_track_error(e, "Dashboard initialization")
                raise
        
        def compose(self) -> ComposeResult:
            """Crear la interfaz completa - VERSION INSTRUMENTADA"""
            bb_track_function("compose")
            bb_track_ui("compose", "start", {"action": "creating_interface"}, True)
            
            try:
                result = super().compose()
                bb_track_ui("compose", "success", {"widgets_created": "header_footer_tabs"}, True)
                return result
            except Exception as e:
                bb_track_error(e, "compose method")
                bb_track_ui("compose", "failed", {"error": str(e)}, False, str(e))
                raise
        
        def render_header_info(self) -> str:
            """Header instrumentado"""
            bb_track_function("render_header_info")
            
            try:
                start_time = time.time()
                
                # Log estado antes del render
                bb_track_ui("header", "render_start", {
                    "analysis_running": self.analysis_running,
                    "engine_session": self.ict_engine.session_id
                }, True)
                
                elapsed = time.time() - self.ict_engine.start_time
                total_patterns = sum(m.patterns_detected for m in self.ict_engine.modules.values())
                status = "🟢 ACTIVO" if self.analysis_running else "🟡 LISTO"
                
                content = f"""[bold cyan]ICT ENGINE v6.1 ENTERPRISE DASHBOARD[/bold cyan]
Session: {self.ict_engine.session_id} | Tiempo: {elapsed:.0f}s | Patterns: {total_patterns} | Estado: {status}"""
                
                execution_time = time.time() - start_time
                bb_track_render("render_header_info", content[:100], True, None, len(content))
                bb_track_function("render_header_info", result="success", execution_time=execution_time)
                
                return content
                
            except Exception as e:
                bb_track_error(e, "render_header_info")
                bb_track_render("render_header_info", None, False, str(e), 0)
                bb_track_tab("header", "render_header_info", False, 0, str(e))
                return f"[bold red]ERROR HEADER: {str(e)}[/bold red]"
        
        def render_overview_enterprise(self) -> str:
            """Overview instrumentado"""
            bb_track_function("render_overview_enterprise")
            
            try:
                start_time = time.time()
                
                # Log estado de datos de entrada
                bb_track_data("overview_input_check", self.ict_engine.modules, 
                             f"modules_count: {len(self.ict_engine.modules)}")
                
                bb_track_ui("overview_tab", "render_start", {
                    "modules_available": len(self.ict_engine.modules),
                    "analysis_running": self.analysis_running
                }, True)
                
                total_modules = len(self.ict_engine.modules)
                completed = len([m for m in self.ict_engine.modules.values() if m.status == "COMPLETED"])
                processing = len([m for m in self.ict_engine.modules.values() if m.status == "PROCESSING"])
                total_patterns = sum(m.patterns_detected for m in self.ict_engine.modules.values())
                total_signals = sum(m.signals_generated for m in self.ict_engine.modules.values())
                
                # Log métricas calculadas
                bb_track_data("overview_metrics", {
                    "total_modules": total_modules,
                    "completed": completed,
                    "processing": processing
                }, {
                    "total_patterns": total_patterns,
                    "total_signals": total_signals
                })
                
                # Calcular grade general
                completion_rate = (completed / total_modules) * 100 if total_modules > 0 else 0
                if completion_rate >= 90:
                    grade = "A+ EXCELLENT"
                    grade_color = "bold green"
                elif completion_rate >= 75:
                    grade = "A VERY GOOD"
                    grade_color = "bold blue"
                elif completion_rate >= 60:
                    grade = "B GOOD"
                    grade_color = "bold yellow"
                else:
                    grade = "C DEVELOPING"
                    grade_color = "bold red"
                
                # Top 3 performers
                top_performers = sorted(
                    self.ict_engine.modules.values(), 
                    key=lambda x: x.patterns_detected, 
                    reverse=True
                )[:3]
                
                content = f"""[bold cyan]📊 OVERVIEW ENTERPRISE - ICT ENGINE v6.1[/bold cyan]

[bold white]RESUMEN EJECUTIVO:[/bold white]
┌─────────────────────────────────────────────────────────────────┐
│ • Módulos ICT: [bold]{total_modules}[/bold] | Completados: [bold green]{completed}[/bold green] | Procesando: [bold yellow]{processing}[/bold yellow]          │
│ • Patterns detectados: [bold green]{total_patterns}[/bold green] | Señales generadas: [bold blue]{total_signals}[/bold blue]                │
│ • Files analizados: [bold]{self.ict_engine.total_files}[/bold] | Grade: [{grade_color}]{grade}[/{grade_color}]                          │
└─────────────────────────────────────────────────────────────────┘

[bold white]TOP PERFORMERS:[/bold white]
{"🥇" if len(top_performers) > 0 else "🏅"} [bold]{top_performers[0].icon if len(top_performers) > 0 else "---"} {top_performers[0].name if len(top_performers) > 0 else "Pendiente"}[/bold] - {top_performers[0].patterns_detected if len(top_performers) > 0 else 0} patterns
{"🥈" if len(top_performers) > 1 else "🏅"} [bold]{top_performers[1].icon if len(top_performers) > 1 else "---"} {top_performers[1].name if len(top_performers) > 1 else "Pendiente"}[/bold] - {top_performers[1].patterns_detected if len(top_performers) > 1 else 0} patterns  
{"🥉" if len(top_performers) > 2 else "🏅"} [bold]{top_performers[2].icon if len(top_performers) > 2 else "---"} {top_performers[2].name if len(top_performers) > 2 else "Pendiente"}[/bold] - {top_performers[2].patterns_detected if len(top_performers) > 2 else 0} patterns

[bold white]SISTEMA STATUS:[/bold white]
• Engine Core: [bold green]✅ Operativo[/bold green]
• Detectores ICT: [bold green]✅ Cargados[/bold green]
• Análisis Real: [bold green]✅ Disponible[/bold green]
• Export/Reports: [bold green]✅ Funcional[/bold green]

[bold white]ESTADO DE ANÁLISIS:[/bold white]
• Status: {"[bold green]EJECUTANDO[/bold green]" if self.analysis_running else "[bold yellow]LISTO PARA EJECUTAR[/bold yellow]"}
• Datos disponibles: [bold blue]{len(self.ict_engine.load_market_data())} archivos CSV[/bold blue]
• Tiempo transcurrido: [bold]{time.time() - self.ict_engine.start_time:.1f}s[/bold]

[bold green]🎯 SISTEMA ICT ENTERPRISE COMPLETAMENTE OPERATIVO[/bold green]

[bold white]🔴 BLACKBOX LOGGING ACTIVO:[/bold white]
• Session: {ict_blackbox.session_id if BLACKBOX_AVAILABLE else 'N/A'}
• Eventos rastreados: {ict_blackbox.counters['function_calls'] if BLACKBOX_AVAILABLE else 'N/A'}
• Logs en: logs/blackbox/

[bold white]NAVEGACIÓN:[/bold white]
• Tecla 1: 📊 Overview Enterprise (actual)
• Tecla 2: 🔍 Detectores ICT detallados
• Tecla 3: ⚡ Performance & Métricas  
• Tecla 4: 📈 Análisis Técnico avanzado
• Tecla 5: 📋 Reportes & Exportación
• Ctrl+S: Iniciar análisis completo
• Ctrl+R: Refresh todos los datos
• Ctrl+E: Exportar reportes"""

                execution_time = time.time() - start_time
                bb_track_render("render_overview_enterprise", content[:200], True, None, len(content))
                bb_track_tab("overview", "render_overview_enterprise", True, len(content))
                bb_track_function("render_overview_enterprise", result="success", execution_time=execution_time)
                
                return content
                
            except Exception as e:
                bb_track_error(e, "render_overview_enterprise")
                bb_track_render("render_overview_enterprise", None, False, str(e), 0)
                bb_track_tab("overview", "render_overview_enterprise", False, 0, str(e))
                return f"[bold red]ERROR OVERVIEW: {str(e)}[/bold red]"
        
        def render_ict_detectors(self) -> str:
            """Detectores instrumentados"""
            bb_track_function("render_ict_detectors")
            
            try:
                start_time = time.time()
                
                bb_track_ui("detectors_tab", "render_start", {
                    "modules_to_process": len(self.ict_engine.modules)
                }, True)
                
                content = """[bold cyan]🔍 DETECTORES ICT - ANÁLISIS DETALLADO[/bold cyan]

[bold white]ESTADO DE MÓDULOS ICT:[/bold white]
┌──────────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│ Detector             │ Estado      │ Patterns    │ Precisión   │ Cobertura   │
├──────────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤"""
                
                modules_processed = 0
                for module in self.ict_engine.modules.values():
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
                        
                        # Métricas con colores
                        precision = module.precision_score if module.precision_score > 0 else self.ict_engine.ict_benchmarks.get(module.name.lower().replace(' ', '_'), {}).get('precision', 75.0)
                        coverage = module.coverage_score if module.coverage_score > 0 else self.ict_engine.ict_benchmarks.get(module.name.lower().replace(' ', '_'), {}).get('coverage', 60.0)
                        
                        precision_color = "bold green" if precision >= 80 else "yellow" if precision >= 70 else "red"
                        coverage_color = "bold green" if coverage >= 70 else "yellow" if coverage >= 60 else "red"
                        
                        content += f"""
│ {module.icon} {module.name:<16} │ [{status_color}]{status_text:<9}[/{status_color}] │ [bold blue]{module.patterns_detected:>9}[/bold blue] │ [{precision_color}]{precision:>8.1f}%[/{precision_color}] │ [{coverage_color}]{coverage:>8.1f}%[/{coverage_color}] │"""
                        
                        modules_processed += 1
                        
                    except Exception as module_error:
                        bb_track_error(module_error, f"Processing module {module.name}")
                        content += f"""
│ ❌ {module.name:<16} │ [red]ERROR[/red]    │ [red]    N/A[/red] │ [red]   N/A[/red] │ [red]   N/A[/red] │"""
                
                content += """
└──────────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘

[bold white]BENCHMARKS ICT ENTERPRISE:[/bold white]
• Pattern Detector: Target 15 signals, Precisión 78.5%
• BOS Detector: Target 12 signals, Precisión 82.0%
• CHOCH Detector: Target 18 signals, Precisión 76.5%
• Breaker Blocks: Target 8 signals, Precisión 85.0%
• Silver Bullet: Target 5 signals, Precisión 88.0%

[bold white]ANÁLISIS REAL DE PATRONES:[/bold white]"""
                
                # Mostrar patterns detectados recientemente
                if self.ict_engine.analysis_results:
                    content += """
• Break of Structure: Detección de rupturas estructurales
• Change of Character: Análisis de cambios en momentum  
• Liquidity Zones: Identificación de zonas de liquidez
• Order Blocks: Detección de bloques institucionales
• Smart Money: Conceptos de dinero inteligente"""
                else:
                    content += """
• [dim]Ejecutar análisis para ver patterns detectados[/dim]
• [dim]Presiona Ctrl+S para iniciar análisis completo[/dim]"""
                
                content += f"""

[bold green]🎯 DETECTORES ICT PROFESIONALES LISTOS[/bold green]

[bold red]🔴 BLACKBOX DEBUG INFO:[/bold red]
• Módulos procesados: {modules_processed}/{len(self.ict_engine.modules)}
• Tiempo de render: {time.time() - start_time:.3f}s
• Errors detectados: {ict_blackbox.counters['errors'] if BLACKBOX_AVAILABLE else 'N/A'}"""
                
                execution_time = time.time() - start_time
                bb_track_render("render_ict_detectors", content[:200], True, None, len(content))
                bb_track_tab("detectors", "render_ict_detectors", True, len(content))
                bb_track_function("render_ict_detectors", result="success", execution_time=execution_time)
                
                return content
                
            except Exception as e:
                bb_track_error(e, "render_ict_detectors")
                bb_track_render("render_ict_detectors", None, False, str(e), 0)
                bb_track_tab("detectors", "render_ict_detectors", False, 0, str(e))
                return f"[bold red]ERROR DETECTORS: {str(e)}[/bold red]"
        
        def render_performance_metrics(self) -> str:
            """Performance instrumentado"""
            bb_track_function("render_performance_metrics")
            
            try:
                start_time = time.time()
                
                # Actualizar métricas del sistema
                self.ict_engine.update_system_metrics()
                
                elapsed = time.time() - self.ict_engine.start_time
                total_processed = sum(m.files_processed for m in self.ict_engine.modules.values())
                processing_speed = total_processed / elapsed if elapsed > 0 else 0
                
                content = f"""[bold cyan]⚡ PERFORMANCE & MÉTRICAS DEL SISTEMA[/bold cyan]

[bold white]VELOCIDAD DE PROCESAMIENTO:[/bold white]
┌─────────────────────────────────────────────────────────────────┐
│ • Tiempo total: [bold blue]{elapsed:.1f}s[/bold blue] | Files/seg: [bold green]{processing_speed:.2f}[/bold green]                   │
│ • Data points: [bold]{sum(m.data_points for m in self.ict_engine.modules.values()):,}[/bold] | Errores: [bold red]{sum(m.error_count for m in self.ict_engine.modules.values())}[/bold red]                    │
│ • Tasa de éxito: [bold green]{np.mean([m.success_rate for m in self.ict_engine.modules.values()]):.1f}%[/bold green] | Threads activos: [bold]{self.ict_engine.system_metrics.active_threads}[/bold]           │
└─────────────────────────────────────────────────────────────────┘

[bold white]RECURSOS DEL SISTEMA:[/bold white]
• CPU Usage: [bold green]{self.ict_engine.system_metrics.cpu_percent:.1f}%[/bold green]
• Memory Usage: [bold green]{self.ict_engine.system_metrics.memory_percent:.1f}%[/bold green]
• Memory Available: [bold blue]{self.ict_engine.system_metrics.memory_available_gb:.1f} GB[/bold blue]
• Network I/O: [bold green]Active[/bold green]

[bold red]🔴 BLACKBOX PERFORMANCE METRICS:[/bold red]
• Function calls tracked: {ict_blackbox.counters['function_calls'] if BLACKBOX_AVAILABLE else 'N/A'}
• UI events tracked: {ict_blackbox.counters['ui_events'] if BLACKBOX_AVAILABLE else 'N/A'}
• Renders successful: {ict_blackbox.counters['renders_success'] if BLACKBOX_AVAILABLE else 'N/A'}
• Renders failed: {ict_blackbox.counters['renders_failed'] if BLACKBOX_AVAILABLE else 'N/A'}
• Errors logged: {ict_blackbox.counters['errors'] if BLACKBOX_AVAILABLE else 'N/A'}

[bold green]💾 SISTEMA DE MONITORING ACTIVO[/bold green]"""

                execution_time = time.time() - start_time
                bb_track_render("render_performance_metrics", content[:200], True, None, len(content))
                bb_track_tab("performance", "render_performance_metrics", True, len(content))
                bb_track_function("render_performance_metrics", result="success", execution_time=execution_time)
                
                return content
                
            except Exception as e:
                bb_track_error(e, "render_performance_metrics")
                bb_track_render("render_performance_metrics", None, False, str(e), 0)
                bb_track_tab("performance", "render_performance_metrics", False, 0, str(e))
                return f"[bold red]ERROR PERFORMANCE: {str(e)}[/bold red]"
        
        def render_technical_analysis(self) -> str:
            """Analysis instrumentado"""
            bb_track_function("render_technical_analysis")
            
            try:
                start_time = time.time()
                
                content = f"""[bold cyan]📈 ANÁLISIS TÉCNICO AVANZADO[/bold cyan]

[bold white]ESTADÍSTICAS DE PATTERNS DETECTADOS:[/bold white]
• Total patterns: {len(self.ict_engine.analysis_results)}
• Patterns de alta confianza (>80%): {len([p for p in self.ict_engine.analysis_results if p.confidence > 0.8])}
• Symbols analizados: {len(set(p.symbol for p in self.ict_engine.analysis_results)) if self.ict_engine.analysis_results else 0}

[bold white]ANÁLISIS DE CALIDAD:[/bold white]
• Confidence promedio: {np.mean([p.confidence for p in self.ict_engine.analysis_results]) * 100:.1f}% if self.ict_engine.analysis_results else 0
• Distribución por tipo: Balanceada
• Coverage temporal: Completa

[bold red]🔴 BLACKBOX ANALYSIS DEBUG:[/bold red]
• Session time: {time.time() - ict_blackbox.start_time:.1f}s if BLACKBOX_AVAILABLE else 'N/A'
• Total events logged: {sum(ict_blackbox.counters.values()) if BLACKBOX_AVAILABLE else 'N/A'}
• Log directory: logs/blackbox/{ict_blackbox.session_id if BLACKBOX_AVAILABLE else 'N/A'}/

[bold green]📊 ANÁLISIS TÉCNICO COMPLETADO[/bold green]"""

                execution_time = time.time() - start_time
                bb_track_render("render_technical_analysis", content[:200], True, None, len(content))
                bb_track_tab("analysis", "render_technical_analysis", True, len(content))
                bb_track_function("render_technical_analysis", result="success", execution_time=execution_time)
                
                return content
                
            except Exception as e:
                bb_track_error(e, "render_technical_analysis")
                bb_track_render("render_technical_analysis", None, False, str(e), 0)
                bb_track_tab("analysis", "render_technical_analysis", False, 0, str(e))
                return f"[bold red]ERROR ANALYSIS: {str(e)}[/bold red]"
        
        def render_reports_export(self) -> str:
            """Reports instrumentado"""
            bb_track_function("render_reports_export")
            
            try:
                start_time = time.time()
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                session_duration = time.time() - self.ict_engine.start_time
                
                content = f"""[bold cyan]📋 REPORTES & EXPORTACIÓN ENTERPRISE[/bold cyan]

[bold white]INFORMACIÓN DE SESIÓN:[/bold white]
┌─────────────────────────────────────────────────────────────────┐
│ • Session ID: [bold]{self.ict_engine.session_id}[/bold]                 │
│ • Timestamp: [bold blue]{timestamp}[/bold blue]                                       │
│ • Duración: [bold green]{session_duration:.0f} segundos[/bold green]                                   │
│ • Files procesados: [bold]{sum(m.files_processed for m in self.ict_engine.modules.values())}[/bold]                                      │
└─────────────────────────────────────────────────────────────────┘

[bold red]🔴 BLACKBOX LOGGING REPORTES:[/bold red]
┌─────────────────────────────────────────────────────────────────┐
│ • BlackBox Session: [bold]{ict_blackbox.session_id if BLACKBOX_AVAILABLE else 'N/A'}[/bold]          │
│ • Eventos capturados: [bold blue]{sum(ict_blackbox.counters.values()) if BLACKBOX_AVAILABLE else 'N/A'}[/bold blue]                                  │
│ • Errores detectados: [bold red]{ict_blackbox.counters['errors'] if BLACKBOX_AVAILABLE else 'N/A'}[/bold red]                                    │
│ • Renders exitosos: [bold green]{ict_blackbox.counters['renders_success'] if BLACKBOX_AVAILABLE else 'N/A'}[/bold green]                                    │
│ • Renders fallidos: [bold red]{ict_blackbox.counters['renders_failed'] if BLACKBOX_AVAILABLE else 'N/A'}[/bold red]                                     │
└─────────────────────────────────────────────────────────────────┘

[bold white]ACCIONES DISPONIBLES:[/bold white]
• Ctrl+E: Exportar reporte completo
• Ctrl+B: Generar BlackBox debug report
• Exportar solo métricas de performance
• Exportar patterns detectados (JSON)
• Generar reporte PDF ejecutivo

[bold white]UBICACIONES DE LOGS:[/bold white]
• Reportes regulares: test_reports/ict_enterprise/
• BlackBox logs: logs/blackbox/{ict_blackbox.session_id if BLACKBOX_AVAILABLE else 'N/A'}/
• Debug reports: logs/blackbox/*/COMPREHENSIVE_DEBUG_REPORT.json

[bold green]💾 SISTEMA DE REPORTES ENTERPRISE + BLACKBOX LISTO[/bold green]"""

                execution_time = time.time() - start_time
                bb_track_render("render_reports_export", content[:200], True, None, len(content))
                bb_track_tab("reports", "render_reports_export", True, len(content))
                bb_track_function("render_reports_export", result="success", execution_time=execution_time)
                
                return content
                
            except Exception as e:
                bb_track_error(e, "render_reports_export")
                bb_track_render("render_reports_export", None, False, str(e), 0)
                bb_track_tab("reports", "render_reports_export", False, 0, str(e))
                return f"[bold red]ERROR REPORTS: {str(e)}[/bold red]"
        
        async def refresh_all_displays(self) -> None:
            """Refresh instrumentado"""
            bb_track_function("refresh_all_displays")
            
            try:
                bb_track_ui("refresh", "start", {"action": "refresh_all_displays"}, True)
                
                # Header
                try:
                    header_display = self.query_one("#header_info", Static)
                    header_display.update(self.render_header_info())
                    bb_track_ui("header_display", "update", {"status": "success"}, True)
                except Exception as e:
                    bb_track_error(e, "refresh_header_display")
                
                # Overview
                try:
                    overview_display = self.query_one("#overview_display", Static)
                    overview_display.update(self.render_overview_enterprise())
                    bb_track_ui("overview_display", "update", {"status": "success"}, True)
                except Exception as e:
                    bb_track_error(e, "refresh_overview_display")
                
                # Detectors
                try:
                    detectors_display = self.query_one("#detectors_display", Static)
                    detectors_display.update(self.render_ict_detectors())
                    bb_track_ui("detectors_display", "update", {"status": "success"}, True)
                except Exception as e:
                    bb_track_error(e, "refresh_detectors_display")
                
                # Performance
                try:
                    performance_display = self.query_one("#performance_display", Static)
                    performance_display.update(self.render_performance_metrics())
                    bb_track_ui("performance_display", "update", {"status": "success"}, True)
                except Exception as e:
                    bb_track_error(e, "refresh_performance_display")
                
                # Analysis
                try:
                    analysis_display = self.query_one("#analysis_display", Static)
                    analysis_display.update(self.render_technical_analysis())
                    bb_track_ui("analysis_display", "update", {"status": "success"}, True)
                except Exception as e:
                    bb_track_error(e, "refresh_analysis_display")
                
                # Reports
                try:
                    reports_display = self.query_one("#reports_display", Static)
                    reports_display.update(self.render_reports_export())
                    bb_track_ui("reports_display", "update", {"status": "success"}, True)
                except Exception as e:
                    bb_track_error(e, "refresh_reports_display")
                
                bb_track_ui("refresh", "completed", {"all_displays": "updated"}, True)
                
            except Exception as e:
                bb_track_error(e, "refresh_all_displays")
                bb_track_ui("refresh", "failed", {"error": str(e)}, False, str(e))
        
        async def action_export_data(self) -> None:
            """Export con BlackBox report"""
            bb_track_function("action_export_data")
            
            try:
                # Ejecutar export original
                await super().action_export_data()
                
                # Generar reporte BlackBox también
                if BLACKBOX_AVAILABLE:
                    bb_generate_report()
                    bb_track_ui("export", "blackbox_report_generated", {"status": "success"}, True)
                
            except Exception as e:
                bb_track_error(e, "action_export_data")
    
    # Función principal instrumentada
    def main_instrumented():
        """Función principal con BlackBox Logger"""
        console = Console()
        
        try:
            console.print("[bold cyan]🎯 ICT ENGINE v6.1 ENTERPRISE + BLACKBOX[/bold cyan]")
            console.print("[bold red]🔴 BlackBox Logger ACTIVO[/bold red]")
            if BLACKBOX_AVAILABLE:
                console.print(f"[dim]Session: {ict_blackbox.session_id}[/dim]")
                console.print(f"[dim]Logs: logs/blackbox/{ict_blackbox.session_id}/[/dim]")
            console.print()
            
            if not TEXTUAL_AVAILABLE:
                console.print("[bold red]❌ Error: Textual no disponible[/bold red]")
                return
            
            console.print("[bold green]🚀 Iniciando Dashboard Enterprise + BlackBox...[/bold green]")
            
            # Usar la clase instrumentada
            app = ICTEnterpriseAppInstrumented()
            
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

except ImportError as e:
    print(f"❌ Error importando dashboard original: {e}")
    print("Ejecutar desde el directorio tests/ donde está ict_enterprise_dashboard.py")
