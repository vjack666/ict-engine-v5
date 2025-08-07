#!/usr/bin/env python3
"""
🏗️ MARKET STRUCTURE ANALYZER - ICT ENGINE v6.0 Enterprise SIC
=============================================================

Analizador avanzado de estructura de mercado para ICT Engine v6.0 Enterprise
que proporciona detección automática de:

📊 **Análisis de Estructura ICT:**
- Change of Character (CHoCH) detection
- Break of Structure (BOS) identification
- Fair Value Gap (FVG) analysis
- Order Block detection
- Swing point analysis

🎯 **Características v6.0 Enterprise:**
- Integración nativa con SIC v3.1 Enterprise
- Análisis multi-timeframe inteligente
- Cache predictivo de patrones estructurales
- Debug avanzado con AdvancedDebugger
- Performance optimizada para real-time

🔄 **Pipeline Completo:**
1. Obtención de datos vía AdvancedCandleDownloader
2. Detección de swing points (Higher Highs/Lower Lows)
3. Identificación de cambios estructurales
4. Análisis de confluencias multi-timeframe
5. Generación de señales estructurales

Autor: ICT Engine v6.0 Enterprise Team
Versión: v6.0.0-enterprise
Fecha: Agosto 2025
"""

# ===============================
# IMPORTS SIC v3.1 ENTERPRISE
# ===============================

import threading
import time
from typing import Dict, List, Optional, Callable, Any, Set, Tuple, Union
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum

# Imports SIC v3.1 Enterprise
try:
    from sistema.sic_v3_1.enterprise_interface import SICEnterpriseInterface
    from sistema.sic_v3_1.advanced_debug import AdvancedDebugger
    SIC_V3_1_AVAILABLE = True
except ImportError:
    SIC_V3_1_AVAILABLE = False
    # Fallback para desarrollo
    class SICEnterpriseInterface:
        def __init__(self): pass

# Sistema de logging
try:
    from sistema.sic import enviar_senal_log
except ImportError:
    def enviar_senal_log(level, message, module, category):
        print(f"[{level}] {module}.{category}: {message}")

# Componentes v6.0
try:
    from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
    from utils.mt5_data_manager import MT5DataManager
    COMPONENTS_AVAILABLE = True
except ImportError:
    COMPONENTS_AVAILABLE = False
    print("⚠️ Algunos componentes v6.0 no están disponibles, usando fallbacks")

# ===============================
# TIPOS Y ENUMS ICT
# ===============================

class StructureType(Enum):
    """🏗️ Tipos de estructura de mercado ICT"""
    CHOCH_BULLISH = "choch_bullish"          # Change of Character alcista
    CHOCH_BEARISH = "choch_bearish"          # Change of Character bajista
    BOS_BULLISH = "bos_bullish"              # Break of Structure alcista
    BOS_BEARISH = "bos_bearish"              # Break of Structure bajista
    RANGE_BOUND = "range_bound"              # Rango lateral
    CONSOLIDATION = "consolidation"          # Consolidación
    UNKNOWN = "unknown"


class FVGType(Enum):
    """📊 Tipos de Fair Value Gap"""
    BULLISH_FVG = "bullish_fvg"             # FVG alcista
    BEARISH_FVG = "bearish_fvg"             # FVG bajista
    BALANCED_FVG = "balanced_fvg"           # FVG balanceado
    PREMIUM_FVG = "premium_fvg"             # FVG en premium
    DISCOUNT_FVG = "discount_fvg"           # FVG en discount


class OrderBlockType(Enum):
    """📦 Tipos de Order Block"""
    BULLISH_OB = "bullish_ob"               # Order Block alcista
    BEARISH_OB = "bearish_ob"               # Order Block bajista
    BREAKER_BLOCK = "breaker_block"         # Breaker Block
    MITIGATION_BLOCK = "mitigation_block"   # Mitigation Block


class TradingDirection(Enum):
    """📈 Direcciones de trading"""
    BUY = "BUY"
    SELL = "SELL"
    NEUTRAL = "NEUTRAL"


# ===============================
# DATACLASSES ICT
# ===============================

@dataclass
class SwingPoint:
    """🎯 Swing point detectado"""
    index: int
    price: float
    timestamp: datetime
    point_type: str  # 'high' o 'low'
    strength: float = 0.0
    confirmed: bool = False


@dataclass 
class MarketStructureSignal:
    """🏗️ Señal de estructura de mercado"""
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
    
    # Nuevos campos v6.0
    swing_highs: List[SwingPoint] = field(default_factory=list)
    swing_lows: List[SwingPoint] = field(default_factory=list)
    sic_stats: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FairValueGap:
    """📊 Fair Value Gap detectado"""
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
    """📦 Order Block detectado"""
    ob_type: OrderBlockType
    high_price: float
    low_price: float
    origin_candle: int
    reaction_strength: float
    is_tested: bool
    test_count: int
    narrative: str
    timestamp: datetime


# ===============================
# MARKET STRUCTURE ANALYZER
# ===============================

class MarketStructureAnalyzer:
    """
    🏗️ MARKET STRUCTURE ANALYZER v6.0 ENTERPRISE
    =============================================

    Analizador profesional de estructura de mercado ICT con:
    - Detección automática de CHoCH y BOS
    - Análisis multi-timeframe inteligente
    - Fair Value Gap detection avanzada
    - Order Block identification precisa
    - Integración completa con SIC v3.1
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        🏗️ Inicializa el Market Structure Analyzer v6.0
        
        Args:
            config: Configuración avanzada del analizador
        """
        
        # Configuración v6.0
        self._config = config or {}
        self._enable_debug = self._config.get('enable_debug', True)
        self._use_multi_timeframe = self._config.get('use_multi_timeframe', True)
        self._enable_cache = self._config.get('enable_cache', True)
        
        # Configuración de detección ICT
        self.min_confidence = self._config.get('min_confidence', 70.0)
        self.structure_lookback = self._config.get('structure_lookback', 50)
        self.swing_window = self._config.get('swing_window', 5)
        self.fvg_min_gap = self._config.get('fvg_min_gap', 0.0005)  # 5 pips
        self.ob_reaction_threshold = self._config.get('ob_reaction_threshold', 0.001)
        
        # Pesos de scoring ICT
        self.structure_weight = self._config.get('structure_weight', 0.40)
        self.momentum_weight = self._config.get('momentum_weight', 0.25)
        self.volume_weight = self._config.get('volume_weight', 0.20)
        self.confluence_weight = self._config.get('confluence_weight', 0.15)
        
        # Estado interno
        self.detected_fvgs: List[FairValueGap] = []
        self.detected_order_blocks: List[OrderBlock] = []
        self.structure_history: List[MarketStructureSignal] = []
        self.current_trend = TradingDirection.NEUTRAL
        
        # Componentes v6.0
        self._downloader: Optional[AdvancedCandleDownloader] = None
        self._pandas_module = None
        self._performance_metrics = []
        
        # Threading para análisis asíncrono
        self.lock = threading.Lock()
        self._analysis_cache = {}
        
        # Inicializar componentes
        self._initialize_components()
        
        # Log de inicialización
        self._log_info("MarketStructureAnalyzer v6.0 inicializado con SIC v3.1")

    def _initialize_components(self):
        """🔧 Inicializa componentes v6.0"""
        try:
            # Configurar downloader
            if COMPONENTS_AVAILABLE:
                self._downloader = AdvancedCandleDownloader()
                self._log_info("AdvancedCandleDownloader conectado")
            else:
                self._log_warning("AdvancedCandleDownloader no disponible")
            
            # Configurar SIC v3.1 si está disponible
            if SIC_V3_1_AVAILABLE:
                self._log_info("Integración SIC v3.1 activa")
            
        except Exception as e:
            self._log_error(f"Error inicializando componentes: {e}")

    def analyze_market_structure(self,
                               symbol: str,
                               timeframe: str = "M15",
                               lookback_days: int = 7,
                               current_price: Optional[float] = None) -> Optional[MarketStructureSignal]:
        """
        🏗️ ANÁLISIS COMPLETO DE ESTRUCTURA DE MERCADO v6.0
        
        Args:
            symbol: Símbolo a analizar (ej: "EURUSD")
            timeframe: Timeframe principal (ej: "M15")
            lookback_days: Días de historia para análisis
            current_price: Precio actual (opcional)
            
        Returns:
            MarketStructureSignal si se detecta cambio estructural
        """
        try:
            start_time = time.time()
            self._log_info(f"🏗️ Iniciando análisis Market Structure: {symbol} {timeframe}")
            
            # 1. 📥 OBTENER DATOS
            candles_data = self._get_market_data(symbol, timeframe, lookback_days)
            if candles_data is None or len(candles_data) < 50:
                self._log_warning(f"Insuficientes datos para {symbol} {timeframe}")
                return None
            
            # 2. 🎯 DETECTAR SWING POINTS
            swing_highs, swing_lows = self._detect_swing_points(candles_data)
            if len(swing_highs) < 2 or len(swing_lows) < 2:
                self._log_debug("Insuficientes swing points para análisis")
                return None
            
            # 3. 🔍 DETECTAR CAMBIOS ESTRUCTURALES
            structure_result = self._detect_structure_change(
                candles_data, swing_highs, swing_lows, current_price
            )
            
            if structure_result[0] < 0.5:  # structure_score
                self._log_debug(f"Sin cambio estructural significativo: score={structure_result[0]:.2f}")
                return None
            
            structure_score, structure_type, break_level, target_level = structure_result
            
            # 4. 💨 ANALIZAR MOMENTUM
            momentum_score = self._analyze_momentum(candles_data, structure_type)
            
            # 5. 📊 ANALIZAR VOLUMEN
            volume_score = self._analyze_volume_structure(candles_data)
            
            # 6. 🔗 ANALIZAR CONFLUENCIAS MULTI-TIMEFRAME
            confluence_score = 0.5  # Default si no hay multi-timeframe
            if self._use_multi_timeframe:
                confluence_score = self._analyze_multi_timeframe_confluence(
                    symbol, timeframe, structure_type
                )
            
            # 7. 🧮 CALCULAR CONFIANZA TOTAL
            total_confidence = (
                structure_score * self.structure_weight +
                momentum_score * self.momentum_weight +
                volume_score * self.volume_weight +
                confluence_score * self.confluence_weight
            ) * 100
            
            # 8. ✅ VALIDAR THRESHOLD
            if total_confidence < self.min_confidence:
                self._log_debug(f"Confianza insuficiente: {total_confidence:.1f}% < {self.min_confidence}%")
                return None
            
            # 9. 💎 DETECTAR FVGs
            fvg_present = self._detect_fair_value_gaps(candles_data)
            
            # 10. 📦 DETECTAR ORDER BLOCKS
            ob_present = self._detect_order_blocks(candles_data)
            
            # 11. 🎯 GENERAR SEÑAL
            signal = self._generate_structure_signal(
                structure_type=structure_type,
                confidence=total_confidence,
                break_level=break_level,
                target_level=target_level,
                confluence_score=confluence_score,
                fvg_present=fvg_present,
                ob_present=ob_present,
                swing_highs=swing_highs,
                swing_lows=swing_lows,
                timeframe=timeframe,
                candles=candles_data
            )
            
            # 12. 📝 ACTUALIZAR ESTADO
            self._update_structure_state(structure_type, signal)
            
            # 13. 📊 MÉTRICAS DE PERFORMANCE
            analysis_time = time.time() - start_time
            self._performance_metrics.append({
                'symbol': symbol,
                'timeframe': timeframe,
                'analysis_time': analysis_time,
                'confidence': total_confidence,
                'timestamp': datetime.now()
            })
            
            self._log_info(f"🎯 Estructura detectada: {signal.structure_type.value} - {signal.confidence:.1f}% confianza")
            return signal
            
        except Exception as e:
            self._log_error(f"Error en análisis Market Structure: {e}")
            return None

    def _get_market_data(self, symbol: str, timeframe: str, lookback_days: int):
        """📥 Obtiene datos de mercado usando AdvancedCandleDownloader"""
        try:
            if not self._downloader:
                self._log_error("AdvancedCandleDownloader no disponible")
                return None
            
            # Calcular fechas
            end_date = datetime.now()
            start_date = end_date - timedelta(days=lookback_days)
            
            # Descargar datos
            result = self._downloader.download_candles(
                symbol=symbol,
                timeframe=timeframe,
                start_date=start_date,
                end_date=end_date,
                save_to_file=False
            )
            
            if result and result.get('success', False):
                data = result.get('data')
                if data is not None and len(data) > 0:
                    self._log_info(f"✅ Datos obtenidos: {len(data)} velas {symbol} {timeframe}")
                    return data
            
            self._log_warning(f"Sin datos para {symbol} {timeframe}")
            return None
            
        except Exception as e:
            self._log_error(f"Error obteniendo datos: {e}")
            return None

    def _detect_swing_points(self, candles) -> Tuple[List[SwingPoint], List[SwingPoint]]:
        """🎯 Detecta swing highs y swing lows"""
        try:
            swing_highs = []
            swing_lows = []
            
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
                    swing_point = SwingPoint(
                        index=i,
                        price=current_high,
                        timestamp=candles.index[i] if hasattr(candles.index[i], 'timestamp') else datetime.now(),
                        point_type='high',
                        strength=1.0,
                        confirmed=True
                    )
                    swing_highs.append(swing_point)
            
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
                    swing_point = SwingPoint(
                        index=i,
                        price=current_low,
                        timestamp=candles.index[i] if hasattr(candles.index[i], 'timestamp') else datetime.now(),
                        point_type='low',
                        strength=1.0,
                        confirmed=True
                    )
                    swing_lows.append(swing_point)
            
            self._log_debug(f"🎯 Swing points: {len(swing_highs)} highs, {len(swing_lows)} lows")
            return swing_highs, swing_lows
            
        except Exception as e:
            self._log_error(f"Error detectando swing points: {e}")
            return [], []

    def _detect_structure_change(self, candles, swing_highs: List[SwingPoint], swing_lows: List[SwingPoint], current_price: Optional[float]) -> Tuple[float, StructureType, float, float]:
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
            if last_high.price > prev_high.price:
                if last_low.price > prev_low.price:  # HH + HL = BOS alcista
                    structure_score = 0.8
                    structure_type = StructureType.BOS_BULLISH
                    break_level = prev_high.price
                    target_level = last_high.price + (last_high.price - prev_high.price)
                else:  # HH + LL = CHoCH alcista
                    structure_score = 0.7
                    structure_type = StructureType.CHOCH_BULLISH
                    break_level = last_low.price
                    target_level = last_high.price
            
            # DETECTAR BOS BAJISTA (Rompe low anterior)
            elif last_low.price < prev_low.price:
                if last_high.price < prev_high.price:  # LL + LH = BOS bajista
                    structure_score = 0.8
                    structure_type = StructureType.BOS_BEARISH
                    break_level = prev_low.price
                    target_level = last_low.price - (prev_low.price - last_low.price)
                else:  # LL + HH = CHoCH bajista
                    structure_score = 0.7
                    structure_type = StructureType.CHOCH_BEARISH
                    break_level = last_high.price
                    target_level = last_low.price
            
            # DETECTAR CONSOLIDACIÓN
            else:
                # Verificar si está en rango
                high_range = max(last_high.price, prev_high.price)
                low_range = min(last_low.price, prev_low.price)
                range_size = high_range - low_range
                
                if range_size < (high_range * 0.01):  # Rango menor al 1%
                    structure_score = 0.4
                    structure_type = StructureType.CONSOLIDATION
                    break_level = high_range
                    target_level = low_range
            
            self._log_debug(f"🔍 Estructura: {structure_type.value} - Score: {structure_score:.2f}")
            return structure_score, structure_type, break_level, target_level
            
        except Exception as e:
            self._log_error(f"Error detectando cambio estructural: {e}")
            return 0.0, StructureType.UNKNOWN, 0.0, 0.0

    def _analyze_momentum(self, candles, structure_type: StructureType) -> float:
        """💨 Analiza momentum para confirmar estructura"""
        try:
            # Calcular momentum básico usando últimas 10 velas
            recent_candles = candles.tail(10)
            if len(recent_candles) < 5:
                return 0.5
            
            # Contar velas alcistas vs bajistas
            bullish_candles = sum(1 for _, row in recent_candles.iterrows() if row['close'] > row['open'])
            bearish_candles = len(recent_candles) - bullish_candles
            
            # Calcular ratio de momentum
            momentum_ratio = bullish_candles / len(recent_candles)
            
            # Ajustar según tipo de estructura
            if structure_type in [StructureType.BOS_BULLISH, StructureType.CHOCH_BULLISH]:
                # Para estructuras alcistas, momentum alto es bueno
                momentum_score = momentum_ratio
            elif structure_type in [StructureType.BOS_BEARISH, StructureType.CHOCH_BEARISH]:
                # Para estructuras bajistas, momentum bajo es bueno
                momentum_score = 1.0 - momentum_ratio
            else:
                momentum_score = 0.5
            
            self._log_debug(f"💨 Momentum score: {momentum_score:.2f}")
            return momentum_score
            
        except Exception as e:
            self._log_error(f"Error analizando momentum: {e}")
            return 0.5

    def _analyze_volume_structure(self, candles) -> float:
        """📊 Analiza estructura de volumen"""
        try:
            # Análisis básico de volumen
            if 'volume' not in candles.columns:
                return 0.5  # Sin datos de volumen, score neutral
            
            recent_volume = candles['volume'].tail(10)
            avg_volume = recent_volume.mean()
            latest_volume = recent_volume.iloc[-1]
            
            # Score basado en volumen relativo
            volume_ratio = latest_volume / avg_volume if avg_volume > 0 else 1.0
            volume_score = min(1.0, volume_ratio / 2.0)  # Normalizar
            
            self._log_debug(f"📊 Volume score: {volume_score:.2f}")
            return volume_score
            
        except Exception as e:
            self._log_error(f"Error analizando volumen: {e}")
            return 0.5

    def _analyze_multi_timeframe_confluence(self, symbol: str, main_timeframe: str, structure_type: StructureType) -> float:
        """🔗 Analiza confluencias multi-timeframe"""
        try:
            # Para desarrollo inicial, usar score básico
            # TODO: Implementar análisis multi-timeframe completo
            
            confluence_score = 0.6  # Score moderado por defecto
            
            self._log_debug(f"🔗 Confluence score: {confluence_score:.2f}")
            return confluence_score
            
        except Exception as e:
            self._log_error(f"Error analizando confluencias: {e}")
            return 0.5

    def _detect_fair_value_gaps(self, candles) -> bool:
        """💎 Detecta Fair Value Gaps"""
        try:
            # Implementación básica de FVG detection
            fvg_found = False
            
            for i in range(2, len(candles)):
                # Verificar FVG alcista
                prev_high = candles.iloc[i-2]['high']
                current_low = candles.iloc[i]['low']
                
                if current_low > prev_high:  # Gap alcista
                    gap_size = current_low - prev_high
                    if gap_size >= self.fvg_min_gap:
                        fvg = FairValueGap(
                            fvg_type=FVGType.BULLISH_FVG,
                            high_price=current_low,
                            low_price=prev_high,
                            origin_candle=i-1,
                            filled_percentage=0.0,
                            is_mitigated=False,
                            mitigation_candle=None,
                            narrative=f"Bullish FVG: {gap_size:.5f} gap",
                            timestamp=datetime.now()
                        )
                        self.detected_fvgs.append(fvg)
                        fvg_found = True
                
                # Verificar FVG bajista
                prev_low = candles.iloc[i-2]['low']
                current_high = candles.iloc[i]['high']
                
                if current_high < prev_low:  # Gap bajista
                    gap_size = prev_low - current_high
                    if gap_size >= self.fvg_min_gap:
                        fvg = FairValueGap(
                            fvg_type=FVGType.BEARISH_FVG,
                            high_price=prev_low,
                            low_price=current_high,
                            origin_candle=i-1,
                            filled_percentage=0.0,
                            is_mitigated=False,
                            mitigation_candle=None,
                            narrative=f"Bearish FVG: {gap_size:.5f} gap",
                            timestamp=datetime.now()
                        )
                        self.detected_fvgs.append(fvg)
                        fvg_found = True
            
            # Limpiar FVGs antiguos
            self.detected_fvgs = self.detected_fvgs[-20:]
            
            if fvg_found:
                self._log_debug(f"💎 FVGs detectados: {len(self.detected_fvgs)}")
            
            return fvg_found
            
        except Exception as e:
            self._log_error(f"Error detectando FVGs: {e}")
            return False

    def _detect_order_blocks(self, candles) -> bool:
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
                    self._log_debug(f"📦 Order Block detectado: {ob_type.value}")
            
            # Limpiar Order Blocks antiguos
            self.detected_order_blocks = self.detected_order_blocks[-10:]
            
            return ob_found
            
        except Exception as e:
            self._log_error(f"Error detectando Order Blocks: {e}")
            return False

    def _calculate_reaction_strength(self, candles, candle_index: int) -> float:
        """⚡ Calcula la fuerza de reacción desde un nivel"""
        try:
            if candle_index < 2 or candle_index >= len(candles) - 2:
                return 0.0
            
            candle = candles.iloc[candle_index]
            
            # Verificar reacción en velas posteriores
            reaction_strength = 0.0
            for i in range(candle_index + 1, min(candle_index + 5, len(candles))):
                next_candle = candles.iloc[i]
                
                # Medir distancia del precio de reacción
                if candle['close'] > candle['open']:  # Bullish OB
                    distance = abs(next_candle['low'] - candle['high'])
                else:  # Bearish OB
                    distance = abs(next_candle['high'] - candle['low'])
                
                # Convertir distancia a score
                price_range = candle['high'] - candle['low']
                if price_range > 0:
                    reaction_strength += distance / price_range
            
            return reaction_strength / 4  # Normalizar
            
        except Exception as e:
            self._log_error(f"Error calculando reacción: {e}")
            return 0.0

    def _generate_structure_signal(self, **kwargs) -> MarketStructureSignal:
        """🎯 Genera señal de estructura de mercado"""
        try:
            structure_type = kwargs.get('structure_type', StructureType.UNKNOWN)
            confidence = kwargs.get('confidence', 0.0)
            break_level = kwargs.get('break_level', 0.0)
            target_level = kwargs.get('target_level', 0.0)
            confluence_score = kwargs.get('confluence_score', 0.0)
            fvg_present = kwargs.get('fvg_present', False)
            ob_present = kwargs.get('ob_present', False)
            swing_highs = kwargs.get('swing_highs', [])
            swing_lows = kwargs.get('swing_lows', [])
            timeframe = kwargs.get('timeframe', 'M15')
            
            # Determinar dirección
            if structure_type in [StructureType.BOS_BULLISH, StructureType.CHOCH_BULLISH]:
                direction = TradingDirection.BUY
            elif structure_type in [StructureType.BOS_BEARISH, StructureType.CHOCH_BEARISH]:
                direction = TradingDirection.SELL
            else:
                direction = TradingDirection.NEUTRAL
            
            # Generar narrativa
            narrative = self._generate_narrative(structure_type, confidence, fvg_present, ob_present)
            
            # Crear señal
            signal = MarketStructureSignal(
                structure_type=structure_type,
                confidence=confidence,
                direction=direction,
                break_level=break_level,
                target_level=target_level,
                narrative=narrative,
                timestamp=datetime.now(),
                timeframe=timeframe,
                confluence_score=confluence_score,
                fvg_present=fvg_present,
                order_block_present=ob_present,
                swing_highs=swing_highs,
                swing_lows=swing_lows,
                sic_stats={'version': 'v6.0', 'analyzer': 'market_structure'}
            )
            
            return signal
            
        except Exception as e:
            self._log_error(f"Error generando señal: {e}")
            raise

    def _generate_narrative(self, structure_type: StructureType, confidence: float, fvg_present: bool, ob_present: bool) -> str:
        """📖 Genera narrativa descriptiva de la estructura"""
        narratives = {
            StructureType.BOS_BULLISH: f"Break of Structure Alcista detectado con {confidence:.1f}% confianza",
            StructureType.BOS_BEARISH: f"Break of Structure Bajista detectado con {confidence:.1f}% confianza",
            StructureType.CHOCH_BULLISH: f"Change of Character Alcista detectado con {confidence:.1f}% confianza",
            StructureType.CHOCH_BEARISH: f"Change of Character Bajista detectado con {confidence:.1f}% confianza",
            StructureType.CONSOLIDATION: f"Consolidación detectada con {confidence:.1f}% confianza",
        }
        
        base_narrative = narratives.get(structure_type, f"Estructura {structure_type.value} - {confidence:.1f}% confianza")
        
        # Agregar confluencias
        confluences = []
        if fvg_present:
            confluences.append("FVG presente")
        if ob_present:
            confluences.append("Order Block detectado")
        
        if confluences:
            base_narrative += f". Confluencias: {', '.join(confluences)}"
        
        return base_narrative

    def _update_structure_state(self, structure_type: StructureType, signal: MarketStructureSignal):
        """📝 Actualiza estado interno de estructura"""
        try:
            # Actualizar tendencia actual
            if structure_type in [StructureType.BOS_BULLISH, StructureType.CHOCH_BULLISH]:
                self.current_trend = TradingDirection.BUY
            elif structure_type in [StructureType.BOS_BEARISH, StructureType.CHOCH_BEARISH]:
                self.current_trend = TradingDirection.SELL
            
            # Agregar a historia
            self.structure_history.append(signal)
            
            # Mantener solo últimas 50 señales
            self.structure_history = self.structure_history[-50:]
            
        except Exception as e:
            self._log_error(f"Error actualizando estado: {e}")

    def get_current_structure_state(self) -> Dict[str, Any]:
        """📊 Obtiene estado actual de la estructura"""
        return {
            'current_trend': self.current_trend.value,
            'detected_fvgs': len(self.detected_fvgs),
            'detected_order_blocks': len(self.detected_order_blocks),
            'structure_history_count': len(self.structure_history),
            'last_analysis': self.structure_history[-1].timestamp if self.structure_history else None
        }

    def get_performance_metrics(self) -> Dict[str, Any]:
        """📈 Obtiene métricas de performance"""
        if not self._performance_metrics:
            return {'total_analyses': 0}
        
        return {
            'total_analyses': len(self._performance_metrics),
            'avg_analysis_time': sum(m['analysis_time'] for m in self._performance_metrics) / len(self._performance_metrics),
            'avg_confidence': sum(m['confidence'] for m in self._performance_metrics) / len(self._performance_metrics),
            'recent_analyses': self._performance_metrics[-5:]
        }

    # ===============================
    # MÉTODOS DE LOGGING
    # ===============================
    
    def _log_info(self, message: str):
        """ℹ️ Log de información"""
        enviar_senal_log("INFO", f"[MarketStructureAnalyzer v6.0] {message}", __name__, "market_structure")
    
    def _log_warning(self, message: str):
        """⚠️ Log de advertencia"""
        enviar_senal_log("WARNING", f"[MarketStructureAnalyzer v6.0] {message}", __name__, "market_structure")
    
    def _log_error(self, message: str):
        """❌ Log de error"""
        enviar_senal_log("ERROR", f"[MarketStructureAnalyzer v6.0] {message}", __name__, "market_structure")
    
    def _log_debug(self, message: str):
        """🐛 Log de debug"""
        enviar_senal_log("DEBUG", f"[MarketStructureAnalyzer v6.0] {message}", __name__, "market_structure")


# ===============================
# FACTORY FUNCTIONS
# ===============================

def get_market_structure_analyzer(config: Optional[Dict[str, Any]] = None) -> MarketStructureAnalyzer:
    """
    🏭 Factory function para crear MarketStructureAnalyzer v6.0
    
    Args:
        config: Configuración opcional del analizador
        
    Returns:
        Instancia configurada de MarketStructureAnalyzer
    """
    default_config = {
        'enable_debug': True,
        'use_multi_timeframe': True,
        'enable_cache': True,
        'min_confidence': 70.0,
        'structure_lookback': 50,
        'swing_window': 5,
        'fvg_min_gap': 0.0005,
        'ob_reaction_threshold': 0.001
    }
    
    if config:
        default_config.update(config)
    
    return MarketStructureAnalyzer(config=default_config)


# ===============================
# TEST Y VALIDACIÓN
# ===============================

if __name__ == "__main__":
    print("🧪 Testing MarketStructureAnalyzer v6.0 Enterprise...")
    
    try:
        # Crear analizador con configuración de test
        test_config = {
            'enable_debug': True,
            'use_multi_timeframe': False,  # Simplificar para test
            'min_confidence': 60.0
        }
        
        analyzer = get_market_structure_analyzer(test_config)
        print("✅ MarketStructureAnalyzer creado exitosamente")
        
        # Test de análisis básico
        signal = analyzer.analyze_market_structure(
            symbol="EURUSD",
            timeframe="M15",
            lookback_days=3
        )
        
        if signal:
            print(f"✅ Señal generada: {signal.structure_type.value} - {signal.confidence:.1f}%")
        else:
            print("ℹ️ Sin señales estructurales detectadas")
        
        # Test de estado
        state = analyzer.get_current_structure_state()
        print(f"✅ Estado actual: {state}")
        
        # Test de métricas
        metrics = analyzer.get_performance_metrics()
        print(f"✅ Métricas: {metrics}")
        
        print("🎯 Test de MarketStructureAnalyzer v6.0 completado exitosamente")
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
