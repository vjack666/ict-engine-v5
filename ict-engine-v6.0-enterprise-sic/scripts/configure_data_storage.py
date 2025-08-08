#!/usr/bin/env python3
"""
🗄️ ICT DATA STORAGE CONFIGURATOR - Configuración inteligente de almacenamiento
============================================================================

Configurador inteligente para optimizar el almacenamiento de datos ICT
según las necesidades del trader y disponibilidad de espacio.

Modos de operación:
- MEMORY_ONLY: Solo memoria (trading en vivo)
- CACHE_SMART: Cache inteligente (híbrido)
- FULL_STORAGE: Almacenamiento completo (análisis profundo)
- BACKUP_MODE: Solo respaldos críticos

Autor: ICT Engine v6.1.0 Enterprise Team
Fecha: Agosto 2025
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json

def analyze_storage_needs():
    """📊 Analizar necesidades de almacenamiento ICT"""
    print("\n" + "="*70)
    print("🗄️ ICT DATA STORAGE CONFIGURATOR v6.0")
    print("="*70)
    
    # Analizar espacio disponible
    root_path = Path(__file__).parent
    try:
        import shutil
        total, used, free = shutil.disk_usage(root_path)
        free_gb = free // (1024**3)
        print(f"\n💾 ESPACIO DISPONIBLE: {free_gb} GB")
    except:
        free_gb = "unknown"
        print(f"\n💾 ESPACIO DISPONIBLE: No se pudo determinar")
    
    # Estimar uso de datos ICT
    symbols = ['EURUSD', 'GBPUSD', 'XAUUSD', 'USDJPY']
    timeframes = ['D1', 'H4', 'H1', 'M15', 'M5']
    
    # Estimación conservadora: 1KB por vela
    total_velas_estimate = {
        'D1': 1000 * len(symbols),      # 1000 velas x símbolo
        'H4': 2500 * len(symbols),      # 2500 velas x símbolo  
        'H1': 5000 * len(symbols),      # 5000 velas x símbolo
        'M15': 10000 * len(symbols),    # 10000 velas x símbolo
        'M5': 5000 * len(symbols),      # 5000 velas x símbolo
    }
    
    total_velas = sum(total_velas_estimate.values())
    estimated_mb = total_velas * 0.001  # ~1KB por vela
    
    print(f"\n📊 ESTIMACIÓN ICT DATA:")
    print(f"   Símbolos principales: {len(symbols)}")
    print(f"   Timeframes ICT: {len(timeframes)}")
    print(f"   Velas totales estimadas: {total_velas:,}")
    print(f"   Espacio estimado: {estimated_mb:.1f} MB (~{estimated_mb/1024:.2f} GB)")
    
    # Recomendaciones según espacio
    if isinstance(free_gb, int):
        if free_gb > 10:
            recommendation = "FULL_STORAGE"
        elif free_gb > 5:
            recommendation = "CACHE_SMART"
        else:
            recommendation = "MEMORY_ONLY"
    else:
        recommendation = "CACHE_SMART"
    
    print(f"\n🎯 RECOMENDACIÓN: {recommendation}")
    
    return {
        'free_space_gb': free_gb,
        'estimated_usage_mb': estimated_mb,
        'recommendation': recommendation,
        'symbols': symbols,
        'timeframes': timeframes
    }

def configure_storage_mode(mode: str = "AUTO") -> dict:
    """🔧 Configurar modo de almacenamiento ICT"""
    
    storage_configs = {
        "MEMORY_ONLY": {
            "description": "Solo memoria RAM - Ideal para trading en vivo",
            "save_to_file": False,
            "cache_enabled": True,
            "max_cache_mb": 500,
            "backup_critical": False,
            "advantages": [
                "Velocidad máxima",
                "Sin uso de disco",
                "Ideal para VPS pequeños"
            ],
            "disadvantages": [
                "Datos se pierden al cerrar",
                "Sin backup automático",
                "Limitado para backtesting"
            ]
        },
        
        "CACHE_SMART": {
            "description": "Cache inteligente - Balance perfecto",
            "save_to_file": "smart",  # Solo timeframes críticos
            "cache_enabled": True,
            "max_cache_mb": 1000,
            "backup_critical": True,
            "critical_timeframes": ["H4", "H1", "M15"],
            "advantages": [
                "Balance óptimo velocidad/storage",
                "Backup de timeframes críticos",
                "Cache predictivo ICT"
            ],
            "disadvantages": [
                "Configuración más compleja",
                "Uso moderado de disco"
            ]
        },
        
        "FULL_STORAGE": {
            "description": "Almacenamiento completo - Análisis profundo",
            "save_to_file": True,
            "cache_enabled": True,
            "max_cache_mb": 2000,
            "backup_critical": True,
            "organize_by_date": True,
            "advantages": [
                "Backup completo",
                "Análisis histórico completo",
                "Auditoría total de trades"
            ],
            "disadvantages": [
                "Mayor uso de disco",
                "Gestión de archivos"
            ]
        },
        
        "BACKUP_MODE": {
            "description": "Solo respaldos críticos - Seguridad",
            "save_to_file": "critical_only",
            "cache_enabled": True,
            "max_cache_mb": 750,
            "backup_critical": True,
            "backup_trades_only": True,
            "advantages": [
                "Backup mínimo esencial",
                "Seguridad de trades",
                "Poco uso de disco"
            ],
            "disadvantages": [
                "Datos limitados para análisis",
                "Sin historial completo"
            ]
        }
    }
    
    if mode == "AUTO":
        analysis = analyze_storage_needs()
        mode = analysis['recommendation']
    
    if mode not in storage_configs:
        mode = "CACHE_SMART"  # Default seguro
    
    config = storage_configs[mode]
    config['mode'] = mode
    config['timestamp'] = datetime.now().isoformat()
    
    print(f"\n⚙️ CONFIGURACIÓN SELECCIONADA: {mode}")
    print(f"   {config['description']}")
    print(f"\n✅ VENTAJAS:")
    for advantage in config['advantages']:
        print(f"   - {advantage}")
    print(f"\n⚠️ CONSIDERACIONES:")
    for disadvantage in config['disadvantages']:
        print(f"   - {disadvantage}")
    
    return config

def apply_storage_configuration(config: dict):
    """🚀 Aplicar configuración de almacenamiento al downloader"""
    
    print(f"\n🔧 Aplicando configuración {config['mode']}...")
    
    # Crear configuración para el downloader
    downloader_config = {
        'storage_mode': config['mode'],
        'save_to_file_default': config.get('save_to_file', False),
        'cache_enabled': config.get('cache_enabled', True),
        'max_cache_mb': config.get('max_cache_mb', 500),
        'backup_critical': config.get('backup_critical', False)
    }
    
    # Configuraciones especiales por modo
    if config['mode'] == "CACHE_SMART":
        downloader_config['critical_timeframes'] = config.get('critical_timeframes', ['H4', 'H1', 'M15'])
        downloader_config['save_strategy'] = 'smart'
    elif config['mode'] == "FULL_STORAGE":
        downloader_config['organize_by_date'] = True
        downloader_config['save_strategy'] = 'all'
    elif config['mode'] == "BACKUP_MODE":
        downloader_config['save_strategy'] = 'critical_only'
    
    # Guardar configuración
    config_file = Path("config/storage_config.json")
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump({
            'storage_config': config,
            'downloader_config': downloader_config
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Configuración guardada en: {config_file}")
    
    # Crear directorio de datos si es necesario
    if config.get('save_to_file', False):
        data_dir = Path("data/candles")
        data_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Directorio de datos creado: {data_dir}")
    
    return downloader_config

def get_storage_recommendations():
    """💡 Obtener recomendaciones específicas por caso de uso"""
    
    recommendations = {
        "🏛️ TRADING INSTITUCIONAL": {
            "mode": "FULL_STORAGE",
            "reason": "Necesitas auditoría completa y análisis histórico profundo"
        },
        
        "⚡ SCALPING RÁPIDO": {
            "mode": "MEMORY_ONLY", 
            "reason": "Velocidad máxima, datos en tiempo real únicamente"
        },
        
        "📊 SWING TRADING": {
            "mode": "CACHE_SMART",
            "reason": "Balance perfecto para análisis multi-timeframe"
        },
        
        "🔬 BACKTESTING": {
            "mode": "FULL_STORAGE",
            "reason": "Necesitas años de datos históricos precisos"
        },
        
        "🌐 VPS LIMITADO": {
            "mode": "MEMORY_ONLY",
            "reason": "Recursos limitados, priorizar velocidad"
        },
        
        "🎯 LEARNING ICT": {
            "mode": "CACHE_SMART",
            "reason": "Datos suficientes para aprender sin ocupar mucho espacio"
        }
    }
    
    print(f"\n💡 RECOMENDACIONES POR CASO DE USO:")
    print(f"="*50)
    
    for use_case, rec in recommendations.items():
        print(f"\n{use_case}")
        print(f"   Modo recomendado: {rec['mode']}")
        print(f"   Razón: {rec['reason']}")
    
    return recommendations

if __name__ == "__main__":
    print("🗄️ ICT ENGINE v6.0 - DATA STORAGE CONFIGURATOR")
    print("=" * 70)
    
    # Analizar necesidades
    analysis = analyze_storage_needs()
    
    # Mostrar recomendaciones
    get_storage_recommendations()
    
    # Configurar automáticamente
    print(f"\n🚀 AUTO-CONFIGURACIÓN:")
    config = configure_storage_mode("AUTO")
    
    # Aplicar configuración
    downloader_config = apply_storage_configuration(config)
    
    print(f"\n✅ CONFIGURACIÓN COMPLETADA")
    print(f"   Modo: {config['mode']}")
    print(f"   Guardar archivos: {downloader_config.get('save_to_file_default', False)}")
    print(f"   Cache habilitado: {downloader_config.get('cache_enabled', True)}")
    print(f"   Límite cache: {downloader_config.get('max_cache_mb', 500)} MB")
    
    print(f"\n🎯 PRÓXIMOS PASOS:")
    print(f"   1. El downloader usará automáticamente esta configuración")
    print(f"   2. Puedes cambiar el modo editando config/storage_config.json")
    print(f"   3. Para trading en vivo, considera MEMORY_ONLY o CACHE_SMART")
    print(f"   4. Para análisis histórico, usa FULL_STORAGE")
