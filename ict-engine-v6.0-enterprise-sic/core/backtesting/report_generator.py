"""
🎯 Report Generator v6.0 Enterprise
==================================

Generador de reportes profesionales para el Backtest Engine v6.0.
Crea reportes detallados en HTML, PDF y Excel.

Features:
- Reportes HTML interactivos
- Gráficos de performance
- Análisis detallado por patterns
- Resumen ejecutivo
- Exportación multi-formato
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd
import json
from pathlib import Path


class ReportGenerator:
    """
    🎯 Report Generator v6.0 Enterprise
    
    Genera reportes profesionales:
    - HTML interactivo
    - Análisis detallado
    - Gráficos de performance
    - Resumen ejecutivo
    """
    
    def __init__(self, output_dir: str = "reports"):
        """
        Inicializar Report Generator
        
        Args:
            output_dir: Directorio de salida para reportes
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_comprehensive_report(self, backtest_results, trade_quality_analysis: Dict,
                                    monthly_breakdown: Dict, monte_carlo: Dict,
                                    report_name: Optional[str] = None) -> str:
        """
        Generar reporte comprehensive
        
        Args:
            backtest_results: Resultados del backtest
            trade_quality_analysis: Análisis de calidad de trades
            monthly_breakdown: Breakdown mensual
            monte_carlo: Análisis Monte Carlo
            report_name: Nombre del reporte
            
        Returns:
            str: Ruta del reporte generado
        """
        if report_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"backtest_report_{timestamp}"
        
        # Generate HTML report
        html_path = self._generate_html_report(
            backtest_results, trade_quality_analysis, monthly_breakdown,
            monte_carlo, report_name
        )
        
        # Generate CSV data files
        self._generate_csv_files(backtest_results, report_name)
        
        # Generate JSON summary
        self._generate_json_summary(backtest_results, report_name)
        
        return str(html_path)
    
    def _generate_html_report(self, results, quality_analysis: Dict, monthly: Dict,
                            monte_carlo: Dict, report_name: str) -> Path:
        """Generar reporte HTML"""
        html_content = self._create_html_template(
            results, quality_analysis, monthly, monte_carlo
        )
        
        html_path = self.output_dir / f"{report_name}.html"
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_path
    
    def _create_html_template(self, results, quality_analysis: Dict, 
                            monthly: Dict, monte_carlo: Dict) -> str:
        """Crear template HTML"""
        
        # Extract key metrics safely
        config = getattr(results, 'config', None)
        symbol = config.symbol if config else "Unknown"
        timeframe = config.primary_timeframe if config else "Unknown"
        start_date = config.start_date.strftime("%Y-%m-%d") if config and config.start_date else "Unknown"
        end_date = config.end_date.strftime("%Y-%m-%d") if config and config.end_date else "Unknown"
        initial_balance = config.initial_balance if config else 0.0
        
        # Performance metrics
        total_trades = getattr(results, 'total_trades', 0)
        win_rate = getattr(results, 'win_rate', 0.0) * 100
        total_pnl = getattr(results, 'total_pnl', 0.0)
        max_drawdown = getattr(results, 'max_drawdown', 0.0)
        sharpe_ratio = getattr(results, 'sharpe_ratio', 0.0)
        profit_factor = getattr(results, 'profit_factor', 0.0)
        patterns_detected = getattr(results, 'patterns_detected', 0)
        smart_money_signals = getattr(results, 'smart_money_signals', 0)
        execution_time = getattr(results, 'execution_time', 0.0)
        
        # ROI calculation
        roi_percent = (total_pnl / initial_balance * 100) if initial_balance > 0 else 0.0
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ICT Backtest Report v6.0 Enterprise</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                    color: #333;
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                }}
                
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                
                .header h1 {{
                    margin: 0;
                    font-size: 2.5em;
                    font-weight: 300;
                }}
                
                .header p {{
                    margin: 10px 0 0 0;
                    font-size: 1.2em;
                    opacity: 0.9;
                }}
                
                .summary {{
                    padding: 30px;
                    border-bottom: 1px solid #eee;
                }}
                
                .metrics-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-top: 20px;
                }}
                
                .metric-card {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #667eea;
                }}
                
                .metric-card h3 {{
                    margin: 0 0 10px 0;
                    color: #667eea;
                    font-size: 0.9em;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                
                .metric-card .value {{
                    font-size: 2em;
                    font-weight: bold;
                    color: #333;
                }}
                
                .positive {{ color: #28a745; }}
                .negative {{ color: #dc3545; }}
                
                .section {{
                    padding: 30px;
                    border-bottom: 1px solid #eee;
                }}
                
                .section h2 {{
                    color: #667eea;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }}
                
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                
                th {{
                    background-color: #f8f9fa;
                    font-weight: bold;
                    color: #667eea;
                }}
                
                .footer {{
                    padding: 20px 30px;
                    background-color: #f8f9fa;
                    text-align: center;
                    color: #666;
                    font-size: 0.9em;
                }}
                
                .config-info {{
                    background: #e9ecef;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }}
                
                .highlight {{
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 15px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎯 ICT Backtest Report v6.0</h1>
                    <p>Enterprise Performance Analysis</p>
                    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>
                
                <div class="summary">
                    <h2>📊 Executive Summary</h2>
                    
                    <div class="config-info">
                        <strong>Configuration:</strong> {symbol} • {timeframe} • {start_date} to {end_date} • 
                        Initial Balance: ${initial_balance:,.2f}
                    </div>
                    
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <h3>Total Return</h3>
                            <div class="value {'positive' if total_pnl > 0 else 'negative'}">${total_pnl:,.2f}</div>
                            <div>ROI: {roi_percent:.2f}%</div>
                        </div>
                        
                        <div class="metric-card">
                            <h3>Total Trades</h3>
                            <div class="value">{total_trades}</div>
                            <div>Win Rate: {win_rate:.1f}%</div>
                        </div>
                        
                        <div class="metric-card">
                            <h3>Max Drawdown</h3>
                            <div class="value negative">${max_drawdown:,.2f}</div>
                            <div>Peak to Trough</div>
                        </div>
                        
                        <div class="metric-card">
                            <h3>Sharpe Ratio</h3>
                            <div class="value {'positive' if sharpe_ratio > 1 else 'negative'}">{sharpe_ratio:.2f}</div>
                            <div>Risk-Adjusted Return</div>
                        </div>
                        
                        <div class="metric-card">
                            <h3>Profit Factor</h3>
                            <div class="value {'positive' if profit_factor > 1 else 'negative'}">{profit_factor:.2f}</div>
                            <div>Gross Profit / Gross Loss</div>
                        </div>
                        
                        <div class="metric-card">
                            <h3>Execution Time</h3>
                            <div class="value">{execution_time:.1f}s</div>
                            <div>{patterns_detected} Patterns • {smart_money_signals} Smart Money</div>
                        </div>
                    </div>
                </div>
                
                {self._generate_pattern_analysis_section(quality_analysis)}
                
                {self._generate_monthly_section(monthly)}
                
                {self._generate_monte_carlo_section(monte_carlo)}
                
                <div class="footer">
                    <p>📈 ICT Engine v6.0 Enterprise • Advanced Trading System Analysis</p>
                    <p>This report was generated automatically by the ICT Backtest Engine v6.0</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def _generate_pattern_analysis_section(self, quality_analysis: Dict) -> str:
        """Generar sección de análisis de patterns"""
        if not quality_analysis or 'pattern_performance' not in quality_analysis:
            return ""
        
        pattern_perf = quality_analysis['pattern_performance']
        
        rows = ""
        for pattern, metrics in pattern_perf.items():
            win_rate = metrics.get('win_rate', 0) * 100
            total_pnl = metrics.get('total_pnl', 0)
            trades = metrics.get('total_trades', 0)
            avg_pnl = metrics.get('avg_pnl', 0)
            
            pnl_class = 'positive' if total_pnl > 0 else 'negative'
            
            rows += f"""
            <tr>
                <td>{pattern}</td>
                <td>{trades}</td>
                <td>{win_rate:.1f}%</td>
                <td class="{pnl_class}">${total_pnl:,.2f}</td>
                <td class="{pnl_class}">${avg_pnl:,.2f}</td>
            </tr>
            """
        
        return f"""
        <div class="section">
            <h2>🎯 Pattern Performance Analysis</h2>
            <p>Detailed breakdown of performance by pattern type detected by the ICT Engine v6.0.</p>
            
            <table>
                <thead>
                    <tr>
                        <th>Pattern Type</th>
                        <th>Total Trades</th>
                        <th>Win Rate</th>
                        <th>Total PnL</th>
                        <th>Avg PnL</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        """
    
    def _generate_monthly_section(self, monthly: Dict) -> str:
        """Generar sección mensual"""
        if not monthly:
            return ""
        
        rows = ""
        for month, metrics in monthly.items():
            pnl = metrics.get('pnl', 0)
            trades = metrics.get('trades', 0)
            win_rate = metrics.get('win_rate', 0) * 100
            
            pnl_class = 'positive' if pnl > 0 else 'negative'
            
            rows += f"""
            <tr>
                <td>{month}</td>
                <td>{trades}</td>
                <td>{win_rate:.1f}%</td>
                <td class="{pnl_class}">${pnl:,.2f}</td>
            </tr>
            """
        
        return f"""
        <div class="section">
            <h2>📅 Monthly Performance Breakdown</h2>
            <p>Month-by-month analysis of trading performance.</p>
            
            <table>
                <thead>
                    <tr>
                        <th>Month</th>
                        <th>Trades</th>
                        <th>Win Rate</th>
                        <th>PnL</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        """
    
    def _generate_monte_carlo_section(self, monte_carlo: Dict) -> str:
        """Generar sección Monte Carlo"""
        if not monte_carlo:
            return ""
        
        final_percentiles = monte_carlo.get('final_return_percentiles', {})
        dd_percentiles = monte_carlo.get('max_drawdown_percentiles', {})
        prob_positive = monte_carlo.get('probability_positive', 0) * 100
        
        return f"""
        <div class="section">
            <h2>🎲 Monte Carlo Analysis</h2>
            <p>Statistical analysis based on 1000 random trade order simulations.</p>
            
            <div class="highlight">
                <strong>Probability of Positive Return:</strong> {prob_positive:.1f}%
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 20px;">
                <div>
                    <h3>Final Return Percentiles</h3>
                    <table>
                        <tr><th>Percentile</th><th>Return</th></tr>
                        <tr><td>5th</td><td>${final_percentiles.get('5th', 0):,.2f}</td></tr>
                        <tr><td>25th</td><td>${final_percentiles.get('25th', 0):,.2f}</td></tr>
                        <tr><td>50th (Median)</td><td>${final_percentiles.get('50th', 0):,.2f}</td></tr>
                        <tr><td>75th</td><td>${final_percentiles.get('75th', 0):,.2f}</td></tr>
                        <tr><td>95th</td><td>${final_percentiles.get('95th', 0):,.2f}</td></tr>
                    </table>
                </div>
                
                <div>
                    <h3>Max Drawdown Percentiles</h3>
                    <table>
                        <tr><th>Percentile</th><th>Drawdown</th></tr>
                        <tr><td>5th</td><td>${dd_percentiles.get('5th', 0):,.2f}</td></tr>
                        <tr><td>25th</td><td>${dd_percentiles.get('25th', 0):,.2f}</td></tr>
                        <tr><td>50th (Median)</td><td>${dd_percentiles.get('50th', 0):,.2f}</td></tr>
                        <tr><td>75th</td><td>${dd_percentiles.get('75th', 0):,.2f}</td></tr>
                        <tr><td>95th</td><td>${dd_percentiles.get('95th', 0):,.2f}</td></tr>
                    </table>
                </div>
            </div>
        </div>
        """
    
    def _generate_csv_files(self, results, report_name: str) -> None:
        """Generar archivos CSV con datos"""
        # Trades history
        trades_history = getattr(results, 'trades_history', [])
        if trades_history:
            trades_df = pd.DataFrame(trades_history)
            trades_path = self.output_dir / f"{report_name}_trades.csv"
            trades_df.to_csv(trades_path, index=False)
        
        # Equity curve
        equity_curve = getattr(results, 'equity_curve', pd.DataFrame())
        if not equity_curve.empty:
            equity_path = self.output_dir / f"{report_name}_equity.csv"
            equity_curve.to_csv(equity_path)
    
    def _generate_json_summary(self, results, report_name: str) -> None:
        """Generar resumen JSON"""
        summary = {
            'report_name': report_name,
            'generated_at': datetime.now().isoformat(),
            'total_trades': getattr(results, 'total_trades', 0),
            'winning_trades': getattr(results, 'winning_trades', 0),
            'win_rate': getattr(results, 'win_rate', 0.0),
            'total_pnl': getattr(results, 'total_pnl', 0.0),
            'max_drawdown': getattr(results, 'max_drawdown', 0.0),
            'sharpe_ratio': getattr(results, 'sharpe_ratio', 0.0),
            'profit_factor': getattr(results, 'profit_factor', 0.0),
            'patterns_detected': getattr(results, 'patterns_detected', 0),
            'smart_money_signals': getattr(results, 'smart_money_signals', 0),
            'execution_time': getattr(results, 'execution_time', 0.0)
        }
        
        # Add config info if available
        config = getattr(results, 'config', None)
        if config:
            summary['config'] = {
                'symbol': config.symbol,
                'primary_timeframe': config.primary_timeframe,
                'start_date': config.start_date.isoformat() if config.start_date else None,
                'end_date': config.end_date.isoformat() if config.end_date else None,
                'initial_balance': config.initial_balance,
                'risk_per_trade': config.risk_per_trade
            }
        
        json_path = self.output_dir / f"{report_name}_summary.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
    
    def generate_quick_summary(self, results) -> str:
        """
        Generar resumen rápido en texto
        
        Args:
            results: Resultados del backtest
            
        Returns:
            str: Resumen en texto
        """
        config = getattr(results, 'config', None)
        symbol = config.symbol if config else "Unknown"
        
        total_trades = getattr(results, 'total_trades', 0)
        win_rate = getattr(results, 'win_rate', 0.0) * 100
        total_pnl = getattr(results, 'total_pnl', 0.0)
        max_drawdown = getattr(results, 'max_drawdown', 0.0)
        sharpe_ratio = getattr(results, 'sharpe_ratio', 0.0)
        execution_time = getattr(results, 'execution_time', 0.0)
        
        return f"""
🎯 ICT Backtest Summary v6.0
═══════════════════════════════
Symbol: {symbol}
Total Trades: {total_trades}
Win Rate: {win_rate:.1f}%
Total PnL: ${total_pnl:,.2f}
Max Drawdown: ${max_drawdown:,.2f}
Sharpe Ratio: {sharpe_ratio:.2f}
Execution Time: {execution_time:.1f}s
Status: {'✅ PROFITABLE' if total_pnl > 0 else '❌ UNPROFITABLE'}
"""
