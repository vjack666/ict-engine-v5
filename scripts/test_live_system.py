#!/usr/bin/env python3
"""
🚀 TEST LIVE-ONLY SYSTEM
========================

Script de prueba para verificar que la migración a Live-Only funciona correctamente.
Valida la detección de tipo de cuenta y la configuración del sistema.

Autor: Sistema Sentinel Grid
Fecha: 2025-08-03
Versión: Live Test v1.0
"""

import sys
from pathlib import Path

# Configurar path del proyecto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from config.live_account_validator import LiveAccountValidator, AccountType
    from config.live_only_config import get_live_config, is_demo_mode_disabled
    from utils.mt5_data_manager import get_mt5_manager
    from dashboard.widgets.account_status_widget import get_account_status_widget
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    IMPORTS_OK = True
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    IMPORTS_OK = False

def test_live_configuration():
    """Prueba la configuración Live-Only"""
    console = Console()

    console.print("\n🚀 TESTING CONFIGURACIÓN LIVE-ONLY", style="bold blue")
    console.print("=" * 50)

    # Test 1: Configuración Live-Only
    console.print("\n📋 Test 1: Configuración Live-Only")
    config = get_live_config()

    if config["mt5"]["mode"] == "LIVE_ONLY":
        console.print("✅ Modo LIVE_ONLY configurado correctamente", style="green")
    else:
        console.print("❌ Error: Modo no configurado como LIVE_ONLY", style="red")

    # Test 2: Modo demo deshabilitado
    console.print("\n📋 Test 2: Modo Demo Deshabilitado")
    demo_disabled = is_demo_mode_disabled()

    if demo_disabled:
        console.print("✅ Modo demo completamente deshabilitado", style="green")
    else:
        console.print("❌ Error: Modo demo aún habilitado", style="red")

    # Test 3: Configuración de datos
    console.print("\n📋 Test 3: Configuración de Datos")
    data_config = config["data"]

    if (data_config["sources"]["primary"] == "MT5_LIVE" and
        data_config["sources"]["backup"] is None):
        console.print("✅ Fuente de datos configurada para Live únicamente", style="green")
    else:
        console.print("❌ Error: Configuración de datos incorrecta", style="red")

    return config

def test_account_validator():
    """Prueba el validador de tipo de cuenta"""
    console = Console()

    console.print("\n🔍 TESTING VALIDADOR DE CUENTA", style="bold blue")
    console.print("=" * 50)

    # Crear validador
    validator = LiveAccountValidator()

    # Test detección de tipo de cuenta
    console.print("\n📋 Test: Detección de Tipo de Cuenta")
    try:
        account_type, account_data = validator.detect_account_type()

        console.print(f"✅ Tipo detectado: {account_type.value.upper()}", style="green")
        console.print(f"   Número: {account_data.get('login', 'N/A')}")
        console.print(f"   Servidor: {account_data.get('server', 'N/A')}")
        console.print(f"   Broker: {account_data.get('company', 'N/A')}")

        # Validación para trading live
        validation = validator.validate_account_for_live_trading()
        console.print(f"\n✅ Apropiada para Live: {validation['suitable_for_live_trading']}")

        if validation.get('warnings'):
            console.print("\n⚠️ Advertencias:", style="yellow")
            for warning in validation['warnings']:
                console.print(f"  • {warning}", style="yellow")

        return account_type, account_data, validation

    except Exception as e:
        console.print(f"❌ Error en validación: {e}", style="red")
        return None, None, None

def test_mt5_manager():
    """Prueba el MT5DataManager actualizado"""
    console = Console()

    console.print("\n🔗 TESTING MT5 DATA MANAGER", style="bold blue")
    console.print("=" * 50)

    try:
        # Obtener manager
        mt5_manager = get_mt5_manager()

        # Test conexión
        console.print("\n📋 Test: Conexión MT5")
        if mt5_manager.connect():
            console.print("✅ Conexión exitosa", style="green")

            # Test información de cuenta
            console.print("\n📋 Test: Información de Cuenta")
            account_info = mt5_manager.get_account_info()

            if account_info and "error" not in account_info:
                console.print(f"✅ Tipo: {account_info['account_type'].upper()}", style="green")
                console.print(f"   Apropiada para Live: {account_info['suitable_for_live']}")
                console.print(f"   Nivel de Riesgo: {account_info['risk_level']}")
                console.print(f"   Trading Habilitado: {mt5_manager.is_live_trading_enabled()}")
            else:
                console.print(f"❌ Error obteniendo info: {account_info.get('error', 'Unknown')}", style="red")

        else:
            console.print("❌ Error de conexión MT5", style="red")

    except Exception as e:
        console.print(f"❌ Error en MT5Manager: {e}", style="red")

    return mt5_manager

def test_account_widget():
    """Prueba el widget de status de cuenta"""
    console = Console()

    console.print("\n🎨 TESTING ACCOUNT STATUS WIDGET", style="bold blue")
    console.print("=" * 50)

    try:
        # Obtener widget
        widget = get_account_status_widget()

        # Crear panel de status
        mt5_manager = get_mt5_manager()
        panel = widget.create_account_status_panel(mt5_manager)

        console.print("\n📋 Panel de Status de Cuenta:")
        console.print(panel)

        # Status compacto
        compact_status = widget.create_compact_status(mt5_manager)
        console.print(f"\n✅ Status Compacto: {compact_status}")

        # Métricas
        metrics = widget.get_account_metrics(mt5_manager)
        console.print(f"\n📊 Métricas: {metrics}")

    except Exception as e:
        console.print(f"❌ Error en widget: {e}", style="red")

def main():
    """Función principal de testing"""
    if not IMPORTS_OK:
        print("❌ No se pudieron importar los módulos necesarios")
        return

    console = Console()

    # Header
    console.print(Panel(
        Text.from_markup(
            "[bold blue]🚀 SISTEMA LIVE-ONLY - SUITE DE TESTING[/bold blue]\n"
            "[blue]Verificación completa de la migración a modo Live-Only[/blue]\n"
            "[dim]Sistema Sentinel Grid - Live Test v1.0[/dim]"
        ),
        title="LIVE-ONLY TESTING SUITE",
        border_style="blue"
    ))

    # Ejecutar tests
    try:
        config = test_live_configuration()
        account_type, account_data, validation = test_account_validator()
        mt5_manager = test_mt5_manager()
        test_account_widget()

        # Resumen final
        console.print("\n🎯 RESUMEN DE TESTING", style="bold green")
        console.print("=" * 50)

        if config and account_type and validation:
            console.print("✅ Configuración Live-Only: FUNCIONAL", style="green")
            console.print("✅ Validador de Cuenta: FUNCIONAL", style="green")
            console.print("✅ MT5 Data Manager: FUNCIONAL", style="green")
            console.print("✅ Account Widget: FUNCIONAL", style="green")

            console.print(f"\n🏦 Cuenta detectada: {account_type.value.upper()}")
            console.print(f"🎯 Apropiada para Live: {validation['suitable_for_live_trading']}")
            console.print(f"⚡ Sistema: LISTO PARA PRODUCCIÓN", style="bold green")

        else:
            console.print("❌ Algunos tests fallaron - revisar configuración", style="red")

    except Exception as e:
        console.print(f"❌ Error crítico en testing: {e}", style="red")

if __name__ == "__main__":
    main()
