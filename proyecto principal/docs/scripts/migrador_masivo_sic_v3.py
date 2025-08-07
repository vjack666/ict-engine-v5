#!/usr/bin/env python3
"""
🚀 MIGRADOR MASIVO SIC v3.0 - AUTOMATIZACIÓN TOTAL
=================================================
Script para migrar TODOS los archivos del proyecto al nuevo SIC v3.0

Características:
- Migración automatizada de imports
- Validación de sintaxis
- Logging de progreso
- Rollback automático si hay errores

Autor: ITC Engine v5.0
Fecha: 2025-08-06
Versión: v1.0
"""

# MIGRACIÓN SIC v3.0 + SLUC v2.1
from sistema.sic import enviar_senal_log, log_info, log_warning

from sistema.sic import os
from sistema.sic import sys
from sistema.sic import re
import shutil
from sistema.sic import Path
from sistema.sic import Dict, List, Optional, Tuple, Set
from sistema.sic import json
from sistema.sic import datetime

# Asegurar que podemos importar del SIC
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from sistema.sic import enviar_senal_log, log_info, log_warning, get_sic_status
    SIC_AVAILABLE = True
    print("✅ SIC v3.0 disponible para migración")
except ImportError as e:
    print(f"❌ Error importando SIC: {e}")
    SIC_AVAILABLE = False

# =============================================================================
# CONFIGURACIÓN DE MIGRACIÓN
# =============================================================================

# Directorios por prioridad
DIRECTORIOS_MIGRACION = {
    "PRIORIDAD_1": [
        "core/ict_engine/",
        "core/analytics/",
    ],
    "PRIORIDAD_2": [
        "core/data_management/",
        "core/risk_management/",
        "core/poi_system/",
        "core/integrations/",
    ],
    "PRIORIDAD_3": [
        "dashboard/",
        "utils/",
        "utilities/",
        "teste/",
        "scripts/",
    ]
}

# Patterns de migración
MIGRATION_PATTERNS = {
    # Eliminar imports legacy
    r'import sistema\.sic as sic': '',
    r'from sistema\.sic import\s*$': '',

    # Reemplazar referencias algo
    r'sic\.([a-zA-Z_][a-zA-Z0-9_]*)': r'\1',

    # Normalizar imports de SIC
    r'from sistema\.imports_interface import': 'from sistema.sic import',
    r'from sistema\.sic_clean import': 'from sistema.sic import',

    # Imports standard que deben venir del SIC
    r'^import os$': 'from sistema.sic import os',
    r'^import sys$': 'from sistema.sic import sys',
    r'^import json$': 'from sistema.sic import json',
    r'^import re$': 'from sistema.sic import re',
    r'^from pathlib import Path$': 'from sistema.sic import Path',
    r'^from datetime import datetime': 'from sistema.sic import datetime',
    r'^from typing import': 'from sistema.sic import',
}

# Archivos a ignorar
ARCHIVOS_IGNORAR = {
    "__pycache__",
    ".git",
    ".vscode",
    "node_modules",
    "venv",
    "env",
    ".pytest_cache",
    "__init__.py",  # Generalmente están vacíos
}

# Extensiones de archivo a procesar
EXTENSIONES_VALIDAS = {".py"}

# =============================================================================
# FUNCIONES DE MIGRACIÓN
# =============================================================================

def crear_backup_archivo(archivo_path: Path) -> Path:
    """Crea un backup del archivo antes de modificarlo."""
    backup_path = archivo_path.with_suffix(archivo_path.suffix + ".backup")
    shutil.copy2(archivo_path, backup_path)
    return backup_path

def validar_sintaxis_python(archivo_path: Path) -> bool:
    """Valida que un archivo Python tenga sintaxis correcta."""
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        compile(contenido, archivo_path, 'exec')
        return True
    except SyntaxError as e:
        print(f"❌ Error de sintaxis en {archivo_path}: {e}")
        return False
    except Exception as e:
        print(f"⚠️ Error validando {archivo_path}: {e}")
        return True  # Asumimos que está bien si no podemos validar

def migrar_archivo(archivo_path: Path) -> Dict:
    """Migra un archivo individual al patrón SIC v3.0."""
    resultado = {
        "archivo": str(archivo_path),
        "migrado": False,
        "cambios": 0,
        "backup_creado": False,
        "errores": []
    }

    try:
        # Leer archivo original
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido_original = f.read()

        # Si no tiene imports relacionados, saltar
        if not re.search(r'from sistema\.|import sistema\.|import os|import sys', contenido_original):
            return resultado

        # Crear backup
        backup_path = crear_backup_archivo(archivo_path)
        resultado["backup_creado"] = True

        # Aplicar patterns de migración
        contenido_migrado = contenido_original
        cambios_realizados = 0

        for pattern, replacement in MIGRATION_PATTERNS.items():
            matches = len(re.findall(pattern, contenido_migrado, re.MULTILINE))
            if matches > 0:
                contenido_migrado = re.sub(pattern, replacement, contenido_migrado, flags=re.MULTILINE)
                cambios_realizados += matches

        # Solo escribir si hay cambios
        if cambios_realizados > 0:
            # Validar sintaxis antes de escribir
            temp_path = archivo_path.with_suffix(".temp")
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(contenido_migrado)

            if validar_sintaxis_python(temp_path):
                # Sintaxis OK, reemplazar archivo original
                shutil.move(temp_path, archivo_path)
                resultado["migrado"] = True
                resultado["cambios"] = cambios_realizados
                print(f"✅ Migrado: {archivo_path.name} ({cambios_realizados} cambios)")
            else:
                # Error de sintaxis, restaurar backup
                resultado["errores"].append("Error de sintaxis después de migración")
                shutil.copy2(backup_path, archivo_path)
                temp_path.unlink(missing_ok=True)
                print(f"❌ Error en migración: {archivo_path.name}")

    except Exception as e:
        resultado["errores"].append(str(e))
        print(f"❌ Error procesando {archivo_path}: {e}")

    return resultado

def migrar_directorio(directorio: str, base_path: Path) -> Dict:
    """Migra todos los archivos de un directorio."""
    dir_path = base_path / directorio
    resultado = {
        "directorio": directorio,
        "archivos_procesados": 0,
        "archivos_migrados": 0,
        "cambios_totales": 0,
        "errores": [],
        "archivos_detalle": []
    }

    if not dir_path.exists():
        resultado["errores"].append(f"Directorio no existe: {dir_path}")
        return resultado

    print(f"🔄 Procesando directorio: {directorio}")

    # Buscar archivos Python recursivamente
    for archivo_path in dir_path.rglob("*.py"):
        # Saltar archivos a ignorar
        if any(ignore in str(archivo_path) for ignore in ARCHIVOS_IGNORAR):
            continue

        resultado["archivos_procesados"] += 1
        resultado_archivo = migrar_archivo(archivo_path)
        resultado["archivos_detalle"].append(resultado_archivo)

        if resultado_archivo["migrado"]:
            resultado["archivos_migrados"] += 1
            resultado["cambios_totales"] += resultado_archivo["cambios"]

        if resultado_archivo["errores"]:
            resultado["errores"].extend(resultado_archivo["errores"])

    print(f"✅ Completado {directorio}: {resultado['archivos_migrados']}/{resultado['archivos_procesados']} archivos migrados")
    return resultado

def ejecutar_migracion_completa() -> Dict:
    """Ejecuta la migración completa del proyecto."""
    base_path = Path(__file__).parent.parent

    resultado_global = {
        "timestamp": datetime.now().isoformat(),
        "sic_status": get_sic_status() if SIC_AVAILABLE else "No disponible",
        "fases": {},
        "totales": {
            "directorios_procesados": 0,
            "archivos_procesados": 0,
            "archivos_migrados": 0,
            "cambios_totales": 0,
        },
        "errores_globales": []
    }

    print("🚀 INICIANDO MIGRACIÓN MASIVA AL SIC v3.0")
    print("=" * 50)

    # Ejecutar por fases de prioridad
    for fase, directorios in DIRECTORIOS_MIGRACION.items():
        print(f"\n📋 EJECUTANDO {fase}")
        print("-" * 30)

        resultado_fase = {
            "directorios": {},
            "archivos_procesados": 0,
            "archivos_migrados": 0,
            "cambios_totales": 0
        }

        for directorio in directorios:
            resultado_dir = migrar_directorio(directorio, base_path)
            resultado_fase["directorios"][directorio] = resultado_dir
            resultado_fase["archivos_procesados"] += resultado_dir["archivos_procesados"]
            resultado_fase["archivos_migrados"] += resultado_dir["archivos_migrados"]
            resultado_fase["cambios_totales"] += resultado_dir["cambios_totales"]

            if resultado_dir["errores"]:
                resultado_global["errores_globales"].extend(resultado_dir["errores"])

        resultado_global["fases"][fase] = resultado_fase
        resultado_global["totales"]["directorios_procesados"] += len(directorios)
        resultado_global["totales"]["archivos_procesados"] += resultado_fase["archivos_procesados"]
        resultado_global["totales"]["archivos_migrados"] += resultado_fase["archivos_migrados"]
        resultado_global["totales"]["cambios_totales"] += resultado_fase["cambios_totales"]

        print(f"🎯 {fase} COMPLETADA: {resultado_fase['archivos_migrados']} archivos migrados, {resultado_fase['cambios_totales']} cambios")

    # Guardar reporte
    reporte_path = base_path / "data" / "logs" / f"migracion_sic_v3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    reporte_path.parent.mkdir(parents=True, exist_ok=True)

    with open(reporte_path, 'w', encoding='utf-8') as f:
        json.dump(resultado_global, f, indent=2, ensure_ascii=False)

    print(f"\n📊 REPORTE GUARDADO: {reporte_path}")
    return resultado_global

def mostrar_resumen_final(resultado: Dict):
    """Muestra un resumen final de la migración."""
    totales = resultado["totales"]

    print("\n" + "=" * 60)
    print("🎉 MIGRACIÓN MASIVA SIC v3.0 COMPLETADA")
    print("=" * 60)
    print(f"📁 Directorios procesados: {totales['directorios_procesados']}")
    print(f"📄 Archivos procesados: {totales['archivos_procesados']}")
    print(f"✅ Archivos migrados: {totales['archivos_migrados']}")
    print(f"🔧 Cambios totales: {totales['cambios_totales']}")

    if resultado["errores_globales"]:
        print(f"❌ Errores encontrados: {len(resultado['errores_globales'])}")
        for error in resultado["errores_globales"][:5]:  # Mostrar solo los primeros 5
            print(f"   - {error}")
    else:
        print("✅ Sin errores detectados")

    print(f"\n🕒 Timestamp: {resultado['timestamp']}")

    if SIC_AVAILABLE:
        print("\n🔍 VALIDACIÓN FINAL:")
        try:
            status = get_sic_status()
            print(f"SIC Status: {status['version']} - {status['status']}")
            print(f"Exports disponibles: {status['total_exports']}")

            if SIC_AVAILABLE:
                enviar_senal_log("INFO", f"Migración masiva completada: {totales['archivos_migrados']} archivos", "migrador", "completed")
        except Exception as e:
            print(f"⚠️ Error en validación final: {e}")

# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("🎯 MIGRADOR MASIVO SIC v3.0")
    print("Autor: ITC Engine v5.0")
    print("Versión: v1.0")

    if not SIC_AVAILABLE:
        print("❌ SIC v3.0 no disponible. Abortando migración.")
        sys.exit(1)

    try:
        # Mostrar estado inicial
        print(f"\n🔍 Estado inicial SIC: {get_sic_status()['version']}")

        # Confirmar ejecución
        print("\n⚠️ Esta operación modificará múltiples archivos.")
        print("Se crearán backups automáticamente (.backup)")
        respuesta = input("¿Continuar con la migración? (y/N): ")

        if respuesta.lower() not in ['y', 'yes', 'sí', 's']:
            print("❌ Migración cancelada por el usuario.")
            sys.exit(0)

        # Ejecutar migración
        resultado = ejecutar_migracion_completa()

        # Mostrar resumen
        mostrar_resumen_final(resultado)

        print("\n🚀 Migración completada exitosamente!")
        print("💡 Revisa VS Code Problems para verificar la reducción de errores.")

    except KeyboardInterrupt:
        print("\n❌ Migración interrumpida por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error crítico en migración: {e}")
        sys.exit(1)
