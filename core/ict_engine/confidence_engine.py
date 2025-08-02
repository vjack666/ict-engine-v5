"""
🧠 ICT CONFIDENCE ENGINE - Motor de Confianza Inteligente
========================================================

Motor unificado que calcula scores de confianza para patrones ICT usando:
- Análisis base del patrón (pattern_analyzer.py)
- Confluencia con POIs de alta calidad
- Rendimiento histórico (ict_historical_analyzer.py)
- Contexto de mercado y sesión

OBJETIVO: Unified confidence scoring 0.0-1.0 para cada patrón ICT detectado.

Versión: v1.0.0 (Nueva implementación)
Fecha: 27 Julio 2025
"""

from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

# Imports del ICT Engine
from .ict_types import ICTPattern, MarketPhase, SessionType, SignalStrength
from .ict_historical_analyzer import ICTHistoricalAnalyzer

# Logger especializado
from sistema.emoji_logger import get_emoji_safe_logger
confidence_logger = get_emoji_safe_logger('ict')

class ConfidenceEngine:
    """
    Motor de confianza unificado que orquesta el cálculo de confidence scores
    para patrones ICT usando múltiples fuentes de información.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializa el motor de confianza con configuración personalizable.

        Args:
            config: Configuración opcional para pesos y parámetros
        """
        confidence_logger.info("🧠 Inicializando ICT Confidence Engine")

        # Configuración por defecto
        self.config = config or {
            'weights': {
                'base_pattern': 0.5,      # 50% peso al análisis base del patrón
                'poi_confluence': 0.3,    # 30% peso a confluencia con POIs
                'historical': 0.2,        # 20% peso al rendimiento histórico
            },
            'confluence_distance_pips': 10,  # Distancia máxima para confluencia
            'min_historical_samples': 5,     # Mínimo de samples para histórico
            'session_multipliers': {
                'asian': 0.8,      # Sesión asiática: menor volatilidad
                'london': 1.1,     # Sesión Londres: mayor confiabilidad
                'new_york': 1.0,   # Sesión NY: baseline
                'overlap': 1.2,    # Overlap: máxima confiabilidad
            }
        }

        # Inicializar analizador histórico
        self.historical_analyzer = ICTHistoricalAnalyzer()

        confidence_logger.info("✅ Confidence Engine inicializado correctamente")

    def calculate_pattern_confidence(self,
                                   pattern: Dict,
                                   market_context: Dict,
                                   poi_list: List[Dict],
                                   current_price: float,
                                   current_session: Optional[str] = None) -> float:
        """
        Calcula un score de confianza unificado (0.0 a 1.0) para un patrón ICT.

        Args:
            pattern: Patrón ICT detectado con información base
            market_context: Contexto de mercado (bias, fase, etc.)
            poi_list: Lista de POIs con scores inteligentes
            current_price: Precio actual del mercado
            current_session: Sesión actual de trading

        Returns:
            float: Score de confianza entre 0.0 y 1.0
        """
        if not pattern:
            confidence_logger.warning("❌ Patrón vacío recibido para análisis")
            return 0.0

        try:
            # 1. SCORE BASE DEL PATRÓN
            base_score = self._calculate_base_pattern_score(pattern, market_context)

            # 2. BONIFICACIÓN POR CONFLUENCIA CON POI
            confluence_bonus = self._calculate_poi_confluence(pattern, poi_list, current_price)

            # 3. PONDERACIÓN POR RENDIMIENTO HISTÓRICO
            historical_weight = self._calculate_historical_weight(pattern)

            # 4. MULTIPLICADOR DE SESIÓN
            session_multiplier = self._get_session_multiplier(current_session)

            # 5. CÁLCULO FINAL PONDERADO
            weights = self.config['weights']
            final_confidence = (
                base_score * weights['base_pattern'] +
                confluence_bonus * weights['poi_confluence'] +
                historical_weight * weights['historical']
            ) * session_multiplier

            # Asegurar que esté en rango válido
            final_confidence = max(0.0, min(final_confidence, 1.0))

            confidence_logger.info(
                f"🎯 Confianza calculada para {pattern.get('type', 'UNKNOWN')}: {final_confidence:.3f} "
                f"(Base: {base_score:.3f}, POI: {confluence_bonus:.3f}, "
                f"Histórico: {historical_weight:.3f}, Sesión: {session_multiplier:.2f})"
            )

            return final_confidence

        except (ValueError, KeyError, TypeError) as e:
            confidence_logger.error("❌ Error calculando confianza del patrón: %s", e)
            return 0.0

    def _calculate_base_pattern_score(self, pattern: Dict, market_context: Dict) -> float:
        """
        Calcula el score base del patrón usando lógica mejorada de pattern_analyzer.

        Migra y mejora la lógica de _calculate_analysis_confidence del pattern_analyzer.
        """
        base_confidence = 0.6  # Base del 60%

        # Strength del patrón (si disponible)
        pattern_strength = pattern.get('strength', 70)  # Default 70
        if pattern_strength >= 80:
            base_confidence += 0.15  # +15% para patrones fuertes
        elif pattern_strength >= 70:
            base_confidence += 0.08  # +8% para patrones medios

        # Calidad de estructura de mercado
        market_structure_quality = market_context.get('structure_quality', 'MEDIUM')
        if market_structure_quality == 'HIGH':
            base_confidence += 0.15
        elif market_structure_quality == 'MEDIUM':
            base_confidence += 0.08

        # Alineación con bias H4
        h4_bias = market_context.get('h4_bias', 'NEUTRAL')
        pattern_direction = pattern.get('direction', 'NEUTRAL')

        if h4_bias != 'NEUTRAL' and h4_bias == pattern_direction:
            base_confidence += 0.10  # +10% por alineación con bias

        return min(base_confidence, 1.0)

    def _calculate_poi_confluence(self, pattern: Dict, poi_list: List[Dict], current_price: float) -> float:
        """
        Calcula bonificación por confluencia con POIs de alta calidad.

        Esta es LA GRAN SINERGIA entre el POI Scoring Engine y el ICT Engine.
        """
        if not poi_list:
            return 0.0

        pattern_price = pattern.get('price', current_price)
        confluence_distance = self.config['confluence_distance_pips'] * 0.0001  # Convertir a precio

        best_confluence_score = 0.0

        for poi in poi_list:
            poi_price = poi.get('price', 0)
            poi_score = poi.get('intelligent_score', 0) / 100.0  # Convertir a 0-1

            # Verificar si están en confluencia (dentro de la distancia)
            distance = abs(pattern_price - poi_price)

            if distance <= confluence_distance:
                # Calcular score ponderado por proximidad
                proximity_factor = 1.0 - (distance / confluence_distance)
                confluence_score = poi_score * proximity_factor

                best_confluence_score = max(best_confluence_score, confluence_score)

                confidence_logger.debug(
                    f"🎯 Confluencia detectada: Patrón {pattern_price:.5f} <-> "
                    f"POI {poi_price:.5f} (Score: {confluence_score:.3f})"
                )

        return best_confluence_score

    def _calculate_historical_weight(self, pattern: Dict) -> float:
        """
        Calcula ponderación basada en rendimiento histórico del tipo de patrón.
        """
        pattern_type = pattern.get('type', 'UNKNOWN')

        try:
            # Usar el analizador histórico para obtener rendimiento
            historical_performance = self.historical_analyzer.get_historical_poi_performance(
                pattern_type,
                pattern.get('timeframe', 'M15'),
                'EURUSD'  # TODO: hacer dinámico
            )

            # Convertir a score 0-1 (asumiendo que histórico retorna 0-100)
            return min(historical_performance / 100.0, 1.0)

        except (ValueError, KeyError, TypeError) as e:
            confidence_logger.warning("⚠️ Error obteniendo histórico para %s: %s", pattern_type, e)
            return 0.6  # Score neutro como fallback

    def _get_session_multiplier(self, current_session: Optional[str]) -> float:
        """
        Obtiene multiplicador de confianza basado en la sesión actual.
        """
        if not current_session:
            return 1.0

        session_lower = current_session.lower()
        multiplier = self.config['session_multipliers'].get(session_lower, 1.0)

        confidence_logger.debug("🕐 Multiplicador de sesión %s: %s", current_session, multiplier)
        return multiplier

    def generate_confidence_report(self, pattern: Dict, confidence_score: float) -> Dict:
        """
        Genera un reporte detallado del análisis de confianza.

        Returns:
            Dict con breakdown detallado del análisis
        """
        # Clasificar nivel de confianza
        if confidence_score >= 0.85:
            confidence_level = "VERY_HIGH"
            confidence_grade = "A+"
        elif confidence_score >= 0.75:
            confidence_level = "HIGH"
            confidence_grade = "A"
        elif confidence_score >= 0.65:
            confidence_level = "MEDIUM"
            confidence_grade = "B"
        elif confidence_score >= 0.50:
            confidence_level = "LOW"
            confidence_grade = "C"
        else:
            confidence_level = "VERY_LOW"
            confidence_grade = "D"

        return {
            'confidence_score': confidence_score,
            'confidence_level': confidence_level,
            'confidence_grade': confidence_grade,
            'pattern_type': pattern.get('type', 'UNKNOWN'),
            'timestamp': datetime.now().isoformat(),
            'recommendation': self._get_confidence_recommendation(confidence_level)
        }

    def _get_confidence_recommendation(self, confidence_level: str) -> str:
        """Genera recomendación basada en nivel de confianza"""
        recommendations = {
            'VERY_HIGH': "🟢 EJECUTAR: Confianza muy alta, proceder con operación",
            'HIGH': "🟡 CONSIDERAR: Buena confianza, revisar contexto adicional",
            'MEDIUM': "🟠 PRECAUCIÓN: Confianza moderada, esperar confirmación",
            'LOW': "🔴 EVITAR: Baja confianza, no recomendada operación",
            'VERY_LOW': "❌ RECHAZAR: Confianza muy baja, evitar completamente"
        }

        return recommendations.get(confidence_level, "❓ REVISAR: Nivel de confianza desconocido")

    def calculate_overall_confidence(self, patterns: List[Any], market_context: Any) -> float:
        """Calcula la confianza general del análisis"""
        if not patterns:
            return 0.0

        base_confidence = sum(getattr(p, 'confidence', 0.5) for p in patterns) / len(patterns)
        market_modifier = getattr(market_context, 'confidence_modifier', 1.0) if market_context else 1.0

        return min(base_confidence * market_modifier, 1.0)


# Instancia global del motor (singleton pattern)
confidence_engine = ConfidenceEngine()

def calculate_pattern_confidence(pattern: Dict,
                               market_context: Dict,
                               poi_list: List[Dict],
                               current_price: float,
                               current_session: Optional[str] = None) -> float:
    """
    Función de conveniencia para calcular confianza de patrón.

    Esta función será la que use pattern_analyzer.py para obtener scores.
    """
    return confidence_engine.calculate_pattern_confidence(
        pattern, market_context, poi_list, current_price, current_session
    )

def generate_confidence_report(pattern: Dict, confidence_score: float) -> Dict:
    """
    Función de conveniencia para generar reporte de confianza.
    """
    return confidence_engine.generate_confidence_report(pattern, confidence_score)
