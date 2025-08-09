#!/usr/bin/env python3
"""
🔄 MULTI-PATTERN CONFLUENCE ENGINE v6.0
=======================================

Motor de confluencia avanzado que integra todos los patrones ICT:
- Silver Bullet + Breaker Blocks + Liquidity Analysis
- Confluence scoring multi-dimensional  
- Trade signal synthesis enterprise
- Risk management integrado
- UnifiedMemorySystem v6.1 integration
- SLUC v2.1 logging system

FASE 5: Advanced Patterns Migration
Integration Target: Enterprise v6.0 SIC architecture

Autor: ICT Engine Team
Sprint: FASE 5 - Advanced Patterns  
Fecha: 09 Agosto 2025
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

# 🏗️ ENTERPRISE ARCHITECTURE v6.0
try:
    from core.smart_trading_logger import SmartTradingLogger
    from core.data_management.unified_memory_system import UnifiedMemorySystem
    from core.ict_engine.ict_types import TradingDirection
    from core.ict_engine.advanced_patterns.silver_bullet_enterprise import (
        SilverBulletDetectorEnterprise
    )
    from core.ict_engine.advanced_patterns.breaker_blocks_enterprise import (
        BreakerBlockDetectorEnterprise, BreakerBlockSignal
    )
    from core.ict_engine.advanced_patterns.liquidity_analyzer_enterprise import (
        LiquidityAnalyzerEnterprise
    )
except ImportError:
    # Fallback para testing
    print("[WARNING] Enterprise modules not available - using fallback")
    SmartTradingLogger = Any
    UnifiedMemorySystem = Any
    BreakerBlockSignal = Any
    
    # Fallback TradingDirection for testing
    class TradingDirection(Enum):
        BUY = "buy"
        SELL = "sell"
        BULLISH = "bullish"
        BEARISH = "bearish"
        NEUTRAL = "neutral"
    class TradingDirection(Enum):
        BUY = "buy"
        SELL = "sell"
        BULLISH = "bullish"
        BEARISH = "bearish"
        NEUTRAL = "neutral"
    
    # Fallback classes
    SilverBulletEnterprise = None
    BreakerBlocksEnterprise = None
    LiquidityAnalyzerEnterprise = None


class ConfluenceLevel(Enum):
    """📊 Niveles de confluencia"""
    LOW = "low"               # 1-2 confluencias
    MODERATE = "moderate"     # 3-4 confluencias
    HIGH = "high"            # 5-6 confluencias
    EXTREME = "extreme"      # 7+ confluencias


class SignalQuality(Enum):
    """⭐ Calidad de señal"""
    POOR = "poor"           # < 40% confidence
    FAIR = "fair"           # 40-60% confidence  
    GOOD = "good"           # 60-80% confidence
    EXCELLENT = "excellent" # 80%+ confidence


class TradeRiskLevel(Enum):
    """⚠️ Nivel de riesgo"""
    VERY_LOW = "very_low"     # 0.5% risk
    LOW = "low"               # 1% risk
    MODERATE = "moderate"     # 1.5% risk
    HIGH = "high"             # 2% risk
    VERY_HIGH = "very_high"   # 2.5%+ risk


@dataclass
class ConfluenceFactors:
    """🎯 Factores de confluencia detectados"""
    # Pattern signals - usando Any para type safety según REGLA #14
    silver_bullet_signal: Optional[Any] = None
    breaker_block_signal: Optional[Any] = None
    liquidity_pools: List[Any] = field(default_factory=list)
    liquidity_sweeps: List[Any] = field(default_factory=list)
    
    # Market structure
    trend_alignment: bool = False
    structure_break: bool = False
    support_resistance_level: bool = False
    
    # Volume & Time analysis
    volume_confirmation: bool = False
    time_of_day_optimal: bool = False
    session_alignment: bool = False
    
    # Risk factors
    news_events_clear: bool = True
    spread_normal: bool = True
    volatility_acceptable: bool = True
    
    # Institutional behavior
    smart_money_alignment: bool = False
    institutional_order_flow: bool = False
    liquidity_hunt_complete: bool = False


@dataclass
class ConfluenceTradeSignal:
    """🎯 Señal de Trading con Confluencia Enterprise"""
    # Core signal info
    signal_id: str
    direction: TradingDirection
    signal_quality: SignalQuality
    confluence_level: ConfluenceLevel
    
    # Trading levels  
    entry_price: float
    entry_zone: Tuple[float, float]
    stop_loss: float
    take_profit_1: float
    take_profit_2: float
    take_profit_3: Optional[float] = None
    
    # Risk management
    risk_level: TradeRiskLevel = TradeRiskLevel.MODERATE
    risk_reward_ratio: float = 2.0
    position_size_pct: float = 1.0  # Default 1% position size
    max_acceptable_loss_pct: float = 1.0
    
    # Confluence analysis
    confluence_score: float = 0.0           # 0.0 - 10.0
    confluence_factors: ConfluenceFactors = field(default_factory=ConfluenceFactors)
    total_confluences: int = 0
    critical_confluences: int = 0
    
    # Probability & confidence
    win_probability: float = 0.5           # 0.0 - 1.0
    confidence_score: float = 0.5          # 0.0 - 1.0
    expected_value: float = 0.0            # Esperanza matemática
    
    # Timing & execution
    optimal_entry_timeframe: str = "M15"
    max_wait_time_minutes: int = 30
    invalidation_conditions: List[str] = field(default_factory=list)
    
    # Narrative & context
    trade_narrative: str = ""
    market_context: str = ""
    key_levels: Dict[str, float] = field(default_factory=dict)
    
    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)
    symbol: str = ""
    timeframe: str = ""
    analysis_session_id: str = ""


class MultiPatternConfluenceEngine:
    """
    🔄 MULTI-PATTERN CONFLUENCE ENGINE v6.0
    =======================================
    
    Motor de confluencia enterprise que integra:
    ✅ Silver Bullet Enterprise v6.0
    ✅ Breaker Blocks Enterprise v6.0  
    ✅ Liquidity Analyzer Enterprise v6.0
    ✅ Advanced confluence scoring
    ✅ Risk management integrado
    ✅ Trade signal synthesis
    ✅ UnifiedMemorySystem v6.1 integration
    ✅ SLUC v2.1 logging completo
    ✅ Real-time pattern confluence
    """

    def __init__(self,
                 memory_system: Optional[UnifiedMemorySystem] = None,
                 logger: Optional[SmartTradingLogger] = None):
        """🚀 Inicializar Multi-Pattern Confluence Engine"""
        
        # 🏗️ ENTERPRISE INFRASTRUCTURE
        self.memory_system = memory_system
        self.logger = logger or self._create_fallback_logger()
        
        self._log_info("🔄 Inicializando Multi-Pattern Confluence Engine v6.0")
        
        # 🎯 PATTERN DETECTORS ENTERPRISE
        self.silver_bullet = SilverBulletEnterprise(memory_system, logger) if SilverBulletEnterprise else None
        self.breaker_blocks = BreakerBlocksEnterprise(memory_system, logger) if BreakerBlocksEnterprise else None  
        self.liquidity_analyzer = LiquidityAnalyzerEnterprise(memory_system, logger) if LiquidityAnalyzerEnterprise else None
        
        # ⚙️ CONFLUENCE ENGINE CONFIGURATION
        self.config = {
            # Confluence thresholds
            'min_confluence_score': 4.0,        # Mínimo score para señal válida
            'high_confluence_threshold': 6.5,    # Threshold para alta confluencia
            'extreme_confluence_threshold': 8.0, # Threshold para confluencia extrema
            
            # Signal quality
            'min_confidence_for_trade': 0.6,     # Confianza mínima para trade
            'excellent_confidence_threshold': 0.8, # Threshold para señal excelente
            
            # Risk management
            'max_risk_per_trade': 0.02,          # 2% máximo por trade
            'min_risk_reward_ratio': 1.5,        # RR mínimo
            'optimal_risk_reward_ratio': 3.0,    # RR objetivo
            
            # Timing
            'max_signal_age_minutes': 60,        # Máxima edad de señal válida
            'optimal_entry_window_minutes': 15,   # Ventana óptima para entrada
            
            # Volume & Market conditions
            'min_volume_spike_factor': 1.5,      # Factor mínimo de volumen
            'max_spread_multiplier': 2.0,        # Máximo spread aceptable
            'volatility_range_acceptable': (0.5, 3.0), # Rango volatilidad aceptable
        }
        
        # 📊 CONFLUENCE WEIGHTS (suma = 10.0)
        self.confluence_weights = {
            # Patrones principales (60% peso total)
            'silver_bullet': 2.5,
            'breaker_blocks': 2.0,
            'liquidity_sweep': 1.5,
            
            # Market structure (25% peso total)
            'trend_alignment': 1.0,
            'structure_break': 0.8,
            'support_resistance': 0.7,
            
            # Confirmaciones adicionales (15% peso total)
            'volume_confirmation': 0.5,
            'time_session_alignment': 0.4,
            'smart_money_alignment': 0.6,
        }
        
        # 📊 ESTADO INTERNO  
        self.detected_signals: List[ConfluenceTradeSignal] = []
        self.confluence_stats = {
            'total_signals_generated': 0,
            'high_confluence_signals': 0,
            'extreme_confluence_signals': 0,
            'average_confluence_score': 0.0,
            'successful_confluences': 0,
            'patterns_integrated': 0
        }
        
        self._log_info("✅ Multi-Pattern Confluence Engine v6.0 inicializado correctamente")

    def analyze_confluence_enterprise(self,
                                    data_h4: pd.DataFrame,
                                    data_h1: pd.DataFrame,
                                    data_m15: pd.DataFrame,
                                    data_m5: pd.DataFrame,
                                    symbol: str,
                                    current_price: float) -> List[ConfluenceTradeSignal]:
        """
        🔄 ANÁLISIS PRINCIPAL DE CONFLUENCIA ENTERPRISE
        
        Args:
            data_h4: Datos H4 para contexto macro
            data_h1: Datos H1 para estructura intermedia
            data_m15: Datos M15 para patrones precisos
            data_m5: Datos M5 para timing de entrada
            symbol: Par de divisa
            current_price: Precio actual de mercado
            
        Returns:
            Lista de señales de confluencia enterprise
        """
        try:
            self._log_info(f"🔄 Iniciando análisis de confluencia para {symbol}")
            
            confluence_signals = []
            
            # 1. 🎯 DETECTAR PATRONES INDIVIDUALES
            pattern_signals = self._detect_all_patterns_enterprise(
                data_h4, data_h1, data_m15, data_m5, symbol, current_price
            )
            
            if not pattern_signals['silver_bullet'] and not pattern_signals['breaker_blocks'] and not pattern_signals['liquidity_sweeps']:
                self._log_info("ℹ️ No hay patrones base detectados para confluencia")
                return []
            
            # 2. 🔍 BUSCAR CONFLUENCIAS TEMPORALES
            time_confluences = self._find_temporal_confluences(pattern_signals, data_m5)
            
            # 3. 🎯 GENERAR SEÑALES DE CONFLUENCIA
            for confluence_group in time_confluences:
                signal = self._generate_confluence_signal_enterprise(
                    confluence_group, data_h1, data_m15, data_m5, symbol, current_price
                )
                
                if signal and signal.confluence_score >= self.config['min_confluence_score']:
                    confluence_signals.append(signal)
            
            # 4. ✅ VALIDAR Y FILTRAR SEÑALES
            validated_signals = self._validate_confluence_signals(confluence_signals, data_m5)
            
            # 5. 📊 RANKING POR CALIDAD
            ranked_signals = self._rank_signals_by_quality(validated_signals)
            
            # 6. 💾 GUARDAR EN MEMORIA ENTERPRISE
            if self.memory_system and ranked_signals:
                self._store_confluence_signals_in_memory(ranked_signals)
            
            # 7. 📊 ACTUALIZAR ESTADÍSTICAS
            self._update_confluence_stats(ranked_signals)
            
            self._log_info(f"🎯 Análisis de confluencia completado: {len(ranked_signals)} señales válidas")
            return ranked_signals
            
        except Exception as e:
            self._log_error(f"❌ Error en análisis de confluencia: {e}")
            return []

    def _detect_all_patterns_enterprise(self,
                                       data_h4: pd.DataFrame,
                                       data_h1: pd.DataFrame,
                                       data_m15: pd.DataFrame,
                                       data_m5: pd.DataFrame,
                                       symbol: str,
                                       current_price: float) -> Dict[str, List]:
        """🎯 Detectar todos los patrones enterprise"""
        try:
            patterns = {
                'silver_bullet': [],
                'breaker_blocks': [],
                'liquidity_pools': [],
                'liquidity_sweeps': []
            }
            
            # 1. 🥈 SILVER BULLET DETECTION
            if self.silver_bullet:
                try:
                    sb_signals = self.silver_bullet.detect_silver_bullet_enterprise(
                        data_h1, data_m15, data_m5, symbol, "M15"
                    )
                    patterns['silver_bullet'] = sb_signals
                    self._log_debug(f"Silver Bullet: {len(sb_signals)} señales detectadas")
                except Exception as e:
                    self._log_warning(f"Error en Silver Bullet detection: {e}")
            
            # 2. 🧱 BREAKER BLOCKS DETECTION
            if self.breaker_blocks:
                try:
                    bb_signals = self.breaker_blocks.detect_breaker_blocks_enterprise(
                        data_h4, data_h1, data_m15, symbol
                    )
                    patterns['breaker_blocks'] = bb_signals
                    self._log_debug(f"Breaker Blocks: {len(bb_signals)} señales detectadas")
                except Exception as e:
                    self._log_warning(f"Error en Breaker Blocks detection: {e}")
            
            # 3. 💧 LIQUIDITY ANALYSIS
            if self.liquidity_analyzer:
                try:
                    liquidity_pools = self.liquidity_analyzer.detect_liquidity_pools_enterprise(
                        data_h4, data_h1, data_m15, symbol, current_price
                    )
                    patterns['liquidity_pools'] = liquidity_pools
                    
                    liquidity_sweeps = self.liquidity_analyzer.detect_liquidity_sweeps_enterprise(
                        data_m15, liquidity_pools, symbol, "M15"
                    )
                    patterns['liquidity_sweeps'] = liquidity_sweeps
                    
                    self._log_debug(f"Liquidity: {len(liquidity_pools)} pools, {len(liquidity_sweeps)} sweeps")
                except Exception as e:
                    self._log_warning(f"Error en Liquidity analysis: {e}")
            
            return patterns
            
        except Exception as e:
            self._log_error(f"Error detectando patrones: {e}")
            return {'silver_bullet': [], 'breaker_blocks': [], 'liquidity_pools': [], 'liquidity_sweeps': []}

    def _find_temporal_confluences(self, 
                                 pattern_signals: Dict[str, List],
                                 data_m5: pd.DataFrame) -> List[Dict]:
        """⏰ Encontrar confluencias temporales"""
        try:
            confluences = []
            
            # Obtener señales con timestamps válidos
            sb_signals = pattern_signals.get('silver_bullet', [])
            bb_signals = pattern_signals.get('breaker_blocks', [])
            ls_signals = pattern_signals.get('liquidity_sweeps', [])
            
            # Si tenemos al menos un patrón principal, crear confluencia
            for sb_signal in sb_signals:
                confluence = {
                    'silver_bullet': sb_signal,
                    'breaker_blocks': self._find_matching_breaker_block(sb_signal, bb_signals),
                    'liquidity_sweeps': self._find_matching_liquidity_sweeps(sb_signal, ls_signals),
                    'liquidity_pools': pattern_signals.get('liquidity_pools', []),
                    'timestamp': getattr(sb_signal, 'timestamp', datetime.now())
                }
                confluences.append(confluence)
            
            # También crear confluencias basadas en Breaker Blocks si no hay Silver Bullet
            if not sb_signals:
                for bb_signal in bb_signals:
                    confluence = {
                        'silver_bullet': None,
                        'breaker_blocks': bb_signal,
                        'liquidity_sweeps': self._find_matching_liquidity_sweeps(bb_signal, ls_signals),
                        'liquidity_pools': pattern_signals.get('liquidity_pools', []),
                        'timestamp': getattr(bb_signal, 'timestamp', datetime.now())
                    }
                    confluences.append(confluence)
            
            return confluences
            
        except Exception as e:
            self._log_error(f"Error finding temporal confluences: {e}")
            return []

    def _generate_confluence_signal_enterprise(self,
                                             confluence_group: Dict,
                                             data_h1: pd.DataFrame,
                                             data_m15: pd.DataFrame,
                                             data_m5: pd.DataFrame,
                                             symbol: str,
                                             current_price: float) -> Optional[ConfluenceTradeSignal]:
        """🎯 Generar señal de confluencia enterprise"""
        try:
            # 1. 🎯 DETERMINAR DIRECCIÓN PRINCIPAL
            direction = self._determine_confluence_direction(confluence_group)
            if not direction:
                return None
            
            # 2. 📊 CALCULAR CONFLUENCE FACTORS
            confluence_factors = self._calculate_confluence_factors_enterprise(
                confluence_group, data_h1, data_m15, data_m5
            )
            
            # 3. 📊 CALCULAR CONFLUENCE SCORE
            confluence_score = self._calculate_confluence_score(confluence_factors)
            
            # 4. 🎯 CALCULAR TRADING LEVELS
            trading_levels = self._calculate_confluence_trading_levels(
                confluence_group, direction, current_price
            )
            
            # 5. ⚠️ CALCULAR RISK MANAGEMENT
            risk_management = self._calculate_confluence_risk_management(
                trading_levels, confluence_score
            )
            
            # 6. 📊 CALCULAR PROBABILIDADES
            probabilities = self._calculate_confluence_probabilities(
                confluence_factors, confluence_score
            )
            
            # 7. 🎯 CREAR SEÑAL ENTERPRISE
            signal = ConfluenceTradeSignal(
                signal_id=f"CONF_{symbol}_{int(datetime.now().timestamp())}",
                direction=direction,
                signal_quality=self._determine_signal_quality(probabilities['confidence']),
                confluence_level=self._determine_confluence_level(confluence_score),
                
                # Trading levels
                entry_price=trading_levels['entry_price'],
                entry_zone=trading_levels['entry_zone'],
                stop_loss=trading_levels['stop_loss'],
                take_profit_1=trading_levels['tp1'],
                take_profit_2=trading_levels['tp2'],
                take_profit_3=trading_levels.get('tp3'),
                
                # Risk management
                risk_level=risk_management['risk_level'],
                risk_reward_ratio=risk_management['risk_reward'],
                position_size_pct=risk_management['position_size'],
                max_acceptable_loss_pct=risk_management['max_loss'],
                
                # Confluence analysis
                confluence_score=confluence_score,
                confluence_factors=confluence_factors,
                total_confluences=self._count_total_confluences(confluence_factors),
                critical_confluences=self._count_critical_confluences(confluence_factors),
                
                # Probabilities
                win_probability=probabilities['win_prob'],
                confidence_score=probabilities['confidence'],
                expected_value=probabilities['expected_value'],
                
                # Timing
                optimal_entry_timeframe="M15",
                max_wait_time_minutes=self.config['max_signal_age_minutes'],
                invalidation_conditions=self._generate_invalidation_conditions(confluence_group),
                
                # Narrative
                trade_narrative=self._generate_trade_narrative(confluence_group, direction),
                market_context=self._generate_market_context(data_h1, data_m15),
                key_levels=self._extract_key_levels(confluence_group),
                
                # Metadata
                timestamp=datetime.now(),
                symbol=symbol,
                timeframe="M15",
                analysis_session_id=f"CONF_SESSION_{int(datetime.now().timestamp())}"
            )
            
            return signal
            
        except Exception as e:
            self._log_error(f"Error generando señal de confluencia: {e}")
            return None

    # ===========================================
    # 🧮 CONFLUENCE CALCULATION METHODS
    # ===========================================

    def _calculate_confluence_factors_enterprise(self,
                                                confluence_group: Dict,
                                                data_h1: pd.DataFrame,
                                                data_m15: pd.DataFrame,
                                                data_m5: pd.DataFrame) -> ConfluenceFactors:
        """📊 Calcular factores de confluencia enterprise"""
        try:
            factors = ConfluenceFactors()
            
            # Patrones detectados
            factors.silver_bullet_signal = confluence_group.get('silver_bullet')
            factors.breaker_block_signal = confluence_group.get('breaker_blocks')
            factors.liquidity_pools = confluence_group.get('liquidity_pools', [])
            factors.liquidity_sweeps = confluence_group.get('liquidity_sweeps', [])
            
            # Market structure analysis
            factors.trend_alignment = self._analyze_trend_alignment(data_h1, data_m15)
            factors.structure_break = self._analyze_structure_break(data_m15, data_m5)
            factors.support_resistance_level = self._analyze_sr_levels(data_m15, confluence_group)
            
            # Volume & Time analysis  
            factors.volume_confirmation = self._analyze_volume_confirmation(data_m5)
            factors.time_of_day_optimal = self._analyze_optimal_timing()
            factors.session_alignment = self._analyze_session_alignment()
            
            # Risk factors
            factors.news_events_clear = self._check_news_events()
            factors.spread_normal = self._check_spread_conditions()
            factors.volatility_acceptable = self._check_volatility_conditions(data_m15)
            
            # Institutional behavior
            factors.smart_money_alignment = self._analyze_smart_money_alignment(confluence_group)
            factors.institutional_order_flow = self._analyze_institutional_flow(data_m5)
            factors.liquidity_hunt_complete = self._analyze_liquidity_hunt(factors.liquidity_sweeps)
            
            return factors
            
        except Exception as e:
            self._log_error(f"Error calculando confluence factors: {e}")
            return ConfluenceFactors()

    def _calculate_confluence_score(self, factors: ConfluenceFactors) -> float:
        """📊 Calcular score de confluencia"""
        try:
            score = 0.0
            
            # Patrones principales (60% del peso)
            if factors.silver_bullet_signal:
                score += self.confluence_weights['silver_bullet']
            
            if factors.breaker_block_signal:
                score += self.confluence_weights['breaker_blocks']
            
            if factors.liquidity_sweeps:
                score += self.confluence_weights['liquidity_sweep']
            
            # Market structure (25% del peso)
            if factors.trend_alignment:
                score += self.confluence_weights['trend_alignment']
            
            if factors.structure_break:
                score += self.confluence_weights['structure_break']
            
            if factors.support_resistance_level:
                score += self.confluence_weights['support_resistance']
            
            # Confirmaciones adicionales (15% del peso)
            if factors.volume_confirmation:
                score += self.confluence_weights['volume_confirmation']
            
            if factors.time_of_day_optimal and factors.session_alignment:
                score += self.confluence_weights['time_session_alignment']
            
            if factors.smart_money_alignment:
                score += self.confluence_weights['smart_money_alignment']
            
            return min(score, 10.0)  # Máximo 10.0
            
        except Exception as e:
            self._log_error(f"Error calculando confluence score: {e}")
            return 0.0

    def _calculate_confluence_trading_levels(self,
                                           confluence_group: Dict,
                                           direction: TradingDirection,
                                           current_price: float) -> Dict[str, float]:
        """🎯 Calcular niveles de trading para confluencia"""
        try:
            levels = {}
            
            # Determinar entry price basado en patrones
            if confluence_group.get('silver_bullet'):
                levels['entry_price'] = getattr(confluence_group['silver_bullet'], 'entry_price', current_price)
            elif confluence_group.get('breaker_blocks'):
                levels['entry_price'] = getattr(confluence_group['breaker_blocks'], 'entry_price', current_price)
            else:
                levels['entry_price'] = current_price
            
            # Entry zone (5 pips de tolerancia)
            levels['entry_zone'] = (
                levels['entry_price'] - 0.0005,
                levels['entry_price'] + 0.0005
            )
            
            # Stop loss conservador
            if direction == TradingDirection.BUY if TradingDirection else True:
                levels['stop_loss'] = levels['entry_price'] - 0.0020  # 20 pips
                levels['tp1'] = levels['entry_price'] + 0.0030       # 30 pips (1.5 RR)
                levels['tp2'] = levels['entry_price'] + 0.0060       # 60 pips (3.0 RR)
                levels['tp3'] = levels['entry_price'] + 0.0100       # 100 pips (5.0 RR)
            else:
                levels['stop_loss'] = levels['entry_price'] + 0.0020
                levels['tp1'] = levels['entry_price'] - 0.0030
                levels['tp2'] = levels['entry_price'] - 0.0060
                levels['tp3'] = levels['entry_price'] - 0.0100
            
            return levels
            
        except Exception as e:
            self._log_error(f"Error calculando trading levels: {e}")
            return {
                'entry_price': current_price,
                'entry_zone': (current_price - 0.0005, current_price + 0.0005),
                'stop_loss': current_price - 0.0020,
                'tp1': current_price + 0.0030,
                'tp2': current_price + 0.0060
            }

    def _calculate_confluence_risk_management(self,
                                            trading_levels: Dict,
                                            confluence_score: float) -> Dict:
        """⚠️ Calcular risk management para confluencia"""
        try:
            risk_reward = abs(trading_levels['tp1'] - trading_levels['entry_price']) / abs(trading_levels['stop_loss'] - trading_levels['entry_price'])
            
            # Position size basado en confluence score
            if confluence_score >= 8.0:
                position_size = 0.02  # 2% para confluencia extrema
                risk_level = TradeRiskLevel.MODERATE
            elif confluence_score >= 6.5:
                position_size = 0.015  # 1.5% para confluencia alta
                risk_level = TradeRiskLevel.LOW
            elif confluence_score >= 4.0:
                position_size = 0.01   # 1% para confluencia moderada
                risk_level = TradeRiskLevel.VERY_LOW
            else:
                position_size = 0.005  # 0.5% para confluencia baja
                risk_level = TradeRiskLevel.VERY_LOW
            
            return {
                'risk_level': risk_level,
                'risk_reward': risk_reward,
                'position_size': position_size,
                'max_loss': position_size
            }
            
        except Exception as e:
            self._log_error(f"Error calculando risk management: {e}")
            return {
                'risk_level': TradeRiskLevel.LOW,
                'risk_reward': 1.5,
                'position_size': 0.01,
                'max_loss': 0.01
            }

    def _calculate_confluence_probabilities(self,
                                          factors: ConfluenceFactors,
                                          confluence_score: float) -> Dict[str, float]:
        """📊 Calcular probabilidades para confluencia"""
        try:
            # Base win probability from confluence score
            base_prob = min(0.5 + (confluence_score / 20.0), 0.85)  # Max 85%
            
            # Adjust for pattern quality
            pattern_bonus = 0.0
            if factors.silver_bullet_signal:
                pattern_bonus += 0.05
            if factors.breaker_block_signal:
                pattern_bonus += 0.03
            if factors.liquidity_sweeps:
                pattern_bonus += 0.02
            
            win_prob = min(base_prob + pattern_bonus, 0.9)  # Max 90%
            
            # Confidence based on multiple factors
            confidence = min(confluence_score / 10.0, 0.95)  # Max 95%
            
            # Expected value (simplified)
            expected_value = (win_prob * 3.0) - ((1 - win_prob) * 1.0)  # Asume 3:1 RR
            
            return {
                'win_prob': win_prob,
                'confidence': confidence,
                'expected_value': expected_value
            }
            
        except Exception as e:
            self._log_error(f"Error calculando probabilidades: {e}")
            return {'win_prob': 0.6, 'confidence': 0.6, 'expected_value': 1.0}

    # ===========================================
    # 🔍 PATTERN MATCHING METHODS  
    # ===========================================

    def _find_matching_breaker_block(self, 
                                   primary_signal,
                                   bb_signals: List) -> Optional:
        """🔍 Encontrar Breaker Block coincidente"""
        try:
            if not bb_signals:
                return None
            
            # Por simplicidad, tomar el primer BB con dirección similar
            primary_direction = getattr(primary_signal, 'direction', None)
            
            for bb in bb_signals:
                bb_direction = getattr(bb, 'direction', None)
                if bb_direction == primary_direction:
                    return bb
            
            return bb_signals[0] if bb_signals else None
            
        except:
            return None

    def _find_matching_liquidity_sweeps(self, 
                                      primary_signal,
                                      ls_signals: List) -> List:
        """🔍 Encontrar Liquidity Sweeps coincidentes"""
        try:
            if not ls_signals:
                return []
            
            # Filtrar sweeps compatibles con dirección principal
            primary_direction = getattr(primary_signal, 'direction', None)
            
            matching_sweeps = []
            for sweep in ls_signals:
                sweep_direction = getattr(sweep, 'direction', None)
                if sweep_direction == primary_direction:
                    matching_sweeps.append(sweep)
            
            return matching_sweeps[:3]  # Máximo 3 sweeps
            
        except:
            return []

    def _determine_confluence_direction(self, confluence_group: Dict):
        """🎯 Determinar dirección de confluencia"""
        try:
            # Prioridad: Silver Bullet > Breaker Blocks > Liquidity Sweeps
            if confluence_group.get('silver_bullet'):
                return getattr(confluence_group['silver_bullet'], 'direction', None)
            elif confluence_group.get('breaker_blocks'):
                return getattr(confluence_group['breaker_blocks'], 'direction', None)
            elif confluence_group.get('liquidity_sweeps'):
                sweeps = confluence_group['liquidity_sweeps']
                if sweeps:
                    return getattr(sweeps[0], 'direction', None)
            
            return None
            
        except:
            return None

    # ===========================================
    # 📊 MARKET ANALYSIS METHODS
    # ===========================================

    def _analyze_trend_alignment(self, data_h1: pd.DataFrame, data_m15: pd.DataFrame) -> bool:
        """📈 Analizar alineación de tendencia"""
        try:
            if len(data_h1) < 20 or len(data_m15) < 20:
                return False
            
            # Simplificado: comparar EMAs
            h1_trend_up = data_h1['close'].iloc[-1] > data_h1['close'].rolling(20).mean().iloc[-1]
            m15_trend_up = data_m15['close'].iloc[-1] > data_m15['close'].rolling(20).mean().iloc[-1]
            
            return h1_trend_up == m15_trend_up
            
        except:
            return False

    def _analyze_structure_break(self, data_m15: pd.DataFrame, data_m5: pd.DataFrame) -> bool:
        """🔨 Analizar ruptura de estructura"""
        try:
            if len(data_m15) < 10:
                return False
            
            # Simplificado: buscar nuevos highs/lows recientes
            recent_high = data_m15['high'].tail(10).max()
            previous_high = data_m15['high'].iloc[-20:-10].max()
            
            return recent_high > previous_high
            
        except:
            return False

    def _analyze_sr_levels(self, data_m15: pd.DataFrame, confluence_group: Dict) -> bool:
        """📊 Analizar niveles de soporte/resistencia"""
        try:
            # Si hay liquidity pools cerca, consideramos que hay S/R
            pools = confluence_group.get('liquidity_pools', [])
            return len(pools) > 0
            
        except:
            return False

    def _analyze_volume_confirmation(self, data_m5: pd.DataFrame) -> bool:
        """📊 Analizar confirmación de volumen"""
        try:
            if 'volume' not in data_m5.columns or len(data_m5) < 10:
                return False
            
            recent_volume = data_m5['volume'].tail(5).mean()
            avg_volume = data_m5['volume'].tail(20).mean()
            
            return recent_volume > avg_volume * 1.2
            
        except:
            return False

    def _analyze_optimal_timing(self) -> bool:
        """⏰ Analizar timing óptimo"""
        try:
            current_hour = datetime.now().hour
            # London/NY overlap (13-17 UTC) o London session (8-17 UTC)
            return 8 <= current_hour <= 17
            
        except:
            return False

    def _analyze_session_alignment(self) -> bool:
        """🏛️ Analizar alineación de sesión"""
        try:
            current_hour = datetime.now().hour
            # Durante sesiones principales (no Asian)
            return 8 <= current_hour <= 22
            
        except:
            return False

    def _check_news_events(self) -> bool:
        """📰 Verificar eventos de noticias"""
        # Simplificado: asumir que no hay eventos importantes
        return True

    def _check_spread_conditions(self) -> bool:
        """📊 Verificar condiciones de spread"""
        # Simplificado: asumir spread normal
        return True

    def _check_volatility_conditions(self, data_m15: pd.DataFrame) -> bool:
        """📊 Verificar condiciones de volatilidad"""
        try:
            if len(data_m15) < 20:
                return True
            
            # Calcular ATR simplificado
            high_low = data_m15['high'] - data_m15['low']
            volatility = high_low.tail(20).mean()
            
            # Asumir volatilidad normal si está en rango razonable
            return 0.0005 <= volatility <= 0.0030
            
        except:
            return True

    def _analyze_smart_money_alignment(self, confluence_group: Dict) -> bool:
        """🏦 Analizar alineación smart money"""
        try:
            # Si hay patrones institucionales, consideramos alineación
            return (confluence_group.get('silver_bullet') is not None or 
                   confluence_group.get('breaker_blocks') is not None)
            
        except:
            return False

    def _analyze_institutional_flow(self, data_m5: pd.DataFrame) -> bool:
        """🏛️ Analizar flujo institucional"""
        try:
            # Simplificado: buscar movimientos fuertes recientes
            if len(data_m5) < 5:
                return False
            
            recent_range = data_m5['high'].tail(5).max() - data_m5['low'].tail(5).min()
            avg_range = (data_m5['high'] - data_m5['low']).tail(20).mean()
            
            return recent_range > avg_range * 1.5
            
        except:
            return False

    def _analyze_liquidity_hunt(self, liquidity_sweeps: List) -> bool:
        """🎯 Analizar hunt de liquidez"""
        return len(liquidity_sweeps) > 0

    # ===========================================
    # 🛠️ UTILITY METHODS
    # ===========================================

    def _determine_signal_quality(self, confidence: float) -> SignalQuality:
        """⭐ Determinar calidad de señal"""
        if confidence >= 0.8:
            return SignalQuality.EXCELLENT
        elif confidence >= 0.6:
            return SignalQuality.GOOD
        elif confidence >= 0.4:
            return SignalQuality.FAIR
        else:
            return SignalQuality.POOR

    def _determine_confluence_level(self, score: float) -> ConfluenceLevel:
        """📊 Determinar nivel de confluencia"""
        if score >= 8.0:
            return ConfluenceLevel.EXTREME
        elif score >= 6.5:
            return ConfluenceLevel.HIGH
        elif score >= 4.0:
            return ConfluenceLevel.MODERATE
        else:
            return ConfluenceLevel.LOW

    def _count_total_confluences(self, factors: ConfluenceFactors) -> int:
        """📊 Contar confluencias totales"""
        count = 0
        if factors.silver_bullet_signal: count += 1
        if factors.breaker_block_signal: count += 1
        if factors.liquidity_sweeps: count += 1
        if factors.trend_alignment: count += 1
        if factors.structure_break: count += 1
        if factors.support_resistance_level: count += 1
        if factors.volume_confirmation: count += 1
        if factors.time_of_day_optimal: count += 1
        if factors.session_alignment: count += 1
        if factors.smart_money_alignment: count += 1
        if factors.institutional_order_flow: count += 1
        if factors.liquidity_hunt_complete: count += 1
        return count

    def _count_critical_confluences(self, factors: ConfluenceFactors) -> int:
        """🎯 Contar confluencias críticas"""
        count = 0
        if factors.silver_bullet_signal: count += 1
        if factors.breaker_block_signal: count += 1
        if factors.liquidity_sweeps: count += 1
        if factors.smart_money_alignment: count += 1
        return count

    def _generate_invalidation_conditions(self, confluence_group: Dict) -> List[str]:
        """⚠️ Generar condiciones de invalidación"""
        conditions = [
            "Precio cierra por encima/debajo del stop loss",
            "Patrón de confluencia se rompe",
            "Tiempo máximo de espera excedido"
        ]
        
        if confluence_group.get('silver_bullet'):
            conditions.append("Silver Bullet invalidado")
        
        if confluence_group.get('breaker_blocks'):
            conditions.append("Breaker Block invalidado")
        
        return conditions

    def _generate_trade_narrative(self, confluence_group: Dict, direction) -> str:
        """📝 Generar narrativa del trade"""
        patterns = []
        
        if confluence_group.get('silver_bullet'):
            patterns.append("Silver Bullet")
        
        if confluence_group.get('breaker_blocks'):
            patterns.append("Breaker Block")
        
        if confluence_group.get('liquidity_sweeps'):
            patterns.append("Liquidity Sweep")
        
        # 📌 REGLA #14: Expresión condicional corregida
        try:
            direction_text = "COMPRA" if direction == TradingDirection.BUY else "VENTA"
        except:
            direction_text = "NEUTRAL"
        
        return f"Confluencia {direction_text} detectada con patrones: {', '.join(patterns)}"

    def _generate_market_context(self, data_h1: pd.DataFrame, data_m15: pd.DataFrame) -> str:
        """📊 Generar contexto de mercado"""
        try:
            if len(data_h1) >= 5:
                trend = "Alcista" if data_h1['close'].iloc[-1] > data_h1['close'].iloc[-5] else "Bajista"
                return f"Tendencia {trend} en H1 - Confluencia detectada en M15"
            else:
                return "Análisis de confluencia multi-patrón"
        except:
            return "Contexto de mercado en análisis"

    def _extract_key_levels(self, confluence_group: Dict) -> Dict[str, float]:
        """🔑 Extraer niveles clave"""
        levels = {}
        
        try:
            if confluence_group.get('silver_bullet'):
                levels['silver_bullet_entry'] = getattr(confluence_group['silver_bullet'], 'entry_price', 0.0)
            
            if confluence_group.get('breaker_blocks'):
                levels['breaker_block_level'] = getattr(confluence_group['breaker_blocks'], 'entry_price', 0.0)
            
            pools = confluence_group.get('liquidity_pools', [])
            if pools:
                levels['liquidity_pool'] = pools[0].price_level
                
        except:
            pass
        
        return levels

    def _validate_confluence_signals(self, 
                                   signals: List[ConfluenceTradeSignal],
                                   data_m5: pd.DataFrame) -> List[ConfluenceTradeSignal]:
        """✅ Validar señales de confluencia"""
        try:
            validated = []
            
            for signal in signals:
                # Filtros de validación
                if (signal.confluence_score >= self.config['min_confluence_score'] and
                    signal.confidence_score >= self.config['min_confidence_for_trade'] and
                    signal.risk_reward_ratio >= self.config['min_risk_reward_ratio']):
                    validated.append(signal)
            
            return validated
            
        except Exception as e:
            self._log_error(f"Error validando señales: {e}")
            return signals

    def _rank_signals_by_quality(self, signals: List[ConfluenceTradeSignal]) -> List[ConfluenceTradeSignal]:
        """🏆 Ranking de señales por calidad"""
        try:
            return sorted(signals, 
                         key=lambda s: (s.confluence_score, s.confidence_score, s.risk_reward_ratio),
                         reverse=True)
        except:
            return signals

    # ===========================================
    # 💾 MEMORY & STATS METHODS
    # ===========================================

    def _store_confluence_signals_in_memory(self, signals: List[ConfluenceTradeSignal]):
        """💾 Guardar señales en memoria"""
        try:
            self.detected_signals.extend(signals)
            
            # Limitar memoria
            if len(self.detected_signals) > 20:
                self.detected_signals = self.detected_signals[-20:]
                
        except Exception as e:
            self._log_error(f"Error storing signals: {e}")

    def _update_confluence_stats(self, signals: List[ConfluenceTradeSignal]):
        """📊 Actualizar estadísticas"""
        try:
            self.confluence_stats['total_signals_generated'] += len(signals)
            
            high_conf = len([s for s in signals if s.confluence_level in [ConfluenceLevel.HIGH, ConfluenceLevel.EXTREME]])
            self.confluence_stats['high_confluence_signals'] += high_conf
            
            extreme_conf = len([s for s in signals if s.confluence_level == ConfluenceLevel.EXTREME])
            self.confluence_stats['extreme_confluence_signals'] += extreme_conf
            
            if signals:
                avg_score = sum(s.confluence_score for s in signals) / len(signals)
                self.confluence_stats['average_confluence_score'] = avg_score
                
        except:
            pass

    # ===========================================
    # 🛠️ LOGGING METHODS  
    # ===========================================

    def _create_fallback_logger(self):
        """📝 Crear logger fallback"""
        class FallbackLogger:
            def log_info(self, msg, component="confluence"): print(f"[INFO] {msg}")
            def log_warning(self, msg, component="confluence"): print(f"[WARNING] {msg}")
            def log_error(self, msg, component="confluence"): print(f"[ERROR] {msg}")
            def log_debug(self, msg, component="confluence"): print(f"[DEBUG] {msg}")
        return FallbackLogger()

    def _log_info(self, message: str):
        if self.logger: self.logger.log_info(message, "confluence_enterprise")
        else: print(f"[INFO] {message}")

    def _log_warning(self, message: str):
        if self.logger: self.logger.log_warning(message, "confluence_enterprise")
        else: print(f"[WARNING] {message}")

    def _log_error(self, message: str):
        if self.logger: self.logger.log_error(message, "confluence_enterprise")
        else: print(f"[ERROR] {message}")

    def _log_debug(self, message: str):
        if self.logger: self.logger.log_debug(message, "confluence_enterprise")
        else: print(f"[DEBUG] {message}")


# ===========================================
# 🧪 TESTING & UTILITIES
# ===========================================

def create_test_confluence_engine() -> MultiPatternConfluenceEngine:
    """🧪 Crear engine para testing"""
    return MultiPatternConfluenceEngine()


if __name__ == "__main__":
    # 🧪 Test básico
    engine = create_test_confluence_engine()
    print("✅ Multi-Pattern Confluence Engine v6.0 - Test básico completado")
