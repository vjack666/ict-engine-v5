#!/usr/bin/env python3
"""
🧠 ICT HISTORICAL ANALYZER - SENTINEL GRID SYSTEM v3.4
Análisis histórico de rendimiento de POIs para scoring dinámico
Fecha: 2025-07-24
Componente: FASE 2.4 - Integración Smart Logger Completa
"""

import json
from json import JSONDecodeError
import pandas as pd
# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log, log_ict

from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class ICTHistoricalAnalyzer:
    """
    Analiza el rendimiento histórico de POIs basado en logs del Smart Logger
    para proporcionar scoring dinámico y adaptativo.
    """

    def __init__(self, logs_dir: str = "logs"):
        self.logs_dir = Path(logs_dir)
        self.analysis_dir = self.logs_dir / "analysis"
        self.cache = {}
        self.cache_timestamp = None
        self.cache_ttl = timedelta(hours=1)  # Cache por 1 hora

        # Configuración de pesos para análisis
        self.config = {
            'min_samples': 5,  # Mínimo de muestras para análisis confiable
            'success_threshold': 0.7,  # 70% de éxito para considerarse "exitoso"
            'time_decay_factor': 0.1,  # Factor de decaimiento temporal
            'max_lookback_days': 30,  # Máximo 30 días de lookback
            'weight_multipliers': {
                'ORDER_BLOCK': 1.0,
                'FAIR_VALUE_GAP': 1.1,
                'LIQUIDITY_POOL': 1.2,
                'H4_BIAS': 0.9
            }
        }

    def get_historical_poi_performance(self, poi_type: str, timeframe: str = "M15",
                                     symbol: str = "EURUSD") -> float:
        """
        Obtiene el factor de ponderación histórico para un tipo de POI específico.

        Args:
            poi_type: Tipo de POI (ORDER_BLOCK, FAIR_VALUE_GAP, etc.)
            timeframe: Marco temporal (M15, H4, etc.)
            symbol: Símbolo del mercado

        Returns:
            float: Factor de ponderación (1.0 = neutral, >1.0 = mejor rendimiento, <1.0 = peor)
        """

        # Verificar cache
        cache_key = f"{poi_type}_{timeframe}_{symbol}"
        if self._is_cache_valid() and cache_key in self.cache:
            return self.cache[cache_key]

        try:
            # Cargar datos históricos
            historical_data = self._load_historical_logs(poi_type, timeframe, symbol)

            if not historical_data or len(historical_data) < self.config['min_samples']:
                # No hay suficientes datos históricos, usar peso base
                weight = self.config['weight_multipliers'].get(poi_type, 1.0)
                enviar_senal_log("WARNING", f"[COLD_START] 🟡 Datos insuficientes para {poi_type} "
                             f"({len(historical_data) if historical_data else 0} muestras), "
                             f"usando peso base: {weight}", __name__, "general")
                self.cache[cache_key] = weight
                return weight

            # Calcular rendimiento histórico
            success_rate = self._calculate_success_rate(historical_data)
            time_weighted_rate = self._apply_time_decay(historical_data, success_rate)

            # Convertir tasa de éxito a factor de ponderación
            weight = self._success_rate_to_weight(time_weighted_rate, poi_type)

            # Cachear resultado
            self.cache[cache_key] = weight
            self._update_cache_timestamp()

            enviar_senal_log("INFO", f"Performance histórica {poi_type}/{timeframe}: "
                       f"éxito={success_rate:.2%}, peso ajustado={weight:.3f}", __name__, "general")

            return weight

        except FileNotFoundError as e:
            enviar_senal_log("WARNING", f"[COLD_START] 🟡 Archivos de logs no encontrados para {poi_type}: {e}", __name__, "general")
            weight = self.config['weight_multipliers'].get(poi_type, 1.0)
            self.cache[cache_key] = weight
            return weight
        except pd.errors.EmptyDataError as e:
            enviar_senal_log("WARNING", f"[DATA_ERROR] 🟡 Logs vacíos o corruptos para {poi_type}: {e}", __name__, "general")
            weight = self.config['weight_multipliers'].get(poi_type, 1.0)
            self.cache[cache_key] = weight
            return weight
        except (JSONDecodeError, ValueError) as e:
            enviar_senal_log("ERROR", f"[HISTORICAL_ERROR] ❌ Error calculando performance histórica para {poi_type}: {e}", __name__, "general")
            # Fallback a peso base
            weight = self.config['weight_multipliers'].get(poi_type, 1.0)
            self.cache[cache_key] = weight
            return weight

    def get_poi_confidence_score(self, poi_data: Dict) -> float:
        """
        Calcula un score de confianza basado en análisis histórico.

        Args:
            poi_data: Diccionario con datos del POI

        Returns:
            float: Score de confianza (0.0-1.0)
        """
        try:
            poi_type = poi_data.get('type', 'UNKNOWN')
            timeframe = poi_data.get('timeframe', 'M15')
            symbol = poi_data.get('symbol', 'EURUSD')

            # Obtener weight histórico
            historical_weight = self.get_historical_poi_performance(poi_type, timeframe, symbol)

            # Score base del POI
            base_score = poi_data.get('score', 0.5)
            base_confidence = poi_data.get('confidence', 0.5)

            # Calcular confianza ajustada
            adjusted_confidence = min(1.0, base_confidence * historical_weight)

            # Factores adicionales
            freshness_factor = self._calculate_freshness_factor(poi_data)
            confluence_factor = self._calculate_confluence_factor(poi_data)

            # Score final de confianza
            final_confidence = adjusted_confidence * freshness_factor * confluence_factor

            return min(1.0, max(0.0, final_confidence))

        except (JSONDecodeError, ValueError) as e:
            enviar_senal_log("ERROR", f"Error calculando confidence score: {e}", __name__, "general")
            return 0.5  # Valor neutral por defecto

    def generate_performance_report(self, days_back: int = 7) -> Dict:
        """
        Genera un reporte de rendimiento de POIs para los últimos N días.

        Args:
            days_back: Días hacia atrás para el análisis

        Returns:
            Dict: Reporte con estadísticas de rendimiento
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days_back)

            # Cargar todos los logs relevantes
            all_logs = self._load_all_recent_logs(cutoff_date)

            if not all_logs:
                return {'error': 'No hay datos suficientes para generar reporte'}

            # Análisis por tipo de POI
            performance_by_type = {}
            total_detections = 0
            total_successes = 0

            for poi_type in ['ORDER_BLOCK', 'FAIR_VALUE_GAP', 'LIQUIDITY_POOL', 'H4_BIAS']:
                type_entries = [entry for entry in all_logs if entry.get('poi_type') == poi_type]

                if type_entries:
                    success_rate = self._calculate_success_rate(type_entries)
                    avg_confidence = sum(entry.get('confidence', 0) for entry in type_entries) / len(type_entries)

                    performance_by_type[poi_type] = {
                        'detections': len(type_entries),
                        'success_rate': success_rate,
                        'avg_confidence': avg_confidence,
                        'current_weight': self.get_historical_poi_performance(poi_type)
                    }

                    total_detections += len(type_entries)
                    total_successes += len([entry for entry in type_entries if entry.get('success', False)])

            # Estadísticas globales
            overall_success_rate = total_successes / total_detections if total_detections > 0 else 0

            report = {
                'period': f"Últimos {days_back} días",
                'generated_at': datetime.now().isoformat(),
                'overall_stats': {
                    'total_detections': total_detections,
                    'overall_success_rate': overall_success_rate,
                    'total_successes': total_successes
                },
                'performance_by_type': performance_by_type,
                'recommendations': self._generate_recommendations(performance_by_type)
            }

            return report

        except (JSONDecodeError, ValueError) as e:
            enviar_senal_log("ERROR", f"Error generando reporte de performance: {e}", __name__, "general")
            return {'error': f'Error generando reporte: {str(e)}'}

    def _load_historical_logs(self, poi_type: str, timeframe: str, symbol: str) -> List[Dict]:
        """Carga logs históricos filtrados por tipo de POI."""
        logs = []

        try:
            # Buscar archivos de logs de análisis
            if self.analysis_dir.exists():
                for log_file in self.analysis_dir.glob("*.jsonl"):
                    with open(log_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            try:
                                log_entry = json.loads(line.strip())
                                if (log_entry.get('poi_type') == poi_type and
                                    log_entry.get('timeframe') == timeframe and
                                    log_entry.get('symbol') == symbol):
                                    logs.append(log_entry)
                            except json.JSONDecodeError:
                                continue

            # También buscar en archivos JSON individuales
            json_files = list(self.analysis_dir.glob("*.json"))
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            for entry in data:
                                if (entry.get('poi_type') == poi_type and
                                    entry.get('timeframe') == timeframe and
                                    entry.get('symbol') == symbol):
                                    logs.append(entry)
                        elif (data.get('poi_type') == poi_type and
                              data.get('timeframe') == timeframe and
                              data.get('symbol') == symbol):
                            logs.append(data)
                except (json.JSONDecodeError, FileNotFoundError):
                    continue

            # Filtrar por fecha (últimos N días)
            cutoff_date = datetime.now() - timedelta(days=self.config['max_lookback_days'])

            filtered_logs = []
            for entry in logs:
                try:
                    entry_date = datetime.fromisoformat(entry.get('timestamp', '').replace('Z', '+00:00'))
                    if entry_date >= cutoff_date:
                        filtered_logs.append(entry)
                except (ValueError, TypeError):
                    continue

            return filtered_logs

        except (JSONDecodeError, ValueError) as e:
            enviar_senal_log("ERROR", f"Error cargando logs históricos: {e}", __name__, "general")
            return []

    def _load_all_recent_logs(self, cutoff_date: datetime) -> List[Dict]:
        """Carga todos los logs recientes para análisis de reporte."""
        all_logs = []

        try:
            if self.analysis_dir.exists():
                for log_file in self.analysis_dir.glob("*.json*"):
                    try:
                        with open(log_file, 'r', encoding='utf-8') as f:
                            if log_file.suffix == '.jsonl':
                                for line in f:
                                    try:
                                        log_entry = json.loads(line.strip())
                                        log_date = datetime.fromisoformat(
                                            log_entry.get('timestamp', '').replace('Z', '+00:00')
                                        )
                                        if log_date >= cutoff_date:
                                            all_logs.append(log_entry)
                                    except (json.JSONDecodeError, ValueError):
                                        continue
                            else:
                                data = json.load(f)
                                if isinstance(data, list):
                                    for entry in data:
                                        try:
                                            log_date = datetime.fromisoformat(
                                                entry.get('timestamp', '').replace('Z', '+00:00')
                                            )
                                            if log_date >= cutoff_date:
                                                all_logs.append(entry)
                                        except (ValueError, TypeError):
                                            continue
                                else:
                                    try:
                                        log_date = datetime.fromisoformat(
                                            data.get('timestamp', '').replace('Z', '+00:00')
                                        )
                                        if log_date >= cutoff_date:
                                            all_logs.append(data)
                                    except (ValueError, TypeError):
                                        continue
                    except (FileNotFoundError, json.JSONDecodeError):
                        continue

            return all_logs

        except (JSONDecodeError, ValueError) as e:
            enviar_senal_log("ERROR", f"Error cargando logs recientes: {e}", __name__, "general")
            return []

    def _calculate_success_rate(self, entries: List[Dict]) -> float:
        """Calcula la tasa de éxito de los entries."""
        if not entries:
            return 0.5  # Valor neutral

        successes = sum(1 for entry in entries if entry.get('success', False))
        return successes / len(entries)

    def _apply_time_decay(self, entries: List[Dict], base_rate: float) -> float:
        """Aplica decaimiento temporal a la tasa de éxito."""
        if not entries:
            return base_rate

        now = datetime.now()
        weighted_sum = 0
        total_weight = 0

        for entry in entries:
            try:
                entry_date = datetime.fromisoformat(entry.get('timestamp', '').replace('Z', '+00:00'))
                days_old = (now - entry_date).days
                weight = max(0.1, 1.0 - (days_old * self.config['time_decay_factor']))

                success_value = 1.0 if entry.get('success', False) else 0.0
                weighted_sum += success_value * weight
                total_weight += weight

            except (ValueError, TypeError):
                continue

        return weighted_sum / total_weight if total_weight > 0 else base_rate

    def _success_rate_to_weight(self, success_rate: float, poi_type: str) -> float:
        """Convierte tasa de éxito a factor de ponderación."""
        base_multiplier = self.config['weight_multipliers'].get(poi_type, 1.0)

        # Mapear tasa de éxito a rango de ponderación (0.5 - 1.5)
        if success_rate >= self.config['success_threshold']:
            # Alto rendimiento: peso entre 1.0 y 1.5
            weight_factor = 1.0 + (success_rate - self.config['success_threshold']) * 1.67
        else:
            # Bajo rendimiento: peso entre 0.5 y 1.0
            weight_factor = 0.5 + (success_rate / self.config['success_threshold']) * 0.5

        return base_multiplier * weight_factor

    def _calculate_freshness_factor(self, poi_data: Dict) -> float:
        """Calcula factor de frescura del POI."""
        try:
            timestamp = poi_data.get('timestamp')
            if not timestamp:
                return 1.0

            poi_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            hours_old = (datetime.now() - poi_date).total_seconds() / 3600

            # Factor de frescura: 1.0 para POIs frescos, decae con el tiempo
            return max(0.5, 1.0 - (hours_old / 168))  # Decae en 7 días

        except (ValueError, TypeError):
            return 1.0

    def _calculate_confluence_factor(self, poi_data: Dict) -> float:
        """Calcula factor de confluencia del POI."""
        try:
            confluence_count = poi_data.get('confluence_count', 1)
            # Factor de confluencia: 1.0 base, +10% por cada confluencia adicional
            return min(1.5, 1.0 + (confluence_count - 1) * 0.1)
        except (ValueError, TypeError):
            return 1.0

    def _generate_recommendations(self, performance_data: Dict) -> List[str]:
        """Genera recomendaciones basadas en el análisis de rendimiento."""
        recommendations = []

        try:
            for poi_type, stats in performance_data.items():
                success_rate = stats.get('success_rate', 0)
                detections = stats.get('detections', 0)

                if detections < self.config['min_samples']:
                    recommendations.append(
                        f"{poi_type}: Necesita más datos históricos (solo {detections} muestras)"
                    )
                elif success_rate < 0.4:
                    recommendations.append(
                        f"{poi_type}: Bajo rendimiento ({success_rate:.1%}) - considerar revisar criterios"
                    )
                elif success_rate > 0.8:
                    recommendations.append(
                        f"{poi_type}: Excelente rendimiento ({success_rate:.1%}) - mantener estrategia"
                    )

            if not recommendations:
                recommendations.append("Rendimiento general estable - continuar monitoreo")

            return recommendations

        except (JSONDecodeError, ValueError) as e:
            enviar_senal_log("ERROR", f"Error generando recomendaciones: {e}", __name__, "general")
            return ["Error generando recomendaciones"]

    def _is_cache_valid(self) -> bool:
        """Verifica si el cache es válido."""
        if not self.cache_timestamp:
            return False
        return datetime.now() - self.cache_timestamp < self.cache_ttl

    def _update_cache_timestamp(self):
        """Actualiza el timestamp del cache."""
        self.cache_timestamp = datetime.now()

# Instancia global del analizador
historical_analyzer = ICTHistoricalAnalyzer()

# Funciones de conveniencia para importación fácil
def get_historical_poi_performance(poi_type: str, timeframe: str = "M15", symbol: str = "EURUSD") -> float:
    """Función de conveniencia para obtener performance histórica."""
    return historical_analyzer.get_historical_poi_performance(poi_type, timeframe, symbol)

def get_poi_confidence_score(poi_data: Dict) -> float:
    """Función de conveniencia para obtener score de confianza."""
    return historical_analyzer.get_poi_confidence_score(poi_data)

def generate_performance_report(days_back: int = 7) -> Dict:
    """Función de conveniencia para generar reporte de performance."""
    return historical_analyzer.generate_performance_report(days_back)
