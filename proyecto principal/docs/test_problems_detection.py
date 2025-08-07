#!/usr/bin/env python3
"""
🧪 ITC ENGINE v5.0 - TESTING SISTEMA DETECCIÓN DE ERRORES
==========================================================

🎯 OBJETIVO: Testing completo del Sistema de Detección de Errores Jerárquico
            incluyendo motor, dashboard, integración y rendimiento

📊 CARACTERÍSTICAS:
   - ✅ Testing unitario del motor de detección
   - ✅ Testing de integración dashboard
   - ✅ Validación de rendimiento
   - ✅ Testing de casos extremos
   - ✅ Generación de reportes automáticos

🔬 COBERTURA:
   - Motor de detección principal
   - Renderizador de problemas
   - Patch de integración dashboard
   - Scripts de automatización
   - Validación end-to-end

📅 Fecha: 2025-08-06 | Versión: 1.0.0
👤 Autor: ITC Engine v5.0 System
"""

import unittest
import sys
import os
import time
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
import subprocess

# Agregar workspace root al path
WORKSPACE_ROOT = Path(__file__).parent
sys.path.insert(0, str(WORKSPACE_ROOT))

# Importaciones del sistema a testear
try:
    # Usar importación dinámica para evitar problemas de dependencias
    import importlib.util

    # Import detector
    detector_spec = importlib.util.spec_from_file_location(
        "error_detector",
        WORKSPACE_ROOT / "scripts" / "error_detection" / "error_detector.py"
    )
    detector_module = importlib.util.module_from_spec(detector_spec)
    detector_spec.loader.exec_module(detector_module)

    ErrorDetector = detector_module.ErrorDetector
    Severity = detector_module.Severity
    Category = detector_module.Category

    # Import renderer
    renderer_spec = importlib.util.spec_from_file_location(
        "problems_tab_renderer",
        WORKSPACE_ROOT / "dashboard" / "problems_tab_renderer.py"
    )
    renderer_module = importlib.util.module_from_spec(renderer_spec)
    renderer_spec.loader.exec_module(renderer_module)

    ProblemsTabRenderer = renderer_module.ProblemsTabRenderer
    render_problems_tab_simple = renderer_module.render_problems_tab_simple
    get_problems_summary = renderer_module.get_problems_summary

    # Import patcher
    patcher_spec = importlib.util.spec_from_file_location(
        "dashboard_problems_patch",
        WORKSPACE_ROOT / "dashboard" / "dashboard_problems_patch.py"
    )
    patcher_module = importlib.util.module_from_spec(patcher_spec)
    patcher_spec.loader.exec_module(patcher_module)

    DashboardPatcher = patcher_module.DashboardPatcher

    IMPORTS_OK = True
except Exception as e:
    IMPORTS_OK = False
    IMPORT_ERROR = str(e)


class TestErrorDetector(unittest.TestCase):
    """🔍 Tests del motor principal de detección"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.test_workspace = tempfile.mkdtemp()
        self.test_workspace_path = Path(self.test_workspace)

        # Crear estructura de prueba
        self._create_test_structure()

        self.detector = ErrorDetector(self.test_workspace)

    def tearDown(self):
        """Limpieza después de cada test"""
        shutil.rmtree(self.test_workspace, ignore_errors=True)

    def _create_test_structure(self):
        """Crear estructura de archivos de prueba"""
        # Directorio core con archivo problemático
        core_dir = self.test_workspace_path / "core"
        core_dir.mkdir()

        # Archivo con errores de sintaxis
        syntax_error_file = core_dir / "syntax_error.py"
        syntax_error_file.write_text("""
def broken_function(
    # Función con error de sintaxis - paréntesis no cerrado
    print("Esto causará error")
    return True
""")

        # Archivo con imports problemáticos
        import_error_file = core_dir / "import_issues.py"
        import_error_file.write_text("""
import os
import subprocess
from .. import something_dangerous
# Hardcoded path
path = "C:\\hardcoded\\path"
print("Debug statement in production")
TODO: Fix this later
""")

        # Archivo largo
        long_file = core_dir / "long_file.py"
        long_content = "# Very long file\n" + "\n".join([f"def function_{i}(): pass" for i in range(100)])
        long_file.write_text(long_content)

        # Archivo crítico sin docstring
        critical_file = self.test_workspace_path / "main.py"
        critical_file.write_text("""
import sys
def main():
    print("Main function")
if __name__ == "__main__":
    main()
""")

        # Dashboard directory
        dashboard_dir = self.test_workspace_path / "dashboard"
        dashboard_dir.mkdir()

        dashboard_file = dashboard_dir / "test_dashboard.py"
        dashboard_file.write_text("""
import streamlit as st
def render_dashboard():
    st.title("Test Dashboard")
""")

    def test_detector_initialization(self):
        """Test inicialización del detector"""
        self.assertIsInstance(self.detector, ErrorDetector)
        self.assertEqual(self.detector.workspace_root, Path(self.test_workspace))
        self.assertEqual(len(self.detector.problems), 0)

    def test_syntax_error_detection(self):
        """Test detección de errores de sintaxis"""
        # Ejecutar análisis
        self.detector._analyze_directory("core")

        # Verificar que se detectó error de sintaxis
        syntax_errors = [p for p in self.detector.problems if p.problem_type == "SYNTAX_ERROR"]
        self.assertGreater(len(syntax_errors), 0)

        # Verificar severidad
        self.assertTrue(any(p.severity in [Severity.CRITICAL.value, Severity.HIGH.value] for p in syntax_errors))

    def test_import_issues_detection(self):
        """Test detección de problemas de imports"""
        self.detector._analyze_directory("core")

        # Verificar detección de imports relativos problemáticos
        relative_imports = [p for p in self.detector.problems if p.problem_type == "RELATIVE_IMPORT"]
        self.assertGreater(len(relative_imports), 0)

        # Verificar detección de imports críticos
        critical_imports = [p for p in self.detector.problems if p.problem_type == "CRITICAL_IMPORT"]
        self.assertGreater(len(critical_imports), 0)

    def test_code_quality_detection(self):
        """Test detección de problemas de calidad"""
        self.detector._analyze_directory("core")

        # Verificar detección de TODO comments
        todo_comments = [p for p in self.detector.problems if p.problem_type == "TODO_COMMENT"]
        self.assertGreater(len(todo_comments), 0)

        # Verificar detección de paths hardcodeados
        hardcoded_paths = [p for p in self.detector.problems if p.problem_type == "HARDCODED_PATH"]
        self.assertGreater(len(hardcoded_paths), 0)

        # Verificar detección de print statements
        print_statements = [p for p in self.detector.problems if p.problem_type == "PRINT_STATEMENT"]
        self.assertGreater(len(print_statements), 0)

    def test_file_structure_analysis(self):
        """Test análisis de estructura de archivos"""
        self.detector._analyze_directory("core")

        # Verificar detección de archivos largos
        large_files = [p for p in self.detector.problems if p.problem_type == "LARGE_FILE"]
        self.assertGreater(len(large_files), 0)

    def test_critical_files_analysis(self):
        """Test análisis de archivos críticos"""
        self.detector._analyze_critical_files()

        # Verificar detección de falta de docstring en main.py
        missing_docstrings = [p for p in self.detector.problems if p.problem_type == "MISSING_DOCSTRING"]
        self.assertGreater(len(missing_docstrings), 0)

    def test_categorization(self):
        """Test categorización de archivos"""
        # Test categorización de dashboard
        dashboard_file = self.test_workspace_path / "dashboard" / "test.py"
        category = self.detector._categorize_file(dashboard_file)
        self.assertEqual(category, Category.DASHBOARD)

        # Test categorización de core
        core_file = self.test_workspace_path / "core" / "test.py"
        category = self.detector._categorize_file(core_file)
        self.assertEqual(category, Category.SISTEMA)

    def test_full_analysis(self):
        """Test análisis completo del sistema"""
        start_time = time.time()

        report = self.detector.analyze_full_system(quick_mode=True)

        end_time = time.time()

        # Verificar estructura del reporte
        self.assertIn('timestamp', report)
        self.assertIn('summary', report)
        self.assertIn('statistics', report)
        self.assertIn('problems', report)

        # Verificar que se encontraron problemas
        self.assertGreater(report['summary']['total_problems'], 0)

        # Verificar tiempo de ejecución razonable
        self.assertLess(end_time - start_time, 30)  # Menos de 30 segundos

    def test_dashboard_summary(self):
        """Test resumen para dashboard"""
        self.detector.analyze_full_system(quick_mode=True)

        summary = self.detector.get_dashboard_summary()

        # Verificar estructura
        self.assertIn('total_problems', summary)
        self.assertIn('critical_problems', summary)
        self.assertIn('files_analyzed', summary)
        self.assertIn('top_problems', summary)


class TestProblemsTabRenderer(unittest.TestCase):
    """🎨 Tests del renderizador de la pestaña problemas"""

    def setUp(self):
        """Configuración inicial"""
        self.renderer = ProblemsTabRenderer()

    def test_renderer_initialization(self):
        """Test inicialización del renderer"""
        self.assertIsInstance(self.renderer, ProblemsTabRenderer)
        self.assertEqual(len(self.renderer.current_problems), 0)

    def test_simple_tab_rendering(self):
        """Test renderizado simple"""
        # Agregar problema de prueba
        self.renderer.current_problems = [{
            'severity': '🚨 CRITICAL',
            'title': 'Test problem',
            'file_path': '/test/file.py'
        }]

        output = self.renderer._render_simple_tab()

        self.assertIsInstance(output, str)
        self.assertIn('PROBLEMAS DETECTADOS', output)
        self.assertIn('Test problem', output)

    def test_problems_summary(self):
        """Test resumen de problemas"""
        summary = get_problems_summary()

        # Verificar estructura
        self.assertIn('total_problems', summary)
        self.assertIn('critical_count', summary)
        self.assertIn('high_count', summary)
        self.assertIn('last_analysis', summary)


class TestDashboardPatcher(unittest.TestCase):
    """🔧 Tests del patcher de dashboard"""

    def setUp(self):
        """Configuración inicial"""
        # Crear dashboard temporal
        self.test_dir = tempfile.mkdtemp()
        self.test_dashboard = Path(self.test_dir) / "dashboard_definitivo.py"
        self.test_renderer = Path(self.test_dir) / "problems_tab_renderer.py"

        # Crear contenido básico
        self.test_dashboard.write_text("""
import streamlit as st

def main():
    st.title("Test Dashboard")

    tabs = st.tabs(["📊 Overview", "📈 Trading"])

    with tabs[0]:
        st.write("Overview content")

    with tabs[1]:
        st.write("Trading content")

if __name__ == "__main__":
    main()
""")

        self.test_renderer.write_text("def render_problems_tab_simple(): return 'Test'")

        # Crear patcher con rutas de prueba
        self.patcher = DashboardPatcher()
        self.patcher.dashboard_path = self.test_dashboard
        self.patcher.problems_renderer_path = self.test_renderer

    def tearDown(self):
        """Limpieza"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_prerequisites_validation(self):
        """Test validación de prerequisitos"""
        success, message = self.patcher._validate_prerequisites()
        self.assertTrue(success)

    def test_dashboard_structure_analysis(self):
        """Test análisis de estructura"""
        success, message = self.patcher._analyze_dashboard_structure()
        self.assertTrue(success)

    def test_import_addition(self):
        """Test adición de imports"""
        with open(self.test_dashboard, 'r') as f:
            original_content = f.read()

        modified_content = self.patcher._add_import_if_needed(original_content)

        self.assertIn('problems_tab_renderer', modified_content)

    def test_tabs_modification(self):
        """Test modificación de pestañas"""
        with open(self.test_dashboard, 'r') as f:
            original_content = f.read()

        modified_content = self.patcher._modify_tabs_section(original_content)

        self.assertIn('🚨 Problemas', modified_content)


class TestSystemIntegration(unittest.TestCase):
    """🔗 Tests de integración del sistema completo"""

    def setUp(self):
        """Configuración para tests de integración"""
        self.original_workspace = WORKSPACE_ROOT

    def test_end_to_end_detection(self):
        """Test detección end-to-end"""
        # Crear detector
        detector = ErrorDetector(str(self.original_workspace))

        # Ejecutar análisis rápido
        start_time = time.time()
        report = detector.analyze_full_system(quick_mode=True)
        end_time = time.time()

        # Validaciones básicas
        self.assertIsInstance(report, dict)
        self.assertIn('problems', report)
        self.assertLess(end_time - start_time, 60)  # Menos de 1 minuto

    def test_dashboard_integration(self):
        """Test integración con dashboard"""
        try:
            content = render_problems_tab_simple()
            self.assertIsInstance(content, str)
            self.assertGreater(len(content), 0)
        except Exception as e:
            self.fail(f"Error en integración dashboard: {str(e)}")

    def test_powershell_script_execution(self):
        """Test ejecución del script PowerShell"""
        script_path = WORKSPACE_ROOT / "scripts" / "ejecutar_deteccion_errores.ps1"

        if script_path.exists():
            # Test solo que el script existe y es legible
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Verificar contenido básico
            self.assertIn('error_detector.py', content)
            self.assertIn('dashboard', content)


class TestPerformance(unittest.TestCase):
    """⚡ Tests de rendimiento"""

    def test_detection_performance(self):
        """Test rendimiento de detección"""
        detector = ErrorDetector(str(WORKSPACE_ROOT))

        # Medir tiempo de análisis rápido
        start_time = time.time()
        detector.analyze_full_system(quick_mode=True)
        quick_time = time.time() - start_time

        # El análisis rápido debe completarse en menos de 30 segundos
        self.assertLess(quick_time, 30)

    def test_memory_usage(self):
        """Test uso de memoria"""
        import psutil

        process = psutil.Process()
        memory_before = process.memory_info().rss

        # Ejecutar análisis
        detector = ErrorDetector(str(WORKSPACE_ROOT))
        detector.analyze_full_system(quick_mode=True)

        memory_after = process.memory_info().rss
        memory_increase = memory_after - memory_before

        # El incremento de memoria debe ser razonable (< 100MB)
        self.assertLess(memory_increase, 100 * 1024 * 1024)


def run_test_suite():
    """🚀 Ejecutar suite completa de tests"""
    print("🧪 INICIANDO TESTS SISTEMA DETECCIÓN DE ERRORES")
    print("=" * 60)

    # Verificar imports
    if not IMPORTS_OK:
        print(f"❌ ERROR: No se pudieron importar módulos: {IMPORT_ERROR}")
        return False

    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Agregar tests
    test_classes = [
        TestErrorDetector,
        TestProblemsTabRenderer,
        TestDashboardPatcher,
        TestSystemIntegration,
        TestPerformance
    ]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()

    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    print(f"⏱️ Tiempo total: {end_time - start_time:.2f} segundos")
    print(f"✅ Tests exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Tests fallidos: {len(result.failures)}")
    print(f"🚨 Errores: {len(result.errors)}")

    if result.failures:
        print("\n❌ TESTS FALLIDOS:")
        for test, traceback in result.failures:
            print(f"   • {test}: {traceback.split(chr(10))[-2]}")

    if result.errors:
        print("\n🚨 ERRORES:")
        for test, traceback in result.errors:
            print(f"   • {test}: {traceback.split(chr(10))[-2]}")

    success = len(result.failures) == 0 and len(result.errors) == 0

    if success:
        print("\n🎉 TODOS LOS TESTS PASARON EXITOSAMENTE")
    else:
        print("\n⚠️ ALGUNOS TESTS FALLARON - REVISAR ERRORES")

    return success


def run_quick_smoke_test():
    """⚡ Test rápido de funcionalidad básica"""
    print("⚡ EJECUTANDO SMOKE TEST RÁPIDO")
    print("=" * 40)

    tests_passed = 0
    total_tests = 5

    # Test 1: Import del detector
    try:
        import importlib.util
        detector_spec = importlib.util.spec_from_file_location(
            "error_detector",
            WORKSPACE_ROOT / "scripts" / "error_detection" / "error_detector.py"
        )
        detector_module = importlib.util.module_from_spec(detector_spec)
        detector_spec.loader.exec_module(detector_module)
        ErrorDetector = detector_module.ErrorDetector
        print("✅ Import detector OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Import detector falló: {e}")
        ErrorDetector = None

    # Test 2: Import del renderer
    try:
        renderer_spec = importlib.util.spec_from_file_location(
            "problems_tab_renderer",
            WORKSPACE_ROOT / "dashboard" / "problems_tab_renderer.py"
        )
        renderer_module = importlib.util.module_from_spec(renderer_spec)
        renderer_spec.loader.exec_module(renderer_module)
        render_problems_tab_simple = renderer_module.render_problems_tab_simple
        print("✅ Import renderer OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Import renderer falló: {e}")
        render_problems_tab_simple = None

    # Test 3: Creación de detector
    try:
        if ErrorDetector:
            detector = ErrorDetector(str(WORKSPACE_ROOT))
            print("✅ Creación detector OK")
            tests_passed += 1
        else:
            print("❌ No se puede crear detector (import falló)")
    except Exception as e:
        print(f"❌ Creación detector falló: {e}")

    # Test 4: Renderizado simple
    try:
        if render_problems_tab_simple:
            content = render_problems_tab_simple()
            if content and len(content) > 0:
                print("✅ Renderizado simple OK")
                tests_passed += 1
            else:
                print("❌ Renderizado simple retornó contenido vacío")
        else:
            print("❌ No se puede renderizar (import falló)")
    except Exception as e:
        print(f"❌ Renderizado simple falló: {e}")

    # Test 5: Verificación de archivos
    required_files = [
        "scripts/error_detection/error_detector.py",
        "dashboard/problems_tab_renderer.py",
        "scripts/ejecutar_deteccion_errores.ps1"
    ]

    files_exist = all((WORKSPACE_ROOT / f).exists() for f in required_files)
    if files_exist:
        print("✅ Archivos requeridos OK")
        tests_passed += 1
    else:
        print("❌ Algunos archivos requeridos no existen")

    print(f"\n📊 Resultado: {tests_passed}/{total_tests} tests pasaron")

    if tests_passed == total_tests:
        print("🎉 SMOKE TEST EXITOSO - Sistema listo")
        return True
    else:
        print("⚠️ SMOKE TEST FALLÓ - Revisar instalación")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="🧪 Tests Sistema Detección Errores")
    parser.add_argument("--full", action="store_true", help="Ejecutar suite completa")
    parser.add_argument("--smoke", action="store_true", help="Ejecutar solo smoke test")
    parser.add_argument("--performance", action="store_true", help="Solo tests de rendimiento")

    args = parser.parse_args()

    if args.smoke:
        success = run_quick_smoke_test()
    elif args.performance:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestPerformance)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        success = len(result.failures) == 0 and len(result.errors) == 0
    else:
        success = run_test_suite()

    sys.exit(0 if success else 1)
