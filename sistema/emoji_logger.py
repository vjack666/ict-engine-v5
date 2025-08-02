"""
🎨 EMOJI LOGGER - Sistema de Logging Visual Inteligente
======================================================

Solución para mantener emojis en consola y ASCII en archivos de log.
Compatible con Windows cp1252 y UTF-8.

Funcionalidades:
- Emojis visibles en consola para experiencia de usuario
- Texto ASCII limpio en archivos de log
- Mapeo automático de emojis a texto descriptivo
- Preserva toda la funcionalidad existente

Versión: v1.0.0
Fecha: 27 Julio 2025
"""

import logging
import re
from typing import Dict, Optional

class EmojiSafeLogger:
    """
    Logger que convierte emojis a texto ASCII para archivos y mantiene emojis en consola.
    """
    
    # Mapeo de emojis a texto ASCII descriptivo
    EMOJI_MAP = {
        '🚀': '[INICIO]',
        '🎯': '[TARGET]',
        '✅': '[OK]',
        '❌': '[ERROR]',
        '⚡': '[FAST]',
        '🧠': '[BRAIN]',
        '🔍': '[SEARCH]',
        '📊': '[DATA]',
        '⚠️': '[WARNING]',
        '🎉': '[SUCCESS]',
        '🔧': '[TOOL]',
        '📈': '[UP]',
        '📉': '[DOWN]',
        '💡': '[IDEA]',
        '🎲': '[RANDOM]',
        '🏁': '[FINISH]',
        '🌟': '[STAR]',
        '🔥': '[HOT]',
        '💪': '[STRONG]',
        '🎪': '[SHOW]',
        '🛡️': '[SHIELD]',
        '⭐': '[GRADE]',
        '🎨': '[ART]',
        '🧪': '[TEST]',
        '🚦': '[STATUS]',
        '📋': '[LIST]',
        '🎭': '[MASK]',
        '🔮': '[MAGIC]',
        '⚙️': '[CONFIG]',
        '📢': '[ANNOUNCE]',
        '🎪': '[CIRCUS]',
    }
    
    def __init__(self, base_logger: logging.Logger):
        """
        Inicializa el emoji logger con un logger base.
        
        Args:
            base_logger: Logger estándar de Python
        """
        self.base_logger = base_logger
    
    def _convert_emojis_to_ascii(self, message: str) -> str:
        """
        Convierte emojis en el mensaje a texto ASCII descriptivo.
        OPTIMIZADO para evitar encoding errors en logs usando técnicas robustas.
        
        Args:
            message: Mensaje original con posibles emojis
            
        Returns:
            Mensaje con emojis convertidos a ASCII limpio
        """
        ascii_message = message
        
        for emoji, ascii_replacement in self.EMOJI_MAP.items():
            ascii_message = ascii_message.replace(emoji, ascii_replacement)
        
        # Remover cualquier emoji no mapeado usando regex
        # Esto captura la mayoría de emojis Unicode
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE
        )
        
        ascii_message = emoji_pattern.sub('[EMOJI]', ascii_message)
        
        # TÉCNICA ROBUSTA: Forzar encoding seguro (inspirado en universal_intelligent_logger)
        try:
            # 1. Intentar mantener UTF-8 válido
            ascii_message.encode('utf-8')
        except UnicodeEncodeError:
            # 2. Fallback robusto - limpiar caracteres problemáticos
            ascii_message = ascii_message.encode('ascii', 'replace').decode('ascii')
        
        # 3. Limpiar caracteres de control problemáticos comunes que aparecen en logs
        problematic_chars = {
            'ð': '[D]',        # Caracter corrupto común
            'Ÿ': '[Y]',        # Caracter corrupto común  
            'Š': '[S]',        # Caracter corrupto común
            'â': '[A]',        # Caracter corrupto común
            'ï¸': '[I]',       # Caracter corrupto común
            'ðŸŽ¯': '[TARGET]', # Emoji target corrupto
            'ðŸ"§': '[TOOL]',   # Emoji tool corrupto
            'â ï¸': '[WARNING]', # Emoji warning corrupto
            'ðŸ"Š': '[CHART]',  # Emoji chart corrupto
            'âœ…': '[CHECK]',   # Emoji check corrupto
            'ðŸš¨': '[ALERT]',  # Emoji alert corrupto
            'ðŸ"ˆ': '[TREND_UP]' # Emoji trend corrupto
        }
        
        for problematic, replacement in problematic_chars.items():
            ascii_message = ascii_message.replace(problematic, replacement)
        
        return ascii_message
    
    def info(self, message: str, *args, **kwargs):
        """Log info con conversión automática de emojis"""
        ascii_message = self._convert_emojis_to_ascii(message)
        self.base_logger.info(ascii_message, *args, **kwargs)
    
    def debug(self, message: str, *args, **kwargs):
        """Log debug con conversión automática de emojis"""
        ascii_message = self._convert_emojis_to_ascii(message)
        self.base_logger.debug(ascii_message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """Log warning con conversión automática de emojis"""
        ascii_message = self._convert_emojis_to_ascii(message)
        self.base_logger.warning(ascii_message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """Log error con conversión automática de emojis"""
        ascii_message = self._convert_emojis_to_ascii(message)
        self.base_logger.error(ascii_message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """Log critical con conversión automática de emojis"""
        ascii_message = self._convert_emojis_to_ascii(message)
        self.base_logger.critical(ascii_message, *args, **kwargs)

def get_emoji_safe_logger(name: Optional[str] = None) -> EmojiSafeLogger:
    """
    Obtiene un logger emoji-safe para cualquier módulo.
    
    Args:
        name: Nombre del módulo
        
    Returns:
        EmojiSafeLogger configurado
        
    Ejemplo de uso:
        logger = get_emoji_safe_logger(__name__)
        logger.info("🚀 INICIANDO SISTEMA")  # En archivo: [INICIO] INICIANDO SISTEMA
        print("🚀 INICIANDO SISTEMA")        # En consola: 🚀 INICIANDO SISTEMA
    """
    from sistema.logging_config import get_logger
    base_logger = get_logger(name)
    return EmojiSafeLogger(base_logger)

def safe_log_and_print(module: str, message: str, show_in_console: bool = True):
    """
    Función de conveniencia para log seguro + print con emojis.
    
    Args:
        module: Nombre del módulo/sistema
        message: Mensaje con emojis
        show_in_console: Si mostrar en consola con emojis
        
    Ejemplo:
        safe_log_and_print("MAIN", "🚀 Sistema iniciado", True)
        # Log archivo: [INICIO] Sistema iniciado
        # Consola: 🚀 Sistema iniciado
    """
    logger = get_emoji_safe_logger(module.lower())
    logger.info(message)
    
    if show_in_console:
        print(f"[{module}] {message}")
