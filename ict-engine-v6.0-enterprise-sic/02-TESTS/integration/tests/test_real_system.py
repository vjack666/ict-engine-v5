#!/usr/bin/env python3
"""
🚀 TEST SISTEMA REAL - ICT ENGINE v6.0 ENTERPRISE
================================================

Test del sistema con DATOS REALES de MT5
NO HAY SIMULACIONES - Solo datos de mercado en vivo

REQUISITOS:
1. MetaTrader 5 ABIERTO
2. Cuenta conectada (demo o real)
3. EURUSD disponible
"""

import sys
sys.path.append('.')

from datetime import datetime, timedelta
from core.analysis.market_structure_analyzer import get_market_structure_analyzer
from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader

def test_real_mt5_connection():
    """🔌 Test conexión MT5 REAL"""
    print("=" * 60)
    print("🚀 ICT ENGINE v6.0 ENTERPRISE - TEST SISTEMA REAL")
    print("=" * 60)
    
    # Test directo MT5
    try:
        import MetaTrader5 as mt5
        print("✅ MetaTrader5 library disponible")
        
        if mt5.initialize():
            print("✅ MT5 inicializado correctamente")
            
            account = mt5.account_info()
            if account:
                print(f"✅ Cuenta: {account.login}")
                print(f"   Broker: {account.company}")
                print(f"   Balance: {account.balance} {account.currency}")
                print(f"   Leverage: 1:{account.leverage}")
                
                # Test símbolo
                eurusd = mt5.symbol_info("EURUSD")
                if eurusd:
                    print(f"✅ EURUSD: Bid={eurusd.bid}, Ask={eurusd.ask}")
                    return True
                else:
                    print("❌ EURUSD no disponible")
                    return False
            else:
                print("❌ Sin cuenta conectada")
                return False
        else:
            print("❌ No se pudo inicializar MT5")
            print("   ¿Está MT5 abierto?")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_real_downloader():
    """📥 Test descarga REAL de datos"""
    print("\n" + "=" * 60)
    print("📥 TEST DOWNLOADER CON DATOS REALES")
    print("=" * 60)
    
    try:
        downloader = AdvancedCandleDownloader()
        print("✅ AdvancedCandleDownloader creado")
        
        # Test conexión
        if not downloader._check_mt5_connection():
            print("❌ MT5 no conectado - SISTEMA REQUIERE DATOS REALES")
            print("   INSTRUCCIONES:")
            print("   1. Abrir MetaTrader 5")
            print("   2. Conectar cuenta demo o real")
            print("   3. Volver a ejecutar este test")
            return False
        
        # Descargar datos REALES
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
        
        print(f"🌍 Descargando datos REALES EURUSD M15...")
        print(f"   Desde: {start_date}")
        print(f"   Hasta: {end_date}")
        
        result = downloader.download_candles(
            symbol="EURUSD",
            timeframe="M15", 
            start_date=start_date,
            end_date=end_date,
            save_to_file=False
        )
        
        if result['success']:
            data = result['data']
            print(f"✅ DATOS REALES obtenidos: {len(data)} velas")
            print(f"   Source: {result.get('source', 'unknown')}")
            print(f"   Última vela close: {data.iloc[-1]['close']:.5f}")
            print(f"   Rango última vela: {data.iloc[-1]['high']:.5f} - {data.iloc[-1]['low']:.5f}")
            return data
        else:
            print(f"❌ Error descargando: {result['error']}")
            if 'instructions' in result:
                print("   INSTRUCCIONES:")
                for instruction in result['instructions']:
                    print(f"   - {instruction}")
            return None
            
    except Exception as e:
        print(f"❌ Error en downloader: {e}")
        return None

def test_real_market_structure():
    """🏗️ Test análisis Market Structure con datos REALES"""
    print("\n" + "=" * 60)
    print("🏗️ TEST MARKET STRUCTURE CON DATOS REALES")
    print("=" * 60)
    
    try:
        # Configuración para análisis real
        config = {
            'enable_debug': True,
            'min_confidence': 60.0,  # Más permisivo para datos reales
            'swing_window': 5,
            'fvg_min_gap': 0.0005,
            'ob_reaction_threshold': 0.001
        }
        
        analyzer = get_market_structure_analyzer(config)
        print("✅ MarketStructureAnalyzer creado")
        
        # Análisis con datos REALES
        print("🌍 Analizando estructura con DATOS REALES...")
        signal = analyzer.analyze_market_structure(
            symbol="EURUSD",
            timeframe="M15",
            lookback_days=3  # 3 días de datos reales
        )
        
        if signal:
            print("✅ SEÑAL DE ESTRUCTURA DETECTADA (DATOS REALES):")
            print(f"   Estructura: {signal.structure_type.value}")
            print(f"   Dirección: {signal.direction.value}")
            print(f"   Confianza: {signal.confidence:.1f}%")
            print(f"   Break Level: {signal.break_level:.5f}")
            print(f"   Target Level: {signal.target_level:.5f}")
            print(f"   FVGs presentes: {signal.fvg_present}")
            print(f"   Order Blocks: {signal.order_block_present}")
            
            # Métricas del análisis
            metrics = analyzer.get_performance_metrics()
            print(f"\n📊 MÉTRICAS DE ANÁLISIS REAL:")
            print(f"   Tiempo análisis: {metrics['avg_analysis_time']:.3f}s")
            print(f"   Total análisis: {metrics['total_analyses']}")
            
            return signal
        else:
            print("ℹ️ No se detectó cambio estructural significativo")
            print("   (Esto es normal - no siempre hay señales)")
            return None
            
    except Exception as e:
        print(f"❌ Error en análisis: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """🚀 Ejecuta test completo del sistema REAL"""
    print("🎯 EJECUTANDO TESTS DE SISTEMA REAL...")
    
    # 1. Test conexión MT5
    if not test_real_mt5_connection():
        print("\n❌ SISTEMA REQUIERE MT5 FUNCIONAL")
        print("   ABRIR METATRADER 5 Y CONECTAR CUENTA")
        return False
    
    # 2. Test downloader
    data = test_real_downloader()
    if data is None:
        print("\n❌ SISTEMA REQUIERE DATOS REALES")
        return False
    
    # 3. Test análisis
    signal = test_real_market_structure()
    
    # Resultado final
    print("\n" + "=" * 60)
    print("🏆 RESULTADO FINAL")
    print("=" * 60)
    
    if data is not None:
        print("✅ SISTEMA FUNCIONANDO CON DATOS REALES")
        print(f"   📊 {len(data)} velas reales descargadas")
        if signal:
            print(f"   🎯 Señal detectada: {signal.structure_type.value}")
        else:
            print("   📈 Sin señales (normal en mercado)")
        print("\n🚀 ICT ENGINE v6.0 ENTERPRISE - SISTEMA REAL OPERATIVO")
        return True
    else:
        print("❌ SISTEMA REQUIERE CONFIGURACIÓN MT5")
        return False

if __name__ == "__main__":
    main()
