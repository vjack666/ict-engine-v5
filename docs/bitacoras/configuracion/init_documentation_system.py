#!/usr/bin/env python3
"""
🚀 INICIALIZADOR DEL SISTEMA DE DOCUMENTACIÓN ICT ENGINE
======================================================

Script de inicialización que configura y activa todos los sistemas
de documentación, bitácoras y monitoreo del ICT Engine v3.44.

Ejecuta este script para:
- Inicializar el sistema de bitácoras
- Activar el monitoreo del sistema
- Crear estructuras de directorios necesarias
- Configurar logging especializado
- Generar reportes iniciales

Uso:
    python init_documentation_system.py

Autor: ICT Engine Team
Fecha: Agosto 2025
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Agregar el directorio raíz al path para imports
current_dir = Path(__file__).parent
root_dir = current_dir.parent
sys.path.insert(0, str(root_dir))

try:
    from docs.bitacoras.bitacora_manager import (
        bitacora_manager,
        log_system_startup,
        BitacoraType,
        SeverityLevel
    )
    from sistema.system_monitor import (
        system_monitor,
        start_system_monitoring,
        get_system_status,
        get_health_report
    )
    from sistema.logging_interface import enviar_senal_log

    DEPENDENCIES_OK = True
except ImportError as e:
    print(f"❌ Error importando dependencias: {e}")
#     DEPENDENCIES_OK = False  # Constant redefinition


def crear_estructura_directorios():
    """Crea la estructura completa de directorios de documentación"""
    print("📁 Creando estructura de directorios...")

    directorios = [
        "docs",
        "docs/logs",
        "docs/bitacoras",
        "docs/bitacoras/system_status",
        "docs/bitacoras/trading_decisions",
        "docs/bitacoras/pattern_detection",
        "docs/bitacoras/performance",
        "docs/bitacoras/error_tracking",
        "docs/bitacoras/session_analysis",
        "docs/bitacoras/poi_lifecycle",
        "docs/bitacoras/risk_management",
        "docs/architecture",
        "docs/reports",
        "docs/reports/daily",
        "docs/reports/weekly",
        "docs/reports/monthly",
        "data",
        "data/logs",
        "data/logs/terminal_capture",
        "data/candles"
    ]

    for directorio in directorios:
        dir_path = root_dir / directorio
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directorio}")

    print("📁 Estructura de directorios creada correctamente")


def inicializar_bitacoras():
    """Inicializa el sistema de bitácoras"""
    print("📋 Inicializando sistema de bitácoras...")

    if not DEPENDENCIES_OK:
        print("❌ No se pueden inicializar las bitácoras - dependencias faltantes")
        return False

    try:
        # Registrar inicio del sistema
        log_system_startup()

        # Registrar inicialización de cada tipo de bitácora
        for bitacora_type in BitacoraType:
            bitacora_manager.log_system_event(
                SeverityLevel.INFO,
                f"BITACORA_{bitacora_type.value.upper()}_INIT",
                f"Bitácora {bitacora_type.value} inicializada",
                {"type": bitacora_type.value, "status": "READY"}
            )

        print("📋 Sistema de bitácoras inicializado correctamente")
        return True

    except Exception as e:
        print(f"❌ Error inicializando bitácoras: {e}")
        return False


def inicializar_monitor_sistema():
    """Inicializa el monitor del sistema"""
    print("📊 Inicializando monitor del sistema...")

    if not DEPENDENCIES_OK:
        print("❌ No se puede inicializar el monitor - dependencias faltantes")
        return False

    try:
        # Iniciar monitoreo
        start_system_monitoring()

        # Esperar un momento para recopilar datos iniciales
        import time
        time.sleep(3)

        # Obtener estado inicial
        status = get_system_status()
        print(f"📊 Estado del sistema: {status['overall_status']}")
        print(f"📊 Componentes monitoreados: {len(status['components'])}")
        print(f"📊 Alertas activas: {status['alerts']['active']}")

        print("📊 Monitor del sistema inicializado correctamente")
        return True

    except Exception as e:
        print(f"❌ Error inicializando monitor: {e}")
        return False


def generar_reporte_inicial():
    """Genera reporte inicial del sistema"""
    print("📄 Generando reporte inicial...")

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Reporte de salud del sistema
        if DEPENDENCIES_OK and system_monitor:
            health_report = get_health_report()

            report_file = root_dir / "docs" / "reports" / f"system_health_init_{timestamp}.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(health_report)

            print(f"📄 Reporte de salud guardado: {report_file.name}")

        # Reporte de configuración inicial
        config_report = f"""
📋 REPORTE DE INICIALIZACIÓN ICT ENGINE v3.44
============================================

🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🏗️ Versión: ICT Engine v3.44
🎯 Estado: Sistema inicializado correctamente

📁 ESTRUCTURA DE DIRECTORIOS:
✅ docs/ - Documentación principal
✅ docs/logs/ - Logs del sistema
✅ docs/bitacoras/ - Bitácoras especializadas
✅ docs/architecture/ - Documentación de arquitectura
✅ docs/reports/ - Reportes del sistema
✅ data/ - Datos del sistema

📋 SISTEMAS INICIALIZADOS:
✅ Sistema de Bitácoras (SLUC v2.0)
✅ Monitor de Sistema
✅ Logging Centralizado
✅ Estructura de Directorios

🎯 COMPONENTES DISPONIBLES:
• Pattern Analyzer - Análisis de patrones ICT
• POI Detector - Detección de puntos de interés
• Risk Manager - Gestión de riesgo
• Dashboard - Interfaz de usuario
• System Monitor - Monitoreo en tiempo real

📊 TIPOS DE BITÁCORAS ACTIVAS:
• system_status - Estado general del sistema
• trading_decisions - Decisiones de trading
• pattern_detection - Detección de patrones
• performance - Métricas de rendimiento
• error_tracking - Seguimiento de errores
• session_analysis - Análisis por sesión
• poi_lifecycle - Ciclo de vida de POIs
• risk_management - Gestión de riesgo

🔄 PRÓXIMOS PASOS:
1. Iniciar el dashboard principal
2. Configurar conexión con MT5
3. Comenzar análisis en tiempo real
4. Revisar logs en docs/logs/
5. Consultar bitácoras en docs/bitacoras/

📞 SOPORTE:
- Logs del sistema: docs/logs/system_monitoring_*.json
- Bitácoras: docs/bitacoras/*/
- Reportes: docs/reports/
- Documentación: docs/README.md

🚀 ¡Sistema ICT Engine v3.44 listo para operar!
        """.strip()

        config_file = root_dir / "docs" / "reports" / f"init_report_{timestamp}.txt"
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_report)

        print(f"📄 Reporte de inicialización guardado: {config_file.name}")

        # Mostrar resumen en consola
        print("\n" + "="*60)
        print("🚀 SISTEMA ICT ENGINE v3.44 INICIALIZADO CORRECTAMENTE")
        print("="*60)
        print(f"📋 Bitácoras: {'✅ ACTIVAS' if DEPENDENCIES_OK else '❌ ERROR'}")
        print(f"📊 Monitor: {'✅ ACTIVO' if DEPENDENCIES_OK else '❌ ERROR'}")
        print(f"📁 Directorios: ✅ CREADOS")
        print(f"📄 Reportes: ✅ GENERADOS")
        print("="*60)

        if DEPENDENCIES_OK:
            print("🎯 El sistema está listo para comenzar el análisis de trading ICT")
            print("📋 Consulta las bitácoras en: docs/bitacoras/")
            print("📊 Revisa el estado del sistema en: docs/logs/")
        else:
            print("⚠️  Algunas funciones avanzadas no están disponibles")
            print("🔧 Verifica las dependencias e imports del sistema")

        print("="*60)
        return True

    except Exception as e:
        print(f"❌ Error generando reporte inicial: {e}")
        return False


def main():
    """Función principal de inicialización"""
    print("\n🚀 INICIALIZANDO SISTEMA DE DOCUMENTACIÓN ICT ENGINE v3.44")
    print("="*65)

    success_count = 0
    total_steps = 4

    # Paso 1: Crear estructura de directorios
    crear_estructura_directorios()
    success_count += 1

    # Paso 2: Inicializar bitácoras
    if inicializar_bitacoras():
        success_count += 1

    # Paso 3: Inicializar monitor
    if inicializar_monitor_sistema():
        success_count += 1

    # Paso 4: Generar reporte inicial
    if generar_reporte_inicial():
        success_count += 1

    # Resumen final
    print(f"\n✅ Inicialización completada: {success_count}/{total_steps} pasos exitosos")

    if success_count == total_steps:
        print("🎉 ¡Sistema de documentación totalmente operativo!")
        return 0
    else:
        print("⚠️  Sistema parcialmente inicializado - revisar errores arriba")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️  Inicialización cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error crítico durante la inicialización: {e}")
        sys.exit(1)
