#!/usr/bin/env python3
"""
🔧 ARREGLO DE IMPORTS - SIGUIENDO REGLAS COPILOT
===============================================

Arregla el problema de imports para el test de migración Fase 1
aplicando REGLA #4: SISTEMA SIC Y SLUC OBLIGATORIO

Fecha: Agosto 8, 2025
Aplicando: REGLAS_COPILOT.md
"""

import sys
import os
from pathlib import Path

# ✅ REGLA #4: Importar SIC Bridge según las reglas
try:
    from sistema.sic_bridge import SICBridge
    SIC_AVAILABLE = True
except ImportError:
    print("⚠️ SIC Bridge no disponible - continuando sin SIC")
    SIC_AVAILABLE = False

# ✅ REGLA #4: Importar SLUC según las reglas
try:
    from core.smart_trading_logger import log_trading_decision_smart_v6
    SLUC_AVAILABLE = True
except ImportError:
    print("⚠️ SLUC no disponible - usando print temporal")
    SLUC_AVAILABLE = False
    
    def log_trading_decision_smart_v6(event_type, data, **kwargs):
        """Fallback temporal para logging"""
        print(f"[{event_type}] {data}")

def setup_python_path():
    """
    Configura PYTHONPATH siguiendo las reglas del proyecto
    
    ✅ REGLA #1: Revisar antes de crear - verificando estructura existente
    ✅ REGLA #4: Sistema SIC - logging con SLUC
    """
    
    # Log inicio según REGLA #4
    log_trading_decision_smart_v6("SETUP_START", {
        "function": "setup_python_path",
        "purpose": "Configurar imports para tests migración",
        "sic_available": SIC_AVAILABLE,
        "sluc_available": SLUC_AVAILABLE
    })
    
    # Encontrar directorio raíz del proyecto
    current_dir = Path(__file__).parent.absolute()
    project_root = current_dir.parent  # Subir un nivel desde tests/
    
    log_trading_decision_smart_v6("PATH_DETECTION", {
        "current_dir": str(current_dir),
        "project_root": str(project_root),
        "exists": project_root.exists()
    })
    
    # Verificar estructura según REGLA #1
    core_dir = project_root / "core"
    sistema_dir = project_root / "sistema"
    
    structure_check = {
        "core_exists": core_dir.exists(),
        "sistema_exists": sistema_dir.exists(),
        "core_init": (core_dir / "__init__.py").exists(),
        "sistema_init": (sistema_dir / "__init__.py").exists()
    }
    
    log_trading_decision_smart_v6("STRUCTURE_CHECK", structure_check)
    
    # Agregar al PYTHONPATH
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        log_trading_decision_smart_v6("PYTHONPATH_UPDATED", {
            "added_path": str(project_root),
            "sys_path_length": len(sys.path)
        })
    
    # Crear __init__.py si no existen (siguiendo REGLA #3: Arquitectura Enterprise)
    init_files_created = []
    
    if not (core_dir / "__init__.py").exists() and core_dir.exists():
        (core_dir / "__init__.py").write_text('"""Core module for ICT Engine v6.1.0"""\n')
        init_files_created.append("core/__init__.py")
    
    if not (sistema_dir / "__init__.py").exists() and sistema_dir.exists():
        (sistema_dir / "__init__.py").write_text('"""Sistema SIC v3.1"""\n')
        init_files_created.append("sistema/__init__.py")
    
    # Verificar subdirectorios críticos
    critical_dirs = [
        core_dir / "analysis",
        core_dir / "data_management", 
        core_dir / "ict_engine",
        core_dir / "smart_money_concepts"
    ]
    
    for dir_path in critical_dirs:
        if dir_path.exists() and not (dir_path / "__init__.py").exists():
            (dir_path / "__init__.py").write_text(f'"""{dir_path.name} module"""\n')
            init_files_created.append(f"{dir_path.relative_to(project_root)}/__init__.py")
    
    if init_files_created:
        log_trading_decision_smart_v6("INIT_FILES_CREATED", {
            "files": init_files_created,
            "count": len(init_files_created)
        })
    
    # Verificar imports críticos
    import_tests = {}
    
    try:
        from core.analysis.market_context import MarketContext
        import_tests["MarketContext"] = True
    except ImportError as e:
        import_tests["MarketContext"] = str(e)
    
    try:
        from core.analysis.ict_historical_analyzer import ICTHistoricalAnalyzer
        import_tests["ICTHistoricalAnalyzer"] = True
    except ImportError as e:
        import_tests["ICTHistoricalAnalyzer"] = str(e)
    
    try:
        from core.smart_trading_logger import TradingDecisionCacheV6
        import_tests["TradingDecisionCacheV6"] = True
    except ImportError as e:
        import_tests["TradingDecisionCacheV6"] = str(e)
    
    log_trading_decision_smart_v6("IMPORT_VERIFICATION", import_tests)
    
    # Resultado final
    success = all(result == True for result in import_tests.values())
    
    log_trading_decision_smart_v6("SETUP_COMPLETE", {
        "success": success,
        "imports_working": sum(1 for r in import_tests.values() if r == True),
        "total_imports": len(import_tests),
        "project_root": str(project_root)
    })
    
    return success, project_root, import_tests

def run_migration_test_with_fixed_imports():
    """
    Ejecuta el test de migración con imports arreglados
    
    ✅ REGLA #4: SIC y SLUC obligatorio
    """
    
    log_trading_decision_smart_v6("TEST_EXECUTION_START", {
        "test": "test_migration_phase1.py",
        "purpose": "Verificar migración Fase 1 con imports arreglados"
    })
    
    # Configurar paths
    success, project_root, import_results = setup_python_path()
    
    if not success:
        log_trading_decision_smart_v6("TEST_EXECUTION_ERROR", {
            "error": "Imports no funcionan correctamente",
            "import_results": import_results
        })
        return False
    
    # Importar y ejecutar test
    try:
        # Cambiar al directorio del proyecto
        original_cwd = os.getcwd()
        os.chdir(str(project_root))
        
        # Importar el módulo de test
        sys.path.insert(0, str(project_root / "tests"))
        import test_migration_phase1
        
        # Ejecutar test principal
        test_migration_phase1.main()
        
        log_trading_decision_smart_v6("TEST_EXECUTION_SUCCESS", {
            "test_completed": True,
            "cwd_restored": True
        })
        
        return True
        
    except Exception as e:
        log_trading_decision_smart_v6("TEST_EXECUTION_FAILED", {
            "error": str(e),
            "error_type": type(e).__name__
        })
        return False
        
    finally:
        # Restaurar directorio original
        os.chdir(original_cwd)

def main():
    """
    Main function siguiendo REGLAS COPILOT
    
    ✅ REGLA #1: Revisar antes de crear
    ✅ REGLA #4: SIC y SLUC obligatorio
    """
    
    print("🔧 ARREGLO DE IMPORTS - REGLAS COPILOT v6.0")
    print("=" * 60)
    
    # ✅ REGLA #4: Verificar SIC system ready (si está disponible)
    if SIC_AVAILABLE:
        sic = SICBridge()
        if not sic.is_system_ready():
            log_trading_decision_smart_v6("SIC_WARNING", {
                "warning": "SIC system not ready",
                "continuing": "with manual setup"
            })
    
    # Ejecutar arreglo y test
    success = run_migration_test_with_fixed_imports()
    
    if success:
        print("\n✅ IMPORTS ARREGLADOS Y TEST EJECUTADO")
        print("🚀 Fase 1 migración verificada correctamente")
    else:
        print("\n❌ PROBLEMAS DETECTADOS")
        print("🔧 Revisar logs para más detalles")

if __name__ == "__main__":
    main()
