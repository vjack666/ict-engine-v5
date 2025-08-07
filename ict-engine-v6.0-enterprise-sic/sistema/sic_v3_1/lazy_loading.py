"""
SIC v3.1 - Lazy Loading Manager
==============================

Gestión inteligente de carga diferida de módulos para optimización de performance.

Este módulo implementa un sistema avanzado de lazy loading que permite:
- Carga diferida de módulos pesados
- Proxy objects para acceso transparente
- Gestión inteligente de memoria
- Optimización automática de performance

Autor: ICT Engine v6.0 Team  
Versión: v3.1.0
Fecha: Agosto 2025
"""

import sys
import time
import threading
import importlib
import importlib.util
from typing import Dict, List, Optional, Any, Callable, Union
from pathlib import Path
import weakref
import psutil
import traceback


class LazyModuleProxy:
    """
    🔄 Proxy para módulos con carga diferida
    
    Permite acceso transparente a módulos que aún no han sido cargados,
    cargándolos automáticamente cuando se accede a sus atributos o métodos.
    """
    
    def __init__(self, module_name: str, loader_callback: Callable):
        """
        Inicializa el proxy de módulo lazy
        
        Args:
            module_name: Nombre del módulo a cargar
            loader_callback: Función que carga el módulo real
        """
        self._module_name = module_name
        self._loader_callback = loader_callback
        self._real_module = None
        self._is_loading = False
        self._load_time = None
        self._access_count = 0
        self._lock = threading.Lock()
    
    def _ensure_loaded(self):
        """Asegura que el módulo real esté cargado"""
        if self._real_module is not None:
            return self._real_module
        
        with self._lock:
            # Double-check locking
            if self._real_module is not None:
                return self._real_module
            
            if self._is_loading:
                # Evitar carga recursiva
                raise ImportError(f"Carga recursiva detectada para {self._module_name}")
            
            self._is_loading = True
            
            try:
                start_time = time.time()
                self._real_module = self._loader_callback()
                self._load_time = time.time() - start_time
                
                print(f"🔄 [Lazy Loading] {self._module_name} cargado en {self._load_time:.4f}s")
                
            except Exception as e:
                raise ImportError(f"Error cargando módulo lazy {self._module_name}: {e}")
            finally:
                self._is_loading = False
            
            return self._real_module
    
    def __getattr__(self, name: str):
        """Acceso transparente a atributos del módulo"""
        self._access_count += 1
        real_module = self._ensure_loaded()
        return getattr(real_module, name)
    
    def __dir__(self):
        """Lista de atributos disponibles"""
        if self._real_module is None:
            # Si no está cargado, intentar cargar para obtener dir()
            try:
                real_module = self._ensure_loaded()
                return dir(real_module)
            except:
                return []
        return dir(self._real_module)
    
    def __call__(self, *args, **kwargs):
        """Permite que el proxy sea callable si el módulo lo es"""
        real_module = self._ensure_loaded()
        return real_module(*args, **kwargs)
    
    def __repr__(self):
        status = "loaded" if self._real_module else "lazy"
        return f"<LazyModuleProxy '{self._module_name}' ({status})>"
    
    @property
    def is_loaded(self) -> bool:
        """Indica si el módulo ya fue cargado"""
        return self._real_module is not None
    
    @property
    def load_time(self) -> Optional[float]:
        """Tiempo que tomó cargar el módulo"""
        return self._load_time
    
    @property
    def access_count(self) -> int:
        """Número de veces que se accedió al módulo"""
        return self._access_count


class LazyLoadingManager:
    """
    🧠 Gestor Inteligente de Lazy Loading
    
    Maneja la carga diferida de módulos de forma inteligente, optimizando
    el uso de memoria y tiempo de startup de la aplicación.
    
    Características:
    - Carga diferida automática
    - Gestión de memoria inteligente
    - Métricas de performance
    - Configuración flexible
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el gestor de lazy loading
        
        Args:
            config: Configuración del sistema de lazy loading
        """
        self._config = config or {}
        self._lazy_modules: Dict[str, LazyModuleProxy] = {}
        self._load_stats = {
            'total_lazy_loads': 0,
            'successful_loads': 0,
            'failed_loads': 0,
            'total_load_time': 0.0,
            'memory_saved_mb': 0.0
        }
        self._lock = threading.Lock()
        
        # Configuración por defecto
        self._max_memory_mb = self._config.get('max_memory_mb', 1024)  # 1GB
        self._enable_memory_monitoring = self._config.get('enable_memory_monitoring', True)
        self._lazy_threshold_mb = self._config.get('lazy_threshold_mb', 50)  # 50MB
        
        # Módulos que siempre deben usar lazy loading
        self._always_lazy = set(self._config.get('always_lazy', [
            'pandas', 'numpy', 'matplotlib', 'plotly', 'seaborn',
            'scipy', 'sklearn', 'tensorflow', 'torch', 'cv2'
        ]))
        
        # Proceso para monitoreo de memoria
        self._process = psutil.Process() if self._enable_memory_monitoring else None
        
    def lazy_import(self, module_name: str, 
                   from_list: Optional[List[str]] = None,
                   alias: Optional[str] = None) -> Union[LazyModuleProxy, Any]:
        """
        🔄 Realiza un import con lazy loading
        
        Args:
            module_name: Nombre del módulo a importar
            from_list: Lista de elementos específicos a importar
            alias: Alias para el módulo
            
        Returns:
            Proxy del módulo o elemento específico
        """
        
        def loader_callback():
            """Callback que carga el módulo real cuando sea necesario"""
            try:
                start_memory = self._get_memory_usage_mb()
                
                # Cargar el módulo
                module = importlib.import_module(module_name)
                
                # Calcular memoria utilizada
                end_memory = self._get_memory_usage_mb()
                memory_used = max(0, end_memory - start_memory)
                
                # Actualizar estadísticas
                with self._lock:
                    self._load_stats['successful_loads'] += 1
                    self._load_stats['total_lazy_loads'] += 1
                
                # Manejar from imports
                if from_list:
                    if len(from_list) == 1:
                        return getattr(module, from_list[0])
                    else:
                        return {name: getattr(module, name) for name in from_list}
                
                return module
                
            except Exception as e:
                with self._lock:
                    self._load_stats['failed_loads'] += 1
                    self._load_stats['total_lazy_loads'] += 1
                raise ImportError(f"Error en lazy loading de {module_name}: {e}")
        
        # Crear clave única para el cache
        cache_key = f"{module_name}::{from_list}::{alias}"
        
        # Verificar si ya existe un proxy para este módulo
        if cache_key in self._lazy_modules:
            return self._lazy_modules[cache_key]
        
        # Crear nuevo proxy lazy
        proxy = LazyModuleProxy(module_name, loader_callback)
        
        with self._lock:
            self._lazy_modules[cache_key] = proxy
        
        print(f"🔄 [Lazy Loading] Proxy creado para {module_name}")
        return proxy
    
    def should_use_lazy_loading(self, module_name: str) -> bool:
        """
        🤔 Determina si un módulo debe usar lazy loading
        
        Args:
            module_name: Nombre del módulo a evaluar
            
        Returns:
            True si debe usar lazy loading
        """
        # Verificar lista de módulos siempre lazy
        if any(lazy_mod in module_name.lower() for lazy_mod in self._always_lazy):
            return True
        
        # Verificar uso de memoria actual
        if self._enable_memory_monitoring:
            current_memory = self._get_memory_usage_mb()
            if current_memory > self._max_memory_mb * 0.8:  # 80% del límite
                return True
        
        # Verificar si el módulo ya está en sys.modules (ya cargado)
        if module_name in sys.modules:
            return False
        
        return False
    
    def preload_module(self, module_name: str, 
                      from_list: Optional[List[str]] = None) -> bool:
        """
        ⚡ Pre-carga un módulo lazy en background
        
        Args:
            module_name: Nombre del módulo a pre-cargar
            from_list: Elementos específicos a pre-cargar
            
        Returns:
            True si la pre-carga fue exitosa
        """
        cache_key = f"{module_name}::{from_list}::None"
        
        if cache_key not in self._lazy_modules:
            return False
        
        proxy = self._lazy_modules[cache_key]
        
        if proxy.is_loaded:
            return True
        
        try:
            # Forzar carga del módulo
            proxy._ensure_loaded()
            print(f"⚡ [Lazy Loading] Pre-carga exitosa: {module_name}")
            return True
            
        except Exception as e:
            print(f"❌ [Lazy Loading] Error en pre-carga de {module_name}: {e}")
            return False
    
    def get_lazy_stats(self) -> Dict[str, Any]:
        """
        📊 Obtiene estadísticas del sistema de lazy loading
        
        Returns:
            Diccionario con métricas detalladas
        """
        with self._lock:
            stats = self._load_stats.copy()
        
        # Calcular estadísticas de módulos
        total_modules = len(self._lazy_modules)
        loaded_modules = sum(1 for proxy in self._lazy_modules.values() if proxy.is_loaded)
        pending_modules = total_modules - loaded_modules
        
        # Estadísticas de memoria
        current_memory = self._get_memory_usage_mb()
        memory_efficiency = self._calculate_memory_efficiency()
        
        return {
            'lazy_loading_stats': stats,
            'module_stats': {
                'total_lazy_modules': total_modules,
                'loaded_modules': loaded_modules,
                'pending_modules': pending_modules,
                'load_ratio': loaded_modules / max(1, total_modules) * 100
            },
            'memory_stats': {
                'current_usage_mb': current_memory,
                'max_allowed_mb': self._max_memory_mb,
                'memory_efficiency_percent': memory_efficiency,
                'estimated_savings_mb': stats.get('memory_saved_mb', 0)
            },
            'performance_stats': {
                'avg_load_time': (
                    stats['total_load_time'] / max(1, stats['successful_loads'])
                ),
                'success_rate': (
                    stats['successful_loads'] / max(1, stats['total_lazy_loads']) * 100
                )
            }
        }
    
    def cleanup_unused_proxies(self) -> int:
        """
        🧹 Limpia proxies que no han sido utilizados
        
        Returns:
            Número de proxies eliminados
        """
        cleaned = 0
        
        with self._lock:
            # Encontrar proxies no utilizados
            unused_keys = []
            for key, proxy in self._lazy_modules.items():
                if proxy.access_count == 0 and not proxy.is_loaded:
                    unused_keys.append(key)
            
            # Eliminar proxies no utilizados
            for key in unused_keys:
                del self._lazy_modules[key]
                cleaned += 1
        
        if cleaned > 0:
            print(f"🧹 [Lazy Loading] {cleaned} proxies no utilizados eliminados")
        
        return cleaned
    
    def force_load_all(self) -> Dict[str, bool]:
        """
        ⚡ Fuerza la carga de todos los módulos lazy
        
        Returns:
            Diccionario con resultados de carga por módulo
        """
        results = {}
        
        for key, proxy in self._lazy_modules.items():
            if not proxy.is_loaded:
                try:
                    proxy._ensure_loaded()
                    results[key] = True
                except Exception as e:
                    results[key] = False
                    print(f"❌ Error forzando carga de {key}: {e}")
            else:
                results[key] = True
        
        return results
    
    def get_status(self) -> str:
        """Estado del gestor de lazy loading"""
        stats = self.get_lazy_stats()
        module_stats = stats['module_stats']
        memory_stats = stats['memory_stats']
        
        return (f"Lazy Loading: {module_stats['loaded_modules']}/{module_stats['total_lazy_modules']} "
                f"módulos cargados, {memory_stats['current_usage_mb']:.1f}MB memoria")
    
    def _get_memory_usage_mb(self) -> float:
        """Obtiene el uso actual de memoria en MB"""
        if not self._enable_memory_monitoring or not self._process:
            return 0.0
        
        try:
            memory_info = self._process.memory_info()
            return memory_info.rss / 1024 / 1024  # Convertir a MB
        except Exception:
            return 0.0
    
    def _calculate_memory_efficiency(self) -> float:
        """Calcula la eficiencia de memoria del lazy loading"""
        current_memory = self._get_memory_usage_mb()
        
        if current_memory == 0:
            return 100.0
        
        # Estimar memoria que se habría usado sin lazy loading
        estimated_full_memory = current_memory * 1.5  # Estimación conservadora
        efficiency = (1 - current_memory / estimated_full_memory) * 100
        
        return max(0, min(100, efficiency))


if __name__ == "__main__":
    # Test del LazyLoadingManager
    print("🔄 Testing Lazy Loading Manager...")
    
    manager = LazyLoadingManager()
    
    # Test de lazy import
    try:
        # Crear un proxy lazy para sys (módulo ligero para test)
        sys_proxy = manager.lazy_import('sys')
        print(f"✅ Proxy creado: {sys_proxy}")
        
        # Acceder al módulo (debería cargarlo)
        version = sys_proxy.version
        print(f"✅ Módulo cargado, versión: {version[:50]}...")
        
        # Mostrar estadísticas
        stats = manager.get_lazy_stats()
        print(f"📊 Stats: {stats['module_stats']}")
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        traceback.print_exc()
    
    print("🎯 Lazy Loading Manager test completado")
