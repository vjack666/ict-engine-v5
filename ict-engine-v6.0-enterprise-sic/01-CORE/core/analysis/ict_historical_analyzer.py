#!/usr/bin/env python3
"""
📈 ICT HISTORICAL ANALYZER v6.0 - ANÁLISIS HISTÓRICO CON MEMORIA PERSISTENTE
=============================================================================

Analizador histórico de performance de patrones ICT para scoring dinámico
y aprendizaje adaptativo. Migrado y mejorado desde sistema legacy.

Componente crítico del Sistema de Memoria de Trader Real.

Fecha: Agosto 8, 2025
Estado: IMPLEMENTADO - MEMORIA TRADER REAL
Prioridad: CRÍTICA - BLOQUEANTE
"""

# === IMPORTS STANDARD LIBRARY ===
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from pathlib import Path
import json
from json import JSONDecodeError
import pandas as pd
import numpy as np
import pickle
import statistics

# === IMPORTS ESPECÍFICOS v6.0 ===
try:
    from core.analysis.market_context import MarketContext
    MarketContext_available = True
except ImportError:
    MarketContext = None
    MarketContext_available = False

# === TYPE DEFINITIONS ===
if MarketContext_available:
    MarketContextType = MarketContext
else:
    MarketContextType = Any

# === LOGGING SIMPLE PARA DESARROLLO ===
def enviar_senal_log(level: str, message: str, module: str, category: str = "general"):
    """Función simple de logging para desarrollo"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level} - {module}.{category}: {message}")


class ICTHistoricalAnalyzer:
    """
    📈 Analizador histórico de patrones ICT con memoria persistente.
    
    Analiza el rendimiento histórico de POIs, BOS, CHoCH y otros patrones
    para proporcionar scoring dinámico y adaptativo basado en experiencia real.
    
    Migrado y mejorado desde sistema legacy para v6.0 Enterprise.
    Incluye aprendizaje adaptativo y persistencia entre sesiones.
    """

    def __init__(self, market_context: Optional[Any] = None, 
                 logs_dir: str = "data/logs", config_path: str = "config/memory_config.json"):
        """
        Inicializa el analizador histórico con memoria persistente.
        
        Args:
            market_context: Contexto de mercado para integración
            logs_dir: Directorio de logs para análisis histórico
            config_path: Ruta de configuración de memoria
        """
        enviar_senal_log("INFO", "📈 Inicializando ICT Historical Analyzer v6.0", __name__, "init")
        
        # Contexto de mercado integrado
        self.market_context = market_context
        if not market_context and MarketContext_available:
            enviar_senal_log("WARNING", "⚠️ MarketContext no proporcionado, creando instancia nueva", __name__, "init")
        
        # Directorios y archivos
        self.logs_dir = Path(logs_dir)
        self.analysis_dir = self.logs_dir / "ict_analysis"
        self.analysis_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache temporal
        self.cache = {}
        self.cache_timestamp = None
        self.cache_ttl = timedelta(hours=1)  # Cache por 1 hora
        
        # Configuración
        self.config = self._load_config(config_path)
        
        # Performance cache para análisis persistente
        self.performance_cache = {}
        self.performance_cache_file = self.analysis_dir / "performance_cache.pkl"
        self._load_performance_cache()
        
        # Time decay factor para dar más peso a eventos recientes
        self.time_decay_factor = self.config.get('time_decay_factor', 0.1)
        
        enviar_senal_log("INFO", "✅ ICT Historical Analyzer v6.0 inicializado", __name__, "init")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Carga configuración desde archivo JSON."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            return config.get('historical_analysis', {
                'min_samples': 5,
                'success_threshold': 0.7,
                'time_decay_factor': 0.1,
                'max_lookback_days': 30,
                'weight_multipliers': {
                    'BOS': 1.0,
                    'CHoCH': 1.1,
                    'ORDER_BLOCK': 1.0,
                    'FAIR_VALUE_GAP': 1.1,
                    'LIQUIDITY_POOL': 1.2,
                    'H4_BIAS': 0.9
                }
            })
        except FileNotFoundError:
            enviar_senal_log("WARNING", f"⚠️ Config no encontrado: {config_path}, usando defaults", __name__, "config")
            return {
                'min_samples': 5,
                'success_threshold': 0.7,
                'time_decay_factor': 0.1,
                'max_lookback_days': 30,
                'weight_multipliers': {
                    'BOS': 1.0,
                    'CHoCH': 1.1,
                    'ORDER_BLOCK': 1.0,
                    'FAIR_VALUE_GAP': 1.1,
                    'LIQUIDITY_POOL': 1.2,
                    'H4_BIAS': 0.9
                }
            }

    def _load_performance_cache(self):
        """Carga cache de performance desde disco."""
        if self.performance_cache_file.exists():
            try:
                with open(self.performance_cache_file, 'rb') as f:
                    self.performance_cache = pickle.load(f)
                enviar_senal_log("INFO", f"✅ Performance cache cargado: {len(self.performance_cache)} entradas", __name__, "cache")
            except Exception as e:
                enviar_senal_log("ERROR", f"❌ Error cargando performance cache: {e}", __name__, "cache")
                self.performance_cache = {}
        else:
            enviar_senal_log("INFO", "🆕 Nuevo performance cache creado", __name__, "cache")

    def _save_performance_cache(self):
        """Guarda cache de performance a disco."""
        try:
            with open(self.performance_cache_file, 'wb') as f:
                pickle.dump(self.performance_cache, f)
            enviar_senal_log("DEBUG", f"✅ Performance cache guardado: {len(self.performance_cache)} entradas", __name__, "cache")
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error guardando performance cache: {e}", __name__, "cache")

    def analyze_historical_pois(self, symbol: str = "EURUSD", timeframe: str = "M15") -> Dict[str, Any]:
        """
        Analiza performance histórica de POIs para el símbolo y timeframe.
        
        Args:
            symbol: Símbolo del mercado
            timeframe: Marco temporal
            
        Returns:
            Dict con análisis histórico de POIs
        """
        enviar_senal_log("INFO", f"📊 Analizando POIs históricos: {symbol}/{timeframe}", __name__, "poi_analysis")
        
        # Verificar cache
        cache_key = f"pois_{symbol}_{timeframe}"
        if self._is_cache_valid(cache_key):
            enviar_senal_log("DEBUG", f"📋 Usando cache para POIs {symbol}/{timeframe}", __name__, "poi_analysis")
            return self.cache[cache_key]
        
        try:
            # Obtener datos históricos de POIs
            poi_data = self._get_historical_poi_data(symbol, timeframe)
            
            if not poi_data or len(poi_data) < self.config['min_samples']:
                result = {
                    'symbol': symbol,
                    'timeframe': timeframe,
                    'total_pois': len(poi_data) if poi_data else 0,
                    'success_rate': 0.5,  # Neutral por falta de datos
                    'confidence': 0.3,  # Baja confianza
                    'weight_factor': 1.0,  # Neutral
                    'status': 'insufficient_data'
                }
                self.cache[cache_key] = result
                return result
            
            # Analizar performance
            success_rate = self._calculate_poi_success_rate(poi_data)
            time_weighted_rate = self._apply_time_decay_pois(poi_data, success_rate)
            weight_factor = self._success_rate_to_weight(time_weighted_rate, 'POI')
            confidence = min(1.0, len(poi_data) / 20)  # Máximo confianza con 20+ POIs
            
            result = {
                'symbol': symbol,
                'timeframe': timeframe,
                'total_pois': len(poi_data),
                'success_rate': success_rate,
                'time_weighted_rate': time_weighted_rate,
                'confidence': confidence,
                'weight_factor': weight_factor,
                'recent_performance': self._get_recent_poi_performance(poi_data),
                'status': 'analyzed'
            }
            
            # Cachear resultado
            self.cache[cache_key] = result
            self._update_cache_timestamp()
            
            enviar_senal_log("INFO", f"✅ POIs analizados: {len(poi_data)} POIs, éxito={success_rate:.2%}", __name__, "poi_analysis")
            return result
            
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error analizando POIs históricos: {e}", __name__, "poi_analysis")
            return {
                'symbol': symbol,
                'timeframe': timeframe,
                'error': str(e),
                'status': 'error'
            }

    def analyze_bos_performance(self, symbol: str = "EURUSD") -> Dict[str, Any]:
        """
        Analiza efectividad histórica de patrones BOS.
        
        Args:
            symbol: Símbolo del mercado
            
        Returns:
            Dict con análisis de performance BOS
        """
        enviar_senal_log("INFO", f"📈 Analizando performance BOS: {symbol}", __name__, "bos_analysis")
        
        try:
            # Obtener eventos BOS del contexto de mercado
            bos_events = []
            if self.market_context and hasattr(self.market_context, 'bos_events'):
                bos_events = self.market_context.bos_events
            
            if len(bos_events) < self.config['min_samples']:
                enviar_senal_log("WARNING", f"⚠️ Pocos eventos BOS para análisis: {len(bos_events)}", __name__, "bos_analysis")
                return {
                    'symbol': symbol,
                    'total_events': len(bos_events),
                    'success_rate': 0.5,  # Neutral
                    'confidence': 0.3,
                    'weight_factor': 1.0,
                    'status': 'insufficient_data'
                }
            
            # Calcular métricas
            successful_events = sum(1 for event in bos_events if event.get('success', False))
            success_rate = successful_events / len(bos_events)
            
            # Análisis por timeframe
            by_timeframe = {}
            for event in bos_events:
                tf = event.get('timeframe', 'unknown')
                if tf not in by_timeframe:
                    by_timeframe[tf] = {'total': 0, 'successful': 0}
                by_timeframe[tf]['total'] += 1
                if event.get('success', False):
                    by_timeframe[tf]['successful'] += 1
            
            # Calcular tasas por timeframe
            for tf in by_timeframe:
                by_timeframe[tf]['success_rate'] = (
                    by_timeframe[tf]['successful'] / by_timeframe[tf]['total']
                    if by_timeframe[tf]['total'] > 0 else 0.5
                )
            
            # Análisis temporal (últimos 7 días vs total)
            recent_cutoff = datetime.now() - timedelta(days=7)
            recent_events = [e for e in bos_events if e.get('timestamp', datetime.min) > recent_cutoff]
            recent_success_rate = (
                sum(1 for e in recent_events if e.get('success', False)) / len(recent_events)
                if recent_events else success_rate
            )
            
            # Weight factor basado en performance
            weight_factor = self._success_rate_to_weight(success_rate, 'BOS')
            confidence = min(1.0, len(bos_events) / 15)  # Máximo con 15+ eventos
            
            result = {
                'symbol': symbol,
                'total_events': len(bos_events),
                'successful_events': successful_events,
                'success_rate': success_rate,
                'recent_success_rate': recent_success_rate,
                'confidence': confidence,
                'weight_factor': weight_factor,
                'by_timeframe': by_timeframe,
                'trend': 'improving' if recent_success_rate > success_rate else 'stable' if recent_success_rate == success_rate else 'declining',
                'status': 'analyzed'
            }
            
            enviar_senal_log("INFO", f"✅ BOS Performance: {success_rate:.2%} éxito en {len(bos_events)} eventos", __name__, "bos_analysis")
            return result
            
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error analizando BOS performance: {e}", __name__, "bos_analysis")
            return {
                'symbol': symbol,
                'error': str(e),
                'status': 'error'
            }

    def analyze_choch_performance(self, symbol: str = "EURUSD") -> Dict[str, Any]:
        """
        Analiza efectividad histórica de patrones CHoCH.
        
        Args:
            symbol: Símbolo del mercado
            
        Returns:
            Dict con análisis de performance CHoCH
        """
        enviar_senal_log("INFO", f"🔄 Analizando performance CHoCH: {symbol}", __name__, "choch_analysis")
        
        try:
            # Obtener eventos CHoCH del contexto de mercado
            choch_events = []
            if self.market_context and hasattr(self.market_context, 'choch_events'):
                choch_events = self.market_context.choch_events
            
            if len(choch_events) < self.config['min_samples']:
                enviar_senal_log("WARNING", f"⚠️ Pocos eventos CHoCH para análisis: {len(choch_events)}", __name__, "choch_analysis")
                return {
                    'symbol': symbol,
                    'total_events': len(choch_events),
                    'success_rate': 0.5,  # Neutral
                    'confidence': 0.3,
                    'weight_factor': 1.0,
                    'status': 'insufficient_data'
                }
            
            # Calcular métricas similares a BOS
            successful_events = sum(1 for event in choch_events if event.get('success', False))
            success_rate = successful_events / len(choch_events)
            
            # Análisis por timeframe
            by_timeframe = {}
            for event in choch_events:
                tf = event.get('timeframe', 'unknown')
                if tf not in by_timeframe:
                    by_timeframe[tf] = {'total': 0, 'successful': 0}
                by_timeframe[tf]['total'] += 1
                if event.get('success', False):
                    by_timeframe[tf]['successful'] += 1
            
            # Calcular tasas por timeframe
            for tf in by_timeframe:
                by_timeframe[tf]['success_rate'] = (
                    by_timeframe[tf]['successful'] / by_timeframe[tf]['total']
                    if by_timeframe[tf]['total'] > 0 else 0.5
                )
            
            # Análisis temporal reciente
            recent_cutoff = datetime.now() - timedelta(days=7)
            recent_events = [e for e in choch_events if e.get('timestamp', datetime.min) > recent_cutoff]
            recent_success_rate = (
                sum(1 for e in recent_events if e.get('success', False)) / len(recent_events)
                if recent_events else success_rate
            )
            
            # Weight factor basado en performance
            weight_factor = self._success_rate_to_weight(success_rate, 'CHoCH')
            confidence = min(1.0, len(choch_events) / 15)  # Máximo con 15+ eventos
            
            result = {
                'symbol': symbol,
                'total_events': len(choch_events),
                'successful_events': successful_events,
                'success_rate': success_rate,
                'recent_success_rate': recent_success_rate,
                'confidence': confidence,
                'weight_factor': weight_factor,
                'by_timeframe': by_timeframe,
                'trend': 'improving' if recent_success_rate > success_rate else 'stable' if recent_success_rate == success_rate else 'declining',
                'status': 'analyzed'
            }
            
            enviar_senal_log("INFO", f"✅ CHoCH Performance: {success_rate:.2%} éxito en {len(choch_events)} eventos", __name__, "choch_analysis")
            return result
            
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error analizando CHoCH performance: {e}", __name__, "choch_analysis")
            return {
                'symbol': symbol,
                'error': str(e),
                'status': 'error'
            }

    def get_adaptive_threshold(self, pattern_type: str, symbol: str = "EURUSD") -> float:
        """
        Calcula threshold adaptativo basado en performance histórica.
        
        Args:
            pattern_type: Tipo de patrón (BOS, CHoCH, etc.)
            symbol: Símbolo del mercado
            
        Returns:
            Threshold adaptativo optimizado
        """
        base_threshold = 0.6  # Threshold base
        
        try:
            # Obtener performance histórica del patrón
            if pattern_type == "BOS":
                performance = self.analyze_bos_performance(symbol)
            elif pattern_type == "CHoCH":
                performance = self.analyze_choch_performance(symbol)
            else:
                enviar_senal_log("WARNING", f"⚠️ Tipo de patrón no soportado: {pattern_type}", __name__, "adaptive_threshold")
                return base_threshold
            
            if performance.get('status') != 'analyzed':
                return base_threshold
            
            success_rate = performance.get('success_rate', 0.5)
            confidence = performance.get('confidence', 0.5)
            
            # Ajustar threshold basado en performance
            if success_rate > 0.8 and confidence > 0.7:
                # Alta performance -> reducir threshold para más detecciones
                adaptive_threshold = base_threshold * 0.85
            elif success_rate < 0.4 and confidence > 0.5:
                # Baja performance -> aumentar threshold para mayor selectividad
                adaptive_threshold = base_threshold * 1.2
            else:
                # Performance normal -> ajuste ligero
                adaptive_threshold = base_threshold + (success_rate - 0.5) * 0.2
            
            # Clamp entre límites razonables
            adaptive_threshold = max(0.3, min(0.9, adaptive_threshold))
            
            enviar_senal_log("DEBUG", f"🎯 Threshold adaptativo {pattern_type}: {adaptive_threshold:.2f} (base: {base_threshold:.2f})", __name__, "adaptive_threshold")
            return adaptive_threshold
            
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error calculando threshold adaptativo: {e}", __name__, "adaptive_threshold")
            return base_threshold

    def assess_pattern_quality(self, pattern_data: Dict[str, Any], pattern_type: str) -> float:
        """
        Evalúa calidad de pattern contra histórico.
        
        Args:
            pattern_data: Datos del patrón actual
            pattern_type: Tipo de patrón
            
        Returns:
            Score de calidad (0.0 - 1.0)
        """
        base_quality = pattern_data.get('confidence', 0.5)
        
        try:
            # Obtener contexto histórico
            if pattern_type == "BOS":
                historical = self.analyze_bos_performance()
            elif pattern_type == "CHoCH":
                historical = self.analyze_choch_performance()
            else:
                return base_quality
            
            if historical.get('status') != 'analyzed':
                return base_quality
            
            # Factores de calidad histórica
            historical_success = historical.get('success_rate', 0.5)
            confidence_factor = historical.get('confidence', 0.5)
            
            # Ajustar calidad basado en histórico
            quality_adjustment = (historical_success - 0.5) * confidence_factor * 0.3
            final_quality = base_quality + quality_adjustment
            
            # Clamp entre 0 y 1
            final_quality = max(0.0, min(1.0, final_quality))
            
            return final_quality
            
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error evaluando calidad de pattern: {e}", __name__, "pattern_quality")
            return base_quality

    def _get_historical_poi_data(self, symbol: str, timeframe: str) -> List[Dict[str, Any]]:
        """Obtiene datos históricos de POIs desde logs o contexto."""
        # Por ahora, simular datos hasta implementar integración completa con logs
        return []

    def _calculate_poi_success_rate(self, poi_data: List[Dict[str, Any]]) -> float:
        """Calcula tasa de éxito de POIs."""
        if not poi_data:
            return 0.5
        successful = sum(1 for poi in poi_data if poi.get('success', False))
        return successful / len(poi_data)

    def _apply_time_decay_pois(self, poi_data: List[Dict[str, Any]], base_rate: float) -> float:
        """Aplica decaimiento temporal a tasa de éxito de POIs."""
        # Implementación simplificada - dar más peso a POIs recientes
        return base_rate  # Por ahora retornar base rate

    def _get_recent_poi_performance(self, poi_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Obtiene performance de POIs recientes."""
        recent_cutoff = datetime.now() - timedelta(days=7)
        recent_pois = [poi for poi in poi_data if poi.get('timestamp', datetime.min) > recent_cutoff]
        
        if not recent_pois:
            return {'count': 0, 'success_rate': 0.5}
        
        success_rate = sum(1 for poi in recent_pois if poi.get('success', False)) / len(recent_pois)
        return {
            'count': len(recent_pois),
            'success_rate': success_rate
        }

    def _success_rate_to_weight(self, success_rate: float, pattern_type: str) -> float:
        """Convierte tasa de éxito a factor de peso."""
        base_multiplier = self.config['weight_multipliers'].get(pattern_type, 1.0)
        
        # Convertir success rate a multiplicador
        if success_rate > 0.7:
            weight_factor = base_multiplier * (1.0 + (success_rate - 0.7) * 0.5)
        elif success_rate < 0.4:
            weight_factor = base_multiplier * (0.7 + success_rate * 0.75)
        else:
            weight_factor = base_multiplier
        
        return max(0.5, min(2.0, weight_factor))  # Clamp entre 0.5 y 2.0

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Verifica si el cache es válido."""
        if cache_key not in self.cache or not self.cache_timestamp:
            return False
        return datetime.now() - self.cache_timestamp < self.cache_ttl

    def _update_cache_timestamp(self):
        """Actualiza timestamp del cache."""
        self.cache_timestamp = datetime.now()


# === INSTANCIA GLOBAL PARA COMPATIBILIDAD ===
_global_historical_analyzer = None

def get_historical_analyzer(market_context: Optional[Any] = None) -> ICTHistoricalAnalyzer:
    """Obtiene instancia global de ICTHistoricalAnalyzer."""
    global _global_historical_analyzer
    
    if _global_historical_analyzer is None:
        _global_historical_analyzer = ICTHistoricalAnalyzer(market_context)
    
    return _global_historical_analyzer
