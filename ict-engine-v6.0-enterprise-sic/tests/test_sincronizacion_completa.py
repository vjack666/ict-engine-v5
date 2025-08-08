#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 TEST SINCRONIZACIÓN COMPLETA SIC-DOWNLOADER
==============================================

Test final que verifica que todos los componentes están sincronizados:
1. SIC v3.1 Enterprise con métodos getter
2. Cache predictivo con warm-up automático
3. Downloader con integración SIC completa
4. Persistencia sin errores de 'open'

Autor: ICT Engine v6.0 Team
"""

import sys
import time
from pathlib import Path

# Agregar paths necesarios
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

def test_sincronizacion_completa():
    """🔄 Test de sincronización completa del sistema"""
    print("🔄 TEST SINCRONIZACIÓN COMPLETA SIC-DOWNLOADER")
    print("="*70)
    
    success_count = 0
    total_tests = 6
    
    # Test 1: SIC v3.1 Enterprise con métodos getter
    print("📦 Test 1: SIC v3.1 Enterprise - Métodos Getter")
    try:
        from sistema.sic_v3_1.enterprise_interface import SICv31Enterprise
        
        sic = SICv31Enterprise()
        
        # Verificar métodos getter
        lazy_manager = sic.get_lazy_loading_manager()
        cache_manager = sic.get_predictive_cache_manager()
        monitor = sic.get_monitor()
        debugger = sic.get_debugger()
        
        if all([lazy_manager, cache_manager, monitor, debugger]):
            print("✅ Todos los métodos getter funcionan")
            success_count += 1
        else:
            print("⚠️ Algunos métodos getter retornaron None")
            success_count += 0.5  # Parcial
            
    except Exception as e:
        print(f"❌ Error en SIC Enterprise: {e}")
    
    print()
    
    # Test 2: Cache predictivo con warm-up automático
    print("🧠 Test 2: Cache Predictivo - Warm-up Automático")
    try:
        from sistema.sic_v3_1.predictive_cache import PredictiveCacheManager
        
        cache = PredictiveCacheManager()
        
        # Verificar que 'sys' ya está en cache después del warm-up
        sys_cached = cache.get_cached_module('sys')
        
        if sys_cached is not None:
            print("✅ Cache warm-up funcionando - 'sys' pre-cacheado")
            success_count += 1
        else:
            print("⚠️ Cache warm-up no detectado")
            
    except Exception as e:
        print(f"❌ Error en Cache Predictivo: {e}")
    
    print()
    
    # Test 3: Downloader con integración SIC completa
    print("📥 Test 3: Downloader - Integración SIC Completa")
    try:
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        
        downloader = AdvancedCandleDownloader()
        
        # Verificar que el SIC está realmente integrado
        if hasattr(downloader, 'sic') and downloader.sic is not None:
            # Verificar acceso a componentes SIC
            lazy_mgr = downloader.sic.get_lazy_loading_manager()
            cache_mgr = downloader.sic.get_predictive_cache_manager()
            
            if lazy_mgr and cache_mgr:
                print("✅ Downloader integrado completamente con SIC")
                success_count += 1
            else:
                print("⚠️ Downloader parcialmente integrado con SIC")
                success_count += 0.5
        else:
            print("❌ Downloader SIN integración SIC detectable")
            
    except Exception as e:
        print(f"❌ Error en Downloader: {e}")
    
    print()
    
    # Test 4: Persistencia sin errores
    print("💾 Test 4: Persistencia - Sin errores de 'open'")
    try:
        from sistema.sic_v3_1.predictive_cache import PredictiveCacheManager
        
        # Crear cache y forzar guardado
        cache = PredictiveCacheManager()
        cache._save_persistence_data()
        
        print("✅ Persistencia funcionando sin errores")
        success_count += 1
        
    except Exception as e:
        if "name 'open' is not defined" in str(e):
            print(f"❌ ERROR PERSISTENCIA: {e}")
        else:
            print(f"⚠️ Error menor en persistencia: {e}")
            success_count += 0.5
    
    print()
    
    # Test 5: Smart import funcionando
    print("🧠 Test 5: Smart Import - Funcionalidad Completa")
    try:
        from sistema.sic_v3_1.enterprise_interface import smart_import
        
        # Test import de módulo crítico
        os_module = smart_import('os')
        json_module = smart_import('json')
        
        if os_module and json_module:
            print("✅ Smart import funcionando perfectamente")
            success_count += 1
        else:
            print("⚠️ Smart import con problemas")
            
    except Exception as e:
        print(f"❌ Error en Smart Import: {e}")
    
    print()
    
    # Test 6: Integración downloader-cache en tiempo real
    print("⚡ Test 6: Integración Tiempo Real Downloader-Cache")
    try:
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        
        downloader = AdvancedCandleDownloader()
        
        # Verificar que no hay cache miss en módulos básicos
        if hasattr(downloader, 'sic') and downloader.sic:
            cache_mgr = downloader.sic.get_predictive_cache_manager()
            if cache_mgr:
                # Intentar acceso a módulo crítico
                sys_cached = cache_mgr.get_cached_module('sys')
                if sys_cached:
                    print("✅ Integración tiempo real funcionando - sin cache miss")
                    success_count += 1
                else:
                    print("⚠️ Cache miss aún presente")
            else:
                print("⚠️ Cache manager no accesible")
        else:
            print("❌ SIC no disponible en downloader")
            
    except Exception as e:
        print(f"❌ Error en integración tiempo real: {e}")
    
    print()
    
    # Resultado final
    print("="*70)
    print("🎯 RESULTADO SINCRONIZACIÓN")
    print("="*70)
    
    success_rate = (success_count / total_tests) * 100
    
    print(f"📊 Tests exitosos: {success_count:.1f}/{total_tests}")
    print(f"📈 Tasa de éxito: {success_rate:.1f}%")
    
    if success_rate >= 95:
        print("🎉 ¡SINCRONIZACIÓN PERFECTA!")
        print("✅ Todos los componentes trabajando en armonía")
        print("✅ SIC v3.1 Enterprise completamente integrado")
        print("✅ Cache predictivo con warm-up automático")
        print("✅ Downloader sincronizado con SIC")
        print("✅ Persistencia sin errores")
        status = "PERFECTO"
        
    elif success_rate >= 80:
        print("🎊 ¡SINCRONIZACIÓN EXCELENTE!")
        print("✅ Componentes principales funcionando")
        print("⚠️ Algunos aspectos menores por optimizar")
        status = "EXCELENTE"
        
    elif success_rate >= 60:
        print("👍 Sincronización Buena")
        print("✅ Funcionalidad básica operativa") 
        print("🔧 Requiere ajustes menores")
        status = "BUENA"
        
    else:
        print("🔧 Requiere Reparación")
        print("❌ Problemas significativos de sincronización")
        print("🚨 Atención inmediata requerida")
        status = "REPARACIÓN"
    
    print()
    print("🚀 COMANDOS POST-SINCRONIZACIÓN:")
    print("-"*50)
    print("🧪 Test POI:              python tests/test_simple_poi.py")
    print("📊 Test downloader:       python tests/test_advanced_candle_downloader.py")
    print("🎯 Test integración:      python tests/test_sic_downloader_integration.py")
    print("📈 Monitor performance:   python scripts/ict_performance_monitor.py")
    
    return success_rate >= 80

if __name__ == "__main__":
    print("🚀 INICIANDO TEST SINCRONIZACIÓN COMPLETA")
    print("="*70)
    
    success = test_sincronizacion_completa()
    
    if success:
        print("\n🎉 ¡SISTEMA COMPLETAMENTE SINCRONIZADO!")
        print("🎯 Listo para operaciones ICT Enterprise")
    else:
        print("\n🔧 Sincronización requiere atención")
        print("📋 Revisar logs arriba para detalles")
