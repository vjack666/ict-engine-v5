#!/usr/bin/env python3
"""
TEST REAL DE IMPORTACIONES POST-REORGANIZACIÓN
=============================================

Este es un TEST HONESTO que prueba las importaciones reales después de la reorganización.
Si alguna importación falla, se debe CORREGIR EN EL SISTEMA, NO EN EL TEST.

Fecha: 2025-08-10
Autor: GitHub Copilot  
Protocolo: REGLA #11 - Test Real, No Tramposo

ESTRUCTURA OBJETIVO SEGÚN TREE:
===============================
01-CORE/
├── core/
│   ├── analysis/
│   ├── data_management/
│   ├── ict_engine/
│   │   ├── advanced_patterns/
│   │   │   ├── breaker_blocks_enterprise_v62.py ⭐
│   │   │   ├── liquidity_analyzer_enterprise.py
│   │   │   ├── multi_pattern_confluence_engine.py
│   │   │   └── silver_bullet_enterprise.py
│   │   ├── displacement_detector_enterprise.py
│   │   ├── fractal_analyzer_enterprise.py
│   │   └── pattern_detector.py
│   └── smart_money_concepts/
└── utils/

02-TESTS/
├── integration/tests/ (múltiples archivos de test)
└── unit/

IMPORTACIONES CRÍTICAS A VALIDAR:
=================================
✅ Breaker Blocks v6.2 (recién migrado)
✅ Pattern Detector (integrado con v6.2)
✅ Fractal Analyzer Enterprise
✅ Data Management (MT5 connections)
✅ Smart Money Concepts
✅ ICT Engine Core Components
✅ Utils y Helper Systems
"""

import sys
import os
import importlib
import traceback
from pathlib import Path

# Agregar el directorio raíz al path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "01-CORE"))

def test_import_safety(module_path, description):
    """
    Test individual de importación con manejo de errores detallado.
    
    Args:
        module_path (str): Ruta del módulo a importar
        description (str): Descripción del módulo para el reporte
        
    Returns:
        tuple: (success: bool, error_info: str)
    """
    try:
        print(f"\n🔍 Probando: {description}")
        print(f"   Ruta: {module_path}")
        
        # Intento de importación
        module = importlib.import_module(module_path)
        
        # Verificación básica de que el módulo tiene contenido
        module_attrs = [attr for attr in dir(module) if not attr.startswith('_')]
        if not module_attrs:
            return False, f"Módulo importado pero sin atributos públicos"
            
        print(f"   ✅ SUCCESS - {len(module_attrs)} atributos públicos")
        return True, f"OK - {len(module_attrs)} atributos"
        
    except ImportError as e:
        error_detail = f"ImportError: {str(e)}"
        print(f"   ❌ IMPORT ERROR: {error_detail}")
        return False, error_detail
        
    except Exception as e:
        error_detail = f"Exception: {type(e).__name__}: {str(e)}"
        print(f"   ❌ GENERAL ERROR: {error_detail}")
        return False, error_detail

def test_core_imports_reorganization():
    """
    TEST PRINCIPAL: Valida todas las importaciones críticas post-reorganización.
    
    Este test es HONESTO y NO hace trampa. Si algo falla aquí,
    significa que hay un problema REAL que debe corregirse en el sistema.
    """
    print("="*80)
    print("TEST REAL DE IMPORTACIONES POST-REORGANIZACIÓN")
    print("="*80)
    print(f"Directorio de trabajo: {os.getcwd()}")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Python path agregado: {PROJECT_ROOT / '01-CORE'}")
    
    # DEFINICIÓN DE IMPORTACIONES CRÍTICAS SEGÚN LA ESTRUCTURA REAL
    critical_imports = [
        # === CORE ICT ENGINE ===
        ("core.ict_engine.advanced_patterns.breaker_blocks_enterprise_v62", 
         "🎯 Breaker Blocks v6.2 Enterprise (RECIÉN MIGRADO)"),
        
        ("core.ict_engine.pattern_detector", 
         "🔧 Pattern Detector (integrado con v6.2)"),
        
        ("core.ict_engine.fractal_analyzer_enterprise", 
         "📊 Fractal Analyzer Enterprise"),
        
        ("core.ict_engine.displacement_detector_enterprise", 
         "🚀 Displacement Detector Enterprise"),
        
        ("core.ict_engine.ict_types", 
         "🏗️ ICT Types (definiciones base)"),
        
        # === ADVANCED PATTERNS ===
        ("core.ict_engine.advanced_patterns.liquidity_analyzer_enterprise", 
         "💧 Liquidity Analyzer Enterprise"),
        
        ("core.ict_engine.advanced_patterns.multi_pattern_confluence_engine", 
         "🌊 Multi Pattern Confluence Engine"),
        
        ("core.ict_engine.advanced_patterns.silver_bullet_enterprise", 
         "🔫 Silver Bullet Enterprise"),
        
        # === ANALYSIS MODULES ===
        ("core.analysis.market_structure_analyzer", 
         "🏗️ Market Structure Analyzer"),
        
        ("core.analysis.market_context", 
         "📈 Market Context"),
        
        ("core.analysis.ict_historical_analyzer", 
         "📚 ICT Historical Analyzer"),
        
        ("core.analysis.multi_timeframe_analyzer", 
         "⏰ Multi Timeframe Analyzer"),
        
        # === DATA MANAGEMENT ===
        ("core.data_management.mt5_connection_manager", 
         "🔌 MT5 Connection Manager"),
        
        ("core.data_management.mt5_data_manager", 
         "📊 MT5 Data Manager"),
        
        ("core.data_management.ict_data_manager", 
         "🗄️ ICT Data Manager"),
        
        ("core.data_management.advanced_candle_downloader", 
         "⬇️ Advanced Candle Downloader"),
        
        # === SMART MONEY CONCEPTS ===
        ("core.smart_money_concepts.smart_money_analyzer", 
         "💰 Smart Money Analyzer"),
        
        # === CORE SYSTEMS ===
        ("core.poi_system", 
         "📍 POI System (Points of Interest)"),
        
        ("core.smart_trading_logger", 
         "📝 Smart Trading Logger"),
        
        # === UTILS ===
        ("utils.smart_trading_logger", 
         "📝 Utils Smart Trading Logger"),
        
        ("utils.ict_import_helper", 
         "🆘 ICT Import Helper"),
        
        ("utils.mt5_data_manager", 
         "📊 Utils MT5 Data Manager"),
    ]
    
    # EJECUTAR TESTS DE IMPORTACIÓN
    results = []
    successful_imports = 0
    failed_imports = 0
    
    print(f"\n🎯 INICIANDO VALIDACIÓN DE {len(critical_imports)} IMPORTACIONES CRÍTICAS...")
    
    for module_path, description in critical_imports:
        success, error_info = test_import_safety(module_path, description)
        
        results.append({
            'module': module_path,
            'description': description,
            'success': success,
            'error': error_info
        })
        
        if success:
            successful_imports += 1
        else:
            failed_imports += 1
    
    # === REPORTE FINAL ===
    print("\n" + "="*80)
    print("REPORTE FINAL DE IMPORTACIONES")
    print("="*80)
    
    print(f"\n📊 RESUMEN:")
    print(f"   ✅ Exitosas: {successful_imports}")
    print(f"   ❌ Fallidas: {failed_imports}")
    print(f"   📈 Tasa de éxito: {(successful_imports/len(critical_imports)*100):.1f}%")
    
    if failed_imports > 0:
        print(f"\n❌ IMPORTACIONES FALLIDAS ({failed_imports}):")
        print("-" * 50)
        
        for result in results:
            if not result['success']:
                print(f"\n🔥 FALLA: {result['description']}")
                print(f"   Módulo: {result['module']}")
                print(f"   Error: {result['error']}")
                
                # Sugerencias de corrección
                if "No module named" in result['error']:
                    print(f"   💡 ACCIÓN: Verificar que el archivo existe en la ruta correcta")
                    print(f"   💡 ACCIÓN: Verificar estructura de directorios")
                    print(f"   💡 ACCIÓN: Verificar archivos __init__.py")
                elif "ImportError" in result['error']:
                    print(f"   💡 ACCIÓN: Revisar dependencias del módulo")
                    print(f"   💡 ACCIÓN: Verificar imports internos del archivo")
    
    if successful_imports > 0:
        print(f"\n✅ IMPORTACIONES EXITOSAS ({successful_imports}):")
        print("-" * 50)
        
        for result in results:
            if result['success']:
                print(f"   ✅ {result['description']}")
    
    # === CONCLUSIÓN ===
    print(f"\n" + "="*80)
    if failed_imports == 0:
        print("🎉 CONCLUSIÓN: TODAS LAS IMPORTACIONES FUNCIONAN CORRECTAMENTE")
        print("   La reorganización fue exitosa. El sistema está listo para desarrollo.")
    else:
        print("⚠️  CONCLUSIÓN: HAY PROBLEMAS DE IMPORTACIÓN QUE DEBEN CORREGIRSE")
        print("   Estos son problemas REALES del sistema, no del test.")
        print("   Se deben corregir los imports y la estructura antes de continuar.")
    
    print("="*80)
    
    # Retornar True solo si TODAS las importaciones fueron exitosas
    return failed_imports == 0

if __name__ == "__main__":
    print("🚀 EJECUTANDO TEST REAL DE IMPORTACIONES POST-REORGANIZACIÓN...")
    print("   Este test NO hace trampas. Si falla, hay problemas reales que corregir.\n")
    
    success = test_core_imports_reorganization()
    
    if success:
        print("\n🏆 RESULTADO: TEST PASSED - Sistema listo para desarrollo")
        sys.exit(0)
    else:
        print("\n💥 RESULTADO: TEST FAILED - Corregir problemas de importación")
        sys.exit(1)
