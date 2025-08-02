# utils/poi_utils.py
"""
POI Utilities
=============

Utilidades para manejo de múltiples tipos de POI (Points of Interest)
en el sistema SENTINEL GRID.

Tipos de POI soportados:
- BULLISH_OB: Order Block alcista
- BEARISH_OB: Order Block bajista  
- BULLISH_FVG: Fair Value Gap alcista
- BEARISH_FVG: Fair Value Gap bajista
- BULLISH_BREAKER: Breaker Block alcista
- BEARISH_BREAKER: Breaker Block bajista
- LIQUIDITY_VOID: Zona de baja liquidez
- PRICE_IMBALANCE: Desequilibrio de precio
"""

from typing import List, Dict, Optional
from datetime import datetime
# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log, log_poi

# =============================================================================
# CONFIGURACIÓN DE TIPOS POI
# =============================================================================

POI_TYPES = {
    "BULLISH_OB": {
        "emoji": "🔵",
        "color": "blue",
        "description": "Order Block Alcista",
        "priority": 1
    },
    "BEARISH_OB": {
        "emoji": "🔴", 
        "color": "red",
        "description": "Order Block Bajista",
        "priority": 1
    },
    "BULLISH_FVG": {
        "emoji": "🟢",
        "color": "green", 
        "description": "Fair Value Gap Alcista",
        "priority": 2
    },
    "BEARISH_FVG": {
        "emoji": "🟠",
        "color": "orange",
        "description": "Fair Value Gap Bajista", 
        "priority": 2
    },
    "BULLISH_BREAKER": {
        "emoji": "🟡",
        "color": "yellow",
        "description": "Breaker Block Alcista",
        "priority": 3
    },
    "BEARISH_BREAKER": {
        "emoji": "⚫",
        "color": "black",
        "description": "Breaker Block Bajista",
        "priority": 3
    },
    "LIQUIDITY_VOID": {
        "emoji": "⚪",
        "color": "white",
        "description": "Zona de Baja Liquidez",
        "priority": 4
    },
    "PRICE_IMBALANCE": {
        "emoji": "🟣",
        "color": "purple",
        "description": "Desequilibrio de Precio",
        "priority": 4
    }
}

# =============================================================================
# ESTRUCTURA ESTÁNDAR POI
# =============================================================================

def crear_poi_estructura(
    poi_type: str,
    price: float,
    score: float,
    confidence: str = "MEDIA",
    timeframe: str = "M15",
    range_high: Optional[float] = None,
    range_low: Optional[float] = None,
    **metadata
) -> Dict:
    """
    Crea una estructura POI estándar.
    
    Args:
        poi_type: Tipo de POI (debe estar en POI_TYPES)
        price: Precio central del POI
        score: Score de 0.0 a 10.0
        confidence: "ALTA", "MEDIA", "BAJA"
        timeframe: Timeframe donde se detectó
        range_high: Precio máximo del rango POI
        range_low: Precio mínimo del rango POI
        **metadata: Datos adicionales específicos del POI
    
    Returns:
        Dict con estructura POI estándar
    """
    
    # Validar tipo de POI
    if poi_type not in POI_TYPES:
        raise ValueError(f"Tipo POI '{poi_type}' no válido. Usar: {list(POI_TYPES.keys())}")
    
    # Calcular rango si no se proporciona
    if range_high is None:
        range_high = price * 1.0005  # +0.05%
    if range_low is None:
        range_low = price * 0.9995   # -0.05%
    
    return {
        "id": f"{poi_type}_{int(datetime.now().timestamp())}",
        "type": poi_type,
        "price": round(price, 5),
        "score": round(max(0.0, min(10.0, score)), 1),
        "confidence": confidence.upper(),
        "timeframe": timeframe,
        "timestamp": datetime.now().isoformat(),
        "range": {
            "high": round(range_high, 5),
            "low": round(range_low, 5),
            "width": round(range_high - range_low, 5)
        },
        "display": {
            "emoji": POI_TYPES[poi_type]["emoji"],
            "color": POI_TYPES[poi_type]["color"],
            "description": POI_TYPES[poi_type]["description"],
            "priority": POI_TYPES[poi_type]["priority"]
        },
        "metadata": metadata
    }

# =============================================================================
# FUNCIONES DE CLASIFICACIÓN
# =============================================================================

def clasificar_poi_por_tipo(poi_data: Dict) -> str:
    """
    Clasifica un POI genérico en un tipo específico.
    
    Args:
        poi_data: Datos del POI a clasificar
        
    Returns:
        Tipo de POI clasificado
    """
    
    # Lógica de clasificación basada en características
    poi_type = poi_data.get('type', 'UNKNOWN')
    
    # Mapear tipos legacy a nuevos tipos
    type_mapping = {
        'BULLISH': 'BULLISH_OB',
        'BEARISH': 'BEARISH_OB',
        'OB_BULLISH': 'BULLISH_OB',
        'OB_BEARISH': 'BEARISH_OB',
        'FVG_BULL': 'BULLISH_FVG',
        'FVG_BEAR': 'BEARISH_FVG'
    }
    
    return type_mapping.get(poi_type, poi_type) or "UNKNOWN"

def calcular_score_poi(poi_data: Dict) -> float:
    """
    Calcula el score de un POI basado en múltiples factores.
    
    Args:
        poi_data: Datos del POI
        
    Returns:
        Score de 0.0 a 10.0
    """
    
    base_score = 5.0
    
    # Factores de scoring
    factors = {
        'volume': poi_data.get('volume', 0),
        'formation_strength': poi_data.get('formation_strength', 5.0),
        'confirmation_candles': poi_data.get('confirmation_candles', 0),
        'age_hours': poi_data.get('age_hours', 24),
        'touch_count': poi_data.get('touch_count', 0)
    }
    
    # Ajustes de score
    if factors['volume'] > 1000:
        base_score += 1.0
    if factors['formation_strength'] > 7.0:
        base_score += 1.5
    if factors['confirmation_candles'] >= 3:
        base_score += 1.0
    if factors['age_hours'] < 12:  # POI reciente
        base_score += 0.5
    if factors['touch_count'] == 0:  # POI intacto
        base_score += 1.0
    
    return round(max(0.0, min(10.0, base_score)), 1)

# =============================================================================
# FUNCIONES DE FILTRADO
# =============================================================================

def filtrar_pois_por_relevancia(
    pois_list: List[Dict], 
    min_score: float = 3.0,
    max_count: int = 10,
    current_price: Optional[float] = None
) -> List[Dict]:
    """
    Filtra POIs por relevancia y proximidad al precio actual.
    
    Args:
        pois_list: Lista de POIs
        min_score: Score mínimo para incluir
        max_count: Máximo número de POIs a retornar
        current_price: Precio actual para calcular proximidad
        
    Returns:
        Lista filtrada de POIs
    """
    
    # Filtrar por score mínimo
    filtered = [poi for poi in pois_list if poi.get('score', 0) >= min_score]
    
    # Ordenar por score y proximidad al precio actual
    def poi_priority(poi):
        score = poi.get('score', 0)
        priority = poi.get('display', {}).get('priority', 10)
        
        # Factor de proximidad si tenemos precio actual
        proximity_factor = 0
        if current_price:
            price_distance = abs(poi.get('price', 0) - current_price)
            proximity_factor = 1.0 / (1.0 + price_distance * 1000)  # Normalizado
        
        return (score + proximity_factor) / priority
    
    filtered.sort(key=poi_priority, reverse=True)
    
    return filtered[:max_count]

def agrupar_pois_cercanos(
    pois_list: List[Dict], 
    distance_threshold: float = 0.0010
) -> List[Dict]:
    """
    Agrupa POIs que están muy cerca entre sí.
    
    Args:
        pois_list: Lista de POIs
        distance_threshold: Distancia máxima para agrupar (en precio)
        
    Returns:
        Lista de POIs agrupados
    """
    
    if not pois_list:
        return []
    
    grouped = []
    used_indices = set()
    
    for i, poi in enumerate(pois_list):
        if i in used_indices:
            continue
            
        group = [poi]
        poi_price = poi.get('price', 0)
        
        # Buscar POIs cercanos
        for j, other_poi in enumerate(pois_list[i+1:], i+1):
            if j in used_indices:
                continue
                
            other_price = other_poi.get('price', 0)
            if abs(poi_price - other_price) <= distance_threshold:
                group.append(other_poi)
                used_indices.add(j)
        
        # Si hay múltiples POIs en el grupo, crear POI combinado
        if len(group) > 1:
            combined_poi = combinar_pois_grupo(group)
            grouped.append(combined_poi)
        else:
            grouped.append(poi)
        
        used_indices.add(i)
    
    return grouped

def combinar_pois_grupo(pois_group: List[Dict]) -> Dict:
    """
    Combina múltiples POIs cercanos en uno solo.
    
    Args:
        pois_group: Lista de POIs a combinar
        
    Returns:
        POI combinado
    """
    
    # Tomar el POI con mejor score como base
    base_poi = max(pois_group, key=lambda p: p.get('score', 0))
    
    # Calcular precio promedio
    avg_price = sum(p.get('price', 0) for p in pois_group) / len(pois_group)
    
    # Combinar metadata
    combined_metadata = {
        'group_size': len(pois_group),
        'group_types': [p.get('type') for p in pois_group],
        'combined_score': sum(p.get('score', 0) for p in pois_group) / len(pois_group)
    }
    
    # Crear POI combinado
    combined = base_poi.copy()
    combined['price'] = round(avg_price, 5)
    combined['score'] = round(combined_metadata['combined_score'], 1)
    combined['id'] = f"COMBINED_{int(datetime.now().timestamp())}"
    combined['metadata'].update(combined_metadata)
    
    return combined

# =============================================================================
# FUNCIONES DE DISPLAY
# =============================================================================

def formatear_poi_para_dashboard(poi: Dict, compact: bool = False) -> str:
    """
    Formatea un POI para mostrar en el dashboard.
    
    Args:
        poi: Diccionario del POI
        compact: Si usar formato compacto
        
    Returns:
        String formateado para display
    """
    
    emoji = poi.get('display', {}).get('emoji', '⚪')
    poi_type = poi.get('type', 'UNKNOWN')
    price = poi.get('price', 0)
    score = poi.get('score', 0)
    
    if compact:
        # Formato compacto: "🔵 BULLISH_OB $1.16180 (7.5)"
        return f"{emoji} {poi_type} ${price:.5f} ({score})"
    else:
        # Formato detallado
        confidence = poi.get('confidence', 'MEDIA')
        timeframe = poi.get('timeframe', 'M15')
        description = poi.get('display', {}).get('description', poi_type)
        
        return f"{emoji} {description} | ${price:.5f} | Score: {score}/10 | {confidence} | {timeframe}"

def crear_resumen_pois(pois_list: List[Dict]) -> Dict:
    """
    Crea un resumen estadístico de la lista de POIs.
    
    Args:
        pois_list: Lista de POIs
        
    Returns:
        Diccionario con estadísticas
    """
    
    if not pois_list:
        return {
            'total_pois': 0,
            'avg_score': 0.0,
            'best_poi': None,
            'types_count': {},
            'confidence_distribution': {}
        }
    
    # Estadísticas básicas
    total_pois = len(pois_list)
    avg_score = sum(p.get('score', 0) for p in pois_list) / total_pois
    best_poi = max(pois_list, key=lambda p: p.get('score', 0))
    
    # Conteo por tipos
    types_count = {}
    confidence_distribution = {}
    
    for poi in pois_list:
        poi_type = poi.get('type', 'UNKNOWN')
        confidence = poi.get('confidence', 'MEDIA')
        
        types_count[poi_type] = types_count.get(poi_type, 0) + 1
        confidence_distribution[confidence] = confidence_distribution.get(confidence, 0) + 1
    
    return {
        'total_pois': total_pois,
        'avg_score': round(avg_score, 1),
        'best_poi': best_poi,
        'types_count': types_count,
        'confidence_distribution': confidence_distribution,
        'score_range': {
            'min': min(p.get('score', 0) for p in pois_list),
            'max': max(p.get('score', 0) for p in pois_list)
        }
    }

# =============================================================================
# FUNCIONES PARA TESTING
# =============================================================================

def crear_pois_ejemplo() -> List[Dict]:
    """
    Crea POIs de ejemplo para testing.
    
    Returns:
        Lista de POIs de ejemplo
    """
    
    pois_ejemplo = [
        crear_poi_estructura(
            "BULLISH_OB", 1.16180, 7.5, "ALTA", "M15",
            range_high=1.16200, range_low=1.16160,
            volume=1250, formation_strength=8.2, confirmation_candles=3
        ),
        crear_poi_estructura(
            "BEARISH_FVG", 1.16250, 6.2, "MEDIA", "H1", 
            range_high=1.16270, range_low=1.16230,
            volume=980, formation_strength=6.8, confirmation_candles=2
        ),
        crear_poi_estructura(
            "BULLISH_BREAKER", 1.16120, 5.8, "MEDIA", "M15",
            range_high=1.16140, range_low=1.16100,
            volume=750, formation_strength=6.1, confirmation_candles=4
        ),
        crear_poi_estructura(
            "LIQUIDITY_VOID", 1.16300, 4.1, "BAJA", "H4",
            range_high=1.16320, range_low=1.16280,
            volume=400, formation_strength=4.5, confirmation_candles=1
        )
    ]
    
    return pois_ejemplo

if __name__ == "__main__":
    # Test básico
    enviar_senal_log("INFO", "Testing POI Utilities...", __name__, "poi")
    
    # Crear POIs de ejemplo
    pois = crear_pois_ejemplo()
    enviar_senal_log("INFO", f"Creados {len(pois)} POIs de ejemplo", __name__, "poi")
    
    # Filtrar por relevancia
    filtered = filtrar_pois_por_relevancia(pois, min_score=5.0, current_price=1.16200)
    enviar_senal_log("INFO", f"Filtrados {len(filtered)} POIs relevantes", __name__, "poi")
    
    # Formatear para display
    for poi in filtered:
        enviar_senal_log("DEBUG", f"POI: {formatear_poi_para_dashboard(poi, compact=True)}", __name__, "poi")
    
    # Crear resumen
    resumen = crear_resumen_pois(pois)
    enviar_senal_log("INFO", f"Resumen: {resumen.get("total_pois", 0)} POIs, Score promedio: {resumen['avg_score']}", __name__, "poi")
    
    enviar_senal_log("SUCCESS", "POI Utilities funcionando correctamente!", __name__, "poi")
