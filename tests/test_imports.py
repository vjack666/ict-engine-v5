#!/usr/bin/env python3
"""
Quick Import Test - verifica las importaciones principales del sistema
"""

def test_imports():
    """Prueba las importaciones críticas del sistema"""
    success_count = 0
    total_tests = 0

    print("🔍 INICIANDO PRUEBAS DE IMPORTACIÓN...")

    # Test 1: Core modules
    try:
        total_tests += 1
        from core.ict_engine.ict_detector import MarketContext
        print("✅ MarketContext importado correctamente")
        success_count += 1
    except Exception as e:
        print(f"❌ Error importando MarketContext: {e}")

    try:
        total_tests += 1
        from core.analysis_command_center.tct_pipeline.tct_interface import TCTInterface
        print("✅ TCTInterface importado correctamente")
        success_count += 1
    except Exception as e:
        print(f"❌ Error importando TCTInterface: {e}")

    try:
        total_tests += 1
        from core.analysis_command_center.tct_pipeline.tct_aggregator import TCTAggregator
        print("✅ TCTAggregator importado correctamente")
        success_count += 1
    except Exception as e:
        print(f"❌ Error importando TCTAggregator: {e}")

    # Test 2: Check syntax in critical files
    import ast
    import os

    critical_files = [
        "core/analysis_command_center/tct_pipeline/tct_interface.py",
        "core/analysis_command_center/tct_pipeline/tct_aggregator.py",
        "core/ict_engine/veredicto_engine_v4.py"
    ]

    for file_path in critical_files:
        total_tests += 1
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            ast.parse(content)
            print(f"✅ Sintaxis correcta: {file_path}")
            success_count += 1
        except SyntaxError as e:
            print(f"❌ Error de sintaxis en {file_path}: {e}")
        except Exception as e:
            print(f"❌ Error verificando {file_path}: {e}")

    print(f"\n📊 RESUMEN: {success_count}/{total_tests} pruebas exitosas")

    if success_count == total_tests:
        print("🎉 TODAS LAS PRUEBAS PASARON!")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron")
        return False

if __name__ == "__main__":
    test_imports()
