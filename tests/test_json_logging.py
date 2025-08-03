#!/usr/bin/env python3
"""
🧪 TEST JSON FUNCTIONALITY - LOGGING INTERFACE
==============================================

Script de prueba para validar que el import json se está usando correctamente
en logging_interface.py y que las nuevas funciones JSON funcionan.

Autor: ICT Engine Team
Fecha: 02 Agosto 2025
"""

import sys
import os
from pathlib import Path

# Añadir el path del proyecto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_json_functions():
    """Test de las funciones JSON en logging_interface.py"""

    print("🧪 === TEST JSON FUNCTIONALITY ===")

    try:
        # Importar funciones
        from sistema.logging_interface import export_log_config, export_log_stats, enviar_senal_log

        print("✅ Imports exitosos")

        # Test 1: Generar algunos logs
        print("📝 Generando logs de prueba...")
        enviar_senal_log("INFO", "Test de configuración JSON", "test")
        enviar_senal_log("DEBUG", "Probando exportación de estadísticas", "test")
        enviar_senal_log("WARNING", "Test de funcionalidad JSON", "test")

        # Test 2: Exportar configuración
        print("📤 Exportando configuración...")
        config_file = "data/logs/config/test_config.json"
        config_data = export_log_config(config_file)

        if os.path.exists(config_file):
            print(f"✅ Configuración exportada exitosamente: {config_file}")
            print(f"   Versión: {config_data['version']}")
            print(f"   Directorios: {len(config_data['directories'])}")
            print(f"   Modo silencioso: {config_data['silent_mode']}")
        else:
            print("❌ Error: Archivo de configuración no creado")
            return False

        # Test 3: Exportar estadísticas
        print("📊 Exportando estadísticas...")
        stats_file = "data/logs/stats/test_stats.json"
        stats_data = export_log_stats(stats_file)

        if os.path.exists(stats_file):
            print(f"✅ Estadísticas exportadas exitosamente: {stats_file}")
            print(f"   Versión del sistema: {stats_data['system_info']['version']}")
            print(f"   Total logs: {stats_data['system_info']['total_logs']}")
        else:
            print("❌ Error: Archivo de estadísticas no creado")
            return False

        # Test 4: Verificar contenido JSON válido
        print("🔍 Verificando validez JSON...")
        import json

        with open(config_file, 'r', encoding='utf-8') as f:
            config_test = json.load(f)
            print(f"✅ JSON de configuración válido - {len(config_test)} campos")

        with open(stats_file, 'r', encoding='utf-8') as f:
            stats_test = json.load(f)
            print(f"✅ JSON de estadísticas válido - {len(stats_test)} campos")

        print("\n🎉 ¡TODOS LOS TESTS JSON PASARON!")
        print("📝 El import json en logging_interface.py ahora está siendo usado correctamente")

        return True

    except Exception as e:
        print(f"❌ Error en test JSON: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_json_import_usage():
    """Verificar que json se está usando en logging_interface.py"""

    print("\n🔍 === VERIFICANDO USO DE JSON ===")

    # Leer el archivo y buscar usos de json
    interface_file = "sistema/logging_interface.py"

    if not os.path.exists(interface_file):
        print("❌ Archivo logging_interface.py no encontrado")
        return False

    with open(interface_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscar usos de json
    json_uses = []
    if 'json.dump(' in content:
        json_uses.append('json.dump()')
    if 'json.load(' in content:
        json_uses.append('json.load()')
    if 'json.dumps(' in content:
        json_uses.append('json.dumps()')
    if 'json.loads(' in content:
        json_uses.append('json.loads()')

    if json_uses:
        print(f"✅ JSON está siendo usado: {', '.join(json_uses)}")
        print("✅ El import json es necesario y correcto")
        return True
    else:
        print("❌ JSON no se está usando en el archivo")
        return False

def main():
    """Ejecuta todos los tests"""

    print("🚀 === INICIANDO TESTS JSON LOGGING INTERFACE ===")

    tests_passed = 0
    total_tests = 2

    # Test 1: Funcionalidad JSON
    if test_json_functions():
        tests_passed += 1

    # Test 2: Verificación de uso
    if test_json_import_usage():
        tests_passed += 1

    print(f"\n🏁 === RESULTADO FINAL: {tests_passed}/{total_tests} TESTS PASADOS ===")

    if tests_passed == total_tests:
        print("🎉 ¡SOLUCIÓN IMPLEMENTADA CORRECTAMENTE!")
        print("📋 El import json en logging_interface.py ahora tiene un propósito válido")
        print("✅ No más warnings de Pylance sobre import json no usado")
        return True
    else:
        print(f"⚠️ {total_tests - tests_passed} test(s) fallaron")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
