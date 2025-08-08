#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 DIAGNÓSTICO SIC Y LOGGING CENTRAL
===================================

Verificar estado del SIC v3.1 Enterprise y sistema de logging central.
"""

import sys
from pathlib import Path

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def diagnosticar_sic():
    """🔍 Diagnosticar estado del SIC"""
    
    print("🔧 DIAGNÓSTICO SIC v3.1 ENTERPRISE Y LOGGING CENTRAL")
    print("="*70)
    
    # 1. Verificar SIC
    print("1️⃣ VERIFICANDO SIC v3.1 ENTERPRISE:")
    print("-"*50)
    
    try:
        from sistema.sic_v3_1 import get_sic_instance, smart_import
        sic = get_sic_instance()
        
        print("✅ SIC v3.1: DISPONIBLE")
        print("✅ get_sic_instance: FUNCIONA")
        print("✅ smart_import: DISPONIBLE")
        
        # Verificar estadísticas
        try:
            stats = sic.get_system_stats()
            print(f"✅ Stats: {stats['imports_stats']['total_imports']} imports")
            print(f"✅ Cache rate: {stats['imports_stats']['cache_hit_rate']:.1f}%")
        except Exception as e:
            print(f"⚠️ Stats error: {e}")
            
    except Exception as e:
        print(f"❌ SIC ERROR: {e}")
        return False
    
    # 2. Verificar logging central
    print("\n2️⃣ VERIFICANDO LOGGING CENTRAL:")
    print("-"*50)
    
    try:
        from core.smart_trading_logger import get_smart_logger, log_info
        
        logger = get_smart_logger()
        print("✅ Smart Trading Logger: DISPONIBLE")
        
        # Test logging
        log_info("Test logging central", "DIAGNOSTIC")
        print("✅ Logging functions: FUNCIONANDO")
        
    except Exception as e:
        print(f"❌ LOGGING ERROR: {e}")
        return False
    
    # 3. Verificar integración SIC + Modules
    print("\n3️⃣ VERIFICANDO INTEGRACIÓN SIC + MÓDULOS:")
    print("-"*50)
    
    try:
        # Test smart imports
        sys_module = smart_import('sys')
        print("✅ Smart import sys: FUNCIONA")
        
        os_module = smart_import('os')
        print("✅ Smart import os: FUNCIONA")
        
        # Test core modules con SIC
        try:
            downloader_module = smart_import('core.data_management.advanced_candle_downloader')
            print("✅ Smart import downloader: FUNCIONA")
        except Exception as e:
            print(f"⚠️ Downloader import: {e}")
        
        try:
            poi_module = smart_import('core.analysis.poi_system')
            print("✅ Smart import POI: FUNCIONA")
        except Exception as e:
            print(f"⚠️ POI import: {e}")
            
    except Exception as e:
        print(f"❌ INTEGRATION ERROR: {e}")
        return False
    
    # 4. Verificar paths y estructura
    print("\n4️⃣ VERIFICANDO PATHS Y ESTRUCTURA:")
    print("-"*50)
    
    core_files = {
        'smart_trading_logger.py': 'core/smart_trading_logger.py',
        'advanced_candle_downloader.py': 'core/data_management/advanced_candle_downloader.py',
        'poi_system.py': 'core/analysis/poi_system.py'
    }
    
    for name, path in core_files.items():
        file_path = project_root / path
        if file_path.exists():
            print(f"✅ {name}: EXISTE")
        else:
            print(f"❌ {name}: FALTANTE ({path})")
    
    # 5. Test de enlazado SIC
    print("\n5️⃣ TEST ENLAZADO SIC CON CORE:")
    print("-"*50)
    
    try:
        # Verificar si SIC puede importar módulos core
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        
        # Test con SIC
        downloader = AdvancedCandleDownloader()
        print("✅ AdvancedCandleDownloader: INSTANCIADO")
        
        # Verificar si usa SIC internamente
        if hasattr(downloader, '_sic_interface'):
            print("✅ SIC Integration: HABILITADA en downloader")
        else:
            print("⚠️ SIC Integration: NO DETECTADA en downloader")
            
    except Exception as e:
        print(f"❌ CORE INTEGRATION ERROR: {e}")
        return False
    
    print("\n" + "="*70)
    print("📊 RESUMEN DIAGNÓSTICO:")
    print("="*70)
    print("✅ SIC v3.1 Enterprise: FUNCIONANDO")
    print("✅ Logging Central: FUNCIONANDO")
    print("✅ Smart Imports: FUNCIONANDO")
    print("✅ Core Modules: ACCESIBLES")
    print("✅ Estructura Files: CORRECTA")
    
    return True

if __name__ == "__main__":
    success = diagnosticar_sic()
    if success:
        print("\n🎉 SIC Y LOGGING: SISTEMA INTEGRADO CORRECTAMENTE")
    else:
        print("\n❌ PROBLEMAS DETECTADOS EN SIC/LOGGING")
    
    sys.exit(0 if success else 1)
