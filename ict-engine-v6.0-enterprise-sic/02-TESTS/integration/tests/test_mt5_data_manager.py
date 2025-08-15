#!/usr/bin/env python3
"""
🧪 TESTS PARA MT5DATAMANAGER v6.0 ENTERPRISE
==========================================

Suite de tests completa para el componente FUNDAMENTAL #1
del ICT Engine v6.1.0 Enterprise SIC.

Tests incluidos:
- Inicialización y configuración
- Integración SIC v3.1
- Validaciones de seguridad FTMO Global Markets
- Lazy loading y cache predictivo
- Conexión y desconexión
- Operaciones de datos
- Performance y métricas
- Compatibilidad legacy

Autor: ICT Engine v6.1.0 Enterprise Team
Prioridad: CRÍTICA - COMPONENTE FUNDAMENTAL
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from pathlib import Path
import time

# Agregar el directorio raíz al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Importar el MT5DataManager
try:
    from utils.mt5_data_manager import (
        MT5DataManager, 
        get_mt5_manager,
        create_connection_info,
        descargar_y_guardar_m1,
        MT5ConnectionInfo,
        MT5TickData,
        MT5HistoricalData,
        AccountType,
        validate_ftmo_installation,
        ensure_only_ftmo_connection,
        FTMO_CONFIG,
        TIMEFRAME_MAPPING
    )
    MT5_MANAGER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Error importando MT5DataManager: {e}")
    MT5_MANAGER_AVAILABLE = False

class TestMT5DataManagerBasics(unittest.TestCase):
    """🔧 Tests básicos de inicialización y configuración"""

    def setUp(self):
        """Configurar entorno de test"""
        self.test_config = {
            'enable_debug': True,
            'use_predictive_cache': True,
            'enable_lazy_loading': True,
            'security_level': 'MAXIMUM'
        }

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    def test_initialization_default(self):
        """✅ Test inicialización con configuración por defecto"""
        manager = MT5DataManager()
        
        # Verificar estado inicial
        self.assertIsInstance(manager, MT5DataManager)
        self.assertFalse(manager.is_connected)
        self.assertEqual(manager.account_type, AccountType.UNKNOWN)
        self.assertIsNotNone(manager.connection_info)
        
        print("✅ Test inicialización por defecto: PASSED")

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    def test_initialization_with_config(self):
        """✅ Test inicialización con configuración personalizada"""
        manager = MT5DataManager(config=self.test_config)
        
        # Verificar configuración aplicada
        self.assertTrue(manager._enable_debug)
        self.assertTrue(manager._use_predictive_cache)
        self.assertTrue(manager._enable_lazy_loading)
        self.assertEqual(manager._security_level, 'MAXIMUM')
        
        print("✅ Test inicialización con config: PASSED")

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    def test_factory_function(self):
        """✅ Test función factory get_mt5_manager"""
        manager = get_mt5_manager(self.test_config)
        
        self.assertIsInstance(manager, MT5DataManager)
        self.assertTrue(manager._enable_debug)
        
        print("✅ Test función factory: PASSED")

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    def test_connection_info_creation(self):
        """✅ Test creación de MT5ConnectionInfo"""
        conn_info = create_connection_info()
        
        self.assertIsInstance(conn_info, MT5ConnectionInfo)
        self.assertFalse(conn_info.is_connected)
        self.assertEqual(conn_info.account_type, AccountType.UNKNOWN)
        self.assertTrue(conn_info.sic_integration)  # Debe estar habilitado por defecto
        
        print("✅ Test creación ConnectionInfo: PASSED")

class TestMT5DataManagerSecurity(unittest.TestCase):
    """🛡️ Tests de seguridad y validaciones FTMO Global Markets"""

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    def test_ftmo_config(self):
        """✅ Test configuración FTMO Global Markets"""
        self.assertIn("executable_path", FTMO_CONFIG)
        self.assertIn("ftmo", FTMO_CONFIG["executable_path"].lower())
        self.assertEqual(FTMO_CONFIG["security_level"], "MAXIMUM")
        self.assertEqual(FTMO_CONFIG["version"], "v6.0-enterprise")
        
        print("✅ Test configuración FTMO Global Markets: PASSED")

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    @patch('utils.mt5_data_manager.os.path.exists')
    @patch('utils.mt5_data_manager.os.path.isfile')
    def test_validate_ftmo_installation_success(self, mock_isfile, mock_exists):
        """✅ Test validación exitosa de instalación FTMO Global Markets"""
        mock_exists.return_value = True
        mock_isfile.return_value = True
        
        result = validate_ftmo_installation()
        self.assertTrue(result)
        
        print("✅ Test validación FTMO Global Markets exitosa: PASSED")

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    @patch('utils.mt5_data_manager.os.path.exists')
    def test_validate_ftmo_installation_failure(self, mock_exists):
        """✅ Test validación fallida de instalación FTMO Global Markets"""
        mock_exists.return_value = False
        
        result = validate_ftmo_installation()
        self.assertFalse(result)
        
        print("✅ Test validación FTMO Global Markets fallida: PASSED")

class TestMT5DataManagerDataTypes(unittest.TestCase):
    """📊 Tests de tipos de datos y estructuras"""

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    def test_account_type_enum(self):
        """✅ Test enum AccountType"""
        self.assertEqual(AccountType.DEMO.value, "DEMO")
        self.assertEqual(AccountType.REAL.value, "REAL") 
        self.assertEqual(AccountType.CONTEST.value, "CONTEST")
        self.assertEqual(AccountType.FUNDING.value, "FUNDING")
        self.assertEqual(AccountType.UNKNOWN.value, "UNKNOWN")
        
        print("✅ Test AccountType enum: PASSED")

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    def test_tick_data_creation(self):
        """✅ Test creación de MT5TickData"""
        tick_data = MT5TickData(
            symbol="EURUSD",
            bid=1.0950,
            ask=1.0952,
            last=1.0951,
            volume=100,
            time=int(time.time()),
            flags=0
        )
        
        self.assertEqual(tick_data.symbol, "EURUSD")
        self.assertAlmostEqual(tick_data.spread, 0.0002, places=4)  # Usar assertAlmostEqual para floats
        self.assertEqual(tick_data.mid_price, 1.0951)
        self.assertIsInstance(tick_data.timestamp, datetime)
        
        print("✅ Test creación TickData: PASSED")

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    def test_historical_data_creation(self):
        """✅ Test creación de MT5HistoricalData"""
        historical_data = MT5HistoricalData(
            symbol="EURUSD",
            timeframe="M1",
            data=None,  # Mock data
            bars_count=1000,
            download_time=datetime.now()
        )
        
        self.assertEqual(historical_data.symbol, "EURUSD")
        self.assertEqual(historical_data.timeframe, "M1")
        self.assertEqual(historical_data.bars_count, 1000)
        self.assertFalse(historical_data.from_cache)
        
        print("✅ Test creación HistoricalData: PASSED")

class TestMT5DataManagerTimeframes(unittest.TestCase):
    """⏰ Tests de gestión de timeframes"""

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    def test_timeframe_mapping(self):
        """✅ Test mapeo de timeframes"""
        expected_timeframes = ['M1', 'M3', 'M5', 'M15', 'H1', 'H4', 'D1']
        
        for tf in expected_timeframes:
            self.assertIn(tf, TIMEFRAME_MAPPING)
            self.assertIsInstance(TIMEFRAME_MAPPING[tf], int)
        
        print("✅ Test mapeo timeframes: PASSED")

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    @patch('utils.mt5_data_manager.MT5_AVAILABLE', True)
    @patch('utils.mt5_data_manager.mt5')
    def test_get_timeframe_constant(self, mock_mt5):
        """✅ Test obtención de constante de timeframe"""
        manager = MT5DataManager()
        
        # Mock MT5 timeframe constants
        mock_mt5.TIMEFRAME_M1 = 1
        mock_mt5.TIMEFRAME_M5 = 5
        
        # Test timeframes de minutos
        result = manager.get_timeframe_constant('M1')
        self.assertEqual(result, 1)
        
        # Test timeframes con constantes directas
        result = manager.get_timeframe_constant('H1')
        self.assertEqual(result, TIMEFRAME_MAPPING['H1'])
        
        print("✅ Test obtención timeframe constant: PASSED")

class TestMT5DataManagerStatus(unittest.TestCase):
    """📊 Tests de estado y métricas"""

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    def test_get_status(self):
        """✅ Test obtención de estado"""
        manager = MT5DataManager(config={'enable_debug': True})
        status = manager.get_status()
        
        # Verificar estructura de status
        required_keys = [
            'is_connected', 'mt5_available', 'account_type',
            'connection_attempts', 'sic_integration', 'connection_info'
        ]
        
        for key in required_keys:
            self.assertIn(key, status)
        
        # Verificar integración SIC
        self.assertIn('version', status['sic_integration'])
        self.assertEqual(status['sic_integration']['version'], 'v3.1')
        
        print("✅ Test obtención estado: PASSED")

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    def test_get_performance_report(self):
        """✅ Test reporte de performance"""
        manager = MT5DataManager()
        
        # Simular algunas operaciones
        manager._performance_metrics.append({
            'operation': 'test_connect',
            'duration': 0.5,
            'success': True,
            'timestamp': time.time()
        })
        
        report = manager.get_performance_report()
        
        # Verificar estructura del reporte
        required_keys = [
            'total_operations', 'total_duration', 'connection_attempts',
            'cache_performance', 'sic_integration_active'
        ]
        
        for key in required_keys:
            self.assertIn(key, report)
        
        self.assertEqual(report['total_operations'], 1)
        
        print("✅ Test reporte performance: PASSED")

class TestMT5DataManagerFunctionality(unittest.TestCase):
    """⚙️ Tests de funcionalidades principales (con mocks)"""

    def setUp(self):
        """Configurar mocks para tests"""
        self.manager = None
        if MT5_MANAGER_AVAILABLE:
            self.manager = MT5DataManager(config={'enable_debug': False})

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    @patch('utils.mt5_data_manager.MT5_AVAILABLE', False)
    def test_operations_without_mt5(self):
        """✅ Test operaciones sin MT5 disponible"""
        manager = MT5DataManager()
        
        # Todas estas operaciones deben fallar gracefully
        self.assertFalse(manager.connect())
        self.assertIsNone(manager.get_symbol_tick("EURUSD"))
        self.assertIsNone(manager.get_historical_data("EURUSD", "M1"))
        
        print("✅ Test operaciones sin MT5: PASSED")

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    @patch('utils.mt5_data_manager.MT5_AVAILABLE', True)
    @patch('utils.mt5_data_manager.mt5')
    @patch('utils.mt5_data_manager.validate_ftmo_installation')
    def test_connect_without_ftmo(self, mock_validate, mock_mt5):
        """✅ Test conexión sin FTMO Global Markets instalado"""
        mock_validate.return_value = False
        
        manager = MT5DataManager()
        result = manager.connect()
        
        self.assertFalse(result)
        print("✅ Test conexión sin FTMO Global Markets: PASSED")

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    def test_disconnect_without_connection(self):
        """✅ Test desconexión sin conexión activa"""
        manager = MT5DataManager()
        
        # No debería fallar aunque no esté conectado
        try:
            manager.disconnect()
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
        print("✅ Test desconexión sin conexión: PASSED")

class TestMT5DataManagerCompatibility(unittest.TestCase):
    """🔄 Tests de compatibilidad y funciones legacy"""

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    @patch('utils.mt5_data_manager.get_mt5_manager')
    def test_descargar_y_guardar_m1_function(self, mock_get_manager):
        """✅ Test función de compatibilidad descargar_y_guardar_m1"""
        # Mock manager con conexión fallida
        mock_manager = Mock()
        mock_manager.connect.return_value = False
        mock_get_manager.return_value = mock_manager
        
        result = descargar_y_guardar_m1("EURUSD", 1000)
        self.assertFalse(result)
        
        # Mock manager con conexión exitosa pero sin datos
        mock_manager.connect.return_value = True
        mock_manager.get_historical_data.return_value = None
        
        result = descargar_y_guardar_m1("EURUSD", 1000)
        self.assertFalse(result)
        
        print("✅ Test función compatibilidad M1: PASSED")

class TestMT5DataManagerIntegration(unittest.TestCase):
    """🔗 Tests de integración completa"""

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    def test_full_manager_lifecycle(self):
        """✅ Test ciclo de vida completo del manager"""
        # Crear manager
        manager = get_mt5_manager({
            'enable_debug': True,
            'use_predictive_cache': True,
            'enable_lazy_loading': True
        })
        
        # Verificar estado inicial
        status = manager.get_status()
        self.assertFalse(status['is_connected'])
        
        # Verificar funciones disponibles
        self.assertIsInstance(manager.available_functions, dict)
        
        # Obtener reporte de performance (sin operaciones)
        report = manager.get_performance_report()
        # Verificar que el reporte se genera, incluso sin operaciones
        self.assertIn('total_operations', report)
        
        # Simular cleanup
        manager.disconnect()
        
        print("✅ Test ciclo vida completo: PASSED")

    @unittest.skipUnless(MT5_MANAGER_AVAILABLE, "MT5DataManager no disponible")
    def test_thread_safety_basic(self):
        """✅ Test básico de thread safety"""
        import threading
        
        manager = MT5DataManager()
        results = []
        
        def test_operation():
            try:
                status = manager.get_status()
                results.append(status['is_connected'])
            except Exception as e:
                results.append(f"Error: {e}")
        
        # Crear múltiples threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=test_operation)
            threads.append(thread)
            thread.start()
        
        # Esperar que terminen
        for thread in threads:
            thread.join()
        
        # Verificar que todas las operaciones fueron exitosas
        self.assertEqual(len(results), 5)
        for result in results:
            self.assertIsInstance(result, bool)  # No debe haber errores
        
        print("✅ Test thread safety básico: PASSED")

def run_mt5_data_manager_tests():
    """🚀 Ejecutar todos los tests del MT5DataManager"""
    print("🧪 INICIANDO TESTS MT5DATAMANAGER v6.0 ENTERPRISE")
    print("=" * 60)
    
    if not MT5_MANAGER_AVAILABLE:
        print("❌ MT5DataManager no está disponible para testing")
        return False
    
    # Crear suite de tests
    test_suite = unittest.TestSuite()
    
    # Agregar clases de test
    test_classes = [
        TestMT5DataManagerBasics,
        TestMT5DataManagerSecurity,
        TestMT5DataManagerDataTypes,
        TestMT5DataManagerTimeframes,
        TestMT5DataManagerStatus,
        TestMT5DataManagerFunctionality,
        TestMT5DataManagerCompatibility,
        TestMT5DataManagerIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS MT5DATAMANAGER v6.0:")
    print(f"   ✅ Tests ejecutados: {result.testsRun}")
    print(f"   ❌ Fallos: {len(result.failures)}")
    print(f"   ⚠️  Errores: {len(result.errors)}")
    print(f"   ⏭️  Omitidos: {len(result.skipped)}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    if success:
        print("🏆 TODOS LOS TESTS PASARON - MT5DataManager v6.0 VALIDADO ✅")
    else:
        print("⚠️  ALGUNOS TESTS FALLARON - REVISAR IMPLEMENTACIÓN")
    
    return success

if __name__ == "__main__":
    print("🏆 MT5DATAMANAGER v6.0 ENTERPRISE - COMPONENT TEST SUITE")
    print("📡 COMPONENTE FUNDAMENTAL #1 - SIN ESTE NO FUNCIONA NADA")
    print()
    
    success = run_mt5_data_manager_tests()
    
    if success:
        print("\n🚀 MT5DataManager v6.0 Enterprise: LISTO PARA PRODUCCIÓN")
        print("🔗 Preparado para integración con el resto del sistema ICT Engine")
        print("🏆 POSICIÓN CONFIRMADA: COMPONENTE FUNDAMENTAL #1")
    else:
        print("\n⚠️  Revisar implementación antes de continuar")
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("   1. ✅ MT5DataManager (COMPLETADO)")
    print("   2. ⏳ Integrar Advanced Candle Downloader")
    print("   3. ⏳ Crear sistema de análisis ICT")
    print("   4. ⏳ Implementar POI System")
    print("   5. ⏳ Dashboard y widgets principales")
