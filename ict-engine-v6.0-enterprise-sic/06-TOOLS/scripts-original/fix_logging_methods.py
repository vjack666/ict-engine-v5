#!/usr/bin/env python3
"""
🔧 SCRIPT CORRECCIÓN MÉTODOS DE LOGGING
=====================================

Corrige todos los métodos de logging en los archivos de memoria v6.0
para usar los métodos correctos del SmartTradingLogger central.

Fecha: 8 de Agosto 2025 - 21:15 GMT
"""

import os
import re

def fix_logging_methods(file_path):
    """Corrige los métodos de logging en un archivo."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Diccionario de reemplazos
        replacements = {
            r'\.log_info\(': '.info(',
            r'\.log_warning\(': '.warning(',
            r'\.log_error\(': '.error(',
            r'\.log_debug\(': '.debug(',
            r'\.log_critical\(': '.critical('
        }
        
        original_content = content
        
        # Aplicar cada reemplazo
        for pattern, replacement in replacements.items():
            content = re.sub(pattern, replacement, content)
        
        # Solo escribir si hubo cambios
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Corregido: {file_path}")
            return True
        else:
            print(f"⚪ Sin cambios: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error en {file_path}: {e}")
        return False

def main():
    """Función principal para corregir todos los archivos."""
    print("🔧 INICIANDO CORRECCIÓN DE MÉTODOS DE LOGGING")
    print("=" * 50)
    
    # Archivos a corregir
    files_to_fix = [
        "core/analysis/ict_historical_analyzer_v6.py",
        "core/analysis/unified_market_memory.py"
    ]
    
    corrected_files = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            if fix_logging_methods(file_path):
                corrected_files += 1
        else:
            print(f"⚠️ Archivo no encontrado: {file_path}")
    
    print("\\n" + "=" * 50)
    print(f"🎉 CORRECCIÓN COMPLETADA")
    print(f"📊 Archivos corregidos: {corrected_files}/{len(files_to_fix)}")
    print("✅ Métodos de logging actualizados al estándar central")

if __name__ == "__main__":
    main()
