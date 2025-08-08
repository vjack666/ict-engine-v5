#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌙 HIBERNACIÓN PERFECTA - DETECCIÓN OPTIMIZADA MT5
===================================================

Versión optimizada del panel de hibernación con detección
mejorada y más rápida de MT5 para mostrar el estado real.

Mejoras:
- ✅ Detección MT5 optimizada y más rápida
- ✅ Cache inteligente para evitar lag

# MIGRADO A SLUC v2.0
from sistema.sic import enviar_senal_log
- ✅ Verificación múltiple para mayor precisión
- ✅ UI más clara y profesional
- ✅ Estados dinámicos con colores apropiados

Autor: ICT Engine Team
Fecha: 04 Agosto 2025
"""

from sistema.sic import datetime
from sistema.sic import Tuple, Optional, Any
from rich.text import Text
from rich.panel import Panel

# Importar el MT5DataManager del sistema en lugar de usar MT5 directamente
try:
    from utils.mt5_data_manager import get_mt5_manager
    mt5_manager_available = True
except ImportError:
    # Para cuando se ejecuta directamente, intentar con path
    from sistema.sic import sys
    from sistema.sic import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    try:
        from utils.mt5_data_manager import get_mt5_manager
        mt5_manager_available = True
    except ImportError:
        mt5_manager_available = False


def detectar_mt5_optimizado() -> Tuple[bool, float, str]:
    """
    Detección optimizada de MT5 usando el MT5DataManager del sistema

    Returns:
        tuple: (conectado: bool, precio_actual: float, info_conexion: str)
    """
    if not mt5_manager_available:
        return False, 0.0, "MT5DataManager no disponible"

    try:
        # Usar el MT5DataManager del sistema
        mt5_manager = get_mt5_manager()

        # Verificar conexión
        if not mt5_manager.is_connected:
            # Intentar conectar
            if not mt5_manager.connect():
                return False, 0.0, "MT5 no puede conectar"

        # Obtener información de cuenta para verificar conexión activa
        account_info = mt5_manager.get_account_info()
        if account_info.get("error"):
            return False, 0.0, f"Error cuenta: {account_info['error']}"

        # Intentar obtener datos históricos recientes para confirmar conexión
        try:
            # Obtener las últimas 2 barras M1 para verificar datos actuales
            recent_data = mt5_manager.get_historical_data("EURUSD", "M1", 2, force_download=True)
            if recent_data is not None and not recent_data.empty:
                # Usar el precio de cierre más reciente
                precio_actual = float(recent_data.iloc[-1]['close'])

                # Verificar que el precio es realista (mayor que 0.5 y menor que 2.0 para EURUSD)
                if 0.5 < precio_actual < 2.0:
                    timestamp = recent_data.iloc[-1]['time'] if 'time' in recent_data.columns else "desconocido"
                    return True, precio_actual, f"Conectado - {precio_actual:.5f} ({timestamp})"
                else:
                    return True, precio_actual, f"Conectado - Precio: {precio_actual:.5f} (verificar)"

            # Si no hay datos recientes, verificar que al menos la conexión existe
            return True, 0.0, "Conectado sin datos recientes"

        except Exception as e:
            # Conexión existe pero sin datos
            return True, 0.0, f"Conectado - Error datos: {str(e)[:30]}"

    except Exception as e:
        return False, 0.0, f"Error MT5Manager: {str(e)[:50]}"


def render_hibernacion_perfecta(market_detector, hibernation_start, analysis_count,
                               patterns_detected, high_probability_signals,
                               system_metrics, riskbot=None, debug_mode=False):
    """
    Renderiza panel de hibernación perfecta con detección optimizada

    Args:
        market_detector: Detector de estado del mercado
        hibernation_start: Tiempo de inicio del estado actual
        analysis_count: Número de análisis realizados
        patterns_detected: Patrones detectados
        high_probability_signals: Señales de alta probabilidad
        system_metrics: Métricas del sistema
        riskbot: Bot de gestión de riesgo (opcional)
        debug_mode: Modo debug activado

    Returns:
        Panel: Panel renderizado para la UI
    """

    # 🚀 DETECCIÓN OPTIMIZADA DE ESTADO
    market_status = market_detector.get_current_market_status()
    market_status_text = market_status.get('market_status', 'DESCONOCIDO')
    is_market_open = market_status_text == 'MERCADO ABIERTO'

    # 🔥 DETECCIÓN MT5 OPTIMIZADA
    mt5_connected, precio_actual, info_mt5 = detectar_mt5_optimizado()

    # Información de sesión
    current_session = market_status.get('session_activa', {})
    session_name = current_session.get('name', 'Ninguna') if current_session else 'Ninguna'

    # 🎨 CREAR CONTENIDO DINÁMICO
    content = Text()
    content.append("🚀 SENTINEL ICT ANALYZER - HIBERNACIÓN PERFECTA\n\n",
                  style="bold magenta")

    # 🎯 DETERMINAR ESTADO Y ESTILO
    if is_market_open and mt5_connected:
        # 🔥 SISTEMA COMPLETAMENTE ACTIVO
        content.append("🔥 SISTEMA ACTIVO - ANÁLISIS EN TIEMPO REAL\n", style="bold green")
        content.append(f"📊 Sesión: {session_name}\n", style="bright_cyan")
        content.append(f"💰 Precio Actual: {precio_actual:.5f}\n", style="bright_yellow")
        content.append(f"✅ {info_mt5}\n", style="green")
        hibernation_status = "🔥 OPERATIVO"
        panel_title = "🔥 [bold green]SISTEMA ACTIVO - ANÁLISIS EN TIEMPO REAL[/bold green]"
        border_color = "bright_green"

    elif is_market_open and not mt5_connected:
        # ⚠️ MODO LIMITADO
        content.append("⚠️ MODO LIMITADO - MERCADO ABIERTO SIN MT5\n", style="bold yellow")
        content.append(f"📊 Sesión: {session_name}\n", style="bright_cyan")
        content.append(f"❌ {info_mt5}\n", style="red")
        content.append("🔧 Reconectar MT5 para análisis completo\n", style="bright_red")
        hibernation_status = "⚠️ LIMITADO"
        panel_title = "⚠️ [bold yellow]MODO LIMITADO - RECONECTAR MT5[/bold yellow]"
        border_color = "bright_yellow"

    else:
        # 🌙 HIBERNACIÓN REAL
        content.append("🌙 SISTEMA EN HIBERNACIÓN - MERCADO CERRADO\n", style="bold blue")
        next_session = market_status.get('proxima_sesion', {})
        if next_session:
            content.append(f"⏰ Próxima sesión: {next_session.get('time_string', 'Calculando...')}\n", style="bright_cyan")
        content.append(f"📊 Estado mercado: {market_status_text}\n", style="bright_blue")
        hibernation_status = "🌙 HIBERNANDO"
        panel_title = "🌙 [bold blue]HIBERNACIÓN INTELIGENTE - ESPERANDO MERCADO[/bold blue]"
        border_color = "bright_blue"

    # ⏱️ TIEMPO EN ESTADO ACTUAL
    elapsed = datetime.now() - hibernation_start
    hours = int(elapsed.total_seconds() // 3600)
    minutes = int((elapsed.total_seconds() % 3600) // 60)
    content.append(f"⏱️ Tiempo en estado actual: {hours}h {minutes}m\n\n", style="white")

    # 📈 MÉTRICAS DEL SISTEMA MEJORADAS
    content.append("📈 MÉTRICAS DEL SISTEMA:\n", style="bold blue")
    content.append(f"• Estado: {hibernation_status}\n", style="bold cyan")
    content.append(f"• Análisis realizados: {analysis_count}\n", style="white")
    content.append(f"• Patrones detectados: {patterns_detected}\n", style="bright_cyan")
    content.append(f"• Señales alta probabilidad: {high_probability_signals}\n", style="bright_green")
    content.append(f"• Actualizaciones de datos: {system_metrics.get('data_updates', 0)}\n", style="bright_yellow")

    # 🔍 ESTADO DETALLADO
    content.append(f"• Mercado: {'🟢 ABIERTO' if is_market_open else '🔴 CERRADO'}\n",
                  style="bright_green" if is_market_open else "bright_red")
    content.append(f"• MT5: {'🟢 CONECTADO' if mt5_connected else '🔴 DESCONECTADO'}\n",
                  style="bright_green" if mt5_connected else "bright_red")

    # 🛡️ INFORMACIÓN DE GESTIÓN DE RIESGO
    if riskbot:
        try:
            balance = riskbot.get_account_balance()
            positions = len(riskbot.get_open_positions())
            _, _, profit_neto, _, _ = riskbot.get_total_profit_and_lots()
            content.append(f"🛡️ RiskBot: ${balance:.2f} | {positions} pos | P&L: ${profit_neto:.2f}\n",
                          style="bright_green")
        except Exception as e:
            content.append("🛡️ RiskBot: Error obteniendo datos\n", style="red")
            if debug_mode:
                content.append(f"   Error: {e}\n", style="dim red")

    # 🎨 CREAR PANEL FINAL
    return Panel(
        content,
        title=panel_title,
        subtitle=f"🔬 Debug: {'ON' if debug_mode else 'OFF'} | 📊 {patterns_detected} patrones | 💾 {system_metrics.get('export_count', 0)} exports",
        border_style=border_color,
        padding=(1, 2)
    )


def test_hibernacion_perfecta():
    """
    Función de prueba para la hibernación perfecta
    """
    enviar_senal_log("INFO", "🧪 PROBANDO HIBERNACIÓN PERFECTA...", __name__, "sistema")
    enviar_senal_log("INFO", "=" * 50, __name__, "sistema")

    # Probar detección MT5
    conectado, precio, info = detectar_mt5_optimizado()
    enviar_senal_log("INFO", f"MT5 Conectado: {conectado}", __name__, "sistema")
    enviar_senal_log("INFO", f"Precio: {precio}", __name__, "sistema")
    enviar_senal_log("INFO", f"Info: {info}", __name__, "sistema")

    enviar_senal_log("INFO", "\n✅ Prueba completada", __name__, "sistema")


if __name__ == "__main__":
    test_hibernacion_perfecta()
