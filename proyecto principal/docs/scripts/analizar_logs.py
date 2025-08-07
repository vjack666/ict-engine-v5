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

# MIGRACIÓN SIC v3.0 + SLUC v2.1
from sistema.sic import enviar_senal_log, log_info, log_warning

from sistema.sic import sys
from sistema.sic import Path
from sistema.sic import datetime, timedelta
from sistema.sic import re
from sistema.sic import defaultdict
from sistema.sic import Dict, List, Tuple

# 📁 Configurar paths del proyecto
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from sistema.sic import enviar_senal_log

def analizar_logs_mt5(log_path: Path) -> Dict:
    """Analiza los logs de MT5"""
    enviar_senal_log('INFO', '🔍 Analizando logs de MT5...', __name__, 'analisis')

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
    enviar_senal_log('INFO', '📊 Analizando logs del dashboard...', __name__, 'analisis')

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
    enviar_senal_log('INFO', "❌ Analizando logs de errores...", __name__, "analisis")

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
    enviar_senal_log('INFO', '🔍 Detectando patrones problemáticos...', __name__, 'analisis')

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

    enviar_senal_log('INFO', '=' * 70, __name__, 'analisis')
    enviar_senal_log('INFO', '📊 ICT ENGINE v5.0 - ANÁLISIS INTELIGENTE DE LOGS', __name__, 'analisis')
    enviar_senal_log('INFO', '=' * 70, __name__, 'analisis')

    logs_dir = PROJECT_ROOT / "data" / "logs"
    today = datetime.now().strftime("%Y%m%d")

    # Analizar logs específicos
    stats_mt5 = analizar_logs_mt5(logs_dir / "mt5" / f"mt5_{today}.log")
    stats_dashboard = analizar_logs_dashboard(logs_dir / "dashboard" / f"dashboard_{today}.log")
    stats_errores = analizar_logs_errores(logs_dir / "errors" / f"errors_{today}.log")

    # Detectar patrones problemáticos
    problemas = detectar_patrones_problematicos(logs_dir)

    # Generar reporte
    enviar_senal_log('INFO', '📈 ESTADÍSTICAS MT5:', __name__, 'analisis')
    enviar_senal_log('INFO', '-' * 30, __name__, 'analisis')
    if "error" not in stats_mt5:
        enviar_senal_log('INFO', f"  💾 Descargas exitosas: {stats_mt5['descargas_exitosas']}", __name__, 'analisis')
        enviar_senal_log('INFO', f"  🔗 Conexiones MT5: {stats_mt5['conexiones_mt5']}", __name__, 'analisis')
        enviar_senal_log('INFO', f"  📊 Confirmaciones datos REALES: {stats_mt5['datos_reales_confirmados']}", __name__, 'analisis')
        enviar_senal_log('INFO', f"  📈 Símbolos procesados: {len(stats_mt5['simbolos_procesados'])}", __name__, 'analisis')
        enviar_senal_log('INFO', f"  ⏰ Timeframes procesados: {len(stats_mt5['timeframes_procesados'])}", __name__, 'analisis')

        if stats_mt5['cuenta_detectada']:
            enviar_senal_log('INFO', f"  🏦 Tipo de cuenta: {stats_mt5['cuenta_detectada'].group(1)}", __name__, 'analisis')
        if stats_mt5['broker_info']:
            enviar_senal_log('INFO', f"Broker: {stats_mt5['broker_info'].group(1)}", __name__, 'sistema')
        if stats_mt5['balance_info']:
            enviar_senal_log('INFO', f"Balance: ${stats_mt5['balance_info'].group(1)}", __name__, 'sistema')

        enviar_senal_log('ERROR', f"Errores: {stats_mt5['errores']}", __name__, 'sistema')
        enviar_senal_log('WARNING', f"Warnings: {stats_mt5['warnings']}", __name__, 'sistema')
    else:
        enviar_senal_log('ERROR', f"{stats_mt5['error']}", __name__, 'sistema')

    enviar_senal_log('INFO', '', __name__, 'analisis')
    enviar_senal_log('INFO', '📊 ESTADÍSTICAS DASHBOARD:', __name__, 'analisis')
    enviar_senal_log('INFO', '-' * 30, __name__, 'analisis')
    if "error" not in stats_dashboard:
        enviar_senal_log('INFO', f"  🚀 Inicios dashboard: {stats_dashboard['inicios_dashboard']}", __name__, 'analisis')
        enviar_senal_log('INFO', f"  🔄 Migraciones SLUC: {stats_dashboard['migraciones_sluc']}", __name__, 'analisis')
        enviar_senal_log('INFO', f"  🎛️ Activaciones centro mando: {stats_dashboard['activaciones_centro_mando']}", __name__, 'analisis')
        enviar_senal_log('ERROR', f"  ❌ Errores: {stats_dashboard['errores']}", __name__, 'sistema')
        enviar_senal_log('WARNING', f"  ⚠️ Warnings: {stats_dashboard['warnings']}", __name__, 'sistema')
    else:
        enviar_senal_log('ERROR', f"  ❌ {stats_dashboard['error']}", __name__, 'sistema')

    enviar_senal_log('INFO', '', __name__, 'analisis')
    enviar_senal_log('INFO', '❌ ANÁLISIS DE ERRORES:', __name__, 'analisis')
    enviar_senal_log('INFO', '-' * 30, __name__, 'analisis')
    if "error" not in stats_errores:
        enviar_senal_log('INFO', f"  🔴 Total errores: {stats_errores['total_errores']}", __name__, 'analisis')
        enviar_senal_log('INFO', f"  💥 Errores críticos: {stats_errores['errores_criticos']}", __name__, 'analisis')
        enviar_senal_log('WARNING', f"  ⚠️ Warnings importantes: {stats_errores['warnings_importantes']}", __name__, 'sistema')

        if stats_errores['errores_recientes']:
            enviar_senal_log('INFO', "  📋 Errores recientes:", __name__, 'analisis')
            for error in stats_errores['errores_recientes']:
                enviar_senal_log('ERROR', f"    • {error[:100]}...", __name__, 'sistema')
    else:
        enviar_senal_log('ERROR', f"  ❌ {stats_errores['error']}", __name__, 'sistema')

    enviar_senal_log('INFO', '', __name__, 'analisis')
    enviar_senal_log('INFO', '🔍 PATRONES PROBLEMÁTICOS:', __name__, 'analisis')
    enviar_senal_log('INFO', '-' * 30, __name__, 'analisis')
    if problemas:
        for problema in problemas:
            enviar_senal_log('INFO', f"  {problema}", __name__, 'analisis')
    else:
        enviar_senal_log('INFO', "  ✅ No se detectaron patrones problemáticos", __name__, 'analisis')

    enviar_senal_log('INFO', '', __name__, 'analisis')
    enviar_senal_log('INFO', '🎯 EVALUACIÓN DE RENDIMIENTO:', __name__, 'analisis')
    enviar_senal_log('INFO', '-' * 30, __name__, 'analisis')
    rendimiento = generar_resumen_rendimiento(stats_mt5)
    for linea in rendimiento.split("\\n"):
        enviar_senal_log('INFO', f"  {linea}", __name__, 'analisis')

    enviar_senal_log('INFO', '', __name__, 'analisis')
    enviar_senal_log('INFO', '🔧 RECOMENDACIONES:', __name__, 'analisis')
    enviar_senal_log('INFO', '-' * 30, __name__, 'analisis')

    # Generar recomendaciones basadas en el análisis
    if stats_mt5.get("errores", 0) > 0:
        enviar_senal_log('WARNING', "  🔴 Revisar errores de MT5 - pueden afectar la descarga de datos", __name__, 'sistema')

    if stats_mt5.get("descargas_exitosas", 0) < 20:
        enviar_senal_log('WARNING', "  🟡 Pocas descargas exitosas - verificar conectividad MT5", __name__, 'sistema')

    if not stats_mt5.get("datos_reales_confirmados", 0):
        enviar_senal_log('WARNING', "  ⚠️ No se confirmaron datos REALES - verificar configuración", __name__, 'sistema')

    if stats_dashboard.get("errores", 0) > 0:
        enviar_senal_log('WARNING', "  📊 Errores en dashboard - revisar logs detallados", __name__, 'sistema')

    if not problemas and stats_mt5.get("descargas_exitosas", 0) > 25:
        enviar_senal_log('INFO', "  🎉 ¡Sistema funcionando ÓPTIMAMENTE!", __name__, 'analisis')

    enviar_senal_log('INFO', '', __name__, 'analisis')
    enviar_senal_log('INFO', '=' * 70, __name__, 'analisis')
    enviar_senal_log('INFO', f"📅 Análisis completado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", __name__, 'analisis')
    enviar_senal_log('INFO', '=' * 70, __name__, 'analisis')

if __name__ == "__main__":
    main()
