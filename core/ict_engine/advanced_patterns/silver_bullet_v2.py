#!/usr/bin/env python3
"""
Advanced Silver Bullet Detector v2.0
====================================

Detector avanzado de patrones Silver Bullet con timing preciso,
integración de killzones y confluencia con Order Blocks.

Características Sprint 1.7:
- Timing específico (3-5 AM, 10-11 AM EST)
- Confluencia con Order Blocks
- Validación multi-timeframe
- Análisis de estructura completa

Autor: ICT Engine Team
Sprint: 1.7 - Advanced Patterns
Fecha: 04 Agosto 2025
"""

import pandas as pd
from datetime import datetime, time, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Sistema de logging SLUC v2.1
from sistema.logging_interface import enviar_senal_log

# ICT Types
from ..ict_types import SessionType, TradingDirection, SignalStrength


class SilverBulletType(Enum):
    """Tipos de Silver Bullet según sesión"""
    LONDON_KILL = "london_killzone"      # 3-5 AM EST
    NY_KILL = "newyork_killzone"         # 10-11 AM EST
    LONDON_CLOSE = "london_close"        # 10-11 AM EST (overlap)
    UNKNOWN = "unknown"


@dataclass
class SilverBulletSignal:
    """Señal Silver Bullet avanzada"""
    signal_type: SilverBulletType
    confidence: float
    direction: TradingDirection
    entry_price: float
    structure_confluence: bool
    killzone_timing: bool
    order_block_present: bool
    timeframe_alignment: bool
    narrative: str
    timestamp: datetime
    session_context: Dict


class AdvancedSilverBulletDetector:
    """
    🔫 ADVANCED SILVER BULLET DETECTOR v2.0
    =======================================

    Detector profesional de patrones Silver Bullet con:
    - Timing específico de killzones
    - Confluencia estructural
    - Validación multi-timeframe
    """

    def __init__(self):
        """Inicializa el detector avanzado Silver Bullet"""
        enviar_senal_log("INFO", "🔫 Inicializando Advanced Silver Bullet Detector v2.0", __name__, "silver_bullet")

        # ⏰ Configuración de timing (EST)
        self.london_killzone = (time(3, 0), time(5, 0))    # 3-5 AM EST
        self.ny_killzone = (time(10, 0), time(11, 0))       # 10-11 AM EST
        self.london_close = (time(10, 0), time(11, 0))      # Overlap period

        # 🎯 Configuración de detección
        self.min_confidence = 75.0
        self.structure_weight = 0.3
        self.timing_weight = 0.4
        self.confluence_weight = 0.3

        # 📊 Estado interno
        self.last_analysis = None
        self.detected_obs = []

        enviar_senal_log("INFO", "✅ Silver Bullet Detector v2.0 inicializado", __name__, "silver_bullet")

    def analyze_silver_bullet_setup(self,
                                  candles_m5: pd.DataFrame,
                                  candles_m1: Optional[pd.DataFrame] = None,
                                  candles_h1: Optional[pd.DataFrame] = None,
                                  current_price: float = 0.0,
                                  detected_obs: List[Dict] = None) -> Optional[SilverBulletSignal]:
        """
        🎯 ANÁLISIS COMPLETO SILVER BULLET v2.0

        Args:
            candles_m5: Datos M5 para estructura principal
            candles_m1: Datos M1 para confirmación (opcional)
            candles_h1: Datos H1 para contexto (opcional)
            current_price: Precio actual
            detected_obs: Order Blocks detectados

        Returns:
            SilverBulletSignal si se detecta patrón válido
        """
        try:
            enviar_senal_log("INFO", "🔫 Iniciando análisis Silver Bullet v2.0", __name__, "silver_bullet")

            if candles_m5 is None or candles_m5.empty:
                enviar_senal_log("WARNING", "❌ Sin datos M5 para análisis Silver Bullet", __name__, "silver_bullet")
                return None

            # 1. ⏰ VALIDAR TIMING DE KILLZONE
            timing_score, killzone_type = self._validate_killzone_timing()
            if timing_score < 0.5:
                enviar_senal_log("DEBUG", f"⏰ Fuera de killzone: score={timing_score:.2f}", __name__, "silver_bullet")
                return None

            # 2. 📊 ANALIZAR ESTRUCTURA DE MERCADO
            structure_score, direction = self._analyze_market_structure(candles_m5, candles_h1)

            # 3. 🎯 DETECTAR CONFLUENCIA CON ORDER BLOCKS
            confluence_score, ob_present = self._analyze_ob_confluence(candles_m5, detected_obs or [], current_price)

            # 4. 📈 VALIDACIÓN MULTI-TIMEFRAME
            mtf_score, mtf_aligned = self._validate_multi_timeframe_alignment(candles_m5, candles_m1, candles_h1)

            # 5. 🧮 CALCULAR CONFIANZA TOTAL
            total_confidence = (
                timing_score * self.timing_weight +
                structure_score * self.structure_weight +
                confluence_score * self.confluence_weight +
                mtf_score * 0.2  # Peso adicional para MTF
            ) * 100

            # 6. ✅ VALIDAR THRESHOLD
            if total_confidence < self.min_confidence:
                enviar_senal_log("DEBUG", f"🔫 Confianza insuficiente: {total_confidence:.1f}% < {self.min_confidence}%", __name__, "silver_bullet")
                return None

            # 7. 🎯 GENERAR SEÑAL SILVER BULLET
            signal = self._generate_silver_bullet_signal(
                killzone_type=killzone_type,
                confidence=total_confidence,
                direction=direction,
                entry_price=current_price or candles_m5['close'].iloc[-1],
                structure_confluence=confluence_score > 0.6,
                killzone_timing=timing_score > 0.7,
                order_block_present=ob_present,
                timeframe_alignment=mtf_aligned,
                candles_m5=candles_m5
            )

            enviar_senal_log("INFO", f"🎯 Silver Bullet detectado: {signal.signal_type.value} - {signal.confidence:.1f}% confianza", __name__, "silver_bullet")
            return signal

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error en análisis Silver Bullet: {e}", __name__, "silver_bullet")
            return None

    def _validate_killzone_timing(self) -> Tuple[float, SilverBulletType]:
        """⏰ Valida si estamos en una killzone válida"""
        try:
            current_time = datetime.now().time()

            # London Killzone (3-5 AM EST)
            if self.london_killzone[0] <= current_time <= self.london_killzone[1]:
                score = 1.0
                killzone = SilverBulletType.LONDON_KILL
                enviar_senal_log("DEBUG", f"⏰ London Killzone activa: {current_time}", __name__, "silver_bullet")
                return score, killzone

            # NY Killzone (10-11 AM EST)
            if self.ny_killzone[0] <= current_time <= self.ny_killzone[1]:
                score = 1.0
                killzone = SilverBulletType.NY_KILL
                enviar_senal_log("DEBUG", f"⏰ NY Killzone activa: {current_time}", __name__, "silver_bullet")
                return score, killzone

            # Zona de tolerancia (30 min antes/después)
            tolerance = timedelta(minutes=30)

            # Verificar tolerancia London
            london_start = datetime.combine(datetime.now().date(), self.london_killzone[0])
            london_end = datetime.combine(datetime.now().date(), self.london_killzone[1])
            current_dt = datetime.combine(datetime.now().date(), current_time)

            if (london_start - tolerance <= current_dt <= london_start) or (london_end <= current_dt <= london_end + tolerance):
                score = 0.6  # Puntuación reducida en tolerancia
                killzone = SilverBulletType.LONDON_KILL
                enviar_senal_log("DEBUG", f"⏰ London Killzone (tolerancia): {current_time}", __name__, "silver_bullet")
                return score, killzone

            # Verificar tolerancia NY
            ny_start = datetime.combine(datetime.now().date(), self.ny_killzone[0])
            ny_end = datetime.combine(datetime.now().date(), self.ny_killzone[1])

            if (ny_start - tolerance <= current_dt <= ny_start) or (ny_end <= current_dt <= ny_end + tolerance):
                score = 0.6  # Puntuación reducida en tolerancia
                killzone = SilverBulletType.NY_KILL
                enviar_senal_log("DEBUG", f"⏰ NY Killzone (tolerancia): {current_time}", __name__, "silver_bullet")
                return score, killzone

            # Fuera de horarios válidos
            enviar_senal_log("DEBUG", f"⏰ Fuera de killzones: {current_time}", __name__, "silver_bullet")
            return 0.0, SilverBulletType.UNKNOWN

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error validando timing: {e}", __name__, "silver_bullet")
            return 0.0, SilverBulletType.UNKNOWN

    def _analyze_market_structure(self, candles_m5: pd.DataFrame, candles_h1: Optional[pd.DataFrame]) -> Tuple[float, TradingDirection]:
        """📊 Analiza estructura de mercado para Silver Bullet"""
        try:
            if len(candles_m5) < 20:
                return 0.3, TradingDirection.NEUTRAL

            # Análisis de estructura M5
            recent_m5 = candles_m5.tail(20)

            # Detectar swing highs/lows
            highs = recent_m5['high'].rolling(window=3, center=True).max()
            lows = recent_m5['low'].rolling(window=3, center=True).min()

            # Determinar dirección predominante
            recent_close = recent_m5['close'].iloc[-1]
            sma_10 = recent_m5['close'].rolling(10).mean().iloc[-1]
            sma_20 = recent_m5['close'].rolling(20).mean().iloc[-1]

            # Scoring basado en posición relativa
            if recent_close > sma_10 > sma_20:
                direction = TradingDirection.BULLISH
                structure_score = 0.8
            elif recent_close < sma_10 < sma_20:
                direction = TradingDirection.BEARISH
                structure_score = 0.8
            else:
                direction = TradingDirection.NEUTRAL
                structure_score = 0.4

            # Bonus por confirmación H1 si disponible
            if candles_h1 is not None and len(candles_h1) >= 10:
                h1_recent = candles_h1.tail(10)
                h1_sma = h1_recent['close'].rolling(5).mean().iloc[-1]
                h1_close = h1_recent['close'].iloc[-1]

                if (direction == TradingDirection.BULLISH and h1_close > h1_sma) or \
                   (direction == TradingDirection.BEARISH and h1_close < h1_sma):
                    structure_score += 0.15  # Bonus por alineación MTF

            enviar_senal_log("DEBUG", f"📊 Estructura: {direction.value} - Score: {structure_score:.2f}", __name__, "silver_bullet")
            return min(structure_score, 1.0), direction

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error analizando estructura: {e}", __name__, "silver_bullet")
            return 0.3, TradingDirection.NEUTRAL

    def _analyze_ob_confluence(self, candles_m5: pd.DataFrame, detected_obs: List[Dict], current_price: float) -> Tuple[float, bool]:
        """🎯 Analiza confluencia con Order Blocks"""
        try:
            if not detected_obs:
                enviar_senal_log("DEBUG", "🎯 Sin Order Blocks para confluencia", __name__, "silver_bullet")
                return 0.3, False

            confluence_score = 0.0
            ob_present = False

            # Evaluar proximidad a Order Blocks
            for ob in detected_obs:
                ob_price = ob.get('price', 0)
                if ob_price == 0:
                    continue

                # Calcular distancia relativa
                distance = abs(current_price - ob_price) / current_price if current_price > 0 else 1.0

                # Si estamos cerca del OB (< 20 pips en EURUSD)
                if distance < 0.002:  # ~20 pips
                    confluence_score += 0.4
                    ob_present = True

                    # Bonus por tipo de OB
                    ob_type = ob.get('type', '')
                    if 'BULLISH' in ob_type or 'BEARISH' in ob_type:
                        confluence_score += 0.2

                    enviar_senal_log("DEBUG", f"🎯 OB confluencia: {ob_type} @ {ob_price:.5f} - Distancia: {distance:.4f}", __name__, "silver_bullet")

            # Bonus por múltiples OBs cerca
            if len([ob for ob in detected_obs if abs(current_price - ob.get('price', 0)) / current_price < 0.003]) > 1:
                confluence_score += 0.2

            final_score = min(confluence_score, 1.0)
            enviar_senal_log("DEBUG", f"🎯 Confluencia OB: Score={final_score:.2f}, Present={ob_present}", __name__, "silver_bullet")
            return final_score, ob_present

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error analizando confluencia OB: {e}", __name__, "silver_bullet")
            return 0.3, False

    def _validate_multi_timeframe_alignment(self,
                                          candles_m5: pd.DataFrame,
                                          candles_m1: Optional[pd.DataFrame],
                                          candles_h1: Optional[pd.DataFrame]) -> Tuple[float, bool]:
        """📈 Valida alineación multi-timeframe"""
        try:
            alignment_score = 0.5  # Base score
            aligned = False

            if candles_m1 is not None and len(candles_m1) >= 10:
                # Verificar alineación M1-M5
                m1_trend = self._get_timeframe_trend(candles_m1.tail(10))
                m5_trend = self._get_timeframe_trend(candles_m5.tail(10))

                if m1_trend == m5_trend and m1_trend != TradingDirection.NEUTRAL:
                    alignment_score += 0.2
                    aligned = True

            if candles_h1 is not None and len(candles_h1) >= 5:
                # Verificar alineación H1
                h1_trend = self._get_timeframe_trend(candles_h1.tail(5))
                m5_trend = self._get_timeframe_trend(candles_m5.tail(10))

                if h1_trend == m5_trend and h1_trend != TradingDirection.NEUTRAL:
                    alignment_score += 0.25
                    aligned = True

            final_score = min(alignment_score, 1.0)
            enviar_senal_log("DEBUG", f"📈 MTF Alignment: Score={final_score:.2f}, Aligned={aligned}", __name__, "silver_bullet")
            return final_score, aligned

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error validando MTF alignment: {e}", __name__, "silver_bullet")
            return 0.5, False

    def _get_timeframe_trend(self, candles: pd.DataFrame) -> TradingDirection:
        """Determina tendencia en un timeframe específico"""
        try:
            if len(candles) < 3:
                return TradingDirection.NEUTRAL

            close = candles['close']
            sma_short = close.rolling(3).mean().iloc[-1]
            sma_long = close.rolling(min(len(candles), 5)).mean().iloc[-1]
            current = close.iloc[-1]

            if current > sma_short > sma_long:
                return TradingDirection.BULLISH
            elif current < sma_short < sma_long:
                return TradingDirection.BEARISH
            else:
                return TradingDirection.NEUTRAL

        except Exception:
            return TradingDirection.NEUTRAL

    def _generate_silver_bullet_signal(self, **kwargs) -> SilverBulletSignal:
        """🎯 Genera señal Silver Bullet completa"""
        try:
            # Extraer datos
            killzone_type = kwargs.get('killzone_type', SilverBulletType.UNKNOWN)
            confidence = kwargs.get('confidence', 75.0)
            direction = kwargs.get('direction', TradingDirection.NEUTRAL)
            entry_price = kwargs.get('entry_price', 1.0)
            candles_m5 = kwargs.get('candles_m5')

            # Generar narrativa contextual
            narrative = self._generate_narrative(killzone_type, direction, confidence, candles_m5)

            # Crear contexto de sesión
            session_context = {
                'killzone_active': killzone_type != SilverBulletType.UNKNOWN,
                'market_phase': 'manipulation' if confidence > 85 else 'distribution',
                'volatility': self._calculate_volatility(candles_m5) if candles_m5 is not None else 0.0,
                'session_strength': confidence / 100.0
            }

            signal = SilverBulletSignal(
                signal_type=killzone_type,
                confidence=confidence,
                direction=direction,
                entry_price=entry_price,
                structure_confluence=kwargs.get('structure_confluence', False),
                killzone_timing=kwargs.get('killzone_timing', False),
                order_block_present=kwargs.get('order_block_present', False),
                timeframe_alignment=kwargs.get('timeframe_alignment', False),
                narrative=narrative,
                timestamp=datetime.now(),
                session_context=session_context
            )

            return signal

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error generando señal: {e}", __name__, "silver_bullet")
            # Return minimal signal
            return SilverBulletSignal(
                signal_type=SilverBulletType.UNKNOWN,
                confidence=0.0,
                direction=TradingDirection.NEUTRAL,
                entry_price=0.0,
                structure_confluence=False,
                killzone_timing=False,
                order_block_present=False,
                timeframe_alignment=False,
                narrative="Error generating signal",
                timestamp=datetime.now(),
                session_context={}
            )

    def _generate_narrative(self, killzone_type: SilverBulletType, direction: TradingDirection, confidence: float, candles_m5: pd.DataFrame) -> str:
        """Genera narrativa contextual para la señal"""
        try:
            # Base de la narrativa según killzone
            if killzone_type == SilverBulletType.LONDON_KILL:
                base = "🇬🇧 London Killzone Silver Bullet"
            elif killzone_type == SilverBulletType.NY_KILL:
                base = "🇺🇸 New York Killzone Silver Bullet"
            else:
                base = "🔫 Silver Bullet Pattern"

            # Dirección y confianza
            direction_text = {
                TradingDirection.BULLISH: "📈 BULLISH setup",
                TradingDirection.BEARISH: "📉 BEARISH setup",
                TradingDirection.NEUTRAL: "⚖️ NEUTRAL setup"
            }.get(direction, "Unknown direction")

            # Nivel de confianza
            if confidence > 90:
                confidence_text = "EXCEPTIONAL confidence"
            elif confidence > 80:
                confidence_text = "HIGH confidence"
            elif confidence > 70:
                confidence_text = "GOOD confidence"
            else:
                confidence_text = "MODERATE confidence"

            # Contexto adicional
            context = ""
            if candles_m5 is not None and len(candles_m5) >= 5:
                volatility = self._calculate_volatility(candles_m5)
                if volatility > 0.001:
                    context = " con alta volatilidad"
                elif volatility < 0.0005:
                    context = " en condiciones de baja volatilidad"

            narrative = f"{base} detectado: {direction_text} con {confidence_text} ({confidence:.1f}%){context}. Setup ideal para entry en killzone activa."

            return narrative

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error generando narrativa: {e}", __name__, "silver_bullet")
            return "Silver Bullet pattern detected"

    def _calculate_volatility(self, candles: pd.DataFrame) -> float:
        """Calcula volatilidad de las velas"""
        try:
            if len(candles) < 5:
                return 0.0

            recent = candles.tail(10)
            ranges = recent['high'] - recent['low']
            return float(ranges.mean())

        except Exception:
            return 0.0
