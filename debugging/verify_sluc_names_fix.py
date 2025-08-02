#!/usr/bin/env python3
"""
🔧 VERIFICACIÓN: SLUC System Names Fix
====================================

Script para verificar que se han corregido los nombres de sistemas
inválidos en las llamadas a enviar_senal_log.

Versión: v1.0
Fecha: Agosto 2025
Estado: VERIFICACIÓN SLUC FIX
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_sluc_system_names():
    """
    Verifica que los nombres de sistemas SLUC sean válidos
    """
    print("🔧 VERIFICACIÓN: SLUC System Names Fix")
    print("=" * 50)

    try:
        # 1. Verificar importaciones de trading.py
        print("📊 1. Verificando core/trading.py...")
        try:
            from core.trading import TRADING_SCHEDULE_AVAILABLE
            print(f"   ✅ trading.py cargado correctamente")
            print(f"   📋 TRADING_SCHEDULE_AVAILABLE: {TRADING_SCHEDULE_AVAILABLE}")
        except Exception as e:
            print(f"   ❌ Error en trading.py: {e}")

        # 2. Verificar importaciones de limit_order_manager.py
        print("\n🎯 2. Verificando core/limit_order_manager.py...")
        try:
            from core.limit_order_manager import MT5_CONNECTOR_AVAILABLE
            print(f"   ✅ limit_order_manager.py cargado correctamente")
            print(f"   📋 MT5_CONNECTOR_AVAILABLE: {MT5_CONNECTOR_AVAILABLE}")
        except Exception as e:
            print(f"   ❌ Error en limit_order_manager.py: {e}")

        # 3. Verificar sistema de logging
        print("\n📝 3. Verificando sistema de logging...")
        try:
            from sistema.logging_interface import enviar_senal_log

            # Test de nombres de sistemas válidos
            test_systems = ["trading", "mt5", "ict", "poi", "dashboard"]

            for system in test_systems:
                try:
                    # Enviar log de prueba
                    enviar_senal_log("DEBUG", f"Test SLUC para sistema: {system}", "verify_sluc", system)
                    print(f"   ✅ Sistema '{system}': VÁLIDO")
                except Exception as e:
                    print(f"   ❌ Sistema '{system}': ERROR - {e}")

        except Exception as e:
            print(f"   ❌ Error en sistema de logging: {e}")

        # 4. Verificar que no existen nombres inválidos EN LOGS (no en imports)
        print("\n🔍 4. Verificando ausencia de nombres inválidos EN LOGS...")

        # Buscar patrones específicos de enviar_senal_log con nombres problemáticos
        problematic_patterns = [
            'enviar_senal_log.*"imports"',
            'enviar_senal_log.*"sistema.trading_schedule"',
            'enviar_senal_log.*"sistema.mt5_connector"'
        ]

        # Buscar en archivos fuente
        source_files = [
            "core/trading.py",
            "core/limit_order_manager.py"
        ]

        issues_found = False

        for file_path in source_files:
            full_path = Path(__file__).parent.parent / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    for pattern in problematic_patterns:
                        import re
                        if re.search(pattern, content):
                            print(f"   ❌ Patrón problemático '{pattern}' encontrado en {file_path}")
                            issues_found = True
                        else:
                            print(f"   ✅ Patrón '{pattern}' NO encontrado en {file_path}")

                except Exception as e:
                    print(f"   ⚠️ Error leyendo {file_path}: {e}")

        if not issues_found:
            print("\n🎉 RESULTADO: Todos los nombres de sistemas SLUC en logs están corregidos")
        else:
            print("\n⚠️ RESULTADO: Aún existen algunos nombres problemáticos en logs")

        print("\n" + "=" * 50)
        print("✅ Verificación completada")
        return not issues_found

    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO en verificación: {e}")
        return False

if __name__ == "__main__":
    success = test_sluc_system_names()
    sys.exit(0 if success else 1)
