#!/usr/bin/env python3
"""
🧪 APLICACIÓN REGLA #7 - TESTS PRIMERO
======================================

Demostración de la REGLA #7: Si un test está bien redactado, modificar el código, NO el test.

Este script analiza tests fallidos y determina si la falla es del código o del test,
aplicando la metodología establecida en la REGLA #7.

Fecha: Agosto 8, 2025
Aplicando: REGLAS_COPILOT.md - REGLA #7
"""

import os
import subprocess
import ast
from pathlib import Path
from datetime import datetime

# ✅ REGLA #4: Importar SIC Bridge y SLUC
try:
    from sistema.sic_bridge import SICBridge
    from core.smart_trading_logger import log_trading_decision_smart_v6
    SIC_SLUC_AVAILABLE = True
except ImportError:
    print("⚠️ SIC/SLUC no disponible - modo fallback")
    SIC_SLUC_AVAILABLE = False
    
    def log_trading_decision_smart_v6(event_type, data, **kwargs):
        print(f"[{event_type}] {data}")

def analyze_test_quality(test_file_path: str) -> dict:
    """
    ✅ REGLA #7: Analizar calidad de un test para determinar si está bien redactado
    
    Retorna análisis de calidad del test según criterios de REGLA #7
    """
    
    log_trading_decision_smart_v6("TEST_ANALYSIS_START", {
        "rule": "REGLA #7 - Tests Primero",
        "test_file": str(test_file_path),
        "purpose": "Determinar si test está bien redactado"
    })
    
    analysis = {
        "file_path": str(test_file_path),
        "is_well_written": False,
        "quality_score": 0.0,
        "criteria_scores": {},
        "issues_found": [],
        "recommendations": []
    }
    
    try:
        # Leer archivo de test
        with open(test_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ✅ REGLA #7: Criterios para test bien redactado
        criteria = {
            "descriptive_names": 0.0,      # Nombres descriptivos
            "clear_logic": 0.0,            # Lógica clara
            "appropriate_assertions": 0.0,  # Assertions apropiadas
            "realistic_cases": 0.0,        # Casos realistas
            "proper_setup": 0.0,           # Setup apropiado
            "documentation": 0.0           # Documentación
        }
        
        lines = content.split('\n')
        
        # 1. ✅ Verificar nombres descriptivos
        descriptive_test_names = 0
        total_test_functions = 0
        
        for line in lines:
            if line.strip().startswith('def test_'):
                total_test_functions += 1
                test_name = line.split('def ')[1].split('(')[0]
                # Nombre descriptivo si tiene más de 3 palabras separadas por _
                if len(test_name.split('_')) >= 3:
                    descriptive_test_names += 1
        
        if total_test_functions > 0:
            criteria["descriptive_names"] = descriptive_test_names / total_test_functions
        
        # 2. ✅ Verificar lógica clara (docstrings en tests)
        docstring_tests = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('def test_') and i + 1 < len(lines):
                if '"""' in lines[i + 1] or "'''" in lines[i + 1]:
                    docstring_tests += 1
        
        if total_test_functions > 0:
            criteria["clear_logic"] = docstring_tests / total_test_functions
        
        # 3. ✅ Verificar assertions apropiadas
        assertion_keywords = ['assert', 'assertEqual', 'assertTrue', 'assertFalse', 'assertIn']
        assertion_count = 0
        
        for line in lines:
            if any(keyword in line for keyword in assertion_keywords):
                assertion_count += 1
        
        # Ratio de assertions por test (ideal: 1-5 assertions por test)
        if total_test_functions > 0:
            assertions_per_test = assertion_count / total_test_functions
            criteria["appropriate_assertions"] = min(1.0, assertions_per_test / 3.0)
        
        # 4. ✅ Verificar casos realistas (buscar datos de prueba sensatos)
        realistic_indicators = ['EURUSD', 'data', 'timeframe', 'price', 'volume']
        realistic_score = 0
        
        for indicator in realistic_indicators:
            if indicator in content:
                realistic_score += 0.2
        
        criteria["realistic_cases"] = min(1.0, realistic_score)
        
        # 5. ✅ Verificar setup apropiado (setUp, fixtures, etc.)
        setup_indicators = ['setUp', 'fixture', '@pytest', 'before', 'setup']
        setup_score = 0
        
        for indicator in setup_indicators:
            if indicator in content:
                setup_score += 0.3
        
        criteria["proper_setup"] = min(1.0, setup_score)
        
        # 6. ✅ Verificar documentación
        doc_indicators = ['"""', "'''", '#', 'Test:', 'Verifica', 'Prueba']
        doc_score = 0
        
        for indicator in doc_indicators:
            if indicator in content:
                doc_score += 0.2
        
        criteria["documentation"] = min(1.0, doc_score)
        
        # Calcular score total
        analysis["criteria_scores"] = criteria
        analysis["quality_score"] = sum(criteria.values()) / len(criteria)
        
        # ✅ REGLA #7: Determinar si está bien redactado (threshold: 0.6)
        analysis["is_well_written"] = analysis["quality_score"] >= 0.6
        
        # Identificar issues y recomendaciones
        if criteria["descriptive_names"] < 0.5:
            analysis["issues_found"].append("Nombres de test poco descriptivos")
            analysis["recommendations"].append("Usar nombres más descriptivos como test_detect_bos_with_valid_data")
        
        if criteria["clear_logic"] < 0.3:
            analysis["issues_found"].append("Falta documentación en tests")
            analysis["recommendations"].append("Agregar docstrings explicando qué se está probando")
        
        if criteria["appropriate_assertions"] < 0.3:
            analysis["issues_found"].append("Pocas assertions por test")
            analysis["recommendations"].append("Agregar más assertions específicas")
        
        if criteria["realistic_cases"] < 0.4:
            analysis["issues_found"].append("Casos de prueba poco realistas")
            analysis["recommendations"].append("Usar datos de mercado reales para tests")
        
        log_trading_decision_smart_v6("TEST_ANALYSIS_COMPLETE", {
            "quality_score": analysis["quality_score"],
            "is_well_written": analysis["is_well_written"],
            "total_tests": total_test_functions,
            "issues_count": len(analysis["issues_found"])
        })
        
        return analysis
        
    except Exception as e:
        log_trading_decision_smart_v6("TEST_ANALYSIS_ERROR", {
            "error": str(e),
            "file": str(test_file_path)
        })
        analysis["issues_found"].append(f"Error analizando archivo: {e}")
        return analysis

def apply_rule_7_decision(test_analysis: dict, test_failure_info: str) -> dict:
    """
    ✅ REGLA #7: Tomar decisión de modificar código vs test basado en análisis
    """
    
    decision = {
        "modify_code": False,
        "modify_test": False,
        "reasoning": "",
        "action_plan": [],
        "documentation_required": []
    }
    
    log_trading_decision_smart_v6("RULE_7_DECISION_START", {
        "test_quality_score": test_analysis["quality_score"],
        "is_well_written": test_analysis["is_well_written"],
        "failure_info": test_failure_info[:200]  # Truncar para logging
    })
    
    # ✅ REGLA #7: Si test está bien redactado → Modificar CÓDIGO
    if test_analysis["is_well_written"]:
        decision["modify_code"] = True
        decision["reasoning"] = (
            f"Test está bien redactado (score: {test_analysis['quality_score']:.2f}). "
            "Según REGLA #7, el problema está en el CÓDIGO, no en el test."
        )
        decision["action_plan"] = [
            "1. Analizar falla específica del test",
            "2. Identificar qué parte del código no cumple la especificación",
            "3. Modificar el código para hacer pasar el test",
            "4. Validar que otros tests siguen pasando",
            "5. Documentar el cambio en SLUC"
        ]
        decision["documentation_required"] = [
            "Registrar en SLUC por qué se modificó código",
            "Documentar análisis de calidad del test",
            "Actualizar bitácora con lección aprendida"
        ]
    
    # ⚠️ REGLA #7: Si test mal redactado → Analizar más y posiblemente modificar test
    else:
        decision["modify_test"] = True
        decision["reasoning"] = (
            f"Test mal redactado (score: {test_analysis['quality_score']:.2f}). "
            "Issues encontrados: " + ", ".join(test_analysis["issues_found"][:3])
        )
        decision["action_plan"] = [
            "1. Revisar issues específicos del test",
            "2. Corregir problemas de redacción identificados",
            "3. Aplicar recomendaciones de mejora",
            "4. Validar que el test mejorado sigue siendo válido",
            "5. Documentar por qué se modificó el test"
        ]
        decision["documentation_required"] = [
            "Documentar detalladamente por qué test era incorrecto",
            "Registrar issues específicos encontrados",
            "Documentar mejoras aplicadas",
            "Actualizar bitácora con lecciones sobre calidad de tests"
        ]
    
    log_trading_decision_smart_v6("RULE_7_DECISION_COMPLETE", {
        "decision": "modify_code" if decision["modify_code"] else "modify_test",
        "reasoning_length": len(decision["reasoning"]),
        "action_steps": len(decision["action_plan"])
    })
    
    return decision

def demonstrate_rule_7():
    """
    ✅ REGLA #7: Demostración completa de la aplicación de la regla
    """
    
    print("🧪 DEMOSTRACIÓN REGLA #7 - TESTS PRIMERO")
    print("=" * 60)
    
    # Buscar archivos de test en el proyecto
    project_root = Path(__file__).parent.parent
    test_files = list(project_root.glob("tests/test_*.py"))
    
    if not test_files:
        print("⚠️ No se encontraron archivos de test")
        return
    
    print(f"📋 Archivos de test encontrados: {len(test_files)}")
    
    # Analizar un test específico como ejemplo
    example_test = None
    for test_file in test_files:
        if "phase2" in test_file.name or "memory" in test_file.name:
            example_test = test_file
            break
    
    if not example_test and test_files:
        example_test = test_files[0]
    
    if example_test:
        print(f"\n🔍 Analizando test ejemplo: {example_test.name}")
        
        # ✅ REGLA #7: Analizar calidad del test
        analysis = analyze_test_quality(example_test)
        
        print(f"\n📊 ANÁLISIS DE CALIDAD DEL TEST:")
        print(f"   Score general: {analysis['quality_score']:.2f}/1.0")
        print(f"   Bien redactado: {'✅ SÍ' if analysis['is_well_written'] else '❌ NO'}")
        
        if analysis['criteria_scores']:
            print(f"\n📋 Criterios evaluados:")
            for criteria, score in analysis['criteria_scores'].items():
                print(f"   {criteria}: {score:.2f}")
        
        if analysis['issues_found']:
            print(f"\n⚠️ Issues encontrados:")
            for issue in analysis['issues_found']:
                print(f"   - {issue}")
        
        if analysis['recommendations']:
            print(f"\n💡 Recomendaciones:")
            for rec in analysis['recommendations']:
                print(f"   - {rec}")
        
        # ✅ REGLA #7: Simular decisión con falla de test
        simulated_failure = "AssertionError: Expected True but got False in BOS detection"
        
        print(f"\n🎯 APLICANDO REGLA #7:")
        print(f"   Falla simulada: {simulated_failure}")
        
        decision = apply_rule_7_decision(analysis, simulated_failure)
        
        print(f"\n📋 DECISIÓN REGLA #7:")
        print(f"   Modificar código: {'✅ SÍ' if decision['modify_code'] else '❌ NO'}")
        print(f"   Modificar test: {'✅ SÍ' if decision['modify_test'] else '❌ NO'}")
        print(f"   Razonamiento: {decision['reasoning']}")
        
        print(f"\n🎯 PLAN DE ACCIÓN:")
        for i, action in enumerate(decision['action_plan'], 1):
            print(f"   {action}")
        
        print(f"\n📝 DOCUMENTACIÓN REQUERIDA:")
        for doc in decision['documentation_required']:
            print(f"   - {doc}")
    
    # ✅ REGLA #5: Documentar aplicación de regla
    print(f"\n" + "=" * 60)
    print(f"📊 RESUMEN APLICACIÓN REGLA #7:")
    print(f"   Regla aplicada exitosamente ✅")
    print(f"   Metodología de análisis establecida ✅")
    print(f"   Criterios de calidad definidos ✅")
    print(f"   Proceso de decisión automatizado ✅")
    print(f"   Documentación de decisiones implementada ✅")
    
    return True

def main():
    """
    Main function aplicando todas las reglas Copilot
    """
    
    # ✅ REGLA #4: Verificar SIC system ready (si está disponible)
    if SIC_SLUC_AVAILABLE:
        try:
            sic = SICBridge()
            log_trading_decision_smart_v6("SIC_STATUS", {
                "available": True,
                "rule_7_demo": True
            })
        except Exception as e:
            log_trading_decision_smart_v6("SIC_WARNING", {
                "warning": str(e),
                "continuing": "with REGLA #7 demo"
            })
    
    # Ejecutar demostración
    success = demonstrate_rule_7()
    
    if success:
        print("\n🎉 REGLA #7 APLICADA EXITOSAMENTE")
        print("📋 Metodología de 'Tests Primero' establecida")
        print("🔧 Proceso de análisis de calidad implementado")
        print("🎯 Decisiones automáticas código vs test funcionando")
    else:
        print("\n❌ PROBLEMAS EN APLICACIÓN REGLA #7")
        print("🔧 Revisar logs para más detalles")

if __name__ == "__main__":
    main()
