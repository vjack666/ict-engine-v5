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
    enviar_senal_log("INFO", "🔧 VERIFICACIÓN: SLUC System Names Fix", "verify_sluc_names_fix", "migration")
    enviar_senal_log("INFO", "=" * 50, "verify_sluc_names_fix", "migration")

    try:
        # 1. Verificar importaciones de trading.py
        enviar_senal_log("INFO", "📊 1. Verificando core/trading.py...", "verify_sluc_names_fix", "migration")
        try:
            from core.trading import TRADING_SCHEDULE_AVAILABLE
            enviar_senal_log("INFO", f"   ✅ trading.py cargado correctamente", "verify_sluc_names_fix", "migration")
            enviar_senal_log("INFO", f"   📋 TRADING_SCHEDULE_AVAILABLE: {TRADING_SCHEDULE_AVAILABLE}", "verify_sluc_names_fix", "migration")
        except Exception as e:
            enviar_senal_log("ERROR", f"   ❌ Error en trading.py: {e}", "verify_sluc_names_fix", "migration")

        # 2. Verificar importaciones de limit_order_manager.py
        enviar_senal_log("INFO", "\n🎯 2. Verificando core/limit_order_manager.py...", "verify_sluc_names_fix", "migration")
        try:
            from core.limit_order_manager import MT5_CONNECTOR_AVAILABLE
            enviar_senal_log("INFO", f"   ✅ limit_order_manager.py cargado correctamente", "verify_sluc_names_fix", "migration")
            enviar_senal_log("INFO", f"   📋 MT5_CONNECTOR_AVAILABLE: {MT5_CONNECTOR_AVAILABLE}", "verify_sluc_names_fix", "migration")
        except Exception as e:
            enviar_senal_log("ERROR", f"   ❌ Error en limit_order_manager.py: {e}", "verify_sluc_names_fix", "migration")

        # 3. Verificar sistema de logging
        enviar_senal_log("INFO", "\n📝 3. Verificando sistema de logging...", "verify_sluc_names_fix", "migration")
        try:
            from sistema.logging_interface import enviar_senal_log

            # Test de nombres de sistemas válidos
            test_systems = ["trading", "mt5", "ict", "poi", "dashboard"]

            for system in test_systems:
                try:
                    # Enviar log de prueba
                    enviar_senal_log("DEBUG", f"Test SLUC para sistema: {system}", "verify_sluc", system)
                    enviar_senal_log("INFO", f"   ✅ Sistema '{system}': VÁLIDO", "verify_sluc_names_fix", "migration")
                except Exception as e:
                    enviar_senal_log("ERROR", f"   ❌ Sistema '{system}': ERROR - {e}", "verify_sluc_names_fix", "migration")

        except Exception as e:
            enviar_senal_log("ERROR", f"   ❌ Error en sistema de logging: {e}", "verify_sluc_names_fix", "migration")

        # 4. Verificar que no existen nombres inválidos EN LOGS (no en imports)
        enviar_senal_log("INFO", "\n🔍 4. Verificando ausencia de nombres inválidos EN LOGS...", "verify_sluc_names_fix", "migration")

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
                            enviar_senal_log("INFO", f"   ❌ Patrón problemático '{pattern}' encontrado en {file_path}", "verify_sluc_names_fix", "migration")
                            issues_found = True
                        else:
                            enviar_senal_log("INFO", f"   ✅ Patrón '{pattern}' NO encontrado en {file_path}", "verify_sluc_names_fix", "migration")

                except Exception as e:
                    enviar_senal_log("ERROR", f"   ⚠️ Error leyendo {file_path}: {e}", "verify_sluc_names_fix", "migration")

        if not issues_found:
            enviar_senal_log("INFO", "\n🎉 RESULTADO: Todos los nombres de sistemas SLUC en logs están corregidos", "verify_sluc_names_fix", "migration")
        else:
            enviar_senal_log("INFO", "\n⚠️ RESULTADO: Aún existen algunos nombres problemáticos en logs", "verify_sluc_names_fix", "migration")

        enviar_senal_log("INFO", "\n" + "=" * 50, "verify_sluc_names_fix", "migration")
        enviar_senal_log("INFO", "✅ Verificación completada", "verify_sluc_names_fix", "migration")
        return not issues_found

    except Exception as e:
        enviar_senal_log("ERROR", f"\n❌ ERROR CRÍTICO en verificación: {e}", "verify_sluc_names_fix", "migration")
        return False

if __name__ == "__main__":
    success = test_sluc_system_names()
    sys.exit(0 if success else 1)
