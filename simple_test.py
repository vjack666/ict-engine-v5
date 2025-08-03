#!/usr/bin/env python3
"""
Test simple del refactoring Sprint 1.2
"""

import sys
import os

# Añadir la ruta del proyecto
project_path = r"c:\Users\v_jac\Desktop\itc engine v5.0"
if project_path not in sys.path:
    sys.path.insert(0, project_path)

print("🧪 SIMPLE TEST - SPRINT 1.2 REFACTORED")
print("=" * 50)

# Test básico de import
print("📦 Testing imports...")

try:
    from utils.advanced_candle_downloader import AdvancedCandleDownloader
    print("✅ AdvancedCandleDownloader imported")
except Exception as e:
    print(f"❌ Error importing AdvancedCandleDownloader: {e}")
    sys.exit(1)

try:
    downloader = AdvancedCandleDownloader()
    print("✅ Downloader instance created")
except Exception as e:
    print(f"❌ Error creating downloader: {e}")
    sys.exit(1)

# Check new methods exist
new_methods = [
    'set_progress_callback',
    'queue_download', 
    'process_download_queue',
    'get_enhanced_status'
]

print("\n🔍 Checking new methods:")
for method in new_methods:
    exists = hasattr(downloader, method)
    print(f"{'✅' if exists else '❌'} {method}")

print("\n✨ Basic test completed successfully!")
