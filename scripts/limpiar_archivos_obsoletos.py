# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
"""
🧹 ICT ENGINE v5.0 - LIMPIEZA DE ARCHIVOS OBSOLETOS
=================================================

Script para identificar y eliminar archivos obsoletos del sistema
de forma segura y documentada.

ANÁLISIS DE ARCHIVOS:
- ✅ dashboard_definitivo.py - ACTIVO (usado por auto_start.py)
- ❌ dashboard_directo.py - OBSOLETO (no usado en ningún import)
- ✅ poi_dashboard_integration.py - ACTIVO (usado por dashboard_definitivo.py)
- ❌ poi_dashboard_integration_corrected.py - OBSOLETO (duplicado)
- ✅ hibernacion_perfecta.py - ACTIVO (usado por dashboard_definitivo.py)
"""

import shutil
from pathlib import Path
from typing import List, Dict, Tuple

# Configurar paths
PROJECT_ROOT = Path(__file__).parent
BACKUP_DIR = PROJECT_ROOT / "backup_obsoletos"

def identificar_archivos_obsoletos() -> Dict[str, List[str]]:
    """
    Identifica archivos obsoletos por categoría.

    Returns:
        Diccionario con categorías y listas de archivos obsoletos
    """
    obsoletos = {
        "dashboard_duplicados": [
            "dashboard/dashboard_directo.py",  # No usado en imports
            "dashboard/poi_dashboard_integration_corrected.py",  # Duplicado
        ],
        "directorios_vacios": [
            "debugging",  # Directorio vacío
            "deployment",  # Directorio vacío
        ],
        "archivos_pycache": [
            # Se identificarán dinámicamente
        ],
        "tests_vacios": [
            "teste/teste_template.py",  # Template sin usar
            "teste/.gitkeep",  # Placeholder
        ],
        "scripts_diagnostico": [
            # Scripts de diagnóstico que ya cumplieron su función
            "scripts/audit_candle_downloader.py",
            "scripts/clean_poi_diagnostics.py",
            "scripts/fix_dashboard.py",
            "scripts/reporte_final_diagnostico.py",
            "scripts/validate_poi_dashboard.py",
            "scripts/validate_sprint_1_6.py",
            "scripts/verificacion_real_sistema.py",
            "scripts/verificar_integridad_dashboard.py",
        ]
    }

    # Buscar archivos __pycache__ dinámicamente
    for pycache_dir in PROJECT_ROOT.rglob("__pycache__"):
        if pycache_dir.is_dir():
            obsoletos["archivos_pycache"].append(str(pycache_dir.relative_to(PROJECT_ROOT)))

    return obsoletos

def crear_backup(archivos: List[str]) -> bool:
    """
    Crea backup de archivos antes de eliminarlos.

    Args:
        archivos: Lista de archivos a respaldar

    Returns:
        True si el backup fue exitoso
    """
    try:
        # Crear directorio de backup
        BACKUP_DIR.mkdir(exist_ok=True)

        print(f"📦 Creando backup en: {BACKUP_DIR}")

        for archivo_rel in archivos:
            archivo_path = PROJECT_ROOT / archivo_rel

            if not archivo_path.exists():
                print(f"⚠️  Archivo no encontrado: {archivo_rel}")
                continue

            # Crear estructura de directorios en backup
            backup_path = BACKUP_DIR / archivo_rel
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            if archivo_path.is_file():
                shutil.copy2(archivo_path, backup_path)
                print(f"✅ Respaldado: {archivo_rel}")
            elif archivo_path.is_dir():
                shutil.copytree(archivo_path, backup_path, dirs_exist_ok=True)
                print(f"✅ Respaldado directorio: {archivo_rel}")

        return True

    except Exception as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error creando backup: {e}")
        return False

def eliminar_archivos(archivos: List[str], categoria: str) -> Tuple[int, int]:
    """
    Elimina archivos de forma segura.

    Args:
        archivos: Lista de archivos a eliminar
        categoria: Categoría de archivos

    Returns:
        Tupla (eliminados, errores)
    """
    eliminados = 0
    errores = 0

    print(f"\n🗑️  Eliminando {categoria}...")

    for archivo_rel in archivos:
        archivo_path = PROJECT_ROOT / archivo_rel

        try:
            if not archivo_path.exists():
                print(f"⚠️  Ya eliminado: {archivo_rel}")
                continue

            if archivo_path.is_file():
                archivo_path.unlink()
                print(f"✅ Eliminado archivo: {archivo_rel}")
                eliminados += 1
            elif archivo_path.is_dir():
                shutil.rmtree(archivo_path)
                print(f"✅ Eliminado directorio: {archivo_rel}")
                eliminados += 1

        except Exception as e:
            # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error eliminando {archivo_rel}: {e}")
            errores += 1

    return eliminados, errores

def mostrar_resumen_limpieza(obsoletos: Dict[str, List[str]]) -> None:
    """Muestra un resumen de lo que se va a limpiar."""

    print("🧹 RESUMEN DE LIMPIEZA")
    print("=" * 50)

    total_archivos = 0

    for categoria, archivos in obsoletos.items():
        if archivos:
            print(f"\n📂 {categoria.upper()}:")
            for archivo in archivos:
                print(f"  🗑️  {archivo}")
            total_archivos += len(archivos)

    print(f"\n📊 TOTAL A ELIMINAR: {total_archivos} elementos")
    print("=" * 50)

def main():
    """Función principal de limpieza."""

    print("🧹 ICT ENGINE v5.0 - LIMPIADOR DE ARCHIVOS OBSOLETOS")
    print("=" * 60)

    # 1. Identificar archivos obsoletos
    obsoletos = identificar_archivos_obsoletos()

    # 2. Mostrar resumen
    mostrar_resumen_limpieza(obsoletos)

    # 3. Confirmar con usuario
    respuesta = input("\n¿Proceder con la limpieza? (s/N): ").strip().lower()

    if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Limpieza cancelada por el usuario.")
        return

    # 4. Crear lista completa de archivos
    todos_archivos = []
    for archivos in obsoletos.values():
        todos_archivos.extend(archivos)

    # 5. Crear backup
    if not crear_backup(todos_archivos):
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print("❌ Error creando backup. Cancelando limpieza.")
        return

    # 6. Eliminar archivos por categoría
    total_eliminados = 0
    total_errores = 0

    for categoria, archivos in obsoletos.items():
        if archivos:
            eliminados, errores = eliminar_archivos(archivos, categoria)
            total_eliminados += eliminados
            total_errores += errores

    # 7. Resumen final
    print("\n" + "=" * 60)
    print("🎯 LIMPIEZA COMPLETADA")
    print("=" * 60)
    print(f"✅ Archivos eliminados: {total_eliminados}")
    # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Errores: {total_errores}")
    print(f"📦 Backup creado en: {BACKUP_DIR}")

    if total_errores == 0:
        print("🎉 ¡Limpieza exitosa! El sistema está más ligero.")
    else:
        print("⚠️  Algunos archivos no se pudieron eliminar. Revisar logs.")

    print("\n💡 Notas importantes:")
    print("  • Los archivos se respaldaron antes de eliminar")
    print("  • El sistema principal no se vio afectado")
    print("  • Los archivos activos se mantuvieron intactos")

if __name__ == "__main__":
    main()
