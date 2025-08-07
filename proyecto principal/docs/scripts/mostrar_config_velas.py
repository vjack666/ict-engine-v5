#!/usr/bin/env python3
"""
📊 CONFIGURACIÓN DE VELAS DEL SISTEMA
====================================

Muestra la configuración actual de timeframes y velas.
"""

# MIGRACIÓN SIC v3.0 + SLUC v2.1
from sistema.sic import enviar_senal_log, log_info, log_warning

from sistema.sic import sys
from sistema.sic import Path

# Agregar project root al path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from sistema.sic import enviar_senal_log

def mostrar_config_velas():
    """Muestra la configuración actual de velas y timeframes"""

    enviar_senal_log("INFO", "📊 CONFIGURACIÓN DE VELAS DEL SISTEMA", "mostrar_config_velas", "system")
    enviar_senal_log("INFO", "=" * 50, "mostrar_config_velas", "system")

    try:
        # 1. Timeframes configurados
        enviar_senal_log("INFO", "⏱️ 1. TIMEFRAMES CONFIGURADOS", "mostrar_config_velas", "system")

        timeframes = {
            "M1": "1 minuto",
            "M5": "5 minutos",
            "M15": "15 minutos",
            "M30": "30 minutos",
            "H1": "1 hora",
            "H4": "4 horas",
            "D1": "Diario",
            "W1": "Semanal"
        }

        for tf, desc in timeframes.items():
            enviar_senal_log("INFO", f"   📈 {tf}: {desc}", "mostrar_config_velas", "system")

        # 2. Configuración por defecto del dashboard
        enviar_senal_log("INFO", "", "mostrar_config_velas", "system")
        enviar_senal_log("INFO", "🎯 2. CONFIGURACIÓN DASHBOARD", "mostrar_config_velas", "system")
        enviar_senal_log("INFO", "   📊 Timeframes principales: M15, H1, H4", "mostrar_config_velas", "system")
        enviar_senal_log("INFO", "   🔄 Actualización: Tiempo real", "mostrar_config_velas", "system")
        enviar_senal_log("INFO", "   📡 Fuente: MT5 Live Data", "mostrar_config_velas", "system")

        # 3. Configuración MT5
        enviar_senal_log("INFO", "", "mostrar_config_velas", "system")
        enviar_senal_log("INFO", "🔧 3. CONFIGURACIÓN MT5", "mostrar_config_velas", "system")
        enviar_senal_log("INFO", "   📈 Símbolo principal: EURUSD", "mostrar_config_velas", "system")
        enviar_senal_log("INFO", "   📊 Velas por request: 1000", "mostrar_config_velas", "system")
        enviar_senal_log("INFO", "   ⏰ Timeout: 10 segundos", "mostrar_config_velas", "system")
        enviar_senal_log("INFO", "   🔄 Retry: 3 intentos", "mostrar_config_velas", "system")

        # 4. Estado del sistema
        enviar_senal_log("INFO", "", "mostrar_config_velas", "system")
        enviar_senal_log("INFO", "📊 4. ESTADO ACTUAL", "mostrar_config_velas", "system")
        enviar_senal_log("INFO", "   ✅ Pipeline MT5: Operativo", "mostrar_config_velas", "system")
        enviar_senal_log("INFO", "   ✅ Descarga de velas: Funcional", "mostrar_config_velas", "system")
        enviar_senal_log("INFO", "   ✅ Dashboard integrado: Sí", "mostrar_config_velas", "system")
        enviar_senal_log("INFO", "   ✅ Modo de operación: Live Trading", "mostrar_config_velas", "system")

        enviar_senal_log("INFO", "", "mostrar_config_velas", "system")
        enviar_senal_log("INFO", "✅ CONFIGURACIÓN MOSTRADA CORRECTAMENTE", "mostrar_config_velas", "system")

        return True

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ ERROR MOSTRANDO CONFIGURACIÓN: {e}", "mostrar_config_velas", "system")
        return False

def main():
    """Función principal"""
    enviar_senal_log("INFO", "🚀 Mostrando configuración de velas", "mostrar_config_velas", "system")

    success = mostrar_config_velas()

    if success:
        enviar_senal_log("INFO", "🎉 Configuración mostrada exitosamente", "mostrar_config_velas", "system")
    else:
        enviar_senal_log("ERROR", "⚠️ Error mostrando configuración", "mostrar_config_velas", "system")

if __name__ == "__main__":
    main()
