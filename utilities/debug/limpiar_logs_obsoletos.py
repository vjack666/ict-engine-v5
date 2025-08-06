#!/usr/bin/env python3
"""
🧹 LIMPIADOR DE LOGS OBSOLETOS
============================

Busca y elimina todas las referencias obsoletas de logging en todo el sistema,
reemplazándolas con enviar_senal_log del SLUC v2.0

VERSIÓN: 1.0 - Limpieza masiva AsyncIO
"""

import sys
import asyncio
import ast
import re
from pathlib import Path

# Configurar project root
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from sistema.logging_interface import enviar_senal_log

class LoggingCleanupAnalyzer(ast.NodeVisitor):
    """Analizador AST para detectar referencias obsoletas de logging"""

    def __init__(self):
        self.imports_logging = False
        self.logging_usages = []
        self.logger_definitions = []
        self.logger_usages = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == 'logging':
                self.imports_logging = True
                self.logging_usages.append({
                    'type': 'import',
                    'line': node.lineno,
                    'text': f"import {alias.name}"
                })
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module == 'logging':
            self.imports_logging = True
            names = [alias.name for alias in node.names]
            self.logging_usages.append({
                'type': 'from_import',
                'line': node.lineno,
                'text': f"from logging import {', '.join(names)}"
            })
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Detectar logger = logging.getLogger()
        if (isinstance(node.value, ast.Call) and
            isinstance(node.value.func, ast.Attribute) and
            isinstance(node.value.func.value, ast.Name) and
            node.value.func.value.id == 'logging' and
            node.value.func.attr == 'getLogger'):

            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.logger_definitions.append({
                        'name': target.id,
                        'line': node.lineno,
                        'type': 'logger_definition'
                    })
        self.generic_visit(node)

    def visit_Call(self, node):
        # Detectar logger.debug(), logger.info(), etc.
        if (isinstance(node.func, ast.Attribute) and
            isinstance(node.func.value, ast.Name)):

            if node.func.value.id == 'logging':
                # logging.debug(), logging.info(), etc.
                self.logging_usages.append({
                    'type': 'logging_call',
                    'line': node.lineno,
                    'method': node.func.attr,
                    'object': 'logging'
                })
            elif any(logger['name'] == node.func.value.id for logger in self.logger_definitions):
                # logger.debug(), logger.info(), etc.
                self.logger_usages.append({
                    'type': 'logger_call',
                    'line': node.lineno,
                    'method': node.func.attr,
                    'object': node.func.value.id
                })
        self.generic_visit(node)

class LoggingCleanupTool:
    """Herramienta para limpiar referencias obsoletas de logging"""

    def __init__(self):
        self.files_to_process = []
        self.files_with_issues = []
        self.total_issues_found = 0

    async def scan_entire_project(self):
        """Escanea todo el proyecto buscando referencias obsoletas"""

        enviar_senal_log("INFO", "🔍 ESCANEANDO PROYECTO COMPLETO PARA LOGS OBSOLETOS", "logging_cleanup", "scan")
        enviar_senal_log("INFO", "=" * 70, "logging_cleanup", "scan")

        # Directorios a escanear
        scan_dirs = [
            PROJECT_ROOT / "core",
            PROJECT_ROOT / "dashboard",
            PROJECT_ROOT / "scripts",
            PROJECT_ROOT / "sistema",
            PROJECT_ROOT / "utilities",
            PROJECT_ROOT / "config",
            PROJECT_ROOT,  # Archivos raíz
        ]

        # Recopilar todos los archivos Python
        all_files = []
        for scan_dir in scan_dirs:
            if scan_dir.exists():
                py_files = list(scan_dir.rglob("*.py"))
                all_files.extend(py_files)

        # Incluir archivos Python en la raíz
        root_py_files = [f for f in PROJECT_ROOT.glob("*.py") if f.is_file()]
        all_files.extend(root_py_files)

        # Eliminar duplicados
        all_files = list(set(all_files))

        enviar_senal_log("INFO", f"📁 Archivos Python encontrados: {len(all_files)}", "logging_cleanup", "scan")

        # Procesar archivos de forma asíncrona
        tasks = [self._analyze_file_async(file_path) for file_path in all_files]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Procesar resultados
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                enviar_senal_log("WARNING", f"Error procesando {all_files[i].name}: {result}", "logging_cleanup", "scan")

        await self._generate_cleanup_report()

    async def _analyze_file_async(self, file_path: Path):
        """Analiza un archivo individual de forma asíncrona"""

        try:
            # Leer archivo
            content = await asyncio.to_thread(self._read_file_sync, file_path)

            # Análisis con AST
            try:
                tree = ast.parse(content)
                analyzer = LoggingCleanupAnalyzer()
                analyzer.visit(tree)

                # Análisis adicional con regex para capturas más amplias
                regex_issues = await self._regex_analysis_async(content, file_path)

                # Si hay problemas, registrar archivo
                total_ast_issues = (len(analyzer.logging_usages) +
                                  len(analyzer.logger_definitions) +
                                  len(analyzer.logger_usages))

                if total_ast_issues > 0 or len(regex_issues) > 0:
                    file_info = {
                        'path': file_path,
                        'ast_analysis': analyzer,
                        'regex_issues': regex_issues,
                        'total_issues': total_ast_issues + len(regex_issues)
                    }
                    self.files_with_issues.append(file_info)
                    self.total_issues_found += file_info['total_issues']

            except SyntaxError:
                enviar_senal_log("DEBUG", f"Error de sintaxis en {file_path.name}, analizando con regex", "logging_cleanup", "analysis")
                # Fallback a análisis regex
                regex_issues = await self._regex_analysis_async(content, file_path)
                if len(regex_issues) > 0:
                    file_info = {
                        'path': file_path,
                        'ast_analysis': None,
                        'regex_issues': regex_issues,
                        'total_issues': len(regex_issues)
                    }
                    self.files_with_issues.append(file_info)
                    self.total_issues_found += file_info['total_issues']

        except Exception as e:
            enviar_senal_log("WARNING", f"Error analizando {file_path.name}: {e}", "logging_cleanup", "analysis")

    def _read_file_sync(self, file_path: Path) -> str:
        """Lee archivo de forma síncrona para asyncio.to_thread"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    async def _regex_analysis_async(self, content: str, file_path: Path):
        """Análisis adicional con regex para capturas más amplias"""

        regex_patterns = [
            (r'logger\.debug\s*\(', 'logger.debug() call'),
            (r'logger\.info\s*\(', 'logger.info() call'),
            (r'logger\.warning\s*\(', 'logger.warning() call'),
            (r'logger\.error\s*\(', 'logger.error() call'),
            (r'logger\.critical\s*\(', 'logger.critical() call'),
            (r'logging\.debug\s*\(', 'logging.debug() call'),
            (r'logging\.info\s*\(', 'logging.info() call'),
            (r'logging\.warning\s*\(', 'logging.warning() call'),
            (r'logging\.error\s*\(', 'logging.error() call'),
            (r'logging\.getLogger\s*\(', 'logging.getLogger() call'),
            (r'import\s+logging', 'import logging'),
            (r'from\s+logging\s+import', 'from logging import'),
            (r'=\s*logging\.getLogger', 'logger definition'),
        ]

        issues = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            for pattern, description in regex_patterns:
                if re.search(pattern, line):
                    issues.append({
                        'line': line_num,
                        'text': line.strip(),
                        'type': description,
                        'pattern': pattern
                    })

        return issues

    async def _generate_cleanup_report(self):
        """Genera reporte detallado de limpieza"""

        enviar_senal_log("INFO", "\n📊 REPORTE DE LOGS OBSOLETOS ENCONTRADOS", "logging_cleanup", "report")
        enviar_senal_log("INFO", "=" * 70, "logging_cleanup", "report")

        enviar_senal_log("INFO", f"📄 Archivos con problemas: {len(self.files_with_issues)}", "logging_cleanup", "report")
        enviar_senal_log("INFO", f"⚠️ Total de issues encontrados: {self.total_issues_found}", "logging_cleanup", "report")

        if len(self.files_with_issues) == 0:
            enviar_senal_log("INFO", "✅ No se encontraron logs obsoletos en el proyecto", "logging_cleanup", "report")
            return

        # Mostrar archivos problemáticos
        enviar_senal_log("INFO", "\n🔍 ARCHIVOS CON LOGS OBSOLETOS:", "logging_cleanup", "report")

        for file_info in self.files_with_issues:
            file_path = file_info['path']
            relative_path = file_path.relative_to(PROJECT_ROOT)

            enviar_senal_log("INFO", f"\n📁 {relative_path} ({file_info['total_issues']} issues)", "logging_cleanup", "report")

            # Mostrar issues de AST
            if file_info['ast_analysis']:
                ast_analyzer = file_info['ast_analysis']

                for usage in ast_analyzer.logging_usages:
                    text_part = usage.get('text', f"{usage['type']} detected")
                    enviar_senal_log("INFO", f"   🔸 Línea {usage['line']}: {usage['type']} - {text_part}", "logging_cleanup", "report")

                for definition in ast_analyzer.logger_definitions:
                    enviar_senal_log("INFO", f"   🔸 Línea {definition['line']}: Logger definition - {definition['name']}", "logging_cleanup", "report")

                for usage in ast_analyzer.logger_usages:
                    enviar_senal_log("INFO", f"   🔸 Línea {usage['line']}: {usage['object']}.{usage['method']}()", "logging_cleanup", "report")

            # Mostrar issues de regex
            for issue in file_info['regex_issues']:
                enviar_senal_log("INFO", f"   🔹 Línea {issue['line']}: {issue['type']} - {issue['text'][:50]}...", "logging_cleanup", "report")

        await self._generate_cleanup_suggestions()

    async def _generate_cleanup_suggestions(self):
        """Genera sugerencias de limpieza automática"""

        enviar_senal_log("INFO", "\n🎯 SUGERENCIAS DE LIMPIEZA AUTOMÁTICA", "logging_cleanup", "suggestions")
        enviar_senal_log("INFO", "=" * 70, "logging_cleanup", "suggestions")

        # Categorizar por tipo de cambio necesario
        files_need_import_cleanup = []
        files_need_logger_migration = []
        files_need_call_migration = []

        for file_info in self.files_with_issues:
            needs_import = False
            needs_logger = False
            needs_calls = False

            if file_info['ast_analysis']:
                ast_analyzer = file_info['ast_analysis']
                if ast_analyzer.imports_logging or any('import' in u['type'] for u in ast_analyzer.logging_usages):
                    needs_import = True
                if ast_analyzer.logger_definitions:
                    needs_logger = True
                if ast_analyzer.logger_usages or any('call' in u['type'] for u in ast_analyzer.logging_usages):
                    needs_calls = True

            # También verificar regex
            for issue in file_info['regex_issues']:
                if 'import' in issue['type']:
                    needs_import = True
                elif 'definition' in issue['type'] or 'getLogger' in issue['type']:
                    needs_logger = True
                elif 'call' in issue['type']:
                    needs_calls = True

            if needs_import:
                files_need_import_cleanup.append(file_info)
            if needs_logger:
                files_need_logger_migration.append(file_info)
            if needs_calls:
                files_need_call_migration.append(file_info)

        enviar_senal_log("INFO", f"📦 Archivos que necesitan limpieza de imports: {len(files_need_import_cleanup)}", "logging_cleanup", "suggestions")
        enviar_senal_log("INFO", f"🏷️ Archivos que necesitan migración de logger: {len(files_need_logger_migration)}", "logging_cleanup", "suggestions")
        enviar_senal_log("INFO", f"📞 Archivos que necesitan migración de calls: {len(files_need_call_migration)}", "logging_cleanup", "suggestions")

        enviar_senal_log("INFO", "\n💡 PRÓXIMOS PASOS RECOMENDADOS:", "logging_cleanup", "suggestions")
        enviar_senal_log("INFO", "1. Ejecutar limpieza automática de imports obsoletos", "logging_cleanup", "suggestions")
        enviar_senal_log("INFO", "2. Migrar definiciones de logger a enviar_senal_log", "logging_cleanup", "suggestions")
        enviar_senal_log("INFO", "3. Reemplazar calls de logger.* con enviar_senal_log", "logging_cleanup", "suggestions")
        enviar_senal_log("INFO", "4. Verificar funcionalidad después de cada paso", "logging_cleanup", "suggestions")

async def main():
    """Función principal"""

    enviar_senal_log("INFO", "🧹 INICIANDO LIMPIEZA DE LOGS OBSOLETOS", "logging_cleanup", "main")

    cleanup_tool = LoggingCleanupTool()
    await cleanup_tool.scan_entire_project()

    enviar_senal_log("INFO", "\n🎉 ESCANEO COMPLETADO", "logging_cleanup", "main")
    enviar_senal_log("INFO", "Revisa el reporte para proceder con la limpieza", "logging_cleanup", "main")

if __name__ == "__main__":
    asyncio.run(main())
