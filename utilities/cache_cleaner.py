#!/usr/bin/env python3
"""
🧹 CACHE CLEANER - Limpieza Completa de Cache del Sistema

Script para limpiar todos los tipos de cache que pueden interferir
con el análisis de tipos y la compilación de Python.

Versión: v1.0.0
Fecha: 03 Agosto 2025
"""

import os
import shutil
import sys
from pathlib import Path

def clear_python_cache():
    """Limpia cache de Python (.pyc, __pycache__)"""
    print("🗑️  Limpiando cache de Python...")

    cache_dirs = []
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dirs.append(os.path.join(root, '__pycache__'))

    for cache_dir in cache_dirs:
        try:
            shutil.rmtree(cache_dir)
            print(f"   ✅ Eliminado: {cache_dir}")
        except Exception as e:
            print(f"   ❌ Error eliminando {cache_dir}: {e}")

    print(f"🔄 Eliminados {len(cache_dirs)} directorios de cache")

def clear_type_checker_cache():
    """Limpia cache de type checkers (mypy, pylance)"""
    print("🔍 Limpiando cache de type checkers...")

    type_cache_patterns = ['.mypy_cache', '.pylance_cache', '.pyright_cache']

    for pattern in type_cache_patterns:
        for cache_dir in Path('.').rglob(pattern):
            try:
                if cache_dir.is_dir():
                    shutil.rmtree(cache_dir)
                    print(f"   ✅ Eliminado: {cache_dir}")
            except Exception as e:
                print(f"   ❌ Error eliminando {cache_dir}: {e}")

def recompile_python_files():
    """Recompila archivos Python para refrescar bytecode"""
    print("🔄 Recompilando archivos Python...")

    import compileall
    try:
        compileall.compile_dir('.', force=True, quiet=1)
        print("   ✅ Recompilación completada")
    except Exception as e:
        print(f"   ❌ Error en recompilación: {e}")

def main():
    """Función principal de limpieza"""
    print("=" * 60)
    print("🧹 INICIANDO LIMPIEZA COMPLETA DE CACHE")
    print("=" * 60)

    clear_python_cache()
    print()
    clear_type_checker_cache()
    print()
    recompile_python_files()

    print()
    print("=" * 60)
    print("✅ LIMPIEZA DE CACHE COMPLETADA")
    print("=" * 60)
    print()
    print("📝 RECOMENDACIONES POST-LIMPIEZA:")
    print("   1. Reiniciar VS Code (Ctrl+Shift+P -> 'Developer: Reload Window')")
    print("   2. Esperar 30-60 segundos para que Pylance recargue")
    print("   3. Verificar errores de tipo nuevamente")
    print()

if __name__ == "__main__":
    main()
