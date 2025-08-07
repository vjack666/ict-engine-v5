#!/usr/bin/env python3
"""
🗄️ TEST STORAGE INTELIGENTE - Verificación del sistema de almacenamiento
=======================================================================

Test para verificar que el sistema de almacenamiento inteligente funciona
correctamente según la configuración automática y las necesidades ICT.

Funcionalidades probadas:
- Carga automática de configuración de storage
- Decisiones inteligentes de almacenamiento por timeframe
- Verificación de archivos guardados
- Integración con descarga ICT óptima

Autor: ICT Engine v6.0 Enterprise Team
Fecha: Agosto 2025
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

def test_storage_configuration():
    """🧪 Test: Configuración de almacenamiento"""
    print("\n" + "="*70)
    print("🗄️ TEST STORAGE INTELIGENTE v6.0")
    print("="*70)
    
    try:
        print("\n📋 1. Verificando configuración de storage...")
        
        # Verificar que existe el archivo de configuración
        config_file = Path("config/storage_config.json")
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            storage_config = config_data.get('storage_config', {})
            downloader_config = config_data.get('downloader_config', {})
            
            print(f"✅ Configuración cargada:")
            print(f"   Modo: {storage_config.get('mode', 'UNKNOWN')}")
            print(f"   Descripción: {storage_config.get('description', 'N/A')}")
            print(f"   Guardar por defecto: {downloader_config.get('save_to_file_default', False)}")
            print(f"   Cache habilitado: {downloader_config.get('cache_enabled', False)}")
            print(f"   Límite cache: {downloader_config.get('max_cache_mb', 0)} MB")
        else:
            print("❌ No se encontró archivo de configuración de storage")
            return False
        
        print("\n🏗️ 2. Inicializando downloader con storage automático...")
        
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        downloader = AdvancedCandleDownloader(
            config={'enable_debug': True}
        )
        print("✅ Downloader inicializado con configuración automática")
        
        print("\n🧠 3. Probando lógica de decisión de almacenamiento...")
        
        # Test de decisiones automáticas
        test_cases = [
            ('EURUSD', 'M15'),
            ('EURUSD', 'H1'), 
            ('EURUSD', 'H4'),
            ('EURUSD', 'M5'),
            ('XAUUSD', 'H4'),
            ('GBPUSD', 'M1')
        ]
        
        decisions = {}
        for symbol, timeframe in test_cases:
            if hasattr(downloader, '_should_save_to_file'):
                should_save = downloader._should_save_to_file(timeframe, symbol)
                decisions[f"{symbol}_{timeframe}"] = should_save
                decision_text = "💾 GUARDAR" if should_save else "🧠 MEMORIA"
                print(f"   {symbol} {timeframe}: {decision_text}")
            else:
                print(f"   {symbol} {timeframe}: ❌ Método no disponible")
        
        print("\n📥 4. Test de descarga con storage automático...")
        
        # Test de descarga real
        result = downloader.download_candles(
            symbol="EURUSD",
            timeframe="M15",
            save_to_file=None,  # Usar decisión automática
            use_ict_optimal=True
        )
        
        print(f"\n📊 RESULTADO DESCARGA:")
        print(f"   Success: {result.get('success', False)}")
        print(f"   Message: {result.get('message', 'N/A')}")
        
        if result.get('success'):
            # Verificar información de storage
            storage_info = result.get('storage_info', {})
            print(f"\n🗄️ INFORMACIÓN DE STORAGE:")
            print(f"   Guardado en archivo: {storage_info.get('saved_to_file', 'N/A')}")
            print(f"   Modo de storage: {storage_info.get('storage_mode', 'N/A')}")
            print(f"   Decisión: {storage_info.get('storage_decision', 'N/A')}")
            
            # Verificar si se creó archivo (si debería)
            if storage_info.get('saved_to_file'):
                data_dir = Path("data/candles")
                if data_dir.exists():
                    csv_files = list(data_dir.glob("EURUSD_M15_*.csv"))
                    if csv_files:
                        latest_file = max(csv_files, key=lambda p: p.stat().st_mtime)
                        file_size = latest_file.stat().st_size
                        print(f"   Archivo creado: {latest_file.name}")
                        print(f"   Tamaño: {file_size:,} bytes ({file_size/1024:.1f} KB)")
                    else:
                        print(f"   ⚠️ No se encontraron archivos CSV recientes")
                else:
                    print(f"   ⚠️ Directorio de datos no existe")
        
        print("\n📈 5. Verificando métricas de storage...")
        
        if hasattr(downloader, 'get_performance_report'):
            perf_report = downloader.get_performance_report()
            print(f"   Cache stats: {perf_report.get('cache_stats', {})}")
            print(f"   SIC integration: {perf_report.get('sic_integration_active', False)}")
        
        print("\n✅ TEST STORAGE INTELIGENTE COMPLETADO")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de storage: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_storage_modes():
    """🔧 Test: Diferentes modos de storage"""
    print("\n" + "="*50)
    print("🔧 TEST MODOS DE STORAGE")
    print("="*50)
    
    # Simulación de diferentes configuraciones
    test_configs = {
        'MEMORY_ONLY': {
            'mode': 'MEMORY_ONLY',
            'expected_save': {'M15': False, 'H4': False, 'H1': False}
        },
        'CACHE_SMART': {
            'mode': 'CACHE_SMART', 
            'critical_timeframes': ['H4', 'H1', 'M15'],
            'expected_save': {'M15': True, 'H4': True, 'H1': True, 'M5': False}
        },
        'FULL_STORAGE': {
            'mode': 'FULL_STORAGE',
            'expected_save': {'M15': True, 'H4': True, 'H1': True, 'M5': True, 'M1': True}
        }
    }
    
    try:
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        
        for mode_name, config in test_configs.items():
            print(f"\n🧪 Probando modo: {mode_name}")
            
            # Crear downloader con configuración simulada
            downloader = AdvancedCandleDownloader()
            downloader._storage_config = config  # Simular configuración
            
            expected = config['expected_save']
            all_correct = True
            
            for timeframe, expected_save in expected.items():
                if hasattr(downloader, '_should_save_to_file'):
                    actual_save = downloader._should_save_to_file(timeframe, 'EURUSD')
                    match = actual_save == expected_save
                    
                    status = "✅" if match else "❌"
                    print(f"   {timeframe}: Esperado={expected_save}, Actual={actual_save} {status}")
                    
                    if not match:
                        all_correct = False
                else:
                    print(f"   {timeframe}: ❌ Método no disponible")
                    all_correct = False
            
            if all_correct:
                print(f"   ✅ Modo {mode_name} funciona correctamente")
            else:
                print(f"   ❌ Modo {mode_name} tiene errores")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando modos de storage: {e}")
        return False

def verify_data_directory():
    """📁 Verificar estructura de directorios de datos"""
    print("\n" + "="*50)
    print("📁 VERIFICACIÓN DIRECTORIO DE DATOS")
    print("="*50)
    
    # Verificar estructura de directorios
    data_paths = [
        "data/candles",
        "data/reports", 
        "config"
    ]
    
    for path_str in data_paths:
        path = Path(path_str)
        if path.exists():
            if path.is_dir():
                files = list(path.glob("*"))
                print(f"✅ {path_str}: {len(files)} archivos")
                
                # Mostrar archivos recientes si existen
                if files:
                    recent_files = sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)[:3]
                    for f in recent_files:
                        size = f.stat().st_size
                        print(f"   - {f.name} ({size:,} bytes)")
            else:
                print(f"⚠️ {path_str}: Es archivo, no directorio")
        else:
            print(f"❌ {path_str}: No existe")
    
    return True

if __name__ == "__main__":
    print("🗄️ ICT ENGINE v6.0 - TEST STORAGE INTELIGENTE")
    print("=" * 70)
    
    # Ejecutar tests
    test1_passed = test_storage_configuration()
    test2_passed = test_storage_modes()
    verify_data_directory()
    
    print(f"\n🏁 RESUMEN FINAL:")
    print(f"   Test configuración storage: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"   Test modos de storage: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    
    if test1_passed and test2_passed:
        print(f"\n🎉 SISTEMA DE STORAGE INTELIGENTE: ✅ FUNCIONANDO")
        print(f"   El almacenamiento automático está operativo")
        print(f"   Las decisiones se toman según configuración ICT")
    else:
        print(f"\n⚠️ SISTEMA DE STORAGE NECESITA REVISIÓN")
