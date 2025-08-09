#!/usr/bin/env python3
"""
🧪 TEST FASE 1 - MIGRACIÓN CORE LOGIC FVG
=========================================
Test básico para validar la migración exitosa del código legacy FVG
✅ REGLA #8: Testing crítico con SIC/SLUC y PowerShell
"""

import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

# ✅ REGLA #8: SIC/SLUC imports obligatorios
try:
    from sistema.sic_bridge import SICBridge
    from core.smart_trading_logger import log_trading_decision_smart_v6
    SIC_SLUC_AVAILABLE = True
except ImportError:
    print("⚠️ SIC/SLUC no disponible - test en modo fallback")
    SIC_SLUC_AVAILABLE = False
    def log_trading_decision_smart_v6(event, data, **kwargs):
        print(f"[FALLBACK] {event}: {data}")

def test_fvg_fase_1_migration():
    """
    🧪 Test FASE 1: Migración Core Logic FVG
    Valida que el código legacy fue migrado correctamente
    """
    
    # ✅ REGLA #8: Log inicio de test con SLUC
    log_trading_decision_smart_v6("TEST_FASE1_FVG_START", {
        "test_name": "test_fvg_fase_1_migration",
        "purpose": "Validar migración legacy FVG",
        "sic_available": SIC_SLUC_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    })
    
    print("🧪 TEST FASE 1 - MIGRACIÓN CORE LOGIC FVG")
    print("=" * 50)
    
    try:
        # 1. Import del pattern detector
        from core.ict_engine.pattern_detector import ICTPatternDetector
        print("✅ Import ICTPatternDetector exitoso")
        
        # 2. Crear instancia del detector
        detector = ICTPatternDetector()
        print("✅ ICTPatternDetector inicializado")
        
        # 3. Crear datos de prueba simulando FVG
        test_data = create_test_fvg_data()
        print(f"✅ Datos de prueba creados: {len(test_data)} velas")
        
        # 4. Test detect_fvg_with_memory method
        if hasattr(detector, 'detect_fvg_with_memory'):
            result = detector.detect_fvg_with_memory(
                data=test_data,
                timeframe="M15",
                symbol="EURUSD"
            )
            
            # ✅ REGLA #8: Assertions específicas
            assert isinstance(result, dict), f"Expected dict, got {type(result)}"
            assert 'detected_fvgs' in result, "Missing 'detected_fvgs' key"
            assert 'total_detected' in result, "Missing 'total_detected' key"
            assert 'execution_time' in result, "Missing 'execution_time' key"
            assert 'performance_ok' in result, "Missing 'performance_ok' key"
            
            detected_fvgs = result['detected_fvgs']
            execution_time = result['execution_time']
            
            print(f"✅ FVG detection ejecutado en {execution_time:.3f}s")
            print(f"✅ FVGs detectados: {len(detected_fvgs)}")
            
            # ✅ REGLA #8: Performance enterprise <5s
            assert execution_time < 5.0, f"Performance failed: {execution_time}s > 5s"
            print("✅ Performance enterprise validado (<5s)")
            
            # 5. Validar que se detectó al menos un FVG en datos de prueba
            assert len(detected_fvgs) > 0, "No FVGs detected in test data"
            print(f"✅ FVG detection functional: {len(detected_fvgs)} FVGs detectados")
            
            # 6. Validar estructura de FVG
            if detected_fvgs:
                fvg = detected_fvgs[0]
                
                # Verificar atributos obligatorios
                required_attrs = ['fvg_type', 'high_price', 'low_price', 'gap_size_pips']
                for attr in required_attrs:
                    assert hasattr(fvg, attr), f"Missing attribute: {attr}"
                
                print("✅ Estructura FVG validada")
                
                # Verificar legacy scoring en metadata
                if hasattr(fvg, 'sic_stats') and fvg.sic_stats:
                    assert 'legacy_score' in fvg.sic_stats, "Missing legacy_score in sic_stats"
                    assert 'legacy_confidence' in fvg.sic_stats, "Missing legacy_confidence in sic_stats"
                    print("✅ Legacy scoring migrado correctamente")
            
        else:
            raise AttributeError("Method detect_fvg_with_memory not found")
        
        # ✅ REGLA #8: Log éxito con métricas
        log_trading_decision_smart_v6("TEST_FASE1_FVG_SUCCESS", {
            "test_name": "test_fvg_fase_1_migration",
            "execution_time": execution_time,
            "fvgs_detected": len(detected_fvgs),
            "performance_ok": execution_time < 5.0,
            "assertions_passed": 8,
            "status": "MIGRATION_SUCCESSFUL"
        })
        
        print("\n🎉 ¡FASE 1 COMPLETADA EXITOSAMENTE!")
        print(f"✅ Migración legacy validada")
        print(f"✅ Performance: {execution_time:.3f}s < 5s")
        print(f"✅ FVGs detectados: {len(detected_fvgs)}")
        print(f"✅ Todas las assertions pasaron")
        
        return True
        
    except Exception as e:
        # ✅ REGLA #8: Log falla con contexto completo
        log_trading_decision_smart_v6("TEST_FASE1_FVG_FAILURE", {
            "test_name": "test_fvg_fase_1_migration",
            "error": str(e),
            "error_type": type(e).__name__,
            "status": "MIGRATION_FAILED"
        })
        print(f"❌ ERROR en FASE 1: {e}")
        raise

def create_test_fvg_data():
    """
    📊 Crea datos de prueba que contienen Fair Value Gaps para validar detección
    """
    
    # Crear DataFrame con FVG bullish
    data = {
        'open': [1.0900, 1.0910, 1.0920, 1.0950, 1.0955],
        'high': [1.0905, 1.0915, 1.0925, 1.0960, 1.0965],
        'low':  [1.0895, 1.0905, 1.0915, 1.0945, 1.0950],
        'close':[1.0910, 1.0920, 1.0930, 1.0955, 1.0960]
    }
    
    # Crear gap bullish entre índice 1 y 3
    # prev_high = 1.0915, next_low = 1.0945 -> gap de 30 pips
    data['high'][1] = 1.0915
    data['low'][3] = 1.0945
    
    df = pd.DataFrame(data)
    df.index = pd.date_range(start='2025-01-01', periods=len(df), freq='15min')
    
    return df

def main():
    """Main con configuración PowerShell y SIC/SLUC"""
    
    # ✅ REGLA #8: Verificar PYTHONPATH (PowerShell)
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    print("🧪 INICIANDO TEST FASE 1 - MIGRACIÓN FVG...")
    
    try:
        success = test_fvg_fase_1_migration()
        
        if success:
            print(f"\n🏆 TEST FASE 1 COMPLETADO EXITOSAMENTE!")
            print(f"✅ Migración Core Logic FVG validada")
            print(f"📋 LISTO PARA FASE 2: Memory Enhancement")
        
        return True
        
    except Exception as e:
        print(f"❌ FASE 1 FALLÓ: {e}")
        print(f"🔧 Revisar migración antes de continuar")
        return False

if __name__ == "__main__":
    success = main()
    exit_code = 0 if success else 1
    print(f"\n🏁 Test FASE 1 completado con código: {exit_code}")
    sys.exit(exit_code)
