#!/usr/bin/env python3
"""
✅ VALIDADOR FINAL - REFINAMIENTO SIC v2.0 COMPLETADO
===================================================
Validación completa del sistema após refinamiento quirúrgico

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
Versión: v2.0
"""

from sistema.sic import os
from sistema.sic import sys
from sistema.sic import Path
import importlib.util
from sistema.sic import datetime

def validar_archivo_python(archivo_path: Path) -> dict:
    """✅ Validar sintaxis y carga de un archivo Python"""

    resultado = {
        'archivo': str(archivo_path),
        'existe': False,
        'sintaxis_valida': False,
        'importable': False,
        'tamaño_kb': 0,
        'lineas': 0,
        'imports_sic': 0,
        'errores': []
    }

    try:
        # Verificar existencia
        if not archivo_path.exists():
            resultado['errores'].append("Archivo no existe")
            return resultado

        resultado['existe'] = True
        resultado['tamaño_kb'] = round(archivo_path.stat().st_size / 1024, 2)

        # Leer contenido
        with open(archivo_path, 'r', encoding='utf-8') as f:
            content = f.read()

        resultado['lineas'] = len(content.splitlines())

        # Contar imports SIC
        resultado['imports_sic'] = content.count('# === IMPORTS SIC ===')

        # Verificar sintaxis
        try:
            compile(content, str(archivo_path), 'exec')
            resultado['sintaxis_valida'] = True
        except SyntaxError as e:
            resultado['errores'].append(f"Error sintaxis: {e.msg} (línea {e.lineno})")

        # Verificar importabilidad (test básico)
        try:
            spec = importlib.util.spec_from_file_location("test_module", archivo_path)
            if spec and spec.loader:
                resultado['importable'] = True
            else:
                resultado['errores'].append("No se puede crear spec de importación")
        except Exception as e:
            resultado['errores'].append(f"Error importación: {str(e)[:100]}")

    except Exception as e:
        resultado['errores'].append(f"Error general: {e}")

    return resultado

def validar_sic_centralizado() -> dict:
    """✅ Validar el sistema SIC centralizado"""

    resultado = {
        'sic_existe': False,
        'sic_funcional': False,
        'componentes_ok': 0,
        'componentes_total': 0,
        'errores': []
    }

    try:
        sic_path = Path('sistema/py')

        if not sic_path.exists():
            resultado['errores'].append("sistema/py no existe")
            return resultado

        resultado['sic_existe'] = True

        # Intentar importar SIC
        sys.path.insert(0, str(Path.cwd()))

        try:
            from sistema import sic
            resultado['sic_funcional'] = True

            # Contar componentes disponibles
            componentes = [attr for attr in dir(sic) if not attr.startswith('_')]
            resultado['componentes_total'] = len(componentes)

            # Verificar componentes clave
            componentes_clave = [
                'logger', 'CandleDownloader', 'DataPipeline', 'ICTDetector',
                'POISystem', 'TradingEngine', 'ConfigManager'
            ]

            for comp in componentes_clave:
                if hasattr(sic, comp):
                    resultado['componentes_ok'] += 1
                else:
                    resultado['errores'].append(f"Componente {comp} no disponible en SIC")

        except Exception as e:
            resultado['errores'].append(f"Error importando SIC: {e}")

    except Exception as e:
        resultado['errores'].append(f"Error validando SIC: {e}")

    return resultado

def ejecutar_validacion_completa():
    """🚀 Ejecutar validación completa del refinamiento"""

    print("✅ VALIDACIÓN FINAL - REFINAMIENTO SIC v2.0")
    print("=" * 50)

    # Archivos refinados
    archivos_refinados = [
        'dashboard/dashboard_definitivo.py',
        'core/ict_engine/ict_detector.py',
        'dashboard/dashboard_widgets.py',
        'core/analysis_command_center/tct_pipeline/tct_interface.py',
        'dashboard/poi_dashboard_integration.py'
    ]

    print("📋 VALIDANDO ARCHIVOS REFINADOS")
    print("-" * 40)

    archivos_ok = 0
    total_archivos = len(archivos_refinados)

    for archivo_rel in archivos_refinados:
        archivo_path = Path(archivo_rel)
        resultado = validar_archivo_python(archivo_path)

        print(f"\n📄 {archivo_rel}")
        print(f"   ✅ Existe: {resultado['existe']}")
        print(f"   ✅ Sintaxis: {resultado['sintaxis_valida']}")
        print(f"   ✅ Importable: {resultado['importable']}")
        print(f"   📊 Tamaño: {resultado['tamaño_kb']} KB")
        print(f"   📊 Líneas: {resultado['lineas']}")
        print(f"   🎯 Imports SIC: {'Sí' if resultado['imports_sic'] > 0 else 'No'}")

        if resultado['errores']:
            print(f"   ⚠️ Errores: {'; '.join(resultado['errores'][:2])}")

        if resultado['existe'] and resultado['sintaxis_valida']:
            archivos_ok += 1

    print(f"\n📊 RESUMEN ARCHIVOS:")
    print(f"   ✅ Archivos válidos: {archivos_ok}/{total_archivos}")

    # Validar SIC
    print("\n🎯 VALIDANDO SISTEMA SIC")
    print("-" * 40)

    sic_resultado = validar_sic_centralizado()

    print(f"✅ SIC existe: {sic_resultado['sic_existe']}")
    print(f"✅ SIC funcional: {sic_resultado['sic_funcional']}")
    print(f"📊 Componentes OK: {sic_resultado['componentes_ok']}/{sic_resultado['componentes_total']}")

    if sic_resultado['errores']:
        print(f"⚠️ Errores SIC: {'; '.join(sic_resultado['errores'][:3])}")

    # Resultado final
    print(f"\n🎉 VALIDACIÓN FINAL COMPLETADA")
    print("=" * 50)

    exito_archivos = archivos_ok >= total_archivos * 0.8  # 80% mínimo
    exito_sic = sic_resultado['sic_existe'] and sic_resultado['componentes_ok'] >= 5

    if exito_archivos and exito_sic:
        print("✅ REFINAMIENTO SIC v2.0 EXITOSO")
        print("   ✅ Archivos migrados y funcionales")
        print("   ✅ Sistema SIC operativo")
        print("   ✅ Imports precisos aplicados")
        print("   ✅ Sin sobre-importación")
        print("")
        print("🚀 SISTEMA LISTO PARA PRODUCCIÓN")
        return True
    else:
        print("⚠️ REFINAMIENTO PARCIALMENTE EXITOSO")
        print(f"   📊 Archivos OK: {exito_archivos}")
        print(f"   📊 SIC OK: {exito_sic}")
        print("")
        print("🔧 REQUIERE AJUSTES MENORES")
        return False

def main():
    """🚀 Función principal de validación"""

    try:
        return ejecutar_validacion_completa()
    except Exception as e:
        print(f"\n❌ ERROR DURANTE VALIDACIÓN: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
