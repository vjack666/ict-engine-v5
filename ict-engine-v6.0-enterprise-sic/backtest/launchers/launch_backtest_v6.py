#!/usr/bin/env python3
"""
🚀 BACKTEST LAUNCHER v6.0 ENTERPRISE
===================================

Launcher profesional para el sistema de backtesting ICT Engine v6.0.
Interfaz fácil para ejecutar backtests con diferentes configuraciones.

Autor: ICT Engine v6.0 Enterprise Team
Fecha: 7 de Agosto 2025
"""

import sys
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

# Setup path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def create_backtest_config(config_name: str = "default"):
    """Crear configuración de backtesting personalizada"""
    configs = {
        "conservative": {
            "initial_balance": 10000.0,
            "risk_per_trade": 0.01,
            "min_confidence": 0.75,
            "description": "Configuración conservadora - 1% riesgo, alta confianza"
        },
        "aggressive": {
            "initial_balance": 10000.0,
            "risk_per_trade": 0.03,
            "min_confidence": 0.65,
            "description": "Configuración agresiva - 3% riesgo, confianza estándar"
        },
        "professional": {
            "initial_balance": 50000.0,
            "risk_per_trade": 0.015,
            "min_confidence": 0.70,
            "description": "Configuración profesional - Balance alto, 1.5% riesgo"
        },
        "smart_money_focus": {
            "initial_balance": 25000.0,
            "risk_per_trade": 0.02,
            "min_confidence": 0.65,
            "description": "Enfoque Smart Money - Balance medio, confianza en SM"
        },
        "default": {
            "initial_balance": 10000.0,
            "risk_per_trade": 0.02,
            "min_confidence": 0.65,
            "description": "Configuración por defecto - Balanceada"
        }
    }
    
    return configs.get(config_name, configs["default"])

def run_backtest_with_config(config_name: str, symbol: str, start_date: str, end_date: str, save_results: bool = True):
    """Ejecutar backtest con configuración específica"""
    try:
        from core.backtesting.backtest_engine_v6 import ICTBacktestEngine
        
        # Obtener configuración
        config = create_backtest_config(config_name)
        
        print(f"🚀 INICIANDO BACKTEST ICT ENGINE v6.0")
        print(f"=" * 60)
        print(f"📊 Configuración: {config_name}")
        print(f"📝 Descripción: {config['description']}")
        print(f"💰 Balance inicial: ${config['initial_balance']:,.2f}")
        print(f"🎯 Riesgo por trade: {config['risk_per_trade']:.1%}")
        print(f"⭐ Confianza mínima: {config['min_confidence']:.1%}")
        print(f"📈 Símbolo: {symbol}")
        print(f"📅 Período: {start_date} → {end_date}")
        print(f"=" * 60)
        
        # Crear engine con configuración
        engine = ICTBacktestEngine(
            initial_balance=config['initial_balance'],
            risk_per_trade=config['risk_per_trade']
        )
        
        # Actualizar configuración mínima
        engine.min_confidence = config['min_confidence']
        
        # Ejecutar backtest
        results = engine.run_comprehensive_backtest(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date
        )
        
        # Guardar resultados si se solicita
        if save_results and results.total_trades > 0:
            save_backtest_results(results, config_name, symbol, start_date, end_date)
        
        return results
        
    except Exception as e:
        print(f"❌ Error ejecutando backtest: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_backtest_results(results, config_name: str, symbol: str, start_date: str, end_date: str):
    """Guardar resultados del backtest"""
    try:
        # Crear directorio de resultados
        results_dir = Path("data/backtest_results")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Timestamp para archivo único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backtest_{config_name}_{symbol}_{timestamp}.json"
        
        # Preparar datos para guardar
        save_data = {
            "config": {
                "name": config_name,
                "symbol": symbol,
                "start_date": start_date,
                "end_date": end_date,
                "timestamp": timestamp
            },
            "results": {
                "total_trades": results.total_trades,
                "winning_trades": results.winning_trades,
                "losing_trades": results.losing_trades,
                "win_rate": results.win_rate,
                "total_pnl": results.total_pnl,
                "total_pips": results.total_pips,
                "max_drawdown": results.max_drawdown,
                "profit_factor": results.profit_factor,
                "sharpe_ratio": results.sharpe_ratio,
                "avg_win": results.avg_win,
                "avg_loss": results.avg_loss,
                "largest_win": results.largest_win,
                "largest_loss": results.largest_loss,
                "avg_trade_duration_hours": results.avg_trade_duration.total_seconds() / 3600,
                "pattern_performance": results.pattern_performance,
                "session_performance": results.session_performance,
                "smart_money_performance": results.smart_money_performance
            },
            "trades": [trade.to_dict() for trade in results.trades]
        }
        
        # Guardar archivo
        filepath = results_dir / filename
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=2, default=str)
        
        print(f"\n💾 Resultados guardados en: {filepath}")
        
    except Exception as e:
        print(f"⚠️ Error guardando resultados: {e}")

def run_multiple_configs_comparison(symbol: str, start_date: str, end_date: str):
    """Ejecutar comparación entre múltiples configuraciones"""
    print(f"\n🔄 COMPARACIÓN MÚLTIPLES CONFIGURACIONES")
    print(f"=" * 60)
    
    configs_to_test = ["conservative", "aggressive", "professional", "smart_money_focus"]
    results_comparison = {}
    
    for config_name in configs_to_test:
        print(f"\n🚀 Ejecutando configuración: {config_name}")
        print("-" * 40)
        
        results = run_backtest_with_config(config_name, symbol, start_date, end_date, save_results=False)
        
        if results:
            results_comparison[config_name] = {
                "total_trades": results.total_trades,
                "win_rate": results.win_rate,
                "total_pnl": results.total_pnl,
                "max_drawdown": results.max_drawdown,
                "profit_factor": results.profit_factor,
                "sharpe_ratio": results.sharpe_ratio,
                "smart_money_trades": results.smart_money_performance['smart_money']['total_trades']
            }
    
    # Mostrar comparación
    print(f"\n📊 COMPARACIÓN DE CONFIGURACIONES")
    print(f"=" * 80)
    print(f"{'Config':<18} {'Trades':<8} {'WinRate':<8} {'PnL':<12} {'MaxDD':<10} {'PF':<6} {'Sharpe':<8} {'SM':<6}")
    print(f"-" * 80)
    
    for config, metrics in results_comparison.items():
        print(f"{config:<18} {metrics['total_trades']:<8} {metrics['win_rate']:<7.1%} "
              f"${metrics['total_pnl']:<11,.0f} ${metrics['max_drawdown']:<9,.0f} "
              f"{metrics['profit_factor']:<5.2f} {metrics['sharpe_ratio']:<7.3f} {metrics['smart_money_trades']:<6}")
    
    # Determinar mejor configuración
    if results_comparison:
        best_config = max(results_comparison.items(), 
                         key=lambda x: x[1]['total_pnl'] if x[1]['max_drawdown'] < 2000 else -float('inf'))
        
        print(f"\n🏆 MEJOR CONFIGURACIÓN: {best_config[0]}")
        print(f"   PnL: ${best_config[1]['total_pnl']:,.2f}")
        print(f"   Win Rate: {best_config[1]['win_rate']:.1%}")
        print(f"   Max Drawdown: ${best_config[1]['max_drawdown']:,.2f}")

def create_sample_scenarios():
    """Crear escenarios de prueba predefinidos"""
    scenarios = {
        "quick_test": {
            "symbol": "EURUSD",
            "start_date": "2024-11-01",
            "end_date": "2024-11-30",
            "description": "Test rápido - 1 mes"
        },
        "quarterly": {
            "symbol": "EURUSD",  
            "start_date": "2024-10-01",
            "end_date": "2024-12-31",
            "description": "Test trimestral - Q4 2024"
        },
        "full_year": {
            "symbol": "EURUSD",
            "start_date": "2024-01-01", 
            "end_date": "2024-12-31",
            "description": "Test anual completo - 2024"
        },
        "crisis_period": {
            "symbol": "EURUSD",
            "start_date": "2024-08-01",
            "end_date": "2024-10-31", 
            "description": "Período de alta volatilidad"
        }
    }
    
    return scenarios

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(description="ICT Backtest Engine v6.0 Enterprise Launcher")
    
    parser.add_argument("--config", "-c", default="default", 
                       choices=["conservative", "aggressive", "professional", "smart_money_focus", "default"],
                       help="Configuración de backtesting")
    
    parser.add_argument("--symbol", "-s", default="EURUSD",
                       help="Par de divisas (default: EURUSD)")
    
    parser.add_argument("--start-date", default="2024-10-01",
                       help="Fecha de inicio (YYYY-MM-DD)")
    
    parser.add_argument("--end-date", default="2024-12-31", 
                       help="Fecha de fin (YYYY-MM-DD)")
    
    parser.add_argument("--scenario", 
                       choices=["quick_test", "quarterly", "full_year", "crisis_period"],
                       help="Escenario predefinido")
    
    parser.add_argument("--compare", action="store_true",
                       help="Comparar múltiples configuraciones")
    
    parser.add_argument("--save", action="store_true", default=True,
                       help="Guardar resultados")
    
    args = parser.parse_args()
    
    # Usar escenario si se especifica
    if args.scenario:
        scenarios = create_sample_scenarios()
        scenario = scenarios[args.scenario]
        symbol = scenario["symbol"]
        start_date = scenario["start_date"]
        end_date = scenario["end_date"]
        print(f"📋 Usando escenario: {args.scenario} - {scenario['description']}")
    else:
        symbol = args.symbol
        start_date = args.start_date
        end_date = args.end_date
    
    try:
        if args.compare:
            # Ejecutar comparación múltiple
            run_multiple_configs_comparison(symbol, start_date, end_date)
        else:
            # Ejecutar configuración específica
            results = run_backtest_with_config(args.config, symbol, start_date, end_date, args.save)
            
            if results and results.total_trades > 0:
                print(f"\n🎉 Backtest completado exitosamente!")
                print(f"📊 Trades totales: {results.total_trades}")
                print(f"💰 PnL final: ${results.total_pnl:,.2f}")
                print(f"📈 Win Rate: {results.win_rate:.1%}")
            else:
                print(f"⚠️ Backtest completado sin trades o con errores")
    
    except KeyboardInterrupt:
        print(f"\n⏹️ Backtest interrumpido por usuario")
    except Exception as e:
        print(f"❌ Error ejecutando launcher: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Si se ejecuta sin argumentos, mostrar menú interactivo
    if len(sys.argv) == 1:
        print("🚀 ICT BACKTEST ENGINE v6.0 ENTERPRISE")
        print("=" * 50)
        print("1. Ejecutar test rápido (default config)")
        print("2. Comparar todas las configuraciones")
        print("3. Test trimestral completo")
        print("4. Ver ayuda")
        print("5. Salir")
        
        choice = input("\nSelecciona una opción (1-5): ").strip()
        
        if choice == "1":
            run_backtest_with_config("default", "EURUSD", "2024-11-01", "2024-11-30")
        elif choice == "2":
            run_multiple_configs_comparison("EURUSD", "2024-10-01", "2024-12-31")
        elif choice == "3":
            run_backtest_with_config("professional", "EURUSD", "2024-10-01", "2024-12-31")
        elif choice == "4":
            import subprocess
            subprocess.run([sys.executable, __file__, "--help"])
        elif choice == "5":
            print("👋 ¡Hasta luego!")
        else:
            print("⚠️ Opción no válida")
    else:
        main()
