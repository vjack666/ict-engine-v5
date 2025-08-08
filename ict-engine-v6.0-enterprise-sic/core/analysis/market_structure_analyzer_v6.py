#!/usr/bin/env python3
"""
🏗️ MARKET STRUCTURE ANALYZER v6.0 ENTERPRISE
============================================

Versión enterprise del Market Structure Engine que fusiona:
- Market Structure v2.0 (proyecto principal) - 739 líneas probadas
- Integración SIC v3.1 Enterprise
- Datos reales FundedNext MT5
- SLUC v2.1 Logging Enterprise
- Performance optimizations

Características v6.0:
✅ CHoCH/BOS detection (migrado de v2.0)
✅ Fair Value Gap detection (migrado de v2.0)
✅ Order Block identification (migrado de v2.0)
✅ Multi-timeframe analysis
✅ SIC Bridge integration
✅ Real data compatibility
✅ Enterprise logging

Autor: ICT Engine Team v6.0
Migrado desde: proyecto principal/core/ict_engine/advanced_patterns/market_structure_v2.py
Fecha: 07 Agosto 2025
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import time

# SIC Bridge Integration v6.0
from sistema.sic_bridge import get_sic_bridge, smart_import

# Enterprise logging SLUC v2.1
from core.smart_trading_logger import SmartTradingLogger

# ICT Types v6.0 Enterprise
from core.ict_engine.ict_types import TradingDirection

# Data management para datos reales
from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader


class StructureTypeV6(Enum):
    """Tipos de estructura de mercado v6.0 Enterprise"""
    CHOCH_BULLISH = "choch_bullish"          # Change of Character alcista
    CHOCH_BEARISH = "choch_bearish"          # Change of Character bajista
    BOS_BULLISH = "bos_bullish"              # Break of Structure alcista
    BOS_BEARISH = "bos_bearish"              # Break of Structure bajista
    RANGE_BOUND = "range_bound"              # Rango lateral
    CONSOLIDATION = "consolidation"          # Consolidación
    LIQUIDITY_GRAB = "liquidity_grab"        # Liquidity grab v6.0
    MARKET_REVERSAL = "market_reversal"      # Market reversal v6.0
    UNKNOWN = "unknown"


class FVGTypeV6(Enum):
    """Tipos de Fair Value Gap v6.0 Enterprise"""
    BULLISH_FVG = "bullish_fvg"             # FVG alcista
    BEARISH_FVG = "bearish_fvg"             # FVG bajista
    BALANCED_FVG = "balanced_fvg"           # FVG balanceado
    PREMIUM_FVG = "premium_fvg"             # FVG en premium
    DISCOUNT_FVG = "discount_fvg"           # FVG en discount
    INSTITUTIONAL_FVG = "institutional_fvg"  # FVG institucional v6.0
    RETAIL_FVG = "retail_fvg"               # FVG retail v6.0


class OrderBlockTypeV6(Enum):
    """Tipos de Order Block v6.0 Enterprise"""
    BULLISH_OB = "bullish_ob"               # Order Block alcista
    BEARISH_OB = "bearish_ob"               # Order Block bajista
    BREAKER_BLOCK = "breaker_block"         # Breaker Block
    MITIGATION_BLOCK = "mitigation_block"   # Mitigation Block
    INSTITUTIONAL_OB = "institutional_ob"    # Institutional Order Block v6.0
    LIQUIDITY_POOL = "liquidity_pool"       # Liquidity Pool v6.0


@dataclass
class MarketStructureSignalV6:
    """Señal de estructura de mercado v6.0 Enterprise"""
    structure_type: StructureTypeV6
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
    
    # Enterprise features v6.0
    ict_compliance: bool
    smart_money_alignment: bool
    liquidity_strength: float
    risk_reward_ratio: float
    session_context: str
    market_condition: str


@dataclass
class FairValueGapV6:
    """Fair Value Gap v6.0 Enterprise"""
    fvg_type: FVGTypeV6
    high_price: float
    low_price: float
    origin_candle: int
    filled_percentage: float
    is_mitigated: bool
    mitigation_candle: Optional[int]
    narrative: str
    timestamp: datetime
    
    # Enterprise features v6.0
    institutional_strength: float
    volume_profile: Dict[str, float]
    time_validity: int  # Minutes valid
    session_origin: str


@dataclass
class OrderBlockV6:
    """Order Block v6.0 Enterprise"""
    ob_type: OrderBlockTypeV6
    high_price: float
    low_price: float
    origin_candle: int
    reaction_strength: float
    is_tested: bool
    test_count: int
    narrative: str
    timestamp: datetime
    
    # Enterprise features v6.0
    institutional_confirmation: bool
    liquidity_depth: float
    smart_money_origin: bool
    time_decay_factor: float
    volume_confirmation: float


class MarketStructureAnalyzerV6:
    """
    🏗️ MARKET STRUCTURE ANALYZER v6.0 ENTERPRISE
    =============================================

    Motor profesional de análisis de estructura migrado desde v2.0:
    - Detección automática de CHoCH y BOS (migrado)
    - Análisis multi-timeframe de estructura (migrado + mejorado)
    - Fair Value Gap detection v6.0 (migrado + enterprise features)
    - Order Block identification v6.0 (migrado + enterprise features)
    - SIC Bridge integration
    - Real FundedNext MT5 data
    - Enterprise logging SLUC v2.1
    """

    def __init__(self):
        """Inicializa el Market Structure Analyzer v6.0 Enterprise"""
        
        # Enterprise logging
        self.logger = SmartTradingLogger()
        self.logger.info("🏗️ Inicializando Market Structure Analyzer v6.0 Enterprise")

        # SIC Bridge integration
        self.sic_bridge = get_sic_bridge()
        
        # Data manager para datos reales
        self.data_manager = AdvancedCandleDownloader()
        
        # 🎯 Configuración de detección (migrada desde v2.0 + ajustada)
        self.min_confidence = 60.0  # Bajado de 65.0 para detectar más eventos
        self.structure_lookback = 50  # Velas hacia atrás para análisis
        self.swing_window = 5         # Ventana para swing points
        self.fvg_min_gap = 0.0005    # Gap mínimo para FVG (5 pips)
        self.ob_reaction_threshold = 0.001  # Threshold para Order Block

        # 📊 Pesos de scoring (migrados desde v2.0)
        self.structure_weight = 0.40
        self.momentum_weight = 0.25
        self.volume_weight = 0.20
        self.confluence_weight = 0.15

        # 📈 Estado interno (migrado desde v2.0)
        self.detected_fvgs: List[FairValueGapV6] = []
        self.detected_order_blocks: List[OrderBlockV6] = []
        self.structure_history: List[Dict] = []
        self.current_trend = TradingDirection.NEUTRAL

        # Enterprise features v6.0
        self.session_context = self._detect_session_context()
        self.market_condition = "normal"
        self.ict_compliance_mode = True
        
        # Performance monitoring
        self.analysis_count = 0
        self.avg_analysis_time = 0.0
        
        self.logger.info("✅ Market Structure Analyzer v6.0 Enterprise inicializado")
        self.logger.info(f"   SIC Bridge: {self.sic_bridge.active_system}")
        self.logger.info(f"   Configuración: confidence={self.min_confidence}%, lookback={self.structure_lookback}")

    def _detect_session_context(self) -> str:
        """Detecta contexto de sesión v6.0"""
        try:
            current_hour = datetime.now().hour
            
            # London session
            if 8 <= current_hour <= 16:
                return "London"
            # New York session
            elif 13 <= current_hour <= 21:
                return "New York"
            # Asian session
            elif 22 <= current_hour or current_hour <= 7:
                return "Asian"
            else:
                return "Overlap"
        except Exception:
            return "Unknown"

    def analyze_market_structure(self,
                                candles_m15: pd.DataFrame,
                                candles_m5: Optional[pd.DataFrame] = None,
                                candles_h1: Optional[pd.DataFrame] = None,
                                current_price: float = 0.0,
                                symbol: str = "EURUSD") -> Optional[MarketStructureSignalV6]:
        """
        🏗️ ANÁLISIS COMPLETO DE ESTRUCTURA v6.0 ENTERPRISE
        (Migrado y mejorado desde Market Structure v2.0)

        Args:
            candles_m15: Datos M15 para análisis principal
            candles_m5: Datos M5 para confirmación detallada
            candles_h1: Datos H1 para contexto superior
            current_price: Precio actual
            symbol: Símbolo para contexto

        Returns:
            MarketStructureSignalV6 si se detecta cambio estructural
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"🏗️ Iniciando análisis Market Structure v6.0 - {symbol}")

            if candles_m15 is None or candles_m15.empty:
                self.logger.warning("❌ Sin datos M15 para análisis estructura")
                return None

            # 1. 🎯 DETECTAR SWING POINTS (migrado desde v2.0)
            swing_highs, swing_lows = self._detect_swing_points(candles_m15)
            if len(swing_highs) < 2 or len(swing_lows) < 2:
                self.logger.debug("🎯 Insuficientes swing points para análisis")
                return None

            # 2. 🔍 DETECTAR CAMBIOS ESTRUCTURALES (migrado desde v2.0)
            structure_score, structure_type, break_level, target_level = self._detect_structure_change(
                candles_m15, swing_highs, swing_lows, current_price
            )

            if structure_score < 0.5:
                self.logger.debug(f"🔍 Sin cambio estructural significativo: score={structure_score:.2f}")
                return None

            # 3. 💨 ANALIZAR MOMENTUM (migrado desde v2.0)
            momentum_score = self._analyze_momentum(candles_m15, structure_type)

            # 4. 📊 ANALIZAR VOLUMEN (migrado desde v2.0)
            volume_score = self._analyze_volume_structure(candles_m15)

            # 5. 🔗 ANALIZAR CONFLUENCIAS (migrado desde v2.0 + v6.0 enhancements)
            confluence_score = self._analyze_confluence_v6(candles_m15, candles_h1, structure_type)

            # 6. 🧮 CALCULAR CONFIANZA TOTAL (migrado desde v2.0)
            total_confidence = (
                structure_score * self.structure_weight +
                momentum_score * self.momentum_weight +
                volume_score * self.volume_weight +
                confluence_score * self.confluence_weight
            ) * 100

            # 7. ✅ VALIDAR THRESHOLD (migrado desde v2.0)
            if total_confidence < self.min_confidence:
                self.logger.debug(f"🏗️ Confianza insuficiente: {total_confidence:.1f}% < {self.min_confidence}%")
                return None

            # 8. 💎 DETECTAR FVGs v6.0 (migrado + enhanced)
            fvg_present = self._detect_fair_value_gaps_v6(candles_m15)

            # 9. 📦 DETECTAR ORDER BLOCKS v6.0 (migrado + enhanced)
            ob_present = self._detect_order_blocks_v6(candles_m15)

            # 10. 🎯 ENTERPRISE FEATURES v6.0
            ict_compliance = self._validate_ict_compliance(structure_type, total_confidence)
            smart_money_alignment = self._detect_smart_money_alignment(candles_h1, structure_type)
            liquidity_strength = self._calculate_liquidity_strength(candles_m15)
            risk_reward = self._calculate_risk_reward_ratio(break_level, target_level, current_price)

            # 11. 🎯 GENERAR SEÑAL v6.0 (migrado + enhanced)
            signal = self._generate_structure_signal_v6(
                structure_type=structure_type,
                confidence=total_confidence,
                break_level=break_level,
                target_level=target_level,
                confluence_score=confluence_score,
                fvg_present=fvg_present,
                ob_present=ob_present,
                candles=candles_m15,
                ict_compliance=ict_compliance,
                smart_money_alignment=smart_money_alignment,
                liquidity_strength=liquidity_strength,
                risk_reward_ratio=risk_reward
            )

            # 12. 📝 ACTUALIZAR ESTADO (migrado desde v2.0)
            self._update_structure_state_v6(structure_type, signal)

            # 13. 📊 PERFORMANCE TRACKING v6.0
            analysis_time = time.time() - start_time
            self._update_performance_stats(analysis_time)

            self.logger.info(f"🎯 Estructura v6.0 detectada: {signal.structure_type.value}")
            self.logger.info(f"   Confianza: {signal.confidence:.1f}%")
            self.logger.info(f"   ICT Compliance: {signal.ict_compliance}")
            self.logger.info(f"   Smart Money: {signal.smart_money_alignment}")
            self.logger.info(f"   Tiempo análisis: {analysis_time:.4f}s")
            
            return signal

        except Exception as e:
            self.logger.error(f"❌ Error en análisis Market Structure v6.0: {e}")
            return None

    def _detect_swing_points(self, candles: pd.DataFrame) -> Tuple[List[Dict], List[Dict]]:
        """🎯 Detecta swing highs y lows (migrado desde v2.0)"""
        try:
            swing_highs = []
            swing_lows = []

            if len(candles) < self.swing_window * 2 + 1:
                return swing_highs, swing_lows

            # Detectar swing highs (lógica migrada desde v2.0)
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

            # Detectar swing lows (lógica migrada desde v2.0)
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

            self.logger.debug(f"🎯 Swing points v6.0: {len(swing_highs)} highs, {len(swing_lows)} lows")
            return swing_highs, swing_lows

        except Exception as e:
            self.logger.error(f"❌ Error detectando swing points v6.0: {e}")
            return [], []

    def _detect_structure_change(self, candles: pd.DataFrame, swing_highs: List[Dict], swing_lows: List[Dict], current_price: float) -> Tuple[float, StructureTypeV6, float, float]:
        """🔍 Detecta cambios estructurales CHoCH/BOS (migrado desde v2.0 + enhanced)"""
        try:
            if len(swing_highs) < 2 or len(swing_lows) < 2:
                return 0.0, StructureTypeV6.UNKNOWN, 0.0, 0.0

            # Obtener últimos swing points (lógica migrada desde v2.0)
            last_high = swing_highs[-1]
            prev_high = swing_highs[-2] if len(swing_highs) > 1 else swing_highs[-1]
            last_low = swing_lows[-1]
            prev_low = swing_lows[-2] if len(swing_lows) > 1 else swing_lows[-1]

            structure_score = 0.0
            structure_type = StructureTypeV6.UNKNOWN
            break_level = 0.0
            target_level = 0.0

            # DETECTAR BOS ALCISTA (lógica migrada desde v2.0)
            if current_price > last_high['price'] and last_high['price'] > prev_high['price']:
                structure_score = 0.8
                structure_type = StructureTypeV6.BOS_BULLISH
                break_level = last_high['price']
                target_level = break_level * 1.002  # Target 20 pips arriba
                self.logger.debug(f"🔍 BOS BULLISH v6.0 detectado @ {break_level:.5f}")

            # DETECTAR BOS BAJISTA (lógica migrada desde v2.0)
            elif current_price < last_low['price'] and last_low['price'] < prev_low['price']:
                structure_score = 0.8
                structure_type = StructureTypeV6.BOS_BEARISH
                break_level = last_low['price']
                target_level = break_level * 0.998  # Target 20 pips abajo
                self.logger.debug(f"🔍 BOS BEARISH v6.0 detectado @ {break_level:.5f}")

            # DETECTAR CHOCH ALCISTA (lógica migrada desde v2.0)
            elif (current_price > prev_low['price'] and
                  self.current_trend == TradingDirection.BEARISH and
                  last_low['price'] > prev_low['price']):
                structure_score = 0.9
                structure_type = StructureTypeV6.CHOCH_BULLISH
                break_level = prev_low['price']
                target_level = last_high['price']
                self.logger.debug(f"🔍 CHoCH BULLISH v6.0 detectado @ {break_level:.5f}")

            # DETECTAR CHOCH BAJISTA (lógica migrada desde v2.0)
            elif (current_price < prev_high['price'] and
                  self.current_trend == TradingDirection.BULLISH and
                  last_high['price'] < prev_high['price']):
                structure_score = 0.9
                structure_type = StructureTypeV6.CHOCH_BEARISH
                break_level = prev_high['price']
                target_level = last_low['price']
                self.logger.debug(f"🔍 CHoCH BEARISH v6.0 detectado @ {break_level:.5f}")

            # DETECTAR LIQUIDITY GRAB v6.0 (nuevo)
            elif self._detect_liquidity_grab(candles, swing_highs, swing_lows, current_price):
                structure_score = 0.85
                structure_type = StructureTypeV6.LIQUIDITY_GRAB
                break_level = current_price
                target_level = self._calculate_liquidity_target(candles, current_price)
                self.logger.debug(f"🔍 LIQUIDITY GRAB v6.0 detectado @ {break_level:.5f}")

            # DETECTAR RANGO (MIGRADO COMPLETO desde market_structure_v2.py)
            elif self._is_range_bound_v6(swing_highs, swing_lows):
                structure_score = 0.6
                structure_type = StructureTypeV6.RANGE_BOUND
                break_level = (last_high['price'] + last_low['price']) / 2
                target_level = break_level
                self.logger.debug(f"🔍 RANGE BOUND v6.0 detectado")

            return structure_score, structure_type, break_level, target_level

        except Exception as e:
            self.logger.error(f"❌ Error detectando cambio estructural v6.0: {e}")
            return 0.0, StructureTypeV6.UNKNOWN, 0.0, 0.0

    def _is_range_bound_v6(self, swing_highs: List[Dict], swing_lows: List[Dict]) -> bool:
        """🔍 Detecta si el mercado está en rango (MIGRADO desde market_structure_v2.py)"""
        try:
            if len(swing_highs) < 3 or len(swing_lows) < 3:
                return False

            # Verificar si los últimos 3 highs están cerca (lógica MIGRADA)
            recent_highs = [sh['price'] for sh in swing_highs[-3:]]
            high_range = max(recent_highs) - min(recent_highs)
            avg_high = sum(recent_highs) / len(recent_highs)

            # Verificar si los últimos 3 lows están cerca (lógica MIGRADA)
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

    def _analyze_momentum_v6(self, candles: pd.DataFrame, structure_type: StructureTypeV6) -> float:
        """💨 Analiza momentum para confirmación (MIGRADO desde market_structure_v2.py)"""
        try:
            if len(candles) < 20:
                return 0.5

            recent = candles.tail(10)

            # Calcular momentum básico (lógica MIGRADA)
            price_change = (recent['close'].iloc[-1] - recent['close'].iloc[0]) / recent['close'].iloc[0]
            momentum_score = 0.5

            # Analizar según tipo de estructura (adaptado a StructureTypeV6)
            if structure_type in [StructureTypeV6.BOS_BULLISH, StructureTypeV6.CHOCH_BULLISH]:
                if price_change > 0:
                    momentum_score += 0.3
                if price_change > 0.001:  # >10 pips
                    momentum_score += 0.2

            elif structure_type in [StructureTypeV6.BOS_BEARISH, StructureTypeV6.CHOCH_BEARISH]:
                if price_change < 0:
                    momentum_score += 0.3
                if price_change < -0.001:  # <-10 pips
                    momentum_score += 0.2

            return min(1.0, momentum_score)

        except Exception:
            return 0.5

    def _detect_liquidity_grab(self, candles: pd.DataFrame, swing_highs: List[Dict], swing_lows: List[Dict], current_price: float) -> bool:
        """🔍 Detecta liquidity grab v6.0 (nueva funcionalidad)"""
        try:
            if len(candles) < 10:
                return False

            recent = candles.tail(10)
            
            # Buscar sweeps de highs/lows seguidos de reversal
            for i in range(1, len(recent)):
                current_candle = recent.iloc[i]
                prev_candle = recent.iloc[i-1]
                
                # Sweep of high seguido de reversal bajista
                if (current_candle['high'] > prev_candle['high'] and
                    current_candle['close'] < current_candle['open'] and
                    (current_candle['high'] - current_candle['close']) > (current_candle['close'] - current_candle['low'])):
                    return True
                
                # Sweep of low seguido de reversal alcista
                if (current_candle['low'] < prev_candle['low'] and
                    current_candle['close'] > current_candle['open'] and
                    (current_candle['close'] - current_candle['low']) > (current_candle['high'] - current_candle['close'])):
                    return True
            
            return False

        except Exception:
            return False

    def _calculate_liquidity_target(self, candles: pd.DataFrame, current_price: float) -> float:
        """Calcula target para liquidity grab v6.0"""
        try:
            recent = candles.tail(20)
            avg_range = recent['high'].subtract(recent['low']).mean()
            
            # Target basado en rango promedio
            if current_price > recent['close'].mean():
                return current_price - (avg_range * 1.5)
            else:
                return current_price + (avg_range * 1.5)
                
        except Exception:
            return current_price

    def _is_range_bound(self, swing_highs: List[Dict], swing_lows: List[Dict]) -> bool:
        """Detecta si el mercado está en rango (migrado desde v2.0)"""
        try:
            if len(swing_highs) < 3 or len(swing_lows) < 3:
                return False

            # Verificar si los últimos 3 highs están cerca (lógica migrada)
            recent_highs = [sh['price'] for sh in swing_highs[-3:]]
            high_range = max(recent_highs) - min(recent_highs)
            avg_high = sum(recent_highs) / len(recent_highs)

            # Verificar si los últimos 3 lows están cerca (lógica migrada)
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

    def _analyze_momentum(self, candles: pd.DataFrame, structure_type: StructureTypeV6) -> float:
        """💨 Analiza momentum para confirmación (migrado desde v2.0)"""
        try:
            if len(candles) < 20:
                return 0.5

            recent = candles.tail(10)

            # Calcular momentum básico
            price_change = (recent['close'].iloc[-1] - recent['close'].iloc[0]) / recent['close'].iloc[0]
            momentum_score = 0.5

            # Analizar según tipo de estructura
            if structure_type in [StructureTypeV6.BOS_BULLISH, StructureTypeV6.CHOCH_BULLISH]:
                if price_change > 0:
                    momentum_score += 0.3
                if price_change > 0.001:  # >10 pips
                    momentum_score += 0.2

            elif structure_type in [StructureTypeV6.BOS_BEARISH, StructureTypeV6.CHOCH_BEARISH]:
                if price_change < 0:
                    momentum_score += 0.3
                if price_change < -0.001:  # <-10 pips
                    momentum_score += 0.2

            # Analizar velas de confirmación
            bullish_candles = sum(1 for _, candle in recent.iterrows()
                                if candle['close'] > candle['open'])
            bearish_candles = len(recent) - bullish_candles

            if structure_type in [StructureTypeV6.BOS_BULLISH, StructureTypeV6.CHOCH_BULLISH]:
                if bullish_candles > bearish_candles:
                    momentum_score += 0.1
            elif structure_type in [StructureTypeV6.BOS_BEARISH, StructureTypeV6.CHOCH_BEARISH]:
                if bearish_candles > bullish_candles:
                    momentum_score += 0.1

            return min(momentum_score, 1.0)

        except Exception:
            return 0.5

    def _analyze_volume_structure(self, candles: pd.DataFrame) -> float:
        """📊 Analiza volumen para confirmación estructural (migrado desde v2.0)"""
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

    def _analyze_confluence_v6(self, candles_m15: pd.DataFrame, candles_h1: Optional[pd.DataFrame], structure_type: StructureTypeV6) -> float:
        """🔗 Analiza confluencias multi-timeframe v6.0 (migrado desde v2.0 + enhanced)"""
        try:
            confluence_score = 0.5

            # Verificar alineación con timeframe superior
            if candles_h1 is not None and len(candles_h1) >= 10:
                h1_trend = self._detect_higher_tf_trend(candles_h1)

                # Bonus por alineación
                if structure_type in [StructureTypeV6.BOS_BULLISH, StructureTypeV6.CHOCH_BULLISH]:
                    if h1_trend == TradingDirection.BULLISH:
                        confluence_score += 0.3
                elif structure_type in [StructureTypeV6.BOS_BEARISH, StructureTypeV6.CHOCH_BEARISH]:
                    if h1_trend == TradingDirection.BEARISH:
                        confluence_score += 0.3

            # Verificar presencia de niveles clave
            if self.detected_fvgs:
                confluence_score += 0.1

            if self.detected_order_blocks:
                confluence_score += 0.1

            # Enterprise features v6.0
            if self.session_context in ["London", "New York"]:
                confluence_score += 0.05

            return min(confluence_score, 1.0)

        except Exception:
            return 0.5

    def _detect_higher_tf_trend(self, candles_h1: pd.DataFrame) -> TradingDirection:
        """Detecta tendencia en timeframe superior (migrado desde v2.0)"""
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

    def _detect_fair_value_gaps_v6(self, candles: pd.DataFrame) -> bool:
        """💎 Detecta Fair Value Gaps v6.0 (migrado desde v2.0 + enhanced)"""
        try:
            if len(candles) < 10:
                return False

            fvg_found = False
            recent = candles.tail(20)

            for i in range(2, len(recent)):
                candle_1 = recent.iloc[i-2]  # Candle anterior
                candle_3 = recent.iloc[i]    # Candle actual

                # Detectar FVG alcista
                if candle_1['low'] > candle_3['high']:
                    gap_size = candle_1['low'] - candle_3['high']
                    if gap_size > self.fvg_min_gap:
                        # Enterprise features v6.0
                        institutional_strength = self._calculate_institutional_strength(recent, i)
                        volume_profile = self._get_volume_profile(recent, i)
                        
                        fvg = FairValueGapV6(
                            fvg_type=FVGTypeV6.BULLISH_FVG,
                            high_price=candle_1['low'],
                            low_price=candle_3['high'],
                            origin_candle=i,
                            filled_percentage=0.0,
                            is_mitigated=False,
                            mitigation_candle=None,
                            narrative=f"Bullish FVG v6.0: gap {gap_size:.5f}",
                            timestamp=datetime.now(),
                            institutional_strength=institutional_strength,
                            volume_profile=volume_profile,
                            time_validity=60,  # 60 minutes
                            session_origin=self.session_context
                        )
                        self.detected_fvgs.append(fvg)
                        fvg_found = True
                        self.logger.debug(f"💎 Bullish FVG v6.0 detectado: {gap_size:.5f}")

                # Detectar FVG bajista
                elif candle_1['high'] < candle_3['low']:
                    gap_size = candle_3['low'] - candle_1['high']
                    if gap_size > self.fvg_min_gap:
                        # Enterprise features v6.0
                        institutional_strength = self._calculate_institutional_strength(recent, i)
                        volume_profile = self._get_volume_profile(recent, i)
                        
                        fvg = FairValueGapV6(
                            fvg_type=FVGTypeV6.BEARISH_FVG,
                            high_price=candle_3['low'],
                            low_price=candle_1['high'],
                            origin_candle=i,
                            filled_percentage=0.0,
                            is_mitigated=False,
                            mitigation_candle=None,
                            narrative=f"Bearish FVG v6.0: gap {gap_size:.5f}",
                            timestamp=datetime.now(),
                            institutional_strength=institutional_strength,
                            volume_profile=volume_profile,
                            time_validity=60,  # 60 minutes
                            session_origin=self.session_context
                        )
                        self.detected_fvgs.append(fvg)
                        fvg_found = True
                        self.logger.debug(f"💎 Bearish FVG v6.0 detectado: {gap_size:.5f}")

            # Limpiar FVGs antiguos
            self.detected_fvgs = self.detected_fvgs[-10:]  # Mantener solo últimos 10

            return fvg_found

        except Exception as e:
            self.logger.error(f"❌ Error detectando FVG v6.0: {e}")
            return False

    def _detect_order_blocks_v6(self, candles: pd.DataFrame) -> bool:
        """📦 Detecta Order Blocks v6.0 (migrado desde v2.0 + enhanced)"""
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
                        ob_type = OrderBlockTypeV6.BULLISH_OB
                        narrative = f"Bullish Order Block v6.0: reacción {reaction_score:.4f}"
                    else:  # Bearish candle
                        ob_type = OrderBlockTypeV6.BEARISH_OB
                        narrative = f"Bearish Order Block v6.0: reacción {reaction_score:.4f}"

                    # Enterprise features v6.0
                    institutional_confirmation = self._check_institutional_confirmation(recent, i)
                    liquidity_depth = self._calculate_liquidity_depth(recent, i)
                    smart_money_origin = self._detect_smart_money_origin(recent, i)

                    order_block = OrderBlockV6(
                        ob_type=ob_type,
                        high_price=candle['high'],
                        low_price=candle['low'],
                        origin_candle=i,
                        reaction_strength=reaction_score,
                        is_tested=False,
                        test_count=0,
                        narrative=narrative,
                        timestamp=datetime.now(),
                        institutional_confirmation=institutional_confirmation,
                        liquidity_depth=liquidity_depth,
                        smart_money_origin=smart_money_origin,
                        time_decay_factor=1.0,
                        volume_confirmation=self._get_volume_confirmation(recent, i)
                    )

                    self.detected_order_blocks.append(order_block)
                    ob_found = True
                    self.logger.debug(f"📦 Order Block v6.0 detectado: {ob_type.value}")

            # Limpiar Order Blocks antiguos
            self.detected_order_blocks = self.detected_order_blocks[-10:]  # Mantener solo últimos 10

            return ob_found

        except Exception as e:
            self.logger.error(f"❌ Error detectando Order Blocks v6.0: {e}")
            return False

    def _calculate_reaction_strength(self, candles: pd.DataFrame, candle_index: int) -> float:
        """Calcula fuerza de reacción desde un nivel (migrado desde v2.0)"""
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

    def _validate_ict_compliance(self, structure_type: StructureTypeV6, confidence: float) -> bool:
        """✅ Valida compliance ICT v6.0"""
        try:
            # Compliance básico
            if confidence < 75.0:
                return False
            
            # Compliance por tipo de estructura
            if structure_type in [StructureTypeV6.CHOCH_BULLISH, StructureTypeV6.CHOCH_BEARISH]:
                return confidence >= 80.0
            elif structure_type in [StructureTypeV6.BOS_BULLISH, StructureTypeV6.BOS_BEARISH]:
                return confidence >= 75.0
            elif structure_type == StructureTypeV6.LIQUIDITY_GRAB:
                return confidence >= 85.0
            
            return True
            
        except Exception:
            return False

    def _detect_smart_money_alignment(self, candles_h1: Optional[pd.DataFrame], structure_type: StructureTypeV6) -> bool:
        """🧠 Detecta alineación smart money v6.0"""
        try:
            if candles_h1 is None or len(candles_h1) < 10:
                return False
            
            # Verificar sesión activa
            if self.session_context not in ["London", "New York"]:
                return False
            
            # Verificar alineación con timeframe superior
            h1_trend = self._detect_higher_tf_trend(candles_h1)
            
            if structure_type in [StructureTypeV6.BOS_BULLISH, StructureTypeV6.CHOCH_BULLISH]:
                return h1_trend == TradingDirection.BULLISH
            elif structure_type in [StructureTypeV6.BOS_BEARISH, StructureTypeV6.CHOCH_BEARISH]:
                return h1_trend == TradingDirection.BEARISH
            
            return False
            
        except Exception:
            return False

    def _calculate_liquidity_strength(self, candles: pd.DataFrame) -> float:
        """💧 Calcula fuerza de liquidez v6.0"""
        try:
            if len(candles) < 10:
                return 0.5
            
            recent = candles.tail(10)
            
            # Calcular volatilidad reciente
            volatility = recent['high'].subtract(recent['low']).mean()
            
            # Calcular volumen promedio
            if 'tick_volume' in recent.columns:
                avg_volume = recent['tick_volume'].mean()
                volume_factor = min(avg_volume / 1000.0, 2.0)  # Cap en 2.0
            else:
                volume_factor = 1.0
            
            # Score basado en volatilidad y volumen
            liquidity_score = (volatility * 10000) * volume_factor  # Convertir a pips
            
            return min(liquidity_score / 100.0, 1.0)  # Normalizar a 0-1
            
        except Exception:
            return 0.5

    def _calculate_risk_reward_ratio(self, break_level: float, target_level: float, current_price: float) -> float:
        """⚖️ Calcula ratio riesgo/beneficio v6.0"""
        try:
            if break_level == 0 or target_level == 0 or current_price == 0:
                return 1.0
            
            # Calcular distancia al break y al target
            risk_distance = abs(current_price - break_level)
            reward_distance = abs(target_level - break_level)
            
            if risk_distance == 0:
                return 10.0  # Ratio muy favorable
            
            ratio = reward_distance / risk_distance
            return min(ratio, 10.0)  # Cap en 10:1
            
        except Exception:
            return 1.0

    def _generate_structure_signal_v6(self, **kwargs) -> MarketStructureSignalV6:
        """🎯 Genera señal de estructura completa v6.0 (migrado desde v2.0 + enhanced)"""
        try:
            structure_type = kwargs.get('structure_type', StructureTypeV6.UNKNOWN)
            confidence = kwargs.get('confidence', self.min_confidence)

            # Determinar dirección
            if structure_type in [StructureTypeV6.BOS_BULLISH, StructureTypeV6.CHOCH_BULLISH]:
                direction = TradingDirection.BULLISH
            elif structure_type in [StructureTypeV6.BOS_BEARISH, StructureTypeV6.CHOCH_BEARISH]:
                direction = TradingDirection.BEARISH
            else:
                direction = TradingDirection.NEUTRAL

            # Generar narrativa
            narrative = self._generate_structure_narrative_v6(structure_type, confidence)

            signal = MarketStructureSignalV6(
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
                order_block_present=kwargs.get('ob_present', False),
                # Enterprise features v6.0
                ict_compliance=kwargs.get('ict_compliance', False),
                smart_money_alignment=kwargs.get('smart_money_alignment', False),
                liquidity_strength=kwargs.get('liquidity_strength', 0.5),
                risk_reward_ratio=kwargs.get('risk_reward_ratio', 1.0),
                session_context=self.session_context,
                market_condition=self.market_condition
            )

            return signal

        except Exception as e:
            self.logger.error(f"❌ Error generando señal estructura v6.0: {e}")
            return MarketStructureSignalV6(
                structure_type=StructureTypeV6.UNKNOWN,
                confidence=0.0,
                direction=TradingDirection.NEUTRAL,
                break_level=0.0,
                target_level=0.0,
                narrative="Error generating signal v6.0",
                timestamp=datetime.now(),
                timeframe="M15",
                confluence_score=0.0,
                fvg_present=False,
                order_block_present=False,
                ict_compliance=False,
                smart_money_alignment=False,
                liquidity_strength=0.0,
                risk_reward_ratio=1.0,
                session_context="Unknown",
                market_condition="error"
            )

    def _generate_structure_narrative_v6(self, structure_type: StructureTypeV6, confidence: float) -> str:
        """Genera narrativa para cambio estructural v6.0 (migrado desde v2.0 + enhanced)"""
        try:
            type_descriptions = {
                StructureTypeV6.CHOCH_BULLISH: "🔄 Change of Character BULLISH v6.0 - Reversión alcista confirmada",
                StructureTypeV6.CHOCH_BEARISH: "🔄 Change of Character BEARISH v6.0 - Reversión bajista confirmada",
                StructureTypeV6.BOS_BULLISH: "📈 Break of Structure BULLISH v6.0 - Continuación alcista",
                StructureTypeV6.BOS_BEARISH: "📉 Break of Structure BEARISH v6.0 - Continuación bajista",
                StructureTypeV6.RANGE_BOUND: "↔️ Range Bound v6.0 - Mercado lateral entre niveles",
                StructureTypeV6.CONSOLIDATION: "🔄 Consolidation v6.0 - Pausa en la tendencia",
                StructureTypeV6.LIQUIDITY_GRAB: "💧 Liquidity Grab v6.0 - Smart money capturando liquidez",
                StructureTypeV6.MARKET_REVERSAL: "🔄 Market Reversal v6.0 - Reversión institutional",
                StructureTypeV6.UNKNOWN: "❓ Estructura indefinida v6.0"
            }

            base_desc = type_descriptions.get(structure_type, "Cambio estructural v6.0")

            # Añadir contexto de confianza
            if confidence > 85:
                conf_desc = "con ALTA confianza"
            elif confidence > 75:
                conf_desc = "con BUENA confianza"
            else:
                conf_desc = "con MODERADA confianza"

            narrative = f"{base_desc} {conf_desc} ({confidence:.1f}%). "

            # Añadir contexto adicional v6.0
            if self.detected_fvgs:
                narrative += "FVG v6.0 presente. "
            if self.detected_order_blocks:
                narrative += "Order Block v6.0 detectado. "
            if self.session_context in ["London", "New York"]:
                narrative += f"Sesión {self.session_context} activa. "

            return narrative.strip()

        except Exception:
            return "Market structure change detected v6.0"

    def _update_structure_state_v6(self, structure_type: StructureTypeV6, signal: MarketStructureSignalV6):
        """📝 Actualiza estado interno de estructura v6.0 (migrado desde v2.0 + enhanced)"""
        try:
            # Actualizar tendencia actual
            if structure_type in [StructureTypeV6.BOS_BULLISH, StructureTypeV6.CHOCH_BULLISH]:
                self.current_trend = TradingDirection.BULLISH
            elif structure_type in [StructureTypeV6.BOS_BEARISH, StructureTypeV6.CHOCH_BEARISH]:
                self.current_trend = TradingDirection.BEARISH
            else:
                self.current_trend = TradingDirection.NEUTRAL

            # Añadir a historial
            self.structure_history.append({
                'timestamp': datetime.now(),
                'structure_type': structure_type,
                'confidence': signal.confidence,
                'direction': signal.direction,
                'ict_compliance': signal.ict_compliance,
                'smart_money_alignment': signal.smart_money_alignment,
                'session_context': signal.session_context
            })

            # Mantener historial limitado
            self.structure_history = self.structure_history[-20:]

            self.logger.debug(f"📝 Estado v6.0 actualizado: tendencia={self.current_trend.value}")

        except Exception as e:
            self.logger.error(f"❌ Error actualizando estado v6.0: {e}")

    def _update_performance_stats(self, analysis_time: float):
        """📊 Actualiza estadísticas de performance v6.0"""
        try:
            self.analysis_count += 1
            
            # Calcular tiempo promedio
            if self.analysis_count == 1:
                self.avg_analysis_time = analysis_time
            else:
                self.avg_analysis_time = (self.avg_analysis_time * (self.analysis_count - 1) + analysis_time) / self.analysis_count
            
            self.logger.debug(f"📊 Performance v6.0: {self.analysis_count} análisis, promedio {self.avg_analysis_time:.4f}s")
            
        except Exception as e:
            self.logger.error(f"❌ Error actualizando performance v6.0: {e}")

    # =============================================================================
    # ENTERPRISE HELPER FUNCTIONS v6.0
    # =============================================================================

    def _calculate_institutional_strength(self, candles: pd.DataFrame, index: int) -> float:
        """Calcula fuerza institucional v6.0"""
        try:
            if 'tick_volume' not in candles.columns:
                return 0.5
            
            volume = candles.iloc[index]['tick_volume']
            avg_volume = candles['tick_volume'].mean()
            
            return min(volume / avg_volume, 3.0) / 3.0  # Normalizar
            
        except Exception:
            return 0.5

    def _get_volume_profile(self, candles: pd.DataFrame, index: int) -> Dict[str, float]:
        """Obtiene perfil de volumen v6.0"""
        try:
            if 'tick_volume' not in candles.columns:
                return {'high': 0.5, 'low': 0.5, 'close': 0.5}
            
            volume_data = candles['tick_volume'].iloc[max(0, index-5):index+1]
            
            return {
                'high': float(volume_data.max()),
                'low': float(volume_data.min()),
                'close': float(volume_data.iloc[-1]) if len(volume_data) > 0 else 0.5
            }
            
        except Exception:
            return {'high': 0.5, 'low': 0.5, 'close': 0.5}

    def _check_institutional_confirmation(self, candles: pd.DataFrame, index: int) -> bool:
        """Verifica confirmación institucional v6.0"""
        try:
            # Verificar sesión activa
            if self.session_context not in ["London", "New York"]:
                return False
            
            # Verificar volumen
            if 'tick_volume' in candles.columns:
                volume = candles.iloc[index]['tick_volume']
                avg_volume = candles['tick_volume'].mean()
                return volume > avg_volume * 1.5
            
            return False
            
        except Exception:
            return False

    def _calculate_liquidity_depth(self, candles: pd.DataFrame, index: int) -> float:
        """Calcula profundidad de liquidez v6.0"""
        try:
            candle = candles.iloc[index]
            candle_range = candle['high'] - candle['low']
            
            # Comparar con rango promedio
            avg_range = (candles['high'] - candles['low']).mean()
            
            if avg_range == 0:
                return 0.5
            
            return min(candle_range / avg_range, 3.0) / 3.0  # Normalizar
            
        except Exception:
            return 0.5

    def _detect_smart_money_origin(self, candles: pd.DataFrame, index: int) -> bool:
        """Detecta origen smart money v6.0"""
        try:
            # Verificar sesión y timing
            current_hour = datetime.now().hour
            
            # London open (8-10 GMT)
            if 8 <= current_hour <= 10:
                return True
            
            # New York open (13-15 GMT)
            if 13 <= current_hour <= 15:
                return True
            
            # London close (15:30-16:30 GMT)
            if current_hour == 15 or current_hour == 16:
                return True
            
            return False
            
        except Exception:
            return False

    def _get_volume_confirmation(self, candles: pd.DataFrame, index: int) -> float:
        """Obtiene confirmación de volumen v6.0"""
        try:
            if 'tick_volume' not in candles.columns:
                return 0.5
            
            current_volume = candles.iloc[index]['tick_volume']
            recent_volumes = candles['tick_volume'].iloc[max(0, index-10):index]
            
            if len(recent_volumes) == 0:
                return 0.5
            
            avg_volume = recent_volumes.mean()
            
            if avg_volume == 0:
                return 0.5
            
            ratio = current_volume / avg_volume
            return min(ratio / 2.0, 1.0)  # Normalizar
            
        except Exception:
            return 0.5

    # =============================================================================
    # API METHODS v6.0
    # =============================================================================

    def get_system_status(self) -> Dict[str, Any]:
        """Obtiene estado del sistema v6.0"""
        try:
            return {
                'system': 'Market Structure Analyzer v6.0 Enterprise',
                'version': 'v6.0.0-enterprise',
                'sic_bridge': self.sic_bridge.active_system,
                'session_context': self.session_context,
                'market_condition': self.market_condition,
                'analysis_count': self.analysis_count,
                'avg_analysis_time': self.avg_analysis_time,
                'detected_fvgs': len(self.detected_fvgs),
                'detected_order_blocks': len(self.detected_order_blocks),
                'current_trend': self.current_trend.value,
                'ict_compliance_mode': self.ict_compliance_mode
            }
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo estado v6.0: {e}")
            return {'error': str(e)}

    def get_detected_patterns(self) -> Dict[str, Any]:
        """Obtiene patrones detectados v6.0"""
        try:
            return {
                'fair_value_gaps': [
                    {
                        'type': fvg.fvg_type.value,
                        'high_price': fvg.high_price,
                        'low_price': fvg.low_price,
                        'institutional_strength': fvg.institutional_strength,
                        'session_origin': fvg.session_origin,
                        'timestamp': fvg.timestamp.isoformat()
                    }
                    for fvg in self.detected_fvgs
                ],
                'order_blocks': [
                    {
                        'type': ob.ob_type.value,
                        'high_price': ob.high_price,
                        'low_price': ob.low_price,
                        'reaction_strength': ob.reaction_strength,
                        'institutional_confirmation': ob.institutional_confirmation,
                        'smart_money_origin': ob.smart_money_origin,
                        'timestamp': ob.timestamp.isoformat()
                    }
                    for ob in self.detected_order_blocks
                ]
            }
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo patrones v6.0: {e}")
            return {'error': str(e)}
