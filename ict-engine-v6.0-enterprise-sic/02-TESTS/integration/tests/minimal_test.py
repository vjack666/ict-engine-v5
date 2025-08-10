#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard mínimo para debug
"""

from textual.app import App, ComposeResult
from textual.widgets import Static, TabbedContent, TabPane

class MinimalDashboard(App):
    """Dashboard mínimo para identificar el problema"""
    
    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Tab 1"):
                yield Static("TEXTO SIMPLE DE PRUEBA EN TAB 1")
            
            with TabPane("Tab 2"):
                yield Static("TEXTO SIMPLE DE PRUEBA EN TAB 2")

if __name__ == "__main__":
    app = MinimalDashboard()
    app.run()
