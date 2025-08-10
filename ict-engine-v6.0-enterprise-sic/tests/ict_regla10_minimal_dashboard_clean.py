#!/usr/bin/env python3
"""
🎯 ICT ENGINE REGLA #10 - DASHBOARD MINIMALISTA REAL
================================================================================
Dashboard súper compacto conectado directamente al sistema ICT real
Cumple estrictamente con REGLA #10 de las reglas de Copilot
================================================================================
"""

import os
import sys
import time
import json
import threading
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from pathlib import Path

# Rich imports minimalistas
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn

# Importar el backtester real
try:
    sys.path.append(str(Path(__file__).parent))
    from modular_ict_backtester import ModularICTBacktester, ModuleResult
except ImportError as e:
    print(f"❌ Error importando backtester: {e}")
    sys.exit(1)

@dataclass
class ModuleStatus:
    """Estado minimalista de cada módulo"""
    name: str
    icon: str
    progress: float = 0.0
    patterns_found: int = 0
    precision: float = 0.0
    regla10_status: str = "PENDING"  # PENDING, RUNNING, PASSED, FAILED
    
class ICTRegla10MinimalDashboard:
    """🎯 Dashboard minimalista para REGLA #10"""
    
    def __init__(self):
        self.console = Console()
        self.modules = self._init_modules()
        self.total_progress = 0.0
        self.session_start = datetime.now()
        self.is_running = False
        self.execution_log = []  # Log para reporte final
        
    def _init_modules(self) -> Dict[str, ModuleStatus]:
        """Inicializar módulos ICT reales"""
        return {
            "ORDER_BLOCKS": ModuleStatus("ORDER_BLOCKS", "🎯"),
            "FAIR_VALUE_GAPS": ModuleStatus("FAIR_VALUE_GAPS", "📏"),
            "BREAKER_BLOCKS": ModuleStatus("BREAKER_BLOCKS", "🧱"),
            "SILVER_BULLET": ModuleStatus("SILVER_BULLET", "🥈"),
            "LIQUIDITY_POOLS": ModuleStatus("LIQUIDITY_POOLS", "💧"),
            "DISPLACEMENT": ModuleStatus("DISPLACEMENT", "⚡"),
        }
    
    def _create_display_table(self) -> Table:
        """Crear tabla de visualización minimalista"""
        table = Table(show_header=True, header_style="bold magenta", box=None)
        table.add_column("MÓDULO", style="cyan", width=16)
        table.add_column("PROGRESO", justify="center", width=22)
        table.add_column("PATTERNS", justify="right", width=8)
        table.add_column("PRECISIÓN", justify="right", width=9)
        table.add_column("REGLA #10", justify="center", width=8)
        
        for module in self.modules.values():
            # Barra de progreso compacta
            bar_length = 10
            filled = int(module.progress / 10)
            progress_bar = "█" * filled + "░" * (bar_length - filled)
            progress_text = f"{progress_bar} {module.progress:5.1f}%"
            
            # Color para REGLA #10
            if module.regla10_status == "PASSED":
                status_text = "[green]✅ PASS[/green]"
            elif module.regla10_status == "FAILED":
                status_text = "[red]❌ FAIL[/red]"
            elif module.regla10_status == "RUNNING":
                status_text = "[yellow]🔄 RUN[/yellow]"
            else:
                status_text = "[dim]⏳ PEND[/dim]"
            
            table.add_row(
                f"{module.icon} {module.name}",
                f"[cyan]{progress_text}[/cyan]",
                f"[cyan]{module.patterns_found:,}[/cyan]",
                f"[cyan]{module.precision:.1f}%[/cyan]",
                status_text
            )
        
        # Resumen final
        elapsed = (datetime.now() - self.session_start).total_seconds()
        total_patterns = sum(m.patterns_found for m in self.modules.values())
        passed_modules = sum(1 for m in self.modules.values() if m.regla10_status == "PASSED")
        
        table.add_section()
        table.add_row(
            "[bold]SISTEMA",
            f"[bold cyan]{'█' * int(self.total_progress/10)}{'░' * (10-int(self.total_progress/10))} {self.total_progress:5.1f}%[/bold cyan]",
            f"[bold cyan]{total_patterns:,}[/bold cyan]",
            f"[bold cyan]{elapsed:.0f}s[/bold cyan]",
            f"[bold green]{passed_modules}/6[/bold green]" if passed_modules >= 4 else f"[bold red]{passed_modules}/6[/bold red]"
        )
        
        return table
    
    def run_real_analysis(self):
        """🎯 Ejecutar análisis real del sistema ICT"""
        
        try:
            # Instanciar el backtester real con path de datos
            data_path = str(Path(__file__).parent.parent / "data" / "candles")
            self.backtester = ModularICTBacktester(data_path=data_path)
            
            # Preparar datos reales
            self.console.print("[yellow]🔄 Preparando datos del sistema real...[/yellow]")
            data_files = self.backtester._prepare_data_files()
            
            # Análisis real usando métodos del backtester
            analysis_phases = [
                ("ORDER_BLOCKS", self.backtester._analyze_order_blocks, "📦"),
                ("FAIR_VALUE_GAPS", self.backtester._analyze_fair_value_gaps, "📏"),
                ("BREAKER_BLOCKS", self.backtester._analyze_breaker_blocks, "🧱"),
                ("SILVER_BULLET", self.backtester._analyze_silver_bullet, "🥈"),
                ("LIQUIDITY_POOLS", self.backtester._analyze_liquidity_pools, "💧"),
                ("DISPLACEMENT", self.backtester._analyze_displacement, "⚡")
            ]
            
            for i, (module_key, analysis_func, icon) in enumerate(analysis_phases):
                if not self.is_running:
                    break
                    
                # Marcar módulo como ejecutándose
                self.modules[module_key].regla10_status = "RUNNING"
                
                # Ejecutar análisis real usando el backtester
                try:
                    self.console.print(f"[yellow]🔍 Analizando {module_key}...[/yellow]")
                    result = analysis_func(data_files)
                    
                    # Actualizar resultados con datos reales
                    self.modules[module_key].patterns_found = result.patterns_detected
                    self.modules[module_key].precision = result.success_rate
                    self.modules[module_key].progress = 100.0
                    
                    # Evaluar REGLA #10 (success_rate >= 80%)
                    regla10_passed = result.success_rate >= 80.0
                    self.modules[module_key].regla10_status = "PASSED" if regla10_passed else "FAILED"
                    
                    # Log para archivo final
                    self.execution_log.append({
                        "module": module_key,
                        "patterns_detected": result.patterns_detected,
                        "signals_generated": result.signals_generated,
                        "success_rate": result.success_rate,
                        "avg_confidence": result.avg_confidence,
                        "execution_time": result.execution_time,
                        "data_points_analyzed": result.data_points_analyzed,
                        "errors": result.errors,
                        "status": result.status,
                        "regla10_compliant": regla10_passed,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    self.modules[module_key].regla10_status = "FAILED"
                    self.console.print(f"[red]❌ Error en {module_key}: {str(e)[:50]}[/red]")
                    self.execution_log.append({
                        "module": module_key,
                        "error": str(e),
                        "regla10_compliant": False,
                        "timestamp": datetime.now().isoformat()
                    })
                
                # Actualizar progreso total
                self.total_progress = ((i + 1) / len(analysis_phases)) * 100
                
                # Pequeña pausa para visualización
                time.sleep(0.3)
            
            # Finalizar análisis
            self.console.print("[green]✅ Análisis completo del sistema real[/green]")
            
        except Exception as e:
            self.console.print(f"[red]❌ Error crítico en análisis real: {e}[/red]")
            import traceback
            self.console.print(f"[red]{traceback.format_exc()}[/red]")
    
    def _save_final_report(self):
        """💾 Guardar reporte final detallado"""
        try:
            # Crear directorio de reportes
            reports_dir = Path(__file__).parent.parent / "test_reports"
            reports_dir.mkdir(exist_ok=True)
            
            # Generar timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Datos del reporte
            report_data = {
                "session_info": {
                    "timestamp": datetime.now().isoformat(),
                    "duration_seconds": (datetime.now() - self.session_start).total_seconds(),
                    "total_patterns_found": sum(m.patterns_found for m in self.modules.values()),
                    "regla10_compliance": sum(1 for m in self.modules.values() if m.regla10_status == "PASSED")
                },
                "modules_summary": {
                    name: {
                        "patterns_found": module.patterns_found,
                        "precision": module.precision,
                        "regla10_status": module.regla10_status,
                        "progress": module.progress
                    }
                    for name, module in self.modules.items()
                },
                "detailed_execution_log": self.execution_log,
                "regla10_evaluation": {
                    "total_modules": len(self.modules),
                    "passed_modules": sum(1 for m in self.modules.values() if m.regla10_status == "PASSED"),
                    "failed_modules": sum(1 for m in self.modules.values() if m.regla10_status == "FAILED"),
                    "compliance_percentage": (sum(1 for m in self.modules.values() if m.regla10_status == "PASSED") / len(self.modules)) * 100,
                    "overall_status": "COMPLIANT" if sum(1 for m in self.modules.values() if m.regla10_status == "PASSED") >= 4 else "NON_COMPLIANT"
                }
            }
            
            # Guardar reporte
            report_file = reports_dir / f"ict_regla10_minimal_report_{timestamp}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            self.console.print(f"[green]💾 Reporte guardado: {report_file}[/green]")
            
        except Exception as e:
            self.console.print(f"[red]❌ Error guardando reporte: {e}[/red]")
    
    def run(self):
        """🚀 Ejecutar dashboard en tiempo real"""
        self.console.clear()
        self.console.print("\n[bold magenta]🎯 ICT ENGINE - REGLA #10 DASHBOARD MINIMALISTA[/bold magenta]")
        self.console.print("[dim]Conectado al sistema real - Cumplimiento estricto REGLA #10[/dim]\n")
        
        self.is_running = True
        
        # Hilo para análisis en paralelo
        analysis_thread = threading.Thread(target=self.run_real_analysis)
        analysis_thread.daemon = True
        analysis_thread.start()
        
        try:
            # Display en tiempo real
            with Live(self._create_display_table(), refresh_per_second=2) as live:
                while self.is_running and (self.total_progress < 100 or analysis_thread.is_alive()):
                    live.update(self._create_display_table())
                    time.sleep(0.5)
                
                # Display final
                live.update(self._create_display_table())
                
        except KeyboardInterrupt:
            self.is_running = False
            self.console.print("\n[yellow]⚠️ Dashboard interrumpido por usuario[/yellow]")
        
        # Guardar reporte final
        self._save_final_report()
        
        self.console.print("\n[green]✅ Dashboard finalizado correctamente[/green]")

def main():
    """🎯 Función principal"""
    dashboard = ICTRegla10MinimalDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
