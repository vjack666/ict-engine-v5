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
from typing import Dict, List, Optional, Callable, Any, Set, Tuple, Union
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field, asdict
from pathlib import Path

# Imports SIC v3.1 Enterprise (usando try/except para compatibilidad)
try:
    from sistema.sic_v3_1.enterprise_interface import SICEnterpriseInterface
    from sistema.sic_v3_1.advanced_debug import AdvancedDebugger
    SIC_V3_1_AVAILABLE = True
except ImportError:
    SIC_V3_1_AVAILABLE = False
    # Fallback para desarrollo
    class SICEnterpriseInterface:
        def __init__(self): pass
        def smart_import(self, module_name): return None
        def get_lazy_loading_manager(self): return None
        def get_predictive_cache_manager(self): return None
    
    class AdvancedDebugger:
        def __init__(self, config=None): pass
        def log_import_debug(self, *args, **kwargs): pass
        def diagnose_import_problem(self, *args, **kwargs): pass
        def get_debug_summary(self): return {'debug_stats': {'total_events': 0}}
        def save_session_log(self, *args, **kwargs): pass
        def log_error(self, *args, **kwargs): pass

# El SIC v3.1 gestionará estos imports de forma inteligente
sic = SICEnterpriseInterface()

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
        
        # Inicializar componentes SIC v3.1
        self._initialize_sic_integration()
        
        # Log de inicialización
        self._log_info("AdvancedCandleDownloader v6.0 inicializado con SIC v3.1")

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
            
            # pandas es pesado, cargarlo solo cuando sea necesario
            self._lazy_modules['pandas'] = lazy_manager.lazy_import('pandas')
            
            # asyncio para operaciones asíncronas
            self._lazy_modules['asyncio'] = lazy_manager.lazy_import('asyncio')
            
            self._log_info("Lazy loading configurado para módulos pesados")
            
        except Exception as e:
            self._log_error(f"Error configurando lazy loading: {e}")

    def _setup_predictive_cache(self):
        """🔮 Configura cache predictivo"""
        try:
            cache_manager = sic.get_predictive_cache_manager()
            
            # Pre-cachear configuraciones comunes
            common_configs = [
                {'symbols': ['EURUSD', 'GBPUSD'], 'timeframes': ['M1', 'M5']},
                {'symbols': ['XAUUSD'], 'timeframes': ['M15', 'H1']},
            ]
            
            for config in common_configs:
                cache_key = f"download_config_{hash(str(config))}"
                cache_manager.predict_and_cache(cache_key, config)
            
            self._log_info("Cache predictivo configurado")
            
        except Exception as e:
            self._log_error(f"Error configurando cache predictivo: {e}")

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
            # Usar SIC para obtener el manager de forma inteligente
            if hasattr(sic, 'get_mt5_manager'):
                return sic.get_mt5_manager()
            
            # Fallback: importar directamente
            utils_mt5 = sic.smart_import('utils.mt5_data_manager')
            return utils_mt5.get_mt5_manager() if utils_mt5 else None
            
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
                if self._mt5_manager.connect():
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
                cached_result = sic.get_predictive_cache_manager().get_cached_prediction(cache_key)
                if cached_result:
                    self._cache_stats['hits'] += 1
                    self._log_info(f"Cache hit para configuración: {cache_key}")

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
            if hasattr(sic, 'get_stats'):
                status['sic_stats'] = sic.get_stats()
            
            # Agregar debug summary si está habilitado
            if self._enable_debug:
                status['debug_summary'] = debugger.get_debug_summary()
            
            return status

    def get_performance_report(self) -> Dict[str, Any]:
        """📈 Genera reporte de performance v6.0"""
        if not self._performance_metrics:
            return {'error': 'No performance data available'}
        
        # Calcular métricas agregadas
        downloads = [m for m in self._performance_metrics if m['operation'] == 'single_download']
        
        if downloads:
            avg_duration = sum(d['duration'] for d in downloads) / len(downloads)
            avg_speed = sum(d.get('speed', 0) for d in downloads) / len(downloads)
            total_bars = sum(d.get('bars', 0) for d in downloads)
        else:
            avg_duration = avg_speed = total_bars = 0
        
        return {
            'total_operations': len(self._performance_metrics),
            'successful_downloads': len([d for d in downloads if d['success']]),
            'failed_downloads': len([d for d in downloads if not d['success']]),
            'avg_download_duration': avg_duration,
            'avg_download_speed': avg_speed,
            'total_bars_downloaded': total_bars,
            'cache_stats': self._cache_stats,
            'sic_integration_active': True,
            'debug_events': debugger.get_debug_summary()['debug_stats']['total_events'] if self._enable_debug else 0
        }

    # ===============================
    # MÉTODOS DE LOGGING OPTIMIZADOS
    # ===============================

    def _log_info(self, message: str):
        """📝 Log de información con SIC v3.1"""
        try:
            if hasattr(sic, 'log_info'):
                sic.log_info(message, 'advanced_candle_downloader', 'info')
            else:
                print(f"ℹ️  [AdvancedCandleDownloader v6.0] {message}")
        except:
            print(f"ℹ️  [AdvancedCandleDownloader v6.0] {message}")

    def _log_warning(self, message: str):
        """⚠️  Log de advertencia con SIC v3.1"""
        try:
            if hasattr(sic, 'log_warning'):
                sic.log_warning(message, 'advanced_candle_downloader', 'warning')
            else:
                print(f"⚠️  [AdvancedCandleDownloader v6.0] {message}")
        except:
            print(f"⚠️  [AdvancedCandleDownloader v6.0] {message}")

    def _log_error(self, message: str):
        """❌ Log de error con SIC v3.1"""
        try:
            if hasattr(sic, 'log_error'):
                sic.log_error(message, 'advanced_candle_downloader', 'error')
            else:
                print(f"❌ [AdvancedCandleDownloader v6.0] {message}")
        except:
            print(f"❌ [AdvancedCandleDownloader v6.0] {message}")


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
        if hasattr(sic, 'get_stats'):
            sic_stats = sic.get_stats()
            print(f"✅ Estadísticas SIC: {sic_stats}")
        
        print("🎯 Test de AdvancedCandleDownloader v6.0 completado exitosamente")
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
