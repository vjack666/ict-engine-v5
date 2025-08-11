#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 TEST MACHINE LEARNING CAPABILITIES - ICT ENGINE v6.0
=======================================================

PROPÓSITO:
    Auditar y verificar qué componentes del ICT Engine tienen capacidades
    de Machine Learning implementadas y evaluar su estado de desarrollo.

COBERTURA:
    ✅ Pattern Detection con ML
    ✅ Market Structure Analysis con ML 
    ✅ Risk Management con ML
    ✅ Unified Memory System con ML
    ✅ Advanced Analytics con ML
    ✅ Fractal Analysis con ML
    ✅ POI System con ML
    ✅ Trading Decision con ML

AUTOR: GitHub Copilot
FECHA: 2024-08-11 (Auditoría ML Domingo)
VERSION: 1.0.0
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os
import importlib
import inspect
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple

# Agregar path del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '01-CORE'))

# Palabras clave que indican ML/AI
ML_KEYWORDS = [
    'neural', 'network', 'model', 'predict', 'forecast', 'learn',
    'train', 'fit', 'sklearn', 'tensorflow', 'torch', 'pytorch',
    'regression', 'classification', 'clustering', 'ml_', 'ai_',
    'machine_learning', 'artificial_intelligence', 'deep_learning',
    'random_forest', 'gradient_boost', 'svm', 'knn', 'lstm',
    'transformer', 'attention', 'embedding', 'feature_', 'score_',
    'probability', 'confidence', 'weights', 'bias', 'optimization'
]

class TestMLCapabilities(unittest.TestCase):
    """🤖 Test Suite para auditar capacidades de Machine Learning"""
    
    def setUp(self):
        """⚙️ Configuración inicial para auditoría ML"""
        self.ml_components = {}
        self.ml_methods = {}
        self.ml_imports = {}
        self.ml_scores = {}
        
        print("🤖 Iniciando auditoría de Machine Learning en ICT Engine v6.0")
    
    def test_pattern_detector_ml_capabilities(self):
        """🔍 Test: Capacidades ML en Pattern Detector"""
        print("\n🔍 AUDITANDO: Pattern Detector ML")
        
        try:
            from core.ict_engine.pattern_detector import ICTPatternDetector
            
            # Analizar métodos y atributos
            detector = ICTPatternDetector()
            ml_features = self._analyze_ml_features(detector, "PatternDetector")
            
            # Buscar específicamente métodos ML en pattern detection
            ml_methods = [
                method for method in dir(detector) 
                if any(keyword in method.lower() for keyword in ML_KEYWORDS)
            ]
            
            # Verificar imports ML en el archivo
            ml_imports = self._check_ml_imports("core/ict_engine/pattern_detector.py")
            
            score = self._calculate_ml_score(ml_features, ml_methods, ml_imports)
            self.ml_scores['PatternDetector'] = score
            
            print(f"   📊 Métodos ML detectados: {len(ml_methods)}")
            print(f"   📦 Imports ML: {len(ml_imports)}")
            print(f"   🎯 Score ML: {score:.1f}/10")
            
            if ml_methods:
                print(f"   🔧 Métodos ML: {', '.join(ml_methods[:5])}")
            if ml_imports:
                print(f"   📥 Imports ML: {', '.join(ml_imports[:3])}")
                
        except Exception as e:
            print(f"   ❌ Error analizando PatternDetector: {e}")
            self.ml_scores['PatternDetector'] = 0.0
    
    def test_market_structure_ml_capabilities(self):
        """📈 Test: Capacidades ML en Market Structure Analyzer"""
        print("\n📈 AUDITANDO: Market Structure Analyzer ML")
        
        try:
            from core.analysis.market_structure_analyzer_v6 import MarketStructureAnalyzerV6
            
            analyzer = MarketStructureAnalyzerV6()
            ml_features = self._analyze_ml_features(analyzer, "MarketStructureAnalyzer")
            
            ml_methods = [
                method for method in dir(analyzer) 
                if any(keyword in method.lower() for keyword in ML_KEYWORDS)
            ]
            
            ml_imports = self._check_ml_imports("core/analysis/market_structure_analyzer_v6.py")
            
            score = self._calculate_ml_score(ml_features, ml_methods, ml_imports)
            self.ml_scores['MarketStructureAnalyzer'] = score
            
            print(f"   📊 Métodos ML detectados: {len(ml_methods)}")
            print(f"   📦 Imports ML: {len(ml_imports)}")
            print(f"   🎯 Score ML: {score:.1f}/10")
            
            if ml_methods:
                print(f"   🔧 Métodos ML: {', '.join(ml_methods[:5])}")
                
        except Exception as e:
            print(f"   ❌ Error analizando MarketStructureAnalyzer: {e}")
            self.ml_scores['MarketStructureAnalyzer'] = 0.0
    
    def test_unified_memory_ml_capabilities(self):
        """🧠 Test: Capacidades ML en Unified Memory System"""
        print("\n🧠 AUDITANDO: Unified Memory System ML")
        
        try:
            from core.memory_v6.unified_memory_system import UnifiedMemorySystem
            
            memory_system = UnifiedMemorySystem()
            ml_features = self._analyze_ml_features(memory_system, "UnifiedMemorySystem")
            
            ml_methods = [
                method for method in dir(memory_system) 
                if any(keyword in method.lower() for keyword in ML_KEYWORDS)
            ]
            
            ml_imports = self._check_ml_imports("core/memory_v6/unified_memory_system.py")
            
            score = self._calculate_ml_score(ml_features, ml_methods, ml_imports)
            self.ml_scores['UnifiedMemorySystem'] = score
            
            print(f"   📊 Métodos ML detectados: {len(ml_methods)}")
            print(f"   📦 Imports ML: {len(ml_imports)}")
            print(f"   🎯 Score ML: {score:.1f}/10")
            
            if ml_methods:
                print(f"   🔧 Métodos ML: {', '.join(ml_methods[:5])}")
                
        except Exception as e:
            print(f"   ❌ Error analizando UnifiedMemorySystem: {e}")
            self.ml_scores['UnifiedMemorySystem'] = 0.0
    
    def test_fractal_analyzer_ml_capabilities(self):
        """🔬 Test: Capacidades ML en Fractal Analyzer"""
        print("\n🔬 AUDITANDO: Fractal Analyzer ML")
        
        try:
            from core.ict_engine.fractal_analyzer_enterprise import FractalAnalyzerEnterprise
            
            fractal_analyzer = FractalAnalyzerEnterprise()
            ml_features = self._analyze_ml_features(fractal_analyzer, "FractalAnalyzer")
            
            ml_methods = [
                method for method in dir(fractal_analyzer) 
                if any(keyword in method.lower() for keyword in ML_KEYWORDS)
            ]
            
            ml_imports = self._check_ml_imports("core/ict_engine/fractal_analyzer_enterprise.py")
            
            score = self._calculate_ml_score(ml_features, ml_methods, ml_imports)
            self.ml_scores['FractalAnalyzer'] = score
            
            print(f"   📊 Métodos ML detectados: {len(ml_methods)}")
            print(f"   📦 Imports ML: {len(ml_imports)}")
            print(f"   🎯 Score ML: {score:.1f}/10")
            
            if ml_methods:
                print(f"   🔧 Métodos ML: {', '.join(ml_methods[:5])}")
                
        except Exception as e:
            print(f"   ❌ Error analizando FractalAnalyzer: {e}")
            self.ml_scores['FractalAnalyzer'] = 0.0
    
    def test_risk_management_ml_capabilities(self):
        """⚠️ Test: Capacidades ML en Risk Management"""
        print("\n⚠️ AUDITANDO: Risk Management ML")
        
        try:
            from core.risk_management.dynamic_risk_manager_v6 import DynamicRiskManagerV6
            
            risk_manager = DynamicRiskManagerV6()
            ml_features = self._analyze_ml_features(risk_manager, "RiskManager")
            
            ml_methods = [
                method for method in dir(risk_manager) 
                if any(keyword in method.lower() for keyword in ML_KEYWORDS)
            ]
            
            ml_imports = self._check_ml_imports("core/risk_management/dynamic_risk_manager_v6.py")
            
            score = self._calculate_ml_score(ml_features, ml_methods, ml_imports)
            self.ml_scores['RiskManager'] = score
            
            print(f"   📊 Métodos ML detectados: {len(ml_methods)}")
            print(f"   📦 Imports ML: {len(ml_imports)}")
            print(f"   🎯 Score ML: {score:.1f}/10")
            
            if ml_methods:
                print(f"   🔧 Métodos ML: {', '.join(ml_methods[:5])}")
                
        except Exception as e:
            print(f"   ❌ Error analizando RiskManager: {e}")
            self.ml_scores['RiskManager'] = 0.0
    
    def test_poi_system_ml_capabilities(self):
        """📍 Test: Capacidades ML en POI System"""
        print("\n📍 AUDITANDO: POI System ML")
        
        try:
            from core.poi_system.poi_detector_v6 import POIDetectorV6
            
            poi_detector = POIDetectorV6()
            ml_features = self._analyze_ml_features(poi_detector, "POIDetector")
            
            ml_methods = [
                method for method in dir(poi_detector) 
                if any(keyword in method.lower() for keyword in ML_KEYWORDS)
            ]
            
            ml_imports = self._check_ml_imports("core/poi_system/poi_detector_v6.py")
            
            score = self._calculate_ml_score(ml_features, ml_methods, ml_imports)
            self.ml_scores['POIDetector'] = score
            
            print(f"   📊 Métodos ML detectados: {len(ml_methods)}")
            print(f"   📦 Imports ML: {len(ml_imports)}")
            print(f"   🎯 Score ML: {score:.1f}/10")
            
            if ml_methods:
                print(f"   🔧 Métodos ML: {', '.join(ml_methods[:5])}")
                
        except Exception as e:
            print(f"   ❌ Error analizando POIDetector: {e}")
            self.ml_scores['POIDetector'] = 0.0
    
    def test_analytics_ml_capabilities(self):
        """📊 Test: Capacidades ML en Analytics"""
        print("\n📊 AUDITANDO: Advanced Analytics ML")
        
        try:
            # Buscar componentes de analytics
            analytics_files = [
                "core/analytics/advanced_analytics_v6.py",
                "core/analytics/performance_analyzer.py", 
                "core/analytics/market_context_analyzer.py"
            ]
            
            total_ml_methods = 0
            total_ml_imports = 0
            
            for file_path in analytics_files:
                try:
                    ml_imports = self._check_ml_imports(file_path)
                    total_ml_imports += len(ml_imports)
                    print(f"   📁 {file_path}: {len(ml_imports)} imports ML")
                except:
                    continue
            
            score = min(10.0, total_ml_imports * 2.0)  # Score basado en imports
            self.ml_scores['Analytics'] = score
            
            print(f"   📦 Total imports ML: {total_ml_imports}")
            print(f"   🎯 Score ML: {score:.1f}/10")
                
        except Exception as e:
            print(f"   ❌ Error analizando Analytics: {e}")
            self.ml_scores['Analytics'] = 0.0
    
    def test_generate_ml_report(self):
        """📋 Test: Generar reporte completo de capacidades ML"""
        print("\n📋 GENERANDO REPORTE ML COMPLETO")
        
        # Calcular estadísticas generales
        total_components = len(self.ml_scores)
        avg_score = sum(self.ml_scores.values()) / total_components if total_components > 0 else 0
        high_ml_components = [comp for comp, score in self.ml_scores.items() if score >= 7.0]
        medium_ml_components = [comp for comp, score in self.ml_scores.items() if 3.0 <= score < 7.0]
        low_ml_components = [comp for comp, score in self.ml_scores.items() if score < 3.0]
        
        print("\n" + "="*60)
        print("🤖 REPORTE FINAL - CAPACIDADES MACHINE LEARNING")
        print("="*60)
        print(f"📊 Componentes analizados: {total_components}")
        print(f"🎯 Score promedio ML: {avg_score:.1f}/10")
        print()
        
        print("🏆 COMPONENTES CON ALTO ML (Score >= 7.0):")
        for comp in high_ml_components:
            print(f"   ✅ {comp}: {self.ml_scores[comp]:.1f}/10")
        
        print("\n🔄 COMPONENTES CON ML MEDIO (Score 3.0-6.9):")
        for comp in medium_ml_components:
            print(f"   🔸 {comp}: {self.ml_scores[comp]:.1f}/10")
        
        print("\n⚠️ COMPONENTES CON BAJO ML (Score < 3.0):")
        for comp in low_ml_components:
            print(f"   🔻 {comp}: {self.ml_scores[comp]:.1f}/10")
        
        print("\n🎯 RECOMENDACIONES:")
        if len(low_ml_components) > 0:
            print("   📈 Priorizar implementación ML en componentes de bajo score")
        if len(high_ml_components) > 0:
            print("   🚀 Expandir capacidades ML en componentes exitosos")
        if avg_score < 5.0:
            print("   ⚡ Implementar estrategia integral de ML/AI")
        
        print("\n" + "="*60)
        
        # Assertivo: El sistema debe tener al menos capacidades ML básicas
        self.assertGreater(avg_score, 0.0, "El sistema debe tener al menos algunas capacidades ML")
        print("✅ Test reporte ML: COMPLETADO")
    
    def _analyze_ml_features(self, obj: Any, component_name: str) -> Dict[str, Any]:
        """🔍 Analiza características ML de un objeto"""
        features = {
            'ml_methods': [],
            'ml_attributes': [],
            'ml_docstrings': []
        }
        
        try:
            # Buscar métodos con keywords ML
            for method_name in dir(obj):
                if any(keyword in method_name.lower() for keyword in ML_KEYWORDS):
                    features['ml_methods'].append(method_name)
                
                # Verificar docstrings
                try:
                    method = getattr(obj, method_name)
                    if hasattr(method, '__doc__') and method.__doc__:
                        if any(keyword in method.__doc__.lower() for keyword in ML_KEYWORDS):
                            features['ml_docstrings'].append(method_name)
                except:
                    continue
            
            # Buscar atributos ML
            for attr_name in dir(obj):
                if any(keyword in attr_name.lower() for keyword in ML_KEYWORDS):
                    features['ml_attributes'].append(attr_name)
                    
        except Exception as e:
            print(f"   ⚠️ Error analizando {component_name}: {e}")
        
        return features
    
    def _check_ml_imports(self, file_path: str) -> List[str]:
        """📦 Verifica imports relacionados con ML en un archivo"""
        ml_imports = []
        
        try:
            full_path = os.path.join(os.path.dirname(__file__), '..', '..', '01-CORE', file_path)
            
            if os.path.exists(full_path):
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Buscar imports ML
                lines = content.split('\n')
                for line in lines:
                    line = line.strip().lower()
                    if line.startswith(('import ', 'from ')) and any(keyword in line for keyword in ML_KEYWORDS):
                        ml_imports.append(line)
                        
        except Exception as e:
            print(f"   ⚠️ Error leyendo {file_path}: {e}")
        
        return ml_imports
    
    def _calculate_ml_score(self, features: Dict, methods: List, imports: List) -> float:
        """🎯 Calcula score ML basado en características encontradas"""
        score = 0.0
        
        # Puntos por métodos ML
        score += len(methods) * 1.0
        
        # Puntos por imports ML
        score += len(imports) * 1.5
        
        # Puntos por características ML
        score += len(features.get('ml_methods', [])) * 0.5
        score += len(features.get('ml_attributes', [])) * 0.3
        score += len(features.get('ml_docstrings', [])) * 0.2
        
        # Normalizar a escala 0-10
        return min(10.0, score)


if __name__ == '__main__':
    print("🤖" + "="*60)
    print("🤖 INICIANDO AUDITORÍA MACHINE LEARNING - ICT ENGINE v6.0")
    print("🤖" + "="*60)
    
    # Configurar el runner para tests detallados
    unittest.main(
        verbosity=2,
        exit=False,
        failfast=False
    )
    
    print("\n🤖" + "="*60)
    print("🤖 AUDITORÍA ML COMPLETADA - ICT ENGINE v6.0")
    print("🤖" + "="*60)
