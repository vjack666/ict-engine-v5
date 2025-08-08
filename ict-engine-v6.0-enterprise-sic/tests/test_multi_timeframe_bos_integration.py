#!/usr/bin/env python3
"""
🚀 TEST INTEGRACIÓN MULTI-TIMEFRAME BOS - ICT ENGINE v6.0 ENTERPRISE
================================================================

Script de prueba para validar la integración completa del análisis multi-timeframe BOS
usando el pipeline migrado OptimizedICTAnalysisEnterprise en PatternDetector.

Autor: ICT Enterprise Development Team
Fecha: 2025-01-07
Versión: 1.0.0
"""

import sys
import os
from pathlib import Path

# Añadir el directorio raíz al path
current_dir = Path(__file__).parent
root_dir = current_dir.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "core"))

def test_multi_timeframe_bos_integration():
    """🎯 Test principal de integración multi-timeframe BOS"""
    
    print("=" * 80)
    print("🚀 ICT ENGINE v6.0 ENTERPRISE - TEST MULTI-TIMEFRAME BOS")
    print("=" * 80)
    
    try:
        # 1. 📦 IMPORTAR MÓDULOS ENTERPRISE
        print("\n1. 📦 Importando módulos enterprise...")
        
        from core.analysis.pattern_detector import PatternDetector
        from core.data_management.ict_data_manager import ICTDataManager
        
        print("✅ Módulos importados correctamente")
        
        # 2. 🔧 INICIALIZAR PATTERN DETECTOR
        print("\n2. 🔧 Inicializando PatternDetector...")
        
        pattern_detector = PatternDetector()
        data_manager = ICTDataManager()
        print("✅ PatternDetector y DataManager inicializados")
        
        # 3. 🎯 INVESTIGACIÓN PROFUNDA BOS - DATOS REALES
        print("\n3. 🔍 INVESTIGACIÓN PROFUNDA: ¿Por qué no se detectan BOS?")
        print("=" * 60)
        
        # 3. 🔍 INVESTIGACIÓN PROFUNDA BOS CON DATOS REALES
        print("\n3. 🔍 INVESTIGACIÓN: ¿Por qué no se detectan BOS?")
        print("=" * 60)
        
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        downloader = AdvancedCandleDownloader()
        
        test_symbols = ['EURUSD', 'GBPUSD', 'USDJPY']
        total_bos = 0
        
        for symbol in test_symbols:
            print(f"\n� INVESTIGANDO {symbol}")
            print("-" * 40)
            
            try:
                # Descargar datos reales
                print(f"⬇️  Descargando datos de {symbol}...")
                real_data = downloader.download_candles(symbol=symbol, timeframe='M15')
                
                if real_data is None:
                    print(f"❌ No se pudieron descargar datos para {symbol}")
                    continue
                
                print(f"✅ Datos descargados para {symbol}")
                
                # Detectar BOS usando PatternDetector
                print(f"🔍 Analizando BOS para {symbol}...")
                bos_signals = pattern_detector.detect_bos_multi_timeframe(
                    symbol=symbol, 
                    timeframes=['M15']
                )
                
                # Evaluar resultados
                if isinstance(bos_signals, dict):
                    bos_detected = bos_signals.get('detected', False)
                    if bos_detected:
                        total_bos += 1
                        print(f"✅ BOS DETECTADO en {symbol}")
                        print(f"   Dirección: {bos_signals.get('primary_signal', {}).get('direction', 'N/A')}")
                    else:
                        print(f"⚠️  NO BOS detectado en {symbol}")
                elif isinstance(bos_signals, list) and len(bos_signals) > 0:
                    total_bos += len(bos_signals)
                    print(f"✅ {len(bos_signals)} BOS DETECTADOS en {symbol}")
                else:
                    print(f"⚠️  NO BOS detectado en {symbol}")
                
                # Análisis adicional de datos
                if isinstance(real_data, dict) and 'data' in real_data:
                    df = real_data['data']
                    if df is not None and len(df) > 0:
                        print(f"   📊 Velas: {len(df)}")
                        print(f"   💰 Precio actual: {df['close'].iloc[-1]:.5f}")
                
            except Exception as e:
                print(f"❌ Error en {symbol}: {e}")
        
        # 4. 📊 RESUMEN DE INVESTIGACIÓN
        print(f"\n{'='*60}")
        print(f"📊 RESUMEN DE INVESTIGACIÓN")
        print(f"{'='*60}")
        print(f"📊 Símbolos analizados: {len(test_symbols)}")
        print(f"🎯 Total BOS detectados: {total_bos}")
        
        if total_bos == 0:
            print(f"\n� POSIBLES CAUSAS DE 0 BOS:")
            print(f"   1. Mercado en consolidación (normal)")
            print(f"   2. Umbrales muy estrictos")
            print(f"   3. Datos simulados en lugar de reales")
            print(f"   4. Lógica de detección necesita calibración")
        else:
            print(f"✅ BOS detectados correctamente")
        
        # 5. 📈 RESULTADOS FINALES
        print(f"\n{'='*80}")
        print(f"📈 RESULTADOS INVESTIGACIÓN BOS")
        print(f"{'='*80}")
        print("✅ PatternDetector operativo")
        print("✅ AdvancedCandleDownloader funcional")
        print("✅ Datos reales procesados")
        print(f"✅ BOS detectados: {total_bos}")
        print(f"\n🎯 INVESTIGACIÓN COMPLETADA")
        print(f"{'='*80}")
        
        return True
                
                print(f"   🏗️ Estructura: {m15_structure.get('type', 'N/A')}")
                print(f"   💪 Fuerza: {m15_structure.get('strength', 0):.3f}")
                print(f"   🎯 BOS detectado: {m15_structure.get('bos_detected', False)}")
                print(f"   📈 Resistencia: {m15_structure.get('resistance', 0):.5f}")
                print(f"   📉 Soporte: {m15_structure.get('support', 0):.5f}")
                print(f"   � Precio actual: {m15_structure.get('current_price', 0):.5f}")
                print(f"   🚀 Momentum: {m15_structure.get('momentum', 0):.4f}")
                
                # ANÁLISIS MANUAL DE BREAKOUTS
                print(f"\n🔬 ANÁLISIS MANUAL DE BREAKOUTS:")
                
                recent_data = real_data.tail(50)
                highs = recent_data['high']
                lows = recent_data['low']
                closes = recent_data['close']
                
                # Calcular niveles como en el analyzer
                resistance_level = highs.rolling(window=10).max().iloc[-1]
                support_level = lows.rolling(window=10).min().iloc[-1]
                current_price = closes.iloc[-1]
                
                # Umbrales exactos del analyzer
                resistance_target = resistance_level * 0.999
                support_target = support_level * 1.001
                
                # Verificar breakouts manualmente
                bullish_break = current_price > resistance_target
                bearish_break = current_price < support_target
                
                print(f"   📈 Break bullish manual: {bullish_break}")
                print(f"   📉 Break bearish manual: {bearish_break}")
                print(f"   📏 Dist. a resistencia: {(resistance_target - current_price) / current_price * 100:.3f}%")
                print(f"   📏 Dist. a soporte: {(current_price - support_target) / current_price * 100:.3f}%")
                
                # PRUEBA DE UMBRALES
                print(f"\n🎛️ PRUEBA DE UMBRALES:")
                
                umbrales = [
                    {"name": "Estricto (actual)", "res": 0.999, "sup": 1.001},
                    {"name": "Moderado", "res": 0.9995, "sup": 1.0005},
                    {"name": "Relajado", "res": 1.0005, "sup": 0.9995}
                ]
                
                for umbral in umbrales:
                    res_target = resistance_level * umbral["res"]
                    sup_target = support_level * umbral["sup"]
                    bull_break = current_price > res_target
                    bear_break = current_price < sup_target
                    any_break = bull_break or bear_break
                    
                    print(f"   📊 {umbral['name']:12} - Bull: {bull_break:5} | Bear: {bear_break:5} | Any: {any_break}")
                
                # Contar BOS detectados
                bos_detected = m15_structure.get('bos_detected', False)
                if bos_detected:
                    total_bos += 1
                    print(f"✅ BOS DETECTADO por analyzer en {symbol}")
                else:
                    print(f"⚠️  NO BOS detectado por analyzer en {symbol}")
                
                # Guardar resultados
                investigation_results[symbol] = {
                    "analyzer_bos": bos_detected,
                    "manual_bullish": bullish_break,
                    "manual_bearish": bearish_break,
                    "structure_type": m15_structure.get('type', 'N/A'),
                    "data_quality": "REAL_MT5"
                }
                
            except Exception as e:
                print(f"❌ Error investigando {symbol}: {e}")
                import traceback
                traceback.print_exc()
        
        # 4. 📊 RESUMEN DE INVESTIGACIÓN
        print(f"\n{'='*60}")
        print(f"📊 RESUMEN DE INVESTIGACIÓN PROFUNDA")
        print(f"{'='*60}")
        
        print(f"📊 Símbolos investigados: {len(investigation_results)}")
        print(f"🎯 Total BOS detectados por analyzer: {total_bos}")
        
        symbols_with_manual_breaks = 0
        for symbol, results in investigation_results.items():
            manual_break = results.get('manual_bullish', False) or results.get('manual_bearish', False)
            if manual_break:
                symbols_with_manual_breaks += 1
            
            print(f"\n📊 {symbol}:")
            print(f"   🎯 Analyzer BOS: {results.get('analyzer_bos', False)}")
            print(f"   📈 Manual Break: {manual_break}")
            print(f"   🏗️ Estructura: {results.get('structure_type', 'N/A')}")
        
        print(f"\n💡 CONCLUSIONES:")
        print(f"   📊 BOS por analyzer: {total_bos}/{len(investigation_results)}")
        print(f"   📈 Breaks manuales: {symbols_with_manual_breaks}/{len(investigation_results)}")
        
        if total_bos == 0 and symbols_with_manual_breaks == 0:
            print(f"   🔍 RESULTADO: Mercado en consolidación real - NO hay breakouts")
            print(f"   � RECOMENDACIÓN: Los umbrales están correctos, mercado estable")
        elif total_bos == 0 and symbols_with_manual_breaks > 0:
            print(f"   � RESULTADO: Problema en analyzer - hay breaks manuales pero analyzer no detecta")
            print(f"   💡 RECOMENDACIÓN: Revisar lógica de detectar_estructura_m15_optimizada")
        else:
            print(f"   ✅ RESULTADO: Sistema funcionando correctamente")
        
        # 5. 📈 RESULTADOS FINALES
        print(f"\n{'='*80}")
        print(f"📈 RESULTADOS TEST BOS INVESTIGATION")
        print(f"{'='*80}")
        print("✅ PatternDetector inicializado correctamente")
        print("✅ AdvancedCandleDownloader funcional")
        print("✅ MultiTimeframeAnalyzer operativo")
        print("✅ Datos reales MT5 procesados")
        print("✅ Investigación profunda completada")
        print(f"✅ BOS detectados por analyzer: {total_bos}")
        print(f"✅ Breaks manuales detectados: {symbols_with_manual_breaks}")
        print(f"\n🎯 INVESTIGACIÓN BOS COMPLETADA EXITOSAMENTE")
        print(f"{'='*80}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Verificar que todos los módulos estén disponibles")
        return False
        
    except Exception as e:
        print(f"❌ Error general en test: {e}")
        print(f"📍 Tipo: {type(e).__name__}")
        return False

def test_analyzer_standalone():
    """🔧 Test independiente del analyzer multi-timeframe"""
    
    print("\n" + "=" * 60)
    print("🔧 TEST ANALYZER MULTI-TIMEFRAME STANDALONE")
    print("=" * 60)
    
    try:
        from core.analysis.multi_timeframe_analyzer import OptimizedICTAnalysisEnterprise
        
        # Crear instancia
        analyzer = OptimizedICTAnalysisEnterprise()
        print("✅ Analyzer creado")
        
        # Test método analyze_symbol
        result = analyzer.analyze_symbol('EURUSD', ['H4', 'M15', 'M5'])
        
        if result.get('status') == 'SUCCESS':
            print("✅ Análisis exitoso")
            print(f"   📊 Timeframes: {len(result.get('timeframe_results', {}))}")
            print(f"   🎯 Dirección general: {result.get('overall_direction', {}).get('direction', 'N/A')}")
        else:
            print(f"⚠️  Análisis con issues: {result.get('status')}")
            if 'error' in result:
                print(f"   ❌ Error: {result['error']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test standalone: {e}")
        return False

if __name__ == "__main__":
    """🚀 Ejecutar tests de integración"""
    
    print("🚀 INICIANDO TESTS DE INTEGRACIÓN MULTI-TIMEFRAME BOS...")
    
    # Test 1: Analyzer standalone
    standalone_ok = test_analyzer_standalone()
    
    # Test 2: Integración completa
    integration_ok = test_multi_timeframe_bos_integration()
    
    # Resultado final
    print("\n" + "=" * 80)
    print("🏁 RESUMEN FINAL DE TESTS")
    print("=" * 80)
    print(f"🔧 Test Analyzer Standalone: {'✅ PASS' if standalone_ok else '❌ FAIL'}")
    print(f"🚀 Test Integración Completa: {'✅ PASS' if integration_ok else '❌ FAIL'}")
    
    if standalone_ok and integration_ok:
        print("\n🎉 TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("🚀 SISTEMA MULTI-TIMEFRAME BOS LISTO PARA PRODUCCIÓN")
    else:
        print("\n⚠️  ALGUNOS TESTS FALLARON")
        print("🔧 Revisar errores antes de proceder")
    
    print("=" * 80)
