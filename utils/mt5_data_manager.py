# Utilidad para forzar la descarga y guardado de M1
def descargar_y_guardar_m1(symbol: str = "EURUSD", lookback: int = 200000) -> bool:
    """
    Descarga y guarda las velas de M1 siguiendo la lógica del sistema.
    """
    from utils.mt5_data_manager import get_mt5_manager

    manager = get_mt5_manager()
    enviar_senal_log("INFO", f"[MT5] Forzando descarga de velas M1 para {symbol}...", "mt5_data_manager")
    df = manager.get_historical_data(symbol, "M1", lookback, force_download=True)
    if df is not None and not df.empty:
        enviar_senal_log("INFO", f"[MT5] Velas M1 descargadas y guardadas: {len(df)} filas.", "mt5_data_manager")
        return True
    else:
        enviar_senal_log("ERROR", f"[MT5] ERROR: No se pudieron descargar velas M1 para {symbol}.", "mt5_data_manager")
        return False
"""
MT5 Data Manager - Sistema Sentinel Grid v3.3.3.3.3
============================================

Módulo centralizado para manejar todas las operaciones de MetaTrader5
de forma consistente y con manejo de errores robusto.

Autor: Sistema Sentinel Grid v3.3.3.3.3
Fecha: 2025
"""

# CORREGIDO: Imports estándar en lugar de sistema.sic
from typing import Optional, Any, Dict, List
import pandas as pd
# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log
from config.live_account_validator import get_account_validator, AccountType
from pathlib import Path
import os

# Importación segura de MT5 y configuración FundedNext
try:
    import MetaTrader5 as mt5
    mt5_available = True
except ImportError:
    mt5_available = False
    mt5 = None

# Configuración específica para FundedNext MT5
FUNDEDNEXT_MT5_PATH = r"C:\Program Files\FundedNext MT5 Terminal\terminal64.exe"
FUNDEDNEXT_CONFIG = {
    "executable_path": FUNDEDNEXT_MT5_PATH,
    "max_bars": 50000,
    "symbols": ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD"],
    "timeframes": ["M1", "M3", "M5", "M15", "H1", "H4", "D1"],
    "magic_number": 20250724
}

def validate_fundednext_installation() -> bool:
    """
    Valida que el terminal FundedNext esté instalado y sea accesible.
    SOLO permite el uso del terminal FundedNext.
    """
    if not os.path.exists(FUNDEDNEXT_MT5_PATH):
        return False
    if not os.path.isfile(FUNDEDNEXT_MT5_PATH):
        return False

    # Verificación adicional del nombre del archivo
    if "fundednext" not in FUNDEDNEXT_MT5_PATH.lower():
        return False

    return True

def ensure_only_fundednext_connection():
    """
    Garantiza que solo se use el terminal FundedNext MT5.
    Desconecta cualquier otra conexión MT5 activa.
    """
    if not mt5_available or mt5 is None:
        return False

    try:
        # Verificar si hay alguna conexión activa
        if hasattr(mt5, 'terminal_info'):
            terminal_info = mt5.terminal_info()  # type: ignore
            if terminal_info:
                terminal_path = str(terminal_info.path).lower()
                if "fundednext" not in terminal_path:
                    # Hay una conexión a un terminal que NO es FundedNext
                    enviar_senal_log("WARNING", f"🚨 TERMINAL INCORRECTO DETECTADO: {terminal_info.path}", "mt5_data_manager", "security")
                    enviar_senal_log("WARNING", "🔒 Desconectando terminal no autorizado...", "mt5_data_manager", "security")
                    mt5.shutdown()  # type: ignore
                    return False
                else:
                    enviar_senal_log("INFO", "✅ Terminal FundedNext verificado como activo", "mt5_data_manager", "security")
                    return True
    except Exception as e:
        enviar_senal_log("ERROR", f"Error verificando terminal activo: {e}", "mt5_data_manager", "security")

    return False

# Configuración de timeframes
TIMEFRAME_MAPPING = {
    'M1': 1,     # Añadimos M1
    'M3': 3,
    'M5': 5,
    'M15': 15,
    'H1': 16385,
    'H4': 16388,
    'D1': 16408
}

class MT5DataManager:
    """
    Gestor centralizado para operaciones con MetaTrader5.
    Maneja la descarga, validación y almacenamiento de datos históricos.
    """

    def __init__(self):
        self.is_connected = False
        self.available_functions = {}
        self.account_validator = get_account_validator()
        self.account_type = None
        self.account_config = None

        # 🔒 VERIFICACIÓN DE SEGURIDAD INICIAL
        ensure_only_fundednext_connection()

        self._check_mt5_availability()

    def _check_mt5_availability(self) -> None:
        """Verifica qué funciones de MT5 están disponibles."""
        if not mt5_available or mt5 is None:
            return

        # Lista de funciones críticas de MT5
        critical_functions = [
            'initialize',
            'shutdown',
            'copy_rates_from_pos',
            'copy_rates_from',
            'symbol_info_tick',
            'symbols_get'
        ]

        for func_name in critical_functions:
            self.available_functions[func_name] = hasattr(mt5, func_name)

    def connect(self) -> bool:
        """
        Conecta EXCLUSIVAMENTE al terminal FundedNext MT5.
        NUNCA permite conexión a otros terminales MT5.
        """
        if not mt5_available or mt5 is None:
            enviar_senal_log("ERROR", "❌ MetaTrader5 no está disponible", "mt5_data_manager", "connection")
            return False

        if not validate_fundednext_installation():
            enviar_senal_log("ERROR", f"❌ Terminal FundedNext MT5 no encontrado en: {FUNDEDNEXT_MT5_PATH}", "mt5_data_manager", "connection")
            enviar_senal_log("ERROR", "🚨 SEGURIDAD: Solo se permite conexión a FundedNext MT5", "mt5_data_manager", "connection")
            return False

        try:
            # 🔒 VERIFICACIÓN DE SEGURIDAD: Desconectar cualquier terminal previo
            try:
                if hasattr(mt5, 'shutdown'):
                    mt5.shutdown()  # type: ignore
                    enviar_senal_log("INFO", "🔒 Desconectado cualquier terminal MT5 previo", "mt5_data_manager", "security")
            except Exception:
                pass

            if self.available_functions.get('initialize', False):
                enviar_senal_log("INFO", f"🔗 Conectando EXCLUSIVAMENTE a FundedNext MT5", "mt5_data_manager", "connection")
                enviar_senal_log("INFO", f"📁 Ruta obligatoria: {FUNDEDNEXT_MT5_PATH}", "mt5_data_manager", "connection")

                # 🛡️ CONEXIÓN EXCLUSIVA con ruta específica de FundedNext
                self.is_connected = mt5.initialize(path=FUNDEDNEXT_MT5_PATH)  # type: ignore

                if self.is_connected:
                    # 🔍 VALIDACIÓN CRÍTICA: Verificar que estamos conectados al terminal correcto
                    if not self._verify_fundednext_connection():
                        enviar_senal_log("ERROR", "🚨 ALERTA: No se conectó al terminal FundedNext correcto", "mt5_data_manager", "security")
                        self.disconnect()
                        return False

                    # Validar tipo de cuenta después de conectar
                    self._validate_account_type()

                    enviar_senal_log("INFO", "✅ CONEXIÓN SEGURA ESTABLECIDA - Solo FundedNext MT5", "mt5_data_manager", "connection")
                else:
                    enviar_senal_log("ERROR", "❌ Error al conectar con FundedNext MT5", "mt5_data_manager", "connection")

                return self.is_connected
        except (FileNotFoundError, PermissionError, IOError) as e:
            enviar_senal_log("ERROR", f"❌ Error de conexión MT5: {e}", "mt5_data_manager", "connection")

        return False

    def _verify_fundednext_connection(self) -> bool:
        """
        Verifica que estamos conectados específicamente al terminal FundedNext.

        Returns:
            True si la conexión es al terminal FundedNext correcto
        """
        try:
            terminal_info = mt5.terminal_info()  # type: ignore
            if terminal_info:
                terminal_path = str(terminal_info.path).lower()
                expected_path = FUNDEDNEXT_MT5_PATH.lower()

                # Verificar que la ruta coincida con FundedNext
                if "fundednext" in terminal_path or terminal_path == expected_path:
                    enviar_senal_log("INFO", f"✅ Verificado: Conectado a FundedNext MT5", "mt5_data_manager", "security")
                    enviar_senal_log("INFO", f"   Terminal: {terminal_info.name}", "mt5_data_manager", "security")
                    enviar_senal_log("INFO", f"   Empresa: {terminal_info.company}", "mt5_data_manager", "security")
                    enviar_senal_log("INFO", f"   Ruta: {terminal_info.path}", "mt5_data_manager", "security")
                    return True
                else:
                    enviar_senal_log("ERROR", f"🚨 TERMINAL INCORRECTO: {terminal_info.path}", "mt5_data_manager", "security")
                    enviar_senal_log("ERROR", f"🚨 SE ESPERABA: {FUNDEDNEXT_MT5_PATH}", "mt5_data_manager", "security")
                    return False
            else:
                enviar_senal_log("ERROR", "❌ No se pudo obtener información del terminal", "mt5_data_manager", "security")
                return False
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error verificando terminal: {e}", "mt5_data_manager", "security")
            return False

    def _validate_account_type(self) -> None:
        """Valida el tipo de cuenta después de conectar"""
        try:
            account_type, account_data = self.account_validator.detect_account_type()
            self.account_type = account_type
            self.account_config = self.account_validator.get_live_trading_config()

            # Log del tipo de cuenta detectado con claridad sobre datos reales
            if account_type == AccountType.DEMO:
                enviar_senal_log("INFO", f"🔶 CUENTA DEMO detectada - Usando datos REALES de mercado para trading simulado", "mt5_data_manager", "migration")
            elif account_type == AccountType.REAL:
                enviar_senal_log("INFO", f"💰 CUENTA REAL detectada - Usando datos REALES de mercado para trading en vivo", "mt5_data_manager", "migration")
            elif account_type == AccountType.CONTEST:
                enviar_senal_log("INFO", f"🏆 CUENTA DE FONDEO detectada - Usando datos REALES de mercado con reglas de evaluación", "mt5_data_manager", "migration")
            else:
                enviar_senal_log("ERROR", f"❓ TIPO DE CUENTA DESCONOCIDO", "mt5_data_manager", "migration")

            # Mensaje clarificatorio sobre datos de mercado
            enviar_senal_log("INFO", f"📊 CONFIRMACIÓN: TODOS los datos de mercado son REALES desde MT5", "mt5_data_manager", "migration")
            enviar_senal_log("INFO", f"🔍 El sistema NUNCA simula precios - Solo obtiene datos directos del broker", "mt5_data_manager", "migration")

            # Log información adicional
            enviar_senal_log("INFO", f"   Número de cuenta: {account_data.get('login', 'N/A')}", "mt5_data_manager", "migration")
            enviar_senal_log("INFO", f"   Servidor: {account_data.get('server', 'N/A')}", "mt5_data_manager", "migration")
            enviar_senal_log("INFO", f"   Broker: {account_data.get('company', 'N/A')}", "mt5_data_manager", "migration")
            enviar_senal_log("INFO", f"   Balance: {account_data.get('balance', 0):.2f} {account_data.get('currency', '')}", "mt5_data_manager", "migration")

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error validando tipo de cuenta: {e}", "mt5_data_manager", "migration")
            self.account_type = AccountType.UNKNOWN

    def get_symbol_tick(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene el tick actual de un símbolo de forma segura.

        Args:
            symbol: Símbolo a consultar (ej: "EURUSD")

        Returns:
            Diccionario con información del tick o None si falla
        """
        if not mt5_available or mt5 is None:
            enviar_senal_log("ERROR", f"MT5 no disponible para obtener tick de {symbol}", "mt5_data_manager", "tick")
            return None

        if not self.is_connected:
            enviar_senal_log("WARNING", f"MT5 no conectado para obtener tick de {symbol}", "mt5_data_manager", "tick")
            return None

        try:
            # Verificar que la función esté disponible
            if not hasattr(mt5, 'symbol_info_tick'):
                enviar_senal_log("ERROR", f"Función symbol_info_tick no disponible en MT5", "mt5_data_manager", "tick")
                return None

            tick = mt5.symbol_info_tick(symbol)  # type: ignore
            if tick is None:
                enviar_senal_log("WARNING", f"No se pudo obtener tick para {symbol}", "mt5_data_manager", "tick")
                return None

            # Convertir a diccionario para facilitar el uso
            return {
                'symbol': symbol,
                'bid': tick.bid,
                'ask': tick.ask,
                'last': tick.last,
                'volume': tick.volume,
                'time': tick.time,
                'flags': tick.flags,
                'volume_real': getattr(tick, 'volume_real', 0.0)
            }

        except (ImportError, AttributeError, Exception) as e:
            enviar_senal_log("ERROR", f"Error obteniendo tick para {symbol}: {e}", "mt5_data_manager", "tick")
            return None

    def get_account_info(self) -> Dict[str, Any]:
        """
        Obtiene información completa de la cuenta desde MT5 directamente.

        Returns:
            Diccionario con información de la cuenta MT5
        """
        if not mt5_available or mt5 is None:
            return {"error": "MT5 no disponible"}

        if not self.is_connected:
            return {"error": "MT5 no conectado"}

        try:
            # Obtener información de cuenta directamente de MT5
            account_info = mt5.account_info()  # type: ignore
            if account_info is None:
                return {"error": "No se pudo obtener información de la cuenta"}

            # Convertir a diccionario con toda la información
            account_data = {
                "login": account_info.login,
                "trade_mode": account_info.trade_mode,
                "name": account_info.name,
                "server": account_info.server,
                "currency": account_info.currency,
                "balance": account_info.balance,
                "credit": account_info.credit,
                "profit": account_info.profit,
                "equity": account_info.equity,
                "margin": account_info.margin,
                "margin_free": account_info.margin_free,
                "margin_level": account_info.margin_level,
                "company": account_info.company,
                "broker": account_info.company,  # Alias para compatibilidad
                "leverage": account_info.leverage,
                "trade_allowed": account_info.trade_allowed,
                "trade_expert": account_info.trade_expert,
                "margin_so_mode": account_info.margin_so_mode,
                "margin_so_call": account_info.margin_so_call,
                "margin_so_so": account_info.margin_so_so,
                "currency_digits": account_info.currency_digits,
                "fifo_close": account_info.fifo_close
            }

            # Agregar información del validador si está disponible
            if self.account_validator:
                try:
                    validation = self.account_validator.validate_account_for_live_trading()
                    account_data.update({
                        "account_type": validation.get("account_type", "UNKNOWN"),
                        "suitable_for_live": validation.get("suitable_for_live_trading", False),
                        "risk_level": validation.get("risk_level", "UNKNOWN"),
                        "warnings": validation.get("warnings", []),
                        "type_description": self._get_account_type_description(account_info.trade_mode)
                    })
                except Exception as e:
                    enviar_senal_log("WARNING", f"Error obteniendo validación de cuenta: {e}", "mt5_data_manager", "account_info")

            return account_data

        except Exception as e:
            enviar_senal_log("ERROR", f"Error obteniendo información de cuenta MT5: {e}", "mt5_data_manager", "account_info")
            return {"error": f"Error: {e}"}

    def _get_account_type_description(self, trade_mode: int) -> str:
        """
        Convierte el trade_mode numérico a descripción legible.

        Args:
            trade_mode: Modo de trading de MT5

        Returns:
            Descripción del tipo de cuenta
        """
        trade_modes = {
            0: "Demo Account",
            1: "Contest Account",
            2: "Real Account"
        }
        return trade_modes.get(trade_mode, f"Unknown ({trade_mode})")

    def get_account_validator_info(self) -> Dict[str, Any]:
        """Obtiene información del validador de cuenta (función original)"""
        if not self.account_validator:
            return {"error": "Validador no disponible"}

        validation = self.account_validator.validate_account_for_live_trading()
        return {
            "account_type": validation["account_type"],
            "suitable_for_live": validation["suitable_for_live_trading"],
            "risk_level": validation.get("risk_level", "UNKNOWN"),
            "warnings": validation.get("warnings", []),
            "config": self.account_config or {}
        }

    def is_live_trading_enabled(self) -> bool:
        """Verifica si el trading en vivo está habilitado para esta cuenta"""
        if not self.account_config:
            return False
        return self.account_config.get("trading_enabled", False)

    def verificar_simbolo(self, simbolo: str) -> bool:
        """
        Verifica si un símbolo está disponible en MT5 y lo habilita si no lo está.

        Args:
            simbolo: El símbolo a verificar (ej: "EURUSD")

        Returns:
            True si el símbolo está disponible, False en caso contrario
        """
        if not mt5_available or mt5 is None:
            enviar_senal_log('ERROR', f"MT5 no disponible para verificar símbolo {simbolo}", __name__, 'mt5')
            return False

        if not self.is_connected:
            enviar_senal_log('ERROR', f"MT5 no conectado para verificar símbolo {simbolo}", __name__, 'mt5')
            return False

        try:
            # Obtener información del símbolo
            info = mt5.symbol_info(simbolo)  # type: ignore
            if info is None:
                enviar_senal_log('ERROR', f"Símbolo {simbolo} no encontrado en MT5", __name__, 'mt5')
                return False

            # Verificar si el símbolo está visible/habilitado
            if not info.visible:
                enviar_senal_log('WARNING', f"Símbolo {simbolo} no visible, intentando habilitarlo...", __name__, 'mt5')
                if not mt5.symbol_select(simbolo, True):  # type: ignore
                    enviar_senal_log('ERROR', f"No se pudo habilitar el símbolo {simbolo}", __name__, 'mt5')
                    return False

            enviar_senal_log('INFO', f"Símbolo {simbolo} verificado y disponible", __name__, 'mt5')
            return True

        except (FileNotFoundError, PermissionError, IOError) as e:
            enviar_senal_log('ERROR', f"Error verificando símbolo {simbolo}: {e}", __name__, 'mt5')
            return False

    def disconnect(self) -> None:
        """Desconecta de MetaTrader5."""
        if self.is_connected and self.available_functions.get('shutdown', False):
            try:
                mt5.shutdown()  # type: ignore
                self.is_connected = False
            except (FileNotFoundError, PermissionError, IOError):
                pass

    def get_timeframe_constant(self, timeframe: str) -> Optional[int]:
        """
        Obtiene la constante de timeframe de MT5.

        Args:
            timeframe: Timeframe como string ('M1', 'M5', etc.)

        Returns:
            Constante de MT5 o None si no existe
        """
        if not mt5_available or mt5 is None:
            return None

        try:
            # Primero intentar con el mapeo directo
            if timeframe in TIMEFRAME_MAPPING:
                tf_value = TIMEFRAME_MAPPING[timeframe]
                if tf_value < 100:  # Es un timeframe en minutos
                    return getattr(mt5, f'TIMEFRAME_{timeframe}', None)
                else:  # Es una constante directa
                    return tf_value

            # Si no existe, intentar obtenerlo directamente
            return getattr(mt5, f'TIMEFRAME_{timeframe}', None)
        except (FileNotFoundError, PermissionError, IOError):
            return None

    def download_historical_data(self,
                                symbol: str,
                                timeframe: str,
                                count: Optional[int] = None) -> Optional[pd.DataFrame]:
        """
        Descarga datos históricos de MT5 usando configuración FundedNext.

        Args:
            symbol: Símbolo a descargar (debe estar en la lista configurada)
            timeframe: Timeframe de las velas
            count: Número de velas (usa configuración por defecto si es None)

        Returns:
            DataFrame con los datos o None si falla
        """
        # Usar configuración específica de FundedNext
        if count is None:
            count = FUNDEDNEXT_CONFIG["max_bars"]

        # Verificar que el símbolo esté en la lista configurada
        if symbol not in FUNDEDNEXT_CONFIG["symbols"]:
            enviar_senal_log("INFO", f"⚠️  Símbolo {symbol} no está en la configuración FundedNext", "mt5_data_manager", "migration")
            enviar_senal_log("INFO", f"   Símbolos configurados: {FUNDEDNEXT_CONFIG['symbols']}", "mt5_data_manager", "migration")

        # Verificar que el timeframe esté configurado
        if timeframe not in FUNDEDNEXT_CONFIG["timeframes"]:
            enviar_senal_log("INFO", f"⚠️  Timeframe {timeframe} no está en la configuración FundedNext", "mt5_data_manager", "migration")
            enviar_senal_log("INFO", f"   Timeframes configurados: {FUNDEDNEXT_CONFIG['timeframes']}", "mt5_data_manager", "migration")

        if not self.is_connected:
            enviar_senal_log("INFO", "🔗 Conectando a FundedNext MT5...", "mt5_data_manager", "migration")
            if not self.connect():
                enviar_senal_log("INFO", "❌ No se pudo conectar a FundedNext MT5", "mt5_data_manager", "migration")
                return None

        timeframe_const = self.get_timeframe_constant(timeframe)
        if timeframe_const is None:
            enviar_senal_log("INFO", f"❌ Timeframe {timeframe} no reconocido por MT5", "mt5_data_manager", "migration")
            return None

        try:
            enviar_senal_log("INFO", f"📥 Descargando {count} velas de {symbol} {timeframe} desde FundedNext...", "mt5_data_manager", "migration")
            rates = None

            # Intentar con copy_rates_from_pos (preferido)
            if self.available_functions.get('copy_rates_from_pos', False):
                rates = mt5.copy_rates_from_pos(symbol, timeframe_const, 0, count)  # type: ignore

            # Si falla, intentar con copy_rates_from
            if rates is None and self.available_functions.get('copy_rates_from', False):
                import datetime
                end_time = datetime.datetime.now()
                rates = mt5.copy_rates_from(symbol, timeframe_const, end_time, count)  # type: ignore

            if rates is not None and len(rates) > 0:
                df = pd.DataFrame(rates)
                df['time'] = pd.to_datetime(df['time'], unit='s')
                df.set_index('time', inplace=True)
                return df

        except (FileNotFoundError, PermissionError, IOError) as e:
            enviar_senal_log("ERROR", f"Error descargando datos MT5: {e}", "mt5_data_manager", "migration")

        return None

    def save_data_to_csv(self, df: pd.DataFrame, timeframe: str) -> bool:
        """
        Guarda datos en archivo CSV.

        Args:
            df: DataFrame con los datos
            timeframe: Timeframe de los datos

        Returns:
            True si se guardó exitosamente
        """
        try:
            # Usar ruta absoluta desde el directorio actual
            current_dir = os.path.dirname(os.path.abspath(__file__))
            candles_dir = os.path.join(current_dir, '..', 'data', 'candles')
            csv_path = Path(candles_dir) / f"{timeframe}.csv"
            csv_path.parent.mkdir(parents=True, exist_ok=True)

            # Preparar DataFrame para guardar
            df_to_save = df.copy()

            # Si 'time' está como índice, resetearlo a columna
            if df_to_save.index.name == 'time':
                df_to_save = df_to_save.reset_index()

            # Asegurar que la columna 'time' existe y está en formato timestamp
            if 'time' in df_to_save.columns:
                # Convertir a timestamp si es datetime
                if df_to_save['time'].dtype.kind in ['M', 'O']:  # datetime or object
                    df_to_save['time'] = pd.to_datetime(df_to_save['time']).astype('int64') // 10**9
            else:
                enviar_senal_log("ERROR", f"❌ DataFrame no tiene columna 'time' para {timeframe}", "mt5_data_manager", "save_csv")
                return False

            df_to_save.to_csv(csv_path, index=False)
            enviar_senal_log("INFO", f"✅ Guardado {timeframe}.csv: {len(df_to_save)} velas", "mt5_data_manager", "save_csv")
            return True
        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error guardando {timeframe}.csv: {e}", "mt5_data_manager", "save_csv")
            return False

    def load_data_from_csv(self, timeframe: str, lookback: int = 10000) -> Optional[pd.DataFrame]:
        """
        Carga datos desde archivo CSV.

        Args:
            timeframe: Timeframe de los datos
            lookback: Número máximo de barras a cargar

        Returns:
            DataFrame con los datos o None si falla
        """
        try:
            # Usar ruta absoluta desde el directorio actual
            current_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = Path(os.path.join(current_dir, '..', 'data', 'candles', f"{timeframe}.csv"))

            if not csv_path.exists() or csv_path.stat().st_size < 100:
                return None

            df = pd.read_csv(csv_path)
            if df.empty:
                return None

            # Asegurar que la columna 'time' existe
            if 'time' not in df.columns:
                return None

            # Convertir timestamp a datetime y establecer como índice
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)

            return df.tail(lookback)
        except (FileNotFoundError, PermissionError, IOError) as e:
            enviar_senal_log("ERROR", f"Error cargando {timeframe} desde CSV: {e}", "mt5_data_manager", "migration")
            return None

    def get_historical_data(self,
                           symbol: str,
                           timeframe: str,
                           lookback: int = 10000,
                           force_download: bool = False) -> Optional[pd.DataFrame]:
        """
        Obtiene datos históricos desde CSV o descarga desde MT5.

        Args:
            symbol: Símbolo a obtener
            timeframe: Timeframe de las velas
            lookback: Número de barras a obtener
            force_download: Forzar descarga desde MT5

        Returns:
            DataFrame con los datos o None si falla
        """
        # Primero intentar cargar desde CSV si no se fuerza la descarga
        if not force_download:
            df = self.load_data_from_csv(timeframe, lookback)
            if df is not None:
                return df

        # Si no hay datos locales o se fuerza, descargar desde MT5
        df = self.download_historical_data(symbol, timeframe, lookback)
        if df is not None:
            # Guardar los datos para la próxima vez
            self.save_data_to_csv(df, timeframe)

        return df


# Instancia global del manager
_mt5_manager_instance: Optional[MT5DataManager] = None

def get_mt5_manager() -> MT5DataManager:
    """
    Obtiene la instancia global del MT5DataManager.
    GARANTIZA que solo se use el terminal FundedNext MT5.
    """
    global _mt5_manager_instance
    if _mt5_manager_instance is None:
        # Verificación de seguridad antes de crear la instancia
        if not validate_fundednext_installation():
            enviar_senal_log("ERROR", "🚨 SEGURIDAD: Terminal FundedNext MT5 no encontrado", "mt5_data_manager", "security")
            enviar_senal_log("ERROR", f"🚨 Ruta requerida: {FUNDEDNEXT_MT5_PATH}", "mt5_data_manager", "security")
            raise ConnectionError("SOLO se permite el uso del terminal FundedNext MT5")

        _mt5_manager_instance = MT5DataManager()
        enviar_senal_log("INFO", "🔒 MT5DataManager creado con seguridad FundedNext", "mt5_data_manager", "security")

    return _mt5_manager_instance

def force_fundednext_only_connection() -> bool:
    """
    Función de emergencia para garantizar conexión solo a FundedNext.

    Returns:
        True si la conexión es segura a FundedNext
    """
    try:
        # Desconectar cualquier conexión activa
        if mt5_available and mt5 is not None:
            mt5.shutdown()  # type: ignore

        # Verificar instalación FundedNext
        if not validate_fundednext_installation():
            enviar_senal_log("ERROR", "🚨 CRITICAL: FundedNext MT5 no disponible", "mt5_data_manager", "emergency")
            return False

        # Conectar específicamente a FundedNext
        if mt5_available and mt5 is not None:
            success = mt5.initialize(path=FUNDEDNEXT_MT5_PATH)  # type: ignore
            if success:
                terminal_info = mt5.terminal_info()  # type: ignore
                if terminal_info and "fundednext" in str(terminal_info.path).lower():
                    enviar_senal_log("INFO", "✅ SEGURIDAD: Conexión FundedNext verificada", "mt5_data_manager", "emergency")
                    return True
                else:
                    enviar_senal_log("ERROR", "🚨 TERMINAL INCORRECTO detectado", "mt5_data_manager", "emergency")
                    mt5.shutdown()  # type: ignore
                    return False

        return False

    except Exception as e:
        enviar_senal_log("ERROR", f"🚨 Error en conexión de emergencia: {e}", "mt5_data_manager", "emergency")
        return False

def cargar_datos_historicos_unificado(timeframe: str,
                                     lookback: int = 10000,
                                     symbol: str = "EURUSD") -> Optional[pd.DataFrame]:
    """
    Función unificada para cargar datos históricos.
    Reemplaza a las funciones dispersas del sistema.

    Args:
        timeframe: Timeframe de los datos ('M1', 'M5', etc.)
        lookback: Número de barras a cargar
        symbol: Símbolo a cargar

    Returns:
        DataFrame con los datos o None si falla
    """
    manager = get_mt5_manager()
    return manager.get_historical_data(symbol, timeframe, lookback)

def cargar_datos_historicos_resiliente(timeframe: str, lookback: int) -> Optional[pd.DataFrame]:
    """Función de compatibilidad con el sistema existente."""
    return cargar_datos_historicos_unificado(timeframe, lookback)

def auto_download_essential_data(symbols: Optional[List[str]] = None, timeframes: Optional[List[str]] = None, lookback: int = 30000) -> bool:
    """
    Descarga automática de datos esenciales para el sistema

    Args:
        symbols: Lista de símbolos (usa defaults si None)
        timeframes: Lista de timeframes (usa defaults si None)
        lookback: Número de velas a descargar

    Returns:
        True si la descarga fue exitosa
    """
    if symbols is None:
        symbols = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD"]

    if timeframes is None:
        timeframes = ["H4", "H1", "M15", "M5", "M1"]  # Orden de prioridad ICT

    manager = get_mt5_manager()
    successful_downloads = 0
    total_downloads = len(symbols) * len(timeframes)

    enviar_senal_log("INFO", f"🚀 Iniciando descarga automática: {total_downloads} conjuntos de datos", "mt5_data_manager", "auto_download")
    enviar_senal_log("INFO", f"📊 CONFIRMACIÓN: Descargando datos REALES directos del broker MT5", "mt5_data_manager", "auto_download")

    for symbol in symbols:
        for timeframe in timeframes:
            try:
                enviar_senal_log("INFO", f"📥 Descargando {symbol} {timeframe}...", "mt5_data_manager", "auto_download")

                df = manager.get_historical_data(symbol, timeframe, lookback, force_download=True)

                if df is not None and not df.empty:
                    successful_downloads += 1
                    enviar_senal_log("INFO", f"✅ {symbol} {timeframe}: {len(df)} velas descargadas", "mt5_data_manager", "auto_download")
                else:
                    enviar_senal_log("ERROR", f"❌ Error descargando {symbol} {timeframe}", "mt5_data_manager", "auto_download")

            except Exception as e:
                enviar_senal_log("ERROR", f"❌ Excepción descargando {symbol} {timeframe}: {e}", "mt5_data_manager", "auto_download")

    success_rate = (successful_downloads / total_downloads) * 100
    enviar_senal_log("INFO", f"📊 Descarga completada: {successful_downloads}/{total_downloads} ({success_rate:.1f}%)", "mt5_data_manager", "auto_download")

    return success_rate >= 80  # Consideramos exitoso si al menos 80% se descargó
