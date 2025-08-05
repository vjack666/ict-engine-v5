#!/usr/bin/env python3
"""
🧠 ANALYSIS COMMAND CENTER - Centro de Mando de Análisis
ARQUITECTURA: Punto de entrada unificado para todo el sistema de análisis
PROTOCOLO: "Caja Negra" - Orquestación completa, logging exhaustivo
"""

from typing import Optional, List

# 🎯 EXPORTACIONES PRINCIPALES DEL ACC
from .acc_orchestrator import AnalysisOrchestrator
from .acc_flow_controller import AccFlowController, FlowPriority, CacheStrategy  # ✅ REACTIVADO
from .acc_data_models import (
    AnalysisInput,
    AnalysisOutput,
    AnalysisStatus,
    ComponentResult,
    ComponentType,
    MarketStructureData,
    POIData,
    ConfidenceData,
    VeredictoData,
    TCTData
)

# 🎯 TCT PIPELINE INTEGRADO
from .tct_pipeline import (
    TCTInterface,
    TCTMeasurementEngine,
    TCTMetrics,
    TCTAggregator,
    AggregatedTCTMetrics,
    TCTFormatter
)

# 📊 FUNCIONES DE CONVENIENCIA PARA INTEGRACIÓN DASHBOARD

def create_analysis_orchestrator(**kwargs) -> AnalysisOrchestrator:
    """
    🎯 Factory function para crear orquestador de análisis

    Args:
        **kwargs: Parámetros de configuración

    Returns:
        AnalysisOrchestrator configurado
    """
    return AnalysisOrchestrator(**kwargs)

def run_quick_analysis(symbol: str, timeframe: str = "M15") -> AnalysisOutput:
    """
    ⚡ Análisis rápido para dashboard

    Args:
        symbol: Símbolo a analizar
        timeframe: Timeframe (default M15)

    Returns:
        AnalysisOutput con resultado completo
    """
    orchestrator = AnalysisOrchestrator()
    return orchestrator.run_focused_analysis(
        symbol=symbol,
        timeframe=timeframe,
        focus_areas=["ICT", "POI", "CONFIDENCE"]
    )

def run_comprehensive_analysis(symbol: str,
                             timeframes: Optional[List[str]] = None) -> AnalysisOutput:
    """
    🎼 Análisis completo para dashboard

    Args:
        symbol: Símbolo a analizar
        timeframes: Lista de timeframes (default ["M1", "M5", "M15"])

    Returns:
        AnalysisOutput con resultado completo
    """
    if timeframes is None:
        timeframes = ["M1", "M5", "M15"]

    orchestrator = AnalysisOrchestrator()
    return orchestrator.run_full_analysis_cycle(symbol, timeframes)

# 🎯 EXPORTACIONES PARA EL DASHBOARD
__all__ = [
    # 🎯 COMPONENTES PRINCIPALES
    'AnalysisOrchestrator',
    'AccFlowController',

    # 📊 MODELOS DE DATOS
    'AnalysisInput',
    'AnalysisOutput',
    'AnalysisStatus',
    'ComponentResult',
    'ComponentType',
    'MarketStructureData',
    'POIData',
    'ConfidenceData',
    'VeredictoData',
    'TCTData',

    # 🎛️ CONTROL DE FLUJO
    'FlowPriority',
    'CacheStrategy',

    # 🎯 TCT PIPELINE
    'TCTInterface',
    'TCTMeasurementEngine',
    'TCTMetrics',
    'TCTAggregator',
    'AggregatedTCTMetrics',
    'TCTFormatter',

    # 📊 FUNCIONES DE CONVENIENCIA
    'create_analysis_orchestrator',
    'run_quick_analysis',
    'run_comprehensive_analysis'
]

# 📊 METADATA DEL ACC
__version__ = "1.0.0"
__description__ = "Centro de Mando de Análisis para ICT Engine v3.4"
__architecture__ = "ORCHESTRATED_SPECIALISTS"
__protocol__ = "CAJA_NEGRA"

# 📝 MÓDULO CARGADO - Analysis Command Center
# Sistema de orquestación activado
