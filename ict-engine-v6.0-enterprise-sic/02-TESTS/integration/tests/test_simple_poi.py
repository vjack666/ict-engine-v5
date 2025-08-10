# -*- coding: utf-8 -*-
"""
🧪 TEST SIMPLE POI SYSTEM - Verificar mensajes MT5
"""

import sys
from pathlib import Path

# Añadir path del proyecto
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def test_simple():
    print("=== TEST SIMPLE POI SYSTEM ===")
    
    try:
        from core.analysis.poi_system import get_poi_system
        
        # Test con debug habilitado para ver mensajes
        print("\n1. Test con debug ON:")
        poi_system_debug = get_poi_system({
            'enable_debug': True, 
            'min_poi_strength': 60.0
        })
        
        pois_debug = poi_system_debug.detect_pois("EURUSD", "M15", 2)
        print(f"   Detectados: {len(pois_debug)} POIs")
        
        # Test con debug deshabilitado
        print("\n2. Test con debug OFF:")
        poi_system_clean = get_poi_system({
            'enable_debug': False, 
            'min_poi_strength': 60.0
        })
        
        pois_clean = poi_system_clean.detect_pois("EURUSD", "M15", 2)
        print(f"   Detectados: {len(pois_clean)} POIs")
        
        print(f"\nRESULTADO: Sistema funcional - {len(pois_debug)} POIs detectados")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    test_simple()
