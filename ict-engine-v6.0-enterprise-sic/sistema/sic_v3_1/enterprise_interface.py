"""
SIC v3.1 Enterprise - Sistema de Imports Inteligente
==================================================

Interface Principal Enterprise para el Sistema de Imports Inteligente v3.1

Este módulo proporciona la API principal para el SIC v3.1 Enterprise,
unificando todas las capacidades avanzadas en una interface limpia y profesional.

Características Enterprise:
- Lazy Loading Inteligente
- Caché Predictivo
- Monitoreo en Tiempo Real  
- Debug Avanzado
- Interface API Limpia

Autor: ICT Engine v6.0 Team
Versión: v3.1.0-enterprise
Fecha: Agosto 2025
"""

import sys
import time
import threading
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
import importlib.util
import traceback

# Importar componentes del SIC v3.1
from .lazy_loading import LazyLoadingManager
from .predictive_cache import PredictiveCacheManager
from .monitor_dashboard import MonitorDashboard
from .advanced_debug import AdvancedDebugger


class SICv31Enterprise:
    """
    🚀 SIC v3.1 Enterprise - Sistema de Imports Inteligente
    
    Interface principal que unifica todas las capacidades enterprise
    del Sistema de Imports Inteligente v3.1.
    
    Funcionalidades:
    - Gestión inteligente de imports con lazy loading
    - Caché predictivo para optimización de performance
    - Monitoreo en tiempo real del sistema
    - Debug avanzado con métricas detalladas
    - API enterprise limpia y profesional
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el SIC v3.1 Enterprise
        
        Args:
            config: Configuración opcional del sistema
        """
        self._config = config or {}
        self._is_initialized = False
        self._start_time = time.time()
        
        # Componentes principales del SIC v3.1
        self._lazy_manager = None
        self._cache_manager = None
        self._monitor = None
        self._debugger = None
        
        # Estado del sistema
        self._stats = {
            'imports_realizados': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'tiempo_total_carga': 0.0,
            'modulos_activos': set(),
            'errores_capturados': []
        }
        
        # Thread safety
        self._lock = threading.Lock()
        
        # Inicializar componentes
        self._initialize_components()
        
    def _initialize_components(self):
        """Inicializa todos los componentes del SIC v3.1"""
        try:
            # Lazy Loading Manager
            self._lazy_manager = LazyLoadingManager(
                config=self._config.get('lazy_loading', {})
            )
            
            # Predictive Cache Manager
            self._cache_manager = PredictiveCacheManager(
                config=self._config.get('predictive_cache', {})
            )
            
            # Monitor Dashboard
            self._monitor = MonitorDashboard(
                config=self._config.get('monitor', {})
            )
            
            # Advanced Debugger
            self._debugger = AdvancedDebugger(
                config=self._config.get('debug', {})
            )
            
            self._is_initialized = True
            self._log_system_event("SIC v3.1 Enterprise inicializado correctamente")
            
        except Exception as e:
            self._handle_error(f"Error inicializando SIC v3.1: {e}")
            raise
    
    def smart_import(self, module_name: str, 
                    from_list: Optional[List[str]] = None,
                    alias: Optional[str] = None,
                    priority: str = 'normal') -> Any:
        """
        🧠 Import Inteligente Enterprise
        
        Realiza imports utilizando todas las capacidades del SIC v3.1:
        - Lazy loading cuando sea apropiado
        - Caché predictivo
        - Monitoreo en tiempo real
        - Debug automático
        
        Args:
            module_name: Nombre del módulo a importar
            from_list: Lista de elementos específicos a importar
            alias: Alias opcional para el módulo
            priority: Prioridad del import ('high', 'normal', 'low')
            
        Returns:
            El módulo o elementos importados
        """
        start_time = time.time()
        
        try:
            with self._lock:
                self._stats['imports_realizados'] += 1
            
            # 1. Verificar caché predictivo
            cached_result = self._cache_manager.get_cached_module(
                module_name, from_list, alias
            )
            
            if cached_result is not None:
                with self._lock:
                    self._stats['cache_hits'] += 1
                self._log_import_event(f"Cache HIT: {module_name}", start_time)
                return cached_result
            
            with self._lock:
                self._stats['cache_misses'] += 1
            
            # 2. Decidir estrategia de carga
            if priority == 'low' or self._should_use_lazy_loading(module_name):
                # Usar lazy loading
                result = self._lazy_manager.lazy_import(
                    module_name, from_list, alias
                )
            else:
                # Import inmediato
                result = self._immediate_import(module_name, from_list, alias)
            
            # 3. Guardar en caché predictivo
            self._cache_manager.cache_module(
                module_name, from_list, alias, result
            )
            
            # 4. Actualizar estadísticas
            load_time = time.time() - start_time
            with self._lock:
                self._stats['tiempo_total_carga'] += load_time
                self._stats['modulos_activos'].add(module_name)
            
            # 5. Logging y monitoreo
            self._log_import_event(f"Import exitoso: {module_name}", start_time)
            self._monitor.record_import(module_name, load_time, from_list, alias)
            
            return result
            
        except Exception as e:
            error_msg = f"Error en smart_import de {module_name}: {e}"
            self._handle_error(error_msg)
            raise ImportError(error_msg) from e
    
    def _immediate_import(self, module_name: str, 
                         from_list: Optional[List[str]] = None,
                         alias: Optional[str] = None) -> Any:
        """Realiza un import inmediato tradicional"""
        try:
            # Import básico del módulo
            module = importlib.import_module(module_name)
            
            # Manejar from imports
            if from_list:
                if len(from_list) == 1:
                    return getattr(module, from_list[0])
                else:
                    return {name: getattr(module, name) for name in from_list}
            
            return module
            
        except Exception as e:
            raise ImportError(f"Error en import inmediato de {module_name}: {e}")
    
    def _should_use_lazy_loading(self, module_name: str) -> bool:
        """Determina si un módulo debe usar lazy loading"""
        # Módulos pesados que se benefician de lazy loading
        heavy_modules = [
            'pandas', 'numpy', 'matplotlib', 'scipy', 'tensorflow',
            'torch', 'sklearn', 'plotly', 'seaborn'
        ]
        
        return any(heavy in module_name.lower() for heavy in heavy_modules)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """
        📊 Obtiene estadísticas completas del sistema
        
        Returns:
            Diccionario con todas las métricas del SIC v3.1
        """
        uptime = time.time() - self._start_time
        
        with self._lock:
            stats = self._stats.copy()
        
        return {
            'sic_version': 'v3.1.0-enterprise',
            'uptime_seconds': uptime,
            'uptime_formatted': self._format_uptime(uptime),
            'is_initialized': self._is_initialized,
            'imports_stats': {
                'total_imports': stats['imports_realizados'],
                'cache_hits': stats['cache_hits'],
                'cache_misses': stats['cache_misses'],
                'cache_hit_rate': (
                    stats['cache_hits'] / max(1, stats['imports_realizados']) * 100
                ),
                'avg_load_time': (
                    stats['tiempo_total_carga'] / max(1, stats['imports_realizados'])
                ),
                'total_load_time': stats['tiempo_total_carga']
            },
            'active_modules': list(stats['modulos_activos']),
            'error_count': len(stats['errores_capturados']),
            'component_status': {
                'lazy_manager': self._lazy_manager.get_status() if self._lazy_manager else 'Not initialized',
                'cache_manager': self._cache_manager.get_status() if self._cache_manager else 'Not initialized',
                'monitor': self._monitor.get_status() if self._monitor else 'Not initialized',
                'debugger': self._debugger.get_status() if self._debugger else 'Not initialized'
            }
        }
    
    def get_lazy_loading_manager(self):
        """🔄 Obtiene el gestor de lazy loading"""
        return self._lazy_manager
    
    def get_predictive_cache_manager(self):
        """🧠 Obtiene el gestor de cache predictivo"""
        return self._cache_manager
    
    def get_monitor(self):
        """📊 Obtiene el monitor del sistema"""
        return self._monitor
    
    def get_debugger(self):
        """🔧 Obtiene el debugger avanzado"""
        return self._debugger
    
    def enable_debug_mode(self, level: str = 'info'):
        """
        🔧 Habilita el modo debug avanzado
        
        Args:
            level: Nivel de debug ('debug', 'info', 'warning', 'error')
        """
        if self._debugger:
            self._debugger.set_debug_level(level)
            self._log_system_event(f"Debug mode enabled: {level}")
    
    def get_debug_report(self) -> Dict[str, Any]:
        """
        📋 Genera un reporte completo de debug
        
        Returns:
            Reporte detallado del estado del sistema
        """
        if not self._debugger:
            return {'error': 'Debugger not initialized'}
        
        return self._debugger.generate_full_report()
    
    def _log_import_event(self, message: str, start_time: float):
        """Log de eventos de import"""
        duration = time.time() - start_time
        log_msg = f"[SIC v3.1] {message} (⏱️ {duration:.4f}s)"
        print(log_msg)  # Por ahora, luego integramos con SLUC v2.1
    
    def _log_system_event(self, message: str):
        """Log de eventos del sistema"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] [SIC v3.1 Enterprise] {message}"
        print(log_msg)  # Por ahora, luego integramos con SLUC v2.1
    
    def _handle_error(self, error_msg: str):
        """Manejo centralizado de errores"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        error_entry = {
            'timestamp': timestamp,
            'message': error_msg,
            'traceback': traceback.format_exc()
        }
        
        with self._lock:
            self._stats['errores_capturados'].append(error_entry)
        
        self._log_system_event(f"ERROR: {error_msg}")
        
        if self._debugger:
            self._debugger.log_error(error_entry)
    
    def _format_uptime(self, seconds: float) -> str:
        """Formatea el tiempo de actividad en formato legible"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def shutdown(self):
        """Apaga el sistema SIC v3.1 limpiamente"""
        self._log_system_event("Iniciando shutdown del SIC v3.1 Enterprise")
        
        if self._monitor:
            self._monitor.shutdown()
        
        if self._cache_manager:
            self._cache_manager.clear_cache()
        
        if self._debugger:
            self._debugger.save_session_log()
        
        self._log_system_event("SIC v3.1 Enterprise shutdown completado")


# Instance global del SIC v3.1 Enterprise
_sic_instance: Optional[SICv31Enterprise] = None


def get_sic_instance(config: Optional[Dict[str, Any]] = None) -> SICv31Enterprise:
    """
    🌟 Obtiene la instancia global del SIC v3.1 Enterprise
    
    Args:
        config: Configuración opcional (solo se usa en la primera llamada)
        
    Returns:
        Instancia del SIC v3.1 Enterprise
    """
    global _sic_instance
    
    if _sic_instance is None:
        _sic_instance = SICv31Enterprise(config)
    
    return _sic_instance


def smart_import(module_name: str, 
                from_list: Optional[List[str]] = None,
                alias: Optional[str] = None,
                priority: str = 'normal') -> Any:
    """
    🚀 Función de conveniencia para imports inteligentes
    
    Esta es la función principal que debe usar el resto del sistema
    para realizar imports utilizando todas las capacidades del SIC v3.1.
    
    Args:
        module_name: Nombre del módulo a importar
        from_list: Lista de elementos específicos a importar  
        alias: Alias opcional para el módulo
        priority: Prioridad del import ('high', 'normal', 'low')
        
    Returns:
        El módulo o elementos importados
        
    Example:
        # Import simple
        pd = smart_import('pandas', alias='pd')
        
        # From import
        plt = smart_import('matplotlib.pyplot', alias='plt')
        
        # Import específico
        train_test_split = smart_import('sklearn.model_selection', 
                                       from_list=['train_test_split'])
        
        # Import con prioridad baja (lazy loading)
        heavy_module = smart_import('some.heavy.module', priority='low')
    """
    sic = get_sic_instance()
    return sic.smart_import(module_name, from_list, alias, priority)


# Alias para compatibilidad
sic_import = smart_import


if __name__ == "__main__":
    # Test básico del SIC v3.1
    print("🚀 Testing SIC v3.1 Enterprise...")
    
    # Inicializar SIC
    sic = get_sic_instance()
    
    # Test de import
    try:
        sys_module = smart_import('sys')
        print("✅ Import test exitoso")
        
        # Mostrar estadísticas
        stats = sic.get_system_stats()
        print(f"📊 Stats: {stats['imports_stats']}")
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
    
    print("🎯 SIC v3.1 Enterprise test completado")
