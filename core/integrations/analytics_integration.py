#!/usr/bin/env python3
"""
🔗 ANALYTICS INTEGRATION - Dashboard Enhancement
==============================================

Integración completa del sistema de analytics ICT con el dashboard principal,
proporcionando análisis en tiempo real y señales de alta probabilidad.

Creado por Sprint 1.3 - Advanced Analytics Integration
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import threading
import time

# Ajustar path para imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Imports del proyecto
try:
    from core.analytics.ict_analyzer import ICTAnalyzer, ICTPattern, ICTSignal
    from dashboard.widgets.ict_analytics_widget import ICTAnalyticsWidget
    from utils.advanced_candle_downloader import AdvancedCandleDownloader
    ANALYTICS_INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Analytics Integration Error: {e}")
    ANALYTICS_INTEGRATION_AVAILABLE = False

class AnalyticsIntegration:
    """
    Integración completa del sistema de analytics ICT con el dashboard.

    Características:
    - Coordinación entre ICT Analyzer y Dashboard
    - Threading para análisis en background
    - Cache inteligente de señales
    - Notificaciones de alta prioridad
    """

    def __init__(self):
        self.is_active = False
        self.analyzer = ICTAnalyzer() if ANALYTICS_INTEGRATION_AVAILABLE else None
        self.widget = ICTAnalyticsWidget() if ANALYTICS_INTEGRATION_AVAILABLE else None
        self.downloader = None

        # Threading para análisis continuo
        self.analysis_thread = None
        self.analysis_interval = 30  # segundos

        # Cache de datos y señales
        self.data_cache = {}
        self.signal_cache = []
        self.last_analysis = {}

        # Métricas de integración
        self.integration_metrics = {
            "total_analysis_cycles": 0,
            "signals_generated": 0,
            "high_priority_alerts": 0,
            "cache_hits": 0,
            "analysis_errors": 0,
            "uptime_start": datetime.now()
        }

        # Configuración de símbolos y timeframes
        self.analysis_config = {
            "symbols": ["EURUSD", "GBPUSD", "USDJPY", "USDCHF"],
            "timeframes": ["H1", "H4", "D1"],
            "lookback_periods": {"H1": 200, "H4": 100, "D1": 50},
            "confidence_threshold": 75.0,
            "high_priority_threshold": 90.0
        }

        if ANALYTICS_INTEGRATION_AVAILABLE:
            self._initialize_downloader()

    def _initialize_downloader(self):
        """Inicializar el downloader con manejo de errores"""
        try:
            self.downloader = AdvancedCandleDownloader()
            print("✅ Analytics Integration: Downloader inicializado")
        except Exception as e:
            print(f"⚠️ Analytics Integration: Error inicializando downloader: {e}")
            self.downloader = None

    def start_analytics_engine(self) -> bool:
        """Iniciar el motor de analytics en background"""
        if not ANALYTICS_INTEGRATION_AVAILABLE:
            print("❌ Analytics no disponible")
            return False

        if self.is_active:
            print("⚠️ Analytics ya está activo")
            return True

        try:
            self.is_active = True

            # Iniciar thread de análisis continuo
            self.analysis_thread = threading.Thread(
                target=self._continuous_analysis_loop,
                daemon=True
            )
            self.analysis_thread.start()

            print("🚀 Analytics Engine iniciado exitosamente")
            return True

        except Exception as e:
            print(f"❌ Error iniciando Analytics Engine: {e}")
            self.is_active = False
            return False

    def stop_analytics_engine(self):
        """Detener el motor de analytics"""
        self.is_active = False
        if self.analysis_thread and self.analysis_thread.is_alive():
            self.analysis_thread.join(timeout=5.0)
        print("🛑 Analytics Engine detenido")

    def _continuous_analysis_loop(self):
        """Loop principal de análisis continuo"""
        print("🔄 Iniciando loop de análisis continuo...")

        while self.is_active:
            try:
                start_time = time.time()

                # Ejecutar ciclo de análisis
                self._run_analysis_cycle()

                # Actualizar métricas
                self.integration_metrics["total_analysis_cycles"] += 1

                # Calcular tiempo de espera dinámico
                cycle_time = time.time() - start_time
                wait_time = max(self.analysis_interval - cycle_time, 5)

                # Esperar hasta el próximo ciclo
                time.sleep(wait_time)

            except Exception as e:
                print(f"❌ Error en loop de análisis: {e}")
                self.integration_metrics["analysis_errors"] += 1
                time.sleep(10)  # Espera más larga en caso de error

    def _run_analysis_cycle(self):
        """Ejecutar un ciclo completo de análisis"""

        if not self.analyzer:
            return

        new_signals = []

        # Analizar cada símbolo y timeframe
        for symbol in self.analysis_config["symbols"]:
            for timeframe in self.analysis_config["timeframes"]:
                try:
                    # Obtener datos (con cache)
                    df = self._get_market_data_cached(symbol, timeframe)

                    if df is not None and not df.empty:
                        # Ejecutar análisis ICT
                        signals = self.analyzer.analyze_market_data(df, symbol, timeframe)

                        # Filtrar señales nuevas de alta calidad
                        for signal in signals:
                            if (signal.confidence >= self.analysis_config["confidence_threshold"] and
                                not self._is_duplicate_signal(signal)):
                                new_signals.append(signal)

                except Exception as e:
                    print(f"⚠️ Error analizando {symbol} {timeframe}: {e}")

        # Procesar nuevas señales
        if new_signals:
            self._process_new_signals(new_signals)

        # Limpiar señales antiguas
        self._cleanup_old_signals()

        # Actualizar widget si está disponible
        if self.widget:
            self.widget.active_signals.extend(new_signals)
            self.widget.analyze_current_market()

    def _get_market_data_cached(self, symbol: str, timeframe: str) -> Optional[Any]:
        """Obtener datos de mercado con sistema de cache"""
        cache_key = f"{symbol}_{timeframe}"
        current_time = datetime.now()

        # Verificar cache (válido por 1 minuto)
        if (cache_key in self.data_cache and
            cache_key in self.last_analysis and
            (current_time - self.last_analysis[cache_key]).total_seconds() < 60):

            self.integration_metrics["cache_hits"] += 1
            return self.data_cache[cache_key]

        # Obtener datos frescos
        df = None
        if self.downloader:
            try:
                # Usar método correcto del downloader
                lookback = self.analysis_config["lookback_periods"].get(timeframe, 100)

                # Verificar si el downloader tiene el método correcto
                if hasattr(self.downloader, 'get_historical_data'):
                    df = self.downloader.get_historical_data(symbol, timeframe, lookback)
                elif hasattr(self.downloader, 'download_data'):
                    df = self.downloader.download_data(symbol, timeframe, lookback)
                else:
                    # Fallback: usar el manager MT5 directamente
                    from utils.mt5_data_manager import cargar_datos_historicos_unificado
                    df = cargar_datos_historicos_unificado(timeframe, lookback, symbol)

            except Exception as e:
                print(f"⚠️ Error obteniendo datos {symbol} {timeframe}: {e}")

        # Actualizar cache
        if df is not None:
            self.data_cache[cache_key] = df
            self.last_analysis[cache_key] = current_time

        return df

    def _is_duplicate_signal(self, new_signal: Any) -> bool:
        """Verificar si la señal es duplicada"""
        for existing_signal in self.signal_cache:
            if (existing_signal.pattern_type == new_signal.pattern_type and
                existing_signal.symbol == new_signal.symbol and
                abs((existing_signal.timestamp - new_signal.timestamp).total_seconds()) < 3600):  # 1 hora
                return True
        return False

    def _process_new_signals(self, signals: List[Any]):
        """Procesar nuevas señales detectadas"""
        for signal in signals:
            # Agregar al cache
            self.signal_cache.append(signal)
            self.integration_metrics["signals_generated"] += 1

            # Verificar si es alta prioridad
            if signal.confidence >= self.analysis_config["high_priority_threshold"]:
                self._handle_high_priority_signal(signal)

    def _handle_high_priority_signal(self, signal: Any):
        """Manejar señal de alta prioridad"""
        self.integration_metrics["high_priority_alerts"] += 1

        # Log de alta prioridad
        print(f"🚨 HIGH PRIORITY SIGNAL: {signal.pattern_type.value} on {signal.symbol} - {signal.confidence:.1f}%")

        # Aquí se pueden agregar notificaciones, emails, etc.

    def _cleanup_old_signals(self):
        """Limpiar señales antiguas del cache"""
        current_time = datetime.now()
        cutoff_hours = 4

        self.signal_cache = [
            signal for signal in self.signal_cache
            if (current_time - signal.timestamp).total_seconds() < cutoff_hours * 3600
        ]

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Obtener datos para el dashboard principal"""

        if not ANALYTICS_INTEGRATION_AVAILABLE:
            return {"available": False, "error": "Analytics not available"}

        # Calcular uptime
        uptime = datetime.now() - self.integration_metrics["uptime_start"]
        uptime_hours = uptime.total_seconds() / 3600

        # Señales recientes (últimas 2 horas)
        recent_signals = [
            s for s in self.signal_cache
            if (datetime.now() - s.timestamp).total_seconds() < 7200
        ]

        # Contar patrones por tipo
        pattern_counts = {}
        for signal in self.signal_cache:
            pattern_type = signal.pattern_type.value
            pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + 1

        return {
            "available": True,
            "status": "active" if self.is_active else "inactive",
            "uptime_hours": round(uptime_hours, 1),
            "metrics": self.integration_metrics,
            "recent_signals": len(recent_signals),
            "total_signals": len(self.signal_cache),
            "pattern_distribution": pattern_counts,
            "high_confidence_signals": [
                s for s in recent_signals
                if s.confidence >= self.analysis_config["high_priority_threshold"]
            ],
            "analysis_config": self.analysis_config
        }

    def get_real_time_alerts(self) -> List[str]:
        """Obtener alertas en tiempo real"""
        alerts = []

        # Alertas de señales de alta confianza
        high_conf_signals = [
            s for s in self.signal_cache[-10:]  # Últimas 10 señales
            if s.confidence >= 90
        ]

        for signal in high_conf_signals:
            alert = f"🎯 {signal.pattern_type.value.upper()} - {signal.symbol} - {signal.confidence:.1f}%"
            alerts.append(alert)

        # Alertas de sistema
        if self.integration_metrics["analysis_errors"] > 5:
            alerts.append("⚠️ Múltiples errores de análisis detectados")

        if not self.is_active:
            alerts.append("❌ Motor de analytics desactivado")

        return alerts

    def force_analysis_update(self) -> Dict[str, Any]:
        """Forzar actualización inmediata del análisis"""
        if not ANALYTICS_INTEGRATION_AVAILABLE:
            return {"success": False, "error": "Analytics not available"}

        try:
            self._run_analysis_cycle()
            return {"success": True, "message": "Análisis actualizado exitosamente"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def export_analytics_report(self) -> Dict[str, Any]:
        """Exportar reporte completo de analytics"""
        dashboard_data = self.get_dashboard_data()

        return {
            "report_timestamp": datetime.now().isoformat(),
            "integration_status": dashboard_data,
            "signal_details": [
                {
                    "pattern": s.pattern_type.value,
                    "symbol": s.symbol,
                    "confidence": s.confidence,
                    "timestamp": s.timestamp.isoformat(),
                    "risk_reward": s.risk_reward_ratio
                }
                for s in self.signal_cache
            ],
            "performance_summary": {
                "total_cycles": self.integration_metrics["total_analysis_cycles"],
                "signals_per_hour": (
                    self.integration_metrics["signals_generated"] /
                    max(dashboard_data.get("uptime_hours", 1), 1)
                ),
                "error_rate": (
                    self.integration_metrics["analysis_errors"] /
                    max(self.integration_metrics["total_analysis_cycles"], 1)
                ),
                "cache_efficiency": (
                    self.integration_metrics["cache_hits"] /
                    max(self.integration_metrics["total_analysis_cycles"], 1)
                )
            }
        }


# Instancia global para integración con dashboard
_analytics_integration = None

def get_analytics_integration() -> AnalyticsIntegration:
    """Obtener instancia global de integración de analytics"""
    global _analytics_integration
    if _analytics_integration is None:
        _analytics_integration = AnalyticsIntegration()
    return _analytics_integration

def initialize_analytics_for_dashboard():
    """Inicializar analytics para integración con dashboard"""
    integration = get_analytics_integration()
    success = integration.start_analytics_engine()
    return success

def get_analytics_dashboard_data():
    """Función de conveniencia para obtener datos para dashboard"""
    integration = get_analytics_integration()
    return integration.get_dashboard_data()

def get_analytics_alerts():
    """Función de conveniencia para obtener alertas"""
    integration = get_analytics_integration()
    return integration.get_real_time_alerts()


# Testing del módulo
if __name__ == "__main__":
    print("🔗 Analytics Integration - Test completo")

    integration = AnalyticsIntegration()

    # Test inicialización
    if integration.start_analytics_engine():
        print("✅ Analytics Engine iniciado exitosamente")

        # Esperar un poco para que el análisis se ejecute
        print("⏳ Esperando análisis...")
        time.sleep(5)

        # Obtener datos del dashboard
        dashboard_data = integration.get_dashboard_data()
        print(f"📊 Dashboard data: {dashboard_data['status']}")
        print(f"🎯 Señales recientes: {dashboard_data['recent_signals']}")

        # Obtener alertas
        alerts = integration.get_real_time_alerts()
        if alerts:
            print("🚨 Alertas activas:")
            for alert in alerts:
                print(f"   {alert}")

        # Exportar reporte
        report = integration.export_analytics_report()
        print(f"📋 Reporte exportado con {len(report['signal_details'])} señales")

        # Detener engine
        integration.stop_analytics_engine()
        print("🛑 Analytics Engine detenido")

    else:
        print("❌ Error iniciando Analytics Engine")

    print("✅ Test de Analytics Integration completado")
