#!/usr/bin/env python3
"""
🚨 TEST CRÍTICO: H1 y H4 TIMEFRAMES
==================================
Test específico para verificar que H1 y H4 funcionan correctamente
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_critical_timeframes():
    """🚨 Test crítico de H1 y H4 - SIN ESTOS NO HAY ANÁLISIS ICT"""
    print("🚨 TEST CRÍTICO: TIMEFRAMES H1 y H4")
    print("="*50)
    
    try:
        from core.data_management.advanced_candle_downloader import get_advanced_candle_downloader
        
        # Crear downloader
        config = {'enable_debug': True}
        downloader = get_advanced_candle_downloader(config)
        print("✅ Downloader creado")
        
        # Fechas de test (más cortas para H1/H4)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5)  # Solo 5 días
        
        # TEST CRÍTICO 1: H1
        print("\n🚨 TEST H1 (CRÍTICO PARA ICT)...")
        try:
            result_h1 = downloader.download_candles('EURUSD', 'H1', start_date, end_date, False)
            if result_h1['success']:
                data_h1 = result_h1['data']
                print(f"✅ H1 ÉXITO: {len(data_h1)} velas descargadas")
                print(f"   Método usado: {result_h1.get('timeframe_method', 'N/A')}")
                print(f"   Rango: {data_h1.index[0]} a {data_h1.index[-1]}")
            else:
                print(f"❌ H1 FALLÓ: {result_h1['message']}")
                return False
        except Exception as e:
            print(f"❌ H1 ERROR CRÍTICO: {e}")
            return False
        
        # TEST CRÍTICO 2: H4
        print("\n🚨 TEST H4 (CRÍTICO PARA ICT)...")
        try:
            result_h4 = downloader.download_candles('EURUSD', 'H4', start_date, end_date, False)
            if result_h4['success']:
                data_h4 = result_h4['data']
                print(f"✅ H4 ÉXITO: {len(data_h4)} velas descargadas")
                print(f"   Método usado: {result_h4.get('timeframe_method', 'N/A')}")
                print(f"   Rango: {data_h4.index[0]} a {data_h4.index[-1]}")
            else:
                print(f"❌ H4 FALLÓ: {result_h4['message']}")
                return False
        except Exception as e:
            print(f"❌ H4 ERROR CRÍTICO: {e}")
            return False
        
        # TEST VERIFICACIÓN: M15 (debe seguir funcionando)
        print("\n✅ TEST M15 (verificación)...")
        result_m15 = downloader.download_candles('EURUSD', 'M15', start_date, end_date, False)
        if result_m15['success']:
            data_m15 = result_m15['data']
            print(f"✅ M15 OK: {len(data_m15)} velas")
        else:
            print(f"⚠️ M15 warning: {result_m15['message']}")
        
        print("\n" + "="*50)
        print("🎉 TIMEFRAMES CRÍTICOS FUNCIONANDO")
        print("✅ H1: Disponible para análisis ICT")
        print("✅ H4: Disponible para análisis ICT") 
        print("🚀 SISTEMA LISTO PARA ANÁLISIS COMPLETO")
        return True
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO EN TEST: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_critical_timeframes()
    if success:
        print("\n🏆 TEST CRÍTICO PASADO - SISTEMA OPERATIVO")
        sys.exit(0)
    else:
        print("\n💥 TEST CRÍTICO FALLIDO - SISTEMA NO OPERATIVO")
        sys.exit(1)
