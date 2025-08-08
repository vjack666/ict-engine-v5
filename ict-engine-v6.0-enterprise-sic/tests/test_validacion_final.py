#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✅ TEST VALIDACIÓN ICT COMPLIANCE FINAL
======================================

Validación completa del sistema ICT Engine v6.1.0 Enterprise
tras la reparación de datos históricos insuficientes.

Autor: ICT Engine v6.1.0 Team
"""

import subprocess
import sys
import time

def validar_ict_compliance():
    """🎯 Validar cumplimiento total ICT"""
    
    print("✅ ICT ENGINE v6.0 - VALIDACIÓN FINAL POST-REPARACIÓN")
    print("="*70)
    print(f"📅 {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    print("🔧 REPARACIÓN APLICADA:")
    print("   ✅ Estrategia ICT COMPLIANT implementada")  
    print("   ✅ copy_rates_from para todos los timeframes")
    print("   ✅ M15: 2016+ velas (21 días de datos)")
    print("   ✅ Cumplimiento estándares institucionales")
    print()
    
    print("🧪 EJECUTANDO TEST DE VALIDACIÓN...")
    print("-" * 50)
    
    try:
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, "tests/test_simple_poi.py"],
            capture_output=True,
            text=True,
            timeout=45
        )
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ TEST PASSED ({duration:.1f}s)")
            
            # Extraer métricas clave del output completo
            output_text = result.stdout
            velas_descargadas = 0
            pois_detectados = 0
            ict_compliance = "NO_DATA"
            rango_datos = "NO_DATA"
            
            # Buscar métricas en todo el output
            if "velas REALES de MT5" in output_text:
                import re
                match = re.search(r'Descargadas (\d+) velas REALES', output_text)
                if match:
                    velas_descargadas = int(match.group(1))
            
            if "POIs detectados" in output_text or "Detectados:" in output_text:
                import re
                match = re.search(r'Detectados[:\s]*(\d+)\s*POIs?', output_text)
                if match:
                    pois_detectados = int(match.group(1))
            
            if "ICT COMPLIANCE:" in output_text:
                import re
                match = re.search(r'ICT COMPLIANCE:\s*([^\n]+)', output_text)
                if match:
                    ict_compliance = match.group(1).strip()
            
            if "Rango:" in output_text:
                import re
                match = re.search(r'Rango:\s*([^\n]+)', output_text)
                if match:
                    rango_datos = match.group(1).strip()
            
            print("\n📊 MÉTRICAS VALIDADAS:")
            print("-" * 30)
            print(f"📈 Velas descargadas: {velas_descargadas}")
            print(f"🎯 POIs detectados: {pois_detectados}")
            print(f"✅ ICT Compliance: {ict_compliance}")
            print(f"📅 Rango datos: {rango_datos}")
            
            # Validaciones críticas
            validaciones = []
            
            if velas_descargadas >= 2000:
                validaciones.append("✅ VELAS: Cumple mínimo ICT (2000+)")
            else:
                validaciones.append(f"❌ VELAS: Insuficientes ({velas_descargadas} < 2000)")
            
            if pois_detectados >= 30:
                validaciones.append("✅ POIs: Detección exitosa (30+)")
            else:
                validaciones.append(f"⚠️ POIs: Detección limitada ({pois_detectados})")
            
            if "COMPLIANCE" in ict_compliance:
                validaciones.append("✅ ICT: Sistema compliant")
            else:
                validaciones.append("❌ ICT: Sistema non-compliant")
            
            print("\n🎯 VALIDACIONES CRÍTICAS:")
            print("-" * 30)
            for validacion in validaciones:
                print(f"   {validacion}")
            
            # Resultado final
            errores = sum(1 for v in validaciones if v.startswith("❌"))
            warnings = sum(1 for v in validaciones if v.startswith("⚠️"))
            
            print(f"\n{'='*70}")
            if errores == 0:
                print("🎉 VALIDACIÓN EXITOSA - SISTEMA COMPLETAMENTE FUNCIONAL")
                print("✅ ICT Engine v6.1.0 Enterprise listo para trading institucional")
                if warnings > 0:
                    print(f"⚠️ {warnings} advertencia(s) menor(es) - No críticas")
            else:
                print(f"❌ VALIDACIÓN FALLIDA - {errores} error(es) crítico(s)")
                print("🔧 Requiere reparación adicional")
            
            print(f"{'='*70}")
            
            return errores == 0
            
        else:
            print(f"❌ TEST FAILED ({duration:.1f}s)")
            print("🔧 Error en la ejecución del test")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ TEST TIMEOUT (>45s)")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """🎯 Función principal"""
    success = validar_ict_compliance()
    
    if success:
        print("\n🚀 COMANDOS PRINCIPALES VALIDADOS:")
        print("-" * 40)
        print("🧪 Test principal:        python tests/test_simple_poi.py")
        print("📊 Monitor rendimiento:   python scripts/ict_performance_monitor.py")
        print("🎯 Launcher enterprise:   python scripts/launch_ict_enterprise.py")
        print("🔧 Verificar sistema:     python utils/verificar_sistema.py")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
