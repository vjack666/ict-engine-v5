"""
🎯 ICT Backtest Engine v6.0 Enterprise
======================================

Motor principal de backtesting que integra completamente con el ICT Engine v6.0.
Utiliza Pattern Detector, Smart Money Concepts y Multi-Timeframe Analysis para
ejecutar backtests profesionales y detallados.

Features:
- Integración nativa con ICT Engine v6.0
- Multi-timeframe backtesting
- Smart Money Concepts integration
- Real data simulation
- Enterprise performance analytics
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import pandas as pd
import numpy as np
from dataclasses import dataclass, field

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
from core.analysis.pattern_detector import PatternDetector
from core.smart_money_concepts.smart_money_analyzer import SmartMoneyAnalyzer
from utils.smart_trading_logger import SmartTradingLogger
from .trading_simulator import TradingSimulator
from .risk_manager import RiskManager
from .performance_analyzer import PerformanceAnalyzer


@dataclass
class BacktestConfig:
    """Configuración para el backtest"""
    symbol: str = "EURUSD"
    primary_timeframe: str = "M15"
    context_timeframes: List[str] = field(default_factory=lambda: ["H1", "H4", "D1"])
    start_date: datetime = field(default_factory=lambda: datetime.now() - timedelta(days=30))
    end_date: datetime = field(default_factory=lambda: datetime.now())
    initial_balance: float = 10000.0
    risk_per_trade: float = 1.0  # Percentage
    max_positions: int = 3
    commission_per_lot: float = 7.0  # USD per lot
    spread_points: int = 2
    slippage_points: int = 1
    enable_smart_money: bool = True
    enable_multi_timeframe: bool = True


@dataclass
class BacktestResults:
    """Resultados del backtest"""
    config: BacktestConfig
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate: float = 0.0
    total_pnl: float = 0.0
    max_drawdown: float = 0.0
    sharpe_ratio: float = 0.0
    profit_factor: float = 0.0
    avg_trade: float = 0.0
    avg_winner: float = 0.0
    avg_loser: float = 0.0
    largest_winner: float = 0.0
    largest_loser: float = 0.0
    max_consecutive_wins: int = 0
    max_consecutive_losses: int = 0
    execution_time: float = 0.0
    patterns_detected: int = 0
    smart_money_signals: int = 0
    trades_history: List[Dict] = field(default_factory=list)
    equity_curve: pd.DataFrame = field(default_factory=pd.DataFrame)


class BacktestEngine:
    """
    🎯 ICT Backtest Engine v6.0 Enterprise
    
    Motor principal de backtesting que integra completamente con:
    - Pattern Detector v6.0
    - Smart Money Analyzer v6.0  
    - Multi-Timeframe Analysis
    - Advanced Risk Management
    - Real Data Simulation
    """
    
    def __init__(self, config: BacktestConfig):
        """
        Inicializar Backtest Engine v6.0 Enterprise
        
        Args:
            config: Configuración del backtest
        """
        self.config = config
        self.logger = SmartTradingLogger("BacktestEngine")
        
        # Initialize core components
        self.logger.info("🎯 Inicializando Backtest Engine v6.0 Enterprise...")
        
        # Data downloader
        self.downloader = AdvancedCandleDownloader()
        
        # Pattern detection
        self.pattern_detector = PatternDetector()
        
        # Smart Money analyzer (if enabled)
        self.smart_money_analyzer = None
        if config.enable_smart_money:
            self.smart_money_analyzer = SmartMoneyAnalyzer()
            
        # Trading simulator
        self.simulator = TradingSimulator(
            initial_balance=config.initial_balance,
            commission_per_lot=config.commission_per_lot,
            spread_points=config.spread_points,
            slippage_points=config.slippage_points
        )
        
        # Risk manager
        self.risk_manager = RiskManager(
            max_risk_per_trade=config.risk_per_trade / 100,
            max_positions=config.max_positions
        )
        
        # Performance analyzer
        self.performance_analyzer = PerformanceAnalyzer()
        
        # Data storage
        self.market_data: Dict[str, pd.DataFrame] = {}
        self.current_bar_index = 0
        self.total_bars = 0
        
        self.logger.info("✅ Backtest Engine v6.0 Enterprise inicializado")
        self.logger.info(f"   Symbol: {config.symbol}")
        self.logger.info(f"   Primary TF: {config.primary_timeframe}")
        self.logger.info(f"   Context TFs: {config.context_timeframes}")
        self.logger.info(f"   Period: {config.start_date.date()} to {config.end_date.date()}")
        self.logger.info(f"   Initial Balance: ${config.initial_balance:,.2f}")
        
    def download_data(self) -> bool:
        """
        Descargar datos de mercado para el backtest
        
        Returns:
            bool: True si la descarga fue exitosa
        """
        try:
            self.logger.info("📥 Descargando datos de mercado...")
            
            # Download primary timeframe data
            primary_result = self.downloader.download_candles(
                symbol=self.config.symbol,
                timeframe=self.config.primary_timeframe,
                start_date=self.config.start_date,
                end_date=self.config.end_date
            )
            
            # Handle different return types from downloader
            if isinstance(primary_result, dict) and 'data' in primary_result:
                primary_data = primary_result['data']
            elif isinstance(primary_result, dict) and 'candles' in primary_result:
                primary_data = primary_result['candles']
            else:
                primary_data = primary_result
            
            if primary_data is None or (hasattr(primary_data, 'empty') and primary_data.empty):
                self.logger.error(f"❌ No se pudieron descargar datos para {self.config.symbol} {self.config.primary_timeframe}")
                return False
                
            self.market_data[self.config.primary_timeframe] = primary_data
            self.total_bars = len(primary_data)
            
            self.logger.info(f"✅ Datos primarios descargados: {len(primary_data)} velas {self.config.primary_timeframe}")
            
            # Download context timeframe data (if multi-timeframe enabled)
            if self.config.enable_multi_timeframe:
                for tf in self.config.context_timeframes:
                    context_result = self.downloader.download_candles(
                        symbol=self.config.symbol,
                        timeframe=tf,
                        start_date=self.config.start_date,
                        end_date=self.config.end_date
                    )
                    
                    # Handle different return types from downloader
                    if isinstance(context_result, dict) and 'data' in context_result:
                        context_data = context_result['data']
                    elif isinstance(context_result, dict) and 'candles' in context_result:
                        context_data = context_result['candles']
                    else:
                        context_data = context_result
                    
                    if context_data is not None and not (hasattr(context_data, 'empty') and context_data.empty):
                        self.market_data[tf] = context_data
                        self.logger.info(f"✅ Datos contexto descargados: {len(context_data)} velas {tf}")
                    else:
                        self.logger.warning(f"⚠️ No se pudieron descargar datos para {tf}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error descargando datos: {e}")
            return False
    
    def run_backtest(self) -> BacktestResults:
        """
        Ejecutar backtest completo
        
        Returns:
            BacktestResults: Resultados detallados del backtest
        """
        start_time = datetime.now()
        self.logger.info("🚀 Iniciando backtest...")
        
        # Download data
        if not self.download_data():
            raise RuntimeError("No se pudieron descargar los datos de mercado")
        
        # Get primary data
        primary_data = self.market_data[self.config.primary_timeframe]
        
        # Initialize counters
        patterns_detected = 0
        smart_money_signals = 0
        
        # Main backtest loop
        self.logger.info(f"🔄 Procesando {self.total_bars} velas...")
        
        for i, (timestamp, candle) in enumerate(primary_data.iterrows()):
            self.current_bar_index = i
            
            # Skip first few bars to allow for lookback
            if i < 50:
                continue
                
            # Update simulator with current price
            current_price = float(candle['close'])
            self.simulator.update_current_price(current_price, timestamp)
            
            # Get historical data up to current point
            historical_data = self._get_historical_data(i)
            
            # Detect patterns - Pass historical data to avoid redundant downloads
            patterns = self.pattern_detector.detect_patterns(
                data=historical_data[self.config.primary_timeframe],
                symbol=self.config.symbol,
                timeframe=self.config.primary_timeframe
            )
            
            if patterns:
                patterns_detected += len(patterns)
                
                # Apply Smart Money enhancement if enabled
                if self.config.enable_smart_money and self.smart_money_analyzer:
                    enhanced_patterns = self.smart_money_analyzer.enhance_patterns(
                        patterns, historical_data
                    )
                    smart_money_signals += len([p for p in enhanced_patterns if p.smart_money_confidence > 0.7])
                else:
                    enhanced_patterns = patterns
                
                # Apply Multi-Timeframe enhancement if enabled
                if self.config.enable_multi_timeframe:
                    enhanced_patterns = self._apply_multi_timeframe_enhancement(
                        enhanced_patterns, historical_data
                    )
                
                # Generate trading signals
                signals = self._generate_trading_signals(enhanced_patterns, current_price)
                
                # Execute trades
                for signal in signals:
                    self._execute_trade_signal(signal, current_price, timestamp)
            
            # Progress logging
            if i % 1000 == 0:
                progress = (i / self.total_bars) * 100
                self.logger.info(f"📊 Progreso: {progress:.1f}% ({i}/{self.total_bars})")
        
        # Calculate final results
        execution_time = (datetime.now() - start_time).total_seconds()
        results = self._calculate_results(patterns_detected, smart_money_signals, execution_time)
        
        self.logger.info("✅ Backtest completado")
        self.logger.info(f"⏱️ Tiempo de ejecución: {execution_time:.2f}s")
        self.logger.info(f"📊 Patterns detectados: {patterns_detected}")
        self.logger.info(f"💰 Smart Money signals: {smart_money_signals}")
        self.logger.info(f"🎯 Total trades: {results.total_trades}")
        self.logger.info(f"💵 PnL total: ${results.total_pnl:.2f}")
        
        return results
    
    def _get_historical_data(self, current_index: int) -> Dict[str, pd.DataFrame]:
        """
        Obtener datos históricos hasta el punto actual
        
        Args:
            current_index: Índice actual en los datos primarios
            
        Returns:
            Dict con datos históricos por timeframe
        """
        historical = {}
        
        # Primary timeframe
        primary_data = self.market_data[self.config.primary_timeframe]
        historical[self.config.primary_timeframe] = primary_data.iloc[:current_index + 1]
        
        # Context timeframes
        if self.config.enable_multi_timeframe:
            current_timestamp = primary_data.index[current_index]
            
            for tf in self.config.context_timeframes:
                if tf in self.market_data:
                    context_data = self.market_data[tf]
                    # Get data up to current timestamp
                    mask = context_data.index <= current_timestamp
                    historical[tf] = context_data[mask]
        
        return historical
    
    def _apply_multi_timeframe_enhancement(self, patterns: List, historical_data: Dict[str, pd.DataFrame]) -> List:
        """
        Aplicar mejoras multi-timeframe a los patterns
        
        Args:
            patterns: Lista de patterns detectados
            historical_data: Datos históricos por timeframe
            
        Returns:
            Lista de patterns mejorados
        """
        # This would integrate with the existing multi-timeframe logic
        # from the Pattern Detector v6.0
        enhanced_patterns = []
        
        for pattern in patterns:
            # Apply multi-timeframe context
            pattern.multi_tf_confirmation = self._check_multi_tf_context(pattern, historical_data)
            enhanced_patterns.append(pattern)
        
        return enhanced_patterns
    
    def _check_multi_tf_context(self, pattern, historical_data: Dict[str, pd.DataFrame]) -> float:
        """
        Verificar contexto multi-timeframe para un pattern
        
        Args:
            pattern: Pattern a verificar
            historical_data: Datos históricos
            
        Returns:
            float: Confirmación multi-timeframe (0.0 - 1.0)
        """
        # Simplified multi-timeframe confirmation logic
        confirmations = 0
        total_checks = 0
        
        for tf in self.config.context_timeframes:
            if tf in historical_data and not historical_data[tf].empty:
                # Check trend alignment, support/resistance, etc.
                # This is a simplified version - the full logic would be more complex
                total_checks += 1
                if self._check_tf_alignment(pattern, historical_data[tf]):
                    confirmations += 1
        
        return confirmations / total_checks if total_checks > 0 else 0.0
    
    def _check_tf_alignment(self, pattern, tf_data: pd.DataFrame) -> bool:
        """
        Verificar alineación con timeframe específico
        
        Args:
            pattern: Pattern a verificar
            tf_data: Datos del timeframe
            
        Returns:
            bool: True si hay alineación
        """
        # Simplified alignment check
        if tf_data.empty or len(tf_data) < 10:
            return False
            
        # Check trend direction
        recent_data = tf_data.tail(10)
        trend_up = recent_data['close'].iloc[-1] > recent_data['close'].iloc[0]
        
        # Pattern should align with higher timeframe trend
        if hasattr(pattern, 'direction'):
            pattern_bullish = pattern.direction == 'bullish'
            return pattern_bullish == trend_up
        
        return True  # Default to true if can't determine
    
    def _generate_trading_signals(self, patterns: List, current_price: float) -> List[Dict]:
        """
        Generar señales de trading basadas en patterns
        
        Args:
            patterns: Lista de patterns detectados
            current_price: Precio actual
            
        Returns:
            Lista de señales de trading
        """
        signals = []
        
        for pattern in patterns:
            # Check if pattern is actionable
            if self._is_pattern_actionable(pattern, current_price):
                signal = self._pattern_to_signal(pattern, current_price)
                if signal:
                    signals.append(signal)
        
        return signals
    
    def _is_pattern_actionable(self, pattern, current_price: float) -> bool:
        """
        Verificar si un pattern es accionable
        
        Args:
            pattern: Pattern a verificar
            current_price: Precio actual
            
        Returns:
            bool: True si es accionable
        """
        # Check pattern quality - Handle enum confidence values
        if hasattr(pattern, 'confidence'):
            # Convert enum confidence to numeric for comparison
            confidence_values = {
                'low': 0.3,
                'medium': 0.6,
                'high': 0.8,
                'very_high': 0.9,
                'extreme': 0.95
            }
            
            confidence_value = 0.0
            if hasattr(pattern.confidence, 'value'):
                confidence_value = confidence_values.get(pattern.confidence.value, 0.0)
            else:
                confidence_value = confidence_values.get(str(pattern.confidence).lower(), 0.0)
            
            if confidence_value < 0.7:
                return False
        
        # Check if price is near pattern level
        if hasattr(pattern, 'level'):
            distance = abs(current_price - pattern.level) / current_price
            if distance > 0.001:  # More than 10 pips for EURUSD
                return False
        
        # Check multi-timeframe confirmation
        if hasattr(pattern, 'multi_tf_confirmation') and pattern.multi_tf_confirmation < 0.5:
            return False
        
        return True
    
    def _pattern_to_signal(self, pattern, current_price: float) -> Optional[Dict]:
        """
        Convertir pattern a señal de trading
        
        Args:
            pattern: Pattern detectado
            current_price: Precio actual
            
        Returns:
            Dict con la señal de trading o None
        """
        if not hasattr(pattern, 'pattern_type') or not hasattr(pattern, 'direction'):
            return None
        
        # Determine trade direction
        if pattern.direction == 'bullish':
            side = 'buy'
        elif pattern.direction == 'bearish':
            side = 'sell'
        else:
            return None
        
        # Calculate position size
        position_size = self.risk_manager.calculate_position_size(
            account_balance=self.simulator.get_balance(),
            entry_price=current_price,
            stop_loss=getattr(pattern, 'stop_loss', current_price * 0.995),  # Default 0.5% SL
            risk_amount=self.config.risk_per_trade / 100
        )
        
        return {
            'side': side,
            'size': position_size,
            'entry_price': current_price,
            'stop_loss': getattr(pattern, 'stop_loss', current_price * (0.995 if side == 'buy' else 1.005)),
            'take_profit': getattr(pattern, 'take_profit', current_price * (1.01 if side == 'buy' else 0.99)),
            'pattern_type': pattern.pattern_type,
            'confidence': getattr(pattern, 'confidence', 0.5),
            'smart_money_confidence': getattr(pattern, 'smart_money_confidence', 0.0)
        }
    
    def _execute_trade_signal(self, signal: Dict, current_price: float, timestamp) -> None:
        """
        Ejecutar señal de trading
        
        Args:
            signal: Señal de trading
            current_price: Precio actual
            timestamp: Timestamp actual
        """
        # Check if we can open new position
        if not self.risk_manager.can_open_position(
            current_positions=len(self.simulator.get_open_positions())
        ):
            return
        
        # Execute trade in simulator
        self.simulator.open_position(
            side=signal['side'],
            size=signal['size'],
            entry_price=signal['entry_price'],
            stop_loss=signal['stop_loss'],
            take_profit=signal['take_profit'],
            timestamp=timestamp,
            metadata={
                'pattern_type': signal['pattern_type'],
                'confidence': signal['confidence'],
                'smart_money_confidence': signal['smart_money_confidence']
            }
        )
    
    def _calculate_results(self, patterns_detected: int, smart_money_signals: int, 
                          execution_time: float) -> BacktestResults:
        """
        Calcular resultados finales del backtest
        
        Args:
            patterns_detected: Número de patterns detectados
            smart_money_signals: Número de señales Smart Money
            execution_time: Tiempo de ejecución
            
        Returns:
            BacktestResults: Resultados completos
        """
        # Get trade history
        trades = self.simulator.get_trade_history()
        
        # Calculate basic metrics
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t.get('pnl', 0) > 0])
        losing_trades = len([t for t in trades if t.get('pnl', 0) < 0])
        
        # Use performance analyzer for detailed calculations
        detailed_metrics = self.performance_analyzer.calculate_metrics(
            trades, self.simulator.get_equity_curve()
        )
        
        return BacktestResults(
            config=self.config,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=detailed_metrics.get('win_rate', 0.0),
            total_pnl=detailed_metrics.get('total_pnl', 0.0),
            max_drawdown=detailed_metrics.get('max_drawdown', 0.0),
            sharpe_ratio=detailed_metrics.get('sharpe_ratio', 0.0),
            profit_factor=detailed_metrics.get('profit_factor', 0.0),
            avg_trade=detailed_metrics.get('avg_trade', 0.0),
            avg_winner=detailed_metrics.get('avg_winner', 0.0),
            avg_loser=detailed_metrics.get('avg_loser', 0.0),
            largest_winner=detailed_metrics.get('largest_winner', 0.0),
            largest_loser=detailed_metrics.get('largest_loser', 0.0),
            max_consecutive_wins=detailed_metrics.get('max_consecutive_wins', 0),
            max_consecutive_losses=detailed_metrics.get('max_consecutive_losses', 0),
            execution_time=execution_time,
            patterns_detected=patterns_detected,
            smart_money_signals=smart_money_signals,
            trades_history=trades,
            equity_curve=self.simulator.get_equity_curve()
        )
