#!/usr/bin/env python3
"""
🚀 TEST FTMO MT5 TERMINAL - ICT ENGINE v6.0 ENTERPRISE
=========================================================

Test específico para FTMO Global Markets MT5 Terminal
Path: C:\Program Files\FTMO Global Markets MT5 Terminal\terminal64.exe

REQUISITOS:
1. FTMO Global Markets MT5 Terminal instalado
2. Cuenta FTMO Global Markets conectada
3. EURUSD disponible
"""

import sys
sys.path.append('.')

import os
import subprocess
import time
from datetime import datetime, timedelta
from core.analysis.market_structure_analyzer import get_market_structure_analyzer
from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader

# Configuración FTMO Global Markets
FTMO_PATH = r"C:\Program Files\FTMO Global Markets MT5 Terminal\terminal64.exe"

def check_ftmo_installation():
    """🔍 Verificar instalación de FTMO Global Markets"""
    print("=" * 60)
    print("🔍 VERIFICANDO FTMO MT5 TERMINAL")
    print("=" * 60)
    
    if os.path.exists(FTMO_PATH):
        print(f"✅ FTMO Global Markets encontrado: {FTMO_PATH}")
        
        # Verificar tamaño del archivo
        size = os.path.getsize(FTMO_PATH)
        print(f"   Tamaño: {size / (1024*1024):.1f} MB")
        return True
    else:
        print(f"❌ FTMO Global Markets NO encontrado en: {FTMO_PATH}")
        print("   Verificar instalación de FTMO Global Markets MT5 Terminal")
        return False

def check_ftmo_running():
    """🔍 Verificar si FTMO Global Markets está corriendo"""
    try:
        import psutil
        
        print("\n🔍 Verificando procesos FTMO Global Markets...")
        ftmo_found = False
        
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if proc.info['name'] and 'terminal64.exe' in proc.info['name'].lower():
                    if proc.info['exe'] and 'ftmo' in proc.info['exe'].lower():
                        print(f"✅ FTMO Global Markets corriendo: PID {proc.info['pid']}")
                        print(f"   Ejecutable: {proc.info['exe']}")
                        ftmo_found = True
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if not ftmo_found:
            print("❌ FTMO Global Markets MT5 Terminal no está corriendo")
            
        return ftmo_found
        
    except Exception as e:
        print(f"❌ Error verificando procesos: {e}")
        return False

def start_ftmo():
    """🚀 Iniciar FTMO Global Markets MT5 Terminal"""
    print("\n🚀 Iniciando FTMO Global Markets MT5 Terminal...")
    
    try:
        # Abrir FTMO Global Markets
        subprocess.Popen([FTMO_PATH], shell=True)
        print("✅ Comando de inicio ejecutado")
        
        # Esperar a que se inicie
        print("⏳ Esperando 5 segundos para que se inicie...")
        time.sleep(5)
        
        # Verificar que se haya iniciado
        if check_ftmo_running():
            print("✅ FTMO Global Markets MT5 Terminal iniciado correctamente")
            return True
        else:
            print("❌ FTMO Global Markets no se inició correctamente")
            return False
            
    except Exception as e:
        print(f"❌ Error iniciando FTMO Global Markets: {e}")
        return False

def test_ftmo_mt5_connection():
    """🔌 Test conexión específica con FTMO Global Markets"""
    print("\n" + "=" * 60)
    print("🔌 TEST CONEXIÓN FTMO MT5")
    print("=" * 60)
    
    try:
        import MetaTrader5 as mt5
        print("✅ MetaTrader5 library disponible")
        
        # Intentar con path específico de FTMO Global Markets
        print(f"🎯 Conectando a FTMO Global Markets: {FTMO_PATH}")
        
        if mt5.initialize(path=FTMO_PATH):
            print("✅ MT5 inicializado con FTMO Global Markets path")
        elif mt5.initialize():
            print("✅ MT5 inicializado automáticamente")
        else:
            print("❌ No se pudo inicializar MT5")
            print("   ¿Está FTMO Global Markets abierto con cuenta conectada?")
            return False
        
        # Verificar cuenta
        account = mt5.account_info()
        if account:
            print(f"✅ Cuenta FTMO Global Markets: {account.login}")
            print(f"   Broker: {account.company}")
            print(f"   Balance: {account.balance} {account.currency}")
            print(f"   Leverage: 1:{account.leverage}")
            
            # Verificar que es FTMO Global Markets
            if 'funded' in account.company.lower() or 'funded' in str(account.login).lower():
                print("✅ Confirmado: Cuenta FTMO Global Markets detectada")
            else:
                print(f"ℹ️ Broker: {account.company} (verificar si es FTMO Global Markets)")
            
            # Test símbolo
            eurusd = mt5.symbol_info("EURUSD")
            if eurusd:
                print(f"✅ EURUSD disponible: Bid={eurusd.bid}, Ask={eurusd.ask}")
                print(f"   Spread: {(eurusd.ask - eurusd.bid) * 10000:.1f} pips")
                return True
            else:
                print("❌ EURUSD no disponible en FTMO Global Markets")
                return False
        else:
            print("❌ Sin cuenta conectada en FTMO Global Markets")
            print("   CONECTAR CUENTA EN FTMO MT5 TERMINAL")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ftmo_downloader():
    """📥 Test descarga con FTMO Global Markets"""
    print("\n" + "=" * 60)
    print("📥 TEST DOWNLOADER CON FTMO")
    print("=" * 60)
    
    try:
        downloader = AdvancedCandleDownloader()
        print("✅ AdvancedCandleDownloader creado")
        
        # Test conexión FTMO Global Markets
        if not downloader._check_mt5_connection():
            print("❌ No se pudo conectar a FTMO Global Markets")
            print("   ABRIR FTMO Y CONECTAR CUENTA")
            return None
        
        # Descargar datos REALES de FTMO Global Markets
        end_date = datetime.now()
        start_date = end_date - timedelta(hours=6)  # 6 horas de datos
        
        print(f"🌍 Descargando datos REALES de FTMO Global Markets...")
        print(f"   Símbolo: EURUSD")
        print(f"   Timeframe: M15")
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
            print(f"✅ DATOS REALES de FTMO Global Markets: {len(data)} velas")
            print(f"   Source: {result.get('source', 'unknown')}")
            print(f"   Última vela:")
            print(f"     Open: {data.iloc[-1]['open']:.5f}")
            print(f"     High: {data.iloc[-1]['high']:.5f}")
            print(f"     Low: {data.iloc[-1]['low']:.5f}")
            print(f"     Close: {data.iloc[-1]['close']:.5f}")
            print(f"     Volume: {data.iloc[-1].get('volume', 'N/A')}")
            return data
        else:
            print(f"❌ Error descargando de FTMO Global Markets: {result['error']}")
            return None
            
    except Exception as e:
        print(f"❌ Error en downloader: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_ftmo_analysis():
    """🏗️ Test análisis con datos de FTMO Global Markets"""
    print("\n" + "=" * 60)
    print("🏗️ TEST ANÁLISIS CON DATOS FTMO")
    print("=" * 60)
    
    try:
        # Configuración para FTMO Global Markets
        config = {
            'enable_debug': True,
            'min_confidence': 55.0,  # Más sensible para datos reales
            'swing_window': 4,
            'fvg_min_gap': 0.0003,   # 3 pips para FTMO Global Markets
            'structure_lookback': 40
        }
        
        analyzer = get_market_structure_analyzer(config)
        print("✅ MarketStructureAnalyzer configurado para FTMO Global Markets")
        
        # Análisis con datos FTMO Global Markets
        print("🌍 Analizando estructura con datos FTMO Global Markets...")
        signal = analyzer.analyze_market_structure(
            symbol="EURUSD",
            timeframe="M15",
            lookback_days=2  # 2 días de datos FTMO Global Markets
        )
        
        if signal:
            print("✅ SEÑAL DETECTADA CON DATOS FTMO:")
            print(f"   🏗️ Estructura: {signal.structure_type.value}")
            print(f"   📈 Dirección: {signal.direction.value}")
            print(f"   🎯 Confianza: {signal.confidence:.1f}%")
            print(f"   📊 Break Level: {signal.break_level:.5f}")
            print(f"   🎯 Target Level: {signal.target_level:.5f}")
            print(f"   💎 FVGs: {'Sí' if signal.fvg_present else 'No'}")
            print(f"   📦 Order Blocks: {'Sí' if signal.order_block_present else 'No'}")
            
            # Estado del analizador
            state = analyzer.get_current_structure_state()
            print(f"\n📊 ESTADO ACTUAL FTMO:")
            print(f"   Tendencia: {state.get('current_trend', 'N/A')}")
            print(f"   FVGs detectados: {len(state.get('detected_fvgs', []))}")
            print(f"   Order Blocks: {len(state.get('detected_order_blocks', []))}")
            
            return signal
        else:
            print("ℹ️ No se detectó cambio estructural")
            print("   (Normal en mercado - no siempre hay señales)")
            return None
            
    except Exception as e:
        print(f"❌ Error en análisis: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """🚀 Test completo FTMO Global Markets MT5 Terminal"""
    print("🎯 ICT ENGINE v6.0 ENTERPRISE - TEST FTMO")
    print("=" * 60)
    
    # 1. Verificar instalación
    if not check_ftmo_installation():
        print("\n❌ FTMO NO INSTALADO")
        return False
    
    # 2. Verificar si está corriendo
    if not check_ftmo_running():
        print("\n🚀 FTMO Global Markets no está corriendo, intentando iniciar...")
        if not start_ftmo():
            print("\n❌ NO SE PUDO INICIAR FTMO")
            print("   ABRIR MANUALMENTE Y CONECTAR CUENTA")
            return False
    
    # 3. Test conexión MT5
    if not test_ftmo_mt5_connection():
        print("\n❌ CONEXIÓN FTMO FALLIDA")
        return False
    
    # 4. Test downloader
    data = test_ftmo_downloader()
    if data is None:
        print("\n❌ DESCARGA FTMO FALLIDA")
        return False
    
    # 5. Test análisis
    signal = test_ftmo_analysis()
    
    # Resultado final
    print("\n" + "=" * 60)
    print("🏆 RESULTADO FINAL FTMO")
    print("=" * 60)
    
    if data is not None:
        print("✅ SISTEMA FUNCIONANDO CON FTMO MT5")
        print(f"   📊 {len(data)} velas reales descargadas")
        print(f"   🏢 Broker: FTMO Global Markets")
        if signal:
            print(f"   🎯 Señal: {signal.structure_type.value} ({signal.confidence:.1f}%)")
        else:
            print("   📈 Sin señales actuales")
        print("\n🚀 ICT ENGINE v6.0 + FTMO - SISTEMA OPERATIVO")
        return True
    else:
        print("❌ SISTEMA REQUIERE FTMO FUNCIONAL")
        return False

if __name__ == "__main__":
    main()
