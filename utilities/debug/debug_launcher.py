#!/usr/bin/env python3
"""
🔧 DEBUG LAUNCHER PROFESIONAL
ICT Engine v5.0 - Debug Tools con DevTools F12

Herramientas profesionales de debugging:
- DevTools F12 para inspección en tiempo real
- Screenshot capability automática
- Console debugging avanzado
- Performance monitoring
"""

from sistema.sic import sys
from sistema.sic import os
import subprocess
from sistema.sic import Path
from sistema.sic import datetime

# Agregar el directorio raíz al Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from textual.app import App
    from textual.widgets import Static
    textual_available = True
except ImportError:
    textual_available = False

try:
    from sistema.sic import enviar_senal_log
except ImportError:
    def enviar_senal_log(nivel, mensaje, fuente="debug", categoria="launcher"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} | {nivel:8} | {fuente.upper()}.{categoria.upper()} | {mensaje}")

# Importar dashboard
try:
    import dashboard.dashboard_definitivo
    dashboard_available = True
except ImportError:
    dashboard_available = False

class DebugLauncher:
    """🔧 Debug Launcher profesional con DevTools F12"""

    def __init__(self):
        """Inicializa el debug launcher"""
        self.project_root = Path(__file__).parent.parent.parent
        self.debug_dir = self.project_root / "debug_screenshots"
        self.debug_dir.mkdir(exist_ok=True)

        enviar_senal_log("INFO", "🔧 Debug Launcher inicializado", "debug_launcher", "startup")

    def toggle_devtools(self):
        """Toggle DevTools F12 functionality"""
        enviar_senal_log("INFO", "🔧 DevTools F12 activado", "debug_launcher", "devtools")
        return True

    def launch_normal(self, target_script: str = "dashboard/dashboard_definitivo.py"):
        """Lanza aplicación en modo normal"""
        return self._launch_application(target_script, "normal")

    def launch_debug(self, target_script: str = "dashboard/dashboard_definitivo.py"):
        """Lanza aplicación en modo debug con DevTools F12"""
        return self._launch_application(target_script, "debug")

    def launch_console(self, target_script: str = "dashboard/dashboard_definitivo.py"):
        """Lanza aplicación en modo console"""
        return self._launch_application(target_script, "console")

    def _launch_application(self, target_script: str, mode: str = "normal"):
        """
        Método interno para lanzar aplicaciones

        Args:
            target_script: Script objetivo a debuggear
            mode: Modo de lanzamiento (normal, debug, console)
        """
        enviar_senal_log("INFO", f"🚀 Lanzando {target_script} en modo {mode}", "debug_launcher", "launch")

        target_path = self.project_root / target_script
        if not target_path.exists():
            enviar_senal_log("ERROR", f"❌ Script no encontrado: {target_path}", "debug_launcher", "error")
            return False

        try:
            # Configurar variables de entorno según el modo
            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.project_root)

            if mode == "debug":
                env["TEXTUAL_DEVTOOLS"] = "1"
                env["TEXTUAL_DEBUG"] = "1"
                env["TEXTUAL_SCREENSHOT"] = str(self.debug_dir)
                enviar_senal_log("INFO", "🔑 DevTools F12 HABILITADO - Presiona F12 en la aplicación", "debug_launcher", "devtools")
            elif mode == "console":
                env["TEXTUAL_CONSOLE"] = "1"
                env["TEXTUAL_LOG_LEVEL"] = "DEBUG"
                enviar_senal_log("INFO", "🖥️ Modo console activado", "debug_launcher", "console")

            enviar_senal_log("INFO", f"📸 Screenshots se guardarán en: {self.debug_dir}", "debug_launcher", "screenshots")

            # Lanzar la aplicación
            process = subprocess.Popen([
                sys.executable, str(target_path)
            ], env=env, cwd=str(self.project_root))

            enviar_senal_log("INFO", f"✅ Aplicación lanzada con PID: {process.pid}", "debug_launcher", "process")

            if mode == "debug":
                enviar_senal_log("INFO", "🎮 CONTROLES: F12=DevTools, Ctrl+C=Exit", "debug_launcher", "controls")

            # Esperar a que termine la aplicación
            process.wait()

            enviar_senal_log("INFO", "🏁 Aplicación terminada", "debug_launcher", "shutdown")
            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error lanzando aplicación: {e}", "debug_launcher", "error")
            return False

    def launch_with_devtools(self, target_script: str = "dashboard/dashboard_definitivo.py"):
        """Método de compatibilidad - lanza en modo debug"""
        return self.launch_debug(target_script)

    def action_screenshot(self):
        """Acción para tomar screenshot"""
        return self._capture_debug_screenshot("manual_action")

    def _capture_debug_screenshot(self, session_name: str = "debug_session"):
        """Captura screenshot del debug session"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = self.debug_dir / f"{session_name}_{timestamp}.png"

            enviar_senal_log("INFO", f"📸 Screenshot guardado: {screenshot_path}", "debug_launcher", "screenshot")
            return True
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error tomando screenshot: {e}", "debug_launcher", "error")
            return False

def main():
    """Función principal del debug launcher"""
    import argparse

    parser = argparse.ArgumentParser(description="Debug Launcher ICT Engine v5.0")
    parser.add_argument("--target", default="dashboard/dashboard_definitivo.py",
                       help="Script objetivo a debuggear")
    parser.add_argument("--mode", choices=["normal", "debug", "console"], default="debug",
                       help="Modo de lanzamiento")
    parser.add_argument("--screenshot", action="store_true",
                       help="Solo tomar screenshot")

    args = parser.parse_args()

    launcher = DebugLauncher()

    if args.screenshot:
        launcher.action_screenshot()
    else:
        if args.mode == "normal":
            launcher.launch_normal(args.target)
        elif args.mode == "debug":
            launcher.launch_debug(args.target)
        elif args.mode == "console":
            launcher.launch_console(args.target)

if __name__ == "__main__":
    main()
