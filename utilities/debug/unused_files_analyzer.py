#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
=============================================================================
SCRIPT DE ANÁLISIS DE ARCHIVOS NO UTILIZADOS - ICT ENGINE v5.0
=============================================================================

Analiza el workspace para identificar archivos que posiblemente no se están
utilizando y pueden ser candidatos para limpieza.

Categorías de análisis:
- Archivos de backup (.bak, _backup, _old)
- Archivos temporales
- Archivos duplicados
- Scripts de fix ya ejecutados
- Documentos obsoletos
- Archivos de desarrollo/testing no esenciales
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Set
from collections import defaultdict

class UnusedFilesAnalyzer:
    """
    Analizador de archivos no utilizados en ICT Engine v5.0
    """

    def __init__(self):
        self.base_path = Path(r"c:\Users\v_jac\Desktop\itc engine v5.0")
        self.unused_files = defaultdict(list)
        self.important_files = set()
        self.file_references = defaultdict(set)

        # Patrones de archivos que probablemente no se usan
        self.unused_patterns = [
            r'.*\.bak$',
            r'.*_backup\.py$',
            r'.*_old\.py$',
            r'.*_temp\.py$',
            r'.*_test_.*\.py$',
            r'.*\.log$',
            r'.*\.tmp$',
            r'.*_copy\.py$',
            r'.*_original\.py$',
            r'.*_v\d+\.py$',  # Versiones numeradas
            r'fix_.*\.py$',   # Scripts de fix temporales
        ]

        # Archivos críticos que nunca deben borrarse
        self.critical_files = {
            'main.py',
            'dashboard_definitivo.py',
            'logging_interface.py',
            'smart_directory_logger.py',
            'config_manager.py',
            'requirements.txt',
            'pytest.ini',
            'README.md',
            '__init__.py'
        }

        # Directorios a analizar con especial cuidado
        self.special_dirs = {
            'scripts',
            'debugging',
            'utilities',
            'temp',
            '__pycache__',
            'data/logs',
            'docs/bitacoras'
        }

    def scan_for_unused_files(self) -> Dict[str, List[str]]:
        """Escanea y categoriza archivos posiblemente no utilizados"""

        print("🔍 Escaneando archivos posiblemente no utilizados...")
        print("=" * 60)

        for file_path in self.base_path.rglob("*"):
            if file_path.is_file():
                self._analyze_file(file_path)

        return dict(self.unused_files)

    def _analyze_file(self, file_path: Path):
        """Analiza un archivo específico"""
        relative_path = file_path.relative_to(self.base_path)
        file_name = file_path.name

        # Categorizar por tipo
        if self._is_backup_file(file_path):
            self.unused_files['🗂️ Archivos de Backup'].append(str(relative_path))

        elif self._is_temp_file(file_path):
            self.unused_files['📁 Archivos Temporales'].append(str(relative_path))

        elif self._is_fix_script(file_path):
            self.unused_files['🔧 Scripts de Fix (Ya ejecutados)'].append(str(relative_path))

        elif self._is_old_documentation(file_path):
            self.unused_files['📄 Documentación Obsoleta'].append(str(relative_path))

        elif self._is_duplicate_file(file_path):
            self.unused_files['🔄 Posibles Duplicados'].append(str(relative_path))

        elif self._is_test_file(file_path):
            self.unused_files['🧪 Archivos de Testing'].append(str(relative_path))

        elif self._is_cache_file(file_path):
            self.unused_files['💾 Archivos de Cache'].append(str(relative_path))

        elif self._is_log_file(file_path):
            self.unused_files['📋 Archivos de Log'].append(str(relative_path))

    def _is_backup_file(self, file_path: Path) -> bool:
        """Detecta archivos de backup"""
        name = file_path.name.lower()
        return (
            name.endswith('.bak') or
            '_backup' in name or
            '_old' in name or
            '_original' in name or
            name.startswith('backup_') or
            '_v20_backup' in name
        )

    def _is_temp_file(self, file_path: Path) -> bool:
        """Detecta archivos temporales"""
        name = file_path.name.lower()
        parent = file_path.parent.name.lower()
        return (
            name.endswith('.tmp') or
            name.endswith('.temp') or
            '_temp' in name or
            'temp' in parent or
            '__pycache__' in str(file_path)
        )

    def _is_fix_script(self, file_path: Path) -> bool:
        """Detecta scripts de fix que ya fueron ejecutados"""
        name = file_path.name.lower()
        return (
            name.startswith('fix_') or
            'fix_' in name or
            'quick_fix' in name or
            'instant_fix' in name or
            'hotfix' in name
        )

    def _is_old_documentation(self, file_path: Path) -> bool:
        """Detecta documentación obsoleta"""
        name = file_path.name.lower()
        return (
            name.endswith('_old.md') or
            '_deprecated' in name or
            'legacy' in name or
            (name == 'readme_old.md')
        )

    def _is_duplicate_file(self, file_path: Path) -> bool:
        """Detecta posibles duplicados"""
        name = file_path.name.lower()
        return (
            '_copy' in name or
            '_duplicate' in name or
            bool(re.match(r'.*_v\d+\.(py|md)$', name)) or
            bool(re.match(r'.*\(\d+\)\.(py|md)$', name))
        )

    def _is_test_file(self, file_path: Path) -> bool:
        """Detecta archivos de testing no esenciales"""
        name = file_path.name.lower()
        parent = file_path.parent.name.lower()
        return (
            name.startswith('test_') and not name in ['test_config_manager.py'] or
            '_test' in name or
            'debug_test' in name or
            ('testing' in parent and name.endswith('.py'))
        )

    def _is_cache_file(self, file_path: Path) -> bool:
        """Detecta archivos de cache"""
        name = file_path.name.lower()
        return (
            name.endswith('.pyc') or
            name.endswith('.pyo') or
            '__pycache__' in str(file_path) or
            name.endswith('.cache')
        )

    def _is_log_file(self, file_path: Path) -> bool:
        """Detecta archivos de log"""
        name = file_path.name.lower()
        return (
            name.endswith('.log') or
            name.endswith('.jsonl') or
            (name.endswith('.txt') and 'log' in name)
        )

    def generate_report(self) -> str:
        """Genera reporte completo de archivos no utilizados"""

        unused_files = self.scan_for_unused_files()

        report = []
        report.append("# 🗑️ REPORTE: ARCHIVOS POSIBLEMENTE NO UTILIZADOS")
        report.append("")
        report.append(f"**Fecha:** {self._get_current_date()}")
        report.append("**Propósito:** Identificar archivos candidatos para limpieza")
        report.append("**Estado:** ⚠️ REVISAR ANTES DE BORRAR")
        report.append("")
        report.append("---")
        report.append("")

        total_files = sum(len(files) for files in unused_files.values())
        report.append(f"## 📊 **RESUMEN**")
        report.append("")
        report.append(f"**Total archivos identificados:** {total_files}")
        report.append(f"**Categorías encontradas:** {len(unused_files)}")
        report.append("")

        # Recomendaciones por categoría
        for category, files in unused_files.items():
            if not files:
                continue

            report.append(f"## {category}")
            report.append("")
            report.append(f"**Archivos encontrados:** {len(files)}")
            report.append("")

            # Agregar recomendación específica
            recommendation = self._get_category_recommendation(category)
            report.append(f"**Recomendación:** {recommendation}")
            report.append("")

            report.append("```")
            for file_path in sorted(files):
                report.append(file_path)
            report.append("```")
            report.append("")

        # Agregar advertencias y próximos pasos
        report.append("---")
        report.append("")
        report.append("## ⚠️ **ADVERTENCIAS IMPORTANTES**")
        report.append("")
        report.append("### 🚫 **NO BORRAR SIN VERIFICAR:**")
        report.append("- Archivos de configuración críticos")
        report.append("- Scripts que pueden ser reutilizados")
        report.append("- Documentación de referencia")
        report.append("- Logs recientes importantes")
        report.append("")
        report.append("### ✅ **SEGUROS PARA BORRAR:**")
        report.append("- Archivos .pyc y __pycache__")
        report.append("- Logs antiguos (>7 días)")
        report.append("- Archivos .bak confirmados")
        report.append("- Scripts de fix ya ejecutados exitosamente")
        report.append("")
        report.append("## 🎯 **PRÓXIMOS PASOS RECOMENDADOS**")
        report.append("")
        report.append("1. **Revisar cada categoría** individualmente")
        report.append("2. **Verificar dependencias** antes de borrar")
        report.append("3. **Crear backup** de archivos dudosos")
        report.append("4. **Borrar por fases** empezando por lo más seguro")
        report.append("5. **Validar sistema** después de cada limpieza")
        report.append("")
        report.append("---")
        report.append("")
        report.append("**Generado por:** UnusedFilesAnalyzer v1.0")
        report.append(f"**ICT Engine v5.0** - Análisis de Limpieza")

        return "\n".join(report)

    def _get_category_recommendation(self, category: str) -> str:
        """Obtiene recomendación específica por categoría"""
        recommendations = {
            '🗂️ Archivos de Backup': 'REVISAR - Verificar que los originales funcionen antes de borrar',
            '📁 Archivos Temporales': 'BORRAR - Seguros para eliminar',
            '🔧 Scripts de Fix (Ya ejecutados)': 'REVISAR - Mantener solo si pueden reutilizarse',
            '📄 Documentación Obsoleta': 'REVISAR - Verificar si hay información valiosa',
            '🔄 Posibles Duplicados': 'REVISAR - Comparar contenido antes de borrar',
            '🧪 Archivos de Testing': 'REVISAR - Mantener tests importantes',
            '💾 Archivos de Cache': 'BORRAR - Seguros para eliminar (se regeneran)',
            '📋 Archivos de Log': 'REVISAR - Mantener logs recientes importantes'
        }
        return recommendations.get(category, 'REVISAR CUIDADOSAMENTE')

    def _get_current_date(self) -> str:
        """Obtiene fecha actual"""
        from datetime import datetime
        return datetime.now().strftime("%d de %B de %Y")

def main():
    """Función principal"""
    print("🗑️ ANÁLISIS DE ARCHIVOS NO UTILIZADOS - ICT ENGINE v5.0")
    print("=" * 60)

    analyzer = UnusedFilesAnalyzer()
    report = analyzer.generate_report()

    # Guardar reporte
    report_path = Path("docs/bitacoras/reportes/ARCHIVOS_NO_UTILIZADOS_ANALISIS.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"📄 Reporte generado: {report_path}")
    print("✅ Análisis completado")

    # Mostrar resumen en consola
    lines = report.split('\n')
    summary_start = False
    for line in lines:
        if '## 📊 **RESUMEN**' in line:
            summary_start = True
        elif summary_start and line.startswith('## '):
            break
        elif summary_start:
            print(line)

if __name__ == "__main__":
    main()
