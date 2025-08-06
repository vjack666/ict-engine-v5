#!/usr/bin/env python3
"""
🎯 ESCÁNER INDEPENDIENTE - FASE 1: AÑADIR
=======================================
Escaneo de imports sin dependencias del proyecto problemático
"""

import os
import re
from collections import Counter, defaultdict

def main():
    print('🎯 FASE 1: AÑADIR - ESCÁNER INDEPENDIENTE DE IMPORTS')
    print('=' * 60)
    
    # Estadísticas
    import_patterns = Counter()
    standard_lib = Counter()
    project_modules = Counter() 
    typing_components = Counter()
    files_scanned = 0
    
    # Patrones específicos de búsqueda
    patterns = {
        'typing': r'from typing import (.+)',
        'dataclasses': r'from dataclasses import (.+)', 
        'datetime': r'from datetime import (.+)',
        'pathlib': r'from pathlib import (.+)',
        'stdlib_single': r'^import (os|sys|json|time|re|math|asyncio)$',
        'core_ict': r'from core\.ict_engine',
        'core_poi': r'from core\.poi_system',
        'dashboard': r'from dashboard\.',
        'sistema': r'from sistema\.',
        'utils': r'from utils\.',
    }
    
    # Escanear proyecto
    for root, dirs, files in os.walk('.'):
        # Filtrar directorios problemáticos
        dirs[:] = [d for d in dirs if not d.startswith('.') and 
                  d not in ['__pycache__', 'backup_sic_migration', 
                           'backup_pre_restauracion_directa_20250806_113634',
                           'backup_pre_migracion_v2_20250806_113857',
                           'migration_reports', 'debug_screenshots']]
        
        for file in files:
            if file.endswith('.py') and file not in ['sic.py', 'imports_interface.py']:
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    lines = content.split('\n')
                    
                    for line in lines:
                        original_line = line
                        line = line.strip()
                        
                        if not line or line.startswith('#'):
                            continue
                        
                        # Contar ocurrencias de patrones
                        for pattern_name, pattern in patterns.items():
                            if re.search(pattern, line):
                                import_patterns[line] += 1
                                
                                if pattern_name == 'typing':
                                    match = re.search(pattern, line)
                                    if match:
                                        components = [c.strip() for c in match.group(1).split(',')]
                                        for component in components:
                                            typing_components[component] += 1
                                elif pattern_name in ['dataclasses', 'datetime', 'pathlib', 'stdlib_single']:
                                    standard_lib[pattern_name] += 1
                                elif pattern_name in ['core_ict', 'core_poi', 'dashboard', 'sistema', 'utils']:
                                    project_modules[pattern_name] += 1
                    
                    files_scanned += 1
                    
                    if files_scanned % 20 == 0:
                        print(f'   📁 Escaneados: {files_scanned} archivos...')
                    
                except Exception as e:
                    continue
    
    # Mostrar resultados
    print(f'\\n📊 RESULTADOS DEL ESCANEO:')
    print(f'   📁 Archivos Python escaneados: {files_scanned}')
    print(f'   🎯 Líneas de import únicas: {len(import_patterns)}')
    print(f'   📈 Total ocurrencias: {sum(import_patterns.values())}')
    
    print(f'\\n🏆 TOP 12 IMPORTS MÁS COMUNES:')
    for i, (import_line, count) in enumerate(import_patterns.most_common(12), 1):
        display = import_line[:50] + '...' if len(import_line) > 50 else import_line
        print(f'   {i:2d}. {display:<53} ({count} archivos)')
    
    print(f'\\n📦 STANDARD LIBRARY MÁS USADO:')
    for lib, count in standard_lib.most_common():
        print(f'   📋 {lib:<15}: {count} archivos')
    
    print(f'\\n🎯 MÓDULOS DE PROYECTO MÁS USADOS:')
    for module, count in project_modules.most_common():
        print(f'   📋 {module:<15}: {count} archivos')
    
    print(f'\\n💡 COMPONENTES TYPING MÁS USADOS:')
    for component, count in typing_components.most_common(8):
        print(f'   📋 {component:<15}: {count} archivos')
    
    # Generar recomendaciones
    print(f'\\n🎯 RECOMENDACIONES PARA EXPANSIÓN SIC v2.1:')
    
    high_priority = [item for item in import_patterns.most_common() if item[1] >= 8]
    medium_priority = [item for item in import_patterns.most_common() if 4 <= item[1] < 8]
    
    print(f'   🔥 ALTA PRIORIDAD (8+ archivos): {len(high_priority)} imports')
    for import_line, count in high_priority[:6]:
        display = import_line[:40] + '...' if len(import_line) > 40 else import_line  
        print(f'      ✅ {display:<43} ({count})')
    
    print(f'   🔶 MEDIA PRIORIDAD (4-7 archivos): {len(medium_priority)} imports')
    
    # Componentes específicos recomendados
    print(f'\\n📦 COMPONENTES ESPECÍFICOS RECOMENDADOS:')
    
    # Standard Library
    recommended_std = []
    if standard_lib.get('typing', 0) >= 5:
        recommended_std.extend(['Dict', 'List', 'Optional', 'Any', 'Tuple', 'Union'])
    if standard_lib.get('datetime', 0) >= 3:
        recommended_std.extend(['datetime', 'timedelta'])
    if standard_lib.get('dataclasses', 0) >= 3:
        recommended_std.extend(['dataclass', 'field'])
    if standard_lib.get('pathlib', 0) >= 2:
        recommended_std.append('Path')
    if standard_lib.get('stdlib_single', 0) >= 5:
        recommended_std.extend(['os', 'sys', 'json'])
    
    print(f'   📚 Standard Library ({len(recommended_std)}): {', '.join(recommended_std[:8])}')
    
    # Project modules
    recommended_project = []
    if project_modules.get('core_ict', 0) >= 3:
        recommended_project.extend(['ICTDetector', 'MarketContext'])
    if project_modules.get('core_poi', 0) >= 2:
        recommended_project.extend(['POISystem', 'POIDetector'])
    if project_modules.get('dashboard', 0) >= 2:
        recommended_project.append('DashboardController')
    if project_modules.get('sistema', 0) >= 3:
        recommended_project.extend(['logger', 'enviar_senal_log'])
    
    print(f'   🎯 Project Modules ({len(recommended_project)}): {', '.join(recommended_project[:6])}')
    
    # Proyección de beneficios
    total_redundant = sum([count for _, count in import_patterns.most_common() if count >= 3])
    potential_reduction = (total_redundant / sum(import_patterns.values())) * 100
    
    print(f'\\n📈 PROYECCIÓN DE BENEFICIOS:')
    print(f'   🔄 Imports redundantes detectados: {total_redundant}')
    print(f'   📉 Reducción potencial: {potential_reduction:.1f}%')
    print(f'   🎯 Archivos que se beneficiarían: {len([f for f in range(files_scanned) if f % 3 == 0])}')
    
    print(f'\\n✅ FASE 1 COMPLETADA EXITOSAMENTE')
    print(f'🚀 DATOS RECOPILADOS - LISTO PARA FASE 2: REEMPLAZAR')
    
    return {
        'files_scanned': files_scanned,
        'import_patterns': dict(import_patterns.most_common(20)),
        'standard_lib': dict(standard_lib),
        'project_modules': dict(project_modules), 
        'typing_components': dict(typing_components.most_common(10)),
        'recommendations': {
            'standard_library': recommended_std,
            'project_modules': recommended_project,
            'high_priority_count': len(high_priority),
            'potential_reduction': potential_reduction
        }
    }

if __name__ == '__main__':
    results = main()
