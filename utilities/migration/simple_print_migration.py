"""
Print Migration Tool - Ultra Simple Version
"""
import os
import re
from pathlib import Path
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def scan_prints(project_root):
    """Escanea prints en archivos Python"""
    log("🔍 Escaneando prints...")

    python_files = []
    for root, dirs, files in os.walk(project_root):
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

    log(f"✅ Escaneo completado:")
    log(f"  📁 Archivos Python: {len(python_files)}")
    log(f"  🔍 Prints encontrados: {total_prints}")
    log(f"  📂 Archivos con prints: {len(files_with_prints)}")

    # Mostrar algunos archivos con prints
    if files_with_prints:
        log("📋 Archivos con prints (primeros 10):")
        for file_path in files_with_prints[:10]:
            rel_path = os.path.relpath(file_path, project_root)
            log(f"  - {rel_path}")

        if len(files_with_prints) > 10:
            log(f"  ... y {len(files_with_prints) - 10} más")

    return {
        'total_files': len(python_files),
        'total_prints': total_prints,
        'files_with_prints': len(files_with_prints),
        'print_files': files_with_prints
    }

def migrate_prints_dry_run(project_root):
    """Simula migración de prints"""
    log("🚀 Simulando migración de prints...")

    result = scan_prints(project_root)

    if result['total_prints'] == 0:
        log("✅ No hay prints para migrar")
        return True

    log("📝 Migración simulada:")
    log(f"  🔄 {result['total_prints']} prints serían migrados")
    log(f"  📁 En {result['files_with_prints']} archivos")
    log("  🔧 Conversión: print() → enviar_senal_log()")

    # Simular que la migración fue exitosa
    log("✅ Migración simulada completada exitosamente")
    return True

def main():
    """Función principal"""
    log("🚀 Print Migration Tool - Ultra Simple")

    # Obtener directorio del proyecto
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))

    log(f"📁 Proyecto: {project_root}")

    # Ejecutar migración simulada
    success = migrate_prints_dry_run(project_root)

    if success:
        log("🎉 Print Migration Tool completado exitosamente!")
        return True
    else:
        log("❌ Print Migration Tool falló")
        return False

if __name__ == "__main__":
    main()
