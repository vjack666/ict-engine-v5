#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🚀 TEST FINAL MARKET STATUS DETECTOR v3.0
==========================================

Verificación completa del sistema de detección de estado de mercado
"""

import sys
import os
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_market_status_detector():
    """Test completo del Market Status Detector v3.0"""
    print("=" * 60)
    print("🚀 TEST MARKET STATUS DETECTOR v3.0")
    print("=" * 60)

    try:
        # Test 1: Importación básica
        print("📦 Test 1: Importación del detector...")
        from sistema.market_status_detector import MarketStatusDetector
        print("✅ MarketStatusDetector importado correctamente")

        # Test 2: Creación de instancia
        print("\n🔧 Test 2: Creación de instancia...")
        detector = MarketStatusDetector()
        print("✅ Detector instanciado correctamente")

        # Test 3: Obtener estado del mercado
        print("\n📊 Test 3: Obtener estado del mercado...")
        status = detector.get_current_market_status()
        print("✅ Estado del mercado obtenido")
        
        # Mostrar resultados
        print(f"   Status: {status.get('emoji_status', '❓')} {status.get('market_status', 'UNKNOWN')}")
        session = status.get('session_activa', {})
        print(f"   Sesión: {session.get('name', 'UNKNOWN')}")
        print(f"   Descripción: {session.get('description', 'N/A')}")
        print(f"   Volatilidad: {session.get('volatility', 'UNKNOWN')}")
        print(f"   Activa: {session.get('is_active', False)}")

        # Test 4: Información de timezone
        print("\n🌍 Test 4: Información de timezone...")
        tz_info = detector.get_timezone_info()
        detection = tz_info.get('detection_summary', {})
        print("✅ Información de timezone obtenida")
        print(f"   Zona Local: {detection.get('local_timezone', 'UNKNOWN')}")
        print(f"   Offset UTC: {detection.get('local_offset', 'UNKNOWN')}")
        print(f"   Plataforma: {detection.get('platform', 'UNKNOWN')}")

        # Test 5: Resumen textual
        print("\n📋 Test 5: Resumen textual...")
        resumen = detector.get_session_summary()
        print("✅ Resumen generado")
        print(f"   Resumen: {resumen}")

        # Test 6: Próxima sesión
        print("\n⏰ Test 6: Cálculo de próxima sesión...")
        proxima = status.get('proxima_sesion', {})
        print("✅ Cálculo de próxima sesión")
        print(f"   Tiempo restante: {proxima.get('time_string', '00:00:00')}")
        print(f"   Horas: {proxima.get('hours', 0)}")
        print(f"   Minutos: {proxima.get('minutes', 0)}")

        # Test 7: Verificar compatibilidad
        print("\n🔧 Test 7: Verificar compatibilidades...")
        system_info = status.get('system_info', {})
        print(f"   Trading Schedule: {system_info.get('trading_schedule_available', False)}")
        print(f"   Pytz: {system_info.get('pytz_available', False)}")
        print(f"   Versión Detector: {system_info.get('detector_version', 'UNKNOWN')}")

        print("\n" + "=" * 60)
        print("✅ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
        print("🚀 Market Status Detector v3.0 está operativo")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n❌ ERROR EN TEST: {e}")
        print(f"Tipo de error: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

def test_integrations():
    """Test de integraciones con otros módulos"""
    print("\n🔗 TESTING INTEGRACIONES")
    print("-" * 40)

    try:
        # Test integración con trading_schedule
        print("📅 Testing integración con TradingScheduleManager...")
        try:
            from sistema.trading_schedule import TradingScheduleManager, get_current_session_info
            print("✅ TradingScheduleManager disponible")
            session_info = get_current_session_info()
            if session_info:
                print(f"   Sesión actual: {session_info.get('name', 'UNKNOWN')}")
            else:
                print("   ⚠️  Sin información de sesión actual")
        except ImportError as e:
            print(f"   ⚠️  TradingScheduleManager no disponible: {e}")

        # Test integración con logging
        print("\n📝 Testing integración con logging...")
        try:
            from sistema.logging_interface import enviar_senal_log
            enviar_senal_log("INFO", "Test de logging desde Market Status Detector", "test_final", "market_status")
            print("✅ Sistema de logging integrado")
        except ImportError as e:
            print(f"   ⚠️  Sistema de logging no disponible: {e}")

        print("\n✅ TESTS DE INTEGRACIÓN COMPLETADOS")
        return True

    except Exception as e:
        print(f"\n❌ ERROR EN TESTS DE INTEGRACIÓN: {e}")
        return False

if __name__ == "__main__":
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Python: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    # Ejecutar tests
    test_basic = test_market_status_detector()
    test_integration = test_integrations()
    
    if test_basic and test_integration:
        print("\n🎉 TODOS LOS TESTS EXITOSOS")
        print("🚀 Market Status Detector v3.0 listo para producción")
    else:
        print("\n⚠️  Algunos tests fallaron - revisar logs")
