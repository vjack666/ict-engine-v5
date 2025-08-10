#!/usr/bin/env python3
"""
🧪 TEST DIAGNÓSTICO UNIFIED_MEMORY_SYSTEM_CREATE - v6.1
========================================================
✅ REGLA #7: Test primero para diagnosticar conexión
✅ REGLA #8: Testing crítico con SIC/SLUC

Verifica específicamente por qué UnifiedMemorySystem se crea pero no se conecta.
"""

import sys
from pathlib import Path

# Configurar PYTHONPATH
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

try:
    from core.smart_trading_logger import log_trading_decision_smart_v6
    from core.ict_engine.pattern_detector import ICTPatternDetector
    from core.analysis.unified_memory_system import get_unified_memory_system
    
    # Verificar disponibilidad
    try:
        from core.ict_engine.pattern_detector import UNIFIED_MEMORY_SYSTEM_AVAILABLE
    except ImportError:
        UNIFIED_MEMORY_SYSTEM_AVAILABLE = False
    
    print("✅ Imports exitosos")
except ImportError as e:
    print(f"❌ Error de import: {e}")
    sys.exit(1)

def diagnose_unified_memory_system_connection():
    """
    🔍 Diagnóstico específico de conexión UnifiedMemorySystem
    """
    print("🔍 DIAGNÓSTICO UNIFIED_MEMORY_SYSTEM_CREATE")
    print("=" * 60)
    
    log_trading_decision_smart_v6("DIAGNOSTIC_START", {
        "test": "UnifiedMemorySystem connection diagnostic",
        "purpose": "Verificar por qué se crea pero no se conecta"
    })
    
    # ✅ PASO 1: Verificar disponibilidad del módulo
    print(f"\\n🧪 PASO 1: Módulo UnifiedMemorySystem disponible: {UNIFIED_MEMORY_SYSTEM_AVAILABLE}")
    
    # ✅ PASO 2: Crear instancia directa
    print("\\n🧪 PASO 2: Creando instancia directa...")
    try:
        direct_instance = get_unified_memory_system()
        print(f"   ✅ Instancia directa creada: {type(direct_instance)}")
        print(f"   ✅ ID de instancia: {id(direct_instance)}")
        print(f"   ✅ Tiene market_context: {hasattr(direct_instance, 'market_context')}")
        print(f"   ✅ Tiene confidence_evaluator: {hasattr(direct_instance, 'confidence_evaluator')}")
    except Exception as e:
        print(f"   ❌ Error creando instancia directa: {e}")
        return False
    
    # ✅ PASO 3: Crear ICTPatternDetector y verificar conexión
    print("\\n🧪 PASO 3: Creando ICTPatternDetector...")
    try:
        detector = ICTPatternDetector()
        print(f"   ✅ ICTPatternDetector creado: {type(detector)}")
        
        # Verificar la variable de memoria
        print(f"   🔍 _unified_memory_system type: {type(detector._unified_memory_system)}")
        print(f"   🔍 _unified_memory_system is None: {detector._unified_memory_system is None}")
        print(f"   🔍 _unified_memory_system ID: {id(detector._unified_memory_system) if detector._unified_memory_system else 'None'}")
        
        # Verificar si son la misma instancia
        if detector._unified_memory_system:
            same_instance = id(detector._unified_memory_system) == id(direct_instance)
            print(f"   🔍 Misma instancia que directa: {same_instance}")
        
    except Exception as e:
        print(f"   ❌ Error creando ICTPatternDetector: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # ✅ PASO 4: Verificar métodos memory-aware
    print("\\n🧪 PASO 4: Verificando métodos memory-aware...")
    methods_to_check = [
        'detect_bos_with_memory',
        'detect_choch_with_memory', 
        '_enhance_with_memory',
        '_is_known_false_positive'
    ]
    
    for method in methods_to_check:
        has_method = hasattr(detector, method)
        print(f"   - {method}: {'✅' if has_method else '❌'}")
    
    # ✅ PASO 5: Test funcional de memoria
    print("\\n🧪 PASO 5: Test funcional básico...")
    try:
        if detector._unified_memory_system:
            # Test básico del sistema de memoria
            test_insight = detector._unified_memory_system.get_historical_insight("test", "M15")
            print(f"   ✅ get_historical_insight funciona: {type(test_insight)}")
            
            # Test de evaluación de confianza
            test_data = {'confidence': 0.5, 'strength': 0.7}
            confidence_result = detector._unified_memory_system.confidence_evaluator.assess_market_confidence(test_data)
            print(f"   ✅ assess_market_confidence funciona: {confidence_result}")
            
        else:
            print("   ❌ No se puede hacer test funcional - sistema no conectado")
            
    except Exception as e:
        print(f"   ⚠️ Error en test funcional: {e}")
    
    # ✅ RESULTADO FINAL
    memory_connected = detector._unified_memory_system is not None
    all_methods_present = all(hasattr(detector, method) for method in methods_to_check)
    
    print(f"\\n🎯 RESULTADO DIAGNÓSTICO:")
    print(f"   - Módulo disponible: {'✅' if UNIFIED_MEMORY_SYSTEM_AVAILABLE else '❌'}")
    print(f"   - Instancia directa: ✅")
    print(f"   - UnifiedMemorySystem conectado: {'✅' if memory_connected else '❌'}")
    print(f"   - Métodos memory-aware: {'✅' if all_methods_present else '❌'}")
    
    success = UNIFIED_MEMORY_SYSTEM_AVAILABLE and memory_connected and all_methods_present
    
    log_trading_decision_smart_v6("DIAGNOSTIC_RESULT", {
        "module_available": UNIFIED_MEMORY_SYSTEM_AVAILABLE,
        "memory_connected": memory_connected,
        "methods_present": all_methods_present,
        "diagnostic_success": success
    })
    
    if success:
        print("\\n🎉 DIAGNÓSTICO: FASE 3 FUNCIONAL")
    else:
        print("\\n❌ DIAGNÓSTICO: PROBLEMAS IDENTIFICADOS")
        
        if not memory_connected:
            print("   🔧 SOLUCIÓN: Verificar inicialización en _initialize_components")
        if not all_methods_present:
            print("   🔧 SOLUCIÓN: Verificar que métodos memory-aware estén implementados")
    
    return success

def main():
    """
    ✅ REGLA #8: Main con configuración PowerShell y SIC/SLUC
    """
    print("🧪 DIAGNÓSTICO DETALLADO - UNIFIED_MEMORY_SYSTEM_CREATE")
    print("=" * 70)
    
    success = diagnose_unified_memory_system_connection()
    
    if success:
        print("\\n✅ DIAGNÓSTICO COMPLETADO - SISTEMA FUNCIONAL")
    else:
        print("\\n❌ DIAGNÓSTICO COMPLETADO - REQUIERE CORRECCIONES")

if __name__ == "__main__":
    main()
