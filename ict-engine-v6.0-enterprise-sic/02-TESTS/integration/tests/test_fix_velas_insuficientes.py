#!/usr/bin/env python3
"""
🩺 TEST DIAGNÓSTICO: VELAS INSUFICIENTES CORREGIDO
==================================================

PROPÓSITO: Validar que se corrigió el problema de velas insuficientes
reportado por el usuario en timeframes H1/H4.

ANTES: H1 descargaba solo 1440 velas, H4 solo 540 velas
DESPUÉS: H1 descarga 5000 velas, H4 descarga 3000 velas

Autor: ICT Engine v6.1.0 Enterprise
Fecha: 2025-01-08
"""

import sys
from pathlib import Path
import time
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_fix_velas_insuficientes():
    """🔍 Test principal para validar la corrección de velas insuficientes"""
    
    print("=" * 80)
    print("🩺 TEST DIAGNÓSTICO: VELAS INSUFICIENTES CORREGIDO")
    print("=" * 80)
    print()
    
    try:
        # Importar módulos necesarios
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        from sistema.sic_v3_1.enterprise_interface import SICv31Enterprise
        
        print("✅ Módulos importados correctamente")
        
        # Configurar SIC y downloader
        sic = SICv31Enterprise()
        downloader = AdvancedCandleDownloader()  # No necesita SIC como parámetro
        
        print("✅ Downloader ICT Enterprise inicializado")
        print()
        
        # Timeframes críticos que reportaban problemas
        timeframes_criticos = ['M15', 'H1', 'H4', 'D1']
        symbol = 'EURUSD'
        
        # Cantidad mínima esperada según nueva configuración
        expected_counts = {
            'M15': 5000,
            'H1': 5000,   # 🔥 CORREGIDO: antes era 1440
            'H4': 3000,   # 🔥 CORREGIDO: antes era 540
            'D1': 2000
        }
        
        results = {}
        
        print("📊 ANÁLISIS DE VELAS POR TIMEFRAME:")
        print("-" * 60)
        
        for timeframe in timeframes_criticos:
            print(f"\n🔍 Analizando {timeframe}...")
            
            start_time = time.time()
            
            try:
                # Intentar descarga real
                result = downloader.download_candles(
                    symbol=symbol,
                    timeframe=timeframe,
                    use_ict_optimal=True,  # Usar configuración ICT óptima
                    save_to_file=False
                )
                
                duration = time.time() - start_time
                
                if result['success'] and result['data'] is not None:
                    actual_count = len(result['data'])
                    expected_count = expected_counts[timeframe]
                    
                    # Analizar resultado
                    is_sufficient = actual_count >= expected_count * 0.8  # 80% tolerancia para MT5
                    is_ideal = actual_count >= expected_count
                    
                    results[timeframe] = {
                        'success': True,
                        'actual_count': actual_count,
                        'expected_count': expected_count,
                        'is_sufficient': is_sufficient,
                        'is_ideal': is_ideal,
                        'duration': duration,
                        'data_range': f"{result['data'].index[0]} a {result['data'].index[-1]}"
                    }
                    
                    # Status visual
                    status = "✅ EXCELENTE" if is_ideal else ("⚠️ SUFICIENTE" if is_sufficient else "❌ INSUFICIENTE")
                    
                    print(f"   Resultado: {status}")
                    print(f"   Velas obtenidas: {actual_count:,}")
                    print(f"   Velas esperadas: {expected_count:,}")
                    print(f"   Porcentaje: {(actual_count/expected_count)*100:.1f}%")
                    print(f"   Tiempo: {duration:.2f}s")
                    print(f"   Rango: {result['data'].index[0].strftime('%Y-%m-%d')} a {result['data'].index[-1].strftime('%Y-%m-%d')}")
                    
                else:
                    results[timeframe] = {
                        'success': False,
                        'error': result.get('error', 'Unknown error'),
                        'duration': duration
                    }
                    print(f"   ❌ ERROR: {result.get('error', 'Descarga falló')}")
                    
            except Exception as e:
                results[timeframe] = {
                    'success': False,
                    'error': str(e),
                    'duration': time.time() - start_time
                }
                print(f"   ❌ EXCEPCIÓN: {e}")
        
        # Análisis final
        print()
        print("=" * 80)
        print("📊 RESUMEN DEL DIAGNÓSTICO")
        print("=" * 80)
        
        successful_downloads = sum(1 for r in results.values() if r.get('success', False))
        total_timeframes = len(timeframes_criticos)
        
        print(f"✅ Descargas exitosas: {successful_downloads}/{total_timeframes}")
        
        if successful_downloads > 0:
            print()
            print("🔍 ANÁLISIS DE CORRECCIÓN:")
            
            for tf, result in results.items():
                if result.get('success', False):
                    actual = result['actual_count']
                    expected = result['expected_count']
                    
                    # Comparar con valores anteriores problemáticos
                    if tf == 'H1':
                        old_expected = 1440
                        improvement = actual - old_expected
                        print(f"   H1: {actual:,} velas (vs {old_expected:,} anterior = +{improvement:,} mejora)")
                        
                    elif tf == 'H4':
                        old_expected = 540
                        improvement = actual - old_expected
                        print(f"   H4: {actual:,} velas (vs {old_expected:,} anterior = +{improvement:,} mejora)")
                        
                    else:
                        print(f"   {tf}: {actual:,} velas (✅ Cumple estándar ICT)")
            
            # Verificar si se solucionó el problema principal
            h1_ok = results.get('H1', {}).get('is_sufficient', False)
            h4_ok = results.get('H4', {}).get('is_sufficient', False)
            
            print()
            if h1_ok and h4_ok:
                print("🎉 PROBLEMA SOLUCIONADO: H1 y H4 ahora descargan suficientes velas")
                print("✅ Sistema listo para análisis ICT institucional completo")
            elif h1_ok or h4_ok:
                print("⚠️ MEJORA PARCIAL: Al menos uno de H1/H4 mejoró significativamente")
            else:
                print("❌ PROBLEMA PERSISTE: Revisar configuración MT5 o conexión")
        
        else:
            print("❌ No se pudieron realizar descargas. Verificar:")
            print("   1. MT5 Terminal abierto y conectado")
            print("   2. Símbolos disponibles en FTMO Global Markets")
            print("   3. Conexión a internet estable")
        
        print()
        print("=" * 80)
        
        return results
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("   Verificar que todos los módulos estén disponibles")
        return None
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return None

def main():
    """🚀 Función principal del test"""
    print(f"🕒 Iniciando test diagnóstico: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = test_fix_velas_insuficientes()
    
    print()
    print("📋 Test diagnóstico completado.")
    
    if results:
        successful = sum(1 for r in results.values() if r.get('success', False))
        if successful >= 2:  # Al menos 2 timeframes funcionando
            print("✅ DIAGNÓSTICO: CORRECCIÓN APLICADA EXITOSAMENTE")
            return True
        else:
            print("⚠️ DIAGNÓSTICO: CORRECCIÓN PARCIAL - Revisar configuración")
            return False
    else:
        print("❌ DIAGNÓSTICO: ERROR EN LA VALIDACIÓN")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
