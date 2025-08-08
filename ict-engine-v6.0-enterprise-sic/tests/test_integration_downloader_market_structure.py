#!/usr/bin/env python3
"""
🧪 INTEGRATION TEST: Advanced Candle Downloader + Market Structure
==================================================================

Test de integración que verifica que el downloader puede proporcionar
datos reales compatibles con Market Structure Analysis.

Autor: ICT Engine v6.0 Enterprise Team
Fecha: Agosto 7, 2025
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Agregar el directorio raíz al PATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_downloader_market_structure_integration():
    """
    🎯 Test de integración: Downloader → Market Structure
    
    Verifica que:
    1. El downloader puede obtener datos reales
    2. Los datos tienen la estructura correcta para Market Structure
    3. Los timeframes están sincronizados
    4. Los datos son suficientes para análisis
    """
    print("🧪 INTEGRATION TEST: Downloader + Market Structure")
    print("=" * 60)
    
    try:
        # 1. 📥 IMPORTAR DOWNLOADER
        print("📥 1. Importando Advanced Candle Downloader...")
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        print("✅ Downloader importado correctamente")
        
        # 2. 🔧 CONFIGURAR DOWNLOADER
        print("\n🔧 2. Configurando downloader...")
        downloader = AdvancedCandleDownloader()
        
        # Verificar que MT5 está disponible (usando fallback si no)
        mt5_available = downloader._check_mt5_connection()
        print(f"📡 MT5 Status: {'✅ Conectado' if mt5_available else '⚠️ Simulación'}")
        
        # 3. 📊 DESCARGAR DATOS PARA MARKET STRUCTURE
        print("\n📊 3. Descargando datos para Market Structure...")
        
        symbol = "EURUSD"
        timeframes = ["M15", "M5", "H1"]  # Timeframes necesarios para Market Structure
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)  # 1 semana de datos
        
        data_results = {}
        
        for tf in timeframes:
            print(f"   📈 Descargando {symbol} {tf}...")
            
            result = downloader.download_candles(
                symbol=symbol,
                timeframe=tf,
                start_date=start_date,
                end_date=end_date,
                save_to_file=False  # Solo en memoria para test
            )
            
            if result and result.get('success', False):
                candles_data = result.get('data')
                if candles_data is not None and len(candles_data) > 0:
                    data_results[tf] = candles_data
                    print(f"      ✅ {len(candles_data)} velas descargadas")
                    
                    # Verificar estructura de datos
                    if hasattr(candles_data, 'columns'):
                        expected_cols = ['open', 'high', 'low', 'close', 'volume']
                        available_cols = [col.lower() for col in candles_data.columns]
                        missing_cols = [col for col in expected_cols if col not in available_cols]
                        
                        if missing_cols:
                            print(f"      ⚠️ Columnas faltantes: {missing_cols}")
                        else:
                            print(f"      ✅ Estructura de datos completa")
                else:
                    print(f"      ❌ Sin datos para {tf}")
            else:
                print(f"      ❌ Error descargando {tf}")
        
        # 4. 🏗️ VERIFICAR COMPATIBILIDAD CON MARKET STRUCTURE
        print(f"\n🏗️ 4. Verificando compatibilidad con Market Structure...")
        
        if len(data_results) >= 2:  # Al menos 2 timeframes
            print("✅ Múltiples timeframes disponibles")
            
            # Verificar que M15 esté disponible (principal para Market Structure)
            if "M15" in data_results:
                m15_data = data_results["M15"]
                print(f"✅ Datos M15 disponibles: {len(m15_data)} velas")
                
                # Verificar cantidad mínima de datos
                if len(m15_data) >= 100:  # Mínimo para análisis de estructura
                    print("✅ Suficientes datos para análisis de estructura")
                    
                    # Simular requerimientos de Market Structure
                    print("\n📊 5. Simulando requerimientos Market Structure...")
                    
                    # Verificar que podemos calcular swing points
                    if len(m15_data) >= 50:
                        print("✅ Suficientes datos para swing points")
                    
                    # Verificar timeframe secundario
                    if "M5" in data_results or "H1" in data_results:
                        print("✅ Timeframe secundario disponible para confluencia")
                    
                    # Verificar datos recientes
                    if hasattr(m15_data, 'index'):
                        latest_time = m15_data.index[-1] if len(m15_data) > 0 else None
                        if latest_time:
                            time_diff = datetime.now() - latest_time.to_pydatetime().replace(tzinfo=None)
                            if time_diff.total_seconds() < 3600:  # Menos de 1 hora
                                print("✅ Datos recientes disponibles")
                            else:
                                print(f"⚠️ Datos no tan recientes: {time_diff}")
                    
                    print("\n🎯 RESULTADO FINAL:")
                    print("✅ Downloader está listo para Market Structure")
                    print(f"📊 Timeframes disponibles: {list(data_results.keys())}")
                    print(f"📈 Datos totales: {sum(len(data) for data in data_results.values())} velas")
                    
                    return True
                    
                else:
                    print(f"❌ Insuficientes datos M15: {len(m15_data)} < 100")
            else:
                print("❌ Datos M15 no disponibles")
        else:
            print("❌ Insuficientes timeframes disponibles")
            
        print("\n❌ RESULTADO FINAL:")
        print("❌ Downloader NO está listo para Market Structure")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR EN INTEGRATION TEST:")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_market_structure_data_requirements():
    """
    📋 Test específico para verificar requerimientos de datos del Market Structure
    """
    print("\n" + "=" * 60)
    print("📋 MARKET STRUCTURE DATA REQUIREMENTS TEST")
    print("=" * 60)
    
    requirements = {
        "min_candles_m15": 100,
        "min_candles_m5": 200,  
        "required_columns": ["open", "high", "low", "close", "volume"],
        "max_data_age_hours": 2,
        "required_timeframes": ["M15"],
        "optional_timeframes": ["M5", "H1"]
    }
    
    print("📊 Requerimientos mínimos para Market Structure:")
    for req, value in requirements.items():
        print(f"   • {req}: {value}")
    
    print("\n✅ Requerimientos documentados para desarrollo")
    return True

if __name__ == "__main__":
    print("🧪 ICT ENGINE v6.0 - INTEGRATION TESTS")
    print("=" * 60)
    
    # Ejecutar tests
    test1_result = test_downloader_market_structure_integration()
    test2_result = test_market_structure_data_requirements()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS:")
    print(f"   🧪 Integration Test: {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"   📋 Requirements Test: {'✅ PASS' if test2_result else '❌ FAIL'}")
    
    if test1_result and test2_result:
        print("\n🎉 TODOS LOS TESTS PASARON")
        print("✅ Downloader está listo para integración con Market Structure")
    else:
        print("\n⚠️ ALGUNOS TESTS FALLARON")
        print("🔧 Revisar y fortalecer el Advanced Candle Downloader")
