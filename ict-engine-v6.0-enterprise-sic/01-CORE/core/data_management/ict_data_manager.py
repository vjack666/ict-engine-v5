#!/usr/bin/env python3
"""
📊 ICT DATA MANAGER - SISTEMA HÍBRIDO INTELIGENTE
=================================================

Gestor de datos ICT optimizado para inicialización rápida y mejora continua.
Implementa estrategia híbrida: warm-up rápido + enhancement en background.

Características:
- Cache warm-up en 15-30 segundos
- Descarga paralela inteligente  
- Priorización por importancia ICT
- Mejora continua automática
- Compatible con trading en vivo

Autor: ICT Engine v6.1.0 Enterprise Team
Versión: 1.0.0
Fecha: 2025-08-08
"""

import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import json

# Integración SIC + SLUC para Memoria Unificada v6.0
try:
    from core.analysis.unified_market_memory import (
        get_unified_market_memory,
        update_market_memory,
        get_trading_insights
    )
    UNIFIED_MEMORY_AVAILABLE = True
    print("✅ [SIC Integration] Sistema de Memoria Unificada v6.0 conectado")
except ImportError:
    UNIFIED_MEMORY_AVAILABLE = False
    print("⚠️ Sistema de Memoria Unificada no disponible")

# Configuración ICT Enterprise
ICT_DATA_CONFIG = {
    # Símbolos por prioridad ICT
    'symbols_critical': ['EURUSD', 'GBPUSD'],
    'symbols_important': ['USDJPY', 'AUDUSD', 'USDCHF'],
    'symbols_extended': ['NZDUSD', 'EURGBP', 'XAUUSD'],
    
    # Timeframes por prioridad
    'timeframes_critical': ['H4', 'M15'],  # Para análisis inmediato
    'timeframes_enhanced': ['M5', 'H1'],   # Para refinamiento
    'timeframes_extended': ['D1', 'M30'],  # Para contexto completo
    
    # Cantidad de datos por modo
    'bars_minimal': {
        'H4': 240,    # 10 días (mínimo ICT)
        'M15': 480,   # 5 días (estructura básica)
        'M5': 720,    # 2.5 días (timing)
        'H1': 240,    # 10 días
        'D1': 60,     # 2 meses
        'M30': 480    # 10 días
    },
    'bars_optimal': {
        'H4': 720,    # 30 días (optimal ICT)
        'M15': 1440,  # 15 días (estructura completa)
        'M5': 2880,   # 10 días (timing preciso)
        'H1': 720,    # 30 días
        'D1': 180,    # 6 meses
        'M30': 1440   # 30 días
    }
}

class ICTDataManager:
    """
    📊 GESTOR DE DATOS ICT HÍBRIDO
    
    Maneja descarga inteligente de datos con priorización ICT:
    1. Warm-up rápido (datos críticos)
    2. Enhancement background (datos completos)
    3. Monitoring continuo (actualizaciones)
    """
    
    def __init__(self, downloader=None):
        """Inicializar ICT Data Manager"""
        
        self.downloader = downloader
        self.config = ICT_DATA_CONFIG.copy()
        
        # Estado del sistema
        self.warm_up_completed = False
        self.enhancement_active = False
        self.data_status = {}
        
        # Threading para operaciones paralelas
        self.executor = ThreadPoolExecutor(max_workers=6)
        self.enhancement_thread = None
        
        # Cache de resultados
        self.available_data = {}
        self.last_update = {}
        
        # Sistema de Memoria Unificada v6.0 (SIC + SLUC)
        self.unified_memory = None
        if UNIFIED_MEMORY_AVAILABLE:
            try:
                self.unified_memory = get_unified_market_memory()
                print("🧠 ICTDataManager: Memoria Unificada v6.0 conectada (SIC + SLUC)")
            except Exception as e:
                print(f"⚠️ Error conectando Memoria Unificada: {e}")
        
        # Métricas
        self.performance_metrics = {
            'warm_up_time': 0.0,
            'total_downloads': 0,
            'successful_downloads': 0,
            'failed_downloads': 0,
            'last_warm_up': None,
            'enhancement_cycles': 0
        }
        
        print("📊 ICT Data Manager inicializado")
        print(f"   Símbolos críticos: {self.config['symbols_critical']}")
        print(f"   Timeframes críticos: {self.config['timeframes_critical']}")
        print(f"   Modo: Híbrido (warm-up + enhancement)")
    
    def warm_up_cache(self, symbols: Optional[List[str]] = None, 
                     timeframes: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        🚀 WARM-UP RÁPIDO del cache con datos críticos
        
        Descarga SOLO los datos esenciales para análisis ICT inmediato.
        Objetivo: Sistema operativo en 15-30 segundos.
        
        Args:
            symbols: Símbolos a descargar (default: críticos)
            timeframes: Timeframes a descargar (default: críticos)
            
        Returns:
            Dict con resultado del warm-up
        """
        start_time = time.time()
        
        # Usar configuración por defecto si no se especifica
        if symbols is None:
            symbols = self.config['symbols_critical']
        if timeframes is None:
            timeframes = self.config['timeframes_critical']
        
        print(f"\n🚀 INICIANDO ICT CACHE WARM-UP")
        print(f"   Símbolos: {symbols}")
        print(f"   Timeframes: {timeframes}")
        print(f"   Objetivo: Datos mínimos para análisis inmediato")
        
        # Verificar downloader
        if not self.downloader:
            return {
                'success': False,
                'error': 'Downloader no disponible',
                'warm_up_time': 0.0
            }
        
        # Preparar tareas de descarga
        download_tasks = []
        for symbol in symbols:
            for timeframe in timeframes:
                task_key = f"{symbol}_{timeframe}"
                download_tasks.append({
                    'key': task_key,
                    'symbol': symbol,
                    'timeframe': timeframe,
                    'bars': self.config['bars_minimal'][timeframe],
                    'priority': 'CRITICAL'
                })
        
        print(f"   📋 {len(download_tasks)} descargas programadas")
        
        # Ejecutar descargas en paralelo
        results = self._execute_parallel_downloads(download_tasks, mode='warm_up')
        
        # Procesar resultados
        successful = sum(1 for r in results.values() if r.get('success', False))
        total = len(download_tasks)
        
        warm_up_time = time.time() - start_time
        self.performance_metrics['warm_up_time'] = warm_up_time
        self.performance_metrics['last_warm_up'] = datetime.now()
        
        self.warm_up_completed = successful >= (total * 0.7)  # 70% éxito mínimo
        
        # Log resultados
        print(f"\n✅ ICT CACHE WARM-UP COMPLETADO")
        print(f"   ⏱️ Tiempo: {warm_up_time:.1f} segundos")
        print(f"   📊 Éxito: {successful}/{total} ({successful/total*100:.1f}%)")
        print(f"   🎯 Estado: {'OPERATIVO' if self.warm_up_completed else 'PARCIAL'}")
        
        # Actualizar estado de datos disponibles
        self._update_data_status(results)
        
        # Iniciar enhancement en background si warm-up exitoso
        if self.warm_up_completed:
            self._start_background_enhancement()
        
        return {
            'success': self.warm_up_completed,
            'warm_up_time': warm_up_time,
            'successful_downloads': successful,
            'total_downloads': total,
            'success_rate': successful / total,
            'results': results,
            'next_phase': 'enhancement' if self.warm_up_completed else 'retry_warm_up'
        }
    
    def _execute_parallel_downloads(self, tasks: List[Dict], mode: str = 'standard') -> Dict[str, Any]:
        """🔄 Ejecutar descargas en paralelo"""
        
        results = {}
        futures = {}
        
        # Enviar tareas al executor
        for task in tasks:
            future = self.executor.submit(self._download_single_task, task, mode)
            futures[future] = task['key']
        
        # Procesar resultados conforme se completan
        completed_count = 0
        for future in as_completed(futures):
            task_key = futures[future]
            completed_count += 1
            
            try:
                result = future.result()
                results[task_key] = result
                
                if result.get('success', False):
                    status_icon = "✅"
                    self.performance_metrics['successful_downloads'] += 1
                else:
                    status_icon = "❌"
                    self.performance_metrics['failed_downloads'] += 1
                
                print(f"   {status_icon} {task_key}: {completed_count}/{len(tasks)}")
                
            except Exception as e:
                results[task_key] = {
                    'success': False,
                    'error': str(e),
                    'timestamp': datetime.now()
                }
                self.performance_metrics['failed_downloads'] += 1
                print(f"   ❌ {task_key}: Error - {e}")
        
        self.performance_metrics['total_downloads'] += len(tasks)
        return results
    
    def _download_single_task(self, task: Dict, mode: str) -> Dict[str, Any]:
        """📥 Ejecutar una descarga individual"""
        
        try:
            # Extraer datos del task con fallbacks seguros
            symbol = task.get('symbol', 'UNKNOWN')
            timeframe = task.get('timeframe', 'H4')
            bars_count = task.get('bars', task.get('bars_count', 240))  # Fallback para diferentes formatos
            
            result = self.downloader.download_candles(
                symbol=symbol,
                timeframe=timeframe,
                bars_count=bars_count,
                use_ict_optimal=True,
                save_to_file=None  # Decisión automática
            )
            
            # Agregar metadatos del task
            if result and result.get('success', False):
                result['task_info'] = {
                    'priority': task.get('priority', 'NORMAL'),
                    'mode': mode,
                    'bars_requested': bars_count,
                    'bars_received': len(result.get('data', [])) if result.get('data') is not None else 0
                }
            
            return result or {
                'success': False,
                'error': 'Downloader returned None',
                'task_info': task,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'task_info': task,
                'timestamp': datetime.now()
            }
    
    def _update_data_status(self, results: Dict[str, Any]):
        """📊 Actualizar estado de datos disponibles"""
        
        for key, result in results.items():
            symbol, timeframe = key.split('_')
            
            if symbol not in self.data_status:
                self.data_status[symbol] = {}
            
            self.data_status[symbol][timeframe] = {
                'available': result.get('success', False),
                'bars_count': result.get('task_info', {}).get('bars_received', 0),
                'last_update': datetime.now(),
                'source': result.get('source', 'unknown'),
                'quality': self._assess_data_quality(result)
            }
    
    def _assess_data_quality(self, result: Dict[str, Any]) -> str:
        """🎯 Evaluar calidad de datos para análisis ICT"""
        
        if not result.get('success', False):
            return 'UNAVAILABLE'
        
        bars_received = result.get('task_info', {}).get('bars_received', 0)
        bars_requested = result.get('task_info', {}).get('bars_requested', 0)
        
        if bars_received == 0:
            return 'NO_DATA'
        elif bars_received >= bars_requested * 0.9:
            return 'EXCELLENT'
        elif bars_received >= bars_requested * 0.7:
            return 'GOOD'
        elif bars_received >= bars_requested * 0.5:
            return 'ACCEPTABLE'
        else:
            return 'INSUFFICIENT'
    
    def _start_background_enhancement(self):
        """🔄 Iniciar enhancement en background"""
        
        if self.enhancement_active:
            print("   🔄 Enhancement ya activo")
            return
        
        print("   🚀 Iniciando enhancement en background...")
        
        self.enhancement_thread = threading.Thread(
            target=self._background_enhancement_loop,
            daemon=True
        )
        self.enhancement_thread.start()
        self.enhancement_active = True
    
    def _background_enhancement_loop(self):
        """🔄 Loop de enhancement en background"""
        
        print("📈 Background enhancement iniciado")
        
        try:
            while self.enhancement_active:
                # Ejecutar ciclo de enhancement
                self._execute_enhancement_cycle()
                
                # Esperar antes del próximo ciclo
                time.sleep(300)  # 5 minutos entre ciclos
                
        except Exception as e:
            print(f"❌ Error en background enhancement: {e}")
        finally:
            self.enhancement_active = False
            print("📈 Background enhancement detenido")
    
    def _execute_enhancement_cycle(self):
        """🎯 Ejecutar un ciclo de enhancement"""
        
        print(f"🔄 Ejecutando enhancement cycle #{self.performance_metrics['enhancement_cycles'] + 1}")
        
        # Preparar tareas de enhancement
        enhancement_tasks = []
        
        # Prioridad 1: Completar datos de símbolos críticos
        for symbol in self.config['symbols_critical']:
            for timeframe in self.config['timeframes_enhanced']:
                if not self._has_optimal_data(symbol, timeframe):
                    enhancement_tasks.append({
                        'key': f"{symbol}_{timeframe}",
                        'symbol': symbol,
                        'timeframe': timeframe,
                        'bars': self.config['bars_optimal'][timeframe],
                        'priority': 'ENHANCEMENT_CRITICAL'
                    })
        
        # Prioridad 2: Expandir a símbolos importantes
        for symbol in self.config['symbols_important']:
            for timeframe in self.config['timeframes_critical']:
                if not self._has_minimal_data(symbol, timeframe):
                    enhancement_tasks.append({
                        'key': f"{symbol}_{timeframe}",
                        'symbol': symbol,
                        'timeframe': timeframe,
                        'bars': self.config['bars_minimal'][timeframe],
                        'priority': 'ENHANCEMENT_IMPORTANT'
                    })
        
        if enhancement_tasks:
            print(f"   📋 {len(enhancement_tasks)} tareas de enhancement")
            results = self._execute_parallel_downloads(enhancement_tasks, mode='enhancement')
            self._update_data_status(results)
            
            successful = sum(1 for r in results.values() if r.get('success', False))
            print(f"   ✅ Enhancement: {successful}/{len(enhancement_tasks)} exitosas")
        else:
            print("   ✅ No se requiere enhancement - datos óptimos")
        
        self.performance_metrics['enhancement_cycles'] += 1
    
    def _has_minimal_data(self, symbol: str, timeframe: str) -> bool:
        """Verificar si tenemos datos mínimos para análisis"""
        
        if symbol not in self.data_status or timeframe not in self.data_status[symbol]:
            return False
        
        data_info = self.data_status[symbol][timeframe]
        return (data_info['available'] and 
                data_info['bars_count'] >= self.config['bars_minimal'][timeframe] * 0.7)
    
    def _has_optimal_data(self, symbol: str, timeframe: str) -> bool:
        """Verificar si tenemos datos óptimos para análisis"""
        
        if symbol not in self.data_status or timeframe not in self.data_status[symbol]:
            return False
        
        data_info = self.data_status[symbol][timeframe]
        return (data_info['available'] and 
                data_info['bars_count'] >= self.config['bars_optimal'][timeframe] * 0.9)
    
    def get_data_readiness(self, symbol: str, timeframes: List[str]) -> Dict[str, Any]:
        """
        📊 Evaluar disponibilidad de datos para análisis multi-timeframe
        
        Returns:
            Dict con estado de disponibilidad por timeframe
        """
        
        readiness = {
            'symbol': symbol,
            'overall_ready': True,
            'timeframes': {},
            'analysis_capability': 'NONE',
            'recommendations': []
        }
        
        ready_count = 0
        for tf in timeframes:
            if self._has_minimal_data(symbol, tf):
                readiness['timeframes'][tf] = {
                    'status': 'READY',
                    'quality': self.data_status[symbol][tf]['quality'],
                    'bars': self.data_status[symbol][tf]['bars_count']
                }
                ready_count += 1
            else:
                readiness['timeframes'][tf] = {
                    'status': 'NOT_READY',
                    'quality': 'UNAVAILABLE',
                    'bars': 0
                }
                readiness['overall_ready'] = False
        
        # Determinar capacidad de análisis
        if ready_count == len(timeframes):
            readiness['analysis_capability'] = 'FULL'
        elif ready_count >= len(timeframes) * 0.67:
            readiness['analysis_capability'] = 'PARTIAL'
            readiness['recommendations'].append(f"Análisis parcial disponible con {ready_count}/{len(timeframes)} timeframes")
        else:
            readiness['analysis_capability'] = 'LIMITED'
            readiness['recommendations'].append("Datos insuficientes para análisis confiable")
        
        return readiness
    
    def auto_detect_multi_tf_data(self, symbols: List[str], required_timeframes: List[str]) -> Dict[str, Any]:
        """
        🔍 AUTO-DETECCIÓN DE DATOS MULTI-TIMEFRAME
        
        Detecta automáticamente disponibilidad de datos en múltiples timeframes
        y sincroniza la información para análisis cross-timeframe.
        
        Args:
            symbols: Lista de símbolos a verificar
            required_timeframes: Timeframes requeridos para análisis
            
        Returns:
            Dict con estado de disponibilidad multi-timeframe
        """
        print(f"🔍 AUTO-DETECCIÓN MULTI-TF: {len(symbols)} símbolos x {len(required_timeframes)} timeframes")
        
        detection_results = {
            'symbols_analyzed': len(symbols),
            'timeframes_required': len(required_timeframes),
            'detection_matrix': {},
            'readiness_summary': {},
            'recommendations': [],
            'sync_status': 'PENDING'
        }
        
        # Analizar cada símbolo
        for symbol in symbols:
            symbol_readiness = self.get_data_readiness(symbol, required_timeframes)
            detection_results['detection_matrix'][symbol] = symbol_readiness
            
            # Categorizar por disponibilidad
            if symbol_readiness['analysis_capability'] == 'FULL':
                detection_results['readiness_summary'][symbol] = 'READY'
            elif symbol_readiness['analysis_capability'] == 'PARTIAL':
                detection_results['readiness_summary'][symbol] = 'PARTIAL'
            else:
                detection_results['readiness_summary'][symbol] = 'NOT_READY'
        
        # Generar recomendaciones inteligentes
        ready_count = sum(1 for status in detection_results['readiness_summary'].values() if status == 'READY')
        partial_count = sum(1 for status in detection_results['readiness_summary'].values() if status == 'PARTIAL')
        
        if ready_count >= len(symbols) * 0.8:
            detection_results['recommendations'].append("✅ Análisis multi-TF recomendado - datos suficientes")
            detection_results['sync_status'] = 'OPTIMAL'
        elif ready_count + partial_count >= len(symbols) * 0.6:
            detection_results['recommendations'].append("⚠️ Análisis parcial posible - completar datos faltantes")
            detection_results['sync_status'] = 'ACCEPTABLE'
        else:
            detection_results['recommendations'].append("❌ Datos insuficientes - iniciar warm-up antes de análisis")
            detection_results['sync_status'] = 'INSUFFICIENT'
        
        # Log de SLUC v2.1 para auditoría
        self._log_multitf_detection(detection_results)
        
        print(f"   ✅ Auto-detección completada: {ready_count}/{len(symbols)} símbolos listos")
        return detection_results
    
    def sync_multi_tf_data(self, symbol: str, timeframes: List[str], force_download: bool = False) -> Dict[str, Any]:
        """
        🔄 SINCRONIZACIÓN MULTI-TIMEFRAME
        
        Sincroniza y alinea datos entre múltiples timeframes para un símbolo.
        Detecta gaps y descarga datos faltantes automáticamente.
        
        Args:
            symbol: Símbolo a sincronizar
            timeframes: Lista de timeframes a alinear
            force_download: Forzar descarga aunque existan datos
            
        Returns:
            Dict con resultado de sincronización
        """
        print(f"🔄 SINCRONIZANDO {symbol} en {len(timeframes)} timeframes...")
        
        sync_result = {
            'symbol': symbol,
            'timeframes_processed': 0,
            'sync_tasks': [],
            'gaps_detected': [],
            'downloads_executed': 0,
            'alignment_status': 'PENDING'
        }
        
        # Detectar gaps en cada timeframe
        for tf in timeframes:
            if not self._has_minimal_data(symbol, tf) or force_download:
                # Programar descarga
                sync_task = {
                    'symbol': symbol,
                    'timeframe': tf,
                    'bars': self.config['bars_optimal'][tf],
                    'priority': 'SYNC_CRITICAL',
                    'reason': 'gap_detected' if not self._has_minimal_data(symbol, tf) else 'forced_update'
                }
                sync_result['sync_tasks'].append(sync_task)
                sync_result['gaps_detected'].append(f"{symbol}_{tf}")
        
        # Ejecutar descargas de sincronización si hay gaps
        if sync_result['sync_tasks']:
            print(f"   📥 Ejecutando {len(sync_result['sync_tasks'])} descargas de sincronización...")
            download_results = self._execute_parallel_downloads(sync_result['sync_tasks'], mode='sync')
            
            # Procesar resultados
            successful_downloads = sum(1 for r in download_results.values() if r.get('success', False))
            sync_result['downloads_executed'] = successful_downloads
            
            # Actualizar estado de datos
            self._update_data_status(download_results)
            
            print(f"   ✅ Sincronización: {successful_downloads}/{len(sync_result['sync_tasks'])} exitosas")
        else:
            print(f"   ✅ {symbol} ya sincronizado - no se requieren descargas")
        
        # Evaluar alineación final
        final_readiness = self.get_data_readiness(symbol, timeframes)
        if final_readiness['analysis_capability'] in ['FULL', 'PARTIAL']:
            sync_result['alignment_status'] = 'SYNCHRONIZED'
        else:
            sync_result['alignment_status'] = 'FAILED'
        
        sync_result['timeframes_processed'] = len(timeframes)
        
        # Log de SLUC v2.1
        self._log_sync_operation(sync_result)
        
        return sync_result
    
    def get_multi_tf_cache_status(self) -> Dict[str, Any]:
        """
        📊 ESTADO DEL CACHE MULTI-TIMEFRAME
        
        Analiza el estado del cache desde perspectiva multi-timeframe,
        identificando patrones de uso y optimizaciones posibles.
        
        Returns:
            Dict con análisis del cache multi-TF
        """
        cache_analysis = {
            'total_symbols': len(self.data_status),
            'timeframe_coverage': {},
            'cache_efficiency': {},
            'recommendations': [],
            'optimization_opportunities': []
        }
        
        # Analizar cobertura por timeframe
        for tf in ['H4', 'M15', 'M5', 'H1', 'D1', 'M30']:
            symbols_with_tf = 0
            for symbol_data in self.data_status.values():
                if tf in symbol_data and symbol_data[tf]['available']:
                    symbols_with_tf += 1
            
            coverage_pct = (symbols_with_tf / len(self.data_status) * 100) if self.data_status else 0
            cache_analysis['timeframe_coverage'][tf] = {
                'symbols_count': symbols_with_tf,
                'coverage_percentage': coverage_pct,
                'status': 'GOOD' if coverage_pct >= 70 else 'NEEDS_IMPROVEMENT'
            }
        
        # Calcular eficiencia de cache
        total_data_points = 0
        optimal_data_points = 0
        
        for symbol, timeframes in self.data_status.items():
            for tf, data_info in timeframes.items():
                if data_info['available']:
                    total_data_points += data_info['bars_count']
                    if self._has_optimal_data(symbol, tf):
                        optimal_data_points += data_info['bars_count']
        
        efficiency = (optimal_data_points / total_data_points * 100) if total_data_points > 0 else 0
        cache_analysis['cache_efficiency'] = {
            'total_bars': total_data_points,
            'optimal_bars': optimal_data_points,
            'efficiency_percentage': efficiency,
            'status': 'EXCELLENT' if efficiency >= 80 else 'GOOD' if efficiency >= 60 else 'NEEDS_OPTIMIZATION'
        }
        
        # Generar recomendaciones
        if efficiency < 60:
            cache_analysis['recommendations'].append("🔧 Ejecutar enhancement para optimizar datos")
        
        low_coverage_tfs = [tf for tf, data in cache_analysis['timeframe_coverage'].items() 
                           if data['coverage_percentage'] < 50]
        if low_coverage_tfs:
            cache_analysis['recommendations'].append(f"📈 Mejorar cobertura en: {', '.join(low_coverage_tfs)}")
        
        return cache_analysis
    
    def _log_multitf_detection(self, detection_results: Dict[str, Any]):
        """📝 Log estructurado para detección multi-TF (SLUC v2.1)"""
        try:
            # Integración SLUC v2.1 para eventos de detección
            if UNIFIED_MEMORY_AVAILABLE and self.unified_memory:
                event_data = {
                    'event_type': 'multi_tf_detection',
                    'symbols_analyzed': detection_results['symbols_analyzed'],
                    'timeframes_required': detection_results['timeframes_required'],
                    'sync_status': detection_results['sync_status'],
                    'ready_symbols': len([s for s, status in detection_results['readiness_summary'].items() if status == 'READY']),
                    'timestamp': datetime.now()
                }
                
                # Log con SLUC v2.1
                update_market_memory(
                    'multi_tf_detection',
                    event_data,
                    context_type='data_management'
                )
                
        except Exception as e:
            print(f"⚠️ Error logging detección multi-TF: {e}")
    
    def _log_sync_operation(self, sync_result: Dict[str, Any]):
        """📝 Log estructurado para sincronización (SLUC v2.1)"""
        try:
            # Integración SLUC v2.1 para eventos de sincronización
            if UNIFIED_MEMORY_AVAILABLE and self.unified_memory:
                event_data = {
                    'event_type': 'multi_tf_sync',
                    'symbol': sync_result['symbol'],
                    'timeframes_processed': sync_result['timeframes_processed'],
                    'downloads_executed': sync_result['downloads_executed'],
                    'alignment_status': sync_result['alignment_status'],
                    'gaps_detected': len(sync_result['gaps_detected']),
                    'timestamp': datetime.now()
                }
                
                # Log con SLUC v2.1
                update_market_memory(
                    'multi_tf_sync',
                    event_data,
                    context_type='data_management'
                )
                
        except Exception as e:
            print(f"⚠️ Error logging sincronización multi-TF: {e}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """📈 Obtener resumen de performance del data manager"""
        
        return {
            'warm_up_completed': self.warm_up_completed,
            'enhancement_active': self.enhancement_active,
            'metrics': self.performance_metrics.copy(),
            'data_symbols_count': len(self.data_status),
            'total_timeframes': sum(len(tfs) for tfs in self.data_status.values()),
            'system_status': 'OPERATIONAL' if self.warm_up_completed else 'WARMING_UP'
        }
    
    def stop_enhancement(self):
        """🛑 Detener enhancement en background"""
        
        if self.enhancement_active:
            print("🛑 Deteniendo background enhancement...")
            self.enhancement_active = False
            if self.enhancement_thread and self.enhancement_thread.is_alive():
                self.enhancement_thread.join(timeout=10)
            print("✅ Background enhancement detenido")

# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def create_ict_data_manager(downloader=None) -> ICTDataManager:
    """🏭 Factory para crear ICT Data Manager"""
    return ICTDataManager(downloader=downloader)

def get_default_warm_up_config() -> Dict[str, Any]:
    """📋 Obtener configuración por defecto para warm-up"""
    return {
        'symbols': ICT_DATA_CONFIG['symbols_critical'],
        'timeframes': ICT_DATA_CONFIG['timeframes_critical'],
        'target_time': 30  # segundos
    }

if __name__ == "__main__":
    """🧪 Test básico del ICT Data Manager"""
    
    print("🧪 Test ICT Data Manager")
    print("=" * 50)
    
    # Crear manager
    data_manager = ICTDataManager()
    
    # Simular warm-up sin downloader real
    print("\n📊 Configuración cargada:")
    print(f"Símbolos críticos: {data_manager.config['symbols_critical']}")
    print(f"Timeframes críticos: {data_manager.config['timeframes_critical']}")
    print(f"Datos mínimos H4: {data_manager.config['bars_minimal']['H4']} velas")
    print(f"Datos mínimos M15: {data_manager.config['bars_minimal']['M15']} velas")
    
    # Test de readiness check
    readiness = data_manager.get_data_readiness('EURUSD', ['H4', 'M15', 'M5'])
    print(f"\n📈 Data readiness test: {readiness['analysis_capability']}")
    
    print("\n✅ ICT Data Manager test completado")
