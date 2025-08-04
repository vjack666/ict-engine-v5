#!/usr/bin/env python3
"""
🕐 DETECTOR AUTOMÁTICO DE ESTADO DE MERCADO - VERSIÓN ADAPTATIVA
===============================================================

Sistema inteligente que detecta automáticamente el estado del mercado Forex
con soporte para múltiples zonas horarias, servidores VPS, y broker MT5.

Características:
- ✅ Detección automática de zona horaria local del sistema
- ✅ Sincronización con hora del broker MT5
- ✅ Soporte para VPS en cua    enviar_senal_log("INFO", "🕐 DETECTOR ADAPTATIVO DE ESTADO DE MERCADO", __name__, "market_status")
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
- ✅ Conversión inteligente entre zonas horarias
- ✅ Detección adaptativa de sesiones de trading
- ✅ Fallback robusto para cualquier configuración
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, Tuple
import sys
import platform
import time
from pathlib import Path

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

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
    """Detector automático e inteligente del estado del mercado"""
    
    def __init__(self):
        """Inicializa el detector con detección automática de zona horaria"""
        self.trading_schedule = TradingScheduleManager()
        
        # 🌍 DETECCIÓN AUTOMÁTICA DE ZONA HORARIA
        self.timezone_info = self._detect_system_timezone()
        self.mt5_broker_offset = self._detect_mt5_broker_timezone()
        
        # 📊 LOG DE CONFIGURACIÓN DETECTADA
        enviar_senal_log("INFO", 
            f"🕐 MarketStatusDetector inicializado - Local: {self.timezone_info['name']} " +
            f"({self.timezone_info['offset_hours']:+.1f}h), MT5: {self.mt5_broker_offset:+.1f}h", 
            __name__, "market_status")
    
    def _detect_system_timezone(self) -> Dict[str, Any]:
        """
        Detecta automáticamente la zona horaria del sistema
        Funciona en Windows, Linux, VPS, etc.
        """
        try:
            # Método 1: Usar time.timezone (más confiable)
            local_offset_seconds = -time.timezone
            if time.daylight and time.localtime().tm_isdst:
                local_offset_seconds = -time.altzone
            
            offset_hours = local_offset_seconds / 3600
            
            # Método 2: Detectar zona horaria específica si pytz está disponible
            timezone_name = "Local"
            if pytz:
                try:
                    local_tz = pytz.timezone('UTC')
                    # Intentar detectar zona horaria común por offset
                    common_timezones = {
                        -5: "America/New_York",  # Ecuador está en UTC-5
                        -4: "America/Santiago", 
                        -3: "America/Sao_Paulo",
                        0: "UTC",
                        1: "Europe/London",
                        2: "Europe/Berlin",
                        3: "Europe/Moscow",
                        8: "Asia/Singapore",
                        9: "Asia/Tokyo"
                    }
                    if int(offset_hours) in common_timezones:
                        timezone_name = common_timezones[int(offset_hours)]
                except:
                    pass
            
            # Detección específica para Ecuador (UTC-5)
            if abs(offset_hours + 5.0) < 0.5:  # Ecuador UTC-5
                timezone_name = "America/Guayaquil (Ecuador)"
            
            return {
                'name': timezone_name,
                'offset_hours': offset_hours,
                'offset_seconds': local_offset_seconds,
                'is_dst': bool(time.daylight and time.localtime().tm_isdst),
                'platform': platform.system(),
                'detection_method': 'time.timezone'
            }
            
        except Exception as e:
            enviar_senal_log("WARNING", f"⚠️ Error detectando zona horaria: {e}", __name__, "timezone")
            # Fallback conservador
            return {
                'name': 'UTC (fallback)',
                'offset_hours': 0.0,
                'offset_seconds': 0,
                'is_dst': False,
                'platform': platform.system(),
                'detection_method': 'fallback'
            }
    
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
                        
                        # Redondear a zona horaria común del broker
                        if abs(diff_hours - 2) < 1:
                            return 2.0  # UTC+2 (Europa)
                        elif abs(diff_hours - 3) < 1:
                            return 3.0  # UTC+3 (Europa DST)
                        elif abs(diff_hours + 5) < 1:
                            return -5.0  # UTC-5 (América)
                        
                    mt5.shutdown()
            except ImportError:
                pass
            
            # Fallback: Detectar por zona horaria local común de brokers
            local_offset = self.timezone_info['offset_hours']
            
            # Brokers europeos (más comunes)
            if -2 <= local_offset <= 4:
                return 2.0  # UTC+2 (Europa)
            # Brokers americanos
            elif -8 <= local_offset <= -3:
                return -5.0  # UTC-5 (América)
            # Brokers asiáticos
            elif 6 <= local_offset <= 10:
                return 8.0  # UTC+8 (Asia)
            else:
                return 2.0  # Default: Europa UTC+2
                
        except Exception as e:
            enviar_senal_log("WARNING", f"⚠️ Error detectando MT5 timezone: {e}", __name__, "mt5_timezone")
            return 2.0  # Default seguro: Europa UTC+2
    
    def _get_time_in_multiple_zones(self) -> Dict[str, Dict[str, Any]]:
        """
        Obtiene la hora actual en múltiples zonas horarias relevantes
        """
        now_utc = datetime.now(timezone.utc)
        
        return {
            'local': {
                'datetime': now_utc + timedelta(hours=self.timezone_info['offset_hours']),
                'timezone_name': self.timezone_info['name'],
                'offset': self.timezone_info['offset_hours'],
                'is_dst': self.timezone_info['is_dst']
            },
            'utc': {
                'datetime': now_utc,
                'timezone_name': 'UTC',
                'offset': 0.0,
                'is_dst': False
            },
            'mt5_broker': {
                'datetime': now_utc + timedelta(hours=self.mt5_broker_offset),
                'timezone_name': f'MT5 Broker (UTC{self.mt5_broker_offset:+.0f})',
                'offset': self.mt5_broker_offset,
                'is_dst': False
            },
            'london': {
                'datetime': now_utc + timedelta(hours=1),  # UTC+1 (Londres invierno)
                'timezone_name': 'London',
                'offset': 1.0,
                'is_dst': False
            },
            'new_york': {
                'datetime': now_utc + timedelta(hours=-4),  # UTC-4 (NY verano)
                'timezone_name': 'New York',
                'offset': -4.0,
                'is_dst': True
            },
            'tokyo': {
                'datetime': now_utc + timedelta(hours=9),  # UTC+9
                'timezone_name': 'Tokyo',
                'offset': 9.0,
                'is_dst': False
            }
        }
    
    def _detect_active_trading_sessions(self, time_zones: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Detecta qué sesiones de trading están activas basado en múltiples zonas horarias
        """
        # Obtener hora UTC para cálculos estándar
        utc_hour = time_zones['utc']['datetime'].hour
        
        # Definir sesiones en UTC (horario estándar)
        sessions = {
            'SYDNEY': {'start': 21, 'end': 6, 'active': False, 'description': 'Sydney/Asia-Pacific'},
            'TOKYO': {'start': 23, 'end': 8, 'active': False, 'description': 'Tokyo/Asia'},
            'LONDON': {'start': 7, 'end': 16, 'active': False, 'description': 'London/Europe'},
            'NEW_YORK': {'start': 12, 'end': 21, 'active': False, 'description': 'New York/America'}
        }
        
        # Verificar qué sesiones están activas
        active_sessions = []
        
        for session_name, session_info in sessions.items():
            start_hour = session_info['start']
            end_hour = session_info['end']
            
            # Manejar sesiones que cruzan medianoche
            if start_hour > end_hour:  # Ej: 21:00 - 06:00
                if utc_hour >= start_hour or utc_hour < end_hour:
                    session_info['active'] = True
                    active_sessions.append(session_name)
            else:  # Sesiones normales
                if start_hour <= utc_hour < end_hour:
                    session_info['active'] = True
                    active_sessions.append(session_name)
        
        # Determinar sesión principal
        primary_session = None
        if active_sessions:
            # Prioridad: London > New York > Tokyo > Sydney
            priority = ['LONDON', 'NEW_YORK', 'TOKYO', 'SYDNEY']
            for session in priority:
                if session in active_sessions:
                    primary_session = session
                    break
        
        return {
            'sessions': sessions,
            'active_sessions': active_sessions,
            'primary_session': primary_session,
            'total_active': len(active_sessions),
            'market_open': len(active_sessions) > 0
        }
    
    def get_current_market_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado actual del mercado de forma inteligente y adaptativa
        
        Returns:
            Dict con información completa del estado del mercado
        """
        try:
            # 🌍 OBTENER TIEMPO EN MÚLTIPLES ZONAS HORARIAS
            time_zones = self._get_time_in_multiple_zones()
            
            # 📊 DETECTAR SESIONES ACTIVAS
            trading_sessions = self._detect_active_trading_sessions(time_zones)
            
            # 📅 INFORMACIÓN BÁSICA
            local_time = time_zones['local']['datetime']
            utc_time = time_zones['utc']['datetime']
            broker_time = time_zones['mt5_broker']['datetime']
            
            fecha_actual = local_time.strftime("%Y-%m-%d")
            hora_local = local_time.strftime("%H:%M:%S")
            hora_utc = utc_time.strftime("%H:%M:%S")
            hora_broker = broker_time.strftime("%H:%M:%S")
            dia_semana = local_time.strftime("%A")
            
            # 🔍 DETERMINAR ESTADO DEL MERCADO
            is_weekend = utc_time.weekday() >= 5  # Sábado=5, Domingo=6
            
            if is_weekend:
                market_status = "CERRADO"
                session_name = "FIN DE SEMANA"
                session_description = "Mercado cerrado - Fin de semana"
            elif trading_sessions['market_open']:
                market_status = "ABIERTO"
                session_name = trading_sessions['primary_session']
                session_description = f"Sesión {session_name} activa"
            else:
                market_status = "CERRADO"
                session_name = "ENTRE SESIONES"
                session_description = "Mercado cerrado entre sesiones"
            
            # ⏰ PRÓXIMA SESIÓN
            next_session_time = self.trading_schedule.calcular_tiempo_restante_para_proxima_sesion()
            if next_session_time:
                next_session_hours = next_session_time.get('hours', 0)
                next_session_minutes = next_session_time.get('minutes', 0)
            else:
                next_session_hours = 0
                next_session_minutes = 0
            
            # 📊 CREAR STATUS COMPLETO Y ADAPTATIVO
            status = {
                'timestamp': utc_time.isoformat(),
                'fecha': fecha_actual,
                'dia_semana': dia_semana,
                'is_weekend': is_weekend,
                
                # ⏰ MÚLTIPLES ZONAS HORARIAS
                'tiempo_local': {
                    'hora': hora_local,
                    'timezone': self.timezone_info['name'],
                    'offset': f"UTC{self.timezone_info['offset_hours']:+.1f}"
                },
                'tiempo_utc': {
                    'hora': hora_utc,
                    'timezone': 'UTC',
                    'offset': 'UTC+0.0'
                },
                'tiempo_broker': {
                    'hora': hora_broker,
                    'timezone': f'MT5 Broker',
                    'offset': f'UTC{self.mt5_broker_offset:+.1f}'
                },
                
                # 📊 ESTADO DEL MERCADO
                'market_status': market_status,
                'session_activa': {
                    'name': session_name,
                    'description': session_description,
                    'active': trading_sessions['market_open'],
                    'total_sessions': trading_sessions['total_active'],
                    'all_active': trading_sessions['active_sessions']
                },
                
                # ⏳ PRÓXIMA SESIÓN
                'proxima_sesion': {
                    'name': "Próxima sesión",
                    'hours_remaining': next_session_hours,
                    'minutes_remaining': next_session_minutes,
                    'time_string': f"{next_session_hours}h {next_session_minutes}m"
                },
                
                # 🎯 INFORMACIÓN PARA DISPLAY
                'status_display': self._generate_adaptive_status_display(
                    market_status, session_name, is_weekend, trading_sessions
                ),
                'emoji_status': self._get_adaptive_status_emoji(market_status, is_weekend, trading_sessions),
                
                # 🔧 INFORMACIÓN TÉCNICA
                'timezone_detection': {
                    'local_timezone': self.timezone_info,
                    'broker_offset': self.mt5_broker_offset,
                    'platform': platform.system()
                }
            }
            
            # 📋 LOG ADAPTATIVO
            enviar_senal_log("INFO", 
                f"🕐 Estado detectado: {market_status} | {session_name} | " +
                f"Local: {hora_local} ({self.timezone_info['name']}) | " +
                f"UTC: {hora_utc} | Broker: {hora_broker}", 
                __name__, "market_status")
            
            return status
            
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error detectando estado del mercado: {e}", __name__, "market_status")
            
            # Fallback ultra-robusto
            now = datetime.now()
            return {
                'timestamp': now.isoformat(),
                'fecha': now.strftime("%Y-%m-%d"),
                'dia_semana': now.strftime("%A"),
                'is_weekend': now.weekday() >= 5,
                'tiempo_local': {'hora': now.strftime("%H:%M:%S"), 'timezone': 'Local', 'offset': 'Unknown'},
                'tiempo_utc': {'hora': 'Unknown', 'timezone': 'UTC', 'offset': 'UTC+0.0'},
                'tiempo_broker': {'hora': 'Unknown', 'timezone': 'MT5', 'offset': 'Unknown'},
                'market_status': "ERROR",
                'session_activa': {'name': 'ERROR', 'description': 'Error detectando sesión', 'active': False},
                'proxima_sesion': {'name': 'ERROR', 'hours_remaining': 0, 'minutes_remaining': 0, 'time_string': 'N/A'},
                'status_display': "ERROR EN DETECCIÓN",
                'emoji_status': "❌",
                'timezone_detection': {'error': str(e)}
            }
    
    def _generate_adaptive_status_display(self, market_status: str, session_name: str, 
                                        is_weekend: bool, trading_sessions: Dict) -> str:
        """Genera texto adaptativo para mostrar el estado"""
        if is_weekend:
            return "MERCADO CERRADO - FIN DE SEMANA"
        elif market_status == "ABIERTO":
            if trading_sessions['total_active'] > 1:
                return f"MERCADO ABIERTO - MÚLTIPLES SESIONES ({trading_sessions['total_active']})"
            else:
                return f"MERCADO ABIERTO - SESIÓN {session_name}"
        else:
            return "MERCADO CERRADO - ENTRE SESIONES"
    
    def _get_adaptive_status_emoji(self, market_status: str, is_weekend: bool, 
                                 trading_sessions: Dict) -> str:
        """Obtiene emoji adaptativo para el estado"""
        if is_weekend:
            return "🔴"
        elif market_status == "ABIERTO":
            if trading_sessions['total_active'] > 1:
                return "🟢🟡"  # Múltiples sesiones
            else:
                return "🟢"
        else:
            return "🟡"

    def is_market_open(self) -> bool:
        """Verifica si el mercado está abierto"""
        status = self.get_current_market_status()
        return status['market_status'] == "ABIERTO"
    
    def get_simple_status(self) -> str:
        """Obtiene status simple para logging rápido"""
        status = self.get_current_market_status()
        return f"{status['emoji_status']} {status['status_display']}"
    
    def get_timezone_info(self) -> Dict[str, Any]:
        """Obtiene información detallada de zonas horarias detectadas"""
        time_zones = self._get_time_in_multiple_zones()
        return {
            'detection_summary': {
                'local_timezone': self.timezone_info['name'],
                'local_offset': f"UTC{self.timezone_info['offset_hours']:+.1f}",
                'broker_offset': f"UTC{self.mt5_broker_offset:+.1f}",
                'platform': self.timezone_info['platform']
            },
            'current_times': {
                zone: {
                    'time': info['datetime'].strftime("%H:%M:%S"),
                    'date': info['datetime'].strftime("%Y-%m-%d"),
                    'timezone': info['timezone_name'],
                    'offset': f"UTC{info['offset']:+.1f}"
                }
                for zone, info in time_zones.items()
            }
        }


def main():
    """Función principal para testing adaptativo"""
    detector = MarketStatusDetector()
    
    print("🕐 DETECTOR ADAPTATIVO DE ESTADO DE MERCADO")
    print("=" * 60)
    
    # Estado general
    status = detector.get_current_market_status()
    
    print(f"� Fecha: {status['fecha']}")
    print(f"📆 Día: {status['dia_semana']}")
    print()
    
    # Múltiples zonas horarias
    print("🌍 ZONAS HORARIAS DETECTADAS:")
    print(f"  🏠 Local: {status['tiempo_local']['hora']} ({status['tiempo_local']['timezone']}) {status['tiempo_local']['offset']}")
    print(f"  🌐 UTC: {status['tiempo_utc']['hora']} ({status['tiempo_utc']['timezone']}) {status['tiempo_utc']['offset']}")
    print(f"  � Broker: {status['tiempo_broker']['hora']} ({status['tiempo_broker']['timezone']}) {status['tiempo_broker']['offset']}")
    print()
    
    # Estado del mercado
    print("📊 ESTADO DEL MERCADO:")
    print(f"  Status: {status['emoji_status']} {status['market_status']}")
    print(f"  Sesión: {status['session_activa']['name']}")
    if status['session_activa'].get('all_active'):
        print(f"  Sesiones activas: {', '.join(status['session_activa']['all_active'])}")
    print(f"  Descripción: {status['session_activa']['description']}")
    print()
    
    # Próxima sesión
    print("⏳ PRÓXIMA SESIÓN:")
    print(f"  En: {status['proxima_sesion']['time_string']}")
    print()
    
    # Información técnica
    print("� DETECCIÓN TÉCNICA:")
    if 'timezone_detection' in status:
        tz_info = status['timezone_detection']
        if 'local_timezone' in tz_info:
            print(f"  Método detección: {tz_info['local_timezone'].get('detection_method', 'N/A')}")
            print(f"  Plataforma: {tz_info.get('platform', 'N/A')}")
            print(f"  DST activo: {tz_info['local_timezone'].get('is_dst', False)}")
    
    # Test de zona horaria específica
    print("\n🧪 TEST ESPECÍFICO PARA ECUADOR:")
    tz_info = detector.get_timezone_info()
    if 'Ecuador' in tz_info['detection_summary']['local_timezone'] or abs(float(tz_info['detection_summary']['local_offset'].replace('UTC', '')) + 5.0) < 0.5:
        print("  ✅ Ecuador detectado correctamente (UTC-5)")
    else:
        print(f"  📍 Zona detectada: {tz_info['detection_summary']['local_timezone']} ({tz_info['detection_summary']['local_offset']})")


if __name__ == "__main__":
    main()
