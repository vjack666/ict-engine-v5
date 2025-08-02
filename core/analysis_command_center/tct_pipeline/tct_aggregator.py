#!/usr/bin/env python3
"""
🔄 TCT AGGREGATOR - Agregador Multi-Timeframe para mediciones TCT
BASADO EN: Lógica de frequency analysis del health_analyzer.py
PROTOCOLO: "Caja Negra" - Consolidación inteligente de métricas
"""

import datetime
from typing import Dict, List, Optional
from collections import defaultdict, deque
from dataclasses import dataclass

# 🔌 IMPORTS DEL ICT ENGINE
from sistema.logging_interface import enviar_senal_log
from .tct_measurements import TCTMetrics

@dataclass
class AggregatedTCTMetrics:
    """Métricas TCT agregadas por timeframe y sesión"""
    
    # 🕐 MÉTRICAS AGREGADAS POR TIMEFRAME
    timeframe_metrics: Dict[str, TCTMetrics] = None
    
    # 📊 MÉTRICAS CONSOLIDADAS GLOBALES
    global_avg_tct_ms: float = 0.0
    global_max_tct_ms: float = 0.0
    global_min_tct_ms: float = float('inf')
    
    # 🎯 ANÁLISIS DE TENDENCIAS
    tct_trend: str = "STABLE"  # IMPROVING, DEGRADING, STABLE
    performance_grade: str = "A"  # A, B, C, D, F
    
    # 📈 MÉTRICAS DE FRECUENCIA (como health_analyzer)
    measurements_per_minute: float = 0.0
    analysis_frequency_hz: float = 0.0
    
    # 🧬 METADATA
    aggregation_timestamp: str = ""
    total_timeframes: int = 0
    active_sessions: List[str] = None
    
    def __post_init__(self):
        if self.timeframe_metrics is None:
            self.timeframe_metrics = {}
        if self.active_sessions is None:
            self.active_sessions = []

class TCTAggregator:
    """
    Agregador de métricas TCT multi-timeframe
    Inspirado en _analyze_system_frequency del health_analyzer
    """
    
    def __init__(self):
        """Inicialización del agregador TCT"""
        
        # 🗃️ ALMACENAMIENTO POR TIMEFRAME (como health_analyzer por categorías)
        self.timeframe_data = defaultdict(list)  # {timeframe: [TCTMetrics]}
        self.session_data = defaultdict(list)    # {session: [TCTMetrics]}
        
        # 📊 HISTORIAL DE AGREGACIONES (deque como health_analyzer)
        self.aggregation_history = deque(maxlen=50)
        
        # ⏱️ TRACKING DE FRECUENCIA
        self.measurement_timestamps = deque(maxlen=100)
        
        # 📝 CAJA NEGRA - LOG INICIALIZACIÓN
        enviar_senal_log(
            level='DEBUG',
            message="TCT Aggregator inicializado | Listo para consolidación multi-timeframe",
            emisor='tct_aggregator',
            categoria='tct'
        )
        
        enviar_senal_log(
            level='INFO',
            message="TCT Aggregator - Sistema de consolidación activado",
            emisor='tct_aggregator',
            categoria='tct'
        )
    
    def add_metrics(self, timeframe: str, metrics: TCTMetrics, session: str = None):
        """
        Añade métricas TCT para un timeframe específico
        Similar a como health_analyzer acumula datos por categoría
        """
        
        # 🗃️ ALMACENAR POR TIMEFRAME
        self.timeframe_data[timeframe].append(metrics)
        
        # 🗃️ ALMACENAR POR SESIÓN (si se proporciona)
        if session:
            self.session_data[session].append(metrics)
        
        # ⏱️ REGISTRAR TIMESTAMP PARA FRECUENCIA
        timestamp = datetime.datetime.now()
        self.measurement_timestamps.append(timestamp)
        
        # 📝 CAJA NEGRA - LOG ADICIÓN
        enviar_senal_log(
            level='DEBUG',
            message=f"🔄 METRICS ADDED | TF: {timeframe} | Session: {session} | "
                   f"TCT: {metrics.avg_tct_ms:.2f}ms | Patterns: {metrics.patterns_analyzed}",
            emisor='tct_aggregator',
            categoria='tct'
        )
    
    def aggregate_all_timeframes(self) -> AggregatedTCTMetrics:
        """
        Agrega métricas de todos los timeframes
        Lógica inspirada en el análisis de frecuencia del health_analyzer
        """
        
        enviar_senal_log(
            level='DEBUG',
            message="🔄 Iniciando agregación completa de todos los timeframes",
            emisor='tct_aggregator',
            categoria='tct'
        )
        
        # 📊 INICIALIZAR MÉTRICAS AGREGADAS
        aggregated = AggregatedTCTMetrics()
        aggregated.aggregation_timestamp = datetime.datetime.now().isoformat()
        
        # 🔄 PROCESAR CADA TIMEFRAME
        all_avg_times = []
        all_max_times = []
        all_min_times = []
        
        for timeframe, metrics_list in self.timeframe_data.items():
            if not metrics_list:
                continue
                
            # 📊 CALCULAR MÉTRICAS CONSOLIDADAS PARA ESTE TIMEFRAME
            timeframe_avg = sum(m.avg_tct_ms for m in metrics_list) / len(metrics_list)
            timeframe_max = max(m.max_tct_ms for m in metrics_list)
            timeframe_min = min(m.min_tct_ms for m in metrics_list if m.min_tct_ms != float('inf'))
            
            # 🎯 CREAR MÉTRICA CONSOLIDADA PARA EL TIMEFRAME
            consolidated_metric = TCTMetrics()
            consolidated_metric.avg_tct_ms = timeframe_avg
            consolidated_metric.max_tct_ms = timeframe_max
            consolidated_metric.min_tct_ms = timeframe_min if timeframe_min != float('inf') else 0.0
            consolidated_metric.measurements_taken = sum(m.measurements_taken for m in metrics_list)
            consolidated_metric.patterns_analyzed = sum(m.patterns_analyzed for m in metrics_list)
            consolidated_metric.pois_processed = sum(m.pois_processed for m in metrics_list)
            consolidated_metric.current_timeframe = timeframe
            
            # 🗃️ ALMACENAR EN AGREGACIÓN
            aggregated.timeframe_metrics[timeframe] = consolidated_metric
            
            # 📊 ACUMULAR PARA GLOBALES
            all_avg_times.append(timeframe_avg)
            all_max_times.append(timeframe_max)
            if timeframe_min != float('inf'):
                all_min_times.append(timeframe_min)
            
            # 📝 CAJA NEGRA - LOG TIMEFRAME CONSOLIDADO
            enviar_senal_log(
                level='DEBUG',
                message=f"🔄 TF CONSOLIDATED | {timeframe} | Avg: {timeframe_avg:.2f}ms | "
                       f"Max: {timeframe_max:.2f}ms | Measurements: {consolidated_metric.measurements_taken}",
                emisor='tct_aggregator',
                categoria='tct'
            )
        
        # 🌍 CALCULAR MÉTRICAS GLOBALES
        if all_avg_times:
            aggregated.global_avg_tct_ms = sum(all_avg_times) / len(all_avg_times)
            aggregated.global_max_tct_ms = max(all_max_times)
            aggregated.global_min_tct_ms = min(all_min_times) if all_min_times else 0.0
        
        # 📈 CALCULAR FRECUENCIA (como health_analyzer)
        aggregated.measurements_per_minute, aggregated.analysis_frequency_hz = self._calculate_frequency()
        
        # 🎯 ANÁLISIS DE TENDENCIAS
        aggregated.tct_trend = self._analyze_trend()
        aggregated.performance_grade = self._calculate_performance_grade(aggregated.global_avg_tct_ms)
        
        # 🧬 METADATA
        aggregated.total_timeframes = len(self.timeframe_data)
        aggregated.active_sessions = list(self.session_data.keys())
        
        # 🗃️ GUARDAR EN HISTORIAL
        self.aggregation_history.append(aggregated)
        
        # 📝 CAJA NEGRA - LOG AGREGACIÓN COMPLETA
        enviar_senal_log(
            level='DEBUG',
            message=f"🔄 GLOBAL AGGREGATION | Avg: {aggregated.global_avg_tct_ms:.2f}ms | "
                   f"Timeframes: {aggregated.total_timeframes} | Trend: {aggregated.tct_trend} | "
                   f"Grade: {aggregated.performance_grade}",
            emisor='tct_aggregator',
            categoria='tct'
        )
        
        # 📋 INFO TERMINAL (SILENCIOSO)
        enviar_senal_log(
            level='INFO',
            message=f"🔄 TCT Agregación completada - {aggregated.total_timeframes} timeframes procesados",
            emisor='tct_aggregator',
            categoria='tct'
        )
        
        return aggregated
    
    def _calculate_frequency(self) -> tuple[float, float]:
        """
        Calcula frecuencia de mediciones (lógica de health_analyzer)
        Retorna: (measurements_per_minute, frequency_hz)
        """
        
        if len(self.measurement_timestamps) < 2:
            return 0.0, 0.0
        
        # 📊 TOMAR ÚLTIMAS 20 MEDICIONES (como health_analyzer toma últimos 10 ciclos)
        recent_timestamps = list(self.measurement_timestamps)[-20:] if len(self.measurement_timestamps) >= 20 else list(self.measurement_timestamps)
        
        if len(recent_timestamps) < 2:
            return 0.0, 0.0
        
        # ⏱️ CALCULAR DURACIÓN TOTAL
        first_time = recent_timestamps[0]
        last_time = recent_timestamps[-1]
        duration_minutes = (last_time - first_time).total_seconds() / 60
        
        if duration_minutes <= 0:
            return 0.0, 0.0
        
        # 📈 CALCULAR FRECUENCIAS
        measurements_count = len(recent_timestamps) - 1
        measurements_per_minute = measurements_count / duration_minutes
        frequency_hz = (measurements_count / duration_minutes) / 60
        
        # 📝 CAJA NEGRA - LOG FRECUENCIA
        enviar_senal_log(
            level='DEBUG',
            message=f"📈 FREQUENCY CALC | {measurements_per_minute:.2f} measurements/min | "
                   f"{frequency_hz:.4f} Hz | Duration: {duration_minutes:.1f}min",
            emisor='tct_aggregator',
            categoria='tct'
        )
        
        return measurements_per_minute, frequency_hz
    
    def _analyze_trend(self) -> str:
        """Analiza tendencia de performance basado en historial"""
        
        if len(self.aggregation_history) < 3:
            return "STABLE"
        
        # 📊 COMPARAR ÚLTIMAS 3 AGREGACIONES
        recent_averages = [agg.global_avg_tct_ms for agg in list(self.aggregation_history)[-3:]]
        
        # 🎯 DETERMINAR TENDENCIA
        if recent_averages[-1] < recent_averages[0] * 0.95:  # Mejora del 5%
            trend = "IMPROVING"
        elif recent_averages[-1] > recent_averages[0] * 1.05:  # Empeora del 5%
            trend = "DEGRADING"
        else:
            trend = "STABLE"
        
        # 📝 CAJA NEGRA - LOG TENDENCIA
        enviar_senal_log(
            level='DEBUG',
            message=f"📈 TREND ANALYSIS | {trend} | Recent avgs: {recent_averages}",
            emisor='tct_aggregator',
            categoria='tct'
        )
        
        return trend
    
    def _calculate_performance_grade(self, avg_tct_ms: float) -> str:
        """Calcula grado de rendimiento basado en tiempo promedio"""
        
        # 🎯 ESCALA DE GRADES (ajustable según benchmarks)
        if avg_tct_ms <= 100:    # < 100ms = Excelente
            grade = "A"
        elif avg_tct_ms <= 250:  # < 250ms = Bueno  
            grade = "B"
        elif avg_tct_ms <= 500:  # < 500ms = Aceptable
            grade = "C"
        elif avg_tct_ms <= 1000: # < 1s = Necesita mejora
            grade = "D"
        else:                    # > 1s = Crítico
            grade = "F"
        
        # 📝 CAJA NEGRA - LOG GRADE
        enviar_senal_log(
            level='DEBUG',
            message=f"🎯 PERFORMANCE GRADE | {grade} | Avg TCT: {avg_tct_ms:.2f}ms",
            emisor='tct_aggregator',
            categoria='tct'
        )
        
        return grade
    
    def get_timeframe_summary(self) -> Dict:
        """Genera resumen por timeframe para dashboard"""
        
        summary = {}
        
        for timeframe, metrics_list in self.timeframe_data.items():
            if not metrics_list:
                continue
                
            latest_metric = metrics_list[-1]  # Última métrica del timeframe
            
            summary[timeframe] = {
                "avg_tct_ms": latest_metric.avg_tct_ms,
                "max_tct_ms": latest_metric.max_tct_ms,
                "measurements_taken": latest_metric.measurements_taken,
                "patterns_analyzed": latest_metric.patterns_analyzed,
                "pois_processed": latest_metric.pois_processed,
                "sample_count": len(metrics_list)
            }
        
        # 📝 CAJA NEGRA - LOG SUMMARY
        enviar_senal_log(
            level='DEBUG',
            message=f"📋 TIMEFRAME SUMMARY | {summary}",
            emisor='tct_aggregator',
            categoria='tct'
        )
        
        return summary
