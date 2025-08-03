#!/usr/bin/env python3
"""
🔗 CANDLE DOWNLOADER INTEGRATION - ICT ENGINE v5.0
==================================================

Módulo de integración entre AdvancedCandleDownloader, Dashboard y ICT Engine
Proporciona funciones de conveniencia para integración completa

Creado por Sprint 1.2 Executor
"""

from typing import Dict, List, Optional, Callable
import sys
from pathlib import Path

# Importaciones seguras
try:
    from core.data_management.candle_coordinator import candle_coordinator
except ImportError:
    print("Warning: No se pudo importar candle_coordinator")
    candle_coordinator = None

try:
    from dashboard.candle_downloader_widget import candle_downloader_widget
except ImportError:
    print("Warning: No se pudo importar candle_downloader_widget")
    candle_downloader_widget = None

try:
    from advanced_candle_downloader import AdvancedCandleDownloader
except ImportError:
    print("Warning: No se pudo importar AdvancedCandleDownloader")
    AdvancedCandleDownloader = None

class CandleDownloaderIntegration:
    """
    🔗 INTEGRACIÓN COMPLETA DEL CANDLE DOWNLOADER
    
    Coordina entre:
    - AdvancedCandleDownloader (descarga real)
    - CandleCoordinator (orquestación)
    - CandleDownloaderWidget (UI)
    - Dashboard (visualización)
    - ICT Engine (consumo de datos)
    """
    
    def __init__(self):
        self.coordinator = candle_coordinator
        self.widget = candle_downloader_widget
        self.is_integrated = False
        
    def setup_integration(self) -> bool:
        """Configura integración completa"""
        try:
            if not self.coordinator or not self.widget:
                print("Error: Componentes no disponibles para integración")
                return False
                
            # Conectar callbacks del coordinador con el widget
            self.coordinator.set_progress_callback(self.widget.on_progress_update)
            self.coordinator.set_completion_callback(self.widget.on_download_completed)
            self.coordinator.set_error_callback(self.widget.on_download_error)
            
            # Iniciar coordinador
            if self.coordinator.start_coordinator():
                self.is_integrated = True
                return True
            return False
            
        except Exception as e:
            print(f"Error en setup_integration: {e}")
            return False
    
    def start_download_session(self, symbols: List[str] = None, 
                             timeframes: List[str] = None,
                             lookback: int = 50000) -> bool:
        """Inicia sesión de descarga completa"""
        if not self.is_integrated:
            if not self.setup_integration():
                return False
        
        # Usar valores por defecto si no se especifican
        symbols = symbols or ["EURUSD"]
        timeframes = timeframes or ["H4", "H1", "M15", "M5"]
        
        try:
            # Configurar widget
            if self.widget:
                self.widget.configure_symbols(symbols)
                self.widget.configure_timeframes(timeframes)
                self.widget.configure_lookback(lookback)
                self.widget.start_download()
            
            # Iniciar descarga coordinada
            if self.coordinator:
                for symbol in symbols:
                    for timeframe in timeframes:
                        self.coordinator.queue_download(symbol, timeframe, lookback)
            
            return True
            
        except Exception as e:
            print(f"Error iniciando descarga: {e}")
            return False
    
    def stop_download_session(self):
        """Detiene sesión de descarga"""
        if self.widget:
            self.widget.stop_download()
        # El coordinador sigue corriendo en background
    
    def download_for_ict_analysis(self, symbol: str = "EURUSD") -> bool:
        """Descarga datos específicamente para análisis ICT"""
        # Timeframes prioritarios para ICT
        ict_timeframes = ["H4", "H1", "M15", "M5"]
        
        return self.start_download_session([symbol], ict_timeframes, 100000)
    
    def auto_update_stale_data(self, max_age_hours: int = 24) -> int:
        """Auto-actualiza datos obsoletos"""
        if not self.is_integrated:
            self.setup_integration()
            
        if not self.widget or not self.coordinator:
            return 0
            
        symbols = self.widget.selected_symbols
        timeframes = self.widget.selected_timeframes
        
        return self.coordinator.auto_update_stale_data(symbols, timeframes, max_age_hours)
    
    def get_integration_status(self) -> Dict:
        """Obtiene estado de la integración"""
        coordinator_status = self.coordinator.get_status() if self.coordinator else {}
        widget_stats = self.widget.download_stats if self.widget else {}
        
        return {
            'is_integrated': self.is_integrated,
            'coordinator_status': coordinator_status,
            'widget_downloading': self.widget.is_downloading if self.widget else False,
            'widget_stats': widget_stats
        }
    
    def trigger_emergency_download(self, symbol: str, timeframe: str) -> bool:
        """Descarga de emergencia (inmediata)"""
        if not self.is_integrated:
            self.setup_integration()
            
        if not self.coordinator:
            return False
            
        return self.coordinator.download_immediate(symbol, timeframe, 50000)

# Instancia global para usar desde cualquier parte del sistema
downloader_integration = CandleDownloaderIntegration()

# Funciones de conveniencia
def start_download(symbols: List[str] = None, timeframes: List[str] = None) -> bool:
    """Función de conveniencia para iniciar descarga"""
    return downloader_integration.start_download_session(symbols, timeframes)

def stop_download():
    """Función de conveniencia para detener descarga"""
    downloader_integration.stop_download_session()

def download_for_trading(symbol: str = "EURUSD") -> bool:
    """Función de conveniencia para descarga de trading"""
    return downloader_integration.download_for_ict_analysis(symbol)

def get_downloader_status() -> Dict:
    """Función de conveniencia para obtener estado"""
    return downloader_integration.get_integration_status()
