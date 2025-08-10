#!/usr/bin/env python3
"""
🎯 ICT ENGINE REGLA #10 - DASHBOARD FINAL MINIMALISTA
================================================================================
Exactamente como pediste: solo nombre, barra de progreso, precisión, 
número de patterns encontrados. Todo lo demás se guarda en archivo.
================================================================================
"""

print("LOG: Iniciando imports...")

import os
import sys
import time
import json
import threading
from datetime import datetime
from dataclasses import dataclass
from typing import Dict
from pathlib import Path
import contextlib
from io import StringIO

print("LOG: Imports básicos completados")

# Rich imports
try:
    print("LOG: Importando Rich...")
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.panel import Panel
    from rich.text import Text
    print("LOG: Rich importado correctamente")
except Exception as e:
    print(f"LOG: ERROR importando Rich: {e}")
    sys.exit(1)

print("LOG: Añadiendo path...")

# Importar el backtester real
try:
    current_path = str(Path(__file__).parent)
    print(f"LOG: Path actual: {current_path}")
    sys.path.append(current_path)
    print("LOG: Importando backtester...")
    from modular_ict_backtester import ModularICTBacktester
    print("LOG: Backtester importado correctamente")
except ImportError as e:
    print(f"LOG: ERROR importando backtester: {e}")
    sys.exit(1)
except Exception as e:
    print(f"LOG: ERROR inesperado con backtester: {e}")
    sys.exit(1)

@dataclass
class ModuleStatus:
    name: str
    icon: str
    progress: float = 0.0
    patterns_found: int = 0
    precision: float = 0.0
    rule10_status: str = "⏳"

print("LOG: Definiendo clase ModuleStatus completada")

class ICTFinalDashboard:
    def __init__(self):
        print("LOG: Inicializando dashboard...")
        try:
            self.console = Console()
            print("LOG: Console creada")
            
            self.modules = {
                "ORDER_BLOCKS": ModuleStatus("ORDER_BLOCKS", "🎯"),
                "FAIR_VALUE_GAPS": ModuleStatus("FAIR_VALUE_GAPS", "📏"), 
                "BREAKER_BLOCKS": ModuleStatus("BREAKER_BLOCKS", "🧱"),
                "SILVER_BULLET": ModuleStatus("SILVER_BULLET", "🥈"),
                "LIQUIDITY_POOLS": ModuleStatus("LIQUIDITY_POOLS", "💧"),
                "DISPLACEMENT": ModuleStatus("DISPLACEMENT", "⚡")
            }
            print("LOG: Módulos inicializados")
            
            self.session_start = datetime.now()
            self.is_running = False
            self.execution_log = []
            self.current_module = ""
            print("LOG: Dashboard inicializado correctamente")
        except Exception as e:
            print(f"LOG: ERROR en __init__: {e}")
            raise
        
    def _create_minimal_table(self) -> Table:
        """Tabla exactamente como pediste"""
        table = Table(show_header=False, box=None, padding=(0, 2))
        
        for module in self.modules.values():
            # Nombre con icono
            name_display = f"{module.icon} {module.name}"
            
            # Barra de progreso como pediste
            bar_length = 15
            filled = int(module.progress * bar_length / 100)
            progress_bar = "█" * filled + "░" * (bar_length - filled)
            
            # Precisión con formato limpio
            precision_text = f"Precisión: {module.precision:.1f}%"
            
            # Número de patterns encontrados
            patterns_text = f"{module.patterns_found:,} patterns"
            
            # Status info
            if module.rule10_status == "✅":
                status_info = "[green]✅ REGLA #10 OK[/green]"
            elif module.rule10_status == "❌":
                status_info = "[red]❌ REGLA #10 FAIL[/red]"
            elif module.rule10_status == "🔄":
                status_info = "[yellow]🔄 ANALIZANDO[/yellow]"
            else:
                status_info = "[dim]⏳ PENDIENTE[/dim]"
            
            table.add_row(
                f"[cyan]{name_display}[/cyan]",
                f"[bright_blue]{progress_bar}[/bright_blue]",
                f"[green]{precision_text}[/green]",
                f"[yellow]{patterns_text}[/yellow]",
                status_info
            )
        
        return table
    
    def _silent_analysis(self, analysis_func, data_files):
        """Ejecutar análisis completamente silencioso"""
        with contextlib.redirect_stdout(StringIO()), contextlib.redirect_stderr(StringIO()):
            return analysis_func(data_files)
    
    def run_analysis(self):
        """Análisis real silencioso con mejor manejo de errores"""
        try:
            # Inicializar sistema real
            data_path = str(Path(__file__).parent.parent / "data" / "candles")
            
            # Silenciar la inicialización del backtester
            with contextlib.redirect_stdout(StringIO()), contextlib.redirect_stderr(StringIO()):
                self.backtester = ModularICTBacktester(data_path=data_path)
                data_files = self.backtester._prepare_data_files()
            
            # Análisis de cada módulo
            modules_analysis = [
                ("ORDER_BLOCKS", self.backtester._analyze_order_blocks),
                ("FAIR_VALUE_GAPS", self.backtester._analyze_fair_value_gaps), 
                ("BREAKER_BLOCKS", self.backtester._analyze_breaker_blocks),
                ("SILVER_BULLET", self.backtester._analyze_silver_bullet),
                ("LIQUIDITY_POOLS", self.backtester._analyze_liquidity_pools),
                ("DISPLACEMENT", self.backtester._analyze_displacement)
            ]
            
            for module_key, analysis_func in modules_analysis:
                if not self.is_running:
                    break
                    
                try:
                    self.current_module = module_key
                    self.modules[module_key].rule10_status = "🔄"
                    
                    # Progreso gradual para efecto visual
                    for progress in range(0, 101, 25):
                        if not self.is_running:
                            break
                        self.modules[module_key].progress = progress
                        time.sleep(0.3)
                    
                    # Ejecutar análisis real silenciosamente
                    result = self._silent_analysis(analysis_func, data_files)
                    
                    # Actualizar con resultados reales
                    self.modules[module_key].patterns_found = result.patterns_detected
                    self.modules[module_key].precision = result.success_rate
                    self.modules[module_key].progress = 100.0
                    self.modules[module_key].rule10_status = "✅" if result.success_rate >= 80.0 else "❌"
                    
                    # Log detallado para archivo final
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
                    
                except Exception as e:
                    # Manejar errores por módulo sin detener todo
                    self.modules[module_key].rule10_status = "❌"
                    self.modules[module_key].progress = 100.0
                    self.execution_log.append({
                        "module": module_key,
                        "error": str(e),
                        "regla10_compliant": False,
                        "timestamp": datetime.now().isoformat()
                    })
                
                time.sleep(0.5)  # Pausa entre módulos
            
            self.current_module = "COMPLETED"
            
        except Exception as e:
            self.execution_log.append({
                "critical_error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            self.current_module = "ERROR"
    
    def _save_detailed_report(self):
        """Guardar TODA la información detallada en archivo"""
        try:
            reports_dir = Path(__file__).parent.parent / "test_reports"
            reports_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Reporte COMPLETO como pediste
            complete_report = {
                "dashboard_summary": {
                    "execution_timestamp": datetime.now().isoformat(),
                    "total_duration_seconds": (datetime.now() - self.session_start).total_seconds(),
                    "total_patterns_found": sum(m.patterns_found for m in self.modules.values()),
                    "regla10_compliance_score": sum(1 for m in self.modules.values() if m.rule10_status == "✅"),
                    "overall_regla10_status": "COMPLIANT" if sum(1 for m in self.modules.values() if m.rule10_status == "✅") >= 4 else "NON_COMPLIANT"
                },
                "modules_detailed_results": {
                    name: {
                        "patterns_found": module.patterns_found,
                        "precision_percentage": module.precision,
                        "regla10_status": module.rule10_status,
                        "final_progress": module.progress
                    }
                    for name, module in self.modules.items()
                },
                "complete_execution_log": self.execution_log,
                "regla10_detailed_evaluation": {
                    "total_modules_analyzed": len(self.modules),
                    "modules_passed_regla10": sum(1 for m in self.modules.values() if m.rule10_status == "✅"),
                    "modules_failed_regla10": sum(1 for m in self.modules.values() if m.rule10_status == "❌"),
                    "regla10_compliance_percentage": (sum(1 for m in self.modules.values() if m.rule10_status == "✅") / len(self.modules)) * 100,
                    "system_overall_status": "ENTERPRISE_COMPLIANT" if sum(1 for m in self.modules.values() if m.rule10_status == "✅") >= 5 else "REQUIRES_REVIEW"
                },
                "technical_details": {
                    "backtester_used": "ModularICTBacktester",
                    "data_source": "Real historical data",
                    "analysis_mode": "Live real-time analysis",
                    "regla10_threshold": "80% success rate minimum",
                    "dashboard_version": "Final Minimal v1.0"
                }
            }
            
            report_file = reports_dir / f"ict_final_minimal_regla10_{timestamp}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(complete_report, f, indent=2, ensure_ascii=False)
            
            return str(report_file)
            
        except Exception:
            return None
    
    def run(self):
        """Ejecutar dashboard final minimalista"""
        print("LOG: Iniciando run()")
        try:
            print("LOG: Limpiando console...")
            self.console.clear()
            
            # Header como pediste
            print("LOG: Creando title panel...")
            title = Panel.fit(
                "[bold bright_cyan]🎯 ICT ENGINE - REGLA #10 DASHBOARD[/bold bright_cyan]",
                style="bright_cyan"
            )
            
            # Mostrar header inicial
            print("LOG: Mostrando header...")
            self.console.print(title)
            self.console.print()
            
            print("LOG: Configurando is_running = True")
            self.is_running = True
            
            # Hilo de análisis
            print("LOG: Creando thread de análisis...")
            analysis_thread = threading.Thread(target=self.run_analysis)
            analysis_thread.daemon = True
            print("LOG: Iniciando thread...")
            analysis_thread.start()
            print("LOG: Thread iniciado exitosamente")
            
            # Display en tiempo real con manejo de errores mejorado
            try:
                print("LOG: Iniciando Live display...")
                # Crear la primera tabla para inicializar Live
                initial_table = self._create_minimal_table()
                
                with Live(initial_table, refresh_per_second=3, console=self.console) as live:
                    print("LOG: Live display activo")
                    while self.is_running and analysis_thread.is_alive():
                        
                        # Crear display actual
                        table = self._create_minimal_table()
                        print(f"LOG: Tabla actualizada, current_module: {self.current_module}")
                        
                        # Status actual
                        if self.current_module == "COMPLETED":
                            total_patterns = sum(m.patterns_found for m in self.modules.values())
                            passed = sum(1 for m in self.modules.values() if m.rule10_status == "✅")
                            status_line = f"[green]✅ ANÁLISIS COMPLETADO: {total_patterns:,} patterns detectados | REGLA #10: {passed}/6 módulos[/green]"
                            
                            # Actualizar solo la tabla y salir
                            live.update(table)
                            print("LOG: Análisis completado, mostrando resultado final...")
                            time.sleep(3)  # Mostrar resultado final por 3 segundos
                            break
                            
                        elif self.current_module:
                            status_line = f"[yellow]🔍 Analizando: {self.current_module}...[/yellow]"
                        else:
                            status_line = "[dim]Inicializando análisis del sistema real...[/dim]"
                        
                        # Actualizar solo la tabla (sin combinar strings)
                        live.update(table)
                        
                        time.sleep(0.3)
                
                print("LOG: Live display terminado")
                        
            except KeyboardInterrupt:
                print("LOG: Interrupción por teclado detectada")
                self.is_running = False
                self.console.print("\n[yellow]⚠️ Dashboard interrumpido por usuario[/yellow]")
            except Exception as e:
                print(f"LOG: ERROR en Live display: {e}")
                self.console.print(f"\n[red]❌ Error en display: {e}[/red]")
            
            print("LOG: Esperando finalización del thread...")
            # Esperar a que termine el análisis
            if analysis_thread.is_alive():
                analysis_thread.join(timeout=5)
            
            # Mostrar resultado final estático
            self.console.clear()
            self.console.print(title)
            self.console.print()
            self.console.print(self._create_minimal_table())
            self.console.print()
            
            # Guardar reporte detallado
            report_file = self._save_detailed_report()
            if report_file:
                self.console.print(f"[green]💾 Reporte completo guardado en:[/green]")
                self.console.print(f"[dim]{report_file}[/dim]")
            
            duration = (datetime.now() - self.session_start).total_seconds()
            total_patterns = sum(m.patterns_found for m in self.modules.values())
            passed_modules = sum(1 for m in self.modules.values() if m.rule10_status == "✅")
            
            self.console.print(f"\n[green]✅ Análisis completado en {duration:.1f}s[/green]")
            self.console.print(f"[cyan]📊 Total patterns: {total_patterns:,} | REGLA #10: {passed_modules}/6 módulos aprobados[/cyan]")
            
        except Exception as e:
            self.console.print(f"[red]❌ Error crítico en dashboard: {e}[/red]")
            import traceback
            self.console.print(f"[red]{traceback.format_exc()}[/red]")

def main():
    print("LOG: main() iniciado")
    try:
        print("LOG: Creando instancia de ICTFinalDashboard...")
        dashboard = ICTFinalDashboard()
        print("LOG: Dashboard creado exitosamente")
        print("LOG: Ejecutando dashboard.run()...")
        dashboard.run()
        print("LOG: dashboard.run() completado")
    except Exception as e:
        print(f"LOG: ERROR CRÍTICO en main(): {e}")
        import traceback
        print(f"LOG: Traceback completo:")
        traceback.print_exc()

if __name__ == "__main__":
    print("LOG: Script iniciado (__main__)")
    main()
    print("LOG: Script completado")
