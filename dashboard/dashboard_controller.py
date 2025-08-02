#!/usr/bin/env python3
"""
Dashboard Controller - Integración Total con Motor de Trading
============================================================
Controlador central que conecta todos los dashboards con el motor de trading principal.
Proporciona comunicación bidireccional y estado compartido en tiempo real.

Características:
- Integración directa con SentinelApp
- Estado compartido entre dashboard y trading engine  
- Control en tiempo real del sistema de trading
- WebSocket support para dashboards web
- Thread-safe communication
"""

import threading
import queue
from datetime import datetime
from dataclasses import dataclass, asdict, field
from json import JSONDecodeError
from typing import Dict, Any, Optional, Callable, List
import time

# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log, log_dashboard

# 🎯 INTEGRACIÓN ACC - CENTRO DE MANDO DE ANÁLISIS  
from core.analysis_command_center import AnalysisOrchestrator
# run_comprehensive_analysis reservado para futuras extensiones

@dataclass
class DashboardState:
    """Estado compartido del dashboard"""
    # Estados del sistema
    trading_active: bool = False
    dashboard_active: bool = False
    mt5_connected: bool = False
    
    # Datos de mercado
    current_price: float = 0.0
    spread: float = 0.0
    
    # 🔧 CORRECCIÓN CRÍTICA: Usar factory functions para tipos mutables
    # Esto elimina completamente los errores de tipado y es thread-safe
    symbols: List[str] = field(default_factory=list)
    
    # Análisis ICT
    ict_results: Dict[str, Any] = field(default_factory=dict)
    poi_results: Dict[str, Any] = field(default_factory=dict)
    
    # 🎯 ACC - CENTRO DE MANDO DE ANÁLISIS
    acc_analysis: Dict[str, Any] = field(default_factory=dict)
    acc_performance: Dict[str, Any] = field(default_factory=dict)
    acc_status: str = "INITIALIZED"
    
    # Métricas del sistema
    cycle_count: int = 0
    uptime: float = 0.0
    last_update: str = ""
    
    # Estados de riesgo
    positions_open: int = 0
    grid_active: bool = False
    risk_level: str = "LOW"
    
    # Logs y alertas
    recent_logs: List[Dict[str, Any]] = field(default_factory=list)
    alerts: List[Dict[str, Any]] = field(default_factory=list)

class DashboardController:
    """
    Controlador central para integración dashboard-trading engine
    """
    
    def __init__(self):
        # SLUC v2.0: logging centralizado
        
        # Estado compartido
        self.state = DashboardState()
        self.state_lock = threading.RLock()
        
        # 🎯 INICIALIZAR ACC - CENTRO DE MANDO DE ANÁLISIS
        self.acc_orchestrator = AnalysisOrchestrator(
            enable_cache=True,
            max_concurrent_analyses=2,
            default_timeout_seconds=30
        )
        
        # Comunicación
        self.command_queue = queue.Queue()
        self.update_queue = queue.Queue()
        self.callbacks: Dict[str, Callable] = {}
        
        # Control de threads
        self.running = False
        self.update_thread = None
        
        # Referencias
        self.sentinel_app = None  # Referencia al app principal
        self.active_dashboards: Dict[str, Any] = {}
        
        # Métricas
        self.start_time = time.time()
        self.updates_sent = 0
        self.commands_processed = 0
        
        # 📝 LOG INICIALIZACIÓN ACC
        enviar_senal_log(
            "INFO", 
            "🎯 Dashboard Controller inicializado con ACC - Centro de Mando activado", 
            __name__, 
            "general"
        )
        
    def connect_sentinel_app(self, sentinel_app):
        """Conectar con la aplicación principal de trading"""
        self.sentinel_app = sentinel_app
        enviar_senal_log("INFO", "✅ Dashboard Controller conectado a SentinelApp", __name__, "general")
        
        # Inicializar estado desde el app
        self._sync_state_from_app()
        
    def register_dashboard(self, dashboard_id: str, dashboard_instance):
        """Registrar un dashboard para recibir actualizaciones"""
        self.active_dashboards[dashboard_id] = dashboard_instance
        enviar_senal_log("INFO", f"📊 Dashboard registrado: {dashboard_id}", __name__, "general")
        
    def unregister_dashboard(self, dashboard_id: str):
        """Desregistrar dashboard"""
        if dashboard_id in self.active_dashboards:
            del self.active_dashboards[dashboard_id]
            enviar_senal_log("INFO", f"📊 Dashboard desregistrado: {dashboard_id}", __name__, "general")
    
    def start(self):
        """Iniciar el controlador"""
        if not self.running:
            self.running = True
            self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
            self.update_thread.start()
            enviar_senal_log("INFO", "🚀 Dashboard Controller iniciado", __name__, "general")
    
    def stop(self):
        """Detener el controlador"""
        self.running = False
        if self.update_thread:
            self.update_thread.join(timeout=2)
        enviar_senal_log("INFO", "🛑 Dashboard Controller detenido", __name__, "general")
    
    def _update_loop(self):
        """Loop principal de actualización"""
        while self.running:
            try:
                # Procesar comandos entrantes
                self._process_commands()
                
                # Actualizar estado desde el app principal
                if self.sentinel_app:
                    self._sync_state_from_app()
                
                # Enviar actualizaciones a dashboards
                self._broadcast_updates()
                
                time.sleep(1.5)  # 0.67 Hz update rate - más estable para TUI
                
            except (JSONDecodeError, ValueError) as e:
                enviar_senal_log("ERROR", f"Error en update loop: {e}", __name__, "general")
                time.sleep(1)
    
    def _process_commands(self):
        """Procesar comandos desde dashboards"""
        while not self.command_queue.empty():
            try:
                command = self.command_queue.get_nowait()
                self._execute_command(command)
                self.commands_processed += 1
            except queue.Empty:
                break
            except (JSONDecodeError, ValueError) as e:
                enviar_senal_log("ERROR", f"Error procesando comando: {e}", __name__, "general")
    
    def _execute_command(self, command: Dict[str, Any]):
        """Ejecutar comando específico"""
        cmd_type = command.get('type')
        # cmd_data = command.get('data', {})  # Reservado para futuras extensiones
        
        enviar_senal_log("INFO", f"⚡ Ejecutando comando: {cmd_type}", __name__, "general")
        
        if cmd_type == 'START_TRADING':
            if self.sentinel_app:
                # Comando para iniciar trading
                pass
        
        elif cmd_type == 'STOP_TRADING':
            if self.sentinel_app:
                # Comando para detener trading
                pass
        
        elif cmd_type == 'UPDATE_PARAMS':
            if self.sentinel_app:
                # Actualizar parámetros del sistema
                # params = cmd_data.get('params', {})
                # self.sentinel_app.update_parameters(params)
                pass
        
        elif cmd_type == 'FORCE_ANALYSIS':
            if self.sentinel_app:
                # Forzar nuevo análisis
                pass
        
        elif cmd_type == 'EMERGENCY_STOP':
            if self.sentinel_app:
                # Parada de emergencia
                pass
        
        # ✨ COMANDOS ESPECÍFICOS DE HIBERNACIÓN ✨
        elif cmd_type == 'TOGGLE_EMERGENCY':
            if self.sentinel_app and hasattr(self.sentinel_app, 'system_status'):
                # Alternar modo de emergencia
                status = self.sentinel_app.system_status
                status.emergency_mode = not getattr(status, 'emergency_mode', False)
                enviar_senal_log("INFO", f"🚨 Modo emergencia: {status.emergency_mode}", __name__, "general")
        
        elif cmd_type == 'ADD_SIM_POSITION':
            if self.sentinel_app and hasattr(self.sentinel_app, 'system_status'):
                # Agregar posición simulada para testing
                status = self.sentinel_app.system_status
                current_positions = getattr(status, 'positions_open', 0)
                status.positions_open = current_positions + 1
                enviar_senal_log("INFO", f"📊 Posiciones simuladas: {status.positions_open}", __name__, "general")
        
        elif cmd_type == 'CLEAR_POSITIONS':
            if self.sentinel_app and hasattr(self.sentinel_app, 'system_status'):
                # Limpiar posiciones simuladas
                status = self.sentinel_app.system_status
                status.positions_open = 0
                enviar_senal_log("INFO", "🧹 Posiciones simuladas limpiadas", __name__, "general")
        
        elif cmd_type == 'RESTART_DEMO':
            if self.sentinel_app:
                # Reiniciar demo (resetear estados)
                if hasattr(self.sentinel_app, 'system_status'):
                    status = self.sentinel_app.system_status
                    status.positions_open = 0
                    status.emergency_mode = False
                    status.riskbot_active = False
                    status.grid_active = False
                enviar_senal_log("INFO", "🔄 Demo reiniciada", __name__, "general")
        
    def _execute_acc_analysis(self):
        """
        🎯 Ejecuta análisis completo via ACC (Analysis Command Center)
        - Caja Negra: Sin salida terminal, logging exhaustivo
        - Centraliza: ICT, POI, Confidence, Veredicto, TCT
        """
        try:
            # Obtener símbolo actual
            current_symbol = getattr(self.sentinel_app, 'current_symbol', 'EURUSD')
            
            # Obtener timeframes (por defecto análisis integral)
            analysis_timeframes = ['M1', 'M5', 'M15', 'H1', 'H4', 'D1']
            
            enviar_senal_log("INFO", f"🎯 ACC INICIANDO análisis completo para {current_symbol}", __name__, "acc")
            
            # 🎯 LLAMADA CENTRAL AL ACC
            acc_result = self.acc_orchestrator.run_full_analysis_cycle(
                symbol=current_symbol,
                timeframes=analysis_timeframes
            )
            
            # Inyectar resultados en estado del dashboard
            self.state.acc_analysis = acc_result.dashboard_payload
            self.state.acc_performance = {
                'success_rate': acc_result.overall_success_rate,
                'execution_time': acc_result.total_execution_time_ms,
                'quality_score': acc_result.analysis_quality_score,
                'components': len(acc_result.component_results)
            }
            # Agregar dashboard_payload al state si no existe
            if not hasattr(self.state, 'dashboard_payload'):
                self.state.__dict__['dashboard_payload'] = acc_result.dashboard_payload
            
            # Telemetría de éxito
            enviar_senal_log('INFO', "ACC COMPLETADO - Dashboard actualizado con análisis unificado", __name__, "dashboard")
            
        except (ConnectionError, ValueError, KeyError) as e:
            enviar_senal_log('ERROR', f"ACC ERROR en análisis: {str(e)}", __name__, "dashboard")
            
            # Valores por defecto en caso de error
            self.state.acc_analysis = {}
            self.state.acc_performance = {}
            if not hasattr(self.state, 'dashboard_payload'):
                self.state.__dict__['dashboard_payload'] = {}

    def _sync_state_from_app(self):
        """Sincronizar estado desde la aplicación principal"""
        if not self.sentinel_app:
            return
            
        try:
            with self.state_lock:
                # Datos básicos
                self.state.trading_active = getattr(self.sentinel_app, 'running', False)
                self.state.current_price = getattr(self.sentinel_app, 'current_price', 0.0)
                self.state.spread = getattr(self.sentinel_app, 'spread', 0.0)
                self.state.cycle_count = getattr(self.sentinel_app, 'cycle_count', 0)
                
                # Estados MT5
                self.state.mt5_connected = True  # Asumir conectado si tenemos datos
                
                # Análisis ICT (LEGACY - Mantenido para compatibilidad)
                if hasattr(self.sentinel_app, 'ict_cache'):
                    self.state.ict_results = self.sentinel_app.ict_cache or {}
                
                # 🎯 ACC - ANÁLISIS COMPLETO CON CENTRO DE MANDO
                self._execute_acc_analysis()
                
                # Estados de riesgo
                if hasattr(self.sentinel_app, 'riskbot') and self.sentinel_app.riskbot:
                    self.state.positions_open = len(getattr(self.sentinel_app.riskbot, 'positions', []))
                    self.state.grid_active = getattr(self.sentinel_app.riskbot, 'grid_active', False)
                
                # ✨ DATOS ESPECÍFICOS DE HIBERNACIÓN ✨
                # Fase del sistema
                if hasattr(self.sentinel_app, 'current_phase'):
                    phase = getattr(self.sentinel_app, 'current_phase')
                    if hasattr(phase, 'value'):
                        self.state.__dict__['system_phase'] = phase.value
                    else:
                        self.state.__dict__['system_phase'] = str(phase)
                
                # Datos de hibernación desde system_status
                if hasattr(self.sentinel_app, 'system_status'):
                    status = self.sentinel_app.system_status
                    self.state.positions_open = getattr(status, 'positions_open', 0)
                    self.state.__dict__['emergency_mode'] = getattr(status, 'emergency_mode', False)
                    self.state.__dict__['cpu_usage'] = getattr(status, 'cpu_usage', 0.0)
                    self.state.__dict__['riskbot_active'] = getattr(status, 'riskbot_active', False)
                    self.state.grid_active = getattr(status, 'grid_active', False)
                
                # Próxima sesión y countdown
                if hasattr(self.sentinel_app, 'get_next_session_countdown'):
                    try:
                        countdown_result = self.sentinel_app.get_next_session_countdown()
                        
                        # Validar que obtenemos exactamente 3 valores
                        if isinstance(countdown_result, (tuple, list)) and len(countdown_result) == 3:
                            hours, minutes, seconds = countdown_result
                            from datetime import timedelta
                            total_timedelta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                            self.state.__dict__['time_to_next_session'] = total_timedelta
                            self.state.__dict__['next_session_name'] = 'LONDRES'
                        else:
                            # Fallback silencioso con valores por defecto
                            self.state.__dict__['time_to_next_session'] = timedelta(hours=1, minutes=0, seconds=0)
                            self.state.__dict__['next_session_name'] = 'PRÓXIMA'
                    except (JSONDecodeError, ValueError):
                        # Error ya manejado - fallback silencioso sin logging repetitivo
                        self.state.__dict__['time_to_next_session'] = timedelta(hours=1, minutes=0, seconds=0)
                        self.state.__dict__['next_session_name'] = 'PRÓXIMA'
                
                # Timeframes data
                if hasattr(self.sentinel_app, 'df_by_timeframe'):
                    # Convertir DataFrames a información útil para dashboard
                    pass
                
                # Timestamps
                self.state.uptime = time.time() - self.start_time
                self.state.last_update = datetime.now().strftime("%H:%M:%S")
                self.state.dashboard_active = True
                
        except (JSONDecodeError, ValueError) as e:
            enviar_senal_log("ERROR", f"Error sincronizando estado: {e}", __name__, "general")
    
    def _broadcast_updates(self):
        """Enviar actualizaciones a todos los dashboards activos"""
        if not self.active_dashboards:
            return
        
        try:
            # Preparar datos para envío
            state_dict = asdict(self.state)
            
            # Enviar a cada dashboard registrado
            for dashboard_id, dashboard in self.active_dashboards.items():
                try:
                    if hasattr(dashboard, 'update_from_controller'):
                        dashboard.update_from_controller(state_dict)
                    self.updates_sent += 1
                except (JSONDecodeError, ValueError) as e:
                    enviar_senal_log("ERROR", f"Error enviando update a {dashboard_id}: {e}", __name__, "general")
                    
        except (JSONDecodeError, ValueError) as e:
            enviar_senal_log("ERROR", f"Error en broadcast: {e}", __name__, "general")
    
    # API Pública para dashboards
    def send_command(self, command_type: str, data: Optional[Dict[str, Any]] = None):
        """Enviar comando al sistema de trading"""
        command = {
            'type': command_type,
            'data': data or {},
            'timestamp': datetime.now().isoformat()
        }
        self.command_queue.put(command)
        enviar_senal_log("INFO", f"📤 Comando enviado: {command_type}", __name__, "general")
    
    def get_state(self) -> Dict[str, Any]:
        """Obtener estado actual del sistema"""
        with self.state_lock:
            return asdict(self.state)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Obtener métricas del controlador"""
        return {
            'uptime': time.time() - self.start_time,
            'updates_sent': self.updates_sent,
            'commands_processed': self.commands_processed,
            'active_dashboards': len(self.active_dashboards),
            'last_sync': self.state.last_update
        }
    
    def add_alert(self, message: str, alert_type: str = "INFO"):
        """Agregar alerta al sistema"""
        alert = {
            'message': message,
            'type': alert_type,
            'timestamp': datetime.now().isoformat(),
            'id': f"alert_{int(time.time() * 1000)}"
        }
        
        with self.state_lock:
            self.state.alerts.append(alert)
            # Mantener solo las últimas 20 alertas
            if len(self.state.alerts) > 20:
                self.state.alerts = self.state.alerts[-20:]
    
    def add_log_entry(self, level: str, message: str, source: str = "SYSTEM"):
        """Agregar entrada de log"""
        log_entry = {
            'level': level,
            'message': message,
            'source': source,
            'timestamp': datetime.now().isoformat()
        }
        
        with self.state_lock:
            self.state.recent_logs.append(log_entry)
            # Mantener solo los últimos 50 logs
            if len(self.state.recent_logs) > 50:
                self.state.recent_logs = self.state.recent_logs[-50:]

    def update_market_data(self, market_data: Dict[str, Any]):
        """
        Actualiza el estado con nuevos datos del mercado y notifica a dashboards
        
        Args:
            market_data: Diccionario con datos del mercado:
                - current_price: Precio actual
                - historical_candles: DataFrame con velas históricas  
                - pois: Lista de POIs detectados
                - market_analysis: Análisis de estructura
                - symbol: Símbolo del activo
                - last_update: Timestamp de actualización
        """
        # LOG CRÍTICO: RECEPCIÓN DE DATOS EN EL CONTROLLER
        pois_count = len(market_data.get('pois', [])) if market_data.get('pois') else 0
        analysis_keys = list(market_data.get('market_analysis', {}).keys()) if market_data.get('market_analysis') else []
        
        enviar_senal_log("INFO", ">>> [DASHBOARD-CONTROLLER] Paquete de datos RECIBIDO del app principal", __name__, "general")
        enviar_senal_log("INFO", "    📦 Contenido recibido:", __name__, "general")
        
        # Analizar current_price
        if 'current_price' in market_data:
            price_info = market_data['current_price']
            if isinstance(price_info, dict) and 'bid' in price_info:
                current_price_val = price_info['bid']
            elif isinstance(price_info, (int, float)):
                current_price_val = price_info
            else:
                current_price_val = "FORMATO_DESCONOCIDO"
            enviar_senal_log("INFO", f"       💰 Precio: {current_price_val}", __name__, "general")
        
        # Analizar historical_candles
        candles_info = "N/A"
        if 'historical_candles' in market_data and market_data['historical_candles'] is not None:
            candles_df = market_data['historical_candles']
            if hasattr(candles_df, '__len__'):
                candles_info = f"{len(candles_df)} velas"
        enviar_senal_log("INFO", f"       📊 Velas: {candles_info}", __name__, "general")
        
        enviar_senal_log("INFO", f"       🎯 POIs: {pois_count}", __name__, "general")
        enviar_senal_log("INFO", f"       📈 Análisis: {len(analysis_keys)} métricas ({', '.join(analysis_keys)})", __name__, "general")
        enviar_senal_log("INFO", f"       🕐 Timestamp: {market_data.get('last_update', 'NO_TIMESTAMP')}", __name__, "general")
        
        try:
            with self.state_lock:
                # Actualizar precio actual
                if 'current_price' in market_data:
                    price = market_data['current_price']
                    if isinstance(price, (int, float)):
                        self.state.current_price = float(price)
                    elif hasattr(price, 'bid') and hasattr(price, 'ask'):
                        self.state.current_price = (price.bid + price.ask) / 2
                    elif isinstance(price, dict) and 'bid' in price:
                        self.state.current_price = float(price['bid'])
                
                # Actualizar datos ICT/POI
                if 'pois' in market_data:
                    self.state.poi_results = {
                        'pois': market_data['pois'],
                        'count': len(market_data['pois']),
                        'last_update': market_data.get('last_update', datetime.now().isoformat())
                    }
                
                if 'market_analysis' in market_data:
                    self.state.ict_results = market_data['market_analysis']
                
                # Actualizar timestamp
                self.state.last_update = market_data.get('last_update', datetime.now().isoformat())
                
                # Incrementar contador de ciclos
                self.state.cycle_count += 1
            
            enviar_senal_log("INFO", "    ✅ Estado interno del controller ACTUALIZADO exitosamente", __name__, "general")
            enviar_senal_log("INFO", f"       Estado interno: Precio={getattr(self.state, 'current_price', 'N/A')}, Ciclo={getattr(self.state, 'cycle_count', 'N/A')}", __name__, "general")
            
            # Notificar a dashboards registrados que tengan método de actualización
            enviar_senal_log("INFO", f"🔄 [DASHBOARD-NOTIFY] Iniciando notificación a {len(self.active_dashboards)} dashboards registrados", __name__, "general")
            self._notify_dashboards_market_update(market_data)
            enviar_senal_log("INFO", "<<< [DASHBOARD-NOTIFY] Notificación a dashboards COMPLETADA", __name__, "general")
            
            enviar_senal_log("DEBUG", f"Market data updated - Price: {self.state.current_price}, POIs: {len(market_data.get('pois', []))}", __name__, "general")
            
        except (JSONDecodeError, ValueError) as e:
            enviar_senal_log("ERROR", f"🚨 [DASHBOARD-CONTROLLER-ERROR] Error crítico actualizando datos: {e}", __name__, "general")

    def _notify_dashboards_market_update(self, market_data: Dict[str, Any]):
        """Notifica a dashboards sobre actualización de datos del mercado"""
        enviar_senal_log("INFO", f"🔔 [WIDGET-DISTRIBUTION] Distribuyendo datos a {len(self.active_dashboards)} dashboards activos", __name__, "general")
        
        successful_notifications = 0
        failed_notifications = 0
        
        for dashboard_id, dashboard in self.active_dashboards.items():
            dashboard_type = type(dashboard).__name__
            
            try:
                # Verificar si el dashboard tiene método para actualizar datos ICT
                if hasattr(dashboard, 'update_professional_ict_data'):
                    enviar_senal_log("INFO", f"   📊 [WIDGET-UPDATE] Actualizando {dashboard_type} (ID: {dashboard_id})", __name__, "general")
                    dashboard.update_professional_ict_data(market_data)
                    enviar_senal_log("INFO", f"   ✅ [WIDGET-SUCCESS] {dashboard_type} actualizado exitosamente", __name__, "general")
                    successful_notifications += 1
                    
                elif hasattr(dashboard, 'refresh_hibernation_analysis'):
                    enviar_senal_log("INFO", f"   🛌 [WIDGET-UPDATE] Actualizando {dashboard_type} (ID: {dashboard_id})", __name__, "general")
                    dashboard.refresh_hibernation_analysis()
                    enviar_senal_log("INFO", f"   ✅ [WIDGET-SUCCESS] {dashboard_type} refrescado exitosamente", __name__, "general")
                    successful_notifications += 1
                    
                elif hasattr(dashboard, 'update_from_controller'):
                    enviar_senal_log("INFO", f"   🔄 [WIDGET-UPDATE] Actualizando {dashboard_type} (ID: {dashboard_id})", __name__, "general")
                    # Método genérico para widgets
                    dashboard.update_from_controller(self.get_state())
                    enviar_senal_log("INFO", f"   ✅ [WIDGET-SUCCESS] {dashboard_type} actualizado con estado del controller", __name__, "general")
                    successful_notifications += 1
                    
                else:
                    enviar_senal_log("WARNING", f"   ⚠️ [WIDGET-SKIP] {dashboard_type} (ID: {dashboard_id})", __name__, "general")
                    
            except (JSONDecodeError, ValueError) as e:
                failed_notifications += 1
                enviar_senal_log("ERROR", f"   🚨 [WIDGET-ERROR] Error notificando a {dashboard_type} (ID: {dashboard_id}): {e}", __name__, "general")
        
        enviar_senal_log("INFO", f"📈 [WIDGET-SUMMARY] Distribución completada: {successful_notifications} exitosas, {failed_notifications} fallidas", __name__, "general")

# Instancia global del controlador
dashboard_controller = DashboardController()

def get_dashboard_controller() -> DashboardController:
    """Obtener instancia global del controlador"""
    return dashboard_controller
