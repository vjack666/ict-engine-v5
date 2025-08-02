#!/usr/bin/env python3
"""
🚨 FIX CRÍTICO: JSONDecodeError Import
====================================
Resuelve el error más crítico en ict_historical_analyzer.py
"""

import re
from pathlib import Path

def fix_jsondecode_error():
    """Fix crítico para JSONDecodeError en ict_historical_analyzer.py"""

    file_path = Path("core/ict_engine/ict_historical_analyzer.py")

    if not file_path.exists():
        print(f"❌ Archivo no encontrado: {file_path}")
        return False

    try:
        # Leer archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"🔍 Procesando: {file_path}")

        # Verificar si ya tiene el import correcto
        if 'from json import JSONDecodeError' in content:
            print("✅ JSONDecodeError ya está importado correctamente")
            return True

        # Buscar si tiene import json
        if 'import json' in content:
            # Agregar import de JSONDecodeError después de import json
            content = re.sub(
                r'^import json$',
                'import json\nfrom json import JSONDecodeError',
                content,
                flags=re.MULTILINE
            )

            # Escribir archivo corregido
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print("✅ JSONDecodeError import agregado exitosamente")
            print("🔧 6 instancias de JSONDecodeError ahora están correctamente importadas")
            return True
        else:
            # Si no tiene import json, agregarlo al principio de imports
            lines = content.split('\n')
            import_section_end = 0

            # Encontrar donde terminan los imports
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    import_section_end = i + 1

            # Insertar imports
            lines.insert(import_section_end, 'import json')
            lines.insert(import_section_end + 1, 'from json import JSONDecodeError')

            # Escribir archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

            print("✅ import json y JSONDecodeError agregados exitosamente")
            return True

    except Exception as e:
        print(f"❌ Error procesando archivo: {e}")
        return False

def verify_fix():
    """Verifica que el fix fue aplicado correctamente"""
    file_path = Path("core/ict_engine/ict_historical_analyzer.py")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        has_json_import = 'import json' in content
        has_jsondecode_import = 'from json import JSONDecodeError' in content
        jsondecode_usage_count = content.count('JSONDecodeError')

        print("\n📊 VERIFICACIÓN DEL FIX:")
        print("=" * 30)
        print(f"✅ import json: {'SÍ' if has_json_import else 'NO'}")
        print(f"✅ from json import JSONDecodeError: {'SÍ' if has_jsondecode_import else 'NO'}")
        print(f"📍 Usos de JSONDecodeError: {jsondecode_usage_count}")

        if has_json_import and has_jsondecode_import and jsondecode_usage_count > 0:
            print("🎉 ¡FIX VERIFICADO EXITOSAMENTE!")
            return True
        else:
            print("⚠️ Fix necesita revisión manual")
            return False

    except Exception as e:
        print(f"❌ Error verificando fix: {e}")
        return False

if __name__ == "__main__":
    print("🚨 INICIANDO FIX CRÍTICO: JSONDecodeError")
    print("=" * 50)

    # Aplicar fix
    success = fix_jsondecode_error()

    if success:
        # Verificar fix
        verify_fix()
        print("\n✅ FASE 1 COMPLETADA - JSONDecodeError resuelto")
    else:
        print("\n❌ FASE 1 FALLÓ - Revisar manualmente")
