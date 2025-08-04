#!/usr/bin/env python3
"""
Market Structure Engine v2.0
============================

Motor avanzado de análisis de estructura de mercado con detección automática
de change of character (CHoCH), break of structure (BOS), y fair value gaps (FVG).

Características Sprint 1.7:
- Detección automática de CHoCH y BOS
- Análisis multi-timeframe de estructura
- Fair Value Gap detection y clasificación
- Order Block identification avanzada

Autor: ICT Engine Team
Sprint: 1.7 - Advanced Patterns
Fecha: 04 Agosto 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Sistema de logging SLUC v2.1
from sistema.logging_interface import enviar_senal_log

# ICT Types
from ..ict_types import SessionType, TradingDirection, SignalStrength


class StructureType(Enum):
    """Tipos de estructura de mercado"""
    CHOCH_BULLISH = "choch_bullish"          # Change of Character alcista
    CHOCH_BEARISH = "choch_bearish"          # Change of Character bajista
    BOS_BULLISH = "bos_bullish"              # Break of Structure alcista
    BOS_BEARISH = "bos_bearish"              # Break of Structure bajista
    RANGE_BOUND = "range_bound"              # Rango lateral
    CONSOLIDATION = "consolidation"          # Consolidación
    UNKNOWN = "unknown"


class FVGType(Enum):
    """Tipos de Fair Value Gap"""
    BULLISH_FVG = "bullish_fvg"             # FVG alcista
    BEARISH_FVG = "bearish_fvg"             # FVG bajista
    BALANCED_FVG = "balanced_fvg"           # FVG balanceado
    PREMIUM_FVG = "premium_fvg"             # FVG en premium
    DISCOUNT_FVG = "discount_fvg"           # FVG en discount


class OrderBlockType(Enum):
    """Tipos de Order Block"""
    BULLISH_OB = "bullish_ob"               # Order Block alcista
    BEARISH_OB = "bearish_ob"               # Order Block bajista
    BREAKER_BLOCK = "breaker_block"         # Breaker Block
    MITIGATION_BLOCK = "mitigation_block"   # Mitigation Block


@dataclass
class MarketStructureSignal:
    """Señal de estructura de mercado"""
    structure_type: StructureType
    confidence: float
    direction: TradingDirection
    break_level: float
    target_level: float
    narrative: str
    timestamp: datetime
    timeframe: str
    confluence_score: float
    fvg_present: bool
    order_block_present: bool


@dataclass
class FairValueGap:
    """Fair Value Gap detectado"""
    fvg_type: FVGType
    high_price: float
    low_price: float
    origin_candle: int
    filled_percentage: float
    is_mitigated: bool
    mitigation_candle: Optional[int]
    narrative: str
    timestamp: datetime


@dataclass
class OrderBlock:
    """Order Block detectado"""
    ob_type: OrderBlockType
    high_price: float
    low_price: float
    origin_candle: int
    reaction_strength: float
    is_tested: bool
    test_count: int
    narrative: str
    timestamp: datetime


class MarketStructureEngine:
    """
    🏗️ MARKET STRUCTURE ENGINE v2.0
    ===============================

    Motor profesional de análisis de estructura con:
    - Detección automática de CHoCH y BOS
    - Análisis multi-timeframe de estructura
    - Fair Value Gap detection y clasificación
    - Order Block identification avanzada
    """

    def __init__(self):
        """Inicializa el motor de estructura de mercado"""
        enviar_senal_log("INFO", "🏗️ Inicializando Market Structure Engine v2.0", __name__, "market_structure")

        # 🎯 Configuración de detección
        self.min_confidence = 70.0
        self.structure_lookback = 50  # Velas hacia atrás para análisis
        self.swing_window = 5         # Ventana para swing points
        self.fvg_min_gap = 0.0005    # Gap mínimo para FVG (5 pips)
        self.ob_reaction_threshold = 0.001  # Threshold para Order Block

        # 📊 Pesos de scoring
        self.structure_weight = 0.40
        self.momentum_weight = 0.25
        self.volume_weight = 0.20
        self.confluence_weight = 0.15

        # 📈 Estado interno
        self.detected_fvgs = []
        self.detected_order_blocks = []
        self.structure_history = []
        self.current_trend = TradingDirection.NEUTRAL

        enviar_senal_log("INFO", "✅ Market Structure Engine v2.0 inicializado", __name__, "market_structure")

    def analyze_market_structure(self,
                                candles_m15: pd.DataFrame,
                                candles_m5: Optional[pd.DataFrame] = None,
                                candles_h1: Optional[pd.DataFrame] = None,
                                current_price: float = 0.0) -> Optional[MarketStructureSignal]:
        """
        🏗️ ANÁLISIS COMPLETO DE ESTRUCTURA v2.0

        Args:
            candles_m15: Datos M15 para análisis principal
            candles_m5: Datos M5 para confirmación detallada
            candles_h1: Datos H1 para contexto superior
            current_price: Precio actual

        Returns:
            MarketStructureSignal si se detecta cambio estructural
        """
        try:
            enviar_senal_log("INFO", "🏗️ Iniciando análisis Market Structure v2.0", __name__, "market_structure")

            if candles_m15 is None or candles_m15.empty:
                enviar_senal_log("WARNING", "❌ Sin datos M15 para análisis estructura", __name__, "market_structure")
                return None

            # 1. 🎯 DETECTAR SWING POINTS
            swing_highs, swing_lows = self._detect_swing_points(candles_m15)
            if len(swing_highs) < 2 or len(swing_lows) < 2:
                enviar_senal_log("DEBUG", "🎯 Insuficientes swing points para análisis", __name__, "market_structure")
                return None

            # 2. 🔍 DETECTAR CAMBIOS ESTRUCTURALES
            structure_score, structure_type, break_level, target_level = self._detect_structure_change(
                candles_m15, swing_highs, swing_lows, current_price
            )

            if structure_score < 0.5:
                enviar_senal_log("DEBUG", f"🔍 Sin cambio estructural significativo: score={structure_score:.2f}", __name__, "market_structure")
                return None

            # 3. 💨 ANALIZAR MOMENTUM
            momentum_score = self._analyze_momentum(candles_m15, structure_type)

            # 4. 📊 ANALIZAR VOLUMEN
            volume_score = self._analyze_volume_structure(candles_m15)

            # 5. 🔗 ANALIZAR CONFLUENCIAS
            confluence_score = self._analyze_confluence(candles_m15, candles_h1, structure_type)

            # 6. 🧮 CALCULAR CONFIANZA TOTAL
            total_confidence = (
                structure_score * self.structure_weight +
                momentum_score * self.momentum_weight +
                volume_score * self.volume_weight +
                confluence_score * self.confluence_weight
            ) * 100

            # 7. ✅ VALIDAR THRESHOLD
            if total_confidence < self.min_confidence:
                enviar_senal_log("DEBUG", f"🏗️ Confianza insuficiente: {total_confidence:.1f}% < {self.min_confidence}%", __name__, "market_structure")
                return None

            # 8. 💎 DETECTAR FVGs
            fvg_present = self._detect_fair_value_gaps(candles_m15)

            # 9. 📦 DETECTAR ORDER BLOCKS
            ob_present = self._detect_order_blocks(candles_m15)

            # 10. 🎯 GENERAR SEÑAL
            signal = self._generate_structure_signal(
                structure_type=structure_type,
                confidence=total_confidence,
                break_level=break_level,
                target_level=target_level,
                confluence_score=confluence_score,
                fvg_present=fvg_present,
                ob_present=ob_present,
                candles=candles_m15
            )

            # 11. 📝 ACTUALIZAR ESTADO
            self._update_structure_state(structure_type, signal)

            enviar_senal_log("INFO", f"🎯 Estructura detectada: {signal.structure_type.value} - {signal.confidence:.1f}% confianza", __name__, "market_structure")
            return signal

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error en análisis Market Structure: {e}", __name__, "market_structure")
            return None

    def _detect_swing_points(self, candles: pd.DataFrame) -> Tuple[List[Dict], List[Dict]]:
        """🎯 Detecta swing highs y lows"""
        try:
            swing_highs = []
            swing_lows = []

            if len(candles) < self.swing_window * 2 + 1:
                return swing_highs, swing_lows

            # Detectar swing highs
            for i in range(self.swing_window, len(candles) - self.swing_window):
                current_high = candles.iloc[i]['high']

                # Verificar que sea el máximo en la ventana
                is_swing_high = True
                for j in range(i - self.swing_window, i + self.swing_window + 1):
                    if j != i and candles.iloc[j]['high'] >= current_high:
                        is_swing_high = False
                        break

                if is_swing_high:
                    swing_highs.append({
                        'index': i,
                        'price': current_high,
                        'timestamp': candles.index[i] if hasattr(candles.index[i], 'timestamp') else i
                    })

            # Detectar swing lows
            for i in range(self.swing_window, len(candles) - self.swing_window):
                current_low = candles.iloc[i]['low']

                # Verificar que sea el mínimo en la ventana
                is_swing_low = True
                for j in range(i - self.swing_window, i + self.swing_window + 1):
                    if j != i and candles.iloc[j]['low'] <= current_low:
                        is_swing_low = False
                        break

                if is_swing_low:
                    swing_lows.append({
                        'index': i,
                        'price': current_low,
                        'timestamp': candles.index[i] if hasattr(candles.index[i], 'timestamp') else i
                    })

            enviar_senal_log("DEBUG", f"🎯 Swing points: {len(swing_highs)} highs, {len(swing_lows)} lows", __name__, "market_structure")
            return swing_highs, swing_lows

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error detectando swing points: {e}", __name__, "market_structure")
            return [], []

    def _detect_structure_change(self, candles: pd.DataFrame, swing_highs: List[Dict], swing_lows: List[Dict], current_price: float) -> Tuple[float, StructureType, float, float]:
        """🔍 Detecta cambios estructurales (CHoCH/BOS)"""
        try:
            if len(swing_highs) < 2 or len(swing_lows) < 2:
                return 0.0, StructureType.UNKNOWN, 0.0, 0.0

            # Obtener últimos swing points
            last_high = swing_highs[-1]
            prev_high = swing_highs[-2] if len(swing_highs) > 1 else swing_highs[-1]
            last_low = swing_lows[-1]
            prev_low = swing_lows[-2] if len(swing_lows) > 1 else swing_lows[-1]

            structure_score = 0.0
            structure_type = StructureType.UNKNOWN
            break_level = 0.0
            target_level = 0.0

            # DETECTAR BOS ALCISTA (Rompe high anterior)
            if current_price > last_high['price'] and last_high['price'] > prev_high['price']:
                structure_score = 0.8
                structure_type = StructureType.BOS_BULLISH
                break_level = last_high['price']
                target_level = break_level * 1.002  # Target 20 pips arriba
                enviar_senal_log("DEBUG", f"🔍 BOS BULLISH detectado @ {break_level:.5f}", __name__, "market_structure")

            # DETECTAR BOS BAJISTA (Rompe low anterior)
            elif current_price < last_low['price'] and last_low['price'] < prev_low['price']:
                structure_score = 0.8
                structure_type = StructureType.BOS_BEARISH
                break_level = last_low['price']
                target_level = break_level * 0.998  # Target 20 pips abajo
                enviar_senal_log("DEBUG", f"🔍 BOS BEARISH detectado @ {break_level:.5f}", __name__, "market_structure")

            # DETECTAR CHOCH ALCISTA (Rompe low anterior en downtrend)
            elif (current_price > prev_low['price'] and
                  self.current_trend == TradingDirection.BEARISH and
                  last_low['price'] > prev_low['price']):
                structure_score = 0.9
                structure_type = StructureType.CHOCH_BULLISH
                break_level = prev_low['price']
                target_level = last_high['price']
                enviar_senal_log("DEBUG", f"🔍 CHoCH BULLISH detectado @ {break_level:.5f}", __name__, "market_structure")

            # DETECTAR CHOCH BAJISTA (Rompe high anterior en uptrend)
            elif (current_price < prev_high['price'] and
                  self.current_trend == TradingDirection.BULLISH and
                  last_high['price'] < prev_high['price']):
                structure_score = 0.9
                structure_type = StructureType.CHOCH_BEARISH
                break_level = prev_high['price']
                target_level = last_low['price']
                enviar_senal_log("DEBUG", f"🔍 CHoCH BEARISH detectado @ {break_level:.5f}", __name__, "market_structure")

            # DETECTAR RANGO
            elif self._is_range_bound(swing_highs, swing_lows):
                structure_score = 0.6
                structure_type = StructureType.RANGE_BOUND
                break_level = (last_high['price'] + last_low['price']) / 2
                target_level = break_level
                enviar_senal_log("DEBUG", f"🔍 RANGE BOUND detectado", __name__, "market_structure")

            return structure_score, structure_type, break_level, target_level

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error detectando cambio estructural: {e}", __name__, "market_structure")
            return 0.0, StructureType.UNKNOWN, 0.0, 0.0

    def _is_range_bound(self, swing_highs: List[Dict], swing_lows: List[Dict]) -> bool:
        """Detecta si el mercado está en rango"""
        try:
            if len(swing_highs) < 3 or len(swing_lows) < 3:
                return False

            # Verificar si los últimos 3 highs están cerca
            recent_highs = [sh['price'] for sh in swing_highs[-3:]]
            high_range = max(recent_highs) - min(recent_highs)
            avg_high = sum(recent_highs) / len(recent_highs)

            # Verificar si los últimos 3 lows están cerca
            recent_lows = [sl['price'] for sl in swing_lows[-3:]]
            low_range = max(recent_lows) - min(recent_lows)
            avg_low = sum(recent_lows) / len(recent_lows)

            # Si la variación es menor al 0.3% del precio promedio, es rango
            avg_price = (avg_high + avg_low) / 2
            high_variation = high_range / avg_price if avg_price > 0 else 1
            low_variation = low_range / avg_price if avg_price > 0 else 1

            return high_variation < 0.003 and low_variation < 0.003

        except Exception:
            return False

    def _analyze_momentum(self, candles: pd.DataFrame, structure_type: StructureType) -> float:
        """💨 Analiza momentum para confirmación"""
        try:
            if len(candles) < 20:
                return 0.5

            recent = candles.tail(10)

            # Calcular momentum básico
            price_change = (recent['close'].iloc[-1] - recent['close'].iloc[0]) / recent['close'].iloc[0]
            momentum_score = 0.5

            # Analizar según tipo de estructura
            if structure_type in [StructureType.BOS_BULLISH, StructureType.CHOCH_BULLISH]:
                if price_change > 0:
                    momentum_score += 0.3
                if price_change > 0.001:  # >10 pips
                    momentum_score += 0.2

            elif structure_type in [StructureType.BOS_BEARISH, StructureType.CHOCH_BEARISH]:
                if price_change < 0:
                    momentum_score += 0.3
                if price_change < -0.001:  # <-10 pips
                    momentum_score += 0.2

            # Analizar velas de confirmación
            bullish_candles = sum(1 for _, candle in recent.iterrows()
                                if candle['close'] > candle['open'])
            bearish_candles = len(recent) - bullish_candles

            if structure_type in [StructureType.BOS_BULLISH, StructureType.CHOCH_BULLISH]:
                if bullish_candles > bearish_candles:
                    momentum_score += 0.1
            elif structure_type in [StructureType.BOS_BEARISH, StructureType.CHOCH_BEARISH]:
                if bearish_candles > bullish_candles:
                    momentum_score += 0.1

            return min(momentum_score, 1.0)

        except Exception:
            return 0.5

    def _analyze_volume_structure(self, candles: pd.DataFrame) -> float:
        """📊 Analiza volumen para confirmación estructural"""
        try:
            if 'tick_volume' not in candles.columns or len(candles) < 20:
                return 0.5

            recent = candles.tail(10)
            historical = candles.tail(30).head(20)

            recent_avg_volume = recent['tick_volume'].mean()
            historical_avg_volume = historical['tick_volume'].mean()

            if historical_avg_volume == 0:
                return 0.5

            volume_ratio = recent_avg_volume / historical_avg_volume

            # Scoring basado en volumen relativo
            if volume_ratio > 1.5:
                return 0.9  # Alto volumen confirma breakout
            elif volume_ratio > 1.2:
                return 0.7
            elif volume_ratio > 0.8:
                return 0.5
            else:
                return 0.3  # Bajo volumen = débil confirmación

        except Exception:
            return 0.5

    def _analyze_confluence(self, candles_m15: pd.DataFrame, candles_h1: Optional[pd.DataFrame], structure_type: StructureType) -> float:
        """🔗 Analiza confluencias multi-timeframe"""
        try:
            confluence_score = 0.5

            # Verificar alineación con timeframe superior
            if candles_h1 is not None and len(candles_h1) >= 10:
                h1_trend = self._detect_higher_tf_trend(candles_h1)

                # Bonus por alineación
                if structure_type in [StructureType.BOS_BULLISH, StructureType.CHOCH_BULLISH]:
                    if h1_trend == TradingDirection.BULLISH:
                        confluence_score += 0.3
                elif structure_type in [StructureType.BOS_BEARISH, StructureType.CHOCH_BEARISH]:
                    if h1_trend == TradingDirection.BEARISH:
                        confluence_score += 0.3

            # Verificar presencia de niveles clave
            if self.detected_fvgs:
                confluence_score += 0.1

            if self.detected_order_blocks:
                confluence_score += 0.1

            return min(confluence_score, 1.0)

        except Exception:
            return 0.5

    def _detect_higher_tf_trend(self, candles_h1: pd.DataFrame) -> TradingDirection:
        """Detecta tendencia en timeframe superior"""
        try:
            if len(candles_h1) < 5:
                return TradingDirection.NEUTRAL

            recent = candles_h1.tail(5)

            # Análisis simple de tendencia
            price_change = (recent['close'].iloc[-1] - recent['close'].iloc[0]) / recent['close'].iloc[0]

            if price_change > 0.005:  # >50 pips en H1
                return TradingDirection.BULLISH
            elif price_change < -0.005:  # <-50 pips en H1
                return TradingDirection.BEARISH
            else:
                return TradingDirection.NEUTRAL

        except Exception:
            return TradingDirection.NEUTRAL

    def _detect_fair_value_gaps(self, candles: pd.DataFrame) -> bool:
        """💎 Detecta Fair Value Gaps"""
        try:
            if len(candles) < 10:
                return False

            fvg_found = False
            recent = candles.tail(20)

            for i in range(2, len(recent)):
                candle_1 = recent.iloc[i-2]  # Candle anterior
                candle_2 = recent.iloc[i-1]  # Candle medio
                candle_3 = recent.iloc[i]    # Candle actual

                # Detectar FVG alcista
                if candle_1['low'] > candle_3['high']:
                    gap_size = candle_1['low'] - candle_3['high']
                    if gap_size > self.fvg_min_gap:
                        fvg = FairValueGap(
                            fvg_type=FVGType.BULLISH_FVG,
                            high_price=candle_1['low'],
                            low_price=candle_3['high'],
                            origin_candle=i,
                            filled_percentage=0.0,
                            is_mitigated=False,
                            mitigation_candle=None,
                            narrative=f"Bullish FVG: gap {gap_size:.5f}",
                            timestamp=datetime.now()
                        )
                        self.detected_fvgs.append(fvg)
                        fvg_found = True
                        enviar_senal_log("DEBUG", f"💎 Bullish FVG detectado: {gap_size:.5f}", __name__, "market_structure")

                # Detectar FVG bajista
                elif candle_1['high'] < candle_3['low']:
                    gap_size = candle_3['low'] - candle_1['high']
                    if gap_size > self.fvg_min_gap:
                        fvg = FairValueGap(
                            fvg_type=FVGType.BEARISH_FVG,
                            high_price=candle_3['low'],
                            low_price=candle_1['high'],
                            origin_candle=i,
                            filled_percentage=0.0,
                            is_mitigated=False,
                            mitigation_candle=None,
                            narrative=f"Bearish FVG: gap {gap_size:.5f}",
                            timestamp=datetime.now()
                        )
                        self.detected_fvgs.append(fvg)
                        fvg_found = True
                        enviar_senal_log("DEBUG", f"💎 Bearish FVG detectado: {gap_size:.5f}", __name__, "market_structure")

            # Limpiar FVGs antiguos
            self.detected_fvgs = self.detected_fvgs[-10:]  # Mantener solo últimos 10

            return fvg_found

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error detectando FVG: {e}", __name__, "market_structure")
            return False

    def _detect_order_blocks(self, candles: pd.DataFrame) -> bool:
        """📦 Detecta Order Blocks"""
        try:
            if len(candles) < 15:
                return False

            ob_found = False
            recent = candles.tail(20)

            for i in range(5, len(recent) - 5):
                candle = recent.iloc[i]

                # Verificar reacción fuerte desde este nivel
                reaction_score = self._calculate_reaction_strength(recent, i)

                if reaction_score > self.ob_reaction_threshold:
                    # Determinar tipo de Order Block
                    if candle['close'] > candle['open']:  # Bullish candle
                        ob_type = OrderBlockType.BULLISH_OB
                        narrative = f"Bullish Order Block: reacción {reaction_score:.4f}"
                    else:  # Bearish candle
                        ob_type = OrderBlockType.BEARISH_OB
                        narrative = f"Bearish Order Block: reacción {reaction_score:.4f}"

                    order_block = OrderBlock(
                        ob_type=ob_type,
                        high_price=candle['high'],
                        low_price=candle['low'],
                        origin_candle=i,
                        reaction_strength=reaction_score,
                        is_tested=False,
                        test_count=0,
                        narrative=narrative,
                        timestamp=datetime.now()
                    )

                    self.detected_order_blocks.append(order_block)
                    ob_found = True
                    enviar_senal_log("DEBUG", f"📦 Order Block detectado: {ob_type.value}", __name__, "market_structure")

            # Limpiar Order Blocks antiguos
            self.detected_order_blocks = self.detected_order_blocks[-10:]  # Mantener solo últimos 10

            return ob_found

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error detectando Order Blocks: {e}", __name__, "market_structure")
            return False

    def _calculate_reaction_strength(self, candles: pd.DataFrame, candle_index: int) -> float:
        """Calcula fuerza de reacción desde un nivel"""
        try:
            if candle_index < 2 or candle_index >= len(candles) - 2:
                return 0.0

            base_candle = candles.iloc[candle_index]
            base_price = (base_candle['high'] + base_candle['low']) / 2

            # Calcular movimiento después del candle
            max_move = 0.0
            for i in range(candle_index + 1, min(candle_index + 6, len(candles))):
                next_candle = candles.iloc[i]
                move = abs(next_candle['close'] - base_price) / base_price
                max_move = max(max_move, move)

            return max_move

        except Exception:
            return 0.0

    def _generate_structure_signal(self, **kwargs) -> MarketStructureSignal:
        """🎯 Genera señal de estructura completa"""
        try:
            structure_type = kwargs.get('structure_type', StructureType.UNKNOWN)
            confidence = kwargs.get('confidence', 70.0)

            # Determinar dirección
            if structure_type in [StructureType.BOS_BULLISH, StructureType.CHOCH_BULLISH]:
                direction = TradingDirection.BULLISH
            elif structure_type in [StructureType.BOS_BEARISH, StructureType.CHOCH_BEARISH]:
                direction = TradingDirection.BEARISH
            else:
                direction = TradingDirection.NEUTRAL

            # Generar narrativa
            narrative = self._generate_structure_narrative(structure_type, confidence)

            signal = MarketStructureSignal(
                structure_type=structure_type,
                confidence=confidence,
                direction=direction,
                break_level=kwargs.get('break_level', 0.0),
                target_level=kwargs.get('target_level', 0.0),
                narrative=narrative,
                timestamp=datetime.now(),
                timeframe="M15",
                confluence_score=kwargs.get('confluence_score', 0.5),
                fvg_present=kwargs.get('fvg_present', False),
                order_block_present=kwargs.get('ob_present', False)
            )

            return signal

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error generando señal estructura: {e}", __name__, "market_structure")
            return MarketStructureSignal(
                structure_type=StructureType.UNKNOWN,
                confidence=0.0,
                direction=TradingDirection.NEUTRAL,
                break_level=0.0,
                target_level=0.0,
                narrative="Error generating signal",
                timestamp=datetime.now(),
                timeframe="M15",
                confluence_score=0.0,
                fvg_present=False,
                order_block_present=False
            )

    def _generate_structure_narrative(self, structure_type: StructureType, confidence: float) -> str:
        """Genera narrativa para cambio estructural"""
        try:
            type_descriptions = {
                StructureType.CHOCH_BULLISH: "🔄 Change of Character BULLISH - Reversión alcista confirmada",
                StructureType.CHOCH_BEARISH: "🔄 Change of Character BEARISH - Reversión bajista confirmada",
                StructureType.BOS_BULLISH: "📈 Break of Structure BULLISH - Continuación alcista",
                StructureType.BOS_BEARISH: "📉 Break of Structure BEARISH - Continuación bajista",
                StructureType.RANGE_BOUND: "↔️ Range Bound - Mercado lateral entre niveles",
                StructureType.CONSOLIDATION: "🔄 Consolidation - Pausa en la tendencia",
                StructureType.UNKNOWN: "❓ Estructura indefinida"
            }

            base_desc = type_descriptions.get(structure_type, "Cambio estructural")

            # Añadir contexto de confianza
            if confidence > 85:
                conf_desc = "con ALTA confianza"
            elif confidence > 75:
                conf_desc = "con BUENA confianza"
            else:
                conf_desc = "con MODERADA confianza"

            narrative = f"{base_desc} {conf_desc} ({confidence:.1f}%). "

            # Añadir contexto adicional
            if self.detected_fvgs:
                narrative += "FVG presente. "
            if self.detected_order_blocks:
                narrative += "Order Block detectado. "

            return narrative.strip()

        except Exception:
            return "Market structure change detected"

    def _update_structure_state(self, structure_type: StructureType, signal: MarketStructureSignal):
        """📝 Actualiza estado interno de estructura"""
        try:
            # Actualizar tendencia actual
            if structure_type in [StructureType.BOS_BULLISH, StructureType.CHOCH_BULLISH]:
                self.current_trend = TradingDirection.BULLISH
            elif structure_type in [StructureType.BOS_BEARISH, StructureType.CHOCH_BEARISH]:
                self.current_trend = TradingDirection.BEARISH
            else:
                self.current_trend = TradingDirection.NEUTRAL

            # Añadir a historial
            self.structure_history.append({
                'timestamp': datetime.now(),
                'structure_type': structure_type,
                'confidence': signal.confidence,
                'direction': signal.direction
            })

            # Mantener historial limitado
            self.structure_history = self.structure_history[-20:]

            enviar_senal_log("DEBUG", f"📝 Estado actualizado: tendencia={self.current_trend.value}", __name__, "market_structure")

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error actualizando estado: {e}", __name__, "market_structure")
