from sistema.logging_interface import enviar_senal_log
"""
🔍 VERIFICADOR DE LOGS DE BITÁCORAS
=================================

Script para verificar si los logs del Multi-POI Dashboard se están
registrando correctamente en las bitácoras del sistema.
"""

import os
from datetime import datetime

def verificar_logs_sistema():
    """Verifica los logs en todas las carpetas de bitácoras."""

    enviar_senal_log("INFO", "🔍 VERIFICANDO LOGS DEL SISTEMA POI/ICT...", "verificar_logs", "migration")
    enviar_senal_log("INFO", "=" * 60, "verificar_logs", "migration")

    # Directorios de logs a verificar
    log_dirs = {
        'POI': 'data/logs/poi',
        'ICT': 'data/logs/ict',
        'Dashboard': 'data/logs/dashboard',
        'MT5': 'data/logs/mt5',
        'General': 'data/logs/general',
        'Analysis': 'data/logs/analysis',
        'Structured': 'data/logs/structured'
    }

    resultados = {}

    for categoria, path in log_dirs.items():
        enviar_senal_log("INFO", f"\n📂 {categoria} LOGS ({path}, "verificar_logs", "migration"):")

        if not os.path.exists(path):
            enviar_senal_log("INFO", f"   ❌ Directorio no existe: {path}", "verificar_logs", "migration")
            resultados[categoria] = {'status': 'NO_EXISTE', 'archivos': []}
            continue

        archivos = [f for f in os.listdir(path) if f.endswith('.log')]
        resultados[categoria] = {'status': 'EXISTE', 'archivos': archivos}

        if not archivos:
            enviar_senal_log("INFO", f"   ⚠️  Directorio vacío - sin archivos .log", "verificar_logs", "migration")
        else:
            for archivo in archivos:
                archivo_path = os.path.join(path, archivo)
                try:
                    # Verificar tamaño y fecha de modificación
                    stat = os.stat(archivo_path)
                    tamaño = stat.st_size
                    mod_time = datetime.fromtimestamp(stat.st_mtime)

                    # Leer últimas líneas para verificar actividad reciente
                    with open(archivo_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        total_lines = len(lines)

                        # Buscar logs de hoy
                        hoy = datetime.now().strftime("%Y-%m-%d")
                        logs_hoy = [l for l in lines if hoy in l]

                        # Buscar logs relacionados a POI/Dashboard
                        logs_poi = [l for l in lines if any(word in l.lower() for word in ['poi', 'dashboard', 'multi-poi', 'forex'])]

                    enviar_senal_log("INFO", f"   ✅ {archivo}", "verificar_logs", "migration")
                    enviar_senal_log("INFO", f"      └─ Tamaño: {tamaño} bytes | Líneas: {total_lines}", "verificar_logs", "migration")
                    enviar_senal_log("INFO", f"      └─ Modificado: {mod_time.strftime('%Y-%m-%d %H:%M:%S', "verificar_logs", "migration")}")
                    enviar_senal_log("INFO", f"      └─ Logs hoy: {len(logs_hoy, "verificar_logs", "migration")} | Logs POI: {len(logs_poi)}")

                    # Si hay logs POI, mostrar algunos ejemplos
                    if logs_poi:
                        enviar_senal_log("INFO", f"      📊 EJEMPLOS DE LOGS POI/DASHBOARD:", "verificar_logs", "migration")
                        for i, log_line in enumerate(logs_poi[-3:], 1):  # Últimos 3
                            enviar_senal_log("INFO", f"         {i}. {log_line.strip(, "verificar_logs", "migration")[:80]}...")

                except Exception as e:
                    enviar_senal_log("ERROR", f"   ❌ Error leyendo {archivo}: {e}", "verificar_logs", "migration")

    enviar_senal_log("INFO", "\n" + "=" * 60, "verificar_logs", "migration")
    enviar_senal_log("INFO", "📊 RESUMEN DE VERIFICACIÓN:", "verificar_logs", "migration")

    for categoria, info in resultados.items():
        status_icon = "✅" if info['status'] == 'EXISTE' and info['archivos'] else "❌"
        enviar_senal_log("INFO", f"{status_icon} {categoria}: {len(info['archivos'], "verificar_logs", "migration")} archivos de log")

    return resultados

if __name__ == "__main__":
    verificar_logs_sistema()
