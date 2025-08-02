# Utilidad para forzar la descarga y guardado de M1
def descargar_y_guardar_m1(symbol: str = "EURUSD", lookback: int = 200000) -> bool:
    """
    Descarga y guarda las velas de M1 siguiendo la lógica del sistema.
    """
    manager = get_mt5_manager()
    print(f"[MT5] Forzando descarga de velas M1 para {symbol}...")
    df = manager.get_historical_data(symbol, "M1", lookback, force_download=True)
    if df is not None and not df.empty:
        print(f"[MT5] Velas M1 descargadas y guardadas: {len(df)} filas.")
        return True
    else:
        print(f"[MT5] ERROR: No se pudieron descargar velas M1 para {symbol}.")
        return False
"""
MT5 Data Manager - Sistema Sentinel Grid v3.3.3.3.3
============================================

Módulo centralizado para manejar todas las operaciones de MetaTrader5
de forma consistente y con manejo de errores robusto.

Autor: Sistema Sentinel Grid v3.3.3.3.3
Fecha: 2025
"""

from typing import Optional, Any, Dict
import pandas as pd
# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log

import numpy as np
from pathlib import Path
import os

# Importación segura de MT5 y configuración FundedNext
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False
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
    """Valida que el terminal FundedNext esté instalado."""
    import os
    return os.path.exists(FUNDEDNEXT_MT5_PATH) and os.path.isfile(FUNDEDNEXT_MT5_PATH)

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
        self._check_mt5_availability()
        
    def _check_mt5_availability(self) -> None:
        """Verifica qué funciones de MT5 están disponibles."""
        if not MT5_AVAILABLE or mt5 is None:
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
        """Conecta específicamente al terminal FundedNext MT5."""
        if not MT5_AVAILABLE or mt5 is None:
            print("❌ MetaTrader5 no está disponible")
            return False
            
        if not validate_fundednext_installation():
            print(f"❌ Terminal FundedNext MT5 no encontrado en: {FUNDEDNEXT_MT5_PATH}")
            return False
            
        try:
            if self.available_functions.get('initialize', False):
                print(f"🔗 Conectando a FundedNext MT5: {FUNDEDNEXT_MT5_PATH}")
                
                # Intentar conexión con ruta específica de FundedNext
                self.is_connected = mt5.initialize(path=FUNDEDNEXT_MT5_PATH)  # type: ignore
                
                if self.is_connected:
                    # Obtener información del terminal conectado
                    try:
                        terminal_info = mt5.terminal_info()  # type: ignore
                        if terminal_info:
                            print(f"✅ Conectado a: {terminal_info.name}")
                            print(f"   Versión: {terminal_info.version}")
                            print(f"   Empresa: {terminal_info.company}")
                            print(f"   Ruta: {terminal_info.path}")
                        else:
                            print("✅ Conectado a FundedNext MT5")
                    except:
                        print("✅ Conectado a FundedNext MT5 (info limitada)")
                else:
                    print("❌ Error al conectar con FundedNext MT5")
                    
                return self.is_connected
        except (FileNotFoundError, PermissionError, IOError) as e:
            print(f"❌ Error de conexión MT5: {e}")
            
        return False
        
    def verificar_simbolo(self, simbolo: str) -> bool:
        """
        Verifica si un símbolo está disponible en MT5 y lo habilita si no lo está.
        
        Args:
            simbolo: El símbolo a verificar (ej: "EURUSD")
            
        Returns:
            True si el símbolo está disponible, False en caso contrario
        """
        if not MT5_AVAILABLE or mt5 is None:
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
        if not MT5_AVAILABLE or mt5 is None:
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
            print(f"⚠️  Símbolo {symbol} no está en la configuración FundedNext")
            print(f"   Símbolos configurados: {FUNDEDNEXT_CONFIG['symbols']}")
        
        # Verificar que el timeframe esté configurado
        if timeframe not in FUNDEDNEXT_CONFIG["timeframes"]:
            print(f"⚠️  Timeframe {timeframe} no está en la configuración FundedNext")
            print(f"   Timeframes configurados: {FUNDEDNEXT_CONFIG['timeframes']}")
            
        if not self.is_connected:
            print("🔗 Conectando a FundedNext MT5...")
            if not self.connect():
                print("❌ No se pudo conectar a FundedNext MT5")
                return None
                
        timeframe_const = self.get_timeframe_constant(timeframe)
        if timeframe_const is None:
            print(f"❌ Timeframe {timeframe} no reconocido por MT5")
            return None
            
        try:
            print(f"📥 Descargando {count} velas de {symbol} {timeframe} desde FundedNext...")
            rates = None
            
            # Intentar con copy_rates_from_pos (preferido)
            if self.available_functions.get('copy_rates_from_pos', False):
                rates = mt5.copy_rates_from_pos(symbol, timeframe_const, 0, count)  # type: ignore
            
            # Si falla, intentar con copy_rates_from
            if rates is None and self.available_functions.get('copy_rates_from', False):
                from datetime import datetime, timedelta
                end_time = datetime.now()
                rates = mt5.copy_rates_from(symbol, timeframe_const, end_time, count)  # type: ignore
            
            if rates is not None and len(rates) > 0:
                df = pd.DataFrame(rates)
                df['time'] = pd.to_datetime(df['time'], unit='s')
                df.set_index('time', inplace=True)
                return df
                
        except (FileNotFoundError, PermissionError, IOError) as e:
            print(f"Error descargando datos MT5: {e}")
            
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
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            candles_dir = os.path.join(current_dir, '..', 'data', 'candles')
            csv_path = Path(candles_dir) / f"{timeframe}.csv"
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Resetear índice para guardar la columna time
            df_to_save = df.reset_index()
            df_to_save['time'] = df_to_save['time'].astype('int64') // 10**9  # Convertir a timestamp
            df_to_save.to_csv(csv_path, index=False)
            return True
        except (FileNotFoundError, PermissionError, IOError):
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
            import os
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
            print(f"Error cargando {timeframe} desde CSV: {e}")
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
_mt5_manager = None

def get_mt5_manager() -> MT5DataManager:
    """Obtiene la instancia global del MT5DataManager."""
    global _mt5_manager
    if _mt5_manager is None:
        _mt5_manager = MT5DataManager()
    return _mt5_manager

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

# Funciones de compatibilidad para el sistema existente
def cargar_datos_historicos_resiliente(timeframe: str, lookback: int) -> Optional[pd.DataFrame]:
    """Función de compatibilidad con el sistema existente."""
    return cargar_datos_historicos_unificado(timeframe, lookback)
