#!/usr/bin/env python3
"""
🚨 ITC ENGINE v5.0 - RENDERIZADOR PESTAÑA PROBLEMAS DASHBOARD
=============================================================

🎯 OBJETIVO: Renderizar pestaña "🚨 Problemas" en el dashboard principal
            con integración completa del Sistema de Detección de Errores

📊 CARACTERÍSTICAS:
   - ✅ Interfaz rica con Rich/Panel
   - ✅ Clasificación jerárquica de problemas
   - ✅ Filtros por severidad y categoría
   - ✅ Ejecutión automática de detección
   - ✅ Navegación interactiva
   - ✅ Métricas en tiempo real

🎨 INTEGRACIÓN:
   - Función principal: render_problems_tab()
   - Auto-detección y carga de problemas
   - UI responsiva y clara
   - Botones de acción

📅 Fecha: 2025-08-06 | Versión: 1.0.0
👤 Autor: ITC Engine v5.0 System
"""

# MIGRACIÓN SIC v3.0 + SLUC v2.1
from sistema.sic import enviar_senal_log, log_info, log_warning

from sistema.sic import json
from sistema.sic import os
from sistema.sic import sys
from sistema.sic import Path
from sistema.sic import Dict, List, Any, Optional, Tuple
from sistema.sic import datetime
import subprocess
import time

# Importaciones de Rich para UI
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.tree import Tree
    from rich.columns import Columns
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
    from rich.layout import Layout
    from rich.align import Align
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Configuración global
WORKSPACE_ROOT = Path(__file__).parent.parent
ERROR_DETECTOR_SCRIPT = WORKSPACE_ROOT / "scripts" / "error_detection" / "error_detector.py"
DIAGNOSTICS_DIR = WORKSPACE_ROOT / "docs" / "bitacoras" / "diagnosticos"


class ProblemsTabRenderer:
    """🚨 Renderizador de la pestaña Problemas del Dashboard"""

    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.current_problems: List[Dict] = []
        self.current_stats: Dict = {}
        self.filters = {
            'severity': None,
            'category': None,
            'show_resolved': False
        }

    def render_tab(self) -> str:
        """🎨 Renderizar pestaña completa de problemas"""
        if not RICH_AVAILABLE:
            return self._render_simple_tab()

        try:
            # Cargar datos más recientes
            self._load_latest_detection_data()

            # Crear layout principal
            layout = Layout()

            # Dividir en secciones
            layout.split_column(
                Layout(name="header", size=3),
                Layout(name="main"),
                Layout(name="footer", size=3)
            )

            # Dividir main en estadísticas y problemas
            layout["main"].split_row(
                Layout(name="stats", ratio=1),
                Layout(name="problems", ratio=2)
            )

            # Renderizar cada sección
            layout["header"].update(self._render_header())
            layout["stats"].update(self._render_statistics())
            layout["problems"].update(self._render_problems_list())
            layout["footer"].update(self._render_actions())

            # Convertir a string
            return str(layout)

        except Exception as e:
            return self._render_error_panel(f"Error renderizando pestaña: {str(e)}")

    def _render_simple_tab(self) -> str:
        """📝 Renderizado simple sin Rich"""
        try:
            self._load_latest_detection_data()

            output = []
            output.append("🚨 PROBLEMAS DETECTADOS - ITC ENGINE v5.0")
            output.append("=" * 50)
            output.append("")

            # Estadísticas básicas
            output.append(f"📊 Total problemas: {len(self.current_problems)}")
            if self.current_stats:
                for severity, count in self.current_stats.get('by_severity', {}).items():
                    if count > 0:
                        output.append(f"   {severity}: {count}")
            output.append("")

            # Lista de problemas críticos
            critical_problems = [p for p in self.current_problems if 'CRITICAL' in p.get('severity', '')]
            if critical_problems:
                output.append("🚨 PROBLEMAS CRÍTICOS:")
                for problem in critical_problems[:5]:
                    output.append(f"   • {problem.get('title', 'Sin título')}")
                    output.append(f"     📁 {problem.get('file_path', '')}")
                    output.append("")

            return "\n".join(output)

        except Exception as e:
            return f"❌ Error cargando problemas: {str(e)}"

    def _render_header(self) -> Panel:
        """🎯 Renderizar header de la pestaña"""
        title = Text("🚨 SISTEMA DE DETECCIÓN DE ERRORES", style="bold red")
        subtitle = Text("Análisis jerárquico en tiempo real", style="dim")

        header_content = Align.center(
            Text.assemble(title, "\n", subtitle)
        )

        return Panel(
            header_content,
            box=box.DOUBLE,
            border_style="red",
            padding=(0, 1)
        )

    def _render_statistics(self) -> Panel:
        """📊 Renderizar panel de estadísticas"""
        if not self.current_stats:
            return Panel("📊 Sin datos estadísticos", border_style="yellow")

        # Tabla de estadísticas principales
        stats_table = Table(show_header=False, box=None)
        stats_table.add_column("Métrica", style="cyan")
        stats_table.add_column("Valor", style="bold white")

        stats_table.add_row("📁 Archivos", str(self.current_stats.get('files_analyzed', 0)))
        stats_table.add_row("🚨 Problemas", str(len(self.current_problems)))

        # Desglose por severidad
        severity_stats = self.current_stats.get('by_severity', {})
        for severity, count in severity_stats.items():
            if count > 0:
                emoji = self._get_severity_emoji(severity)
                stats_table.add_row(f"{emoji} {severity}", str(count))

        # Tiempo de análisis
        analysis_time = self.current_stats.get('analysis_time', 0)
        stats_table.add_row("⏱️ Tiempo", f"{analysis_time:.1f}s")

        return Panel(
            stats_table,
            title="📊 Estadísticas",
            border_style="cyan"
        )

    def _render_problems_list(self) -> Panel:
        """📋 Renderizar lista de problemas"""
        if not self.current_problems:
            return Panel(
                Align.center("✅ No hay problemas detectados"),
                title="📋 Problemas",
                border_style="green"
            )

        # Filtrar problemas
        filtered_problems = self._apply_filters()

        if not filtered_problems:
            return Panel(
                Align.center("🔍 Sin problemas con los filtros actuales"),
                title="📋 Problemas (filtrados)",
                border_style="yellow"
            )

        # Crear tabla de problemas
        problems_table = Table(show_header=True, header_style="bold magenta")
        problems_table.add_column("🎯 Severidad", width=12)
        problems_table.add_column("📁 Archivo", width=25)
        problems_table.add_column("📝 Problema", width=40)
        problems_table.add_column("💡 Sugerencia", width=30)

        # Mostrar solo los primeros 10 para no saturar
        for problem in filtered_problems[:10]:
            severity = self._format_severity(problem.get('severity', ''))
            file_name = Path(problem.get('file_path', '')).name
            title = problem.get('title', 'Sin título')[:35] + "..." if len(problem.get('title', '')) > 35 else problem.get('title', '')
            suggestion = problem.get('suggestion', '')[:25] + "..." if len(problem.get('suggestion', '')) > 25 else problem.get('suggestion', '')

            problems_table.add_row(severity, file_name, title, suggestion)

        # Agregar footer si hay más problemas
        if len(filtered_problems) > 10:
            problems_table.add_row(
                "...", "...", f"... y {len(filtered_problems) - 10} más", "..."
            )

        return Panel(
            problems_table,
            title=f"📋 Problemas ({len(filtered_problems)} total)",
            border_style="red" if any('CRITICAL' in p.get('severity', '') for p in filtered_problems) else "yellow"
        )

    def _render_actions(self) -> Panel:
        """🎮 Renderizar panel de acciones"""
        actions_text = Text()
        actions_text.append("🔄 [R]efresh", style="bold cyan")
        actions_text.append(" • ")
        actions_text.append("🔍 [D]etectar", style="bold green")
        actions_text.append(" • ")
        actions_text.append("📊 [E]stadísticas", style="bold yellow")
        actions_text.append(" • ")
        actions_text.append("🔧 [F]iltros", style="bold magenta")
        actions_text.append(" • ")
        actions_text.append("💾 [S]eguir", style="bold blue")

        return Panel(
            Align.center(actions_text),
            border_style="dim"
        )

    def _load_latest_detection_data(self):
        """📂 Cargar datos más recientes de detección"""
        try:
            # Buscar archivo más reciente en diagnosticos
            if DIAGNOSTICS_DIR.exists():
                detection_files = list(DIAGNOSTICS_DIR.glob("deteccion_errores_*.json"))
                if detection_files:
                    latest_file = max(detection_files, key=lambda f: f.stat().st_mtime)

                    with open(latest_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    self.current_problems = data.get('problems', [])
                    self.current_stats = data.get('statistics', {})
                    return

            # Si no hay datos, establecer vacío (no ejecutar detección automática)
            self.current_problems = []
            self.current_stats = {'no_data': True}

        except Exception as e:
            self.current_problems = []
            self.current_stats = {'error': str(e)}

    def _run_quick_detection(self):
        """⚡ Ejecutar detección rápida"""
        try:
            if not ERROR_DETECTOR_SCRIPT.exists():
                return

            # Ejecutar detector en modo rápido
            result = subprocess.run([
                sys.executable,
                str(ERROR_DETECTOR_SCRIPT),
                "--workspace", str(WORKSPACE_ROOT),
                "--quick"
            ], capture_output=True, text=True, timeout=30)

            if result.returncode in [0, 1]:  # 0 = ok, 1 = problemas encontrados
                # Buscar el archivo más reciente después de la ejecución
                time.sleep(1)  # Dar tiempo para que se escriba el archivo
                if DIAGNOSTICS_DIR.exists():
                    detection_files = list(DIAGNOSTICS_DIR.glob("deteccion_errores_*.json"))
                    if detection_files:
                        latest_file = max(detection_files, key=lambda f: f.stat().st_mtime)

                        with open(latest_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)

                        self.current_problems = data.get('problems', [])
                        self.current_stats = data.get('statistics', {})

        except Exception:
            pass  # Silenciar errores de detección automática

    def _apply_filters(self) -> List[Dict]:
        """🔍 Aplicar filtros a la lista de problemas"""
        filtered = self.current_problems

        # Filtro por severidad
        if self.filters['severity']:
            filtered = [p for p in filtered if self.filters['severity'] in p.get('severity', '')]

        # Filtro por categoría
        if self.filters['category']:
            filtered = [p for p in filtered if self.filters['category'] in p.get('category', '')]

        return filtered

    def _get_severity_emoji(self, severity: str) -> str:
        """🎨 Obtener emoji para severidad"""
        emoji_map = {
            'CRITICAL': '🚨',
            'HIGH': '⚠️',
            'MEDIUM': '⚡',
            'LOW': '📝',
            'INFO': 'ℹ️'
        }
        return emoji_map.get(severity, '❓')

    def _format_severity(self, severity: str) -> str:
        """🎨 Formatear severidad con colores"""
        if 'CRITICAL' in severity:
            return f"[bold red]{severity}[/bold red]"
        elif 'HIGH' in severity:
            return f"[bold yellow]{severity}[/bold yellow]"
        elif 'MEDIUM' in severity:
            return f"[cyan]{severity}[/cyan]"
        elif 'LOW' in severity:
            return f"[dim]{severity}[/dim]"
        else:
            return severity

    def _render_error_panel(self, error_msg: str) -> str:
        """❌ Renderizar panel de error"""
        if RICH_AVAILABLE:
            error_panel = Panel(
                f"❌ {error_msg}",
                title="Error",
                border_style="red"
            )
            return str(error_panel)
        else:
            return f"❌ ERROR: {error_msg}"

    def handle_user_action(self, action: str) -> Dict[str, Any]:
        """🎮 Manejar acciones del usuario"""
        actions = {
            'r': self._action_refresh,
            'd': self._action_detect,
            'e': self._action_statistics,
            'f': self._action_filters,
            's': self._action_export
        }

        action_func = actions.get(action.lower())
        if action_func:
            return action_func()

        return {'status': 'unknown_action', 'message': f'Acción desconocida: {action}'}

    def _action_refresh(self) -> Dict[str, Any]:
        """🔄 Acción refrescar datos"""
        self._load_latest_detection_data()
        return {'status': 'success', 'message': 'Datos actualizados'}

    def _action_detect(self) -> Dict[str, Any]:
        """🔍 Acción ejecutar detección"""
        try:
            self._run_quick_detection()
            return {'status': 'success', 'message': 'Detección ejecutada'}
        except Exception as e:
            return {'status': 'error', 'message': f'Error en detección: {str(e)}'}

    def _action_statistics(self) -> Dict[str, Any]:
        """📊 Acción mostrar estadísticas detalladas"""
        return {
            'status': 'info',
            'message': 'Estadísticas detalladas',
            'data': self.current_stats
        }

    def _action_filters(self) -> Dict[str, Any]:
        """🔧 Acción configurar filtros"""
        # Aquí se podría implementar una UI para configurar filtros
        return {'status': 'info', 'message': 'Configuración de filtros disponible'}

    def _action_export(self) -> Dict[str, Any]:
        """💾 Acción exportar problemas"""
        try:
            export_file = WORKSPACE_ROOT / "data" / "exports" / f"problemas_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            export_file.parent.mkdir(parents=True, exist_ok=True)

            export_data = {
                'timestamp': datetime.now().isoformat(),
                'problems': self.current_problems,
                'statistics': self.current_stats
            }

            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            return {'status': 'success', 'message': f'Exportado a: {export_file}'}

        except Exception as e:
            return {'status': 'error', 'message': f'Error exportando: {str(e)}'}


# ===================================================================
# 🚀 FUNCIONES PRINCIPALES PARA INTEGRACIÓN
# ===================================================================

def render_problems_tab() -> str:
    """🎨 Función principal para renderizar pestaña de problemas"""
    renderer = ProblemsTabRenderer()
    return renderer.render_tab()


def render_problems_tab_simple() -> str:
    """📝 Función simple para integración básica"""
    renderer = ProblemsTabRenderer()
    return renderer._render_simple_tab()


def get_problems_summary() -> Dict[str, Any]:
    """📊 Obtener resumen de problemas para dashboard"""
    renderer = ProblemsTabRenderer()
    renderer._load_latest_detection_data()

    return {
        'total_problems': len(renderer.current_problems),
        'critical_count': len([p for p in renderer.current_problems if 'CRITICAL' in p.get('severity', '')]),
        'high_count': len([p for p in renderer.current_problems if 'HIGH' in p.get('severity', '')]),
        'stats': renderer.current_stats,
        'last_analysis': datetime.now().isoformat()
    }


def execute_detection(quick_mode: bool = True) -> Dict[str, Any]:
    """🔍 Ejecutar detección de errores"""
    try:
        args = [
            sys.executable,
            str(ERROR_DETECTOR_SCRIPT),
            "--workspace", str(WORKSPACE_ROOT)
        ]

        if quick_mode:
            args.append("--quick")

        result = subprocess.run(args, capture_output=True, text=True, timeout=60)

        return {
            'status': 'success' if result.returncode in [0, 1] else 'error',
            'return_code': result.returncode,
            'output': result.stdout,
            'error': result.stderr if result.stderr else None
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }


# ===================================================================
# 🧪 TESTING Y DEMO
# ===================================================================

def demo_problems_tab():
    """🎬 Demo de la pestaña de problemas"""
    print("🎬 DEMO - Pestaña Problemas Dashboard")
    print("=" * 40)

    renderer = ProblemsTabRenderer()

    # Mostrar renderizado
    tab_content = renderer.render_tab()
    print(tab_content)

    print("\n" + "=" * 40)
    print("📊 Resumen:")
    summary = get_problems_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")


if __name__ == "__main__":
    demo_problems_tab()
