#!/usr/bin/env python3
"""
🧪 TEST: Market Structure Analyzer v6.0 Enterprise
=================================================

Test completo del Market Structure Analyzer que verifica:
- Detección de swing points
- Identificación de CHoCH y BOS
- Análisis de Fair Value Gaps
- Detección de Order Blocks
- Integración con AdvancedCandleDownloader

Autor: ICT Engine v6.0 Enterprise Team
Fecha: Agosto 7, 2025
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import pytest

# Agregar el directorio raíz al PATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_market_structure_analyzer_initialization():
    """🏗️ Test de inicialización del Market Structure Analyzer"""
    print("🧪 TEST: Market Structure Analyzer Initialization")
    print("=" * 60)
    
    try:
        # Importar el analizador
        from core.analysis.market_structure_analyzer import get_market_structure_analyzer
        
        # Crear instancia con configuración de test
        config = {
            'enable_debug': True,
            'use_multi_timeframe': False,  # Simplificar para test
            'min_confidence': 60.0,
            'swing_window': 3  # Ventana más pequeña para test
        }
        
        analyzer = get_market_structure_analyzer(config)
        print("✅ MarketStructureAnalyzer creado exitosamente")
        
        # Verificar estado inicial
        state = analyzer.get_current_structure_state()
        print(f"✅ Estado inicial: {state}")
        
        # Verificar configuración
        assert analyzer.min_confidence == 60.0
        assert analyzer.swing_window == 3
        print("✅ Configuración aplicada correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en inicialización: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_market_structure_analysis_basic():
    """📊 Test de análisis básico de estructura"""
    print("\n📊 TEST: Market Structure Analysis Basic")
    print("=" * 60)
    
    try:
        from core.analysis.market_structure_analyzer import get_market_structure_analyzer
        
        # Crear analizador
        analyzer = get_market_structure_analyzer({
            'enable_debug': True,
            'use_multi_timeframe': False,
            'min_confidence': 50.0  # Más permisivo para test
        })
        
        # Ejecutar análisis
        print("📈 Ejecutando análisis de EURUSD M15...")
        signal = analyzer.analyze_market_structure(
            symbol="EURUSD",
            timeframe="M15",
            lookback_days=3
        )
        
        if signal:
            print(f"✅ Señal generada:")
            print(f"   🏗️ Tipo: {signal.structure_type.value}")
            print(f"   🎯 Dirección: {signal.direction.value}")
            print(f"   📊 Confianza: {signal.confidence:.1f}%")
            print(f"   💎 FVG presente: {signal.fvg_present}")
            print(f"   📦 Order Block presente: {signal.order_block_present}")
            print(f"   🎯 Swing highs: {len(signal.swing_highs)}")
            print(f"   🎯 Swing lows: {len(signal.swing_lows)}")
            
            # Validar estructura de la señal
            assert hasattr(signal, 'structure_type')
            assert hasattr(signal, 'confidence')
            assert hasattr(signal, 'direction')
            assert signal.confidence >= 0
            assert signal.confidence <= 100
            
            print("✅ Estructura de señal válida")
            
        else:
            print("ℹ️ Sin señales estructurales detectadas (normal en datos simulados)")
        
        # Verificar métricas de performance
        metrics = analyzer.get_performance_metrics()
        print(f"✅ Métricas de performance: {metrics}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en análisis: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_market_structure_swing_points():
    """🎯 Test específico de detección de swing points"""
    print("\n🎯 TEST: Swing Points Detection")
    print("=" * 60)
    
    try:
        from core.analysis.market_structure_analyzer import get_market_structure_analyzer
        
        # Crear analizador con ventana pequeña para test
        analyzer = get_market_structure_analyzer({
            'swing_window': 2,
            'enable_debug': True
        })
        
        # Crear datos de prueba usando el downloader
        print("📥 Obteniendo datos para test...")
        candles_data = analyzer._get_market_data("EURUSD", "M15", 2)
        
        if candles_data is not None and len(candles_data) >= 10:
            print(f"✅ Datos obtenidos: {len(candles_data)} velas")
            
            # Test de detección de swing points
            swing_highs, swing_lows = analyzer._detect_swing_points(candles_data)
            
            print(f"🎯 Swing highs detectados: {len(swing_highs)}")
            print(f"🎯 Swing lows detectados: {len(swing_lows)}")
            
            # Validar swing points
            for sh in swing_highs[:3]:  # Primeros 3
                assert hasattr(sh, 'price')
                assert hasattr(sh, 'index')
                assert hasattr(sh, 'point_type')
                assert sh.point_type == 'high'
                print(f"   📈 Swing High: {sh.price} en index {sh.index}")
            
            for sl in swing_lows[:3]:  # Primeros 3
                assert hasattr(sl, 'price')
                assert hasattr(sl, 'index')
                assert hasattr(sl, 'point_type')
                assert sl.point_type == 'low'
                print(f"   📉 Swing Low: {sl.price} en index {sl.index}")
            
            print("✅ Swing points detectados correctamente")
            
        else:
            print("⚠️ Sin datos suficientes para test swing points")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test swing points: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_market_structure_integration_with_downloader():
    """🔗 Test de integración con AdvancedCandleDownloader"""
    print("\n🔗 TEST: Integration with AdvancedCandleDownloader")
    print("=" * 60)
    
    try:
        from core.analysis.market_structure_analyzer import get_market_structure_analyzer
        
        # Crear analizador
        analyzer = get_market_structure_analyzer()
        
        # Verificar que el downloader está configurado
        assert analyzer._downloader is not None
        print("✅ AdvancedCandleDownloader conectado")
        
        # Test de obtención de datos
        symbols = ["EURUSD", "GBPUSD"]
        timeframes = ["M15", "M5"]
        
        for symbol in symbols:
            for tf in timeframes:
                print(f"📊 Probando {symbol} {tf}...")
                
                data = analyzer._get_market_data(symbol, tf, 1)  # 1 día
                
                if data is not None:
                    print(f"   ✅ {len(data)} velas obtenidas")
                    
                    # Verificar estructura de datos
                    required_columns = ['open', 'high', 'low', 'close']
                    for col in required_columns:
                        assert col in data.columns, f"Columna {col} faltante"
                    
                    print(f"   ✅ Estructura de datos válida")
                else:
                    print(f"   ⚠️ Sin datos para {symbol} {tf}")
        
        print("✅ Integración con downloader funcional")
        return True
        
    except Exception as e:
        print(f"❌ Error en integración: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_market_structure_fvg_detection():
    """💎 Test de detección de Fair Value Gaps"""
    print("\n💎 TEST: Fair Value Gap Detection")
    print("=" * 60)
    
    try:
        from core.analysis.market_structure_analyzer import get_market_structure_analyzer
        
        analyzer = get_market_structure_analyzer({
            'fvg_min_gap': 0.0001  # Gap muy pequeño para test
        })
        
        # Obtener datos para test
        data = analyzer._get_market_data("EURUSD", "M15", 2)
        
        if data is not None and len(data) >= 10:
            print(f"📊 Analizando FVGs en {len(data)} velas...")
            
            # Contar FVGs antes
            fvgs_before = len(analyzer.detected_fvgs)
            
            # Ejecutar detección
            fvg_found = analyzer._detect_fair_value_gaps(data)
            
            # Contar FVGs después
            fvgs_after = len(analyzer.detected_fvgs)
            new_fvgs = fvgs_after - fvgs_before
            
            print(f"💎 FVGs detectados: {new_fvgs}")
            print(f"💎 Total FVGs en memoria: {fvgs_after}")
            
            # Verificar estructura de FVGs detectados
            for fvg in analyzer.detected_fvgs[-3:]:  # Últimos 3
                assert hasattr(fvg, 'fvg_type')
                assert hasattr(fvg, 'high_price')
                assert hasattr(fvg, 'low_price')
                assert fvg.high_price > fvg.low_price
                print(f"   💎 FVG {fvg.fvg_type.value}: {fvg.low_price} - {fvg.high_price}")
            
            print("✅ Detección de FVGs funcional")
            
        else:
            print("⚠️ Sin datos suficientes para test FVG")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test FVG: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_market_structure_order_blocks():
    """📦 Test de detección de Order Blocks"""
    print("\n📦 TEST: Order Block Detection")
    print("=" * 60)
    
    try:
        from core.analysis.market_structure_analyzer import get_market_structure_analyzer
        
        analyzer = get_market_structure_analyzer({
            'ob_reaction_threshold': 0.1  # Threshold bajo para test
        })
        
        # Obtener datos para test
        data = analyzer._get_market_data("EURUSD", "M15", 2)
        
        if data is not None and len(data) >= 20:
            print(f"📊 Analizando Order Blocks en {len(data)} velas...")
            
            # Contar OBs antes
            obs_before = len(analyzer.detected_order_blocks)
            
            # Ejecutar detección
            ob_found = analyzer._detect_order_blocks(data)
            
            # Contar OBs después
            obs_after = len(analyzer.detected_order_blocks)
            new_obs = obs_after - obs_before
            
            print(f"📦 Order Blocks detectados: {new_obs}")
            print(f"📦 Total OBs en memoria: {obs_after}")
            
            # Verificar estructura de OBs detectados
            for ob in analyzer.detected_order_blocks[-3:]:  # Últimos 3
                assert hasattr(ob, 'ob_type')
                assert hasattr(ob, 'high_price')
                assert hasattr(ob, 'low_price')
                assert hasattr(ob, 'reaction_strength')
                assert ob.high_price > ob.low_price
                print(f"   📦 OB {ob.ob_type.value}: {ob.low_price} - {ob.high_price} (fuerza: {ob.reaction_strength:.3f})")
            
            print("✅ Detección de Order Blocks funcional")
            
        else:
            print("⚠️ Sin datos suficientes para test Order Blocks")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test Order Blocks: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_market_structure_performance():
    """📈 Test de performance y métricas"""
    print("\n📈 TEST: Performance Metrics")
    print("=" * 60)
    
    try:
        from core.analysis.market_structure_analyzer import get_market_structure_analyzer
        
        analyzer = get_market_structure_analyzer()
        
        # Ejecutar múltiples análisis para generar métricas
        symbols = ["EURUSD", "GBPUSD"]
        
        for symbol in symbols:
            print(f"⚡ Analizando {symbol}...")
            
            start_time = datetime.now()
            signal = analyzer.analyze_market_structure(symbol, "M15", 1)
            end_time = datetime.now()
            
            analysis_time = (end_time - start_time).total_seconds()
            print(f"   ⏱️ Tiempo de análisis: {analysis_time:.3f} segundos")
            
            if signal:
                print(f"   ✅ Señal: {signal.structure_type.value} - {signal.confidence:.1f}%")
        
        # Obtener métricas finales
        metrics = analyzer.get_performance_metrics()
        print(f"\n📊 MÉTRICAS FINALES:")
        print(f"   🔢 Total análisis: {metrics.get('total_analyses', 0)}")
        if metrics.get('avg_analysis_time'):
            print(f"   ⏱️ Tiempo promedio: {metrics['avg_analysis_time']:.3f}s")
        if metrics.get('avg_confidence'):
            print(f"   🎯 Confianza promedio: {metrics['avg_confidence']:.1f}%")
        
        print("✅ Métricas de performance generadas")
        return True
        
    except Exception as e:
        print(f"❌ Error en test performance: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 ICT ENGINE v6.0 - MARKET STRUCTURE ANALYZER TESTS")
    print("=" * 70)
    
    # Ejecutar todos los tests
    tests = [
        test_market_structure_analyzer_initialization,
        test_market_structure_analysis_basic,
        test_market_structure_swing_points,
        test_market_structure_integration_with_downloader,
        test_market_structure_fvg_detection,
        test_market_structure_order_blocks,
        test_market_structure_performance
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE TESTS:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {i+1}. {test.__name__}: {status}")
    
    print(f"\n🎯 RESULTADO FINAL: {passed}/{total} tests pasaron")
    
    if passed == total:
        print("🎉 TODOS LOS TESTS PASARON")
        print("✅ Market Structure Analyzer está listo para producción")
    else:
        print("⚠️ ALGUNOS TESTS FALLARON")
        print("🔧 Revisar implementación antes de continuar")
    
    print("\n🏆 Market Structure Analyzer v6.0 Enterprise - Testing Complete")
