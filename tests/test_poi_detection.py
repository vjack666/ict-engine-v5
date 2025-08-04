#!/usr/bin/env python3
"""
🧪 TEST COMPLETO DEL POI SYSTEM CON DETECCIÓN
============================================

Test para verificar que el POI System Manager funciona con detección real.
"""

import sys
import os
import pandas as pd
import numpy as np

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_sample_data():
    """Crear datos de muestra para testing."""
    dates = pd.date_range('2024-01-01', periods=100, freq='15min')
    np.random.seed(42)
    
    # Generar datos OHLC realistas
    open_prices = 1.1000 + np.random.randn(100) * 0.0010
    close_prices = open_prices + np.random.randn(100) * 0.0005
    high_prices = np.maximum(open_prices, close_prices) + np.abs(np.random.randn(100) * 0.0003)
    low_prices = np.minimum(open_prices, close_prices) - np.abs(np.random.randn(100) * 0.0003)
    volumes = np.random.randint(100, 1000, 100)
    
    df = pd.DataFrame({
        'time': dates,
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices,
        'volume': volumes
    })
    
    return df

def test_poi_detection():
    """Test completo del POI System con detección."""
    print("🎯 INICIANDO TEST DE DETECCIÓN POI")
    print("=" * 50)
    
    try:
        # Importar sistema POI
        print("📦 Importando POI System...")
        from core.poi_system.poi_system import (
            get_poi_system_instance,
            poi_detect_wrapper,
            get_poi_detector_instance
        )
        print("✅ Sistema POI importado")
        
        # Crear datos de muestra
        print("\n📊 Creando datos de muestra...")
        df = create_sample_data()
        current_price = df['close'].iloc[-1]
        print(f"✅ Datos creados: {len(df)} filas, precio actual: {current_price:.5f}")
        
        # Test 1: Obtener instancia singleton
        print("\n🎯 Test 1: Obteniendo instancia singleton...")
        poi_system = get_poi_system_instance()
        print(f"✅ Instancia obtenida, inicializado: {poi_system.is_initialized()}")
        
        # Test 2: Inicializar si no está listo
        if not poi_system.is_initialized():
            print("\n⚡ Inicializando sistema POI...")
            success = poi_system.initialize()
            print(f"✅ Inicialización: {success}")
        
        # Test 3: Detección POI directa
        print("\n🔍 Test 3: Detección POI directa...")
        pois_direct = poi_system.detect_pois(df, "M15", current_price)
        print(f"✅ POIs detectados (directo): {len(pois_direct)}")
        
        # Test 4: Detección POI con wrapper
        print("\n🔧 Test 4: Detección POI con wrapper...")
        pois_wrapper = poi_detect_wrapper(df, "M15", current_price)
        print(f"✅ POIs detectados (wrapper): {len(pois_wrapper)}")
        
        # Test 5: Cache verification (segunda llamada)
        print("\n💾 Test 5: Verificando cache...")
        stats_before = poi_system.get_stats()
        pois_cached = poi_system.detect_pois(df, "M15", current_price)
        stats_after = poi_system.get_stats()
        
        cache_hits_before = stats_before['instance_stats']['cache_hits']
        cache_hits_after = stats_after['instance_stats']['cache_hits']
        
        print(f"✅ Cache hits antes: {cache_hits_before}, después: {cache_hits_after}")
        print(f"✅ Cache funcionando: {cache_hits_after > cache_hits_before}")
        print(f"✅ POIs desde cache: {len(pois_cached)}")
        
        # Test 6: Estadísticas completas
        print("\n📊 Test 6: Estadísticas del sistema...")
        final_stats = poi_system.get_stats()
        instance_stats = final_stats['instance_stats']
        global_stats = final_stats['global_stats']
        
        print(f"✅ Total detecciones: {instance_stats['total_detections']}")
        print(f"✅ Cache hits: {instance_stats['cache_hits']}")
        print(f"✅ Cache misses: {instance_stats['cache_misses']}")
        print(f"✅ Tiempo inicialización: {instance_stats['initialization_time']:.3f}s")
        print(f"✅ Tamaño cache: {final_stats['cache_size']}")
        
        # Test 7: Detector independiente
        print("\n🎯 Test 7: Acceso al detector...")
        detector = get_poi_detector_instance()
        print(f"✅ Detector obtenido: {detector is not None}")
        
        print("\n" + "=" * 50)
        print("🎉 TODOS LOS TESTS DE DETECCIÓN PASARON")
        print("✅ POI System Manager con detección funcionando perfectamente")
        
        # Mostrar resumen final
        print(f"\n📈 RESUMEN FINAL:")
        print(f"   • POIs detectados: {len(pois_direct)}")
        print(f"   • Cache hits: {cache_hits_after}")
        print(f"   • Total detecciones: {instance_stats['total_detections']}")
        print(f"   • Sistema inicializado: {poi_system.is_initialized()}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN TEST DE DETECCIÓN: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_poi_detection()
    sys.exit(0 if success else 1)
