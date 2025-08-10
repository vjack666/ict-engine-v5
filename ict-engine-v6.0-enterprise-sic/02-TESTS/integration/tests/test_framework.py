#!/usr/bin/env python3
"""Test básico del framework mejorado"""

import sys
from pathlib import Path

# Test de imports
try:
    from textual.app import App
    from textual.widgets import Static
    from rich.console import Console
    print("✅ Imports básicos funcionando")
except ImportError as e:
    print(f"❌ Error en imports: {e}")
    sys.exit(1)

# Test de creación de directorio
try:
    log_dir = Path("logs") / "improved_dashboard"
    log_dir.mkdir(parents=True, exist_ok=True)
    print("✅ Directorio de logs creado")
except Exception as e:
    print(f"❌ Error creando directorio: {e}")

# Test de app básica
class TestApp(App):
    def compose(self):
        yield Static("🚀 Test Framework Funcionando")

if __name__ == "__main__":
    console = Console()
    console.print("[bold green]🧪 Testing Improved Framework...[/bold green]")
    
    try:
        app = TestApp()
        print("✅ App creada exitosamente")
        console.print("[bold green]✅ Framework Test Completado[/bold green]")
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
