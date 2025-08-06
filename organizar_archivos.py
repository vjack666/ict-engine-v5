#!/usr/bin/env python3
"""
🗂️ ORGANIZADOR DE ARCHIVOS DEL PROYECTO
=====================================

Script para reorganizar archivos del directorio raíz en sus carpetas correspondientes
"""

from sistema.sic import os
import shutil
from sistema.sic import Path

def main():
    print("🗂️ ORGANIZANDO ARCHIVOS DEL PROYECTO")
    print("=" * 50)

    # Directorio base
    base_dir = Path(".")

    # Definir categorías y destinos
    organizacion = {
        # DOCUMENTACIÓN
        "docs/": [
            "ANALISIS_SUBPROCESS_COMPLETO.md",
            "README.md",
            "REPORTE_SCRIPTS_INDISPENSABLES.md"
        ],

        # SCRIPTS DE ANÁLISIS Y HERRAMIENTAS
        "scripts/": [
            "analizar_scripts_indispensables.py",
            "check_subprocess_imports.py"
        ],

        # HERRAMIENTAS DE DESARROLLO
        "utilities/debug/": [
            "detector_logs_rapido.py",
            "limpiar_logs_obsoletos.py",
            "reporte_final_logs.py"
        ],

        # HERRAMIENTAS DE MIGRACIÓN
        "utilities/migration/": [
            "migrate_sluc_atomic.py"
        ],

        # TESTS
        "teste/": [
            "test_dashboard_poi.py",
            "test_hibernation_widget.py",
            "test_poi_integration.py",
            "simple_test.py"
        ],

        # LAUNCHERS Y STARTERS (mantener en raíz)
        "./": [
            "main.py",
            "auto_start.py",
            "launch_dashboard.py",
            "START_ICT_ENGINE.bat",
            "START_ICT_ENGINE.ps1",
            "requirements.txt"
        ]
    }

    # Crear directorios si no existen
    for destino in organizacion.keys():
        if destino != "./":
            dest_path = base_dir / destino
            dest_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Directorio asegurado: {destino}")

    # Mover archivos
    movidos = 0
    for destino, archivos in organizacion.items():
        print(f"\n📂 Organizando en {destino}:")

        for archivo in archivos:
            archivo_path = base_dir / archivo
            destino_path = base_dir / destino / archivo

            if archivo_path.exists():
                if destino == "./":
                    print(f"   ⚡ {archivo} - MANTENER EN RAÍZ")
                else:
                    try:
                        # Si el archivo ya existe en destino, crear backup
                        if destino_path.exists():
                            backup_path = destino_path.with_suffix(destino_path.suffix + ".backup")
                            shutil.move(str(destino_path), str(backup_path))
                            print(f"   📋 Backup creado: {backup_path.name}")

                        shutil.move(str(archivo_path), str(destino_path))
                        print(f"   ✅ {archivo} → {destino}")
                        movidos += 1
                    except Exception as e:
                        print(f"   ❌ Error moviendo {archivo}: {e}")
            else:
                print(f"   ⚠️ {archivo} - NO ENCONTRADO")

    print(f"\n📊 RESUMEN:")
    print(f"   📦 Archivos movidos: {movidos}")
    print(f"   🏠 Archivos en raíz: {len(organizacion.get('./', []))}")
    print(f"\n✅ ORGANIZACIÓN COMPLETADA")

    # Mostrar estructura final
    print(f"\n📋 ESTRUCTURA FINAL:")
    for destino, archivos in organizacion.items():
        if destino != "./":
            print(f"   📁 {destino}")
            for archivo in archivos:
                destino_path = base_dir / destino / archivo
                estado = "✅" if destino_path.exists() else "❌"
                print(f"      {estado} {archivo}")

    print(f"\n   📁 RAÍZ DEL PROYECTO:")
    for archivo in organizacion.get("./", []):
        archivo_path = base_dir / archivo
        estado = "✅" if archivo_path.exists() else "❌"
        print(f"      {estado} {archivo}")

if __name__ == "__main__":
    main()
