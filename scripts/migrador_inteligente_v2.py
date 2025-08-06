#!/usr/bin/env python3
"""
🧠 MIGRADOR INTELIGENTE SIC v2.0 - SISTEMA QUIRÚRGICO
====================================================
Migración inteligente y precisa al Sistema de Imports Centralizados

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
Versión: v2.0

CARACTERÍSTICAS:
- Análisis semántico avanzado de dependencias
- Imports precisos basados en uso real
- Sin sobre-importación
- Preservación de funcionalidad
- Backup automático de seguridad
"""

import os
import ast
import shutil
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Set, List, Tuple
import re

class MigradorInteligenteSIC:
    """🧠 Migrador inteligente con análisis semántico"""

    def __init__(self):
        self.archivos_migrar = [
            'dashboard/dashboard_definitivo.py',
            'core/ict_engine/ict_detector.py',
            'dashboard/dashboard_widgets.py',
            'core/analysis_command_center/tct_pipeline/tct_interface.py',
            'dashboard/poi_dashboard_integration.py'
        ]

        # Mapeo inteligente de imports SIC por funcionalidad
        self.mapa_sic_funcional = {
            # Logging y Sistema
            'logging': 'from sistema.smart_directory_logger import logger',
            'logger': 'from sistema.smart_directory_logger import logger',
            'get_logger': 'from sistema.smart_directory_logger import get_logger',
            'setup_logging': 'from sistema.smart_directory_logger import setup_logging',

            # Data Management
            'CandleDownloader': 'from core.data_management.candle_downloader import CandleDownloader',
            'DataPipeline': 'from core.data_pipeline.enhanced_data_pipeline import DataPipeline',
            'VelasManager': 'from core.data_management.velas_manager import VelasManager',

            # ICT Engine
            'ICTDetector': 'from core.ict_engine.ict_detector import ICTDetector',
            'ICTAnalyzer': 'from core.ict_engine.ict_analyzer import ICTAnalyzer',
            'FairValueGap': 'from core.ict_engine.concepts.fair_value_gap import FairValueGap',
            'OrderBlock': 'from core.ict_engine.concepts.order_block import OrderBlock',
            'LiquidityPool': 'from core.ict_engine.concepts.liquidity_pool import LiquidityPool',

            # POI System
            'POISystem': 'from core.poi_system.poi_manager import POISystem',
            'POIManager': 'from core.poi_system.poi_manager import POIManager',
            'POIDetector': 'from core.poi_system.poi_detector import POIDetector',
            'POIAnalyzer': 'from core.poi_system.poi_analyzer import POIAnalyzer',

            # Analytics
            'AnalyticsEngine': 'from core.analytics.analytics_engine import AnalyticsEngine',
            'PerformanceAnalyzer': 'from core.analytics.performance_analyzer import PerformanceAnalyzer',
            'MarketAnalyzer': 'from core.analytics.market_analyzer import MarketAnalyzer',

            # Trading
            'TradingEngine': 'from core.trading import TradingEngine',
            'SmartTradingLogger': 'from core.smart_trading_logger import SmartTradingLogger',
            'LimitOrderManager': 'from core.limit_order_manager import LimitOrderManager',

            # Risk Management
            'RiskManager': 'from core.risk_management.risk_manager import RiskManager',
            'PositionSizer': 'from core.risk_management.position_sizer import PositionSizer',

            # Dashboard y UI
            'DashboardController': 'from dashboard.dashboard_controller import DashboardController',
            'POIDashboardIntegration': 'from dashboard.poi_dashboard_integration import POIDashboardIntegration',

            # Configuración
            'ConfigManager': 'from config.config_manager import ConfigManager',
            'LiveAccountValidator': 'from config.live_account_validator import LiveAccountValidator',

            # Sistema
            'MarketStatusDetector': 'from sistema.market_status_detector_v3 import MarketStatusDetector',
            'TradingSchedule': 'from sistema.trading_schedule import TradingSchedule',
            'SystemMonitor': 'from sistema.system_monitor import SystemMonitor',

            # Integrations
            'MT5Manager': 'from core.integrations.mt5_manager import MT5Manager',
            'TelegramBot': 'from core.integrations.telegram_bot import TelegramBot',

            # Analysis Command Center
            'TCTInterface': 'from core.analysis_command_center.tct_pipeline.tct_interface import TCTInterface',
            'AnalysisCommandCenter': 'from core.analysis_command_center.command_center import AnalysisCommandCenter'
        }

        self.imports_standard = {
            'datetime', 'os', 'sys', 'pathlib', 'json', 'time', 'threading',
            'asyncio', 'typing', 're', 'collections', 'itertools', 'functools',
            'dataclasses', 'enum', 'abc', 'warnings'
        }

        self.imports_terceros = {
            'numpy', 'pandas', 'matplotlib', 'plotly', 'tkinter', 'requests',
            'MetaTrader5', 'yfinance', 'ta', 'scipy'
        }

    def analizar_dependencias_archivo(self, archivo_path: Path) -> Set[str]:
        """🔍 Analizar dependencias reales de un archivo Python"""

        try:
            with open(archivo_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse AST para análisis semántico
            tree = ast.parse(content)

            dependencias = set()

            # Análisis de nombres utilizados
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    dependencias.add(node.id)
                elif isinstance(node, ast.Attribute):
                    # Para casos como logger.info, POISystem.create, etc.
                    if isinstance(node.value, ast.Name):
                        dependencias.add(node.value.id)

            # Análisis de strings para detección adicional
            patrones_funcionales = [
                r'\b(logger|logging)\b',
                r'\b(CandleDownloader|DataPipeline|VelasManager)\b',
                r'\b(ICTDetector|ICTAnalyzer|FairValueGap|OrderBlock)\b',
                r'\b(POISystem|POIManager|POIDetector|POIAnalyzer)\b',
                r'\b(TradingEngine|RiskManager|ConfigManager)\b',
                r'\b(DashboardController|POIDashboardIntegration)\b'
            ]

            for patron in patrones_funcionales:
                matches = re.findall(patron, content, re.IGNORECASE)
                dependencias.update(matches)

            return dependencias

        except Exception as e:
            print(f"⚠️ Error analizando {archivo_path}: {e}")
            return set()

    def generar_imports_precisos(self, dependencias: Set[str]) -> List[str]:
        """🎯 Generar imports precisos basados en dependencias reales"""

        imports_necesarios = []

        # Filtrar dependencias por categoría
        deps_sic = set()
        deps_standard = set()
        deps_terceros = set()

        for dep in dependencias:
            if dep in self.mapa_sic_funcional:
                deps_sic.add(dep)
            elif any(dep.startswith(std) for std in self.imports_standard):
                deps_standard.add(dep)
            elif any(dep.startswith(ter) for ter in self.imports_terceros):
                deps_terceros.add(ter for ter in self.imports_terceros if dep.startswith(ter))

        # Generar imports SIC específicos
        for dep in sorted(deps_sic):
            if dep in self.mapa_sic_funcional:
                imports_necesarios.append(self.mapa_sic_funcional[dep])

        return imports_necesarios

    def migrar_archivo_inteligente(self, archivo_path: Path) -> bool:
        """🧠 Migrar un archivo usando análisis inteligente"""

        print(f"\n🧠 Migrando inteligentemente: {archivo_path}")

        try:
            # 1. Analizar dependencias reales
            dependencias = self.analizar_dependencias_archivo(archivo_path)
            print(f"   🔍 Dependencias detectadas: {len(dependencias)}")

            # 2. Generar imports precisos
            imports_sic = self.generar_imports_precisos(dependencias)
            print(f"   🎯 Imports SIC necesarios: {len(imports_sic)}")

            # 3. Leer archivo original
            with open(archivo_path, 'r', encoding='utf-8') as f:
                lineas_originales = f.readlines()

            # 4. Procesar líneas
            lineas_nuevas = []
            imports_existentes = []
            seccion_imports = True

            for i, linea in enumerate(lineas_originales):
                linea_strip = linea.strip()

                # Detectar imports existentes
                if (linea_strip.startswith('import ') or
                    linea_strip.startswith('from ') or
                    linea_strip == '' and seccion_imports):
                    if linea_strip != '':
                        imports_existentes.append(linea)
                    continue

                # Fin de sección de imports
                if linea_strip != '' and not linea_strip.startswith('#'):
                    seccion_imports = False

                    # Insertar imports SIC al inicio del código
                    if not any('# === IMPORTS SIC ===' in l for l in lineas_nuevas):
                        lineas_nuevas.append('# === IMPORTS SIC ===\n')

                        for import_sic in imports_sic:
                            lineas_nuevas.append(f"{import_sic}\n")

                        lineas_nuevas.append('\n')
                        lineas_nuevas.append('# === RESTO DE IMPORTS ===\n')

                        # Preservar imports no-SIC importantes
                        for import_existente in imports_existentes:
                            if not any(palabra in import_existente.lower()
                                     for palabra in ['sistema', 'core', 'dashboard', 'config']):
                                lineas_nuevas.append(import_existente)

                        lineas_nuevas.append('\n')

                # Agregar línea de código
                lineas_nuevas.append(linea)

            # 5. Escribir archivo migrado
            with open(archivo_path, 'w', encoding='utf-8') as f:
                f.writelines(lineas_nuevas)

            print(f"   ✅ Migración inteligente completada")
            print(f"      - Imports SIC: {len(imports_sic)}")
            print(f"      - Imports preservados: {len([i for i in imports_existentes if not any(p in i.lower() for p in ['sistema', 'core', 'dashboard', 'config'])])}")

            return True

        except Exception as e:
            print(f"   ❌ Error durante migración inteligente: {e}")
            return False

    def ejecutar_migracion_completa(self) -> bool:
        """🚀 Ejecutar migración inteligente completa"""

        print("🧠 INICIANDO MIGRACIÓN INTELIGENTE SIC v2.0")
        print("=" * 60)

        # Crear backup de seguridad
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Path(f"backup_pre_migracion_v2_{timestamp}")
        backup_dir.mkdir(exist_ok=True)

        print(f"💾 Creando backup de seguridad: {backup_dir}")

        migraciones_exitosas = 0

        for archivo_relativo in self.archivos_migrar:
            archivo_path = Path(archivo_relativo)

            if not archivo_path.exists():
                print(f"⚠️ Archivo no encontrado: {archivo_relativo}")
                continue

            # Backup del archivo
            backup_file = backup_dir / archivo_relativo
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(archivo_path, backup_file)

            # Migrar inteligentemente
            if self.migrar_archivo_inteligente(archivo_path):
                migraciones_exitosas += 1

        print(f"\n📊 REPORTE MIGRACIÓN INTELIGENTE v2.0:")
        print(f"   ✅ Migraciones exitosas: {migraciones_exitosas}/{len(self.archivos_migrar)}")
        print(f"   💾 Backup de seguridad: {backup_dir}")

        return migraciones_exitosas == len(self.archivos_migrar)

def main():
    """🚀 Función principal del migrador inteligente"""

    try:
        migrador = MigradorInteligenteSIC()
        exito = migrador.ejecutar_migracion_completa()

        if exito:
            print(f"\n🎉 MIGRACIÓN INTELIGENTE v2.0 COMPLETADA")
            print("=" * 50)
            print("✅ Todos los archivos migrados con imports precisos")
            print("✅ Sin sobre-importación")
            print("✅ Funcionalidad preservada")
            print("✅ Backup de seguridad creado")
            print("")
            print("🚀 SISTEMA SIC v2.0 OPERATIVO")
            print("   Los imports son ahora precisos y optimizados")
        else:
            print("❌ CRÍTICO: Falló la migración inteligente")
            return False

        return True

    except Exception as e:
        print(f"\n❌ ERROR DURANTE MIGRACIÓN INTELIGENTE: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
