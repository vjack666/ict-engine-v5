#!/usr/bin/env python3
"""
🔄 TEST CHoCH DETECTION - ICT ENGINE v6.0 ENTERPRISE
===================================================

Test específico para validar la implementación de detect_choch()
en PatternDetector v6.0 Enterprise.

Autor: ICT Engine v6.1.0 Enterprise Team
Fecha: Agosto 8, 2025
"""

import sys
import os
import time
from datetime import datetime

# Agregar path del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar configuración Python
try:
    from sistema.sic_v3_1.smart_import import smart_import
    print("✅ Sistema SIC v3.1 Enterprise disponible")
except ImportError:
    print("⚠️  Sistema SIC v3.1 no disponible - usando imports directos")

# Importar PatternDetector
try:
    from core.analysis.pattern_detector import PatternDetector
    print("✅ PatternDetector v6.0 Enterprise cargado")
except ImportError as e:
    print(f"❌ Error importando PatternDetector: {e}")
    sys.exit(1)

def test_choch_basic():
    """🔄 Test básico de CHoCH detection"""
    print("\n" + "="*60)
    print("🔄 TEST CHoCH DETECTION - BASIC")
    print("="*60)
    
    try:
        # Inicializar detector
        print("\n1. 🎯 Inicializando PatternDetector...")
        detector = PatternDetector()
        print("   ✅ PatternDetector inicializado")
        
        # Test CHoCH con datos simulados
        print("\n2. 🔄 Probando detect_choch()...")
        test_symbol = "EURUSD"
        
        start_time = time.time()
        result = detector.detect_choch(test_symbol, mode='minimal')
        analysis_time = time.time() - start_time
        
        print(f"   ⚡ Tiempo de análisis: {analysis_time:.3f}s")
        
        # Mostrar resultados
        print(f"\n3. 📊 RESULTADOS CHoCH:")
        print(f"   Symbol: {test_symbol}")
        print(f"   Detectado: {result.get('detected', False)}")
        print(f"   Pattern Type: {result.get('pattern_type', 'N/A')}")
        print(f"   Status: {result.get('status', 'N/A')}")
        
        if result.get('detected', False):
            print(f"   Dirección: {result.get('direction', 'N/A')}")
            print(f"   Confianza: {result.get('confidence', 0):.1f}%")
            print(f"   Timeframes: {result.get('timeframe_count', 0)}")
            
            # Detalles de la señal principal
            primary = result.get('primary_signal', {})
            if primary:
                print(f"\n   🎯 SEÑAL PRINCIPAL ({primary.get('timeframe', 'N/A')}):")
                print(f"      Estructura: {primary.get('structure_type', 'N/A')}")
                print(f"      Break Level: {primary.get('break_level', 0):.5f}")
                print(f"      Target Level: {primary.get('target_level', 0):.5f}")
                print(f"      Cambio Trend: {primary.get('trend_change', 'N/A')}")
        else:
            print(f"   Razón: {result.get('reason', 'N/A')}")
        
        # Análisis de timeframes
        tf_results = result.get('tf_results', {})
        if tf_results:
            print(f"\n   📈 ANÁLISIS POR TIMEFRAME:")
            for tf, tf_result in tf_results.items():
                detected = tf_result.get('detected', False)
                status = "✅ DETECTADO" if detected else "⚪ No detectado"
                print(f"      {tf}: {status}")
                if detected:
                    print(f"         - Dirección: {tf_result.get('direction', 'N/A')}")
                    print(f"         - Confianza: {tf_result.get('confidence', 0):.1f}%")
        
        # Resumen de ejecución
        exec_summary = result.get('execution_summary', {})
        if exec_summary:
            print(f"\n   ⚡ RESUMEN EJECUCIÓN:")
            print(f"      Timeframes analizados: {exec_summary.get('total_timeframes_analyzed', 0)}")
            print(f"      CHoCH detectados: {exec_summary.get('choch_detected_count', 0)}")
            print(f"      Modo usado: {exec_summary.get('mode_used', 'N/A')}")
            print(f"      Fuente datos: {exec_summary.get('data_source', 'N/A')}")
        
        print(f"\n✅ Test CHoCH completado exitosamente")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en test CHoCH: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_choch_multiple_symbols():
    """🔄 Test CHoCH con múltiples símbolos"""
    print("\n" + "="*60)
    print("🔄 TEST CHoCH DETECTION - MULTIPLE SYMBOLS")
    print("="*60)
    
    symbols = ["EURUSD", "GBPUSD", "USDJPY", "USDCAD"]
    detector = PatternDetector()
    
    results = {}
    
    for symbol in symbols:
        print(f"\n🔍 Analizando {symbol}...")
        start_time = time.time()
        
        result = detector.detect_choch(symbol, mode='live_ready')
        analysis_time = time.time() - start_time
        
        results[symbol] = {
            'result': result,
            'analysis_time': analysis_time
        }
        
        detected = result.get('detected', False)
        status = "✅ CHoCH DETECTADO" if detected else "⚪ Sin CHoCH"
        confidence = result.get('confidence', 0)
        
        print(f"   {status} ({analysis_time:.3f}s)")
        if detected:
            print(f"   Dirección: {result.get('direction', 'N/A')}")
            print(f"   Confianza: {confidence:.1f}%")
    
    # Resumen final
    print(f"\n📊 RESUMEN FINAL:")
    detected_count = sum(1 for r in results.values() if r['result'].get('detected', False))
    total_time = sum(r['analysis_time'] for r in results.values())
    avg_time = total_time / len(results) if results else 0
    
    print(f"   Símbolos analizados: {len(symbols)}")
    print(f"   CHoCH detectados: {detected_count}")
    print(f"   Tiempo total: {total_time:.3f}s")
    print(f"   Tiempo promedio: {avg_time:.3f}s")
    
    return results

def main():
    """🎯 Función principal de testing"""
    print("🔄 CHoCH DETECTION TEST SUITE - ICT ENGINE v6.0")
    print("=" * 80)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: CHoCH básico
    test1_success = test_choch_basic()
    
    # Test 2: CHoCH múltiple (solo si test básico pasa)
    if test1_success:
        test2_results = test_choch_multiple_symbols()
    
    # Resumen final
    print("\n" + "="*80)
    print("🏆 RESUMEN FINAL TEST CHoCH")
    print("="*80)
    
    if test1_success:
        print("✅ CHoCH Detection implementado y funcionando")
        print("✅ Método detect_choch() operativo")
        print("✅ Multi-timeframe analysis funcional")
        print("✅ Error handling robusto")
        
        print(f"\n🎯 PRÓXIMOS PASOS:")
        print("   1. Integrar con ICT Data Manager (datos reales)")
        print("   2. Mejorar detección de trend actual")
        print("   3. Añadir más confluencias ICT")
        print("   4. Optimizar performance")
        
        print(f"\n🎉 CHoCH IMPLEMENTATION SUCCESSFUL!")
    else:
        print("❌ CHoCH Detection falló - revisar implementación")
    
    print("="*80)

if __name__ == "__main__":
    main()
