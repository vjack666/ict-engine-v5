#!/usr/bin/env python3
"""
📋 SISTEMA DE BITÁCORAS ICT ENGINE v3.44
=======================================

Sistema centralizado de registro y monitoreo del estado del sistema ICT Engine.
Registra eventos críticos, decisiones de trading, métricas de rendimiento y
estado de componentes en tiempo real.

Autor: ICT Engine Team
Fecha: Agosto 2025
Versión: v5.0
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import hashlib

# Imports del sistema ICT - MIGRADO A SLUC v2.1
from sistema.logging_interface import enviar_senal_log


class BitacoraType(Enum):
    """Tipos de bitácoras del sistema"""
    SYSTEM_STATUS = "system_status"          # Estado general del sistema
    TRADING_DECISIONS = "trading_decisions"   # Decisiones de trading
    PATTERN_DETECTION = "pattern_detection"   # Detección de patrones
    PERFORMANCE_METRICS = "performance"       # Métricas de rendimiento
    ERROR_TRACKING = "error_tracking"         # Seguimiento de errores
    SESSION_ANALYSIS = "session_analysis"     # Análisis por sesión
    POI_LIFECYCLE = "poi_lifecycle"           # Ciclo de vida de POIs
    RISK_MANAGEMENT = "risk_management"       # Eventos de gestión de riesgo


class SeverityLevel(Enum):
    """Niveles de severidad para eventos"""
    CRITICAL = "CRITICAL"    # Errores críticos del sistema
    HIGH = "HIGH"           # Eventos importantes
    MEDIUM = "MEDIUM"       # Eventos normales
    LOW = "LOW"             # Información de rutina
    DEBUG = "DEBUG"         # Información de debugging


@dataclass
class BitacoraEntry:
    """Entrada individual de bitácora"""
    timestamp: str
    bitacora_type: str
    severity: str
    component: str
    event_id: str
    description: str
    data: Dict[str, Any]
    context: Dict[str, Any]
    session_id: str


class ICTBitacoraManager:
    """
    Gestor centralizado de bitácoras para ICT Engine

    Características:
    - Múltiples tipos de bitácoras especializadas
    - Rotación automática de archivos
    - Thread-safe operations
    - Formato JSON estructurado
    - Indexación por eventos críticos
    """

    def __init__(self, base_path: Optional[str] = None):
        """Inicializa el sistema de bitácoras"""
        self.base_path = (Path(base_path) if base_path
                         else Path(__file__).parent.parent / "docs" / "bitacoras")
        self.base_path.mkdir(parents=True, exist_ok=True)

        # 🔒 Thread safety
        self._lock = threading.Lock()

        # 📊 Contadores de eventos
        self.event_counters = {bt.value: 0 for bt in BitacoraType}

        # 🎯 Sesión actual
        self.current_session_id = self._generate_session_id()

        # 📁 Crear directorios para cada tipo de bitácora
        for bitacora_type in BitacoraType:
            (self.base_path / bitacora_type.value).mkdir(exist_ok=True)

        # 🚀 Registrar inicio del sistema
        self.log_system_event(
            SeverityLevel.HIGH,
            "SYSTEM_STARTUP",
            "ICT Bitácora Manager inicializado",
            {"session_id": self.current_session_id, "version": "v3.44"}
        )

        # Sistema SLUC v2.1 para logging
        enviar_senal_log("INFO", "📋 Sistema de Bitácoras ICT inicializado", "bitacora_manager", "initialization")

    def _generate_session_id(self) -> str:
        """Genera ID único para la sesión actual"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_hash = hashlib.md5(str(datetime.now().microsecond).encode()).hexdigest()[:8]
        return f"ICT_{timestamp}_{random_hash}"

    def _get_log_file_path(self, bitacora_type: BitacoraType) -> Path:
        """Obtiene la ruta del archivo de log para el tipo especificado"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{bitacora_type.value}_{date_str}.jsonl"
        return self.base_path / bitacora_type.value / filename

    def _write_entry(self, entry: BitacoraEntry):
        """Escribe una entrada a la bitácora correspondiente"""
        with self._lock:
            try:
                bitacora_type = BitacoraType(entry.bitacora_type)
                log_file = self._get_log_file_path(bitacora_type)

                # Escribir en formato JSONL (JSON Lines)
                with open(log_file, 'a', encoding='utf-8') as f:
                    json.dump(asdict(entry), f, ensure_ascii=False, default=str)
                    f.write('\n')

                # Incrementar contador
                self.event_counters[entry.bitacora_type] += 1

            except (ValueError, OSError) as e:
                enviar_senal_log("ERROR", f"❌ Error escribiendo bitácora: {e}", "bitacora_manager", "write_error")

    # 🔧 MÉTODOS PÚBLICOS DE LOGGING ESPECIALIZADO

    def log_system_event(self, severity: SeverityLevel, event_id: str,
                        description: str, data: Optional[Dict[str, Any]] = None,
                        context: Optional[Dict[str, Any]] = None):
        """Registra eventos del sistema general"""
        entry = BitacoraEntry(
            timestamp=datetime.now().isoformat(),
            bitacora_type=BitacoraType.SYSTEM_STATUS.value,
            severity=severity.value,
            component="SYSTEM",
            event_id=event_id,
            description=description,
            data=data or {},
            context=context or {},
            session_id=self.current_session_id
        )
        self._write_entry(entry)

    def log_trading_decision(self, pattern: str, direction: str, strength: float,
                           entry_price: float, targets: List[float],
                           stop_loss: float, risk_reward: float,
                           reasoning: str, context: Optional[Dict[str, Any]] = None):
        """Registra decisiones de trading"""
        entry = BitacoraEntry(
            timestamp=datetime.now().isoformat(),
            bitacora_type=BitacoraType.TRADING_DECISIONS.value,
            severity=SeverityLevel.HIGH.value,
            component="TRADING_ENGINE",
            event_id=f"TRADE_DECISION_{pattern}",
            description=f"Decisión de trading: {direction} {pattern}",
            data={
                "pattern": pattern,
                "direction": direction,
                "strength": strength,
                "entry_price": entry_price,
                "targets": targets,
                "stop_loss": stop_loss,
                "risk_reward": risk_reward,
                "reasoning": reasoning
            },
            context=context or {},
            session_id=self.current_session_id
        )
        self._write_entry(entry)

    def log_pattern_detection(self, pattern_type: str, confidence: float,
                            location_data: Dict[str, Any],
                            confluences: List[str],
                            context: Optional[Dict[str, Any]] = None):
        """Registra detección de patrones ICT"""
        entry = BitacoraEntry(
            timestamp=datetime.now().isoformat(),
            bitacora_type=BitacoraType.PATTERN_DETECTION.value,
            severity=SeverityLevel.MEDIUM.value,
            component="PATTERN_ANALYZER",
            event_id=f"PATTERN_{pattern_type}",
            description=f"Patrón {pattern_type} detectado con {confidence}% confianza",
            data={
                "pattern_type": pattern_type,
                "confidence": confidence,
                "location": location_data,
                "confluences": confluences,
                "detection_time": datetime.now().isoformat()
            },
            context=context or {},
            session_id=self.current_session_id
        )
        self._write_entry(entry)

    def log_performance_metrics(self, metrics: Dict[str, Any]):
        """Registra métricas de rendimiento del sistema"""
        entry = BitacoraEntry(
            timestamp=datetime.now().isoformat(),
            bitacora_type=BitacoraType.PERFORMANCE_METRICS.value,
            severity=SeverityLevel.LOW.value,
            component="PERFORMANCE_MONITOR",
            event_id="METRICS_UPDATE",
            description="Actualización de métricas de rendimiento",
            data=metrics,
            context={"measurement_window": "real_time"},
            session_id=self.current_session_id
        )
        self._write_entry(entry)

    def log_error_event(self, component: str, error_type: str,
                       error_message: str, stack_trace: Optional[str] = None,
                       recovery_action: Optional[str] = None):
        """Registra errores del sistema"""
        entry = BitacoraEntry(
            timestamp=datetime.now().isoformat(),
            bitacora_type=BitacoraType.ERROR_TRACKING.value,
            severity=SeverityLevel.CRITICAL.value,
            component=component,
            event_id=f"ERROR_{error_type}",
            description=f"Error en {component}: {error_message}",
            data={
                "error_type": error_type,
                "error_message": error_message,
                "stack_trace": stack_trace,
                "recovery_action": recovery_action
            },
            context={"requires_attention": True},
            session_id=self.current_session_id
        )
        self._write_entry(entry)

    def log_session_analysis(self, session_type: str, summary: Dict[str, Any]):
        """Registra análisis de sesión de trading"""
        entry = BitacoraEntry(
            timestamp=datetime.now().isoformat(),
            bitacora_type=BitacoraType.SESSION_ANALYSIS.value,
            severity=SeverityLevel.MEDIUM.value,
            component="SESSION_ANALYZER",
            event_id=f"SESSION_{session_type}",
            description=f"Análisis de sesión {session_type} completado",
            data=summary,
            context={"session_type": session_type},
            session_id=self.current_session_id
        )
        self._write_entry(entry)

    def log_poi_lifecycle(self, poi_id: str, action: str,
                         poi_data: Dict[str, Any]):
        """Registra eventos del ciclo de vida de POIs"""
        entry = BitacoraEntry(
            timestamp=datetime.now().isoformat(),
            bitacora_type=BitacoraType.POI_LIFECYCLE.value,
            severity=SeverityLevel.LOW.value,
            component="POI_SYSTEM",
            event_id=f"POI_{action}_{poi_id}",
            description=f"POI {poi_id}: {action}",
            data=poi_data,
            context={"poi_id": poi_id, "action": action},
            session_id=self.current_session_id
        )
        self._write_entry(entry)

    def log_risk_management(self, action: str, details: Dict[str, Any],
                           reason: str):
        """Registra eventos de gestión de riesgo"""
        entry = BitacoraEntry(
            timestamp=datetime.now().isoformat(),
            bitacora_type=BitacoraType.RISK_MANAGEMENT.value,
            severity=SeverityLevel.HIGH.value,
            component="RISK_MANAGER",
            event_id=f"RISK_{action}",
            description=f"Acción de riesgo: {action} - {reason}",
            data=details,
            context={"action": action, "reason": reason},
            session_id=self.current_session_id
        )
        self._write_entry(entry)

    # 📊 MÉTODOS DE CONSULTA Y ANÁLISIS

    def get_session_summary(self) -> Dict[str, Any]:
        """Obtiene resumen de la sesión actual"""
        return {
            "session_id": self.current_session_id,
            "start_time": datetime.now().isoformat(),
            "event_counters": self.event_counters.copy(),
            "total_events": sum(self.event_counters.values()),
            "bitacora_types": len(BitacoraType),
            "status": "ACTIVE"
        }

    def cleanup_old_logs(self, retention_days: int = 30):
        """Limpia logs antiguos según política de retención"""
        cutoff_date = datetime.now() - timedelta(days=retention_days)

        for bitacora_type in BitacoraType:
            type_dir = self.base_path / bitacora_type.value

            for log_file in type_dir.glob("*.jsonl"):
                try:
                    # Extraer fecha del nombre del archivo
                    date_part = log_file.stem.split('_')[-1]
                    file_date = datetime.strptime(date_part, "%Y-%m-%d")

                    if file_date < cutoff_date:
                        log_file.unlink()
                        enviar_senal_log("INFO", f"🗑️ Archivo de bitácora antiguo eliminado: {log_file.name}", "bitacora_manager", "cleanup")

                except (ValueError, IndexError):
                    # Si no se puede parsear la fecha, mantener el archivo
                    continue

    def generate_daily_report(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """Genera reporte diario de bitácoras"""
        if date is None:
            date = datetime.now()

        date_str = date.strftime("%Y-%m-%d")
        report = {
            "date": date_str,
            "summary": {},
            "critical_events": [],
            "performance_stats": {},
            "error_summary": {}
        }

        # Analizar cada tipo de bitácora
        for bitacora_type in BitacoraType:
            log_file = (self.base_path / bitacora_type.value /
                       f"{bitacora_type.value}_{date_str}.jsonl")

            if log_file.exists():
                count = 0
                critical_events = []

                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            count += 1

                            if entry.get('severity') == 'CRITICAL':
                                critical_events.append(entry)

                        except json.JSONDecodeError:
                            continue

                report["summary"][bitacora_type.value] = count
                if critical_events:
                    report["critical_events"].extend(critical_events)

        return report


# 🌍 INSTANCIA GLOBAL DEL GESTOR DE BITÁCORAS
bitacora_manager = ICTBitacoraManager()


# 🔧 FUNCIONES DE CONVENIENCIA PARA USO DIRECTO
def log_system_startup():
    """Registra inicio del sistema ICT"""
    bitacora_manager.log_system_event(
        SeverityLevel.HIGH,
        "SYSTEM_STARTUP",
        "ICT Engine iniciado correctamente",
        {"version": "v3.44", "components": ["core", "dashboard", "sistema"]}
    )

def log_trading_signal(pattern: str, direction: str, strength: float, **kwargs):
    """Registra señal de trading detectada"""
    bitacora_manager.log_trading_decision(
        pattern=pattern,
        direction=direction,
        strength=strength,
        entry_price=kwargs.get('entry_price', 0.0),
        targets=kwargs.get('targets', []),
        stop_loss=kwargs.get('stop_loss', 0.0),
        risk_reward=kwargs.get('risk_reward', 0.0),
        reasoning=kwargs.get('reasoning', 'Señal automática detectada')
    )

def log_poi_detected(poi_type: str, price: float, strength: str, **kwargs):
    """Registra POI detectado"""
    bitacora_manager.log_poi_lifecycle(
        poi_id=f"{poi_type}_{price}_{datetime.now().strftime('%H%M%S')}",
        action="DETECTED",
        poi_data={
            "type": poi_type,
            "price": price,
            "strength": strength,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
    )

def log_critical_error(component: str, error: Exception):
    """Registra error crítico del sistema"""
    bitacora_manager.log_error_event(
        component=component,
        error_type=type(error).__name__,
        error_message=str(error),
        stack_trace="",  # Se puede agregar traceback si es necesario
        recovery_action="Reiniciar componente afectado"
    )
