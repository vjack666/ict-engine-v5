#!/usr/bin/env python3
"""
🔄 TCT AGGREGATOR - Agregador Multi-Timeframe para mediciones TCT
BASADO EN: Lógica de frequency analysis del health_analyzer.py
PROTOCOLO: "Caja Negra" - Consolidación inteligente de métricas
"""

import datetime
from sistema.sic import Dict, List, Optional, Any
from collections import defaultdict, deque
from sistema.sic import dataclass, field

# 🔌 IMPORTS DEL ICT ENGINE
from sistema.sic import enviar_senal_log, log_tct
from .tct_measurements import TCTMetrics

@dataclass
class AggregatedTCTMetrics:
    """Métricas TCT agregadas por timeframe y sesión"""

    # 🕐 MÉTRICAS AGREGADAS POR TIMEFRAME
    timeframe_metrics: Dict[str, TCTMetrics] = field(default_factory=dict)

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
    active_sessions: List[str] = field(default_factory=list)

    def __post_init__(self):
        # Inicialización adicional si es necesaria
        pass


    def to_dict(self) -> Dict[str, Any]:
        """Convierte las métricas agregadas a diccionario para serialización"""

        # 📊 CONVERTIR TIMEFRAME_METRICS A DICT
        timeframe_dict = {}
        for tf, metrics in self.timeframe_metrics.items():
            timeframe_dict[tf] = metrics.to_dict()

        return {
            # 🕐 MÉTRICAS GLOBALES AGREGADAS
            'global_avg_tct_ms': self.global_avg_tct_ms,
            'global_max_tct_ms': self.global_max_tct_ms,
            'global_min_tct_ms': self.global_min_tct_ms,

            # 📊 MÉTRICAS POR TIMEFRAME
            'timeframe_metrics': timeframe_dict,

            # 🎯 ANÁLISIS DE TENDENCIAS Y PERFORMANCE
            'tct_trend': self.tct_trend,
            'performance_grade': self.performance_grade,

            # 📈 MÉTRICAS DE FRECUENCIA
            'measurements_per_minute': self.measurements_per_minute,
            'analysis_frequency_hz': self.analysis_frequency_hz,

            # 🧬 METADATA Y CONTEXTO
            'aggregation_timestamp': self.aggregation_timestamp,
            'total_timeframes': self.total_timeframes,
            'active_sessions': self.active_sessions
        }
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
            nivel='DEBUG',
            mensaje="TCT Aggregator inicializado | Listo para consolidación multi-timeframe",
            fuente='tct_aggregator',
            categoria='tct'
        )

        enviar_senal_log(
            nivel='INFO',
            mensaje="TCT Aggregator - Sistema de consolidación activado",
            fuente='tct_aggregator',
            categoria='tct'
        )

    def add_metrics(self, timeframe: str, metrics: TCTMetrics, session: Optional[str] = None):
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
            nivel='DEBUG',
            mensaje=f"🔄 METRICS ADDED | TF: {timeframe} | Session: {session} | "
                   f"TCT: {metrics.avg_tct_ms:.2f}ms | Patterns: {metrics.patterns_analyzed}",
            fuente='tct_aggregator',
            categoria='tct'
        )

    def aggregate_all_timeframes(self) -> AggregatedTCTMetrics:
        """
        Agrega métricas de todos los timeframes
        Lógica inspirada en el análisis de frecuencia del health_analyzer
        """

        enviar_senal_log(
            nivel='DEBUG',
            mensaje="🔄 Iniciando agregación completa de todos los timeframes",
            fuente='tct_aggregator',
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
                nivel='DEBUG',
                mensaje=f"🔄 TF CONSOLIDATED | {timeframe} | Avg: {timeframe_avg:.2f}ms | "
                       f"Max: {timeframe_max:.2f}ms | Measurements: {consolidated_metric.measurements_taken}",
                fuente='tct_aggregator',
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
            nivel='DEBUG',
            mensaje=f"🔄 GLOBAL AGGREGATION | Avg: {aggregated.global_avg_tct_ms:.2f}ms | "
                   f"Timeframes: {aggregated.total_timeframes} | Trend: {aggregated.tct_trend} | "
                   f"Grade: {aggregated.performance_grade}",
            fuente='tct_aggregator',
            categoria='tct'
        )

        # 📋 INFO TERMINAL (SILENCIOSO)
        enviar_senal_log(
            nivel='INFO',
            mensaje=f"🔄 TCT Agregación completada - {aggregated.total_timeframes} timeframes procesados",
            fuente='tct_aggregator',
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
            nivel='DEBUG',
            mensaje=f"📈 FREQUENCY CALC | {measurements_per_minute:.2f} measurements/min | "
                   f"{frequency_hz:.4f} Hz | Duration: {duration_minutes:.1f}min",
            fuente='tct_aggregator',
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
            nivel='DEBUG',
            mensaje=f"📈 TREND ANALYSIS | {trend} | Recent avgs: {recent_averages}",
            fuente='tct_aggregator',
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
            nivel='DEBUG',
            mensaje=f"🎯 PERFORMANCE GRADE | {grade} | Avg TCT: {avg_tct_ms:.2f}ms",
            fuente='tct_aggregator',
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
            nivel='DEBUG',
            mensaje=f"📋 TIMEFRAME SUMMARY | {summary}",
            fuente='tct_aggregator',
            categoria='tct'
        )

        return summary

    def aggregate_recent_measurements(self,
                                    timeframe: str = "ALL",
                                    max_age_minutes: int = 60,
                                    min_samples: int = 5) -> Optional[AggregatedTCTMetrics]:
        """
        🚀 MÉTODO CRÍTICO: Agrega solo las mediciones recientes
        Útil para análisis en tiempo real y dashboard updates

        Args:
            timeframe: Timeframe específico ("M5", "H1", etc.) o "ALL" para todos
            max_age_minutes: Edad máxima de las mediciones en minutos
            min_samples: Mínimo número de samples requeridos

        Returns:
            AggregatedTCTMetrics con solo datos recientes o None si insuficientes datos
        """

        enviar_senal_log(
            nivel='DEBUG',
            mensaje=f"📊 AGGREGATE RECENT | TF: {timeframe} | Max age: {max_age_minutes}min | Min samples: {min_samples}",
            fuente='tct_aggregator',
            categoria='tct'
        )

        current_time = datetime.datetime.now()
        cutoff_time = current_time - datetime.timedelta(minutes=max_age_minutes)

        # 🔄 FILTRAR TIMESTAMPS RECIENTES
        recent_timestamps = [
            ts for ts in self.measurement_timestamps
            if ts >= cutoff_time
        ]

        if len(recent_timestamps) < min_samples:
            enviar_senal_log(
                nivel='WARNING',
                mensaje=f"⚠️ Insuficientes mediciones recientes: {len(recent_timestamps)} < {min_samples}",
                fuente='tct_aggregator',
                categoria='tct'
            )
            return None

        # 📊 INICIALIZAR MÉTRICAS AGREGADAS RECIENTES
        aggregated = AggregatedTCTMetrics()
        aggregated.aggregation_timestamp = current_time.isoformat()

        # 🎯 PROCESAR TIMEFRAMES ESPECÍFICOS O TODOS
        target_timeframes = [timeframe] if timeframe != "ALL" else list(self.timeframe_data.keys())

        recent_metrics_found = False
        all_avg_times = []
        all_max_times = []
        all_min_times = []

        for tf in target_timeframes:
            if tf not in self.timeframe_data or not self.timeframe_data[tf]:
                continue

            # 🕐 FILTRAR MÉTRICAS RECIENTES POR TIMESTAMP
            # Nota: Asumimos que las métricas están ordenadas cronológicamente
            recent_metrics = []

            # Tomar las últimas métricas dentro del rango de tiempo
            for i in range(len(self.timeframe_data[tf]) - 1, -1, -1):
                # Aproximar que cada métrica corresponde a un timestamp
                if i < len(recent_timestamps):
                    recent_metrics.append(self.timeframe_data[tf][i])
                if len(recent_metrics) >= min_samples:
                    break

            if not recent_metrics:
                continue

            recent_metrics_found = True

            # 📊 CALCULAR MÉTRICAS CONSOLIDADAS PARA ESTE TIMEFRAME (RECIENTES)
            tf_avg = sum(m.avg_tct_ms for m in recent_metrics) / len(recent_metrics)
            tf_max = max(m.max_tct_ms for m in recent_metrics)
            tf_min = min(m.min_tct_ms for m in recent_metrics if m.min_tct_ms != float('inf'))

            # 🎯 CREAR MÉTRICA CONSOLIDADA RECIENTE
            consolidated_metric = TCTMetrics()
            consolidated_metric.avg_tct_ms = tf_avg
            consolidated_metric.max_tct_ms = tf_max
            consolidated_metric.min_tct_ms = tf_min if tf_min != float('inf') else 0.0
            consolidated_metric.measurements_taken = len(recent_metrics)
            consolidated_metric.patterns_analyzed = sum(m.patterns_analyzed for m in recent_metrics)
            consolidated_metric.pois_processed = sum(m.pois_processed for m in recent_metrics)
            consolidated_metric.current_timeframe = tf

            # 🗃️ ALMACENAR EN AGREGACIÓN
            aggregated.timeframe_metrics[tf] = consolidated_metric

            # 📊 ACUMULAR PARA GLOBALES
            all_avg_times.append(tf_avg)
            all_max_times.append(tf_max)
            if tf_min != float('inf'):
                all_min_times.append(tf_min)

            enviar_senal_log(
                nivel='DEBUG',
                mensaje=f"📊 RECENT TF PROCESSED | {tf} | Avg: {tf_avg:.2f}ms | Samples: {len(recent_metrics)}",
                fuente='tct_aggregator',
                categoria='tct'
            )

        if not recent_metrics_found:
            enviar_senal_log(
                nivel='WARNING',
                mensaje=f"⚠️ No se encontraron métricas recientes para timeframe: {timeframe}",
                fuente='tct_aggregator',
                categoria='tct'
            )
            return None

        # 🌍 CALCULAR MÉTRICAS GLOBALES RECIENTES
        if all_avg_times:
            aggregated.global_avg_tct_ms = sum(all_avg_times) / len(all_avg_times)
            aggregated.global_max_tct_ms = max(all_max_times)
            aggregated.global_min_tct_ms = min(all_min_times) if all_min_times else 0.0

        # 📈 CALCULAR FRECUENCIA RECIENTE
        if len(recent_timestamps) >= 2:
            duration_minutes = (recent_timestamps[-1] - recent_timestamps[0]).total_seconds() / 60
            if duration_minutes > 0:
                measurements_count = len(recent_timestamps) - 1
                aggregated.measurements_per_minute = measurements_count / duration_minutes
                aggregated.analysis_frequency_hz = (measurements_count / duration_minutes) / 60

        # 🎯 ANÁLISIS DE TENDENCIAS RECIENTES
        aggregated.tct_trend = self._analyze_trend()  # Reutilizar método existente
        aggregated.performance_grade = self._calculate_performance_grade(aggregated.global_avg_tct_ms)

        # 🧬 METADATA
        aggregated.total_timeframes = len(aggregated.timeframe_metrics)
        aggregated.active_sessions = list(self.session_data.keys())

        enviar_senal_log(
            nivel='INFO',
            mensaje=f"✅ Agregación reciente completada | TFs: {aggregated.total_timeframes} | Avg: {aggregated.global_avg_tct_ms:.2f}ms",
            fuente='tct_aggregator',
            categoria='tct'
        )

        return aggregated
