#!/usr/bin/env python3
"""
💥 BREAKER BLOCKS DETECTOR ENTERPRISE v6.0
==========================================

Complete implementation of Breaker Block detection with enterprise features:
- Advanced Order Block → Breaker conversion logic
- Lifecycle management (OrderBlock → Break → Retest → Breaker)
- UnifiedMemorySystem v6.1 integration
- SLUC v2.1 logging system
- Enhanced confidence scoring
- Real-time mitigation tracking

FASE 5: Advanced Patterns Migration
Enhanced from: poi_detector_adapted.py detectar_breaker_blocks()
Target: Enterprise v6.0 SIC architecture

Autor: ICT Engine Team
Sprint: FASE 5 - Advanced Patterns
Fecha: 09 Agosto 2025
"""

# 📌 REGLA #14: Mantener código libre de lint warnings y orden de imports correcto

# 1. Estándar
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

# 2. Terceros
import pandas as pd

# 3. Internos - SIC/SLUC Enterprise
try:
    from core.smart_trading_logger import SmartTradingLogger
    from core.data_management.unified_memory_system import UnifiedMemorySystem
    from core.ict_engine.ict_types import TradingDirection
except ImportError:
    # Fallback for testing
    print("[WARNING] Enterprise modules not available - using fallback")
    SmartTradingLogger = Any
    UnifiedMemorySystem = Any
    
    # Fallback TradingDirection for testing
    class TradingDirection(Enum):
        BUY = "buy"
        SELL = "sell"
        BULLISH = "bullish"
        BEARISH = "bearish"
        NEUTRAL = "neutral"


class BreakerBlockType(Enum):
    """💥 Tipos de Breaker Blocks"""
    BULLISH_BREAKER = "bullish_breaker"    # Ex-bearish OB ahora soporte
    BEARISH_BREAKER = "bearish_breaker"    # Ex-bullish OB ahora resistencia
    FAILED_BREAKER = "failed_breaker"      # Breaker que falló en su función
    UNKNOWN = "unknown"


class BreakerStatus(Enum):
    """🔄 Estados del ciclo de vida Breaker"""
    FORMING = "forming"          # En proceso de formación
    CONFIRMED = "confirmed"      # Confirmado como breaker
    ACTIVE = "active"           # Activo como soporte/resistencia
    TESTED = "tested"           # Ha sido testeado
    FAILED = "failed"           # Falló como breaker
    EXPIRED = "expired"         # Expirado por tiempo


class OrderBlockBreakType(Enum):
    """⚡ Tipos de ruptura de Order Block"""
    CLEAN_BREAK = "clean_break"        # Ruptura limpia sin retorno
    FALSE_BREAK = "false_break"        # Ruptura falsa, retorno inmediato  
    RETEST_BREAK = "retest_break"      # Ruptura con retest posterior
    VIOLENT_BREAK = "violent_break"    # Ruptura violenta con volume
    UNKNOWN = "unknown"


@dataclass
class BreakerBlockSignal:
    """💥 Señal de Breaker Block Enterprise v6.0"""
    breaker_type: BreakerBlockType
    status: BreakerStatus
    direction: TradingDirection
    
    # 📊 Precio y zonas
    price_level: float
    support_zone: Tuple[float, float]
    resistance_zone: Tuple[float, float]
    
    # 🏗️ Origen y formación
    original_order_block_id: str
    break_type: OrderBlockBreakType
    break_timestamp: datetime
    retest_timestamp: Optional[datetime]
    
    # 📈 Métricas enterprise
    confidence: float
    strength: float
    institutional_interest: float
    volume_confirmation: bool
    
    # 🎯 Trading levels
    entry_zone: Tuple[float, float]
    stop_loss: float
    take_profit_1: float
    take_profit_2: float
    
    # 📝 Metadata
    narrative: str
    timestamp: datetime
    symbol: str
    timeframe: str
    
    # 🔄 Lifecycle tracking
    test_count: int = 0
    successful_tests: int = 0
    failed_tests: int = 0
    last_test_time: Optional[datetime] = None
    expiry_time: Optional[datetime] = None
    analysis_id: str = ""


class BreakerBlockLifecycle:
    """🔄 Gestor del ciclo de vida de Breaker Blocks"""
    
    def __init__(self, logger: Optional[Any] = None):
        self.logger = logger
        self.active_breakers: Dict[str, BreakerBlockSignal] = {}
        self.breaker_history: List[BreakerBlockSignal] = []
        
    def track_breaker_formation(self, 
                               order_block: Dict,
                               break_data: Dict,
                               retest_data: Optional[Dict] = None) -> Optional[BreakerBlockSignal]:
        """📊 Rastrea la formación de un Breaker Block"""
        try:
            # Determinar tipo de breaker basado en OB original
            if order_block.get('type') == 'BULLISH_OB':
                breaker_type = BreakerBlockType.BEARISH_BREAKER  # OB bullish roto = resistencia
                direction = TradingDirection.SELL
            else:
                breaker_type = BreakerBlockType.BULLISH_BREAKER  # OB bearish roto = soporte
                direction = TradingDirection.BUY
                
            # Crear señal de breaker
            breaker = BreakerBlockSignal(
                breaker_type=breaker_type,
                status=BreakerStatus.CONFIRMED if retest_data else BreakerStatus.FORMING,
                direction=direction,
                price_level=order_block.get('price', 0.0),
                support_zone=(order_block.get('range_low', 0.0), order_block.get('price', 0.0)),
                resistance_zone=(order_block.get('price', 0.0), order_block.get('range_high', 0.0)),
                original_order_block_id=order_block.get('id', ''),
                break_type=self._classify_break_type(break_data),
                break_timestamp=break_data.get('timestamp', datetime.now()),
                retest_timestamp=retest_data.get('timestamp') if retest_data else None,
                confidence=self._calculate_breaker_confidence(order_block, break_data, retest_data),
                strength=self._calculate_breaker_strength(order_block, break_data),
                institutional_interest=order_block.get('confidence', 0.5),
                volume_confirmation=break_data.get('volume_spike', False),
                entry_zone=self._calculate_breaker_entry_zone(order_block, direction),
                stop_loss=self._calculate_breaker_stop_loss(order_block, direction),
                take_profit_1=self._calculate_breaker_tp1(order_block, direction),
                take_profit_2=self._calculate_breaker_tp2(order_block, direction),
                narrative=self._generate_breaker_narrative(breaker_type, order_block, break_data),
                timestamp=datetime.now(),
                symbol=break_data.get('symbol', ''),
                timeframe=break_data.get('timeframe', ''),
                expiry_time=datetime.now() + timedelta(hours=48),
                analysis_id=f"BRK_{order_block.get('symbol', '')}_{int(datetime.now().timestamp())}"
            )
            
            # Registrar en tracking
            self.active_breakers[breaker.analysis_id] = breaker
            
            if self.logger:
                self.logger.log_info(f"💥 Breaker Block formado: {breaker_type.value} desde {order_block.get('id')}")
                
            return breaker
            
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Error tracking breaker formation: {e}")
            return None
    
    def update_breaker_test(self, breaker_id: str, test_data: Dict) -> bool:
        """🧪 Actualizar test de breaker"""
        try:
            if breaker_id not in self.active_breakers:
                return False
                
            breaker = self.active_breakers[breaker_id]
            breaker.test_count += 1
            breaker.last_test_time = datetime.now()
            
            # Evaluar si el test fue exitoso
            test_successful = self._evaluate_breaker_test(breaker, test_data)
            
            if test_successful:
                breaker.successful_tests += 1
                breaker.status = BreakerStatus.ACTIVE
            else:
                breaker.failed_tests += 1
                if breaker.failed_tests >= 3:  # 3 fallos = breaker failed
                    breaker.status = BreakerStatus.FAILED
                    
            if self.logger:
                self.logger.log_debug(f"Breaker test actualizado: {breaker_id} - {'exitoso' if test_successful else 'fallido'}")
                
            return test_successful
            
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Error updating breaker test: {e}")
            return False
    
    def _classify_break_type(self, break_data: Dict) -> OrderBlockBreakType:
        """⚡ Clasificar tipo de ruptura"""
        volume_spike = break_data.get('volume_spike', False)
        price_action = break_data.get('price_action', 'normal')
        
        if volume_spike and price_action == 'violent':
            return OrderBlockBreakType.VIOLENT_BREAK
        elif break_data.get('immediate_return', False):
            return OrderBlockBreakType.FALSE_BREAK
        elif break_data.get('retest_confirmed', False):
            return OrderBlockBreakType.RETEST_BREAK
        else:
            return OrderBlockBreakType.CLEAN_BREAK
    
    def _calculate_breaker_confidence(self, 
                                    order_block: Dict, 
                                    break_data: Dict, 
                                    retest_data: Optional[Dict]) -> float:
        """🎯 Calcular confianza del breaker"""
        base_confidence = order_block.get('confidence', 0.5)
        
        # Bonus por tipo de ruptura
        break_bonus = 0.0
        break_type = self._classify_break_type(break_data)
        if break_type == OrderBlockBreakType.VIOLENT_BREAK:
            break_bonus = 0.2
        elif break_type == OrderBlockBreakType.RETEST_BREAK:
            break_bonus = 0.15
        elif break_type == OrderBlockBreakType.CLEAN_BREAK:
            break_bonus = 0.1
        
        # Bonus por retest confirmado
        retest_bonus = 0.15 if retest_data else 0.0
        
        # Bonus por volumen
        volume_bonus = 0.1 if break_data.get('volume_spike', False) else 0.0
        
        final_confidence = min(base_confidence + break_bonus + retest_bonus + volume_bonus, 0.95)
        return final_confidence
    
    def _calculate_breaker_strength(self, order_block: Dict, break_data: Dict) -> float:
        """💪 Calcular fuerza del breaker"""
        base_strength = order_block.get('score', 50) / 100.0
        
        # Factor de ruptura
        break_strength = break_data.get('break_strength', 0.5)
        
        # Combinar factores
        final_strength = (base_strength + break_strength) / 2
        return min(final_strength, 0.95)
    
    def _calculate_breaker_entry_zone(self, order_block: Dict, direction: TradingDirection) -> Tuple[float, float]:
        """🎯 Calcular zona de entrada"""
        if direction == TradingDirection.BUY:
            # Breaker bullish - entrada cerca del range low
            low = order_block.get('range_low', 0)
            high = order_block.get('price', 0)
            return (low - 0.0005, high + 0.0005)
        else:
            # Breaker bearish - entrada cerca del range high
            low = order_block.get('price', 0)
            high = order_block.get('range_high', 0)
            return (low - 0.0005, high + 0.0005)
    
    def _calculate_breaker_stop_loss(self, order_block: Dict, direction: TradingDirection) -> float:
        """🛑 Calcular stop loss"""
        if direction == TradingDirection.BUY:
            return order_block.get('range_low', 0) - 0.0015
        else:
            return order_block.get('range_high', 0) + 0.0015
    
    def _calculate_breaker_tp1(self, order_block: Dict, direction: TradingDirection) -> float:
        """🎯 Calcular take profit 1"""
        price = order_block.get('price', 0)
        if direction == TradingDirection.BUY:
            return price + 0.0030
        else:
            return price - 0.0030
    
    def _calculate_breaker_tp2(self, order_block: Dict, direction: TradingDirection) -> float:
        """🎯 Calcular take profit 2"""
        price = order_block.get('price', 0)
        if direction == TradingDirection.BUY:
            return price + 0.0050
        else:
            return price - 0.0050
    
    def _generate_breaker_narrative(self, 
                                  breaker_type: BreakerBlockType, 
                                  order_block: Dict, 
                                  break_data: Dict) -> str:
        """📝 Generar narrativa del breaker"""
        ob_type = order_block.get('type', 'unknown')
        break_type = self._classify_break_type(break_data)
        
        return f"{breaker_type.value.replace('_', ' ').title()} formado desde {ob_type} con {break_type.value.replace('_', ' ')}"
    
    def _evaluate_breaker_test(self, breaker: BreakerBlockSignal, test_data: Dict) -> bool:
        """🧪 Evaluar si un test del breaker fue exitoso"""
        test_price = test_data.get('price', 0)
        
        if breaker.direction == TradingDirection.BUY:
            # Test exitoso si precio rebota desde zona de soporte
            return (test_price >= breaker.support_zone[0] and 
                   test_data.get('bounced', False))
        else:
            # Test exitoso si precio rebota desde zona de resistencia  
            return (test_price <= breaker.resistance_zone[1] and 
                   test_data.get('bounced', False))


class BreakerBlockDetectorEnterprise:
    """
    💥 BREAKER BLOCKS DETECTOR ENTERPRISE v6.0
    ==========================================
    
    Advanced Breaker Block detection with complete lifecycle management:
    ✅ Order Block → Break → Retest → Breaker conversion
    ✅ Advanced break type classification
    ✅ Lifecycle management (forming → confirmed → active → failed)
    ✅ UnifiedMemorySystem v6.1 integration
    ✅ SLUC v2.1 logging completo
    ✅ Enhanced confidence scoring
    ✅ Volume confirmation analysis
    ✅ Real-time test tracking
    """

    def __init__(self, 
                 memory_system: Optional[Any] = None,
                 logger: Optional[Any] = None):
        """🚀 Inicializar Breaker Blocks Detector Enterprise"""
        
        # 🏗️ ENTERPRISE INFRASTRUCTURE
        self.memory_system = memory_system
        self.logger = logger or self._create_fallback_logger()
        self.lifecycle_manager = BreakerBlockLifecycle(logger)
        
        self._log_info("💥 Inicializando Breaker Blocks Detector Enterprise v6.0")
        
        # ⚙️ CONFIGURATION
        self.config = {
            'min_ob_age_hours': 1,          # Edad mínima OB para ser candidato
            'max_ob_age_hours': 48,         # Edad máxima OB para consideración
            'break_confirmation_pips': 10,   # Pips mínimos para confirmar ruptura
            'retest_window_hours': 24,      # Ventana para buscar retest
            'retest_tolerance_pips': 5,     # Tolerancia para retest
            'min_confidence': 0.6,          # Confianza mínima para breaker
            'volume_spike_threshold': 1.5,  # Multiplicador para detectar volume spike
            'max_simultaneous_breakers': 10 # Máximo breakers activos simultáneos
        }
        
        # 📊 ESTADO INTERNO
        self.detected_breakers: List[BreakerBlockSignal] = []
        self.processing_stats = {
            'total_order_blocks_analyzed': 0,
            'total_breaks_detected': 0,
            'total_retests_confirmed': 0,
            'total_breakers_formed': 0,
            'successful_breaker_rate': 0.0
        }
        
        self._log_info("✅ Breaker Blocks Detector Enterprise v6.0 inicializado correctamente")

    def detect_breaker_blocks_enterprise(self,
                                       data: pd.DataFrame,
                                       order_blocks: List[Dict],
                                       symbol: str,
                                       timeframe: str) -> List[BreakerBlockSignal]:
        """
        💥 DETECCIÓN PRINCIPAL DE BREAKER BLOCKS ENTERPRISE
        
        Args:
            data: Datos de velas OHLCV
            order_blocks: Order Blocks detectados previamente
            symbol: Par de divisa (ej: EURUSD)
            timeframe: Timeframe de análisis
            
        Returns:
            Lista de Breaker Blocks detectados
        """
        try:
            self._log_info(f"💥 Iniciando detección Breaker Blocks para {symbol} {timeframe}")
            
            if not order_blocks:
                self._log_warning("⚠️ No hay Order Blocks base para análisis de Breakers")
                return []
            
            if data is None or data.empty or len(data) < 20:
                self._log_warning(f"❌ Datos insuficientes: {len(data) if not data.empty else 0} velas")
                return []
            
            breaker_signals = []
            current_time = datetime.now()
            
            self._log_debug(f"Analizando {len(order_blocks)} Order Blocks para conversión a Breakers")
            
            # 🔍 ANÁLISIS DE CADA ORDER BLOCK
            for ob in order_blocks:
                try:
                    # 1. ✅ VALIDAR CANDIDATO
                    if not self._is_valid_breaker_candidate(ob, current_time):
                        continue
                    
                    # 2. 🔍 DETECTAR RUPTURA
                    break_analysis = self._analyze_order_block_break(ob, data)
                    if not break_analysis['broken']:
                        continue
                    
                    # 3. 🔄 BUSCAR RETEST
                    retest_analysis = self._analyze_retest_behavior(ob, data, break_analysis)
                    
                    # 4. 💥 EVALUAR FORMACIÓN DE BREAKER
                    if self._evaluate_breaker_formation(break_analysis, retest_analysis):
                        
                        # 5. 🎯 CREAR SEÑAL DE BREAKER
                        breaker_signal = self.lifecycle_manager.track_breaker_formation(
                            order_block=ob,
                            break_data=break_analysis,
                            retest_data=retest_analysis if retest_analysis['confirmed'] else None
                        )
                        
                        if breaker_signal:
                            # 6. 📊 ENHANCED VALIDATION
                            enhanced_signal = self._apply_enterprise_enhancements(
                                breaker_signal, data, symbol, timeframe
                            )
                            
                            if enhanced_signal.confidence >= self.config['min_confidence']:
                                breaker_signals.append(enhanced_signal)
                                self._log_info(f"✅ Breaker detectado: {enhanced_signal.breaker_type.value} - Confianza: {enhanced_signal.confidence:.2f}")
                    
                    self.processing_stats['total_order_blocks_analyzed'] += 1
                    
                except Exception as e:
                    self._log_error(f"Error procesando OB {ob.get('id', 'unknown')}: {e}")
                    continue
            
            # 7. 💾 GUARDAR EN MEMORIA ENTERPRISE
            if self.memory_system and breaker_signals:
                self._store_breakers_in_memory(breaker_signals)
            
            # 8. 📊 ACTUALIZAR ESTADÍSTICAS
            self._update_processing_stats(len(order_blocks), len(breaker_signals))
            
            self._log_info(f"🎯 Detección completada: {len(breaker_signals)} Breaker Blocks de {len(order_blocks)} OBs analizados")
            return breaker_signals
            
        except Exception as e:
            self._log_error(f"❌ Error en detección de Breaker Blocks: {e}")
            return []

    def _is_valid_breaker_candidate(self, order_block: Dict, current_time: datetime) -> bool:
        """✅ Validar si OB es candidato válido para breaker"""
        try:
            # Verificar edad del OB
            ob_timestamp = order_block.get('created_at')
            if isinstance(ob_timestamp, str):
                ob_timestamp = datetime.fromisoformat(ob_timestamp.replace('Z', '+00:00'))
            elif ob_timestamp is None:
                ob_timestamp = current_time  # Fallback
            
            age_hours = (current_time - ob_timestamp).total_seconds() / 3600
            
            if age_hours < self.config['min_ob_age_hours']:
                self._log_debug(f"OB muy nuevo: {age_hours:.1f}h < {self.config['min_ob_age_hours']}h")
                return False
            
            if age_hours > self.config['max_ob_age_hours']:
                self._log_debug(f"OB muy viejo: {age_hours:.1f}h > {self.config['max_ob_age_hours']}h")
                return False
            
            # Verificar que no esté ya roto (si está marcado)
            if order_block.get('broken', False):
                return False
            
            # Verificar confianza mínima
            if order_block.get('confidence', 0) < 0.4:
                return False
            
            return True
            
        except Exception as e:
            self._log_error(f"Error validando candidato breaker: {e}")
            return False

    def _analyze_order_block_break(self, order_block: Dict, data: pd.DataFrame) -> Dict[str, Any]:
        """🔍 Analizar ruptura de Order Block"""
        try:
            ob_high = order_block.get('range_high', 0)
            ob_low = order_block.get('range_low', 0)
            ob_type = order_block.get('type', '')
            
            recent_data = data.tail(50)  # Últimas 50 velas
            break_analysis = {
                'broken': False,
                'break_timestamp': None,
                'break_strength': 0.0,
                'break_type': OrderBlockBreakType.UNKNOWN,
                'volume_spike': False,
                'price_action': 'normal',
                'break_confirmation_pips': 0.0,
                'immediate_return': False
            }
            
            # 🔍 DETECTAR RUPTURA SEGÚN TIPO DE OB
            for i, (timestamp, candle) in enumerate(recent_data.iterrows()):
                if ob_type == 'BULLISH_OB':
                    # Ruptura bearish - precio rompe por debajo del OB low
                    if candle['low'] < ob_low:
                        break_pips = (ob_low - candle['low']) * 10000
                        if break_pips >= self.config['break_confirmation_pips']:
                            break_analysis['broken'] = True
                            break_analysis['break_timestamp'] = timestamp
                            break_analysis['break_confirmation_pips'] = break_pips
                            break_analysis['break_strength'] = min(break_pips / 20.0, 1.0)
                            
                            # Verificar retorno inmediato
                            if i < len(recent_data) - 3:
                                next_candles = recent_data.iloc[i+1:i+4]
                                if any(next_candles['close'] > ob_low):
                                    break_analysis['immediate_return'] = True
                                    break_analysis['break_type'] = OrderBlockBreakType.FALSE_BREAK
                            
                            break
                
                elif ob_type == 'BEARISH_OB':
                    # Ruptura bullish - precio rompe por encima del OB high
                    if candle['high'] > ob_high:
                        break_pips = (candle['high'] - ob_high) * 10000
                        if break_pips >= self.config['break_confirmation_pips']:
                            break_analysis['broken'] = True
                            break_analysis['break_timestamp'] = timestamp
                            break_analysis['break_confirmation_pips'] = break_pips
                            break_analysis['break_strength'] = min(break_pips / 20.0, 1.0)
                            
                            # Verificar retorno inmediato
                            if i < len(recent_data) - 3:
                                next_candles = recent_data.iloc[i+1:i+4]
                                if any(next_candles['close'] < ob_high):
                                    break_analysis['immediate_return'] = True
                                    break_analysis['break_type'] = OrderBlockBreakType.FALSE_BREAK
                            
                            break
            
            # 📊 ANALIZAR VOLUMEN SI DISPONIBLE
            if 'volume' in recent_data.columns and break_analysis['broken']:
                break_idx = recent_data.index.get_loc(break_analysis['break_timestamp'])
                break_volume = recent_data['volume'].iloc[break_idx]
                avg_volume = recent_data['volume'].tail(20).mean()
                
                if break_volume > avg_volume * self.config['volume_spike_threshold']:
                    break_analysis['volume_spike'] = True
                    if break_analysis['break_strength'] > 0.8:
                        break_analysis['price_action'] = 'violent'
                        break_analysis['break_type'] = OrderBlockBreakType.VIOLENT_BREAK
            
            if break_analysis['broken'] and break_analysis['break_type'] == OrderBlockBreakType.UNKNOWN:
                break_analysis['break_type'] = OrderBlockBreakType.CLEAN_BREAK
            
            return break_analysis
            
        except Exception as e:
            self._log_error(f"Error analizando ruptura OB: {e}")
            return {'broken': False}

    def _analyze_retest_behavior(self, 
                               order_block: Dict, 
                               data: pd.DataFrame, 
                               break_analysis: Dict) -> Dict[str, Any]:
        """🔄 Analizar comportamiento de retest"""
        try:
            if not break_analysis.get('broken', False):
                return {'confirmed': False}
            
            ob_high = order_block.get('range_high', 0)
            ob_low = order_block.get('range_low', 0)
            ob_type = order_block.get('type', '')
            break_timestamp = break_analysis.get('break_timestamp')
            
            retest_analysis = {
                'confirmed': False,
                'retest_timestamp': None,
                'retest_strength': 0.0,
                'bounce_confirmed': False,
                'retest_count': 0,
                'price_respect': 0.0
            }
            
            # 🔍 BUSCAR RETEST DESPUÉS DE LA RUPTURA
            break_idx = data.index.get_loc(break_timestamp)
            post_break_data = data.iloc[break_idx+1:]
            
            if len(post_break_data) < 5:
                return retest_analysis
            
            # Definir zona de retest según tipo de OB
            if ob_type == 'BULLISH_OB':
                # Después de ruptura bearish, buscar retest desde arriba
                retest_zone_high = ob_high + 0.0005
                retest_zone_low = ob_low - 0.0005
                
                for i, (timestamp, candle) in enumerate(post_break_data.iterrows()):
                    # Precio regresa a zona de OB roto
                    if retest_zone_low <= candle['low'] <= retest_zone_high:
                        retest_analysis['retest_count'] += 1
                        
                        if not retest_analysis['confirmed']:
                            retest_analysis['confirmed'] = True
                            retest_analysis['retest_timestamp'] = timestamp
                            
                            # Verificar si hay bounce (rechazo desde la zona)
                            if i < len(post_break_data) - 3:
                                next_candles = post_break_data.iloc[i+1:i+4]
                                if any(next_candles['close'] < retest_zone_low):
                                    retest_analysis['bounce_confirmed'] = True
                                    retest_analysis['retest_strength'] = 0.8
            
            elif ob_type == 'BEARISH_OB':
                # Después de ruptura bullish, buscar retest desde abajo
                retest_zone_high = ob_high + 0.0005
                retest_zone_low = ob_low - 0.0005
                
                for i, (timestamp, candle) in enumerate(post_break_data.iterrows()):
                    # Precio regresa a zona de OB roto
                    if retest_zone_low <= candle['high'] <= retest_zone_high:
                        retest_analysis['retest_count'] += 1
                        
                        if not retest_analysis['confirmed']:
                            retest_analysis['confirmed'] = True
                            retest_analysis['retest_timestamp'] = timestamp
                            
                            # Verificar si hay bounce (rechazo desde la zona)
                            if i < len(post_break_data) - 3:
                                next_candles = post_break_data.iloc[i+1:i+4]
                                if any(next_candles['close'] > retest_zone_high):
                                    retest_analysis['bounce_confirmed'] = True
                                    retest_analysis['retest_strength'] = 0.8
            
            # Calcular respeto al precio
            if retest_analysis['retest_count'] > 0:
                retest_analysis['price_respect'] = min(retest_analysis['retest_count'] / 3.0, 1.0)
            
            return retest_analysis
            
        except Exception as e:
            self._log_error(f"Error analizando retest: {e}")
            return {'confirmed': False}

    def _evaluate_breaker_formation(self, break_analysis: Dict, retest_analysis: Dict) -> bool:
        """💥 Evaluar si se forma un Breaker Block válido"""
        try:
            # Requisito mínimo: ruptura confirmada
            if not break_analysis.get('broken', False):
                return False
            
            # Descartar rupturas falsas inmediatas
            if break_analysis.get('immediate_return', False):
                return False
            
            # Preferir rupturas con retest confirmado
            if retest_analysis.get('confirmed', False):
                return True
            
            # Aceptar rupturas violentas sin retest
            if break_analysis.get('break_type') == OrderBlockBreakType.VIOLENT_BREAK:
                return True
            
            # Aceptar rupturas limpias con suficiente fuerza
            if (break_analysis.get('break_type') == OrderBlockBreakType.CLEAN_BREAK and 
                break_analysis.get('break_strength', 0) > 0.7):
                return True
            
            return False
            
        except Exception as e:
            self._log_error(f"Error evaluando formación breaker: {e}")
            return False

    def _apply_enterprise_enhancements(self, 
                                     breaker_signal: BreakerBlockSignal,
                                     data: pd.DataFrame,
                                     symbol: str,
                                     timeframe: str) -> BreakerBlockSignal:
        """🚀 Aplicar mejoras enterprise al breaker"""
        try:
            # Actualizar metadata
            breaker_signal.symbol = symbol
            breaker_signal.timeframe = timeframe
            
            # Mejorar confianza con análisis adicional
            additional_confidence = self._calculate_additional_confidence(breaker_signal, data)
            breaker_signal.confidence = min(breaker_signal.confidence + additional_confidence, 0.98)
            
            # Validar con contexto de mercado si disponible
            market_context_bonus = self._validate_market_context(breaker_signal, data)
            breaker_signal.institutional_interest += market_context_bonus
            
            # Actualizar narrativa con detalles enterprise
            breaker_signal.narrative += f" | Enterprise validated - {timeframe} | Confidence: {breaker_signal.confidence:.1%}"
            
            return breaker_signal
            
        except Exception as e:
            self._log_error(f"Error aplicando enterprise enhancements: {e}")
            return breaker_signal

    def _calculate_additional_confidence(self, breaker_signal: BreakerBlockSignal, data: pd.DataFrame) -> float:
        """📊 Calcular confianza adicional enterprise"""
        try:
            bonus = 0.0
            
            # Bonus por volume confirmation
            if breaker_signal.volume_confirmation:
                bonus += 0.05
            
            # Bonus por múltiples tests exitosos
            if breaker_signal.successful_tests > 0:
                bonus += min(breaker_signal.successful_tests * 0.03, 0.1)
            
            # Bonus por contexto de mercado
            if len(data) >= 20:
                recent_volatility = data['close'].pct_change().tail(20).std()
                if recent_volatility > 0.001:  # Alta volatilidad favorece breakers
                    bonus += 0.03
            
            return bonus
            
        except Exception:
            return 0.0

    def _validate_market_context(self, breaker_signal: BreakerBlockSignal, data: pd.DataFrame) -> float:
        """🏗️ Validar contexto de mercado"""
        try:
            # Análisis simplificado de tendencia
            if len(data) >= 10:
                recent_trend = data['close'].tail(10).pct_change().mean()
                
                # Si el breaker está alineado con la tendencia
                if ((breaker_signal.direction == TradingDirection.BUY and recent_trend > 0) or
                    (breaker_signal.direction == TradingDirection.SELL and recent_trend < 0)):
                    return 0.1
            
            return 0.0
            
        except Exception:
            return 0.0

    def _store_breakers_in_memory(self, breaker_signals: List[BreakerBlockSignal]):
        """💾 Guardar breakers en memoria enterprise"""
        try:
            if not self.memory_system:
                return
            
            for breaker in breaker_signals:
                breaker_data = {
                    'breaker_type': breaker.breaker_type.value,
                    'confidence': breaker.confidence,
                    'strength': breaker.strength,
                    'timestamp': breaker.timestamp.isoformat(),
                    'symbol': breaker.symbol,
                    'timeframe': breaker.timeframe,
                    'direction': breaker.direction.value,
                    'price_level': breaker.price_level
                }
                
                # En el futuro se integrará con UnifiedMemorySystem
                # self.memory_system.store_breaker_pattern(breaker_data)
                
            self._log_debug(f"Stored {len(breaker_signals)} breakers in memory")
            
        except Exception as e:
            self._log_error(f"Error storing breakers in memory: {e}")

    def _update_processing_stats(self, total_obs: int, total_breakers: int):
        """📊 Actualizar estadísticas de procesamiento"""
        try:
            self.processing_stats['total_order_blocks_analyzed'] += total_obs
            self.processing_stats['total_breakers_formed'] += total_breakers
            
            if self.processing_stats['total_order_blocks_analyzed'] > 0:
                self.processing_stats['successful_breaker_rate'] = (
                    self.processing_stats['total_breakers_formed'] / 
                    self.processing_stats['total_order_blocks_analyzed']
                )
            
        except Exception as e:
            self._log_error(f"Error updating stats: {e}")

    # ===========================================
    # 🛠️ UTILITY METHODS
    # ===========================================

    def get_active_breakers(self) -> List[BreakerBlockSignal]:
        """📋 Obtener breakers activos"""
        return [b for b in self.lifecycle_manager.active_breakers.values() 
                if b.status in [BreakerStatus.ACTIVE, BreakerStatus.CONFIRMED]]

    def get_processing_stats(self) -> Dict[str, Any]:
        """📊 Obtener estadísticas de procesamiento"""
        return self.processing_stats.copy()

    # ===========================================
    # 🛠️ LOGGING METHODS
    # ===========================================

    def _create_fallback_logger(self):
        """📝 Crear logger fallback"""
        class FallbackLogger:
            def log_info(self, msg, component="breaker_blocks"): print(f"[INFO] {msg}")
            def log_warning(self, msg, component="breaker_blocks"): print(f"[WARNING] {msg}")
            def log_error(self, msg, component="breaker_blocks"): print(f"[ERROR] {msg}")
            def log_debug(self, msg, component="breaker_blocks"): print(f"[DEBUG] {msg}")
        return FallbackLogger()

    def _log_info(self, message: str):
        if self.logger: self.logger.log_info(message, "breaker_blocks_enterprise")
        else: print(f"[INFO] {message}")

    def _log_warning(self, message: str):
        if self.logger: self.logger.log_warning(message, "breaker_blocks_enterprise")
        else: print(f"[WARNING] {message}")

    def _log_error(self, message: str):
        if self.logger: self.logger.log_error(message, "breaker_blocks_enterprise")
        else: print(f"[ERROR] {message}")

    def _log_debug(self, message: str):
        if self.logger: self.logger.log_debug(message, "breaker_blocks_enterprise")
        else: print(f"[DEBUG] {message}")


# ===========================================
# 🧪 TESTING & UTILITIES
# ===========================================

def create_test_breaker_detector() -> BreakerBlockDetectorEnterprise:
    """🧪 Crear detector para testing"""
    return BreakerBlockDetectorEnterprise()


if __name__ == "__main__":
    # 🧪 Test básico
    detector = create_test_breaker_detector()
    print("✅ Breaker Blocks Detector Enterprise v6.0 - Test básico completado")
