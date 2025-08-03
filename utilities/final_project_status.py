#!/usr/bin/env python3
"""
📋 ESTADO FINAL DEL PROYECTO - ICT Engine v5.0
==============================================

Generador de reporte consolidado del estado actual del proyecto
después de la limpieza completa.
"""

import os
from pathlib import Path
from datetime import datetime
import json

PROJECT_ROOT = Path(__file__).parent.parent

def count_files_by_type():
    """Cuenta archivos por tipo"""
    counts = {
        'python': 0,
        'markdown': 0,
        'json': 0,
        'total': 0
    }

    for file_path in PROJECT_ROOT.rglob("*"):
        if file_path.is_file() and "__pycache__" not in str(file_path):
            counts['total'] += 1

            if file_path.suffix == '.py':
                counts['python'] += 1
            elif file_path.suffix == '.md':
                counts['markdown'] += 1
            elif file_path.suffix == '.json':
                counts['json'] += 1

    return counts

def get_directory_structure():
    """Obtiene estructura de directorios principales"""
    main_dirs = []
    for item in PROJECT_ROOT.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name != '__pycache__':
            python_count = len(list(item.rglob("*.py")))
            main_dirs.append({
                'name': item.name,
                'python_files': python_count
            })

    return sorted(main_dirs, key=lambda x: x['python_files'], reverse=True)

def check_critical_files():
    """Verifica que archivos críticos existan"""
    critical_files = [
        'main.py',
        'utils/mt5_data_manager.py',
        'dashboard/dashboard_definitivo.py',
        'sistema/logging_interface.py',
        'config/config_manager.py',
        'requirements.txt',
        'README.md'
    ]

    status = {}
    for file_path in critical_files:
        full_path = PROJECT_ROOT / file_path
        status[file_path] = full_path.exists()

    return status

def generate_final_report():
    """Genera reporte final consolidado"""
    timestamp = datetime.now()

    # Recopilar datos
    file_counts = count_files_by_type()
    dir_structure = get_directory_structure()
    critical_status = check_critical_files()

    # Generar reporte
    report = {
        'timestamp': timestamp.isoformat(),
        'project_name': 'ICT Engine v5.0',
        'cleanup_status': 'COMPLETED',
        'file_statistics': file_counts,
        'directory_structure': dir_structure,
        'critical_files_status': critical_status,
        'summary': {
            'total_files': file_counts['total'],
            'python_modules': file_counts['python'],
            'documentation_files': file_counts['markdown'],
            'all_critical_files_present': all(critical_status.values()),
            'main_directories': len(dir_structure)
        }
    }

    return report

def print_final_status():
    """Imprime estado final del proyecto"""
    report = generate_final_report()

    print("=" * 70)
    print("🎯 ESTADO FINAL DEL PROYECTO - ICT Engine v5.0")
    print("=" * 70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🧹 Estado de limpieza: {report['cleanup_status']}")
    print()

    print("📊 ESTADÍSTICAS DE ARCHIVOS:")
    stats = report['file_statistics']
    print(f"  📁 Total archivos: {stats['total']}")
    print(f"  🐍 Archivos Python: {stats['python']}")
    print(f"  📝 Archivos Markdown: {stats['markdown']}")
    print(f"  📋 Archivos JSON: {stats['json']}")
    print()

    print("🏗️ ESTRUCTURA DE DIRECTORIOS PRINCIPALES:")
    for dir_info in report['directory_structure'][:8]:  # Top 8
        print(f"  📂 {dir_info['name']:<20} - {dir_info['python_files']} archivos Python")
    print()

    print("🛡️ ARCHIVOS CRÍTICOS:")
    all_critical_ok = True
    for file_path, exists in report['critical_files_status'].items():
        status = "✅" if exists else "❌"
        print(f"  {status} {file_path}")
        if not exists:
            all_critical_ok = False
    print()

    print("🎉 RESUMEN:")
    summary = report['summary']
    print(f"  📁 {summary['total_files']} archivos totales")
    print(f"  🐍 {summary['python_modules']} módulos Python")
    print(f"  📂 {summary['main_directories']} directorios principales")

    if all_critical_ok:
        print("  ✅ Todos los archivos críticos presentes")
        print("  🚀 Proyecto listo para desarrollo/producción")
    else:
        print("  ⚠️ Algunos archivos críticos faltantes")

    print("=" * 70)
    print("✨ PROYECTO ICT ENGINE v5.0 - LIMPIEZA COMPLETADA")
    print("=" * 70)

    # Guardar reporte JSON
    output_path = PROJECT_ROOT / "docs" / "reports" / f"final_project_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"📊 Reporte completo guardado en: {output_path}")

    return report

if __name__ == "__main__":
    print_final_status()
