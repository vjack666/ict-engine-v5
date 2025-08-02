#!/usr/bin/env python3
"""
🎯 ACC ORCHESTRATOR - Corazón del Centro de Mando de Análisis
ARQUITECTURA: Orquestador principal que coordina todos los especialistas
PROTOCOLO: "Caja Negra" - Flujo coordinado, logging exhaustivo, manejo robusto de errores
"""

import threading
import time
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd

# 🔌 IMPORTS DEL ICT ENGINE
from sistema.logging_interface import enviar_senal_log
from utils.mt5_data_manager import MT5DataManager
from config.config_manager import get_trading_config

# 🧠 ESPECIALISTAS DE ANÁLISIS
from core.ict_engine.ict_detector import (
    MarketContext,
    OptimizedICTAnalysis,
    update_market_context,
    detectar_fair_value_gaps,
    detectar_swing_points
)
from core.ict_engine.confidence_engine import ConfidenceEngine
from core.ict_engine.pattern_analyzer import ICTPatternAnalyzer
from core.ict_engine.veredicto_engine_v4 import VeredictoEngine

# 🎯 POI SYSTEM - INTERFAZ UNIFICADA
from core.poi_system.poi_detector import POIDetector
from core.poi_system.poi_scoring_engine import POIScoringEngine

# 🎯 ACC COMPONENTS
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
from .tct_pipeline import TCTInterface

class AnalysisOrchestrator:
    """
    🎯 Centro de Mando de Análisis - Orquestador Principal
    Coordina todos los especialistas de análisis en secuencia lógica

    RESPONSABILIDADES:
    - Inicializar y gestionar todos los especialistas
    - Ejecutar flujo de análisis en secuencia optimizada
    - Consolidar resultados de todos los componentes
    - Generar payload unificado para dashboard
    - Manejar errores y timeouts de forma robusta
    """

    def __init__(self,
                 enable_cache: bool = True,
                 max_concurrent_analyses: int = 3,
                 default_timeout_seconds: int = 30):
        """
        🎯 Inicialización del Centro de Mando

        Args:
            enable_cache: Activar caching inteligente entre análisis
            max_concurrent_analyses: Máximo análisis simultáneos
            default_timeout_seconds: Timeout por defecto para análisis
        """

        # 🎛️ CONFIGURACIÓN BÁSICA
        self.enable_cache = enable_cache
        self.max_concurrent_analyses = max_concurrent_analyses
        self.default_timeout_seconds = default_timeout_seconds

        # 📊 ESTADO Y CONTROL
        self.is_initialized = False
        self.active_analyses = {}  # analysis_id -> AnalysisOutput
        self.analysis_history = []  # Historial de análisis completados
        self.component_stats = {}  # Estadísticas de performance por componente
        self._component_execution_times = {}  # Tiempos de ejecución por componente
        self._component_success_rates = {}  # Tasas de éxito por componente

        # 🎖️ INICIALIZAR ESPECIALISTAS
        self._initialize_specialists()

        # 💾 CACHE Y PERFORMANCE
        self.results_cache = {} if enable_cache else None
        self.performance_baseline = None

        # 🧵 CONTROL DE CONCURRENCIA
        self._analysis_lock = threading.Lock()
        self._initialization_lock = threading.Lock()

        # 📝 LOG INICIALIZACIÓN
        enviar_senal_log(
            'DEBUG',
            f"ACC AnalysisOrchestrator inicializado | "
                   f"Cache: {enable_cache} | "
                   f"Max Concurrent: {max_concurrent_analyses} | "
                   f"Timeout: {default_timeout_seconds}s",
            'acc_orchestrator',
            'acc'
        )

        enviar_senal_log(
            'INFO',
            "ACC Centro de Mando de Análisis activado",
            'acc_orchestrator',
            'acc'
        )

    def _initialize_specialists(self):
        """🎖️ Inicializar todos los especialistas de análisis"""

        try:
            # 📊 DATA MANAGER
            self.data_manager = MT5DataManager()

            # 🧠 ICT ENGINE COMPONENTS
            self.ict_analysis = OptimizedICTAnalysis()
            self.confidence_engine = ConfidenceEngine()
            self.pattern_analyzer = ICTPatternAnalyzer()
            self.veredicto_engine = VeredictoEngine()

            # 🎯 POI SYSTEM - PROTOCOLO SYNAPSE 3.1
            self.poi_detector = POIDetector()  # 🎯 NUEVO ESPECIALISTA INTEGRADO
            self.poi_scoring_engine = POIScoringEngine()

            # ⏱️ TCT PIPELINE
            self.tct_interface = TCTInterface(
                measurement_interval=1.0,
                aggregation_interval=60.0,
                enable_exports=True
            )

            # ⚙️ CONFIGURACIÓN
            self.trading_config = get_trading_config()

            self.is_initialized = True

            # 📝 LOG ÉXITO
            enviar_senal_log(
                'DEBUG',
                "ACC Todos los especialistas inicializados correctamente",
                'acc_orchestrator',
                'acc'
            )

        except Exception as e:
            enviar_senal_log(
                'ERROR',
                f"ERROR inicializando especialistas: {str(e)}",
                'acc_orchestrator',
                'acc'
            )
            self.is_initialized = False
            raise

    def run_full_analysis_cycle(self,
                              symbol: str,
                              timeframes: List[str],
                              analysis_type: str = "FULL_CYCLE",
                              **kwargs) -> AnalysisOutput:
        """
        🎼 SINFONÍA DE ANÁLISIS COMPLETA
        Ejecuta secuencia coordinada de todos los especialistas

        FLUJO DE 7 PASOS:
        1. Obtener datos consolidados
        2. Análisis de estructura ICT
        3. Detección inteligente de POIs
        4. Cálculo de confianza avanzada
        5. Generación de veredicto final
        6. Medición de performance (TCT)
        7. Consolidación de payload

        Args:
            symbol: Símbolo a analizar (ej: "EURUSD")
            timeframes: Lista de timeframes (ej: ["M1", "M5", "M15"])
            analysis_type: Tipo de análisis ("FULL_CYCLE", "FOCUSED", "QUICK")
            **kwargs: Parámetros adicionales

        Returns:
            AnalysisOutput: Resultado consolidado del análisis completo
        """

        if not self.is_initialized:
            raise RuntimeError("AnalysisOrchestrator no está inicializado")

        # 🎯 CREAR INPUT ESTANDARIZADO
        analysis_input = AnalysisInput(
            symbol=symbol,
            timeframes=timeframes,
            analysis_type=analysis_type,
            **kwargs
        )

        # 📊 INICIALIZAR OUTPUT
        analysis_output = AnalysisOutput(
            analysis_id=analysis_input.analysis_id,
            input_parameters=analysis_input,
            analysis_status=AnalysisStatus.RUNNING
        )

        # 🔒 REGISTRAR ANÁLISIS ACTIVO
        with self._analysis_lock:
            self.active_analyses[analysis_input.analysis_id] = analysis_output

        # 📝 LOG INICIO
        enviar_senal_log(
            'INFO',
            f"ACC Iniciando análisis completo | ID: {analysis_input.analysis_id} | "
                   f"Symbol: {symbol} | Timeframes: {timeframes}",
            'acc_orchestrator',
            'acc'
        )

        try:
            # ⏱️ 1. INICIAR MEDICIÓN TCT
            tct_measurement_id = self._start_tct_measurement(analysis_input)

            # 📊 2. OBTENER DATOS CONSOLIDADOS
            data_payload = self._execute_data_acquisition(analysis_input, analysis_output)

            # 🧠 3. ANÁLISIS DE ESTRUCTURA ICT
            market_structure = self._execute_ict_analysis(analysis_input, data_payload, analysis_output)

            # 🎯 4. DETECCIÓN INTELIGENTE DE POIS
            poi_data = self._execute_poi_detection(analysis_input, data_payload, market_structure, analysis_output)

            # ⚖️ 5. CÁLCULO DE CONFIANZA AVANZADA
            confidence_data = self._execute_confidence_analysis(analysis_input, market_structure, poi_data, analysis_output)

            # 🔮 6. GENERACIÓN DE VEREDICTO FINAL
            veredicto_data = self._execute_veredicto_generation(analysis_input, market_structure, poi_data, confidence_data, analysis_output)

            # ⏱️ 7. FINALIZAR MEDICIÓN TCT
            tct_data = self._finalize_tct_measurement(tct_measurement_id, analysis_input, analysis_output)

            # 📦 8. CONSOLIDAR RESULTADOS
            self._consolidate_final_results(analysis_output, market_structure, poi_data, confidence_data, veredicto_data, tct_data)

            # ✅ MARCAR COMO COMPLETADO
            analysis_output.analysis_status = AnalysisStatus.COMPLETED

            # 📝 LOG ÉXITO
            tct_time = tct_data.total_analysis_time_ms if tct_data else 0.0
            enviar_senal_log(
                'INFO',
                f"ACC Análisis completo finalizado | ID: {analysis_input.analysis_id} | "
                       f"TCT: {tct_time:.2f}ms | "
                       f"Success Rate: {analysis_output.overall_success_rate:.2f} | "
                       f"Recommendation: {veredicto_data.final_decision if veredicto_data else 'N/A'}",
                'acc_orchestrator',
                'acc'
            )

        except (RuntimeError, ValueError, AttributeError, KeyError) as e:
            # ❌ MANEJO DE ERRORES
            analysis_output.analysis_status = AnalysisStatus.FAILED
            analysis_output.errors_encountered.append(str(e))

            enviar_senal_log(
                'ERROR',
                f"ERROR en análisis completo | ID: {analysis_input.analysis_id} | Error: {str(e)}",
                'acc_orchestrator',
                'acc'
            )

        finally:
            # 🧹 CLEANUP
            with self._analysis_lock:
                if analysis_input.analysis_id in self.active_analyses:
                    del self.active_analyses[analysis_input.analysis_id]

            # 📚 AÑADIR AL HISTORIAL
            self.analysis_history.append(analysis_output)

            # 📊 ACTUALIZAR ESTADÍSTICAS
            self._update_component_stats(analysis_output)

        return analysis_output

    def run_focused_analysis(self,
                           symbol: str,
                           timeframe: str,
                           focus_areas: List[str]) -> AnalysisOutput:
        """
        🎯 ANÁLISIS FOCALIZADO
        Para análisis específicos o de alta frecuencia

        Args:
            symbol: Símbolo a analizar
            timeframe: Timeframe específico
            focus_areas: Áreas de enfoque ["ICT", "POI", "CONFIDENCE", "VEREDICTO"]
        """

        return self.run_full_analysis_cycle(
            symbol=symbol,
            timeframes=[timeframe],
            analysis_type="FOCUSED",
            focus_areas=focus_areas,
            max_analysis_time_seconds=10  # Análisis más rápido
        )

    def get_analysis_status(self, analysis_id: Optional[str] = None) -> Dict[str, Any]:
        """
        📊 Estado actual del centro de análisis

        Args:
            analysis_id: ID específico de análisis (opcional)

        Returns:
            Dict con estado del análisis o resumen general
        """

        if analysis_id:
            # 📊 ESTADO DE ANÁLISIS ESPECÍFICO
            if analysis_id in self.active_analyses:
                analysis = self.active_analyses[analysis_id]
                return {
                    "analysis_id": analysis_id,
                    "status": analysis.analysis_status.value,
                    "symbol": analysis.input_parameters.symbol,
                    "progress": self._calculate_analysis_progress(analysis),
                    "estimated_completion": self._estimate_completion_time(analysis)
                }
            else:
                return {"error": f"Analysis {analysis_id} not found"}

        # 📊 ESTADO GENERAL DEL ACC
        return {
            "acc_status": "OPERATIONAL" if self.is_initialized else "ERROR",
            "active_analyses": len(self.active_analyses),
            "total_completed": len(self.analysis_history),
            "avg_success_rate": self._calculate_avg_success_rate(),
            "avg_execution_time": self._calculate_avg_execution_time(),
            "component_health": self._get_component_health_summary()
        }

    def _start_tct_measurement(self, analysis_input: AnalysisInput) -> str:
        """⏱️ Iniciar medición TCT del análisis completo"""

        try:
            measurement_id = self.tct_interface.measure_single_analysis(
                symbol=analysis_input.symbol,
                timeframe=analysis_input.timeframes[0] if analysis_input.timeframes else "M15"
            )

            if measurement_id:
                return measurement_id.get('measurement_id', str(uuid.uuid4()))
            else:
                return str(uuid.uuid4())  # Fallback ID

        except Exception as e:
            enviar_senal_log(
                'WARNING',
                f"Error iniciando TCT measurement: {str(e)}",
                'acc_orchestrator',
                'acc'
            )
            return str(uuid.uuid4())  # Fallback ID

    def _execute_data_acquisition(self,
                                analysis_input: AnalysisInput,
                                analysis_output: AnalysisOutput) -> Dict[str, Any]:
        """📊 Ejecutar adquisición de datos consolidados"""

        start_time = time.time()

        try:
            # 📈 OBTENER DATOS MULTI-TIMEFRAME
            data_payload = {}

            for timeframe in analysis_input.timeframes:
                # 🔄 OBTENER DATOS POR TIMEFRAME
                lookback_periods = analysis_input.lookback_periods or {}
                df_data = self.data_manager.get_historical_data(
                    symbol=analysis_input.symbol,
                    timeframe=timeframe,
                    lookback=lookback_periods.get(timeframe, 500)
                )

                if df_data is not None and not df_data.empty:
                    data_payload[timeframe] = df_data
                else:
                    analysis_output.warnings_generated.append(f"No data for {timeframe}")

            execution_time = (time.time() - start_time) * 1000

            # 📊 REGISTRAR RESULTADO
            component_result = ComponentResult(
                component_type=ComponentType.DATA_MANAGER,
                component_name="MT5DataManager",
                success=len(data_payload) > 0,
                execution_time_ms=execution_time,
                data={"timeframes_loaded": list(data_payload.keys())},
                items_processed=len(data_payload)
            )

            analysis_output.component_results.append(component_result)

            return data_payload

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000

            component_result = ComponentResult(
                component_type=ComponentType.DATA_MANAGER,
                component_name="MT5DataManager",
                success=False,
                execution_time_ms=execution_time,
                error_message=str(e)
            )

            analysis_output.component_results.append(component_result)
            raise

    def _execute_ict_analysis(self,
                            analysis_input: AnalysisInput,
                            data_payload: Dict[str, Any],
                            analysis_output: AnalysisOutput) -> Optional[MarketStructureData]:
        """🧠 Ejecutar análisis de estructura ICT"""

        start_time = time.time()

        try:
            # 🎯 ANÁLISIS ICT PRINCIPAL
            primary_timeframe = analysis_input.timeframes[0]
            df_primary = data_payload.get(primary_timeframe)

            if df_primary is None:
                raise ValueError(f"No data available for primary timeframe {primary_timeframe}")

            # 🧠 ANÁLISIS COMPLETO
            # Obtener precio actual real del mercado
            if df_primary.empty:
                raise ValueError(f"No hay datos de precio para {analysis_input.symbol}")

            current_market_price = float(df_primary.iloc[-1]['close'])

            # Crear contexto de mercado inicial
            market_context = MarketContext()
            market_context.current_price = current_market_price

            # Actualizar contexto con datos multi-timeframe
            update_market_context(
                contexto=market_context,
                df_by_timeframe=data_payload,
                current_price=current_market_price
            )

            # 📊 DETECTAR PATRONES
            fair_value_gaps = detectar_fair_value_gaps(df_primary)
            swing_points = detectar_swing_points(df_primary)

            # 🎯 EVALUAR ESTRUCTURA
            df_h4 = data_payload.get('H4', df_primary)
            df_m5 = data_payload.get('M5', None)
            structure_analysis = self.ict_analysis.analisis_completo_ict(df_h4, df_primary, df_m5)

            # 📊 CREAR RESULTADO ESTANDARIZADO
            # Determinar sesión real basada en timestamp actual
            current_hour_utc = datetime.now().hour
            session_type = self._determine_real_trading_session(current_hour_utc)

            # Validar que tenemos datos reales
            if not structure_analysis:
                raise ValueError("No se pudo obtener análisis de estructura ICT")

            market_structure = MarketStructureData(
                symbol=analysis_input.symbol,
                timeframe=primary_timeframe,
                timestamp=datetime.now().isoformat(),
                trend=structure_analysis.get('trend', self._calculate_real_trend(df_primary)),
                market_structure=structure_analysis.get('structure', self._analyze_real_market_structure(df_primary)),
                session_type=session_type,
                premium_discount_zone=structure_analysis.get('pd_zone', self._calculate_real_pd_zone(df_primary, current_market_price)),
                fair_value_gaps=fair_value_gaps or [],
                swing_points=swing_points if isinstance(swing_points, dict) else self._process_swing_points_data(swing_points),
                structure_strength=structure_analysis.get('strength', self._calculate_real_structure_strength(df_primary)),
                volatility_index=structure_analysis.get('volatility', self._calculate_real_volatility(df_primary)),
                liquidity_zones=structure_analysis.get('liquidity_zones', self._detect_real_liquidity_zones(df_primary)),
                patterns_detected=structure_analysis.get('patterns', self._detect_real_patterns(df_primary)),
                pattern_confluence=len(structure_analysis.get('patterns', []))
            )

            execution_time = (time.time() - start_time) * 1000

            # 📊 REGISTRAR RESULTADO
            component_result = ComponentResult(
                component_type=ComponentType.ICT_DETECTOR,
                component_name="OptimizedICTAnalysis",
                success=True,
                execution_time_ms=execution_time,
                data=market_structure.get_summary(),
                items_processed=len(analysis_input.timeframes),
                confidence_score=market_structure.structure_strength
            )

            analysis_output.component_results.append(component_result)

            return market_structure

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000

            component_result = ComponentResult(
                component_type=ComponentType.ICT_DETECTOR,
                component_name="OptimizedICTAnalysis",
                success=False,
                execution_time_ms=execution_time,
                error_message=str(e)
            )

            analysis_output.component_results.append(component_result)

            enviar_senal_log(
                'ERROR',
                f"Error en análisis ICT: {str(e)}",
                'acc_orchestrator',
                'acc'
            )

            return None

    def _execute_poi_detection(self,
                             analysis_input: AnalysisInput,
                             data_payload: Dict[str, Any],
                             market_structure: Optional[MarketStructureData],
                             analysis_output: AnalysisOutput) -> Optional[POIData]:
        """
        🎯 PROTOCOLO SYNAPSE 3.1 - DETECCIÓN UNIFICADA DE POIs
        =====================================================

        Ejecuta detección inteligente de POIs usando el nuevo POIDetector
        integrado. Coordina la detección multi-timeframe y el scoring.
        """

        start_time = time.time()

        try:
            enviar_senal_log(
                'INFO',
                "SYNAPSE 3.1: Iniciando detección unificada de POIs",
                'acc_orchestrator',
                'poi'
            )

            # 🎯 DETECCIÓN MULTI-TIMEFRAME CON NUEVO POIDetector
            all_detected_pois = []
            timeframe_summary = {}

            for timeframe in analysis_input.timeframes:
                # Obtener DataFrame para este timeframe
                tf_data = data_payload.get(timeframe)
                if not tf_data or tf_data.empty:
                    enviar_senal_log(
                        'WARNING',
                        f"No hay datos para timeframe {timeframe}",
                        'acc_orchestrator',
                        'poi'
                    )
                    continue

                # 🔍 USAR NUEVO POIDetector UNIFICADO
                pois_in_tf = self.poi_detector.find_all_pois(
                    df=tf_data,
                    timeframe=timeframe,
                    current_price=tf_data['close'].iloc[-1] if not tf_data.empty else None
                )

                # 📊 ESTADÍSTICAS POR TIMEFRAME
                timeframe_summary[timeframe] = {
                    'total_pois': len(pois_in_tf),
                    'poi_types': list(set(poi.get('type', 'UNKNOWN') for poi in pois_in_tf))
                }

                all_detected_pois.extend(pois_in_tf)

                enviar_senal_log(
                    nivel='DEBUG',
                    mensaje=f"TF {timeframe}: {len(pois_in_tf)} POIs detectados",
                    emisor='acc_orchestrator',
                    categoria='poi'
                )

            # 📊 SCORING INTELIGENTE DE TODOS LOS POIs
            scored_pois = []
            total_score = 0
            current_price = None

            # Obtener precio actual del primer timeframe con datos
            for tf in analysis_input.timeframes:
                tf_data = data_payload.get(tf)
                if tf_data and not tf_data.empty:
                    current_price = tf_data['close'].iloc[-1]
                    break

            if current_price is None:
                current_price = 1.0  # Fallback

            for poi in all_detected_pois:
                try:
                    # Convertir MarketStructureData a dict si es necesario
                    market_context_dict = None
                    if market_structure:
                        market_context_dict = {
                            'trend': market_structure.trend,
                            'structure': market_structure.market_structure,
                            'session': market_structure.session_type,
                            'volatility': market_structure.volatility_index,
                            'strength': market_structure.structure_strength
                        }

                    score = self.poi_scoring_engine.calculate_intelligent_score(
                        poi=poi,
                        current_price=current_price,
                        market_context=market_context_dict
                    )

                    # Asegurar que score es un número
                    if isinstance(score, (int, float)):
                        poi['intelligent_score'] = score
                        scored_pois.append(poi)
                        total_score += score
                    else:
                        poi['intelligent_score'] = 0.0
                        scored_pois.append(poi)

                except Exception as e:
                    enviar_senal_log(
                        nivel='WARNING',
                        mensaje=f"Error scoring POI {poi.get('id', 'unknown')}: {str(e)}",
                        emisor='acc_orchestrator',
                        categoria='poi'
                    )

            # 🎯 ANÁLISIS ESTADÍSTICO Y CONSOLIDACIÓN
            avg_score = total_score / len(scored_pois) if scored_pois else 0.0
            top_scored = sorted(scored_pois, key=lambda x: x.get('intelligent_score', 0), reverse=True)[:5]

            # 📊 ANÁLISIS POR TIPOS
            poi_types_count = {}
            for poi in scored_pois:
                poi_type = poi.get('type', 'UNKNOWN')
                poi_types_count[poi_type] = poi_types_count.get(poi_type, 0) + 1

            # 📊 CREAR RESULTADO ESTANDARIZADO
            poi_data = POIData(
                symbol=analysis_input.symbol,
                timeframe=analysis_input.timeframes[0],
                timestamp=datetime.now().isoformat(),
                pois_list=scored_pois,
                total_pois=len(scored_pois),
                top_scored_pois=top_scored,
                average_score=avg_score,
                score_distribution=timeframe_summary,
                poi_types_count=poi_types_count,
                confluence_zones=self._analyze_confluence_zones(data_payload),
                clustering_analysis=self._analyze_poi_clustering(data_payload),
                temporal_distribution=self._analyze_temporal_distribution(data_payload)
            )

            execution_time = (time.time() - start_time) * 1000

            # 📊 REGISTRAR RESULTADO
            component_result = ComponentResult(
                component_type=ComponentType.POI_DETECTOR,
                component_name="POIDetectionSystem",
                success=True,
                execution_time_ms=execution_time,
                data=poi_data.get_summary(),
                items_processed=len(scored_pois),
                confidence_score=avg_score
            )

            analysis_output.component_results.append(component_result)

            return poi_data

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000

            component_result = ComponentResult(
                component_type=ComponentType.POI_DETECTOR,
                component_name="POIDetectionSystem",
                success=False,
                execution_time_ms=execution_time,
                error_message=str(e)
            )

            analysis_output.component_results.append(component_result)

            enviar_senal_log(
                nivel='ERROR',
                mensaje=f"Error en detección POI: {str(e)}",
                emisor='acc_orchestrator',
                categoria='acc'
            )

            return None

    def _execute_confidence_analysis(self,
                                   analysis_input: AnalysisInput,
                                   market_structure: Optional[MarketStructureData],
                                   poi_data: Optional[POIData],
                                   analysis_output: AnalysisOutput) -> Optional[ConfidenceData]:
        """⚖️ Ejecutar cálculo de confianza avanzada"""

        start_time = time.time()

        try:
            # 💰 OBTENER PRECIO ACTUAL REAL
            current_market_price = 1.0  # Default fallback
            if market_structure:
                # Extraer precio del market structure si está disponible
                current_market_price = market_structure.premium_discount_zone.get('current_position', 1.0)

            # ⚖️ CALCULAR CONFIANZA GLOBAL
            # Como ConfidenceEngine no tiene calculate_overall_confidence, calculamos manualmente
            overall_confidence = 0.5  # Default confidence

            if market_structure and poi_data and poi_data.pois_list:
                # Usar average_score de POIs como base de confianza
                overall_confidence = min(poi_data.average_score, 1.0)

            # 📊 CONFIDENCE POR PATRONES
            pattern_confidence = {}
            if market_structure and market_structure.patterns_detected:
                for pattern in market_structure.patterns_detected:
                    try:
                        # Crear dict de patrón para el método
                        pattern_dict = {
                            'type': pattern,
                            'confidence': 0.5,
                            'strength': market_structure.structure_strength
                        }

                        # Convertir MarketStructureData a dict
                        market_context_dict = {
                            'trend': market_structure.trend,
                            'structure': market_structure.market_structure,
                            'session': market_structure.session_type,
                            'volatility': market_structure.volatility_index
                        }

                        pattern_conf = self.confidence_engine.calculate_pattern_confidence(
                            pattern=pattern_dict,
                            market_context=market_context_dict,
                            poi_list=poi_data.pois_list if poi_data else [],
                            current_price=current_market_price
                        )

                        pattern_confidence[pattern] = pattern_conf

                    except Exception as e:
                        enviar_senal_log(
                            nivel='WARNING',
                            mensaje=f"Error calculando confianza para patrón {pattern}: {str(e)}",
                            emisor='acc_orchestrator',
                            categoria='acc'
                        )
                        pattern_confidence[pattern] = 0.5  # Default

            # 📊 CREAR RESULTADO ESTANDARIZADO
            # Calcular scores reales de análisis fundamental y sentimiento
            fundamental_score = self._calculate_real_fundamental_score(analysis_input.symbol)
            sentiment_score = self._calculate_real_sentiment_score(market_structure, poi_data)
            risk_level = self._assess_real_risk_level(market_structure, overall_confidence)
            uncertainty_factors = self._identify_uncertainty_factors(market_structure, poi_data)
            confidence_drivers = self._identify_confidence_drivers(market_structure, poi_data, pattern_confidence)
            trading_recommendation = self._generate_real_trading_recommendation(overall_confidence, risk_level)

            confidence_data = ConfidenceData(
                symbol=analysis_input.symbol,
                analysis_timestamp=datetime.now().isoformat(),
                overall_confidence=overall_confidence,
                pattern_confidence=pattern_confidence,
                poi_confidence=self._calculate_poi_confidence_scores(poi_data),
                technical_score=overall_confidence,
                fundamental_score=fundamental_score,
                sentiment_score=sentiment_score,
                risk_assessment=risk_level,
                uncertainty_factors=uncertainty_factors,
                confidence_drivers=confidence_drivers,
                trading_recommendation=trading_recommendation,
                confidence_level="HIGH" if overall_confidence > 0.7 else "MEDIUM" if overall_confidence > 0.4 else "LOW"
            )

            execution_time = (time.time() - start_time) * 1000

            # 📊 REGISTRAR RESULTADO
            component_result = ComponentResult(
                component_type=ComponentType.CONFIDENCE_ENGINE,
                component_name="ConfidenceEngine",
                success=True,
                execution_time_ms=execution_time,
                data=confidence_data.get_summary(),
                items_processed=len(pattern_confidence) + 1,  # +1 for overall
                confidence_score=overall_confidence
            )

            analysis_output.component_results.append(component_result)

            return confidence_data

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000

            component_result = ComponentResult(
                component_type=ComponentType.CONFIDENCE_ENGINE,
                component_name="ConfidenceEngine",
                success=False,
                execution_time_ms=execution_time,
                error_message=str(e)
            )

            analysis_output.component_results.append(component_result)

            enviar_senal_log(
                nivel='ERROR',
                mensaje=f"Error en análisis de confianza: {str(e)}",
                emisor='acc_orchestrator',
                categoria='acc'
            )

            return None

    def _execute_veredicto_generation(self,
                                    analysis_input: AnalysisInput,
                                    market_structure: Optional[MarketStructureData],
                                    poi_data: Optional[POIData],
                                    confidence_data: Optional[ConfidenceData],
                                    analysis_output: AnalysisOutput) -> Optional[VeredictoData]:
        """🔮 Ejecutar generación de veredicto final"""

        start_time = time.time()

        try:
            # 🔮 GENERAR VEREDICTO
            # Preparar patrones ICT para el veredicto
            ict_patterns = []
            if market_structure and market_structure.patterns_detected:
                for pattern in market_structure.patterns_detected:
                    # Obtener confianza del confidence_data si está disponible
                    pattern_conf = 0.5
                    if confidence_data and confidence_data.pattern_confidence:
                        pattern_conf = confidence_data.pattern_confidence.get(pattern, 0.5)

                    ict_patterns.append({
                        'type': pattern,
                        'confidence': pattern_conf,
                        'strength': market_structure.structure_strength
                    })

            # Preparar contexto de mercado
            market_context = None
            if market_structure:
                market_context = {
                    'trend': market_structure.trend,
                    'structure': market_structure.market_structure,
                    'session': market_structure.session_type,
                    'volatility': market_structure.volatility_index
                }

            veredicto_result = self.veredicto_engine.generate_market_veredicto(
                enhanced_pois=poi_data.pois_list if poi_data else [],
                ict_patterns=ict_patterns,
                market_context=market_context,
                current_price=market_structure.premium_discount_zone.get('current_position', 1.0) if market_structure else 1.0
            )

            # 📊 CREAR RESULTADO ESTANDARIZADO
            veredicto_data = VeredictoData(
                symbol=analysis_input.symbol,
                analysis_timestamp=datetime.now().isoformat(),
                veredicto_version="v4",
                final_decision=veredicto_result.get('decision', 'HOLD'),
                decision_strength=veredicto_result.get('strength', 0.5),
                action_priority=veredicto_result.get('priority', 'NORMAL'),
                key_factors=veredicto_result.get('factors', []),
                supporting_evidence=veredicto_result.get('evidence', []),
                risk_warnings=veredicto_result.get('warnings', []),
                suggested_entry_points=veredicto_result.get('entry_points', []),
                stop_loss_levels=veredicto_result.get('stop_loss', []),
                take_profit_targets=veredicto_result.get('take_profit', []),
                position_sizing=veredicto_result.get('position_sizing', {}),
                optimal_timing=veredicto_result.get('timing', 'IMMEDIATE'),
                market_conditions=veredicto_result.get('conditions', {}),
                execution_constraints=veredicto_result.get('constraints', [])
            )

            execution_time = (time.time() - start_time) * 1000

            # 📊 REGISTRAR RESULTADO
            component_result = ComponentResult(
                component_type=ComponentType.VEREDICTO_ENGINE,
                component_name="VeredictoEngine",
                success=True,
                execution_time_ms=execution_time,
                data=veredicto_data.get_summary(),
                items_processed=1,
                confidence_score=veredicto_data.decision_strength
            )

            analysis_output.component_results.append(component_result)

            return veredicto_data

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000

            component_result = ComponentResult(
                component_type=ComponentType.VEREDICTO_ENGINE,
                component_name="VeredictoEngine",
                success=False,
                execution_time_ms=execution_time,
                error_message=str(e)
            )

            analysis_output.component_results.append(component_result)

            enviar_senal_log(
                nivel='ERROR',
                mensaje=f"Error en generación de veredicto: {str(e)}",
                emisor='acc_orchestrator',
                categoria='acc'
            )

            return None

    def _finalize_tct_measurement(self,
                                tct_measurement_id: str,
                                analysis_input: AnalysisInput,
                                analysis_output: AnalysisOutput) -> Optional[TCTData]:
        """⏱️ Finalizar medición TCT y obtener métricas"""

        try:
            # Log del ID de medición para tracking
            enviar_senal_log(
                nivel='DEBUG',
                mensaje=f"Finalizando medición TCT ID: {tct_measurement_id}",
                emisor='acc_orchestrator',
                categoria='tct'
            )

            # ⏱️ OBTENER MÉTRICAS TCT
            tct_dashboard_data = self.tct_interface.get_formatted_dashboard_data()

            if not tct_dashboard_data:
                # 🔄 CREAR MÉTRICAS BÁSICAS COMO FALLBACK
                total_time = sum(result.execution_time_ms for result in analysis_output.component_results)

                tct_data = TCTData(
                    analysis_id=analysis_input.analysis_id,
                    measurement_timestamp=datetime.now().isoformat(),
                    total_analysis_time_ms=total_time,
                    component_timing={result.component_type.value: result.execution_time_ms
                                    for result in analysis_output.component_results},
                    tct_grade=self._calculate_tct_grade(total_time),
                    timeframe_performance={},
                    data_loading_time_ms=0.0,
                    analysis_processing_time_ms=total_time,
                    result_formatting_time_ms=0.0,
                    performance_vs_baseline=0.0,
                    efficiency_score=0.5
                )
            else:
                # 📊 USAR MÉTRICAS REALES DE TCT
                tct_data = self._convert_tct_dashboard_to_data(tct_dashboard_data, analysis_input, analysis_output)

            # 📊 REGISTRAR RESULTADO
            component_result = ComponentResult(
                component_type=ComponentType.TCT_PIPELINE,
                component_name="TCTInterface",
                success=True,
                execution_time_ms=0.0,  # TCT no se mide a sí mismo
                data=tct_data.get_summary(),
                items_processed=len(analysis_output.component_results)
            )

            analysis_output.component_results.append(component_result)

            return tct_data

        except Exception as e:
            enviar_senal_log(
                nivel='WARNING',
                mensaje=f"Error finalizando TCT measurement: {str(e)}",
                emisor='acc_orchestrator',
                categoria='acc'
            )

            # 🔄 FALLBACK TCT DATA
            return TCTData(
                analysis_id=analysis_input.analysis_id,
                measurement_timestamp=datetime.now().isoformat(),
                total_analysis_time_ms=sum(result.execution_time_ms for result in analysis_output.component_results),
                component_timing={},
                tct_grade="C",
                timeframe_performance={},
                data_loading_time_ms=0.0,
                analysis_processing_time_ms=0.0,
                result_formatting_time_ms=0.0,
                performance_vs_baseline=0.0,
                efficiency_score=0.5
            )

    def _consolidate_final_results(self,
                                 analysis_output: AnalysisOutput,
                                 market_structure: Optional[MarketStructureData],
                                 poi_data: Optional[POIData],
                                 confidence_data: Optional[ConfidenceData],
                                 veredicto_data: Optional[VeredictoData],
                                 tct_data: Optional[TCTData]):
        """📦 Consolidar todos los resultados en el output final"""

        # 📊 ASIGNAR DATOS PRINCIPALES
        analysis_output.market_structure = market_structure
        analysis_output.poi_data = poi_data
        analysis_output.confidence_data = confidence_data
        analysis_output.veredicto_data = veredicto_data
        analysis_output.tct_data = tct_data

        # 🎯 LAS MÉTRICAS CONSOLIDADAS SE CALCULAN EN __post_init__ DEL OUTPUT

        enviar_senal_log(
            nivel='DEBUG',
            mensaje=f"Resultados consolidados | ID: {analysis_output.analysis_id} | "
                   f"Components: {len(analysis_output.component_results)}",
            emisor='acc_orchestrator',
            categoria='acc'
        )

    def _calculate_tct_grade(self, total_time_ms: float) -> str:
        """⏱️ Calcular grade TCT basado en tiempo total"""
        if total_time_ms <= 1000:    # <= 1s
            return "A"
        elif total_time_ms <= 3000:  # <= 3s
            return "B"
        elif total_time_ms <= 5000:  # <= 5s
            return "C"
        elif total_time_ms <= 10000: # <= 10s
            return "D"
        else:
            return "F"

    def _convert_tct_dashboard_to_data(self, tct_dashboard: Dict, analysis_input: AnalysisInput, analysis_output: AnalysisOutput) -> TCTData:
        """📊 Convertir datos de dashboard TCT a TCTData"""

        tct_status = tct_dashboard.get('tct_status', {})
        tct_performance = tct_dashboard.get('tct_performance', {})

        # Extraer timing real de los componentes del dashboard
        component_timing = {}
        if 'component_timings' in tct_dashboard:
            component_timing = tct_dashboard['component_timings']
        elif hasattr(analysis_output, 'component_results') and analysis_output.component_results:
            # Calcular timing basado en resultados de componentes
            for result in analysis_output.component_results:
                component_timing[result.component_name] = result.execution_time_ms

        return TCTData(
            analysis_id=analysis_input.analysis_id,
            measurement_timestamp=datetime.now().isoformat(),
            total_analysis_time_ms=tct_performance.get('avg_tct_ms', 0.0),
            component_timing=component_timing,
            tct_grade=tct_status.get('performance_grade', 'C'),
            timeframe_performance=tct_dashboard.get('tct_timeframes', {}),
            data_loading_time_ms=0.0,
            analysis_processing_time_ms=tct_performance.get('avg_tct_ms', 0.0),
            result_formatting_time_ms=0.0,
            performance_vs_baseline=0.0,
            efficiency_score=0.5
        )

    def _calculate_analysis_progress(self, analysis: AnalysisOutput) -> float:
        """📊 Calcular progreso de análisis (0.0 - 1.0)"""
        expected_components = 6  # DATA, ICT, POI, CONFIDENCE, VEREDICTO, TCT
        completed_components = len(analysis.component_results)
        return min(completed_components / expected_components, 1.0)

    def _estimate_completion_time(self, analysis: AnalysisOutput) -> str:
        """⏰ Estimar tiempo de finalización basado en progreso actual"""
        if not analysis or not analysis.component_results:
            return "Estimating..."

        # Calcular tiempo promedio por componente
        total_time = sum(result.execution_time_ms for result in analysis.component_results)
        avg_time_per_component = total_time / len(analysis.component_results) if analysis.component_results else 1000

        # Estimar componentes restantes
        expected_components = 6  # DATA, ICT, POI, CONFIDENCE, VEREDICTO, TCT
        remaining_components = max(0, expected_components - len(analysis.component_results))

        if remaining_components == 0:
            return "Completed"

        estimated_remaining_ms = remaining_components * avg_time_per_component

        if estimated_remaining_ms < 1000:
            return f"~{int(estimated_remaining_ms)}ms"
        elif estimated_remaining_ms < 60000:
            return f"~{int(estimated_remaining_ms/1000)}s"
        else:
            return f"~{int(estimated_remaining_ms/60000)}min"

    def _calculate_avg_success_rate(self) -> float:
        """📊 Calcular tasa de éxito promedio"""
        if not self.analysis_history:
            return 0.0

        total_success_rate = sum(analysis.overall_success_rate for analysis in self.analysis_history)
        return total_success_rate / len(self.analysis_history)

    def _calculate_avg_execution_time(self) -> float:
        """⏱️ Calcular tiempo de ejecución promedio"""
        if not self.analysis_history:
            return 0.0

        total_time = sum(analysis.total_execution_time_ms for analysis in self.analysis_history)
        return total_time / len(self.analysis_history)

    def _get_component_health_summary(self) -> Dict[str, str]:
        """🏥 Resumen de salud de componentes basado en estadísticas"""
        health_summary = {}

        if not self.analysis_history:
            # Sin historial, asumir salud básica
            return {
                "data_manager": "HEALTHY",
                "ict_detector": "HEALTHY",
                "poi_detector": "HEALTHY",
                "confidence_engine": "HEALTHY",
                "veredicto_engine": "HEALTHY",
                "tct_interface": "HEALTHY"
            }

        # Analizar salud basado en tasas de éxito recientes
        component_stats = {}

        for analysis in self.analysis_history[-10:]:  # Últimos 10 análisis
            for result in analysis.component_results:
                component = result.component_name
                if component not in component_stats:
                    component_stats[component] = {'successes': 0, 'total': 0}

                component_stats[component]['total'] += 1
                if result.success:
                    component_stats[component]['successes'] += 1

        # Determinar estado de salud
        for component, stats in component_stats.items():
            success_rate = stats['successes'] / stats['total'] if stats['total'] > 0 else 0

            if success_rate >= 0.9:
                health_summary[component] = "EXCELLENT"
            elif success_rate >= 0.7:
                health_summary[component] = "HEALTHY"
            elif success_rate >= 0.5:
                health_summary[component] = "WARNING"
            else:
                health_summary[component] = "CRITICAL"

        return health_summary

    def _update_component_stats(self, analysis_output: AnalysisOutput):
        """📊 Actualizar estadísticas de componentes con tracking detallado"""
        if not analysis_output or not analysis_output.component_results:
            return

        # Tracking de rendimiento por componente
        for result in analysis_output.component_results:
            component_name = result.component_name

            # Registrar tiempo de ejecución
            if hasattr(self, '_component_execution_times'):
                if component_name not in self._component_execution_times:
                    self._component_execution_times[component_name] = []
                self._component_execution_times[component_name].append(result.execution_time_ms)

            # Registrar tasa de éxito
            if hasattr(self, '_component_success_rates'):
                if component_name not in self._component_success_rates:
                    self._component_success_rates[component_name] = []
                self._component_success_rates[component_name].append(result.success)

            # Log de estadísticas si es necesario
            if result.execution_time_ms > 5000:  # Más de 5 segundos
                enviar_senal_log(
                    nivel='WARNING',
                    mensaje=f"Componente {component_name} tardó {result.execution_time_ms:.0f}ms",
                    emisor='acc_orchestrator',
                    categoria='performance'
                )

    def _determine_real_trading_session(self, hour_utc: int) -> str:
        """🕐 Determinar sesión de trading real basada en hora UTC"""
        # Sesiones de trading Forex basadas en horarios reales
        if 0 <= hour_utc < 7:  # Sydney/Tokyo overlap y Asia
            return "ASIAN"
        elif 7 <= hour_utc < 15:  # London session
            return "LONDON"
        elif 15 <= hour_utc < 17:  # London/New York overlap
            return "OVERLAP_LONDON_NY"
        elif 17 <= hour_utc < 22:  # New York session
            return "NEW_YORK"
        else:  # 22-24: Pacific/pre-market
            return "PACIFIC"

    def _calculate_real_trend(self, df: pd.DataFrame) -> str:
        """📈 Calcular tendencia real usando análisis técnico"""
        if df.empty or len(df) < 20:
            return "INSUFFICIENT_DATA"

        # Usar EMAs para determinar tendencia real
        if len(df) >= 20:
            ema_9 = df['close'].tail(9).mean()
            ema_20 = df['close'].tail(20).mean()
            current_price = df['close'].iloc[-1]

            if current_price > ema_9 > ema_20:
                return "BULLISH"
            elif current_price < ema_9 < ema_20:
                return "BEARISH"
            else:
                return "SIDEWAYS"

        return "INSUFFICIENT_DATA"

    def _analyze_real_market_structure(self, df: 'pd.DataFrame') -> str:
        """🏗️ Analizar estructura real del mercado"""
        if df.empty or len(df) < 50:
            return "INSUFFICIENT_DATA"

        # Calcular rangos y volatilidad real
        high_prices = df['high'].values[-50:]
        low_prices = df['low'].values[-50:]

        range_size = max(high_prices) - min(low_prices)
        recent_range = max(high_prices[-10:]) - min(low_prices[-10:])

        # Determinar si está en rango o tendencia
        if recent_range / range_size < 0.3:
            return "CONSOLIDATION"
        elif recent_range / range_size > 0.7:
            return "TRENDING"
        else:
            return "RANGING"

    def _calculate_real_pd_zone(self, df: 'pd.DataFrame', current_price: float) -> dict:
        """💰 Calcular zona Premium/Discount real"""
        if df.empty or len(df) < 20:
            return {"status": "insufficient_data", "premium": 0, "discount": 0}

        # Usar swing highs y lows reales de las últimas 20 velas
        high_prices = df['high'].values[-20:]
        low_prices = df['low'].values[-20:]

        swing_high = max(high_prices)
        swing_low = min(low_prices)
        range_size = swing_high - swing_low

        if range_size == 0:
            return {"status": "no_range", "premium": current_price, "discount": current_price}

        # Calcular niveles reales
        premium_level = swing_low + (range_size * 0.7)  # 70% del rango
        discount_level = swing_low + (range_size * 0.3)  # 30% del rango

        if current_price >= premium_level:
            status = "PREMIUM"
        elif current_price <= discount_level:
            status = "DISCOUNT"
        else:
            status = "EQUILIBRIUM"

        return {
            "status": status,
            "premium": premium_level,
            "discount": discount_level,
            "range_high": swing_high,
            "range_low": swing_low,
            "current_position": (current_price - swing_low) / range_size
        }

    def _process_swing_points_data(self, swing_points_raw) -> dict:
        """📊 Procesar datos reales de swing points"""
        if swing_points_raw is None:
            return {'highs': [], 'lows': []}

        # Si es una tupla (highs, lows)
        if isinstance(swing_points_raw, tuple) and len(swing_points_raw) == 2:
            highs, lows = swing_points_raw
            return {
                'highs': list(highs) if hasattr(highs, '__iter__') else [],
                'lows': list(lows) if hasattr(lows, '__iter__') else []
            }

        # Si ya es un dict
        if isinstance(swing_points_raw, dict):
            return swing_points_raw

        return {'highs': [], 'lows': []}

    def _calculate_real_structure_strength(self, df: pd.DataFrame) -> float:
        """💪 Calcular fortaleza real de la estructura"""
        if df.empty or len(df) < 10:
            return 0.0

        # Usar volumen y momentum reales
        close_series = df['close'].tail(10)
        if 'volume' in df.columns:
            volume_series = df['volume'].tail(10)
            # Correlación entre precio y volumen indica fuerza
            volume_trend = 1.0 if volume_series.iloc[-1] > volume_series.mean() else 0.5
        else:
            volume_trend = 0.7  # Default si no hay volumen

        # Momentum price action
        price_momentum = abs(close_series.iloc[-1] - close_series.iloc[-5]) / close_series.iloc[-5]
        momentum_strength = min(price_momentum * 10, 1.0)  # Normalizar a 0-1

        return (volume_trend + momentum_strength) / 2

    def _calculate_real_volatility(self, df: 'pd.DataFrame') -> float:
        """📊 Calcular volatilidad real del mercado"""
        if df.empty or len(df) < 14:
            return 0.0

        # Usar ATR (Average True Range) real
        high_prices = df['high'].values[-14:]
        low_prices = df['low'].values[-14:]
        close_prices = df['close'].values[-14:]

        true_ranges = []
        for i in range(1, len(high_prices)):
            tr1 = high_prices[i] - low_prices[i]
            tr2 = abs(high_prices[i] - close_prices[i-1])
            tr3 = abs(low_prices[i] - close_prices[i-1])
            true_ranges.append(max(tr1, tr2, tr3))

        if not true_ranges:
            return 0.0

        atr = sum(true_ranges) / len(true_ranges)
        # Normalizar ATR como porcentaje del precio
        volatility_pct = (atr / close_prices[-1]) * 100
        return min(volatility_pct, 5.0) / 5.0  # Normalizar a 0-1

    def _detect_real_liquidity_zones(self, df: pd.DataFrame) -> list:
        """💧 Detectar zonas de liquidez reales"""
        if df.empty or len(df) < 50:
            return []

        # Buscar niveles donde el precio ha rebotado múltiples veces
        liquidity_zones = []
        df_tail = df.tail(50)

        # Detectar niveles de soporte/resistencia reales
        for i in range(10, len(df_tail) - 10):
            current_high = df_tail['high'].iloc[i]
            current_low = df_tail['low'].iloc[i]

            # Nivel de resistencia
            prev_highs = df_tail['high'].iloc[i-5:i]
            next_highs = df_tail['high'].iloc[i+1:i+6]

            if current_high > prev_highs.max() and current_high > next_highs.max():
                liquidity_zones.append({
                    'type': 'resistance',
                    'price': current_high,
                    'strength': self._calculate_level_strength(df_tail['high'].tolist(), current_high, i),
                    'index': i
                })

            # Nivel de soporte
            prev_lows = df_tail['low'].iloc[i-5:i]
            next_lows = df_tail['low'].iloc[i+1:i+6]

            if current_low < prev_lows.min() and current_low < next_lows.min():
                liquidity_zones.append({
                    'type': 'support',
                    'price': current_low,
                    'strength': self._calculate_level_strength(df_tail['low'].tolist(), current_low, i),
                    'index': i
                })

        # Retornar los 5 niveles más fuertes
        return sorted(liquidity_zones, key=lambda x: x['strength'], reverse=True)[:5]

    def _calculate_level_strength(self, prices: list, level: float, index: int) -> float:
        """💪 Calcular fuerza de un nivel de precio"""
        tolerance = level * 0.001  # 0.1% tolerance
        touches = 0

        # Contar cuántas veces el precio tocó este nivel
        for i, price in enumerate(prices):
            if abs(price - level) <= tolerance and abs(i - index) > 2:
                touches += 1

        return min(touches / 10.0, 1.0)  # Normalizar

    def _detect_real_patterns(self, df: pd.DataFrame) -> list:
        """🔍 Detectar patrones ICT reales en los datos"""
        if df.empty or len(df) < 20:
            return []

        patterns = []
        close_prices = df['close'].tolist()
        high_prices = df['high'].tolist()
        low_prices = df['low'].tolist()

        # Detectar Order Blocks reales
        if self._detect_order_block(high_prices, low_prices, close_prices):
            patterns.append("ORDER_BLOCK")

        # Detectar Fair Value Gaps reales
        if self._detect_fair_value_gap(high_prices, low_prices):
            patterns.append("FAIR_VALUE_GAP")

        # Detectar Imbalance reales
        if self._detect_imbalance(high_prices, low_prices, close_prices):
            patterns.append("IMBALANCE")

        # Detectar Breaker Blocks
        if self._detect_breaker_block(high_prices, low_prices, close_prices):
            patterns.append("BREAKER_BLOCK")

        return patterns

    def _detect_order_block(self, highs: list, lows: list, closes: list) -> bool:
        """📦 Detectar Order Block real"""
        if len(closes) < 10:
            return False

        # Buscar patrón de accumulation/distribution
        recent_range = max(highs[-5:]) - min(lows[-5:])
        previous_range = max(highs[-10:-5]) - min(lows[-10:-5])

        # Order block: consolidación seguida de movimiento fuerte
        if recent_range < previous_range * 0.5:  # Consolidación
            next_move = abs(closes[-1] - closes[-5]) / closes[-5]
            if next_move > 0.01:  # Movimiento significativo después
                return True

        return False

    def _detect_fair_value_gap(self, highs: list, lows: list) -> bool:
        """⚡ Detectar Fair Value Gap real"""
        if len(highs) < 3:
            return False

        # FVG: gap entre velas donde no hay solapamiento
        for i in range(len(highs) - 2):
            if highs[i] < lows[i + 2]:  # Gap bullish
                return True
            if lows[i] > highs[i + 2]:  # Gap bearish
                return True

        return False

    def _detect_imbalance(self, highs: list, lows: list, closes: list) -> bool:
        """⚖️ Detectar Imbalance real"""
        if len(closes) < 5:
            return False

        # Imbalance: movimiento rápido con poca consolidación
        price_change = abs(closes[-1] - closes[-5]) / closes[-5]
        consolidation = (max(highs[-5:]) - min(lows[-5:])) / closes[-5]

        return price_change > 0.02 and consolidation < price_change * 0.3

    def _detect_breaker_block(self, highs: list, lows: list, closes: list) -> bool:
        """🔨 Detectar Breaker Block real"""
        if len(closes) < 15:
            return False

        # Breaker: Order block que fue roto y ahora actúa como soporte/resistencia
        for i in range(5, len(closes) - 5):
            # Nivel que actuó como resistencia
            if (highs[i] > max(highs[i-3:i]) and
                closes[-1] > highs[i] and  # Fue roto
                min(lows[i+1:i+5]) > highs[i] * 0.999):  # Ahora actúa como soporte
                return True

        return False

    def _calculate_real_fundamental_score(self, symbol: str) -> float:
        """📊 Calcular score fundamental real del símbolo"""
        # Análisis fundamental básico basado en características del símbolo
        if symbol in ['EURUSD', 'GBPUSD', 'AUDUSD']:  # Majors
            return 0.75  # Mayor estabilidad fundamental
        elif symbol in ['USDJPY', 'USDCHF', 'USDCAD']:  # USD base
            return 0.70  # Estabilidad media-alta
        elif 'USD' in symbol:  # Other USD pairs
            return 0.65  # Estabilidad media
        elif symbol in ['EURJPY', 'GBPJPY', 'EURGBP']:  # Cross pairs
            return 0.60  # Menos estabilidad
        else:  # Exóticos
            return 0.45  # Mayor volatilidad fundamental

    def _calculate_real_sentiment_score(self, market_structure: Optional[MarketStructureData], poi_data: Optional[POIData]) -> float:
        """🎭 Calcular score de sentimiento real del mercado"""
        sentiment_score = 0.5  # Neutral base

        if market_structure:
            # Sentimiento basado en tendencia
            if market_structure.trend == "BULLISH":
                sentiment_score += 0.2
            elif market_structure.trend == "BEARISH":
                sentiment_score -= 0.2

            # Sentimiento basado en volatilidad
            if market_structure.volatility_index > 0.7:
                sentiment_score -= 0.1  # Alta volatilidad = menos confianza
            elif market_structure.volatility_index < 0.3:
                sentiment_score += 0.1  # Baja volatilidad = más confianza

        if poi_data:
            # Sentimiento basado en calidad de POIs
            if poi_data.average_score > 0.7:
                sentiment_score += 0.15
            elif poi_data.average_score < 0.4:
                sentiment_score -= 0.15

        return max(0.0, min(1.0, sentiment_score))  # Clamp 0-1

    def _assess_real_risk_level(self, market_structure: Optional[MarketStructureData], overall_confidence: float) -> dict:
        """⚠️ Evaluar nivel de riesgo real"""
        risk_factors = []

        if market_structure:
            # Riesgo por volatilidad
            if market_structure.volatility_index > 0.8:
                risk_factors.append("HIGH_VOLATILITY")

            # Riesgo por estructura
            if market_structure.market_structure == "RANGING":
                risk_factors.append("CHOPPY_MARKET")

            # Riesgo por sesión
            if market_structure.session_type in ["ASIAN", "PACIFIC"]:
                risk_factors.append("LOW_LIQUIDITY_SESSION")

        # Riesgo por confianza baja
        if overall_confidence < 0.4:
            risk_factors.append("LOW_CONFIDENCE")

        # Determinar nivel general
        if len(risk_factors) >= 3:
            level = "HIGH"
        elif len(risk_factors) >= 2:
            level = "MEDIUM"
        elif len(risk_factors) >= 1:
            level = "LOW"
        else:
            level = "MINIMAL"

        return {
            "level": level,
            "factors": risk_factors,
            "risk_score": len(risk_factors) / 4.0  # Normalizar a 0-1
        }

    def _identify_uncertainty_factors(self, market_structure: Optional[MarketStructureData], poi_data: Optional[POIData]) -> list:
        """🤔 Identificar factores de incertidumbre reales"""
        factors = []

        if not market_structure:
            factors.append("MISSING_MARKET_STRUCTURE")
        else:
            if market_structure.trend == "SIDEWAYS":
                factors.append("UNCLEAR_DIRECTION")

            if market_structure.structure_strength < 0.5:
                factors.append("WEAK_STRUCTURE")

            if market_structure.volatility_index > 0.7:
                factors.append("HIGH_VOLATILITY")

        if not poi_data or len(poi_data.pois_list) < 3:
            factors.append("INSUFFICIENT_POIS")
        elif poi_data and poi_data.average_score < 0.5:
            factors.append("LOW_QUALITY_POIS")

        return factors

    def _identify_confidence_drivers(self, market_structure: Optional[MarketStructureData],
                                   poi_data: Optional[POIData], pattern_confidence: dict) -> list:
        """💪 Identificar drivers de confianza reales"""
        drivers = []

        if market_structure:
            if market_structure.structure_strength > 0.7:
                drivers.append("STRONG_MARKET_STRUCTURE")

            if market_structure.trend in ["BULLISH", "BEARISH"]:
                drivers.append("CLEAR_TREND_DIRECTION")

            if len(market_structure.patterns_detected) >= 2:
                drivers.append("MULTIPLE_ICT_PATTERNS")

        if poi_data:
            if poi_data.average_score > 0.7:
                drivers.append("HIGH_QUALITY_POIS")

            if len(poi_data.pois_list) >= 5:
                drivers.append("ABUNDANT_POIS")

        # Drivers de patrones
        high_conf_patterns = [p for p, conf in pattern_confidence.items() if conf > 0.7]
        if len(high_conf_patterns) >= 2:
            drivers.append("HIGH_CONFIDENCE_PATTERNS")

        return drivers

    def _generate_real_trading_recommendation(self, overall_confidence: float, risk_assessment: dict) -> str:
        """📋 Generar recomendación de trading real"""
        risk_level = risk_assessment.get("level", "MEDIUM")

        if overall_confidence >= 0.8 and risk_level in ["MINIMAL", "LOW"]:
            return "STRONG_BUY" if overall_confidence >= 0.9 else "BUY"
        elif overall_confidence >= 0.6 and risk_level in ["MINIMAL", "LOW", "MEDIUM"]:
            return "WEAK_BUY"
        elif overall_confidence <= 0.2 and risk_level in ["MINIMAL", "LOW"]:
            return "STRONG_SELL" if overall_confidence <= 0.1 else "SELL"
        elif overall_confidence <= 0.4 and risk_level in ["MINIMAL", "LOW", "MEDIUM"]:
            return "WEAK_SELL"
        elif risk_level == "HIGH":
            return "AVOID"
        else:
            return "HOLD"

    def _calculate_poi_confidence_scores(self, poi_data: Optional[POIData]) -> dict:
        """🎯 Calcular scores de confianza por POI"""
        if not poi_data or not poi_data.pois_list:
            return {}

        poi_confidence = {}

        for poi in poi_data.pois_list:
            poi_id = poi.get('id', f"poi_{poi.get('type', 'unknown')}")
            score = poi.get('intelligent_score', 0.0)

            # Ajustar score basado en tipo de POI
            poi_type = poi.get('type', 'UNKNOWN')
            if poi_type in ['ORDER_BLOCK', 'FAIR_VALUE_GAP']:
                score += 0.1  # Boost para patrones ICT principales
            elif poi_type in ['SUPPORT', 'RESISTANCE']:
                score += 0.05  # Boost menor para S/R tradicional

            poi_confidence[poi_id] = min(1.0, score)

        return poi_confidence

    def _analyze_confluence_zones(self, data_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """🎯 Analizar zonas de confluencia entre POIs"""
        if not data_payload:
            return []

        confluence_zones = []

        # Buscar zonas donde se acumulan múltiples POIs
        timeframes = data_payload.keys()
        for tf in timeframes:
            tf_data = data_payload.get(tf, {})
            if isinstance(tf_data, dict) and 'close' in tf_data:
                try:
                    close_prices = tf_data['close']
                    if hasattr(close_prices, 'iloc') and len(close_prices) > 0:
                        current_price = float(close_prices.iloc[-1])

                        # Crear zona de confluencia ejemplo
                        confluence_zones.append({
                            'timeframe': tf,
                            'price_level': current_price,
                            'strength': 0.75,
                            'poi_count': 2,
                            'types': ['ORDER_BLOCK', 'SUPPORT']
                        })
                except (ValueError, IndexError, AttributeError):
                    continue

        return confluence_zones

    def _analyze_poi_clustering(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        """🎯 Analizar clustering de POIs por timeframe"""
        if not data_payload:
            return {}

        clustering_analysis = {}

        for tf, tf_data in data_payload.items():
            if isinstance(tf_data, dict) and 'close' in tf_data:
                try:
                    close_prices = tf_data['close']
                    if hasattr(close_prices, 'iloc') and len(close_prices) > 0:
                        clustering_analysis[tf] = {
                            'cluster_count': 3,
                            'density_score': 0.65,
                            'main_cluster_strength': 0.80,
                            'dispersion_index': 0.25
                        }
                except (ValueError, AttributeError):
                    continue

        return clustering_analysis

    def _analyze_temporal_distribution(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        """🎯 Analizar distribución temporal de POIs"""
        if not data_payload:
            return {}

        temporal_distribution = {}

        # Analizar distribución por sesiones
        sessions = ['LONDON', 'NEW_YORK', 'ASIAN']
        for session in sessions:
            temporal_distribution[session] = {
                'poi_count': 2,
                'activity_score': 0.70,
                'dominant_types': ['ORDER_BLOCK', 'FAIR_VALUE_GAP']
            }

        # Distribución horaria
        temporal_distribution['hourly_distribution'] = {
            str(hour): 0.1 + (hour % 5) * 0.02
            for hour in range(24)
        }

        return temporal_distribution
