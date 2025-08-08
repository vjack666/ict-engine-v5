#!/usr/bin/env python3
"""
🧪 TEST MIGRACIÓN MEMORIA LEGACY - FASE 1
==========================================

Test rápido para verificar que los componentes migrados funcionan correctamente.

Fecha: Agosto 8, 2025
Estado: FASE 1 - MIGRACIÓN COMPLETADA
"""

import sys
import traceback
from datetime import datetime

def test_market_context():
    """Test MarketContext migrado"""
    print("🧠 Testing MarketContext migration...")
    
    try:
        from core.analysis.market_context import MarketContext, get_market_context
        
        # Test creación
        context = MarketContext()
        print(f"✅ MarketContext creado: {context}")
        
        # Test funciones básicas
        context.update_market_bias("BULLISH", 0.8)
        print(f"✅ Bias actualizado: {context.h4_bias}")
        
        # Test eventos BOS/CHoCH
        context.add_bos_event({
            'timeframe': 'M15',
            'direction': 'bullish',
            'strength': 0.75,
            'confidence': 0.85
        })
        print(f"✅ BOS event agregado: {len(context.bos_events)} eventos")
        
        # Test contexto histórico
        historical = context.get_historical_context("M15", "BOS")
        print(f"✅ Contexto histórico obtenido: {len(historical)} keys")
        
        # Test instancia global
        global_context = get_market_context()
        print(f"✅ Instancia global: {type(global_context).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en MarketContext: {e}")
        traceback.print_exc()
        return False

def test_historical_analyzer():
    """Test ICTHistoricalAnalyzer migrado"""
    print("\n📈 Testing ICTHistoricalAnalyzer migration...")
    
    try:
        from core.analysis.ict_historical_analyzer import ICTHistoricalAnalyzer, get_historical_analyzer
        from core.analysis.market_context import MarketContext
        
        # Test creación con MarketContext
        context = MarketContext()
        analyzer = ICTHistoricalAnalyzer(context)
        print(f"✅ ICTHistoricalAnalyzer creado: {type(analyzer).__name__}")
        
        # Test análisis BOS performance
        bos_performance = analyzer.analyze_bos_performance("EURUSD")
        print(f"✅ BOS Performance: {bos_performance.get('status', 'unknown')}")
        
        # Test análisis CHoCH performance
        choch_performance = analyzer.analyze_choch_performance("EURUSD")
        print(f"✅ CHoCH Performance: {choch_performance.get('status', 'unknown')}")
        
        # Test threshold adaptativo
        adaptive_threshold = analyzer.get_adaptive_threshold("BOS", "EURUSD")
        print(f"✅ Threshold adaptativo BOS: {adaptive_threshold:.2f}")
        
        # Test instancia global
        global_analyzer = get_historical_analyzer()
        print(f"✅ Instancia global: {type(global_analyzer).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en ICTHistoricalAnalyzer: {e}")
        traceback.print_exc()
        return False

def test_trading_decision_cache():
    """Test TradingDecisionCache migrado"""
    print("\n💾 Testing TradingDecisionCache migration...")
    
    try:
        from core.smart_trading_logger import (
            TradingDecisionCacheV6, 
            get_trading_decision_cache,
            log_trading_decision_smart_v6
        )
        
        # Test creación
        cache = TradingDecisionCacheV6()
        print(f"✅ TradingDecisionCacheV6 creado: {type(cache).__name__}")
        
        # Test should_log_event
        test_data = {
            'timeframe': 'M15',
            'direction': 'bullish',
            'strength': 0.8
        }
        
        should_log_1 = cache.should_log_event("BOS_TEST", test_data)
        should_log_2 = cache.should_log_event("BOS_TEST", test_data)  # Mismo estado
        
        print(f"✅ Should log first: {should_log_1}, second: {should_log_2}")
        
        # Test Smart Money cache
        sm_analysis = {
            'bias': 'bullish',
            'institutional_flow': 0.75,
            'confidence': 0.8
        }
        
        is_significant = cache.is_significant_smart_money_change(sm_analysis)
        print(f"✅ Smart Money change significant: {is_significant}")
        
        # Test estadísticas
        stats = cache.get_cache_statistics()
        print(f"✅ Cache stats: Hit rate {stats['hit_rate_percent']}%")
        
        # Test instancia global
        global_cache = get_trading_decision_cache()
        print(f"✅ Instancia global: {type(global_cache).__name__}")
        
        # Test logging inteligente
        logged = log_trading_decision_smart_v6("BOS_DETECTION", test_data, symbol="EURUSD")
        print(f"✅ Logging inteligente: {logged}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en TradingDecisionCache: {e}")
        traceback.print_exc()
        return False

def test_integration():
    """Test integración entre componentes"""
    print("\n🔗 Testing component integration...")
    
    try:
        from core.analysis.market_context import MarketContext
        from core.analysis.ict_historical_analyzer import ICTHistoricalAnalyzer
        from core.smart_trading_logger import get_trading_decision_cache
        
        # Crear sistema integrado
        context = MarketContext()
        analyzer = ICTHistoricalAnalyzer(context)
        cache = get_trading_decision_cache()
        
        print("✅ Componentes integrados creados")
        
        # Test flujo completo
        # 1. Agregar evento BOS al contexto
        context.add_bos_event({
            'timeframe': 'M15',
            'direction': 'bullish',
            'strength': 0.85,
            'confidence': 0.9,
            'success': True  # Simular evento exitoso
        })
        
        # 2. Analizar con historical analyzer
        bos_analysis = analyzer.analyze_bos_performance("EURUSD")
        
        # 3. Obtener threshold adaptativo
        adaptive_threshold = analyzer.get_adaptive_threshold("BOS", "EURUSD")
        
        # 4. Test cache de decisión
        decision_data = {
            'analysis': bos_analysis,
            'threshold': adaptive_threshold,
            'context_quality': context.assess_current_quality()
        }
        
        should_log = cache.should_log_event("INTEGRATED_ANALYSIS", decision_data)
        
        print(f"✅ Flujo integrado completado:")
        print(f"   - BOS events en contexto: {len(context.bos_events)}")
        print(f"   - BOS analysis status: {bos_analysis.get('status', 'unknown')}")
        print(f"   - Threshold adaptativo: {adaptive_threshold:.2f}")
        print(f"   - Should log decision: {should_log}")
        print(f"   - Context quality: {context.assess_current_quality():.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en integración: {e}")
        traceback.print_exc()
        return False

def main():
    """Test principal de migración Fase 1"""
    print("🚀 INICIO TEST MIGRACIÓN MEMORIA LEGACY - FASE 1")
    print("=" * 60)
    
    start_time = datetime.now()
    
    # Ejecutar tests
    tests = [
        ("MarketContext", test_market_context),
        ("ICTHistoricalAnalyzer", test_historical_analyzer),
        ("TradingDecisionCache", test_trading_decision_cache),
        ("Integration", test_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Test {test_name} falló: {e}")
            results[test_name] = False
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN FASE 1 - MIGRACIÓN MEMORIA LEGACY:")
    print("-" * 60)
    
    total_tests = len(tests)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print("-" * 60)
    print(f"🎯 RESULTADO FINAL:")
    print(f"   Tests ejecutados: {total_tests}")
    print(f"   Tests exitosos: {passed_tests}")
    print(f"   Tests fallidos: {failed_tests}")
    print(f"   Tasa de éxito: {(passed_tests/total_tests)*100:.1f}%")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"   Tiempo total: {duration:.2f}s")
    
    if passed_tests == total_tests:
        print("\n🎉 ¡FASE 1 COMPLETADA EXITOSAMENTE!")
        print("✅ Componentes de memoria migrados y funcionando")
        print("🚀 Listo para FASE 2: Memoria Unificada v6.0")
    else:
        print(f"\n⚠️ FASE 1 PARCIALMENTE COMPLETADA")
        print(f"❌ {failed_tests} componentes requieren atención")
        print("🔧 Revisar errores antes de continuar")

if __name__ == "__main__":
    main()
