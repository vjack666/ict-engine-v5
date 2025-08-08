#!/usr/bin/env python3
"""
🎯 SCRIPT DE PRUEBA - MOTOR DE BACKTESTING ICT REAL
==================================================

Script para probar la integración completa del motor de backtesting
con el sistema ICT real del usuario.

Este script ejecuta:
- Backtesting con MT5DataManager real
- Detección POI con POIDetector real  
- Análisis ICT con ICTDetector real
- Scoring con ConfidenceEngine real
- Veredictos con VeredictoEngine real

Versión: v6.0.0
Fecha: 7 Agosto 2025
"""

import sys
import os
from pathlib import Path

# Añadir directorio del proyecto
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Importar el motor real
from core.backtesting.real_data_backtest_engine import (
    RealICTBacktestEngine, 
    RealBacktestConfig,
    run_complete_real_ict_backtest
)

def test_real_integration():
    """Probar la integración con el sistema real"""
    
    print("🚀 PRUEBA DE INTEGRACIÓN - SISTEMA ICT REAL")
    print("="*60)
    
    try:
        # Ejecutar test completo
        results = run_complete_real_ict_backtest()
        
        if results:
            print("\n✅ INTEGRACIÓN EXITOSA")
            print(f"📊 Estrategias probadas: {len(results.get('strategies', {}))}")
            print(f"💰 Profit total: ${results.get('performance', {}).get('total_profit', 0):.2f}")
            print(f"🎯 Win rate promedio: {results.get('performance', {}).get('avg_win_rate', 0):.1f}%")
            
            # Validar componentes reales
            validation = results.get('components_validation', {})
            print(f"\n🔧 COMPONENTES INTEGRADOS:")
            for component, status in validation.items():
                print(f"   {component}: {status}")
            
            return True
        else:
            print("❌ Error: No se obtuvieron resultados")
            return False
            
    except Exception as e:
        print(f"❌ Error en la integración: {e}")
        return False

def quick_test():
    """Test rápido de configuración"""
    
    print("⚡ TEST RÁPIDO DE CONFIGURACIÓN")
    print("="*40)
    
    try:
        from datetime import datetime
        
        # Configuración básica
        config = RealBacktestConfig(
            symbol='EURUSD',
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 1, 31),  # Solo 1 mes para test rápido
            timeframes=['M15', 'H1'],
            strategies=['Fair_Value_Gaps'],  # Solo una estrategia
            confidence_threshold=0.65
        )
        
        # Crear motor
        engine = RealICTBacktestEngine(config)
        
        print("✅ Motor inicializado correctamente")
        print("✅ Componentes reales cargados")
        print("✅ Configuración válida")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

if __name__ == "__main__":
    
    print("🎯 MOTOR DE BACKTESTING ICT REAL v6.0")
    print("Sistema de prueba de integración")
    print("="*50)
    
    # Test rápido primero
    if quick_test():
        print("\n" + "="*50)
        
        # Preguntar si ejecutar test completo
        response = input("\n¿Ejecutar test completo de integración? (y/n): ").lower()
        
        if response in ['y', 'yes', 's', 'si']:
            print("\n" + "="*50)
            test_real_integration()
        else:
            print("\n✅ Test rápido completado. Sistema listo para uso.")
    else:
        print("\n❌ Test rápido falló. Verificar configuración.")
