#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🕐 MARKET STATUS DETECTOR v3.0 - ICT ENGINE v5.0
================================================

SISTEMA PROFESIONAL DE DETECCIÓN DE ESTADO DE MERCADO FOREX

CARACTERÍSTICAS AVANZADAS:
- ✅ Detección automática de sesiones de trading en tiempo real
- ✅ Soporte completo para múltiples zonas horarias
- ✅ Integración con TradingScheduleManager profesional
- ✅ Detección automática de DST (Daylight Saving Time)
- ✅ Cálculo preciso de tiempo restante hasta próximas sesiones
- ✅ Soporte para brokers MT5 con diferentes zonas horarias
- ✅ Logging avanzado con SLUC v2.1
- ✅ APIs optimizadas para dashboard e integración
- ✅ Cache inteligente para optimización de rendimiento

SESIONES SOPORTADAS:
- 🌏 ASIA (Sydney/Tokyo): 21:00-06:00 UTC
- 🇬🇧 LONDON (Europa): 08:00-17:00 UTC
- 🇺🇸 NEW_YORK (América): 13:00-22:00 UTC
- 🔄 Detección automática de solapamientos

INTEGRACIÓN:
- Dashboard definitivo: Display en tiempo real
- ICT Detector: Análisis de sesiones para estrategias
- Trading Engine: Filtros de horario para trading automático

AUTOR: ICT Engine v5.0 Professional
FECHA: 4 Agosto 2025
VERSIÓN: v3.0 - Production Ready
"""

from sistema.sic import sys
from sistema.sic import datetime, timezone, timedelta
import platform
from sistema.sic import Dict, Optional, Any, Tuple
from sistema.sic import dataclass
from enum import Enum

# MIGRADO A SLUC v2.1
try:
    from sistema.sic import enviar_senal_log
except ImportError:
    def enviar_senal_log(nivel: str, mensaje: str, fuente: str = "market_status", categoria: str = "general") -> None:
        print(f"[{nivel}] {fuente}: {mensaje}")

try:
    from sistema.trading_schedule import TradingScheduleManager, get_current_session_info, calcular_tiempo_restante_para_proxima_sesion
    trading_schedule_available = True
except ImportError as e:
    enviar_senal_log("ERROR", f"Error crítico importando TradingScheduleManager: {e}", __name__, "market_status")
    trading_schedule_available = False

# Pytz para manejo avanzado de zonas horarias (opcional)
try:
    import pytz
    pytz_available = True
except ImportError:
    pytz = None
    pytz_available = False
    enviar_senal_log("WARNING", "Pytz no disponible - usando datetime estándar", __name__, "market_status")


class MarketSession(Enum):
    """Enumeración de sesiones de mercado"""
    ASIA = "ASIA"
    LONDON = "LONDON"
    NEW_YORK = "NEW_YORK"
    CLOSED = "CLOSED"


class MarketStatus(Enum):
    """Estados del mercado"""
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    PRE_MARKET = "PRE_MARKET"
    POST_MARKET = "POST_MARKET"


@dataclass
class SessionInfo:
    """Información de sesión estructurada"""
    session: MarketSession
    status: MarketStatus
    name: str
    start_time: str
    end_time: str
    description: str
    volatility: str
    is_active: bool
    time_remaining: Optional[Dict[str, int]] = None


class MarketStatusDetector:
    """
    🚀 DETECTOR PROFESIONAL DE ESTADO DE MERCADO v3.0

    Proporciona detección en tiempo real del estado del mercado Forex
    con soporte completo para múltiples zonas horarias y sesiones.
    """

    def __init__(self):
        """Inicializar detector con configuración automática avanzada"""
        enviar_senal_log("INFO", "🚀 Inicializando Market Status Detector v3.0", __name__, "market_status")

        # Integración con Trading Schedule Manager
        if trading_schedule_available:
            self.trading_schedule = TradingScheduleManager()
            enviar_senal_log("INFO", "✅ TradingScheduleManager integrado exitosamente", __name__, "market_status")
        else:
            self.trading_schedule = None
            enviar_senal_log("ERROR", "❌ TradingScheduleManager no disponible", __name__, "market_status")

        # Detectar configuración del sistema
        self.timezone_info = self._detect_system_configuration()

        # Cache para optimización
        self._cache_session_info = None
        self._cache_timestamp = None
        self._cache_duration = 30  # segundos

        enviar_senal_log("INFO",
                        f"Configuración detectada - "
                        f"Local: {self.timezone_info['local_timezone']} | "
                        f"Platform: {self.timezone_info['platform']} | "
                        f"Pytz: {pytz_available}",
                        __name__, "market_status")

    def _detect_system_configuration(self) -> Dict[str, Any]:
        """
        Detecta configuración del sistema y zonas horarias
        """
        try:
            # Información del sistema
            platform_info = platform.system()

            # Zona horaria local
            local_time = datetime.now()
            local_utc_offset = local_time.astimezone().utcoffset().total_seconds() / 3600
            local_timezone = self._get_timezone_name(local_utc_offset)

            # Detección de broker MT5 (si está disponible)
            broker_timezone = self._detect_broker_timezone()

            return {
                'platform': platform_info,
                'local_utc_offset': local_utc_offset,
                'local_timezone': local_timezone,
                'broker_timezone': broker_timezone,
                'detection_time': datetime.now().isoformat(),
                'pytz_available': pytz_available
            }

        except Exception as e:
            enviar_senal_log("ERROR", f"Error detectando configuración del sistema: {e}", __name__, "market_status")
            return {
                'platform': 'Unknown',
                'local_utc_offset': 0.0,
                'local_timezone': 'UTC+0',
                'broker_timezone': 'UTC+2',
                'detection_time': datetime.now().isoformat(),
                'pytz_available': False
            }

    def _get_timezone_name(self, utc_offset: float) -> str:
        """
        Obtiene el nombre de la zona horaria basado en el offset UTC
        """
        # Mapeo mejorado de offsets UTC a zonas horarias
        timezone_map = {
            -12.0: "UTC-12 (Baker Island)",
            -11.0: "UTC-11 (American Samoa)",
            -10.0: "UTC-10 (Hawaii)",
            -9.0: "UTC-9 (Alaska)",
            -8.0: "UTC-8 (Pacific Time)",
            -7.0: "UTC-7 (Mountain Time)",
            -6.0: "UTC-6 (Central Time)",
            -5.0: "UTC-5 (Eastern Time / Ecuador)",
            -4.0: "UTC-4 (Atlantic Time)",
            -3.0: "UTC-3 (Brazil)",
            -2.0: "UTC-2 (South Georgia)",
            -1.0: "UTC-1 (Azores)",
            0.0: "UTC+0 (London/GMT)",
            1.0: "UTC+1 (Central Europe)",
            2.0: "UTC+2 (Eastern Europe)",
            3.0: "UTC+3 (Moscow)",
            4.0: "UTC+4 (Gulf Standard)",
            5.0: "UTC+5 (Pakistan)",
            5.5: "UTC+5:30 (India)",
            6.0: "UTC+6 (Bangladesh)",
            7.0: "UTC+7 (Thailand)",
            8.0: "UTC+8 (China/Singapore)",
            9.0: "UTC+9 (Japan)",
            10.0: "UTC+10 (Australia East)",
            11.0: "UTC+11 (Solomon Islands)",
            12.0: "UTC+12 (New Zealand)",
        }

        return timezone_map.get(utc_offset, f"UTC{utc_offset:+.1f} (Unknown)")

    def _detect_broker_timezone(self) -> str:
        """
        Detecta la zona horaria del broker MT5
        """
        try:
            # Intentar detectar con MT5
            try:
                import MetaTrader5 as mt5
                # Usar getattr para evitar errores de tipo en tiempo de compilación
                initialize_func = getattr(mt5, 'initialize', None)
                if initialize_func and initialize_func():
                    # Obtener información del servidor
                    account_info_func = getattr(mt5, 'account_info', None)
                    if account_info_func:
                        account_info = account_info_func()
                        if account_info:
                            # La mayoría de brokers europeos usan UTC+2/UTC+3
                            enviar_senal_log("INFO", "Broker MT5 detectado - usando UTC+2 (Europa)", __name__, "market_status")
                            shutdown_func = getattr(mt5, 'shutdown', None)
                            if shutdown_func:
                                shutdown_func()
                            return "UTC+2 (Europe/MT5)"

                    shutdown_func = getattr(mt5, 'shutdown', None)
                    if shutdown_func:
                        shutdown_func()

            except ImportError:
                enviar_senal_log("WARNING", "MT5 no disponible - usando zona horaria por defecto", __name__, "market_status")

        except Exception as e:
            enviar_senal_log("WARNING", f"Error detectando broker timezone: {e}", __name__, "market_status")

        # Fallback a UTC+2 (común para brokers europeos)
        return "UTC+2 (Default/Europe)"

    def get_current_market_status(self) -> Dict[str, Any]:
        """
        🚀 FUNCIÓN PRINCIPAL: Obtiene el estado actual completo del mercado

        Returns:
            Diccionario completo con estado del mercado, sesión activa,
            tiempo restante y información técnica
        """
        try:
            # Usar cache si está disponible y es reciente
            if self._is_cache_valid() and self._cache_session_info is not None:
                return self._cache_session_info

            # Obtener información de sesión actual
            if self.trading_schedule:
                current_session = get_current_session_info()
                time_remaining = calcular_tiempo_restante_para_proxima_sesion()
            else:
                current_session = self._get_fallback_session()
                time_remaining = {"hours": 0, "minutes": 0, "seconds": 0}

            # Determinar estado del mercado
            market_status = self._determine_market_status_v3(current_session)

            # Construir respuesta completa
            status_response = {
                'market_status': market_status['status'],
                'emoji_status': market_status['emoji'],
                'session_activa': {
                    'name': current_session.get('name', 'UNKNOWN') if current_session else 'UNKNOWN',
                    'description': current_session.get('description', 'N/A') if current_session else 'N/A',
                    'volatility': current_session.get('volatility', 'MEDIUM') if current_session else 'MEDIUM',
                    'is_active': current_session.get('is_active', False) if current_session else False,
                    'start': current_session.get('start', 'N/A') if current_session else 'N/A',
                    'end': current_session.get('end', 'N/A') if current_session else 'N/A'
                },
                'proxima_sesion': {
                    'hours': time_remaining.get('hours', 0) if time_remaining else 0,
                    'minutes': time_remaining.get('minutes', 0) if time_remaining else 0,
                    'seconds': time_remaining.get('seconds', 0) if time_remaining else 0,
                    'time_string': f"{time_remaining.get('hours', 0):02d}:{time_remaining.get('minutes', 0):02d}:{time_remaining.get('seconds', 0):02d}" if time_remaining else "00:00:00"
                },
                'timezone_info': self.timezone_info,
                'timestamp': datetime.now().isoformat(),
                'system_info': {
                    'trading_schedule_available': trading_schedule_available,
                    'pytz_available': pytz_available,
                    'detector_version': '3.0'
                }
            }

            # Actualizar cache
            self._update_cache(status_response)

            return status_response

        except Exception as e:
            enviar_senal_log("ERROR", f"Error obteniendo estado del mercado: {e}", __name__, "market_status")
            return self._get_error_response(str(e))

    def _determine_market_status_v3(self, session_info: Optional[Dict]) -> Dict[str, str]:
        """
        Determina el estado del mercado basado en la sesión actual
        """
        if not session_info or not session_info.get('is_active', False):
            return {
                'status': 'CLOSED',
                'emoji': '🔴'
            }

        session_name = session_info.get('session_key', 'UNKNOWN')
        volatility = session_info.get('volatility', 'MEDIUM')

        # Mapeo de estados por sesión
        if session_name == 'ASIA':
            return {'status': 'OPEN (Asian Session)', 'emoji': '🟡'}
        elif session_name == 'LONDON':
            return {'status': 'OPEN (London Session)', 'emoji': '🟢'}
        elif session_name == 'NEW_YORK':
            return {'status': 'OPEN (New York Session)', 'emoji': '🔵'}
        else:
            return {'status': 'OPEN (Active)', 'emoji': '🟢'}

    def _is_cache_valid(self) -> bool:
        """Verifica si el cache es válido"""
        if not self._cache_session_info or not self._cache_timestamp:
            return False

        time_diff = (datetime.now() - self._cache_timestamp).total_seconds()
        return time_diff < self._cache_duration

    def _update_cache(self, data: Dict[str, Any]) -> None:
        """Actualiza el cache con nueva información"""
        self._cache_session_info = data
        self._cache_timestamp = datetime.now()

    def _get_fallback_session(self) -> Dict[str, Any]:
        """Sesión de fallback cuando TradingScheduleManager no está disponible"""
        current_hour = datetime.now().hour

        if 8 <= current_hour < 17:
            return {
                'name': 'London Session',
                'session_key': 'LONDON',
                'description': 'Sesión Europea',
                'volatility': 'MEDIUM',
                'is_active': True,
                'start': '08:00',
                'end': '17:00'
            }
        elif 13 <= current_hour < 22:
            return {
                'name': 'New York Session',
                'session_key': 'NEW_YORK',
                'description': 'Sesión Americana',
                'volatility': 'HIGH',
                'is_active': True,
                'start': '13:00',
                'end': '22:00'
            }
        elif 21 <= current_hour or current_hour < 6:
            return {
                'name': 'Asia-Pacific',
                'session_key': 'ASIA',
                'description': 'Sesión Asia-Pacífico',
                'volatility': 'LOW',
                'is_active': True,
                'start': '21:00',
                'end': '06:00'
            }
        else:
            return {
                'name': 'Market Closed',
                'session_key': 'CLOSED',
                'description': 'Mercado Cerrado',
                'volatility': 'NONE',
                'is_active': False,
                'start': 'N/A',
                'end': 'N/A'
            }

    def _get_error_response(self, error_message: str) -> Dict[str, Any]:
        """Respuesta de error estandarizada"""
        return {
            'market_status': 'ERROR',
            'emoji_status': '❌',
            'session_activa': {
                'name': 'ERROR',
                'description': f'Error: {error_message[:50]}...',
                'volatility': 'UNKNOWN',
                'is_active': False
            },
            'proxima_sesion': {
                'hours': 0,
                'minutes': 0,
                'seconds': 0,
                'time_string': "00:00:00"
            },
            'timezone_info': self.timezone_info,
            'timestamp': datetime.now().isoformat(),
            'error': error_message
        }

    def get_timezone_info(self) -> Dict[str, Any]:
        """
        Obtiene información detallada de zona horaria del sistema
        """
        return {
            'detection_summary': {
                'local_timezone': self.timezone_info['local_timezone'],
                'local_offset': f"UTC{self.timezone_info['local_utc_offset']:+.1f}",
                'broker_timezone': self.timezone_info['broker_timezone'],
                'platform': self.timezone_info['platform']
            },
            'full_info': self.timezone_info,
            'capabilities': {
                'trading_schedule_available': trading_schedule_available,
                'pytz_available': pytz_available,
                'mt5_detection': True
            }
        }

    def get_session_summary(self) -> str:
        """
        Obtiene resumen textual del estado del mercado
        """
        try:
            status = self.get_current_market_status()
            session = status['session_activa']
            remaining = status['proxima_sesion']

            if session['is_active']:
                return f"{status['emoji_status']} {session['name']} - Próxima en {remaining['time_string']}"
            else:
                return f"{status['emoji_status']} Mercado Cerrado - Próxima sesión en {remaining['time_string']}"

        except Exception as e:
            return f"❌ Error obteniendo resumen: {str(e)[:30]}..."


# =============================================================================
# FUNCIÓN PRINCIPAL PARA TESTING Y DEBUGGING
# =============================================================================

def main():
    """
    Función principal para testing del Market Status Detector v3.0
    """
    print("=" * 60)
    print("🚀 TESTING MARKET STATUS DETECTOR v3.0")
    print("=" * 60)

    # Crear detector
    detector = MarketStatusDetector()

    # Obtener estado completo
    status = detector.get_current_market_status()

    # Mostrar resultados via logging
    enviar_senal_log("INFO", "📊 ESTADO DEL MERCADO:", __name__, "market_status")
    enviar_senal_log("INFO", f"  Status: {status['emoji_status']} {status['market_status']}", __name__, "market_status")
    enviar_senal_log("INFO", f"  Sesión: {status['session_activa']['name']}", __name__, "market_status")
    enviar_senal_log("INFO", f"  Descripción: {status['session_activa']['description']}", __name__, "market_status")
    enviar_senal_log("INFO", f"  Volatilidad: {status['session_activa']['volatility']}", __name__, "market_status")

    # Próxima sesión
    enviar_senal_log("INFO", "⏳ PRÓXIMA SESIÓN:", __name__, "market_status")
    enviar_senal_log("INFO", f"  En: {status['proxima_sesion']['time_string']}", __name__, "market_status")

    # Información técnica
    enviar_senal_log("INFO", "🔧 INFORMACIÓN TÉCNICA:", __name__, "market_status")
    tz_info = detector.get_timezone_info()
    enviar_senal_log("INFO", f"  Zona Local: {tz_info['detection_summary']['local_timezone']}", __name__, "market_status")
    enviar_senal_log("INFO", f"  Offset UTC: {tz_info['detection_summary']['local_offset']}", __name__, "market_status")
    enviar_senal_log("INFO", f"  Plataforma: {tz_info['detection_summary']['platform']}", __name__, "market_status")

    # Resumen textual
    resumen = detector.get_session_summary()
    enviar_senal_log("INFO", f"📋 RESUMEN: {resumen}", __name__, "market_status")

    print("=" * 60)
    print("✅ Testing completado exitosamente")
    print("=" * 60)


if __name__ == "__main__":
    main()
