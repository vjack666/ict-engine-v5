#!/usr/bin/env python3
"""
❌ DEPRECATED - CANDLE COORDINATOR
=================================

⚠️  ESTE ARCHIVO HA SIDO DEPRECADO EN SPRINT 1.2 REFACTORED

Razón: Duplicación innecesaria de funcionalidad del AdvancedCandleDownloader

Migración:
- Usa directamente: utils.advanced_candle_downloader.AdvancedCandleDownloader  
- Para funciones de conveniencia: utils.candle_integration
- Para widget simplificado: dashboard.simple_candle_widget

El AdvancedCandleDownloader ahora incluye:
✅ Callbacks integrados
✅ Sistema de colas con prioridades  
✅ Coordinación automática
✅ Auto-update de datos obsoletos

Backup guardado en: candle_coordinator_deprecated_backup.py
"""

import warnings

class CandleCoordinator:
    """CLASE DEPRECADA - Usar AdvancedCandleDownloader directamente"""
    
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "CandleCoordinator está deprecado. "
            "Usa utils.advanced_candle_downloader.AdvancedCandleDownloader directamente. "
            "Ver utils.candle_integration para funciones de conveniencia.",
            DeprecationWarning,
            stacklevel=2
        )
        
        # Intentar importar el downloader mejorado como fallback
        try:
            from utils.advanced_candle_downloader import AdvancedCandleDownloader
            self._downloader = AdvancedCandleDownloader()
            print("⚠️  CandleCoordinator deprecado. Usando AdvancedCandleDownloader como fallback.")
        except ImportError:
            self._downloader = None
            print("❌ Error: No se pudo cargar AdvancedCandleDownloader. Actualiza tu sistema.")
    
    def __getattr__(self, name):
        """Redirigir llamadas al downloader como fallback temporal"""
        if self._downloader and hasattr(self._downloader, name):
            return getattr(self._downloader, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

# Mantener compatibilidad temporal
candle_coordinator = CandleCoordinator()
