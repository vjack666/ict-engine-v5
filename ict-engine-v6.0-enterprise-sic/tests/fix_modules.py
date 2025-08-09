#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir ModuleProgress en progress_dashboard_clean.py
"""

# Leer el archivo
with open('progress_dashboard_clean.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Reemplazos específicos
replacements = [
    ('ModuleProgress("Break of Structure", "ðŸ"ˆ", 0, 0, "", "WAITING")', 'ModuleProgress(name="Break of Structure", icon="BOS")'),
    ('ModuleProgress("Change of Character", "ðŸ"„", 0, 0, "", "WAITING")', 'ModuleProgress(name="Change of Character", icon="CHC")'),
    ('ModuleProgress("Order Blocks", "ðŸ"¦", 0, 0, "", "WAITING")', 'ModuleProgress(name="Order Blocks", icon="OB")'),
    ('ModuleProgress("Fair Value Gaps", "ðŸ'Ž", 0, 0, "", "WAITING")', 'ModuleProgress(name="Fair Value Gaps", icon="FVG")'),
    ('ModuleProgress("Liquidity Analysis", "ðŸ'§", 0, 0, "", "WAITING")', 'ModuleProgress(name="Liquidity Analysis", icon="LIQ")'),
    ('ModuleProgress("Silver Bullet", "ðŸ¥ˆ", 0, 0, "", "WAITING")', 'ModuleProgress(name="Silver Bullet", icon="SB")'),
    ('ModuleProgress("Breaker Blocks", "ðŸ§±", 0, 0, "", "WAITING")', 'ModuleProgress(name="Breaker Blocks", icon="BB")'),
    ('ModuleProgress("Smart Money Concepts", "ðŸ'°", 0, 0, "", "WAITING")', 'ModuleProgress(name="Smart Money Concepts", icon="SMC")'),
    ('ModuleProgress("Fractal Analysis", "ðŸ"®", 0, 0, "", "WAITING")', 'ModuleProgress(name="Fractal Analysis", icon="FRAC")'),
]

# Aplicar reemplazos
for old, new in replacements:
    content = content.replace(old, new)

# Escribir archivo corregido
with open('progress_dashboard_fixed.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Archivo progress_dashboard_fixed.py creado con ModuleProgress corregido!")
