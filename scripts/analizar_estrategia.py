#!/usr/bin/env python3
"""
🔍 ICT ENGINE v5.0 - ANÁLISIS DE ESTRATEGIA
===========================================

Script para analizar la ejecución de la estrategia ICT y detectar errores,
cuellos de botella y oportunidades de mejora.

Uso:
    python analizar_estrategia.py
    python analizar_estrategia.py --test-mode
    python analizar_estrategia.py --detailed
"""

from sistema.sic import sys
from sistema.sic import Path
import traceback
from sistema.sic import datetime
from sistema.sic import Dict, List, Any

# 📁 Configurar paths del proyecto
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from sistema.sic import enviar_senal_log

def test_importaciones_estrategia():
    """Prueba las importaciones de los componentes de la estrategia"""
    enviar_senal_log("🔍 FASE 1: Verificando importaciones de componentes ICT...", "DEBUG")

    resultados = {
        "imports_exitosos": [],
        "imports_fallidos": [],
        "componentes_disponibles": {}
    }

    # Test 1: ICT Engine principal
    try:
        from core.ict_engine.ict_engine import ICTEngine
        resultados["imports_exitosos"].append("✅ ICTEngine")
        resultados["componentes_disponibles"]["ict_engine"] = True
    except Exception as e:
        resultados["imports_fallidos"].append(f"❌ ICTEngine: {e}")
        resultados["componentes_disponibles"]["ict_engine"] = False

    # Test 2: ICT Detector
    try:
        from sistema.sic import ICTDetector
        resultados["imports_exitosos"].append("✅ ICTDetector")
        resultados["componentes_disponibles"]["ict_detector"] = True
    except Exception as e:
        resultados["imports_fallidos"].append(f"❌ ICTDetector: {e}")
        resultados["componentes_disponibles"]["ict_detector"] = False

    # Test 3: POI System
    try:
        from core.poi_system.poi_system import POISystem
        resultados["imports_exitosos"].append("✅ POISystem")
        resultados["componentes_disponibles"]["poi_system"] = True
    except Exception as e:
        resultados["imports_fallidos"].append(f"❌ POISystem: {e}")
        resultados["componentes_disponibles"]["poi_system"] = False

    # Test 4: Confidence Engine
    try:
        from core.ict_engine.confidence_engine import ConfidenceEngine
        resultados["imports_exitosos"].append("✅ ConfidenceEngine")
        resultados["componentes_disponibles"]["confidence_engine"] = True
    except Exception as e:
        resultados["imports_fallidos"].append(f"❌ ConfidenceEngine: {e}")
        resultados["componentes_disponibles"]["confidence_engine"] = False

    # Test 5: MT5 Data Manager
    try:
        from utils.mt5_data_manager import get_mt5_manager
        manager = get_mt5_manager()
        resultados["imports_exitosos"].append("✅ MT5DataManager")
        resultados["componentes_disponibles"]["mt5_manager"] = True
    except Exception as e:
        resultados["imports_fallidos"].append(f"❌ MT5DataManager: {e}")
        resultados["componentes_disponibles"]["mt5_manager"] = False

    return resultados

def test_inicializacion_estrategia():
    """Prueba la inicialización de los componentes de la estrategia"""
    enviar_senal_log("🔍 FASE 2: Probando inicialización de componentes...", "DEBUG")

    resultados = {
        "inicializaciones_exitosas": [],
        "inicializaciones_fallidas": [],
        "instancias_creadas": {}
    }

    # Test inicialización ICT Engine
    try:
        from core.ict_engine.ict_engine import ICTEngine
        from utils.mt5_data_manager import get_mt5_manager

        manager = get_mt5_manager()
        engine = ICTEngine(mt5_manager=manager)

        resultados["inicializaciones_exitosas"].append("✅ ICTEngine inicializado")
        resultados["instancias_creadas"]["ict_engine"] = engine
    except Exception as e:
        resultados["inicializaciones_fallidas"].append(f"❌ ICTEngine: {e}")
        resultados["instancias_creadas"]["ict_engine"] = None

    # Test inicialización POI System
    try:
        from core.poi_system.poi_system import POISystem

        poi_system = POISystem()

        resultados["inicializaciones_exitosas"].append("✅ POISystem inicializado")
        resultados["instancias_creadas"]["poi_system"] = poi_system
    except Exception as e:
        resultados["inicializaciones_fallidas"].append(f"❌ POISystem: {e}")
        resultados["instancias_creadas"]["poi_system"] = None

    return resultados

def test_carga_datos():
    """Prueba la carga de datos históricos"""
    enviar_senal_log("🔍 FASE 3: Probando carga de datos históricos...", "DEBUG")

    resultados = {
        "cargas_exitosas": [],
        "cargas_fallidas": [],
        "datos_disponibles": {}
    }

    try:
        from utils.mt5_data_manager import get_mt5_manager

        manager = get_mt5_manager()

        # Test datos básicos
        timeframes = ["M15", "H1", "H4"]
        symbols = ["EURUSD"]

        for symbol in symbols:
            for timeframe in timeframes:
                try:
                    df = manager.get_historical_data(symbol, timeframe, 500)

                    if df is not None and not df.empty:
                        resultados["cargas_exitosas"].append(f"✅ {symbol} {timeframe}: {len(df)} velas")
                        resultados["datos_disponibles"][f"{symbol}_{timeframe}"] = len(df)
                    else:
                        resultados["cargas_fallidas"].append(f"❌ {symbol} {timeframe}: Sin datos")
                        resultados["datos_disponibles"][f"{symbol}_{timeframe}"] = 0

                except Exception as e:
                    resultados["cargas_fallidas"].append(f"❌ {symbol} {timeframe}: {e}")
                    resultados["datos_disponibles"][f"{symbol}_{timeframe}"] = 0

    except Exception as e:
        resultados["cargas_fallidas"].append(f"❌ Error general carga de datos: {e}")

    return resultados

def test_ejecucion_estrategia():
    """Prueba la ejecución completa de la estrategia"""
    enviar_senal_log("🔍 FASE 4: Probando ejecución completa de estrategia ICT...", "DEBUG")

    resultados = {
        "ejecuciones_exitosas": [],
        "ejecuciones_fallidas": [],
        "analisis_resultados": {}
    }

    try:
        # Importar e inicializar
        from core.ict_engine.ict_engine import ICTEngine
        from utils.mt5_data_manager import get_mt5_manager

        manager = get_mt5_manager()
        engine = ICTEngine(mt5_manager=manager)

        # Test análisis completo
        try:
            resultado = engine.analizar_mercado_completo(
                symbol="EURUSD",
                timeframe="H1",
                lookback=500
            )

            if resultado:
                resultados["ejecuciones_exitosas"].append("✅ Análisis mercado completo exitoso")
                resultados["analisis_resultados"]["mercado_completo"] = {
                    "symbol": resultado.symbol,
                    "timeframe": resultado.timeframe,
                    "confidence": resultado.confidence,
                    "patterns_count": len(resultado.patterns_detected),
                    "signals_count": len(resultado.signals)
                }
            else:
                resultados["ejecuciones_fallidas"].append("❌ Análisis mercado completo: Sin resultado")

        except Exception as e:
            resultados["ejecuciones_fallidas"].append(f"❌ Análisis mercado completo: {e}")
            enviar_senal_log("ERROR", f"Error detallado: {traceback.format_exc()}", __name__, "analisis")

    except Exception as e:
        resultados["ejecuciones_fallidas"].append(f"❌ Error general ejecución: {e}")
        enviar_senal_log("ERROR", f"Error detallado: {traceback.format_exc()}", __name__, "analisis")

    return resultados

def detectar_cuellos_botella():
    """Detecta posibles cuellos de botella en la estrategia"""
    enviar_senal_log("🔍 FASE 5: Detectando cuellos de botella...", "DEBUG")

    problemas_detectados = []

    # Verificar tamaños de archivos de datos
    try:
        data_dir = PROJECT_ROOT / "data" / "candles"
        if data_dir.exists():
            for archivo in data_dir.glob("*.csv"):
                tamano = archivo.stat().st_size
                if tamano < 1000:  # Menor a 1KB
                    problemas_detectados.append(f"🔴 Archivo de datos muy pequeño: {archivo.name}")
                elif tamano > 50_000_000:  # Mayor a 50MB
                    problemas_detectados.append(f"🟡 Archivo de datos muy grande: {archivo.name}")
        else:
            problemas_detectados.append("🔴 Directorio de datos no existe")
    except Exception as e:
        problemas_detectados.append(f"❌ Error verificando datos: {e}")

    # Verificar logs de errores recientes
    try:
        logs_dir = PROJECT_ROOT / "data" / "logs" / "errors"
        if logs_dir.exists():
            today = datetime.now().strftime("%Y%m%d")
            error_file = logs_dir / f"errors_{today}.log"

            if error_file.exists():
                with open(error_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'CRITICAL' in content:
                        problemas_detectados.append("🔴 Errores críticos detectados en logs")
                    elif 'ERROR' in content:
                        problemas_detectados.append("🟡 Errores detectados en logs")
    except Exception as e:
        problemas_detectados.append(f"❌ Error verificando logs: {e}")

    return problemas_detectados

def generar_reporte_estrategia():
    """Genera un reporte completo del análisis de la estrategia"""

    enviar_senal_log("=" * 70, "INFO")
    enviar_senal_log("🔍 ICT ENGINE v5.0 - ANÁLISIS COMPLETO DE ESTRATEGIA", "INFO")
    enviar_senal_log("=" * 70, "INFO")
    enviar_senal_log("", "INFO")

    # Ejecutar todas las fases de análisis
    try:
        imports = test_importaciones_estrategia()
        enviar_senal_log("\n📋 IMPORTACIONES:", "INFO")
        for item in imports["imports_exitosos"]:
            enviar_senal_log(f"  {item}", "INFO")
        for item in imports["imports_fallidos"]:
            enviar_senal_log(f"  {item}", "WARNING")

        inicializaciones = test_inicializacion_estrategia()
        enviar_senal_log("\n🚀 INICIALIZACIONES:", "INFO")
        for item in inicializaciones["inicializaciones_exitosas"]:
            enviar_senal_log(f"  {item}", "INFO")
        for item in inicializaciones["inicializaciones_fallidas"]:
            enviar_senal_log(f"  {item}", "WARNING")

        datos = test_carga_datos()
        enviar_senal_log("\n💾 CARGA DE DATOS:", "INFO")
        for item in datos["cargas_exitosas"]:
            enviar_senal_log(f"  {item}", "INFO")
        for item in datos["cargas_fallidas"]:
            enviar_senal_log(f"  {item}", "WARNING")

        ejecucion = test_ejecucion_estrategia()
        enviar_senal_log("\n⚡ EJECUCIÓN DE ESTRATEGIA:", "INFO")
        for item in ejecucion["ejecuciones_exitosas"]:
            enviar_senal_log(f"  {item}", "INFO")
        for item in ejecucion["ejecuciones_fallidas"]:
            enviar_senal_log(f"  {item}", "WARNING")

        if ejecucion["analisis_resultados"]:
            enviar_senal_log("\n📊 RESULTADOS DE ANÁLISIS:", "INFO")
            for key, value in ejecucion["analisis_resultados"].items():
                enviar_senal_log(f"  📈 {key}:", "INFO")
                for k, v in value.items():
                    enviar_senal_log(f"    • {k}: {v}", "INFO")

        cuellos_botella = detectar_cuellos_botella()
        enviar_senal_log("\n🚨 CUELLOS DE BOTELLA DETECTADOS:", "WARNING")
        if cuellos_botella:
            for problema in cuellos_botella:
                enviar_senal_log(f"  {problema}", "WARNING")
        else:
            enviar_senal_log("  ✅ No se detectaron cuellos de botella críticos", "INFO")

        # Evaluación general
        enviar_senal_log("\n" + "=" * 70, "INFO")
        enviar_senal_log("📊 EVALUACIÓN GENERAL:", "INFO")

        total_exitosos = (len(imports["imports_exitosos"]) +
                         len(inicializaciones["inicializaciones_exitosas"]) +
                         len(datos["cargas_exitosas"]) +
                         len(ejecucion["ejecuciones_exitosas"]))

        total_fallidos = (len(imports["imports_fallidos"]) +
                         len(inicializaciones["inicializaciones_fallidas"]) +
                         len(datos["cargas_fallidas"]) +
                         len(ejecucion["ejecuciones_fallidas"]))

        if total_fallidos == 0:
            enviar_senal_log("🎉 ESTRATEGIA FUNCIONANDO PERFECTAMENTE", "INFO")
        elif total_fallidos < 3:
            enviar_senal_log("🟡 ESTRATEGIA CON PROBLEMAS MENORES", "WARNING")
        else:
            enviar_senal_log("🔴 ESTRATEGIA CON PROBLEMAS CRÍTICOS", "ERROR")

        enviar_senal_log(f"Componentes funcionando: {total_exitosos}", "INFO")
        enviar_senal_log(f"Componentes con problemas: {total_fallidos}", "WARNING")

        enviar_senal_log("\n🔧 RECOMENDACIONES:", "INFO")
        if total_fallidos > 0:
            enviar_senal_log("1. 🔍 Revisar errores específicos mostrados arriba", "WARNING")
            enviar_senal_log("2. 🛠️ Verificar dependencias de componentes fallidos", "WARNING")
            enviar_senal_log("3. 📊 Comprobar integridad de datos históricos", "WARNING")
            enviar_senal_log("4. 🔄 Considerar reinicialización de componentes problemáticos", "WARNING")
        else:
            enviar_senal_log("✅ La estrategia está funcionando óptimamente", "INFO")
            enviar_senal_log("🚀 Lista para trading en vivo", "INFO")

    except Exception as e:
        enviar_senal_log(f"ERROR CRÍTICO en análisis: {e}", "ERROR")
        enviar_senal_log(f"Detalles: {traceback.format_exc()}", "ERROR")

    enviar_senal_log("\n" + "=" * 70, "INFO")
    enviar_senal_log(f"📅 Análisis completado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "INFO")
    enviar_senal_log("=" * 70, "INFO")

if __name__ == "__main__":
    generar_reporte_estrategia()
