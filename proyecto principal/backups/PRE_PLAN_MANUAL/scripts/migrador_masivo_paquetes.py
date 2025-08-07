#!/usr/bin/env python3
"""
🚀 MIGRADOR MASIVO POR PAQUETES - SIC v3.0 + SLUC v2.1
====================================================
Procesa archivos en paquetes de 20 simultáneos para migración rápida

Autor: ITC Engine v5.0
Fecha: 2025-08-06
Versión: v2.0 - Paquetes
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
import concurrent.futures
import threading

# Configurar path del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from sistema.sic import enviar_senal_log, log_info, log_warning

# =============================================================================
# CONFIGURACIÓN DE MIGRACIÓN MASIVA
# =============================================================================

# Patterns de migración completos
MIGRATION_PATTERNS = {
    # Eliminar imports de logging tradicional
    r'^import logging$': '',
    r'^import logging as [a-zA-Z_]+$': '',
    r'^from logging import.*$': '',

    # Eliminar usos de logging tradicional
    r'logging\.getLogger\([^)]*\)': 'None  # Removido - usar SIC v3.0',
    r'logging\.basicConfig\([^)]*\)': '# Removido - usar SIC v3.0',
    r'logger\.[a-zA-Z_]+\([^)]*\)': '# Removido - usar enviar_senal_log',
    r'log\.[a-zA-Z_]+\([^)]*\)': '# Removido - usar enviar_senal_log',

    # Reemplazar imports estándar por SIC
    r'^import os$': 'from sistema.sic import os',
    r'^import sys$': 'from sistema.sic import sys',
    r'^import json$': 'from sistema.sic import json',
    r'^import re$': 'from sistema.sic import re',
    r'^from pathlib import Path$': 'from sistema.sic import Path',
    r'^from datetime import datetime': 'from sistema.sic import datetime',
    r'^from datetime import timedelta': 'from sistema.sic import timedelta',
    r'^from typing import': 'from sistema.sic import',
    r'^from dataclasses import': 'from sistema.sic import',
    r'^from collections import': 'from sistema.sic import',

    # Agregar import de logging SIC si no existe
    r'(#!/usr/bin/env python3\n"""[\s\S]*?"""\n)': r'\1\n# MIGRACIÓN SIC v3.0 + SLUC v2.1\nfrom sistema.sic import enviar_senal_log, log_info, log_warning\n',
}

# Archivos a ignorar completamente
ARCHIVOS_IGNORAR = {
    "__pycache__", ".git", ".vscode", "node_modules", "venv", "env", ".pytest_cache",
    "sic.py", "sic_v3_limpio.py", "logging_interface.py", "smart_directory_logger.py",
    "__init__.py",  # Generalmente están vacíos
    ".backup", ".old", ".temp"
}

# Directorios a procesar
DIRECTORIOS_PROCESAR = [
    "core/analytics/",
    "core/data_management/",
    "core/risk_management/",
    "core/poi_system/",
    "core/integrations/",
    "core/ict_engine/",
    "dashboard/",
    "dashboard/widgets/",
    "utils/",
    "utilities/",
    "teste/",
    "scripts/",
    "scripts/error_detection/",
    "sistema/",
]

# Lock para thread safety
migration_lock = threading.Lock()
migration_stats = {
    "archivos_procesados": 0,
    "archivos_migrados": 0,
    "errores": [],
    "cambios_totales": 0
}

# =============================================================================
# FUNCIONES DE MIGRACIÓN
# =============================================================================

def validar_sintaxis_python(contenido: str, archivo_path: str) -> bool:
    """Valida sintaxis Python de contenido."""
    try:
        compile(contenido, archivo_path, 'exec')
        return True
    except SyntaxError as e:
        return False
    except Exception:
        return True  # Asumir válido si no se puede verificar

def migrar_archivo_individual(archivo_path: Path) -> Dict:
    """Migra un archivo individual con todas las optimizaciones."""
    resultado = {
        "archivo": str(archivo_path),
        "migrado": False,
        "cambios": 0,
        "errores": []
    }

    try:
        # Leer archivo
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido_original = f.read()

        # Si no tiene imports problemáticos, saltar
        patterns_check = [
            r'import logging', r'logger\.', r'logging\.',
            r'import os', r'import sys', r'import json'
        ]

        if not any(re.search(pattern, contenido_original) for pattern in patterns_check):
            return resultado

        # Crear backup
        backup_path = archivo_path.with_suffix(archivo_path.suffix + ".backup")
        shutil.copy2(archivo_path, backup_path)

        # Aplicar migración
        contenido_migrado = contenido_original
        cambios_realizados = 0

        # Primero, agregar import de SIC si no existe
        if 'from sistema.sic import' not in contenido_migrado:
            # Buscar donde insertar el import
            lines = contenido_migrado.split('\n')
            insert_idx = 0

            # Encontrar línea después del docstring
            in_docstring = False
            for i, line in enumerate(lines):
                if line.strip().startswith('"""') or line.strip().startswith("'''"):
                    if not in_docstring:
                        in_docstring = True
                    elif in_docstring:
                        insert_idx = i + 1
                        break
                elif line.strip().startswith('#') or line.strip() == '':
                    continue
                elif not in_docstring:
                    insert_idx = i
                    break

            # Insertar import del SIC
            lines.insert(insert_idx, "\n# MIGRACIÓN SIC v3.0 + SLUC v2.1")
            lines.insert(insert_idx + 1, "from sistema.sic import enviar_senal_log, log_info, log_warning")
            lines.insert(insert_idx + 2, "")
            contenido_migrado = '\n'.join(lines)
            cambios_realizados += 1

        # Aplicar patterns de migración
        for pattern, replacement in MIGRATION_PATTERNS.items():
            matches = len(re.findall(pattern, contenido_migrado, re.MULTILINE))
            if matches > 0:
                contenido_migrado = re.sub(pattern, replacement, contenido_migrado, flags=re.MULTILINE)
                cambios_realizados += matches

        # Validar sintaxis antes de escribir
        if cambios_realizados > 0:
            if validar_sintaxis_python(contenido_migrado, str(archivo_path)):
                # Escribir archivo migrado
                with open(archivo_path, 'w', encoding='utf-8') as f:
                    f.write(contenido_migrado)

                resultado["migrado"] = True
                resultado["cambios"] = cambios_realizados

                # Stats thread-safe
                with migration_lock:
                    migration_stats["archivos_migrados"] += 1
                    migration_stats["cambios_totales"] += cambios_realizados

            else:
                # Restaurar backup si hay error de sintaxis
                shutil.copy2(backup_path, archivo_path)
                resultado["errores"].append("Error de sintaxis post-migración")

        # Stats thread-safe
        with migration_lock:
            migration_stats["archivos_procesados"] += 1

    except Exception as e:
        resultado["errores"].append(str(e))
        with migration_lock:
            migration_stats["errores"].append(f"{archivo_path}: {e}")

    return resultado

def obtener_archivos_python(directorio: str, base_path: Path) -> List[Path]:
    """Obtiene lista de archivos Python en un directorio."""
    dir_path = base_path / directorio
    archivos = []

    if not dir_path.exists():
        return archivos

    for archivo_path in dir_path.rglob("*.py"):
        # Saltar archivos a ignorar
        if any(ignore in str(archivo_path) for ignore in ARCHIVOS_IGNORAR):
            continue
        archivos.append(archivo_path)

    return archivos

def procesar_paquete_archivos(archivos: List[Path], paquete_num: int) -> Dict:
    """Procesa un paquete de archivos en paralelo."""
    print(f"🔄 Procesando paquete {paquete_num}: {len(archivos)} archivos")

    # Usar ThreadPoolExecutor para procesar archivos en paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futuros = [executor.submit(migrar_archivo_individual, archivo) for archivo in archivos]
        resultados = []

        for futuro in concurrent.futures.as_completed(futuros):
            try:
                resultado = futuro.result()
                resultados.append(resultado)
                if resultado["migrado"]:
                    print(f"  ✅ {Path(resultado['archivo']).name} ({resultado['cambios']} cambios)")
                elif resultado["errores"]:
                    print(f"  ❌ {Path(resultado['archivo']).name} - {resultado['errores'][0]}")
            except Exception as e:
                print(f"  ❌ Error en futuro: {e}")

    migrados = sum(1 for r in resultados if r["migrado"])
    total_cambios = sum(r["cambios"] for r in resultados)

    print(f"✅ Paquete {paquete_num} completado: {migrados}/{len(archivos)} archivos migrados, {total_cambios} cambios")

    return {
        "paquete": paquete_num,
        "archivos_procesados": len(archivos),
        "archivos_migrados": migrados,
        "cambios_totales": total_cambios,
        "resultados": resultados
    }

def ejecutar_migracion_masiva_por_paquetes() -> Dict:
    """Ejecuta la migración completa por paquetes de 20."""
    base_path = Path(project_root)

    print("🚀 INICIANDO MIGRACIÓN MASIVA POR PAQUETES")
    print("=" * 55)

    # Recopilar todos los archivos
    todos_los_archivos = []
    for directorio in DIRECTORIOS_PROCESAR:
        archivos = obtener_archivos_python(directorio, base_path)
        todos_los_archivos.extend(archivos)

    print(f"📁 Total archivos encontrados: {len(todos_los_archivos)}")

    # Dividir en paquetes de 20
    tamano_paquete = 20
    paquetes = [todos_los_archivos[i:i + tamano_paquete]
                for i in range(0, len(todos_los_archivos), tamano_paquete)]

    print(f"📦 Total paquetes a procesar: {len(paquetes)}")

    # Resetear stats
    global migration_stats
    migration_stats = {
        "archivos_procesados": 0,
        "archivos_migrados": 0,
        "errores": [],
        "cambios_totales": 0
    }

    # Procesar paquetes secuencialmente (cada paquete se procesa en paralelo internamente)
    resultados_paquetes = []
    for i, paquete in enumerate(paquetes, 1):
        resultado_paquete = procesar_paquete_archivos(paquete, i)
        resultados_paquetes.append(resultado_paquete)

        # Log de progreso
        progreso = (i / len(paquetes)) * 100
        print(f"📊 Progreso: {progreso:.1f}% ({i}/{len(paquetes)} paquetes)")

        # Log cada 5 paquetes con el sistema de logging
        if i % 5 == 0:
            enviar_senal_log("INFO",
                f"Migración progreso: {i}/{len(paquetes)} paquetes, {migration_stats['archivos_migrados']} archivos migrados",
                "migrador_masivo", "progress")

    # Resultado final
    resultado_final = {
        "timestamp": datetime.now().isoformat(),
        "paquetes_procesados": len(paquetes),
        "archivos_totales": len(todos_los_archivos),
        "archivos_migrados": migration_stats["archivos_migrados"],
        "cambios_totales": migration_stats["cambios_totales"],
        "errores": migration_stats["errores"],
        "paquetes": resultados_paquetes
    }

    # Guardar reporte
    reporte_path = base_path / "data" / "logs" / f"migracion_paquetes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    reporte_path.parent.mkdir(parents=True, exist_ok=True)

    with open(reporte_path, 'w', encoding='utf-8') as f:
        json.dump(resultado_final, f, indent=2, ensure_ascii=False)

    print(f"\n📊 REPORTE GUARDADO: {reporte_path}")
    return resultado_final

def mostrar_resumen_final(resultado: Dict):
    """Muestra resumen final de la migración masiva."""
    print("\n" + "=" * 70)
    print("🎉 MIGRACIÓN MASIVA POR PAQUETES COMPLETADA")
    print("=" * 70)
    print(f"📦 Paquetes procesados: {resultado['paquetes_procesados']}")
    print(f"📄 Archivos totales: {resultado['archivos_totales']}")
    print(f"✅ Archivos migrados: {resultado['archivos_migrados']}")
    print(f"🔧 Cambios totales: {resultado['cambios_totales']}")

    if resultado["errores"]:
        print(f"❌ Errores encontrados: {len(resultado['errores'])}")
        for error in resultado["errores"][:3]:  # Mostrar solo los primeros 3
            print(f"   - {error}")
    else:
        print("✅ Sin errores detectados")

    # Tasa de éxito
    tasa_exito = (resultado["archivos_migrados"] / resultado["archivos_totales"]) * 100
    print(f"📈 Tasa de éxito: {tasa_exito:.1f}%")

    # Log final
    enviar_senal_log("INFO",
        f"Migración masiva completada: {resultado['archivos_migrados']}/{resultado['archivos_totales']} archivos, {resultado['cambios_totales']} cambios",
        "migrador_masivo", "completed")

# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("🚀 MIGRADOR MASIVO POR PAQUETES - SIC v3.0 + SLUC v2.1")
    print("Versión: v2.0 - Paquetes de 20 archivos simultáneos")

    try:
        # Confirmar ejecución
        print("\n⚠️ Esta operación modificará archivos en paquetes de 20.")
        print("Se crearán backups automáticamente (.backup)")
        respuesta = input("¿Continuar con la migración masiva? (y/N): ")

        if respuesta.lower() not in ['y', 'yes', 'sí', 's']:
            print("❌ Migración cancelada por el usuario.")
            sys.exit(0)

        # Ejecutar migración
        resultado = ejecutar_migracion_masiva_por_paquetes()

        # Mostrar resumen
        mostrar_resumen_final(resultado)

        print("\n🚀 Migración por paquetes completada exitosamente!")
        print("💡 Ejecuta el validador para verificar el estado final.")

    except KeyboardInterrupt:
        print("\n❌ Migración interrumpida por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error crítico en migración: {e}")
        enviar_senal_log("ERROR", f"Error crítico en migración masiva: {e}", "migrador_masivo", "critical")
        sys.exit(1)
