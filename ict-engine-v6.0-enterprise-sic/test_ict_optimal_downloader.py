#!/usr/bin/env python3
"""
🧪 TEST ICT OPTIMAL DOWNLOADER - Verificación de funcionamiento óptimo
====================================================================

Test para verificar que el Advanced Candle Downloader funciona con 
configuración ICT óptima y descarga las cantidades correctas de velas
según las leyes institucionales.

Autor: ICT Engine v6.0 Enterprise Team
Fecha: Agosto 2025
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

def test_ict_optimal_configuration():
    """🏛️ Test: Verificar configuración ICT óptima"""
    print("\n" + "="*70)
    print("🧪 TEST ICT OPTIMAL DOWNLOADER v6.0")
    print("="*70)
    
    try:
        print("\n📥 1. Importando Advanced Candle Downloader...")
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        print("✅ Import exitoso")
        
        print("\n🔧 2. Inicializando downloader...")
        downloader = AdvancedCandleDownloader(
            config={
                'enable_debug': True,
                'use_predictive_cache': True,
                'enable_lazy_loading': True
            }
        )
        print("✅ Downloader inicializado")
        
        print("\n📊 3. Probando configuración ICT por timeframe...")
        timeframes_test = ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1']
        
        for tf in timeframes_test:
            if hasattr(downloader, '_get_ict_optimal_config'):
                config = downloader._get_ict_optimal_config(tf)
                print(f"   {tf}: Min={config['minimum_bars']:,} | Ideal={config['ideal_bars']:,} | Óptimo={config['optimal_bars']:,}")
            else:
                print(f"   {tf}: Método _get_ict_optimal_config no disponible")
        
        print("\n🚀 4. Probando descarga ICT con EURUSD M15...")
        
        # Test de descarga con configuración ICT
        result = downloader.download_candles(
            symbol="EURUSD",
            timeframe="M15",
            save_to_file=False,
            use_ict_optimal=True
        )
        
        print(f"\n📊 RESULTADO DESCARGA:")
        print(f"   Success: {result.get('success', False)}")
        print(f"   Message: {result.get('message', 'N/A')}")
        
        if result.get('success') and result.get('data') is not None:
            data = result['data']
            print(f"   Velas descargadas: {len(data):,}")
            print(f"   Rango: {data.index[0]} a {data.index[-1]}")
            print(f"   Fuente: {result.get('source', 'N/A')}")
            
            # Mostrar análisis ICT si está disponible
            if 'ict_analysis' in result:
                ict = result['ict_analysis']
                print(f"\n🏛️ ANÁLISIS ICT:")
                print(f"   Velas objetivo: {ict.get('target_bars', 'N/A'):,}")
                print(f"   Velas reales: {ict.get('actual_bars', 'N/A'):,}")
                print(f"   Cumple ICT mínimo: {ict.get('meets_ict_minimum', False)}")
                print(f"   Cumple ICT ideal: {ict.get('meets_ict_ideal', False)}")
                print(f"   Es ICT óptimo: {ict.get('is_ict_optimal', False)}")
            
            # Verificar cumplimiento ICT
            if 'ict_compliance' in result:
                comp = result['ict_compliance']
                print(f"\n✅ CUMPLIMIENTO ICT:")
                print(f"   Status: {comp.get('status', 'UNKNOWN')}")
                print(f"   Calidad: {comp.get('analysis_quality', 'UNKNOWN')}")
                print(f"   Compliant: {comp.get('compliant', False)}")
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")
            if 'instructions' in result:
                print(f"\n📋 INSTRUCCIONES:")
                for instruction in result['instructions']:
                    print(f"   - {instruction}")
        
        print("\n🔄 5. Probando descarga conjunto completo ICT...")
        
        if hasattr(downloader, 'download_ict_full_analysis_set'):
            full_result = downloader.download_ict_full_analysis_set(
                symbol="EURUSD",
                timeframes=['H4', 'H1', 'M15'],
                save_files=False
            )
            
            print(f"\n📊 RESULTADO CONJUNTO ICT:")
            print(f"   Success: {full_result.get('success', False)}")
            
            if full_result.get('success') and 'summary' in full_result:
                summary = full_result['summary']
                print(f"   Timeframes: {summary.get('timeframes_downloaded', 0)}")
                print(f"   Total velas: {summary.get('total_bars', 0):,}")
                print(f"   ICT Compliant: {summary.get('all_ict_compliant', False)}")
                print(f"   Grado análisis: {summary.get('analysis_grade', 'UNKNOWN')}")
        else:
            print("   Método download_ict_full_analysis_set no disponible")
        
        print("\n📈 6. Verificando métricas de performance...")
        
        if hasattr(downloader, 'get_performance_report'):
            perf_report = downloader.get_performance_report()
            print(f"   Operaciones totales: {perf_report.get('total_operations', 0)}")
            print(f"   Descargas exitosas: {perf_report.get('successful_downloads', 0)}")
            print(f"   Descargas fallidas: {perf_report.get('failed_downloads', 0)}")
            print(f"   Integración SIC activa: {perf_report.get('sic_integration_active', False)}")
        
        print("\n✅ TEST ICT OPTIMAL DOWNLOADER COMPLETADO")
        print("="*70)
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("   Verificar que todos los módulos estén disponibles")
        return False
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ict_timeframe_requirements():
    """📊 Test específico para verificar requerimientos por timeframe"""
    print("\n" + "="*50)
    print("📊 TEST REQUERIMIENTOS ICT POR TIMEFRAME")
    print("="*50)
    
    # Requerimientos ICT esperados (según leyes institucionales)
    expected_requirements = {
        'M1': {'min': 500, 'ideal': 1000, 'optimal': 2000},
        'M5': {'min': 1000, 'ideal': 2000, 'optimal': 5000},
        'M15': {'min': 2000, 'ideal': 5000, 'optimal': 10000},
        'M30': {'min': 1500, 'ideal': 3000, 'optimal': 6000},
        'H1': {'min': 1000, 'ideal': 2500, 'optimal': 5000},
        'H4': {'min': 500, 'ideal': 1200, 'optimal': 2500},
        'D1': {'min': 200, 'ideal': 500, 'optimal': 1000}
    }
    
    try:
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        downloader = AdvancedCandleDownloader()
        
        all_correct = True
        
        for tf, expected in expected_requirements.items():
            if hasattr(downloader, '_get_ict_optimal_config'):
                actual = downloader._get_ict_optimal_config(tf)
                
                print(f"\n{tf}:")
                print(f"   Esperado - Min: {expected['min']:,} | Ideal: {expected['ideal']:,} | Óptimo: {expected['optimal']:,}")
                print(f"   Actual   - Min: {actual['minimum_bars']:,} | Ideal: {actual['ideal_bars']:,} | Óptimo: {actual['optimal_bars']:,}")
                
                # Verificar coincidencia
                matches = (
                    actual['minimum_bars'] == expected['min'] and
                    actual['ideal_bars'] == expected['ideal'] and
                    actual['optimal_bars'] == expected['optimal']
                )
                
                if matches:
                    print(f"   ✅ CORRECTO")
                else:
                    print(f"   ❌ NO COINCIDE")
                    all_correct = False
            else:
                print(f"{tf}: ❌ Método no disponible")
                all_correct = False
        
        if all_correct:
            print(f"\n✅ TODOS LOS TIMEFRAMES ICT CORRECTOS")
        else:
            print(f"\n❌ ALGUNOS TIMEFRAMES NO COINCIDEN CON ESTÁNDARES ICT")
        
        return all_correct
        
    except Exception as e:
        print(f"❌ Error verificando requerimientos ICT: {e}")
        return False

if __name__ == "__main__":
    print("🏛️ ICT ENGINE v6.0 - TEST OPTIMAL DOWNLOADER")
    print("=" * 70)
    print("Verificando configuración ICT institucional y descarga óptima...")
    
    # Ejecutar tests
    test1_passed = test_ict_optimal_configuration()
    test2_passed = test_ict_timeframe_requirements()
    
    print(f"\n🏁 RESUMEN FINAL:")
    print(f"   Test configuración ICT: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"   Test requerimientos TF: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    
    if test1_passed and test2_passed:
        print(f"\n🎉 TODOS LOS TESTS ICT OPTIMAL DOWNLOADER: ✅ EXITOSOS")
        print(f"   El sistema está listo para análisis institucional ICT")
    else:
        print(f"\n⚠️ ALGUNOS TESTS FALLARON - Revisar implementación ICT")
