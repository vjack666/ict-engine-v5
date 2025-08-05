# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log
"""
🚀 WIDGET DE STATUS DE CUENTA - LIVE ONLY
========================================

Widget especializado para mostrar el tipo de cuenta MT5 y su configuración
en el dashboard principal. Detecta automáticamente:
- Cuenta Demo (con advertencias)
- Cuenta Real (con confirmación)
- Cuenta de Fondeo (con reglas especiales)

Autor: Sistema Sentinel Grid
Fecha: 2025-08-03
Versión: Account Status Widget v1.0
"""

from typing import Dict, Any, Optional
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.table import Table
from rich.console import Console
from datetime import datetime

# Importación condicional para evitar errores en demo
try:
    from config.live_account_validator import get_account_validator, AccountType
except ImportError:
    # Para cuando se ejecuta directamente
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from config.live_account_validator import get_account_validator, AccountType

class AccountStatusWidget:
    """Widget para mostrar el status de la cuenta MT5"""

    def __init__(self):
        self.validator = get_account_validator()
        self.last_update = None
        self.cached_info = None

    def create_account_status_panel(self, mt5_manager=None) -> Panel:
        """Crea el panel de status de cuenta"""

        # Obtener información de cuenta
        account_info = self._get_account_info(mt5_manager)

        # Crear contenido del panel
        content = self._create_account_content(account_info)

        # Determinar estilo del panel basado en tipo de cuenta
        panel_style = self._get_panel_style(account_info.get("account_type"))

        return Panel(
            content,
            title=f"🏦 STATUS DE CUENTA MT5 - {account_info.get('account_type', 'UNKNOWN').upper()}",
            border_style=panel_style,
            expand=False
        )

    def _get_account_info(self, mt5_manager=None) -> Dict[str, Any]:
        """Obtiene información actualizada de la cuenta"""

        try:
            if mt5_manager and hasattr(mt5_manager, 'get_account_info'):
                return mt5_manager.get_account_info()
            else:
                # Usar validador directamente
                validation = self.validator.validate_account_for_live_trading()
                config = self.validator.get_live_trading_config()

                # Combinar información de validación y configuración
                combined_info = {
                    "account_type": validation.get("account_type", "unknown"),
                    "suitable_for_live": validation.get("suitable_for_live_trading", False),
                    "risk_level": validation.get("risk_level", "UNKNOWN"),
                    "warnings": validation.get("warnings", []),
                    "recommendations": validation.get("recommendations", []),
                    "config": {
                        "risk_management": config.get("risk_management", "N/A"),
                        "position_sizing": config.get("position_sizing", "N/A"),
                        "max_risk_per_trade": config.get("max_risk_per_trade", 0),
                        "trading_enabled": config.get("trading_enabled", False),
                        "auto_trading": config.get("auto_trading", False)
                    },
                    "account_data": validation.get("account_data", {})
                }
                return combined_info
        except Exception as e:
            return {
                "account_type": "error",
                "error": str(e),
                "suitable_for_live": False,
                "risk_level": "UNKNOWN",
                "warnings": [f"Error al obtener información: {str(e)}"],
                "config": {}
            }

    def _create_account_content(self, account_info: Dict[str, Any]) -> Text:
        """Crea el contenido del widget de cuenta"""

        content = Text()
        account_type = account_info.get("account_type", "unknown")

        # Header con tipo de cuenta
        if account_type == "demo":
            content.append("🔶 CUENTA DEMO DETECTADA\n", style="bold yellow")
            content.append("└─ Datos reales, ejecución simulada\n", style="yellow")

        elif account_type == "real":
            content.append("💰 CUENTA REAL ACTIVA\n", style="bold green")
            content.append("└─ Trading en vivo habilitado\n", style="green")

        elif account_type == "contest":
            content.append("🏆 CUENTA DE FONDEO\n", style="bold blue")
            content.append("└─ Reglas de prop firm aplicadas\n", style="blue")

        else:
            content.append("❓ TIPO DE CUENTA DESCONOCIDO\n", style="bold red")
            content.append("└─ Verificar conexión MT5\n", style="red")

        content.append("\n")

        # Información de trading
        suitable = account_info.get("suitable_for_live", False)
        if suitable:
            content.append("✅ Apropiada para trading live\n", style="green")
        else:
            content.append("❌ NO apropiada para trading live\n", style="red")

        # Risk level
        risk_level = account_info.get("risk_level", "UNKNOWN")
        risk_colors = {
            "NONE": "gray",
            "LOW": "green",
            "CONTROLLED": "blue",
            "STANDARD": "yellow",
            "HIGH": "red",
            "UNKNOWN": "gray"
        }
        content.append(f"🎯 Nivel de riesgo: {risk_level}\n", style=risk_colors.get(risk_level, "gray"))

        # Configuración específica
        config = account_info.get("config", {})
        if config:
            content.append("\n📋 CONFIGURACIÓN:\n", style="bold")

            # Risk management
            risk_mgmt = config.get("risk_management", "N/A")
            content.append(f"  • Risk Management: {risk_mgmt}\n")

            # Position sizing
            pos_sizing = config.get("position_sizing", "N/A")
            content.append(f"  • Position Sizing: {pos_sizing}\n")

            # Max risk per trade
            max_risk = config.get("max_risk_per_trade", 0)
            content.append(f"  • Riesgo máximo/trade: {max_risk}%\n")

            # Trading enabled
            trading_enabled = config.get("trading_enabled", False)
            if trading_enabled:
                content.append("  • Trading: ✅ HABILITADO\n", style="green")
            else:
                content.append("  • Trading: ❌ DESHABILITADO\n", style="red")

        # Advertencias
        warnings = account_info.get("warnings", [])
        if warnings:
            content.append("\n⚠️ ADVERTENCIAS:\n", style="bold yellow")
            for warning in warnings:
                content.append(f"  • {warning}\n", style="yellow")

        # Timestamp
        content.append(f"\n🕐 Actualizado: {datetime.now().strftime('%H:%M:%S')}", style="dim")

        return content

    def _get_panel_style(self, account_type: Optional[str]) -> str:
        """Determina el estilo del panel basado en el tipo de cuenta"""

        style_mapping = {
            "demo": "yellow",
            "real": "green",
            "contest": "blue",
            "error": "red",
            "unknown": "gray"
        }

        # Manejar el caso None
        if account_type is None:
            account_type = "unknown"

        return style_mapping.get(account_type, "white")

    def create_compact_status(self, mt5_manager=None) -> str:
        """Crea un status compacto para mostrar en otras partes del dashboard"""

        account_info = self._get_account_info(mt5_manager)
        account_type = account_info.get("account_type", "unknown")
        suitable = account_info.get("suitable_for_live", False)

        # Emojis por tipo de cuenta
        type_emojis = {
            "demo": "🔶",
            "real": "💰",
            "contest": "🏆",
            "error": "❌",
            "unknown": "❓"
        }

        emoji = type_emojis.get(account_type, "❓")
        status = "LIVE" if suitable else "DISABLED"

        return f"{emoji} {account_type.upper()} ({status})"

    def get_account_metrics(self, mt5_manager=None) -> Dict[str, Any]:
        """Obtiene métricas de cuenta para el dashboard"""

        account_info = self._get_account_info(mt5_manager)

        return {
            "account_type": account_info.get("account_type", "unknown"),
            "suitable_for_live": account_info.get("suitable_for_live", False),
            "risk_level": account_info.get("risk_level", "UNKNOWN"),
            "trading_enabled": account_info.get("config", {}).get("trading_enabled", False),
            "warnings_count": len(account_info.get("warnings", [])),
            "status_emoji": self._get_status_emoji(account_info),
            "last_check": datetime.now().isoformat()
        }

    def _get_status_emoji(self, account_info: Dict[str, Any]) -> str:
        """Obtiene emoji de status basado en la información de cuenta"""

        account_type = account_info.get("account_type", "unknown")
        suitable = account_info.get("suitable_for_live", False)

        if account_type == "real" and suitable:
            return "💰✅"
        elif account_type == "contest" and suitable:
            return "🏆✅"
        elif account_type == "demo":
            return "🔶⚠️"
        else:
            return "❌❓"

# Instancia global del widget
account_status_widget = AccountStatusWidget()

def get_account_status_widget() -> AccountStatusWidget:
    """Obtiene la instancia del widget de status de cuenta"""
    return account_status_widget

def create_account_panel(mt5_manager=None) -> Panel:
    """Función de conveniencia para crear el panel de cuenta"""
    widget = get_account_status_widget()
    return widget.create_account_status_panel(mt5_manager)

def get_compact_account_status(mt5_manager=None) -> str:
    """Función de conveniencia para obtener status compacto"""
    widget = get_account_status_widget()
    return widget.create_compact_status(mt5_manager)

if __name__ == "__main__":
    # Demo del widget
    try:
        console = Console()
        widget = AccountStatusWidget()

        panel = widget.create_account_status_panel()
        console.print(panel)

        print(f"\nStatus compacto: {widget.create_compact_status()}")

        metrics = widget.get_account_metrics()
        print(f"Métricas: {metrics}")

        print("\n✅ Demo del widget ejecutada correctamente")

    except Exception as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error en demo: {e}")
        print("💡 Ejecuta desde el directorio raíz del proyecto: python dashboard/widgets/account_status_widget.py")
