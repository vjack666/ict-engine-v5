"""
🎯 Risk Manager v6.0 Enterprise
==============================

Gestor de riesgo avanzado para el Backtest Engine v6.0.
Implementa múltiples estrategias de gestión de riesgo y capital.

Features:
- Position sizing basado en riesgo
- Límites de drawdown
- Gestión de correlaciones
- Risk-adjusted returns
- Máximo de posiciones concurrentes
- Stop Loss dinámicos
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


@dataclass
class RiskMetrics:
    """Métricas de riesgo"""
    max_risk_per_trade: float
    max_positions: int
    max_drawdown_percent: float
    max_daily_loss_percent: float
    correlation_limit: float
    volatility_adjustment: bool
    position_sizing_method: str  # 'fixed', 'percent_risk', 'kelly', 'volatility_adjusted'


class RiskManager:
    """
    🎯 Risk Manager v6.0 Enterprise
    
    Gestiona el riesgo de manera avanzada:
    - Position sizing inteligente
    - Límites de drawdown
    - Gestión de correlaciones
    - Ajustes por volatilidad
    """
    
    def __init__(self, max_risk_per_trade: float = 0.02, max_positions: int = 5,
                 max_drawdown_percent: float = 0.15, max_daily_loss_percent: float = 0.05):
        """
        Inicializar Risk Manager
        
        Args:
            max_risk_per_trade: Máximo riesgo por trade (como decimal, ej: 0.02 = 2%)
            max_positions: Máximo número de posiciones concurrentes
            max_drawdown_percent: Máximo drawdown permitido
            max_daily_loss_percent: Máxima pérdida diaria permitida
        """
        self.metrics = RiskMetrics(
            max_risk_per_trade=max_risk_per_trade,
            max_positions=max_positions,
            max_drawdown_percent=max_drawdown_percent,
            max_daily_loss_percent=max_daily_loss_percent,
            correlation_limit=0.7,
            volatility_adjustment=True,
            position_sizing_method='percent_risk'
        )
        
        # Track risk metrics
        self.daily_pnl_history: List[float] = []
        self.position_correlations: Dict[str, float] = {}
        self.volatility_window = 20
        self.kelly_lookback = 100
        
    def calculate_position_size(self, account_balance: float, entry_price: float,
                              stop_loss: float, risk_amount: Optional[float] = None) -> float:
        """
        Calcular tamaño de posición basado en riesgo
        
        Args:
            account_balance: Balance de la cuenta
            entry_price: Precio de entrada
            stop_loss: Nivel de stop loss
            risk_amount: Cantidad específica en riesgo (None = usar max_risk_per_trade)
            
        Returns:
            float: Tamaño de posición en lotes
        """
        if risk_amount is None:
            risk_amount = account_balance * self.metrics.max_risk_per_trade
        
        # Calculate risk per unit
        risk_per_unit = abs(entry_price - stop_loss)
        
        if risk_per_unit == 0:
            return 0.0
        
        # Calculate base position size
        if self.metrics.position_sizing_method == 'percent_risk':
            # Standard percent risk method
            position_value = risk_amount / risk_per_unit
            position_size = position_value / 100000  # Convert to lots (assuming EURUSD)
            
        elif self.metrics.position_sizing_method == 'kelly':
            # Kelly criterion sizing
            position_size = self._calculate_kelly_size(account_balance, entry_price, stop_loss)
            
        elif self.metrics.position_sizing_method == 'volatility_adjusted':
            # Volatility adjusted sizing
            position_size = self._calculate_volatility_adjusted_size(
                account_balance, entry_price, stop_loss, risk_amount
            )
            
        else:  # fixed
            position_size = 0.1  # Fixed 0.1 lots
        
        # Apply minimum and maximum position size limits
        position_size = max(0.01, min(position_size, 10.0))  # Min 0.01, Max 10 lots
        
        return round(position_size, 2)
    
    def can_open_position(self, current_positions: int, current_drawdown: float = 0.0,
                         daily_loss: float = 0.0) -> bool:
        """
        Verificar si se puede abrir una nueva posición
        
        Args:
            current_positions: Número actual de posiciones
            current_drawdown: Drawdown actual
            daily_loss: Pérdida del día actual
            
        Returns:
            bool: True si se puede abrir posición
        """
        # Check position limit
        if current_positions >= self.metrics.max_positions:
            return False
        
        # Check drawdown limit
        if current_drawdown > self.metrics.max_drawdown_percent:
            return False
        
        # Check daily loss limit
        if daily_loss > self.metrics.max_daily_loss_percent:
            return False
        
        return True
    
    def should_reduce_position_size(self, recent_losses: int, consecutive_losses: int) -> float:
        """
        Determinar si se debe reducir el tamaño de posición
        
        Args:
            recent_losses: Número de pérdidas recientes
            consecutive_losses: Número de pérdidas consecutivas
            
        Returns:
            float: Factor de reducción (1.0 = sin reducción, 0.5 = 50% reducción)
        """
        reduction_factor = 1.0
        
        # Reduce size after consecutive losses
        if consecutive_losses >= 3:
            reduction_factor *= 0.75  # 25% reduction
        
        if consecutive_losses >= 5:
            reduction_factor *= 0.5   # Additional 50% reduction
        
        # Reduce size if many recent losses
        if recent_losses >= 7:
            reduction_factor *= 0.8   # 20% reduction
        
        return max(0.1, reduction_factor)  # Minimum 10% of original size
    
    def calculate_dynamic_stop_loss(self, entry_price: float, volatility: float,
                                   direction: str, atr_period: int = 14) -> float:
        """
        Calcular stop loss dinámico basado en volatilidad
        
        Args:
            entry_price: Precio de entrada
            volatility: Volatilidad actual (ATR)
            direction: 'buy' or 'sell'
            atr_period: Período para ATR
            
        Returns:
            float: Nivel de stop loss dinámico
        """
        # Use 1.5x ATR as default stop distance
        atr_multiplier = 1.5
        stop_distance = volatility * atr_multiplier
        
        if direction == 'buy':
            return entry_price - stop_distance
        else:  # sell
            return entry_price + stop_distance
    
    def calculate_correlation_risk(self, positions: List[Dict], new_position_symbol: str) -> float:
        """
        Calcular riesgo de correlación
        
        Args:
            positions: Lista de posiciones actuales
            new_position_symbol: Símbolo de la nueva posición
            
        Returns:
            float: Score de riesgo de correlación (0.0 - 1.0)
        """
        if not positions:
            return 0.0
        
        # Simplified correlation calculation
        # In a real implementation, this would use historical correlation data
        correlation_risk = 0.0
        
        for position in positions:
            symbol = position.get('symbol', '')
            
            # Check for obvious correlations
            if self._symbols_are_correlated(symbol, new_position_symbol):
                correlation_risk += 0.3
        
        return min(1.0, correlation_risk)
    
    def update_daily_pnl(self, daily_pnl: float) -> None:
        """
        Actualizar PnL diario para tracking
        
        Args:
            daily_pnl: PnL del día
        """
        self.daily_pnl_history.append(daily_pnl)
        
        # Keep only last 30 days
        if len(self.daily_pnl_history) > 30:
            self.daily_pnl_history = self.daily_pnl_history[-30:]
    
    def get_risk_metrics(self) -> Dict[str, float]:
        """
        Obtener métricas de riesgo actuales
        
        Returns:
            Dict con métricas de riesgo
        """
        if not self.daily_pnl_history:
            return {
                'daily_var_95': 0.0,
                'max_daily_loss': 0.0,
                'volatility': 0.0,
                'sharpe_ratio': 0.0
            }
        
        daily_returns = np.array(self.daily_pnl_history)
        
        return {
            'daily_var_95': np.percentile(daily_returns, 5),  # 95% VaR
            'max_daily_loss': np.min(daily_returns),
            'volatility': np.std(daily_returns),
            'sharpe_ratio': np.mean(daily_returns) / np.std(daily_returns) if np.std(daily_returns) > 0 else 0.0
        }
    
    def _calculate_kelly_size(self, account_balance: float, entry_price: float, 
                             stop_loss: float) -> float:
        """
        Calcular tamaño usando criterio de Kelly
        
        Args:
            account_balance: Balance de cuenta
            entry_price: Precio de entrada
            stop_loss: Stop loss
            
        Returns:
            float: Tamaño de posición en lotes
        """
        # Simplified Kelly calculation
        # In practice, this would use historical win rate and average win/loss
        
        # Assume historical metrics (these would be calculated from trade history)
        win_rate = 0.6  # 60% win rate
        avg_win = 0.015  # 1.5% average win
        avg_loss = 0.01  # 1% average loss
        
        # Kelly fraction = (bp - q) / b
        # where b = odds received (avg_win/avg_loss), p = win probability, q = loss probability
        b = avg_win / avg_loss
        p = win_rate
        q = 1 - win_rate
        
        kelly_fraction = (b * p - q) / b
        kelly_fraction = max(0, min(kelly_fraction, 0.25))  # Cap at 25%
        
        # Convert to position size
        risk_amount = account_balance * kelly_fraction
        risk_per_unit = abs(entry_price - stop_loss)
        
        if risk_per_unit > 0:
            position_value = risk_amount / risk_per_unit
            return position_value / 100000  # Convert to lots
        
        return 0.1  # Default size
    
    def _calculate_volatility_adjusted_size(self, account_balance: float, entry_price: float,
                                          stop_loss: float, base_risk_amount: float) -> float:
        """
        Calcular tamaño ajustado por volatilidad
        
        Args:
            account_balance: Balance de cuenta
            entry_price: Precio de entrada
            stop_loss: Stop loss
            base_risk_amount: Cantidad base en riesgo
            
        Returns:
            float: Tamaño ajustado de posición
        """
        # Simplified volatility adjustment
        # In practice, this would use recent volatility measurements
        
        # Assume current volatility vs normal volatility
        current_volatility = 0.012  # 1.2% daily volatility
        normal_volatility = 0.010   # 1.0% normal volatility
        
        volatility_ratio = normal_volatility / current_volatility
        volatility_ratio = max(0.5, min(volatility_ratio, 2.0))  # Cap adjustment
        
        adjusted_risk = base_risk_amount * volatility_ratio
        risk_per_unit = abs(entry_price - stop_loss)
        
        if risk_per_unit > 0:
            position_value = adjusted_risk / risk_per_unit
            return position_value / 100000  # Convert to lots
        
        return 0.1  # Default size
    
    def _symbols_are_correlated(self, symbol1: str, symbol2: str) -> bool:
        """
        Verificar si dos símbolos están correlacionados
        
        Args:
            symbol1: Primer símbolo
            symbol2: Segundo símbolo
            
        Returns:
            bool: True si están correlacionados
        """
        # Simplified correlation detection
        major_pairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'AUDUSD', 'USDCAD', 'NZDUSD']
        
        # Same currency pairs are obviously correlated
        if symbol1 == symbol2:
            return True
        
        # Check for common currencies
        if len(symbol1) >= 6 and len(symbol2) >= 6:
            currency1_base = symbol1[:3]
            currency1_quote = symbol1[3:6]
            currency2_base = symbol2[:3]
            currency2_quote = symbol2[3:6]
            
            # Check if they share currencies
            if (currency1_base in [currency2_base, currency2_quote] or 
                currency1_quote in [currency2_base, currency2_quote]):
                return True
        
        return False
