from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
"""
🔍 AUDITORÍA COMPLETA - ADVANCED CANDLE DOWNLOADER
===============================================

Script que analiza la estructura, dependencias, métodos y capacidades
del Advanced Candle Downloader para planificar la integración completa.

Fecha: 02 Agosto 2025
Objetivo: Preparación para integración con dashboard y sistemas
"""

import sys
import inspect
import importlib.util
from pathlib import Path
from typing import Dict, List, Any
import ast

def analyze_advanced_candle_downloader():
    """Análisis completo del Advanced Candle Downloader"""

    enviar_senal_log("INFO", "🔍 === AUDITORÍA ADVANCED CANDLE DOWNLOADER ===", "audit_candle_downloader", "migration")
    enviar_senal_log("INFO", , "audit_candle_downloader", "migration")

    # 1. ANÁLISIS DE ESTRUCTURA DE ARCHIVO
    enviar_senal_log("INFO", "📁 1. ESTRUCTURA DE ARCHIVO:", "audit_candle_downloader", "migration")
    enviar_senal_log("INFO", "-" * 40, "audit_candle_downloader", "migration")

    downloader_path = Path("utils/advanced_candle_downloader.py")
    if not downloader_path.exists():
        enviar_senal_log("ERROR", "❌ Error: Archivo no encontrado", "audit_candle_downloader", "migration")
        return

    # Leer contenido del archivo
    with open(downloader_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    enviar_senal_log("INFO", f"📊 Total líneas: {len(lines, "audit_candle_downloader", "migration")}")
    enviar_senal_log("INFO", f"📊 Tamaño archivo: {len(content, "audit_candle_downloader", "migration")} caracteres")

    # 2. ANÁLISIS DE IMPORTS Y DEPENDENCIAS
    enviar_senal_log("INFO", "\n📦 2. IMPORTS Y DEPENDENCIAS:", "audit_candle_downloader", "migration")
    enviar_senal_log("INFO", "-" * 40, "audit_candle_downloader", "migration")

    imports = []
    for line in lines:
        line = line.strip()
        if line.startswith('import ') or line.startswith('from '):
            imports.append(line)

    enviar_senal_log("INFO", f"📊 Total imports: {len(imports, "audit_candle_downloader", "migration")}")
    for imp in imports[:10]:  # Mostrar primeros 10
        enviar_senal_log("INFO", f"   • {imp}", "audit_candle_downloader", "migration")
    if len(imports) > 10:
        enviar_senal_log("INFO", f"   ... y {len(imports, "audit_candle_downloader", "migration") - 10} más")

    # 3. ANÁLISIS DE CONFIGURACIONES
    enviar_senal_log("INFO", "\n⚙️ 3. CONFIGURACIONES DETECTADAS:", "audit_candle_downloader", "migration")
    enviar_senal_log("INFO", "-" * 40, "audit_candle_downloader", "migration")

    configs = []
    for i, line in enumerate(lines):
        if '_CONFIG' in line and '=' in line:
            configs.append((i+1, line.strip()))

    for line_num, config in configs:
        enviar_senal_log("INFO", f"   Línea {line_num}: {config}", "audit_candle_downloader", "migration")

    # 4. ANÁLISIS DE CLASES Y MÉTODOS
    enviar_senal_log("INFO", "\n🏗️ 4. CLASES Y MÉTODOS:", "audit_candle_downloader", "migration")
    enviar_senal_log("INFO", "-" * 40, "audit_candle_downloader", "migration")

    try:
        # Importar el módulo dinámicamente
        sys.path.insert(0, str(Path.cwd()))
        from utils.advanced_candle_downloader import AdvancedCandleDownloader

        # Analizar la clase principal
        class_methods = inspect.getmembers(AdvancedCandleDownloader, predicate=inspect.isfunction)

        enviar_senal_log("INFO", f"📊 Clase principal: AdvancedCandleDownloader", "audit_candle_downloader", "migration")
        enviar_senal_log("INFO", f"📊 Total métodos: {len(class_methods, "audit_candle_downloader", "migration")}")

        # Categorizar métodos
        public_methods = [name for name, _ in class_methods if not name.startswith('_')]
        private_methods = [name for name, _ in class_methods if name.startswith('_')]

        enviar_senal_log("INFO", f"\n🔓 MÉTODOS PÚBLICOS ({len(public_methods, "audit_candle_downloader", "migration")}):")
        for method in public_methods:
            enviar_senal_log("INFO", f"   • {method}", "audit_candle_downloader", "migration")

        enviar_senal_log("INFO", f"\n🔒 MÉTODOS PRIVADOS ({len(private_methods, "audit_candle_downloader", "migration")}):")
        for method in private_methods[:8]:  # Mostrar primeros 8
            enviar_senal_log("INFO", f"   • {method}", "audit_candle_downloader", "migration")
        if len(private_methods) > 8:
            enviar_senal_log("INFO", f"   ... y {len(private_methods, "audit_candle_downloader", "migration") - 8} más")

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error analizando clases: {e}", "audit_candle_downloader", "migration")

    # 5. ANÁLISIS DE FUNCIONES DE CONVENIENCIA
    enviar_senal_log("INFO", "\n🛠️ 5. FUNCIONES DE CONVENIENCIA:", "audit_candle_downloader", "migration")
    enviar_senal_log("INFO", "-" * 40, "audit_candle_downloader", "migration")

    try:
        import utils.advanced_candle_downloader as downloader_module

        # Obtener todas las funciones del módulo
        functions = inspect.getmembers(downloader_module, predicate=inspect.isfunction)
        module_functions = [name for name, _ in functions if not name.startswith('_')]

        enviar_senal_log("INFO", f"📊 Total funciones del módulo: {len(module_functions, "audit_candle_downloader", "migration")}")
        for func in module_functions:
            enviar_senal_log("INFO", f"   • {func}", "audit_candle_downloader", "migration")

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error analizando funciones: {e}", "audit_candle_downloader", "migration")

    # 6. ANÁLISIS DE CAPACIDADES DE DATOS
    enviar_senal_log("INFO", "\n📊 6. CAPACIDADES DE DATOS:", "audit_candle_downloader", "migration")
    enviar_senal_log("INFO", "-" * 40, "audit_candle_downloader", "migration")

    try:
        from utils.advanced_candle_downloader import DOWNLOAD_CONFIG, TIMEFRAME_MAPPING

        enviar_senal_log("INFO", "🎯 SÍMBOLOS SOPORTADOS:", "audit_candle_downloader", "migration")
        for i, symbol in enumerate(DOWNLOAD_CONFIG["symbols"], 1):
            enviar_senal_log("INFO", f"   {i}. {symbol}", "audit_candle_downloader", "migration")

        enviar_senal_log("INFO", "\n⏰ TIMEFRAMES SOPORTADOS:", "audit_candle_downloader", "migration")
        for tf, code in TIMEFRAME_MAPPING.items():
            enviar_senal_log("INFO", f"   • {tf} (MT5: {code}, "audit_candle_downloader", "migration")")

        enviar_senal_log("INFO", f"\n⚙️ CONFIGURACIÓN:", "audit_candle_downloader", "migration")
        enviar_senal_log("INFO", f"   • Velas por defecto: {DOWNLOAD_CONFIG['default_lookback']:,}", "audit_candle_downloader", "migration")
        enviar_senal_log("INFO", f"   • Chunk size: {DOWNLOAD_CONFIG['chunk_size']:,}", "audit_candle_downloader", "migration")
        enviar_senal_log("INFO", f"   • Descargas paralelas: {DOWNLOAD_CONFIG['parallel_downloads']}", "audit_candle_downloader", "migration")
        enviar_senal_log("INFO", f"   • Verificar integridad: {DOWNLOAD_CONFIG['verify_data_integrity']}", "audit_candle_downloader", "migration")
        enviar_senal_log("INFO", f"   • Backup automático: {DOWNLOAD_CONFIG['backup_existing_data']}", "audit_candle_downloader", "migration")

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error analizando configuraciones: {e}", "audit_candle_downloader", "migration")

    # 7. ANÁLISIS DE INTEGRACIÓN ACTUAL
    enviar_senal_log("INFO", "\n🔗 7. INTEGRACIÓN ACTUAL:", "audit_candle_downloader", "migration")
    enviar_senal_log("INFO", "-" * 40, "audit_candle_downloader", "migration")

    integration_points = [
        "get_mt5_manager()",
        "enviar_senal_log()",
        "sistema.logging_interface",
        "utils.mt5_data_manager"
    ]

    for point in integration_points:
        if point in content:
            enviar_senal_log("INFO", f"   ✅ {point} - CONECTADO", "audit_candle_downloader", "migration")
        else:
            enviar_senal_log("INFO", f"   ❌ {point} - NO ENCONTRADO", "audit_candle_downloader", "migration")

    # 8. ANÁLISIS DE FORMATOS DE SALIDA
    enviar_senal_log("INFO", "\n💾 8. FORMATOS DE SALIDA:", "audit_candle_downloader", "migration")
    enviar_senal_log("INFO", "-" * 40, "audit_candle_downloader", "migration")

    output_formats = []
    if "save_data_to_csv" in content:
        output_formats.append("CSV")
    if "json.dump" in content:
        output_formats.append("JSON")
    if "to_csv" in content:
        output_formats.append("Pandas CSV")

    for fmt in output_formats:
        enviar_senal_log("INFO", f"   ✅ {fmt}", "audit_candle_downloader", "migration")

    # 9. RECOMENDACIONES PARA INTEGRACIÓN
    enviar_senal_log("INFO", "\n💡 9. RECOMENDACIONES PARA INTEGRACIÓN:", "audit_candle_downloader", "migration")
    enviar_senal_log("INFO", "-" * 40, "audit_candle_downloader", "migration")

    recommendations = [
        "Usar download_multiple() para descarga optimizada",
        "Aprovechar validación de integridad (_validate_data_integrity)",
        "Utilizar sistema de backup automático",
        "Implementar callbacks en descargas paralelas",
        "Usar DownloadStats para monitoreo en tiempo real",
        "Aprovechar formato CSV existente para distribución",
        "Integrar con sistema de logging SLUC v2.1 existente"
    ]

    for i, rec in enumerate(recommendations, 1):
        enviar_senal_log("INFO", f"   {i}. {rec}", "audit_candle_downloader", "migration")

    enviar_senal_log("INFO", "\n🎯 PRÓXIMOS PASOS RECOMENDADOS:", "audit_candle_downloader", "migration")
    enviar_senal_log("INFO", "-" * 40, "audit_candle_downloader", "migration")
    enviar_senal_log("INFO", "1. Crear CandleCoordinator que use AdvancedCandleDownloader", "audit_candle_downloader", "migration")
    enviar_senal_log("INFO", "2. Implementar sistema de callbacks para tiempo real", "audit_candle_downloader", "migration")
    enviar_senal_log("INFO", "3. Integrar con dashboard usando download_multiple(, "audit_candle_downloader", "migration")")
    enviar_senal_log("INFO", "4. Aprovechar validación y backup existentes", "audit_candle_downloader", "migration")
    enviar_senal_log("INFO", "5. Usar DownloadStats para métricas de rendimiento", "audit_candle_downloader", "migration")

if __name__ == "__main__":
    analyze_advanced_candle_downloader()
