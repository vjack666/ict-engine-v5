from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para corregir todos los parámetros de enviar_senal_log en el TCT pipeline
"""

import re
import os

def fix_tct_pipeline_logging():
    """Corrige los parámetros incorrectos en todos los archivos del TCT pipeline"""

    tct_files = [
        r"c:\Users\v_jac\Desktop\itc engine v5.0\core\analysis_command_center\tct_pipeline\tct_aggregator.py",
        r"c:\Users\v_jac\Desktop\itc engine v5.0\core\analysis_command_center\tct_pipeline\tct_interface.py",
        r"c:\Users\v_jac\Desktop\itc engine v5.0\core\analysis_command_center\tct_pipeline\tct_formatter.py",
        r"c:\Users\v_jac\Desktop\itc engine v5.0\core\analysis_command_center\tct_pipeline\tct_measurements.py"
    ]

    # Reemplazos necesarios
    replacements = [
        (r"level='([^']*)'", r"nivel='\1'"),
        (r'level="([^"]*)"', r'nivel="\1"'),
        (r"message=", r"mensaje="),
        (r"emisor=", r"fuente=")
    ]

    for file_path in tct_files:
        if os.path.exists(file_path):
            try:
                # Leer el archivo
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Aplicar reemplazos
                original_content = content
                for old_pattern, new_pattern in replacements:
                    content = re.sub(old_pattern, new_pattern, content)

                # Solo escribir si hubo cambios
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    enviar_senal_log("INFO", f"✅ Corregido: {os.path.basename(file_path, "fix_tct_pipeline_logging", "migration")}")
                else:
                    enviar_senal_log("INFO", f"📝 Sin cambios: {os.path.basename(file_path, "fix_tct_pipeline_logging", "migration")}")

            except Exception as e:
                enviar_senal_log("ERROR", f"❌ Error procesando {file_path}: {e}", "fix_tct_pipeline_logging", "migration")
        else:
            enviar_senal_log("INFO", f"⚠️ Archivo no encontrado: {file_path}", "fix_tct_pipeline_logging", "migration")

    enviar_senal_log("INFO", , "fix_tct_pipeline_logging", "migration")
    enviar_senal_log("INFO", "✅ Corrección completada en TCT Pipeline", "fix_tct_pipeline_logging", "migration")
    enviar_senal_log("INFO", "✅ Parámetros actualizados:", "fix_tct_pipeline_logging", "migration")
    enviar_senal_log("INFO", "  - level -> nivel", "fix_tct_pipeline_logging", "migration")
    enviar_senal_log("INFO", "  - message -> mensaje", "fix_tct_pipeline_logging", "migration")
    enviar_senal_log("INFO", "  - emisor -> fuente", "fix_tct_pipeline_logging", "migration")

if __name__ == "__main__":
    fix_tct_pipeline_logging()
