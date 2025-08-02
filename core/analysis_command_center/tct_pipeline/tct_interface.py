#!/usr/bin/env python3
"""
🚪 TCT INTERFACE - Punto de entrada principal para el pipeline TCT
BASADO EN: Lógica principal del health_analyzer.py
PROTOCOLO: "Caja Negra" - Interfaz sin terminal, logs exhaustivos
"""

import asyncio
import threading
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

# 🔌 IMPORTS DEL ICT ENGINE
from sistema.logging_interface import enviar_senal_log
from core.ict_engine import (
    MarketContext, 
    OptimizedICTAnalysis,
    update_market_context,
    ConfidenceEngine
)
from core.poi_system import encontrar_pois_multiples_para_dashboard

# 🔌 IMPORTS DEL TCT PIPELINE
from .tct_measurements import TCTMeasurementEngine
from .tct_aggregator import TCTAggregator
from .tct_formatter import TCTFormatter

class TCTInterface:
    """
    Interfaz principal del pipeline TCT
    Coordina mediciones, agregación y formateo
    Similar al patrón del health_analyzer pero para TCT
    """
    
    def __init__(self, 
                 measurement_interval: float = 1.0,
                 aggregation_interval: float = 60.0,
                 enable_exports: bool = True):
        """
        Inicialización del interface TCT
        
        Args:
            measurement_interval: Intervalo entre mediciones (segundos)
            aggregation_interval: Intervalo de agregación (segundos)
            enable_exports: Activar exports automáticos
        """
        
        # 🧭 CONFIGURACIÓN BÁSICA
        self.measurement_interval = measurement_interval
        self.aggregation_interval = aggregation_interval
        self.enable_exports = enable_exports
        
        # 🔧 COMPONENTES DEL PIPELINE
        self.measurement_engine = TCTMeasurementEngine()
        self.aggregator = TCTAggregator()
        self.formatter = TCTFormatter()
        
        # 🏃 CONTROL DE EJECUCIÓN
        self._running = False
        self._measurement_thread = None
        self._aggregation_thread = None
        
        # 📊 ESTADO Y CONTEXTO
        self._current_market_context = None
        self._tct_session_active = False
        self._last_aggregation = None
        
        # 📝 CAJA NEGRA - LOG INICIALIZACIÓN
        enviar_senal_log(
            level='DEBUG',
            message=f"TCT Interface inicializado | "
                   f"Medición: {measurement_interval}s | "
                   f"Agregación: {aggregation_interval}s | "
                   f"Exports: {enable_exports}",
            emisor='tct_interface',
            categoria='tct'
        )
        
        enviar_senal_log(
            level='INFO',
            message="🚪 TCT Interface - Sistema principal activado",
            emisor='tct_interface',
            categoria='tct'
        )
    
    def start_tct_monitoring(self, 
                           symbols: List[str] = None,
                           timeframes: List[str] = None) -> bool:
        """
        Inicia el monitoreo TCT en modo background
        Similar a start_monitoring del health_analyzer
        """
        
        if self._running:
            enviar_senal_log(
                level='WARNING',
                message="🚪 TCT Interface ya está ejecutándose",
                emisor='tct_interface',
                categoria='tct'
            )
            return False
        
        # 🎯 CONFIGURAR PARÁMETROS DE MONITOREO
        if symbols is None:
            symbols = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD"]  # Default
        
        if timeframes is None:
            timeframes = ["M1", "M5", "M15", "H1"]  # Default
        
        # 🏁 ACTIVAR SISTEMA
        self._running = True
        self._tct_session_active = True
        
        # 🧵 INICIAR THREADS DE MONITOREO
        self._measurement_thread = threading.Thread(
            target=self._measurement_loop,
            args=(symbols, timeframes),
            daemon=True,
            name="TCT_Measurement_Thread"
        )
        
        self._aggregation_thread = threading.Thread(
            target=self._aggregation_loop,
            daemon=True,
            name="TCT_Aggregation_Thread"
        )
        
        # 🚀 LAUNCH
        self._measurement_thread.start()
        self._aggregation_thread.start()
        
        # 📝 CAJA NEGRA - LOG START
        enviar_senal_log(
            level='DEBUG',
            message=f"🚀 TCT MONITORING STARTED | "
                   f"Symbols: {symbols} | "
                   f"Timeframes: {timeframes} | "
                   f"Threads: Measurement={self._measurement_thread.is_alive()}, "
                   f"Aggregation={self._aggregation_thread.is_alive()}",
            emisor='tct_interface',
            categoria='tct'
        )
        
        enviar_senal_log(
            level='INFO',
            message=f"🚀 TCT Pipeline iniciado - {len(symbols)} símbolos, {len(timeframes)} timeframes",
            emisor='tct_interface',
            categoria='tct'
        )
        
        return True
    
    def stop_tct_monitoring(self) -> bool:
        """Detiene el monitoreo TCT"""
        
        if not self._running:
            enviar_senal_log(
                level='WARNING',
                message="🚪 TCT Interface no está ejecutándose",
                emisor='tct_interface',
                categoria='tct'
            )
            return False
        
        # 🛑 DETENER SISTEMA
        self._running = False
        self._tct_session_active = False
        
        # 🧵 ESPERAR THREADS
        if self._measurement_thread and self._measurement_thread.is_alive():
            self._measurement_thread.join(timeout=5.0)
        
        if self._aggregation_thread and self._aggregation_thread.is_alive():
            self._aggregation_thread.join(timeout=5.0)
        
        # 📝 CAJA NEGRA - LOG STOP
        enviar_senal_log(
            level='DEBUG',
            message="🛑 TCT MONITORING STOPPED | All threads terminated",
            emisor='tct_interface',
            categoria='tct'
        )
        
        enviar_senal_log(
            level='INFO',
            message="🛑 TCT Pipeline detenido",
            emisor='tct_interface',
            categoria='tct'
        )
        
        return True
    
    def measure_single_analysis(self, 
                              symbol: str, 
                              timeframe: str,
                              market_context: MarketContext = None) -> Optional[Dict]:
        """
        Ejecuta una medición TCT única
        Para uso sincrónico desde dashboard u otros componentes
        """
        
        try:
            # 🎯 USAR CONTEXTO PROPORCIONADO O CREAR UNO NUEVO
            if market_context is None:
                market_context = self._get_current_market_context(symbol, timeframe)
            
            # ⏱️ INICIAR MEDICIÓN
            measurement_id = self.measurement_engine.start_measurement(
                operation_name=f"single_analysis_{symbol}_{timeframe}",
                component_name="ict_engine",
                metadata={
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "analysis_type": "single",
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            # 🧠 EJECUTAR ANÁLISIS ICT (simulando el análisis real)
            analysis_result = self._execute_ict_analysis(symbol, timeframe, market_context)
            
            # ⏹️ FINALIZAR MEDICIÓN
            tct_metric = self.measurement_engine.end_measurement(measurement_id)
            
            # 📊 FORMATEAR RESULTADO
            result = {
                "measurement_id": measurement_id,
                "symbol": symbol,
                "timeframe": timeframe,
                "tct_ms": tct_metric.total_time_ms,
                "analysis_result": analysis_result,
                "timestamp": tct_metric.end_time,
                "metadata": tct_metric.metadata
            }
            
            # 📝 CAJA NEGRA - LOG SINGLE MEASUREMENT
            enviar_senal_log(
                level='DEBUG',
                message=f"📊 SINGLE TCT MEASUREMENT | "
                       f"Symbol: {symbol} | "
                       f"Timeframe: {timeframe} | "
                       f"TCT: {tct_metric.total_time_ms:.2f}ms | "
                       f"ID: {measurement_id}",
                emisor='tct_interface',
                categoria='tct'
            )
            
            return result
            
        except Exception as e:
            enviar_senal_log(
                level='ERROR',
                message=f"❌ ERROR en medición única TCT | Symbol: {symbol} | "
                       f"Timeframe: {timeframe} | Error: {str(e)}",
                emisor='tct_interface',
                categoria='tct'
            )
            return None
    
    def get_current_tct_status(self) -> Dict:
        """
        Obtiene el estado actual del pipeline TCT
        Para uso desde dashboard
        """
        
        status = {
            "is_running": self._running,
            "session_active": self._tct_session_active,
            "measurement_interval": self.measurement_interval,
            "aggregation_interval": self.aggregation_interval,
            "last_aggregation": self._last_aggregation.aggregation_timestamp if self._last_aggregation else None,
            "current_measurements": self.measurement_engine.get_active_measurements_count(),
            "total_measurements": self.measurement_engine.get_total_measurements_count(),
            "aggregated_data_available": self._last_aggregation is not None
        }
        
        # 📝 CAJA NEGRA - LOG STATUS REQUEST
        enviar_senal_log(
            level='DEBUG',
            message=f"📋 TCT STATUS REQUEST | "
                   f"Running: {status['is_running']} | "
                   f"Active: {status['current_measurements']} | "
                   f"Total: {status['total_measurements']}",
            emisor='tct_interface',
            categoria='tct'
        )
        
        return status
    
    def get_formatted_dashboard_data(self) -> Optional[Dict]:
        """
        Obtiene datos formateados para dashboard
        Retorna None si no hay datos agregados disponibles
        """
        
        if self._last_aggregation is None:
            enviar_senal_log(
                level='DEBUG',
                message="📊 Dashboard data request - No aggregated data available yet",
                emisor='tct_interface',
                categoria='tct'
            )
            return None
        
        # 📊 FORMATEAR PARA DASHBOARD
        dashboard_data = self.formatter.format_for_dashboard(self._last_aggregation)
        
        # 📝 CAJA NEGRA - LOG DASHBOARD DATA
        enviar_senal_log(
            level='DEBUG',
            message=f"📊 DASHBOARD DATA PROVIDED | "
                   f"Grade: {dashboard_data['tct_status']['performance_grade']} | "
                   f"Timeframes: {len(dashboard_data['tct_timeframes'])}",
            emisor='tct_interface',
            categoria='tct'
        )
        
        return dashboard_data
    
    def export_tct_data(self, format_type: str = "json") -> Optional[str]:
        """
        Exporta datos TCT en formato especificado
        Returns: Path del archivo exportado
        """
        
        if self._last_aggregation is None:
            enviar_senal_log(
                level='WARNING',
                message="💾 Export request - No aggregated data available",
                emisor='tct_interface',
                categoria='tct'
            )
            return None
        
        try:
            if format_type.lower() == "json":
                export_path = self.formatter.format_for_json_export(self._last_aggregation)
            elif format_type.lower() == "csv":
                export_path = self.formatter.format_for_csv_export(self._last_aggregation)
            else:
                enviar_senal_log(
                    level='ERROR',
                    message=f"💾 Export format no soportado: {format_type}",
                    emisor='tct_interface',
                    categoria='tct'
                )
                return None
            
            # 📝 CAJA NEGRA - LOG EXPORT
            enviar_senal_log(
                level='INFO',
                message=f"💾 TCT data exported - {format_type.upper()} format",
                emisor='tct_interface',
                categoria='tct'
            )
            
            return export_path
            
        except Exception as e:
            enviar_senal_log(
                level='ERROR',
                message=f"❌ ERROR en export TCT | Format: {format_type} | Error: {str(e)}",
                emisor='tct_interface',
                categoria='tct'
            )
            return None
    
    def _measurement_loop(self, symbols: List[str], timeframes: List[str]):
        """Loop principal de mediciones (thread background)"""
        
        enviar_senal_log(
            level='DEBUG',
            message="🔄 MEASUREMENT LOOP iniciado",
            emisor='tct_interface',
            categoria='tct'
        )
        
        while self._running:
            try:
                # 🔄 MEDIR TODOS LOS SYMBOL/TIMEFRAME COMBINATIONS
                for symbol in symbols:
                    if not self._running:
                        break
                    
                    for timeframe in timeframes:
                        if not self._running:
                            break
                        
                        # 📊 REALIZAR MEDICIÓN AUTOMÁTICA
                        result = self.measure_single_analysis(symbol, timeframe)
                        
                        if result:
                            # 📝 LOG SUCCESS (sin detalles para evitar spam)
                            pass
                        else:
                            enviar_senal_log(
                                level='WARNING',
                                message=f"⚠️ Measurement failed | {symbol}_{timeframe}",
                                emisor='tct_interface',
                                categoria='tct'
                            )
                
                # ⏸️ PAUSA HASTA PRÓXIMA MEDICIÓN
                time.sleep(self.measurement_interval)
                
            except Exception as e:
                enviar_senal_log(
                    level='ERROR',
                    message=f"❌ ERROR en measurement loop: {str(e)}",
                    emisor='tct_interface',
                    categoria='tct'
                )
                time.sleep(self.measurement_interval)  # Continue after error
        
        enviar_senal_log(
            level='DEBUG',
            message="🔄 MEASUREMENT LOOP terminado",
            emisor='tct_interface',
            categoria='tct'
        )
    
    def _aggregation_loop(self):
        """Loop de agregación (thread background)"""
        
        enviar_senal_log(
            level='DEBUG',
            message="📊 AGGREGATION LOOP iniciado",
            emisor='tct_interface',
            categoria='tct'
        )
        
        while self._running:
            try:
                # ⏸️ ESPERAR INTERVALO DE AGREGACIÓN
                time.sleep(self.aggregation_interval)
                
                if not self._running:
                    break
                
                # 📊 EJECUTAR AGREGACIÓN
                self._last_aggregation = self.aggregator.aggregate_recent_measurements()
                
                if self._last_aggregation:
                    # 📝 CAJA NEGRA - LOG AGGREGATION
                    enviar_senal_log(
                        level='DEBUG',
                        message=f"📊 AGGREGATION COMPLETED | "
                               f"Grade: {self._last_aggregation.performance_grade} | "
                               f"Avg TCT: {self._last_aggregation.global_avg_tct_ms:.2f}ms | "
                               f"Timeframes: {self._last_aggregation.total_timeframes}",
                        emisor='tct_interface',
                        categoria='tct'
                    )
                    
                    enviar_senal_log(
                        level='INFO',
                        message="📊 TCT agregación completada",
                        emisor='tct_interface',
                        categoria='tct'
                    )
                    
                    # 💾 AUTO-EXPORT SI ESTÁ HABILITADO
                    if self.enable_exports:
                        self.export_tct_data("json")
                
            except Exception as e:
                enviar_senal_log(
                    level='ERROR',
                    message=f"❌ ERROR en aggregation loop: {str(e)}",
                    emisor='tct_interface',
                    categoria='tct'
                )
        
        enviar_senal_log(
            level='DEBUG',
            message="📊 AGGREGATION LOOP terminado",
            emisor='tct_interface',
            categoria='tct'
        )
    
    def _get_current_market_context(self, symbol: str, timeframe: str) -> MarketContext:
        """Obtiene contexto de mercado actual para análisis"""
        
        try:
            # 🔄 UTILIZAR FUNCIÓN DEL ICT ENGINE
            market_context = update_market_context(symbol, timeframe)
            
            # 📝 CAJA NEGRA - LOG CONTEXT
            enviar_senal_log(
                level='DEBUG',
                message=f"🧭 Market context updated | {symbol}_{timeframe}",
                emisor='tct_interface',
                categoria='tct'
            )
            
            return market_context
            
        except Exception as e:
            enviar_senal_log(
                level='ERROR',
                message=f"❌ ERROR obteniendo market context | {symbol}_{timeframe} | Error: {str(e)}",
                emisor='tct_interface',
                categoria='tct'
            )
            
            # 🔄 RETORNAR CONTEXTO BÁSICO EN CASO DE ERROR
            return MarketContext(
                symbol=symbol,
                timeframe=timeframe,
                current_price=1.0,  # Placeholder
                trend="UNDEFINED",
                volatility=0.0
            )
    
    def _execute_ict_analysis(self, symbol: str, timeframe: str, market_context: MarketContext) -> Dict:
        """
        Simula la ejecución del análisis ICT completo
        En implementación real, llamaría a las funciones del core ICT engine
        """
        
        try:
            # 🧠 ANÁLISIS ICT OPTIMIZADO
            analysis = OptimizedICTAnalysis()
            
            # 📍 DETECTAR POIS
            pois = encontrar_pois_multiples_para_dashboard(
                symbol=symbol,
                timeframe=timeframe,
                limit=10
            )
            
            # 🔍 ANÁLISIS DE CONFIANZA
            confidence = ConfidenceEngine()
            confidence_score = confidence.calculate_overall_confidence(market_context)
            
            # 📊 RESULTADO SIMULADO
            result = {
                "analysis_type": "complete_ict",
                "pois_detected": len(pois) if pois else 0,
                "confidence_score": confidence_score,
                "market_structure": market_context.trend if hasattr(market_context, 'trend') else "UNKNOWN",
                "analysis_timestamp": datetime.now().isoformat(),
                "patterns_found": ["FVG", "OB", "BOS"],  # Placeholder
                "trade_signals": 2  # Placeholder
            }
            
            return result
            
        except Exception as e:
            enviar_senal_log(
                level='ERROR',
                message=f"❌ ERROR en análisis ICT | {symbol}_{timeframe} | Error: {str(e)}",
                emisor='tct_interface',
                categoria='tct'
            )
            
            # 📊 RESULTADO BÁSICO EN CASO DE ERROR
            return {
                "analysis_type": "error_fallback",
                "pois_detected": 0,
                "confidence_score": 0.0,
                "market_structure": "ERROR",
                "analysis_timestamp": datetime.now().isoformat(),
                "patterns_found": [],
                "trade_signals": 0,
                "error": str(e)
            }
