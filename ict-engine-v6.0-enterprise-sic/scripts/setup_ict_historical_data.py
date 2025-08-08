#!/usr/bin/env python3
"""
🏛️ ICT HISTORICAL DATA DOWNLOADER - Descarga masiva según leyes ICT
==================================================================

Script para descargar años de datos históricos para todos los timeframes
críticos ICT. Garantiza que tengamos suficiente historia para análisis
institucional completo según las mejores prácticas ICT.

Funcionalidades:
- Descarga automática para todos los timeframes ICT
- Manejo inteligente de fechas y cantidad de velas
- Verificación de cumplimiento ICT
- Guardado organizado por símbolo y timeframe
- Reportes detallados de descarga

Autor: ICT Engine v6.1.0 Enterprise Team
Fecha: Agosto 2025
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import json

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

def setup_ict_historical_data():
    """🏛️ Configuración y descarga masiva de datos históricos ICT"""
    print("\n" + "="*80)
    print("🏛️ ICT HISTORICAL DATA DOWNLOADER v6.0 Enterprise")
    print("="*80)
    print("Descargando años de datos para análisis institucional completo...")
    
    try:
        print("\n📥 1. Inicializando Advanced Candle Downloader...")
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        
        # Configuración optimizada para descarga masiva
        downloader = AdvancedCandleDownloader(
            config={
                'enable_debug': False,  # Reducir logs para descarga masiva
                'use_predictive_cache': True,
                'enable_lazy_loading': True,
                'max_concurrent': 1,  # Evitar sobrecargar MT5
                'retry_attempts': 5,
                'retry_delay': 3.0
            }
        )
        print("✅ Downloader inicializado para descarga masiva")
        
        # Símbolos ICT principales para análisis institucional
        ict_symbols = [
            'EURUSD',  # Par principal ICT
            'GBPUSD',  # Sterling
            'USDJPY',  # Yen  
            'XAUUSD',  # Gold (muy importante para ICT)
            # 'AUDUSD',  # Aussie (opcional)
            # 'USDCAD',  # Loonie (opcional)
        ]
        
        # Timeframes ICT con configuración de fechas inteligente
        ict_timeframes_config = {
            'D1': {'years_back': 5, 'critical': True},   # 5 años para análisis macro
            'H4': {'years_back': 2, 'critical': True},   # 2 años para análisis semanal
            'H1': {'years_back': 1, 'critical': True},   # 1 año para análisis diario
            'M15': {'years_back': 0.5, 'critical': True}, # 6 meses para entrada
            'M5': {'years_back': 0.25, 'critical': False}, # 3 meses para timing
            'M1': {'years_back': 0.08, 'critical': False}, # 1 mes para scalping
        }
        
        print(f"\n📊 2. Configuración de descarga ICT:")
        print(f"   Símbolos: {', '.join(ict_symbols)}")
        print(f"   Timeframes críticos: {', '.join([tf for tf, cfg in ict_timeframes_config.items() if cfg['critical']])}")
        
        download_results = {}
        total_downloads = len(ict_symbols) * len(ict_timeframes_config)
        current_download = 0
        
        print(f"\n🚀 3. Iniciando descarga masiva ICT ({total_downloads} descargas)...")
        
        for symbol in ict_symbols:
            print(f"\n📈 Procesando {symbol}...")
            download_results[symbol] = {}
            
            for timeframe, config in ict_timeframes_config.items():
                current_download += 1
                progress = (current_download / total_downloads) * 100
                
                print(f"\n   📥 [{progress:5.1f}%] {symbol} {timeframe} ({config['years_back']} años)...")
                
                try:
                    # Calcular fechas basadas en configuración
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=config['years_back'] * 365)
                    
                    # Descarga con configuración ICT específica
                    result = downloader.download_candles(
                        symbol=symbol,
                        timeframe=timeframe,
                        start_date=start_date,
                        end_date=end_date,
                        save_to_file=True,  # Guardar todos los archivos
                        use_ict_optimal=True
                    )
                    
                    # Procesar resultado
                    if result.get('success') and result.get('data') is not None:
                        bars_downloaded = len(result['data'])
                        ict_analysis = result.get('ict_analysis', {})
                        ict_compliance = result.get('ict_compliance', {})
                        
                        # Resumen del resultado
                        status = "✅ ÓPTIMO" if ict_analysis.get('is_ict_optimal') else \
                                "✅ IDEAL" if ict_analysis.get('meets_ict_ideal') else \
                                "⚠️ MÍNIMO" if ict_analysis.get('meets_ict_minimum') else \
                                "❌ INSUFICIENTE"
                        
                        print(f"      {status} - {bars_downloaded:,} velas descargadas")
                        print(f"      Rango: {result['data'].index[0].strftime('%Y-%m-%d')} a {result['data'].index[-1].strftime('%Y-%m-%d')}")
                        print(f"      Calidad ICT: {ict_compliance.get('analysis_quality', 'N/A')}")
                        
                        download_results[symbol][timeframe] = {
                            'success': True,
                            'bars_downloaded': bars_downloaded,
                            'start_date': result['data'].index[0].isoformat(),
                            'end_date': result['data'].index[-1].isoformat(),
                            'ict_compliant': ict_compliance.get('compliant', False),
                            'ict_status': ict_compliance.get('status', 'UNKNOWN'),
                            'analysis_quality': ict_compliance.get('analysis_quality', 'UNKNOWN'),
                            'source': result.get('source', 'unknown')
                        }
                        
                    else:
                        print(f"      ❌ FALLO - {result.get('error', 'Error desconocido')}")
                        download_results[symbol][timeframe] = {
                            'success': False,
                            'error': result.get('error', 'Unknown error'),
                            'bars_downloaded': 0
                        }
                        
                        # Si es timeframe crítico y falla, mostrar instrucciones
                        if config['critical']:
                            print(f"      ⚠️ CRÍTICO: {timeframe} es esencial para análisis ICT")
                            if 'instructions' in result:
                                for instruction in result['instructions']:
                                    print(f"         - {instruction}")
                
                except Exception as e:
                    print(f"      ❌ ERROR TÉCNICO - {e}")
                    download_results[symbol][timeframe] = {
                        'success': False,
                        'error': str(e),
                        'bars_downloaded': 0
                    }
        
        print(f"\n📊 4. Generando reporte final...")
        
        # Calcular estadísticas finales
        total_successful = 0
        total_failed = 0
        total_bars = 0
        critical_failures = []
        
        for symbol, timeframes in download_results.items():
            for timeframe, result in timeframes.items():
                if result['success']:
                    total_successful += 1
                    total_bars += result['bars_downloaded']
                else:
                    total_failed += 1
                    if ict_timeframes_config[timeframe]['critical']:
                        critical_failures.append(f"{symbol} {timeframe}")
        
        # Guardar reporte detallado
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_downloads': total_downloads,
                'successful': total_successful,
                'failed': total_failed,
                'total_bars_downloaded': total_bars,
                'critical_failures': critical_failures,
                'success_rate': (total_successful / total_downloads) * 100
            },
            'results_by_symbol': download_results,
            'ict_configuration': ict_timeframes_config
        }
        
        # Guardar reporte
        report_file = Path("data/reports/ict_historical_download_report.json")
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ DESCARGA MASIVA ICT COMPLETADA")
        print(f"="*80)
        print(f"📊 ESTADÍSTICAS FINALES:")
        print(f"   Total descargas: {total_downloads}")
        print(f"   Exitosas: {total_successful} ({(total_successful/total_downloads)*100:.1f}%)")
        print(f"   Fallidas: {total_failed}")
        print(f"   Velas totales: {total_bars:,}")
        print(f"   Reporte guardado: {report_file}")
        
        if critical_failures:
            print(f"\n⚠️ TIMEFRAMES CRÍTICOS FALLIDOS:")
            for failure in critical_failures:
                print(f"   - {failure}")
            print(f"   ESTOS SON ESENCIALES PARA ANÁLISIS ICT")
        
        if total_successful >= (total_downloads * 0.8):  # 80% éxito
            print(f"\n🎉 SISTEMA ICT LISTO PARA ANÁLISIS INSTITUCIONAL")
            print(f"   Suficientes datos históricos para trading profesional")
        else:
            print(f"\n⚠️ DATOS INSUFICIENTES PARA ANÁLISIS ICT COMPLETO")
            print(f"   Revisar conexión MT5 y disponibilidad de símbolos")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO EN DESCARGA MASIVA: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_ict_data_integrity():
    """🔍 Verificar integridad de datos ICT descargados"""
    print("\n" + "="*50)
    print("🔍 VERIFICACIÓN DE INTEGRIDAD ICT")
    print("="*50)
    
    try:
        # Verificar si existe el reporte
        report_file = Path("data/reports/ict_historical_download_report.json")
        
        if not report_file.exists():
            print("❌ No se encontró reporte de descarga ICT")
            return False
        
        # Cargar y analizar reporte
        with open(report_file, 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        summary = report['summary']
        
        print(f"📊 Análisis del reporte ({report['timestamp']}):")
        print(f"   Tasa de éxito: {summary['success_rate']:.1f}%")
        print(f"   Velas totales: {summary['total_bars_downloaded']:,}")
        print(f"   Fallos críticos: {len(summary['critical_failures'])}")
        
        # Verificar archivos guardados
        data_dir = Path("data/candles")
        if data_dir.exists():
            csv_files = list(data_dir.glob("*.csv"))
            print(f"   Archivos CSV: {len(csv_files)}")
        else:
            print(f"   ❌ Directorio de datos no encontrado")
        
        # Análisis por símbolo
        print(f"\n📈 Por símbolo:")
        for symbol, timeframes in report['results_by_symbol'].items():
            successful_tf = sum(1 for tf, result in timeframes.items() if result['success'])
            total_tf = len(timeframes)
            total_bars_symbol = sum(result.get('bars_downloaded', 0) for result in timeframes.values())
            
            print(f"   {symbol}: {successful_tf}/{total_tf} timeframes, {total_bars_symbol:,} velas")
        
        # Recomendaciones
        if summary['success_rate'] >= 90:
            print(f"\n✅ INTEGRIDAD ICT EXCELENTE - Listo para trading")
        elif summary['success_rate'] >= 70:
            print(f"\n⚠️ INTEGRIDAD ICT ACEPTABLE - Revisar fallos")
        else:
            print(f"\n❌ INTEGRIDAD ICT INSUFICIENTE - Reejecutar descarga")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando integridad: {e}")
        return False

if __name__ == "__main__":
    print("🏛️ ICT ENGINE v6.0 - HISTORICAL DATA SETUP")
    print("=" * 80)
    print("Preparando el sistema con años de datos históricos para análisis ICT...")
    
    # Ejecutar descarga masiva
    download_success = setup_ict_historical_data()
    
    if download_success:
        # Verificar integridad
        verify_ict_data_integrity()
        
        print(f"\n🎯 PRÓXIMOS PASOS:")
        print(f"   1. Verificar que FundedNext MT5 esté conectado")
        print(f"   2. Ejecutar análisis ICT con datos históricos")
        print(f"   3. Configurar alertas para nuevas oportunidades")
        print(f"   4. Iniciar backtesting con datos reales")
    else:
        print(f"\n⚠️ CONFIGURACIÓN INCOMPLETA:")
        print(f"   - Verificar conexión MT5")
        print(f"   - Asegurar que FundedNext esté corriendo")
        print(f"   - Revisar disponibilidad de símbolos")
