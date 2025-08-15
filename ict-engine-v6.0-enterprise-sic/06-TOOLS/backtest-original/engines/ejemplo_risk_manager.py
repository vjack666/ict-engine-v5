#!/usr/bin/env python3
"""
🎯 Risk Manager v6.0 Enterprise - Ejemplo de Uso
===============================================

Ejemplo completo de uso del Risk Manager adaptativo para ICT Engine v6.0.
Demuestra integración con POI system y Smart Money Concepts.

Autor: ICT Engine v6.0 Enterprise Team
Fecha: 14 Agosto 2025
"""

import sys
import os
from datetime import datetime

# Añadir path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from risk_manager import RiskManager, ICTRiskConfig, RiskAlert
    print("✅ Risk Manager importado correctamente")
except ImportError as e:
    print(f"❌ Error importando Risk Manager: {e}")
    print("Asegúrate de ejecutar desde el directorio correcto")
    sys.exit(1)


def ejemplo_backtesting():
    """Ejemplo de uso para backtesting"""
    print("\n🔙 EJEMPLO BACKTESTING")
    print("=" * 50)
    
    # Configuración para backtesting
    risk_manager = RiskManager(
        max_risk_per_trade=0.02,  # 2% riesgo por trade
        max_positions=5,
        mode='backtest'
    )
    
    # Cálculo básico de position size
    position_size = risk_manager.calculate_position_size(
        account_balance=10000,
        entry_price=1.0850,
        stop_loss=1.0820
    )
    
    print(f"💰 Balance: $10,000")
    print(f"📈 Entry: 1.0850")
    print(f"🛑 Stop Loss: 1.0820")
    print(f"📊 Position Size: {position_size} lots")
    
    # Verificar si se puede operar
    can_trade = risk_manager.can_open_position(
        current_positions=2,
        current_drawdown=0.08,
        daily_loss=0.02
    )
    
    print(f"✅ Puede operar: {'Sí' if can_trade else 'No'}")
    

def ejemplo_trading_live():
    """Ejemplo de uso para trading live con ICT"""
    print("\n🔴 EJEMPLO TRADING LIVE CON ICT")
    print("=" * 50)
    
    # Configuración ICT específica
    ict_config = ICTRiskConfig(
        poi_weight_factor=1.3,
        smart_money_factor=1.2,
        correlation_threshold=0.75
    )
    
    # Risk Manager para trading live
    risk_manager = RiskManager(
        max_risk_per_trade=0.015,  # 1.5% riesgo (más conservador en live)
        max_positions=3,
        ict_config=ict_config,
        mode='live'
    )
    
    # Position sizing con factores ICT
    position_size = risk_manager.calculate_ict_position_size(
        account_balance=25000,
        entry_price=1.0850,
        stop_loss=1.0820,
        poi_quality='A',           # POI de alta calidad
        smart_money_signal=True,   # Confirmación Smart Money
        session='overlap'          # London-NY overlap
    )
    
    print(f"💰 Balance: $25,000")
    print(f"🎯 POI Quality: A (alta calidad)")
    print(f"🧠 Smart Money Signal: Confirmado")
    print(f"🕐 Session: London-NY Overlap")
    print(f"📊 Position Size ICT: {position_size} lots")
    
    # Verificación completa de riesgo
    risk_status = risk_manager.check_risk_limits(
        current_positions=1,
        current_drawdown=0.05,
        daily_loss=0.01
    )
    
    print(f"\n🚦 ESTADO DE RIESGO:")
    print(f"✅ Puede operar: {'Sí' if risk_status['can_trade'] else 'No'}")
    print(f"⚠️  Warnings: {len(risk_status['warnings'])}")
    print(f"🚨 Critical Alerts: {len(risk_status['critical_alerts'])}")
    

def ejemplo_alertas():
    """Ejemplo de sistema de alertas"""
    print("\n🚨 EJEMPLO SISTEMA DE ALERTAS")
    print("=" * 50)
    
    # Callback para manejar alertas
    def manejar_alerta(alert: RiskAlert):
        timestamp_str = alert.timestamp.strftime("%H:%M:%S")
        print(f"[{timestamp_str}] {alert.alert_type}: {alert.message}")
        print(f"    Valor actual: {alert.current_value:.4f}")
        print(f"    Umbral: {alert.threshold_value:.4f}")
        print(f"    Acción recomendada: {alert.recommended_action}")
        print()
    
    # Configurar Risk Manager con alertas
    risk_manager = RiskManager(
        max_risk_per_trade=0.02,
        max_positions=2,  # Límite bajo para demo
        max_drawdown_percent=0.10,  # 10% máximo drawdown
        mode='live'
    )
    
    # Añadir callback de alertas
    risk_manager.add_alert_callback(manejar_alerta)
    
    print("📝 Simulando situaciones de riesgo...")
    
    # Simular situación que dispara alertas
    risk_status = risk_manager.check_risk_limits(
        current_positions=3,        # Excede límite de 2
        current_drawdown=0.12,      # Excede 10%
        daily_loss=0.02            # Dentro del límite
    )
    
    # Mostrar resultados
    print(f"📊 RESULTADO DE VERIFICACIÓN:")
    print(f"✅ Puede operar: {'Sí' if risk_status['can_trade'] else 'No'}")
    print(f"🚨 Alertas críticas: {risk_status['critical_alerts']}")
    

def ejemplo_export_reporte():
    """Ejemplo de exportación de reporte"""
    print("\n📊 EJEMPLO EXPORTACIÓN REPORTE")
    print("=" * 50)
    
    # Configurar Risk Manager
    risk_manager = RiskManager(
        max_risk_per_trade=0.02,
        max_positions=5,
        mode='live'
    )
    
    # Simular algunos datos históricos
    risk_manager.update_daily_pnl(150.0)
    risk_manager.update_daily_pnl(-80.0)
    risk_manager.update_daily_pnl(220.0)
    risk_manager.update_daily_pnl(-45.0)
    risk_manager.update_daily_pnl(180.0)
    
    # Exportar reporte
    filename = risk_manager.export_risk_report()
    
    if filename:
        print(f"✅ Reporte exportado: {filename}")
        print("📁 El reporte incluye:")
        print("   - Configuración actual")
        print("   - Métricas de riesgo")
        print("   - Historial de alertas")
        print("   - Performance metrics")
    else:
        print("❌ Error exportando reporte")


def main():
    """Función principal - ejecuta todos los ejemplos"""
    print("🎯 RISK MANAGER v6.0 ENTERPRISE - EJEMPLOS DE USO")
    print("=" * 60)
    print(f"⏰ Ejecutado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    try:
        ejemplo_backtesting()
        ejemplo_trading_live()
        ejemplo_alertas()
        ejemplo_export_reporte()
        
        print("\n✅ TODOS LOS EJEMPLOS EJECUTADOS CORRECTAMENTE")
        print("🎉 Risk Manager v6.0 Enterprise está funcionando perfectamente!")
        
    except Exception as e:
        print(f"\n❌ ERROR EN EJEMPLOS: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
