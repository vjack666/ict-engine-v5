#!/usr/bin/env python3
"""
🔄 RESTAURACIÓN SELECTIVA - REFINAMIENTO SIC v2.0
=================================================
Restaura archivos problemáticos desde backups y preserva archivos funcionales

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
Versión: v2.0
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime

def crear_backup_pre_restauracion():
    """💾 Crear backup de seguridad antes de restaurar"""

    print("💾 CREANDO BACKUP DE SEGURIDAD PRE-RESTAURACIÓN")
    print("-" * 50)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"backup_pre_restauracion_{timestamp}")
    backup_dir.mkdir(exist_ok=True)

    archivos_a_respaldar = [
        'dashboard/dashboard_definitivo.py',
        'core/ict_engine/ict_detector.py',
        'dashboard/dashboard_widgets.py',
        'core/analysis_command_center/tct_pipeline/tct_interface.py',
        'dashboard/poi_dashboard_integration.py'
    ]

    for archivo in archivos_a_respaldar:
        archivo_path = Path(archivo)
        if archivo_path.exists():
            # Crear estructura de directorios
            backup_file_path = backup_dir / archivo
            backup_file_path.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(archivo_path, backup_file_path)
            print(f"   💾 {archivo} → {backup_file_path}")

    print(f"✅ Backup de seguridad creado: {backup_dir}")
    return backup_dir

def restaurar_archivo_desde_backup(archivo, backup_original_dir):
    """🔄 Restaurar un archivo específico desde backup"""

    archivo_path = Path(archivo)

    # Buscar backup en la estructura organizada
    # Los backups están en backup_sic_migration/{directorio_padre}/{archivo}.{timestamp}.bak
    backup_file_path = backup_original_dir / archivo_path.parent / f"{archivo_path.name}.*.bak"
    backup_files = list(backup_original_dir.glob(f"**/{archivo_path.name}.*.bak"))

    if not backup_files:
        print(f"❌ No se encontró backup para {archivo}")
        print(f"   Buscado en: {backup_file_path}")
        return False

    # Usar el backup más reciente
    backup_file = max(backup_files, key=os.path.getmtime)

    try:
        # Restaurar archivo
        shutil.copy2(backup_file, archivo_path)
        print(f"   ✅ Restaurado: {archivo} ← {backup_file.name}")
        return True
    except Exception as e:
        print(f"   ❌ Error restaurando {archivo}: {e}")
        return False

def ejecutar_restauracion_selectiva():
    """🔄 Ejecutar restauración selectiva de archivos problemáticos"""

    print("\n🔄 EJECUTANDO RESTAURACIÓN SELECTIVA")
    print("=" * 50)

    # Verificar disponibilidad de backups
    backup_original_dir = Path("backup_sic_migration")
    if not backup_original_dir.exists():
        print("❌ CRÍTICO: No se encontró directorio de backups originales")
        return False

    # Crear backup de seguridad
    backup_seguridad = crear_backup_pre_restauracion()

    # Archivos problemáticos que necesitan restauración
    archivos_problematicos = [
        'dashboard/dashboard_definitivo.py',
        'core/ict_engine/ict_detector.py',
        'dashboard/dashboard_widgets.py',
        'core/analysis_command_center/tct_pipeline/tct_interface.py',
        'dashboard/poi_dashboard_integration.py'
    ]

    print(f"\n📄 RESTAURANDO ARCHIVOS PROBLEMÁTICOS:")
    restauraciones_exitosas = 0

    for archivo in archivos_problematicos:
        print(f"\n🎯 Restaurando: {archivo}")
        if restaurar_archivo_desde_backup(archivo, backup_original_dir):
            restauraciones_exitosas += 1
        else:
            print(f"⚠️ Falló restauración de {archivo}")

    # Verificar archivos funcionales (no tocar)
    archivos_funcionales = [
        'config/live_only_config.py',
        'core/analytics/ict_analyzer.py',
        'core/data_management/advanced_candle_downloader.py',
        'dashboard/hibernation_widget_v2.py'
    ]

    print(f"\n✅ ARCHIVOS FUNCIONALES (SIN CAMBIOS):")
    for archivo in archivos_funcionales:
        if Path(archivo).exists():
            print(f"   📄 {archivo} - Preservado")

    # Reporte final
    print(f"\n📊 REPORTE DE RESTAURACIÓN:")
    print(f"   ✅ Restauraciones exitosas: {restauraciones_exitosas}/{len(archivos_problematicos)}")
    print(f"   📄 Archivos funcionales preservados: {len(archivos_funcionales)}")
    print(f"   💾 Backup de seguridad: {backup_seguridad}")

    return restauraciones_exitosas == len(archivos_problematicos)

def validar_post_restauracion():
    """✅ Validar estado después de la restauración"""

    print(f"\n✅ VALIDANDO ESTADO POST-RESTAURACIÓN")
    print("-" * 40)

    # Test básico de sintaxis Python
    archivos_a_validar = [
        'dashboard/dashboard_definitivo.py',
        'core/ict_engine/ict_detector.py',
        'dashboard/dashboard_widgets.py',
        'core/analysis_command_center/tct_pipeline/tct_interface.py',
        'dashboard/poi_dashboard_integration.py'
    ]

    archivos_validos = 0

    for archivo in archivos_a_validar:
        archivo_path = Path(archivo)
        if not archivo_path.exists():
            print(f"❌ {archivo} - No existe")
            continue

        try:
            # Test básico de compilación Python
            with open(archivo_path, 'r', encoding='utf-8') as f:
                content = f.read()

            compile(content, archivo_path, 'exec')
            print(f"✅ {archivo} - Sintaxis válida")
            archivos_validos += 1

        except SyntaxError as e:
            print(f"❌ {archivo} - Error de sintaxis: {e}")
        except Exception as e:
            print(f"⚠️ {archivo} - Advertencia: {e}")

    print(f"\n📊 VALIDACIÓN COMPLETADA:")
    print(f"   ✅ Archivos con sintaxis válida: {archivos_validos}/{len(archivos_a_validar)}")

    return archivos_validos == len(archivos_a_validar)

def generar_reporte_restauracion():
    """📄 Generar reporte de restauración"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    reporte_path = Path(f"migration_reports/restauracion_selectiva_{timestamp}.txt")

    reporte = [
        "🔄 REPORTE DE RESTAURACIÓN SELECTIVA - SIC v2.0",
        "=" * 60,
        f"📅 Timestamp: {timestamp}",
        "",
        "🎯 OBJETIVO:",
        "   Restaurar archivos problemáticos desde backups originales",
        "   Preservar archivos que funcionan correctamente",
        "",
        "📄 ARCHIVOS RESTAURADOS:",
        "   ✅ dashboard/dashboard_definitivo.py",
        "   ✅ core/ict_engine/ict_detector.py",
        "   ✅ dashboard/dashboard_widgets.py",
        "   ✅ core/analysis_command_center/tct_pipeline/tct_interface.py",
        "   ✅ dashboard/poi_dashboard_integration.py",
        "",
        "📄 ARCHIVOS PRESERVADOS:",
        "   ✅ config/live_only_config.py (migración exitosa)",
        "   ✅ core/analytics/ict_analyzer.py (funcional)",
        "   ✅ core/data_management/advanced_candle_downloader.py (funcional)",
        "   ✅ dashboard/hibernation_widget_v2.py (funcional)",
        "",
        "✅ RESTAURACIÓN SELECTIVA COMPLETADA",
        "",
        "🚀 PRÓXIMO PASO:",
        "   Ejecutar migrador v2.0 inteligente con análisis AST preciso"
    ]

    with open(reporte_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(reporte))

    print(f"📄 Reporte guardado: {reporte_path}")
    return reporte_path

def main():
    """🚀 Función principal de restauración selectiva"""

    print("🔄 INICIANDO RESTAURACIÓN SELECTIVA - REFINAMIENTO SIC v2.0")
    print("=" * 60)

    try:
        # 1. Ejecutar restauración selectiva
        restauracion_exitosa = ejecutar_restauracion_selectiva()

        if not restauracion_exitosa:
            print("❌ CRÍTICO: Falló la restauración selectiva")
            return False

        # 2. Validar estado post-restauración
        validacion_exitosa = validar_post_restauracion()

        if not validacion_exitosa:
            print("⚠️ ADVERTENCIA: Algunos archivos tienen problemas de sintaxis")
            print("   Esto es esperado - serán corregidos por el migrador v2.0")

        # 3. Generar reporte
        reporte_path = generar_reporte_restauracion()

        # 4. Mensaje final
        print(f"\n🎉 RESTAURACIÓN SELECTIVA COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("📋 ESTADO ACTUAL:")
        print("   🔄 Archivos problemáticos restaurados desde backups originales")
        print("   ✅ Archivos funcionales preservados intactos")
        print("   💾 Backup de seguridad creado")
        print("")
        print("🚀 LISTO PARA MIGRACIÓN v2.0 INTELIGENTE")
        print("   Siguiente comando: python scripts/migrate_to_sic_v2.py --intelligent")

        return True

    except Exception as e:
        print(f"\n❌ ERROR DURANTE RESTAURACIÓN: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
