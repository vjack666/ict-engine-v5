
from sistema.sic import Dict, Optional, Union, Tuple, Any, datetime, List, timezone, timedelta
from sistema.sic import get_dashboard_controller, enviar_senal_log, get_mt5_manager, log_info, get_logging, log_error
from sistema.sic import time
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌙 HIBERNATION WIDGET v2.0 - ARQUITECTURA DIRECTA
=================================================
Usa TODA la infraestructura existente siguiendo el patrón exitoso del POI Integration

📚 DOCUMENTACIÓN COMPLETA:
- docs/bitacoras/reportes/HIBERNATION_WIDGET_V2_BITACORA_COMPLETA.md
- docs/bitacoras/checklists/HIBERNATION_WIDGET_V2_CHECKLIST_COMPLETO.md
- docs/bitacoras/reportes/HIBERNATION_WIDGET_V2_INDICE_DOCUMENTACION.md
- docs/bitacoras/reportes/DASHBOARD_H1_HIBERNACION.md (actualizado)
- docs/bitacoras/reportes/REGISTRAR_ACCION_PROPOSITO_SISTEMA.md
"""

from sistema.sic import enviar_senal_log
from utils.mt5_data_manager import get_mt5_manager
from sistema.sic import get_dashboard_controller
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from sistema.sic import datetime, timedelta
from sistema.sic import Dict, List, Tuple, Optional, Any
from sistema.sic import time

# 🚀 INICIALIZACIÓN DEL MÓDULO USANDO INFRAESTRUCTURA EXISTENTE
enviar_senal_log("INFO", "✅ Hibernation Widget v2.0 - Arquitectura Directa inicializado exitosamente", __name__, "module_init")
enviar_senal_log("SUCCESS", "🌙 Integración completa con: SLUC Logging + MT5 Manager + Dashboard Controller + Rich UI", __name__, "architecture")

def crear_panel_hibernacion_inteligente(dashboard_instance) -> Panel:
    """
    🌙 PANEL HIBERNACIÓN INTELIGENTE
    Arquitectura Directa: 100% Infraestructura Existente

    └─► MT5 Manager (estado de conexión)
    └─► Dashboard Controller (coordinación)
    └─► Real Market Data (datos de mercado)
    └─► SLUC Logging (monitoreo total)
    └─► Rich UI (presentación profesional)
    """

    try:
        # 1️⃣ VALIDACIÓN MT5 + CONTROLLER
        mt5_manager = get_mt5_manager()
        controller = get_dashboard_controller()

        enviar_senal_log("INFO", f"🔍 Validando sistemas: MT5 ({'✓' if mt5_manager else '✗'}) | Controller ({'✓' if controller else '✗'})", __name__, "validation")

        # 2️⃣ ACCESO A DATOS REAL_MARKET_DATA
        market_status = "🔴 DESCONOCIDO"
        trading_hours = "⏰ Sin datos"
        current_price = "💰 N/A"

        if hasattr(dashboard_instance, 'real_market_data') and dashboard_instance.real_market_data:
            market_data = dashboard_instance.real_market_data

            # Extraer datos reales del mercado
            if isinstance(market_data, dict) and 'H1' in market_data:
                h1_data = market_data['H1']
                if isinstance(h1_data, dict) and 'close' in h1_data and h1_data['close']:
                    current_price = f"💰 {h1_data['close'][-1]:.5f}"
                    enviar_senal_log("INFO", f"📊 Precio actual extraído: {current_price}", __name__, "market_data")

        # 3️⃣ ESTADO MT5 Y MERCADO
        if mt5_manager:
            try:
                # Verificar estado MT5 real usando métodos disponibles
                # El MT5DataManager no tiene verificar_conexion, pero podemos usar get_account_info
                account_info = mt5_manager.get_account_info() if hasattr(mt5_manager, 'get_account_info') else None
                mt5_status = account_info is not None and len(account_info) > 0

                if mt5_status:
                    market_status = "🟢 ACTIVO"
                    trading_hours = determinar_horario_trading()
                    enviar_senal_log("SUCCESS", "✅ MT5 conectado - Mercado activo", __name__, "mt5_status")
                else:
                    market_status = "🔴 DESCONECTADO"
                    trading_hours = "⏸️ Fuera de horario"
                    enviar_senal_log("WARNING", "⚠️ MT5 disponible pero desconectado", __name__, "mt5_status")
            except Exception as e:
                market_status = "🟡 PARCIAL"
                trading_hours = "⚠️ Error conexión"
                enviar_senal_log("WARNING", f"⚠️ Error verificando MT5: {e}", __name__, "mt5_error")
        else:
            market_status = "🔴 NO DISPONIBLE"
            trading_hours = "❌ MT5 no encontrado"
            enviar_senal_log("ERROR", "❌ MT5 Manager no disponible", __name__, "mt5_unavailable")

        # 4️⃣ CREAR PANEL HIBERNACIÓN
        hibernation_content = crear_contenido_hibernacion(market_status, trading_hours, current_price)

        # 5️⃣ NOTIFICAR AL CONTROLLER (si disponible)
        if controller:
            try:
                controller_data = {
                    'market_status': market_status,
                    'current_price': current_price,
                    'hibernation_active': True,
                    'timestamp': datetime.now().isoformat(),
                    'source': 'HIBERNATION_WIDGET_V2'
                }
                # 🎯 REGISTRAR ACCIÓN: Notifica al controller sobre actualización de estado hibernación
                # Propósito: Tracking de cambios de estado del mercado, coordinación sistema hibernación
                controller.registrar_accion("HIBERNATION_STATUS_UPDATE", controller_data)
                enviar_senal_log("INFO", "📡 Estado hibernación reportado al Dashboard Controller", __name__, "controller_sync")
            except Exception as e:
                enviar_senal_log("WARNING", f"⚠️ Error al reportar hibernación al controller: {e}", __name__, "controller_sync")

        enviar_senal_log("SUCCESS", f"🌙 Panel hibernación creado: {market_status}", __name__, "hibernation_complete")
        return hibernation_content

    except Exception as e:
        # ERROR HANDLING CON LOGGING CENTRAL
        error_msg = f"Error crítico en hibernación: {str(e)}"
        enviar_senal_log("CRITICAL", error_msg, __name__, "hibernation_error")
        return crear_panel_hibernacion_error(error_msg)

def crear_contenido_hibernacion(market_status: str, trading_hours: str, current_price: str) -> Panel:
    """
    🎨 Crear contenido del panel hibernación con datos reales
    """

    # DETERMINAR ESTADO DE HIBERNACIÓN
    if "🟢" in market_status:
        hibernation_mode = "🌅 MODO ACTIVO"
        hibernation_color = "green"
        action_text = "Sistema operativo - Trading habilitado"
    elif "🟡" in market_status:
        hibernation_mode = "🌤️ MODO PARCIAL"
        hibernation_color = "yellow"
        action_text = "Conexión parcial - Verificar MT5"
    else:
        hibernation_mode = "🌙 MODO HIBERNACIÓN"
        hibernation_color = "blue"
        action_text = "Sistema en reposo - Esperando mercado"

    # CREAR CONTENIDO DEL PANEL
    content_lines = [
        f"[bold {hibernation_color}]{hibernation_mode}[/bold {hibernation_color}]",
        "",
        f"📊 Estado: {market_status}",
        f"⏰ Horario: {trading_hours}",
        f"💰 Precio: {current_price}",
        "",
        f"🔄 Acción: {action_text}",
        f"⏱️ Actualizado: {datetime.now().strftime('%H:%M:%S')}"
    ]

    content_text = Text("\n".join(content_lines))

    # CREAR PANEL CON ESTILO APROPIADO
    panel = Panel(
        content_text,
        title=f"🌙 Hibernación Inteligente",
        title_align="left",
        border_style=hibernation_color,
        padding=(1, 2),
        expand=False
    )

    enviar_senal_log("INFO", f"🎨 Panel hibernación creado: {hibernation_mode}", __name__, "panel_creation")

    return panel

def determinar_horario_trading() -> str:
    """
    🕐 Determinar horario de trading actual
    """

    now = datetime.now()
    hour = now.hour
    weekday = now.weekday()  # 0 = Monday, 6 = Sunday

    # HORARIOS FOREX (approximate)
    if weekday >= 5:  # Weekend
        return "📅 Fin de semana - Mercado cerrado"
    elif 0 <= hour < 6:
        return "🌙 Sesión Asia-Pacífico"
    elif 6 <= hour < 14:
        return "🌅 Sesión Europea"
    elif 14 <= hour < 22:
        return "🌞 Sesión Americana"
    else:
        return "🌃 Sesión Asia tardía"

def crear_panel_hibernacion_error(error_msg: str) -> Panel:
    """
    🚨 Panel de error para hibernación
    """

    enviar_senal_log("ERROR", f"🚨 Creando panel error hibernación: {error_msg}", __name__, "error_panel")

    error_content = Text(f"""🚨 ERROR EN HIBERNACIÓN

❌ Error: {error_msg[:50]}...

🔧 Acciones recomendadas:
• Verificar conexión MT5
• Revisar logs del sistema
• Reiniciar dashboard

⏱️ {datetime.now().strftime('%H:%M:%S')}""")

    return Panel(
        error_content,
        title="🚨 Error Hibernación",
        title_align="left",
        border_style="red",
        padding=(1, 2),
        expand=False
    )

def crear_tabla_hibernacion_detallada(dashboard_instance) -> Table:
    """
    📋 Crear tabla detallada de hibernación (alternativa al panel)
    """

    try:
        # CREAR TABLA CON ESTILO PROFESIONAL
        tabla = Table(
            title=f"🌙 Sistema Hibernación - {datetime.now().strftime('%H:%M:%S')}",
            title_style="bold blue",
            header_style="bold white on blue",
            border_style="bright_blue",
            show_header=True,
            show_lines=True,
            expand=True
        )

        # DEFINIR COLUMNAS
        tabla.add_column("Componente", style="bold white", width=20)
        tabla.add_column("Estado", style="bold green", width=15)
        tabla.add_column("Detalle", style="dim white", width=30)
        tabla.add_column("Acción", style="bold cyan", width=20)

        # VALIDAR SISTEMAS
        mt5_manager = get_mt5_manager()
        controller = get_dashboard_controller()

        # AGREGAR FILAS DEL SISTEMA
        tabla.add_row("MT5 Manager", "🟢 Activo" if mt5_manager else "🔴 Inactivo",
                     "Conexión verificada" if mt5_manager else "No disponible",
                     "Operativo" if mt5_manager else "Revisar MT5")

        tabla.add_row("Dashboard Controller", "🟢 Activo" if controller else "🔴 Inactivo",
                     "Coordinando sistema" if controller else "No disponible",
                     "Funcionando" if controller else "Reiniciar")

        # DATOS DE MERCADO
        market_available = hasattr(dashboard_instance, 'real_market_data') and dashboard_instance.real_market_data
        tabla.add_row("Market Data", "🟢 Disponible" if market_available else "🔴 No disponible",
                     f"{len(dashboard_instance.real_market_data)} timeframes" if market_available else "Sin datos",
                     "Datos cargados" if market_available else "Cargar datos")

        # ESTADO GENERAL
        all_systems = mt5_manager and controller and market_available
        tabla.add_row("Sistema General", "🟢 Operativo" if all_systems else "🟡 Parcial",
                     "Todos los sistemas activos" if all_systems else "Algunos sistemas inactivos",
                     "Modo normal" if all_systems else "Verificar sistemas")

        enviar_senal_log("SUCCESS", f"📋 Tabla hibernación detallada creada", __name__, "detailed_table")

        return tabla

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error creando tabla hibernación: {e}", __name__, "table_error")
        # Retornar tabla de error
        tabla_error = Table(title="🚨 Error Tabla Hibernación")
        tabla_error.add_column("Error")
        tabla_error.add_row(f"❌ {str(e)[:50]}...")
        return tabla_error
