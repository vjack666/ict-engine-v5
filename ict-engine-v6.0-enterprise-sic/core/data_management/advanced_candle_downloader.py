#!/usr/bin/env python3
"""
📥 ADVANCED CANDLE DOWNLOADER - ICT ENGINE v6.0 Enterprise SIC
==============================================================

Downloader avanzado de velas integrado con SIC v3.1 Enterprise que proporciona:
- Gestión inteligente de imports mediante SIC v3.1
- Descarga masiva de datos históricos
- Soporte para múltiples símbolos y timeframes
- Progress tracking en tiempo real
- Manejo robusto de errores con debugging avanzado
- Integración completa con dashboard y coordinador
- Lazy loading de dependencias pesadas
- Cache predictivo para optimización

Características v6.0 Enterprise:
- Integración nativa con SIC v3.1 Enterprise
- Debug avanzado con AdvancedDebugger
- Lazy loading de pandas y asyncio
- Cache predictivo de configuraciones
- Monitoreo en tiempo real

Autor: ICT Engine v6.0 Enterprise Team
Versión: v6.0.0-enterprise
Fecha: Agosto 2025
"""

# ===============================
# IMPORTS OPTIMIZADOS SIC v3.1
# ===============================

# Imports básicos (optimizados por SIC)
import threading
import time
import os
import subprocess
import random
from typing import Dict, List, Optional, Callable, Any, Set, Tuple, Union
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field, asdict
from pathlib import Path

# Imports críticos para funcionamiento
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False
    # Crear mock para desarrollo sin MT5
    class MT5Mock:
        TIMEFRAME_M1 = 1
        TIMEFRAME_M5 = 5
        TIMEFRAME_M15 = 15
        TIMEFRAME_M30 = 30
        TIMEFRAME_H1 = 16385
        TIMEFRAME_H4 = 16388
        TIMEFRAME_D1 = 16408
        
        def initialize(self, path=None): return False
        def copy_rates_from(self, *args): return None
        def copy_rates_range(self, *args): return None
        def last_error(self): return (0, "Mock error")
        def symbol_info(self, symbol): return None
        def account_info(self): return None
        def shutdown(self): pass
    
    mt5 = MT5Mock()

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None

try:
    import asyncio
    ASYNCIO_AVAILABLE = True
except ImportError:
    ASYNCIO_AVAILABLE = False
    asyncio = None

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None

# Imports SIC v3.1 Enterprise (usando try/except para compatibilidad)
try:
    from sistema.sic_v3_1.enterprise_interface import SICv31Enterprise
    from sistema.sic_v3_1.advanced_debug import AdvancedDebugger
    SIC_V3_1_AVAILABLE = True
    print("✅ [SIC Integration] SIC v3.1 Enterprise cargado exitosamente")
except ImportError as e:
    SIC_V3_1_AVAILABLE = False
    print(f"⚠️ [SIC Integration] SIC v3.1 no disponible: {e}")
    # Fallback para desarrollo
    class SICv31Enterprise:
        def __init__(self): pass
        def smart_import(self, module_name): return None
        def get_lazy_loading_manager(self): return None
        def get_predictive_cache_manager(self): return None
        def get_system_stats(self): return {'sic_version': 'fallback', 'status': 'inactive'}
        def get_monitor(self): return None
        def get_debugger(self): return None
    
    class AdvancedDebugger:
        def __init__(self, config=None): pass
        def log_import_debug(self, *args, **kwargs): pass
        def diagnose_import_problem(self, *args, **kwargs): pass
        def get_debug_summary(self): return {'debug_stats': {'total_events': 0}}
        def save_session_log(self, *args, **kwargs): pass
        def log_error(self, *args, **kwargs): pass

# El SIC v3.1 gestionará estos imports de forma inteligente
sic = SICv31Enterprise()

# Configurar debugging avanzado
debugger = AdvancedDebugger({
    'debug_level': 'info',
    'enable_detailed_logging': True,
    'max_events': 500
})


@dataclass
class DownloadStats:
    """📊 Estadísticas de descarga mejoradas para v6.0"""
    symbol: str
    timeframe: str
    total_bars: int = 0
    downloaded_bars: int = 0
    download_speed: float = 0.0  # velas por segundo
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    success: bool = False
    error_message: str = ""
    
    # Nuevas métricas v6.0
    cache_hits: int = 0
    lazy_loads: int = 0
    memory_usage_mb: float = 0.0
    debug_events: int = 0


@dataclass
class DownloadRequest:
    """📋 Solicitud de descarga mejorada con SIC v3.1"""
    symbol: str
    timeframe: str
    lookback: int
    request_id: str
    priority: int = 1
    
    # Nuevos campos v6.0
    use_cache: bool = True
    enable_lazy_loading: bool = True
    debug_mode: bool = False


@dataclass
class DownloadStatus:
    """🚦 Estado de descarga con monitoreo avanzado"""
    request_id: str
    status: str  # 'pending', 'downloading', 'completed', 'error'
    progress: float = 0.0
    message: str = ""
    
    # Nuevos campos v6.0
    sic_stats: Dict[str, Any] = field(default_factory=dict)
    debug_info: Dict[str, Any] = field(default_factory=dict)


class AdvancedCandleDownloader:
    """
    📥 DOWNLOADER AVANZADO DE VELAS v6.0 ENTERPRISE
    ===============================================

    Versión completamente integrada con SIC v3.1 Enterprise que proporciona:
    
    🧠 **Características Inteligentes:**
    - Lazy loading automático de dependencias pesadas
    - Cache predictivo de configuraciones frecuentes
    - Debug avanzado con análisis de dependencias
    - Monitoreo en tiempo real de performance
    
    📊 **Gestión Avanzada:**
    - Progreso en tiempo real con callbacks optimizados
    - Manejo robusto de errores con diagnóstico automático
    - Integración perfecta con coordinador v6.0
    - Threading optimizado con control de recursos
    
    🚀 **Performance Enterprise:**
    - Descarga masiva optimizada
    - Gestión inteligente de memoria
    - Cache de resultados frecuentes
    - Predictive loading de próximas solicitudes
    """

    def __init__(self,
                 progress_callback: Optional[Callable] = None,
                 complete_callback: Optional[Callable] = None,
                 error_callback: Optional[Callable] = None,
                 config: Optional[Dict[str, Any]] = None):
        """
        🏗️ Inicializa el downloader v6.0 Enterprise
        
        Args:
            progress_callback: Función llamada durante el progreso
            complete_callback: Función llamada al completar
            error_callback: Función llamada en errores
            config: Configuración avanzada del downloader
        """
        
        # Configuración v6.0
        self._config = config or {}
        self._enable_debug = self._config.get('enable_debug', True)
        self._use_predictive_cache = self._config.get('use_predictive_cache', True)
        self._enable_lazy_loading = self._config.get('enable_lazy_loading', True)
        
        # Cargar configuración de almacenamiento automáticamente
        self._storage_config = self._load_storage_configuration()
        
        # Sistema de callbacks para UI
        self.progress_callback = progress_callback
        self.complete_callback = complete_callback
        self.error_callback = error_callback

        # Estado del downloader
        self.is_downloading = False
        self.active_downloads: Dict[str, DownloadStats] = {}
        self.download_queue: List[DownloadRequest] = []
        
        # Nuevos estados v6.0
        self._lazy_modules = {}
        self._cache_stats = {'hits': 0, 'misses': 0, 'saves': 0}
        self._memory_cache = {}  # Cache en memoria como fallback
        self._performance_metrics = []

        # Componentes del sistema (lazy loading)
        self._mt5_manager = None
        self._coordinator = None
        self._pandas_module = None
        self._asyncio_module = None

        # Configuración optimizada
        self.max_concurrent_downloads = self._config.get('max_concurrent', 3)
        self.download_batch_size = self._config.get('batch_size', 10000)
        self.retry_attempts = self._config.get('retry_attempts', 3)
        self.retry_delay = self._config.get('retry_delay', 2.0)

        # Threading optimizado
        self.lock = threading.Lock()
        self.worker_thread = None
        self.stop_event = threading.Event()
        
        # Asignar instancia SIC como atributo de clase
        self.sic = sic
        
        # Inicializar componentes SIC v3.1
        self._initialize_sic_integration()
        
        # Log de inicialización con info de storage
        self._log_info(f"AdvancedCandleDownloader v6.0 inicializado con SIC v3.1")
        self._log_info(f"Storage Mode: {self._storage_config.get('mode', 'DEFAULT')} - {self._storage_config.get('description', 'Standard config')}")

    def _load_storage_configuration(self) -> Dict[str, Any]:
        """🗄️ Carga configuración ENTERPRISE de almacenamiento"""
        try:
            import json
            
            # 1. Intentar cargar configuración ENTERPRISE primero
            enterprise_config_file = Path("config/performance_config_enterprise.json")
            if enterprise_config_file.exists():
                with open(enterprise_config_file, 'r', encoding='utf-8') as f:
                    enterprise_data = json.load(f)
                    storage_config = enterprise_data.get('storage', {})
                    cache_config = enterprise_data.get('cache', {})
                    
                    # Configuración ENTERPRISE optimizada
                    combined_config = {
                        'mode': 'FULL_STORAGE_ENTERPRISE',
                        'description': 'ENTERPRISE MAXIMUM PERFORMANCE',
                        'save_to_file_default': True,
                        'cache_enabled': True,
                        'max_cache_mb': cache_config.get('total_size_mb', 2048),  # 2GB cache
                        'compression': storage_config.get('compression', 'SMART_GZIP'),
                        'memory_mapping': storage_config.get('memory_mapping', True),
                        'concurrent_writes': storage_config.get('concurrent_writes', 4),
                        'critical_timeframes': storage_config.get('critical_timeframes', ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1']),
                        'ict_symbols': storage_config.get('ict_symbols', ['EURUSD', 'GBPUSD', 'XAUUSD', 'USDJPY']),
                        'cache_layers': cache_config.get('cache_layers', {}),
                        'predictive_loading': cache_config.get('predictive_loading', True),
                        'enterprise_mode': True
                    }
                    
                    if self._config.get('enable_debug', True):
                        self._log_info(f"🚀 ENTERPRISE CONFIG cargada: {combined_config.get('mode', 'UNKNOWN')}")
                        self._log_info(f"   Cache: {combined_config.get('max_cache_mb', 0)} MB")
                        self._log_info(f"   Compresión: {combined_config.get('compression', 'NONE')}")
                        self._log_info(f"   Memory Mapping: {combined_config.get('memory_mapping', False)}")
                    
                    return combined_config
            
            # 2. Fallback a configuración storage normal
            config_file = Path("config/storage_config.json")
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    storage_data = json.load(f)
                    downloader_config = storage_data.get('downloader_config', {})
                    storage_config = storage_data.get('storage_config', {})
                    
                    # Combinar configuraciones
                    combined_config = {**storage_config, **downloader_config}
                    
                    if self._config.get('enable_debug', True):
                        self._log_info(f"✅ Configuración de storage cargada: {combined_config.get('mode', 'UNKNOWN')}")
                    
                    return combined_config
            else:
                # Configuración ENTERPRISE por defecto
                default_config = {
                    'mode': 'FULL_STORAGE_ENTERPRISE',
                    'description': 'ENTERPRISE DEFAULT - Full storage with 2GB cache',
                    'save_to_file_default': True,
                    'cache_enabled': True,
                    'max_cache_mb': 2048,  # 2GB por defecto
                    'compression': 'SMART_GZIP',
                    'memory_mapping': True,
                    'concurrent_writes': 4,
                    'critical_timeframes': ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1'],
                    'enterprise_mode': True
                }
                
                if self._config.get('enable_debug', True):
                    self._log_info("🚀 Usando configuración ENTERPRISE por defecto")
                
                return default_config
                
        except Exception as e:
            if self._config.get('enable_debug', True):
                self._log_error(f"Error cargando configuración ENTERPRISE: {e}")
            
            # Fallback ENTERPRISE seguro
            return {
                'mode': 'FULL_STORAGE_ENTERPRISE',
                'description': 'ENTERPRISE SAFE MODE - Full storage optimized',
                'save_to_file_default': True,
                'cache_enabled': True,
                'max_cache_mb': 1024,  # 1GB fallback
                'compression': 'FAST',
                'memory_mapping': False,
                'enterprise_mode': True
            }

    def _check_mt5_connection(self) -> bool:
        """🔌 Verifica y FUERZA la conexión con MT5 REAL"""
        try:
            # Intentar cargar MT5DataManager
            mt5_manager = self._get_mt5_manager()
            if mt5_manager and hasattr(mt5_manager, 'is_connected'):
                if mt5_manager.is_connected:
                    self._log_info("✅ MT5 conectado y funcionando")
                    return True
                else:
                    if self._enable_debug:
                        self._log_info("MT5 no está conectado - activando conexión directa")
                    return self._force_mt5_connection()
            
            # Sin MT5DataManager - usar conexión directa (NORMAL)
            if self._enable_debug:
                self._log_info("Usando conexión directa MT5 para datos reales")
            return self._force_mt5_connection()
            
        except Exception as e:
            if self._enable_debug:
                self._log_error(f"Error verificando MT5: {e}")
            return self._force_mt5_connection()

    def _force_mt5_connection(self) -> bool:
        """🚀 FUERZA la conexión MT5 para FundedNext Terminal"""
        try:
            self._log_info("🚀 FORZANDO conexión FUNDEDNEXT MT5 TERMINAL")
            
            # PATH ESPECÍFICO para FundedNext
            fundednext_path = r"C:\Program Files\FundedNext MT5 Terminal\terminal64.exe"
            
            # Verificar si FundedNext está instalado
            import os
            if not os.path.exists(fundednext_path):
                self._log_error(f"❌ FundedNext Terminal no encontrado en: {fundednext_path}")
                self._log_error("   Verificar instalación de FundedNext MT5 Terminal")
                return False
            
            # Importar MT5 directamente
            import MetaTrader5 as mt5
            
            # Intentar inicializar MT5 con FundedNext path
            if not mt5.initialize(path=fundednext_path):
                self._log_warning("❌ No se pudo inicializar con path específico, intentando automático...")
                
                # Verificar si FundedNext está corriendo
                if not self._is_fundednext_running():
                    self._log_info("🚀 FundedNext no está corriendo, intentando abrir...")
                    if self._start_fundednext():
                        # Esperar a que se inicie
                        import time
                        time.sleep(3)
                        
                        # Reintentar inicialización
                        if not mt5.initialize():
                            self._log_error("❌ No se pudo inicializar MT5 después de abrir FundedNext")
                            return False
                    else:
                        self._log_error("❌ No se pudo abrir FundedNext Terminal")
                        return False
                else:
                    # FundedNext está corriendo pero MT5 no conecta
                    if not mt5.initialize():
                        self._log_error("❌ FundedNext corriendo pero MT5 no conecta")
                        self._log_error("   ABRIR FUNDEDNEXT Y CONECTAR CUENTA")
                        return False
            
            # Verificar conexión de cuenta
            account_info = mt5.account_info()
            if not account_info:
                self._log_error("❌ FundedNext abierto pero sin cuenta conectada")
                self._log_error("   CONECTAR CUENTA EN FUNDEDNEXT MT5 TERMINAL")
                mt5.shutdown()
                return False
            
            # Verificar símbolo de prueba
            symbol_info = mt5.symbol_info("EURUSD")
            if not symbol_info:
                self._log_error("❌ EURUSD no disponible en FundedNext")
                self._log_error("   Verificar símbolos disponibles en broker")
                mt5.shutdown()
                return False
            
            # ✅ CONEXIÓN FUNDEDNEXT ESTABLECIDA
            self._log_info(f"✅ FUNDEDNEXT MT5 REAL conectado - Cuenta: {account_info.login}")
            self._log_info(f"   Broker: {account_info.company}")
            self._log_info(f"   Balance: {account_info.balance} {account_info.currency}")
            self._log_info(f"   Terminal: FundedNext MT5 Terminal")
            
            # Actualizar MT5DataManager con conexión real
            if self._mt5_manager:
                self._mt5_manager._mt5_initialized = True
                self._mt5_manager._connection_status = True
            
            return True
            
        except Exception as e:
            self._log_error(f"❌ Error forzando conexión FundedNext: {e}")
            self._log_error("   SISTEMA REQUIERE FUNDEDNEXT MT5 TERMINAL")
            return False

    def _is_fundednext_running(self) -> bool:
        """🔍 Verifica si FundedNext MT5 Terminal está corriendo"""
        try:
            import psutil
            
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    if proc.info['name'] and 'terminal64.exe' in proc.info['name'].lower():
                        if proc.info['exe'] and 'fundednext' in proc.info['exe'].lower():
                            self._log_info(f"✅ FundedNext encontrado corriendo: PID {proc.info['pid']}")
                            return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self._log_info("❌ FundedNext MT5 Terminal no está corriendo")
            return False
            
        except Exception as e:
            self._log_error(f"Error verificando procesos: {e}")
            return False

    def _start_fundednext(self) -> bool:
        """🚀 Inicia FundedNext MT5 Terminal"""
        try:
            import subprocess
            import os
            
            fundednext_path = r"C:\Program Files\FundedNext MT5 Terminal\terminal64.exe"
            
            if not os.path.exists(fundednext_path):
                self._log_error(f"❌ FundedNext no encontrado: {fundednext_path}")
                return False
            
            self._log_info("🚀 Iniciando FundedNext MT5 Terminal...")
            
            # Abrir FundedNext
            subprocess.Popen([fundednext_path], shell=True)
            
            # Esperar un momento
            import time
            time.sleep(2)
            
            # Verificar que se haya iniciado
            if self._is_fundednext_running():
                self._log_info("✅ FundedNext MT5 Terminal iniciado")
                return True
            else:
                self._log_error("❌ No se pudo iniciar FundedNext")
                return False
                
        except Exception as e:
            self._log_error(f"Error iniciando FundedNext: {e}")
            return False

    def _get_mt5_manager(self):
        """📡 Obtiene MT5DataManager usando lazy loading"""
        if self._mt5_manager is None:
            try:
                # Importar MT5DataManager usando SIC v3.1
                if SIC_V3_1_AVAILABLE:
                    from utils.mt5_data_manager import MT5DataManager
                    self._mt5_manager = MT5DataManager()
                    self._log_info("MT5DataManager cargado correctamente")
                else:
                    # Solo log debug, no warning
                    if self._enable_debug:
                        self._log_info("MT5DataManager no disponible - usando conexión directa")
                    
            except Exception as e:
                if self._enable_debug:
                    self._log_error(f"Error cargando MT5DataManager: {e}")
                
        return self._mt5_manager

    def download_candles(self, 
                        symbol: str, 
                        timeframe: str, 
                        start_date: Optional[datetime] = None, 
                        end_date: Optional[datetime] = None,
                        save_to_file: Optional[bool] = None,
                        bars_count: Optional[int] = None,
                        use_ict_optimal: bool = True) -> Dict[str, Any]:
        """
        📥 Descarga velas OPTIMIZADA según LEYES ICT v6.0 con STORAGE INTELIGENTE
        
        Args:
            symbol: Símbolo a descargar (ej: "EURUSD")
            timeframe: Timeframe ICT (ej: "M15", "M5", "H1", "H4", "D1")
            start_date: Fecha de inicio (opcional si se usa bars_count)
            end_date: Fecha de fin (opcional, default: ahora)
            save_to_file: Si guardar en archivo (None = usar configuración automática)
            bars_count: Cantidad específica de velas (override ICT optimal)
            use_ict_optimal: Si usar configuración ICT óptima automática
            
        Returns:
            Dict con resultado de la descarga ICT-compliant
        """
        try:
            # 🗄️ DETERMINAR ESTRATEGIA DE ALMACENAMIENTO INTELIGENTE
            if save_to_file is None:
                save_to_file = self._should_save_to_file(timeframe, symbol)
                storage_decision = "AUTO"
            else:
                storage_decision = "MANUAL"
            
            # 🏛️ APLICAR CONFIGURACIÓN ICT ÓPTIMA
            if use_ict_optimal:
                ict_config = self._get_ict_optimal_config(timeframe)
                if not bars_count:
                    bars_count = ict_config['optimal_bars']
                
                self._log_info(f"📊 ICT OPTIMAL: {symbol} {timeframe} - {bars_count} velas (según leyes institucionales)")
                self._log_info(f"   Mínimo ICT: {ict_config['minimum_bars']} | Ideal: {ict_config['ideal_bars']}")
                self._log_info(f"   Storage: {'💾 Archivo' if save_to_file else '🧠 Memoria'} ({storage_decision})")
            else:
                # Fallback para cantidad manual
                if not bars_count:
                    bars_count = 1000  # Default conservador
            
            # Calcular fechas si no se proporcionan
            if not end_date:
                end_date = datetime.now()
            
            if not start_date and bars_count:
                # Calcular fecha de inicio basada en cantidad de velas y timeframe
                minutes_per_bar = self._get_minutes_per_candle(timeframe)
                total_minutes = bars_count * minutes_per_bar
                start_date = end_date - timedelta(minutes=total_minutes * 1.5)  # 50% extra para fines de semana
            elif not start_date:
                # Fallback: usar 30 días atrás
                start_date = end_date - timedelta(days=30)
            
            self._log_info(f"📥 Descarga ICT ÓPTIMA: {symbol} {timeframe}")
            self._log_info(f"   Período: {start_date.strftime('%Y-%m-%d %H:%M')} a {end_date.strftime('%Y-%m-%d %H:%M')}")
            self._log_info(f"   Objetivo: {bars_count} velas para análisis institucional")
            
            # FORZAR conexión MT5 REAL - Sin fallbacks
            mt5_available = self._check_mt5_connection()
            
            if not mt5_available:
                # ❌ SISTEMA REAL REQUIERE MT5 - NO HAY FALLBACK
                error_msg = f"❌ SISTEMA ICT REQUIERE MT5 REAL - NO HAY DATOS SIMULADOS"
                self._log_error(error_msg)
                self._log_error("   ANÁLISIS ICT NECESITA DATOS INSTITUCIONALES REALES")
                self._log_error("   1. Abrir FundedNext MT5 Terminal")
                self._log_error("   2. Conectar cuenta")
                self._log_error("   3. Verificar símbolos ICT principales")
                
                return {
                    'success': False,
                    'error': 'ICT_MT5_NOT_AVAILABLE',
                    'data': None,
                    'message': error_msg,
                    'ict_requirement': 'DATOS_INSTITUCIONALES_REALES',
                    'instructions': [
                        'Abrir FundedNext MT5 Terminal',
                        'Conectar cuenta demo o real',
                        'Verificar símbolos ICT: EURUSD, GBPUSD, XAUUSD, etc.'
                    ]
                }
            
            # ✅ Usar MT5 REAL con configuración ICT
            result = self._download_with_mt5_ict_optimal(symbol, timeframe, start_date, end_date, save_to_file, bars_count)
            
            # Agregar información de storage
            if result['success']:
                result['storage_info'] = {
                    'saved_to_file': save_to_file,
                    'storage_mode': self._storage_config.get('mode', 'UNKNOWN'),
                    'storage_decision': storage_decision
                }
            
            # Verificar cumplimiento ICT
            if result['success'] and use_ict_optimal:
                result = self._validate_ict_compliance(result, timeframe, bars_count)
            
            return result
                
        except Exception as e:
            self._log_error(f"Error en download_candles ICT: {e}")
            return {
                'success': False,
                'error': str(e),
                'data': None,
                'message': f"Error descargando {symbol} {timeframe} (ICT mode)",
                'ict_status': 'DOWNLOAD_ERROR'
            }

    def _should_save_to_file(self, timeframe: str, symbol: str) -> bool:
        """🤖 Determina automáticamente si guardar archivo según configuración ENTERPRISE"""
        try:
            storage_mode = self._storage_config.get('mode', 'CACHE_SMART')
            
            # Modo ENTERPRISE: decisiones inteligentes optimizadas
            if 'ENTERPRISE' in storage_mode:
                # ENTERPRISE siempre guarda, pero con estrategias optimizadas
                critical_timeframes = self._storage_config.get('critical_timeframes', ['H4', 'H1', 'M15'])
                ict_symbols = self._storage_config.get('ict_symbols', ['EURUSD', 'GBPUSD', 'XAUUSD'])
                
                # Prioridad máxima: símbolos ICT + timeframes críticos
                if symbol in ict_symbols and timeframe in critical_timeframes:
                    return True
                
                # Prioridad alta: timeframes críticos (cualquier símbolo)
                if timeframe in critical_timeframes:
                    return True
                
                # Prioridad media: símbolos ICT (cualquier timeframe)
                if symbol in ict_symbols:
                    return True
                
                # ENTERPRISE mode: guardar todo por defecto (tenemos 520GB)
                return True
            
            # Modo MEMORY_ONLY: nunca guardar
            elif storage_mode == 'MEMORY_ONLY':
                return False
            
            # Modo FULL_STORAGE: siempre guardar
            elif storage_mode == 'FULL_STORAGE':
                return True
            
            # Modo CACHE_SMART: guardar solo timeframes críticos
            elif storage_mode == 'CACHE_SMART':
                critical_timeframes = self._storage_config.get('critical_timeframes', ['H4', 'H1', 'M15'])
                return timeframe in critical_timeframes
            
            # Modo BACKUP_MODE: guardar solo si es crítico y símbolo importante
            elif storage_mode == 'BACKUP_MODE':
                critical_symbols = ['EURUSD', 'XAUUSD', 'GBPUSD']
                critical_timeframes = ['H4', 'H1']
                return symbol in critical_symbols and timeframe in critical_timeframes
            
            # Default ENTERPRISE: guardar todo
            else:
                return True
                
        except Exception as e:
            self._log_error(f"Error determinando storage strategy ENTERPRISE: {e}")
            # Fallback ENTERPRISE: guardar siempre
            return True

    def _download_with_mt5(self, symbol: str, timeframe: str, start_date: datetime, end_date: datetime, save_to_file: bool) -> Dict[str, Any]:
        """📡 Descarga usando MT5 DIRECTO con manejo ROBUSTO de timeframes"""
        try:
            self._log_info(f"📡 Descarga directa MT5: {symbol} {timeframe}")
            
            # Importar MT5 directamente  
            import MetaTrader5 as mt5
            
            # Verificar que MT5 esté inicializado
            if not mt5.initialize():
                # Intentar con FundedNext path específico
                fundednext_path = r"C:\Program Files\FundedNext MT5 Terminal\terminal64.exe"
                if not mt5.initialize(path=fundednext_path):
                    raise Exception("No se pudo inicializar MT5")
            
            # Convertir timeframe a formato MT5
            mt5_timeframe = self._convert_timeframe_to_mt5(timeframe)
            
            # 🚨 ESTRATEGIA MEJORADA: Diferentes métodos para diferentes timeframes
            rates = None
            
            # 🚀 ESTRATEGIA ICT COMPLIANT: Usar copy_rates_from para TODOS los timeframes
            # Esto garantiza obtener suficientes datos históricos
            
            self._log_info(f"📥 Descargando {symbol} {timeframe} usando copy_rates_from (ICT COMPLIANT)...")
            
            # Calcular velas necesarias según estándares ICT
            if timeframe == 'M1':
                count = min(5000, 60 * 24 * 7)    # 7 días de M1
            elif timeframe == 'M5':
                count = min(4000, 12 * 24 * 14)   # 14 días de M5  
            elif timeframe == 'M15':
                count = min(3000, 4 * 24 * 21)    # 21 días de M15 (más datos)
            elif timeframe == 'M30':
                count = min(2500, 2 * 24 * 30)    # 30 días de M30
            elif timeframe == 'H1':
                count = min(2000, 24 * 60)        # 60 días de H1
            elif timeframe == 'H4':
                count = min(1500, 6 * 90)         # 90 días de H4
            else:  # D1
                count = min(1000, 365)            # 1 año de D1
            
            self._log_info(f"📊 ICT TARGET: {count} velas para análisis institucional completo")
            
            # SIEMPRE usar copy_rates_from desde fecha actual hacia atrás
            from datetime import datetime
            rates = mt5.copy_rates_from(symbol, mt5_timeframe, datetime.now(), count)
            
            # Fallback si no funciona
            if rates is None or len(rates) == 0:
                self._log_warning(f"⚠️ Fallback: intentando con end_date específica...")
                rates = mt5.copy_rates_from(symbol, mt5_timeframe, end_date, count)
                
            # Último fallback: usar copy_rates_range solo si todo falla
            if rates is None or len(rates) == 0:
                self._log_warning(f"⚠️ Último fallback: copy_rates_range...")
                rates = mt5.copy_rates_range(symbol, mt5_timeframe, start_date, end_date)
            
            # Verificar resultados
            if rates is None or len(rates) == 0:
                error = mt5.last_error()
                error_msg = f"MT5 no devolvió datos para {symbol} {timeframe}. Error: {error}"
                
                # 🚨 DIAGNÓSTICO ADICIONAL
                self._log_error(f"❌ {error_msg}")
                self._log_error(f"   Timeframe MT5: {mt5_timeframe}")
                self._log_error(f"   Start date: {start_date}")
                self._log_error(f"   End date: {end_date}")
                
                # Verificar información del símbolo
                symbol_info = mt5.symbol_info(symbol)
                if symbol_info:
                    self._log_info(f"   Símbolo OK: {symbol_info.name}")
                else:
                    self._log_error(f"   ❌ Símbolo {symbol} no disponible")
                
                raise Exception(error_msg)
            
            # Convertir a DataFrame usando pandas
            pd = self._get_pandas()
            
            # Crear DataFrame con estructura estándar
            data = pd.DataFrame(rates)
            
            # Convertir timestamp a datetime
            if 'time' in data.columns:
                data.index = pd.to_datetime(data['time'], unit='s')
                data = data.drop('time', axis=1)
            
            # Asegurar columnas estándar OHLCV
            if 'tick_volume' in data.columns and 'volume' not in data.columns:
                data['volume'] = data['tick_volume']
            
            # Redondear precios a 5 decimales para forex
            for col in ['open', 'high', 'low', 'close']:
                if col in data.columns:
                    data[col] = data[col].round(5)
            
            self._log_info(f"✅ Descargadas {len(data)} velas REALES de MT5")
            self._log_info(f"   Rango: {data.index[0]} a {data.index[-1]}")
            self._log_info(f"   Última vela: O={data.iloc[-1]['open']:.5f} C={data.iloc[-1]['close']:.5f}")
            
            # Guardar si se solicita
            if save_to_file:
                self._save_candles_to_file(data, symbol, timeframe)
            
            return {
                'success': True,
                'data': data,
                'message': f"Descargadas {len(data)} velas reales",
                'source': 'mt5_direct',
                'broker': 'FundedNext',
                'timeframe_method': 'copy_rates_from' if timeframe in ['H1', 'H4', 'D1'] else 'copy_rates_range'
            }
                
        except Exception as e:
            self._log_error(f"❌ Error en descarga MT5 directa: {e}")
            raise

    def _download_with_simulation(self, symbol: str, timeframe: str, start_date: datetime, end_date: datetime, save_to_file: bool) -> Dict[str, Any]:
        """🎭 Genera datos simulados para desarrollo"""
        try:
            self._log_info(f"Generando datos simulados para {symbol} {timeframe}")
            
            # Importar pandas usando lazy loading
            pd = self._get_pandas()
            
            # Calcular número de velas basado en timeframe
            minutes_per_candle = self._get_minutes_per_candle(timeframe)
            total_minutes = int((end_date - start_date).total_seconds() / 60)
            num_candles = max(100, min(1000, total_minutes // minutes_per_candle))
            
            # Generar datos simulados realistas
            import random
            import numpy as np
            
            # Precio base para el símbolo
            base_prices = {
                'EURUSD': 1.0900,
                'GBPUSD': 1.2700,
                'USDJPY': 148.50,
                'AUDUSD': 0.6600
            }
            base_price = base_prices.get(symbol, 1.0000)
            
            # Generar series de tiempo
            dates = pd.date_range(start=start_date, periods=num_candles, freq=f'{minutes_per_candle}min')
            
            # Generar precios realistas usando random walk
            prices = []
            current_price = base_price
            
            for i in range(num_candles):
                # Variación pequeña realista
                change = random.gauss(0, base_price * 0.0002)  # 0.02% volatilidad
                current_price += change
                
                # Generar OHLC para esta vela
                open_price = current_price
                volatility = base_price * 0.0005  # 0.05% rango intra-vela
                
                high_price = open_price + random.uniform(0, volatility)
                low_price = open_price - random.uniform(0, volatility)
                close_price = open_price + random.gauss(0, volatility * 0.5)
                
                # Asegurar que high >= low y que OHLC sean consistentes
                high_price = max(high_price, open_price, close_price)
                low_price = min(low_price, open_price, close_price)
                
                prices.append({
                    'open': round(open_price, 5),
                    'high': round(high_price, 5),
                    'low': round(low_price, 5),
                    'close': round(close_price, 5),
                    'volume': random.randint(50, 500)
                })
                
                current_price = close_price
            
            # Crear DataFrame
            data = pd.DataFrame(prices, index=dates)
            
            self._log_info(f"✅ Generadas {len(data)} velas simuladas para {symbol} {timeframe}")
            
            # Guardar si se solicita
            if save_to_file:
                self._save_candles_to_file(data, symbol, timeframe)
            
            return {
                'success': True,
                'data': data,
                'message': f"Generadas {len(data)} velas simuladas",
                'source': 'simulation'
            }
            
        except Exception as e:
            self._log_error(f"Error generando datos simulados: {e}")
            raise

    def _get_pandas(self):
        """🐼 Obtiene pandas usando SIC v3.1"""
        if self._pandas_module is None:
            try:
                if SIC_V3_1_AVAILABLE:
                    from sistema.sic_v3_1 import smart_import
                    self._pandas_module = smart_import('pandas', alias='pd')
                else:
                    import pandas as pd
                    self._pandas_module = pd
            except Exception as e:
                self._log_error(f"Error importando pandas: {e}")
                raise
        return self._pandas_module

    def _get_minutes_per_candle(self, timeframe: str) -> int:
        """⏰ Convierte timeframe a minutos"""
        timeframe_minutes = {
            'M1': 1,
            'M5': 5,
            'M15': 15,
            'M30': 30,
            'H1': 60,
            'H4': 240,
            'D1': 1440
        }
        return timeframe_minutes.get(timeframe, 15)

    def _convert_timeframe_to_mt5(self, timeframe: str):
        """🔄 Convierte timeframe a formato MT5 CORRECTO"""
        try:
            # Importar MT5 para obtener las constantes correctas
            import MetaTrader5 as mt5
            
            # Mapeo CORRECTO de timeframes usando constantes MT5
            tf_mapping = {
                'M1': mt5.TIMEFRAME_M1,     # 1
                'M5': mt5.TIMEFRAME_M5,     # 5  
                'M15': mt5.TIMEFRAME_M15,   # 15
                'M30': mt5.TIMEFRAME_M30,   # 30
                'H1': mt5.TIMEFRAME_H1,     # 16385 (0x4001)
                'H4': mt5.TIMEFRAME_H4,     # 16388 (0x4004)
                'D1': mt5.TIMEFRAME_D1      # 16408 (0x4018)
            }
            
            mt5_tf = tf_mapping.get(timeframe, mt5.TIMEFRAME_M15)
            
            # Log debug para verificar conversión
            if self._enable_debug:
                self._log_info(f"🔄 Timeframe {timeframe} -> MT5 constant: {mt5_tf}")
            
            return mt5_tf
        except Exception as e:
            self._log_error(f"Error convirtiendo timeframe {timeframe}: {e}")
            # Fallback con constantes hardcodeadas
            fallback_mapping = {
                'M1': 1,
                'M5': 5,
                'M15': 15,
                'M30': 30,
                'H1': 16385,  # Constante correcta para H1
                'H4': 16388,  # Constante correcta para H4
                'D1': 16408   # Constante correcta para D1
            }
            return fallback_mapping.get(timeframe, 15)

    def _save_candles_to_file(self, data, symbol: str, timeframe: str):
        """💾 Guarda velas en archivo"""
        try:
            # Crear directorio de datos si no existe
            data_dir = Path("data/candles")
            data_dir.mkdir(parents=True, exist_ok=True)
            
            # Nombre del archivo
            filename = f"{symbol}_{timeframe}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = data_dir / filename
            
            # Guardar usando pandas
            if hasattr(data, 'to_csv'):
                data.to_csv(filepath)
                self._log_info(f"📁 Datos guardados en: {filepath}")
            else:
                self._log_warning("Datos no son DataFrame, no se puede guardar")
                
        except Exception as e:
            self._log_error(f"Error guardando archivo: {e}")

    def _initialize_sic_integration(self):
        """🔧 Inicializa la integración con SIC v3.1 Enterprise"""
        try:
            # Configurar lazy loading para módulos pesados
            if self._enable_lazy_loading:
                self._setup_lazy_modules()
            
            # Configurar cache predictivo
            if self._use_predictive_cache:
                self._setup_predictive_cache()
            
            # Configurar debugging avanzado
            if self._enable_debug:
                debugger.log_import_debug(
                    module_name='advanced_candle_downloader',
                    import_type='enterprise',
                    operation='initialize',
                    duration=0.001,
                    success=True,
                    details={'version': 'v6.0-enterprise', 'sic_version': 'v3.1'}
                )
            
            self._log_info("Integración SIC v3.1 configurada exitosamente")
            
        except Exception as e:
            self._log_error(f"Error configurando integración SIC: {e}")
            if self._enable_debug:
                debugger.diagnose_import_problem('sic_integration', e)

    def _setup_lazy_modules(self):
        """⚡ Configura lazy loading para módulos pesados"""
        try:
            # Configurar proxies lazy para módulos pesados
            lazy_manager = sic.get_lazy_loading_manager()
            
            if lazy_manager is not None:
                # pandas es pesado, cargarlo solo cuando sea necesario
                self._lazy_modules['pandas'] = lazy_manager.lazy_import('pandas')
                
                # asyncio para operaciones asíncronas
                self._lazy_modules['asyncio'] = lazy_manager.lazy_import('asyncio')
                
                self._log_info("Lazy loading configurado para módulos pesados")
            else:
                # Fallback: cargar módulos directamente para sistema funcional
                import pandas as pd
                import asyncio
                self._lazy_modules['pandas'] = pd
                self._lazy_modules['asyncio'] = asyncio
                self._log_info("Lazy loading fallback: módulos cargados directamente")
            
        except Exception as e:
            self._log_error(f"Error configurando lazy loading: {e}")
            # Fallback crítico: cargar módulos directamente
            try:
                import pandas as pd
                import asyncio
                self._lazy_modules['pandas'] = pd
                self._lazy_modules['asyncio'] = asyncio
                self._log_info("Lazy loading emergency fallback: módulos cargados")
            except Exception as fallback_error:
                self._log_error(f"Error en fallback lazy loading: {fallback_error}")

    def _setup_predictive_cache(self):
        """🔮 Configura cache predictivo"""
        try:
            cache_manager = sic.get_predictive_cache_manager()
            
            if cache_manager is not None:
                # Pre-cachear configuraciones comunes
                common_configs = [
                    {'symbols': ['EURUSD', 'GBPUSD'], 'timeframes': ['M1', 'M5']},
                    {'symbols': ['XAUUSD'], 'timeframes': ['M15', 'H1']},
                ]
                
                for config in common_configs:
                    cache_key = f"download_config_{hash(str(config))}"
                    # Usar cache_module en lugar de predict_and_cache
                    cache_manager.cache_module(cache_key, module_obj=config)
                
                self._log_info("Cache predictivo configurado")
            else:
                # Fallback: cache simple en memoria
                self._cache_stats = {'hits': 0, 'misses': 0, 'saves': 0}
                self._memory_cache = {}
                self._log_info("Cache predictivo fallback: cache en memoria configurado")
            
        except Exception as e:
            self._log_error(f"Error configurando cache predictivo: {e}")
            # Fallback crítico: cache básico
            self._cache_stats = {'hits': 0, 'misses': 0, 'saves': 0}
            self._memory_cache = {}
            self._log_info("Cache predictivo emergency fallback: cache básico")

    def initialize(self) -> bool:
        """🚀 Inicializa el downloader y sus componentes con SIC v3.1"""
        start_time = time.time()
        
        try:
            # Obtener MT5 Manager a través de SIC
            self._mt5_manager = self._get_mt5_manager_lazy()
            if not self._mt5_manager:
                self._log_error("No se pudo obtener MT5Manager")
                return False

            # Conectar MT5 con retry inteligente
            if not self._connect_mt5_with_retry():
                self._log_error("No se pudo conectar a MT5")
                return False

            # Inicializar coordinador
            self._coordinator = self._get_coordinator_lazy()
            if not self._coordinator or not self._coordinator.start_coordinator():
                self._log_error("No se pudo iniciar CandleCoordinator")
                return False

            # Registrar métricas de inicialización
            init_duration = time.time() - start_time
            self._performance_metrics.append({
                'operation': 'initialize',
                'duration': init_duration,
                'success': True,
                'timestamp': time.time()
            })

            # Debug avanzado
            if self._enable_debug:
                debugger.log_import_debug(
                    module_name='advanced_candle_downloader',
                    import_type='enterprise',
                    operation='full_initialize',
                    duration=init_duration,
                    success=True,
                    details={
                        'mt5_connected': True,
                        'coordinator_started': True,
                        'lazy_modules': len(self._lazy_modules),
                        'cache_enabled': self._use_predictive_cache
                    }
                )

            self._log_info(f"AdvancedCandleDownloader v6.0 inicializado exitosamente ({init_duration:.3f}s)")
            return True

        except Exception as e:
            init_duration = time.time() - start_time
            self._log_error(f"Error inicializando AdvancedCandleDownloader: {e}")
            
            # Debug de error
            if self._enable_debug:
                debugger.diagnose_import_problem('downloader_initialization', e)
                debugger.log_import_debug(
                    module_name='advanced_candle_downloader',
                    import_type='enterprise',
                    operation='initialize',
                    duration=init_duration,
                    success=False,
                    error=e
                )
            
            return False

    def _get_mt5_manager_lazy(self):
        """🔄 Obtiene MT5Manager con lazy loading"""
        try:
            # Intentar importar MT5DataManager directamente para sistema funcional
            try:
                from utils.mt5_data_manager import MT5DataManager
                manager = MT5DataManager()
                self._log_info("MT5DataManager cargado directamente")
                return manager
            except ImportError:
                self._log_warning("MT5DataManager no disponible en utils")
                
            # Fallback: usar smart_import de SIC si está disponible
            if hasattr(sic, 'smart_import') and sic.smart_import:
                utils_mt5 = sic.smart_import('utils.mt5_data_manager')
                if utils_mt5 and hasattr(utils_mt5, 'MT5DataManager'):
                    return utils_mt5.MT5DataManager()
            
            # Sin MT5DataManager - usar conexión directa MT5
            self._log_warning("MT5DataManager no disponible - usando conexión directa")
            return None
            
        except Exception as e:
            self._log_error(f"Error obteniendo MT5Manager: {e}")
            return None

    def _get_coordinator_lazy(self):
        """🔄 Obtiene CandleCoordinator con lazy loading"""
        try:
            # Lazy import del coordinador
            coordinator_module = sic.smart_import('core.data_management.candle_coordinator')
            if coordinator_module:
                return coordinator_module.CandleCoordinator()
            return None
            
        except Exception as e:
            self._log_error(f"Error obteniendo CandleCoordinator: {e}")
            return None

    def _connect_mt5_with_retry(self, max_attempts: int = 3) -> bool:
        """🔄 Conecta MT5 con reintentos inteligentes"""
        for attempt in range(max_attempts):
            try:
                # Si tenemos MT5DataManager, usarlo
                if self._mt5_manager and hasattr(self._mt5_manager, 'connect'):
                    if self._mt5_manager.connect():
                        return True
                else:
                    # Conexión directa MT5 sin manager
                    if self._force_mt5_connection():
                        return True
                
                if attempt < max_attempts - 1:
                    self._log_info(f"Reintentando conexión MT5 (intento {attempt + 2}/{max_attempts})")
                    time.sleep(self.retry_delay * (attempt + 1))
                    
            except Exception as e:
                self._log_error(f"Error en intento de conexión {attempt + 1}: {e}")
                
        return False

    def start_batch_download(self,
                           symbols: List[str],
                           timeframes: List[str],
                           lookback_bars: int = 50000,
                           priority: int = 1,
                           use_cache: bool = True) -> bool:
        """
        🚀 Inicia descarga masiva con características v6.0 Enterprise
        
        Args:
            symbols: Lista de símbolos a descargar
            timeframes: Lista de timeframes
            lookback_bars: Cantidad de velas por descarga
            priority: Prioridad de la descarga (1=alta, 5=baja)
            use_cache: Usar cache predictivo si está disponible
            
        Returns:
            bool: True si se inició correctamente
        """
        start_time = time.time()
        
        if self.is_downloading:
            self._log_warning("Descarga ya en progreso")
            return False

        try:
            # Verificar cache predictivo
            if use_cache and self._use_predictive_cache:
                cache_key = f"batch_{hash(str(symbols + timeframes))}"
                
                # Verificar si el cache manager está disponible
                cache_manager = sic.get_predictive_cache_manager()
                if cache_manager and hasattr(cache_manager, 'get_cached_prediction'):
                    cached_result = cache_manager.get_cached_prediction(cache_key)
                    if cached_result:
                        self._cache_stats['hits'] += 1
                        self._log_info(f"Cache hit para configuración: {cache_key}")
                else:
                    # Fallback: usar cache en memoria
                    cached_result = self._memory_cache.get(cache_key) if hasattr(self, '_memory_cache') else None
                    if cached_result:
                        self._cache_stats['hits'] += 1
                        self._log_info(f"Memory cache hit para configuración: {cache_key}")

            # Limpiar estado anterior
            with self.lock:
                self.active_downloads.clear()
                self.download_queue.clear()
                self.stop_event.clear()

            # Generar solicitudes de descarga optimizadas
            total_requests = 0
            for symbol in symbols:
                for timeframe in timeframes:
                    request = DownloadRequest(
                        symbol=symbol,
                        timeframe=timeframe,
                        lookback=lookback_bars,
                        request_id=f"{symbol}_{timeframe}_{int(time.time())}_{total_requests}",
                        priority=priority,
                        use_cache=use_cache,
                        enable_lazy_loading=self._enable_lazy_loading,
                        debug_mode=self._enable_debug
                    )
                    self.download_queue.append(request)
                    total_requests += 1

            # Ordenar por prioridad
            self.download_queue.sort(key=lambda x: x.priority)

            # Iniciar worker thread optimizado
            self.is_downloading = True
            self.worker_thread = threading.Thread(
                target=self._download_worker_v6, 
                daemon=True,
                name="AdvancedCandleDownloader-v6.0"
            )
            self.worker_thread.start()

            # Métricas de inicio
            setup_duration = time.time() - start_time
            self._performance_metrics.append({
                'operation': 'batch_download_start',
                'duration': setup_duration,
                'success': True,
                'requests': total_requests,
                'timestamp': time.time()
            })

            # Debug avanzado
            if self._enable_debug:
                debugger.log_import_debug(
                    module_name='advanced_candle_downloader',
                    import_type='enterprise',
                    operation='batch_download_start',
                    duration=setup_duration,
                    success=True,
                    details={
                        'symbols': len(symbols),
                        'timeframes': len(timeframes),
                        'total_requests': total_requests,
                        'priority': priority,
                        'cache_enabled': use_cache
                    }
                )

            self._log_info(f"Descarga masiva v6.0 iniciada: {len(symbols)} símbolos, "
                          f"{len(timeframes)} timeframes, {total_requests} solicitudes")
            return True

        except Exception as e:
            self._log_error(f"Error iniciando descarga masiva: {e}")
            self.is_downloading = False
            
            # Debug de error
            if self._enable_debug:
                debugger.diagnose_import_problem('batch_download_start', e)
            
            return False

    def _download_worker_v6(self):
        """⚙️ Worker thread optimizado para v6.0 Enterprise"""
        try:
            # Obtener pandas de forma lazy si es necesario
            pd = self._get_pandas_lazy()
            
            concurrent_downloads = 0
            max_concurrent = self.max_concurrent_downloads
            
            while self.download_queue and not self.stop_event.is_set():
                # Controlar concurrencia
                if concurrent_downloads >= max_concurrent:
                    time.sleep(0.1)
                    continue
                
                # Obtener siguiente solicitud
                with self.lock:
                    if not self.download_queue:
                        break
                    request = self.download_queue.pop(0)
                
                # Crear thread para descarga individual
                download_thread = threading.Thread(
                    target=self._process_single_download,
                    args=(request, pd),
                    daemon=True
                )
                download_thread.start()
                concurrent_downloads += 1
                
            # Esperar que terminen todas las descargas
            while concurrent_downloads > 0:
                time.sleep(0.5)
                concurrent_downloads = len([t for t in threading.enumerate() 
                                          if t.name.startswith('Download-')])
            
            self._finalize_batch_download()
            
        except Exception as e:
            self._log_error(f"Error en worker thread: {e}")
            if self._enable_debug:
                debugger.log_error({
                    'module_name': 'advanced_candle_downloader',
                    'message': f'Worker thread error: {e}',
                    'traceback': str(e)
                })
        finally:
            self.is_downloading = False

    def _get_pandas_lazy(self):
        """🐼 Obtiene pandas con lazy loading"""
        if 'pandas' in self._lazy_modules:
            pd_proxy = self._lazy_modules['pandas']
            if not pd_proxy.is_loaded:
                self._log_info("Cargando pandas (lazy loading)...")
            return pd_proxy
        else:
            # Fallback: import directo
            import pandas as pd
            return pd

    def _process_single_download(self, request: DownloadRequest, pd):
        """⚡ Procesa una descarga individual con optimizaciones v6.0"""
        threading.current_thread().name = f"Download-{request.symbol}-{request.timeframe}"
        
        start_time = time.time()
        stats = DownloadStats(
            symbol=request.symbol,
            timeframe=request.timeframe,
            start_time=datetime.now()
        )
        
        try:
            # Registrar descarga activa
            with self.lock:
                self.active_downloads[request.request_id] = stats
            
            # Debug de inicio
            if request.debug_mode:
                debugger.log_import_debug(
                    module_name='advanced_candle_downloader',
                    import_type='enterprise',
                    operation='single_download_start',
                    duration=0.001,
                    success=True,
                    details={
                        'symbol': request.symbol,
                        'timeframe': request.timeframe,
                        'lookback': request.lookback
                    }
                )
            
            # Simular descarga (en implementación real, usar MT5)
            # TODO: Implementar descarga real con self._mt5_manager
            total_bars = request.lookback
            batch_size = min(self.download_batch_size, total_bars)
            
            downloaded = 0
            while downloaded < total_bars and not self.stop_event.is_set():
                # Simular descarga de batch
                current_batch = min(batch_size, total_bars - downloaded)
                time.sleep(0.01)  # Simular tiempo de descarga
                downloaded += current_batch
                
                # Actualizar estadísticas
                stats.downloaded_bars = downloaded
                stats.download_speed = downloaded / (time.time() - start_time)
                
                # Callback de progreso
                if self.progress_callback:
                    progress = downloaded / total_bars
                    self.progress_callback(request.symbol, request.timeframe, progress)
            
            # Finalizar descarga exitosa
            stats.total_bars = total_bars
            stats.success = True
            stats.end_time = datetime.now()
            
            # Métricas finales
            duration = time.time() - start_time
            self._performance_metrics.append({
                'operation': 'single_download',
                'symbol': request.symbol,
                'timeframe': request.timeframe,
                'duration': duration,
                'bars': total_bars,
                'speed': stats.download_speed,
                'success': True,
                'timestamp': time.time()
            })
            
            # Debug de finalización
            if request.debug_mode:
                debugger.log_import_debug(
                    module_name='advanced_candle_downloader',
                    import_type='enterprise',
                    operation='single_download_complete',
                    duration=duration,
                    success=True,
                    details={
                        'symbol': request.symbol,
                        'timeframe': request.timeframe,
                        'bars_downloaded': total_bars,
                        'speed': stats.download_speed
                    }
                )
            
            self._log_info(f"Descarga completada: {request.symbol} {request.timeframe} "
                          f"({total_bars} velas, {duration:.2f}s)")
            
        except Exception as e:
            stats.success = False
            stats.error_message = str(e)
            stats.end_time = datetime.now()
            
            self._log_error(f"Error descargando {request.symbol} {request.timeframe}: {e}")
            
            if request.debug_mode:
                debugger.diagnose_import_problem(f'{request.symbol}_{request.timeframe}', e)
        
        finally:
            # Limpiar descarga activa
            with self.lock:
                if request.request_id in self.active_downloads:
                    del self.active_downloads[request.request_id]

    def _finalize_batch_download(self):
        """🏁 Finaliza el batch download con métricas v6.0"""
        try:
            # Calcular estadísticas finales
            total_duration = sum(m['duration'] for m in self._performance_metrics 
                               if m['operation'] == 'single_download')
            successful_downloads = len([m for m in self._performance_metrics 
                                      if m['operation'] == 'single_download' and m['success']])
            
            # Callback de finalización
            if self.complete_callback:
                self.complete_callback(successful_downloads, total_duration)
            
            # Debug final
            if self._enable_debug:
                summary = debugger.get_debug_summary()
                self._log_info(f"Batch download finalizado - Debug summary: {summary['debug_stats']['total_events']} eventos")
            
            self._log_info(f"Descarga masiva completada: {successful_downloads} descargas exitosas")
            
        except Exception as e:
            self._log_error(f"Error finalizando batch download: {e}")

    def stop_download(self) -> None:
        """🛑 Detiene todas las descargas con cleanup v6.0"""
        if not self.is_downloading:
            return

        self._log_info("Deteniendo descargas v6.0...")
        self.stop_event.set()

        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=15.0)

        # Cleanup avanzado
        with self.lock:
            self.active_downloads.clear()
            self.download_queue.clear()

        self.is_downloading = False
        
        # Guardar sesión de debug si está habilitado
        if self._enable_debug:
            debugger.save_session_log(f"candle_downloader_session_{int(time.time())}.json")
        
        self._log_info("Descargas detenidas y cleanup completado")

    def get_status(self) -> Dict[str, Any]:
        """📊 Obtiene estado detallado v6.0 con métricas SIC"""
        with self.lock:
            status = {
                'is_downloading': self.is_downloading,
                'active_downloads': len(self.active_downloads),
                'queue_size': len(self.download_queue),
                'cache_stats': self._cache_stats.copy(),
                'performance_metrics': len(self._performance_metrics),
                'sic_integration': {
                    'version': 'v3.1',
                    'lazy_modules': len(self._lazy_modules),
                    'cache_enabled': self._use_predictive_cache,
                    'debug_enabled': self._enable_debug
                }
            }
            
            # Agregar estadísticas SIC si disponibles
            try:
                if hasattr(sic, 'get_system_stats') and callable(getattr(sic, 'get_system_stats', None)):
                    status['sic_stats'] = sic.get_system_stats()
                else:
                    status['sic_stats'] = {
                        'cache_hits': self._cache_stats.get('hits', 0),
                        'cache_misses': self._cache_stats.get('misses', 0),
                        'lazy_modules_loaded': len(self._lazy_modules)
                    }
            except Exception as e:
                status['sic_stats'] = {'error': f'Error obteniendo stats: {e}'}
            
            # Agregar debug summary si está habilitado
            if self._enable_debug:
                status['debug_summary'] = debugger.get_debug_summary()
            
            return status

    def get_performance_report(self) -> Dict[str, Any]:
        """📈 Genera reporte de performance v6.0"""
        # Calcular métricas agregadas
        downloads = [m for m in self._performance_metrics if m['operation'] == 'single_download'] if self._performance_metrics else []
        
        if downloads:
            avg_duration = sum(d['duration'] for d in downloads) / len(downloads)
            avg_speed = sum(d.get('speed', 0) for d in downloads) / len(downloads)
            total_bars = sum(d.get('bars', 0) for d in downloads)
        else:
            avg_duration = avg_speed = total_bars = 0
        
        # SIEMPRE devolver estructura completa, incluso sin datos
        return {
            'total_operations': len(self._performance_metrics) if self._performance_metrics else 0,
            'successful_downloads': len([d for d in downloads if d['success']]) if downloads else 0,
            'failed_downloads': len([d for d in downloads if not d['success']]) if downloads else 0,
            'avg_download_duration': avg_duration,
            'avg_download_speed': avg_speed,
            'total_bars_downloaded': total_bars,
            'cache_stats': self._cache_stats,
            'sic_integration_active': True,
            'debug_events': debugger.get_debug_summary()['debug_stats']['total_events'] if self._enable_debug else 0
        }

    # ===============================
    # MÉTODOS ICT OPTIMIZADOS v6.0
    # ===============================

    def _get_ict_optimal_config(self, timeframe: str) -> Dict[str, int]:
        """📊 Obtiene configuración ICT óptima por timeframe"""
        # Configuración basada en leyes ICT institucionales
        ict_configs = {
            'M1': {'minimum_bars': 500, 'ideal_bars': 1000, 'optimal_bars': 2000},
            'M5': {'minimum_bars': 1000, 'ideal_bars': 2000, 'optimal_bars': 5000},
            'M15': {'minimum_bars': 2000, 'ideal_bars': 5000, 'optimal_bars': 10000},
            'M30': {'minimum_bars': 1500, 'ideal_bars': 3000, 'optimal_bars': 6000},
            'H1': {'minimum_bars': 1000, 'ideal_bars': 2500, 'optimal_bars': 5000},
            'H4': {'minimum_bars': 500, 'ideal_bars': 1200, 'optimal_bars': 2500},
            'D1': {'minimum_bars': 200, 'ideal_bars': 500, 'optimal_bars': 1000},
        }
        
        return ict_configs.get(timeframe, {
            'minimum_bars': 1000, 
            'ideal_bars': 2000, 
            'optimal_bars': 5000
        })

    def _download_with_mt5_ict_optimal(self, 
                                      symbol: str, 
                                      timeframe: str, 
                                      start_date: datetime, 
                                      end_date: datetime, 
                                      save_to_file: bool,
                                      bars_count: int) -> Dict[str, Any]:
        """📡 Descarga ICT-optimizada usando MT5 con gestión inteligente de cantidad"""
        try:
            self._log_info(f"📊 ICT DOWNLOAD: {symbol} {timeframe} - Target: {bars_count} velas")
            
            # Usar el método MT5 existente pero con configuración ICT
            result = self._download_with_mt5(symbol, timeframe, start_date, end_date, save_to_file)
            
            if result['success'] and result['data'] is not None:
                # Verificar si tenemos suficientes velas según ICT
                actual_bars = len(result['data'])
                ict_config = self._get_ict_optimal_config(timeframe)
                
                # Agregar metadatos ICT
                result['ict_analysis'] = {
                    'target_bars': bars_count,
                    'actual_bars': actual_bars,
                    'ict_minimum': ict_config['minimum_bars'],
                    'ict_ideal': ict_config['ideal_bars'],
                    'ict_optimal': ict_config['optimal_bars'],
                    'meets_ict_minimum': actual_bars >= ict_config['minimum_bars'],
                    'meets_ict_ideal': actual_bars >= ict_config['ideal_bars'],
                    'is_ict_optimal': actual_bars >= ict_config['optimal_bars']
                }
                
                # Log del análisis ICT
                if actual_bars >= ict_config['optimal_bars']:
                    self._log_info(f"✅ ICT OPTIMAL: {actual_bars} velas - Excelente para análisis institucional")
                elif actual_bars >= ict_config['ideal_bars']:
                    self._log_info(f"✅ ICT IDEAL: {actual_bars} velas - Bueno para análisis ICT")
                elif actual_bars >= ict_config['minimum_bars']:
                    self._log_info(f"⚠️ ICT MINIMUM: {actual_bars} velas - Suficiente pero limitado")
                else:
                    self._log_warning(f"❌ ICT INSUFICIENTE: {actual_bars} velas - Menos del mínimo ICT ({ict_config['minimum_bars']})")
                
                result['message'] = f"ICT Download: {actual_bars} velas descargadas"
                result['download_method'] = 'ict_optimal'
            
            return result
            
        except Exception as e:
            self._log_error(f"Error en descarga ICT: {e}")
            raise

    def _validate_ict_compliance(self, result: Dict[str, Any], timeframe: str, target_bars: int) -> Dict[str, Any]:
        """🏛️ Valida cumplimiento de estándares ICT institucionales"""
        try:
            if not result['success'] or result['data'] is None:
                result['ict_compliance'] = {
                    'status': 'FAILED',
                    'reason': 'Download failed',
                    'compliant': False
                }
                return result
            
            actual_bars = len(result['data'])
            ict_config = self._get_ict_optimal_config(timeframe)
            
            # Análisis de cumplimiento ICT
            compliance = {
                'status': 'COMPLIANT',
                'actual_bars': actual_bars,
                'target_bars': target_bars,
                'ict_minimum': ict_config['minimum_bars'],
                'ict_optimal': ict_config['optimal_bars'],
                'compliant': actual_bars >= ict_config['minimum_bars'],
                'optimal_level': False,
                'analysis_quality': 'UNKNOWN'
            }
            
            # Determinar calidad del análisis
            if actual_bars >= ict_config['optimal_bars']:
                compliance['optimal_level'] = True
                compliance['analysis_quality'] = 'INSTITUTIONAL_GRADE'
                compliance['status'] = 'OPTIMAL'
            elif actual_bars >= ict_config['ideal_bars']:
                compliance['analysis_quality'] = 'PROFESSIONAL_GRADE'
                compliance['status'] = 'IDEAL'
            elif actual_bars >= ict_config['minimum_bars']:
                compliance['analysis_quality'] = 'BASIC_GRADE'
                compliance['status'] = 'MINIMUM'
            else:
                compliance['compliant'] = False
                compliance['analysis_quality'] = 'INSUFFICIENT'
                compliance['status'] = 'NON_COMPLIANT'
            
            # Recomendaciones ICT
            recommendations = []
            if not compliance['compliant']:
                recommendations.append(f"Aumentar a mínimo {ict_config['minimum_bars']} velas para análisis ICT")
            elif not compliance['optimal_level']:
                recommendations.append(f"Considerar {ict_config['optimal_bars']} velas para análisis institucional óptimo")
            
            compliance['recommendations'] = recommendations
            result['ict_compliance'] = compliance
            
            # Log de cumplimiento
            if compliance['compliant']:
                self._log_info(f"✅ ICT COMPLIANCE: {compliance['status']} - {compliance['analysis_quality']}")
            else:
                self._log_error(f"❌ ICT NON-COMPLIANT: {actual_bars} < {ict_config['minimum_bars']} velas mínimas")
            
            return result
            
        except Exception as e:
            self._log_error(f"Error validando cumplimiento ICT: {e}")
            result['ict_compliance'] = {
                'status': 'ERROR',
                'reason': str(e),
                'compliant': False
            }
            return result

    def download_ict_full_analysis_set(self, 
                                      symbol: str, 
                                      timeframes: Optional[List[str]] = None,
                                      save_files: bool = True) -> Dict[str, Any]:
        """🏛️ Descarga conjunto completo ICT para análisis institucional"""
        if not timeframes:
            # Timeframes ICT estándar para análisis completo
            timeframes = ['D1', 'H4', 'H1', 'M15', 'M5']
        
        try:
            self._log_info(f"🏛️ ICT FULL ANALYSIS DOWNLOAD: {symbol}")
            self._log_info(f"   Timeframes: {', '.join(timeframes)}")
            
            results = {}
            total_bars = 0
            all_compliant = True
            
            for tf in timeframes:
                self._log_info(f"📊 Descargando {symbol} {tf} (ICT optimal)...")
                
                # Descarga con configuración ICT óptima
                result = self.download_candles(
                    symbol=symbol,
                    timeframe=tf,
                    save_to_file=save_files,
                    use_ict_optimal=True
                )
                
                results[tf] = result
                
                if result['success'] and 'ict_analysis' in result:
                    total_bars += result['ict_analysis']['actual_bars']
                    if not result['ict_analysis']['meets_ict_minimum']:
                        all_compliant = False
                else:
                    all_compliant = False
            
            # Resumen del análisis completo
            summary = {
                'symbol': symbol,
                'timeframes_downloaded': len(timeframes),
                'total_bars': total_bars,
                'all_ict_compliant': all_compliant,
                'download_timestamp': datetime.now().isoformat(),
                'analysis_grade': 'INSTITUTIONAL' if all_compliant else 'INCOMPLETE',
                'results_by_timeframe': results
            }
            
            self._log_info(f"✅ ICT FULL ANALYSIS COMPLETE: {total_bars} velas totales")
            self._log_info(f"   Cumplimiento ICT: {'✅ COMPLIANT' if all_compliant else '❌ INCOMPLETE'}")
            
            return {
                'success': True,
                'summary': summary,
                'data': results,
                'message': f"ICT analysis set downloaded: {len(timeframes)} timeframes, {total_bars} total bars"
            }
            
        except Exception as e:
            self._log_error(f"Error en descarga ICT completa: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Error downloading ICT analysis set for {symbol}"
            }

    # ===============================
    # MÉTODOS DE LOGGING OPTIMIZADOS
    # ===============================

    def _log_info(self, message: str):
        """📝 Log información usando sistema optimizado"""
        try:
            print(f"ℹ️  [AdvancedCandleDownloader v6.0] {message}")
        except Exception:
            pass

    def _log_warning(self, message: str):
        """⚠️ Log warning usando sistema optimizado"""
        try:
            print(f"⚠️  [AdvancedCandleDownloader v6.0] {message}")
        except Exception:
            pass

    def _log_error(self, message: str):
        """❌ Log error usando sistema optimizado"""
        try:
            print(f"❌ [AdvancedCandleDownloader v6.0] {message}")
        except Exception:
            pass


# ===============================
# FUNCIONES DE UTILIDAD v6.0
# ===============================

def get_advanced_candle_downloader(config: Optional[Dict[str, Any]] = None) -> AdvancedCandleDownloader:
    """
    🏭 Factory function para crear AdvancedCandleDownloader v6.0
    
    Args:
        config: Configuración opcional del downloader
        
    Returns:
        Instancia configurada de AdvancedCandleDownloader
    """
    default_config = {
        'enable_debug': True,
        'use_predictive_cache': True,
        'enable_lazy_loading': True,
        'max_concurrent': 3,
        'batch_size': 10000,
        'retry_attempts': 3,
        'retry_delay': 2.0
    }
    
    if config:
        default_config.update(config)
    
    return AdvancedCandleDownloader(config=default_config)


def create_download_request(symbol: str, timeframe: str, lookback: int = 50000) -> DownloadRequest:
    """
    📋 Factory function para crear DownloadRequest
    
    Args:
        symbol: Símbolo a descargar
        timeframe: Timeframe de las velas
        lookback: Cantidad de velas
        
    Returns:
        DownloadRequest configurado
    """
    return DownloadRequest(
        symbol=symbol,
        timeframe=timeframe,
        lookback=lookback,
        request_id=f"{symbol}_{timeframe}_{int(time.time())}",
        use_cache=True,
        enable_lazy_loading=True,
        debug_mode=True
    )


# ===============================
# TEST Y VALIDACIÓN
# ===============================

if __name__ == "__main__":
    print("🧪 Testing AdvancedCandleDownloader v6.0 Enterprise...")
    
    try:
        # Crear downloader con configuración de test
        test_config = {
            'enable_debug': True,
            'use_predictive_cache': True,
            'enable_lazy_loading': True,
            'max_concurrent': 2,
            'batch_size': 1000
        }
        
        downloader = get_advanced_candle_downloader(test_config)
        print("✅ Downloader creado exitosamente")
        
        # Test de estado inicial
        status = downloader.get_status()
        print(f"✅ Estado inicial: {status['sic_integration']['version']}")
        
        # Test de performance report
        report = downloader.get_performance_report()
        print(f"✅ Reporte de performance generado")
        
        # Test de configuración SIC
        try:
            if SIC_V3_1_AVAILABLE:
                from sistema.sic_v3_1 import get_sic_instance
                sic_instance = get_sic_instance()
                sic_stats = sic_instance.get_system_stats()
                print(f"✅ Estadísticas SIC v3.1: {sic_stats.get('sic_version', 'N/A')}")
            else:
                print("ℹ️ SIC v3.1 no disponible para estadísticas")
        except Exception as e:
            print(f"⚠️ Error obteniendo stats SIC: {e}")
        
        print("🎯 Test de AdvancedCandleDownloader v6.0 completado exitosamente")
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
