#!/usr/bin/env python3
"""
🎨 MASTER BACKTEST VISUAL SELECTOR v6.0
=======================================

Sistema unificado con múltiples niveles de visualización:
1. 📊 Executive Dashboard - Para reportes ejecutivos
2. 🔬 Technical Analysis - Para análisis técnico detallado  
3. ⚡ Quick Check - Para validación rápida
4. 📈 Comparative View - Para comparar estrategias
5. 🎯 Single Metric Focus - Para métricas específicas

¡Elige tu nivel de detalle según la situación!
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Add project path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class MasterBacktestVisualizer:
    """Sistema maestro de visualización para backtesting"""
    
    def __init__(self):
        self.sample_data = {
            'symbol': 'EURUSD',
            'trades': 58,
            'wins': 37,
            'win_rate': 0.638,
            'total_pnl': 1456.80,
            'roi': 14.57,
            'max_dd': 9.2,
            'profit_factor': 1.82,
            'sharpe': 1.34,
            'avg_win': 87.30,
            'avg_loss': -42.10,
            'largest_win': 234.50,
            'largest_loss': -89.20,
            'best_pattern': 'SILVER_BULLET',
            'best_pattern_wr': 0.75,
            'best_session': 'LONDON',
            'sm_trades': 18,
            'sm_boost': 0.093
        }
    
    def executive_dashboard(self):
        """Dashboard ejecutivo limpio para presentaciones"""
        data = self.sample_data
        
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 18 + "📊 EXECUTIVE SUMMARY" + " " * 29 + "║") 
        print("╚" + "═" * 68 + "╝")
        
        # KPIs principales en formato de tarjetas
        print()
        print("┌─ 💼 KEY PERFORMANCE INDICATORS " + "─" * 33 + "┐")
        
        # Status colors
        wr_status = "🟢 STRONG" if data['win_rate'] >= 0.6 else "🟡 MODERATE"
        roi_status = "🟢 EXCELLENT" if data['roi'] >= 15 else "🟡 GOOD" if data['roi'] >= 10 else "🔴 POOR"
        risk_status = "🟢 LOW" if data['max_dd'] <= 10 else "🟡 MEDIUM"
        
        print(f"│ Win Rate     │ {data['win_rate']:>6.1%} │ {wr_status:<12} │ {data['wins']}/{data['trades']} trades │")
        print(f"│ ROI          │ {data['roi']:>6.1f}% │ {roi_status:<12} │ ${data['total_pnl']:>8,.0f}      │")
        print(f"│ Risk Level   │ {data['max_dd']:>6.1f}% │ {risk_status:<12} │ Max Drawdown     │")
        print(f"│ Edge Factor  │ {data['profit_factor']:>6.2f} │ {'🟢 STRONG' if data['profit_factor'] >= 1.5 else '🟡 MODERATE':<12} │ Trading Edge     │")
        
        print("└" + "─" * 66 + "┘")
        
        # Recomendación ejecutiva
        if data['win_rate'] >= 0.6 and data['roi'] >= 12 and data['max_dd'] <= 12:
            recommendation = "✅ APPROVED FOR LIVE TRADING"
            action = "Deploy with current parameters"
        elif data['win_rate'] >= 0.5 and data['roi'] >= 8:
            recommendation = "🟡 CONDITIONAL APPROVAL"
            action = "Deploy with reduced risk per trade"
        else:
            recommendation = "🔴 REQUIRES OPTIMIZATION"
            action = "Optimize strategy before deployment"
        
        print(f"\n🎯 EXECUTIVE DECISION: {recommendation}")
        print(f"📋 RECOMMENDED ACTION: {action}")
        print()
    
    def technical_analysis(self):
        """Análisis técnico detallado para traders"""
        data = self.sample_data
        
        print("╔" + "═" * 76 + "╗")
        print("║" + " " * 22 + "🔬 TECHNICAL ANALYSIS" + " " * 31 + "║")
        print("╚" + "═" * 76 + "╝")
        
        # Métricas de distribución
        print("\n┌─ 📊 TRADE DISTRIBUTION ANALYSIS " + "─" * 40 + "┐")
        print(f"│ Win/Loss Ratio    │ {abs(data['avg_win']/data['avg_loss']):>8.2f} │ Avg Win: ${data['avg_win']:>6.0f} vs Avg Loss: ${abs(data['avg_loss']):>6.0f} │")
        print(f"│ Largest Win/Loss  │ {data['largest_win']/abs(data['largest_loss']):>8.2f} │ Best: ${data['largest_win']:>8.0f} vs Worst: ${abs(data['largest_loss']):>8.0f}  │")
        print(f"│ Expectancy        │ ${(data['win_rate']*data['avg_win'] + (1-data['win_rate'])*data['avg_loss']):>8.0f} │ Per trade expected return             │")
        print(f"│ Sharpe Ratio      │ {data['sharpe']:>8.2f} │ Risk-adjusted performance             │")
        print("└" + "─" * 74 + "┘")
        
        # Pattern analysis
        print("\n┌─ 🎯 PATTERN & SESSION PERFORMANCE " + "─" * 36 + "┐")
        print(f"│ Best Pattern      │ {data['best_pattern']:<20} │ Win Rate: {data['best_pattern_wr']:.1%}           │")
        print(f"│ Best Session      │ {data['best_session']:<20} │ Most profitable timeframe    │")
        print(f"│ Smart Money Edge  │ {data['sm_trades']:>2} trades enhanced    │ +{data['sm_boost']:.1%} win rate boost        │")
        print("└" + "─" * 74 + "┘")
        
        # Risk metrics
        print("\n┌─ ⚠️  RISK ASSESSMENT " + "─" * 50 + "┐")
        kelly_pct = (data['win_rate'] * data['avg_win'] - (1-data['win_rate']) * abs(data['avg_loss'])) / data['avg_win'] * 100
        print(f"│ Kelly Criterion   │ {kelly_pct:>6.1f}% │ Optimal position size recommendation │")
        print(f"│ Risk of Ruin      │ {(1-data['win_rate'])**10*100:>6.1f}% │ 10 consecutive losses probability    │")
        print(f"│ Recovery Factor   │ {data['total_pnl']/data['max_dd']/100:>6.1f} │ Profit/Drawdown ratio               │")
        print("└" + "─" * 74 + "┘")
    
    def quick_check(self):
        """Validación ultra-rápida de 5 segundos"""
        data = self.sample_data
        
        # Single line summary
        status = "🟢" if data['win_rate'] >= 0.6 and data['roi'] >= 12 else "🟡" if data['win_rate'] >= 0.5 else "🔴"
        verdict = "GO" if status == "🟢" else "OPTIMIZE" if status == "🟡" else "REBUILD"
        
        print("⚡ QUICK CHECK ⚡")
        print("=" * 50)
        print(f"{status} {data['symbol']} │ {data['win_rate']:.0%} win │ {data['roi']:+.1f}% ROI │ {data['max_dd']:.1f}% DD │ PF:{data['profit_factor']:.1f} │ {verdict}")
        
        # Traffic light system
        metrics = [
            ("Win Rate", data['win_rate'], 0.6, 0.5),
            ("ROI", data['roi']/100, 0.15, 0.08),
            ("Drawdown", 1-data['max_dd']/100, 0.9, 0.8),  # Inverted (lower is better)
            ("Profit Factor", data['profit_factor'], 1.5, 1.2)
        ]
        
        print("\n🚦 TRAFFIC LIGHT SYSTEM:")
        for name, value, excellent, good in metrics:
            if value >= excellent:
                light = "🟢"
            elif value >= good:
                light = "🟡"
            else:
                light = "🔴"
            print(f"{light} {name}")
    
    def comparative_view(self):
        """Vista comparativa de múltiples configuraciones"""
        configs = [
            ("Conservative", 0.58, 11.2, 6.8, 1.45),
            ("Balanced", 0.62, 14.6, 9.2, 1.72),
            ("Aggressive", 0.65, 18.3, 13.1, 1.89)
        ]
        
        print("╔" + "═" * 80 + "╗")
        print("║" + " " * 26 + "📈 STRATEGY COMPARISON" + " " * 31 + "║")
        print("╚" + "═" * 80 + "╝")
        
        print("\n┌─ PERFORMANCE MATRIX " + "─" * 55 + "┐")
        print("│ Strategy     │ Win Rate │   ROI   │ Drawdown │ P.Factor │ Score │")
        print("├─────────────┼─────────┼────────┼─────────┼─────────┼──────┤")
        
        for name, wr, roi, dd, pf in configs:
            # Calculate score
            score = 0
            if wr >= 0.6: score += 1
            if roi >= 15: score += 1  
            if dd <= 10: score += 1
            if pf >= 1.5: score += 1
            
            stars = "★" * score + "☆" * (4 - score)
            
            # Color coding
            if score >= 3:
                status = "🟢"
            elif score >= 2:
                status = "🟡"
            else:
                status = "🔴"
            
            print(f"│ {status} {name:<10} │ {wr:>7.1%} │ {roi:>6.1f}% │ {dd:>7.1f}% │ {pf:>7.2f} │ {stars} │")
        
        print("└─────────────┴─────────┴────────┴─────────┴─────────┴──────┘")
        
        # Winner
        best = max(configs, key=lambda x: (x[1] >= 0.6) + (x[2] >= 15) + (x[3] <= 10) + (x[4] >= 1.5))
        print(f"\n🏆 RECOMMENDED: {best[0]} strategy")
    
    def single_metric_focus(self, metric: str = "roi"):
        """Enfoque en una métrica específica"""
        data = self.sample_data
        
        metrics_info = {
            'roi': ("💰 RETURN ON INVESTMENT", data['roi'], "%", "Profitability"),
            'win_rate': ("🎯 WIN RATE", data['win_rate']*100, "%", "Consistency"), 
            'drawdown': ("⚠️ MAX DRAWDOWN", data['max_dd'], "%", "Risk Control"),
            'profit_factor': ("📊 PROFIT FACTOR", data['profit_factor'], "", "Trading Edge"),
            'sharpe': ("⚖️ SHARPE RATIO", data['sharpe'], "", "Risk-Adjusted Return")
        }
        
        if metric not in metrics_info:
            metric = 'roi'
        
        title, value, unit, description = metrics_info[metric]
        
        print("╔" + "═" * 60 + "╗")
        print(f"║{' ' * 15}{title}{' ' * (44-len(title))}║")
        print("╚" + "═" * 60 + "╝")
        
        # Large number display
        print(f"\n{' ' * 20}{value:.1f}{unit}")
        print(f"{' ' * 15}({description})")
        
        # Benchmark comparison
        benchmarks = {
            'roi': [(20, "Excellent"), (12, "Good"), (5, "Poor")],
            'win_rate': [(60, "Excellent"), (50, "Good"), (40, "Poor")],
            'drawdown': [(8, "Excellent"), (15, "Good"), (25, "Poor")],
            'profit_factor': [(2.0, "Excellent"), (1.5, "Good"), (1.2, "Poor")],
            'sharpe': [(1.5, "Excellent"), (1.0, "Good"), (0.5, "Poor")]
        }
        
        if metric in benchmarks:
            bench_value = value if metric != 'drawdown' else 100 - value  # Invert drawdown
            for threshold, rating in benchmarks[metric]:
                if bench_value >= threshold:
                    print(f"\n🎯 RATING: {rating}")
                    break
    
    def run_visual_selector(self):
        """Selector principal de visualización"""
        print("🎨 MASTER BACKTEST VISUAL SELECTOR v6.0")
        print("=" * 50)
        print("Choose your visualization level:")
        print()
        print("1. 📊 Executive Dashboard  - Clean summary for reports")
        print("2. 🔬 Technical Analysis   - Detailed metrics for traders") 
        print("3. ⚡ Quick Check         - 5-second validation")
        print("4. 📈 Comparative View    - Compare strategies")
        print("5. 🎯 Single Metric       - Focus on one metric")
        print("6. 🌟 ALL VIEWS           - Show everything")
        
        choice = input("\nSelect view (1-6): ").strip()
        
        print("\n" + "=" * 80)
        
        if choice == "1":
            self.executive_dashboard()
        elif choice == "2":
            self.technical_analysis()
        elif choice == "3":
            self.quick_check()
        elif choice == "4":
            self.comparative_view()
        elif choice == "5":
            metric = input("Which metric? (roi/win_rate/drawdown/profit_factor/sharpe): ").strip()
            self.single_metric_focus(metric)
        elif choice == "6":
            print("🌟 SHOWING ALL VISUALIZATION LEVELS...\n")
            
            self.executive_dashboard()
            print("\n" + "─" * 80 + "\n")
            
            self.technical_analysis()
            print("\n" + "─" * 80 + "\n")
            
            self.quick_check()
            print("\n" + "─" * 80 + "\n")
            
            self.comparative_view()
            
        else:
            print("Invalid choice, showing executive dashboard...")
            self.executive_dashboard()

if __name__ == "__main__":
    visualizer = MasterBacktestVisualizer()
    visualizer.run_visual_selector()
