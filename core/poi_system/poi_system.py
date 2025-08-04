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

# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log, log_poi

# Importar componentes POI existentes
try:
    from .poi_detector import encontrar_pois_multiples_para_dashboard
    # Funciones específicas se importarán si se necesitan
    poi_components_available = True
except ImportError as e:
    enviar_senal_log("WARNING", f"Componentes POI no disponibles: {e}", "poi_system")
    poi_components_available = False

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

# Función de conveniencia para obtener instancia del sistema
_poi_system_instance = None

def get_poi_system(mt5_manager=None):
    """
    Obtiene una instancia del POI System (singleton).

    Args:
        mt5_manager: Manager de MT5 para integración

    Returns:
        Instancia de POISystem
    """
    global _poi_system_instance

    if _poi_system_instance is None:
        _poi_system_instance = POISystem(mt5_manager)
    elif mt5_manager and _poi_system_instance.mt5_manager is None:
        _poi_system_instance.mt5_manager = mt5_manager

    return _poi_system_instance
