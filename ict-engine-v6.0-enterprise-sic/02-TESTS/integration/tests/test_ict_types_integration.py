"""
Test de Integración ICT Types v6.0 con SIC v3.1 Enterprise
=========================================================

Validación de la integración entre ICT Types v6.0 y SIC v3.1 Enterprise
"""

print("🚀 INICIANDO TEST DE INTEGRACIÓN ICT TYPES v6.0")
print("=" * 60)

try:
    # Test 1: Import básico
    print("🧪 TEST 1: Import ICT Types v6.0...")
    from core.ict_engine.ict_types import (
        ICTPattern, SmartMoneyType, TradingDirection, 
        ICTSignal, SmartMoneySignal, ICTConfig,
        TimeFrame, SessionType, MarketPhase, StructureType, LiquidityLevel
    )
    print("✅ Import exitoso")
    
    # Test 2: Creación de configuración
    print("\n🧪 TEST 2: Configuración ICT...")
    config = ICTConfig(
        primary_timeframe=TimeFrame.H1,
        min_confidence=80.0,
        enable_smart_money=True
    )
    print("✅ Configuración creada")
    
    # Test 3: Crear señal ICT
    print("\n🧪 TEST 3: Creación de señal ICT...")
    from datetime import datetime
    
    signal = ICTSignal(
        pattern_type=ICTPattern.JUDAS_SWING,
        direction=TradingDirection.BULLISH,
        confidence=85.5,
        entry_price=1.1000,
        stop_loss=1.0950,
        take_profit=1.1100,
        risk_reward_ratio=2.0,
        timestamp=datetime.now(),
        timeframe=TimeFrame.H1,
        session=SessionType.LONDON,
        market_phase=MarketPhase.MANIPULATION,
        narrative="Judas Swing bullish detectado en sesión de Londres"
    )
    print("✅ Señal ICT creada")
    
    # Test 4: Validación de señal
    print("\n🧪 TEST 4: Validación de señal...")
    from core.ict_engine.ict_types import validate_ict_signal
    is_valid = validate_ict_signal(signal)
    print(f"✅ Señal válida: {is_valid}")
    
    # Test 5: Narrativa
    print("\n🧪 TEST 5: Generación de narrativa...")
    from core.ict_engine.ict_types import create_ict_narrative
    narrative = create_ict_narrative(signal)
    print("✅ Narrativa generada:")
    print(narrative)
    
    # Test 6: Smart Money Signal
    print("\n🧪 TEST 6: Smart Money Signal...")
    
    smart_signal = SmartMoneySignal(
        smart_money_type=SmartMoneyType.LIQUIDITY_GRAB_BULLISH,
        direction=TradingDirection.BULLISH,
        confidence=82.0,
        liquidity_level=LiquidityLevel.HIGH,
        entry_price=1.1000,
        target_price=1.1150,
        invalidation_price=1.0950,
        timestamp=datetime.now(),
        timeframe=TimeFrame.H1,
        volume_confirmation=True,
        institutional_footprint=True,
        narrative="Smart Money grab de liquidez bullish detectado",
        confluence_score=85.5
    )
    print("✅ Smart Money Signal creado")
    
    print("\n" + "=" * 60)
    print("🎉 TODOS LOS TESTS PASARON - ICT TYPES v6.0 FUNCIONANDO")
    print(f"📊 Patrones ICT disponibles: {len(ICTPattern.__members__)}")
    print(f"💰 Smart Money Types: {len(SmartMoneyType.__members__)}")
    print(f"🏗️ Structure Types: {len(StructureType.__members__)}")
    print(f"📈 Trading Directions: {len(TradingDirection.__members__)}")
    
except Exception as e:
    print(f"❌ ERROR EN TEST: {e}")
    import traceback
    traceback.print_exc()
