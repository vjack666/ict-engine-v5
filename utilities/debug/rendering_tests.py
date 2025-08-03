#!/usr/bin/env python3
"""
🧪 RENDERING TESTS
ICT Engine v5.0 - Tests de validación de rendering

Tests automáticos para validar que el rendering de las aplicaciones
Textual funciona correctamente sin interferencias.
"""

import sys
import os
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Tuple

# Agregar el directorio raíz al Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from sistema.logging_interface import enviar_senal_log
except ImportError:
    def enviar_senal_log(nivel, mensaje, modulo="rendering", categoria="tests"):
        enviar_senal_log("INFO", f"[{nivel}] {modulo}.{categoria}: {mensaje}", "rendering_tests", "migration")

class RenderingTests:
    """🧪 Tests de rendering para aplicaciones Textual"""
    
    def __init__(self, project_root: Path):
        """Inicializa los tests de rendering"""
        self.project_root = project_root
        self.test_results = []
        
        enviar_senal_log("INFO", "🧪 Rendering Tests inicializados", __name__, "tests")
    
    def run_all_tests(self) -> bool:
        """Ejecuta todos los tests de rendering"""
        enviar_senal_log("INFO", "🔍 Iniciando tests de rendering...", __name__, "tests")
        
        tests = [
            ("dashboard_launch", "Test de lanzamiento del dashboard", self._test_dashboard_launch),
            ("console_output", "Test de output limpio en consola", self._test_console_output),
            ("textual_compatibility", "Test de compatibilidad Textual", self._test_textual_compatibility),
            ("logging_integration", "Test de integración de logging", self._test_logging_integration)
        ]
        
        success_count = 0
        
        for test_id, description, test_func in tests:
            enviar_senal_log("INFO", f"🧪 Ejecutando: {description}", __name__, "tests")
            
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
                    enviar_senal_log("INFO", f"✅ {description} - PASS", __name__, "tests")
                else:
                    enviar_senal_log("ERROR", f"❌ {description} - FAIL", __name__, "tests")
                    
            except Exception as e:
                self.test_results.append({
                    "test_id": test_id,
                    "description": description,
                    "result": "ERROR",
                    "error": str(e),
                    "timestamp": time.time()
                })
                enviar_senal_log("ERROR", f"❌ Error en {description}: {e}", __name__, "tests")
        
        success_rate = (success_count / len(tests)) * 100
        enviar_senal_log("INFO", f"📊 Tests completados: {success_count}/{len(tests)} exitosos ({success_rate:.1f}%)", __name__, "tests")
        
        return success_count == len(tests)
    
    def _test_dashboard_launch(self) -> bool:
        """Test de lanzamiento básico del dashboard"""
        try:
            dashboard_path = self.project_root / "dashboard" / "dashboard_definitivo.py"
            
            if not dashboard_path.exists():
                enviar_senal_log("WARNING", f"⚠️ Dashboard no encontrado: {dashboard_path}", __name__, "tests")
                return False
            
            # Test de sintaxis básica (import test)
            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.project_root)
            
            result = subprocess.run([
                sys.executable, "-m", "py_compile", str(dashboard_path)
            ], capture_output=True, text=True, env=env, timeout=10)
            
            return result.returncode == 0
            
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error en test dashboard launch: {e}", __name__, "tests")
            return False
    
    def _test_console_output(self) -> bool:
        """Test de output limpio en consola"""
        try:
            # Verificar que la configuración de console mode existe
            console_config_path = self.project_root / "utilities" / "debug" / "console_config.py"
            
            if not console_config_path.exists():
                enviar_senal_log("WARNING", f"⚠️ Console config no encontrado: {console_config_path}", __name__, "tests")
                return False
            
            # Test de importación de la configuración
            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.project_root)
            
            test_code = """
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

try:
    from utilities.debug.console_config import configure_console_mode
    configure_console_mode()
    enviar_senal_log("INFO", "SUCCESS", "rendering_tests", "migration")
except Exception as e:
    enviar_senal_log("ERROR", f"ERROR: {e}", "rendering_tests", "migration")
"""
            
            result = subprocess.run([
                sys.executable, "-c", test_code
            ], capture_output=True, text=True, env=env, timeout=5, cwd=str(self.project_root))
            
            return "SUCCESS" in result.stdout
            
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error en test console output: {e}", __name__, "tests")
            return False
    
    def _test_textual_compatibility(self) -> bool:
        """Test de compatibilidad con Textual"""
        try:
            # Test de importación de Textual
            test_code = """
try:
    import textual
    from textual.app import App
    from textual.widgets import Static
    enviar_senal_log("INFO", "TEXTUAL_OK", "rendering_tests", "migration")
except ImportError:
    enviar_senal_log("INFO", "TEXTUAL_MISSING", "rendering_tests", "migration")
except Exception as e:
    enviar_senal_log("ERROR", f"TEXTUAL_ERROR: {e}", "rendering_tests", "migration")
"""
            
            result = subprocess.run([
                sys.executable, "-c", test_code
            ], capture_output=True, text=True, timeout=5)
            
            output = result.stdout.strip()
            
            if "TEXTUAL_OK" in output:
                return True
            elif "TEXTUAL_MISSING" in output:
                enviar_senal_log("WARNING", "⚠️ Textual no está instalado - ejecutar: pip install textual", __name__, "tests")
                return False
            else:
                enviar_senal_log("WARNING", f"⚠️ Error de compatibilidad Textual: {output}", __name__, "tests")
                return False
                
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error en test Textual compatibility: {e}", __name__, "tests")
            return False
    
    def _test_logging_integration(self) -> bool:
        """Test de integración del sistema de logging"""
        try:
            # Test de importación del sistema de logging
            test_code = """
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

try:
    from sistema.logging_interface import enviar_senal_log
    enviar_senal_log("INFO", "Test message", "test_module", "test_category")
    enviar_senal_log("INFO", "LOGGING_OK", "rendering_tests", "migration")
except ImportError as e:
    enviar_senal_log("ERROR", f"LOGGING_IMPORT_ERROR: {e}", "rendering_tests", "migration")
except Exception as e:
    enviar_senal_log("ERROR", f"LOGGING_ERROR: {e}", "rendering_tests", "migration")
"""
            
            result = subprocess.run([
                sys.executable, "-c", test_code
            ], capture_output=True, text=True, timeout=5, cwd=str(self.project_root))
            
            return "LOGGING_OK" in result.stdout
            
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error en test logging integration: {e}", __name__, "tests")
            return False

def main():
    """Función principal de los tests"""
    project_root = Path(__file__).parent.parent.parent
    tests = RenderingTests(project_root)
    tests.run_all_tests()

if __name__ == "__main__":
    main()
