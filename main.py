from sistema.logging_interface import enviar_senal_log
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
    # 🚀 AUTO-INICIALIZACIÓN INTELIGENTE DE DATOS AL ARRANQUE
    enviar_senal_log("INFO", "🚀 === ICT ENGINE v5.0 INICIANDO ===", "main", "startup")

    # Usar sistema inteligente de auto-descarga existente
    try:
        from utils.mt5_data_manager import auto_download_essential_data

        enviar_senal_log("INFO", "🔍 Iniciando auto-descarga inteligente de datos...", "main", "startup")

        # El sistema ya verifica automáticamente qué datos necesita actualizar
        # Solo descarga lo que falta o está obsoleto (>6 horas)
        success = auto_download_essential_data(
            symbols=["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD"],
            timeframes=["H4", "H1", "M15", "M5", "M1"],  # Orden de prioridad ICT
            lookback=30000  # 30k velas como solicitado
        )

        if success:
            enviar_senal_log("INFO", "✅ Auto-descarga inteligente completada", "main", "startup")
        else:
            enviar_senal_log("WARNING", "⚠️ Auto-descarga completada con algunos errores", "main", "startup")

    except Exception as e:
        enviar_senal_log("WARNING", f"⚠️ Error en auto-descarga inteligente: {e}", "main", "startup")
        enviar_senal_log("INFO", "🔄 Continuando sin auto-descarga...", "main", "startup")

    parser = argparse.ArgumentParser(
        description="ICT Engine v5.0 - Sistema de Trading Profesional",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py                    # Launcher interactivo
  python main.py --dashboard        # Dashboard directo
  python main.py --debug           # Herramientas de debug
  python main.py --utilities       # Utilidades de desarrollo
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

    # 🔧 Opciones de configuración
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Output verbose")
    parser.add_argument("--config", type=str, default="main",
                       help="Configuración a usar (main, user, temp)")

    args = parser.parse_args()

    # 🎯 Ejecutar según parámetros - MODO AUTOMÁTICO
    try:
        if args.dashboard:
            launch_dashboard(args)
        elif args.debug:
            launch_debug_tools(args)
        elif args.utilities:
            show_utilities_menu(args)
        else:
            # 🚀 MODO AUTOMÁTICO: Lanzar dashboard directamente
            enviar_senal_log("INFO", "🤖 MODO AUTOMÁTICO: Lanzando Dashboard Principal...", "main", "auto")
            launch_dashboard(args)

    except KeyboardInterrupt:
        enviar_senal_log("INFO", "\n❌ Operación cancelada por el usuario", "main", "migration")
        sys.exit(0)
    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error inesperado: {e}", "main", "migration")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def launch_dashboard(args):
    """Lanza el dashboard principal"""
    enviar_senal_log("INFO", "🚀 Lanzando Dashboard Principal...", "main", "migration")

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
        enviar_senal_log("ERROR", f"❌ Error importando dashboard: {e}", "main", "migration")
        enviar_senal_log("INFO", "🔧 Asegúrate de que todos los módulos estén instalados", "main", "migration")
        sys.exit(1)

def launch_debug_tools(args):
    """Lanza las herramientas de debug"""
    enviar_senal_log("DEBUG", "🔧 Lanzando Debug Tools...", "main", "migration")

    try:
        from utilities.debug.debug_launcher import DebugLauncher

        # 🔧 Configurar modo debug
        os.environ['TEXTUAL_DEBUG'] = '1'
        if args.verbose:
            os.environ['TEXTUAL_LOG'] = '1'

        app = DebugLauncher()
        # Usar launch_debug por defecto para debug tools
        app.launch_debug()


    except ImportError as e:
        enviar_senal_log("ERROR", f"❌ Error importando debug tools: {e}", "main", "migration")
        enviar_senal_log("DEBUG", "🔧 Verifica que las utilidades estén en utilities/debug/", "main", "migration")
        sys.exit(1)

def show_utilities_menu(args):
    """Muestra el menú de utilidades"""
    enviar_senal_log("INFO", "🛠️ UTILIDADES DISPONIBLES:", "main", "migration")
    enviar_senal_log("INFO", "=" * 50, "main", "migration")

    utilities = [
        ("1", "🔧 Debug Launcher", "python utilities/debug/debug_launcher.py"),
        ("2", "📝 Print Migration Tool", "python utilities/migration/print_migration_tool.py --scan-only"),
        ("3", "📊 Sprint Consolidator", "python utilities/sprint/sprint_1_1_consolidator.py"),
        ("5", "📋 System Info", "python scripts/system_info.py"),
    ]

    for num, name, command in utilities:
        enviar_senal_log("INFO", f"  {num}. {name}", "main", "migration")
        if args.verbose:
            enviar_senal_log("INFO", f"     💻 {command}", "main", "migration")

    enviar_senal_log("INFO", "\n🎯 Para ejecutar una utilidad:", "main", "migration")
    enviar_senal_log("INFO", "  python main.py --utilities", "main", "migration")
    enviar_senal_log("INFO", "  Luego ingresa el número de la opción", "main", "migration")

    # 🎮 Menú interactivo
    try:
        choice = input("\n📋 Selecciona una opción (1-5) o 'q' para salir: ").strip()

        if choice.lower() == 'q':
            return

        if choice in ['1', '2', '3', '4', '5']:
            command = utilities[int(choice)-1][2]
            enviar_senal_log("INFO", f"\n🚀 Ejecutando: {command}", "main", "migration")
            os.system(command)
        else:
            enviar_senal_log("INFO", "❌ Opción inválida", "main", "migration")

    except (KeyboardInterrupt, EOFError):
        enviar_senal_log("INFO", "\n👋 ¡Hasta luego!", "main", "migration")

def launch_interactive_menu(args):
    """Lanza el menú interactivo principal"""
    enviar_senal_log("INFO", "🎯 ICT ENGINE v5.0 - LAUNCHER PRINCIPAL", "main", "migration")
    enviar_senal_log("INFO", "=" * 50, "main", "migration")

    options = [
        ("1", "🚀 Dashboard Principal", "Lanzar dashboard de trading"),
        ("2", "🔧 Debug Tools", "Herramientas de debugging"),
        ("3", "🛠️ Utilidades", "Ver utilidades disponibles"),
        ("4", "📊 Estado del Sistema", "Ver información del sistema"),
        ("5", "📋 Documentación", "Ver documentación disponible"),
    ]

    while True:
        enviar_senal_log("INFO", "\n📋 OPCIONES DISPONIBLES:", "main", "migration")
        for num, name, desc in options:
            enviar_senal_log("INFO", f"  {num}. {name} - {desc}", "main", "migration")

        enviar_senal_log("INFO", "\n❌ q. Salir", "main", "migration")

        try:
            choice = input("\n🎯 Selecciona una opción: ").strip().lower()

            if choice == 'q':
                enviar_senal_log("INFO", "👋 ¡Hasta luego!", "main", "migration")
                break
            elif choice == '1':
                launch_dashboard(args)
            elif choice == '2':
                launch_debug_tools(args)
            elif choice == '3':
                show_utilities_menu(args)
            elif choice == '4':
                show_system_status()
            elif choice == '5':
                show_documentation()
            else:
                enviar_senal_log("INFO", "❌ Opción inválida. Intenta de nuevo.", "main", "migration")

        except (KeyboardInterrupt, EOFError):
            enviar_senal_log("INFO", "\n👋 ¡Hasta luego!", "main", "migration")
            break

def show_system_status():
    """Muestra el estado del sistema"""
    enviar_senal_log("INFO", "\n📊 ESTADO DEL SISTEMA:", "main", "migration")
    enviar_senal_log("INFO", "-" * 30, "main", "migration")

    # 🐍 Información de Python
    enviar_senal_log("INFO", f"🐍 Python: {sys.version}", "main", "migration")
    enviar_senal_log("INFO", f"📁 Directorio: {os.getcwd()}", "main", "migration")

    # 📦 Verificar módulos principales
    modules_to_check = [
        ('dashboard.dashboard_definitivo', 'Dashboard Principal'),
        ('core.ict_engine', 'ICT Engine'),
        ('sistema.logging_interface', 'Sistema de Logging'),
        ('config.config_manager', 'Gestor de Configuración'),
        ('utilities.debug', 'Debug Tools'),
    ]

    enviar_senal_log("INFO", f"\n📦 MÓDULOS:", "main", "migration")
    for module_name, display_name in modules_to_check:
        try:
            __import__(module_name)
            enviar_senal_log("INFO", f"  ✅ {display_name}", "main", "migration")
        except ImportError:
            enviar_senal_log("INFO", f"  ❌ {display_name}", "main", "migration")

    # 📁 Verificar estructura de directorios
    required_dirs = [
        'dashboard', 'core', 'sistema', 'config',
        'utilities', 'teste', 'data', 'docs'
    ]

    enviar_senal_log("INFO", f"\n📁 ESTRUCTURA:", "main", "migration")
    for dir_name in required_dirs:
        if (PROJECT_ROOT / dir_name).exists():
            enviar_senal_log("INFO", f"  ✅ {dir_name}/", "main", "migration")
        else:
            enviar_senal_log("INFO", f"  ❌ {dir_name}/", "main", "migration")

def show_documentation():
    """Muestra la documentación disponible"""
    enviar_senal_log("INFO", "\n📚 DOCUMENTACIÓN DISPONIBLE:", "main", "migration")
    enviar_senal_log("INFO", "-" * 40, "main", "migration")

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
            enviar_senal_log("INFO", f"  ✅ {doc_file} - {description}", "main", "migration")
        else:
            enviar_senal_log("INFO", f"  ❌ {doc_file} - {description}", "main", "migration")

if __name__ == "__main__":
    main()
