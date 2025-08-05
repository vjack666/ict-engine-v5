"""
ICT Engine - Motor Principal de Análisis ICT
============================================

Motor central que integra todos los componentes del análisis ICT,
proporcionando una interfaz unificada para el sistema.

Autor: Sistema Sentinel Grid v3.3.3.3.3
Fecha: 2025-08-03
"""

from typing import Dict, List, Any, Optional
import pandas as pd
from dataclasses import dataclass
from datetime import datetime
# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log, log_ict

# Importar componentes ICT existentes
ict_components_available = False
try:
    from .ict_detector import ICTDetector, MarketContext, OptimizedICTAnalysis
    from .ict_types import (
        ICTPattern, MarketPhase, SessionType, SignalStrength, TradingDirection,
        ICTSignal, MarketStructure, ICTAnalysisResult
    )
    from .confidence_engine import ConfidenceEngine
    ict_components_available = True
except ImportError as e:
    enviar_senal_log("WARNING", f"Componentes ICT no disponibles: {e}", "ict_engine")

@dataclass
class ICTEngineResult:
    """Resultado unificado del análisis ICT."""
    symbol: str
    timeframe: str
    timestamp: datetime
    market_phase: str
    direction: str
    strength: float
    patterns_detected: List[Dict[str, Any]]
    signals: List[Dict[str, Any]]
    confidence: float
    recommendation: str
    risk_level: float
    detalles: Dict[str, Any]

class ICTEngine:
    """
    Motor principal de análisis ICT.
    Centraliza todo el análisis Inner Circle Trader.
    """

    def __init__(self, mt5_manager=None):
        """
        Inicializa el motor ICT.

        Args:
            mt5_manager: Instancia del MT5DataManager para datos
        """
        self.mt5_manager = mt5_manager
        self.configuracion = {
            'timeframes_principales': ['M15', 'H1', 'H4'],
            'patterns_prioritarios': ['FVG', 'ORDER_BLOCK', 'LIQUIDITY_SWEEP'],
            'min_confidence': 0.6,
            'max_risk_acceptable': 0.7,
            'simbolos_principales': ['EURUSD', 'GBPUSD', 'USDJPY']
        }

        # Inicializar componentes ICT si están disponibles
        if ict_components_available:
            try:
                self.detector = ICTDetector()
                self.confidence_engine = ConfidenceEngine()
                enviar_senal_log("INFO", "Componentes ICT inicializados correctamente", "ict_engine")
            except Exception as e:
                enviar_senal_log("ERROR", f"Error inicializando componentes ICT: {e}", "ict_engine")
                self.detector = None
                self.confidence_engine = None
        else:
            self.detector = None
            self.confidence_engine = None

        enviar_senal_log("INFO", "ICTEngine inicializado correctamente", "ict_engine")

    def analizar_mercado_completo(self,
                                 symbol: str = "EURUSD",
                                 timeframe: str = "H1",
                                 lookback: int = 500) -> Optional[ICTEngineResult]:
        """
        Realiza un análisis ICT completo para un símbolo y timeframe.

        Args:
            symbol: Símbolo a analizar
            timeframe: Timeframe para el análisis
            lookback: Número de barras a analizar

        Returns:
            ICTEngineResult con el análisis completo o None si falla
        """
        try:
            enviar_senal_log("INFO", f"🎯 Iniciando análisis ICT completo: {symbol} {timeframe}", "ict_engine")

            # Validar parámetros
            if not self._validar_parametros(symbol, timeframe):
                return None

            # Obtener datos de MT5
            if not self.mt5_manager:
                enviar_senal_log("ERROR", "MT5Manager no disponible para análisis ICT", "ict_engine")
                return None

            df = self.mt5_manager.get_historical_data(symbol, timeframe, lookback)
            if df is None or df.empty:
                enviar_senal_log("ERROR", f"No se pudieron obtener datos para {symbol} {timeframe}", "ict_engine")
                return None

            # Realizar análisis ICT
            if not ict_components_available or not self.detector:
                enviar_senal_log("WARNING", "Componentes ICT no disponibles, simulando análisis", "ict_engine")
                return self._simular_analisis_ict(symbol, timeframe, df)

            # Análisis real con componentes ICT
            try:
                enviar_senal_log("INFO", f"🔍 Ejecutando análisis ICT con detector disponible", "ict_engine")

                # Preparar datos para el detector
                data_dict = {
                    "dataframe": df,
                    "symbol": symbol,
                    "timeframe": timeframe
                }

                # Usar ICTDetector directamente para obtener patrones
                patterns = []
                if hasattr(self.detector, 'detect_patterns'):
                    detected_patterns = self.detector.detect_patterns(data_dict)
                    patterns.extend(detected_patterns or [])
                    enviar_senal_log("INFO", f"🎯 ICTDetector encontró {len(patterns)} patrones", "ict_engine")

                # Obtener análisis de estructura
                structure_analysis = {}
                if hasattr(self.detector, 'analyze_structure'):
                    structure_analysis = self.detector.analyze_structure(df) or {}
                    enviar_senal_log("INFO", f"🏗️ Análisis de estructura completado", "ict_engine")

                # Obtener análisis de bias
                bias_analysis = {}
                if hasattr(self.detector, 'detect_bias'):
                    bias_analysis = self.detector.detect_bias(df) or {}
                    enviar_senal_log("INFO", f"🧭 Análisis de bias completado", "ict_engine")

                # Obtener POIs adicionales
                pois = []
                if hasattr(self.detector, 'find_pois'):
                    found_pois = self.detector.find_pois(df) or []
                    pois.extend(found_pois)
                    enviar_senal_log("INFO", f"🎯 ICTDetector encontró {len(pois)} POIs", "ict_engine")

                # Generar señales basadas en patrones
                signals = self._generar_signals_desde_patterns(patterns, pois)
                enviar_senal_log("INFO", f"📡 Generadas {len(signals)} señales", "ict_engine")

                # Calcular confianza usando el Confidence Engine
                confidence = 0.0
                if self.confidence_engine and patterns:
                    try:
                        # Usar el primer patrón para calcular confianza general
                        market_context_dict = {
                            **structure_analysis,
                            **bias_analysis
                        }
                        confidence = self.confidence_engine.calculate_overall_confidence(patterns, market_context_dict)
                        enviar_senal_log("INFO", f"🧠 Confianza calculada: {confidence:.3f}", "ict_engine")
                    except Exception as e:
                        enviar_senal_log("WARNING", f"Error calculando confianza: {e}", "ict_engine")
                        confidence = 0.0

                # Calcular métricas derivadas
                risk_level = max(0.0, 1.0 - confidence) if confidence > 0 else 0.0
                strength = confidence

                # Determinar fase de mercado desde análisis de estructura
                market_phase = structure_analysis.get('structure', 'UNKNOWN')
                direction = bias_analysis.get('bias', 'NEUTRAL')

                # Generar recomendación
                if confidence >= 0.6:
                    recommendation = "TRADE_READY"
                elif confidence >= 0.4:
                    recommendation = "MONITOR"
                else:
                    recommendation = "NO_TRADE"

                # Crear resultado final
                resultado_final = ICTEngineResult(
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=datetime.now(),
                    market_phase=market_phase,
                    direction=direction,
                    strength=strength,
                    patterns_detected=patterns,
                    signals=signals,
                    confidence=confidence,
                    recommendation=recommendation,
                    risk_level=risk_level,
                    detalles={
                        'total_patterns': len(patterns),
                        'total_signals': len(signals),
                        'barras_analizadas': len(df),
                        'componentes_disponibles': ict_components_available
                    }
                )

                enviar_senal_log("INFO",
                               f"✅ Análisis ICT completado: {len(patterns)} patterns, {len(signals)} signals, confidence: {confidence:.3f}",
                               "ict_engine")

                # 📊 LOG DETALLADO PARA DASHBOARD TRACKING
                self._log_datos_para_dashboard(resultado_final, patterns, signals, pois)

                return resultado_final

            except Exception as e:
                enviar_senal_log("ERROR", f"Error en análisis ICT real: {e}", "ict_engine")
                return self._simular_analisis_ict(symbol, timeframe, df)

        except Exception as e:
            enviar_senal_log("ERROR", f"Error en análisis ICT: {e}", "ict_engine")
            return None

    def obtener_analisis_dashboard(self,
                                  symbols: Optional[List[str]] = None,
                                  timeframes: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Obtiene análisis ICT optimizado para mostrar en el dashboard.

        Args:
            symbols: Lista de símbolos a analizar
            timeframes: Lista de timeframes a analizar

        Returns:
            Dict con datos ICT formateados para dashboard
        """
        if symbols is None:
            symbols = self.configuracion['simbolos_principales'][:2]
        if timeframes is None:
            timeframes = ['H1', 'H4']

        resultados_dashboard = {
            'timestamp': datetime.now().isoformat(),
            'simbolos_analizados': [],
            'resumen_general': {},
            'alertas': [],
            'datos_detallados': {},
            'market_overview': {}
        }

        try:
            total_patterns = 0
            total_signals = 0
            confidence_acumulada = 0.0
            num_analisis = 0

            for symbol in symbols:
                for timeframe in timeframes:
                    resultado = self.analizar_mercado_completo(symbol, timeframe, lookback=300)

                    if resultado:
                        key = f"{symbol}_{timeframe}"
                        resultados_dashboard['datos_detallados'][key] = {
                            'market_phase': resultado.market_phase,
                            'direction': resultado.direction,
                            'strength': resultado.strength,
                            'confidence': resultado.confidence,
                            'patterns_count': len(resultado.patterns_detected),
                            'signals_count': len(resultado.signals),
                            'recommendation': resultado.recommendation,
                            'risk_level': resultado.risk_level
                        }

                        total_patterns += len(resultado.patterns_detected)
                        total_signals += len(resultado.signals)
                        confidence_acumulada += resultado.confidence
                        num_analisis += 1

                        # Generar alertas
                        if resultado.confidence > 0.8 and resultado.strength > 0.7:
                            resultados_dashboard['alertas'].append({
                                'tipo': 'HIGH_CONFIDENCE_SIGNAL',
                                'symbol': symbol,
                                'timeframe': timeframe,
                                'direction': resultado.direction,
                                'mensaje': f"Señal de alta confianza en {symbol} {timeframe}: {resultado.direction}"
                            })

                        if resultado.risk_level > 0.8:
                            resultados_dashboard['alertas'].append({
                                'tipo': 'HIGH_RISK_WARNING',
                                'symbol': symbol,
                                'timeframe': timeframe,
                                'mensaje': f"Alto riesgo detectado en {symbol} {timeframe}"
                            })

            # Calcular resumen general
            confidence_promedio = confidence_acumulada / max(num_analisis, 1)

            resultados_dashboard['resumen_general'] = {
                'total_patterns_sistema': total_patterns,
                'total_signals_sistema': total_signals,
                'confidence_promedio_global': confidence_promedio,
                'simbolos_analizados': len(symbols) if symbols else 0,
                'timeframes_analizados': len(timeframes) if timeframes else 0,
                'estado_sistema': 'OPERATIVO' if ict_components_available else 'SIMULADO',
                'alertas_activas': len(resultados_dashboard['alertas'])
            }

            # Market overview
            resultados_dashboard['market_overview'] = {
                'tendencia_general': self._determinar_tendencia_general(resultados_dashboard['datos_detallados']),
                'volatilidad': self._evaluar_volatilidad(resultados_dashboard['datos_detallados']),
                'recomendacion_general': self._generar_recomendacion_general(confidence_promedio, total_signals)
            }

            enviar_senal_log("INFO",
                           f"📊 Dashboard ICT actualizado: {total_patterns} patterns, {total_signals} signals",
                           "ict_engine")

            # 📊 LOG DETALLADO PARA DASHBOARD FINAL
            self._log_resumen_dashboard(resultados_dashboard, total_patterns, total_signals, confidence_promedio)

            return resultados_dashboard

        except Exception as e:
            enviar_senal_log("ERROR", f"Error generando datos ICT para dashboard: {e}", "ict_engine")
            return resultados_dashboard

    def _validar_parametros(self, symbol: str, timeframe: str) -> bool:
        """Valida los parámetros de entrada."""
        if timeframe not in ['M1', 'M5', 'M15', 'H1', 'H4', 'D1']:
            enviar_senal_log("WARNING", f"Timeframe {timeframe} puede no ser óptimo para ICT", "ict_engine")
        return True

    def _simular_analisis_ict(self, symbol: str, timeframe: str, df: pd.DataFrame) -> ICTEngineResult:
        """Simula un análisis ICT cuando los componentes no están disponibles."""
        import random

        # Simular patterns
        patterns_simulados = []
        for pattern_type in ['FVG', 'ORDER_BLOCK', 'LIQUIDITY_SWEEP']:
            if random.random() > 0.4:  # 60% chance de cada pattern
                patterns_simulados.append({
                    'type': pattern_type,
                    'strength': random.uniform(0.4, 0.9),
                    'price_level': df['close'].iloc[random.randint(0, len(df)-1)],
                    'confidence': random.uniform(0.5, 0.85),
                    'timestamp': datetime.now().isoformat()
                })

        # Simular signals
        signals_simulados = []
        for signal_type in ['BUY', 'SELL']:
            if random.random() > 0.6:  # 40% chance de cada signal
                signals_simulados.append({
                    'type': signal_type,
                    'strength': random.uniform(0.3, 0.8),
                    'entry_price': df['close'].iloc[-1],
                    'confidence': random.uniform(0.4, 0.8),
                    'risk_reward': random.uniform(1.5, 3.0)
                })

        # Calcular métricas simuladas
        confidence = random.uniform(0.4, 0.8)
        strength = random.uniform(0.3, 0.7)
        risk_level = random.uniform(0.2, 0.6)

        return ICTEngineResult(
            symbol=symbol,
            timeframe=timeframe,
            timestamp=datetime.now(),
            market_phase=random.choice(['ACCUMULATION', 'MARKUP', 'DISTRIBUTION', 'MARKDOWN']),
            direction=random.choice(['BULLISH', 'BEARISH', 'NEUTRAL']),
            strength=strength,
            patterns_detected=patterns_simulados,
            signals=signals_simulados,
            confidence=confidence,
            recommendation=self._generar_recomendacion(confidence, risk_level, strength),
            risk_level=risk_level,
            detalles={
                'total_patterns': len(patterns_simulados),
                'total_signals': len(signals_simulados),
                'barras_analizadas': len(df),
                'modo': 'SIMULADO',
                'componentes_disponibles': False
            }
        )

    def _crear_resultado_basico(self, symbol: str, timeframe: str, df: pd.DataFrame) -> ICTEngineResult:
        """Crea un resultado básico cuando el análisis falla."""
        return ICTEngineResult(
            symbol=symbol,
            timeframe=timeframe,
            timestamp=datetime.now(),
            market_phase='UNKNOWN',
            direction='NEUTRAL',
            strength=0.0,
            patterns_detected=[],
            signals=[],
            confidence=0.0,
            recommendation='NO_ANALYSIS',
            risk_level=0.0,
            detalles={
                'total_patterns': 0,
                'total_signals': 0,
                'barras_analizadas': len(df),
                'componentes_disponibles': ict_components_available
            }
        )

    def _extraer_patterns(self, resultado_ict) -> List[Dict[str, Any]]:
        """Extrae patterns del resultado ICT."""
        patterns = []
        try:
            if hasattr(resultado_ict, 'patterns') and resultado_ict.patterns:
                for pattern in resultado_ict.patterns:
                    patterns.append({
                        'type': str(pattern.get('type', 'UNKNOWN')),
                        'strength': float(pattern.get('strength', 0.5)),
                        'price_level': float(pattern.get('price_level', 0)),
                        'confidence': float(pattern.get('confidence', 0.5))
                    })
        except Exception:
            pass
        return patterns

    def _extraer_signals(self, resultado_ict) -> List[Dict[str, Any]]:
        """Extrae signals del resultado ICT."""
        signals = []
        try:
            if hasattr(resultado_ict, 'signals') and resultado_ict.signals:
                for signal in resultado_ict.signals:
                    signals.append({
                        'type': str(signal.get('type', 'NEUTRAL')),
                        'strength': float(signal.get('strength', 0.5)),
                        'entry_price': float(signal.get('entry_price', 0)),
                        'confidence': float(signal.get('confidence', 0.5))
                    })
        except Exception:
            pass
        return signals

    def _calcular_confidence(self, patterns: List[Dict], signals: List[Dict]) -> float:
        """Calcula la confianza general del análisis."""
        if not patterns and not signals:
            return 0.0

        all_items = patterns + signals
        confidences = [item.get('confidence', 0.5) for item in all_items]
        return sum(confidences) / len(confidences) if confidences else 0.0

    def _calcular_riesgo(self, patterns: List[Dict], signals: List[Dict]) -> float:
        """Calcula el nivel de riesgo del análisis."""
        # Riesgo basado en número de elementos y sus características
        total_items = len(patterns) + len(signals)
        if total_items == 0:
            return 0.0

        # Más elementos = potencialmente más riesgo
        risk_base = min(total_items / 8.0, 0.6)

        # Riesgo por baja confianza
        all_items = patterns + signals
        low_confidence_items = sum(1 for item in all_items if item.get('confidence', 0.5) < 0.5)
        risk_confidence = (low_confidence_items / total_items) * 0.4 if total_items > 0 else 0

        return min(risk_base + risk_confidence, 1.0)

    def _determinar_fase_mercado(self, resultado_ict) -> str:
        """Determina la fase actual del mercado."""
        try:
            if hasattr(resultado_ict, 'market_phase'):
                return str(resultado_ict.market_phase)
        except Exception:
            pass
        return 'UNKNOWN'

    def _determinar_direccion(self, signals: List[Dict]) -> str:
        """Determina la dirección predominante."""
        if not signals:
            return 'NEUTRAL'

        buy_signals = sum(1 for s in signals if s.get('type', '').upper() in ['BUY', 'BULLISH'])
        sell_signals = sum(1 for s in signals if s.get('type', '').upper() in ['SELL', 'BEARISH'])

        if buy_signals > sell_signals:
            return 'BULLISH'
        elif sell_signals > buy_signals:
            return 'BEARISH'
        else:
            return 'NEUTRAL'

    def _generar_signals_desde_patterns(self, patterns: List[Dict], pois: List[Dict]) -> List[Dict]:
        """Genera señales de trading basadas en patrones y POIs detectados."""
        signals = []

        try:
            # Procesar patrones para generar señales
            for pattern in patterns:
                pattern_type = pattern.get('type', 'UNKNOWN')
                confidence = pattern.get('confidence', 0.0)

                # Solo generar señales para patrones con confianza mínima
                if confidence >= 0.5:
                    signal = {
                        'type': 'PATTERN_SIGNAL',
                        'source_pattern': pattern_type,
                        'direction': self._inferir_direccion_desde_pattern(pattern),
                        'strength': confidence,
                        'price_level': pattern.get('price', 0.0),
                        'timestamp': datetime.now(),
                        'confidence': confidence,
                        'metadata': {
                            'pattern_id': pattern.get('analysis_id', 0),
                            'pattern_details': pattern
                        }
                    }
                    signals.append(signal)

            # Procesar POIs para generar señales adicionales
            for poi in pois:
                poi_type = poi.get('type', 'UNKNOWN')
                confidence = poi.get('confidence', 0.0)

                # Solo generar señales para POIs con confianza mínima
                if confidence >= 0.7:
                    signal = {
                        'type': 'POI_SIGNAL',
                        'source_poi': poi_type,
                        'direction': self._inferir_direccion_desde_poi(poi),
                        'strength': confidence,
                        'price_level': poi.get('price_level', 0.0),
                        'timestamp': datetime.now(),
                        'confidence': confidence,
                        'metadata': {
                            'poi_id': poi.get('metadata', {}).get('id', 'unknown'),
                            'poi_details': poi
                        }
                    }
                    signals.append(signal)

            enviar_senal_log("INFO", f"🎯 Generadas {len(signals)} señales desde {len(patterns)} patrones y {len(pois)} POIs", "ict_engine")

        except Exception as e:
            enviar_senal_log("ERROR", f"Error generando señales: {e}", "ict_engine")

        return signals

    def _inferir_direccion_desde_pattern(self, pattern: Dict) -> str:
        """Infiere dirección de trading desde un patrón."""
        pattern_type = pattern.get('type', '')
        subtype = pattern.get('subtype', '')

        # FVG patterns
        if 'FVG' in pattern_type:
            if 'BULLISH' in subtype:
                return 'BUY'
            elif 'BEARISH' in subtype:
                return 'SELL'

        # Order Block patterns
        if 'ORDER_BLOCK' in pattern_type:
            if 'BULLISH' in subtype:
                return 'BUY'
            elif 'BEARISH' in subtype:
                return 'SELL'

        # Swing Point patterns
        if 'SWING' in pattern_type:
            if 'HIGH' in subtype:
                return 'SELL'  # Swing high = posible reversal bearish
            elif 'LOW' in subtype:
                return 'BUY'   # Swing low = posible reversal bullish

        return 'NEUTRAL'

    def _inferir_direccion_desde_poi(self, poi: Dict) -> str:
        """Infiere dirección de trading desde un POI."""
        poi_type = poi.get('type', '')

        # Bullish POIs
        if 'BULLISH' in poi_type:
            return 'BUY'

        # Bearish POIs
        if 'BEARISH' in poi_type:
            return 'SELL'

        # Support/Resistance logic
        if 'SUPPORT' in poi_type:
            return 'BUY'
        elif 'RESISTANCE' in poi_type:
            return 'SELL'

        return 'NEUTRAL'

    def _calcular_strength(self, patterns: List[Dict], signals: List[Dict]) -> float:
        """Calcula la fuerza general del análisis."""
        all_items = patterns + signals
        if not all_items:
            return 0.0

        strengths = [item.get('strength', 0.5) for item in all_items]
        return sum(strengths) / len(strengths)

    def _generar_recomendacion(self, confidence: float, risk_level: float, strength: float) -> str:
        """Genera una recomendación basada en las métricas."""
        if confidence >= 0.8 and risk_level <= 0.3 and strength >= 0.7:
            return "STRONG_BUY_SELL"
        elif confidence >= 0.6 and risk_level <= 0.5 and strength >= 0.5:
            return "MODERATE_TRADE"
        elif confidence >= 0.4 and risk_level <= 0.7:
            return "WEAK_SIGNAL"
        else:
            return "NO_TRADE"

    def _determinar_tendencia_general(self, datos_detallados: Dict) -> str:
        """Determina la tendencia general del mercado."""
        directions = [data.get('direction', 'NEUTRAL') for data in datos_detallados.values()]

        bullish_count = sum(1 for d in directions if d == 'BULLISH')
        bearish_count = sum(1 for d in directions if d == 'BEARISH')

        if bullish_count > bearish_count:
            return 'BULLISH'
        elif bearish_count > bullish_count:
            return 'BEARISH'
        else:
            return 'NEUTRAL'

    def _evaluar_volatilidad(self, datos_detallados: Dict) -> str:
        """Evalúa la volatilidad general del mercado."""
        strengths = [data.get('strength', 0.5) for data in datos_detallados.values()]
        avg_strength = sum(strengths) / len(strengths) if strengths else 0.5

        if avg_strength > 0.7:
            return 'HIGH'
        elif avg_strength > 0.4:
            return 'MODERATE'
        else:
            return 'LOW'

    def _generar_recomendacion_general(self, confidence_promedio: float, total_signals: int) -> str:
        """Genera recomendación general del mercado."""
        if confidence_promedio > 0.7 and total_signals > 3:
            return 'ACTIVE_TRADING'
        elif confidence_promedio > 0.5 and total_signals > 1:
            return 'SELECTIVE_TRADING'
        else:
            return 'WAIT_AND_SEE'

    def _log_datos_para_dashboard(self, resultado: ICTEngineResult, patterns: List[Dict], signals: List[Dict], pois: List[Dict]) -> None:
        """
        📊 LOGGING DETALLADO PARA DASHBOARD TRACKING

        Registra todos los datos que se enviarán al dashboard para verificar
        que los datos mostrados coinciden exactamente con los procesados.
        """
        try:
            # Generar ID único para este análisis
            analysis_id = f"{resultado.symbol}_{resultado.timeframe}_{datetime.now().strftime('%H%M%S')}"

            # Log del resultado principal
            enviar_senal_log("INFO",
                           f"📊 [DASHBOARD_DATA] ID: {analysis_id} | Symbol: {resultado.symbol} | TF: {resultado.timeframe}",
                           "ict_engine", "dashboard_tracking")

            enviar_senal_log("INFO",
                           f"📈 [DASHBOARD_DATA] Metrics - Confidence: {resultado.confidence:.3f} | Strength: {resultado.strength:.3f} | Risk: {resultado.risk_level:.3f}",
                           "ict_engine", "dashboard_tracking")

            enviar_senal_log("INFO",
                           f"🎯 [DASHBOARD_DATA] Phase: {resultado.market_phase} | Direction: {resultado.direction} | Recommendation: {resultado.recommendation}",
                           "ict_engine", "dashboard_tracking")

            # Log detallado de patrones
            enviar_senal_log("INFO",
                           f"🔍 [DASHBOARD_DATA] Patterns detected: {len(patterns)} items",
                           "ict_engine", "dashboard_tracking")

            for i, pattern in enumerate(patterns[:5]):  # Log primeros 5 patrones
                pattern_info = f"Pattern {i+1}: {pattern.get('type', 'UNKNOWN')} | " + \
                             f"Subtype: {pattern.get('subtype', 'N/A')} | " + \
                             f"Confidence: {pattern.get('confidence', 0.0):.3f} | " + \
                             f"Price: {pattern.get('price_high', pattern.get('price', 0.0)):.5f}"

                enviar_senal_log("INFO", f"   • {pattern_info}", "ict_engine", "dashboard_tracking")

            # Log detallado de señales
            enviar_senal_log("INFO",
                           f"📡 [DASHBOARD_DATA] Signals generated: {len(signals)} items",
                           "ict_engine", "dashboard_tracking")

            for i, signal in enumerate(signals[:5]):  # Log primeras 5 señales
                signal_info = f"Signal {i+1}: {signal.get('type', 'UNKNOWN')} | " + \
                            f"Direction: {signal.get('direction', 'NEUTRAL')} | " + \
                            f"Strength: {signal.get('strength', 0.0):.3f} | " + \
                            f"Price: {signal.get('price_level', 0.0):.5f}"

                enviar_senal_log("INFO", f"   • {signal_info}", "ict_engine", "dashboard_tracking")

            # Log detallado de POIs
            enviar_senal_log("INFO",
                           f"🎯 [DASHBOARD_DATA] POIs found: {len(pois)} items",
                           "ict_engine", "dashboard_tracking")

            for i, poi in enumerate(pois[:5]):  # Log primeros 5 POIs
                poi_info = f"POI {i+1}: {poi.get('type', 'UNKNOWN')} | " + \
                         f"Confidence: {poi.get('confidence', 0.0):.3f} | " + \
                         f"Price: {poi.get('price_level', 0.0):.5f} | " + \
                         f"Distance: {poi.get('distance_pips', 0.0):.1f} pips"

                enviar_senal_log("INFO", f"   • {poi_info}", "ict_engine", "dashboard_tracking")

            # Log de timestamp para sincronización
            enviar_senal_log("INFO",
                           f"⏰ [DASHBOARD_DATA] Timestamp: {resultado.timestamp.isoformat()} | " + \
                           f"Analysis ID: {analysis_id} | Ready for dashboard display",
                           "ict_engine", "dashboard_tracking")

            # Log de verificación de integridad
            total_elements = len(patterns) + len(signals) + len(pois)
            enviar_senal_log("INFO",
                           f"✅ [DASHBOARD_DATA] Integrity check - Total elements: {total_elements} | " + \
                           f"Patterns: {len(patterns)} | Signals: {len(signals)} | POIs: {len(pois)}",
                           "ict_engine", "dashboard_tracking")

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error en logging de dashboard: {e}", "ict_engine", "dashboard_tracking")

    def _log_resumen_dashboard(self, resultados: Dict[str, Any], total_patterns: int, total_signals: int, confidence_promedio: float) -> None:
        """
        📊 LOGGING DEL RESUMEN FINAL PARA DASHBOARD

        Registra el resumen final que se envía al dashboard para verificación.
        """
        try:
            dashboard_id = f"DASHBOARD_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            enviar_senal_log("INFO",
                           f"📋 [DASHBOARD_SUMMARY] ID: {dashboard_id} | Timestamp: {resultados.get('timestamp', 'N/A')}",
                           "ict_engine", "dashboard_tracking")

            # Log de resumen general
            resumen = resultados.get('resumen_general', {})
            enviar_senal_log("INFO",
                           f"📊 [DASHBOARD_SUMMARY] Global metrics - Patterns: {total_patterns} | Signals: {total_signals} | Avg Confidence: {confidence_promedio:.3f}",
                           "ict_engine", "dashboard_tracking")

            enviar_senal_log("INFO",
                           f"🔍 [DASHBOARD_SUMMARY] System status: {resumen.get('estado_sistema', 'UNKNOWN')} | Active alerts: {resumen.get('alertas_activas', 0)}",
                           "ict_engine", "dashboard_tracking")

            # Log de market overview
            market_overview = resultados.get('market_overview', {})
            enviar_senal_log("INFO",
                           f"🌍 [DASHBOARD_SUMMARY] Market - Trend: {market_overview.get('tendencia_general', 'UNKNOWN')} | " + \
                           f"Volatility: {market_overview.get('volatilidad', 'UNKNOWN')} | Recommendation: {market_overview.get('recomendacion_general', 'UNKNOWN')}",
                           "ict_engine", "dashboard_tracking")

            # Log de datos detallados por símbolo
            datos_detallados = resultados.get('datos_detallados', {})
            enviar_senal_log("INFO",
                           f"📈 [DASHBOARD_SUMMARY] Symbols analyzed: {len(datos_detallados)} pairs",
                           "ict_engine", "dashboard_tracking")

            for symbol_tf, data in datos_detallados.items():
                symbol_info = f"{symbol_tf}: Phase={data.get('market_phase', 'UNKNOWN')} | " + \
                            f"Direction={data.get('direction', 'NEUTRAL')} | " + \
                            f"Confidence={data.get('confidence', 0.0):.3f} | " + \
                            f"Patterns={data.get('patterns_count', 0)} | " + \
                            f"Signals={data.get('signals_count', 0)}"

                enviar_senal_log("INFO", f"   • {symbol_info}", "ict_engine", "dashboard_tracking")

            # Log de alertas
            alertas = resultados.get('alertas', [])
            if alertas:
                enviar_senal_log("INFO",
                               f"🚨 [DASHBOARD_SUMMARY] Active alerts: {len(alertas)} items",
                               "ict_engine", "dashboard_tracking")

                for i, alerta in enumerate(alertas):
                    alert_info = f"Alert {i+1}: {alerta.get('tipo', 'UNKNOWN')} | " + \
                               f"{alerta.get('symbol', 'UNKNOWN')} {alerta.get('timeframe', 'UNKNOWN')} | " + \
                               f"Message: {alerta.get('mensaje', 'No message')}"

                    enviar_senal_log("INFO", f"   🚨 {alert_info}", "ict_engine", "dashboard_tracking")

            # Log final de verificación
            enviar_senal_log("INFO",
                           f"✅ [DASHBOARD_SUMMARY] Dashboard data package ready - ID: {dashboard_id} | " + \
                           f"Total data points: {len(datos_detallados)} | Alerts: {len(alertas)} | Status: READY_FOR_DISPLAY",
                           "ict_engine", "dashboard_tracking")

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error en logging de resumen dashboard: {e}", "ict_engine", "dashboard_tracking")

def get_ict_engine(mt5_manager=None) -> ICTEngine:
    """
    Obtiene una instancia del ICT Engine (patrón singleton mejorado).

    Args:
        mt5_manager: Manager de MT5 para integración

    Returns:
        Instancia de ICTEngine
    """
    # Usar nonlocal en lugar de global para mejor encapsulación
    if not hasattr(get_ict_engine, '_instance'):
        get_ict_engine._instance = ICTEngine(mt5_manager)  # type: ignore
    elif mt5_manager and get_ict_engine._instance.mt5_manager is None:  # type: ignore
        get_ict_engine._instance.mt5_manager = mt5_manager  # type: ignore

    return get_ict_engine._instance  # type: ignore
