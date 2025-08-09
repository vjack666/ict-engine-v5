#!/usr/bin/env python3
"""
🐛 DEBUG DASHBOARD SIMPLE - Para diagnosticar problema de pestañas vacías
================================================================================
"""

import sys
from pathlib import Path

# Textual imports for tabbed interface
try:
    from textual.app import App, ComposeResult
    from textual.containers import Container
    from textual.widgets import Header, Footer, Static, TabbedContent, TabPane
    from textual.binding import Binding
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False
    print("⚠️ Textual no disponible")
    sys.exit(1)

class SimpleDebugDashboard(App):
    """Dashboard simple para debug"""
    
    TITLE = "🐛 DEBUG DASHBOARD - ICT ENGINE"
    
    CSS = """
    .tab-content {
        height: 100%;
        overflow-y: auto;
        padding: 1;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Salir", show=True),
    ]
    
    def compose(self) -> ComposeResult:
        """Crear la interfaz"""
        yield Header()
        
        # ÁREA DE PESTAÑAS PRINCIPALES
        with TabbedContent(initial="tab_test1", id="main_tabs"):
            
            # PESTAÑA 1: TEST BÁSICO
            with TabPane("🟢 Test 1", id="tab_test1"):
                with Container(classes="tab-content"):
                    yield Static(
                        "[bold green]✅ CONTENIDO DE PRUEBA 1[/bold green]\n\nSi puedes leer esto, las pestañas funcionan correctamente.\n\nEsta es la pestaña de prueba número 1.",
                        id="test1_display"
                    )
            
            # PESTAÑA 2: TEST AVANZADO
            with TabPane("🔍 Test 2", id="tab_test2"):
                with Container(classes="tab-content"):
                    yield Static(
                        self.render_test_content(),
                        id="test2_display"
                    )
            
            # PESTAÑA 3: TEST DINÁMICO
            with TabPane("⚡ Test 3", id="tab_test3"):
                with Container(classes="tab-content"):
                    yield Static(
                        "[bold blue]🔄 CONTENIDO DINÁMICO[/bold blue]\n\nEsta pestaña tiene contenido generado dinámicamente.\n\nFunción render llamada correctamente.",
                        id="test3_display"
                    )
        
        yield Footer()
    
    def render_test_content(self) -> str:
        """Renderizar contenido de prueba"""
        return """[bold cyan]🧪 CONTENIDO DE PRUEBA RENDERIZADO[/bold cyan]

Si puedes leer esto, significa que:
✅ El método render_test_content() funciona
✅ Las pestañas cargan contenido dinámico
✅ El sistema de rendering está operativo

INFORMACIÓN DE DEBUG:
• Python version: """ + sys.version.split()[0] + """
• Textual disponible: """ + str(TEXTUAL_AVAILABLE) + """
• Dashboard funcionando correctamente

SIGUIENTES PASOS:
• Si ves este contenido, el problema no está en Textual
• El problema debe estar en los métodos render_* del dashboard principal
• Revisar cada método render_* individualmente
"""

def main():
    """Función principal de debug"""
    if not TEXTUAL_AVAILABLE:
        print("❌ Error: Textual no está disponible")
        return
    
    print("🐛 Iniciando Dashboard de Debug Simple...")
    print("📋 Instrucciones:")
    print("   • Usa las flechas ← → para cambiar entre pestañas")
    print("   • Presiona 'q' para salir")
    print("   • Verifica si el contenido se muestra en cada pestaña")
    print()
    
    app = SimpleDebugDashboard()
    app.run()

if __name__ == "__main__":
    main()
