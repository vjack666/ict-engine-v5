#!/usr/bin/env python3
"""
Script para detectar imports de subprocess no usados
Analiza el patrón que teníamos con 'os'
"""

import ast
from pathlib import Path
# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log

class SubprocessImportChecker(ast.NodeVisitor):
    def __init__(self):
        self.imports_subprocess = False
        self.uses_subprocess = False
        self.subprocess_usage_lines = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == 'subprocess':
                self.imports_subprocess = True
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module == 'subprocess':
            self.imports_subprocess = True
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == 'subprocess':
            self.uses_subprocess = True
            self.subprocess_usage_lines.append(node.lineno)
        self.generic_visit(node)

    def visit_Name(self, node):
        # Revisar si se usa subprocess directamente (ej: subprocess como argumento)
        if node.id == 'subprocess' and isinstance(node.ctx, ast.Load):
            # Solo contar como uso si no es parte de import
            # Esto es más complejo, pero por simplicidad asumimos uso directo
            pass
        self.generic_visit(node)

def check_file(file_path):
    """Verifica si un archivo importa subprocess sin usarlo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content)
        checker = SubprocessImportChecker()
        checker.visit(tree)

        return {
            'imports_subprocess': checker.imports_subprocess,
            'uses_subprocess': checker.uses_subprocess,
            'usage_lines': checker.subprocess_usage_lines,
            'file_path': str(file_path)
        }
    except Exception as e:
        return {
            'imports_subprocess': False,
            'uses_subprocess': False,
            'usage_lines': [],
            'file_path': str(file_path),
            'error': str(e)
        }

def main():
    """Función principal"""
    project_root = Path(__file__).parent
    print(f"🔍 Escaneando subprocess imports en: {project_root}")
    print("=" * 70)

    unused_subprocess_files = []
    total_files_checked = 0

    # Escanear todos los archivos Python
    for py_file in project_root.rglob("*.py"):
        # Saltar archivos de cache y este mismo script
        if "__pycache__" in str(py_file) or py_file.name == "check_subprocess_imports.py":
            continue

        total_files_checked += 1
        result = check_file(py_file)

        if 'error' in result:
            enviar_senal_log("ERROR", f"❌ Error en {result['file_path']}: {result['error']}", __name__, "sistema")
            continue

        if result['imports_subprocess'] and not result['uses_subprocess']:
            unused_subprocess_files.append(result)
            print(f"🟡 SUBPROCESS NO USADO: {result['file_path']}")
        elif result['imports_subprocess'] and result['uses_subprocess']:
            print(f"✅ SUBPROCESS USADO: {result['file_path']} (líneas: {result['usage_lines']})")

    print("\n" + "=" * 70)
    print(f"📊 RESUMEN:")
    print(f"   Archivos verificados: {total_files_checked}")
    print(f"   Imports subprocess sin usar: {len(unused_subprocess_files)}")

    if unused_subprocess_files:
        print(f"\n🧹 ARCHIVOS QUE NECESITAN LIMPIEZA:")
        for result in unused_subprocess_files:
            print(f"   - {result['file_path']}")
    else:
        print(f"\n🎉 ¡Todos los imports de subprocess están siendo usados!")

if __name__ == "__main__":
    main()
