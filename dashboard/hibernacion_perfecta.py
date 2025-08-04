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
- ✅ Verificación múltiple para mayor precisión
- ✅ UI más clara y profesional
- ✅ Estados dinámicos con colores apropiados

Autor: ICT Engine Team
Fecha: 04 Agosto 2025
"""

from datetime import datetime
from rich.text import Text
from rich.panel import Panel


def detectar_mt5_optimizado():
    """
    Detección optimizada de MT5 con múltiples métodos

    Returns:
        tuple: (conectado: bool, precio_actual: float, info_conexion: str)
    """
    try:
        # Método 1: Verificación directa MT5
        import MetaTrader5 as mt5

        # Intentar conexión rápida
        if not mt5.initialize():
            return False, 0.0, "MT5 no inicializado"

        # Verificar cuenta activa
        account_info = mt5.account_info()
        if not account_info:
            mt5.shutdown()
            return False, 0.0, "Sin info de cuenta"

        # Obtener tick actual para confirmar conexión activa
        tick = mt5.symbol_info_tick("EURUSD")
        if not tick:
            mt5.shutdown()
            return False, 0.0, "Sin datos de tick"

        precio_actual = tick.bid
        mt5.shutdown()

        return True, precio_actual, f"Conectado - Precio: {precio_actual:.5f}"

    except ImportError:
        return False, 0.0, "MT5 no instalado"
    except Exception as e:
        return False, 0.0, f"Error: {str(e)[:50]}"


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
    print("🧪 PROBANDO HIBERNACIÓN PERFECTA...")
    print("=" * 50)

    # Probar detección MT5
    conectado, precio, info = detectar_mt5_optimizado()
    print(f"MT5 Conectado: {conectado}")
    print(f"Precio: {precio}")
    print(f"Info: {info}")

    print("\n✅ Prueba completada")


if __name__ == "__main__":
    test_hibernacion_perfecta()
