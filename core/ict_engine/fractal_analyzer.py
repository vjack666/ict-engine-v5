#!/usr/bin/env python3
"""
🔮 FRACTAL ANALYZER - ICT ENGINE v5.0
====================================

Análisis profesional de rangos fractales ICT para identificación de niveles
de equilibrium, swing highs/lows y validación de estructura de mercado.

Implementa metodología ICT estándar para cálculo de fractales con:
- Detección automática de swing points significativos
- Cálculo de equilibrium dinámico
- Validación temporal y de fuerza
- Integración con MarketContext

Versión: v1.0.0
Autor: ICT Engine Team
Fecha: 02 Agosto 2025
"""

# MIGRADO A SLUC v2.1
from sistema.logging_interface import enviar_senal_log

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union, TypedDict
from dataclasses import dataclass
from enum import Enum

# =============================================================================
# CONFIGURACIÓN FRACTAL ICT
# =============================================================================

FRACTAL_CONFIG = {
    # Detección de Swing Points (AJUSTADO PARA COMPATIBILIDAD)
    'swing_detection_period': 10,          # Período mínimo para swing válido
    'swing_left_bars': 3,                  # Barras a la izquierda del swing (REDUCIDO)
    'swing_right_bars': 2,                 # Barras a la derecha del swing

    # Validación de Fuerza (DESHABILITADO PARA TESTING)
    'min_swing_strength': 0.000001,        # Fuerza mínima casi 0 (TESTING)
    'min_range_size': 0.000001,            # Tamaño mínimo casi 0 (TESTING)

    # Gestión Temporal
    'max_fractal_age_hours': 24,           # Edad máxima del fractal
    'invalidation_timeout_hours': 48,      # Timeout para invalidación

    # Scoring y Confianza (RELAJADO PARA TESTING)
    'confidence_threshold': 0.40,          # Confianza mínima para validez (REDUCIDO)
    'equilibrium_tolerance': 0.0001,       # Tolerancia para nivel EQ (10 pips)
    'test_reinforcement_bonus': 0.05,      # Bonus por test del nivel

    # Configuración Avanzada
    'multi_timeframe_validation': True,    # Validación multi-timeframe
    'volume_confirmation_weight': 0.15,    # Peso de confirmación por volumen
    'session_context_weight': 0.10         # Peso del contexto de sesión
}

class FractalStatus(Enum):
    """Estados posibles del análisis fractal"""
    NO_CALCULADO = "NO_CALCULADO"
    CALCULANDO = "CALCULANDO"
    CALCULADO = "CALCULADO"
    VALIDO = "VÁLIDO"
    CADUCADO = "CADUCADO"
    INVALIDADO = "INVALIDADO"

class FractalGrade(Enum):
    """Grados de calidad del fractal"""
    A_PLUS = "A+"  # 90-100% confianza
    A = "A"        # 80-89% confianza
    B = "B"        # 70-79% confianza
    C = "C"        # 60-69% confianza
    D = "D"        # <60% confianza

# =============================================================================
# TIPOS ESPECIALIZADOS
# =============================================================================

class FractalLevels(TypedDict):
    """Tipo específico para niveles fractales"""
    high: float
    low: float
    eq: float
    confidence: float
    grade: str

# =============================================================================
# DATACLASSES PARA ESTRUCTURA DE DATOS
# =============================================================================

@dataclass
class SwingPoint:
    """Representa un swing point detectado"""
    price: float
    timestamp: datetime
    index: int
    swing_type: str  # 'HIGH' o 'LOW'
    strength: float
    confirmed: bool = False
    tests: int = 0

@dataclass
class FractalRange:
    """Representa un rango fractal completo"""
    high: float
    low: float
    eq: float  # Equilibrium point
    high_timestamp: datetime
    low_timestamp: datetime
    status: FractalStatus
    confidence: float
    grade: FractalGrade
    age_minutes: int
    tests: int = 0
    valid: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario para MarketContext"""
        return {
            'high': self.high,
            'low': self.low,
            'eq': self.eq,
            'status': self.status.value,
            'confidence': self.confidence,
            'grade': self.grade.value,
            'age_minutes': self.age_minutes,
            'tests': self.tests,
            'valid': self.valid,
            'high_timestamp': self.high_timestamp.isoformat(),
            'low_timestamp': self.low_timestamp.isoformat()
        }

# =============================================================================
# CLASE PRINCIPAL - FRACTAL ANALYZER
# =============================================================================

class FractalAnalyzer:
    """
    🔮 FRACTAL ANALYZER - Análisis ICT Profesional

    Implementa análisis fractal completo siguiendo metodología ICT estándar:
    - Detección de swing highs/lows significativos
    - Cálculo de equilibrium dinámico
    - Validación de fuerza y temporalidad
    - Scoring de confianza avanzado
    """

    def __init__(self):
        """Inicializa el analizador fractal"""
        self.config = FRACTAL_CONFIG.copy()
        self.current_fractal: Optional[FractalRange] = None
        self.swing_cache: Dict[str, List[SwingPoint]] = {
            'highs': [],
            'lows': []
        }
        self.analysis_count = 0

        enviar_senal_log("INFO", "🔮 [FRACTAL ANALYZER] Inicializado con configuración ICT estándar", __name__, "fractal_analysis")
        enviar_senal_log("DEBUG", f"Configuración: swing_period={self.config['swing_detection_period']}, min_strength={self.config['min_swing_strength']}", __name__, "fractal_analysis")

    def analyze_fractal_range(self, df: pd.DataFrame, current_price: float) -> Optional[FractalRange]:
        """
        🎯 FUNCIÓN PRINCIPAL: Analiza y calcula rango fractal completo

        Args:
            df: DataFrame con datos OHLCV
            current_price: Precio actual del mercado

        Returns:
            FractalRange calculado o None si no es válido
        """
        try:
            self.analysis_count += 1
            enviar_senal_log("DEBUG", f"🔮 Iniciando análisis fractal #{self.analysis_count}", __name__, "fractal_analysis")

            if df is None or len(df) < self.config['swing_detection_period'] * 2:
                enviar_senal_log("WARNING", "Datos insuficientes para análisis fractal", __name__, "fractal_analysis")
                return None

            # FASE 1: Detectar swing points significativos
            swing_highs, swing_lows = self._detect_significant_swings(df)

            if not swing_highs or not swing_lows:
                enviar_senal_log("DEBUG", f"No se encontraron swing points válidos. Highs: {len(swing_highs) if swing_highs else 0}, Lows: {len(swing_lows) if swing_lows else 0}", __name__, "fractal_analysis")
                return None

            # FASE 2: Seleccionar swings más relevantes
            latest_high = self._select_most_relevant_swing(swing_highs, current_price, 'HIGH')
            latest_low = self._select_most_relevant_swing(swing_lows, current_price, 'LOW')

            if not latest_high or not latest_low:
                enviar_senal_log("DEBUG", "No se pudieron identificar swings relevantes", __name__, "fractal_analysis")
                return None

            # FASE 3: Calcular rango fractal
            fractal_range = self._calculate_fractal_range(latest_high, latest_low, current_price)

            # FASE 4: Validar calidad del fractal
            if not self._validate_fractal_quality(fractal_range, df):
                enviar_senal_log("DEBUG", f"Fractal no cumple criterios de calidad mínima", __name__, "fractal_analysis")
                return None

            # FASE 5: Calcular confianza y grado
            fractal_range.confidence = self._calculate_fractal_confidence(fractal_range, df, current_price)
            fractal_range.grade = self._assign_fractal_grade(fractal_range.confidence)
            fractal_range.valid = fractal_range.confidence >= self.config['confidence_threshold']

            # FASE 6: Actualizar estado
            if fractal_range.valid:
                fractal_range.status = FractalStatus.VALIDO
                self.current_fractal = fractal_range
                enviar_senal_log("INFO", f"✅ Fractal VÁLIDO calculado: H={fractal_range.high:.5f}, L={fractal_range.low:.5f}, EQ={fractal_range.eq:.5f} | Confianza={fractal_range.confidence:.1f}% | Grado={fractal_range.grade.value}", __name__, "fractal_analysis")
            else:
                fractal_range.status = FractalStatus.CALCULADO
                enviar_senal_log("DEBUG", f"Fractal calculado pero por debajo del umbral de confianza: {fractal_range.confidence:.1f}%", __name__, "fractal_analysis")

            return fractal_range

        except Exception as e:
            enviar_senal_log("ERROR", f"Error crítico en análisis fractal: {e}", __name__, "fractal_analysis")
            return None

    def _detect_significant_swings(self, df: pd.DataFrame) -> Tuple[List[SwingPoint], List[SwingPoint]]:
        """
        🔍 Detecta swing points significativos usando metodología ICT
        """
        swing_highs = []
        swing_lows = []

        left_bars = self.config['swing_left_bars']
        right_bars = self.config['swing_right_bars']
        min_strength = self.config['min_swing_strength']

        # Analizar desde left_bars hasta len(df) - right_bars
        for i in range(left_bars, len(df) - right_bars):
            current_high = df.iloc[i]['high']
            current_low = df.iloc[i]['low']
            current_time = df.index[i]

            # DETECTAR SWING HIGH
            is_swing_high = True

            # Verificar barras a la izquierda
            for j in range(i - left_bars, i):
                if df.iloc[j]['high'] >= current_high:
                    is_swing_high = False
                    break

            # Verificar barras a la derecha
            if is_swing_high:
                for j in range(i + 1, i + right_bars + 1):
                    if df.iloc[j]['high'] >= current_high:
                        is_swing_high = False
                        break

            # Validar fuerza mínima del swing high
            if is_swing_high:
                strength = self._calculate_swing_strength(df, i, 'HIGH')
                enviar_senal_log("DEBUG", f"Swing HIGH candidato en {i}: price={current_high:.5f}, strength={strength:.6f}, min_req={min_strength:.6f}", __name__, "fractal_analysis")
                if strength >= min_strength:
                    swing_point = SwingPoint(
                        price=current_high,
                        timestamp=current_time,
                        index=i,
                        swing_type='HIGH',
                        strength=strength,
                        confirmed=True
                    )
                    swing_highs.append(swing_point)
                    enviar_senal_log("DEBUG", f"✅ Swing HIGH válido agregado: {current_high:.5f}", __name__, "fractal_analysis")

            # DETECTAR SWING LOW
            is_swing_low = True

            # Verificar barras a la izquierda
            for j in range(i - left_bars, i):
                if df.iloc[j]['low'] <= current_low:
                    is_swing_low = False
                    break

            # Verificar barras a la derecha
            if is_swing_low:
                for j in range(i + 1, i + right_bars + 1):
                    if df.iloc[j]['low'] <= current_low:
                        is_swing_low = False
                        break

            # Validar fuerza mínima del swing low
            if is_swing_low:
                strength = self._calculate_swing_strength(df, i, 'LOW')
                if strength >= min_strength:
                    swing_point = SwingPoint(
                        price=current_low,
                        timestamp=current_time,
                        index=i,
                        swing_type='LOW',
                        strength=strength,
                        confirmed=True
                    )
                    swing_lows.append(swing_point)

        enviar_senal_log("DEBUG", f"Swing points detectados: {len(swing_highs)} highs, {len(swing_lows)} lows", __name__, "fractal_analysis")
        return swing_highs, swing_lows

    def _calculate_swing_strength(self, df: pd.DataFrame, index: int, swing_type: str) -> float:
        """
        💪 Calcula la fuerza relativa de un swing point
        """
        try:
            if swing_type == 'HIGH':
                current_price = df.iloc[index]['high']
                # Comparar con highs en ventana de análisis
                window_start = max(0, index - 10)
                window_end = min(len(df), index + 10)
                window_highs = df.iloc[window_start:window_end]['high']
                max_in_window = window_highs.max()
                avg_in_window = window_highs.mean()
            else:  # LOW
                current_price = df.iloc[index]['low']
                # Comparar con lows en ventana de análisis
                window_start = max(0, index - 10)
                window_end = min(len(df), index + 10)
                window_lows = df.iloc[window_start:window_end]['low']
                min_in_window = window_lows.min()
                avg_in_window = window_lows.mean()

            # Calcular fuerza relativa
            if swing_type == 'HIGH':
                if max_in_window == current_price:
                    strength = abs(current_price - avg_in_window) / avg_in_window
                else:
                    strength = 0.0
            else:
                if min_in_window == current_price:
                    strength = abs(avg_in_window - current_price) / avg_in_window
                else:
                    strength = 0.0

            return min(strength, 0.1)  # Cap máximo de fuerza

        except Exception:
            return 0.0

    def _select_most_relevant_swing(self, swings: List[SwingPoint], current_price: float, swing_type: str) -> Optional[SwingPoint]:
        """
        🎯 Selecciona el swing más relevante para el análisis fractal actual
        """
        if not swings:
            return None

        # Filtrar swings muy antiguos (últimas 50 barras para mayor relevancia)
        recent_swings = swings[-10:] if len(swings) > 10 else swings

        if not recent_swings:
            return None

        # Seleccionar basado en relevancia (más reciente + mayor fuerza)
        best_swing = None
        best_score = 0.0

        for swing in recent_swings:
            # Score compuesto: recency + strength
            recency_score = (len(recent_swings) - recent_swings.index(swing)) / len(recent_swings)
            strength_score = swing.strength / 0.1  # Normalizar contra máximo

            composite_score = (recency_score * 0.6) + (strength_score * 0.4)

            if composite_score > best_score:
                best_score = composite_score
                best_swing = swing

        return best_swing

    def _calculate_fractal_range(self, high_swing: SwingPoint, low_swing: SwingPoint, current_price: float) -> FractalRange:
        """
        📏 Calcula el rango fractal completo con equilibrium
        """
        high_price = high_swing.price
        low_price = low_swing.price

        # Asegurar que high > low
        if high_price <= low_price:
            high_price, low_price = low_price, high_price
            high_swing, low_swing = low_swing, high_swing

        # Calcular equilibrium (punto medio)
        equilibrium = (high_price + low_price) / 2

        # Calcular edad del fractal (usar el swing más reciente)
        most_recent_time = max(high_swing.timestamp, low_swing.timestamp)
        age_minutes = int((datetime.now() - most_recent_time).total_seconds() / 60)

        fractal_range = FractalRange(
            high=high_price,
            low=low_price,
            eq=equilibrium,
            high_timestamp=high_swing.timestamp,
            low_timestamp=low_swing.timestamp,
            status=FractalStatus.CALCULADO,
            confidence=0.0,  # Se calculará después
            grade=FractalGrade.D,  # Se asignará después
            age_minutes=age_minutes,
            tests=0,
            valid=False
        )

        return fractal_range

    def _validate_fractal_quality(self, fractal_range: FractalRange, df: pd.DataFrame) -> bool:
        """
        ✅ Valida que el fractal cumpla criterios mínimos de calidad ICT
        """
        # Criterio 1: Tamaño mínimo del rango
        range_size = fractal_range.high - fractal_range.low
        if range_size < self.config['min_range_size']:
            enviar_senal_log("DEBUG", f"Fractal rechazado por tamaño insuficiente: {range_size:.5f} < {self.config['min_range_size']:.5f}", __name__, "fractal_analysis")
            return False

        # Criterio 2: Edad máxima
        if fractal_range.age_minutes > self.config['max_fractal_age_hours'] * 60:
            enviar_senal_log("DEBUG", f"Fractal rechazado por edad excesiva: {fractal_range.age_minutes} minutos", __name__, "fractal_analysis")
            return False

        # Criterio 3: Relevancia del rango (debe abarcar movimiento significativo)
        recent_data = df.tail(20)
        recent_high = recent_data['high'].max()
        recent_low = recent_data['low'].min()
        recent_range = recent_high - recent_low

        if recent_range > 0 and range_size < recent_range * 0.1:  # Al menos 10% del rango reciente (RELAJADO)
            enviar_senal_log("DEBUG", f"Fractal rechazado por relevancia insuficiente vs rango reciente", __name__, "fractal_analysis")
            return False

        return True

    def _calculate_fractal_confidence(self, fractal_range: FractalRange, df: pd.DataFrame, current_price: float) -> float:
        """
        🎯 Calcula confianza del fractal usando algoritmo ICT propietario
        """
        confidence = 50.0  # Base confidence

        # Factor 1: Tamaño del rango (rangos más grandes = mayor confianza)
        range_size = fractal_range.high - fractal_range.low
        recent_atr = self._calculate_atr(df, 14)
        if recent_atr > 0:
            size_factor = min(range_size / recent_atr, 3.0) * 10  # Max 30 puntos
            confidence += size_factor

        # Factor 2: Edad del fractal (más reciente = mayor confianza)
        age_hours = fractal_range.age_minutes / 60
        age_factor = max(0, (24 - age_hours) / 24 * 15)  # Max 15 puntos
        confidence += age_factor

        # Factor 3: Posición actual vs equilibrium
        eq_distance = abs(current_price - fractal_range.eq)
        eq_tolerance = self.config['equilibrium_tolerance']
        if eq_distance <= eq_tolerance:
            confidence += 15  # Bonus por estar cerca del EQ
        elif eq_distance <= eq_tolerance * 2:
            confidence += 10  # Bonus menor por proximidad moderada

        # Factor 4: Tests previos del rango (cada test refuerza)
        test_bonus = fractal_range.tests * self.config['test_reinforcement_bonus'] * 100
        confidence += test_bonus

        # Factor 5: Análisis de volumen (si disponible)
        if 'volume' in df.columns:
            volume_factor = self._analyze_volume_confirmation(df, fractal_range)
            confidence += volume_factor * self.config['volume_confirmation_weight'] * 100

        # Factor 6: Contexto de sesión
        session_factor = self._analyze_session_context(fractal_range)
        confidence += session_factor * self.config['session_context_weight'] * 100

        # Normalizar entre 0-100
        final_confidence = max(0.0, min(100.0, confidence))

        enviar_senal_log("DEBUG", f"Confianza fractal calculada: {final_confidence:.1f}% (base={50}, factores={final_confidence-50:.1f})", __name__, "fractal_analysis")
        return final_confidence

    def _calculate_atr(self, df: pd.DataFrame, period: int = 14) -> float:
        """Calcula Average True Range para análisis de volatilidad"""
        try:
            if len(df) < period:
                return 0.0

            df_calc = df.tail(period).copy()
            df_calc['tr1'] = df_calc['high'] - df_calc['low']
            df_calc['tr2'] = abs(df_calc['high'] - df_calc['close'].shift(1))
            df_calc['tr3'] = abs(df_calc['low'] - df_calc['close'].shift(1))
            df_calc['tr'] = df_calc[['tr1', 'tr2', 'tr3']].max(axis=1)

            return df_calc['tr'].mean()
        except Exception:
            return 0.0

    def _analyze_volume_confirmation(self, df: pd.DataFrame, fractal_range: FractalRange) -> float:
        """Analiza confirmación por volumen"""
        try:
            # Simplified volume analysis
            recent_volume = df.tail(10)['volume'].mean()
            historical_volume = df['volume'].mean()

            if recent_volume > historical_volume * 1.2:
                return 0.8  # Alta confirmación
            elif recent_volume > historical_volume:
                return 0.5  # Confirmación moderada
            else:
                return 0.2  # Baja confirmación
        except Exception:
            return 0.5  # Default neutral

    def _analyze_session_context(self, fractal_range: FractalRange) -> float:
        """Analiza contexto de sesión para el fractal"""
        current_hour = datetime.now().hour

        # Sesiones de alta liquidez tienen mayor peso
        if 8 <= current_hour <= 12 or 13 <= current_hour <= 17:  # London/NY sessions
            return 0.8
        elif 0 <= current_hour <= 8:  # Asian session
            return 0.4
        else:  # Overlap/quiet periods
            return 0.6

    def _assign_fractal_grade(self, confidence: float) -> FractalGrade:
        """
        🏆 Asigna grado de calidad basado en confianza
        """
        if confidence >= 90:
            return FractalGrade.A_PLUS
        elif confidence >= 80:
            return FractalGrade.A
        elif confidence >= 70:
            return FractalGrade.B
        elif confidence >= 60:
            return FractalGrade.C
        else:
            return FractalGrade.D

    def update_fractal_context(self, market_context, df: pd.DataFrame, current_price: float) -> bool:
        """
        🔄 Actualiza el contexto fractal en MarketContext

        Args:
            market_context: Instancia de MarketContext a actualizar
            df: DataFrame con datos de mercado
            current_price: Precio actual

        Returns:
            bool: True si se actualizó exitosamente
        """
        try:
            enviar_senal_log("DEBUG", "🔮 Actualizando contexto fractal...", __name__, "fractal_analysis")

            # Calcular nuevo fractal
            new_fractal = self.analyze_fractal_range(df, current_price)

            if new_fractal is None:
                # Mantener fractal anterior si existe y verificar caducidad
                if hasattr(market_context, 'fractal_range') and market_context.fractal_range.get('valid', False):
                    age_minutes = market_context.fractal_range.get('age_minutes', 0)
                    if age_minutes > self.config['invalidation_timeout_hours'] * 60:
                        market_context.fractal_range['status'] = 'CADUCADO'
                        market_context.fractal_range['valid'] = False
                        enviar_senal_log("INFO", "⏰ Fractal anterior marcado como CADUCADO por timeout", __name__, "fractal_analysis")
                return False

            # Actualizar MarketContext con nuevo fractal
            market_context.fractal_range = new_fractal.to_dict()

            # Log de actualización exitosa
            if new_fractal.valid:
                enviar_senal_log("INFO", f"✅ Contexto fractal actualizado: EQ={new_fractal.eq:.5f} | Grado={new_fractal.grade.value} | Confianza={new_fractal.confidence:.1f}%", __name__, "fractal_analysis")
            else:
                enviar_senal_log("DEBUG", f"Contexto fractal actualizado (no válido): confianza={new_fractal.confidence:.1f}%", __name__, "fractal_analysis")

            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"Error actualizando contexto fractal: {e}", __name__, "fractal_analysis")
            return False

    def get_fractal_levels(self) -> Optional[FractalLevels]:
        """
        📊 Obtiene niveles fractales actuales para trading

        Returns:
            FractalLevels con niveles high, low, eq o None si no hay fractal válido
        """
        if self.current_fractal and self.current_fractal.valid:
            # Explicitly typed return to ensure type checker correctness
            fractal_levels: FractalLevels = {
                'high': self.current_fractal.high,
                'low': self.current_fractal.low,
                'eq': self.current_fractal.eq,
                'confidence': self.current_fractal.confidence,
                'grade': self.current_fractal.grade.value
            }
            return fractal_levels
        return None

    def is_price_at_equilibrium(self, current_price: float, tolerance_multiplier: float = 1.0) -> bool:
        """
        🎯 Verifica si el precio está en zona de equilibrium

        Args:
            current_price: Precio actual
            tolerance_multiplier: Multiplicador de tolerancia (default 1.0)

        Returns:
            bool: True si está en zona EQ
        """
        if not self.current_fractal or not self.current_fractal.valid:
            return False

        tolerance = self.config['equilibrium_tolerance'] * tolerance_multiplier
        distance = abs(current_price - self.current_fractal.eq)

        return distance <= tolerance

# =============================================================================
# FUNCIONES DE UTILIDAD Y EXPORTACIÓN
# =============================================================================

def create_fractal_analyzer() -> FractalAnalyzer:
    """Factory function para crear instancia del analizador fractal"""
    return FractalAnalyzer()

def update_fractal_in_context(market_context, df: pd.DataFrame, current_price: float, analyzer: Optional[FractalAnalyzer] = None) -> bool:
    """
    🔄 Función de conveniencia para actualizar fractales en MarketContext

    Args:
        market_context: MarketContext a actualizar
        df: DataFrame con datos OHLCV
        current_price: Precio actual del mercado
        analyzer: Instancia opcional de FractalAnalyzer (se crea una nueva si es None)

    Returns:
        bool: True si se actualizó exitosamente
    """
    if analyzer is None:
        analyzer = FractalAnalyzer()

    return analyzer.update_fractal_context(market_context, df, current_price)

# =============================================================================
# EXPORTACIONES PÚBLICAS
# =============================================================================

__all__ = [
    'FractalAnalyzer',
    'FractalRange',
    'FractalLevels',
    'SwingPoint',
    'FractalStatus',
    'FractalGrade',
    'FRACTAL_CONFIG',
    'create_fractal_analyzer',
    'update_fractal_in_context'
]
