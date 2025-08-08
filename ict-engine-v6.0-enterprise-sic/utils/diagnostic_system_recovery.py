#!/usr/bin/env python3
"""
🔍 DIAGNÓSTICO COMPLETO DE ARCHIVOS - ICT ENGINE v6.0
===================================================

Script para identificar archivos vacíos, corruptos o faltantes
y generar plan de recuperación automático.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json

class ICTSystemDiagnostic:
    """Diagnóstico completo del sistema ICT Engine v6.1.0"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.issues_found = []
        self.files_analyzed = 0
        self.empty_files = []
        self.corrupted_files = []
        self.missing_critical_files = []
        
    def run_complete_diagnostic(self):
        """Ejecutar diagnóstico completo"""
        print("🔍 ICT ENGINE v6.0 - DIAGNÓSTICO COMPLETO DE ARCHIVOS")
        print("=" * 60)
        print(f"📁 Proyecto: {self.project_root}")
        print(f"🕐 Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 1. Escanear estructura de directorios
        self._scan_directory_structure()
        
        # 2. Verificar archivos críticos
        self._check_critical_files()
        
        # 3. Detectar archivos vacíos
        self._detect_empty_files()
        
        # 4. Verificar archivos Python
        self._verify_python_files()
        
        # 5. Generar reporte
        self._generate_report()
        
        # 6. Crear plan de recuperación
        self._create_recovery_plan()
    
    def _scan_directory_structure(self):
        """Escanear estructura de directorios"""
        print("📂 ESCANEANDO ESTRUCTURA DE DIRECTORIOS...")
        
        expected_structure = {
            'core/': {
                'data_management/': [
                    'advanced_candle_downloader.py',
                    'mt5_data_manager.py',
                    'mt5_connection_manager.py',
                    '__init__.py'
                ],
                'analysis/': [
                    'market_structure_analyzer.py',
                    'market_structure_analyzer_v6.py',
                    'pattern_detector.py',
                    'poi_system.py',
                    '__init__.py'
                ],
                'smart_money_concepts/': [
                    'smart_money_analyzer.py',
                    '__init__.py'
                ],
                'ict_engine/': [
                    '__init__.py'
                ]
            },
            'sistema/sic_v3_1/': [
                'smart_import.py',
                'lazy_loading.py',
                'predictive_cache.py',
                'advanced_debugger.py',
                '__init__.py'
            ],
            'utils/': [
                'smart_trading_logger.py',
                '__init__.py'
            ],
            'tests/': [
                'test_final_system_validation_v6.py',
                'test_smart_money_integration_v6.py',
                'test_multi_timeframe_integration_v6.py',
                '__init__.py'
            ],
            'docs/': [
                'README.md',
                'INDEX.md',
                'roadmap_v6.md',
                'BITACORA_DESARROLLO_SMART_MONEY_v6.md'
            ]
        }
        
        # Verificar estructura
        missing_dirs = []
        missing_files = []
        
        for dir_path, content in expected_structure.items():
            full_dir_path = self.project_root / dir_path
            
            if not full_dir_path.exists():
                missing_dirs.append(dir_path)
                print(f"❌ Directorio faltante: {dir_path}")
                continue
            else:
                print(f"✅ Directorio OK: {dir_path}")
            
            if isinstance(content, dict):
                # Es un subdirectorio
                for subdir, files in content.items():
                    full_subdir_path = full_dir_path / subdir
                    if not full_subdir_path.exists():
                        missing_dirs.append(f"{dir_path}{subdir}")
                        print(f"❌ Subdirectorio faltante: {dir_path}{subdir}")
                        continue
                    else:
                        print(f"✅ Subdirectorio OK: {dir_path}{subdir}")
                    
                    # Verificar archivos en subdirectorio
                    for file in files:
                        file_path = full_subdir_path / file
                        if not file_path.exists():
                            missing_files.append(f"{dir_path}{subdir}/{file}")
                            print(f"❌ Archivo faltante: {dir_path}{subdir}/{file}")
                        else:
                            print(f"✅ Archivo OK: {dir_path}{subdir}/{file}")
            else:
                # Es una lista de archivos
                for file in content:
                    file_path = full_dir_path / file
                    if not file_path.exists():
                        missing_files.append(f"{dir_path}{file}")
                        print(f"❌ Archivo faltante: {dir_path}{file}")
                    else:
                        print(f"✅ Archivo OK: {dir_path}{file}")
        
        self.missing_critical_files = missing_files
        print(f"\n📊 Resumen estructura:")
        print(f"   Directorios faltantes: {len(missing_dirs)}")
        print(f"   Archivos faltantes: {len(missing_files)}")
        print()
    
    def _check_critical_files(self):
        """Verificar archivos críticos del sistema"""
        print("🔍 VERIFICANDO ARCHIVOS CRÍTICOS...")
        
        critical_files = [
            'main.py',
            'core/smart_money_concepts/smart_money_analyzer.py',
            'core/analysis/pattern_detector.py',
            'core/data_management/advanced_candle_downloader.py',
            'sistema/sic_v3_1/smart_import.py',
            'utils/smart_trading_logger.py'
        ]
        
        for file_path in critical_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                size = full_path.stat().st_size
                if size == 0:
                    print(f"⚠️  Archivo VACÍO: {file_path}")
                    self.empty_files.append(file_path)
                elif size < 100:  # Muy pequeño, posiblemente corrupto
                    print(f"⚠️  Archivo SOSPECHOSO (muy pequeño): {file_path} ({size} bytes)")
                    self.corrupted_files.append(file_path)
                else:
                    print(f"✅ Archivo crítico OK: {file_path} ({size:,} bytes)")
            else:
                print(f"❌ Archivo crítico FALTANTE: {file_path}")
                self.missing_critical_files.append(file_path)
        
        print()
    
    def _detect_empty_files(self):
        """Detectar todos los archivos vacíos"""
        print("📄 DETECTANDO ARCHIVOS VACÍOS...")
        
        for file_path in self.project_root.rglob('*.py'):
            if file_path.stat().st_size == 0:
                rel_path = file_path.relative_to(self.project_root)
                print(f"⚠️  Archivo vacío: {rel_path}")
                self.empty_files.append(str(rel_path))
            self.files_analyzed += 1
        
        print(f"📊 Archivos Python analizados: {self.files_analyzed}")
        print(f"📊 Archivos vacíos encontrados: {len(self.empty_files)}")
        print()
    
    def _verify_python_files(self):
        """Verificar sintaxis de archivos Python"""
        print("🐍 VERIFICANDO SINTAXIS PYTHON...")
        
        syntax_errors = []
        
        for file_path in self.project_root.rglob('*.py'):
            if file_path.stat().st_size > 0:  # Solo archivos no vacíos
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Verificar sintaxis básica
                    compile(content, str(file_path), 'exec')
                    
                except SyntaxError as e:
                    rel_path = file_path.relative_to(self.project_root)
                    print(f"❌ Error sintaxis: {rel_path} - {e}")
                    syntax_errors.append(str(rel_path))
                    
                except UnicodeDecodeError:
                    rel_path = file_path.relative_to(self.project_root)
                    print(f"❌ Error encoding: {rel_path}")
                    syntax_errors.append(str(rel_path))
                    
                except Exception as e:
                    rel_path = file_path.relative_to(self.project_root)
                    print(f"⚠️  Error verificando: {rel_path} - {e}")
        
        print(f"📊 Archivos con errores de sintaxis: {len(syntax_errors)}")
        print()
    
    def _generate_report(self):
        """Generar reporte completo"""
        print("📋 GENERANDO REPORTE DIAGNÓSTICO...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'summary': {
                'files_analyzed': self.files_analyzed,
                'empty_files_count': len(self.empty_files),
                'corrupted_files_count': len(self.corrupted_files),
                'missing_critical_files_count': len(self.missing_critical_files)
            },
            'empty_files': self.empty_files,
            'corrupted_files': self.corrupted_files,
            'missing_critical_files': self.missing_critical_files,
            'status': 'CRITICAL' if len(self.missing_critical_files) > 0 else 'WARNING' if len(self.empty_files) > 0 else 'OK'
        }
        
        # Guardar reporte JSON
        report_file = self.project_root / 'diagnostic_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Reporte guardado: {report_file}")
        
        # Mostrar resumen
        print("\n" + "="*60)
        print("📊 RESUMEN DIAGNÓSTICO")
        print("="*60)
        print(f"🔍 Archivos analizados: {self.files_analyzed}")
        print(f"⚠️  Archivos vacíos: {len(self.empty_files)}")
        print(f"❌ Archivos corruptos: {len(self.corrupted_files)}")
        print(f"❌ Archivos críticos faltantes: {len(self.missing_critical_files)}")
        print(f"🎯 Estado general: {report['status']}")
        
        if len(self.empty_files) > 0:
            print("\n⚠️  ARCHIVOS VACÍOS DETECTADOS:")
            for file in self.empty_files[:10]:  # Mostrar primeros 10
                print(f"   - {file}")
            if len(self.empty_files) > 10:
                print(f"   ... y {len(self.empty_files) - 10} más")
        
        if len(self.missing_critical_files) > 0:
            print("\n❌ ARCHIVOS CRÍTICOS FALTANTES:")
            for file in self.missing_critical_files:
                print(f"   - {file}")
        
        print()
    
    def _create_recovery_plan(self):
        """Crear plan de recuperación automático"""
        print("🛠️  CREANDO PLAN DE RECUPERACIÓN...")
        
        recovery_commands = []
        
        # Comandos para archivos faltantes críticos
        if len(self.missing_critical_files) > 0:
            recovery_commands.append("# RECUPERACIÓN DE ARCHIVOS CRÍTICOS FALTANTES")
            recovery_commands.append("echo '🔄 Recuperando archivos críticos...'")
            
            for file in self.missing_critical_files:
                if 'smart_money_analyzer.py' in file:
                    recovery_commands.append(f"echo '⚠️  CRÍTICO: {file} faltante - requiere recuperación manual'")
                elif 'pattern_detector.py' in file:
                    recovery_commands.append(f"echo '⚠️  CRÍTICO: {file} faltante - requiere recuperación manual'")
                elif '__init__.py' in file:
                    recovery_commands.append(f"touch '{file}'")
                    recovery_commands.append(f"echo '# ICT Engine v6.1.0 Enterprise Module' > '{file}'")
        
        # Comandos para archivos vacíos
        if len(self.empty_files) > 0:
            recovery_commands.append("\n# RECUPERACIÓN DE ARCHIVOS VACÍOS")
            recovery_commands.append("echo '🔄 Recuperando archivos vacíos...'")
            
            for file in self.empty_files:
                if '__init__.py' in file:
                    recovery_commands.append(f"echo '# ICT Engine v6.1.0 Enterprise Module' > '{file}'")
                else:
                    recovery_commands.append(f"echo '⚠️  VACÍO: {file} - requiere recuperación manual'")
        
        # Guardar script de recuperación
        recovery_file = self.project_root / 'recovery_plan.sh'
        with open(recovery_file, 'w', encoding='utf-8') as f:
            f.write("#!/bin/bash\n")
            f.write("# ICT Engine v6.1.0 - Plan de Recuperación Automático\n")
            f.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write('\n'.join(recovery_commands))
        
        print(f"✅ Plan de recuperación creado: {recovery_file}")
        
        # Crear también versión PowerShell
        recovery_ps_file = self.project_root / 'recovery_plan.ps1'
        ps_commands = [cmd.replace('echo', 'Write-Host').replace('touch', 'New-Item -ItemType File -Force') 
                      for cmd in recovery_commands if not cmd.startswith('#')]
        
        with open(recovery_ps_file, 'w', encoding='utf-8') as f:
            f.write("# ICT Engine v6.1.0 - Plan de Recuperación PowerShell\n")
            f.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write('\n'.join(ps_commands))
        
        print(f"✅ Plan PowerShell creado: {recovery_ps_file}")
        print()

def main():
    """Ejecutar diagnóstico completo"""
    try:
        diagnostic = ICTSystemDiagnostic()
        diagnostic.run_complete_diagnostic()
        
        print("🎯 DIAGNÓSTICO COMPLETADO")
        print("="*60)
        print("📋 Revisa el archivo 'diagnostic_report.json' para detalles completos")
        print("🛠️  Ejecuta 'recovery_plan.ps1' para recuperación automática")
        print("⚠️  Archivos críticos requerirán recuperación manual")
        print()
        
    except Exception as e:
        print(f"❌ Error en diagnóstico: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
