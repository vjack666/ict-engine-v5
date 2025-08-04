#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DETECTOR ADAPTATIVO DE ESTADO DE MERCADO v2.0
==============================================

CARACTERÍSTICAS CLAVE:
- ✅ Detección automática de zona horaria (local, VPS, broker)
- ✅ Soporte para múltiples brokers y zonas horarias
- ✅ Detección adaptativa de DST (Daylight Saving Time)
- ✅ Soporte para VPS en cualquier zona horaria
- ✅ Integración con sistema de logging inteligente (SLUC v2.1)
- ✅ Logs organizados automáticamente en data/logs/
- ✅ Sin output en terminal (logging silencioso)

OBJETIVO:
Detectar automáticamente el estado actual del mercado Forex considerando:
1. Zona horaria local del sistema
2. Zona horaria del VPS (si aplica)
3. Zona horaria del broker MT5
4. Sesiones de trading activas
5. Días de la semana

INTEGRACIÓN:
- dashboard_definitivo.py: Display en tiempo real
- trading_schedule.py: Sesiones y horarios
- logging_interface.py: SLUC v2.1 para logs organizados

AUTOR: ICT Engine v5.0
FECHA: 2025-01-06
"""

import sys
import os
from datetime import datetime, timezone, timedelta
import platform

try:
    from sistema.trading_schedule import TradingScheduleManager
    from sistema.logging_interface import enviar_senal_log
    import pytz  # Para manejo avanzado de zonas horarias
except ImportError as e:
    # Fallback sin pytz
    pytz = None
    try:
        from sistema.trading_schedule import TradingScheduleManager
        from sistema.logging_interface import enviar_senal_log
    except ImportError as e2:
        enviar_senal_log("ERROR", f"Error crítico importando módulos: {e2}", __name__, "market_status")
        sys.exit(1)


class MarketStatusDetector:
    """
    Detector adaptativo de estado de mercado con soporte multi-zona horaria
    """

    def __init__(self):
        """Inicializar detector con configuración automática"""
        self.trading_schedule = TradingScheduleManager()

        # 📊 LOG DE CONFIGURACIÓN DETECTADA
        enviar_senal_log("INFO", "🚀 Inicializando Detector Adaptativo de Estado de Mercado", __name__, "market_status")

        # Detectar configuración del sistema
        self.timezone_info = self._detect_system_timezones()

        enviar_senal_log("INFO",
                        f"Configuración detectada - "
                        f"Local: {self.timezone_info['local_timezone_name']} | "
                        f"Broker: {self.timezone_info['broker_timezone_name']} | "
                        f"Plataforma: {self.timezone_info['platform']}",
                        __name__, "market_status")

    def _detect_system_timezones(self) -> dict:
        """
        Detecta automáticamente las zonas horarias del sistema
        """
        # Información base del sistema
        platform_info = platform.system()

        # Hora local del sistema
        local_time = datetime.now()
        local_utc_offset = local_time.astimezone().utcoffset().total_seconds() / 3600

        # Detección de zona horaria local
        local_tz_name = self._detect_local_timezone_name(local_utc_offset)

        # Detección de zona horaria del broker (por defecto UTC+2/UTC+3 Europa)
        broker_utc_offset = self._detect_mt5_broker_timezone()
        broker_tz_name = self._get_broker_timezone_name(broker_utc_offset)

        return {
            'platform': platform_info,
            'local_utc_offset': local_utc_offset,
            'local_timezone_name': local_tz_name,
            'broker_utc_offset': broker_utc_offset,
            'broker_timezone_name': broker_tz_name,
            'detection_method': 'automatic_system_detection',
            'pytz_available': pytz is not None
        }

    def _detect_local_timezone_name(self, utc_offset: float) -> str:
        """
        Detecta el nombre de la zona horaria local basado en el offset UTC
        """
        # Mapeo común de offsets UTC a zonas horarias
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

    def _detect_mt5_broker_timezone(self) -> float:
        """
        Detecta la zona horaria del broker MT5
        Común: UTC+2 (Europa), UTC+3 (Europa DST), UTC-5 (América)
        """
        try:
            # Intentar conectar con MT5 para obtener hora del servidor
            try:
                import MetaTrader5 as mt5
                if mt5.initialize():
                    # Obtener hora del servidor MT5
                    server_time = mt5.symbol_info_tick("EURUSD")
                    if server_time:
                        server_timestamp = server_time.time
                        server_dt = datetime.fromtimestamp(server_timestamp, tz=timezone.utc)
                        local_dt = datetime.now(timezone.utc)

                        # Calcular diferencia (aproximada)
                        diff_hours = (server_dt - local_dt).total_seconds() / 3600

                        enviar_senal_log("INFO", f"Broker MT5 detectado - Offset: UTC{diff_hours:+.1f}", __name__, "market_status")
                        mt5.shutdown()
                        return diff_hours
                    mt5.shutdown()
            except ImportError:
                enviar_senal_log("WARNING", "MT5 no disponible - usando zona horaria por defecto", __name__, "market_status")
        except Exception as e:
            enviar_senal_log("WARNING", f"Error detectando broker timezone: {e}", __name__, "market_status")

        # Fallback: Zona horaria europea por defecto (más común en Forex)
        # UTC+2 o UTC+3 dependiendo de la época del año
        now = datetime.now()
        if 3 <= now.month <= 10:  # Aproximación de DST europeo
            return 3.0  # UTC+3 (DST activo)
        else:
            return 2.0  # UTC+2 (DST inactivo)

    def _get_broker_timezone_name(self, utc_offset: float) -> str:
        """
        Obtiene el nombre de la zona horaria del broker
        """
        broker_map = {
            2.0: "Europe/Berlin (UTC+2, Standard)",
            3.0: "Europe/Berlin (UTC+3, DST)",
            0.0: "UTC/GMT (UTC+0)",
            -5.0: "America/New_York (UTC-5)"
        }

        return broker_map.get(utc_offset, f"Broker UTC{utc_offset:+.1f}")

    def get_timezone_info(self) -> dict:
        """
        Obtiene información completa de zonas horarias detectadas
        """
        return {
            'detection_summary': {
                'local_timezone': self.timezone_info['local_timezone_name'],
                'local_offset': f"UTC{self.timezone_info['local_utc_offset']:+.1f}",
                'broker_timezone': self.timezone_info['broker_timezone_name'],
                'broker_offset': f"UTC{self.timezone_info['broker_utc_offset']:+.1f}",
                'platform': self.timezone_info['platform'],
                'pytz_support': self.timezone_info['pytz_available']
            },
            'raw_data': self.timezone_info
        }

    def get_current_market_status(self) -> dict:
        """
        Obtiene el estado actual completo del mercado con información multi-zona horaria
        """
        try:
            # Calcular todas las zonas horarias relevantes
            now_local = datetime.now()
            now_utc = datetime.now(timezone.utc)

            # Tiempo del broker
            broker_offset_hours = self.timezone_info['broker_utc_offset']
            broker_offset = timedelta(hours=broker_offset_hours)
            now_broker = now_utc + broker_offset

            enviar_senal_log("INFO",
                            f"Calculando estado del mercado - "
                            f"Local: {now_local.strftime('%H:%M')} | "
                            f"UTC: {now_utc.strftime('%H:%M')} | "
                            f"Broker: {now_broker.strftime('%H:%M')}",
                            __name__, "market_status")

            # Usar el horario del broker para determinar sesiones (más preciso)
            session_info = self.trading_schedule.get_active_sessions(now_broker)

            # 📊 DETECTAR SESIONES ACTIVAS
            session_activa = {
                'name': 'Mercado Cerrado',
                'description': 'No hay sesiones activas',
                'all_active': []
            }

            if session_info['sessions_activas']:
                active_names = [s['nombre'] for s in session_info['sessions_activas']]
                session_activa = {
                    'name': active_names[0] if active_names else 'Mercado Cerrado',
                    'description': f"Sesiones activas: {', '.join(active_names)}" if active_names else 'Sin sesiones activas',
                    'all_active': active_names
                }

            # ⏰ PRÓXIMA SESIÓN
            proxima_sesion = {
                'time_string': session_info.get('proxima_sesion', 'Calculando...'),
                'raw_info': session_info
            }

            # 📊 CREAR STATUS COMPLETO Y ADAPTATIVO
            market_status = self._determine_market_status(now_broker, session_activa)

            status_completo = {
                'timestamp': now_local.isoformat(),
                'fecha': now_local.strftime('%Y-%m-%d'),
                'dia_semana': now_local.strftime('%A'),
                # ⏰ MÚLTIPLES ZONAS HORARIAS
                'tiempo_local': {
                    'hora': now_local.strftime('%H:%M:%S'),
                    'timezone': self.timezone_info['local_timezone_name'],
                    'offset': f"UTC{self.timezone_info['local_utc_offset']:+.1f}"
                },
                'tiempo_utc': {
                    'hora': now_utc.strftime('%H:%M:%S'),
                    'timezone': 'UTC/GMT',
                    'offset': 'UTC+0.0'
                },
                'tiempo_broker': {
                    'hora': now_broker.strftime('%H:%M:%S'),
                    'timezone': self.timezone_info['broker_timezone_name'],
                    'offset': f"UTC{self.timezone_info['broker_utc_offset']:+.1f}"
                },
                # 📊 ESTADO DEL MERCADO
                'market_status': market_status['status'],
                'emoji_status': market_status['emoji'],
                'session_activa': session_activa,
                'proxima_sesion': proxima_sesion,
                'timezone_detection': self.timezone_info
            }

            enviar_senal_log("SUCCESS",
                            f"Estado del mercado calculado - "
                            f"Status: {market_status['emoji']} {market_status['status']} | "
                            f"Sesión: {session_activa['name']}",
                            __name__, "market_status")

            return status_completo

        except Exception as e:
            enviar_senal_log("ERROR", f"Error calculando estado del mercado: {e}", __name__, "market_status")
            return {
                'error': str(e),
                'market_status': 'ERROR',
                'emoji_status': '❌',
                'timestamp': datetime.now().isoformat()
            }

    def _determine_market_status(self, broker_time: datetime, session_info: dict) -> dict:
        """
        Determina el estado del mercado basado en el tiempo del broker y sesiones activas
        """
        # Verificar día de la semana (en tiempo del broker)
        dia_semana = broker_time.weekday()  # 0=Lunes, 6=Domingo

        # Fin de semana
        if dia_semana == 5:  # Sábado
            if broker_time.hour < 22:  # Antes de las 22:00 del sábado
                return {'status': 'FIN DE SEMANA', 'emoji': '🌴'}
            else:
                return {'status': 'PREPARANDOSE PARA APERTURA', 'emoji': '🔄'}

        if dia_semana == 6:  # Domingo
            if broker_time.hour < 22:  # Antes de las 22:00 del domingo
                return {'status': 'FIN DE SEMANA', 'emoji': '🌴'}
            else:
                return {'status': 'MERCADO ABRIENDO', 'emoji': '🟢'}

        # Días laborables
        if session_info['all_active']:
            return {'status': 'MERCADO ABIERTO', 'emoji': '🟢'}
        else:
            return {'status': 'ENTRE SESIONES', 'emoji': '🟡'}


def main():
    """Función principal para testing adaptativo"""
    detector = MarketStatusDetector()

    enviar_senal_log("INFO", "🕐 DETECTOR ADAPTATIVO DE ESTADO DE MERCADO", __name__, "market_status")
    enviar_senal_log("INFO", "=" * 60, __name__, "market_status")

    # Estado general
    status = detector.get_current_market_status()

    enviar_senal_log("INFO", f"📅 Fecha: {status['fecha']}", __name__, "market_status")
    enviar_senal_log("INFO", f"📆 Día: {status['dia_semana']}", __name__, "market_status")

    # Múltiples zonas horarias
    enviar_senal_log("INFO", "🌍 ZONAS HORARIAS DETECTADAS:", __name__, "market_status")
    enviar_senal_log("INFO", f"  🏠 Local: {status['tiempo_local']['hora']} ({status['tiempo_local']['timezone']}) {status['tiempo_local']['offset']}", __name__, "market_status")
    enviar_senal_log("INFO", f"  🌐 UTC: {status['tiempo_utc']['hora']} ({status['tiempo_utc']['timezone']}) {status['tiempo_utc']['offset']}", __name__, "market_status")
    enviar_senal_log("INFO", f"  🏦 Broker: {status['tiempo_broker']['hora']} ({status['tiempo_broker']['timezone']}) {status['tiempo_broker']['offset']}", __name__, "market_status")

    # Estado del mercado
    enviar_senal_log("INFO", "📊 ESTADO DEL MERCADO:", __name__, "market_status")
    enviar_senal_log("INFO", f"  Status: {status['emoji_status']} {status['market_status']}", __name__, "market_status")
    enviar_senal_log("INFO", f"  Sesión: {status['session_activa']['name']}", __name__, "market_status")
    if status['session_activa'].get('all_active'):
        enviar_senal_log("INFO", f"  Sesiones activas: {', '.join(status['session_activa']['all_active'])}", __name__, "market_status")
    enviar_senal_log("INFO", f"  Descripción: {status['session_activa']['description']}", __name__, "market_status")

    # Próxima sesión
    enviar_senal_log("INFO", "⏳ PRÓXIMA SESIÓN:", __name__, "market_status")
    enviar_senal_log("INFO", f"  En: {status['proxima_sesion']['time_string']}", __name__, "market_status")

    # Información técnica
    enviar_senal_log("INFO", "🔧 DETECCIÓN TÉCNICA:", __name__, "market_status")
    if 'timezone_detection' in status:
        tz_info = status['timezone_detection']
        if 'local_timezone_name' in tz_info:
            enviar_senal_log("INFO", f"  Método detección: {tz_info.get('detection_method', 'N/A')}", __name__, "market_status")
            enviar_senal_log("INFO", f"  Plataforma: {tz_info.get('platform', 'N/A')}", __name__, "market_status")
            enviar_senal_log("INFO", f"  Pytz disponible: {tz_info.get('pytz_available', False)}", __name__, "market_status")

    # Test de zona horaria específica
    enviar_senal_log("INFO", "🧪 TEST ESPECÍFICO PARA ECUADOR:", __name__, "market_status")
    tz_info = detector.get_timezone_info()
    if 'Ecuador' in tz_info['detection_summary']['local_timezone'] or abs(float(tz_info['detection_summary']['local_offset'].replace('UTC', '')) + 5.0) < 0.5:
        enviar_senal_log("SUCCESS", "  ✅ Ecuador detectado correctamente (UTC-5)", __name__, "market_status")
    else:
        enviar_senal_log("INFO", f"  📍 Zona detectada: {tz_info['detection_summary']['local_timezone']} ({tz_info['detection_summary']['local_offset']})", __name__, "market_status")


if __name__ == "__main__":
    main()
