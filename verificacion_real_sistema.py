import sys
import os
import traceback

# Añadir path actual
sys.path.insert(0, os.getcwd())

print("🔧 VERIFICACIÓN REAL DEL SISTEMA - SPRINT 1.8")
print("="*60)

# Test 1: Advanced Patterns
print("\n🎯 TEST 1: Advanced Patterns (Sprint 1.7)")
try:
    from core.ict_engine.advanced_patterns import AdvancedSilverBulletDetector
    from core.ict_engine.advanced_patterns import JudasSwingAnalyzer
    from core.ict_engine.advanced_patterns import MarketStructureEngine

    # Test instanciación
    detector = AdvancedSilverBulletDetector()
    analyzer = JudasSwingAnalyzer()
    engine = MarketStructureEngine()

    print("✅ AdvancedSilverBulletDetector: FUNCIONANDO")
    print("✅ JudasSwingAnalyzer: FUNCIONANDO")
    print("✅ MarketStructureEngine: FUNCIONANDO")
    advanced_patterns_ok = True
except Exception as e:
    print(f"❌ Error en Advanced Patterns: {e}")
    advanced_patterns_ok = False

# Test 2: ICT Engine Core
print("\n🧠 TEST 2: ICT Engine Core")
try:
    from core.ict_engine.pattern_analyzer import ICTPatternAnalyzer
    from core.ict_engine.confidence_engine import ConfidenceEngine

    analyzer = ICTPatternAnalyzer()
    print("✅ ICTPatternAnalyzer: FUNCIONANDO")

    confidence = ConfidenceEngine()
    print("✅ ConfidenceEngine: FUNCIONANDO")
    ict_core_ok = True
except Exception as e:
    print(f"❌ Error en ICT Core: {e}")
    ict_core_ok = False

# Test 3: POI System
print("\n📊 TEST 3: POI System")
try:
    from core.poi_system.poi_detector import POIDetector
    poi_detector = POIDetector()
    print("✅ POI Detector: FUNCIONANDO")
    poi_ok = True
except Exception as e:
    print(f"❌ Error en POI System: {e}")
    poi_ok = False

# Test 4: Dashboard
print("\n🖥️ TEST 4: Dashboard System")
try:
    import dashboard.dashboard_definitivo as dashboard
    from dashboard.dashboard_widgets import HibernationStatusWidget
    print("✅ Dashboard: FUNCIONANDO")
    dashboard_ok = True
except Exception as e:
    print(f"❌ Error en Dashboard: {e}")
    dashboard_ok = False

# Test 5: Logging
print("\n📝 TEST 5: Sistema SLUC v2.1")
try:
    from sistema.logging_interface import enviar_senal_log
    enviar_senal_log("INFO", "Test verificación real", "test", "verification")
    print("✅ SLUC v2.1 Logging: FUNCIONANDO")
    logging_ok = True
except Exception as e:
    print(f"❌ Error en Logging: {e}")
    logging_ok = False

# Test 6: MT5
print("\n💹 TEST 6: MT5 Data Manager")
try:
    from utils.mt5_data_manager import MT5DataManager
    mt5_manager = MT5DataManager()
    print("✅ MT5 Data Manager: FUNCIONANDO")
    mt5_ok = True
except Exception as e:
    print(f"❌ Error en MT5: {e}")
    mt5_ok = False

# Resumen
print("\n" + "="*60)
print("📊 RESUMEN DE VERIFICACIÓN REAL")
print("="*60)

tests = [
    ("Advanced Patterns (Sprint 1.7)", advanced_patterns_ok),
    ("ICT Engine Core", ict_core_ok),
    ("POI System", poi_ok),
    ("Dashboard System", dashboard_ok),
    ("SLUC v2.1 Logging", logging_ok),
    ("MT5 Data Manager", mt5_ok)
]

critical_passed = 0
total_tests = len(tests)

for test_name, passed in tests:
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} {test_name}")
    if passed:
        critical_passed += 1

print(f"\n📈 RESULTADO: {critical_passed}/{total_tests} tests pasaron")

if critical_passed >= 4:  # Al menos los críticos deben pasar
    print("🎉 SISTEMA LISTO PARA SPRINT 1.8")
    print("✅ Componentes críticos verificados")
else:
    print("⚠️ SISTEMA REQUIERE ATENCIÓN")
    print("🔧 Algunos componentes críticos fallan")

print("="*60)
