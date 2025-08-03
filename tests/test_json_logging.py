from sistema.logging_interface import enviar_senal_log
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

    enviar_senal_log("INFO", "🧪 === TEST JSON FUNCTIONALITY ===", "test_json_logging", "migration")

    try:
        # Importar funciones
        from sistema.logging_interface import export_log_config, export_log_stats, enviar_senal_log

        enviar_senal_log("INFO", "✅ Imports exitosos", "test_json_logging", "migration")

        # Test 1: Generar algunos logs
        enviar_senal_log("INFO", "📝 Generando logs de prueba...", "test_json_logging", "migration")
        enviar_senal_log("INFO", "Test de configuración JSON", "test")
        enviar_senal_log("DEBUG", "Probando exportación de estadísticas", "test")
        enviar_senal_log("WARNING", "Test de funcionalidad JSON", "test")

        # Test 2: Exportar configuración
        enviar_senal_log("INFO", "📤 Exportando configuración...", "test_json_logging", "migration")
        config_file = "data/logs/config/test_config.json"
        config_data = export_log_config(config_file)

        if os.path.exists(config_file):
            enviar_senal_log("INFO", f"✅ Configuración exportada exitosamente: {config_file}", "test_json_logging", "migration")
            enviar_senal_log("INFO", f"   Versión: {config_data['version']}", "test_json_logging", "migration")
            enviar_senal_log("INFO", f"   Directorios: {len(config_data['directories'], "test_json_logging", "migration")}")
            enviar_senal_log("INFO", f"   Modo silencioso: {config_data['silent_mode']}", "test_json_logging", "migration")
        else:
            enviar_senal_log("ERROR", "❌ Error: Archivo de configuración no creado", "test_json_logging", "migration")
            return False

        # Test 3: Exportar estadísticas
        enviar_senal_log("INFO", "📊 Exportando estadísticas...", "test_json_logging", "migration")
        stats_file = "data/logs/stats/test_stats.json"
        stats_data = export_log_stats(stats_file)

        if os.path.exists(stats_file):
            enviar_senal_log("INFO", f"✅ Estadísticas exportadas exitosamente: {stats_file}", "test_json_logging", "migration")
            enviar_senal_log("INFO", f"   Versión del sistema: {stats_data['system_info']['version']}", "test_json_logging", "migration")
            enviar_senal_log("INFO", f"   Total logs: {stats_data['system_info']['total_logs']}", "test_json_logging", "migration")
        else:
            enviar_senal_log("ERROR", "❌ Error: Archivo de estadísticas no creado", "test_json_logging", "migration")
            return False

        # Test 4: Verificar contenido JSON válido
        enviar_senal_log("INFO", "🔍 Verificando validez JSON...", "test_json_logging", "migration")
        import json

        with open(config_file, 'r', encoding='utf-8') as f:
            config_test = json.load(f)
            enviar_senal_log("INFO", f"✅ JSON de configuración válido - {len(config_test, "test_json_logging", "migration")} campos")

        with open(stats_file, 'r', encoding='utf-8') as f:
            stats_test = json.load(f)
            enviar_senal_log("INFO", f"✅ JSON de estadísticas válido - {len(stats_test, "test_json_logging", "migration")} campos")

        enviar_senal_log("INFO", "\n🎉 ¡TODOS LOS TESTS JSON PASARON!", "test_json_logging", "migration")
        enviar_senal_log("INFO", "📝 El import json en logging_interface.py ahora está siendo usado correctamente", "test_json_logging", "migration")

        return True

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en test JSON: {e}", "test_json_logging", "migration")
        import traceback
        enviar_senal_log("INFO", f"Traceback: {traceback.format_exc(, "test_json_logging", "migration")}")
        return False

def test_json_import_usage():
    """Verificar que json se está usando en logging_interface.py"""

    enviar_senal_log("INFO", "\n🔍 === VERIFICANDO USO DE JSON ===", "test_json_logging", "migration")

    # Leer el archivo y buscar usos de json
    interface_file = "sistema/logging_interface.py"

    if not os.path.exists(interface_file):
        enviar_senal_log("INFO", "❌ Archivo logging_interface.py no encontrado", "test_json_logging", "migration")
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
        enviar_senal_log("INFO", f"✅ JSON está siendo usado: {', '.join(json_uses, "test_json_logging", "migration")}")
        enviar_senal_log("INFO", "✅ El import json es necesario y correcto", "test_json_logging", "migration")
        return True
    else:
        enviar_senal_log("INFO", "❌ JSON no se está usando en el archivo", "test_json_logging", "migration")
        return False

def main():
    """Ejecuta todos los tests"""

    enviar_senal_log("INFO", "🚀 === INICIANDO TESTS JSON LOGGING INTERFACE ===", "test_json_logging", "migration")

    tests_passed = 0
    total_tests = 2

    # Test 1: Funcionalidad JSON
    if test_json_functions():
        tests_passed += 1

    # Test 2: Verificación de uso
    if test_json_import_usage():
        tests_passed += 1

    enviar_senal_log("INFO", f"\n🏁 === RESULTADO FINAL: {tests_passed}/{total_tests} TESTS PASADOS ===", "test_json_logging", "migration")

    if tests_passed == total_tests:
        enviar_senal_log("INFO", "🎉 ¡SOLUCIÓN IMPLEMENTADA CORRECTAMENTE!", "test_json_logging", "migration")
        enviar_senal_log("INFO", "📋 El import json en logging_interface.py ahora tiene un propósito válido", "test_json_logging", "migration")
        enviar_senal_log("WARNING", "✅ No más warnings de Pylance sobre import json no usado", "test_json_logging", "migration")
        return True
    else:
        enviar_senal_log("INFO", f"⚠️ {total_tests - tests_passed} test(s, "test_json_logging", "migration") fallaron")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
