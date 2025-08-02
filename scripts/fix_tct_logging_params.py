#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para corregir los parámetros de enviar_senal_log en tct_measurements.py
"""

import re

def fix_tct_measurements():
    """Corrige los parámetros incorrectos en tct_measurements.py"""
    file_path = r"c:\Users\v_jac\Desktop\itc engine v5.0\core\analysis_command_center\tct_pipeline\tct_measurements.py"

    # Leer el archivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Reemplazos necesarios
    replacements = [
        (r"level='([^']*)'", r"nivel='\1'"),
        (r'level="([^"]*)"', r'nivel="\1"'),
        (r"message=", r"mensaje="),
        (r"emisor=", r"fuente=")
    ]

    # Aplicar reemplazos
    for old_pattern, new_pattern in replacements:
        content = re.sub(old_pattern, new_pattern, content)

    # Escribir el archivo corregido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Archivo tct_measurements.py corregido")
    print("✅ Parámetros actualizados:")
    print("  - level -> nivel")
    print("  - message -> mensaje")
    print("  - emisor -> fuente")

if __name__ == "__main__":
    fix_tct_measurements()
