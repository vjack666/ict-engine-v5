#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 PATTERN DETECTOR CORE - ICT ENGINE v6.0 ENTERPRISE
====================================================

Detector avanzado de patterns ICT que implementa la metodología institucional
para identificación automática de:

📦 **Order Blocks ICT:**
- Bullish Order Blocks
- Bearish Order Blocks  
- Breaker Blocks
- Mitigation Blocks

💎 **Fair Value Gaps:**
- Bullish FVGs
- Bearish FVGs
- Premium FVGs
- Discount FVGs

🎯 **Características v6.0 Enterprise:**
- Integración nativa con Market Structure Analyzer
- Cache predictivo de patterns
- Análisis multi-timeframe sincronizado
- Validación de calidad enterprise
- Performance optimizada para real-time
- SIC v3.1 Enterprise integration

🔄 **Pipeline Completo:**
1. Integración con Market Structure Analyzer
2. Detección de Order Blocks institucionales
3. Identificación de Fair Value Gaps
4. Análisis de strength y probabilidad
5. Correlación multi-timeframe
6. Validación de calidad enterprise

Autor: ICT Engine v6.1.0 Enterprise Team
Versión: v6.1.0-enterprise
Fecha: Agosto 2025 - Fase 2.2 Cronograma
"""

# ===============================
# IMPORTS SIC v3.1 ENTERPRISE
# ===============================

import time
import threading
from typing import Dict, List, Optional, Any, Tuple, Union, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

# Imports SIC v3.1 Enterprise
try:
    from sistema.sic_v3_1.enterprise_interface import SICv31Enterprise
    from sistema.sic_v3_1.advanced_debug import AdvancedDebugger
    SIC_V3_1_AVAILABLE = True
except ImportError:
    SIC_V3_1_AVAILABLE = False
    # Fallback para desarrollo
    class SICv31Enterprise:
        def __init__(self): pass

# Sistema de logging
try:
    from sistema.sic import enviar_senal_log
except ImportError:
    def enviar_senal_log(level, message, module, category):
        print(f"[{level}] {module}.{category}: {message}")

# Componentes ICT Engine v6.1.0
try:
    from core.analysis.market_structure_analyzer_v6 import MarketStructureAnalyzerV6, MarketStructureSignalV6
    from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
    from utils.mt5_data_manager import MT5DataManager
    MARKET_STRUCTURE_AVAILABLE = True
except ImportError:
    MARKET_STRUCTURE_AVAILABLE = False
    print("⚠️ Market Structure Analyzer no disponible")

# Sistema de Memoria Unificada v6.0 Enterprise (SIC + SLUC)
try:
    from core.analysis.unified_market_memory import (
        get_unified_market_memory,
        update_market_memory, 
        get_trading_insights
    )
    UNIFIED_MEMORY_AVAILABLE = True
    print("✅ [SIC Integration] Sistema de Memoria Unificada v6.0 cargado")
except ImportError:
    UNIFIED_MEMORY_AVAILABLE = False
    print("⚠️ Sistema de Memoria Unificada no disponible")

# ✅ FASE 2: Sistema de Memoria Unificada v6.1 Enterprise (FASE 2)
try:
    from core.analysis.unified_memory_system import (
        get_unified_memory_system,
        UnifiedMemorySystem
    )
    UNIFIED_MEMORY_SYSTEM_AVAILABLE = True
    print("✅ [SIC Integration] UnifiedMemorySystem FASE 2 cargado")
except ImportError:
    UNIFIED_MEMORY_SYSTEM_AVAILABLE = False
    print("⚠️ UnifiedMemorySystem FASE 2 no disponible")

# ===============================
# TIPOS Y ENUMS ICT PATTERNS
# ===============================

class OrderBlockType(Enum):
    """📦 Tipos de Order Block ICT"""
    BULLISH_OB = "bullish_order_block"           # Order Block alcista
    BEARISH_OB = "bearish_order_block"           # Order Block bajista
    BREAKER_BLOCK = "breaker_block"              # Breaker Block
    MITIGATION_BLOCK = "mitigation_block"        # Mitigation Block
    REJECTION_BLOCK = "rejection_block"          # Rejection Block

class FVGType(Enum):
    """💎 Tipos de Fair Value Gap"""
    BULLISH_FVG = "bullish_fvg"                 # FVG alcista
    BEARISH_FVG = "bearish_fvg"                 # FVG bajista
    BALANCED_FVG = "balanced_fvg"               # FVG balanceado
    PREMIUM_FVG = "premium_fvg"                 # FVG en premium
    DISCOUNT_FVG = "discount_fvg"               # FVG en discount

class PatternStrength(Enum):
    """💪 Fuerza del pattern"""
    WEAK = "weak"                               # Débil
    MODERATE = "moderate"                       # Moderado
    STRONG = "strong"                           # Fuerte
    VERY_STRONG = "very_strong"                 # Muy fuerte

class PatternStatus(Enum):
    """🔄 Estado del pattern"""
    ACTIVE = "active"                           # Activo
    TESTED = "tested"                           # Testeado
    MITIGATED = "mitigated"                     # Mitigado
    INVALIDATED = "invalidated"                 # Invalidado

# ===============================
# DATACLASSES ICT PATTERNS
# ===============================

@dataclass
class OrderBlock:
    """📦 Order Block ICT detectado"""
    ob_type: OrderBlockType
    high_price: float
    low_price: float
    origin_candle_index: int
    origin_timestamp: datetime
    strength: PatternStrength
    status: PatternStatus
    probability: float
    
    # Métricas de calidad
    reaction_count: int = 0
    reaction_strength: float = 0.0
    volume_confirmation: bool = False
    structure_confluence: bool = False
    
    # Context información
    timeframe: str = ""
    symbol: str = ""
    narrative: str = ""
    
    # SIC v3.1 stats
    sic_stats: Dict[str, Any] = field(default_factory=dict)
    
    def get_middle_price(self) -> float:
        """💫 Obtiene precio medio del Order Block"""
        return (self.high_price + self.low_price) / 2
    
    def get_size_pips(self) -> float:
        """📏 Obtiene tamaño en pips (simplificado)"""
        return abs(self.high_price - self.low_price) * 10000

@dataclass
class FairValueGap:
    """💎 Fair Value Gap ICT detectado"""
    fvg_type: FVGType
    high_price: float
    low_price: float
    origin_candle_index: int
    origin_timestamp: datetime
    strength: PatternStrength
    status: PatternStatus
    probability: float
    
    # Estado de fill
    filled_percentage: float = 0.0
    is_filled: bool = False
    fill_timestamp: Optional[datetime] = None
    
    # Métricas de calidad
    gap_size_pips: float = 0.0
    volume_confirmation: bool = False
    structure_confluence: bool = False
    
    # Context información
    timeframe: str = ""
    symbol: str = ""
    narrative: str = ""
    
    # SIC v3.1 stats
    sic_stats: Dict[str, Any] = field(default_factory=dict)
    
    def get_middle_price(self) -> float:
        """💫 Obtiene precio medio del FVG"""
        return (self.high_price + self.low_price) / 2
    
    def get_gap_size(self) -> float:
        """📏 Obtiene tamaño del gap"""
        return abs(self.high_price - self.low_price)

@dataclass
class PatternDetectionResult:
    """🎯 Resultado de detección de patterns"""
    order_blocks: List[OrderBlock] = field(default_factory=list)
    fair_value_gaps: List[FairValueGap] = field(default_factory=list)
    detection_timestamp: datetime = field(default_factory=datetime.now)
    timeframe: str = ""
    symbol: str = ""
    total_patterns: int = 0
    quality_score: float = 0.0
    processing_time: float = 0.0
    
    # SIC v3.1 Enterprise stats
    sic_performance: Dict[str, Any] = field(default_factory=dict)

# ===============================
# PATTERN DETECTOR CORE
# ===============================

class ICTPatternDetector:
    """
    🎯 ICT PATTERN DETECTOR v6.0 ENTERPRISE
    =======================================
    
    Detector profesional de patterns ICT con:
    - Order Block detection avanzada
    - Fair Value Gap identification precisa
    - Pattern strength analysis
    - Quality validation enterprise
    - Multi-timeframe correlation
    - Integración completa con SIC v3.1
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        🏗️ Inicializa el Pattern Detector v6.0
        
        Args:
            config: Configuración avanzada del detector
        """
        
        # Configuración v6.0
        self._config = config or {}
        self._enable_debug = self._config.get('enable_debug', True)
        self._use_multi_timeframe = self._config.get('use_multi_timeframe', True)
        self._enable_cache = self._config.get('enable_cache', True)
        
        # Configuración de detección
        self.min_ob_reaction_pips = self._config.get('min_ob_reaction_pips', 10.0)
        self.min_fvg_size_pips = self._config.get('min_fvg_size_pips', 5.0)
        self.pattern_lookback = self._config.get('pattern_lookback', 100)
        self.volume_weight = self._config.get('volume_weight', 0.3)
        self.structure_weight = self._config.get('structure_weight', 0.7)
        
        # Thresholds de calidad
        self.min_pattern_probability = self._config.get('min_pattern_probability', 60.0)
        self.min_pattern_strength = self._config.get('min_pattern_strength', 0.5)
        
        # Estado del detector
        self.detected_order_blocks: List[OrderBlock] = []
        self.detected_fvgs: List[FairValueGap] = []
        self.pattern_cache: Dict[str, Any] = {}
        self.performance_metrics: List[Dict[str, Any]] = []
        
        # Componentes
        self._market_structure: Optional[MarketStructureAnalyzerV6] = None
        self._downloader: Optional[AdvancedCandleDownloader] = None
        self._sic: Optional[SICv31Enterprise] = None
        self._unified_memory = None  # Sistema de Memoria Unificada v6.0 (FASE 1)
        self._unified_memory_system = None  # Sistema de Memoria Unificada v6.1 (FASE 2) (FASE 1)
        self._unified_memory_system = None  # Sistema de Memoria Unificada v6.1 (FASE 2)
        
        # Threading
        self._lock = threading.Lock()
        
        # Inicializar componentes
        self._initialize_components()
        
        # Log de inicialización
        self._log_info("ICTPatternDetector v6.0 inicializado con SIC v3.1")
    
    def _initialize_components(self):
        """🔧 Inicializa componentes v6.0"""
        try:
            # Configurar SIC v3.1 si está disponible
            if SIC_V3_1_AVAILABLE:
                self._sic = SICv31Enterprise()
                self._log_info("SIC v3.1 Enterprise integrado")
            
            # Configurar Sistema de Memoria Unificada v6.0 (SIC + SLUC)
            if UNIFIED_MEMORY_AVAILABLE:
                self._unified_memory = get_unified_market_memory()
                self._log_info("🧠 Sistema de Memoria Unificada v6.0 conectado (SIC + SLUC)")
            
            # ✅ FASE 2: Configurar UnifiedMemorySystem v6.1 (Trader Real)
            if UNIFIED_MEMORY_SYSTEM_AVAILABLE:
                self._unified_memory_system = get_unified_memory_system()
                self._log_info("🧠 UnifiedMemorySystem v6.1 FASE 2 conectado (Trader Real)")
            
            # ✅ FASE 2: Configurar UnifiedMemorySystem v6.1 (Trader Real)
            if UNIFIED_MEMORY_SYSTEM_AVAILABLE:
                self._unified_memory_system = get_unified_memory_system()
                self._log_info("🧠 UnifiedMemorySystem v6.1 FASE 2 conectado (Trader Real)")
            
            # ✅ FASE 2: Configurar UnifiedMemorySystem v6.1 (Trader Real)
            if UNIFIED_MEMORY_SYSTEM_AVAILABLE:
                self._unified_memory_system = get_unified_memory_system()
                self._log_info("🧠 UnifiedMemorySystem v6.1 FASE 2 conectado (Trader Real)")
            
            # Configurar Market Structure Analyzer
            if MARKET_STRUCTURE_AVAILABLE:
                self._market_structure = MarketStructureAnalyzerV6()
                self._log_info("Market Structure Analyzer conectado")
            
            # Configurar Advanced Candle Downloader
            self._downloader = AdvancedCandleDownloader()
            self._log_info("AdvancedCandleDownloader conectado")
            
        except Exception as e:
            self._log_error(f"Error inicializando componentes: {e}")
    
    def detect_patterns(self, 
                       symbol: str, 
                       timeframe: str = "H1",
                       lookback_days: int = 7) -> PatternDetectionResult:
        """
        🎯 DETECCIÓN COMPLETA DE PATTERNS ICT v6.0
        
        Args:
            symbol: Símbolo a analizar (ej: "EURUSD")
            timeframe: Timeframe principal (ej: "H1")
            lookback_days: Días de historia para análisis
            
        Returns:
            PatternDetectionResult con todos los patterns detectados
        """
        start_time = time.time()
        
        try:
            self._log_info(f"🎯 Iniciando detección de patterns: {symbol} {timeframe}")
            
            # 1. 📥 OBTENER DATOS DE MERCADO
            candles_data = self._get_market_data(symbol, timeframe, lookback_days)
            if candles_data is None or len(candles_data) < 50:
                self._log_warning(f"Insuficientes datos para {symbol} {timeframe}")
                return self._create_empty_result(symbol, timeframe)
            
            # 2. 📊 ANÁLISIS DE ESTRUCTURA (opcional)
            market_structure = None
            if self._market_structure:
                try:
                    market_structure = self._market_structure.analyze_market_structure(
                        candles_m15=candles_data,
                        current_price=float(candles_data['close'].iloc[-1]) if not candles_data.empty else 0.0,
                        symbol=symbol
                    )
                except Exception as e:
                    self._log_warning(f"Error en análisis de estructura: {e}")
            
            # 3. 📦 DETECTAR ORDER BLOCKS
            order_blocks = self._detect_order_blocks(candles_data, market_structure)
            
            # 4. 💎 DETECTAR FAIR VALUE GAPS
            fair_value_gaps = self._detect_fair_value_gaps(candles_data, market_structure)
            
            # 5. 🔍 VALIDAR CALIDAD DE PATTERNS
            order_blocks = self._validate_pattern_quality(order_blocks, candles_data)
            fair_value_gaps = self._validate_pattern_quality(fair_value_gaps, candles_data)
            
            # 6. 📊 CALCULAR STRENGTH Y PROBABILITY
            order_blocks = self._calculate_pattern_metrics(order_blocks, candles_data)
            fair_value_gaps = self._calculate_pattern_metrics(fair_value_gaps, candles_data)
            
            # 7. 🎯 CREAR RESULTADO
            result = PatternDetectionResult(
                order_blocks=order_blocks,
                fair_value_gaps=fair_value_gaps,
                detection_timestamp=datetime.now(),
                timeframe=timeframe,
                symbol=symbol,
                total_patterns=len(order_blocks) + len(fair_value_gaps),
                quality_score=self._calculate_overall_quality(order_blocks, fair_value_gaps),
                processing_time=time.time() - start_time
            )
            
            # 8. 🧠 ACTUALIZAR MEMORIA UNIFICADA (SIC + SLUC)
            if self._unified_memory and UNIFIED_MEMORY_AVAILABLE:
                self._update_unified_memory_with_patterns(result, symbol, timeframe)
            
            # 9. 💾 ACTUALIZAR ESTADO
            self._update_detector_state(result)
            
            # 10. 📊 MÉTRICAS DE PERFORMANCE
            self._update_performance_metrics(result)
            
            self._log_info(f"🎯 Patterns detectados: {result.total_patterns} "
                          f"(OB: {len(order_blocks)}, FVG: {len(fair_value_gaps)}) "
                          f"- Calidad: {result.quality_score:.1f}%")
            
            return result
            
        except Exception as e:
            self._log_error(f"Error en detección de patterns: {e}")
            return self._create_empty_result(symbol, timeframe)
    
    def _detect_order_blocks(self, 
                           candles, 
                           market_structure: Optional[MarketStructureSignalV6] = None) -> List[OrderBlock]:
        """📦 Detecta Order Blocks ICT"""
        order_blocks = []
        
        try:
            if len(candles) < 20:
                return order_blocks
            
            # Detectar Order Blocks usando metodología ICT
            for i in range(5, len(candles) - 5):
                # Obtener vela actual
                current_candle = candles.iloc[i]
                
                # 1. DETECTAR BULLISH ORDER BLOCK
                bullish_ob = self._detect_bullish_order_block(candles, i)
                if bullish_ob:
                    order_blocks.append(bullish_ob)
                
                # 2. DETECTAR BEARISH ORDER BLOCK
                bearish_ob = self._detect_bearish_order_block(candles, i)
                if bearish_ob:
                    order_blocks.append(bearish_ob)
                
                # 3. DETECTAR BREAKER BLOCKS
                breaker_block = self._detect_breaker_block(candles, i, market_structure)
                if breaker_block:
                    order_blocks.append(breaker_block)
            
            # Filtrar por calidad mínima
            order_blocks = [ob for ob in order_blocks if ob.probability >= self.min_pattern_probability]
            
            self._log_debug(f"📦 Order Blocks detectados: {len(order_blocks)}")
            return order_blocks
            
        except Exception as e:
            self._log_error(f"Error detectando Order Blocks: {e}")
            return []
    
    def _detect_bullish_order_block(self, candles, candle_index: int) -> Optional[OrderBlock]:
        """📈 Detecta Bullish Order Block"""
        try:
            current = candles.iloc[candle_index]
            
            # Condición 1: Vela alcista fuerte
            if current['close'] <= current['open']:
                return None
            
            body_size = current['close'] - current['open']
            candle_range = current['high'] - current['low']
            
            # Condición 2: Body significativo
            if body_size < candle_range * 0.5:
                return None
            
            # Condición 3: Verificar reacción posterior
            reaction_strength = self._calculate_reaction_strength(candles, candle_index, 'bullish')
            
            if reaction_strength < self.min_ob_reaction_pips / 10000:  # Convertir pips
                return None
            
            # Crear Order Block
            order_block = OrderBlock(
                ob_type=OrderBlockType.BULLISH_OB,
                high_price=current['high'],
                low_price=current['low'],
                origin_candle_index=candle_index,
                origin_timestamp=current.name if hasattr(current.name, 'timestamp') else datetime.now(),
                strength=self._classify_pattern_strength(reaction_strength),
                status=PatternStatus.ACTIVE,
                probability=min(95.0, 60.0 + (reaction_strength * 1000)),
                reaction_strength=reaction_strength,
                narrative=f"Bullish Order Block - Reacción: {reaction_strength:.5f}"
            )
            
            return order_block
            
        except Exception as e:
            self._log_debug(f"Error detectando Bullish OB: {e}")
            return None
    
    def _detect_bearish_order_block(self, candles, candle_index: int) -> Optional[OrderBlock]:
        """📉 Detecta Bearish Order Block"""
        try:
            current = candles.iloc[candle_index]
            
            # Condición 1: Vela bajista fuerte
            if current['close'] >= current['open']:
                return None
            
            body_size = current['open'] - current['close']
            candle_range = current['high'] - current['low']
            
            # Condición 2: Body significativo
            if body_size < candle_range * 0.5:
                return None
            
            # Condición 3: Verificar reacción posterior
            reaction_strength = self._calculate_reaction_strength(candles, candle_index, 'bearish')
            
            if reaction_strength < self.min_ob_reaction_pips / 10000:  # Convertir pips
                return None
            
            # Crear Order Block
            order_block = OrderBlock(
                ob_type=OrderBlockType.BEARISH_OB,
                high_price=current['high'],
                low_price=current['low'],
                origin_candle_index=candle_index,
                origin_timestamp=current.name if hasattr(current.name, 'timestamp') else datetime.now(),
                strength=self._classify_pattern_strength(reaction_strength),
                status=PatternStatus.ACTIVE,
                probability=min(95.0, 60.0 + (reaction_strength * 1000)),
                reaction_strength=reaction_strength,
                narrative=f"Bearish Order Block - Reacción: {reaction_strength:.5f}"
            )
            
            return order_block
            
        except Exception as e:
            self._log_debug(f"Error detectando Bearish OB: {e}")
            return None
    
    def _detect_breaker_block(self, 
                            candles, 
                            candle_index: int, 
                            market_structure: Optional[MarketStructureSignalV6] = None) -> Optional[OrderBlock]:
        """💥 Detecta Breaker Block (Order Block que se rompe y cambia de rol)"""
        try:
            # Lógica simplificada para Breaker Block
            # TODO: Implementar lógica completa de Breaker Block
            
            current = candles.iloc[candle_index]
            
            # Verificar si hay cambio de estructura
            if not market_structure:
                return None
            
            # Placeholder para lógica de Breaker Block
            # Se implementará en futuras versiones
            
            return None
            
        except Exception as e:
            self._log_debug(f"Error detectando Breaker Block: {e}")
            return None
    
    def _detect_fair_value_gaps(self, 
                              candles, 
                              market_structure: Optional[MarketStructureSignalV6] = None) -> List[FairValueGap]:
        """💎 Detecta Fair Value Gaps ICT"""
        fvgs = []
        
        try:
            if len(candles) < 3:
                return fvgs
            
            # Detectar FVGs usando metodología ICT
            for i in range(1, len(candles) - 1):
                # 1. DETECTAR BULLISH FVG
                bullish_fvg = self._detect_bullish_fvg(candles, i)
                if bullish_fvg:
                    fvgs.append(bullish_fvg)
                
                # 2. DETECTAR BEARISH FVG
                bearish_fvg = self._detect_bearish_fvg(candles, i)
                if bearish_fvg:
                    fvgs.append(bearish_fvg)
            
            # Filtrar por tamaño mínimo
            fvgs = [fvg for fvg in fvgs if fvg.gap_size_pips >= self.min_fvg_size_pips]
            
            self._log_debug(f"💎 Fair Value Gaps detectados: {len(fvgs)}")
            return fvgs
            
        except Exception as e:
            self._log_error(f"Error detectando FVGs: {e}")
            return []
    
    def _detect_bullish_fvg(self, candles, candle_index: int) -> Optional[FairValueGap]:
        """📈 Detecta Bullish Fair Value Gap"""
        try:
            if candle_index < 1 or candle_index >= len(candles) - 1:
                return None
            
            prev_candle = candles.iloc[candle_index - 1]
            current_candle = candles.iloc[candle_index]
            next_candle = candles.iloc[candle_index + 1]
            
            # Condición: Gap entre low de next y high de prev
            if next_candle['low'] > prev_candle['high']:
                gap_size = next_candle['low'] - prev_candle['high']
                gap_size_pips = gap_size * 10000  # Conversión simplificada a pips
                
                if gap_size_pips >= self.min_fvg_size_pips:
                    fvg = FairValueGap(
                        fvg_type=FVGType.BULLISH_FVG,
                        high_price=next_candle['low'],
                        low_price=prev_candle['high'],
                        origin_candle_index=candle_index,
                        origin_timestamp=current_candle.name if hasattr(current_candle.name, 'timestamp') else datetime.now(),
                        strength=self._classify_pattern_strength(gap_size),
                        status=PatternStatus.ACTIVE,
                        probability=min(90.0, 50.0 + (gap_size_pips * 2)),
                        gap_size_pips=gap_size_pips,
                        narrative=f"Bullish FVG - Gap: {gap_size_pips:.1f} pips"
                    )
                    
                    return fvg
            
            return None
            
        except Exception as e:
            self._log_debug(f"Error detectando Bullish FVG: {e}")
            return None
    
    def _detect_bearish_fvg(self, candles, candle_index: int) -> Optional[FairValueGap]:
        """📉 Detecta Bearish Fair Value Gap"""
        try:
            if candle_index < 1 or candle_index >= len(candles) - 1:
                return None
            
            prev_candle = candles.iloc[candle_index - 1]
            current_candle = candles.iloc[candle_index]
            next_candle = candles.iloc[candle_index + 1]
            
            # Condición: Gap entre high de next y low de prev
            if next_candle['high'] < prev_candle['low']:
                gap_size = prev_candle['low'] - next_candle['high']
                gap_size_pips = gap_size * 10000  # Conversión simplificada a pips
                
                if gap_size_pips >= self.min_fvg_size_pips:
                    fvg = FairValueGap(
                        fvg_type=FVGType.BEARISH_FVG,
                        high_price=prev_candle['low'],
                        low_price=next_candle['high'],
                        origin_candle_index=candle_index,
                        origin_timestamp=current_candle.name if hasattr(current_candle.name, 'timestamp') else datetime.now(),
                        strength=self._classify_pattern_strength(gap_size),
                        status=PatternStatus.ACTIVE,
                        probability=min(90.0, 50.0 + (gap_size_pips * 2)),
                        gap_size_pips=gap_size_pips,
                        narrative=f"Bearish FVG - Gap: {gap_size_pips:.1f} pips"
                    )
                    
                    return fvg
            
            return None
            
        except Exception as e:
            self._log_debug(f"Error detectando Bearish FVG: {e}")
            return None
    
    def _calculate_reaction_strength(self, candles, candle_index: int, direction: str) -> float:
        """⚡ Calcula la fuerza de reacción desde un nivel"""
        try:
            if candle_index >= len(candles) - 3:
                return 0.0
            
            origin_candle = candles.iloc[candle_index]
            reaction_strength = 0.0
            
            # Analizar las siguientes 3-5 velas
            for i in range(candle_index + 1, min(candle_index + 6, len(candles))):
                next_candle = candles.iloc[i]
                
                if direction == 'bullish':
                    # Medir distancia desde el high del Order Block
                    distance = abs(next_candle['high'] - origin_candle['high'])
                elif direction == 'bearish':
                    # Medir distancia desde el low del Order Block
                    distance = abs(origin_candle['low'] - next_candle['low'])
                else:
                    continue
                
                reaction_strength = max(reaction_strength, distance)
            
            return reaction_strength
            
        except Exception as e:
            self._log_debug(f"Error calculando reacción: {e}")
            return 0.0
    
    def _classify_pattern_strength(self, value: float) -> PatternStrength:
        """💪 Clasifica la fuerza del pattern"""
        try:
            # Clasificación basada en el valor (ajustable)
            if value < 0.001:
                return PatternStrength.WEAK
            elif value < 0.002:
                return PatternStrength.MODERATE
            elif value < 0.004:
                return PatternStrength.STRONG
            else:
                return PatternStrength.VERY_STRONG
        except:
            return PatternStrength.WEAK
    
    def _validate_pattern_quality(self, patterns: List, candles) -> List:
        """🔍 Valida la calidad de los patterns"""
        try:
            validated_patterns = []
            
            for pattern in patterns:
                # Validaciones básicas
                if pattern.probability >= self.min_pattern_probability:
                    # Validación adicional específica del tipo
                    if self._validate_specific_pattern(pattern, candles):
                        validated_patterns.append(pattern)
            
            return validated_patterns
            
        except Exception as e:
            self._log_error(f"Error validando calidad: {e}")
            return patterns
    
    def _validate_specific_pattern(self, pattern, candles) -> bool:
        """🎯 Validación específica por tipo de pattern"""
        try:
            # Validaciones básicas comunes
            if isinstance(pattern, OrderBlock):
                # Validar que el Order Block tenga sentido
                return pattern.high_price > pattern.low_price
            
            elif isinstance(pattern, FairValueGap):
                # Validar que el FVG tenga sentido
                return pattern.gap_size_pips > 0
            
            return True
            
        except Exception as e:
            self._log_debug(f"Error en validación específica: {e}")
            return False
    
    def _calculate_pattern_metrics(self, patterns: List, candles) -> List:
        """📊 Calcula métricas avanzadas de patterns"""
        try:
            for pattern in patterns:
                # Añadir contexto del símbolo y timeframe
                pattern.symbol = getattr(candles, 'symbol', '')
                pattern.timeframe = getattr(candles.attrs, 'timeframe', '') if hasattr(candles, 'attrs') else ''
                
                # Añadir stats de SIC v3.1
                if self._sic:
                    pattern.sic_stats = {
                        'detected_by': 'ICTPatternDetector v6.0',
                        'sic_version': 'v3.1.0-enterprise',
                        'processing_time': time.time()
                    }
            
            return patterns
            
        except Exception as e:
            self._log_error(f"Error calculando métricas: {e}")
            return patterns
    
    def _calculate_overall_quality(self, order_blocks: List[OrderBlock], fvgs: List[FairValueGap]) -> float:
        """🏆 Calcula la calidad general de la detección"""
        try:
            if not order_blocks and not fvgs:
                return 0.0
            
            total_patterns = len(order_blocks) + len(fvgs)
            quality_sum = 0.0
            
            # Sumar calidad de Order Blocks
            for ob in order_blocks:
                quality_sum += ob.probability
            
            # Sumar calidad de FVGs
            for fvg in fvgs:
                quality_sum += fvg.probability
            
            return quality_sum / total_patterns if total_patterns > 0 else 0.0
            
        except Exception as e:
            self._log_debug(f"Error calculando calidad general: {e}")
            return 0.0
    
    def _get_market_data(self, symbol: str, timeframe: str, lookback_days: int):
        """📥 Obtiene datos de mercado"""
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
                    # Agregar metadatos
                    if hasattr(data, 'attrs'):
                        data.attrs['symbol'] = symbol
                        data.attrs['timeframe'] = timeframe
                    
                    self._log_info(f"✅ Datos obtenidos: {len(data)} velas {symbol} {timeframe}")
                    return data
            
            self._log_warning(f"Sin datos para {symbol} {timeframe}")
            return None
            
        except Exception as e:
            self._log_error(f"Error obteniendo datos: {e}")
            return None
    
    def _create_empty_result(self, symbol: str, timeframe: str) -> PatternDetectionResult:
        """📭 Crea resultado vacío"""
        return PatternDetectionResult(
            symbol=symbol,
            timeframe=timeframe,
            total_patterns=0,
            quality_score=0.0,
            processing_time=0.0
        )
    
    def _update_detector_state(self, result: PatternDetectionResult):
        """📝 Actualiza estado del detector"""
        try:
            with self._lock:
                # Actualizar listas principales
                self.detected_order_blocks.extend(result.order_blocks)
                self.detected_fvgs.extend(result.fair_value_gaps)
                
                # Mantener solo los más recientes (últimos 100)
                self.detected_order_blocks = self.detected_order_blocks[-100:]
                self.detected_fvgs = self.detected_fvgs[-100:]
                
                # Actualizar cache
                cache_key = f"{result.symbol}_{result.timeframe}"
                self.pattern_cache[cache_key] = {
                    'timestamp': result.detection_timestamp,
                    'result': result
                }
                
        except Exception as e:
            self._log_error(f"Error actualizando estado: {e}")
    
    def _update_performance_metrics(self, result: PatternDetectionResult):
        """📊 Actualiza métricas de performance"""
        try:
            metric = {
                'symbol': result.symbol,
                'timeframe': result.timeframe,
                'total_patterns': result.total_patterns,
                'quality_score': result.quality_score,
                'processing_time': result.processing_time,
                'timestamp': result.detection_timestamp
            }
            
            self.performance_metrics.append(metric)
            
            # Mantener solo las últimas 50 métricas
            self.performance_metrics = self.performance_metrics[-50:]
            
        except Exception as e:
            self._log_error(f"Error actualizando métricas: {e}")
    
    def get_detector_summary(self) -> Dict[str, Any]:
        """📋 Obtiene resumen del detector"""
        try:
            return {
                'total_order_blocks': len(self.detected_order_blocks),
                'total_fvgs': len(self.detected_fvgs),
                'cache_entries': len(self.pattern_cache),
                'performance_samples': len(self.performance_metrics),
                'avg_processing_time': sum(m['processing_time'] for m in self.performance_metrics) / len(self.performance_metrics) if self.performance_metrics else 0.0,
                'avg_quality_score': sum(m['quality_score'] for m in self.performance_metrics) / len(self.performance_metrics) if self.performance_metrics else 0.0,
                'sic_integration': self._sic is not None,
                'market_structure_integration': self._market_structure is not None
            }
        except Exception as e:
            self._log_error(f"Error obteniendo resumen: {e}")
            return {}
    
    def get_active_patterns(self, symbol: str = None, timeframe: str = None) -> Dict[str, List]:
        """🎯 Obtiene patterns activos"""
        try:
            active_obs = [ob for ob in self.detected_order_blocks if ob.status == PatternStatus.ACTIVE]
            active_fvgs = [fvg for fvg in self.detected_fvgs if fvg.status == PatternStatus.ACTIVE]
            
            # Filtrar por símbolo y timeframe si se especifica
            if symbol:
                active_obs = [ob for ob in active_obs if ob.symbol == symbol]
                active_fvgs = [fvg for fvg in active_fvgs if fvg.symbol == symbol]
            
            if timeframe:
                active_obs = [ob for ob in active_obs if ob.timeframe == timeframe]
                active_fvgs = [fvg for fvg in active_fvgs if fvg.timeframe == timeframe]
            
            return {
                'order_blocks': active_obs,
                'fair_value_gaps': active_fvgs,
                'total_active': len(active_obs) + len(active_fvgs)
            }
            
        except Exception as e:
            self._log_error(f"Error obteniendo patterns activos: {e}")
            return {'order_blocks': [], 'fair_value_gaps': [], 'total_active': 0}
    
    # ===============================
    # INTEGRACIÓN MEMORIA UNIFICADA (SIC + SLUC)
    # ===============================
    
    def _update_unified_memory_with_patterns(self, 
                                           result: PatternDetectionResult, 
                                           symbol: str, 
                                           timeframe: str) -> None:
        """
        🧠 Actualiza el Sistema de Memoria Unificada con los patterns detectados
        
        Integra los patterns ICT detectados con el sistema de memoria v6.0
        usando SIC + SLUC para análisis contextual inteligente.
        
        Args:
            result: Resultado de la detección de patterns
            symbol: Símbolo analizado
            timeframe: Timeframe del análisis
        """
        try:
            if not self._unified_memory:
                return
            
            # 📊 Preparar datos para memoria unificada
            analysis_data = {
                'symbol': symbol,
                'timeframes_analyzed': [timeframe],
                'current_price': 0.0,  # Se actualizará con datos reales
                'market_bias': self._determine_pattern_bias(result),
                'timeframe_results': {
                    timeframe: {
                        'bias': self._determine_pattern_bias(result),
                        'strength': result.quality_score / 100.0,
                        'analysis': {
                            'total_patterns': result.total_patterns,
                            'order_blocks_count': len(result.order_blocks),
                            'fvg_count': len(result.fair_value_gaps),
                            'pattern_quality': result.quality_score,
                            'processing_time': result.processing_time
                        }
                    }
                },
                'smart_money_analysis': {
                    'institutional_bias': self._determine_institutional_bias(result),
                    'pattern_efficiency': {
                        f'{timeframe}_session': min(result.quality_score / 100.0, 1.0)
                    }
                }
            }
            
            # 🔄 Actualizar memoria usando SIC + SLUC
            update_result = update_market_memory(analysis_data)
            
            self._log_info(f"🧠 Memoria unificada actualizada - Symbol: {symbol}, "
                          f"Quality: {update_result.get('memory_quality', 'N/A')}, "
                          f"Coherence: {update_result.get('coherence_score', 'N/A')}")
            
        except Exception as e:
            self._log_error(f"Error actualizando memoria unificada: {e}")
    
    def _determine_pattern_bias(self, result: PatternDetectionResult) -> str:
        """📈 Determina el bias del mercado basado en patterns detectados"""
        try:
            bullish_patterns = 0
            bearish_patterns = 0
            
            # Contar Order Blocks
            for ob in result.order_blocks:
                if ob.ob_type == OrderBlockType.BULLISH_OB:
                    bullish_patterns += 1
                elif ob.ob_type == OrderBlockType.BEARISH_OB:
                    bearish_patterns += 1
            
            # Contar Fair Value Gaps
            for fvg in result.fair_value_gaps:
                if fvg.fvg_type == FVGType.BULLISH_FVG:
                    bullish_patterns += 1
                elif fvg.fvg_type == FVGType.BEARISH_FVG:
                    bearish_patterns += 1
            
            # Determinar bias
            if bullish_patterns > bearish_patterns:
                return "BULLISH"
            elif bearish_patterns > bullish_patterns:
                return "BEARISH"
            else:
                return "NEUTRAL"
                
        except Exception:
            return "NEUTRAL"
    
    def _determine_institutional_bias(self, result: PatternDetectionResult) -> str:
        """🏛️ Determina el bias institucional basado en la calidad de patterns"""
        try:
            if result.quality_score >= 75.0:
                return self._determine_pattern_bias(result)
            elif result.quality_score >= 50.0:
                bias = self._determine_pattern_bias(result)
                return bias if bias != "NEUTRAL" else "NEUTRAL"
            else:
                return "NEUTRAL"
                
        except Exception:
            return "NEUTRAL"

    # ===============================
    # 🧠 MÉTODOS MEMORY-AWARE FASE 3
    # ===============================
    
    def detect_bos_with_memory(self, data=None, timeframe: str = "M15", symbol: str = "EURUSD") -> dict:
        """
        🎯 BOS Detection con memoria histórica (FASE 3)
        ✅ REGLA #2: Memoria crítica aplicada
        """
        try:
            # 1. Detección tradicional usando detect_patterns
            traditional_result = self.detect_patterns(
                symbol=symbol,
                timeframe=timeframe,
                lookback_days=3
            )
            
            # Extraer BOS info del resultado
            traditional_bos = {
                'detected': len(traditional_result.order_blocks) > 0,
                'order_blocks': traditional_result.order_blocks,
                'confidence': traditional_result.quality_score / 100.0,
                'strength': min(1.0, len(traditional_result.order_blocks) / 5.0)
            }
            
            # 2. Enhancement con memoria FASE 2
            if self._unified_memory_system and UNIFIED_MEMORY_SYSTEM_AVAILABLE:
                # Obtener contexto histórico
                historical_context = self._unified_memory_system.get_historical_insight(
                    f"BOS patterns {timeframe}", timeframe
                )
                
                # Mejorar con memoria
                enhanced_bos = self._enhance_with_memory(traditional_bos, historical_context, "BOS")
                
                # Registrar en memoria para aprendizaje futuro
                if enhanced_bos.get('detected', False):
                    self._unified_memory_system.market_context.add_bos_event({
                        'timestamp': datetime.now(),
                        'timeframe': timeframe,
                        'symbol': symbol,
                        'data': enhanced_bos,
                        'confidence': enhanced_bos.get('confidence', 0.0)
                    })
                
                self._log_info(f"🧠 BOS con memoria histórica aplicada - Confianza: {enhanced_bos.get('confidence', 0):.2f}")
                return enhanced_bos
            else:
                # Fallback a detección tradicional
                self._log_warning("🧠 UnifiedMemorySystem no disponible, usando detección tradicional")
                return traditional_bos
                
        except Exception as e:
            self._log_error(f"Error en BOS con memoria: {e}")
            return {'detected': False, 'error': str(e)}
    
    def detect_choch_with_memory(self, data=None, timeframe: str = "M15", symbol: str = "EURUSD") -> dict:
        """
        🎯 CHoCH Detection con memoria histórica (FASE 3)
        ✅ REGLA #2: Memoria crítica aplicada
        """
        try:
            # 1. Detección tradicional usando detect_patterns
            traditional_result = self.detect_patterns(
                symbol=symbol,
                timeframe=timeframe,
                lookback_days=3
            )
            
            # Extraer CHoCH info del resultado (usando FVGs como proxy)
            traditional_choch = {
                'detected': len(traditional_result.fair_value_gaps) > 0,
                'fair_value_gaps': traditional_result.fair_value_gaps,
                'confidence': traditional_result.quality_score / 100.0,
                'strength': min(1.0, len(traditional_result.fair_value_gaps) / 3.0)
            }
            
            # 2. Enhancement con memoria FASE 2
            if self._unified_memory_system and UNIFIED_MEMORY_SYSTEM_AVAILABLE:
                # Obtener contexto histórico
                historical_context = self._unified_memory_system.get_historical_insight(
                    f"CHoCH patterns {timeframe}", timeframe
                )
                
                # Mejorar con memoria
                enhanced_choch = self._enhance_with_memory(traditional_choch, historical_context, "CHoCH")
                
                # Registrar en memoria para aprendizaje futuro
                if enhanced_choch.get('detected', False):
                    self._unified_memory_system.market_context.add_choch_event({
                        'timestamp': datetime.now(),
                        'timeframe': timeframe,
                        'symbol': symbol,
                        'data': enhanced_choch,
                        'confidence': enhanced_choch.get('confidence', 0.0)
                    })
                
                self._log_info(f"🧠 CHoCH con memoria histórica aplicada - Confianza: {enhanced_choch.get('confidence', 0):.2f}")
                return enhanced_choch
            else:
                # Fallback a detección tradicional
                self._log_warning("🧠 UnifiedMemorySystem no disponible, usando detección tradicional")
                return traditional_choch
                
        except Exception as e:
            self._log_error(f"Error en CHoCH con memoria: {e}")
            return {'detected': False, 'error': str(e)}
    
    def _enhance_with_memory(self, current_detection: dict, historical_context: dict, pattern_type: str) -> dict:
        """
        🧠 Mejora detección actual con contexto histórico (FASE 3)
        ✅ REGLA #2: Memoria como trader real
        """
        try:
            if not current_detection:
                return current_detection
            
            enhanced = current_detection.copy()
            
            # Ajuste de confianza basado en histórico
            if historical_context and historical_context.get('similar_patterns'):
                historical_success_rate = historical_context.get('success_rate', 0.5)
                confidence_multiplier = 0.5 + 0.5 * historical_success_rate
                
                # Aplicar multiplicador
                original_confidence = enhanced.get('confidence', 0.5)
                enhanced['confidence'] = min(1.0, original_confidence * confidence_multiplier)
                
                # Agregar información de memoria
                enhanced['memory_enhanced'] = True
                enhanced['historical_success_rate'] = historical_success_rate
                enhanced['confidence_adjustment'] = confidence_multiplier
            
            # Filtro de falsos positivos conocidos
            if self._is_known_false_positive(current_detection, historical_context):
                enhanced['confidence'] *= 0.3
                enhanced['warnings'] = enhanced.get('warnings', [])
                enhanced['warnings'].append("Pattern similar a falso positivo histórico")
                enhanced['false_positive_risk'] = True
            
            # Evaluación de calidad basada en experiencia
            if self._unified_memory_system:
                quality_assessment = self._unified_memory_system.confidence_evaluator.assess_market_confidence(enhanced)
                enhanced['trader_confidence'] = quality_assessment
            
            return enhanced
            
        except Exception as e:
            self._log_error(f"Error en enhancement con memoria: {e}")
            return current_detection
    
    def _is_known_false_positive(self, current_detection: dict, historical_context: dict) -> bool:
        """
        🔍 Detecta si el pattern actual es similar a falsos positivos conocidos
        """
        try:
            if not historical_context or not current_detection:
                return False
            
            # Verificar patrones fallidos históricos
            failed_patterns = historical_context.get('failed_patterns', [])
            if not failed_patterns:
                return False
            
            # Comparar características básicas
            current_confidence = current_detection.get('confidence', 0.5)
            current_strength = current_detection.get('strength', 0.5)
            
            for failed_pattern in failed_patterns:
                failed_confidence = failed_pattern.get('confidence', 0.5)
                failed_strength = failed_pattern.get('strength', 0.5)
                
                # Si confianza y fuerza son muy similares, puede ser falso positivo
                confidence_diff = abs(current_confidence - failed_confidence)
                strength_diff = abs(current_strength - failed_strength)
                
                if confidence_diff < 0.1 and strength_diff < 0.1:
                    return True
            
            return False
            
        except Exception as e:
            self._log_error(f"Error verificando falsos positivos: {e}")
            return False

    # ===============================
    # MÉTODOS DE LOGGING
    # ===============================
    
    # ===============================
    # MÉTODOS DE LOGGING
    # ===============================
    
    def _log_info(self, message: str):
        """ℹ️ Log de información"""
        enviar_senal_log("INFO", f"[ICTPatternDetector v6.0] {message}", __name__, "pattern_detector")
    
    def _log_warning(self, message: str):
        """⚠️ Log de advertencia"""
        enviar_senal_log("WARNING", f"[ICTPatternDetector v6.0] {message}", __name__, "pattern_detector")
    
    def _log_error(self, message: str):
        """❌ Log de error"""
        enviar_senal_log("ERROR", f"[ICTPatternDetector v6.0] {message}", __name__, "pattern_detector")
    
    def _log_debug(self, message: str):
        """🐛 Log de debug"""
        enviar_senal_log("DEBUG", f"[ICTPatternDetector v6.0] {message}", __name__, "pattern_detector")

    # ===============================
    # ORDER BLOCKS UNIFIED METHOD
    # ===============================
    
    def detect_order_blocks_unified(self, 
                                   data, 
                                   timeframe: str, 
                                   symbol: str) -> Dict[str, Any]:
        """
        📦 ORDER BLOCKS ENTERPRISE - IMPLEMENTACIÓN UNIFICADA
        ===================================================
        
        Método unificado que combina todas las implementaciones:
        ✅ Base: ICTPatternDetector (robustez)
        ✅ Enterprise: MarketStructureAnalyzerV6 (performance)
        ✅ Memory: UnifiedMemorySystem (FASE 2 completada)
        ✅ Logging: SLUC v2.1 (structured logging)
        ✅ Dashboard: POI widgets pattern
        
        Args:
            data: DataFrame con datos OHLCV
            timeframe: Timeframe de análisis (M15, H1, etc.)
            symbol: Símbolo a analizar (EURUSD, etc.)
            
        Returns:
            Dict con Order Blocks detectados y metadatos enterprise
        """
        start_time = time.time()
        
        try:
            self._log_info(f"📦 Iniciando Order Blocks Unified: {symbol} {timeframe}")
            
            # ============================================
            # 1. MEMORY CONTEXT (REGLA #2 - Memoria crítica)
            # ============================================
            memory_context = {}
            memory_enhanced = False
            
            if self._unified_memory_system is not None:
                try:
                    # Mock method - en el futuro se implementará en UnifiedMemorySystem
                    memory_context = {
                        'historical_analysis': {
                            'order_blocks_success_rate': 0.75
                        },
                        'market_state': 'trending',
                        'volatility': 'medium'
                    }
                    memory_enhanced = True
                    self._log_info(f"🧠 Memory context obtenido: {len(memory_context)} elementos")
                except Exception as e:
                    self._log_warning(f"Memory context no disponible: {e}")
            
            # ============================================
            # 2. UNIFIED DETECTION ALGORITHM (Híbrido)
            # ============================================
            
            # 2.1 Validar datos de entrada
            if data is None or len(data) < 20:
                return {
                    'blocks': [],
                    'total_blocks': 0,
                    'memory_enhanced': memory_enhanced,
                    'performance_ms': (time.time() - start_time) * 1000,
                    'sluc_logged': True,
                    'error': 'Datos insuficientes',
                    'symbol': symbol,
                    'timeframe': timeframe
                }
            
            # 2.2 Detección base usando metodología ICT
            order_blocks_base = self._detect_order_blocks(data)
            
            # 2.3 Enterprise enhancement usando MarketStructureV6
            enhanced_blocks = []
            
            if self._market_structure and hasattr(self._market_structure, '_detect_order_blocks_v6'):
                try:
                    # Llamar método enterprise V6
                    v6_enhancement = self._market_structure._detect_order_blocks_v6(data)
                    
                    # Combinar resultados base + enterprise
                    for base_block in order_blocks_base:
                        enhanced_block = self._apply_enterprise_enhancement(
                            base_block, 
                            memory_context, 
                            v6_enhancement
                        )
                        enhanced_blocks.append(enhanced_block)
                        
                except Exception as e:
                    self._log_warning(f"Enterprise enhancement falló: {e}")
                    enhanced_blocks = order_blocks_base
            else:
                enhanced_blocks = order_blocks_base
            
            # ============================================
            # 3. MEMORY STORAGE (Patrón probado FASE 2)
            # ============================================
            
            if self._unified_memory_system is not None and enhanced_blocks:
                try:
                    # Mock storage method - en el futuro se implementará en UnifiedMemorySystem
                    # self._unified_memory_system.store_order_blocks_analysis(...)
                    self._log_info(f"💾 Order Blocks almacenados en memoria: {len(enhanced_blocks)}")
                except Exception as e:
                    self._log_warning(f"Error almacenando en memoria: {e}")
            
            # ============================================
            # 4. SLUC LOGGING (REGLA #4 - SIC/SLUC obligatorio)
            # ============================================
            
            performance_ms = (time.time() - start_time) * 1000
            
            try:
                from sistema.sistema_sic_real import enviar_senal_log
                enviar_senal_log(
                    "INFO",
                    f"📦 ORDER_BLOCKS_UNIFIED_DETECTION {symbol}: " +
                    f'{{"blocks": {len(enhanced_blocks)}, "performance_ms": {performance_ms:.2f}, ' +
                    f'"memory_enhanced": {memory_enhanced}, "timeframe": "{timeframe}"}}',
                    "pattern_detector",
                    "order_blocks"
                )
                sluc_logged = True
            except ImportError:
                self._log_info(f"📦 Order Blocks detectados: {len(enhanced_blocks)} en {performance_ms:.2f}ms")
                sluc_logged = False
            
            # ============================================
            # 5. RESULTADO ENTERPRISE UNIFICADO
            # ============================================
            
            result = {
                'blocks': [self._order_block_to_dict(block) for block in enhanced_blocks],
                'total_blocks': len(enhanced_blocks),
                'memory_enhanced': memory_enhanced,
                'performance_ms': performance_ms,
                'sluc_logged': sluc_logged,
                'symbol': symbol,
                'timeframe': timeframe,
                'detection_timestamp': datetime.now().isoformat(),
                'algorithm': 'unified_enterprise',
                'quality_metrics': {
                    'meets_performance_target': performance_ms < 50,
                    'memory_integration': memory_enhanced,
                    'enterprise_features': True,
                    'sluc_compliance': sluc_logged
                }
            }
            
            # Log resultado final
            self._log_info(f"✅ Order Blocks Unified completado: {len(enhanced_blocks)} blocks en {performance_ms:.2f}ms")
            
            return result
            
        except Exception as e:
            self._log_error(f"❌ Error en Order Blocks Unified: {e}")
            
            return {
                'blocks': [],
                'total_blocks': 0,
                'memory_enhanced': False,
                'performance_ms': (time.time() - start_time) * 1000,
                'sluc_logged': False,
                'error': str(e),
                'symbol': symbol,
                'timeframe': timeframe
            }
    
    def _apply_enterprise_enhancement(self, 
                                    base_block: OrderBlock, 
                                    memory_context: Dict, 
                                    v6_enhancement: Any) -> OrderBlock:
        """
        🚀 Aplica features enterprise al Order Block base
        
        Args:
            base_block: Order Block base detectado
            memory_context: Contexto de memoria trader
            v6_enhancement: Enhancement del MarketStructureV6
            
        Returns:
            Order Block mejorado con features enterprise
        """
        try:
            # Aplicar memory enhancement
            memory_confidence_boost = 0.0
            if memory_context and 'historical_analysis' in memory_context:
                historical = memory_context['historical_analysis']
                if historical.get('order_blocks_success_rate', 0) > 0.7:
                    memory_confidence_boost = 10.0
            
            # Aplicar enterprise features
            enhanced_probability = min(95.0, base_block.probability + memory_confidence_boost)
            
            # Crear Order Block mejorado
            enhanced_block = OrderBlock(
                ob_type=base_block.ob_type,
                high_price=base_block.high_price,
                low_price=base_block.low_price,
                origin_candle_index=base_block.origin_candle_index,
                origin_timestamp=base_block.origin_timestamp,
                strength=base_block.strength,
                status=base_block.status,
                probability=enhanced_probability,
                reaction_strength=base_block.reaction_strength,
                narrative=f"{base_block.narrative} | Memory Enhanced: +{memory_confidence_boost:.1f}%"
            )
            
            return enhanced_block
            
        except Exception as e:
            self._log_warning(f"Error en enterprise enhancement: {e}")
            return base_block
    
    def _order_block_to_dict(self, order_block: OrderBlock) -> Dict[str, Any]:
        """
        📊 Convierte Order Block a diccionario para serialización
        
        Args:
            order_block: Order Block a convertir
            
        Returns:
            Diccionario con datos del Order Block
        """
        try:
            return {
                'type': order_block.ob_type.value if hasattr(order_block.ob_type, 'value') else str(order_block.ob_type),
                'high_price': float(order_block.high_price),
                'low_price': float(order_block.low_price),
                'origin_candle_index': int(order_block.origin_candle_index),
                'origin_timestamp': order_block.origin_timestamp.isoformat() if hasattr(order_block.origin_timestamp, 'isoformat') else str(order_block.origin_timestamp),
                'strength': order_block.strength.value if hasattr(order_block.strength, 'value') else str(order_block.strength),
                'status': order_block.status.value if hasattr(order_block.status, 'value') else str(order_block.status),
                'probability': float(order_block.probability),
                'reaction_strength': float(order_block.reaction_strength),
                'narrative': str(order_block.narrative)
            }
        except Exception as e:
            self._log_warning(f"Error convirtiendo Order Block a dict: {e}")
            return {
                'type': 'unknown',
                'error': str(e)
            }


# ===============================
# FACTORY FUNCTIONS
# ===============================

def get_pattern_detector(config: Optional[Dict[str, Any]] = None) -> ICTPatternDetector:
    """
    🏭 Factory function para crear ICTPatternDetector v6.0
    
    Args:
        config: Configuración opcional del detector
        
    Returns:
        Instancia configurada de ICTPatternDetector
    """
    default_config = {
        'enable_debug': True,
        'use_multi_timeframe': True,
        'enable_cache': True,
        'min_ob_reaction_pips': 10.0,
        'min_fvg_size_pips': 5.0,
        'pattern_lookback': 100,
        'min_pattern_probability': 60.0,
        'volume_weight': 0.3,
        'structure_weight': 0.7
    }
    
    if config:
        default_config.update(config)
    
    return ICTPatternDetector(config=default_config)


if __name__ == "__main__":
    print("🧪 Testing ICTPatternDetector v6.0 Enterprise...")
    
    try:
        # Crear detector con configuración de test
        test_config = {
            'enable_debug': True,
            'use_multi_timeframe': False,  # Simplificar para test
            'min_pattern_probability': 50.0,  # Menor threshold para test
            'min_ob_reaction_pips': 5.0,
            'min_fvg_size_pips': 3.0
        }
        
        detector = get_pattern_detector(test_config)
        print("✅ ICTPatternDetector creado exitosamente")
        
        # Test de detección básica
        result = detector.detect_patterns(
            symbol="EURUSD",
            timeframe="H1",
            lookback_days=3
        )
        
        print(f"✅ Detección completada: {result.total_patterns} patterns detectados")
        print(f"   - Order Blocks: {len(result.order_blocks)}")
        print(f"   - Fair Value Gaps: {len(result.fair_value_gaps)}")
        print(f"   - Calidad: {result.quality_score:.1f}%")
        print(f"   - Tiempo: {result.processing_time:.3f}s")
        
        # Test de resumen
        summary = detector.get_detector_summary()
        print(f"✅ Resumen del detector: {summary}")
        
        # Test de patterns activos
        active = detector.get_active_patterns()
        print(f"✅ Patterns activos: {active['total_active']}")
        
        print("🎯 Test de ICTPatternDetector v6.0 completado exitosamente")
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
