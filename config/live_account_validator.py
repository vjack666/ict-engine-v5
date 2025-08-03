"""
🚀 VALIDADOR DE TIPO DE CUENTA MT5 - LIVE ONLY
==============================================

Sistema para detectar y validar el tipo de cuenta MT5:
- Cuenta Demo (detección y alerta)
- Cuenta Real (validación y procesamientoo)
- Cuenta de Prueba de Fondeo (detección y configuración especial)

El sistema SIEMPRE trabaja con datos reales de MT5, independientemente
del tipo de cuenta, pero adapta su comportamiento según el tipo detectado.

Autor: Sistema Sentinel Grid
Fecha: 2025-08-03
Versión: Live Account Validator v1.0
"""

from typing import Dict, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import MetaTrader5 as mt5

class AccountType(Enum):
    """Tipos de cuenta MT5 detectables"""
    DEMO = "demo"
    REAL = "real"
    CONTEST = "contest"  # Pruebas de fondeo
    UNKNOWN = "unknown"

@dataclass
class AccountInfo:
    """Información detallada de la cuenta MT5"""
    account_type: AccountType
    account_number: int
    server_name: str
    broker: str
    currency: str
    balance: float
    equity: float
    margin_level: float
    is_funded_account: bool
    is_prop_firm: bool
    trade_allowed: bool
    expert_allowed: bool

class LiveAccountValidator:
    """Validador de tipo de cuenta para sistema Live-Only"""

    def __init__(self):
        self.account_info: Optional[AccountInfo] = None
        self.last_validation: Optional[datetime] = None
        self.validation_interval = 300  # 5 minutos

    def detect_account_type(self) -> Tuple[AccountType, Dict[str, Any]]:
        """
        Detecta el tipo de cuenta MT5 conectada

        Returns:
            Tuple con el tipo de cuenta y información adicional
        """
        if not mt5.initialize():
            return AccountType.UNKNOWN, {"error": "MT5 no inicializado"}

        try:
            account_info = mt5.account_info()
            if not account_info:
                return AccountType.UNKNOWN, {"error": "No se pudo obtener info de cuenta"}

            # Información básica de la cuenta
            account_data = {
                "login": account_info.login,
                "server": account_info.server,
                "name": account_info.name,
                "company": account_info.company,
                "currency": account_info.currency,
                "balance": account_info.balance,
                "equity": account_info.equity,
                "margin_level": account_info.margin_level,
                "trade_allowed": account_info.trade_allowed,
                "trade_expert": account_info.trade_expert
            }

            # Detectar tipo de cuenta basado en múltiples factores
            account_type = self._classify_account_type(account_info)

            # Información adicional específica del tipo
            additional_info = self._get_additional_account_info(account_info, account_type)

            return account_type, {**account_data, **additional_info}

        except Exception as e:
            return AccountType.UNKNOWN, {"error": f"Error detectando cuenta: {str(e)}"}

    def _classify_account_type(self, account_info) -> AccountType:
        """Clasifica el tipo de cuenta basado en la información de MT5"""

        # Verificar si es cuenta demo
        if hasattr(account_info, 'trade_mode') and account_info.trade_mode == 0:
            return AccountType.DEMO

        # Verificar por nombre del servidor (patrones comunes)
        server_name = account_info.server.lower()

        # Patrones de servidores demo
        demo_patterns = ['demo', 'test', 'practice', 'trial']
        if any(pattern in server_name for pattern in demo_patterns):
            return AccountType.DEMO

        # Patrones de servidores de contest/fondeo
        contest_patterns = ['contest', 'competition', 'challenge', 'funded', 'prop']
        if any(pattern in server_name for pattern in contest_patterns):
            return AccountType.CONTEST

        # Verificar por compañía (prop firms conocidas)
        company = account_info.company.lower()
        prop_firms = ['fundednext', 'ftmo', 'myfundedfx', 'the5ers', 'topsteptrader']
        if any(firm in company for firm in prop_firms):
            return AccountType.CONTEST

        # Si no es demo ni contest, asumir real
        return AccountType.REAL

    def _get_additional_account_info(self, account_info, account_type: AccountType) -> Dict[str, Any]:
        """Obtiene información adicional específica del tipo de cuenta"""

        additional = {
            "account_type": account_type.value,
            "is_demo": account_type == AccountType.DEMO,
            "is_real": account_type == AccountType.REAL,
            "is_funded_challenge": account_type == AccountType.CONTEST,
            "requires_special_handling": account_type in [AccountType.DEMO, AccountType.CONTEST]
        }

        # Información específica para cuentas de fondeo
        if account_type == AccountType.CONTEST:
            additional.update({
                "prop_firm_detected": True,
                "risk_management_strict": True,
                "max_daily_loss_monitoring": True,
                "challenge_mode": True
            })

        # Información para cuentas demo
        elif account_type == AccountType.DEMO:
            additional.update({
                "demo_account_warning": True,
                "simulated_environment": True,
                "live_data_real_execution_simulated": True
            })

        # Información para cuentas reales
        elif account_type == AccountType.REAL:
            additional.update({
                "real_money_trading": True,
                "full_risk_exposure": True,
                "live_execution": True
            })

        return additional

    def validate_account_for_live_trading(self) -> Dict[str, Any]:
        """Valida si la cuenta es apropiada para trading live"""

        account_type, account_data = self.detect_account_type()

        validation_result = {
            "account_type": account_type.value,
            "suitable_for_live_trading": False,
            "warnings": [],
            "recommendations": [],
            "account_data": account_data
        }

        # Validación específica por tipo de cuenta
        if account_type == AccountType.REAL:
            validation_result.update({
                "suitable_for_live_trading": True,
                "risk_level": "HIGH",
                "real_money_exposure": True
            })

        elif account_type == AccountType.CONTEST:
            validation_result.update({
                "suitable_for_live_trading": True,
                "risk_level": "CONTROLLED",
                "prop_firm_rules_apply": True,
                "warnings": ["Cuenta de fondeo detectada - aplicar reglas estrictas de riesgo"]
            })

        elif account_type == AccountType.DEMO:
            validation_result.update({
                "suitable_for_live_trading": False,
                "risk_level": "NONE",
                "simulated_environment": True,
                "warnings": ["CUENTA DEMO DETECTADA - Sin exposición real al mercado"],
                "recommendations": [
                    "Cambiar a cuenta real para trading live",
                    "Usar solo para testing y desarrollo"
                ]
            })

        else:  # UNKNOWN
            validation_result.update({
                "suitable_for_live_trading": False,
                "risk_level": "UNKNOWN",
                "warnings": ["Tipo de cuenta no identificado"],
                "recommendations": ["Verificar conexión MT5 y tipo de cuenta"]
            })

        return validation_result

    def get_live_trading_config(self) -> Dict[str, Any]:
        """Obtiene configuración optimizada basada en el tipo de cuenta"""

        validation = self.validate_account_for_live_trading()
        account_type = AccountType(validation["account_type"])

        base_config = {
            "data_source": "MT5_LIVE",  # Siempre datos reales
            "real_time_data": True,
            "account_type": account_type.value
        }

        # Configuración específica por tipo de cuenta
        if account_type == AccountType.REAL:
            return {
                **base_config,
                "risk_management": "STANDARD",
                "position_sizing": "NORMAL",
                "max_risk_per_trade": 2.0,
                "max_daily_loss": 5.0,
                "trading_enabled": True,
                "auto_trading": True
            }

        elif account_type == AccountType.CONTEST:
            return {
                **base_config,
                "risk_management": "STRICT",
                "position_sizing": "CONSERVATIVE",
                "max_risk_per_trade": 1.0,
                "max_daily_loss": 3.0,
                "drawdown_monitoring": True,
                "prop_firm_rules": True,
                "trading_enabled": True,
                "auto_trading": True
            }

        elif account_type == AccountType.DEMO:
            return {
                **base_config,
                "risk_management": "RELAXED",
                "position_sizing": "TESTING",
                "max_risk_per_trade": 5.0,
                "max_daily_loss": 10.0,
                "trading_enabled": False,  # Solo análisis
                "auto_trading": False,
                "testing_mode": True
            }

        else:  # UNKNOWN
            return {
                **base_config,
                "risk_management": "DISABLED",
                "trading_enabled": False,
                "auto_trading": False,
                "error_mode": True
            }

    def continuous_validation(self) -> bool:
        """Validación continua del tipo de cuenta"""
        current_time = datetime.now()

        # Verificar si necesita revalidación
        if (self.last_validation and
            (current_time - self.last_validation).total_seconds() < self.validation_interval):
            return True

        # Realizar nueva validación
        try:
            account_type, account_data = self.detect_account_type()

            # Actualizar información de cuenta
            self.account_info = AccountInfo(
                account_type=account_type,
                account_number=account_data.get('login', 0),
                server_name=account_data.get('server', ''),
                broker=account_data.get('company', ''),
                currency=account_data.get('currency', ''),
                balance=account_data.get('balance', 0.0),
                equity=account_data.get('equity', 0.0),
                margin_level=account_data.get('margin_level', 0.0),
                is_funded_account=account_data.get('is_funded_challenge', False),
                is_prop_firm=account_data.get('prop_firm_detected', False),
                trade_allowed=account_data.get('trade_allowed', False),
                expert_allowed=account_data.get('trade_expert', False)
            )

            self.last_validation = current_time
            return True

        except Exception:
            return False

# Instancia global del validador
live_account_validator = LiveAccountValidator()

def get_account_validator() -> LiveAccountValidator:
    """Obtiene la instancia del validador de cuenta"""
    return live_account_validator

def quick_account_check() -> str:
    """Verificación rápida del tipo de cuenta"""
    validator = get_account_validator()
    account_type, _ = validator.detect_account_type()
    return account_type.value

def is_account_suitable_for_live() -> bool:
    """Verifica si la cuenta es adecuada para trading live"""
    validator = get_account_validator()
    validation = validator.validate_account_for_live_trading()
    return validation["suitable_for_live_trading"]

if __name__ == "__main__":
    # Demo del validador
    validator = LiveAccountValidator()

    print("🔍 VALIDADOR DE CUENTA MT5 - LIVE ONLY")
    print("=" * 50)

    account_type, account_data = validator.detect_account_type()
    print(f"Tipo de Cuenta: {account_type.value.upper()}")
    print(f"Número: {account_data.get('login', 'N/A')}")
    print(f"Servidor: {account_data.get('server', 'N/A')}")
    print(f"Broker: {account_data.get('company', 'N/A')}")

    validation = validator.validate_account_for_live_trading()
    print(f"\n✅ Apropiada para Live: {validation['suitable_for_live_trading']}")

    if validation.get('warnings'):
        print("\n⚠️ Advertencias:")
        for warning in validation['warnings']:
            print(f"  - {warning}")
