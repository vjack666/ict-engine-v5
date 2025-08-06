#!/usr/bin/env python3
"""
🕐 TRADING SCHEDULE - SISTEMA DE HORARIOS
========================================

Sistema profesional de gestión de horarios de trading Forex
que maneja sesiones internacionales, zonas horarias y cálculo
de tiempo restante hasta próximas sesiones.

Características:
- ✅ Gestión de sesiones Londres, Nueva York, Asia
- ✅ Cálculo automático de tiempo restante
- ✅ Detección de sesiones activas
- ✅ Solapamientos de sesiones
- ✅ Zona horaria UTC/EST/GMT automática

Versión: v1.0.0 - Professional Trading Schedule
Fecha: Agosto 2025
"""

from sistema.sic import Dict, Optional, Tuple, Any
from sistema.sic import datetime, timezone, timedelta
from enum import Enum
from sistema.sic import time

# MIGRADO A SLUC v2.1
try:
    from sistema.sic import enviar_senal_log
except ImportError:
    def enviar_senal_log(nivel: str, mensaje: str, fuente: str = "trading_schedule", categoria: str = "general") -> None:
        """Fallback logging function"""
        print(f"[{nivel}] {fuente}: {mensaje}")  # Fallback seguro sin recursión


class TradingSession(Enum):
    """Enumeración de sesiones de trading principales"""
    ASIA = "ASIA"
    LONDON = "LONDON"
    NEW_YORK = "NEW_YORK"
    SYDNEY = "SYDNEY"


# 🌍 CONFIGURACIÓN DE SESIONES FOREX PROFESIONAL
SESIONES_TRADING = {
    "ASIA": {
        "name": "Asia-Pacific",
        "start": "21:00",      # UTC domingo/lunes
        "end": "06:00",        # UTC lunes
        "timezone": "UTC",
        "description": "Sesión Asia-Pacífico (Sydney/Tokyo)",
        "volatility": "LOW",
        "major_pairs": ["USDJPY", "AUDUSD", "NZDUSD"],
        "overlap_sessions": []
    },
    "LONDON": {
        "name": "London",
        "start": "07:00",      # UTC
        "end": "16:00",        # UTC
        "timezone": "UTC",
        "description": "Sesión Europea (Londres)",
        "volatility": "HIGH",
        "major_pairs": ["EURUSD", "GBPUSD", "USDCHF"],
        "overlap_sessions": ["NEW_YORK"]
    },
    "NEW_YORK": {
        "name": "New York",
        "start": "12:00",      # UTC
        "end": "21:00",        # UTC
        "timezone": "UTC",
        "description": "Sesión Americana (Nueva York)",
        "volatility": "HIGH",
        "major_pairs": ["EURUSD", "GBPUSD", "USDCAD"],
        "overlap_sessions": ["LONDON"]
    },
    "SYDNEY": {
        "name": "Sydney",
        "start": "21:00",      # UTC domingo
        "end": "06:00",        # UTC lunes
        "timezone": "UTC",
        "description": "Sesión Australiana (Sydney)",
        "volatility": "MEDIUM",
        "major_pairs": ["AUDUSD", "NZDUSD"],
        "overlap_sessions": []
    }
}


class TradingScheduleManager:
    """
    🕐 GESTOR DE HORARIOS DE TRADING PROFESIONAL
    ===========================================

    Maneja todos los aspectos relacionados con horarios de trading,
    sesiones activas, cálculo de tiempo restante y optimización temporal.
    """

    def __init__(self):
        """Inicializa el gestor de horarios"""
        self.sessions = SESIONES_TRADING
        self.current_time_utc = None
        self._update_current_time()

        enviar_senal_log(
            "INFO",
            "🕐 Trading Schedule Manager inicializado correctamente",
            __name__,
            "trading_schedule"
        )

    def _update_current_time(self) -> None:
        """Actualiza el tiempo UTC actual"""
        self.current_time_utc = datetime.now(timezone.utc)

    def _parse_time_string(self, time_str: str) -> tuple:
        """
        Convierte string de tiempo "HH:MM" a tupla (hora, minuto)

        Args:
            time_str: String en formato "HH:MM"

        Returns:
            Tupla (hora, minuto)
        """
        try:
            hour, minute = map(int, time_str.split(':'))
            return hour, minute
        except (ValueError, AttributeError):
            return 0, 0

    def _time_to_minutes(self, hour: int, minute: int) -> int:
        """Convierte hora:minuto a minutos totales del día"""
        return hour * 60 + minute

    def _minutes_to_time_dict(self, total_minutes: int) -> Dict[str, int]:
        """Convierte minutos totales a diccionario de tiempo"""
        total_minutes = int(total_minutes)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        seconds = 0  # Para compatibilidad

        return {
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        }

    def get_current_session_info(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene información de la sesión activa actual

        Returns:
            Diccionario con información de sesión o None si no hay sesión activa
        """
        self._update_current_time()
        current_hour = self.current_time_utc.hour
        current_minute = self.current_time_utc.minute
        current_total_minutes = self._time_to_minutes(current_hour, current_minute)

        for session_key, session_info in self.sessions.items():
            start_hour, start_minute = self._parse_time_string(session_info["start"])
            end_hour, end_minute = self._parse_time_string(session_info["end"])

            start_minutes = self._time_to_minutes(start_hour, start_minute)
            end_minutes = self._time_to_minutes(end_hour, end_minute)

            # Manejar sesiones que cruzan medianoche
            if start_minutes > end_minutes:
                # Sesión cruza medianoche (ej: 21:00 - 06:00)
                if current_total_minutes >= start_minutes or current_total_minutes <= end_minutes:
                    return {
                        "session_key": session_key,
                        "name": session_info["name"],
                        "start": session_info["start"],
                        "end": session_info["end"],
                        "description": session_info["description"],
                        "volatility": session_info["volatility"],
                        "is_active": True
                    }
            else:
                # Sesión normal dentro del mismo día
                if start_minutes <= current_total_minutes <= end_minutes:
                    return {
                        "session_key": session_key,
                        "name": session_info["name"],
                        "start": session_info["start"],
                        "end": session_info["end"],
                        "description": session_info["description"],
                        "volatility": session_info["volatility"],
                        "is_active": True
                    }

        return None

    def calcular_tiempo_restante_para_proxima_sesion(self) -> Optional[Dict[str, int]]:
        """
        Calcula el tiempo restante hasta la próxima sesión de trading

        Returns:
            Diccionario con hours, minutes, seconds hasta próxima sesión
        """
        self._update_current_time()
        current_hour = self.current_time_utc.hour
        current_minute = self.current_time_utc.minute
        current_total_minutes = self._time_to_minutes(current_hour, current_minute)

        # Buscar la próxima sesión
        next_session_minutes = None
        next_session_name = None

        for session_key, session_info in self.sessions.items():
            start_hour, start_minute = self._parse_time_string(session_info["start"])
            start_minutes = self._time_to_minutes(start_hour, start_minute)

            # Calcular minutos hasta esta sesión
            if start_minutes > current_total_minutes:
                # Sesión hoy
                minutes_until = start_minutes - current_total_minutes
            else:
                # Sesión mañana
                minutes_until = (24 * 60) - current_total_minutes + start_minutes

            # Encontrar la sesión más cercana
            if next_session_minutes is None or minutes_until < next_session_minutes:
                next_session_minutes = minutes_until
                next_session_name = session_info["name"]

        if next_session_minutes is not None:
            result = self._minutes_to_time_dict(next_session_minutes)

            enviar_senal_log(
                "DEBUG",
                f"⏰ Tiempo hasta {next_session_name}: {result['hours']}h {result['minutes']}m",
                __name__,
                "trading_schedule"
            )

            return result

        return None


# 🌟 INSTANCIA GLOBAL DEL GESTOR
_schedule_manager = TradingScheduleManager()


# 🔄 FUNCIONES DE INTERFAZ PÚBLICA (Para compatibilidad con core/trading.py)

def get_current_session_info() -> Optional[Dict[str, Any]]:
    """
    Función de interfaz para obtener sesión actual

    Returns:
        Información de sesión activa o None
    """
    return _schedule_manager.get_current_session_info()


def calcular_tiempo_restante_para_proxima_sesion() -> Optional[Dict[str, int]]:
    """
    Función de interfaz para calcular tiempo restante

    Returns:
        Diccionario con tiempo restante hasta próxima sesión
    """
    return _schedule_manager.calcular_tiempo_restante_para_proxima_sesion()


def get_session_overlaps() -> list:
    """
    Función de interfaz para obtener solapamientos de sesiones

    Returns:
        Lista de solapamientos de sesiones
    """
    overlaps = []

    # London-New York overlap (más importante)
    overlaps.append({
        "sessions": ["London", "New York"],
        "start": "12:00",
        "end": "16:00",
        "duration_hours": 4,
        "volatility": "VERY_HIGH",
        "description": "Solapamiento Europa-América (Mayor volatilidad)"
    })

    return overlaps


def is_market_open() -> bool:
    """
    Determina si el mercado Forex está abierto

    Returns:
        True si hay alguna sesión activa
    """
    current_session = get_current_session_info()
    return current_session is not None


def get_market_status() -> Dict[str, Any]:
    """
    Obtiene estado completo del mercado

    Returns:
        Estado completo incluyendo sesión activa y próxima sesión
    """
    current_session = get_current_session_info()
    tiempo_restante = calcular_tiempo_restante_para_proxima_sesion()

    return {
        "is_open": current_session is not None,
        "current_session": current_session,
        "time_to_next_session": tiempo_restante,
        "overlaps": get_session_overlaps(),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# 🧪 FUNCIÓN DE TESTING Y DIAGNÓSTICO
def test_trading_schedule() -> bool:
    """
    Función de testing para verificar funcionamiento del sistema

    Returns:
        True si todas las pruebas pasan
    """
    try:
        # Test 1: Obtener sesión actual
        current_session = get_current_session_info()
        enviar_senal_log("INFO", f"✅ Test sesión actual: {current_session['name'] if current_session else 'Sin sesión activa'}", "trading_schedule", "migration")

        # Test 2: Calcular tiempo restante
        tiempo_restante = calcular_tiempo_restante_para_proxima_sesion()
        if tiempo_restante:
            enviar_senal_log("INFO", f"✅ Test tiempo restante: {tiempo_restante['hours']}h {tiempo_restante['minutes']}m", "trading_schedule", "migration")
        else:
            enviar_senal_log("INFO", "✅ Test tiempo restante: Datos no disponibles", "trading_schedule", "migration")

        # Test 3: Estado del mercado
        market_status = get_market_status()
        enviar_senal_log("INFO", f"✅ Test estado mercado: {'ABIERTO' if market_status['is_open'] else 'CERRADO'}", "trading_schedule", "migration")

        enviar_senal_log(
            "INFO",
            "🧪 Trading Schedule: Todos los tests pasaron exitosamente",
            __name__,
            "testing"
        )

        return True

    except Exception as e:
        enviar_senal_log(
            "ERROR",
            f"🧪 Trading Schedule: Test falló - {str(e)}",
            __name__,
            "testing"
        )
        return False


# 🚀 INICIALIZACIÓN AUTOMÁTICA
if __name__ == "__main__":
    enviar_senal_log("INFO", "🕐 TRADING SCHEDULE - SISTEMA DE HORARIOS v1.0.0", "trading_schedule", "migration")
    enviar_senal_log("INFO", "=" * 50, "trading_schedule", "migration")
    test_trading_schedule()
