#!/usr/bin/env python3
"""
📋 VALIDACIÓN REGLA #5 - VERIFICAR ACTUALIZACIÓN COMPLETA
========================================================

Verifica que la REGLA #5 se aplicó correctamente en TODOS los documentos
"""

import os
from pathlib import Path

def main():
    print("🔍 VALIDANDO APLICACIÓN COMPLETA DE REGLA #5")
    print("=" * 50)
    
    current_dir = Path(__file__).parent.parent
    docs_dir = current_dir / "docs"
    
    # Encontrar archivos .md
    md_files = []
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)
    
    print(f"📄 Verificando {len(md_files)} archivos .md")
    
    # Verificar archivos con FASE 2 documentada
    files_with_phase2 = 0
    files_without_phase2 = []
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "FASE 2 COMPLETADO" in content:
                files_with_phase2 += 1
            else:
                files_without_phase2.append(str(md_file.relative_to(current_dir)))
                
        except Exception as e:
            print(f"❌ Error leyendo {md_file.name}: {e}")
    
    # Verificar plan principal
    plan_file = docs_dir / "04-development-logs" / "memoria" / "MEMORIA_TRADER_REAL_PLAN_COMPLETO.md"
    plan_updated = False
    
    if plan_file.exists():
        try:
            with open(plan_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "[x] ✅ FASE 2: Sistema Memoria Unificada v6.0 (COMPLETADA)" in content:
                plan_updated = True
                
        except Exception as e:
            print(f"❌ Error leyendo plan: {e}")
    
    # Resultados
    print(f"\n📊 RESULTADOS VALIDACIÓN REGLA #5:")
    print(f"   📄 Total archivos .md: {len(md_files)}")
    print(f"   ✅ Con FASE 2 documentada: {files_with_phase2}")
    print(f"   ❌ Sin FASE 2 documentada: {len(files_without_phase2)}")
    print(f"   🎯 Plan principal actualizado: {'✅' if plan_updated else '❌'}")
    
    if files_without_phase2:
        print(f"\n⚠️ Archivos faltantes:")
        for file in files_without_phase2:
            print(f"   - {file}")
    
    # Validación final
    if files_with_phase2 == len(md_files) and plan_updated:
        print(f"\n🏆 REGLA #5 APLICADA COMPLETAMENTE ✅")
        print(f"   ✅ TODOS los documentos actualizados")
        print(f"   ✅ Plan principal marcado como COMPLETADO")
        print(f"   ✅ FASE 2 documentada en 100% de archivos")
        return True
    else:
        print(f"\n❌ REGLA #5 NO APLICADA COMPLETAMENTE")
        print(f"   📊 Cobertura: {(files_with_phase2/len(md_files)*100):.1f}%")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
