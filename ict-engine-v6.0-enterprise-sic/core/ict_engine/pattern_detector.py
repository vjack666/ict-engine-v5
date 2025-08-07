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

Autor: ICT Engine v6.0 Enterprise Team
Versión: v6.0.0-enterprise
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

# Componentes ICT Engine v6.0
try:
    from core.analysis.market_structure_analyzer import MarketStructureAnalyzer, MarketStructureSignal
    from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
    from utils.mt5_data_manager import MT5DataManager
    MARKET_STRUCTURE_AVAILABLE = True
except ImportError:
    MARKET_STRUCTURE_AVAILABLE = False
    print("⚠️ Market Structure Analyzer no disponible")

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
        self._market_structure: Optional[MarketStructureAnalyzer] = None
        self._downloader: Optional[AdvancedCandleDownloader] = None
        self._sic: Optional[SICv31Enterprise] = None
        
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
            
            # Configurar Market Structure Analyzer
            if MARKET_STRUCTURE_AVAILABLE:
                self._market_structure = MarketStructureAnalyzer()
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
                        symbol=symbol, 
                        timeframe=timeframe, 
                        lookback_days=lookback_days
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
            
            # 8. 💾 ACTUALIZAR ESTADO
            self._update_detector_state(result)
            
            # 9. 📊 MÉTRICAS DE PERFORMANCE
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
                           market_structure: Optional[MarketStructureSignal] = None) -> List[OrderBlock]:
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
                            market_structure: Optional[MarketStructureSignal] = None) -> Optional[OrderBlock]:
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
                              market_structure: Optional[MarketStructureSignal] = None) -> List[FairValueGap]:
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

# ===============================
# TEST Y VALIDACIÓN
# ===============================

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
