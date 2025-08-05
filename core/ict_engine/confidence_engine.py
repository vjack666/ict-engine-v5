#!/usr/bin/env python3
"""
🧠 ICT CONFIDENCE ENGINE - Motor de Confianza Inteligente v5.0
==============================================================

Motor unificado que calcula scores de confianza para patrones ICT usando:
- Análisis base del patrón (pattern_analyzer.py)
- Confluencia con POIs de alta calidad
- Rendimiento histórico (ict_historical_analyzer.py)
- Contexto de mercado y sesión
- Validación multi-timeframe
- Análisis de volatilidad y liquidez

OBJETIVO: Unified confidence scoring 0.0-1.0 para cada patrón ICT detectado.

Versión: v2.0.0 (Migrado a SLUC v2.1)
Fecha: 03 Agosto 2025
Autor: ICT Engine Team
"""
# MIGRADO A SLUC v2.1
from sistema.logging_interface import enviar_senal_log
# Imports del ICT Engine - manejo seguro con type checking
from typing import Dict, List, Optional, Tuple, Any, TYPE_CHECKING
from datetime import datetime, timedelta
import numpy as np

# Type checking imports para evitar conflictos
if TYPE_CHECKING:
    try:
        from .ict_types import ICTPattern, MarketPhase, SessionType, SignalStrength
    except ImportError:
        # Definir tipos stub para type checking
        ICTPattern = Any
        MarketPhase = Any
        SessionType = Any
        SignalStrength = Any

# Runtime imports con fallback seguro
ict_types_available = False
try:
    from .ict_types import ICTPattern, MarketPhase, SessionType, SignalStrength  # type: ignore
    enviar_senal_log("INFO", "✅ ICT Types importados correctamente", __name__, "confidence_engine")
    ict_types_available = True
except ImportError as e:
    enviar_senal_log("WARNING", f"⚠️ ICT Types no disponibles: {e}", __name__, "confidence_engine")
    # En runtime, usaremos duck typing - no necesitamos clases fallback explícitas

try:
    from .ict_historical_analyzer import ICTHistoricalAnalyzer
    enviar_senal_log("INFO", "✅ ICT Historical Analyzer importado correctamente", __name__, "confidence_engine")
except ImportError as e:
    enviar_senal_log("WARNING", f"⚠️ ICT Historical Analyzer no disponible: {e}", __name__, "confidence_engine")
    ICTHistoricalAnalyzer = None

# =============================================================================
# CONFIGURACIÓN GLOBAL DEL MOTOR DE CONFIANZA
# =============================================================================

CONFIDENCE_CONFIG = {
    'weights': {
        'base_pattern': 0.25,        # ⭐ REDUCIDO: 40% → 25% (menos dependencia de patrón base)
        'poi_confluence': 0.40,      # ⭐ AUMENTADO: 25% → 40% (mayor sinergia POI-ICT)
        'historical': 0.20,          # ⭐ AUMENTADO: 15% → 20% (mayor peso histórico)
        'market_structure': 0.10,    # MANTENIDO: 10% estructura de mercado
        'session_context': 0.05,     # ⭐ REDUCIDO: 10% → 5% (menos peso sesión)
    },
    'confluence_distance_pips': 20,      # ⭐ AUMENTADO: 10 → 20 pips (mayor rango confluencia)
    'min_historical_samples': 5,         # Mínimo de samples para histórico
    'max_pattern_age_minutes': 120,      # Edad máxima del patrón (2 horas)
    'volatility_adjustment': True,       # Ajuste por volatilidad
    'session_multipliers': {
        'asian': 0.95,           # ⭐ MEJORADO: 0.85 → 0.95 (mejor asiática)
        'london': 1.25,          # ⭐ MEJORADO: 1.1 → 1.25 (mejor Londres)
        'new_york': 1.15,        # ⭐ MEJORADO: 1.0 → 1.15 (mejor NY)
        'overlap': 1.30,         # ⭐ MEJORADO: 1.15 → 1.30 (mejor overlap)
        'quiet': 0.80,           # ⭐ MEJORADO: 0.7 → 0.80 (mejor horas silenciosas)
    },
    'confidence_thresholds': {
        'very_high': 0.85,       # 85%+
        'high': 0.75,            # 75-84%
        'medium': 0.65,          # 65-74%
        'low': 0.50,             # 50-64%
        'very_low': 0.0,         # <50%
    }
}

# =============================================================================
# CLASE PRINCIPAL - CONFIDENCE ENGINE
# =============================================================================

class ConfidenceEngine:
    """
    🧠 MOTOR DE CONFIANZA ICT v2.0

    Calcula scores de confianza unificados para patrones ICT integrando:
    - Análisis base del patrón y fuerza
    - Confluencia inteligente con POIs
    - Rendimiento histórico y estadísticas
    - Contexto de mercado y estructura
    - Análisis de sesión y liquidez
    - Ajustes dinámicos por volatilidad
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Inicializa el motor de confianza con configuración personalizable.

        Args:
            config: Configuración opcional para pesos y parámetros
        """
        enviar_senal_log("INFO", "🧠 [CONFIDENCE ENGINE] Inicializando motor de confianza ICT v2.0", __name__, "confidence_engine")

        # Configuración por defecto o personalizada
        self.config = {**CONFIDENCE_CONFIG, **(config or {})}

        # Contadores de estadísticas
        self.stats = {
            'calculations_total': 0,
            'patterns_analyzed': {},
            'avg_confidence': 0.0,
            'last_reset': datetime.now()
        }

        # Inicializar analizador histórico si está disponible
        if ICTHistoricalAnalyzer:
            try:
                self.historical_analyzer = ICTHistoricalAnalyzer()
                enviar_senal_log("INFO", "✅ Historical Analyzer inicializado", __name__, "confidence_engine")
            except Exception as e:
                enviar_senal_log("WARNING", f"⚠️ Error inicializando Historical Analyzer: {e}", __name__, "confidence_engine")
                self.historical_analyzer = None
        else:
            self.historical_analyzer = None

        enviar_senal_log("INFO", "✅ Confidence Engine inicializado correctamente", __name__, "confidence_engine")
        enviar_senal_log("DEBUG", f"Configuración: weights={self.config['weights']}", __name__, "confidence_engine")

    def calculate_pattern_confidence(self,
                                   pattern: Dict,
                                   market_context: Dict,
                                   poi_list: List[Dict],
                                   current_price: float,
                                   current_session: Optional[str] = None,
                                   symbol: str = 'EURUSD') -> float:
        """
        🎯 FUNCIÓN PRINCIPAL: Calcula un score de confianza unificado (0.0 a 1.0) para un patrón ICT.

        Args:
            pattern: Patrón ICT detectado con información base
            market_context: Contexto de mercado (bias, fase, estructura, etc.)
            poi_list: Lista de POIs con scores inteligentes
            current_price: Precio actual del mercado
            current_session: Sesión actual de trading
            symbol: Símbolo del instrumento financiero

        Returns:
            float: Score de confianza entre 0.0 y 1.0
        """
        if not pattern:
            enviar_senal_log("WARNING", "❌ Patrón vacío recibido para análisis", __name__, "confidence_engine")
            return 0.0

        # Validar entradas críticas
        if not self._validate_inputs(pattern, market_context, current_price):
            enviar_senal_log("WARNING", "❌ Entradas inválidas para cálculo de confianza", __name__, "confidence_engine")
            return 0.0

        try:
            self.stats['calculations_total'] += 1
            pattern_type = pattern.get('type', 'UNKNOWN')

            enviar_senal_log("DEBUG", f"🧠 Iniciando cálculo de confianza para patrón {pattern_type}", __name__, "confidence_engine")

            # 1. SCORE BASE DEL PATRÓN
            base_score = self._calculate_base_pattern_score(pattern, market_context)

            # 2. BONIFICACIÓN POR CONFLUENCIA CON POI
            confluence_bonus = self._calculate_poi_confluence(pattern, poi_list, current_price)

            # 3. PONDERACIÓN POR RENDIMIENTO HISTÓRICO
            historical_weight = self._calculate_historical_weight(pattern, symbol)

            # 4. ANÁLISIS DE ESTRUCTURA DE MERCADO
            structure_bonus = self._calculate_structure_bonus(market_context, pattern)

            # 5. MULTIPLICADOR DE SESIÓN
            session_multiplier = self._get_session_multiplier(current_session)

            # 6. AJUSTE POR VOLATILIDAD (si está habilitado)
            volatility_adjustment = self._calculate_volatility_adjustment(market_context, pattern)

            # 7. CÁLCULO FINAL PONDERADO
            weights = self.config['weights']
            final_confidence = (
                base_score * weights['base_pattern'] +
                confluence_bonus * weights['poi_confluence'] +
                historical_weight * weights['historical'] +
                structure_bonus * weights['market_structure']
            ) * session_multiplier * volatility_adjustment

            # Asegurar que esté en rango válido
            final_confidence = max(0.0, min(final_confidence, 1.0))

            # Actualizar estadísticas
            self._update_stats(pattern_type, final_confidence)

            enviar_senal_log(
                "INFO",
                f"🎯 Confianza calculada para {pattern_type}: {final_confidence:.3f} "
                f"(Base: {base_score:.3f}, POI: {confluence_bonus:.3f}, "
                f"Histórico: {historical_weight:.3f}, Estructura: {structure_bonus:.3f}, "
                f"Sesión: {session_multiplier:.2f}, Volatilidad: {volatility_adjustment:.2f})",
                __name__, "confidence_engine"
            )

            return final_confidence

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error crítico calculando confianza del patrón: {e}", __name__, "confidence_engine")
            return 0.0

    def _validate_inputs(self, pattern: Dict, market_context: Dict, current_price: float) -> bool:
        """
        🔍 Valida que las entradas sean correctas y completas

        Args:
            pattern: Patrón a validar
            market_context: Contexto de mercado
            current_price: Precio actual

        Returns:
            bool: True si las entradas son válidas
        """
        try:
            # Validar patrón
            if not isinstance(pattern, dict) or not pattern:
                return False

            # Validar precio actual
            if not isinstance(current_price, (int, float)) or current_price <= 0:
                return False

            # Validar contexto de mercado
            if not isinstance(market_context, dict):
                return False

            # Validar edad del patrón
            pattern_timestamp = pattern.get('timestamp')
            if pattern_timestamp:
                try:
                    if isinstance(pattern_timestamp, str):
                        pattern_time = datetime.fromisoformat(pattern_timestamp.replace('Z', '+00:00'))
                    else:
                        pattern_time = pattern_timestamp

                    age_minutes = (datetime.now() - pattern_time.replace(tzinfo=None)).total_seconds() / 60
                    if age_minutes > self.config['max_pattern_age_minutes']:
                        enviar_senal_log("WARNING", f"⚠️ Patrón demasiado antiguo: {age_minutes:.1f} minutos", __name__, "confidence_engine")
                        return False
                except Exception as e:
                    enviar_senal_log("DEBUG", f"No se pudo validar timestamp del patrón: {e}", __name__, "confidence_engine")

            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"Error validando entradas: {e}", __name__, "confidence_engine")
            return False

    def _calculate_base_pattern_score(self, pattern: Dict, market_context: Dict) -> float:
        """
        📊 Calcula el score base del patrón usando lógica mejorada de pattern_analyzer.

        Migra y mejora la lógica de _calculate_analysis_confidence del pattern_analyzer.

        Args:
            pattern: Información del patrón detectado
            market_context: Contexto actual del mercado

        Returns:
            float: Score base entre 0.0 y 1.0
        """
        try:
            base_confidence = 0.5  # Base del 50%

            # Factor 1: Strength del patrón (si disponible)
            pattern_strength = pattern.get('strength', 60)  # Default 60
            if pattern_strength >= 85:
                base_confidence += 0.20  # +20% para patrones muy fuertes
            elif pattern_strength >= 75:
                base_confidence += 0.15  # +15% para patrones fuertes
            elif pattern_strength >= 65:
                base_confidence += 0.10  # +10% para patrones buenos
            elif pattern_strength >= 55:
                base_confidence += 0.05  # +5% para patrones aceptables

            # Factor 2: Calidad de estructura de mercado
            market_structure_quality = market_context.get('structure_quality', 'MEDIUM')
            if market_structure_quality == 'HIGH':
                base_confidence += 0.15
            elif market_structure_quality == 'MEDIUM':
                base_confidence += 0.08
            elif market_structure_quality == 'LOW':
                base_confidence += 0.02

            # Factor 3: Alineación con bias H4
            h4_bias = market_context.get('h4_bias', 'NEUTRAL')
            pattern_direction = pattern.get('direction', 'NEUTRAL')

            if h4_bias != 'NEUTRAL' and h4_bias == pattern_direction:
                base_confidence += 0.12  # +12% por alineación con bias
            elif h4_bias != 'NEUTRAL' and h4_bias != pattern_direction:
                base_confidence -= 0.08  # -8% por ir contra el bias

            # Factor 4: Confluencia temporal (multi-timeframe)
            timeframe_confirmation = pattern.get('timeframe_confirmation', False)
            if timeframe_confirmation:
                base_confidence += 0.08  # +8% por confirmación multi-timeframe

            # Factor 5: Calidad de la detección
            detection_quality = pattern.get('detection_quality', 'MEDIUM')
            if detection_quality == 'HIGH':
                base_confidence += 0.10
            elif detection_quality == 'MEDIUM':
                base_confidence += 0.05

            enviar_senal_log("DEBUG", f"Score base calculado: {base_confidence:.3f}", __name__, "confidence_engine")
            return min(base_confidence, 1.0)

        except Exception as e:
            enviar_senal_log("ERROR", f"Error calculando score base: {e}", __name__, "confidence_engine")
            return 0.5  # Retornar score neutro como fallback

    def _calculate_poi_confluence(self, pattern: Dict, poi_list: List[Dict], current_price: float) -> float:
        """
        🎯 Calcula bonificación por confluencia con POIs de alta calidad.

        Esta es LA GRAN SINERGIA entre el POI Scoring Engine y el ICT Engine.

        Args:
            pattern: Patrón ICT detectado
            poi_list: Lista de POIs con scores inteligentes
            current_price: Precio actual del mercado

        Returns:
            float: Score de confluencia entre 0.0 y 1.0
        """
        if not poi_list:
            enviar_senal_log("DEBUG", "No hay POIs disponibles para confluencia", __name__, "confidence_engine")
            return 0.0

        try:
            pattern_price = pattern.get('price', current_price)
            confluence_distance = self.config['confluence_distance_pips'] * 0.0001  # Convertir a precio

            best_confluence_score = 0.0
            total_confluence_score = 0.0
            confluences_found = 0

            for poi in poi_list:
                try:
                    poi_price = poi.get('price', 0)
                    poi_score = poi.get('intelligent_score', 0) / 100.0  # Convertir a 0-1

                    if poi_price <= 0 or poi_score <= 0:
                        continue

                    # Verificar si están en confluencia (dentro de la distancia)
                    distance = abs(pattern_price - poi_price)

                    if distance <= confluence_distance:
                        # Calcular score ponderado por proximidad y tipo de POI
                        proximity_factor = 1.0 - (distance / confluence_distance)

                        # Bonus por tipo de POI
                        poi_type = poi.get('type', 'UNKNOWN')
                        type_multiplier = self._get_poi_type_multiplier(poi_type)

                        confluence_score = poi_score * proximity_factor * type_multiplier

                        best_confluence_score = max(best_confluence_score, confluence_score)
                        total_confluence_score += confluence_score
                        confluences_found += 1

                        enviar_senal_log(
                            "DEBUG",
                            f"🎯 Confluencia detectada: Patrón {pattern_price:.5f} <-> "
                            f"POI {poi_type} {poi_price:.5f} (Score: {confluence_score:.3f}, "
                            f"Proximidad: {proximity_factor:.2f})",
                            __name__, "confidence_engine"
                        )

                except Exception as e:
                    enviar_senal_log("WARNING", f"Error procesando POI: {e}", __name__, "confidence_engine")
                    continue

            # Calcular score final (combinación de mejor score y promedio)
            if confluences_found > 0:
                avg_confluence = total_confluence_score / confluences_found
                # 70% mejor score + 30% promedio
                final_score = (best_confluence_score * 0.7) + (avg_confluence * 0.3)

                # Bonus por múltiples confluencias
                if confluences_found > 1:
                    confluence_bonus = min(confluences_found * 0.05, 0.2)  # Max 20% bonus
                    final_score += confluence_bonus

                enviar_senal_log("INFO", f"✅ Confluencia total: {confluences_found} POIs, Score: {final_score:.3f}", __name__, "confidence_engine")
                return min(final_score, 1.0)
            else:
                enviar_senal_log("DEBUG", "No se encontraron confluencias válidas", __name__, "confidence_engine")
                return 0.0

        except Exception as e:
            enviar_senal_log("ERROR", f"Error calculando confluencia POI: {e}", __name__, "confidence_engine")
            return 0.0

    def _get_poi_type_multiplier(self, poi_type: str) -> float:
        """
        🏷️ Obtiene multiplicador basado en tipo de POI

        Args:
            poi_type: Tipo de POI

        Returns:
            float: Multiplicador de importancia
        """
        multipliers = {
            'FVG': 1.2,         # Fair Value Gaps - alta importancia
            'OB': 1.15,         # Order Blocks - alta importancia
            'BREAKER': 1.1,     # Breaker Blocks - buena importancia
            'MSS': 1.0,         # Market Structure Shift - importancia normal
            'CHOCH': 1.0,       # Change of Character - importancia normal
            'LIQUIDITY': 0.9,   # Liquidez - menor importancia
            'UNKNOWN': 0.8      # Desconocido - baja importancia
        }
        return multipliers.get(poi_type.upper(), 0.8)

    def _calculate_historical_weight(self, pattern: Dict, symbol: str = 'EURUSD') -> float:
        """
        📈 Calcula ponderación basada en rendimiento histórico del tipo de patrón.

        Args:
            pattern: Patrón a analizar
            symbol: Símbolo del instrumento

        Returns:
            float: Peso histórico entre 0.0 y 1.0
        """
        pattern_type = pattern.get('type', 'UNKNOWN')

        try:
            if not self.historical_analyzer:
                enviar_senal_log("DEBUG", "Historical analyzer no disponible, usando score neutro", __name__, "confidence_engine")
                return 0.6  # Score neutro como fallback

            # Usar el analizador histórico para obtener rendimiento
            historical_performance = self.historical_analyzer.get_historical_poi_performance(
                pattern_type,
                pattern.get('timeframe', 'M15'),
                symbol
            )

            # Convertir a score 0-1 (asumiendo que histórico retorna 0-100)
            if isinstance(historical_performance, (int, float)):
                normalized_score = min(historical_performance / 100.0, 1.0)
                enviar_senal_log("DEBUG", f"Score histórico para {pattern_type}: {normalized_score:.3f}", __name__, "confidence_engine")
                return normalized_score
            else:
                enviar_senal_log("WARNING", f"Formato inesperado del score histórico: {historical_performance}", __name__, "confidence_engine")
                return 0.6

        except Exception as e:
            enviar_senal_log("WARNING", f"⚠️ Error obteniendo histórico para {pattern_type}: {e}", __name__, "confidence_engine")
            return 0.6  # Score neutro como fallback

    def _calculate_structure_bonus(self, market_context: Dict, pattern: Dict) -> float:
        """
        🏗️ Calcula bonus basado en estructura de mercado

        Args:
            market_context: Contexto de mercado
            pattern: Patrón detectado

        Returns:
            float: Bonus de estructura entre 0.0 y 1.0
        """
        try:
            structure_bonus = 0.5  # Base neutral

            # Factor 1: Tendencia general
            market_trend = market_context.get('trend', 'NEUTRAL')
            pattern_direction = pattern.get('direction', 'NEUTRAL')

            if market_trend != 'NEUTRAL' and market_trend == pattern_direction:
                structure_bonus += 0.15  # +15% por alineación con tendencia

            # Factor 2: Fuerza de la tendencia
            trend_strength = market_context.get('trend_strength', 'MEDIUM')
            if trend_strength == 'STRONG':
                structure_bonus += 0.10
            elif trend_strength == 'MEDIUM':
                structure_bonus += 0.05

            # Factor 3: Nivel de soporte/resistencia
            sr_level = market_context.get('sr_level', 'NONE')
            if sr_level in ['MAJOR', 'SIGNIFICANT']:
                structure_bonus += 0.12
            elif sr_level in ['MINOR', 'WEAK']:
                structure_bonus += 0.06

            # Factor 4: Momentum
            momentum = market_context.get('momentum', 'NEUTRAL')
            if momentum == 'STRONG_BULLISH' and pattern_direction == 'BULLISH':
                structure_bonus += 0.08
            elif momentum == 'STRONG_BEARISH' and pattern_direction == 'BEARISH':
                structure_bonus += 0.08

            return min(structure_bonus, 1.0)

        except Exception as e:
            enviar_senal_log("ERROR", f"Error calculando bonus de estructura: {e}", __name__, "confidence_engine")
            return 0.5

    def _calculate_volatility_adjustment(self, market_context: Dict, pattern: Dict) -> float:
        """
        📊 Calcula ajuste basado en volatilidad actual

        Args:
            market_context: Contexto de mercado
            pattern: Patrón detectado

        Returns:
            float: Factor de ajuste por volatilidad
        """
        if not self.config.get('volatility_adjustment', True):
            return 1.0  # Sin ajuste si está deshabilitado

        try:
            volatility = market_context.get('volatility', 'MEDIUM')

            # Ajustes basados en volatilidad
            if volatility == 'VERY_HIGH':
                return 0.85  # Reducir confianza en alta volatilidad
            elif volatility == 'HIGH':
                return 0.92
            elif volatility == 'MEDIUM':
                return 1.0   # Sin ajuste
            elif volatility == 'LOW':
                return 1.05  # Ligero aumento en baja volatilidad
            elif volatility == 'VERY_LOW':
                return 1.08
            else:
                return 1.0

        except Exception as e:
            enviar_senal_log("ERROR", f"Error calculando ajuste de volatilidad: {e}", __name__, "confidence_engine")
            return 1.0

    def _get_session_multiplier(self, current_session: Optional[str]) -> float:
        """
        🕐 Obtiene multiplicador de confianza basado en la sesión actual.

        Args:
            current_session: Sesión actual de trading

        Returns:
            float: Multiplicador de sesión
        """
        if not current_session:
            enviar_senal_log("DEBUG", "Sesión no especificada, usando multiplicador neutro", __name__, "confidence_engine")
            return 1.0

        try:
            session_lower = current_session.lower()
            multiplier = self.config['session_multipliers'].get(session_lower, 1.0)

            enviar_senal_log("DEBUG", f"🕐 Multiplicador de sesión {current_session}: {multiplier}", __name__, "confidence_engine")
            return multiplier

        except Exception as e:
            enviar_senal_log("ERROR", f"Error obteniendo multiplicador de sesión: {e}", __name__, "confidence_engine")
            return 1.0

    def _update_stats(self, pattern_type: str, confidence: float) -> None:
        """
        � Actualiza estadísticas internas del motor

        Args:
            pattern_type: Tipo de patrón analizado
            confidence: Score de confianza calculado
        """
        try:
            # Actualizar contador por tipo de patrón
            if pattern_type not in self.stats['patterns_analyzed']:
                self.stats['patterns_analyzed'][pattern_type] = 0
            self.stats['patterns_analyzed'][pattern_type] += 1

            # Actualizar promedio móvil de confianza
            current_avg = self.stats['avg_confidence']
            total_calculations = self.stats['calculations_total']

            if total_calculations == 1:
                self.stats['avg_confidence'] = confidence
            else:
                # Promedio móvil exponencial
                alpha = 0.1  # Factor de suavizado
                self.stats['avg_confidence'] = (alpha * confidence) + ((1 - alpha) * current_avg)

        except Exception as e:
            enviar_senal_log("ERROR", f"Error actualizando estadísticas: {e}", __name__, "confidence_engine")

    def get_engine_stats(self) -> Dict[str, Any]:
        """
        📈 Obtiene estadísticas del motor de confianza

        Returns:
            Dict: Estadísticas completas del motor
        """
        return {
            'total_calculations': self.stats['calculations_total'],
            'patterns_analyzed': dict(self.stats['patterns_analyzed']),
            'average_confidence': self.stats['avg_confidence'],
            'uptime_hours': (datetime.now() - self.stats['last_reset']).total_seconds() / 3600,
            'config_summary': {
                'weights': self.config['weights'],
                'volatility_adjustment': self.config.get('volatility_adjustment', False),
                'historical_analyzer_available': self.historical_analyzer is not None
            }
        }

    def generate_confidence_report(self, pattern: Dict, confidence_score: float) -> Dict:
        """
        📋 Genera un reporte detallado del análisis de confianza.

        Args:
            pattern: Patrón analizado
            confidence_score: Score de confianza calculado

        Returns:
            Dict: Reporte completo con breakdown detallado del análisis
        """
        try:
            # Clasificar nivel de confianza usando umbrales configurables
            thresholds = self.config['confidence_thresholds']

            if confidence_score >= thresholds['very_high']:
                confidence_level = "VERY_HIGH"
                confidence_grade = "A+"
            elif confidence_score >= thresholds['high']:
                confidence_level = "HIGH"
                confidence_grade = "A"
            elif confidence_score >= thresholds['medium']:
                confidence_level = "MEDIUM"
                confidence_grade = "B"
            elif confidence_score >= thresholds['low']:
                confidence_level = "LOW"
                confidence_grade = "C"
            else:
                confidence_level = "VERY_LOW"
                confidence_grade = "D"

            # Determinar estado del patrón
            pattern_status = self._determine_pattern_status(confidence_score, pattern)

            report = {
                'confidence_score': round(confidence_score, 4),
                'confidence_percentage': round(confidence_score * 100, 2),
                'confidence_level': confidence_level,
                'confidence_grade': confidence_grade,
                'pattern_type': pattern.get('type', 'UNKNOWN'),
                'pattern_direction': pattern.get('direction', 'NEUTRAL'),
                'pattern_timeframe': pattern.get('timeframe', 'UNKNOWN'),
                'pattern_status': pattern_status,
                'timestamp': datetime.now().isoformat(),
                'recommendation': self._get_confidence_recommendation(confidence_level),
                'risk_assessment': self._assess_risk_level(confidence_score),
                'next_actions': self._suggest_next_actions(confidence_level, pattern),
                'engine_metadata': {
                    'version': '2.0.0',
                    'calculation_id': self.stats['calculations_total'],
                    'engine_avg_confidence': round(self.stats['avg_confidence'], 3)
                }
            }

            enviar_senal_log("INFO", f"📋 Reporte generado para {pattern.get('type', 'UNKNOWN')}: {confidence_level} ({confidence_score:.3f})", __name__, "confidence_engine")
            return report

        except Exception as e:
            enviar_senal_log("ERROR", f"Error generando reporte de confianza: {e}", __name__, "confidence_engine")
            return {
                'confidence_score': confidence_score,
                'confidence_level': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _determine_pattern_status(self, confidence_score: float, pattern: Dict) -> str:
        """
        🔍 Determina el estado operativo del patrón

        Args:
            confidence_score: Score de confianza
            pattern: Información del patrón

        Returns:
            str: Estado del patrón
        """
        if confidence_score >= 0.85:
            return "READY_TO_EXECUTE"
        elif confidence_score >= 0.75:
            return "GOOD_TO_CONSIDER"
        elif confidence_score >= 0.65:
            return "NEEDS_CONFIRMATION"
        elif confidence_score >= 0.50:
            return "RISKY_SETUP"
        else:
            return "NOT_RECOMMENDED"

    def _get_confidence_recommendation(self, confidence_level: str) -> str:
        """🎯 Genera recomendación basada en nivel de confianza"""
        recommendations = {
            'VERY_HIGH': "🟢 EJECUTAR: Confianza muy alta, excelente oportunidad de trading",
            'HIGH': "🟡 CONSIDERAR: Buena confianza, revisar contexto adicional antes de ejecutar",
            'MEDIUM': "🟠 PRECAUCIÓN: Confianza moderada, esperar confirmación adicional",
            'LOW': "🔴 EVITAR: Baja confianza, no recomendada para operación directa",
            'VERY_LOW': "❌ RECHAZAR: Confianza muy baja, evitar completamente"
        }
        return recommendations.get(confidence_level, "❓ REVISAR: Nivel de confianza desconocido")

    def _assess_risk_level(self, confidence_score: float) -> str:
        """⚠️ Evalúa nivel de riesgo basado en confianza"""
        if confidence_score >= 0.85:
            return "LOW"
        elif confidence_score >= 0.75:
            return "MEDIUM_LOW"
        elif confidence_score >= 0.65:
            return "MEDIUM"
        elif confidence_score >= 0.50:
            return "MEDIUM_HIGH"
        else:
            return "HIGH"

    def _suggest_next_actions(self, confidence_level: str, pattern: Dict) -> List[str]:
        """📝 Sugiere próximas acciones basadas en confianza"""
        actions = []

        if confidence_level == "VERY_HIGH":
            actions = [
                "Ejecutar operación con tamaño de posición estándar",
                "Monitorear nivel de entrada precisamente",
                "Configurar stop loss según reglas ICT"
            ]
        elif confidence_level == "HIGH":
            actions = [
                "Considerar operación con tamaño reducido",
                "Buscar confirmación adicional en timeframe menor",
                "Verificar confluencia con niveles de soporte/resistencia"
            ]
        elif confidence_level == "MEDIUM":
            actions = [
                "Esperar confirmación adicional",
                "Monitorear evolución del patrón",
                "Revisar contexto de mercado más amplio"
            ]
        elif confidence_level == "LOW":
            actions = [
                "No operar este setup",
                "Buscar patrones alternativos",
                "Esperar mejor oportunidad"
            ]
        else:  # VERY_LOW
            actions = [
                "Descartar completamente este setup",
                "Revisar análisis por posibles errores",
                "Buscar oportunidades en otros timeframes"
            ]

        return actions

    def calculate_overall_confidence(self, patterns: List[Any], market_context: Any) -> float:
        """
        🌍 Calcula la confianza general del análisis considerando múltiples patrones

        Args:
            patterns: Lista de patrones detectados
            market_context: Contexto general de mercado

        Returns:
            float: Confianza general entre 0.0 y 1.0
        """
        if not patterns:
            enviar_senal_log("WARNING", "No hay patrones para calcular confianza general", __name__, "confidence_engine")
            return 0.0

        try:
            # Calcular confianza base promedio
            individual_confidences = []
            for pattern in patterns:
                if hasattr(pattern, 'confidence'):
                    individual_confidences.append(getattr(pattern, 'confidence', 0.5))
                elif isinstance(pattern, dict):
                    individual_confidences.append(pattern.get('confidence', 0.5))
                else:
                    individual_confidences.append(0.5)  # Fallback

            if not individual_confidences:
                return 0.0

            # Calcular promedio ponderado (dar más peso a patrones con mayor confianza)
            weights = np.array(individual_confidences)  # Pesos basados en confianza
            weighted_avg = np.average(individual_confidences, weights=weights)

            # Aplicar modificador de contexto de mercado
            market_modifier = 1.0
            if market_context:
                if hasattr(market_context, 'confidence_modifier'):
                    market_modifier = getattr(market_context, 'confidence_modifier', 1.0)
                elif isinstance(market_context, dict):
                    market_modifier = market_context.get('confidence_modifier', 1.0)

            # Bonus por cantidad de patrones (pero con diminishing returns)
            pattern_count_bonus = min(len(patterns) * 0.02, 0.1)  # Max 10% bonus

            # Calcular confianza final (convertir a float explícitamente)
            final_confidence = float(weighted_avg * market_modifier) + pattern_count_bonus
            final_confidence = max(0.0, min(final_confidence, 1.0))

            enviar_senal_log(
                "INFO",
                f"🌍 Confianza general calculada: {final_confidence:.3f} "
                f"(Patrones: {len(patterns)}, Promedio: {weighted_avg:.3f}, "
                f"Modificador: {market_modifier:.2f})",
                __name__, "confidence_engine"
            )

            return final_confidence

        except Exception as e:
            enviar_senal_log("ERROR", f"Error calculando confianza general: {e}", __name__, "confidence_engine")
            return 0.0

    def reset_engine_stats(self) -> None:
        """
        🔄 Reinicia estadísticas del motor
        """
        enviar_senal_log("INFO", "🔄 Reiniciando estadísticas del Confidence Engine", __name__, "confidence_engine")

        self.stats = {
            'calculations_total': 0,
            'patterns_analyzed': {},
            'avg_confidence': 0.0,
            'last_reset': datetime.now()
        }

    def update_config(self, new_config: Dict) -> bool:
        """
        ⚙️ Actualiza configuración del motor en tiempo real

        Args:
            new_config: Nueva configuración a aplicar

        Returns:
            bool: True si se actualizó correctamente
        """
        try:
            # Validar configuración básica
            if 'weights' in new_config:
                weights = new_config['weights']
                if not isinstance(weights, dict):
                    enviar_senal_log("ERROR", "Pesos deben ser un diccionario", __name__, "confidence_engine")
                    return False

                # Verificar que los pesos sumen aproximadamente 1.0 (excluyendo session_context)
                core_weights = {k: v for k, v in weights.items() if k != 'session_context'}
                weight_sum = sum(core_weights.values())
                if not (0.8 <= weight_sum <= 1.2):  # Tolerancia del 20%
                    enviar_senal_log("WARNING", f"Suma de pesos core no ideal: {weight_sum:.3f}", __name__, "confidence_engine")

            # Aplicar nueva configuración
            old_config = self.config.copy()
            self.config.update(new_config)

            enviar_senal_log("INFO", f"✅ Configuración actualizada correctamente", __name__, "confidence_engine")
            enviar_senal_log("DEBUG", f"Configuración anterior: {old_config}", __name__, "confidence_engine")
            enviar_senal_log("DEBUG", f"Nueva configuración: {self.config}", __name__, "confidence_engine")

            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"Error actualizando configuración: {e}", __name__, "confidence_engine")
            return False

# =============================================================================
# INSTANCIA GLOBAL Y FUNCIONES DE CONVENIENCIA
# =============================================================================


# Instancia global del motor (singleton pattern)
confidence_engine = ConfidenceEngine()

def calculate_pattern_confidence(pattern: Dict,
                               market_context: Dict,
                               poi_list: List[Dict],
                               current_price: float,
                               current_session: Optional[str] = None,
                               symbol: str = 'EURUSD') -> float:
    """
    🎯 Función de conveniencia para calcular confianza de patrón.

    Esta función será la que use pattern_analyzer.py para obtener scores.

    Args:
        pattern: Patrón ICT detectado
        market_context: Contexto de mercado
        poi_list: Lista de POIs
        current_price: Precio actual
        current_session: Sesión de trading
        symbol: Símbolo del instrumento

    Returns:
        float: Score de confianza entre 0.0 y 1.0
    """
    try:
        return confidence_engine.calculate_pattern_confidence(
            pattern, market_context, poi_list, current_price, current_session, symbol
        )
    except Exception as e:
        enviar_senal_log("ERROR", f"Error en función de conveniencia calculate_pattern_confidence: {e}", __name__, "confidence_engine")
        return 0.0

def generate_confidence_report(pattern: Dict, confidence_score: float) -> Dict:
    """
    📋 Función de conveniencia para generar reporte de confianza.

    Args:
        pattern: Patrón analizado
        confidence_score: Score de confianza

    Returns:
        Dict: Reporte completo de confianza
    """
    try:
        return confidence_engine.generate_confidence_report(pattern, confidence_score)
    except Exception as e:
        enviar_senal_log("ERROR", f"Error en función de conveniencia generate_confidence_report: {e}", __name__, "confidence_engine")
        return {
            'confidence_score': confidence_score,
            'confidence_level': 'ERROR',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def get_engine_stats() -> Dict[str, Any]:
    """
    📊 Función de conveniencia para obtener estadísticas del motor

    Returns:
        Dict: Estadísticas completas
    """
    try:
        return confidence_engine.get_engine_stats()
    except Exception as e:
        enviar_senal_log("ERROR", f"Error obteniendo estadísticas del motor: {e}", __name__, "confidence_engine")
        return {'error': str(e)}

def update_engine_config(new_config: Dict) -> bool:
    """
    ⚙️ Función de conveniencia para actualizar configuración

    Args:
        new_config: Nueva configuración

    Returns:
        bool: True si se actualizó correctamente
    """
    try:
        return confidence_engine.update_config(new_config)
    except Exception as e:
        enviar_senal_log("ERROR", f"Error actualizando configuración del motor: {e}", __name__, "confidence_engine")
        return False

# =============================================================================
# EXPORTACIONES PÚBLICAS
# =============================================================================

__all__ = [
    'ConfidenceEngine',
    'CONFIDENCE_CONFIG',
    'confidence_engine',
    'calculate_pattern_confidence',
    'generate_confidence_report',
    'get_engine_stats',
    'update_engine_config'
]

# Log de inicialización del módulo
enviar_senal_log("INFO", "✅ Módulo confidence_engine v2.0 cargado correctamente", __name__, "confidence_engine")
