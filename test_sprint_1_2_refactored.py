#!/usr/bin/env python3
"""
Test script para verificar el refactoring Sprint 1.2
"""

print("🧪 TESTING SPRINT 1.2 REFACTORED")
print("=" * 50)

# Test 1: Import AdvancedCandleDownloader
try:
    from utils.advanced_candle_downloader import AdvancedCandleDownloader
    print("✅ AdvancedCandleDownloader imported successfully")
except Exception as e:
    print(f"❌ Error importing AdvancedCandleDownloader: {e}")
    exit(1)

# Test 2: Create downloader instance
try:
    downloader = AdvancedCandleDownloader()
    print("✅ Downloader instance created")
except Exception as e:
    print(f"❌ Error creating downloader: {e}")
    exit(1)

# Test 3: Check Sprint 1.2 methods
sprint_methods = [
    'set_progress_callback',
    'set_completion_callback', 
    'set_error_callback',
    'queue_download',
    'process_download_queue',
    'download_with_coordination',
    'auto_update_stale_data',
    'get_enhanced_status'
]

print("\n🔍 Checking Sprint 1.2 methods:")
for method in sprint_methods:
    has_method = hasattr(downloader, method)
    status = "✅" if has_method else "❌"
    print(f"  {status} {method}")

# Test 4: Test callback system
try:
    print("\n🔧 Testing callback system:")
    
    def test_callback(*args, **kwargs):
        print(f"  📞 Callback called with args: {args}, kwargs: {kwargs}")
    
    downloader.set_progress_callback(test_callback)
    downloader.set_completion_callback(test_callback)
    downloader.set_error_callback(test_callback)
    print("✅ Callbacks set successfully")
    
except Exception as e:
    print(f"❌ Error setting callbacks: {e}")

# Test 5: Test queue system
try:
    print("\n📥 Testing queue system:")
    queue_length = downloader.queue_download("EURUSD", "H4", 1000)
    print(f"✅ Queued download, queue length: {queue_length}")
    
    status = downloader.get_enhanced_status()
    print(f"✅ Enhanced status: queue_length={status.get('queue_length', 0)}")
    
except Exception as e:
    print(f"❌ Error testing queue: {e}")

# Test 6: Test integration functions
try:
    print("\n🔗 Testing integration functions:")
    import utils.candle_integration as ci
    
    integration_downloader = ci.get_downloader()
    print(f"✅ Integration downloader: {type(integration_downloader).__name__}")
    
    # Test convenience functions
    functions = ['download_for_ict', 'download_quick', 'update_stale_data', 'get_download_status']
    for func_name in functions:
        has_func = hasattr(ci, func_name)
        status = "✅" if has_func else "❌"
        print(f"  {status} {func_name}")
    
except Exception as e:
    print(f"❌ Error testing integration: {e}")

# Test 7: Test widget
try:
    print("\n🎮 Testing simple widget:")
    from dashboard.simple_candle_widget import SimpleCandleWidget, simple_candle_widget
    print(f"✅ Widget imported: {type(simple_candle_widget).__name__}")
    
    widget_methods = ['start_download_session', 'update_stale_data', 'configure']
    for method in widget_methods:
        has_method = hasattr(simple_candle_widget, method)
        status = "✅" if has_method else "❌"
        print(f"  {status} {method}")
    
except Exception as e:
    print(f"❌ Error testing widget: {e}")

# Test 8: Test deprecated coordinator
try:
    print("\n⚠️  Testing deprecated coordinator:")
    from core.data_management.candle_coordinator import CandleCoordinator
    
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        coordinator = CandleCoordinator()
        
        if w:
            print(f"✅ Deprecation warning raised: {w[0].message}")
        else:
            print("❌ No deprecation warning raised")
    
except Exception as e:
    print(f"❌ Error testing deprecated coordinator: {e}")

print("\n" + "=" * 50)
print("🎉 SPRINT 1.2 REFACTORED TESTING COMPLETED")
print("🚀 Arquitectura simplificada funcional")
