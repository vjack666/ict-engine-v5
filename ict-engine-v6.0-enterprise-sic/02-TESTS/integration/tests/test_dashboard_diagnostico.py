#!/usr/bin/env python3
"""
🔧 TEST DIAGNÓSTICO - Dashboard ICT Regla #10
================================================================================
Test paso a paso para identificar el problema del dashboard
================================================================================
"""

import sys
import os
from pathlib import Path

print("🔧 DIAGNÓSTICO DASHBOARD ICT - REGLA #10")
print("=" * 60)

# Test 1: Verificar Python y ubicación
print("\n1️⃣ VERIFICANDO PYTHON Y UBICACIÓN")
print(f"   Python version: {sys.version}")
print(f"   Directorio actual: {os.getcwd()}")
print(f"   Archivo test: {__file__}")

# Test 2: Verificar Rich
print("\n2️⃣ VERIFICANDO RICH")
try:
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.panel import Panel
    console = Console()
    console.print("   ✅ Rich imports OK")
except Exception as e:
    print(f"   ❌ Error Rich: {e}")
    sys.exit(1)

# Test 3: Verificar paths del sistema
print("\n3️⃣ VERIFICANDO PATHS DEL SISTEMA")
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
data_dir = parent_dir / "data" / "candles"

print(f"   Directorio actual: {current_dir}")
print(f"   Directorio padre: {parent_dir}")
print(f"   Directorio datos: {data_dir}")
print(f"   Datos existe: {data_dir.exists()}")

if data_dir.exists():
    csv_files = list(data_dir.glob("*.csv"))
    print(f"   Archivos CSV encontrados: {len(csv_files)}")
    if len(csv_files) > 0:
        print(f"   Ejemplo: {csv_files[0].name}")
else:
    print("   ⚠️ Directorio de datos no encontrado")

# Test 4: Verificar backtester
print("\n4️⃣ VERIFICANDO BACKTESTER")
try:
    sys.path.append(str(current_dir))
    print(f"   Path añadido: {current_dir}")
    
    # Verificar si existe el archivo
    backtester_file = current_dir / "modular_ict_backtester.py"
    print(f"   Archivo backtester: {backtester_file}")
    print(f"   Existe: {backtester_file.exists()}")
    
    if backtester_file.exists():
        # Intentar importar
        from modular_ict_backtester import ModularICTBacktester, ModuleResult
        print("   ✅ Import backtester OK")
        
        # Verificar si se puede instanciar
        data_path = str(data_dir) if data_dir.exists() else "test_path"
        print(f"   Probando instanciar con path: {data_path}")
        
        backtester = ModularICTBacktester(data_path=data_path)
        print("   ✅ Instanciación backtester OK")
        
    else:
        print("   ❌ Archivo modular_ict_backtester.py no encontrado")
        
except Exception as e:
    print(f"   ❌ Error backtester: {e}")
    import traceback
    print(f"   Traceback: {traceback.format_exc()}")

# Test 5: Test básico de Rich display
print("\n5️⃣ TEST BÁSICO RICH DISPLAY")
try:
    console = Console()
    
    # Test tabla básica
    table = Table(show_header=False, box=None)
    table.add_row("🎯 ORDER_BLOCKS", "████████████████████", "Precisión: 84.2%", "2,596 patterns", "✅")
    
    console.print("\n   Test tabla:")
    console.print(table)
    
    # Test panel
    panel = Panel.fit("🎯 ICT ENGINE - REGLA #10", style="bright_cyan")
    console.print("\n   Test panel:")
    console.print(panel)
    
    print("\n   ✅ Rich display test OK")
    
except Exception as e:
    print(f"   ❌ Error Rich display: {e}")

# Test 6: Test threading básico
print("\n6️⃣ TEST THREADING BÁSICO")
try:
    import threading
    import time
    
    def test_thread():
        time.sleep(1)
        print("   ✅ Thread ejecutado OK")
    
    thread = threading.Thread(target=test_thread)
    thread.daemon = True
    thread.start()
    thread.join(timeout=2)
    
    if thread.is_alive():
        print("   ⚠️ Thread aún ejecutándose")
    else:
        print("   ✅ Threading test OK")
        
except Exception as e:
    print(f"   ❌ Error threading: {e}")

# Test 7: Test contextlib (para silenciar output)
print("\n7️⃣ TEST CONTEXTLIB")
try:
    import contextlib
    from io import StringIO
    
    # Test redirect stdout
    with contextlib.redirect_stdout(StringIO()):
        print("Este mensaje debe estar silenciado")
    
    print("   ✅ Contextlib test OK")
    
except Exception as e:
    print(f"   ❌ Error contextlib: {e}")

# Test 8: Test escritura de archivo
print("\n8️⃣ TEST ESCRITURA REPORTE")
try:
    import json
    from datetime import datetime
    
    reports_dir = parent_dir / "test_reports"
    reports_dir.mkdir(exist_ok=True)
    
    test_data = {
        "test": "diagnóstico",
        "timestamp": datetime.now().isoformat(),
        "status": "OK"
    }
    
    test_file = reports_dir / "test_diagnostico.json"
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2)
    
    print(f"   ✅ Archivo test creado: {test_file}")
    
except Exception as e:
    print(f"   ❌ Error escritura: {e}")

print("\n" + "=" * 60)
print("🏁 DIAGNÓSTICO COMPLETADO")

# Resumen final
print("\n📋 RESUMEN:")
print("   - Si todos los tests son ✅, el dashboard debería funcionar")
print("   - Si hay ❌, esos son los problemas a resolver")
print("   - Revisa los errores específicos arriba")

print(f"\n🕒 Test completado: {datetime.now()}")
