#!/usr/bin/env python3
"""
🎯 FASE 1: AÑADIR - ESCÁNER DE IMPORTS COMUNES
============================================
Escanea todo el proyecto para identificar imports más utilizados
Implementa la primera fase de la estrategia "AÑADIR → REEMPLAZAR → ELIMINAR"

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
Versión: v1.0
"""

import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime
import json

class ImportScanner:
    """🔍 Escáner inteligente de imports en el proyecto"""
    
    def __init__(self):
        self.import_stats = Counter()
        self.file_stats = defaultdict(list)
        self.pattern_stats = defaultdict(int)
        self.project_imports = defaultdict(int)
        self.standard_imports = defaultdict(int)
        self.files_scanned = 0
        
        # Patrones de imports a buscar
        self.import_patterns = [
            # Standard Library - Typing
            r'^(\s*)from typing import (.+)$',
            r'^(\s*)import typing$',
            
            # Standard Library - Básicos
            r'^(\s*)import (os|sys|json|time|re|math)$',
            r'^(\s*)from (datetime|pathlib|dataclasses|collections|itertools) import (.+)$',
            r'^(\s*)import (datetime|pathlib|dataclasses|collections|itertools)$',
            
            # Project imports - Core
            r'^(\s*)from core\.([a-zA-Z_]+) import (.+)$',
            r'^(\s*)from core\.([a-zA-Z_]+)\.([a-zA-Z_]+) import (.+)$',
            
            # Project imports - Dashboard  
            r'^(\s*)from dashboard\.([a-zA-Z_]+) import (.+)$',
            
            # Project imports - Sistema
            r'^(\s*)from sistema\.([a-zA-Z_]+) import (.+)$',
            
            # Project imports - Utils
            r'^(\s*)from utils\.([a-zA-Z_]+) import (.+)$',
            
            # Third party - Common
            r'^(\s*)import (pandas|numpy|matplotlib|plotly)$',
            r'^(\s*)from (pandas|numpy|matplotlib|plotly) import (.+)$',
        ]
        
        # Directorios a excluir
        self.exclude_dirs = {
            '__pycache__', '.git', '.vscode', 'node_modules',
            'backup_sic_migration', 'backup_pre_restauracion_directa_20250806_113634',
            'backup_pre_migracion_v2_20250806_113857', 'migration_reports',
            'debug_screenshots'
        }
        
        # Archivos a excluir
        self.exclude_files = {
            'sic.py', 'imports_interface.py', '__init__.py'
        }

    def scan_file(self, file_path: Path) -> dict:
        """🔍 Escanear un archivo individual para imports"""
        
        result = {
            'file': str(file_path),
            'imports_found': [],
            'import_count': 0,
            'standard_lib': [],
            'project_imports': [],
            'third_party': [],
            'typing_imports': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                if not line or line.startswith('#'):
                    continue
                
                # Detectar imports con patrones
                for pattern in self.import_patterns:
                    match = re.match(pattern, line)
                    if match:
                        import_info = {
                            'line': line,
                            'line_number': line_num,
                            'pattern': pattern,
                            'groups': match.groups()
                        }
                        
                        result['imports_found'].append(import_info)
                        result['import_count'] += 1
                        
                        # Categorizar import
                        self._categorize_import(line, result)
                        
                        # Actualizar estadísticas globales
                        self.import_stats[line] += 1
                        self.file_stats[str(file_path)].append(line)
                        
                        break
            
            return result
            
        except Exception as e:
            result['error'] = str(e)
            return result

    def _categorize_import(self, import_line: str, result: dict):
        """📊 Categorizar tipo de import"""
        
        # Standard library
        std_lib_patterns = [
            'import os', 'import sys', 'import json', 'import time', 'import re', 'import math',
            'from datetime', 'from pathlib', 'from dataclasses', 'from collections', 'from itertools'
        ]
        
        # Typing específico
        if 'from typing import' in import_line or 'import typing' in import_line:
            result['typing_imports'].append(import_line)
            self.standard_imports['typing'] += 1
        
        # Standard library
        elif any(pattern in import_line for pattern in std_lib_patterns):
            result['standard_lib'].append(import_line)
            
            for pattern in std_lib_patterns:
                if pattern in import_line:
                    module = pattern.split()[-1] if 'import' in pattern else pattern.split('from ')[1]
                    self.standard_imports[module] += 1
                    break
        
        # Project imports
        elif any(prefix in import_line for prefix in ['from core.', 'from dashboard.', 'from sistema.', 'from utils.']):
            result['project_imports'].append(import_line)
            
            # Detectar módulo específico
            if 'from core.' in import_line:
                module = import_line.split('from core.')[1].split()[0]
                self.project_imports[f'core.{module}'] += 1
            elif 'from dashboard.' in import_line:
                module = import_line.split('from dashboard.')[1].split()[0]
                self.project_imports[f'dashboard.{module}'] += 1
            elif 'from sistema.' in import_line:
                module = import_line.split('from sistema.')[1].split()[0]
                self.project_imports[f'sistema.{module}'] += 1
            elif 'from utils.' in import_line:
                module = import_line.split('from utils.')[1].split()[0]
                self.project_imports[f'utils.{module}'] += 1
        
        # Third party
        else:
            third_party_libs = ['pandas', 'numpy', 'matplotlib', 'plotly', 'requests', 'MetaTrader5']
            if any(lib in import_line for lib in third_party_libs):
                result['third_party'].append(import_line)

    def scan_project(self) -> dict:
        """🎯 Escanear todo el proyecto"""
        
        print("🔍 INICIANDO ESCANEO MASIVO DE IMPORTS")
        print("=" * 50)
        
        project_root = Path('.')
        scan_results = {
            'files_scanned': 0,
            'files_with_imports': 0,
            'total_imports_found': 0,
            'scan_timestamp': datetime.now().isoformat(),
            'file_results': {},
            'summary': {}
        }
        
        # Escanear recursivamente
        for file_path in project_root.rglob('*.py'):
            # Filtrar archivos/directorios excluidos
            if any(exclude_dir in str(file_path) for exclude_dir in self.exclude_dirs):
                continue
                
            if file_path.name in self.exclude_files:
                continue
            
            print(f"📄 Escaneando: {file_path}")
            
            result = self.scan_file(file_path)
            scan_results['file_results'][str(file_path)] = result
            
            self.files_scanned += 1
            scan_results['files_scanned'] += 1
            
            if result['import_count'] > 0:
                scan_results['files_with_imports'] += 1
                scan_results['total_imports_found'] += result['import_count']
        
        # Generar resumen
        scan_results['summary'] = self._generate_summary()
        
        return scan_results

    def _generate_summary(self) -> dict:
        """📊 Generar resumen de resultados"""
        
        summary = {
            'top_imports': dict(self.import_stats.most_common(20)),
            'top_standard_imports': dict(sorted(self.standard_imports.items(), key=lambda x: x[1], reverse=True)[:10]),
            'top_project_imports': dict(sorted(self.project_imports.items(), key=lambda x: x[1], reverse=True)[:10]),
            'files_scanned': self.files_scanned,
            'unique_imports': len(self.import_stats),
            'total_import_occurrences': sum(self.import_stats.values())
        }
        
        return summary

    def generate_expansion_recommendations(self, scan_results: dict) -> dict:
        """🎯 Generar recomendaciones para expansión del SIC"""
        
        recommendations = {
            'high_priority': [],      # 15+ archivos
            'medium_priority': [],    # 8-14 archivos  
            'low_priority': [],       # 3-7 archivos
            'standard_library': [],
            'project_modules': [],
            'expansion_targets': {}
        }
        
        # Analizar frecuencia de imports
        for import_line, count in self.import_stats.most_common(50):
            if count >= 15:
                recommendations['high_priority'].append({
                    'import': import_line,
                    'count': count,
                    'priority': 'HIGH'
                })
            elif count >= 8:
                recommendations['medium_priority'].append({
                    'import': import_line,
                    'count': count,
                    'priority': 'MEDIUM'
                })
            elif count >= 3:
                recommendations['low_priority'].append({
                    'import': import_line,
                    'count': count,
                    'priority': 'LOW'
                })
        
        # Standard library recommendations
        for module, count in self.standard_imports.items():
            if count >= 5:
                recommendations['standard_library'].append({
                    'module': module,
                    'count': count
                })
        
        # Project modules recommendations
        for module, count in self.project_imports.items():
            if count >= 3:
                recommendations['project_modules'].append({
                    'module': module,
                    'count': count
                })
        
        # Targets específicos para expansión
        recommendations['expansion_targets'] = {
            'typing_components': ['Dict', 'List', 'Optional', 'Any', 'Tuple', 'Union', 'TYPE_CHECKING'],
            'datetime_components': ['datetime', 'timedelta', 'timezone'],
            'dataclass_components': ['dataclass', 'field', 'asdict'],
            'pathlib_components': ['Path'],
            'core_ict_components': ['ICTDetector', 'ICTAnalyzer', 'FairValueGap', 'OrderBlock'],
            'core_poi_components': ['POISystem', 'POIDetector', 'POIAnalyzer'],
            'dashboard_components': ['DashboardController', 'SentinelDashboard'],
            'sistema_components': ['logger', 'enviar_senal_log', 'MarketStatusDetector']
        }
        
        return recommendations

def main():
    """🚀 Función principal de escaneo"""
    
    print("🎯 FASE 1: AÑADIR - ESCÁNER DE IMPORTS COMUNES")
    print("=" * 60)
    
    try:
        # Inicializar escáner
        scanner = ImportScanner()
        
        # Escanear proyecto
        results = scanner.scan_project()
        
        # Generar recomendaciones
        recommendations = scanner.generate_expansion_recommendations(results)
        
        # Mostrar resultados
        print(f"\n📊 RESULTADOS DEL ESCANEO:")
        print(f"   📁 Archivos escaneados: {results['files_scanned']}")
        print(f"   📋 Archivos con imports: {results['files_with_imports']}")
        print(f"   🎯 Total imports encontrados: {results['total_imports_found']}")
        print(f"   🔍 Imports únicos: {results['summary']['unique_imports']}")
        
        print(f"\n🏆 TOP 10 IMPORTS MÁS COMUNES:")
        for i, (import_line, count) in enumerate(list(results['summary']['top_imports'].items())[:10], 1):
            print(f"   {i:2d}. {import_line[:60]:<60} ({count} archivos)")
        
        print(f"\n🎯 RECOMENDACIONES DE EXPANSIÓN:")
        print(f"   🔥 Alta prioridad (15+ archivos): {len(recommendations['high_priority'])}")
        print(f"   🔶 Media prioridad (8-14 archivos): {len(recommendations['medium_priority'])}")
        print(f"   🔸 Baja prioridad (3-7 archivos): {len(recommendations['low_priority'])}")
        
        print(f"\n📦 COMPONENTES PARA EXPANSIÓN:")
        for category, components in recommendations['expansion_targets'].items():
            print(f"   📋 {category}: {', '.join(components[:5])}")
        
        # Guardar resultados
        output_file = 'migration_reports/fase1_scan_results.json'
        os.makedirs('migration_reports', exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'scan_results': results,
                'recommendations': recommendations
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultados guardados en: {output_file}")
        
        print(f"\n🎉 FASE 1 COMPLETADA - LISTO PARA FASE 2: REEMPLAZAR")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN FASE 1: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
