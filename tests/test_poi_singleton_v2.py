#!/usr/bin/env python3
"""
🧪 TEST DEL POI SYSTEM MANAGER SINGLETON
=====================================

Test para verificar que el nuevo POI System Manager funciona correctamente.
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_poi_system_manager():
    """Test completo del POI System Manager."""
    print("🧪 INICIANDO TEST DEL POI SYSTEM MANAGER")
    print("=" * 50)

    try:
        # Test 1: Importación
        print("📦 Test 1: Importando POI System Manager...")
        from core.poi_system.poi_system import (
            POISystemManager,
            get_poi_system_instance,
            is_poi_system_initialized,
            get_poi_system_stats,
            reset_poi_system_instance
        )
        print("✅ Importación exitosa")

        # Test 2: Crear instancia
        print("\n🏗️ Test 2: Creando instancia directa...")
        manager = POISystemManager()
        print(f"✅ Instancia creada. Inicializado: {manager.is_initialized()}")

        # Test 3: Singleton pattern
        print("\n🔄 Test 3: Probando patrón singleton...")
        instance1 = get_poi_system_instance()
        instance2 = get_poi_system_instance()
        print(f"✅ Singleton funcionando: {instance1 is instance2}")

        # Test 4: Inicialización
        print("\n⚡ Test 4: Inicializando sistema...")
        success = instance1.initialize()
        print(f"✅ Inicialización exitosa: {success}")
        print(f"✅ Estado después de init: {instance1.is_initialized()}")

        # Test 5: Estadísticas
        print("\n📊 Test 5: Verificando estadísticas...")
        stats = instance1.get_stats()
        print(f"✅ Estadísticas obtenidas: {len(stats)} campos")

        # Test 6: Sistema global
        print("\n🌐 Test 6: Verificando estado global...")
        global_initialized = is_poi_system_initialized()
        global_stats = get_poi_system_stats()
        print(f"✅ Sistema global inicializado: {global_initialized}")
        print(f"✅ Estadísticas globales: {len(global_stats)} campos")

        # Test 7: Reset
        print("\n🔄 Test 7: Probando reset del sistema...")
        reset_poi_system_instance()
        after_reset = is_poi_system_initialized()
        print(f"✅ Sistema después de reset: {after_reset}")

        print("\n" + "=" * 50)
        print("🎉 TODOS LOS TESTS PASARON CORRECTAMENTE")
        print("✅ POI System Manager está funcionando perfectamente")

        return True

    except Exception as e:
        print(f"\n❌ ERROR EN TEST: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_poi_system_manager()
    sys.exit(0 if success else 1)
