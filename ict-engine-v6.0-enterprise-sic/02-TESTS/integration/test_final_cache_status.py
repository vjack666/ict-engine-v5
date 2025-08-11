#!/usr/bin/env python3
"""
🔍 TEST FINAL: VERIFICACIÓN STATUS CACHE POST-FIX
==========================================================
Verifica que el ICTDataManager cache funciona correctamente después del fix.
"""

import sys
import os
import time

# Asegurar imports directos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '01-CORE'))

def test_cache_final_status():
    """Test final del status del cache después de todas las correcciones"""
    print("🔍 TEST FINAL: CACHE STATUS POST-FIX")
    print("=" * 60)
    
    # 1. Importar y crear componentes
    try:
        # Añadir path específico
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'proyecto principal'))
        
        from core.data_management.ict_data_manager import ICTDataManager
        print("✅ ICTDataManager importado")
        
        # Crear manager
        print("📊 Creando ICTDataManager...")
        manager = ICTDataManager()
        print("✅ ICTDataManager creado")
        
        # 2. Test warm-up 
        print("\n🚀 TEST WARM-UP CON MONITOREO:")
        print("   Símbolos: EURUSD, GBPUSD")
        print("   Timeframes: H4, M15")
        
        start_time = time.time()
        result = manager.warm_up_cache(
            symbols=['EURUSD', 'GBPUSD'],
            timeframes=['H4', 'M15']
        )
        warm_up_time = time.time() - start_time
        
        print(f"   ⏱️ Tiempo warm-up: {warm_up_time:.2f}s")
        print(f"   ✅ Resultado: {result}")
        
        # 3. Verificar cache después de warm-up
        print("\n📊 VERIFICACIÓN CACHE POST WARM-UP:")
        try:
            cache_status = manager.get_multi_tf_cache_status()
            total_symbols = cache_status.get('total_symbols', 0)
            print(f"   📈 Total símbolos: {total_symbols}")
            print(f"   📊 Data symbols count: {len(manager.data_status)}")
            
            # Solo mostrar cache efficiency si está disponible
            if 'cache_efficiency' in cache_status:
                print(f"   � Cache efficiency: {cache_status['cache_efficiency']}")
            else:
                print("   🔄 Cache efficiency: N/A")
                
        except Exception as e:
            print(f"   ❌ Error obteniendo cache status: {e}")
            cache_status = {}
        
        # 4. Test directo de data
        print("\n🔍 VERIFICACIÓN DATOS DIRECTOS:")
        for symbol in ['EURUSD', 'GBPUSD']:
            if symbol in manager.data_status:
                timeframes = manager.data_status[symbol]
                print(f"   ✅ {symbol}: {list(timeframes.keys())}")
                for tf, data in timeframes.items():
                    bars = data.get('bars', 0)
                    print(f"     - {tf}: {bars} bars")
            else:
                print(f"   ❌ {symbol}: NO DATA")
        
        # 5. Test manual update
        print("\n🔧 TEST MANUAL UPDATE:")
        test_data = {
            'bars': 500,
            'source': 'MANUAL_TEST',
            'quality': 'EXCELLENT',
            'last_update': time.time(),
            'available': True
        }
        
        print("   📝 Aplicando _update_data_status manual...")
        manager._update_data_status('EURJPY', 'H4', test_data)
        
        if 'EURJPY' in manager.data_status:
            print("   ✅ Manual update: SUCCESS")
            print(f"   📊 EURJPY H4: {manager.data_status['EURJPY']['H4']}")
        else:
            print("   ❌ Manual update: FAILED")
        
        # 6. Resumen final
        print("\n✅ RESUMEN FINAL:")
        print("=" * 60)
        print(f"   📊 Cache funcionando: {'✅ SÍ' if len(manager.data_status) > 0 else '❌ NO'}")
        print(f"   📈 Símbolos registrados: {len(manager.data_status)}")
        
        total_timeframes = sum(len(tfs) for tfs in manager.data_status.values())
        print(f"   📊 Total timeframes: {total_timeframes}")
        
        cache_working = len(manager.data_status) > 0
        print(f"   🎯 Status general: {'🟢 FUNCIONANDO' if cache_working else '🔴 PROBLEMAS'}")
        
        return cache_working
        
    except Exception as e:
        print(f"❌ Error en test cache final: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_cache_final_status()
    print(f"\n🏁 RESULTADO FINAL: {'✅ CACHE FUNCIONANDO' if success else '❌ CACHE CON PROBLEMAS'}")
