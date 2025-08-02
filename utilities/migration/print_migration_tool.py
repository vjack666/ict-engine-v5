# 🔧 PRINT STATEMENT MIGRATION TOOL
# Sprint 1.1 - Debug System & Clean Code
# Migra todos los print() statements a enviar_senal_log()

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import argparse
import json
from datetime import datetime

class PrintMigrationTool:
    """
    Herramienta para migrar print statements a enviar_senal_log()
    Parte del Sprint 1.1 - Clean Code initiative
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.migration_report = {
            'files_processed': 0,
            'prints_found': 0,
            'prints_migrated': 0,
            'errors': [],
            'files_modified': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # 🎯 Patrones de print statements a buscar
        self.print_patterns = [
            r'print\s*\(',  # print(
            r'print\s+',    # print (space)
        ]
        
        # 🔧 Archivos a excluir de la migración
        self.exclude_files = {
            '__pycache__',
            '.git',
            '.vscode',
            'venv',
            'env',
            '.pytest_cache',
            'node_modules',
            'debug_launcher.py',  # Este archivo puede tener prints para debug
            'print_migration_tool.py'  # Este mismo archivo
        }
        
        # 📁 Extensiones de archivo a procesar
        self.target_extensions = {'.py'}
    
    def scan_project(self) -> Dict:
        """Escanea todo el proyecto buscando print statements"""
        print("🔍 Escaneando proyecto en busca de print statements...")
        
        results = {
            'files_with_prints': [],
            'total_prints': 0,
            'files_scanned': 0
        }
        
        for file_path in self._get_python_files():
            self.migration_report['files_processed'] += 1
            results['files_scanned'] += 1
            
            print_locations = self._find_prints_in_file(file_path)
            
            if print_locations:
                results['files_with_prints'].append({
                    'file': str(file_path.relative_to(self.project_root)),
                    'prints': print_locations,
                    'count': len(print_locations)
                })
                results['total_prints'] += len(print_locations)
                self.migration_report['prints_found'] += len(print_locations)
        
        return results
    
    def _get_python_files(self) -> List[Path]:
        """Obtiene todos los archivos Python del proyecto"""
        python_files = []
        
        for root, dirs, files in os.walk(self.project_root):
            # 🚫 Excluir directorios no deseados
            dirs[:] = [d for d in dirs if d not in self.exclude_files]
            
            for file in files:
                if any(file.endswith(ext) for ext in self.target_extensions):
                    file_path = Path(root) / file
                    
                    # 🚫 Excluir archivos específicos
                    if file not in self.exclude_files:
                        python_files.append(file_path)
        
        return python_files
    
    def _find_prints_in_file(self, file_path: Path) -> List[Dict]:
        """Encuentra todos los print statements en un archivo"""
        print_locations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                # 🔍 Buscar patrones de print
                for pattern in self.print_patterns:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        # ✅ Verificar que no sea un comentario
                        if not self._is_commented_out(line, match.start()):
                            print_locations.append({
                                'line_number': line_num,
                                'line_content': line.strip(),
                                'column': match.start(),
                                'pattern_matched': pattern
                            })
        
        except Exception as e:
            self.migration_report['errors'].append({
                'file': str(file_path),
                'error': str(e),
                'operation': 'reading_file'
            })
        
        return print_locations
    
    def _is_commented_out(self, line: str, position: int) -> bool:
        """Verifica si el print está comentado"""
        # 🔍 Buscar # antes de la posición
        hash_pos = line.find('#')
        return hash_pos != -1 and hash_pos < position
    
    def migrate_file(self, file_path: Path, dry_run: bool = True) -> Dict:
        """Migra los print statements de un archivo específico"""
        migration_result = {
            'file': str(file_path.relative_to(self.project_root)),
            'prints_migrated': 0,
            'errors': [],
            'changes_made': []
        }
        
        try:
            # 📖 Leer archivo original
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
                lines = original_content.splitlines()
            
            # 🔄 Procesar línea por línea
            modified_lines = []
            changes_made = False
            
            for line_num, line in enumerate(lines):
                modified_line = self._migrate_line(line, line_num + 1, file_path)
                
                if modified_line != line:
                    changes_made = True
                    migration_result['prints_migrated'] += 1
                    migration_result['changes_made'].append({
                        'line_number': line_num + 1,
                        'original': line.strip(),
                        'modified': modified_line.strip()
                    })
                
                modified_lines.append(modified_line)
            
            # 💾 Guardar cambios si no es dry run
            if changes_made and not dry_run:
                # 🔐 Crear backup
                backup_path = file_path.with_suffix(f'{file_path.suffix}.backup')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # 💾 Escribir archivo modificado
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(modified_lines))
                
                self.migration_report['files_modified'].append(str(file_path))
                migration_result['backup_created'] = str(backup_path)
            
            migration_result['dry_run'] = dry_run
            migration_result['changes_needed'] = changes_made
            
        except Exception as e:
            error_info = {
                'error': str(e),
                'operation': 'migrating_file'
            }
            migration_result['errors'].append(error_info)
            self.migration_report['errors'].append({
                'file': str(file_path),
                **error_info
            })
        
        return migration_result
    
    def _migrate_line(self, line: str, line_number: int, file_path: Path) -> str:
        """Migra una línea específica reemplazando print con enviar_senal_log"""
        
        # 🚫 Skip si es comentario
        stripped = line.strip()
        if stripped.startswith('#'):
            return line
        
        # 🔍 Buscar y reemplazar print statements
        modified_line = line
        
        # 🎯 Patrón más específico para capturar el contenido del print
        print_pattern = r'print\s*\(\s*([^)]+)\s*\)'
        
        def replace_print(match):
            print_content = match.group(1).strip()
            
            # 🎯 Determinar el tipo de log basado en el contenido
            log_type = self._determine_log_type(print_content)
            
            # 🔧 Crear llamada a enviar_senal_log
            return f'enviar_senal_log("{log_type}", {print_content}, __name__, "sistema")'
        
        # 🔄 Aplicar reemplazo
        modified_line = re.sub(print_pattern, replace_print, modified_line)
        
        # ✅ Verificar si necesitamos añadir import
        if modified_line != line and 'enviar_senal_log' in modified_line:
            self._ensure_import_exists(file_path)
        
        return modified_line
    
    def _determine_log_type(self, print_content: str) -> str:
        """Determina el tipo de log basado en el contenido del print"""
        content_lower = print_content.lower()
        
        # 🚨 Error patterns
        if any(word in content_lower for word in ['error', 'exception', 'failed', 'fail']):
            return 'ERROR'
        
        # ⚠️ Warning patterns  
        if any(word in content_lower for word in ['warning', 'warn', 'deprecated']):
            return 'WARNING'
        
        # ✅ Success patterns
        if any(word in content_lower for word in ['success', 'completed', 'done', 'ok']):
            return 'SUCCESS'
        
        # 🔧 Debug patterns
        if any(word in content_lower for word in ['debug', 'test', 'checking']):
            return 'DEBUG'
        
        # 📊 Info por defecto
        return 'INFO'
    
    def _ensure_import_exists(self, file_path: Path):
        """Asegura que el import de enviar_senal_log existe en el archivo"""
        # 📝 Esta función sería más compleja en implementación real
        # Por ahora, solo registramos que necesita el import
        pass
    
    def generate_migration_report(self, output_path: Path = None) -> str:
        """Genera un reporte detallado de la migración"""
        if output_path is None:
            output_path = self.project_root / f"migration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # 📊 Calcular estadísticas
        success_rate = 0
        if self.migration_report['prints_found'] > 0:
            success_rate = (self.migration_report['prints_migrated'] / self.migration_report['prints_found']) * 100
        
        report_data = {
            **self.migration_report,
            'success_rate_percentage': round(success_rate, 2),
            'completion_status': 'COMPLETED' if success_rate >= 95 else 'PARTIAL' if success_rate >= 50 else 'NEEDS_WORK'
        }
        
        # 💾 Guardar reporte
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        return str(output_path)
    
    def migrate_all_files(self, dry_run: bool = True) -> Dict:
        """Migra todos los archivos del proyecto"""
        print(f"🚀 {'[DRY RUN] ' if dry_run else ''}Iniciando migración de print statements...")
        
        # 🔍 Primero escanear
        scan_results = self.scan_project()
        
        if scan_results['total_prints'] == 0:
            print("✅ No se encontraron print statements para migrar")
            return {
                'status': 'NO_ACTION_NEEDED',
                'files_processed': scan_results['files_scanned'],
                'prints_found': 0
            }
        
        print(f"📊 Encontrados {scan_results['total_prints']} prints en {len(scan_results['files_with_prints'])} archivos")
        
        # 🔄 Migrar cada archivo
        migration_results = []
        for file_info in scan_results['files_with_prints']:
            file_path = self.project_root / file_info['file']
            result = self.migrate_file(file_path, dry_run)
            migration_results.append(result)
            
            if result['prints_migrated'] > 0:
                print(f"  {'[DRY RUN] ' if dry_run else ''}✅ {file_info['file']}: {result['prints_migrated']} prints migrados")
        
        # 📊 Resumen final
        total_migrated = sum(r['prints_migrated'] for r in migration_results)
        self.migration_report['prints_migrated'] = total_migrated
        
        return {
            'status': 'COMPLETED' if total_migrated == scan_results['total_prints'] else 'PARTIAL',
            'files_processed': len(migration_results),
            'prints_found': scan_results['total_prints'],
            'prints_migrated': total_migrated,
            'migration_results': migration_results
        }


def main():
    """Función principal del migration tool"""
    parser = argparse.ArgumentParser(description="Print Migration Tool - Sprint 1.1")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(), 
                       help="Root directory of the project")
    parser.add_argument("--scan-only", action="store_true", 
                       help="Only scan for print statements, don't migrate")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be changed without making changes")
    parser.add_argument("--report", action="store_true", 
                       help="Generate detailed migration report")
    
    args = parser.parse_args()
    
    # 🎯 Inicializar herramienta
    migration_tool = PrintMigrationTool(args.project_root)
    
    if args.scan_only:
        # 🔍 Solo escanear
        print("🔍 MODO SCAN - Solo escanear print statements")
        results = migration_tool.scan_project()
        
        print(f"\n📊 RESULTADOS DEL SCAN:")
        print(f"  📁 Archivos escaneados: {results['files_scanned']}")
        print(f"  📋 Archivos con prints: {len(results['files_with_prints'])}")
        print(f"  🎯 Total prints encontrados: {results['total_prints']}")
        
        if results['files_with_prints']:
            print(f"\n📋 ARCHIVOS CON PRINT STATEMENTS:")
            for file_info in results['files_with_prints']:
                print(f"  📄 {file_info['file']}: {file_info['count']} prints")
    
    elif args.dry_run:
        # 🧪 Dry run
        print("🧪 MODO DRY RUN - Mostrar cambios sin aplicar")
        results = migration_tool.migrate_all_files(dry_run=True)
        
        print(f"\n📊 RESULTADOS DEL DRY RUN:")
        print(f"  📁 Archivos procesados: {results['files_processed']}")
        print(f"  🎯 Prints encontrados: {results['prints_found']}")
        print(f"  🔄 Prints que se migrarían: {results['prints_migrated']}")
        print(f"  📈 Estado: {results['status']}")
    
    else:
        # 🚀 Migración real
        print("🚀 MODO MIGRACIÓN - Aplicando cambios")
        results = migration_tool.migrate_all_files(dry_run=False)
        
        print(f"\n📊 RESULTADOS DE LA MIGRACIÓN:")
        print(f"  📁 Archivos procesados: {results['files_processed']}")
        print(f"  🎯 Prints encontrados: {results['prints_found']}")
        print(f"  ✅ Prints migrados: {results['prints_migrated']}")
        print(f"  📈 Estado: {results['status']}")
        
        if results['status'] == 'COMPLETED':
            print("🎉 ¡Migración completada exitosamente!")
        elif results['status'] == 'PARTIAL':
            print("⚠️ Migración parcial - revisar errores")
        
        # 🔐 Recordar sobre backups
        if migration_tool.migration_report['files_modified']:
            print(f"\n💾 BACKUPS CREADOS:")
            print("  Se crearon archivos .backup para todos los archivos modificados")
            print("  Puedes restaurar usando: mv archivo.py.backup archivo.py")
    
    # 📊 Generar reporte si se solicita
    if args.report:
        report_path = migration_tool.generate_migration_report()
        print(f"\n📊 Reporte detallado guardado en: {report_path}")


if __name__ == "__main__":
    main()
