"""
Sistema Core - ICT Engine v6.0 Enterprise
=========================================

Módulo principal del sistema que contiene todos los componentes core
del ICT Engine v6.0 Enterprise, incluyendo el SIC v3.1 y SLUC v2.1.

Componentes:
- SIC v3.1 Enterprise: Sistema de Imports Inteligente
- SLUC v2.1: Sistema de Logging Universal Centralizado

Autor: ICT Engine v6.0 Team
Versión: v6.0.0-enterprise
Fecha: Agosto 2025
"""

__version__ = "6.0.0-enterprise"

# Import del SIC v3.1 Enterprise
from .sic_v3_1 import (
    SICv31Enterprise,
    get_sic_instance,
    smart_import,
    sic_import,
    initialize_sic,
    get_version_info as get_sic_version_info,
    quick_test as sic_quick_test
)

# Import del SLUC v2.1 (cuando esté implementado)
# from .logging_interface import LoggingInterface, setup_logging

__all__ = [
    # SIC v3.1 Enterprise
    'SICv31Enterprise',
    'get_sic_instance',
    'smart_import',
    'sic_import',
    'initialize_sic',
    'get_sic_version_info',
    'sic_quick_test',
    
    # Funciones de utilidad del sistema
    'get_system_info',
    'system_quick_test',
    
    # Metadata
    '__version__'
]


def get_system_info():
    """
    📋 Obtiene información completa del sistema
    
    Returns:
        Diccionario con información de todos los componentes
    """
    info = {
        'system_version': __version__,
        'components': {
            'sic_v3_1': get_sic_version_info(),
            # 'sluc_v2_1': get_sluc_version_info(),  # Cuando esté implementado
        },
        'status': 'operational'
    }
    
    return info


def system_quick_test():
    """
    🧪 Test rápido de todo el sistema
    
    Ejecuta tests de todos los componentes principales.
    
    Returns:
        True si todos los tests pasan
    """
    print("🧪 Ejecutando test completo del sistema...")
    
    all_passed = True
    
    # Test SIC v3.1
    print("\n🚀 Testing SIC v3.1 Enterprise...")
    try:
        sic_result = sic_quick_test()
        if sic_result:
            print("✅ SIC v3.1 Enterprise: PASSED")
        else:
            print("❌ SIC v3.1 Enterprise: FAILED")
            all_passed = False
    except Exception as e:
        print(f"❌ SIC v3.1 Enterprise: ERROR - {e}")
        all_passed = False
    
    # Test SLUC v2.1 (cuando esté implementado)
    # print("\n📝 Testing SLUC v2.1...")
    # try:
    #     sluc_result = sluc_quick_test()
    #     if sluc_result:
    #         print("✅ SLUC v2.1: PASSED")
    #     else:
    #         print("❌ SLUC v2.1: FAILED")
    #         all_passed = False
    # except Exception as e:
    #     print(f"❌ SLUC v2.1: ERROR - {e}")
    #     all_passed = False
    
    # Resultado final
    print(f"\n{'🎯 Todos los tests PASSED!' if all_passed else '⚠️ Algunos tests FAILED!'}")
    return all_passed


# Banner del sistema
print("🏗️ ICT Engine v6.0 Enterprise - Sistema Core")
print(f"   Versión: {__version__}")
print("   Componentes: SIC v3.1, SLUC v2.1 (próximamente)")


if __name__ == "__main__":
    # Ejecutar test completo del sistema
    print("Ejecutando desde sistema/__main__...")
    system_info = get_system_info()
    print(f"Sistema info: {system_info}")
    
    system_quick_test()
