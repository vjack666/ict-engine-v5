"""
Smart Import System v3.1 Enterprise
Sistema inteligente de importación para ICT Engine v6.1.0

Características:
- Importación condicional y lazy loading
- Detección automática de dependencias
- Fallbacks inteligentes
- Gestión de errores robusta
"""

import sys
import importlib
import importlib.util
from typing import Any, Optional, Dict, List, Union
from pathlib import Path
import warnings
from utils.smart_trading_logger import SmartTradingLogger

class SmartImporter:
    """
    Sistema de importación inteligente para ICT Engine v6.1.0
    """
    
    def __init__(self):
        """Inicializar el smart importer"""
        self.logger = SmartTradingLogger()
        self.imported_modules = {}
        self.failed_imports = set()
        self.import_cache = {}
        
    def smart_import(self, module_name: str, fallback: Optional[str] = None, 
                    optional: bool = False) -> Optional[Any]:
        """
        Importar módulo de forma inteligente con fallbacks
        
        Args:
            module_name: Nombre del módulo a importar
            fallback: Módulo de fallback si falla la importación
            optional: Si es True, no genera error si falla
            
        Returns:
            Módulo importado o None si falla
        """
        # Verificar cache
        if module_name in self.import_cache:
            return self.import_cache[module_name]
            
        # Verificar si ya falló antes
        if module_name in self.failed_imports and not fallback:
            return None
            
        try:
            # Intentar importación
            module = importlib.import_module(module_name)
            self.import_cache[module_name] = module
            self.imported_modules[module_name] = module
            self.logger.debug(f"✅ Importado: {module_name}")
            return module
            
        except ImportError as e:
            self.failed_imports.add(module_name)
            
            if fallback:
                self.logger.warning(f"⚠️ Fallo {module_name}, usando fallback {fallback}")
                return self.smart_import(fallback, optional=True)
                
            if optional:
                self.logger.debug(f"🔍 Importación opcional falló: {module_name}")
                return None
                
            self.logger.error(f"❌ Error importando {module_name}: {e}")
            return None
    
    def conditional_import(self, module_name: str, condition_func: callable) -> Optional[Any]:
        """
        Importar módulo solo si se cumple una condición
        
        Args:
            module_name: Módulo a importar
            condition_func: Función que determina si importar
            
        Returns:
            Módulo o None
        """
        try:
            if condition_func():
                return self.smart_import(module_name)
            else:
                self.logger.debug(f"🚫 Condición no cumplida para: {module_name}")
                return None
        except Exception as e:
            self.logger.error(f"❌ Error en condición para {module_name}: {e}")
            return None
    
    def lazy_import(self, module_name: str):
        """
        Crear un wrapper para importación lazy
        
        Args:
            module_name: Módulo a importar de forma lazy
            
        Returns:
            Wrapper que importa cuando se accede
        """
        class LazyModule:
            def __init__(self, name, importer):
                self._module_name = name
                self._importer = importer
                self._module = None
                
            def __getattr__(self, attr):
                if self._module is None:
                    self._module = self._importer.smart_import(self._module_name)
                    if self._module is None:
                        raise ImportError(f"No se pudo importar {self._module_name}")
                return getattr(self._module, attr)
                
        return LazyModule(module_name, self)
    
    def import_from_path(self, file_path: str, module_name: Optional[str] = None) -> Optional[Any]:
        """
        Importar módulo desde una ruta específica
        
        Args:
            file_path: Ruta al archivo del módulo
            module_name: Nombre opcional del módulo
            
        Returns:
            Módulo importado o None
        """
        try:
            path = Path(file_path)
            if not path.exists():
                self.logger.error(f"❌ Archivo no encontrado: {file_path}")
                return None
                
            if module_name is None:
                module_name = path.stem
                
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None:
                self.logger.error(f"❌ No se pudo crear spec para: {file_path}")
                return None
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            self.import_cache[module_name] = module
            self.imported_modules[module_name] = module
            self.logger.debug(f"✅ Importado desde path: {file_path}")
            return module
            
        except Exception as e:
            self.logger.error(f"❌ Error importando desde {file_path}: {e}")
            return None
    
    def check_dependencies(self, dependencies: List[str]) -> Dict[str, bool]:
        """
        Verificar disponibilidad de dependencias
        
        Args:
            dependencies: Lista de módulos a verificar
            
        Returns:
            Dict con el estado de cada dependencia
        """
        results = {}
        for dep in dependencies:
            try:
                importlib.import_module(dep)
                results[dep] = True
            except ImportError:
                results[dep] = False
                
        return results
    
    def get_import_report(self) -> Dict[str, Any]:
        """
        Obtener reporte de importaciones
        
        Returns:
            Reporte completo de importaciones
        """
        return {
            'imported_modules': list(self.imported_modules.keys()),
            'failed_imports': list(self.failed_imports),
            'cache_size': len(self.import_cache),
            'total_imports': len(self.imported_modules)
        }

# Instancia global del smart importer
_smart_importer = SmartImporter()

def smart_import(module_name: str, fallback: Optional[str] = None, optional: bool = False):
    """Función de conveniencia para importación inteligente"""
    return _smart_importer.smart_import(module_name, fallback, optional)

def lazy_import(module_name: str):
    """Función de conveniencia para importación lazy"""
    return _smart_importer.lazy_import(module_name)

def conditional_import(module_name: str, condition_func: callable):
    """Función de conveniencia para importación condicional"""
    return _smart_importer.conditional_import(module_name, condition_func)

def check_dependencies(dependencies: List[str]) -> Dict[str, bool]:
    """Función de conveniencia para verificar dependencias"""
    return _smart_importer.check_dependencies(dependencies)

def get_import_report() -> Dict[str, Any]:
    """Función de conveniencia para obtener reporte"""
    return _smart_importer.get_import_report()

# Importaciones críticas para ICT Engine
try:
    # MT5 - Crítico para el sistema
    mt5 = smart_import('MetaTrader5', optional=True)
    
    # Pandas y NumPy - Esenciales
    pd = smart_import('pandas', optional=False)
    np = smart_import('numpy', optional=False)
    
    # Matplotlib - Para gráficos
    plt = smart_import('matplotlib.pyplot', optional=True)
    
    # TA-Lib - Para análisis técnico
    talib = smart_import('talib', optional=True)
    
    # Warnings management
    if talib is None:
        warnings.warn("TA-Lib no disponible, usando implementaciones nativas", UserWarning)
        
except Exception as e:
    logger = SmartTradingLogger()
    logger.error(f"❌ Error en importaciones críticas: {e}")
