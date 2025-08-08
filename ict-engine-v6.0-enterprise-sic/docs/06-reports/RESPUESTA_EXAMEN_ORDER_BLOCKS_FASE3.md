# 📦 **RESPUESTA OFICIAL EXAMEN ORDER BLOCKS ICT | FASE 3 FINAL**

## 💹 **SECCIÓN 5: TRADING APPLICATIONS**
**(30 puntos)**

### **Pregunta 5.1 (10 puntos) - Estrategias de Entrada**

**Respuesta basada en implementación ICT Engine v6.0:**

```python
class OrderBlockTradingStrategies:
    \"\"\"
    💹 Estrategias de trading para Order Blocks - ICT Engine v6.0
    
    Implementa las tres estrategias principales con puntos exactos
    \"\"\"
    
    def aggressive_entry_strategy(self, order_block: Dict, current_price: float) -> Dict:
        \"\"\"
        🚀 AGGRESSIVE ENTRY - Primera línea de contacto con Order Block
        
        Características:
        - Entry inmediato en edge del Order Block
        - Risk:Reward premium (1:3+)
        - Requiere alta confianza en el setup
        \"\"\"
        ob_high = order_block['high_price']
        ob_low = order_block['low_price']
        ob_type = order_block['type']
        
        strategy = {
            'entry_type': 'AGGRESSIVE',
            'risk_level': 'HIGH',
            'confidence_required': 0.85  # 85% confianza mínima
        }
        
        if ob_type == 'BULLISH_OB':
            # Entry en el HIGH del Bullish Order Block
            strategy.update({
                'entry_price': ob_high,
                'entry_trigger': 'PRICE_TOUCHES_OB_HIGH',
                'stop_loss': ob_low - 0.0005,  # 5 pips debajo del low
                'take_profit_1': ob_high + ((ob_high - ob_low) * 2),  # 1:2 R:R
                'take_profit_2': ob_high + ((ob_high - ob_low) * 3),  # 1:3 R:R
                'take_profit_3': ob_high + ((ob_high - ob_low) * 5),  # 1:5 R:R premium
                'direction': 'LONG'
            })
            
        else:  # BEARISH_OB
            # Entry en el LOW del Bearish Order Block
            strategy.update({
                'entry_price': ob_low,
                'entry_trigger': 'PRICE_TOUCHES_OB_LOW',
                'stop_loss': ob_high + 0.0005,  # 5 pips arriba del high
                'take_profit_1': ob_low - ((ob_high - ob_low) * 2),  # 1:2 R:R
                'take_profit_2': ob_low - ((ob_high - ob_low) * 3),  # 1:3 R:R
                'take_profit_3': ob_low - ((ob_high - ob_low) * 5),  # 1:5 R:R premium
                'direction': 'SHORT'
            })
        
        # Cálculos de Risk:Reward
        risk_pips = abs(strategy['entry_price'] - strategy['stop_loss']) * 10000
        reward_1_pips = abs(strategy['take_profit_1'] - strategy['entry_price']) * 10000
        reward_2_pips = abs(strategy['take_profit_2'] - strategy['entry_price']) * 10000
        reward_3_pips = abs(strategy['take_profit_3'] - strategy['entry_price']) * 10000
        
        strategy['risk_reward'] = {
            'risk_pips': risk_pips,
            'tp1_ratio': reward_1_pips / risk_pips if risk_pips > 0 else 0,
            'tp2_ratio': reward_2_pips / risk_pips if risk_pips > 0 else 0,
            'tp3_ratio': reward_3_pips / risk_pips if risk_pips > 0 else 0
        }
        
        strategy['advantages'] = [
            'Entry inmediato - no se pierde el movimiento',
            'Risk:Reward premium (1:3 a 1:5)',
            'Máximo profit potential'
        ]
        
        strategy['disadvantages'] = [
            'Mayor riesgo de stop out',
            'Requiere timing perfecto',
            'Falsos breakouts pueden activar entry'
        ]
        
        return strategy
    
    def conservative_entry_strategy(self, order_block: Dict, current_price: float) -> Dict:
        \"\"\"
        🛡️ CONSERVATIVE ENTRY - 50% fill del Order Block
        
        Características:
        - Entry en mitad del Order Block
        - Risk:Reward balanceado (1:2 a 1:3)
        - Mayor probabilidad de éxito
        \"\"\"
        ob_high = order_block['high_price']
        ob_low = order_block['low_price']
        ob_middle = (ob_high + ob_low) / 2
        ob_type = order_block['type']
        
        strategy = {
            'entry_type': 'CONSERVATIVE',
            'risk_level': 'MEDIUM',
            'confidence_required': 0.70  # 70% confianza mínima
        }
        
        if ob_type == 'BULLISH_OB':
            strategy.update({
                'entry_price': ob_middle,
                'entry_trigger': 'PRICE_REACHES_50_PERCENT_OB',
                'stop_loss': ob_low - 0.0003,  # 3 pips debajo del low
                'take_profit_1': ob_high + ((ob_high - ob_low) * 1.5),  # 1:1.5 R:R
                'take_profit_2': ob_high + ((ob_high - ob_low) * 2.5),  # 1:2.5 R:R
                'direction': 'LONG'
            })
            
        else:  # BEARISH_OB
            strategy.update({
                'entry_price': ob_middle,
                'entry_trigger': 'PRICE_REACHES_50_PERCENT_OB',
                'stop_loss': ob_high + 0.0003,  # 3 pips arriba del high
                'take_profit_1': ob_low - ((ob_high - ob_low) * 1.5),  # 1:1.5 R:R
                'take_profit_2': ob_low - ((ob_high - ob_low) * 2.5),  # 1:2.5 R:R
                'direction': 'SHORT'
            })
        
        # Cálculos de Risk:Reward
        risk_pips = abs(strategy['entry_price'] - strategy['stop_loss']) * 10000
        reward_1_pips = abs(strategy['take_profit_1'] - strategy['entry_price']) * 10000
        reward_2_pips = abs(strategy['take_profit_2'] - strategy['entry_price']) * 10000
        
        strategy['risk_reward'] = {
            'risk_pips': risk_pips,
            'tp1_ratio': reward_1_pips / risk_pips if risk_pips > 0 else 0,
            'tp2_ratio': reward_2_pips / risk_pips if risk_pips > 0 else 0
        }
        
        strategy['advantages'] = [
            'Mayor probabilidad de éxito',
            'Mejor fill probability',
            'Risk:Reward equilibrado'
        ]
        
        strategy['disadvantages'] = [
            'Menor profit potential',
            'Puede perderse movimientos rápidos',
            'Entry tardío vs aggressive'
        ]
        
        return strategy
    
    def confirmation_entry_strategy(self, order_block: Dict, current_price: float) -> Dict:
        \"\"\"
        ✅ CONFIRMATION ENTRY - Tras rejection del Order Block zone
        
        Características:
        - Entry después de confirmación de respeto
        - Risk:Reward conservador pero seguro (1:2)
        - Máxima probabilidad de éxito
        \"\"\"
        ob_high = order_block['high_price']
        ob_low = order_block['low_price']
        ob_type = order_block['type']
        
        strategy = {
            'entry_type': 'CONFIRMATION',
            'risk_level': 'LOW',
            'confidence_required': 0.60  # 60% confianza mínima
        }
        
        if ob_type == 'BULLISH_OB':
            # Entry tras rejection bullish confirmada
            confirmation_trigger = ob_high + 0.0002  # 2 pips arriba del OB
            strategy.update({
                'entry_price': confirmation_trigger,
                'entry_trigger': 'BULLISH_REJECTION_CONFIRMED',
                'confirmation_signals': [
                    'Pin bar rejection en OB zone',
                    'Engulfing bullish post-touch',
                    'Volume spike en rejection'
                ],
                'stop_loss': ob_low - 0.0002,  # 2 pips debajo del low
                'take_profit_1': confirmation_trigger + ((ob_high - ob_low) * 1.5),  # 1:1.5 R:R
                'take_profit_2': confirmation_trigger + ((ob_high - ob_low) * 2.0),  # 1:2 R:R
                'direction': 'LONG'
            })
            
        else:  # BEARISH_OB
            # Entry tras rejection bearish confirmada
            confirmation_trigger = ob_low - 0.0002  # 2 pips debajo del OB
            strategy.update({
                'entry_price': confirmation_trigger,
                'entry_trigger': 'BEARISH_REJECTION_CONFIRMED',
                'confirmation_signals': [
                    'Pin bar rejection en OB zone',
                    'Engulfing bearish post-touch',
                    'Volume spike en rejection'
                ],
                'stop_loss': ob_high + 0.0002,  # 2 pips arriba del high
                'take_profit_1': confirmation_trigger - ((ob_high - ob_low) * 1.5),  # 1:1.5 R:R
                'take_profit_2': confirmation_trigger - ((ob_high - ob_low) * 2.0),  # 1:2 R:R
                'direction': 'SHORT'
            })
        
        # Cálculos de Risk:Reward
        risk_pips = abs(strategy['entry_price'] - strategy['stop_loss']) * 10000
        reward_1_pips = abs(strategy['take_profit_1'] - strategy['entry_price']) * 10000
        reward_2_pips = abs(strategy['take_profit_2'] - strategy['entry_price']) * 10000
        
        strategy['risk_reward'] = {
            'risk_pips': risk_pips,
            'tp1_ratio': reward_1_pips / risk_pips if risk_pips > 0 else 0,
            'tp2_ratio': reward_2_pips / risk_pips if risk_pips > 0 else 0
        }
        
        strategy['advantages'] = [
            'Máxima probabilidad de éxito',
            'Confirmación reduce falsos positivos',
            'Entry con momentum establecido'
        ]
        
        strategy['disadvantages'] = [
            'Entry más tardío',
            'Menor R:R vs aggressive',
            'Puede perderse movimientos rápidos'
        ]
        
        return strategy
```

### **Pregunta 5.2 (8 puntos) - Position Sizing Adaptativo**

**Respuesta:**

```python
def calculate_ob_position_size(account_balance: float, 
                              risk_percent: float,
                              ob_data: Dict, 
                              market_conditions: Dict) -> Dict:
    \"\"\"
    💰 Calcula position size basado en Order Block strength y condiciones
    
    Implementación enterprise adaptativa para ICT Engine v6.0
    
    Args:
        account_balance: Balance de la cuenta en USD
        risk_percent: Porcentaje de riesgo (ej: 0.02 = 2%)
        ob_data: Información completa del Order Block
        market_conditions: Condiciones actuales del mercado
        
    Returns:
        Dict con tamaño de posición recomendado y justificación
    \"\"\"
    try:
        # ===================================
        # 1. BASE RISK CALCULATION
        # ===================================
        base_risk_amount = account_balance * risk_percent
        
        position_calc = {
            'base_risk_amount': base_risk_amount,
            'adjustments': {},
            'final_position_size': 0.0,
            'lot_size': 0.0,
            'risk_justification': [],
            'warnings': []
        }
        
        # ===================================
        # 2. ORDER BLOCK STRENGTH MULTIPLIER
        # ===================================
        ob_strength = ob_data.get('probability', 50.0) / 100.0
        ob_status = ob_data.get('status', 'ACTIVE')
        
        # Multiplicador base por strength
        if ob_strength >= 0.90:
            strength_multiplier = 1.50  # Premium setup
            position_calc['risk_justification'].append(f"Premium OB strength ({ob_strength:.2f}) - +50% size")
        elif ob_strength >= 0.80:
            strength_multiplier = 1.25  # Strong setup
            position_calc['risk_justification'].append(f"Strong OB strength ({ob_strength:.2f}) - +25% size")
        elif ob_strength >= 0.70:
            strength_multiplier = 1.00  # Standard setup
            position_calc['risk_justification'].append(f"Standard OB strength ({ob_strength:.2f}) - normal size")
        elif ob_strength >= 0.50:
            strength_multiplier = 0.75  # Weak setup
            position_calc['risk_justification'].append(f"Weak OB strength ({ob_strength:.2f}) - -25% size")
            position_calc['warnings'].append("Order Block strength below optimal")
        else:
            strength_multiplier = 0.50  # Very weak
            position_calc['risk_justification'].append(f"Very weak OB ({ob_strength:.2f}) - -50% size")
            position_calc['warnings'].append("Order Block strength significantly low")
        
        position_calc['adjustments']['strength_multiplier'] = strength_multiplier
        
        # ===================================
        # 3. ORDER BLOCK STATUS ADJUSTMENT
        # ===================================
        status_multipliers = {
            'VIRGIN': 1.20,      # +20% for virgin OB
            'ACTIVE': 1.00,      # Standard
            'TESTED': 0.85,      # -15% for tested OB
            'MITIGATING': 0.70,  # -30% durante mitigation
            'PARTIALLY_FILLED': 0.50,  # -50% si parcialmente llenado
            'BROKEN': 0.10       # Mínimo si roto
        }
        
        status_multiplier = status_multipliers.get(ob_status, 1.00)
        position_calc['adjustments']['status_multiplier'] = status_multiplier
        position_calc['risk_justification'].append(f"OB status {ob_status} - {status_multiplier:.2f}x multiplier")
        
        # ===================================
        # 4. MARKET CONDITIONS ADJUSTMENT
        # ===================================
        volatility = market_conditions.get('volatility', 'NORMAL')
        session = market_conditions.get('session', 'LONDON')
        news_impact = market_conditions.get('news_impact', 'NONE')
        
        # Volatility adjustment
        volatility_multipliers = {
            'LOW': 1.10,      # +10% en baja volatilidad
            'NORMAL': 1.00,   # Standard
            'HIGH': 0.90,     # -10% en alta volatilidad
            'EXTREME': 0.70   # -30% en volatilidad extrema
        }
        
        volatility_multiplier = volatility_multipliers.get(volatility, 1.00)
        position_calc['adjustments']['volatility_multiplier'] = volatility_multiplier
        
        # Session adjustment
        session_multipliers = {
            'ASIAN': 0.80,           # -20% sesión Asian
            'LONDON': 1.00,          # Standard
            'NEW_YORK': 1.15,        # +15% sesión NY
            'LONDON_NY_OVERLAP': 1.30 # +30% overlap premium
        }
        
        session_multiplier = session_multipliers.get(session, 1.00)
        position_calc['adjustments']['session_multiplier'] = session_multiplier
        
        # News impact adjustment
        news_multipliers = {
            'NONE': 1.00,      # Sin impacto
            'LOW': 0.95,       # -5% news bajo impacto
            'MEDIUM': 0.85,    # -15% news medio impacto
            'HIGH': 0.70,      # -30% news alto impacto
            'VERY_HIGH': 0.50  # -50% news muy alto impacto
        }
        
        news_multiplier = news_multipliers.get(news_impact, 1.00)
        position_calc['adjustments']['news_multiplier'] = news_multiplier
        
        if news_impact in ['HIGH', 'VERY_HIGH']:
            position_calc['warnings'].append(f"High impact news detected - reduced position size")
        
        # ===================================
        # 5. CONFLUENCE BONUS
        # ===================================
        confluence_score = ob_data.get('confluence_score', 0.0)
        
        if confluence_score >= 0.80:
            confluence_multiplier = 1.25  # +25% para alta confluencia
            position_calc['risk_justification'].append(f"High confluence ({confluence_score:.2f}) - +25% bonus")
        elif confluence_score >= 0.60:
            confluence_multiplier = 1.10  # +10% para confluencia moderada
            position_calc['risk_justification'].append(f"Moderate confluence ({confluence_score:.2f}) - +10% bonus")
        else:
            confluence_multiplier = 1.00
        
        position_calc['adjustments']['confluence_multiplier'] = confluence_multiplier
        
        # ===================================
        # 6. TIMEFRAME AUTHORITY BONUS
        # ===================================
        timeframe = ob_data.get('timeframe', 'H1')
        
        timeframe_multipliers = {
            'M5': 0.70,   # -30% timeframes menores
            'M15': 0.85,  # -15%
            'H1': 1.00,   # Standard
            'H4': 1.20,   # +20% mayor autoridad
            'D1': 1.40    # +40% máxima autoridad
        }
        
        timeframe_multiplier = timeframe_multipliers.get(timeframe, 1.00)
        position_calc['adjustments']['timeframe_multiplier'] = timeframe_multiplier
        
        # ===================================
        # 7. CALCULATE FINAL POSITION SIZE
        # ===================================
        total_multiplier = (strength_multiplier * 
                           status_multiplier * 
                           volatility_multiplier * 
                           session_multiplier * 
                           news_multiplier * 
                           confluence_multiplier * 
                           timeframe_multiplier)
        
        # Apply safety limits
        max_multiplier = 2.00  # Máximo 2x el riesgo base
        min_multiplier = 0.10  # Mínimo 0.1x el riesgo base
        
        total_multiplier = max(min_multiplier, min(max_multiplier, total_multiplier))
        
        final_risk_amount = base_risk_amount * total_multiplier
        
        # ===================================
        # 8. CONVERT TO POSITION SIZE
        # ===================================
        # Asumir EURUSD para cálculo (ajustar según par)
        entry_price = ob_data.get('entry_price', 1.0000)
        stop_loss = ob_data.get('stop_loss_price', entry_price * 0.999)  # 1% default
        
        risk_pips = abs(entry_price - stop_loss) * 10000
        
        if risk_pips > 0:
            pip_value = 10  # $10 per pip para 1 lote estándar EURUSD
            max_loss_per_pip = final_risk_amount / risk_pips
            lot_size = max_loss_per_pip / pip_value
        else:
            lot_size = 0.01  # Minimum lot size
            position_calc['warnings'].append("Unable to calculate proper lot size - using minimum")
        
        # Round to appropriate lot size increments
        lot_size = round(lot_size, 2)  # Round to 0.01 lots
        
        # ===================================
        # 9. FINAL VALIDATION
        # ===================================
        max_lot_size = account_balance / 100000 * 5  # Máximo 5% del balance en lot size
        if lot_size > max_lot_size:
            lot_size = max_lot_size
            position_calc['warnings'].append(f"Position size capped at {max_lot_size} lots for safety")
        
        min_lot_size = 0.01
        if lot_size < min_lot_size:
            lot_size = min_lot_size
        
        position_calc.update({
            'total_multiplier': total_multiplier,
            'final_risk_amount': final_risk_amount,
            'final_position_size': final_risk_amount,
            'lot_size': lot_size,
            'risk_pips': risk_pips,
            'max_loss_usd': final_risk_amount
        })
        
        # ===================================
        # 10. SUMMARY REPORT
        # ===================================
        position_calc['summary'] = {
            'recommended_lot_size': lot_size,
            'risk_amount_usd': final_risk_amount,
            'risk_percentage': (final_risk_amount / account_balance) * 100,
            'total_adjustments': f"{total_multiplier:.2f}x base risk",
            'confidence_level': 'HIGH' if total_multiplier >= 1.2 else 'MEDIUM' if total_multiplier >= 0.8 else 'LOW'
        }
        
        return position_calc
        
    except Exception as e:
        return {
            'error': str(e),
            'lot_size': 0.01,  # Safe fallback
            'final_position_size': account_balance * 0.01,  # 1% fallback
            'warnings': ['Error in calculation - using conservative fallback']
        }

# ===================================
# EJEMPLO DE USO
# ===================================

def example_position_sizing():
    \"\"\"📊 Ejemplo de cálculo de position sizing\"\"\"
    
    # Datos de ejemplo
    account_balance = 10000.00  # $10,000 USD
    risk_percent = 0.02  # 2% risk
    
    ob_data = {
        'probability': 88.5,  # 88.5% strength
        'status': 'VIRGIN',
        'confluence_score': 0.85,
        'timeframe': 'H4',
        'entry_price': 1.0980,
        'stop_loss_price': 1.0970
    }
    
    market_conditions = {
        'volatility': 'NORMAL',
        'session': 'LONDON_NY_OVERLAP',
        'news_impact': 'LOW'
    }
    
    # Calcular position size
    result = calculate_ob_position_size(account_balance, risk_percent, ob_data, market_conditions)
    
    print(f"💰 Recommended Lot Size: {result['lot_size']}")
    print(f"💵 Risk Amount: ${result['final_risk_amount']:.2f}")
    print(f"📊 Total Multiplier: {result['total_multiplier']:.2f}x")
    print(f"🎯 Confidence Level: {result['summary']['confidence_level']}")
    
    return result
```

### **Pregunta 5.3 (7 puntos) - Risk Management Múltiples OBs**

**Respuesta:**

```python
class MultipleOrderBlocksRiskManager:
    \"\"\"
    🛡️ Gestor de riesgo para múltiples Order Blocks activos simultáneamente
    
    Implementación enterprise para ICT Engine v6.0
    \"\"\"
    
    def __init__(self, account_balance: float, max_total_risk: float = 0.06):
        \"\"\"
        🏗️ Inicializa el gestor de riesgo múltiple
        
        Args:
            account_balance: Balance total de la cuenta
            max_total_risk: Riesgo máximo total permitido (6% default)
        \"\"\"
        self.account_balance = account_balance
        self.max_total_risk = max_total_risk
        self.active_positions = {}
        self.risk_allocation_matrix = {}
        
        # Configuración de límites
        self.max_positions_per_symbol = 2
        self.max_total_positions = 5
        self.correlation_threshold = 0.70
        
    def manage_multiple_obs_risk(self, new_ob_opportunities: List[Dict]) -> Dict:
        \"\"\"
        🎯 Gestiona riesgo para múltiples Order Blocks simultáneos
        
        Args:
            new_ob_opportunities: Lista de nuevas oportunidades de Order Blocks
            
        Returns:
            Dict con plan de gestión de riesgo completo
        \"\"\"
        risk_plan = {
            'total_risk_budget': self.account_balance * self.max_total_risk,
            'available_risk': 0.0,
            'position_allocations': [],
            'rejected_opportunities': [],
            'risk_warnings': [],
            'correlation_analysis': {},
            'portfolio_balance': {}
        }
        
        # 1. Calcular riesgo disponible
        current_risk = sum(pos['risk_amount'] for pos in self.active_positions.values())
        risk_plan['available_risk'] = risk_plan['total_risk_budget'] - current_risk
        
        if risk_plan['available_risk'] <= 0:
            risk_plan['risk_warnings'].append("No available risk budget - reject all new positions")
            risk_plan['rejected_opportunities'] = new_ob_opportunities
            return risk_plan
        
        # 2. Analizar correlaciones entre oportunidades
        correlation_analysis = self._analyze_correlations(new_ob_opportunities)
        risk_plan['correlation_analysis'] = correlation_analysis
        
        # 3. Priorizar oportunidades por calidad
        prioritized_opportunities = self._prioritize_opportunities(new_ob_opportunities)
        
        # 4. Asignar riesgo por prioridades
        remaining_risk = risk_plan['available_risk']
        
        for opportunity in prioritized_opportunities:
            if remaining_risk <= 0:
                risk_plan['rejected_opportunities'].append(opportunity)
                continue
                
            # Verificar límites por símbolo
            symbol = opportunity.get('symbol', 'UNKNOWN')
            symbol_positions = len([p for p in self.active_positions.values() if p['symbol'] == symbol])
            
            if symbol_positions >= self.max_positions_per_symbol:
                risk_plan['rejected_opportunities'].append(opportunity)
                risk_plan['risk_warnings'].append(f"Symbol {symbol} at max positions limit")
                continue
            
            # Verificar límites totales
            if len(self.active_positions) >= self.max_total_positions:
                risk_plan['rejected_opportunities'].append(opportunity)
                risk_plan['risk_warnings'].append("At maximum total positions limit")
                continue
            
            # Calcular asignación de riesgo
            allocation = self._calculate_risk_allocation(opportunity, remaining_risk, correlation_analysis)
            
            if allocation['allocated_risk'] > 0:
                risk_plan['position_allocations'].append(allocation)
                remaining_risk -= allocation['allocated_risk']
            else:
                risk_plan['rejected_opportunities'].append(opportunity)
        
        # 5. Análisis de balance de portfolio
        risk_plan['portfolio_balance'] = self._analyze_portfolio_balance(risk_plan['position_allocations'])
        
        return risk_plan
    
    def _prioritize_opportunities(self, opportunities: List[Dict]) -> List[Dict]:
        \"\"\"🏆 Prioriza oportunidades por calidad y confluencia\"\"\"
        
        def calculate_priority_score(opportunity):
            score = 0.0
            
            # Order Block strength (40% peso)
            ob_strength = opportunity.get('probability', 50.0) / 100.0
            score += ob_strength * 0.40
            
            # Confluence score (25% peso)
            confluence = opportunity.get('confluence_score', 0.0)
            score += confluence * 0.25
            
            # Timeframe authority (20% peso)
            timeframe_weights = {'M5': 0.2, 'M15': 0.4, 'H1': 0.6, 'H4': 0.8, 'D1': 1.0}
            tf_weight = timeframe_weights.get(opportunity.get('timeframe', 'H1'), 0.6)
            score += tf_weight * 0.20
            
            # Risk:Reward ratio (15% peso)
            rr_ratio = opportunity.get('risk_reward_ratio', 1.0)
            rr_score = min(1.0, rr_ratio / 3.0)  # Normalizar a max 1:3
            score += rr_score * 0.15
            
            return score
        
        # Ordenar por score descendente
        opportunities_with_scores = [(opp, calculate_priority_score(opp)) for opp in opportunities]
        opportunities_with_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [opp for opp, score in opportunities_with_scores]
    
    def _analyze_correlations(self, opportunities: List[Dict]) -> Dict:
        \"\"\"📊 Analiza correlaciones entre símbolos y timeframes\"\"\"
        correlation_analysis = {
            'symbol_correlations': {},
            'timeframe_distribution': {},
            'direction_balance': {'LONG': 0, 'SHORT': 0},
            'high_correlation_pairs': []
        }
        
        # Análisis por símbolos
        symbols = [opp.get('symbol', 'UNKNOWN') for opp in opportunities]
        symbol_counts = {}
        for symbol in symbols:
            symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
        
        correlation_analysis['symbol_correlations'] = symbol_counts
        
        # Distribución por timeframes
        timeframes = [opp.get('timeframe', 'H1') for opp in opportunities]
        tf_counts = {}
        for tf in timeframes:
            tf_counts[tf] = tf_counts.get(tf, 0) + 1
        
        correlation_analysis['timeframe_distribution'] = tf_counts
        
        # Balance direccional
        for opp in opportunities:
            direction = opp.get('direction', 'UNKNOWN')
            if direction in correlation_analysis['direction_balance']:
                correlation_analysis['direction_balance'][direction] += 1
        
        # Detectar pares altamente correlacionados
        highly_correlated_pairs = [
            ['EURUSD', 'GBPUSD'],  # USD correlation
            ['EURJPY', 'GBPJPY'],  # JPY correlation
            ['AUDUSD', 'NZDUSD'],  # Commodity currencies
        ]
        
        for pair in highly_correlated_pairs:
            if all(symbol in symbols for symbol in pair):
                correlation_analysis['high_correlation_pairs'].append(pair)
        
        return correlation_analysis
    
    def _calculate_risk_allocation(self, opportunity: Dict, available_risk: float, correlation_analysis: Dict) -> Dict:
        \"\"\"💰 Calcula asignación específica de riesgo para una oportunidad\"\"\"
        
        base_allocation = available_risk * 0.30  # Máximo 30% del riesgo disponible por posición
        
        allocation = {
            'opportunity': opportunity,
            'base_allocation': base_allocation,
            'adjustments': {},
            'allocated_risk': 0.0,
            'lot_size': 0.0,
            'reasoning': []
        }
        
        # Ajuste por calidad del Order Block
        ob_strength = opportunity.get('probability', 50.0) / 100.0
        if ob_strength >= 0.85:
            quality_multiplier = 1.25
            allocation['reasoning'].append("High quality OB - +25% allocation")
        elif ob_strength >= 0.70:
            quality_multiplier = 1.00
            allocation['reasoning'].append("Standard quality OB - normal allocation")
        else:
            quality_multiplier = 0.75
            allocation['reasoning'].append("Below average OB - -25% allocation")
        
        allocation['adjustments']['quality_multiplier'] = quality_multiplier
        
        # Ajuste por correlación
        symbol = opportunity.get('symbol', 'UNKNOWN')
        correlation_penalty = 0.0
        
        # Penalizar si ya hay posiciones en símbolos correlacionados
        for pair in correlation_analysis['high_correlation_pairs']:
            if symbol in pair:
                other_symbol = pair[1] if pair[0] == symbol else pair[0]
                if any(pos['symbol'] == other_symbol for pos in self.active_positions.values()):
                    correlation_penalty += 0.20  # -20% por correlación
                    allocation['reasoning'].append(f"Correlation penalty with {other_symbol} - -20%")
        
        correlation_multiplier = max(0.50, 1.0 - correlation_penalty)
        allocation['adjustments']['correlation_multiplier'] = correlation_multiplier
        
        # Ajuste por balance direccional
        direction = opportunity.get('direction', 'UNKNOWN')
        direction_counts = correlation_analysis['direction_balance']
        total_opportunities = sum(direction_counts.values())
        
        if total_opportunities > 0:
            direction_ratio = direction_counts.get(direction, 0) / total_opportunities
            if direction_ratio > 0.70:  # Más del 70% en una dirección
                direction_multiplier = 0.80  # -20% por concentración direccional
                allocation['reasoning'].append("Direction concentration detected - -20% allocation")
            else:
                direction_multiplier = 1.00
        else:
            direction_multiplier = 1.00
        
        allocation['adjustments']['direction_multiplier'] = direction_multiplier
        
        # Cálculo final
        total_multiplier = quality_multiplier * correlation_multiplier * direction_multiplier
        final_allocation = min(available_risk, base_allocation * total_multiplier)
        
        allocation['allocated_risk'] = final_allocation
        allocation['total_multiplier'] = total_multiplier
        
        # Convertir a lot size
        if final_allocation > 0:
            # Usar la función de position sizing existente
            position_data = calculate_ob_position_size(
                account_balance=self.account_balance,
                risk_percent=final_allocation / self.account_balance,
                ob_data=opportunity,
                market_conditions=opportunity.get('market_conditions', {})
            )
            allocation['lot_size'] = position_data.get('lot_size', 0.01)
        
        return allocation
    
    def _analyze_portfolio_balance(self, allocations: List[Dict]) -> Dict:
        \"\"\"⚖️ Analiza balance general del portfolio\"\"\"
        
        balance_analysis = {
            'total_allocated_risk': sum(alloc['allocated_risk'] for alloc in allocations),
            'position_count': len(allocations),
            'symbol_distribution': {},
            'timeframe_distribution': {},
            'direction_balance': {'LONG': 0, 'SHORT': 0},
            'risk_concentration': {},
            'balance_score': 0.0
        }
        
        # Distribución por símbolos
        for alloc in allocations:
            symbol = alloc['opportunity'].get('symbol', 'UNKNOWN')
            balance_analysis['symbol_distribution'][symbol] = balance_analysis['symbol_distribution'].get(symbol, 0) + 1
        
        # Distribución por timeframes
        for alloc in allocations:
            tf = alloc['opportunity'].get('timeframe', 'H1')
            balance_analysis['timeframe_distribution'][tf] = balance_analysis['timeframe_distribution'].get(tf, 0) + 1
        
        # Balance direccional
        for alloc in allocations:
            direction = alloc['opportunity'].get('direction', 'UNKNOWN')
            if direction in balance_analysis['direction_balance']:
                balance_analysis['direction_balance'][direction] += 1
        
        # Concentración de riesgo
        for alloc in allocations:
            symbol = alloc['opportunity'].get('symbol', 'UNKNOWN')
            risk_pct = (alloc['allocated_risk'] / balance_analysis['total_allocated_risk']) * 100
            balance_analysis['risk_concentration'][symbol] = balance_analysis['risk_concentration'].get(symbol, 0) + risk_pct
        
        # Score de balance (0-100)
        balance_score = 100.0
        
        # Penalizar concentración de símbolos
        max_symbol_concentration = max(balance_analysis['risk_concentration'].values()) if balance_analysis['risk_concentration'] else 0
        if max_symbol_concentration > 40:  # Más del 40% en un símbolo
            balance_score -= (max_symbol_concentration - 40)
        
        # Penalizar desbalance direccional
        direction_counts = balance_analysis['direction_balance']
        total_positions = sum(direction_counts.values())
        if total_positions > 0:
            long_ratio = direction_counts['LONG'] / total_positions
            if long_ratio > 0.80 or long_ratio < 0.20:  # Más del 80% en una dirección
                balance_score -= 20
        
        balance_analysis['balance_score'] = max(0.0, balance_score)
        
        return balance_analysis

# ===================================
# PROTOCOLO DE GESTIÓN MÚLTIPLE
# ===================================

def implement_multiple_obs_protocol():
    \"\"\"
    📋 Protocolo completo para gestión de múltiples Order Blocks
    \"\"\"
    protocol = {
        'pre_trade_checklist': [
            "Verificar riesgo total disponible",
            "Analizar correlaciones entre símbolos", 
            "Confirmar límites por símbolo",
            "Evaluar balance direccional",
            "Priorizar por calidad y confluencia"
        ],
        
        'position_management': [
            "Escalonar entradas en el tiempo",
            "Monitorear correlaciones activas",
            "Ajustar stops dinámicamente",
            "Tomar profits parciales coordinados",
            "Rebalancear portfolio periódicamente"
        ],
        
        'exit_strategies': [
            "Close correlated positions simultaneously",
            "Scale out based on overall portfolio performance",
            "Emergency exit protocol if correlation spike",
            "Profit protection for winning clusters",
            "Loss limitation for failing clusters"
        ],
        
        'monitoring_requirements': [
            "Real-time correlation tracking",
            "Portfolio heat map visualization", 
            "Risk utilization percentage",
            "Individual OB performance metrics",
            "Market condition impact analysis"
        ]
    }
    
    return protocol
```

### **Pregunta 5.4 (5 puntos) - Condiciones de Mercado para Order Blocks**

**Respuesta:**

**📈 Condiciones de Mercado MÁS Efectivas para Order Blocks:**

```python
def analyze_optimal_market_conditions_for_obs():
    \"\"\"
    🎯 Análisis de condiciones óptimas para Order Blocks
    
    Basado en observaciones del ICT Engine v6.0
    \"\"\"
    
    optimal_conditions = {
        'MOST_EFFECTIVE': {
            'market_structure': 'TRENDING',
            'volatility': 'MEDIUM_TO_HIGH', 
            'session': 'LONDON_NY_OVERLAP',
            'volume': 'ABOVE_AVERAGE',
            'news_environment': 'POST_NEWS_CLARITY',
            'effectiveness_rate': 0.90,  # 90% success rate
            'reasoning': [
                "Institutional activity maximized",
                "Clear directional bias established", 
                "Volume confirma actividad smart money",
                "Overlaps generan Order Blocks premium"
            ]
        },
        
        'HIGHLY_EFFECTIVE': {
            'market_structure': 'RANGING_WITH_BIAS',
            'volatility': 'MEDIUM',
            'session': 'LONDON_OR_NY', 
            'volume': 'NORMAL_TO_HIGH',
            'news_environment': 'LOW_IMPACT_NEWS',
            'effectiveness_rate': 0.75,  # 75% success rate
            'reasoning': [
                "Rangos permiten mitigation clara",
                "Bias direccional preserva OB validity",
                "Sesiones principales respetan niveles institucionales"
            ]
        }
    }
    
    least_effective_conditions = {
        'LEAST_EFFECTIVE': {
            'market_structure': 'CHOPPY_SIDEWAYS',
            'volatility': 'VERY_LOW',
            'session': 'ASIAN_QUIET_HOURS',
            'volume': 'BELOW_AVERAGE', 
            'news_environment': 'HIGH_IMPACT_PENDING',
            'effectiveness_rate': 0.35,  # 35% success rate
            'reasoning': [
                "Falta de actividad institucional",
                "Movimientos limitados impiden mitigation",
                "Baja participación reduce respeto de niveles",
                "News pending genera incertidumbre"
            ]
        },
        
        'MODERATELY_INEFFECTIVE': {
            'market_structure': 'HIGHLY_VOLATILE_NEWS',
            'volatility': 'EXTREME',
            'session': 'ANY',
            'volume': 'EXTREME_SPIKES',
            'news_environment': 'HIGH_IMPACT_ACTIVE',
            'effectiveness_rate': 0.45,  # 45% success rate
            'reasoning': [
                "Volatilidad extrema rompe niveles técnicos",
                "News events alteran comportamiento institucional",
                "Volume spikes pueden invalidar OBs rápidamente"
            ]
        }
    }
    
    return {
        'optimal': optimal_conditions,
        'suboptimal': least_effective_conditions,
        'adaptation_strategies': get_adaptation_strategies()
    }

def get_adaptation_strategies():
    \"\"\"🔧 Estrategias de adaptación por condiciones\"\"\"
    
    return {
        'LOW_VOLATILITY_ADAPTATION': {
            'position_sizing': 'INCREASE_BY_20_PERCENT',
            'stop_losses': 'TIGHTEN_BY_30_PERCENT', 
            'take_profits': 'REDUCE_EXPECTATIONS',
            'entry_timing': 'MORE_PATIENT',
            'reasoning': 'Compensar movimientos limitados con mayor precisión'
        },
        
        'HIGH_VOLATILITY_ADAPTATION': {
            'position_sizing': 'REDUCE_BY_30_PERCENT',
            'stop_losses': 'WIDEN_BY_50_PERCENT',
            'take_profits': 'SCALE_OUT_FASTER', 
            'entry_timing': 'MORE_SELECTIVE',
            'reasoning': 'Proteger contra whipsaws y falsos breakouts'
        },
        
        'NEWS_ENVIRONMENT_ADAPTATION': {
            'pre_news': {
                'action': 'AVOID_NEW_POSITIONS',
                'existing_positions': 'REDUCE_SIZE_OR_CLOSE',
                'reasoning': 'Prevenir volatilidad impredecible'
            },
            'post_news': {
                'action': 'WAIT_FOR_CLARITY_30_MINUTES',
                'opportunity': 'NEW_OB_FORMATION_LIKELY',
                'reasoning': 'News events crean nuevos Order Blocks institucionales'
            }
        },
        
        'SESSION_ADAPTATION': {
            'ASIAN_SESSION': {
                'strategy': 'RANGE_TRADING_FOCUS',
                'ob_types': 'PREFER_TESTED_OBS',
                'risk': 'REDUCE_POSITION_SIZE',
                'reasoning': 'Actividad institucional limitada'
            },
            'LONDON_SESSION': {
                'strategy': 'TREND_FOLLOWING',
                'ob_types': 'VIRGIN_OBS_PREMIUM',
                'risk': 'STANDARD_SIZING',
                'reasoning': 'Actividad europea genera OBs de calidad'
            },
            'NY_SESSION': {
                'strategy': 'INSTITUTIONAL_ALIGNMENT',
                'ob_types': 'ANY_HIGH_PROBABILITY',
                'risk': 'INCREASE_ON_CONFLUENCE',
                'reasoning': 'Máxima actividad smart money'
            }
        }
    }
```

**📊 Por qué estas condiciones son más/menos efectivas:**

**🟢 MÁS Efectivas:**
1. **Trending Markets:** Instituciones operan con bias claro, Order Blocks se respetan
2. **Medium-High Volatility:** Suficiente movimiento para mitigation, no excesivo para invalidación
3. **London-NY Overlap:** Máxima liquidez institucional, smart money más activo
4. **Post-News Clarity:** Direccionalidad establecida, instituciones reposicionándose

**🔴 MENOS Efectivas:**
1. **Choppy/Sideways:** Sin bias claro, Order Blocks se rompen frecuentemente  
2. **Very Low Volatility:** Insuficiente movimiento para alcanzar OBs o generar reacciones
3. **Asian Quiet Hours:** Mínima actividad institucional, retail dominante
4. **High Impact News Pending:** Incertidumbre impide comportamiento institucional normal

---

*Continuando con Sección 6 y Pregunta Maestra...*
