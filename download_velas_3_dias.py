#!/usr/bin/env python3
"""
📥 CANDLE DOWNLOADER INDEPENDIENTE
================================

Script autónomo para descargar velas de los últimos 3 días
en timeframes H4, H1, y M15, guardándolas en una carpeta
separada del sistema principal.

Uso:
    python download_velas_3_dias.py

Autor: Sistema ICT Engine v5.0
Fecha: 2025-08-06
"""

import sys
import os
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime, timedelta
from pathlib import Path
import traceback

# Configuración básica
SYMBOL = "EURUSD"
TIMEFRAMES = {
    'H4': mt5.TIMEFRAME_H4,
    'H1': mt5.TIMEFRAME_H1,
    'M15': mt5.TIMEFRAME_M15
}

# Crear carpeta de datos de hoy
fecha_hoy = datetime.now().strftime("%Y%m%d")
data_folder = Path(f"data_{fecha_hoy}")
data_folder.mkdir(exist_ok=True)

def inicializar_mt5():
    """Inicializar conexión con MetaTrader5"""
    print("🔗 Iniciando conexión con MetaTrader5...")

    if not mt5.initialize():
        print(f"❌ Error inicializando MT5: {mt5.last_error()}")
        return False

    # Verificar información de cuenta
    account_info = mt5.account_info()
    if account_info is None:
        print("❌ No se pudo obtener información de cuenta")
        mt5.shutdown()
        return False

    print(f"✅ MT5 conectado exitosamente")
    print(f"📊 Cuenta: {account_info.login}")
    print(f"💰 Broker: {account_info.company}")
    print(f"💱 Moneda: {account_info.currency}")

    return True

def verificar_simbolo(symbol):
    """Verificar que el símbolo esté disponible"""
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"❌ Símbolo {symbol} no encontrado")
        return False

    if not symbol_info.visible:
        print(f"📊 Habilitando símbolo {symbol}...")
        if not mt5.symbol_select(symbol, True):
            print(f"❌ Error habilitando símbolo {symbol}")
            return False

    print(f"✅ Símbolo {symbol} verificado y disponible")
    return True

def descargar_velas(symbol, timeframe_name, timeframe_mt5, dias=3):
    """
    Descargar velas para un timeframe específico

    Args:
        symbol: Símbolo a descargar (ej: EURUSD)
        timeframe_name: Nombre del timeframe (ej: H1)
        timeframe_mt5: Timeframe de MT5 (ej: mt5.TIMEFRAME_H1)
        dias: Número de días hacia atrás

    Returns:
        DataFrame con las velas o None si hay error
    """
    try:
        print(f"📥 Descargando {symbol} {timeframe_name} - {dias} días...")

        # Calcular fechas
        fecha_fin = datetime.now()
        fecha_inicio = fecha_fin - timedelta(days=dias)

        print(f"📅 Desde: {fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📅 Hasta: {fecha_fin.strftime('%Y-%m-%d %H:%M:%S')}")

        # Obtener datos históricos
        rates = mt5.copy_rates_range(symbol, timeframe_mt5, fecha_inicio, fecha_fin)

        if rates is None:
            error = mt5.last_error()
            print(f"❌ Error descargando datos: {error}")
            return None

        if len(rates) == 0:
            print(f"⚠️ No se encontraron datos para el período especificado")
            return None

        # Convertir a DataFrame
        df = pd.DataFrame(rates)

        # Convertir timestamp a datetime
        df['time'] = pd.to_datetime(df['time'], unit='s')

        # Reordenar columnas
        df = df[['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']]

        print(f"✅ Descargadas {len(df)} velas de {symbol} {timeframe_name}")
        print(f"📊 Primera vela: {df['time'].iloc[0]}")
        print(f"📊 Última vela: {df['time'].iloc[-1]}")

        return df

    except Exception as e:
        print(f"❌ Error en descarga: {e}")
        traceback.print_exc()
        return None

def guardar_velas(df, symbol, timeframe_name, data_folder):
    """
    Guardar velas en archivo CSV

    Args:
        df: DataFrame con las velas
        symbol: Símbolo
        timeframe_name: Nombre del timeframe
        data_folder: Carpeta donde guardar
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{symbol}_{timeframe_name}_{timestamp}.csv"
        filepath = data_folder / filename

        # Guardar con índice de tiempo como columna
        df.to_csv(filepath, index=False)

        print(f"💾 Guardado: {filepath}")
        print(f"📊 Archivo tamaño: {filepath.stat().st_size / 1024:.1f} KB")

        return filepath

    except Exception as e:
        print(f"❌ Error guardando archivo: {e}")
        return None

def generar_resumen(resultados, data_folder):
    """Generar archivo de resumen con estadísticas"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        resumen_file = data_folder / "resumen_descarga.txt"

        with open(resumen_file, 'w', encoding='utf-8') as f:
            f.write("📥 RESUMEN DE DESCARGA DE VELAS\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"🕐 Fecha de descarga: {timestamp}\n")
            f.write(f"📊 Símbolo: {SYMBOL}\n")
            f.write(f"📅 Período: Últimos 3 días\n")
            f.write(f"📁 Carpeta: {data_folder.name}\n\n")

            f.write("📋 ARCHIVOS GENERADOS:\n")
            f.write("-" * 30 + "\n")

            total_velas = 0
            for timeframe, resultado in resultados.items():
                if resultado['success']:
                    velas = resultado['velas']
                    archivo = resultado['archivo']
                    total_velas += velas

                    f.write(f"✅ {timeframe}:\n")
                    f.write(f"   📁 Archivo: {archivo.name}\n")
                    f.write(f"   📊 Velas: {velas}\n")
                    f.write(f"   📏 Tamaño: {archivo.stat().st_size / 1024:.1f} KB\n\n")
                else:
                    f.write(f"❌ {timeframe}: {resultado['error']}\n\n")

            f.write(f"📈 TOTAL DE VELAS DESCARGADAS: {total_velas}\n")
            f.write(f"💾 TOTAL DE ARCHIVOS: {len([r for r in resultados.values() if r['success']])}\n")

        print(f"📄 Resumen guardado: {resumen_file}")

    except Exception as e:
        print(f"❌ Error generando resumen: {e}")

def main():
    """Función principal"""
    print("=" * 60)
    print("📥 CANDLE DOWNLOADER INDEPENDIENTE v1.0")
    print("=" * 60)
    print(f"🎯 Símbolo: {SYMBOL}")
    print(f"📅 Período: Últimos 3 días")
    print(f"⏰ Timeframes: {', '.join(TIMEFRAMES.keys())}")
    print(f"📁 Carpeta de datos: {data_folder}")
    print("=" * 60)

    # Inicializar MT5
    if not inicializar_mt5():
        print("❌ No se pudo conectar a MT5. Cerrando...")
        sys.exit(1)

    # Verificar símbolo
    if not verificar_simbolo(SYMBOL):
        print(f"❌ Símbolo {SYMBOL} no disponible. Cerrando...")
        mt5.shutdown()
        sys.exit(1)

    # Diccionario para almacenar resultados
    resultados = {}

    try:
        # Descargar cada timeframe
        for timeframe_name, timeframe_mt5 in TIMEFRAMES.items():
            print(f"\n📥 PROCESANDO {timeframe_name}")
            print("-" * 40)

            # Descargar velas
            df = descargar_velas(SYMBOL, timeframe_name, timeframe_mt5, dias=3)

            if df is not None:
                # Guardar archivo
                archivo = guardar_velas(df, SYMBOL, timeframe_name, data_folder)

                if archivo:
                    resultados[timeframe_name] = {
                        'success': True,
                        'velas': len(df),
                        'archivo': archivo,
                        'primera_vela': df['time'].iloc[0],
                        'ultima_vela': df['time'].iloc[-1]
                    }
                    print(f"✅ {timeframe_name} completado exitosamente")
                else:
                    resultados[timeframe_name] = {
                        'success': False,
                        'error': 'Error guardando archivo'
                    }
                    print(f"❌ {timeframe_name} falló al guardar")
            else:
                resultados[timeframe_name] = {
                    'success': False,
                    'error': 'Error descargando datos'
                }
                print(f"❌ {timeframe_name} falló en descarga")

    except KeyboardInterrupt:
        print("\n⚠️ Descarga interrumpida por usuario")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        traceback.print_exc()

    finally:
        # Cerrar MT5
        mt5.shutdown()
        print("\n🔌 Conexión MT5 cerrada")

    # Generar resumen
    print("\n📄 GENERANDO RESUMEN...")
    print("-" * 40)
    generar_resumen(resultados, data_folder)

    # Mostrar estadísticas finales
    exitosos = len([r for r in resultados.values() if r['success']])
    total = len(resultados)

    print(f"\n📊 ESTADÍSTICAS FINALES:")
    print("-" * 40)
    print(f"✅ Exitosos: {exitosos}/{total}")
    print(f"❌ Fallidos: {total - exitosos}/{total}")

    if exitosos > 0:
        total_velas = sum(r['velas'] for r in resultados.values() if r['success'])
        print(f"📈 Total velas descargadas: {total_velas}")
        print(f"📁 Archivos en: {data_folder}")
        print(f"📄 Ver resumen completo: {data_folder}/resumen_descarga.txt")

    print("\n🎯 Descarga completada!")

    # Abrir carpeta de datos (opcional)
    try:
        import webbrowser
        webbrowser.open(str(data_folder.absolute()))
        print(f"📁 Abriendo carpeta: {data_folder}")
    except:
        pass

if __name__ == "__main__":
    main()
