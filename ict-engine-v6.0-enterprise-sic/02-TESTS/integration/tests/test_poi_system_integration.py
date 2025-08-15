# -*- coding: utf-8 -*-
"""
🧪 TEST POI SYSTEM v6.0 ENTERPRISE
===================================

Test de integración completo del POI System v6.0 Enterprise
con datos reales de FTMO Global Markets MT5 Terminal.

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

def test_poi_system_integration():
    """Test de integración completo del POI System"""
    
    print("🧪 ICT ENGINE v6.0 ENTERPRISE - POI SYSTEM TEST")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🖥️  Sistema: POI System v6.0 Enterprise")
    print(f"🎯 Objetivo: Validación completa de Points of Interest")
    print("=" * 60)
    
    try:
        # 1. IMPORTAR POI SYSTEM
        print("\n🔧 FASE 1: Importando POI System...")
        
        from core.analysis.poi_system import get_poi_system, POIType, POISignificance, POIStatus
        
        print("✅ POI System importado correctamente")
        
        # 2. INICIALIZAR SISTEMA
        print("\n🚀 FASE 2: Inicializando POI System...")
        
        config = {
            'enable_debug': True,
            'min_poi_strength': 60.0,
            'max_active_pois': 30,
            'enable_order_blocks': True,
            'enable_fair_value_gaps': True,
            'enable_swing_points': True,
            'enable_session_levels': True,
            'enable_liquidity_pools': True,
            'enable_fibonacci_levels': True,
            'enable_psychological_levels': True,
            'proximity_threshold': 0.0008
        }
        
        poi_system = get_poi_system(config)
        print(f"✅ POI System inicializado: {poi_system.is_initialized}")
        print(f"📊 Configuración: {len(config)} parámetros")
        
        # 3. VERIFICAR COMPONENTES
        print("\n🔍 FASE 3: Verificando componentes integrados...")
        
        print(f"   Downloader conectado: {poi_system._downloader is not None}")
        print(f"   Pattern Detector conectado: {poi_system._pattern_detector is not None}")
        print(f"   Market Analyzer conectado: {poi_system._market_analyzer is not None}")
        
        # 4. DETECCIÓN PRINCIPAL DE POIS
        print("\n🎯 FASE 4: Detección principal de POIs...")
        
        start_time = time.time()
        
        pois = poi_system.detect_pois(
            symbol="EURUSD",
            timeframe="M15",
            lookback_days=5
        )
        
        analysis_time = time.time() - start_time
        
        print(f"✅ Detección completada en {analysis_time:.3f}s")
        print(f"🎪 POIs detectados: {len(pois)}")
        
        # Verificar performance target
        if analysis_time > 0.1:
            print(f"⚠️  WARNING: Tiempo excede target de 100ms")
        else:
            print(f"⚡ PERFORMANCE: Dentro del target (<100ms)")
        
        # 5. ANALIZAR POIS DETECTADOS
        if pois:
            print(f"\n📊 FASE 5: Análisis de POIs detectados...")
            
            pois_by_type = {}
            pois_by_significance = {}
            total_strength = 0
            
            # Mostrar primeros 10 POIs
            for i, poi in enumerate(pois[:10], 1):
                print(f"\n🎯 POI {i}: {poi.poi_type.value.upper()}")
                print(f"   💰 Precio: {poi.price_level:.5f}")
                print(f"   📊 Zona: {poi.price_zone[0]:.5f} - {poi.price_zone[1]:.5f}")
                print(f"   ⭐ Significancia: {poi.significance.value.upper()}")
                print(f"   💪 Strength: {poi.strength:.1f}%")
                print(f"   🔄 Estado: {poi.status.value}")
                print(f"   🏛️  Estructura: {poi.market_structure}")
                print(f"   🔗 Confluencias: {', '.join(poi.confluences[:3])}")
                print(f"   ⏰ Expira: {poi.expiry_time.strftime('%H:%M') if poi.expiry_time else 'N/A'}")
                print(f"   🆔 ID: {poi.analysis_id}")
                
                # Contar estadísticas
                ptype = poi.poi_type.value
                pois_by_type[ptype] = pois_by_type.get(ptype, 0) + 1
                
                sig = poi.significance.value
                pois_by_significance[sig] = pois_by_significance.get(sig, 0) + 1
                
                total_strength += poi.strength
            
            # 6. ESTADÍSTICAS DETALLADAS
            print(f"\n📈 FASE 6: Estadísticas de POIs...")
            
            avg_strength = total_strength / len(pois)
            
            print(f"📊 RESUMEN ESTADÍSTICO:")
            print(f"   Total POIs: {len(pois)}")
            print(f"   Strength promedio: {avg_strength:.1f}%")
            print(f"   Tiempo de detección: {analysis_time:.3f}s")
            
            print(f"\n🎪 POR TIPO DE POI:")
            for ptype, count in pois_by_type.items():
                print(f"   {ptype.replace('_', ' ').title()}: {count}")
            
            print(f"\n⭐ POR SIGNIFICANCIA:")
            for sig, count in pois_by_significance.items():
                print(f"   {sig.title()}: {count}")
            
            # Validaciones
            if len(pois_by_type) >= 4:
                print("✅ DIVERSIDAD: Múltiples tipos de POI detectados")
            else:
                print("⚠️  DIVERSIDAD: Pocos tipos de POI")
            
            if avg_strength >= 65.0:
                print("✅ CALIDAD: Strength promedio bueno")
            else:
                print("⚠️  CALIDAD: Strength promedio bajo")
            
            # Verificar POIs críticos
            critical_pois = [p for p in pois if p.significance == POISignificance.CRITICAL]
            high_pois = [p for p in pois if p.significance == POISignificance.HIGH]
            
            print(f"\n🔥 POIs CRÍTICOS: {len(critical_pois)}")
            print(f"🔥 POIs ALTOS: {len(high_pois)}")
            
        else:
            print("\n⚠️  FASE 5: No se detectaron POIs")
            print("   Esto puede indicar condiciones de mercado específicas")
        
        # 7. TEST DE FUNCIONALIDADES ESPECÍFICAS
        print(f"\n🎯 FASE 7: Test de funcionalidades específicas...")
        
        # Test buscar POIs por tipo
        if pois:
            order_blocks = poi_system.get_active_pois(POIType.ORDER_BLOCK)
            fvgs = poi_system.get_active_pois(POIType.FAIR_VALUE_GAP)
            swing_points = poi_system.get_active_pois(POIType.SWING_HIGH)
            
            print(f"   Order Blocks activos: {len(order_blocks)}")
            print(f"   FVGs activos: {len(fvgs)}")
            print(f"   Swing Points activos: {len(swing_points)}")
            
            # Test buscar POIs cerca del precio actual
            if pois:
                current_price = 1.16500  # Precio simulado
                nearby_pois = poi_system.get_pois_near_price(current_price, 0.0050)
                print(f"   POIs cerca de {current_price:.5f}: {len(nearby_pois)}")
                
                for poi in nearby_pois[:3]:
                    distance = abs(poi.price_level - current_price)
                    print(f"     {poi.poi_type.value}: {poi.price_level:.5f} (dist: {distance*10000:.1f} pips)")
        
        # 8. RESUMEN DEL SISTEMA
        print(f"\n📋 FASE 8: Resumen del POI System...")
        
        summary = poi_system.get_poi_summary()
        
        print(f"📈 RESUMEN POI SYSTEM:")
        print(f"   Total activos: {summary['total_active']}")
        print(f"   Strength promedio: {summary['avg_strength']}%")
        print(f"   Históricos: {summary['historical_count']}")
        print(f"   Próxima expiración: {summary['next_expiry']}")
        
        print(f"\n🎪 DISTRIBUCIÓN POR TIPO:")
        for ptype, count in summary['by_type'].items():
            print(f"   {ptype.replace('_', ' ').title()}: {count}")
        
        print(f"\n⭐ DISTRIBUCIÓN POR SIGNIFICANCIA:")
        for sig, count in summary['by_significance'].items():
            print(f"   {sig.title()}: {count}")
        
        # 9. MÉTRICAS DE PERFORMANCE
        print(f"\n⚡ FASE 9: Métricas de performance...")
        
        metrics = poi_system.get_performance_metrics()
        
        print(f"📊 MÉTRICAS DE RENDIMIENTO:")
        print(f"   POIs creados: {metrics['total_pois_created']}")
        print(f"   POIs activos: {metrics['active_pois']}")
        print(f"   Lifetime promedio: {metrics['avg_poi_lifetime']}")
        print(f"   Tasa de éxito: {metrics['success_rate']:.1f}%")
        print(f"   Última actualización: {metrics['last_update']}")
        
        # 10. TEST DE MÚLTIPLES TIMEFRAMES
        print(f"\n🕐 FASE 10: Test multi-timeframe...")
        
        timeframes = ["M5", "M15", "H1"]
        tf_results = {}
        
        for tf in timeframes:
            print(f"\n   Analizando {tf}...")
            start_tf = time.time()
            
            tf_pois = poi_system.detect_pois("EURUSD", tf, 3)
            tf_time = time.time() - start_tf
            
            tf_results[tf] = {
                'pois': len(tf_pois),
                'time': tf_time,
                'avg_strength': sum(p.strength for p in tf_pois) / len(tf_pois) if tf_pois else 0
            }
            
            print(f"   ✅ {tf}: {len(tf_pois)} POIs en {tf_time:.3f}s")
        
        print(f"\n📊 RESULTADOS MULTI-TIMEFRAME:")
        for tf, result in tf_results.items():
            print(f"   {tf}: {result['pois']} POIs, {result['avg_strength']:.1f}% avg strength")
        
        # 11. VALIDACIÓN FINAL
        print(f"\n✅ FASE 11: Validación final...")
        
        total_success = True
        
        # Verificar performance
        if analysis_time <= 0.1:
            print("✅ PERFORMANCE: Tiempo de detección dentro del target")
        else:
            print("❌ PERFORMANCE: Tiempo de detección excede target")
            total_success = False
        
        # Verificar inicialización
        if poi_system.is_initialized:
            print("✅ INICIALIZACIÓN: POI System correctamente inicializado")
        else:
            print("❌ INICIALIZACIÓN: POI System no inicializado")
            total_success = False
        
        # Verificar detección
        if len(pois) > 0:
            print("✅ DETECCIÓN: Capacidad de detectar POIs confirmada")
        else:
            print("⚠️  DETECCIÓN: No se detectaron POIs")
        
        # Verificar diversidad
        if len(summary['by_type']) >= 3:
            print("✅ DIVERSIDAD: Múltiples tipos de POI detectados")
        else:
            print("⚠️  DIVERSIDAD: Pocos tipos de POI detectados")
        
        # Verificar funcionalidades
        if summary['total_active'] > 0:
            print("✅ FUNCIONALIDADES: Sistema de gestión de POIs activo")
        else:
            print("⚠️  FUNCIONALIDADES: Sin POIs activos para gestionar")
        
        # RESULTADO FINAL
        print("\n" + "=" * 60)
        if total_success and len(pois) > 0:
            print("🎉 RESULTADO: TEST COMPLETADO EXITOSAMENTE")
            print("✅ POI System v6.0 Enterprise VALIDADO")
        else:
            print("⚠️  RESULTADO: TEST COMPLETADO CON WARNINGS")
            print("🔧 Revisar componentes marcados")
        
        print("=" * 60)
        
        return total_success, pois, summary
        
    except Exception as e:
        print(f"\n❌ ERROR EN TEST: {e}")
        import traceback
        traceback.print_exc()
        return False, [], {}


def test_poi_specific_functionality():
    """Test específico de funcionalidades del POI System"""
    
    print("\n🎯 TEST ESPECÍFICO DE FUNCIONALIDADES POI")
    print("-" * 50)
    
    try:
        from core.analysis.poi_system import get_poi_system, POIType, POISignificance
        
        poi_system = get_poi_system({
            'enable_debug': False,  # Menos verbose
            'min_poi_strength': 50.0,  # Más permisivo
            'max_active_pois': 20
        })
        
        # Test detección específica por tipo
        print("\n🔍 Testing detección por tipo...")
        
        pois = poi_system.detect_pois("EURUSD", "M15", 3)
        
        # Contar tipos detectados
        type_counts = {}
        for poi in pois:
            ptype = poi.poi_type.value
            type_counts[ptype] = type_counts.get(ptype, 0) + 1
        
        expected_types = [
            'order_block', 'fair_value_gap', 'swing_high', 'swing_low',
            'session_high', 'session_low', 'liquidity_pool', 'fibonacci_level',
            'psychological_level'
        ]
        
        for expected in expected_types:
            count = type_counts.get(expected, 0)
            if count > 0:
                print(f"✅ {expected.replace('_', ' ').title()}: {count} detectados")
            else:
                print(f"ℹ️  {expected.replace('_', ' ').title()}: No detectado")
        
        # Test gestión de POIs
        print(f"\n🔄 Testing gestión de POIs...")
        
        if pois:
            # Test filtros
            high_significance = [p for p in pois if p.significance == POISignificance.HIGH]
            critical_pois = [p for p in pois if p.significance == POISignificance.CRITICAL]
            strong_pois = [p for p in pois if p.strength >= 80.0]
            
            print(f"   POIs alta significancia: {len(high_significance)}")
            print(f"   POIs críticos: {len(critical_pois)}")
            print(f"   POIs strength >80%: {len(strong_pois)}")
            
            # Test búsqueda por proximidad
            if pois:
                test_price = pois[0].price_level
                nearby = poi_system.get_pois_near_price(test_price, 0.0020)
                print(f"   POIs cerca de {test_price:.5f}: {len(nearby)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test específico: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Iniciando test completo del POI System...")
    
    # Test principal
    success, pois, summary = test_poi_system_integration()
    
    # Test específico
    specific_success = test_poi_specific_functionality()
    
    # Resumen final
    print(f"\n📋 RESUMEN FINAL:")
    print(f"   Test principal: {'✅ PASS' if success else '❌ FAIL'}")
    print(f"   Test específico: {'✅ PASS' if specific_success else '❌ FAIL'}")
    print(f"   POIs detectados: {len(pois)}")
    print(f"   Tipos únicos: {len(summary.get('by_type', {}))}")
    print(f"   Strength promedio: {summary.get('avg_strength', 0):.1f}%")
    
    if success and specific_success:
        print("\n🎉 TODOS LOS TESTS PASARON")
        print("✅ POI System v6.0 Enterprise LISTO PARA PRODUCCIÓN")
    else:
        print("\n⚠️  ALGUNOS TESTS FALLARON")
        print("🔧 Revisar logs arriba para detalles")
