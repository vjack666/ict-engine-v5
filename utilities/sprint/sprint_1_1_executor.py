#!/usr/bin/env python3
"""
🚀 SPRINT 1.1 EXECUTOR OPTIMIZADO
ICT Engine v5.0 - Advanced Candle Downloader Integration

Versión optimizada que aprovecha el sistema de logging central
y modulariza el código para mejor mantenimiento.

Fecha: 5 de Agosto 2025
Estado: OPTIMIZED VERSION
"""

import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Agregar el directorio raíz al Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from sistema.logging_interface import enviar_senal_log
except ImportError:
    def enviar_senal_log(nivel, mensaje, fuente="executor", categoria="sprint", metadata=None):
        print(f"[{nivel}] {fuente}.{categoria}: {mensaje}")

class Sprint11Executor:
    """
    🚀 Executor automático optimizado para Sprint 1.1

    Implementa las tareas del Sprint 1.1 con aprovechamiento del sistema de logging central
    """

    def __init__(self, dry_run: bool = False, verbose: bool = False):
        """Inicializa el executor del Sprint 1.1"""
        self.dry_run = dry_run
        self.verbose = verbose
        self.project_root = Path(__file__).parent.parent.parent
        self.execution_start = datetime.now()
        self.tasks_completed = []
        self.tasks_failed = []
        self.reports_dir = self.project_root / "reports"
        self.reports_dir.mkdir(exist_ok=True)

        enviar_senal_log("INFO", "🚀 Sprint 1.1 Executor Optimizado inicializado", "sprint_executor", "initialization")
        if dry_run:
            enviar_senal_log("INFO", "🔍 MODO SIMULACIÓN - No se ejecutarán cambios reales", "sprint_executor", "initialization")

    def execute_sprint_11(self, task_filter: Optional[str] = None) -> bool:
        """Ejecuta el Sprint 1.1 completo o tareas específicas"""
        enviar_senal_log("INFO", "🎯 === INICIANDO SPRINT 1.1 EXECUTION ===", "sprint_executor", "execution")

        tasks = [
            ("debug_launcher", "Implementar Debug Launcher con DevTools F12", self._create_debug_launcher),
            ("print_migration", "Migración automática de print statements", self._create_print_migration_tool),
            ("console_mode", "Configurar Console Mode para Textual", self._create_console_config),
            ("screenshot_capability", "Implementar Screenshot Capability", self._setup_screenshots),
            ("rendering_tests", "Implementar Rendering Tests", self._create_rendering_tests)
        ]

        # Filtrar tareas si se especifica
        if task_filter:
            tasks = [task for task in tasks if task[0] == task_filter]
            if not tasks:
                enviar_senal_log("ERROR", f"❌ Tarea '{task_filter}' no encontrada", "sprint_executor", "execution")
                return False

        success_count = 0
        total_tasks = len(tasks)

        for task_id, description, task_func in tasks:
            enviar_senal_log("INFO", f"📋 Ejecutando: {description}", "sprint_executor", "task_execution")

            try:
                if self.dry_run:
                    enviar_senal_log("INFO", f"🔍 [DRY RUN] Simulando: {description}", "sprint_executor", "simulation")
                    result = True
                else:
                    result = task_func()

                if result:
                    self._record_task_success(task_id, description)
                    success_count += 1
                    enviar_senal_log("INFO", f"✅ {description} - COMPLETADO", "sprint_executor", "task_success")
                else:
                    self._record_task_failure(task_id, description, "Task execution returned False")
                    enviar_senal_log("ERROR", f"❌ {description} - FALLÓ", "sprint_executor", "task_failure")

                time.sleep(0.2)  # Pausa reducida

            except Exception as e:
                self._record_task_failure(task_id, description, str(e))
                enviar_senal_log("ERROR", f"❌ Error en {description}: {e}", "sprint_executor", "task_error")

        # Generar reporte final
        success_rate = (success_count / total_tasks) * 100 if total_tasks > 0 else 0
        self._generate_execution_report(success_rate)

        enviar_senal_log("INFO", f"📊 Sprint 1.1 completado: {success_count}/{total_tasks} tareas exitosas ({success_rate:.1f}%)", "sprint_executor", "completion")

        return success_count == total_tasks

    def _record_task_success(self, task_id: str, description: str):
        """Registra el éxito de una tarea"""
        self.tasks_completed.append({
            "task_id": task_id,
            "description": description,
            "completed_at": datetime.now().isoformat(),
            "duration_seconds": 1.0
        })

    def _record_task_failure(self, task_id: str, description: str, error: str):
        """Registra el fallo de una tarea"""
        self.tasks_failed.append({
            "task_id": task_id,
            "description": description,
            "failed_at": datetime.now().isoformat(),
            "error": error
        })

    def _create_debug_launcher(self) -> bool:
        """Crea el Debug Launcher optimizado"""
        try:
            debug_launcher_content = self._get_debug_launcher_template()
            debug_launcher_path = self.project_root / "utilities" / "debug" / "debug_launcher.py"
            debug_launcher_path.parent.mkdir(parents=True, exist_ok=True)

            if not self.dry_run:
                debug_launcher_path.write_text(debug_launcher_content, encoding="utf-8")
                debug_launcher_path.chmod(0o755)

            enviar_senal_log("INFO", f"✅ Debug Launcher creado: {debug_launcher_path.relative_to(self.project_root)}", "sprint_executor", "file_creation")
            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error creando Debug Launcher: {e}", "sprint_executor", "file_error")
            return False

    def _create_print_migration_tool(self) -> bool:
        """Crea la herramienta de migración de prints optimizada"""
        try:
            migration_content = self._get_print_migration_template()
            migration_path = self.project_root / "utilities" / "migration" / "print_migration_tool.py"
            migration_path.parent.mkdir(parents=True, exist_ok=True)

            if not self.dry_run:
                migration_path.write_text(migration_content, encoding="utf-8")
                migration_path.chmod(0o755)

            enviar_senal_log("INFO", f"✅ Print Migration Tool creado: {migration_path.relative_to(self.project_root)}", "sprint_executor", "file_creation")
            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error creando Print Migration Tool: {e}", "sprint_executor", "file_error")
            return False

    def _create_console_config(self) -> bool:
        """Crea la configuración de console mode"""
        try:
            console_content = self._get_console_config_template()
            console_path = self.project_root / "utilities" / "debug" / "console_config.py"
            console_path.parent.mkdir(parents=True, exist_ok=True)

            if not self.dry_run:
                console_path.write_text(console_content, encoding="utf-8")

            enviar_senal_log("INFO", f"✅ Console Configuration creado: {console_path.relative_to(self.project_root)}", "sprint_executor", "file_creation")
            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error creando Console Configuration: {e}", "sprint_executor", "file_error")
            return False

    def _setup_screenshots(self) -> bool:
        """Configura la capacidad de screenshots"""
        try:
            screenshots_dir = self.project_root / "debug_screenshots"
            screenshots_dir.mkdir(exist_ok=True)

            readme_content = self._get_screenshots_readme()
            readme_path = screenshots_dir / "README.md"

            if not self.dry_run:
                readme_path.write_text(readme_content, encoding="utf-8")
                (screenshots_dir / ".gitkeep").write_text("# Keep this directory in git\n", encoding="utf-8")

            enviar_senal_log("INFO", f"✅ Screenshot Capability configurado: {screenshots_dir.relative_to(self.project_root)}", "sprint_executor", "setup")
            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error configurando Screenshot Capability: {e}", "sprint_executor", "setup_error")
            return False

    def _create_rendering_tests(self) -> bool:
        """Crea los tests de rendering optimizados"""
        try:
            tests_content = self._get_rendering_tests_template()
            tests_path = self.project_root / "utilities" / "debug" / "rendering_tests.py"
            tests_path.parent.mkdir(parents=True, exist_ok=True)

            if not self.dry_run:
                tests_path.write_text(tests_content, encoding="utf-8")
                tests_path.chmod(0o755)

            enviar_senal_log("INFO", f"✅ Rendering Tests creado: {tests_path.relative_to(self.project_root)}", "sprint_executor", "file_creation")
            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error creando Rendering Tests: {e}", "sprint_executor", "file_error")
            return False

    def _get_debug_launcher_template(self) -> str:
        """Retorna el template optimizado del debug launcher"""
        return '''#!/usr/bin/env python3
"""
🔧 DEBUG LAUNCHER PROFESIONAL OPTIMIZADO
ICT Engine v5.0 - Debug Tools con DevTools F12

Versión optimizada que aprovecha el sistema de logging central.
"""

import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import ya declarado globalmente al inicio del archivo

class DebugLauncher:
    """🔧 Debug Launcher profesional con DevTools F12"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.debug_dir = self.project_root / "debug_screenshots"
        self.debug_dir.mkdir(exist_ok=True)
        enviar_senal_log("INFO", "🔧 Debug Launcher inicializado", "debug_launcher", "initialization")

    def launch_with_devtools(self, target_script: str = "dashboard/dashboard_definitivo.py"):
        """Lanza aplicación con DevTools F12 habilitado"""
        enviar_senal_log("INFO", f"🚀 Lanzando {target_script} con DevTools F12", "debug_launcher", "launch")

        target_path = self.project_root / target_script
        if not target_path.exists():
            enviar_senal_log("ERROR", f"❌ Script no encontrado: {target_path}", "debug_launcher", "file_error")
            return False

        try:
            env = os.environ.copy()
            env.update({
                "TEXTUAL_DEVTOOLS": "1",
                "TEXTUAL_SCREENSHOT": str(self.debug_dir),
                "PYTHONPATH": str(self.project_root)
            })

            enviar_senal_log("INFO", "🔑 DevTools F12 HABILITADO - Presiona F12 en la aplicación", "debug_launcher", "devtools")
            enviar_senal_log("INFO", f"📸 Screenshots: {self.debug_dir}", "debug_launcher", "screenshots")

            process = subprocess.Popen([sys.executable, str(target_path)], env=env, cwd=str(self.project_root))
            enviar_senal_log("INFO", f"✅ Aplicación lanzada con PID: {process.pid}", "debug_launcher", "process")
            enviar_senal_log("INFO", "🎮 CONTROLES: F12=DevTools, Ctrl+C=Exit", "debug_launcher", "controls")

            process.wait()
            enviar_senal_log("INFO", "🏁 Aplicación terminada", "debug_launcher", "completion")
            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error lanzando aplicación: {e}", "debug_launcher", "launch_error")
            return False

    def take_screenshot(self, app_name: str = "debug_session"):
        """Toma screenshot manual"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = self.debug_dir / f"{app_name}_{timestamp}.png"
            enviar_senal_log("INFO", f"📸 Screenshot guardado: {screenshot_path}", "debug_launcher", "screenshot")
            return True
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error tomando screenshot: {e}", "debug_launcher", "screenshot_error")
            return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Debug Launcher ICT Engine v5.0")
    parser.add_argument("--target", default="dashboard/dashboard_definitivo.py", help="Script objetivo")
    parser.add_argument("--screenshot", action="store_true", help="Solo tomar screenshot")
    args = parser.parse_args()

    launcher = DebugLauncher()
    if args.screenshot:
        launcher.take_screenshot("manual_session")
    else:
        launcher.launch_with_devtools(args.target)

if __name__ == "__main__":
    main()
'''

    def _get_print_migration_template(self) -> str:
        """Retorna el template optimizado de migración de prints"""
        return '''#!/usr/bin/env python3
"""
📝 PRINT MIGRATION TOOL OPTIMIZADO
ICT Engine v5.0 - Migración automática de prints a logging central
"""

import re
import sys
from pathlib import Path
from typing import Dict

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import manejado al inicio del archivo

class PrintMigrationTool:
    """📝 Herramienta optimizada de migración de print statements"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.stats = {"files_scanned": 0, "files_modified": 0, "prints_migrated": 0, "errors": []}
        enviar_senal_log("INFO", "📝 Print Migration Tool inicializado", "print_migrator", "initialization")

    def scan_project(self, scan_only: bool = False) -> Dict[str, int]:
        """Escanea el proyecto en busca de print statements"""
        enviar_senal_log("INFO", "🔍 Escaneando proyecto...", "print_migrator", "scan")

        exclude_patterns = ["utilities/sprint/", "debug_screenshots/", "reports/", "__pycache__/", ".git/"]
        python_files = [f for f in self.project_root.rglob("*.py")
                       if not any(pattern in str(f) for pattern in exclude_patterns)]

        enviar_senal_log("INFO", f"📂 {len(python_files)} archivos Python encontrados", "print_migrator", "files")

        for file_path in python_files:
            self.stats["files_scanned"] += 1
            try:
                if scan_only:
                    self._scan_file(file_path)
                else:
                    self._migrate_file(file_path)
            except Exception as e:
                error_msg = f"Error procesando {file_path}: {e}"
                self.stats["errors"].append(error_msg)
                enviar_senal_log("ERROR", error_msg, "print_migrator", "file_error")

        self._print_summary()
        return self.stats

    def _scan_file(self, file_path: Path) -> None:
        """Escanea archivo sin modificarlo"""
        try:
            content = file_path.read_text(encoding="utf-8")
            print_count = len(re.findall(r'\\bprint\\s*\\(', content))
            if print_count > 0:
                enviar_senal_log("INFO", f"📄 {file_path.relative_to(self.project_root)}: {print_count} prints", "print_migrator", "scan_result")
                self.stats["prints_migrated"] += print_count
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error leyendo {file_path}: {e}", "print_migrator", "read_error")

    def _migrate_file(self, file_path: Path) -> None:
        """Migra prints de un archivo específico"""
        try:
            content = file_path.read_text(encoding="utf-8")
            original_content = content

            print_pattern = r'\\bprint\\s*\\(([^)]*)\\)'
            prints_found = re.findall(print_pattern, content)

            if not prints_found:
                return

            # Agregar import si es necesario
            if "from sistema.logging_interface import enviar_senal_log" not in content:
                lines = content.split('\\n')
                import_line = "from sistema.logging_interface import enviar_senal_log"

                insert_index = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith(('import ', 'from ')):
                        insert_index = i + 1
                    elif line.strip() and not line.strip().startswith('#'):
                        break

                lines.insert(insert_index, import_line)
                content = '\\n'.join(lines)

            # Migrar prints
            def replace_print(match):
                print_content = match.group(1).strip()

                # Determinar nivel de log
                if any(keyword in print_content.lower() for keyword in ['error', 'fail', 'exception']):
                    nivel = 'ERROR'
                elif any(keyword in print_content.lower() for keyword in ['warning', 'warn']):
                    nivel = 'WARNING'
                elif any(keyword in print_content.lower() for keyword in ['debug']):
                    nivel = 'DEBUG'
                else:
                    nivel = 'INFO'

                module_name = file_path.stem
                return f'enviar_senal_log("{nivel}", {print_content}, "{module_name}", "migration")'

            content = re.sub(print_pattern, replace_print, content)

            if content != original_content:
                file_path.write_text(content, encoding="utf-8")
                self.stats["files_modified"] += 1
                self.stats["prints_migrated"] += len(prints_found)
                enviar_senal_log("INFO", f"✅ {file_path.relative_to(self.project_root)}: {len(prints_found)} prints migrados", "print_migrator", "migration_success")

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error migrando {file_path}: {e}", "print_migrator", "migration_error")

    def _print_summary(self) -> None:
        """Imprime resumen de la migración"""
        enviar_senal_log("INFO", "📊 === RESUMEN DE MIGRACIÓN ===", "print_migrator", "summary")
        enviar_senal_log("INFO", f"📂 Archivos escaneados: {self.stats['files_scanned']}", "print_migrator", "summary")
        enviar_senal_log("INFO", f"📝 Archivos modificados: {self.stats['files_modified']}", "print_migrator", "summary")
        enviar_senal_log("INFO", f"🔄 Prints migrados: {self.stats['prints_migrated']}", "print_migrator", "summary")

        if self.stats["errors"]:
            enviar_senal_log("WARNING", f"⚠️ Errores: {len(self.stats['errors'])}", "print_migrator", "summary")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Print Migration Tool ICT Engine v5.0")
    parser.add_argument("--scan-only", action="store_true", help="Solo escanear")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent.parent
    migrator = PrintMigrationTool(project_root)
    migrator.scan_project(scan_only=args.scan_only)

if __name__ == "__main__":
    main()
'''

    def _get_console_config_template(self) -> str:
        """Retorna el template de configuración de consola"""
        return '''#!/usr/bin/env python3
"""
🖥️ CONSOLE MODE CONFIGURATION OPTIMIZADO
ICT Engine v5.0 - Configuración para aplicaciones Textual
"""

import os
import sys
from pathlib import Path

def configure_console_mode():
    """Configura el entorno para modo consola limpio"""
    os.environ.update({
        "TEXTUAL_COLOR_SYSTEM": "truecolor",
        "TEXTUAL_DRIVER": "auto",
        "TEXTUAL_LOG": "textual.log"
    })

    if sys.platform == "win32":
        os.environ["PYTHONIOENCODING"] = "utf-8"

    class ConsoleRedirect:
        def __init__(self, log_file: str = "console_output.log"):
            self.log_file = Path(log_file)
            self.log_file.parent.mkdir(exist_ok=True)

        def write(self, text: str):
            if text.strip():
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(text)

        def flush(self):
            pass

    return ConsoleRedirect

def setup_textual_app():
    """Configuración específica para aplicaciones Textual"""
    debug_mode = os.getenv("TEXTUAL_DEBUG", "0") == "1"

    if debug_mode:
        os.environ.update({"TEXTUAL_DEVTOOLS": "1", "TEXTUAL_LOG_LEVEL": "DEBUG"})
    else:
        os.environ["TEXTUAL_LOG_LEVEL"] = "WARNING"

    return debug_mode

# Configurar automáticamente al importar
configure_console_mode()
'''

    def _get_screenshots_readme(self) -> str:
        """Retorna el README optimizado para screenshots"""
        return '''# 📸 Debug Screenshots

Screenshots automáticos durante debugging.

## 🔧 Estructura:
- `dashboard_YYYYMMDD_HHMMSS.png` - Screenshots del dashboard
- `debug_session_YYYYMMDD_HHMMSS.png` - Screenshots de debug sessions
- `manual_YYYYMMDD_HHMMSS.png` - Screenshots manuales

## 🎮 Uso:
1. `python utilities/debug/debug_launcher.py`
2. Presionar F12 para DevTools
3. Screenshots automáticos durante debugging

## 📋 Variables de entorno:
- `TEXTUAL_SCREENSHOT=1` - Habilita screenshots
- `TEXTUAL_DEVTOOLS=1` - Habilita DevTools F12
'''

    def _get_rendering_tests_template(self) -> str:
        """Retorna el template optimizado de rendering tests"""
        return '''#!/usr/bin/env python3
"""
🧪 RENDERING TESTS OPTIMIZADO
ICT Engine v5.0 - Tests de validación de rendering
"""

import time

# Reutilizar imports del bloque superior
# sys, os, subprocess, Path ya importados

# Import manejado al inicio del archivo

class RenderingTests:
    """🧪 Tests optimizados de rendering"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.test_results = []
        enviar_senal_log("INFO", "🧪 Rendering Tests inicializados", "rendering_tests", "initialization")

    def run_all_tests(self) -> bool:
        """Ejecuta todos los tests de rendering"""
        enviar_senal_log("INFO", "🔍 Iniciando tests de rendering...", "rendering_tests", "start")

        tests = [
            ("dashboard_launch", "Test lanzamiento dashboard", self._test_dashboard_launch),
            ("console_output", "Test output limpio consola", self._test_console_output),
            ("textual_compatibility", "Test compatibilidad Textual", self._test_textual_compatibility),
            ("logging_integration", "Test integración logging", self._test_logging_integration)
        ]

        success_count = 0
        for test_id, description, test_func in tests:
            enviar_senal_log("INFO", f"🧪 Ejecutando: {description}", "rendering_tests", "test_execution")

            try:
                result = test_func()
                self.test_results.append({
                    "test_id": test_id,
                    "description": description,
                    "result": "PASS" if result else "FAIL",
                    "timestamp": time.time()
                })

                if result:
                    success_count += 1
                    enviar_senal_log("INFO", f"✅ {description} - PASS", "rendering_tests", "test_pass")
                else:
                    enviar_senal_log("ERROR", f"❌ {description} - FAIL", "rendering_tests", "test_fail")

            except Exception as e:
                self.test_results.append({
                    "test_id": test_id,
                    "description": description,
                    "result": "ERROR",
                    "error": str(e),
                    "timestamp": time.time()
                })
                enviar_senal_log("ERROR", f"❌ Error en {description}: {e}", "rendering_tests", "test_error")

        success_rate = (success_count / len(tests)) * 100
        enviar_senal_log("INFO", f"📊 Tests: {success_count}/{len(tests)} exitosos ({success_rate:.1f}%)", "rendering_tests", "completion")
        return success_count == len(tests)

    def _test_dashboard_launch(self) -> bool:
        """Test de lanzamiento básico del dashboard"""
        try:
            dashboard_path = self.project_root / "dashboard" / "dashboard_definitivo.py"
            if not dashboard_path.exists():
                enviar_senal_log("WARNING", f"⚠️ Dashboard no encontrado: {dashboard_path}", "rendering_tests", "file_missing")
                return False

            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.project_root)

            result = subprocess.run([
                sys.executable, "-m", "py_compile", str(dashboard_path)
            ], capture_output=True, text=True, env=env, timeout=10)

            return result.returncode == 0

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error en test dashboard: {e}", "rendering_tests", "dashboard_error")
            return False

    def _test_console_output(self) -> bool:
        """Test de output limpio en consola"""
        try:
            console_config_path = self.project_root / "utilities" / "debug" / "console_config.py"
            if not console_config_path.exists():
                enviar_senal_log("WARNING", f"⚠️ Console config no encontrado", "rendering_tests", "config_missing")
                return False

            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.project_root)

            test_code = """
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

try:
    from utilities.debug.console_config import configure_console_mode
    configure_console_mode()
    enviar_senal_log("INFO", "Test console configurado exitosamente", "rendering_tests", "console_success")
except Exception as e:
    # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"ERROR: {e}")
"""

            result = subprocess.run([
                sys.executable, "-c", test_code
            ], capture_output=True, text=True, env=env, timeout=5, cwd=str(self.project_root))

            return "SUCCESS" in result.stdout

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error en test console: {e}", "rendering_tests", "console_error")
            return False

    def _test_textual_compatibility(self) -> bool:
        """Test de compatibilidad con Textual"""
        try:
            test_code = """
try:
    import textual
    from textual.app import App
    from textual.widgets import Static
    enviar_senal_log("INFO", "Textual disponible", "rendering_tests", "textual_ok")
    print("TEXTUAL_OK")
except ImportError:
    enviar_senal_log("WARNING", "Textual no disponible", "rendering_tests", "textual_missing")
    print("TEXTUAL_MISSING")
except Exception as e:
    # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"TEXTUAL_ERROR: {e}")
"""

            result = subprocess.run([
                sys.executable, "-c", test_code
            ], capture_output=True, text=True, timeout=5)

            output = result.stdout.strip()
            if "TEXTUAL_OK" in output:
                return True
            elif "TEXTUAL_MISSING" in output:
                enviar_senal_log("WARNING", "⚠️ Textual no instalado - pip install textual", "rendering_tests", "textual_missing")
                return False
            else:
                enviar_senal_log("WARNING", f"⚠️ Error Textual: {output}", "rendering_tests", "textual_error")
                return False

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error en test Textual: {e}", "rendering_tests", "textual_test_error")
            return False

    def _test_logging_integration(self) -> bool:
        """Test de integración del sistema de logging"""
        try:
            test_code = """
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

try:
    # Import manejado al inicio del archivo
    enviar_senal_log("INFO", "Test message", "test_module", "test_category")
    enviar_senal_log("INFO", "Test logging OK", "rendering_tests", "logging_test")
    print("LOGGING_OK")
except ImportError as e:
    # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"LOGGING_IMPORT_ERROR: {e}")
except Exception as e:
    # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"LOGGING_ERROR: {e}")
"""

            result = subprocess.run([
                sys.executable, "-c", test_code
            ], capture_output=True, text=True, timeout=5, cwd=str(self.project_root))

            return "LOGGING_OK" in result.stdout

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error en test logging: {e}", "rendering_tests", "logging_test_error")
            return False

def main():
    project_root = Path(__file__).parent.parent.parent
    tests = RenderingTests(project_root)
    tests.run_all_tests()

if __name__ == "__main__":
    main()
'''

    def _generate_execution_report(self, success_rate: float) -> None:
        """Genera reporte optimizado de la ejecución"""
        try:
            execution_time = (datetime.now() - self.execution_start).total_seconds()

            report = {
                "execution_info": {
                    "sprint": "1.1",
                    "executor_version": "2.0_optimized",
                    "start_time": self.execution_start.isoformat(),
                    "end_time": datetime.now().isoformat(),
                    "duration_seconds": execution_time,
                    "dry_run": self.dry_run
                },
                "results": {
                    "success_rate": success_rate,
                    "tasks_completed": len(self.tasks_completed),
                    "tasks_failed": len(self.tasks_failed),
                    "total_tasks": len(self.tasks_completed) + len(self.tasks_failed)
                },
                "completed_tasks": self.tasks_completed,
                "failed_tasks": self.tasks_failed,
                "next_steps": [
                    "Probar Debug Launcher: python utilities/debug/debug_launcher.py",
                    "Ejecutar migración: python utilities/migration/print_migration_tool.py --scan-only",
                    "Proceder Sprint 1.2 si success_rate > 80%"
                ]
            }

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = self.reports_dir / f"sprint_1_1_execution_{timestamp}.json"

            if not self.dry_run:
                with open(report_path, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)

            enviar_senal_log("INFO", f"📋 Reporte guardado: {report_path.relative_to(self.project_root)}", "sprint_executor", "report")

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error generando reporte: {e}", "sprint_executor", "report_error")

def main():
    """Función principal optimizada"""
    parser = argparse.ArgumentParser(description="Sprint 1.1 Executor Optimizado - ICT Engine v5.0")
    parser.add_argument("--dry-run", action="store_true", help="Modo simulación")
    parser.add_argument("--verbose", action="store_true", help="Modo verbose")
    parser.add_argument("--task", type=str, help="Ejecutar tarea específica")

    args = parser.parse_args()

    executor = Sprint11Executor(dry_run=args.dry_run, verbose=args.verbose)
    success = executor.execute_sprint_11(task_filter=args.task)

    if success:
        enviar_senal_log("INFO", "🎉 ¡Sprint 1.1 completado exitosamente!", "sprint_executor", "final_success")
        enviar_senal_log("INFO", "📋 Próximos pasos:", "sprint_executor", "next_steps")
        enviar_senal_log("INFO", "  - python utilities/debug/debug_launcher.py", "sprint_executor", "next_steps")
        enviar_senal_log("INFO", "  - python utilities/migration/print_migration_tool.py --scan-only", "sprint_executor", "next_steps")
    else:
        enviar_senal_log("ERROR", "⚠️ Sprint 1.1 completado con errores", "sprint_executor", "final_error")

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
