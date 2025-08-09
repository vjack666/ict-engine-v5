#!/usr/bin/env python3
"""
🔴 ICT ENTERPRISE DASHBOARD - BLACKBOX LOGGER SUPER DETALLADO
================================================================================
Sistema de logging tipo "caja negra" ultra detallado para diagnosticar problemas
en el dashboard ICT Enterprise, especialmente problemas con pestañas y contenido.

🎯 OBJETIVO: Detectar exactamente por qué fallan las pestañas y el contenido
de las ventanas en ict_enterprise_dashboard.py

🔍 CARACTERÍSTICAS:
- Logging de TODAS las llamadas a funciones
- Registro detallado de estados de UI
- Tracking de datos de velas y procesamiento
- Análisis de errores con stack traces
- Logs separados por categorías (UI, Data, Errors, etc.)
- Reportes automáticos de debugging
================================================================================
"""

import logging
import traceback
import inspect
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class ICTDashboardBlackBox:
    """
    🔴 CAJA NEGRA ULTRA DETALLADA para ICT Enterprise Dashboard
    
    Sistema que registra TODO lo que sucede en el dashboard para diagnosticar
    exactamente por qué las pestañas no muestran contenido.
    """
    
    def __init__(self, session_name="ICT_Dashboard_BlackBox"):
        self.session_name = session_name
        self.session_id = datetime.now().strftime("BB_%Y%m%d_%H%M%S")
        self.start_time = time.time()
        
        # Crear estructura de directorios para logs
        self.base_log_dir = Path("logs") / "blackbox" / self.session_id
        self.base_log_dir.mkdir(parents=True, exist_ok=True)
        
        # Contadores de eventos
        self.counters = {
            "function_calls": 0,
            "ui_events": 0,
            "data_operations": 0,
            "errors": 0,
            "warnings": 0,
            "renders_success": 0,
            "renders_failed": 0
        }
        
        # Almacenamiento de eventos críticos
        self.events_log = []
        self.errors_log = []
        self.ui_state_log = []
        self.data_processing_log = []
        
        # Configurar loggers especializados
        self._setup_specialized_loggers()
        
        # Log de inicio
        self.log_session_start()
    
    def _setup_specialized_loggers(self):
        """Configurar loggers especializados para diferentes aspectos"""
        
        # Logger principal (todo)
        self.main_logger = self._create_logger("main", "blackbox_main.log", logging.DEBUG)
        
        # Logger de UI (interfaz y pestañas)
        self.ui_logger = self._create_logger("ui", "blackbox_ui.log", logging.DEBUG)
        
        # Logger de datos (procesamiento de velas, CSV, etc.)
        self.data_logger = self._create_logger("data", "blackbox_data.log", logging.DEBUG)
        
        # Logger de renders (métodos render_*)
        self.render_logger = self._create_logger("render", "blackbox_render.log", logging.DEBUG)
        
        # Logger de errores críticos
        self.error_logger = self._create_logger("error", "blackbox_errors.log", logging.ERROR)
        
        # Logger de performance
        self.perf_logger = self._create_logger("perf", "blackbox_performance.log", logging.INFO)
        
        # Logger de funciones (tracking de llamadas)
        self.func_logger = self._create_logger("func", "blackbox_functions.log", logging.DEBUG)
    
    def _create_logger(self, name: str, filename: str, level: int) -> logging.Logger:
        """Crear logger individual con configuración específica"""
        logger_name = f"{self.session_name}_{name}"
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        
        # Evitar duplicar handlers
        if logger.handlers:
            return logger
        
        # Handler para archivo
        log_file = self.base_log_dir / filename
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        
        # Formato ultra detallado con microsegundos
        formatter = logging.Formatter(
            '[%(asctime)s.%(msecs)03d] [%(name)s] [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def log_session_start(self):
        """Log del inicio de sesión con información del sistema"""
        session_info = {
            "session_id": self.session_id,
            "start_time": datetime.now().isoformat(),
            "purpose": "Diagnosticar problemas de pestañas y contenido en ICT Dashboard",
            "log_directory": str(self.base_log_dir),
            "expected_issues": [
                "Pestañas no muestran contenido",
                "Errores en métodos render_*",
                "Problemas con datos de velas",
                "Fallos en carga de archivos CSV"
            ]
        }
        
        self.main_logger.info(f"BLACKBOX_SESSION_START | {json.dumps(session_info, indent=2)}")
        print(f"🔴 BlackBox Logger iniciado: {self.session_id}")
        print(f"📁 Logs en: {self.base_log_dir}")
    
    def track_function_call(self, func_name: str, args: Any = None, kwargs: Any = None, 
                           execution_time: float = None, result: Any = None, error: Exception = None):
        """Trackear llamada a función con todos los detalles posibles"""
        
        # Obtener información del caller
        frame = None
        caller_info = "Unknown"
        try:
            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                caller_info = f"{caller_frame.f_code.co_filename}:{caller_frame.f_lineno}"
        except:
            pass
        
        self.counters["function_calls"] += 1
        
        call_data = {
            "timestamp": datetime.now().isoformat(),
            "session_time": time.time() - self.start_time,
            "function": func_name,
            "caller": caller_info,
            "args_type": type(args).__name__ if args is not None else None,
            "args_str": str(args)[:200] if args is not None else None,
            "kwargs_type": type(kwargs).__name__ if kwargs is not None else None,
            "kwargs_str": str(kwargs)[:200] if kwargs is not None else None,
            "execution_time": execution_time,
            "result_type": type(result).__name__ if result is not None else None,
            "result_size": len(result) if hasattr(result, '__len__') else None,
            "error": str(error) if error else None,
            "call_count": self.counters["function_calls"]
        }
        
        self.events_log.append(call_data)
        
        if error:
            self.counters["errors"] += 1
            self.func_logger.error(f"FUNC_ERROR | {func_name} | {error} | Caller: {caller_info}")
            self.log_critical_error(error, f"Function: {func_name}")
        else:
            self.func_logger.debug(f"FUNC_CALL | {func_name} | Args: {type(args).__name__} | Result: {type(result).__name__} | Time: {execution_time}")
    
    def track_render_method(self, method_name: str, content_preview: str = None, 
                          success: bool = True, error_msg: str = None, 
                          content_length: int = None):
        """Trackear específicamente métodos render_* del dashboard"""
        
        if success:
            self.counters["renders_success"] += 1
            log_level = "info"
            status = "SUCCESS"
        else:
            self.counters["renders_failed"] += 1
            log_level = "error"
            status = "FAILED"
        
        render_data = {
            "timestamp": datetime.now().isoformat(),
            "method": method_name,
            "status": status,
            "content_length": content_length,
            "content_preview": content_preview[:300] if content_preview else None,
            "error_message": error_msg,
            "success_rate": self.counters["renders_success"] / (self.counters["renders_success"] + self.counters["renders_failed"]) * 100
        }
        
        if success:
            self.render_logger.info(f"RENDER_SUCCESS | {method_name} | Length: {content_length} | Preview: {content_preview[:100] if content_preview else 'None'}")
        else:
            self.render_logger.error(f"RENDER_FAILED | {method_name} | Error: {error_msg}")
        
        self.events_log.append(render_data)
    
    def track_ui_component(self, component_name: str, action: str, state: Dict[str, Any] = None,
                          success: bool = True, error_msg: str = None):
        """Trackear componentes de UI (pestañas, botones, displays)"""
        
        self.counters["ui_events"] += 1
        
        ui_data = {
            "timestamp": datetime.now().isoformat(),
            "component": component_name,
            "action": action,
            "state": state,
            "success": success,
            "error": error_msg,
            "event_number": self.counters["ui_events"]
        }
        
        self.ui_state_log.append(ui_data)
        
        if success:
            self.ui_logger.info(f"UI_SUCCESS | {component_name} | {action} | State: {state}")
        else:
            self.ui_logger.error(f"UI_FAILED | {component_name} | {action} | Error: {error_msg}")
    
    def track_data_processing(self, operation: str, input_data: Any, output_data: Any,
                            processing_time: float = None, metadata: Dict[str, Any] = None):
        """Trackear procesamiento de datos (CSV, velas, análisis)"""
        
        self.counters["data_operations"] += 1
        
        data_info = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "input_type": type(input_data).__name__,
            "input_size": len(input_data) if hasattr(input_data, '__len__') else None,
            "output_type": type(output_data).__name__,
            "output_size": len(output_data) if hasattr(output_data, '__len__') else None,
            "processing_time": processing_time,
            "metadata": metadata,
            "operation_number": self.counters["data_operations"]
        }
        
        self.data_processing_log.append(data_info)
        
        self.data_logger.info(
            f"DATA_OP | {operation} | "
            f"Input: {data_info['input_type']}({data_info['input_size']}) | "
            f"Output: {data_info['output_type']}({data_info['output_size']}) | "
            f"Time: {processing_time}s"
        )
    
    def track_candle_data(self, symbol: str, timeframe: str, candle_count: int, 
                         data_quality: str, file_path: str = None, errors: List[str] = None):
        """Trackear específicamente datos de velas"""
        
        candle_info = {
            "timestamp": datetime.now().isoformat(),
            "symbol": symbol,
            "timeframe": timeframe,
            "candle_count": candle_count,
            "data_quality": data_quality,
            "file_path": file_path,
            "errors": errors
        }
        
        self.data_logger.info(f"CANDLE_DATA | {symbol} | {timeframe} | Count: {candle_count} | Quality: {data_quality}")
        
        if errors:
            for error in errors:
                self.data_logger.warning(f"CANDLE_WARNING | {symbol} | {error}")
    
    def log_critical_error(self, error: Exception, context: str = "Unknown"):
        """Log de error crítico con stack trace completo"""
        
        self.counters["errors"] += 1
        
        # Obtener variables locales del frame que llamó
        local_vars = {}
        try:
            frame = inspect.currentframe()
            if frame and frame.f_back:
                local_vars = {k: str(v)[:100] for k, v in frame.f_back.f_locals.items()}
        except:
            pass
        
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "stack_trace": traceback.format_exc(),
            "local_variables": local_vars,
            "error_number": self.counters["errors"]
        }
        
        self.errors_log.append(error_data)
        
        self.error_logger.critical(f"CRITICAL_ERROR | {context} | {type(error).__name__}: {error}")
        self.error_logger.critical(f"STACK_TRACE | {traceback.format_exc()}")
        
        # También log en main logger
        self.main_logger.critical(f"CRITICAL | {context} | {error}")
    
    def log_tab_content_attempt(self, tab_name: str, method_name: str, success: bool,
                               content_length: int = None, error_details: str = None):
        """Log específico para intentos de mostrar contenido en pestañas"""
        
        tab_data = {
            "timestamp": datetime.now().isoformat(),
            "tab_name": tab_name,
            "render_method": method_name,
            "success": success,
            "content_length": content_length,
            "error_details": error_details
        }
        
        if success:
            self.ui_logger.info(f"TAB_CONTENT_SUCCESS | {tab_name} | {method_name} | Length: {content_length}")
        else:
            self.ui_logger.error(f"TAB_CONTENT_FAILED | {tab_name} | {method_name} | Error: {error_details}")
        
        self.ui_state_log.append(tab_data)
    
    def generate_comprehensive_report(self):
        """Generar reporte comprehensivo de toda la sesión"""
        
        session_duration = time.time() - self.start_time
        
        report = {
            "session_info": {
                "session_id": self.session_id,
                "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration_seconds": session_duration,
                "purpose": "Diagnosticar problemas de pestañas en ICT Dashboard"
            },
            "summary_counters": self.counters.copy(),
            "success_rates": {
                "render_success_rate": (self.counters["renders_success"] / 
                                      max(1, self.counters["renders_success"] + self.counters["renders_failed"])) * 100,
                "error_rate": (self.counters["errors"] / max(1, self.counters["function_calls"])) * 100
            },
            "recent_events": self.events_log[-20:],  # Últimos 20 eventos
            "critical_errors": self.errors_log,
            "ui_events": self.ui_state_log[-15:],  # Últimos 15 eventos UI
            "data_operations": self.data_processing_log[-10:],  # Últimas 10 operaciones de datos
            "log_files": {
                "main": str(self.base_log_dir / "blackbox_main.log"),
                "ui": str(self.base_log_dir / "blackbox_ui.log"),
                "data": str(self.base_log_dir / "blackbox_data.log"),
                "render": str(self.base_log_dir / "blackbox_render.log"),
                "errors": str(self.base_log_dir / "blackbox_errors.log"),
                "performance": str(self.base_log_dir / "blackbox_performance.log"),
                "functions": str(self.base_log_dir / "blackbox_functions.log")
            },
            "recommendations": self._generate_recommendations()
        }
        
        # Guardar reporte principal
        report_file = self.base_log_dir / "COMPREHENSIVE_DEBUG_REPORT.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Generar reporte de texto legible
        self._generate_text_report(report)
        
        self.main_logger.info(f"COMPREHENSIVE_REPORT_GENERATED | {report_file}")
        print(f"📊 Reporte comprehensivo generado: {report_file}")
        
        return report_file
    
    def _generate_recommendations(self) -> List[str]:
        """Generar recomendaciones basadas en los logs"""
        recommendations = []
        
        if self.counters["renders_failed"] > 0:
            recommendations.append(
                f"❌ {self.counters['renders_failed']} métodos render fallaron. "
                "Revisar logs de render para errores específicos."
            )
        
        if self.counters["errors"] > 5:
            recommendations.append(
                f"⚠️ {self.counters['errors']} errores detectados. "
                "Sistema inestable, revisar errores críticos."
            )
        
        if self.counters["data_operations"] == 0:
            recommendations.append(
                "📊 No se detectaron operaciones de datos. "
                "Posible problema en carga de archivos CSV."
            )
        
        error_rate = (self.counters["errors"] / max(1, self.counters["function_calls"])) * 100
        if error_rate > 10:
            recommendations.append(
                f"🚨 Tasa de errores alta: {error_rate:.1f}%. "
                "Revisar robustez del código."
            )
        
        if len(recommendations) == 0:
            recommendations.append("✅ No se detectaron problemas críticos en esta sesión.")
        
        return recommendations
    
    def _generate_text_report(self, report_data: Dict[str, Any]):
        """Generar reporte de texto legible"""
        
        text_report = f"""
🔴 ICT DASHBOARD BLACKBOX REPORT
================================

Session ID: {report_data['session_info']['session_id']}
Duration: {report_data['session_info']['duration_seconds']:.2f} seconds
Purpose: {report_data['session_info']['purpose']}

📊 SUMMARY COUNTERS:
- Function calls: {report_data['summary_counters']['function_calls']}
- UI events: {report_data['summary_counters']['ui_events']}
- Data operations: {report_data['summary_counters']['data_operations']}
- Successful renders: {report_data['summary_counters']['renders_success']}
- Failed renders: {report_data['summary_counters']['renders_failed']}
- Errors: {report_data['summary_counters']['errors']}
- Warnings: {report_data['summary_counters']['warnings']}

📈 SUCCESS RATES:
- Render success rate: {report_data['success_rates']['render_success_rate']:.1f}%
- Error rate: {report_data['success_rates']['error_rate']:.1f}%

🚨 CRITICAL ERRORS: {len(report_data['critical_errors'])}
"""
        
        for i, error in enumerate(report_data['critical_errors'][:5]):  # Top 5 errores
            text_report += f"\n{i+1}. {error['context']}: {error['error_message']}\n"
        
        text_report += f"\n💡 RECOMMENDATIONS:\n"
        for rec in report_data['recommendations']:
            text_report += f"- {rec}\n"
        
        text_report += f"\n📁 LOG FILES:\n"
        for log_type, log_path in report_data['log_files'].items():
            text_report += f"- {log_type.upper()}: {log_path}\n"
        
        # Guardar reporte de texto
        text_file = self.base_log_dir / "DEBUG_REPORT_READABLE.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text_report)
        
        print(f"📄 Reporte legible generado: {text_file}")

# Instancia global del BlackBox Logger
ict_blackbox = ICTDashboardBlackBox()

# Funciones de conveniencia para usar desde el dashboard
def bb_track_function(func_name: str, args=None, kwargs=None, execution_time=None, result=None, error=None):
    """Función de conveniencia para trackear llamadas a función"""
    ict_blackbox.track_function_call(func_name, args, kwargs, execution_time, result, error)

def bb_track_render(method_name: str, content_preview=None, success=True, error_msg=None, content_length=None):
    """Función de conveniencia para trackear renders"""
    ict_blackbox.track_render_method(method_name, content_preview, success, error_msg, content_length)

def bb_track_ui(component: str, action: str, state=None, success=True, error_msg=None):
    """Función de conveniencia para trackear UI"""
    ict_blackbox.track_ui_component(component, action, state, success, error_msg)

def bb_track_data(operation: str, input_data, output_data, processing_time=None, metadata=None):
    """Función de conveniencia para trackear datos"""
    ict_blackbox.track_data_processing(operation, input_data, output_data, processing_time, metadata)

def bb_track_error(error: Exception, context: str = "Unknown"):
    """Función de conveniencia para trackear errores críticos"""
    ict_blackbox.log_critical_error(error, context)

def bb_track_tab(tab_name: str, method_name: str, success: bool, content_length=None, error_details=None):
    """Función de conveniencia para trackear contenido de pestañas"""
    ict_blackbox.log_tab_content_attempt(tab_name, method_name, success, content_length, error_details)

def bb_generate_report():
    """Función de conveniencia para generar reporte"""
    return ict_blackbox.generate_comprehensive_report()

if __name__ == "__main__":
    # Test del sistema
    print("🔴 Testing ICT Dashboard BlackBox Logger...")
    
    # Simular algunos eventos
    bb_track_function("test_function", args=("test",), result="success")
    bb_track_render("render_overview", "Test content", True, content_length=100)
    bb_track_ui("tab_overview", "display_content", {"visible": True}, True)
    bb_track_data("load_csv", ["file1.csv"], {"loaded": 1}, 0.5)
    
    # Simular un error
    try:
        raise ValueError("Test error for BlackBox")
    except Exception as e:
        bb_track_error(e, "Test context")
    
    # Generar reporte
    report_file = bb_generate_report()
    print(f"✅ Test completado. Reporte en: {report_file}")
