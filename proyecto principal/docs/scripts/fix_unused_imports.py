#!/usr/bin/env python3
"""
🔧 CORRECTOR AUTOMÁTICO DE IMPORTS NO UTILIZADOS
===============================================

Script para detectar y corregir automáticamente imports no utilizados en todo el proyecto.
Analiza archivos Python y elimina imports que no se usan en el código.

Características:
- Detección automática de imports no utilizados
- Corrección automática con backup
- Análisis completo del proyecto
- Reporte detallado de cambios
- Modo dry-run para vista previa

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
Versión: v1.0
"""

# MIGRACIÓN SIC v3.0 + SLUC v2.1
from sistema.sic import enviar_senal_log, log_info, log_warning

from sistema.sic import os
from sistema.sic import sys
import ast
from sistema.sic import re
from sistema.sic import Path
from sistema.sic import List, Dict, Set, Tuple, Optional
from sistema.sic import dataclass
from sistema.sic import datetime
import shutil
import argparse

@dataclass
class ImportInfo:
    """Información sobre un import"""
    line_number: int
    line_content: str
    import_name: str
    module_name: str
    is_used: bool = False
    import_type: str = "import"  # "import", "from_import", "from_import_as"

@dataclass
class FileAnalysis:
    """Análisis de un archivo Python"""
    file_path: str
    imports: List[ImportInfo]
    unused_imports: List[ImportInfo]
    content_lines: List[str]
    modified: bool = False

class UnusedImportDetector:
    """Detector de imports no utilizados"""

    def __init__(self, project_root: str, backup_dir: Optional[str] = None):
        self.project_root = Path(project_root)
        self.backup_dir = Path(backup_dir) if backup_dir else self.project_root / "backup_imports"
        self.analysis_results: List[FileAnalysis] = []

        # Patrones de imports a analizar
        self.import_patterns = [
            r'^import\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)',
            r'^from\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s+import\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*)*)',
            r'^from\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s+import\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+as\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        ]

        # Módulos que siempre se consideran utilizados (pueden ser imports implícitos)
        self.always_used_modules = {
            '__future__', 'typing_extensions', 'annotations'
        }

    def find_python_files(self) -> List[Path]:
        """Encuentra todos los archivos Python en el proyecto"""
        python_files = []

        # Directorios a excluir
        exclude_dirs = {
            '__pycache__', '.git', '.vscode', 'node_modules',
            'venv', 'env', '.env', 'backup_imports'
        }

        for root, dirs, files in os.walk(self.project_root):
            # Filtrar directorios excluidos
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    python_files.append(file_path)

        return python_files

    def extract_imports(self, file_path: Path) -> List[ImportInfo]:
        """Extrae todos los imports de un archivo"""
        imports = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for i, line in enumerate(lines, 1):
                line_stripped = line.strip()

                # Import simple: import module
                if line_stripped.startswith('import ') and ' as ' not in line_stripped:
                    match = re.match(r'^import\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)', line_stripped)
                    if match:
                        module_name = match.group(1)
                        import_name = module_name.split('.')[0]  # Solo el primer nivel
                        imports.append(ImportInfo(
                            line_number=i,
                            line_content=line.rstrip(),
                            import_name=import_name,
                            module_name=module_name,
                            import_type="import"
                        ))

                # From import: from module import item
                elif line_stripped.startswith('from ') and ' import ' in line_stripped:
                    if ' as ' in line_stripped:
                        # from module import item as alias
                        match = re.match(r'^from\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s+import\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+as\s+([a-zA-Z_][a-zA-Z0-9_]*)', line_stripped)
                        if match:
                            module_name = match.group(1)
                            original_name = match.group(2)
                            alias_name = match.group(3)
                            imports.append(ImportInfo(
                                line_number=i,
                                line_content=line.rstrip(),
                                import_name=alias_name,
                                module_name=module_name,
                                import_type="from_import_as"
                            ))
                    else:
                        # from module import item
                        match = re.match(r'^from\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s+import\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*)*)', line_stripped)
                        if match:
                            module_name = match.group(1)
                            import_items = match.group(2)

                            # Manejar múltiples imports
                            for item in import_items.split(','):
                                item = item.strip()
                                imports.append(ImportInfo(
                                    line_number=i,
                                    line_content=line.rstrip(),
                                    import_name=item,
                                    module_name=module_name,
                                    import_type="from_import"
                                ))

        except Exception as e:
            print(f"❌ Error leyendo {file_path}: {e}")

        return imports

    def check_import_usage(self, file_path: Path, imports: List[ImportInfo]) -> List[ImportInfo]:
        """Verifica qué imports se usan en el archivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Eliminar comentarios y strings para evitar falsos positivos
            lines = content.split('\n')
            code_lines = []

            for line in lines:
                # Eliminar comentarios
                if '#' in line:
                    line = line.split('#')[0]
                code_lines.append(line)

            code_content = '\n'.join(code_lines)

            for import_info in imports:
                # Verificar si el import se usa en el código
                import_name = import_info.import_name

                # Módulos que siempre se consideran usados
                if import_info.module_name in self.always_used_modules:
                    import_info.is_used = True
                    continue

                # Buscar uso del import en el código
                # Patrones de uso común
                usage_patterns = [
                    rf'\b{re.escape(import_name)}\.',  # module.function()
                    rf'\b{re.escape(import_name)}\[',  # module[key]
                    rf'\b{re.escape(import_name)}\(',  # function()
                    rf'\b{re.escape(import_name)}\s*=',  # assignment
                    rf'=\s*{re.escape(import_name)}\b',  # right side assignment
                    rf'\({re.escape(import_name)}\b',  # function parameter
                    rf',\s*{re.escape(import_name)}\b',  # list/tuple element
                    rf'\[{re.escape(import_name)}\b',  # list element
                    rf'return\s+{re.escape(import_name)}\b',  # return statement
                    rf'yield\s+{re.escape(import_name)}\b',  # yield statement
                    rf'isinstance\s*\([^,]*,\s*{re.escape(import_name)}\b',  # isinstance check
                ]

                # Buscar en todo el contenido del archivo excepto la línea del import
                file_lines = content.split('\n')
                search_content = '\n'.join(
                    line for i, line in enumerate(file_lines)
                    if i + 1 != import_info.line_number
                )

                for pattern in usage_patterns:
                    if re.search(pattern, search_content):
                        import_info.is_used = True
                        break

        except Exception as e:
            print(f"❌ Error analizando uso en {file_path}: {e}")
            # En caso de error, marcar como usado para evitar eliminación incorrecta
            for import_info in imports:
                import_info.is_used = True

        return imports

    def analyze_file(self, file_path: Path) -> FileAnalysis:
        """Analiza un archivo completo"""
        print(f"🔍 Analizando: {file_path.relative_to(self.project_root)}")

        # Extraer imports
        imports = self.extract_imports(file_path)

        # Verificar uso
        imports = self.check_import_usage(file_path, imports)

        # Identificar imports no utilizados
        unused_imports = [imp for imp in imports if not imp.is_used]

        # Leer contenido del archivo
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content_lines = f.readlines()
        except Exception:
            content_lines = []

        return FileAnalysis(
            file_path=str(file_path),
            imports=imports,
            unused_imports=unused_imports,
            content_lines=content_lines
        )

    def create_backup(self, file_path: Path) -> Path:
        """Crea backup de un archivo"""
        self.backup_dir.mkdir(exist_ok=True)

        # Mantener estructura de directorios en el backup
        relative_path = file_path.relative_to(self.project_root)
        backup_path = self.backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        # Agregar timestamp al backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_path.with_suffix(f'.{timestamp}.bak')

        shutil.copy2(file_path, backup_path)
        return backup_path

    def fix_file(self, analysis: FileAnalysis, dry_run: bool = False) -> bool:
        """Corrige un archivo eliminando imports no utilizados"""
        if not analysis.unused_imports:
            return False

        file_path = Path(analysis.file_path)

        if not dry_run:
            # Crear backup
            backup_path = self.create_backup(file_path)
            print(f"💾 Backup creado: {backup_path}")

        # Crear contenido corregido
        lines_to_remove = {imp.line_number for imp in analysis.unused_imports}
        corrected_lines = [
            line for i, line in enumerate(analysis.content_lines, 1)
            if i not in lines_to_remove
        ]

        if not dry_run:
            # Escribir archivo corregido
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(corrected_lines)
                analysis.modified = True
                return True
            except Exception as e:
                print(f"❌ Error escribiendo {file_path}: {e}")
                return False
        else:
            analysis.modified = True
            return True

    def run_analysis(self, fix_files: bool = False, dry_run: bool = False) -> None:
        """Ejecuta el análisis completo del proyecto"""
        print("🚀 INICIANDO ANÁLISIS DE IMPORTS NO UTILIZADOS")
        print("=" * 60)

        # Encontrar archivos Python
        python_files = self.find_python_files()
        print(f"📁 Archivos Python encontrados: {len(python_files)}")

        # Analizar cada archivo
        total_unused = 0
        files_with_issues = 0
        files_fixed = 0

        for file_path in python_files:
            analysis = self.analyze_file(file_path)
            self.analysis_results.append(analysis)

            if analysis.unused_imports:
                files_with_issues += 1
                total_unused += len(analysis.unused_imports)

                print(f"\n📄 {file_path.relative_to(self.project_root)}")
                print(f"   🔴 Imports no utilizados: {len(analysis.unused_imports)}")

                for imp in analysis.unused_imports:
                    print(f"   - Línea {imp.line_number}: {imp.line_content.strip()}")

                if fix_files:
                    if self.fix_file(analysis, dry_run):
                        files_fixed += 1
                        if not dry_run:
                            print(f"   ✅ Archivo corregido")
                        else:
                            print(f"   🔍 Archivo sería corregido (dry-run)")

        # Reporte final
        print("\n" + "=" * 60)
        print("📊 REPORTE FINAL")
        print("=" * 60)
        print(f"📁 Archivos analizados: {len(python_files)}")
        print(f"🔴 Archivos con imports no utilizados: {files_with_issues}")
        print(f"📝 Total de imports no utilizados: {total_unused}")

        if fix_files:
            if not dry_run:
                print(f"✅ Archivos corregidos: {files_fixed}")
                print(f"💾 Backups creados en: {self.backup_dir}")
            else:
                print(f"🔍 Archivos que serían corregidos: {files_fixed}")

        # Guardar reporte detallado
        self.save_report()

    def save_report(self) -> None:
        """Guarda un reporte detallado del análisis"""
        report_path = self.project_root / "import_analysis_report.txt"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("🔧 REPORTE DE ANÁLISIS DE IMPORTS NO UTILIZADOS\n")
            f.write("=" * 60 + "\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Proyecto: {self.project_root}\n\n")

            total_files = len(self.analysis_results)
            files_with_issues = len([a for a in self.analysis_results if a.unused_imports])
            total_unused = sum(len(a.unused_imports) for a in self.analysis_results)

            f.write("RESUMEN:\n")
            f.write(f"- Archivos analizados: {total_files}\n")
            f.write(f"- Archivos con imports no utilizados: {files_with_issues}\n")
            f.write(f"- Total de imports no utilizados: {total_unused}\n\n")

            f.write("DETALLES POR ARCHIVO:\n")
            f.write("-" * 40 + "\n")

            for analysis in self.analysis_results:
                if analysis.unused_imports:
                    rel_path = Path(analysis.file_path).relative_to(self.project_root)
                    f.write(f"\n📄 {rel_path}\n")
                    f.write(f"   Imports no utilizados: {len(analysis.unused_imports)}\n")

                    for imp in analysis.unused_imports:
                        f.write(f"   - Línea {imp.line_number}: {imp.line_content.strip()}\n")

        print(f"📋 Reporte guardado en: {report_path}")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Corrector de imports no utilizados")
    parser.add_argument("--project-root", default=".", help="Directorio raíz del proyecto")
    parser.add_argument("--fix", action="store_true", help="Corregir automáticamente los archivos")
    parser.add_argument("--dry-run", action="store_true", help="Modo dry-run (solo mostrar qué se haría)")
    parser.add_argument("--backup-dir", help="Directorio para backups (opcional)")

    args = parser.parse_args()

    # Obtener directorio del proyecto
    if args.project_root == ".":
        project_root = Path(__file__).parent.parent  # Subir dos niveles desde scripts/
    else:
        project_root = Path(args.project_root)

    # Crear detector
    detector = UnusedImportDetector(
        project_root=str(project_root),
        backup_dir=args.backup_dir
    )

    # Ejecutar análisis
    detector.run_analysis(
        fix_files=args.fix,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    main()
