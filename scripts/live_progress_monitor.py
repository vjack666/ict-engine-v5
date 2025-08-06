"""
📊 MONITOR DE PROGRESO EN TIEMPO REAL - ITC ENGINE v5.0
======================================================

Sistema de monitoreo en vivo para mostrar progreso durante la ejecución
del plan de corrección de errores VS Code.

Autor: Sistema de Análisis Automático
Fecha: 06 Agosto 2025
"""

import os
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# Agregar el directorio padre al path para imports
current_dir = Path(__file__).parent
project_root = current_dir.parent
import sys
sys.path.insert(0, str(project_root))

# MIGRACIÓN SIC v3.0 + SLUC v2.1
try:
    from sistema.sic import enviar_senal_log, log_info, log_warning
except ImportError:
    # Fallback si SIC no está disponible
    def enviar_senal_log(level, message, module, category):
        print(f"[{level}] {module}: {message}")
    log_info = log_warning = enviar_senal_log

@dataclass
class ProgressSnapshot:
    timestamp: str
    vs_code_errors: int
    phase: str
    files_processed: int
    files_total: int
    elapsed_time: str
    eta_remaining: str
    current_file: str
    alerts: List[str]

class LiveProgressMonitor:
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.start_time = datetime.now()
        self.baseline_errors = 0
        self.target_errors = 0
        self.current_phase = "INITIALIZATION"
        self.processed_files = []
        self.monitoring = False

        # Configuración de alertas
        self.alert_thresholds = {
            'phase_timeout_multiplier': 1.5,  # Alertar si fase tarda 150% del tiempo estimado
            'error_increase_threshold': 10,   # Alertar si errores aumentan >10
            'memory_usage_threshold': 80      # Alertar si uso de memoria >80%
        }

        # Estimaciones de tiempo por fase (en minutos)
        self.phase_estimates = {
            "FASE_1_REIMPORTS": 15,
            "FASE_2_SIC_EXPANSION": 45,
            "FASE_3_MIGRATION": 60,
            "FASE_4_VALIDATION": 30
        }

    def start_monitoring(self, baseline_errors: int = None):
        """Iniciar monitoreo en tiempo real"""
        enviar_senal_log("INFO", "📊 Iniciando monitoreo de progreso en tiempo real", __name__, "monitor")

        if baseline_errors:
            self.baseline_errors = baseline_errors
        else:
            self.baseline_errors = self._count_vs_code_errors()

        self.monitoring = True
        print(self._generate_header())
        print(f"🎯 ERRORES BASELINE: {self.baseline_errors}")
        print("=" * 60)

        # Loop principal de monitoreo
        while self.monitoring:
            try:
                snapshot = self._capture_snapshot()
                self._display_progress(snapshot)
                self._check_alerts(snapshot)
                time.sleep(5)  # Actualizar cada 5 segundos

            except KeyboardInterrupt:
                self.stop_monitoring()
                break
            except Exception as e:
                enviar_senal_log("ERROR", f"Error en monitoreo: {e}", __name__, "monitor")
                time.sleep(10)

    def stop_monitoring(self):
        """Detener monitoreo"""
        self.monitoring = False
        print("\n🏁 MONITOREO FINALIZADO")
        final_snapshot = self._capture_snapshot()
        self._generate_final_report(final_snapshot)

    def update_phase(self, phase_name: str, files_total: int = 0):
        """Actualizar fase actual"""
        self.current_phase = phase_name
        self.phase_start_time = datetime.now()
        enviar_senal_log("INFO", f"📋 Iniciando fase: {phase_name}", __name__, "monitor")

    def mark_file_processed(self, file_path: str, errors_before: int, errors_after: int):
        """Marcar archivo como procesado"""
        self.processed_files.append({
            'file': file_path,
            'timestamp': datetime.now().isoformat(),
            'errors_before': errors_before,
            'errors_after': errors_after,
            'delta': errors_after - errors_before
        })

    def _capture_snapshot(self) -> ProgressSnapshot:
        """Capturar snapshot del estado actual"""
        current_time = datetime.now()
        elapsed = current_time - self.start_time
        current_errors = self._count_vs_code_errors()

        # Calcular ETA basado en progreso actual
        if self.baseline_errors > 0:
            progress_pct = max(0, (self.baseline_errors - current_errors) / self.baseline_errors)
            if progress_pct > 0:
                total_estimated = elapsed / progress_pct
                eta = total_estimated - elapsed
            else:
                eta = timedelta(hours=2)  # Estimación por defecto
        else:
            eta = timedelta(0)

        # Detectar archivo actual
        current_file = self._detect_current_file()

        # Generar alertas
        alerts = self._generate_alerts(current_errors, elapsed)

        return ProgressSnapshot(
            timestamp=current_time.isoformat(),
            vs_code_errors=current_errors,
            phase=self.current_phase,
            files_processed=len(self.processed_files),
            files_total=self._estimate_total_files(),
            elapsed_time=self._format_timedelta(elapsed),
            eta_remaining=self._format_timedelta(eta) if eta.total_seconds() > 0 else "Finalizando...",
            current_file=current_file,
            alerts=alerts
        )

    def _display_progress(self, snapshot: ProgressSnapshot):
        """Mostrar progreso en consola con formato ASCII"""
        # Limpiar pantalla (compatible con Windows)
        os.system('cls' if os.name == 'nt' else 'clear')

        print(self._generate_header())
        print()

        # Panel principal de progreso
        errors_delta = self.baseline_errors - snapshot.vs_code_errors
        progress_pct = max(0, errors_delta / self.baseline_errors * 100) if self.baseline_errors > 0 else 0

        print("┌─────────────────────────────────────────────────────────┐")
        print("│  📊 ICT ENGINE - PLAN PROGRESS LIVE                    │")
        print("├─────────────────────────────────────────────────────────┤")
        print(f"│  🎯 ERRORES VS CODE                                     │")
        print(f"│  ├─ Inicial: {self.baseline_errors:<8} Target: {self.target_errors:<8}              │")
        print(f"│  ├─ Actual:  {snapshot.vs_code_errors:<8} Delta: {errors_delta:+<8}             │")
        print(f"│  └─ Progreso: {progress_pct:5.1f}%                                │")
        print("├─────────────────────────────────────────────────────────┤")
        print(f"│  ⏱️  TIMING                                            │")
        print(f"│  ├─ Iniciado: {self.start_time.strftime('%H:%M:%S')}                              │")
        print(f"│  ├─ Transcurrido: {snapshot.elapsed_time:<12}                  │")
        print(f"│  └─ ETA: {snapshot.eta_remaining:<12}                          │")
        print("├─────────────────────────────────────────────────────────┤")
        print(f"│  📁 FASE ACTUAL: {snapshot.phase:<25}            │")
        print(f"│  ├─ Archivos procesados: {snapshot.files_processed:<8}                │")
        print(f"│  └─ Archivo actual: {snapshot.current_file[:35]:<35}│")
        print("├─────────────────────────────────────────────────────────┤")

        # Barra de progreso ASCII
        bar_width = 40
        filled = int(progress_pct / 100 * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)
        print(f"│  {bar} {progress_pct:5.1f}%  │")
        print("├─────────────────────────────────────────────────────────┤")

        # Alertas
        if snapshot.alerts:
            print("│  🚨 ALERTAS                                            │")
            for alert in snapshot.alerts[:3]:  # Mostrar máximo 3 alertas
                print(f"│  └─ {alert[:50]:<50}│")
        else:
            print("│  ✅ Sin alertas - Todo funcionando normalmente         │")

        print("└─────────────────────────────────────────────────────────┘")

        # Mostrar últimos archivos procesados
        if self.processed_files:
            print("\n📈 ÚLTIMOS ARCHIVOS PROCESADOS:")
            for file_data in self.processed_files[-5:]:  # Últimos 5
                file_name = Path(file_data['file']).name
                delta = file_data['delta']
                status = "✅" if delta <= 0 else "⚠️"
                print(f"   {status} {file_name:<30} ({delta:+3d} errores)")

        print(f"\n⏱️ Última actualización: {datetime.now().strftime('%H:%M:%S')}")

    def _count_vs_code_errors(self) -> int:
        """Contar errores actuales en VS Code"""
        try:
            # Ejecutar pylint para obtener count de errores
            result = subprocess.run([
                'python', '-m', 'pylint',
                '--errors-only',
                '--disable=C0103,C0114,C0115,C0116',
                'dashboard/', 'sistema/', 'core/', 'utils/'
            ],
            capture_output=True, text=True, cwd=self.project_root, timeout=30)

            # Contar líneas de error
            error_lines = [line for line in result.stdout.split('\n')
                          if line.strip() and not line.startswith('*')]
            return len(error_lines)

        except Exception as e:
            enviar_senal_log("WARNING", f"Error contando errores VS Code: {e}", __name__, "monitor")
            return 999  # Valor por defecto si no se puede obtener

    def _detect_current_file(self) -> str:
        """Detectar archivo que se está procesando actualmente"""
        # Buscar procesos de Python que podrían estar editando archivos
        try:
            # En entorno real, esto sería más sofisticado
            # Por ahora, devolver el último archivo procesado o mensaje genérico
            if self.processed_files:
                return Path(self.processed_files[-1]['file']).name
            else:
                return "Iniciando análisis..."
        except:
            return "Analizando..."

    def _generate_alerts(self, current_errors: int, elapsed: timedelta) -> List[str]:
        """Generar alertas basadas en métricas actuales"""
        alerts = []

        # Alerta si errores aumentan
        if hasattr(self, '_last_error_count'):
            if current_errors > self._last_error_count + self.alert_thresholds['error_increase_threshold']:
                alerts.append(f"⚠️ Errores aumentaron +{current_errors - self._last_error_count}")

        # Alerta si fase tarda mucho
        phase_estimate = self.phase_estimates.get(self.current_phase, 60)  # Default 60 min
        if hasattr(self, 'phase_start_time'):
            phase_elapsed = datetime.now() - self.phase_start_time
            if phase_elapsed.total_seconds() > phase_estimate * 60 * self.alert_thresholds['phase_timeout_multiplier']:
                alerts.append(f"⏱️ Fase {self.current_phase} excede tiempo estimado")

        # Alerta de progreso lento
        if elapsed.total_seconds() > 1800:  # Después de 30 min
            errors_reduced = self.baseline_errors - current_errors
            if errors_reduced < 10:
                alerts.append("🐌 Progreso más lento del esperado")

        self._last_error_count = current_errors
        return alerts

    def _check_alerts(self, snapshot: ProgressSnapshot):
        """Verificar y procesar alertas críticas"""
        for alert in snapshot.alerts:
            if "Errores aumentaron" in alert:
                enviar_senal_log("WARNING", f"ALERTA: {alert}", __name__, "monitor")
            elif "excede tiempo" in alert:
                enviar_senal_log("INFO", f"TIEMPO: {alert}", __name__, "monitor")

    def _estimate_total_files(self) -> int:
        """Estimar total de archivos a procesar"""
        # Contar archivos Python en directorios críticos
        total = 0
        for dir_name in ['dashboard', 'sistema', 'core', 'utils']:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                total += len(list(dir_path.rglob("*.py")))
        return total

    def _format_timedelta(self, td: timedelta) -> str:
        """Formatear timedelta a string legible"""
        hours, remainder = divmod(int(td.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def _generate_header(self) -> str:
        """Generar header ASCII"""
        return """
🚀 ICT ENGINE v5.0 - LIVE PROGRESS MONITOR
=========================================="""

    def _generate_final_report(self, final_snapshot: ProgressSnapshot):
        """Generar reporte final del monitoreo"""
        print("\n" + "="*60)
        print("📊 REPORTE FINAL DE MONITOREO")
        print("="*60)

        total_time = datetime.now() - self.start_time
        errors_reduced = self.baseline_errors - final_snapshot.vs_code_errors
        success_rate = (errors_reduced / self.baseline_errors * 100) if self.baseline_errors > 0 else 0

        print(f"⏱️ Tiempo total: {self._format_timedelta(total_time)}")
        print(f"🎯 Errores eliminados: {errors_reduced}/{self.baseline_errors}")
        print(f"📈 Tasa de éxito: {success_rate:.1f}%")
        print(f"📁 Archivos procesados: {final_snapshot.files_processed}")

        if self.processed_files:
            print(f"\n📋 ARCHIVOS MÁS IMPACTANTES:")
            # Ordenar por mayor reducción de errores
            sorted_files = sorted(self.processed_files,
                                key=lambda x: x['delta'], reverse=True)
            for file_data in sorted_files[:5]:
                file_name = Path(file_data['file']).name
                delta = file_data['delta']
                print(f"   🏆 {file_name}: {delta:+d} errores")

        # Guardar reporte completo
        report_path = self.project_root / "data" / "exports" / f"progress_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)

        report_data = {
            'final_snapshot': asdict(final_snapshot),
            'processed_files': self.processed_files,
            'total_time_seconds': total_time.total_seconds(),
            'success_rate': success_rate
        }

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        print(f"\n📄 Reporte completo guardado en: {report_path}")

def main():
    """Función principal para iniciar monitoreo"""
    print("📊 INICIANDO MONITOR DE PROGRESO EN TIEMPO REAL")
    print("=" * 50)

    project_root = Path.cwd()
    monitor = LiveProgressMonitor(project_root)

    try:
        monitor.start_monitoring()
    except KeyboardInterrupt:
        print("\n⚠️ Monitoreo interrumpido por usuario")
    finally:
        monitor.stop_monitoring()

if __name__ == "__main__":
    main()
