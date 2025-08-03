from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para corregir manualmente acc_flow_controller.py
"""

import re

def fix_acc_flow_controller():
    """Corrige completamente el archivo acc_flow_controller.py"""
    file_path = r"c:\Users\v_jac\Desktop\itc engine v5.0\core\analysis_command_center\acc_flow_controller.py"

    # Leer el archivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Lista de reemplazos específicos y precisos
    replacements = [
        # Corregir parámetros de enviar_senal_log
        (r"level='([^']*)'", r"nivel='\1'"),
        (r'level="([^"]*)"', r'nivel="\1"'),
        (r"emisor='([^']*)'", r"fuente='\1'"),
        (r'emisor="([^"]*)"', r'fuente="\1"'),

        # Corregir message= por mensaje=
        (r"\s+message=", r" mensaje="),

        # Corregir f-strings mal escapados
        (r'mensaje=f\\"([^"]*?)\\"', r'mensaje=f"\1"'),
        (r'message=f\\"([^"]*?)\\"', r'mensaje=f"\1"'),

        # Casos específicos de líneas múltiples
        (r'message=f"([^"]*?)"\s*\+\s*f"([^"]*?)"', r'mensaje=f"\1\2"'),
        (r'message=f"([^"]*?)"\s*\n\s*f"([^"]*?)"', r'mensaje=f"\1\2"'),

        # Multilinea patterns específicos para este archivo
        (r'message=f"([^"]+?)"\s*\n\s*"([^"]+?)"', r'mensaje=f"\1\2"'),
        (r'message=f"([^"]+?)"\s*\n\s*f"([^"]+?)"', r'mensaje=f"\1\2"'),
    ]

    # Aplicar reemplazos
    for old_pattern, new_pattern in replacements:
        content = re.sub(old_pattern, new_pattern, content, flags=re.MULTILINE | re.DOTALL)

    # Reemplazos específicos de líneas problemáticas conocidas
    specific_fixes = [
        # Línea específica que causa problemas
        ('message=f"💾 Cache result returned | Original ID: {result.analysis_id} | "\n                       f"New ID: {cached_result.analysis_id}",',
         'mensaje=f"💾 Cache result returned | Original ID: {result.analysis_id} | New ID: {cached_result.analysis_id}",'),

        ('message=f"📥 Analysis queued | ID: {analysis_input.analysis_id} | "\n                   f"Priority: {priority.value} | Queue Length: {len(self.analysis_queue)}",',
         'mensaje=f"📥 Analysis queued | ID: {analysis_input.analysis_id} | Priority: {priority.value} | Queue Length: {len(self.analysis_queue)}",'),

        ('message=f"📤 Analysis dequeued | ID: {analysis_item[\'analysis_input\'].analysis_id} | "\n                           f"Priority: {analysis_item[\'priority\'].value}",',
         'mensaje=f"📤 Analysis dequeued | ID: {analysis_item[\'analysis_input\'].analysis_id} | Priority: {analysis_item[\'priority\'].value}",'),

        ('message=f"📊 Analysis completed | ID: {analysis_id} | "\n                   f"Time: {execution_time:.0f}ms | Success: {success} | "\n                   f"Active: {len(self.active_analyses)}",',
         'mensaje=f"📊 Analysis completed | ID: {analysis_id} | Time: {execution_time:.0f}ms | Success: {success} | Active: {len(self.active_analyses)}",'),

        ('message=f"🎯 Flow optimized | Symbol: {symbol} | "\n                   f"Avg Time: {avg_time:.0f}ms | Success: {success_rate:.1%}",',
         'mensaje=f"🎯 Flow optimized | Symbol: {symbol} | Avg Time: {avg_time:.0f}ms | Success: {success_rate:.1%}",'),
    ]

    for old_text, new_text in specific_fixes:
        content = content.replace(old_text, new_text)

    # Escribir el archivo corregido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    enviar_senal_log("INFO", "✅ acc_flow_controller.py corregido completamente", "fix_acc_flow_controller", "migration")
    enviar_senal_log("INFO", "✅ Parámetros actualizados:", "fix_acc_flow_controller", "migration")
    enviar_senal_log("INFO", "  - level -> nivel", "fix_acc_flow_controller", "migration")
    enviar_senal_log("INFO", "  - message -> mensaje", "fix_acc_flow_controller", "migration")
    enviar_senal_log("INFO", "  - emisor -> fuente", "fix_acc_flow_controller", "migration")
    enviar_senal_log("INFO", "  - f-strings corregidos", "fix_acc_flow_controller", "migration")
    enviar_senal_log("INFO", "  - Líneas multilinea unificadas", "fix_acc_flow_controller", "migration")

if __name__ == "__main__":
    fix_acc_flow_controller()
