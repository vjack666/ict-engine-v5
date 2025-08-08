#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 ICT ENGINE v6.0 ENTERPRISE - TEST RUNNER GENERAL
==================================================

Script maestro para ejecutar TODOS los tests disponibles de forma ágil.
Ejecuta tests en paralelo cuando es posible y genera reporte completo.

Tests incluidos:
- SIC v3.1 Enterprise completo
- Advanced Candle Downloader  
- MT5 Data Manager
- POI System Integration
- Pattern Detector
- Critical Timeframes H1/H4
- Enterprise Performance
- Storage Inteligente
- Sistema FundedNext
- Y todos los demás...

Autor: ICT Engine v6.1.0 Team
Versión: v6.1.0-enterprise
"""

import sys
import time
import threading
import subprocess
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Configurar paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class TestRunner:
    """🚀 Runner de tests paralelo y optimizado"""
    
    def __init__(self):
        self.tests_dir = project_root / "tests"
        self.results = {}
        self.start_time = None
        self.total_time = 0
        
    def discover_tests(self):
        """🔍 Descubrir todos los tests disponibles"""
        test_files = []
        
        if self.tests_dir.exists():
            test_files.extend(list(self.tests_dir.glob("test_*.py")))
        
        # Buscar también en el directorio raíz
        test_files.extend(list(project_root.glob("test_*.py")))
        
        # Filtrar duplicados
        unique_tests = {}
        for test_file in test_files:
            unique_tests[test_file.name] = test_file
        
        return list(unique_tests.values())
    
    def run_single_test(self, test_file):
        """🧪 Ejecutar un test individual"""
        test_name = test_file.stem
        print(f"🔄 Ejecutando: {test_name}")
        
        start_time = time.time()
        try:
            # Ejecutar el test
            result = subprocess.run(
                [sys.executable, str(test_file)],
                cwd=str(project_root),
                capture_output=True,
                text=True,
                timeout=120  # 2 minutos máximo por test
            )
            
            duration = time.time() - start_time
            success = result.returncode == 0
            
            return {
                'name': test_name,
                'success': success,
                'duration': duration,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'file_path': str(test_file)
            }
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return {
                'name': test_name,
                'success': False,
                'duration': duration,
                'stdout': '',
                'stderr': 'TEST TIMEOUT (>2min)',
                'file_path': str(test_file)
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                'name': test_name,
                'success': False,
                'duration': duration,
                'stdout': '',
                'stderr': f'ERROR: {str(e)}',
                'file_path': str(test_file)
            }
    
    def run_tests_parallel(self, test_files, max_workers=4):
        """⚡ Ejecutar tests en paralelo"""
        print(f"🚀 Ejecutando {len(test_files)} tests con {max_workers} workers...")
        
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Enviar todos los tests
            future_to_test = {
                executor.submit(self.run_single_test, test_file): test_file 
                for test_file in test_files
            }
            
            # Recoger resultados conforme vayan completando
            for future in as_completed(future_to_test):
                test_file = future_to_test[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    # Mostrar resultado inmediato
                    status = "✅" if result['success'] else "❌"
                    print(f"{status} {result['name']:<35} ({result['duration']:.2f}s)")
                    
                except Exception as e:
                    print(f"❌ {test_file.stem:<35} (ERROR: {e})")
        
        return results
    
    def generate_report(self, results):
        """📊 Generar reporte completo"""
        passed = sum(1 for r in results if r['success'])
        failed = len(results) - passed
        total_duration = sum(r['duration'] for r in results)
        
        # Reporte en consola
        print("\n" + "="*80)
        print("📋 REPORTE GENERAL DE TESTS ICT ENGINE v6.0 ENTERPRISE")
        print("="*80)
        print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏱️ Duración total: {total_duration:.2f}s")
        print(f"📊 Tests ejecutados: {len(results)}")
        print(f"✅ Exitosos: {passed}")
        print(f"❌ Fallidos: {failed}")
        print(f"📈 Tasa de éxito: {(passed/len(results)*100):.1f}%")
        print("-"*80)
        
        # Detalles por test
        print("📋 DETALLE POR TEST:")
        results.sort(key=lambda x: x['duration'], reverse=True)
        
        for result in results:
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"{status} {result['name']:<35} {result['duration']:.2f}s")
            
            # Mostrar errores si los hay
            if not result['success'] and result['stderr']:
                error_lines = result['stderr'].split('\n')[:3]  # Primeras 3 líneas
                for line in error_lines:
                    if line.strip():
                        print(f"      🔸 {line.strip()}")
        
        print("-"*80)
        
        # Tests más lentos
        print("🐌 TESTS MÁS LENTOS:")
        for result in results[:5]:  # Top 5 más lentos
            print(f"   {result['name']:<35} {result['duration']:.2f}s")
        
        # Tests fallidos
        if failed > 0:
            print(f"\n❌ TESTS FALLIDOS ({failed}):")
            for result in results:
                if not result['success']:
                    print(f"   • {result['name']}")
        
        print("="*80)
        
        # Guardar reporte JSON
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': len(results),
                'passed': passed,
                'failed': failed,
                'success_rate': passed/len(results)*100,
                'total_duration': total_duration
            },
            'results': results
        }
        
        report_file = project_root / "logs" / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Reporte detallado guardado en: {report_file}")
        
        return passed == len(results)
    
    def run_priority_tests_first(self, test_files):
        """⚡ Ejecutar tests prioritarios primero"""
        # Tests críticos que deben ejecutarse primero
        priority_tests = [
            'test_critical_timeframes',
            'test_fundednext_system', 
            'test_enterprise_performance',
            'test_advanced_candle_downloader'
        ]
        
        priority_files = []
        regular_files = []
        
        for test_file in test_files:
            test_name = test_file.stem
            if any(priority in test_name for priority in priority_tests):
                priority_files.append(test_file)
            else:
                regular_files.append(test_file)
        
        print(f"🎯 EJECUTANDO {len(priority_files)} TESTS PRIORITARIOS PRIMERO...")
        priority_results = self.run_tests_parallel(priority_files, max_workers=2)
        
        # Verificar que los críticos pasaron
        critical_passed = all(r['success'] for r in priority_results)
        if not critical_passed:
            print("\n⚠️ TESTS CRÍTICOS FALLARON - Continuando con precaución...")
        
        print(f"\n🔄 EJECUTANDO {len(regular_files)} TESTS REGULARES...")
        regular_results = self.run_tests_parallel(regular_files, max_workers=4)
        
        return priority_results + regular_results

def main():
    """🎯 Función principal"""
    print("🧪 ICT ENGINE v6.0 ENTERPRISE - TEST RUNNER GENERAL")
    print("="*80)
    
    runner = TestRunner()
    runner.start_time = time.time()
    
    # Descubrir tests
    test_files = runner.discover_tests()
    
    if not test_files:
        print("❌ No se encontraron archivos de test.")
        return False
    
    print(f"🔍 Tests encontrados: {len(test_files)}")
    for test_file in test_files:
        print(f"   📄 {test_file.name}")
    
    print(f"\n🚀 INICIANDO EJECUCIÓN DE TESTS...")
    
    # Ejecutar tests con prioridad
    results = runner.run_priority_tests_first(test_files)
    
    # Generar reporte
    runner.total_time = time.time() - runner.start_time
    success = runner.generate_report(results)
    
    if success:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ ICT ENGINE v6.0 ENTERPRISE está funcionando perfectamente")
    else:
        print("\n⚠️ Algunos tests fallaron - Revisar detalles arriba")
    
    print(f"\n⏱️ Tiempo total de ejecución: {runner.total_time:.2f}s")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
