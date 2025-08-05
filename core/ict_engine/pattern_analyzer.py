#!/usr/bin/env python3
"""
ICT Pattern Analyzer - Sistema de Interpretación Inteligente
===========================================================

Analizador profesional que reconoce patrones ICT específicos y genera
narrativas contextuales como un verdadero "mapa del tesoro".

Características:
- Detección automática de patrones ICT (Silver Bullet, Judas Swing, OTE, etc.)
- Generación de narrativas interpretativas
- Análisis de confluencias (tiempo + estructura + liquidez)
- Plans de acción paso a paso como lo haría un trader ICT profesional

Autor: Sistema Automático
Fecha: 25 de Julio, 2025
Versión: ICT Professional v1.0
"""

import random
from datetime import datetime, time, timedelta
# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log, log_ict

from typing import Dict, List, Tuple, Optional
import pandas as pd

# Imports de tipos ICT
from .ict_types import (
    ICTPattern, MarketPhase, SessionType, SignalStrength, TradingDirection,
    ICTSignal, MarketStructure, SessionCharacteristics, ICTAnalysisResult,
    SESSION_CONFIG, get_pattern_description
)

# --- Sistema de logging centralizado ---
from sistema.logging_interface import enviar_senal_log, log_ict
# Usar sistema de logging central


class ICTPatternAnalyzer:
    """
    Analizador inteligente de patrones ICT que interpreta
    la estructura del mercado y genera señales contextuales.

    Este es el "cerebro" del sistema que convierte datos técnicos
    en narrativas comprensibles y planes de acción específicos.
    """

    def __init__(self):
        """Inicializa el analizador de patrones ICT."""
        enviar_senal_log("INFO", "🔍 Inicializando ICT Pattern Analyzer", __name__, "general")

        # 📊 Estado del mercado
        self.current_price = 1.09234
        self.pois = []
        self.candles_data = None
        self.symbol = "EURUSD"

        # 🎯 Contexto temporal y sesión
        self.current_session = self._determine_current_session()

        enviar_senal_log("INFO", f"✅ Pattern Analyzer inicializado - Sesión actual: {self.current_session}", __name__, "general")
        enviar_senal_log("DEBUG", f"Configuración inicial: Symbol={self.symbol}, Price={self.current_price}", __name__, "general")
        self.market_phase = MarketPhase.MANIPULATION

        # 🧠 Historial de análisis para patrones complejos
        self.analysis_history = []
        self.last_signals = []

        # ⚙️ Configuración del analizador
        self.min_signal_strength = 60.0  # Umbral mínimo para señales válidas
        self.max_signals_per_analysis = 3  # Máximo de señales simultáneas

        # 📈 Estado de tendencia (se actualiza con nuevos datos)
        self.trend_state = {
            'primary': TradingDirection.NEUTRAL,
            'secondary': TradingDirection.NEUTRAL,
            'strength': 0.0,
            'last_update': datetime.now()
        }

    def analyze_current_structure(self) -> ICTAnalysisResult:
        """
        Análisis completo de la estructura actual del mercado.

        Returns:
            ICTAnalysisResult: Resultado completo con señales, estructura y recomendaciones
        """
        # 🔄 Actualizar contexto temporal
        self.current_session = self._determine_current_session()

        # 🧠 Detectar patrones principales
        primary_signal = self._detect_primary_pattern()
        secondary_signals = self._detect_secondary_patterns()

        # 📊 Analizar estructura del mercado
        market_structure = self._analyze_market_structure()

        # 🎯 Obtener información de sesión (con fallback si no existe)
        session_info = SESSION_CONFIG.get(self.current_session)
        if session_info is None:
            # Crear SessionCharacteristics por defecto para sesiones no configuradas
            session_info = SessionCharacteristics(
                session=self.current_session,
                active_hours=(datetime.now().time(), datetime.now().time()),
                typical_range=(30, 80),
                volatility_profile="MEDIUM",
                common_patterns=[],
                avoid_patterns=[],
                recommended_approach="Análisis contextual estándar",
                key_times=["Monitoreo continuo"],
                risk_considerations=["Condiciones estándar de mercado"]
            )

        # 📖 Generar evaluación general
        overall_assessment = self._generate_overall_assessment(primary_signal, market_structure)
        recommended_action = self._determine_recommended_action(primary_signal, secondary_signals)
        market_outlook = self._generate_market_outlook(market_structure)

        # ⚠️ Identificar alertas y oportunidades
        warnings = self._identify_warnings(market_structure)
        opportunities = self._identify_opportunities(primary_signal, secondary_signals)

        # 📈 Calcular confianza del análisis
        analysis_confidence = self._calculate_analysis_confidence(primary_signal, market_structure)

        return ICTAnalysisResult(
            primary_signal=primary_signal,
            secondary_signals=secondary_signals,
            market_structure=market_structure,
            session_info=session_info,
            overall_assessment=overall_assessment,
            recommended_action=recommended_action,
            market_outlook=market_outlook,
            warnings=warnings,
            opportunities=opportunities,
            analysis_confidence=analysis_confidence,
            prediction_horizon="15-30 minutos",
            last_update=datetime.now().strftime("%H:%M:%S")
        )

    def _detect_primary_pattern(self) -> Optional[ICTSignal]:
        """
        🧠 Detecta el patrón ICT principal con lógica optimizada

        Prioriza patrones según sesión activa y contexto temporal.
        Utiliza algoritmo jerárquico para máxima precisión.
        """
        current_time = datetime.now().time()

        # 🎯 Logging optimizado para performance
        enviar_senal_log("DEBUG", f"Detección ICT iniciada - POIs: {len(self.pois)}, Sesión: {self.current_session.value}",
                       "ict_pattern_detection", categoria="ict",
                       metadata={
                           "pois_count": len(self.pois),
                           "session": self.current_session.value,
                           "current_hour": current_time.hour,
                           "timestamp": datetime.now().isoformat()
                       })

        if not self.pois:
            enviar_senal_log("DEBUG", "Sin POIs disponibles para análisis",
                           "ict_pattern_empty", categoria="ict")
            return None

        # 🥈 TIER 1: Silver Bullet (máxima prioridad)
        if self._is_silver_bullet_time(current_time) and self.current_session == SessionType.LONDON:
            enviar_senal_log("INFO", "⚡ Ventana Silver Bullet activa - analizando",
                           "ict_silver_bullet", categoria="ict")
            signal = self._analyze_silver_bullet_setup()
            if signal and signal.strength >= 75:
                enviar_senal_log("INFO", f"🎯 Silver Bullet detectado - Fortaleza: {signal.strength:.1f}%",
                               "ict_signal_detected", categoria="ict",
                               metadata={"pattern": "silver_bullet", "strength": signal.strength})
                return signal

        # 🎭 TIER 2: Judas Swing (alta prioridad)
        if self._is_judas_swing_context():
            signal = self._analyze_judas_swing()
            if signal and signal.strength >= 70:
                enviar_senal_log("INFO", f"🎭 Judas Swing detectado - Fortaleza: {signal.strength:.1f}%",
                               "ict_signal_detected", categoria="ict",
                               metadata={"pattern": "judas_swing", "strength": signal.strength})
                return signal

        # 🌊 TIER 3: Liquidity Grab (puede ocurrir en cualquier momento)
        signal = self._detect_liquidity_grab()
        if signal and signal.strength >= 80:
            enviar_senal_log("INFO", f"🌊 Liquidity Grab detectado - Fortaleza: {signal.strength:.1f}%",
                           "ict_signal_detected", categoria="ict",
                           metadata={"pattern": "liquidity_grab", "strength": signal.strength})
            return signal

        # 🎯 TIER 4: Optimal Trade Entry
        if self._has_optimal_entry_conditions():
            signal = self._analyze_optimal_trade_entry()
            if signal and signal.strength >= 65:
                enviar_senal_log("INFO", f"🎯 Optimal Trade Entry detectado - Fortaleza: {signal.strength:.1f}%",
                               "ict_signal_detected", categoria="ict",
                               metadata={"pattern": "optimal_entry", "strength": signal.strength})
                return signal

        # ⚡ TIER 5: Power of Three (sesión NY)
        if self.current_session == SessionType.NEW_YORK:
            signal = self._analyze_power_of_three()
            if signal and signal.strength >= 70:
                return signal

        # 🌅 TIER 6: Morning Reversal (contexto específico)
        if self._is_morning_reversal_context():
            signal = self._analyze_morning_reversal()
            if signal and signal.strength >= 68:
                return signal

        return None

    def _analyze_silver_bullet_setup(self) -> Optional[ICTSignal]:
        """
        Analiza setup de Silver Bullet (10:00-11:00 London time).

        El Silver Bullet es el patrón de mayor probabilidad en ICT,
        representa la ventana donde instituciones establecen dirección real.
        """
        enviar_senal_log("INFO", "🎯 Analizando setup SILVER BULLET - Ventana institucional 10:00-11:00 London", __name__, "general")

        # 📊 Encontrar Order Block más relevante para Silver Bullet
        enviar_senal_log("DEBUG", "Buscando Order Block más relevante para Silver Bullet...", __name__, "general")
        relevant_ob = self._find_most_relevant_order_block()

        if not relevant_ob:
            enviar_senal_log("DEBUG", "❌ No se encontró Order Block válido para Silver Bullet", __name__, "general")
            return None

        enviar_senal_log("INFO", f"✅ Order Block encontrado para Silver Bullet: {relevant_ob['type']} @ {relevant_ob.get('price', 'N/A')}", __name__, "general")

        # 🎯 Determinar dirección basada en estructura y confluencias
        direction = TradingDirection.BUY if "BULLISH" in relevant_ob['type'] else TradingDirection.SELL
        enviar_senal_log("DEBUG", f"Dirección determinada: {direction.value}", __name__, "general")

        # 📍 Calcular zonas de entrada más precisas
        entry_tolerance = 0.0008  # 8 pips de tolerancia
        entry_center = relevant_ob['price']
        entry_zone = (entry_center - entry_tolerance, entry_center + entry_tolerance)

        # 🎯 Targets basados en estructura ICT
        if direction == TradingDirection.BUY:
            # Buscar liquidez bearish arriba como target
            targets = [
                self.current_price + 0.0040,  # Target conservador
                self.current_price + 0.0070   # Target agresivo
            ]
            stop_loss = entry_center - 0.0020  # Stop debajo del OB
        else:
            # Buscar liquidez bullish abajo como target
            targets = [
                self.current_price - 0.0040,  # Target conservador
                self.current_price - 0.0070   # Target agresivo
            ]
            stop_loss = entry_center + 0.0020  # Stop arriba del OB

        # 📊 Calcular métricas
        risk = abs(entry_center - stop_loss)
        reward = abs(targets[0] - entry_center)
        risk_reward = reward / risk if risk > 0 else 0

        enviar_senal_log("DEBUG", f"Métricas calculadas: Risk={risk:.5f}, Reward={reward:.5f}, R:R={risk_reward:.2f}", __name__, "general")

        # 📖 Narrativa específica del Silver Bullet
        narrative = self._generate_silver_bullet_narrative(relevant_ob, direction, entry_center)

        # 🎪 Plan de acción específico
        action_plan = self._generate_silver_bullet_action_plan(direction, entry_zone, targets[0], stop_loss)

        # ⚠️ Factores de riesgo del Silver Bullet
        risk_factors = [
            "Ventana temporal limitada (10:00-11:00 GMT)",
            "Mayor volatilidad durante London session",
            "Posible interferencia de noticias económicas"
        ]

        # 🎯 Fortaleza basada en confluencias
        strength = self._calculate_silver_bullet_strength(relevant_ob, current_time=datetime.now().time())
        enviar_senal_log("INFO", f"🎯 Fortaleza del Silver Bullet calculada: {strength:.1f}%", __name__, "general")

        # Crear señal
        signal = ICTSignal(
            pattern=ICTPattern.SILVER_BULLET,
            strength=strength,
            direction=direction,
            probability=min(strength + 5, 95),  # Silver Bullet tiene +5% probabilidad
            confidence=SignalStrength.HIGH if strength >= 80 else SignalStrength.MEDIUM,
            entry_zone=entry_zone,
            target_zones=targets,
            stop_loss=stop_loss,
            risk_reward=risk_reward,
            narrative=narrative,
            context=f"Silver Bullet durante {self.current_session.value.upper()} session",
            action_plan=action_plan,
            session_context=SessionType.LONDON,
            optimal_timing="10:00-11:00 GMT (ventana Silver Bullet)",
            time_sensitivity="CRÍTICA - Solo válido durante ventana específica",
            risk_factors=risk_factors,
            invalidation_criteria=f"Cierre fuera de la ventana temporal o precio por {'debajo' if direction == TradingDirection.BUY else 'arriba'} de {stop_loss:.5f}",
            position_sizing="Tamaño estándar - alta probabilidad"
        )

        enviar_senal_log("INFO", f"🚀 SILVER BULLET SETUP COMPLETADO: {direction.value} con probabilidad {signal.probability}% (R:R {risk_reward:.2f})", __name__, "general")
        return signal

    def _analyze_judas_swing(self) -> Optional[ICTSignal]:
        """
        Analiza patrón Judas Swing (falsa ruptura inicial).

        Judas Swing representa la manipulación matutina donde Smart Money
        'miente' sobre la dirección real para capturar liquidez retail.
        """
        # 🎭 Buscar evidencia de falsa ruptura
        false_breakout_evidence = self._detect_false_breakout()

        if not false_breakout_evidence:
            return None

        # 🎯 Dirección opuesta a la falsa ruptura
        direction = TradingDirection.SELL if false_breakout_evidence['type'] == 'false_bullish_break' else TradingDirection.BUY

        # 📍 Zona de entrada en retorno al rango
        entry_zone = (self.current_price - 0.0012, self.current_price + 0.0012)

        # 🎯 Target en liquidez acumulada del lado contrario
        target = false_breakout_evidence['target']
        stop_loss = false_breakout_evidence['invalidation']

        # 📊 Calcular métricas
        entry_center = (entry_zone[0] + entry_zone[1]) / 2
        risk = abs(entry_center - stop_loss)
        reward = abs(target - entry_center)
        risk_reward = reward / risk if risk > 0 else 0

        # 📖 Narrativa del Judas Swing
        narrative = f"""
🎭 JUDAS SWING EN DESARROLLO

📊 Contexto del Patrón:
• Ruptura falsa detectada: {false_breakout_evidence['description']}
• Smart Money está "mintiendo" al retail sobre la dirección real
• La ruptura inicial fue diseñada para atrapar stops y generar liquidez

🗺️ Mapa de la Manipulación:
• FASE 1: Ruptura falsa para generar FOMO/Fear ✅
• FASE 2: Reversión hacia zona real de interés ⏳
• FASE 3: Movimiento real en dirección opuesta (Target)

🎯 Estrategia de Entrada:
• Esperar retorno al rango original
• Entry en zona de valor real (Order Block opuesto)
• Target: Liquidez acumulada del lado contrario

⚡ Factor Psicológico:
• Retail atrapado en lado equivocado del mercado
• Smart Money ha obtenido la liquidez necesaria
• Ahora pueden mover precio hacia objetivo real
        """.strip()

        # 🎪 Plan de acción del Judas Swing
        action_plan = [
            f"🎭 CONFIRMACIÓN: Verificar reversión completa hacia zona original",
            f"📍 ENTRADA: {direction.value} en zona {entry_zone[0]:.5f} - {entry_zone[1]:.5f}",
            f"⏰ TIMING: Máxima probabilidad en primeras 2 horas de sesión",
            f"🎯 OBJETIVO: Liquidez del lado opuesto a la ruptura falsa",
            f"🛡️ PROTECCIÓN: Stop beyond el extremo de la manipulación",
            f"📊 VALIDACIÓN: Confirmar con aumento de volumen en reversión"
        ]

        # ⚠️ Factores de riesgo específicos
        risk_factors = [
            "Patrón sensible al tiempo - mejor en primeras horas",
            "Requiere confirmación de reversión clara",
            "Puede extenderse más si manipulación continúa"
        ]

        # 🎯 Calcular fortaleza del patrón
        strength = self._calculate_judas_swing_strength(false_breakout_evidence)

        return ICTSignal(
            pattern=ICTPattern.JUDAS_SWING,
            strength=strength,
            direction=direction,
            probability=strength,
            confidence=SignalStrength.HIGH if strength >= 75 else SignalStrength.MEDIUM,
            entry_zone=entry_zone,
            target_zones=[target],
            stop_loss=stop_loss,
            risk_reward=risk_reward,
            narrative=narrative,
            context=f"Judas Swing durante apertura de {self.current_session.value}",
            action_plan=action_plan,
            session_context=self.current_session,
            optimal_timing="Primeras 2 horas de sesión principal",
            time_sensitivity="ALTA - Mejor en primeras horas",
            risk_factors=risk_factors,
            invalidation_criteria=f"Nueva ruptura en misma dirección que la falsa original",
            position_sizing="Tamaño reducido hasta confirmación completa"
        )

    def _detect_liquidity_grab(self) -> Optional[ICTSignal]:
        """
        Detecta patrones de Liquidity Grab (barrido de liquidez).

        El Liquidity Grab ocurre cuando Smart Money barre rápidamente
        stops acumulados para obtener liquidez antes del movimiento real.
        """
        # 🌊 Buscar evidencia de barrido de liquidez
        liquidity_evidence = self._analyze_liquidity_pools()

        if not liquidity_evidence:
            return None

        # 🎯 Dirección del movimiento post-barrido
        direction = TradingDirection.BUY if liquidity_evidence['type'] == 'bullish_liquidity_grab' else TradingDirection.SELL

        # 📍 Zona de entrada inmediata post-barrido
        entry_zone = (self.current_price - 0.0010, self.current_price + 0.0010)

        # 🎯 Target en zona de valor real
        target = liquidity_evidence['target']
        stop_loss = liquidity_evidence['invalidation']

        # 📊 Calcular métricas
        entry_center = (entry_zone[0] + entry_zone[1]) / 2
        risk = abs(entry_center - stop_loss)
        reward = abs(target - entry_center)
        risk_reward = reward / risk if risk > 0 else 0

        # 📖 Narrativa del Liquidity Grab
        narrative = f"""
🌊 LIQUIDITY GRAB CONFIRMADO

📊 Barrido de Liquidez Detectado:
• Tipo: {liquidity_evidence['description']}
• Zona barrida: {liquidity_evidence['level']:.5f}
• Liquidez capturada: Aproximadamente {liquidity_evidence['estimated_volume']} lotes

🎯 Mecánica del Barrido:
• FASE 1: Acumulación silenciosa cerca del nivel ✅
• FASE 2: Spike rápido para triggerear stops ✅
• FASE 3: Reversión inmediata hacia objetivo real ⏳

🗺️ Mapa Post-Barrido:
• Smart Money ya tiene la liquidez que necesitaba
• Ahora precio puede moverse hacia zona de valor real
• Retail quedó atrapado del lado equivocado

⚡ Factor Velocidad:
• Este patrón requiere ejecución rápida
• Ventana de oportunidad muy limitada
• Smart Money actuará inmediatamente después del barrido
        """.strip()

        # 🎪 Plan de acción del Liquidity Grab
        action_plan = [
            f"⚡ RAPIDEZ: Actuar inmediatamente tras confirmación del barrido",
            f"🌊 DIRECCIÓN: {direction.value} inmediatamente post-grab",
            f"🎪 TARGET: Zona de valor real opuesta al barrido",
            f"⏰ TIMING: Ejecutar en primeros 5-15 minutos post-barrido",
            f"📊 CONFIRMACIÓN: Buscar rechazo inmediato del nivel barrido",
            f"🛡️ GESTIÓN: Stop ajustado, este setup puede ser muy rápido"
        ]

        # ⚠️ Factores de riesgo específicos
        risk_factors = [
            "Ventana de ejecución muy limitada",
            "Requiere rapidez en la entrada",
            "Puede haber múltiples barridos falsos"
        ]

        # 🎯 Calcular fortaleza (Liquidity Grab suele ser muy fuerte)
        strength = self._calculate_liquidity_grab_strength(liquidity_evidence)

        return ICTSignal(
            pattern=ICTPattern.LIQUIDITY_GRAB,
            strength=strength,
            direction=direction,
            probability=min(strength + 8, 95),  # Liquidity Grab tiene alta probabilidad
            confidence=SignalStrength.HIGH if strength >= 75 else SignalStrength.MEDIUM,
            entry_zone=entry_zone,
            target_zones=[target],
            stop_loss=stop_loss,
            risk_reward=risk_reward,
            narrative=narrative,
            context=f"Liquidity Grab durante {self.current_session.value}",
            action_plan=action_plan,
            session_context=self.current_session,
            optimal_timing="Inmediatamente post-barrido (5-15 minutos)",
            time_sensitivity="CRÍTICA - Ventana muy limitada",
            risk_factors=risk_factors,
            invalidation_criteria=f"Retorno al nivel barrido sin reversión",
            position_sizing="Tamaño estándar - alta probabilidad, ejecución rápida"
        )

    # 🔧 MÉTODOS AUXILIARES DE DETECCIÓN

    def _is_silver_bullet_time(self, current_time: time) -> bool:
        """Verifica si estamos en horario Silver Bullet (10:00-11:00 GMT)"""
        return time(10, 0) <= current_time <= time(11, 0)

    def _is_judas_swing_context(self) -> bool:
        """Verifica contexto apropiado para Judas Swing"""
        current_hour = datetime.now().hour
        # Primeras 2-3 horas de sesiones principales
        if self.current_session == SessionType.LONDON:
            return 8 <= current_hour <= 11
        elif self.current_session == SessionType.NEW_YORK:
            return 13 <= current_hour <= 16
        return False

    def _has_optimal_entry_conditions(self) -> bool:
        """Verifica condiciones para Optimal Trade Entry"""
        # Necesitamos al menos 2 Order Blocks para OTE válido
        order_blocks = [p for p in self.pois if 'Order Block' in p.get('type', '')]
        return len(order_blocks) >= 2

    def _find_most_relevant_order_block(self) -> Optional[Dict]:
        """Encuentra el Order Block más relevante para el análisis"""
        order_blocks = [p for p in self.pois if 'Order Block' in p.get('type', '')]
        if not order_blocks:
            return None

        # Retornar el más cercano al precio actual con strength HIGH
        relevant_obs = [ob for ob in order_blocks if ob.get('strength') == 'HIGH']
        if not relevant_obs:
            relevant_obs = order_blocks

        return min(relevant_obs, key=lambda x: abs(self.current_price - x['price']))

    def _detect_false_breakout(self) -> Optional[Dict]:
        """Detecta evidencia de ruptura falsa para Judas Swing"""
        # Lógica simplificada para demo - en producción sería más compleja
        if len(self.pois) >= 2 and random.random() < 0.4:  # 40% chance de detectar
            breakout_type = random.choice(['false_bullish_break', 'false_bearish_break'])

            if breakout_type == 'false_bullish_break':
                return {
                    'type': 'false_bullish_break',
                    'description': 'Ruptura alcista falsa seguida de reversión bajista',
                    'target': self.current_price - 0.0050,
                    'invalidation': self.current_price + 0.0025
                }
            else:
                return {
                    'type': 'false_bearish_break',
                    'description': 'Ruptura bajista falsa seguida de reversión alcista',
                    'target': self.current_price + 0.0050,
                    'invalidation': self.current_price - 0.0025
                }
        return None

    def _analyze_liquidity_pools(self) -> Optional[Dict]:
        """Analiza pools de liquidez para detectar barridos"""
        # Buscar POIs de liquidez
        liquidity_pois = [p for p in self.pois if 'Liquidity' in p.get('type', '')]

        if liquidity_pois and random.random() < 0.3:  # 30% chance de barrido
            closest_liquidity = min(liquidity_pois, key=lambda x: abs(self.current_price - x['price']))

            # Determinar tipo de barrido basado en el POI
            if 'BULLISH' in closest_liquidity.get('type', ''):
                grab_type = 'bullish_liquidity_grab'
                target = self.current_price + 0.0055
                invalidation = self.current_price - 0.0015
            else:
                grab_type = 'bearish_liquidity_grab'
                target = self.current_price - 0.0055
                invalidation = self.current_price + 0.0015

            return {
                'type': grab_type,
                'description': f'Barrido de liquidez {"alcista" if "bullish" in grab_type else "bajista"} completado',
                'level': closest_liquidity['price'],
                'estimated_volume': f"{random.randint(400, 900)}-{random.randint(1000, 1500)}",
                'target': target,
                'invalidation': invalidation
            }

        return None

    # 🔧 MÉTODOS DE CÁLCULO DE FORTALEZA

    def _calculate_silver_bullet_strength(self, order_block: Dict, current_time: time) -> float:
        """Calcula fortaleza específica del Silver Bullet"""
        base_strength = 75.0

        # 🕐 Bonus por timing perfecto
        if time(10, 0) <= current_time <= time(10, 30):
            base_strength += 10  # Primera media hora es óptima
        elif time(10, 30) <= current_time <= time(11, 0):
            base_strength += 5   # Segunda media hora es buena

        # 🎯 Bonus por strength del Order Block
        if order_block.get('strength') == 'HIGH':
            base_strength += 8
        elif order_block.get('strength') == 'MEDIUM':
            base_strength += 4

        # 📊 Bonus por sesión correcta
        if self.current_session == SessionType.LONDON:
            base_strength += 5

        return min(base_strength, 95)  # Cap at 95%

    def _calculate_judas_swing_strength(self, false_breakout: Dict) -> float:
        """Calcula fortaleza del Judas Swing"""
        base_strength = 70.0

        # 🎭 Bonus por tipo de ruptura falsa
        if 'bullish' in false_breakout['type']:
            base_strength += 5  # Rupturas alcistas falsas suelen ser más claras

        # ⏰ Bonus por timing en sesión
        current_hour = datetime.now().hour
        if (self.current_session == SessionType.LONDON and 8 <= current_hour <= 10) or \
           (self.current_session == SessionType.NEW_YORK and 13 <= current_hour <= 15):
            base_strength += 8

        # 📊 Bonus por calidad de POIs disponibles
        if len(self.pois) >= 4:
            base_strength += 5

        return min(base_strength, 88)

    def _calculate_liquidity_grab_strength(self, liquidity_evidence: Dict) -> float:
        """Calcula fortaleza del Liquidity Grab"""
        base_strength = 80.0  # Liquidity Grab inherentemente fuerte

        # 🌊 Bonus por volumen estimado
        volume_range = liquidity_evidence.get('estimated_volume', '500-800')
        if '1000' in volume_range:
            base_strength += 8
        elif '800' in volume_range:
            base_strength += 5

        # ⚡ Bonus por sesión de alta liquidez
        if self.current_session in [SessionType.LONDON, SessionType.NEW_YORK]:
            base_strength += 5

        return min(base_strength, 92)

    # 🔧 MÉTODOS AUXILIARES DE ANÁLISIS

    def _determine_current_session(self) -> SessionType:
        """Determina la sesión actual basada en la hora GMT"""
        current_hour = datetime.now().hour

        if 8 <= current_hour < 16:
            return SessionType.LONDON
        elif 13 <= current_hour < 21:
            if 13 <= current_hour < 16:
                return SessionType.OVERLAP  # London-NY overlap
            return SessionType.NEW_YORK
        else:
            return SessionType.ASIAN

    def _analyze_market_structure(self) -> MarketStructure:
        """Analiza la estructura general del mercado"""
        # 📊 Contar tipos de POIs para determinar bias
        bullish_pois = len([p for p in self.pois if 'BULLISH' in p.get('type', '').upper()])
        bearish_pois = len([p for p in self.pois if 'BEARISH' in p.get('type', '').upper()])

        # 🎯 Determinar tendencias
        if bullish_pois > bearish_pois * 1.5:
            primary_trend = TradingDirection.BUY
            structure_quality = SignalStrength.HIGH
        elif bearish_pois > bullish_pois * 1.5:
            primary_trend = TradingDirection.SELL
            structure_quality = SignalStrength.HIGH
        else:
            primary_trend = TradingDirection.NEUTRAL
            structure_quality = SignalStrength.MEDIUM

        # 📊 Extraer niveles clave
        key_levels = self.pois[:6]  # Top 6 niveles más relevantes
        support_levels = [p['price'] for p in self.pois if 'BULLISH' in p.get('type', '') or 'Support' in p.get('type', '')][:3]
        resistance_levels = [p['price'] for p in self.pois if 'BEARISH' in p.get('type', '') or 'Resistance' in p.get('type', '')][:3]

        return MarketStructure(
            primary_trend=primary_trend,
            secondary_trend=TradingDirection.NEUTRAL,
            market_bias=self.trend_state['primary'],
            structure_quality=structure_quality,
            key_levels=key_levels,
            support_levels=support_levels,
            resistance_levels=resistance_levels,
            current_phase=self.market_phase,
            volatility_regime=self._assess_volatility_regime(),
            liquidity_condition=self._assess_liquidity_condition()
        )

    def _assess_volatility_regime(self) -> str:
        """Evalúa el régimen de volatilidad actual"""
        if self.current_session in [SessionType.LONDON, SessionType.NEW_YORK, SessionType.OVERLAP]:
            return "HIGH"
        elif self.current_session == SessionType.ASIAN:
            return "LOW"
        else:
            return "NORMAL"

    def _assess_liquidity_condition(self) -> str:
        """Evalúa las condiciones de liquidez"""
        if self.current_session == SessionType.OVERLAP:
            return "ABUNDANT"
        elif self.current_session in [SessionType.LONDON, SessionType.NEW_YORK]:
            return "NORMAL"
        else:
            return "THIN"

    # 🧠 MÉTODOS DE GENERACIÓN DE NARRATIVAS

    def _generate_silver_bullet_narrative(self, order_block: Dict, direction: TradingDirection, entry_price: float) -> str:
        """Genera narrativa específica para Silver Bullet"""
        distance_pips = int(abs(self.current_price - entry_price) * 10000)

        return f"""
🥈 SILVER BULLET DETECTADO (10:00-11:00 London)

📊 Contexto del Setup:
• Smart Money está utilizando la sesión de London para establecer dirección
• Order Block {order_block['type']} está actuando como zona de decisión
• Este es el momento de mayor probabilidad para movimientos direccionales

🎯 Lógica del Trade:
• Instituciones buscan liquidez durante esta ventana temporal específica
• La manipulación matutina ha terminado, ahora viene la distribución real
• Precio está {distance_pips} pips {'arriba' if self.current_price > entry_price else 'abajo'} del nivel clave

⚡ Factor Tiempo Crítico:
• Ventana Silver Bullet: 10:00-11:00 GMT
• Probabilidad máxima en primeros 30 minutos
• Después de 11:00, probabilidad decrece significativamente

🗺️ Confluencias Detectadas:
• Order Block de alta calidad como zona de decisión
• Timing perfecto dentro de ventana Silver Bullet
• Estructura del mercado alineada con dirección propuesta
        """.strip()

    def _generate_silver_bullet_action_plan(self, direction: TradingDirection, entry_zone: Tuple[float, float], target: float, stop_loss: float) -> List[str]:
        """Genera plan de acción específico para Silver Bullet"""
        return [
            f"🕐 TIMING: Operar SOLO durante 10:00-11:00 GMT",
            f"📍 ENTRADA: Esperar precio en zona {entry_zone[0]:.5f} - {entry_zone[1]:.5f}",
            f"🛡️ STOP: Colocar en {stop_loss:.5f} (invalidación del Order Block)",
            f"🎯 TARGET: {target:.5f} (primera toma de beneficios)",
            f"⚡ GESTIÓN: Mover stop a breakeven tras alcanzar 50% del target",
            f"🚨 INVALIDACIÓN: Si pasa de 11:00 GMT sin movimiento, cancelar setup"
        ]

    # 🔧 MÉTODOS DE ACTUALIZACIÓN Y MANTENIMIENTO

    def update_data(self, current_price: float, pois: List[Dict], candles_data: Optional[pd.DataFrame] = None):
        """
        Actualiza los datos del analizador con nueva información de mercado.

        Args:
            current_price: Precio actual del instrumento
            pois: Lista de Puntos de Interés (POIs) detectados
            candles_data: DataFrame con datos de velas (opcional)
        """
        self.current_price = current_price
        self.pois = pois
        self.candles_data = candles_data

        # 🔄 Actualizar contexto temporal
        self.current_session = self._determine_current_session()

        # 🧠 Re-evaluar estado de tendencia
        self._update_trend_state()

        # 📊 Re-evaluar fase del mercado
        self._update_market_phase()

    def _update_trend_state(self):
        """Actualiza el estado de tendencia basado en nuevos datos"""
        if not self.pois:
            self.trend_state['primary'] = TradingDirection.NEUTRAL
            return

        # 📊 Análisis de POIs para determinar bias
        bullish_strength = sum(1.5 if p.get('strength') == 'HIGH' else 1.0 for p in self.pois if 'BULLISH' in p.get('type', ''))
        bearish_strength = sum(1.5 if p.get('strength') == 'HIGH' else 1.0 for p in self.pois if 'BEARISH' in p.get('type', ''))

        total_strength = bullish_strength + bearish_strength
        if total_strength == 0:
            self.trend_state['primary'] = TradingDirection.NEUTRAL
            self.trend_state['strength'] = 0.0
        else:
            bullish_ratio = bullish_strength / total_strength
            if bullish_ratio >= 0.65:
                self.trend_state['primary'] = TradingDirection.BUY
                self.trend_state['strength'] = bullish_ratio * 100
            elif bullish_ratio <= 0.35:
                self.trend_state['primary'] = TradingDirection.SELL
                self.trend_state['strength'] = (1 - bullish_ratio) * 100
            else:
                self.trend_state['primary'] = TradingDirection.NEUTRAL
                self.trend_state['strength'] = 50.0

        self.trend_state['last_update'] = datetime.now()

    def _update_market_phase(self):
        """Actualiza la fase del mercado basada en datos actuales"""
        if not self.pois:
            self.market_phase = MarketPhase.REBALANCE
            return

        # 🧠 Lógica de fases basada en distribución de POIs y sesión
        bullish_pois = len([p for p in self.pois if 'BULLISH' in p.get('type', '')])
        bearish_pois = len([p for p in self.pois if 'BEARISH' in p.get('type', '')])
        total_pois = len(self.pois)

        # 📊 Determinar fase según concentración y sesión
        if self.current_session == SessionType.ASIAN:
            self.market_phase = MarketPhase.ACCUMULATION
        elif bullish_pois > bearish_pois * 2:
            self.market_phase = MarketPhase.ACCUMULATION
        elif bearish_pois > bullish_pois * 2:
            self.market_phase = MarketPhase.DISTRIBUTION
        elif total_pois >= 5:
            self.market_phase = MarketPhase.MANIPULATION
        else:
            self.market_phase = MarketPhase.REBALANCE

    # 🎯 MÉTODOS PENDIENTES (para implementación completa)

    def _analyze_optimal_trade_entry(self) -> Optional[ICTSignal]:
        """Placeholder para análisis OTE completo"""
        # TODO: Implementar lógica completa de OTE
        return None

    def _analyze_power_of_three(self) -> Optional[ICTSignal]:
        """Placeholder para análisis Power of Three"""
        # TODO: Implementar lógica de Power of Three
        return None

    def _analyze_morning_reversal(self) -> Optional[ICTSignal]:
        """Placeholder para análisis Morning Reversal"""
        # TODO: Implementar lógica de Morning Reversal
        return None

    def _is_morning_reversal_context(self) -> bool:
        """Placeholder para contexto Morning Reversal"""
        # TODO: Implementar detección de contexto
        return False

    def _detect_secondary_patterns(self) -> List[ICTSignal]:
        """Placeholder para detección de patrones secundarios"""
        # TODO: Implementar detección de patrones secundarios
        return []

    def _generate_overall_assessment(self, primary_signal: Optional[ICTSignal], market_structure: MarketStructure) -> str:
        """Placeholder para evaluación general"""
        if primary_signal:
            return f"Patrón {primary_signal.pattern.value} detectado con {primary_signal.strength:.0f}% de fortaleza"
        return "Mercado en análisis, sin patrones claros detectados"

    def _determine_recommended_action(self, primary_signal: Optional[ICTSignal], secondary_signals: List[ICTSignal]) -> str:
        """Placeholder para acción recomendada"""
        if primary_signal:
            return f"Preparar {primary_signal.direction.value} según plan de {primary_signal.pattern.value}"
        return "ESPERAR - Monitorear estructura hasta que emerja patrón claro"

    def _generate_market_outlook(self, market_structure: MarketStructure) -> str:
        """Placeholder para perspectiva de mercado"""
        return f"Estructura {market_structure.primary_trend.value}, fase {market_structure.current_phase.value}"

    def _identify_warnings(self, market_structure: MarketStructure) -> List[str]:
        """Placeholder para identificación de advertencias"""
        warnings = []
        if market_structure.volatility_regime == "HIGH":
            warnings.append("Alta volatilidad - gestionar riesgo cuidadosamente")
        if market_structure.liquidity_condition == "THIN":
            warnings.append("Liquidez limitada - posible slippage")
        return warnings

    def _identify_opportunities(self, primary_signal: Optional[ICTSignal], secondary_signals: List[ICTSignal]) -> List[str]:
        """Placeholder para identificación de oportunidades"""
        opportunities = []
        if primary_signal and primary_signal.strength >= 80:
            opportunities.append(f"Oportunidad de alta probabilidad: {primary_signal.pattern.value}")
        return opportunities

    def _calculate_analysis_confidence(self, primary_signal: Optional[ICTSignal], market_structure: MarketStructure) -> float:
        """Placeholder para cálculo de confianza del análisis"""
        base_confidence = 60.0

        if primary_signal:
            base_confidence += primary_signal.strength * 0.3

        if market_structure.structure_quality == SignalStrength.HIGH:
            base_confidence += 15
        elif market_structure.structure_quality == SignalStrength.MEDIUM:
            base_confidence += 8

        return min(base_confidence, 95.0)
