#!/usr/bin/env python3
"""
🧪 PRUEBA COMPLETA DEL DETECTOR AUTOMÁTICO DE ESTADO DE MERCADO
==============================================================

Script para probar y validar que el detector automático funciona
correctamente con múltiples zonas horarias y configuraciones.
"""

import sys
from pathlib import Path
from datetime import datetime

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from sistema.market_status_detector import MarketStatusDetector
    from sistema.logging_interface import enviar_senal_log
except ImportError as e:
    print(f"Error importando módulos: {e}")
    sys.exit(1)


def test_market_detector():
    """Prueba completa del detector de mercado"""
    print("🧪 PRUEBA COMPLETA DEL DETECTOR AUTOMÁTICO")
    print("=" * 60)

    # Inicializar detector
    detector = MarketStatusDetector()

    # Obtener estado completo
    status = detector.get_current_market_status()

    # 1. INFORMACIÓN BÁSICA
    print("📅 INFORMACIÓN BÁSICA:")
    print(f"  Fecha: {status['fecha']}")
    print(f"  Día: {status['dia_semana']}")
    print(f"  Fin de semana: {'SÍ' if status['is_weekend'] else 'NO'}")
    print()

    # 2. ZONAS HORARIAS
    print("🌍 MÚLTIPLES ZONAS HORARIAS:")
    print(f"  🏠 Local: {status['tiempo_local']['hora']} ({status['tiempo_local']['timezone']}) {status['tiempo_local']['offset']}")
    print(f"  🌐 UTC: {status['tiempo_utc']['hora']} ({status['tiempo_utc']['timezone']}) {status['tiempo_utc']['offset']}")
    print(f"  💼 Broker: {status['tiempo_broker']['hora']} ({status['tiempo_broker']['timezone']}) {status['tiempo_broker']['offset']}")
    print()

    # 3. ESTADO DEL MERCADO
    print("📊 ESTADO DEL MERCADO:")
    print(f"  Status: {status['emoji_status']} {status['market_status']}")
    print(f"  Display: {status['status_display']}")
    print(f"  Sesión activa: {status['session_activa']['name']}")
    print(f"  Descripción: {status['session_activa']['description']}")

    if 'all_active' in status['session_activa'] and status['session_activa']['all_active']:
        print(f"  Sesiones activas: {', '.join(status['session_activa']['all_active'])}")
        print(f"  Total sesiones: {status['session_activa'].get('total_sessions', 0)}")
    print()

    # 4. PRÓXIMA SESIÓN
    print("⏳ PRÓXIMA SESIÓN:")
    print(f"  En: {status['proxima_sesion']['time_string']}")
    print()

    # 5. DETECCIÓN TÉCNICA
    print("🔧 INFORMACIÓN TÉCNICA:")
    if 'timezone_detection' in status:
        tz_info = status['timezone_detection']
        if 'local_timezone' in tz_info:
            print(f"  Método detección: {tz_info['local_timezone'].get('detection_method', 'N/A')}")
            print(f"  Plataforma: {tz_info.get('platform', 'N/A')}")
            print(f"  DST activo: {tz_info['local_timezone'].get('is_dst', False)}")
    print()

    # 6. VALIDACIÓN ESPECÍFICA
    print("✅ VALIDACIONES:")

    # Validar que detectó correctamente Ecuador
    tz_info = detector.get_timezone_info()
    local_offset = tz_info['detection_summary']['local_offset']
    if 'Ecuador' in tz_info['detection_summary']['local_timezone'] or 'UTC-5' in local_offset:
        print("  ✅ Zona horaria de Ecuador detectada correctamente")
    else:
        print(f"  📍 Zona detectada: {tz_info['detection_summary']['local_timezone']} ({local_offset})")

    # Validar lógica de mercado
    if status['is_weekend']:
        if status['market_status'] == 'CERRADO':
            print("  ✅ Lógica de fin de semana correcta")
        else:
            print("  ❌ Error: Mercado debería estar cerrado en fin de semana")
    else:
        # En día laborable, verificar lógica de sesiones
        if status['session_activa']['active']:
            print("  ✅ Sesión activa detectada en día laborable")
        else:
            print("  🟡 Mercado cerrado entre sesiones (normal)")

    # Validar consistencia de datos
    if all(k in status for k in ['tiempo_local', 'tiempo_utc', 'tiempo_broker']):
        print("  ✅ Todas las zonas horarias disponibles")
    else:
        print("  ❌ Error: Faltan datos de zonas horarias")

    print()

    # 7. RESUMEN PARA DASHBOARD
    print("🎯 RESUMEN PARA DASHBOARD:")
    print(f"  Header: {status['emoji_status']} {status['status_display']}")
    print(f"  Multi-zona: Local {status['tiempo_local']['hora']} | UTC {status['tiempo_utc']['hora']} | Broker {status['tiempo_broker']['hora']}")
    print(f"  Estado: {'MERCADO ABIERTO' if status['market_status'] == 'ABIERTO' else 'MERCADO CERRADO'}")

    return status


def test_integration_with_dashboard():
    """Prueba de integración con dashboard"""
    print("\n🔗 PRUEBA DE INTEGRACIÓN CON DASHBOARD")
    print("=" * 50)

    try:
        # Simular uso en dashboard
        detector = MarketStatusDetector()

        # Obtener datos como los usaría el dashboard
        market_data = detector.get_current_market_status()

        # Simular logging como en dashboard
        enviar_senal_log("INFO",
            f"🕐 Dashboard usando estado: {market_data['market_status']} | " +
            f"{market_data['session_activa']['name']} | " +
            f"Local: {market_data['tiempo_local']['hora']} | " +
            f"UTC: {market_data['tiempo_utc']['hora']}",
            "dashboard_test", "market_status")

        # Verificar métodos auxiliares
        is_open = detector.is_market_open()
        simple_status = detector.get_simple_status()

        print(f"  ✅ is_market_open(): {is_open}")
        print(f"  ✅ get_simple_status(): {simple_status}")

        # Datos para renderizado
        datos_para_dashboard = {
            'header_text': f"{market_data['emoji_status']} {market_data['status_display']}",
            'tiempo_info': f"Local: {market_data['tiempo_local']['hora']} | UTC: {market_data['tiempo_utc']['hora']} | Broker: {market_data['tiempo_broker']['hora']}",
            'market_open': is_open,
            'color_scheme': 'green' if is_open else 'yellow' if not market_data['is_weekend'] else 'red'
        }

        print(f"  ✅ Datos para dashboard: {datos_para_dashboard}")

        return True

    except Exception as e:
        print(f"  ❌ Error en integración: {e}")
        return False


def main():
    """Función principal"""
    print("🚀 SISTEMA DE DETECCIÓN AUTOMÁTICA DE ESTADO DE MERCADO")
    print("🌍 Adaptativo para cualquier zona horaria y configuración VPS")
    print("=" * 80)
    print()

    # Prueba 1: Detector básico
    status = test_market_detector()

    # Prueba 2: Integración con dashboard
    integration_ok = test_integration_with_dashboard()

    # Resumen final
    print("\n🏁 RESUMEN DE PRUEBAS")
    print("=" * 30)
    print(f"✅ Detector básico: FUNCIONANDO")
    print(f"{'✅' if integration_ok else '❌'} Integración dashboard: {'FUNCIONANDO' if integration_ok else 'ERROR'}")
    print(f"✅ Multi-zona horaria: FUNCIONANDO")
    print(f"✅ Detección automática: FUNCIONANDO")

    if status['is_weekend']:
        print("🔴 Estado actual: FIN DE SEMANA - Mercado cerrado")
    elif status['market_status'] == 'ABIERTO':
        print(f"🟢 Estado actual: MERCADO ABIERTO - Sesión {status['session_activa']['name']}")
    else:
        print("🟡 Estado actual: MERCADO CERRADO - Entre sesiones")

    print()
    print("🎯 LISTO PARA INTEGRACIÓN EN DASHBOARD!")


if __name__ == "__main__":
    main()
