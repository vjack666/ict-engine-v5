"""
🎯 Performance Analyzer v6.0 Enterprise
======================================

Analizador de performance avanzado para el Backtest Engine v6.0.
Calcula métricas detalladas de performance y riesgo.

Features:
- Métricas estándar de trading
- Risk-adjusted returns
- Drawdown analysis
- Monte Carlo simulation
- Trade quality analysis
- Time-based performance
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import statistics


@dataclass
class PerformanceMetrics:
    """Métricas completas de performance"""
    # Basic metrics
    total_return: float = 0.0
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate: float = 0.0
    
    # PnL metrics
    total_pnl: float = 0.0
    gross_profit: float = 0.0
    gross_loss: float = 0.0
    profit_factor: float = 0.0
    
    # Trade metrics
    avg_trade: float = 0.0
    avg_winner: float = 0.0
    avg_loser: float = 0.0
    largest_winner: float = 0.0
    largest_loser: float = 0.0
    
    # Risk metrics
    max_drawdown: float = 0.0
    max_drawdown_percent: float = 0.0
    avg_drawdown: float = 0.0
    max_drawdown_duration: float = 0.0  # Days
    
    # Risk-adjusted returns
    sharpe_ratio: float = 0.0
    sortino_ratio: float = 0.0
    calmar_ratio: float = 0.0
    
    # Consistency metrics
    max_consecutive_wins: int = 0
    max_consecutive_losses: int = 0
    profit_consistency: float = 0.0  # % of profitable periods
    
    # Time-based metrics
    trades_per_day: float = 0.0
    hold_time_avg: float = 0.0  # Hours
    best_month: float = 0.0
    worst_month: float = 0.0


class PerformanceAnalyzer:
    """
    🎯 Performance Analyzer v6.0 Enterprise
    
    Analiza performance de manera integral:
    - Métricas estándar y avanzadas
    - Risk-adjusted returns
    - Análisis de drawdown
    - Consistencia temporal
    """
    
    def __init__(self):
        """Inicializar Performance Analyzer"""
        self.risk_free_rate = 0.02  # 2% annual risk-free rate
        
    def calculate_metrics(self, trades: List[Dict], equity_curve: pd.DataFrame) -> Dict[str, Any]:
        """
        Calcular métricas completas de performance
        
        Args:
            trades: Lista de trades
            equity_curve: Curva de equity
            
        Returns:
            Dict con todas las métricas
        """
        if not trades:
            return self._empty_metrics()
        
        # Basic trade metrics
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t.get('pnl', 0) > 0])
        losing_trades = len([t for t in trades if t.get('pnl', 0) < 0])
        
        # PnL calculations
        pnls = [t.get('pnl', 0) for t in trades]
        total_pnl = sum(pnls)
        gross_profit = sum([pnl for pnl in pnls if pnl > 0])
        gross_loss = abs(sum([pnl for pnl in pnls if pnl < 0]))
        
        # Calculate comprehensive metrics
        metrics = {
            # Basic metrics
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': winning_trades / total_trades if total_trades > 0 else 0.0,
            
            # PnL metrics
            'total_pnl': total_pnl,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'profit_factor': gross_profit / gross_loss if gross_loss > 0 else float('inf') if gross_profit > 0 else 0.0,
            
            # Trade size metrics
            'avg_trade': statistics.mean(pnls) if pnls else 0.0,
            'avg_winner': statistics.mean([pnl for pnl in pnls if pnl > 0]) if gross_profit > 0 else 0.0,
            'avg_loser': statistics.mean([pnl for pnl in pnls if pnl < 0]) if gross_loss > 0 else 0.0,
            'largest_winner': max(pnls) if pnls else 0.0,
            'largest_loser': min(pnls) if pnls else 0.0,
            
            # Consistency metrics
            'max_consecutive_wins': self._calculate_max_consecutive(trades, 'wins'),
            'max_consecutive_losses': self._calculate_max_consecutive(trades, 'losses'),
        }
        
        # Drawdown analysis
        if not equity_curve.empty:
            drawdown_metrics = self._calculate_drawdown_metrics(equity_curve)
            metrics.update(drawdown_metrics)
            
            # Risk-adjusted returns
            risk_metrics = self._calculate_risk_adjusted_returns(equity_curve, trades)
            metrics.update(risk_metrics)
            
            # Time-based metrics
            time_metrics = self._calculate_time_metrics(trades, equity_curve)
            metrics.update(time_metrics)
        
        return metrics
    
    def analyze_trade_quality(self, trades: List[Dict]) -> Dict[str, Any]:
        """
        Analizar calidad de trades
        
        Args:
            trades: Lista de trades
            
        Returns:
            Dict con análisis de calidad
        """
        if not trades:
            return {}
        
        # Separate by pattern type
        pattern_performance = {}
        for trade in trades:
            pattern_type = trade.get('metadata', {}).get('pattern_type', 'unknown')
            if pattern_type not in pattern_performance:
                pattern_performance[pattern_type] = []
            pattern_performance[pattern_type].append(trade.get('pnl', 0))
        
        # Analyze each pattern type
        pattern_analysis = {}
        for pattern, pnls in pattern_performance.items():
            winning = len([p for p in pnls if p > 0])
            total = len(pnls)
            
            pattern_analysis[pattern] = {
                'total_trades': total,
                'win_rate': winning / total if total > 0 else 0.0,
                'avg_pnl': statistics.mean(pnls) if pnls else 0.0,
                'total_pnl': sum(pnls),
                'best_trade': max(pnls) if pnls else 0.0,
                'worst_trade': min(pnls) if pnls else 0.0
            }
        
        # Confidence level analysis
        confidence_analysis = self._analyze_by_confidence(trades)
        
        # Duration analysis
        duration_analysis = self._analyze_by_duration(trades)
        
        return {
            'pattern_performance': pattern_analysis,
            'confidence_analysis': confidence_analysis,
            'duration_analysis': duration_analysis,
            'trade_efficiency': self._calculate_trade_efficiency(trades)
        }
    
    def generate_monthly_breakdown(self, trades: List[Dict], equity_curve: pd.DataFrame) -> Dict[str, Any]:
        """
        Generar breakdown mensual
        
        Args:
            trades: Lista de trades
            equity_curve: Curva de equity
            
        Returns:
            Dict con análisis mensual
        """
        if not trades or equity_curve.empty:
            return {}
        
        # Group trades by month
        monthly_trades = {}
        for trade in trades:
            close_time = trade.get('close_time')
            if isinstance(close_time, datetime):
                month_key = close_time.strftime('%Y-%m')
                if month_key not in monthly_trades:
                    monthly_trades[month_key] = []
                monthly_trades[month_key].append(trade)
        
        # Calculate monthly metrics
        monthly_metrics = {}
        for month, month_trades in monthly_trades.items():
            pnls = [t.get('pnl', 0) for t in month_trades]
            winning = len([p for p in pnls if p > 0])
            
            monthly_metrics[month] = {
                'trades': len(month_trades),
                'pnl': sum(pnls),
                'win_rate': winning / len(month_trades) if month_trades else 0.0,
                'avg_trade': statistics.mean(pnls) if pnls else 0.0,
                'best_trade': max(pnls) if pnls else 0.0,
                'worst_trade': min(pnls) if pnls else 0.0
            }
        
        return monthly_metrics
    
    def calculate_monte_carlo_analysis(self, trades: List[Dict], iterations: int = 1000) -> Dict[str, Any]:
        """
        Realizar análisis Monte Carlo
        
        Args:
            trades: Lista de trades
            iterations: Número de iteraciones
            
        Returns:
            Dict con resultados Monte Carlo
        """
        if not trades:
            return {}
        
        trade_returns = [t.get('pnl', 0) for t in trades]
        
        # Run Monte Carlo simulations
        final_returns = []
        max_drawdowns = []
        
        for _ in range(iterations):
            # Randomly shuffle trade order
            shuffled_returns = np.random.choice(trade_returns, size=len(trade_returns), replace=True)
            
            # Calculate cumulative return and drawdown
            cumulative = np.cumsum(shuffled_returns)
            running_max = np.maximum.accumulate(cumulative)
            drawdown = (cumulative - running_max)
            
            final_returns.append(cumulative[-1])
            max_drawdowns.append(np.min(drawdown))
        
        return {
            'final_return_percentiles': {
                '5th': float(np.percentile(final_returns, 5)),
                '25th': float(np.percentile(final_returns, 25)),
                '50th': float(np.percentile(final_returns, 50)),
                '75th': float(np.percentile(final_returns, 75)),
                '95th': float(np.percentile(final_returns, 95))
            },
            'max_drawdown_percentiles': {
                '5th': float(np.percentile(max_drawdowns, 5)),
                '25th': float(np.percentile(max_drawdowns, 25)),
                '50th': float(np.percentile(max_drawdowns, 50)),
                '75th': float(np.percentile(max_drawdowns, 75)),
                '95th': float(np.percentile(max_drawdowns, 95))
            },
            'probability_positive': float(np.mean([r > 0 for r in final_returns])),
            'expected_return': float(np.mean(final_returns)),
            'return_volatility': float(np.std(final_returns))
        }
    
    def _empty_metrics(self) -> Dict[str, Any]:
        """Retornar métricas vacías"""
        return {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'win_rate': 0.0,
            'total_pnl': 0.0,
            'gross_profit': 0.0,
            'gross_loss': 0.0,
            'profit_factor': 0.0,
            'avg_trade': 0.0,
            'avg_winner': 0.0,
            'avg_loser': 0.0,
            'largest_winner': 0.0,
            'largest_loser': 0.0,
            'max_drawdown': 0.0,
            'max_drawdown_percent': 0.0,
            'sharpe_ratio': 0.0,
            'sortino_ratio': 0.0,
            'max_consecutive_wins': 0,
            'max_consecutive_losses': 0
        }
    
    def _calculate_max_consecutive(self, trades: List[Dict], type_: str) -> int:
        """Calcular máximo de wins/losses consecutivos"""
        if not trades:
            return 0
        
        max_consecutive = 0
        current_consecutive = 0
        
        for trade in trades:
            pnl = trade.get('pnl', 0)
            is_win = pnl > 0
            
            if (type_ == 'wins' and is_win) or (type_ == 'losses' and not is_win):
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 0
        
        return max_consecutive
    
    def _calculate_drawdown_metrics(self, equity_curve: pd.DataFrame) -> Dict[str, float]:
        """Calcular métricas de drawdown"""
        if equity_curve.empty or 'equity' not in equity_curve.columns:
            return {
                'max_drawdown': 0.0,
                'max_drawdown_percent': 0.0,
                'avg_drawdown': 0.0,
                'max_drawdown_duration': 0.0
            }
        
        equity = equity_curve['equity'].values
        running_max = np.maximum.accumulate(equity)
        drawdown = equity - running_max
        drawdown_percent = (drawdown / running_max) * 100
        
        return {
            'max_drawdown': float(np.min(drawdown)),
            'max_drawdown_percent': float(np.min(drawdown_percent)),
            'avg_drawdown': float(np.mean(drawdown[drawdown < 0])) if len(drawdown[drawdown < 0]) > 0 else 0.0,
            'max_drawdown_duration': self._calculate_max_drawdown_duration(drawdown)
        }
    
    def _calculate_max_drawdown_duration(self, drawdown: np.ndarray) -> float:
        """Calcular duración máxima del drawdown"""
        in_drawdown = drawdown < 0
        if not np.any(in_drawdown):
            return 0.0
        
        # Find consecutive drawdown periods
        changes = np.diff(np.concatenate(([False], in_drawdown, [False])).astype(int))
        starts = np.where(changes == 1)[0]
        ends = np.where(changes == -1)[0]
        
        if len(starts) == 0 or len(ends) == 0:
            return 0.0
        
        durations = ends - starts
        return float(np.max(durations))  # Return in periods (convert to days based on timeframe)
    
    def _calculate_risk_adjusted_returns(self, equity_curve: pd.DataFrame, trades: List[Dict]) -> Dict[str, float]:
        """Calcular retornos ajustados por riesgo"""
        if equity_curve.empty or not trades:
            return {'sharpe_ratio': 0.0, 'sortino_ratio': 0.0, 'calmar_ratio': 0.0}
        
        # Calculate returns
        returns = equity_curve['equity'].pct_change().dropna()
        
        if len(returns) == 0:
            return {'sharpe_ratio': 0.0, 'sortino_ratio': 0.0, 'calmar_ratio': 0.0}
        
        # Annualize returns and volatility
        mean_return = returns.mean() * 252  # Assuming daily data
        volatility = returns.std() * np.sqrt(252)
        
        # Sharpe ratio
        sharpe_ratio = (mean_return - self.risk_free_rate) / volatility if volatility > 0 else 0.0
        
        # Sortino ratio (downside deviation)
        negative_returns = returns[returns < 0]
        downside_deviation = negative_returns.std() * np.sqrt(252) if len(negative_returns) > 0 else 0.0
        sortino_ratio = (mean_return - self.risk_free_rate) / downside_deviation if downside_deviation > 0 else 0.0
        
        # Calmar ratio (return / max drawdown)
        max_dd = self._calculate_drawdown_metrics(equity_curve)['max_drawdown_percent']
        calmar_ratio = mean_return / abs(max_dd) if max_dd != 0 else 0.0
        
        return {
            'sharpe_ratio': float(sharpe_ratio),
            'sortino_ratio': float(sortino_ratio),
            'calmar_ratio': float(calmar_ratio)
        }
    
    def _calculate_time_metrics(self, trades: List[Dict], equity_curve: pd.DataFrame) -> Dict[str, float]:
        """Calcular métricas temporales"""
        if not trades:
            return {'trades_per_day': 0.0, 'hold_time_avg': 0.0}
        
        # Calculate average holding time
        durations = [t.get('duration', 0) for t in trades if t.get('duration')]
        avg_hold_time = statistics.mean(durations) if durations else 0.0
        
        # Calculate trades per day
        if not equity_curve.empty and len(equity_curve) > 1:
            total_days = (equity_curve.index[-1] - equity_curve.index[0]).days
            trades_per_day = len(trades) / total_days if total_days > 0 else 0.0
        else:
            trades_per_day = 0.0
        
        return {
            'trades_per_day': float(trades_per_day),
            'hold_time_avg': float(avg_hold_time)
        }
    
    def _analyze_by_confidence(self, trades: List[Dict]) -> Dict[str, Any]:
        """Analizar trades por nivel de confianza"""
        confidence_buckets = {'high': [], 'medium': [], 'low': []}
        
        for trade in trades:
            confidence = trade.get('metadata', {}).get('confidence', 0.5)
            pnl = trade.get('pnl', 0)
            
            if confidence >= 0.8:
                confidence_buckets['high'].append(pnl)
            elif confidence >= 0.6:
                confidence_buckets['medium'].append(pnl)
            else:
                confidence_buckets['low'].append(pnl)
        
        analysis = {}
        for level, pnls in confidence_buckets.items():
            if pnls:
                winning = len([p for p in pnls if p > 0])
                analysis[level] = {
                    'trades': len(pnls),
                    'win_rate': winning / len(pnls),
                    'avg_pnl': statistics.mean(pnls),
                    'total_pnl': sum(pnls)
                }
            else:
                analysis[level] = {'trades': 0, 'win_rate': 0.0, 'avg_pnl': 0.0, 'total_pnl': 0.0}
        
        return analysis
    
    def _analyze_by_duration(self, trades: List[Dict]) -> Dict[str, Any]:
        """Analizar trades por duración"""
        duration_buckets = {'short': [], 'medium': [], 'long': []}
        
        for trade in trades:
            duration = trade.get('duration', 0)  # Hours
            pnl = trade.get('pnl', 0)
            
            if duration <= 4:
                duration_buckets['short'].append(pnl)
            elif duration <= 24:
                duration_buckets['medium'].append(pnl)
            else:
                duration_buckets['long'].append(pnl)
        
        analysis = {}
        for duration_type, pnls in duration_buckets.items():
            if pnls:
                winning = len([p for p in pnls if p > 0])
                analysis[duration_type] = {
                    'trades': len(pnls),
                    'win_rate': winning / len(pnls),
                    'avg_pnl': statistics.mean(pnls),
                    'total_pnl': sum(pnls)
                }
            else:
                analysis[duration_type] = {'trades': 0, 'win_rate': 0.0, 'avg_pnl': 0.0, 'total_pnl': 0.0}
        
        return analysis
    
    def _calculate_trade_efficiency(self, trades: List[Dict]) -> Dict[str, float]:
        """Calcular eficiencia de trades"""
        if not trades:
            return {'efficiency_ratio': 0.0, 'avg_bars_per_trade': 0.0}
        
        # Simple efficiency metrics
        total_pnl = sum([t.get('pnl', 0) for t in trades])
        total_trades = len(trades)
        
        # Efficiency ratio: PnL per trade
        efficiency_ratio = total_pnl / total_trades if total_trades > 0 else 0.0
        
        return {
            'efficiency_ratio': float(efficiency_ratio),
            'avg_bars_per_trade': float(statistics.mean([t.get('duration', 0) for t in trades])) if trades else 0.0
        }
