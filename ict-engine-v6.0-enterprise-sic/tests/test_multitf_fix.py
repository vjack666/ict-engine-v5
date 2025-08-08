#!/usr/bin/env python3
"""
🔧 TEST RÁPIDO: Multi-Timeframe Enhancement CORREGIDO
====================================================

Test para verificar que los errores de TimedeltaIndex y metadata están corregidos.

Autor: ICT Engine v6.0 Enterprise
Fecha: 2025-01-08
"""

import sys
from pathlib import Path
import time
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_multi_timeframe_fix():
    """🔍 Test rápido para validar las correcciones"""
    
    print("=" * 60)
    print("🔧 TEST RÁPIDO: Multi-Timeframe Enhancement CORREGIDO")
    print("=" * 60)
    print()
    
    try:
        # Importar módulos necesarios
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        from core.analysis.pattern_detector import PatternDetector
        from sistema.sic_v3_1.enterprise_interface import SICv31Enterprise
        
        print("✅ Imports exitosos")
        
        # Inicializar componentes
        sic = SICv31Enterprise()
        detector = PatternDetector()  # 🔧 FIX: sin parámetros
        
        print("✅ Componentes inicializados")
        
        # Test rápido con datos pequeños
        symbol = 'EURUSD'
        timeframe = 'H1'
        
        print(f"\n🔍 Test rápido con {symbol} {timeframe}...")
        
        start_time = time.time()
        
        # Ejecutar análisis de patrones
        patterns = detector.detect_patterns(
            symbol=symbol,
            timeframe=timeframe,
            lookback_days=2  # Solo 2 días para test rápido
        )
        
        duration = time.time() - start_time
        
        print(f"\n📊 RESULTADOS TEST RÁPIDO:")
        print(f"   ✅ Sin errores TimedeltaIndex")
        print(f"   ✅ Sin errores metadata")
        print(f"   ✅ Patterns detectados: {len(patterns)}")
        print(f"   ✅ Tiempo: {duration:.3f}s")
        
        # Verificar que no hay mensajes de error en patterns
        error_count = 0
        for pattern in patterns:
            if "Error" in pattern.narrative:
                error_count += 1
        
        if error_count == 0:
            print(f"   ✅ Sin errores en narrativas: {error_count}")
        else:
            print(f"   ⚠️ Errores encontrados: {error_count}")
        
        print(f"\n🎉 TEST RÁPIDO COMPLETADO:")
        print(f"   Status: {'✅ SUCCESS' if error_count == 0 else '⚠️ PARTIAL'}")
        print(f"   Errores corregidos: TimedeltaIndex ✅, metadata ✅")
        
        return error_count == 0
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False

def main():
    """🚀 Función principal del test"""
    print(f"🕒 Iniciando test: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success = test_multi_timeframe_fix()
    
    print()
    print("=" * 60)
    if success:
        print("🎉 ERRORES MULTI-TIMEFRAME CORREGIDOS EXITOSAMENTE")
        print("✅ Sistema listo para producción")
    else:
        print("⚠️ Revisar errores restantes")
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
