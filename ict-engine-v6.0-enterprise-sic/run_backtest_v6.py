"""
🎯 ICT Backtest Runner v6.0 Enterprise
=====================================

Script principal para ejecutar backtests con el ICT Engine v6.0.
Integra todos los componentes para un backtesting profesional.

Usage:
    python run_backtest_v6.py --symbol EURUSD --days 30 --risk 1.5
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from core.backtesting.backtest_engine import BacktestEngine, BacktestConfig
from core.backtesting.performance_analyzer import PerformanceAnalyzer
from core.backtesting.report_generator import ReportGenerator
from utils.smart_trading_logger import SmartTradingLogger


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='ICT Backtest Runner v6.0 Enterprise')
    
    parser.add_argument('--symbol', type=str, default='EURUSD',
                       help='Trading symbol (default: EURUSD)')
    parser.add_argument('--timeframe', type=str, default='M15',
                       help='Primary timeframe (default: M15)')
    parser.add_argument('--days', type=int, default=30,
                       help='Number of days to backtest (default: 30)')
    parser.add_argument('--balance', type=float, default=10000.0,
                       help='Initial balance (default: 10000)')
    parser.add_argument('--risk', type=float, default=1.0,
                       help='Risk per trade percentage (default: 1.0)')
    parser.add_argument('--max-positions', type=int, default=3,
                       help='Maximum concurrent positions (default: 3)')
    parser.add_argument('--no-smart-money', action='store_true',
                       help='Disable Smart Money Concepts')
    parser.add_argument('--no-multi-tf', action='store_true',
                       help='Disable Multi-Timeframe analysis')
    parser.add_argument('--output-dir', type=str, default='backtest_results',
                       help='Output directory for reports')
    parser.add_argument('--report-name', type=str, default=None,
                       help='Custom report name')
    
    return parser.parse_args()


def main():
    """Main execution function"""
    logger = SmartTradingLogger("BacktestRunner")
    
    # Parse arguments
    args = parse_arguments()
    
    logger.info("🎯 ICT Backtest Runner v6.0 Enterprise")
    logger.info("=" * 50)
    
    # Create backtest configuration
    end_date = datetime.now()
    start_date = end_date - timedelta(days=args.days)
    
    config = BacktestConfig(
        symbol=args.symbol,
        primary_timeframe=args.timeframe,
        context_timeframes=['H1', 'H4', 'D1'],
        start_date=start_date,
        end_date=end_date,
        initial_balance=args.balance,
        risk_per_trade=args.risk,
        max_positions=args.max_positions,
        enable_smart_money=not args.no_smart_money,
        enable_multi_timeframe=not args.no_multi_tf
    )
    
    logger.info(f"📊 Configuration:")
    logger.info(f"   Symbol: {config.symbol}")
    logger.info(f"   Primary TF: {config.primary_timeframe}")
    logger.info(f"   Period: {start_date.date()} to {end_date.date()}")
    logger.info(f"   Initial Balance: ${config.initial_balance:,.2f}")
    logger.info(f"   Risk per Trade: {config.risk_per_trade}%")
    logger.info(f"   Smart Money: {'✅ Enabled' if config.enable_smart_money else '❌ Disabled'}")
    logger.info(f"   Multi-TF: {'✅ Enabled' if config.enable_multi_timeframe else '❌ Disabled'}")
    
    try:
        # Initialize backtest engine
        logger.info("🚀 Inicializando Backtest Engine...")
        engine = BacktestEngine(config)
        
        # Run backtest
        logger.info("⚡ Ejecutando backtest...")
        results = engine.run_backtest()
        
        # Generate additional analysis
        logger.info("📈 Generando análisis avanzado...")
        performance_analyzer = PerformanceAnalyzer()
        
        # Trade quality analysis
        trade_quality = performance_analyzer.analyze_trade_quality(results.trades_history)
        
        # Monthly breakdown
        monthly_breakdown = performance_analyzer.generate_monthly_breakdown(
            results.trades_history, results.equity_curve
        )
        
        # Monte Carlo analysis
        monte_carlo = performance_analyzer.calculate_monte_carlo_analysis(
            results.trades_history, iterations=1000
        )
        
        # Generate reports
        logger.info("📋 Generando reportes...")
        report_generator = ReportGenerator(args.output_dir)
        
        report_path = report_generator.generate_comprehensive_report(
            results, trade_quality, monthly_breakdown, monte_carlo, args.report_name
        )
        
        # Print summary
        summary = report_generator.generate_quick_summary(results)
        print(summary)
        
        logger.info(f"✅ Backtest completado exitosamente!")
        logger.info(f"📁 Reporte generado: {report_path}")
        
        # Return results for potential further processing
        return {
            'results': results,
            'trade_quality': trade_quality,
            'monthly_breakdown': monthly_breakdown,
            'monte_carlo': monte_carlo,
            'report_path': report_path
        }
        
    except Exception as e:
        logger.error(f"❌ Error durante el backtest: {e}")
        raise


def run_custom_backtest(symbol: str = "EURUSD", days: int = 30, risk: float = 1.0,
                       enable_smart_money: bool = True) -> dict:
    """
    Función helper para ejecutar backtest programáticamente
    
    Args:
        symbol: Símbolo a testear
        days: Días de backtest
        risk: Riesgo por trade
        enable_smart_money: Habilitar Smart Money Concepts
        
    Returns:
        dict: Resultados completos del backtest
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    config = BacktestConfig(
        symbol=symbol,
        primary_timeframe="M15",
        start_date=start_date,
        end_date=end_date,
        risk_per_trade=risk,
        enable_smart_money=enable_smart_money
    )
    
    engine = BacktestEngine(config)
    results = engine.run_backtest()
    
    return {
        'config': config,
        'results': results,
        'summary': {
            'total_trades': results.total_trades,
            'win_rate': results.win_rate,
            'total_pnl': results.total_pnl,
            'max_drawdown': results.max_drawdown,
            'sharpe_ratio': results.sharpe_ratio
        }
    }


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n⚠️ Backtest interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        sys.exit(1)
