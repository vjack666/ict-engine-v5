#!/usr/bin/env python3
"""
Validador de Log Central - PROTOCOLO OBLIGATORIO
===============================================

REGLA DIRECTA: "Al añadir cualquier log o sistema de seguridad y errores → AL SISTEMA LOG CENTRAL"

Este script verifica automáticamente que:
1. No existan imports duplicados de logging
2. Solo se use enviar_senal_log del sistema central
3. No se usen prints para logging
4. Todos los logs vayan al sistema centralizado SLUC v2.0

Autor: ICT Engine v5.0 - Sistema de Validación Automática
"""

# MIGRACIÓN SIC v3.0 + SLUC v2.1
from sistema.sic import enviar_senal_log, log_info, log_warning

from sistema.sic import os
from sistema.sic import re
from sistema.sic import sys
from sistema.sic import Path
from sistema.sic import List, Dict, Any, Optional
from sistema.sic import datetime

# Añadir el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent.parent))

# PROTOCOLO: Solo sistema de log centralizado
from sistema.sic import enviar_senal_log

class ValidadorLogCentral:
    """
    Validador automático del protocolo de logging centralizado

    MISIÓN: Garantizar que TODOS los logs vayan al sistema central
    """

    def __init__(self, ruta_proyecto: str = "."):
        self.ruta_proyecto = Path(ruta_proyecto).resolve()
        self.errores_encontrados: List[Dict[str, Any]] = []
        self.archivos_validados = 0
        self.violaciones_protocolo = 0

        # ARCHIVOS DE INFRAESTRUCTURA (EXENTOS DE VALIDACIÓN)
        self.archivos_excepcion = {
            'sistema/logging_interface.py',  # Sistema central de logging
            'sistema/smart_directory_logger.py',  # Logger especializado
            'utils/logging_utils.py',  # Utilidades de logging
            'migrate_sluc_atomic.py',  # Migrador con código de ejemplo
            'scripts/validador_log_central.py',  # Este mismo validador
            'scripts/corrector_log_central.py'  # Corrector de logging
        }

        # Patrones PROHIBIDOS (violaciones del protocolo)
        self.patrones_prohibidos = {
            'import_logging': r'^(\s*)import\s+logging',
            'from_logging': r'^(\s*)from\s+logging\s+import',
            'print_logging': r'print\s*\([^)]*(?:error|warning|info|debug|log)[^)]*\)',
            # REMOVED: 'reimport_enviar_senal' - Este causa falsos positivos
            'log_direct': r'(?:log|logging)\.[a-zA-Z]+\(',
            'logger_creation': r'logger\s*=\s*(?:logging\.getLogger|Logger)'
        }

        # Patrones OBLIGATORIOS (protocolo correcto)
        self.patrones_obligatorios = {
            'enviar_senal_log_usage': r'enviar_senal_log\s*\(',
            'sistema_logging_import': r'from\s+sistema\.logging_interface\s+import\s+enviar_senal_log'
        }

        self.log_inicial()

    def log_inicial(self):
        """Log inicial del validador"""
        enviar_senal_log("INFO", "🔍 INICIANDO VALIDACIÓN DE PROTOCOLO LOG CENTRAL", __name__, "validacion")
        enviar_senal_log("INFO", f"📁 Proyecto: {self.ruta_proyecto}", __name__, "validacion")
        enviar_senal_log("INFO", "📋 REGLA: Solo enviar_senal_log del sistema central", __name__, "validacion")

    def validar_proyecto_completo(self) -> Dict[str, Any]:
        """
        Validación completa del proyecto

        Returns:
            Diccionario con resultados de la validación
        """
        enviar_senal_log("INFO", "🔍 INICIANDO VALIDACIÓN COMPLETA DEL PROTOCOLO", __name__, "validacion")

        archivos_python = self._buscar_archivos_python()

        for archivo in archivos_python:
            self._validar_archivo(archivo)

        resultado = self._generar_reporte_final()
        self._log_reporte_final(resultado)

        return resultado

    def _buscar_archivos_python(self) -> List[Path]:
        """Busca todos los archivos Python del proyecto"""
        archivos = []

        # Directorios a validar (excluir __pycache__, .git, etc.)
        directorios_validar = [
            'core', 'dashboard', 'scripts', 'sistema', 'utils',
            'config', 'debugging', 'utilities'
        ]

        for directorio in directorios_validar:
            dir_path = self.ruta_proyecto / directorio
            if dir_path.exists():
                archivos.extend(dir_path.rglob('*.py'))

        # Archivos en la raíz
        archivos.extend(self.ruta_proyecto.glob('*.py'))

        return archivos

    def _verificar_imports_duplicados(self, contenido):
        """
        Detecta imports duplicados REALES de enviar_senal_log en el mismo archivo
        Ignora imports dentro de strings o comentarios
        """
        lineas = contenido.split('\n')
        imports_encontrados = []

        for i, linea in enumerate(lineas, 1):
            # Ignorar líneas comentadas
            if linea.strip().startswith('#'):
                continue

            # Buscar el import específico, pero NO dentro de strings
            if re.search(self.patrones_obligatorios['sistema_logging_import'], linea):
                # Verificar que NO esté dentro de una cadena de texto
                # Contar comillas antes del import para detectar si está en string
                pos_import = linea.find('from sistema.logging_interface import enviar_senal_log')
                if pos_import > 0:
                    texto_antes = linea[:pos_import]
                    comillas_simples = texto_antes.count("'") - texto_antes.count("\\'")
                    comillas_dobles = texto_antes.count('"') - texto_antes.count('\\"')

                    # Si hay número impar de comillas, está dentro de un string
                    if comillas_simples % 2 != 0 or comillas_dobles % 2 != 0:
                        continue

                imports_encontrados.append(i)

        # Si hay más de 1 import REAL, reportar como duplicados
        if len(imports_encontrados) > 1:
            return [(f"IMPORT_DUPLICADO", i, lineas[i-1].strip()) for i in imports_encontrados[1:]]

        return []

    def _validar_archivo(self, archivo: Path):
        """Valida un archivo individual"""
        try:
            # VERIFICAR SI EL ARCHIVO ESTÁ EN LA LISTA DE EXCEPCIONES
            archivo_relativo = str(archivo.relative_to(self.ruta_proyecto)).replace('\\', '/')
            if archivo_relativo in self.archivos_excepcion:
                enviar_senal_log("DEBUG", f"⚠️ SALTANDO (Infraestructura): {archivo_relativo}", __name__, "validacion")
                return

            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
                lineas = contenido.split('\n')

            self.archivos_validados += 1
            enviar_senal_log("DEBUG", f"📄 Validando: {archivo.relative_to(self.ruta_proyecto)}", __name__, "validacion")

            # Verificar violaciones del protocolo
            violaciones = self._detectar_violaciones(archivo, lineas)

            if violaciones:
                self.violaciones_protocolo += len(violaciones)
                for violacion in violaciones:
                    self.errores_encontrados.append(violacion)
                    enviar_senal_log("ERROR", f"❌ VIOLACIÓN: {violacion['descripcion']} en {archivo.relative_to(self.ruta_proyecto)}:{violacion['linea']}", __name__, "validacion")

            # Verificar cumplimiento del protocolo
            cumplimiento = self._verificar_cumplimiento(archivo, contenido)
            if cumplimiento['usando_sistema_central']:
                enviar_senal_log("SUCCESS", f"✅ {archivo.relative_to(self.ruta_proyecto)}: Protocolo cumplido", __name__, "validacion")

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error validando {archivo}: {e}", __name__, "validacion")

    def _detectar_violaciones(self, archivo: Path, lineas: List[str]) -> List[Dict[str, Any]]:
        """Detecta violaciones del protocolo de logging"""
        violaciones = []

        # Verificar imports duplicados REALES usando método específico
        contenido = '\n'.join(lineas)
        imports_duplicados = self._verificar_imports_duplicados(contenido)

        for violacion_data in imports_duplicados:
            violaciones.append({
                'tipo': violacion_data[0],
                'archivo': archivo,
                'linea': violacion_data[1],
                'contenido': violacion_data[2],
                'descripcion': 'Import duplicado de enviar_senal_log',
                'severidad': 'ERROR'
            })

        # Detectar otros patrones prohibidos
        for i, linea in enumerate(lineas, 1):
            for patron_nombre, patron_regex in self.patrones_prohibidos.items():
                if re.search(patron_regex, linea, re.IGNORECASE):
                    violaciones.append({
                        'tipo': patron_nombre.upper(),
                        'archivo': archivo,
                        'linea': i,
                        'contenido': linea.strip(),
                        'descripcion': f'Uso prohibido: {patron_nombre}',
                        'severidad': 'ERROR'
                    })

        return violaciones

    def _verificar_cumplimiento(self, archivo: Path, contenido: str) -> Dict[str, bool]:
        """Verifica el cumplimiento del protocolo"""
        return {
            'usando_sistema_central': bool(re.search(self.patrones_obligatorios['enviar_senal_log_usage'], contenido)),
            'import_correcto': bool(re.search(self.patrones_obligatorios['sistema_logging_import'], contenido)),
            'sin_violaciones': len(self._detectar_violaciones(archivo, contenido.split('\n'))) == 0
        }

    def _generar_reporte_final(self) -> Dict[str, Any]:
        """Genera el reporte final de validación"""
        archivos_con_violaciones = len(set(v['archivo'] for v in self.errores_encontrados))

        return {
            'archivos_validados': self.archivos_validados,
            'archivos_con_violaciones': archivos_con_violaciones,
            'total_violaciones': self.violaciones_protocolo,
            'violaciones_por_tipo': self._agrupar_violaciones_por_tipo(),
            'protocolo_cumplido': self.violaciones_protocolo == 0,
            'timestamp': datetime.now().isoformat()
        }

    def _agrupar_violaciones_por_tipo(self) -> Dict[str, int]:
        """Agrupa las violaciones por tipo"""
        conteos = {}
        for violacion in self.errores_encontrados:
            tipo = violacion['tipo']
            conteos[tipo] = conteos.get(tipo, 0) + 1
        return conteos

    def _log_reporte_final(self, resultado: Dict[str, Any]):
        """Log del reporte final"""
        enviar_senal_log("INFO", "📊 REPORTE FINAL DE VALIDACIÓN", __name__, "validacion")
        enviar_senal_log("INFO", f"📁 Archivos validados: {resultado['archivos_validados']}", __name__, "validacion")
        enviar_senal_log("INFO", f"⚠️ Archivos con violaciones: {resultado['archivos_con_violaciones']}", __name__, "validacion")
        enviar_senal_log("INFO", f"🚫 Total violaciones: {resultado['total_violaciones']}", __name__, "validacion")

        if resultado['protocolo_cumplido']:
            enviar_senal_log("SUCCESS", "✅ PROTOCOLO LOG CENTRAL: CUMPLIDO", __name__, "validacion")
        else:
            enviar_senal_log("ERROR", "❌ PROTOCOLO LOG CENTRAL: VIOLACIONES DETECTADAS", __name__, "validacion")

            # Mostrar violaciones por tipo
            for tipo, cantidad in resultado['violaciones_por_tipo'].items():
                enviar_senal_log("WARNING", f"   🔸 {tipo}: {cantidad} violaciones", __name__, "validacion")

    def corregir_violaciones_automaticamente(self) -> bool:
        """
        Corrige automáticamente las violaciones más comunes

        Returns:
            True si se realizaron correcciones
        """
        enviar_senal_log("INFO", "🔧 INICIANDO CORRECCIÓN AUTOMÁTICA", __name__, "validacion")

        correcciones_realizadas = 0

        for violacion in self.errores_encontrados:
            if violacion['tipo'] == 'REIMPORT_DUPLICADO':
                if self._corregir_reimport_duplicado(violacion):
                    correcciones_realizadas += 1

        if correcciones_realizadas > 0:
            enviar_senal_log("SUCCESS", f"✅ {correcciones_realizadas} correcciones realizadas", __name__, "validacion")
            return True
        else:
            enviar_senal_log("INFO", "ℹ️ No se requieren correcciones automáticas", __name__, "validacion")
            return False

    def _corregir_reimport_duplicado(self, violacion: Dict[str, Any]) -> bool:
        """Corrige imports duplicados de enviar_senal_log"""
        try:
            archivo = violacion['archivo']
            enviar_senal_log("INFO", f"🔧 Corrigiendo import duplicado en {archivo.relative_to(self.ruta_proyecto)}", __name__, "validacion")

            # Aquí implementaríamos la lógica de corrección
            # Por ahora solo log del intento
            enviar_senal_log("WARNING", "⚠️ Corrección automática pendiente de implementación", __name__, "validacion")
            return False

        except Exception as e:
            enviar_senal_log("ERROR", f"❌ Error corrigiendo violación: {e}", __name__, "validacion")
            return False


def validar_protocolo_log_central() -> Dict[str, Any]:
    """
    Función principal para validar el protocolo de log central

    PROTOCOLO: Solo enviar_senal_log del sistema central
    """
    validador = ValidadorLogCentral()
    resultado = validador.validar_proyecto_completo()

    # Intentar corregir violaciones automáticamente
    if not resultado['protocolo_cumplido']:
        enviar_senal_log("INFO", "🔧 Intentando corrección automática...", __name__, "validacion")
        validador.corregir_violaciones_automaticamente()

    return resultado


if __name__ == "__main__":
    enviar_senal_log("INFO", "🚀 EJECUTANDO VALIDADOR DE PROTOCOLO LOG CENTRAL", __name__, "validacion")
    resultado = validar_protocolo_log_central()

    if resultado['protocolo_cumplido']:
        enviar_senal_log("INFO", "✅ PROTOCOLO LOG CENTRAL: CUMPLIDO", __name__, "validacion")
    else:
        enviar_senal_log("WARNING", "❌ PROTOCOLO LOG CENTRAL: VIOLACIONES DETECTADAS", __name__, "validacion")
        enviar_senal_log("INFO", f"📊 Violaciones: {resultado['total_violaciones']}", __name__, "validacion")
