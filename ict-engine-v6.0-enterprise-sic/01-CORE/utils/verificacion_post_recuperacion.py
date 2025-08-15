#!/usr/bin/env python3
"""
🔍 VERIFICACIÓN FINAL DEL SISTEMA ICT ENGINE v6.0
==================================================

Script de verificación completa después de la recuperación de archivos.
Valida que todos los componentes críticos estén funcionando.

Uso:
    python verificacion_post_recuperacion.py
"""

import sys
import os
from pathlib import Path
import importlib.util
from typing import Dict, List, Any
import json
from datetime import datetime

# Añadir path del proyecto
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

class SystemVerifier:
    """Verificador completo del sistema ICT Engine v6.1.0"""
    
    def __init__(self):
        """Inicializar verificador"""
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'modules': {},
            'imports': {},
            'critical_files': {},
            'system_status': 'UNKNOWN'
        }
        
    def verify_critical_modules(self) -> Dict[str, bool]:
        """Verificar módulos críticos del sistema"""
        critical_modules = [
            'core.data_management.advanced_candle_downloader',
            'core.data_management.mt5_data_manager', 
            'core.data_management.mt5_connection_manager',
            'core.analysis.pattern_detector',
            'core.analysis.market_structure_analyzer_v6',
            'core.analysis.poi_system',
            'core.smart_money_concepts.smart_money_analyzer',
            'utils.smart_trading_logger',
            'sistema.sic_v3_1.smart_import',
            'sistema.sic_v3_1.lazy_loading',
            'sistema.sic_v3_1.predictive_cache'
        ]
        
        results = {}
        for module in critical_modules:
            try:
                importlib.import_module(module)
                results[module] = True
                print(f"✅ {module}")
            except Exception as e:
                results[module] = False
                print(f"❌ {module}: {e}")
                
        self.results['modules'] = results
        return results
    
    def verify_external_dependencies(self) -> Dict[str, bool]:
        """Verificar dependencias externas"""
        dependencies = [
            'pandas',
            'numpy', 
            'MetaTrader5',
            'pytest',
            'matplotlib'
        ]
        
        results = {}
        for dep in dependencies:
            try:
                importlib.import_module(dep)
                results[dep] = True
                print(f"✅ {dep}")
            except ImportError:
                results[dep] = False
                print(f"⚠️ {dep} - No disponible")
                
        self.results['imports'] = results
        return results
    
    def verify_critical_files(self) -> Dict[str, bool]:
        """Verificar archivos críticos"""
        critical_files = [
            'main.py',
            'core/data_management/advanced_candle_downloader.py',
            'core/data_management/mt5_data_manager.py',
            'core/data_management/mt5_connection_manager.py',
            'core/analysis/pattern_detector.py',
            'core/analysis/market_structure_analyzer_v6.py',
            'core/smart_money_concepts/smart_money_analyzer.py',
            'utils/smart_trading_logger.py',
            'sistema/sic_v3_1/smart_import.py',
            'tests/test_final_system_validation_v6.py',
            'config/storage_config.json',
            'requirements.txt'
        ]
        
        results = {}
        for file_path in critical_files:
            path = PROJECT_ROOT / file_path
            exists = path.exists()
            results[file_path] = exists
            
            if exists:
                size = path.stat().st_size
                if size > 0:
                    print(f"✅ {file_path} ({size} bytes)")
                else:
                    print(f"⚠️ {file_path} (VACÍO)")
                    results[file_path] = False
            else:
                print(f"❌ {file_path} (FALTANTE)")
                
        self.results['critical_files'] = results
        return results
    
    def test_core_functionality(self) -> Dict[str, bool]:
        """Probar funcionalidad core básica"""
        tests = {}
        
        # Test 1: Smart Trading Logger
        try:
            from utils.smart_trading_logger import SmartTradingLogger
            logger = SmartTradingLogger()
            logger.info("Test de logging")
            tests['smart_logger'] = True
            print("✅ Smart Trading Logger")
        except Exception as e:
            tests['smart_logger'] = False
            print(f"❌ Smart Trading Logger: {e}")
        
        # Test 2: Pattern Detector
        try:
            from core.analysis.pattern_detector import PatternDetector
            detector = PatternDetector()
            tests['pattern_detector'] = True
            print("✅ Pattern Detector")
        except Exception as e:
            tests['pattern_detector'] = False
            print(f"❌ Pattern Detector: {e}")
        
        # Test 3: Smart Money Analyzer
        try:
            from core.smart_money_concepts.smart_money_analyzer import SmartMoneyAnalyzer
            analyzer = SmartMoneyAnalyzer()
            tests['smart_money'] = True
            print("✅ Smart Money Analyzer")
        except Exception as e:
            tests['smart_money'] = False
            print(f"❌ Smart Money Analyzer: {e}")
        
        # Test 4: Market Structure Analyzer
        try:
            from core.analysis.market_structure_analyzer import MarketStructureAnalyzer as MarketStructureAnalyzerV6
            ms_analyzer = MarketStructureAnalyzerV6()
            tests['market_structure'] = True
            print("✅ Market Structure Analyzer v6")
        except Exception as e:
            tests['market_structure'] = False
            print(f"❌ Market Structure Analyzer v6: {e}")
            
        self.results['functionality'] = tests
        return tests
    
    def determine_system_status(self) -> str:
        """Determinar estado general del sistema"""
        module_success = sum(self.results.get('modules', {}).values())
        file_success = sum(self.results.get('critical_files', {}).values())
        func_success = sum(self.results.get('functionality', {}).values())
        
        total_modules = len(self.results.get('modules', {}))
        total_files = len(self.results.get('critical_files', {}))
        total_funcs = len(self.results.get('functionality', {}))
        
        if module_success == total_modules and file_success == total_files and func_success == total_funcs:
            return "EXCELLENT"
        elif module_success >= total_modules * 0.9 and file_success >= total_files * 0.9:
            return "GOOD"
        elif module_success >= total_modules * 0.7 and file_success >= total_files * 0.7:
            return "WARNING"
        else:
            return "CRITICAL"
    
    def run_verification(self) -> Dict[str, Any]:
        """Ejecutar verificación completa"""
        print("🔍 VERIFICACIÓN FINAL DEL SISTEMA ICT ENGINE v6.0")
        print("=" * 60)
        
        print("\n📦 VERIFICANDO MÓDULOS CRÍTICOS...")
        self.verify_critical_modules()
        
        print("\n🔗 VERIFICANDO DEPENDENCIAS EXTERNAS...")
        self.verify_external_dependencies()
        
        print("\n📁 VERIFICANDO ARCHIVOS CRÍTICOS...")
        self.verify_critical_files()
        
        print("\n⚙️ PROBANDO FUNCIONALIDAD CORE...")
        self.test_core_functionality()
        
        # Determinar estado final
        self.results['system_status'] = self.determine_system_status()
        
        print(f"\n🎯 ESTADO FINAL DEL SISTEMA: {self.results['system_status']}")
        
        # Guardar reporte
        report_path = PROJECT_ROOT / 'verification_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Reporte guardado en: {report_path}")
        
        return self.results

def main():
    """Función principal"""
    verifier = SystemVerifier()
    results = verifier.run_verification()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    status = results['system_status']
    if status == "EXCELLENT":
        print("🟢 Sistema completamente operativo")
        print("🚀 Listo para producción")
    elif status == "GOOD":
        print("🟡 Sistema mayormente operativo")
        print("🔧 Requiere ajustes menores")
    elif status == "WARNING":
        print("🟠 Sistema parcialmente operativo")
        print("⚠️ Requiere atención")
    else:
        print("🔴 Sistema con problemas críticos")
        print("🚨 Requiere reparación inmediata")
    
    return 0 if status in ["EXCELLENT", "GOOD"] else 1

if __name__ == "__main__":
    sys.exit(main())
