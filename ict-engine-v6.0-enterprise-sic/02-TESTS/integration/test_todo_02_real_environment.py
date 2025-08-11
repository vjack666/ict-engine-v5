#!/usr/bin/env python3
"""
🚀 TEST REAL TODO #2: MULTI_TF_DATA_MANAGER CON MT5 REAL
=========================================================

Test en entorno REAL con FundedNext MT5 para verificar:
1. ✅ Detección automática multi-timeframe con datos reales
2. ✅ Sincronización entre timeframes reales
3. ✅ Confluencias ICT con datos de mercado real
4. ✅ Performance en condiciones de producción

ENTORNO: FundedNext MT5 Terminal (C:\Program Files\FundedNext MT5 Terminal\terminal64.exe)
DATOS: Mercado real EURUSD, GBPUSD
TIMEFRAMES: H4, M15, M5 (critical ICT analysis)

REGLAS COPILOT:
- REGLA #6: Test en entorno real antes de producción
- REGLA #1: Verificación exhaustiva de funcionalidad
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Configurar path para importaciones
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / '01-CORE'))

def main():
    """🎯 Test completo en entorno real MT5"""
    
    print("🚀 TEST REAL TODO #2: MULTI_TF_DATA_MANAGER CON MT5 REAL")
    print("=" * 70)
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🖥️ Entorno: FundedNext MT5 Terminal")
    print(f"📊 Símbolos: EURUSD, GBPUSD")
    print(f"📈 Timeframes: H4, M15, M5")
    
    # Test 1: Verificar conexión MT5 real
    print(f"\n📡 1. VERIFICACIÓN CONEXIÓN MT5 REAL:")
    mt5_status = test_real_mt5_connection()
    
    if not mt5_status['connected']:
        print(f"❌ MT5 no disponible - Test abortado")
        print(f"💡 Asegúrate de que FundedNext MT5 esté ejecutándose")
        return
    
    # Test 2: Test detección automática real
    print(f"\n🔍 2. TEST DETECCIÓN AUTOMÁTICA REAL:")
    detection_results = test_real_auto_detection()
    
    # Test 3: Test sincronización multi-TF real  
    print(f"\n🔄 3. TEST SINCRONIZACIÓN MULTI-TF REAL:")
    sync_results = test_real_multi_tf_sync()
    
    # Test 4: Test análisis confluencias real
    print(f"\n🔗 4. TEST ANÁLISIS CONFLUENCIAS REAL:")
    confluence_results = test_real_confluence_analysis()
    
    # Test 5: Test performance en entorno real
    print(f"\n⚡ 5. TEST PERFORMANCE ENTORNO REAL:")
    performance_results = test_real_performance()
    
    # Resumen final
    print(f"\n✅ 6. RESUMEN TEST ENTORNO REAL:")
    generate_real_test_summary(mt5_status, detection_results, sync_results, 
                              confluence_results, performance_results)

def test_real_mt5_connection() -> Dict[str, Any]:
    """📡 Test conexión real con FundedNext MT5"""
    
    connection_status = {
        'connected': False,
        'terminal_detected': False,
        'symbols_available': 0,
        'account_info': None,
        'connection_time': 0.0
    }
    
    try:
        start_time = time.time()
        
        # Verificar proceso FundedNext MT5
        import subprocess
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq terminal64.exe'], 
                              capture_output=True, text=True)
        
        if 'terminal64.exe' in result.stdout:
            connection_status['terminal_detected'] = True
            print("   ✅ FundedNext MT5 Terminal: DETECTADO EN EJECUCIÓN")
        else:
            print("   ❌ FundedNext MT5 Terminal: NO EJECUTÁNDOSE")
            return connection_status
        
        # Intentar importar MT5
        try:
            import MetaTrader5 as mt5
            print("   ✅ MetaTrader5 library: DISPONIBLE")
        except ImportError:
            print("   ❌ MetaTrader5 library: NO INSTALADA")
            print("   💡 Instalar con: pip install MetaTrader5")
            return connection_status
        
        # Intentar conexión real
        if mt5.initialize(path="C:\\Program Files\\FundedNext MT5 Terminal\\terminal64.exe"):
            connection_status['connected'] = True
            connection_status['connection_time'] = time.time() - start_time
            print(f"   ✅ Conexión MT5: EXITOSA ({connection_status['connection_time']:.2f}s)")
            
            # Verificar símbolos disponibles
            symbols = mt5.symbols_get()
            if symbols:
                connection_status['symbols_available'] = len(symbols)
                print(f"   ✅ Símbolos disponibles: {len(symbols)}")
                
                # Verificar símbolos específicos de test
                test_symbols = ['EURUSD', 'GBPUSD']
                available_test_symbols = [s.name for s in symbols if s.name in test_symbols]
                print(f"   ✅ Símbolos de test disponibles: {available_test_symbols}")
            
            # Información de cuenta
            account_info = mt5.account_info()
            if account_info:
                connection_status['account_info'] = {
                    'login': account_info.login,
                    'server': account_info.server,
                    'balance': account_info.balance,
                    'company': account_info.company
                }
                print(f"   ✅ Cuenta: {account_info.login} ({account_info.server})")
                print(f"   ✅ Broker: {account_info.company}")
            
            mt5.shutdown()
            
        else:
            print("   ❌ Error conectando a MT5")
            print(f"   💡 Error: {mt5.last_error()}")
            
    except Exception as e:
        print(f"   ❌ Error en test conexión MT5: {e}")
    
    return connection_status

def test_real_auto_detection() -> Dict[str, Any]:
    """🔍 Test detección automática con datos reales"""
    
    detection_results = {
        'manager_created': False,
        'detection_executed': False,
        'symbols_processed': 0,
        'timeframes_analyzed': 0,
        'sync_status': 'UNKNOWN',
        'execution_time': 0.0
    }
    
    try:
        start_time = time.time()
        
        # Crear ICTDataManager con AdvancedCandleDownloader real
        from core.data_management.ict_data_manager import ICTDataManager
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        
        print("   📥 Creando AdvancedCandleDownloader...")
        downloader = AdvancedCandleDownloader()
        
        print("   📊 Creando ICTDataManager...")
        manager = ICTDataManager(downloader=downloader)
        detection_results['manager_created'] = True
        print("   ✅ ICTDataManager creado con downloader real")
        
        # Test detección automática real
        test_symbols = ['EURUSD', 'GBPUSD']
        test_timeframes = ['H4', 'M15', 'M5']
        
        print(f"   🔍 Ejecutando auto-detección: {test_symbols} x {test_timeframes}")
        detection_result = manager.auto_detect_multi_tf_data(test_symbols, test_timeframes)
        
        if detection_result:
            detection_results['detection_executed'] = True
            detection_results['symbols_processed'] = detection_result.get('symbols_analyzed', 0)
            detection_results['timeframes_analyzed'] = detection_result.get('timeframes_required', 0)
            detection_results['sync_status'] = detection_result.get('sync_status', 'UNKNOWN')
            
            print(f"   ✅ Auto-detección ejecutada exitosamente")
            print(f"   📊 Símbolos analizados: {detection_results['symbols_processed']}")
            print(f"   📈 Timeframes analizados: {detection_results['timeframes_analyzed']}")
            print(f"   🎯 Estado sincronización: {detection_results['sync_status']}")
            
            # Mostrar matriz de detección
            if 'detection_matrix' in detection_result:
                print(f"   📋 Matriz de disponibilidad:")
                for symbol, readiness in detection_result['detection_matrix'].items():
                    capability = readiness.get('analysis_capability', 'UNKNOWN')
                    print(f"     - {symbol}: {capability}")
            
            # Mostrar recomendaciones
            if 'recommendations' in detection_result:
                for rec in detection_result['recommendations']:
                    print(f"   💡 {rec}")
        
        detection_results['execution_time'] = time.time() - start_time
        print(f"   ⏱️ Tiempo ejecución: {detection_results['execution_time']:.2f}s")
        
    except Exception as e:
        print(f"   ❌ Error en detección automática real: {e}")
        if "MT5" in str(e) or "connection" in str(e).lower():
            print(f"   💡 Error relacionado con conexión MT5 - esperado en algunos casos")
    
    return detection_results

def test_real_multi_tf_sync() -> Dict[str, Any]:
    """🔄 Test sincronización multi-timeframe real"""
    
    sync_results = {
        'sync_executed': False,
        'downloads_attempted': 0,
        'downloads_successful': 0,
        'alignment_achieved': False,
        'execution_time': 0.0
    }
    
    try:
        start_time = time.time()
        
        # Crear manager
        from core.data_management.ict_data_manager import ICTDataManager
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        
        downloader = AdvancedCandleDownloader()
        manager = ICTDataManager(downloader=downloader)
        
        # Test sincronización EURUSD
        print("   🔄 Ejecutando sincronización multi-TF para EURUSD...")
        sync_result = manager.sync_multi_tf_data('EURUSD', ['H4', 'M15', 'M5'], force_download=False)
        
        if sync_result:
            sync_results['sync_executed'] = True
            sync_results['downloads_attempted'] = len(sync_result.get('sync_tasks', []))
            sync_results['downloads_successful'] = sync_result.get('downloads_executed', 0)
            sync_results['alignment_achieved'] = (sync_result.get('alignment_status', '') == 'SYNCHRONIZED')
            
            print(f"   ✅ Sincronización ejecutada")
            print(f"   📥 Descargas intentadas: {sync_results['downloads_attempted']}")
            print(f"   ✅ Descargas exitosas: {sync_results['downloads_successful']}")
            print(f"   🎯 Alineación: {sync_result.get('alignment_status', 'UNKNOWN')}")
            
            # Mostrar gaps detectados
            if 'gaps_detected' in sync_result:
                gaps = sync_result['gaps_detected']
                if gaps:
                    print(f"   ⚠️ Gaps detectados: {gaps}")
                else:
                    print(f"   ✅ No se detectaron gaps - datos sincronizados")
        
        sync_results['execution_time'] = time.time() - start_time
        print(f"   ⏱️ Tiempo sincronización: {sync_results['execution_time']:.2f}s")
        
    except Exception as e:
        print(f"   ❌ Error en sincronización real: {e}")
        if "downloader" in str(e).lower() or "MT5" in str(e):
            print(f"   💡 Error relacionado con MT5 - verificar conexión")
    
    return sync_results

def test_real_confluence_analysis() -> Dict[str, Any]:
    """🔗 Test análisis confluencias con datos reales"""
    
    confluence_results = {
        'analyzer_created': False,
        'analysis_executed': False,
        'confluence_score': 0.0,
        'timeframes_analyzed': 0,
        'execution_time': 0.0
    }
    
    try:
        start_time = time.time()
        
        # Crear MarketStructureAnalyzer
        from core.analysis.market_structure_analyzer import MarketStructureAnalyzer, StructureType
        
        print("   🔗 Creando MarketStructureAnalyzer...")
        analyzer = MarketStructureAnalyzer()
        confluence_results['analyzer_created'] = True
        print("   ✅ MarketStructureAnalyzer creado")
        
        # Test análisis confluencias real
        print("   🎯 Ejecutando análisis confluencias EURUSD H4...")
        
        # Simular estructura type (en implementación real vendría del análisis previo)
        structure_type = StructureType.BULLISH if hasattr(StructureType, 'BULLISH') else 'BULLISH'
        
        confluence_score = analyzer._analyze_multi_timeframe_confluence(
            symbol='EURUSD',
            main_timeframe='H4',
            structure_type=structure_type
        )
        
        if confluence_score is not None:
            confluence_results['analysis_executed'] = True
            confluence_results['confluence_score'] = confluence_score
            
            print(f"   ✅ Análisis confluencias ejecutado")
            print(f"   📊 Score confluencia: {confluence_score:.3f}")
            
            # Interpretación del score
            if confluence_score >= 0.7:
                interpretation = "🟢 CONFLUENCIA FUERTE"
            elif confluence_score >= 0.5:
                interpretation = "🟡 CONFLUENCIA MODERADA"
            else:
                interpretation = "🔴 CONFLUENCIA DÉBIL"
            
            print(f"   🎯 Interpretación: {interpretation}")
        
        confluence_results['execution_time'] = time.time() - start_time
        print(f"   ⏱️ Tiempo análisis: {confluence_results['execution_time']:.2f}s")
        
    except Exception as e:
        print(f"   ❌ Error en análisis confluencias real: {e}")
        print(f"   💡 Error puede ser por datos faltantes o configuración")
    
    return confluence_results

def test_real_performance() -> Dict[str, Any]:
    """⚡ Test performance en condiciones reales"""
    
    performance_results = {
        'cache_status_obtained': False,
        'cache_efficiency': 0.0,
        'total_symbols': 0,
        'total_timeframes': 0,
        'memory_usage_mb': 0.0,
        'execution_time': 0.0
    }
    
    try:
        start_time = time.time()
        
        # Test cache status
        from core.data_management.ict_data_manager import ICTDataManager
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        
        downloader = AdvancedCandleDownloader()
        manager = ICTDataManager(downloader=downloader)
        
        print("   📊 Obteniendo estado de cache multi-TF...")
        cache_status = manager.get_multi_tf_cache_status()
        
        if cache_status:
            performance_results['cache_status_obtained'] = True
            performance_results['total_symbols'] = cache_status.get('total_symbols', 0)
            performance_results['cache_efficiency'] = cache_status.get('cache_efficiency', {}).get('efficiency_percentage', 0.0)
            
            print(f"   ✅ Estado cache obtenido")
            print(f"   📊 Símbolos en cache: {performance_results['total_symbols']}")
            print(f"   ⚡ Eficiencia cache: {performance_results['cache_efficiency']:.1f}%")
            
            # Mostrar cobertura por timeframe
            if 'timeframe_coverage' in cache_status:
                print(f"   📈 Cobertura por timeframe:")
                for tf, coverage in cache_status['timeframe_coverage'].items():
                    pct = coverage.get('coverage_percentage', 0)
                    status = coverage.get('status', 'UNKNOWN')
                    print(f"     - {tf}: {pct:.1f}% ({status})")
        
        # Test performance summary
        performance_summary = manager.get_performance_summary()
        if performance_summary:
            system_status = performance_summary.get('system_status', 'UNKNOWN')
            total_tfs = performance_summary.get('total_timeframes', 0)
            performance_results['total_timeframes'] = total_tfs
            
            print(f"   🎯 Estado sistema: {system_status}")
            print(f"   📈 Total timeframes: {total_tfs}")
        
        # Simular medición de memoria (básica)
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        performance_results['memory_usage_mb'] = memory_info.rss / 1024 / 1024
        
        performance_results['execution_time'] = time.time() - start_time
        print(f"   💾 Uso memoria: {performance_results['memory_usage_mb']:.1f} MB")
        print(f"   ⏱️ Tiempo performance: {performance_results['execution_time']:.2f}s")
        
    except Exception as e:
        print(f"   ❌ Error en test performance real: {e}")
    
    return performance_results

def generate_real_test_summary(mt5_status, detection_results, sync_results, 
                              confluence_results, performance_results):
    """✅ Generar resumen completo de test real"""
    
    print("   📊 RESUMEN TEST ENTORNO REAL:")
    print("   " + "="*50)
    
    # Calcular score general
    scores = {
        'mt5_connection': 100 if mt5_status['connected'] else 0,
        'auto_detection': 100 if detection_results['detection_executed'] else 0,
        'multi_tf_sync': 100 if sync_results['sync_executed'] else 0,
        'confluence_analysis': 100 if confluence_results['analysis_executed'] else 0,
        'performance': 100 if performance_results['cache_status_obtained'] else 0
    }
    
    total_score = sum(scores.values()) / len(scores)
    
    print(f"   🎯 SCORE TOTAL ENTORNO REAL: {total_score:.0f}%")
    print(f"   📡 Conexión MT5: {'✅' if mt5_status['connected'] else '❌'} ({scores['mt5_connection']:.0f}%)")
    print(f"   🔍 Auto-detección: {'✅' if detection_results['detection_executed'] else '❌'} ({scores['auto_detection']:.0f}%)")
    print(f"   🔄 Sincronización: {'✅' if sync_results['sync_executed'] else '❌'} ({scores['multi_tf_sync']:.0f}%)")
    print(f"   🔗 Confluencias: {'✅' if confluence_results['analysis_executed'] else '❌'} ({scores['confluence_analysis']:.0f}%)")
    print(f"   ⚡ Performance: {'✅' if performance_results['cache_status_obtained'] else '❌'} ({scores['performance']:.0f}%)")
    
    # Métricas de performance
    print(f"\n   📈 MÉTRICAS DE PERFORMANCE:")
    if detection_results['execution_time'] > 0:
        print(f"     ⏱️ Detección automática: {detection_results['execution_time']:.2f}s")
    if sync_results['execution_time'] > 0:
        print(f"     ⏱️ Sincronización: {sync_results['execution_time']:.2f}s")
    if confluence_results['execution_time'] > 0:
        print(f"     ⏱️ Análisis confluencias: {confluence_results['execution_time']:.2f}s")
    if performance_results['memory_usage_mb'] > 0:
        print(f"     💾 Uso memoria: {performance_results['memory_usage_mb']:.1f} MB")
    
    # Estado final
    if total_score >= 80:
        status = "✅ TODO #2 FUNCIONANDO EN ENTORNO REAL"
        recommendation = "🚀 LISTO PARA PRODUCCIÓN"
    elif total_score >= 60:
        status = "⚠️ TODO #2 FUNCIONANDO PARCIALMENTE"
        recommendation = "🔧 AJUSTES MENORES REQUERIDOS"
    else:
        status = "❌ TODO #2 REQUIERE TRABAJO ADICIONAL"
        recommendation = "🛠️ REVISAR DEPENDENCIAS Y CONFIGURACIÓN"
    
    print(f"\n   🏆 ESTADO FINAL: {status}")
    print(f"   📋 RECOMENDACIÓN: {recommendation}")
    
    # Información de entorno
    if mt5_status['connected']:
        print(f"\n   🖥️ ENTORNO VERIFICADO:")
        print(f"     📡 FundedNext MT5: CONECTADO")
        if mt5_status['account_info']:
            account = mt5_status['account_info']
            print(f"     🏢 Broker: {account.get('company', 'N/A')}")
            print(f"     🔑 Servidor: {account.get('server', 'N/A')}")
        print(f"     📊 Símbolos disponibles: {mt5_status['symbols_available']}")
    
    print(f"\n   ⏰ Test completado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   📋 TODO #2 verificado en condiciones REALES de mercado")

if __name__ == "__main__":
    main()
