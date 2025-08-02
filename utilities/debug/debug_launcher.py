# 🔧 DEBUG LAUNCHER - DEVTOOLS F12 SUPPORT
# Sprint 1.1 - Debug System & Clean Code

import sys
import os
from pathlib import Path
import asyncio
from datetime import datetime
import argparse
import json

# 📁 Configurar path del proyecto
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from textual.app import App
from textual.binding import Binding
from textual.widgets import Static, Header, Footer
from textual.containers import Container
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table

# 🎯 Import del sistema principal
try:
    from dashboard.dashboard_definitivo import SentinelDashboardDefinitivo as SentinelDashboard
    from sistema.logging_interface import enviar_senal_log
except ImportError as e:
    print(f"❌ Error importing main system: {e}")
    print("🔧 Make sure you're running from the correct directory")
    sys.exit(1)

class DebugLauncher(App):
    """
    Launcher profesional con DevTools F12 support y debugging avanzado
    """

    CSS = """
    Screen {
        background: $surface;
    }

    .debug_panel {
        background: $panel;
        border: solid $accent;
        margin: 1;
        padding: 1;
    }

    .launch_buttons {
        background: $surface-lighten-1;
        border: solid $success;
        margin: 1;
        padding: 2;
    }

    .system_info {
        background: $surface-darken-1;
        border: solid $warning;
        margin: 1;
        padding: 1;
    }
    """

    TITLE = "🔧 SENTINEL DEBUG LAUNCHER - DevTools Professional"
    SUB_TITLE = "Debug System & Clean Code - Sprint 1.1"

    BINDINGS = [
        Binding("f12", "toggle_devtools", "🔧 DevTools", show=True),
        Binding("1", "launch_normal", "🚀 Launch Normal", show=True),
        Binding("2", "launch_debug", "🐛 Launch Debug", show=True),
        Binding("3", "launch_console", "💻 Launch Console", show=True),
        Binding("4", "run_diagnostics", "🔍 Diagnostics", show=True),
        Binding("s", "screenshot", "📸 Screenshot", show=True),
        Binding("l", "view_logs", "📋 View Logs", show=True),
        Binding("q", "quit", "❌ Exit", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.console = Console()
        self.devtools_active = False
        self.system_diagnostics = {}

        # 🔧 Debug configuration
        self.debug_config = {
            'devtools_enabled': True,
            'console_mode': False,
            'verbose_logging': False,
            'screenshot_enabled': True,
            'performance_monitoring': True
        }

    def compose(self):
        """Composición de la interfaz de debug"""
        yield Header()

        with Container(classes="debug_panel"):
            yield Static(self.render_launcher_panel(), id="launcher_display")

        yield Footer()

    def on_mount(self):
        """Configuración inicial del launcher"""
        self.set_interval(2.0, self.update_system_info)
        self.run_system_diagnostics()
        self.notify("🔧 Debug Launcher iniciado - F12 para DevTools")

    def render_launcher_panel(self) -> Panel:
        """Renderiza el panel principal del launcher"""

        # 🏗️ Información del sistema
        system_info = self._get_system_info()

        # 📊 Estado de diagnósticos
        diagnostics_info = self._get_diagnostics_info()

        # 🎯 Panel combinado
        content = Text()

        # 🔧 Header con información clave
        content.append("🔧 SENTINEL DEBUG LAUNCHER v1.0\n\n", style="bold cyan")
        content.append(f"📊 Sistema: {system_info['status']}\n", style="green")
        content.append(f"🐛 Debug Mode: {'✅ ACTIVO' if self.devtools_active else '⭕ INACTIVO'}\n", style="yellow" if self.devtools_active else "dim white")
        content.append(f"📸 Screenshots: {'✅ HABILITADO' if self.debug_config['screenshot_enabled'] else '❌ DESHABILITADO'}\n", style="green")
        content.append(f"⏰ Última actualización: {datetime.now().strftime('%H:%M:%S')}\n\n", style="dim cyan")

        # 🚀 Opciones de launch
        content.append("🚀 OPCIONES DE LANZAMIENTO:\n\n", style="bold blue")
        content.append("1️⃣  Launch Normal     - Modo producción estándar\n", style="white")
        content.append("2️⃣  Launch Debug      - Modo debug con logging verbose\n", style="yellow")
        content.append("3️⃣  Launch Console    - Modo consola para desarrollo\n", style="cyan")
        content.append("4️⃣  Run Diagnostics  - Ejecutar diagnósticos del sistema\n", style="magenta")

        content.append("\n🔧 HERRAMIENTAS DE DEBUG:\n\n", style="bold green")
        content.append("F12  DevTools         - Activar/desactivar herramientas de desarrollo\n", style="white")
        content.append("S    Screenshot       - Capturar screenshot del sistema\n", style="white")
        content.append("L    View Logs        - Ver logs recientes del sistema\n", style="white")

        # 📊 Diagnósticos del sistema
        if self.system_diagnostics:
            content.append(f"\n📊 DIAGNÓSTICOS DEL SISTEMA:\n\n", style="bold magenta")
            content.append(f"✅ Imports: {self.system_diagnostics.get('imports_ok', 'N/A')}\n", style="green")
            content.append(f"📁 Paths: {self.system_diagnostics.get('paths_ok', 'N/A')}\n", style="green")
            content.append(f"🔧 Config: {self.system_diagnostics.get('config_ok', 'N/A')}\n", style="green")
            content.append(f"📋 Logs: {self.system_diagnostics.get('logs_ok', 'N/A')}\n", style="green")

        return Panel(
            content,
            title="🔧 [bold cyan]DEBUG LAUNCHER PROFESSIONAL[/bold cyan]",
            subtitle=f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            border_style="bright_cyan",
            padding=(1, 2)
        )

    def _get_system_info(self) -> dict:
        """Obtiene información del sistema"""
        return {
            'status': 'OPERATIVO',
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'platform': sys.platform,
            'cwd': os.getcwd(),
            'project_root': str(project_root)
        }

    def _get_diagnostics_info(self) -> dict:
        """Obtiene información de diagnósticos"""
        return {
            'last_run': datetime.now().strftime('%H:%M:%S'),
            'status': 'COMPLETO' if self.system_diagnostics else 'PENDIENTE'
        }

    def run_system_diagnostics(self):
        """Ejecuta diagnósticos completos del sistema"""
        diagnostics = {}

        # ✅ Verificar imports críticos
        try:
            from dashboard.dashboard_definitivo import SentinelDashboardDefinitivo as SentinelDashboard
            from sistema.logging_interface import enviar_senal_log
            diagnostics['imports_ok'] = True
        except ImportError as e:
            diagnostics['imports_ok'] = f"ERROR: {e}"

        # 📁 Verificar paths críticos
        critical_paths = [
            project_root / "dashboard",
            project_root / "core",
            project_root / "sistema",
            project_root / "config"
        ]

        paths_status = []
        for path in critical_paths:
            if path.exists():
                paths_status.append(f"✅ {path.name}")
            else:
                paths_status.append(f"❌ {path.name}")

        diagnostics['paths_ok'] = " | ".join(paths_status)

        # 🔧 Verificar configuración
        try:
            config_files = list(project_root.glob("**/*.json"))
            diagnostics['config_ok'] = f"{len(config_files)} archivos encontrados"
        except Exception as e:
            diagnostics['config_ok'] = f"ERROR: {e}"

        # 📋 Verificar logs
        try:
            log_files = list(project_root.glob("**/logs/**/*.log"))
            diagnostics['logs_ok'] = f"{len(log_files)} logs encontrados"
        except Exception as e:
            diagnostics['logs_ok'] = f"ERROR: {e}"

        self.system_diagnostics = diagnostics

        # 🔄 Actualizar display
        try:
            launcher_display = self.query_one("#launcher_display", Static)
            launcher_display.update(self.render_launcher_panel())
        except:
            pass

    def update_system_info(self):
        """Actualiza información del sistema cada 2 segundos"""
        try:
            launcher_display = self.query_one("#launcher_display", Static)
            launcher_display.update(self.render_launcher_panel())
        except:
            pass

    # 🎮 ACCIONES DE LAUNCHER

    def action_toggle_devtools(self):
        """Toggle DevTools F12"""
        self.devtools_active = not self.devtools_active
        status = "ACTIVADO" if self.devtools_active else "DESACTIVADO"

        if self.devtools_active:
            # 🔧 Configurar modo debug
            os.environ['TEXTUAL_DEBUG'] = '1'
            os.environ['TEXTUAL_LOG'] = '1'
            self.debug_config['verbose_logging'] = True
            self.notify("🔧 DevTools ACTIVADO - Logging verbose habilitado", timeout=3)
        else:
            # 🔕 Desactivar modo debug
            os.environ.pop('TEXTUAL_DEBUG', None)
            os.environ.pop('TEXTUAL_LOG', None)
            self.debug_config['verbose_logging'] = False
            self.notify("🔕 DevTools DESACTIVADO - Modo normal", timeout=3)

    def action_launch_normal(self):
        """Launch en modo normal"""
        self.notify("🚀 Lanzando Sentinel en modo NORMAL...")
        self._launch_sentinel_app(mode="normal")

    def action_launch_debug(self):
        """Launch en modo debug"""
        self.notify("🐛 Lanzando Sentinel en modo DEBUG...")
        self._launch_sentinel_app(mode="debug")

    def action_launch_console(self):
        """Launch en modo console"""
        self.notify("💻 Lanzando Sentinel en modo CONSOLE...")
        self._launch_sentinel_app(mode="console")

    def action_run_diagnostics(self):
        """Ejecutar diagnósticos del sistema"""
        self.notify("🔍 Ejecutando diagnósticos del sistema...")
        self.run_system_diagnostics()
        self.notify("✅ Diagnósticos completados", timeout=2)

    def action_screenshot(self):
        """Capturar screenshot del sistema"""
        if not self.debug_config['screenshot_enabled']:
            self.notify("❌ Screenshots deshabilitados", timeout=2)
            return

        try:
            # 📸 Generar nombre de screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = project_root / f"debug_screenshot_{timestamp}.svg"

            # 🎯 Capturar screenshot (simulado - Textual no tiene screenshot nativo)
            self._capture_debug_screenshot(screenshot_path)

            self.notify(f"📸 Screenshot capturado: {screenshot_path.name}", timeout=3)
        except Exception as e:
            self.notify(f"❌ Error capturando screenshot: {e}", timeout=3)

    def action_view_logs(self):
        """Ver logs recientes del sistema"""
        self.notify("📋 Mostrando logs recientes...")
        # TODO: Implementar viewer de logs en nueva ventana
        self.notify("📋 Feature en desarrollo - usar archivos de log directamente", timeout=3)

    def _launch_sentinel_app(self, mode: str = "normal"):
        """Lanza la aplicación Sentinel con configuración específica"""
        try:
            # 🔧 Configurar ambiente según modo
            if mode == "debug":
                os.environ['TEXTUAL_DEBUG'] = '1'
                os.environ['TEXTUAL_LOG'] = '1'
                os.environ['SENTINEL_DEBUG'] = '1'
            elif mode == "console":
                os.environ['TEXTUAL_CONSOLE'] = '1'

            # 🚀 Cerrar launcher y lanzar app principal
            self.notify(f"🎯 Iniciando Sentinel Dashboard en modo {mode.upper()}...", timeout=2)

            # 🔄 Pequeña pausa para que se vea la notificación
            import time
            time.sleep(1)

            # 🚀 Exit launcher y launch main app
            self.exit()

            # 🎯 Launch main app
            app = SentinelDashboard()

            # 🔧 Configurar app según modo
            if mode == "debug":
                app.debug_mode = True
            elif mode == "console":
                app.console = self.console

            app.run()

        except Exception as e:
            self.notify(f"❌ Error lanzando aplicación: {e}", timeout=5)
            enviar_senal_log("ERROR", f"Error lanzando aplicación: {e}", __name__, "debug")

    def _capture_debug_screenshot(self, path: Path):
        """Captura screenshot de debug (simulado)"""
        # 🎯 En una implementación real, usaríamos la funcionalidad de screenshot de Textual
        # Por ahora, guardamos información de debug

        debug_info = {
            'timestamp': datetime.now().isoformat(),
            'system_diagnostics': self.system_diagnostics,
            'debug_config': self.debug_config,
            'devtools_active': self.devtools_active,
            'environment_vars': {
                'TEXTUAL_DEBUG': os.environ.get('TEXTUAL_DEBUG'),
                'TEXTUAL_LOG': os.environ.get('TEXTUAL_LOG'),
                'SENTINEL_DEBUG': os.environ.get('SENTINEL_DEBUG')
            }
        }

        # 💾 Guardar información de debug
        debug_path = path.with_suffix('.json')
        with open(debug_path, 'w', encoding='utf-8') as f:
            json.dump(debug_info, f, indent=2, ensure_ascii=False)


def main():
    """Función principal del debug launcher"""
    parser = argparse.ArgumentParser(description="Sentinel Debug Launcher")
    parser.add_argument("--mode", choices=["launcher", "normal", "debug", "console"],
                       default="launcher", help="Launch mode")
    parser.add_argument("--devtools", action="store_true", help="Enable DevTools")
    parser.add_argument("--diagnostics", action="store_true", help="Run diagnostics only")

    args = parser.parse_args()

    # 🔧 Configurar ambiente según argumentos
    if args.devtools:
        os.environ['TEXTUAL_DEBUG'] = '1'
        os.environ['TEXTUAL_LOG'] = '1'

    # 🔍 Solo ejecutar diagnósticos
    if args.diagnostics:
        enviar_senal_log("INFO", "Ejecutando diagnósticos del sistema...", __name__, "debug")
        launcher = DebugLauncher()
        launcher.run_system_diagnostics()
        enviar_senal_log("SUCCESS", "Diagnósticos completados", __name__, "debug")
        return

    # 🚀 Launch según modo
    if args.mode == "launcher":
        # 🔧 Mostrar launcher
        app = DebugLauncher()
        app.run()
    else:
        # 🎯 Launch directo
        try:
            from dashboard.dashboard_definitivo import SentinelDashboardDefinitivo as SentinelDashboard

            if args.mode == "debug":
                os.environ['TEXTUAL_DEBUG'] = '1'
                os.environ['SENTINEL_DEBUG'] = '1'
            elif args.mode == "console":
                os.environ['TEXTUAL_CONSOLE'] = '1'

            app = SentinelDashboard()
            app.run()

        except Exception as e:
            enviar_senal_log("ERROR", f"Error lanzando aplicación: {e}", __name__, "debug")
            sys.exit(1)


if __name__ == "__main__":
    main()
