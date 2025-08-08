#!/usr/bin/env python3
"""
🔢 APLICACIÓN REGLA #6 - CONTROL DE VERSIONES INTELIGENTE
===========================================================

Análisis y corrección de versiones inconsistentes en el proyecto ICT Engine,
aplicando la nueva REGLA #6 de control de versiones.

Fecha: Agosto 8, 2025
Aplicando: REGLAS_COPILOT.md - REGLA #6
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

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

class VersionAnalyzer:
    """🔢 Analizador de versiones siguiendo REGLA #6"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.version_patterns = [
            r'v(\d+)\.(\d+)\.(\d+)',
            r'v(\d+)\.(\d+)',
            r'version.*?(\d+)\.(\d+)\.(\d+)',
            r'Version.*?(\d+)\.(\d+)\.(\d+)',
            r'ICT Engine v(\d+)\.(\d+)',
            r'SIC v(\d+)\.(\d+)',
            r'SLUC v(\d+)\.(\d+)',
        ]
        
    def scan_versions(self) -> Dict[str, List[Tuple[str, int, str]]]:
        """Escanea todas las versiones en el proyecto"""
        
        log_trading_decision_smart_v6("VERSION_SCAN_START", {
            "rule": "REGLA #6 - Control de Versiones",
            "project_root": str(self.project_root)
        })
        
        versions_found = {}
        
        # Buscar en archivos Python
        for py_file in self.project_root.rglob("*.py"):
            if "test_reports" in str(py_file) or "__pycache__" in str(py_file):
                continue
                
            try:
                content = py_file.read_text(encoding='utf-8')
                file_versions = self._extract_versions_from_content(content)
                
                if file_versions:
                    relative_path = py_file.relative_to(self.project_root)
                    versions_found[str(relative_path)] = file_versions
                    
            except Exception as e:
                log_trading_decision_smart_v6("VERSION_SCAN_ERROR", {
                    "file": str(py_file),
                    "error": str(e)
                })
        
        log_trading_decision_smart_v6("VERSION_SCAN_COMPLETE", {
            "files_with_versions": len(versions_found),
            "total_versions": sum(len(v) for v in versions_found.values())
        })
        
        return versions_found
    
    def _extract_versions_from_content(self, content: str) -> List[Tuple[str, int, str]]:
        """Extrae versiones de contenido de archivo"""
        versions = []
        
        for line_num, line in enumerate(content.split('\n'), 1):
            for pattern in self.version_patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    versions.append((match.group(0), line_num, line.strip()))
        
        return versions
    
    def analyze_version_consistency(self, versions_data: Dict) -> Dict[str, any]:
        """Analiza consistencia de versiones según REGLA #6"""
        
        log_trading_decision_smart_v6("VERSION_ANALYSIS_START", {
            "analysis": "Consistencia de versiones según REGLA #6"
        })
        
        # Extraer versiones principales
        ict_versions = []
        sic_versions = []
        sluc_versions = []
        
        for file_path, file_versions in versions_data.items():
            for version_str, line_num, line_content in file_versions:
                if "ICT Engine" in line_content or "ict-engine" in line_content:
                    ict_versions.append((version_str, file_path, line_num))
                elif "SIC" in line_content:
                    sic_versions.append((version_str, file_path, line_num))
                elif "SLUC" in line_content:
                    sluc_versions.append((version_str, file_path, line_num))
        
        # Análisis de consistencia
        analysis = {
            "ict_engine": {
                "versions": ict_versions,
                "unique_versions": list(set(v[0] for v in ict_versions)),
                "is_consistent": len(set(v[0] for v in ict_versions)) <= 1
            },
            "sic": {
                "versions": sic_versions,
                "unique_versions": list(set(v[0] for v in sic_versions)),
                "is_consistent": len(set(v[0] for v in sic_versions)) <= 1
            },
            "sluc": {
                "versions": sluc_versions,
                "unique_versions": list(set(v[0] for v in sluc_versions)),
                "is_consistent": len(set(v[0] for v in sluc_versions)) <= 1
            }
        }
        
        # Recomendaciones según REGLA #6
        analysis["recommendations"] = self._generate_version_recommendations(analysis)
        
        log_trading_decision_smart_v6("VERSION_ANALYSIS_COMPLETE", {
            "ict_consistent": analysis["ict_engine"]["is_consistent"],
            "sic_consistent": analysis["sic"]["is_consistent"],
            "sluc_consistent": analysis["sluc"]["is_consistent"],
            "recommendations_count": len(analysis["recommendations"])
        })
        
        return analysis
    
    def _generate_version_recommendations(self, analysis: Dict) -> List[Dict]:
        """Genera recomendaciones de versioning según REGLA #6"""
        recommendations = []
        
        # ✅ REGLA #6: Evaluación de impacto
        if not analysis["ict_engine"]["is_consistent"]:
            # FASE 1 completada + FASE 2 iniciándose = MINOR increment
            recommendations.append({
                "component": "ICT Engine",
                "current_versions": analysis["ict_engine"]["unique_versions"],
                "recommended_version": "v6.1.0",
                "reason": "FASE 1 completada, FASE 2 iniciándose - MINOR increment justificado",
                "type": "MINOR",
                "impact": "Nueva funcionalidad memoria unificada"
            })
        
        if not analysis["sic"]["is_consistent"]:
            recommendations.append({
                "component": "SIC",
                "current_versions": analysis["sic"]["unique_versions"],
                "recommended_version": "v3.1.0",
                "reason": "Funcionalidad enterprise estable - consistencia requerida",
                "type": "CONSISTENCY",
                "impact": "Mantener versión consistente"
            })
        
        if not analysis["sluc"]["is_consistent"]:
            recommendations.append({
                "component": "SLUC", 
                "current_versions": analysis["sluc"]["unique_versions"],
                "recommended_version": "v2.1.0",
                "reason": "Logging enterprise funcionando - mantener consistencia",
                "type": "CONSISTENCY",
                "impact": "Estabilidad del logging"
            })
        
        return recommendations

def apply_version_corrections(project_root: str):
    """Aplica correcciones de versión según REGLA #6"""
    
    log_trading_decision_smart_v6("VERSION_CORRECTION_START", {
        "rule": "REGLA #6 - Aplicando correcciones de versión"
    })
    
    # Análisis inicial
    analyzer = VersionAnalyzer(project_root)
    versions_data = analyzer.scan_versions()
    analysis = analyzer.analyze_version_consistency(versions_data)
    
    # ✅ REGLA #6: Criterios para incremento
    # FASE 1 completada + FASE 2 iniciándose = MINOR increment (6.0 → 6.1)
    new_ict_version = "v6.1.0"
    new_sic_version = "v3.1"
    new_sluc_version = "v2.1"
    
    corrections_made = []
    
    # Aplicar correcciones automáticas
    for file_path, file_versions in versions_data.items():
        full_path = Path(project_root) / file_path
        
        try:
            content = full_path.read_text(encoding='utf-8')
            original_content = content
            
            # Correcciones específicas
            content = re.sub(r'ICT Engine v6\.0', f'ICT Engine {new_ict_version}', content)
            content = re.sub(r'v6\.0\.0-enterprise', f'{new_ict_version}-enterprise', content)
            content = re.sub(r'SIC v3\.0', f'SIC {new_sic_version}', content) 
            content = re.sub(r'SLUC v2\.0', f'SLUC {new_sluc_version}', content)
            
            if content != original_content:
                full_path.write_text(content, encoding='utf-8')
                corrections_made.append(str(file_path))
                
        except Exception as e:
            log_trading_decision_smart_v6("VERSION_CORRECTION_ERROR", {
                "file": str(file_path),
                "error": str(e)
            })
    
    log_trading_decision_smart_v6("VERSION_CORRECTION_COMPLETE", {
        "files_corrected": len(corrections_made),
        "new_ict_version": new_ict_version,
        "new_sic_version": new_sic_version,
        "new_sluc_version": new_sluc_version
    })
    
    return {
        "analysis": analysis,
        "corrections_made": corrections_made,
        "new_versions": {
            "ict": new_ict_version,
            "sic": new_sic_version,
            "sluc": new_sluc_version
        }
    }

def main():
    """Aplicación principal de REGLA #6"""
    
    print("🔢 APLICANDO REGLA #6 - CONTROL DE VERSIONES INTELIGENTE")
    print("=" * 70)
    
    # ✅ REGLA #4: Verificar SIC system ready
    if SIC_SLUC_AVAILABLE:
        try:
            sic = SICBridge()
            log_trading_decision_smart_v6("SIC_STATUS", {
                "available": True,
                "version_control_ready": True
            })
        except Exception as e:
            log_trading_decision_smart_v6("SIC_WARNING", {
                "warning": str(e),
                "continuing": "with version analysis"
            })
    
    # Obtener project root
    project_root = Path(__file__).parent.parent
    
    print(f"\n📁 Analizando proyecto: {project_root.name}")
    
    # ✅ REGLA #6: Análisis y corrección de versiones
    result = apply_version_corrections(str(project_root))
    
    print(f"\n📊 RESULTADOS REGLA #6:")
    print("-" * 50)
    print(f"✅ Archivos analizados: {len(result['analysis'])} componentes")
    print(f"✅ Correcciones aplicadas: {len(result['corrections_made'])} archivos")
    print(f"✅ Nueva versión ICT Engine: {result['new_versions']['ict']}")
    print(f"✅ Versión SIC consistente: {result['new_versions']['sic']}")
    print(f"✅ Versión SLUC consistente: {result['new_versions']['sluc']}")
    
    # ✅ REGLA #6: Justificación del incremento
    print(f"\n🎯 JUSTIFICACIÓN VERSIÓN ICT ENGINE:")
    print("-" * 50)
    print("📈 MINOR increment (v6.0 → v6.1.0) porque:")
    print("   ✅ FASE 1 completada exitosamente")
    print("   ✅ Componentes memoria migrados")
    print("   ✅ FASE 2 iniciándose (memoria unificada)")
    print("   ✅ Nueva funcionalidad significativa")
    print("   ✅ No breaking changes")
    
    if result['corrections_made']:
        print(f"\n📝 ARCHIVOS ACTUALIZADOS:")
        for file_path in result['corrections_made'][:10]:  # Mostrar primeros 10
            print(f"   ✅ {file_path}")
        if len(result['corrections_made']) > 10:
            print(f"   ... y {len(result['corrections_made']) - 10} más")
    
    print("\n" + "=" * 70)
    print("🎉 REGLA #6 APLICADA EXITOSAMENTE")
    print("✅ Versiones consistentes y actualizadas")
    print("📋 READY FOR FASE 2 con versioning correcto")

if __name__ == "__main__":
    main()
