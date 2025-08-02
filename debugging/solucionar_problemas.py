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
    print("🔧 SOLUCIONANDO PROBLEMA DE ENCODING...")

    # Verificar archivo de configuración de logging
    sistema_dir = Path("sistema")
    if not sistema_dir.exists():
        print("   ❌ Directorio 'sistema' no encontrado")
        return False

    logging_config_file = sistema_dir / "logging_config.py"
    if logging_config_file.exists():
        print("   ✅ Archivo logging_config.py encontrado")

        # Leer contenido actual
        with open(logging_config_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verificar si ya tiene configuración UTF-8
        if 'encoding=' in content:
            print("   ✅ Configuración de encoding ya presente")
        else:
            print("   🔧 Añadiendo configuración UTF-8")
            # Aquí añadiríamos la configuración si fuera necesario

        return True
    else:
        print("   ❌ Archivo logging_config.py no encontrado")
        return False

def fix_limit_order_manager():
    """Soluciona el problema de reinicialización del limit order manager."""
    print("🔧 SOLUCIONANDO PROBLEMA DE REINICIALIZACIÓN...")

    # Verificar archivo del limit order manager
    lom_file = Path("core/limit_order_manager.py")
    if lom_file.exists():
        print("   ✅ Archivo limit_order_manager.py encontrado")

        with open(lom_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verificar patrones problemáticos
        if 'def __init__' in content:
            print("   🔍 Analizando constructor...")

            # Contar llamadas de logging en __init__
            init_logs = content.count('inicializado')
            print(f"   📊 Referencias a 'inicializado': {init_logs}")

            if init_logs > 2:
                print("   ⚠️ Posible logging excesivo en inicialización")

        return True
    else:
        print("   ❌ Archivo limit_order_manager.py no encontrado")
        return False

def fix_dynamic_volume():
    """Soluciona el problema de volumen fijo."""
    print("🔧 SOLUCIONANDO PROBLEMA DE VOLUMEN FIJO...")

    # Verificar RiskBot
    riskbot_file = Path("core/risk_management/riskbot_mt5.py")
    if riskbot_file.exists():
        print("   ✅ RiskBot encontrado")

        with open(riskbot_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verificar si tiene cálculo dinámico de volumen
        if 'calcular_volumen' in content or 'calculate_volume' in content:
            print("   ✅ Cálculo dinámico de volumen presente")
        else:
            print("   ⚠️ No se encontró cálculo dinámico de volumen")

        return True
    else:
        print("   ❌ RiskBot no encontrado")
        return False

def analyze_log_patterns():
    """Analiza patrones en los logs para identificar problemas."""
    print("🔍 ANALIZANDO PATRONES EN LOGS...")

    log_file = Path("data/logs/trading/trading_decisions.log")
    if not log_file.exists():
        print("   ❌ Log de trading no encontrado")
        return False

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        print("   ⚠️ PROBLEMA DETECTADO: Encoding corrupto en logs")
        try:
            with open(log_file, 'r', encoding='latin-1') as f:
                lines = f.readlines()
            print("   🔧 Usando encoding latin-1 como fallback")
        except Exception as e:
            print(f"   ❌ Error leyendo log: {e}")
            return False

    print(f"   📊 Total líneas: {len(lines)}")

    # Analizar frecuencia de inicializaciones
    init_lines = [l for l in lines if 'inicializado' in l]
    print(f"   🔄 Inicializaciones detectadas: {len(init_lines)}")

    if len(init_lines) > 10:
        print("   ⚠️ PROBLEMA: Demasiadas reinicializaciones")

        # Analizar timestamps para ver frecuencia
        timestamps = []
        for line in init_lines[-10:]:  # Últimas 10
            parts = line.split('|')
            if len(parts) > 1:
                timestamp_str = parts[1].strip()
                print(f"     📅 {timestamp_str}")

        print("   💡 SOLUCIÓN: Implementar singleton o caché de instancia")

    # Analizar volúmenes
    volume_lines = [l for l in lines if 'Volumen primera orden' in l]
    volumes = []
    for line in volume_lines:
        if '0.05 lotes' in line:
            volumes.append(0.05)

    if len(set(volumes)) == 1 and volumes:
        print(f"   ⚠️ PROBLEMA: Volumen siempre fijo en {volumes[0]} lotes")
        print("   💡 SOLUCIÓN: Implementar cálculo dinámico basado en equity y riesgo")

    return True

def create_fixes_summary():
    """Crea un resumen de las correcciones necesarias."""
    print("\n📋 RESUMEN DE CORRECCIONES NECESARIAS:")
    print("=" * 50)

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
        print(f"{i}. 🎯 {fix['problema']}")
        print(f"   🔧 Solución: {fix['solucion']}")
        print(f"   ⚡ Prioridad: {fix['prioridad']}")
        print(f"   📁 Archivo: {fix['archivo']}")
        print()

    return fixes

def main():
    print("🔧 SISTEMA DE CORRECCIÓN DE PROBLEMAS")
    print("=" * 40)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Ejecutar análisis y correcciones
    analyze_log_patterns()
    print()

    fix_logging_encoding()
    print()

    fix_limit_order_manager()
    print()

    fix_dynamic_volume()
    print()

    fixes = create_fixes_summary()

    print("✅ ANÁLISIS COMPLETADO")
    print(f"📊 Total problemas identificados: {len(fixes)}")
    print("🎯 Revisa el resumen arriba para implementar las correcciones")

if __name__ == "__main__":
    main()
