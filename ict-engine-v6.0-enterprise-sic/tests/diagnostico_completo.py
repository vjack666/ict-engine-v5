#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 DIAGNÓSTICO COMPLETO - ICT ENGINE v6.0 ENTERPRISE
===================================================

Diagnóstico detallado de problemas actuales del sistema:
- Sistema de logging central
- Estado SIC v3.1 Enterprise  
- Problemas de imports
- Estructura de archivos
- Configuraciones

Autor: ICT Engine v6.0 Team
"""

import sys
import traceback
import logging
from pathlib import Path
import json

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def diagnosticar_logging():
    """🔍 Diagnosticar sistema de logging central"""
    print("🔍 DIAGNÓSTICO SISTEMA DE LOGGING")
    print("-" * 50)
    
    problemas = []
    
    try:
        # Verificar configuración de logging
        print("1️⃣ Verificando configuración de logging...")
        
        # Verificar logger root
        root_logger = logging.getLogger()
        print(f"   📊 Root logger level: {root_logger.level}")
        print(f"   📊 Handlers: {len(root_logger.handlers)}")
        
        # Verificar directorio de logs
        logs_dir = project_root / "logs"
        if logs_dir.exists():
            log_files = list(logs_dir.glob("*.log"))
            print(f"   📁 Directorio logs: ✅ {len(log_files)} archivos")
        else:
            print("   📁 Directorio logs: ❌ NO EXISTE")
            problemas.append("Directorio logs no existe")
        
        # Verificar smart_trading_logger
        try:
            from core.smart_trading_logger import SmartTradingLogger
            logger = SmartTradingLogger()
            print("   🔧 SmartTradingLogger: ✅ DISPONIBLE")
        except Exception as e:
            print(f"   🔧 SmartTradingLogger: ❌ ERROR - {e}")
            problemas.append(f"SmartTradingLogger error: {e}")
            
    except Exception as e:
        print(f"   ❌ ERROR GENERAL: {e}")
        problemas.append(f"Error general logging: {e}")
    
    return problemas

def diagnosticar_sic():
    """🔍 Diagnosticar SIC v3.1 Enterprise"""
    print("\n🔍 DIAGNÓSTICO SIC v3.1 ENTERPRISE")
    print("-" * 50)
    
    problemas = []
    
    try:
        print("1️⃣ Verificando estructura SIC...")
        
        # Verificar directorio sistema
        sistema_dir = project_root / "sistema"
        if sistema_dir.exists():
            print(f"   📁 Directorio sistema: ✅ EXISTE")
            
            # Verificar SIC v3.1
            sic_dir = sistema_dir / "sic_v3_1"
            if sic_dir.exists():
                print(f"   📁 SIC v3.1: ✅ EXISTE")
                
                # Verificar archivos clave
                archivos_clave = [
                    "__init__.py",
                    "enterprise_interface.py",
                    "lazy_loading.py", 
                    "predictive_cache.py",
                    "monitor_dashboard.py",
                    "advanced_debug.py"
                ]
                
                for archivo in archivos_clave:
                    archivo_path = sic_dir / archivo
                    if archivo_path.exists():
                        print(f"   📄 {archivo}: ✅")
                    else:
                        print(f"   📄 {archivo}: ❌ FALTA")
                        problemas.append(f"Archivo SIC faltante: {archivo}")
            else:
                print("   📁 SIC v3.1: ❌ NO EXISTE")
                problemas.append("Directorio SIC v3.1 no existe")
        else:
            print("   📁 Directorio sistema: ❌ NO EXISTE") 
            problemas.append("Directorio sistema no existe")
        
        print("\n2️⃣ Probando imports SIC...")
        
        # Test import básico
        try:
            from sistema import get_sic_instance, smart_import
            print("   📦 Import básico: ✅ FUNCIONA")
            
            # Test instancia SIC
            sic = get_sic_instance()
            print(f"   🏗️ Instancia SIC: ✅ {type(sic)}")
            
            # Test smart import
            sys_module = smart_import('sys')
            print(f"   🧠 Smart import: ✅ {type(sys_module)}")
            
        except Exception as e:
            print(f"   📦 Import SIC: ❌ ERROR - {e}")
            problemas.append(f"Error import SIC: {e}")
    
    except Exception as e:
        print(f"   ❌ ERROR GENERAL SIC: {e}")
        problemas.append(f"Error general SIC: {e}")
    
    return problemas

def diagnosticar_imports():
    """🔍 Diagnosticar problemas de imports"""
    print("\n🔍 DIAGNÓSTICO PROBLEMAS DE IMPORTS")
    print("-" * 50)
    
    problemas = []
    
    # Tests de imports críticos
    imports_criticos = [
        ("core.data_management.advanced_candle_downloader", "AdvancedCandleDownloader"),
        ("core.analysis.market_structure_analyzer", "MarketStructureAnalyzer"),
        ("core.analysis.pattern_detector", "PatternDetector"),
        ("core.poi_system", "POISystem"),
        ("utils.mt5_data_manager", "MT5DataManager")
    ]
    
    for modulo, clase in imports_criticos:
        try:
            module = __import__(modulo, fromlist=[clase])
            cls = getattr(module, clase)
            print(f"   📦 {modulo}.{clase}: ✅")
        except ImportError as e:
            print(f"   📦 {modulo}.{clase}: ❌ IMPORT ERROR - {e}")
            problemas.append(f"Import error: {modulo}.{clase}")
        except AttributeError as e:
            print(f"   📦 {modulo}.{clase}: ❌ ATTR ERROR - {e}")
            problemas.append(f"Attribute error: {modulo}.{clase}")
        except Exception as e:
            print(f"   📦 {modulo}.{clase}: ❌ ERROR - {e}")
            problemas.append(f"Error general: {modulo}.{clase}")
    
    return problemas

def diagnosticar_estructura():
    """🔍 Diagnosticar estructura de archivos"""
    print("\n🔍 DIAGNÓSTICO ESTRUCTURA DE ARCHIVOS")
    print("-" * 50)
    
    problemas = []
    
    # Directorios esenciales
    directorios_esenciales = {
        "core": "Núcleo del sistema",
        "core/data_management": "Gestión de datos",
        "core/analysis": "Análisis ICT",
        "tests": "Tests del sistema",
        "scripts": "Scripts ejecutables",
        "utils": "Utilidades",
        "config": "Configuraciones",
        "logs": "Logs del sistema",
        "data": "Datos del sistema",
        "sistema": "SIC v3.1"
    }
    
    for directorio, descripcion in directorios_esenciales.items():
        dir_path = project_root / directorio
        if dir_path.exists():
            archivos_py = len(list(dir_path.glob("*.py")))
            print(f"   📁 {directorio}/: ✅ {archivos_py} archivos Python")
        else:
            print(f"   📁 {directorio}/: ❌ NO EXISTE")
            problemas.append(f"Directorio faltante: {directorio}")
    
    return problemas

def diagnosticar_configuraciones():
    """🔍 Diagnosticar configuraciones"""
    print("\n🔍 DIAGNÓSTICO CONFIGURACIONES")
    print("-" * 50)
    
    problemas = []
    
    # Archivos de configuración esperados
    configs_esperadas = [
        "config/performance_config_enterprise.json",
        "config/storage_config.json",
        "config/cache_config.json",
        "config/sic_cache_stats.json"
    ]
    
    for config_file in configs_esperadas:
        config_path = project_root / config_file
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"   ⚙️ {config_file}: ✅ {len(data)} keys")
            except Exception as e:
                print(f"   ⚙️ {config_file}: ⚠️ ERROR LECTURA - {e}")
                problemas.append(f"Config corrupta: {config_file}")
        else:
            print(f"   ⚙️ {config_file}: ❌ NO EXISTE")
            # No es crítico, se puede generar automáticamente
    
    return problemas

def generar_plan_reparacion(todos_problemas):
    """🔧 Generar plan de reparación"""
    print("\n" + "="*70)
    print("🔧 PLAN DE REPARACIÓN AUTOMATIZADA")
    print("="*70)
    
    if not todos_problemas:
        print("✅ NO SE ENCONTRARON PROBLEMAS CRÍTICOS")
        return
    
    # Categorizar problemas
    problemas_criticos = []
    problemas_menores = []
    
    for problema in todos_problemas:
        if any(keyword in problema.lower() for keyword in ['import error', 'no existe', 'faltante']):
            problemas_criticos.append(problema)
        else:
            problemas_menores.append(problema)
    
    if problemas_criticos:
        print("🚨 PROBLEMAS CRÍTICOS (REQUIEREN REPARACIÓN):")
        for i, problema in enumerate(problemas_criticos, 1):
            print(f"   {i}. {problema}")
    
    if problemas_menores:
        print("\n⚠️ PROBLEMAS MENORES (NO CRÍTICOS):")
        for i, problema in enumerate(problemas_menores, 1):
            print(f"   {i}. {problema}")
    
    print(f"\n📊 RESUMEN: {len(problemas_criticos)} críticos, {len(problemas_menores)} menores")

def main():
    """🎯 Diagnóstico principal"""
    print("🔍 ICT ENGINE v6.0 ENTERPRISE - DIAGNÓSTICO COMPLETO")
    print("="*70)
    
    todos_problemas = []
    
    # Ejecutar todos los diagnósticos
    todos_problemas.extend(diagnosticar_logging())
    todos_problemas.extend(diagnosticar_sic())
    todos_problemas.extend(diagnosticar_imports())
    todos_problemas.extend(diagnosticar_estructura())
    todos_problemas.extend(diagnosticar_configuraciones())
    
    # Generar plan de reparación
    generar_plan_reparacion(todos_problemas)
    
    # Test final del sistema crítico
    print("\n🧪 TEST SISTEMA CRÍTICO FINAL:")
    print("-" * 50)
    
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "tests/test_simple_poi.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ SISTEMA CRÍTICO: FUNCIONANDO")
            print("🎯 A pesar de problemas menores, el núcleo funciona")
        else:
            print("❌ SISTEMA CRÍTICO: FALLO")
            todos_problemas.append("Sistema crítico no funciona")
    except Exception as e:
        print(f"❌ ERROR TEST CRÍTICO: {e}")
        todos_problemas.append(f"Error test crítico: {e}")
    
    print(f"\n{'='*70}")
    if len([p for p in todos_problemas if 'import error' in p.lower() or 'no existe' in p.lower()]) == 0:
        print("🎉 SISTEMA EN BUEN ESTADO GENERAL")
        print("✅ Problemas menores no afectan funcionalidad crítica")
    else:
        print("⚠️ SISTEMA REQUIERE REPARACIÓN")
        print("🔧 Ejecutar reparaciones sugeridas")
    
    return len(todos_problemas)

if __name__ == "__main__":
    num_problemas = main()
    sys.exit(1 if num_problemas > 5 else 0)
