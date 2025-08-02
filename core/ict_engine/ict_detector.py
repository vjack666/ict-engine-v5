#!/usr/bin/env python3
"""
📊 ICT DETECTOR - Sistema Consolidado de Análisis ICT
====================================================

Módulo consolidado para análisis Inner Circle Trader (ICT) multi-timeframe.
Incluye análisis de bias, estructura, contexto de mercado y patrones ICT.

Consolidado desde:
- MarketContext class de analisis_ict.py
- Funciones ICT no-fractal de analisis_ict.py
- OptimizedICTAnalysis de ict_analysis_optimized.py
- Funciones de bias, estructura y POI

Versión: v3.3.3
"""

import pandas as pd
import numpy as np
# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
import json
from json import JSONDecodeError
from pathlib import Path

# --- Sistema de logging centralizado ---
from sistema.logging_config import get_specialized_logger
logger = get_specialized_logger('ict')

# =============================================================================
# CONFIGURACIÓN Y CONSTANTES
# =============================================================================

ICT_CONFIG = {
    'h4_bias_lookback': 20,
    'm15_structure_lookback': 50,
    'ltf_confirmation_lookback': 20,
    'bias_threshold_pct': 0.1,
    'structure_strength_threshold': 0.4,
    'premium_discount_tolerance': 0.5,
    'swing_detection_left': 5,
    'swing_detection_right': 1,
    'ob_lookback_candles': 20,
    'fvg_gap_threshold': 0.0001
}

BIAS_TYPES = {
    'BULLISH': 'Sesgo Alcista H4',
    'BEARISH': 'Sesgo Bajista H4',
    'NEUTRAL': 'Sesgo Neutral H4',
    'NO_DATA': 'Sin Datos Suficientes',
    'ERROR': 'Error en Análisis'
}

STRUCTURE_TYPES = {
    'bullish_structure': 'Estructura Alcista',
    'bearish_structure': 'Estructura Bajista',
    'consolidation': 'Consolidación',
    'insufficient_data': 'Datos Insuficientes',
    'error': 'Error en Detección'
}

# =============================================================================
# CLASE PRINCIPAL - MARKET CONTEXT
# =============================================================================

class MarketContext:
    """
    Contiene el estado persistente del mercado (la "memoria" del bot).
    Este objeto se crea una sola vez y se va actualizando con cada vela.
    
    Consolidado y mejorado desde analisis_ict.py
    """
    
    def __init__(self):
        """Inicializa el contexto del mercado con valores por defecto."""
        enviar_senal_log("INFO", "🧠 Inicializando Market Context - Motor ICT", __name__, "general")
        enviar_senal_log("DEBUG", "Configurando bias, rangos y estructuras por defecto", __name__, "general")
        
        # Precio actual del mercado
        self.current_price = 0.0
        
        # Precio actual del mercado
        self.current_price = 0.0
        
        # Bias de timeframes
        self.h4_bias = "NEUTRAL"
        self.m15_bias = "NEUTRAL"
        
        # Rangos y niveles
        self.daily_range = {'high': 0, 'low': 0, 'mid': 0}
        self.current_session = "UNKNOWN"
        
        # Análisis fractal dinámico (ya consolidado en fractal module)
        self.fractal_range = {'high': 0, 'low': 0, 'eq': 0, 'status': 'NO_CALCULADO'}
        
        # POIs por timeframe
        self.pois_h4 = []
        self.pois_m15 = []
        self.pois_m5 = []
        
        # Información de BOS y swing points
        self.latest_bos_info = None
        self.last_swing_high = None
        self.last_swing_low = None
        
        # Niveles adaptativos (si están disponibles)
        self.adaptive_levels = None
        
        # Métricas adicionales
        self.last_update = datetime.now()
        self.analysis_quality = "MEDIUM"
        self.market_phase = "RANGING"  # RANGING, TRENDING, BREAKOUT
        
        enviar_senal_log("INFO", "✅ Market Context inicializado correctamente", __name__, "general")
        enviar_senal_log("DEBUG", f"Configuración inicial: H4_bias={self.h4_bias}, Sesión={self.current_session}, Fase={self.market_phase}", __name__, "general")
        
        # Cache para optimización
        self._cache = {}
        self._cache_timestamps = {}
    
    def __repr__(self):
        """Representación legible del contexto."""
        return (
            f"MarketContext("
            f"h4_bias={self.h4_bias}, "
            f"fractal_status={self.fractal_range.get('status', 'N/A')}, "
            f"daily_range={self.daily_range['high']:.5f}-{self.daily_range['low']:.5f}, "
            f"pois_count={len(self.pois_h4) + len(self.pois_m15) + len(self.pois_m5)}"
            f")"
        )
    
    def update_bias(self, df_h4):
        """Actualiza el bias H4 (wrapper para compatibilidad)."""
        self.h4_bias = _calculate_h4_bias(df_h4)
    
    def find_new_pois(self, df, timeframe):
        """Encuentra nuevos POIs (wrapper para compatibilidad)."""
        return _find_new_pois(self, df, timeframe)
    
    def update_existing_pois(self, current_price, high, low, timeframe):
        """Actualiza POIs existentes (wrapper para compatibilidad)."""
        # Crear un candle simulado con los datos proporcionados
        import pandas as pd
        last_candle = pd.Series({
            'close': current_price,
            'high': high,
            'low': low,
            'open': current_price,  # Aproximación
            'time': pd.Timestamp.now()
        })
        _update_existing_pois(self, last_candle, timeframe)
    
    def get_cache_key(self, key: str, timeframe: str = "default") -> str:
        """Genera clave de caché única."""
        return f"{timeframe}_{key}"
    
    def is_cache_valid(self, cache_key: str, max_age_minutes: int = 5) -> bool:
        """Verifica si un valor en caché sigue siendo válido."""
        if cache_key not in self._cache_timestamps:
            return False
        
        cache_time = self._cache_timestamps[cache_key]
        age = datetime.now() - cache_time
        return age.total_seconds() < (max_age_minutes * 60)
    
    def set_cache(self, cache_key: str, value: Any):
        """Establece un valor en caché."""
        self._cache[cache_key] = value
        self._cache_timestamps[cache_key] = datetime.now()
    
    def get_cache(self, cache_key: str) -> Optional[Any]:
        """Obtiene un valor del caché si es válido."""
        if self.is_cache_valid(cache_key):
            return self._cache.get(cache_key)
        return None

# =============================================================================
# CLASE OPTIMIZADA ICT ANALYSIS
# =============================================================================

class OptimizedICTAnalysis:
    """
    Análisis ICT optimizado con cache y lógica funcional.
    Consolidado desde ict_analysis_optimized.py
    """
    
    def __init__(self):
        self.cache_enabled = True
        
    def calcular_bias_h4_optimizado(self, df_h4: pd.DataFrame) -> str:
        """
        Cálculo optimizado de bias H4 con lógica real.
        """
        if df_h4 is None or len(df_h4) < ICT_CONFIG['h4_bias_lookback']:
            return "NO_DATA"
        
        try:
            # Lógica mejorada de bias H4
            recent_bars = df_h4.tail(ICT_CONFIG['h4_bias_lookback'])
            
            if len(recent_bars) >= 10:
                first_half_avg = recent_bars.head(10)['close'].mean()
                second_half_avg = recent_bars.tail(10)['close'].mean()
                
                price_change_pct = ((second_half_avg - first_half_avg) / first_half_avg) * 100
                
                if price_change_pct > ICT_CONFIG['bias_threshold_pct']:
                    return "BULLISH"
                elif price_change_pct < -ICT_CONFIG['bias_threshold_pct']:
                    return "BEARISH"
                else:
                    return "NEUTRAL"
            
            return "NEUTRAL"
            
        except (JSONDecodeError, ValueError) as e:
            enviar_senal_log("ERROR", f"Error calculando bias H4: {e}", __name__, "ict")
            return "ERROR"
        
    def detectar_estructura_m15_optimizada(self, df_m15: pd.DataFrame) -> Dict[str, Any]:
        """
        Detección optimizada de estructura M15 con lógica real.
        """
        if df_m15 is None or len(df_m15) < ICT_CONFIG['m15_structure_lookback']:
            return {"type": "insufficient_data", "strength": 0, "bos_detected": False}
        
        try:
            # Lógica funcional para detectar estructura M15
            recent_data = df_m15.tail(ICT_CONFIG['m15_structure_lookback'])
            
            # Detectar Break of Structure (BOS) simple
            highs = recent_data['high']
            lows = recent_data['low']
            
            # Calcular niveles clave
            resistance_level = highs.rolling(window=10).max().iloc[-1]
            support_level = lows.rolling(window=10).min().iloc[-1]
            current_price = recent_data['close'].iloc[-1]
            
            # Determinar estructura
            if current_price > resistance_level * 0.999:  # Near resistance break
                structure_type = "bullish_structure"
                strength = 0.8
                bos_detected = True
            elif current_price < support_level * 1.001:  # Near support break
                structure_type = "bearish_structure"
                strength = 0.8
                bos_detected = True
            else:
                structure_type = "consolidation"
                strength = 0.4
                bos_detected = False
            
            return {
                "type": structure_type,
                "strength": strength,
                "bos_detected": bos_detected,
                "resistance": resistance_level,
                "support": support_level,
                "status": "ANALYZED"
            }
            
        except (JSONDecodeError, ValueError) as e:
            enviar_senal_log("ERROR", f"Error detectando estructura M15: {e}", __name__, "ict")
            return {"type": "error", "strength": 0, "bos_detected": False, "error": str(e)}
    
    def analizar_confirmacion_ltf(self, df_m5: pd.DataFrame, m15_structure: Dict) -> Dict[str, Any]:
        """
        Análisis de confirmación en Lower Time Frame (M5).
        """
        if df_m5 is None or len(df_m5) < ICT_CONFIG['ltf_confirmation_lookback']:
            return {"confirmation": False, "strength": 0}
        
        try:
            # Lógica simple de confirmación LTF
            recent_m5 = df_m5.tail(ICT_CONFIG['ltf_confirmation_lookback'])
            
            # Si M15 sugiere estructura bullish, buscar confirmación en M5
            if m15_structure.get("type") == "bullish_structure":
                # Buscar impulsos alcistas en M5
                price_momentum = (recent_m5['close'].iloc[-1] - recent_m5['close'].iloc[-10]) / recent_m5['close'].iloc[-10]
                if price_momentum > 0.001:  # 0.1% momentum
                    return {"confirmation": True, "strength": 0.7, "direction": "bullish"}
            
            elif m15_structure.get("type") == "bearish_structure":
                # Buscar impulsos bajistas en M5
                price_momentum = (recent_m5['close'].iloc[-1] - recent_m5['close'].iloc[-10]) / recent_m5['close'].iloc[-10]
                if price_momentum < -0.001:  # -0.1% momentum
                    return {"confirmation": True, "strength": 0.7, "direction": "bearish"}
            
            return {"confirmation": False, "strength": 0.3, "direction": "neutral"}
            
        except (JSONDecodeError, ValueError) as e:
            enviar_senal_log("ERROR", f"Error en confirmación LTF: {e}", __name__, "ict")
            return {"confirmation": False, "strength": 0, "error": str(e)}
    
    def analisis_completo_ict(self, df_h4: pd.DataFrame, df_m15: pd.DataFrame, df_m5: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """
        Análisis ICT completo H4 → M15 → M5.
        """
        try:
            # Paso 1: H4 Bias
            h4_bias = self.calcular_bias_h4_optimizado(df_h4)
            
            # Paso 2: M15 Structure
            m15_structure = self.detectar_estructura_m15_optimizada(df_m15)
            
            # Paso 3: M5 Confirmation (opcional)
            ltf_confirmation = {}
            if df_m5 is not None:
                ltf_confirmation = self.analizar_confirmacion_ltf(df_m5, m15_structure)
            
            # Resultado integrado
            return {
                "h4_bias": h4_bias,
                "m15_structure": m15_structure,
                "ltf_confirmation": ltf_confirmation,
                "pipeline_status": "COMPLETED",
                "overall_direction": self._determine_overall_direction(h4_bias, m15_structure, ltf_confirmation)
            }
            
        except (JSONDecodeError, ValueError) as e:
            return {
                "pipeline_status": "ERROR",
                "error": str(e),
                "h4_bias": "ERROR",
                "m15_structure": {"type": "error", "strength": 0},
                "ltf_confirmation": {"confirmation": False, "strength": 0}
            }
    
    def _determine_overall_direction(self, h4_bias: str, m15_structure: Dict, ltf_confirmation: Dict) -> str:
        """Determina dirección general basada en análisis multi-timeframe."""
        try:
            bullish_signals = 0
            bearish_signals = 0
            
            # H4 bias
            if h4_bias == "BULLISH":
                bullish_signals += 1
            elif h4_bias == "BEARISH":
                bearish_signals += 1
            
            # M15 structure
            if m15_structure.get("type") == "bullish_structure":
                bullish_signals += 1
            elif m15_structure.get("type") == "bearish_structure":
                bearish_signals += 1
            
            # LTF confirmation
            if ltf_confirmation.get("direction") == "bullish":
                bullish_signals += 1
            elif ltf_confirmation.get("direction") == "bearish":
                bearish_signals += 1
            
            if bullish_signals > bearish_signals:
                return "BULLISH"
            elif bearish_signals > bullish_signals:
                return "BEARISH"
            else:
                return "NEUTRAL"
                
        except (JSONDecodeError, ValueError):
            return "NEUTRAL"

# =============================================================================
# FUNCIONES PRINCIPALES DE ANÁLISIS ICT
# =============================================================================

def update_market_context(contexto: MarketContext, df_by_timeframe: dict, current_price: float):
    """
    Actualiza el contexto del mercado con nueva información.
    Función principal consolidada desde analisis_ict.py
    
    Args:
        contexto: Objeto MarketContext a actualizar
        df_by_timeframe: Diccionario con DataFrames por timeframe
        current_price: Precio actual del mercado
    """
    enviar_senal_log("INFO", f"📊 Actualizando contexto de mercado - Precio actual: {current_price:.5f}", __name__, "general")
    
    # Log de datos disponibles
    timeframes_disponibles = [tf for tf, df in df_by_timeframe.items() if df is not None and len(df) > 0]
    enviar_senal_log("DEBUG", f"Timeframes disponibles para análisis: {timeframes_disponibles}", __name__, "general")
    
    for tf, df in df_by_timeframe.items():
        if df is not None and len(df) > 0:
            enviar_senal_log("DEBUG", f"  {tf}: {len(df)} velas (desde {df.index[0]} hasta {df.index[-1]})", __name__, "ict")
    
    try:
        
        
        # Actualizar timestamp
        contexto.last_update = datetime.now()
        enviar_senal_log("DEBUG", f"Timestamp actualizado: {contexto.last_update}", __name__, "general")
        
        # Actualizar bias H4
        if 'H4' in df_by_timeframe:
            enviar_senal_log("DEBUG", "🔍 Iniciando análisis de bias H4...", __name__, "general")
            previous_h4_bias = contexto.h4_bias
            _update_bias_h4(contexto, df_by_timeframe['H4'])
            if contexto.h4_bias != previous_h4_bias:
                enviar_senal_log("INFO", f"🔄 CAMBIO DE BIAS H4: {previous_h4_bias} → {contexto.h4_bias}", __name__, "general")
            else:
                enviar_senal_log("DEBUG", f"Bias H4 mantenido: {contexto.h4_bias}", __name__, "general")
        
        # Actualizar bias M15
        if 'M15' in df_by_timeframe:
            enviar_senal_log("DEBUG", "🔍 Iniciando análisis de bias M15...", __name__, "general")
            previous_m15_bias = contexto.m15_bias
            _update_bias_m15(contexto, df_by_timeframe['M15'])
            if contexto.m15_bias != previous_m15_bias:
                enviar_senal_log("INFO", f"🔄 CAMBIO DE BIAS M15: {previous_m15_bias} → {contexto.m15_bias}", __name__, "general")
            else:
                enviar_senal_log("DEBUG", f"Bias M15 mantenido: {contexto.m15_bias}", __name__, "general")
        
        # Actualizar rango diario
        if 'D1' in df_by_timeframe:
            enviar_senal_log("DEBUG", "📏 Analizando rango diario...", __name__, "general")
            _update_daily_range(contexto, df_by_timeframe['D1'], current_price)
            enviar_senal_log("DEBUG", f"Rango diario: H={contexto.daily_range['high']:.5f}, L={contexto.daily_range['low']:.5f}, Mid={contexto.daily_range['mid']:.5f}", __name__, "general")
        
        # Buscar nuevos POIs en todos los timeframes
        enviar_senal_log("DEBUG", "🎯 Iniciando búsqueda de POIs multi-timeframe...", __name__, "general")
        for timeframe, df in df_by_timeframe.items():
            if timeframe in ['H4', 'M15', 'M5'] and df is not None and len(df) > 0:
                enviar_senal_log("DEBUG", f"Buscando POIs en {timeframe}...", __name__, "general")
                pois_antes = len(getattr(contexto, f'pois_{timeframe.lower()}', []))
                _find_new_pois(contexto, df, timeframe)
                pois_despues = len(getattr(contexto, f'pois_{timeframe.lower()}', []))
                
                if pois_despues > pois_antes:
                    nuevos_pois = pois_despues - pois_antes
                    enviar_senal_log("INFO", f"✨ {nuevos_pois} nuevo(s) POI(s) detectado(s) en {timeframe}", __name__, "general")
                
                # Actualizar POIs existentes con la última vela
                if len(df) > 0:
                    last_candle = df.iloc[-1]
                    _update_existing_pois(contexto, last_candle, timeframe)
        
        # Actualizar calidad del análisis
        enviar_senal_log("DEBUG", "📈 Evaluando calidad del análisis...", __name__, "general")
        _evaluate_analysis_quality(contexto)
        enviar_senal_log("DEBUG", f"Calidad del análisis: {contexto.analysis_quality}", __name__, "general")
        
        # Log del contexto actualizado
        context_summary = {
            "h4_bias": contexto.h4_bias,
            "m15_bias": contexto.m15_bias,
            "fractal_status": contexto.fractal_range.get('status', 'N/A'),
            "total_pois": len(contexto.pois_h4) + len(contexto.pois_m15) + len(contexto.pois_m5),
            "analysis_quality": contexto.analysis_quality,
            "market_phase": contexto.market_phase
        }
        
        enviar_senal_log("INFO", f"✅ Contexto de mercado actualizado completamente", __name__, "general")
        enviar_senal_log("INFO", f"📋 RESUMEN: H4_bias={contexto.h4_bias}, M15_bias={contexto.m15_bias}, POIs_total={context_summary['total_pois']}, Calidad={contexto.analysis_quality}", __name__, "general")
        
        # Log context summary como DEBUG con metadata
        enviar_senal_log("DEBUG", f"Context actualizado: {context_summary}", __name__, "ict")
        
    except (JSONDecodeError, ValueError) as e:
        enviar_senal_log("ERROR", f"❌ Error crítico actualizando contexto de mercado: {e}", __name__, "general")

def _calculate_h4_bias(df_h4: pd.DataFrame) -> str:
    """Calcula el bias H4 usando lógica consolidada."""
    optimizer = OptimizedICTAnalysis()
    return optimizer.calcular_bias_h4_optimizado(df_h4)

def _update_bias_h4(contexto: MarketContext, df_h4: pd.DataFrame, debug_mode: bool = False):
    """
    Actualiza el bias H4 en el contexto.
    Función consolidada desde analisis_ict.py
    """
    try:
        enviar_senal_log("DEBUG", "🔍 Analizando bias H4...", __name__, "general")
        enviar_senal_log("DEBUG", f"Datos H4 disponibles: {len(df_h4)} velas", __name__, "ict")
        
        previous_bias = contexto.h4_bias
        new_bias = _calculate_h4_bias(df_h4)
        
        enviar_senal_log("DEBUG", f"Cálculo bias H4: {previous_bias} → {new_bias}", __name__, "general")
        
        if new_bias != previous_bias:
            contexto.h4_bias = new_bias
            
            # Log del cambio de bias
            enviar_senal_log("INFO", f"🔄 CAMBIO DE BIAS H4: {previous_bias} → {new_bias}", __name__, "ict")
            
            if debug_mode:
                # Análisis detallado para debug
                recent_bars = df_h4.tail(ICT_CONFIG['h4_bias_lookback'])
                if len(recent_bars) >= 10:
                    first_half_avg = recent_bars.head(10)['close'].mean()
                    second_half_avg = recent_bars.tail(10)['close'].mean()
                    price_change_pct = ((second_half_avg - first_half_avg) / first_half_avg) * 100
                    
                    bias_analysis_data = {
                        "previous_bias": previous_bias,
                        "new_bias": new_bias,
                        "price_change_pct": price_change_pct,
                        "first_half_avg": first_half_avg,
                        "second_half_avg": second_half_avg,
                        "bars_analyzed": len(recent_bars),
                        "threshold": ICT_CONFIG['bias_threshold_pct']
                    }
                    
                    # Log debug data con enviar_senal_log 
                    enviar_senal_log("DEBUG", f"H4 Bias Debug - Cambio: {price_change_pct:.3f}%, Umbral: {ICT_CONFIG['bias_threshold_pct']}%", __name__, "ict")
        
    except (JSONDecodeError, ValueError) as e:
        enviar_senal_log("ERROR", f"Error actualizando bias H4: {e}", __name__, "ict")

def _update_bias_m15(contexto: MarketContext, df_m15: pd.DataFrame):
    """
    Actualiza el bias M15 en el contexto.
    Función consolidada desde analisis_ict.py
    """
    try:
        # Lógica simplificada para M15 bias
        if df_m15 is None or len(df_m15) < 20:
            contexto.m15_bias = "NO_DATA"
            return
        
        recent_data = df_m15.tail(20)
        
        # Analizar estructura reciente
        highs = recent_data['high']
        lows = recent_data['low']
        closes = recent_data['close']
        
        # Tendencia de cierres
        if len(closes) >= 10:
            recent_trend = (closes.iloc[-5:].mean() - closes.iloc[-10:-5].mean()) / closes.iloc[-10:-5].mean()
            
            if recent_trend > 0.001:  # 0.1% threshold
                new_bias = "BULLISH"
            elif recent_trend < -0.001:
                new_bias = "BEARISH"
            else:
                new_bias = "NEUTRAL"
            
            if new_bias != contexto.m15_bias:
                previous_bias = contexto.m15_bias
                contexto.m15_bias = new_bias
                
                enviar_senal_log("INFO", f"🔄 CAMBIO DE BIAS M15: {previous_bias} → {new_bias}", __name__, "ict")
        
    except (JSONDecodeError, ValueError) as e:
        enviar_senal_log("ERROR", f"Error actualizando bias M15: {e}", __name__, "ict")

def _update_daily_range(contexto: MarketContext, df_d1: pd.DataFrame, current_price: float):
    """
    Actualiza el rango diario en el contexto.
    Función consolidada desde analisis_ict.py
    """
    try:
        if df_d1 is None or len(df_d1) == 0:
            return
        
        # Usar la última vela diaria
        last_daily = df_d1.iloc[-1]
        
        contexto.daily_range = {
            'high': last_daily['high'],
            'low': last_daily['low'],
            'mid': (last_daily['high'] + last_daily['low']) / 2,
            'open': last_daily['open'],
            'close': last_daily['close']
        }
        
    except (JSONDecodeError, ValueError) as e:
        enviar_senal_log("ERROR", f"Error actualizando el rango diario: {e}", __name__, "ict")

def _find_new_pois(contexto: MarketContext, df: pd.DataFrame, timeframe: str):
    """
    Busca nuevos POIs en el timeframe especificado.
    Función consolidada desde analisis_ict.py
    """
    try:
        if df is None or len(df) < 10:
            return
        
        # Lógica simplificada de detección de POIs
        new_pois = []
        
        # Detectar Order Blocks simples
        recent_data = df.tail(20)
        for i in range(1, len(recent_data) - 1):
            current = recent_data.iloc[i]
            prev_candle = recent_data.iloc[i-1]
            next_candle = recent_data.iloc[i+1]
            
            # OB Alcista: vela bajista seguida de vela alcista fuerte
            if (prev_candle['close'] < prev_candle['open'] and  # Vela bajista
                current['close'] > current['open'] and           # Vela alcista actual
                current['close'] > prev_candle['high']):         # Rompe máximo anterior
                
                poi = {
                    'type': 'BULLISH_OB',
                    'price': prev_candle['low'],
                    'high': prev_candle['high'],
                    'low': prev_candle['low'],
                    'timeframe': timeframe,
                    'timestamp': current.name,
                    'mitigated': False,
                    'broken': False,
                    'confidence': 0.7
                }
                new_pois.append(poi)
            
            # OB Bajista: vela alcista seguida de vela bajista fuerte  
            elif (prev_candle['close'] > prev_candle['open'] and  # Vela alcista
                  current['close'] < current['open'] and           # Vela bajista actual
                  current['close'] < prev_candle['low']):          # Rompe mínimo anterior
                
                poi = {
                    'type': 'BEARISH_OB',
                    'price': prev_candle['high'],
                    'high': prev_candle['high'],
                    'low': prev_candle['low'],
                    'timeframe': timeframe,
                    'timestamp': current.name,
                    'mitigated': False,
                    'broken': False,
                    'confidence': 0.7
                }
                new_pois.append(poi)
        
        # Agregar nuevos POIs al contexto según timeframe
        if timeframe == 'H4':
            contexto.pois_h4.extend(new_pois)
        elif timeframe == 'M15':
            contexto.pois_m15.extend(new_pois)
        elif timeframe == 'M5':
            contexto.pois_m5.extend(new_pois)
        
        if new_pois:
            poi_types = [poi['type'] for poi in new_pois]
            enviar_senal_log("INFO", f"✨ {len(new_pois)} nuevo(s) POI(s) detectado(s) en {timeframe}: {poi_types}", __name__, "ict")
        
    except (JSONDecodeError, ValueError) as e:
        enviar_senal_log("ERROR", f"Error buscando nuevos POIs en {timeframe}: {e}", __name__, "ict")

def _update_existing_pois(contexto: MarketContext, last_candle: pd.Series, timeframe: str):
    """
    Actualiza el estado de POIs existentes.
    Función consolidada desde analisis_ict.py
    """
    try:
        # Obtener lista de POIs según timeframe
        if timeframe == 'H4':
            pois_list = contexto.pois_h4
        elif timeframe == 'M15':
            pois_list = contexto.pois_m15
        elif timeframe == 'M5':
            pois_list = contexto.pois_m5
        else:
            return
        
        updated_count = 0
        
        for poi in pois_list:
            if poi.get('mitigated', False) or poi.get('broken', False):
                continue  # Skip already processed POIs
            
            # Verificar mitigación
            if poi['type'] == 'BULLISH_OB':
                # OB alcista se mitiga si el precio regresa a la zona
                if last_candle['low'] <= poi['price']:
                    poi['mitigated'] = True
                    poi['mitigation_time'] = last_candle.name
                    updated_count += 1
            
            elif poi['type'] == 'BEARISH_OB':
                # OB bajista se mitiga si el precio regresa a la zona
                if last_candle['high'] >= poi['price']:
                    poi['mitigated'] = True
                    poi['mitigation_time'] = last_candle.name
                    updated_count += 1
        
        if updated_count > 0:
            enviar_senal_log("INFO", f"🔄 {updated_count} POI(s) actualizados en {timeframe}", __name__, "ict")
        
    except (JSONDecodeError, ValueError) as e:
        enviar_senal_log("ERROR", f"Error actualizando POIs existentes en {timeframe}: {e}", __name__, "ict")

def _evaluate_analysis_quality(contexto: MarketContext):
    """Evalúa la calidad del análisis basado en datos disponibles."""
    try:
        quality_score = 0
        
        # Factor 1: Bias disponible
        if contexto.h4_bias not in ["NO_DATA", "ERROR"]:
            quality_score += 1
        if contexto.m15_bias not in ["NO_DATA", "ERROR"]:
            quality_score += 1
        
        # Factor 2: Análisis fractal válido
        if contexto.fractal_range.get('valid', False):
            quality_score += 2
        
        # Factor 3: POIs disponibles
        total_pois = len(contexto.pois_h4) + len(contexto.pois_m15) + len(contexto.pois_m5)
        if total_pois >= 5:
            quality_score += 2
        elif total_pois >= 2:
            quality_score += 1
        
        # Factor 4: Información BOS
        if contexto.latest_bos_info:
            quality_score += 1
        
        # Determinar calidad final
        if quality_score >= 6:
            contexto.analysis_quality = "HIGH"
        elif quality_score >= 3:
            contexto.analysis_quality = "MEDIUM"
        else:
            contexto.analysis_quality = "LOW"
        
        # Determinar fase del mercado
        if contexto.latest_bos_info and contexto.latest_bos_info.get('bos_found', False):
            bos_strength = contexto.latest_bos_info.get('bos_strength', 0)
            if bos_strength > 50:
                contexto.market_phase = "TRENDING"
            else:
                contexto.market_phase = "BREAKOUT"
        else:
            contexto.market_phase = "RANGING"
            
    except (JSONDecodeError, ValueError) as e:
        contexto.analysis_quality = "LOW"
        contexto.market_phase = "RANGING"

# =============================================================================
# FUNCIONES ADICIONALES ICT
# =============================================================================

def evaluar_checklist_de_entrada(mercado, pd_data, estocastico, en_horario, precio_actual) -> dict:
    """
    Evalúa el checklist de entrada ICT.
    Función consolidada desde analisis_ict.py
    """
    try:
        resultado = {
            "puntuacion_total": 0,
            "criterios_cumplidos": [],
            "recomendacion": "NO_ENTRY",
            "confianza": 0.0
        }
        
        # Criterio 1: Bias H4 definido
        if hasattr(mercado, 'h4_bias') and mercado.h4_bias in ['BULLISH', 'BEARISH']:
            resultado["puntuacion_total"] += 2
            resultado["criterios_cumplidos"].append(f"H4 Bias: {mercado.h4_bias}")
        
        # Criterio 2: Estructura fractal válida
        if hasattr(mercado, 'fractal_range') and mercado.fractal_range.get('valid', False):
            resultado["puntuacion_total"] += 2
            resultado["criterios_cumplidos"].append(f"Fractal: {mercado.fractal_range.get('status', 'N/A')}")
        
        # Criterio 3: Horario de trading
        if en_horario:
            resultado["puntuacion_total"] += 1
            resultado["criterios_cumplidos"].append("Horario válido")
        
        # Criterio 4: Estocastico en zona
        if estocastico is not None:
            if mercado.h4_bias == 'BULLISH' and estocastico < 30:
                resultado["puntuacion_total"] += 1
                resultado["criterios_cumplidos"].append("Estocastico oversold")
            elif mercado.h4_bias == 'BEARISH' and estocastico > 70:
                resultado["puntuacion_total"] += 1
                resultado["criterios_cumplidos"].append("Estocastico overbought")
        
        # Criterio 5: POIs cercanos
        total_pois = 0
        if hasattr(mercado, 'pois_h4'):
            total_pois += len([poi for poi in mercado.pois_h4 if not poi.get('mitigated', False)])
        if hasattr(mercado, 'pois_m15'):
            total_pois += len([poi for poi in mercado.pois_m15 if not poi.get('mitigated', False)])
        
        if total_pois > 0:
            resultado["puntuacion_total"] += 1
            resultado["criterios_cumplidos"].append(f"POIs activos: {total_pois}")
        
        # Determinar recomendación
        if resultado["puntuacion_total"] >= 5:
            resultado["recomendacion"] = "STRONG_ENTRY"
            resultado["confianza"] = 0.8
        elif resultado["puntuacion_total"] >= 3:
            resultado["recomendacion"] = "MODERATE_ENTRY"
            resultado["confianza"] = 0.6
        else:
            resultado["recomendacion"] = "NO_ENTRY"
            resultado["confianza"] = 0.3
        
        return resultado
        
    except (JSONDecodeError, ValueError) as e:
        return {
            "puntuacion_total": 0,
            "criterios_cumplidos": [],
            "recomendacion": "ERROR",
            "confianza": 0.0,
            "error": str(e)
        }

def get_premium_discount_zone(daily_candle, current_price):
    """
    Determina si el precio está en zona premium o discount.
    Función consolidada desde analisis_ict.py
    """
    try:
        if daily_candle is None:
            return {"zone": "UNKNOWN", "percentage": 0}
        
        daily_high = daily_candle.get('high', 0)
        daily_low = daily_candle.get('low', 0)
        daily_range = daily_high - daily_low
        
        if daily_range <= 0:
            return {"zone": "UNKNOWN", "percentage": 0}
        
        # Calcular posición en el rango (0-100%)
        position_in_range = ((current_price - daily_low) / daily_range) * 100
        
        # Determinar zona
        if position_in_range > 70:
            zone = "PREMIUM"
        elif position_in_range < 30:
            zone = "DISCOUNT"
        else:
            zone = "EQUILIBRIUM"
        
        return {
            "zone": zone,
            "percentage": position_in_range,
            "daily_high": daily_high,
            "daily_low": daily_low,
            "daily_mid": (daily_high + daily_low) / 2
        }
        
    except (JSONDecodeError, ValueError) as e:
        return {"zone": "ERROR", "percentage": 0, "error": str(e)}

def detectar_swing_points(df, len_left=5, len_right=1):
    """
    Detecta swing points en un DataFrame.
    Función consolidada desde analisis_ict.py (versión alternativa)
    """
    try:
        if df is None or len(df) < (len_left + len_right + 1):
            return [], []
        
        swing_highs = []
        swing_lows = []
        
        for i in range(len_left, len(df) - len_right):
            # Verificar swing high
            is_swing_high = True
            current_high = df.iloc[i]['high']
            
            # Verificar velas a la izquierda
            for j in range(i - len_left, i):
                if df.iloc[j]['high'] >= current_high:
                    is_swing_high = False
                    break
            
            # Verificar velas a la derecha
            if is_swing_high:
                for j in range(i + 1, i + len_right + 1):
                    if df.iloc[j]['high'] >= current_high:
                        is_swing_high = False
                        break
            
            if is_swing_high:
                swing_highs.append({
                    'index': i,
                    'price': current_high,
                    'time': df.index[i]
                })
            
            # Verificar swing low
            is_swing_low = True
            current_low = df.iloc[i]['low']
            
            # Verificar velas a la izquierda
            for j in range(i - len_left, i):
                if df.iloc[j]['low'] <= current_low:
                    is_swing_low = False
                    break
            
            # Verificar velas a la derecha
            if is_swing_low:
                for j in range(i + 1, i + len_right + 1):
                    if df.iloc[j]['low'] <= current_low:
                        is_swing_low = False
                        break
            
            if is_swing_low:
                swing_lows.append({
                    'index': i,
                    'price': current_low,
                    'time': df.index[i]
                })
        
        return swing_highs, swing_lows
        
    except (JSONDecodeError, ValueError) as e:
        enviar_senal_log("ERROR", f"Error en detección de swing points: {e}", __name__, "ict")
        return [], []

# =============================================================================
# FUNCIONES PARA COMPATIBILIDAD Y ANÁLISIS ESPECÍFICO
# =============================================================================

def _initialize_ict_cache_for_timeframe(timeframe_str):
    """Inicializa caché ICT para un timeframe específico."""
    return {
        'swing_highs': [],
        'swing_lows': [],
        'order_blocks': [],
        'fair_value_gaps': [],
        'last_update': None,
        'timeframe': timeframe_str
    }

def _analizar_estructura_single_tf(df, current_price, timeframe_str, lookback_swing, cache):
    """Analiza estructura en un solo timeframe."""
    try:
        if df is None or len(df) < lookback_swing:
            return cache
        
        # Detectar swing points
        swing_highs, swing_lows = detectar_swing_points(df, len_left=lookback_swing)
        
        # Actualizar caché
        cache['swing_highs'] = swing_highs
        cache['swing_lows'] = swing_lows
        cache['last_update'] = datetime.now()
        
        return cache
        
    except (JSONDecodeError, ValueError) as e:
        enviar_senal_log("ERROR", f"Error en análisis de estructura single TF: {e}", __name__, "ict")
        return cache

def _find_ob_before_break(df, break_idx, ob_type, timeframe_str):
    """Encuentra Order Block antes de un rompimiento."""
    try:
        # Lógica simplificada para encontrar OB
        if break_idx < ICT_CONFIG['ob_lookback_candles']:
            return None
        
        lookback_data = df.iloc[break_idx - ICT_CONFIG['ob_lookback_candles']:break_idx]
        
        if ob_type == 'bullish':
            # Buscar vela bajista antes del rompimiento alcista
            for i in range(len(lookback_data) - 1, -1, -1):
                candle = lookback_data.iloc[i]
                if candle['close'] < candle['open']:  # Vela bajista
                    return {
                        'type': 'BULLISH_OB',
                        'high': candle['high'],
                        'low': candle['low'],
                        'timeframe': timeframe_str,
                        'index': break_idx - ICT_CONFIG['ob_lookback_candles'] + i
                    }
        
        elif ob_type == 'bearish':
            # Buscar vela alcista antes del rompimiento bajista
            for i in range(len(lookback_data) - 1, -1, -1):
                candle = lookback_data.iloc[i]
                if candle['close'] > candle['open']:  # Vela alcista
                    return {
                        'type': 'BEARISH_OB',
                        'high': candle['high'],
                        'low': candle['low'],
                        'timeframe': timeframe_str,
                        'index': break_idx - ICT_CONFIG['ob_lookback_candles'] + i
                    }
        
        return None
        
    except (JSONDecodeError, ValueError):
        return None

def _update_ob_mitigation_and_break(df, obs):
    """Actualiza mitigación y rompimiento de Order Blocks."""
    try:
        if not obs or df is None or len(df) == 0:
            return obs
        
        current_price = df.iloc[-1]['close']
        current_high = df.iloc[-1]['high']
        current_low = df.iloc[-1]['low']
        
        for ob in obs:
            if ob.get('mitigated', False) or ob.get('broken', False):
                continue
            
            # Verificar mitigación
            if ob['type'] == 'BULLISH_OB':
                if current_low <= ob['low']:
                    ob['mitigated'] = True
                    ob['mitigation_time'] = df.index[-1]
                elif current_low < ob['high'] * 0.98:  # Rompimiento significativo
                    ob['broken'] = True
                    ob['break_time'] = df.index[-1]
            
            elif ob['type'] == 'BEARISH_OB':
                if current_high >= ob['high']:
                    ob['mitigated'] = True
                    ob['mitigation_time'] = df.index[-1]
                elif current_high > ob['low'] * 1.02:  # Rompimiento significativo
                    ob['broken'] = True
                    ob['break_time'] = df.index[-1]
        
        return obs
        
    except (JSONDecodeError, ValueError):
        return obs

def detectar_fair_value_gaps(df):
    """
    Detecta Fair Value Gaps en el DataFrame.
    Función consolidada desde analisis_ict.py
    """
    try:
        if df is None or len(df) < 3:
            return []
        
        fvgs = []
        
        for i in range(1, len(df) - 1):
            prev_candle = df.iloc[i-1]
            current_candle = df.iloc[i]
            next_candle = df.iloc[i+1]
            
            # FVG Alcista: gap entre prev_high y next_low
            if (prev_candle['high'] < next_candle['low'] and
                current_candle['close'] > current_candle['open']):  # Vela alcista
                
                gap_size = next_candle['low'] - prev_candle['high']
                if gap_size > ICT_CONFIG['fvg_gap_threshold']:
                    fvgs.append({
                        'type': 'BULLISH_FVG',
                        'high': next_candle['low'],
                        'low': prev_candle['high'],
                        'gap_size': gap_size,
                        'index': i,
                        'time': df.index[i],
                        'mitigated': False
                    })
            
            # FVG Bajista: gap entre prev_low y next_high
            elif (prev_candle['low'] > next_candle['high'] and
                  current_candle['close'] < current_candle['open']):  # Vela bajista
                
                gap_size = prev_candle['low'] - next_candle['high']
                if gap_size > ICT_CONFIG['fvg_gap_threshold']:
                    fvgs.append({
                        'type': 'BEARISH_FVG',
                        'high': prev_candle['low'],
                        'low': next_candle['high'],
                        'gap_size': gap_size,
                        'index': i,
                        'time': df.index[i],
                        'mitigated': False
                    })
        
        return fvgs
        
    except (JSONDecodeError, ValueError) as e:
        enviar_senal_log("ERROR", f"Error en detección de Fair Value Gaps: {e}", __name__, "ict")
        return []

def _update_fvg_mitigation(df, fvgs, timeframe_str):
    """Actualiza mitigación de Fair Value Gaps."""
    try:
        if not fvgs or df is None or len(df) == 0:
            return fvgs
        
        current_high = df.iloc[-1]['high']
        current_low = df.iloc[-1]['low']
        
        for fvg in fvgs:
            if fvg.get('mitigated', False):
                continue
            
            # Verificar mitigación del FVG
            if fvg['type'] == 'BULLISH_FVG':
                # FVG alcista se mitiga si el precio regresa al gap
                if current_low <= fvg['high'] and current_low >= fvg['low']:
                    fvg['mitigated'] = True
                    fvg['mitigation_time'] = df.index[-1]
            
            elif fvg['type'] == 'BEARISH_FVG':
                # FVG bajista se mitiga si el precio regresa al gap
                if current_high >= fvg['low'] and current_high <= fvg['high']:
                    fvg['mitigated'] = True
                    fvg['mitigation_time'] = df.index[-1]
        
        return fvgs
        
    except (JSONDecodeError, ValueError):
        return fvgs

# =============================================================================
# EXPORTACIONES PÚBLICAS
# =============================================================================

__all__ = [
    # Clases principales
    'MarketContext',
    'OptimizedICTAnalysis',
    
    # Funciones de análisis principal
    'update_market_context',
    'evaluar_checklist_de_entrada',
    'get_premium_discount_zone',
    
    # Detección de patrones
    'detectar_swing_points',
    'detectar_fair_value_gaps',
    
    # Funciones internas
    '_update_bias_h4',
    '_update_bias_m15',
    '_update_daily_range',
    '_find_new_pois',
    '_update_existing_pois',
    
    # Análisis de estructura
    '_initialize_ict_cache_for_timeframe',
    '_analizar_estructura_single_tf',
    '_find_ob_before_break',
    '_update_ob_mitigation_and_break',
    '_update_fvg_mitigation',
    
    # Configuración
    'ICT_CONFIG',
    'BIAS_TYPES',
    'STRUCTURE_TYPES'
]


# ===============================================================================
# 🚀 CLASE ICTDETECTOR - PLACEHOLDER PARA FASE 1.2
# ===============================================================================

class ICTDetector:
    """
    🔧 PLACEHOLDER: Clase ICTDetector para resolver ImportError
    
    Esta es una implementación básica temporal para FASE 1.2 del Plan de Ataque.
    En FASE 2.1 se implementará la funcionalidad completa integrando las
    funciones existentes en este módulo.
    
    ESTADO: PLACEHOLDER - Solo previene crashes de importación
    """
    
    def __init__(self):
        """Inicializar el detector ICT en modo placeholder"""
        self.initialized = False
        enviar_senal_log("INFO", "🔧 [ICTDETECTOR] Placeholder inicializado (FASE 1.2)", __name__, "general")
        
    def detect_patterns(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Placeholder para detección de patrones ICT
        FASE 2.1: Implementar detección real usando las funciones del módulo
        """
        enviar_senal_log("DEBUG", "🔧 [ICTDETECTOR] Placeholder detect_patterns llamado", __name__, "general")
        return []  # Lista vacía en placeholder
        
    def analyze_structure(self, candles: pd.DataFrame) -> Dict[str, Any]:
        """
        Placeholder para análisis de estructura
        FASE 2.1: Usar analyze_market_structure() del módulo
        """
        enviar_senal_log("DEBUG", "🔧 [ICTDETECTOR] Placeholder analyze_structure llamado", __name__, "general")
        return {'structure': 'unknown', 'experimental': True}
        
    def detect_bias(self, candles: pd.DataFrame) -> Dict[str, Any]:
        """
        Placeholder para detección de bias
        FASE 2.1: Usar analyze_bias() del módulo
        """
        enviar_senal_log("DEBUG", "🔧 [ICTDETECTOR] Placeholder detect_bias llamado", __name__, "general")
        return {'bias': 'neutral', 'experimental': True}
        
    def find_pois(self, candles: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Placeholder para encontrar POIs
        FASE 2.1: Usar analyze_pois() del módulo
        """
        enviar_senal_log("DEBUG", "🔧 [ICTDETECTOR] Placeholder find_pois llamado", __name__, "general")
        return []  # Lista vacía en placeholder
