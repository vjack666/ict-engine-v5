#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
=============================================================================
VERIFICADOR DE DEPENDENCIAS ANTES DE LIMPIEZA - ICT ENGINE v5.0
=============================================================================

Script de seguridad que verifica dependencias antes de eliminar archivos.
Analiza imports, referencias y uso de archivos candidatos para eliminación.
"""

import os
import re
import ast
from pathlib import Path
from typing import List, Dict, Set, Any
from collections import defaultdict

class DependencyVerifier:
    """
    Verificador de dependencias para archivos candidatos a eliminación
    """

    def __init__(self):
        self.base_path = Path(r"c:\Users\v_jac\Desktop\itc engine v5.0")
        self.python_files = []
        self.dependencies = defaultdict(set)
        self.reverse_dependencies = defaultdict(set)

        # Archivos candidatos para eliminación de cada categoría
        self.candidates = {
            'fix_scripts': [
                'debugging/tct_instant_fix.py',
                'debugging/tct_live_hotfix.py',
                'debugging/tct_quick_fix.py',
                'scripts/fix_escaped_quotes.py',
                'scripts/fix_jsondecode_critical.py',
                'scripts/fix_jsondecode_error.py',
                'scripts/fix_log_encoding.py',
                'scripts/fix_tct_logging_params.py'
            ],
            'backup_files': [
                'core/analysis_command_center/acc_data_models.py.bak',
                'core/analysis_command_center/acc_flow_controller.py.bak',
                'core/analysis_command_center/acc_orchestrator.py.bak',
                'core/trading.py.bak',
                'scripts/master_sluc_v21_updater.py.bak'
            ],
            'test_files': [
                'debugging/test_poi_integration.py',
                'debugging/test_tct_render.py',
                'tests/test_imports.py',
                'utilities/debug/test_imports.py'
            ],
            'duplicates': [
                'core/ict_engine/veredicto_engine_v4.py',
                'sistema/logging_interface_v21.py'
            ]
        }

    def scan_all_dependencies(self) -> Dict[str, Dict]:
        """Escanea todas las dependencias del proyecto"""
        print("🔍 Escaneando dependencias del proyecto...")

        # Obtener todos los archivos Python
        self._get_all_python_files()

        # Analizar imports en cada archivo
        for py_file in self.python_files:
            self._analyze_file_imports(py_file)

        # Verificar cada categoría de candidatos
        verification_results = {}

        for category, candidates in self.candidates.items():
            print(f"\\n📂 Verificando categoría: {category}")
            verification_results[category] = self._verify_category(candidates)

        return verification_results

    def _get_all_python_files(self):
        """Obtiene todos los archivos Python del proyecto"""
        exclude_dirs = {'__pycache__', '.git', '.vscode', 'venv', 'env'}

        for root, dirs, files in os.walk(self.base_path):
            # Filtrar directorios excluidos
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(self.base_path)
                    self.python_files.append(rel_path)

    def _analyze_file_imports(self, file_path: Path):
        """Analiza los imports de un archivo específico"""
        full_path = self.base_path / file_path

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Usar AST para análisis más preciso
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self._add_dependency(file_path, alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            self._add_dependency(file_path, node.module)
            except SyntaxError:
                # Si falla AST, usar regex como respaldo
                self._analyze_imports_regex(file_path, content)

        except Exception as e:
            print(f"❌ Error analizando {file_path}: {e}")

    def _analyze_imports_regex(self, file_path: Path, content: str):
        """Análisis de imports usando regex como respaldo"""
        import_patterns = [
            r'from\\s+(\\w+(?:\\.\\w+)*)\\s+import',
            r'import\\s+(\\w+(?:\\.\\w+)*)',
        ]

        for pattern in import_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                module_name = match.group(1)
                self._add_dependency(file_path, module_name)

    def _add_dependency(self, file_path: Path, module_name: str):
        """Añade una dependencia al mapeo"""
        # Convertir nombre de módulo a posible archivo
        possible_files = self._module_to_file_paths(module_name)

        for possible_file in possible_files:
            if possible_file in [str(pf) for pf in self.python_files]:
                self.dependencies[str(file_path)].add(possible_file)
                self.reverse_dependencies[possible_file].add(str(file_path))

    def _module_to_file_paths(self, module_name: str) -> List[str]:
        """Convierte nombre de módulo a posibles rutas de archivo"""
        paths = []

        # Reemplazar puntos con barras
        path_parts = module_name.split('.')

        # Posibles ubicaciones
        possible_paths = [
            '/'.join(path_parts) + '.py',
            '/'.join(path_parts) + '/__init__.py',
            'core/' + '/'.join(path_parts) + '.py',
            'sistema/' + '/'.join(path_parts) + '.py',
            'utilities/' + '/'.join(path_parts) + '.py',
        ]

        return possible_paths

    def _verify_category(self, candidates: List[str]) -> Dict[str, Any]:
        """Verifica una categoría específica de candidatos"""
        results = {
            'safe_to_delete': [],
            'has_dependencies': [],
            'not_found': [],
            'analysis': {}
        }

        for candidate in candidates:
            candidate_path = str(Path(candidate).as_posix())

            # Verificar si el archivo existe
            if not (self.base_path / candidate).exists():
                results['not_found'].append(candidate)
                continue

            # Verificar dependencias
            dependencies = self.reverse_dependencies.get(candidate_path, set())

            if dependencies:
                results['has_dependencies'].append(candidate)
                results['analysis'][candidate] = {
                    'used_by': list(dependencies),
                    'dependency_count': len(dependencies),
                    'risk_level': 'HIGH' if len(dependencies) > 3 else 'MEDIUM'
                }
                print(f"⚠️ {candidate}: usado por {len(dependencies)} archivos")
            else:
                results['safe_to_delete'].append(candidate)
                results['analysis'][candidate] = {
                    'used_by': [],
                    'dependency_count': 0,
                    'risk_level': 'SAFE'
                }
                print(f"✅ {candidate}: seguro para eliminar")

        return results

    def verify_duplicates(self) -> Dict[str, Any]:
        """Verificación especial para archivos duplicados"""
        print("\\n🔍 Verificación especial de duplicados...")

        duplicate_analysis = {}

        # Verificar veredicto_engine_v4.py vs veredicto_engine.py
        v4_path = self.base_path / 'core/ict_engine/veredicto_engine_v4.py'
        original_path = self.base_path / 'core/ict_engine/veredicto_engine.py'

        if v4_path.exists() and original_path.exists():
            v4_content = v4_path.read_text(encoding='utf-8')
            original_content = original_path.read_text(encoding='utf-8')

            duplicate_analysis['veredicto_engine_v4.py'] = {
                'has_original': True,
                'content_identical': v4_content == original_content,
                'size_v4': len(v4_content),
                'size_original': len(original_content),
                'recommendation': 'COMPARE_MANUALLY' if v4_content != original_content else 'SAFE_TO_DELETE'
            }

        # Verificar logging_interface_v21.py vs logging_interface.py
        v21_path = self.base_path / 'sistema/logging_interface_v21.py'
        current_path = self.base_path / 'sistema/logging_interface.py'

        if v21_path.exists() and current_path.exists():
            v21_content = v21_path.read_text(encoding='utf-8')
            current_content = current_path.read_text(encoding='utf-8')

            duplicate_analysis['logging_interface_v21.py'] = {
                'has_original': True,
                'content_identical': v21_content == current_content,
                'size_v21': len(v21_content),
                'size_current': len(current_content),
                'recommendation': 'COMPARE_MANUALLY' if v21_content != current_content else 'SAFE_TO_DELETE'
            }

        return duplicate_analysis

    def generate_safety_report(self, verification_results: Dict, duplicate_analysis: Dict) -> str:
        """Genera reporte de seguridad para limpieza"""

        report = []
        report.append("# 🛡️ REPORTE DE SEGURIDAD - VERIFICACIÓN DE DEPENDENCIAS")
        report.append("")
        report.append(f"**Fecha:** {self._get_current_date()}")
        report.append("**Propósito:** Verificar seguridad antes de eliminación de archivos")
        report.append("**Estado:** ✅ VERIFICACIÓN COMPLETADA")
        report.append("")
        report.append("---")
        report.append("")

        # Resumen de seguridad por categoría
        total_safe = 0
        total_risky = 0

        for category, results in verification_results.items():
            safe_count = len(results['safe_to_delete'])
            risky_count = len(results['has_dependencies'])
            total_safe += safe_count
            total_risky += risky_count

            report.append(f"## 📂 {category.replace('_', ' ').title()}")
            report.append("")
            report.append(f"**Seguros para eliminar:** {safe_count}")
            report.append(f"**Con dependencias:** {risky_count}")
            report.append("")

            if results['safe_to_delete']:
                report.append("### ✅ SEGUROS PARA ELIMINAR:")
                report.append("```")
                for file in results['safe_to_delete']:
                    report.append(f"✅ {file}")
                report.append("```")
                report.append("")

            if results['has_dependencies']:
                report.append("### ⚠️ CON DEPENDENCIAS (NO ELIMINAR):")
                report.append("```")
                for file in results['has_dependencies']:
                    analysis = results['analysis'][file]
                    report.append(f"⚠️ {file} - Usado por {analysis['dependency_count']} archivos")
                    for user in analysis['used_by'][:3]:  # Mostrar solo los primeros 3
                        report.append(f"   └── {user}")
                    if len(analysis['used_by']) > 3:
                        report.append(f"   └── ... y {len(analysis['used_by']) - 3} más")
                report.append("```")
                report.append("")

        # Análisis de duplicados
        report.append("## 🔄 ANÁLISIS DE DUPLICADOS")
        report.append("")

        for file, analysis in duplicate_analysis.items():
            report.append(f"### 📄 {file}")
            report.append(f"**Recomendación:** {analysis['recommendation']}")
            report.append(f"**Contenido idéntico:** {'✅ Sí' if analysis['content_identical'] else '❌ No'}")
            report.append("")

        # Resumen final
        report.append("---")
        report.append("")
        report.append("## 📊 RESUMEN DE SEGURIDAD")
        report.append("")
        report.append(f"**Total archivos verificados:** {total_safe + total_risky}")
        report.append(f"**✅ Seguros para eliminar:** {total_safe}")
        report.append(f"**⚠️ Con dependencias (mantener):** {total_risky}")
        report.append("")

        if total_risky == 0:
            report.append("🎯 **ESTADO:** ✅ Todos los archivos son seguros para eliminar")
        else:
            report.append("🎯 **ESTADO:** ⚠️ Algunos archivos tienen dependencias - revisar antes de eliminar")

        report.append("")
        report.append("---")
        report.append("**Generado por:** DependencyVerifier v1.0")
        report.append("**ICT Engine v5.0** - Verificación de Seguridad")

        return "\\n".join(report)

    def _get_current_date(self) -> str:
        """Obtiene fecha actual"""
        from datetime import datetime
        return datetime.now().strftime("%d de %B de %Y")

def main():
    """Función principal"""
    print("🛡️ VERIFICADOR DE DEPENDENCIAS - ICT ENGINE v5.0")
    print("=" * 60)

    verifier = DependencyVerifier()

    # Verificar dependencias
    verification_results = verifier.scan_all_dependencies()

    # Verificar duplicados
    duplicate_analysis = verifier.verify_duplicates()

    # Generar reporte
    report = verifier.generate_safety_report(verification_results, duplicate_analysis)

    # Guardar reporte
    report_path = Path("docs/bitacoras/reportes/REPORTE_SEGURIDAD_DEPENDENCIAS.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\\n📄 Reporte de seguridad generado: {report_path}")
    print("✅ Verificación de dependencias completada")

if __name__ == "__main__":
    main()
