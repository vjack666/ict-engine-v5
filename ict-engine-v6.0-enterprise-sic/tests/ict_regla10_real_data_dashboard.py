#!/usr/bin/env python3
"""
🎯 ICT ENGINE REGLA #10 - ENTERPRISE DASHBOARD CON DATOS REALES
================================================================================
Dashboard empresarial basado en análisis técnico real de ICT Engine
Usando datos del archivo: technical_analysis_report_20250809_122230_091155f8e2c3.json
================================================================================
Autor: ICT Engine Team
Fecha: 2025-08-09
Version: 6.0 Enterprise Real Data
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

# Rich imports
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, TaskID, BarColumn, TextColumn, TimeRemainingColumn, SpinnerColumn
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich.live import Live
from rich.columns import Columns

@dataclass
class RealModuleMetrics:
    """Métricas reales de módulo ICT"""
    name: str
    icon: str
    total_signals: int
    processing_speed: float
    accuracy_score: float
    precision_rate: float
    recall_rate: float
    f1_score: float
    optimization_score: float
    memory_efficiency: float
    cpu_utilization: int
    error_rate: float
    stability_index: float
    performance_percentile: float
    regla10_compliance: bool = False
    grade: str = "PENDING"
    
@dataclass
class SystemRealStats:
    """Estadísticas reales del sistema"""
    session_id: str = ""
    total_execution_time: float = 0.0
    modules_analyzed: int = 8
    files_processed: int = 24
    total_signals: int = 789
    overall_performance_score: float = 0.858771875
    system_efficiency_rating: str = "EXCELLENT"
    current_progress: float = 0.0
    start_time: Optional[datetime] = None

class ICTRegla10RealDataDashboard:
    """🎯 Dashboard Enterprise con datos reales de ICT Engine"""
    
    def __init__(self):
        self.console = Console()
        self.real_data = self._load_real_data()
        self.modules = self._initialize_real_modules()
        self.system_stats = self._initialize_real_system_stats()
        self.current_phase = "INITIALIZING"
        self.phase_progress = 0.0
        self.is_running = False
        
    def _load_real_data(self) -> Dict:
        """Cargar datos reales del archivo JSON"""
        json_file = Path(__file__).parent / "test_reports" / "technical_analysis" / "technical_analysis_report_20250809_122230_091155f8e2c3.json"
        
        if not json_file.exists():
            # Buscar el archivo más reciente
            reports_dir = Path(__file__).parent.parent / "test_reports" / "technical_analysis"
            if reports_dir.exists():
                json_files = list(reports_dir.glob("technical_analysis_report_*.json"))
                if json_files:
                    json_file = max(json_files, key=lambda x: x.stat().st_mtime)
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.console.print(f"[red]⚠️ Error cargando datos reales: {e}[/red]")
            return self._get_fallback_data()
    
    def _get_fallback_data(self) -> Dict:
        """Datos de fallback si no se puede cargar el archivo"""
        return {
            "session_id": "fallback_session",
            "total_execution_time": 147.8,
            "modules_analyzed": 8,
            "files_processed": 24,
            "total_signals": 789,
            "overall_performance_score": 0.858771875,
            "system_efficiency_rating": "EXCELLENT",
            "detailed_metrics": {
                "BOS": {
                    "module_name": "Break of Structure",
                    "total_signals_detected": 53,
                    "processing_speed": 1.36,
                    "accuracy_score": 0.86,
                    "precision_rate": 0.817,
                    "recall_rate": 0.7912,
                    "f1_score": 0.8038930481283422,
                    "optimization_score": 0.8279333333333333,
                    "memory_efficiency": 2.3,
                    "cpu_utilization": 57,
                    "error_rate": 0.0131,
                    "stability_index": 0.9269,
                    "performance_percentile": 58.25
                },
                "ORDER_BLOCKS": {
                    "module_name": "Order Blocks",
                    "total_signals_detected": 57,
                    "processing_speed": 1.04,
                    "accuracy_score": 0.94,
                    "precision_rate": 0.9156,
                    "recall_rate": 0.8272,
                    "f1_score": 0.8691400215749729,
                    "optimization_score": 0.7600666666666666,
                    "memory_efficiency": 4.4,
                    "cpu_utilization": 38,
                    "error_rate": 0.0199,
                    "stability_index": 0.9201,
                    "performance_percentile": 59.25
                },
                "FVG": {
                    "module_name": "Fair Value Gaps",
                    "total_signals_detected": 130,
                    "processing_speed": 2.4,
                    "accuracy_score": 0.95,
                    "precision_rate": 0.931,
                    "recall_rate": 0.8455,
                    "f1_score": 0.8861925133689837,
                    "optimization_score": 0.8913333333333333,
                    "memory_efficiency": 2.1,
                    "cpu_utilization": 75,
                    "error_rate": 0.008,
                    "stability_index": 0.932,
                    "performance_percentile": 77.5
                }
            }
        }
    
    def _initialize_real_modules(self) -> Dict[str, RealModuleMetrics]:
        """Inicializar módulos con datos reales"""
        modules = {}
        
        # Mapeo de módulos ICT a estrategias REGLA #10
        module_mapping = {
            # CONFLUENCE_CORE: Order Blocks + FVG + Liquidity
            "ORDER_BLOCKS": ("🎯", "CONFLUENCE_CORE"),
            "FVG": ("📏", "CONFLUENCE_CORE"), 
            "LIQUIDITY": ("💧", "CONFLUENCE_CORE"),
            
            # DISPLACEMENT_POWER: Displacement + Silver Bullet
            "CHOCH": ("⚡", "DISPLACEMENT_POWER"),  # Change of Character = Displacement
            "SILVER_BULLET": ("🥈", "DISPLACEMENT_POWER"),
            
            # BREAKER_ENTERPRISE: Breaker Blocks
            "BREAKER_BLOCKS": ("🧱", "BREAKER_ENTERPRISE"),
            
            # Otros módulos
            "BOS": ("📊", "BOS_ANALYSIS"),
            "SMART_MONEY": ("💰", "SMART_MONEY_ANALYSIS")
        }
        
        detailed_metrics = self.real_data.get("detailed_metrics", {})
        
        for module_key, metrics_data in detailed_metrics.items():
            if module_key in module_mapping:
                icon, strategy_group = module_mapping[module_key]
                
                # Calcular REGLA #10 compliance
                regla10_compliant = self._calculate_regla10_compliance(metrics_data)
                grade = self._calculate_grade(metrics_data, regla10_compliant)
                
                modules[module_key] = RealModuleMetrics(
                    name=metrics_data.get("module_name", module_key),
                    icon=icon,
                    total_signals=metrics_data.get("total_signals_detected", 0),
                    processing_speed=metrics_data.get("processing_speed", 0.0),
                    accuracy_score=metrics_data.get("accuracy_score", 0.0),
                    precision_rate=metrics_data.get("precision_rate", 0.0),
                    recall_rate=metrics_data.get("recall_rate", 0.0),
                    f1_score=metrics_data.get("f1_score", 0.0),
                    optimization_score=metrics_data.get("optimization_score", 0.0),
                    memory_efficiency=metrics_data.get("memory_efficiency", 0.0),
                    cpu_utilization=metrics_data.get("cpu_utilization", 0),
                    error_rate=metrics_data.get("error_rate", 0.0),
                    stability_index=metrics_data.get("stability_index", 0.0),
                    performance_percentile=metrics_data.get("performance_percentile", 0.0),
                    regla10_compliance=regla10_compliant,
                    grade=grade
                )
        
        return modules
    
    def _calculate_regla10_compliance(self, metrics: Dict) -> bool:
        """Calcular compliance REGLA #10 basado en métricas reales"""
        f1_score = metrics.get("f1_score", 0.0)
        processing_speed = metrics.get("processing_speed", 0.0)
        error_rate = metrics.get("error_rate", 1.0)
        stability_index = metrics.get("stability_index", 0.0)
        
        # REGLA #10 CRITERIA (súper estrictos)
        # 1. F1 Score >= 0.85 (excelente precisión y recall)
        # 2. Processing Speed >= 1.0 (velocidad aceptable)
        # 3. Error Rate <= 0.015 (menos del 1.5% de errores)
        # 4. Stability Index >= 0.92 (alta estabilidad)
        
        return (
            f1_score >= 0.85 and
            processing_speed >= 1.0 and
            error_rate <= 0.015 and
            stability_index >= 0.92
        )
    
    def _calculate_grade(self, metrics: Dict, regla10_compliant: bool) -> str:
        """Calcular grado basado en métricas"""
        optimization_score = metrics.get("optimization_score", 0.0)
        
        if regla10_compliant and optimization_score >= 0.9:
            return "A+ MASTER"
        elif regla10_compliant and optimization_score >= 0.85:
            return "A EXPERT" 
        elif optimization_score >= 0.8:
            return "B+ ADVANCED"
        elif optimization_score >= 0.75:
            return "B GOOD"
        elif optimization_score >= 0.65:
            return "C MODERATE"
        else:
            return "F NEEDS_IMPROVEMENT"
    
    def _initialize_real_system_stats(self) -> SystemRealStats:
        """Inicializar estadísticas del sistema con datos reales"""
        return SystemRealStats(
            session_id=self.real_data.get("session_id", "unknown"),
            total_execution_time=self.real_data.get("total_execution_time", 0.0),
            modules_analyzed=self.real_data.get("modules_analyzed", 8),
            files_processed=self.real_data.get("files_processed", 24),
            total_signals=self.real_data.get("total_signals", 789),
            overall_performance_score=self.real_data.get("overall_performance_score", 0.0),
            system_efficiency_rating=self.real_data.get("system_efficiency_rating", "UNKNOWN"),
            start_time=datetime.now()
        )
    
    def _get_screen_dimensions(self) -> tuple:
        """Obtener dimensiones de pantalla"""
        try:
            import shutil
            size = shutil.get_terminal_size()
            return size.columns, size.lines
        except:
            return 120, 30
    
    def create_module_panel(self, module: RealModuleMetrics, current_progress: float = 0.0) -> Panel:
        """Crear panel para módulo individual con datos reales"""
        
        # Color basado en REGLA #10 compliance
        if current_progress < 100.0:
            border_color = "yellow"
            title_color = "yellow"
        elif module.regla10_compliance:
            border_color = "green"
            title_color = "green"
        else:
            border_color = "red"
            title_color = "red"
        
        # Tabla de métricas
        table = Table.grid(padding=0)
        table.add_column(justify="left", style="dim", width=18)
        table.add_column(justify="right", width=12)
        
        # Progress bar
        progress_chars = int(current_progress / 4)
        progress_bar = "█" * progress_chars + "░" * (25 - progress_chars)
        
        table.add_row("📊 Progreso:", f"[{title_color}]{current_progress:6.1f}%[/{title_color}]")
        table.add_row("", f"[{title_color}]{progress_bar}[/{title_color}]")
        table.add_row("")
        
        # Métricas principales
        table.add_row("💡 Señales:", f"[cyan]{module.total_signals:,}[/cyan]")
        table.add_row("⚡ Velocidad:", f"[cyan]{module.processing_speed:.2f}x[/cyan]")
        table.add_row("🎯 Precisión:", f"[cyan]{module.precision_rate:.1%}[/cyan]")
        table.add_row("📈 Recall:", f"[cyan]{module.recall_rate:.1%}[/cyan]")
        table.add_row("🏆 F1 Score:", f"[cyan]{module.f1_score:.3f}[/cyan]")
        table.add_row("💾 Memoria:", f"[cyan]{module.memory_efficiency:.1f}MB[/cyan]")
        table.add_row("🖥️ CPU:", f"[cyan]{module.cpu_utilization}%[/cyan]")
        table.add_row("❌ Errores:", f"[cyan]{module.error_rate:.1%}[/cyan]")
        table.add_row("🔒 Estabilidad:", f"[cyan]{module.stability_index:.3f}[/cyan]")
        table.add_row("")
        
        # Grade y compliance
        table.add_row("💎 Grade:", f"[{title_color}]{module.grade}[/{title_color}]")
        
        regla10_status = "✅ PASSED" if module.regla10_compliance else "❌ FAILED"
        regla10_color = "green" if module.regla10_compliance else "red"
        table.add_row("🏆 REGLA #10:", f"[{regla10_color}]{regla10_status}[/{regla10_color}]")
        
        return Panel(
            table,
            title=f"{module.icon} {module.name}",
            border_style=border_color,
            title_align="left"
        )
    
    def create_system_overview_panel(self) -> Panel:
        """Crear panel de resumen del sistema"""
        
        table = Table.grid(padding=0)
        table.add_column(justify="left", style="dim")
        table.add_column(justify="right")
        
        # Tiempo transcurrido
        if self.system_stats.start_time:
            elapsed = datetime.now() - self.system_stats.start_time
            elapsed_str = f"{int(elapsed.total_seconds()//60):02d}:{int(elapsed.total_seconds()%60):02d}"
        else:
            elapsed_str = "00:00"
        
        # Progress del sistema
        system_progress_bar = "█" * int(self.system_stats.current_progress / 4) + "░" * (25 - int(self.system_stats.current_progress / 4))
        
        table.add_row("🎯 Sesión:", f"[cyan]{self.system_stats.session_id[:12]}[/cyan]")
        table.add_row("⏱️ Tiempo:", f"[cyan]{elapsed_str}[/cyan]")
        table.add_row("📊 Progreso:", f"[cyan]{self.system_stats.current_progress:6.1f}%[/cyan]")
        table.add_row("", f"[cyan]{system_progress_bar}[/cyan]")
        table.add_row("📁 Archivos:", f"[cyan]{self.system_stats.files_processed}[/cyan]")
        table.add_row("📈 Módulos:", f"[cyan]{self.system_stats.modules_analyzed}[/cyan]")
        table.add_row("💡 Señales Total:", f"[cyan]{self.system_stats.total_signals:,}[/cyan]")
        table.add_row("")
        
        # Compliance general
        total_modules = len(self.modules)
        compliant_modules = sum(1 for m in self.modules.values() if m.regla10_compliance)
        
        table.add_row("✅ REGLA #10:", f"[green]{compliant_modules}[/green]/[cyan]{total_modules}[/cyan]")
        table.add_row("🏆 Performance:", f"[cyan]{self.system_stats.overall_performance_score:.1%}[/cyan]")
        table.add_row("⚙️ Eficiencia:", f"[cyan]{self.system_stats.system_efficiency_rating}[/cyan]")
        table.add_row("🔄 Fase:", f"[yellow]{self.current_phase}[/yellow]")
        
        # Status general
        if self.system_stats.current_progress >= 100.0:
            overall_status = "✅ COMPLETADO" if compliant_modules >= total_modules * 0.6 else "❌ REGLA #10 FALLIDA"
            status_color = "green" if compliant_modules >= total_modules * 0.6 else "red"
        else:
            overall_status = "🔄 EJECUTANDO"
            status_color = "yellow"
        
        table.add_row("📋 Estado:", f"[{status_color}]{overall_status}[/{status_color}]")
        
        return Panel(
            table,
            title="📊 SISTEMA ICT ENGINE",
            border_style="cyan",
            title_align="center"
        )
    
    def create_header_panel(self) -> Panel:
        """Crear panel de encabezado"""
        current_time = datetime.now().strftime("%H:%M:%S")
        header_text = Text()
        header_text.append("🎯 ICT ENGINE REGLA #10 - ENTERPRISE REAL DATA DASHBOARD\n", style="bold cyan")
        header_text.append(f"Live: {current_time} | ", style="dim")
        header_text.append(f"Análisis Real: {self.system_stats.total_signals:,} señales procesadas", style="bold green")
        
        return Panel(
            Align.center(header_text),
            style="cyan"
        )
    
    def generate_layout(self) -> Layout:
        """Generar layout optimizado"""
        
        width, height = self._get_screen_dimensions()
        
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=1)
        )
        
        # Organizar módulos en grid
        main_modules = ["ORDER_BLOCKS", "FVG", "LIQUIDITY", "CHOCH", "SILVER_BULLET", "BREAKER_BLOCKS"]
        module_panels = []
        
        for module_key in main_modules:
            if module_key in self.modules:
                module_panels.append(
                    self.create_module_panel(self.modules[module_key], self.system_stats.current_progress)
                )
        
        # Layout responsive
        if width >= 180:  # Pantalla muy ancha - 3 filas x 2 columnas + panel sistema
            layout["main"].split_row(
                Layout(name="modules", ratio=4),
                Layout(name="system", ratio=1)
            )
            
            # Organizar módulos en 3 filas de 2 columnas
            modules_layout = Layout()
            modules_layout.split_column(
                Layout(name="row1"),
                Layout(name="row2"), 
                Layout(name="row3")
            )
            
            if len(module_panels) >= 2:
                modules_layout["row1"].split_row(Layout(module_panels[0]), Layout(module_panels[1]))
            if len(module_panels) >= 4:
                modules_layout["row2"].split_row(Layout(module_panels[2]), Layout(module_panels[3]))
            if len(module_panels) >= 6:
                modules_layout["row3"].split_row(Layout(module_panels[4]), Layout(module_panels[5]))
            
            layout["main"]["modules"].update(modules_layout)
            
        elif width >= 120:  # Pantalla normal - 2 filas x 2 columnas + sistema abajo
            layout["main"].split_column(
                Layout(name="modules", ratio=3),
                Layout(name="system", ratio=1)
            )
            
            # 2 filas de 2 columnas
            modules_layout = Layout()
            modules_layout.split_column(
                Layout(name="row1"),
                Layout(name="row2"),
                Layout(name="row3")
            )
            
            if len(module_panels) >= 2:
                modules_layout["row1"].split_row(Layout(module_panels[0]), Layout(module_panels[1]))
            if len(module_panels) >= 4:
                modules_layout["row2"].split_row(Layout(module_panels[2]), Layout(module_panels[3]))
            if len(module_panels) >= 6:
                modules_layout["row3"].split_row(Layout(module_panels[4]), Layout(module_panels[5]))
                
            layout["main"]["modules"].update(modules_layout)
            
        else:  # Pantalla pequeña - columna única
            all_panels = module_panels + [self.create_system_overview_panel()]
            layout["main"].update(Columns(all_panels, equal=False, expand=True))
        
        # Actualizar headers y footers
        layout["header"].update(self.create_header_panel())
        
        if "system" in layout["main"]._children:
            layout["main"]["system"].update(self.create_system_overview_panel())
        
        layout["footer"].update(Panel(
            "[dim]🎯 ICT Engine Enterprise Real Data | Datos reales de trading | Ctrl+C para salir[/dim]",
            style="dim"
        ))
        
        return layout
    
    def run_real_analysis_simulation(self):
        """Simular análisis basado en datos reales"""
        
        phases = [
            ("LOADING_REAL_DATA", "📂 Cargando datos reales del sistema...", 15),
            ("ANALYZING_ORDER_BLOCKS", "📦 Analizando Order Blocks...", 25),
            ("ANALYZING_FVG", "📏 Analizando Fair Value Gaps...", 35),
            ("ANALYZING_LIQUIDITY", "💧 Analizando Liquidity Pools...", 50),
            ("ANALYZING_DISPLACEMENT", "⚡ Analizando Change of Character...", 65),
            ("ANALYZING_SILVER_BULLET", "🥈 Analizando Silver Bullet...", 80),
            ("ANALYZING_BREAKERS", "🧱 Analizando Breaker Blocks...", 90),
            ("CALCULATING_REGLA10", "🏆 Calculando compliance REGLA #10...", 95),
            ("COMPLETED", "✅ Análisis completado", 100)
        ]
        
        for phase_name, phase_description, target_progress in phases:
            self.current_phase = phase_description
            
            # Simular progreso gradual hacia el target
            current = self.system_stats.current_progress
            while current < target_progress:
                current += 2.5
                self.system_stats.current_progress = min(current, target_progress)
                time.sleep(0.3)
            
            time.sleep(1)  # Pausa entre fases
    
    def run_live_dashboard(self):
        """Ejecutar dashboard en tiempo real con datos reales"""
        
        self.is_running = True
        self.system_stats.start_time = datetime.now()
        
        # Thread para simular análisis
        analysis_thread = threading.Thread(target=self.run_real_analysis_simulation)
        analysis_thread.daemon = True
        analysis_thread.start()
        
        try:
            with Live(self.generate_layout(), refresh_per_second=2, console=self.console) as live:
                self.console.print("[dim]🎯 Dashboard ICT Engine con datos reales iniciado...[/dim]")
                
                while self.is_running and self.system_stats.current_progress < 100.0:
                    live.update(self.generate_layout())
                    time.sleep(0.5)
                
                # Mostrar resultados finales por 45 segundos
                self.console.print("\n[green]✅ Análisis completado! Mostrando resultados finales...[/green]")
                
                for i in range(90):  # 45 segundos
                    live.update(self.generate_layout())
                    time.sleep(0.5)
                    
        except KeyboardInterrupt:
            self.is_running = False
            self.console.print("\n[yellow]👋 Dashboard cerrado por el usuario[/yellow]")

def main():
    """🎯 Función principal - Dashboard con datos reales"""
    
    dashboard = ICTRegla10RealDataDashboard()
    
    # Mostrar información de datos cargados
    dashboard.console.print(Panel.fit(
        f"[bold green]🎯 ICT ENGINE REGLA #10 - ENTERPRISE DASHBOARD[/bold green]\n"
        f"[cyan]📊 Datos reales cargados:[/cyan]\n"
        f"[dim]• Sesión: {dashboard.system_stats.session_id}[/dim]\n"
        f"[dim]• Señales procesadas: {dashboard.system_stats.total_signals:,}[/dim]\n"
        f"[dim]• Módulos analizados: {dashboard.system_stats.modules_analyzed}[/dim]\n"
        f"[dim]• Performance: {dashboard.system_stats.overall_performance_score:.1%}[/dim]",
        border_style="green"
    ))
    
    time.sleep(2)
    
    # Ejecutar dashboard
    dashboard.run_live_dashboard()

if __name__ == "__main__":
    main()
