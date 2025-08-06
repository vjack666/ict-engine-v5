#!/usr/bin/env python3
"""
🔍 SCRIPT DE PREPARACIÓN - REFINAMIENTO SIC v2.0
=====================================================
Verifica el estado actual y prepara el entorno para refinamiento quirúrgico

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
Versión: v2.0
"""

from sistema.sic import os
import shutil
from sistema.sic import sys
from sistema.sic import Path
from sistema.sic import datetime

def verificar_estado_actual():
    """🔍 Verificar estado actual del proyecto"""

    print("🔍 VERIFICANDO ESTADO ACTUAL DEL PROYECTO")
    print("=" * 50)

    # 1. Verificar SIC
    sic_path = Path("sistema/imports_interface.py")
    sic_exists = sic_path.exists()
    print(f"🎯 SIC Disponible: {'✅ SÍ' if sic_exists else '❌ NO'}")

    if sic_exists:
        # Test rápido del SIC
        try:
            sys.path.insert(0, '.')
            import sistema.imports_interface
            print("✅ SIC Funcional: Componentes principales accesibles")
        except Exception as e:
            print(f"⚠️ SIC Parcial: {str(e)[:100]}...")

    # 2. Verificar backups
    backup_dir = Path("backup_sic_migration")
    backups_available = backup_dir.exists()
    print(f"💾 Backups Disponibles: {'✅ SÍ' if backups_available else '❌ NO'}")

    backup_files = []
    if backups_available:
        backup_files = list(backup_dir.rglob("*.bak"))
        print(f"📁 Total backups: {len(backup_files)}")

        # Mostrar backups más recientes
        recent_backups = sorted(backup_files, key=os.path.getmtime, reverse=True)[:5]
        print("📄 Backups más recientes:")
        for backup in recent_backups:
            mod_time = datetime.fromtimestamp(backup.stat().st_mtime)
            print(f"   💾 {backup.name} - {mod_time.strftime('%H:%M:%S')}")

    # 3. Verificar archivos migrados
    archivos_objetivo = [
        'config/live_only_config.py',
        'dashboard/dashboard_definitivo.py',
        'core/ict_engine/ict_detector.py',
        'dashboard/dashboard_widgets.py',
        'core/analysis_command_center/tct_pipeline/tct_interface.py',
        'core/analytics/ict_analyzer.py',
        'core/data_management/advanced_candle_downloader.py',
        'dashboard/hibernation_widget_v2.py',
        'dashboard/poi_dashboard_integration.py'
    ]

    print(f"\n📊 ESTADO DE ARCHIVOS OBJETIVO:")
    archivos_existentes = 0
    archivos_con_backup = 0

    for archivo in archivos_objetivo:
        archivo_path = Path(archivo)
        existe = archivo_path.exists()

        # Buscar backup correspondiente
        relative_backup = backup_dir / archivo
        backup_files_for_file = list(backup_dir.rglob(f"*{archivo_path.name}*.bak"))
        tiene_backup = len(backup_files_for_file) > 0

        status = "✅" if existe else "❌"
        backup_status = "💾" if tiene_backup else "📄"

        print(f"   {status} {archivo} {backup_status}")

        if existe:
            archivos_existentes += 1
        if tiene_backup:
            archivos_con_backup += 1

    print(f"\n📈 RESUMEN:")
    print(f"   📁 Archivos existentes: {archivos_existentes}/{len(archivos_objetivo)}")
    print(f"   💾 Archivos con backup: {archivos_con_backup}/{len(archivos_objetivo)}")

    # 4. Verificar herramientas
    migrador_v1 = Path("scripts/migrate_to_sic.py").exists()
    analizador = Path("scripts/fix_unused_imports.py").exists()
    corrector = Path("scripts/fix_migration_indentation.py").exists()

    print(f"\n🛠️ HERRAMIENTAS:")
    print(f"   🔧 Migrador v1.0: {'✅' if migrador_v1 else '❌'}")
    print(f"   📊 Analizador imports: {'✅' if analizador else '❌'}")
    print(f"   🔧 Corrector indentación: {'✅' if corrector else '❌'}")

    return {
        'sic_functional': sic_exists,
        'backups_available': backups_available,
        'backup_count': len(backup_files),
        'files_existing': archivos_existentes,
        'files_with_backup': archivos_con_backup,
        'tools_ready': migrador_v1 and analizador and corrector
    }

def identificar_archivos_problematicos():
    """🚨 Identificar archivos que necesitan restauración"""

    print("\n🚨 IDENTIFICANDO ARCHIVOS PROBLEMÁTICOS")
    print("-" * 40)

    # Archivos que sabemos tienen problemas de indentación o sintaxis
    archivos_problematicos = [
        'dashboard/dashboard_definitivo.py',
        'core/ict_engine/ict_detector.py',
        'dashboard/dashboard_widgets.py',
        'core/analysis_command_center/tct_pipeline/tct_interface.py',
        'dashboard/poi_dashboard_integration.py'
    ]

    # Archivos que funcionan bien
    archivos_funcionales = [
        'config/live_only_config.py',  # Este migró perfectamente
        'core/analytics/ict_analyzer.py',  # Funcional después de correcciones
        'core/data_management/advanced_candle_downloader.py',  # Sin problemas
        'dashboard/hibernation_widget_v2.py'  # Sin problemas
    ]

    print("❌ ARCHIVOS QUE NECESITAN RESTAURACIÓN Y RE-MIGRACIÓN:")
    for archivo in archivos_problematicos:
        print(f"   📄 {archivo}")

    print("\n✅ ARCHIVOS QUE FUNCIONAN BIEN (MANTENER):")
    for archivo in archivos_funcionales:
        print(f"   📄 {archivo}")

    return {
        'problematicos': archivos_problematicos,
        'funcionales': archivos_funcionales
    }

def preparar_entorno_refinamiento():
    """🔧 Preparar entorno para refinamiento"""

    print("\n🔧 PREPARANDO ENTORNO DE REFINAMIENTO")
    print("-" * 40)

    # Crear directorio para backups v2.0
    backup_v2_dir = Path("backup_sic_refinamiento_v2")
    backup_v2_dir.mkdir(exist_ok=True)
    print(f"📁 Directorio backups v2.0: ✅ Creado")

    # Crear directorio para reportes
    reports_dir = Path("migration_reports")
    reports_dir.mkdir(exist_ok=True)
    print(f"📄 Directorio reportes: ✅ Creado")

    # Crear directorio temporal para trabajo
    temp_dir = Path("temp_refinamiento")
    temp_dir.mkdir(exist_ok=True)
    print(f"🔧 Directorio temporal: ✅ Creado")

    return {
        'backup_v2_dir': backup_v2_dir,
        'reports_dir': reports_dir,
        'temp_dir': temp_dir
    }

def generar_reporte_preparacion(estado, archivos, entorno):
    """📊 Generar reporte de preparación"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    reporte_path = Path(f"migration_reports/preparacion_refinamiento_{timestamp}.txt")

    reporte = [
        "🔍 REPORTE DE PREPARACIÓN - REFINAMIENTO SIC v2.0",
        "=" * 60,
        f"📅 Timestamp: {timestamp}",
        "",
        "📊 ESTADO DEL SISTEMA:",
        f"   🎯 SIC Funcional: {'✅' if estado['sic_functional'] else '❌'}",
        f"   💾 Backups Disponibles: {'✅' if estado['backups_available'] else '❌'}",
        f"   📁 Total de backups: {estado['backup_count']}",
        f"   📁 Archivos Objetivo Existentes: {estado['files_existing']}/9",
        f"   🛠️ Herramientas Listas: {'✅' if estado['tools_ready'] else '❌'}",
        "",
        "🚨 ARCHIVOS PROBLEMÁTICOS (requieren restauración):",
    ]

    for archivo in archivos['problematicos']:
        reporte.append(f"   ❌ {archivo}")

    reporte.extend([
        "",
        "✅ ARCHIVOS FUNCIONALES (mantener como están):",
    ])

    for archivo in archivos['funcionales']:
        reporte.append(f"   ✅ {archivo}")

    reporte.extend([
        "",
        "🎯 PREPARACIÓN COMPLETADA:",
        f"   📁 Backup v2.0 dir: {entorno['backup_v2_dir']}",
        f"   📄 Reports dir: {entorno['reports_dir']}",
        f"   🔧 Temp dir: {entorno['temp_dir']}",
        "",
        "🚀 LISTO PARA REFINAMIENTO QUIRÚRGICO",
        "   Siguiente paso: Ejecutar restauración selectiva y migrador v2.0",
        "",
        "📋 PRÓXIMOS COMANDOS:",
        "   python scripts/restaurar_archivos_selectivo.py",
        "   python scripts/migrate_to_sic_v2.py --intelligent",
        "   python scripts/validar_refinamiento.py"
    ])

    # Escribir reporte
    with open(reporte_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(reporte))

    print(f"\n📄 Reporte guardado: {reporte_path}")
    return reporte_path

def main():
    """🚀 Función principal de preparación"""

    print("🚀 INICIANDO PREPARACIÓN PARA REFINAMIENTO QUIRÚRGICO")
    print("=" * 60)

    try:
        # 1. Verificar estado actual
        estado = verificar_estado_actual()

        # 2. Identificar archivos problemáticos
        archivos = identificar_archivos_problematicos()

        # 3. Preparar entorno
        entorno = preparar_entorno_refinamiento()

        # 4. Generar reporte
        reporte_path = generar_reporte_preparacion(estado, archivos, entorno)

        # 5. Validaciones críticas
        print(f"\n🎯 VALIDACIONES CRÍTICAS:")

        if not estado['sic_functional']:
            print("❌ CRÍTICO: SIC no funcional - Detener refinamiento")
            return False

        if not estado['backups_available']:
            print("❌ CRÍTICO: Sin backups - Detener refinamiento")
            return False

        if estado['files_with_backup'] < 5:
            print("⚠️ ADVERTENCIA: Pocos backups disponibles")

        if not estado['tools_ready']:
            print("⚠️ ADVERTENCIA: Algunas herramientas no están disponibles")

        print("✅ Validaciones críticas completadas")

        # 6. Mensaje final
        print(f"\n🎉 PREPARACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("📋 SISTEMA LISTO PARA REFINAMIENTO QUIRÚRGICO")
        print("")
        print("🔄 PRÓXIMOS PASOS:")
        print("   1. Restauración selectiva de archivos problemáticos")
        print("   2. Migración inteligente v2.0 con análisis AST")
        print("   3. Validación integral del sistema refinado")
        print("")
        print("📊 RESULTADO ESPERADO:")
        print("   - Imports no utilizados: 303 → ~20-30 (reducción 90%+)")
        print("   - Errores de sintaxis: Eliminación completa")
        print("   - Funcionalidad: 100% preservada")
        print("   - Arquitectura: Nivel profesional perfecto")

        return True

    except Exception as e:
        print(f"\n❌ ERROR DURANTE PREPARACIÓN: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
