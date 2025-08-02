#!/usr/bin/env python3
"""
📊 ACC DATA MODELS - Modelos de datos unificados para el Centro de Mando
ARQUITECTURA: Dataclasses para estandarizar flujo de datos entre especialistas
PROTOCOLO: "Caja Negra" - Estructuras robustas, logging exhaustivo
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum

# 🔌 IMPORTS DEL ICT ENGINE
from sistema.logging_interface import enviar_senal_log

class AnalysisStatus(Enum):
    """Estados posibles del análisis"""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"

class ComponentType(Enum):
    """Tipos de componentes en el ACC"""
    DATA_MANAGER = "DATA_MANAGER"
    ICT_DETECTOR = "ICT_DETECTOR"
    POI_DETECTOR = "POI_DETECTOR"
    CONFIDENCE_ENGINE = "CONFIDENCE_ENGINE"
    VEREDICTO_ENGINE = "VEREDICTO_ENGINE"
    TCT_PIPELINE = "TCT_PIPELINE"

@dataclass
class AnalysisInput:
    """
    📥 Estructura de entrada unificada para el ACC
    Estandariza todos los parámetros de análisis
    """
    
    # 🎯 PARÁMETROS BÁSICOS
    symbol: str
    timeframes: List[str]
    analysis_id: str = field(default_factory=lambda: f"ACC_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # 🔧 CONFIGURACIÓN DE ANÁLISIS
    analysis_type: str = "FULL_CYCLE"  # FULL_CYCLE, FOCUSED, QUICK
    focus_areas: List[str] = field(default_factory=list)  # Para análisis focalizados
    priority: str = "NORMAL"  # HIGH, NORMAL, LOW
    
    # 📊 PARÁMETROS ESPECÍFICOS
    lookback_periods: Optional[Dict[str, int]] = None
    confidence_threshold: float = 0.7
    poi_limit: int = 20
    enable_tct_measurement: bool = True
    
    # 🎛️ CONFIGURACIÓN AVANZADA
    use_cache: bool = True
    max_analysis_time_seconds: int = 30
    error_tolerance: str = "MEDIUM"  # HIGH, MEDIUM, LOW
    
    def __post_init__(self):
        """Validación post-inicialización"""
        
        # 📝 LOG CREACIÓN
        enviar_senal_log(
            level='DEBUG',
            message=f"📥 AnalysisInput created | ID: {self.analysis_id} | "
                   f"Symbol: {self.symbol} | Timeframes: {len(self.timeframes)} | "
                   f"Type: {self.analysis_type}",
            emisor='acc_data_models',
            categoria='acc'
        )
        
        # ✅ VALIDACIONES BÁSICAS
        if not self.symbol:
            raise ValueError("Symbol cannot be empty")
        
        if not self.timeframes:
            raise ValueError("At least one timeframe must be specified")
        
        # 🔧 VALORES POR DEFECTO
        if self.lookback_periods is None:
            self.lookback_periods = {
                "M1": 100,
                "M5": 200,
                "M15": 300,
                "H1": 500,
                "H4": 200,
                "D1": 50
            }

@dataclass
class ComponentResult:
    """
    🎖️ Resultado de un componente especialista individual
    Estructura unificada para respuestas de todos los especialistas
    """
    
    component_type: ComponentType
    component_name: str
    success: bool
    execution_time_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # 📊 DATOS DEL RESULTADO
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # ⚠️ ERROR HANDLING
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    warning_messages: List[str] = field(default_factory=list)
    
    # 🎯 MÉTRICAS ESPECÍFICAS
    confidence_score: Optional[float] = None
    quality_score: Optional[float] = None
    items_processed: int = 0
    
    def __post_init__(self):
        """Log del resultado del componente"""
        
        status = "SUCCESS" if self.success else "FAILED"
        
        enviar_senal_log(
            level='DEBUG' if self.success else 'WARNING',
            message=f"🎖️ ComponentResult | {self.component_type.value} | "
                   f"Status: {status} | Time: {self.execution_time_ms:.2f}ms | "
                   f"Items: {self.items_processed}",
            emisor='acc_data_models',
            categoria='acc'
        )

@dataclass
class MarketStructureData:
    """
    🧠 Datos de estructura de mercado del ICT Engine
    Resultado estandarizado del análisis ICT
    """
    
    symbol: str
    timeframe: str
    timestamp: str
    
    # 📊 ESTRUCTURA PRINCIPAL
    trend: str  # BULLISH, BEARISH, NEUTRAL
    market_structure: str  # BOS, CHoCH, RANGE
    session_type: str  # LONDON, NEW_YORK, ASIAN, OVERLAP
    
    # 🎯 NIVELES CRÍTICOS
    premium_discount_zone: Dict[str, float]
    fair_value_gaps: List[Dict[str, Any]]
    swing_points: Dict[str, List[float]]
    
    # ⚖️ EVALUACIONES
    structure_strength: float  # 0.0 - 1.0
    volatility_index: float
    liquidity_zones: List[Dict[str, Any]]
    
    # 📈 PATRONES DETECTADOS
    patterns_detected: List[str]
    pattern_confluence: int
    
    def get_summary(self) -> Dict[str, Any]:
        """📋 Resumen ejecutivo de la estructura"""
        return {
            "trend": self.trend,
            "structure": self.market_structure,
            "strength": self.structure_strength,
            "patterns": len(self.patterns_detected),
            "fvg_count": len(self.fair_value_gaps),
            "session": self.session_type
        }

@dataclass 
class POIData:
    """
    🎯 Datos de Puntos de Interés del POI System
    Resultado estandarizado de detección de POIs
    """
    
    symbol: str
    timeframe: str
    timestamp: str
    
    # 🎯 POIS DETECTADOS
    pois_list: List[Dict[str, Any]]
    total_pois: int
    
    # 📊 SCORING Y CLASIFICACIÓN
    top_scored_pois: List[Dict[str, Any]]
    average_score: float
    score_distribution: Dict[str, int]
    
    # 🎪 TIPOS DE POI
    poi_types_count: Dict[str, int]
    confluence_zones: List[Dict[str, Any]]
    
    # 🔍 ANÁLISIS AVANZADO
    clustering_analysis: Dict[str, Any]
    temporal_distribution: Dict[str, int]
    
    def get_summary(self) -> Dict[str, Any]:
        """📋 Resumen ejecutivo de POIs"""
        return {
            "total_pois": self.total_pois,
            "avg_score": self.average_score,
            "types": len(self.poi_types_count),
            "clusters": len(self.confluence_zones),
            "top_score": max([poi.get('score', 0) for poi in self.top_scored_pois]) if self.top_scored_pois else 0
        }

@dataclass
class ConfidenceData:
    """
    ⚖️ Datos de confianza del Confidence Engine
    Evaluación consolidada de patrones y confianza
    """
    
    symbol: str
    analysis_timestamp: str
    
    # ⚖️ SCORES DE CONFIANZA
    overall_confidence: float  # 0.0 - 1.0
    pattern_confidence: Dict[str, float]
    poi_confidence: Dict[str, float]
    
    # 📊 EVALUACIONES DETALLADAS
    technical_score: float
    fundamental_score: float
    sentiment_score: float
    
    # 🔍 ANÁLISIS DE RIESGO
    risk_assessment: Dict[str, Any]
    uncertainty_factors: List[str]
    confidence_drivers: List[str]
    
    # 🎯 RECOMENDACIONES
    trading_recommendation: str  # BUY, SELL, HOLD, AVOID
    confidence_level: str  # HIGH, MEDIUM, LOW
    
    def get_summary(self) -> Dict[str, Any]:
        """📋 Resumen ejecutivo de confianza"""
        return {
            "overall": self.overall_confidence,
            "recommendation": self.trading_recommendation,
            "level": self.confidence_level,
            "patterns": len(self.pattern_confidence),
            "risk": self.risk_assessment.get('level', 'UNKNOWN')
        }

@dataclass
class VeredictoData:
    """
    🔮 Datos del veredicto final del Veredicto Engine
    Decisión final y actionable del análisis
    """
    
    symbol: str
    analysis_timestamp: str
    
    # 🔮 VEREDICTO FINAL
    final_decision: str  # BUY, SELL, HOLD, WAIT
    decision_strength: float  # 0.0 - 1.0
    action_priority: str  # URGENT, HIGH, NORMAL, LOW
    
    # 📊 FACTORES DECISIVOS
    key_factors: List[str]
    supporting_evidence: List[Dict[str, Any]]
    risk_warnings: List[str]
    
    # 🎯 PARÁMETROS OPERACIONALES
    suggested_entry_points: List[float]
    stop_loss_levels: List[float]
    take_profit_targets: List[float]
    position_sizing: Dict[str, Any]
    
    # ⏰ TIMING Y CONTEXTO
    optimal_timing: str
    market_conditions: Dict[str, Any]
    execution_constraints: List[str]
    
    # OPCIONALES CON DEFAULTS AL FINAL
    veredicto_version: str = "v4"
    
    def get_summary(self) -> Dict[str, Any]:
        """📋 Resumen ejecutivo del veredicto"""
        return {
            "decision": self.final_decision,
            "strength": self.decision_strength,
            "priority": self.action_priority,
            "factors": len(self.key_factors),
            "entries": len(self.suggested_entry_points),
            "timing": self.optimal_timing
        }

@dataclass
class TCTData:
    """
    ⏱️ Datos de performance del TCT Pipeline
    Métricas de tiempo y rendimiento del análisis
    """
    
    analysis_id: str
    measurement_timestamp: str
    
    # ⏱️ MÉTRICAS PRINCIPALES
    total_analysis_time_ms: float
    component_timing: Dict[str, float]
    tct_grade: str  # A, B, C, D, F
    
    # 📊 BREAKDOWN POR TIMEFRAME
    timeframe_performance: Dict[str, Dict[str, float]]
    
    # 🎯 MÉTRICAS ESPECÍFICAS
    data_loading_time_ms: float
    analysis_processing_time_ms: float
    result_formatting_time_ms: float
    
    # 📈 COMPARATIVAS
    performance_vs_baseline: float  # % mejora/degradación
    efficiency_score: float  # 0.0 - 1.0
    
    def get_summary(self) -> Dict[str, Any]:
        """📋 Resumen ejecutivo de TCT"""
        return {
            "total_time_ms": self.total_analysis_time_ms,
            "grade": self.tct_grade,
            "efficiency": self.efficiency_score,
            "components": len(self.component_timing),
            "vs_baseline": self.performance_vs_baseline
        }

@dataclass
class AnalysisOutput:
    """
    📤 Resultado consolidado final del ACC
    Payload completo para dashboard y sistemas downstream
    """
    
    # 🎯 IDENTIFICACIÓN
    analysis_id: str
    input_parameters: AnalysisInput
    analysis_status: AnalysisStatus
    completion_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # 📊 RESULTADOS PRINCIPALES
    market_structure: Optional[MarketStructureData] = None
    poi_data: Optional[POIData] = None
    confidence_data: Optional[ConfidenceData] = None
    veredicto_data: Optional[VeredictoData] = None
    tct_data: Optional[TCTData] = None
    
    # 🎖️ RESULTADOS DE COMPONENTES
    component_results: List[ComponentResult] = field(default_factory=list)
    
    # 📊 MÉTRICAS CONSOLIDADAS
    overall_success_rate: float = 0.0
    total_execution_time_ms: float = 0.0
    analysis_quality_score: float = 0.0
    
    # ⚠️ ERROR HANDLING
    errors_encountered: List[str] = field(default_factory=list)
    warnings_generated: List[str] = field(default_factory=list)
    
    # 📦 PAYLOAD PARA DASHBOARD
    dashboard_payload: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Consolidación final y logging"""
        
        # 🧮 CALCULAR MÉTRICAS CONSOLIDADAS
        self._calculate_consolidated_metrics()
        
        # 📦 GENERAR PAYLOAD DASHBOARD
        self._generate_dashboard_payload()
        
        # 📝 LOG RESULTADO FINAL
        enviar_senal_log(
            level='INFO',
            message=f"📤 AnalysisOutput completed | ID: {self.analysis_id} | "
                   f"Status: {self.analysis_status.value} | "
                   f"Success Rate: {self.overall_success_rate:.2f} | "
                   f"Time: {self.total_execution_time_ms:.2f}ms",
            emisor='acc_data_models',
            categoria='acc'
        )
    
    def _calculate_consolidated_metrics(self):
        """🧮 Calcular métricas consolidadas"""
        
        if not self.component_results:
            return
        
        # ✅ TASA DE ÉXITO
        successful_components = sum(1 for result in self.component_results if result.success)
        self.overall_success_rate = successful_components / len(self.component_results)
        
        # ⏱️ TIEMPO TOTAL
        self.total_execution_time_ms = sum(result.execution_time_ms for result in self.component_results)
        
        # 🎯 SCORE DE CALIDAD
        quality_scores = [result.quality_score for result in self.component_results if result.quality_score is not None]
        self.analysis_quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
    
    def _generate_dashboard_payload(self):
        """📦 Generar payload optimizado para dashboard"""
        
        self.dashboard_payload = {
            "analysis_id": self.analysis_id,
            "timestamp": self.completion_timestamp,
            "status": self.analysis_status.value,
            "symbol": self.input_parameters.symbol,
            "timeframes": self.input_parameters.timeframes,
            
            # 📊 DATOS PRINCIPALES
            "market_structure": self.market_structure.get_summary() if self.market_structure else None,
            "poi_summary": self.poi_data.get_summary() if self.poi_data else None,
            "confidence_summary": self.confidence_data.get_summary() if self.confidence_data else None,
            "veredicto_summary": self.veredicto_data.get_summary() if self.veredicto_data else None,
            "tct_summary": self.tct_data.get_summary() if self.tct_data else None,
            
            # 🎯 MÉTRICAS CONSOLIDADAS
            "performance": {
                "success_rate": self.overall_success_rate,
                "execution_time_ms": self.total_execution_time_ms,
                "quality_score": self.analysis_quality_score,
                "components_executed": len(self.component_results)
            },
            
            # ⚠️ ALERTAS Y WARNINGS
            "alerts": {
                "errors": len(self.errors_encountered),
                "warnings": len(self.warnings_generated),
                "has_issues": len(self.errors_encountered) > 0
            }
        }
    
    def get_executive_summary(self) -> Dict[str, Any]:
        """📋 Resumen ejecutivo ultra-condensado"""
        
        return {
            "id": self.analysis_id,
            "symbol": self.input_parameters.symbol,
            "status": self.analysis_status.value,
            "success_rate": f"{self.overall_success_rate:.1%}",
            "execution_time": f"{self.total_execution_time_ms:.0f}ms",
            "recommendation": self.veredicto_data.final_decision if self.veredicto_data else "N/A",
            "confidence": f"{self.confidence_data.overall_confidence:.1%}" if self.confidence_data else "N/A",
            "tct_grade": self.tct_data.tct_grade if self.tct_data else "N/A"
        }
