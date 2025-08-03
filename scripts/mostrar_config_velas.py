from sistema.logging_interface import enviar_senal_log
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

    enviar_senal_log("INFO", '📊 === CONFIGURACIÓN DE DESCARGA DE VELAS ===', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", , "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", f'📈 VELAS POR DEFECTO: {DOWNLOAD_CONFIG["default_lookback"]:,} velas', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", f'🎯 SÍMBOLOS: {len(DOWNLOAD_CONFIG["symbols"], "mostrar_config_velas", "migration")} símbolos')
    enviar_senal_log("INFO", f'⏰ TIMEFRAMES: {len(DOWNLOAD_CONFIG["timeframes"], "mostrar_config_velas", "migration")} timeframes')
    enviar_senal_log("INFO", f'📦 CHUNK SIZE: {DOWNLOAD_CONFIG["chunk_size"]:,} velas por chunk', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", , "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", '📋 SÍMBOLOS CONFIGURADOS:', "mostrar_config_velas", "migration")
    for i, symbol in enumerate(DOWNLOAD_CONFIG["symbols"], 1):
        enviar_senal_log("INFO", f'   {i}. {symbol}', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", , "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", '⏱️ TIMEFRAMES CONFIGURADOS:', "mostrar_config_velas", "migration")
    for i, tf in enumerate(DOWNLOAD_CONFIG["timeframes"], 1):
        enviar_senal_log("INFO", f'   {i}. {tf}', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", , "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", '🔢 CÁLCULOS DE DESCARGA:', "mostrar_config_velas", "migration")
    velas_por_descarga = DOWNLOAD_CONFIG["default_lookback"]
    total_simbolos = len(DOWNLOAD_CONFIG["symbols"])
    total_timeframes = len(DOWNLOAD_CONFIG["timeframes"])
    total_combinaciones = total_simbolos * total_timeframes
    total_velas_completa = total_combinaciones * velas_por_descarga

    enviar_senal_log("INFO", f'   • Una sola descarga: {velas_por_descarga:,} velas', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", f'   • Descarga completa: {total_velas_completa:,} velas totales', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", f'   • Combinaciones posibles: {total_combinaciones} descargas', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", , "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", '⚙️ CONFIGURACIÓN MAIN(, "mostrar_config_velas", "migration"):')
    enviar_senal_log("INFO", '   • Argumento --lookback por defecto: 50,000 velas', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", '   • Configuración interna por defecto: 100,000 velas', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", , "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", '🎯 EJEMPLOS DE USO:', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", '   • python utils/advanced_candle_downloader.py --timeframe H4', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", '     → Descarga 50,000 velas de EURUSD H4', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", '   • python utils/advanced_candle_downloader.py --all', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", '     → Descarga 50,000 velas de EURUSD en todos los timeframes', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", '   • python utils/advanced_candle_downloader.py --full', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", '     → Descarga 50,000 velas de todos los símbolos y timeframes', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", '   • python utils/advanced_candle_downloader.py --lookback 200000', "mostrar_config_velas", "migration")
    enviar_senal_log("INFO", '     → Descarga 200,000 velas personalizadas', "mostrar_config_velas", "migration")

if __name__ == "__main__":
    mostrar_configuracion_velas()
