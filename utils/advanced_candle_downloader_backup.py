#!/usr/bin/env python3
"""
🚀 ADVANCED CANDLE DOWNLOADER - ICT ENGINE v5.0
===============================================

Sistema avanzado de descarga de velas con tecnología de múltiples fuentes:
- Descarga masiva optimizada para FundedNext MT5
- Barras de progreso en tiempo real
- Cálculo de velocidades de transferencia
- Cache inteligente y validación de datos
- Recuperación automática de errores
- Soporte para múltiples símbolos y timeframes

Basado en mejores prácticas de:
- SENTINEL_GRID_SYSTEM candle_data_downloader_progress.py
- ICT Engine v3.4 descargador_profesional.py
- SENTINEL_ICT_ANALYZER mt5_data_manager.py

Versión: v2.0.0
Autor: ICT Engine Team
Fecha: 02 Agosto 2025
"""

import sys
import os
import time
import json
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple, Union
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

# MIGRADO A SLUC v2.1
from sistema.logging_interface import enviar_senal_log

# Usar el MT5DataManager del sistema en lugar de MetaTrader5 directo
from utils.mt5_data_manager import get_mt5_manager

# =============================================================================
# CONFIGURACIÓN AVANZADA
# =============================================================================

# Configuración específica para FundedNext MT5
FUNDEDNEXT_CONFIG = {
    "executable_path": r"C:\Program Files\FundedNext MT5 Terminal\terminal64.exe",
    "max_bars_per_request": 5000,  # Optimizado para velocidad
    "connection_timeout": 30,
    "retry_delay": 2,
    "max_retries": 5
}

# Configuración de descarga
DOWNLOAD_CONFIG = {
    "symbols": ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "EURJPY", "EURGBP"],
    "timeframes": ["M1", "M3", "M5", "M15", "H1", "H4", "D1"],
    "default_lookback": 100000,  # 100K velas por defecto
    "chunk_size": 5000,  # Velas por chunk
    "parallel_downloads": 3,  # Descargas paralelas
    "verify_data_integrity": True,
    "backup_existing_data": True
}

# Mapeo de timeframes MT5
TIMEFRAME_MAPPING = {
    'M1': 1,
    'M3': 3,
    'M5': 5,
    'M15': 15,
    'H1': 16385,
    'H4': 16388,
    'D1': 16408
}

# =============================================================================
# DATACLASSES PARA ESTADÍSTICAS
# =============================================================================

@dataclass
class DownloadStats:
    """Estadísticas de descarga"""
    symbol: str
    timeframe: str
    total_bars: int
    downloaded_bars: int
    start_time: datetime
    end_time: Optional[datetime] = None
    success: bool = False
    error_message: str = ""

    @property
    def elapsed_time(self) -> float:
        """Tiempo transcurrido en segundos"""
        end = self.end_time if self.end_time else datetime.now()
        return (end - self.start_time).total_seconds()

    @property
    def download_speed(self) -> float:
        """Velocidad de descarga en velas/segundo"""
        if self.elapsed_time <= 0:
            return 0.0
        return self.downloaded_bars / self.elapsed_time

    @property
    def progress_percentage(self) -> float:
        """Porcentaje de progreso"""
        if self.total_bars <= 0:
            return 0.0
        return (self.downloaded_bars / self.total_bars) * 100

# =============================================================================
# CLASE PRINCIPAL - ADVANCED CANDLE DOWNLOADER
# =============================================================================

class AdvancedCandleDownloader:
    """
    🚀 ADVANCED CANDLE DOWNLOADER - Descarga masiva inteligente

    Características avanzadas:
    - Descarga paralela optimizada
    - Progreso en tiempo real con visualización
    - Cache inteligente y validación de datos
    - Recuperación automática de errores
    - Estadísticas detalladas de rendimiento
    """

    def __init__(self, data_dir: str = "data/candles"):
        """Inicializa el descargador avanzado usando el MT5DataManager del sistema"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.stats_dir = self.data_dir / "stats"
        self.stats_dir.mkdir(exist_ok=True)

        # Usar el MT5DataManager del sistema en lugar de MetaTrader5 directo
        self.mt5_manager = None
        self.is_connected = False
        self.download_stats: List[DownloadStats] = []
        self.active_downloads = 0
        self.total_downloads = 0

        enviar_senal_log("INFO", "🚀 AdvancedCandleDownloader inicializado", __name__, "downloader")
        self._validate_environment()

    def _validate_environment(self) -> bool:
        """Valida el ambiente de ejecución usando MT5DataManager"""
        try:
            # Usar el MT5DataManager ya inicializado del sistema
            self.mt5_manager = get_mt5_manager()

            if self.mt5_manager:
                enviar_senal_log("INFO", "✅ MT5DataManager disponible", __name__, "downloader")
                return True
            else:
                enviar_senal_log("WARNING", "⚠️ MT5DataManager no disponible", __name__, "downloader")
                return False

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error validando MT5DataManager: {e}", __name__, "downloader")
            return False

    def connect_mt5(self) -> bool:
        """Conecta a MetaTrader5 usando el MT5DataManager del sistema"""
        if not self.mt5_manager:
            enviar_senal_log("ERROR", "MT5DataManager no disponible", __name__, "downloader")
            return False

        enviar_senal_log("INFO", "🔗 Conectando a MT5 via MT5DataManager...", __name__, "downloader")

        try:
            # Usar el método de conexión del MT5DataManager
            if self.mt5_manager.connect():
                enviar_senal_log("INFO", "✅ Conectado a MT5 via MT5DataManager", __name__, "downloader")
                self.is_connected = True
                return True
            else:
                enviar_senal_log("ERROR", "❌ Falló la conexión via MT5DataManager", __name__, "downloader")
                return False

        except Exception as e:
            enviar_senal_log("ERROR", f"Error conectando via MT5DataManager: {e}", __name__, "downloader")
            return False

    def disconnect_mt5(self) -> None:
        """Desconecta de MetaTrader5 usando MT5DataManager"""
        if self.is_connected and self.mt5_manager:
            self.mt5_manager.disconnect()
            self.is_connected = False
            enviar_senal_log("INFO", "🔌 Desconectado de MT5 via MT5DataManager", __name__, "downloader")

    def download_symbol_timeframe(self, symbol: str, timeframe: str,
                                 lookback: Optional[int] = None) -> DownloadStats:
        """Descarga datos para un símbolo y timeframe específico usando MT5DataManager"""

        # Asegurar que lookback tiene un valor válido
        if lookback is None:
            lookback = DOWNLOAD_CONFIG["default_lookback"]

        # Asegurar que lookback es int para el tipo checking
        assert isinstance(lookback, int), "lookback debe ser un entero"

        stats = DownloadStats(
            symbol=symbol,
            timeframe=timeframe,
            total_bars=lookback,
            downloaded_bars=0,
            start_time=datetime.now()
        )

        try:
            enviar_senal_log("INFO", f"📥 Iniciando descarga {symbol} {timeframe} ({lookback:,} velas)", __name__, "downloader")

            if not self.is_connected:
                if not self.connect_mt5():
                    stats.error_message = "No se pudo conectar a MT5"
                    stats.end_time = datetime.now()
                    return stats

            # Usar MT5DataManager para descargar datos
            df = self.mt5_manager.download_historical_data(
                symbol=symbol,
                timeframe=timeframe,
                count=lookback
            )

            if df is not None and len(df) > 0:
                stats.downloaded_bars = len(df)

                # Validar integridad de datos si está habilitada
                if DOWNLOAD_CONFIG["verify_data_integrity"]:
                    is_valid, errors = self._validate_data_integrity(df, symbol, timeframe)
                    if not is_valid:
                        stats.error_message = f"Validación de datos falló: {'; '.join(errors)}"
                        stats.end_time = datetime.now()
                        return stats

                # Backup de datos existentes si está habilitado
                if DOWNLOAD_CONFIG["backup_existing_data"]:
                    if not self._backup_existing_data(symbol, timeframe):
                        enviar_senal_log("WARNING", f"⚠️ No se pudo crear backup para {symbol} {timeframe}", __name__, "downloader")

                # Guardar datos usando MT5DataManager
                if self.mt5_manager.save_data_to_csv(df, timeframe):
                    stats.success = True
                    enviar_senal_log("INFO", f"✅ {symbol} {timeframe} completado: {len(df):,} velas", __name__, "downloader")
                else:
                    stats.error_message = "Error guardando datos"
            else:
                stats.error_message = "No se pudieron descargar datos"

        except Exception as e:
            enviar_senal_log("ERROR", f"Error descargando {symbol} {timeframe}: {e}", __name__, "downloader")
            stats.error_message = str(e)

        stats.end_time = datetime.now()
        self.download_stats.append(stats)
        return stats

    def download_multiple(self, symbols: Optional[List[str]] = None,
                         timeframes: Optional[List[str]] = None,
                         lookback: Optional[int] = None,
                         use_parallel: bool = True) -> List[DownloadStats]:
        """Descarga múltiples símbolos y timeframes usando MT5DataManager con soporte paralelo"""

        # Asegurar que tenemos listas válidas (no None)
        symbols = symbols if symbols is not None else DOWNLOAD_CONFIG["symbols"]
        timeframes = timeframes if timeframes is not None else DOWNLOAD_CONFIG["timeframes"]
        lookback = lookback if lookback is not None else DOWNLOAD_CONFIG["default_lookback"]

        total_combinations = len(symbols) * len(timeframes)
        enviar_senal_log("INFO", f"🚀 Iniciando descarga masiva: {len(symbols)} símbolos × {len(timeframes)} timeframes = {total_combinations} descargas", __name__, "downloader")

        if use_parallel and total_combinations > 1:
            return self._download_parallel(symbols, timeframes, lookback)
        else:
            return self._download_sequential(symbols, timeframes, lookback)

    def _download_sequential(self, symbols: List[str], timeframes: List[str], lookback: int) -> List[DownloadStats]:
        """Descarga secuencial (método original)"""
        all_stats = []
        current_combination = 0
        total_combinations = len(symbols) * len(timeframes)

        for symbol in symbols:
            for timeframe in timeframes:
                current_combination += 1
                enviar_senal_log("INFO", f"📈 [{current_combination}/{total_combinations}] Procesando {symbol} {timeframe}", __name__, "downloader")

                stats = self.download_symbol_timeframe(symbol, timeframe, lookback)
                all_stats.append(stats)

                # Pequeña pausa entre descargas para no sobrecargar
                time.sleep(0.5)

        # Generar reporte final
        self._generate_download_report(all_stats)
        return all_stats

    def _download_parallel(self, symbols: List[str], timeframes: List[str], lookback: int) -> List[DownloadStats]:
        """Descarga paralela usando threading y concurrent.futures"""
        all_stats = []
        total_combinations = len(symbols) * len(timeframes)
        max_workers = min(DOWNLOAD_CONFIG["parallel_downloads"], total_combinations)

        enviar_senal_log("INFO", f"🔄 Modo paralelo activado: {max_workers} hilos", __name__, "downloader")

        # Crear lista de tareas
        tasks = []
        for symbol in symbols:
            for timeframe in timeframes:
                tasks.append((symbol, timeframe, lookback))

        # Ejecutar en paralelo usando ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Enviar todas las tareas
            future_to_task = {}
            for task in tasks:
                symbol, timeframe, lookback = task
                future = executor.submit(self._download_single_task, symbol, timeframe, lookback)
                future_to_task[future] = task

            # Procesar resultados conforme se completan
            completed = 0
            for future in as_completed(future_to_task):
                completed += 1
                task = future_to_task[future]
                symbol, timeframe, _ = task

                try:
                    stats = future.result()
                    all_stats.append(stats)
                    enviar_senal_log("INFO", f"✅ [{completed}/{total_combinations}] Completado: {symbol} {timeframe}", __name__, "downloader")
                except Exception as e:
                    enviar_senal_log("ERROR", f"❌ Error en {symbol} {timeframe}: {e}", __name__, "downloader")
                    # Crear stats de error
                    error_stats = DownloadStats(
                        symbol=symbol,
                        timeframe=timeframe,
                        total_bars=lookback,
                        downloaded_bars=0,
                        start_time=datetime.now(),
                        end_time=datetime.now(),
                        success=False,
                        error_message=str(e)
                    )
                    all_stats.append(error_stats)

        # Generar reporte final
        self._generate_download_report(all_stats)
        return all_stats

    def _download_single_task(self, symbol: str, timeframe: str, lookback: int) -> DownloadStats:
        """Tarea individual para descarga paralela - usa Union para tipo de retorno"""
        stats = DownloadStats(
            symbol=symbol,
            timeframe=timeframe,
            total_bars=lookback,
            downloaded_bars=0,
            start_time=datetime.now()
        )

        try:
            # Crear conexión MT5 independiente para este hilo
            task_mt5_manager = get_mt5_manager()
            if not task_mt5_manager:
                stats.error_message = "No se pudo obtener MT5DataManager"
                stats.end_time = datetime.now()
                return stats

            # Descargar datos
            df = task_mt5_manager.download_historical_data(
                symbol=symbol,
                timeframe=timeframe,
                count=lookback
            )

            if df is not None and len(df) > 0:
                stats.downloaded_bars = len(df)

                # Validar integridad si está habilitada
                if DOWNLOAD_CONFIG["verify_data_integrity"]:
                    is_valid, errors = self._validate_data_integrity(df, symbol, timeframe)
                    if not is_valid:
                        stats.error_message = f"Validación falló: {errors}"
                        stats.end_time = datetime.now()
                        return stats

                # Backup si está habilitado
                if DOWNLOAD_CONFIG["backup_existing_data"]:
                    self._backup_existing_data(symbol, timeframe)

                # Guardar datos
                if task_mt5_manager.save_data_to_csv(df, timeframe):
                    stats.success = True
                else:
                    stats.error_message = "Error guardando datos"
            else:
                stats.error_message = "No se pudieron descargar datos"

        except Exception as e:
            stats.error_message = str(e)

        stats.end_time = datetime.now()
        return stats

    def _generate_download_report(self, all_stats: List[DownloadStats]):
        """Genera reporte detallado de descarga"""
        successful = [s for s in all_stats if s.success]
        failed = [s for s in all_stats if not s.success]

        total_bars = sum(s.downloaded_bars for s in successful)
        total_time = sum(s.elapsed_time for s in all_stats)
        avg_speed = total_bars / total_time if total_time > 0 else 0

        enviar_senal_log("INFO", "📊 === REPORTE DE DESCARGA COMPLETADO ===", __name__, "downloader")
        enviar_senal_log("INFO", f"✅ Exitosas: {len(successful)}/{len(all_stats)}", __name__, "downloader")
        enviar_senal_log("INFO", f"❌ Fallidas: {len(failed)}", __name__, "downloader")
        enviar_senal_log("INFO", f"📈 Total velas descargadas: {total_bars:,}", __name__, "downloader")
        enviar_senal_log("INFO", f"⚡ Velocidad promedio: {self._format_speed(avg_speed)}", __name__, "downloader")
        enviar_senal_log("INFO", f"⏱️ Tiempo total: {total_time:.1f}s", __name__, "downloader")

        if failed:
            enviar_senal_log("WARNING", "❌ Descargas fallidas:", __name__, "downloader")
            for stats in failed:
                enviar_senal_log("WARNING", f"   {stats.symbol} {stats.timeframe}: {stats.error_message}", __name__, "downloader")

        # Guardar reporte en archivo
        self._save_download_report(all_stats)

    def _format_speed(self, speed: float) -> str:
        """Formatea la velocidad de descarga en formato legible"""
        if speed == 0:
            return "0 velas/s"
        elif speed >= 1000:
            return f"{speed/1000:.1f}K velas/s"
        elif speed >= 100:
            return f"{speed:.0f} velas/s"
        else:
            return f"{speed:.1f} velas/s"

    def _validate_data_integrity(self, df: pd.DataFrame, symbol: str, timeframe: str) -> Tuple[bool, List[str]]:
        """
        Valida la integridad de los datos descargados usando pandas y numpy
        Retorna: (es_válido, lista_de_errores)
        """
        errors = []

        if df is None or df.empty:
            errors.append("DataFrame está vacío o es None")
            return False, errors

        # Verificar columnas requeridas
        required_cols = ['time', 'open', 'high', 'low', 'close', 'tick_volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            errors.append(f"Columnas faltantes: {missing_cols}")

        # Verificar valores usando numpy
        if len(df) > 0:
            # Verificar valores NaN
            nan_cols = df.columns[df.isnull().any()].tolist()
            if nan_cols:
                errors.append(f"Valores NaN encontrados en: {nan_cols}")

            # Verificar que high >= low usando numpy
            if 'high' in df.columns and 'low' in df.columns:
                invalid_bars = np.sum(df['high'] < df['low'])
                if invalid_bars > 0:
                    errors.append(f"{invalid_bars} velas con High < Low")

            # Verificar que open y close estén dentro del rango high/low
            if all(col in df.columns for col in ['open', 'high', 'low', 'close']):
                invalid_open = np.sum((df['open'] > df['high']) | (df['open'] < df['low']))
                invalid_close = np.sum((df['close'] > df['high']) | (df['close'] < df['low']))

                if invalid_open > 0:
                    errors.append(f"{invalid_open} velas con Open fuera del rango High/Low")
                if invalid_close > 0:
                    errors.append(f"{invalid_close} velas con Close fuera del rango High/Low")

            # Verificar ordenamiento temporal
            if 'time' in df.columns and len(df) > 1:
                if not df['time'].is_monotonic_increasing:
                    errors.append("Los datos no están ordenados cronológicamente")

        is_valid = len(errors) == 0

        if is_valid:
            enviar_senal_log("DEBUG", f"✅ Validación exitosa: {symbol} {timeframe} ({len(df)} velas)", __name__, "downloader")
        else:
            enviar_senal_log("WARNING", f"⚠️ Errores de validación {symbol} {timeframe}: {errors}", __name__, "downloader")

        return is_valid, errors

    def _backup_existing_data(self, symbol: str, timeframe: str) -> bool:
        """Respalda datos existentes antes de sobrescribir usando timedelta para timestamp"""
        try:
            # Usar timedelta para crear timestamp único
            backup_time = datetime.now() - timedelta(microseconds=datetime.now().microsecond % 1000)
            timestamp = backup_time.strftime("%Y%m%d_%H%M%S")

            source_file = self.data_dir / f"{timeframe}.csv"
            if source_file.exists():
                backup_dir = self.data_dir / "backups"
                backup_dir.mkdir(exist_ok=True)
                backup_file = backup_dir / f"{symbol}_{timeframe}_{timestamp}.csv"

                # Usar pandas para leer y guardar el backup
                df_backup = pd.read_csv(source_file)
                df_backup.to_csv(backup_file, index=False)

                enviar_senal_log("INFO", f"📁 Backup creado: {backup_file.name}", __name__, "downloader")
                return True
            return True

        except Exception as e:
            enviar_senal_log("ERROR", f"Error creando backup: {e}", __name__, "downloader")
            return False

    def _save_download_report(self, all_stats: List[DownloadStats]):
        """Guarda reporte de descarga en archivo JSON"""
        try:
            report_data = {
                "timestamp": datetime.now().isoformat(),
                "total_downloads": len(all_stats),
                "successful": len([s for s in all_stats if s.success]),
                "failed": len([s for s in all_stats if not s.success]),
                "total_bars": sum(s.downloaded_bars for s in all_stats),
                "downloads": []
            }

            for stats in all_stats:
                report_data["downloads"].append({
                    "symbol": stats.symbol,
                    "timeframe": stats.timeframe,
                    "success": stats.success,
                    "bars_downloaded": stats.downloaded_bars,
                    "elapsed_time": stats.elapsed_time,
                    "download_speed": stats.download_speed,
                    "error_message": stats.error_message
                })

            report_file = self.stats_dir / f"download_report_{int(time.time())}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)

            enviar_senal_log("INFO", f"📋 Reporte guardado: {report_file.name}", __name__, "downloader")

        except Exception as e:
            enviar_senal_log("ERROR", f"Error guardando reporte: {e}", __name__, "downloader")

# =============================================================================
# FUNCIONES DE CONVENIENCIA
# =============================================================================

def download_single_timeframe(timeframe: str, lookback: Optional[int] = None) -> bool:
    """Descarga un timeframe específico para EURUSD"""
    downloader = AdvancedCandleDownloader()
    try:
        stats = downloader.download_symbol_timeframe("EURUSD", timeframe, lookback)
        return stats.success
    finally:
        downloader.disconnect_mt5()

def download_all_timeframes(lookback: Optional[int] = None) -> bool:
    """Descarga todos los timeframes para EURUSD"""
    downloader = AdvancedCandleDownloader()
    try:
        stats_list = downloader.download_multiple(["EURUSD"], None, lookback)
        return all(s.success for s in stats_list)
    finally:
        downloader.disconnect_mt5()

def download_full_database(lookback: Optional[int] = None) -> bool:
    """Descarga completa de todos los símbolos y timeframes"""
    downloader = AdvancedCandleDownloader()
    try:
        stats_list = downloader.download_multiple(None, None, lookback)
        successful = len([s for s in stats_list if s.success])
        total = len(stats_list)
        enviar_senal_log("INFO", f"🎯 Descarga completa finalizada: {successful}/{total} exitosas", __name__, "downloader")
        return successful == total
    finally:
        downloader.disconnect_mt5()

# =============================================================================
# MAIN - EJECUCIÓN DIRECTA
# =============================================================================

def main():
    """Función principal para ejecución directa"""
    enviar_senal_log("INFO", "🚀 === ADVANCED CANDLE DOWNLOADER v2.0 ===", __name__, "downloader")

    import argparse
    parser = argparse.ArgumentParser(description="Advanced Candle Downloader ICT Engine v5.0")
    parser.add_argument("--symbol", default="EURUSD", help="Símbolo a descargar")
    parser.add_argument("--timeframe", default="H4", help="Timeframe a descargar")
    parser.add_argument("--lookback", type=int, default=50000, help="Número de velas")
    parser.add_argument("--all", action="store_true", help="Descargar todos los timeframes")
    parser.add_argument("--full", action="store_true", help="Descarga completa de base de datos")

    args = parser.parse_args()

    if args.full:
        success = download_full_database(args.lookback)
    elif args.all:
        success = download_all_timeframes(args.lookback)
    else:
        success = download_single_timeframe(args.timeframe, args.lookback)

    if success:
        enviar_senal_log("INFO", "🎉 ¡Descarga completada exitosamente!", __name__, "downloader")
    else:
        enviar_senal_log("ERROR", "❌ Descarga falló", __name__, "downloader")

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
