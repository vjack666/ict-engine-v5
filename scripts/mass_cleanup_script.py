from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
"""
🧹 MASS CLEANUP SCRIPT - FASE 2
==============================
Limpieza automática de imports no utilizados y duplicados
"""

import os
import re
from pathlib import Path
from typing import List, Set, Tuple

class MassCleanup:
    """Limpieza masiva automática y segura"""

    def __init__(self):
        self.stats = {
            'files_processed': 0,
            'unused_imports_removed': 0,
            'duplicate_imports_removed': 0,
            'constant_redefinitions_fixed': 0,
            'files_modified': 0
        }

        # Imports que NUNCA debemos remover (pueden ser dinámicos)
        self.protected_imports = {
            'enviar_senal_log', 'logging_interface', 'mt5', 'MetaTrader5',
            'textual', 'rich', 'pandas', 'numpy', 'datetime', 'json'
        }

    def process_all_files(self) -> dict:
        """Procesa todos los archivos Python del proyecto"""
        enviar_senal_log("INFO", "🧹 INICIANDO LIMPIEZA MASIVA...", "mass_cleanup_script", "migration")
        enviar_senal_log("INFO", "=" * 40, "mass_cleanup_script", "migration")

        python_files = list(Path('.').rglob('*.py'))
        total_files = len(python_files)

        enviar_senal_log("INFO", f"📁 Archivos Python encontrados: {total_files}", "mass_cleanup_script", "migration")

        for i, file_path in enumerate(python_files, 1):
            if self._should_skip_file(file_path):
                continue

            enviar_senal_log("INFO", f"🔄 [{i:3d}/{total_files}] {file_path.name}", end=' ', "mass_cleanup_script", "migration")

            try:
                modified = self._process_single_file(file_path)
                if modified:
                    enviar_senal_log("INFO", "✅ MODIFICADO", "mass_cleanup_script", "migration")
                    self.stats['files_modified'] += 1
                else:
                    enviar_senal_log("INFO", "⚪ Sin cambios", "mass_cleanup_script", "migration")

                self.stats['files_processed'] += 1

            except Exception as e:
                enviar_senal_log("ERROR", f"❌ ERROR: {e}", "mass_cleanup_script", "migration")

        return self.stats

    def _should_skip_file(self, file_path: Path) -> bool:
        """Archivos que no deben ser procesados"""
        skip_patterns = [
            '__pycache__', '.git', '.vscode', 'venv', 'env',
            '.pytest_cache', 'node_modules', '.mypy_cache'
        ]

        # Archivos específicos que pueden ser delicados
        skip_files = [
            'fix_jsondecode_error.py',
            'mass_cleanup_script.py',
            'quick_fixes.py'
        ]

        str_path = str(file_path)

        # Saltar patrones de directorio
        if any(pattern in str_path for pattern in skip_patterns):
            return True

        # Saltar archivos específicos
        if file_path.name in skip_files:
            return True

        return False

    def _process_single_file(self, file_path: Path) -> bool:
        """Procesa un archivo individual"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except UnicodeDecodeError:
            # Intentar con encoding diferente
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    original_content = f.read()
            except:
                return False
        except Exception:
            return False

        modified_content = original_content
        file_modified = False

        # 1. Remover imports duplicados
        modified_content, duplicates_removed = self._remove_duplicate_imports(modified_content)
        if duplicates_removed > 0:
            self.stats['duplicate_imports_removed'] += duplicates_removed
            file_modified = True

        # 2. Remover imports obviamente no utilizados
        modified_content, unused_removed = self._remove_obvious_unused_imports(modified_content, file_path)
        if unused_removed > 0:
            self.stats['unused_imports_removed'] += unused_removed
            file_modified = True

        # 3. Fix constant redefinitions
        modified_content, constants_fixed = self._fix_constant_redefinitions(modified_content)
        if constants_fixed > 0:
            self.stats['constant_redefinitions_fixed'] += constants_fixed
            file_modified = True

        # Escribir cambios si hubo modificaciones
        if file_modified:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                return True
            except Exception:
                return False

        return False

    def _remove_duplicate_imports(self, content: str) -> Tuple[str, int]:
        """Remueve imports duplicados"""
        lines = content.split('\n')
        seen_imports = set()
        filtered_lines = []
        duplicates_count = 0

        for line in lines:
            stripped = line.strip()

            # Solo procesar líneas de import
            if stripped.startswith('import ') or stripped.startswith('from '):
                if stripped not in seen_imports:
                    seen_imports.add(stripped)
                    filtered_lines.append(line)
                else:
                    # Es un duplicado, no agregarlo
                    duplicates_count += 1
            else:
                filtered_lines.append(line)

        return '\n'.join(filtered_lines), duplicates_count

    def _remove_obvious_unused_imports(self, content: str, file_path: Path) -> Tuple[str, int]:
        """Remueve imports obviamente no utilizados"""
        lines = content.split('\n')
        imports_to_check = []
        non_import_content = ""

        # Separar imports del resto del contenido
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('import ') and not stripped.startswith('import os') and not stripped.startswith('import sys'):
                # Solo imports simples como "import logging"
                if ' as ' not in stripped and ',' not in stripped:
                    imports_to_check.append((line, stripped))
                else:
                    non_import_content += line + '\n'
            else:
                non_import_content += line + '\n'

        removed_count = 0
        final_lines = []

        for original_line, import_statement in imports_to_check:
            # Extraer el nombre del módulo
            module_name = import_statement.replace('import ', '').strip()

            # Verificar si es un import protegido
            if any(protected in module_name for protected in self.protected_imports):
                final_lines.append(original_line)
                continue

            # Solo remover imports muy obvios que no se usan
            obvious_unused = ['logging', 'tempfile', 'unittest']

            if module_name in obvious_unused:
                # Verificar si realmente no se usa
                if not self._is_module_used(non_import_content, module_name):
                    removed_count += 1
                    continue  # No agregar esta línea

            final_lines.append(original_line)

        # Reconstruir contenido
        all_lines = []
        import_index = 0

        for line in content.split('\n'):
            stripped = line.strip()
            if stripped.startswith('import ') and ' as ' not in stripped and ',' not in stripped:
                if any(protected in stripped for protected in self.protected_imports):
                    all_lines.append(line)
                elif stripped.replace('import ', '').strip() in ['logging', 'tempfile', 'unittest']:
                    module_name = stripped.replace('import ', '').strip()
                    if self._is_module_used(non_import_content, module_name):
                        all_lines.append(line)
                    # Si no se usa, no se agrega (se remueve)
                else:
                    all_lines.append(line)
            else:
                all_lines.append(line)

        return '\n'.join(all_lines), removed_count

    def _is_module_used(self, content: str, module_name: str) -> bool:
        """Verifica si un módulo es usado en el contenido"""
        patterns = [
            rf'\b{module_name}\.',  # module.something
            rf'\b{module_name}\s*\(',  # module(
            rf'={module_name}\b',  # = module
        ]

        for pattern in patterns:
            if re.search(pattern, content):
                return True
        return False

    def _fix_constant_redefinitions(self, content: str) -> Tuple[str, int]:
        """Comenta redefiniciones de constantes"""
        lines = content.split('\n')
        seen_constants = set()
        fixed_count = 0

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Buscar definiciones de constantes (MAYÚSCULAS = valor)
            if re.match(r'^[A-Z_]+\s*=', stripped):
                constant_name = stripped.split('=')[0].strip()

                if constant_name in seen_constants:
                    # Comentar redefinición
                    lines[i] = f"# {line}  # Constant redefinition"
                    fixed_count += 1
                else:
                    seen_constants.add(constant_name)

        return '\n'.join(lines), fixed_count

    def print_summary(self):
        """Imprime resumen de la limpieza"""
        enviar_senal_log("INFO", "\n🎯 RESUMEN DE LIMPIEZA MASIVA:", "mass_cleanup_script", "migration")
        enviar_senal_log("INFO", "=" * 35, "mass_cleanup_script", "migration")
        enviar_senal_log("INFO", f"📁 Archivos procesados: {self.stats['files_processed']}", "mass_cleanup_script", "migration")
        enviar_senal_log("INFO", f"📝 Archivos modificados: {self.stats['files_modified']}", "mass_cleanup_script", "migration")
        enviar_senal_log("INFO", f"🗑️  Imports duplicados removidos: {self.stats['duplicate_imports_removed']}", "mass_cleanup_script", "migration")
        enviar_senal_log("INFO", f"🧹 Imports no utilizados removidos: {self.stats['unused_imports_removed']}", "mass_cleanup_script", "migration")
        enviar_senal_log("INFO", f"🔧 Redefiniciones de constantes: {self.stats['constant_redefinitions_fixed']}", "mass_cleanup_script", "migration")

        total_fixes = (self.stats['duplicate_imports_removed'] +
                      self.stats['unused_imports_removed'] +
                      self.stats['constant_redefinitions_fixed'])

        enviar_senal_log("INFO", f"\n✅ TOTAL DE FIXES APLICADOS: {total_fixes}", "mass_cleanup_script", "migration")

def main():
    """Función principal"""
    enviar_senal_log("INFO", "🧹 MASS CLEANUP - FASE 2 DEL PLAN HÍBRIDO", "mass_cleanup_script", "migration")
    enviar_senal_log("INFO", "=" * 50, "mass_cleanup_script", "migration")

    cleanup = MassCleanup()

    # Procesar todos los archivos
    stats = cleanup.process_all_files()

    # Mostrar resumen
    cleanup.print_summary()

    enviar_senal_log("INFO", "\n✅ FASE 2 COMPLETADA", "mass_cleanup_script", "migration")
    enviar_senal_log("INFO", "➡️  Listo para Fase 3: Fixes Manuales Críticos", "mass_cleanup_script", "migration")

if __name__ == "__main__":
    main()
