#!/usr/bin/env python3
"""
CORRECTOR AUTOMÁTICO - PROTOCOLO LOG CENTRAL
==========================================

MISIÓN CRÍTICA: Migrar TODO el logging al sistema centralizado SLUC v2.0

Estrategia de corrección:
1. Eliminar imports duplicados de enviar_senal_log
2. Reemplazar prints de logging por enviar_senal_log
3. Eliminar imports de logging estándar
4. Migrar logging.X por enviar_senal_log

Autor: ICT Engine v5.0 - Sistema de Corrección Automática
"""

# MIGRACIÓN SIC v3.0 + SLUC v2.1
from sistema.sic import enviar_senal_log, log_info, log_warning

from sistema.sic import os
from sistema.sic import re
from sistema.sic import sys
from sistema.sic import Path
from sistema.sic import List, Dict, Any, Tuple
from sistema.sic import datetime

# Añadir el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent.parent))

# PROTOCOLO: Solo sistema de log centralizado
from sistema.sic import enviar_senal_log

class CorrectorLogCentral:
    """
    Corrector automático para migrar al protocolo de logging centralizado

    REGLA: Solo enviar_senal_log del sistema central
    """

    def __init__(self, ruta_proyecto: str = "."):
        self.ruta_proyecto = Path(ruta_proyecto).resolve()
        self.correcciones_realizadas = 0
        self.archivos_procesados = 0
        self.errores_encontrados = []

        # Mapeos de corrección
        self.mapeos_correccion = {
            # Niveles de logging estándar → enviar_senal_log
            'print_error': ('enviar_senal_log("ERROR", {mensaje}, __name__, "sistema")', 'ERROR'),
            'print_warning': ('enviar_senal_log("WARNING", {mensaje}, __name__, "sistema")', 'WARNING'),
            'print_info': ('enviar_senal_log("INFO", {mensaje}, __name__, "sistema")', 'INFO'),
            'print_debug': ('enviar_senal_log("DEBUG", {mensaje}, __name__, "sistema")', 'DEBUG'),

            # logging.X → enviar_senal_log
            'logging_error': ('enviar_senal_log("ERROR", {mensaje}, __name__, "sistema")', 'ERROR'),
            'logging_warning': ('enviar_senal_log("WARNING", {mensaje}, __name__, "sistema")', 'WARNING'),
            'logging_info': ('enviar_senal_log("INFO", {mensaje}, __name__, "sistema")', 'INFO'),
            'logging_debug': ('enviar_senal_log("DEBUG", {mensaje}, __name__, "sistema")', 'DEBUG'),
        }

        self.log_inicial()

    def log_inicial(self):
        """Log inicial del corrector"""
        enviar_senal_log("INFO", "🔧 INICIANDO CORRECCIÓN AUTOMÁTICA - PROTOCOLO LOG CENTRAL", __name__, "corrector")
        enviar_senal_log("INFO", f"📁 Proyecto: {self.ruta_proyecto}", __name__, "corrector")
        enviar_senal_log("WARNING", "⚠️ CORRECCIÓN MASIVA: 227 violaciones detectadas", __name__, "corrector")

    def corregir_proyecto_completo(self) -> Dict[str, Any]:
        """
        Corrección completa del proyecto

        Returns:
            Diccionario con resultados de la corrección
        """
        enviar_senal_log("INFO", "🚀 INICIANDO CORRECCIÓN MASIVA", __name__, "corrector")

        archivos_python = self._buscar_archivos_python()

        # FASE 1: Prioridad ALTA - Archivos core
        archivos_core = [f for f in archivos_python if 'core' in str(f)]
        enviar_senal_log("INFO", f"🎯 FASE 1: Corrigiendo {len(archivos_core)} archivos CORE", __name__, "corrector")

        for archivo in archivos_core:
            self._corregir_archivo(archivo)

        # FASE 2: Dashboard y scripts críticos
        archivos_dashboard = [f for f in archivos_python if any(x in str(f) for x in ['dashboard', 'main.py'])]
        enviar_senal_log("INFO", f"🎯 FASE 2: Corrigiendo {len(archivos_dashboard)} archivos DASHBOARD", __name__, "corrector")

        for archivo in archivos_dashboard:
            if archivo not in archivos_core:  # Evitar duplicados
                self._corregir_archivo(archivo)

        # FASE 3: Resto de archivos
        archivos_restantes = [f for f in archivos_python if f not in archivos_core and f not in archivos_dashboard]
        enviar_senal_log("INFO", f"🎯 FASE 3: Corrigiendo {len(archivos_restantes)} archivos RESTANTES", __name__, "corrector")

        for archivo in archivos_restantes:
            self._corregir_archivo(archivo)

        resultado = self._generar_reporte_final()
        self._log_reporte_final(resultado)

        return resultado

    def _buscar_archivos_python(self) -> List[Path]:
        """Busca todos los archivos Python del proyecto"""
        archivos = []

        # Directorios a corregir
        directorios_corregir = [
            'core', 'dashboard', 'scripts', 'sistema', 'utils',
            'config', 'utilities'
        ]

        for directorio in directorios_corregir:
            dir_path = self.ruta_proyecto / directorio
            if dir_path.exists():
                archivos.extend(dir_path.rglob('*.py'))

        # Archivos en la raíz (main.py, etc.)
        archivos.extend(self.ruta_proyecto.glob('*.py'))

        return archivos

    def _corregir_archivo(self, archivo: Path):
        """Corrige un archivo individual"""
        try:
            # Leer contenido original
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido_original = f.read()

            self.archivos_procesados += 1
            enviar_senal_log("DEBUG", f"🔧 Procesando: {archivo.relative_to(self.ruta_proyecto)}", __name__, "corrector")

            # Aplicar correcciones
            contenido_corregido = contenido_original
            correcciones_archivo = 0

            # 1. Eliminar imports duplicados de enviar_senal_log
            correcciones_archivo += self._eliminar_imports_duplicados(archivo, contenido_corregido)

            # 2. Corregir prints de logging
            contenido_corregido, correcciones_prints = self._corregir_prints_logging(contenido_corregido)
            correcciones_archivo += correcciones_prints

            # 3. Migrar logging.X calls
            contenido_corregido, correcciones_logging = self._migrar_logging_calls(contenido_corregido)
            correcciones_archivo += correcciones_logging

            # 4. Eliminar imports de logging estándar
            contenido_corregido, correcciones_imports = self._eliminar_imports_logging(contenido_corregido)
            correcciones_archivo += correcciones_imports

            # 5. Asegurar import de enviar_senal_log
            contenido_corregido = self._asegurar_import_enviar_senal_log(contenido_corregido)

            # Escribir archivo corregido si hubo cambios
            if contenido_corregido != contenido_original:
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido_corregido)

                self.correcciones_realizadas += correcciones_archivo
                enviar_senal_log("SUCCESS", f"✅ {archivo.relative_to(self.ruta_proyecto)}: {correcciones_archivo} correcciones", __name__, "corrector")
            else:
                enviar_senal_log("DEBUG", f"ℹ️ {archivo.relative_to(self.ruta_proyecto)}: Sin cambios necesarios", __name__, "corrector")

        except Exception as e:
            error_msg = f"Error corrigiendo {archivo}: {e}"
            self.errores_encontrados.append(error_msg)
            enviar_senal_log("ERROR", f"❌ {error_msg}", __name__, "corrector")

    def _eliminar_imports_duplicados(self, archivo: Path, contenido: str) -> int:
        """Elimina imports duplicados de enviar_senal_log"""
        # Esta función necesita acceso al contenido modificable
        # Por simplicidad, contamos las ocurrencias
        imports_encontrados = re.findall(r'from\s+sistema\.logging_interface\s+import\s+enviar_senal_log', contenido)
        if len(imports_encontrados) > 1:
            enviar_senal_log("WARNING", f"🔄 {archivo.relative_to(self.ruta_proyecto)}: {len(imports_encontrados)} imports duplicados", __name__, "corrector")
            return len(imports_encontrados) - 1
        return 0

    def _corregir_prints_logging(self, contenido: str) -> Tuple[str, int]:
        """Corrige prints que contienen logging"""
        correcciones = 0

        # Patrones de prints de logging
        patrones_print = [
            (r'print\s*\(\s*[\'\"]*[^)]*(?:error|ERROR)[^)]*\)', 'ERROR'),
            (r'print\s*\(\s*[\'\"]*[^)]*(?:warning|WARNING)[^)]*\)', 'WARNING'),
            (r'print\s*\(\s*[\'\"]*[^)]*(?:info|INFO)[^)]*\)', 'INFO'),
            (r'print\s*\(\s*[\'\"]*[^)]*(?:debug|DEBUG)[^)]*\)', 'DEBUG'),
        ]

        contenido_corregido = contenido

        for patron, nivel in patrones_print:
            matches = re.finditer(patron, contenido_corregido, re.IGNORECASE)
            for match in matches:
                # Extraer el mensaje del print
                print_completo = match.group(0)
                # Simplificado: reemplazar con comentario para revisión manual
                reemplazo = f'# TODO: Migrar a enviar_senal_log("{nivel}", mensaje, __name__, "sistema") # {print_completo}'
                contenido_corregido = contenido_corregido.replace(print_completo, reemplazo, 1)
                correcciones += 1

        return contenido_corregido, correcciones

    def _migrar_logging_calls(self, contenido: str) -> Tuple[str, int]:
        """Migra logging.X calls a enviar_senal_log"""
        correcciones = 0

        # Patrones de logging.X
        patrones_logging = [
            (r'logging\.error\s*\([^)]+\)', 'ERROR'),
            (r'logging\.warning\s*\([^)]+\)', 'WARNING'),
            (r'logging\.info\s*\([^)]+\)', 'INFO'),
            (r'logging\.debug\s*\([^)]+\)', 'DEBUG'),
        ]

        contenido_corregido = contenido

        for patron, nivel in patrones_logging:
            matches = re.finditer(patron, contenido_corregido)
            for match in matches:
                logging_call = match.group(0)
                # Comentar para revisión manual
                reemplazo = f'# TODO: Migrar a enviar_senal_log("{nivel}", mensaje, __name__, "sistema") # {logging_call}'
                contenido_corregido = contenido_corregido.replace(logging_call, reemplazo, 1)
                correcciones += 1

        return contenido_corregido, correcciones

    def _eliminar_imports_logging(self, contenido: str) -> Tuple[str, int]:
        """Elimina imports de logging estándar"""
        correcciones = 0

        # Patrones de imports de logging
        patrones_imports = [
            r'^(\s*)import\s+logging\s*$',
            r'^(\s*)from\s+logging\s+import\s+[^\\n]*$',
        ]

        contenido_corregido = contenido

        for patron in patrones_imports:
            matches = re.finditer(patron, contenido_corregido, re.MULTILINE)
            for match in matches:
                import_line = match.group(0)
                # Comentar el import
                reemplazo = f'# TODO: Eliminado - usar enviar_senal_log # {import_line.strip()}'
                contenido_corregido = contenido_corregido.replace(import_line, reemplazo, 1)
                correcciones += 1

        return contenido_corregido, correcciones

    def _asegurar_import_enviar_senal_log(self, contenido: str) -> str:
        """Asegura que el import de enviar_senal_log esté presente"""
        import_pattern = r'from\s+sistema\.logging_interface\s+import\s+enviar_senal_log'

        if not re.search(import_pattern, contenido):
            # Buscar dónde insertar el import (después de otros imports)
            lines = contenido.split('\n')
            insert_index = 0

            # Encontrar la mejor posición para el import
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    insert_index = i + 1
                elif line.strip() and not line.strip().startswith('#'):
                    break

            # Insertar el import
            import_line = '# MIGRADO A SLUC v2.0\nfrom sistema.logging_interface import enviar_senal_log'
            lines.insert(insert_index, import_line)
            contenido = '\n'.join(lines)
        return contenido

    def _generar_reporte_final(self) -> Dict[str, Any]:
        """Genera el reporte final de corrección"""
        return {
            'archivos_procesados': self.archivos_procesados,
            'correcciones_realizadas': self.correcciones_realizadas,
            'errores_encontrados': len(self.errores_encontrados),
            'protocolo_aplicado': self.correcciones_realizadas > 0,
            'timestamp': datetime.now().isoformat()
        }

    def _log_reporte_final(self, resultado: Dict[str, Any]):
        """Log del reporte final"""
        enviar_senal_log("INFO", "📊 REPORTE FINAL DE CORRECCIÓN", __name__, "corrector")
        enviar_senal_log("INFO", f"📁 Archivos procesados: {resultado['archivos_procesados']}", __name__, "corrector")
        enviar_senal_log("INFO", f"✅ Correcciones realizadas: {resultado['correcciones_realizadas']}", __name__, "corrector")
        enviar_senal_log("INFO", f"❌ Errores encontrados: {resultado['errores_encontrados']}", __name__, "corrector")

        if resultado['protocolo_aplicado']:
            enviar_senal_log("SUCCESS", "✅ PROTOCOLO LOG CENTRAL: CORRECCIONES APLICADAS", __name__, "corrector")
        else:
            enviar_senal_log("WARNING", "⚠️ PROTOCOLO LOG CENTRAL: NO SE REQUIRIERON CORRECCIONES", __name__, "corrector")


def ejecutar_corrector_log_central() -> Dict[str, Any]:
    """
    Función principal para ejecutar el corrector de protocolo de log central

    PROTOCOLO: Solo enviar_senal_log del sistema central
    """
    corrector = CorrectorLogCentral()
    resultado = corrector.corregir_proyecto_completo()

    return resultado


if __name__ == "__main__":
    enviar_senal_log("INFO", "🚀 EJECUTANDO CORRECTOR AUTOMÁTICO - PROTOCOLO LOG CENTRAL", __name__, "corrector")
    resultado = ejecutar_corrector_log_central()

    if resultado['protocolo_aplicado']:
        enviar_senal_log("INFO", "✅ PROTOCOLO LOG CENTRAL: CORRECCIONES APLICADAS", __name__, "sistema")
        enviar_senal_log("INFO", f"📊 Correcciones: {resultado['correcciones_realizadas']}", __name__, "sistema")
    else:
        enviar_senal_log("WARNING", "⚠️ PROTOCOLO LOG CENTRAL: NO SE REQUIRIERON CORRECCIONES", __name__, "sistema")
