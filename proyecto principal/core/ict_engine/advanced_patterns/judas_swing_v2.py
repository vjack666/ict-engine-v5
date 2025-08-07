#!/usr/bin/env python3
"""
Judas Swing Analyzer v2.0
=========================

Analizador avanzado de patrones Judas Swing con detección automática
de false breakouts, grab de liquidez y confirmación de reversión.

Características Sprint 1.7:
- Detección automática de false breakouts
- Análisis de liquidity grab patterns
- Confirmación de estructura de reversión
- Market maker manipulation detection

Autor: ICT Engine Team
Sprint: 1.7 - Advanced Patterns
Fecha: 04 Agosto 2025
"""

import pandas as pd
from sistema.sic import datetime, time, timedelta
from sistema.sic import Dict, Optional, Tuple
from sistema.sic import dataclass
from enum import Enum

# Sistema de logging SLUC v2.1
from sistema.sic import enviar_senal_log

# ICT Types
from ..ict_types import TradingDirection


class JudasSwingType(Enum):
    """Tipos de Judas Swing"""
    MORNING_REVERSAL = "morning_reversal"        # 8-9 AM reversión
    LONDON_CLOSE_JUDAS = "london_close_judas"    # 10-11 AM false break
    NY_OPEN_JUDAS = "ny_open_judas"             # 1-2 PM false break
    AFTERNOON_JUDAS = "afternoon_judas"          # 2-4 PM reversión
    UNKNOWN = "unknown"


class BreakoutType(Enum):
    """Tipos de ruptura"""
    FALSE_BREAKOUT_HIGH = "false_breakout_high"
    FALSE_BREAKOUT_LOW = "false_breakout_low"
    LIQUIDITY_GRAB_HIGH = "liquidity_grab_high"
    LIQUIDITY_GRAB_LOW = "liquidity_grab_low"
    NO_BREAKOUT = "no_breakout"


@dataclass
class JudasSwingSignal:
    """Señal Judas Swing avanzada"""
    signal_type: JudasSwingType
    breakout_type: BreakoutType
    confidence: float
    direction: TradingDirection
    false_break_price: float
    reversal_target: float
    liquidity_grabbed: bool
    session_context: str
    structure_confirmed: bool
    narrative: str
    timestamp: datetime
    risk_reward_ratio: float


class JudasSwingAnalyzer:
    """
    🎭 JUDAS SWING ANALYZER v2.0
    ============================

    Analizador profesional de patrones Judas Swing con:
    - Detección automática de false breakouts
    - Análisis de liquidity grab patterns
    - Confirmación de estructura de reversión
    - Market maker manipulation detection
    """

    def __init__(self):
        """Inicializa el analizador Judas Swing"""
        enviar_senal_log("INFO", "🎭 Inicializando Judas Swing Analyzer v2.0", __name__, "judas_swing")

        # ⏰ Configuración de sesiones críticas
        self.morning_session = (time(8, 0), time(9, 30))    # 8-9:30 AM
        self.london_close = (time(10, 0), time(11, 30))     # 10-11:30 AM
        self.ny_open = (time(13, 0), time(14, 30))          # 1-2:30 PM
        self.afternoon = (time(14, 0), time(16, 0))         # 2-4 PM

        # 🎯 Configuración de detección
        self.min_confidence = 70.0
        self.false_break_threshold = 0.0015  # 15 pips threshold
        self.liquidity_grab_threshold = 0.002  # 20 pips para grab
        self.reversal_confirmation_periods = 5  # Velas para confirmación

        # 📊 Pesos de scoring
        self.timing_weight = 0.35
        self.breakout_weight = 0.30
        self.structure_weight = 0.25
        self.volume_weight = 0.10

        # 📈 Estado interno
        self.detected_levels = []
        self.recent_breakouts = []

        enviar_senal_log("INFO", "✅ Judas Swing Analyzer v2.0 inicializado", __name__, "judas_swing")

    def analyze_judas_swing_pattern(self,
                                  candles_m5: pd.DataFrame,
                                  candles_m1: Optional[pd.DataFrame] = None,
                                  current_price: float = 0.0,
                                  market_structure: Optional[Dict] = None) -> Optional[JudasSwingSignal]:
        """
        🎭 ANÁLISIS COMPLETO JUDAS SWING v2.0

        Args:
            candles_m5: Datos M5 para análisis principal
            candles_m1: Datos M1 para confirmación detallada
            current_price: Precio actual
            market_structure: Estructura de mercado actual

        Returns:
            JudasSwingSignal si se detecta patrón válido
        """
        try:
            enviar_senal_log("INFO", "🎭 Iniciando análisis Judas Swing v2.0", __name__, "judas_swing")

            if candles_m5 is None or candles_m5.empty:
                enviar_senal_log("WARNING", "❌ Sin datos M5 para análisis Judas Swing", __name__, "judas_swing")
                return None

            # 1. ⏰ VALIDAR TIMING DE SESIÓN
            timing_score, session_type = self._validate_session_timing()
            if timing_score < 0.4:
                enviar_senal_log("DEBUG", f"⏰ Timing inadecuado para Judas: score={timing_score:.2f}", __name__, "judas_swing")
                return None

            # 2. 🔍 DETECTAR FALSE BREAKOUTS
            breakout_score, breakout_type, break_price = self._detect_false_breakout(candles_m5, candles_m1)
            if breakout_score < 0.5:
                enviar_senal_log("DEBUG", f"🔍 Sin false breakout detectado: score={breakout_score:.2f}", __name__, "judas_swing")
                return None

            # 3. 💧 ANALIZAR LIQUIDITY GRAB
            liquidity_score, liquidity_grabbed = self._analyze_liquidity_grab(candles_m5, break_price, current_price)

            # 4. 🏗️ CONFIRMAR ESTRUCTURA DE REVERSIÓN
            structure_score, reversal_direction, reversal_target = self._confirm_reversal_structure(candles_m5, breakout_type, market_structure)

            # 5. 📊 ANALIZAR VOLUMEN (si disponible)
            volume_score = self._analyze_volume_confirmation(candles_m5)

            # 6. 🧮 CALCULAR CONFIANZA TOTAL
            total_confidence = (
                timing_score * self.timing_weight +
                breakout_score * self.breakout_weight +
                structure_score * self.structure_weight +
                volume_score * self.volume_weight +
                liquidity_score * 0.1  # Bonus por liquidity grab
            ) * 100

            # 7. ✅ VALIDAR THRESHOLD
            if total_confidence < self.min_confidence:
                enviar_senal_log("DEBUG", f"🎭 Confianza insuficiente: {total_confidence:.1f}% < {self.min_confidence}%", __name__, "judas_swing")
                return None

            # 8. 📈 CALCULAR RISK/REWARD
            risk_reward = self._calculate_risk_reward(break_price, reversal_target, current_price)

            # 9. 🎯 GENERAR SEÑAL JUDAS SWING
            signal = self._generate_judas_signal(
                session_type=session_type,
                breakout_type=breakout_type,
                confidence=total_confidence,
                direction=reversal_direction,
                false_break_price=break_price,
                reversal_target=reversal_target,
                liquidity_grabbed=liquidity_grabbed,
                structure_confirmed=structure_score > 0.6,
                risk_reward=risk_reward,
                candles_m5=candles_m5
            )

            enviar_senal_log("INFO", f"🎯 Judas Swing detectado: {signal.signal_type.value} - {signal.confidence:.1f}% confianza", __name__, "judas_swing")
            return signal

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error en análisis Judas Swing: {e}", __name__, "judas_swing")
            return None

    def _validate_session_timing(self) -> Tuple[float, JudasSwingType]:
        """⏰ Valida timing de sesión para Judas Swing"""
        try:
            current_time = datetime.now().time()

            # Morning Session (8-9:30 AM)
            if self.morning_session[0] <= current_time <= self.morning_session[1]:
                score = 1.0
                session = JudasSwingType.MORNING_REVERSAL
                enviar_senal_log("DEBUG", f"⏰ Morning Judas session: {current_time}", __name__, "judas_swing")
                return score, session

            # London Close (10-11:30 AM)
            if self.london_close[0] <= current_time <= self.london_close[1]:
                score = 0.9
                session = JudasSwingType.LONDON_CLOSE_JUDAS
                enviar_senal_log("DEBUG", f"⏰ London Close Judas: {current_time}", __name__, "judas_swing")
                return score, session

            # NY Open (1-2:30 PM)
            if self.ny_open[0] <= current_time <= self.ny_open[1]:
                score = 0.85
                session = JudasSwingType.NY_OPEN_JUDAS
                enviar_senal_log("DEBUG", f"⏰ NY Open Judas: {current_time}", __name__, "judas_swing")
                return score, session

            # Afternoon (2-4 PM)
            if self.afternoon[0] <= current_time <= self.afternoon[1]:
                score = 0.7
                session = JudasSwingType.AFTERNOON_JUDAS
                enviar_senal_log("DEBUG", f"⏰ Afternoon Judas: {current_time}", __name__, "judas_swing")
                return score, session

            # Zona de tolerancia (15 min antes/después de sesiones principales)
            tolerance = timedelta(minutes=15)

            for session_times, session_type, base_score in [
                (self.morning_session, JudasSwingType.MORNING_REVERSAL, 0.6),
                (self.london_close, JudasSwingType.LONDON_CLOSE_JUDAS, 0.5),
                (self.ny_open, JudasSwingType.NY_OPEN_JUDAS, 0.5)
            ]:
                start_dt = datetime.combine(datetime.now().date(), session_times[0])
                end_dt = datetime.combine(datetime.now().date(), session_times[1])
                current_dt = datetime.combine(datetime.now().date(), current_time)

                if (start_dt - tolerance <= current_dt <= start_dt) or (end_dt <= current_dt <= end_dt + tolerance):
                    enviar_senal_log("DEBUG", f"⏰ Judas tolerance zone: {session_type.value}", __name__, "judas_swing")
                    return base_score, session_type

            # Fuera de horarios válidos
            enviar_senal_log("DEBUG", f"⏰ Fuera de sesiones Judas: {current_time}", __name__, "judas_swing")
            return 0.0, JudasSwingType.UNKNOWN

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error validando timing: {e}", __name__, "judas_swing")
            return 0.0, JudasSwingType.UNKNOWN

    def _detect_false_breakout(self, candles_m5: pd.DataFrame, candles_m1: Optional[pd.DataFrame]) -> Tuple[float, BreakoutType, float]:
        """🔍 Detecta false breakouts característicos de Judas Swing"""
        try:
            if len(candles_m5) < 20:
                return 0.0, BreakoutType.NO_BREAKOUT, 0.0

            # Analizar últimas 20 velas para detectar breakouts
            recent = candles_m5.tail(20)

            # Encontrar swing highs y lows recientes
            swing_high = recent['high'].rolling(window=5, center=True).max()
            swing_low = recent['low'].rolling(window=5, center=True).min()

            # Identificar niveles clave
            resistance_level = swing_high.max()
            support_level = swing_low.min()
            current_price = recent['close'].iloc[-1]

            breakout_score = 0.0
            breakout_type = BreakoutType.NO_BREAKOUT
            break_price = current_price

            # Detectar false breakout al alza
            if self._check_false_breakout_high(recent, resistance_level):
                breakout_score = self._score_false_breakout(recent, resistance_level, True)
                breakout_type = BreakoutType.FALSE_BREAKOUT_HIGH
                break_price = resistance_level
                enviar_senal_log("DEBUG", f"🔍 False breakout HIGH detectado @ {break_price:.5f}", __name__, "judas_swing")

            # Detectar false breakout a la baja
            elif self._check_false_breakout_low(recent, support_level):
                breakout_score = self._score_false_breakout(recent, support_level, False)
                breakout_type = BreakoutType.FALSE_BREAKOUT_LOW
                break_price = support_level
                enviar_senal_log("DEBUG", f"🔍 False breakout LOW detectado @ {break_price:.5f}", __name__, "judas_swing")

            # Confirmar con datos M1 si disponible
            if candles_m1 is not None and breakout_score > 0.5:
                m1_confirmation = self._confirm_breakout_with_m1(candles_m1, break_price, breakout_type)
                breakout_score *= m1_confirmation
                enviar_senal_log("DEBUG", f"🔍 Confirmación M1: {m1_confirmation:.2f}", __name__, "judas_swing")

            return breakout_score, breakout_type, break_price

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error detectando false breakout: {e}", __name__, "judas_swing")
            return 0.0, BreakoutType.NO_BREAKOUT, 0.0

    def _check_false_breakout_high(self, candles: pd.DataFrame, resistance: float) -> bool:
        """Verifica false breakout al alza"""
        try:
            # Buscar velas que rompan resistencia y luego reviertan
            for i in range(len(candles) - 5, len(candles)):
                if i < 0:
                    continue

                candle = candles.iloc[i]

                # Ruptura de resistencia
                if candle['high'] > resistance:
                    # Verificar reversión en siguientes velas
                    remaining = candles.iloc[i+1:]
                    if len(remaining) >= 2:
                        # Al menos 2 velas cerrando por debajo de resistencia
                        reversals = sum(1 for _, next_candle in remaining.iterrows()
                                      if next_candle['close'] < resistance)
                        if reversals >= 2:
                            return True

            return False

        except Exception:
            return False

    def _check_false_breakout_low(self, candles: pd.DataFrame, support: float) -> bool:
        """Verifica false breakout a la baja"""
        try:
            # Buscar velas que rompan soporte y luego reviertan
            for i in range(len(candles) - 5, len(candles)):
                if i < 0:
                    continue

                candle = candles.iloc[i]

                # Ruptura de soporte
                if candle['low'] < support:
                    # Verificar reversión en siguientes velas
                    remaining = candles.iloc[i+1:]
                    if len(remaining) >= 2:
                        # Al menos 2 velas cerrando por encima de soporte
                        reversals = sum(1 for _, next_candle in remaining.iterrows()
                                      if next_candle['close'] > support)
                        if reversals >= 2:
                            return True

            return False

        except Exception:
            return False

    def _score_false_breakout(self, candles: pd.DataFrame, level: float, is_high: bool) -> float:
        """Puntúa la calidad del false breakout"""
        try:
            score = 0.5  # Base score

            # Verificar magnitud de la ruptura
            if is_high:
                max_break = candles['high'].max()
                break_distance = max_break - level
            else:
                min_break = candles['low'].min()
                break_distance = level - min_break

            # Scoring basado en distancia de ruptura
            relative_break = break_distance / level if level > 0 else 0

            if 0.0005 < relative_break < 0.002:  # 5-20 pips ideal
                score += 0.3
            elif relative_break < 0.0005:  # Muy poca ruptura
                score += 0.1
            elif relative_break > 0.003:  # Demasiada ruptura
                score += 0.1
            else:
                score += 0.2

            # Verificar rapidez de reversión
            current_price = candles['close'].iloc[-1]
            if is_high:
                if current_price < level:  # Precio regresó bajo resistencia
                    score += 0.2
            else:
                if current_price > level:  # Precio regresó sobre soporte
                    score += 0.2

            return min(score, 1.0)

        except Exception:
            return 0.5

    def _confirm_breakout_with_m1(self, candles_m1: pd.DataFrame, break_price: float, breakout_type: BreakoutType) -> float:
        """Confirma breakout con datos M1"""
        try:
            if len(candles_m1) < 10:
                return 1.0  # Sin penalización si no hay datos suficientes

            recent_m1 = candles_m1.tail(15)
            confirmation = 1.0

            # Verificar comportamiento detallado en M1
            if breakout_type == BreakoutType.FALSE_BREAKOUT_HIGH:
                # Buscar rechazo claro en M1
                rejections = sum(1 for _, candle in recent_m1.iterrows()
                               if candle['high'] > break_price and candle['close'] < break_price)
                if rejections >= 3:
                    confirmation += 0.2

            elif breakout_type == BreakoutType.FALSE_BREAKOUT_LOW:
                # Buscar rechazo claro en M1
                rejections = sum(1 for _, candle in recent_m1.iterrows()
                               if candle['low'] < break_price and candle['close'] > break_price)
                if rejections >= 3:
                    confirmation += 0.2

            return min(confirmation, 1.3)  # Máximo 130%

        except Exception:
            return 1.0

    def _analyze_liquidity_grab(self, candles: pd.DataFrame, break_price: float, current_price: float) -> Tuple[float, bool]:
        """💧 Analiza si hubo grab de liquidez"""
        try:
            if break_price == 0 or current_price == 0:
                return 0.3, False

            # Calcular distancia desde el break
            distance = abs(current_price - break_price) / break_price

            # Si estamos lejos del break price, posible grab de liquidez
            if distance > self.liquidity_grab_threshold:
                liquidity_score = 0.8
                liquidity_grabbed = True
                enviar_senal_log("DEBUG", f"💧 Liquidity grab detectado: distancia={distance:.4f}", __name__, "judas_swing")
            elif distance > self.false_break_threshold:
                liquidity_score = 0.6
                liquidity_grabbed = True
                enviar_senal_log("DEBUG", f"💧 Posible liquidity grab: distancia={distance:.4f}", __name__, "judas_swing")
            else:
                liquidity_score = 0.3
                liquidity_grabbed = False

            return liquidity_score, liquidity_grabbed

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error analizando liquidity grab: {e}", __name__, "judas_swing")
            return 0.3, False

    def _confirm_reversal_structure(self, candles: pd.DataFrame, breakout_type: BreakoutType, market_structure: Optional[Dict]) -> Tuple[float, TradingDirection, float]:
        """🏗️ Confirma estructura de reversión"""
        try:
            if len(candles) < 10:
                return 0.3, TradingDirection.NEUTRAL, 0.0

            recent = candles.tail(10)
            current_price = recent['close'].iloc[-1]

            # Determinar dirección de reversión esperada
            if breakout_type in [BreakoutType.FALSE_BREAKOUT_HIGH, BreakoutType.LIQUIDITY_GRAB_HIGH]:
                expected_direction = TradingDirection.SELL
                # Target para movimiento bajista
                target = recent['low'].min() * 0.999  # 10 pips abajo del low reciente
            elif breakout_type in [BreakoutType.FALSE_BREAKOUT_LOW, BreakoutType.LIQUIDITY_GRAB_LOW]:
                expected_direction = TradingDirection.BUY
                # Target para movimiento alcista
                target = recent['high'].max() * 1.001  # 10 pips arriba del high reciente
            else:
                return 0.3, TradingDirection.NEUTRAL, current_price

            # Verificar confirmación estructural
            structure_score = 0.5

            # Analizar últimas velas para confirmación
            last_3_candles = recent.tail(3)

            if expected_direction == TradingDirection.SELL:
                # Buscar velas bajistas de confirmación
                bearish_candles = sum(1 for _, candle in last_3_candles.iterrows()
                                    if candle['close'] < candle['open'])
                if bearish_candles >= 2:
                    structure_score += 0.3
            else:
                # Buscar velas alcistas de confirmación
                bullish_candles = sum(1 for _, candle in last_3_candles.iterrows()
                                    if candle['close'] > candle['open'])
                if bullish_candles >= 2:
                    structure_score += 0.3

            # Bonus por alineación con estructura de mercado
            if market_structure:
                market_bias = market_structure.get('h4_bias', 'NEUTRAL')
                if (expected_direction == TradingDirection.SELL and market_bias == 'BEARISH') or \
                   (expected_direction == TradingDirection.BUY and market_bias == 'BULLISH'):
                    structure_score += 0.2

            final_score = min(structure_score, 1.0)
            enviar_senal_log("DEBUG", f"🏗️ Estructura reversión: {expected_direction.value} - Score: {final_score:.2f}", __name__, "judas_swing")

            return final_score, expected_direction, target

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error confirmando estructura: {e}", __name__, "judas_swing")
            return 0.3, TradingDirection.NEUTRAL, 0.0

    def _analyze_volume_confirmation(self, candles: pd.DataFrame) -> float:
        """📊 Analiza confirmación por volumen"""
        try:
            if 'tick_volume' not in candles.columns or len(candles) < 10:
                return 0.5  # Score neutro si no hay datos de volumen

            recent = candles.tail(10)
            volume_data = recent['tick_volume']

            # Calcular volumen promedio
            avg_volume = volume_data.mean()
            recent_volume = volume_data.tail(3).mean()

            # Scoring basado en volumen relativo
            if recent_volume > avg_volume * 1.5:
                return 0.8  # Alto volumen = buena confirmación
            elif recent_volume > avg_volume * 1.2:
                return 0.7
            elif recent_volume > avg_volume * 0.8:
                return 0.5
            else:
                return 0.3  # Bajo volumen = poca confirmación

        except Exception:
            return 0.5

    def _calculate_risk_reward(self, break_price: float, target: float, current_price: float) -> float:
        """📈 Calcula ratio risk/reward"""
        try:
            if break_price == 0 or target == 0 or current_price == 0:
                return 1.0

            # Risk = distancia al break price (stop loss)
            risk = abs(current_price - break_price)

            # Reward = distancia al target
            reward = abs(target - current_price)

            if risk == 0:
                return 10.0  # Prácticamente sin riesgo

            ratio = reward / risk
            return min(ratio, 10.0)  # Cap en 10:1

        except Exception:
            return 1.0

    def _generate_judas_signal(self, **kwargs) -> JudasSwingSignal:
        """🎯 Genera señal Judas Swing completa"""
        try:
            # Extraer parámetros
            session_type = kwargs.get('session_type', JudasSwingType.UNKNOWN)
            breakout_type = kwargs.get('breakout_type', BreakoutType.NO_BREAKOUT)
            confidence = kwargs.get('confidence', 70.0)
            direction = kwargs.get('direction', TradingDirection.NEUTRAL)

            # Generar narrativa
            narrative = self._generate_narrative(session_type, breakout_type, direction, confidence)

            # Contexto de sesión
            session_context = self._get_session_context(session_type)

            signal = JudasSwingSignal(
                signal_type=session_type,
                breakout_type=breakout_type,
                confidence=confidence,
                direction=direction,
                false_break_price=kwargs.get('false_break_price', 0.0),
                reversal_target=kwargs.get('reversal_target', 0.0),
                liquidity_grabbed=kwargs.get('liquidity_grabbed', False),
                session_context=session_context,
                structure_confirmed=kwargs.get('structure_confirmed', False),
                narrative=narrative,
                timestamp=datetime.now(),
                risk_reward_ratio=kwargs.get('risk_reward', 1.0)
            )

            return signal

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error generando señal Judas: {e}", __name__, "judas_swing")
            # Return minimal signal
            return JudasSwingSignal(
                signal_type=JudasSwingType.UNKNOWN,
                breakout_type=BreakoutType.NO_BREAKOUT,
                confidence=0.0,
                direction=TradingDirection.NEUTRAL,
                false_break_price=0.0,
                reversal_target=0.0,
                liquidity_grabbed=False,
                session_context="Error",
                structure_confirmed=False,
                narrative="Error generating signal",
                timestamp=datetime.now(),
                risk_reward_ratio=1.0
            )

    def _generate_narrative(self, session_type: JudasSwingType, breakout_type: BreakoutType, direction: TradingDirection, confidence: float) -> str:
        """Genera narrativa contextual"""
        try:
            # Base según sesión
            session_names = {
                JudasSwingType.MORNING_REVERSAL: "🌅 Morning Judas Swing",
                JudasSwingType.LONDON_CLOSE_JUDAS: "🇬🇧 London Close Judas",
                JudasSwingType.NY_OPEN_JUDAS: "🇺🇸 NY Open Judas",
                JudasSwingType.AFTERNOON_JUDAS: "🌆 Afternoon Judas",
                JudasSwingType.UNKNOWN: "🎭 Judas Swing"
            }

            base = session_names.get(session_type, "🎭 Judas Swing")

            # Tipo de breakout
            breakout_desc = {
                BreakoutType.FALSE_BREAKOUT_HIGH: "false breakout alcista",
                BreakoutType.FALSE_BREAKOUT_LOW: "false breakout bajista",
                BreakoutType.LIQUIDITY_GRAB_HIGH: "liquidity grab al alza",
                BreakoutType.LIQUIDITY_GRAB_LOW: "liquidity grab a la baja",
                BreakoutType.NO_BREAKOUT: "patrón de reversión"
            }.get(breakout_type, "pattern")

            # Dirección
            direction_desc = {
                TradingDirection.BUY: "📈 reversión alcista",
                TradingDirection.SELL: "📉 reversión bajista",
                TradingDirection.NEUTRAL: "⚖️ movimiento lateral"
            }.get(direction, "movimiento")

            # Nivel de confianza
            if confidence > 85:
                conf_desc = "ALTA confianza"
            elif confidence > 75:
                conf_desc = "BUENA confianza"
            else:
                conf_desc = "MODERADA confianza"

            narrative = f"{base} detectado: {breakout_desc} seguido de {direction_desc} con {conf_desc} ({confidence:.1f}%). Market makers atrapando liquidez antes de reversión."

            return narrative

        except Exception:
            return "Judas Swing pattern detected"

    def _get_session_context(self, session_type: JudasSwingType) -> str:
        """Obtiene contexto de la sesión"""
        context_map = {
            JudasSwingType.MORNING_REVERSAL: "Asian session ending, London prep",
            JudasSwingType.LONDON_CLOSE_JUDAS: "London session closing, NY overlap",
            JudasSwingType.NY_OPEN_JUDAS: "NY session opening, high volatility",
            JudasSwingType.AFTERNOON_JUDAS: "NY afternoon, institutional flows",
            JudasSwingType.UNKNOWN: "Unknown session context"
        }

        return context_map.get(session_type, "Unknown session")
