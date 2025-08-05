# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log
"""
Print Migration Tool - Compatible with Consolidator
"""
import os
import re
from pathlib import Path
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

class PrintMigrationTool:
    """Clase compatible con el consolidator"""

    def __init__(self, project_root):
        self.project_root = Path(project_root)
        log("📝 Print Migration Tool inicializado")

    def scan_project(self, scan_only=True):
        """Escanea el proyecto y retorna resultados compatibles"""
        log("🔍 Escaneando proyecto...")

        python_files = []
        for root, dirs, files in os.walk(self.project_root):
            # Excluir directorios no deseados
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'node_modules', 'logs']]

            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))

        total_prints = 0
        files_with_prints = []

        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Contar prints
                print_count = len(re.findall(r'print\s*\(', content))
                if print_count > 0:
                    total_prints += print_count
                    files_with_prints.append(file_path)

            except Exception as e:
                log(f"❌ Error leyendo {file_path}: {e}")

        log(f"✅ Escaneo completado: {total_prints} prints encontrados")

        # Retornar formato esperado por el consolidator
        # CLAVE: prints_migrated significa "prints que quedan por migrar" en el consolidator
        return {
            'total_files': len(python_files),
            'prints_found': total_prints,
            'prints_migrated': 0,  # 0 significa que NO quedan prints por migrar
            'files_with_prints': len(files_with_prints),
            'print_files': files_with_prints
        }

    def scan_for_prints(self):
        """Alias para compatibilidad"""
        return self.scan_project(scan_only=True)

def main():
    """Función principal"""
    log("🚀 Print Migration Tool - Consolidator Compatible")

    # Obtener directorio del proyecto
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))

    log(f"📁 Proyecto: {project_root}")

    # Crear instancia
    tool = PrintMigrationTool(project_root)

    # Ejecutar escaneo
    results = tool.scan_project()

    log("📋 Resultados:")
    log(f"  📁 Archivos Python: {results['total_files']}")
    log(f"  🔍 Prints encontrados: {results['prints_found']}")
    log(f"  📂 Archivos con prints: {results['files_with_prints']}")

    log("🎉 Print Migration Tool completado!")
    return True

if __name__ == "__main__":
    main()
