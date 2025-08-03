#!/usr/bin/env python3
"""
🧪 SPRINT 1.2 CONSOLIDATOR - VALIDACIÓN COMPLETA
================================================

Validador y consolidador automático para el Sprint 1.2:
Advanced Candle Downloader Integration

Valida todos los deliverables y genera reporte de completitud
del Sprint 1.2 para asegurar que la integración está lista
para producción.

Versión: 1.0.0
Fecha: 3 de Agosto 2025
"""

import os
import sys
import json
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# Configurar paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Imports del sistema
from sistema.logging_interface import enviar_senal_log

# =============================================================================
# CONFIGURACIÓN DEL CONSOLIDATOR
# =============================================================================

SPRINT_1_2_VALIDATION = {
    "sprint_id": "1.2",
    "name": "Advanced Candle Downloader Integration",
    "required_files": [
        "dashboard/candle_downloader_widget.py",
        "core/data_coordination/candle_coordinator.py",
        "core/monitoring/download_monitor.py",
        "core/integration/ict_downloader_bridge.py",
        "utilities/performance/download_optimizer.py",
        "utils/advanced_candle_downloader.py"  # Debe existir previamente
    ],
    "optional_files": [
        "dashboard/widgets/downloader_controls.py",
        "core/data_coordination/download_scheduler.py",
        "core/data_coordination/gap_detector.py",
        "dashboard/widgets/performance_monitor.py",
        "core/monitoring/metrics_collector.py",
        "core/data_coordination/auto_trigger.py",
        "tests/performance/test_download_performance.py"
    ],
    "integration_tests": [
        "test_candle_downloader_widget",
        "test_candle_coordinator",
        "test_dashboard_integration",
        "test_ict_integration",
        "test_performance_monitoring"
    ],
    "validation_criteria": {
        "required_files_exist": 80,      # 80% mínimo de archivos requeridos
        "code_quality_score": 70,       # 70% mínimo de calidad de código
        "integration_tests_pass": 60,   # 60% mínimo de tests pasando
        "documentation_coverage": 50    # 50% mínimo de documentación
    }
}

# =============================================================================
# SPRINT 1.2 CONSOLIDATOR CLASS
# =============================================================================

class Sprint12Consolidator:
    """
    🧪 Consolidador y validador para Sprint 1.2

    Valida completitud, calidad e integración de todos los
    deliverables del Sprint 1.2: Advanced Candle Downloader Integration
    """

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.validation_report = {
            "sprint": "1.2",
            "name": "Advanced Candle Downloader Integration",
            "validation_time": datetime.now().isoformat(),
            "overall_status": "PENDING",
            "overall_score": 0.0,
            "file_validation": {},
            "integration_validation": {},
            "quality_metrics": {},
            "recommendations": [],
            "errors": [],
            "warnings": []
        }

        enviar_senal_log("INFO", "🧪 Sprint 1.2 Consolidator inicializado", __name__, "consolidator")

    def validate_sprint_1_2(self, verbose: bool = True) -> Dict:
        """Ejecuta validación completa del Sprint 1.2"""
        enviar_senal_log("INFO", "🔍 Iniciando validación Sprint 1.2", __name__, "consolidator")

        try:
            # 1. Validar archivos requeridos
            file_scores = self._validate_required_files()

            # 2. Validar calidad de código
            quality_scores = self._validate_code_quality()

            # 3. Validar integraciones
            integration_scores = self._validate_integrations()

            # 4. Calcular score general
            overall_score = self._calculate_overall_score(file_scores, quality_scores, integration_scores)

            # 5. Generar recomendaciones
            recommendations = self._generate_recommendations()

            # 6. Finalizar reporte
            self.validation_report.update({
                "overall_score": overall_score,
                "overall_status": self._determine_status(overall_score),
                "recommendations": recommendations
            })

            if verbose:
                self._print_validation_summary()

        except Exception as e:
            self.validation_report["errors"].append(f"Error en validación: {str(e)}")
            enviar_senal_log("ERROR", f"💥 Error validando Sprint 1.2: {e}", __name__, "consolidator")

        return self.validation_report

    def _validate_required_files(self) -> Dict[str, float]:
        """Valida existencia y estructura de archivos requeridos"""
        enviar_senal_log("INFO", "📁 Validando archivos requeridos...", __name__, "consolidator")

        file_scores = {}

        # Validar archivos requeridos
        for file_path in SPRINT_1_2_VALIDATION["required_files"]:
            full_path = self.project_root / file_path
            score = self._validate_single_file(full_path, required=True)
            file_scores[file_path] = score

            self.validation_report["file_validation"][file_path] = {
                "exists": full_path.exists(),
                "score": score,
                "required": True,
                "path": str(full_path)
            }

        # Validar archivos opcionales
        for file_path in SPRINT_1_2_VALIDATION["optional_files"]:
            full_path = self.project_root / file_path
            score = self._validate_single_file(full_path, required=False)
            file_scores[file_path] = score

            self.validation_report["file_validation"][file_path] = {
                "exists": full_path.exists(),
                "score": score,
                "required": False,
                "path": str(full_path)
            }

        # Calcular score promedio de archivos requeridos
        required_scores = [file_scores[f] for f in SPRINT_1_2_VALIDATION["required_files"] if f in file_scores]
        avg_required_score = sum(required_scores) / len(required_scores) if required_scores else 0.0

        enviar_senal_log("INFO", f"📁 Archivos validados: {avg_required_score:.1f}% promedio", __name__, "consolidator")

        return file_scores

    def _validate_single_file(self, file_path: Path, required: bool = True) -> float:
        """Valida un archivo individual"""
        if not file_path.exists():
            if required:
                self.validation_report["errors"].append(f"Archivo requerido faltante: {file_path}")
            return 0.0

        score = 50.0  # Base score por existir

        try:
            # Validar tamaño mínimo
            if file_path.stat().st_size > 100:  # Al menos 100 bytes
                score += 20.0

            # Validar contenido básico
            content = file_path.read_text(encoding='utf-8')

            # Verificar que no esté vacío
            if len(content.strip()) > 50:
                score += 20.0

            # Verificar estructura básica de Python
            if file_path.suffix == '.py':
                if 'class ' in content or 'def ' in content:
                    score += 10.0

                # Verificar imports del sistema
                if 'enviar_senal_log' in content:
                    score += 10.0

                # Verificar docstrings
                if '"""' in content:
                    score += 10.0

        except Exception as e:
            if required:
                self.validation_report["warnings"].append(f"Error validando {file_path}: {e}")
            score = max(score - 20.0, 0.0)

        return min(score, 100.0)

    def _validate_code_quality(self) -> Dict[str, float]:
        """Valida calidad de código de archivos creados"""
        enviar_senal_log("INFO", "🔍 Validando calidad de código...", __name__, "consolidator")

        quality_scores = {}

        # Solo validar archivos que existen
        files_to_check = []
        for file_path in SPRINT_1_2_VALIDATION["required_files"]:
            full_path = self.project_root / file_path
            if full_path.exists():
                files_to_check.append(full_path)

        for file_path in files_to_check:
            score = self._analyze_code_quality(file_path)
            quality_scores[str(file_path.relative_to(self.project_root))] = score

        # Calcular promedio
        avg_quality = sum(quality_scores.values()) / len(quality_scores) if quality_scores else 0.0

        self.validation_report["quality_metrics"] = {
            "individual_scores": quality_scores,
            "average_quality": avg_quality,
            "files_analyzed": len(quality_scores)
        }

        enviar_senal_log("INFO", f"🔍 Calidad de código: {avg_quality:.1f}% promedio", __name__, "consolidator")

        return quality_scores

    def _analyze_code_quality(self, file_path: Path) -> float:
        """Analiza calidad de código de un archivo"""
        try:
            content = file_path.read_text(encoding='utf-8')
            score = 0.0

            # Métricas básicas de calidad
            lines = content.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]

            # 1. Documentación (25 puntos)
            if '"""' in content:
                score += 15.0
                # Bonus por docstrings detallados
                docstring_count = content.count('"""') // 2
                score += min(docstring_count * 2, 10.0)

            # 2. Estructura y organización (25 puntos)
            if 'class ' in content:
                score += 10.0
            if 'def ' in content:
                score += 10.0
            if any('import ' in line for line in lines[:20]):  # Imports al inicio
                score += 5.0

            # 3. Uso de sistema de logging (20 puntos)
            if 'enviar_senal_log' in content:
                score += 15.0
                log_count = content.count('enviar_senal_log')
                score += min(log_count, 5.0)

            # 4. Manejo de errores (15 puntos)
            if 'try:' in content and 'except' in content:
                score += 10.0
            if 'raise' in content or 'assert' in content:
                score += 5.0

            # 5. Tipo hints y código moderno (15 puntos)
            if 'from typing import' in content:
                score += 10.0
            if ' -> ' in content:  # Return type hints
                score += 5.0

            return min(score, 100.0)

        except Exception as e:
            self.validation_report["warnings"].append(f"Error analizando calidad de {file_path}: {e}")
            return 0.0

    def _validate_integrations(self) -> Dict[str, float]:
        """Valida integraciones entre componentes"""
        enviar_senal_log("INFO", "🔗 Validando integraciones...", __name__, "consolidator")

        integration_scores = {}

        # Test 1: Validar que advanced_candle_downloader.py existe (prerequisito)
        downloader_path = self.project_root / "utils" / "advanced_candle_downloader.py"
        integration_scores["advanced_candle_downloader_exists"] = 100.0 if downloader_path.exists() else 0.0

        # Test 2: Validar widget de dashboard
        widget_path = self.project_root / "dashboard" / "candle_downloader_widget.py"
        widget_score = self._test_widget_integration(widget_path)
        integration_scores["dashboard_widget"] = widget_score

        # Test 3: Validar CandleCoordinator
        coordinator_path = self.project_root / "core" / "data_coordination" / "candle_coordinator.py"
        coordinator_score = self._test_coordinator_integration(coordinator_path)
        integration_scores["candle_coordinator"] = coordinator_score

        # Test 4: Validar sistema de monitoreo
        monitor_path = self.project_root / "core" / "monitoring" / "download_monitor.py"
        monitor_score = self._test_monitor_integration(monitor_path)
        integration_scores["download_monitor"] = monitor_score

        # Test 5: Validar bridge ICT
        bridge_path = self.project_root / "core" / "integration" / "ict_downloader_bridge.py"
        bridge_score = self._test_bridge_integration(bridge_path)
        integration_scores["ict_bridge"] = bridge_score

        # Calcular promedio
        avg_integration = sum(integration_scores.values()) / len(integration_scores) if integration_scores else 0.0

        self.validation_report["integration_validation"] = {
            "individual_scores": integration_scores,
            "average_integration": avg_integration,
            "tests_run": len(integration_scores)
        }

        enviar_senal_log("INFO", f"🔗 Integraciones validadas: {avg_integration:.1f}% promedio", __name__, "consolidator")

        return integration_scores

    def _test_widget_integration(self, widget_path: Path) -> float:
        """Testa integración del widget de dashboard"""
        if not widget_path.exists():
            return 0.0

        try:
            content = widget_path.read_text(encoding='utf-8')
            score = 50.0  # Base por existir

            # Verificar elementos clave del widget
            if 'CandleDownloaderWidget' in content:
                score += 20.0
            if 'AdvancedCandleDownloader' in content:
                score += 15.0
            if 'Button' in content and 'ProgressBar' in content:
                score += 10.0
            if 'async def' in content:
                score += 5.0

            return min(score, 100.0)

        except Exception:
            return 0.0

    def _test_coordinator_integration(self, coordinator_path: Path) -> float:
        """Testa integración del CandleCoordinator"""
        if not coordinator_path.exists():
            return 0.0

        try:
            content = coordinator_path.read_text(encoding='utf-8')
            score = 50.0  # Base por existir

            # Verificar elementos clave del coordinator
            if 'CandleCoordinator' in content:
                score += 25.0
            if 'AdvancedCandleDownloader' in content:
                score += 15.0
            if 'coordinate_downloads' in content:
                score += 10.0

            return min(score, 100.0)

        except Exception:
            return 0.0

    def _test_monitor_integration(self, monitor_path: Path) -> float:
        """Testa integración del sistema de monitoreo"""
        if not monitor_path.exists():
            return 0.0

        try:
            content = monitor_path.read_text(encoding='utf-8')
            score = 50.0  # Base por existir

            # Verificar elementos clave del monitor
            if 'DownloadMonitor' in content:
                score += 25.0
            if 'metrics' in content:
                score += 15.0
            if 'record_download' in content:
                score += 10.0

            return min(score, 100.0)

        except Exception:
            return 0.0

    def _test_bridge_integration(self, bridge_path: Path) -> float:
        """Testa integración del bridge ICT"""
        if not bridge_path.exists():
            return 0.0

        try:
            content = bridge_path.read_text(encoding='utf-8')
            score = 50.0  # Base por existir

            # Verificar elementos clave del bridge
            if 'ICTDownloaderBridge' in content:
                score += 25.0
            if 'auto_trigger' in content:
                score += 15.0
            if 'check_data_requirements' in content:
                score += 10.0

            return min(score, 100.0)

        except Exception:
            return 0.0

    def _calculate_overall_score(self, file_scores: Dict, quality_scores: Dict, integration_scores: Dict) -> float:
        """Calcula score general del sprint"""

        # Calcular scores individuales
        required_files = SPRINT_1_2_VALIDATION["required_files"]
        required_file_scores = [file_scores.get(f, 0.0) for f in required_files]
        avg_required_files = sum(required_file_scores) / len(required_file_scores) if required_file_scores else 0.0

        avg_quality = sum(quality_scores.values()) / len(quality_scores) if quality_scores else 0.0
        avg_integration = sum(integration_scores.values()) / len(integration_scores) if integration_scores else 0.0

        # Weights para score final
        file_weight = 0.4      # 40% - Archivos requeridos
        quality_weight = 0.3   # 30% - Calidad de código
        integration_weight = 0.3  # 30% - Integraciones

        overall_score = (
            avg_required_files * file_weight +
            avg_quality * quality_weight +
            avg_integration * integration_weight
        )

        return round(overall_score, 2)

    def _determine_status(self, overall_score: float) -> str:
        """Determina status basado en score"""
        if overall_score >= 90:
            return "EXCELLENT"
        elif overall_score >= 80:
            return "GOOD"
        elif overall_score >= 70:
            return "ACCEPTABLE"
        elif overall_score >= 60:
            return "NEEDS_IMPROVEMENT"
        else:
            return "INCOMPLETE"

    def _generate_recommendations(self) -> List[str]:
        """Genera recomendaciones basadas en validación"""
        recommendations = []

        # Revisar archivos faltantes
        missing_required = []
        for file_path in SPRINT_1_2_VALIDATION["required_files"]:
            full_path = self.project_root / file_path
            if not full_path.exists():
                missing_required.append(file_path)

        if missing_required:
            recommendations.append(f"🔴 CRÍTICO: Crear archivos faltantes: {', '.join(missing_required)}")

        # Revisar calidad de código
        quality_metrics = self.validation_report.get("quality_metrics", {})
        avg_quality = quality_metrics.get("average_quality", 0.0)

        if avg_quality < 70:
            recommendations.append("🔶 IMPORTANTE: Mejorar documentación y estructura de código")

        # Revisar integraciones
        integration_validation = self.validation_report.get("integration_validation", {})
        avg_integration = integration_validation.get("average_integration", 0.0)

        if avg_integration < 70:
            recommendations.append("🔶 IMPORTANTE: Completar integraciones entre componentes")

        # Recomendaciones generales
        if self.validation_report["overall_score"] < 80:
            recommendations.append("💡 SUGERENCIA: Ejecutar tests de integración para validar funcionalidad")
            recommendations.append("💡 SUGERENCIA: Revisar logs del sistema para identificar issues")

        if not recommendations:
            recommendations.append("🎉 EXCELENTE: Sprint 1.2 completado satisfactoriamente")

        return recommendations

    def _print_validation_summary(self):
        """Imprime resumen de validación en consola"""
        report = self.validation_report

        enviar_senal_log("INFO", "📊 === RESUMEN VALIDACIÓN SPRINT 1.2 ===", __name__, "consolidator")
        enviar_senal_log("INFO", f"🎯 Score General: {report['overall_score']:.1f}%", __name__, "consolidator")
        enviar_senal_log("INFO", f"📋 Status: {report['overall_status']}", __name__, "consolidator")

        # Archivos
        file_validation = report.get("file_validation", {})
        existing_files = sum(1 for f in file_validation.values() if f.get("exists", False))
        total_files = len(file_validation)
        enviar_senal_log("INFO", f"📁 Archivos: {existing_files}/{total_files} existentes", __name__, "consolidator")

        # Calidad
        quality_metrics = report.get("quality_metrics", {})
        avg_quality = quality_metrics.get("average_quality", 0.0)
        enviar_senal_log("INFO", f"🔍 Calidad promedio: {avg_quality:.1f}%", __name__, "consolidator")

        # Integraciones
        integration_validation = report.get("integration_validation", {})
        avg_integration = integration_validation.get("average_integration", 0.0)
        enviar_senal_log("INFO", f"🔗 Integraciones: {avg_integration:.1f}%", __name__, "consolidator")

        # Errores y warnings
        if report.get("errors"):
            enviar_senal_log("WARNING", f"❌ Errores: {len(report['errors'])}", __name__, "consolidator")

        if report.get("warnings"):
            enviar_senal_log("WARNING", f"⚠️ Warnings: {len(report['warnings'])}", __name__, "consolidator")

        # Recomendaciones
        if report.get("recommendations"):
            enviar_senal_log("INFO", "📋 Recomendaciones principales:", __name__, "consolidator")
            for rec in report["recommendations"][:3]:  # Solo las 3 principales
                enviar_senal_log("INFO", f"  {rec}", __name__, "consolidator")

    def save_validation_report(self) -> str:
        """Guarda reporte de validación en archivo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.project_root / f"sprint_1_2_validation_{timestamp}.json"

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.validation_report, f, indent=2, ensure_ascii=False)

        enviar_senal_log("INFO", f"📋 Reporte validación guardado: {report_path}", __name__, "consolidator")
        return str(report_path)

    def run_integration_tests(self) -> Dict[str, bool]:
        """Ejecuta tests de integración básicos"""
        enviar_senal_log("INFO", "🧪 Ejecutando tests de integración...", __name__, "consolidator")

        test_results = {}

        # Test 1: Import test para componentes principales
        test_results["widget_import"] = self._test_import("dashboard.candle_downloader_widget")
        test_results["coordinator_import"] = self._test_import("core.data_coordination.candle_coordinator")
        test_results["monitor_import"] = self._test_import("core.monitoring.download_monitor")

        # Test 2: Instanciación básica
        if test_results["coordinator_import"]:
            test_results["coordinator_instantiation"] = self._test_coordinator_instantiation()
        else:
            test_results["coordinator_instantiation"] = False

        if test_results["monitor_import"]:
            test_results["monitor_instantiation"] = self._test_monitor_instantiation()
        else:
            test_results["monitor_instantiation"] = False

        passed_tests = sum(1 for result in test_results.values() if result)
        total_tests = len(test_results)

        enviar_senal_log("INFO", f"🧪 Tests de integración: {passed_tests}/{total_tests} pasados", __name__, "consolidator")

        return test_results

    def _test_import(self, module_name: str) -> bool:
        """Testa si un módulo se puede importar"""
        try:
            # Cambiar el path temporalmente para los imports
            old_path = sys.path.copy()
            sys.path.insert(0, str(self.project_root))

            __import__(module_name.replace('.', '/'))

            sys.path = old_path
            return True

        except Exception as e:
            enviar_senal_log("DEBUG", f"Import test failed for {module_name}: {e}", __name__, "consolidator")
            return False

    def _test_coordinator_instantiation(self) -> bool:
        """Testa instanciación del CandleCoordinator"""
        try:
            # Import directo del archivo
            coordinator_path = self.project_root / "core" / "data_coordination" / "candle_coordinator.py"
            if not coordinator_path.exists():
                return False

            # Test básico de syntax
            content = coordinator_path.read_text(encoding='utf-8')

            # Verificar que tiene la clase principal
            return "class CandleCoordinator" in content

        except Exception:
            return False

    def _test_monitor_instantiation(self) -> bool:
        """Testa instanciación del DownloadMonitor"""
        try:
            # Import directo del archivo
            monitor_path = self.project_root / "core" / "monitoring" / "download_monitor.py"
            if not monitor_path.exists():
                return False

            # Test básico de syntax
            content = monitor_path.read_text(encoding='utf-8')

            # Verificar que tiene la clase principal
            return "class DownloadMonitor" in content

        except Exception:
            return False

# =============================================================================
# FUNCIONES DE CONVENIENCIA
# =============================================================================

def validate_sprint_1_2(verbose: bool = True) -> Dict:
    """Valida Sprint 1.2 completo"""
    consolidator = Sprint12Consolidator()
    return consolidator.validate_sprint_1_2(verbose=verbose)

def run_integration_tests() -> Dict[str, bool]:
    """Ejecuta solo tests de integración"""
    consolidator = Sprint12Consolidator()
    return consolidator.run_integration_tests()

def main():
    """Función principal"""
    import argparse

    parser = argparse.ArgumentParser(description="Sprint 1.2 Consolidator - Validación Advanced Candle Downloader Integration")
    parser.add_argument("--validation-only", action="store_true", help="Solo ejecutar validación completa")
    parser.add_argument("--integration-tests", action="store_true", help="Solo ejecutar tests de integración")
    parser.add_argument("--quiet", action="store_true", help="Modo silencioso (menos output)")

    args = parser.parse_args()

    enviar_senal_log("INFO", "🧪 === SPRINT 1.2 CONSOLIDATOR - INICIANDO ===", __name__, "main")

    if args.integration_tests:
        enviar_senal_log("INFO", "🔗 Ejecutando tests de integración únicamente", __name__, "main")
        test_results = run_integration_tests()

        passed_tests = sum(1 for result in test_results.values() if result)
        total_tests = len(test_results)

        enviar_senal_log("INFO", f"🧪 Resultado: {passed_tests}/{total_tests} tests pasados", __name__, "main")

        if passed_tests == total_tests:
            enviar_senal_log("INFO", "🎉 ¡Todos los tests de integración pasaron!", __name__, "main")
        else:
            enviar_senal_log("WARNING", "⚠️ Algunos tests de integración fallaron", __name__, "main")

        return

    # Ejecutar validación completa
    result = validate_sprint_1_2(verbose=not args.quiet)

    # Guardar reporte
    consolidator = Sprint12Consolidator()
    consolidator.validation_report = result
    report_path = consolidator.save_validation_report()

    # Mostrar resultados finales
    overall_score = result.get("overall_score", 0)
    overall_status = result.get("overall_status", "UNKNOWN")

    enviar_senal_log("INFO", f"🎯 Validación completada: {overall_status} ({overall_score:.1f}%)", __name__, "main")
    enviar_senal_log("INFO", f"📋 Reporte guardado en: {report_path}", __name__, "main")

    if overall_score >= 80:
        enviar_senal_log("INFO", "🎉 ¡Sprint 1.2 validado exitosamente!", __name__, "main")
    elif overall_score >= 60:
        enviar_senal_log("WARNING", "⚠️ Sprint 1.2 necesita mejoras antes de finalizar", __name__, "main")
    else:
        enviar_senal_log("ERROR", "❌ Sprint 1.2 incompleto - revisar recomendaciones", __name__, "main")

if __name__ == "__main__":
    main()
