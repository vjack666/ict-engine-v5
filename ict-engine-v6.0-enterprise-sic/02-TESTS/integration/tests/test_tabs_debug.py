#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard ICT Engine v6.1 - VERSION DE PRUEBA PARA DEBUG DE PESTAÑAS
"""

import time
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static, TabbedContent, TabPane, Button
from textual.binding import Binding

class TestDashboard(App):
    """Dashboard de prueba para verificar contenido de pestañas"""
    
    CSS = """
    Screen {
        layout: vertical;
    }
    
    TabbedContent {
        border: solid blue;
        height: 100%;
    }
    
    TabPane {
        padding: 1;
        background: $surface;
    }
    
    .test-content {
        border: solid red;
        padding: 1;
        height: 100%;
        background: white;
        color: black;
    }
    """
    
    BINDINGS = [
        Binding("1", "switch_to_tab1", "Tab 1"),
        Binding("2", "switch_to_tab2", "Tab 2"),
        Binding("q", "quit", "Quit"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with TabbedContent(initial="tab1"):
            with TabPane("📊 Pestaña 1", id="tab1"):
                yield Static(
                    self.render_content_1(),
                    classes="test-content",
                    id="content1"
                )
            
            with TabPane("📈 Pestaña 2", id="tab2"):
                yield Static(
                    self.render_content_2(),
                    classes="test-content",
                    id="content2"
                )
        
        yield Footer()
    
    def render_content_1(self) -> str:
        return """CONTENIDO DE PRUEBA - PESTAÑA 1

Este es el contenido de la primera pestaña.

DATOS DE PRUEBA:
• Item 1: Funcional
• Item 2: En progreso  
• Item 3: Error

INSTRUCCIONES:
• Presiona 1 para esta pestaña
• Presiona 2 para la segunda pestaña
• Presiona Q para salir

CONTENIDO VISIBLE Y FUNCIONAL"""
    
    def render_content_2(self) -> str:
        return """CONTENIDO DE PRUEBA - PESTAÑA 2

Este es el contenido de la segunda pestaña.

TABLA DE PRUEBA:
┌──────────┬──────────┬──────────┐
│ Columna 1│ Columna 2│ Columna 3│
├──────────┼──────────┼──────────┤
│ Dato A   │ Dato B   │ Dato C   │
│ Dato D   │ Dato E   │ Dato F   │
└──────────┴──────────┴──────────┘

ESTADÍSTICAS:
• Total items: 6
• Completados: 4
• Pendientes: 2

SEGUNDA PESTAÑA FUNCIONAL"""
    
    async def action_switch_to_tab1(self):
        """Cambiar a pestaña 1"""
        tabs = self.query_one(TabbedContent)
        tabs.active = "tab1"
    
    async def action_switch_to_tab2(self):
        """Cambiar a pestaña 2"""
        tabs = self.query_one(TabbedContent)
        tabs.active = "tab2"

if __name__ == "__main__":
    app = TestDashboard()
    app.run()
