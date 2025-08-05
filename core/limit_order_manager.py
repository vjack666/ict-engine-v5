"""
Limit Order Manager
==================

Módulo para gestionar órdenes límite automáticas basadas en análisis ICT y POI.
Puede crear, actualizar y cancelar órdenes límite según las condiciones del mercado.
"""

import MetaTrader5 as mt5
from datetime import datetime
from typing import Optional
import time

from sistema.config import SIMBOLO
# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log, log_trading

# RiskBot para cálculo dinámico de volumen
from core.risk_management.riskbot_mt5 import RiskBot

# MT5 Connector - Import condicional
mt5_connector_available = False
try:
    # Intentar import del conector personalizado
    from sistema.mt5_connector import inicializar_mt5, MT5Connector  # type: ignore
    mt5_connector_available = True
except ImportError:
    # Silenciar importación para evitar logging legacy
    MT5Connector = None

    def inicializar_mt5():
        """Fallback function when MT5 connector is not available"""
        try:
            # Usar método correcto de MetaTrader5
            if mt5:
                return mt5.initialize()  # type: ignore
            return False
        except (AttributeError, Exception):
            # mt5.initialize() puede no estar disponible o fallar
            return False

# 🔧 Silenciar advertencias MT5 del linter (falsos positivos)
# pylint: disable=no-member
# Usar sistema de logging central


class LimitOrderManager:
    """
    Gestor de órdenes límite automáticas DUAL.

    Funcionalidades:
    - Ejecutar AMBAS estrategias simultáneamente (CONSERVADORA + AGRESIVA)
    - Crear órdenes buy/sell limit en puntos óptimos
    - Actualizar órdenes existentes si cambian las condiciones
    - Cancelar órdenes que ya no son válidas
    - Gestionar múltiples órdenes simultáneamente
    - Comentarios específicos por estrategia en MT5
    """

    _instance = None
    _initialized = False

    def __new__(cls, symbol: str = SIMBOLO):
        """Implementación singleton para evitar reinicializaciones."""
        if cls._instance is None:
            cls._instance = super(LimitOrderManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, symbol: str = SIMBOLO):
        # Evitar reinicialización si ya está configurado
        if self._initialized:
            return

        self.symbol = symbol
        self.active_orders = {}  # Almacena órdenes activas
        self.last_analysis = {}  # Último análisis para comparar cambios
        self.update_threshold_pips = 10  # Umbral mínimo para actualizar órdenes (en pips)
        self.max_orders = 4  # Máximo número de órdenes pendientes (2 conservadoras + 2 agresivas)

        # 🔍 DIAGNÓSTICO MT5 API - Verificar métodos disponibles
        self._diagnose_mt5_api()

        # Configuración de órdenes
        self.default_volume = 0.05  # Volumen base (será sobrescrito por cálculo dinámico)
        self.magic_number_conservative = 123456  # Bot conservador
        self.magic_number_aggressive = 654321   # Bot agresivo

        # RiskBot para cálculo dinámico de volumen
        try:
            self.riskbot = RiskBot()
            enviar_senal_log("INFO", "RiskBot integrado para volumen dinámico", __name__, "trading")
        except Exception as e:
            enviar_senal_log("WARNING", f"Error inicializando RiskBot: {e}, usando volumen fijo", __name__, "trading")
            self.riskbot = None

        # Estrategias habilitadas
        self.conservative_enabled = True
        self.aggressive_enabled = True

        # Sistema de logging migrado a SLUC v2.0 - SOLO LA PRIMERA VEZ
        enviar_senal_log("INFO", "Gestor DUAL de órdenes límite inicializado (CONSERVADOR + AGRESIVO)", __name__, "trading")
        enviar_senal_log("INFO", "SIN SL/TP automáticos - RiskBot y Bollinger gestionan riesgo", __name__, "trading")

        # Mostrar volumen dinámico inicial
        initial_volume = self.get_dynamic_volume()
        enviar_senal_log("INFO", f"Volumen dinámico inicial: {initial_volume} lotes", __name__, "trading")

        # Marcar como inicializado
        self._initialized = True

    def get_dynamic_volume(self) -> float:
        """
        Obtiene volumen dinámico basado en balance y riesgo.

        Returns:
            float: Volumen calculado dinámicamente o volumen por defecto si hay error
        """
        try:
            if self.riskbot:
                # Usar 1% del balance para cálculo de volumen
                dynamic_vol = self.riskbot.calcular_volumen_dinamico(
                    balance_pct=1.0,  # 1% del balance
                    max_volume=0.50,  # Máximo 0.5 lotes
                    min_volume=0.01   # Mínimo 0.01 lotes
                )
                enviar_senal_log("DEBUG", f"Volumen dinámico: {dynamic_vol} (vs fijo: {self.default_volume})", __name__, "trading")
                return dynamic_vol
            else:
                return self.default_volume
        except Exception as e:
            enviar_senal_log("ERROR", f"Error calculando volumen dinámico: {e}", __name__, "trading")
            return self.default_volume

    def _diagnose_mt5_api(self):
        """🔍 DIAGNÓSTICO: Verificar métodos MT5 disponibles"""
        try:
            mt5_methods = [attr for attr in dir(mt5) if not attr.startswith('_')]
            enviar_senal_log("DEBUG", f"Métodos MT5 disponibles: {mt5_methods}", __name__, "mt5")

            # Verificar métodos críticos
            critical_methods = ['symbol_info', 'order_send', 'orders_get', 'positions_get']
            for method in critical_methods:
                if hasattr(mt5, method):
                    enviar_senal_log("DEBUG", f"✅ MT5.{method} DISPONIBLE", __name__, "mt5")
                else:
                    enviar_senal_log("WARNING", f"❌ MT5.{method} NO DISPONIBLE", __name__, "mt5")

        except Exception as e:
            enviar_senal_log("ERROR", f"Error en diagnóstico MT5: {e}", __name__, "mt5")

    def analyze_and_place_orders(self, ict_results: dict, current_price: float, params: dict) -> bool:
        """
        Analiza el mercado y coloca/actualiza órdenes límite según AMBAS estrategias.

        Args:
            ict_results: Resultados del análisis ICT
            current_price: Precio actual del mercado
            params: Parámetros del sistema

        Returns:
            bool: True si se realizaron cambios en las órdenes
        """
        try:
            # 🔍 LOG DE ENTRADA - Confirmar que la nueva lógica se ejecuta
            enviar_senal_log("DEBUG", "analyze_and_place_orders INICIADO con nueva lógica de control", __name__, "trading")

            if not ict_results or not current_price:
                return False

            changes_made = False

            # IMPLEMENTAR LÓGICA DE CONTROL DE ÓRDENES SIMPLIFICADA
            # ========================================================

            # A. Verificar estado actual de órdenes y posiciones
            hay_posiciones_activas = self._check_active_positions()
            hay_limit_orders_activas = self._check_active_limit_orders()
            total_ordenes_limit = self._count_limit_orders()

            # Log del estado actual
            enviar_senal_log("INFO", f"Estado: Posiciones={hay_posiciones_activas}, Limits={hay_limit_orders_activas}, Total_Limits={total_ordenes_limit}", __name__, "trading")

            # B. APLICAR REGLAS DE CONTROL ESPECÍFICAS
            # ========================================

            # REGLA 1: 🚀 Al iniciar - Sin órdenes → Permitir 1 orden limit (0.05 lotes)
            if not hay_posiciones_activas and not hay_limit_orders_activas:
                enviar_senal_log("INFO", "ESTADO INICIAL: Sin órdenes → Permitir creación de 1 orden limit", __name__, "trading")
                # Permitir estrategias normales
                pass

            # REGLA 2: 🔒 Orden limit activa → BLOQUEAR nuevas órdenes limit
            elif hay_limit_orders_activas and not hay_posiciones_activas:
                enviar_senal_log("WARNING", f"BLOQUEO ACTIVADO: {total_ordenes_limit} orden(es) limit activa(s) → NO crear nuevas", __name__, "trading")
                # BLOQUEAR ambas estrategias
                self.conservative_enabled = False
                self.aggressive_enabled = False
                # Solo limpiar órdenes obsoletas
                self._cancel_obsolete_orders()
                return False

            # REGLA 3: Posición abierta → Solo Grid maneja (no nuevas limit orders)
            elif hay_posiciones_activas:
                enviar_senal_log("INFO", "POSICIÓN ABIERTA: Grid Bollinger maneja riesgo → Bloquear nuevas limit orders", __name__, "trading")
                # BLOQUEAR ambas estrategias
                self.conservative_enabled = False
                self.aggressive_enabled = False
                # Cancelar órdenes limit existentes (no grid)
                self._cancel_limit_orders_only()
                return False

            # REGLA 4: Control de múltiples limit orders (máximo 1)
            elif total_ordenes_limit > 1:
                enviar_senal_log("WARNING", f"LIMPIEZA: {total_ordenes_limit} limit orders detectadas → Mantener solo 1", __name__, "trading")
                self._keep_only_one_limit_order()
                # Temporalmente bloquear nuevas hasta que se estabilice
                self.conservative_enabled = False
                self.aggressive_enabled = False
                return True

            # C. RESTAURAR ESTRATEGIAS SI SE DESHABILITARON TEMPORALMENTE
            if not self.conservative_enabled or not self.aggressive_enabled:
                self.conservative_enabled = True
                self.aggressive_enabled = True
                enviar_senal_log("INFO", "Estrategias restauradas para operación normal", __name__, "trading")

            # D. EJECUTAR ESTRATEGIAS BAJO CONTROL
            # ====================================

            # Ejecutar ESTRATEGIA CONSERVADORA
            if self.conservative_enabled:
                conservative_result = self._execute_conservative_strategy(ict_results, current_price, params)
                if conservative_result:
                    changes_made = True

            # Ejecutar ESTRATEGIA AGRESIVA
            if self.aggressive_enabled:
                aggressive_result = self._execute_aggressive_strategy(ict_results, current_price, params)
                if aggressive_result:
                    changes_made = True

            # Limpiar órdenes obsoletas
            self._cancel_obsolete_orders()

            return changes_made

        except (ValueError, KeyError, TypeError) as e:
            enviar_senal_log("ERROR", f"Error en análisis dual de órdenes: {e}", __name__, "trading")
            return False

    def _execute_conservative_strategy(self, ict_results: dict, current_price: float, params: dict) -> bool:
        """
        Ejecuta la estrategia CONSERVADORA (lógica original).
        Solo órdenes en confluencias perfectas.
        """
        try:
            # Obtener información del mercado
            market_context = ict_results.get('market_context')
            if not market_context:
                return False

            # Obtener POI más relevante
            best_poi = self._get_best_poi(ict_results, current_price)
            if not best_poi:
                return False

            # Determinar dirección CONSERVADORA
            trade_direction = self._determine_conservative_direction(market_context, best_poi, current_price)
            if not trade_direction:
                return False

            # Calcular nivel óptimo
            optimal_level = self._calculate_optimal_level(trade_direction, best_poi, current_price, market_context)
            if not optimal_level:
                return False

            # Verificar si necesitamos actualizar órdenes conservadoras
            if self._should_update_conservative_orders(trade_direction, optimal_level, current_price):
                # Crear orden conservadora
                order_result = self._place_limit_order(
                    trade_direction,
                    optimal_level,
                    current_price,
                    best_poi,
                    strategy="CONSERVATIVE"
                )

                if order_result:
                    enviar_senal_log("INFO", f"CONSERVADOR: {trade_direction} limit en {optimal_level:.5f} (POI Score: {best_poi.get('score', 0)})", __name__, "trading")
                    return True

            return False

        except (ValueError, KeyError, TypeError) as e:
            enviar_senal_log("ERROR", f"Error en estrategia conservadora: {e}", __name__, "trading")
            return False

    def _execute_aggressive_strategy(self, ict_results: dict, current_price: float, params: dict) -> bool:
        """
        Ejecuta la estrategia AGRESIVA.
        Órdenes con POI de alta calidad independientemente de la zona.
        """
        try:
            # Obtener información del mercado
            market_context = ict_results.get('market_context')
            if not market_context:
                return False

            # Obtener POI más relevante
            best_poi = self._get_best_poi(ict_results, current_price)
            if not best_poi:
                return False

            # Determinar dirección AGRESIVA
            trade_direction = self._determine_aggressive_direction(market_context, best_poi, current_price)
            if not trade_direction:
                return False

            # Calcular nivel óptimo (mismo método)
            optimal_level = self._calculate_optimal_level(trade_direction, best_poi, current_price, market_context)
            if not optimal_level:
                return False

            # Verificar si necesitamos actualizar órdenes agresivas
            if self._should_update_aggressive_orders(trade_direction, optimal_level, current_price):
                # Crear orden agresiva
                order_result = self._place_limit_order(
                    trade_direction,
                    optimal_level,
                    current_price,
                    best_poi,
                    strategy="AGGRESSIVE"
                )

                if order_result:
                    enviar_senal_log("INFO", f"AGRESIVO: {trade_direction} limit en {optimal_level:.5f} (POI Score: {best_poi.get('score', 0)})", __name__, "trading")
                    return True

            return False

        except (ValueError, KeyError, TypeError) as e:
            enviar_senal_log("ERROR", f"Error en estrategia agresiva: {e}", __name__, "trading")
            return False

    def _get_best_poi(self, ict_results: dict, current_price: float) -> Optional[dict]:
        """Obtiene el mejor POI del sistema inteligente."""
        try:
            # TODO: Reconectar cuando core.poi_system esté completamente instrumentado
            # from core.poi_system import encontrar_poi_de_alta_probabilidad
            # market_context = ict_results.get('market_context')
            # return encontrar_poi_de_alta_probabilidad(market_context, current_price)
            enviar_senal_log("DEBUG", "POI detection temporalmente deshabilitado durante instrumentación", __name__, "general")
            return None
        except (ValueError, KeyError, TypeError) as e:
            enviar_senal_log("WARNING", f"Error obteniendo POI: {e}", __name__, "general")
            return None

    def _determine_conservative_direction(self, market_context, poi: dict, current_price: float) -> Optional[str]:
        """
        Determina la dirección del trade CONSERVADORA (lógica original).
        Solo confluencias perfectas: H4 bias + zona adecuada + POI alineado.

        Returns:
            str: 'BUY' o 'SELL' o None si no hay señal clara
        """
        try:
            # Obtener bias de diferentes timeframes
            h4_bias = getattr(market_context, 'h4_bias', 'NO_DETERMINADO')
            m15_bias = getattr(market_context, 'm15_bias', 'NO_DETERMINADO')

            # Obtener zona de precios
            zona = getattr(market_context, 'premium_discount_zone', 'NO_CALCULADO')

            # Obtener tipo de POI
            poi_type = poi.get('type', '').upper()
            poi_score = poi.get('score', 0)

            # Lógica CONSERVADORA: solo confluencias perfectas
            if poi_score < 60:  # Score alto requerido para conservador
                return None

            # Confluencia alcista CONSERVADORA (BUY)
            if (h4_bias == 'BULLISH' and zona == 'DISCOUNT' and
                ('BULLISH' in poi_type or 'DEMAND' in poi_type)):
                return 'BUY'

            # Confluencia bajista CONSERVADORA (SELL)
            elif (h4_bias == 'BEARISH' and zona == 'PREMIUM' and
                  ('BEARISH' in poi_type or 'SUPPLY' in poi_type)):
                return 'SELL'

            # Casos especiales con M15 confirmación y score muy alto
            elif (h4_bias == 'BULLISH' and m15_bias == 'BULLISH' and
                  zona == 'DISCOUNT' and poi_score >= 80):
                return 'BUY'

            elif (h4_bias == 'BEARISH' and m15_bias == 'BEARISH' and
                  zona == 'PREMIUM' and poi_score >= 80):
                return 'SELL'

            return None

        except (ValueError, KeyError, TypeError) as e:
            enviar_senal_log("ERROR", f"Error determinando dirección conservadora: {e}", __name__, "trading")
            return None

    def _determine_aggressive_direction(self, market_context, poi: dict, current_price: float) -> Optional[str]:
        """
        Determina la dirección del trade AGRESIVA.
        POI de alta calidad independientemente de la zona.

        Returns:
            str: 'BUY' o 'SELL' o None si no hay señal clara
        """
        try:
            # Obtener bias de diferentes timeframes
            h4_bias = getattr(market_context, 'h4_bias', 'NO_DETERMINADO')
            m15_bias = getattr(market_context, 'm15_bias', 'NO_DETERMINADO')

            # Obtener zona de precios
            zona = getattr(market_context, 'premium_discount_zone', 'NO_CALCULADO')

            # Obtener tipo de POI
            poi_type = poi.get('type', '').upper()
            poi_score = poi.get('score', 0)

            # Lógica AGRESIVA: POI de alta calidad sin restricciones de zona
            if poi_score < 70:  # Score muy alto requerido para agresivo
                return None

            # Confluencia alcista AGRESIVA (BUY) - ignora zona
            if (h4_bias == 'BULLISH' and
                ('BULLISH' in poi_type or 'DEMAND' in poi_type) and
                poi_score >= 70):
                return 'BUY'

            # Confluencia bajista AGRESIVA (SELL) - ignora zona
            elif (h4_bias == 'BEARISH' and
                  ('BEARISH' in poi_type or 'SUPPLY' in poi_type) and
                  poi_score >= 70):
                return 'SELL'

            # Casos con M15 confirmación independiente de zona
            elif (h4_bias == 'BULLISH' and m15_bias == 'BULLISH' and
                  ('BULLISH' in poi_type or 'DEMAND' in poi_type) and
                  poi_score >= 75):
                return 'BUY'

            elif (h4_bias == 'BEARISH' and m15_bias == 'BEARISH' and
                  ('BEARISH' in poi_type or 'SUPPLY' in poi_type) and
                  poi_score >= 75):
                return 'SELL'

            return None

        except (ValueError, KeyError, TypeError) as e:
            enviar_senal_log("ERROR", f"Error determinando dirección agresiva: {e}", __name__, "trading")
            return None

    def _calculate_optimal_level(self, direction: str, poi: dict, current_price: float, market_context) -> Optional[float]:
        """
        Calcula el nivel óptimo para colocar la orden límite.

        Args:
            direction: 'BUY' o 'SELL'
            poi: Información del POI
            current_price: Precio actual
            market_context: Contexto del mercado

        Returns:
            float: Nivel óptimo para la orden límite
        """
        try:
            poi_level = poi.get('level', current_price)
            poi_score = poi.get('score', 0)

            # Obtener daily range para calcular buffer
            daily_range = getattr(market_context, 'daily_range', {})
            daily_high = daily_range.get('high', current_price)
            daily_low = daily_range.get('low', current_price)
            daily_range_pips = abs(daily_high - daily_low) * 10000

            # Calcular buffer basado en el score del POI y volatilidad
            base_buffer_pips = 3  # Buffer mínimo
            volatility_buffer = min(daily_range_pips * 0.02, 15)  # Máximo 15 pips
            score_buffer = (poi_score / 100) * 5  # Hasta 5 pips extra por score alto

            total_buffer_pips = base_buffer_pips + volatility_buffer + score_buffer
            buffer_price = total_buffer_pips / 10000  # Convertir a precio

            if direction == 'BUY':
                # Para compra, colocar orden por debajo del POI
                optimal_level = poi_level - buffer_price
                # Verificar que esté por debajo del precio actual
                if optimal_level >= current_price:
                    optimal_level = current_price - (10 / 10000)  # 10 pips abajo

            else:  # SELL
                # Para venta, colocar orden por encima del POI
                optimal_level = poi_level + buffer_price
                # Verificar que esté por encima del precio actual
                if optimal_level <= current_price:
                    optimal_level = current_price + (10 / 10000)  # 10 pips arriba

            return round(optimal_level, 5)

        except (ValueError, KeyError, TypeError) as e:
            enviar_senal_log("ERROR", f"Error calculando nivel óptimo: {e}", __name__, "trading")
            return None

    def _should_update_conservative_orders(self, direction: str, optimal_level: float, current_price: float) -> bool:
        """Determina si se deben actualizar las órdenes conservadoras."""
        return self._should_update_orders_by_strategy(direction, optimal_level, current_price, "CONSERVATIVE")

    def _should_update_aggressive_orders(self, direction: str, optimal_level: float, current_price: float) -> bool:
        """Determina si se deben actualizar las órdenes agresivas."""
        return self._should_update_orders_by_strategy(direction, optimal_level, current_price, "AGGRESSIVE")

    def _should_update_orders_by_strategy(self, direction: str, optimal_level: float, current_price: float, strategy: str) -> bool:
        """
        Determina si se deben actualizar las órdenes de una estrategia específica.

        Args:
            direction: Nueva dirección del trade
            optimal_level: Nuevo nivel óptimo
            current_price: Precio actual
            strategy: "CONSERVATIVE" o "AGGRESSIVE"

        Returns:
            bool: True si se deben actualizar las órdenes
        """
        try:
            # Filtrar órdenes por estrategia
            strategy_orders = {
                ticket: order for ticket, order in self.active_orders.items()
                if order.get('strategy') == strategy
            }

            # Si no hay órdenes de esta estrategia, crear nueva
            if not strategy_orders:
                return True

            # Verificar si hay cambio de dirección para esta estrategia
            strategy_directions = [order['direction'] for order in strategy_orders.values()]
            if direction not in strategy_directions:
                return True

            # Verificar si el nivel ha cambiado significativamente
            for order_id, order_info in strategy_orders.items():
                if order_info['direction'] == direction:
                    current_level = order_info['level']
                    distance_pips = abs(optimal_level - current_level) * 10000

                    if distance_pips >= self.update_threshold_pips:
                        return True

            return False

        except (ValueError, KeyError, TypeError) as e:
            enviar_senal_log("ERROR", f"Error verificando actualización {strategy}: {e}", __name__, "trading")
            return False

    def _place_limit_order(self, direction: str, level: float, current_price: float, poi: dict, strategy: str = "CONSERVATIVE") -> Optional[dict]:
        """
        Coloca una orden límite en MT5 con comentario específico por estrategia.

        Args:
            direction: 'BUY' o 'SELL'
            level: Nivel de la orden límite
            current_price: Precio actual
            poi: Información del POI
            strategy: "CONSERVATIVE" o "AGGRESSIVE"

        Returns:
            dict: Resultado de la orden o None si falló
        """
        try:
            # Verificar conexión MT5
            if not inicializar_mt5():
                enviar_senal_log("CRITICAL", "Error: MT5 no inicializado (FundedNext)", __name__, "trading")
                return None

            # Obtener información del símbolo
            symbol_info = mt5.symbol_info(self.symbol)  # type: ignore
            if not symbol_info:
                enviar_senal_log("CRITICAL", f"Error: Símbolo {self.symbol} no encontrado", __name__, "trading")
                return None

            # Cancelar órdenes existentes de la misma estrategia y dirección
            self._cancel_orders_by_strategy_and_direction(strategy, direction)

            # Configurar tipo de orden
            if direction == 'BUY':
                order_type = mt5.ORDER_TYPE_BUY_LIMIT
                action = "Compra límite"
            else:
                order_type = mt5.ORDER_TYPE_SELL_LIMIT
                action = "Venta límite"

            # Seleccionar magic number según estrategia
            magic_number = self.magic_number_conservative if strategy == "CONSERVATIVE" else self.magic_number_aggressive

            # Crear comentario específico
            strategy_prefix = "CONS" if strategy == "CONSERVATIVE" else "AGR"
            poi_score = poi.get('score', 0)
            comment = f"{strategy_prefix}_POI{int(poi_score)}_ICT"

            # SIN Stop Loss ni Take Profit - Dejar que RiskBot y Bollinger gestionen
            # El sistema de gestión de riesgo automático se encargará
            sl = 0.0  # Sin SL automático
            tp = 0.0  # Sin TP automático

            # Obtener volumen dinámico
            dynamic_volume = self.get_dynamic_volume()

            # Preparar request SIN SL/TP
            request = {
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": self.symbol,
                "volume": dynamic_volume,
                "type": order_type,
                "price": level,
                # sl y tp eliminados - gestión por RiskBot/Bollinger
                "deviation": 20,
                "magic": magic_number,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            }

            # Enviar orden
            result = mt5.order_send(request)  # type: ignore

            if result.retcode == mt5.TRADE_RETCODE_DONE:
                # Almacenar información de la orden
                order_info = {
                    'ticket': result.order,
                    'direction': direction,
                    'level': level,
                    'volume': dynamic_volume,
                    'sl': 0.0,  # Sin SL - gestionado por RiskBot
                    'tp': 0.0,  # Sin TP - gestionado por Bollinger
                    'poi_score': poi_score,
                    'strategy': strategy,
                    'comment': comment,
                    'timestamp': datetime.now()
                }

                self.active_orders[result.order] = order_info

                # Log del evento con sistema centralizado
                enviar_senal_log("INFO", f"ORDEN LÍMITE EJECUTADA: {strategy} {action} en {self.symbol} - Precio: {level:.5f}, Volumen: {dynamic_volume}, Ticket: #{result.order}", __name__, "general")
                enviar_senal_log("INFO", f"{strategy_prefix} {action} ejecutada: Ticket #{result.order} en {level:.5f} (SIN SL/TP - RiskBot gestiona)", __name__, "trading")

                return order_info

            else:
                enviar_senal_log("ERROR", f"Error creando orden {strategy}: {result.retcode} - {result.comment}", __name__, "trading")
                return None

        except (ValueError, KeyError, TypeError) as e:
            enviar_senal_log("ERROR", f"Error colocando orden límite {strategy}: {e}", __name__, "trading")
            return None

    def _cancel_orders_by_strategy_and_direction(self, strategy: str, direction: str):
        """Cancela órdenes existentes de una estrategia y dirección específica."""
        try:
            orders_to_cancel = []

            for ticket, order_info in self.active_orders.items():
                if (order_info.get('strategy') == strategy and
                    order_info.get('direction') == direction):
                    orders_to_cancel.append(ticket)

            for ticket in orders_to_cancel:
                self._cancel_order(ticket)

        except (ValueError, KeyError, TypeError) as e:
            enviar_senal_log("ERROR", f"Error cancelando órdenes {strategy} {direction}: {e}", __name__, "trading")

    def _cancel_obsolete_orders(self):
        """Cancela órdenes que ya no son relevantes."""
        try:
            # Obtener órdenes pendientes actuales
            orders = mt5.orders_get(symbol=self.symbol)  # type: ignore
            if not orders:
                self.active_orders.clear()
                return

            orders_to_cancel = []

            # Verificar si nuestras órdenes guardadas aún existen
            for ticket, order_info in list(self.active_orders.items()):
                order_exists = any(order.ticket == ticket for order in orders)

                if not order_exists:
                    # La orden ya no existe (fue ejecutada o cancelada)
                    del self.active_orders[ticket]
                    continue

                # Verificar si la orden es muy antigua (más de 4 horas)
                age = datetime.now() - order_info['timestamp']
                if age.total_seconds() > 4 * 3600:  # 4 horas
                    orders_to_cancel.append(ticket)

            # Cancelar órdenes obsoletas
            for ticket in orders_to_cancel:
                self._cancel_order(ticket)

            # Limitar número máximo de órdenes por estrategia
            conservative_orders = [t for t, o in self.active_orders.items() if o.get('strategy') == 'CONSERVATIVE']
            aggressive_orders = [t for t, o in self.active_orders.items() if o.get('strategy') == 'AGGRESSIVE']

            # Máximo 2 órdenes por estrategia
            if len(conservative_orders) > 2:
                oldest_conservative = sorted(
                    [(t, self.active_orders[t]['timestamp']) for t in conservative_orders],
                    key=lambda x: x[1]
                )
                for ticket, _ in oldest_conservative[2:]:  # Cancelar las más antiguas
                    self._cancel_order(ticket)

            if len(aggressive_orders) > 2:
                oldest_aggressive = sorted(
                    [(t, self.active_orders[t]['timestamp']) for t in aggressive_orders],
                    key=lambda x: x[1]
                )
                for ticket, _ in oldest_aggressive[2:]:  # Cancelar las más antiguas
                    self._cancel_order(ticket)

        except (ValueError, KeyError, TypeError) as e:
            enviar_senal_log("ERROR", f"Error cancelando órdenes obsoletas: {e}", __name__, "trading")

    def _cancel_order(self, ticket: int) -> bool:
        """
        Cancela una orden específica.

        Args:
            ticket: Número de ticket de la orden

        Returns:
            bool: True si se canceló exitosamente
        """
        try:
            request = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": ticket,
            }

            result = mt5.order_send(request)  # type: ignore

            if result.retcode == mt5.TRADE_RETCODE_DONE:
                if ticket in self.active_orders:
                    order_info = self.active_orders[ticket]
                    strategy = order_info.get('strategy', 'UNKNOWN')
                    strategy_prefix = "CONS" if strategy == "CONSERVATIVE" else "AGR"
                    enviar_senal_log("INFO", f"{strategy_prefix} Orden #{ticket} cancelada ({order_info['direction']} en {order_info['level']:.5f})", __name__, "trading")
                    del self.active_orders[ticket]
                return True
            else:
                enviar_senal_log("ERROR", f"Error cancelando orden #{ticket}: {result.comment}", __name__, "trading")
                return False

        except (ValueError, KeyError, TypeError) as e:
            enviar_senal_log("ERROR", f"Error cancelando orden #{ticket}: {e}", __name__, "trading")
            return False

    def get_active_orders_summary(self) -> str:
        """
        Retorna un resumen de las órdenes activas separadas por estrategia para mostrar en el dashboard.

        Returns:
            str: Resumen de órdenes activas por estrategia
        """
        try:
            if not self.active_orders:
                return "Sin órdenes límite activas"

            conservative_orders = []
            aggressive_orders = []

            for ticket, order_info in self.active_orders.items():
                direction = order_info['direction']
                level = order_info['level']
                score = order_info['poi_score']
                strategy = order_info.get('strategy', 'UNKNOWN')

                # Calcular edad de la orden
                age = datetime.now() - order_info['timestamp']
                age_hours = age.total_seconds() / 3600

                order_line = f"#{ticket}: {direction} @ {level:.5f} (Score: {score}, {age_hours:.1f}h)"

                if strategy == 'CONSERVATIVE':
                    conservative_orders.append(f"CONS {order_line}")
                else:
                    aggressive_orders.append(f"AGR {order_line}")

            summary_lines = []

            if conservative_orders:
                summary_lines.append("CONSERVADOR:")
                summary_lines.extend(conservative_orders)

            if aggressive_orders:
                summary_lines.append("AGRESIVO:")
                if len(summary_lines) > 0:
                    summary_lines.append("")  # Línea en blanco
                summary_lines.extend(aggressive_orders)

            return "\n".join(summary_lines)

        except (ValueError, KeyError, TypeError) as e:
            return f"Error al generar resumen: {e}"

        # ==========================================
        # FUNCIONES AUXILIARES DE CONTROL DE ÓRDENES
        # ==========================================

    def _check_active_positions(self) -> bool:
        """Verifica si hay posiciones abiertas (trades ejecutados)."""
        try:
            positions = mt5.positions_get()  # type: ignore
            return positions and len(positions) > 0
        except (ValueError, KeyError, TypeError):
            return False

    def _check_active_limit_orders(self) -> bool:
        """Verifica si hay órdenes limit activas (pendientes de 0.05 lotes)."""
        try:
            orders = mt5.orders_get()  # type: ignore
            if not orders:
                return False

            for order in orders:
                volume = getattr(order, 'volume_initial', 0)
                comment = getattr(order, 'comment', '').upper()
                magic = getattr(order, 'magic', 0)

                # Identificar órdenes limit de entrada (0.05 lotes, no grid)
                is_limit_entry = (
                    volume == 0.05 and
                    'GRID' not in comment and
                    'BOLLINGER' not in comment and
                    magic != 12345  # Magic del grid
                )

                if is_limit_entry:
                    return True

            return False
        except (ValueError, KeyError, TypeError):
            return False

    def _count_limit_orders(self) -> int:
        """Cuenta el número de órdenes limit de entrada activas."""
        try:
            orders = mt5.orders_get()  # type: ignore
            if not orders:
                return 0

            count = 0
            for order in orders:
                volume = getattr(order, 'volume_initial', 0)
                comment = getattr(order, 'comment', '').upper()
                magic = getattr(order, 'magic', 0)

                # Identificar órdenes limit de entrada (0.05 lotes, no grid)
                is_limit_entry = (
                    volume == 0.05 and
                    'GRID' not in comment and
                    'BOLLINGER' not in comment and
                    magic != 12345  # Magic del grid
                )

                if is_limit_entry:
                    count += 1

            return count
        except (ValueError, KeyError, TypeError):
            return 0

    def _cancel_limit_orders_only(self):
        """Cancela solo órdenes limit de entrada, preserva las del grid."""
        try:
            orders = mt5.orders_get()  # type: ignore
            if not orders:
                return

            for order in orders:
                volume = getattr(order, 'volume_initial', 0)
                comment = getattr(order, 'comment', '').upper()
                magic = getattr(order, 'magic', 0)

                # Identificar órdenes limit de entrada (0.05 lotes, no grid)
                is_limit_entry = (
                    volume == 0.05 and
                    'GRID' not in comment and
                    'BOLLINGER' not in comment and
                    magic != 12345  # Magic del grid
                )

                if is_limit_entry:
                    result = mt5.order_send({  # type: ignore
                        "action": mt5.TRADE_ACTION_REMOVE,
                        "order": order.ticket,
                    })
                    if result.retcode == mt5.TRADE_RETCODE_DONE:
                        enviar_senal_log("INFO", f"Orden limit cancelada: #{order.ticket}", __name__, "trading")
                    else:
                        enviar_senal_log("ERROR", f"Error cancelando limit #{order.ticket}: {result.comment}", __name__, "trading")
        except (ValueError, KeyError, TypeError) as e:
            enviar_senal_log("ERROR", f"Error cancelando órdenes limit: {e}", __name__, "trading")

    def _keep_only_one_limit_order(self):
        """Mantiene solo la orden limit más reciente, cancela las demás."""
        try:
            orders = mt5.orders_get()  # type: ignore
            if not orders:
                return

            limit_orders = []
            for order in orders:
                volume = getattr(order, 'volume_initial', 0)
                comment = getattr(order, 'comment', '').upper()
                magic = getattr(order, 'magic', 0)

                # Identificar órdenes limit de entrada
                is_limit_entry = (
                    volume == 0.05 and
                    'GRID' not in comment and
                    'BOLLINGER' not in comment and
                    magic != 12345
                )

                if is_limit_entry:
                    limit_orders.append(order)

            # Si hay más de 1, cancelar todas menos la más reciente
            if len(limit_orders) > 1:
                # Ordenar por tiempo de creación (más antiguas primero)
                sorted_orders = sorted(limit_orders, key=lambda x: x.time_setup)
                orders_to_cancel = sorted_orders[:-1]  # Todas menos la última

                enviar_senal_log("INFO", f"Cancelando {len(orders_to_cancel)} órdenes limit excesivas", __name__, "trading")

                for order in orders_to_cancel:
                    result = mt5.order_send({  # type: ignore
                        "action": mt5.TRADE_ACTION_REMOVE,
                        "order": order.ticket,
                    })
                    if result.retcode == mt5.TRADE_RETCODE_DONE:
                        enviar_senal_log("INFO", f"Orden limit excesiva cancelada: #{order.ticket}", __name__, "trading")
                    else:
                        enviar_senal_log("ERROR", f"Error cancelando orden #{order.ticket}: {result.comment}", __name__, "trading")

        except (ValueError, KeyError, TypeError) as e:
            enviar_senal_log("ERROR", f"Error en limpieza de órdenes: {e}", __name__, "trading")


# =============================================================================
# INSTANCIA GLOBAL
# =============================================================================
limit_order_manager = LimitOrderManager()


def update_limit_orders(ict_results: dict, current_price: float, params: dict) -> bool:
    """
    Función principal para actualizar órdenes límite desde el sistema principal.

    Args:
        ict_results: Resultados del análisis ICT
        current_price: Precio actual
        params: Parámetros del sistema

    Returns:
        bool: True si se realizaron cambios
    """
    return limit_order_manager.analyze_and_place_orders(ict_results, current_price, params)


def get_limit_orders_status() -> str:
    """
    Obtiene el estado actual de las órdenes límite para el dashboard.

    Returns:
        str: Estado de las órdenes límite
    """
    return limit_order_manager.get_active_orders_summary()
