#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 TEST SIC-DOWNLOADER INTEGRATION
==================================

Test específico para diagnosticar la integración entre SIC v3.1 y el Downloader.
Identifica y repara problemas de:
- Importaciones fallidas
- Cache miss en sistema predictivo
- Conexión SIC-Downloader

Autor: ICT Engine v6.0 Team
"""

import sys
import os
from pathlib import Path

# Agregar paths necesarios
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "sistema" / "sic_v3_1"))

def test_sic_imports():
    """🔍 Test de importaciones SIC"""
    print("🔍 DIAGNÓSTICO SIC-DOWNLOADER INTEGRATION")
    print("="*60)
    
    # Test 1: Import básico de SIC v3.1
    print("📦 Test 1: Importaciones básicas SIC v3.1")
    try:
        from sistema.sic_v3_1.enterprise_interface import SICv31Enterprise
        print("✅ SICv31Enterprise: OK")
        sic_available = True
    except Exception as e:
        print(f"❌ SICv31Enterprise: FAILED - {e}")
        sic_available = False
    
    try:
        from sistema.sic_v3_1.advanced_debug import AdvancedDebugger
        print("✅ AdvancedDebugger: OK")
        debug_available = True
    except Exception as e:
        print(f"❌ AdvancedDebugger: FAILED - {e}")
        debug_available = False
    
    try:
        from sistema.sic_v3_1.predictive_cache import PredictiveCacheManager
        print("✅ PredictiveCacheManager: OK")
        cache_available = True
    except Exception as e:
        print(f"❌ PredictiveCacheManager: FAILED - {e}")
        cache_available = False
    
    print()
    
    # Test 2: Instanciación de objetos SIC
    if sic_available:
        print("🏗️ Test 2: Instanciación SIC Enterprise Interface")
        try:
            sic = SICv31Enterprise()
            print("✅ SIC Interface creada correctamente")
            
            # Test smart_import
            result = sic.smart_import('sys')
            if result is not None:
                print("✅ smart_import funciona")
            else:
                print("⚠️ smart_import retorna None (esperado en fallback)")
                
        except Exception as e:
            print(f"❌ Error creando SIC Interface: {e}")
    
    print()
    
    # Test 3: Cache predictivo
    if cache_available:
        print("🧠 Test 3: Cache Predictivo")
        try:
            cache = PredictiveCacheManager()
            print("✅ PredictiveCacheManager creado")
            
            # Test cache de sys (que está causando el cache miss)
            cache_result = cache.get_cached_module('sys')
            if cache_result is not None:
                print("✅ Cache de 'sys' funciona")
            else:
                print("⚠️ Cache MISS para 'sys' - necesita warm-up")
                
        except Exception as e:
            print(f"❌ Error con Cache Predictivo: {e}")
    
    print()
    
    # Test 4: Integración con Downloader
    print("📥 Test 4: Integración Downloader")
    try:
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        print("✅ AdvancedCandleDownloader importado")
        
        # Verificar si SIC está realmente integrado
        downloader = AdvancedCandleDownloader()
        
        # Verificar si tiene instancia SIC
        if hasattr(downloader, 'sic') or hasattr(downloader, '_sic'):
            print("✅ Downloader tiene integración SIC")
        else:
            print("⚠️ Downloader NO tiene integración SIC detectada")
            
    except Exception as e:
        print(f"❌ Error con Downloader: {e}")
    
    print()
    
    # Test 5: Diagnóstico de paths
    print("📁 Test 5: Verificación de paths")
    
    sic_path = current_dir / "sistema" / "sic_v3_1"
    print(f"📂 SIC Path: {sic_path}")
    print(f"📂 Existe: {sic_path.exists()}")
    
    if sic_path.exists():
        sic_files = list(sic_path.glob("*.py"))
        print(f"📄 Archivos Python en SIC: {len(sic_files)}")
        for file in sorted(sic_files):
            print(f"   - {file.name}")
    
    print()
    
    # Test 6: Recomendaciones de reparación
    print("🔧 RECOMENDACIONES DE REPARACIÓN:")
    print("-"*60)
    
    if not sic_available:
        print("❌ SIC no disponible - Verificar imports en enterprise_interface.py")
        
    if not cache_available:
        print("❌ Cache no disponible - Verificar predictive_cache.py")
        
    if not debug_available:
        print("❌ Debug no disponible - Verificar advanced_debug.py")
    
    # Cache miss específico
    print("🧠 Para solucionar Cache MISS de 'sys':")
    print("   1. Warm-up el cache predictivo")
    print("   2. Agregar 'sys' a la lista de módulos críticos")
    print("   3. Verificar persistencia del cache")
    
    print()
    print("="*60)
    print("🎯 RESULTADO DEL DIAGNÓSTICO")
    print("="*60)
    
    total_tests = 3
    passed_tests = sum([sic_available, cache_available, debug_available])
    
    print(f"📊 Tests pasados: {passed_tests}/{total_tests}")
    print(f"📈 Ratio de éxito: {(passed_tests/total_tests*100):.1f}%")
    
    if passed_tests == total_tests:
        print("✅ TODOS LOS COMPONENTES SIC FUNCIONAN")
        print("🔧 Problema probablemente en configuración de cache")
    else:
        print("❌ COMPONENTES SIC CON PROBLEMAS")
        print("🔧 Requiere reparación de imports")
    
    return passed_tests == total_tests

def test_cache_warmup():
    """🔥 Warm-up del cache predictivo para solucionar cache miss"""
    print("\n🔥 WARM-UP CACHE PREDICTIVO")
    print("-"*40)
    
    try:
        from sistema.sic_v3_1.predictive_cache import PredictiveCacheManager
        
        cache = PredictiveCacheManager()
        
        # Módulos críticos que siempre deben estar en cache
        critical_modules = ['sys', 'os', 'time', 'datetime', 'pathlib', 'json']
        
        for module_name in critical_modules:
            try:
                # Simular carga del módulo
                actual_module = __import__(module_name)
                cache.cache_module(module_name, actual_module)
                print(f"✅ {module_name} agregado al cache")
            except Exception as e:
                print(f"❌ Error cacheando {module_name}: {e}")
        
        print("🔥 Warm-up completado")
        return True
        
    except Exception as e:
        print(f"❌ Error en warm-up: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO DIAGNÓSTICO SIC-DOWNLOADER")
    print("="*60)
    
    # Diagnóstico principal
    success = test_sic_imports()
    
    # Warm-up si es necesario
    if success:
        test_cache_warmup()
    
    print("\n🎉 DIAGNÓSTICO COMPLETADO")
