#!/usr/bin/env python3
"""
Debug del test AdvancedCandleDownloader
=====================================
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def debug_performance_report():
    """🔍 Debug del reporte de performance"""
    try:
        from core.data_management.advanced_candle_downloader import get_advanced_candle_downloader
        
        config = {
            'enable_debug': True,
            'use_predictive_cache': True,
            'enable_lazy_loading': True,
            'max_concurrent': 2,
            'batch_size': 1000
        }
        
        downloader = get_advanced_candle_downloader(config)
        report = downloader.get_performance_report()
        
        print("🔍 REPORTE DE PERFORMANCE COMPLETO:")
        print("-" * 40)
        for key, value in report.items():
            print(f"{key}: {value}")
        print("-" * 40)
        
        print("\n🔍 VERIFICACIÓN ESPECÍFICA:")
        print(f"'sic_integration_active' existe: {'sic_integration_active' in report}")
        if 'sic_integration_active' in report:
            print(f"Valor: {report['sic_integration_active']} (tipo: {type(report['sic_integration_active'])})")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_performance_report()
