#!/usr/bin/env python3
"""
🎯 ICT DASHBOARD MINIMAL - SOLO LO ESENCIAL
===========================================

Dashboard ultra-minimalista que muestra únicamente:
- ✅ Barras de progreso en tiempo real
- ✅ Patterns detectados 
- ✅ Precisión por módulo
- ✅ Estado Regla 10
- ✅ Resultado final con ubicación del archivo

❌ SIN logs innecesarios
❌ SIN información técnica
❌ SIN duplicaciones

Autor: ICT Engine Team
Versión: 1.0-minimal
"""

import time
import threading
from datetime import datetime
from pathlib import Path
from maestro_wrapper import MaestroWrapper
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.text import Text

class ICTDashboardMinimal:
    """Dashboard ultra-limpio para análisis ICT"""
    
    def __init__(self):
        self.console = Console()
        self.wrapper = MaestroWrapper()
        self.modules = {
            "ORDER_BLOCKS": {"progress": 0, "patterns": 0, "precision": 0, "rule10": "⏳"},
            "FAIR_VALUE_GAPS": {"progress": 0, "patterns": 0, "precision": 0, "rule10": "⏳"},
            "BREAKER_BLOCKS": {"progress": 0, "patterns": 0, "precision": 0, "rule10": "⏳"},
            "SILVER_BULLET": {"progress": 0, "patterns": 0, "precision": 0, "rule10": "⏳"},
            "LIQUIDITY": {"progress": 0, "patterns": 0, "precision": 0, "rule10": "⏳"}
        }
        self.total_patterns = 0
        self.execution_complete = False
        self.results_file = ""
        
    def _create_minimal_table(self) -> Table:
        """Crear tabla minimalista"""
        table = Table(show_header=True, header_style="bold blue", box=None)
        table.add_column("🎯 MÓDULO", style="bold white", width=20)
        table.add_column("PROGRESO", style="cyan", width=15) 
        table.add_column("PATTERNS", style="green", width=12)
        table.add_column("PRECISIÓN", style="yellow", width=10)
        table.add_column("REGLA 10", style="magenta", width=8)
        
        for module_name, data in self.modules.items():
            # Iconos por módulo
            icons = {
                "ORDER_BLOCKS": "🎯", "FAIR_VALUE_GAPS": "📏", 
                "BREAKER_BLOCKS": "🧱", "SILVER_BULLET": "🥈", "LIQUIDITY": "💧"
            }
            
            # Barra de progreso
            progress = data["progress"]
            if progress == 100:
                bar = "████████████ 100%"
            elif progress > 0:
                filled = int(progress / 8.33)  # 12 bloques
                bar = f"{'█' * filled}{'░' * (12 - filled)} {progress:3.0f}%"
            else:
                bar = "░░░░░░░░░░░░   0%"
            
            # Formatear datos
            patterns = f"{data['patterns']:,}" if data['patterns'] > 0 else "-"
            precision = f"{data['precision']:.1f}%" if data['precision'] > 0 else "-"
            
            table.add_row(
                f"{icons.get(module_name, '⚡')} {module_name}",
                bar,
                patterns,
                precision,
                data['rule10']
            )
        
        return table
    
    def _create_status_panel(self) -> Panel:
        """Panel de estado minimalista"""
        if self.execution_complete:
            content = f"""🎉 [bold green]ANÁLISIS COMPLETADO[/bold green]

📊 Total Patterns: [bold cyan]{self.total_patterns:,}[/bold cyan]
🎯 Regla 10: [bold green]5/5 ✅[/bold green]
⏱️  Duración: [bold yellow]{getattr(self, 'execution_time', 'N/A')}s[/bold yellow]

💾 [bold white]Archivo guardado:[/bold white]
📁 [dim]{Path(self.results_file).parent}[/dim]
📄 [bold cyan]{Path(self.results_file).name}[/bold cyan]"""
        else:
            content = f"""⚡ [bold yellow]ANÁLISIS EN PROGRESO...[/bold yellow]

📊 Patterns detectados: [bold cyan]{self.total_patterns:,}[/bold cyan]
🔄 Módulos procesándose...
⏱️  Duración: [bold white]{time.time() - self.start_time:.1f}s[/bold white]"""
        
        return Panel(
            content, 
            title="🎛️ Estado del Sistema",
            border_style="blue",
            padding=(1, 2)
        )
    
    def _update_modules_from_blackbox(self):
        """Actualizar datos desde blackbox"""
        try:
            dashboard_data = self.wrapper._load_from_blackbox("dashboard_metrics.json")
            if dashboard_data:
                modules_data = dashboard_data.get("modules", {})
                
                for module_name in self.modules:
                    if module_name in modules_data:
                        module_data = modules_data[module_name]
                        self.modules[module_name].update({
                            "progress": module_data.get("progress", 0),
                            "patterns": module_data.get("patterns_found", 0),
                            "precision": module_data.get("precision", 0),
                            "rule10": "✅" if module_data.get("progress", 0) == 100 else "⏳"
                        })
                
                # Actualizar totales
                self.total_patterns = sum(m["patterns"] for m in self.modules.values())
                
                # Verificar si está completo
                completed_modules = sum(1 for m in self.modules.values() if m["progress"] == 100)
                if completed_modules == len(self.modules):
                    self.execution_complete = True
                    # Buscar archivo de resultados
                    execution_data = self.wrapper._load_from_blackbox("execution_metadata.json")
                    if execution_data:
                        self.results_file = execution_data.get("final_report_path", "")
                        self.execution_time = execution_data.get("total_execution_time", 0)
        except:
            pass  # Silenciar errores de lectura
    
    def run(self):
        """Ejecutar dashboard minimal"""
        self.start_time = time.time()
        
        # Panel inicial
        self.console.print(Panel(
            f"""🚀 [bold blue]ICT ENGINE v6.0 ENTERPRISE[/bold blue]

⚡ Iniciando análisis maestro...
📊 Dashboard minimal activado
🎯 Solo lo esencial, sin ruido""",
            title="🎛️ Sistema Iniciando",
            border_style="green"
        ))
        
        # Ejecutar maestro en hilo separado
        maestro_thread = threading.Thread(target=self.wrapper.execute_maestro_silently)
        maestro_thread.daemon = True
        maestro_thread.start()
        
        # Layout principal
        layout = Layout()
        layout.split_column(
            Layout(name="table", size=12),
            Layout(name="status", size=8)
        )
        
        # Loop principal con Live display
        with Live(layout, refresh_per_second=2, screen=False) as live:
            while not self.execution_complete:
                # Actualizar datos
                self._update_modules_from_blackbox()
                
                # Actualizar layout
                layout["table"].update(self._create_minimal_table())
                layout["status"].update(self._create_status_panel())
                
                time.sleep(1)
            
            # Mostrar resultado final
            time.sleep(2)  # Pausa para mostrar resultado final
        
        # Resumen final
        if self.results_file:
            self.console.print(f"\n💡 [bold green]Tip:[/bold green] [dim]Archivo con todos los resultados guardado en {Path(self.results_file).name}[/dim]")

if __name__ == "__main__":
    dashboard = ICTDashboardMinimal()
    dashboard.run()
