#!/usr/bin/env python3
"""
⚡ TCT MEASUREMENTS ENGINE - Motor de Mediciones Time-to-Complete
BASADO EN: health_analyzer.py (SENTINEL_ICT_ANALYZER - backup)
ADAPTADO PARA: Pipeline TCT en ICT Engine v3.4
PROTOCOLO: "Caja Negra" - Telemetría exhaustiva, terminal silencioso
"""

from sistema.sic import time
import datetime
from sistema.sic import dataclass, asdict
from collections import deque
from sistema.sic import Dict, List, Optional, Any
from sistema.sic import Path

# 🔌 IMPORTS DEL ICT ENGINE
from sistema.sic import enviar_senal_log, log_tct

@dataclass
class TCTMetrics:
    """Métricas de Time-to-Complete para análisis ICT"""

    # 🕐 MÉTRICAS DE TIEMPO CORE (Adaptado de SystemHealthMetrics)
    avg_tct_ms: float = 0.0                    # Tiempo promedio completo
    max_tct_ms: float = 0.0                    # Tiempo máximo registrado
    min_tct_ms: float = float('inf')           # Tiempo mínimo registrado

    # 📊 MÉTRICAS DE ANÁLISIS ICT
    analysis_start_time: Optional[str] = None  # Timestamp inicio análisis
    analysis_end_time: Optional[str] = None    # Timestamp fin análisis
    analysis_duration_ms: float = 0.0          # Duración total del análisis

    # 🎯 MÉTRICAS DE PATRONES
    patterns_analyzed: int = 0                 # Cantidad de patrones procesados
    pois_processed: int = 0                    # POIs procesados
    confidence_calculations: int = 0           # Cálculos de confianza realizados

    # 📈 MÉTRICAS DE RENDIMIENTO
    cycles_completed: int = 0                  # Ciclos completados (como health_analyzer)
    measurements_taken: int = 0               # Total de mediciones tomadas

    # 🧬 METADATA DE CONTEXTO
    current_symbol: Optional[str] = None       # Símbolo actual
    current_timeframe: Optional[str] = None    # Timeframe actual
    market_session: Optional[str] = None       # Sesión de mercado

    def to_dict(self) -> Dict:
        """Convierte a diccionario para serialización (igual que health_analyzer)"""
        return asdict(self)

class TCTMeasurementEngine:
    """
    Motor de mediciones TCT - Adaptado de SystemHealthAnalyzer
    Mide el tiempo completo de análisis ICT desde inicio hasta finalización
    """

    def __init__(self, logs_directory: str = "data/logs/tct"):
        """Inicialización del motor TCT"""
        self.logs_dir = Path(logs_directory)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # 📊 MÉTRICAS PRINCIPALES
        self.metrics = TCTMetrics()

        # 🗃️ DEQUE PARA SAMPLES (Igual que health_analyzer)
        self.tct_samples = deque(maxlen=100)      # Últimas 100 mediciones TCT
        self.analysis_history = deque(maxlen=50)  # Historial de análisis

        # ⏱️ TRACKING DE TIEMPO
        self._measurement_start_time = None
        self._active_measurements = {}  # Para múltiples mediciones concurrentes

        # 📝 CAJA NEGRA - LOG DETALLADO
        enviar_senal_log(
            nivel='DEBUG',
            mensaje=f"🎯 TCT Measurement Engine inicializado | Logs: {self.logs_dir}",
            fuente='tct_measurements',
            categoria='tct'
        )

        # 📋 INFO TERMINAL (SILENCIOSO)
        enviar_senal_log(
            nivel='INFO',
            mensaje="TCT Pipeline - Motor de mediciones activado",
            fuente='tct_measurements',
            categoria='tct'
        )

    def start_measurement(self, measurement_id: str = "default", context: Optional[Dict] = None) -> str:
        """
        Inicia una medición TCT (equivalente a [REQUEST-DASHBOARD])
        Retorna: ID único de la medición
        """
        timestamp = datetime.datetime.now()
        measurement_key = f"{measurement_id}_{timestamp.strftime('%H%M%S%f')}"

        # 🕐 REGISTRAR INICIO
        self._active_measurements[measurement_key] = {
            'start_time': timestamp,
            'start_time_ms': time.time() * 1000,
            'context': context or {},
            'measurement_id': measurement_id
        }

        # 📝 CAJA NEGRA - LOG DETALLADO
        enviar_senal_log(
            nivel='DEBUG',
            mensaje=f"🕐 TCT START | ID: {measurement_key} | Context: {context}",
            fuente='tct_measurements',
            categoria='tct'
        )

        return measurement_key

    def end_measurement(self, measurement_key: str, results: Optional[Dict] = None) -> float:
        """
        Finaliza una medición TCT (equivalente a [RESPONSE-DASHBOARD])
        Retorna: Duración en milisegundos
        """
        if measurement_key not in self._active_measurements:
            enviar_senal_log(
                nivel='WARNING',
                mensaje=f"⚠️ TCT measurement key no encontrado: {measurement_key}",
                fuente='tct_measurements',
                categoria='tct'
            )
            return 0.0

        # 🕐 CALCULAR DURACIÓN (Igual que health_analyzer)
        end_time = time.time() * 1000
        start_data = self._active_measurements[measurement_key]
        duration_ms = end_time - start_data['start_time_ms']

        # 📊 ACTUALIZAR MÉTRICAS (Lógica de health_analyzer adaptada)
        self._update_metrics(duration_ms, start_data, results)

        # 🗃️ GUARDAR EN HISTORIAL
        self.tct_samples.append(duration_ms)
        self.analysis_history.append({
            'measurement_id': start_data['measurement_id'],
            'duration_ms': duration_ms,
            'timestamp': datetime.datetime.now().isoformat(),
            'context': start_data['context'],
            'results': results or {}
        })

        # 📝 CAJA NEGRA - LOG DETALLADO
        enviar_senal_log(
            nivel='DEBUG',
            mensaje=f"🕐 TCT END | ID: {measurement_key} | Duration: {duration_ms:.2f}ms | Results: {results}",
            fuente='tct_measurements',
            categoria='tct'
        )

        # 🧹 LIMPIAR MEDICIÓN ACTIVA
        del self._active_measurements[measurement_key]

        return duration_ms

    def _update_metrics(self, duration_ms: float, start_data: Dict, results: Optional[Dict]):
        """Actualiza métricas internas (lógica de health_analyzer)"""

        # 🕐 ACTUALIZAR MÉTRICAS DE TIEMPO
        if duration_ms > 0:  # Filtro de sanidad
            self.metrics.measurements_taken += 1

            # 📊 ESTADÍSTICAS DE TIEMPO (igual que health_analyzer)
            if self.metrics.measurements_taken == 1:
                self.metrics.avg_tct_ms = duration_ms
                self.metrics.max_tct_ms = duration_ms
                self.metrics.min_tct_ms = duration_ms
            else:
                # Promedio móvil
                total_previous = self.metrics.avg_tct_ms * (self.metrics.measurements_taken - 1)
                self.metrics.avg_tct_ms = (total_previous + duration_ms) / self.metrics.measurements_taken

                # Min/Max
                self.metrics.max_tct_ms = max(self.metrics.max_tct_ms, duration_ms)
                self.metrics.min_tct_ms = min(self.metrics.min_tct_ms, duration_ms)

        # 🎯 ACTUALIZAR CONTEXTO
        context = start_data.get('context', {})
        if 'symbol' in context:
            self.metrics.current_symbol = context['symbol']
        if 'timeframe' in context:
            self.metrics.current_timeframe = context['timeframe']
        if 'session' in context:
            self.metrics.market_session = context['session']

        # 📈 ACTUALIZAR CONTADORES DE ANÁLISIS
        if results:
            if 'patterns_found' in results:
                self.metrics.patterns_analyzed += results.get('patterns_count', 0)
            if 'pois_found' in results:
                self.metrics.pois_processed += results.get('pois_count', 0)
            if 'confidence_calculated' in results:
                self.metrics.confidence_calculations += 1

    def get_current_metrics(self) -> TCTMetrics:
        """Retorna métricas actuales (API igual que health_analyzer)"""

        # 📊 ACTUALIZAR CICLOS COMPLETADOS
        self.metrics.cycles_completed = len(self.analysis_history)

        # 📝 CAJA NEGRA - LOG MÉTRICS SNAPSHOT
        enviar_senal_log(
            nivel='DEBUG',
            mensaje=f"📊 TCT METRICS | Avg: {self.metrics.avg_tct_ms:.2f}ms | "
                   f"Cycles: {self.metrics.cycles_completed} | "
                   f"Patterns: {self.metrics.patterns_analyzed}",
            fuente='tct_measurements',
            categoria='tct'
        )

        return self.metrics

    def get_performance_summary(self) -> Dict:
        """Genera resumen de rendimiento (como health_analyzer.to_dict())"""

        metrics = self.get_current_metrics()

        summary = {
            "performance": {
                "avg_tct_ms": metrics.avg_tct_ms,
                "max_tct_ms": metrics.max_tct_ms,
                "min_tct_ms": metrics.min_tct_ms,
                "measurements_taken": metrics.measurements_taken
            },
            "analysis": {
                "cycles_completed": metrics.cycles_completed,
                "patterns_analyzed": metrics.patterns_analyzed,
                "pois_processed": metrics.pois_processed,
                "confidence_calculations": metrics.confidence_calculations
            },
            "context": {
                "current_symbol": metrics.current_symbol,
                "current_timeframe": metrics.current_timeframe,
                "market_session": metrics.market_session
            },
            "samples": {
                "recent_tct_samples": list(self.tct_samples)[-10:],  # Últimas 10
                "total_samples": len(self.tct_samples)
            }
        }

        # 📝 CAJA NEGRA - LOG SUMMARY COMPLETO
        enviar_senal_log(
            nivel='DEBUG',
            mensaje=f"📋 TCT PERFORMANCE SUMMARY | {summary}",
            fuente='tct_measurements',
            categoria='tct'
        )

        return summary
