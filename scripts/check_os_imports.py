# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
"""
🔍 OS IMPORT CHECKER
Verifica qué archivos tienen imports de os no utilizados
"""

import re
from pathlib import Path

def check_os_usage(file_path):
    """Verifica si un archivo usa realmente el módulo os"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verificar si tiene import os
        has_import_os = re.search(r'^import os$', content, re.MULTILINE)

        if not has_import_os:
            return "no_import", 0

        # Buscar uso de os. (excluyendo comentarios)
        lines = content.split('\n')
        os_usage_count = 0

        for line in lines:
            # Ignorar líneas que son solo comentarios
            if line.strip().startswith('#'):
                continue

            # Buscar os. en la línea
            if re.search(r'\bos\.', line):
                os_usage_count += 1

        if os_usage_count > 0:
            return "used", os_usage_count
        else:
            return "unused", 0

    except Exception as e:
        return "error", str(e)

def main():
    """Función principal"""
    files_to_check = [
        'utils/mt5_data_manager.py',
        'utils/logging_utils.py',
        'sistema/data_logger.py',
        'sistema/config.py',
        'scripts/verificar_datos_reales.py',
        'scripts/validador_maestro.py',
        'scripts/sprint_1_6_calibrator.py',
        'scripts/limpiar_archivos_obsoletos.py',
        'scripts/diagnosticar_estrategia.py',
        'scripts/analizar_logs.py',
        'scripts/analizar_estrategia.py',
        'main.py',
        'core/trading.py',
        'core/smart_trading_logger.py'
    ]

    print("🔍 VERIFICANDO IMPORTS DE OS")
    print("=" * 50)

    unused_files = []
    used_files = []
    error_files = []

    for file_path in files_to_check:
        full_path = Path(file_path)
        if full_path.exists():
            status, count = check_os_usage(full_path)

            if status == "unused":
                print(f"❌ {file_path}: import os NO USADO")
                unused_files.append(file_path)
            elif status == "used":
                print(f"✅ {file_path}: import os USADO ({count} veces)")
                used_files.append(file_path)
            elif status == "no_import":
                print(f"⚪ {file_path}: sin import os")
            else:
                # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"🔴 {file_path}: Error - {count}")
                error_files.append(file_path)
        else:
            print(f"🚫 {file_path}: archivo no existe")

    print("\n📊 RESUMEN:")
    print(f"❌ Archivos con import os NO USADO: {len(unused_files)}")
    print(f"✅ Archivos con import os USADO: {len(used_files)}")
    # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"🔴 Archivos con errores: {len(error_files)}")

    if unused_files:
        print("\n🧹 ARCHIVOS QUE NECESITAN LIMPIEZA:")
        for file_path in unused_files:
            print(f"  - {file_path}")

if __name__ == "__main__":
    main()
