"""
🎯 POI SCORING ENGINE - Sistema Inteligente de Calificación de POIs
=================================================================

Módulo que implementa el scoring avanzado para garantizar que el panel
del dashboard SIEMPRE reciba información significativa y procesable.

OBJETIVO: Eliminar casos de datos vacíos/None en el panel dashboard.

Funcionalidades:
- Scoring contextual por proximidad al precio
- Clasificación por grados (A+, A, B, C)
- Confidence scoring basado en múltiples factores
- Narrativa inteligente para cada POI

Versión: v3.5.1 (Nueva implementación)
Fecha: 27 Julio 2025
"""

from typing import List, Dict, Optional
from datetime import datetime
# Logger especializado
from sistema.logging_interface import enviar_senal_log, log_poi
# Usar sistema de logging central

class POIScoringEngine:
    """
    Motor de scoring inteligente para POIs que garantiza datos
    significativos para el dashboard.
    """

    def __init__(self):
        """Inicializa el motor de scoring con configuraciones optimizadas."""
        self.config = {
            'DISTANCE_WEIGHTS': {
                'VERY_CLOSE': (0, 10),      # 0-10 pips: máxima relevancia
                'CLOSE': (10, 25),          # 10-25 pips: alta relevancia
                'MEDIUM': (25, 50),         # 25-50 pips: media relevancia
                'FAR': (50, 100),           # 50-100 pips: baja relevancia
                'VERY_FAR': (100, float('inf'))  # >100 pips: mínima relevancia
            },
            'QUALITY_GRADES': {
                'A+': {'min_score': 85, 'color': 'bright_green', 'confidence': 0.9},
                'A': {'min_score': 75, 'color': 'green', 'confidence': 0.8},
                'B': {'min_score': 65, 'color': 'yellow', 'confidence': 0.7},
                'C': {'min_score': 50, 'color': 'orange', 'confidence': 0.6},
                'D': {'min_score': 0, 'color': 'red', 'confidence': 0.4}
            },
            'POI_TYPE_MULTIPLIERS': {
                'BULLISH_OB': 1.2,
                'BEARISH_OB': 1.2,
                'BULLISH_FVG': 1.0,
                'BEARISH_FVG': 1.0,
                'BULLISH_BREAKER': 1.1,
                'BEARISH_BREAKER': 1.1,
                'LIQUIDITY_VOID': 0.9,
                'PRICE_IMBALANCE': 0.8
            }
        }

        log_poi("INFO", "POI Scoring Engine inicializado", "poi_scoring_engine")

    def calculate_intelligent_score(self, poi: Dict, current_price: float,
                                   market_context: Optional[Dict] = None) -> Dict:
        """
        Calcula un score inteligente y contextual para un POI.

        Args:
            poi: Diccionario con datos del POI
            current_price: Precio actual del mercado
            market_context: Contexto adicional del mercado

        Returns:
            Dict con score, grado, confianza y narrativa
        """
        try:
            # 1. SCORE BASE del POI (del sistema original)
            base_score = poi.get('score', 50)

            # 2. SCORE POR PROXIMIDAD (factor crítico)
            distance_pips = abs(current_price - poi['price']) * 10000  # Convertir a pips
            proximity_score = self._calculate_proximity_score(distance_pips)

            # 3. SCORE POR TIPO DE POI (algunos son más importantes)
            type_multiplier = self.config['POI_TYPE_MULTIPLIERS'].get(poi['type'], 1.0)

            # 4. SCORE CONTEXTUAL (basado en dirección de mercado)
            context_score = self._calculate_context_score(poi, market_context)

            # 5. SCORE FINAL COMBINADO
            final_score = (
                base_score * 0.4 +           # 40% score original
                proximity_score * 0.35 +     # 35% proximidad
                context_score * 0.25         # 25% contexto
            ) * type_multiplier

            # Limitar entre 0-100
            final_score = max(0, min(100, final_score))

            # 6. DETERMINAR GRADO Y CONFIANZA
            grade_info = self._determine_grade(final_score)

            # 7. GENERAR NARRATIVA INTELIGENTE
            narrative = self._generate_poi_narrative(poi, grade_info, distance_pips)

            result = {
                'original_score': base_score,
                'proximity_score': proximity_score,
                'context_score': context_score,
                'final_score': round(final_score, 1),
                'grade': grade_info['grade'],
                'confidence': grade_info['confidence'],
                'color': grade_info['color'],
                'distance_pips': round(distance_pips, 1),
                'narrative': narrative,
                'type_multiplier': type_multiplier
            }

            log_poi("DEBUG", f"POI {poi['type']} scored: {final_score:.1f} ({grade_info['grade']})", "poi_scoring_engine")

            return result

        except (ValueError, KeyError, TypeError) as e:
            log_poi("ERROR", f"Error calculando score inteligente: {e}", "poi_scoring_engine")
            # Fallback seguro
            return {
                'final_score': 50.0,
                'grade': 'C',
                'confidence': 0.5,
                'color': 'orange',
                'narrative': f"POI {poi['type']} detectado (score por defecto)"
            }

    def _calculate_proximity_score(self, distance_pips: float) -> float:
        """Calcula score basado en proximidad al precio actual."""
        if distance_pips <= 10:
            return 100  # Muy cerca: máximo score
        elif distance_pips <= 25:
            return 85   # Cerca: score alto
        elif distance_pips <= 50:
            return 70   # Medio: score medio
        elif distance_pips <= 100:
            return 50   # Lejos: score bajo
        else:
            return 30   # Muy lejos: score mínimo

    def _calculate_context_score(self, poi: Dict, market_context: Optional[Dict]) -> float:
        """Calcula score basado en contexto de mercado."""
        if not market_context:
            return 60  # Score neutro sin contexto

        try:
            # Verificar alineación con bias del mercado
            h4_bias = market_context.get('h4_bias', 'NEUTRAL')
            poi_type = poi['type']

            # Score mayor si POI está alineado con bias
            if ('BULLISH' in poi_type and h4_bias == 'BULLISH') or \
               ('BEARISH' in poi_type and h4_bias == 'BEARISH'):
                return 85  # Alineado con tendencia
            elif h4_bias == 'NEUTRAL':
                return 70  # Mercado neutral
            else:
                return 55  # Contra tendencia (menos probable)

        except (ValueError, KeyError, TypeError):
            return 60  # Score neutro en caso de error

    def _determine_grade(self, score: float) -> Dict:
        """Determina el grado basado en el score final."""
        for grade, config in self.config['QUALITY_GRADES'].items():
            if score >= config['min_score']:
                return {
                    'grade': grade,
                    'confidence': config['confidence'],
                    'color': config['color']
                }

        # Fallback (no debería llegar aquí)
        return {
            'grade': 'D',
            'confidence': 0.4,
            'color': 'red'
        }

    def _generate_poi_narrative(self, poi: Dict, grade_info: Dict, distance_pips: float) -> str:
        """Genera una narrativa inteligente para el POI."""
        try:
            poi_type = poi['type']
            grade = grade_info['grade']
            price = poi['price']

            # Nombres amigables para los tipos de POI
            type_names = {
                'BULLISH_OB': 'Order Block Alcista',
                'BEARISH_OB': 'Order Block Bajista',
                'BULLISH_FVG': 'Gap de Valor Alcista',
                'BEARISH_FVG': 'Gap de Valor Bajista',
                'BULLISH_BREAKER': 'Breaker Alcista',
                'BEARISH_BREAKER': 'Breaker Bajista'
            }

            friendly_name = type_names.get(poi_type, poi_type)

            # Narrativa basada en grado
            if grade in ['A+', 'A']:
                quality_desc = "de alta calidad"
                action_desc = "Setup prioritario para monitoreo"
            elif grade == 'B':
                quality_desc = "de calidad media"
                action_desc = "Setup válido para considerar"
            else:
                quality_desc = "de baja calidad"
                action_desc = "Setup de respaldo"

            # Distancia en términos comprensibles
            if distance_pips <= 10:
                distance_desc = "muy cerca"
            elif distance_pips <= 25:
                distance_desc = "cerca"
            elif distance_pips <= 50:
                distance_desc = "a distancia media"
            else:
                distance_desc = "lejos"

            narrative = f"{friendly_name} {quality_desc} en {price:.5f} ({distance_desc}, {distance_pips:.1f} pips). {action_desc}."

            return narrative

        except (ValueError, KeyError, TypeError) as e:
            log_poi("WARNING", f"Error generando narrativa: {e}", "poi_scoring_engine")
            return f"POI {poi_type} detectado en {poi.get('price', 0):.5f}"

    def process_pois_for_dashboard(self, pois_list: List[Dict], current_price: float,
                                  market_context: Optional[Dict] = None) -> List[Dict]:
        """
        Procesa una lista de POIs aplicando scoring inteligente para el dashboard.

        GARANTIZA que el dashboard SIEMPRE reciba datos procesables.
        """
        if not pois_list:
            log_poi("WARNING", "Lista de POIs vacía recibida", "poi_scoring_engine")
            return []

        processed_pois = []

        for poi in pois_list:
            try:
                # Aplicar scoring inteligente
                scoring_result = self.calculate_intelligent_score(poi, current_price, market_context)

                # Combinar datos originales con scoring
                enhanced_poi = {
                    **poi,  # Datos originales
                    'intelligent_score': scoring_result['final_score'],
                    'grade': scoring_result['grade'],
                    'confidence': scoring_result['confidence'],
                    'color': scoring_result['color'],
                    'distance_pips': scoring_result['distance_pips'],
                    'narrative': scoring_result['narrative'],
                    'dashboard_ready': True,  # Flag de que está listo para dashboard
                    'last_scored': datetime.now().isoformat()
                }

                processed_pois.append(enhanced_poi)

            except (ValueError, KeyError, TypeError) as e:
                log_poi("ERROR", f"Error procesando POI: {e}", "poi_scoring_engine")
                # Incluir POI con datos mínimos para evitar lista vacía
                fallback_poi = {
                    **poi,
                    'intelligent_score': 50.0,
                    'grade': 'C',
                    'confidence': 0.5,
                    'color': 'orange',
                    'narrative': f"POI {poi.get('type', 'UNKNOWN')} (procesamiento fallback)",
                    'dashboard_ready': True
                }
                processed_pois.append(fallback_poi)

        # Ordenar por score inteligente
        processed_pois.sort(key=lambda x: x['intelligent_score'], reverse=True)

        log_poi("INFO", f"✅ {len(processed_pois)} POIs procesados para dashboard", "poi_scoring_engine")

        return processed_pois

# Instancia global del motor de scoring
poi_scoring_engine = POIScoringEngine()

def enhance_pois_for_dashboard(pois: List[Dict], current_price: float,
                              market_context: Optional[Dict] = None) -> List[Dict]:
    """
    Función de conveniencia para mejorar POIs para el dashboard.

    Esta función es la que usará app.py para garantizar datos de calidad.
    """
    return poi_scoring_engine.process_pois_for_dashboard(pois, current_price, market_context)
