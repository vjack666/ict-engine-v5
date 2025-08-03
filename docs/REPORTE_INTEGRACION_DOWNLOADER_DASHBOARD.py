#!/usr/bin/env python3
"""
📊 REPORTE DE INTEGRACIÓN: ADVANCED CANDLE DOWNLOADER ↔ DASHBOARD
===============================================================================

OBJETIVO: Conectar el Advanced Candle Downloader con el dashboard para
automatizar la descarga y actualización de datos que alimenten a todos
los sistemas (POI, ICT, Fractal, etc.)

ANÁLISIS DEL FLUJO ACTUAL:
=========================

1. 🚀 PUNTO DE ENTRADA - main.py → dashboard_definitivo.py
   - El usuario ejecuta: python main.py --dashboard
   - Se lanza dashboard_definitivo.py como interfaz principal
   - El dashboard se conecta a MT5 usando get_mt5_manager()

2. 📊 FLUJO DE DATOS ACTUAL (dashboard_definitivo.py):
   Línea 447: self.mt5_manager = get_mt5_manager()
   Línea 1086: data = self.mt5_manager.get_historical_data(symbol, tf_code, bars)

   LIMITACIÓN DETECTADA:
   - Solo descarga cantidades pequeñas (200-300 velas)
   - No hay persistencia a largo plazo de datos
   - Cada arranque requiere re-descarga

3. 🎯 SISTEMAS QUE CONSUMEN DATOS:
   a) ICT Engine (core/ict_engine/):
      - ict_detector.py - Análisis de patrones ICT
      - fractal_analyzer.py - Análisis de fractales
      - confidence_engine.py - Motor de confianza

   b) POI System (core/poi_system/):
      - poi_detector.py - Detección de POIs
      - poi_scoring_engine.py - Scoring de POIs

   c) Trading Engine (core/trading.py):
      - Análisis de trade execution

PROPUESTA DE INTEGRACIÓN:
========================

FASE 1: MODIFICACIÓN DEL DASHBOARD (dashboard_definitivo.py)
----------------------------------------------------------

A. AGREGAR ADVANCED CANDLE DOWNLOADER AL INICIO

   Línea ~77 (imports):
   + from utils.advanced_candle_downloader import AdvancedCandleDownloader

   Línea ~315 (inicialización):
   + self.candle_downloader = AdvancedCandleDownloader()

B. NUEVA FUNCIÓN: auto_download_data_on_startup()

   def auto_download_data_on_startup(self):
       \"\"\"Descarga automática de datos al iniciar el dashboard\"\"\"
       try:
           # Verificar si necesitamos datos frescos
           if self._needs_data_refresh():
               enviar_senal_log("INFO", "🔄 Descarga automática iniciada", __name__, "downloader")

               # Descarga optimizada para el dashboard
               stats = self.candle_downloader.download_multiple(
                   symbols=["EURUSD"],  # Symbol principal
                   timeframes=["M1", "M5", "H1", "H4"],  # TFs críticos
                   lookback=100000,  # 100K velas (suficiente para análisis)
                   use_parallel=True
               )

               enviar_senal_log("INFO", f"✅ Descarga completada: {len(stats)} timeframes", __name__, "downloader")
               return True
       except Exception as e:
           enviar_senal_log("ERROR", f"❌ Error en descarga automática: {e}", __name__, "downloader")
           return False

C. FUNCIÓN DE VERIFICACIÓN: _needs_data_refresh()

   def _needs_data_refresh(self) -> bool:
       \"\"\"Verifica si necesitamos refrescar los datos\"\"\"
       try:
           # Verificar archivos existentes
           data_dir = Path("data/candles")
           if not data_dir.exists():
               return True

           # Verificar timestamps de archivos críticos
           critical_files = ["M1.csv", "H1.csv", "H4.csv"]
           for file in critical_files:
               file_path = data_dir / file
               if not file_path.exists():
                   return True

               # Verificar si el archivo es muy viejo (>24 horas)
               file_age = time.time() - file_path.stat().st_mtime
               if file_age > 86400:  # 24 horas
                   return True

           return False
       except Exception:
           return True  # Si hay error, mejor descargar

D. MODIFICAR load_multi_timeframe_data() (línea ~1060)

   def load_multi_timeframe_data(self):
       \"\"\"Carga datos optimizada usando archivos pre-descargados\"\"\"
       try:
           # 🔄 NUEVO: Primero intentar cargar desde archivos CSV
           if self._load_from_csv_files():
               enviar_senal_log("INFO", "📂 Datos cargados desde archivos CSV", __name__, "data")
               return

           # 🔄 FALLBACK: Si no hay archivos, usar MT5 directo (método actual)
           if not self.mt5_manager:
               enviar_senal_log("WARNING", "🔴 MT5 Manager no disponible", __name__, "data")
               return

           # Código actual de carga desde MT5...
           [mantener código existente como fallback]

FASE 2: INTEGRACIÓN CON SISTEMAS CONSUMIDORES
---------------------------------------------

A. ICT ENGINE (core/ict_engine/ict_detector.py)

   Modificar para usar datos pre-descargados:

   def load_market_data(self, symbol: str, timeframe: str) -> pd.DataFrame:
       \"\"\"Carga datos desde archivos pre-descargados\"\"\"
       try:
           data_file = Path(f"data/candles/{timeframe}.csv")
           if data_file.exists():
               df = pd.read_csv(data_file)
               df['time'] = pd.to_datetime(df['time'])
               return df.tail(1000)  # Últimas 1000 velas para análisis
           else:
               # Fallback a MT5 directo
               return self._load_from_mt5(symbol, timeframe)
       except Exception as e:
           enviar_senal_log("ERROR", f"Error cargando datos: {e}", __name__, "ict")
           return pd.DataFrame()

B. FRACTAL ANALYZER (core/ict_engine/fractal_analyzer.py)

   Similar integración para usar archivos pre-descargados.

C. POI SYSTEM (core/poi_system/poi_detector.py)

   Usar el mismo patrón de carga desde archivos CSV.

FASE 3: SISTEMA DE ACTUALIZACIÓN AUTOMÁTICA
-------------------------------------------

A. AGREGAR BINDING AL DASHBOARD (línea ~350)

   Binding("ctrl+u", "update_data", "Actualizar Datos"),

B. FUNCIÓN DE ACTUALIZACIÓN MANUAL:

   def action_update_data(self):
       \"\"\"Actualización manual de datos vía hotkey\"\"\"
       self.notify("🔄 Iniciando actualización de datos...")

       # Ejecutar descarga en background
       import threading
       thread = threading.Thread(target=self._background_data_update)
       thread.daemon = True
       thread.start()

   def _background_data_update(self):
       \"\"\"Actualización de datos en background\"\"\"
       try:
           stats = self.candle_downloader.download_multiple(
               symbols=["EURUSD"],
               timeframes=["M1", "M5", "H1", "H4"],
               lookback=50000,  # Actualización más rápida
               use_parallel=True
           )

           # Notificar al usuario
           self.call_from_thread(self.notify, f"✅ Datos actualizados: {len(stats)} timeframes")

           # Recargar datos en dashboard
           self.call_from_thread(self._reload_dashboard_data)

       except Exception as e:
           self.call_from_thread(self.notify, f"❌ Error actualizando: {e}")

FASE 4: CONFIGURACIÓN Y OPTIMIZACIÓN
------------------------------------

A. ARCHIVO DE CONFIGURACIÓN (config/data_config.py):

   DATA_UPDATE_CONFIG = {
       "auto_download_on_startup": True,
       "symbols": ["EURUSD"],
       "timeframes": ["M1", "M5", "H1", "H4"],
       "lookback_startup": 100000,
       "lookback_update": 50000,
       "max_file_age_hours": 24,
       "parallel_downloads": True,
       "verify_integrity": True,
       "backup_old_data": True
   }

B. SISTEMA DE LOGS DEDICADO:

   Usar smart_directory_logger.py para logs específicos de descarga:
   - data/logs/mt5/ para logs de conexión MT5
   - data/logs/daily/ para logs de descarga diaria

IMPLEMENTACIÓN PASO A PASO:
===========================

PASO 1: Modificar dashboard_definitivo.py
- Agregar imports
- Agregar inicialización del downloader
- Implementar auto_download_data_on_startup()
- Modificar load_multi_timeframe_data()

PASO 2: Crear funciones auxiliares
- _needs_data_refresh()
- _load_from_csv_files()
- _background_data_update()

PASO 3: Integrar sistemas consumidores
- Modificar ICT Engine para usar CSV
- Modificar POI System para usar CSV
- Modificar Fractal Analyzer para usar CSV

PASO 4: Testing y validación
- Test de flujo completo
- Verificar rendimiento
- Validar integridad de datos

BENEFICIOS ESPERADOS:
====================

1. 🚀 ARRANQUE MÁS RÁPIDO: Dashboard carga desde archivos pre-descargados
2. 📊 DATOS CONSISTENTES: Todos los sistemas usan la misma fuente
3. 🔄 ACTUALIZACIÓN AUTOMÁTICA: Datos frescos sin intervención manual
4. 💾 PERSISTENCIA: Datos guardados para análisis offline
5. ⚡ MEJOR RENDIMIENTO: Menos llamadas a MT5 en tiempo real
6. 🛡️ MAYOR ROBUSTEZ: Fallbacks en caso de problemas MT5

CRONOGRAMA ESTIMADO:
===================

- Fase 1: 2-3 horas (modificación dashboard)
- Fase 2: 2-3 horas (integración sistemas)
- Fase 3: 1-2 horas (sistema actualización)
- Fase 4: 1 hora (configuración)
- Testing: 1-2 horas

TOTAL: 7-11 horas de desarrollo

RIESGOS Y MITIGACIONES:
======================

RIESGO: Conflictos con código existente
MITIGACIÓN: Implementar como funcionalidad adicional, mantener fallbacks

RIESGO: Problemas de rendimiento
MITIGACIÓN: Carga paralela, datos en chunks, validación de memoria

RIESGO: Datos corruptos
MITIGACIÓN: Validación con pandas/numpy, backups automáticos

PRÓXIMOS PASOS:
===============

1. ✅ Preparar este reporte (COMPLETADO)
2. 🔄 Implementar Fase 1 (modificar dashboard)
3. 🔄 Testing inicial
4. 🔄 Implementar Fases 2-4
5. 🔄 Testing completo y validación

¿PROCEDER CON LA IMPLEMENTACIÓN?
"""

print(__doc__)
