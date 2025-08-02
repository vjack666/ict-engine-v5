# 🗑️ REPORTE: ARCHIVOS POSIBLEMENTE NO UTILIZADOS

**Fecha:** 02 de August de 2025
**Propósito:** Identificar archivos candidatos para limpieza
**Estado:** ⚠️ REVISAR ANTES DE BORRAR

---

## 📊 **RESUMEN**

**Total archivos identificados:** 124
**Categorías encontradas:** 6

## 🗂️ Archivos de Backup

**Archivos encontrados:** 7

**Recomendación:** REVISAR - Verificar que los originales funcionen antes de borrar

```
core\analysis_command_center\acc_data_models.py.bak
core\analysis_command_center\acc_flow_controller.py.bak
core\analysis_command_center\acc_orchestrator.py.bak
core\trading.py.bak
scripts\master_sluc_v21_updater.py.bak
sistema\logging_interface_v20_backup.py
sistema\logging_interface_v20_backup.py.bak
```

## 🔧 Scripts de Fix (Ya ejecutados)

**Archivos encontrados:** 14

**Recomendación:** REVISAR - Mantener solo si pueden reutilizarse

```
debugging\fix_logging_emoji_errors.py
debugging\tct_instant_fix.py
debugging\tct_live_hotfix.py
debugging\tct_quick_fix.py
docs\bitacoras\sistemas\poi_system_fix_completed.md
docs\bitacoras\sistemas\sluc_system_names_fix_completed.md
scripts\fix_acc_flow_controller.py
scripts\fix_escaped_quotes.py
scripts\fix_jsondecode_critical.py
scripts\fix_jsondecode_error.py
scripts\fix_log_encoding.py
scripts\fix_tct_logging_params.py
scripts\fix_tct_pipeline_logging.py
scripts\quick_fixes.py
```

## 🧪 Archivos de Testing

**Archivos encontrados:** 22

**Recomendación:** REVISAR - Mantener tests importantes

```
debugging\test_poi_integration.py
debugging\test_tct_render.py
docs\bitacoras\diagnosticos\tct_debugging_weekend_testing_completed.md
docs\bitacoras\reportes\REPORTE_POI_TEST_SUITE_20250801_153152.md
docs\bitacoras\reportes\REPORTE_POI_TEST_SUITE_20250801_153900.md
docs\bitacoras\reportes\REPORTE_TEST_SUITE_COMPLETO.md
tests\integration\test_poi_dashboard_integration.py
tests\poi_system\poi_test_simple.py
tests\poi_system\poi_test_suite.py
tests\test_caja_negra.py
tests\test_correcciones.py
tests\test_ictdetector_sprint12.py
tests\test_imports.py
tests\test_poi_panel.py
tests\test_tct_pipeline_complete.py
tests\unit\test_dashboard_specific.py
tests\unit\test_dashboard_widgets.py
tests\unit\test_ict_engine.py
tests\unit\test_imports.py
tests\unit\test_logging_system.py
tests\unit\test_trading_engine.py
utilities\debug\test_imports.py
```

## 🔄 Posibles Duplicados

**Archivos encontrados:** 2

**Recomendación:** REVISAR - Comparar contenido antes de borrar

```
core\ict_engine\veredicto_engine_v4.py
sistema\logging_interface_v21.py
```

## 📁 Archivos Temporales

**Archivos encontrados:** 60

**Recomendación:** BORRAR - Seguros para eliminar

```
__pycache__\clean_poi_diagnostics.cpython-313.pyc
__pycache__\poi_black_box_diagnostics.cpython-313.pyc
config\__pycache__\__init__.cpython-313.pyc
config\__pycache__\config_manager.cpython-313.pyc
core\__pycache__\__init__.cpython-313.pyc
core\__pycache__\limit_order_manager.cpython-313.pyc
core\__pycache__\smart_trading_logger.cpython-313.pyc
core\__pycache__\trading.cpython-313.pyc
core\analysis_command_center\__pycache__\__init__.cpython-313.pyc
core\analysis_command_center\__pycache__\acc_data_models.cpython-313.pyc
core\analysis_command_center\__pycache__\acc_flow_controller.cpython-313.pyc
core\analysis_command_center\__pycache__\acc_orchestrator.cpython-313.pyc
core\analysis_command_center\tct_pipeline\__pycache__\__init__.cpython-313.pyc
core\analysis_command_center\tct_pipeline\__pycache__\tct_aggregator.cpython-313.pyc
core\analysis_command_center\tct_pipeline\__pycache__\tct_formatter.cpython-313.pyc
core\analysis_command_center\tct_pipeline\__pycache__\tct_interface.cpython-313.pyc
core\analysis_command_center\tct_pipeline\__pycache__\tct_measurements.cpython-313.pyc
core\ict_engine\__pycache__\__init__.cpython-313.pyc
core\ict_engine\__pycache__\confidence_engine.cpython-313.pyc
core\ict_engine\__pycache__\ict_detector.cpython-313.pyc
core\ict_engine\__pycache__\ict_historical_analyzer.cpython-313.pyc
core\ict_engine\__pycache__\ict_types.cpython-313.pyc
core\ict_engine\__pycache__\pattern_analyzer.cpython-313.pyc
core\ict_engine\__pycache__\veredicto_engine_v4.cpython-313.pyc
core\poi_system\__pycache__\__init__.cpython-313.pyc
core\poi_system\__pycache__\poi_black_box_diagnostics.cpython-313.pyc
core\poi_system\__pycache__\poi_detector.cpython-313.pyc
core\poi_system\__pycache__\poi_scoring_engine.cpython-313.pyc
core\poi_system\__pycache__\poi_utils.cpython-313.pyc
core\risk_management\__pycache__\__init__.cpython-313.pyc
core\risk_management\__pycache__\riskbot_mt5.cpython-313.pyc
dashboard\__pycache__\__init__.cpython-313.pyc
dashboard\__pycache__\dashboard_controller.cpython-313.pyc
dashboard\__pycache__\dashboard_definitivo.cpython-313.pyc
dashboard\__pycache__\dashboard_widgets.cpython-313.pyc
dashboard\__pycache__\ict_professional_widget.cpython-313.pyc
dashboard\__pycache__\poi_dashboard_integration.cpython-313.pyc
docs\bitacoras\__pycache__\bitacora_manager.cpython-313.pyc
scripts\__pycache__\__init__.cpython-313.pyc
scripts\__pycache__\clean_poi_diagnostics.cpython-313.pyc
sistema\__pycache__\__init__.cpython-313.pyc
sistema\__pycache__\config.cpython-313.pyc
sistema\__pycache__\data_logger.cpython-313.pyc
sistema\__pycache__\emoji_logger.cpython-313.pyc
sistema\__pycache__\logging_config.cpython-313.pyc
sistema\__pycache__\logging_interface.cpython-313.pyc
sistema\__pycache__\smart_directory_logger.cpython-313.pyc
tests\__pycache__\__init__.cpython-313.pyc
tests\unit\__pycache__\__init__.cpython-313.pyc
tests\unit\__pycache__\test_config_manager.cpython-313-pytest-8.3.5.pyc
tests\unit\__pycache__\test_dashboard_specific.cpython-313-pytest-8.3.5.pyc
tests\unit\__pycache__\test_dashboard_widgets.cpython-313-pytest-8.3.5.pyc
tests\unit\__pycache__\test_ict_engine.cpython-313-pytest-8.3.5.pyc
tests\unit\__pycache__\test_imports.cpython-313-pytest-8.3.5.pyc
tests\unit\__pycache__\test_logging_system.cpython-313-pytest-8.3.5.pyc
tests\unit\__pycache__\test_trading_engine.cpython-313-pytest-8.3.5.pyc
utilities\migration\__pycache__\print_migration_tool.cpython-313.pyc
utils\__pycache__\__init__.cpython-313.pyc
utils\__pycache__\logging_utils.cpython-313.pyc
utils\__pycache__\mt5_data_manager.cpython-313.pyc
```

## 📋 Archivos de Log

**Archivos encontrados:** 19

**Recomendación:** REVISAR - Mantener logs recientes importantes

```
data\logs\daily\sentinel_runtime.log
data\logs\dashboard\dashboard_20250802.log
data\logs\dashboard\data_packets.log
data\logs\debug\debug_20250802.log
data\logs\debug\full_system_trace.log
data\logs\errors\error.log
data\logs\errors\errors_20250802.log
data\logs\ict\ict_20250802.log
data\logs\ict\ict_analysis.log
data\logs\mt5\mt5_20250802.log
data\logs\mt5\mt5_operations.log
data\logs\poi\poi_20250802.log
data\logs\poi\poi_detection.log
data\logs\structured\events.jsonl
data\logs\structured\sentinel_events.jsonl
data\logs\tct\tct_20250802.log
data\logs\trading\trading_20250802.log
data\logs\trading\trading_decisions.log
docs\bitacoras\sistemas\system_status_2025-08-01.jsonl
```

---

## ⚠️ **ADVERTENCIAS IMPORTANTES**

### 🚫 **NO BORRAR SIN VERIFICAR:**
- Archivos de configuración críticos
- Scripts que pueden ser reutilizados
- Documentación de referencia
- Logs recientes importantes

### ✅ **SEGUROS PARA BORRAR:**
- Archivos .pyc y __pycache__
- Logs antiguos (>7 días)
- Archivos .bak confirmados
- Scripts de fix ya ejecutados exitosamente

## 🎯 **PRÓXIMOS PASOS RECOMENDADOS**

1. **Revisar cada categoría** individualmente
2. **Verificar dependencias** antes de borrar
3. **Crear backup** de archivos dudosos
4. **Borrar por fases** empezando por lo más seguro
5. **Validar sistema** después de cada limpieza

---

**Generado por:** UnusedFilesAnalyzer v1.0
**ICT Engine v5.0** - Análisis de Limpieza