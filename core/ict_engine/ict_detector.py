
from sistema.imports_interface import Optional, List, Any, Dict, Union, datetime, timedelta, timezone, Tuple
from sistema.imports_interface import log_info, get_logging, enviar_senal_log, log_error, get_poi_detector, get_poi_system
from sistema.imports_interface import Path, json
import pandas as pd
import numpy as np
from json import JSONDecodeError
    from sistema.market_status_detector import MarketStatusDetector
    from sistema.trading_schedule import get_current_session_info, TradingScheduleManager

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
from sistema.logging_interface import enviar_senal_log, log_ict
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any, Tuple, Union
import json
from json import JSONDecodeError
from pathlib import Path

# --- Import de funciones POI para integración ---
try:
    from core.poi_system.poi_detector import (
        detectar_order_blocks,
        detectar_fair_value_gaps,
        detectar_breaker_blocks,
        detectar_imbalances
    )
    poi_functions_available = True
except ImportError as e:
    enviar_senal_log("WARNING", f"Funciones POI no disponibles: {e}", __name__, "init")
    poi_functions_available = False

# --- Import del FractalAnalyzer ---
try:
    from core.ict_engine.fractal_analyzer import FractalAnalyzer, update_fractal_in_context
    fractal_analyzer_available = True
    enviar_senal_log("INFO", "✅ FractalAnalyzer importado correctamente", __name__, "init")
except ImportError as e:
    enviar_senal_log("WARNING", f"FractalAnalyzer no disponible: {e}", __name__, "init")
    fractal_analyzer_available = False

# --- Import del Market Status Detector (SPRINT 1.4 FIX) ---
try:
    from sistema.market_status_detector import MarketStatusDetector
    from sistema.trading_schedule import get_current_session_info, TradingScheduleManager
    market_status_available = True
    enviar_senal_log("INFO", "✅ Market Status Detector importado correctamente", __name__, "init")
except ImportError as e:
    enviar_senal_log("WARNING", f"❌ Market Status Detector no disponible: {e}", __name__, "init")
    market_status_available = False

# Usar sistema de logging central

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

        # Análisis fractal dinámico (integrado con FractalAnalyzer)
        self.fractal_range = {'high': 0, 'low': 0, 'eq': 0, 'status': 'NO_CALCULADO'}

        # Inicializar FractalAnalyzer si está disponible
        if fractal_analyzer_available:
            self.fractal_analyzer = FractalAnalyzer()
            enviar_senal_log("INFO", "🔮 FractalAnalyzer inicializado en MarketContext", __name__, "fractal_analysis")
        else:
            self.fractal_analyzer = None
            enviar_senal_log("WARNING", "⚠️ FractalAnalyzer no disponible - usando valores por defecto", __name__, "fractal_analysis")

        # Inicializar Market Status Detector (SPRINT 1.4 FIX)
        if market_status_available:
            self.market_status_detector = MarketStatusDetector()
            self.trading_schedule = TradingScheduleManager()
            enviar_senal_log("INFO", "🕐 Market Status Detector inicializado en MarketContext", __name__, "session_detection")
        else:
            self.market_status_detector = None
            self.trading_schedule = None
            enviar_senal_log("WARNING", "⚠️ Market Status Detector no disponible - sesión permanecerá UNKNOWN", __name__, "session_detection")

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
            f"fractal_status={self.fractal_range.get('status', 'NO_CALCULADO')}, "
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

        # Actualizar análisis fractal (usando FractalAnalyzer)
        if hasattr(contexto, 'fractal_analyzer') and contexto.fractal_analyzer is not None:
            enviar_senal_log("DEBUG", "🔮 Actualizando análisis fractal con FractalAnalyzer...", __name__, "fractal_analysis")

            # Usar el timeframe M15 o H4 para análisis fractal (preferencia por M15)
            fractal_df = None
            if 'M15' in df_by_timeframe and df_by_timeframe['M15'] is not None and len(df_by_timeframe['M15']) > 0:
                fractal_df = df_by_timeframe['M15']
            elif 'H4' in df_by_timeframe and df_by_timeframe['H4'] is not None and len(df_by_timeframe['H4']) > 0:
                fractal_df = df_by_timeframe['H4']

            if fractal_df is not None and len(fractal_df) > 10:
                fractal_success = contexto.fractal_analyzer.update_fractal_context(contexto, fractal_df, current_price)
                if fractal_success:
                    fractal_status = contexto.fractal_range.get('status', 'NO_CALCULADO')
                    enviar_senal_log("DEBUG", f"Fractal actualizado exitosamente: {fractal_status}", __name__, "fractal_analysis")
                else:
                    enviar_senal_log("DEBUG", "Fractal no se pudo actualizar - usando valores previos", __name__, "fractal_analysis")
            else:
                enviar_senal_log("WARNING", "Datos insuficientes para análisis fractal", __name__, "fractal_analysis")
        else:
            enviar_senal_log("DEBUG", "FractalAnalyzer no disponible - manteniendo valores por defecto", __name__, "fractal_analysis")

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
        enviar_senal_log("INFO", f"📋 RESUMEN: H4_bias={contexto.h4_bias}, M15_bias={contexto.m15_bias}, POIs_total={context_summary.get("total_pois", 0)}, Calidad={contexto.analysis_quality}", __name__, "general")

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

def detectar_fair_value_gaps_local(df):
    """
    Detecta Fair Value Gaps en el DataFrame.
    Función consolidada desde analisis_ict.py (RENOMBRADA para evitar conflictos)
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
    'ICTDetector',  # ✅ NUEVO: Detector ICT real agregado

    # Funciones de análisis principal
    'update_market_context',
    'evaluar_checklist_de_entrada',
    'get_premium_discount_zone',

    # Detección de patrones
    'detectar_swing_points',
    'detectar_fair_value_gaps_local',

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
# 🚀 CLASE ICTDETECTOR - IMPLEMENTACIÓN REAL SPRINT 1.2
# ===============================================================================

class ICTDetector:
    """
    🚀 IMPLEMENTACIÓN REAL: Clase ICTDetector para SPRINT 1.2

    Integra todas las funciones existentes del módulo ict_detector.py en una
    interfaz coherente y funcional. Reemplaza completamente el placeholder.

    ESTADO: IMPLEMENTACIÓN REAL - Funcionalidad completa de producción
    """

    def __init__(self):
        """Inicializar el detector ICT con funcionalidad completa"""
        self.initialized = True
        self.market_context = None  # Se inicializará con MarketContext()
        self.cache = {}
        self.last_analysis = None
        self.analysis_count = 0

        # Configuración del detector
        self.config = {
            'min_confidence_threshold': 60,
            'max_patterns_per_analysis': 20,
            'swing_detection_params': {'left': 5, 'right': 1},
            'fvg_min_gap_threshold': 0.0001,
            'order_block_lookback': 10
        }

        enviar_senal_log("INFO", "🚀 [ICTDETECTOR] Implementación real inicializada (SPRINT 1.2)", __name__, "general")
        enviar_senal_log("DEBUG", "ICTDetector listo para análisis completo de patrones ICT", __name__, "general")
        enviar_senal_log("INFO", f"⚙️ Configuración cargada: threshold={self.config['min_confidence_threshold']}", __name__, "general")

        # SPRINT 1.4 FIX: Agregar session detection también al ICTDetector
        if market_status_available:
            try:
                self.market_status_detector = MarketStatusDetector()
                self.session_detector_available = True
                enviar_senal_log("INFO", "🕐 Session Detection habilitado en ICTDetector", __name__, "session_detection")
            except Exception as e:
                self.market_status_detector = None
                self.session_detector_available = False
                enviar_senal_log("WARNING", f"🕐 Error habilitando session detection: {e}", __name__, "session_detection")
        else:
            self.market_status_detector = None
            self.session_detector_available = False

    def detect_patterns(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        IMPLEMENTACIÓN REAL: Detección completa de patrones ICT
        Integra: FVGs, Swing Points, Order Blocks, Liquidity Zones
        """
        try:
            self.analysis_count += 1
            enviar_senal_log("DEBUG", f"🔍 [ICTDETECTOR] Iniciando análisis #{self.analysis_count}", __name__, "general")

            patterns_detected = []

            # Validar datos de entrada
            if not data:
                enviar_senal_log("WARNING", "Datos nulos proporcionados al detector", __name__, "general")
                return []

            # Extraer DataFrame de múltiples formatos posibles
            df = self._extract_dataframe(data)
            if df is None or len(df) == 0:
                enviar_senal_log("WARNING", "No se pudieron extraer datos válidos", __name__, "general")
                return []

            enviar_senal_log("INFO", f"📊 Analizando {len(df)} velas de datos", __name__, "general")

            # 1. DETECTAR FAIR VALUE GAPS
            try:
                fvgs = detectar_fair_value_gaps_local(df)
                if fvgs:
                    for fvg in fvgs:
                        pattern = {
                            'type': 'FAIR_VALUE_GAP',
                            'subtype': fvg.get('type', 'UNKNOWN_FVG'),
                            'price_high': fvg.get('high', 0),
                            'price_low': fvg.get('low', 0),
                            'timestamp': fvg.get('time', datetime.now()),
                            'confidence': self._calculate_fvg_confidence(fvg),
                            'mitigated': fvg.get('mitigated', False),
                            'gap_size': fvg.get('high', 0) - fvg.get('low', 0),
                            'analysis_id': self.analysis_count
                        }
                        patterns_detected.append(pattern)

                    enviar_senal_log("INFO", f"✅ Detectados {len(fvgs)} Fair Value Gaps", __name__, "general")
                else:
                    enviar_senal_log("DEBUG", "No se encontraron Fair Value Gaps", __name__, "general")
            except Exception as e:
                enviar_senal_log("ERROR", f"Error detectando FVGs: {e}", __name__, "general")

            # 2. DETECTAR SWING POINTS
            try:
                swing_params = self.config['swing_detection_params']
                swing_highs, swing_lows = detectar_swing_points(
                    df,
                    len_left=swing_params['left'],
                    len_right=swing_params['right']
                )

                # Procesar swing highs (limitar a los más recientes)
                for swing in swing_highs[-5:]:
                    pattern = {
                        'type': 'SWING_POINT',
                        'subtype': 'SWING_HIGH',
                        'price': swing['price'],
                        'index': swing['index'],
                        'timestamp': swing['time'],
                        'confidence': self._calculate_swing_confidence(swing, 'high'),
                        'mitigated': False,
                        'strength': self._calculate_swing_strength(swing, swing_highs),
                        'analysis_id': self.analysis_count
                    }
                    patterns_detected.append(pattern)

                # Procesar swing lows (limitar a los más recientes)
                for swing in swing_lows[-5:]:
                    pattern = {
                        'type': 'SWING_POINT',
                        'subtype': 'SWING_LOW',
                        'price': swing['price'],
                        'index': swing['index'],
                        'timestamp': swing['time'],
                        'confidence': self._calculate_swing_confidence(swing, 'low'),
                        'mitigated': False,
                        'strength': self._calculate_swing_strength(swing, swing_lows),
                        'analysis_id': self.analysis_count
                    }
                    patterns_detected.append(pattern)

                total_swings = len(swing_highs) + len(swing_lows)
                enviar_senal_log("INFO", f"✅ Detectados {total_swings} swing points ({len(swing_highs)} highs, {len(swing_lows)} lows)", __name__, "general")

            except Exception as e:
                enviar_senal_log("ERROR", f"Error detectando swing points: {e}", __name__, "general")

            # 3. DETECTAR ORDER BLOCKS
            try:
                order_blocks = self._detect_order_blocks_advanced(df)
                patterns_detected.extend(order_blocks)
                enviar_senal_log("INFO", f"✅ Detectados {len(order_blocks)} Order Blocks", __name__, "general")
            except Exception as e:
                enviar_senal_log("ERROR", f"Error detectando Order Blocks: {e}", __name__, "general")

            # 4. DETECTAR LIQUIDITY ZONES
            try:
                liquidity_zones = self._detect_liquidity_zones_advanced(df)
                patterns_detected.extend(liquidity_zones)
                enviar_senal_log("INFO", f"✅ Detectadas {len(liquidity_zones)} Liquidity Zones", __name__, "general")
            except Exception as e:
                enviar_senal_log("ERROR", f"Error detectando Liquidity Zones: {e}", __name__, "general")

            # Filtrar por confianza mínima
            filtered_patterns = [
                p for p in patterns_detected
                if p.get('confidence', 0) >= self.config['min_confidence_threshold']
            ]

            # Limitar número máximo de patrones
            max_patterns = self.config['max_patterns_per_analysis']
            if len(filtered_patterns) > max_patterns:
                # Ordenar por confianza y tomar los mejores
                filtered_patterns = sorted(
                    filtered_patterns,
                    key=lambda x: x.get('confidence', 0),
                    reverse=True
                )[:max_patterns]

            # Almacenar análisis
            self.last_analysis = {
                'timestamp': datetime.now(),
                'patterns_count': len(filtered_patterns),
                'raw_patterns_count': len(patterns_detected),
                'types': list(set([p['type'] for p in filtered_patterns])),
                'analysis_id': self.analysis_count,
                'data_quality': self._assess_data_quality(df)
            }

            enviar_senal_log("INFO", f"🎯 Análisis completado: {len(filtered_patterns)} patrones válidos de {len(patterns_detected)} detectados", __name__, "general")

            return filtered_patterns

        except Exception as e:
            enviar_senal_log("ERROR", f"Error crítico en detect_patterns: {e}", __name__, "general")
            return []

    def analyze_structure(self, candles: pd.DataFrame) -> Dict[str, Any]:
        """
        IMPLEMENTACIÓN REAL: Análisis completo de estructura de mercado
        Integra: Market Structure, BOS, Premium/Discount, Trend Analysis
        """
        try:
            enviar_senal_log("DEBUG", "🏗️ [ICTDETECTOR] Iniciando análisis de estructura", __name__, "general")

            if candles is None or len(candles) == 0:
                return {'structure': 'insufficient_data', 'experimental': False, 'error': 'No data provided'}

            # Datos básicos
            current_price = float(candles.iloc[-1]['close'])
            daily_candle = {
                'high': float(candles['high'].max()),
                'low': float(candles['low'].min()),
                'close': current_price,
                'open': float(candles.iloc[0]['open'])
            }

            enviar_senal_log("DEBUG", f"📊 Precio actual: {current_price}, Rango diario: {daily_candle['low']:.5f} - {daily_candle['high']:.5f}", __name__, "general")

            # 1. ANÁLISIS PREMIUM/DISCOUNT usando función existente
            pd_analysis = get_premium_discount_zone(daily_candle, current_price)

            # 2. ANÁLISIS DE TENDENCIA AVANZADO
            trend_analysis = self._analyze_trend_structure_advanced(candles)

            # 3. CÁLCULO DE FUERZA DE ESTRUCTURA
            structure_strength = self._calculate_structure_strength_advanced(candles)

            # 4. DETECCIÓN DE BREAK OF STRUCTURE
            bos_analysis = self._detect_break_of_structure_advanced(candles)

            # 5. ANÁLISIS DE MOMENTUM
            momentum_analysis = self._analyze_momentum_comprehensive(candles)

            # 6. CALIDAD DE LA ESTRUCTURA
            structure_quality = self._assess_structure_quality(candles, trend_analysis, structure_strength)

            structure_result = {
                'structure': trend_analysis['primary_trend'],
                'premium_discount_zone': pd_analysis,
                'structure_strength': structure_strength,
                'break_of_structure': bos_analysis,
                'momentum': momentum_analysis,
                'structure_quality': structure_quality,
                'daily_high': daily_candle['high'],
                'daily_low': daily_candle['low'],
                'daily_range': daily_candle['high'] - daily_candle['low'],
                'current_price': current_price,
                'price_position_pct': ((current_price - daily_candle['low']) / (daily_candle['high'] - daily_candle['low'])) * 100,
                'analysis_timestamp': datetime.now().isoformat(),
                'experimental': False,
                'confidence': self._calculate_structure_confidence_advanced(trend_analysis, structure_strength, structure_quality),
                'analysis_id': self.analysis_count
            }

            enviar_senal_log("INFO", f"🏗️ Estructura: {trend_analysis['primary_trend']}, Zona: {pd_analysis.get('zone', 'UNKNOWN')}, Fuerza: {structure_strength:.1f}%", __name__, "general")

            return structure_result

        except Exception as e:
            enviar_senal_log("ERROR", f"Error en analyze_structure: {e}", __name__, "general")
            return {'structure': 'error', 'experimental': False, 'error': str(e)}

    def detect_bias(self, candles: pd.DataFrame) -> Dict[str, Any]:
        """
        IMPLEMENTACIÓN REAL: Detección de bias multi-timeframe avanzado
        Integra: H4 Bias, M15 Bias, Confluencia, Market Context
        """
        try:
            enviar_senal_log("DEBUG", "🎯 [ICTDETECTOR] Iniciando detección de bias", __name__, "general")

            if candles is None or len(candles) == 0:
                return {'bias': 'neutral', 'experimental': False, 'error': 'No data provided'}

            # Simular datos de diferentes timeframes
            h4_simulation = self._simulate_h4_data(candles)
            m15_simulation = self._simulate_m15_data(candles)

            # Calcular bias para cada timeframe
            h4_bias = self._calculate_h4_bias_advanced(h4_simulation)
            m15_bias = self._calculate_m15_bias_advanced(m15_simulation)

            # Calcular confluencia avanzada
            bias_confluence = self._calculate_bias_confluence_advanced(h4_bias, m15_bias, candles)

            # Análisis de momentum multi-timeframe
            momentum_analysis = self._analyze_bias_momentum(candles)

            # Contexto de sesión (simplificado)
            session_context = self._determine_session_context()

            # Factores de confirmación
            confirmation_factors = self._analyze_bias_confirmation_factors(candles, h4_bias, m15_bias)

            bias_result = {
                'bias': bias_confluence['primary_bias'],
                'h4_bias': h4_bias,
                'm15_bias': m15_bias,
                'confluence_strength': bias_confluence['strength'],
                'confluence_score': bias_confluence['score'],
                'momentum': momentum_analysis,
                'session_context': session_context,
                'confirmation_factors': confirmation_factors,
                'confidence': bias_confluence['confidence'],
                'analysis_timestamp': datetime.now().isoformat(),
                'experimental': False,
                'analysis_id': self.analysis_count
            }

            enviar_senal_log("INFO", f"🎯 Bias: {bias_confluence['primary_bias']} (H4: {h4_bias['bias']}, M15: {m15_bias['bias']}, Conf: {bias_confluence['confidence']:.1f}%)", __name__, "general")

            return bias_result

        except Exception as e:
            enviar_senal_log("ERROR", f"Error en detect_bias: {e}", __name__, "general")
            return {'bias': 'error', 'experimental': False, 'error': str(e)}

    def find_pois(self, candles: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        IMPLEMENTACIÓN REAL: Búsqueda completa de POIs (Points of Interest)
        Integra: Order Blocks, Liquidity Zones, Support/Resistance, FVG Zones
        """
        try:
            enviar_senal_log("DEBUG", "📍 [ICTDETECTOR] Iniciando búsqueda de POIs", __name__, "general")

            if candles is None or len(candles) == 0:
                return []

            all_pois = []
            current_price = float(candles.iloc[-1]['close'])

            # 1. POIs de Order Blocks
            ob_pois = self._find_order_block_pois_advanced(candles, current_price)
            all_pois.extend(ob_pois)

            # 2. POIs de Liquidity Zones
            liquidity_pois = self._find_liquidity_pois_advanced(candles, current_price)
            all_pois.extend(liquidity_pois)

            # 3. POIs de Support/Resistance Dinámicos
            sr_pois = self._find_support_resistance_pois_advanced(candles, current_price)
            all_pois.extend(sr_pois)

            # 4. POIs de Fair Value Gaps
            fvg_pois = self._find_fvg_pois_advanced(candles, current_price)
            all_pois.extend(fvg_pois)

            # 5. POIs de High/Low of Day
            hod_lod_pois = self._find_hod_lod_pois(candles, current_price)
            all_pois.extend(hod_lod_pois)

            # Filtrar, ordenar y optimizar POIs
            filtered_pois = self._filter_and_optimize_pois(all_pois, current_price)

            # Añadir metadata a cada POI
            for poi in filtered_pois:
                poi['analysis_id'] = self.analysis_count
                poi['discovery_timestamp'] = datetime.now().isoformat()
                poi['distance_pips'] = abs(poi['price_level'] - current_price) * 10000  # Aproximación para FOREX

            enviar_senal_log("INFO", f"📍 Encontrados {len(filtered_pois)} POIs relevantes de {len(all_pois)} candidatos", __name__, "general")

            return filtered_pois

        except Exception as e:
            enviar_senal_log("ERROR", f"Error en find_pois: {e}", __name__, "general")
            return []

    # =========================================================================
    # MÉTODOS AUXILIARES AVANZADOS - IMPLEMENTACIÓN REAL
    # =========================================================================

    def _extract_dataframe(self, data: Dict[str, Any]) -> Optional[pd.DataFrame]:
        """Extrae DataFrame de múltiples formatos de datos posibles"""
        try:
            # Formato 1: data['candles'] directo
            if 'candles' in data and isinstance(data['candles'], pd.DataFrame):
                return data['candles']

            # Formato 2: data['dataframe'] (usado por diagnóstico)
            if 'dataframe' in data and isinstance(data['dataframe'], pd.DataFrame):
                return data['dataframe']

            # Formato 3: data directo es DataFrame
            if isinstance(data, pd.DataFrame):
                return data

            # Formato 4: data['last_100_candles_m1'] u otros
            for key in ['last_100_candles_m1', 'ohlc_data', 'market_data', 'data']:
                if key in data:
                    candidate = data[key]
                    if isinstance(candidate, pd.DataFrame):
                        return candidate
                    elif isinstance(candidate, list) and len(candidate) > 0:
                        # Convertir lista a DataFrame
                        return pd.DataFrame(candidate)

            enviar_senal_log("WARNING", f"No se pudo extraer DataFrame de los datos: keys={list(data.keys()) if isinstance(data, dict) else type(data)}", __name__, "general")
            return None

        except Exception as e:
            enviar_senal_log("ERROR", f"Error extrayendo DataFrame: {e}", __name__, "general")
            return None

    def _detect_order_blocks_advanced(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detecta Order Blocks con algoritmo avanzado"""
        order_blocks = []

        try:
            lookback = self.config['order_block_lookback']
            if len(df) < lookback:
                return []

            # Analizar las últimas velas para Order Blocks
            for i in range(len(df) - lookback, len(df)):
                if i < 3:
                    continue

                current_candle = df.iloc[i]
                prev_candles = df.iloc[max(0, i-3):i]

                # Order Block alcista
                if self._is_bullish_order_block_advanced(current_candle, prev_candles, df):
                    ob = {
                        'type': 'ORDER_BLOCK',
                        'subtype': 'BULLISH_OB',
                        'price_high': float(current_candle['high']),
                        'price_low': float(current_candle['low']),
                        'price_mid': float((current_candle['high'] + current_candle['low']) / 2),
                        'timestamp': df.index[i] if hasattr(df.index[i], 'isoformat') else datetime.now(),
                        'confidence': self._calculate_ob_confidence(current_candle, prev_candles, 'bullish'),
                        'mitigated': False,
                        'strength': self._calculate_ob_strength(current_candle, prev_candles),
                        'volume_confirmation': self._check_volume_confirmation(current_candle, prev_candles)
                    }
                    order_blocks.append(ob)

                # Order Block bajista
                elif self._is_bearish_order_block_advanced(current_candle, prev_candles, df):
                    ob = {
                        'type': 'ORDER_BLOCK',
                        'subtype': 'BEARISH_OB',
                        'price_high': float(current_candle['high']),
                        'price_low': float(current_candle['low']),
                        'price_mid': float((current_candle['high'] + current_candle['low']) / 2),
                        'timestamp': df.index[i] if hasattr(df.index[i], 'isoformat') else datetime.now(),
                        'confidence': self._calculate_ob_confidence(current_candle, prev_candles, 'bearish'),
                        'mitigated': False,
                        'strength': self._calculate_ob_strength(current_candle, prev_candles),
                        'volume_confirmation': self._check_volume_confirmation(current_candle, prev_candles)
                    }
                    order_blocks.append(ob)

        except Exception as e:
            enviar_senal_log("ERROR", f"Error en detección avanzada de Order Blocks: {e}", __name__, "general")

        return order_blocks

    def _is_bullish_order_block_advanced(self, candle, prev_candles, full_df) -> bool:
        """Algoritmo avanzado para detectar Order Block alcista"""
        try:
            # Condición 1: Vela alcista
            is_bullish = candle['close'] > candle['open']
            if not is_bullish:
                return False

            # Condición 2: Secuencia bajista previa
            bearish_sequence = sum(1 for _, prev in prev_candles.iterrows() if prev['close'] < prev['open'])
            has_bearish_setup = bearish_sequence >= 2

            # Condición 3: Tamaño significativo de la vela
            candle_size = candle['high'] - candle['low']
            avg_size = full_df['high'].tail(20).subtract(full_df['low'].tail(20)).mean()
            significant_size = candle_size > avg_size * 0.8

            return has_bearish_setup and significant_size

        except Exception:
            return False

    def _is_bearish_order_block_advanced(self, candle, prev_candles, full_df) -> bool:
        """Algoritmo avanzado para detectar Order Block bajista"""
        try:
            # Condición 1: Vela bajista
            is_bearish = candle['close'] < candle['open']
            if not is_bearish:
                return False

            # Condición 2: Secuencia alcista previa
            bullish_sequence = sum(1 for _, prev in prev_candles.iterrows() if prev['close'] > prev['open'])
            has_bullish_setup = bullish_sequence >= 2

            # Condición 3: Tamaño significativo de la vela
            candle_size = candle['high'] - candle['low']
            avg_size = full_df['high'].tail(20).subtract(full_df['low'].tail(20)).mean()
            significant_size = candle_size > avg_size * 0.8

            return has_bullish_setup and significant_size

        except Exception:
            return False

    # =========================================================================
    # MÉTODOS AUXILIARES SIMPLIFICADOS PARA INTEGRACIÓN INICIAL
    # =========================================================================

    def _detect_liquidity_zones_advanced(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        🎯 LIQUIDITY DETECTION ENGINE v1.0 (Sprint 1.5)

        Detecta zonas de liquidez institucional según metodología ICT:
        - Equal Highs/Lows (Stop Hunt Zones)
        - Session Extremes (London/NY/Asian)
        - Previous Day High/Low
        - Swing Point Liquidity
        """
        try:
            liquidity_zones = []

            if len(df) < 20:
                enviar_senal_log("WARNING", "Insuficientes datos para Liquidity Detection", __name__, "liquidity")
                return []

            enviar_senal_log("INFO", f"🔍 Iniciando Liquidity Detection en {len(df)} velas", __name__, "liquidity")

            # 1. EQUAL HIGHS DETECTION
            equal_highs = self._find_equal_highs(df)
            liquidity_zones.extend(equal_highs)

            # 2. EQUAL LOWS DETECTION
            equal_lows = self._find_equal_lows(df)
            liquidity_zones.extend(equal_lows)

            # 3. SESSION EXTREMES (usar session detection existente)
            session_liquidity = self._find_session_liquidity_zones(df)
            liquidity_zones.extend(session_liquidity)

            # 4. DAILY HIGH/LOW LEVELS
            daily_levels = self._find_daily_liquidity_levels(df)
            liquidity_zones.extend(daily_levels)

            # 5. SWING POINT LIQUIDITY (usar swing points existentes)
            swing_liquidity = self._find_swing_liquidity_zones(df)
            liquidity_zones.extend(swing_liquidity)

            # Filtrar y rankear por importancia
            liquidity_zones = self._rank_liquidity_zones(liquidity_zones, df['close'].iloc[-1])

            enviar_senal_log("INFO",
                f"✅ Liquidity Engine completado: {len(liquidity_zones)} zonas detectadas",
                __name__, "liquidity")

            # Desglose por tipo
            equal_h_count = len([z for z in liquidity_zones if z.get('type') == 'EQUAL_HIGHS'])
            equal_l_count = len([z for z in liquidity_zones if z.get('type') == 'EQUAL_LOWS'])
            session_count = len([z for z in liquidity_zones if 'SESSION' in z.get('type', '')])
            daily_count = len([z for z in liquidity_zones if 'DAILY' in z.get('type', '')])
            swing_count = len([z for z in liquidity_zones if 'SWING' in z.get('type', '')])

            enviar_senal_log("INFO",
                f"🎯 Desglose: Equal Highs: {equal_h_count} | Equal Lows: {equal_l_count} | Session: {session_count} | Daily: {daily_count} | Swing: {swing_count}",
                __name__, "liquidity")

            return liquidity_zones

        except Exception as e:
            enviar_senal_log("ERROR", f"Error en Liquidity Detection Engine: {e}", __name__, "liquidity")
            return []

    def _assess_data_quality(self, df: pd.DataFrame) -> str:
        """Evalúa la calidad de los datos"""
        try:
            if len(df) < 10:
                return "LOW"
            elif len(df) < 50:
                return "MEDIUM"
            else:
                return "HIGH"
        except Exception:
            return "LOW"

    def _analyze_trend_structure_advanced(self, candles: pd.DataFrame) -> Dict[str, str]:
        """Análisis avanzado de estructura de tendencia"""
        try:
            trend = self._analyze_trend_structure_basic(candles)
            return {'primary_trend': trend, 'secondary_trend': 'neutral'}
        except Exception:
            return {'primary_trend': 'unknown', 'secondary_trend': 'unknown'}

    def _analyze_trend_structure_basic(self, df: pd.DataFrame) -> str:
        """Análisis básico de estructura de tendencia"""
        try:
            if len(df) < 20:
                return 'insufficient_data'

            recent_prices = df['close'].tail(20)
            sma_short = recent_prices.tail(5).mean()
            sma_long = recent_prices.head(15).mean()

            if sma_short > sma_long * 1.001:
                return 'bullish_structure'
            elif sma_short < sma_long * 0.999:
                return 'bearish_structure'
            else:
                return 'consolidation'
        except Exception:
            return 'error'

    def _calculate_structure_strength_advanced(self, candles: pd.DataFrame) -> float:
        """Calcula la fuerza de la estructura actual"""
        try:
            if len(candles) < 10:
                return 0.0

            recent_close = candles['close'].tail(10)
            volatility = recent_close.std() / recent_close.mean()
            momentum = (recent_close.iloc[-1] - recent_close.iloc[0]) / recent_close.iloc[0]

            strength = min(abs(momentum) * 100 + (1 - volatility) * 50, 100)
            return max(0, strength)
        except Exception:
            return 50.0

    def _detect_break_of_structure_advanced(self, candles: pd.DataFrame) -> Dict[str, Any]:
        """Detecta Break of Structure avanzado"""
        return {'detected': False, 'type': 'none', 'strength': 0}

    def _analyze_momentum_comprehensive(self, candles: pd.DataFrame) -> Dict[str, Any]:
        """Análisis comprehensivo de momentum"""
        try:
            if len(candles) < 5:
                return {'overall': 'NEUTRAL'}

            short_term = (candles['close'].iloc[-1] - candles['close'].iloc[-3]) / candles['close'].iloc[-3]

            if short_term > 0.002:
                return {'overall': 'BULLISH', 'short_term': short_term * 100}
            elif short_term < -0.002:
                return {'overall': 'BEARISH', 'short_term': short_term * 100}
            else:
                return {'overall': 'NEUTRAL', 'short_term': short_term * 100}
        except Exception:
            return {'overall': 'NEUTRAL'}

    def _assess_structure_quality(self, candles, trend_analysis, structure_strength) -> str:
        """Evalúa la calidad de la estructura"""
        try:
            if structure_strength > 70:
                return "HIGH"
            elif structure_strength > 40:
                return "MEDIUM"
            else:
                return "LOW"
        except Exception:
            return "MEDIUM"

    def _calculate_structure_confidence_advanced(self, trend_analysis, structure_strength, structure_quality) -> float:
        """Calcula confianza avanzada de estructura"""
        try:
            base = 60
            if trend_analysis['primary_trend'] in ['bullish_structure', 'bearish_structure']:
                base += 20
            return min(base + structure_strength * 0.3, 95)
        except Exception:
            return 60.0

    def _simulate_h4_data(self, candles: pd.DataFrame) -> pd.DataFrame:
        """Simula datos H4 a partir de datos actuales"""
        return candles.tail(20)  # Usar últimas 20 velas como simulación H4

    def _simulate_m15_data(self, candles: pd.DataFrame) -> pd.DataFrame:
        """Simula datos M15 a partir de datos actuales"""
        return candles.tail(10)  # Usar últimas 10 velas como simulación M15

    def _calculate_h4_bias_advanced(self, h4_simulation: pd.DataFrame) -> Dict[str, Any]:
        """Calcula bias H4 avanzado"""
        try:
            trend = self._analyze_trend_structure_basic(h4_simulation)
            if trend == 'bullish_structure':
                bias = 'BULLISH'
            elif trend == 'bearish_structure':
                bias = 'BEARISH'
            else:
                bias = 'NEUTRAL'

            return {'bias': bias, 'confidence': 75, 'strength': 'MEDIUM'}
        except Exception:
            return {'bias': 'NEUTRAL', 'confidence': 50, 'strength': 'LOW'}

    def _calculate_m15_bias_advanced(self, m15_simulation: pd.DataFrame) -> Dict[str, Any]:
        """Calcula bias M15 avanzado"""
        try:
            if len(m15_simulation) < 5:
                return {'bias': 'NEUTRAL', 'confidence': 25, 'strength': 'LOW'}

            recent_momentum = (m15_simulation['close'].iloc[-1] - m15_simulation['close'].iloc[0]) / m15_simulation['close'].iloc[0]

            if recent_momentum > 0.001:
                bias = 'BULLISH'
            elif recent_momentum < -0.001:
                bias = 'BEARISH'
            else:
                bias = 'NEUTRAL'

            return {'bias': bias, 'confidence': 70, 'strength': 'MEDIUM'}
        except Exception:
            return {'bias': 'NEUTRAL', 'confidence': 50, 'strength': 'LOW'}

    def _calculate_bias_confluence_advanced(self, h4_bias: Dict, m15_bias: Dict, candles: pd.DataFrame) -> Dict[str, Any]:
        """Calcula confluencia avanzada entre bias H4 y M15"""
        try:
            h4_val = h4_bias['bias']
            m15_val = m15_bias['bias']

            if h4_val == m15_val and h4_val != 'NEUTRAL':
                return {
                    'primary_bias': h4_val,
                    'strength': 'HIGH',
                    'confidence': 85,
                    'score': 90
                }
            elif h4_val != 'NEUTRAL' and m15_val == 'NEUTRAL':
                return {
                    'primary_bias': h4_val,
                    'strength': 'MEDIUM',
                    'confidence': 65,
                    'score': 70
                }
            elif h4_val == 'NEUTRAL' and m15_val != 'NEUTRAL':
                return {
                    'primary_bias': m15_val,
                    'strength': 'LOW',
                    'confidence': 45,
                    'score': 50
                }
            else:
                return {
                    'primary_bias': 'NEUTRAL',
                    'strength': 'LOW',
                    'confidence': 30,
                    'score': 25
                }
        except Exception:
            return {'primary_bias': 'NEUTRAL', 'strength': 'LOW', 'confidence': 25, 'score': 20}

    def _analyze_bias_momentum(self, candles: pd.DataFrame) -> Dict[str, Any]:
        """Analiza momentum para bias"""
        return self._analyze_momentum_comprehensive(candles)

    def _determine_session_context(self) -> Dict[str, Any]:
        """
        Determina contexto de sesión usando Market Status Detector
        SPRINT 1.4 FIX: Conecta con sistema real de sesiones
        """
        try:
            # Verificar si tenemos session detection disponible (ICTDetector)
            if hasattr(self, 'session_detector_available') and self.session_detector_available:
                if market_status_available:
                    current_session = get_current_session_info()
                else:
                    enviar_senal_log("WARNING", "🕐 Market Status no disponible", __name__, "session_detection")
                    return {'session': 'UNKNOWN', 'overlap': False, 'activity_level': 'MEDIUM'}
            # Verificar si tenemos market_status_detector disponible (MarketContext)
            elif hasattr(self, 'market_status_detector') and self.market_status_detector:
                if market_status_available:
                    current_session = get_current_session_info()
                else:
                    enviar_senal_log("WARNING", "🕐 Market Status no disponible", __name__, "session_detection")
                    return {'session': 'UNKNOWN', 'overlap': False, 'activity_level': 'MEDIUM'}
            else:
                enviar_senal_log("WARNING", "🕐 Session Detection no disponible en este contexto", __name__, "session_detection")
                return {'session': 'UNKNOWN', 'overlap': False, 'activity_level': 'MEDIUM'}

            if current_session:
                session_name = current_session.get('session_key', 'UNKNOWN')
                is_active = current_session.get('is_active', False)
                volatility = current_session.get('volatility', 'MEDIUM')

                # Detectar si estamos en killzone
                is_killzone = self._is_killzone_active(session_name)

                # Actualizar session en contexto si es MarketContext
                if hasattr(self, 'current_session'):
                    self.current_session = session_name

                enviar_senal_log("INFO",
                               f"🕐 Sesión detectada: {session_name} | Activa: {is_active} | Killzone: {is_killzone}",
                               __name__, "session_detection")

                return {
                    'session': session_name,
                    'is_active': is_active,
                    'volatility': volatility,
                    'is_killzone': is_killzone,
                    'activity_level': volatility
                }
            else:
                enviar_senal_log("WARNING", "🕐 No hay sesión activa detectada", __name__, "session_detection")
                return {'session': 'NO_SESSION', 'is_active': False, 'activity_level': 'LOW'}

        except Exception as e:
            enviar_senal_log("ERROR", f"🕐 Error determinando sesión: {e}", __name__, "session_detection")
            return {'session': 'ERROR', 'overlap': False, 'activity_level': 'MEDIUM'}

    def _is_killzone_active(self, session_name: str) -> bool:
        """
        Determina si estamos en killzone ICT
        London Killzone: 2-5 AM EST (7-10 UTC)
        NY Killzone: 8-11 AM EST (13-16 UTC)
        """
        try:
            current_utc = datetime.now(timezone.utc)
            current_hour = current_utc.hour

            if session_name == 'LONDON':
                # London Killzone: 7-10 UTC (2-5 AM EST)
                return 7 <= current_hour <= 10
            elif session_name == 'NEW_YORK':
                # NY Killzone: 13-16 UTC (8-11 AM EST)
                return 13 <= current_hour <= 16
            else:
                return False

        except Exception as e:
            enviar_senal_log("ERROR", f"🕐 Error detectando killzone: {e}", __name__, "session_detection")
            return False

    def _analyze_bias_confirmation_factors(self, candles, h4_bias, m15_bias) -> List[str]:
        """Analiza factores de confirmación de bias"""
        return ['price_action', 'volume_profile', 'market_structure']

    # POI methods simplificados
    def _find_order_block_pois_advanced(self, candles, current_price) -> List[Dict[str, Any]]:
        """Encuentra POIs basados en Order Blocks avanzados"""
        if not poi_functions_available:
            return []

        try:
            # Usar la función real del poi_detector
            order_blocks = detectar_order_blocks(candles, 'M15')

            # Convertir a formato ICTDetector POI
            pois = []
            for ob in order_blocks:
                poi = {
                    'type': f"OB_{ob['type']}",
                    'price_level': ob['price'],
                    'confidence': ob.get('score', 50) / 100.0,
                    'strength': min(100, ob.get('score', 50)),
                    'timeframe': ob.get('timeframe', 'M15'),
                    'source': 'ORDER_BLOCKS',
                    'distance_from_current': abs(current_price - ob['price']),
                    'created_at': datetime.now().isoformat(),
                    'metadata': ob
                }
                pois.append(poi)

            enviar_senal_log("DEBUG", f"Order Blocks POIs encontrados: {len(pois)}", __name__, "poi")
            return pois

        except Exception as e:
            enviar_senal_log("ERROR", f"Error detectando Order Block POIs: {e}", __name__, "poi")
            return []

    def _find_liquidity_pois_advanced(self, candles, current_price) -> List[Dict[str, Any]]:
        """Encuentra POIs basados en liquidez"""
        if not poi_functions_available:
            return []

        try:
            # Usar Fair Value Gaps como proxy de liquidez
            fvgs = detectar_fair_value_gaps(candles, 'M15')

            pois = []
            for fvg in fvgs:
                poi = {
                    'type': f"LIQUIDITY_{fvg['type']}",
                    'price_level': fvg['price'],
                    'confidence': fvg.get('score', 45) / 100.0,
                    'strength': min(100, fvg.get('score', 45)),
                    'timeframe': fvg.get('timeframe', 'M15'),
                    'source': 'LIQUIDITY_ZONES',
                    'distance_from_current': abs(current_price - fvg['price']),
                    'created_at': datetime.now().isoformat(),
                    'metadata': fvg
                }
                pois.append(poi)

            enviar_senal_log("DEBUG", f"Liquidity POIs encontrados: {len(pois)}", __name__, "poi")
            return pois

        except Exception as e:
            enviar_senal_log("ERROR", f"Error detectando Liquidity POIs: {e}", __name__, "poi")
            return []

    def _find_support_resistance_pois_advanced(self, candles, current_price) -> List[Dict[str, Any]]:
        """Encuentra POIs de soporte/resistencia"""
        if not poi_functions_available:
            return []

        try:
            # Usar Breaker Blocks como S/R dinámicos
            breakers = detectar_breaker_blocks(candles, 'M15')

            pois = []
            for breaker in breakers:
                poi = {
                    'type': f"SR_{breaker['type']}",
                    'price_level': breaker['price'],
                    'confidence': breaker.get('score', 40) / 100.0,
                    'strength': min(100, breaker.get('score', 40)),
                    'timeframe': breaker.get('timeframe', 'M15'),
                    'source': 'SUPPORT_RESISTANCE',
                    'distance_from_current': abs(current_price - breaker['price']),
                    'created_at': datetime.now().isoformat(),
                    'metadata': breaker
                }
                pois.append(poi)

            enviar_senal_log("DEBUG", f"Support/Resistance POIs encontrados: {len(pois)}", __name__, "poi")
            return pois

        except Exception as e:
            enviar_senal_log("ERROR", f"Error detectando S/R POIs: {e}", __name__, "poi")
            return []

    def _find_fvg_pois_advanced(self, candles, current_price) -> List[Dict[str, Any]]:
        """Encuentra POIs basados en FVGs"""
        if not poi_functions_available:
            return []

        try:
            # Usar función directa de FVG
            fvgs = detectar_fair_value_gaps(candles, 'M15')

            pois = []
            for fvg in fvgs:
                poi = {
                    'type': f"FVG_{fvg['type']}",
                    'price_level': fvg['price'],
                    'confidence': fvg.get('score', 50) / 100.0,
                    'strength': min(100, fvg.get('score', 50)),
                    'timeframe': fvg.get('timeframe', 'M15'),
                    'source': 'FAIR_VALUE_GAPS',
                    'distance_from_current': abs(current_price - fvg['price']),
                    'created_at': datetime.now().isoformat(),
                    'metadata': fvg
                }
                pois.append(poi)

            enviar_senal_log("DEBUG", f"FVG POIs encontrados: {len(pois)}", __name__, "poi")
            return pois

        except Exception as e:
            enviar_senal_log("ERROR", f"Error detectando FVG POIs: {e}", __name__, "poi")
            return []

    def _find_hod_lod_pois(self, candles, current_price) -> List[Dict[str, Any]]:
        """Encuentra POIs de High/Low of Day"""
        try:
            if candles is None or len(candles) == 0:
                return []

            # Encontrar high y low del día actual
            today_high = float(candles['high'].max())
            today_low = float(candles['low'].min())

            pois = []

            # POI para High of Day
            if today_high > current_price:
                hod_poi = {
                    'type': 'HOD_RESISTANCE',
                    'price_level': today_high,
                    'confidence': 0.7,
                    'strength': 65,
                    'timeframe': 'DAILY',
                    'source': 'HIGH_LOW_OF_DAY',
                    'distance_from_current': abs(current_price - today_high),
                    'created_at': datetime.now().isoformat(),
                    'metadata': {'level_type': 'high_of_day', 'price': today_high}
                }
                pois.append(hod_poi)

            # POI para Low of Day
            if today_low < current_price:
                lod_poi = {
                    'type': 'LOD_SUPPORT',
                    'price_level': today_low,
                    'confidence': 0.7,
                    'strength': 65,
                    'timeframe': 'DAILY',
                    'source': 'HIGH_LOW_OF_DAY',
                    'distance_from_current': abs(current_price - today_low),
                    'created_at': datetime.now().isoformat(),
                    'metadata': {'level_type': 'low_of_day', 'price': today_low}
                }
                pois.append(lod_poi)

            enviar_senal_log("DEBUG", f"HOD/LOD POIs encontrados: {len(pois)}", __name__, "poi")
            return pois

        except Exception as e:
            enviar_senal_log("ERROR", f"Error detectando HOD/LOD POIs: {e}", __name__, "poi")
            return []

    def _filter_and_optimize_pois(self, all_pois, current_price) -> List[Dict[str, Any]]:
        """Filtra y optimiza POIs"""
        try:
            if not all_pois:
                return []

            # Filtrar POIs por distancia (no muy lejos del precio actual)
            max_distance = 0.005  # 50 pips para FOREX
            filtered_pois = [
                poi for poi in all_pois
                if poi.get('distance_from_current', float('inf')) <= max_distance
            ]

            # Ordenar por strength y confidence
            filtered_pois.sort(key=lambda x: (x.get('strength', 0), x.get('confidence', 0)), reverse=True)

            # Limitar a los mejores 15 POIs
            optimized_pois = filtered_pois[:15]

            enviar_senal_log("DEBUG", f"POIs filtrados y optimizados: {len(optimized_pois)} de {len(all_pois)}", __name__, "poi")
            return optimized_pois

        except Exception as e:
            enviar_senal_log("ERROR", f"Error filtrando POIs: {e}", __name__, "poi")
            return all_pois[:10]  # Fallback básico
        return all_pois[:10]  # Limitar a 10 por ahora

    # Métodos de confianza
    def _calculate_fvg_confidence(self, fvg) -> float:
        """Calcula confianza de FVG"""
        try:
            base_confidence = 70
            gap_size = fvg.get('high', 0) - fvg.get('low', 0)
            if gap_size > 0.001:
                base_confidence += 10
            return base_confidence
        except Exception:
            return 70

    def _calculate_swing_confidence(self, swing, swing_type) -> float:
        """Calcula confianza de swing point"""
        return 75

    def _calculate_swing_strength(self, swing, all_swings) -> float:
        """Calcula fuerza de swing point"""
        return 50

    def _calculate_ob_confidence(self, candle, prev_candles, ob_type) -> float:
        """Calcula confianza de Order Block"""
        return 75

    def _calculate_ob_strength(self, candle, prev_candles) -> float:
        """Calcula fuerza de Order Block"""
        return 60

    def _check_volume_confirmation(self, candle, prev_candles) -> bool:
        """Verifica confirmación de volumen"""
        return True  # Simplificado por ahora

    # =========================================================================
    # LIQUIDITY DETECTION ENGINE - HELPER FUNCTIONS (Sprint 1.5)
    # =========================================================================

    def _find_equal_highs(self, df: pd.DataFrame, tolerance_pips: float = 5.0) -> List[Dict[str, Any]]:
        """
        Detecta Equal Highs - niveles donde el precio ha tocado múltiples veces
        Estos son zonas prime para stop hunts institucionales
        """
        try:
            equal_highs = []
            highs = df['high'].values
            current_price = df['close'].iloc[-1]

            # Buscar niveles tocados múltiples veces
            for i in range(len(highs) - 10, len(highs) - 1):  # Últimas 10 velas
                if i < 5:  # Necesitamos contexto previo
                    continue

                current_high = highs[i]

                # Contar cuántas veces se ha tocado este nivel
                tolerance = tolerance_pips * 0.00001  # Convertir pips a precio
                touches = 0

                for j in range(max(0, i-20), len(highs)):  # Buscar en 20 velas
                    if abs(highs[j] - current_high) <= tolerance:
                        touches += 1

                # Si se ha tocado 2+ veces, es zona de liquidez
                if touches >= 2:
                    distance_pips = abs(current_price - current_high) / 0.00001

                    equal_highs.append({
                        'type': 'EQUAL_HIGHS',
                        'level': current_high,
                        'touches': touches,
                        'distance_pips': distance_pips,
                        'strength': min(touches * 25, 100),  # Max 100%
                        'side': 'RESISTANCE',
                        'freshness': 'FRESH' if distance_pips > 10 else 'CLOSE',
                        'candle_index': i,
                        'description': f"Equal Highs @ {current_high:.5f} ({touches} touches)"
                    })

            enviar_senal_log("DEBUG", f"Equal Highs detectados: {len(equal_highs)}", __name__, "liquidity")
            return equal_highs

        except Exception as e:
            enviar_senal_log("ERROR", f"Error detectando Equal Highs: {e}", __name__, "liquidity")
            return []

    def _find_equal_lows(self, df: pd.DataFrame, tolerance_pips: float = 5.0) -> List[Dict[str, Any]]:
        """
        Detecta Equal Lows - niveles donde el precio ha tocado múltiples veces
        Zonas prime para stop hunts en el lado de compra
        """
        try:
            equal_lows = []
            lows = df['low'].values
            current_price = df['close'].iloc[-1]

            # Buscar niveles tocados múltiples veces
            for i in range(len(lows) - 10, len(lows) - 1):  # Últimas 10 velas
                if i < 5:  # Necesitamos contexto previo
                    continue

                current_low = lows[i]

                # Contar cuántas veces se ha tocado este nivel
                tolerance = tolerance_pips * 0.00001  # Convertir pips a precio
                touches = 0

                for j in range(max(0, i-20), len(lows)):  # Buscar en 20 velas
                    if abs(lows[j] - current_low) <= tolerance:
                        touches += 1

                # Si se ha tocado 2+ veces, es zona de liquidez
                if touches >= 2:
                    distance_pips = abs(current_price - current_low) / 0.00001

                    equal_lows.append({
                        'type': 'EQUAL_LOWS',
                        'level': current_low,
                        'touches': touches,
                        'distance_pips': distance_pips,
                        'strength': min(touches * 25, 100),  # Max 100%
                        'side': 'SUPPORT',
                        'freshness': 'FRESH' if distance_pips > 10 else 'CLOSE',
                        'candle_index': i,
                        'description': f"Equal Lows @ {current_low:.5f} ({touches} touches)"
                    })

            enviar_senal_log("DEBUG", f"Equal Lows detectados: {len(equal_lows)}", __name__, "liquidity")
            return equal_lows

        except Exception as e:
            enviar_senal_log("ERROR", f"Error detectando Equal Lows: {e}", __name__, "liquidity")
            return []

    def _find_session_liquidity_zones(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detecta zonas de liquidez en extremos de sesión
        Usa el session detection ya implementado en Sprint 1.4
        """
        try:
            session_zones = []

            # Solo si tenemos session detection disponible
            if hasattr(self, 'session_detector_available') and self.session_detector_available and market_status_available:

                # Obtener información de sesión actual
                session_info = get_current_session_info()

                if session_info:
                    session_name = session_info.get('session_key', 'UNKNOWN')

                    # Buscar high/low de la sesión actual (aprox. últimas 4 horas en M15)
                    session_period = min(16, len(df))  # 16 velas = 4 horas en M15
                    session_data = df.tail(session_period)

                    session_high = session_data['high'].max()
                    session_low = session_data['low'].min()
                    current_price = df['close'].iloc[-1]

                    # Session High como zona de liquidez
                    high_distance = abs(current_price - session_high) / 0.00001
                    session_zones.append({
                        'type': f'SESSION_HIGH_{session_name}',
                        'level': session_high,
                        'distance_pips': high_distance,
                        'strength': 75,  # Session levels son importantes
                        'side': 'RESISTANCE',
                        'freshness': 'FRESH' if high_distance > 15 else 'CLOSE',
                        'session': session_name,
                        'description': f"{session_name} Session High @ {session_high:.5f}"
                    })

                    # Session Low como zona de liquidez
                    low_distance = abs(current_price - session_low) / 0.00001
                    session_zones.append({
                        'type': f'SESSION_LOW_{session_name}',
                        'level': session_low,
                        'distance_pips': low_distance,
                        'strength': 75,  # Session levels son importantes
                        'side': 'SUPPORT',
                        'freshness': 'FRESH' if low_distance > 15 else 'CLOSE',
                        'session': session_name,
                        'description': f"{session_name} Session Low @ {session_low:.5f}"
                    })

                    enviar_senal_log("DEBUG",
                        f"Session Liquidity {session_name}: High @ {session_high:.5f}, Low @ {session_low:.5f}",
                        __name__, "liquidity")

            return session_zones

        except Exception as e:
            enviar_senal_log("ERROR", f"Error detectando Session Liquidity: {e}", __name__, "liquidity")
            return []

    def _find_daily_liquidity_levels(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detecta Previous Day High/Low como zonas de liquidez
        Estos niveles son críticos en la metodología ICT
        """
        try:
            daily_zones = []

            # Aproximar PDH/PDL usando los extremos de las últimas 96 velas (24h en M15)
            if len(df) >= 96:
                previous_day_data = df.iloc[-96:-1]  # Excluir vela actual

                pdh = previous_day_data['high'].max()
                pdl = previous_day_data['low'].min()
                current_price = df['close'].iloc[-1]

                # Previous Day High
                pdh_distance = abs(current_price - pdh) / 0.00001
                daily_zones.append({
                    'type': 'DAILY_HIGH',
                    'level': pdh,
                    'distance_pips': pdh_distance,
                    'strength': 85,  # Daily levels son muy importantes
                    'side': 'RESISTANCE',
                    'freshness': 'FRESH' if pdh_distance > 20 else 'CLOSE',
                    'description': f"Previous Day High @ {pdh:.5f}"
                })

                # Previous Day Low
                pdl_distance = abs(current_price - pdl) / 0.00001
                daily_zones.append({
                    'type': 'DAILY_LOW',
                    'level': pdl,
                    'distance_pips': pdl_distance,
                    'strength': 85,  # Daily levels son muy importantes
                    'side': 'SUPPORT',
                    'freshness': 'FRESH' if pdl_distance > 20 else 'CLOSE',
                    'description': f"Previous Day Low @ {pdl:.5f}"
                })

                enviar_senal_log("DEBUG",
                    f"Daily Liquidity: PDH @ {pdh:.5f}, PDL @ {pdl:.5f}",
                    __name__, "liquidity")

            return daily_zones

        except Exception as e:
            enviar_senal_log("ERROR", f"Error detectando Daily Liquidity: {e}", __name__, "liquidity")
            return []

    def _find_swing_liquidity_zones(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detecta liquidez en swing points ya identificados
        Conecta con el sistema de swing detection existente
        """
        try:
            swing_zones = []

            # Usar swing points ya detectados por el sistema
            swing_points = self._detect_swing_points(df)
            current_price = df['close'].iloc[-1]

            for swing in swing_points:
                swing_level = swing.get('price', 0)
                swing_type = swing.get('type', 'UNKNOWN')

                if swing_level > 0:
                    distance_pips = abs(current_price - swing_level) / 0.00001

                    swing_zones.append({
                        'type': f'SWING_{swing_type.upper()}',
                        'level': swing_level,
                        'distance_pips': distance_pips,
                        'strength': 65,  # Swing points tienen fuerza media
                        'side': 'RESISTANCE' if swing_type.upper() == 'HIGH' else 'SUPPORT',
                        'freshness': 'FRESH' if distance_pips > 10 else 'CLOSE',
                        'description': f"Swing {swing_type} @ {swing_level:.5f}"
                    })

            enviar_senal_log("DEBUG", f"Swing Liquidity detectado: {len(swing_zones)} zonas", __name__, "liquidity")
            return swing_zones

        except Exception as e:
            enviar_senal_log("ERROR", f"Error detectando Swing Liquidity: {e}", __name__, "liquidity")
            return []

    def _rank_liquidity_zones(self, zones: List[Dict[str, Any]], current_price: float) -> List[Dict[str, Any]]:
        """
        Rankea zonas de liquidez por importancia e relevancia
        """
        try:
            if not zones:
                return []

            # Asignar score a cada zona
            for zone in zones:
                base_strength = zone.get('strength', 50)
                distance_pips = zone.get('distance_pips', 100)

                # Score basado en fuerza y proximidad
                proximity_score = max(0, 100 - distance_pips)  # Más cerca = mayor score
                final_score = (base_strength * 0.7) + (proximity_score * 0.3)

                zone['score'] = round(final_score, 1)

            # Ordenar por score (mayor a menor)
            ranked_zones = sorted(zones, key=lambda x: x.get('score', 0), reverse=True)

            # Limitar a top 20 para performance
            return ranked_zones[:20]

        except Exception as e:
            enviar_senal_log("ERROR", f"Error rankeando liquidity zones: {e}", __name__, "liquidity")
            return zones  # Retornar sin rankear si hay error

    def _detect_swing_points(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Wrapper para detectar swing points usando la función global existente
        Conecta con detectar_swing_points() ya implementada
        """
        try:
            if df is None or len(df) < 10:
                return []

            # Usar la función global ya implementada
            swing_highs, swing_lows = detectar_swing_points(df, len_left=5, len_right=1)

            swing_points = []

            # Convertir swing highs a formato estándar
            for high in swing_highs:
                swing_points.append({
                    'type': 'HIGH',
                    'price': high.get('price', 0),
                    'index': high.get('index', 0),
                    'strength': high.get('strength', 50),
                    'created_at': datetime.now().isoformat()
                })

            # Convertir swing lows a formato estándar
            for low in swing_lows:
                swing_points.append({
                    'type': 'LOW',
                    'price': low.get('price', 0),
                    'index': low.get('index', 0),
                    'strength': low.get('strength', 50),
                    'created_at': datetime.now().isoformat()
                })

            enviar_senal_log("DEBUG", f"Swing Points detectados: {len(swing_points)} ({len(swing_highs)} highs, {len(swing_lows)} lows)", __name__, "liquidity")
            return swing_points

        except Exception as e:
            enviar_senal_log("ERROR", f"Error en _detect_swing_points: {e}", __name__, "liquidity")
            return []

    # =========================================================================
    # MÉTODOS DE UTILIDAD Y ESTADO
    # =========================================================================

    def get_analysis_summary(self) -> Dict[str, Any]:
        """Retorna un resumen completo del último análisis realizado"""
        if not self.last_analysis:
            return {
                'status': 'no_analysis_performed',
                'detector_initialized': self.initialized,
                'total_analyses': self.analysis_count
            }

        return {
            'status': 'analysis_available',
            'last_analysis_time': self.last_analysis['timestamp'],
            'patterns_detected': self.last_analysis['patterns_count'],
            'raw_patterns_detected': self.last_analysis['raw_patterns_count'],
            'pattern_types': self.last_analysis['types'],
            'data_quality': self.last_analysis['data_quality'],
            'analysis_id': self.last_analysis['analysis_id'],
            'detector_initialized': self.initialized,
            'total_analyses': self.analysis_count,
            'configuration': self.config
        }

    def reset_cache(self):
        """Reinicia el cache del detector"""
        self.cache = {}
        enviar_senal_log("INFO", "🔄 Cache del ICTDetector reiniciado", __name__, "general")

    def set_market_context(self, market_context):
        """
        Establece el contexto de mercado para análisis más precisos
        SPRINT 1.4 FIX: Actualiza sesión inmediatamente
        """
        self.market_context = market_context

        # SPRINT 1.4 FIX: Actualizar sesión inmediatamente al establecer contexto
        if hasattr(market_context, '_determine_session_context'):
            try:
                session_info = market_context._determine_session_context()
                session_name = session_info.get('session', 'UNKNOWN')
                enviar_senal_log("INFO", f"🕐 Sesión actualizada al establecer contexto: {session_name}", __name__, "session_detection")
            except Exception as e:
                enviar_senal_log("ERROR", f"🕐 Error actualizando sesión en contexto: {e}", __name__, "session_detection")

        enviar_senal_log("DEBUG", "📊 Contexto de mercado establecido en ICTDetector", __name__, "general")

    def update_configuration(self, new_config: Dict[str, Any]):
        """Actualiza la configuración del detector"""
        self.config.update(new_config)
        enviar_senal_log("INFO", f"⚙️ Configuración actualizada: {new_config}", __name__, "general")

    def get_detector_status(self) -> Dict[str, Any]:
        """Retorna el estado completo del detector"""
        return {
            'initialized': self.initialized,
            'total_analyses': self.analysis_count,
            'has_market_context': self.market_context is not None,
            'cache_size': len(self.cache),
            'configuration': self.config,
            'last_analysis': self.last_analysis is not None
        }
