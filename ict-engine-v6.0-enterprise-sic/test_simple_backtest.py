#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 ICT Backtest Simple Test v6.0
===============================

Test básico y rápido del sistema de backtesting

Autor: ICT Engine v6.0 Enterprise Team
Fecha: Agosto 7, 2025
"""

from datetime import datetime, timedelta
from core.backtesting.backtest_engine import BacktestEngine, BacktestConfig

def test_simple_backtest():
    """Test básico del backtest engine"""
    print("🧪 ICT Backtest Simple Test v6.0")
    print("=" * 50)
    
    # Configuración mínima
    config = BacktestConfig(
        symbol="EURUSD",
        primary_timeframe="M15",
        start_date=datetime.now() - timedelta(days=3),
        end_date=datetime.now(),
        initial_balance=10000.0,
        risk_per_trade=1.0,
        max_positions=1,
        enable_smart_money=False,
        enable_multi_timeframe=False
    )
    
    print(f"📊 Config: {config.symbol} {config.primary_timeframe}")
    print(f"💰 Balance: ${config.initial_balance:,.2f}")
    print(f"🎯 Risk: {config.risk_per_trade}%")
    
    try:
        # Inicializar engine
        engine = BacktestEngine(config)
        print("✅ Engine inicializado")
        
        # Ejecutar backtest
        results = engine.run_backtest()
        print("✅ Backtest ejecutado")
        
        # Mostrar resultados básicos
        print("\n📈 RESULTADOS:")
        print(f"   Total PnL: ${results.total_pnl:.2f}")
        print(f"   Total Trades: {results.total_trades}")
        print(f"   Win Rate: {results.win_rate:.1%}")
        print(f"   Max Drawdown: ${results.max_drawdown:.2f}")
        
        if results.total_trades > 0:
            print("🎉 ¡Test exitoso! El sistema funciona")
        else:
            print("⚠️ No se generaron trades (normal para datos cortos)")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_simple_backtest()
    exit(0 if success else 1)
