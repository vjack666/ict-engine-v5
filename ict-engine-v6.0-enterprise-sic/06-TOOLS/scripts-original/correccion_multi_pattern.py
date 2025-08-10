#!/usr/bin/env python3
"""
🧹 CORRECCIÓN AUTOMÁTICA REGLA #14 - MULTI PATTERN CONFLUENCE
============================================================

Script para aplicar REGLA #14 y corregir problemas en multi_pattern_confluence_engine.py:
- Corregir dataclass field ordering
- Usar Any para tipos no definidos
- Corregir sintaxis

Fecha: 09 Agosto 2025
"""

import re

def corregir_multi_pattern_confluence():
    """🧹 Aplicar correcciones automáticas según REGLA #14"""
    
    archivo = "core/ict_engine/advanced_patterns/multi_pattern_confluence_engine.py"
    
    print("🧹 REGLA #14: Corrigiendo Multi Pattern Confluence Engine...")
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # 1. ✅ Corregir dataclass - agregar valores por defecto
        print("   ✅ Corrigiendo dataclass field ordering...")
        
        # Patrón simple: agregar = 0 o = "" a campos problemáticos
        patrones_correccion = [
            (r'risk_level: TradeRiskLevel$', 'risk_level: TradeRiskLevel = TradeRiskLevel.MODERATE'),
            (r'risk_reward_ratio: float$', 'risk_reward_ratio: float = 2.0'),
            (r'max_acceptable_loss_pct: float$', 'max_acceptable_loss_pct: float = 1.0'),
            (r'confluence_score: float           # 0.0 - 10.0$', 'confluence_score: float = 0.0           # 0.0 - 10.0'),
            (r'confluence_factors: ConfluenceFactors$', 'confluence_factors: ConfluenceFactors = field(default_factory=ConfluenceFactors)'),
            (r'total_confluences: int$', 'total_confluences: int = 0'),
            (r'critical_confluences: int$', 'critical_confluences: int = 0'),
            (r'win_probability: float           # 0.0 - 1.0$', 'win_probability: float = 0.5           # 0.0 - 1.0'),
            (r'confidence_score: float          # 0.0 - 1.0$', 'confidence_score: float = 0.5          # 0.0 - 1.0'),
            (r'expected_value: float            # Esperanza matemática$', 'expected_value: float = 0.0            # Esperanza matemática'),
            (r'optimal_entry_timeframe: str$', 'optimal_entry_timeframe: str = "M15"'),
            (r'max_wait_time_minutes: int$', 'max_wait_time_minutes: int = 30'),
            (r'invalidation_conditions: List\[str\]$', 'invalidation_conditions: List[str] = field(default_factory=list)'),
            (r'trade_narrative: str$', 'trade_narrative: str = ""'),
            (r'market_context: str$', 'market_context: str = ""'),
            (r'key_levels: Dict\[str, float\]$', 'key_levels: Dict[str, float] = field(default_factory=dict)'),
            (r'timestamp: datetime$', 'timestamp: datetime = field(default_factory=datetime.now)'),
            (r'symbol: str$', 'symbol: str = ""'),
            (r'timeframe: str$', 'timeframe: str = ""'),
            (r'analysis_session_id: str$', 'analysis_session_id: str = ""')
        ]
        
        for patron, reemplazo in patrones_correccion:
            contenido = re.sub(patron, reemplazo, contenido, flags=re.MULTILINE)
        
        # 2. ✅ Agregar import field si falta
        if 'from dataclasses import dataclass, field' not in contenido:
            contenido = contenido.replace(
                'from dataclasses import dataclass',
                'from dataclasses import dataclass, field'
            )
        
        # 3. ✅ Guardar archivo corregido
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print("   ✅ Archivo corregido exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    import os
    os.chdir("c:/Users/v_jac/Desktop/itc engine v5.0/ict-engine-v6.0-enterprise-sic")
    
    if corregir_multi_pattern_confluence():
        print("\n🎯 REGLA #14 APLICADA - Multi Pattern Confluence corregido")
    else:
        print("\n❌ ERROR EN CORRECCIÓN")
