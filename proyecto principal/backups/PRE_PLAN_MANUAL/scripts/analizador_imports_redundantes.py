"""
🔍 ANALIZADOR DE IMPORTS REDUNDANTES - ITC ENGINE v5.0
===============================================

Objetivo: Detectar y mapear imports redundantes, duplicados y conflictivos
para consolidar todo en SIC v3.0

Autor: Sistema de Análisis Automático
Fecha: 06 Agosto 2025
"""

import os
import re
import ast
import json
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple
import sys

# Configuración de paths
BASE_PATH = Path(__file__).parent.parent
SISTEMA_PATH = BASE_PATH / "sistema"
DASHBOARD_PATH = BASE_PATH / "dashboard"

class ImportAnalyzer:
    def __init__(self):
        self.redundant_imports = defaultdict(list)
        self.circular_dependencies = []
        self.direct_imports = defaultdict(list)
        self.sic_imports = defaultdict(list)
        self.reimports = defaultdict(list)
        self.missing_in_sic = set()
        self.all_imports = defaultdict(set)

    def analyze_file(self, file_path: Path) -> Dict:
        """Analiza un archivo Python para extraer información de imports"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)
            file_data = {
                'path': str(file_path),
                'imports': [],
                'from_imports': [],
                'sic_imports': [],
                'direct_imports': [],
                'reimports': []
            }

            # Extraer imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        import_info = {
                            'type': 'import',
                            'module': alias.name,
                            'name': alias.asname or alias.name,
                            'line': node.lineno
                        }
                        file_data['imports'].append(import_info)
                        self.all_imports[str(file_path)].add(alias.name)

                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        import_info = {
                            'type': 'from_import',
                            'module': module,
                            'name': alias.name,
                            'alias': alias.asname,
                            'line': node.lineno
                        }
                        file_data['from_imports'].append(import_info)

                        # Clasificar imports
                        full_import = f"{module}.{alias.name}" if module else alias.name
                        self.all_imports[str(file_path)].add(full_import)

                        if module == 'sistema.sic':
                            file_data['sic_imports'].append(import_info)
                            self.sic_imports[str(file_path)].append(import_info)
                        else:
                            file_data['direct_imports'].append(import_info)
                            self.direct_imports[str(file_path)].append(import_info)

            return file_data

        except Exception as e:
            print(f"❌ Error analizando {file_path}: {e}")
            return None

    def detect_redundancies(self):
        """Detecta imports redundantes y duplicados"""
        print("\n🔍 DETECTANDO REDUNDANCIAS...")

        # Buscar imports duplicados en el mismo archivo
        for file_path, imports in self.all_imports.items():
            import_counts = Counter()

            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for i, line in enumerate(lines, 1):
                # Buscar imports de enviar_senal_log específicamente
                if 'enviar_senal_log' in line and ('import' in line or 'from' in line):
                    self.reimports[file_path].append({
                        'line': i,
                        'content': line.strip(),
                        'type': 'enviar_senal_log_duplicate'
                    })

                # Detectar otros patterns de duplicación
                if 'from sistema.sic import' in line and 'from sistema.logging_interface import' in line:
                    self.reimports[file_path].append({
                        'line': i,
                        'content': line.strip(),
                        'type': 'cross_system_duplicate'
                    })

    def find_missing_in_sic(self):
        """Encuentra imports que no están disponibles en SIC v3.0"""
        print("\n🔍 BUSCANDO IMPORTS FALTANTES EN SIC...")

        # Leer exports actuales de SIC
        sic_path = SISTEMA_PATH / "sic.py"
        sic_exports = set()

        try:
            with open(sic_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extraer __all__
            all_match = re.search(r'__all__\s*=\s*\[(.*?)\]', content, re.DOTALL)
            if all_match:
                exports_text = all_match.group(1)
                exports = re.findall(r"'([^']+)'", exports_text)
                sic_exports.update(exports)

        except Exception as e:
            print(f"❌ Error leyendo SIC: {e}")

        # Comparar con imports requeridos
        for file_path, direct_imports in self.direct_imports.items():
            for import_info in direct_imports:
                imported_name = import_info['name']
                if imported_name not in sic_exports:
                    self.missing_in_sic.add(imported_name)

        print(f"📊 Encontrados {len(self.missing_in_sic)} imports faltantes en SIC")

    def generate_report(self) -> str:
        """Genera un reporte completo del análisis"""
        report = [
            "🔍 REPORTE DE ANÁLISIS DE IMPORTS REDUNDANTES",
            "=" * 50,
            f"Fecha: {Path.cwd()}",
            ""
        ]

        # Resumen ejecutivo
        report.extend([
            "📊 RESUMEN EJECUTIVO",
            "-" * 20,
            f"• Archivos analizados: {len(self.all_imports)}",
            f"• Reimports detectados: {sum(len(v) for v in self.reimports.values())}",
            f"• Imports directos (no SIC): {sum(len(v) for v in self.direct_imports.values())}",
            f"• Imports faltantes en SIC: {len(self.missing_in_sic)}",
            ""
        ])

        # Detalles de reimports críticos
        if self.reimports:
            report.extend([
                "🔥 REIMPORTS CRÍTICOS DETECTADOS",
                "-" * 30
            ])

            for file_path, reimports in self.reimports.items():
                if reimports:
                    report.append(f"\n📁 {file_path}")
                    for reimport in reimports:
                        report.append(f"   Línea {reimport['line']}: {reimport['content']}")
                        report.append(f"   Tipo: {reimport['type']}")

        # Imports faltantes en SIC
        if self.missing_in_sic:
            report.extend([
                "",
                "❌ IMPORTS FALTANTES EN SIC v3.0",
                "-" * 30
            ])
            for missing in sorted(self.missing_in_sic):
                report.append(f"• {missing}")

        # Estadísticas por archivo
        report.extend([
            "",
            "📈 ESTADÍSTICAS POR ARCHIVO",
            "-" * 25
        ])

        for file_path in sorted(self.all_imports.keys()):
            sic_count = len(self.sic_imports.get(file_path, []))
            direct_count = len(self.direct_imports.get(file_path, []))

            status = "✅ LIMPIO" if direct_count == 0 else "❌ NECESITA LIMPIEZA"
            report.append(f"{status} {Path(file_path).name}: SIC({sic_count}) | Directos({direct_count})")

        # Recomendaciones
        report.extend([
            "",
            "💡 RECOMENDACIONES PRIORITARIAS",
            "-" * 30,
            "1. 🔥 ELIMINAR reimports de enviar_senal_log",
            "2. 📦 AGREGAR exports faltantes a SIC v3.0:",
        ])

        for missing in sorted(list(self.missing_in_sic)[:10]):  # Top 10
            report.append(f"   • {missing}")

        if len(self.missing_in_sic) > 10:
            report.append(f"   ... y {len(self.missing_in_sic) - 10} más")

        report.extend([
            "",
            "3. 🧹 CONVERTIR todos los imports directos a SIC",
            "4. ✅ VALIDAR que no hay dependencias circulares",
            ""
        ])

        return "\n".join(report)

    def save_detailed_data(self):
        """Guarda datos detallados para análisis posterior"""
        data = {
            'missing_in_sic': list(self.missing_in_sic),
            'reimports_by_file': dict(self.reimports),
            'direct_imports_by_file': dict(self.direct_imports),
            'sic_imports_by_file': dict(self.sic_imports),
            'summary': {
                'total_files': len(self.all_imports),
                'files_with_reimports': len([f for f in self.reimports.values() if f]),
                'files_with_direct_imports': len([f for f in self.direct_imports.values() if f]),
                'total_missing_exports': len(self.missing_in_sic)
            }
        }

        output_path = BASE_PATH / "data" / "exports" / "imports_analysis.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"📄 Datos detallados guardados en: {output_path}")

def main():
    print("🚀 INICIANDO ANÁLISIS DE IMPORTS REDUNDANTES")
    print("=" * 50)

    analyzer = ImportAnalyzer()

    # Archivos a analizar (prioridad alta)
    priority_files = [
        DASHBOARD_PATH / "dashboard_definitivo.py",
        SISTEMA_PATH / "sic.py",
        SISTEMA_PATH / "logging_interface.py"
    ]

    # Analizar archivos prioritarios
    print("\n🎯 ANALIZANDO ARCHIVOS PRIORITARIOS...")
    for file_path in priority_files:
        if file_path.exists():
            print(f"   📁 {file_path.name}")
            analyzer.analyze_file(file_path)
        else:
            print(f"   ❌ No encontrado: {file_path}")

    # Analizar todo el directorio dashboard
    print("\n📁 ANALIZANDO DIRECTORIO DASHBOARD...")
    for py_file in DASHBOARD_PATH.glob("*.py"):
        if py_file.name != "__init__.py":
            analyzer.analyze_file(py_file)

    # Analizar todo el directorio sistema
    print("\n📁 ANALIZANDO DIRECTORIO SISTEMA...")
    for py_file in SISTEMA_PATH.glob("*.py"):
        if py_file.name != "__init__.py":
            analyzer.analyze_file(py_file)

    # Detectar problemas
    analyzer.detect_redundancies()
    analyzer.find_missing_in_sic()

    # Generar reporte
    print("\n📊 GENERANDO REPORTE...")
    report = analyzer.generate_report()

    # Guardar reporte
    report_path = BASE_PATH / "data" / "exports" / "reporte_imports_redundantes.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    # Guardar datos detallados
    analyzer.save_detailed_data()

    # Mostrar reporte en consola
    print("\n" + report)

    print(f"\n📄 Reporte completo guardado en: {report_path}")
    print("🏁 ANÁLISIS COMPLETADO")

if __name__ == "__main__":
    main()
