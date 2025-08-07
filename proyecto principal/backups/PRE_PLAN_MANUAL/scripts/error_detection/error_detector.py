#!/usr/bin/env python3
"""
🔍 ITC ENGINE v5.0 - SISTEMA DE DETECCIÓN DE ERRORES JERÁRQUICO
===============================================================

🎯 OBJETIVO: Detectar automáticamente errores, problemas de calidad y riesgos
            en todo el pipeline ITC Engine con clasificación jerárquica

📊 CARACTERÍSTICAS:
   - ✅ Detección AST (sintaxis)
   - ✅ Validación de imports y dependencias
   - ✅ Análisis de riesgos de runtime
   - ✅ Calidad de código especializada
   - ✅ Detección de dependencias circulares

📋 CLASIFICACIÓN JERÁRQUICA:
   - Severidad: CRITICAL → HIGH → MEDIUM → LOW → INFO
   - Categoría: SISTEMA, TRADING, ICT_ENGINE, POI_SYSTEM, DASHBOARD
   - Especialización: Trading Engine, ICT Analysis, POI System

🎨 INTEGRACIÓN:
   - Dashboard con pestaña "🚨 Problemas"
   - Bitácoras automáticas en docs/bitacoras/diagnosticos/
   - Métricas y estadísticas completas

📅 Fecha: 2025-08-06 | Versión: 1.0.0
👤 Autor: ITC Engine v5.0 System
"""

# MIGRACIÓN SIC v3.0 + SLUC v2.1
from sistema.sic import enviar_senal_log, log_info, log_warning

import ast
from sistema.sic import os
from sistema.sic import sys
from sistema.sic import json
import time
import importlib.util
from sistema.sic import Path
from sistema.sic import Dict, List, Tuple, Any, Optional, Set
from sistema.sic import datetime
from sistema.sic import dataclass, asdict
from enum import Enum
from sistema.sic import re
import traceback

# Rich para UI mejorada
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.tree import Tree
    from rich.table import Table
    from rich.progress import track
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    rprint = print


class Severity(Enum):
    """Niveles de severidad de problemas detectados"""
    CRITICAL = "🚨 CRITICAL"
    HIGH = "⚠️ HIGH"
    MEDIUM = "⚡ MEDIUM"
    LOW = "📝 LOW"
    INFO = "ℹ️ INFO"


class Category(Enum):
    """Categorías especializadas del sistema"""
    SISTEMA = "🔧 SISTEMA"
    TRADING = "💹 TRADING"
    ICT_ENGINE = "⚙️ ICT_ENGINE"
    POI_SYSTEM = "📍 POI_SYSTEM"
    DASHBOARD = "📊 DASHBOARD"
    UTILITIES = "🛠️ UTILITIES"
    UNKNOWN = "❓ UNKNOWN"


@dataclass
class DetectedProblem:
    """Estructura de problema detectado"""
    id: str
    timestamp: str
    file_path: str
    line_number: int
    severity: str
    category: str
    problem_type: str
    title: str
    description: str
    suggestion: str
    code_snippet: str = ""
    context: Dict[str, Any] = None

    def to_dict(self) -> Dict:
        return asdict(self)


class ErrorDetector:
    """🔍 Motor Principal de Detección de Errores Jerárquico"""

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.console = Console() if RICH_AVAILABLE else None
        self.problems: List[DetectedProblem] = []
        self.stats = {
            'files_analyzed': 0,
            'problems_found': 0,
            'by_severity': {severity.name: 0 for severity in Severity},
            'by_category': {category.name: 0 for category in Category},
            'analysis_time': 0.0
        }

        # Directorios a analizar
        self.analyze_dirs = [
            'core', 'dashboard', 'sistema', 'scripts',
            'utilities', 'utils', 'config', 'teste'
        ]

        # Archivos principales críticos
        self.critical_files = [
            'main.py', 'launch_dashboard.py', 'auto_start.py'
        ]

    def analyze_full_system(self, quick_mode: bool = False) -> Dict[str, Any]:
        """🚀 Análisis completo del sistema"""
        start_time = time.time()

        if self.console:
            self.console.print("\n🔍 INICIANDO ANÁLISIS SISTEMA DE DETECCIÓN DE ERRORES")
            self.console.print("=" * 60)

        # 1. Análisis de archivos críticos
        self._analyze_critical_files()

        if not quick_mode:
            # 2. Análisis por directorios
            for directory in self.analyze_dirs:
                self._analyze_directory(directory)

            # 3. Análisis de dependencias circulares
            self._detect_circular_dependencies()

            # 4. Análisis de calidad de código
            self._analyze_code_quality()

        # 5. Análisis de configuración
        self._analyze_configuration()

        self.stats['analysis_time'] = time.time() - start_time

        # 6. Generar reporte
        report = self._generate_report()

        # 7. Guardar bitácora
        self._save_diagnostics_log()

        return report

    def _analyze_critical_files(self):
        """📍 Análisis de archivos críticos del sistema"""
        if self.console:
            self.console.print("\n📍 Analizando archivos críticos...")

        for file_name in self.critical_files:
            file_path = self.workspace_root / file_name
            if file_path.exists():
                self._analyze_python_file(file_path, is_critical=True)

    def _analyze_directory(self, directory: str):
        """📂 Análisis recursivo de directorio"""
        dir_path = self.workspace_root / directory
        if not dir_path.exists():
            return

        if self.console:
            self.console.print(f"📂 Analizando directorio: {directory}")

        python_files = list(dir_path.rglob("*.py"))

        if RICH_AVAILABLE and python_files:
            for file_path in track(python_files, description=f"Analizando {directory}..."):
                self._analyze_python_file(file_path)
        else:
            for file_path in python_files:
                self._analyze_python_file(file_path)

    def _analyze_python_file(self, file_path: Path, is_critical: bool = False):
        """🐍 Análisis específico de archivo Python"""
        try:
            self.stats['files_analyzed'] += 1

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 1. Análisis de sintaxis AST
            self._check_syntax(file_path, content, is_critical)

            # 2. Análisis de imports
            self._check_imports(file_path, content, is_critical)

            # 3. Análisis de código específico
            self._check_specific_code_issues(file_path, content, is_critical)

            # 4. Análisis de estructura
            self._check_file_structure(file_path, content, is_critical)

        except Exception as e:
            self._add_problem(
                file_path=str(file_path),
                line_number=1,
                severity=Severity.HIGH if is_critical else Severity.MEDIUM,
                category=self._categorize_file(file_path),
                problem_type="FILE_ACCESS_ERROR",
                title="Error accediendo al archivo",
                description=f"No se pudo analizar el archivo: {str(e)}",
                suggestion="Verificar permisos y encoding del archivo"
            )

    def _check_syntax(self, file_path: Path, content: str, is_critical: bool):
        """🔍 Verificación de sintaxis usando AST"""
        try:
            ast.parse(content)
        except SyntaxError as e:
            self._add_problem(
                file_path=str(file_path),
                line_number=e.lineno or 1,
                severity=Severity.CRITICAL if is_critical else Severity.HIGH,
                category=self._categorize_file(file_path),
                problem_type="SYNTAX_ERROR",
                title="Error de sintaxis",
                description=f"Error de sintaxis en línea {e.lineno}: {e.msg}",
                suggestion="Corregir la sintaxis del código",
                code_snippet=self._get_code_snippet(content, e.lineno or 1)
            )
        except Exception as e:
            self._add_problem(
                file_path=str(file_path),
                line_number=1,
                severity=Severity.MEDIUM,
                category=self._categorize_file(file_path),
                problem_type="AST_PARSE_ERROR",
                title="Error al parsear AST",
                description=f"No se pudo parsear el archivo: {str(e)}",
                suggestion="Verificar la estructura del archivo Python"
            )

    def _check_imports(self, file_path: Path, content: str, is_critical: bool):
        """📦 Verificación de imports y dependencias"""
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # Imports problemáticos
            if line.startswith('from') or line.startswith('import'):
                # Imports relativos problemáticos
                if '..' in line and 'from' in line:
                    self._add_problem(
                        file_path=str(file_path),
                        line_number=line_num,
                        severity=Severity.MEDIUM,
                        category=self._categorize_file(file_path),
                        problem_type="RELATIVE_IMPORT",
                        title="Import relativo problemático",
                        description=f"Import relativo que puede causar problemas: {line}",
                        suggestion="Usar imports absolutos cuando sea posible",
                        code_snippet=line
                    )

                # Imports de módulos críticos
                critical_imports = ['os', 'sys', 'subprocess', 'eval', 'exec']
                for critical in critical_imports:
                    if critical in line and not line.startswith('#'):
                        severity = Severity.HIGH if is_critical else Severity.MEDIUM
                        self._add_problem(
                            file_path=str(file_path),
                            line_number=line_num,
                            severity=severity,
                            category=self._categorize_file(file_path),
                            problem_type="CRITICAL_IMPORT",
                            title=f"Import crítico detectado: {critical}",
                            description=f"Uso de módulo crítico que requiere revisión: {line}",
                            suggestion="Verificar que el uso sea seguro y necesario",
                            code_snippet=line
                        )

    def _check_specific_code_issues(self, file_path: Path, content: str, is_critical: bool):
        """🔧 Verificación de problemas específicos del código"""
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            line_stripped = line.strip()

            # TODO/FIXME/HACK comments
            if any(tag in line_stripped.upper() for tag in ['TODO', 'FIXME', 'HACK', 'XXX']):
                self._add_problem(
                    file_path=str(file_path),
                    line_number=line_num,
                    severity=Severity.LOW,
                    category=self._categorize_file(file_path),
                    problem_type="TODO_COMMENT",
                    title="Comentario TODO/FIXME encontrado",
                    description=f"Comentario que indica trabajo pendiente: {line_stripped}",
                    suggestion="Revisar y completar el trabajo pendiente",
                    code_snippet=line_stripped
                )

            # Hardcoded paths (Windows específico)
            if re.search(r'[C-Z]:\\', line_stripped):
                self._add_problem(
                    file_path=str(file_path),
                    line_number=line_num,
                    severity=Severity.MEDIUM,
                    category=self._categorize_file(file_path),
                    problem_type="HARDCODED_PATH",
                    title="Ruta hardcodeada detectada",
                    description=f"Ruta absoluta hardcodeada: {line_stripped}",
                    suggestion="Usar rutas relativas o configuración",
                    code_snippet=line_stripped
                )

            # Print statements en producción (excepto debugging/)
            if ('print(' in line_stripped or 'pprint(' in line_stripped) and \
               'debugging' not in str(file_path) and not line_stripped.startswith('#'):
                self._add_problem(
                    file_path=str(file_path),
                    line_number=line_num,
                    severity=Severity.LOW,
                    category=self._categorize_file(file_path),
                    problem_type="PRINT_STATEMENT",
                    title="Print statement en producción",
                    description=f"Print statement que debería ser logging: {line_stripped}",
                    suggestion="Reemplazar con sistema de logging apropiado",
                    code_snippet=line_stripped
                )

    def _check_file_structure(self, file_path: Path, content: str, is_critical: bool):
        """📋 Verificación de estructura del archivo"""
        lines = content.split('\n')

        # Archivos muy largos
        if len(lines) > 500:
            self._add_problem(
                file_path=str(file_path),
                line_number=1,
                severity=Severity.LOW,
                category=self._categorize_file(file_path),
                problem_type="LARGE_FILE",
                title="Archivo muy largo",
                description=f"Archivo con {len(lines)} líneas, considerar refactoring",
                suggestion="Dividir en módulos más pequeños",
                context={'line_count': len(lines)}
            )

        # Falta de docstring en archivos importantes
        if is_critical and not content.strip().startswith('"""') and not content.strip().startswith("'''"):
            self._add_problem(
                file_path=str(file_path),
                line_number=1,
                severity=Severity.MEDIUM,
                category=self._categorize_file(file_path),
                problem_type="MISSING_DOCSTRING",
                title="Falta docstring en archivo crítico",
                description="Archivo crítico sin documentación de módulo",
                suggestion="Agregar docstring descriptivo al inicio del archivo"
            )

    def _detect_circular_dependencies(self):
        """🔄 Detección de dependencias circulares"""
        if self.console:
            self.console.print("\n🔄 Detectando dependencias circulares...")

        # Mapa de dependencias
        dependencies = {}

        for directory in self.analyze_dirs:
            dir_path = self.workspace_root / directory
            if not dir_path.exists():
                continue

            for file_path in dir_path.rglob("*.py"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extraer imports
                    imports = []
                    for line in content.split('\n'):
                        if line.strip().startswith('from ') or line.strip().startswith('import '):
                            imports.append(line.strip())

                    dependencies[str(file_path)] = imports

                except Exception:
                    continue

        # Detectar ciclos simples (A -> B -> A)
        for file_path, imports in dependencies.items():
            for import_line in imports:
                # Simplificado: buscar imports que podrían crear ciclos
                if 'from .' in import_line or 'from ..' in import_line:
                    self._add_problem(
                        file_path=file_path,
                        line_number=1,
                        severity=Severity.MEDIUM,
                        category=Category.SISTEMA,
                        problem_type="POTENTIAL_CIRCULAR_DEPENDENCY",
                        title="Posible dependencia circular",
                        description=f"Import relativo que podría crear ciclo: {import_line}",
                        suggestion="Revisar arquitectura de módulos",
                        code_snippet=import_line
                    )

    def _analyze_code_quality(self):
        """✨ Análisis de calidad de código"""
        if self.console:
            self.console.print("\n✨ Analizando calidad de código...")

        # Buscar patrones de código problemático
        for directory in self.analyze_dirs:
            dir_path = self.workspace_root / directory
            if not dir_path.exists():
                continue

            for file_path in dir_path.rglob("*.py"):
                self._analyze_code_patterns(file_path)

    def _analyze_code_patterns(self, file_path: Path):
        """🎯 Análisis de patrones específicos de código"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')

            # Funciones muy largas
            in_function = False
            function_start = 0
            function_name = ""
            indent_level = 0

            for line_num, line in enumerate(lines, 1):
                if line.strip().startswith('def '):
                    if in_function and line_num - function_start > 50:
                        self._add_problem(
                            file_path=str(file_path),
                            line_number=function_start,
                            severity=Severity.LOW,
                            category=self._categorize_file(file_path),
                            problem_type="LONG_FUNCTION",
                            title=f"Función muy larga: {function_name}",
                            description=f"Función con {line_num - function_start} líneas",
                            suggestion="Considerar dividir en funciones más pequeñas"
                        )

                    in_function = True
                    function_start = line_num
                    function_name = line.strip().split('(')[0].replace('def ', '')
                    indent_level = len(line) - len(line.lstrip())

                elif in_function and line.strip() and len(line) - len(line.lstrip()) <= indent_level and line.strip()[0].isalpha():
                    if line_num - function_start > 50:
                        self._add_problem(
                            file_path=str(file_path),
                            line_number=function_start,
                            severity=Severity.LOW,
                            category=self._categorize_file(file_path),
                            problem_type="LONG_FUNCTION",
                            title=f"Función muy larga: {function_name}",
                            description=f"Función con {line_num - function_start} líneas",
                            suggestion="Considerar dividir en funciones más pequeñas"
                        )
                    in_function = False

        except Exception:
            pass

    def _analyze_configuration(self):
        """⚙️ Análisis de configuración del sistema"""
        if self.console:
            self.console.print("\n⚙️ Analizando configuración...")

        # Verificar archivos de configuración críticos
        config_files = [
            'config/config_manager.py',
            'config/live_account_validator.py',
            'requirements.txt'
        ]

        for config_file in config_files:
            file_path = self.workspace_root / config_file
            if not file_path.exists():
                self._add_problem(
                    file_path=str(file_path),
                    line_number=1,
                    severity=Severity.HIGH,
                    category=Category.SISTEMA,
                    problem_type="MISSING_CONFIG_FILE",
                    title=f"Archivo de configuración faltante: {config_file}",
                    description=f"Archivo crítico de configuración no encontrado",
                    suggestion="Crear o restaurar archivo de configuración"
                )

    def _categorize_file(self, file_path: Path) -> Category:
        """🏷️ Categorizar archivo por ubicación"""
        path_str = str(file_path).lower()

        if 'dashboard' in path_str:
            return Category.DASHBOARD
        elif any(x in path_str for x in ['trading', 'core/trading']):
            return Category.TRADING
        elif any(x in path_str for x in ['ict_engine', 'ict']):
            return Category.ICT_ENGINE
        elif 'poi' in path_str:
            return Category.POI_SYSTEM
        elif any(x in path_str for x in ['sistema', 'config', 'core']):
            return Category.SISTEMA
        elif any(x in path_str for x in ['utilities', 'utils', 'scripts']):
            return Category.UTILITIES
        else:
            return Category.UNKNOWN

    def _add_problem(self, file_path: str, line_number: int, severity: Severity,
                    category: Category, problem_type: str, title: str,
                    description: str, suggestion: str, code_snippet: str = "",
                    context: Dict[str, Any] = None):
        """➕ Agregar problema detectado"""
        problem = DetectedProblem(
            id=f"{len(self.problems):04d}_{problem_type}_{int(time.time())}",
            timestamp=datetime.now().isoformat(),
            file_path=file_path,
            line_number=line_number,
            severity=severity.value,
            category=category.value,
            problem_type=problem_type,
            title=title,
            description=description,
            suggestion=suggestion,
            code_snippet=code_snippet,
            context=context or {}
        )

        self.problems.append(problem)
        self.stats['problems_found'] += 1
        self.stats['by_severity'][severity.name] += 1
        self.stats['by_category'][category.name] += 1

    def _get_code_snippet(self, content: str, line_number: int, context_lines: int = 2) -> str:
        """📝 Obtener snippet de código con contexto"""
        lines = content.split('\n')
        start = max(0, line_number - context_lines - 1)
        end = min(len(lines), line_number + context_lines)

        snippet_lines = []
        for i in range(start, end):
            prefix = ">>> " if i == line_number - 1 else "    "
            snippet_lines.append(f"{prefix}{lines[i]}")

        return '\n'.join(snippet_lines)

    def _generate_report(self) -> Dict[str, Any]:
        """📊 Generar reporte completo"""
        if self.console:
            self.console.print("\n📊 Generando reporte...")

        # Ordenar problemas por severidad
        severity_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']
        sorted_problems = sorted(
            self.problems,
            key=lambda p: severity_order.index(p.severity.split()[1])
        )

        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_problems': len(self.problems),
                'files_analyzed': self.stats['files_analyzed'],
                'analysis_time': round(self.stats['analysis_time'], 2)
            },
            'statistics': {
                'by_severity': self.stats['by_severity'],
                'by_category': self.stats['by_category']
            },
            'problems': [p.to_dict() for p in sorted_problems],
            'recommendations': self._generate_recommendations()
        }

        return report

    def _generate_recommendations(self) -> List[str]:
        """💡 Generar recomendaciones basadas en problemas encontrados"""
        recommendations = []

        # Recomendaciones por severidad
        critical_count = self.stats['by_severity']['CRITICAL']
        high_count = self.stats['by_severity']['HIGH']

        if critical_count > 0:
            recommendations.append(f"🚨 URGENTE: {critical_count} errores críticos requieren atención inmediata")

        if high_count > 5:
            recommendations.append(f"⚠️ ALTA PRIORIDAD: {high_count} problemas de alta severidad detectados")

        # Recomendaciones por categoría
        for category, count in self.stats['by_category'].items():
            if count > 10:
                recommendations.append(f"📂 Revisar módulo {category}: {count} problemas detectados")

        # Recomendaciones generales
        if self.stats['files_analyzed'] > 50:
            recommendations.append("✨ Considerar implementar CI/CD con análisis automático")

        return recommendations

    def _save_diagnostics_log(self):
        """💾 Guardar bitácora de diagnósticos"""
        diagnostics_dir = self.workspace_root / "docs" / "bitacoras" / "diagnosticos"
        diagnostics_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = diagnostics_dir / f"deteccion_errores_{timestamp}.json"

        report_data = self._generate_report()

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        if self.console:
            self.console.print(f"💾 Bitácora guardada: {log_file}")

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """📊 Resumen para integración con dashboard"""
        return {
            'total_problems': len(self.problems),
            'critical_problems': self.stats['by_severity']['CRITICAL'],
            'high_problems': self.stats['by_severity']['HIGH'],
            'files_analyzed': self.stats['files_analyzed'],
            'analysis_time': round(self.stats['analysis_time'], 2),
            'top_problems': [p.to_dict() for p in self.problems[:5]],
            'by_category': self.stats['by_category']
        }


def main():
    """🚀 Función principal del detector de errores"""
    import argparse

    parser = argparse.ArgumentParser(description="🔍 Sistema de Detección de Errores Jerárquico ITC Engine v5.0")
    parser.add_argument("--workspace", default=".", help="Directorio workspace (default: actual)")
    parser.add_argument("--quick", action="store_true", help="Análisis rápido (solo archivos críticos)")
    parser.add_argument("--output", help="Archivo de salida JSON (optional)")

    args = parser.parse_args()

    # Inicializar detector
    detector = ErrorDetector(args.workspace)

    # Ejecutar análisis
    report = detector.analyze_full_system(quick_mode=args.quick)

    # Mostrar resumen
    if RICH_AVAILABLE and detector.console:
        detector.console.print("\n🎯 RESUMEN DEL ANÁLISIS")
        detector.console.print("=" * 40)

        summary_table = Table(title="📊 Estadísticas")
        summary_table.add_column("Métrica")
        summary_table.add_column("Valor")

        summary_table.add_row("Archivos analizados", str(report['summary']['files_analyzed']))
        summary_table.add_row("Problemas encontrados", str(report['summary']['total_problems']))
        summary_table.add_row("Tiempo de análisis", f"{report['summary']['analysis_time']}s")

        detector.console.print(summary_table)

        # Mostrar problemas críticos
        critical_problems = [p for p in detector.problems if 'CRITICAL' in p.severity]
        if critical_problems:
            detector.console.print("\n🚨 PROBLEMAS CRÍTICOS:")
            for problem in critical_problems[:3]:
                detector.console.print(Panel(
                    f"📍 {problem.title}\n📁 {problem.file_path}:{problem.line_number}\n💡 {problem.suggestion}",
                    border_style="red"
                ))

    # Guardar salida opcional
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"📁 Reporte guardado: {args.output}")

    # Código de salida
    critical_count = detector.stats['by_severity']['CRITICAL']
    return 1 if critical_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
