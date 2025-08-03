#!/usr/bin/env python3
"""
🎯 MULTI-POI DASHBOARD INTEGRATION
=================================

Integración directa para dashboard_definitivo.py -            # Verificar si es problema de datos o de mercado
            if df_m5 is not None and hasattr(df_m5, '__len__'):
                dataset_size = len(df_m5)
                if dataset_size < 20:
                    enviar_senal_log("INFO", f"📊 FOREX CONTEXT: Dataset pequeño ({dataset_size} velas) - insuficiente para POI detection", __name__, "analysis")
                    content.append("📊 Datos insuficientes para análisis POI\n", style="yellow")
                    content.append(f"   └─ Solo {dataset_size} velas disponibles (mín: 20)\n", style="dim")
                else:
                    enviar_senal_log("INFO", f"📊 FOREX CONTEXT: Dataset OK ({dataset_size} velas) pero sin POIs - mercado en consolidación", __name__, "analysis")
                    content.append("🔍 Mercado en fase de consolidación\n", style="yellow")
                    content.append("   └─ No hay estructuras POI claras detectadas\n", style="dim")
            else:
                enviar_senal_log("WARNING", "📊 FOREX CONTEXT: df_m5 no disponible para diagnóstico", __name__, "analysis")
                content.append("📊 Sin datos para diagnóstico detallado\n", style="yellow")
                content.append("   └─ DataFrame M5 no disponible\n", style="dim")T PROFESIONAL
Versión optimizada para usar el sistema POI existente al 100%

Fecha: Agosto 2025
"""

from typing import Dict, List, Optional, Any
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from datetime import datetime

# Imports del sistema POI existente
try:
    from core.poi_system.poi_detector import POIDetector, encontrar_pois_multiples_para_dashboard
    from sistema.logging_interface import enviar_senal_log, log_poi
except ImportError as e:
    enviar_senal_log("WARNING", f"⚠️ Import warning: {e}", "poi_dashboard_integration", "migration")


def integrar_multi_poi_en_panel_ict(dashboard_instance):
    """
    🎯 FUNCIÓN PRINCIPAL DE INTEGRACIÓN PARA PANEL ICT PROFESIONAL
    =============================================================

    Reemplaza el contenido actual del panel ICT PROFESIONAL con Multi-POI Dashboard.

    Args:
        dashboard_instance: Instancia del dashboard principal

    Returns:
        Panel con contenido Multi-POI para el panel ICT
    """
    try:
        enviar_senal_log("INFO", "🚀 Integrando Multi-POI en panel ICT PROFESIONAL", __name__, "dashboard")

        # 1. VERIFICAR DATOS DISPONIBLES
        current_price = getattr(dashboard_instance, 'current_price', 1.17500)
        mt5_connected = getattr(dashboard_instance, 'mt5_connected', False)

        # 2. OBTENER DATOS DEL MERCADO CON DIAGNÓSTICO COMPLETO
        market_data = getattr(dashboard_instance, 'real_market_data', {})
        df_m5 = market_data.get('candles_m5')
        df_h1 = market_data.get('candles_h1')

        # 📊 DIAGNÓSTICO DETALLADO DE DATOS FOREX
        data_issues = []

        if market_data is None or not market_data:
            data_issues.append("MARKET_DATA_EMPTY")
            enviar_senal_log("ERROR", "🚨 FOREX DATA ISSUE: market_data completamente vacío", __name__, "mt5")

        if df_m5 is None:
            data_issues.append("M5_NULL")
            enviar_senal_log("WARNING", "⚠️ FOREX DATA: df_m5 es None - posible problema de conexión MT5", __name__, "mt5")
        elif df_m5.empty:
            data_issues.append("M5_EMPTY")
            enviar_senal_log("WARNING", "⚠️ FOREX DATA: df_m5 vacío - sin datos históricos M5", __name__, "mt5")
        else:
            dataset_size = len(df_m5) if df_m5 is not None else 0
            enviar_senal_log("INFO", f"✅ FOREX DATA: M5 disponible con {dataset_size} velas", __name__, "mt5")

        if df_h1 is None:
            data_issues.append("H1_NULL")
            enviar_senal_log("WARNING", "⚠️ FOREX DATA: df_h1 es None - análisis de tendencia limitado", __name__, "mt5")
        elif df_h1.empty:
            data_issues.append("H1_EMPTY")
            enviar_senal_log("WARNING", "⚠️ FOREX DATA: df_h1 vacío - sin contexto H1", __name__, "mt5")

        # 🔍 VERIFICACIÓN CRÍTICA: Sin datos M5 no podemos continuar
        if df_m5 is None or df_m5.empty:
            # Log detallado del problema
            mt5_status = "CONECTADO" if mt5_connected else "DESCONECTADO"
            session_time = datetime.now().strftime("%H:%M:%S")

            enviar_senal_log("CRITICAL", f"🚨 FOREX CRITICAL: Sin datos M5 para POI | MT5: {mt5_status} | Hora: {session_time} | Issues: {', '.join(data_issues)}", __name__, "mt5")

            # Retornar panel específico con diagnóstico
            return _crear_panel_diagnostico_forex(data_issues, mt5_connected, session_time)

        dataset_size = len(df_m5) if df_m5 is not None else 0
        enviar_senal_log("DEBUG", f"Datos disponibles: M5={dataset_size} velas, precio={current_price:.5f}", __name__, "dashboard")

        # 3. DETECTAR POIs USANDO SISTEMA EXISTENTE
        poi_detector = POIDetector()

        # Simular mercado context para encontrar_pois_multiples_para_dashboard
        class MockMercado:
            def __init__(self, pois_list, current_price):
                self.pois = {'M5': pois_list}
                self.current_price = current_price

        # Detectar POIs en M5
        all_pois = poi_detector.find_all_pois(df_m5, "M5", current_price)
        enviar_senal_log("INFO", f"✅ POIs detectados: {len(all_pois)}", __name__, "poi")

        # Crear mock mercado y obtener POIs para dashboard
        mock_mercado = MockMercado(all_pois, current_price)
        pois_dashboard = encontrar_pois_multiples_para_dashboard(mock_mercado, current_price, max_pois=6)

        enviar_senal_log("INFO", f"✅ POIs para dashboard: {len(pois_dashboard)}", __name__, "dashboard")

        # 4. CREAR CONTENIDO MULTI-POI
        return _crear_panel_multi_poi_completo(pois_dashboard, current_price, mt5_connected, df_m5)

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error integrando Multi-POI: {e}", __name__, "dashboard")
        return _crear_panel_fallback_error(str(e))


def _crear_panel_multi_poi_completo(pois_dashboard: List[Dict], current_price: float, mt5_connected: bool, df_m5: Optional[Any] = None) -> Panel:
    """
    Crea el panel Multi-POI completo para reemplazar el panel ICT.

    Args:
        pois_dashboard: Lista de POIs para mostrar
        current_price: Precio actual
        mt5_connected: Estado de conexión MT5
        df_m5: DataFrame M5 para diagnóstico (opcional)
    """
    try:
        # HEADER CON ESTADÍSTICAS
        total_pois = len(pois_dashboard)
        pois_alta_calidad = len([p for p in pois_dashboard if p.get('quality', 'D') in ['A+', 'A', 'B']])

        content = Text()

        # 📊 HEADER DE ESTADO
        content.append("🎯 MULTI-POI DASHBOARD\n", style="bold bright_cyan")
        content.append("=" * 40 + "\n\n", style="dim")

        # Estado de conexión
        if mt5_connected:
            content.append("🟢 MT5 CONECTADO", style="bold green")
        else:
            content.append("🔴 MT5 DESCONECTADO", style="bold red")

        content.append(f" | 💰 {current_price:.5f}\n", style="bright_white")

        # Estadísticas POI
        content.append(f"📊 DETECTED: {total_pois} | ", style="cyan")
        content.append(f"⚡ QUALITY: {pois_alta_calidad} | ", style="bright_yellow")
        content.append(f"🎯 ACTIVOS: {len([p for p in pois_dashboard if p.get('status') == 'ACTIVO'])}\n\n", style="bright_green")

        if not pois_dashboard:
            # 🔍 DIAGNÓSTICO: ¿Por qué no hay POIs?
            enviar_senal_log("WARNING", "🔍 FOREX ANALYSIS: Sin POIs detectados - iniciando diagnóstico", __name__, "poi")

            # Verificar si es problema de datos o de mercado
            if df_m5 is not None and hasattr(df_m5, '__len__') and len(df_m5) < 20:
                dataset_size = len(df_m5) if df_m5 is not None else 0
                enviar_senal_log("INFO", f"📊 FOREX CONTEXT: Dataset pequeño ({dataset_size} velas) - insuficiente para POI detection", __name__, "analysis")
                content.append("� Datos insuficientes para análisis POI\n", style="yellow")
                content.append(f"   └─ Solo {dataset_size} velas disponibles (mín: 20)\n", style="dim")
            else:
                dataset_size = len(df_m5) if df_m5 is not None else 0
                enviar_senal_log("INFO", f"📊 FOREX CONTEXT: Dataset OK ({dataset_size} velas) pero sin POIs - mercado en consolidación", __name__, "analysis")
                content.append("🔍 Mercado en fase de consolidación\n", style="yellow")
                content.append("   └─ No hay estructuras POI claras detectadas\n", style="dim")

            content.append("⏳ Esperando nuevas oportunidades...\n", style="dim")
        else:
            # 🎯 MOSTRAR TOP POIs (máximo 4 para el espacio del panel)
            top_pois = sorted(pois_dashboard, key=lambda x: x.get('score', 0), reverse=True)[:4]

            for i, poi in enumerate(top_pois, 1):
                poi_type = poi.get('type', 'POI_TYPE_UNDEFINED')
                price = poi.get('price', 0)
                score = poi.get('score', 0)
                distance = poi.get('distance', 0) * 10000  # Convertir a pips
                quality = poi.get('quality', 'UNRATED')

                # Emoji por tipo
                emoji = _get_poi_emoji(poi_type)
                color = _get_poi_color(poi_type)

                # Línea compacta por POI
                content.append(f"{emoji} ", style=f"bold {color}")
                content.append(f"{poi_type.replace('_', ' '):<12} | ", style=f"{color}")
                content.append(f"💰 {price:.5f} | ", style="white")
                content.append(f"📊 {score:2.0f} | ", style="bright_white")
                content.append(f"📏 {distance:4.1f}p | ", style="yellow")
                content.append(f"⭐ {quality}\n", style=f"bold {_get_tier_color(quality)}")

            # 🎯 RECOMENDACIÓN
            if top_pois:
                mejor_poi = top_pois[0]
                content.append("\n" + "─" * 40 + "\n", style="dim")
                content.append("🎯 RECOMENDACIÓN: ", style="bold bright_yellow")

                # Obtener tipo de POI de forma segura con logging específico
                if mejor_poi:
                    poi_type = mejor_poi.get('type', 'NO_POI_DETECTED')
                    poi_quality = mejor_poi.get('quality', 'C')
                    poi_distance = mejor_poi.get('distance', 0)
                    poi_score = mejor_poi.get('score', 0)

                    # Log del POI seleccionado
                    enviar_senal_log("INFO", f"🎯 MEJOR POI: {poi_type} | Score: {poi_score} | Distancia: {poi_distance * 10000:.1f} pips", __name__, "poi")
                else:
                    # Caso muy raro: hay top_pois pero mejor_poi es None
                    poi_type = 'DATA_CORRUPTION_DETECTED'
                    poi_quality = 'N/A'
                    poi_distance = 0
                    poi_score = 0

                    enviar_senal_log("ERROR", "🚨 FOREX ANOMALY: top_pois existe pero mejor_poi es None - posible corrupción de datos", __name__, "analysis")

                content.append(f"{poi_type} ", style=f"bold {_get_poi_color(poi_type)}")
                content.append(f"(TIER {poi_quality})\n", style=f"bold {_get_tier_color(poi_quality)}")
                content.append(f"Distancia: {poi_distance * 10000:.1f} pips | Score: {poi_score:.0f}", style="bright_white")

        return Panel(
            content,
            title="🎯 [bold bright_cyan]MULTI-POI DASHBOARD[/bold bright_cyan]",
            border_style="bright_cyan",
            padding=(1, 2)
        )

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error creando panel Multi-POI completo: {e}", __name__, "dashboard")
        return _crear_panel_fallback_error(str(e))


def _get_poi_emoji(poi_type: str) -> str:
    """Retorna emoji apropiado para cada tipo de POI."""
    emojis = {
        'BULLISH_OB': '🔵',
        'BEARISH_OB': '🔴',
        'BULLISH_FVG': '🟢',
        'BEARISH_FVG': '🟡',
        'BULLISH_BREAKER': '🟦',
        'BEARISH_BREAKER': '🟥',
        'LIQUIDITY_VOID': '⚪',
        'PRICE_IMBALANCE': '🟣',
        'NO_POI_DETECTED': '❓',
        'NO_DATA_AVAILABLE': '⏸️',
        'POI_TYPE_UNDEFINED': '❔'
    }
    return emojis.get(poi_type, '⚫')


def _get_poi_color(poi_type: str) -> str:
    """Retorna color apropiado para cada tipo de POI."""
    # Manejar casos None o vacíos
    if not poi_type or not isinstance(poi_type, str):
        return 'white'

    colors = {
        'BULLISH_OB': 'bright_blue',
        'BEARISH_OB': 'bright_red',
        'BULLISH_FVG': 'bright_green',
        'BEARISH_FVG': 'yellow',
        'BULLISH_BREAKER': 'blue',
        'BEARISH_BREAKER': 'red',
        'LIQUIDITY_VOID': 'white',
        'PRICE_IMBALANCE': 'magenta',
        'NO_POI_DETECTED': 'dim',
        'NO_DATA_AVAILABLE': 'red',
        'POI_TYPE_UNDEFINED': 'yellow'
    }
    return colors.get(poi_type.upper(), 'white')  # Usar upper() para mayor tolerancia


def _get_tier_color(grade: str) -> str:
    """Retorna color apropiado para cada tier de calidad."""
    # Manejar casos None o vacíos
    if not grade or not isinstance(grade, str):
        return 'white'

    colors = {
        'A+': 'bright_yellow',  # Dorado
        'A': 'bright_green',
        'B': 'bright_white',
        'C': 'white',
        'D': 'dim',
        'N/A': 'red',
        'UNRATED': 'yellow'
    }
    return colors.get(grade.upper(), 'white')  # Usar upper() para mayor tolerancia


def _crear_panel_diagnostico_forex(data_issues: List[str], mt5_connected: bool, session_time: str) -> Panel:
    """
    🩺 PANEL DE DIAGNÓSTICO ESPECÍFICO PARA PROBLEMAS DE DATOS FOREX
    ================================================================

    Crea un panel detallado que explica exactamente qué está fallando
    en la obtención de datos Forex y sugiere soluciones.
    """
    content = Text()
    content.append("🩺 FOREX DATA DIAGNOSTICS\n", style="bold bright_red")
    content.append("=" * 35 + "\n\n", style="dim")

    # Estado MT5
    if mt5_connected:
        content.append("🟢 MT5 STATUS: CONNECTED\n", style="bold green")
    else:
        content.append("🔴 MT5 STATUS: DISCONNECTED\n", style="bold red")
        content.append("   └─ Problema principal identificado\n", style="red")

    content.append(f"⏰ Session Time: {session_time}\n\n", style="cyan")

    # Diagnóstico específico por issue
    content.append("🔍 ISSUES DETECTED:\n", style="bold yellow")

    for issue in data_issues:
        if issue == "MARKET_DATA_EMPTY":
            content.append("   ❌ Market Data Container: EMPTY\n", style="red")
            content.append("      └─ Sistema no recibió datos del backend\n", style="dim")

        elif issue == "M5_NULL":
            content.append("   ❌ M5 Timeframe: NULL REFERENCE\n", style="red")
            content.append("      └─ MT5 no respondió para M5\n", style="dim")

        elif issue == "M5_EMPTY":
            content.append("   ❌ M5 Timeframe: NO HISTORICAL DATA\n", style="red")
            content.append("      └─ Posible: Market closed/Weekend\n", style="dim")

        elif issue == "H1_NULL":
            content.append("   ⚠️ H1 Timeframe: NULL (Análisis limitado)\n", style="yellow")

        elif issue == "H1_EMPTY":
            content.append("   ⚠️ H1 Timeframe: EMPTY (Sin contexto)\n", style="yellow")

    content.append("\n🛠️ RECOMMENDED ACTIONS:\n", style="bold bright_white")

    if not mt5_connected:
        content.append("   1. Verificar conexión MT5\n", style="white")
        content.append("   2. Revisar credenciales de trading\n", style="white")
        content.append("   3. Comprobar estado del servidor\n", style="white")
    else:
        # MT5 conectado pero sin datos
        hour = int(session_time.split(':')[0])
        if 22 <= hour or hour <= 6:  # Fin de semana o fuera de horario
            content.append("   • Horario de mercado cerrado detectado\n", style="yellow")
            content.append("   • Esperando apertura del mercado...\n", style="yellow")
        else:
            content.append("   • Reiniciar feed de datos MT5\n", style="white")
            content.append("   • Verificar símbolo EURUSD disponible\n", style="white")

    content.append("\n📊 Multi-POI en standby hasta resolución\n", style="dim")

    return Panel(
        content,
        title="🩺 [bold bright_red]FOREX DATA DIAGNOSTICS[/bold bright_red]",
        border_style="bright_red",
        padding=(1, 2)
    )


def _crear_panel_fallback_mt5() -> Panel:
    """Crea panel de fallback cuando no hay datos MT5."""
    content = Text()
    content.append("🎯 MULTI-POI DASHBOARD\n", style="bold bright_cyan")
    content.append("=" * 30 + "\n\n", style="dim")
    content.append("⚠️ Esperando datos MT5...\n", style="yellow")
    content.append("🔄 Conectando a fuente de datos\n", style="white")
    content.append("📊 Sistema POI listo para activar\n", style="dim")

    return Panel(
        content,
        title="🎯 [bold yellow]POI SYSTEM - STANDBY[/bold yellow]",
        border_style="yellow",
        padding=(2, 4)
    )


def _crear_panel_fallback_error(error_msg: str) -> Panel:
    """Crea panel de fallback cuando hay errores."""
    content = Text()
    content.append("🎯 MULTI-POI DASHBOARD\n", style="bold bright_cyan")
    content.append("=" * 30 + "\n\n", style="dim")
    content.append("❌ Error temporal del sistema\n", style="red")
    content.append("🔧 Reintentando conexión...\n", style="yellow")
    content.append(f"📝 Debug: {error_msg[:50]}...\n", style="dim")

    return Panel(
        content,
        title="🎯 [bold red]POI SYSTEM - ERROR[/bold red]",
        border_style="red",
        padding=(2, 4)
    )
