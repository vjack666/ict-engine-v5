#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 DASHBOARD SIMPLE ICT - SOLO LECTURA DE DATOS REALES
======================================================
Dashboard que lee directamente el último archivo JSON del maestro
Sin fallbacks, solo datos reales del modular_ict_backtester.py
"""

import json
import os
import glob
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
import time

console = Console()

def find_latest_json():
    """Busca el último archivo JSON generado por el maestro"""
    results_dir = r"c:\Users\v_jac\Desktop\itc engine v5.0\ict-engine-v6.0-enterprise-sic\data\backtest_results"
    pattern = os.path.join(results_dir, "modular_backtest_fase*.json")
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)

def load_results():
    """Carga los resultados del último test"""
    json_file = find_latest_json()
    if not json_file:
        return None
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[red]Error cargando {json_file}: {e}[/red]")
        return None

def create_dashboard(data):
    """Crea el dashboard con datos reales"""
    if not data:
        return Panel("❌ No se encontraron datos del maestro", 
                    title="🎯 ICT Dashboard", 
                    border_style="red")
    
    # Header con resumen ejecutivo
    summary = data.get('summary', {})
    total_patterns = summary.get('total_patterns', 'N/A')
    total_signals = summary.get('total_signals', 'N/A')
    total_data = summary.get('total_data_points', 'N/A')
    
    patterns_str = f"{total_patterns:,}" if isinstance(total_patterns, int) else str(total_patterns)
    signals_str = f"{total_signals:,}" if isinstance(total_signals, int) else str(total_signals)
    data_str = f"{total_data:,}" if isinstance(total_data, int) else str(total_data)
    
    header = f"""[bold green]📊 RESULTADOS BACKTEST MODULAR - FASE 5[/bold green]

🎯 RESUMEN EJECUTIVO:
   ⏱️  Tiempo total: {summary.get('total_time', 'N/A')}
   📊 Datos analizados: {data_str}
   🔍 Patterns detectados: {patterns_str}
   💡 Señales generadas: {signals_str}
   📈 Success rate: {summary.get('overall_success_rate', 'N/A')}%
   🏆 Grade: {summary.get('grade', 'N/A')}"""
    
    # Tabla de módulos
    modules_table = Table(title="🔧 ANÁLISIS POR MÓDULO")
    modules_table.add_column("Módulo", style="cyan")
    modules_table.add_column("Patterns", justify="right", style="yellow")
    modules_table.add_column("Señales", justify="right", style="green")
    modules_table.add_column("Success %", justify="right", style="magenta")
    modules_table.add_column("Confianza %", justify="right", style="blue")
    modules_table.add_column("Tiempo", justify="right", style="white")
    
    modules = data.get('modules', {})
    for module_name, module_data in modules.items():
        patterns = module_data.get('patterns_count', 0)
        signals = module_data.get('signals_count', 0)
        success = module_data.get('success_rate', 0)
        confidence = module_data.get('confidence', 0)
        time_taken = module_data.get('execution_time', 'N/A')
        
        # Emoji por módulo
        emoji_map = {
            'order_blocks': '📦',
            'fair_value_gaps': '📏',
            'breaker_blocks': '🧱',
            'silver_bullet': '🥈',
            'liquidity_pools': '💧',
            'displacement': '⚡',
            'fractal_analysis': '🔄',
            'multi_pattern': '🔄'
        }
        emoji = emoji_map.get(module_name, '🔍')
        
        modules_table.add_row(
            f"{emoji} {module_name.replace('_', ' ').title()}",
            f"{patterns:,}",
            f"{signals:,}",
            f"{success:.1f}",
            f"{confidence:.1f}",
            f"{time_taken}"
        )
    
    # Footer con detalles
    symbols = ", ".join(data.get('symbols', []))
    timeframes = ", ".join(data.get('timeframes', []))
    date_range = data.get('date_range', {})
    
    latest_file = find_latest_json()
    filename = latest_file.split(os.sep)[-1] if latest_file else 'N/A'
    
    footer = f"""📈 SÍMBOLOS: {symbols}
⏰ TIMEFRAMES: {timeframes}
📅 RANGO: {date_range.get('start', 'N/A')} → {date_range.get('end', 'N/A')}

💾 Archivo: {filename}"""
    
    # Layout combinado
    layout = Layout()
    layout.split_column(
        Layout(Panel(header, border_style="green"), name="header"),
        Layout(modules_table, name="table"),
        Layout(Panel(footer, border_style="blue"), name="footer")
    )
    
    return layout

def main():
    """Dashboard principal"""
    console.clear()
    console.print("[bold yellow]🎯 ICT DASHBOARD SIMPLE - INICIANDO...[/bold yellow]")
    
    # Cargar datos una sola vez
    data = load_results()
    
    if not data:
        console.print("[red]❌ No se encontraron resultados del maestro[/red]")
        console.print("[yellow]🔄 Ejecuta primero: python modular_ict_backtester.py[/yellow]")
        return
    
    # Mostrar dashboard estático
    dashboard = create_dashboard(data)
    console.print(dashboard)
    
    console.print("\n[bold green]✅ DASHBOARD COMPLETADO - Datos cargados exitosamente[/bold green]")
    
    # Mostrar ubicación del archivo
    json_file = find_latest_json()
    if json_file:
        console.print(f"[cyan]📁 Archivo fuente: {json_file}[/cyan]")

if __name__ == "__main__":
    main()
