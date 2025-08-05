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

    enviar_senal_log("INFO", "🔍 VERIFICANDO IMPORTS DE OS", __name__, "sistema")
    enviar_senal_log("INFO", "=" * 50, __name__, "sistema")

    unused_files = []
    used_files = []
    error_files = []

    for file_path in files_to_check:
        full_path = Path(file_path)
        if full_path.exists():
            status, count = check_os_usage(full_path)

            if status == "unused":
                enviar_senal_log("WARNING", f"❌ {file_path}: import os NO USADO", __name__, "sistema")
                unused_files.append(file_path)
            elif status == "used":
                enviar_senal_log("INFO", f"✅ {file_path}: import os USADO ({count} veces)", __name__, "sistema")
                used_files.append(file_path)
            elif status == "no_import":
                enviar_senal_log("INFO", f"⚪ {file_path}: sin import os", __name__, "sistema")
            else:
                enviar_senal_log("ERROR", f"🔴 {file_path}: Error - {count}", __name__, "sistema")
                error_files.append(file_path)
        else:
            enviar_senal_log("WARNING", f"🚫 {file_path}: archivo no existe", __name__, "sistema")

    enviar_senal_log("INFO", "\n📊 RESUMEN:", __name__, "sistema")
    enviar_senal_log("INFO", f"❌ Archivos con import os NO USADO: {len(unused_files)}", __name__, "sistema")
    enviar_senal_log("INFO", f"✅ Archivos con import os USADO: {len(used_files)}", __name__, "sistema")
    enviar_senal_log("WARNING", f"🔴 Archivos con errores: {len(error_files)}", __name__, "sistema")

    if unused_files:
        enviar_senal_log("INFO", "\n🧹 ARCHIVOS QUE NECESITAN LIMPIEZA:", __name__, "sistema")
        for file_path in unused_files:
            enviar_senal_log("INFO", f"  - {file_path}", __name__, "sistema")

if __name__ == "__main__":
    main()
