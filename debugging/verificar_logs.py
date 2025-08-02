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

    print("🔍 VERIFICANDO LOGS DEL SISTEMA POI/ICT...")
    print("=" * 60)

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
        print(f"\n📂 {categoria} LOGS ({path}):")

        if not os.path.exists(path):
            print(f"   ❌ Directorio no existe: {path}")
            resultados[categoria] = {'status': 'NO_EXISTE', 'archivos': []}
            continue

        archivos = [f for f in os.listdir(path) if f.endswith('.log')]
        resultados[categoria] = {'status': 'EXISTE', 'archivos': archivos}

        if not archivos:
            print(f"   ⚠️  Directorio vacío - sin archivos .log")
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

                    print(f"   ✅ {archivo}")
                    print(f"      └─ Tamaño: {tamaño} bytes | Líneas: {total_lines}")
                    print(f"      └─ Modificado: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"      └─ Logs hoy: {len(logs_hoy)} | Logs POI: {len(logs_poi)}")

                    # Si hay logs POI, mostrar algunos ejemplos
                    if logs_poi:
                        print(f"      📊 EJEMPLOS DE LOGS POI/DASHBOARD:")
                        for i, log_line in enumerate(logs_poi[-3:], 1):  # Últimos 3
                            print(f"         {i}. {log_line.strip()[:80]}...")

                except Exception as e:
                    print(f"   ❌ Error leyendo {archivo}: {e}")

    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN:")

    for categoria, info in resultados.items():
        status_icon = "✅" if info['status'] == 'EXISTE' and info['archivos'] else "❌"
        print(f"{status_icon} {categoria}: {len(info['archivos'])} archivos de log")

    return resultados

if __name__ == "__main__":
    verificar_logs_sistema()
