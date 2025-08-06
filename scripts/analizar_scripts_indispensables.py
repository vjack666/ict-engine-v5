#!/usr/bin/env python3
"""
🧹 ANALIZADOR DE SCRIPTS INDISPENSABLES
======================================

Analiza todos los scripts en /scripts/ para determinar cuáles son
indispensables para la ejecución del sistema y cuáles se pueden eliminar.

VERSIÓN: 2.0 AsyncIO Compatible
"""

import sys
import asyncio
from pathlib import Path
import ast
# TODO: Eliminado - usar enviar_senal_log # import logging
# Configurar project root
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from sistema.logging_interface import enviar_senal_log

# MIGRADO A SLUC v2.0: logger eliminado - usar enviar_senal_log

class ScriptAnalyzer:
    """Analizador de scripts del proyecto"""

    def __init__(self, scripts_dir: Path):
        self.scripts_dir = scripts_dir
        self.essential_scripts = []
        self.utility_scripts = []
        self.diagnostic_scripts = []
        self.obsolete_scripts = []
        self.empty_scripts = []

    async def analyze_all_scripts(self):
        """Analiza todos los scripts en el directorio de forma asíncrona"""

        enviar_senal_log("INFO", "🔍 ANALIZANDO SCRIPTS DEL PROYECTO (AsyncIO)", "script_analyzer", "analysis")
        enviar_senal_log("INFO", "=" * 60, "script_analyzer", "analysis")

        # Lista de scripts a analizar
        scripts = list(self.scripts_dir.glob("*.py"))
        scripts = [s for s in scripts if s.name != "__init__.py"]

        # 🚀 Procesar scripts de forma asíncrona
        tasks = [self._analyze_script_async(script_path) for script_path in scripts]
        await asyncio.gather(*tasks, return_exceptions=True)

        await self._generate_report_async()

    async def _analyze_script_async(self, script_path: Path):
        """Analiza un script individual de forma asíncrona"""

        try:
            # 📖 Leer archivo de forma asíncrona
            content = await asyncio.to_thread(self._read_file_sync, script_path)

            # Script vacío
            if len(content.strip()) == 0:
                self.empty_scripts.append({
                    'name': script_path.name,
                    'reason': 'Archivo completamente vacío'
                })
                return

            # Analizar contenido
            lines = content.split('\n')

            # Determinar categoría basado en nombre y contenido
            script_info = {
                'name': script_path.name,
                'lines': len(lines),
                'has_main': 'if __name__ == "__main__"' in content,
                'imports_core': any('from core.' in line or 'import core.' in line for line in lines),
                'imports_dashboard': any('dashboard' in line for line in lines if line.strip().startswith(('import', 'from'))),
                'has_tests': any(word in content.lower() for word in ['test', 'verificar', 'validar']),
                'has_diagnostics': any(word in content.lower() for word in ['diagnos', 'analizar', 'audit']),
                'has_cleanup': any(word in content.lower() for word in ['limpiar', 'clean', 'obsolet']),
                'docstring': await self._extract_docstring_async(content)
            }

            # Categorizar script
            self._categorize_script(script_info)

        except Exception as e:
            enviar_senal_log("WARNING", f"Error analizando {script_path.name}: {e}", "script_analyzer", "analysis")

    def _read_file_sync(self, script_path: Path) -> str:
        """Lee un archivo de forma síncrona para usar con asyncio.to_thread"""
        with open(script_path, 'r', encoding='utf-8') as f:
            return f.read()

    async def _extract_docstring_async(self, content: str) -> str:
        """Extrae el docstring principal del script de forma asíncrona"""
        try:
            # 🔄 Parsear AST en thread separado para no bloquear
            tree = await asyncio.to_thread(ast.parse, content)
            docstring = ast.get_docstring(tree)
            if docstring:
                return docstring[:100] + "..."
        except (SyntaxError, ValueError) as e:
            enviar_senal_log("DEBUG", f"Error parsing docstring for script: {e}", "script_analyzer", "docstring_parsing")
        return "Sin docstring"

    def _categorize_script(self, script_info: dict):
        """Categoriza el script según su propósito"""

        name = script_info['name']

        # Scripts esenciales para el sistema
        if any(essential in name for essential in [
            'verificar_datos_reales',  # Verificación crítica MT5
        ]):
            if script_info['imports_core'] or script_info['imports_dashboard']:
                self.essential_scripts.append(script_info)
            else:
                self.utility_scripts.append(script_info)

        # Scripts de diagnóstico y análisis
        elif any(diag in name for diag in [
            'analizar_', 'diagnosticar_', 'audit_', 'validate_', 'verificar_', 'check_'
        ]) or script_info['has_diagnostics'] or script_info['has_tests']:
            self.diagnostic_scripts.append(script_info)

        # Scripts de limpieza y mantenimiento
        elif any(clean in name for clean in [
            'limpiar_', 'clean_', 'mejorar_', 'sprint_', 'reporte_', 'resumen_'
        ]) or script_info['has_cleanup']:
            if 'obsolet' in name or 'backup' in name:
                self.obsolete_scripts.append(script_info)
            else:
                self.utility_scripts.append(script_info)

        # Scripts de configuración y utilidades
        elif any(util in name for util in [
            'system_info', 'mostrar_', 'config_', 'test_'
        ]):
            self.utility_scripts.append(script_info)

        else:
            # Por defecto, considerar como utilidad
            self.utility_scripts.append(script_info)

    async def _generate_report_async(self):
        """Genera el reporte de análisis de forma asíncrona"""

        enviar_senal_log("INFO", "\n📊 RESULTADO DEL ANÁLISIS (AsyncIO)", "script_analyzer", "analysis")
        enviar_senal_log("INFO", "=" * 60, "script_analyzer", "analysis")

        # Scripts esenciales
        enviar_senal_log("INFO", f"\n✅ SCRIPTS ESENCIALES ({len(self.essential_scripts)}):", "script_analyzer", "analysis")
        enviar_senal_log("INFO", "   (Necesarios para ejecución del sistema)", "script_analyzer", "analysis")
        for script in self.essential_scripts:
            enviar_senal_log("INFO", f"   📌 {script['name']} - {script['docstring']}", "script_analyzer", "analysis")

        # Scripts de utilidad
        enviar_senal_log("INFO", f"\n🔧 SCRIPTS DE UTILIDAD ({len(self.utility_scripts)}):", "script_analyzer", "analysis")
        enviar_senal_log("INFO", "   (Útiles para desarrollo/mantenimiento)", "script_analyzer", "analysis")
        for script in self.utility_scripts:
            enviar_senal_log("INFO", f"   🛠️ {script['name']} - {script['lines']} líneas", "script_analyzer", "analysis")

        # Scripts de diagnóstico
        enviar_senal_log("INFO", f"\n🔍 SCRIPTS DE DIAGNÓSTICO ({len(self.diagnostic_scripts)}):", "script_analyzer", "analysis")
        enviar_senal_log("INFO", "   (Para debugging y análisis)", "script_analyzer", "analysis")
        for script in self.diagnostic_scripts:
            enviar_senal_log("INFO", f"   🧪 {script['name']} - {script['lines']} líneas", "script_analyzer", "analysis")

        # Scripts obsoletos
        enviar_senal_log("INFO", f"\n❌ SCRIPTS OBSOLETOS/CANDIDATOS A ELIMINAR ({len(self.obsolete_scripts)}):", "script_analyzer", "analysis")
        for script in self.obsolete_scripts:
            enviar_senal_log("INFO", f"   🗑️ {script['name']} - {script.get('reason', 'Obsoleto')}", "script_analyzer", "analysis")

        # Scripts vacíos
        if self.empty_scripts:
            enviar_senal_log("INFO", f"\n🚫 SCRIPTS VACÍOS ({len(self.empty_scripts)}):", "script_analyzer", "analysis")
            for script in self.empty_scripts:
                enviar_senal_log("INFO", f"   💨 {script['name']} - {script['reason']}", "script_analyzer", "analysis")

        # Recomendaciones
        await self._generate_recommendations_async()

    async def _generate_recommendations_async(self):
        """Genera recomendaciones de limpieza de forma asíncrona"""

        enviar_senal_log("INFO", "\n🎯 RECOMENDACIONES DE LIMPIEZA", "script_analyzer", "analysis")
        enviar_senal_log("INFO", "=" * 60, "script_analyzer", "analysis")

        # Scripts a mantener
        keep_scripts = self.essential_scripts + [s for s in self.utility_scripts if s['name'] in [
            'system_info.py',  # Info del sistema
            'verificar_datos_reales.py'  # Verificación MT5
        ]]

        enviar_senal_log("INFO", f"\n✅ MANTENER ({len(keep_scripts)} scripts):", "script_analyzer", "analysis")
        for script in keep_scripts:
            enviar_senal_log("INFO", f"   📌 {script['name']}", "script_analyzer", "analysis")

        # Scripts a considerar para eliminación
        remove_candidates = (
            self.obsolete_scripts +
            self.empty_scripts +
            [s for s in self.diagnostic_scripts if not any(keep in s['name'] for keep in ['validate_poi', 'verificar_'])]
        )

        enviar_senal_log("INFO", f"\n🗑️ CANDIDATOS PARA ELIMINAR ({len(remove_candidates)} scripts):", "script_analyzer", "analysis")
        for script in remove_candidates:
            reason = script.get('reason', 'No esencial para ejecución del sistema')
            enviar_senal_log("INFO", f"   ❌ {script['name']} - {reason}", "script_analyzer", "analysis")

        enviar_senal_log("INFO", f"\n📋 RESUMEN:", "script_analyzer", "analysis")
        enviar_senal_log("INFO", f"   🎯 Scripts totales analizados: {len(self.essential_scripts) + len(self.utility_scripts) + len(self.diagnostic_scripts) + len(self.obsolete_scripts) + len(self.empty_scripts)}", "script_analyzer", "analysis")
        enviar_senal_log("INFO", f"   ✅ Mantener: {len(keep_scripts)}", "script_analyzer", "analysis")
        enviar_senal_log("INFO", f"   🗑️ Eliminar: {len(remove_candidates)}", "script_analyzer", "analysis")
        enviar_senal_log("INFO", f"   💾 Espacio ahorrado: ~{sum(s.get('lines', 0) for s in remove_candidates)} líneas", "script_analyzer", "analysis")

async def main():
    """Función principal asíncrona"""

    scripts_dir = PROJECT_ROOT / "scripts"
    analyzer = ScriptAnalyzer(scripts_dir)
    await analyzer.analyze_all_scripts()

    enviar_senal_log("INFO", "\n🎉 ANÁLISIS COMPLETADO (AsyncIO)", "script_analyzer", "analysis")
    enviar_senal_log("INFO", "Revisa las recomendaciones para optimizar el proyecto", "script_analyzer", "analysis")

if __name__ == "__main__":
    asyncio.run(main())
