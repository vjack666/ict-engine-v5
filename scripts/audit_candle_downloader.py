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

    print("🔍 === AUDITORÍA ADVANCED CANDLE DOWNLOADER ===")
    print()

    # 1. ANÁLISIS DE ESTRUCTURA DE ARCHIVO
    print("📁 1. ESTRUCTURA DE ARCHIVO:")
    print("-" * 40)

    downloader_path = Path("utils/advanced_candle_downloader.py")
    if not downloader_path.exists():
        print("❌ Error: Archivo no encontrado")
        return

    # Leer contenido del archivo
    with open(downloader_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    print(f"📊 Total líneas: {len(lines)}")
    print(f"📊 Tamaño archivo: {len(content)} caracteres")

    # 2. ANÁLISIS DE IMPORTS Y DEPENDENCIAS
    print("\n📦 2. IMPORTS Y DEPENDENCIAS:")
    print("-" * 40)

    imports = []
    for line in lines:
        line = line.strip()
        if line.startswith('import ') or line.startswith('from '):
            imports.append(line)

    print(f"📊 Total imports: {len(imports)}")
    for imp in imports[:10]:  # Mostrar primeros 10
        print(f"   • {imp}")
    if len(imports) > 10:
        print(f"   ... y {len(imports) - 10} más")

    # 3. ANÁLISIS DE CONFIGURACIONES
    print("\n⚙️ 3. CONFIGURACIONES DETECTADAS:")
    print("-" * 40)

    configs = []
    for i, line in enumerate(lines):
        if '_CONFIG' in line and '=' in line:
            configs.append((i+1, line.strip()))

    for line_num, config in configs:
        print(f"   Línea {line_num}: {config}")

    # 4. ANÁLISIS DE CLASES Y MÉTODOS
    print("\n🏗️ 4. CLASES Y MÉTODOS:")
    print("-" * 40)

    try:
        # Importar el módulo dinámicamente
        sys.path.insert(0, str(Path.cwd()))
        from utils.advanced_candle_downloader import AdvancedCandleDownloader

        # Analizar la clase principal
        class_methods = inspect.getmembers(AdvancedCandleDownloader, predicate=inspect.isfunction)

        print(f"📊 Clase principal: AdvancedCandleDownloader")
        print(f"📊 Total métodos: {len(class_methods)}")

        # Categorizar métodos
        public_methods = [name for name, _ in class_methods if not name.startswith('_')]
        private_methods = [name for name, _ in class_methods if name.startswith('_')]

        print(f"\n🔓 MÉTODOS PÚBLICOS ({len(public_methods)}):")
        for method in public_methods:
            print(f"   • {method}")

        print(f"\n🔒 MÉTODOS PRIVADOS ({len(private_methods)}):")
        for method in private_methods[:8]:  # Mostrar primeros 8
            print(f"   • {method}")
        if len(private_methods) > 8:
            print(f"   ... y {len(private_methods) - 8} más")

    except Exception as e:
        print(f"❌ Error analizando clases: {e}")

    # 5. ANÁLISIS DE FUNCIONES DE CONVENIENCIA
    print("\n🛠️ 5. FUNCIONES DE CONVENIENCIA:")
    print("-" * 40)

    try:
        import utils.advanced_candle_downloader as downloader_module

        # Obtener todas las funciones del módulo
        functions = inspect.getmembers(downloader_module, predicate=inspect.isfunction)
        module_functions = [name for name, _ in functions if not name.startswith('_')]

        print(f"📊 Total funciones del módulo: {len(module_functions)}")
        for func in module_functions:
            print(f"   • {func}")

    except Exception as e:
        print(f"❌ Error analizando funciones: {e}")

    # 6. ANÁLISIS DE CAPACIDADES DE DATOS
    print("\n📊 6. CAPACIDADES DE DATOS:")
    print("-" * 40)

    try:
        from utils.advanced_candle_downloader import DOWNLOAD_CONFIG, TIMEFRAME_MAPPING

        print("🎯 SÍMBOLOS SOPORTADOS:")
        for i, symbol in enumerate(DOWNLOAD_CONFIG["symbols"], 1):
            print(f"   {i}. {symbol}")

        print("\n⏰ TIMEFRAMES SOPORTADOS:")
        for tf, code in TIMEFRAME_MAPPING.items():
            print(f"   • {tf} (MT5: {code})")

        print(f"\n⚙️ CONFIGURACIÓN:")
        print(f"   • Velas por defecto: {DOWNLOAD_CONFIG['default_lookback']:,}")
        print(f"   • Chunk size: {DOWNLOAD_CONFIG['chunk_size']:,}")
        print(f"   • Descargas paralelas: {DOWNLOAD_CONFIG['parallel_downloads']}")
        print(f"   • Verificar integridad: {DOWNLOAD_CONFIG['verify_data_integrity']}")
        print(f"   • Backup automático: {DOWNLOAD_CONFIG['backup_existing_data']}")

    except Exception as e:
        print(f"❌ Error analizando configuraciones: {e}")

    # 7. ANÁLISIS DE INTEGRACIÓN ACTUAL
    print("\n🔗 7. INTEGRACIÓN ACTUAL:")
    print("-" * 40)

    integration_points = [
        "get_mt5_manager()",
        "enviar_senal_log()",
        "sistema.logging_interface",
        "utils.mt5_data_manager"
    ]

    for point in integration_points:
        if point in content:
            print(f"   ✅ {point} - CONECTADO")
        else:
            print(f"   ❌ {point} - NO ENCONTRADO")

    # 8. ANÁLISIS DE FORMATOS DE SALIDA
    print("\n💾 8. FORMATOS DE SALIDA:")
    print("-" * 40)

    output_formats = []
    if "save_data_to_csv" in content:
        output_formats.append("CSV")
    if "json.dump" in content:
        output_formats.append("JSON")
    if "to_csv" in content:
        output_formats.append("Pandas CSV")

    for fmt in output_formats:
        print(f"   ✅ {fmt}")

    # 9. RECOMENDACIONES PARA INTEGRACIÓN
    print("\n💡 9. RECOMENDACIONES PARA INTEGRACIÓN:")
    print("-" * 40)

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
        print(f"   {i}. {rec}")

    print("\n🎯 PRÓXIMOS PASOS RECOMENDADOS:")
    print("-" * 40)
    print("1. Crear CandleCoordinator que use AdvancedCandleDownloader")
    print("2. Implementar sistema de callbacks para tiempo real")
    print("3. Integrar con dashboard usando download_multiple()")
    print("4. Aprovechar validación y backup existentes")
    print("5. Usar DownloadStats para métricas de rendimiento")

if __name__ == "__main__":
    analyze_advanced_candle_downloader()
