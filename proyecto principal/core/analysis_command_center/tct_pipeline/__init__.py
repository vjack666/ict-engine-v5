# 🎯 TCT PIPELINE - TIME TO COMPLETE MEASUREMENT SYSTEM
# ARQUITECTURA: Motor de mediciones de tiempo completo para análisis ICT
# PROTOCOLO: "Caja Negra" - Silent terminal, comprehensive logging

from .tct_measurements import TCTMeasurementEngine, TCTMetrics
from .tct_aggregator import TCTAggregator, AggregatedTCTMetrics
from .tct_formatter import TCTFormatter
from .tct_interface import TCTInterface

__all__ = [
    'TCTMeasurementEngine',
    'TCTMetrics',
    'TCTAggregator',
    'AggregatedTCTMetrics',
    'TCTFormatter',
    'TCTInterface'
]

# 📊 VERSIÓN Y METADATA
__version__ = "1.0.0"
__description__ = "Sistema de mediciones TCT para ICT Engine v3.4"
__protocol__ = "CAJA_NEGRA"
