"""
SIC v3.1 - Advanced Debugger
============================

Sistema de debugging avanzado para el Sistema de Imports Inteligente.

Este módulo proporciona:
- Debug detallado de operaciones de import
- Análisis de dependencias y problemas
- Logging estructurado de eventos
- Herramientas de diagnóstico avanzado
- Reportes detallados de problemas

Autor: ICT Engine v6.0 Team
Versión: v3.1.0
Fecha: Agosto 2025
"""

import sys
import time
import threading
import traceback
import inspect
import json
import logging
from typing import Dict, List, Optional, Any, Tuple, Set, Callable
from pathlib import Path
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from datetime import datetime
import importlib.util
import gc
import weakref


@dataclass
class DebugEvent:
    """🔧 Evento de debug detallado"""
    timestamp: float
    event_type: str  # 'import', 'error', 'warning', 'info'
    module_name: str
    function_name: Optional[str]
    line_number: Optional[int]
    message: str
    details: Dict[str, Any]
    stack_trace: Optional[str] = None
    memory_snapshot: Optional[Dict[str, Any]] = None


class DependencyAnalyzer:
    """🔍 Analizador de dependencias de módulos"""
    
    def __init__(self):
        """Inicializa el analizador de dependencias"""
        self._dependency_graph = defaultdict(set)
        self._reverse_deps = defaultdict(set)
        self._circular_deps = set()
        self._analyzed_modules = set()
    
    def analyze_module_dependencies(self, module_name: str) -> Dict[str, Any]:
        """
        🔍 Analiza las dependencias de un módulo
        
        Args:
            module_name: Nombre del módulo a analizar
            
        Returns:
            Análisis detallado de dependencias
        """
        if module_name in self._analyzed_modules:
            return self._get_cached_analysis(module_name)
        
        analysis = {
            'module_name': module_name,
            'direct_dependencies': set(),
            'indirect_dependencies': set(),
            'circular_dependencies': set(),
            'dependency_depth': 0,
            'potential_issues': []
        }
        
        try:
            # Obtener el módulo si ya está cargado
            if module_name in sys.modules:
                module = sys.modules[module_name]
                analysis['direct_dependencies'] = self._extract_module_dependencies(module)
            else:
                # Intentar cargar y analizar
                try:
                    spec = importlib.util.find_spec(module_name)
                    if spec and spec.origin:
                        analysis['direct_dependencies'] = self._analyze_source_dependencies(spec.origin)
                except Exception as e:
                    analysis['potential_issues'].append(f"Error analizando spec: {e}")
            
            # Detectar dependencias circulares
            analysis['circular_dependencies'] = self._detect_circular_dependencies(
                module_name, analysis['direct_dependencies']
            )
            
            # Calcular profundidad de dependencias
            analysis['dependency_depth'] = self._calculate_dependency_depth(module_name)
            
            # Actualizar grafos internos
            self._dependency_graph[module_name] = analysis['direct_dependencies']
            for dep in analysis['direct_dependencies']:
                self._reverse_deps[dep].add(module_name)
            
            self._analyzed_modules.add(module_name)
            
        except Exception as e:
            analysis['potential_issues'].append(f"Error en análisis: {e}")
        
        return analysis
    
    def _extract_module_dependencies(self, module) -> Set[str]:
        """Extrae dependencias de un módulo cargado"""
        dependencies = set()
        
        try:
            # Analizar atributos del módulo
            for attr_name in dir(module):
                try:
                    attr = getattr(module, attr_name)
                    if hasattr(attr, '__module__') and attr.__module__:
                        if attr.__module__ != module.__name__:
                            # Obtener el módulo base
                            base_module = attr.__module__.split('.')[0]
                            if base_module not in ['builtins', '__main__']:
                                dependencies.add(base_module)
                except:
                    continue
        except Exception:
            pass
        
        return dependencies
    
    def _analyze_source_dependencies(self, source_path: str) -> Set[str]:
        """Analiza dependencias desde el código fuente"""
        dependencies = set()
        
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Buscar imports básicos
            import re
            
            # import module
            import_patterns = [
                r'import\s+([a-zA-Z_][a-zA-Z0-9_]*)',
                r'from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import',
            ]
            
            for pattern in import_patterns:
                matches = re.findall(pattern, content)
                dependencies.update(matches)
        
        except Exception:
            pass
        
        return dependencies
    
    def _detect_circular_dependencies(self, module_name: str, dependencies: Set[str]) -> Set[str]:
        """Detecta dependencias circulares"""
        circular = set()
        
        for dep in dependencies:
            if self._has_circular_dependency(module_name, dep):
                circular.add(dep)
        
        return circular
    
    def _has_circular_dependency(self, module_a: str, module_b: str, 
                                visited: Optional[Set[str]] = None) -> bool:
        """Verifica si existe dependencia circular entre dos módulos"""
        if visited is None:
            visited = set()
        
        if module_a in visited:
            return True
        
        if module_b not in self._dependency_graph:
            return False
        
        visited.add(module_a)
        
        for dep in self._dependency_graph[module_b]:
            if dep == module_a or self._has_circular_dependency(module_a, dep, visited.copy()):
                return True
        
        return False
    
    def _calculate_dependency_depth(self, module_name: str, 
                                   visited: Optional[Set[str]] = None) -> int:
        """Calcula la profundidad máxima de dependencias"""
        if visited is None:
            visited = set()
        
        if module_name in visited:
            return 0  # Evitar ciclos infinitos
        
        if module_name not in self._dependency_graph:
            return 0
        
        visited.add(module_name)
        max_depth = 0
        
        for dep in self._dependency_graph[module_name]:
            depth = 1 + self._calculate_dependency_depth(dep, visited.copy())
            max_depth = max(max_depth, depth)
        
        return max_depth
    
    def _get_cached_analysis(self, module_name: str) -> Dict[str, Any]:
        """Obtiene análisis cacheado de un módulo"""
        return {
            'module_name': module_name,
            'direct_dependencies': self._dependency_graph.get(module_name, set()),
            'circular_dependencies': set(),
            'dependency_depth': self._calculate_dependency_depth(module_name),
            'cached': True
        }


class AdvancedDebugger:
    """
    🔧 Debugger Avanzado del SIC v3.1
    
    Proporciona herramientas de debugging detallado para el Sistema
    de Imports Inteligente, incluyendo análisis de dependencias,
    logging estructurado y diagnóstico de problemas.
    
    Características:
    - Debug detallado de imports
    - Análisis de dependencias
    - Logging estructurado
    - Detección de problemas
    - Reportes de diagnóstico
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el debugger avanzado
        
        Args:
            config: Configuración del debugger
        """
        self._config = config or {}
        self._debug_level = self._config.get('debug_level', 'info')
        self._enable_detailed_logging = self._config.get('enable_detailed_logging', True)
        self._max_events = self._config.get('max_events', 1000)
        
        # Almacenamiento de eventos
        self._debug_events = deque(maxlen=self._max_events)
        self._error_history = deque(maxlen=100)
        self._performance_metrics = defaultdict(list)
        
        # Analizador de dependencias
        self._dependency_analyzer = DependencyAnalyzer()
        
        # Threading
        self._lock = threading.Lock()
        
        # Logger estructurado
        self._setup_structured_logger()
        
        # Estadísticas de debug
        self._debug_stats = {
            'total_events': 0,
            'errors_logged': 0,
            'warnings_logged': 0,
            'performance_samples': 0,
            'dependency_analyses': 0
        }
        
        # Sistema de hooks para interceptar operaciones
        self._import_hooks = []
        self._error_hooks = []
        
        print(f"🔧 [Advanced Debugger] Inicializado (nivel: {self._debug_level})")
    
    def set_debug_level(self, level: str):
        """
        🎚️ Establece el nivel de debug
        
        Args:
            level: Nivel de debug ('debug', 'info', 'warning', 'error')
        """
        valid_levels = ['debug', 'info', 'warning', 'error']
        if level.lower() in valid_levels:
            self._debug_level = level.lower()
            self._logger.setLevel(getattr(logging, level.upper()))
            print(f"🎚️ [Advanced Debugger] Nivel establecido: {level}")
        else:
            print(f"❌ Nivel de debug inválido: {level}. Usar: {valid_levels}")
    
    def log_import_debug(self, module_name: str, import_type: str,
                        operation: str, duration: float,
                        success: bool, details: Optional[Dict[str, Any]] = None,
                        error: Optional[Exception] = None):
        """
        📝 Log detallado de operación de import
        
        Args:
            module_name: Nombre del módulo
            import_type: Tipo de import ('normal', 'lazy', 'cached')
            operation: Operación realizada ('load', 'cache_hit', 'lazy_create', etc.)
            duration: Tiempo que tomó la operación
            success: Si la operación fue exitosa
            details: Detalles adicionales
            error: Excepción si hubo error
        """
        timestamp = time.time()
        
        # Crear evento de debug
        debug_event = DebugEvent(
            timestamp=timestamp,
            event_type='import',
            module_name=module_name,
            function_name=operation,
            line_number=None,
            message=f"{import_type.upper()} {operation} for {module_name}",
            details={
                'import_type': import_type,
                'operation': operation,
                'duration': duration,
                'success': success,
                'error_type': type(error).__name__ if error else None,
                'error_message': str(error) if error else None,
                **(details or {})
            },
            stack_trace=traceback.format_exc() if error else None,
            memory_snapshot=self._take_memory_snapshot() if self._enable_detailed_logging else None
        )
        
        with self._lock:
            self._debug_events.append(debug_event)
            self._debug_stats['total_events'] += 1
            
            if not success:
                self._debug_stats['errors_logged'] += 1
                self._error_history.append(debug_event)
            
            # Registrar métricas de performance
            self._performance_metrics[f"{import_type}_{operation}"].append(duration)
            self._debug_stats['performance_samples'] += 1
        
        # Log estructurado
        log_level = logging.ERROR if error else logging.INFO
        self._logger.log(log_level, 
                        f"[{import_type.upper()}] {operation}: {module_name} "
                        f"({duration:.4f}s) {'✅' if success else '❌'}",
                        extra={
                            'module_name': module_name,
                            'import_type': import_type,
                            'operation': operation,
                            'duration': duration,
                            'success': success,
                            'details': details
                        })
    
    def analyze_import_dependencies(self, module_name: str) -> Dict[str, Any]:
        """
        🔍 Analiza las dependencias de un módulo
        
        Args:
            module_name: Nombre del módulo a analizar
            
        Returns:
            Análisis detallado de dependencias
        """
        with self._lock:
            self._debug_stats['dependency_analyses'] += 1
        
        analysis = self._dependency_analyzer.analyze_module_dependencies(module_name)
        
        # Log del análisis
        if analysis.get('potential_issues'):
            self._logger.warning(f"Problemas detectados en {module_name}: {analysis['potential_issues']}")
        
        if analysis.get('circular_dependencies'):
            self._logger.warning(f"Dependencias circulares detectadas en {module_name}: {analysis['circular_dependencies']}")
        
        # Crear evento de debug
        debug_event = DebugEvent(
            timestamp=time.time(),
            event_type='info',
            module_name=module_name,
            function_name='dependency_analysis',
            line_number=None,
            message=f"Dependency analysis for {module_name}",
            details=analysis
        )
        
        with self._lock:
            self._debug_events.append(debug_event)
        
        return analysis
    
    def diagnose_import_problem(self, module_name: str, 
                               error: Exception) -> Dict[str, Any]:
        """
        🩺 Diagnostica problemas de import
        
        Args:
            module_name: Nombre del módulo problemático
            error: Excepción que se produjo
            
        Returns:
            Diagnóstico detallado del problema
        """
        diagnosis = {
            'module_name': module_name,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'possible_causes': [],
            'suggested_solutions': [],
            'related_modules': [],
            'system_info': self._get_system_diagnostic_info()
        }
        
        # Análisis específico según tipo de error
        if isinstance(error, ImportError):
            diagnosis['possible_causes'].extend([
                'Módulo no instalado',
                'Módulo no en el PYTHONPATH',
                'Dependencias faltantes',
                'Versión incompatible'
            ])
            diagnosis['suggested_solutions'].extend([
                f'pip install {module_name}',
                'Verificar PYTHONPATH',
                'Verificar versiones de dependencias',
                'Verificar nombre del módulo'
            ])
        
        elif isinstance(error, ModuleNotFoundError):
            diagnosis['possible_causes'].extend([
                'Módulo no existe',
                'Typo en el nombre',
                'Módulo no instalado'
            ])
            diagnosis['suggested_solutions'].extend([
                'Verificar nombre del módulo',
                f'pip install {module_name}',
                'Verificar documentación del módulo'
            ])
        
        elif isinstance(error, AttributeError):
            diagnosis['possible_causes'].extend([
                'Atributo no existe en el módulo',
                'Versión incorrecta del módulo',
                'Import parcial fallido'
            ])
        
        # Analizar dependencias para más contexto
        try:
            dep_analysis = self.analyze_import_dependencies(module_name)
            diagnosis['dependency_analysis'] = dep_analysis
            
            if dep_analysis.get('circular_dependencies'):
                diagnosis['possible_causes'].append('Dependencias circulares')
                diagnosis['suggested_solutions'].append('Resolver dependencias circulares')
        
        except Exception:
            pass
        
        # Buscar módulos relacionados en errores anteriores
        related_errors = self._find_related_errors(module_name)
        if related_errors:
            diagnosis['related_modules'] = [e.module_name for e in related_errors]
            diagnosis['possible_causes'].append('Problema sistemático con módulos relacionados')
        
        # Log del diagnóstico
        self._logger.error(f"Diagnóstico para {module_name}: {diagnosis['error_type']} - {len(diagnosis['possible_causes'])} causas posibles")
        
        return diagnosis
    
    def log_error(self, error_entry: Dict[str, Any]):
        """
        ❌ Registra un error en el sistema de debug
        
        Args:
            error_entry: Información del error
        """
        debug_event = DebugEvent(
            timestamp=time.time(),
            event_type='error',
            module_name=error_entry.get('module_name', 'unknown'),
            function_name=None,
            line_number=None,
            message=error_entry.get('message', 'Error sin mensaje'),
            details=error_entry,
            stack_trace=error_entry.get('traceback')
        )
        
        with self._lock:
            self._debug_events.append(debug_event)
            self._error_history.append(debug_event)
            self._debug_stats['errors_logged'] += 1
        
        self._logger.error(f"Error registrado: {error_entry.get('message', 'Sin mensaje')}")
    
    def get_debug_summary(self) -> Dict[str, Any]:
        """
        📊 Obtiene resumen del debug
        
        Returns:
            Resumen de actividad de debug
        """
        with self._lock:
            stats = self._debug_stats.copy()
            recent_events = list(self._debug_events)[-50:]  # Últimos 50 eventos
            recent_errors = list(self._error_history)[-10:]  # Últimos 10 errores
        
        # Análisis de performance
        performance_summary = {}
        for operation, durations in self._performance_metrics.items():
            if durations:
                performance_summary[operation] = {
                    'count': len(durations),
                    'avg_duration': sum(durations) / len(durations),
                    'min_duration': min(durations),
                    'max_duration': max(durations)
                }
        
        # Módulos más problemáticos
        error_modules = defaultdict(int)
        for error in recent_errors:
            error_modules[error.module_name] += 1
        
        problematic_modules = sorted(error_modules.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'debug_stats': stats,
            'performance_summary': performance_summary,
            'recent_events_count': len(recent_events),
            'recent_errors_count': len(recent_errors),
            'problematic_modules': problematic_modules,
            'debug_level': self._debug_level,
            'total_modules_analyzed': len(self._dependency_analyzer._analyzed_modules)
        }
    
    def generate_full_report(self) -> Dict[str, Any]:
        """
        📋 Genera reporte completo de debug
        
        Returns:
            Reporte detallado de toda la actividad de debug
        """
        summary = self.get_debug_summary()
        
        with self._lock:
            all_events = [asdict(event) for event in self._debug_events]
            all_errors = [asdict(error) for error in self._error_history]
        
        # Análisis de tendencias
        event_timeline = self._analyze_event_timeline()
        
        # Sistema de información
        system_info = self._get_system_diagnostic_info()
        
        return {
            'timestamp': time.time(),
            'formatted_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'summary': summary,
            'system_info': system_info,
            'event_timeline': event_timeline,
            'recent_events': all_events[-100:],  # Últimos 100 eventos
            'error_history': all_errors,
            'dependency_graph_size': len(self._dependency_analyzer._dependency_graph)
        }
    
    def save_session_log(self, filepath: Optional[str] = None):
        """
        💾 Guarda log de la sesión de debug
        
        Args:
            filepath: Ruta donde guardar el log (opcional)
        """
        if not filepath:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f"sic_debug_session_{timestamp}.json"
        
        try:
            report = self.generate_full_report()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str)
            
            print(f"💾 [Advanced Debugger] Sesión guardada: {filepath}")
            
        except Exception as e:
            print(f"❌ Error guardando sesión de debug: {e}")
    
    def get_status(self) -> str:
        """Estado del debugger avanzado"""
        summary = self.get_debug_summary()
        stats = summary['debug_stats']
        
        return (f"Advanced Debugger: {stats['total_events']} eventos, "
                f"{stats['errors_logged']} errores, "
                f"nivel: {self._debug_level}")
    
    def _setup_structured_logger(self):
        """Configura el logger estructurado"""
        self._logger = logging.getLogger('SIC.AdvancedDebugger')
        self._logger.setLevel(getattr(logging, self._debug_level.upper()))
        
        # Handler para consola si no existe
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
    
    def _take_memory_snapshot(self) -> Dict[str, Any]:
        """Toma snapshot de memoria actual"""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            return {
                'rss_mb': memory_info.rss / 1024 / 1024,
                'vms_mb': memory_info.vms / 1024 / 1024,
                'percent': process.memory_percent(),
                'available_mb': psutil.virtual_memory().available / 1024 / 1024
            }
        except:
            return {'error': 'psutil no disponible'}
    
    def _find_related_errors(self, module_name: str) -> List[DebugEvent]:
        """Encuentra errores relacionados con un módulo"""
        related = []
        
        # Buscar errores en módulos similares o dependencias
        for error in self._error_history:
            if (error.module_name == module_name or 
                module_name in error.module_name or 
                error.module_name in module_name):
                related.append(error)
        
        return related[-5:]  # Últimos 5 relacionados
    
    def _analyze_event_timeline(self) -> Dict[str, Any]:
        """Analiza timeline de eventos"""
        if not self._debug_events:
            return {}
        
        events_by_hour = defaultdict(int)
        errors_by_hour = defaultdict(int)
        
        current_time = time.time()
        
        for event in self._debug_events:
            # Agrupar por hora
            hour_key = int((current_time - event.timestamp) // 3600)
            events_by_hour[hour_key] += 1
            
            if event.event_type == 'error':
                errors_by_hour[hour_key] += 1
        
        return {
            'events_by_hour': dict(events_by_hour),
            'errors_by_hour': dict(errors_by_hour),
            'total_hours_analyzed': max(events_by_hour.keys()) if events_by_hour else 0
        }
    
    def _get_system_diagnostic_info(self) -> Dict[str, Any]:
        """Obtiene información de diagnóstico del sistema"""
        info = {
            'python_version': sys.version,
            'platform': sys.platform,
            'modules_loaded': len(sys.modules),
            'python_path': sys.path[:5],  # Primeros 5 elementos
            'timestamp': time.time()
        }
        
        try:
            import psutil
            process = psutil.Process()
            info.update({
                'memory_mb': process.memory_info().rss / 1024 / 1024,
                'cpu_percent': process.cpu_percent(),
                'threads': process.num_threads()
            })
        except:
            info['psutil_available'] = False
        
        return info


if __name__ == "__main__":
    # Test del AdvancedDebugger
    print("🔧 Testing Advanced Debugger...")
    
    debugger = AdvancedDebugger()
    
    try:
        # Test de log de import
        debugger.log_import_debug(
            module_name='test_module',
            import_type='normal',
            operation='load',
            duration=0.005,
            success=True,
            details={'test': 'data'}
        )
        
        # Test de análisis de dependencias
        dep_analysis = debugger.analyze_import_dependencies('sys')
        print(f"✅ Análisis de dependencias: {len(dep_analysis)} items")
        
        # Test de diagnóstico de error
        test_error = ImportError("Test error for debugging")
        diagnosis = debugger.diagnose_import_problem('fake_module', test_error)
        print(f"✅ Diagnóstico: {len(diagnosis['possible_causes'])} causas posibles")
        
        # Obtener resumen
        summary = debugger.get_debug_summary()
        print(f"✅ Resumen: {summary['debug_stats']['total_events']} eventos registrados")
        
        # Generar reporte
        report = debugger.generate_full_report()
        print(f"✅ Reporte generado: {len(report)} secciones")
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
    
    print("🎯 Advanced Debugger test completado")
