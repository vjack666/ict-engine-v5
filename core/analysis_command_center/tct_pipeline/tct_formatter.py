#!/usr/bin/env python3
"""
📊 TCT FORMATTER - Formateador de salida para mediciones TCT
BASADO EN: Lógica de generate_health_report del health_analyzer.py
PROTOCOLO: "Caja Negra" - Formateo inteligente para dashboard y exports
"""

import json
import datetime
from typing import Dict, Any, List
from pathlib import Path

# 🔌 IMPORTS DEL ICT ENGINE
from sistema.logging_interface import enviar_senal_log, log_tct
from utils.logging_utils import save_adaptive_debug_to_csv
from .tct_aggregator import AggregatedTCTMetrics

class TCTFormatter:
    """
    Formateador de salida TCT - Inspirado en health_analyzer
    Genera formatos para dashboard, logs y exports
    """
    
    def __init__(self, exports_dir: str = "data/exports/tct"):
        """Inicialización del formateador"""
        
        self.exports_dir = Path(exports_dir)
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        
        # 📝 CAJA NEGRA - LOG INICIALIZACIÓN
        enviar_senal_log(
            nivel='DEBUG',
            mensaje=f"TCT Formatter inicializado | Exports: {self.exports_dir}",
            fuente='tct_formatter',
            categoria='tct'
        )
        
        enviar_senal_log(
            nivel='INFO',
            mensaje="TCT Formatter - Sistema de formateo activado",
            fuente='tct_formatter',
            categoria='tct'
        )
    
    def format_for_dashboard(self, aggregated_metrics: AggregatedTCTMetrics) -> Dict:
        """
        Formatea métricas TCT para dashboard
        Similar a generate_health_report del health_analyzer
        """
        
        # 📊 ESTRUCTURA PARA DASHBOARD (como health_analyzer.to_dict())
        dashboard_data = {
            "tct_status": {
                "performance_grade": aggregated_metrics.performance_grade,
                "trend": aggregated_metrics.tct_trend,
                "timestamp": aggregated_metrics.aggregation_timestamp
            },
            "tct_performance": {
                "avg_tct_ms": aggregated_metrics.global_avg_tct_ms,
                "max_tct_ms": aggregated_metrics.global_max_tct_ms,
                "min_tct_ms": aggregated_metrics.global_min_tct_ms,
                "measurements_per_minute": aggregated_metrics.measurements_per_minute
            },
            "tct_timeframes": {},
            "tct_summary": {
                "total_timeframes": aggregated_metrics.total_timeframes,
                "active_sessions": aggregated_metrics.active_sessions,
                "analysis_frequency_hz": aggregated_metrics.analysis_frequency_hz
            }
        }
        
        # 🔄 FORMATEAR DATOS POR TIMEFRAME
        for timeframe, metrics in aggregated_metrics.timeframe_metrics.items():
            dashboard_data["tct_timeframes"][timeframe] = {
                "avg_ms": round(metrics.avg_tct_ms, 2),
                "max_ms": round(metrics.max_tct_ms, 2),
                "measurements": metrics.measurements_taken,
                "patterns": metrics.patterns_analyzed,
                "pois": metrics.pois_processed,
                
                # 🎨 FORMATO VISUAL PARA DASHBOARD
                "status_color": self._get_status_color(metrics.avg_tct_ms),
                "performance_bar": self._get_performance_bar(metrics.avg_tct_ms),
                "trend_arrow": self._get_trend_arrow(aggregated_metrics.tct_trend)
            }
        
        # 📝 CAJA NEGRA - LOG DASHBOARD FORMAT
        enviar_senal_log(
            nivel='DEBUG',
            mensaje=f"📊 DASHBOARD FORMAT | Grade: {aggregated_metrics.performance_grade} | "
                   f"Timeframes: {len(dashboard_data['tct_timeframes'])} | "
                   f"Global Avg: {aggregated_metrics.global_avg_tct_ms:.2f}ms",
            fuente='tct_formatter',
            categoria='tct'
        )
        
        return dashboard_data
    
    def format_for_csv_export(self, aggregated_metrics: AggregatedTCTMetrics) -> str:
        """
        Exporta métricas TCT a CSV
        Utiliza save_adaptive_debug_to_csv como health_analyzer
        """
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tct_metrics_{timestamp}.csv"
        
        # 📊 PREPARAR DATOS PARA CSV
        csv_data = []
        
        # 🌍 FILA DE MÉTRICAS GLOBALES
        global_row = {
            "timestamp": aggregated_metrics.aggregation_timestamp,
            "metric_type": "GLOBAL",
            "timeframe": "ALL",
            "avg_tct_ms": aggregated_metrics.global_avg_tct_ms,
            "max_tct_ms": aggregated_metrics.global_max_tct_ms,
            "min_tct_ms": aggregated_metrics.global_min_tct_ms,
            "measurements_per_minute": aggregated_metrics.measurements_per_minute,
            "frequency_hz": aggregated_metrics.analysis_frequency_hz,
            "performance_grade": aggregated_metrics.performance_grade,
            "trend": aggregated_metrics.tct_trend,
            "total_timeframes": aggregated_metrics.total_timeframes,
            "patterns_analyzed": 0,  # Se calculará sumando
            "pois_processed": 0      # Se calculará sumando
        }
        csv_data.append(global_row)
        
        # 🔄 FILAS POR TIMEFRAME
        total_patterns = 0
        total_pois = 0
        
        for timeframe, metrics in aggregated_metrics.timeframe_metrics.items():
            timeframe_row = {
                "timestamp": aggregated_metrics.aggregation_timestamp,
                "metric_type": "TIMEFRAME",
                "timeframe": timeframe,
                "avg_tct_ms": metrics.avg_tct_ms,
                "max_tct_ms": metrics.max_tct_ms,
                "min_tct_ms": metrics.min_tct_ms,
                "measurements_per_minute": 0,  # No aplica por timeframe
                "frequency_hz": 0,             # No aplica por timeframe  
                "performance_grade": self._calculate_timeframe_grade(metrics.avg_tct_ms),
                "trend": aggregated_metrics.tct_trend,
                "total_timeframes": 1,
                "patterns_analyzed": metrics.patterns_analyzed,
                "pois_processed": metrics.pois_processed
            }
            csv_data.append(timeframe_row)
            
            total_patterns += metrics.patterns_analyzed
            total_pois += metrics.pois_processed
        
        # 🧮 ACTUALIZAR TOTALES EN FILA GLOBAL
        csv_data[0]["patterns_analyzed"] = total_patterns
        csv_data[0]["pois_processed"] = total_pois
        
        # 💾 GUARDAR CSV (usando logging_utils del ICT Engine)
        csv_path = save_adaptive_debug_to_csv(
            data=csv_data,
            filename=filename,
            directory=str(self.exports_dir)
        )
        
        # 📝 CAJA NEGRA - LOG CSV EXPORT
        enviar_senal_log(
            nivel='DEBUG',
            mensaje=f"💾 CSV EXPORT | File: {filename} | Rows: {len(csv_data)} | Path: {csv_path}",
            fuente='tct_formatter',
            categoria='tct'
        )
        
        # 📋 INFO TERMINAL (SILENCIOSO)
        enviar_senal_log(
            nivel='INFO',
            mensaje=f"💾 TCT métricas exportadas - {filename}",
            fuente='tct_formatter',
            categoria='tct'
        )
        
        return str(csv_path)
    
    def format_for_json_export(self, aggregated_metrics: AggregatedTCTMetrics) -> str:
        """Exporta métricas TCT a JSON estructurado"""
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tct_metrics_{timestamp}.json"
        
        # 📊 ESTRUCTURA JSON COMPLETA
        json_data = {
            "export_metadata": {
                "export_timestamp": datetime.datetime.now().isoformat(),
                "export_type": "TCT_METRICS",
                "version": "1.0.0",
                "source": "ICT_Engine_v3.4"
            },
            "aggregated_metrics": aggregated_metrics.to_dict() if hasattr(aggregated_metrics, 'to_dict') else {
                "global_avg_tct_ms": aggregated_metrics.global_avg_tct_ms,
                "global_max_tct_ms": aggregated_metrics.global_max_tct_ms,
                "global_min_tct_ms": aggregated_metrics.global_min_tct_ms,
                "measurements_per_minute": aggregated_metrics.measurements_per_minute,
                "analysis_frequency_hz": aggregated_metrics.analysis_frequency_hz,
                "tct_trend": aggregated_metrics.tct_trend,
                "performance_grade": aggregated_metrics.performance_grade,
                "total_timeframes": aggregated_metrics.total_timeframes,
                "active_sessions": aggregated_metrics.active_sessions,
                "aggregation_timestamp": aggregated_metrics.aggregation_timestamp
            },
            "timeframe_breakdown": {}
        }
        
        # 🔄 AÑADIR BREAKDOWN POR TIMEFRAME
        for timeframe, metrics in aggregated_metrics.timeframe_metrics.items():
            json_data["timeframe_breakdown"][timeframe] = metrics.to_dict()
        
        # 💾 GUARDAR JSON
        json_file = self.exports_dir / filename
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        # 📝 CAJA NEGRA - LOG JSON EXPORT
        enviar_senal_log(
            nivel='DEBUG',
            mensaje=f"📄 JSON EXPORT | File: {filename} | Size: {json_file.stat().st_size} bytes",
            fuente='tct_formatter',
            categoria='tct'
        )
        
        return str(json_file)
    
    def format_console_summary(self, aggregated_metrics: AggregatedTCTMetrics) -> str:
        """
        Genera resumen para consola (como print_health_report del health_analyzer)
        NOTA: Solo para debugging - NO se usa en producción (protocolo Caja Negra)
        """
        
        lines = []
        lines.append("🎯 TCT PIPELINE - RESUMEN DE MEDICIONES")
        lines.append("=" * 60)
        lines.append(f"📅 Timestamp: {aggregated_metrics.aggregation_timestamp}")
        lines.append(f"🎯 Performance Grade: {aggregated_metrics.performance_grade}")
        lines.append(f"📈 Trend: {aggregated_metrics.tct_trend}")
        lines.append("")
        lines.append("📊 MÉTRICAS GLOBALES:")
        lines.append(f"   ⚡ Tiempo promedio: {aggregated_metrics.global_avg_tct_ms:.2f} ms")
        lines.append(f"   📈 Frecuencia: {aggregated_metrics.measurements_per_minute:.2f} med/min")
        lines.append(f"   🔄 Timeframes activos: {aggregated_metrics.total_timeframes}")
        lines.append("")
        lines.append("🔄 BREAKDOWN POR TIMEFRAME:")
        
        for timeframe, metrics in aggregated_metrics.timeframe_metrics.items():
            lines.append(f"   {timeframe}: {metrics.avg_tct_ms:.2f}ms "
                        f"({metrics.measurements_taken} mediciones)")
        
        summary = "\n".join(lines)
        
        # 📝 CAJA NEGRA - LOG CONSOLE SUMMARY
        enviar_senal_log(
            nivel='DEBUG',
            mensaje=f"🖥️ CONSOLE SUMMARY GENERATED | Lines: {len(lines)}",
            fuente='tct_formatter',
            categoria='tct'
        )
        
        return summary
    
    def _get_status_color(self, avg_tct_ms: float) -> str:
        """Determina color de estado para dashboard"""
        if avg_tct_ms <= 100:
            return "green"
        elif avg_tct_ms <= 250:
            return "yellow"
        elif avg_tct_ms <= 500:
            return "orange"
        else:
            return "red"
    
    def _get_performance_bar(self, avg_tct_ms: float) -> str:
        """Genera barra de rendimiento visual"""
        if avg_tct_ms <= 100:
            return "████████████"  # 100%
        elif avg_tct_ms <= 250:
            return "████████░░░░"  # 66%
        elif avg_tct_ms <= 500:
            return "████░░░░░░░░"  # 33%
        else:
            return "██░░░░░░░░░░"  # 16%
    
    def _get_trend_arrow(self, trend: str) -> str:
        """Genera flecha de tendencia"""
        if trend == "IMPROVING":
            return "↗️"
        elif trend == "DEGRADING":
            return "↘️"
        else:
            return "→"
    
    def _calculate_timeframe_grade(self, avg_tct_ms: float) -> str:
        """Calcula grade para timeframe individual"""
        if avg_tct_ms <= 100:
            return "A"
        elif avg_tct_ms <= 250:
            return "B"
        elif avg_tct_ms <= 500:
            return "C"
        elif avg_tct_ms <= 1000:
            return "D"
        else:
            return "F"
