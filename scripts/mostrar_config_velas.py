#!/usr/bin/env python3
"""
RESUMEN: ¿CUÁNTAS VELAS SE DESCARGAN?
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def mostrar_configuracion_velas():
    """Muestra cuántas velas se descargan en el sistema"""

    # Importar configuración
    from utils.advanced_candle_downloader import DOWNLOAD_CONFIG

    print('📊 === CONFIGURACIÓN DE DESCARGA DE VELAS ===')
    print()
    print(f'📈 VELAS POR DEFECTO: {DOWNLOAD_CONFIG["default_lookback"]:,} velas')
    print(f'🎯 SÍMBOLOS: {len(DOWNLOAD_CONFIG["symbols"])} símbolos')
    print(f'⏰ TIMEFRAMES: {len(DOWNLOAD_CONFIG["timeframes"])} timeframes')
    print(f'📦 CHUNK SIZE: {DOWNLOAD_CONFIG["chunk_size"]:,} velas por chunk')
    print()
    print('📋 SÍMBOLOS CONFIGURADOS:')
    for i, symbol in enumerate(DOWNLOAD_CONFIG["symbols"], 1):
        print(f'   {i}. {symbol}')
    print()
    print('⏱️ TIMEFRAMES CONFIGURADOS:')
    for i, tf in enumerate(DOWNLOAD_CONFIG["timeframes"], 1):
        print(f'   {i}. {tf}')
    print()
    print('🔢 CÁLCULOS DE DESCARGA:')
    velas_por_descarga = DOWNLOAD_CONFIG["default_lookback"]
    total_simbolos = len(DOWNLOAD_CONFIG["symbols"])
    total_timeframes = len(DOWNLOAD_CONFIG["timeframes"])
    total_combinaciones = total_simbolos * total_timeframes
    total_velas_completa = total_combinaciones * velas_por_descarga

    print(f'   • Una sola descarga: {velas_por_descarga:,} velas')
    print(f'   • Descarga completa: {total_velas_completa:,} velas totales')
    print(f'   • Combinaciones posibles: {total_combinaciones} descargas')
    print()
    print('⚙️ CONFIGURACIÓN MAIN():')
    print('   • Argumento --lookback por defecto: 50,000 velas')
    print('   • Configuración interna por defecto: 100,000 velas')
    print()
    print('🎯 EJEMPLOS DE USO:')
    print('   • python utils/advanced_candle_downloader.py --timeframe H4')
    print('     → Descarga 50,000 velas de EURUSD H4')
    print('   • python utils/advanced_candle_downloader.py --all')
    print('     → Descarga 50,000 velas de EURUSD en todos los timeframes')
    print('   • python utils/advanced_candle_downloader.py --full')
    print('     → Descarga 50,000 velas de todos los símbolos y timeframes')
    print('   • python utils/advanced_candle_downloader.py --lookback 200000')
    print('     → Descarga 200,000 velas personalizadas')

if __name__ == "__main__":
    mostrar_configuracion_velas()
