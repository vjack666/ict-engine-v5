"""
SIC v3.1 - Monitor Dashboard
===========================

Dashboard de monitoreo en tiempo real para el Sistema de Imports Inteligente.

Este módulo proporciona:
- Visualización en tiempo real de la actividad de imports
- Métricas de performance del sistema
- Alertas inteligentes sobre problemas
- Reportes detallados de uso

Autor: ICT Engine v6.0 Team
Versión: v3.1.0
Fecha: Agosto 2025
"""

import sys
import time
import threading
import json
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from collections import deque, defaultdict
import psutil
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta


@dataclass
class ImportEvent:
    """📊 Evento de import para el monitoreo"""
    timestamp: float
    module_name: str
    import_type: str  # 'normal', 'lazy', 'cached'
    load_time: float
    from_list: Optional[List[str]]
    alias: Optional[str]
    success: bool
    error_message: Optional[str] = None
    memory_before: float = 0.0
    memory_after: float = 0.0
    cache_hit: bool = False


@dataclass
class SystemMetrics:
    """🔧 Métricas del sistema en un momento dado"""
    timestamp: float
    cpu_percent: float
    memory_mb: float
    memory_percent: float
    active_modules: int
    cache_size: int
    lazy_modules: int


class AlertManager:
    """🚨 Gestor de alertas del sistema"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el gestor de alertas
        
        Args:
            config: Configuración de alertas
        """
        self._config = config or {}
        self._alerts = deque(maxlen=100)  # Últimas 100 alertas
        self._alert_rules = {
            'high_memory': {
                'threshold': self._config.get('memory_threshold_mb', 512),
                'enabled': True,
                'cooldown': 300  # 5 minutos
            },
            'slow_import': {
                'threshold': self._config.get('slow_import_threshold_s', 2.0),
                'enabled': True,
                'cooldown': 60  # 1 minuto
            },
            'cache_miss_rate': {
                'threshold': self._config.get('cache_miss_rate_threshold', 80),  # 80%
                'enabled': True,
                'cooldown': 300  # 5 minutos
            },
            'import_failures': {
                'threshold': self._config.get('failure_rate_threshold', 20),  # 20%
                'enabled': True,
                'cooldown': 180  # 3 minutos
            }
        }
        self._last_alert_time = defaultdict(float)
    
    def check_alerts(self, event: ImportEvent, metrics: SystemMetrics) -> List[str]:
        """
        🚨 Verifica y genera alertas basándose en eventos y métricas
        
        Args:
            event: Evento de import que activó la verificación
            metrics: Métricas actuales del sistema
            
        Returns:
            Lista de alertas generadas
        """
        alerts = []
        current_time = time.time()
        
        # Alerta por uso alto de memoria
        if self._should_alert('high_memory', current_time):
            if metrics.memory_mb > self._alert_rules['high_memory']['threshold']:
                alert_msg = f"Alto uso de memoria: {metrics.memory_mb:.1f}MB (>{self._alert_rules['high_memory']['threshold']}MB)"
                alerts.append(alert_msg)
                self._register_alert('high_memory', alert_msg, current_time)
        
        # Alerta por import lento
        if self._should_alert('slow_import', current_time):
            if event.load_time > self._alert_rules['slow_import']['threshold']:
                alert_msg = f"Import lento detectado: {event.module_name} ({event.load_time:.2f}s)"
                alerts.append(alert_msg)
                self._register_alert('slow_import', alert_msg, current_time)
        
        # Alerta por falla de import
        if not event.success:
            alert_msg = f"Falla de import: {event.module_name} - {event.error_message}"
            alerts.append(alert_msg)
            self._register_alert('import_failure', alert_msg, current_time)
        
        return alerts
    
    def _should_alert(self, rule_name: str, current_time: float) -> bool:
        """Verifica si se debe generar una alerta según el cooldown"""
        if not self._alert_rules[rule_name]['enabled']:
            return False
        
        last_alert = self._last_alert_time[rule_name]
        cooldown = self._alert_rules[rule_name]['cooldown']
        
        return current_time - last_alert > cooldown
    
    def _register_alert(self, rule_name: str, message: str, timestamp: float):
        """Registra una nueva alerta"""
        alert = {
            'rule': rule_name,
            'message': message,
            'timestamp': timestamp,
            'formatted_time': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self._alerts.append(alert)
        self._last_alert_time[rule_name] = timestamp
        
        print(f"🚨 [Monitor] ALERT: {message}")
    
    def get_recent_alerts(self, count: int = 10) -> List[Dict[str, Any]]:
        """Obtiene las alertas más recientes"""
        return list(self._alerts)[-count:]


class MonitorDashboard:
    """
    📊 Dashboard de Monitoreo del SIC v3.1
    
    Proporciona monitoreo en tiempo real, métricas de performance,
    y alertas inteligentes para el Sistema de Imports Inteligente.
    
    Características:
    - Monitoreo en tiempo real de imports
    - Métricas de performance del sistema
    - Alertas automáticas
    - Reportes detallados
    - Visualización de tendencias
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el dashboard de monitoreo
        
        Args:
            config: Configuración del dashboard
        """
        self._config = config or {}
        self._is_active = False
        self._start_time = time.time()
        
        # Almacenamiento de eventos y métricas
        self._import_events = deque(maxlen=1000)  # Últimos 1000 eventos
        self._system_metrics = deque(maxlen=500)   # Últimas 500 métricas (≈1 hora con muestra cada 8s)
        
        # Gestión de alertas
        self._alert_manager = AlertManager(self._config.get('alerts', {}))
        
        # Threading para monitoreo continuo
        self._monitor_thread = None
        self._stop_monitoring = threading.Event()
        self._lock = threading.Lock()
        
        # Configuración de monitoreo
        self._enable_continuous_monitoring = self._config.get('enable_continuous_monitoring', True)
        self._metrics_interval = self._config.get('metrics_interval_seconds', 8)
        
        # Estadísticas agregadas
        self._aggregate_stats = {
            'total_imports': 0,
            'successful_imports': 0,
            'failed_imports': 0,
            'total_load_time': 0.0,
            'cache_hits': 0,
            'cache_misses': 0,
            'lazy_loads': 0,
            'peak_memory_mb': 0.0,
            'avg_cpu_percent': 0.0
        }
        
        # Proceso para métricas del sistema
        try:
            self._process = psutil.Process()
        except:
            self._process = None
            print("⚠️ [Monitor] psutil no disponible, métricas de sistema limitadas")
        
        # Iniciar monitoreo si está habilitado
        if self._enable_continuous_monitoring:
            self.start_monitoring()
    
    def record_import(self, module_name: str, load_time: float,
                     from_list: Optional[List[str]] = None,
                     alias: Optional[str] = None,
                     import_type: str = 'normal',
                     success: bool = True,
                     error_message: Optional[str] = None,
                     cache_hit: bool = False) -> str:
        """
        📝 Registra un evento de import
        
        Args:
            module_name: Nombre del módulo importado
            load_time: Tiempo que tomó la carga
            from_list: Lista de elementos específicos importados
            alias: Alias usado
            import_type: Tipo de import ('normal', 'lazy', 'cached')
            success: Si el import fue exitoso
            error_message: Mensaje de error si falló
            cache_hit: Si fue un hit de caché
            
        Returns:
            ID del evento registrado
        """
        timestamp = time.time()
        
        # Obtener métricas de memoria
        memory_before = self._get_memory_usage_mb()
        
        # Crear evento
        event = ImportEvent(
            timestamp=timestamp,
            module_name=module_name,
            import_type=import_type,
            load_time=load_time,
            from_list=from_list,
            alias=alias,
            success=success,
            error_message=error_message,
            memory_before=memory_before,
            memory_after=memory_before,  # Se actualizará si es necesario
            cache_hit=cache_hit
        )
        
        with self._lock:
            # Registrar evento
            self._import_events.append(event)
            
            # Actualizar estadísticas agregadas
            self._aggregate_stats['total_imports'] += 1
            
            if success:
                self._aggregate_stats['successful_imports'] += 1
                self._aggregate_stats['total_load_time'] += load_time
            else:
                self._aggregate_stats['failed_imports'] += 1
            
            if cache_hit:
                self._aggregate_stats['cache_hits'] += 1
            else:
                self._aggregate_stats['cache_misses'] += 1
            
            if import_type == 'lazy':
                self._aggregate_stats['lazy_loads'] += 1
        
        # Verificar alertas
        current_metrics = self._get_current_system_metrics()
        alerts = self._alert_manager.check_alerts(event, current_metrics)
        
        # ID del evento
        event_id = f"{timestamp}_{module_name}"
        
        return event_id
    
    def get_real_time_stats(self) -> Dict[str, Any]:
        """
        📊 Obtiene estadísticas en tiempo real
        
        Returns:
            Diccionario con métricas actuales del sistema
        """
        with self._lock:
            # Estadísticas de imports
            recent_events = list(self._import_events)[-100:]  # Últimos 100 eventos
            
            if recent_events:
                recent_load_times = [e.load_time for e in recent_events if e.success]
                avg_load_time = sum(recent_load_times) / max(1, len(recent_load_times))
                
                success_rate = len([e for e in recent_events if e.success]) / len(recent_events) * 100
                
                cache_hits = len([e for e in recent_events if e.cache_hit])
                cache_hit_rate = cache_hits / len(recent_events) * 100 if recent_events else 0
            else:
                avg_load_time = 0.0
                success_rate = 100.0
                cache_hit_rate = 0.0
            
            # Métricas del sistema
            current_metrics = self._get_current_system_metrics()
            
            # Estadísticas agregadas
            uptime = time.time() - self._start_time
            total_load_time = self._aggregate_stats['total_load_time']
            total_successful = self._aggregate_stats['successful_imports']
            
            avg_load_time_total = total_load_time / max(1, total_successful)
        
        return {
            'system_status': {
                'uptime_seconds': uptime,
                'uptime_formatted': self._format_uptime(uptime),
                'is_monitoring': self._is_active,
                'cpu_percent': current_metrics.cpu_percent,
                'memory_mb': current_metrics.memory_mb,
                'memory_percent': current_metrics.memory_percent
            },
            'import_stats': {
                'total_imports': self._aggregate_stats['total_imports'],
                'successful_imports': self._aggregate_stats['successful_imports'],
                'failed_imports': self._aggregate_stats['failed_imports'],
                'success_rate_percent': success_rate,
                'avg_load_time_recent': avg_load_time,
                'avg_load_time_total': avg_load_time_total,
                'cache_hit_rate_percent': cache_hit_rate,
                'lazy_loads': self._aggregate_stats['lazy_loads']
            },
            'performance_metrics': {
                'peak_memory_mb': self._aggregate_stats['peak_memory_mb'],
                'active_modules': current_metrics.active_modules,
                'cache_size': current_metrics.cache_size,
                'lazy_modules': current_metrics.lazy_modules
            },
            'recent_alerts': self._alert_manager.get_recent_alerts(5)
        }
    
    def get_trend_analysis(self, hours: float = 1.0) -> Dict[str, Any]:
        """
        📈 Análisis de tendencias del sistema
        
        Args:
            hours: Número de horas hacia atrás para analizar
            
        Returns:
            Análisis de tendencias
        """
        cutoff_time = time.time() - (hours * 3600)
        
        with self._lock:
            # Filtrar eventos recientes
            recent_events = [e for e in self._import_events if e.timestamp > cutoff_time]
            recent_metrics = [m for m in self._system_metrics if m.timestamp > cutoff_time]
        
        if not recent_events and not recent_metrics:
            return {'error': 'No hay datos suficientes para el análisis'}
        
        # Análisis de imports
        import_trend = self._analyze_import_trend(recent_events)
        
        # Análisis de sistema
        system_trend = self._analyze_system_trend(recent_metrics)
        
        # Análisis de performance
        performance_trend = self._analyze_performance_trend(recent_events, recent_metrics)
        
        return {
            'analysis_period': {
                'hours': hours,
                'events_analyzed': len(recent_events),
                'metrics_analyzed': len(recent_metrics)
            },
            'import_trends': import_trend,
            'system_trends': system_trend,
            'performance_trends': performance_trend
        }
    
    def generate_report(self, format: str = 'text') -> str:
        """
        📋 Genera un reporte completo del sistema
        
        Args:
            format: Formato del reporte ('text', 'json')
            
        Returns:
            Reporte formateado
        """
        stats = self.get_real_time_stats()
        trends = self.get_trend_analysis(hours=2.0)
        
        if format == 'json':
            return json.dumps({
                'timestamp': time.time(),
                'real_time_stats': stats,
                'trend_analysis': trends
            }, indent=2)
        
        # Formato texto
        report = []
        report.append("=" * 60)
        report.append("🚀 SIC v3.1 ENTERPRISE - MONITOR DASHBOARD REPORT")
        report.append("=" * 60)
        report.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Uptime: {stats['system_status']['uptime_formatted']}")
        report.append("")
        
        # Estadísticas del sistema
        sys_stats = stats['system_status']
        report.append("📊 SISTEMA:")
        report.append(f"  CPU: {sys_stats['cpu_percent']:.1f}%")
        report.append(f"  Memoria: {sys_stats['memory_mb']:.1f}MB ({sys_stats['memory_percent']:.1f}%)")
        report.append(f"  Monitoreo: {'Activo' if sys_stats['is_monitoring'] else 'Inactivo'}")
        report.append("")
        
        # Estadísticas de imports
        import_stats = stats['import_stats']
        report.append("📦 IMPORTS:")
        report.append(f"  Total: {import_stats['total_imports']}")
        report.append(f"  Exitosos: {import_stats['successful_imports']}")
        report.append(f"  Fallidos: {import_stats['failed_imports']}")
        report.append(f"  Tasa de éxito: {import_stats['success_rate_percent']:.1f}%")
        report.append(f"  Tiempo promedio: {import_stats['avg_load_time_total']:.4f}s")
        report.append(f"  Cache hit rate: {import_stats['cache_hit_rate_percent']:.1f}%")
        report.append(f"  Lazy loads: {import_stats['lazy_loads']}")
        report.append("")
        
        # Alertas recientes
        recent_alerts = stats['recent_alerts']
        if recent_alerts:
            report.append("🚨 ALERTAS RECIENTES:")
            for alert in recent_alerts[-5:]:
                report.append(f"  [{alert['formatted_time']}] {alert['message']}")
        else:
            report.append("✅ No hay alertas recientes")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def start_monitoring(self):
        """▶️ Inicia el monitoreo continuo del sistema"""
        if self._is_active:
            return
        
        self._is_active = True
        self._stop_monitoring.clear()
        
        self._monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True,
            name="SIC-Monitor"
        )
        self._monitor_thread.start()
        
        print("▶️ [Monitor] Monitoreo continuo iniciado")
    
    def stop_monitoring(self):
        """⏹️ Detiene el monitoreo continuo"""
        if not self._is_active:
            return
        
        self._stop_monitoring.set()
        self._is_active = False
        
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=2.0)
        
        print("⏹️ [Monitor] Monitoreo continuo detenido")
    
    def shutdown(self):
        """🔚 Apaga el dashboard limpiamente"""
        self.stop_monitoring()
        print("🔚 [Monitor] Dashboard apagado")
    
    def get_status(self) -> str:
        """Estado del monitor dashboard"""
        stats = self.get_real_time_stats()
        import_stats = stats['import_stats']
        sys_stats = stats['system_status']
        
        return (f"Monitor: {import_stats['total_imports']} imports, "
                f"{import_stats['success_rate_percent']:.1f}% éxito, "
                f"{sys_stats['memory_mb']:.1f}MB RAM, "
                f"{'Activo' if self._is_active else 'Inactivo'}")
    
    def _monitoring_loop(self):
        """Loop principal de monitoreo continuo"""
        while not self._stop_monitoring.is_set():
            try:
                # Recopilar métricas del sistema
                metrics = self._get_current_system_metrics()
                
                with self._lock:
                    self._system_metrics.append(metrics)
                    
                    # Actualizar pico de memoria
                    if metrics.memory_mb > self._aggregate_stats['peak_memory_mb']:
                        self._aggregate_stats['peak_memory_mb'] = metrics.memory_mb
                
                # Esperar intervalo de muestreo
                self._stop_monitoring.wait(self._metrics_interval)
                
            except Exception as e:
                print(f"❌ [Monitor] Error en loop de monitoreo: {e}")
                self._stop_monitoring.wait(self._metrics_interval)
    
    def _get_current_system_metrics(self) -> SystemMetrics:
        """Obtiene métricas actuales del sistema"""
        timestamp = time.time()
        
        # Métricas de CPU y memoria
        if self._process:
            try:
                cpu_percent = self._process.cpu_percent()
                memory_info = self._process.memory_info()
                memory_mb = memory_info.rss / 1024 / 1024
                memory_percent = self._process.memory_percent()
            except:
                cpu_percent = 0.0
                memory_mb = 0.0
                memory_percent = 0.0
        else:
            cpu_percent = 0.0
            memory_mb = 0.0
            memory_percent = 0.0
        
        # Contar módulos activos
        active_modules = len(sys.modules)
        
        # Placeholders para cache y lazy modules (serán actualizados por otros componentes)
        cache_size = 0
        lazy_modules = 0
        
        return SystemMetrics(
            timestamp=timestamp,
            cpu_percent=cpu_percent,
            memory_mb=memory_mb,
            memory_percent=memory_percent,
            active_modules=active_modules,
            cache_size=cache_size,
            lazy_modules=lazy_modules
        )
    
    def _get_memory_usage_mb(self) -> float:
        """Obtiene el uso actual de memoria en MB"""
        if self._process:
            try:
                return self._process.memory_info().rss / 1024 / 1024
            except:
                return 0.0
        return 0.0
    
    def _analyze_import_trend(self, events: List[ImportEvent]) -> Dict[str, Any]:
        """Analiza tendencias de imports"""
        if not events:
            return {}
        
        # Agrupar por tipo de import
        by_type = defaultdict(list)
        for event in events:
            by_type[event.import_type].append(event)
        
        # Calcular estadísticas por tipo
        type_stats = {}
        for import_type, type_events in by_type.items():
            success_rate = len([e for e in type_events if e.success]) / len(type_events) * 100
            avg_load_time = sum(e.load_time for e in type_events if e.success) / max(1, len([e for e in type_events if e.success]))
            
            type_stats[import_type] = {
                'count': len(type_events),
                'success_rate': success_rate,
                'avg_load_time': avg_load_time
            }
        
        return {
            'total_events': len(events),
            'by_type': type_stats,
            'avg_load_time_overall': sum(e.load_time for e in events if e.success) / max(1, len([e for e in events if e.success]))
        }
    
    def _analyze_system_trend(self, metrics: List[SystemMetrics]) -> Dict[str, Any]:
        """Analiza tendencias del sistema"""
        if not metrics:
            return {}
        
        # Calcular promedios y tendencias
        cpu_values = [m.cpu_percent for m in metrics]
        memory_values = [m.memory_mb for m in metrics]
        
        return {
            'cpu_trend': {
                'avg': sum(cpu_values) / len(cpu_values),
                'min': min(cpu_values),
                'max': max(cpu_values),
                'current': cpu_values[-1] if cpu_values else 0
            },
            'memory_trend': {
                'avg': sum(memory_values) / len(memory_values),
                'min': min(memory_values),
                'max': max(memory_values),
                'current': memory_values[-1] if memory_values else 0
            }
        }
    
    def _analyze_performance_trend(self, events: List[ImportEvent], 
                                  metrics: List[SystemMetrics]) -> Dict[str, Any]:
        """Analiza tendencias de performance"""
        performance_data = {}
        
        if events:
            # Tendencia de tiempos de carga
            load_times = [e.load_time for e in events if e.success]
            if load_times:
                performance_data['load_time_trend'] = {
                    'improving': len([t for t in load_times[-10:] if t < sum(load_times) / len(load_times)]) > 5,
                    'avg_recent': sum(load_times[-10:]) / min(10, len(load_times)),
                    'avg_overall': sum(load_times) / len(load_times)
                }
        
        if metrics:
            # Tendencia de uso de recursos
            recent_memory = [m.memory_mb for m in metrics[-10:]]
            overall_memory = [m.memory_mb for m in metrics]
            
            performance_data['resource_trend'] = {
                'memory_stable': max(recent_memory) - min(recent_memory) < 50,  # Variación < 50MB
                'memory_recent_avg': sum(recent_memory) / len(recent_memory),
                'memory_overall_avg': sum(overall_memory) / len(overall_memory)
            }
        
        return performance_data
    
    def _format_uptime(self, seconds: float) -> str:
        """Formatea el tiempo de actividad"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"


if __name__ == "__main__":
    # Test del MonitorDashboard
    print("📊 Testing Monitor Dashboard...")
    
    dashboard = MonitorDashboard()
    
    try:
        # Simular algunos eventos de import
        dashboard.record_import('sys', 0.001, success=True, import_type='normal')
        dashboard.record_import('os', 0.002, success=True, import_type='cached', cache_hit=True)
        dashboard.record_import('pandas', 0.150, success=True, import_type='lazy')
        
        # Obtener estadísticas
        stats = dashboard.get_real_time_stats()
        print(f"✅ Stats obtenidas: {stats['import_stats']['total_imports']} imports")
        
        # Generar reporte
        report = dashboard.generate_report()
        print("✅ Reporte generado")
        print(report[:300] + "...")  # Mostrar primeras líneas
        
        # Test de análisis de tendencias
        trends = dashboard.get_trend_analysis(hours=0.1)  # Última 0.1 horas
        print(f"✅ Análisis de tendencias: {len(trends)} secciones")
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        dashboard.shutdown()
    
    print("🎯 Monitor Dashboard test completado")
