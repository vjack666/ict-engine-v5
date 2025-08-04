#!/usr/bin/env python3
"""
📊 ICT ENGINE v5.0 - ANALIZADOR DE LOGS
========================================

Script para analizar y generar reportes inteligentes de los logs del sistema.
Detecta patrones, errores críticos y métricas de rendimiento.

Uso:
    python analizar_logs.py
    python analizar_logs.py --detailed
    python analizar_logs.py --errors-only
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import re
from collections import defaultdict
from typing import Dict, List, Tuple

# 📁 Configurar paths del proyecto
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from sistema.logging_interface import enviar_senal_log

def analizar_logs_mt5(log_path: Path) -> Dict:
    """Analiza los logs de MT5"""
    print("🔍 Analizando logs de MT5...")

    if not log_path.exists():
        return {"error": "Archivo no encontrado"}

    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()

    stats = {
        "descargas_exitosas": len(re.findall(r'velas descargadas', content)),
        "conexiones_mt5": len(re.findall(r'Conectado a.*MT5', content)),
        "errores": len(re.findall(r'ERROR.*MT5', content)),
        "warnings": len(re.findall(r'WARNING.*MT5', content)),
        "datos_reales_confirmados": len(re.findall(r'datos REALES', content, re.IGNORECASE)),
        "simbolos_procesados": set(re.findall(r'Descargando ([A-Z]{6})', content)),
        "timeframes_procesados": set(re.findall(r'Descargando [A-Z]{6} ([MHD]\d+)', content)),
        "cuenta_detectada": re.search(r'CUENTA (\w+) detectada', content),
        "broker_info": re.search(r'Broker: ([^\\n]+)', content),
        "balance_info": re.search(r'Balance: ([\d.]+)', content)
    }

    return stats

def analizar_logs_dashboard(log_path: Path) -> Dict:
    """Analiza los logs del dashboard"""
    print("📊 Analizando logs del dashboard...")

    if not log_path.exists():
        return {"error": "Archivo no encontrado"}

    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()

    stats = {
        "inicios_dashboard": len(re.findall(r'Dashboard.*inicializado', content)),
        "migraciones_sluc": len(re.findall(r'Migrando a SLUC', content)),
        "errores": len(re.findall(r'ERROR', content)),
        "warnings": len(re.findall(r'WARNING', content)),
        "activaciones_centro_mando": len(re.findall(r'Centro de Mando activado', content))
    }

    return stats

def analizar_logs_errores(log_path: Path) -> Dict:
    """Analiza los logs de errores"""
    print("❌ Analizando logs de errores...")

    if not log_path.exists():
        return {"error": "Archivo no encontrado"}

    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.strip().split('\\n')
    errores_criticos = []
    warnings_importantes = []

    for line in lines:
        if 'ERROR' in line and 'CRITICAL' in line:
            errores_criticos.append(line)
        elif 'WARNING' in line and any(keyword in line for keyword in ['FAILED', 'Error', 'problema']):
            warnings_importantes.append(line)

    stats = {
        "total_errores": len(re.findall(r'ERROR', content)),
        "errores_criticos": len(errores_criticos),
        "warnings_importantes": len(warnings_importantes),
        "errores_recientes": errores_criticos[-5:] if errores_criticos else [],
        "warnings_recientes": warnings_importantes[-5:] if warnings_importantes else []
    }

    return stats

def detectar_patrones_problematicos(logs_dir: Path) -> List[str]:
    """Detecta patrones problemáticos en todos los logs"""
    print("🔍 Detectando patrones problemáticos...")

    problemas = []

    # Buscar archivos de log de hoy
    today = datetime.now().strftime("%Y%m%d")

    for log_file in logs_dir.rglob(f"*{today}.log"):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Patrones problemáticos
            if 'conexión rechazada' in content.lower():
                problemas.append(f"🔴 Conexiones rechazadas detectadas en {log_file.name}")

            if 'timeout' in content.lower():
                problemas.append(f"⏰ Timeouts detectados en {log_file.name}")

            if 'permission denied' in content.lower():
                problemas.append(f"🚫 Permisos denegados en {log_file.name}")

            if re.search(r'ERROR.*MT5.*not available', content):
                problemas.append(f"❌ MT5 no disponible en {log_file.name}")

            if 'memoria insuficiente' in content.lower():
                problemas.append(f"💾 Problemas de memoria en {log_file.name}")

        except Exception as e:
            problemas.append(f"❌ Error leyendo {log_file.name}: {e}")

    return problemas

def generar_resumen_rendimiento(stats_mt5: Dict) -> str:
    """Genera resumen de rendimiento del sistema"""

    rendimiento = []

    # Evaluar descargas
    if stats_mt5.get("descargas_exitosas", 0) > 25:
        rendimiento.append("✅ Descargas MT5: EXCELENTE")
    elif stats_mt5.get("descargas_exitosas", 0) > 15:
        rendimiento.append("🟡 Descargas MT5: BUENO")
    else:
        rendimiento.append("🔴 Descargas MT5: PROBLEMÁTICO")

    # Evaluar conexiones
    if stats_mt5.get("conexiones_mt5", 0) > 0:
        rendimiento.append("✅ Conectividad MT5: FUNCIONAL")
    else:
        rendimiento.append("🔴 Conectividad MT5: FALLANDO")

    # Evaluar datos reales
    if stats_mt5.get("datos_reales_confirmados", 0) > 0:
        rendimiento.append("✅ Datos REALES: CONFIRMADO")
    else:
        rendimiento.append("🟡 Datos REALES: NO CONFIRMADO")

    # Evaluar errores
    if stats_mt5.get("errores", 0) == 0:
        rendimiento.append("✅ Estado de errores: LIMPIO")
    elif stats_mt5.get("errores", 0) < 3:
        rendimiento.append("🟡 Estado de errores: ACEPTABLE")
    else:
        rendimiento.append("🔴 Estado de errores: CRÍTICO")

    return "\\n".join(rendimiento)

def main():
    """Función principal del analizador"""

    print("=" * 70)
    print("📊 ICT ENGINE v5.0 - ANÁLISIS INTELIGENTE DE LOGS")
    print("=" * 70)
    print()

    logs_dir = PROJECT_ROOT / "data" / "logs"
    today = datetime.now().strftime("%Y%m%d")

    # Analizar logs específicos
    stats_mt5 = analizar_logs_mt5(logs_dir / "mt5" / f"mt5_{today}.log")
    stats_dashboard = analizar_logs_dashboard(logs_dir / "dashboard" / f"dashboard_{today}.log")
    stats_errores = analizar_logs_errores(logs_dir / "errors" / f"errors_{today}.log")

    # Detectar patrones problemáticos
    problemas = detectar_patrones_problematicos(logs_dir)

    # Generar reporte
    print("📈 ESTADÍSTICAS MT5:")
    print("-" * 30)
    if "error" not in stats_mt5:
        print(f"  💾 Descargas exitosas: {stats_mt5['descargas_exitosas']}")
        print(f"  🔗 Conexiones MT5: {stats_mt5['conexiones_mt5']}")
        print(f"  📊 Confirmaciones datos REALES: {stats_mt5['datos_reales_confirmados']}")
        print(f"  📈 Símbolos procesados: {len(stats_mt5['simbolos_procesados'])}")
        print(f"  ⏰ Timeframes procesados: {len(stats_mt5['timeframes_procesados'])}")

        if stats_mt5['cuenta_detectada']:
            print(f"  🏦 Tipo de cuenta: {stats_mt5['cuenta_detectada'].group(1)}")
        if stats_mt5['broker_info']:
            print(f"  🏢 Broker: {stats_mt5['broker_info'].group(1)}")
        if stats_mt5['balance_info']:
            print(f"  💰 Balance: ${stats_mt5['balance_info'].group(1)}")

        print(f"  ❌ Errores: {stats_mt5['errores']}")
        print(f"  ⚠️ Warnings: {stats_mt5['warnings']}")
    else:
        print(f"  ❌ {stats_mt5['error']}")

    print()
    print("📊 ESTADÍSTICAS DASHBOARD:")
    print("-" * 30)
    if "error" not in stats_dashboard:
        print(f"  🚀 Inicios dashboard: {stats_dashboard['inicios_dashboard']}")
        print(f"  🔄 Migraciones SLUC: {stats_dashboard['migraciones_sluc']}")
        print(f"  🎛️ Activaciones centro mando: {stats_dashboard['activaciones_centro_mando']}")
        print(f"  ❌ Errores: {stats_dashboard['errores']}")
        print(f"  ⚠️ Warnings: {stats_dashboard['warnings']}")
    else:
        print(f"  ❌ {stats_dashboard['error']}")

    print()
    print("❌ ANÁLISIS DE ERRORES:")
    print("-" * 30)
    if "error" not in stats_errores:
        print(f"  🔴 Total errores: {stats_errores['total_errores']}")
        print(f"  💥 Errores críticos: {stats_errores['errores_criticos']}")
        print(f"  ⚠️ Warnings importantes: {stats_errores['warnings_importantes']}")

        if stats_errores['errores_recientes']:
            print("  📋 Errores recientes:")
            for error in stats_errores['errores_recientes']:
                print(f"    • {error[:100]}...")
    else:
        print(f"  ❌ {stats_errores['error']}")

    print()
    print("🔍 PATRONES PROBLEMÁTICOS:")
    print("-" * 30)
    if problemas:
        for problema in problemas:
            print(f"  {problema}")
    else:
        print("  ✅ No se detectaron patrones problemáticos")

    print()
    print("🎯 EVALUACIÓN DE RENDIMIENTO:")
    print("-" * 30)
    rendimiento = generar_resumen_rendimiento(stats_mt5)
    for linea in rendimiento.split("\\n"):
        print(f"  {linea}")

    print()
    print("🔧 RECOMENDACIONES:")
    print("-" * 30)

    # Generar recomendaciones basadas en el análisis
    if stats_mt5.get("errores", 0) > 0:
        print("  🔴 Revisar errores de MT5 - pueden afectar la descarga de datos")

    if stats_mt5.get("descargas_exitosas", 0) < 20:
        print("  🟡 Pocas descargas exitosas - verificar conectividad MT5")

    if not stats_mt5.get("datos_reales_confirmados", 0):
        print("  ⚠️ No se confirmaron datos REALES - verificar configuración")

    if stats_dashboard.get("errores", 0) > 0:
        print("  📊 Errores en dashboard - revisar logs detallados")

    if not problemas and stats_mt5.get("descargas_exitosas", 0) > 25:
        print("  🎉 ¡Sistema funcionando ÓPTIMAMENTE!")

    print()
    print("=" * 70)
    print(f"📅 Análisis completado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

if __name__ == "__main__":
    main()
