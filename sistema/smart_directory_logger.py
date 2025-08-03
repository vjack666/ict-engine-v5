from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
"""
SISTEMA DE LOGGING INTELIGENTE CON DIRECTORIOS ORGANIZADOS
=========================================================

Sistema que mantiene el orden existente de subcarpetas en data/logs/
y deposita cada log en la carpeta correcta según su función.

ESTRUCTURA RESPETADA:
- data/logs/daily/
- data/logs/dashboard/
- data/logs/debug/
- data/logs/errors/
- data/logs/ict/
- data/logs/metrics/
- data/logs/mt5/
- data/logs/poi/
- data/logs/structured/
- data/logs/tct/
- data/logs/terminal_capture/
- data/logs/trading/

FILOSOFÍA:
- Cada módulo deposita automáticamente en SU carpeta
- Sin emojis en logs de archivos (profesional)
- Terminal silencioso en producción
- Dashboard mantiene emojis para UX

AUTOR: Sistema Inteligente de Directorios v2.1
FECHA: 02 Agosto 2025
"""

import logging
import json
import os
import re
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from logging.handlers import RotatingFileHandler

class SmartDirectoryMapper:
    """
    Mapea automáticamente cada tipo de log a su directorio correcto.
    """

    def __init__(self):
        self.base_log_dir = Path("data/logs")
        self.directory_mapping = self._create_directory_mapping()
        self.ensure_directories_exist()

    def _create_directory_mapping(self) -> Dict[str, List[str]]:
        """
        Mapea palabras clave y fuentes a directorios específicos.
        """
        return {
            # Directorios por función
            'daily': ['daily', 'runtime', 'sentinel_runtime', 'diario'],
            'dashboard': ['dashboard', 'widget', 'ui', 'interface', 'panel'],
            'debug': ['debug', 'trace', 'diagnostic', 'troubleshoot'],
            'errors': ['error', 'exception', 'critical', 'failure', 'crash'],
            'ict': ['ict', 'pattern', 'structure', 'analysis', 'detector'],
            'metrics': ['metric', 'performance', 'stats', 'measurement', 'account'],
            'mt5': ['mt5', 'metatrader', 'broker', 'connection', 'tick'],
            'poi': ['poi', 'point_of_interest', 'zone', 'level'],
            'structured': ['structured', 'event', 'json', 'formatted'],
            'tct': ['tct', 'pipeline', 'time_cycle'],
            'terminal_capture': ['terminal', 'console', 'stdout', 'stderr'],
            'trading': ['trading', 'trade', 'order', 'position', 'execution']
        }

    def get_directory_for_log(self, source: str, category: str, message: str) -> str:
        """
        Determina inteligentemente en qué directorio debe ir el log.

        Args:
            source: Fuente del log (ej: 'core.trading')
            category: Categoría del log (ej: 'trading')
            message: Mensaje del log

        Returns:
            Nombre del directorio donde debe ir el log
        """
        # Buscar coincidencias en orden de prioridad
        search_terms = [
            source.lower(),
            category.lower(),
            message.lower()[:100]  # Solo primeros 100 chars del mensaje
        ]

        # Contar coincidencias por directorio
        directory_scores = {}

        for directory, keywords in self.directory_mapping.items():
            score = 0
            for search_term in search_terms:
                for keyword in keywords:
                    if keyword in search_term:
                        # Peso diferente según dónde se encuentre
                        if keyword in source.lower():
                            score += 3  # Fuente tiene más peso
                        elif keyword in category.lower():
                            score += 2  # Categoría tiene peso medio
                        else:
                            score += 1  # Mensaje tiene menos peso

            if score > 0:
                directory_scores[directory] = score

        # Retornar el directorio con mayor score
        if directory_scores:
            best_directory = max(directory_scores.keys(), key=lambda k: directory_scores[k])
            return best_directory

        # Fallback: usar 'debug' si no hay coincidencias claras
        return 'debug'

    def ensure_directories_exist(self):
        """Asegura que todos los directorios existan."""
        for directory in self.directory_mapping.keys():
            dir_path = self.base_log_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)

class ProfessionalLogFormatter(logging.Formatter):
    """
    Formateador que limpia emojis para logs profesionales.
    """

    def __init__(self):
        fmt = "%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s"
        super().__init__(fmt, datefmt="%Y-%m-%d %H:%M:%S")

        # Mapeo de emojis a texto profesional
        self.emoji_to_text = {
            '🎯': '[TARGET]', '🚀': '[LAUNCH]', '✅': '[SUCCESS]', '❌': '[FAILED]',
            '⚠️': '[WARNING]', '🔍': '[SEARCH]', '📊': '[ANALYTICS]', '💰': '[FINANCIAL]',
            '📈': '[BULLISH]', '📉': '[BEARISH]', '🔥': '[ACTIVE]', '⭐': '[IMPORTANT]',
            '🌟': '[CRITICAL]', '⏰': '[TIMER]', '🎪': '[EVENT]', '🌐': '[NETWORK]',
            '🛡️': '[SECURITY]', '🔧': '[MAINTENANCE]', '📡': '[SIGNAL]', '💎': '[PREMIUM]',
            '🧠': '[AI]', '🎲': '[RANDOM]', '🏆': '[ACHIEVEMENT]', '🎵': '[AUDIO]'
        }

    def format(self, record):
        """Formatea el registro removiendo emojis."""
        formatted = super().format(record)
        return self._clean_emojis(formatted)

    def _clean_emojis(self, text: str) -> str:
        """Limpia emojis del texto."""
        if not text:
            return ""

        # Reemplazar emojis conocidos
        cleaned = text
        for emoji, replacement in self.emoji_to_text.items():
            cleaned = cleaned.replace(emoji, replacement)

        # Remover emojis restantes con regex
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002700-\U000027BF"  # dingbats
            "\U0001f926-\U0001f937"  # additional emoticons
            "\U00010000-\U0010ffff"  # supplementary multilingual plane
            "\u2640-\u2642"          # gender symbols
            "\u2600-\u2B55"          # misc symbols
            "\u200d"                 # zero width joiner
            "\ufe0f"                 # variation selector
            "]+",
            flags=re.UNICODE
        )

        cleaned = emoji_pattern.sub('[SYMBOL]', cleaned)
        return cleaned

class SmartDirectoryLogger:
    """
    Logger inteligente que deposita automáticamente cada log en su directorio correcto.
    """

    def __init__(self):
        self.directory_mapper = SmartDirectoryMapper()
        self.formatter = ProfessionalLogFormatter()
        self.loggers_cache = {}
        self.lock = threading.Lock()
        self.stats = {
            'logs_by_directory': {},
            'total_logs': 0
        }

        # Configurar operación silenciosa
        self.silent_mode = os.getenv('SENTINEL_ENVIRONMENT', '').upper() == 'PRODUCTION'

    def get_logger_for_directory(self, directory: str, source: str) -> logging.Logger:
        """
        Obtiene o crea un logger específico para un directorio.
        """
        cache_key = f"{directory}_{source}"

        with self.lock:
            if cache_key in self.loggers_cache:
                return self.loggers_cache[cache_key]

            # Crear logger único
            logger = logging.getLogger(f"SMART.{directory.upper()}.{source.upper()}")
            logger.setLevel(logging.DEBUG)

            # Remover handlers existentes
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

            # Crear archivo de log en el directorio correspondiente
            log_file = self.directory_mapper.base_log_dir / directory / f"{directory}_{datetime.now().strftime('%Y%m%d')}.log"

            # Handler con rotación
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(logging.DEBUG)

            logger.addHandler(file_handler)

            # No agregar handler de consola si estamos en modo silencioso
            if not self.silent_mode:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(self.formatter)
                console_handler.setLevel(logging.WARNING)  # Solo warnings+ en consola
                logger.addHandler(console_handler)

            # Prevenir propagación para evitar duplicados
            logger.propagate = False

            self.loggers_cache[cache_key] = logger
            return logger

    def smart_log(self, level: str, message: str, source: str,
                  category: str = 'general', metadata: Optional[Dict] = None):
        """
        Registra un log automáticamente en el directorio correcto.

        Args:
            level: Nivel del log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message: Mensaje a registrar
            source: Fuente del log (ej: 'core.trading')
            category: Categoría del log (ej: 'trading')
            metadata: Metadatos adicionales
        """
        try:
            # Determinar directorio automáticamente
            directory = self.directory_mapper.get_directory_for_log(source, category, message)

            # Obtener logger para ese directorio
            logger = self.get_logger_for_directory(directory, source)

            # Formatear mensaje con metadatos si existen
            formatted_message = self._format_message_with_metadata(message, metadata)

            # Registrar según el nivel
            level_upper = level.upper()
            if level_upper == 'DEBUG':
                logger.debug(formatted_message)
            elif level_upper == 'INFO':
                logger.info(formatted_message)
            elif level_upper == 'WARNING':
                logger.warning(formatted_message)
            elif level_upper == 'ERROR':
                logger.error(formatted_message)
            elif level_upper == 'CRITICAL':
                logger.critical(formatted_message)
            else:
                logger.info(formatted_message)

            # Actualizar estadísticas
            with self.lock:
                self.stats['total_logs'] += 1
                if directory not in self.stats['logs_by_directory']:
                    self.stats['logs_by_directory'][directory] = 0
                self.stats['logs_by_directory'][directory] += 1

        except Exception as e:
            # Log de emergencia en debug
            emergency_logger = logging.getLogger('EMERGENCY')
            emergency_logger.error(f"SmartDirectoryLogger error: {e}")

    def _format_message_with_metadata(self, message: str, metadata: Optional[Dict]) -> str:
        """Formatea el mensaje incluyendo metadatos si existen."""
        if not metadata:
            return message

        try:
            metadata_str = json.dumps(metadata, separators=(',', ':'), ensure_ascii=False)
            return f"{message} | META: {metadata_str}"
        except (TypeError, ValueError):
            return f"{message} | META: [SERIALIZATION_ERROR]"

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas del sistema de logging."""
        with self.lock:
            return {
                'total_logs': self.stats['total_logs'],
                'logs_by_directory': self.stats['logs_by_directory'].copy(),
                'directories_active': list(self.stats['logs_by_directory'].keys()),
                'silent_mode': self.silent_mode
            }

    def create_directory_summary(self):
        """Crea un resumen de la actividad por directorio."""
        stats = self.get_stats()

        summary_file = self.directory_mapper.base_log_dir / "directory_summary.json"
        summary_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': stats,
            'directory_mapping': self.directory_mapper.directory_mapping
        }

        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)

# =============================================================================
# INSTANCIA GLOBAL Y FUNCIONES DE CONVENIENCIA
# =============================================================================

_smart_logger = SmartDirectoryLogger()

def smart_log(level: str, message: str, source: str,
              category: str = 'general', metadata: Optional[Dict] = None):
    """
    Función global para logging inteligente con directorios automáticos.

    Ejemplos de uso:
    smart_log('INFO', 'Trade executed', 'core.trading', 'trading')
    smart_log('ERROR', 'Connection failed', 'mt5.connector', 'mt5')
    smart_log('DEBUG', 'Pattern detected', 'ict.detector', 'ict')
    """
    return _smart_logger.smart_log(level, message, source, category, metadata)

def get_smart_stats() -> Dict[str, Any]:
    """Obtiene estadísticas del sistema de logging inteligente."""
    return _smart_logger.get_stats()

def create_summary():
    """Crea resumen de actividad de directorios."""
    _smart_logger.create_directory_summary()

# Funciones de conveniencia para cada tipo de log
def log_trading(level: str, message: str, source: str, metadata: Optional[Dict] = None):
    """Log específico para trading - va automáticamente a data/logs/trading/"""
    smart_log(level, message, source, 'trading', metadata)

def log_ict(level: str, message: str, source: str, metadata: Optional[Dict] = None):
    """Log específico para ICT - va automáticamente a data/logs/ict/"""
    smart_log(level, message, source, 'ict', metadata)

def log_poi(level: str, message: str, source: str, metadata: Optional[Dict] = None):
    """Log específico para POI - va automáticamente a data/logs/poi/"""
    smart_log(level, message, source, 'poi', metadata)

def log_mt5(level: str, message: str, source: str, metadata: Optional[Dict] = None):
    """Log específico para MT5 - va automáticamente a data/logs/mt5/"""
    smart_log(level, message, source, 'mt5', metadata)

def log_dashboard(level: str, message: str, source: str, metadata: Optional[Dict] = None):
    """Log específico para dashboard - va automáticamente a data/logs/dashboard/"""
    smart_log(level, message, source, 'dashboard', metadata)

def log_debug(level: str, message: str, source: str, metadata: Optional[Dict] = None):
    """Log específico para debug - va automáticamente a data/logs/debug/"""
    smart_log(level, message, source, 'debug', metadata)

def log_metrics(level: str, message: str, source: str, metadata: Optional[Dict] = None):
    """Log específico para métricas - va automáticamente a data/logs/metrics/"""
    smart_log(level, message, source, 'metrics', metadata)

def log_tct(level: str, message: str, source: str, metadata: Optional[Dict] = None):
    """Log específico para TCT - va automáticamente a data/logs/tct/"""
    smart_log(level, message, source, 'tct', metadata)

# =============================================================================
# FUNCIÓN DE MIGRACIÓN DESDE SLUC v2.0
# =============================================================================

def enviar_senal_log_smart(nivel: str, mensaje: str, emisor: str,
                          categoria: str = 'general',
                          metadata: Optional[Dict] = None, **kwargs):
    """
    Función de migración compatible con SLUC v2.0.
    Ahora usa el sistema inteligente de directorios.
    """
    return smart_log(nivel, mensaje, emisor, categoria, metadata)

# Alias para compatibilidad total
enviar_senal_log = enviar_senal_log_smart

if __name__ == "__main__":
    # Demo del sistema inteligente
    enviar_senal_log("INFO", "=== DEMO SISTEMA DE LOGGING INTELIGENTE CON DIRECTORIOS ===", "smart_directory_logger", "migration")
    enviar_senal_log("INFO", , "smart_directory_logger", "migration")

    # Ejemplos de diferentes tipos de logs
    smart_log('INFO', 'Sistema iniciado correctamente', 'main', 'daily')
    smart_log('INFO', 'Trade BUY EURUSD ejecutado', 'core.trading', 'trading')
    smart_log('DEBUG', 'Patrón ICT detectado en H4', 'ict.detector', 'ict')
    smart_log('INFO', 'POI de alta calidad encontrado', 'poi.system', 'poi')
    smart_log('WARNING', 'Conexión MT5 lenta', 'mt5.connector', 'mt5')
    smart_log('INFO', 'Dashboard actualizado', 'dashboard.main', 'dashboard')
    smart_log('ERROR', 'Error en validación de datos', 'debug.validator', 'debug')
    smart_log('INFO', 'Métricas de cuenta actualizadas', 'metrics.account', 'metrics')
    smart_log('INFO', 'TCT Pipeline ejecutado', 'tct.pipeline', 'tct')

    # Mostrar estadísticas
    stats = get_smart_stats()
    enviar_senal_log("INFO", "Estadísticas del sistema:", "smart_directory_logger", "migration")
    enviar_senal_log("INFO", f"  Total logs: {stats['total_logs']}", "smart_directory_logger", "migration")
    enviar_senal_log("INFO", f"  Directorios activos: {len(stats['directories_active'], "smart_directory_logger", "migration")}")
    enviar_senal_log("INFO", f"  Modo silencioso: {stats['silent_mode']}", "smart_directory_logger", "migration")
    enviar_senal_log("INFO", , "smart_directory_logger", "migration")
    enviar_senal_log("INFO", "Logs por directorio:", "smart_directory_logger", "migration")
    for directory, count in stats['logs_by_directory'].items():
        enviar_senal_log("INFO", f"  data/logs/{directory}/: {count} logs", "smart_directory_logger", "migration")

    # Crear resumen
    create_summary()
    enviar_senal_log("INFO", , "smart_directory_logger", "migration")
    enviar_senal_log("INFO", "✅ Logs organizados automáticamente en sus directorios correspondientes", "smart_directory_logger", "migration")
    enviar_senal_log("INFO", "✅ Sin emojis en archivos (formato profesional, "smart_directory_logger", "migration")")
    enviar_senal_log("INFO", "✅ Compatibilidad total con código existente", "smart_directory_logger", "migration")
    enviar_senal_log("INFO", "📁 Resumen guardado en data/logs/directory_summary.json", "smart_directory_logger", "migration")
