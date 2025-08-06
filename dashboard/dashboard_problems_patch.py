#!/usr/bin/env python3
"""
🔧 ITC ENGINE v5.0 - PATCH INTEGRACIÓN DASHBOARD PROBLEMAS
==========================================================

🎯 OBJETIVO: Integrar automáticamente la pestaña "🚨 Problemas" en el
            dashboard principal sin modificar manualmente el código

📊 CARACTERÍSTICAS:
   - ✅ Integración automática sin edición manual
   - ✅ Detección del dashboard principal
   - ✅ Inserción de código limpia
   - ✅ Backup automático
   - ✅ Validación de integridad

🔧 FUNCIONALIDAD:
   - Detecta dashboard_definitivo.py
   - Localiza sección de pestañas
   - Inserta código de integración
   - Valida funcionamiento

📅 Fecha: 2025-08-06 | Versión: 1.0.0
👤 Autor: ITC Engine v5.0 System
"""

# MIGRACIÓN SIC v3.0 + SLUC v2.1
from sistema.sic import enviar_senal_log, log_info, log_warning

from sistema.sic import os
from sistema.sic import sys
from sistema.sic import re
import shutil
from sistema.sic import Path
from sistema.sic import datetime
from sistema.sic import Optional, Tuple, List, Dict, Any
import ast
import importlib.util

# Configuración
WORKSPACE_ROOT = Path(__file__).parent.parent
DASHBOARD_FILE = WORKSPACE_ROOT / "dashboard" / "dashboard_definitivo.py"
PROBLEMS_RENDERER = WORKSPACE_ROOT / "dashboard" / "problems_tab_renderer.py"
BACKUP_DIR = WORKSPACE_ROOT / "docs" / "bitacoras" / "backups"


class DashboardPatcher:
    """🔧 Patcher automático para integrar pestaña de problemas"""

    def __init__(self):
        self.dashboard_path = DASHBOARD_FILE
        self.problems_renderer_path = PROBLEMS_RENDERER
        self.backup_dir = BACKUP_DIR
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def apply_patch(self) -> Tuple[bool, str]:
        """🚀 Aplicar patch completo"""
        try:
            # 1. Validar prerequisitos
            success, message = self._validate_prerequisites()
            if not success:
                return False, message

            # 2. Crear backup
            backup_path = self._create_backup()
            print(f"💾 Backup creado: {backup_path}")

            # 3. Analizar dashboard actual
            success, message = self._analyze_dashboard_structure()
            if not success:
                return False, message

            # 4. Aplicar modificaciones
            success, message = self._apply_modifications()
            if not success:
                # Restaurar backup en caso de error
                self._restore_backup(backup_path)
                return False, f"Error aplicando patch: {message}"

            # 5. Validar integridad
            success, message = self._validate_integration()
            if not success:
                self._restore_backup(backup_path)
                return False, f"Validación fallida: {message}"

            return True, "✅ Patch aplicado exitosamente"

        except Exception as e:
            return False, f"❌ Error inesperado: {str(e)}"

    def _validate_prerequisites(self) -> Tuple[bool, str]:
        """🔍 Validar prerequisitos"""
        # Verificar archivos
        if not self.dashboard_path.exists():
            return False, f"Dashboard no encontrado: {self.dashboard_path}"

        if not self.problems_renderer_path.exists():
            return False, f"Renderer no encontrado: {self.problems_renderer_path}"

        # Verificar que dashboard sea válido Python
        try:
            with open(self.dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()
            ast.parse(content)
        except SyntaxError as e:
            return False, f"Dashboard tiene errores de sintaxis: {e}"

        return True, "Prerequisitos OK"

    def _create_backup(self) -> Path:
        """💾 Crear backup del dashboard"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"dashboard_definitivo_backup_{timestamp}.py"
        shutil.copy2(self.dashboard_path, backup_file)
        return backup_file

    def _analyze_dashboard_structure(self) -> Tuple[bool, str]:
        """🔍 Analizar estructura del dashboard"""
        try:
            with open(self.dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Buscar patrones de pestañas existentes
            tab_patterns = [
                r'def.*tab.*\(',
                r'if.*selected_tab.*==',
                r'tab_.*=.*st\.',
                r'st\.tabs?\(',
            ]

            found_patterns = []
            for pattern in tab_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    found_patterns.extend(matches)

            if not found_patterns:
                return False, "No se encontraron patrones de pestañas en el dashboard"

            print(f"📊 Patrones de pestañas encontrados: {len(found_patterns)}")
            return True, "Estructura analizada"

        except Exception as e:
            return False, f"Error analizando estructura: {str(e)}"

    def _apply_modifications(self) -> Tuple[bool, str]:
        """🔧 Aplicar modificaciones al dashboard"""
        try:
            with open(self.dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 1. Agregar import si no existe
            content = self._add_import_if_needed(content)

            # 2. Detectar y modificar sección de pestañas
            content = self._modify_tabs_section(content)

            # 3. Agregar función de renderizado si no existe
            content = self._add_render_function_if_needed(content)

            # Escribir archivo modificado
            with open(self.dashboard_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True, "Modificaciones aplicadas"

        except Exception as e:
            return False, f"Error aplicando modificaciones: {str(e)}"

    def _add_import_if_needed(self, content: str) -> str:
        """📦 Agregar import del renderer si no existe"""
        import_line = "from dashboard.problems_tab_renderer import render_problems_tab_simple, get_problems_summary"

        if "problems_tab_renderer" not in content:
            # Buscar lugar apropiado para insert (después de otros imports)
            lines = content.split('\n')
            insert_index = 0

            # Buscar el último import
            for i, line in enumerate(lines):
                if line.strip().startswith(('import ', 'from ')) and not line.strip().startswith('#'):
                    insert_index = i + 1

            lines.insert(insert_index, import_line)
            content = '\n'.join(lines)
            print("📦 Import agregado")

        return content

    def _modify_tabs_section(self, content: str) -> str:
        """🎨 Modificar sección de pestañas"""
        # Buscar patrones comunes de pestañas en Streamlit

        # Patrón 1: st.tabs([...])
        tab_list_pattern = r'st\.tabs\(\[(.*?)\]\)'
        match = re.search(tab_list_pattern, content, re.DOTALL)

        if match:
            current_tabs = match.group(1)
            if "🚨 Problemas" not in current_tabs:
                # Agregar nueva pestaña a la lista
                new_tabs = current_tabs.rstrip().rstrip(',') + ', "🚨 Problemas"'
                content = content.replace(match.group(1), new_tabs)
                print("🎨 Pestaña agregada a st.tabs()")

                # Agregar lógica de renderizado
                content = self._add_tab_logic(content)

        # Patrón 2: Pestañas manuales con if/elif
        elif "selected_tab" in content and "==" in content:
            content = self._add_manual_tab_logic(content)

        return content

    def _add_tab_logic(self, content: str) -> str:
        """🎯 Agregar lógica de pestaña de problemas"""
        # Buscar el último elif o if de pestañas
        tab_logic_pattern = r'(elif.*tab.*==.*:.*?\n(?:.*?\n)*?)(?=elif|if|def|\Z)'
        matches = list(re.finditer(tab_logic_pattern, content, re.DOTALL | re.IGNORECASE))

        if matches:
            last_match = matches[-1]

            # Insertar nueva lógica después del último match
            new_logic = '''
elif "🚨 Problemas" in str(tab):
    try:
        st.subheader("🚨 Sistema de Detección de Errores")

        # Mostrar resumen
        col1, col2, col3, col4 = st.columns(4)

        try:
            summary = get_problems_summary()
            with col1:
                st.metric("Total Problemas", summary.get('total_problems', 0))
            with col2:
                st.metric("Críticos", summary.get('critical_count', 0))
            with col3:
                st.metric("Altos", summary.get('high_count', 0))
            with col4:
                if summary.get('stats', {}).get('files_analyzed'):
                    st.metric("Archivos", summary['stats']['files_analyzed'])
        except Exception as e:
            st.warning(f"Error cargando resumen: {str(e)}")

        # Mostrar contenido principal
        st.markdown("---")
        try:
            problems_content = render_problems_tab_simple()
            st.text(problems_content)
        except Exception as e:
            st.error(f"Error renderizando problemas: {str(e)}")
            st.markdown("**🔧 Sugerencias:**")
            st.markdown("- Ejecutar detección manual: `python scripts/error_detection/error_detector.py`")
            st.markdown("- Verificar que el sistema esté configurado correctamente")

        # Botones de acción
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔄 Refrescar Datos"):
                st.rerun()

        with col2:
            if st.button("🔍 Ejecutar Detección"):
                with st.spinner("Ejecutando detección..."):
                    try:
                        from dashboard.problems_tab_renderer import execute_detection
                        result = execute_detection(quick_mode=True)
                        if result['status'] == 'success':
                            st.success("✅ Detección completada")
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {result.get('message', 'Error desconocido')}")
                    except Exception as e:
                        st.error(f"❌ Error ejecutando detección: {str(e)}")

        with col3:
            if st.button("📊 Ver Estadísticas"):
                try:
                    summary = get_problems_summary()
                    st.json(summary.get('stats', {}))
                except Exception as e:
                    st.error(f"Error mostrando estadísticas: {str(e)}")

    except Exception as e:
        st.error(f"❌ Error en pestaña Problemas: {str(e)}")
        st.markdown("**🛠️ Solución:**")
        st.code("python scripts/ejecutar_deteccion_errores.ps1 -Dashboard")
'''

            insert_pos = last_match.end()
            content = content[:insert_pos] + new_logic + content[insert_pos:]
            print("🎯 Lógica de pestaña agregada")

        return content

    def _add_manual_tab_logic(self, content: str) -> str:
        """🎯 Agregar lógica manual para pestañas"""
        # Para dashboards que usan selectbox u otro método
        # Buscar patrón de selección manual
        if "selectbox" in content and "tab" in content:
            # Buscar las opciones del selectbox
            selectbox_pattern = r'selectbox\([^,]+,\s*\[(.*?)\]'
            match = re.search(selectbox_pattern, content, re.DOTALL)

            if match and "🚨 Problemas" not in match.group(1):
                current_options = match.group(1)
                new_options = current_options.rstrip().rstrip(',') + ', "🚨 Problemas"'
                content = content.replace(match.group(1), new_options)

                # Agregar lógica correspondiente
                content = self._add_tab_logic(content)

        return content

    def _add_render_function_if_needed(self, content: str) -> str:
        """🔧 Agregar función de renderizado si es necesaria"""
        # Verificar si ya existe una función de renderizado
        if "def render_problems" not in content:
            # Agregar función helper al final del archivo
            helper_function = '''

def render_problems_section():
    """🚨 Renderizar sección de problemas (función helper)"""
    try:
        from dashboard.problems_tab_renderer import render_problems_tab_simple, get_problems_summary

        st.subheader("🚨 Sistema de Detección de Errores")

        # Resumen ejecutivo
        summary = get_problems_summary()
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Problemas", summary.get('total_problems', 0))
        with col2:
            st.metric("Críticos", summary.get('critical_count', 0))
        with col3:
            st.metric("Archivos Analizados", summary.get('stats', {}).get('files_analyzed', 0))

        # Contenido principal
        st.markdown("---")
        problems_content = render_problems_tab_simple()
        st.text(problems_content)

        return True

    except Exception as e:
        st.error(f"Error renderizando problemas: {str(e)}")
        return False
'''
            content += helper_function
            print("🔧 Función helper agregada")

        return content

    def _validate_integration(self) -> Tuple[bool, str]:
        """✅ Validar que la integración sea correcta"""
        try:
            # Verificar sintaxis
            with open(self.dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()

            ast.parse(content)

            # Verificar que contenga los elementos necesarios
            required_elements = [
                "problems_tab_renderer",
                "🚨 Problemas",
                "render_problems_tab_simple"
            ]

            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)

            if missing_elements:
                return False, f"Elementos faltantes: {missing_elements}"

            print("✅ Validación sintáctica OK")
            print("✅ Elementos requeridos presentes")

            return True, "Integración validada"

        except SyntaxError as e:
            return False, f"Error de sintaxis después del patch: {e}"
        except Exception as e:
            return False, f"Error validando integración: {str(e)}"

    def _restore_backup(self, backup_path: Path):
        """🔄 Restaurar backup"""
        try:
            shutil.copy2(backup_path, self.dashboard_path)
            print(f"🔄 Backup restaurado desde: {backup_path}")
        except Exception as e:
            print(f"❌ Error restaurando backup: {str(e)}")

    def show_integration_status(self) -> Dict[str, Any]:
        """📊 Mostrar estado de integración"""
        try:
            with open(self.dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()

            status = {
                'file_exists': self.dashboard_path.exists(),
                'has_import': 'problems_tab_renderer' in content,
                'has_tab': '🚨 Problemas' in content,
                'has_logic': 'render_problems_tab_simple' in content,
                'syntax_valid': False
            }

            try:
                ast.parse(content)
                status['syntax_valid'] = True
            except:
                pass

            return status

        except Exception as e:
            return {'error': str(e)}


def apply_dashboard_patch() -> bool:
    """🚀 Función principal para aplicar patch"""
    patcher = DashboardPatcher()

    print("🔧 INICIANDO PATCH INTEGRACIÓN DASHBOARD")
    print("=" * 50)

    # Mostrar estado actual
    status = patcher.show_integration_status()
    print("📊 Estado actual:")
    for key, value in status.items():
        print(f"   {key}: {value}")
    print()

    # Aplicar patch
    success, message = patcher.apply_patch()

    print(f"\n📋 Resultado: {message}")

    if success:
        print("\n✅ INTEGRACIÓN COMPLETADA")
        print("🎯 La pestaña '🚨 Problemas' está ahora disponible en el dashboard")
        print("🚀 Ejecute el dashboard para ver los cambios")
    else:
        print("\n❌ INTEGRACIÓN FALLIDA")
        print("🔧 Revisar errores y intentar nuevamente")

    return success


def check_integration_status():
    """📊 Verificar estado de integración"""
    patcher = DashboardPatcher()
    status = patcher.show_integration_status()

    print("📊 ESTADO DE INTEGRACIÓN DASHBOARD")
    print("=" * 40)

    for key, value in status.items():
        emoji = "✅" if value else "❌"
        print(f"{emoji} {key}: {value}")

    # Evaluación general
    if all(status.get(k, False) for k in ['file_exists', 'has_import', 'has_tab', 'syntax_valid']):
        print("\n🎉 INTEGRACIÓN COMPLETA Y FUNCIONAL")
    else:
        print("\n⚠️ INTEGRACIÓN INCOMPLETA - ejecutar apply_dashboard_patch()")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="🔧 Patch Dashboard Problemas")
    parser.add_argument("--apply", action="store_true", help="Aplicar patch")
    parser.add_argument("--status", action="store_true", help="Mostrar estado")

    args = parser.parse_args()

    if args.apply:
        apply_dashboard_patch()
    elif args.status:
        check_integration_status()
    else:
        print("Uso: python dashboard_problems_patch.py --apply | --status")
