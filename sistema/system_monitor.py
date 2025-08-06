#!/usr/bin/env python3
"""
📊 MONITOR DE ESTADO ICT ENGINE v3.44
====================================

Sistema de monitoreo en tiempo real del estado y rendimiento del ICT Engine.
Supervisa componentes críticos, métricas de rendimiento y salud del sistema.

Características:
- Monitoreo de componentes en tiempo real
- Alertas automáticas por degradación
- Métricas de rendimiento históricas
- Dashboard de estado consolidado
- Reportes automáticos de salud

Autor: ICT Engine Team
Fecha: Agosto 2025
"""

from sistema.sic_clean import time
import psutil
import threading
from sistema.sic_clean import datetime, timedelta
from sistema.sic_clean import Dict, List, Any, Optional
from sistema.sic_clean import dataclass
from enum import Enum
from sistema.sic_clean import json
from sistema.sic_clean import Path

# Imports del sistema ICT
from sistema.sic_clean import enviar_senal_log


class ComponentStatus(Enum):
    """Estados de componentes del sistema"""
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    OFFLINE = "OFFLINE"
    UNKNOWN = "UNKNOWN"


class AlertLevel(Enum):
    """Niveles de alertas del sistema"""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    EMERGENCY = "EMERGENCY"


@dataclass
class ComponentHealth:
    """Estado de salud de un componente"""
    name: str
    status: ComponentStatus
    last_check: datetime
    response_time: float
    error_count: int
    uptime: float
    metrics: Dict[str, Any]
    alerts: List[str]


@dataclass
class SystemAlert:
    """Alerta del sistema"""
    timestamp: datetime
    level: AlertLevel
    component: str
    message: str
    data: Dict[str, Any]
    resolved: bool = False


class ICTSystemMonitor:
    """
    Monitor de estado del sistema ICT Engine

    Supervisa:
    - Componentes core (pattern analyzer, POI detector, etc.)
    - Recursos del sistema (CPU, memoria, disco)
    - Conectividad y latencia
    - Métricas de trading
    - Logs y errores
    """

    def __init__(self, monitoring_interval: int = 30):
        """
        Inicializa el monitor del sistema

        Args:
            monitoring_interval: Intervalo de monitoreo en segundos
        """
        self.monitoring_interval = monitoring_interval
        self.is_monitoring = False
        self.monitor_thread = None

        # 📊 Estado de componentes
        self.components: Dict[str, ComponentHealth] = {}
        self.system_metrics: Dict[str, Any] = {}
        self.alerts: List[SystemAlert] = []

        # 🎯 Umbrales de alerta
        self.thresholds = {
            'cpu_usage': 80.0,          # %
            'memory_usage': 85.0,       # %
            'disk_usage': 90.0,         # %
            'response_time': 1000.0,    # ms
            'error_rate': 5.0           # errores/minuto
        }

        # 📁 Directorios de logs
        self.logs_dir = Path(__file__).parent.parent / "data" / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # 🔒 Thread safety
        self._lock = threading.Lock()

        # 🚀 Inicializar componentes
        self._initialize_components()

        enviar_senal_log("INFO", "📊 Sistema Monitor ICT inicializado", __name__, "monitor")

    def _initialize_components(self):
        """Inicializa la lista de componentes a monitorear"""
        component_names = [
            "pattern_analyzer",
            "poi_detector",
            "confidence_engine",
            "risk_manager",
            "dashboard",
            "logging_system",
            "data_manager"
        ]

        for name in component_names:
            self.components[name] = ComponentHealth(
                name=name,
                status=ComponentStatus.UNKNOWN,
                last_check=datetime.now(),
                response_time=0.0,
                error_count=0,
                uptime=0.0,
                metrics={},
                alerts=[]
            )

    def start_monitoring(self):
        """Inicia el monitoreo del sistema"""
        if self.is_monitoring:
            enviar_senal_log("WARNING", "Monitor ya está ejecutándose", __name__, "monitor")
            return

        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()

        enviar_senal_log("INFO", "🔄 Monitoreo del sistema iniciado", __name__, "monitor")

    def stop_monitoring(self):
        """Detiene el monitoreo del sistema"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)

        enviar_senal_log("INFO", "⏹️ Monitoreo del sistema detenido", __name__, "monitor")

    def _monitoring_loop(self):
        """Bucle principal de monitoreo"""
        while self.is_monitoring:
            try:
                # 📊 Recopilar métricas del sistema
                self._collect_system_metrics()

                # 🔍 Verificar salud de componentes
                self._check_component_health()

                # ⚠️ Procesar alertas
                self._process_alerts()

                # 💾 Guardar estado
                self._save_monitoring_data()

                # ⏱️ Esperar hasta siguiente verificación
                time.sleep(self.monitoring_interval)

            except Exception as e:
                enviar_senal_log("ERROR", f"Error en bucle de monitoreo: {e}", __name__, "monitor")
                time.sleep(self.monitoring_interval)

    def _collect_system_metrics(self):
        """Recopila métricas del sistema operativo"""
        try:
            # 🖥️ Métricas de CPU
            cpu_percent = psutil.cpu_percent(interval=1)

            # 🧠 Métricas de memoria
            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            # 💾 Métricas de disco (Windows compatible)
            try:
                disk = psutil.disk_usage('C:\\')  # Windows path
            except (OSError, PermissionError):
                disk = psutil.disk_usage('/')  # Fallback para otros OS
            disk_percent = (disk.used / disk.total) * 100

            # 🌐 Métricas de red (si están disponibles)
            network = psutil.net_io_counters()

            # ⏱️ Tiempo de actividad del sistema
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time

            self.system_metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'usage_percent': cpu_percent,
                    'count': psutil.cpu_count(),
                    'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
                },
                'memory': {
                    'usage_percent': memory_percent,
                    'total_gb': round(memory.total / (1024**3), 2),
                    'available_gb': round(memory.available / (1024**3), 2),
                    'used_gb': round(memory.used / (1024**3), 2)
                },
                'disk': {
                    'usage_percent': disk_percent,
                    'total_gb': round(disk.total / (1024**3), 2),
                    'free_gb': round(disk.free / (1024**3), 2),
                    'used_gb': round(disk.used / (1024**3), 2)
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv,
                    'packets_sent': network.packets_sent,
                    'packets_recv': network.packets_recv
                } if network else {},
                'uptime_hours': uptime.total_seconds() / 3600
            }

            # ⚠️ Verificar umbrales
            self._check_system_thresholds()

        except Exception as e:
            enviar_senal_log("ERROR", f"Error recopilando métricas del sistema: {e}", __name__, "monitor")

    def _check_component_health(self):
        """Verifica la salud de cada componente ICT"""
        with self._lock:
            for component_name, health in self.components.items():
                try:
                    # 🔍 Verificar componente específico
                    start_time = time.time()
                    status = self._ping_component(component_name)
                    response_time = (time.time() - start_time) * 1000  # ms

                    # 📊 Actualizar métricas
                    health.status = status
                    health.last_check = datetime.now()
                    health.response_time = response_time
                    health.uptime += self.monitoring_interval / 3600  # horas

                    # ⚠️ Verificar umbrales de respuesta
                    if response_time > self.thresholds['response_time']:
                        alert_msg = f"Tiempo de respuesta alto: {response_time:.1f}ms"
                        health.alerts.append(alert_msg)
                        self._create_alert(AlertLevel.WARNING, component_name, alert_msg)

                    # 🏥 Determinar estado general
                    if status == ComponentStatus.CRITICAL:
                        self._create_alert(AlertLevel.CRITICAL, component_name,
                                        f"Componente en estado crítico")

                except Exception as e:
                    health.status = ComponentStatus.OFFLINE
                    health.error_count += 1
                    enviar_senal_log("ERROR", f"Error verificando {component_name}: {e}",
                                   __name__, "monitor")

    def _ping_component(self, component_name: str) -> ComponentStatus:
        """
        Verifica el estado de un componente específico

        Args:
            component_name: Nombre del componente a verificar

        Returns:
            ComponentStatus: Estado actual del componente
        """
        # 🔍 Lógica simplificada para demo - en producción sería más específica
        try:
            if component_name == "pattern_analyzer":
                # Verificar si el pattern analyzer responde
                return ComponentStatus.HEALTHY
            elif component_name == "poi_detector":
                # Verificar detector de POIs
                return ComponentStatus.HEALTHY
            elif component_name == "dashboard":
                # Verificar dashboard
                return ComponentStatus.HEALTHY
            else:
                # Estado por defecto para otros componentes
                return ComponentStatus.HEALTHY

        except Exception:
            return ComponentStatus.CRITICAL

    def _check_system_thresholds(self):
        """Verifica umbrales del sistema y genera alertas"""
        metrics = self.system_metrics

        # 🖥️ CPU
        if metrics['cpu']['usage_percent'] > self.thresholds['cpu_usage']:
            self._create_alert(
                AlertLevel.WARNING,
                "system_cpu",
                f"Uso de CPU alto: {metrics['cpu']['usage_percent']:.1f}%",
                {"cpu_usage": metrics['cpu']['usage_percent']}
            )

        # 🧠 Memoria
        if metrics['memory']['usage_percent'] > self.thresholds['memory_usage']:
            self._create_alert(
                AlertLevel.WARNING,
                "system_memory",
                f"Uso de memoria alto: {metrics['memory']['usage_percent']:.1f}%",
                {"memory_usage": metrics['memory']['usage_percent']}
            )

        # 💾 Disco
        if metrics['disk']['usage_percent'] > self.thresholds['disk_usage']:
            self._create_alert(
                AlertLevel.CRITICAL,
                "system_disk",
                f"Uso de disco crítico: {metrics['disk']['usage_percent']:.1f}%",
                {"disk_usage": metrics['disk']['usage_percent']}
            )

    def _create_alert(self, level: AlertLevel, component: str, message: str,
                     data: Optional[Dict[str, Any]] = None):
        """Crea una nueva alerta del sistema"""
        alert = SystemAlert(
            timestamp=datetime.now(),
            level=level,
            component=component,
            message=message,
            data=data or {},
            resolved=False
        )

        self.alerts.append(alert)

        # 📝 Log de la alerta
        enviar_senal_log(
            level.value,
            f"[{component.upper()}] {message}",
            __name__,
            "alertas"
        )

    def _process_alerts(self):
        """Procesa alertas pendientes"""
        # 🧹 Limpiar alertas antiguas (más de 24 horas)
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.alerts = [alert for alert in self.alerts if alert.timestamp > cutoff_time]

        # 📊 Contar alertas activas por nivel
        alert_counts = {level.value: 0 for level in AlertLevel}
        for alert in self.alerts:
            if not alert.resolved:
                alert_counts[alert.level.value] += 1

        # 🚨 Alertas críticas
        critical_alerts = [a for a in self.alerts
                          if a.level == AlertLevel.CRITICAL and not a.resolved]

        if len(critical_alerts) >= 3:
            enviar_senal_log("CRITICAL",
                           f"Múltiples alertas críticas activas: {len(critical_alerts)}",
                           __name__, "alertas")

    def _save_monitoring_data(self):
        """Guarda datos de monitoreo en archivo"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        monitoring_file = self.logs_dir / f"system_monitoring_{timestamp}.json"

        monitoring_data = {
            'timestamp': datetime.now().isoformat(),
            'system_metrics': self.system_metrics,
            'component_health': {
                name: {
                    'status': health.status.value,
                    'response_time': health.response_time,
                    'error_count': health.error_count,
                    'uptime': health.uptime,
                    'alerts_count': len(health.alerts)
                }
                for name, health in self.components.items()
            },
            'active_alerts': len([a for a in self.alerts if not a.resolved]),
            'system_status': self.get_overall_status().value
        }

        try:
            with open(monitoring_file, 'a', encoding='utf-8') as f:
                json.dump(monitoring_data, f, ensure_ascii=False, default=str)
                f.write('\n')
        except Exception as e:
            enviar_senal_log("ERROR", f"Error guardando datos de monitoreo: {e}",
                           __name__, "monitor")

    # 📊 MÉTODOS PÚBLICOS DE CONSULTA

    def get_overall_status(self) -> ComponentStatus:
        """Obtiene el estado general del sistema"""
        if not self.components:
            return ComponentStatus.UNKNOWN

        statuses = [health.status for health in self.components.values()]

        if ComponentStatus.CRITICAL in statuses:
            return ComponentStatus.CRITICAL
        elif ComponentStatus.WARNING in statuses:
            return ComponentStatus.WARNING
        elif ComponentStatus.OFFLINE in statuses:
            return ComponentStatus.WARNING
        else:
            return ComponentStatus.HEALTHY

    def get_system_summary(self) -> Dict[str, Any]:
        """Obtiene resumen del estado del sistema"""
        active_alerts = [a for a in self.alerts if not a.resolved]

        return {
            'overall_status': self.get_overall_status().value,
            'monitoring_since': datetime.now().isoformat(),
            'system_metrics': self.system_metrics,
            'components': {
                name: health.status.value
                for name, health in self.components.items()
            },
            'alerts': {
                'total': len(self.alerts),
                'active': len(active_alerts),
                'critical': len([a for a in active_alerts if a.level == AlertLevel.CRITICAL]),
                'warning': len([a for a in active_alerts if a.level == AlertLevel.WARNING])
            },
            'thresholds': self.thresholds
        }

    def get_component_details(self, component_name: str) -> Optional[Dict[str, Any]]:
        """Obtiene detalles de un componente específico"""
        if component_name not in self.components:
            return None

        health = self.components[component_name]
        return {
            'name': health.name,
            'status': health.status.value,
            'last_check': health.last_check.isoformat(),
            'response_time_ms': health.response_time,
            'error_count': health.error_count,
            'uptime_hours': health.uptime,
            'metrics': health.metrics,
            'recent_alerts': health.alerts[-10:] if health.alerts else []
        }

    def get_recent_alerts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Obtiene alertas recientes"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_alerts = [a for a in self.alerts if a.timestamp > cutoff_time]

        return [
            {
                'timestamp': alert.timestamp.isoformat(),
                'level': alert.level.value,
                'component': alert.component,
                'message': alert.message,
                'resolved': alert.resolved,
                'data': alert.data
            }
            for alert in recent_alerts
        ]

    def resolve_alert(self, alert_index: int):
        """Marca una alerta como resuelta"""
        if 0 <= alert_index < len(self.alerts):
            self.alerts[alert_index].resolved = True
            enviar_senal_log("INFO", f"Alerta {alert_index} marcada como resuelta",
                           __name__, "monitor")

    def set_threshold(self, metric: str, value: float):
        """Actualiza umbral de alerta"""
        if metric in self.thresholds:
            old_value = self.thresholds[metric]
            self.thresholds[metric] = value
            enviar_senal_log("INFO",
                           f"Umbral {metric} actualizado: {old_value} → {value}",
                           __name__, "monitor")

    def generate_health_report(self) -> str:
        """Genera reporte de salud del sistema"""
        summary = self.get_system_summary()

        report = f"""
📊 REPORTE DE SALUD ICT ENGINE v3.44
==================================

🎯 Estado General: {summary['overall_status']}
📅 Última Actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💻 MÉTRICAS DEL SISTEMA:
• CPU: {summary['system_metrics']['cpu']['usage_percent']:.1f}%
• Memoria: {summary['system_metrics']['memory']['usage_percent']:.1f}%
• Disco: {summary['system_metrics']['disk']['usage_percent']:.1f}%
• Uptime: {summary['system_metrics']['uptime_hours']:.1f} horas

🔧 ESTADO DE COMPONENTES:
"""

        for name, status in summary['components'].items():
            status_icon = {
                'HEALTHY': '✅',
                'WARNING': '⚠️',
                'CRITICAL': '🔴',
                'OFFLINE': '❌',
                'UNKNOWN': '❓'
            }.get(status, '❓')

            report += f"• {name}: {status_icon} {status}\n"

        report += f"""
🚨 ALERTAS:
• Total: {summary['alerts']['total']}
• Activas: {summary['alerts']['active']}
• Críticas: {summary['alerts']['critical']}
• Advertencias: {summary['alerts']['warning']}

📊 UMBRALES CONFIGURADOS:
• CPU: {self.thresholds['cpu_usage']}%
• Memoria: {self.thresholds['memory_usage']}%
• Disco: {self.thresholds['disk_usage']}%
• Tiempo Respuesta: {self.thresholds['response_time']}ms
        """.strip()

        return report


# 🌍 INSTANCIA GLOBAL DEL MONITOR
system_monitor = ICTSystemMonitor()


# 🔧 FUNCIONES DE CONVENIENCIA
def start_system_monitoring():
    """Inicia el monitoreo del sistema"""
    system_monitor.start_monitoring()

def get_system_status():
    """Obtiene el estado actual del sistema"""
    return system_monitor.get_system_summary()

def get_health_report():
    """Obtiene reporte de salud del sistema"""
    return system_monitor.generate_health_report()
