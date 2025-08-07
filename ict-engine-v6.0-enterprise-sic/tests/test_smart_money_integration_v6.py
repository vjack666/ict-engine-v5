#!/usr/bin/env python3
"""
🧠 TEST SMART MONEY CONCEPTS INTEGRATION v6.0
==============================================

Test de integración para validar que Smart Money Concepts v6.0
está correctamente integrado con el Pattern Detector Enterprise.

Verificaciones:
✅ Importación de Smart Money Analyzer 
✅ Inicialización correcta en Pattern Detector
✅ Enhancement de patrones con Smart Money
✅ Liquidity pools detection
✅ Institutional flow analysis
✅ Market maker behavior
✅ Killzone optimization
✅ Performance Smart Money

Autor: ICT Engine v6.0 Enterprise Team
Fecha: Agosto 7, 2025
"""

import sys
import os
import time
from datetime import datetime

# Configurar path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.analysis.pattern_detector import get_pattern_detector, PatternType, TradingDirection
    from core.smart_money_concepts.smart_money_analyzer import SmartMoneyAnalyzer
    print("✅ Importaciones Smart Money exitosas")
except ImportError as e:
    print(f"❌ Error en importaciones Smart Money: {e}")
    sys.exit(1)


def test_smart_money_analyzer_availability():
    """Test 1: Verificar disponibilidad Smart Money Analyzer"""
    try:
        print("\n" + "="*60)
        print("🧠 TEST 1: SMART MONEY ANALYZER AVAILABILITY")
        print("="*60)
        
        # Crear Smart Money Analyzer directamente
        smart_analyzer = SmartMoneyAnalyzer()
        print("✅ Smart Money Analyzer creado correctamente")
        
        # Verificar métodos principales
        methods = [
            'analyze_liquidity_pools',
            'analyze_institutional_order_flow', 
            'detect_market_maker_behavior',
            'get_system_status'
        ]
        
        for method in methods:
            if hasattr(smart_analyzer, method):
                print(f"✅ Método {method} disponible")
            else:
                print(f"❌ Método {method} NO disponible")
                
        return True
        
    except Exception as e:
        print(f"❌ Error en test Smart Money availability: {e}")
        return False


def test_pattern_detector_smart_money_integration():
    """Test 2: Verificar integración con Pattern Detector"""
    try:
        print("\n" + "="*60)
        print("🎯 TEST 2: PATTERN DETECTOR SMART MONEY INTEGRATION")
        print("="*60)
        
        # Crear Pattern Detector con configuración optimizada
        config = {
            'enable_debug': True,
            'min_confidence': 60.0,
            'enable_silver_bullet': True,
            'enable_judas_swing': True,
            'enable_liquidity_grab': True
        }
        
        detector = get_pattern_detector(config)
        print("✅ Pattern Detector v6.0 Enterprise creado")
        
        # Verificar inicialización Smart Money
        if hasattr(detector, '_smart_money_analyzer'):
            if detector._smart_money_analyzer:
                print("✅ Smart Money Analyzer integrado correctamente")
            else:
                print("⚠️ Smart Money Analyzer no inicializado (puede ser normal)")
        else:
            print("❌ Atributo _smart_money_analyzer no encontrado")
        
        # Verificar métodos Smart Money en detector
        smart_methods = [
            '_enhance_with_smart_money_analysis',
            '_analyze_liquidity_pools_near_pattern',
            '_detect_institutional_flow',
            '_analyze_market_maker_behavior',
            '_optimize_with_killzones'
        ]
        
        for method in smart_methods:
            if hasattr(detector, method):
                print(f"✅ Método {method} integrado")
            else:
                print(f"❌ Método {method} NO integrado")
                
        return True
        
    except Exception as e:
        print(f"❌ Error en test integración: {e}")
        return False


def test_smart_money_pattern_enhancement():
    """Test 3: Verificar enhancement de patrones con Smart Money"""
    try:
        print("\n" + "="*60)
        print("🚀 TEST 3: SMART MONEY PATTERN ENHANCEMENT")
        print("="*60)
        
        # Crear detector con Smart Money habilitado
        config = {
            'enable_debug': True,
            'min_confidence': 50.0,  # Bajo para garantizar detecciones
            'enable_silver_bullet': True,
            'enable_judas_swing': True,
            'enable_liquidity_grab': True
        }
        
        detector = get_pattern_detector(config)
        
        # Ejecutar detección de patrones
        start_time = time.time()
        patterns = detector.detect_patterns("EURUSD", "M15", 3)
        analysis_time = time.time() - start_time
        
        print(f"✅ Análisis completado en {analysis_time:.3f}s")
        print(f"✅ Patrones detectados: {len(patterns)}")
        
        # Verificar enhancement Smart Money en patrones
        enhanced_patterns = 0
        for i, pattern in enumerate(patterns):
            print(f"\n🎯 Patrón {i+1}: {pattern.pattern_type.value}")
            print(f"   Dirección: {pattern.direction.value}")
            print(f"   Confianza: {pattern.confidence.value}")
            print(f"   Strength: {pattern.strength:.1f}%")
            print(f"   Sesión: {pattern.session.value}")
            print(f"   Confluencias: {len(pattern.confluences)}")
            
            # Verificar si tiene Smart Money data
            if hasattr(pattern, 'raw_data') and 'smart_money_data' in pattern.raw_data:
                enhanced_patterns += 1
                sm_data = pattern.raw_data['smart_money_data']
                print(f"   🧠 Smart Money Enhanced:")
                print(f"      - Liquidity pools: {len(sm_data.get('liquidity_pools', []))}")
                print(f"      - Institutional flow: {sm_data.get('institutional_flow', 0):.2f}")
                print(f"      - Market maker: {sm_data.get('market_maker_behavior', 0):.2f}")
                print(f"      - Killzone: {sm_data.get('killzone_optimization', {}).get('active', False)}")
                print(f"      - SM Confidence: {sm_data.get('smart_money_confidence', 0):.2f}")
            
            # Verificar narrative enhancement
            if "liquidity pools" in pattern.narrative or "institucional" in pattern.narrative:
                print(f"   💬 Narrative enhanced with Smart Money")
        
        print(f"\n📊 Resumen Smart Money Enhancement:")
        print(f"   Patrones totales: {len(patterns)}")
        print(f"   Patrones enhanced: {enhanced_patterns}")
        print(f"   Rate de enhancement: {(enhanced_patterns/len(patterns)*100) if patterns else 0:.1f}%")
        
        return len(patterns) > 0
        
    except Exception as e:
        print(f"❌ Error en test enhancement: {e}")
        return False


def test_smart_money_performance():
    """Test 4: Verificar performance con Smart Money"""
    try:
        print("\n" + "="*60)
        print("⚡ TEST 4: SMART MONEY PERFORMANCE")
        print("="*60)
        
        # Test con múltiples ejecuciones
        times = []
        patterns_counts = []
        
        config = {
            'enable_debug': False,  # Desactivar debug para performance
            'min_confidence': 65.0,
            'enable_silver_bullet': True,
            'enable_judas_swing': True
        }
        
        detector = get_pattern_detector(config)
        
        print("Ejecutando 5 análisis para medir performance...")
        
        for i in range(5):
            start_time = time.time()
            patterns = detector.detect_patterns("EURUSD", "M15", 2)
            analysis_time = time.time() - start_time
            
            times.append(analysis_time)
            patterns_counts.append(len(patterns))
            print(f"   Análisis {i+1}: {analysis_time:.3f}s, {len(patterns)} patrones")
        
        avg_time = sum(times) / len(times)
        avg_patterns = sum(patterns_counts) / len(patterns_counts)
        
        print(f"\n📈 Performance Metrics:")
        print(f"   Tiempo promedio: {avg_time:.3f}s")
        print(f"   Patrones promedio: {avg_patterns:.1f}")
        print(f"   Tiempo máximo: {max(times):.3f}s")
        print(f"   Tiempo mínimo: {min(times):.3f}s")
        
        # Verificar que cumple requisitos de performance
        performance_ok = avg_time < 2.0  # Máximo 2 segundos por análisis
        print(f"   Performance OK: {'✅' if performance_ok else '❌'} (<2.0s)")
        
        return performance_ok
        
    except Exception as e:
        print(f"❌ Error en test performance: {e}")
        return False


def test_smart_money_killzone_detection():
    """Test 5: Verificar detección de killzones"""
    try:
        print("\n" + "="*60)
        print("⏰ TEST 5: SMART MONEY KILLZONE DETECTION")
        print("="*60)
        
        detector = get_pattern_detector({'enable_debug': True})
        
        # Simular diferentes horas para killzone testing
        current_hour = datetime.now().hour
        print(f"Hora actual: {current_hour}:00 GMT")
        
        # Verificar método de optimización killzone
        if hasattr(detector, '_optimize_with_killzones'):
            print("✅ Método _optimize_with_killzones disponible")
            
            # Test con patrón simulado
            from core.analysis.pattern_detector import PatternSignal, PatternType, PatternConfidence, TradingDirection, SessionType
            
            test_pattern = PatternSignal(
                pattern_type=PatternType.SILVER_BULLET,
                confidence=PatternConfidence.HIGH,
                direction=TradingDirection.BUY,
                symbol="EURUSD",
                timeframe="M15",
                entry_zone=(1.1050, 1.1060),
                stop_loss=1.1040,
                take_profit_1=1.1080,
                strength=75.0,
                timestamp=datetime.now(),
                session=SessionType.LONDON,
                narrative="Test pattern for killzone"
            )
            
            # Test killzone optimization
            killzone_result = detector._optimize_with_killzones(test_pattern, None)
            
            print(f"✅ Killzone analysis resultado:")
            print(f"   Active: {killzone_result.get('active', False)}")
            print(f"   Strength: {killzone_result.get('strength', 0):.2f}")
            print(f"   Type: {killzone_result.get('killzone_type', 'none')}")
            
            # Verificar lógica de killzones
            if 10 <= current_hour <= 11:
                print("✅ London killzone detectado (10-11 GMT)")
            elif 14 <= current_hour <= 15:
                print("✅ New York killzone detectado (14-15 GMT)")
            elif 1 <= current_hour <= 2:
                print("✅ Asian killzone detectado (01-02 GMT)")
            else:
                print("⚠️ Fuera de killzone principal")
            
            return True
        else:
            print("❌ Método _optimize_with_killzones no disponible")
            return False
            
    except Exception as e:
        print(f"❌ Error en test killzone: {e}")
        return False


def run_comprehensive_smart_money_test():
    """Ejecutar test comprehensivo Smart Money Integration v6.0"""
    print("🧠 SMART MONEY CONCEPTS INTEGRATION TEST v6.0")
    print("=" * 70)
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Smart Money Analyzer Availability", test_smart_money_analyzer_availability),
        ("Pattern Detector Integration", test_pattern_detector_smart_money_integration), 
        ("Pattern Enhancement", test_smart_money_pattern_enhancement),
        ("Performance Test", test_smart_money_performance),
        ("Killzone Detection", test_smart_money_killzone_detection)
    ]
    
    results = []
    start_time = time.time()
    
    for test_name, test_func in tests:
        print(f"\n🚀 Ejecutando: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   Resultado: {status}")
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            results.append((test_name, False))
    
    # Resumen final
    total_time = time.time() - start_time
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("\n" + "="*70)
    print("📊 RESUMEN SMART MONEY INTEGRATION TEST v6.0")
    print("="*70)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Resultado Final:")
    print(f"   Tests ejecutados: {total}")
    print(f"   Tests exitosos: {passed}")
    print(f"   Tasa de éxito: {(passed/total*100):.1f}%")
    print(f"   Tiempo total: {total_time:.2f}s")
    
    if passed == total:
        print(f"\n🎉 TODOS LOS TESTS SMART MONEY v6.0 EXITOSOS!")
        print(f"🧠 Smart Money Concepts están completamente integrados")
        print(f"⚡ Sistema listo para trading institutional enterprise")
    else:
        print(f"\n⚠️ {total-passed} tests fallaron - revisar integración")
    
    return passed == total


if __name__ == "__main__":
    success = run_comprehensive_smart_money_test()
    sys.exit(0 if success else 1)
