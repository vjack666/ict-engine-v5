"""
🎯 VEREDICTO ENGINE v4.0 - Selector de la Mejor Oportunidad
==========================================================

Motor refinado que selecciona la mejor oportunidad entre patrones ICT y POIs
ya enriquecidos con confidence scores. Su trabajo es elegir el "mejor de los mejores"
y emitir un veredicto final procesable.

RESPONSABILIDAD: Selector inteligente de oportunidades, no calculador de confianza.

Funcionalidades:
- Selección del mejor patrón ICT + POI combinado
- Veredicto final basado en la mejor oportunidad disponible
- Primary signals garantizados siempre
- Action plans específicos por grade

Versión: v4.0.0 (Refactorizado para ConfidenceEngine)
Fecha: 27 Julio 2025
"""
# TODO: Eliminado - usar enviar_senal_log # import logging
from sistema.sic import Optional, Dict, List, Any, Tuple
from sistema.sic import datetime
# Logger usando sistema estándar SLUC v2.0
from sistema.sic import enviar_senal_log
def log_veredicto(level, message):
    enviar_senal_log(level, message, 'veredicto_engine_v4', 'ict')

class VeredictoEngine:
    """
    Motor de veredicto refinado que selecciona la mejor oportunidad
    entre patrones ICT enriquecidos y POIs con confidence scores.

    Su función es ser un "selector inteligente" que elige la mejor
    combinación disponible y emite veredictos procesables.
    """

    def __init__(self):
        """Inicializa el motor de veredicto con configuración optimizada."""
        log_veredicto("INFO", "🎯 Inicializando Veredicto Engine v4.0")

        # Configuración de grades y acciones
        self.config = {
            'VEREDICTO_GRADES': {
                'A+': {
                    'min_confidence': 0.85,
                    'emoji': '🟢',
                    'action': 'EJECUTAR',
                    'narrative': 'Setup Excepcional - Confluencia perfecta detectada',
                    'risk_suggestion': 0.8
                },
                'A': {
                    'min_confidence': 0.75,
                    'emoji': '🟡',
                    'action': 'CONSIDERAR',
                    'narrative': 'Setup Excelente - Alta probabilidad de éxito',
                    'risk_suggestion': 0.6
                },
                'B': {
                    'min_confidence': 0.65,
                    'emoji': '🟠',
                    'action': 'MONITOREAR',
                    'narrative': 'Setup Válido - Oportunidad con riesgo controlado',
                    'risk_suggestion': 0.4
                },
                'C': {
                    'min_confidence': 0.50,
                    'emoji': '🔴',
                    'action': 'ESPERAR',
                    'narrative': 'Setup Marginal - Señales débiles, alta cautela',
                    'risk_suggestion': 0.2
                },
                'D': {
                    'min_confidence': 0.0,
                    'emoji': '👁️',
                    'action': 'OBSERVAR',
                    'narrative': 'Sin Setup Claro - Mercado en consolidación',
                    'risk_suggestion': 0.0
                }
            },
            'PRIORITY_WEIGHTS': {
                'ict_pattern': 0.6,    # 60% peso a patrones ICT
                'poi_quality': 0.4,    # 40% peso a calidad POI
            }
        }

        log_veredicto("INFO", "✅ Veredicto Engine v4.0 inicializado - Selector de Oportunidades Listo")

    def generate_market_veredicto(self,
                                enhanced_pois: List[Dict],
                                ict_patterns: List[Dict],
                                market_context: Optional[Dict] = None,
                                current_price: float = 0.0) -> Dict:
        """
        Genera veredicto final seleccionando la mejor oportunidad disponible.

        Args:
            enhanced_pois: POIs ya enriquecidos con scores del POI Scoring Engine
            ict_patterns: Patrones ICT ya enriquecidos con scores del Confidence Engine
            market_context: Contexto de mercado (bias, fase, etc.)
            current_price: Precio actual

        Returns:
            Dict con veredicto final procesable
        """
        try:
            log_veredicto("INFO", f"🔍 Analizando {len(ict_patterns)} patrones ICT + {len(enhanced_pois)} POIs")

            # 1. SELECCIONAR LA MEJOR OPORTUNIDAD COMBINADA
            best_opportunity = self._select_best_opportunity(ict_patterns, enhanced_pois, current_price)

            # 2. DETERMINAR GRADE FINAL DEL VEREDICTO
            final_grade = self._determine_final_grade(best_opportunity)

            # 3. GENERAR NARRATIVA Y ACTION PLAN
            narrative_data = self._generate_veredicto_narrative(best_opportunity, final_grade, market_context)

            # 4. CREAR VEREDICTO FINAL
            veredicto = {
                'timestamp': datetime.now().isoformat(),
                'setup_grade': final_grade,
                'confidence_score': best_opportunity['final_confidence'],
                'primary_signal': narrative_data['primary_signal'],
                'detailed_narrative': narrative_data['detailed_narrative'],
                'action_plan': narrative_data['action_plan'],
                'risk_suggestion': self.config['VEREDICTO_GRADES'][final_grade]['risk_suggestion'],
                'best_pattern': best_opportunity.get('ict_pattern'),
                'best_poi': best_opportunity.get('poi'),
                'opportunity_type': best_opportunity['type'],
                'market_context': market_context,
                'dashboard_ready': True
            }

            log_veredicto("INFO",
                f"✅ Veredicto Final: {final_grade} | "
                f"Confianza: {best_opportunity['final_confidence']:.3f} | "
                f"Tipo: {best_opportunity['type']}"
            )

            return veredicto

        except (FileNotFoundError, PermissionError, IOError) as e:
            log_veredicto("ERROR", f"❌ Error obteniendo últimas velas: {str(e)}")
            return self._generate_fallback_veredicto(current_price)

    def _select_best_opportunity(self, ict_patterns: List[Dict],
                               enhanced_pois: List[Dict],
                               current_price: float) -> Dict:
        """
        Selecciona la mejor oportunidad entre patrones ICT y POIs.

        Evalúa tres tipos de oportunidades:
        1. ICT Pattern + POI en confluencia (BEST)
        2. ICT Pattern standalone (GOOD)
        3. POI standalone (FALLBACK)
        """
        best_opportunity = {
            'type': 'NONE',
            'final_confidence': 0.0,
            'ict_pattern': None,
            'poi': None
        }

        # TIPO 1: CONFLUENCIA ICT + POI (Máxima prioridad)
        confluence_opportunities = self._find_confluence_opportunities(ict_patterns, enhanced_pois)

        for conf_opp in confluence_opportunities:
            combined_confidence = (
                conf_opp['ict_confidence'] * self.config['PRIORITY_WEIGHTS']['ict_pattern'] +
                conf_opp['poi_confidence'] * self.config['PRIORITY_WEIGHTS']['poi_quality']
            )

            if combined_confidence > best_opportunity['final_confidence']:
                best_opportunity = {
                    'type': 'ICT_POI_CONFLUENCE',
                    'final_confidence': combined_confidence,
                    'ict_pattern': conf_opp['ict_pattern'],
                    'poi': conf_opp['poi'],
                    'confluence_bonus': 0.1  # 10% bonus por confluencia
                }

                log_veredicto("DEBUG", f"🎯 Confluencia detectada: {combined_confidence}")

        # TIPO 2: ICT PATTERN STANDALONE (Si no hay confluencia)
        if best_opportunity['type'] == 'NONE' and ict_patterns:
            best_ict = max(ict_patterns, key=lambda p: p.get('confidence_score', 0))

            if best_ict.get('confidence_score', 0) > best_opportunity['final_confidence']:
                best_opportunity = {
                    'type': 'ICT_STANDALONE',
                    'final_confidence': best_ict.get('confidence_score', 0),
                    'ict_pattern': best_ict,
                    'poi': None
                }

                log_veredicto("DEBUG", f"🔍 Mejor ICT standalone: {best_ict.get('confidence_score', 0)}")

        # TIPO 3: POI STANDALONE (Fallback)
        if best_opportunity['type'] == 'NONE' and enhanced_pois:
            best_poi = max(enhanced_pois, key=lambda p: p.get('intelligent_score', 0))
            poi_confidence = best_poi.get('intelligent_score', 0) / 100.0  # Convertir a 0-1

            if poi_confidence > best_opportunity['final_confidence']:
                best_opportunity = {
                    'type': 'POI_STANDALONE',
                    'final_confidence': poi_confidence,
                    'ict_pattern': None,
                    'poi': best_poi
                }

                log_veredicto("DEBUG", f"📍 Mejor POI standalone: {poi_confidence}")

        # Aplicar bonus de confluencia si corresponde
        if best_opportunity['type'] == 'ICT_POI_CONFLUENCE':
            best_opportunity['final_confidence'] += best_opportunity.get('confluence_bonus', 0)
            best_opportunity['final_confidence'] = min(best_opportunity['final_confidence'], 1.0)

        log_veredicto("INFO", f"🏆 Mejor oportunidad: {best_opportunity['type']} (Confianza: {best_opportunity['final_confidence']})")

        return best_opportunity

    def _find_confluence_opportunities(self, ict_patterns: List[Dict],
                                     enhanced_pois: List[Dict]) -> List[Dict]:
        """
        Encuentra oportunidades de confluencia entre patrones ICT y POIs.

        Una confluencia existe cuando un patrón ICT y un POI están
        dentro de una distancia razonable (ej. 10 pips).
        """
        confluence_opportunities = []
        confluence_distance = 10 * 0.0001  # 10 pips convertidos a precio

        for ict_pattern in ict_patterns:
            ict_price = ict_pattern.get('price', 0)
            ict_confidence = ict_pattern.get('confidence_score', 0)

            for poi in enhanced_pois:
                poi_price = poi.get('price', 0)
                poi_confidence = poi.get('intelligent_score', 0) / 100.0  # Convertir a 0-1

                distance = abs(ict_price - poi_price)

                if distance <= confluence_distance:
                    confluence_opportunities.append({
                        'ict_pattern': ict_pattern,
                        'poi': poi,
                        'ict_confidence': ict_confidence,
                        'poi_confidence': poi_confidence,
                        'distance': distance
                    })

                    log_veredicto("DEBUG",
                        f"🎯 Confluencia: ICT {ict_price:.5f} <-> POI {poi_price:.5f} "
                        f"(Distancia: {distance/0.0001:.1f} pips)"
                    )

        # Ordenar por calidad combinada
        confluence_opportunities.sort(
            key=lambda x: x['ict_confidence'] + x['poi_confidence'],
            reverse=True
        )

        return confluence_opportunities

    def _determine_final_grade(self, best_opportunity: Dict) -> str:
        """
        Determina el grade final basado en la confianza de la mejor oportunidad.
        """
        final_confidence = best_opportunity['final_confidence']

        for grade, config in self.config['VEREDICTO_GRADES'].items():
            if final_confidence >= config['min_confidence']:
                log_veredicto("DEBUG", f"📊 Grade asignado: {grade} (Confianza: {final_confidence})")
                return grade

        return 'D'  # Fallback

    def _generate_veredicto_narrative(self, best_opportunity: Dict,
                                    final_grade: str,
                                    market_context: Optional[Dict] = None) -> Dict:
        """
        Genera narrativa completa para el veredicto basado en la mejor oportunidad.
        """
        grade_config = self.config['VEREDICTO_GRADES'][final_grade]
        opportunity_type = best_opportunity['type']

        # Primary Signal (Siempre garantizado)
        primary_signal = f"{grade_config['emoji']} {grade_config['narrative']} (Grado {final_grade})"

        # Detailed Narrative (Específica por tipo de oportunidad)
        if opportunity_type == 'ICT_POI_CONFLUENCE':
            ict_type = best_opportunity['ict_pattern'].get('pattern_type', 'ICT Pattern')
            poi_type = best_opportunity['poi'].get('type', 'POI')
            detailed_narrative = (
                f"🎯 CONFLUENCIA DETECTADA: {ict_type} alineado con {poi_type}. "
                f"Esta combinación presenta una oportunidad de alta calidad con "
                f"confluencia técnica confirmada."
            )
        elif opportunity_type == 'ICT_STANDALONE':
            ict_type = best_opportunity['ict_pattern'].get('pattern_type', 'ICT Pattern')
            detailed_narrative = (
                f"🔍 PATRÓN ICT: {ict_type} identificado con alta confianza. "
                f"Setup técnico sólido aunque sin confluencia POI adicional."
            )
        elif opportunity_type == 'POI_STANDALONE':
            poi_type = best_opportunity['poi'].get('type', 'POI')
            poi_grade = best_opportunity['poi'].get('grade', 'B')
            detailed_narrative = (
                f"📍 POI DESTACADO: {poi_type} (Grado {poi_grade}) presenta "
                f"oportunidad válida. Monitorear para confirmación adicional."
            )
        else:
            detailed_narrative = (
                "👁️ ANÁLISIS COMPLETO: No se detectaron setups de alta confianza. "
                "Mercado en consolidación, mantener observación."
            )

        # Action Plan (Específico por grade)
        action_plans = {
            'A+': f"🚀 {grade_config['action']}: Proceder con operación, confianza máxima.",
            'A': f"✅ {grade_config['action']}: Evaluar condiciones adicionales antes de proceder.",
            'B': f"👀 {grade_config['action']}: Esperar confirmación adicional. Riesgo limitado.",
            'C': f"⏳ {grade_config['action']}: Condiciones marginales. Evitar hasta mejora.",
            'D': f"📊 {grade_config['action']}: Sin setups válidos. Mantener análisis continuo."
        }

        action_plan = action_plans.get(final_grade, action_plans['D'])

        return {
            'primary_signal': primary_signal,
            'detailed_narrative': detailed_narrative,
            'action_plan': action_plan
        }

    def _generate_fallback_veredicto(self, current_price: float) -> Dict:
        """
        Genera veredicto de fallback en caso de error.
        """
        log_veredicto("WARNING", "⚠️ Generando veredicto de fallback")

        return {
            'timestamp': datetime.now().isoformat(),
            'setup_grade': 'D',
            'confidence_score': 0.1,
            'primary_signal': '🔍 Sistema reiniciando análisis - Datos temporalmente no disponibles',
            'detailed_narrative': 'El sistema está recalibrando el análisis de mercado. Mantener observación.',
            'action_plan': '📊 OBSERVAR: Esperar a que el sistema complete el análisis.',
            'risk_suggestion': 0.0,
            'best_pattern': None,
            'best_poi': None,
            'opportunity_type': 'SYSTEM_RESET',
            'dashboard_ready': True
        }

    # MÉTODO DE RETROCOMPATIBILIDAD (temporal)
    def generate_market_veredicto_legacy(self, enhanced_pois: List[Dict],
                                       market_context: Optional[Dict] = None,
                                       current_price: float = 0.0) -> Dict:
        """
        Método de retrocompatibilidad para mantener funcionamiento
        durante la transición. Llama al nuevo método con lista vacía de patrones ICT.
        """
        log_veredicto("WARNING", "🔄 Usando método legacy - actualizar a nuevo signature")
        return self.generate_market_veredicto(
            enhanced_pois=enhanced_pois,
            ict_patterns=[],  # Lista vacía hasta integración completa
            market_context=market_context,
            current_price=current_price
        )
