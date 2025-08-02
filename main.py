#!/usr/bin/env python3
"""
🚀 ICT ENGINE v5.0 - MAIN LAUNCHER
==================================

Script principal para lanzar el sistema ICT Engine con todas sus funcionalidades.
Proporciona una interfaz unificada para acceder a todas las herramientas del sistema.

Uso:
    python main.py                    # Launcher principal
    python main.py --debug          # Modo debug
    python main.py --console        # Modo console
    python main.py --dashboard      # Dashboard directo
    python main.py --utilities      # Herramientas de utilidad
"""

import sys
import os
import argparse
from pathlib import Path

# 📁 Configurar paths del proyecto
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def main():
    """Función principal del launcher"""
    parser = argparse.ArgumentParser(
        description="ICT Engine v5.0 - Sistema de Trading Profesional",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py                    # Launcher interactivo
  python main.py --dashboard        # Dashboard directo
  python main.py --debug           # Herramientas de debug
  python main.py --utilities       # Utilidades de desarrollo
  python main.py --tests           # Ejecutar tests
        """
    )

    # 🎯 Opciones principales
    parser.add_argument("--dashboard", action="store_true",
                       help="Lanzar dashboard principal")
    parser.add_argument("--debug", action="store_true",
                       help="Lanzar herramientas de debug")
    parser.add_argument("--console", action="store_true",
                       help="Modo console para desarrollo")
    parser.add_argument("--utilities", action="store_true",
                       help="Mostrar utilidades disponibles")
    parser.add_argument("--tests", action="store_true",
                       help="Ejecutar suite de tests")

    # 🔧 Opciones de configuración
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Output verbose")
    parser.add_argument("--config", type=str, default="main",
                       help="Configuración a usar (main, user, temp)")

    args = parser.parse_args()

    # 🎯 Ejecutar según parámetros
    try:
        if args.dashboard:
            launch_dashboard(args)
        elif args.debug:
            launch_debug_tools(args)
        elif args.utilities:
            show_utilities_menu(args)
        elif args.tests:
            run_tests(args)
        else:
            launch_interactive_menu(args)

    except KeyboardInterrupt:
        print("\n❌ Operación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def launch_dashboard(args):
    """Lanza el dashboard principal"""
    print("🚀 Lanzando Dashboard Principal...")

    try:
        from dashboard.dashboard_definitivo import SentinelDashboardDefinitivo

        # 🔧 Configurar ambiente
        if args.console:
            os.environ['TEXTUAL_CONSOLE'] = '1'
        if args.verbose:
            os.environ['TEXTUAL_DEBUG'] = '1'

        app = SentinelDashboardDefinitivo()
        app.run()

    except ImportError as e:
        print(f"❌ Error importando dashboard: {e}")
        print("🔧 Asegúrate de que todos los módulos estén instalados")
        sys.exit(1)

def launch_debug_tools(args):
    """Lanza las herramientas de debug"""
    print("🔧 Lanzando Debug Tools...")

    try:
        from utilities.debug.debug_launcher import DebugLauncher

        # 🔧 Configurar modo debug
        os.environ['TEXTUAL_DEBUG'] = '1'
        if args.verbose:
            os.environ['TEXTUAL_LOG'] = '1'

        app = DebugLauncher()
        app.run()

    except ImportError as e:
        print(f"❌ Error importando debug tools: {e}")
        print("🔧 Verifica que las utilidades estén en utilities/debug/")
        sys.exit(1)

def show_utilities_menu(args):
    """Muestra el menú de utilidades"""
    print("🛠️ UTILIDADES DISPONIBLES:")
    print("=" * 50)

    utilities = [
        ("1", "🔧 Debug Launcher", "python utilities/debug/debug_launcher.py"),
        ("2", "📝 Print Migration Tool", "python utilities/migration/print_migration_tool.py --scan-only"),
        ("3", "📊 Sprint Consolidator", "python utilities/sprint/sprint_1_1_consolidator.py"),
        ("4", "🧪 Run Tests", "python -m pytest tests/"),
        ("5", "📋 System Info", "python scripts/system_info.py"),
    ]

    for num, name, command in utilities:
        print(f"  {num}. {name}")
        if args.verbose:
            print(f"     💻 {command}")

    print("\n🎯 Para ejecutar una utilidad:")
    print("  python main.py --utilities")
    print("  Luego ingresa el número de la opción")

    # 🎮 Menú interactivo
    try:
        choice = input("\n📋 Selecciona una opción (1-5) o 'q' para salir: ").strip()

        if choice.lower() == 'q':
            return

        if choice in ['1', '2', '3', '4', '5']:
            command = utilities[int(choice)-1][2]
            print(f"\n🚀 Ejecutando: {command}")
            os.system(command)
        else:
            print("❌ Opción inválida")

    except (KeyboardInterrupt, EOFError):
        print("\n👋 ¡Hasta luego!")

def run_tests(args):
    """Ejecuta la suite de tests"""
    print("🧪 Ejecutando Tests...")

    # 🔍 Verificar que pytest esté disponible
    try:
        import pytest
    except ImportError:
        print("❌ pytest no está instalado")
        print("💡 Instala con: pip install pytest")
        sys.exit(1)

    # 🚀 Ejecutar tests
    test_args = ["tests/"]

    if args.verbose:
        test_args.extend(["-v", "--tb=short"])
    else:
        test_args.extend(["-q"])

    # 📊 Ejecutar con pytest
    exit_code = pytest.main(test_args)

    if exit_code == 0:
        print("✅ Todos los tests pasaron")
        print("📋 Reporte detallado disponible en: docs/bitacoras/REPORTE_TEST_SUITE_COMPLETO.md")
    else:
        print("❌ Algunos tests fallaron")
        print("📋 Revisa el reporte detallado en: docs/bitacoras/REPORTE_TEST_SUITE_COMPLETO.md")
        sys.exit(exit_code)

def launch_interactive_menu(args):
    """Lanza el menú interactivo principal"""
    print("🎯 ICT ENGINE v5.0 - LAUNCHER PRINCIPAL")
    print("=" * 50)

    options = [
        ("1", "🚀 Dashboard Principal", "Lanzar dashboard de trading"),
        ("2", "🔧 Debug Tools", "Herramientas de debugging"),
        ("3", "🛠️ Utilidades", "Ver utilidades disponibles"),
        ("4", "🧪 Tests", "Ejecutar suite de tests"),
        ("5", "📊 Estado del Sistema", "Ver información del sistema"),
        ("6", "📋 Documentación", "Ver documentación disponible"),
    ]

    while True:
        print("\n📋 OPCIONES DISPONIBLES:")
        for num, name, desc in options:
            print(f"  {num}. {name} - {desc}")

        print("\n❌ q. Salir")

        try:
            choice = input("\n🎯 Selecciona una opción: ").strip().lower()

            if choice == 'q':
                print("👋 ¡Hasta luego!")
                break
            elif choice == '1':
                launch_dashboard(args)
            elif choice == '2':
                launch_debug_tools(args)
            elif choice == '3':
                show_utilities_menu(args)
            elif choice == '4':
                run_tests(args)
            elif choice == '5':
                show_system_status()
            elif choice == '6':
                show_documentation()
            else:
                print("❌ Opción inválida. Intenta de nuevo.")

        except (KeyboardInterrupt, EOFError):
            print("\n👋 ¡Hasta luego!")
            break

def show_system_status():
    """Muestra el estado del sistema"""
    print("\n📊 ESTADO DEL SISTEMA:")
    print("-" * 30)

    # 🐍 Información de Python
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Directorio: {os.getcwd()}")

    # 📦 Verificar módulos principales
    modules_to_check = [
        ('dashboard.dashboard_definitivo', 'Dashboard Principal'),
        ('core.ict_engine', 'ICT Engine'),
        ('sistema.logging_interface', 'Sistema de Logging'),
        ('config.config_manager', 'Gestor de Configuración'),
        ('utilities.debug', 'Debug Tools'),
    ]

    print(f"\n📦 MÓDULOS:")
    for module_name, display_name in modules_to_check:
        try:
            __import__(module_name)
            print(f"  ✅ {display_name}")
        except ImportError:
            print(f"  ❌ {display_name}")

    # 📁 Verificar estructura de directorios
    required_dirs = [
        'dashboard', 'core', 'sistema', 'config',
        'utilities', 'tests', 'data', 'docs'
    ]

    print(f"\n📁 ESTRUCTURA:")
    for dir_name in required_dirs:
        if (PROJECT_ROOT / dir_name).exists():
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/")

def show_documentation():
    """Muestra la documentación disponible"""
    print("\n📚 DOCUMENTACIÓN DISPONIBLE:")
    print("-" * 40)

    docs = [
        ("📋 PLAN_TRABAJO_COMPLETO_ICT.md", "Plan completo del proyecto"),
        ("🔧 BITACORA_CONFIGURACION_VSCODE.md", "Configuración de VS Code"),
        ("📊 BITACORA_DIAGNOSTICO_DASHBOARD.md", "Diagnóstico del dashboard"),
        ("📈 BITACORA_SEGUIMIENTO_ICT.md", "Seguimiento del progreso"),
        ("🛠️ CONFIGURACION_VSCODE_MENOS_ESTRICTO.md", "Config VS Code simplificada"),
        ("📖 docs/README.md", "Documentación general"),
    ]

    for doc_file, description in docs:
        doc_path = PROJECT_ROOT / doc_file.split(" ", 1)[1]
        if doc_path.exists():
            print(f"  ✅ {doc_file} - {description}")
        else:
            print(f"  ❌ {doc_file} - {description}")

if __name__ == "__main__":
    main()
