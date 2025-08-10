#!/usr/bin/env python3
"""
🔴 EXTRACTOR DE CONTENIDO DE PESTAÑAS - BLACKBOX LOGGER
====================================================
Extrae y muestra todo el contenido completo de las pestañas capturado por BlackBox Logger
"""

import json
import os
from pathlib import Path

def extract_tab_content_from_blackbox():
    """Extraer todo el contenido de pestañas de la última sesión BlackBox"""
    
    # Buscar la última sesión
    blackbox_dir = Path("logs/blackbox")
    if not blackbox_dir.exists():
        print("❌ No se encontró directorio BlackBox")
        return
    
    # Obtener la sesión más reciente
    sessions = [d for d in blackbox_dir.iterdir() if d.is_dir()]
    if not sessions:
        print("❌ No se encontraron sesiones BlackBox")
        return
    
    latest_session = max(sessions, key=lambda x: x.stat().st_mtime)
    print(f"🔍 Analizando sesión: {latest_session.name}")
    
    # Leer el reporte comprehensivo
    comprehensive_report = latest_session / "COMPREHENSIVE_DEBUG_REPORT.json"
    if not comprehensive_report.exists():
        print("❌ No se encontró reporte comprehensivo")
        return
    
    with open(comprehensive_report, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n🔴 CONTENIDO COMPLETO DE PESTAÑAS - SESSION {latest_session.name}")
    print("=" * 80)
    
    # Extraer información de renders
    render_events = data.get('render_events', [])
    tab_events = data.get('tab_content_events', [])
    
    print(f"\n📊 RESUMEN:")
    print(f"• Renders capturados: {len(render_events)}")
    print(f"• Tab events capturados: {len(tab_events)}")
    print(f"• Duración sesión: {data['session_info']['duration_seconds']:.2f}s")
    
    # Mostrar contenido por pestaña
    tabs_found = {}
    
    for event in render_events:
        method_name = event.get('method_name', '')
        content_preview = event.get('content_preview', '')
        content_length = event.get('content_length', 0)
        success = event.get('success', False)
        
        if 'render_' in method_name:
            tab_name = method_name.replace('render_', '')
            tabs_found[tab_name] = {
                'preview': content_preview,
                'length': content_length,
                'success': success,
                'full_method': method_name
            }
    
    for event in tab_events:
        tab_name = event.get('tab_name', '')
        method_name = event.get('method_name', '')
        success = event.get('success', False)
        content_length = event.get('content_length', 0)
        
        if tab_name and tab_name not in tabs_found:
            tabs_found[tab_name] = {
                'preview': f"Tab content from {method_name}",
                'length': content_length,
                'success': success,
                'full_method': method_name
            }
    
    print(f"\n🎯 PESTAÑAS DETECTADAS: {len(tabs_found)}")
    print("-" * 80)
    
    for tab_name, info in tabs_found.items():
        status = "✅ EXITOSO" if info['success'] else "❌ FALLIDO"
        print(f"\n📋 PESTAÑA: {tab_name.upper()}")
        print(f"   Status: {status}")
        print(f"   Método: {info['full_method']}")
        print(f"   Longitud: {info['length']} caracteres")
        print(f"   Preview: {info['preview'][:150]}...")
        
        if info['length'] > 0:
            print(f"   ✅ CONTENIDO CAPTURADO CORRECTAMENTE")
        else:
            print(f"   ❌ SIN CONTENIDO")
    
    # Buscar contenido completo en logs individuales
    print(f"\n🔍 BUSCANDO CONTENIDO COMPLETO EN LOGS...")
    
    render_log = latest_session / "blackbox_render.log"
    if render_log.exists():
        with open(render_log, 'r', encoding='utf-8') as f:
            render_content = f.read()
        
        print(f"\n📄 CONTENIDO RENDER LOG ({len(render_content)} caracteres):")
        print("-" * 80)
        
        # Extraer y mostrar los renders individuales
        lines = render_content.split('\n')
        current_render = None
        
        for line in lines:
            if 'RENDER_SUCCESS' in line and 'render_' in line:
                parts = line.split('|')
                if len(parts) >= 4:
                    method = parts[1].strip()
                    length = parts[2].strip()
                    preview = parts[3].strip() if len(parts) > 3 else ""
                    
                    print(f"\n🎯 {method}:")
                    print(f"   Longitud: {length}")
                    print(f"   Preview: {preview}")
    
    # Mostrar archivos disponibles
    print(f"\n📁 ARCHIVOS BLACKBOX DISPONIBLES:")
    for file in latest_session.iterdir():
        if file.is_file():
            size = file.stat().st_size
            print(f"   📄 {file.name} ({size} bytes)")
    
    print(f"\n🔴 ANÁLISIS COMPLETO - TODO EL CONTENIDO ESTÁ EN LA CAJA NEGRA")
    print(f"📍 Ubicación: {latest_session}")

if __name__ == "__main__":
    extract_tab_content_from_blackbox()
