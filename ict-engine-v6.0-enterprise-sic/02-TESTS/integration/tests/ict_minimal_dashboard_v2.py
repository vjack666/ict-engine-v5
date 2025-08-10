#!/usr/bin/env python3
"""
🎯 ICT ENGINE REGLA #10 - DASHBOARD MINIMALISTA REAL v2
================================================================================
Dashboard súper limpio: solo nombre, progreso, precisión y patterns
Todo lo demás se guarda en archivo final
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
import contextlib
from io import StringIO

# Rich imports minimalistas
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.align import Align
from rich.panel import Panel

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
    rule10_status: str = "⏳"  # ⏳ 🔄 ✅ ❌
    
class ICTMinimalDashboard:
    """🎯 Dashboard súper minimalista y limpio"""
    
    def __init__(self):
        self.console = Console()
        self.modules = {
            "ORDER_BLOCKS": ModuleStatus("ORDER_BLOCKS", "🎯"),
            "FAIR_VALUE_GAPS": ModuleStatus("FAIR_VALUE_GAPS", "📏"),
            "BREAKER_BLOCKS": ModuleStatus("BREAKER_BLOCKS", "🧱"),
            "SILVER_BULLET": ModuleStatus("SILVER_BULLET", "🥈"),
            "LIQUIDITY_POOLS": ModuleStatus("LIQUIDITY_POOLS", "💧"),
            "DISPLACEMENT": ModuleStatus("DISPLACEMENT", "⚡"),
        }
        self.session_start = datetime.now()
        self.is_running = False
        self.execution_log = []
        self.current_module = ""
        
    def _create_clean_table(self) -> Table:
        """Crear tabla súper limpia como pediste"""
        table = Table(show_header=False, box=None, padding=(0, 1))
        
        for module in self.modules.values():
            # Nombre con icono
            name_text = f"{module.icon} {module.name}"
            
            # Barra de progreso minimalista
            bar_length = 20
            filled = int(module.progress * bar_length / 100)
            progress_bar = "█" * filled + "░" * (bar_length - filled)
            
            # Precisión con color
            if module.precision >= 80:
                precision_text = f"[green]{module.precision:.1f}%[/green]"
            elif module.precision >= 60:
                precision_text = f"[yellow]{module.precision:.1f}%[/yellow]"
            else:
                precision_text = f"[red]{module.precision:.1f}%[/red]"
            
            # Status de Regla 10
            status_icon = module.rule10_status
            
            # Fila limpia
            table.add_row(
                f"[cyan]{name_text}[/cyan]",
                f"[bright_blue]{progress_bar}[/bright_blue]",
                precision_text,
                f"[cyan]{module.patterns_found:,}[/cyan]",
                status_icon
            )
        
        return table
    
    def _silent_analysis(self, analysis_func, data_files):
        """Ejecutar análisis silenciosamente (sin output del backtester)"""
        # Capturar todo el output para mantener limpia la pantalla
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        
        try:
            # Redirigir output a buffer
            sys.stdout = StringIO()
            sys.stderr = StringIO()
            
            # Ejecutar análisis
            result = analysis_func(data_files)
            return result
            
        finally:
            # Restaurar output
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    
    def run_real_analysis(self):
        """🎯 Análisis real silencioso"""
        try:
            # Inicializar backtester silenciosamente
            data_path = str(Path(__file__).parent.parent / "data" / "candles")
            
            # Capturar output de inicialización
            with contextlib.redirect_stdout(StringIO()), contextlib.redirect_stderr(StringIO()):
                self.backtester = ModularICTBacktester(data_path=data_path)
                data_files = self.backtester._prepare_data_files()
            
            # Análisis en orden
            analysis_phases = [
                ("ORDER_BLOCKS", self.backtester._analyze_order_blocks),
                ("FAIR_VALUE_GAPS", self.backtester._analyze_fair_value_gaps),
                ("BREAKER_BLOCKS", self.backtester._analyze_breaker_blocks),
                ("SILVER_BULLET", self.backtester._analyze_silver_bullet),
                ("LIQUIDITY_POOLS", self.backtester._analyze_liquidity_pools),
                ("DISPLACEMENT", self.backtester._analyze_displacement)
            ]
            
            for i, (module_key, analysis_func) in enumerate(analysis_phases):
                if not self.is_running:
                    break
                    
                # Marcar módulo actual
                self.current_module = module_key
                self.modules[module_key].rule10_status = "🔄"
                
                # Ejecutar análisis silencioso
                result = self._silent_analysis(analysis_func, data_files)
                
                # Actualizar progreso gradualmente para efecto visual
                for progress in range(0, 101, 10):
                    if not self.is_running:
                        break
                    self.modules[module_key].progress = progress
                    time.sleep(0.1)
                
                # Actualizar resultados finales
                self.modules[module_key].patterns_found = result.patterns_detected
                self.modules[module_key].precision = result.success_rate
                self.modules[module_key].progress = 100.0
                
                # Evaluar Regla 10
                if result.success_rate >= 80.0:
                    self.modules[module_key].rule10_status = "✅"
                else:
                    self.modules[module_key].rule10_status = "❌"
                
                # Log detallado para archivo
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
                    "regla10_compliant": result.success_rate >= 80.0,
                    "timestamp": datetime.now().isoformat()
                })
                
                time.sleep(0.5)  # Pausa entre módulos
            
            self.current_module = "COMPLETED"
            
        except Exception as e:
            self.execution_log.append({
                "error": f"Critical error: {e}",
                "timestamp": datetime.now().isoformat()
            })
    
    def _save_final_report(self):
        """💾 Guardar reporte completo"""
        try:
            reports_dir = Path(__file__).parent.parent / "test_reports"
            reports_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Reporte completo
            report_data = {
                "session_info": {
                    "timestamp": datetime.now().isoformat(),
                    "duration_seconds": (datetime.now() - self.session_start).total_seconds(),
                    "total_patterns_found": sum(m.patterns_found for m in self.modules.values()),
                    "regla10_compliance_count": sum(1 for m in self.modules.values() if m.rule10_status == "✅")
                },
                "modules_results": {
                    name: {
                        "patterns_found": module.patterns_found,
                        "precision": module.precision,
                        "rule10_status": module.rule10_status,
                        "progress": module.progress
                    }
                    for name, module in self.modules.items()
                },
                "detailed_execution_log": self.execution_log,
                "regla10_final_evaluation": {
                    "total_modules": len(self.modules),
                    "passed_modules": sum(1 for m in self.modules.values() if m.rule10_status == "✅"),
                    "failed_modules": sum(1 for m in self.modules.values() if m.rule10_status == "❌"),
                    "compliance_percentage": (sum(1 for m in self.modules.values() if m.rule10_status == "✅") / len(self.modules)) * 100,
                    "overall_status": "COMPLIANT" if sum(1 for m in self.modules.values() if m.rule10_status == "✅") >= 4 else "NON_COMPLIANT"
                }
            }
            
            report_file = reports_dir / f"ict_minimal_regla10_report_{timestamp}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            return str(report_file)
            
        except Exception:
            return None
    
    def run(self):
        """🚀 Ejecutar dashboard súper limpio"""
        self.console.clear()
        
        # Header minimalista
        header = Panel.fit(
            "[bold bright_cyan]🎯 ICT ENGINE - REGLA #10[/bold bright_cyan]\n[dim]Dashboard Minimalista Real[/dim]",
            style="bright_cyan"
        )
        
        self.is_running = True
        
        # Hilo de análisis
        analysis_thread = threading.Thread(target=self.run_real_analysis)
        analysis_thread.daemon = True
        analysis_thread.start()
        
        try:
            # Display en tiempo real súper limpio
            with Live(refresh_per_second=4) as live:
                while self.is_running and analysis_thread.is_alive():
                    # Crear display completo
                    table = self._create_clean_table()
                    
                    # Info actual
                    if self.current_module and self.current_module != "COMPLETED":
                        status_text = f"[yellow]🔍 Analizando: {self.current_module}[/yellow]"
                    elif self.current_module == "COMPLETED":
                        total_patterns = sum(m.patterns_found for m in self.modules.values())
                        passed = sum(1 for m in self.modules.values() if m.rule10_status == "✅")
                        status_text = f"[green]✅ Completado: {total_patterns:,} patterns | {passed}/6 REGLA #10[/green]"
                    else:
                        status_text = "[dim]Iniciando análisis...[/dim]"
                    
                    # Combinar todo
                    full_display = f"{header}\n\n{table}\n\n{Align.center(status_text)}"
                    live.update(full_display)
                    
                    if self.current_module == "COMPLETED":
                        time.sleep(2)
                        break
                    
                    time.sleep(0.25)
                
        except KeyboardInterrupt:
            self.is_running = False
        
        # Guardar reporte y mostrar resultado
        self.console.clear()
        self.console.print(header)
        self.console.print()
        self.console.print(self._create_clean_table())
        self.console.print()
        
        report_file = self._save_final_report()
        if report_file:
            self.console.print(f"[green]💾 Reporte detallado guardado en:[/green]")
            self.console.print(f"[dim]{report_file}[/dim]")
        
        self.console.print(f"\n[green]✅ Análisis completado en {(datetime.now() - self.session_start).total_seconds():.1f}s[/green]")

def main():
    """🎯 Función principal"""
    dashboard = ICTMinimalDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
