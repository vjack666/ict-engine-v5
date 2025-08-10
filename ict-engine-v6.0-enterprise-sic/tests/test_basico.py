#!/usr/bin/env python3

print("TEST BÁSICO - INICIO")

try:
    print("1. Importando sys...")
    import sys
    print(f"   Python: {sys.version_info}")
    
    print("2. Importando os...")
    import os
    print(f"   Directorio: {os.getcwd()}")
    
    print("3. Importando rich...")
    from rich.console import Console
    console = Console()
    console.print("   [green]Rich OK[/green]")
    
    print("4. Test completo")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("TEST BÁSICO - FIN")
