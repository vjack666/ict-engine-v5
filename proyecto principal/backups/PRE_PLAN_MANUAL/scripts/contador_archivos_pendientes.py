#!/usr/bin/env python3
"""
📊 CONTADOR DE ARCHIVOS PENDIENTES - Post Migración
=================================================
Cuenta exactamente cuántos archivos faltan por migrar al SIC v3.0
"""

import os
import sys
import re
from pathlib import Path

# Configurar path del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from sistema.sic import enviar_senal_log

def analizar_archivos_pendientes():
    """Analiza archivos que faltan por migrar."""

    # Directorios principales a evaluar
    directorios_principales = [
        "core/",
        "dashboard/",
        "utils/",
        "utilities/",
        "teste/",
        "scripts/"
    ]

    # Archivos del sistema que están correctos (ignorar)
    archivos_sistema = {
        "sic.py", "sic_v3_limpio.py", "logging_interface.py",
        "smart_directory_logger.py", "__init__.py",
        "migrador_masivo_paquetes.py", "validador_final_proyecto.py",
        "limpiador_backups.py", "contador_archivos_pendientes.py"
    }

    # Patterns que indican que un archivo necesita migración
    patterns_necesitan_migracion = [
        r'^\s*import\s+logging\s*$',
        r'^\s*from\s+logging\s+import',
        r'logging\.getLogger',
        r'logger\.(debug|info|warning|error|critical)',
        r'logging\.(debug|info|warning|error|critical)'
    ]

    archivos_pendientes = []
    archivos_migrados = []
    archivos_evaluados = 0

    print("📊 ANÁLISIS DE ARCHIVOS PENDIENTES DE MIGRACIÓN")
    print("=" * 60)

    for directorio in directorios_principales:
        dir_path = Path(project_root) / directorio
        if not dir_path.exists():
            continue

        print(f"\n📁 Analizando {directorio}")

        for archivo_py in dir_path.rglob("*.py"):
            if archivo_py.name in archivos_sistema:
                continue

            archivos_evaluados += 1

            try:
                with open(archivo_py, 'r', encoding='utf-8') as f:
                    contenido = f.read()

                # Verificar si necesita migración
                necesita_migracion = False
                problemas_encontrados = []

                for pattern in patterns_necesitan_migracion:
                    if re.search(pattern, contenido, re.MULTILINE):
                        necesita_migracion = True
                        problemas_encontrados.append(pattern)

                # Verificar si ya tiene import del SIC
                tiene_sic = bool(re.search(r'from\s+sistema\.sic\s+import', contenido))

                archivo_relativo = archivo_py.relative_to(Path(project_root))

                if necesita_migracion and not tiene_sic:
                    archivos_pendientes.append({
                        'archivo': str(archivo_relativo),
                        'problemas': problemas_encontrados,
                        'tamaño_kb': archivo_py.stat().st_size / 1024
                    })
                    print(f"  ❌ {archivo_py.name}")
                elif tiene_sic:
                    archivos_migrados.append(str(archivo_relativo))
                    print(f"  ✅ {archivo_py.name}")
                else:
                    # No necesita migración (no usa logging)
                    print(f"  ➖ {archivo_py.name} (sin logging)")

            except Exception as e:
                print(f"  ⚠️ Error leyendo {archivo_py.name}: {e}")

    # Resumen
    print(f"\n" + "=" * 60)
    print(f"📊 RESUMEN FINAL")
    print(f"=" * 60)
    print(f"📁 Archivos evaluados: {archivos_evaluados}")
    print(f"✅ Archivos migrados: {len(archivos_migrados)}")
    print(f"❌ Archivos pendientes: {len(archivos_pendientes)}")
    print(f"📈 Progreso: {(len(archivos_migrados) / (len(archivos_migrados) + len(archivos_pendientes)) * 100):.1f}%")

    if archivos_pendientes:
        print(f"\n📋 ARCHIVOS PENDIENTES DE MIGRACIÓN:")
        for i, archivo_info in enumerate(archivos_pendientes, 1):
            print(f"{i:2d}. {archivo_info['archivo']} ({archivo_info['tamaño_kb']:.1f} KB)")

        # Calcular prioridades
        archivos_core = [a for a in archivos_pendientes if 'core/' in a['archivo']]
        archivos_dashboard = [a for a in archivos_pendientes if 'dashboard/' in a['archivo']]
        archivos_utils = [a for a in archivos_pendientes if 'utils/' in a['archivo']]

        print(f"\n🎯 DISTRIBUCIÓN POR PRIORIDAD:")
        print(f"🔥 Core (alta prioridad): {len(archivos_core)} archivos")
        print(f"📊 Dashboard (media prioridad): {len(archivos_dashboard)} archivos")
        print(f"🛠️ Utils (baja prioridad): {len(archivos_utils)} archivos")

        if archivos_core:
            print(f"\n🔥 ARCHIVOS CORE PENDIENTES (alta prioridad):")
            for archivo_info in archivos_core[:5]:
                print(f"   - {archivo_info['archivo']}")

    # Log final
    enviar_senal_log("INFO",
        f"Análisis pendientes: {len(archivos_pendientes)} archivos faltan, {len(archivos_migrados)} migrados",
        "contador_pendientes", "analysis")

    return {
        'evaluados': archivos_evaluados,
        'migrados': len(archivos_migrados),
        'pendientes': len(archivos_pendientes),
        'archivos_pendientes': archivos_pendientes
    }

if __name__ == "__main__":
    try:
        resultado = analizar_archivos_pendientes()
        print(f"\n✅ Análisis completado")
        print(f"💡 Para migrar los archivos restantes, ejecuta el migrador en modo específico")
    except Exception as e:
        print(f"❌ Error en análisis: {e}")
        enviar_senal_log("ERROR", f"Error en contador pendientes: {e}", "contador_pendientes", "error")
