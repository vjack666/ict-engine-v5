#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para corregir ModuleProgress
"""

# Leer el archivo limpio
with open('progress_dashboard_clean.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Correcciones específicas por línea
corrections = {
    255: '            "BOS": ModuleProgress(name="Break of Structure", icon="BOS"),\n',
    256: '            "CHOCH": ModuleProgress(name="Change of Character", icon="CHC"),\n', 
    257: '            "ORDER_BLOCKS": ModuleProgress(name="Order Blocks", icon="OB"),\n',
    258: '            "FVG": ModuleProgress(name="Fair Value Gaps", icon="FVG"),\n',
    259: '            "LIQUIDITY": ModuleProgress(name="Liquidity Analysis", icon="LIQ"),\n',
    260: '            "SILVER_BULLET": ModuleProgress(name="Silver Bullet", icon="SB"),\n',
    261: '            "BREAKER_BLOCKS": ModuleProgress(name="Breaker Blocks", icon="BB"),\n',
    262: '            "SMART_MONEY": ModuleProgress(name="Smart Money Concepts", icon="SMC"),\n',
    263: '            "FRACTAL": ModuleProgress(name="Fractal Analysis", icon="FRAC")\n'
}

# Aplicar correcciones
for line_num, new_content in corrections.items():
    if line_num < len(lines):
        lines[line_num] = new_content

# Escribir archivo corregido
with open('progress_dashboard_fixed.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ progress_dashboard_fixed.py creado con ModuleProgress corregido!")
