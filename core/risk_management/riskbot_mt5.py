from decimal import Decimal, ROUND_HALF_UP
from typing import Optional
# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log, log_mt5

# riskbot_mt5.py

# =============================================================================
# SECCIÓN 1: IMPORTACIONES DE LIBRERÍAS Y MÓDULOS
# =============================================================================
import MetaTrader5 as mt5
from datetime import datetime
import pytz
from sistema.config import COMISION_POR_LOTE, log_debug
from sistema.data_logger import log_posicion_cerrada, log_error_critico

# =============================================================================
# SECCIÓN 2: CLASE RISKBOTMT5
# =============================================================================
class RiskBot:
    """
    Clase para la gestión de riesgo del sistema de trading en MetaTrader 5.
    Monitorea el profit/loss y cierra operaciones si se exceden los límites.
    """

    def set_backtest_mode(self, sim_broker):
        """
        Activa el modo backtest y conecta el RiskBot a un bróker simulado.
        Esto permite que todos los métodos de gestión de riesgo operen sobre el broker simulado en vez de MT5 real.
        """
        self.backtest_mode = True
        self.sim_broker = sim_broker
        log_debug("RiskBot", "Modo backtest activado y broker simulado conectado.", "INFO")

    def __init__(self, risk_target_profit=10.0, max_profit_target=130.0, risk_percent=1.0, comision_por_lote=COMISION_POR_LOTE):
        # Parámetros originales
        self.risk_target_profit = risk_target_profit
        self.max_profit_target = max_profit_target
        self.risk_percent = risk_percent
        self.comision_por_lote = comision_por_lote

        # Parámetros de Reducción Proporcional
        self.proportional_reduction_active = False
        self.reduction_trigger_mode = "FixedAmount"  # FixedAmount, MaxProfitPercent, AccountBalancePercent
        self.reduction_trigger_value = 50.0
        self.reduction_percentage = 25.0

        # Parámetros de Breakeven-Plus
        self.breakeven_plus_active = True
        self.breakeven_plus_min_positions = 3
        self.breakeven_plus_buffer_usd = 5.0

        # Flags de control interno
        self.reduction_triggered_flag = False

        log_debug("RiskBotMT5", "RiskBotMT5 inicializado con parámetros de riesgo avanzado.", "INFO")

    # =========================================================================
    # SECCIÓN 2.0: Funciones de Compatibilidad para Diagnóstico
    # =========================================================================
    @property
    def balance(self):
        """Compatibilidad: balance de la cuenta"""
        return self.get_account_balance()

    @property
    def max_positions(self):
        """Compatibilidad: máximo número de posiciones"""
        return getattr(self, '_max_positions', 10)  # Valor por defecto

    def calculate_profit_target(self, balance: Optional[float] = None, risk_percent: Optional[float] = None):
        """
        Calcula el objetivo de profit basado en balance y porcentaje de riesgo.
        Función de compatibilidad para el sistema de diagnóstico.
        """
        if balance is None:
            balance = self.get_account_balance()
        if risk_percent is None:
            risk_percent = self.risk_percent

        return balance * (risk_percent / 100.0)

    def should_trigger_breakeven_plus(self, positions=None):
        """
        Determina si se debe activar breakeven plus.
        Función de compatibilidad.
        """
        if positions is None:
            positions = self.get_open_positions()
        return self._should_activate_breakeven_plus()

    def validate_trade_conditions(self, **kwargs):
        """
        Valida condiciones de trading.
        Función de compatibilidad.
        """
        # Verificar que MT5 esté conectado
        if not mt5.initialize():  # type: ignore
            return False

        # Verificar balance mínimo
        balance = self.get_account_balance()
        if balance < 100:  # Balance mínimo
            return False

        return True

    def manage_existing_positions(self):
        """
        Gestiona posiciones existentes.
        Función de compatibilidad que usa check_and_act.
        """
        return self.check_and_act()

    def calcular_volumen_dinamico(self, balance_pct: float = 1.0, max_volume: float = 0.50, min_volume: float = 0.01) -> float:
        """
        Calcula volumen dinámico basado en balance y riesgo.

        Args:
            balance_pct: Porcentaje del balance a usar para cálculo (default 1%)
            max_volume: Volumen máximo permitido
            min_volume: Volumen mínimo permitido

        Returns:
            float: Volumen calculado dinámicamente
        """
        try:
            # Obtener balance actual
            balance = self.get_account_balance()

            if balance <= 0:
                enviar_senal_log("WARNING", f"Balance inválido: {balance}, usando volumen mínimo", __name__, "trading")
                return min_volume

            # Calcular volumen basado en porcentaje del balance
            target_risk = balance * (balance_pct / 100.0)

            # Convertir riesgo a volumen (aproximado)
            # Asumiendo ~$10 por lote como aproximación
            volume_calculated = max(target_risk / 10.0, min_volume)

            # Aplicar límites
            volume_final = min(max(volume_calculated, min_volume), max_volume)

            # Redondear a 2 decimales (estándar MT5)
            volume_final = round(volume_final, 2)

            enviar_senal_log("DEBUG", f"Volumen dinámico calculado: {volume_final} (Balance: ${balance:.2f})", __name__, "trading")

            return volume_final

        except Exception as e:
            enviar_senal_log("ERROR", f"Error calculando volumen dinámico: {e}", __name__, "trading")
            return min_volume

    def calculate_position_size(self, price: float, stop_loss_pips: Optional[float] = None):
        """
        Calcula el tamaño de posición.
        Función de compatibilidad.
        """
        return self.calcular_lotaje_optimo_por_riesgo(price, stop_loss_pips)


    # =========================================================================
    # SECCIÓN 2.1: Métodos de Obtención de Información
    # =========================================================================
    def get_account_balance(self):
        """Obtiene el balance actual de la cuenta."""
        account_info = mt5.account_info()  # type: ignore
        if account_info is None:
            log_debug("RiskBot", "No se pudo obtener la información de la cuenta. Retornando balance 0.0.", "ERROR")
            return 0.0
        return account_info.balance

    def get_account_info(self):
        """
        Obtiene información completa de la cuenta.
        Retorna un objeto con propiedades .equity y .profit para compatibilidad.
        """
        from types import SimpleNamespace

        account_info = mt5.account_info()  # type: ignore
        if account_info is None:
            log_debug("RiskBot", "No se pudo obtener la información de la cuenta.", "ERROR")
            # Retornar objeto simulado con valores por defecto
            return SimpleNamespace(
                equity=0.0,
                profit=0.0,
                balance=0.0
            )

        # Crear objeto compatible con las propiedades esperadas
        return SimpleNamespace(
            equity=account_info.equity,
            profit=account_info.profit,
            balance=account_info.balance
        )

    def calcular_lotaje_optimo_por_riesgo(self, precio_entrada, stop_loss_pips=None, lotaje_base=0.01):
        """
        Calcula el lotaje óptimo basado en el porcentaje de riesgo de la cuenta.

        Args:
            precio_entrada: Precio al que se planea entrar
            stop_loss_pips: Número de pips de stop loss (opcional)
            lotaje_base: Lotaje base mínimo a usar

        Returns:
            float: Lotaje calculado según el riesgo
        """
        try:
            balance = self.get_account_balance()
            if balance <= 0:
                log_debug("RiskBot", "Balance de cuenta inválido, usando lotaje base", "WARNING")
                return lotaje_base

            # Calcular el riesgo en dinero basado en el porcentaje de riesgo
            riesgo_dinero = balance * (self.risk_percent / 100.0)

            # Si no se especifica stop loss, usar una estimación conservadora
            if stop_loss_pips is None:
                stop_loss_pips = 20  # 20 pips por defecto para cálculo conservador

            # Obtener información del símbolo para calcular el valor del pip
            symbol_info = mt5.symbol_info("EURUSD")  # type: ignore
            if symbol_info is None:
                log_debug("RiskBot", "No se pudo obtener info del símbolo, usando lotaje base", "WARNING")
                return lotaje_base

            # Calcular valor del pip por lote estándar (100,000 unidades)
            if symbol_info.digits == 5:
                pip_size = 0.00001
            else:
                pip_size = 0.0001

            valor_pip_por_lote = pip_size * 100000 / precio_entrada

            # Calcular lotaje óptimo
            lotaje_optimo = riesgo_dinero / (stop_loss_pips * valor_pip_por_lote)

            # Aplicar límites de seguridad
            lotaje_optimo = max(lotaje_base, min(lotaje_optimo, 1.0))  # Entre lotaje_base y 1.0

            # Redondear a 2 decimales
            lotaje_optimo = round(lotaje_optimo, 2)

            log_debug("RiskBot", f"Lotaje calculado: {lotaje_optimo} (Balance: ${balance:.2f}, Riesgo: {self.risk_percent}%)", "INFO")
            return lotaje_optimo

        except (FileNotFoundError, PermissionError, IOError) as e:
            log_debug("RiskBot", f"Error calculando lotaje óptimo: {e}, usando lotaje base", "ERROR")
            return lotaje_base

    def calcular_siguiente_lote_grid(self, ultimo_lote, lotaje_inicial):
        """
        Calcula el siguiente lote para el grid basado en el riesgo y la progresión.
        Usa el módulo Decimal para precisión financiera y redondeo predecible.
        """
        try:
            # Convertimos las entradas a Decimal para precisión
            ultimo_lote_d = Decimal(str(ultimo_lote))
            lotaje_inicial_d = Decimal(str(lotaje_inicial))

            # La lógica de progresión es un incremento del 50% del lote inicial
            incremento = lotaje_inicial_d * Decimal('0.5')
            siguiente_lote_d = ultimo_lote_d + incremento

            # Redondeamos a 2 decimales, siempre hacia arriba en el caso de .5 (ROUND_HALF_UP)
            siguiente_lote_redondeado = siguiente_lote_d.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            # Aplicar límites de seguridad
            siguiente_lote_final = max(lotaje_inicial_d, min(siguiente_lote_redondeado, Decimal('2.0')))

            # Devolver como float, como el resto del sistema espera
            return float(siguiente_lote_final)

        except (FileNotFoundError, PermissionError, IOError) as e:
            log_debug("RiskBot", f"Error calculando siguiente lote grid: {e}", "ERROR")
            # Fallback en caso de error, también usando Decimal para consistencia
            fallback_lote = (Decimal(str(ultimo_lote)) + Decimal(str(lotaje_inicial)) * Decimal('0.5')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            return float(fallback_lote)

    def get_open_positions(self):
        """Obtiene todas las posiciones abiertas."""
        positions = mt5.positions_get()  # type: ignore
        if positions is None:
            log_debug("RiskBot", "No se pudieron obtener posiciones abiertas.", "WARNING")
            return []
        return positions

    def get_total_profit_and_lots(self):
        """Calcula el profit total, comisión, swap y lotes de todas las posiciones abiertas."""
        total_profit = 0.0
        total_lots = 0.0
        total_swap = 0.0
        positions = self.get_open_positions()
        for pos in positions:
            try:
                total_profit += float(pos.profit)
                total_lots += float(pos.volume)
                total_swap += float(pos.swap)
            except (ValueError, TypeError) as e:
                log_debug("RiskBot", f"Error procesando posición {pos.ticket}: {e}", "ERROR")
                log_error_critico("RiskBot", "Procesando Posición", f"Error al procesar posición {pos.ticket}: {e}", str(e))
                continue

        try:
            comision_total = total_lots * self.comision_por_lote
        except (TypeError, ValueError) as e:
            log_debug("RiskBot", f"Error calculando comisión total: {e}", "ERROR")
            log_error_critico("RiskBot", "Cálculo Comisión", f"Error calculando comisión: {e}", str(e))
            comision_total = 0.0

        profit_neto = total_profit - comision_total
        return total_profit, comision_total, profit_neto, total_lots, total_swap

    def _get_real_net_profit(self):
        """
        Calcula el beneficio neto real según la fórmula:
        P_net_real = P_bruto - (C_lotes + C_swap)
        """
        total_profit, comision_total, _, _, total_swap = self.get_total_profit_and_lots()
        return total_profit - (comision_total + total_swap)

    # =========================================================================
    # SECCIÓN 2.2: Métodos de Acción (Cierre de Operaciones)
    # =========================================================================
    def close_all_positions(self, motivo_cierre="Cierre Desconocido"):
        """Cierra todas las posiciones abiertas en la cuenta."""
        positions = self.get_open_positions()
        if not positions:
            log_debug("RiskBot", "No hay posiciones abiertas para cerrar.", "INFO")
            return

        log_debug("RiskBot", f"Cerrando todas las {len(positions)} posiciones abiertas por motivo: {motivo_cierre}.", "WARNING")
        for pos in positions:
            order_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": order_type,
                "position": pos.ticket,
                "deviation": 10,
                "magic": 1001,
                "comment": f"RiskBot close ({motivo_cierre})",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            result = mt5.order_send(request)  # type: ignore
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                log_debug("RiskBot", f"Error al cerrar posición {pos.ticket} ({pos.symbol}): {result.retcode} - {result.comment}", "ERROR")
                log_error_critico("RiskBot", "Cierre Posición", f"Error al cerrar posición {pos.ticket}: {result.comment}", str(result))
            else:
                log_debug("RiskBot", f"Posición {pos.ticket} en {pos.symbol} cerrada.", "SUCCESS")

                time_apertura_pos_utc = datetime.fromtimestamp(pos.time, tz=pytz.utc)
                time_cierre_utc = datetime.utcnow()
                duracion_segundos = (time_cierre_utc - time_apertura_pos_utc).total_seconds()

                profit_neto_calc = float(pos.profit) - (float(pos.volume) * self.comision_por_lote)

                log_posicion_cerrada(
                    pos.symbol, pos.ticket, "BUY" if pos.type == mt5.POSITION_TYPE_BUY else "SELL",
                    pos.volume, pos.price_open, result.price,
                    profit_neto_calc, motivo_cierre
                )
        log_debug("RiskBot", "Todas las posiciones han sido procesadas para cierre.", "INFO")

    # =========================================================================
    # SECCIÓN 2.2.1: GESTIÓN DE RIESGO AVANZADO - REDUCCIÓN PROPORCIONAL
    # =========================================================================

    def _should_trigger_reduction(self):
        """
        Evalúa si se debe activar la reducción proporcional basada en el P_net_real
        y el modo de trigger configurado.
        """
        if not self.proportional_reduction_active or self.reduction_triggered_flag:
            return False

        p_net_real = self._get_real_net_profit()

        if self.reduction_trigger_mode == "FixedAmount":
            p_trigger = self.reduction_trigger_value
        elif self.reduction_trigger_mode == "MaxProfitPercent":
            p_trigger = (self.reduction_trigger_value / 100) * self.max_profit_target
        elif self.reduction_trigger_mode == "AccountBalancePercent":
            balance = self.get_account_balance()
            p_trigger = (self.reduction_trigger_value / 100) * balance
        else:
            log_debug("RiskBot", f"Modo de trigger desconocido: {self.reduction_trigger_mode}", "ERROR")
            return False

        return p_net_real >= p_trigger

    def _execute_proportional_reduction(self):
        """
        Ejecuta el cierre parcial de todas las posiciones abiertas según el
        porcentaje de reducción configurado.
        """
        positions = self.get_open_positions()
        if not positions:
            log_debug("RiskBot", "No hay posiciones para aplicar reducción proporcional.", "INFO")
            return False

        reduction_factor = self.reduction_percentage / 100.0
        successful_reductions = 0

        log_debug("RiskBot", f"Ejecutando reducción proporcional del {self.reduction_percentage}% en {len(positions)} posiciones.", "INFO")

        for pos in positions:
            try:
                # Calcular nuevo volumen
                current_volume = float(pos.volume)
                volume_to_close = current_volume * reduction_factor

                # Verificar volumen mínimo
                symbol_info = mt5.symbol_info(pos.symbol)  # type: ignore
                if symbol_info and volume_to_close < symbol_info.volume_min:
                    log_debug("RiskBot", f"Volumen a cerrar {volume_to_close} menor que mínimo {symbol_info.volume_min} para {pos.symbol}", "WARNING")
                    continue

                # Redondear al step del símbolo
                if symbol_info:
                    volume_step = symbol_info.volume_step
                    volume_to_close = round(volume_to_close / volume_step) * volume_step

                # Determinar tipo de orden de cierre
                order_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY

                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": pos.symbol,
                    "volume": volume_to_close,
                    "type": order_type,
                    "position": pos.ticket,
                    "deviation": 10,
                    "magic": 1001,
                    "comment": f"Reducción Proporcional {self.reduction_percentage}%",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_IOC,
                }

                result = mt5.order_send(request)  # type: ignore
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    successful_reductions += 1
                    log_debug("RiskBot", f"Reducción exitosa en posición {pos.ticket}: {volume_to_close} lotes cerrados", "SUCCESS")
                else:
                    log_debug("RiskBot", f"Error en reducción de posición {pos.ticket}: {result.retcode} - {result.comment}", "ERROR")

            except (FileNotFoundError, PermissionError, IOError) as e:
                log_debug("RiskBot", f"Error procesando reducción de posición {pos.ticket}: {e}", "ERROR")
                log_error_critico("RiskBot", "Reducción Proporcional", f"Error en posición {pos.ticket}: {e}", str(e))

        if successful_reductions > 0:
            self.reduction_triggered_flag = True
            log_debug("RiskBot", f"Reducción proporcional completada: {successful_reductions}/{len(positions)} posiciones reducidas.", "INFO")
            return True
        else:
            log_debug("RiskBot", "No se pudo ejecutar ninguna reducción proporcional.", "ERROR")
            return False

    def _should_activate_breakeven_plus(self):
        """
        Evalúa si se debe activar el Breakeven-Plus después de una reducción proporcional.
        """
        if not self.breakeven_plus_active:
            return False

        remaining_positions = self.get_open_positions()
        return len(remaining_positions) > self.breakeven_plus_min_positions

    def _calculate_pip_value(self, symbol, volume):
        """
        Calcula el valor de un pip para el símbolo y volumen dados.
        """
        try:
            symbol_info = mt5.symbol_info(symbol)  # type: ignore
            if not symbol_info:
                log_debug("RiskBot", f"No se pudo obtener información del símbolo {symbol}", "ERROR")
                return 0.0

            # Para la mayoría de pares forex, el valor del pip es:
            # (0.0001 / precio_actual) * tamaño_contrato * volumen
            # Para pares que terminan en JPY, usar 0.01 en lugar de 0.0001

            tick_info = mt5.symbol_info_tick(symbol)  # type: ignore
            if not tick_info:
                return 0.0

            if "JPY" in symbol:
                pip_size = 0.01
            else:
                pip_size = 0.0001

            # Valor del pip = (pip_size / precio_bid) * tamaño_contrato * volumen
            pip_value = (pip_size / tick_info.bid) * symbol_info.trade_contract_size * volume

            return pip_value

        except (FileNotFoundError, PermissionError, IOError) as e:
            log_debug("RiskBot", f"Error calculando valor pip para {symbol}: {e}", "ERROR")
            return 0.0

    def _apply_breakeven_plus(self):
        """
        Aplica el mecanismo Breakeven-Plus modificando los Stop Loss de todas
        las posiciones restantes para cubrir costes + buffer.
        """
        positions = self.get_open_positions()
        if not positions:
            return False

        successful_modifications = 0
        remaining_lots = sum(float(pos.volume) for pos in positions)
        remaining_commission = remaining_lots * self.comision_por_lote

        log_debug("RiskBot", f"Aplicando Breakeven-Plus a {len(positions)} posiciones restantes.", "INFO")

        for pos in positions:
            try:
                # Calcular el coste total a cubrir por esta posición
                cost_per_position = (remaining_commission + self.breakeven_plus_buffer_usd) / len(positions)

                # Calcular valor de pip para esta posición
                pip_value = self._calculate_pip_value(pos.symbol, pos.volume)
                if pip_value <= 0:
                    log_debug("RiskBot", f"No se pudo calcular valor pip para {pos.symbol}, saltando BE+", "WARNING")
                    continue

                # Calcular pips necesarios para cubrir el coste
                pips_needed = cost_per_position / pip_value

                # Determinar dirección del ajuste según tipo de posición
                if pos.type == mt5.POSITION_TYPE_BUY:
                    # Para BUY, el SL debe estar por debajo del precio de entrada
                    symbol_info = mt5.symbol_info(pos.symbol)  # type: ignore
                    point = symbol_info.point if symbol_info else 0.00001
                    new_sl = pos.price_open - (pips_needed * point * 10)  # *10 para convertir pips a points
                else:
                    # Para SELL, el SL debe estar por encima del precio de entrada
                    symbol_info = mt5.symbol_info(pos.symbol)  # type: ignore
                    point = symbol_info.point if symbol_info else 0.00001
                    new_sl = pos.price_open + (pips_needed * point * 10)

                # Redondear al tick size del símbolo
                if symbol_info:
                    tick_size = symbol_info.trade_tick_size
                    new_sl = round(new_sl / tick_size) * tick_size

                # Modificar la posición
                request = {
                    "action": mt5.TRADE_ACTION_SLTP,
                    "symbol": pos.symbol,
                    "position": pos.ticket,
                    "sl": new_sl,
                    "tp": pos.tp  # Mantener el TP existente
                }

                result = mt5.order_send(request)  # type: ignore
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    successful_modifications += 1
                    log_debug("RiskBot", f"BE+ aplicado a posición {pos.ticket}: nuevo SL = {new_sl}", "SUCCESS")
                else:
                    log_debug("RiskBot", f"Error aplicando BE+ a posición {pos.ticket}: {result.retcode} - {result.comment}", "ERROR")

            except (FileNotFoundError, PermissionError, IOError) as e:
                log_debug("RiskBot", f"Error aplicando BE+ a posición {pos.ticket}: {e}", "ERROR")
                log_error_critico("RiskBot", "Breakeven Plus", f"Error en posición {pos.ticket}: {e}", str(e))

        if successful_modifications > 0:
            log_debug("RiskBot", f"Breakeven-Plus aplicado: {successful_modifications}/{len(positions)} posiciones modificadas.", "INFO")
            return True
        else:
            log_debug("RiskBot", "No se pudo aplicar Breakeven-Plus a ninguna posición.", "ERROR")
            return False

    def _reset_flags_if_no_positions(self):
        """
        Resetea los flags de control cuando no hay posiciones abiertas.
        """
        positions = self.get_open_positions()
        if not positions:
            if self.reduction_triggered_flag:
                log_debug("RiskBot", "Reseteando flags de control - no hay posiciones abiertas.", "INFO")
                self.reduction_triggered_flag = False

    # =========================================================================
    # SECCIÓN 2.3: Método Principal de Chequeo y Acción
    # =========================================================================
    def check_and_act(self, **kwargs):
        """
        Verifica el estado de la cuenta y toma acciones de gestión de riesgo.
        Implementa el flujo de prioridades según la especificación:
        1. Máxima Prioridad: Drawdown y Riesgo Máximo
        2. Prioridad Media: Reducción Proporcional + BE+
        3. Prioridad Baja: Otras estrategias
        """
        # Resetear flags si no hay posiciones
        self._reset_flags_if_no_positions()

        balance = self.get_account_balance()
        p_net_real = self._get_real_net_profit()

        # =====================================================================
        # MÁXIMA PRIORIDAD: SEGURIDAD ABSOLUTA
        # =====================================================================

        # Chequeo de Riesgo Máximo (Stop-Loss flotante)
        if balance > 0 and p_net_real < -(self.risk_percent / 100 * balance):
            log_debug("RiskBot", f"RIESGO MÁXIMO EXCEDIDO. P_net_real: ${p_net_real:.2f}, Límite: {self.risk_percent}% de ${balance:.2f}. Cerrando todas las posiciones.", "CRITICAL")
            self.close_all_positions(motivo_cierre='RIESGO_MAXIMO')
            return 'riesgo'

        # =====================================================================
        # PRIORIDAD MEDIA: TOMA DE GANANCIAS PARCIAL
        # =====================================================================

        # Gestión de posiciones pequeñas (< 0.05 lotes) cuando hay más de 2 posiciones
        positions_count = len(self.get_open_positions())
        if positions_count > 2:
            if self._handle_small_positions_strategy():
                return 'posiciones_pequeñas'

        # Estrategia especial para 2 posiciones (después de limpieza de posiciones pequeñas)
        positions_count = len(self.get_open_positions())  # Recalcular después de posibles cierres
        if positions_count == 2:
            # Usar ganancia mínima más conservadora para esta estrategia
            ganancia_minima_2pos = min(self.risk_target_profit, 15.0)  # Mínimo $10-15
            if self._handle_two_positions_strategy(p_net_real, ganancia_minima_2pos):
                return 'estrategia_2_posiciones'

        # Lógica de Reducción Proporcional (solo si hay más de 2 posiciones)
        positions_count = len(self.get_open_positions())  # Recalcular una vez más
        if positions_count > 2 and self._should_trigger_reduction():
            log_debug("RiskBot", f"Activando Reducción Proporcional. P_net_real: ${p_net_real:.2f}", "INFO")

            if self._execute_proportional_reduction():
                # Si la reducción fue exitosa, evaluar Breakeven-Plus
                if self._should_activate_breakeven_plus():
                    log_debug("RiskBot", "Activando Breakeven-Plus tras reducción proporcional.", "INFO")
                    self._apply_breakeven_plus()
                else:
                    log_debug("RiskBot", f"BE+ no activado: {len(self.get_open_positions())} posiciones restantes (mín: {self.breakeven_plus_min_positions})", "INFO")

                return 'reduccion_proporcional'

        # =====================================================================
        # PRIORIDAD BAJA: OTRAS ESTRATEGIAS DE GANANCIA
        # =====================================================================

        # Cierre por ganancia máxima alcanzada
        if p_net_real >= self.max_profit_target:
            log_debug("RiskBot", f"Ganancia máxima alcanzada. P_net_real: ${p_net_real:.2f}, Objetivo: ${self.max_profit_target:.2f}. Cerrando todas las posiciones.", "INFO")
            self.close_all_positions(motivo_cierre='GANANCIA_MAXIMA')
            return 'ganancia_maxima'

        return 'ok'

    # =========================================================================
    # SECCIÓN 2.4: Propiedades Dinámicas para Dashboard
    # =========================================================================
    @property
    def account_balance(self):
        """Propiedad dinámica que obtiene el balance actual."""
        return self.get_account_balance()

    @property
    def account_equity(self):
        """Propiedad dinámica que obtiene el equity actual."""
        account_info = mt5.account_info()  # type: ignore
        if account_info is None:
            log_debug("RiskBot", "No se pudo obtener la información de la cuenta para equity.", "ERROR")
            return 0.0
        return account_info.equity

    @property
    def positions(self):
        """Propiedad dinámica que obtiene las posiciones abiertas."""
        return self.get_open_positions()

    @property
    def current_profit(self):
        """Propiedad dinámica que obtiene el profit neto real actual."""
        return self._get_real_net_profit()

    @property
    def total_lots(self):
        """Propiedad dinámica que obtiene el total de lotes."""
        _, _, _, total_lots, _ = self.get_total_profit_and_lots()
        return total_lots

    @property
    def real_net_profit(self):
        """Propiedad dinámica que obtiene el profit neto real actual (P_net_real)."""
        return self._get_real_net_profit()

    @property
    def total_swap(self):
        """Propiedad dinámica que obtiene el total de swap."""
        _, _, _, _, total_swap = self.get_total_profit_and_lots()
        return total_swap

    @property
    def total_commission(self):
        """Propiedad dinámica que obtiene la comisión total."""
        _, comision_total, _, _, _ = self.get_total_profit_and_lots()
        return comision_total

    @property
    def current_trigger_threshold(self):
        """Propiedad dinámica que obtiene el umbral actual del trigger."""
        return self.get_current_trigger_value()

    @property
    def reduction_ready(self):
        """Indica si la reducción proporcional está lista para activarse."""
        return self.proportional_reduction_active and not self.reduction_triggered_flag

    @property
    def positions_count(self):
        """Propiedad dinámica que obtiene el número de posiciones abiertas."""
        return len(self.get_open_positions())

    # =========================================================================
    # SECCIÓN 2.5: MÉTODOS DE CONFIGURACIÓN PARA INTERFAZ DE USUARIO
    # =========================================================================

    def configure_proportional_reduction(self, active=None, trigger_mode=None, trigger_value=None, reduction_percentage=None):
        """
        Configura los parámetros de reducción proporcional.

        Args:
            active (bool): Activa/desactiva la estrategia
            trigger_mode (str): 'FixedAmount', 'MaxProfitPercent', 'AccountBalancePercent'
            trigger_value (float): Valor numérico para el modo seleccionado
            reduction_percentage (float): Porcentaje de lotaje a cerrar (ej. 25 para 25%)
        """
        if active is not None:
            self.proportional_reduction_active = active
            log_debug("RiskBot", f"Reducción proporcional {'activada' if active else 'desactivada'}", "INFO")

        if trigger_mode is not None:
            valid_modes = ["FixedAmount", "MaxProfitPercent", "AccountBalancePercent"]
            if trigger_mode in valid_modes:
                self.reduction_trigger_mode = trigger_mode
                log_debug("RiskBot", f"Modo de trigger cambiado a: {trigger_mode}", "INFO")
            else:
                log_debug("RiskBot", f"Modo de trigger inválido: {trigger_mode}. Válidos: {valid_modes}", "ERROR")

        if trigger_value is not None:
            self.reduction_trigger_value = float(trigger_value)
            log_debug("RiskBot", f"Valor de trigger cambiado a: {trigger_value}", "INFO")

        if reduction_percentage is not None:
            self.reduction_percentage = float(reduction_percentage)
            log_debug("RiskBot", f"Porcentaje de reducción cambiado a: {reduction_percentage}%", "INFO")

    def configure_breakeven_plus(self, active=None, min_positions=None, buffer_usd=None):
        """
        Configura los parámetros de Breakeven-Plus.

        Args:
            active (bool): Activa/desactiva BE+
            min_positions (int): Número mínimo de operaciones para activar BE+
            buffer_usd (float): Buffer de seguridad en USD
        """
        if active is not None:
            self.breakeven_plus_active = active
            log_debug("RiskBot", f"Breakeven-Plus {'activado' if active else 'desactivado'}", "INFO")

        if min_positions is not None:
            self.breakeven_plus_min_positions = int(min_positions)
            log_debug("RiskBot", f"Mínimo de posiciones para BE+ cambiado a: {min_positions}", "INFO")

        if buffer_usd is not None:
            self.breakeven_plus_buffer_usd = float(buffer_usd)
            log_debug("RiskBot", f"Buffer de BE+ cambiado a: ${buffer_usd}", "INFO")

    def get_advanced_risk_config(self):
        """
        Retorna la configuración actual de gestión de riesgo avanzado.
        """
        return {
            "proportional_reduction": {
                "active": self.proportional_reduction_active,
                "trigger_mode": self.reduction_trigger_mode,
                "trigger_value": self.reduction_trigger_value,
                "reduction_percentage": self.reduction_percentage,
                "triggered_flag": self.reduction_triggered_flag
            },
            "breakeven_plus": {
                "active": self.breakeven_plus_active,
                "min_positions": self.breakeven_plus_min_positions,
                "buffer_usd": self.breakeven_plus_buffer_usd
            }
        }

    def get_current_trigger_value(self):
        """
        Calcula y retorna el valor actual del trigger según el modo configurado.
        """
        if self.reduction_trigger_mode == "FixedAmount":
            return self.reduction_trigger_value
        elif self.reduction_trigger_mode == "MaxProfitPercent":
            return (self.reduction_trigger_value / 100) * self.max_profit_target
        elif self.reduction_trigger_mode == "AccountBalancePercent":
            balance = self.get_account_balance()
            return (self.reduction_trigger_value / 100) * balance
        else:
            return 0.0

    def reset_reduction_flag(self):
        """
        Método para resetear manualmente el flag de reducción (útil para testing).
        """
        self.reduction_triggered_flag = False
        log_debug("RiskBot", "Flag de reducción reseteado manualmente", "INFO")

    def _handle_two_positions_strategy(self, p_net_real, ganancia_minima=10.0):
        """
        Estrategia inteligente para cuando quedan solo 2 posiciones:
        - Si el profit supera el límite mínimo, cierra la posición menos rentable
        - Para ventas: cierra la más barata (precio más bajo)
        - Para compras: cierra la más cara (precio más alto)

        Args:
            p_net_real: Profit neto real actual
            ganancia_minima: Ganancia mínima para activar esta estrategia

        Returns:
            bool: True si se ejecutó la estrategia, False si no
        """
        try:
            positions = self.get_open_positions()

            # Solo aplicar si hay exactamente 2 posiciones
            if len(positions) != 2:
                return False

            # Verificar que se supere la ganancia mínima
            if p_net_real < ganancia_minima:
                return False

            log_debug("RiskBot", f"Activando estrategia de 2 posiciones. P&L: ${p_net_real:.2f}, Mín: ${ganancia_minima:.2f}", "INFO")

            # Separar posiciones por tipo
            buy_positions = [pos for pos in positions if pos.type == mt5.POSITION_TYPE_BUY]
            sell_positions = [pos for pos in positions if pos.type == mt5.POSITION_TYPE_SELL]

            position_to_close = None

            # Lógica para posiciones de COMPRA
            if len(buy_positions) == 2:
                # Para compras: cerrar la más cara (precio de apertura más alto = menos rentable)
                position_to_close = max(buy_positions, key=lambda p: p.price_open)
                log_debug("RiskBot", f"2 posiciones BUY: cerrando la más cara (${position_to_close.price_open:.5f})", "INFO")

            # Lógica para posiciones de VENTA
            elif len(sell_positions) == 2:
                # Para ventas: cerrar la más barata (precio de apertura más bajo = menos rentable)
                position_to_close = min(sell_positions, key=lambda p: p.price_open)
                log_debug("RiskBot", f"2 posiciones SELL: cerrando la más barata (${position_to_close.price_open:.5f})", "INFO")

            # Lógica para 1 compra + 1 venta
            elif len(buy_positions) == 1 and len(sell_positions) == 1:
                # Cerrar la posición con menor profit individual
                buy_pos = buy_positions[0]
                sell_pos = sell_positions[0]

                # Calcular profit neto de cada posición (incluyendo comisión)
                buy_profit_neto = buy_pos.profit - (buy_pos.volume * self.comision_por_lote)
                sell_profit_neto = sell_pos.profit - (sell_pos.volume * self.comision_por_lote)

                position_to_close = buy_pos if buy_profit_neto <= sell_profit_neto else sell_pos
                log_debug("RiskBot", f"1 BUY + 1 SELL: cerrando la menos rentable (${position_to_close.profit:.2f})", "INFO")

            # Ejecutar cierre de la posición seleccionada
            if position_to_close:
                success = self._close_single_position(position_to_close, "ESTRATEGIA_2_POSICIONES")
                if success:
                    log_debug("RiskBot", f"Posición {position_to_close.ticket} cerrada exitosamente. Queda 1 posición.", "SUCCESS")
                    return True
                else:
                    log_debug("RiskBot", f"Error cerrando posición {position_to_close.ticket}", "ERROR")
                    return False

            return False

        except (FileNotFoundError, PermissionError, IOError) as e:
            log_debug("RiskBot", f"Error en estrategia de 2 posiciones: {e}", "ERROR")
            log_error_critico("RiskBot", "_handle_two_positions_strategy", f"Error: {e}", str(e))
            return False

    def _close_single_position(self, position, motivo_cierre="CIERRE_INDIVIDUAL"):
        """
        Cierra una posición individual de forma segura.

        Args:
            position: Posición de MT5 a cerrar
            motivo_cierre: Motivo del cierre para logging

        Returns:
            bool: True si el cierre fue exitoso, False si no
        """
        try:
            # Determinar tipo de orden opuesta
            order_type = mt5.ORDER_TYPE_SELL if position.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY

            # Crear solicitud de cierre
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": order_type,
                "position": position.ticket,
                "deviation": 10,
                "magic": 1001,
                "comment": f"RiskBot: {motivo_cierre}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            # Enviar orden
            result = mt5.order_send(request)  # type: ignore

            if result.retcode != mt5.TRADE_RETCODE_DONE:
                log_debug("RiskBot", f"Error cerrando posición {position.ticket}: {result.retcode} - {result.comment}", "ERROR")
                return False
            else:
                # Log del cierre exitoso
                profit_neto = position.profit - (position.volume * self.comision_por_lote)
                log_debug("RiskBot", f"Posición {position.ticket} cerrada: ${profit_neto:.2f} neto", "SUCCESS")

                # Log detallado para CSV
                time_apertura_pos_utc = datetime.fromtimestamp(position.time, tz=pytz.utc)
                time_cierre_utc = datetime.utcnow()
                duracion_segundos = (time_cierre_utc - time_apertura_pos_utc).total_seconds()

                log_posicion_cerrada(
                    position.symbol, position.ticket,
                    "BUY" if position.type == mt5.POSITION_TYPE_BUY else "SELL",
                    position.volume, position.price_open, result.price,
                    profit_neto, motivo_cierre
                )

                return True

        except (FileNotFoundError, PermissionError, IOError) as e:
            log_debug("RiskBot", f"Excepción cerrando posición {position.ticket}: {e}", "ERROR")
            log_error_critico("RiskBot", "_close_single_position", f"Error: {e}", str(e))
            return False

    # =========================================================================
    # SECCIÓN 2.2.1: GESTIÓN DE RIESGO AVANZADO - REDUCCIÓN PROPORCIONAL
    # =========================================================================
    def _handle_small_positions_strategy(self):
        """
        Gestiona posiciones pequeñas (< 0.05 lotes) cuando hay más de 2 operaciones.

        Si encuentra posiciones pequeñas:
        1. Las cierra completamente
        2. Si están en pérdida, cubre la pérdida cerrando parcialmente otras posiciones
        3. Asegura cubrir: pérdida + comisiones + $3 de buffer

        Returns:
            bool: True si se ejecutó alguna acción, False si no
        """
        try:
            positions = self.get_open_positions()

            # Solo aplicar si hay más de 2 posiciones
            if len(positions) <= 2:
                return False

            # Buscar posiciones pequeñas (< 0.05 lotes)
            small_positions = [pos for pos in positions if pos.volume < 0.05]

            if not small_positions:
                return False

            log_debug("RiskBot", f"Encontradas {len(small_positions)} posiciones pequeñas (< 0.05 lotes)", "INFO")

            total_actions = 0

            for small_pos in small_positions:
                try:
                    # Calcular profit neto de la posición pequeña (incluyendo comisión)
                    small_pos_profit = small_pos.profit - (small_pos.volume * self.comision_por_lote)

                    log_debug("RiskBot", f"Procesando posición pequeña {small_pos.ticket}: {small_pos.volume} lotes, P&L: ${small_pos_profit:.2f}", "INFO")

                    # Cerrar la posición pequeña
                    if self._close_single_position(small_pos, "POSICION_PEQUEÑA"):
                        total_actions += 1

                        # Si estaba en pérdida, cubrir la pérdida
                        if small_pos_profit < 0:
                            loss_to_cover = abs(small_pos_profit)
                            buffer_amount = 3.0  # $3 de buffer adicional
                            total_to_cover = loss_to_cover + buffer_amount

                            log_debug("RiskBot", f"Posición pequeña en pérdida: ${loss_to_cover:.2f}. Cubriendo pérdida + ${buffer_amount:.2f} buffer", "INFO")

                            # Cubrir la pérdida cerrando parcialmente otras posiciones
                            if self._cover_loss_with_partial_closures(total_to_cover, small_pos.ticket):
                                log_debug("RiskBot", f"Pérdida de ${total_to_cover:.2f} cubierta exitosamente", "SUCCESS")
                            else:
                                log_debug("RiskBot", f"No se pudo cubrir completamente la pérdida de ${total_to_cover:.2f}", "WARNING")
                        else:
                            log_debug("RiskBot", f"Posición pequeña cerrada con ganancia: ${small_pos_profit:.2f}", "SUCCESS")

                except (FileNotFoundError, PermissionError, IOError) as e:
                    log_debug("RiskBot", f"Error procesando posición pequeña {small_pos.ticket}: {e}", "ERROR")
                    log_error_critico("RiskBot", "_handle_small_positions_strategy", f"Error en posición {small_pos.ticket}: {e}", str(e))

            if total_actions > 0:
                log_debug("RiskBot", f"Estrategia de posiciones pequeñas completada: {total_actions} posiciones procesadas", "INFO")
                return True

            return False

        except (FileNotFoundError, PermissionError, IOError) as e:
            log_debug("RiskBot", f"Error en estrategia de posiciones pequeñas: {e}", "ERROR")
            log_error_critico("RiskBot", "_handle_small_positions_strategy", f"Error: {e}", str(e))
            return False

    def _cover_loss_with_partial_closures(self, amount_to_cover: float, excluded_ticket: int):
        """
        Cubre una pérdida cerrando parcialmente otras posiciones rentables.

        Args:
            amount_to_cover: Cantidad en USD que se necesita cubrir
            excluded_ticket: Ticket de la posición a excluir (ya cerrada)

        Returns:
            bool: True si se cubrió exitosamente la pérdida, False si no
        """
        try:
            # Obtener posiciones actuales (excluyendo la que ya se cerró)
            all_positions = self.get_open_positions()
            positions = [pos for pos in all_positions if pos.ticket != excluded_ticket]

            if not positions:
                log_debug("RiskBot", "No hay posiciones disponibles para cubrir pérdida", "WARNING")
                return False

            # Filtrar solo posiciones rentables
            profitable_positions = [
                pos for pos in positions
                if (pos.profit - (pos.volume * self.comision_por_lote)) > 0
            ]

            if not profitable_positions:
                log_debug("RiskBot", "No hay posiciones rentables para cubrir pérdida", "WARNING")
                return False

            # Ordenar por rentabilidad descendente (más rentables primero)
            profitable_positions.sort(
                key=lambda p: p.profit - (p.volume * self.comision_por_lote),
                reverse=True
            )

            total_covered = 0.0
            positions_used = 0

            for pos in profitable_positions:
                if total_covered >= amount_to_cover:
                    break

                try:
                    # Calcular cuánto necesitamos cubrir
                    remaining_to_cover = amount_to_cover - total_covered

                    # Calcular profit neto de esta posición
                    pos_profit_neto = pos.profit - (pos.volume * self.comision_por_lote)

                    # Calcular el porcentaje a cerrar (máximo 50% por posición para no cerrar todo)
                    max_closure_percentage = 0.5  # 50% máximo
                    max_profit_to_use = pos_profit_neto * max_closure_percentage

                    # Determinar cuánto cerrar de esta posición
                    profit_to_use = min(remaining_to_cover, max_profit_to_use)

                    if profit_to_use <= 0:
                        continue

                    # Calcular volumen a cerrar basado en el profit que queremos obtener
                    volume_percentage = profit_to_use / pos_profit_neto
                    volume_to_close = pos.volume * volume_percentage

                    # Asegurar volumen mínimo del símbolo
                    symbol_info = mt5.symbol_info(pos.symbol)  # type: ignore
                    if symbol_info and volume_to_close < symbol_info.volume_min:
                        volume_to_close = symbol_info.volume_min

                    # No cerrar más del 50% del volumen original
                    max_volume_to_close = pos.volume * max_closure_percentage
                    volume_to_close = min(volume_to_close, max_volume_to_close)

                    # Redondear al step del símbolo
                    if symbol_info:
                        volume_to_close = round(volume_to_close / symbol_info.volume_step) * symbol_info.volume_step

                    # Ejecutar cierre parcial
                    if volume_to_close > 0 and volume_to_close <= pos.volume:
                        if self._close_partial_position(pos, volume_to_close, f"CUBRIR_PERDIDA_{excluded_ticket}"):
                            # Estimar profit obtenido del cierre parcial
                            estimated_profit = (pos.profit / pos.volume) * volume_to_close
                            estimated_profit_neto = estimated_profit - (volume_to_close * self.comision_por_lote)

                            total_covered += estimated_profit_neto
                            positions_used += 1

                            log_debug("RiskBot", f"Cierre parcial exitoso: {volume_to_close:.2f} lotes de {pos.ticket}, profit estimado: ${estimated_profit_neto:.2f}", "SUCCESS")
                        else:
                            log_debug("RiskBot", f"Error en cierre parcial de posición {pos.ticket}", "ERROR")

                except (FileNotFoundError, PermissionError, IOError) as e:
                    log_debug("RiskBot", f"Error procesando posición {pos.ticket} para cubrir pérdida: {e}", "ERROR")
                    continue

            success = total_covered >= (amount_to_cover * 0.9)  # 90% de cobertura mínima

            if success:
                log_debug("RiskBot", f"Pérdida cubierta exitosamente: ${total_covered:.2f} de ${amount_to_cover:.2f} usando {positions_used} posiciones", "SUCCESS")
            else:
                log_debug("RiskBot", f"Cobertura parcial: ${total_covered:.2f} de ${amount_to_cover:.2f} usando {positions_used} posiciones", "WARNING")

            return success

        except (FileNotFoundError, PermissionError, IOError) as e:
            log_debug("RiskBot", f"Error cubriendo pérdida: {e}", "ERROR")
            log_error_critico("RiskBot", "_cover_loss_with_partial_closures", f"Error: {e}", str(e))
            return False

    def _close_partial_position(self, position, volume_to_close: float, motivo_cierre: str = "CIERRE_PARCIAL"):
        """
        Cierra parcialmente una posición con el volumen especificado.

        Args:
            position: Posición de MT5 a cerrar parcialmente
            volume_to_close: Volumen a cerrar
            motivo_cierre: Motivo del cierre para logging

        Returns:
            bool: True si el cierre fue exitoso, False si no
        """
        try:
            if volume_to_close <= 0 or volume_to_close > position.volume:
                log_debug("RiskBot", f"Volumen inválido para cierre parcial: {volume_to_close} (pos volume: {position.volume})", "ERROR")
                return False

            # Determinar tipo de orden opuesta
            order_type = mt5.ORDER_TYPE_SELL if position.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY

            # Crear solicitud de cierre parcial
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": position.symbol,
                "volume": volume_to_close,
                "type": order_type,
                "position": position.ticket,
                "deviation": 10,
                "magic": 1001,
                "comment": f"RiskBot: {motivo_cierre}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            # Enviar orden
            result = mt5.order_send(request)  # type: ignore

            if result.retcode != mt5.TRADE_RETCODE_DONE:
                log_debug("RiskBot", f"Error en cierre parcial {position.ticket}: {result.retcode} - {result.comment}", "ERROR")
                return False
            else:
                # Calcular profit del cierre parcial
                partial_profit = (position.profit / position.volume) * volume_to_close
                partial_profit_neto = partial_profit - (volume_to_close * self.comision_por_lote)

                log_debug("RiskBot", f"Cierre parcial exitoso {position.ticket}: {volume_to_close:.2f} lotes, profit: ${partial_profit_neto:.2f}", "SUCCESS")
                return True

        except (FileNotFoundError, PermissionError, IOError) as e:
            log_debug("RiskBot", f"Excepción en cierre parcial {position.ticket}: {e}", "ERROR")
            log_error_critico("RiskBot", "_close_partial_position", f"Error: {e}", str(e))
            return False

    # =========================================================================
    # SECCIÓN 2.2.1: GESTIÓN DE RIESGO AVANZADO - REDUCCIÓN PROPORCIONAL
    # =========================================================================
