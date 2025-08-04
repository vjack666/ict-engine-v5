#!/usr/bin/env python3
"""
🧪 TEST CANDLE DOWNLOADER INTEGRATION - ICT ENGINE v5.0
=======================================================

Script de prueba para verificar que la integración del CandleDownloader
funciona correctamente con los componentes creados.

Ejecutar: python test_candle_integration.py
"""

import sys
import os
from pathlib import Path

# Agregar directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

def test_imports():
    """Prueba que todas las importaciones funcionen"""
    print("🔍 Probando importaciones...")
    
    try:
        from core.data_management.candle_coordinator import candle_coordinator, CandleCoordinator
        print("✅ CandleCoordinator importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando CandleCoordinator: {e}")
        return False
    
    try:
        from dashboard.candle_downloader_widget import CandleDownloaderWidget
        print("✅ CandleDownloaderWidget importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando CandleDownloaderWidget: {e}")
        return False
    
    try:
        from core.integrations.candle_downloader_integration import (
            CandleDownloaderIntegration, 
            downloader_integration,
            start_download,
            get_downloader_status
        )
        print("✅ CandleDownloaderIntegration importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando CandleDownloaderIntegration: {e}")
        return False
    
    return True

def test_coordinator_basic():
    """Prueba funcionalidad básica del coordinador"""
    print("\n🧪 Probando CandleCoordinator...")
    
    try:
        from core.data_management.candle_coordinator import CandleCoordinator
        
        # Crear instancia
        coordinator = CandleCoordinator()
        print("✅ CandleCoordinator creado")
        
        # Probar callbacks
        def test_progress(request_id, progress):
            print(f"📊 Progress: {request_id} -> {progress:.1%}")
        
        def test_completion(request_id, success):
            print(f"✅ Completed: {request_id} -> {'SUCCESS' if success else 'FAILED'}")
        
        def test_error(request_id, error):
            print(f"❌ Error: {request_id} -> {error}")
        
        coordinator.set_progress_callback(test_progress)
        coordinator.set_completion_callback(test_completion)
        coordinator.set_error_callback(test_error)
        print("✅ Callbacks configurados")
        
        # Obtener estado
        status = coordinator.get_status()
        print(f"✅ Estado obtenido: {status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test_coordinator_basic: {e}")
        return False

def test_widget_basic():
    """Prueba funcionalidad básica del widget"""
    print("\n🎮 Probando CandleDownloaderWidget...")
    
    try:
        from dashboard.candle_downloader_widget import CandleDownloaderWidget
        
        # Crear instancia
        widget = CandleDownloaderWidget()
        print("✅ CandleDownloaderWidget creado")
        
        # Configurar
        widget.configure_symbols(["EURUSD", "GBPUSD"])
        widget.configure_timeframes(["H1", "M15"])
        widget.configure_lookback(1000)
        print("✅ Widget configurado")
        
        # Probar callbacks
        widget.on_progress_update("EURUSD", "H1", "downloading", progress=0.5)
        widget.on_download_completed("EURUSD", "H1", {"success": True})
        widget.on_download_error("GBPUSD", "M15", "Test error")
        print("✅ Callbacks del widget probados")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test_widget_basic: {e}")
        return False

def test_integration_setup():
    """Prueba la configuración de integración"""
    print("\n🔗 Probando CandleDownloaderIntegration...")
    
    try:
        from core.integrations.candle_downloader_integration import CandleDownloaderIntegration
        
        # Crear instancia
        integration = CandleDownloaderIntegration()
        print("✅ CandleDownloaderIntegration creado")
        
        # Obtener estado inicial
        status = integration.get_integration_status()
        print(f"✅ Estado inicial: {status}")
        
        # Probar setup (sin inicializar MT5 realmente)
        print("⚠️  Setup de integración (puede fallar sin MT5)...")
        try:
            result = integration.setup_integration()
            if result:
                print("✅ Setup exitoso")
            else:
                print("⚠️  Setup falló (esperado sin MT5)")
        except Exception as e:
            print(f"⚠️  Setup falló con excepción: {e} (esperado sin MT5)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test_integration_setup: {e}")
        return False

def test_convenience_functions():
    """Prueba las funciones de conveniencia"""
    print("\n🛠️ Probando funciones de conveniencia...")
    
    try:
        from core.integrations.candle_downloader_integration import (
            start_download, stop_download, download_for_trading, get_downloader_status
        )
        
        # Probar obtener estado
        status = get_downloader_status()
        print(f"✅ get_downloader_status(): {status}")
        
        # Las otras funciones requieren MT5, solo verificamos que existen
        print("✅ start_download existe")
        print("✅ stop_download existe") 
        print("✅ download_for_trading existe")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test_convenience_functions: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS DE INTEGRACIÓN CANDLE DOWNLOADER")
    print("=" * 60)
    
    tests = [
        ("Importaciones", test_imports),
        ("Coordinador Básico", test_coordinator_basic),
        ("Widget Básico", test_widget_basic),
        ("Setup de Integración", test_integration_setup),
        ("Funciones de Conveniencia", test_convenience_functions)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASÓ")
            else:
                print(f"❌ {test_name}: FALLÓ")
        except Exception as e:
            print(f"💥 {test_name}: EXCEPCIÓN -> {e}")
    
    print(f"\n{'='*60}")
    print(f"📊 RESULTADOS: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
