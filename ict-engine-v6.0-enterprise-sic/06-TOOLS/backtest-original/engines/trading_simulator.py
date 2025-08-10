"""
🎯 Trading Simulator v6.0 Enterprise
===================================

Simulador de trading realista para el Backtest Engine v6.0.
Simula ejecución de trades con spread, slippage, comisiones y gestión de posiciones.

Features:
- Simulación realista de ejecución
- Gestión de spread y slippage
- Cálculo de comisiones
- Tracking de equity curve
- Gestión de múltiples posiciones
- Stop Loss y Take Profit automáticos
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import pandas as pd
import uuid


@dataclass
class Position:
    """Representa una posición abierta"""
    id: str
    side: str  # 'buy' or 'sell'
    size: float  # Lot size
    entry_price: float
    current_price: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    open_time: datetime = field(default_factory=datetime.now)
    unrealized_pnl: float = 0.0
    commission: float = 0.0
    swap: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def update_price(self, new_price: float, spread_points: int = 0):
        """Actualizar precio actual y PnL"""
        self.current_price = new_price
        
        # Calculate unrealized PnL
        if self.side == 'buy':
            # For buy positions, subtract spread from current price
            effective_price = new_price - (spread_points * 0.0001)  # Assuming 4-digit broker
            self.unrealized_pnl = (effective_price - self.entry_price) * 100000 * self.size  # EURUSD pip value
        else:  # sell
            # For sell positions, add spread to current price
            effective_price = new_price + (spread_points * 0.0001)
            self.unrealized_pnl = (self.entry_price - effective_price) * 100000 * self.size
    
    def should_close_sl(self) -> bool:
        """Verificar si debe cerrar por Stop Loss"""
        if self.stop_loss is None:
            return False
        
        if self.side == 'buy':
            return self.current_price <= self.stop_loss
        else:
            return self.current_price >= self.stop_loss
    
    def should_close_tp(self) -> bool:
        """Verificar si debe cerrar por Take Profit"""
        if self.take_profit is None:
            return False
        
        if self.side == 'buy':
            return self.current_price >= self.take_profit
        else:
            return self.current_price <= self.take_profit


@dataclass
class Trade:
    """Representa un trade cerrado"""
    id: str
    side: str
    size: float
    entry_price: float
    exit_price: float
    open_time: datetime
    close_time: datetime
    pnl: float
    commission: float
    swap: float
    close_reason: str  # 'manual', 'stop_loss', 'take_profit'
    duration: float  # Hours
    metadata: Dict[str, Any] = field(default_factory=dict)


class TradingSimulator:
    """
    🎯 Trading Simulator v6.0 Enterprise
    
    Simula ejecución de trades de manera realista incluyendo:
    - Spread y slippage
    - Comisiones
    - Gestión de múltiples posiciones
    - Stop Loss y Take Profit automáticos
    - Tracking de equity curve
    """
    
    def __init__(self, initial_balance: float = 10000.0, commission_per_lot: float = 7.0,
                 spread_points: int = 2, slippage_points: int = 1):
        """
        Inicializar Trading Simulator
        
        Args:
            initial_balance: Balance inicial
            commission_per_lot: Comisión por lote en USD
            spread_points: Spread en points (1 point = 0.0001 for 4-digit)
            slippage_points: Slippage en points
        """
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.commission_per_lot = commission_per_lot
        self.spread_points = spread_points
        self.slippage_points = slippage_points
        
        # Positions and trades
        self.open_positions: Dict[str, Position] = {}
        self.closed_trades: List[Trade] = []
        
        # Equity curve tracking
        self.equity_history: List[Dict] = []
        self.current_timestamp = datetime.now()
        self.current_price = 0.0
        
        # Statistics
        self.total_commission_paid = 0.0
        self.total_swap_paid = 0.0
        self.max_equity = initial_balance
        self.min_equity = initial_balance
        
    def update_current_price(self, price: float, timestamp: datetime) -> None:
        """
        Actualizar precio actual y timestamp
        
        Args:
            price: Precio actual
            timestamp: Timestamp actual
        """
        self.current_price = price
        self.current_timestamp = timestamp
        
        # Update all open positions
        for position in self.open_positions.values():
            position.update_price(price, self.spread_points)
        
        # Check for automatic closures (SL/TP)
        self._check_automatic_closures()
        
        # Update equity curve
        self._update_equity_curve()
    
    def open_position(self, side: str, size: float, entry_price: Optional[float] = None,
                     stop_loss: Optional[float] = None, take_profit: Optional[float] = None,
                     timestamp: Optional[datetime] = None, metadata: Optional[Dict] = None) -> str:
        """
        Abrir nueva posición
        
        Args:
            side: 'buy' or 'sell'
            size: Tamaño en lotes
            entry_price: Precio de entrada (None = precio de mercado)
            stop_loss: Nivel de Stop Loss
            take_profit: Nivel de Take Profit
            timestamp: Timestamp de apertura
            metadata: Metadata adicional
            
        Returns:
            str: ID de la posición
        """
        if entry_price is None:
            entry_price = self.current_price
        
        if timestamp is None:
            timestamp = self.current_timestamp
        
        if metadata is None:
            metadata = {}
        
        # Apply spread and slippage
        effective_entry_price = self._apply_execution_costs(entry_price, side, True)
        
        # Calculate commission
        commission = self.commission_per_lot * size
        
        # Check if we have enough balance
        required_margin = self._calculate_margin(size, effective_entry_price)
        if self.get_free_margin() < required_margin:
            return ""  # Not enough margin
        
        # Create position
        position_id = str(uuid.uuid4())
        position = Position(
            id=position_id,
            side=side,
            size=size,
            entry_price=effective_entry_price,
            current_price=effective_entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            open_time=timestamp,
            commission=commission,
            metadata=metadata
        )
        
        # Add to open positions
        self.open_positions[position_id] = position
        
        # Deduct commission
        self.balance -= commission
        self.total_commission_paid += commission
        
        return position_id
    
    def close_position(self, position_id: str, exit_price: Optional[float] = None,
                      close_reason: str = 'manual') -> Optional[Trade]:
        """
        Cerrar posición
        
        Args:
            position_id: ID de la posición
            exit_price: Precio de cierre (None = precio de mercado)
            close_reason: Razón del cierre
            
        Returns:
            Trade: Trade cerrado o None si no existe
        """
        if position_id not in self.open_positions:
            return None
        
        position = self.open_positions[position_id]
        
        if exit_price is None:
            exit_price = self.current_price
        
        # Apply spread and slippage
        effective_exit_price = self._apply_execution_costs(exit_price, position.side, False)
        
        # Calculate PnL
        if position.side == 'buy':
            pnl = (effective_exit_price - position.entry_price) * 100000 * position.size
        else:
            pnl = (position.entry_price - effective_exit_price) * 100000 * position.size
        
        # Calculate duration
        duration = (self.current_timestamp - position.open_time).total_seconds() / 3600
        
        # Create trade record
        trade = Trade(
            id=position.id,
            side=position.side,
            size=position.size,
            entry_price=position.entry_price,
            exit_price=effective_exit_price,
            open_time=position.open_time,
            close_time=self.current_timestamp,
            pnl=pnl,
            commission=position.commission,
            swap=position.swap,
            close_reason=close_reason,
            duration=duration,
            metadata=position.metadata
        )
        
        # Update balance
        self.balance += pnl
        
        # Remove from open positions and add to closed trades
        del self.open_positions[position_id]
        self.closed_trades.append(trade)
        
        return trade
    
    def close_all_positions(self, close_reason: str = 'manual') -> List[Trade]:
        """
        Cerrar todas las posiciones abiertas
        
        Args:
            close_reason: Razón del cierre
            
        Returns:
            List[Trade]: Lista de trades cerrados
        """
        closed_trades = []
        position_ids = list(self.open_positions.keys())
        
        for position_id in position_ids:
            trade = self.close_position(position_id, close_reason=close_reason)
            if trade:
                closed_trades.append(trade)
        
        return closed_trades
    
    def get_balance(self) -> float:
        """Obtener balance actual"""
        return self.balance
    
    def get_equity(self) -> float:
        """Obtener equity actual (balance + PnL no realizado)"""
        unrealized_pnl = sum(pos.unrealized_pnl for pos in self.open_positions.values())
        return self.balance + unrealized_pnl
    
    def get_free_margin(self) -> float:
        """Obtener margen libre"""
        used_margin = sum(self._calculate_margin(pos.size, pos.entry_price) 
                         for pos in self.open_positions.values())
        return self.get_equity() - used_margin
    
    def get_open_positions(self) -> List[Position]:
        """Obtener lista de posiciones abiertas"""
        return list(self.open_positions.values())
    
    def get_trade_history(self) -> List[Dict]:
        """Obtener historial de trades como lista de diccionarios"""
        return [
            {
                'id': trade.id,
                'side': trade.side,
                'size': trade.size,
                'entry_price': trade.entry_price,
                'exit_price': trade.exit_price,
                'open_time': trade.open_time,
                'close_time': trade.close_time,
                'pnl': trade.pnl,
                'commission': trade.commission,
                'swap': trade.swap,
                'close_reason': trade.close_reason,
                'duration': trade.duration,
                'metadata': trade.metadata
            }
            for trade in self.closed_trades
        ]
    
    def get_equity_curve(self) -> pd.DataFrame:
        """Obtener curva de equity como DataFrame"""
        if not self.equity_history:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.equity_history)
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
        
        return df
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas del simulador"""
        return {
            'initial_balance': self.initial_balance,
            'current_balance': self.balance,
            'current_equity': self.get_equity(),
            'max_equity': self.max_equity,
            'min_equity': self.min_equity,
            'total_commission_paid': self.total_commission_paid,
            'total_swap_paid': self.total_swap_paid,
            'open_positions': len(self.open_positions),
            'total_trades': len(self.closed_trades),
            'current_price': self.current_price
        }
    
    def _apply_execution_costs(self, price: float, side: str, is_opening: bool) -> float:
        """
        Aplicar costos de ejecución (spread y slippage)
        
        Args:
            price: Precio base
            side: 'buy' or 'sell'
            is_opening: True si es apertura, False si es cierre
            
        Returns:
            float: Precio efectivo después de costos
        """
        # Convert points to price units
        spread_cost = self.spread_points * 0.0001
        slippage_cost = self.slippage_points * 0.0001
        
        if side == 'buy':
            if is_opening:
                # Buy at ask + slippage
                return price + spread_cost + slippage_cost
            else:
                # Close buy at bid - slippage
                return price - slippage_cost
        else:  # sell
            if is_opening:
                # Sell at bid - slippage
                return price - slippage_cost
            else:
                # Close sell at ask + slippage
                return price + spread_cost + slippage_cost
    
    def _calculate_margin(self, size: float, price: float) -> float:
        """
        Calcular margen requerido para una posición
        
        Args:
            size: Tamaño en lotes
            price: Precio
            
        Returns:
            float: Margen requerido
        """
        # Simplified margin calculation (1:100 leverage)
        return (size * 100000 * price) / 100
    
    def _check_automatic_closures(self) -> None:
        """Verificar y ejecutar cierres automáticos (SL/TP)"""
        positions_to_close = []
        
        for position_id, position in self.open_positions.items():
            if position.should_close_sl():
                positions_to_close.append((position_id, 'stop_loss'))
            elif position.should_close_tp():
                positions_to_close.append((position_id, 'take_profit'))
        
        # Close positions
        for position_id, reason in positions_to_close:
            self.close_position(position_id, close_reason=reason)
    
    def _update_equity_curve(self) -> None:
        """Actualizar curva de equity"""
        current_equity = self.get_equity()
        
        # Update max/min equity
        if current_equity > self.max_equity:
            self.max_equity = current_equity
        if current_equity < self.min_equity:
            self.min_equity = current_equity
        
        # Add to equity history
        self.equity_history.append({
            'timestamp': self.current_timestamp,
            'balance': self.balance,
            'equity': current_equity,
            'unrealized_pnl': current_equity - self.balance,
            'open_positions': len(self.open_positions),
            'price': self.current_price
        })
