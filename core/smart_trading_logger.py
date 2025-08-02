"""
Sistema Inteligente de Trading Decisions - Cache y Detección de Cambios
======================================================================
Evita logs repetitivos y solo registra cambios significativos en el estado del mercado
"""

import csv
import hashlib
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any  # Optional reservado para futuras extensiones

# MIGRADO A SLUC v2.0 - Reservado para integración con sistema de señales
# from sistema.logging_interface import enviar_senal_log

# =============================================================================
# CACHE INTELIGENTE PARA EVITAR LOGS REPETITIVOS
# =============================================================================

class TradingDecisionCache:
    """Cache inteligente que solo registra cambios significativos"""

    def __init__(self):
        self.last_states = {}
        self.last_log_times = {}
        self.change_threshold = 60  # Segundos mínimos entre logs del mismo tipo
        self.important_threshold = 300  # 5 minutos para eventos importantes

    def should_log_event(self, event_type: str, data: Dict[str, Any],
                        force_important: bool = False) -> bool:
        """Determina si un evento debe ser registrado basado en cambios reales"""

        current_time = datetime.now()

        # Crear hash del estado actual para detectar cambios
        data_hash = self._create_state_hash(data)

        # Obtener el último estado y tiempo para este tipo de evento
        last_hash = self.last_states.get(event_type)
        last_time = self.last_log_times.get(event_type)

        # Si es la primera vez o hay un cambio real en el estado
        if last_hash != data_hash:
            self.last_states[event_type] = data_hash
            self.last_log_times[event_type] = current_time
            return True

        # Si es importante, permitir log cada 5 minutos aunque no haya cambios
        if force_important and last_time:
            time_diff = (current_time - last_time).total_seconds()
            if time_diff >= self.important_threshold:
                self.last_log_times[event_type] = current_time
                return True

        # Si ha pasado suficiente tiempo para eventos normales
        if last_time:
            time_diff = (current_time - last_time).total_seconds()
            if time_diff >= self.change_threshold:
                self.last_log_times[event_type] = current_time
                return True

        return False
    
    def _create_state_hash(self, data: Dict[str, Any]) -> str:
        """Crea un hash del estado actual para detectar cambios"""
        # Convertir el diccionario a string ordenado y crear hash
        state_str = str(sorted(data.items()))
        return hashlib.md5(state_str.encode()).hexdigest()[:8]

# Instancia global del cache
trading_cache = TradingDecisionCache()

# =============================================================================
# LOGGER INTELIGENTE MEJORADO
# =============================================================================

def log_trading_decision_smart(event_type: str, data: Dict[str, Any],
                              level: str = "INFO", force_important: bool = False):
    """
    Logger inteligente que solo registra cambios significativos en decisiones de trading
    """
    # Verificar si realmente debemos loggear este evento
    if not trading_cache.should_log_event(event_type, data, force_important):
        return  # No loggear si no hay cambios significativos

    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_dir = "../data/logs/trading_decisions"
        os.makedirs(log_dir, exist_ok=True)

        date_str = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(log_dir, f"trading_decisions_{date_str}.csv")

        # Formatear el mensaje con los datos relevantes
        if event_type == "DIVERGENCE_ANALYSIS":
            divergence_data = (f"Divergencia: {data.get('type', 'N/A')} | "
                             f"Fuerza: {data.get('strength', 'N/A')} | "
                             f"Precio: {data.get('price', 'N/A')}")
            message = divergence_data
        elif event_type == "CONFLUENCE_CHECK":
            confluence_data = (f"ICT: {data.get('ict_bias', 'N/A')} | "
                             f"POI: {data.get('poi_score', 'N/A')} | "
                             f"Estoc: {data.get('stoch_signal', 'N/A')} | "
                             f"Decisión: {data.get('decision', 'N/A')}")
            message = confluence_data
        elif event_type == "MARKET_CONTEXT_CHANGE":
            context_data = (f"Contexto: {data.get('context', 'N/A')} | "
                          f"Sesión: {data.get('session', 'N/A')} | "
                          f"Bias: {data.get('bias', 'N/A')}")
            message = context_data
        elif event_type == "POI_UPDATE":
            poi_data = (f"POI: {data.get('id', 'N/A')} | "
                       f"Tipo: {data.get('type', 'N/A')} | "
                       f"Score: {data.get('score', 'N/A')} | "
                       f"Calidad: {data.get('quality', 'N/A')}")
            message = poi_data
        else:
            message = str(data)

        # Escribir solo SI hay cambios reales
        with open(log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, event_type, level, message])

    except (ValueError, KeyError, TypeError):
        pass  # Fallar silenciosamente para no romper el sistema

# =============================================================================
# FUNCIONES ESPECÍFICAS PARA DIFERENTES TIPOS DE ANÁLISIS
# =============================================================================

def log_divergence_analysis_smart(divergence_type: str, strength: float,
                                  price: float, timeframe: str = "M15"):
    """Log inteligente para análisis de divergencias - solo cambios reales"""
    data = {
        'type': divergence_type,
        'strength': (round(strength, 2) if isinstance(strength, (int, float))
                    else strength),
        'price': (round(price, 5) if isinstance(price, (int, float))
                 else price),
        'timeframe': timeframe
    }

    # Solo loggear si el tipo de divergencia cambió O si es la primera detección
    log_trading_decision_smart("DIVERGENCE_ANALYSIS", data, "INFO")


def log_confluence_analysis_smart(ict_bias: str, poi_score: float,
                                 stoch_signal: str, decision: str,
                                 current_price: float):
    """Log inteligente para análisis de confluencia - solo decisiones importantes"""
    data = {
        'ict_bias': ict_bias,
        'poi_score': (round(poi_score, 1) if isinstance(poi_score, (int, float))
                     else poi_score),
        'stoch_signal': stoch_signal,
        'decision': decision,
        'price': (round(current_price, 5) if isinstance(current_price, (int, float))
                 else current_price)
    }

    # Marcar como importante si hay una decisión de trading (no ESPERAR)
    is_important = decision not in ["ESPERAR", "NO_TRADE", "NONE"]
    log_trading_decision_smart("CONFLUENCE_CHECK", data, "TRADE_ANALYSIS",
                              force_important=is_important)


def log_market_context_change_smart(context: str, session: str, bias: str,
                                   current_price: float):
    """Log inteligente para cambios de contexto de mercado"""
    data = {
        'context': context,
        'session': session,
        'bias': bias,
        'price': (round(current_price, 5) if isinstance(current_price, (int, float))
                 else current_price)
    }

    log_trading_decision_smart("MARKET_CONTEXT_CHANGE", data, "INFO",
                              force_important=True)

def log_poi_update_smart(poi_id: str, poi_type: str, score: float,
                        quality: str, distance: float):
    """Log inteligente para actualizaciones de POI - solo cambios significativos"""
    data = {
        'id': poi_id,
        'type': poi_type,
        'score': round(score, 1) if isinstance(score, (int, float)) else score,
        'quality': quality,
        'distance': (round(distance, 1) if isinstance(distance, (int, float))
                    else distance)
    }

    # Solo loggear si es un POI de alta calidad o si cambió significativamente
    is_important = quality in ["A+", "A"] or score >= 8.0
    log_trading_decision_smart("POI_UPDATE", data, "INFO",
                              force_important=is_important)


def log_trading_entry_smart(entry_type: str, symbol: str, price: float,
                           volume: float, strategy: str, confidence: float):
    """Log para entradas de trading - SIEMPRE importante"""
    data = {
        'type': entry_type,
        'symbol': symbol,
        'price': round(price, 5) if isinstance(price, (int, float)) else price,
        'volume': volume,
        'strategy': strategy,
        'confidence': (round(confidence, 1) if isinstance(confidence, (int, float))
                      else confidence)
    }

    log_trading_decision_smart("TRADING_ENTRY", data, "TRADE_EXECUTED",
                              force_important=True)

# =============================================================================
# FUNCIONES DE ANÁLISIS Y ESTADÍSTICAS
# =============================================================================

def get_trading_decision_summary(hours: int = 24) -> Dict[str, Any]:
    """Obtiene un resumen de las decisiones de trading de las últimas X horas"""
    try:
        today_str = datetime.now().strftime('%Y-%m-%d')
        log_file = (f"../../data/logs/trading_decisions/"
                   f"trading_decisions_{today_str}.csv")

        if not os.path.exists(log_file):
            return {"error": "No hay archivo de decisiones para hoy"}

        cutoff_time = datetime.now() - timedelta(hours=hours)

        summary = {
            "divergences": 0,
            "confluences": 0,
            "trading_entries": 0,
            "market_changes": 0,
            "poi_updates": 0,
            "last_decision": None,
            "important_events": []
        }

        with open(log_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    timestamp_str, event_type, message = row[0], row[1], row[3]
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

                    if timestamp >= cutoff_time:
                        if event_type == "DIVERGENCE_ANALYSIS":
                            summary["divergences"] += 1
                        elif event_type == "CONFLUENCE_CHECK":
                            summary["confluences"] += 1
                            if "COMPRA" in message or "VENTA" in message:
                                summary["last_decision"] = message
                        elif event_type == "TRADING_ENTRY":
                            summary["trading_entries"] += 1
                            summary["important_events"].append(
                                f"{timestamp_str}: {message}")
                        elif event_type == "MARKET_CONTEXT_CHANGE":
                            summary["market_changes"] += 1
                        elif event_type == "POI_UPDATE":
                            summary["poi_updates"] += 1

                except (ValueError, IndexError):
                    continue

        return summary

    except (ValueError, KeyError, TypeError) as e:
        return {"error": f"Error analizando decisiones: {e}"}

def cleanup_old_decision_logs(days_to_keep: int = 7):
    """Limpia logs antiguos de decisiones de trading"""
    try:
        log_dir = Path("../data/logs/trading_decisions")
        if not log_dir.exists():
            return

        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        for log_file in log_dir.glob("trading_decisions_*.csv"):
            try:
                # Extraer fecha del nombre del archivo
                date_str = log_file.stem.split("_")[-1]
                file_date = datetime.strptime(date_str, "%Y-%m-%d")

                if file_date < cutoff_date:
                    log_file.unlink()

            except (ValueError, OSError):
                continue

    except (OSError, PermissionError):
        pass
