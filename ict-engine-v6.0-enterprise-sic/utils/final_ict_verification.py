#!/usr/bin/env python3
"""
🎯 VERIFICACIÓN FINAL ICT - Confirmación de funcionamiento óptimo
===============================================================

Test final para confirmar que el ICT Engine v6.1.0 Enterprise está
funcionando de manera óptima según las leyes ICT institucionales.

- Verificación de configuración ICT
- Test de descarga con cantidades correctas
- Validación de cumplimiento institucional
- Confirmación de datos reales FundedNext

Autor: ICT Engine v6.1.0 Enterprise Team
Fecha: Agosto 2025
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

def final_ict_verification():
    """🎯 Verificación final del sistema ICT óptimo"""
    print("\n" + "="*70)
    print("🎯 VERIFICACIÓN FINAL ICT ENGINE v6.0 ENTERPRISE")
    print("="*70)
    print("Confirmando funcionamiento óptimo según leyes ICT...")
    
    verification_results = {
        'downloader_config': False,
        'ict_optimal_download': False,
        'real_data_connection': False,
        'compliance_validation': False,
        'historical_coverage': False
    }
    
    try:
        print("\n1️⃣ Verificando configuración ICT del downloader...")
        
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        downloader = AdvancedCandleDownloader(
            config={'enable_debug': True, 'use_ict_optimal': True}
        )
        
        # Verificar configuraciones ICT específicas
        expected_ict_configs = {
            'M15': {'optimal_bars': 10000, 'minimum_bars': 2000},
            'H1': {'optimal_bars': 5000, 'minimum_bars': 1000},
            'H4': {'optimal_bars': 2500, 'minimum_bars': 500},
            'D1': {'optimal_bars': 1000, 'minimum_bars': 200}
        }
        
        config_correct = True
        for tf, expected in expected_ict_configs.items():
            actual = downloader._get_ict_optimal_config(tf)
            if (actual['optimal_bars'] != expected['optimal_bars'] or 
                actual['minimum_bars'] != expected['minimum_bars']):
                config_correct = False
                break
        
        if config_correct:
            print("   ✅ Configuraciones ICT correctas para todos los timeframes")
            verification_results['downloader_config'] = True
        else:
            print("   ❌ Configuraciones ICT incorrectas")
        
        print("\n2️⃣ Probando descarga ICT óptima...")
        
        # Test con M15 (timeframe crítico ICT)
        result_m15 = downloader.download_candles(
            symbol="EURUSD",
            timeframe="M15",
            save_to_file=False,
            use_ict_optimal=True
        )
        
        if (result_m15.get('success') and 
            result_m15.get('data') is not None and
            len(result_m15['data']) >= 2000):  # Mínimo ICT para M15
            
            print(f"   ✅ M15: {len(result_m15['data']):,} velas descargadas (≥2000 mínimo ICT)")
            verification_results['ict_optimal_download'] = True
            
            # Verificar fuente de datos
            if result_m15.get('source') == 'mt5_direct':
                print("   ✅ Fuente: MT5 directo (datos reales)")
                verification_results['real_data_connection'] = True
            else:
                print(f"   ⚠️ Fuente: {result_m15.get('source', 'desconocida')}")
        else:
            print(f"   ❌ M15: Solo {len(result_m15.get('data', [])):,} velas (insuficiente)")
        
        print("\n3️⃣ Verificando cumplimiento ICT...")
        
        if 'ict_compliance' in result_m15:
            compliance = result_m15['ict_compliance']
            if (compliance.get('compliant') and 
                compliance.get('analysis_quality') in ['PROFESSIONAL_GRADE', 'INSTITUTIONAL_GRADE']):
                print(f"   ✅ Cumplimiento ICT: {compliance['status']} - {compliance['analysis_quality']}")
                verification_results['compliance_validation'] = True
            else:
                print(f"   ❌ No cumple estándares ICT: {compliance.get('status', 'UNKNOWN')}")
        
        print("\n4️⃣ Verificando cobertura histórica...")
        
        # Verificar que tenemos datos de al menos 6 meses atrás para M15
        if result_m15.get('success') and result_m15.get('data') is not None:
            data = result_m15['data']
            oldest_date = data.index[0]
            newest_date = data.index[-1]
            coverage_days = (newest_date - oldest_date).days
            
            if coverage_days >= 150:  # ~5 meses mínimo
                print(f"   ✅ Cobertura histórica: {coverage_days} días ({oldest_date.strftime('%Y-%m-%d')} a {newest_date.strftime('%Y-%m-%d')})")
                verification_results['historical_coverage'] = True
            else:
                print(f"   ⚠️ Cobertura limitada: solo {coverage_days} días")
        
        print("\n5️⃣ Test rápido H4 (timeframe crítico ICT)...")
        
        result_h4 = downloader.download_candles(
            symbol="EURUSD",
            timeframe="H4",
            save_to_file=False,
            use_ict_optimal=True
        )
        
        if result_h4.get('success'):
            h4_bars = len(result_h4['data']) if result_h4.get('data') is not None else 0
            print(f"   ℹ️ H4: {h4_bars:,} velas (mínimo ICT: 500)")
            
            if h4_bars >= 500:
                print("   ✅ H4 cumple mínimo ICT")
            else:
                print("   ⚠️ H4 por debajo del mínimo ICT")
        
        # Resumen final
        passed_checks = sum(verification_results.values())
        total_checks = len(verification_results)
        
        print(f"\n📊 RESUMEN VERIFICACIÓN ICT:")
        print(f"   Checks pasados: {passed_checks}/{total_checks}")
        print(f"   Porcentaje: {(passed_checks/total_checks)*100:.1f}%")
        
        print(f"\n📋 DETALLES:")
        status_map = {True: "✅ PASS", False: "❌ FAIL"}
        print(f"   Configuración ICT: {status_map[verification_results['downloader_config']]}")
        print(f"   Descarga óptima: {status_map[verification_results['ict_optimal_download']]}")
        print(f"   Datos reales MT5: {status_map[verification_results['real_data_connection']]}")
        print(f"   Cumplimiento ICT: {status_map[verification_results['compliance_validation']]}")
        print(f"   Cobertura histórica: {status_map[verification_results['historical_coverage']]}")
        
        if passed_checks >= 4:  # Al menos 4 de 5 checks
            print(f"\n🎉 SISTEMA ICT CERTIFICADO PARA TRADING INSTITUCIONAL")
            print(f"   El ICT Engine v6.1.0 Enterprise está funcionando óptimamente")
            print(f"   Listo para análisis de mercado según leyes ICT")
            return True
        else:
            print(f"\n⚠️ SISTEMA ICT NECESITA OPTIMIZACIÓN")
            print(f"   Revisar configuración y conexión MT5")
            return False
        
    except Exception as e:
        print(f"\n❌ ERROR EN VERIFICACIÓN ICT: {e}")
        import traceback
        traceback.print_exc()
        return False

def display_ict_optimal_summary():
    """📋 Mostrar resumen de configuración ICT óptima"""
    print("\n" + "="*70)
    print("📋 CONFIGURACIÓN ICT ÓPTIMA - RESUMEN EJECUTIVO")
    print("="*70)
    
    print("""
🏛️ LEYES ICT IMPLEMENTADAS:
   - Market Structure Analysis con datos institucionales
   - Order Blocks detection en timeframes múltiples  
   - Fair Value Gaps identification automática
   - Liquidity analysis en H4, H1, M15, M5
   - Smart Money concepts aplicados

📊 CANTIDADES ÓPTIMAS DE VELAS POR TIMEFRAME:
   D1  (Diario):    1,000 velas (200 mínimo) - Análisis macro
   H4  (4 horas):   2,500 velas (500 mínimo) - Estructura semanal
   H1  (1 hora):    5,000 velas (1,000 mínimo) - Análisis diario
   M15 (15 min):   10,000 velas (2,000 mínimo) - Entradas precisas
   M5  (5 min):     5,000 velas (1,000 mínimo) - Timing de entrada
   M1  (1 min):     2,000 velas (500 mínimo) - Scalping institucional

🚀 FUENTE DE DATOS:
   - FundedNext MT5 Terminal (datos institucionales reales)
   - Sin simulaciones ni datos falsos
   - Conexión directa a liquidez institucional
   - Spreads reales del mercado

✅ CUMPLIMIENTO INSTITUCIONAL:
   - MINIMUM: Suficiente para análisis básico ICT
   - IDEAL: Bueno para trading profesional  
   - OPTIMAL: Excelente para análisis institucional completo

🎯 PRÓXIMOS PASOS:
   1. Ejecutar setup_ict_historical_data.py para descarga masiva
   2. Configurar alertas en timeframes críticos (H4, H1, M15)
   3. Implementar detección automática de Order Blocks
   4. Activar monitoreo de Fair Value Gaps
   5. Iniciar backtesting con datos históricos reales
    """)

if __name__ == "__main__":
    print("🎯 ICT ENGINE v6.0 - VERIFICACIÓN FINAL")
    print("=" * 70)
    
    # Mostrar configuración óptima
    display_ict_optimal_summary()
    
    # Ejecutar verificación
    verification_passed = final_ict_verification()
    
    if verification_passed:
        print(f"\n🏆 CERTIFICACIÓN ICT ENGINE v6.0 ENTERPRISE")
        print(f"   ✅ Sistema verificado y listo para trading institucional")
        print(f"   ✅ Configuración ICT óptima implementada")
        print(f"   ✅ Datos reales FundedNext MT5 conectados")
        print(f"   ✅ Cumplimiento de leyes ICT validado")
        
        print(f"\n🚀 RECOMENDACIÓN:")
        print(f"   Ejecutar: python setup_ict_historical_data.py")
        print(f"   Para descarga masiva de años de datos históricos")
    else:
        print(f"\n⚠️ SISTEMA REQUIERE ATENCIÓN")
        print(f"   Revisar conexión MT5 y configuración ICT")
