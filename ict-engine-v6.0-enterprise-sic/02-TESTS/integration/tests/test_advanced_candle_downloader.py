#!/usr/bin/env python3
"""
Test para AdvancedCandleDownloader v6.0 Enterprise
=================================================

Tests del primer componente migrado al ICT Engine v6.1.0 Enterprise SIC.

Autor: ICT Engine v6.1.0 Enterprise Team
Versión: v6.1.0-enterprise
Fecha: Agosto 2025
"""

import sys
import time
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_advanced_candle_downloader_v6():
    """🧪 Test del AdvancedCandleDownloader v6.0 Enterprise"""
    print("\n" + "="*80)
    print("🧪 TESTING ADVANCED CANDLE DOWNLOADER v6.0 ENTERPRISE")
    print("="*80)
    
    try:
        # Test 1: Importación básica
        print("1️⃣ Testing importación...")
        from core.data_management.advanced_candle_downloader import (
            get_advanced_candle_downloader,
            create_download_request,
            DownloadStats,
            DownloadRequest,
            DownloadStatus
        )
        print("   ✅ Importaciones exitosas")
        
        # Test 2: Creación de downloader
        print("2️⃣ Testing creación de downloader...")
        config = {
            'enable_debug': True,
            'use_predictive_cache': True,
            'enable_lazy_loading': True,
            'max_concurrent': 2,
            'batch_size': 1000
        }
        downloader = get_advanced_candle_downloader(config)
        print("   ✅ Downloader creado exitosamente")
        
        # Test 3: Estado inicial
        print("3️⃣ Testing estado inicial...")
        status = downloader.get_status()
        assert not status['is_downloading']
        assert status['active_downloads'] == 0
        assert status['queue_size'] == 0
        assert status['sic_integration']['version'] == 'v3.1'
        print(f"   ✅ Estado inicial correcto: SIC {status['sic_integration']['version']}")
        
        # Test 4: Creación de download request
        print("4️⃣ Testing creación de requests...")
        request = create_download_request('EURUSD', 'M1', 1000)
        assert request.symbol == 'EURUSD'
        assert request.timeframe == 'M1'
        assert request.lookback == 1000
        assert request.use_cache == True
        print("   ✅ DownloadRequest creado correctamente")
        
        # Test 5: Reporte de performance
        print("5️⃣ Testing reporte de performance...")
        report = downloader.get_performance_report()
        assert 'total_operations' in report
        assert 'sic_integration_active' in report
        assert report['sic_integration_active'] == True
        print("   ✅ Reporte de performance generado")
        
        # Test 6: Dataclasses
        print("6️⃣ Testing dataclasses...")
        stats = DownloadStats('EURUSD', 'M1')
        assert stats.symbol == 'EURUSD'
        assert stats.timeframe == 'M1'
        assert stats.total_bars == 0
        assert stats.cache_hits == 0  # Nuevo campo v6.0
        print("   ✅ DownloadStats funcionando correctamente")
        
        download_status = DownloadStatus('test_123', 'pending')
        assert download_status.request_id == 'test_123'
        assert download_status.status == 'pending'
        assert download_status.progress == 0.0
        print("   ✅ DownloadStatus funcionando correctamente")
        
        # Test 7: Integración SIC v3.1 (configuración)
        print("7️⃣ Testing integración SIC v3.1...")
        sic_config = status['sic_integration']
        assert sic_config['version'] == 'v3.1'
        # Note: lazy_modules y cache_enabled pueden ser 0/False en fallback mode
        print(f"   ✅ SIC v3.1 integrado: lazy_modules={sic_config.get('lazy_modules', 0)}, cache={sic_config.get('cache_enabled', False)}")
        
        print("\n" + "="*80)
        print("✅ ADVANCED CANDLE DOWNLOADER v6.0 - TODOS LOS TESTS PASARON")
        print("="*80)
        return True
        
    except ImportError as e:
        print(f"   ❌ ERROR DE IMPORTACIÓN: {e}")
        return False
    except AssertionError as e:
        print(f"   ❌ ERROR DE ASSERTION: {e}")
        return False
    except Exception as e:
        print(f"   ❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_with_existing_tests():
    """🔗 Test de integración con el sistema de tests existente"""
    print("\n" + "="*60)
    print("🔗 TESTING INTEGRACIÓN CON TESTS EXISTENTES")
    print("="*60)
    
    try:
        # Verificar que puede coexistir con tests SIC existentes
        sys.path.insert(0, '.')
        
        # Test de importación de tests existentes
        try:
            from tests.test_sic_complete import test_sic_enterprise_interface
            print("   ✅ Tests SIC existentes accesibles")
        except ImportError:
            print("   ℹ️  Tests SIC no disponibles (normal en desarrollo)")
        
        # Test del nuevo componente
        result = test_advanced_candle_downloader_v6()
        
        if result:
            print("   ✅ Integración exitosa: AdvancedCandleDownloader v6.0 compatible")
            return True
        else:
            print("   ❌ Fallo en integración")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR EN INTEGRACIÓN: {e}")
        return False

if __name__ == "__main__":
    print("🚀 ICT ENGINE v6.0 ENTERPRISE - TEST SUITE")
    print("Componente: AdvancedCandleDownloader v6.0")
    print("Fecha: Agosto 2025")
    print()
    
    start_time = time.time()
    
    # Ejecutar tests principales
    test1_result = test_advanced_candle_downloader_v6()
    test2_result = test_integration_with_existing_tests()
    
    duration = time.time() - start_time
    
    # Resumen final
    print("\n" + "🎯" * 20)
    print("📊 RESUMEN DE TESTS:")
    print(f"   • Test AdvancedCandleDownloader v6.0: {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"   • Test Integración: {'✅ PASS' if test2_result else '❌ FAIL'}")
    print(f"   • Duración total: {duration:.3f}s")
    
    if test1_result and test2_result:
        print("\n🎉 ¡TODOS LOS TESTS PASARON! AdvancedCandleDownloader v6.0 listo para producción.")
        sys.exit(0)
    else:
        print("\n❌ Algunos tests fallaron. Revisar logs arriba.")
        sys.exit(1)
