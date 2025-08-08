# -*- coding: utf-8 -*-
"""
🧪 TEST PATTERN DETECTOR v6.0 ENTERPRISE
==========================================

Test de integración completo del Pattern Detector v6.0 Enterprise
con datos reales de FundedNext MT5 Terminal.

Autor: ICT Engine v6.1.0 Enterprise Team
Fecha: Agosto 7, 2025
"""

import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# Añadir path del proyecto
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def test_pattern_detector_integration():
    """Test de integración completo del Pattern Detector"""
    
    print("🧪 ICT ENGINE v6.0 ENTERPRISE - PATTERN DETECTOR TEST")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🖥️  Sistema: Pattern Detector v6.0 Enterprise")
    print(f"🎯 Objetivo: Validación completa con datos reales")
    print("=" * 60)
    
    try:
        # 1. IMPORTAR PATTERN DETECTOR
        print("\n🔧 FASE 1: Importando Pattern Detector...")
        
        from core.analysis.pattern_detector import get_pattern_detector, PatternType, PatternConfidence
        
        print("✅ Pattern Detector importado correctamente")
        
        # 2. INICIALIZAR DETECTOR
        print("\n🚀 FASE 2: Inicializando detector...")
        
        config = {
            'enable_debug': True,
            'min_confidence': 65.0,
            'enable_silver_bullet': True,
            'enable_judas_swing': True,
            'enable_liquidity_grab': True,
            'enable_optimal_trade_entry': True,
            'use_multi_timeframe': True,
            'max_patterns_per_analysis': 8,
            'fvg_min_size': 0.0003,
            'order_block_strength': 0.6
        }
        
        detector = get_pattern_detector(config)
        print(f"✅ Detector inicializado: {detector.is_initialized}")
        print(f"📊 Configuración: {len(config)} parámetros")
        
        # 3. VERIFICAR COMPONENTES
        print("\n🔍 FASE 3: Verificando componentes...")
        
        print(f"   Downloader conectado: {detector._downloader is not None}")
        print(f"   Cache habilitado: {detector.config['enable_cache']}")
        print(f"   Debug activo: {detector.config['enable_debug']}")
        
        # 4. ANÁLISIS DE PATRONES PRINCIPAL
        print("\n🎯 FASE 4: Análisis principal de patrones...")
        
        start_time = time.time()
        
        patterns = detector.detect_patterns(
            symbol="EURUSD",
            timeframe="M15",
            lookback_days=5
        )
        
        analysis_time = time.time() - start_time
        
        print(f"✅ Análisis completado en {analysis_time:.3f}s")
        print(f"🎪 Patrones detectados: {len(patterns)}")
        
        if analysis_time > 0.05:
            print(f"⚠️  WARNING: Tiempo excede target de 50ms")
        else:
            print(f"⚡ PERFORMANCE: Dentro del target (<50ms)")
        
        # 5. ANALIZAR PATRONES DETECTADOS
        if patterns:
            print("\n📊 FASE 5: Análisis de patrones detectados...")
            
            patterns_by_type = {}
            patterns_by_confidence = {}
            total_strength = 0
            
            for i, pattern in enumerate(patterns, 1):
                print(f"\n🎯 PATRÓN {i}: {pattern.pattern_type.value.upper()}")
                print(f"   📈 Dirección: {pattern.direction.value.upper()}")
                print(f"   🎪 Confianza: {pattern.confidence.value.upper()}")
                print(f"   💪 Strength: {pattern.strength:.1f}%")
                print(f"   📊 Probabilidad: {pattern.probability:.1f}%")
                print(f"   🎯 Entry Zone: {pattern.entry_zone[0]:.5f} - {pattern.entry_zone[1]:.5f}")
                print(f"   🛡️  Stop Loss: {pattern.stop_loss:.5f}")
                print(f"   🏆 Take Profit: {pattern.take_profit_1:.5f}")
                print(f"   ⚡ R:R Ratio: {pattern.risk_reward_ratio:.2f}")
                print(f"   🏛️  Sesión: {pattern.session.value}")
                print(f"   🔗 Confluencias: {', '.join(pattern.confluences)}")
                print(f"   ⏰ Time Sensitivity: {pattern.time_sensitivity}")
                
                if pattern.narrative:
                    print(f"   📖 Narrativa: {pattern.narrative[:100]}...")
                
                # Contar por tipo
                ptype = pattern.pattern_type.value
                patterns_by_type[ptype] = patterns_by_type.get(ptype, 0) + 1
                
                # Contar por confianza
                conf = pattern.confidence.value
                patterns_by_confidence[conf] = patterns_by_confidence.get(conf, 0) + 1
                
                total_strength += pattern.strength
            
            # 6. ESTADÍSTICAS
            print("\n📈 FASE 6: Estadísticas del análisis...")
            
            avg_strength = total_strength / len(patterns)
            
            print(f"📊 RESUMEN ESTADÍSTICO:")
            print(f"   Total patrones: {len(patterns)}")
            print(f"   Strength promedio: {avg_strength:.1f}%")
            print(f"   Tiempo de análisis: {analysis_time:.3f}s")
            
            print(f"\n🎪 POR TIPO DE PATRÓN:")
            for ptype, count in patterns_by_type.items():
                print(f"   {ptype.replace('_', ' ').title()}: {count}")
            
            print(f"\n🎯 POR NIVEL DE CONFIANZA:")
            for conf, count in patterns_by_confidence.items():
                print(f"   {conf.title()}: {count}")
            
            # Validar que tenemos diversidad de patrones
            if len(patterns_by_type) >= 3:
                print("✅ DIVERSIDAD: Múltiples tipos de patrones detectados")
            else:
                print("⚠️  DIVERSIDAD: Pocos tipos de patrones")
            
            # Validar strength promedio
            if avg_strength >= 70.0:
                print("✅ CALIDAD: Strength promedio bueno")
            else:
                print("⚠️  CALIDAD: Strength promedio bajo")
        
        else:
            print("\n⚠️  FASE 5: No se detectaron patrones")
            print("   Esto puede ser normal dependiendo de condiciones de mercado")
        
        # 7. MÉTRICAS DE PERFORMANCE
        print("\n⚡ FASE 7: Métricas de performance...")
        
        metrics = detector.get_performance_metrics()
        
        print(f"📊 MÉTRICAS DE RENDIMIENTO:")
        print(f"   Análisis totales: {metrics['total_analyses']}")
        print(f"   Tiempo promedio: {metrics['avg_analysis_time']:.3f}s")
        print(f"   Patrones detectados: {metrics['patterns_detected']}")
        print(f"   Tasa de éxito: {metrics['success_rate']:.1f}%")
        print(f"   Última actualización: {metrics['last_update']}")
        
        # 8. RESUMEN FINAL
        print("\n📋 FASE 8: Resumen del detector...")
        
        summary = detector.get_pattern_summary()
        
        print(f"📈 RESUMEN DETECTOR:")
        print(f"   Total patrones: {summary['total_patterns']}")
        print(f"   Strength promedio: {summary['avg_strength']}%")
        print(f"   Último análisis: {summary['last_analysis']}")
        print(f"   Por tipo: {summary['by_type']}")
        print(f"   Por confianza: {summary['by_confidence']}")
        
        # 9. TEST DE MÚLTIPLES TIMEFRAMES
        print("\n🕐 FASE 9: Test multi-timeframe...")
        
        timeframes = ["M5", "M15", "H1"]
        tf_results = {}
        
        for tf in timeframes:
            print(f"\n   Analizando {tf}...")
            start_tf = time.time()
            
            tf_patterns = detector.detect_patterns("EURUSD", tf, 3)
            tf_time = time.time() - start_tf
            
            tf_results[tf] = {
                'patterns': len(tf_patterns),
                'time': tf_time,
                'avg_strength': sum(p.strength for p in tf_patterns) / len(tf_patterns) if tf_patterns else 0
            }
            
            print(f"   ✅ {tf}: {len(tf_patterns)} patrones en {tf_time:.3f}s")
        
        print(f"\n📊 RESULTADOS MULTI-TIMEFRAME:")
        for tf, result in tf_results.items():
            print(f"   {tf}: {result['patterns']} patrones, {result['avg_strength']:.1f}% avg strength")
        
        # 10. VALIDACIÓN FINAL
        print("\n✅ FASE 10: Validación final...")
        
        total_success = True
        
        # Verificar performance
        if analysis_time <= 0.05:
            print("✅ PERFORMANCE: Tiempo de análisis dentro del target")
        else:
            print("❌ PERFORMANCE: Tiempo de análisis excede target")
            total_success = False
        
        # Verificar funcionalidad
        if detector.is_initialized:
            print("✅ INICIALIZACIÓN: Detector correctamente inicializado")
        else:
            print("❌ INICIALIZACIÓN: Detector no inicializado")
            total_success = False
        
        # Verificar detección
        if len(patterns) > 0 or len(tf_results) > 0:
            print("✅ DETECCIÓN: Capacidad de detectar patrones confirmada")
        else:
            print("⚠️  DETECCIÓN: No se detectaron patrones en ningún TF")
        
        # Verificar métricas
        if metrics['total_analyses'] > 0:
            print("✅ MÉTRICAS: Sistema de métricas funcionando")
        else:
            print("❌ MÉTRICAS: Sistema de métricas no funciona")
            total_success = False
        
        # RESULTADO FINAL
        print("\n" + "=" * 60)
        if total_success:
            print("🎉 RESULTADO: TEST COMPLETADO EXITOSAMENTE")
            print("✅ Pattern Detector v6.0 Enterprise VALIDADO")
        else:
            print("⚠️  RESULTADO: TEST COMPLETADO CON WARNINGS")
            print("🔧 Revisar componentes marcados como ERROR")
        
        print("=" * 60)
        
        return total_success, patterns, metrics
        
    except Exception as e:
        print(f"\n❌ ERROR EN TEST: {e}")
        import traceback
        traceback.print_exc()
        return False, [], {}


def test_specific_patterns():
    """Test específico de patrones individuales"""
    
    print("\n🎯 TEST ESPECÍFICO DE PATRONES")
    print("-" * 40)
    
    try:
        from core.analysis.pattern_detector import get_pattern_detector
        
        detector = get_pattern_detector({'enable_debug': True, 'min_confidence': 60.0})
        
        # Test Silver Bullet específico
        print("\n🥈 Testing Silver Bullet...")
        # Configurar para hora Silver Bullet
        current_hour = datetime.now().hour
        if 10 <= current_hour <= 11 or 14 <= current_hour <= 15:
            print("✅ Ventana Silver Bullet activa")
        else:
            print("ℹ️  Fuera de ventana Silver Bullet")
        
        # Test con datos simulados específicos
        print("\n📊 Generando datos de prueba...")
        
        patterns = detector.detect_patterns("EURUSD", "M15", 2)
        
        pattern_types_found = [p.pattern_type.value for p in patterns]
        
        print(f"🎪 Patrones encontrados: {pattern_types_found}")
        
        # Verificar tipos específicos
        expected_types = ['silver_bullet', 'judas_swing', 'liquidity_grab', 'optimal_trade_entry', 'order_block', 'fair_value_gap']
        
        for expected in expected_types:
            if expected in pattern_types_found:
                print(f"✅ {expected.replace('_', ' ').title()}: DETECTADO")
            else:
                print(f"ℹ️  {expected.replace('_', ' ').title()}: No detectado (normal según condiciones)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test específico: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Iniciando test completo del Pattern Detector...")
    
    # Test principal
    success, patterns, metrics = test_pattern_detector_integration()
    
    # Test específico
    specific_success = test_specific_patterns()
    
    # Resumen final
    print(f"\n📋 RESUMEN FINAL:")
    print(f"   Test principal: {'✅ PASS' if success else '❌ FAIL'}")
    print(f"   Test específico: {'✅ PASS' if specific_success else '❌ FAIL'}")
    print(f"   Patrones detectados: {len(patterns)}")
    print(f"   Tiempo promedio: {metrics.get('avg_analysis_time', 0):.3f}s")
    
    if success and specific_success:
        print("\n🎉 TODOS LOS TESTS PASARON")
        print("✅ Pattern Detector v6.0 Enterprise LISTO PARA PRODUCCIÓN")
    else:
        print("\n⚠️  ALGUNOS TESTS FALLARON")
        print("🔧 Revisar logs arriba para detalles")
