#!/usr/bin/env python3
"""
🧠 MARKET CONTEXT v6.0 - MEMORIA CENTRAL DEL MERCADO
=====================================================

Memoria central del mercado como trader real con experiencia.
Migrado y mejorado desde sistema legacy para ICT Engine v6.1.0 Enterprise.

Componente crítico del Sistema de Memoria de Trader Real.

Fecha: Agosto 8, 2025
Estado: IMPLEMENTADO - MEMORIA TRADER REAL
Prioridad: CRÍTICA - BLOQUEANTE
"""

# === IMPORTS STANDARD LIBRARY ===
from typing import Dict, Any, Optional, List, Tuple, Union
from datetime import datetime, timezone
import json
from json import JSONDecodeError
import pandas as pd
import numpy as np
from pathlib import Path
import pickle
import hashlib

# === IMPORTS ESPECÍFICOS v6.0 ===
try:
    from core.smart_trading_logger import SmartTradingLogger
    SmartTradingLogger_available = True
except ImportError:
    SmartTradingLogger = None
    SmartTradingLogger_available = False

# === LOGGING SIMPLE PARA DESARROLLO ===
def enviar_senal_log(level: str, message: str, module: str, category: str = "general"):
    """Función simple de logging para desarrollo"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level} - {module}.{category}: {message}")


class MarketContext:
    """
    🧠 Memoria central del mercado como trader real experimentado.
    
    Esta clase mantiene el estado persistente del mercado (la "memoria" del trader),
    permitiendo al sistema funcionar como un trader real con experiencia histórica
    y contexto acumulado.
    
    Migrado y mejorado desde sistema legacy para v6.0 Enterprise.
    Incluye persistencia entre sesiones y aprendizaje adaptativo.
    """

    def __init__(self, config_path: str = "config/memory_config.json"):
        """Inicializa el contexto del mercado con memoria persistente."""
        enviar_senal_log("INFO", "🧠 Inicializando Market Context v6.0 - Memoria Trader Real", __name__, "memory_init")
        
        # Cargar configuración de memoria
        self.config = self._load_memory_config(config_path)
        
        # === INFORMACIÓN BÁSICA DEL MERCADO ===
        self.current_price = 0.0
        self.symbol = "EURUSD"  # Default symbol
        self.last_update = datetime.now()
        
        # === BIAS DE TIMEFRAMES CON HISTORIA ===
        self.h4_bias = "NEUTRAL"
        self.m15_bias = "NEUTRAL" 
        self.bias_history = []  # Historia de cambios de bias
        self.bias_confidence = 0.5  # Confianza en el bias actual
        
        # === RANGOS Y NIVELES CON CONTEXTO ===
        self.daily_range = {'high': 0, 'low': 0, 'mid': 0}
        self.weekly_range = {'high': 0, 'low': 0, 'mid': 0}
        self.current_session = "UNKNOWN"
        self.session_history = []  # Historia de sesiones
        
        # === MEMORIA DE EVENTOS BOS/CHoCH ===
        self.bos_events = []  # Eventos BOS históricos
        self.choch_events = []  # Eventos CHoCH históricos
        self.bos_success_rate = 0.0  # Tasa de éxito BOS
        self.choch_success_rate = 0.0  # Tasa de éxito CHoCH
        
        # === POIs CON MEMORIA HISTÓRICA ===
        self.pois_h4 = []
        self.pois_m15 = []
        self.pois_m5 = []
        self.previous_pois = []  # POIs históricos para análisis
        
        # === PUNTOS SWING CON CONTEXTO ===
        self.swing_points = {}
        self.last_swing_high = None
        self.last_swing_low = None
        self.swing_history = []  # Historia de puntos swing
        
        # === MÉTRICAS DE CALIDAD Y EXPERIENCIA ===
        self.analysis_quality = 0.5  # Calidad de análisis basada en experiencia
        self.market_phase = "RANGING"  # RANGING, TRENDING, BREAKOUT
        self.confidence_level = 0.5  # Nivel de confianza general
        self.session_count = 0  # Número de sesiones analizadas
        
        # === MEMORIA ADAPTATIVA ===
        self.learning_rate = 0.1  # Tasa de aprendizaje
        self.experience_factor = 1.0  # Factor de experiencia acumulada
        self.pattern_memory = {}  # Memoria de patrones exitosos/fallidos
        
        # === CACHE Y PERSISTENCIA ===
        self._cache = {}
        self._cache_timestamps = {}
        self.persistence_path = Path("cache/memory")
        self.persistence_path.mkdir(parents=True, exist_ok=True)
        
        # === INTEGRACIÓN CON LOGGER ===
        if SmartTradingLogger_available and SmartTradingLogger is not None:
            self.logger = SmartTradingLogger()
            enviar_senal_log("INFO", "✅ Smart Trading Logger integrado con MarketContext", __name__, "memory_init")
        else:
            self.logger = None
            enviar_senal_log("WARNING", "⚠️ Smart Trading Logger no disponible", __name__, "memory_init")
        
        # Cargar contexto persistente si existe
        self._load_persistent_context()
        
        enviar_senal_log("INFO", "✅ Market Context v6.0 inicializado - Memoria Trader Real activa", __name__, "memory_init")

    def _load_memory_config(self, config_path: str) -> Dict[str, Any]:
        """Carga configuración de memoria desde archivo JSON."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            enviar_senal_log("INFO", f"✅ Configuración de memoria cargada desde {config_path}", __name__, "config")
            return config.get('memory_management', {})
        except FileNotFoundError:
            enviar_senal_log("WARNING", f"⚠️ Archivo de configuración no encontrado: {config_path}, usando defaults", __name__, "config")
            return {
                'max_memory_gb': 4.0,
                'cache_timeout_minutes': 30,
                'historical_analysis_depth': 1000,
                'context_retention_hours': 168,
                'bias_retention_periods': 50,
                'poi_history_max_count': 200,
                'swing_points_retention': 100
            }

    def _load_persistent_context(self):
        """Carga contexto persistente desde disco."""
        context_file = self.persistence_path / f"market_context_{self.symbol}.pkl"
        
        if context_file.exists():
            try:
                with open(context_file, 'rb') as f:
                    saved_context = pickle.load(f)
                
                # Restaurar elementos críticos de memoria
                self.bias_history = saved_context.get('bias_history', [])
                self.bos_events = saved_context.get('bos_events', [])
                self.choch_events = saved_context.get('choch_events', [])
                self.previous_pois = saved_context.get('previous_pois', [])
                self.swing_history = saved_context.get('swing_history', [])
                self.session_count = saved_context.get('session_count', 0)
                self.experience_factor = saved_context.get('experience_factor', 1.0)
                self.pattern_memory = saved_context.get('pattern_memory', {})
                
                # Calcular métricas basadas en histórico
                self._calculate_success_rates()
                self._update_experience_factor()
                
                enviar_senal_log("INFO", f"✅ Contexto persistente cargado - {self.session_count} sesiones en memoria", __name__, "persistence")
                
            except Exception as e:
                enviar_senal_log("ERROR", f"❌ Error cargando contexto persistente: {e}", __name__, "persistence")
        else:
            enviar_senal_log("INFO", "🆕 Nuevo contexto de mercado - iniciando memoria trader", __name__, "persistence")

    def save_persistent_context(self):
        """Guarda contexto actual a disco para persistencia entre sesiones."""
        context_file = self.persistence_path / f"market_context_{self.symbol}.pkl"
        
        try:
            context_to_save = {
                'bias_history': self.bias_history[-self.config.get('bias_retention_periods', 50):],
                'bos_events': self.bos_events[-100:],  # Últimos 100 eventos
                'choch_events': self.choch_events[-100:],  # Últimos 100 eventos
                'previous_pois': self.previous_pois[-self.config.get('poi_history_max_count', 200):],
                'swing_history': self.swing_history[-self.config.get('swing_points_retention', 100):],
                'session_count': self.session_count,
                'experience_factor': self.experience_factor,
                'pattern_memory': self.pattern_memory,
                'last_save': datetime.now().isoformat()
            }
            
            with open(context_file, 'wb') as f:
                pickle.dump(context_to_save, f)
            
            enviar_senal_log("INFO", f"✅ Contexto persistente guardado - {self.session_count} sesiones", __name__, "persistence")
            return True
            
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error guardando contexto persistente: {e}", __name__, "persistence")
            return False

    def add_bos_event(self, bos_data: Dict[str, Any]):
        """Registra evento BOS con contexto temporal y calidad."""
        bos_event = {
            'timestamp': datetime.now(),
            'timeframe': bos_data.get('timeframe', 'unknown'),
            'direction': bos_data.get('direction', 'unknown'),
            'strength': bos_data.get('strength', 0.0),
            'price': bos_data.get('price', self.current_price),
            'confidence': bos_data.get('confidence', 0.5),
            'session': self.current_session,
            'market_phase': self.market_phase,
            'id': self._generate_event_id('BOS')
        }
        
        self.bos_events.append(bos_event)
        
        # Mantener solo eventos recientes según configuración
        max_events = self.config.get('historical_analysis_depth', 1000)
        if len(self.bos_events) > max_events:
            self.bos_events = self.bos_events[-max_events:]
        
        # Actualizar tasa de éxito
        self._calculate_success_rates()
        
        enviar_senal_log("INFO", f"📈 BOS event registrado: {bos_event['direction']} en {bos_event['timeframe']}", __name__, "bos_memory")

    def add_choch_event(self, choch_data: Dict[str, Any]):
        """Registra evento CHoCH con contexto temporal y calidad."""
        choch_event = {
            'timestamp': datetime.now(),
            'timeframe': choch_data.get('timeframe', 'unknown'),
            'direction': choch_data.get('direction', 'unknown'),
            'strength': choch_data.get('strength', 0.0),
            'price': choch_data.get('price', self.current_price),
            'confidence': choch_data.get('confidence', 0.5),
            'session': self.current_session,
            'market_phase': self.market_phase,
            'id': self._generate_event_id('CHoCH')
        }
        
        self.choch_events.append(choch_event)
        
        # Mantener solo eventos recientes según configuración
        max_events = self.config.get('historical_analysis_depth', 1000)
        if len(self.choch_events) > max_events:
            self.choch_events = self.choch_events[-max_events:]
        
        # Actualizar tasa de éxito
        self._calculate_success_rates()
        
        enviar_senal_log("INFO", f"🔄 CHoCH event registrado: {choch_event['direction']} en {choch_event['timeframe']}", __name__, "choch_memory")

    def update_market_bias(self, new_bias: str, confidence: float, timeframe: str = "H4"):
        """Actualiza sesgo con histórico de cambios y confianza."""
        old_bias = self.h4_bias if timeframe == "H4" else self.m15_bias
        
        # Solo actualizar si hay cambio real
        if old_bias != new_bias:
            bias_change = {
                'timestamp': datetime.now(),
                'timeframe': timeframe,
                'old_bias': old_bias,
                'new_bias': new_bias,
                'confidence': confidence,
                'session': self.current_session
            }
            
            self.bias_history.append(bias_change)
            
            # Mantener histórico según configuración
            max_history = self.config.get('bias_retention_periods', 50)
            if len(self.bias_history) > max_history:
                self.bias_history = self.bias_history[-max_history:]
            
            # Actualizar bias actual
            if timeframe == "H4":
                self.h4_bias = new_bias
            else:
                self.m15_bias = new_bias
            
            self.bias_confidence = confidence
            
            enviar_senal_log("INFO", f"📊 Bias actualizado {timeframe}: {old_bias} → {new_bias} (confianza: {confidence:.2f})", __name__, "bias_memory")

    def get_historical_context(self, timeframe: str, pattern_type: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene contexto histórico para timeframe y patrón específico."""
        context = {
            'timeframe': timeframe,
            'total_sessions': self.session_count,
            'experience_factor': self.experience_factor,
            'current_phase': self.market_phase,
            'bias_history_count': len(self.bias_history),
            'success_rates': {
                'bos': self.bos_success_rate,
                'choch': self.choch_success_rate
            }
        }
        
        # Contexto específico por patrón
        if pattern_type == "BOS":
            recent_bos = [event for event in self.bos_events 
                         if event['timeframe'] == timeframe][-10:]  # Últimos 10
            context['recent_events'] = recent_bos
            context['pattern_success_rate'] = self.bos_success_rate
            
        elif pattern_type == "CHoCH":
            recent_choch = [event for event in self.choch_events 
                           if event['timeframe'] == timeframe][-10:]  # Últimos 10
            context['recent_events'] = recent_choch
            context['pattern_success_rate'] = self.choch_success_rate
        
        # Contexto de memoria de patrones
        if pattern_type and pattern_type in self.pattern_memory:
            context['pattern_learning'] = self.pattern_memory[pattern_type]
        
        return context

    def assess_current_quality(self) -> float:
        """Evalúa calidad actual basada en histórico y experiencia."""
        base_quality = 0.5  # Calidad base
        
        # Factores de calidad basados en experiencia
        experience_bonus = min(0.3, self.session_count * 0.01)  # Máximo 0.3
        success_bonus = (self.bos_success_rate + self.choch_success_rate) / 2 * 0.2  # Máximo 0.2
        
        # Penalización por falta de datos
        data_penalty = 0.0
        if len(self.bos_events) < 10:
            data_penalty += 0.1
        if len(self.choch_events) < 10:
            data_penalty += 0.1
        
        # Calidad final
        quality = base_quality + experience_bonus + success_bonus - data_penalty
        quality = max(0.0, min(1.0, quality))  # Clamp entre 0 y 1
        
        self.analysis_quality = quality
        return quality

    def learn_from_outcome(self, pattern_type: str, pattern_id: str, outcome: Dict[str, Any]):
        """Aprende de resultado real de pattern para futuras detecciones."""
        if pattern_type not in self.pattern_memory:
            self.pattern_memory[pattern_type] = {
                'successes': 0,
                'failures': 0,
                'total_attempts': 0,
                'learning_data': []
            }
        
        # Registrar resultado
        self.pattern_memory[pattern_type]['total_attempts'] += 1
        
        if outcome.get('success', False):
            self.pattern_memory[pattern_type]['successes'] += 1
        else:
            self.pattern_memory[pattern_type]['failures'] += 1
        
        # Datos de aprendizaje
        learning_entry = {
            'timestamp': datetime.now(),
            'pattern_id': pattern_id,
            'success': outcome.get('success', False),
            'confidence': outcome.get('confidence', 0.5),
            'market_conditions': outcome.get('market_conditions', {}),
            'lessons': outcome.get('lessons', [])
        }
        
        self.pattern_memory[pattern_type]['learning_data'].append(learning_entry)
        
        # Mantener solo datos recientes
        if len(self.pattern_memory[pattern_type]['learning_data']) > 100:
            self.pattern_memory[pattern_type]['learning_data'] = \
                self.pattern_memory[pattern_type]['learning_data'][-100:]
        
        # Actualizar factor de experiencia
        self._update_experience_factor()
        
        enviar_senal_log("INFO", f"🎓 Aprendizaje registrado: {pattern_type} - {'✅' if outcome.get('success') else '❌'}", __name__, "learning")

    def _calculate_success_rates(self):
        """Calcula tasas de éxito basadas en eventos históricos."""
        # Calcular tasa de éxito BOS
        if self.bos_events:
            successful_bos = sum(1 for event in self.bos_events if event.get('success', False))
            self.bos_success_rate = successful_bos / len(self.bos_events)
        else:
            self.bos_success_rate = 0.5  # Neutral si no hay datos
        
        # Calcular tasa de éxito CHoCH
        if self.choch_events:
            successful_choch = sum(1 for event in self.choch_events if event.get('success', False))
            self.choch_success_rate = successful_choch / len(self.choch_events)
        else:
            self.choch_success_rate = 0.5  # Neutral si no hay datos

    def _update_experience_factor(self):
        """Actualiza factor de experiencia basado en actividad acumulada."""
        total_events = len(self.bos_events) + len(self.choch_events) + self.session_count
        self.experience_factor = 1.0 + (total_events * 0.01)  # Crece con experiencia

    def _generate_event_id(self, event_type: str) -> str:
        """Genera ID único para evento."""
        timestamp = datetime.now().isoformat()
        unique_string = f"{event_type}_{timestamp}_{self.symbol}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:8]

    def __repr__(self):
        """Representación legible del contexto con memoria."""
        return (
            f"MarketContext_v6("
            f"symbol={self.symbol}, "
            f"h4_bias={self.h4_bias}, "
            f"sessions={self.session_count}, "
            f"bos_events={len(self.bos_events)}, "
            f"choch_events={len(self.choch_events)}, "
            f"experience={self.experience_factor:.2f}, "
            f"quality={self.analysis_quality:.2f}"
            f")"
        )


# === INSTANCIA GLOBAL PARA COMPATIBILIDAD ===
_global_market_context = None

def get_market_context(symbol: str = "EURUSD") -> MarketContext:
    """Obtiene instancia global de MarketContext para el símbolo especificado."""
    global _global_market_context
    
    if _global_market_context is None or _global_market_context.symbol != symbol:
        _global_market_context = MarketContext()
        _global_market_context.symbol = symbol
    
    return _global_market_context
