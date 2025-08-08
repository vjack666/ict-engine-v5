"""
SIC v3.1 - Predictive Cache Manager
==================================

Sistema de caché predictivo para optimización inteligente de imports.

Este módulo implementa un sistema avanzado de caché que:
- Predice qué módulos serán necesarios
- Mantiene un caché inteligente de módulos frecuentemente usados
- Optimiza la performance basándose en patrones de uso
- Gestiona automáticamente el tamaño del caché

Autor: ICT Engine v6.0 Team
Versión: v3.1.0  
Fecha: Agosto 2025
"""

import sys
import time
import threading
import pickle
import hashlib
from typing import Dict, List, Optional, Any, Tuple, Set
from pathlib import Path
import weakref
from collections import defaultdict, deque
import psutil
import json


class ModuleCacheEntry:
    """
    📦 Entrada individual del caché de módulos
    
    Representa un módulo cacheado con toda su metadata asociada.
    """
    
    def __init__(self, module_name: str, module_obj: Any, 
                 from_list: Optional[List[str]] = None,
                 alias: Optional[str] = None):
        """
        Inicializa una entrada de caché
        
        Args:
            module_name: Nombre del módulo
            module_obj: Objeto del módulo cacheado
            from_list: Lista de elementos importados específicamente
            alias: Alias usado para el import
        """
        self.module_name = module_name
        self.module_obj = module_obj
        self.from_list = from_list or []
        self.alias = alias
        
        # Metadata
        self.created_at = time.time()
        self.last_accessed = time.time()
        self.access_count = 0
        self.hit_count = 0
        self.cache_size_bytes = self._calculate_size()
        
        # Predicción
        self.prediction_score = 0.0
        self.usage_pattern = deque(maxlen=10)  # Últimos 10 accesos
        
    def access(self):
        """Registra un acceso al módulo cacheado"""
        self.last_accessed = time.time()
        self.access_count += 1
        self.hit_count += 1
        self.usage_pattern.append(time.time())
        
        # Actualizar score de predicción basado en frecuencia
        self._update_prediction_score()
    
    def _calculate_size(self) -> int:
        """Calcula el tamaño aproximado del objeto en memoria"""
        try:
            # Estimación básica del tamaño
            return sys.getsizeof(self.module_obj)
        except:
            return 1024  # Estimación por defecto: 1KB
    
    def _update_prediction_score(self):
        """Actualiza el score de predicción basado en patrones de uso"""
        if len(self.usage_pattern) < 2:
            self.prediction_score = 1.0
            return
        
        # Calcular frecuencia de uso
        time_span = self.usage_pattern[-1] - self.usage_pattern[0]
        frequency = len(self.usage_pattern) / max(time_span, 1)
        
        # Calcular recency (qué tan reciente fue el último acceso)
        time_since_last = time.time() - self.last_accessed
        recency = 1.0 / (1.0 + time_since_last / 3600)  # Decay por hora
        
        # Score combinado
        self.prediction_score = (frequency * 0.6 + recency * 0.4) * self.access_count
    
    @property
    def age_hours(self) -> float:
        """Edad del cache entry en horas"""
        return (time.time() - self.created_at) / 3600
    
    @property
    def is_stale(self) -> bool:
        """Indica si la entrada está obsoleta"""
        # Obsoleto si no se ha accedido en más de 1 hora y tiene pocos accesos
        time_since_access = time.time() - self.last_accessed
        return time_since_access > 3600 and self.access_count < 3
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entrada a diccionario para serialización"""
        return {
            'module_name': self.module_name,
            'from_list': self.from_list,
            'alias': self.alias,
            'created_at': self.created_at,
            'last_accessed': self.last_accessed,
            'access_count': self.access_count,
            'hit_count': self.hit_count,
            'cache_size_bytes': self.cache_size_bytes,
            'prediction_score': self.prediction_score,
            'usage_pattern': list(self.usage_pattern)
        }


class PredictiveCacheManager:
    """
    🧠 Gestor de Caché Predictivo Inteligente
    
    Maneja un sistema de caché avanzado que predice y optimiza
    el acceso a módulos basándose en patrones de uso.
    
    Características:
    - Caché predictivo basado en ML básico
    - Gestión automática de memoria
    - Análisis de patrones de uso
    - Persistencia de estadísticas
    - Auto-limpieza inteligente
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el gestor de caché predictivo
        
        Args:
            config: Configuración del sistema de caché
        """
        self._config = config or {}
        self._cache: Dict[str, ModuleCacheEntry] = {}
        self._prediction_patterns: Dict[str, List[str]] = defaultdict(list)
        
        # Configuración
        self._max_cache_size_mb = self._config.get('max_cache_size_mb', 256)  # 256MB
        self._max_entries = self._config.get('max_entries', 100)
        self._prediction_threshold = self._config.get('prediction_threshold', 0.5)
        self._enable_persistence = self._config.get('enable_persistence', True)
        
        # Estadísticas
        self._stats = {
            'cache_hits': 0,
            'cache_misses': 0,
            'predictions_made': 0,
            'predictions_correct': 0,
            'total_size_bytes': 0,
            'cleanup_runs': 0,
            'entries_evicted': 0
        }
        
        # Threading
        self._lock = threading.Lock()
        
        # Patrones de uso global
        self._usage_sequence = deque(maxlen=1000)  # Últimos 1000 imports
        self._module_relationships: Dict[str, Set[str]] = defaultdict(set)
        
        # Archivo de persistencia
        self._persistence_file = Path(self._config.get(
            'persistence_file', 
            'sic_cache_stats.json'
        ))
        
        # Cargar estadísticas previas si existen
        if self._enable_persistence:
            self._load_persistence_data()
        
        # 🔥 WARM-UP AUTOMÁTICO de módulos críticos
        self._warm_up_critical_modules()
    
    def _warm_up_critical_modules(self):
        """🔥 Warm-up automático de módulos críticos del sistema"""
        critical_modules = ['sys', 'os', 'time', 'datetime', 'pathlib', 'json', 'threading']
        
        for module_name in critical_modules:
            try:
                # Importar y cachear módulos críticos
                module_obj = __import__(module_name)
                self.cache_module(module_name, module_obj=module_obj)
                print(f"🔥 [Cache Warm-up] {module_name} pre-cacheado")
            except Exception as e:
                print(f"⚠️ [Cache Warm-up] Error pre-cacheando {module_name}: {e}")
        
        print("🔥 [Predictive Cache] Warm-up de módulos críticos completado")
    
    def cache_module(self, module_name: str, 
                    from_list: Optional[List[str]] = None,
                    alias: Optional[str] = None,
                    module_obj: Any = None) -> bool:
        """
        💾 Almacena un módulo en el caché predictivo
        
        Args:
            module_name: Nombre del módulo
            from_list: Lista de elementos específicos importados
            alias: Alias usado
            module_obj: Objeto del módulo a cachear
            
        Returns:
            True si se cacheó exitosamente
        """
        if module_obj is None:
            return False
        
        cache_key = self._generate_cache_key(module_name, from_list, alias)
        
        with self._lock:
            # Verificar límites de caché
            if not self._has_cache_space():
                self._cleanup_cache()
            
            # Crear entrada de caché
            cache_entry = ModuleCacheEntry(module_name, module_obj, from_list, alias)
            self._cache[cache_key] = cache_entry
            
            # Actualizar estadísticas
            self._stats['total_size_bytes'] += cache_entry.cache_size_bytes
            
            # Registrar secuencia de uso para predicciones
            self._usage_sequence.append(module_name)
            self._update_module_relationships(module_name)
        
        print(f"💾 [Predictive Cache] Módulo cacheado: {module_name}")
        return True
    
    def get_cached_module(self, module_name: str,
                         from_list: Optional[List[str]] = None,
                         alias: Optional[str] = None) -> Optional[Any]:
        """
        🔍 Obtiene un módulo del caché
        
        Args:
            module_name: Nombre del módulo
            from_list: Lista de elementos específicos
            alias: Alias usado
            
        Returns:
            Objeto del módulo si está en caché, None en caso contrario
        """
        cache_key = self._generate_cache_key(module_name, from_list, alias)
        
        with self._lock:
            if cache_key in self._cache:
                cache_entry = self._cache[cache_key]
                cache_entry.access()
                self._stats['cache_hits'] += 1
                
                print(f"🎯 [Predictive Cache] Cache HIT: {module_name}")
                return cache_entry.module_obj
            else:
                self._stats['cache_misses'] += 1
                print(f"❌ [Predictive Cache] Cache MISS: {module_name}")
                return None
    
    def predict_next_modules(self, current_module: str, 
                           count: int = 5) -> List[Tuple[str, float]]:
        """
        🔮 Predice los próximos módulos que serán necesarios
        
        Args:
            current_module: Módulo que se acaba de importar
            count: Número de predicciones a retornar
            
        Returns:
            Lista de tuplas (módulo, probabilidad)
        """
        predictions = []
        
        with self._lock:
            # Predicción basada en relaciones de módulos
            if current_module in self._module_relationships:
                related_modules = self._module_relationships[current_module]
                
                for related_module in related_modules:
                    # Calcular probabilidad basada en frecuencia de co-ocurrencia
                    probability = self._calculate_cooccurrence_probability(
                        current_module, related_module
                    )
                    
                    if probability > self._prediction_threshold:
                        predictions.append((related_module, probability))
            
            # Predicción basada en secuencias de uso
            sequence_predictions = self._predict_from_sequence(current_module)
            predictions.extend(sequence_predictions)
            
            # Eliminar duplicados y ordenar por probabilidad
            unique_predictions = {}
            for module, prob in predictions:
                if module not in unique_predictions or prob > unique_predictions[module]:
                    unique_predictions[module] = prob
            
            # Ordenar y limitar resultados
            sorted_predictions = sorted(
                unique_predictions.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:count]
            
            self._stats['predictions_made'] += len(sorted_predictions)
        
        return sorted_predictions
    
    def preload_predicted_modules(self, current_module: str) -> List[str]:
        """
        ⚡ Pre-carga módulos predichos en background
        
        Args:
            current_module: Módulo base para predicciones
            
        Returns:
            Lista de módulos pre-cargados exitosamente
        """
        predictions = self.predict_next_modules(current_module, count=3)
        preloaded = []
        
        for module_name, probability in predictions:
            if probability > 0.7:  # Solo pre-cargar con alta probabilidad
                try:
                    # Intentar import del módulo predicho
                    import importlib
                    module = importlib.import_module(module_name)
                    
                    # Cachearlo
                    if self.cache_module(module_name, module_obj=module):
                        preloaded.append(module_name)
                        print(f"⚡ [Predictive Cache] Pre-cargado: {module_name} (prob: {probability:.2f})")
                
                except ImportError:
                    # Módulo no disponible, ignorar
                    pass
                except Exception as e:
                    print(f"❌ Error pre-cargando {module_name}: {e}")
        
        return preloaded
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        📊 Obtiene estadísticas completas del caché
        
        Returns:
            Diccionario con métricas detalladas
        """
        with self._lock:
            stats = self._stats.copy()
            
            # Calcular métricas adicionales
            total_requests = stats['cache_hits'] + stats['cache_misses']
            hit_rate = (stats['cache_hits'] / max(1, total_requests)) * 100
            
            # Estadísticas de predicción
            prediction_accuracy = 0.0
            if stats['predictions_made'] > 0:
                prediction_accuracy = (stats['predictions_correct'] / stats['predictions_made']) * 100
            
            # Estadísticas de cache entries
            cache_entries = list(self._cache.values())
            avg_access_count = sum(entry.access_count for entry in cache_entries) / max(1, len(cache_entries))
            
            # Uso de memoria
            memory_usage_mb = stats['total_size_bytes'] / 1024 / 1024
            memory_efficiency = (len(self._cache) / max(1, self._max_entries)) * 100
        
        return {
            'cache_performance': {
                'hit_rate_percent': hit_rate,
                'total_hits': stats['cache_hits'],
                'total_misses': stats['cache_misses'],
                'total_requests': total_requests
            },
            'prediction_stats': {
                'predictions_made': stats['predictions_made'],
                'predictions_correct': stats['predictions_correct'],
                'accuracy_percent': prediction_accuracy
            },
            'cache_info': {
                'total_entries': len(self._cache),
                'max_entries': self._max_entries,
                'memory_usage_mb': memory_usage_mb,
                'max_memory_mb': self._max_cache_size_mb,
                'memory_efficiency_percent': memory_efficiency,
                'avg_access_count': avg_access_count
            },
            'maintenance_stats': {
                'cleanup_runs': stats['cleanup_runs'],
                'entries_evicted': stats['entries_evicted']
            }
        }
    
    def cleanup_cache(self, force: bool = False) -> int:
        """
        🧹 Limpia el caché eliminando entradas obsoletas
        
        Args:
            force: Si True, fuerza una limpieza agresiva
            
        Returns:
            Número de entradas eliminadas
        """
        return self._cleanup_cache(force)
    
    def clear_cache(self):
        """🗑️ Limpia completamente el caché"""
        with self._lock:
            self._cache.clear()
            self._stats['total_size_bytes'] = 0
        
        print("🗑️ [Predictive Cache] Caché completamente limpiado")
    
    def get_status(self) -> str:
        """Estado del gestor de caché"""
        stats = self.get_cache_stats()
        cache_info = stats['cache_info']
        performance = stats['cache_performance']
        
        return (f"Predictive Cache: {cache_info['total_entries']}/{cache_info['max_entries']} "
                f"entradas, {performance['hit_rate_percent']:.1f}% hit rate, "
                f"{cache_info['memory_usage_mb']:.1f}MB")
    
    def _generate_cache_key(self, module_name: str,
                           from_list: Optional[List[str]] = None,
                           alias: Optional[str] = None) -> str:
        """Genera una clave única para el caché"""
        # Crear clave basada en todos los parámetros
        key_parts = [module_name]
        
        if from_list:
            key_parts.append(f"from:{','.join(sorted(from_list))}")
        
        if alias:
            key_parts.append(f"alias:{alias}")
        
        return "::".join(key_parts)
    
    def _has_cache_space(self) -> bool:
        """Verifica si hay espacio disponible en el caché"""
        # Verificar número de entradas
        if len(self._cache) >= self._max_entries:
            return False
        
        # Verificar uso de memoria
        memory_usage_mb = self._stats['total_size_bytes'] / 1024 / 1024
        if memory_usage_mb >= self._max_cache_size_mb:
            return False
        
        return True
    
    def _cleanup_cache(self, force: bool = False) -> int:
        """Implementación interna de limpieza de caché"""
        cleaned_count = 0
        
        with self._lock:
            # Obtener entradas ordenadas por score de predicción (menor primero)
            entries_by_score = sorted(
                self._cache.items(),
                key=lambda x: (x[1].prediction_score, x[1].last_accessed)
            )
            
            # Determinar cuántas entradas eliminar
            target_size = self._max_entries // 2 if force else self._max_entries - 10
            entries_to_remove = max(0, len(self._cache) - target_size)
            
            # Eliminar entradas
            for i in range(min(entries_to_remove, len(entries_by_score))):
                key, entry = entries_by_score[i]
                
                # Solo eliminar si es obsoleta o si estamos forzando
                if force or entry.is_stale:
                    self._stats['total_size_bytes'] -= entry.cache_size_bytes
                    del self._cache[key]
                    cleaned_count += 1
            
            self._stats['cleanup_runs'] += 1
            self._stats['entries_evicted'] += cleaned_count
        
        if cleaned_count > 0:
            print(f"🧹 [Predictive Cache] {cleaned_count} entradas eliminadas")
        
        return cleaned_count
    
    def _update_module_relationships(self, module_name: str):
        """Actualiza las relaciones entre módulos basándose en secuencias de uso"""
        if len(self._usage_sequence) < 2:
            return
        
        # Obtener los últimos módulos usados
        recent_modules = list(self._usage_sequence)[-5:]  # Últimos 5
        
        # Crear relaciones bidireccionales
        for other_module in recent_modules:
            if other_module != module_name:
                self._module_relationships[module_name].add(other_module)
                self._module_relationships[other_module].add(module_name)
    
    def _calculate_cooccurrence_probability(self, module1: str, module2: str) -> float:
        """Calcula la probabilidad de co-ocurrencia entre dos módulos"""
        # Contar co-ocurrencias en la secuencia de uso
        sequence = list(self._usage_sequence)
        cooccurrences = 0
        module1_count = 0
        
        for i, module in enumerate(sequence):
            if module == module1:
                module1_count += 1
                # Buscar module2 en una ventana de ±3 posiciones
                start = max(0, i - 3)
                end = min(len(sequence), i + 4)
                
                if module2 in sequence[start:end]:
                    cooccurrences += 1
        
        if module1_count == 0:
            return 0.0
        
        return cooccurrences / module1_count
    
    def _predict_from_sequence(self, current_module: str, 
                              lookback: int = 10) -> List[Tuple[str, float]]:
        """Predice módulos basándose en secuencias históricas"""
        if len(self._usage_sequence) < lookback:
            return []
        
        # Buscar patrones en la secuencia
        sequence = list(self._usage_sequence)
        predictions = defaultdict(int)
        
        # Buscar todas las ocurrencias del módulo actual
        for i, module in enumerate(sequence):
            if module == current_module and i < len(sequence) - 1:
                # Contar qué módulos vinieron después
                next_module = sequence[i + 1]
                predictions[next_module] += 1
        
        if not predictions:
            return []
        
        # Convertir a probabilidades
        total_occurrences = sum(predictions.values())
        return [
            (module, count / total_occurrences)
            for module, count in predictions.items()
            if count / total_occurrences > 0.1  # Solo predicciones > 10%
        ]
    
    def _load_persistence_data(self):
        """Carga datos de persistencia si existen"""
        if not self._persistence_file.exists():
            return
        
        try:
            with open(self._persistence_file, 'r') as f:
                data = json.load(f)
            
            # Cargar estadísticas básicas
            if 'stats' in data:
                self._stats.update(data['stats'])
            
            # Cargar relaciones de módulos
            if 'module_relationships' in data:
                for module, related in data['module_relationships'].items():
                    self._module_relationships[module] = set(related)
            
            print("📁 [Predictive Cache] Datos de persistencia cargados")
            
        except Exception as e:
            print(f"❌ Error cargando persistencia: {e}")
    
    def _save_persistence_data(self, force_save: bool = False):
        """
        Guarda datos de persistencia de forma segura
        
        Args:
            force_save: Fuerza el guardado incluso durante shutdown
        """
        if not self._enable_persistence:
            return
        
        # Durante shutdown, solo guardar si se fuerza explícitamente
        if not force_save and self._is_shutting_down():
            return
        
        try:
            data = {
                'stats': self._stats,
                'module_relationships': {
                    module: list(related) 
                    for module, related in self._module_relationships.items()
                },
                'saved_at': time.time()
            }
            
            # Guardar usando la función open estándar
            with open(str(self._persistence_file), 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            if not self._is_shutting_down():
                print("💾 [Predictive Cache] Datos de persistencia guardados")
            
        except Exception as e:
            if not self._is_shutting_down():
                print(f"❌ Error guardando persistencia: {e}")
    
    def _is_shutting_down(self) -> bool:
        """
        Detecta si Python está en proceso de shutdown
        
        Returns:
            True si está en shutdown, False en caso contrario
        """
        try:
            # Verificar si los built-ins básicos están disponibles
            import sys
            return (
                not hasattr(__builtins__, 'open') or
                'open' not in dir(__builtins__) or
                getattr(sys, 'is_finalizing', lambda: False)()
            )
        except:
            return True
    
    def graceful_shutdown(self):
        """
        Realiza un shutdown graceful del cache predictivo
        
        Este método debe ser llamado explícitamente antes del cierre
        para guardar los datos de persistencia de forma segura.
        """
        try:
            if self._enable_persistence:
                self._save_persistence_data(force_save=True)
                print("🔄 [Predictive Cache] Shutdown graceful completado")
        except Exception as e:
            print(f"⚠️ [Predictive Cache] Error durante shutdown graceful: {e}")
    
    def __del__(self):
        """
        Destructor que intenta guardado final
        
        Note: Durante shutdown de Python, este método puede ejecutarse
        cuando algunos built-ins ya no están disponibles. Para un guardado
        seguro, use graceful_shutdown() explícitamente.
        """
        # Solo intentar guardado si no estamos en shutdown
        if (hasattr(self, '_enable_persistence') and 
            self._enable_persistence and 
            not self._is_shutting_down()):
            self._save_persistence_data()


if __name__ == "__main__":
    # Test del PredictiveCacheManager
    print("🧠 Testing Predictive Cache Manager...")
    
    cache_manager = PredictiveCacheManager()
    
    try:
        # Test de cacheo
        import sys
        cache_manager.cache_module('sys', module_obj=sys)
        
        # Test de obtención
        cached_sys = cache_manager.get_cached_module('sys')
        print(f"✅ Caché test exitoso: {cached_sys is not None}")
        
        # Test de predicción
        predictions = cache_manager.predict_next_modules('sys')
        print(f"🔮 Predicciones: {predictions}")
        
        # Mostrar estadísticas
        stats = cache_manager.get_cache_stats()
        print(f"📊 Stats: Hit rate = {stats['cache_performance']['hit_rate_percent']:.1f}%")
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
    
    print("🎯 Predictive Cache Manager test completado")
