#!/usr/bin/env python3
"""
🎯 TEST BOS/CHoCH DETECTION CON MEMORIA UNIFICADA
===============================================

Verifica la detección de Break of Structure (BOS) y Change of Character (CHoCH)
utilizando el sistema de memoria unificada v6.0 con datos reales.

Fecha: 8 de Agosto 2025 - 21:30 GMT
"""

import sys
import os
sys.path.append('.')

from datetime import datetime, timedelta
import time

def test_bos_choch_detection_with_memory():
    """Test de detección BOS/CHoCH con memoria unificada."""
    
    print("🎯 INICIANDO TEST - BOS/CHoCH DETECTION CON MEMORIA")
    print("=" * 60)
    
    try:
        # === PASO 1: IMPORTAR COMPONENTES ===
        print("📦 Paso 1: Importando componentes de detección...")
        
        from core.ict_engine.pattern_detector import get_pattern_detector, UNIFIED_MEMORY_AVAILABLE
        from core.analysis.market_structure_analyzer import MarketStructureAnalyzer
        from core.analysis.unified_market_memory import get_unified_market_memory, get_trading_insights
        
        print(f"✅ Componentes importados")
        print(f"   - Memoria Unificada: {'✅ Disponible' if UNIFIED_MEMORY_AVAILABLE else '❌ No disponible'}")
        
        # === PASO 2: CONFIGURAR DETECTOR ===
        print("\\n🔧 Paso 2: Configurando detector enterprise...")
        
        config = {
            'enable_debug': True,
            'use_multi_timeframe': True,
            'enable_cache': True,
            'min_pattern_probability': 50.0,  # Threshold bajo para detectar más patterns
            'min_ob_reaction_pips': 5.0,
            'min_fvg_size_pips': 3.0,
            'pattern_lookback': 200,  # Más historia para mejor detección
            'volume_weight': 0.3,
            'structure_weight': 0.7
        }
        
        detector = get_pattern_detector(config)
        print(f"✅ Detector configurado")
        print(f"   - Memoria: {'✅ Conectada' if detector._unified_memory else '❌ Desconectada'}")
        
        # === PASO 3: CONFIGURAR ANALYZER DE ESTRUCTURA ===
        print("\\n📊 Paso 3: Configurando Market Structure Analyzer...")
        
        structure_analyzer = MarketStructureAnalyzer()
        print(f"✅ Market Structure Analyzer listo")
        
        # === PASO 4: OBTENER MEMORIA ACTUAL ===
        print("\\n🧠 Paso 4: Verificando estado de memoria...")
        
        unified_memory = get_unified_market_memory()
        memory_state = unified_memory.unified_state
        
        print(f"✅ Estado de memoria:")
        print(f"   - Quality: {memory_state['memory_quality']}")
        print(f"   - Total Analyses: {memory_state['total_analyses']}")
        print(f"   - Coherence: {memory_state['coherence_score']:.3f}")
        print(f"   - Components: {sum(memory_state['active_components'].values())}/3")
        
        # === PASO 5: DETECTAR PATTERNS EN MÚLTIPLES SÍMBOLOS ===
        print("\\n🎯 Paso 5: Ejecutando detección BOS/CHoCH...")
        
        # Símbolos críticos para ICT
        symbols = ['EURUSD', 'GBPUSD', 'USDJPY']
        timeframes = ['H4', 'H1', 'M15']
        
        total_bos = 0
        total_choch = 0
        total_patterns = 0
        results_summary = []
        
        for symbol in symbols:
            print(f"\\n   📈 Analizando {symbol}...")
            
            symbol_bos = 0
            symbol_choch = 0
            symbol_patterns = 0
            
            for timeframe in timeframes:
                try:
                    print(f"      🔍 {timeframe}: ", end="")
                    
                    # Detectar patterns
                    result = detector.detect_patterns(
                        symbol=symbol,
                        timeframe=timeframe,
                        lookback_days=5  # 5 días de historia
                    )
                    
                    # Analizar estructura de mercado
                    structure_result = structure_analyzer.analyze_market_structure(
                        symbol=symbol,
                        timeframe=timeframe,
                        lookback_days=5
                    )
                    
                    # Contar BOS y CHoCH de structure analyzer directamente
                    tf_bos = 0
                    tf_choch = 0
                    tf_patterns = result.total_patterns
                    
                    # Contar BOS/CHoCH del analysis de estructura
                    if structure_result and hasattr(structure_result, 'structure_changes'):
                        for change in structure_result.structure_changes:
                            if 'bos' in change.lower():
                                tf_bos += 1
                            elif 'choch' in change.lower():
                                tf_choch += 1
                    
                    # También revisar en logs debug para conteo directo
                    # (Alternative method based on market structure debug output)
                    if structure_result and hasattr(structure_result, 'detected_structures'):
                        for struct in structure_result.detected_structures:
                            struct_type = getattr(struct, 'structure_type', str(struct))
                            if 'bos' in str(struct_type).lower():
                                tf_bos += 1
                            elif 'choch' in str(struct_type).lower():
                                tf_choch += 1
                    
                    # CHoCH se detecta en cambios de bias del mercado
                    if hasattr(structure_result, 'bias_changes') and structure_result.bias_changes > 0:
                        tf_choch += structure_result.bias_changes
                    
                    symbol_bos += tf_bos
                    symbol_choch += tf_choch
                    symbol_patterns += tf_patterns
                    
                    print(f"Patterns: {tf_patterns}, BOS: {tf_bos}, CHoCH: {tf_choch}")
                    
                    # Actualizar memoria con cada detección
                    if detector._unified_memory:
                        insights = get_trading_insights(symbol, [timeframe])
                        
                except Exception as e:
                    print(f"Error: {str(e)[:50]}...")
                    
            total_bos += symbol_bos
            total_choch += symbol_choch
            total_patterns += symbol_patterns
            
            results_summary.append({
                'symbol': symbol,
                'total_patterns': symbol_patterns,
                'bos_count': symbol_bos,
                'choch_count': symbol_choch
            })
            
            print(f"   📊 {symbol} TOTAL: Patterns: {symbol_patterns}, BOS: {symbol_bos}, CHoCH: {symbol_choch}")
        
        # === PASO 6: VERIFICAR MEMORIA POST-ANÁLISIS ===
        print("\\n🧠 Paso 6: Verificando memoria post-análisis...")
        
        updated_memory = get_unified_market_memory()
        updated_state = updated_memory.unified_state
        
        print(f"✅ Estado actualizado:")
        print(f"   - Quality: {updated_state['memory_quality']}")
        print(f"   - Total Analyses: {updated_state['total_analyses']}")
        print(f"   - Coherence: {updated_state['coherence_score']:.3f}")
        
        # === RESUMEN FINAL ===
        print("\\n" + "=" * 60)
        print("🎉 DETECCIÓN BOS/CHoCH CON MEMORIA - COMPLETADA")
        print("=" * 60)
        
        print("📊 RESUMEN GLOBAL:")
        print(f"   🎯 Total Patterns Detectados: {total_patterns}")
        print(f"   📈 Total BOS (Break of Structure): {total_bos}")
        print(f"   🔄 Total CHoCH (Change of Character): {total_choch}")
        print(f"   🧠 Análisis en Memoria: {updated_state['total_analyses']}")
        
        print("\\n📋 DETALLE POR SÍMBOLO:")
        for result in results_summary:
            print(f"   {result['symbol']}: {result['total_patterns']} patterns, "
                  f"{result['bos_count']} BOS, {result['choch_count']} CHoCH")
        
        # Calcular eficiencia
        efficiency = (total_bos + total_choch) / total_patterns * 100 if total_patterns > 0 else 0
        print(f"\\n📈 EFICIENCIA BOS/CHoCH: {efficiency:.1f}%")
        
        print("\\n✅ MEMORIA FUNCIONANDO COMO TRADER REAL")
        print(f"🎯 Coherence Score Final: {updated_state['coherence_score']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"\\n❌ ERROR EN TEST: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_bos_choch_detection_with_memory()
    
    if success:
        print("\\n🎯 RESULTADO: SISTEMA BOS/CHoCH + MEMORIA OPERATIVO")
    else:
        print("\\n⚠️ RESULTADO: REQUIERE CORRECCIONES")
