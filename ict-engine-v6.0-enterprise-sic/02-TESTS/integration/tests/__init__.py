"""
Tests - ICT Engine v6.1.0 Enterprise SIC
======================================

Suite de tests para el ICT Engine v6.1.0 Enterprise y el
Sistema de Imports Inteligente (SIC) v3.1.

Esta carpeta contiene todos los tests del proyecto:
- Tests unitarios de componentes individuales
- Tests de integración del sistema completo
- Tests de performance y benchmarks
- Tests de regresión

Estructura de tests:
- test_sic_complete.py: Test suite completo
- test_lazy_loading.py: Tests específicos de lazy loading
- test_predictive_cache.py: Tests del caché predictivo
- test_monitor_dashboard.py: Tests del dashboard de monitoreo
- test_advanced_debug.py: Tests del debugger avanzado

Autor: ICT Engine v6.1.0 Team
Versión: v6.1.0-enterprise
Fecha: Agosto 2025
"""

__version__ = "6.0.0-enterprise"
__author__ = "ICT Engine v6.1.0 Team"

import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al path para imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Metadata de tests
TEST_INFO = {
    'version': __version__,
    'author': __author__,
    'test_types': [
        'unit_tests',
        'integration_tests',
        'performance_tests',
        'regression_tests'
    ],
    'components_tested': [
        'SIC v3.1 Enterprise Interface',
        'Lazy Loading Manager',
        'Predictive Cache Manager',
        'Monitor Dashboard',
        'Advanced Debugger'
    ]
}


def run_all_tests():
    """
    🧪 Ejecuta todos los tests del proyecto
    
    Returns:
        True si todos los tests pasan
    """
    print("🧪 Ejecutando todos los tests del ICT Engine v6.1.0 Enterprise...")
    
    try:
        # Importar y ejecutar el test principal
        from .test_sic_complete import main as run_complete_tests
        
        result = run_complete_tests()
        
        if result:
            print("✅ Todos los tests del proyecto han pasado!")
        else:
            print("❌ Algunos tests han fallado.")
        
        return result
        
    except Exception as e:
        print(f"❌ Error ejecutando tests: {e}")
        return False


def get_test_info():
    """
    📋 Obtiene información sobre los tests disponibles
    
    Returns:
        Diccionario con información de tests
    """
    return TEST_INFO


# Banner de la suite de tests
print("🧪 ICT Engine v6.1.0 Enterprise - Test Suite")
print(f"   Versión: {__version__}")
print("   Componentes: SIC v3.1, SLUC v2.1 (próximamente)")


if __name__ == "__main__":
    # Ejecutar todos los tests si se ejecuta directamente
    print("Ejecutando todos los tests...")
    success = run_all_tests()
    sys.exit(0 if success else 1)
