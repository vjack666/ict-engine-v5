"""
🧠 VALIDACIÓN INTELIGENTE PRE-EJECUCIÓN - ITC ENGINE v5.0
========================================================

Sistema de análisis profundo de dependencias y validación de scripts
antes de ejecutar el plan de corrección.

Autor: Sistema de Análisis Automático
Fecha: 06 Agosto 2025
"""

import os
import ast
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, deque
from dataclasses import dataclass, asdict

# Agregar el directorio padre al path para imports
current_dir = Path(__file__).parent
project_root = current_dir.parent
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
class DependencyNode:
    file_path: str
    imports: List[str]
    exports: List[str]
    dependencies: List[str]
    dependents: List[str]
    level: int
    priority_score: int

@dataclass
class CircularDependency:
    cycle: List[str]
    severity: str
    impact_files: int

@dataclass
class ValidationResult:
    dependency_graph: Dict[str, DependencyNode]
    circular_dependencies: List[CircularDependency]
    priority_order: List[str]
    orphaned_files: List[str]
    script_validations: Dict[str, bool]
    recommendations: List[str]

class IntelligentValidator:
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.dependency_graph = {}
        self.circular_deps = []
        self.analysis_results = None

        # Directorios críticos a analizar
        self.critical_dirs = [
            "sistema", "dashboard", "core", "utils",
            "config", "scripts"
        ]

        # Scripts automatizados a validar
        self.automation_scripts = [
            "scripts/activate_import_fixer.py",
            "scripts/migrador_masivo_paquetes.py",
            "scripts/create_intelligent_backup.py",
            "scripts/live_progress_monitor.py"
        ]

    def run_full_analysis(self) -> ValidationResult:
        """Ejecutar análisis completo del proyecto"""
        enviar_senal_log("INFO", "🧠 Iniciando análisis inteligente pre-ejecución", __name__, "validator")

        # Paso 1: Construir grafo de dependencias
        self._build_dependency_graph()

        # Paso 2: Detectar dependencias circulares
        self._detect_circular_dependencies()

        # Paso 3: Calcular prioridades
        self._calculate_priority_scores()

        # Paso 4: Generar orden óptimo
        priority_order = self._generate_optimal_order()

        # Paso 5: Encontrar archivos huérfanos
        orphaned_files = self._find_orphaned_files()

        # Paso 6: Validar scripts automatizados
        script_validations = self._validate_automation_scripts()

        # Paso 7: Generar recomendaciones
        recommendations = self._generate_recommendations()

        self.analysis_results = ValidationResult(
            dependency_graph=self.dependency_graph,
            circular_dependencies=self.circular_deps,
            priority_order=priority_order,
            orphaned_files=orphaned_files,
            script_validations=script_validations,
            recommendations=recommendations
        )

        return self.analysis_results

    def _build_dependency_graph(self):
        """Construir grafo completo de dependencias"""
        enviar_senal_log("INFO", "📊 Construyendo grafo de dependencias", __name__, "validator")

        # Escanear todos los archivos Python
        all_files = []
        for dir_name in self.critical_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                all_files.extend(dir_path.rglob("*.py"))

        # Analizar cada archivo
        for file_path in all_files:
            try:
                rel_path = str(file_path.relative_to(self.project_root))
                imports, exports = self._analyze_file_dependencies(file_path)

                self.dependency_graph[rel_path] = DependencyNode(
                    file_path=rel_path,
                    imports=imports,
                    exports=exports,
                    dependencies=[],  # Se calculará después
                    dependents=[],    # Se calculará después
                    level=0,          # Se calculará después
                    priority_score=0  # Se calculará después
                )
            except Exception as e:
                enviar_senal_log("WARNING", f"Error analizando {file_path}: {e}", __name__, "validator")

        # Resolver dependencias entre archivos
        self._resolve_inter_file_dependencies()

        # Calcular niveles de dependencia
        self._calculate_dependency_levels()

    def _analyze_file_dependencies(self, file_path: Path) -> Tuple[List[str], List[str]]:
        """Analizar imports y exports de un archivo"""
        imports = []
        exports = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            # Extraer imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
                        for alias in node.names:
                            imports.append(f"{node.module}.{alias.name}")

            # Extraer exports (funciones, clases definidas)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    exports.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    exports.append(node.name)
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            exports.append(target.id)

            # Buscar __all__ para exports explícitos
            all_match = ast.literal_eval(content) if '__all__' in content else None
            if all_match and isinstance(all_match, list):
                exports.extend(all_match)

        except Exception as e:
            enviar_senal_log("DEBUG", f"Error parsing {file_path}: {e}", __name__, "validator")

        return imports, exports

    def _resolve_inter_file_dependencies(self):
        """Resolver dependencias entre archivos del proyecto"""
        for file_path, node in self.dependency_graph.items():
            dependencies = []

            for import_name in node.imports:
                # Buscar si el import corresponde a algún archivo del proyecto
                for other_file, other_node in self.dependency_graph.items():
                    if other_file == file_path:
                        continue

                    # Verificar si el import coincide con el path o exports del otro archivo
                    if self._is_dependency(import_name, other_file, other_node):
                        dependencies.append(other_file)
                        other_node.dependents.append(file_path)

            node.dependencies = list(set(dependencies))  # Eliminar duplicados

    def _is_dependency(self, import_name: str, target_file: str, target_node: DependencyNode) -> bool:
        """Verificar si un import corresponde a un archivo específico"""
        # Convertir path a módulo (e.g., 'sistema/sic.py' -> 'sistema.sic')
        module_name = target_file.replace('/', '.').replace('\\', '.').replace('.py', '')

        # Verificar coincidencias
        if import_name.startswith(module_name):
            return True

        # Verificar si el import está en los exports del archivo
        for export in target_node.exports:
            if import_name.endswith(export):
                return True

        return False

    def _calculate_dependency_levels(self):
        """Calcular niveles de dependencia usando BFS"""
        # Encontrar nodos raíz (sin dependencias)
        root_nodes = [path for path, node in self.dependency_graph.items()
                     if not node.dependencies]

        # BFS para asignar niveles
        queue = deque([(path, 0) for path in root_nodes])
        visited = set()

        while queue:
            current_path, level = queue.popleft()

            if current_path in visited:
                continue

            visited.add(current_path)
            self.dependency_graph[current_path].level = level

            # Agregar dependientes al siguiente nivel
            for dependent in self.dependency_graph[current_path].dependents:
                if dependent not in visited:
                    queue.append((dependent, level + 1))

    def _detect_circular_dependencies(self):
        """Detectar dependencias circulares usando DFS"""
        enviar_senal_log("INFO", "🔍 Detectando dependencias circulares", __name__, "validator")

        visited = set()
        rec_stack = set()
        self.circular_deps = []

        def dfs(node_path: str, path: List[str]) -> bool:
            if node_path in rec_stack:
                # Encontramos un ciclo
                cycle_start = path.index(node_path)
                cycle = path[cycle_start:] + [node_path]

                severity = "HIGH" if len(cycle) <= 3 else "MEDIUM"
                impact_files = len(cycle)

                circular_dep = CircularDependency(
                    cycle=cycle,
                    severity=severity,
                    impact_files=impact_files
                )
                self.circular_deps.append(circular_dep)
                return True

            if node_path in visited:
                return False

            visited.add(node_path)
            rec_stack.add(node_path)

            for dependency in self.dependency_graph[node_path].dependencies:
                if dfs(dependency, path + [node_path]):
                    return True

            rec_stack.remove(node_path)
            return False

        # Ejecutar DFS desde cada nodo
        for node_path in self.dependency_graph:
            if node_path not in visited:
                dfs(node_path, [])

    def _calculate_priority_scores(self):
        """Calcular score de prioridad para cada archivo"""
        enviar_senal_log("INFO", "📊 Calculando scores de prioridad", __name__, "validator")

        for file_path, node in self.dependency_graph.items():
            score = 0

            # Factor 1: Número de dependientes (archivos que dependen de este)
            score += len(node.dependents) * 5

            # Factor 2: Nivel en la jerarquía (niveles más bajos = mayor prioridad)
            score += max(0, 10 - node.level)

            # Factor 3: Criticidad del archivo
            if self._is_entry_point(file_path):
                score += 20
            if self._is_core_system(file_path):
                score += 15
            if self._is_frequently_modified(file_path):
                score += 10

            # Factor 4: Complejidad (número de imports/exports)
            complexity = len(node.imports) + len(node.exports)
            score += min(complexity // 5, 10)  # Máximo 10 puntos por complejidad

            # Factor 5: Penalización por dependencias circulares
            if any(file_path in cycle.cycle for cycle in self.circular_deps):
                score += 25  # Alta prioridad para resolver ciclos

            node.priority_score = score

    def _is_entry_point(self, file_path: str) -> bool:
        """Verificar si es un punto de entrada del sistema"""
        entry_points = [
            'main.py',
            'dashboard/dashboard_definitivo.py',
            'sistema/sic.py',
            'sistema/logging_interface.py'
        ]
        return any(file_path.endswith(ep) for ep in entry_points)

    def _is_core_system(self, file_path: str) -> bool:
        """Verificar si es parte del sistema core"""
        return file_path.startswith(('sistema/', 'core/', 'config/'))

    def _is_frequently_modified(self, file_path: str) -> bool:
        """Verificar si es modificado frecuentemente (heurística)"""
        # En un entorno real, esto usaría git history
        # Por ahora, asumimos que archivos del dashboard son frecuentemente modificados
        return file_path.startswith('dashboard/')

    def _generate_optimal_order(self) -> List[str]:
        """Generar orden óptimo de corrección basado en prioridades"""
        # Ordenar por score de prioridad (descendente)
        sorted_files = sorted(
            self.dependency_graph.items(),
            key=lambda x: x[1].priority_score,
            reverse=True
        )

        return [file_path for file_path, _ in sorted_files]

    def _find_orphaned_files(self) -> List[str]:
        """Encontrar archivos huérfanos (no importados por nadie)"""
        orphaned = []

        for file_path, node in self.dependency_graph.items():
            if not node.dependents and not self._is_entry_point(file_path):
                orphaned.append(file_path)

        return orphaned

    def _validate_automation_scripts(self) -> Dict[str, bool]:
        """Validar scripts automatizados antes de usar"""
        enviar_senal_log("INFO", "🧪 Validando scripts automatizados", __name__, "validator")

        validations = {}

        for script_path in self.automation_scripts:
            full_path = self.project_root / script_path

            if not full_path.exists():
                validations[script_path] = False
                continue

            try:
                # Verificar sintaxis
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                ast.parse(content)

                # Ejecutar dry-run si el script lo soporta
                result = subprocess.run([
                    sys.executable, str(full_path), '--dry-run'
                ], capture_output=True, text=True, timeout=30, cwd=self.project_root)

                validations[script_path] = result.returncode == 0

            except Exception as e:
                enviar_senal_log("WARNING", f"Error validando {script_path}: {e}", __name__, "validator")
                validations[script_path] = False

        return validations

    def _generate_recommendations(self) -> List[str]:
        """Generar recomendaciones basadas en el análisis"""
        recommendations = []

        # Recomendaciones por dependencias circulares
        if self.circular_deps:
            high_severity = [cd for cd in self.circular_deps if cd.severity == "HIGH"]
            if high_severity:
                recommendations.append(
                    f"🚨 CRÍTICO: Resolver {len(high_severity)} dependencias circulares de alta severidad"
                )

        # Recomendaciones por orden de prioridad
        top_priority = sorted(
            self.dependency_graph.items(),
            key=lambda x: x[1].priority_score,
            reverse=True
        )[:5]

        recommendations.append(
            f"🎯 INICIAR corrección con archivos de mayor prioridad: {', '.join([Path(fp).name for fp, _ in top_priority])}"
        )

        # Recomendaciones por archivos huérfanos
        orphaned = self._find_orphaned_files()
        if orphaned:
            recommendations.append(
                f"🧹 CONSIDERAR eliminar {len(orphaned)} archivos huérfanos para simplificar"
            )

        # Recomendaciones por scripts inválidos
        script_validations = self._validate_automation_scripts()
        invalid_scripts = [script for script, valid in script_validations.items() if not valid]
        if invalid_scripts:
            recommendations.append(
                f"🔧 REPARAR {len(invalid_scripts)} scripts automatizados antes de usar"
            )

        return recommendations

    def display_analysis_results(self):
        """Mostrar resultados del análisis en consola"""
        if not self.analysis_results:
            print("❌ No hay resultados de análisis disponibles")
            return

        results = self.analysis_results

        print("🧠 RESULTADOS DEL ANÁLISIS INTELIGENTE")
        print("=" * 50)

        # Resumen ejecutivo
        print(f"📊 RESUMEN:")
        print(f"├─ Archivos analizados: {len(results.dependency_graph)}")
        print(f"├─ Dependencias circulares: {len(results.circular_dependencies)}")
        print(f"├─ Archivos huérfanos: {len(results.orphaned_files)}")
        print(f"└─ Scripts válidos: {sum(results.script_validations.values())}/{len(results.script_validations)}")

        # Dependencias circulares críticas
        if results.circular_dependencies:
            print(f"\n🚨 DEPENDENCIAS CIRCULARES DETECTADAS:")
            for i, cycle in enumerate(results.circular_dependencies[:3], 1):
                cycle_str = " → ".join([Path(f).name for f in cycle.cycle])
                print(f"   {i}. {cycle.severity}: {cycle_str}")

        # Orden de prioridad (top 10)
        print(f"\n🎯 ORDEN ÓPTIMO DE CORRECCIÓN (Top 10):")
        for i, file_path in enumerate(results.priority_order[:10], 1):
            node = results.dependency_graph[file_path]
            file_name = Path(file_path).name
            print(f"   {i:2d}. {file_name:<30} (Score: {node.priority_score}, Nivel: {node.level})")

        # Recomendaciones
        print(f"\n💡 RECOMENDACIONES:")
        for i, rec in enumerate(results.recommendations, 1):
            print(f"   {i}. {rec}")

        # Guardar resultados completos
        output_path = self.project_root / "data" / "exports" / "dependency_analysis.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convertir a formato serializable
        serializable_data = {
            'dependency_graph': {k: asdict(v) for k, v in results.dependency_graph.items()},
            'circular_dependencies': [asdict(cd) for cd in results.circular_dependencies],
            'priority_order': results.priority_order,
            'orphaned_files': results.orphaned_files,
            'script_validations': results.script_validations,
            'recommendations': results.recommendations
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)

        print(f"\n📄 Análisis completo guardado en: {output_path}")

def main():
    """Función principal para ejecutar validación inteligente"""
    print("🧠 INICIANDO VALIDACIÓN INTELIGENTE PRE-EJECUCIÓN")
    print("=" * 55)

    project_root = Path.cwd()
    validator = IntelligentValidator(project_root)

    # Ejecutar análisis completo
    results = validator.run_full_analysis()

    # Mostrar resultados
    validator.display_analysis_results()

    print("\n🏁 VALIDACIÓN INTELIGENTE COMPLETADA")

if __name__ == "__main__":
    main()
