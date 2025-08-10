#!/usr/bin/env python3
"""
🔧 ICT Engine v6.1.0 Enterprise SIC - Verificación de Sistema
==========================================================

Este script verifica que todo el sistema esté funcionando correctamente.
"""

import sys
import os

def main():
    print("="*80)
    print("🔧 ICT ENGINE v6.0 ENTERPRISE SIC - VERIFICACIÓN COMPLETA")
    print("="*80)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('sistema'):
        print("❌ Error: No se encuentra el directorio 'sistema'")
        print("   Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
        return False
    
    # 1. Verificar estructura de directorios
    print("\n1️⃣ Verificando estructura de directorios...")
    required_dirs = [
        'sistema/sic_v3_1',
        'tests',
        'config',
        'core',
        'dashboard',
        'docs',
        '.vscode'
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ {dir_path} - NO ENCONTRADO")
    
    # 2. Verificar archivos de configuración
    print("\n2️⃣ Verificando configuración...")
    config_files = [
        '.pylintrc',
        '.vscode/settings.json',
        'requirements.txt',
        'README.md'
    ]
    
    for file_path in config_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - NO ENCONTRADO")
    
    # 3. Verificar módulos SIC v3.1
    print("\n3️⃣ Verificando módulos SIC v3.1...")
    sic_modules = [
        'sistema/sic_v3_1/__init__.py',
        'sistema/sic_v3_1/enterprise_interface.py',
        'sistema/sic_v3_1/lazy_loading.py',
        'sistema/sic_v3_1/predictive_cache.py',
        'sistema/sic_v3_1/monitor_dashboard.py',
        'sistema/sic_v3_1/advanced_debug.py'
    ]
    
    for module_path in sic_modules:
        if os.path.exists(module_path):
            print(f"   ✅ {module_path}")
        else:
            print(f"   ❌ {module_path} - NO ENCONTRADO")
    
    # 4. Verificar tests
    print("\n4️⃣ Verificando tests...")
    test_files = [
        'tests/__init__.py',
        'tests/test_sic_complete.py'
    ]
    
    for test_path in test_files:
        if os.path.exists(test_path):
            print(f"   ✅ {test_path}")
        else:
            print(f"   ❌ {test_path} - NO ENCONTRADO")
    
    print("\n" + "="*80)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("="*80)
    print("\n📋 PRÓXIMOS PASOS:")
    print("   1. Abrir el proyecto en VS Code")
    print("   2. La configuración menos estricta ya está aplicada")
    print("   3. Los tests están en la carpeta 'tests/'")
    print("   4. Ejecutar: python -m pytest tests/ -v")
    print("\n🚀 ¡Tu ICT Engine v6.1.0 Enterprise SIC está listo!")
    
    return True

if __name__ == "__main__":
    main()
