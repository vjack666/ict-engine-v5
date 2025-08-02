#!/usr/bin/env python3
"""
ICT Types - Estructuras de Datos Fundamentales
==============================================

Definición de tipos, enums y dataclasses para el sistema ICT profesional.
Contiene las estructuras de datos que utiliza todo el ecosistema de análisis.

Autor: Sistema Automático  
Fecha: 25 de Julio, 2025
Versión: ICT Professional v1.0
"""

from enum import Enum
from typing import Dict, List, Tuple, Optional
# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log

from dataclasses import dataclass
from datetime import time


class ICTPattern(Enum):
    """Patrones ICT reconocibles por el sistema inteligente"""
    JUDAS_SWING = "judas_swing"
    OPTIMAL_TRADE_ENTRY = "optimal_trade_entry"
    LIQUIDITY_GRAB = "liquidity_grab"
    SILVER_BULLET = "silver_bullet"
    POWER_OF_THREE = "power_of_three"
    INSTITUTIONAL_ORDER_FLOW = "institutional_order_flow"
    MORNING_REVERSAL = "morning_reversal"
    FAIR_VALUE_GAP = "fair_value_gap"
    ORDER_BLOCK_RETEST = "order_block_retest"
    BREAK_OF_STRUCTURE = "break_of_structure"


class MarketPhase(Enum):
    """Fases del mercado según metodología ICT"""
    ACCUMULATION = "accumulation"      # Smart Money acumulando posiciones
    MANIPULATION = "manipulation"     # Movimientos falsos para generar liquidez
    DISTRIBUTION = "distribution"     # Smart Money distribuyendo/saliendo
    REBALANCE = "rebalance"           # Corrección técnica/consolidación


class SessionType(Enum):
    """Sesiones de trading con características específicas"""
    ASIAN = "asian"                   # 21:00-08:00 GMT - Baja volatilidad, rangos
    LONDON = "london"                 # 08:00-16:00 GMT - Establecimiento dirección
    NEW_YORK = "new_york"            # 13:00-21:00 GMT - Momentum y continuación
    LONDON_CLOSE = "london_close"    # 15:30-16:30 GMT - Movimientos finales
    OVERLAP = "overlap"              # 13:00-16:00 GMT - Máxima liquidez


class SignalStrength(Enum):
    """Niveles de fortaleza de señales ICT"""
    CRITICAL = "critical"     # 90-100% - Señal extremadamente fuerte
    HIGH = "high"            # 75-89% - Señal fuerte, alta probabilidad
    MEDIUM = "medium"        # 60-74% - Señal moderada, buena probabilidad
    LOW = "low"             # 40-59% - Señal débil, probabilidad baja
    NOISE = "noise"         # 0-39% - Ruido de mercado, ignorar


class TradingDirection(Enum):
    """Direcciones de trading"""
    BUY = "BUY"
    SELL = "SELL"
    NEUTRAL = "NEUTRAL"
    WAIT = "WAIT"


@dataclass
class ICTSignal:
    """
    Señal ICT completa con toda la información necesaria para trading.
    Contiene tanto datos técnicos como narrativa interpretativa.
    """
    # 🎯 Información del patrón
    pattern: ICTPattern
    strength: float                    # 0-100, fortaleza del patrón
    direction: TradingDirection        # Dirección recomendada
    probability: float                 # 0-100, probabilidad de éxito
    confidence: SignalStrength         # Nivel de confianza categórico
    
    # 📊 Datos técnicos de trading
    entry_zone: Tuple[float, float]    # (precio_min, precio_max) para entrada
    target_zones: List[float]          # Lista de objetivos de beneficio
    stop_loss: float                   # Nivel de stop loss
    risk_reward: float                 # Ratio riesgo/beneficio
    
    # 📖 Información narrativa
    narrative: str                     # Historia completa del patrón
    context: str                       # Contexto de mercado actual
    action_plan: List[str]            # Pasos específicos de ejecución
    
    # ⏰ Información temporal
    session_context: SessionType      # Sesión donde ocurre el patrón
    optimal_timing: str               # Ventana temporal óptima
    time_sensitivity: str             # Qué tan sensible al tiempo es
    
    # ⚠️ Gestión de riesgo
    risk_factors: List[str]           # Factores de riesgo específicos
    invalidation_criteria: str       # Qué invalida el patrón
    position_sizing: str             # Recomendación de tamaño de posición


@dataclass
class MarketStructure:
    """
    Estructura del mercado en un momento dado.
    Representa el estado técnico completo del mercado.
    """
    # 📈 Tendencia y bias
    primary_trend: TradingDirection   # Tendencia principal
    secondary_trend: TradingDirection # Tendencia secundaria/pullback
    market_bias: TradingDirection     # Bias operativo actual
    structure_quality: SignalStrength # Qué tan clara está la estructura
    
    # 🎯 Niveles clave
    key_levels: List[Dict]            # Niveles importantes (SR, OB, FVG)
    support_levels: List[float]       # Niveles de soporte identificados
    resistance_levels: List[float]    # Niveles de resistencia identificados
    
    # 📊 Información de contexto
    current_phase: MarketPhase        # Fase actual del mercado
    volatility_regime: str           # "LOW", "NORMAL", "HIGH"
    liquidity_condition: str         # "THIN", "NORMAL", "ABUNDANT"


@dataclass
class SessionCharacteristics:
    """
    Características específicas de cada sesión de trading.
    Define qué esperar y cómo adaptar la estrategia.
    """
    session: SessionType
    active_hours: Tuple[time, time]   # Horario activo (inicio, fin)
    typical_range: Tuple[int, int]    # Rango típico en pips (min, max)
    volatility_profile: str          # "LOW", "MEDIUM", "HIGH"
    
    # 🎯 Patrones más comunes en esta sesión
    common_patterns: List[ICTPattern]
    avoid_patterns: List[ICTPattern]   # Patrones menos fiables en esta sesión
    
    # 💡 Estrategias recomendadas
    recommended_approach: str         # Descripción de enfoque óptimo
    key_times: List[str]             # Momentos clave dentro de la sesión
    risk_considerations: List[str]    # Consideraciones especiales de riesgo


@dataclass
class ICTAnalysisResult:
    """
    Resultado completo de un análisis ICT.
    Combina señales, estructura y recomendaciones.
    """
    # 🎯 Señal principal
    primary_signal: Optional[ICTSignal]
    secondary_signals: List[ICTSignal]
    
    # 📊 Estado del mercado
    market_structure: MarketStructure
    session_info: SessionCharacteristics
    
    # 🧠 Análisis inteligente
    overall_assessment: str           # Evaluación general del mercado
    recommended_action: str          # Acción recomendada inmediata
    market_outlook: str              # Perspectiva a corto/medio plazo
    
    # ⚠️ Alertas y advertencias
    warnings: List[str]              # Advertencias importantes
    opportunities: List[str]         # Oportunidades identificadas
    
    # 📈 Métricas de rendimiento
    analysis_confidence: float       # 0-100, confianza en el análisis
    prediction_horizon: str         # Horizonte temporal de validez
    last_update: str                # Timestamp del análisis


# 🎨 MAPAS DE CONFIGURACIÓN

# Emojis para cada patrón ICT
PATTERN_EMOJIS = {
    ICTPattern.SILVER_BULLET: "🥈",
    ICTPattern.JUDAS_SWING: "🎭", 
    ICTPattern.OPTIMAL_TRADE_ENTRY: "🎯",
    ICTPattern.LIQUIDITY_GRAB: "🌊",
    ICTPattern.POWER_OF_THREE: "⚡",
    ICTPattern.INSTITUTIONAL_ORDER_FLOW: "🏛️",
    ICTPattern.MORNING_REVERSAL: "🌅",
    ICTPattern.FAIR_VALUE_GAP: "🕳️",
    ICTPattern.ORDER_BLOCK_RETEST: "🧱",
    ICTPattern.BREAK_OF_STRUCTURE: "💥"
}

# Colores para direcciones
DIRECTION_COLORS = {
    TradingDirection.BUY: "green",
    TradingDirection.SELL: "red", 
    TradingDirection.NEUTRAL: "yellow",
    TradingDirection.WAIT: "dim white"
}

# Configuración de sesiones
SESSION_CONFIG = {
    SessionType.ASIAN: SessionCharacteristics(
        session=SessionType.ASIAN,
        active_hours=(time(21, 0), time(8, 0)),
        typical_range=(20, 60),
        volatility_profile="LOW",
        common_patterns=[ICTPattern.FAIR_VALUE_GAP, ICTPattern.ORDER_BLOCK_RETEST],
        avoid_patterns=[ICTPattern.SILVER_BULLET, ICTPattern.MORNING_REVERSAL],
        recommended_approach="Operación en rangos, evitar breakouts",
        key_times=["02:33-03:00 (Asian Kill Zone)", "06:00-07:00 (Pre-London)"],
        risk_considerations=["Baja liquidez", "Spreads amplios", "Movimientos erráticos"]
    ),
    
    SessionType.LONDON: SessionCharacteristics(
        session=SessionType.LONDON,
        active_hours=(time(8, 0), time(16, 0)),
        typical_range=(60, 120),
        volatility_profile="HIGH",
        common_patterns=[ICTPattern.SILVER_BULLET, ICTPattern.JUDAS_SWING, ICTPattern.LIQUIDITY_GRAB],
        avoid_patterns=[ICTPattern.FAIR_VALUE_GAP],
        recommended_approach="Seguir direccionalidad, buscar momentum",
        key_times=["08:30-09:00 (London Open)", "10:00-11:00 (Silver Bullet)", "15:15-15:45 (London Close)"],
        risk_considerations=["Alta volatilidad inicial", "Noticias económicas", "Overlaps con NY"]
    ),
    
    SessionType.NEW_YORK: SessionCharacteristics(
        session=SessionType.NEW_YORK,
        active_hours=(time(13, 0), time(21, 0)),
        typical_range=(80, 150),
        volatility_profile="HIGH",
        common_patterns=[ICTPattern.POWER_OF_THREE, ICTPattern.INSTITUTIONAL_ORDER_FLOW, ICTPattern.BREAK_OF_STRUCTURE],
        avoid_patterns=[ICTPattern.MORNING_REVERSAL],
        recommended_approach="Continuación de trends, momentum trading",
        key_times=["13:30-14:00 (NY Open)", "15:00-16:00 (Overlap)", "19:00-20:00 (Late Session)"],
        risk_considerations=["Máxima liquidez", "Noticias US", "Reversiones bruscas"]
    )
}


def get_pattern_description(pattern: ICTPattern) -> str:
    """Obtiene descripción detallada de un patrón ICT"""
    descriptions = {
        ICTPattern.SILVER_BULLET: "Movimiento direccional durante 10:00-11:00 GMT con alta probabilidad",
        ICTPattern.JUDAS_SWING: "Falsa ruptura seguida de reversión hacia dirección real",
        ICTPattern.OPTIMAL_TRADE_ENTRY: "Retroceso a zona óptima (61.8%-78.6%) para continuación",
        ICTPattern.LIQUIDITY_GRAB: "Barrido rápido de liquidez seguido de reversión inmediata",
        ICTPattern.POWER_OF_THREE: "Secuencia acumulación-manipulación-distribución",
        ICTPattern.INSTITUTIONAL_ORDER_FLOW: "Flujo de órdenes institucionales identificable",
        ICTPattern.MORNING_REVERSAL: "Reversión matutina después de gap o movimiento overnight",
        ICTPattern.FAIR_VALUE_GAP: "Zona de ineficiencia de precio que actúa como imán",
        ICTPattern.ORDER_BLOCK_RETEST: "Retesteo de zona donde se originaron órdenes institucionales",
        ICTPattern.BREAK_OF_STRUCTURE: "Ruptura confirmada de estructura para nueva dirección"
    }
    return descriptions.get(pattern, "Patrón ICT no definido")


def get_strength_color(strength: float) -> str:
    """Obtiene color apropiado según la fortaleza de la señal"""
    if strength >= 85:
        return "bold green"
    elif strength >= 70:
        return "green"
    elif strength >= 55:
        return "yellow"
    elif strength >= 40:
        return "orange"
    else:
        return "red"


def get_risk_reward_assessment(rr_ratio: float) -> str:
    """Evalúa el ratio riesgo/beneficio"""
    if rr_ratio >= 3.0:
        return "🌟 EXCELENTE"
    elif rr_ratio >= 2.0:
        return "✅ BUENO"
    elif rr_ratio >= 1.5:
        return "⚖️ ACEPTABLE"
    elif rr_ratio >= 1.0:
        return "⚠️ MARGINAL"
    else:
        return "🚫 POBRE"
