# 🎯 SPRINT 1.1 VALIDATION RUNNER
# Ejecutar validación completa del Sprint 1.1: Debug System & Clean Code
# RESPETA LA ESTRUCTURA MODULAR EXISTENTE

import sys
import os
from pathlib import Path
import subprocess
import json
from datetime import datetime
from sistema.logging_interface import enviar_senal_log

# 📁 Configurar paths respetando estructura modular existente
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def run_sprint_validation():
    """
    Ejecuta la validación completa del Sprint 1.1 usando estructura modular existente
    """
    enviar_senal_log("DEBUG", "🚀 INICIANDO VALIDACIÓN SPRINT 1.1: DEBUG SYSTEM & CLEAN CODE", "validation_runner", "migration")
    enviar_senal_log("INFO", "=" * 70, "validation_runner", "migration")

    enviar_senal_log("INFO", f"📁 Proyecto Root: {PROJECT_ROOT}", "validation_runner", "migration")

    # 🔧 Verificar que existe el consolidator en utilities/sprint/
    consolidator_path = PROJECT_ROOT / "utilities" / "sprint" / "sprint_1_1_consolidator.py"

    if not consolidator_path.exists():
        enviar_senal_log("ERROR", f"❌ ERROR: No se encuentra {consolidator_path}", "validation_runner", "migration")
        enviar_senal_log("INFO", "🔧 Nota: Este archivo debería estar en utilities/sprint/", "validation_runner", "migration")
        return False, "Consolidator no encontrado"

    enviar_senal_log("INFO", f"✅ Consolidator encontrado: {consolidator_path}", "validation_runner", "migration")

    # 🎯 Ejecutar validación completa
    enviar_senal_log("INFO", "\n🔍 EJECUTANDO VALIDACIÓN COMPLETA...", "validation_runner", "migration")
    enviar_senal_log("INFO", "-" * 50, "validation_runner", "migration")

    try:
        # 🏃‍♂️ Ejecutar el consolidator
        result = subprocess.run([
            sys.executable,
            str(consolidator_path),
            "--validation-only"
        ], capture_output=True, text=True, cwd=PROJECT_ROOT)

        enviar_senal_log("INFO", "📊 RESULTADOS DE VALIDACIÓN:", "validation_runner", "migration")
        enviar_senal_log("INFO", "=" * 40, "validation_runner", "migration")

        if result.stdout:
            enviar_senal_log("INFO", "✅ STDOUT:", "validation_runner", "migration")
            enviar_senal_log("INFO", result.stdout, "validation_runner", "migration")

        if result.stderr:
            enviar_senal_log("INFO", "\n⚠️ STDERR:", "validation_runner", "migration")
            enviar_senal_log("INFO", result.stderr, "validation_runner", "migration")

        enviar_senal_log("INFO", f"\n🔢 Return Code: {result.returncode}", "validation_runner", "migration")

        # 🎪 Interpretar resultados
        if result.returncode == 0:
            enviar_senal_log("INFO", "\n🎉 ¡VALIDACIÓN EXITOSA!", "validation_runner", "migration")
            return True, "Sprint 1.1 funcionando correctamente"
        else:
            enviar_senal_log("INFO", "\n⚠️ VALIDACIÓN CON PROBLEMAS", "validation_runner", "migration")
            return False, "Revisar output para identificar issues"

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ ERROR ejecutando validación: {e}", "validation_runner", "migration")
        return False, f"Error de ejecución: {e}"

def run_print_scan():
    """
    Ejecuta escaneo de print statements usando utilities/migration/
    """
    enviar_senal_log("INFO", "\n" + "=" * 70, "validation_runner", "migration")
    enviar_senal_log("INFO", "🔍 ESCANEANDO PRINT STATEMENTS...", "validation_runner", "migration")
    enviar_senal_log("INFO", "=" * 70, "validation_runner", "migration")

    # 📁 Buscar herramienta de migración en utilities/migration/
    migration_tool_path = PROJECT_ROOT / "utilities" / "migration" / "print_migration_tool.py"

    if not migration_tool_path.exists():
        enviar_senal_log("ERROR", f"❌ ERROR: No se encuentra {migration_tool_path}", "validation_runner", "migration")
        enviar_senal_log("INFO", "🔧 Nota: Este archivo debería estar en utilities/migration/", "validation_runner", "migration")
        return False, "Migration tool no encontrado"

    try:
        # 🔍 Ejecutar escaneo
        result = subprocess.run([
            sys.executable,
            str(migration_tool_path),
            "--scan-only"
        ], capture_output=True, text=True, cwd=PROJECT_ROOT)

        enviar_senal_log("INFO", "📊 RESULTADOS DE ESCANEO:", "validation_runner", "migration")
        enviar_senal_log("INFO", "-" * 40, "validation_runner", "migration")

        if result.stdout:
            enviar_senal_log("INFO", result.stdout, "validation_runner", "migration")

        if result.stderr and result.stderr.strip():
            enviar_senal_log("ERROR", "⚠️ Errores:", "validation_runner", "migration")
            enviar_senal_log("INFO", result.stderr, "validation_runner", "migration")

        return result.returncode == 0, "Escaneo completado"

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ ERROR ejecutando escaneo: {e}", "validation_runner", "migration")
        return False, f"Error de escaneo: {e}"

def test_debug_launcher():
    """
    Prueba el debug launcher en utilities/debug/
    """
    enviar_senal_log("INFO", "\n" + "=" * 70, "validation_runner", "migration")
    enviar_senal_log("DEBUG", "🔧 TESTING DEBUG LAUNCHER...", "validation_runner", "migration")
    enviar_senal_log("INFO", "=" * 70, "validation_runner", "migration")

    # 📁 Debug launcher en utilities/debug/
    launcher_path = PROJECT_ROOT / "utilities" / "debug" / "debug_launcher.py"

    if not launcher_path.exists():
        enviar_senal_log("ERROR", f"❌ ERROR: No se encuentra {launcher_path}", "validation_runner", "migration")
        enviar_senal_log("DEBUG", "🔧 Nota: Este archivo debería estar en utilities/debug/", "validation_runner", "migration")
        return False, "Debug launcher no encontrado"

    enviar_senal_log("DEBUG", f"✅ Debug Launcher encontrado: {launcher_path}", "validation_runner", "migration")

    # 🔍 Verificar contenido básico
    try:
        with open(launcher_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # ✅ Verificaciones básicas
        checks = {
            'F12 binding': 'F12' in content or 'f12' in content,
            'DevTools toggle': 'toggle_devtools' in content or 'devtools' in content.lower(),
            'Textual App': 'from textual.app import App' in content or 'textual' in content.lower(),
            'Screenshot capability': 'screenshot' in content.lower(),
            'Console mode': 'console' in content.lower()
        }

        enviar_senal_log("DEBUG", "🔍 VERIFICACIONES DEL DEBUG LAUNCHER:", "validation_runner", "migration")
        enviar_senal_log("INFO", "-" * 40, "validation_runner", "migration")

        for check_name, passed in checks.items():
            status = "✅" if passed else "❌"
            enviar_senal_log("INFO", f"{status} {check_name}", "validation_runner", "migration")

        # 📊 Resultado general
        passed_checks = sum(checks.values())
        total_checks = len(checks)

        enviar_senal_log("INFO", f"\n📊 Resultado: {passed_checks}/{total_checks} verificaciones pasadas", "validation_runner", "migration")

        if passed_checks >= 3:
            enviar_senal_log("DEBUG", "🎉 Debug Launcher parece estar bien implementado!", "validation_runner", "migration")
            return True, f"Debug launcher OK ({passed_checks}/{total_checks})"
        else:
            enviar_senal_log("DEBUG", "⚠️ Debug Launcher necesita trabajo adicional", "validation_runner", "migration")
            return False, f"Debug launcher incompleto ({passed_checks}/{total_checks})"

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ ERROR verificando debug launcher: {e}", "validation_runner", "migration")
        return False, f"Error verificando launcher: {e}"

def check_existing_structure():
    """
    Verifica la estructura existente del proyecto
    """
    enviar_senal_log("INFO", "\n" + "=" * 70, "validation_runner", "migration")
    enviar_senal_log("INFO", "📁 VERIFICANDO ESTRUCTURA DEL PROYECTO...", "validation_runner", "migration")
    enviar_senal_log("INFO", "=" * 70, "validation_runner", "migration")

    # 📂 Directorios clave a verificar
    key_dirs = [
        "utilities",
        "utilities/debug",
        "utilities/migration",
        "utilities/sprint",
        "core",
        "dashboard",
        "sistema"
    ]

    existing_dirs = []
    missing_dirs = []

    for dir_path in key_dirs:
        full_path = PROJECT_ROOT / dir_path
        if full_path.exists():
            existing_dirs.append(dir_path)
            enviar_senal_log("INFO", f"✅ {dir_path}", "validation_runner", "migration")
        else:
            missing_dirs.append(dir_path)
            enviar_senal_log("INFO", f"❌ {dir_path}", "validation_runner", "migration")

    enviar_senal_log("INFO", f"\n📊 Estructura: {len(existing_dirs, "validation_runner", "migration")}/{len(key_dirs)} directorios encontrados")

    return len(missing_dirs) == 0, f"Estructura: {len(existing_dirs)}/{len(key_dirs)}"

def main():
    """
    Función principal - ejecuta todas las validaciones
    """
    enviar_senal_log("INFO", "🎯 SPRINT 1.1 VALIDATION SUITE", "validation_runner", "migration")
    enviar_senal_log("DEBUG", "🚀 Debug System & Clean Code", "validation_runner", "migration")
    enviar_senal_log("INFO", "📅 " + datetime.now(, "validation_runner", "migration").strftime("%Y-%m-%d %H:%M:%S"))
    enviar_senal_log("INFO", "=" * 70, "validation_runner", "migration")

    # 🏃‍♂️ Ejecutar todas las validaciones
    validations = [
        ("Estructura del Proyecto", check_existing_structure),
        ("Debug Launcher Test", test_debug_launcher),
        ("Print Statement Scan", run_print_scan),
        ("Sprint Validation", run_sprint_validation)
    ]

    results = {}
    details = {}

    for name, validation_func in validations:
        enviar_senal_log("INFO", f"\n🔍 Ejecutando: {name}", "validation_runner", "migration")
        try:
            success, detail = validation_func()
            results[name] = success
            details[name] = detail
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error en {name}: {e}", "validation_runner", "migration")
            results[name] = False
            details[name] = f"Error: {e}"

    # 📊 Reporte final
    enviar_senal_log("INFO", "\n" + "=" * 70, "validation_runner", "migration")
    enviar_senal_log("INFO", "📊 REPORTE FINAL DE VALIDACIÓN", "validation_runner", "migration")
    enviar_senal_log("INFO", "=" * 70, "validation_runner", "migration")

    for name, passed in results.items():
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        detail = details.get(name, "")
        enviar_senal_log("INFO", f"{status} {name} - {detail}", "validation_runner", "migration")

    # 🎯 Conclusión
    passed_validations = sum(results.values())
    total_validations = len(results)

    enviar_senal_log("INFO", f"\n🎪 RESULTADO GENERAL: {passed_validations}/{total_validations} validaciones exitosas", "validation_runner", "migration")

    if passed_validations == total_validations:
        enviar_senal_log("INFO", "🎉 ¡SPRINT 1.1 COMPLETAMENTE VALIDADO!", "validation_runner", "migration")
        enviar_senal_log("INFO", "✅ Sistema listo para Sprint 1.2", "validation_runner", "migration")
    elif passed_validations >= total_validations // 2:
        enviar_senal_log("INFO", "⚠️ Sprint 1.1 parcialmente implementado", "validation_runner", "migration")
        enviar_senal_log("INFO", "🔧 Revisar issues identificados antes de continuar", "validation_runner", "migration")
    else:
        enviar_senal_log("INFO", "❌ Sprint 1.1 necesita trabajo significativo", "validation_runner", "migration")
        enviar_senal_log("INFO", "🚨 Abordar problemas críticos antes de continuar", "validation_runner", "migration")

    enviar_senal_log("INFO", f"\n🔧 Ejecutado desde: {PROJECT_ROOT}", "validation_runner", "migration")
    enviar_senal_log("INFO", "📂 Para re-ejecutar: python utilities/validation_runner.py", "validation_runner", "migration")

    return passed_validations, total_validations

if __name__ == "__main__":
    main()
