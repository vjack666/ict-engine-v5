#!/usr/bin/env python3
"""
🧹 LIMPIADOR DE BACKUPS - Post Validación
========================================
Elimina archivos backup después de validar que todo funciona

Autor: ITC Engine v5.0
Fecha: 2025-08-06
"""

import os
import sys
from pathlib import Path

# Configurar path del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from sistema.sic import enviar_senal_log

def encontrar_archivos_backup(directorio_base: Path) -> list:
    """Encuentra todos los archivos backup en el proyecto."""
    archivos_backup = []

    # Patrones de backup
    patrones = [".backup", ".old", ".bak", "_backup"]

    for root, dirs, files in os.walk(directorio_base):
        for file in files:
            if any(patron in file for patron in patrones):
                archivo_path = Path(root) / file
                archivos_backup.append(archivo_path)

    return archivos_backup

def encontrar_directorios_backup(directorio_base: Path) -> list:
    """Encuentra directorios de backup."""
    dirs_backup = []

    patrones_dir = ["backup_", "temp_", "_backup"]

    for item in directorio_base.iterdir():
        if item.is_dir() and any(patron in item.name for patron in patrones_dir):
            dirs_backup.append(item)

    return dirs_backup

def eliminar_backups_seguros():
    """Elimina backups de forma segura después de confirmación."""
    base_path = Path(project_root)

    print("🧹 LIMPIADOR DE BACKUPS - ITC Engine v5.0")
    print("=" * 50)

    # Encontrar archivos backup
    archivos_backup = encontrar_archivos_backup(base_path)
    directorios_backup = encontrar_directorios_backup(base_path)

    print(f"📁 Archivos backup encontrados: {len(archivos_backup)}")
    print(f"📂 Directorios backup encontrados: {len(directorios_backup)}")

    if not archivos_backup and not directorios_backup:
        print("✅ No hay archivos backup para eliminar")
        return

    # Mostrar lista
    print("\n📋 ARCHIVOS BACKUP A ELIMINAR:")
    for archivo in archivos_backup[:10]:  # Mostrar solo los primeros 10
        size_mb = archivo.stat().st_size / (1024 * 1024)
        print(f"  📄 {archivo.relative_to(base_path)} ({size_mb:.2f} MB)")

    if len(archivos_backup) > 10:
        print(f"  ... y {len(archivos_backup) - 10} archivos más")

    print("\n📂 DIRECTORIOS BACKUP A ELIMINAR:")
    for directorio in directorios_backup:
        try:
            size_mb = sum(f.stat().st_size for f in directorio.rglob('*') if f.is_file()) / (1024 * 1024)
            print(f"  📂 {directorio.relative_to(base_path)} ({size_mb:.2f} MB)")
        except:
            print(f"  📂 {directorio.relative_to(base_path)} (tamaño no disponible)")

    # Calcular espacio total
    total_size = 0
    try:
        for archivo in archivos_backup:
            total_size += archivo.stat().st_size
        for directorio in directorios_backup:
            total_size += sum(f.stat().st_size for f in directorio.rglob('*') if f.is_file())
        print(f"\n💾 Espacio total a liberar: {total_size / (1024 * 1024):.2f} MB")
    except:
        print("\n💾 Espacio total: No calculable")

    # Confirmación
    print("\n⚠️ CONFIRMACIÓN REQUERIDA:")
    print("Esta operación eliminará PERMANENTEMENTE todos los archivos backup.")
    print("Solo proceder si la validación fue exitosa.")

    respuesta = input("¿Eliminar todos los backups? (escriba 'ELIMINAR' para confirmar): ")

    if respuesta != "ELIMINAR":
        print("❌ Operación cancelada")
        return

    # Eliminar archivos
    eliminados = 0
    errores = 0

    print("\n🧹 Eliminando archivos backup...")
    for archivo in archivos_backup:
        try:
            archivo.unlink()
            eliminados += 1
            if eliminados % 10 == 0:
                print(f"  ✅ {eliminados} archivos eliminados...")
        except Exception as e:
            errores += 1
            print(f"  ❌ Error eliminando {archivo.name}: {e}")

    print("\n🧹 Eliminando directorios backup...")
    for directorio in directorios_backup:
        try:
            import shutil
            shutil.rmtree(directorio)
            eliminados += 1
            print(f"  ✅ Directorio eliminado: {directorio.name}")
        except Exception as e:
            errores += 1
            print(f"  ❌ Error eliminando {directorio.name}: {e}")

    # Resumen
    print(f"\n🎉 LIMPIEZA COMPLETADA:")
    print(f"✅ Elementos eliminados: {eliminados}")
    if errores > 0:
        print(f"❌ Errores: {errores}")
    else:
        print("✅ Sin errores")

    # Log final
    enviar_senal_log("INFO", f"Limpieza de backups completada: {eliminados} elementos eliminados", "backup_cleaner", "cleanup")
    print("💾 Espacio en disco liberado exitosamente")

if __name__ == "__main__":
    try:
        eliminar_backups_seguros()
    except KeyboardInterrupt:
        print("\n❌ Operación interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error en limpieza: {e}")
        enviar_senal_log("ERROR", f"Error en limpieza de backups: {e}", "backup_cleaner", "error")
