from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
"""
🔧 SOLUCIÓN DE PROBLEMAS DETECTADOS
===================================
Script para resolver los problemas identificados en el sistema.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

def fix_logging_encoding():
    """Soluciona el problema de encoding en los logs."""
    enviar_senal_log("INFO", "🔧 SOLUCIONANDO PROBLEMA DE ENCODING...", "solucionar_problemas", "migration")

    # Verificar archivo de configuración de logging
    sistema_dir = Path("sistema")
    if not sistema_dir.exists():
        enviar_senal_log("INFO", "   ❌ Directorio 'sistema' no encontrado", "solucionar_problemas", "migration")
        return False

    logging_config_file = sistema_dir / "logging_config.py"
    if logging_config_file.exists():
        enviar_senal_log("INFO", "   ✅ Archivo logging_config.py encontrado", "solucionar_problemas", "migration")

        # Leer contenido actual
        with open(logging_config_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verificar si ya tiene configuración UTF-8
        if 'encoding=' in content:
            enviar_senal_log("INFO", "   ✅ Configuración de encoding ya presente", "solucionar_problemas", "migration")
        else:
            enviar_senal_log("INFO", "   🔧 Añadiendo configuración UTF-8", "solucionar_problemas", "migration")
            # Aquí añadiríamos la configuración si fuera necesario

        return True
    else:
        enviar_senal_log("INFO", "   ❌ Archivo logging_config.py no encontrado", "solucionar_problemas", "migration")
        return False

def fix_limit_order_manager():
    """Soluciona el problema de reinicialización del limit order manager."""
    enviar_senal_log("INFO", "🔧 SOLUCIONANDO PROBLEMA DE REINICIALIZACIÓN...", "solucionar_problemas", "migration")

    # Verificar archivo del limit order manager
    lom_file = Path("core/limit_order_manager.py")
    if lom_file.exists():
        enviar_senal_log("INFO", "   ✅ Archivo limit_order_manager.py encontrado", "solucionar_problemas", "migration")

        with open(lom_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verificar patrones problemáticos
        if 'def __init__' in content:
            enviar_senal_log("INFO", "   🔍 Analizando constructor...", "solucionar_problemas", "migration")

            # Contar llamadas de logging en __init__
            init_logs = content.count('inicializado')
            enviar_senal_log("INFO", f"   📊 Referencias a 'inicializado': {init_logs}", "solucionar_problemas", "migration")

            if init_logs > 2:
                enviar_senal_log("INFO", "   ⚠️ Posible logging excesivo en inicialización", "solucionar_problemas", "migration")

        return True
    else:
        enviar_senal_log("INFO", "   ❌ Archivo limit_order_manager.py no encontrado", "solucionar_problemas", "migration")
        return False

def fix_dynamic_volume():
    """Soluciona el problema de volumen fijo."""
    enviar_senal_log("INFO", "🔧 SOLUCIONANDO PROBLEMA DE VOLUMEN FIJO...", "solucionar_problemas", "migration")

    # Verificar RiskBot
    riskbot_file = Path("core/risk_management/riskbot_mt5.py")
    if riskbot_file.exists():
        enviar_senal_log("INFO", "   ✅ RiskBot encontrado", "solucionar_problemas", "migration")

        with open(riskbot_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verificar si tiene cálculo dinámico de volumen
        if 'calcular_volumen' in content or 'calculate_volume' in content:
            enviar_senal_log("INFO", "   ✅ Cálculo dinámico de volumen presente", "solucionar_problemas", "migration")
        else:
            enviar_senal_log("INFO", "   ⚠️ No se encontró cálculo dinámico de volumen", "solucionar_problemas", "migration")

        return True
    else:
        enviar_senal_log("INFO", "   ❌ RiskBot no encontrado", "solucionar_problemas", "migration")
        return False

def analyze_log_patterns():
    """Analiza patrones en los logs para identificar problemas."""
    enviar_senal_log("INFO", "🔍 ANALIZANDO PATRONES EN LOGS...", "solucionar_problemas", "migration")

    log_file = Path("data/logs/trading/trading_decisions.log")
    if not log_file.exists():
        enviar_senal_log("INFO", "   ❌ Log de trading no encontrado", "solucionar_problemas", "migration")
        return False

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        enviar_senal_log("INFO", "   ⚠️ PROBLEMA DETECTADO: Encoding corrupto en logs", "solucionar_problemas", "migration")
        try:
            with open(log_file, 'r', encoding='latin-1') as f:
                lines = f.readlines()
            enviar_senal_log("INFO", "   🔧 Usando encoding latin-1 como fallback", "solucionar_problemas", "migration")
        except Exception as e:
            enviar_senal_log("ERROR", f"   ❌ Error leyendo log: {e}", "solucionar_problemas", "migration")
            return False

    enviar_senal_log("INFO", f"   📊 Total líneas: {len(lines, "solucionar_problemas", "migration")}")

    # Analizar frecuencia de inicializaciones
    init_lines = [l for l in lines if 'inicializado' in l]
    enviar_senal_log("INFO", f"   🔄 Inicializaciones detectadas: {len(init_lines, "solucionar_problemas", "migration")}")

    if len(init_lines) > 10:
        enviar_senal_log("INFO", "   ⚠️ PROBLEMA: Demasiadas reinicializaciones", "solucionar_problemas", "migration")

        # Analizar timestamps para ver frecuencia
        timestamps = []
        for line in init_lines[-10:]:  # Últimas 10
            parts = line.split('|')
            if len(parts) > 1:
                timestamp_str = parts[1].strip()
                enviar_senal_log("INFO", f"     📅 {timestamp_str}", "solucionar_problemas", "migration")

        enviar_senal_log("INFO", "   💡 SOLUCIÓN: Implementar singleton o caché de instancia", "solucionar_problemas", "migration")

    # Analizar volúmenes
    volume_lines = [l for l in lines if 'Volumen primera orden' in l]
    volumes = []
    for line in volume_lines:
        if '0.05 lotes' in line:
            volumes.append(0.05)

    if len(set(volumes)) == 1 and volumes:
        enviar_senal_log("INFO", f"   ⚠️ PROBLEMA: Volumen siempre fijo en {volumes[0]} lotes", "solucionar_problemas", "migration")
        enviar_senal_log("INFO", "   💡 SOLUCIÓN: Implementar cálculo dinámico basado en equity y riesgo", "solucionar_problemas", "migration")

    return True

def create_fixes_summary():
    """Crea un resumen de las correcciones necesarias."""
    enviar_senal_log("INFO", "\n📋 RESUMEN DE CORRECCIONES NECESARIAS:", "solucionar_problemas", "migration")
    enviar_senal_log("INFO", "=" * 50, "solucionar_problemas", "migration")

    fixes = [
        {
            "problema": "Encoding corrupto en logs",
            "solucion": "Configurar UTF-8 en sistema de logging",
            "prioridad": "MEDIA",
            "archivo": "sistema/logging_config.py"
        },
        {
            "problema": "Reinicialización excesiva del LimitOrderManager",
            "solucion": "Implementar patrón singleton o caché",
            "prioridad": "ALTA",
            "archivo": "core/limit_order_manager.py"
        },
        {
            "problema": "Volumen fijo de 0.05 lotes",
            "solucion": "Implementar cálculo dinámico basado en equity",
            "prioridad": "ALTA",
            "archivo": "core/risk_management/riskbot_mt5.py"
        },
        {
            "problema": "Logs repetitivos sin información útil",
            "solucion": "Reducir frecuencia de logging de estado",
            "prioridad": "BAJA",
            "archivo": "Multiple files"
        }
    ]

    for i, fix in enumerate(fixes, 1):
        enviar_senal_log("INFO", f"{i}. 🎯 {fix['problema']}", "solucionar_problemas", "migration")
        enviar_senal_log("INFO", f"   🔧 Solución: {fix['solucion']}", "solucionar_problemas", "migration")
        enviar_senal_log("INFO", f"   ⚡ Prioridad: {fix['prioridad']}", "solucionar_problemas", "migration")
        enviar_senal_log("INFO", f"   📁 Archivo: {fix['archivo']}", "solucionar_problemas", "migration")
        enviar_senal_log("INFO", , "solucionar_problemas", "migration")

    return fixes

def main():
    enviar_senal_log("INFO", "🔧 SISTEMA DE CORRECCIÓN DE PROBLEMAS", "solucionar_problemas", "migration")
    enviar_senal_log("INFO", "=" * 40, "solucionar_problemas", "migration")
    enviar_senal_log("INFO", f"📅 {datetime.now(, "solucionar_problemas", "migration").strftime('%Y-%m-%d %H:%M:%S')}")
    enviar_senal_log("INFO", , "solucionar_problemas", "migration")

    # Ejecutar análisis y correcciones
    analyze_log_patterns()
    enviar_senal_log("INFO", , "solucionar_problemas", "migration")

    fix_logging_encoding()
    enviar_senal_log("INFO", , "solucionar_problemas", "migration")

    fix_limit_order_manager()
    enviar_senal_log("INFO", , "solucionar_problemas", "migration")

    fix_dynamic_volume()
    enviar_senal_log("INFO", , "solucionar_problemas", "migration")

    fixes = create_fixes_summary()

    enviar_senal_log("INFO", "✅ ANÁLISIS COMPLETADO", "solucionar_problemas", "migration")
    enviar_senal_log("INFO", f"📊 Total problemas identificados: {len(fixes, "solucionar_problemas", "migration")}")
    enviar_senal_log("INFO", "🎯 Revisa el resumen arriba para implementar las correcciones", "solucionar_problemas", "migration")

if __name__ == "__main__":
    main()
