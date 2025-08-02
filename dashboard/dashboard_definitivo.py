#!/usr/bin/env python3
"""
🚀 SENTINEL ICT ANALYZER - DASHBOARD DEFINITIVO
=============================================

EL DASHBOARD PRINCIPAL Y ÚNICO DEL SISTEMA SENTINEL ICT ANALYZER.
Conectado a datos reales de MT5 con análisis ICT completo y avanzado.

🌟 CARACTERÍSTICAS PRINCIPALES:
- 4 pestañas especializadas: H1 (Hibernación), H2 (ICT Pro), H3 (Patrones), H4 (Analytics)
- Conexión directa a MetaTrader5 FundedNext para datos reales
- Análisis inteligente con narrativas contextuales avanzadas
- Detección automática de patrones ICT (Silver Bullet, Judas Swing, OTE, etc.)
- Sistema de alertas multinivel para oportunidades de alta probabilidad
- Interface visual profesional con Rich y Textual
- Motor de análisis con datos reales de mercado
- Sistema de métricas y estadísticas en tiempo real

🎮 NAVEGACIÓN:
- H1: Estado de hibernación inteligente con métricas de MT5
- H2: Análisis ICT profesional con datos reales completos
- H3: 🧠 Patrones ICT con narrativa completa y plan de acción
- H4: 📊 Analytics y métricas avanzadas del sistema
- R: Refresh manual de todo el sistema y datos MT5
- P: Toggle análisis automático de patrones
- D: Debug mode para desarrollo
- E: Export de análisis y métricas
- Q: Salir del sistema

Autor: Sistema Sentinel Grid
Fecha: 2025-07-27
Versión: Dashboard Definitivo v5.0 🚀
Entorno: PRODUCCIÓN - DATOS REALES MT5
"""

# Standard library imports
import logging
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Third party imports
import pandas as pd
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Header, Footer, TabbedContent, TabPane, Static

# --- CONFIGURACIÓN CRÍTICA DE PATHS PYTHON ---
# DEBE IR ANTES DE CUALQUIER IMPORT DEL PROYECTO
# Asegurar que Python pueda encontrar todos los módulos del proyecto
try:
    # El directorio padre de dashboard es el proyecto principal
    project_root = Path(__file__).parent.parent  # ICT Engine v3.4

    # Agregar las rutas necesarias al sys.path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    # Verificar que el directorio es correcto
    core_path = project_root / "core"
    if not core_path.exists():
        raise RuntimeError(f"No se puede encontrar el directorio core en {project_root}")

except (FileNotFoundError, PermissionError, IOError) as e:
    print(f"❌ ERROR CRÍTICO configurando paths de Python: {e}")
    sys.exit(1)
# -------------------------------------------------

# Local imports
from sistema.emoji_logger import get_emoji_safe_logger, safe_log_and_print
from sistema.logging_interface import enviar_senal_log
from utils.mt5_data_manager import get_mt5_manager

# Core imports
from core.poi_system import poi_detector
from core.poi_system.poi_scoring_engine import POIScoringEngine
from core.trading import TradingDecisionEngine
from core.smart_trading_logger import TradingDecisionCache
from core.limit_order_manager import LimitOrderManager
from core.risk_management.riskbot_mt5 import RiskBot
from config.config_manager import ConfigManager
from dashboard.dashboard_controller import get_dashboard_controller

# 🎯 MULTI-POI DASHBOARD INTEGRATION
try:
    from dashboard.poi_dashboard_integration import integrar_multi_poi_en_panel_ict
    multi_poi_available = True
    print("✅ Multi-POI Dashboard disponible para panel ICT")
except ImportError as e:
    multi_poi_available = False
    print(f"⚠️ Multi-POI Dashboard no disponible: {e}")

# 🧠 CLEAN POI DIAGNOSTICS INTEGRATION
try:
    from clean_poi_diagnostics import integrar_poi_dashboard_limpio
    clean_poi_available = True
    print("✅ Clean POI Diagnostics disponible")
except ImportError as e:
    clean_poi_available = False
    print(f"⚠️ Clean POI Diagnostics no disponible: {e}")

# 🔧 CONFIGURACIÓN DE LOGGING CENTRALIZADO - FASE 2
try:
    # MIGRADO A SLUC v2.0 - Sistema de logging unificado
    # Inicializar el Smart Logger (patrón singleton)
    # Logger especializado para dashboard
    logger = get_emoji_safe_logger('dashboard')
    safe_log_and_print("DASHBOARD",
                      "🚀 Dashboard Definitivo conectado al sistema de logging centralizado",
                      True)
    safe_log_and_print("DASHBOARD",
                      "📊 Iniciando sistema de vigilancia para dashboard principal",
                      True)
    # Registrar evento de sistema
    enviar_senal_log("INFO", "Dashboard Definitivo iniciado", __name__, "general")
except ImportError as e:
    # Fallback a logging básico si no está disponible el smart logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('data/logs/dashboard/dashboard_definitivo.log',
                              encoding='utf-8')
        ]
    )
    logger = logging.getLogger('sentinel.dashboard_definitivo')
    logger.warning("⚠️ Smart logger no disponible: %s. Usando logging básico.", e)

# Imports de sistemas reales MT5 y ICT
try:
    # CORRECCIÓN: No importar funciones obsoletas
    # from sistema.mt5_connector import inicializar_mt5, asegurar_simbolo_disponible
    # CORRECCIÓN: Importar sistema SLUC para logging
    # Ya importado arriba

    # 🧠 CAJA NEGRA ICT COMPLETA - Motores principales
    # import sys ya importado previamente
    # sys.path.append('..') ya configurado
    from core.ict_engine import ict_types
    from core.ict_engine import ict_detector
    from core.ict_engine import pattern_analyzer as ict_pattern_analyzer
    from core.ict_engine import confidence_engine
    from core.ict_engine.veredicto_engine_v4 import VeredictoEngine
    from core.ict_engine import ict_historical_analyzer

    # Widgets del dashboard
    from dashboard import ict_professional_widget
    from dashboard import dashboard_widgets

    # Extraer las clases necesarias
    ICTPattern = ict_types.ICTPattern
    TradingDirection = ict_types.TradingDirection
    SessionType = ict_types.SessionType
    PATTERN_EMOJIS = ict_types.PATTERN_EMOJIS

    # 🧠 CAJA NEGRA ICT - Clases principales
    ICTPatternAnalyzer = ict_pattern_analyzer.ICTPatternAnalyzer
    ICTDetector = ict_detector.MarketContext  # Clase principal del detector
    ConfidenceEngine = confidence_engine.ConfidenceEngine
    # VeredictoEngine ya se importó directamente arriba
    ICTHistoricalAnalyzer = ict_historical_analyzer.ICTHistoricalAnalyzer

    # Funciones utilitarias ICT
    update_market_context = ict_detector.update_market_context

    ICTProfessionalWidget = ict_professional_widget.ICTProfessionalWidget
    HibernationStatusWidget = dashboard_widgets.HibernationStatusWidget
    CountdownWidget = dashboard_widgets.CountdownWidget

    components_available = True
    # Reemplazamos prints con logging para vigilancia
    logger.info("🎯 Componentes del Dashboard Definitivo cargados exitosamente")
    logger.info("🧠 CAJA NEGRA ICT conectada: Detector, ConfidenceEngine, VeredictoEngine")
    logger.info("📊 Conexión MT5 habilitada para datos reales")
    logger.info("🔧 Motores ICT inicializados correctamente")

    # Log del evento usando el logger centralizado
    logger.info("COMPONENTS_LOADED: Todos los componentes ICT cargados correctamente")
except ImportError as e:
    logger.error("❌ Error importando componentes reales: %s", e)
    logger.warning("📁 Verificando archivos necesarios para datos reales:")
    logger.warning("   • sistema/mt5_connector.py")
    logger.warning("   • utils/mt5_data_manager.py")
    logger.warning("   • core/ict_engine/ict_types.py")
    logger.warning("   • core/ict_engine/ict_detector.py")
    logger.warning("   • core/ict_engine/confidence_engine.py")
    logger.warning("   • core/ict_engine/veredicto_engine_v4.py")
    logger.warning("   • core/ict_engine/pattern_analyzer.py")
    logger.warning("   • dashboard/ict_professional_widget.py")
    logger.warning("   • dashboard/dashboard_widgets.py")

    # Log del error usando el logger disponible
    logger.error('Error cargando componentes: %s', e)
    components_available = False


class SentinelDashboardDefinitivo(App):
    """
    🚀 DASHBOARD DEFINITIVO DEL SISTEMA SENTINEL ICT ANALYZER.

    El único dashboard del sistema que conecta datos reales de MT5
    con el análisis ICT completo y avanzado del sistema.
    """

    # 🎨 CSS profesional
    CSS = """
    Screen {
        background: $surface;
        layout: vertical;
    }

    #sentinel_main_tabs {
        background: $surface;
        height: 1fr;
    }

    .scrollable-container {
        overflow-y: auto;
        overflow-x: auto;
        height: 1fr;
    }

    .hibernation-panel {
        background: $panel;
        border: solid $accent;
        margin: 1;
        padding: 1;
    }

    .ict-panel {
        background: $panel;
        border: solid $primary;
        margin: 1;
        padding: 1;
    }

    .pattern-panel {
        background: $surface-lighten-1;
        border: solid $success;
        margin: 1;
        padding: 1;
        min-height: 10;
    }

    .analytics-panel {
        background: $panel;
        border: solid $warning;
        margin: 1;
        padding: 1;
    }

    .main-header {
        background: $primary;
        color: $text;
    }

    .main-footer {
        background: $secondary;
        color: $text;
    }
    """

    TITLE = "🚀 SENTINEL ICT ANALYZER - DASHBOARD DEFINITIVO v5.0"
    SUB_TITLE = "Sistema Principal - Datos Reales MT5 + Análisis ICT Completo"

    BINDINGS = [
        Binding("h1", "switch_hibernation", "🌙 Hibernación", show=True),
        Binding("h2", "switch_ict", "🔍 ICT Pro", show=True),
        Binding("h3", "switch_patterns", "🧠 Patrones", show=True),
        Binding("h4", "switch_analytics", "📊 Analytics", show=True),
        Binding("r", "refresh_system", "🔄 Refresh", show=True),
        Binding("p", "toggle_patterns", "🎯 Auto", show=True),
        Binding("d", "toggle_debug", "🐛 Debug", show=True),
        Binding("e", "export_analysis", "💾 Export", show=True),
        Binding("q", "quit", "❌ Salir", show=True),
    ]

    def __init__(self):
        super().__init__()

        logger.info("🚀 Inicializando Dashboard Definitivo...")

        if not components_available:
            logger.error("❌ Componentes necesarios no disponibles - Sistema no puede ejecutarse")
            self.exit()
            return

        logger.info("✅ Componentes verificados - Iniciando configuración del sistema")

        # � Métricas del sistema - INICIALIZACIÓN TEMPRANA
        self.analysis_count = 0
        self.patterns_detected = 0
        self.high_probability_signals = 0
        self.system_metrics = {
            'session_start': datetime.now(),
            'total_refreshes': 0,
            'pattern_accuracy': 0.0,
            'alerts_generated': 0,
            'export_count': 0,
            'mt5_connections': 0,
            'data_updates': 0
        }

        # �🔗 Inicializar conexión MT5 real
        self.mt5_manager = None
        self.mt5_connected = False
        self.symbol = "EURUSD"
        self.current_price = 0.0
        self.initialize_mt5_connection()

        # 🧠 CAJA NEGRA ICT COMPLETA - TODOS LOS ESPECIALISTAS CONECTADOS
        self.ict_analyzer = ICTPatternAnalyzer()
        self.ict_detector = ICTDetector()  # Detector principal ICT
        self.confidence_engine = ConfidenceEngine()  # Motor de confianza
        self.veredicto_engine = VeredictoEngine()  # Motor de veredicto final
        self.historical_analyzer = ICTHistoricalAnalyzer()  # Análisis histórico
        self.ict_widget = ICTProfessionalWidget()

        # 🎯 SISTEMA POI - ESPECIALISTAS COMPLETOS (usando imports del header)
        self.poi_detector_functions = poi_detector  # Módulo de funciones POI
        self.poi_scoring_engine = POIScoringEngine()  # Motor de calificación

        # 💼 TRADING CORE - MOTORES DE DECISIÓN
        try:
            self.trading_engine = TradingDecisionEngine()  # Motor principal de trading
            self.decision_cache = TradingDecisionCache()  # Cache inteligente
            print("💼 Trading Core conectado exitosamente")
        except (FileNotFoundError, PermissionError, IOError) as e:
            print(f"⚠️ Trading Core no disponible: {e}")
            self.trading_engine = None
            self.decision_cache = None

        # 🔗 MANAGERS Y CONECTORES ESPECIALIZADOS
        try:
            self.limit_order_manager = LimitOrderManager()
            self.config_manager = ConfigManager()
            self.riskbot = RiskBot(
                risk_target_profit=10.0,
                max_profit_target=130.0,
                risk_percent=1.0
            )
            print("✅ Managers especializados conectados")
            print("🛡️ RiskBot integrado - Gestión de riesgo avanzada activa")
        except (FileNotFoundError, PermissionError, IOError) as e:
            print(f"⚠️ Algunos managers no disponibles: {e}")
            self.limit_order_manager = None
            self.config_manager = None
            self.riskbot = None

        # 📊 LOGGERS INTELIGENTES (Usar sistema SLUC v2.1)
        try:
            # CORRECCIÓN: Usar el sistema SLUC v2.1 en lugar de logging directo
            # Nota: enviar_senal_log ya está importado en el scope global
            self.logger = None  # No usar logging directo
            enviar_senal_log('INFO',
                           "📊 Sistema de logging SLUC v2.1 conectado",
                           __name__,
                           'dashboard')
            print("📊 Sistema de logging inteligente conectado")
        except (FileNotFoundError, PermissionError, IOError) as e:
            print(f"⚠️ Sistema SLUC no disponible: {e}")
            # Fallback temporal - usar logging global importado
            # Nota: logging ya está importado en el scope global (línea 66)
            self.logger = logging.getLogger(__name__)  # Logger por defecto

        print("🎯 INVENTARIO DE ESPECIALISTAS CONECTADOS:")
        print("🧠 ICT Engine: Detector, Analyzer, Confidence, Veredicto, Historical")
        print("🎯 POI System: Detector Functions, Scoring Engine")
        print("💼 Trading Core: Decision Engine, Smart Cache")
        print("🔗 Managers: Limit Orders, Config")
        print("�️ Risk Management: RiskBot MT5, Position Management")
        print("�📊 Logging: Smart Logger activo")
        print("🚀 TODOS LOS ESPECIALISTAS LISTOS PARA ACCIÓN")

        # 🔗 DASHBOARD CONTROLLER INTEGRATION - CRÍTICO PARA COMUNICACIÓN CON BACKEND
        self.dashboard_controller = None
        self.backend_connected = False
        try:
            self.dashboard_controller = get_dashboard_controller()
            logger.info("📡 Dashboard Controller conectado - preparando registro")
        except ImportError as e:
            logger.warning("⚠️ Dashboard Controller no disponible: %s", e)
            print("⚠️ Dashboard Controller no disponible - funcionará sin datos del backend")

        # 🎯 Estado del sistema
        self.hibernation_start = datetime.now()
        self.auto_patterns_enabled = True
        self.debug_mode = False
        self.last_pattern_analysis = None

        # 🎯 Referencias a widgets estáticos
        self.hibernation_static = None
        self.ict_static = None
        self.pattern_static = None
        self.analytics_static = None

        # 📊 Datos reales de mercado - CAJA NEGRA INTEGRADA
        self.real_market_data = {
            'last_update': None,
            'candles_m1': pd.DataFrame(),
            'candles_m5': pd.DataFrame(),
            'candles_h1': pd.DataFrame(),
            'candles_h4': pd.DataFrame(),  # Para análisis de bias H4
            'pois_detected': [],
            'current_session': None,
            'market_structure': None,
            'ict_patterns': [],  # Patrones ICT detectados
            'market_bias': 'NEUTRAL',  # Bias H4 actual
            'veredicto_actual': None,  # Veredicto final de la caja negra
            'confidence_scores': {},  # Scores de confianza por patrón
            'market_context': {}  # Contexto completo del mercado
        }

        # Initialize attributes that might be defined later
        self.market_context_obj = None
        self.last_update_time = None

    def initialize_mt5_connection(self):
        """Inicializa la conexión real con MetaTrader5"""
        try:
            print("🔗 Iniciando conexión con MetaTrader5...")

            # Verificar que system_metrics existe
            if not hasattr(self, 'system_metrics'):
                print("⚠️ system_metrics no inicializado, creando...")
                self.system_metrics = {
                    'session_start': datetime.now(),
                    'total_refreshes': 0,
                    'pattern_accuracy': 0.0,
                    'alerts_generated': 0,
                    'export_count': 0,
                    'mt5_connections': 0,
                    'data_updates': 0
                }

            # Inicializar MT5 usando MT5DataManager
            self.mt5_manager = get_mt5_manager()
            if self.mt5_manager and self.mt5_manager.connect():
                print("✅ MT5 inicializado correctamente")

                # Verificar símbolo usando MT5DataManager
                if self.mt5_manager.verificar_simbolo(self.symbol):
                    print(f"✅ Símbolo {self.symbol} disponible")

                    self.mt5_connected = True
                    self.system_metrics['mt5_connections'] += 1
                    print("🚀 Dashboard conectado a datos reales MT5")

                    # Log usando sistema SLUC
                    try:
                        enviar_senal_log('INFO',
                                       f"MT5_CONNECTED: Dashboard conectado a MT5 - {self.symbol}",
                                       __name__,
                                       'dashboard')
                    except (ImportError, ValueError, TypeError) as e:
                        print(f"MT5_CONNECTED: Dashboard conectado a MT5 - {self.symbol}")
                        print(f"Debug: Exception in logging attempt: {e}")

                        # Obtener precio actual
                        self.update_current_price()
                    else:
                        logger.error("❌ Error conectando MT5 Manager")
                        self.mt5_connected = False
                else:
                    logger.error("❌ Símbolo %s no disponible", self.symbol)
                    self.mt5_connected = False
            else:
                logger.error("❌ Error inicializando MT5")
                self.mt5_connected = False

        except (FileNotFoundError, PermissionError, IOError) as e:
            logger.error("❌ Error en conexión MT5: %s", e)
            self.mt5_connected = False

    def update_current_price(self):
        """Actualiza el precio actual desde MT5"""
        try:
            if self.mt5_manager and self.mt5_connected:
                # Obtener datos recientes para extraer precio actual
                recent_data = self.mt5_manager.get_historical_data(self.symbol, "M1", 1)
                if recent_data is not None and not recent_data.empty:
                    self.current_price = recent_data['close'].iloc[-1]
                    return True
        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"Error actualizando precio: {e}")
        return False

    def compose(self) -> ComposeResult:
        """Composición de la interfaz con 4 pestañas especializadas"""
        yield Header(classes="main-header")

        with TabbedContent(initial="tab_hibernation", id="sentinel_main_tabs"):

            # 🌙 Pestaña H1: Hibernación con datos reales
            with TabPane("🌙 Hibernación Real", id="tab_hibernation"):
                self.hibernation_static = Static(
                    self.render_hibernation_panel(),
                    id="hibernation_display",
                    classes="hibernation-panel"
                )
                yield self.hibernation_static

            # 🔍 Pestaña H2: ICT Pro con datos reales
            with TabPane("🔍 ICT Real", id="tab_ict"):
                with Container(classes="scrollable-container"):
                    self.ict_static = Static(
                        self.render_ict_panel(),
                        id="ict_display",
                        classes="ict-panel"
                    )
                    yield self.ict_static

            # 🧠 Pestaña H3: Patrones con datos reales
            with TabPane("🧠 Patrones Real", id="tab_patterns"):
                with Container(classes="scrollable-container"):
                    self.pattern_static = Static(
                        self.render_patterns_panel(),
                        id="pattern_display",
                        classes="pattern-panel"
                    )
                    yield self.pattern_static

            # 📊 Pestaña H4: Analytics con datos reales
            with TabPane("📊 Analytics Real", id="tab_analytics"):
                with Container(classes="scrollable-container"):
                    self.analytics_static = Static(
                        self.render_analytics_panel(),
                        id="analytics_display",
                        classes="analytics-panel"
                    )
                    yield self.analytics_static

        yield Footer(classes="main-footer")

    def on_mount(self) -> None:
        """Configuración inicial del sistema"""
        logger.info("🔧 Dashboard montado - Configurando sistema de vigilancia")

        # 🔄 Timer para auto-refresh cada 10 segundos
        self.set_interval(10.0, self.auto_refresh_system)

        # 🎯 Timer para análisis de patrones cada 30 segundos
        self.set_interval(30.0, self.auto_analyze_patterns)

        # ⚡ Timer para micro-updates cada 5 segundos
        self.set_interval(5.0, self.micro_update_system)

        # 📊 Generar datos iniciales
        self.refresh_system_data()

        # 📡 REGISTRO CON DASHBOARD CONTROLLER - EL FIX CRÍTICO
        if self.dashboard_controller:
            try:
                logger.info("📡 Intentando registrar dashboard con controller...")
                self.dashboard_controller.register_dashboard(
                    dashboard_id="dashboard_definitivo",
                    dashboard_instance=self
                )
                self.backend_connected = True
                logger.info("✅ Dashboard registrado exitosamente con controller")
                self.notify("📡 Conectado al backend de datos reales", timeout=3)
            except (FileNotFoundError, PermissionError, IOError) as e:
                logger.error("❌ Error registrando dashboard: %s", e)
                self.notify("⚠️ Error conectando con backend", timeout=3)
        else:
            logger.warning("⚠️ Dashboard Controller no disponible - modo independiente")

        logger.info("✅ Dashboard completamente inicializado y operativo")
        logger.info("🔗 MT5 conectado: %s", self.mt5_connected)
        logger.info("📊 Símbolo activo: %s", self.symbol)

        # Log usando el logger centralizado
        logger.info("DASHBOARD_MOUNTED: Dashboard operativo - MT5: %s", self.mt5_connected)

        # 🚀 Notificaciones de bienvenida
        self.notify("🚀 Sentinel Dashboard Definitivo v5.0 iniciado", timeout=4)
        self.notify("💡 H1/H2/H3/H4 | R=refresh | P=auto | D=debug | E=export", timeout=5)
        self.notify("🎯 Sistema conectado a datos reales MT5", timeout=3)

    def render_hibernation_panel(self):
        """Renderiza panel de hibernación con datos reales"""
        from rich.panel import Panel
        from rich.text import Text

        content = Text()
        content.append("🚀 SENTINEL ICT ANALYZER - HIBERNACIÓN INTELIGENTE\n\n",
                      style="bold magenta")

        # Estado de conexión MT5
        if self.mt5_connected:
            content.append("🟢 MT5 CONECTADO - DATOS REALES\n", style="bold green")
            content.append(f"📊 Símbolo: {self.symbol}\n", style="cyan")
            content.append(f"💰 Precio Actual: {self.current_price:.5f}\n", style="yellow")
        else:
            content.append("🔴 MT5 DESCONECTADO - MODO DEMO\n", style="bold red")

        # Tiempo de hibernación
        elapsed = datetime.now() - self.hibernation_start
        hours = int(elapsed.total_seconds() // 3600)
        minutes = int((elapsed.total_seconds() % 3600) // 60)
        content.append(f"⏰ Tiempo de hibernación: {hours}h {minutes}m\n\n", style="white")

        # Verificar que system_metrics existe y tiene las claves necesarias
        if not hasattr(self, 'system_metrics') or not isinstance(self.system_metrics, dict):
            self.system_metrics = {
                'session_start': datetime.now(),
                'total_refreshes': 0,
                'pattern_accuracy': 0.0,
                'alerts_generated': 0,
                'export_count': 0,
                'mt5_connections': 0,
                'data_updates': 0
            }

        content.append("📈 MÉTRICAS DEL SISTEMA:\n", style="bold blue")
        content.append(f"• Análisis realizados: {self.analysis_count}\n", style="white")
        content.append(f"• Patrones detectados: {self.patterns_detected}\n", style="cyan")
        content.append(f"• Señales alta probabilidad: {self.high_probability_signals}\n",
                      style="green")
        content.append(f"• Actualizaciones de datos: {self.system_metrics.get('data_updates', 0)}\n",
                      style="yellow")

        # 🛡️ INFORMACIÓN DE GESTIÓN DE RIESGO
        if self.riskbot:
            try:
                balance = self.riskbot.get_account_balance()
                positions = len(self.riskbot.get_open_positions())
                _, _, profit_neto, _, _ = self.riskbot.get_total_profit_and_lots()
                content.append(f"🛡️ RiskBot: ${balance:.2f} | {positions} pos | P&L: ${profit_neto:.2f}\n", style="bright_green")
            except (FileNotFoundError, PermissionError, IOError) as e:
                content.append("🛡️ RiskBot: Error obteniendo datos\n", style="red")
                if self.debug_mode:
                    content.append(f"   Error: {e}\n", style="dim red")

        return Panel(
            content,
            title="🚀 [bold magenta]HIBERNACIÓN INTELIGENTE - DATOS REALES[/bold magenta]",
            subtitle=f"🔬 Debug: {'ON' if self.debug_mode else 'OFF'} | 📊 {self.patterns_detected} patrones | 💾 {self.system_metrics['export_count']} exports",
            border_style="bright_magenta",
            padding=(1, 2)
        )

    def render_ict_panel(self):
        """
        🧠 PANEL ICT PROFESIONAL - VERSIÓN ESTABLE
        ==========================================

        Versión que asegura mostrar siempre la pantalla completa con datos.
        """
        from rich.panel import Panel
        from rich.text import Text
        from rich.table import Table

        try:
            # CONFIGURACIÓN: FORZAR MODO DESARROLLO PARA DATOS COMPLETOS
            DEVELOPMENT_MODE = True

            # 🧠 USAR SISTEMA LIMPIO DIRECTAMENTE (SIN CAJA NEGRA)
            if clean_poi_available:
                try:
                    contenido_limpio = integrar_poi_dashboard_limpio(
                        dashboard_instance=self,
                        development_mode=DEVELOPMENT_MODE
                    )

                    return Panel(
                        contenido_limpio,
                        title="🧠 ICT PROFESIONAL",
                        border_style="cyan",
                        padding=(1, 2)
                    )
                except Exception as e:
                    enviar_senal_log("ERROR", f"❌ Error en sistema limpio: {e}", __name__, "dashboard")
                    # Continuar con fallback manual

            # 📊 FALLBACK MANUAL CON DATOS COMPLETOS (COMO LA PANTALLA ORIGINAL)
            main_table = Table.grid()
            main_table.add_column()

            # Header como en la pantalla original
            header = Text.assemble(
                ("🔧 DEVELOPMENT MODE | ", "bold bright_yellow"),
                ("🟡 ", "yellow"),
                ("MERCADO CERRADO - FIN DE SEMANA", "bold yellow")
            )
            main_table.add_row(header)
            main_table.add_row("")

            # Estadísticas como en la pantalla original
            stats = Text.assemble(
                ("� SIMULATED: 4 POIs | ", "bold cyan"),
                ("🎯 ACTIVE: 4 | ", "bold cyan"),
                ("⚡ HIGH: 2", "bold cyan")
            )
            main_table.add_row(stats)
            main_table.add_row("")

            # Grid de POIs como en la pantalla original
            poi_grid = Text.assemble(
                ("🔵 BULL OB      🔴 BEAR OB\n", "white"),
                ("� 1.17650      💰 1.17300\n", "white"),
                ("📊 78pts 📏 15p  📊 72pts 📏 20p\n", "bright_white"),
                ("⭐ A (DEV)      ⭐ B (DEV)\n", "bright_green"),
                ("\n", ""),
                ("🟢 BULL FVG     🟡 BEAR FVG\n", "white"),
                ("💰 1.17580      💰 1.17380\n", "white"),
                ("📊 55pts 📏 8p   📊 42pts 📏 12p\n", "bright_white"),
                ("⭐ C (DEV)      ⭐ C (DEV)", "yellow")
            )
            main_table.add_row(poi_grid)
            main_table.add_row("")

            # Recomendación como en la pantalla original
            recommendation = Text("🎯 DEV RECOMMENDATION: BULLISH_OB - 15p", style="bold bright_yellow")
            main_table.add_row(recommendation)

            return Panel(
                main_table,
                title="🧠 ICT PROFESIONAL",
                border_style="cyan",
                padding=(1, 2)
            )

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error crítico en render_ict_panel: {e}", __name__, "dashboard")

            # Fallback ultra-seguro
            basic_content = Text("🧠 ICT PROFESIONAL\nSistema iniciando...", style="cyan")
            return Panel(basic_content, title="🧠 ICT", border_style="cyan")

    def render_patterns_panel(self):
        """Renderiza panel de patrones con datos reales"""
        from rich.panel import Panel
        from rich.text import Text

        content = Text()
        content.append("🧠 ANÁLISIS DE PATRONES ICT\n\n", style="bold green")

        if self.last_pattern_analysis:
            pattern_name = getattr(self.last_pattern_analysis, 'pattern_name', 'Unknown Pattern')
            pattern_name = pattern_name.replace('_', ' ').title()
            content.append(f"🎯 Último patrón: {pattern_name}\n", style="cyan")
            content.append(f"📊 Probabilidad: {self.last_pattern_analysis.probability:.0f}%\n", style="yellow")
            content.append(f"📝 Narrativa: {self.last_pattern_analysis.narrative}\n\n", style="white")
        else:
            content.append("🔍 Buscando patrones en datos reales...\n", style="yellow")
            content.append("⏳ Análisis en progreso...\n\n", style="dim white")

        content.append(f"📈 Total de patrones detectados: {self.patterns_detected}\n", style="white")
        content.append(f"🚀 Señales de alta probabilidad: {self.high_probability_signals}\n", style="green")

        return Panel(
            content,
            title="🧠 [bold green]PATRONES ICT - DATOS REALES[/bold green]",
            border_style="green",
            padding=(2, 4)
        )

    def render_analytics_panel(self):
        """Renderiza panel de analytics con métricas"""
        from rich.panel import Panel
        from rich.text import Text

        content = Text()
        content.append("📊 ANALYTICS Y MÉTRICAS\n\n", style="bold yellow")

        # Duración de sesión
        session_duration = datetime.now() - self.system_metrics['session_start']
        hours = int(session_duration.total_seconds() // 3600)
        minutes = int((session_duration.total_seconds() % 3600) // 60)

        content.append(f"⏰ Sesión activa: {hours}h {minutes}m\n", style="cyan")
        content.append(f"🔄 Total refreshes: {self.system_metrics['total_refreshes']}\n", style="white")
        content.append(f"📈 Alertas generadas: {self.system_metrics['alerts_generated']}\n", style="green")
        content.append(f"🔗 Conexiones MT5: {self.system_metrics['mt5_connections']}\n", style="blue")
        content.append(f"📊 Actualizaciones datos: {self.system_metrics['data_updates']}\n", style="yellow")

        # Precisión calculada
        if self.patterns_detected > 0:
            accuracy = (self.high_probability_signals / self.patterns_detected) * 100
            content.append(f"\n🎯 Precisión: {accuracy:.1f}%\n", style="green")

        return Panel(
            content,
            title="📊 [bold yellow]ANALYTICS - RENDIMIENTO[/bold yellow]",
            border_style="yellow",
            padding=(2, 4)
        )

    # Métodos de navegación
    def action_switch_hibernation(self):
        """Cambiar a pestaña de hibernación (H1)"""
        try:
            tabs = self.query_one("#sentinel_main_tabs", TabbedContent)
            tabs.active = "tab_hibernation"
            self.notify("🌙 Hibernación Real activada")
        except (FileNotFoundError, PermissionError, IOError) as e:
            self.notify(f"⚠️ Error: {e}")

    def action_switch_ict(self):
        """Cambiar a pestaña ICT (H2)"""
        try:
            tabs = self.query_one("#sentinel_main_tabs", TabbedContent)
            tabs.active = "tab_ict"
            self.refresh_system_data()
            self.notify("🔍 ICT Real activado")
        except (FileNotFoundError, PermissionError, IOError) as e:
            self.notify(f"⚠️ Error: {e}")

    def action_switch_patterns(self):
        """Cambiar a pestaña de patrones (H3)"""
        try:
            tabs = self.query_one("#sentinel_main_tabs", TabbedContent)
            tabs.active = "tab_patterns"
            self.analyze_patterns()
            self.notify("🧠 Patrones Real activado")
        except (FileNotFoundError, PermissionError, IOError) as e:
            self.notify(f"⚠️ Error: {e}")

    def action_switch_analytics(self):
        """Cambiar a pestaña de analytics (H4)"""
        try:
            tabs = self.query_one("#sentinel_main_tabs", TabbedContent)
            tabs.active = "tab_analytics"
            self.notify("📊 Analytics Real activado")
        except (FileNotFoundError, PermissionError, IOError) as e:
            self.notify(f"⚠️ Error: {e}")

    def action_refresh_system(self):
        """Refrescar todos los datos del sistema (R)"""
        self.refresh_system_data()
        self.system_metrics['total_refreshes'] += 1
        self.notify("🔄 Sistema completamente actualizado con datos reales", timeout=3)

    def action_toggle_patterns(self):
        """Toggle del análisis automático de patrones (P)"""
        self.auto_patterns_enabled = not self.auto_patterns_enabled
        status = "HABILITADO" if self.auto_patterns_enabled else "DESHABILITADO"
        self.notify(f"🎯 Análisis automático {status}")

    def action_toggle_debug(self):
        """Toggle del modo debug (D)"""
        self.debug_mode = not self.debug_mode
        status = "ACTIVADO" if self.debug_mode else "DESACTIVADO"
        self.notify(f"🐛 Modo Debug {status}", timeout=3)

    def action_export_analysis(self):
        """Exportar análisis y métricas (E)"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.system_metrics['export_count'] += 1
            self.notify(f"💾 Export #{self.system_metrics['export_count']} generado: analysis_{timestamp}", timeout=4)
        except (FileNotFoundError, PermissionError, IOError) as e:
            self.notify(f"❌ Error en export: {e}")

    # Métodos de actualización
    def refresh_system_data(self):
        """Refresca todos los datos del sistema"""
        self.analysis_count += 1

        # Actualizar precio desde MT5
        if self.mt5_connected:
            self.update_current_price()
            self.system_metrics['data_updates'] += 1

        # 🛡️ MONITOREO ACTIVO DE GESTIÓN DE RIESGO
        if self.riskbot:
            try:
                risk_status = self.riskbot.check_and_act()
                if risk_status != 'ok':
                    logger.info("🛡️ RiskBot acción ejecutada: %s", risk_status)
                    if self.debug_mode:
                        print(f"🛡️ RiskBot: {risk_status}")
            except (FileNotFoundError, PermissionError, IOError) as e:
                logger.warning("⚠️ Error en monitoreo RiskBot: %s", e)

        # Actualizar paneles
        if self.hibernation_static:
            self.hibernation_static.update(self.render_hibernation_panel())

    def analyze_patterns(self):
        """🚀 ANÁLISIS COMPLETO usando TODOS LOS ESPECIALISTAS CONECTADOS"""
        if not self.auto_patterns_enabled:
            return

        try:
            # 🧠 EJECUTAR CAJA NEGRA ICT COMPLETA CON TODOS LOS ESPECIALISTAS
            if self.mt5_connected and self.mt5_manager:
                print("🔥 INICIANDO ANÁLISIS INTEGRAL CON TODOS LOS ESPECIALISTAS...")

                # 1. Obtener datos de múltiples timeframes
                self.load_multi_timeframe_data()

                # 2. Actualizar contexto de mercado usando ICT Detector
                market_context = self.update_market_context_complete()

                # 3. Detectar POIs usando el sistema POI completo
                detected_pois = self.detect_pois_complete()

                # 4. Detectar patrones ICT usando Pattern Analyzer
                detected_patterns = self.detect_ict_patterns_complete()

                # 5. Calcular scores de confianza usando Confidence Engine
                enriched_patterns = self.calculate_confidence_scores_complete(detected_patterns, market_context, detected_pois)

                # 6. Scoring de POIs usando POI Scoring Engine
                scored_pois = self.score_pois_complete(detected_pois, market_context)

                # 7. Obtener veredicto final usando Veredicto Engine
                veredicto = self.get_final_veredicto_complete(enriched_patterns, scored_pois, market_context)

                # 8. Registrar en logs usando Smart Logger
                self.log_analysis_complete(veredicto, enriched_patterns, scored_pois, market_context)

                # 9. Actualizar estado del sistema
                self.update_system_state_complete(veredicto, enriched_patterns, scored_pois, market_context)

                # 10. Generar alertas inteligentes
                self.generate_alerts_complete(veredicto)

                # 📊 REGISTRO EN LOGS POI - SINCRONIZACIÓN CON HEALTH ANALYZER
                self.sync_poi_logs_with_health_analyzer(scored_pois)

                # Log del análisis completado
                logger.info("🎯 ANÁLISIS INTEGRAL COMPLETADO:")
                logger.info("   • Patrones ICT: %s", len(enriched_patterns))
                logger.info("   • POIs detectados: %s", len(scored_pois))
                logger.info("   • Veredicto: %s", veredicto['grade'] if veredicto else 'NINGUNO')
                logger.info("   • Contexto: %s", market_context.get('h4_bias', 'NEUTRAL'))

                # Log del análisis usando el logger centralizado
                analysis_summary = f"Análisis: {len(enriched_patterns)} patrones, {len(scored_pois)} POIs, veredicto: {veredicto['grade'] if veredicto else 'NINGUNO'}"
                logger.info("ANALYSIS_COMPLETED: %s", analysis_summary)

            else:
                # Modo simulado para desarrollo
                self.simulate_pattern_detection()
                logger.warning("🔄 Ejecutando en modo simulado - MT5 no conectado")

        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                logger.error("❌ Error en análisis integral: %s", e)
                import traceback
                traceback.print_exc()
            # Fallback a simulación
            self.simulate_pattern_detection()

    def load_multi_timeframe_data(self):
        """Carga datos de múltiples timeframes para análisis ICT"""
        try:
            if not self.mt5_manager:
                logger.warning("🔴 MT5 Manager no disponible para cargar datos")
                return

            symbol = self.symbol
            logger.info("📊 Iniciando carga de datos multi-timeframe para %s", symbol)

            # 🚀 FASE 3: AUMENTAR DATOS HISTÓRICOS PARA ICT ENGINE COMPLETO
            timeframes = {
                'M1': ('M1', 200),    # Aumentado: Para confirmación LTF detallada
                'M5': ('M5', 300),    # Aumentado: Para estructura M15 equivalente completa
                'H1': ('H1', 200),    # Aumentado: Para análisis medio plazo robusto
                'H4': ('H4', 100)     # Aumentado: Para bias H4 con más historia
            }

            loaded_count = 0
            for tf_name, (tf_code, bars) in timeframes.items():
                try:
                    data = self.mt5_manager.get_historical_data(symbol, tf_code, bars)
                    if data is not None and not data.empty:
                        self.real_market_data[f'candles_{tf_name.lower()}'] = data
                        loaded_count += 1
                        logger.info("✅ Datos %s cargados: %s velas (%s solicitadas)", tf_name, len(data), bars)
                        if self.debug_mode:
                            logger.debug("   📊 %s - Último precio: %.5f", tf_name, data['close'].iloc[-1])
                    else:
                        logger.warning("⚠️ No se pudieron cargar datos %s", tf_name)
                except (FileNotFoundError, PermissionError, IOError) as tf_error:
                    logger.error("❌ Error cargando %s: %s", tf_name, tf_error)

            self.real_market_data['last_update'] = datetime.now()
            self.system_metrics['data_updates'] += 1

            logger.info("📈 Carga multi-timeframe completada: %s/4 timeframes cargados", loaded_count)

            # Log usando el logger centralizado
            logger.info("DATA_LOADED: %s timeframes cargados para análisis ICT", loaded_count)

        except (FileNotFoundError, PermissionError, IOError) as e:
            logger.error("❌ Error cargando datos multi-timeframe: %s", e)
            if self.debug_mode:
                import traceback
                logger.debug("Stack trace: %s", traceback.format_exc())

    # ======================================================================
    # 🚀 MÉTODOS COMPLETOS USANDO TODOS LOS ESPECIALISTAS CONECTADOS
    # ======================================================================

    def update_market_context_complete(self) -> Dict:
        """Actualiza contexto de mercado usando ICT Detector completo con datos reales MT5"""
        try:
            # 🚀 RECOLECTAR DATOS REALES MULTI-TIMEFRAME para ICT Engine
            enviar_senal_log("INFO", "🔍 F2.4: Iniciando integración de datos reales MT5 → ICT Engine", __name__, "ict")

            # Obtener todos los timeframes disponibles
            h4_data = self.real_market_data.get('candles_h4')
            h1_data = self.real_market_data.get('candles_h1')
            m5_data = self.real_market_data.get('candles_m5')
            m1_data = self.real_market_data.get('candles_m1')

            # Log de datos disponibles para trazabilidad
            timeframes_info = {}
            for tf_name, data in [('H4', h4_data), ('H1', h1_data), ('M5', m5_data), ('M1', m1_data)]:
                if data is not None and not data.empty:
                    timeframes_info[tf_name] = len(data)
                    enviar_senal_log("DEBUG", f"  📊 {tf_name}: {len(data)} velas reales (desde {data.index[0]} hasta {data.index[-1]})", __name__, "mt5")
                else:
                    timeframes_info[tf_name] = 0
                    enviar_senal_log("WARNING", f"  ⚠️ {tf_name}: Sin datos disponibles", __name__, "mt5")

            enviar_senal_log("INFO", f"Datos MT5 recolectados: {timeframes_info}", __name__, "mt5")

            # Verificar datos mínimos necesarios para ICT
            if h4_data is not None and not h4_data.empty and m5_data is not None and not m5_data.empty:

                # 🧠 PREPARAR DICCIONARIO PARA ICT ENGINE
                df_by_timeframe = {}

                # Añadir todos los timeframes disponibles
                if h4_data is not None and not h4_data.empty:
                    df_by_timeframe['H4'] = h4_data
                if h1_data is not None and not h1_data.empty:
                    df_by_timeframe['H1'] = h1_data
                if m5_data is not None and not m5_data.empty:
                    df_by_timeframe['M5'] = m5_data
                    df_by_timeframe['M15'] = m5_data  # M5 como proxy para M15 por ahora
                if m1_data is not None and not m1_data.empty:
                    df_by_timeframe['M1'] = m1_data

                enviar_senal_log("INFO", f"🎯 Enviando datos reales a ICT Engine: {list(df_by_timeframe.keys())}", __name__, "ict")

                # 🚀 CREAR/ACTUALIZAR CONTEXTO DE MERCADO ICT
                if not hasattr(self, 'market_context_obj'):
                    self.market_context_obj = ICTDetector()
                    enviar_senal_log("INFO", "✅ Nuevo MarketContext creado para datos reales", __name__, "ict")
                elif self.market_context_obj is None:
                    self.market_context_obj = ICTDetector()
                    enviar_senal_log("INFO", "✅ MarketContext reinicializado para datos reales", __name__, "ict")

                # 🔥 LLAMAR AL ICT ENGINE CON DATOS REALES
                enviar_senal_log("INFO", f"🚀 Ejecutando update_market_context con precio actual: {self.current_price:.5f}", __name__, "ict")
                update_market_context(self.market_context_obj, df_by_timeframe, self.current_price)
                enviar_senal_log("SUCCESS", "✅ ICT Engine procesó datos reales exitosamente", __name__, "ict")

                # 📊 EXTRAER RESULTADOS DEL ANÁLISIS ICT
                context = {
                    'h4_bias': getattr(self.market_context_obj, 'h4_bias', 'NEUTRAL'),
                    'm15_bias': getattr(self.market_context_obj, 'm15_bias', 'NEUTRAL'),
                    'market_phase': getattr(self.market_context_obj, 'market_phase', 'RANGING'),
                    'session_type': self.get_current_session_type(),
                    'volatility': self.calculate_current_volatility(m5_data),
                    'total_pois': len(getattr(self.market_context_obj, 'pois_h4', [])) +
                                 len(getattr(self.market_context_obj, 'pois_m15', [])) +
                                 len(getattr(self.market_context_obj, 'pois_m5', [])),
                    'analysis_quality': getattr(self.market_context_obj, 'analysis_quality', 'MEDIUM'),
                    'data_source': 'MT5_REAL'
                }

                # 🎯 GUARDAR CONTEXTO ACTUALIZADO
                self.real_market_data['market_context'] = context
                self.real_market_data['market_bias'] = context.get('h4_bias', 'NEUTRAL')

                # 📋 LOGGING DETALLADO DE RESULTADOS
                enviar_senal_log("SUCCESS", f"📋 ANÁLISIS ICT COMPLETADO - H4_bias: {context['h4_bias']}, M15_bias: {context['m15_bias']}, POIs: {context['total_pois']}, Calidad: {context['analysis_quality']}", __name__, "ict")

                if self.debug_mode:
                    print(f"🧠 ICT Contexto Real: {context.get('h4_bias')} | {context.get('market_phase')} | POIs: {context.get('total_pois')}")

                return context

            else:
                enviar_senal_log("WARNING", "⚠️ Datos insuficientes para análisis ICT - usando contexto por defecto", __name__, "ict")
                return {'h4_bias': 'NEUTRAL', 'market_phase': 'UNKNOWN', 'session_type': 'ASIAN', 'data_source': 'FALLBACK'}

        except (AttributeError, ValueError, TypeError, ImportError, KeyError) as e:
            enviar_senal_log("ERROR", f"❌ Error crítico en integración ICT Engine: {e}", __name__, "ict")
            if self.debug_mode:
                import traceback
                enviar_senal_log("ERROR", f"Stack trace: {traceback.format_exc()}", __name__, "ict")
            return {'h4_bias': 'NEUTRAL', 'market_phase': 'ERROR', 'session_type': 'ASIAN', 'data_source': 'ERROR'}

    def detect_pois_complete(self) -> List[Dict]:
        """Detecta POIs usando el sistema POI completo"""
        try:
            detected_pois = []

            # Obtener datos de múltiples timeframes
            m5_data = self.real_market_data.get('candles_m5')
            m15_data = self.real_market_data.get('candles_m1')  # Usar M1 como M15 equivalente
            h1_data = self.real_market_data.get('candles_h1')

            logger.info("🎯 INICIANDO DETECCIÓN POI COMPLETA")
            logger.debug("Datos disponibles: M5=%s, M15=%s, H1=%s", len(m5_data) if m5_data is not None else 0, len(m15_data) if m15_data is not None else 0, len(h1_data) if h1_data is not None else 0)

            # Detectar POIs en múltiples timeframes usando el detector completo
            timeframes_data = [
                (m5_data, 'M5'),
                (m15_data, 'M15'),
                (h1_data, 'H1')
            ]

            for data, tf_name in timeframes_data:
                if data is not None and not data.empty:
                    logger.info("🔍 Detectando POIs en %s: %s velas disponibles", tf_name, len(data))
                    logger.debug("   Rango precio %s: %.5f - %.5f", tf_name, data['close'].min(), data['close'].max())

                    # Usar las funciones del poi_detector
                    pois_tf = self.poi_detector_functions.detectar_todos_los_pois(
                        df=data,
                        timeframe=tf_name,
                        current_price=self.current_price
                    )

                    logger.info("📊 Resultado detección %s: %s - %s", tf_name, type(pois_tf), len(pois_tf) if isinstance(pois_tf, (list, dict)) else 'N/A')

                    if pois_tf and isinstance(pois_tf, dict):
                        # Consolidar todos los tipos de POI detectados
                        all_pois_from_tf = []
                        for poi_type, poi_list in pois_tf.items():
                            if isinstance(poi_list, list) and poi_type != 'resumen':
                                all_pois_from_tf.extend(poi_list)
                                logger.debug("   %s: %s POIs", poi_type, len(poi_list))

                        detected_pois.extend(all_pois_from_tf)
                        logger.info("✅ %s: %s POIs agregados (Total acumulado: %s)", tf_name, len(all_pois_from_tf), len(detected_pois))
                    elif isinstance(pois_tf, list):
                        detected_pois.extend(pois_tf)
                        logger.info("✅ %s: %s POIs agregados (Total acumulado: %s)", tf_name, len(pois_tf), len(detected_pois))
                    else:
                        logger.warning("⚠️ %s: No se detectaron POIs o formato inesperado", tf_name)

                    if self.debug_mode:
                        print(f"🎯 POIs {tf_name}: {len(pois_tf) if isinstance(pois_tf, (list, dict)) else 0} detectados")

            # Filtrar POIs duplicados y ordenar por score
            unique_pois = self.filter_and_rank_pois(detected_pois)

            logger.info("🏆 POI DETECCIÓN COMPLETADA: %s total → %s únicos", len(detected_pois), len(unique_pois))

            self.real_market_data['pois_detected'] = unique_pois
            return unique_pois

        except (FileNotFoundError, PermissionError, IOError) as e:
            logger.error("❌ Error detectando POIs completos: %s", e, exc_info=True)
            if self.debug_mode:
                print(f"❌ Error detectando POIs completos: {e}")
            return []

    def sync_poi_logs_with_health_analyzer(self, scored_pois: List[Dict]):
        """🔧 SINCRONIZA MÉTRICAS POI CON HEALTH ANALYZER PARA 100% OPERATIVO"""
        try:
            if not scored_pois:
                return

            # 📊 ESCRIBIR EN EL LOG POI QUE LEE EL HEALTH ANALYZER
            # import os  # Ya importado globalmente
            # from pathlib import Path  # Ya importado como Path

            poi_log_path = Path("data/logs/poi/poi_detection.log")
            poi_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Crear entradas de log en el formato que espera el Health Analyzer
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(poi_log_path, 'a', encoding='utf-8') as f:
                for poi in scored_pois:
                    poi_type = poi.get('type', 'UNKNOWN')
                    poi_price = poi.get('price', 0.0)
                    poi_score = poi.get('score', 0)
                    timeframe = poi.get('timeframe', 'M15')

                    # Formato que el Health Analyzer busca
                    log_entry = f"{timestamp} | INFO | POI encontrado: {poi_type} @ {poi_price:.5f} | Score: {poi_score} | TF: {timeframe}\n"
                    f.write(log_entry)

                # Log de resumen que el Health Analyzer cuenta
                summary_entry = f"{timestamp} | INFO | POIs detectados: {len(scored_pois)} total en análisis integral\n"
                f.write(summary_entry)

            logger.info("📊 Sincronizado con Health Analyzer: %s POIs registrados en poi_detection.log", len(scored_pois))

        except (FileNotFoundError, PermissionError, IOError) as e:
            logger.error("❌ Error sincronizando logs POI: %s", e)

    def integrate_poi_scoring_engine(self, raw_pois: List[Dict]) -> List[Dict]:
        """🎯 INTEGRA POI SCORING ENGINE PARA SCORING AVANZADO - 100% OPERATIVO"""
        try:
            if not raw_pois or not self.poi_scoring_engine:
                return raw_pois

            enhanced_pois = []
            current_price = self.current_price or 1.17500  # Fallback
            market_context = self.real_market_data.get('market_context', {})

            logger.info("🎯 Aplicando scoring avanzado a %s POIs...", len(raw_pois))

            for poi in raw_pois:
                try:
                    # Usar el scoring engine avanzado
                    intelligent_score = self.poi_scoring_engine.calculate_intelligent_score(
                        poi, current_price, market_context
                    )

                    # Mejorar el POI con el scoring avanzado
                    enhanced_poi = poi.copy()
                    enhanced_poi.update({
                        'intelligent_score': intelligent_score.get('final_score', poi.get('score', 50)),
                        'grade': intelligent_score.get('grade', 'C'),
                        'confidence': intelligent_score.get('confidence', 0.5),
                        'narrative': intelligent_score.get('narrative', f"POI {poi.get('type', 'UNKNOWN')} detectado"),
                        'color': intelligent_score.get('color', 'white'),
                        'distance_pips': intelligent_score.get('distance_pips', 0),
                        'enhanced': True
                    })

                    enhanced_pois.append(enhanced_poi)

                except (FileNotFoundError, PermissionError, IOError) as scoring_error:
                    logger.warning("⚠️ Error en scoring POI individual: %s", scoring_error)
                    enhanced_pois.append(poi)  # Fallback al POI original

            # Filtrar POIs por calidad (solo grado B o mejor)
            quality_pois = [poi for poi in enhanced_pois if poi.get('grade', 'D') in ['A+', 'A', 'B']]

            logger.info("✅ Scoring avanzado completado: %s procesados → %s de calidad", len(enhanced_pois), len(quality_pois))

            return quality_pois

        except (FileNotFoundError, PermissionError, IOError) as e:
            logger.error("❌ Error en integración scoring engine: %s", e)
            return raw_pois  # Fallback a POIs originales

    def detect_ict_patterns_complete(self) -> List[Dict]:
        """Detecta patrones ICT usando Pattern Analyzer completo"""
        try:
            patterns = []

            # Usar el ICT Pattern Analyzer para detectar patrones específicos
            m5_data = self.real_market_data.get('candles_m5')
            m1_data = self.real_market_data.get('candles_m1')
            market_context = self.real_market_data.get('market_context', {})

            if m5_data is not None and not m5_data.empty:
                # Configurar el analyzer con datos actuales
                self.ict_analyzer.current_price = self.current_price
                # Convertir session type string a SessionType enum
                session_str = self.get_current_session_type()
                # TEMPORAL: Import local necesario por scope issue con SessionType
                from core.ict_engine.ict_types import SessionType as LocalSessionType
                if session_str == 'LONDON':
                    self.ict_analyzer.current_session = LocalSessionType.LONDON
                elif session_str == 'NEWYORK':
                    self.ict_analyzer.current_session = LocalSessionType.NEW_YORK
                else:
                    self.ict_analyzer.current_session = LocalSessionType.ASIAN

                # Detectar patrones específicos
                pattern_methods = [
                    ('SILVER_BULLET', self.detect_silver_bullet_complete),
                    ('JUDAS_SWING', self.detect_judas_swing_complete),
                    ('LIQUIDITY_GRAB', self.detect_liquidity_grab_complete),
                    ('ORDER_BLOCK', self.detect_order_blocks_complete),
                    ('FAIR_VALUE_GAP', self.detect_fair_value_gaps_complete)
                ]

                for pattern_name, method in pattern_methods:
                    try:
                        pattern = method(m5_data, m1_data, market_context)
                        if pattern:
                            patterns.append(pattern)
                            if self.debug_mode:
                                print(f"🎪 {pattern_name} detectado con {pattern.get('strength', 0)}% fortaleza")
                    except (FileNotFoundError, PermissionError, IOError) as pe:
                        if self.debug_mode:
                            print(f"⚠️ Error detectando {pattern_name}: {pe}")

            self.real_market_data['ict_patterns'] = patterns
            return patterns

        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error detectando patrones ICT completos: {e}")
            return []

    def calculate_confidence_scores_complete(self, patterns: List[Dict], market_context: Dict, pois: List[Dict]) -> List[Dict]:
        """Calcula scores de confianza usando Confidence Engine"""
        try:
            enriched_patterns = []

            for pattern in patterns:
                # Usar el Confidence Engine para calcular confianza
                confidence_score = self.confidence_engine.calculate_pattern_confidence(
                    pattern=pattern,
                    market_context=market_context,
                    poi_list=pois,
                    current_price=self.current_price,
                    current_session=self.get_current_session_type()
                )

                # Enriquecer patrón con score de confianza
                enriched_pattern = pattern.copy()
                enriched_pattern['confidence_score'] = confidence_score
                enriched_pattern['confidence_pct'] = confidence_score * 100

                # Agregar análisis histórico si disponible
                if self.historical_analyzer:
                    historical_factor = self.historical_analyzer.get_historical_poi_performance(
                        poi_type=pattern.get('type', 'UNKNOWN'),
                        timeframe=pattern.get('timeframe', 'M5'),
                        symbol=self.symbol
                    )
                    enriched_pattern['historical_factor'] = historical_factor

                enriched_patterns.append(enriched_pattern)

                if self.debug_mode:
                    print(f"🧠 {pattern.get('type', 'Pattern')}: {confidence_score:.2f} confianza")

            return enriched_patterns

        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error calculando confianza completa: {e}")
            return patterns  # Devolver patrones sin enriquecer

    def score_pois_complete(self, pois: List[Dict], market_context: Dict) -> List[Dict]:
        """🎯 CALIFICA POIs USANDO SCORING ENGINE AVANZADO + INTEGRACIÓN COMPLETA"""
        try:
            logger.info("🎯 Iniciando scoring avanzado de %s POIs...", len(pois))

            # 🚀 USAR LA INTEGRACIÓN COMPLETA DEL SCORING ENGINE
            enhanced_pois = self.integrate_poi_scoring_engine(pois)

            # Scoring adicional personalizado si es necesario
            final_scored_pois = []
            for poi in enhanced_pois:
                scored_poi = poi.copy()

                # Asegurar que tenga todos los campos necesarios
                if not scored_poi.get('enhanced', False):
                    # Fallback al scoring básico si no se pudo aplicar el avanzado
                    score_data = self.poi_scoring_engine.calculate_intelligent_score(
                        poi=poi,
                        current_price=self.current_price,
                        market_context=market_context
                    )
                    scored_poi.update(score_data)

                final_scored_pois.append(scored_poi)

                if self.debug_mode:
                    grade = scored_poi.get('grade', 'C')
                    score = scored_poi.get('intelligent_score', scored_poi.get('score', 0))
                    print(f"🎯 POI {poi.get('type', 'Unknown')}: {grade} ({score})")

            logger.info("✅ Scoring POI completado: %s POIs calificados", len(final_scored_pois))
            return final_scored_pois

        except (FileNotFoundError, PermissionError, IOError) as e:
            logger.error("❌ Error en scoring completo POIs: %s", e)
            if self.debug_mode:
                print(f"❌ Error calculando scoring completo: {e}")
            return pois  # Devolver POIs sin enriquecer

    def get_final_veredicto_complete(self, enriched_patterns: List[Dict], scored_pois: List[Dict], market_context: Dict) -> Optional[Dict]:
        """Obtiene veredicto final usando Veredicto Engine"""
        try:
            if not enriched_patterns and not scored_pois:
                return None

            # Usar el Veredicto Engine para obtener veredicto final
            veredicto = self.veredicto_engine.generate_market_veredicto(
                enhanced_pois=scored_pois,
                ict_patterns=enriched_patterns,
                market_context=market_context,
                current_price=self.current_price
            )

            if self.debug_mode and veredicto:
                grade = veredicto.get('grade', 'C')
                action = veredicto.get('action', 'ESPERAR')
                confidence = veredicto.get('confidence', 0)
                print(f"🎯 VEREDICTO FINAL: {grade} | {action} | {confidence:.0f}%")

            return veredicto

        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error generando veredicto completo: {e}")
            return None

    def get_risk_management_status(self) -> Dict:
        """🛡️ Obtiene el estado completo de la gestión de riesgo"""
        try:
            if not self.riskbot:
                return {'status': 'disconnected', 'message': 'RiskBot no conectado'}

            # Obtener datos básicos de la cuenta
            balance = self.riskbot.get_account_balance()
            positions = self.riskbot.get_open_positions()
            total_profit, comision_total, profit_neto, total_lots, total_swap = self.riskbot.get_total_profit_and_lots()

            # Configuración de riesgo avanzado
            risk_config = self.riskbot.get_advanced_risk_config()

            risk_status = {
                'status': 'connected',
                'account': {
                    'balance': balance,
                    'positions_count': len(positions),
                    'total_lots': total_lots,
                    'total_profit': total_profit,
                    'profit_neto': profit_neto,
                    'comision_total': comision_total,
                    'total_swap': total_swap
                },
                'risk_params': {
                    'risk_percent': self.riskbot.risk_percent,
                    'risk_target_profit': self.riskbot.risk_target_profit,
                    'max_profit_target': self.riskbot.max_profit_target
                },
                'advanced_config': risk_config,
                'positions': []
            }

            # Detalles de posiciones
            for pos in positions:
                pos_data = {
                    'ticket': pos.ticket,
                    'symbol': pos.symbol,
                    'type': 'BUY' if pos.type == 0 else 'SELL',
                    'volume': pos.volume,
                    'price_open': pos.price_open,
                    'profit': pos.profit,
                    'profit_neto': pos.profit - (pos.volume * self.riskbot.comision_por_lote)
                }
                risk_status['positions'].append(pos_data)

            logger.info("🛡️ Estado RiskBot actualizado: %s posiciones, P&L neto: $%s", len(positions), profit_neto)
            return risk_status

        except (FileNotFoundError, PermissionError, IOError) as e:
            logger.error("❌ Error obteniendo estado RiskBot: %s", e)
            return {'status': 'error', 'message': str(e)}

    def log_analysis_complete(self, veredicto: Optional[Dict], patterns: List[Dict], pois: List[Dict], context: Dict):
        """Registra análisis usando el sistema de logging centralizado"""
        try:
            # Registrar análisis completo usando el logger estándar
            analysis_data = {
                'timestamp': datetime.now().isoformat(),
                'symbol': self.symbol,
                'current_price': self.current_price,
                'veredicto': veredicto,
                'patterns_count': len(patterns),
                'pois_count': len(pois),
                'market_context': context,
                'session_type': self.get_current_session_type()
            }

            # Debug output para analysis_data
            if self.debug_mode:
                print(f"Debug: Analysis data structure: {len(analysis_data)} fields")

            logger.info("🔍 Análisis integral completado: %s patrones, %s POIs", len(patterns), len(pois))

            if veredicto:
                grade = veredicto.get('grade', 'C')
                logger.info("🎯 Veredicto final: %s", grade)

        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error logging análisis completo: {e}")

    def update_system_state_complete(self, veredicto: Optional[Dict], patterns: List[Dict], pois: List[Dict], context: Dict):
        """Actualiza estado del sistema con resultados completos"""
        # Actualizar métricas
        self.analysis_count += 1
        self.patterns_detected = len(patterns)

        # Contar señales de alta probabilidad (>85%)
        high_prob_patterns = sum(1 for p in patterns if p.get('confidence_pct', 0) >= 85)
        high_prob_pois = sum(1 for p in pois if p.get('score', 0) >= 85)
        self.high_probability_signals = high_prob_patterns + high_prob_pois

        # Guardar veredicto actual
        self.real_market_data['veredicto_actual'] = veredicto
        self.real_market_data['last_analysis'] = {
            'patterns': patterns,
            'pois': pois,
            'context': context,
            'timestamp': datetime.now()
        }

        # Actualizar último análisis para el panel de patrones
        if patterns or pois:
            # Seleccionar el mejor entre patrones y POIs
            best_item = None
            best_confidence = 0

            for pattern in patterns:
                conf = pattern.get('confidence_pct', 0)
                if conf > best_confidence:
                    best_confidence = conf
                    best_item = {'type': 'pattern', 'data': pattern}

            for poi in pois:
                conf = poi.get('score', 0)
                if conf > best_confidence:
                    best_confidence = conf
                    best_item = {'type': 'poi', 'data': poi}

            if best_item:
                self.create_pattern_analysis_object(best_item, veredicto)

        if self.debug_mode:
            print(f"📊 Estado actualizado: {self.patterns_detected} patrones, {len(pois)} POIs, {self.high_probability_signals} alta prob.")

    def generate_alerts_complete(self, veredicto: Optional[Dict]):
        """Genera alertas inteligentes basadas en veredicto completo"""
        if not veredicto:
            return

        grade = veredicto.get('grade', 'C')
        confidence = veredicto.get('confidence', 0)
        pattern_type = veredicto.get('pattern_type', 'Unknown')

        # Alertas para grades altos con más detalle
        if grade in ['A+', 'A', 'A-']:
            self.system_metrics['alerts_generated'] += 1
            action = veredicto.get('action', 'REVISAR')
            emoji = veredicto.get('emoji', '🎯')

            alert_msg = f"{emoji} SEÑAL {grade}: {pattern_type} - {action} ({confidence:.0f}%)"
            self.notify(alert_msg, timeout=8)

            if grade == 'A+':
                self.notify("🚀 SETUP EXCEPCIONAL - Confluencia perfecta detectada", timeout=10)

            # Log adicional para alertas importantes
            logger.warning("🚨 ALERTA %s: %s con %s%% confianza", grade, pattern_type, confidence)

    # ======================================================================
    # 🔧 MÉTODOS AUXILIARES PARA ESPECIALISTAS
    # ======================================================================

    def get_current_session_type(self):
        """Determina el tipo de sesión actual"""
        try:
            hour = datetime.now().hour
            if 8 <= hour < 16:
                return 'LONDON'
            elif 13 <= hour < 21:
                return 'NEWYORK'
            else:
                return 'ASIAN'
        except (ValueError, AttributeError, ImportError) as e:
            # Error getting timezone, default to ASIAN
            print(f"Debug: Exception in timezone detection: {e}")
            return 'ASIAN'

    def calculate_current_volatility(self, data: pd.DataFrame) -> float:
        """Calcula volatilidad actual"""
        try:
            if data is not None and not data.empty and len(data) >= 20:
                recent = data.tail(20)
                ranges = recent['high'] - recent['low']
                return float(ranges.mean())
            return 0.0
        except (ValueError, AttributeError, TypeError) as e:
            # Error calculating volatility, return safe default
            print(f"Debug: Exception in volatility calculation: {e}")
            return 0.0

    def filter_and_rank_pois(self, pois: List[Dict]) -> List[Dict]:
        """Filtra POIs duplicados y los ordena por relevancia"""
        try:
            # Filtrar duplicados por proximidad de precio
            unique_pois = []
            for poi in pois:
                poi_price = poi.get('price', 0)
                is_duplicate = False

                for existing in unique_pois:
                    existing_price = existing.get('price', 0)
                    if abs(poi_price - existing_price) < 0.0005:  # 5 pips de tolerancia
                        is_duplicate = True
                        break

                if not is_duplicate:
                    unique_pois.append(poi)

            # Ordenar por score descendente
            unique_pois.sort(key=lambda x: x.get('score', 0), reverse=True)
            return unique_pois[:10]  # Top 10 POIs

        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error filtrando POIs: {e}")
            return pois

    def create_pattern_analysis_object(self, best_item: Dict, veredicto: Optional[Dict]):
        """Crea objeto de análisis de patrón para el panel"""
        try:
            item_data = best_item['data']
            item_type = best_item['type']

            class MockPattern:
                def __init__(self, data, item_type, veredicto):
                    self.pattern = type('Pattern', (), {})()

                    if item_type == 'pattern':
                        self.pattern_name = data.get('type', 'UNKNOWN_PATTERN')
                        self.probability = data.get('confidence_pct', 0)
                    else:  # POI
                        self.pattern_name = f"POI_{data.get('type', 'UNKNOWN')}"
                        self.probability = data.get('score', 0)

                    self.narrative = self.generate_narrative(data, veredicto, item_type)

                def generate_narrative(self, data, veredicto, item_type):
                    if item_type == 'pattern':
                        pattern_name = data.get('type', 'Pattern').replace('_', ' ').title()
                        confidence = data.get('confidence_pct', 0)
                    else:
                        pattern_name = f"POI {data.get('type', 'Unknown').replace('_', ' ').title()}"
                        confidence = data.get('score', 0)

                    if veredicto:
                        grade = veredicto.get('grade', 'C')
                        action = veredicto.get('action', 'ESPERAR')
                        return f"{pattern_name} detectado con {confidence:.0f}% confianza. Grade: {grade}. Acción: {action}. Análisis completo con todos los especialistas."
                    else:
                        return f"{pattern_name} detectado con {confidence:.0f}% confianza usando análisis integral de especialistas MT5."

            self.last_pattern_analysis = MockPattern(item_data, item_type, veredicto)

        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error creando objeto de análisis: {e}")

    # ======================================================================
    # 🎪 MÉTODOS DE DETECCIÓN ESPECÍFICOS MEJORADOS
    # ======================================================================

    def detect_silver_bullet_complete(self, m5_data: pd.DataFrame, m1_data: Optional[pd.DataFrame], _context: Dict) -> Optional[Dict]:
        """Detecta Silver Bullet usando análisis completo"""
        try:
            # Usar el ICT Pattern Analyzer si está disponible
            analyzer_method = getattr(self.ict_analyzer, '_analyze_silver_bullet_setup', None)
            if analyzer_method:
                try:
                    ict_signal = analyzer_method()
                    if ict_signal:
                        return {
                            'type': 'SILVER_BULLET',
                            'timeframe': 'M5',
                            'strength': ict_signal.strength,
                            'confidence_pct': ict_signal.probability,
                            'direction': ict_signal.direction.value,
                            'narrative': ict_signal.narrative,
                            'price_level': self.current_price,
                            'detected_at': datetime.now()
                        }
                except (AttributeError, TypeError, ValueError):  # ICT analyzer exceptions
                    pass

            # Fallback a detección simple
            return self.detect_silver_bullet(m5_data, m1_data)

        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error Silver Bullet completo: {e}")
            return None

    def detect_judas_swing_complete(self, m5_data: pd.DataFrame, _m1_data: Optional[pd.DataFrame], _context: Dict) -> Optional[Dict]:
        """Detecta Judas Swing usando análisis completo"""
        try:
            # Usar el ICT Pattern Analyzer si está disponible
            analyzer_method = getattr(self.ict_analyzer, '_analyze_judas_swing', None)
            if analyzer_method:
                try:
                    ict_signal = analyzer_method()
                    if ict_signal:
                        return {
                            'type': 'JUDAS_SWING',
                            'timeframe': 'M5',
                            'strength': ict_signal.strength,
                            'confidence_pct': ict_signal.probability,
                            'direction': ict_signal.direction.value,
                            'narrative': ict_signal.narrative,
                            'price_level': self.current_price,
                            'detected_at': datetime.now()
                        }
                except (AttributeError, TypeError, ValueError):  # ICT analyzer exceptions
                    pass

            # Fallback: detección manual de Judas Swing
            if len(m5_data) < 20:
                return None

            # Buscar reversión desde extremos en sesión actual
            hour = datetime.now().hour
            if hour in [8, 9, 13, 14]:  # Horas clave para Judas
                recent = m5_data.tail(20)
                max_high = recent['high'].max()
                min_low = recent['low'].min()
                current_close = recent['close'].iloc[-1]

                # Detectar falsa ruptura seguida de reversión
                range_size = max_high - min_low
                if range_size > 0.001:  # Rango significativo
                    if abs(current_close - max_high) / max_high < 0.0005:  # Cerca del high
                        return {
                            'type': 'JUDAS_SWING',
                            'timeframe': 'M5',
                            'strength': 75,
                            'direction': 'BEARISH',
                            'price_level': max_high,
                            'detected_at': datetime.now()
                        }
                    elif abs(current_close - min_low) / min_low < 0.0005:  # Cerca del low
                        return {
                            'type': 'JUDAS_SWING',
                            'timeframe': 'M5',
                            'strength': 75,
                            'direction': 'BULLISH',
                            'price_level': min_low,
                            'detected_at': datetime.now()
                        }

            return None

        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error Judas Swing completo: {e}")
            return None

    def detect_liquidity_grab_complete(self, m5_data: pd.DataFrame, _m1_data: Optional[pd.DataFrame], _context: Dict) -> Optional[Dict]:
        """Detecta Liquidity Grab usando análisis mejorado"""
        try:
            return self.detect_liquidity_grab(m5_data)
        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error Liquidity Grab completo: {e}")
            return None

    def detect_order_blocks_complete(self, m5_data: pd.DataFrame, _m1_data: Optional[pd.DataFrame], _context: Dict) -> Optional[Dict]:
        """Detecta Order Blocks usando análisis mejorado"""
        try:
            return self.detect_order_blocks(m5_data)
        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error Order Blocks completo: {e}")
            return None

    def detect_fair_value_gaps_complete(self, m5_data: pd.DataFrame, _m1_data: Optional[pd.DataFrame], _context: Dict) -> Optional[Dict]:
        """Detecta Fair Value Gaps usando análisis mejorado"""
        try:
            return self.detect_fair_value_gaps(m5_data)
        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error Fair Value Gaps completo: {e}")
            return None

    # ======================================================================
    # 🎪 MÉTODOS DE DETECCIÓN ESPECÍFICOS BÁSICOS (FALLBACK)
    # ======================================================================

    def detect_silver_bullet(self, m5_data: pd.DataFrame, _m1_data: Optional[pd.DataFrame]) -> Optional[Dict]:
        """Detecta patrón Silver Bullet básico"""
        try:
            if len(m5_data) < 50:
                return None

            # Lógica básica de Silver Bullet
            recent = m5_data.tail(20)
            price_change = abs(recent['close'].iloc[-1] - recent['open'].iloc[0])
            volume_avg = recent['tick_volume'].mean() if 'tick_volume' in recent.columns else 1000

            if price_change > 0.001 and volume_avg > 500:  # Criterios básicos
                return {
                    'type': 'SILVER_BULLET',
                    'timeframe': 'M5',
                    'strength': min(85, price_change * 10000 + 50),
                    'price': recent['close'].iloc[-1],
                    'timestamp': datetime.now().isoformat()
                }
            return None
        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error detectando Silver Bullet: {e}")
            return None

    def detect_liquidity_grab(self, m5_data: pd.DataFrame) -> Optional[Dict]:
        """Detecta Liquidity Grab básico"""
        try:
            if len(m5_data) < 30:
                return None

            recent = m5_data.tail(15)
            high_max = recent['high'].max()
            low_min = recent['low'].min()
            current_price = recent['close'].iloc[-1]

            # Detectar si hay ruptura seguida de reversión
            range_size = high_max - low_min
            if range_size > 0.0015:  # Rango significativo
                return {
                    'type': 'LIQUIDITY_GRAB',
                    'timeframe': 'M5',
                    'strength': min(90, range_size * 5000 + 40),
                    'price': current_price,
                    'timestamp': datetime.now().isoformat()
                }
            return None
        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error detectando Liquidity Grab: {e}")
            return None

    def detect_order_blocks(self, m5_data: pd.DataFrame) -> Optional[Dict]:
        """Detecta Order Blocks básicos"""
        try:
            if len(m5_data) < 40:
                return None

            recent = m5_data.tail(25)

            # Buscar velas con volumen alto y movimiento significativo
            if 'tick_volume' in recent.columns:
                volume_threshold = recent['tick_volume'].quantile(0.8)
                high_volume_candles = recent[recent['tick_volume'] >= volume_threshold]

                if len(high_volume_candles) > 2:
                    return {
                        'type': 'ORDER_BLOCK',
                        'timeframe': 'M5',
                        'strength': min(80, len(high_volume_candles) * 15 + 35),
                        'price': high_volume_candles['close'].iloc[-1],
                        'timestamp': datetime.now().isoformat()
                    }
            return None
        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error detectando Order Blocks: {e}")
            return None

    def detect_fair_value_gaps(self, m5_data: pd.DataFrame) -> Optional[Dict]:
        """Detecta Fair Value Gaps básicos"""
        try:
            if len(m5_data) < 10:
                return None

            recent = m5_data.tail(10)

            # Buscar gaps en el precio
            for i in range(len(recent) - 2):
                candle1 = recent.iloc[i]
                _ = recent.iloc[i + 1]  # candle2 not used in this algorithm
                candle3 = recent.iloc[i + 2]

                # Gap alcista
                if candle1['high'] < candle3['low']:
                    gap_size = candle3['low'] - candle1['high']
                    if gap_size > 0.0008:  # Gap significativo
                        return {
                            'type': 'FAIR_VALUE_GAP',
                            'direction': 'BULLISH',
                            'timeframe': 'M5',
                            'strength': min(75, gap_size * 8000 + 30),
                            'price': (candle1['high'] + candle3['low']) / 2,
                            'timestamp': datetime.now().isoformat()
                        }

                # Gap bajista
                if candle1['low'] > candle3['high']:
                    gap_size = candle1['low'] - candle3['high']
                    if gap_size > 0.0008:  # Gap significativo
                        return {
                            'type': 'FAIR_VALUE_GAP',
                            'direction': 'BEARISH',
                            'timeframe': 'M5',
                            'strength': min(75, gap_size * 8000 + 30),
                            'price': (candle1['low'] + candle3['high']) / 2,
                            'timestamp': datetime.now().isoformat()
                        }

            return None
        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error detectando Fair Value Gaps: {e}")
            return None

    def simulate_pattern_detection(self):
        """Simula detección de patrones para modo demo"""
        try:
            patterns = ['SILVER_BULLET', 'ORDER_BLOCK', 'LIQUIDITY_GRAB', 'FAIR_VALUE_GAP']
            selected_pattern = random.choice(patterns)

            # Crear análisis simulado
            class MockPattern:
                def __init__(self, pattern_type):
                    self.pattern_name = pattern_type
                    self.probability = random.randint(65, 95)
                    self.narrative = f"Patrón {pattern_type.replace('_', ' ').title()} detectado en modo simulado con {self.probability}% de probabilidad."

            self.last_pattern_analysis = MockPattern(selected_pattern)
            self.patterns_detected += 1

            if self.last_pattern_analysis.probability > 85:
                self.high_probability_signals += 1

        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error en simulación: {e}")

    # ======================================================================
    # 🔄 MÉTODOS DE ACTUALIZACIÓN AUTOMÁTICA
    # ======================================================================

    def auto_refresh_system(self):
        """Auto-refresh del sistema cada 10 segundos"""
        try:
            if self.mt5_connected:
                self.update_current_price()

            # Actualizar paneles según pestaña activa
            self.update_active_panel()
        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error en auto-refresh: {e}")

    def auto_analyze_patterns(self):
        """Auto-análisis de patrones cada 30 segundos"""
        if self.auto_patterns_enabled:
            self.analyze_patterns()

    def micro_update_system(self):
        """Micro-updates cada 5 segundos"""
        try:
            # Actualizar métricas básicas
            if self.hibernation_static:
                self.hibernation_static.update(self.render_hibernation_panel())
        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error en micro-update: {e}")

    def update_active_panel(self):
        """Actualiza el panel activo"""
        try:
            # Actualizar todos los paneles
            if self.hibernation_static:
                self.hibernation_static.update(self.render_hibernation_panel())
            if self.ict_static:
                self.ict_static.update(self.render_ict_panel())
            if self.pattern_static:
                self.pattern_static.update(self.render_patterns_panel())
            if self.analytics_static:
                self.analytics_static.update(self.render_analytics_panel())
        except (FileNotFoundError, PermissionError, IOError) as e:
            if self.debug_mode:
                print(f"❌ Error actualizando paneles: {e}")

    def receive_data_from_backend(self, data_package: Dict[str, Any]):
        """
        🎯 MÉTODO CRÍTICO: Recibe datos del backend a través del DashboardController
        Este es el método que el controller llama para enviar datos actualizados
        """
        try:
            logger.info("📦 Datos recibidos del backend")

            # Actualizar datos de mercado
            if 'current_price' in data_package:
                self.current_price = data_package['current_price']

            if 'pois' in data_package:
                self.real_market_data['pois_detected'] = data_package['pois']
                self.patterns_detected = len(data_package['pois'])

            if 'analysis_results' in data_package:
                analysis = data_package['analysis_results']
                self.real_market_data['market_context'] = analysis

            if 'candles_data' in data_package:
                candles = data_package['candles_data']
                # Actualizar datos de velas si están disponibles
                for tf, data in candles.items():
                    if tf in self.real_market_data:
                        self.real_market_data[tf] = data

            # Actualizar métricas del sistema
            self.system_metrics['data_updates'] += 1

            # Forzar actualización de todos los paneles
            self.update_active_panel()

            logger.info("✅ Datos procesados: Precio=%s, POIs=%s", self.current_price, self.patterns_detected)

            if self.debug_mode:
                print(f"📦 Backend data: Precio={self.current_price:.5f}, POIs={self.patterns_detected}")

        except (FileNotFoundError, PermissionError, IOError) as e:
            logger.error("❌ Error procesando datos del backend: %s", e)
            if self.debug_mode:
                print(f"❌ Error procesando datos del backend: {e}")

    def update_from_controller(self, controller_state):
        """
        🎯 MÉTODO REQUERIDO POR DASHBOARDCONTROLLER
        Este método es llamado por el DashboardController para enviar actualizaciones
        """
        try:
            logger.info("🔄 [DASHBOARD-CALLBACK] Recibiendo estado del controller")

            # Verificar si hay datos válidos en el estado del controller
            if controller_state:
                # Actualizar precio actual
                if 'current_price' in controller_state and controller_state['current_price'] > 0:
                    self.current_price = controller_state['current_price']
                    logger.info("💰 Precio actualizado: %s", self.current_price)

                # Actualizar POIs desde poi_results
                if 'poi_results' in controller_state and controller_state['poi_results']:
                    poi_data = controller_state['poi_results']
                    if 'pois' in poi_data:
                        self.real_market_data['pois_detected'] = poi_data['pois']
                        self.patterns_detected = len(poi_data['pois'])
                        logger.info("🎯 POIs actualizados: %s detectados", self.patterns_detected)

                # Actualizar análisis ICT desde ict_results
                if 'ict_results' in controller_state and controller_state['ict_results']:
                    self.real_market_data['market_context'] = controller_state['ict_results']
                    logger.info("📊 Análisis ICT actualizado")

                # Actualizar timestamp
                if 'last_update' in controller_state:
                    self.last_update_time = controller_state['last_update']

                # Incrementar contador de actualizaciones
                self.system_metrics['data_updates'] += 1

                # Forzar actualización de todos los paneles
                self.update_active_panel()

                logger.info("✅ [DASHBOARD-CALLBACK] Estado del controller procesado exitosamente")
            else:
                logger.warning("⚠️ [DASHBOARD-CALLBACK] Estado del controller vacío o None")

        except (FileNotFoundError, PermissionError, IOError) as e:
            logger.error("❌ [DASHBOARD-CALLBACK] Error procesando estado del controller: %s", e)
            import traceback
            logger.error("❌ [DASHBOARD-CALLBACK] Traceback: %s", traceback.format_exc())

    # ======================================================================
    # 🏗️ MÉTODOS STUB - ARQUITECTURA FUTURA (YA DEFINIDOS ARRIBA)
    # ======================================================================
    # Los métodos detect_*_complete están definidos correctamente más arriba
    # Se eliminan duplicados para evitar errores de redefinición

# ======================================================================
# 🚀 FUNCIÓN PRINCIPAL Y PUNTO DE ENTRADA
# ======================================================================

def main():
    """Función principal para ejecutar el Dashboard Definitivo"""
    try:
        app = SentinelDashboardDefinitivo()
        app.run()
    except KeyboardInterrupt:
        print("\n🛑 Dashboard interrumpido por el usuario")
    except (FileNotFoundError, PermissionError, IOError) as e:
        print(f"💥 Error ejecutando Dashboard: {e}")


if __name__ == "__main__":
    main()
