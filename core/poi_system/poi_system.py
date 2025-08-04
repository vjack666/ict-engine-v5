"""
POI System - Sistema Principal de Puntos de Interés
==================================================

Sistema central que maneja todos los aspectos de Points of Interest (POI),
integrándose con el MT5DataManager y proporcionando una interfaz unificada.

Autor: Sistema Sentinel Grid v3.3.3.3.3
Fecha: 2025-08-03
"""

from typing import Dict, List, Any, Optional
import pandas as pd
from dataclasses import dataclass
from datetime import datetime
import threading

# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log, log_poi

# =============================================================================
# SINGLETON PATTERN PARA POI SYSTEM
# =============================================================================

# Variable global para la instancia única del sistema POI
_poi_system_instance: Optional['POISystemManager'] = None

# Lock para thread-safety del singleton
_poi_system_lock = threading.Lock()

# Cache global de POIs para optimización
_poi_global_cache: Dict[str, Any] = {}

# Estadísticas globales del sistema
_poi_system_stats = {
    'initialization_time': None,
    'total_detections': 0,
    'cache_hits': 0,
    'cache_misses': 0,
    'last_reset': None
}

# Importar componentes POI existentes
try:
    from .poi_detector import encontrar_pois_multiples_para_dashboard
    # Funciones específicas se importarán si se necesitan
    poi_components_available = True
except ImportError as e:
    enviar_senal_log("WARNING", f"Componentes POI no disponibles: {e}", "poi_system")
    poi_components_available = False

class POISystemManager:
    """
    🎯 MANAGER SINGLETON DEL SISTEMA POI
    ==================================

    Esta clase ES EL PROPÓSITO de _poi_system_instance.

    Responsabilidades:
    - Una sola instancia para todo el sistema
    - Cache inteligente de detecciones POI
    - Integración con dashboard y componentes
    - Thread-safety para operaciones concurrentes
    - Gestión de estado y métricas globales
    """

    def __init__(self):
        """Inicialización privada (solo llamada por get_instance)."""
        self._initialized = False
        self._poi_detector = None
        self._cache = {}
        self._stats = {
            'total_detections': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'initialization_time': None
        }

        # Logging
        try:
            enviar_senal_log("INFO", "🎯 POI System Manager inicializado", "poi_system")
        except ImportError:
            print("🎯 POI System Manager inicializado")

    def initialize(self, force_reinit: bool = False) -> bool:
        """
        🏗️ INICIALIZACIÓN LAZY DEL SISTEMA POI

        Args:
            force_reinit: Forzar reinicialización

        Returns:
            bool: True si la inicialización fue exitosa
        """
        if self._initialized and not force_reinit:
            return True

        try:
            start_time = datetime.now()

            # Inicializar detector POI
            if not self._poi_detector:
                try:
                    from .poi_detector import encontrar_pois_multiples_para_dashboard
                    self._poi_detector = encontrar_pois_multiples_para_dashboard
                except ImportError:
                    try:
                        from core.poi_system.poi_detector import encontrar_pois_multiples_para_dashboard
                        self._poi_detector = encontrar_pois_multiples_para_dashboard
                    except ImportError:
                        enviar_senal_log("WARNING", "No se pudo cargar detector POI específico", "poi_system")
                        self._poi_detector = self._detector_fallback

            # Inicializar cache
            self._cache = {}
            global _poi_global_cache
            _poi_global_cache = {}

            # Marcar como inicializado
            self._initialized = True

            # Registrar tiempo de inicialización
            init_time = (datetime.now() - start_time).total_seconds()
            self._stats['initialization_time'] = init_time
            global _poi_system_stats
            _poi_system_stats['initialization_time'] = init_time

            enviar_senal_log("INFO", f"✅ POI System Manager inicializado en {init_time:.3f}s", "poi_system")
            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error inicializando POI System Manager: {e}", "poi_system")
            self._initialized = False
            return False

    def _detector_fallback(self, df, current_price=None, **kwargs):
        """Detector de fallback si no se puede cargar el principal."""
        enviar_senal_log("WARNING", "Usando detector POI de fallback", "poi_system")
        return []  # Retorna lista vacía como fallback

    def is_initialized(self) -> bool:
        """Verificar si está inicializado."""
        return self._initialized

    def get_detector(self):
        """Obtener instancia del detector POI."""
        if not self._initialized:
            self.initialize()
        return self._poi_detector

    def detect_pois(self, df, timeframe: str = "M15", current_price: Optional[float] = None, **kwargs) -> List[Dict]:
        """
        🎯 MÉTODO PRINCIPAL DE DETECCIÓN POI CON CACHE

        Args:
            df: DataFrame con datos OHLC
            timeframe: Timeframe de análisis
            current_price: Precio actual opcional
            **kwargs: Parámetros adicionales

        Returns:
            Lista de POIs detectados
        """
        global _poi_system_stats, _poi_global_cache

        if not self._initialized:
            if not self.initialize():
                return []

        try:
            # Generar cache key
            cache_key = f"poi_{timeframe}_{current_price}_{hash(str(kwargs))}"

            # Verificar cache
            if cache_key in self._cache:
                self._stats['cache_hits'] += 1
                _poi_system_stats['cache_hits'] += 1
                return self._cache[cache_key]

            # Cache miss - realizar detección
            self._stats['cache_misses'] += 1
            _poi_system_stats['cache_misses'] += 1

            # Usar detector
            if callable(self._poi_detector):
                # Asegurar que current_price sea float o usar valor por defecto
                safe_current_price = current_price if current_price is not None else 0.0
                pois = self._poi_detector(df, current_price=safe_current_price, **kwargs)
            else:
                pois = []

            # Almacenar en cache
            self._cache[cache_key] = pois
            _poi_global_cache[cache_key] = pois

            # Actualizar estadísticas
            self._stats['total_detections'] += 1
            _poi_system_stats['total_detections'] += 1

            return pois

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error en detección POI: {e}", "poi_system")
            return []

    def get_stats(self) -> dict:
        """Obtener estadísticas del sistema."""
        global _poi_system_stats
        return {
            'instance_stats': self._stats.copy(),
            'global_stats': _poi_system_stats.copy(),
            'cache_size': len(self._cache),
            'initialized': self._initialized
        }

    def reset_cache(self):
        """Limpiar cache del sistema."""
        global _poi_global_cache
        self._cache.clear()
        _poi_global_cache.clear()
        enviar_senal_log("INFO", "🧹 Cache POI limpiado", "poi_system")

    def shutdown(self):
        """Apagar el sistema de manera limpia."""
        self.reset_cache()
        self._initialized = False
        enviar_senal_log("INFO", "🔚 POI System Manager detenido", "poi_system")

@dataclass
class POIResult:
    """Resultado unificado de análisis POI."""
    symbol: str
    timeframe: str
    timestamp: datetime
    pois_encontrados: List[Dict[str, Any]]
    calidad_promedio: float
    riesgo_total: float
    recomendacion: str
    detalles: Dict[str, Any]

class POISystem:
    """
    Sistema principal de manejo de POI.
    Centraliza toda la lógica de Points of Interest.
    """

    def __init__(self, mt5_manager=None):
        """
        Inicializa el sistema POI.

        Args:
            mt5_manager: Instancia del MT5DataManager para datos
        """
        self.mt5_manager = mt5_manager
        self.configuracion = {
            'min_calidad_poi': 0.6,
            'max_riesgo_aceptable': 0.8,
            'timeframes_soportados': ['M1', 'M5', 'M15', 'H1', 'H4', 'D1'],
            'simbolos_principales': ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCAD']
        }

        enviar_senal_log("INFO", "POISystem inicializado correctamente", "poi_system")

    def analizar_pois_completo(self,
                              symbol: str = "EURUSD",
                              timeframe: str = "M15",
                              lookback: int = 1000) -> Optional[POIResult]:
        """
        Realiza un análisis completo de POIs para un símbolo y timeframe.

        Args:
            symbol: Símbolo a analizar
            timeframe: Timeframe para el análisis
            lookback: Número de barras a analizar

        Returns:
            POIResult con el análisis completo o None si falla
        """
        try:
            enviar_senal_log("INFO", f"🎯 Iniciando análisis POI completo: {symbol} {timeframe}", "poi_system")

            # Validar parámetros
            if not self._validar_parametros(symbol, timeframe):
                return None

            # Obtener datos de MT5
            if not self.mt5_manager:
                enviar_senal_log("ERROR", "MT5Manager no disponible para análisis POI", "poi_system")
                return None

            df = self.mt5_manager.get_historical_data(symbol, timeframe, lookback)
            if df is None or df.empty:
                enviar_senal_log("ERROR", f"No se pudieron obtener datos para {symbol} {timeframe}", "poi_system")
                return None

            # Realizar análisis POI
            if not poi_components_available:
                enviar_senal_log("WARNING", "Componentes POI no disponibles, simulando análisis", "poi_system")
                return self._simular_analisis_poi(symbol, timeframe, df)

            # Análisis real con componentes POI
            pois_encontrados = encontrar_pois_multiples_para_dashboard(df, current_price=df['close'].iloc[-1])

            if not pois_encontrados:
                enviar_senal_log("INFO", f"No se encontraron POIs para {symbol} {timeframe}", "poi_system")
                return self._crear_resultado_vacio(symbol, timeframe)

            # Calcular métricas de calidad y riesgo
            calidad_promedio = self._calcular_calidad_promedio(pois_encontrados)
            riesgo_total = self._calcular_riesgo_total(pois_encontrados)
            recomendacion = self._generar_recomendacion(calidad_promedio, riesgo_total)

            # Crear resultado
            resultado = POIResult(
                symbol=symbol,
                timeframe=timeframe,
                timestamp=datetime.now(),
                pois_encontrados=pois_encontrados,
                calidad_promedio=calidad_promedio,
                riesgo_total=riesgo_total,
                recomendacion=recomendacion,
                detalles={
                    'total_pois': len(pois_encontrados),
                    'barras_analizadas': len(df),
                    'componentes_disponibles': poi_components_available
                }
            )

            enviar_senal_log("INFO",
                           f"✅ Análisis POI completado: {len(pois_encontrados)} POIs encontrados",
                           "poi_system")

            return resultado

        except Exception as e:
            enviar_senal_log("ERROR", f"Error en análisis POI: {e}", "poi_system")
            return None

    def obtener_pois_para_dashboard(self,
                                   symbols: Optional[List[str]] = None,
                                   timeframes: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Obtiene POIs optimizados para mostrar en el dashboard.

        Args:
            symbols: Lista de símbolos a analizar
            timeframes: Lista de timeframes a analizar

        Returns:
            Dict con datos de POI formateados para dashboard
        """
        if symbols is None:
            symbols = self.configuracion['simbolos_principales'][:2]  # Limitar para dashboard
        if timeframes is None:
            timeframes = ['M15', 'H1']  # Timeframes más relevantes para dashboard

        resultados_dashboard = {
            'timestamp': datetime.now().isoformat(),
            'simbolos_analizados': [],
            'resumen_general': {},
            'alertas': [],
            'datos_detallados': {}
        }

        try:
            for symbol in symbols:
                for timeframe in timeframes:
                    resultado = self.analizar_pois_completo(symbol, timeframe, lookback=500)

                    if resultado:
                        key = f"{symbol}_{timeframe}"
                        resultados_dashboard['datos_detallados'][key] = {
                            'pois_count': len(resultado.pois_encontrados),
                            'calidad': resultado.calidad_promedio,
                            'riesgo': resultado.riesgo_total,
                            'recomendacion': resultado.recomendacion
                        }

                        # Generar alertas si es necesario
                        if resultado.calidad_promedio > 0.8:
                            resultados_dashboard['alertas'].append({
                                'tipo': 'HIGH_QUALITY_POI',
                                'symbol': symbol,
                                'timeframe': timeframe,
                                'mensaje': f"POIs de alta calidad detectados en {symbol} {timeframe}"
                            })

            # Generar resumen
            total_pois = sum(datos['pois_count'] for datos in resultados_dashboard['datos_detallados'].values())
            calidad_promedio_global = sum(datos['calidad'] for datos in resultados_dashboard['datos_detallados'].values()) / max(len(resultados_dashboard['datos_detallados']), 1)

            resultados_dashboard['resumen_general'] = {
                'total_pois_sistema': total_pois,
                'calidad_promedio_global': calidad_promedio_global,
                'simbolos_analizados': len(symbols) if symbols else 0,
                'timeframes_analizados': len(timeframes) if timeframes else 0,
                'estado_sistema': 'OPERATIVO' if poi_components_available else 'SIMULADO'
            }

            enviar_senal_log("INFO",
                           f"📊 Dashboard POI actualizado: {total_pois} POIs totales",
                           "poi_system")

            return resultados_dashboard

        except Exception as e:
            enviar_senal_log("ERROR", f"Error generando datos para dashboard: {e}", "poi_system")
            return resultados_dashboard

    def _validar_parametros(self, symbol: str, timeframe: str) -> bool:
        """Valida los parámetros de entrada."""
        if timeframe not in self.configuracion['timeframes_soportados']:
            enviar_senal_log("WARNING", f"Timeframe {timeframe} no soportado", "poi_system")
            return False
        return True

    def _simular_analisis_poi(self, symbol: str, timeframe: str, df: pd.DataFrame) -> POIResult:
        """Simula un análisis POI cuando los componentes no están disponibles."""
        import random

        # Simular POIs básicos
        num_pois = random.randint(2, 8)
        pois_simulados = []

        for i in range(num_pois):
            pois_simulados.append({
                'tipo': random.choice(['SUPPORT', 'RESISTANCE', 'PIVOT']),
                'precio': df['close'].iloc[random.randint(0, len(df)-1)],
                'fuerza': random.uniform(0.4, 0.9),
                'confirmacion': random.choice([True, False]),
                'timestamp': datetime.now().isoformat()
            })

        calidad = random.uniform(0.5, 0.85)
        riesgo = random.uniform(0.2, 0.7)

        return POIResult(
            symbol=symbol,
            timeframe=timeframe,
            timestamp=datetime.now(),
            pois_encontrados=pois_simulados,
            calidad_promedio=calidad,
            riesgo_total=riesgo,
            recomendacion=self._generar_recomendacion(calidad, riesgo),
            detalles={
                'total_pois': num_pois,
                'barras_analizadas': len(df),
                'modo': 'SIMULADO',
                'componentes_disponibles': False
            }
        )

    def _crear_resultado_vacio(self, symbol: str, timeframe: str) -> POIResult:
        """Crea un resultado vacío cuando no se encuentran POIs."""
        return POIResult(
            symbol=symbol,
            timeframe=timeframe,
            timestamp=datetime.now(),
            pois_encontrados=[],
            calidad_promedio=0.0,
            riesgo_total=0.0,
            recomendacion="SIN_POIS",
            detalles={
                'total_pois': 0,
                'barras_analizadas': 0,
                'componentes_disponibles': poi_components_available
            }
        )

    def _calcular_calidad_promedio(self, pois: List[Dict[str, Any]]) -> float:
        """Calcula la calidad promedio de los POIs."""
        if not pois:
            return 0.0

        calidades = [poi.get('fuerza', 0.5) for poi in pois]
        return sum(calidades) / len(calidades)

    def _calcular_riesgo_total(self, pois: List[Dict[str, Any]]) -> float:
        """Calcula el riesgo total basado en los POIs."""
        if not pois:
            return 0.0

        # Riesgo basado en número de POIs y sus características
        num_pois = len(pois)
        pois_no_confirmados = sum(1 for poi in pois if not poi.get('confirmacion', False))

        riesgo_base = min(num_pois / 10.0, 0.8)  # Más POIs = más riesgo
        riesgo_confirmacion = (pois_no_confirmados / num_pois) * 0.3

        return min(riesgo_base + riesgo_confirmacion, 1.0)

    def _generar_recomendacion(self, calidad: float, riesgo: float) -> str:
        """Genera una recomendación basada en calidad y riesgo."""
        if calidad >= 0.8 and riesgo <= 0.4:
            return "ALTA_CONFIANZA"
        elif calidad >= 0.6 and riesgo <= 0.6:
            return "MODERADA_CONFIANZA"
        elif calidad >= 0.4:
            return "BAJA_CONFIANZA"
        else:
            return "NO_RECOMENDADO"

# =============================================================================
# FUNCIONES DE ACCESO AL SINGLETON POI SYSTEM MANAGER
# =============================================================================

def get_poi_system_instance() -> POISystemManager:
    """
    🎯 FUNCIÓN PRINCIPAL DE ACCESO AL SINGLETON

    Esta función implementa el patrón Singleton thread-safe.
    Garantiza que solo exista UNA instancia del POI System.

    Returns:
        POISystemManager: Instancia única del sistema POI
    """
    global _poi_system_instance, _poi_system_lock

    # Double-check locking pattern para thread-safety
    if _poi_system_instance is None:
        with _poi_system_lock:
            if _poi_system_instance is None:
                _poi_system_instance = POISystemManager()

    return _poi_system_instance

def reset_poi_system_instance():
    """
    🔄 RESETEAR INSTANCIA DEL SISTEMA POI

    Útil para testing o cuando se necesita reinicializar completamente.
    """
    global _poi_system_instance, _poi_system_lock, _poi_global_cache, _poi_system_stats

    with _poi_system_lock:
        if _poi_system_instance:
            _poi_system_instance.shutdown()
        _poi_system_instance = None
        _poi_global_cache.clear()
        _poi_system_stats['last_reset'] = datetime.now()

def is_poi_system_initialized() -> bool:
    """
    ✅ VERIFICAR SI EL SISTEMA POI ESTÁ INICIALIZADO

    Returns:
        bool: True si el sistema está inicializado y listo
    """
    global _poi_system_instance
    return (_poi_system_instance is not None and
            _poi_system_instance.is_initialized())

def get_poi_system_stats() -> Dict[str, Any]:
    """
    📊 OBTENER ESTADÍSTICAS GLOBALES DEL SISTEMA POI

    Returns:
        Dict con estadísticas globales del sistema
    """
    global _poi_system_stats, _poi_system_instance

    stats = _poi_system_stats.copy()

    if _poi_system_instance:
        stats['instance_status'] = _poi_system_instance.get_stats()

    return stats

# =============================================================================
# FUNCIONES DE CONVENIENCIA PARA COMPATIBILIDAD CON CÓDIGO EXISTENTE
# =============================================================================

def poi_detect_wrapper(df, timeframe: str, current_price: Optional[float] = None, **kwargs) -> List[Dict]:
    """
    🔧 WRAPPER DE CONVENIENCIA PARA DETECCIÓN POI

    Mantiene compatibilidad con código existente que usa detección directa.
    """
    poi_system = get_poi_system_instance()
    return poi_system.detect_pois(df, timeframe, current_price, **kwargs)

def get_poi_detector_instance():
    """
    🎯 OBTENER INSTANCIA DEL DETECTOR POI

    Para compatibilidad con código que espera acceso directo al detector.
    """
    poi_system = get_poi_system_instance()
    if not poi_system.is_initialized():
        poi_system.initialize()
    return poi_system.get_detector()

def get_poi_system(mt5_manager=None):
    """
    🔧 FUNCIÓN DE COMPATIBILIDAD PARA CÓDIGO EXISTENTE

    Redirige al nuevo sistema singleton manteniendo la interfaz anterior.

    Args:
        mt5_manager: Manager de MT5 para integración (mantenido para compatibilidad)

    Returns:
        POISystemManager: Instancia del nuevo sistema POI
    """
    poi_system = get_poi_system_instance()

    # Inicializar si no está listo
    if not poi_system.is_initialized():
        poi_system.initialize()

    return poi_system
