#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 AUDITORÍA ML REAL - ICT ENGINE v6.0
=====================================

PROPÓSITO:
    Auditoría real de capacidades ML existentes sin depender de imports complejos.
    Analiza directamente los archivos de código fuente para identificar:
    - Métodos con algoritmos ML/AI
    - Técnicas de scoring y probabilidad
    - Sistemas de pesos y clasificación
    - Capacidades de predicción

AUTOR: GitHub Copilot
FECHA: 2024-08-11
VERSION: 1.0.0
"""

import os
import re
import unittest
from typing import Dict, List, Tuple

class MLCapabilitiesRealAudit(unittest.TestCase):
    """🤖 Auditoría Real de Capacidades ML en ICT Engine"""
    
    def setUp(self):
        """⚙️ Configuración inicial"""
        self.base_path = os.path.join(os.path.dirname(__file__), '..', '..', '01-CORE')
        self.ml_indicators = {
            'probability': r'probability|prob_|_prob\b',
            'confidence': r'confidence|conf_|_conf\b',
            'score': r'score|scoring|_score\b',
            'weight': r'weight|weigh|_weight\b',
            'bias': r'bias|_bias\b',
            'prediction': r'predict|prediction|forecast',
            'classification': r'classif|classify|_class\b',
            'intelligence': r'smart_|intelligent|ai_|ml_',
            'learning': r'learn|training|adapt',
            'enhanced': r'enhanced|advanced|enterprise'
        }
        self.ml_scores = {}
        
    def test_pattern_detector_ml_analysis(self):
        """🔍 Análisis ML real en Pattern Detector"""
        print("\n🔍 AUDITORÍA ML: Pattern Detector")
        
        file_path = os.path.join(self.base_path, 'core', 'ict_engine', 'pattern_detector.py')
        ml_score = self._analyze_file_ml_capabilities(file_path, 'PatternDetector')
        
        print(f"   🎯 Score ML: {ml_score:.1f}/10")
        self.ml_scores['PatternDetector'] = ml_score
        
        # El Pattern Detector debe tener al menos capacidades básicas ML
        self.assertGreaterEqual(ml_score, 3.0, "Pattern Detector debe tener capacidades ML básicas")
    
    def test_fractal_analyzer_ml_analysis(self):
        """🔬 Análisis ML real en Fractal Analyzer"""
        print("\n🔬 AUDITORÍA ML: Fractal Analyzer")
        
        file_path = os.path.join(self.base_path, 'core', 'ict_engine', 'fractal_analyzer_enterprise.py')
        ml_score = self._analyze_file_ml_capabilities(file_path, 'FractalAnalyzer')
        
        print(f"   🎯 Score ML: {ml_score:.1f}/10")
        self.ml_scores['FractalAnalyzer'] = ml_score
    
    def test_advanced_candle_downloader_ml_analysis(self):
        """📊 Análisis ML real en Advanced Candle Downloader"""
        print("\n📊 AUDITORÍA ML: Advanced Candle Downloader")
        
        file_path = os.path.join(self.base_path, 'core', 'data_management', 'advanced_candle_downloader.py')
        ml_score = self._analyze_file_ml_capabilities(file_path, 'AdvancedCandleDownloader')
        
        print(f"   🎯 Score ML: {ml_score:.1f}/10")
        self.ml_scores['AdvancedCandleDownloader'] = ml_score
    
    def test_memory_system_ml_analysis(self):
        """🧠 Análisis ML real en Memory Systems"""
        print("\n🧠 AUDITORÍA ML: Memory Systems")
        
        memory_files = [
            'core/analysis/unified_memory_system.py',
            'core/memory_v6/market_memory_v6.py',
            'core/memory_v6/historical_memory_v6.py'
        ]
        
        total_score = 0
        files_found = 0
        
        for file_rel_path in memory_files:
            file_path = os.path.join(self.base_path, *file_rel_path.split('/'))
            if os.path.exists(file_path):
                score = self._analyze_file_ml_capabilities(file_path, os.path.basename(file_rel_path))
                total_score += score
                files_found += 1
        
        avg_score = total_score / files_found if files_found > 0 else 0
        print(f"   🎯 Score ML promedio: {avg_score:.1f}/10 ({files_found} archivos)")
        self.ml_scores['MemorySystems'] = avg_score
    
    def test_z_generate_ml_enhancement_recommendations(self):
        """📋 Generar recomendaciones de mejora ML (ejecuta al final)"""
        print("\n📋 REPORTE Y RECOMENDACIONES ML")
        
        # Calcular estadísticas
        if self.ml_scores:
            avg_score = sum(self.ml_scores.values()) / len(self.ml_scores)
            max_score = max(self.ml_scores.values())
            min_score = min(self.ml_scores.values())
            
            print(f"\n📊 ESTADÍSTICAS ML:")
            print(f"   📈 Score promedio: {avg_score:.1f}/10")
            print(f"   🏆 Score máximo: {max_score:.1f}/10")
            print(f"   📉 Score mínimo: {min_score:.1f}/10")
            
            print(f"\n🔍 DETALLE POR COMPONENTE:")
            for component, score in sorted(self.ml_scores.items(), key=lambda x: x[1], reverse=True):
                status = "🏆" if score >= 7 else "🔸" if score >= 4 else "🔻"
                print(f"   {status} {component}: {score:.1f}/10")
            
            print(f"\n🎯 RECOMENDACIONES:")
            
            if avg_score < 3.0:
                print("   ⚡ CRÍTICO: Implementar estrategia integral ML/AI")
                print("   📚 Agregar librerías: scikit-learn, numpy, pandas")
                print("   🔧 Implementar algoritmos básicos de clasificación")
            elif avg_score < 6.0:
                print("   📈 MEJORAR: Expandir capacidades ML existentes")
                print("   🧠 Implementar sistemas de aprendizaje adaptativo")
                print("   📊 Agregar métricas de confianza más sofisticadas")
            else:
                print("   🚀 OPTIMIZAR: Sistema con buenas capacidades ML")
                print("   🎯 Implementar deep learning para patterns complejos")
                print("   🔮 Agregar capacidades de predicción temporal")
            
            # Identificar componente con menor ML para mejora prioritaria
            lowest_component = min(self.ml_scores.items(), key=lambda x: x[1])
            print(f"\n⚠️ PRIORIDAD: Mejorar {lowest_component[0]} (Score: {lowest_component[1]:.1f})")
            
        else:
            print("   ❌ No se pudo analizar ningún componente")
            
        print("\n" + "="*60)
    
    def _analyze_file_ml_capabilities(self, file_path: str, component_name: str) -> float:
        """🔍 Analiza capacidades ML reales de un archivo"""
        if not os.path.exists(file_path):
            print(f"   ❌ Archivo no encontrado: {component_name}")
            return 0.0
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Analizar indicadores ML
            ml_features = {}
            total_matches = 0
            
            for category, pattern in self.ml_indicators.items():
                matches = len(re.findall(pattern, content, re.IGNORECASE))
                ml_features[category] = matches
                total_matches += matches
            
            # Buscar métodos específicos ML
            ml_methods = re.findall(r'def\s+(\w*(?:predict|score|weight|prob|conf|classif|ai_|ml_)\w*)', content, re.IGNORECASE)
            
            # Buscar clases con capacidades ML
            ml_classes = re.findall(r'class\s+(\w*(?:ML|AI|Smart|Intelligence|Enhanced|Enterprise)\w*)', content, re.IGNORECASE)
            
            # Calcular score
            score = min(10.0, (
                total_matches * 0.1 +  # 0.1 por cada match de palabra clave
                len(ml_methods) * 1.0 +  # 1.0 por cada método ML
                len(ml_classes) * 2.0    # 2.0 por cada clase ML
            ))
            
            # Mostrar detalles
            print(f"   📊 Indicadores ML: {total_matches} matches")
            print(f"   🔧 Métodos ML: {len(ml_methods)}")
            print(f"   🏗️ Clases ML: {len(ml_classes)}")
            
            if ml_methods:
                print(f"   📝 Métodos destacados: {', '.join(ml_methods[:3])}")
            
            # Mostrar categorías con más matches
            top_categories = sorted(ml_features.items(), key=lambda x: x[1], reverse=True)[:3]
            if any(count > 0 for _, count in top_categories):
                print(f"   🎯 Categorías principales: {', '.join(f'{cat}({count})' for cat, count in top_categories if count > 0)}")
            
            return score
            
        except Exception as e:
            print(f"   ❌ Error analizando {component_name}: {e}")
            return 0.0


if __name__ == '__main__':
    print("🤖" + "="*60)
    print("🤖 INICIANDO AUDITORÍA ML REAL - ICT ENGINE v6.0")
    print("🤖" + "="*60)
    
    unittest.main(verbosity=2, exit=False)
    
    print("\n🤖" + "="*60)
    print("🤖 AUDITORÍA ML REAL COMPLETADA")
    print("🤖" + "="*60)
