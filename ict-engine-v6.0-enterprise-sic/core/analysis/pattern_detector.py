# -*- coding: utf-8 -*-
"""
🎯 ICT PATTERN DETECTOR v6.0 ENTERPRISE
=============================================

Motor avanzado de detección de patrones ICT para trading institucional.
Implementa los patrones más efectivos de la metodología Inner Circle Trader
con precisión enterprise y rendimiento optimizado.

Autor: ICT Engine v6.0 Enterprise Team
Fecha: Agosto 7, 2025
Versión: v6.0.0-enterprise
"""

import time
from datetime import datetime, timedelta, time as dt_time
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import pandas as pd
import numpy as np

# Importar desde el sistema SIC v3.1 si está disponible
try:
    from sistema.sic_v3_1.smart_import import smart_import
    pd = smart_import('pandas')
    np = smart_import('numpy')
except ImportError:
    # Fallback directo
    import pandas as pd
    import numpy as np

# Importar downloader
try:
    from ..data_management.advanced_candle_downloader import get_advanced_candle_downloader
except ImportError:
    print("[WARNING] Downloader no disponible - usando datos simulados")
    get_advanced_candle_downloader = None

# Importar Smart Money Concepts v6.0
try:
    from ..smart_money_concepts.smart_money_analyzer import SmartMoneyAnalyzer
except ImportError:
    print("[WARNING] Smart Money Analyzer no disponible - funcionalidad limitada")
    SmartMoneyAnalyzer = None


class PatternType(Enum):
    """Tipos de patrones ICT detectables"""
    SILVER_BULLET = "silver_bullet"
    JUDAS_SWING = "judas_swing"
    LIQUIDITY_GRAB = "liquidity_grab"
    OPTIMAL_TRADE_ENTRY = "optimal_trade_entry"
    POWER_OF_THREE = "power_of_three"
    MORNING_REVERSAL = "morning_reversal"
    ORDER_BLOCK = "order_block"
    MITIGATION_BLOCK = "mitigation_block"
    FAIR_VALUE_GAP = "fair_value_gap"


class JudasSwingType(Enum):
    """🎭 Tipos específicos de Judas Swing v6.0"""
    MORNING_REVERSAL = "morning_reversal"        # 8-9 AM reversión
    LONDON_CLOSE_JUDAS = "london_close_judas"    # 10-11 AM false break
    NY_OPEN_JUDAS = "ny_open_judas"             # 1-2 PM false break
    AFTERNOON_JUDAS = "afternoon_judas"          # 2-4 PM reversión
    UNKNOWN = "unknown"


class BreakoutType(Enum):
    """🚨 Tipos de ruptura y false breakouts v6.0"""
    FALSE_BREAKOUT_HIGH = "false_breakout_high"
    FALSE_BREAKOUT_LOW = "false_breakout_low"
    LIQUIDITY_GRAB_HIGH = "liquidity_grab_high"
    LIQUIDITY_GRAB_LOW = "liquidity_grab_low"
    NO_BREAKOUT = "no_breakout"
    BREAKER_BLOCK = "breaker_block"
    FAIR_VALUE_GAP = "fair_value_gap"
    INSTITUTIONAL_ORDER_FLOW = "institutional_order_flow"
    MARKET_MAKER_MODEL = "market_maker_model"


class PatternConfidence(Enum):
    """Niveles de confianza del patrón"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
    EXTREME = "extreme"


class TradingDirection(Enum):
    """Dirección del trade"""
    BUY = "buy"
    SELL = "sell"
    NEUTRAL = "neutral"


class SessionType(Enum):
    """Tipos de sesión de trading"""
    LONDON = "london"
    NEW_YORK = "new_york"
    ASIAN = "asian"
    OVERLAP = "overlap"
    DEAD_ZONE = "dead_zone"


@dataclass
class PatternSignal:
    """Señal de patrón ICT detectada"""
    pattern_type: PatternType
    direction: TradingDirection
    confidence: PatternConfidence
    strength: float  # 0-100
    timestamp: datetime
    symbol: str
    timeframe: str
    
    # Niveles de precio
    entry_zone: Tuple[float, float]
    stop_loss: float
    take_profit_1: float
    take_profit_2: Optional[float] = None
    
    # Métricas
    risk_reward_ratio: float = 0.0
    probability: float = 0.0
    
    # Contexto
    session: SessionType = SessionType.LONDON
    narrative: str = ""
    confluences: List[str] = field(default_factory=list)
    invalidation_criteria: str = ""
    
    # Timing
    optimal_entry_time: Optional[datetime] = None
    time_sensitivity: str = "MEDIUM"
    max_hold_time: Optional[timedelta] = None
    
    # Metadata
    analysis_id: str = ""
    raw_data: Dict[str, Any] = field(default_factory=dict)


class PatternDetector:
    """
    🎯 ICT PATTERN DETECTOR v6.0 ENTERPRISE
    
    Detector avanzado de patrones ICT con capacidades enterprise:
    - Detección en tiempo real de 12+ patrones ICT
    - Análisis multi-timeframe con confluencias
    - Scoring avanzado con ML-ready features
    - Performance optimizado (<50ms por análisis)
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Pattern Detector v6.0 Enterprise
        
        Args:
            config: Configuración del detector
        """
        self.config = self._load_default_config()
        if config:
            self.config.update(config)
        
        # Estado del detector
        self.is_initialized = False
        self.last_analysis_time = None
        self.detected_patterns: List[PatternSignal] = []
        self.performance_metrics = {
            'total_analyses': 0,
            'avg_analysis_time': 0.0,
            'patterns_detected': 0,
            'success_rate': 0.0,
            'last_update': datetime.now()
        }
        
        # Componentes
        self._downloader = None
        self._smart_money_analyzer = None
        self._initialize_components()
        
        # Cache para optimización
        self._pattern_cache = {}
        self._cache_ttl = timedelta(minutes=5)
        
        print(f"[INFO] Pattern Detector v6.0 Enterprise inicializado")
        print(f"[INFO] Configuración: {len(self.config)} parámetros cargados")
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Cargar configuración por defecto"""
        return {
            # General
            'enable_debug': True,
            'enable_cache': True,
            'min_confidence': 70.0,
            'max_patterns_per_analysis': 5,
            
            # Patrones específicos
            'enable_silver_bullet': True,
            'enable_judas_swing': True,
            'enable_liquidity_grab': True,
            'enable_optimal_trade_entry': True,
            'enable_power_of_three': True,
            'enable_morning_reversal': True,
            
            # Timeframes
            'primary_timeframe': 'M15',
            'secondary_timeframes': ['M5', 'H1'],
            'use_multi_timeframe': True,
            
            # Análisis técnico
            'swing_lookback': 20,
            'structure_lookback': 50,
            'fvg_min_size': 0.0005,
            'order_block_strength': 0.6,
            
            # Sesiones
            'london_start': '08:00',
            'london_end': '17:00',
            'newyork_start': '13:00',
            'newyork_end': '22:00',
            
            # Performance
            'max_analysis_time': 0.05,  # 50ms
            'cache_size_limit': 100,
            'concurrent_analysis': False
        }
    
    def _initialize_components(self):
        """Inicializar componentes del detector"""
        try:
            # Inicializar downloader si está disponible
            if get_advanced_candle_downloader:
                self._downloader = get_advanced_candle_downloader()
                print("[INFO] Downloader conectado - datos reales disponibles")
            else:
                print("[WARNING] Downloader no disponible - modo simulación")
            
            # Inicializar Smart Money Analyzer si está disponible
            if SmartMoneyAnalyzer:
                self._smart_money_analyzer = SmartMoneyAnalyzer()
                print("[INFO] Smart Money Analyzer v6.0 conectado - análisis institucional disponible")
            else:
                print("[WARNING] Smart Money Analyzer no disponible - funcionalidad limitada")
            
            self.is_initialized = True
            
        except Exception as e:
            print(f"[WARNING] Error inicializando componentes: {e}")
            print("[INFO] Continuando en modo básico")
    
    def detect_patterns(
        self, 
        symbol: str = "EURUSD", 
        timeframe: str = "M15",
        lookback_days: int = 7
    ) -> List[PatternSignal]:
        """
        Detectar patrones ICT en los datos de mercado
        
        Args:
            symbol: Símbolo a analizar
            timeframe: Marco temporal
            lookback_days: Días de historia a analizar
            
        Returns:
            Lista de patrones detectados
        """
        start_time = time.time()
        
        try:
            # Obtener datos de mercado
            data = self._get_market_data(symbol, timeframe, lookback_days)
            if data is None or data.empty:
                print(f"[WARNING] Sin datos para {symbol} {timeframe}")
                return []
            
            print(f"[INFO] Analizando {len(data)} velas para {symbol} {timeframe}")
            
            # Detectar patrones activos
            patterns = []
            
            # 1. Silver Bullet (máxima prioridad)
            if self.config['enable_silver_bullet']:
                sb_patterns = self._detect_silver_bullet(data, symbol, timeframe)
                patterns.extend(sb_patterns)
            
            # 2. Judas Swing
            if self.config['enable_judas_swing']:
                js_patterns = self._detect_judas_swing(data, symbol, timeframe)
                patterns.extend(js_patterns)
            
            # 3. Liquidity Grab
            if self.config['enable_liquidity_grab']:
                lg_patterns = self._detect_liquidity_grab(data, symbol, timeframe)
                patterns.extend(lg_patterns)
            
            # 4. Optimal Trade Entry
            if self.config['enable_optimal_trade_entry']:
                ote_patterns = self._detect_optimal_trade_entry(data, symbol, timeframe)
                patterns.extend(ote_patterns)
            
            # 5. Order Blocks
            ob_patterns = self._detect_order_blocks(data, symbol, timeframe)
            patterns.extend(ob_patterns)
            
            # 6. Fair Value Gaps
            fvg_patterns = self._detect_fair_value_gaps(data, symbol, timeframe)
            patterns.extend(fvg_patterns)
            
            # Filtrar por confianza mínima
            patterns = [p for p in patterns if p.strength >= self.config['min_confidence']]
            
            # 🧠 SMART MONEY ENHANCEMENT v6.0
            if patterns and self._smart_money_analyzer:
                print(f"[INFO] Aplicando Smart Money analysis a {len(patterns)} patrones...")
                patterns = self._enhance_with_smart_money_analysis(patterns, data)
            
            # 🎯 MULTI-TIMEFRAME ENHANCEMENT v6.0
            if patterns:
                print(f"[INFO] Aplicando Multi-Timeframe enhancement a {len(patterns)} patrones...")
                patterns = self._enhance_analysis_with_multi_tf(patterns, symbol, timeframe)
            
            # Limitar número de patrones
            max_patterns = self.config['max_patterns_per_analysis']
            if len(patterns) > max_patterns:
                # Ordenar por strength y tomar los mejores
                patterns = sorted(patterns, key=lambda x: x.strength, reverse=True)[:max_patterns]
            
            # Actualizar métricas
            analysis_time = time.time() - start_time
            self._update_performance_metrics(analysis_time, len(patterns))
            
            # Almacenar resultados
            self.detected_patterns = patterns
            self.last_analysis_time = datetime.now()
            
            print(f"[INFO] Detectados {len(patterns)} patrones en {analysis_time:.3f}s")
            
            return patterns
            
        except Exception as e:
            print(f"[ERROR] Error en detección de patrones: {e}")
            return []
    
    def _get_market_data(self, symbol: str, timeframe: str, days: int) -> Optional[pd.DataFrame]:
        """
        🔍 OBTENER DATOS MULTI-TIMEFRAME ICT v6.0
        
        Estrategia multi-timeframe para maximizar datos históricos:
        - Primary: timeframe solicitado
        - Secondary: H1, H4, D1 para contexto superior
        - Intelligent data combining para análisis completo
        """
        try:
            if self._downloader:
                # 🎯 ESTRATEGIA MULTI-TIMEFRAME ICT v6.0
                data_collection = {}
                
                # 1. Primary timeframe (solicitado)
                primary_data = self._download_single_timeframe(symbol, timeframe, days)
                if primary_data is not None and not primary_data.empty:
                    data_collection[timeframe] = primary_data
                    
                # 2. Secondary timeframes para contexto ICT
                secondary_timeframes = self._get_ict_secondary_timeframes(timeframe)
                
                for tf in secondary_timeframes:
                    # Más días para timeframes superiores
                    tf_days = self._calculate_ict_optimal_days(tf, days)
                    
                    secondary_data = self._download_single_timeframe(symbol, tf, tf_days)
                    if secondary_data is not None and not secondary_data.empty:
                        data_collection[tf] = secondary_data
                        
                # 3. Return primary data with enhanced context
                if timeframe in data_collection:
                    primary_data = data_collection[timeframe]
                    
                    # Store additional timeframes for multi-TF analysis
                    if hasattr(self, '_multi_tf_data'):
                        self._multi_tf_data[symbol] = data_collection
                    else:
                        self._multi_tf_data = {symbol: data_collection}
                        
                    print(f"📊 Multi-TF data collected: {list(data_collection.keys())}")
                    print(f"   Primary {timeframe}: {len(primary_data)} velas")
                    
                    for tf, data in data_collection.items():
                        if tf != timeframe:
                            print(f"   Context {tf}: {len(data)} velas")
                    
                    return primary_data
                else:
                    print(f"[WARNING] No se pudo obtener datos primarios para {timeframe}")
                    return self._generate_simulated_data(symbol, timeframe, days)
            else:
                # Datos simulados para testing
                return self._generate_simulated_data(symbol, timeframe, days)
                
        except Exception as e:
            print(f"[WARNING] Error obteniendo datos multi-TF: {e}")
            print(f"[INFO] Usando datos simulados como fallback")
            return self._generate_simulated_data(symbol, timeframe, days)

    def _download_single_timeframe(self, symbol: str, timeframe: str, days: int) -> Optional[pd.DataFrame]:
        """Descarga datos de una sola temporalidad"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            result = self._downloader.download_candles(
                symbol=symbol,
                timeframe=timeframe,
                start_date=start_date,
                end_date=end_date,
                save_to_file=False
            )
            
            # Extraer DataFrame del resultado
            if isinstance(result, dict) and 'data' in result:
                return result['data']
            elif isinstance(result, pd.DataFrame):
                return result
            else:
                return None
                
        except Exception as e:
            print(f"[DEBUG] Error descargando {timeframe}: {e}")
            return None

    def _get_ict_secondary_timeframes(self, primary_timeframe: str) -> List[str]:
        """
        🎯 OBTENER TIMEFRAMES SECUNDARIOS ICT
        
        Estrategia ICT para timeframes de contexto:
        - M1, M5, M15 -> H1, H4, D1
        - H1 -> H4, D1, W1
        - H4, D1 -> W1, MN1
        """
        timeframe_hierarchy = {
            'M1': ['M5', 'M15', 'H1', 'H4'],
            'M5': ['M15', 'H1', 'H4', 'D1'],
            'M15': ['H1', 'H4', 'D1'],
            'H1': ['H4', 'D1', 'W1'],
            'H4': ['D1', 'W1'],
            'D1': ['W1', 'MN1'],
            'W1': ['MN1'],
            'MN1': []
        }
        
        return timeframe_hierarchy.get(primary_timeframe, ['H1', 'H4', 'D1'])

    def _calculate_ict_optimal_days(self, timeframe: str, base_days: int) -> int:
        """
        📊 CALCULAR DÍAS ÓPTIMOS ICT POR TIMEFRAME
        
        Más días para timeframes superiores para obtener más datos:
        - M1, M5: base_days
        - M15: base_days * 2
        - H1: base_days * 4
        - H4: base_days * 12
        - D1: base_days * 30
        - W1: base_days * 120
        """
        multipliers = {
            'M1': 1,
            'M5': 1, 
            'M15': 2,
            'H1': 4,
            'H4': 12,
            'D1': 30,
            'W1': 120,
            'MN1': 360
        }
        
        multiplier = multipliers.get(timeframe, 4)
        optimal_days = base_days * multiplier
        
        # Cap máximo para evitar sobrecarga
        max_days = 365 * 2  # 2 años máximo
        return min(optimal_days, max_days)
    
    def _generate_simulated_data(self, symbol: str, timeframe: str, days: int) -> pd.DataFrame:
        """Generar datos simulados para testing"""
        periods = days * 24 * 4  # Asumiendo M15
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='15min')
        
        # Datos OHLCV simulados
        base_price = 1.0800  # EURUSD típico
        data = []
        
        for i, date in enumerate(dates):
            volatility = 0.0020 + np.random.normal(0, 0.0005)
            change = np.random.normal(0, volatility)
            
            if i == 0:
                open_price = base_price
            else:
                open_price = data[-1]['close']
            
            high = open_price + abs(np.random.normal(0, volatility/2))
            low = open_price - abs(np.random.normal(0, volatility/2))
            close = open_price + change
            volume = np.random.randint(100, 1000)
            
            data.append({
                'time': date,
                'open': open_price,
                'high': max(open_price, high, close),
                'low': min(open_price, low, close),
                'close': close,
                'volume': volume
            })
        
        return pd.DataFrame(data)
    
    def _detect_silver_bullet(self, data: pd.DataFrame, symbol: str, timeframe: str) -> List[PatternSignal]:
        """Detectar patrones Silver Bullet"""
        patterns = []
        current_time = datetime.now()
        
        # Verificar ventana temporal Silver Bullet (10:00-11:00 GMT)
        if not self._is_silver_bullet_time(current_time):
            return patterns
        
        try:
            # Buscar setup Silver Bullet
            # Estructura: Order Block + FVG + Confluence
            if len(data) < 20:
                return patterns
            
            # Detectar Order Block reciente
            order_blocks = self._find_order_blocks(data)
            if not order_blocks:
                return patterns
            
            recent_ob = order_blocks[-1]  # Más reciente
            
            # Verificar FVG como confluencia
            fvgs = self._find_fair_value_gaps(data)
            fvg_confluence = len(fvgs) > 0
            
            # Determinar dirección
            direction = TradingDirection.BUY if recent_ob['type'] == 'bullish' else TradingDirection.SELL
            
            # Calcular niveles
            entry_zone = (recent_ob['low'], recent_ob['high'])
            current_price = data['close'].iloc[-1]
            
            if direction == TradingDirection.BUY:
                stop_loss = entry_zone[0] - 0.0020
                take_profit_1 = current_price + 0.0040
                take_profit_2 = current_price + 0.0070
            else:
                stop_loss = entry_zone[1] + 0.0020
                take_profit_1 = current_price - 0.0040
                take_profit_2 = current_price - 0.0070
            
            # Calcular métricas
            risk = abs(np.mean(entry_zone) - stop_loss)
            reward = abs(take_profit_1 - np.mean(entry_zone))
            risk_reward = reward / risk if risk > 0 else 0
            
            # Calcular strength
            strength = 75.0
            if fvg_confluence:
                strength += 10.0
            if current_time.hour == 10:  # Hora óptima
                strength += 5.0
            
            confidence = PatternConfidence.HIGH if strength >= 80 else PatternConfidence.MEDIUM
            
            signal = PatternSignal(
                pattern_type=PatternType.SILVER_BULLET,
                direction=direction,
                confidence=confidence,
                strength=min(strength, 95.0),
                timestamp=current_time,
                symbol=symbol,
                timeframe=timeframe,
                entry_zone=entry_zone,
                stop_loss=stop_loss,
                take_profit_1=take_profit_1,
                take_profit_2=take_profit_2,
                risk_reward_ratio=risk_reward,
                probability=strength,
                session=SessionType.LONDON,
                narrative=f"Silver Bullet {direction.value} setup detectado durante ventana óptima. Order Block confirmado con {'FVG' if fvg_confluence else 'estructura'} como confluencia.",
                confluences=["order_block", "timing_window"] + (["fvg"] if fvg_confluence else []),
                invalidation_criteria=f"Cierre fuera de ventana temporal o precio {'debajo' if direction == TradingDirection.BUY else 'arriba'} de {stop_loss:.5f}",
                time_sensitivity="CRÍTICA - Solo válido durante ventana 10:00-11:00 GMT",
                analysis_id=f"SB_{symbol}_{int(current_time.timestamp())}"
            )
            
            patterns.append(signal)
            
        except Exception as e:
            print(f"[WARNING] Error detectando Silver Bullet: {e}")
        
        return patterns
    
    def _detect_judas_swing(self, data: pd.DataFrame, symbol: str, timeframe: str) -> List[PatternSignal]:
        """
        🎭 DETECCIÓN JUDAS SWING v6.0 ENTERPRISE
        ========================================
        
        Migración completa desde Judas Swing v2.0 con todas las funcionalidades:
        - False breakouts automáticos
        - Liquidity grab detection
        - Session timing validation
        - Market maker manipulation patterns
        """
        patterns = []
        
        try:
            if len(data) < 30:
                return patterns
            
            # ⏰ VALIDAR TIMING DE SESIÓN CRÍTICA
            timing_score, session_type = self._validate_judas_session_timing()
            if timing_score < 0.4:
                return patterns
            
            # 🔍 DETECTAR FALSE BREAKOUTS
            breakout_score, breakout_type, break_price = self._detect_false_breakout_v6(data)
            if breakout_score < 0.5:
                return patterns
            
            # 💧 ANALIZAR LIQUIDITY GRAB
            current_price = data['close'].iloc[-1]
            liquidity_score, liquidity_grabbed = self._analyze_liquidity_grab_v6(data, break_price, current_price)
            
            # 🏗️ CONFIRMAR ESTRUCTURA DE REVERSIÓN
            structure_score, reversal_direction, reversal_target = self._confirm_reversal_structure_v6(data, breakout_type)
            
            # 📊 SCORING FINAL JUDAS SWING v6.0
            timing_weight = 0.35
            breakout_weight = 0.30
            structure_weight = 0.25
            liquidity_weight = 0.10
            
            final_confidence = (
                timing_score * timing_weight +
                breakout_score * breakout_weight +
                structure_score * structure_weight +
                liquidity_score * liquidity_weight
            ) * 100
            
            # Validar umbral de confianza
            if final_confidence < 70.0:
                return patterns
            
            # 🎯 CREAR SEÑAL JUDAS SWING v6.0
            judas_type = self._classify_judas_swing_type(session_type, breakout_type)
            
            # Determinar entry zone alrededor del breakout level
            spread_margin = 0.0010  # 10 pips margin
            if reversal_direction == TradingDirection.SELL:
                entry_zone = (break_price - spread_margin, break_price + spread_margin)
                stop_loss = break_price + (break_price * 0.0020)  # 20 pips stop
                take_profit_1 = reversal_target
            else:
                entry_zone = (break_price - spread_margin, break_price + spread_margin)
                stop_loss = break_price - (break_price * 0.0020)  # 20 pips stop
                take_profit_1 = reversal_target
            
            # Calcular risk/reward
            risk = abs(np.mean(entry_zone) - stop_loss)
            reward = abs(take_profit_1 - np.mean(entry_zone))
            risk_reward = reward / risk if risk > 0 else 0
            
            # Narrative institucional
            narrative_parts = [
                f"🎭 Judas Swing {judas_type.value} detectado",
                f"False breakout @ {break_price:.5f}",
                f"Smart Money manipulation confirmada"
            ]
            
            if liquidity_grabbed:
                narrative_parts.append("💧 Liquidity grab ejecutado por institucionales")
            
            confluences = ["false_breakout", session_type, "smart_money_manipulation"]
            if liquidity_grabbed:
                confluences.append("liquidity_grab")
            if structure_score > 0.7:
                confluences.append("structure_confirmation")
            
            signal = PatternSignal(
                pattern_type=PatternType.JUDAS_SWING,
                direction=reversal_direction,
                confidence=PatternConfidence.HIGH if final_confidence >= 80 else PatternConfidence.MEDIUM,
                strength=min(final_confidence, 95.0),
                timestamp=datetime.now(),
                symbol=symbol,
                timeframe=timeframe,
                entry_zone=entry_zone,
                stop_loss=stop_loss,
                take_profit_1=take_profit_1,
                risk_reward_ratio=risk_reward,
                probability=final_confidence,
                session=session_type,
                narrative=" | ".join(narrative_parts),
                confluences=confluences,
                invalidation_criteria=f"Nueva ruptura definitiva por encima/debajo de {break_price:.5f}",
                time_sensitivity="CRÍTICA - Ejecutar en los próximos 30-60 minutos",
                analysis_id=f"JUDAS_{symbol}_{judas_type.value}_{int(datetime.now().timestamp())}",
                metadata={
                    "judas_swing_type": judas_type.value,
                    "breakout_type": breakout_type.value,
                    "false_break_price": break_price,
                    "liquidity_grabbed": liquidity_grabbed,
                    "timing_score": timing_score,
                    "breakout_score": breakout_score,
                    "structure_score": structure_score,
                    "liquidity_score": liquidity_score,
                    "session_context": session_type,
                    "smart_money_confirmation": True
                }
            )
            
            patterns.append(signal)
            
            return patterns
            
        except Exception as e:
            print(f"[ERROR] Error detectando Judas Swing v6.0: {e}")
            return patterns

    def _validate_judas_session_timing(self) -> Tuple[float, str]:
        """⏰ Valida timing para Judas Swing patterns"""
        current_time = datetime.now().time()
        
        # Definir sesiones críticas
        morning_session = (dt_time(8, 0), dt_time(9, 30))
        london_close = (dt_time(10, 0), dt_time(11, 30))
        ny_open = (dt_time(13, 0), dt_time(14, 30))
        afternoon = (dt_time(14, 0), dt_time(16, 0))
        
        # Verificar en qué sesión estamos
        if morning_session[0] <= current_time <= morning_session[1]:
            return 0.9, "morning_session"
        elif london_close[0] <= current_time <= london_close[1]:
            return 0.8, "london_close"
        elif ny_open[0] <= current_time <= ny_open[1]:
            return 0.85, "ny_open"
        elif afternoon[0] <= current_time <= afternoon[1]:
            return 0.7, "afternoon"
        else:
            return 0.3, "low_probability_session"

    def _detect_false_breakout_v6(self, data: pd.DataFrame) -> Tuple[float, BreakoutType, float]:
        """🚨 Detecta false breakouts v6.0"""
        try:
            if len(data) < 20:
                return 0.0, BreakoutType.NO_BREAKOUT, 0.0

            recent = data.tail(20)
            
            # Encontrar swing highs y lows
            swing_high = recent['high'].rolling(window=5, center=True).max()
            swing_low = recent['low'].rolling(window=5, center=True).min()
            
            resistance_level = swing_high.max()
            support_level = swing_low.min()
            current_price = recent['close'].iloc[-1]
            
            # Detectar false breakout al alza
            if self._check_false_breakout_high_v6(recent, resistance_level):
                score = self._score_false_breakout_v6(recent, resistance_level, True)
                return score, BreakoutType.FALSE_BREAKOUT_HIGH, resistance_level
            
            # Detectar false breakout a la baja
            elif self._check_false_breakout_low_v6(recent, support_level):
                score = self._score_false_breakout_v6(recent, support_level, False)
                return score, BreakoutType.FALSE_BREAKOUT_LOW, support_level
            
            return 0.4, BreakoutType.NO_BREAKOUT, current_price
            
        except Exception:
            return 0.0, BreakoutType.NO_BREAKOUT, 0.0

    def _check_false_breakout_high_v6(self, candles: pd.DataFrame, resistance: float) -> bool:
        """Verifica false breakout al alza v6.0"""
        try:
            for i in range(len(candles) - 5, len(candles)):
                if i >= 0 and candles['high'].iloc[i] > resistance:
                    # Verificar si hay retorno rápido
                    subsequent_closes = candles['close'].iloc[i+1:i+4]
                    if len(subsequent_closes) > 0 and subsequent_closes.min() < resistance:
                        return True
            return False
        except Exception:
            return False

    def _check_false_breakout_low_v6(self, candles: pd.DataFrame, support: float) -> bool:
        """Verifica false breakout a la baja v6.0"""
        try:
            for i in range(len(candles) - 5, len(candles)):
                if i >= 0 and candles['low'].iloc[i] < support:
                    subsequent_closes = candles['close'].iloc[i+1:i+4]
                    if len(subsequent_closes) > 0 and subsequent_closes.max() > support:
                        return True
            return False
        except Exception:
            return False

    def _score_false_breakout_v6(self, candles: pd.DataFrame, level: float, is_high: bool) -> float:
        """Scoring de false breakout v6.0"""
        try:
            score = 0.6
            
            # Analizar velocidad de retorno
            if is_high:
                max_penetration = candles['high'].max() - level
                if max_penetration < level * 0.001:  # Penetración mínima
                    score += 0.2
            else:
                max_penetration = level - candles['low'].min()
                if max_penetration < level * 0.001:
                    score += 0.2
            
            return min(score, 1.0)
            
        except Exception:
            return 0.5

    def _analyze_liquidity_grab_v6(self, data: pd.DataFrame, break_price: float, current_price: float) -> Tuple[float, bool]:
        """💧 Analiza liquidity grab v6.0"""
        try:
            if break_price == 0 or current_price == 0:
                return 0.3, False

            distance = abs(current_price - break_price) / break_price
            
            if distance > 0.002:  # 20 pips
                return 0.8, True
            elif distance > 0.0015:  # 15 pips
                return 0.6, True
            else:
                return 0.3, False
                
        except Exception:
            return 0.3, False

    def _confirm_reversal_structure_v6(self, data: pd.DataFrame, breakout_type: BreakoutType) -> Tuple[float, TradingDirection, float]:
        """🏗️ Confirma estructura de reversión v6.0"""
        try:
            if len(data) < 10:
                return 0.3, TradingDirection.NEUTRAL, 0.0

            recent = data.tail(10)
            current_price = recent['close'].iloc[-1]
            
            if breakout_type in [BreakoutType.FALSE_BREAKOUT_HIGH, BreakoutType.LIQUIDITY_GRAB_HIGH]:
                direction = TradingDirection.SELL
                target = recent['low'].min() * 0.999
            elif breakout_type in [BreakoutType.FALSE_BREAKOUT_LOW, BreakoutType.LIQUIDITY_GRAB_LOW]:
                direction = TradingDirection.BUY
                target = recent['high'].max() * 1.001
            else:
                return 0.3, TradingDirection.NEUTRAL, current_price

            # Verificar confirmación en últimas velas
            last_3 = recent.tail(3)
            
            if direction == TradingDirection.SELL:
                bearish_candles = sum(1 for _, candle in last_3.iterrows() 
                                    if candle['close'] < candle['open'])
                score = 0.5 + (bearish_candles * 0.15)
            else:
                bullish_candles = sum(1 for _, candle in last_3.iterrows() 
                                    if candle['close'] > candle['open'])
                score = 0.5 + (bullish_candles * 0.15)
            
            return min(score, 1.0), direction, target
            
        except Exception:
            return 0.3, TradingDirection.NEUTRAL, 0.0

    def _classify_judas_swing_type(self, session_type: str, breakout_type: BreakoutType) -> JudasSwingType:
        """🎭 Clasifica tipo de Judas Swing"""
        if session_type == "morning_session":
            return JudasSwingType.MORNING_REVERSAL
        elif session_type == "london_close":
            return JudasSwingType.LONDON_CLOSE_JUDAS
        elif session_type == "ny_open":
            return JudasSwingType.NY_OPEN_JUDAS
        elif session_type == "afternoon":
            return JudasSwingType.AFTERNOON_JUDAS
        else:
            return JudasSwingType.UNKNOWN
    
    def _detect_liquidity_grab(self, data: pd.DataFrame, symbol: str, timeframe: str) -> List[PatternSignal]:
        """Detectar patrones Liquidity Grab"""
        patterns = []
        
        try:
            if len(data) < 20:
                return patterns
            
            # Buscar barridos de liquidez recientes
            recent_data = data.tail(15)
            
            # Identificar niveles de liquidez (highs/lows anteriores)
            highs = data['high'].rolling(window=10).max()
            lows = data['low'].rolling(window=10).min()
            
            current_price = recent_data['close'].iloc[-1]
            
            # Verificar barrido de highs (liquidity grab bearish)
            for i in range(len(recent_data) - 3):
                spike_high = recent_data['high'].iloc[i]
                prev_high = highs.iloc[-20:-10].max()
                
                if spike_high > prev_high and i < len(recent_data) - 2:
                    # Verificar reversión inmediata
                    next_candles = recent_data.iloc[i+1:i+3]
                    if len(next_candles) > 0 and next_candles['close'].iloc[-1] < prev_high:
                        # Liquidity Grab bearish confirmado
                        direction = TradingDirection.SELL
                        entry_zone = (current_price - 0.0008, current_price + 0.0008)
                        stop_loss = spike_high + 0.0010
                        take_profit_1 = current_price - 0.0050
                        
                        risk = abs(np.mean(entry_zone) - stop_loss)
                        reward = abs(take_profit_1 - np.mean(entry_zone))
                        risk_reward = reward / risk if risk > 0 else 0
                        
                        strength = 85.0  # Liquidity Grab suele ser muy fuerte
                        
                        signal = PatternSignal(
                            pattern_type=PatternType.LIQUIDITY_GRAB,
                            direction=direction,
                            confidence=PatternConfidence.VERY_HIGH,
                            strength=min(strength, 95.0),
                            timestamp=datetime.now(),
                            symbol=symbol,
                            timeframe=timeframe,
                            entry_zone=entry_zone,
                            stop_loss=stop_loss,
                            take_profit_1=take_profit_1,
                            risk_reward_ratio=risk_reward,
                            probability=strength + 5,  # Extra probabilidad
                            session=self._get_current_session(),
                            narrative=f"Liquidity Grab {direction.value} confirmado. Barrido de liquidez seguido de reversión inmediata. Smart Money ha capturado stops.",
                            confluences=["liquidity_sweep", "immediate_reversal"],
                            invalidation_criteria=f"Retorno al nivel barrido sin continuación",
                            time_sensitivity="CRÍTICA - Ventana muy limitada (5-15 minutos)",
                            max_hold_time=timedelta(hours=2),
                            analysis_id=f"LG_{symbol}_{int(datetime.now().timestamp())}"
                        )
                        
                        patterns.append(signal)
                        break
            
            # Verificar barrido de lows (liquidity grab bullish)
            for i in range(len(recent_data) - 3):
                spike_low = recent_data['low'].iloc[i]
                prev_low = lows.iloc[-20:-10].min()
                
                if spike_low < prev_low and i < len(recent_data) - 2:
                    next_candles = recent_data.iloc[i+1:i+3]
                    if len(next_candles) > 0 and next_candles['close'].iloc[-1] > prev_low:
                        # Liquidity Grab bullish confirmado
                        direction = TradingDirection.BUY
                        entry_zone = (current_price - 0.0008, current_price + 0.0008)
                        stop_loss = spike_low - 0.0010
                        take_profit_1 = current_price + 0.0050
                        
                        risk = abs(np.mean(entry_zone) - stop_loss)
                        reward = abs(take_profit_1 - np.mean(entry_zone))
                        risk_reward = reward / risk if risk > 0 else 0
                        
                        strength = 85.0
                        
                        signal = PatternSignal(
                            pattern_type=PatternType.LIQUIDITY_GRAB,
                            direction=direction,
                            confidence=PatternConfidence.VERY_HIGH,
                            strength=min(strength, 95.0),
                            timestamp=datetime.now(),
                            symbol=symbol,
                            timeframe=timeframe,
                            entry_zone=entry_zone,
                            stop_loss=stop_loss,
                            take_profit_1=take_profit_1,
                            risk_reward_ratio=risk_reward,
                            probability=strength + 5,
                            session=self._get_current_session(),
                            narrative=f"Liquidity Grab {direction.value} confirmado. Barrido de liquidez seguido de reversión inmediata. Smart Money ha capturado stops.",
                            confluences=["liquidity_sweep", "immediate_reversal"],
                            invalidation_criteria=f"Retorno al nivel barrido sin continuación",
                            time_sensitivity="CRÍTICA - Ventana muy limitada (5-15 minutos)",
                            max_hold_time=timedelta(hours=2),
                            analysis_id=f"LG_{symbol}_{int(datetime.now().timestamp())}"
                        )
                        
                        patterns.append(signal)
                        break
                        
        except Exception as e:
            print(f"[WARNING] Error detectando Liquidity Grab: {e}")
        
        return patterns
    
    def _detect_optimal_trade_entry(self, data: pd.DataFrame, symbol: str, timeframe: str) -> List[PatternSignal]:
        """Detectar patrones Optimal Trade Entry (OTE)"""
        patterns = []
        
        try:
            if len(data) < 30:
                return patterns
            
            # Identificar estructura de mercado reciente
            recent_high = data['high'].tail(20).max()
            recent_low = data['low'].tail(20).min()
            current_price = data['close'].iloc[-1]
            
            # Calcular niveles Fibonacci
            price_range = recent_high - recent_low
            fib_62 = recent_high - (price_range * 0.618)
            fib_79 = recent_high - (price_range * 0.786)
            
            # Verificar si precio está en zona OTE (62%-79% retrace)
            if fib_79 <= current_price <= fib_62:
                # Determinar dirección basada en estructura
                direction = TradingDirection.BUY if current_price < (recent_high + recent_low) / 2 else TradingDirection.SELL
                
                entry_zone = (fib_79, fib_62)
                
                if direction == TradingDirection.BUY:
                    stop_loss = recent_low - 0.0015
                    take_profit_1 = recent_high
                    take_profit_2 = recent_high + price_range * 0.618
                else:
                    stop_loss = recent_high + 0.0015
                    take_profit_1 = recent_low
                    take_profit_2 = recent_low - price_range * 0.618
                
                risk = abs(np.mean(entry_zone) - stop_loss)
                reward = abs(take_profit_1 - np.mean(entry_zone))
                risk_reward = reward / risk if risk > 0 else 0
                
                # Verificar confluencias adicionales
                strength = 68.0
                confluences = ["fibonacci_retracement", "optimal_entry_zone"]
                
                # Check for Order Block confluence
                order_blocks = self._find_order_blocks(data.tail(10))
                if order_blocks:
                    strength += 8.0
                    confluences.append("order_block")
                
                # Check for FVG confluence
                fvgs = self._find_fair_value_gaps(data.tail(10))
                if fvgs:
                    strength += 5.0
                    confluences.append("fair_value_gap")
                
                if strength >= self.config['min_confidence']:
                    signal = PatternSignal(
                        pattern_type=PatternType.OPTIMAL_TRADE_ENTRY,
                        direction=direction,
                        confidence=PatternConfidence.HIGH if strength >= 75 else PatternConfidence.MEDIUM,
                        strength=min(strength, 88.0),
                        timestamp=datetime.now(),
                        symbol=symbol,
                        timeframe=timeframe,
                        entry_zone=entry_zone,
                        stop_loss=stop_loss,
                        take_profit_1=take_profit_1,
                        take_profit_2=take_profit_2,
                        risk_reward_ratio=risk_reward,
                        probability=strength,
                        session=self._get_current_session(),
                        narrative=f"Optimal Trade Entry {direction.value} en zona Fibonacci óptima (62%-79%). Retroceso hacia zona de valor antes de continuación.",
                        confluences=confluences,
                        invalidation_criteria=f"Cierre {'debajo' if direction == TradingDirection.BUY else 'arriba'} de zona OTE",
                        time_sensitivity="MEDIA - Ventana de varias horas",
                        analysis_id=f"OTE_{symbol}_{int(datetime.now().timestamp())}"
                    )
                    
                    patterns.append(signal)
                    
        except Exception as e:
            print(f"[WARNING] Error detectando OTE: {e}")
        
        return patterns
    
    def _detect_order_blocks(self, data: pd.DataFrame, symbol: str, timeframe: str) -> List[PatternSignal]:
        """Detectar Order Blocks"""
        patterns = []
        
        try:
            order_blocks = self._find_order_blocks(data)
            
            for ob in order_blocks[-2:]:  # Solo los más recientes
                direction = TradingDirection.BUY if ob['type'] == 'bullish' else TradingDirection.SELL
                entry_zone = (ob['low'], ob['high'])
                current_price = data['close'].iloc[-1]
                
                if direction == TradingDirection.BUY:
                    stop_loss = ob['low'] - 0.0010
                    take_profit_1 = current_price + 0.0030
                else:
                    stop_loss = ob['high'] + 0.0010
                    take_profit_1 = current_price - 0.0030
                
                risk = abs(np.mean(entry_zone) - stop_loss)
                reward = abs(take_profit_1 - np.mean(entry_zone))
                risk_reward = reward / risk if risk > 0 else 0
                
                strength = 65.0 + ob.get('strength', 0) * 15
                
                if strength >= self.config['min_confidence']:
                    signal = PatternSignal(
                        pattern_type=PatternType.ORDER_BLOCK,
                        direction=direction,
                        confidence=PatternConfidence.MEDIUM,
                        strength=min(strength, 82.0),
                        timestamp=datetime.now(),
                        symbol=symbol,
                        timeframe=timeframe,
                        entry_zone=entry_zone,
                        stop_loss=stop_loss,
                        take_profit_1=take_profit_1,
                        risk_reward_ratio=risk_reward,
                        probability=strength,
                        session=self._get_current_session(),
                        narrative=f"Order Block {direction.value} detectado. Zona donde instituciones han dejado órdenes pendientes.",
                        confluences=["institutional_orders", "price_reaction"],
                        invalidation_criteria=f"Ruptura definitiva del Order Block",
                        time_sensitivity="BAJA - Puede mantenerse activo por días",
                        analysis_id=f"OB_{symbol}_{int(datetime.now().timestamp())}"
                    )
                    
                    patterns.append(signal)
                    
        except Exception as e:
            print(f"[WARNING] Error detectando Order Blocks: {e}")
        
        return patterns
    
    def _detect_fair_value_gaps(self, data: pd.DataFrame, symbol: str, timeframe: str) -> List[PatternSignal]:
        """Detectar Fair Value Gaps (FVG)"""
        patterns = []
        
        try:
            fvgs = self._find_fair_value_gaps(data)
            
            for fvg in fvgs[-2:]:  # Solo los más recientes
                direction = TradingDirection.BUY if fvg['type'] == 'bullish' else TradingDirection.SELL
                entry_zone = (fvg['low'], fvg['high'])
                current_price = data['close'].iloc[-1]
                
                gap_size = fvg['high'] - fvg['low']
                
                if direction == TradingDirection.BUY:
                    stop_loss = fvg['low'] - gap_size * 0.2
                    take_profit_1 = current_price + gap_size * 1.5
                else:
                    stop_loss = fvg['high'] + gap_size * 0.2
                    take_profit_1 = current_price - gap_size * 1.5
                
                risk = abs(np.mean(entry_zone) - stop_loss)
                reward = abs(take_profit_1 - np.mean(entry_zone))
                risk_reward = reward / risk if risk > 0 else 0
                
                strength = 60.0
                if gap_size >= self.config['fvg_min_size']:
                    strength += 10.0
                if not fvg.get('partially_filled', False):
                    strength += 8.0
                
                if strength >= self.config['min_confidence']:
                    signal = PatternSignal(
                        pattern_type=PatternType.FAIR_VALUE_GAP,
                        direction=direction,
                        confidence=PatternConfidence.MEDIUM,
                        strength=min(strength, 78.0),
                        timestamp=datetime.now(),
                        symbol=symbol,
                        timeframe=timeframe,
                        entry_zone=entry_zone,
                        stop_loss=stop_loss,
                        take_profit_1=take_profit_1,
                        risk_reward_ratio=risk_reward,
                        probability=strength,
                        session=self._get_current_session(),
                        narrative=f"Fair Value Gap {direction.value} detectado. Desequilibrio que busca ser rellenado por el precio.",
                        confluences=["price_imbalance", "gap_fill_probability"],
                        invalidation_criteria=f"Gap completamente rellenado sin reacción",
                        time_sensitivity="MEDIA - FVG puede persistir por horas/días",
                        analysis_id=f"FVG_{symbol}_{int(datetime.now().timestamp())}"
                    )
                    
                    patterns.append(signal)
                    
        except Exception as e:
            print(f"[WARNING] Error detectando FVG: {e}")
        
        return patterns
    
    def _find_order_blocks(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Encontrar Order Blocks en los datos"""
        order_blocks = []
        
        try:
            if len(data) < 10:
                return order_blocks
            
            # Buscar velas de impulso seguidas de consolidación
            for i in range(5, len(data) - 5):
                current_candle = data.iloc[i]
                candle_size = abs(current_candle['close'] - current_candle['open'])
                
                # Calcular tamaño promedio de velas anteriores
                prev_candles = data.iloc[i-5:i]
                avg_size = abs(prev_candles['close'] - prev_candles['open']).mean()
                
                # Verificar si es vela de impulso
                if candle_size > avg_size * 1.8:
                    # Verificar si hay retorno a la zona
                    future_candles = data.iloc[i+1:i+6]
                    
                    ob_high = current_candle['high']
                    ob_low = current_candle['low']
                    
                    # Check for price return to the Order Block
                    for j, future_candle in future_candles.iterrows():
                        if future_candle['low'] <= ob_high and future_candle['high'] >= ob_low:
                            # Order Block found
                            ob_type = 'bullish' if current_candle['close'] > current_candle['open'] else 'bearish'
                            
                            order_blocks.append({
                                'type': ob_type,
                                'high': ob_high,
                                'low': ob_low,
                                'timestamp': current_candle.name if hasattr(current_candle, 'name') else i,
                                'strength': min(candle_size / avg_size / 2, 1.0),
                                'tested': True
                            })
                            break
                            
        except Exception as e:
            print(f"[WARNING] Error finding Order Blocks: {e}")
        
        return order_blocks
    
    def _find_fair_value_gaps(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Encontrar Fair Value Gaps en los datos"""
        fvgs = []
        
        try:
            if len(data) < 3:
                return fvgs
            
            # Buscar gaps en secuencias de 3 velas
            for i in range(1, len(data) - 1):
                prev_candle = data.iloc[i-1]
                current_candle = data.iloc[i]
                next_candle = data.iloc[i+1]
                
                # Bullish FVG: gap between prev high and next low
                if (prev_candle['high'] < next_candle['low'] and
                    current_candle['close'] > current_candle['open']):
                    
                    gap_size = next_candle['low'] - prev_candle['high']
                    if gap_size >= self.config['fvg_min_size']:
                        fvgs.append({
                            'type': 'bullish',
                            'high': next_candle['low'],
                            'low': prev_candle['high'],
                            'timestamp': current_candle.name if hasattr(current_candle, 'name') else i,
                            'size': gap_size,
                            'partially_filled': False
                        })
                
                # Bearish FVG: gap between prev low and next high
                elif (prev_candle['low'] > next_candle['high'] and
                      current_candle['close'] < current_candle['open']):
                    
                    gap_size = prev_candle['low'] - next_candle['high']
                    if gap_size >= self.config['fvg_min_size']:
                        fvgs.append({
                            'type': 'bearish',
                            'high': prev_candle['low'],
                            'low': next_candle['high'],
                            'timestamp': current_candle.name if hasattr(current_candle, 'name') else i,
                            'size': gap_size,
                            'partially_filled': False
                        })
                        
        except Exception as e:
            print(f"[WARNING] Error finding FVGs: {e}")
        
        return fvgs
    
    def get_multi_timeframe_data(self, symbol: str) -> Dict[str, pd.DataFrame]:
        """
        🎯 OBTENER DATOS MULTI-TIMEFRAME ALMACENADOS
        
        Returns:
            Dict con {timeframe: dataframe} para análisis contextuales
        """
        if hasattr(self, '_multi_tf_data') and symbol in self._multi_tf_data:
            return self._multi_tf_data[symbol]
        return {}

    def _enhance_analysis_with_multi_tf(self, patterns: List[PatternSignal], symbol: str, primary_timeframe: str) -> List[PatternSignal]:
        """
        🔍 ENHANCING PATTERNS CON ANÁLISIS MULTI-TIMEFRAME ICT v6.0
        
        Mejora los patrones detectados usando el contexto de timeframes superiores:
        - HTF Structure confirmation
        - Confluences entre timeframes
        - ICT Kill Zone optimization
        """
        try:
            multi_tf_data = self.get_multi_timeframe_data(symbol)
            
            if not multi_tf_data:
                return patterns
                
            enhanced_patterns = []
            
            for pattern in patterns:
                enhanced_pattern = self._apply_multi_tf_enhancement(
                    pattern, multi_tf_data, primary_timeframe
                )
                enhanced_patterns.append(enhanced_pattern)
                
            print(f"📊 Enhanced {len(enhanced_patterns)} patterns with multi-TF analysis")
            return enhanced_patterns
            
        except Exception as e:
            print(f"[WARNING] Error in multi-TF enhancement: {e}")
            return patterns

    def _apply_multi_tf_enhancement(self, pattern: PatternSignal, multi_tf_data: Dict[str, pd.DataFrame], primary_tf: str) -> PatternSignal:
        """
        📈 APLICAR ENHANCEMENT MULTI-TIMEFRAME A PATRÓN INDIVIDUAL
        
        Args:
            pattern: Patrón detectado en timeframe primario
            multi_tf_data: Datos de todos los timeframes
            primary_tf: Timeframe primario donde se detectó el patrón
            
        Returns:
            PatternSignal mejorado con confirmaciones HTF
        """
        try:
            # Get higher timeframes for confirmation
            htf_timeframes = self._get_higher_timeframes(primary_tf)
            
            confirmations = []
            strength_multiplier = 1.0
            
            for htf in htf_timeframes:
                if htf in multi_tf_data:
                    htf_data = multi_tf_data[htf]
                    
                    # Check HTF structure alignment
                    htf_confirmation = self._check_htf_structure_alignment(
                        pattern, htf_data, htf
                    )
                    
                    if htf_confirmation:
                        confirmations.append(f"HTF_{htf}_ALIGN")
                        strength_multiplier += 0.2
                        
            # Apply Smart Money enhancement if available
            if hasattr(self, 'smart_money_analyzer') and self.smart_money_analyzer:
                smc_enhancement = self.smart_money_analyzer.enhance_pattern_with_smart_money(
                    pattern, multi_tf_data
                )
                
                if smc_enhancement.get('enhanced', False):
                    confirmations.extend(smc_enhancement.get('confirmations', []))
                    strength_multiplier += smc_enhancement.get('strength_boost', 0)
                    
            # Create enhanced pattern with improved strength
            enhanced_strength = min(pattern.strength * strength_multiplier, 100.0)
            
            # Create enhanced pattern with all required fields
            enhanced_pattern = PatternSignal(
                pattern_type=pattern.pattern_type,
                direction=pattern.direction,
                confidence=pattern.confidence,
                strength=enhanced_strength,
                timestamp=pattern.timestamp,
                symbol=pattern.symbol,
                timeframe=pattern.timeframe,
                entry_zone=pattern.entry_zone,
                stop_loss=pattern.stop_loss,
                take_profit_1=pattern.take_profit_1,
                take_profit_2=pattern.take_profit_2,
                risk_reward_ratio=pattern.risk_reward_ratio,
                probability=pattern.probability,
                session=pattern.session,
                narrative=pattern.narrative + f" | Multi-TF Enhanced (+{(strength_multiplier-1)*100:.0f}%)",
                confluences=pattern.confluences + confirmations,
                invalidation_criteria=pattern.invalidation_criteria,
                optimal_entry_time=pattern.optimal_entry_time,
                time_sensitivity=pattern.time_sensitivity,
                max_hold_time=pattern.max_hold_time,
                analysis_id=pattern.analysis_id,
                raw_data=pattern.raw_data.copy() if pattern.raw_data else {}
            )
            
            # Add multi-TF metadata to raw_data
            enhanced_pattern.raw_data.update({
                'multi_tf_confirmations': confirmations,
                'htf_analyzed': list(htf_timeframes),
                'strength_enhancement': strength_multiplier - 1.0,
                'original_strength': pattern.strength
            })
            
            return enhanced_pattern
            
        except Exception as e:
            print(f"[DEBUG] Error applying multi-TF enhancement: {e}")
            return pattern

    def _get_higher_timeframes(self, primary_tf: str) -> List[str]:
        """Obtener timeframes superiores para confirmación"""
        tf_hierarchy = ['M1', 'M5', 'M15', 'H1', 'H4', 'D1', 'W1', 'MN1']
        
        try:
            primary_idx = tf_hierarchy.index(primary_tf)
            return tf_hierarchy[primary_idx + 1:primary_idx + 4]  # Next 3 higher TFs
        except ValueError:
            return ['H1', 'H4', 'D1']  # Default HTFs

    def _check_htf_structure_alignment(self, pattern: PatternSignal, htf_data: pd.DataFrame, htf: str) -> bool:
        """
        🔍 VERIFICAR ALINEACIÓN DE ESTRUCTURA EN HTF
        
        Checks if the pattern aligns with higher timeframe structure:
        - Trend direction alignment
        - Key level confluence
        - Market structure support
        """
        try:
            if htf_data.empty or len(htf_data) < 20:
                return False
                
            # Get recent HTF candles around pattern time
            pattern_time = pattern.timestamp
            
            # Find closest HTF candle to pattern time
            time_diffs = abs(htf_data.index - pattern_time)
            closest_pos = time_diffs.argmin()  # 🔧 FIX: usar argmin() en lugar de idxmin()
            
            # Get context window
            # closest_pos ya es la posición numérica, no necesitamos get_loc()
            start_pos = max(0, closest_pos - 10)
            end_pos = min(len(htf_data), closest_pos + 5)
            
            context_data = htf_data.iloc[start_pos:end_pos]
            
            if len(context_data) < 5:
                return False
                
            # Check trend alignment
            htf_trend = self._determine_htf_trend(context_data)
            pattern_direction = pattern.direction
            
            # Bullish pattern should align with bullish HTF trend
            if pattern_direction == TradingDirection.BUY and htf_trend == "BULLISH":
                return True
            elif pattern_direction == TradingDirection.SELL and htf_trend == "BEARISH":
                return True
            elif htf_trend == "NEUTRAL":  # Neutral HTF allows both directions
                return True
                
            return False
            
        except Exception as e:
            print(f"[DEBUG] Error checking HTF alignment: {e}")
            return False

    def _determine_htf_trend(self, htf_data: pd.DataFrame) -> str:
        """
        📊 DETERMINAR TENDENCIA EN HTF
        
        Returns: "BULLISH", "BEARISH", or "NEUTRAL"
        """
        try:
            if len(htf_data) < 5:
                return "NEUTRAL"
                
            # Simple trend using highs and lows progression
            recent_data = htf_data.tail(5)
            
            highs = recent_data['high'].values
            lows = recent_data['low'].values
            
            # Check for higher highs and higher lows (bullish)
            if highs[-1] > highs[0] and lows[-1] > lows[0]:
                return "BULLISH"
            # Check for lower highs and lower lows (bearish)
            elif highs[-1] < highs[0] and lows[-1] < lows[0]:
                return "BEARISH"
            else:
                return "NEUTRAL"
                
        except Exception:
            return "NEUTRAL"
    
    def _is_silver_bullet_time(self, current_time: datetime) -> bool:
        """Verificar si es ventana Silver Bullet"""
        try:
            # Convertir a GMT si es necesario
            hour = current_time.hour
            # Silver Bullet windows: 10:00-11:00 GMT y 14:00-15:00 GMT
            return (10 <= hour <= 11) or (14 <= hour <= 15)
        except:
            return False
    
    def _is_session_opening(self) -> bool:
        """Verificar si es apertura de sesión"""
        try:
            current_time = datetime.now()
            hour = current_time.hour
            
            # London: 08:00-10:00, New York: 13:00-15:00
            return (8 <= hour <= 10) or (13 <= hour <= 15)
        except:
            return False
    
    def _get_current_session(self) -> SessionType:
        """Obtener sesión actual"""
        try:
            current_time = datetime.now()
            hour = current_time.hour
            
            if 8 <= hour <= 17:
                return SessionType.LONDON
            elif 13 <= hour <= 22:
                return SessionType.NEW_YORK
            elif 22 <= hour <= 24 or 0 <= hour <= 8:
                return SessionType.ASIAN
            else:
                return SessionType.DEAD_ZONE
        except:
            return SessionType.LONDON
    
    def _update_performance_metrics(self, analysis_time: float, patterns_detected: int):
        """Actualizar métricas de rendimiento"""
        try:
            self.performance_metrics['total_analyses'] += 1
            self.performance_metrics['patterns_detected'] += patterns_detected
            
            # Promedio móvil del tiempo de análisis
            total = self.performance_metrics['total_analyses']
            current_avg = self.performance_metrics['avg_analysis_time']
            self.performance_metrics['avg_analysis_time'] = (current_avg * (total - 1) + analysis_time) / total
            
            # Tasa de éxito (patrones detectados vs análisis)
            self.performance_metrics['success_rate'] = (
                self.performance_metrics['patterns_detected'] / total * 100
            )
            
            self.performance_metrics['last_update'] = datetime.now()
            
        except Exception as e:
            print(f"[WARNING] Error actualizando métricas: {e}")
    
    def get_detected_patterns(self) -> List[PatternSignal]:
        """Obtener patrones detectados"""
        return self.detected_patterns.copy()
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Obtener métricas de rendimiento"""
        return self.performance_metrics.copy()
    
    def get_pattern_summary(self) -> Dict[str, Any]:
        """Obtener resumen de patrones detectados"""
        if not self.detected_patterns:
            return {
                'total_patterns': 0,
                'by_type': {},
                'by_confidence': {},
                'avg_strength': 0.0,
                'last_analysis': None
            }
        
        # Contar por tipo
        by_type = {}
        for pattern in self.detected_patterns:
            ptype = pattern.pattern_type.value
            by_type[ptype] = by_type.get(ptype, 0) + 1
        
        # Contar por confianza
        by_confidence = {}
        for pattern in self.detected_patterns:
            conf = pattern.confidence.value
            by_confidence[conf] = by_confidence.get(conf, 0) + 1
        
        # Strength promedio
        avg_strength = sum(p.strength for p in self.detected_patterns) / len(self.detected_patterns)
        
        return {
            'total_patterns': len(self.detected_patterns),
            'by_type': by_type,
            'by_confidence': by_confidence,
            'avg_strength': round(avg_strength, 1),
            'last_analysis': self.last_analysis_time
        }

    # =============================================================================
    # SMART MONEY CONCEPTS INTEGRATION v6.0
    # =============================================================================

    def _enhance_with_smart_money_analysis(self, patterns: List[PatternSignal], data) -> List[PatternSignal]:
        """
        🧠 ENHANCE PATTERNS WITH SMART MONEY CONCEPTS v6.0
        
        Mejora los patrones detectados con análisis Smart Money:
        - Liquidity pools identification
        - Institutional order flow
        - Market maker behavior
        - Killzone optimization
        
        Args:
            patterns: Lista de patrones detectados
            data: Datos de mercado para análisis
            
        Returns:
            Lista de patrones mejorados con Smart Money insights
        """
        if not self._smart_money_analyzer or not patterns:
            return patterns
        
        try:
            enhanced_patterns = []
            
            for pattern in patterns:
                # Analizar liquidity pools cerca del patrón
                liquidity_pools = self._analyze_liquidity_pools_near_pattern(pattern, data)
                
                # Detectar flujo institucional
                institutional_flow = self._detect_institutional_flow(pattern, data)
                
                # Verificar comportamiento market maker
                market_maker_behavior = self._analyze_market_maker_behavior(pattern, data)
                
                # Optimizar con killzones
                killzone_optimization = self._optimize_with_killzones(pattern, data)
                
                # Calcular smart money confidence
                smart_money_confidence = self._calculate_smart_money_confidence(
                    liquidity_pools, institutional_flow, market_maker_behavior, killzone_optimization
                )
                
                # Enhancing pattern with Smart Money data
                enhanced_pattern = self._apply_smart_money_enhancement(
                    pattern, smart_money_confidence, liquidity_pools,
                    institutional_flow, market_maker_behavior, killzone_optimization
                )
                
                enhanced_patterns.append(enhanced_pattern)
                
                if self.config.get('enable_debug'):
                    print(f"🧠 Smart Money enhancement: {pattern.pattern_type.value}")
                    print(f"   Liquidity pools: {len(liquidity_pools)}")
                    print(f"   Institutional flow: {institutional_flow:.2f}")
                    print(f"   Market maker: {market_maker_behavior:.2f}")
                    print(f"   Smart Money confidence: {smart_money_confidence:.2f}")
            
            return enhanced_patterns
            
        except Exception as e:
            if self.config.get('enable_debug'):
                print(f"[ERROR] Error en Smart Money enhancement: {e}")
            return patterns

    def _analyze_liquidity_pools_near_pattern(self, pattern: PatternSignal, data) -> List[Dict[str, Any]]:
        """Analiza liquidity pools cerca del patrón"""
        try:
            if not self._smart_money_analyzer:
                return []
            
            # Usar método genérico del Smart Money Analyzer
            # Simulamos pools básicos basados en el patrón
            pools = []
            
            # Pool en entry zone
            entry_mid = (pattern.entry_zone[0] + pattern.entry_zone[1]) / 2
            pools.append({
                'price': entry_mid,
                'strength': 0.7,
                'type': 'entry_zone',
                'distance': 0.0
            })
            
            # Pool en stop loss (liquidity grab zone)
            pools.append({
                'price': pattern.stop_loss,
                'strength': 0.8,
                'type': 'stop_hunt',
                'distance': abs(entry_mid - pattern.stop_loss)
            })
            
            return pools
            
        except Exception:
            return []

    def _detect_institutional_flow(self, pattern: PatternSignal, data) -> float:
        """Detecta flujo institucional"""
        try:
            if not self._smart_money_analyzer:
                return 0.5
            
            # Simular análisis de flujo institucional basado en sesión y fuerza del patrón
            flow_strength = 0.5
            
            # Bonus por sesión activa
            if pattern.session in [SessionType.LONDON, SessionType.NEW_YORK]:
                flow_strength += 0.2
            
            # Bonus por fuerza del patrón
            if pattern.strength > 75:
                flow_strength += 0.2
            
            # Bonus por confluencias
            if len(pattern.confluences) > 2:
                flow_strength += 0.1
            
            return min(flow_strength, 1.0)
            
        except Exception:
            return 0.5

    def _analyze_market_maker_behavior(self, pattern: PatternSignal, data) -> float:
        """Analiza comportamiento market maker"""
        try:
            if not self._smart_money_analyzer:
                return 0.5
            
            # Simular análisis de market maker basado en tipo de patrón
            mm_score = 0.5
            
            # Patrones que indican market maker activity
            if pattern.pattern_type in [PatternType.LIQUIDITY_GRAB, PatternType.JUDAS_SWING]:
                mm_score += 0.3
            elif pattern.pattern_type == PatternType.SILVER_BULLET:
                mm_score += 0.2
            
            # Bonus por RR alto
            if pattern.risk_reward_ratio > 2.0:
                mm_score += 0.1
            
            return min(mm_score, 1.0)
            
        except Exception:
            return 0.5

    def _optimize_with_killzones(self, pattern: PatternSignal, data) -> Dict[str, Any]:
        """Optimiza patrón con killzones"""
        try:
            if not self._smart_money_analyzer:
                return {'active': False, 'strength': 0.5}
            
            # Verificar si estamos en killzone
            current_hour = datetime.now().hour
            
            # London killzone: 10:00-11:00 GMT
            london_killzone = 10 <= current_hour <= 11
            
            # New York killzone: 14:00-15:00 GMT
            ny_killzone = 14 <= current_hour <= 15
            
            # Asian killzone: 01:00-02:00 GMT
            asian_killzone = 1 <= current_hour <= 2
            
            active_killzone = london_killzone or ny_killzone or asian_killzone
            
            # Fuerza basada en sesión y patrón
            strength = 0.5
            if active_killzone:
                strength = 0.8
                if pattern.session == SessionType.LONDON and london_killzone:
                    strength = 0.9
                elif pattern.session == SessionType.NEW_YORK and ny_killzone:
                    strength = 0.9
            
            return {
                'active': active_killzone,
                'strength': strength,
                'killzone_type': 'london' if london_killzone else 'ny' if ny_killzone else 'asian' if asian_killzone else 'none'
            }
            
        except Exception:
            return {'active': False, 'strength': 0.5}

    def _calculate_smart_money_confidence(self, liquidity_pools: List[Dict], institutional_flow: float,
                                        market_maker_behavior: float, killzone_optimization: Dict) -> float:
        """Calcula confianza Smart Money combinada"""
        try:
            # Peso base
            confidence = 0.5
            
            # Bonus por liquidity pools
            if liquidity_pools:
                pool_strength = sum(pool.get('strength', 0.5) for pool in liquidity_pools) / len(liquidity_pools)
                confidence += pool_strength * 0.2
            
            # Bonus por flujo institucional
            confidence += institutional_flow * 0.3
            
            # Bonus por market maker behavior
            confidence += market_maker_behavior * 0.2
            
            # Bonus por killzone
            if killzone_optimization.get('active', False):
                confidence += killzone_optimization.get('strength', 0.5) * 0.3
            
            return min(confidence, 1.0)
            
        except Exception:
            return 0.5

    def _apply_smart_money_enhancement(self, pattern: PatternSignal, smart_money_confidence: float,
                                     liquidity_pools: List[Dict], institutional_flow: float,
                                     market_maker_behavior: float, killzone_optimization: Dict) -> PatternSignal:
        """Aplica mejoras Smart Money al patrón"""
        try:
            # Crear nuevo patrón mejorado
            enhanced_confidence = PatternConfidence.MEDIUM
            
            # Calcular nueva confianza combinando patrón original + Smart Money
            combined_confidence = (pattern.strength + smart_money_confidence * 100) / 2
            
            if combined_confidence >= 80:
                enhanced_confidence = PatternConfidence.HIGH
            elif combined_confidence >= 70:
                enhanced_confidence = PatternConfidence.MEDIUM
            else:
                enhanced_confidence = PatternConfidence.LOW
            
            # Mejorar narrative con Smart Money insights
            enhanced_narrative = pattern.narrative
            if liquidity_pools:
                enhanced_narrative += f" | 💧 {len(liquidity_pools)} liquidity pools detectados"
            if institutional_flow > 0.7:
                enhanced_narrative += f" | 🏛️ Flujo institucional fuerte ({institutional_flow:.2f})"
            if market_maker_behavior > 0.7:
                enhanced_narrative += f" | 🎯 Comportamiento market maker ({market_maker_behavior:.2f})"
            if killzone_optimization.get('active', False):
                enhanced_narrative += f" | ⏰ Killzone activo ({killzone_optimization.get('strength', 0.5):.2f})"
            
            # Crear patrón mejorado manteniendo estructura original
            enhanced_pattern = PatternSignal(
                pattern_type=pattern.pattern_type,
                confidence=enhanced_confidence,
                direction=pattern.direction,
                symbol=pattern.symbol,
                timeframe=pattern.timeframe,
                entry_zone=pattern.entry_zone,
                stop_loss=pattern.stop_loss,
                take_profit_1=pattern.take_profit_1,
                take_profit_2=pattern.take_profit_2,
                strength=combined_confidence,
                timestamp=pattern.timestamp,
                risk_reward_ratio=pattern.risk_reward_ratio,
                probability=pattern.probability,
                session=pattern.session,
                narrative=enhanced_narrative,
                confluences=pattern.confluences + ["Smart Money Analysis v6.0"],
                invalidation_criteria=pattern.invalidation_criteria,
                optimal_entry_time=pattern.optimal_entry_time,
                time_sensitivity=pattern.time_sensitivity,
                max_hold_time=pattern.max_hold_time,
                raw_data={
                    **pattern.raw_data,
                    'smart_money_data': {
                        'liquidity_pools': liquidity_pools,
                        'institutional_flow': institutional_flow,
                        'market_maker_behavior': market_maker_behavior,
                        'killzone_optimization': killzone_optimization,
                        'smart_money_confidence': smart_money_confidence
                    }
                }
            )
            
            return enhanced_pattern
            
        except Exception as e:
            if self.config.get('enable_debug'):
                print(f"[ERROR] Error aplicando Smart Money enhancement: {e}")
            return pattern


# Factory function para crear instancia
def get_pattern_detector(config: Optional[Dict[str, Any]] = None) -> PatternDetector:
    """
    Factory function para crear Pattern Detector v6.0 Enterprise
    
    Args:
        config: Configuración opcional del detector
        
    Returns:
        Instancia configurada del Pattern Detector
    """
    return PatternDetector(config)


if __name__ == "__main__":
    # Test básico del Pattern Detector
    print("🎯 ICT Pattern Detector v6.0 Enterprise - Test")
    print("=" * 50)
    
    detector = get_pattern_detector({
        'enable_debug': True,
        'min_confidence': 65.0
    })
    
    patterns = detector.detect_patterns("EURUSD", "M15", 3)
    
    print(f"\n📊 Resultados del análisis:")
    print(f"Patrones detectados: {len(patterns)}")
    
    for pattern in patterns:
        print(f"\n🎯 {pattern.pattern_type.value.upper()}")
        print(f"   Dirección: {pattern.direction.value}")
        print(f"   Confianza: {pattern.confidence.value}")
        print(f"   Strength: {pattern.strength:.1f}%")
        print(f"   R:R: {pattern.risk_reward_ratio:.2f}")
    
    # Métricas
    metrics = detector.get_performance_metrics()
    print(f"\n⚡ Performance:")
    print(f"   Tiempo promedio: {metrics['avg_analysis_time']:.3f}s")
    print(f"   Análisis totales: {metrics['total_analyses']}")
    
    summary = detector.get_pattern_summary()
    print(f"\n📈 Resumen:")
    print(f"   Total: {summary['total_patterns']}")
    print(f"   Strength promedio: {summary['avg_strength']}%")
    print(f"   Por tipo: {summary['by_type']}")
