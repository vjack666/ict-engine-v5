#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 SIMPLE POI TEST - Identificar error exacto
"""

from sistema.sic import sys
from sistema.sic import os
import traceback

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    print("🔍 Importando módulos básicos...")
    from sistema.sic import enviar_senal_log
    from rich.table import Table
    from sistema.sic import datetime
    print("✅ Módulos básicos importados")

    print("🔍 Creando tabla simple...")
    tabla = Table(title="Test Simple", show_header=True, show_lines=True)
    tabla.add_column("ID", width=6)
    tabla.add_column("Tipo", width=12)
    tabla.add_row("001", "Test")
    print("✅ Tabla simple creada")

    print("🔍 Test logging...")
    enviar_senal_log("INFO", "Test simple logging", "simple_test", "testing")
    print("✅ Logging funcionando")

    print("🔍 Creando POI simulado simple...")
    poi_simple = {'id': 'POI_001', 'tipo': 'Support', 'precio': 1.1000, 'score': 8.5}
    print(f"POI creado: {poi_simple}")
    print(f"Tipo POI: {type(poi_simple)}")
    print(f"ID POI: {poi_simple.get('id')}")
    print("✅ POI simple funciona")

    print("🔍 Test con lista de POIs...")
    pois_list = [poi_simple]
    for poi in pois_list:
        print(f"Procesando POI: {type(poi)} - {poi}")
        id_poi = poi.get('id', 'default')
        print(f"ID extraído: {id_poi}")
    print("✅ Lista POIs funciona")

    print("🎉 TODOS LOS TESTS BÁSICOS EXITOSOS")

except Exception as e:
    print(f"❌ ERROR EN TEST SIMPLE: {e}")
    print("Stack trace:")
    print(traceback.format_exc())
