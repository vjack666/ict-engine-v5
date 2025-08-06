#!/usr/bin/env python3
"""
ICT Professional Widget - Motor Visual del Sistema ICT
======================================================

Widget profesional que transforma datos ICT técnicos en un "Mapa del Tesoro"
visual con narrativas inteligentes y análisis contextual.

Este widget toma los datos del ICTPatternAnalyzer y los presenta de forma
visualmente impactante y narrativamente comprehensiva para el trader.

Autor: Sistema Automático
Fecha: 25 de Julio, 2025
Versión: ICT Professional v1.0
"""

from rich.panel import Panel
from rich.table import Table
# MIGRADO A SLUC v2.0
from sistema.sic import enviar_senal_log

# 🎯 INTEGRACIÓN POI SYSTEM - VALIDADO AL 100%
from sistema.sic import (
    detectar_todos_los_pois,
    encontrar_pois_multiples_para_dashboard,
    POIDetector,
    POI_TYPES
)

from rich.layout import Layout
from rich.text import Text
from rich.console import Group
from rich import box
from sistema.sic import datetime
import pandas as pd
from sistema.sic import Dict, List, Optional

# 🔍 Logger especializado para widget ICT
# SLUC v2.0: logging centralizado

# Imports de tipos ICT desde el motor consolidado
from core.ict_engine.ict_types import (
    ICTPattern, MarketPhase, SessionType, SignalStrength, TradingDirection,
    ICTSignal, MarketStructure, ICTAnalysisResult,
    PATTERN_EMOJIS, DIRECTION_COLORS, get_pattern_description, get_strength_color, get_risk_reward_assessment
)


class ICTProfessionalWidget:
    """
    Widget profesional ICT que convierte análisis técnico en narrativa visual.

    Características:
    - Renderizado de análisis ICT como "mapa del tesoro"
    - Narrativas contextuales de patrones
    - Plans de acción ejecutivos paso a paso
    - Análisis de confluencias y risk management
    - Presentación visual profesional con Rich
    """

    def __init__(self):
        # 📊 Estado actual del mercado
        self.symbol = "EURUSD"
        self.current_price = 1.09234
        self.pois = []
        self.candles_data = None
        self.last_update = datetime.now()

        # 🧠 Análisis ICT actual
        self.current_analysis: Optional[ICTAnalysisResult] = None

        # 🎯 Configuración de renderizado
        self.max_pois_display = 8
        self.max_action_items = 6

        # 📈 Estado de visualización
        self.show_detailed_levels = True
        self.show_narratives = True
        self.show_risk_assessment = True

        # 🎯 POI DETECTOR - SISTEMA VALIDADO
        self.poi_detector = POIDetector()
        enviar_senal_log("INFO", "🎯 POI Detector inicializado en ICT Widget", "ict_widget", "widget")

    def update_poi_data(self, candles_data: pd.DataFrame) -> None:
        """
        🎯 ACTUALIZA DATOS POI USANDO SISTEMA VALIDADO

        Integra el sistema POI completamente validado con el dashboard.
        Este método usa las funciones del POI detector que pasaron 100% de tests.

        Args:
            candles_data: DataFrame con datos OHLC para análisis POI
        """
        try:
            enviar_senal_log("DEBUG", "🔄 Actualizando datos POI en widget", "ict_widget", "widget")

            # 📊 Validar datos de entrada
            if candles_data is None or candles_data.empty:
                enviar_senal_log("WARNING", "⚠️ Datos OHLC vacíos para POI detection", "ict_widget", "widget")
                self.pois = []
                return

            # 🎯 USAR SISTEMA POI VALIDADO AL 100%
            # Usar detectar_todos_los_pois que es la función principal validada
            pois_resultado = detectar_todos_los_pois(
                candles_data,
                timeframe='H1',  # Timeframe principal para dashboard
                current_price=self.current_price
            )

            # 🔄 Convertir a formato del widget
            self.pois = []

            # Procesar Order Blocks
            for ob in pois_resultado.get('order_blocks', []):
                widget_poi = {
                    'type': ob.get('type', 'Unknown'),
                    'price': ob.get('price', self.current_price),
                    'strength': int(ob.get('score', 50)),
                    'timeframe': ob.get('timeframe', 'H1'),
                    'direction': 'BULLISH' if 'BULLISH' in ob.get('type', '') else 'BEARISH',
                    'timestamp': ob.get('created_at', datetime.now())
                }
                self.pois.append(widget_poi)

            # Procesar Fair Value Gaps
            for fvg in pois_resultado.get('fair_value_gaps', []):
                widget_poi = {
                    'type': fvg.get('type', 'Unknown'),
                    'price': fvg.get('price', self.current_price),
                    'strength': int(fvg.get('score', 50)),
                    'timeframe': fvg.get('timeframe', 'H1'),
                    'direction': 'BULLISH' if 'BULLISH' in fvg.get('type', '') else 'BEARISH',
                    'timestamp': fvg.get('created_at', datetime.now())
                }
                self.pois.append(widget_poi)

            # Procesar Breaker Blocks
            for bb in pois_resultado.get('breaker_blocks', []):
                widget_poi = {
                    'type': bb.get('type', 'Unknown'),
                    'price': bb.get('price', self.current_price),
                    'strength': int(bb.get('score', 50)),
                    'timeframe': bb.get('timeframe', 'H1'),
                    'direction': 'BULLISH' if 'BULLISH' in bb.get('type', '') else 'BEARISH',
                    'timestamp': bb.get('created_at', datetime.now())
                }
                self.pois.append(widget_poi)

            # Procesar Imbalances
            for im in pois_resultado.get('imbalances', []):
                widget_poi = {
                    'type': im.get('type', 'LIQUIDITY_VOID'),
                    'price': im.get('price', self.current_price),
                    'strength': int(im.get('score', 50)),
                    'timeframe': im.get('timeframe', 'H1'),
                    'direction': 'NEUTRAL',
                    'timestamp': im.get('created_at', datetime.now())
                }
                self.pois.append(widget_poi)

            # 📊 Ordenar POIs por proximidad al precio actual
            self.pois.sort(key=lambda x: abs(self.current_price - x['price']))

            # 📊 Log de POIs detectados
            total_pois = len(self.pois)
            resumen = pois_resultado.get('resumen', {})
            tiempo_proc = resumen.get('tiempo_procesamiento', 0) if isinstance(resumen, dict) else 0

            enviar_senal_log("INFO", f"✅ POIs actualizados: {total_pois} detectados", "ict_widget", "widget")
            enviar_senal_log("DEBUG", f"   📋 Distribución: OB={len(pois_resultado.get('order_blocks', []))}, FVG={len(pois_resultado.get('fair_value_gaps', []))}, BB={len(pois_resultado.get('breaker_blocks', []))}, IM={len(pois_resultado.get('imbalances', []))}", "ict_widget", "widget")
            enviar_senal_log("DEBUG", f"   🕐 Tiempo procesamiento: {tiempo_proc:.2f}s", "ict_widget", "widget")

            # 🕐 Actualizar timestamp
            self.last_update = datetime.now()

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error actualizando POIs: {str(e)}", "ict_widget", "widget")
            self.pois = []  # Fallback a estado seguro

    def render_professional_analysis(self) -> Panel:
        """
        🗺️ Renderiza el análisis profesional ICT completo - "Mapa del Tesoro"

        Método principal que genera visualización profesional de análisis ICT
        con narrativas contextuales y planes de acción ejecutivos.

        Returns:
            Panel: Panel de Rich con análisis completo renderizado y optimizado
        """
        # 🎯 Logging optimizado para performance
        current_time = datetime.now()
        enviar_senal_log("DEBUG", "Renderizando análisis ICT profesional", "ict_widget_render", "widget")

        # 🚨 Validación de análisis disponible
        if not self.current_analysis:
            enviar_senal_log("WARNING", f"⏳ [UI-WAITING] Mostrando 'esperando datos' - sin análisis válido", "ict_widget", "widget")
            enviar_senal_log("DEBUG", f"   🔍 Estado actual: analysis={self.current_analysis}, precio={self.current_price}", "ict_widget", "widget")
            return self._render_no_analysis_panel()

        # 🖥️ Log de renderizado exitoso
        enviar_senal_log("INFO", f"🖥️ [UI-RENDER] Renderizando análisis ICT completo", "ict_widget", "widget")

        # Log de datos del análisis
        enviar_senal_log("DEBUG", "Datos disponibles para renderizado", "ict_widget", "widget")

        # 🏗️ Layout principal dividido en secciones
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=4),
            Layout(name="main_content"),
            Layout(name="footer", size=3)
        )

        # 📊 Header con información clave del mercado
        header_content = self._render_header_section()
        layout["header"].update(header_content)

        # 🎯 Contenido principal dividido en dos columnas
        layout["main_content"].split_row(
            Layout(name="analysis_column", ratio=3),
            Layout(name="technical_column", ratio=2)
        )

        # 📖 Columna de análisis (narrativa + patrón principal)
        layout["main_content"]["analysis_column"].split_column(
            Layout(name="primary_signal", ratio=2),
            Layout(name="market_structure", ratio=1)
        )

        # 🎯 Señal principal y narrativa
        primary_signal_content = self._render_primary_signal_section()
        layout["main_content"]["analysis_column"]["primary_signal"].update(primary_signal_content)

        # 📊 Estructura del mercado
        market_structure_content = self._render_market_structure_section()
        layout["main_content"]["analysis_column"]["market_structure"].update(market_structure_content)

        # 🔧 Columna técnica (niveles + métricas)
        layout["main_content"]["technical_column"].split_column(
            Layout(name="levels", ratio=3),
            Layout(name="metrics", ratio=2)
        )

        # 📊 Niveles técnicos
        levels_content = self._render_levels_section()
        layout["main_content"]["technical_column"]["levels"].update(levels_content)

        # 📈 Métricas y risk assessment
        metrics_content = self._render_metrics_section()
        layout["main_content"]["technical_column"]["metrics"].update(metrics_content)

        # 🎪 Footer con plan de acción
        footer_content = self._render_action_plan_footer()
        layout["footer"].update(footer_content)

        # 🔍 LOG CRÍTICO: FINALIZACIÓN DEL RENDERIZADO
        enviar_senal_log("INFO", f"🎨 [WIDGET-ICT-RENDER] Renderizado visual completado exitosamente", __name__, "general")
        enviar_senal_log("DEBUG", f"    🖼️ Panel ICT generado con análisis completo", __name__, "general")
        enviar_senal_log("DEBUG", f"    📊 Confianza: {getattr(self.current_analysis, 'analysis_confidence', 0):.0f}%", __name__, "general")
        enviar_senal_log("DEBUG", f"    🕐 Timestamp renderizado: {self.last_update.strftime('%H:%M:%S')}", __name__, "general")

        return Panel(
            layout,
            title="🗺️ [bold cyan]ICT PROFESSIONAL MARKET ANALYSIS[/bold cyan]",
            subtitle=f"🕐 {self.last_update.strftime('%H:%M:%S')} | 🎯 Confianza: {self.current_analysis.analysis_confidence:.0f}% | 📊 {self.symbol}",
            border_style="bright_cyan",
            padding=(0, 1)
        )

    def _render_no_analysis_panel(self) -> Panel:
        """Renderiza panel cuando no hay análisis disponible"""
        content = Text()
        content.append("🔍 INICIALIZANDO ANÁLISIS ICT PROFESIONAL...\n\n", style="bold cyan")
        content.append("🧠 Sistemas en línea:\n", style="yellow")
        content.append("• Pattern Recognition Engine: ✅ ACTIVO\n", style="green")
        content.append("• Market Structure Analyzer: ✅ ACTIVO\n", style="green")
        content.append("• Narrative Generator: ✅ ACTIVO\n", style="green")
        content.append("• Risk Assessment Module: ✅ ACTIVO\n\n", style="green")
        content.append("⏳ Esperando datos de mercado para análisis...", style="dim white")

        return Panel(
            content,
            title="🚀 [bold yellow]SISTEMA ICT PROFESIONAL[/bold yellow]",
            border_style="yellow",
            padding=(2, 4)
        )

    def _render_header_section(self) -> Panel:
        """Renderiza la sección de header con información clave del mercado"""
        if not self.current_analysis or not self.current_analysis.primary_signal:
            # Header sin señal principal
            header_text = Text()
            header_text.append(f"📊 ESTRUCTURA DE MERCADO: ", style="bold white")
            header_text.append("ANALIZANDO", style="yellow")
            header_text.append(" | ", style="white")
            header_text.append(f"💰 {self.symbol}: {self.current_price:.5f}", style="bold white")
            header_text.append(" | ", style="white")
            header_text.append(f"🌍 {self._get_session_display()}", style="bold cyan")

            return Panel(header_text, border_style="cyan", box=box.ROUNDED)

        signal = self.current_analysis.primary_signal
        header_text = Text()

        # 🎯 Patrón principal con emoji
        pattern_emoji = PATTERN_EMOJIS.get(signal.pattern, "🔍")
        pattern_name = signal.pattern.value.replace('_', ' ').upper()
        strength_color = get_strength_color(signal.strength)

        header_text.append(f"{pattern_emoji} {pattern_name}", style=f"bold {strength_color}")
        header_text.append(" | ", style="white")

        # 💰 Precio y dirección
        direction_color = DIRECTION_COLORS.get(signal.direction, "white")
        header_text.append(f"💰 {self.symbol}: {self.current_price:.5f}", style="bold white")
        header_text.append(f" → {signal.direction.value}", style=f"bold {direction_color}")
        header_text.append(" | ", style="white")

        # 🌍 Sesión y timing
        header_text.append(f"🌍 {self._get_session_display()}", style="bold cyan")
        header_text.append(" | ", style="white")

        # 🎯 Probabilidad
        prob_color = "green" if signal.probability > 75 else "yellow" if signal.probability > 60 else "orange"
        header_text.append(f"🎯 {signal.probability:.0f}%", style=f"bold {prob_color}")

        return Panel(header_text, border_style="cyan", box=box.ROUNDED)

    def _render_primary_signal_section(self) -> Panel:
        """Renderiza la sección de señal principal con narrativa completa"""
        if not self.current_analysis or not self.current_analysis.primary_signal:
            # Sin señal principal - mostrar evaluación general
            content = Text()
            content.append("🔍 ESCANEANDO ESTRUCTURA DE MERCADO...\n\n", style="bold cyan")
            content.append("📊 Estado Actual:\n", style="yellow")

            if self.current_analysis:
                content.append(f"• {self.current_analysis.overall_assessment}\n", style="white")
                content.append(f"• {self.current_analysis.recommended_action}\n", style="cyan")
                content.append(f"• Perspectiva: {self.current_analysis.market_outlook}\n", style="dim white")
            else:
                content.append("• Recopilando datos de mercado...\n", style="white")
                content.append("• Analizando POIs y estructura...\n", style="white")
                content.append("• Identificando confluencias...\n", style="white")

            content.append("\n⚡ El sistema notificará cuando detecte un patrón de alta probabilidad.", style="dim green")

            return Panel(
                content,
                title="📊 [bold yellow]Análisis de Mercado[/bold yellow]",
                border_style="yellow",
                box=box.ROUNDED
            )

        signal = self.current_analysis.primary_signal

        # 🏗️ Layout para la señal dividido en secciones
        signal_layout = Layout()
        signal_layout.split_column(
            Layout(name="pattern_header", size=3),
            Layout(name="narrative_content")
        )

        # 📊 Header del patrón
        pattern_header = self._render_pattern_header(signal)
        signal_layout["pattern_header"].update(pattern_header)

        # 📖 Narrativa completa
        narrative_content = Text()
        narrative_content.append(signal.narrative, style="white")

        # ⚡ Agregar contexto adicional si está disponible
        if signal.context:
            narrative_content.append(f"\n\n🌍 CONTEXTO:\n{signal.context}", style="dim cyan")

        signal_layout["narrative_content"].update(Panel(
            narrative_content,
            title="📖 [bold green]Narrativa del Patrón[/bold green]",
            border_style="green",
            box=box.ROUNDED
        ))

        return Panel(
            signal_layout,
            title=f"🎯 [bold magenta]SEÑAL PRINCIPAL: {signal.pattern.value.upper().replace('_', ' ')}[/bold magenta]",
            border_style="bright_magenta"
        )

    def _render_pattern_header(self, signal: ICTSignal) -> Panel:
        """Renderiza header específico del patrón detectado con mejor claridad visual"""
        # 🎯 Crear tabla para organizar información más claramente
        info_table = Table(show_header=False, show_edge=False, box=None, padding=(0, 1))
        info_table.add_column("metric", style="bold", width=12)
        info_table.add_column("value", style="white", width=15)
        info_table.add_column("metric2", style="bold", width=12)
        info_table.add_column("value2", style="white", width=15)

        # 📊 Primera fila: Fortaleza y Probabilidad
        fortaleza_color = "green" if signal.strength > 80 else "yellow" if signal.strength > 60 else "orange"
        prob_color = "green" if signal.probability > 75 else "yellow" if signal.probability > 60 else "orange"

        info_table.add_row(
            "🎯 Fortaleza:", f"[{fortaleza_color}]{signal.strength:.0f}%[/]",
            "📊 Probabilidad:", f"[{prob_color}]{signal.probability:.0f}%[/]"
        )

        # ⚖️ Segunda fila: Risk/Reward y Timing
        rr_color = "green" if signal.risk_reward > 3 else "yellow" if signal.risk_reward > 2 else "orange"
        entry_center = (signal.entry_zone[0] + signal.entry_zone[1]) / 2

        info_table.add_row(
            "⚖️ R:R Ratio:", f"[{rr_color}]1:{signal.risk_reward:.1f}[/]",
            "🕐 Timing:", "[bold cyan]CRÍTICA[/]"
        )

        # � Tercera fila: Entrada y Stop
        entry_range_pips = int((signal.entry_zone[1] - signal.entry_zone[0]) * 10000)
        stop_distance_pips = int(abs(signal.stop_loss - entry_center) * 10000)

        info_table.add_row(
            "📍 Entrada:", f"[cyan]{entry_center:.5f}[/]",
            "🛡️ Stop Loss:", f"[red]{stop_distance_pips} pips[/]"
        )

        return Panel(
            info_table,
            border_style="blue",
            box=box.ROUNDED,
            padding=(0, 1)
        )

    def _render_market_structure_section(self) -> Panel:
        """Renderiza análisis de estructura del mercado"""
        if not self.current_analysis:
            return Panel(Text("Estructura en análisis...", style="dim white"), border_style="dim white")

        structure = self.current_analysis.market_structure
        content = Text()

        # 📈 Tendencia principal
        trend_color = DIRECTION_COLORS.get(structure.primary_trend, "white")
        content.append("📈 ESTRUCTURA DE MERCADO:\n", style="bold blue")
        content.append(f"• Tendencia: {structure.primary_trend.value}", style=f"bold {trend_color}")
        content.append(f" ({structure.structure_quality.value.upper()})\n", style="white")

        # 🎪 Fase actual
        phase_emoji = {
            MarketPhase.ACCUMULATION: "📊",
            MarketPhase.MANIPULATION: "🎭",
            MarketPhase.DISTRIBUTION: "📉",
            MarketPhase.REBALANCE: "⚖️"
        }.get(structure.current_phase, "🔍")

        content.append(f"• Fase: {phase_emoji} {structure.current_phase.value.upper()}\n", style="yellow")

        # 🌊 Condiciones de mercado
        content.append(f"• Volatilidad: {structure.volatility_regime}\n", style="cyan")
        content.append(f"• Liquidez: {structure.liquidity_condition}\n", style="cyan")

        # 📊 Soporte/Resistencia más cercanos
        if structure.support_levels:
            closest_support = min(structure.support_levels, key=lambda x: abs(x - self.current_price))
            support_distance = int(abs(self.current_price - closest_support) * 10000)
            content.append(f"• Soporte más cercano: {support_distance} pips\n", style="green")

        if structure.resistance_levels:
            closest_resistance = min(structure.resistance_levels, key=lambda x: abs(x - self.current_price))
            resistance_distance = int(abs(self.current_price - closest_resistance) * 10000)
            content.append(f"• Resistencia más cercana: {resistance_distance} pips\n", style="red")

        return Panel(
            content,
            title="🏗️ [bold blue]Estructura del Mercado[/bold blue]",
            border_style="blue",
            box=box.ROUNDED
        )

    def _render_levels_section(self) -> Panel:
        """Renderiza tabla de niveles técnicos clave"""
        # 📊 Crear tabla de niveles
        levels_table = Table(
            show_header=True,
            header_style="bold magenta",
            box=box.SIMPLE_HEAD,
            expand=True
        )

        levels_table.add_column("🎯 Nivel", style="cyan", width=20, no_wrap=True)
        levels_table.add_column("💰 Precio", style="white", width=12, no_wrap=True)
        levels_table.add_column("📏 Dist", style="yellow", width=8, no_wrap=True)
        levels_table.add_column("🔥 Estado", style="green", width=12, no_wrap=True)

        # 💹 Precio actual (primera fila)
        levels_table.add_row(
            "[bold green]💹 Precio Actual[/bold green]",
            f"{self.current_price:.5f}",
            "---",
            "🎯 ACTIVO"
        )

        # 📊 Agregar POIs ordenados por proximidad
        if self.pois:
            sorted_pois = sorted(self.pois, key=lambda x: abs(self.current_price - x['price']))

            for poi in sorted_pois[:self.max_pois_display]:
                distance_pips = int(abs(self.current_price - poi['price']) * 10000)

                # 🎨 Styling dinámico basado en tipo de POI
                poi_type = poi.get('type', 'Unknown')
                if "BULLISH" in poi_type.upper():
                    emoji = "📈"
                    color = "green"
                elif "BEARISH" in poi_type.upper():
                    emoji = "📉"
                    color = "red"
                elif "Liquidity" in poi_type:
                    emoji = "🌊"
                    color = "cyan"
                elif "Order Block" in poi_type:
                    emoji = "🧱"
                    color = "blue"
                else:
                    emoji = "🔵"
                    color = "white"

                # 🚨 Estado basado en proximidad y strength
                strength = poi.get('strength', 'MEDIUM')
                if distance_pips < 20:
                    status = "🚨 CRÍTICO"
                elif distance_pips < 50:
                    if strength == 'HIGH':
                        status = "⚠️ ALERTA"
                    else:
                        status = "📊 CERCA"
                elif distance_pips < 100:
                    status = "👀 MONITOR"
                else:
                    status = "📋 WATCH"

                # 🔤 Truncar tipo si es muy largo
                display_type = poi_type[:18] + "..." if len(poi_type) > 18 else poi_type

                levels_table.add_row(
                    f"[{color}]{emoji} {display_type}[/{color}]",
                    f"{poi['price']:.5f}",
                    f"{distance_pips}p",
                    status
                )
        else:
            # Sin POIs disponibles
            levels_table.add_row(
                "[dim white]📊 Escaneando niveles...[/dim white]",
                "---",
                "---",
                "⏳ WAIT"
            )

        return Panel(
            levels_table,
            title="📊 [bold magenta]Niveles Clave[/bold magenta]",
            subtitle=f"📈 {len(self.pois)} POIs detectados",
            border_style="magenta",
            box=box.ROUNDED
        )

    def _render_metrics_section(self) -> Panel:
        """Renderiza métricas y assessment de riesgo con layout mejorado"""
        # 📊 Layout dividido: métricas arriba, riesgos abajo
        metrics_layout = Layout()
        metrics_layout.split_column(
            Layout(name="signal_metrics", ratio=3),
            Layout(name="risk_factors", ratio=2)
        )

        # ▲ Sección superior: Métricas de la señal
        if self.current_analysis and self.current_analysis.primary_signal:
            signal = self.current_analysis.primary_signal

            # 📊 Crear tabla de métricas
            metrics_table = Table(show_header=False, show_edge=False, box=None, padding=(0, 1))
            metrics_table.add_column("metric", style="bold", width=15)
            metrics_table.add_column("value", style="white", width=20)

            # ⚖️ Risk/Reward con assessment
            rr_assessment = get_risk_reward_assessment(signal.risk_reward)
            rr_color = "green" if signal.risk_reward > 3 else "yellow" if signal.risk_reward > 2 else "orange"
            metrics_table.add_row(
                "⚖️ Risk/Reward:",
                f"[{rr_color}]1:{signal.risk_reward:.1f} {rr_assessment}[/]"
            )

            # 🎯 Confianza con color dinámico
            confidence_color = get_strength_color(signal.probability)
            metrics_table.add_row(
                "🎯 Confianza:",
                f"[{confidence_color}]{signal.confidence.value.upper()}[/]"
            )

            # ⏰ Timing crítico
            time_color = "red" if "CRÍTICA" in signal.time_sensitivity else "yellow" if "ALTA" in signal.time_sensitivity else "green"
            metrics_table.add_row(
                "⏰ Timing:",
                f"[{time_color}]{signal.time_sensitivity.split(' - ')[0]}[/]"
            )

            # 💼 Position sizing
            metrics_table.add_row(
                "💼 Posición:",
                f"[cyan]{signal.position_sizing.split(' - ')[0]}[/]"
            )

            signal_content = Panel(
                metrics_table,
                title="📊 [bold blue]MÉTRICAS DE SEÑAL[/bold blue]",
                border_style="blue",
                box=box.SIMPLE
            )
        else:
            # Sin señal activa
            no_signal_text = Text()
            no_signal_text.append("🔍 EVALUANDO MÉTRICAS...\n", style="bold cyan")
            no_signal_text.append("• Volatilidad: NORMAL\n", style="white")
            no_signal_text.append("• Exposición: NINGUNA\n", style="green")
            no_signal_text.append("• Sistema: VIGILANTE", style="cyan")

            signal_content = Panel(
                no_signal_text,
                title="📊 [bold blue]MÉTRICAS DEL SISTEMA[/bold blue]",
                border_style="blue",
                box=box.SIMPLE
            )

        metrics_layout["signal_metrics"].update(signal_content)

        # ▼ Sección inferior: Factores de riesgo
        risk_content = Text()

        if self.current_analysis and self.current_analysis.warnings:
            risk_content.append("⚠️ FACTORES DE RIESGO:\n", style="bold red")
            for warning in self.current_analysis.warnings[:2]:  # Top 2 warnings
                # 🔤 Truncar warnings largos
                truncated_warning = warning[:35] + "..." if len(warning) > 35 else warning
                risk_content.append(f"• {truncated_warning}\n", style="yellow")

            # 🌟 Una oportunidad clave si hay espacio
            if self.current_analysis.opportunities:
                risk_content.append("\n🌟 OPORTUNIDAD:\n", style="bold green")
                opp = self.current_analysis.opportunities[0]
                truncated_opp = opp[:35] + "..." if len(opp) > 35 else opp
                risk_content.append(f"• {truncated_opp}", style="green")
        else:
            # Estado básico de riesgo
            risk_content.append("✅ EVALUACIÓN LIMPIA:\n", style="bold green")
            risk_content.append("• Sin riesgos inmediatos\n", style="green")
            risk_content.append("• Mercado en vigilancia activa", style="cyan")

        risk_panel = Panel(
            risk_content,
            title="⚠️ [bold yellow]ASSESSMENT[/bold yellow]",
            border_style="yellow",
            box=box.SIMPLE
        )

        metrics_layout["risk_factors"].update(risk_panel)

        return Panel(
            metrics_layout,
            title="📈 [bold blue]Risk Assessment[/bold blue]",
            border_style="blue",
            box=box.ROUNDED
        )

    def _render_action_plan_footer(self) -> Panel:
        """Renderiza el plan de acción en el footer"""
        if not self.current_analysis or not self.current_analysis.primary_signal:
            # Sin señal - mostrar acción recomendada general
            action_text = Text()
            action_text.append("👁️ VIGILANCIA ACTIVA: ", style="bold cyan")

            if self.current_analysis:
                action_text.append(self.current_analysis.recommended_action, style="yellow")
            else:
                action_text.append("Monitoreando estructura hasta detectar oportunidad clara", style="yellow")

            return Panel(
                action_text,
                title="🎪 [bold green]Estado de Acción[/bold green]",
                border_style="green",
                box=box.ROUNDED
            )

        signal = self.current_analysis.primary_signal

        # 🎪 Mostrar primeros 3 pasos del plan de acción
        action_text = Text()
        action_text.append("🎪 PLAN DE EJECUCIÓN INMEDIATO:\n", style="bold green")

        for i, step in enumerate(signal.action_plan[:3], 1):
            # 🎨 Color según prioridad
            if i == 1:
                priority_color = "bold green"
                icon = "🔥"
            elif i == 2:
                priority_color = "bold yellow"
                icon = "⚡"
            else:
                priority_color = "cyan"
                icon = "📊"

            action_text.append(f"{icon} {step}", style=priority_color)
            if i < len(signal.action_plan[:3]):
                action_text.append("  |  ", style="dim white")

        return Panel(
            action_text,
            title="🎪 [bold green]Plan de Acción Ejecutivo[/bold green]",
            border_style="green",
            box=box.ROUNDED
        )

    def _get_session_display(self) -> str:
        """Obtiene display de sesión actual con emoji"""
        session_displays = {
            SessionType.ASIAN: "🇯🇵 ASIA",
            SessionType.LONDON: "🇬🇧 LONDON",
            SessionType.NEW_YORK: "🇺🇸 NEW YORK",
            SessionType.OVERLAP: "🌍 OVERLAP",
            SessionType.LONDON_CLOSE: "🇬🇧 CLOSE"
        }

        if self.current_analysis and self.current_analysis.session_info:
            return session_displays.get(self.current_analysis.session_info.session, "🌍 UNKNOWN")

        # Fallback: determinar sesión por hora
        current_hour = datetime.now().hour
        if 8 <= current_hour < 16:
            return session_displays[SessionType.LONDON]
        elif 13 <= current_hour < 21:
            if 13 <= current_hour < 16:
                return session_displays[SessionType.OVERLAP]
            return session_displays[SessionType.NEW_YORK]
        else:
            return session_displays[SessionType.ASIAN]

    def update_analysis(self, analysis_result: ICTAnalysisResult):
        """
        🔄 Actualiza el widget con nuevo resultado de análisis ICT (optimizado)

        Args:
            analysis_result: Resultado completo del análisis ICT
        """
        current_time = datetime.now()

        # 🔍 LOG CRÍTICO: PUNTO DE RECEPCIÓN DE ANÁLISIS EN WIDGET ICT
        enviar_senal_log("INFO", f"🧠 [ICT-WIDGET] Recibiendo análisis ICT", "ict_widget", "widget")

        if analysis_result:
            patterns_count = len(getattr(analysis_result, 'patterns', [])) if hasattr(analysis_result, 'patterns') else 0
            signals_count = len(getattr(analysis_result, 'signals', [])) if hasattr(analysis_result, 'signals') else 0
            confidence = getattr(analysis_result, 'analysis_confidence', 'N/A')

            enviar_senal_log("INFO", f"✅ [ANÁLISIS-VÁLIDO] Análisis recibido correctamente", "ict_widget", "widget")
            enviar_senal_log("DEBUG", f"   🎯 Tipo: {type(analysis_result)}", "ict_widget", "widget")
            enviar_senal_log("DEBUG", f"   📊 Confianza: {confidence}", "ict_widget", "widget")
            enviar_senal_log("DEBUG", f"   🔍 Patrones: {patterns_count}, Señales: {signals_count}", "ict_widget", "widget")
            enviar_senal_log("DEBUG", f"   🎯 Señal principal: {getattr(analysis_result, 'primary_signal', None) is not None}", "ict_widget", "widget")
        else:
            enviar_senal_log("ERROR", f"❌ [ANÁLISIS-NULO] Análisis nulo/vacío recibido", "ict_widget", "widget")
            enviar_senal_log("DEBUG", f"   🔍 Valor recibido: {analysis_result}", "ict_widget", "widget")

        try:
            self.current_analysis = analysis_result
            self.last_update = current_time

            enviar_senal_log("INFO", f"✅ [ICT-WIDGET] Análisis almacenado correctamente", "ict_widget", "widget")

        except Exception as e:
            enviar_senal_log("ERROR", f"Error actualizando widget ICT: {str(e)}", "ict_widget", "widget")

    def update_ict_data(self, data: Dict):
        # --- SONDA DE TELEMETRÍA (PUNTO DE CONTROL B) ---
        # AÑADIR ESTE BLOQUE AL INICIO DEL MÉTODO:
        try:
            num_velas = len(data.get('last_100_candles_m1', [])) if data.get('last_100_candles_m1') is not None else 'None'
            precio = data.get('current_price', 'N/A')
            enviar_senal_log(
                "ERROR",
                f"[PUNTO DE CONTROL B] WIDGET -> ha RECIBIDO datos. Velas: {num_velas}, Precio: {precio}",
                __name__,
                "diagnostico"
            )
        except Exception as e:
            enviar_senal_log("ERROR", f"Error en sonda B: {e}", "ict_professional_widget", "migration")
        # --- FIN SONDA ---
        """
        Actualiza los datos ICT básicos (método de compatibilidad).

        Args:
            data: Diccionario con datos ICT básicos (precio, POIs, etc.)
        """
        # 🔍 LOG CRÍTICO: PUNTO DE RECEPCIÓN DE DATOS BÁSICOS EN WIDGET ICT
        current_price_new = data.get('current_price', self.current_price)
        pois_count = len(data.get('simple_pois', [])) if isinstance(data.get('simple_pois'), list) else 0

        # 🔧 CORRECCIÓN: Manejar tanto DataFrame como list para candles
        candles_data = data.get('last_100_candles_m1', [])
        if hasattr(candles_data, '__len__'):  # DataFrame, list, etc.
            candles_count = len(candles_data)
        else:
            candles_count = 0

        enviar_senal_log("INFO", f"🎯 [ICT-WIDGET] Recibiendo datos ICT básicos", "ict_widget", "widget")
        enviar_senal_log("DEBUG", f"   � Datos recibidos: {list(data.keys())}", "ict_widget", "widget")
        enviar_senal_log("DEBUG", f"   💰 Precio actualizado: {current_price_new}", "ict_widget", "widget")
        enviar_senal_log("DEBUG", f"   🎯 POIs: {pois_count}, Candles: {candles_count}", "ict_widget", "widget")

        try:
            self.current_price = current_price_new
            self.symbol = data.get('symbol', self.symbol)
            self.pois = data.get('simple_pois', self.pois)
            self.candles_data = data.get('last_100_candles_m1', self.candles_data)
            self.last_update = datetime.now()

            enviar_senal_log("INFO", f"✅ [ICT-WIDGET] Datos básicos actualizados correctamente", "ict_widget", "widget")

            enviar_senal_log("INFO", f"✅ [WIDGET-ICT-BASIC-UPDATE] Datos básicos aplicados al widget ICT", __name__, "general")
            enviar_senal_log("DEBUG", f"    📝 Widget ICT actualizado con datos básicos - listo para renderizado", __name__, "general")

        except (ValueError, KeyError, TypeError) as e:
            enviar_senal_log("ERROR", f"🚨 [WIDGET-ICT-DATA-ERROR] Error actualizando datos básicos ICT: {e}", __name__, "general")

        # 📝 Nota: Este método no actualiza el análisis completo,
        # solo los datos básicos. Para análisis completo usar update_analysis()

    def render_ict_analysis(self) -> Panel:
        """
        Método de compatibilidad que llama al renderizado principal.

        Returns:
            Panel: El mismo resultado que render_professional_analysis()
        """
        return self.render_professional_analysis()

    def get_current_status(self) -> Dict:
        """
        Obtiene estado actual del widget para debugging o logging.

        Returns:
            Dict: Estado actual con métricas clave
        """
        status = {
            'symbol': self.symbol,
            'current_price': self.current_price,
            'pois_count': len(self.pois),
            'last_update': self.last_update.isoformat(),
            'has_analysis': self.current_analysis is not None,
            'has_primary_signal': False,
            'analysis_confidence': 0.0
        }

        if self.current_analysis:
            status['has_primary_signal'] = self.current_analysis.primary_signal is not None
            status['analysis_confidence'] = self.current_analysis.analysis_confidence

            if self.current_analysis.primary_signal:
                signal = self.current_analysis.primary_signal
                status['primary_pattern'] = signal.pattern.value
                status['signal_strength'] = signal.strength
                status['signal_direction'] = signal.direction.value
                status['signal_probability'] = signal.probability

        return status
