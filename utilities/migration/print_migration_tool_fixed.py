"""
Print Migration Tool - Migra print statements a logging profesional
VERSION: 2.0 - Recursion-Safe
"""
import os
import re
import json
from pathlib import Path
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import ast

def simple_log(mensaje: str, nivel: str = "INFO"):
    """Logging ultra-simple y recursion-safe"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{nivel}] MIGRATION: {mensaje}")

@dataclass
class PrintStatement:
    """Representa un print statement encontrado"""
    file_path: str
    line_number: int
    original_code: str
    suggested_replacement: str
    print_type: str
    context: str = ""

@dataclass
class MigrationReport:
    """Reporte de migración"""
    total_files_scanned: int = 0
    total_prints_found: int = 0
    total_prints_migrated: int = 0
    files_with_prints: List[str] = None
    print_statements: List[PrintStatement] = None
    errors: List[str] = None
    
    def __post_init__(self):
        if self.files_with_prints is None:
            self.files_with_prints = []
        if self.print_statements is None:
            self.print_statements = []
        if self.errors is None:
            self.errors = []

class PrintMigrationTool:
    """Tool para migrar print statements a logging profesional"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.report = MigrationReport()
        self.dry_run = True
        simple_log("📝 Print Migration Tool inicializado")
        
        # Patrones para detectar diferentes tipos de print
        self.print_patterns = {
            'simple': re.compile(r'print\s*\(\s*["\']([^"\']*)["\']'),
            'f_string': re.compile(r'print\s*\(\s*f["\']([^"\']*)["\']'),
            'variable': re.compile(r'print\s*\(\s*(\w+)'),
            'complex': re.compile(r'print\s*\([^)]+\)'),
        }
        
        # Mapeo de contexto a logging level
        self.context_mapping = {
            'error': 'ERROR',
            'warning': 'WARNING', 
            'info': 'INFO',
            'debug': 'DEBUG',
            'success': 'SUCCESS'
        }
        
        # Archivos a excluir
        self.exclude_patterns = [
            '*/test*',
            '*/__pycache__/*',
            '*/temp/*',
            '*/logs/*',
            '*/.git/*',
            '*/venv/*',
            '*/node_modules/*'
        ]
    
    def scan_for_prints(self) -> MigrationReport:
        """Escanea todos los archivos Python buscando print statements"""
        simple_log("🔍 Iniciando escaneo de print statements...")
        
        python_files = list(self.project_root.rglob("*.py"))
        python_files = [f for f in python_files if not self._should_exclude(f)]
        
        self.report.total_files_scanned = len(python_files)
        simple_log(f"📁 Escaneando {len(python_files)} archivos Python...")
        
        for file_path in python_files:
            try:
                self._scan_file(file_path)
            except Exception as e:
                error_msg = f"Error escaneando {file_path}: {e}"
                self.report.errors.append(error_msg)
                simple_log(error_msg, "ERROR")
        
        self.report.total_prints_found = len(self.report.print_statements)
        simple_log(f"✅ Escaneo completado: {self.report.total_prints_found} prints encontrados en {len(self.report.files_with_prints)} archivos")
        
        return self.report
    
    def _should_exclude(self, file_path: Path) -> bool:
        """Determina si un archivo debe ser excluido del escaneo"""
        file_str = str(file_path)
        for pattern in self.exclude_patterns:
            if file_str.find(pattern.replace('*', '')) != -1:
                return True
        return False
    
    def _scan_file(self, file_path: Path):
        """Escanea un archivo individual buscando print statements"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            file_has_prints = False
            
            for line_num, line in enumerate(lines, 1):
                line_stripped = line.strip()
                
                # Skip comments and docstrings
                if line_stripped.startswith('#') or line_stripped.startswith('"""') or line_stripped.startswith("'''"):
                    continue
                
                # Check for print statements
                if 'print(' in line:
                    file_has_prints = True
                    print_stmt = self._analyze_print_statement(str(file_path), line_num, line)
                    if print_stmt:
                        self.report.print_statements.append(print_stmt)
            
            if file_has_prints:
                self.report.files_with_prints.append(str(file_path))
                
        except Exception as e:
            self.report.errors.append(f"Error leyendo {file_path}: {e}")
    
    def _analyze_print_statement(self, file_path: str, line_number: int, line: str) -> PrintStatement:
        """Analiza un print statement y sugiere reemplazo"""
        original_code = line.strip()
        
        # Determinar tipo de print
        print_type = "simple"
        if "f'" in line or 'f"' in line:
            print_type = "f_string"
        elif any(op in line for op in ['+', '%', '.format']):
            print_type = "complex"
        
        # Determinar nivel de logging basado en contexto
        logging_level = self._determine_logging_level(line.lower())
        
        # Generar sugerencia de reemplazo
        suggested_replacement = self._generate_replacement(line, logging_level)
        
        return PrintStatement(
            file_path=file_path,
            line_number=line_number,
            original_code=original_code,
            suggested_replacement=suggested_replacement,
            print_type=print_type,
            context=f"Línea {line_number}"
        )
    
    def _determine_logging_level(self, line: str) -> str:
        """Determina el nivel de logging apropiado basado en el contenido"""
        line_lower = line.lower()
        
        if any(word in line_lower for word in ['error', 'exception', 'fail', 'critical']):
            return 'ERROR'
        elif any(word in line_lower for word in ['warning', 'warn', 'attention']):
            return 'WARNING'
        elif any(word in line_lower for word in ['debug', 'trace', 'verbose']):
            return 'DEBUG'
        elif any(word in line_lower for word in ['success', 'complete', 'finish', 'done']):
            return 'SUCCESS'
        else:
            return 'INFO'
    
    def _generate_replacement(self, line: str, logging_level: str) -> str:
        """Genera la línea de reemplazo con logging profesional"""
        # Extraer el contenido del print
        match = re.search(r'print\s*\(([^)]+)\)', line)
        if not match:
            return line
        
        print_content = match.group(1).strip()
        indent = len(line) - len(line.lstrip())
        
        # Generar reemplazo con enviar_senal_log
        replacement = f"{' ' * indent}enviar_senal_log('{logging_level}', {print_content}, __name__)"
        
        return replacement
    
    def migrate_prints(self, dry_run: bool = True) -> MigrationReport:
        """Ejecuta la migración de prints"""
        self.dry_run = dry_run
        mode = "DRY RUN" if dry_run else "REAL"
        simple_log(f"🚀 Iniciando migración de prints - Modo: {mode}")
        
        if not self.report.print_statements:
            simple_log("📝 Primero ejecutando escaneo...")
            self.scan_for_prints()
        
        if not self.report.print_statements:
            simple_log("✅ No se encontraron prints para migrar")
            return self.report
        
        migrated_count = 0
        
        for print_stmt in self.report.print_statements:
            try:
                if not dry_run:
                    self._perform_migration(print_stmt)
                migrated_count += 1
                
            except Exception as e:
                error_msg = f"Error migrando print en {print_stmt.file_path}:{print_stmt.line_number}: {e}"
                self.report.errors.append(error_msg)
                simple_log(error_msg, "ERROR")
        
        self.report.total_prints_migrated = migrated_count
        simple_log(f"✅ Migración completada: {migrated_count}/{len(self.report.print_statements)} prints procesados")
        
        return self.report
    
    def _perform_migration(self, print_stmt: PrintStatement):
        """Ejecuta la migración real de un print statement"""
        file_path = Path(print_stmt.file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Reemplazar la línea
        if print_stmt.line_number <= len(lines):
            lines[print_stmt.line_number - 1] = print_stmt.suggested_replacement + '\n'
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
    
    def generate_report(self) -> str:
        """Genera un reporte detallado de la migración"""
        report_lines = [
            "=" * 60,
            "📋 REPORTE DE MIGRACIÓN DE PRINT STATEMENTS",
            "=" * 60,
            f"📁 Archivos escaneados: {self.report.total_files_scanned}",
            f"🔍 Print statements encontrados: {self.report.total_prints_found}",
            f"✅ Print statements migrados: {self.report.total_prints_migrated}",
            f"📂 Archivos con prints: {len(self.report.files_with_prints)}",
            f"❌ Errores: {len(self.report.errors)}",
            "",
            "📊 DISTRIBUCIÓN POR TIPO:",
        ]
        
        # Contar tipos de print
        type_counts = {}
        for stmt in self.report.print_statements:
            type_counts[stmt.print_type] = type_counts.get(stmt.print_type, 0) + 1
        
        for print_type, count in type_counts.items():
            report_lines.append(f"  {print_type}: {count}")
        
        if self.report.files_with_prints:
            report_lines.extend([
                "",
                "📂 ARCHIVOS CON PRINTS:",
            ])
            for file_path in self.report.files_with_prints[:10]:  # Mostrar solo los primeros 10
                report_lines.append(f"  {file_path}")
            
            if len(self.report.files_with_prints) > 10:
                report_lines.append(f"  ... y {len(self.report.files_with_prints) - 10} más")
        
        if self.report.errors:
            report_lines.extend([
                "",
                "❌ ERRORES ENCONTRADOS:",
            ])
            for error in self.report.errors[:5]:  # Mostrar solo los primeros 5
                report_lines.append(f"  {error}")
            
            if len(self.report.errors) > 5:
                report_lines.append(f"  ... y {len(self.report.errors) - 5} más")
        
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)
    
    def save_report(self, output_path: str = None):
        """Guarda el reporte en un archivo JSON"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.project_root / f"print_migration_report_{timestamp}.json"
        
        report_data = asdict(self.report)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        simple_log(f"💾 Reporte guardado en: {output_path}")


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Print Migration Tool')
    parser.add_argument('--project-root', default='.', help='Ruta del proyecto')
    parser.add_argument('--scan-only', action='store_true', help='Solo escanear, no migrar')
    parser.add_argument('--migrate', action='store_true', help='Ejecutar migración real')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Migración de prueba')
    parser.add_argument('--report', action='store_true', help='Generar reporte')
    
    args = parser.parse_args()
    
    # Si no hay argumentos, ejecutar en modo interactivo
    if len(sys.argv) == 1:
        simple_log("🚀 Ejecutando Print Migration Tool en modo automático...")
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        migrator = PrintMigrationTool(project_root)
        
        # Escaneo
        simple_log("1️⃣ Ejecutando escaneo...")
        migrator.scan_for_prints()
        
        # Mostrar reporte
        simple_log("2️⃣ Generando reporte...")
        print(migrator.generate_report())
        
        # Migración en dry-run
        simple_log("3️⃣ Ejecutando migración (dry-run)...")
        migrator.migrate_prints(dry_run=True)
        
        # Guardar reporte
        simple_log("4️⃣ Guardando reporte...")
        migrator.save_report()
        
        simple_log("✅ Print Migration Tool completado exitosamente!")
        return migrator
    
    # Modo con argumentos
    migrator = PrintMigrationTool(args.project_root)
    
    if args.scan_only:
        migrator.scan_for_prints()
    elif args.migrate:
        migrator.migrate_prints(dry_run=not args.migrate)
    elif args.dry_run:
        migrator.migrate_prints(dry_run=True)
    
    if args.report:
        print(migrator.generate_report())
        migrator.save_report()
    
    return migrator


if __name__ == "__main__":
    main()
