"""
🎯 SISTEMA DE LOGGING UNIFICADO CENTINELA (SLUC v2.0)
====================================================

Sistema de Señales de Logging Centralizado - La única puerta de entrada para TODO el logging.

FILOSOFÍA:
- Los módulos envían "señales" con información
- El SLUC decide cómo, dónde y cuándo registrar
- Separación total entre "emisión" y "procesamiento"

CARACTERÍSTICAS ABSORBIDAS:
- StreamInterceptor (data_logger.py)
- JSON Formatting (smart_logger.py)
- Singleton Pattern (smart_logger.py)
- Intelligent Change Detection (universal_intelligent_logger.py)
- Thread-safe Operations
- Emoji-safe Windows compatibility

AUTOR: SLUC v2.0 - Sistema Consolidado
FECHA: 27 Julio 2025
"""

import logging
import json
from json import JSONDecodeError
import hashlib
import threading
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Imports del sistema existente (para absorber funcionalidades)
from sistema.logging_config import (
    setup_logging, get_specialized_logger,
    log_structured_event, log_account_metrics, log_trading_metrics, log_system_metrics
    # log_poi_structured, log_pattern_structured, log_trade_structured,
    # log_market_context_structured reservados para futuras extensiones
)

def safe_utf8_format(message: str) -> str:
    """
    🌐 PROTOCOLO UTF-8 SEGURO PARA EMOJIS - VERSIÓN MEJORADA

    Protege contra UnicodeEncodeError manteniendo emojis cuando es posible.
    Implementa múltiples estrategias de fallback para máxima compatibilidad.

    Args:
        message: Mensaje original (puede contener emojis)

    Returns:
        str: Mensaje seguro para logging en Windows
    """
    if not message:
        return ""

    try:
        # Estrategia 1: Intentar encoding/decoding UTF-8 completo
        encoded = message.encode('utf-8', 'strict')
        decoded = encoded.decode('utf-8', 'strict')
        return decoded

    except UnicodeEncodeError:
        try:
            # Estrategia 2: Reemplazar caracteres problemáticos pero mantener algunos emojis comunes
            safe_message = message

            # Mapeo de emojis problemáticos a alternativas seguras
            emoji_replacements = {
                '🎯': '[TARGET]',
                '🚀': '[ROCKET]',
                '✅': '[CHECK]',
                '❌': '[CROSS]',
                '⚠️': '[WARNING]',
                '🔍': '[SEARCH]',
                '📊': '[CHART]',
                '🎲': '[DICE]',
                '🧠': '[BRAIN]',
                '🚚': '[TRUCK]',
                '🏆': '[TROPHY]',
                '💰': '[MONEY]',
                '📈': '[TRENDING_UP]',
                '📉': '[TRENDING_DOWN]',
                '🔥': '[FIRE]',
                '⭐': '[STAR]',
                '🌟': '[STAR2]',
                '⏰': '[CLOCK]',
                '🎪': '[CIRCUS]',
                '🌐': '[GLOBE]',
                '🛡️': '[SHIELD]',
                '🔧': '[WRENCH]',
                '⚡': '[ZAP]',
                '💡': '[BULB]',
                '🎮': '[GAME]'
            }

            for emoji, replacement in emoji_replacements.items():
                safe_message = safe_message.replace(emoji, replacement)

            # Probar el mensaje modificado
            safe_message.encode('utf-8', 'strict')
            return safe_message

        except UnicodeEncodeError:
            # Estrategia 3: Fallback a ASCII con marcadores de posición
            try:
                ascii_safe = message.encode('ascii', 'ignore').decode('ascii')
                if len(ascii_safe) < len(message):
                    ascii_safe += f" [EMOJI_CONTENT_{len(message)-len(ascii_safe)}_CHARS]"
                return ascii_safe
            except (UnicodeError, ValueError):
                pass

    except (UnicodeError, ValueError, AttributeError):
        pass

    # Estrategia 4: Último fallback - mensaje genérico pero informativo
    try:
        char_count = len(message)
        first_10_chars = message[:10].encode('ascii', 'ignore').decode('ascii')
        return f"[MSG_{char_count}chars_START_{first_10_chars}]"
    except (UnicodeError, ValueError, AttributeError):
        return "[LOGGING_UNICODE_ERROR]"
from sistema.emoji_logger import EmojiSafeLogger

class SentinelLoggingUnifiedController:
    """
    🎯 CONTROLADOR UNIFICADO - Absorbe TODA la inteligencia de logging

    CARACTERÍSTICAS CONSOLIDADAS:
    - Singleton pattern (smart_logger.py)
    - Emoji-safe logging (emoji_logger.py)
    - JSON structured logging (smart_logger.py)
    - Change detection (universal_intelligent_logger.py)
    - Stream interception (data_logger.py)
    - Thread-safe operations
    """

    _instance = None
    _lock = threading.Lock()
    _state_cache = {}  # Para detección de cambios inteligente

    def __new__(cls):
        """Patrón Singleton absorbido de smart_logger.py"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializar el SLUC una sola vez"""
        if hasattr(self, '_initialized'):
            return

        # 📝 ARQUITECTURA: Inicializar atributos críticos antes de setup
        self.change_thresholds = {}  # Para detección de cambios inteligente
        self.json_handler = None     # Handler JSON estructurado
        self.capture_enabled = False # Estado del stream interceptor
        self.capture_file_path = ""  # Ruta de captura de streams

        self._initialized = True
        self._setup_unified_system()

    def _setup_unified_system(self):
        """Configurar el sistema unificado completo"""

        # 1. Inicializar sistema base existente
        setup_logging()

        # 2. Configurar thresholds de cambio inteligente (de universal_intelligent_logger.py)
        self.change_thresholds = {
            'trading': 0.03,       # 3% cambio para trading (muy sensible)
            'ict': 0.04,           # 4% cambio para ICT
            'poi': 0.05,           # 5% cambio para POI
            'mt5': 0.02,           # 2% cambio para MT5 (crítico)
            'dashboard': 0.08,     # 8% cambio para Dashboard
            'sistema': 0.02,       # 2% cambio para Sistema
            'general': 0.05,       # 5% por defecto
            'acc': 0.03            # 3% cambio para ACC (muy sensible)
        }

        # 3. Configurar logger JSON estructurado (de smart_logger.py)
        self._setup_json_logger()

        # 4. Configurar interceptor de streams (de data_logger.py)
        self._setup_stream_interceptor()

        # 5. Log inicial del sistema unificado
        self.enviar_senal_log(
            nivel='INFO',
            mensaje='🚀 SISTEMA DE LOGGING UNIFICADO CENTINELA (SLUC v2.0) INICIADO',
            emisor='SLUC_CORE',
            categoria='sistema',
            metadata={
                'version': '2.0',
                'features': ['emoji_safe', 'json_structured', 'change_detection', 'stream_interception'],
                'consolidated_from': ['data_logger', 'smart_logger', 'universal_intelligent_logger', 'emoji_logger']
            }
        )

    def _setup_json_logger(self):
        """Configurar logging JSON estructurado (absorbido de smart_logger.py)"""
        try:
            # Crear handler JSONL para análisis automático
            log_dir = Path(__file__).parent.parent / "data" / "logs" / "structured"
            log_dir.mkdir(parents=True, exist_ok=True)

            jsonl_file = log_dir / "sentinel_events.jsonl"

            # Configurar handler JSON personalizado
            self.json_handler = logging.FileHandler(jsonl_file, encoding='utf-8')
            self.json_handler.setLevel(logging.INFO)

            # Formatter JSON personalizado
            class SentinelJSONFormatter(logging.Formatter):
                def format(self, record):
                    log_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'level': record.levelname,
                        'category': getattr(record, 'category', 'general'),
                        'emisor': getattr(record, 'emisor', 'unknown'),
                        'message': record.getMessage(),
                        'metadata': getattr(record, 'metadata', {})
                    }
                    return json.dumps(log_entry, ensure_ascii=False)

            self.json_handler.setFormatter(SentinelJSONFormatter())

            # Agregar a logger raíz
            logging.getLogger().addHandler(self.json_handler)

        except (JSONDecodeError, ValueError) as e:
            # 🔇 OPERACIÓN LIMPIEZA: Error silencioso en configuración JSON
            logging.getLogger('SLUC_INIT').error("Error configurando JSON logger: %s", e)

    def _setup_stream_interceptor(self):
        """Configurar interceptor de streams (absorbido de data_logger.py)"""
        try:
            # Opcional: Interceptar stdout para captura completa
            # Solo si no está ya interceptado
            if not hasattr(sys.stdout, 'log_file'):
                log_dir = Path(__file__).parent.parent / "data" / "logs" / "terminal_capture"
                log_dir.mkdir(parents=True, exist_ok=True)

                date_str = datetime.now().strftime("%Y-%m-%d")
                capture_file = log_dir / f"full_output_{date_str}.log"

                # Configuración básica de interceptor
                self.capture_enabled = True
                self.capture_file_path = capture_file

        except (JSONDecodeError, ValueError) as e:
            # 🔇 OPERACIÓN LIMPIEZA: Error silencioso en stream interceptor
            logging.getLogger('SLUC_INIT').error("Error configurando stream interceptor: %s", e)

    def _calculate_content_hash(self, data: Dict[str, Any]) -> str:
        """
        Calcular hash de contenido para detección inteligente de cambios
        (Absorbido de universal_intelligent_logger.py)
        """
        content_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(content_str.encode()).hexdigest()

    def _should_log_change(self, categoria: str, content_hash: str) -> bool:
        """
        Determinar si un cambio es significativo usando thresholds inteligentes
        (Lógica absorbida y mejorada de universal_intelligent_logger.py)
        """
        if categoria not in self._state_cache:
            self._state_cache[categoria] = content_hash
            return True  # Primera vez, siempre registrar

        if self._state_cache[categoria] != content_hash:
            self._state_cache[categoria] = content_hash
            return True  # Contenido cambió, registrar

        return False  # Sin cambios significativos

    def enviar_senal_log(self,
                        nivel: str,
                        mensaje: str,
                        emisor: str,
                        categoria: str = 'general',
                        metadata: Optional[Dict[str, Any]] = None,
                        force_log: bool = False,
                        # 🌟 NUEVOS PARÁMETROS PARA LOGGING ESTRUCTURADO
                        estructurado: bool = False,
                        evento_tipo: Optional[str] = None,
                        metrica_csv: Optional[str] = None,
                        metrica_tipo: Optional[str] = None) -> None:
        """
        🎯 FUNCIÓN PRINCIPAL: Enviar señal de log al SLUC

        Esta es la ÚNICA forma de registrar logs en todo el sistema.
        Ahora con soporte completo para logging estructurado.

        Args:
            nivel: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
            mensaje: Texto del mensaje (emoji-safe)
            emisor: __name__ del módulo emisor
            categoria: 'trading', 'ict', 'poi', 'mt5', 'dashboard', 'sistema', 'general', 'acc'
            metadata: Datos estructurados adicionales
            force_log: Forzar logging aunque no haya cambios significativos
            estructurado: Si True, también registra en formato JSONL estructurado
            evento_tipo: Tipo de evento para logging estructurado
            metrica_csv: String CSV para registrar en métricas
            metrica_tipo: Tipo de métrica ('account', 'trading', 'system')
        """
        try:
            # 1. Validar entrada
            if not mensaje or not emisor:
                return

            # 2. Preparar metadata
            metadata = metadata or {}

            # 3. Detección inteligente de cambios (si hay metadata)
            if metadata and not force_log:
                content_hash = self._calculate_content_hash(metadata)
                cache_key = f"{categoria}_{emisor}"

                if not self._should_log_change(cache_key, content_hash):
                    return  # No hay cambios significativos, no registrar

            # 4. Obtener logger especializado
            logger = get_specialized_logger(categoria) if categoria != 'general' else logging.getLogger()

            # 5. Crear EmojiSafeLogger para compatibilidad Windows
            emoji_safe_logger = EmojiSafeLogger(logger)

            # 6. Preparar mensaje formateado con protección UTF-8
            mensaje_seguro = safe_utf8_format(mensaje)
            mensaje_formateado = f"[{emisor}] {mensaje_seguro}"

            # 7. Preparar extra data para JSON logging
            extra_data = {
                'category': categoria,
                'emisor': emisor,
                'metadata': metadata
            }

            # 8. Enviar según nivel
            nivel_upper = nivel.upper()
            if nivel_upper == 'DEBUG':
                emoji_safe_logger.debug(mensaje_formateado, extra=extra_data)
            elif nivel_upper == 'INFO':
                emoji_safe_logger.info(mensaje_formateado, extra=extra_data)
            elif nivel_upper == 'WARNING':
                emoji_safe_logger.warning(mensaje_formateado, extra=extra_data)
            elif nivel_upper == 'ERROR':
                emoji_safe_logger.error(mensaje_formateado, extra=extra_data)
            elif nivel_upper == 'CRITICAL':
                emoji_safe_logger.critical(mensaje_formateado, extra=extra_data)
            else:
                emoji_safe_logger.info(mensaje_formateado, extra=extra_data)

            # 🌟 NUEVO: LOGGING ESTRUCTURADO
            if estructurado and metadata:
                # Usar evento_tipo o inferir del categoria
                tipo_evento = evento_tipo or f"{categoria}_event"
                log_structured_event(tipo_evento, metadata, emisor, categoria)

            # 🌟 NUEVO: MÉTRICAS CSV
            if metrica_csv and metrica_tipo:
                if metrica_tipo == 'account':
                    # metrica_csv debe ser: "balance,equity,profit,margin,free_margin,positions_count"
                    valores = metrica_csv.split(',')
                    if len(valores) >= 3:
                        balance = float(valores[0]) if valores[0] else 0.0
                        equity = float(valores[1]) if valores[1] else 0.0
                        profit = float(valores[2]) if valores[2] else 0.0
                        margin = float(valores[3]) if len(valores) > 3 and valores[3] else 0.0
                        free_margin = float(valores[4]) if len(valores) > 4 and valores[4] else 0.0
                        positions_count = int(valores[5]) if len(valores) > 5 and valores[5] else 0
                        log_account_metrics(balance, equity, profit, margin, free_margin, positions_count)

                elif metrica_tipo == 'trading':
                    # metrica_csv debe ser: "symbol,action,volume,price,profit,balance_after,equity_after"
                    valores = metrica_csv.split(',')
                    if len(valores) >= 7:
                        symbol = valores[0]
                        action = valores[1]
                        volume = float(valores[2]) if valores[2] else 0.0
                        price = float(valores[3]) if valores[3] else 0.0
                        profit = float(valores[4]) if valores[4] else 0.0
                        balance_after = float(valores[5]) if valores[5] else 0.0
                        equity_after = float(valores[6]) if valores[6] else 0.0
                        log_trading_metrics(symbol, action, volume, price, profit, balance_after, equity_after)

                elif metrica_tipo == 'system':
                    # metrica_csv debe ser: "cpu_percent,memory_percent,latency_ms,active_positions,mt5_connected,dashboard_connected"
                    valores = metrica_csv.split(',')
                    if len(valores) >= 6:
                        cpu_percent = float(valores[0]) if valores[0] else 0.0
                        memory_percent = float(valores[1]) if valores[1] else 0.0
                        latency_ms = float(valores[2]) if valores[2] else 0.0
                        active_positions = int(valores[3]) if valores[3] else 0
                        mt5_connected = bool(int(valores[4])) if valores[4] else False
                        dashboard_connected = bool(int(valores[5])) if valores[5] else False
                        log_system_metrics(cpu_percent, memory_percent, latency_ms, active_positions, mt5_connected, dashboard_connected)

        except (JSONDecodeError, ValueError) as e:
            # Fallback seguro - logging silencioso en caso de error
            # 🔇 OPERACIÓN LIMPIEZA: Sin prints, usar logging crítico
            logger = logging.getLogger('SLUC_ERROR')

            # 🌐 PROTOCOLO UTF-8 SEGURO PARA EMOJIS
            mensaje_seguro = safe_utf8_format(mensaje)
            try:
                # Intentar log normal
                logger.critical("SLUC ERROR: %s | Mensaje original: %s", e, mensaje_seguro)
            except (UnicodeError, ValueError, OSError, IOError):
                # Último fallback: mensaje genérico
                logger.critical("SLUC ERROR: %s | Mensaje original: [Unicode Error]", e)

# =============================================================================
# INSTANCIA GLOBAL SINGLETON DEL SLUC
# =============================================================================

# Crear instancia global
_sluc_instance = SentinelLoggingUnifiedController()

def enviar_senal_log(nivel: Optional[str] = None,
                    mensaje: Optional[str] = None,
                    emisor: Optional[str] = None,
                    categoria: str = 'general',
                    metadata: Optional[Dict[str, Any]] = None,
                    force_log: bool = False,
                    # 🌟 NUEVOS PARÁMETROS PARA LOGGING ESTRUCTURADO
                    estructurado: bool = False,
                    evento_tipo: Optional[str] = None,
                    metrica_csv: Optional[str] = None,
                    metrica_tipo: Optional[str] = None,
                    # 🛡️ PROTOCOLO UNIFICACIÓN DE COMANDO - SOPORTE KWARGS
                    **kwargs) -> None:
    """
    🎯 FUNCIÓN GLOBAL: Puerta de entrada única para TODO el logging del sistema

    Reemplaza TODAS las llamadas a logger.info(), logger.debug(), etc.
    Ahora con soporte completo para logging estructurado.

    🛡️ PROTOCOLO UNIFICACIÓN DE COMANDO:
    - Acepta argumentos posicionales (legacy): enviar_senal_log('INFO', 'mensaje', 'emisor', 'categoria')
    - Acepta argumentos nombrados (nuevo): enviar_senal_log(level='INFO', message='mensaje', emisor='emisor')
    - Soporte para kwargs adicionales para máxima flexibilidad
    """

    # 🛡️ MANEJO DE ARGUMENTOS LEGACY CON NOMBRES ALTERNATIVOS
    if 'level' in kwargs:
        nivel = kwargs.pop('level')
    if 'message' in kwargs:
        mensaje = kwargs.pop('message')
    if 'emisor' not in locals() or emisor is None:
        if 'emisor' in kwargs:
            emisor = kwargs.pop('emisor')
    if 'categoria' not in locals() or categoria == 'general':
        if 'categoria' in kwargs:
            categoria = kwargs.pop('categoria')

    # 🔒 VALIDACIONES OBLIGATORIAS
    if not nivel or not mensaje or not emisor:
        logger = logging.getLogger('SLUC_ERROR')
        logger.critical("SLUC ERROR: Parámetros obligatorios faltantes | nivel=%s | mensaje=%s | emisor=%s", nivel, mensaje, emisor)
        return

    # 🎯 DELEGACIÓN AL SLUC INSTANCE
    return _sluc_instance.enviar_senal_log(
        nivel, mensaje, emisor, categoria, metadata, force_log,
        estructurado, evento_tipo, metrica_csv, metrica_tipo
    )

# =============================================================================
# FUNCIONES DE CONVENIENCIA PARA MIGRACIÓN GRADUAL
# =============================================================================

def log_info(mensaje: str, emisor: str, categoria: str = 'general', metadata: Optional[Dict[str, Any]] = None):
    """Conveniencia para logs INFO"""
    enviar_senal_log('INFO', mensaje, emisor, categoria, metadata)

def log_debug(mensaje: str, emisor: str, categoria: str = 'general', metadata: Optional[Dict[str, Any]] = None):
    """Conveniencia para logs DEBUG"""
    enviar_senal_log('DEBUG', mensaje, emisor, categoria, metadata)

def log_warning(mensaje: str, emisor: str, categoria: str = 'general', metadata: Optional[Dict[str, Any]] = None):
    """Conveniencia para logs WARNING"""
    enviar_senal_log('WARNING', mensaje, emisor, categoria, metadata)

def log_error(mensaje: str, emisor: str, categoria: str = 'general', metadata: Optional[Dict[str, Any]] = None):
    """Conveniencia para logs ERROR"""
    enviar_senal_log('ERROR', mensaje, emisor, categoria, metadata)

def log_trading_decision(decision: str, price: float, symbol: str, metadata: Optional[Dict[str, Any]] = None):
    """Logging especializado para decisiones de trading"""
    full_metadata = {
        'decision': decision,
        'price': price,
        'symbol': symbol,
        **(metadata or {})
    }
    enviar_senal_log('INFO', f"DECISIÓN: {decision} {symbol} @ {price}", 'trading_system', 'trading', full_metadata)

def log_ict_pattern(pattern_type: str, confidence: float, timeframe: str, metadata: Optional[Dict[str, Any]] = None):
    """Logging especializado para patrones ICT"""
    full_metadata = {
        'pattern_type': pattern_type,
        'confidence': confidence,
        'timeframe': timeframe,
        **(metadata or {})
    }
    enviar_senal_log('INFO', f"PATRÓN ICT: {pattern_type} | Confianza: {confidence:.2f} | TF: {timeframe}", 'ict_engine', 'ict', full_metadata)

def log_poi_detection(poi_type: str, price: float, score: float, metadata: Optional[Dict[str, Any]] = None):
    """Logging especializado para detección de POIs"""
    full_metadata = {
        'poi_type': poi_type,
        'price': price,
        'score': score,
        **(metadata or {})
    }
    enviar_senal_log('INFO', f"POI DETECTADO: {poi_type} @ {price:.5f} | Score: {score:.2f}", 'poi_system', 'poi', full_metadata)

# =============================================================================
# 🌟 FUNCIONES DE CONVENIENCIA PARA LOGGING ESTRUCTURADO
# =============================================================================

def log_poi_event(poi_data: Dict[str, Any], mensaje: str = "POI detectado", emisor: str = "poi_detector"):
    """
    Función de conveniencia para registrar detección de POI en formato estructurado.

    Args:
        poi_data: Diccionario completo del POI
        mensaje: Mensaje descriptivo
        emisor: Módulo emisor
    """
    enviar_senal_log(
        nivel='INFO',
        mensaje=mensaje,
        emisor=emisor,
        categoria='poi',
        metadata=poi_data,
        estructurado=True,
        evento_tipo='poi_detected'
    )

def log_pattern_event(pattern_data: Dict[str, Any], mensaje: str = "Patrón ICT detectado", emisor: str = "ict_analyzer"):
    """
    Función de conveniencia para registrar detección de patrón ICT en formato estructurado.

    Args:
        pattern_data: Diccionario completo del patrón
        mensaje: Mensaje descriptivo
        emisor: Módulo emisor
    """
    enviar_senal_log(
        nivel='INFO',
        mensaje=mensaje,
        emisor=emisor,
        categoria='ict',
        metadata=pattern_data,
        estructurado=True,
        evento_tipo='ict_pattern_detected'
    )

def log_trade_event(trade_data: Dict[str, Any], mensaje: str = "Trade ejecutado", emisor: str = "trading_engine"):
    """
    Función de conveniencia para registrar ejecución de trade en formato estructurado.

    Args:
        trade_data: Diccionario completo del trade
        mensaje: Mensaje descriptivo
        emisor: Módulo emisor
    """
    enviar_senal_log(
        nivel='INFO',
        mensaje=mensaje,
        emisor=emisor,
        categoria='trading',
        metadata=trade_data,
        estructurado=True,
        evento_tipo='trade_executed'
    )

def log_account_snapshot(balance: float, equity: float, profit: float, margin: float = 0.0,
                        free_margin: float = 0.0, positions_count: int = 0, emisor: str = "account_monitor"):
    """
    Función de conveniencia para registrar snapshot de cuenta en CSV.

    Args:
        balance: Balance actual
        equity: Equity actual
        profit: Profit/Loss actual
        margin: Margen usado
        free_margin: Margen libre
        positions_count: Número de posiciones abiertas
        emisor: Módulo emisor
    """
    metrica_csv = f"{balance},{equity},{profit},{margin},{free_margin},{positions_count}"
    enviar_senal_log(
        nivel='INFO',
        mensaje=f"Account metrics: Balance={balance}, Equity={equity}, P&L={profit}",
        emisor=emisor,
        categoria='trading',
        metrica_csv=metrica_csv,
        metrica_tipo='account'
    )

def log_system_snapshot(cpu_percent: float, memory_percent: float, latency_ms: float,
                       active_positions: int, mt5_connected: bool, dashboard_connected: bool,
                       emisor: str = "system_monitor"):
    """
    Función de conveniencia para registrar snapshot del sistema en CSV.

    Args:
        cpu_percent: Porcentaje de CPU usado
        memory_percent: Porcentaje de memoria usado
        latency_ms: Latencia en millisegundos
        active_positions: Posiciones activas
        mt5_connected: Estado de conexión MT5
        dashboard_connected: Estado de conexión dashboard
        emisor: Módulo emisor
    """
    mt5_status = 1 if mt5_connected else 0
    dashboard_status = 1 if dashboard_connected else 0
    metrica_csv = f"{cpu_percent},{memory_percent},{latency_ms},{active_positions},{mt5_status},{dashboard_status}"
    enviar_senal_log(
        nivel='INFO',
        mensaje=f"System metrics: CPU={cpu_percent}%, Mem={memory_percent}%, Latency={latency_ms}ms",
        emisor=emisor,
        categoria='sistema',
        metrica_csv=metrica_csv,
        metrica_tipo='system'
    )

def force_log_and_print(mensaje, nivel='INFO', emisor='SYSTEM'):
    """
    Función para forzar el logging y la impresión de un mensaje.
    Compatible con el dashboard y sistemas que requieren logging inmediato.

    Args:
        mensaje: Mensaje a enviar
        nivel: Nivel de logging (INFO, ERROR, WARNING, DEBUG)
        emisor: Módulo emisor del mensaje
    """
    # Enviar al sistema de logging
    enviar_senal_log(
        nivel=nivel,
        mensaje=mensaje,
        emisor=emisor,
        categoria='forced_log'
    )

    # 🔇 OPERACIÓN LIMPIEZA: Sin prints en función force_log_and_print
    logger = logging.getLogger('FORCED_LOG')
    logger.critical("[%s] %s: %s", nivel, emisor, mensaje)

    return True
