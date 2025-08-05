#!/usr/bin/env python3
"""
🗄️ DATA MANAGEMENT MODULE - ICT ENGINE v5.0
============================================

Módulo de gestión de datos que incluye:
- CandleCoordinator: Coordinación de descargas de velas
- Otros componentes de gestión de datos

Autor: ICT Engine v5.0
"""

# Importaciones principales del módulo
try:
    from .candle_coordinator import (
        candle_coordinator,
        CandleCoordinator,
        DownloadRequest,
        DownloadStatus,
        get_candle_coordinator,
        start_candle_coordinator,
        stop_candle_coordinator
    )

    __all__ = [
        'candle_coordinator',
        'CandleCoordinator',
        'DownloadRequest',
        'DownloadStatus',
        'get_candle_coordinator',
        'start_candle_coordinator',
        'stop_candle_coordinator'
    ]

except ImportError as e:
    try:
        from sistema.logging_interface import enviar_senal_log
        enviar_senal_log("WARNING", f"Error importando componentes de data_management: {e}", __name__, "init")
    except ImportError:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("WARNING", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("WARNING", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("WARNING", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("WARNING", mensaje, __name__, "sistema") # print(f"Warning: Error importando componentes de data_management: {e}")
    __all__ = []

# Información del módulo
__version__ = "5.0.0"
__author__ = "ICT Engine Development Team"
