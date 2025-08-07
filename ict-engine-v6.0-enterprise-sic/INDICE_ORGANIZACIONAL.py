#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📁 ICT ENGINE v6.0 ENTERPRISE - ÍNDICE ORGANIZACIONAL
=====================================================

Índice completo de la estructura organizacional del proyecto.
Todos los archivos están organizados por funcionalidad.

📂 ESTRUCTURA ACTUAL:
├── core/                          # 🏛️ Núcleo del sistema
│   ├── data_management/          # 📥 Gestión de datos
│   ├── analysis/                 # 🔍 Análisis ICT
│   ├── ict_engine/              # 🚀 Motor ICT
│   └── ...
├── scripts/                       # 🚀 Scripts ejecutables
│   ├── ict_performance_optimizer.py    # Optimizador ENTERPRISE
│   ├── ict_performance_monitor.py      # Monitor en tiempo real  
│   ├── configure_data_storage.py       # Configurador de storage
│   ├── setup_ict_historical_data.py    # Setup datos históricos
│   └── launch_ict_enterprise.py        # Launcher principal
├── tests/                         # 🧪 Sistema de pruebas
│   ├── test_enterprise_performance.py  # Test rendimiento
│   ├── test_critical_timeframes.py     # Test timeframes
│   ├── test_storage_inteligente.py     # Test storage
│   ├── test_fundednext_system.py       # Test FundedNext
│   ├── test_ict_optimal_downloader.py  # Test downloader
│   ├── test_real_system.py             # Test sistema real
│   ├── test_simple_poi.py              # Test POI simple
│   └── test_sic_complete.py            # Test SIC completo
├── utils/                         # 🔧 Utilidades
│   ├── ict_optimal_config.py           # Configuración ICT óptima
│   ├── debug_performance_report.py     # Debug de rendimiento
│   ├── final_ict_verification.py       # Verificación final
│   └── verificar_sistema.py            # Verificador sistema
├── config/                        # ⚙️ Configuraciones
│   ├── performance_config_enterprise.json  # Config ENTERPRISE
│   ├── storage_config.json                 # Config storage
│   ├── cache_config.json                   # Config cache
│   ├── threading_config.json               # Config threading
│   ├── memory_config.json                  # Config memoria
│   ├── ict_patterns_config.json            # Config patrones ICT
│   ├── network_config.json                 # Config red
│   └── sic_cache_stats.json               # Stats SIC cache
├── data/                          # 💾 Datos del sistema
│   ├── candles/                   # Datos de velas
│   ├── patterns/                  # Patrones detectados
│   ├── exports/                   # Exportaciones
│   └── ...
├── logs/                          # 📊 Logs y métricas
├── cache/                         # 🧠 Cache del sistema
├── sistema/                       # 🏗️ SIC v3.1 Enterprise
└── docs/                          # 📚 Documentación

🎯 SCRIPTS PRINCIPALES PARA USAR:

🚀 RENDIMIENTO MÁXIMO:
   python scripts/ict_performance_optimizer.py     # Configurar rendimiento ENTERPRISE
   python scripts/ict_performance_monitor.py       # Monitor en tiempo real
   python scripts/launch_ict_enterprise.py         # Launcher completo

🔧 CONFIGURACIÓN:
   python scripts/configure_data_storage.py        # Configurar storage
   python scripts/setup_ict_historical_data.py     # Descargar datos históricos

🧪 TESTING:
   python tests/test_enterprise_performance.py     # Test rendimiento completo
   python tests/test_critical_timeframes.py        # Test timeframes ICT
   python tests/test_fundednext_system.py          # Test sistema FundedNext

🔍 VERIFICACIÓN:
   python utils/verificar_sistema.py               # Verificar sistema completo
   python utils/final_ict_verification.py          # Verificación final ICT

📊 CONFIGURACIÓN ACTUAL:
- Modo: ENTERPRISE_MAXIMUM
- Storage: FULL_STORAGE_ENTERPRISE  
- Cache: 2GB optimizado
- Threads: 15 workers
- Rendimiento: 91.7/100
- Conexión: FundedNext MT5 Real

🎯 LISTO PARA TRADING INSTITUCIONAL ICT
"""

def mostrar_estructura():
    """📁 Muestra la estructura organizacional"""
    from pathlib import Path
    
    print("📁 ICT ENGINE v6.0 ENTERPRISE - ESTRUCTURA ORGANIZACIONAL")
    print("=" * 60)
    
    # Directorios principales
    directorios = {
        'scripts': '🚀 Scripts ejecutables',
        'tests': '🧪 Sistema de pruebas', 
        'utils': '🔧 Utilidades',
        'config': '⚙️ Configuraciones',
        'core': '🏛️ Núcleo del sistema',
        'data': '💾 Datos del sistema',
        'logs': '📊 Logs y métricas',
        'cache': '🧠 Cache del sistema',
        'sistema': '🏗️ SIC v3.1 Enterprise',
        'docs': '📚 Documentación'
    }
    
    for directorio, descripcion in directorios.items():
        path = Path(directorio)
        if path.exists():
            archivos = list(path.glob('*.py'))
            print(f"📂 {directorio}/ - {descripcion}")
            print(f"   📄 {len(archivos)} archivos Python")
            if len(archivos) <= 5:
                for archivo in archivos:
                    print(f"      • {archivo.name}")
            else:
                print(f"      • {archivos[0].name}")
                print(f"      • {archivos[1].name}")
                print(f"      • ... y {len(archivos)-2} más")
            print()
        else:
            print(f"❌ {directorio}/ - {descripcion} (NO ENCONTRADO)")
    
    print("✅ ESTRUCTURA ORGANIZADA Y LISTA PARA USO")

def mostrar_comandos_rapidos():
    """⚡ Muestra comandos rápidos"""
    print("\n⚡ COMANDOS RÁPIDOS:")
    print("-" * 40)
    print("🚀 Optimizar rendimiento:     python scripts/ict_performance_optimizer.py")
    print("📊 Monitor tiempo real:       python scripts/ict_performance_monitor.py") 
    print("🎯 Launcher completo:         python scripts/launch_ict_enterprise.py")
    print("🧪 Test rendimiento:          python tests/test_enterprise_performance.py")
    print("🔧 Verificar sistema:         python utils/verificar_sistema.py")

if __name__ == "__main__":
    mostrar_estructura()
    mostrar_comandos_rapidos()
