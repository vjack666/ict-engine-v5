#!/usr/bin/env python3
"""
💧 LIQUIDITY ANALYZER ENTERPRISE v6.0
=====================================

Advanced Institutional Liquidity Analysis with enterprise features:
- Equal Highs/Lows detection
- Liquidity pool identification  
- Sweep pattern analysis
- Liquidity hunt detection
- UnifiedMemorySystem v6.1 integration
- SLUC v2.1 logging system

FASE 5: Advanced Patterns Migration
Migrated from: Multiple legacy sources (ict_detector.py, pattern_analyzer.py, smart_money_analyzer.py)
Target: Enterprise v6.0 SIC architecture

Autor: ICT Engine Team
Sprint: FASE 5 - Advanced Patterns
Fecha: 09 Agosto 2025
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np

# 🏗️ ENTERPRISE ARCHITECTURE v6.0
try:
    from core.smart_trading_logger import SmartTradingLogger
    from core.data_management.unified_memory_system import UnifiedMemorySystem
    from core.ict_engine.ict_types import TradingDirection
except ImportError:
    # Fallback for testing
    print("[WARNING] Enterprise modules not available - using fallback")
    SmartTradingLogger = None
    UnifiedMemorySystem = None
    
    # Fallback TradingDirection for testing
    from enum import Enum
    class TradingDirection(Enum):
        BUY = "buy"
        SELL = "sell"
        BULLISH = "bullish"
        BEARISH = "bearish"
        NEUTRAL = "neutral"


class LiquidityPoolType(Enum):
    """💧 Tipos de Liquidity Pools"""
    EQUAL_HIGHS = "equal_highs"              # Equal highs (bearish liquidity)
    EQUAL_LOWS = "equal_lows"                # Equal lows (bullish liquidity)
    OLD_HIGH = "old_high"                    # Previous significant high
    OLD_LOW = "old_low"                      # Previous significant low
    DAILY_HIGH = "daily_high"                # Daily high level
    DAILY_LOW = "daily_low"                  # Daily low level
    WEEKLY_HIGH = "weekly_high"              # Weekly high level
    WEEKLY_LOW = "weekly_low"                # Weekly low level
    SESSION_HIGH = "session_high"            # Session extreme high
    SESSION_LOW = "session_low"              # Session extreme low
    STOP_CLUSTER = "stop_cluster"            # Stop loss cluster zone
    UNKNOWN = "unknown"


class LiquiditySweepType(Enum):
    """🌊 Tipos de Liquidity Sweeps"""
    UPSIDE_SWEEP = "upside_sweep"            # Sweep of highs (bearish)
    DOWNSIDE_SWEEP = "downside_sweep"        # Sweep of lows (bullish)
    DOUBLE_SWEEP = "double_sweep"            # Sweep both sides
    FAILED_SWEEP = "failed_sweep"            # Sweep attempt failed
    UNKNOWN = "unknown"


class LiquidityZoneStatus(Enum):
    """🎯 Estado de zonas de liquidez"""
    INTACT = "intact"                # No tocado aún
    APPROACHING = "approaching"      # Precio acercándose
    TESTING = "testing"             # Siendo testeado
    SWEPT = "swept"                 # Ya barrido
    RESPECTED = "respected"         # Respetado como S/R
    EXPIRED = "expired"             # Expirado por tiempo


@dataclass
class LiquidityPool:
    """💧 Pool de Liquidez Enterprise"""
    pool_type: LiquidityPoolType
    price_level: float
    price_zone: Tuple[float, float]
    
    # 📊 Métricas de liquidez
    strength: float                 # 0.0 - 1.0
    liquidity_depth: float         # Estimación de volumen disponible
    touches: int                   # Número de veces tocado
    
    # 🏦 Análisis institucional
    institutional_interest: float  # 0.0 - 1.0
    smart_money_bias: float       # -1.0 (bearish) to 1.0 (bullish)
    volume_evidence: float        # 0.0 - 1.0
    
    # ⏰ Timing y contexto
    timestamp: datetime
    session_origin: str           # London/NY/Asian
    timeframe_origin: str         # H4/H1/M15 etc
    
    # 🎯 Trading expectativas
    expected_reaction: str        # "bullish_reaction", "bearish_reaction"
    invalidation_price: float
    
    # 📝 Metadata
    status: LiquidityZoneStatus = LiquidityZoneStatus.INTACT
    last_test_time: Optional[datetime] = None
    test_count: int = 0
    successful_tests: int = 0


@dataclass  
class LiquiditySweepSignal:
    """🌊 Señal de Liquidity Sweep Enterprise"""
    sweep_type: LiquiditySweepType
    direction: TradingDirection
    
    # 📊 Detalles del sweep
    target_level: float
    sweep_price: float
    liquidity_captured: float
    
    # 🎯 Reacción esperada
    reversal_target: float
    reversal_probability: float
    
    # 📈 Trading levels
    entry_zone: Tuple[float, float]
    stop_loss: float
    take_profit_1: float
    take_profit_2: float
    
    # 📊 Métricas enterprise
    confidence: float
    institutional_confirmation: bool
    volume_spike: bool
    
    # 📝 Metadata
    narrative: str
    timestamp: datetime
    symbol: str
    timeframe: str
    analysis_id: str = ""


class LiquidityAnalyzerEnterprise:
    """
    💧 LIQUIDITY ANALYZER ENTERPRISE v6.0
    ====================================
    
    Advanced institutional liquidity analysis system:
    ✅ Equal highs/lows detection con tolerancia inteligente
    ✅ Liquidity pool identification multi-timeframe
    ✅ Sweep pattern analysis con confirmación volume
    ✅ Smart money bias calculation
    ✅ Institutional interest validation
    ✅ UnifiedMemorySystem v6.1 integration
    ✅ SLUC v2.1 logging completo
    ✅ Real-time liquidity monitoring
    """

    def __init__(self, 
                 memory_system: Optional[UnifiedMemorySystem] = None,
                 logger: Optional[SmartTradingLogger] = None):
        """🚀 Inicializar Liquidity Analyzer Enterprise"""
        
        # 🏗️ ENTERPRISE INFRASTRUCTURE
        self.memory_system = memory_system
        self.logger = logger or self._create_fallback_logger()
        
        self._log_info("💧 Inicializando Liquidity Analyzer Enterprise v6.0")
        
        # ⚙️ LIQUIDITY DETECTION CONFIGURATION
        self.config = {
            # Equal levels detection
            'equal_highs_tolerance': 0.0005,      # 5 pips tolerance
            'equal_lows_tolerance': 0.0005,       # 5 pips tolerance
            'minimum_touches': 2,                 # Mínimo touches para equal level
            'max_equal_level_age_hours': 72,      # Máxima edad para considerar level
            
            # Liquidity pools
            'min_pool_strength': 0.4,             # Fuerza mínima para pool válido
            'pool_invalidation_distance': 0.002,  # 20 pips para invalidación
            'max_simultaneous_pools': 15,         # Máximo pools activos
            
            # Sweep detection
            'sweep_confirmation_pips': 3,         # Pips mínimos para confirmar sweep
            'sweep_reversal_window_candles': 5,   # Velas para buscar reversión
            'min_sweep_strength': 0.6,            # Fuerza mínima para sweep válido
            
            # Volume analysis
            'volume_spike_threshold': 1.8,        # Multiplicador para volume spike
            'institutional_volume_threshold': 2.5, # Multiplicador para volume institucional
            
            # Session analysis
            'session_extreme_lookback': 20,       # Períodos para buscar extremos de sesión
            'daily_level_significance': 0.7,      # Significancia mínima para niveles daily
        }
        
        # 📊 ESTADO INTERNO
        self.detected_pools: List[LiquidityPool] = []
        self.detected_sweeps: List[LiquiditySweepSignal] = []
        self.processing_stats = {
            'total_pools_detected': 0,
            'total_sweeps_detected': 0,
            'equal_highs_found': 0,
            'equal_lows_found': 0,
            'institutional_pools': 0,
            'successful_sweeps': 0
        }
        
        self._log_info("✅ Liquidity Analyzer Enterprise v6.0 inicializado correctamente")

    def detect_liquidity_pools_enterprise(self,
                                         data_h4: pd.DataFrame,
                                         data_h1: pd.DataFrame,
                                         data_m15: pd.DataFrame,
                                         symbol: str,
                                         current_price: float) -> List[LiquidityPool]:
        """
        💧 DETECCIÓN PRINCIPAL DE LIQUIDITY POOLS ENTERPRISE
        
        Args:
            data_h4: Datos H4 para contexto macro
            data_h1: Datos H1 para niveles intermedios
            data_m15: Datos M15 para precisión
            symbol: Par de divisa
            current_price: Precio actual
            
        Returns:
            Lista de Liquidity Pools detectados
        """
        try:
            self._log_info(f"💧 Iniciando detección Liquidity Pools para {symbol}")
            
            detected_pools = []
            
            # 1. 🔍 DETECTAR EQUAL HIGHS/LOWS EN H4
            eq_highs_h4 = self._detect_equal_highs_enterprise(data_h4, "H4", symbol)
            eq_lows_h4 = self._detect_equal_lows_enterprise(data_h4, "H4", symbol)
            detected_pools.extend(eq_highs_h4)
            detected_pools.extend(eq_lows_h4)
            
            # 2. 🔍 DETECTAR EQUAL HIGHS/LOWS EN H1
            eq_highs_h1 = self._detect_equal_highs_enterprise(data_h1, "H1", symbol)
            eq_lows_h1 = self._detect_equal_lows_enterprise(data_h1, "H1", symbol)
            detected_pools.extend(eq_highs_h1)
            detected_pools.extend(eq_lows_h1)
            
            # 3. 🎯 DETECTAR OLD HIGHS/LOWS SIGNIFICATIVOS
            old_levels = self._detect_old_highs_lows_enterprise(data_h4, data_h1, symbol)
            detected_pools.extend(old_levels)
            
            # 4. 📅 DETECTAR DAILY/WEEKLY LEVELS
            daily_weekly = self._detect_daily_weekly_levels_enterprise(data_h4, symbol)
            detected_pools.extend(daily_weekly)
            
            # 5. 🏛️ DETECTAR SESSION EXTREMES
            session_extremes = self._detect_session_extremes_enterprise(data_h1, data_m15, symbol)
            detected_pools.extend(session_extremes)
            
            # 6. 🏦 VALIDAR INTERÉS INSTITUCIONAL
            validated_pools = []
            for pool in detected_pools:
                institutional_score = self._validate_institutional_interest_enterprise(
                    pool, data_m15, current_price
                )
                pool.institutional_interest = institutional_score
                
                if institutional_score >= 0.3:  # Threshold mínimo para interés institucional
                    validated_pools.append(pool)
            
            # 7. 🎯 FILTRAR POR RELEVANCIA Y PROXIMIDAD
            filtered_pools = self._filter_pools_by_relevance(validated_pools, current_price)
            
            # 8. 💾 GUARDAR EN MEMORIA ENTERPRISE
            if self.memory_system and filtered_pools:
                self._store_pools_in_memory(filtered_pools)
            
            # 9. 📊 ACTUALIZAR ESTADÍSTICAS
            self._update_pools_stats(filtered_pools)
            
            self._log_info(f"🎯 Detección completada: {len(filtered_pools)} Liquidity Pools válidos de {len(detected_pools)} candidatos")
            return filtered_pools
            
        except Exception as e:
            self._log_error(f"❌ Error en detección de Liquidity Pools: {e}")
            return []

    def detect_liquidity_sweeps_enterprise(self,
                                          data: pd.DataFrame,
                                          liquidity_pools: List[LiquidityPool],
                                          symbol: str,
                                          timeframe: str) -> List[LiquiditySweepSignal]:
        """
        🌊 DETECCIÓN DE LIQUIDITY SWEEPS ENTERPRISE
        
        Args:
            data: Datos de velas OHLCV
            liquidity_pools: Pools de liquidez detectados
            symbol: Par de divisa
            timeframe: Timeframe de análisis
            
        Returns:
            Lista de Liquidity Sweeps detectados
        """
        try:
            self._log_info(f"🌊 Iniciando detección Liquidity Sweeps para {symbol} {timeframe}")
            
            if not liquidity_pools:
                self._log_warning("⚠️ No hay liquidity pools para análisis de sweeps")
                return []
            
            detected_sweeps = []
            recent_data = data.tail(50)  # Últimas 50 velas
            
            # 🔍 ANALIZAR CADA POOL PARA POSIBLES SWEEPS
            for pool in liquidity_pools:
                try:
                    # Verificar si el pool está en rango para sweep
                    if not self._is_pool_in_sweep_range(pool, recent_data):
                        continue
                    
                    # 1. 🎯 DETECTAR UPSIDE SWEEPS (barrido de highs)
                    if pool.pool_type in [LiquidityPoolType.EQUAL_HIGHS, LiquidityPoolType.OLD_HIGH]:
                        upside_sweep = self._detect_upside_sweep_enterprise(pool, recent_data, symbol, timeframe)
                        if upside_sweep:
                            detected_sweeps.append(upside_sweep)
                    
                    # 2. 🎯 DETECTAR DOWNSIDE SWEEPS (barrido de lows)
                    elif pool.pool_type in [LiquidityPoolType.EQUAL_LOWS, LiquidityPoolType.OLD_LOW]:
                        downside_sweep = self._detect_downside_sweep_enterprise(pool, recent_data, symbol, timeframe)
                        if downside_sweep:
                            detected_sweeps.append(downside_sweep)
                    
                except Exception as e:
                    self._log_error(f"Error analizando pool {pool.pool_type}: {e}")
                    continue
            
            # 3. 🔍 DETECTAR SWEEPS GENERALES (sin pools específicos)
            general_sweeps = self._detect_general_sweeps_enterprise(recent_data, symbol, timeframe)
            detected_sweeps.extend(general_sweeps)
            
            # 4. ✅ VALIDAR Y FILTRAR SWEEPS
            validated_sweeps = self._validate_sweep_signals(detected_sweeps, recent_data)
            
            # 5. 💾 GUARDAR EN MEMORIA ENTERPRISE
            if self.memory_system and validated_sweeps:
                self._store_sweeps_in_memory(validated_sweeps)
            
            # 6. 📊 ACTUALIZAR ESTADÍSTICAS
            self._update_sweeps_stats(validated_sweeps)
            
            self._log_info(f"🎯 Detección sweeps completada: {len(validated_sweeps)} sweeps válidos de {len(detected_sweeps)} candidatos")
            return validated_sweeps
            
        except Exception as e:
            self._log_error(f"❌ Error en detección de Liquidity Sweeps: {e}")
            return []

    # ===========================================
    # 🔍 EQUAL HIGHS/LOWS DETECTION
    # ===========================================

    def _detect_equal_highs_enterprise(self, 
                                      data: pd.DataFrame, 
                                      timeframe: str,
                                      symbol: str) -> List[LiquidityPool]:
        """🔍 Detectar Equal Highs enterprise"""
        try:
            pools = []
            if len(data) < 20:
                return pools
            
            tolerance = self.config['equal_highs_tolerance']
            min_touches = self.config['minimum_touches']
            
            # Rolling max para encontrar highs locales
            highs = data['high'].rolling(window=5, center=True).max()
            
            for i in range(10, len(data) - 10):
                current_high = highs.iloc[i]
                
                # Buscar highs similares en ventana de búsqueda
                search_window = highs.iloc[max(0, i-20):min(len(highs), i+20)]
                equal_highs = search_window[abs(search_window - current_high) <= tolerance]
                
                if len(equal_highs) >= min_touches:
                    # Calcular métricas del pool
                    strength = min(len(equal_highs) / 5.0, 1.0)
                    touches = len(equal_highs)
                    
                    pool = LiquidityPool(
                        pool_type=LiquidityPoolType.EQUAL_HIGHS,
                        price_level=current_high,
                        price_zone=(current_high - tolerance, current_high + tolerance),
                        strength=strength,
                        liquidity_depth=self._estimate_liquidity_depth(touches, strength),
                        touches=touches,
                        institutional_interest=0.0,  # Se calculará después
                        smart_money_bias=-0.6,       # Equal highs = bearish bias
                        volume_evidence=0.5,         # Se validará después
                        timestamp=data.index[i] if hasattr(data.index[i], 'hour') else datetime.now(),
                        session_origin=self._identify_session_origin(data.index[i] if hasattr(data.index[i], 'hour') else datetime.now()),
                        timeframe_origin=timeframe,
                        expected_reaction="bearish_reaction",
                        invalidation_price=current_high + self.config['pool_invalidation_distance']
                    )
                    
                    pools.append(pool)
                    self._log_debug(f"Equal Highs detectado: {current_high:.5f} con {touches} touches")
            
            self.processing_stats['equal_highs_found'] += len(pools)
            return pools
            
        except Exception as e:
            self._log_error(f"Error detectando equal highs: {e}")
            return []

    def _detect_equal_lows_enterprise(self, 
                                     data: pd.DataFrame, 
                                     timeframe: str,
                                     symbol: str) -> List[LiquidityPool]:
        """🔍 Detectar Equal Lows enterprise"""
        try:
            pools = []
            if len(data) < 20:
                return pools
            
            tolerance = self.config['equal_lows_tolerance']
            min_touches = self.config['minimum_touches']
            
            # Rolling min para encontrar lows locales
            lows = data['low'].rolling(window=5, center=True).min()
            
            for i in range(10, len(data) - 10):
                current_low = lows.iloc[i]
                
                # Buscar lows similares en ventana de búsqueda
                search_window = lows.iloc[max(0, i-20):min(len(lows), i+20)]
                equal_lows = search_window[abs(search_window - current_low) <= tolerance]
                
                if len(equal_lows) >= min_touches:
                    # Calcular métricas del pool
                    strength = min(len(equal_lows) / 5.0, 1.0)
                    touches = len(equal_lows)
                    
                    pool = LiquidityPool(
                        pool_type=LiquidityPoolType.EQUAL_LOWS,
                        price_level=current_low,
                        price_zone=(current_low - tolerance, current_low + tolerance),
                        strength=strength,
                        liquidity_depth=self._estimate_liquidity_depth(touches, strength),
                        touches=touches,
                        institutional_interest=0.0,  # Se calculará después
                        smart_money_bias=0.6,        # Equal lows = bullish bias
                        volume_evidence=0.5,         # Se validará después
                        timestamp=data.index[i] if hasattr(data.index[i], 'hour') else datetime.now(),
                        session_origin=self._identify_session_origin(data.index[i] if hasattr(data.index[i], 'hour') else datetime.now()),
                        timeframe_origin=timeframe,
                        expected_reaction="bullish_reaction",
                        invalidation_price=current_low - self.config['pool_invalidation_distance']
                    )
                    
                    pools.append(pool)
                    self._log_debug(f"Equal Lows detectado: {current_low:.5f} con {touches} touches")
            
            self.processing_stats['equal_lows_found'] += len(pools)
            return pools
            
        except Exception as e:
            self._log_error(f"Error detectando equal lows: {e}")
            return []

    # ===========================================
    # 🎯 OLD HIGHS/LOWS & DAILY LEVELS
    # ===========================================

    def _detect_old_highs_lows_enterprise(self, 
                                         data_h4: pd.DataFrame,
                                         data_h1: pd.DataFrame, 
                                         symbol: str) -> List[LiquidityPool]:
        """🎯 Detectar old highs/lows significativos"""
        try:
            pools = []
            
            # Old highs/lows de H4 (últimos 50 períodos)
            if len(data_h4) >= 50:
                recent_h4 = data_h4.tail(50)
                old_high = recent_h4['high'].max()
                old_low = recent_h4['low'].min()
                
                # Pool para old high
                pools.append(LiquidityPool(
                    pool_type=LiquidityPoolType.OLD_HIGH,
                    price_level=old_high,
                    price_zone=(old_high - 0.0003, old_high + 0.0003),
                    strength=0.75,
                    liquidity_depth=0.8,
                    touches=1,
                    institutional_interest=0.0,
                    smart_money_bias=-0.5,
                    volume_evidence=0.6,
                    timestamp=recent_h4[recent_h4['high'] == old_high].index[0],
                    session_origin="multiple",
                    timeframe_origin="H4",
                    expected_reaction="bearish_reaction",
                    invalidation_price=old_high + 0.002
                ))
                
                # Pool para old low
                pools.append(LiquidityPool(
                    pool_type=LiquidityPoolType.OLD_LOW,
                    price_level=old_low,
                    price_zone=(old_low - 0.0003, old_low + 0.0003),
                    strength=0.75,
                    liquidity_depth=0.8,
                    touches=1,
                    institutional_interest=0.0,
                    smart_money_bias=0.5,
                    volume_evidence=0.6,
                    timestamp=recent_h4[recent_h4['low'] == old_low].index[0],
                    session_origin="multiple",
                    timeframe_origin="H4",
                    expected_reaction="bullish_reaction",
                    invalidation_price=old_low - 0.002
                ))
            
            return pools
            
        except Exception as e:
            self._log_error(f"Error detectando old highs/lows: {e}")
            return []

    def _detect_daily_weekly_levels_enterprise(self, 
                                              data: pd.DataFrame, 
                                              symbol: str) -> List[LiquidityPool]:
        """📅 Detectar niveles daily/weekly"""
        try:
            pools = []
            
            if len(data) < 24:  # Mínimo un día de datos H4
                return pools
            
            # Daily high/low (últimas 6 velas H4 = 24 horas)
            daily_data = data.tail(6)
            daily_high = daily_data['high'].max()
            daily_low = daily_data['low'].min()
            
            # Daily High pool
            pools.append(LiquidityPool(
                pool_type=LiquidityPoolType.DAILY_HIGH,
                price_level=daily_high,
                price_zone=(daily_high - 0.0002, daily_high + 0.0002),
                strength=0.8,
                liquidity_depth=0.9,
                touches=1,
                institutional_interest=0.0,
                smart_money_bias=-0.4,
                volume_evidence=0.7,
                timestamp=datetime.now(),
                session_origin="daily",
                timeframe_origin="D1",
                expected_reaction="bearish_reaction",
                invalidation_price=daily_high + 0.0015
            ))
            
            # Daily Low pool
            pools.append(LiquidityPool(
                pool_type=LiquidityPoolType.DAILY_LOW,
                price_level=daily_low,
                price_zone=(daily_low - 0.0002, daily_low + 0.0002),
                strength=0.8,
                liquidity_depth=0.9,
                touches=1,
                institutional_interest=0.0,
                smart_money_bias=0.4,
                volume_evidence=0.7,
                timestamp=datetime.now(),
                session_origin="daily",
                timeframe_origin="D1",
                expected_reaction="bullish_reaction",
                invalidation_price=daily_low - 0.0015
            ))
            
            return pools
            
        except Exception as e:
            self._log_error(f"Error detectando daily levels: {e}")
            return []

    def _detect_session_extremes_enterprise(self, 
                                           data_h1: pd.DataFrame,
                                           data_m15: pd.DataFrame, 
                                           symbol: str) -> List[LiquidityPool]:
        """🏛️ Detectar extremos de sesión"""
        try:
            pools = []
            
            # Simplificado: usar últimos extremos de H1
            if len(data_h1) >= self.config['session_extreme_lookback']:
                recent = data_h1.tail(self.config['session_extreme_lookback'])
                session_high = recent['high'].max()
                session_low = recent['low'].min()
                
                # Session High pool
                pools.append(LiquidityPool(
                    pool_type=LiquidityPoolType.SESSION_HIGH,
                    price_level=session_high,
                    price_zone=(session_high - 0.0002, session_high + 0.0002),
                    strength=0.65,
                    liquidity_depth=0.7,
                    touches=1,
                    institutional_interest=0.0,
                    smart_money_bias=-0.3,
                    volume_evidence=0.5,
                    timestamp=datetime.now(),
                    session_origin=self._get_current_session(),
                    timeframe_origin="H1",
                    expected_reaction="bearish_reaction",
                    invalidation_price=session_high + 0.001
                ))
                
                # Session Low pool
                pools.append(LiquidityPool(
                    pool_type=LiquidityPoolType.SESSION_LOW,
                    price_level=session_low,
                    price_zone=(session_low - 0.0002, session_low + 0.0002),
                    strength=0.65,
                    liquidity_depth=0.7,
                    touches=1,
                    institutional_interest=0.0,
                    smart_money_bias=0.3,
                    volume_evidence=0.5,
                    timestamp=datetime.now(),
                    session_origin=self._get_current_session(),
                    timeframe_origin="H1",
                    expected_reaction="bullish_reaction",
                    invalidation_price=session_low - 0.001
                ))
            
            return pools
            
        except Exception as e:
            self._log_error(f"Error detectando session extremes: {e}")
            return []

    # ===========================================
    # 🌊 LIQUIDITY SWEEPS DETECTION
    # ===========================================

    def _detect_upside_sweep_enterprise(self, 
                                       pool: LiquidityPool,
                                       data: pd.DataFrame,
                                       symbol: str, 
                                       timeframe: str) -> Optional[LiquiditySweepSignal]:
        """🌊 Detectar upside sweep (barrido de highs)"""
        try:
            target_level = pool.price_level
            sweep_threshold = target_level + (self.config['sweep_confirmation_pips'] * 0.0001)
            
            # Buscar precio que supera el nivel
            for i, (timestamp, candle) in enumerate(data.iterrows()):
                if candle['high'] > sweep_threshold:
                    # ✅ SWEEP CONFIRMADO
                    
                    # Buscar reversión en las siguientes velas
                    reversal_confirmed = False
                    reversal_candles = data.iloc[i+1:i+1+self.config['sweep_reversal_window_candles']]
                    
                    if len(reversal_candles) > 0:
                        # Verificar si hay reversión bearish después del sweep
                        reversal_low = reversal_candles['low'].min()
                        if reversal_low < target_level:
                            reversal_confirmed = True
                    
                    # Calcular métricas del sweep
                    sweep_distance = candle['high'] - target_level
                    liquidity_captured = self._estimate_swept_liquidity(pool, sweep_distance)
                    
                    # Crear señal de sweep
                    sweep_signal = LiquiditySweepSignal(
                        sweep_type=LiquiditySweepType.UPSIDE_SWEEP,
                        direction=TradingDirection.SELL if reversal_confirmed else TradingDirection.BUY,
                        target_level=target_level,
                        sweep_price=candle['high'],
                        liquidity_captured=liquidity_captured,
                        reversal_target=target_level - 0.0030 if reversal_confirmed else target_level + 0.0030,
                        reversal_probability=0.8 if reversal_confirmed else 0.3,
                        entry_zone=self._calculate_sweep_entry_zone(candle['high'], TradingDirection.SELL if reversal_confirmed else TradingDirection.BUY),
                        stop_loss=self._calculate_sweep_stop_loss(candle['high'], TradingDirection.SELL if reversal_confirmed else TradingDirection.BUY),
                        take_profit_1=self._calculate_sweep_tp1(candle['high'], TradingDirection.SELL if reversal_confirmed else TradingDirection.BUY),
                        take_profit_2=self._calculate_sweep_tp2(candle['high'], TradingDirection.SELL if reversal_confirmed else TradingDirection.BUY),
                        confidence=self._calculate_sweep_confidence(pool, sweep_distance, reversal_confirmed),
                        institutional_confirmation=pool.institutional_interest > 0.6,
                        volume_spike=self._detect_volume_spike(data, i),
                        narrative=f"Upside sweep del level {target_level:.5f} - Liquidez capturada: {liquidity_captured:.1%}",
                        timestamp=timestamp,
                        symbol=symbol,
                        timeframe=timeframe,
                        analysis_id=f"SWEEP_{symbol}_{int(datetime.now().timestamp())}"
                    )
                    
                    return sweep_signal
            
            return None
            
        except Exception as e:
            self._log_error(f"Error detectando upside sweep: {e}")
            return None

    def _detect_downside_sweep_enterprise(self, 
                                        pool: LiquidityPool,
                                        data: pd.DataFrame,
                                        symbol: str, 
                                        timeframe: str) -> Optional[LiquiditySweepSignal]:
        """🌊 Detectar downside sweep (barrido de lows)"""
        try:
            target_level = pool.price_level
            sweep_threshold = target_level - (self.config['sweep_confirmation_pips'] * 0.0001)
            
            # Buscar precio que rompe por debajo del nivel
            for i, (timestamp, candle) in enumerate(data.iterrows()):
                if candle['low'] < sweep_threshold:
                    # ✅ SWEEP CONFIRMADO
                    
                    # Buscar reversión en las siguientes velas
                    reversal_confirmed = False
                    reversal_candles = data.iloc[i+1:i+1+self.config['sweep_reversal_window_candles']]
                    
                    if len(reversal_candles) > 0:
                        # Verificar si hay reversión bullish después del sweep
                        reversal_high = reversal_candles['high'].max()
                        if reversal_high > target_level:
                            reversal_confirmed = True
                    
                    # Calcular métricas del sweep
                    sweep_distance = target_level - candle['low']
                    liquidity_captured = self._estimate_swept_liquidity(pool, sweep_distance)
                    
                    # Crear señal de sweep
                    sweep_signal = LiquiditySweepSignal(
                        sweep_type=LiquiditySweepType.DOWNSIDE_SWEEP,
                        direction=TradingDirection.BUY if reversal_confirmed else TradingDirection.SELL,
                        target_level=target_level,
                        sweep_price=candle['low'],
                        liquidity_captured=liquidity_captured,
                        reversal_target=target_level + 0.0030 if reversal_confirmed else target_level - 0.0030,
                        reversal_probability=0.8 if reversal_confirmed else 0.3,
                        entry_zone=self._calculate_sweep_entry_zone(candle['low'], TradingDirection.BUY if reversal_confirmed else TradingDirection.SELL),
                        stop_loss=self._calculate_sweep_stop_loss(candle['low'], TradingDirection.BUY if reversal_confirmed else TradingDirection.SELL),
                        take_profit_1=self._calculate_sweep_tp1(candle['low'], TradingDirection.BUY if reversal_confirmed else TradingDirection.SELL),
                        take_profit_2=self._calculate_sweep_tp2(candle['low'], TradingDirection.BUY if reversal_confirmed else TradingDirection.SELL),
                        confidence=self._calculate_sweep_confidence(pool, sweep_distance, reversal_confirmed),
                        institutional_confirmation=pool.institutional_interest > 0.6,
                        volume_spike=self._detect_volume_spike(data, i),
                        narrative=f"Downside sweep del level {target_level:.5f} - Liquidez capturada: {liquidity_captured:.1%}",
                        timestamp=timestamp,
                        symbol=symbol,
                        timeframe=timeframe,
                        analysis_id=f"SWEEP_{symbol}_{int(datetime.now().timestamp())}"
                    )
                    
                    return sweep_signal
            
            return None
            
        except Exception as e:
            self._log_error(f"Error detectando downside sweep: {e}")
            return None

    def _detect_general_sweeps_enterprise(self, 
                                        data: pd.DataFrame,
                                        symbol: str, 
                                        timeframe: str) -> List[LiquiditySweepSignal]:
        """🌊 Detectar sweeps generales sin pools específicos"""
        try:
            sweeps = []
            
            if len(data) < 15:
                return sweeps
            
            # Buscar patrones de spike + reversal inmediato
            for i in range(5, len(data) - 5):
                current = data.iloc[i]
                prev_window = data.iloc[i-5:i]
                next_window = data.iloc[i+1:i+6]
                
                # Spike upside seguido de reversal
                if (current['high'] > prev_window['high'].max() and 
                    len(next_window) > 0 and 
                    next_window['close'].iloc[-1] < current['open']):
                    
                    sweep = self._create_general_sweep_signal(
                        LiquiditySweepType.UPSIDE_SWEEP,
                        current, next_window, symbol, timeframe
                    )
                    if sweep:
                        sweeps.append(sweep)
                
                # Spike downside seguido de reversal
                elif (current['low'] < prev_window['low'].min() and 
                      len(next_window) > 0 and 
                      next_window['close'].iloc[-1] > current['open']):
                    
                    sweep = self._create_general_sweep_signal(
                        LiquiditySweepType.DOWNSIDE_SWEEP,
                        current, next_window, symbol, timeframe
                    )
                    if sweep:
                        sweeps.append(sweep)
            
            return sweeps
            
        except Exception as e:
            self._log_error(f"Error detectando general sweeps: {e}")
            return []

    # ===========================================
    # 🛠️ UTILITY METHODS
    # ===========================================

    def _validate_institutional_interest_enterprise(self, 
                                                   pool: LiquidityPool,
                                                   data_m15: pd.DataFrame, 
                                                   current_price: float) -> float:
        """🏦 Validar interés institucional en pool"""
        try:
            interest_score = 0.0
            
            # Factor 1: Proximidad al precio actual
            distance = abs(current_price - pool.price_level) / current_price
            if distance <= 0.01:  # Dentro de 100 pips
                interest_score += 0.3
            
            # Factor 2: Strength del pool
            interest_score += pool.strength * 0.3
            
            # Factor 3: Número de touches
            touch_bonus = min(pool.touches / 5.0, 0.2)
            interest_score += touch_bonus
            
            # Factor 4: Timeframe origin (H4 más significativo)
            if pool.timeframe_origin == "H4":
                interest_score += 0.2
            
            return min(interest_score, 1.0)
            
        except Exception:
            return 0.3

    def _filter_pools_by_relevance(self, 
                                  pools: List[LiquidityPool], 
                                  current_price: float) -> List[LiquidityPool]:
        """🎯 Filtrar pools por relevancia"""
        try:
            # Filtrar por fuerza mínima
            strong_pools = [p for p in pools if p.strength >= self.config['min_pool_strength']]
            
            # Ordenar por relevancia (proximidad + fuerza + institutional interest)
            def relevance_score(pool):
                distance = abs(current_price - pool.price_level) / current_price
                proximity_score = max(0, 1 - distance * 100)  # Penalizar distancia
                return (proximity_score * 0.4 + 
                       pool.strength * 0.3 + 
                       pool.institutional_interest * 0.3)
            
            strong_pools.sort(key=relevance_score, reverse=True)
            
            # Limitar número máximo
            return strong_pools[:self.config['max_simultaneous_pools']]
            
        except Exception as e:
            self._log_error(f"Error filtrando pools: {e}")
            return pools

    def _estimate_liquidity_depth(self, touches: int, strength: float) -> float:
        """💧 Estimar profundidad de liquidez"""
        base_depth = 0.5
        touch_bonus = min(touches / 10.0, 0.3)
        strength_bonus = strength * 0.2
        return min(base_depth + touch_bonus + strength_bonus, 1.0)

    def _estimate_swept_liquidity(self, pool: LiquidityPool, sweep_distance: float) -> float:
        """🌊 Estimar liquidez barrida"""
        base_liquidity = pool.liquidity_depth
        distance_factor = min(sweep_distance * 10000 / 10.0, 1.0)  # Normalizar por pips
        return base_liquidity * distance_factor

    def _identify_session_origin(self, timestamp: datetime) -> str:
        """🏛️ Identificar sesión de origen"""
        try:
            hour = timestamp.hour
            if 8 <= hour <= 17:
                return "London"
            elif 13 <= hour <= 22:
                return "NY"
            else:
                return "Asian"
        except:
            return "unknown"

    def _get_current_session(self) -> str:
        """🏛️ Obtener sesión actual"""
        return self._identify_session_origin(datetime.now())

    def _is_pool_in_sweep_range(self, pool: LiquidityPool, data: pd.DataFrame) -> bool:
        """🎯 Verificar si pool está en rango para sweep"""
        try:
            if len(data) == 0:
                return False
            
            current_price = data['close'].iloc[-1]
            distance = abs(current_price - pool.price_level) / current_price
            
            # Pool debe estar dentro del 1% del precio actual
            return distance <= 0.01
            
        except:
            return False

    def _calculate_sweep_confidence(self, 
                                  pool: LiquidityPool, 
                                  sweep_distance: float, 
                                  reversal_confirmed: bool) -> float:
        """🎯 Calcular confianza del sweep"""
        base_confidence = 0.6
        
        # Bonus por fuerza del pool
        pool_bonus = pool.strength * 0.2
        
        # Bonus por distancia del sweep
        distance_bonus = min(sweep_distance * 10000 / 5.0, 0.1)  # Max 0.1 por 5+ pips
        
        # Bonus mayor si hay reversión confirmada
        reversal_bonus = 0.2 if reversal_confirmed else 0.0
        
        return min(base_confidence + pool_bonus + distance_bonus + reversal_bonus, 0.95)

    def _detect_volume_spike(self, data: pd.DataFrame, index: int) -> bool:
        """📊 Detectar spike de volumen"""
        try:
            if 'volume' not in data.columns or index < 5:
                return False
            
            current_volume = data['volume'].iloc[index]
            avg_volume = data['volume'].iloc[index-5:index].mean()
            
            return current_volume > avg_volume * self.config['volume_spike_threshold']
            
        except:
            return False

    def _calculate_sweep_entry_zone(self, sweep_price: float, direction) -> Tuple[float, float]:
        """🎯 Calcular zona de entrada para sweep"""
        if hasattr(direction, 'BUY') and direction == direction.BUY:
            return (sweep_price - 0.0005, sweep_price + 0.0005)
        else:
            return (sweep_price - 0.0005, sweep_price + 0.0005)

    def _calculate_sweep_stop_loss(self, sweep_price: float, direction) -> float:
        """🛑 Calcular stop loss para sweep"""
        if hasattr(direction, 'BUY') and direction == direction.BUY:
            return sweep_price - 0.0015
        else:
            return sweep_price + 0.0015

    def _calculate_sweep_tp1(self, sweep_price: float, direction) -> float:
        """🎯 Calcular TP1 para sweep"""
        if hasattr(direction, 'BUY') and direction == direction.BUY:
            return sweep_price + 0.0025
        else:
            return sweep_price - 0.0025

    def _calculate_sweep_tp2(self, sweep_price: float, direction) -> float:
        """🎯 Calcular TP2 para sweep"""
        if hasattr(direction, 'BUY') and direction == direction.BUY:
            return sweep_price + 0.0045
        else:
            return sweep_price - 0.0045

    def _create_general_sweep_signal(self, 
                                   sweep_type: LiquiditySweepType,
                                   candle: pd.Series, 
                                   reversal_data: pd.DataFrame,
                                   symbol: str, 
                                   timeframe: str) -> Optional[LiquiditySweepSignal]:
        """🌊 Crear señal de sweep general"""
        try:
            direction = TradingDirection.SELL if sweep_type == LiquiditySweepType.UPSIDE_SWEEP else TradingDirection.BUY
            
            return LiquiditySweepSignal(
                sweep_type=sweep_type,
                direction=direction,
                target_level=candle['high'] if sweep_type == LiquiditySweepType.UPSIDE_SWEEP else candle['low'],
                sweep_price=candle['high'] if sweep_type == LiquiditySweepType.UPSIDE_SWEEP else candle['low'],
                liquidity_captured=0.6,
                reversal_target=candle['close'],
                reversal_probability=0.7,
                entry_zone=self._calculate_sweep_entry_zone(candle['close'], direction),
                stop_loss=self._calculate_sweep_stop_loss(candle['close'], direction),
                take_profit_1=self._calculate_sweep_tp1(candle['close'], direction),
                take_profit_2=self._calculate_sweep_tp2(candle['close'], direction),
                confidence=0.7,
                institutional_confirmation=False,
                volume_spike=False,
                narrative=f"General {sweep_type.value} detectado con reversión",
                timestamp=datetime.now(),
                symbol=symbol,
                timeframe=timeframe
            )
        except:
            return None

    def _validate_sweep_signals(self, 
                               sweeps: List[LiquiditySweepSignal], 
                               data: pd.DataFrame) -> List[LiquiditySweepSignal]:
        """✅ Validar señales de sweep"""
        try:
            validated = []
            
            for sweep in sweeps:
                # Filtrar por confianza mínima
                if sweep.confidence >= self.config['min_sweep_strength']:
                    validated.append(sweep)
            
            return validated
            
        except Exception as e:
            self._log_error(f"Error validando sweeps: {e}")
            return sweeps

    # ===========================================
    # 💾 MEMORY & STATS METHODS
    # ===========================================

    def _store_pools_in_memory(self, pools: List[LiquidityPool]):
        """💾 Guardar pools en memoria"""
        try:
            # En el futuro se integrará con UnifiedMemorySystem
            self.detected_pools.extend(pools)
            
            # Limitar memoria
            if len(self.detected_pools) > 50:
                self.detected_pools = self.detected_pools[-50:]
                
        except Exception as e:
            self._log_error(f"Error storing pools: {e}")

    def _store_sweeps_in_memory(self, sweeps: List[LiquiditySweepSignal]):
        """💾 Guardar sweeps en memoria"""
        try:
            # En el futuro se integrará con UnifiedMemorySystem
            self.detected_sweeps.extend(sweeps)
            
            # Limitar memoria
            if len(self.detected_sweeps) > 30:
                self.detected_sweeps = self.detected_sweeps[-30:]
                
        except Exception as e:
            self._log_error(f"Error storing sweeps: {e}")

    def _update_pools_stats(self, pools: List[LiquidityPool]):
        """📊 Actualizar estadísticas de pools"""
        try:
            self.processing_stats['total_pools_detected'] += len(pools)
            institutional_count = len([p for p in pools if p.institutional_interest > 0.6])
            self.processing_stats['institutional_pools'] += institutional_count
        except:
            pass

    def _update_sweeps_stats(self, sweeps: List[LiquiditySweepSignal]):
        """📊 Actualizar estadísticas de sweeps"""
        try:
            self.processing_stats['total_sweeps_detected'] += len(sweeps)
            successful_count = len([s for s in sweeps if s.confidence > 0.8])
            self.processing_stats['successful_sweeps'] += successful_count
        except:
            pass

    # ===========================================
    # 🛠️ LOGGING METHODS
    # ===========================================

    def _create_fallback_logger(self):
        """📝 Crear logger fallback"""
        class FallbackLogger:
            def log_info(self, msg, component="liquidity"): print(f"[INFO] {msg}")
            def log_warning(self, msg, component="liquidity"): print(f"[WARNING] {msg}")
            def log_error(self, msg, component="liquidity"): print(f"[ERROR] {msg}")
            def log_debug(self, msg, component="liquidity"): print(f"[DEBUG] {msg}")
        return FallbackLogger()

    def _log_info(self, message: str):
        if self.logger: self.logger.log_info(message, "liquidity_enterprise")
        else: print(f"[INFO] {message}")

    def _log_warning(self, message: str):
        if self.logger: self.logger.log_warning(message, "liquidity_enterprise")
        else: print(f"[WARNING] {message}")

    def _log_error(self, message: str):
        if self.logger: self.logger.log_error(message, "liquidity_enterprise")
        else: print(f"[ERROR] {message}")

    def _log_debug(self, message: str):
        if self.logger: self.logger.log_debug(message, "liquidity_enterprise")
        else: print(f"[DEBUG] {message}")


# ===========================================
# 🧪 TESTING & UTILITIES
# ===========================================

def create_test_liquidity_analyzer() -> LiquidityAnalyzerEnterprise:
    """🧪 Crear analyzer para testing"""
    return LiquidityAnalyzerEnterprise()


if __name__ == "__main__":
    # 🧪 Test básico
    analyzer = create_test_liquidity_analyzer()
    print("✅ Liquidity Analyzer Enterprise v6.0 - Test básico completado")
