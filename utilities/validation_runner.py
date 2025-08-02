# 🎯 SPRINT 1.1 VALIDATION RUNNER
# Ejecutar validación completa del Sprint 1.1: Debug System & Clean Code
# RESPETA LA ESTRUCTURA MODULAR EXISTENTE

import sys
import os
from pathlib import Path
import subprocess
import json
from datetime import datetime

# 📁 Configurar paths respetando estructura modular existente
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def run_sprint_validation():
    """
    Ejecuta la validación completa del Sprint 1.1 usando estructura modular existente
    """
    print("🚀 INICIANDO VALIDACIÓN SPRINT 1.1: DEBUG SYSTEM & CLEAN CODE")
    print("=" * 70)

    print(f"📁 Proyecto Root: {PROJECT_ROOT}")

    # 🔧 Verificar que existe el consolidator en utilities/sprint/
    consolidator_path = PROJECT_ROOT / "utilities" / "sprint" / "sprint_1_1_consolidator.py"

    if not consolidator_path.exists():
        print(f"❌ ERROR: No se encuentra {consolidator_path}")
        print("🔧 Nota: Este archivo debería estar en utilities/sprint/")
        return False, "Consolidator no encontrado"

    print(f"✅ Consolidator encontrado: {consolidator_path}")

    # 🎯 Ejecutar validación completa
    print("\n🔍 EJECUTANDO VALIDACIÓN COMPLETA...")
    print("-" * 50)

    try:
        # 🏃‍♂️ Ejecutar el consolidator
        result = subprocess.run([
            sys.executable,
            str(consolidator_path),
            "--validation-only"
        ], capture_output=True, text=True, cwd=PROJECT_ROOT)

        print("📊 RESULTADOS DE VALIDACIÓN:")
        print("=" * 40)

        if result.stdout:
            print("✅ STDOUT:")
            print(result.stdout)

        if result.stderr:
            print("\n⚠️ STDERR:")
            print(result.stderr)

        print(f"\n🔢 Return Code: {result.returncode}")

        # 🎪 Interpretar resultados
        if result.returncode == 0:
            print("\n🎉 ¡VALIDACIÓN EXITOSA!")
            return True, "Sprint 1.1 funcionando correctamente"
        else:
            print("\n⚠️ VALIDACIÓN CON PROBLEMAS")
            return False, "Revisar output para identificar issues"

    except Exception as e:
        print(f"❌ ERROR ejecutando validación: {e}")
        return False, f"Error de ejecución: {e}"

def run_print_scan():
    """
    Ejecuta escaneo de print statements usando utilities/migration/
    """
    print("\n" + "=" * 70)
    print("🔍 ESCANEANDO PRINT STATEMENTS...")
    print("=" * 70)

    # 📁 Buscar herramienta de migración en utilities/migration/
    migration_tool_path = PROJECT_ROOT / "utilities" / "migration" / "print_migration_tool.py"

    if not migration_tool_path.exists():
        print(f"❌ ERROR: No se encuentra {migration_tool_path}")
        print("🔧 Nota: Este archivo debería estar en utilities/migration/")
        return False, "Migration tool no encontrado"

    try:
        # 🔍 Ejecutar escaneo
        result = subprocess.run([
            sys.executable,
            str(migration_tool_path),
            "--scan-only"
        ], capture_output=True, text=True, cwd=PROJECT_ROOT)

        print("📊 RESULTADOS DE ESCANEO:")
        print("-" * 40)

        if result.stdout:
            print(result.stdout)

        if result.stderr and result.stderr.strip():
            print("⚠️ Errores:")
            print(result.stderr)

        return result.returncode == 0, "Escaneo completado"

    except Exception as e:
        print(f"❌ ERROR ejecutando escaneo: {e}")
        return False, f"Error de escaneo: {e}"

def test_debug_launcher():
    """
    Prueba el debug launcher en utilities/debug/
    """
    print("\n" + "=" * 70)
    print("🔧 TESTING DEBUG LAUNCHER...")
    print("=" * 70)

    # 📁 Debug launcher en utilities/debug/
    launcher_path = PROJECT_ROOT / "utilities" / "debug" / "debug_launcher.py"

    if not launcher_path.exists():
        print(f"❌ ERROR: No se encuentra {launcher_path}")
        print("🔧 Nota: Este archivo debería estar en utilities/debug/")
        return False, "Debug launcher no encontrado"

    print(f"✅ Debug Launcher encontrado: {launcher_path}")

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

        print("🔍 VERIFICACIONES DEL DEBUG LAUNCHER:")
        print("-" * 40)

        for check_name, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"{status} {check_name}")

        # 📊 Resultado general
        passed_checks = sum(checks.values())
        total_checks = len(checks)

        print(f"\n📊 Resultado: {passed_checks}/{total_checks} verificaciones pasadas")

        if passed_checks >= 3:
            print("🎉 Debug Launcher parece estar bien implementado!")
            return True, f"Debug launcher OK ({passed_checks}/{total_checks})"
        else:
            print("⚠️ Debug Launcher necesita trabajo adicional")
            return False, f"Debug launcher incompleto ({passed_checks}/{total_checks})"

    except Exception as e:
        print(f"❌ ERROR verificando debug launcher: {e}")
        return False, f"Error verificando launcher: {e}"

def check_existing_structure():
    """
    Verifica la estructura existente del proyecto
    """
    print("\n" + "=" * 70)
    print("📁 VERIFICANDO ESTRUCTURA DEL PROYECTO...")
    print("=" * 70)

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
            print(f"✅ {dir_path}")
        else:
            missing_dirs.append(dir_path)
            print(f"❌ {dir_path}")

    print(f"\n📊 Estructura: {len(existing_dirs)}/{len(key_dirs)} directorios encontrados")

    return len(missing_dirs) == 0, f"Estructura: {len(existing_dirs)}/{len(key_dirs)}"

def main():
    """
    Función principal - ejecuta todas las validaciones
    """
    print("🎯 SPRINT 1.1 VALIDATION SUITE")
    print("🚀 Debug System & Clean Code")
    print("📅 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70)

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
        print(f"\n🔍 Ejecutando: {name}")
        try:
            success, detail = validation_func()
            results[name] = success
            details[name] = detail
        except Exception as e:
            print(f"❌ Error en {name}: {e}")
            results[name] = False
            details[name] = f"Error: {e}"

    # 📊 Reporte final
    print("\n" + "=" * 70)
    print("📊 REPORTE FINAL DE VALIDACIÓN")
    print("=" * 70)

    for name, passed in results.items():
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        detail = details.get(name, "")
        print(f"{status} {name} - {detail}")

    # 🎯 Conclusión
    passed_validations = sum(results.values())
    total_validations = len(results)

    print(f"\n🎪 RESULTADO GENERAL: {passed_validations}/{total_validations} validaciones exitosas")

    if passed_validations == total_validations:
        print("🎉 ¡SPRINT 1.1 COMPLETAMENTE VALIDADO!")
        print("✅ Sistema listo para Sprint 1.2")
    elif passed_validations >= total_validations // 2:
        print("⚠️ Sprint 1.1 parcialmente implementado")
        print("🔧 Revisar issues identificados antes de continuar")
    else:
        print("❌ Sprint 1.1 necesita trabajo significativo")
        print("🚨 Abordar problemas críticos antes de continuar")

    print(f"\n🔧 Ejecutado desde: {PROJECT_ROOT}")
    print("📂 Para re-ejecutar: python utilities/validation_runner.py")

    return passed_validations, total_validations

if __name__ == "__main__":
    main()
