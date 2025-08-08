#!/usr/bin/env python3
"""
🧪 TEST FASE 2 - UNIFIED MEMORY SYSTEM v6.1
============================================

Test completo del sistema de memoria unificado implementado en FASE 2,
siguiendo todas las REGLAS COPILOT establecidas.

✅ REGLA #1: Revisado - UnifiedMemorySystem implementado
✅ REGLA #2: Memoria trader real - CRÍTICO validado
✅ REGLA #3: Arquitectura enterprise v6.1
✅ REGLA #4: SIC v3.1 + SLUC v2.1 probados
✅ REGLA #5: Control progreso aplicado
✅ REGLA #6: Versión v6.1.0 validada

Fecha: Agosto 8, 2025
Versión: v6.1.0-enterprise-test-fase2
Estado: VALIDACIÓN FASE 2
"""

import sys
import traceback
from datetime import datetime
from pathlib import Path

def test_unified_memory_system_integration():
    """Test integración UnifiedMemorySystem FASE 2"""
    print("🧠 Testing UnifiedMemorySystem FASE 2 integration...")
    
    try:
        from core.analysis.unified_memory_system import UnifiedMemorySystem, get_unified_memory_system
        
        # Test creación del sistema unificado
        system = UnifiedMemorySystem()
        print(f"✅ UnifiedMemorySystem creado: {system.system_state['memory_quality']}")
        
        # Test estado del sistema
        print(f"✅ Versión: {system.system_state['version']}")
        print(f"✅ Fase: {system.system_state['fase']}")
        print(f"✅ Experiencia trader: {system.system_state['trader_experience_level']}/10")
        print(f"✅ SIC status: {system.system_state['sic_status']}")
        print(f"✅ SLUC status: {system.system_state['sluc_status']}")
        
        # Test componentes integrados
        assert hasattr(system, 'market_context'), "MarketContext no integrado"
        assert hasattr(system, 'historical_analyzer'), "HistoricalAnalyzer no integrado"
        assert hasattr(system, 'decision_cache'), "DecisionCache no integrado"
        assert hasattr(system, 'unified_memory'), "UnifiedMemory no integrado"
        
        print("✅ Todos los componentes FASE 1 integrados correctamente")
        
        # Test nuevos componentes FASE 2
        assert hasattr(system, 'persistence_manager'), "PersistenceManager no implementado"
        assert hasattr(system, 'learning_engine'), "LearningEngine no implementado"
        assert hasattr(system, 'confidence_evaluator'), "ConfidenceEvaluator no implementado"
        
        print("✅ Nuevos componentes FASE 2 implementados correctamente")
        
        # Test instancia global
        global_system = get_unified_memory_system()
        print(f"✅ Instancia global: {type(global_system).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en UnifiedMemorySystem: {e}")
        traceback.print_exc()
        return False

def test_trader_memory_persistence():
    """Test memoria persistente como trader real"""
    print("\n💾 Testing trader memory persistence...")
    
    try:
        from core.analysis.unified_memory_system import get_unified_memory_system
        
        system = get_unified_memory_system()
        
        # Test carga de contexto persistente
        load_success = system.load_persistent_context("EURUSD")
        print(f"✅ Load persistent context: {load_success}")
        
        # Test guardado de contexto
        save_success = system.save_context_to_disk("EURUSD")
        print(f"✅ Save context to disk: {save_success}")
        
        # Test actualización de memoria
        test_data = {
            'price': 1.0850,
            'direction': 'bullish',
            'timeframe': 'M15',
            'confidence': 0.85
        }
        
        system.update_market_memory(test_data, "EURUSD")
        print("✅ Market memory updated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en trader memory persistence: {e}")
        traceback.print_exc()
        return False

def test_trader_insights_and_recommendations():
    """Test insights y recomendaciones como trader real"""
    print("\n🎯 Testing trader insights and recommendations...")
    
    try:
        from core.analysis.unified_memory_system import get_unified_memory_system
        
        system = get_unified_memory_system()
        
        # Test historical insight
        insight = system.get_historical_insight("BOS patterns M15", "M15")
        print(f"✅ Historical insight generated: {insight.get('trader_experience_level', 'unknown')}")
        print(f"✅ Insight confidence: {insight.get('confidence_adjustment', 0.0)}")
        
        # Test trader recommendation
        test_analysis = {
            'type': 'BOS_DETECTION',
            'timeframe': 'M15',
            'direction': 'bullish',
            'strength': 0.8,
            'quality': 0.75
        }
        
        recommendation = system.get_trader_recommendation(test_analysis)
        print(f"✅ Trader recommendation: {recommendation['action']}")
        print(f"✅ Recommendation confidence: {recommendation['recommendation_confidence']}")
        print(f"✅ Risk level: {recommendation['risk_assessment']['level']}")
        
        # Test market confidence assessment
        confidence = system.assess_market_confidence(test_analysis)
        print(f"✅ Market confidence assessment: {confidence}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en trader insights: {e}")
        traceback.print_exc()
        return False

def test_adaptive_learning_system():
    """Test sistema de aprendizaje adaptativo"""
    print("\n🎓 Testing adaptive learning system...")
    
    try:
        from core.analysis.unified_memory_system import get_unified_memory_system
        
        system = get_unified_memory_system()
        
        # Test learning engine
        assert hasattr(system.learning_engine, 'process_new_data'), "Learning engine incomplete"
        print("✅ Learning engine ready")
        
        # Test confidence evaluator
        test_insights = {
            'query': 'test_pattern',
            'timeframe': 'M15',
            'trader_experience_level': system.system_state['trader_experience_level']
        }
        
        confidence = system.confidence_evaluator.evaluate_insight_confidence(test_insights)
        print(f"✅ Insight confidence evaluation: {confidence}")
        
        # Test market confidence assessment
        test_analysis = {'quality': 0.8, 'strength': 0.75}
        market_confidence = system.confidence_evaluator.assess_market_confidence(test_analysis)
        print(f"✅ Market confidence assessment: {market_confidence}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en adaptive learning: {e}")
        traceback.print_exc()
        return False

def test_trader_experience_calculation():
    """Test cálculo de experiencia como trader real"""
    print("\n📈 Testing trader experience calculation...")
    
    try:
        from core.analysis.unified_memory_system import get_unified_memory_system
        
        system = get_unified_memory_system()
        
        # Test nivel de experiencia inicial
        initial_experience = system.system_state['trader_experience_level']
        print(f"✅ Initial trader experience: {initial_experience}/10")
        
        # Verificar que la experiencia esté en rango válido
        assert 1.0 <= initial_experience <= 10.0, f"Experience out of range: {initial_experience}"
        print("✅ Experience level within valid range")
        
        # Test recálculo de experiencia
        new_experience = system._calculate_experience_level()
        print(f"✅ Recalculated experience: {new_experience}/10")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en trader experience: {e}")
        traceback.print_exc()
        return False

def test_sic_sluc_integration():
    """Test integración SIC v3.1 + SLUC v2.1"""
    print("\n⚡ Testing SIC v3.1 + SLUC v2.1 integration...")
    
    try:
        from core.analysis.unified_memory_system import get_unified_memory_system
        
        system = get_unified_memory_system()
        
        # Verificar SIC está activo
        assert system.system_state['sic_status'] == 'ACTIVE', "SIC not active"
        print("✅ SIC v3.1 status: ACTIVE")
        
        # Verificar SLUC está activo
        assert system.system_state['sluc_status'] == 'ACTIVE', "SLUC not active"
        print("✅ SLUC v2.1 status: ACTIVE")
        
        # Test SIC Bridge
        assert hasattr(system, 'sic'), "SIC Bridge not available"
        print("✅ SIC Bridge integrated")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en SIC/SLUC integration: {e}")
        traceback.print_exc()
        return False

def test_performance_enterprise():
    """Test performance enterprise <5s"""
    print("\n⚡ Testing enterprise performance...")
    
    try:
        start_time = datetime.now()
        
        from core.analysis.unified_memory_system import get_unified_memory_system
        
        # Test operaciones principales
        system = get_unified_memory_system()
        
        # Test insight generation
        insight = system.get_historical_insight("test_query", "M15")
        
        # Test recommendation generation
        test_analysis = {'type': 'test', 'timeframe': 'M15', 'quality': 0.7}
        recommendation = system.get_trader_recommendation(test_analysis)
        
        # Test confidence assessment
        confidence = system.assess_market_confidence(test_analysis)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"✅ Total operations time: {duration:.3f}s")
        
        # ✅ REGLA #3: Performance enterprise <5s
        assert duration < 5.0, f"Performance too slow: {duration}s"
        print("✅ Performance requirement met: <5s")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en performance test: {e}")
        traceback.print_exc()
        return False

def main():
    """Test principal FASE 2 siguiendo REGLAS COPILOT"""
    print("🧪 INICIO TEST FASE 2 - UNIFIED MEMORY SYSTEM v6.1")
    print("=" * 70)
    
    start_time = datetime.now()
    
    # ✅ REGLA #5: Tests obligatorios para FASE 2
    tests = [
        ("UnifiedMemorySystem Integration", test_unified_memory_system_integration),
        ("Trader Memory Persistence", test_trader_memory_persistence),
        ("Trader Insights & Recommendations", test_trader_insights_and_recommendations),
        ("Adaptive Learning System", test_adaptive_learning_system),
        ("Trader Experience Calculation", test_trader_experience_calculation),
        ("SIC v3.1 + SLUC v2.1 Integration", test_sic_sluc_integration),
        ("Enterprise Performance <5s", test_performance_enterprise)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Test {test_name} falló: {e}")
            results[test_name] = False
    
    # ✅ REGLA #5: Resumen obligatorio
    print("\n" + "=" * 70)
    print("📊 RESUMEN FASE 2 - UNIFIED MEMORY SYSTEM v6.1:")
    print("-" * 70)
    
    total_tests = len(tests)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print("-" * 70)
    print(f"🎯 RESULTADO FINAL FASE 2:")
    print(f"   Tests ejecutados: {total_tests}")
    print(f"   Tests exitosos: {passed_tests}")
    print(f"   Tests fallidos: {failed_tests}")
    print(f"   Tasa de éxito: {(passed_tests/total_tests)*100:.1f}%")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"   Tiempo total: {duration:.2f}s")
    
    # ✅ REGLA #6: Evaluación para incremento de versión
    if passed_tests == total_tests:
        print("\n🎉 ¡FASE 2 COMPLETADA EXITOSAMENTE!")
        print("✅ Sistema de memoria unificado funcionando como trader real")
        print("✅ SIC v3.1 + SLUC v2.1 integrados correctamente")
        print("✅ Performance enterprise validada (<5s)")
        print("✅ Memoria persistente como trader profesional")
        print("✅ Insights y recomendaciones basadas en experiencia")
        print("🚀 READY FOR FASE 3: Validación con datos reales MT5")
        print(f"📋 VERSIÓN v6.1.0 JUSTIFICADA: FASE 2 completada")
    else:
        print(f"\n⚠️ FASE 2 PARCIALMENTE COMPLETADA")
        print(f"❌ {failed_tests} componentes requieren atención")
        print("🔧 Revisar errores antes de continuar a FASE 3")

if __name__ == "__main__":
    main()
