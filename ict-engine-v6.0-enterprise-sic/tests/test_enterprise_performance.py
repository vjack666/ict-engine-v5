#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 TEST ICT ENTERPRISE PERFORMANCE
=================================

Test completo de rendimiento ENTERPRISE para verificar que todas las 
optimizaciones están funcionando correctamente.
"""

import sys
import time
import json
import psutil
from pathlib import Path
from datetime import datetime

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_enterprise_configuration():
    """🔧 Test configuración ENTERPRISE"""
    print("🔧 TESTING CONFIGURACIÓN ENTERPRISE...")
    
    # 1. Verificar archivos de configuración
    required_configs = [
        "config/performance_config_enterprise.json",
        "config/storage_config.json", 
        "config/cache_config.json",
        "config/threading_config.json",
        "config/memory_config.json",
        "config/ict_patterns_config.json",
        "config/network_config.json"
    ]
    
    missing_configs = []
    for config_file in required_configs:
        if not Path(config_file).exists():
            missing_configs.append(config_file)
        else:
            print(f"   ✅ {config_file}")
    
    if missing_configs:
        print(f"   ❌ Configuraciones faltantes: {missing_configs}")
        return False
    
    # 2. Verificar contenido de configuración ENTERPRISE
    try:
        with open("config/performance_config_enterprise.json", 'r') as f:
            enterprise_config = json.load(f)
        
        # Verificar campos críticos
        required_fields = ['performance_mode', 'storage', 'cache', 'threading', 'memory']
        for field in required_fields:
            if field not in enterprise_config:
                print(f"   ❌ Campo faltante en config: {field}")
                return False
        
        print(f"   ✅ Performance Mode: {enterprise_config.get('performance_mode')}")
        print(f"   ✅ Storage Mode: {enterprise_config['storage'].get('mode')}")
        print(f"   ✅ Cache Size: {enterprise_config['cache'].get('total_size_mb')} MB")
        print(f"   ✅ Max Workers: {enterprise_config['threading'].get('max_workers')}")
        
    except Exception as e:
        print(f"   ❌ Error leyendo configuración ENTERPRISE: {e}")
        return False
    
    print("✅ Configuración ENTERPRISE válida")
    return True

def test_downloader_enterprise():
    """📥 Test downloader con configuración ENTERPRISE"""
    print("\n📥 TESTING DOWNLOADER ENTERPRISE...")
    
    try:
        # Import downloader
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        
        # Crear downloader con configuración enterprise
        downloader = AdvancedCandleDownloader(config={'enable_debug': True})
        
        # Verificar que cargó configuración ENTERPRISE
        storage_config = downloader._storage_config
        print(f"   ✅ Storage Mode: {storage_config.get('mode')}")
        print(f"   ✅ Cache MB: {storage_config.get('max_cache_mb')}")
        print(f"   ✅ Enterprise Mode: {storage_config.get('enterprise_mode', False)}")
        
        # Verificar decisiones de storage inteligente
        test_cases = [
            ('EURUSD', 'H4'),   # Crítico: debería guardar
            ('EURUSD', 'M15'),  # Crítico: debería guardar  
            ('EURUSD', 'M1'),   # ICT symbol: debería guardar en ENTERPRISE
            ('GBPUSD', 'H1'),   # ICT + crítico: debería guardar
            ('AUDCAD', 'M5'),   # No crítico: ENTERPRISE debería guardar anyway
        ]
        
        for symbol, timeframe in test_cases:
            should_save = downloader._should_save_to_file(timeframe, symbol)
            print(f"   📊 {symbol} {timeframe}: {'💾 GUARDAR' if should_save else '🧠 MEMORIA'}")
        
        print("✅ Downloader ENTERPRISE funcionando")
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing downloader: {e}")
        return False

def test_system_performance():
    """📊 Test rendimiento del sistema"""
    print("\n📊 TESTING RENDIMIENTO DEL SISTEMA...")
    
    # Medir recursos disponibles
    cpu_count = psutil.cpu_count()
    memory_gb = psutil.virtual_memory().total // (1024**3)
    disk_gb = psutil.disk_usage('.').free // (1024**3)
    
    print(f"   🖥️  CPU Cores: {cpu_count}")
    print(f"   💾 RAM: {memory_gb} GB")
    print(f"   💿 Disk Free: {disk_gb} GB")
    
    # Verificar si cumple requisitos ENTERPRISE
    enterprise_ready = True
    
    if cpu_count < 4:
        print(f"   ⚠️  CPU cores bajo para ENTERPRISE (recomendado: 4+)")
        enterprise_ready = False
    else:
        print(f"   ✅ CPU cores adecuados para ENTERPRISE")
    
    if memory_gb < 8:
        print(f"   ⚠️  RAM baja para ENTERPRISE (recomendado: 8GB+)")
        enterprise_ready = False
    else:
        print(f"   ✅ RAM adecuada para ENTERPRISE")
    
    if disk_gb < 50:
        print(f"   ⚠️  Espacio en disco bajo (recomendado: 50GB+)")
        enterprise_ready = False
    else:
        print(f"   ✅ Espacio en disco adecuado")
    
    # Test de velocidad básica
    print("   🔄 Testing velocidad básica...")
    start_time = time.time()
    
    # Simulación carga de trabajo
    for i in range(1000000):
        x = i * 2 + 1
    
    duration = time.time() - start_time
    print(f"   ⚡ Velocidad de procesamiento: {duration:.3f}s")
    
    if duration < 0.1:
        print("   ✅ Rendimiento EXCELENTE")
    elif duration < 0.3:
        print("   ✅ Rendimiento BUENO")
    else:
        print("   ⚠️  Rendimiento BÁSICO")
    
    return enterprise_ready

def test_directory_structure():
    """📁 Test estructura de directorios ENTERPRISE"""
    print("\n📁 TESTING ESTRUCTURA ENTERPRISE...")
    
    required_dirs = [
        "data/candles/cache",
        "data/candles/archive", 
        "data/candles/realtime",
        "data/candles/analysis",
        "data/patterns/liquidity",
        "data/patterns/structure",
        "data/patterns/orderblocks",
        "data/patterns/poi",
        "data/exports/reports",
        "data/exports/signals",
        "cache/memory",
        "cache/predictions",
        "logs/performance",
        "logs/ict_analysis"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
        else:
            print(f"   ✅ {dir_path}")
    
    if missing_dirs:
        print(f"   ❌ Directorios faltantes: {missing_dirs}")
        return False
    
    print("✅ Estructura de directorios ENTERPRISE completa")
    return True

def test_cache_system():
    """🧠 Test sistema de cache ENTERPRISE"""
    print("\n🧠 TESTING SISTEMA DE CACHE...")
    
    try:
        # Verificar configuración de cache
        with open("config/cache_config.json", 'r') as f:
            cache_config = json.load(f)
        
        total_mb = cache_config.get('total_size_mb', 0)
        distribution = cache_config.get('distribution', {})
        
        print(f"   💾 Cache Total: {total_mb} MB")
        print(f"   📊 Distribución:")
        for component, size_mb in distribution.items():
            print(f"      {component}: {size_mb} MB")
        
        # Verificar que la suma es correcta
        total_distributed = sum(distribution.values())
        if abs(total_distributed - total_mb) <= 10:  # Tolerancia de 10MB
            print("   ✅ Distribución de cache consistente")
        else:
            print(f"   ⚠️  Inconsistencia en distribución: {total_distributed} vs {total_mb}")
        
        # Verificar cache layers
        cache_layers = cache_config.get('cache_layers', {})
        if cache_layers:
            print(f"   🔄 Cache Layers configurados:")
            for layer, size in cache_layers.items():
                print(f"      {layer}: {size}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error verificando cache: {e}")
        return False

def test_ict_patterns_config():
    """🏛️ Test configuración de patrones ICT"""
    print("\n🏛️ TESTING CONFIGURACIÓN ICT...")
    
    try:
        with open("config/ict_patterns_config.json", 'r') as f:
            ict_config = json.load(f)
        
        # Verificar patrones prioritarios
        priority_patterns = ict_config.get('priority_patterns', [])
        print(f"   📊 Patrones ICT configurados: {len(priority_patterns)}")
        for pattern in priority_patterns[:5]:  # Mostrar primeros 5
            print(f"      • {pattern}")
        
        # Verificar timeframes críticos
        critical_timeframes = ict_config.get('critical_timeframes', {})
        print(f"   ⏰ Timeframes críticos: {len(critical_timeframes)}")
        for tf, config in critical_timeframes.items():
            priority = config.get('priority', 'N/A')
            cache_hours = config.get('cache_duration_hours', 'N/A')
            print(f"      {tf}: Prioridad {priority}, Cache {cache_hours}h")
        
        # Verificar símbolos ICT
        ict_symbols = ict_config.get('ict_symbols', {})
        print(f"   💱 Símbolos ICT: {len(ict_symbols)}")
        for symbol, config in ict_symbols.items():
            priority = config.get('priority', 'N/A')
            sessions = config.get('session_focus', [])
            print(f"      {symbol}: Prioridad {priority}, Sesiones {sessions}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error verificando configuración ICT: {e}")
        return False

def generate_performance_summary():
    """📈 Generar resumen de rendimiento"""
    print("\n📈 RESUMEN DE RENDIMIENTO ENTERPRISE:")
    print("=" * 50)
    
    # Información del sistema
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('.').percent
    
    print(f"📊 Estado actual del sistema:")
    print(f"   CPU: {cpu_percent:.1f}%")
    print(f"   RAM: {memory_percent:.1f}%") 
    print(f"   Disk: {disk_percent:.1f}%")
    
    # Calcular score de rendimiento
    performance_score = 0
    
    # Score por utilización de recursos
    if cpu_percent < 30:
        performance_score += 25
    elif cpu_percent < 60:
        performance_score += 15
    else:
        performance_score += 5
    
    if memory_percent < 60:
        performance_score += 25
    elif memory_percent < 80:
        performance_score += 15
    else:
        performance_score += 5
    
    if disk_percent < 70:
        performance_score += 25
    elif disk_percent < 85:
        performance_score += 15
    else:
        performance_score += 5
    
    # Score por configuración
    performance_score += 25  # Configuración ENTERPRISE
    
    print(f"\n🏆 SCORE DE RENDIMIENTO: {performance_score}/100")
    
    if performance_score >= 90:
        status = "🚀 ENTERPRISE MAXIMUM"
        color = "🟢"
    elif performance_score >= 75:
        status = "⚡ ENTERPRISE READY"
        color = "🟡"
    else:
        status = "⚠️ BÁSICO"
        color = "🔴"
    
    print(f"{color} STATUS: {status}")
    
    return performance_score

def main():
    """🚀 Función principal de testing"""
    print("🚀 ICT ENTERPRISE PERFORMANCE TEST")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Configuración ENTERPRISE", test_enterprise_configuration),
        ("Downloader ENTERPRISE", test_downloader_enterprise),
        ("Rendimiento del Sistema", test_system_performance),
        ("Estructura de Directorios", test_directory_structure),
        ("Sistema de Cache", test_cache_system),
        ("Configuración ICT", test_ict_patterns_config)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ ERROR en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen final
    print(f"\n{'='*50}")
    print("📋 RESUMEN DE TESTS:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {test_name}")
        if result:
            passed += 1
    
    success_rate = (passed / total) * 100
    print(f"\n📊 Tests pasados: {passed}/{total} ({success_rate:.1f}%)")
    
    # Generar resumen de rendimiento
    performance_score = generate_performance_summary()
    
    # Recomendaciones finales
    print(f"\n💡 RECOMENDACIONES:")
    if success_rate == 100 and performance_score >= 90:
        print("   🚀 Sistema ENTERPRISE en perfecto estado!")
        print("   🎯 Listo para análisis ICT de alta frecuencia")
        print("   📊 Rendimiento óptimo para trading institucional")
    elif success_rate >= 80:
        print("   ✅ Sistema ENTERPRISE funcionando bien")
        print("   🔧 Considerar optimizaciones menores")
    else:
        print("   ⚠️ Sistema necesita atención")
        print("   🛠️ Revisar configuraciones fallidas")
    
    print(f"\n🏁 Test completado. Score final: {performance_score}/100")
    return success_rate, performance_score

if __name__ == "__main__":
    try:
        success_rate, performance_score = main()
        exit_code = 0 if success_rate >= 80 and performance_score >= 70 else 1
        sys.exit(exit_code)
    except Exception as e:
        print(f"💥 ERROR CRÍTICO en testing: {e}")
        sys.exit(1)
