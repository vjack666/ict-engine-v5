#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para corregir comillas mal escapadas en acc_flow_controller.py
"""

import re

def fix_escaped_quotes():
    """Corrige las comillas mal escapadas en f-strings"""
    file_path = r"c:\Users\v_jac\Desktop\itc engine v5.0\core\analysis_command_center\acc_flow_controller.py"

    # Leer el archivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Reemplazar las comillas mal escapadas
    # Patrón: mensaje=f\"texto con {variables}\"
    # Cambiar a: mensaje=f"texto con {variables}"

    content = re.sub(r'mensaje=f\\"([^"]*?)\\"', r'mensaje=f"\1"', content)

    # Escribir el archivo corregido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Comillas mal escapadas corregidas en acc_flow_controller.py")

if __name__ == "__main__":
    fix_escaped_quotes()
