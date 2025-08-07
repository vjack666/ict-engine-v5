"""
🎯 ICT Backtest Example v6.0 Enterprise
======================================

Ejemplo práctico que integra tu código de backtesting existente
con el nuevo Backtest Engine v6.0 Enterprise.

Este ejemplo muestra cómo migrar desde tu backtester_ict.py original
al nuevo sistema enterprise con todas las mejoras.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from core.backtesting.backtest_engine import BacktestEngine, BacktestConfig
from core.backtesting.performance_analyzer import PerformanceAnalyzer
from core.backtesting.report_generator import ReportGenerator
from utils.smart_trading_logger import SmartTradingLogger


def create_ict_backtest_config() -> BacktestConfig:
    """
    Crear configuración basada en tu backtester_ict.py original
    """
    return BacktestConfig(
        symbol="EURUSD",
        primary_timeframe="M15",
        context_timeframes=["H1", "H4", "D1"],
        start_date=datetime.now() - timedelta(days=30),  # 30 días como en tu ejemplo
        end_date=datetime.now(),
        initial_balance=10000.0,  # BALANCE_INICIAL de tu código
        risk_per_trade=2.0,       # RIESGO_PORCENTAJE de tu código
        max_positions=3,
        commission_per_lot=7.0,
        spread_points=2,
        slippage_points=1,
        enable_smart_money=True,   # Mejora sobre tu sistema original
        enable_multi_timeframe=True
    )


def run_ict_backtest_example():
    """
    Ejecutar ejemplo de backtest ICT v6.0
    Esto reemplaza tu bucle principal de simulación con el nuevo sistema enterprise
    """
    logger = SmartTradingLogger("ICTBacktestExample")
    
    print("🎯 ICT Backtest Example v6.0 Enterprise")
    print("=" * 60)
    print("Migración desde backtester_ict.py al sistema enterprise")
    print()
    
    start_time = time.time()
    
    try:
        # 1. Crear configuración (equivalente a tu sección de configuración)
        logger.info("📋 Creando configuración...")
        config = create_ict_backtest_config()
        
        print(f"✅ Configuración ICT Enterprise:")
        print(f"   Symbol: {config.symbol}")
        print(f"   Primary TF: {config.primary_timeframe}")
        print(f"   Context TFs: {config.context_timeframes}")
        print(f"   Period: {config.start_date.date()} to {config.end_date.date()}")
        print(f"   Initial Balance: ${config.initial_balance:,.2f}")
        print(f"   Risk per Trade: {config.risk_per_trade}%")
        print(f"   Max Positions: {config.max_positions}")
        print(f"   Smart Money: {'✅ Enabled' if config.enable_smart_money else '❌ Disabled'}")
        print(f"   Multi-TF: {'✅ Enabled' if config.enable_multi_timeframe else '❌ Disabled'}")
        print()
        
        # 2. Inicializar motor de backtest (reemplaza tu inicialización manual)
        logger.info("🚀 Inicializando Backtest Engine v6.0...")
        engine = BacktestEngine(config)
        print("✅ Backtest Engine v6.0 inicializado")
        print("   - AdvancedCandleDownloader integrado")
        print("   - PatternDetector v6.0 integrado")
        print("   - SmartMoneyAnalyzer v6.0 integrado")
        print("   - TradingSimulator profesional")
        print("   - RiskManager avanzado")
        print()
        
        # 3. Ejecutar backtest (reemplaza tu bucle principal)
        logger.info("⚡ Ejecutando backtest...")
        print("🔄 Procesando datos y ejecutando estrategia ICT...")
        print("   (Esto reemplaza tu bucle manual de velas M15)")
        
        # Esto internamente hace todo lo que hacía tu bucle:
        # - Cargar datos M15, H1, H4, D1
        # - Analizar conceptos ICT multi-timeframe
        # - Determinar zonas Premium/Discount
        # - Detectar POIs (Order Blocks, FVGs)
        # - Aplicar lógica de decisión
        # - Ejecutar trades con gestión de riesgo
        # - Calcular lotajes optimizados
        # - Registrar todo en logs detallados
        results = engine.run_backtest()
        
        execution_time = time.time() - start_time
        
        print(f"✅ Backtest completado en {execution_time:.2f}s")
        print()
        
        # 4. Análisis avanzado (mejora sobre tu sistema original)
        logger.info("📊 Generando análisis avanzado...")
        performance_analyzer = PerformanceAnalyzer()
        
        # Análisis de calidad de trades por pattern
        trade_quality = performance_analyzer.analyze_trade_quality(results.trades_history)
        
        # Breakdown mensual
        monthly_breakdown = performance_analyzer.generate_monthly_breakdown(
            results.trades_history, results.equity_curve
        )
        
        # Análisis Monte Carlo (nuevo)
        monte_carlo = performance_analyzer.calculate_monte_carlo_analysis(
            results.trades_history, iterations=500
        )
        
        print("✅ Análisis avanzado completado:")
        print(f"   - Trade quality por pattern type")
        print(f"   - Monthly performance breakdown")
        print(f"   - Monte Carlo analysis (500 simulaciones)")
        print()
        
        # 5. Generar reportes profesionales (mejora sobre tu CSV simple)
        logger.info("📋 Generando reportes...")
        report_generator = ReportGenerator("ict_backtest_results")
        
        report_path = report_generator.generate_comprehensive_report(
            results, trade_quality, monthly_breakdown, monte_carlo,
            f"ict_enterprise_backtest_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        print("✅ Reportes generados:")
        print(f"   - HTML interactivo: {report_path}")
        print(f"   - CSV de trades detallado")
        print(f"   - JSON summary")
        print(f"   - Equity curve data")
        print()
        
        # 6. Mostrar resumen (equivalente a tu reporte final)
        print("📊 RESUMEN EJECUTIVO ICT v6.0")
        print("=" * 60)
        
        # Métricas básicas (como en tu código original)
        print(f"Balance Inicial:     ${config.initial_balance:,.2f}")
        print(f"Balance Final:       ${config.initial_balance + results.total_pnl:,.2f}")
        
        if results.total_pnl >= 0:
            print(f"Ganancia Total:      ✅ ${results.total_pnl:,.2f}")
        else:
            print(f"Pérdida Total:       ❌ ${results.total_pnl:,.2f}")
        
        roi_percent = (results.total_pnl / config.initial_balance) * 100
        print(f"ROI:                 {roi_percent:+.2f}%")
        print()
        
        # Métricas avanzadas (nuevas en v6.0)
        print("MÉTRICAS AVANZADAS v6.0:")
        print(f"Total Trades:        {results.total_trades}")
        print(f"Trades Ganadores:    {results.winning_trades}")
        print(f"Win Rate:            {results.win_rate:.1%}")
        print(f"Profit Factor:       {results.profit_factor:.2f}")
        print(f"Max Drawdown:        ${results.max_drawdown:,.2f}")
        print(f"Sharpe Ratio:        {results.sharpe_ratio:.2f}")
        print(f"Avg Trade:           ${results.avg_trade:,.2f}")
        print()
        
        # Métricas ICT específicas
        print("MÉTRICAS ICT ENTERPRISE:")
        print(f"Patterns Detectados: {results.patterns_detected}")
        print(f"Smart Money Signals: {results.smart_money_signals}")
        print(f"Ejecución:          {results.execution_time:.2f}s")
        print()
        
        # Comparación con sistema original
        print("🔄 MEJORAS vs SISTEMA ORIGINAL:")
        print("✅ Pattern detection automatizado vs manual")
        print("✅ Smart Money Concepts integrados")
        print("✅ Multi-timeframe enhancement automático")
        print("✅ Risk management profesional")
        print("✅ Performance analytics avanzados")
        print("✅ Reportes HTML interactivos")
        print("✅ Monte Carlo analysis")
        print("✅ Gestión de spread/slippage realista")
        print("✅ Tracking de equity curve completo")
        print()
        
        if results.total_pnl > 0:
            print("🎉 ESTRATEGIA ICT v6.0: ✅ PROFITABLE")
        else:
            print("⚠️ ESTRATEGIA ICT v6.0: ❌ NEEDS OPTIMIZATION")
        
        print(f"📁 Reporte completo disponible en: {report_path}")
        print()
        print("🎯 ICT Backtest Example v6.0 Enterprise - COMPLETADO")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Error en backtest example: {e}")
        print(f"❌ Error: {e}")
        raise


def compare_with_original():
    """
    Mostrar comparación con el sistema original
    """
    print("🔄 COMPARACIÓN: backtester_ict.py vs ICT Engine v6.0")
    print("=" * 60)
    print()
    
    comparison = [
        ("📁 Datos", "CSV local M15", "✅ Real-time MT5 multi-TF"),
        ("🎯 Pattern Detection", "Manual analisis_ict", "✅ Automated PatternDetector v6.0"),
        ("💰 Smart Money", "No incluido", "✅ SmartMoneyAnalyzer v6.0"),
        ("📊 Multi-Timeframe", "Resample manual", "✅ Integrated enhancement"),
        ("🎲 Risk Management", "RiskBot básico", "✅ Enterprise RiskManager"),
        ("💹 Trading Simulation", "SimBroker simple", "✅ Realistic TradingSimulator"),
        ("📈 Performance Analysis", "Métricas básicas", "✅ Advanced analytics + Monte Carlo"),
        ("📋 Reporting", "CSV simple", "✅ HTML interactivo + multi-format"),
        ("⚡ Performance", "Loop manual", "✅ Optimized engine"),
        ("🛡️ Error Handling", "Básico", "✅ Enterprise robustness"),
        ("🔧 Configuración", "Hardcoded", "✅ Flexible BacktestConfig"),
        ("📊 Métricas", "PnL básico", "✅ 20+ métricas profesionales")
    ]
    
    for feature, original, v6 in comparison:
        print(f"{feature:<20} {original:<25} → {v6}")
    
    print()
    print("🎯 CONCLUSIÓN: ICT Engine v6.0 es una evolución completa")
    print("   de tu sistema original con capacidades enterprise.")


if __name__ == "__main__":
    try:
        # Mostrar comparación primero
        compare_with_original()
        print()
        
        # Ejecutar ejemplo práctico
        results = run_ict_backtest_example()
        
    except KeyboardInterrupt:
        print("\\n⚠️ Ejemplo interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error en ejemplo: {e}")
        print("\\n💡 NOTA: Algunos errores son normales si no hay conexión MT5")
        print("   El sistema está diseñado para funcionar con datos reales")
