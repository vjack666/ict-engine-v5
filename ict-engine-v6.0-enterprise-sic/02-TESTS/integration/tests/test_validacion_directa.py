#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 VALIDACIÓN DIRECTA ICT COMPLIANCE
===================================

Validación directa del sistema sin parsing de output.
"""

import sys
from pathlib import Path

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def validacion_directa():
    """🎯 Validación directa del sistema"""
    
    print("🎯 ICT ENGINE v6.0 - VALIDACIÓN DIRECTA")
    print("="*60)
    
    try:
        # Test directo del POI System
        from core.poi_system import POISystem
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        
        print("1️⃣ Inicializando sistema...")
        downloader = AdvancedCandleDownloader()
        poi_system = POISystem(downloader=downloader)
        
        print("2️⃣ Descargando datos EURUSD M15...")
        data = downloader.download_candle_data("EURUSD", "M15", 3000)
        
        if data is not None and len(data) > 0:
            velas_count = len(data)
            print(f"✅ Descargadas: {velas_count} velas")
            
            if velas_count >= 2000:
                print("✅ ICT COMPLIANCE: MINIMUM+ (≥2000 velas)")
                
                print("3️⃣ Detectando POIs...")
                pois = poi_system.detect_pois("EURUSD", "M15")
                pois_count = len(pois) if pois else 0
                
                print(f"✅ POIs detectados: {pois_count}")
                
                if pois_count >= 20:
                    print("✅ DETECCIÓN POI: EXITOSA")
                    
                    print("\n" + "="*60)
                    print("🎉 VALIDACIÓN EXITOSA - SISTEMA COMPLETO")
                    print("="*60)
                    print(f"📊 Datos: {velas_count} velas ICT compliant")
                    print(f"🎯 POIs: {pois_count} puntos de interés")
                    print("✅ Sistema listo para trading institucional")
                    return True
                else:
                    print(f"⚠️ DETECCIÓN POI: LIMITADA ({pois_count} < 20)")
            else:
                print(f"❌ ICT NON-COMPLIANCE: {velas_count} < 2000 velas")
        else:
            print("❌ NO SE PUDIERON DESCARGAR DATOS")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        
    print("\n❌ VALIDACIÓN FALLIDA")
    return False

if __name__ == "__main__":
    success = validacion_directa()
    sys.exit(0 if success else 1)
