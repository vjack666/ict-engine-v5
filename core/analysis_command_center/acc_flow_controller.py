#!/usr/bin/env python3
"""
🎛️ ACC FLOW CONTROLLER - Controlador de flujo avanzado del ACC
ARQUITECTURA: Gestión inteligente de flujos, caching y optimización
PROTOCOLO: "Caja Negra" - Control fino de ejecución, logging exhaustivo
"""

import asyncio
import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from collections import deque, defaultdict
from dataclasses import dataclass
from enum import Enum

# 🔌 IMPORTS DEL ICT ENGINE
from sistema.logging_interface import enviar_senal_log

# 🧠 IMPORTS DEL ACC
from .acc_data_models import (
    AnalysisInput,
    AnalysisOutput,
    AnalysisStatus,
    ComponentType
)

class FlowPriority(Enum):
    """Prioridades de flujo de análisis"""
    URGENT = "URGENT"       # Análisis críticos
    HIGH = "HIGH"           # Análisis de alta prioridad  
    NORMAL = "NORMAL"       # Análisis estándar
    LOW = "LOW"             # Análisis de baja prioridad
    BACKGROUND = "BACKGROUND"  # Análisis en background

class CacheStrategy(Enum):
    """Estrategias de caching"""
    NO_CACHE = "NO_CACHE"           # Sin cache
    AGGRESSIVE = "AGGRESSIVE"       # Cache agresivo
    CONSERVATIVE = "CONSERVATIVE"   # Cache conservador
    INTELLIGENT = "INTELLIGENT"     # Cache inteligente

@dataclass
class FlowMetrics:
    """Métricas de flujo y performance"""
    
    total_analyses: int = 0
    successful_analyses: int = 0
    failed_analyses: int = 0
    avg_execution_time_ms: float = 0.0
    cache_hit_rate: float = 0.0
    throughput_per_minute: float = 0.0
    queue_length: int = 0
    
    def get_success_rate(self) -> float:
        """Calcular tasa de éxito"""
        if self.total_analyses == 0:
            return 0.0
        return self.successful_analyses / self.total_analyses
    
    def get_summary(self) -> Dict[str, Any]:
        """Resumen de métricas"""
        return {
            "total": self.total_analyses,
            "success_rate": f"{self.get_success_rate():.1%}",
            "avg_time_ms": f"{self.avg_execution_time_ms:.0f}",
            "cache_hit_rate": f"{self.cache_hit_rate:.1%}",
            "throughput_min": f"{self.throughput_per_minute:.1f}",
            "queue_length": self.queue_length
        }

class AccFlowController:
    """
    🎛️ Controlador de flujo avanzado del ACC
    
    RESPONSABILIDADES:
    - Gestión de colas de análisis por prioridad
    - Caching inteligente de resultados
    - Optimización de flujos de ejecución
    - Control de concurrencia y throttling
    - Métricas avanzadas de performance
    """
    
    def __init__(self,
                 max_concurrent_analyses: int = 3,
                 cache_ttl_minutes: int = 5,
                 cache_strategy: CacheStrategy = CacheStrategy.INTELLIGENT,
                 enable_flow_optimization: bool = True):
        """
        🎛️ Inicialización del controlador de flujo
        
        Args:
            max_concurrent_analyses: Máximo análisis concurrentes
            cache_ttl_minutes: TTL del cache en minutos
            cache_strategy: Estrategia de caching
            enable_flow_optimization: Activar optimizaciones de flujo
        """
        
        # ⚙️ CONFIGURACIÓN
        self.max_concurrent_analyses = max_concurrent_analyses
        self.cache_ttl_minutes = cache_ttl_minutes
        self.cache_strategy = cache_strategy
        self.enable_flow_optimization = enable_flow_optimization
        
        # 📊 COLAS DE PRIORIDAD
        self.priority_queues = {
            FlowPriority.URGENT: deque(),
            FlowPriority.HIGH: deque(),
            FlowPriority.NORMAL: deque(),
            FlowPriority.LOW: deque(),
            FlowPriority.BACKGROUND: deque()
        }
        
        # 💾 SISTEMA DE CACHE
        self.results_cache = {}  # cache_key -> (result, timestamp)
        self.cache_stats = defaultdict(int)
        
        # 📊 MÉTRICAS Y ESTADO
        self.flow_metrics = FlowMetrics()
        self.active_analyses = {}  # analysis_id -> start_time
        self.execution_history = deque(maxlen=1000)  # Historial limitado
        
        # 🎯 OPTIMIZACIONES
        self.flow_patterns = {}  # symbol -> pattern_data
        self.component_performance = defaultdict(list)  # component -> [times]
        
        # 📝 LOG INICIALIZACIÓN
        enviar_senal_log(
            'DEBUG',
            f"AccFlowController inicializado | "
                   f"Max Concurrent: {max_concurrent_analyses} | "
                   f"Cache TTL: {cache_ttl_minutes}min | "
                   f"Strategy: {cache_strategy.value}",
            'acc_flow_controller',
            'acc'
        )
    
    def should_use_cache(self, analysis_input: AnalysisInput) -> bool:
        """
        💾 Determinar si usar cache para un análisis
        
        Args:
            analysis_input: Parámetros de análisis
            
        Returns:
            bool: True si debe usar cache
        """
        
        if self.cache_strategy == CacheStrategy.NO_CACHE:
            return False
        
        # 🔑 GENERAR CACHE KEY
        cache_key = self._generate_cache_key(analysis_input)
        
        # ✅ VERIFICAR EXISTENCIA Y VALIDEZ
        if cache_key in self.results_cache:
            result, timestamp = self.results_cache[cache_key]
            
            # ⏰ VERIFICAR TTL
            age_minutes = (datetime.now() - timestamp).total_seconds() / 60
            
            if age_minutes <= self.cache_ttl_minutes:
                # 📊 REGISTRAR HIT
                self.cache_stats['hits'] += 1
                self._update_cache_hit_rate()
                
                enviar_senal_log(
                    level='DEBUG',
                    message=f"💾 Cache HIT | Key: {cache_key[:20]}... | Age: {age_minutes:.1f}min",
                    emisor='acc_flow_controller',
                    categoria='acc'
                )
                
                return True
            else:
                # 🗑️ CACHE EXPIRADO
                del self.results_cache[cache_key]
                enviar_senal_log(
                    level='DEBUG',
                    message=f"💾 Cache EXPIRED | Key: {cache_key[:20]}... | Age: {age_minutes:.1f}min",
                    emisor='acc_flow_controller',
                    categoria='acc'
                )
        
        # 📊 REGISTRAR MISS
        self.cache_stats['misses'] += 1
        self._update_cache_hit_rate()
        
        return False
    
    def get_cached_result(self, analysis_input: AnalysisInput) -> Optional[AnalysisOutput]:
        """
        💾 Obtener resultado del cache
        
        Args:
            analysis_input: Parámetros de análisis
            
        Returns:
            AnalysisOutput o None si no está en cache
        """
        
        cache_key = self._generate_cache_key(analysis_input)
        
        if cache_key in self.results_cache:
            result, timestamp = self.results_cache[cache_key]
            
            # 📊 CREAR COPIA CON NUEVO ID
            cached_result = self._create_cached_copy(result, analysis_input)
            
            enviar_senal_log(
                level='DEBUG',
                message=f"💾 Cache result returned | Original ID: {result.analysis_id} | "
                       f"New ID: {cached_result.analysis_id}",
                emisor='acc_flow_controller',
                categoria='acc'
            )
            
            return cached_result
        
        return None
    
    def cache_result(self, analysis_input: AnalysisInput, result: AnalysisOutput):
        """
        💾 Almacenar resultado en cache
        
        Args:
            analysis_input: Parámetros de análisis
            result: Resultado a cachear
        """
        
        if self.cache_strategy == CacheStrategy.NO_CACHE:
            return
        
        cache_key = self._generate_cache_key(analysis_input)
        self.results_cache[cache_key] = (result, datetime.now())
        
        enviar_senal_log(
            level='DEBUG',
            message=f"💾 Result cached | Key: {cache_key[:20]}... | ID: {result.analysis_id}",
            emisor='acc_flow_controller',
            categoria='acc'
        )
        
        # 🧹 CLEANUP PERIÓDICO
        self._cleanup_expired_cache()
    
    def queue_analysis(self, 
                      analysis_input: AnalysisInput, 
                      executor_func: Callable,
                      priority: FlowPriority = FlowPriority.NORMAL) -> str:
        """
        📥 Encolar análisis para ejecución
        
        Args:
            analysis_input: Parámetros de análisis
            executor_func: Función ejecutora del análisis
            priority: Prioridad de ejecución
            
        Returns:
            str: ID del análisis encolado
        """
        
        # 📦 CREAR ITEM DE COLA
        queue_item = {
            'analysis_input': analysis_input,
            'executor_func': executor_func,
            'queue_timestamp': datetime.now(),
            'priority': priority
        }
        
        # 📥 AÑADIR A COLA APROPIADA
        self.priority_queues[priority].append(queue_item)
        
        # 📊 ACTUALIZAR MÉTRICAS
        self.flow_metrics.queue_length = sum(len(queue) for queue in self.priority_queues.values())
        
        enviar_senal_log(
            level='DEBUG',
            message=f"📥 Analysis queued | ID: {analysis_input.analysis_id} | "
                   f"Priority: {priority.value} | Queue Length: {self.flow_metrics.queue_length}",
            emisor='acc_flow_controller',
            categoria='acc'
        )
        
        return analysis_input.analysis_id
    
    def get_next_analysis(self) -> Optional[Dict[str, Any]]:
        """
        📤 Obtener próximo análisis de las colas por prioridad
        
        Returns:
            Dict con análisis a ejecutar o None si no hay ninguno
        """
        
        # 🎯 REVISAR COLAS POR PRIORIDAD
        for priority in FlowPriority:
            queue = self.priority_queues[priority]
            
            if queue:
                # 📤 EXTRAER PRIMER ELEMENTO
                analysis_item = queue.popleft()
                
                # 📊 ACTUALIZAR MÉTRICAS
                self.flow_metrics.queue_length = sum(len(q) for q in self.priority_queues.values())
                
                enviar_senal_log(
                    level='DEBUG',
                    message=f"📤 Analysis dequeued | ID: {analysis_item['analysis_input'].analysis_id} | "
                           f"Priority: {priority.value} | Remaining: {self.flow_metrics.queue_length}",
                    emisor='acc_flow_controller',
                    categoria='acc'
                )
                
                return analysis_item
        
        return None
    
    def can_execute_analysis(self) -> bool:
        """
        🚦 Verificar si se puede ejecutar un nuevo análisis
        
        Returns:
            bool: True si se puede ejecutar
        """
        
        current_active = len(self.active_analyses)
        can_execute = current_active < self.max_concurrent_analyses
        
        if not can_execute:
            enviar_senal_log(
                level='DEBUG',
                message=f"🚦 Execution blocked | Active: {current_active} | Max: {self.max_concurrent_analyses}",
                emisor='acc_flow_controller',
                categoria='acc'
            )
        
        return can_execute
    
    def register_analysis_start(self, analysis_id: str):
        """
        📊 Registrar inicio de análisis
        
        Args:
            analysis_id: ID del análisis
        """
        
        self.active_analyses[analysis_id] = datetime.now()
        
        enviar_senal_log(
            level='DEBUG',
            message=f"📊 Analysis started | ID: {analysis_id} | Active: {len(self.active_analyses)}",
            emisor='acc_flow_controller',
            categoria='acc'
        )
    
    def register_analysis_completion(self, 
                                   analysis_id: str, 
                                   result: AnalysisOutput, 
                                   success: bool = True):
        """
        📊 Registrar finalización de análisis
        
        Args:
            analysis_id: ID del análisis
            result: Resultado del análisis
            success: Si fue exitoso
        """
        
        # ⏱️ CALCULAR TIEMPO DE EJECUCIÓN
        start_time = self.active_analyses.get(analysis_id)
        execution_time = 0.0
        
        if start_time:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            del self.active_analyses[analysis_id]
        
        # 📊 ACTUALIZAR MÉTRICAS
        self.flow_metrics.total_analyses += 1
        
        if success:
            self.flow_metrics.successful_analyses += 1
        else:
            self.flow_metrics.failed_analyses += 1
        
        # 📈 ACTUALIZAR TIEMPO PROMEDIO
        total_time = (self.flow_metrics.avg_execution_time_ms * (self.flow_metrics.total_analyses - 1) + execution_time)
        self.flow_metrics.avg_execution_time_ms = total_time / self.flow_metrics.total_analyses
        
        # 📚 AÑADIR AL HISTORIAL
        self.execution_history.append({
            'analysis_id': analysis_id,
            'execution_time_ms': execution_time,
            'success': success,
            'timestamp': datetime.now()
        })
        
        # 🎯 ACTUALIZAR THROUGHPUT
        self._update_throughput()
        
        enviar_senal_log(
            level='DEBUG',
            message=f"📊 Analysis completed | ID: {analysis_id} | "
                   f"Time: {execution_time:.0f}ms | Success: {success} | "
                   f"Success Rate: {self.flow_metrics.get_success_rate():.1%}",
            emisor='acc_flow_controller',
            categoria='acc'
        )
    
    def get_flow_metrics(self) -> Dict[str, Any]:
        """
        📊 Obtener métricas de flujo actuales
        
        Returns:
            Dict con métricas completas
        """
        
        return {
            "flow_metrics": self.flow_metrics.get_summary(),
            "cache_stats": dict(self.cache_stats),
            "active_analyses": len(self.active_analyses),
            "queue_summary": {
                priority.value: len(queue) 
                for priority, queue in self.priority_queues.items()
            },
            "cache_size": len(self.results_cache),
            "history_size": len(self.execution_history)
        }
    
    def optimize_flow(self, symbol: str) -> Dict[str, Any]:
        """
        🎯 Optimizar flujo para símbolo específico
        
        Args:
            symbol: Símbolo a optimizar
            
        Returns:
            Dict con recomendaciones de optimización
        """
        
        if not self.enable_flow_optimization:
            return {"optimization": "disabled"}
        
        # 📊 ANALIZAR PATRONES HISTÓRICOS
        symbol_history = [
            entry for entry in self.execution_history 
            if entry.get('symbol') == symbol
        ]
        
        if len(symbol_history) < 5:
            return {"optimization": "insufficient_data"}
        
        # 📈 CALCULAR MÉTRICAS
        avg_time = sum(entry['execution_time_ms'] for entry in symbol_history) / len(symbol_history)
        success_rate = sum(1 for entry in symbol_history if entry['success']) / len(symbol_history)
        
        # 🎯 GENERAR RECOMENDACIONES
        recommendations = []
        
        if avg_time > self.flow_metrics.avg_execution_time_ms * 1.2:
            recommendations.append("consider_increased_cache_ttl")
        
        if success_rate < 0.8:
            recommendations.append("review_component_configuration")
        
        optimization_data = {
            "symbol": symbol,
            "avg_execution_time_ms": avg_time,
            "success_rate": success_rate,
            "sample_size": len(symbol_history),
            "recommendations": recommendations,
            "suggested_priority": FlowPriority.HIGH.value if success_rate > 0.9 else FlowPriority.NORMAL.value
        }
        
        # 💾 ALMACENAR PATRÓN
        self.flow_patterns[symbol] = optimization_data
        
        enviar_senal_log(
            level='DEBUG',
            message=f"🎯 Flow optimized | Symbol: {symbol} | "
                   f"Avg Time: {avg_time:.0f}ms | Success: {success_rate:.1%}",
            emisor='acc_flow_controller',
            categoria='acc'
        )
        
        return optimization_data
    
    def _generate_cache_key(self, analysis_input: AnalysisInput) -> str:
        """🔑 Generar clave de cache para análisis"""
        
        # 🎯 COMPONENTES DE LA CLAVE
        key_components = [
            analysis_input.symbol,
            "_".join(sorted(analysis_input.timeframes)),
            analysis_input.analysis_type,
            str(analysis_input.confidence_threshold),
            str(analysis_input.poi_limit)
        ]
        
        # 🔐 GENERAR HASH
        cache_key = "_".join(key_components)
        return cache_key
    
    def _create_cached_copy(self, original_result: AnalysisOutput, new_input: AnalysisInput) -> AnalysisOutput:
        """📊 Crear copia de resultado cacheado con nuevo ID"""
        
        # 🔄 CLONAR RESULTADO (simplificado)
        cached_result = AnalysisOutput(
            analysis_id=new_input.analysis_id,
            input_parameters=new_input,
            analysis_status=AnalysisStatus.COMPLETED,
            completion_timestamp=datetime.now().isoformat()
        )
        
        # 📊 COPIAR DATOS PRINCIPALES
        cached_result.market_structure = original_result.market_structure
        cached_result.poi_data = original_result.poi_data
        cached_result.confidence_data = original_result.confidence_data
        cached_result.veredicto_data = original_result.veredicto_data
        cached_result.tct_data = original_result.tct_data
        
        # 📊 COPIAR MÉTRICAS (con ajustes)
        cached_result.overall_success_rate = original_result.overall_success_rate
        cached_result.total_execution_time_ms = 0.0  # Cache hit = tiempo mínimo
        cached_result.analysis_quality_score = original_result.analysis_quality_score
        
        return cached_result
    
    def _update_cache_hit_rate(self):
        """📊 Actualizar tasa de hit del cache"""
        
        hits = self.cache_stats['hits']
        misses = self.cache_stats['misses']
        total = hits + misses
        
        if total > 0:
            self.flow_metrics.cache_hit_rate = hits / total
    
    def _update_throughput(self):
        """📈 Actualizar throughput por minuto"""
        
        # 📊 CONTAR ANÁLISIS EN LA ÚLTIMA HORA
        cutoff_time = datetime.now() - timedelta(minutes=60)
        recent_analyses = [
            entry for entry in self.execution_history 
            if entry['timestamp'] > cutoff_time
        ]
        
        # 📈 CALCULAR THROUGHPUT
        if recent_analyses:
            time_span_minutes = (datetime.now() - recent_analyses[0]['timestamp']).total_seconds() / 60
            if time_span_minutes > 0:
                self.flow_metrics.throughput_per_minute = len(recent_analyses) / time_span_minutes
    
    def _cleanup_expired_cache(self):
        """🧹 Limpiar entradas expiradas del cache"""
        
        if len(self.results_cache) < 100:  # Solo limpiar si hay muchas entradas
            return
        
        cutoff_time = datetime.now() - timedelta(minutes=self.cache_ttl_minutes)
        expired_keys = []
        
        for cache_key, (result, timestamp) in self.results_cache.items():
            if timestamp < cutoff_time:
                expired_keys.append(cache_key)
        
        # 🗑️ ELIMINAR EXPIRADAS
        for key in expired_keys:
            del self.results_cache[key]
        
        if expired_keys:
            enviar_senal_log(
                level='DEBUG',
                message=f"🧹 Cache cleanup | Removed: {len(expired_keys)} | Remaining: {len(self.results_cache)}",
                emisor='acc_flow_controller',
                categoria='acc'
            )
