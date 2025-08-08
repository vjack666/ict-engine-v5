"""
SIC v3.1 Enterprise - Sistema de Imports Inteligente
===================================================

Paquete principal del Sistema de Imports Inteligente v3.1 Enterprise.

Este paquete proporciona capacidades avanzadas de gestión de imports:
- Lazy Loading Inteligente
- Caché Predictivo
- Monitoreo en Tiempo Real
- Debug Avanzado
- Interface Enterprise

Autor: ICT Engine v6.1.0 Team
Versión: v3.1.0-enterprise
Fecha: Agosto 2025
"""

__version__ = "3.1.0-enterprise"
__author__ = "ICT Engine v6.1.0 Team"

# Imports principales del SIC v3.1
from .enterprise_interface import SICv31Enterprise, get_sic_instance, smart_import, sic_import
from .lazy_loading import LazyLoadingManager, LazyModuleProxy
from .predictive_cache import PredictiveCacheManager, ModuleCacheEntry
from .monitor_dashboard import MonitorDashboard, ImportEvent, SystemMetrics
from .advanced_debug import AdvancedDebugger, DebugEvent, DependencyAnalyzer

# Interface principal para el resto del sistema
__all__ = [
    # Interface principal
    'SICv31Enterprise',
    'get_sic_instance', 
    'smart_import',
    'sic_import',
    
    # Componentes principales
    'LazyLoadingManager',
    'PredictiveCacheManager',
    'MonitorDashboard',
    'AdvancedDebugger',
    
    # Clases auxiliares
    'LazyModuleProxy',
    'ModuleCacheEntry',
    'ImportEvent',
    'SystemMetrics',
    'DebugEvent',
    'DependencyAnalyzer',
    
    # Metadata
    '__version__',
    '__author__'
]

# Configuración por defecto del SIC v3.1
DEFAULT_CONFIG = {
    'lazy_loading': {
        'max_memory_mb': 1024,
        'enable_memory_monitoring': True,
        'lazy_threshold_mb': 50,
        'always_lazy': [
            'pandas', 'numpy', 'matplotlib', 'plotly', 'seaborn',
            'scipy', 'sklearn', 'tensorflow', 'torch', 'cv2'
        ]
    },
    'predictive_cache': {
        'max_cache_size_mb': 256,
        'max_entries': 100,
        'prediction_threshold': 0.5,
        'enable_persistence': True,
        'persistence_file': 'sic_cache_stats.json'
    },
    'monitor': {
        'enable_continuous_monitoring': True,
        'metrics_interval_seconds': 8,
        'alerts': {
            'memory_threshold_mb': 512,
            'slow_import_threshold_s': 2.0,
            'cache_miss_rate_threshold': 80,
            'failure_rate_threshold': 20
        }
    },
    'debug': {
        'debug_level': 'info',
        'enable_detailed_logging': True,
        'max_events': 1000
    }
}


def initialize_sic(config=None):
    """
    🚀 Inicializa el SIC v3.1 Enterprise con configuración personalizada
    
    Args:
        config: Configuración personalizada (opcional)
        
    Returns:
        Instancia del SIC v3.1 Enterprise inicializada
        
    Example:
        # Inicialización básica
        sic = initialize_sic()
        
        # Inicialización con configuración personalizada
        custom_config = {
            'lazy_loading': {'max_memory_mb': 2048},
            'debug': {'debug_level': 'debug'}
        }
        sic = initialize_sic(custom_config)
    """
    # Combinar configuración por defecto con la personalizada
    final_config = DEFAULT_CONFIG.copy()
    
    if config:
        # Merge deep de configuraciones
        for category, settings in config.items():
            if category in final_config:
                final_config[category].update(settings)
            else:
                final_config[category] = settings
    
    # Crear instancia del SIC v3.1
    sic_instance = SICv31Enterprise(final_config)
    
    print(f"🚀 SIC v3.1 Enterprise inicializado (versión: {__version__})")
    return sic_instance


def get_version_info():
    """
    📋 Obtiene información detallada de la versión
    
    Returns:
        Diccionario con información de versión y componentes
    """
    return {
        'version': __version__,
        'author': __author__,
        'components': {
            'lazy_loading': 'Gestión inteligente de carga diferida',
            'predictive_cache': 'Caché predictivo con ML básico',
            'monitor_dashboard': 'Monitoreo en tiempo real',
            'advanced_debug': 'Debug enterprise-level',
            'enterprise_interface': 'API unificada enterprise'
        },
        'features': [
            'Lazy Loading Inteligente',
            'Caché Predictivo',
            'Monitoreo en Tiempo Real',
            'Debug Avanzado',
            'Alertas Automáticas',
            'Análisis de Dependencias',
            'Reportes Detallados',
            'Interface Enterprise'
        ],
        'requirements': {
            'python': '>=3.11',
            'psutil': '>=5.9.0'
        }
    }


def quick_test():
    """
    🧪 Test rápido del SIC v3.1 Enterprise
    
    Ejecuta un test básico de todos los componentes principales.
    """
    print("🧪 Ejecutando quick test del SIC v3.1 Enterprise...")
    
    try:
        # Test 1: Inicialización
        print("1️⃣ Test de inicialización...")
        sic = get_sic_instance()
        print("   ✅ SIC inicializado correctamente")
        
        # Test 2: Smart import
        print("2️⃣ Test de smart import...")
        sys_module = smart_import('sys')
        print(f"   ✅ Smart import exitoso: {type(sys_module)}")
        
        # Test 3: Estadísticas
        print("3️⃣ Test de estadísticas...")
        stats = sic.get_system_stats()
        print(f"   ✅ Estadísticas obtenidas: {stats['imports_stats']['total_imports']} imports")
        
        # Test 4: Lazy loading
        print("4️⃣ Test de lazy loading...")
        os_module = smart_import('os', priority='low')  # Forzar lazy
        print("   ✅ Lazy loading test completado")
        
        print("🎯 Quick test completado exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en quick test: {e}")
        import traceback
        traceback.print_exc()
        return False


# Inicialización automática al importar el paquete
try:
    # Verificar si psutil está disponible
    import psutil
    _PSUTIL_AVAILABLE = True
except ImportError:
    _PSUTIL_AVAILABLE = False
    print("⚠️ [SIC v3.1] psutil no disponible, algunas funciones estarán limitadas")

# Banner de bienvenida
print("🚀 SIC v3.1 Enterprise - Sistema de Imports Inteligente")
print(f"   Versión: {__version__}")
print(f"   Componentes: Lazy Loading, Predictive Cache, Monitor, Debug")
print(f"   psutil: {'✅' if _PSUTIL_AVAILABLE else '❌'}")


if __name__ == "__main__":
    # Ejecutar quick test si el módulo se ejecuta directamente
    print("Ejecutando desde __main__...")
    version_info = get_version_info()
    print(f"Información de versión: {version_info}")
    
    quick_test()
