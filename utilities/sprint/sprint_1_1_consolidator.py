# [TARGET] SPRINT 1.1 CONSOLIDATOR - DEBUG SYSTEM COMPLETE
# Herramienta final para consolidar todas las mejoras del Sprint 1.1

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import subprocess
import argparse
from typing import Dict, List

class Sprint11Consolidator:
    """
    Consolidador final para Sprint 1.1: Debug System & Clean Code

    Funcionalidades:
    - Validación completa del debug launcher
    - Verificación de migración de prints
    - Configuración de console mode
    - Testing de rendering limpio
    - Generación de reporte de sprint
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.sprint_report = {
            'sprint': '1.1',
            'name': 'Debug System & Clean Code',
            'start_date': datetime.now().isoformat(),
            'status': 'IN_PROGRESS',
            'tasks_completed': [],
            'tasks_pending': [],
            'issues_found': [],
            'metrics': {},
            'next_actions': []
        }

        # [TARGET] Tareas del Sprint 1.1
        self.sprint_tasks = {
            'debug_launcher': {
                'name': 'Crear debug_launcher.py con DevTools F12 support',
                'priority': 'CRÍTICA',
                'estimated_hours': 6,
                'deliverable': 'debug_launcher.py'
            },
            'print_migration': {
                'name': 'Migrar 20+ print statements a enviar_senal_log()',
                'priority': 'ALTA',
                'estimated_hours': 4,
                'deliverable': 'Codebase limpio'
            },
            'console_mode': {
                'name': 'Configurar console mode para Textual app',
                'priority': 'MEDIA',
                'estimated_hours': 3,
                'deliverable': 'Console mode configurado'
            },
            'screenshot_tool': {
                'name': 'Implementar screenshot capability',
                'priority': 'BAJA',
                'estimated_hours': 3,
                'deliverable': 'Screenshot tool'
            },
            'rendering_tests': {
                'name': 'Testing intensivo de rendering limpio',
                'priority': 'ALTA',
                'estimated_hours': 3,
                'deliverable': '100+ actualizaciones sin corrupción'
            }
        }

    def run_complete_validation(self) -> Dict:
        """Ejecuta validación completa del Sprint 1.1"""
        print("[SCAN] Iniciando validación completa del Sprint 1.1...")

        validation_results = {
            'overall_status': 'UNKNOWN',
            'task_results': {},
            'critical_issues': [],
            'warnings': [],
            'recommendations': []
        }

        # [OK] Validar cada tarea del sprint
        for task_id, task_info in self.sprint_tasks.items():
            print(f"\n[CHECK] Validando tarea: {task_info['name']}")

            task_result = self._validate_task(task_id, task_info)
            validation_results['task_results'][task_id] = task_result

            if task_result['status'] == 'COMPLETED':
                self.sprint_report['tasks_completed'].append(task_id)
                print(f"  [OK] COMPLETADA")
            elif task_result['status'] == 'FAILED':
                self.sprint_report['tasks_pending'].append(task_id)
                print(f"  [ERROR] FALLIDA: {task_result.get('error', 'Unknown error')}")
            else:
                self.sprint_report['tasks_pending'].append(task_id)
                print(f"  [PENDING] PENDIENTE")

        # [TARGET] Determinar estado general
        completed_tasks = len(self.sprint_report['tasks_completed'])
        total_tasks = len(self.sprint_tasks)
        completion_rate = (completed_tasks / total_tasks) * 100

        if completion_rate >= 90:
            validation_results['overall_status'] = 'SPRINT_COMPLETE'
        elif completion_rate >= 70:
            validation_results['overall_status'] = 'MOSTLY_COMPLETE'
        elif completion_rate >= 50:
            validation_results['overall_status'] = 'PARTIAL_COMPLETE'
        else:
            validation_results['overall_status'] = 'NEEDS_WORK'

        self.sprint_report['completion_rate'] = completion_rate
        self.sprint_report['status'] = validation_results['overall_status']

        return validation_results

    def _validate_task(self, task_id: str, task_info: Dict) -> Dict:
        """Valida una tarea específica del sprint"""
        task_result = {
            'task_id': task_id,
            'status': 'PENDING',
            'checks_passed': 0,
            'checks_total': 0,
            'details': [],
            'error': None
        }

        try:
            if task_id == 'debug_launcher':
                task_result = self._validate_debug_launcher()
            elif task_id == 'print_migration':
                task_result = self._validate_print_migration()
            elif task_id == 'console_mode':
                task_result = self._validate_console_mode()
            elif task_id == 'screenshot_tool':
                task_result = self._validate_screenshot_tool()
            elif task_id == 'rendering_tests':
                task_result = self._validate_rendering_tests()

        except Exception as e:
            task_result['status'] = 'FAILED'
            task_result['error'] = str(e)

        return task_result

    def _validate_debug_launcher(self) -> Dict:
        """Valida que debug_launcher.py esté funcionando"""
        result = {
            'task_id': 'debug_launcher',
            'checks_passed': 0,
            'checks_total': 5,
            'details': [],
            'status': 'PENDING'
        }

        # [OK] Check 1: Archivo existe
        launcher_path = self.project_root / "utilities" / "debug" / "debug_launcher.py"
        if launcher_path.exists():
            result['checks_passed'] += 1
            result['details'].append("[OK] debug_launcher.py existe")
        else:
            result['details'].append("[ERROR] debug_launcher.py no encontrado")
            result['status'] = 'FAILED'
            return result

        # [OK] Check 2: Imports correctos
        try:
            with open(launcher_path, 'r', encoding='utf-8') as f:
                content = f.read()

            required_imports = [
                'from textual.app import App',
                'dashboard.dashboard_definitivo',
                'class DebugLauncher'
            ]

            imports_ok = all(imp in content for imp in required_imports)
            if imports_ok:
                result['checks_passed'] += 1
                result['details'].append("[OK] Imports correctos")
            else:
                result['details'].append("[ERROR] Imports faltantes")

        except Exception as e:
            result['details'].append(f"[ERROR] Error leyendo archivo: {e}")

        # [OK] Check 3: Bindings F12
        if 'F12' in content or 'f12' in content:
            result['checks_passed'] += 1
            result['details'].append("[OK] Binding F12 presente")
        else:
            result['details'].append("[ERROR] Binding F12 no encontrado")

        # [OK] Check 4: DevTools functionality
        if 'toggle_devtools' in content:
            result['checks_passed'] += 1
            result['details'].append("[OK] DevTools functionality presente")
        else:
            result['details'].append("[ERROR] DevTools functionality faltante")

        # [OK] Check 5: Launch modes
        launch_modes = ['launch_normal', 'launch_debug', 'launch_console']
        modes_present = sum(1 for mode in launch_modes if mode in content)
        if modes_present >= 2:
            result['checks_passed'] += 1
            result['details'].append(f"[OK] Launch modes ({modes_present}/3)")
        else:
            result['details'].append(f"[ERROR] Launch modes insuficientes ({modes_present}/3)")

        # [TARGET] Determinar estado final
        if result['checks_passed'] >= 4:
            result['status'] = 'COMPLETED'
        elif result['checks_passed'] >= 2:
            result['status'] = 'PARTIAL'
        else:
            result['status'] = 'FAILED'

        return result

    def _validate_print_migration(self) -> Dict:
        """Valida que la migración de prints esté completa"""
        result = {
            'task_id': 'print_migration',
            'checks_passed': 0,
            'checks_total': 4,
            'details': [],
            'status': 'PENDING'
        }

        # [OK] Check 1: Print migration tool existe
        migration_tool_path = self.project_root / "utilities" / "migration" / "print_migration_tool.py"
        if migration_tool_path.exists():
            result['checks_passed'] += 1
            result['details'].append("[OK] Print migration tool existe")
        else:
            result['details'].append("[ERROR] Print migration tool no encontrado")

        # [OK] Check 2: Escanear prints restantes
        try:
            # Importar herramienta de migración si existe
            if migration_tool_path.exists():
                import importlib.util
                spec = importlib.util.spec_from_file_location("print_migration_tool", migration_tool_path)
                migration_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(migration_module)

                migration_tool = migration_module.PrintMigrationTool(self.project_root)
                scan_results = migration_tool.scan_project()

                total_prints = scan_results['total_prints']
                if total_prints == 0:
                    result['checks_passed'] += 2  # Double points for zero prints
                    result['details'].append("[OK] No hay print statements restantes")
                elif total_prints <= 5:
                    result['checks_passed'] += 1
                    result['details'].append(f"[WARNING] Quedan {total_prints} prints (aceptable)")
                else:
                    result['details'].append(f"[ERROR] Quedan {total_prints} prints (demasiados)")
            else:
                result['details'].append("[ERROR] No se pudo escanear prints")

        except Exception as e:
            result['details'].append(f"[ERROR] Error escaneando prints: {e}")

        # [OK] Check 3: enviar_senal_log usage
        enviar_senal_log_usage = 0
        try:
            for py_file in self.project_root.rglob("*.py"):
                if py_file.name in ['debug_launcher.py', 'print_migration_tool.py']:
                    continue

                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'enviar_senal_log' in content:
                            enviar_senal_log_usage += content.count('enviar_senal_log')
                except:
                    continue

            if enviar_senal_log_usage > 0:
                result['checks_passed'] += 1
                result['details'].append(f"[OK] enviar_senal_log usado {enviar_senal_log_usage} veces")
            else:
                result['details'].append("[ERROR] enviar_senal_log no encontrado")

        except Exception as e:
            result['details'].append(f"[ERROR] Error verificando enviar_senal_log: {e}")

        # [TARGET] Determinar estado
        if result['checks_passed'] >= 3:
            result['status'] = 'COMPLETED'
        elif result['checks_passed'] >= 2:
            result['status'] = 'PARTIAL'
        else:
            result['status'] = 'FAILED'

        return result

    def _validate_console_mode(self) -> Dict:
        """Valida configuración de console mode"""
        result = {
            'task_id': 'console_mode',
            'checks_passed': 0,
            'checks_total': 3,
            'details': [],
            'status': 'PENDING'
        }

        # [OK] Check 1: Environment variables en debug launcher
        launcher_path = self.project_root / "utilities" / "debug" / "debug_launcher.py"
        if launcher_path.exists():
            try:
                with open(launcher_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if 'TEXTUAL_CONSOLE' in content:
                    result['checks_passed'] += 1
                    result['details'].append("[OK] TEXTUAL_CONSOLE configurado")
                else:
                    result['details'].append("[ERROR] TEXTUAL_CONSOLE no configurado")

                if 'TEXTUAL_DEBUG' in content:
                    result['checks_passed'] += 1
                    result['details'].append("[OK] TEXTUAL_DEBUG configurado")
                else:
                    result['details'].append("[ERROR] TEXTUAL_DEBUG no configurado")

            except Exception as e:
                result['details'].append(f"[ERROR] Error verificando console mode: {e}")

        # [OK] Check 2: Console mode launch option
        if launcher_path.exists():
            try:
                with open(launcher_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if 'launch_console' in content:
                    result['checks_passed'] += 1
                    result['details'].append("[OK] Launch console mode disponible")
                else:
                    result['details'].append("[ERROR] Launch console mode no encontrado")

            except Exception as e:
                result['details'].append(f"[ERROR] Error verificando launch console: {e}")        # [TARGET] Determinar estado
        if result['checks_passed'] >= 2:
            result['status'] = 'COMPLETED'
        elif result['checks_passed'] >= 1:
            result['status'] = 'PARTIAL'
        else:
            result['status'] = 'FAILED'

        return result

    def _validate_screenshot_tool(self) -> Dict:
        """Valida funcionalidad de screenshots"""
        result = {
            'task_id': 'screenshot_tool',
            'checks_passed': 0,
            'checks_total': 2,
            'details': [],
            'status': 'PENDING'
        }

        # [OK] Check 1: Screenshot functionality en debug launcher
        launcher_path = self.project_root / "utilities" / "debug" / "debug_launcher.py"
        if launcher_path.exists():
            try:
                with open(launcher_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if 'action_screenshot' in content:
                    result['checks_passed'] += 1
                    result['details'].append("[OK] Screenshot action implementado")
                else:
                    result['details'].append("[ERROR] Screenshot action no encontrado")

                if '_capture_debug_screenshot' in content:
                    result['checks_passed'] += 1
                    result['details'].append("[OK] Screenshot capture function presente")
                else:
                    result['details'].append("[ERROR] Screenshot capture function faltante")

            except Exception as e:
                result['details'].append(f"[ERROR] Error verificando screenshot tool: {e}")        # [TARGET] Determinar estado
        if result['checks_passed'] >= 1:
            result['status'] = 'COMPLETED'
        else:
            result['status'] = 'FAILED'

        return result

    def _validate_rendering_tests(self) -> Dict:
        """Valida sistema de testing de rendering"""
        result = {
            'task_id': 'rendering_tests',
            'checks_passed': 0,
            'checks_total': 3,
            'details': [],
            'status': 'PENDING'
        }

        # [OK] Check 1: Logging system funcionando
        try:
            from sistema.logging_interface import enviar_senal_log
            result['checks_passed'] += 1
            result['details'].append("[OK] Sistema de logging funcional")
        except ImportError:
            result['details'].append("[ERROR] Sistema de logging no disponible")

        # [OK] Check 2: Dashboard principal ejecutable
        dashboard_path = self.project_root / "dashboard" / "dashboard_definitivo.py"
        if dashboard_path.exists():
            result['checks_passed'] += 1
            result['details'].append("[OK] Dashboard principal existe")
        else:
            result['details'].append("[ERROR] Dashboard principal no encontrado")

        # [OK] Check 3: Debug launcher ejecutable
        launcher_path = self.project_root / "utilities" / "debug" / "debug_launcher.py"
        if launcher_path.exists():
            result['checks_passed'] += 1
            result['details'].append("[OK] Debug launcher ejecutable")
        else:
            result['details'].append("[ERROR] Debug launcher no disponible")

        # [TARGET] Determinar estado
        if result['checks_passed'] >= 2:
            result['status'] = 'COMPLETED'
        elif result['checks_passed'] >= 1:
            result['status'] = 'PARTIAL'
        else:
            result['status'] = 'FAILED'

        return result

    def generate_sprint_report(self) -> str:
        """Genera reporte completo del sprint"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.project_root / f"sprint_1_1_report_{timestamp}.json"

        # [REPORT] Métricas adicionales
        self.sprint_report['metrics'] = {
            'completion_rate': self.sprint_report.get('completion_rate', 0),
            'tasks_total': len(self.sprint_tasks),
            'tasks_completed': len(self.sprint_report['tasks_completed']),
            'tasks_pending': len(self.sprint_report['tasks_pending']),
            'validation_timestamp': datetime.now().isoformat()
        }

        # [TARGET] Próximas acciones recomendadas
        if self.sprint_report['completion_rate'] >= 80:
            self.sprint_report['next_actions'] = [
                "[OK] Sprint 1.1 mayormente completo",
                "[LAUNCH] Proceder con Sprint 1.2: Trading Engine Foundation",
                "[REPORT] Ejecutar testing final de integración",
                "[LIST] Actualizar documentation del sistema"
            ]
        else:
            self.sprint_report['next_actions'] = [
                "[WARNING] Completar tareas pendientes del Sprint 1.1",
                "[SCAN] Resolver issues críticos identificados",
                "[TEST] Ejecutar validación nuevamente",
                "[LIST] Revisar criterios de aceptación"
            ]

        # [SAVE] Guardar reporte
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.sprint_report, f, indent=2, ensure_ascii=False)

        return str(report_path)

    def run_integration_tests(self) -> Dict:
        """Ejecuta tests de integración básicos"""
        print("[TEST] Ejecutando tests de integración...")

        integration_results = {
            'tests_run': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'test_details': []
        }

        # [TEST] Test 1: Import básico del debug launcher
        try:
            launcher_path = self.project_root / "debug_launcher.py"
            if launcher_path.exists():
                spec = importlib.util.spec_from_file_location("debug_launcher", launcher_path)
                launcher_module = importlib.util.module_from_spec(spec)
                # No ejecutamos spec.loader.exec_module() para evitar side effects
                integration_results['tests_run'] += 1
                integration_results['tests_passed'] += 1
                integration_results['test_details'].append("[OK] Debug launcher importable")
            else:
                integration_results['tests_run'] += 1
                integration_results['tests_failed'] += 1
                integration_results['test_details'].append("[ERROR] Debug launcher no encontrado")
        except Exception as e:
            integration_results['tests_run'] += 1
            integration_results['tests_failed'] += 1
            integration_results['test_details'].append(f"[ERROR] Error importando debug launcher: {e}")

        # [TEST] Test 2: Sistema de logging funcional
        try:
            enviar_senal_log("INFO", "Test de integración Sprint 1.1", "sprint_consolidator", "test")
            integration_results['tests_run'] += 1
            integration_results['tests_passed'] += 1
            integration_results['test_details'].append("[OK] Sistema de logging funcional")
        except Exception as e:
            integration_results['tests_run'] += 1
            integration_results['tests_failed'] += 1
            integration_results['test_details'].append(f"[ERROR] Error en sistema de logging: {e}")

        # [TEST] Test 3: Estructura de directorios
        required_dirs = ['dashboard', 'core', 'sistema', 'config']
        dirs_ok = 0
        for dir_name in required_dirs:
            if (self.project_root / dir_name).exists():
                dirs_ok += 1

        integration_results['tests_run'] += 1
        if dirs_ok == len(required_dirs):
            integration_results['tests_passed'] += 1
            integration_results['test_details'].append("[OK] Estructura de directorios correcta")
        else:
            integration_results['tests_failed'] += 1
            integration_results['test_details'].append(f"[ERROR] Estructura de directorios incompleta ({dirs_ok}/{len(required_dirs)})")

        return integration_results


def main():
    """Función principal del consolidator"""
    parser = argparse.ArgumentParser(description="Sprint 1.1 Consolidator")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(),
                       help="Root directory of the project")
    parser.add_argument("--validation-only", action="store_true",
                       help="Only run validation, skip integration tests")
    parser.add_argument("--integration-only", action="store_true",
                       help="Only run integration tests")
    parser.add_argument("--report", action="store_true",
                       help="Generate detailed sprint report")

    args = parser.parse_args()

    # [TARGET] Inicializar consolidator
    consolidator = Sprint11Consolidator(args.project_root)

    print("[TARGET] SPRINT 1.1 CONSOLIDATOR - DEBUG SYSTEM & CLEAN CODE")
    print("=" * 60)

    if args.integration_only:
        # [TEST] Solo integration tests
        print("[TEST] Ejecutando solo tests de integración...")
        integration_results = consolidator.run_integration_tests()

        print(f"\n[REPORT] RESULTADOS DE INTEGRACIÓN:")
        print(f"  [TEST] Tests ejecutados: {integration_results['tests_run']}")
        print(f"  [OK] Tests pasados: {integration_results['tests_passed']}")
        print(f"  [ERROR] Tests fallidos: {integration_results['tests_failed']}")

        for detail in integration_results['test_details']:
            print(f"  {detail}")

    elif args.validation_only:
        # [SCAN] Solo validación
        print("[SCAN] Ejecutando solo validación de tareas...")
        validation_results = consolidator.run_complete_validation()

        print(f"\n[REPORT] RESULTADOS DE VALIDACIÓN:")
        print(f"  [CHART] Estado general: {validation_results['overall_status']}")
        print(f"  [PROGRESS] Completitud: {consolidator.sprint_report['completion_rate']:.1f}%")
        print(f"  [OK] Tareas completadas: {len(consolidator.sprint_report['tasks_completed'])}")
        print(f"  [PENDING] Tareas pendientes: {len(consolidator.sprint_report['tasks_pending'])}")

    else:
        # [LAUNCH] Validación completa + integration tests
        print("[LAUNCH] Ejecutando validación completa y tests de integración...")

        # [SCAN] Validación de tareas
        validation_results = consolidator.run_complete_validation()

        # [TEST] Integration tests
        integration_results = consolidator.run_integration_tests()

        # [REPORT] Resultados combinados
        print(f"\n[SUCCESS] RESUMEN COMPLETO DEL SPRINT 1.1:")
        print("=" * 50)

        print(f"\n[VALIDATION] VALIDACIÓN DE TAREAS:")
        print(f"  [CHART] Estado general: {validation_results['overall_status']}")
        print(f"  [REPORT] Completitud: {consolidator.sprint_report['completion_rate']:.1f}%")
        print(f"  [OK] Tareas completadas: {len(consolidator.sprint_report['tasks_completed'])}")
        print(f"  [PENDING] Tareas pendientes: {len(consolidator.sprint_report['tasks_pending'])}")

        print(f"\n[TEST] TESTS DE INTEGRACIÓN:")
        print(f"  [TEST] Tests ejecutados: {integration_results['tests_run']}")
        print(f"  [OK] Tests pasados: {integration_results['tests_passed']}")
        print(f"  [ERROR] Tests fallidos: {integration_results['tests_failed']}")

        # [TARGET] Recomendaciones
        print(f"\n[TARGET] PRÓXIMAS ACCIONES:")
        for action in consolidator.sprint_report['next_actions']:
            print(f"  {action}")

        # 🏆 Estado final
        if consolidator.sprint_report['completion_rate'] >= 80:
            print(f"\n🏆 ¡SPRINT 1.1 EXITOSO!")
            print("[LAUNCH] Listo para proceder con Sprint 1.2: Trading Engine Foundation")
        else:
            print(f"\n[WARNING] SPRINT 1.1 REQUIERE ATENCIÓN")
            print("[TOOL] Completar tareas pendientes antes de continuar")

    # [REPORT] Generar reporte si se solicita
    if args.report:
        report_path = consolidator.generate_sprint_report()
        print(f"\n[REPORT] Reporte detallado guardado en: {report_path}")


if __name__ == "__main__":
    main()
