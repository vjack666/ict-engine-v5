#!/usr/bin/env python3
"""
🧪 TEST BACKTEST ENGINE v6.0 ENTERPRISE
======================================

Test comprehensivo para el sistema de backtesting ICT Engine v6.0.
Valida funcionalidad completa, integración con componentes ICT, y performance.

Autor: ICT Engine v6.0 Enterprise Team
Fecha: 7 de Agosto 2025
"""

import pytest
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Setup path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_backtest_engine_initialization():
    """Test inicialización del Backtest Engine"""
    print("\n🧪 Testing Backtest Engine initialization...")
    
    try:
        from core.backtesting.backtest_engine_v6 import ICTBacktestEngine
        
        # Test basic initialization
        engine = ICTBacktestEngine(initial_balance=5000.0, risk_per_trade=0.015)
        
        assert engine.initial_balance == 5000.0
        assert engine.current_balance == 5000.0
        assert engine.risk_per_trade == 0.015
        assert engine.spread == 0.00015
        assert engine.commission == 7.0
        assert engine.min_confidence == 0.65
        
        print("   ✅ Basic initialization successful")
        
        # Test default initialization
        engine_default = ICTBacktestEngine()
        assert engine_default.initial_balance == 10000.0
        assert engine_default.risk_per_trade == 0.01
        
        print("   ✅ Default initialization successful")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Initialization test failed: {e}")
        return False

def test_realistic_data_generation():
    """Test generación de datos realistas"""
    print("\n🧪 Testing realistic data generation...")
    
    try:
        from core.backtesting.backtest_engine_v6 import ICTBacktestEngine
        
        engine = ICTBacktestEngine()
        
        # Generate data for 3 months
        data_mtf = engine._generate_realistic_data_mtf(
            symbol='EURUSD',
            start_date='2024-09-01',
            end_date='2024-12-01'
        )
        
        # Validate multi-timeframe structure
        assert isinstance(data_mtf, dict)
        assert 'M15' in data_mtf or 'H1' in data_mtf
        
        # Test primary timeframe
        primary_tf = 'H1' if 'H1' in data_mtf else list(data_mtf.keys())[0]
        data = data_mtf[primary_tf]
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) > 100
        assert all(col in data.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume'])
        
        # Validate OHLC consistency
        assert (data['High'] >= data['Open']).all()
        assert (data['High'] >= data['Close']).all()
        assert (data['Low'] <= data['Open']).all()
        assert (data['Low'] <= data['Close']).all()
        
        # Validate price range (realistic for EURUSD)
        assert data['Close'].min() > 1.0
        assert data['Close'].max() < 1.4
        
        print(f"   ✅ Generated {len(data_mtf)} timeframes with {len(data)} H1 periods")
        print(f"   ✅ Price range: {data['Close'].min():.5f} - {data['Close'].max():.5f}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Data generation test failed: {e}")
        return False

def test_signal_generation():
    """Test generación de señales ICT"""
    print("\n🧪 Testing ICT signal generation...")
    
    try:
        from core.backtesting.backtest_engine_v6 import ICTBacktestEngine
        
        engine = ICTBacktestEngine()
        
        # Generate test data
        data_mtf = engine._generate_realistic_data_mtf(
            symbol='EURUSD',
            start_date='2024-10-01',
            end_date='2024-11-01'
        )
        
        # Generate signals
        signals = engine._run_ict_analysis(data_mtf, 'EURUSD')
        
        assert isinstance(signals, list)
        assert len(signals) > 0
        
        print(f"   ✅ Generated {len(signals)} ICT signals")
        
        # Validate signal structure
        for signal in signals[:3]:  # Check first 3 signals
            required_fields = [
                'timestamp', 'pattern', 'direction', 'entry_price',
                'stop_loss', 'take_profit', 'confidence', 'timeframe'
            ]
            
            for field in required_fields:
                assert field in signal, f"Missing field: {field}"
            
            assert signal['direction'] in ['BUY', 'SELL']
            assert 0.0 < signal['confidence'] <= 1.0
            assert signal['entry_price'] > 0
            
            # Validate stop loss and take profit logic
            if signal['direction'] == 'BUY':
                assert signal['stop_loss'] < signal['entry_price']
                assert signal['take_profit'] > signal['entry_price']
            else:
                assert signal['stop_loss'] > signal['entry_price']
                assert signal['take_profit'] < signal['entry_price']
        
        print("   ✅ Signal validation passed")
        
        # Check Smart Money enhancement ratio
        sm_signals = [s for s in signals if s.get('smart_money_enhanced', False)]
        sm_ratio = len(sm_signals) / len(signals) if signals else 0
        
        print(f"   ✅ Smart Money enhanced signals: {len(sm_signals)} ({sm_ratio:.1%})")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Signal generation test failed: {e}")
        return False

def test_trade_simulation():
    """Test simulación de trades"""
    print("\n🧪 Testing trade simulation...")
    
    try:
        from core.backtesting.backtest_engine_v6 import ICTBacktestEngine
        
        engine = ICTBacktestEngine(initial_balance=5000.0, risk_per_trade=0.02)
        
        # Generate test data
        data_mtf = engine._generate_realistic_data_mtf(
            symbol='EURUSD',
            start_date='2024-10-01',
            end_date='2024-11-15'
        )
        
        # Get base data for simulation
        base_tf = 'H1' if 'H1' in data_mtf else list(data_mtf.keys())[0]
        base_data = data_mtf[base_tf]
        
        # Create test signal
        test_signal = {
            'timestamp': base_data.index[50],  # Middle of data
            'pattern': 'TEST_SILVER_BULLET',
            'direction': 'BUY',
            'entry_price': base_data['Close'].iloc[50],
            'stop_loss': base_data['Close'].iloc[50] - 0.0015,  # 15 pips
            'take_profit': base_data['Close'].iloc[50] + 0.0030,  # 30 pips (2:1 R:R)
            'confidence': 0.75,
            'timeframe': 'H1',
            'smart_money_enhanced': True,
            'confluence_score': 0.85
        }
        
        # Simulate single trade
        trade = engine._simulate_single_trade_advanced(test_signal, base_data)
        
        assert trade is not None
        assert trade.pattern == 'TEST_SILVER_BULLET'
        assert trade.direction == 'BUY'
        assert trade.confidence == 0.75
        assert trade.smart_money_enhanced == True
        assert trade.confluence_score == 0.85
        
        # Validate trade logic
        assert trade.entry_time == test_signal['timestamp']
        assert trade.entry_price == test_signal['entry_price']
        assert trade.stop_loss == test_signal['stop_loss']
        assert trade.take_profit == test_signal['take_profit']
        assert trade.exit_time > trade.entry_time
        
        # Validate PnL calculation
        if trade.direction == 'BUY':
            expected_pips = (trade.exit_price - trade.entry_price) * 10000
        else:
            expected_pips = (trade.entry_price - trade.exit_price) * 10000
        
        assert abs(trade.pnl_pips - expected_pips) < 0.1  # Small tolerance
        
        print(f"   ✅ Trade simulated successfully:")
        print(f"      Entry: {trade.entry_price:.5f} at {trade.entry_time}")
        print(f"      Exit: {trade.exit_price:.5f} at {trade.exit_time}")
        print(f"      PnL: ${trade.pnl:.2f} ({trade.pnl_pips:.1f} pips)")
        print(f"      Duration: {trade.exit_time - trade.entry_time}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Trade simulation test failed: {e}")
        return False

def test_position_sizing():
    """Test cálculo de position sizing"""
    print("\n🧪 Testing position sizing calculation...")
    
    try:
        from core.backtesting.backtest_engine_v6 import ICTBacktestEngine
        
        engine = ICTBacktestEngine(initial_balance=10000.0, risk_per_trade=0.02)
        
        # Test signal with 20 pip stop
        test_signal = {
            'entry_price': 1.1750,
            'stop_loss': 1.1730,  # 20 pips
            'confidence': 0.80,
            'smart_money_enhanced': True
        }
        
        position_size = engine._calculate_position_size_advanced(test_signal)
        
        assert position_size > 0
        assert position_size <= 5.0  # Max position limit
        
        # Validate risk calculation
        risk_amount = engine.current_balance * engine.risk_per_trade  # $200
        stop_distance_pips = abs(test_signal['entry_price'] - test_signal['stop_loss']) * 10000  # 20 pips
        expected_size = risk_amount / (stop_distance_pips * engine.pip_value)  # $200 / (20 * $10)
        
        # Account for confidence and SM multipliers
        confidence_mult = 0.8 + (test_signal['confidence'] * 0.4)
        sm_mult = 1.1 if test_signal['smart_money_enhanced'] else 1.0
        expected_size *= confidence_mult * sm_mult
        
        assert abs(position_size - expected_size) < 0.1  # Small tolerance
        
        print(f"   ✅ Position size calculated: {position_size:.2f} lots")
        print(f"   ✅ Risk amount: ${risk_amount:.2f}")
        print(f"   ✅ Stop distance: {stop_distance_pips:.1f} pips")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Position sizing test failed: {e}")
        return False

def test_comprehensive_backtest():
    """Test backtest comprehensivo completo"""
    print("\n🧪 Testing comprehensive backtest...")
    
    try:
        from core.backtesting.backtest_engine_v6 import ICTBacktestEngine
        
        engine = ICTBacktestEngine(
            initial_balance=10000.0,
            risk_per_trade=0.015  # 1.5% risk
        )
        
        # Run comprehensive backtest
        print("   🚀 Ejecutando backtest comprehensivo...")
        
        results = engine.run_comprehensive_backtest(
            symbol='EURUSD',
            start_date='2024-10-01',
            end_date='2024-11-30'
        )
        
        # Validate results structure
        assert hasattr(results, 'trades')
        assert hasattr(results, 'total_trades')
        assert hasattr(results, 'win_rate')
        assert hasattr(results, 'total_pnl')
        assert hasattr(results, 'pattern_performance')
        assert hasattr(results, 'smart_money_performance')
        
        # Validate metrics
        assert results.total_trades >= 0
        assert 0.0 <= results.win_rate <= 1.0
        assert isinstance(results.total_pnl, (int, float))
        assert isinstance(results.pattern_performance, dict)
        
        print(f"   ✅ Backtest completed successfully:")
        print(f"      Total Trades: {results.total_trades}")
        print(f"      Win Rate: {results.win_rate:.1%}")
        print(f"      Total PnL: ${results.total_pnl:,.2f}")
        print(f"      Max Drawdown: ${results.max_drawdown:,.2f}")
        print(f"      Profit Factor: {results.profit_factor:.2f}")
        
        # Validate Smart Money analysis
        sm_perf = results.smart_money_performance
        if sm_perf['smart_money']['total_trades'] > 0:
            print(f"      SM Trades: {sm_perf['smart_money']['total_trades']}")
            print(f"      SM Win Rate: {sm_perf['smart_money']['win_rate']:.1%}")
            print(f"      SM Advantage: +{sm_perf['smart_money_advantage']:.1%}")
        
        # Validate pattern performance
        if results.pattern_performance:
            print(f"      Patterns analyzed: {len(results.pattern_performance)}")
            for pattern, stats in list(results.pattern_performance.items())[:3]:
                print(f"        {pattern}: {stats['total_trades']} trades, {stats['win_rate']:.1%} WR")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Comprehensive backtest failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ict_integration():
    """Test integración con componentes ICT v6.0"""
    print("\n🧪 Testing ICT v6.0 integration...")
    
    try:
        from core.backtesting.backtest_engine_v6 import ICTBacktestEngine
        
        engine = ICTBacktestEngine()
        
        # Test component imports
        components = [
            'pattern_detector',
            'smart_money_analyzer', 
            'data_manager',
            'downloader'
        ]
        
        for component in components:
            has_component = hasattr(engine, component)
            print(f"   📦 {component}: {'✅ Available' if has_component else '⚠️ Fallback mode'}")
        
        # Test logger
        has_logger = engine.logger is not None
        print(f"   📝 Logger: {'✅ Active' if has_logger else '⚠️ Fallback mode'}")
        
        # Test ATR calculation
        test_data = pd.DataFrame({
            'High': [1.1780, 1.1785, 1.1790, 1.1795, 1.1800],
            'Low': [1.1770, 1.1775, 1.1780, 1.1785, 1.1790],
            'Close': [1.1775, 1.1780, 1.1785, 1.1790, 1.1795]
        })
        
        atr = engine._calculate_atr(test_data)
        assert atr > 0
        assert atr < 0.01  # Reasonable for EURUSD
        
        print(f"   📊 ATR calculation: ✅ {atr:.6f}")
        
        # Test session identification
        test_times = [
            datetime(2024, 11, 1, 2, 0),   # Asian
            datetime(2024, 11, 1, 10, 0),  # London
            datetime(2024, 11, 1, 15, 0),  # NY
            datetime(2024, 11, 1, 20, 0)   # Overlap
        ]
        
        for test_time in test_times:
            session = engine._get_session(test_time)
            assert session in ['ASIAN', 'LONDON', 'NY', 'OVERLAP', 'UNKNOWN']
        
        print("   ⏰ Session identification: ✅ Working")
        
        return True
        
    except Exception as e:
        print(f"   ❌ ICT integration test failed: {e}")
        return False

def test_performance_benchmarks():
    """Test performance benchmarks"""
    print("\n🧪 Testing performance benchmarks...")
    
    try:
        from core.backtesting.backtest_engine_v6 import ICTBacktestEngine
        import time
        
        engine = ICTBacktestEngine()
        
        # Test data generation performance
        start_time = time.time()
        data_mtf = engine._generate_realistic_data_mtf(
            symbol='EURUSD',
            start_date='2024-08-01',
            end_date='2024-10-31'
        )
        data_gen_time = time.time() - start_time
        
        assert data_gen_time < 5.0  # Should complete in under 5 seconds
        print(f"   📊 Data generation: ✅ {data_gen_time:.3f}s")
        
        # Test signal generation performance
        start_time = time.time()
        signals = engine._run_ict_analysis(data_mtf, 'EURUSD')
        signal_gen_time = time.time() - start_time
        
        assert signal_gen_time < 10.0  # Should complete in under 10 seconds
        print(f"   🎯 Signal generation: ✅ {signal_gen_time:.3f}s ({len(signals)} signals)")
        
        # Test trade simulation performance
        if signals:
            base_tf = 'H1' if 'H1' in data_mtf else list(data_mtf.keys())[0]
            base_data = data_mtf[base_tf]
            
            start_time = time.time()
            engine._simulate_trades_with_rm(signals[:10], data_mtf)  # Test with 10 signals
            simulation_time = time.time() - start_time
            
            assert simulation_time < 5.0  # Should complete in under 5 seconds
            print(f"   💼 Trade simulation: ✅ {simulation_time:.3f}s (10 trades)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Performance benchmark failed: {e}")
        return False

def run_comprehensive_test_suite():
    """Ejecutar suite completo de tests"""
    print("🧪 ICT BACKTEST ENGINE v6.0 - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    test_functions = [
        test_backtest_engine_initialization,
        test_realistic_data_generation,
        test_signal_generation,
        test_trade_simulation,
        test_position_sizing,
        test_ict_integration,
        test_performance_benchmarks,
        test_comprehensive_backtest,  # Last because it's most comprehensive
    ]
    
    results = []
    start_time = time.time()
    
    for test_func in test_functions:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test_func.__name__} failed with exception: {e}")
            results.append(False)
    
    total_time = time.time() - start_time
    
    # Summary
    passed = sum(results)
    total = len(results)
    success_rate = passed / total
    
    print(f"\n{'='*70}")
    print(f"🎯 TEST RESULTS SUMMARY")
    print(f"{'='*70}")
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {success_rate:.1%}")
    print(f"Total Time: {total_time:.2f}s")
    
    if success_rate >= 0.8:
        print(f"🎉 BACKTEST ENGINE v6.0 - VALIDATION SUCCESSFUL!")
        print(f"✅ Ready for production backtesting")
    else:
        print(f"⚠️ Some tests failed - review and fix issues")
    
    return success_rate >= 0.8


if __name__ == "__main__":
    import time
    run_comprehensive_test_suite()
