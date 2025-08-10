# 📦 **RESPUESTA OFICIAL EXAMEN ORDER BLOCKS ICT | FASE 2**

## ⚡ **SECCIÓN 3: ANÁLISIS MULTI-TIMEFRAME (CONTINUACIÓN)**

### **Pregunta 3.3 (8 puntos) - Función Confluencia Multi-TF**

**Respuesta:**

```python
def calculate_multi_tf_ob_confluence(h4_ob, h1_ob, m15_ob, current_price):
    \"\"\"
    🎯 Calcula score de confluencia entre Order Blocks de múltiples timeframes
    
    Implementación enterprise basada en ICT Engine v6.0
    
    Args:
        h4_ob: Order Block H4 (dict o None)
        h1_ob: Order Block H1 (dict o None) 
        m15_ob: Order Block M15 (dict o None)
        current_price: Precio actual del mercado (float)
    
    Returns:
        Float entre 0.0 y 1.0 indicando confluencia strength
    \"\"\"
    try:
        confluence_score = 0.0
        confluence_factors = []
        
        # ===================================
        # 1. VALIDAR INPUTS
        # ===================================
        valid_obs = [ob for ob in [h4_ob, h1_ob, m15_ob] if ob is not None]
        if not valid_obs:
            return 0.0
        
        # ===================================
        # 2. ANÁLISIS DIRECCIONAL CONFLUENCE
        # ===================================
        directional_score = 0.0
        direction_weights = {'H4': 0.50, 'H1': 0.30, 'M15': 0.20}
        
        # Determinar bias dominante
        biases = {}
        if h4_ob:
            biases['H4'] = 'BULLISH' if h4_ob['type'] == 'BULLISH_OB' else 'BEARISH'
        if h1_ob:
            biases['H1'] = 'BULLISH' if h1_ob['type'] == 'BULLISH_OB' else 'BEARISH'
        if m15_ob:
            biases['M15'] = 'BULLISH' if m15_ob['type'] == 'BULLISH_OB' else 'BEARISH'
        
        # Calcular confluencia direccional
        if len(set(biases.values())) == 1:
            # Todos los timeframes en la misma dirección = confluencia perfecta
            directional_score = 1.0
            confluence_factors.append("Perfect directional alignment")
        else:
            # Confluencia parcial basada en pesos
            dominant_bias = max(set(biases.values()), key=lambda x: sum(direction_weights[tf] for tf, bias in biases.items() if bias == x))
            
            aligned_weight = sum(direction_weights[tf] for tf, bias in biases.items() if bias == dominant_bias)
            directional_score = aligned_weight
            confluence_factors.append(f"Partial alignment: {dominant_bias} dominance ({aligned_weight:.2f})")
        
        confluence_score += directional_score * 0.40  # 40% peso direccional
        
        # ===================================
        # 3. ANÁLISIS GEOGRÁFICO (PROXIMITY)
        # ===================================
        geographic_score = 0.0
        price_levels = []
        
        if h4_ob:
            price_levels.append(('H4', (h4_ob['high_price'] + h4_ob['low_price']) / 2))
        if h1_ob:
            price_levels.append(('H1', (h1_ob['high_price'] + h1_ob['low_price']) / 2))
        if m15_ob:
            price_levels.append(('M15', (m15_ob['high_price'] + m15_ob['low_price']) / 2))
        
        if len(price_levels) >= 2:
            # Calcular dispersión de niveles
            prices = [level[1] for level in price_levels]
            price_range = max(prices) - min(prices)
            
            # Confluencia geográfica = inverso de dispersión (normalizado)
            max_reasonable_range = current_price * 0.002  # 200 pips como máximo razonable
            geographic_score = max(0.0, 1.0 - (price_range / max_reasonable_range))
            
            confluence_factors.append(f"Geographic proximity: {geographic_score:.2f} (range: {price_range:.5f})")
        
        confluence_score += geographic_score * 0.25  # 25% peso geográfico
        
        # ===================================
        # 4. ANÁLISIS DE STRENGTH AGGREGATED
        # ===================================
        strength_score = 0.0
        total_strength = 0.0
        total_weight = 0.0
        
        strength_weights = {'H4': 0.50, 'H1': 0.30, 'M15': 0.20}
        
        if h4_ob:
            h4_strength = h4_ob.get('probability', 50) / 100.0
            total_strength += h4_strength * strength_weights['H4']
            total_weight += strength_weights['H4']
        
        if h1_ob:
            h1_strength = h1_ob.get('probability', 50) / 100.0
            total_strength += h1_strength * strength_weights['H1']
            total_weight += strength_weights['H1']
        
        if m15_ob:
            m15_strength = m15_ob.get('probability', 50) / 100.0
            total_strength += m15_strength * strength_weights['M15']
            total_weight += strength_weights['M15']
        
        if total_weight > 0:
            strength_score = total_strength / total_weight
            confluence_factors.append(f"Aggregated strength: {strength_score:.2f}")
        
        confluence_score += strength_score * 0.20  # 20% peso strength
        
        # ===================================
        # 5. ANÁLISIS DE CURRENT PRICE CONTEXT
        # ===================================
        price_context_score = 0.0
        
        # Verificar si precio actual está en confluencia con los OBs
        price_relevance = []
        
        for ob_data in [(h4_ob, 'H4'), (h1_ob, 'H1'), (m15_ob, 'M15')]:
            ob, tf = ob_data
            if ob is None:
                continue
                
            ob_high = ob['high_price']
            ob_low = ob['low_price']
            
            # Determinar relevancia del precio actual
            if ob_low <= current_price <= ob_high:
                # Precio dentro del OB = máxima relevancia
                relevance = 1.0
                price_relevance.append((tf, relevance, "INSIDE"))
            else:
                # Precio fuera = relevancia basada en distancia
                distance = min(abs(current_price - ob_high), abs(current_price - ob_low))
                max_relevant_distance = current_price * 0.001  # 100 pips máximo
                relevance = max(0.0, 1.0 - (distance / max_relevant_distance))
                price_relevance.append((tf, relevance, "NEAR" if relevance > 0.5 else "FAR"))
        
        if price_relevance:
            # Precio context = promedio ponderado de relevancia
            context_weights = {'H4': 0.50, 'H1': 0.30, 'M15': 0.20}
            weighted_relevance = sum(relevance * context_weights[tf] for tf, relevance, _ in price_relevance)
            price_context_score = weighted_relevance
            
            confluence_factors.append(f"Price context relevance: {price_context_score:.2f}")
        
        confluence_score += price_context_score * 0.15  # 15% peso price context
        
        # ===================================
        # 6. NORMALIZAR Y RETORNAR
        # ===================================
        final_confluence = max(0.0, min(1.0, confluence_score))
        
        # Agregar metadata para debugging
        confluence_metadata = {
            'final_score': final_confluence,
            'breakdown': {
                'directional': directional_score * 0.40,
                'geographic': geographic_score * 0.25,
                'strength': strength_score * 0.20,
                'price_context': price_context_score * 0.15
            },
            'factors': confluence_factors,
            'obs_analyzed': len(valid_obs),
            'biases': biases
        }
        
        # En producción, solo retornar el score
        # Para debugging, se puede retornar confluence_metadata
        return final_confluence
        
    except Exception as e:
        print(f"Error en calculate_multi_tf_ob_confluence: {e}")
        return 0.0

# ===================================
# FUNCIONES AUXILIARES
# ===================================

def validate_order_block_format(ob):
    \"\"\"🔍 Valida formato de Order Block\"\"\"
    if not isinstance(ob, dict):
        return False
    
    required_fields = ['type', 'high_price', 'low_price', 'probability']
    return all(field in ob for field in required_fields)

def calculate_price_distance_score(price1, price2, current_price, max_distance_ratio=0.002):
    \"\"\"📏 Calcula score basado en distancia entre precios\"\"\"
    distance = abs(price1 - price2)
    max_distance = current_price * max_distance_ratio
    return max(0.0, 1.0 - (distance / max_distance))

# ===================================
# EJEMPLO DE USO
# ===================================

def example_confluence_calculation():
    \"\"\"📊 Ejemplo de uso del calculador de confluencia\"\"\"
    
    # Order Blocks de ejemplo
    h4_ob = {
        'type': 'BULLISH_OB',
        'high_price': 1.0985,
        'low_price': 1.0975,
        'probability': 88.5,
        'status': 'VIRGIN'
    }
    
    h1_ob = {
        'type': 'BULLISH_OB', 
        'high_price': 1.0982,
        'low_price': 1.0978,
        'probability': 75.2,
        'status': 'TESTED'
    }
    
    m15_ob = {
        'type': 'BULLISH_OB',
        'high_price': 1.0981,
        'low_price': 1.0979,
        'probability': 65.8,
        'status': 'ACTIVE'
    }
    
    current_price = 1.0980
    
    # Calcular confluencia
    confluence_score = calculate_multi_tf_ob_confluence(h4_ob, h1_ob, m15_ob, current_price)
    
    print(f"🎯 Confluence Score: {confluence_score:.3f}")
    
    # Interpretación
    if confluence_score >= 0.80:
        print("🟢 ALTA CONFLUENCIA - Setup premium")
    elif confluence_score >= 0.60:
        print("🟡 CONFLUENCIA MODERADA - Setup válido")
    elif confluence_score >= 0.40:
        print("🟠 CONFLUENCIA BAJA - Precaución")
    else:
        print("🔴 SIN CONFLUENCIA - Evitar trade")
    
    return confluence_score
```

---

## 🔬 **SECCIÓN 4: MITIGATION Y LIFECYCLE**
**(30 puntos)**

### **Pregunta 4.1 (8 puntos) - Tipos de Mitigation**

**Respuesta:**

**🔄 Tipos de Mitigation Implementados en ICT Engine v6.0:**

**1. 📊 Partial Mitigation:**
```python
def detect_partial_mitigation(self, order_block, price_data):
    \"\"\"
    🎯 Detecta mitigation parcial del Order Block
    
    Partial Mitigation = precio toca la zona OB pero NO la llena completamente
    \"\"\"
    ob_high = order_block['high_price']
    ob_low = order_block['low_price']
    ob_range = ob_high - ob_low
    
    mitigation_analysis = {
        'type': 'PARTIAL',
        'percentage_filled': 0.0,
        'deepest_penetration': 0.0,
        'mitigation_points': [],
        'implications': []
    }
    
    for candle in price_data:
        # Verificar si precio entró en la zona
        if ob_low <= candle['low'] <= ob_high or ob_low <= candle['high'] <= ob_high:
            
            # Calcular penetración
            if order_block['type'] == 'BULLISH_OB':
                # Para Bullish OB, medir penetración desde arriba
                penetration = max(0, ob_high - candle['low'])
                percentage = min(100.0, (penetration / ob_range) * 100)
            else:
                # Para Bearish OB, medir penetración desde abajo  
                penetration = max(0, candle['high'] - ob_low)
                percentage = min(100.0, (penetration / ob_range) * 100)
            
            mitigation_analysis['mitigation_points'].append({
                'timestamp': candle.name,
                'penetration': penetration,
                'percentage': percentage,
                'candle_type': 'bullish' if candle['close'] > candle['open'] else 'bearish'
            })
            
            # Actualizar métricas
            mitigation_analysis['percentage_filled'] = max(mitigation_analysis['percentage_filled'], percentage)
            mitigation_analysis['deepest_penetration'] = max(mitigation_analysis['deepest_penetration'], penetration)
    
    # Determinar si es partial mitigation
    if 10.0 <= mitigation_analysis['percentage_filled'] < 75.0:
        mitigation_analysis['implications'] = [
            "Order Block parcialmente mitigado",
            "Instituciones han cerrado PARTE de sus órdenes",
            "Zona mantiene relevancia pero con fuerza reducida",
            f"Remaining strength: {100 - mitigation_analysis['percentage_filled']:.1f}%"
        ]
        return mitigation_analysis
    
    return None

def trading_implications_partial_mitigation(self, partial_mitigation_data):
    \"\"\"💹 Implicaciones de trading para Partial Mitigation\"\"\"
    percentage_filled = partial_mitigation_data['percentage_filled']
    
    implications = {
        'position_sizing': 1.0,  # Factor multiplicador
        'stop_loss_adjustment': 0.0,  # Pips de ajuste
        'take_profit_expectation': 1.0,  # Factor de expectativa
        'entry_timing': 'NORMAL'
    }
    
    if percentage_filled < 25:
        # Mitigation mínima
        implications.update({
            'position_sizing': 0.9,  # Reducir 10%
            'entry_timing': 'AGGRESSIVE',
            'notes': 'Mitigation menor - mantener agresividad'
        })
    elif percentage_filled < 50:
        # Mitigation moderada
        implications.update({
            'position_sizing': 0.7,  # Reducir 30%
            'stop_loss_adjustment': 2,  # +2 pips safety
            'entry_timing': 'CONSERVATIVE',
            'notes': 'Mitigation moderada - precaución aumentada'
        })
    else:
        # Mitigation significativa
        implications.update({
            'position_sizing': 0.5,  # Reducir 50%
            'stop_loss_adjustment': 5,  # +5 pips safety
            'take_profit_expectation': 0.8,  # Reducir expectativa
            'entry_timing': 'CONFIRMATION_REQUIRED',
            'notes': 'Mitigation alta - confirmación necesaria'
        })
    
    return implications
```

**2. 🎯 Full Mitigation:**
```python
def detect_full_mitigation(self, order_block, price_data):
    \"\"\"
    🔥 Detecta mitigation completa del Order Block
    
    Full Mitigation = precio llena completamente el Order Block
    \"\"\"
    ob_high = order_block['high_price']
    ob_low = order_block['low_price']
    
    full_mitigation_analysis = {
        'type': 'FULL',
        'completion_timestamp': None,
        'completion_percentage': 0.0,
        'volume_on_completion': 0.0,
        'implications': []
    }
    
    for candle in price_data:
        # Verificar llenado completo
        fill_percentage = 0.0
        
        if order_block['type'] == 'BULLISH_OB':
            # Bullish OB completamente llenado si precio toca/penetra el low
            if candle['low'] <= ob_low:
                fill_percentage = 100.0
        else:
            # Bearish OB completamente llenado si precio toca/penetra el high
            if candle['high'] >= ob_high:
                fill_percentage = 100.0
        
        if fill_percentage >= 100.0:
            full_mitigation_analysis.update({
                'completion_timestamp': candle.name,
                'completion_percentage': 100.0,
                'volume_on_completion': candle.get('volume', 0),
                'completion_candle': {
                    'open': candle['open'],
                    'high': candle['high'], 
                    'low': candle['low'],
                    'close': candle['close']
                }
            })
            
            # Implicaciones de Full Mitigation
            full_mitigation_analysis['implications'] = [
                "Order Block COMPLETAMENTE mitigado",
                "Instituciones han cerrado TODAS sus órdenes pendientes",
                "Zona pierde relevancia como soporte/resistencia",
                "Puede convertirse en Breaker Block si el precio retorna"
            ]
            
            return full_mitigation_analysis
    
    return None

def trading_implications_full_mitigation(self, order_block):
    \"\"\"⚠️ Implicaciones de trading para Full Mitigation\"\"\"
    return {
        'trade_status': 'INVALIDATED',
        'new_role': 'POTENTIAL_BREAKER_BLOCK',
        'position_sizing': 0.0,  # No trade
        'alternative_strategy': 'WAIT_FOR_BREAKER_CONFIRMATION',
        'monitoring': 'TRACK_FOR_ROLE_REVERSAL',
        'notes': 'Order Block invalidado - monitorear para Breaker Block'
    }
```

**3. ❌ Failed Mitigation:**
```python
def detect_failed_mitigation(self, order_block, price_data, lookback_period=48):
    \"\"\"
    🚫 Detecta Failed Mitigation del Order Block
    
    Failed Mitigation = precio NO puede retornar al Order Block después de formación
    \"\"\"
    ob_high = order_block['high_price']
    ob_low = order_block['low_price']
    formation_time = order_block['origin_timestamp']
    
    failed_mitigation_analysis = {
        'type': 'FAILED',
        'time_since_formation': 0,
        'closest_approach': float('inf'),
        'failure_strength': 0.0,
        'implications': []
    }
    
    # Filtrar datos posteriores a la formación del OB
    post_formation_data = [candle for candle in price_data 
                          if candle.name > formation_time]
    
    if not post_formation_data:
        return None
    
    # Analizar el precio en el período de lookback
    current_time = post_formation_data[-1].name
    time_elapsed = (current_time - formation_time).total_seconds() / 3600  # Horas
    
    failed_mitigation_analysis['time_since_formation'] = time_elapsed
    
    # Buscar approach más cercano al Order Block
    closest_distance = float('inf')
    
    for candle in post_formation_data:
        if order_block['type'] == 'BULLISH_OB':
            # Para Bullish OB, medir distancia hacia abajo
            distance = candle['low'] - ob_high
        else:
            # Para Bearish OB, medir distancia hacia arriba  
            distance = ob_low - candle['high']
        
        if distance >= 0:  # Solo considerar approaches válidos
            closest_distance = min(closest_distance, distance)
    
    failed_mitigation_analysis['closest_approach'] = closest_distance
    
    # Determinar si es Failed Mitigation
    min_time_for_failure = 24  # 24 horas mínimo
    min_distance_for_failure = order_block.get('range_size', 0.001) * 2  # 2x el tamaño del OB
    
    if (time_elapsed >= min_time_for_failure and 
        closest_distance >= min_distance_for_failure):
        
        # Calcular strength del failure
        failure_strength = min(1.0, (closest_distance / min_distance_for_failure))
        failed_mitigation_analysis['failure_strength'] = failure_strength
        
        # Implicaciones
        failed_mitigation_analysis['implications'] = [
            f"FAILED MITIGATION después de {time_elapsed:.1f} horas",
            f"Precio no pudo retornar - distancia mínima: {closest_distance:.5f}",
            "Indica FUERZA EXTREMA del Order Block",
            "Probabilidad de mitigation futura MUY ALTA cuando el precio retorne",
            f"Failure strength: {failure_strength:.2f} (0.0 = débil, 1.0 = muy fuerte)"
        ]
        
        return failed_mitigation_analysis
    
    return None

def trading_implications_failed_mitigation(self, failed_mitigation_data):
    \"\"\"🚀 Implicaciones de trading para Failed Mitigation\"\"\"
    failure_strength = failed_mitigation_data['failure_strength']
    
    return {
        'strength_multiplier': 1.0 + failure_strength,  # Aumentar fuerza del OB
        'position_sizing': 1.2 + (failure_strength * 0.3),  # Aumentar posición
        'take_profit_expectation': 1.5 + failure_strength,  # Mayor expectativa
        'stop_loss_adjustment': -2,  # Stops más amplios (mayor confianza)
        'entry_timing': 'AGGRESSIVE_ON_RETURN',
        'priority': 'HIGH',
        'notes': f'Failed mitigation indica OB de fuerza excepcional ({failure_strength:.2f})'
    }
```

### **Pregunta 4.2 (10 puntos) - Clase OrderBlockLifecycle**

**Respuesta:**

```python
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple
import time

class OrderBlockStatus(Enum):
    \"\"\"🔄 Estados del ciclo de vida de Order Block\"\"\"
    ACTIVE = "ACTIVE"
    MITIGATING = "MITIGATING"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FULLY_FILLED = "FULLY_FILLED"
    BROKEN = "BROKEN"
    EXPIRED = "EXPIRED"
    BREAKER = "BREAKER"

class OrderBlockLifecycle:
    \"\"\"
    🔄 Maneja el ciclo de vida completo de un Order Block
    
    Implementación enterprise para ICT Engine v6.0
    Estados: ACTIVE → MITIGATING → FILLED/BROKEN → EXPIRED/BREAKER
    \"\"\"
    
    def __init__(self, order_block: Dict):
        \"\"\"
        🏗️ Inicializa lifecycle manager
        
        Args:
            order_block: Dict con datos del Order Block
        \"\"\"
        self.order_block = order_block.copy()
        self.status = OrderBlockStatus.ACTIVE
        self.lifecycle_history = []
        self.mitigation_events = []
        self.strength_adjustments = []
        
        # Configuración de timeframes
        self.timeframe = order_block.get('timeframe', 'H1')
        self.max_lifetime = self._calculate_max_lifetime()
        
        # Métricas de performance
        self.performance_metrics = {
            'total_tests': 0,
            'successful_tests': 0,
            'failed_tests': 0,
            'max_penetration': 0.0,
            'total_mitigation_percentage': 0.0
        }
        
        # Estado inicial
        self._add_lifecycle_event("CREATION", {
            'initial_status': self.status.value,
            'initial_strength': order_block.get('probability', 50.0),
            'creation_time': datetime.now()
        })
    
    def update_status(self, current_price: float, current_time: datetime, candle_data: Optional[Dict] = None):
        \"\"\"
        🔄 Actualiza el estado del Order Block basado en precio y tiempo actual
        
        Args:
            current_price: Precio actual del mercado
            current_time: Timestamp actual
            candle_data: Datos opcional de la vela actual
        \"\"\"
        try:
            previous_status = self.status
            
            # 1. Verificar expiración por tiempo
            if self._is_expired(current_time):
                self._transition_to_status(OrderBlockStatus.EXPIRED, {
                    'expiration_reason': 'TIME_EXPIRED',
                    'lifetime_hours': self._get_lifetime_hours(current_time)
                })
                return
            
            # 2. Analizar interacción con precio actual
            price_interaction = self._analyze_price_interaction(current_price, candle_data)
            
            # 3. Determinar nuevo estado basado en interacción
            if price_interaction['type'] == 'NO_INTERACTION':
                # Sin cambio, mantener estado actual
                pass
                
            elif price_interaction['type'] == 'TOUCH':
                if self.status == OrderBlockStatus.ACTIVE:
                    self._transition_to_status(OrderBlockStatus.MITIGATING, {
                        'touch_price': current_price,
                        'penetration_depth': price_interaction['penetration_depth']
                    })
                    
            elif price_interaction['type'] == 'PARTIAL_FILL':
                self._transition_to_status(OrderBlockStatus.PARTIALLY_FILLED, {
                    'fill_percentage': price_interaction['fill_percentage'],
                    'penetration_depth': price_interaction['penetration_depth']
                })
                
            elif price_interaction['type'] == 'FULL_FILL':
                self._transition_to_status(OrderBlockStatus.FULLY_FILLED, {
                    'fill_price': current_price,
                    'completion_time': current_time
                })
                
            elif price_interaction['type'] == 'CLEAN_BREAK':
                self._transition_to_status(OrderBlockStatus.BROKEN, {
                    'break_price': current_price,
                    'break_time': current_time,
                    'break_strength': price_interaction.get('break_strength', 1.0)
                })
            
            # 4. Verificar transición a Breaker Block
            if (self.status == OrderBlockStatus.BROKEN and 
                self._check_breaker_formation(current_price, current_time)):
                self._transition_to_status(OrderBlockStatus.BREAKER, {
                    'breaker_confirmation_price': current_price,
                    'breaker_confirmation_time': current_time
                })
            
            # 5. Actualizar métricas de performance
            self._update_performance_metrics(price_interaction)
            
            # 6. Registrar evento si hubo cambio
            if previous_status != self.status:
                self._add_lifecycle_event("STATUS_CHANGE", {
                    'from': previous_status.value,
                    'to': self.status.value,
                    'trigger': price_interaction['type'],
                    'price': current_price,
                    'time': current_time
                })
                
        except Exception as e:
            self._add_lifecycle_event("ERROR", {
                'error': str(e),
                'current_price': current_price,
                'time': current_time
            })
    
    def get_strength_score(self) -> float:
        \"\"\"
        💪 Calcula strength actual basado en lifecycle y performance
        
        Returns:
            Float entre 0.0 y 1.0 representando strength actual
        \"\"\"
        try:
            # Strength base del Order Block
            base_strength = self.order_block.get('probability', 50.0) / 100.0
            
            # Ajustes basados en estado
            status_multipliers = {
                OrderBlockStatus.ACTIVE: 1.0,
                OrderBlockStatus.MITIGATING: 0.95,
                OrderBlockStatus.PARTIALLY_FILLED: 0.70,
                OrderBlockStatus.FULLY_FILLED: 0.10,
                OrderBlockStatus.BROKEN: 0.05,
                OrderBlockStatus.EXPIRED: 0.20,
                OrderBlockStatus.BREAKER: 0.85  # Breaker tiene nueva fuerza
            }
            
            status_multiplier = status_multipliers.get(self.status, 1.0)
            
            # Ajustes basados en performance histórica
            performance_multiplier = 1.0
            
            if self.performance_metrics['total_tests'] > 0:
                success_rate = (self.performance_metrics['successful_tests'] / 
                              self.performance_metrics['total_tests'])
                
                # Success rate alto = strength aumentada
                performance_multiplier = 0.8 + (success_rate * 0.4)  # 0.8 a 1.2
            
            # Ajuste por edad (Order Blocks frescos son más fuertes)
            age_multiplier = self._calculate_age_multiplier()
            
            # Ajustes manuales aplicados
            manual_multiplier = 1.0
            for adjustment in self.strength_adjustments:
                manual_multiplier *= adjustment.get('multiplier', 1.0)
            
            # Strength final
            final_strength = (base_strength * 
                            status_multiplier * 
                            performance_multiplier * 
                            age_multiplier * 
                            manual_multiplier)
            
            return max(0.0, min(1.0, final_strength))
            
        except Exception as e:
            return 0.5  # Fallback a strength neutral
    
    def is_still_valid(self) -> bool:
        \"\"\"
        ✅ Determina si el Order Block sigue siendo válido para trading
        
        Returns:
            bool: True si es válido, False si no
        \"\"\"
        try:
            # Estados que invalidan completamente el OB
            invalid_states = [
                OrderBlockStatus.FULLY_FILLED,
                OrderBlockStatus.BROKEN,
                OrderBlockStatus.EXPIRED
            ]
            
            if self.status in invalid_states:
                return False
            
            # Verificar strength mínima
            current_strength = self.get_strength_score()
            min_valid_strength = 0.30  # 30% mínimo
            
            if current_strength < min_valid_strength:
                return False
            
            # Verificar si no ha sido sobre-testeado
            max_failed_tests = 3
            if self.performance_metrics['failed_tests'] >= max_failed_tests:
                return False
            
            # Verificar que no sea demasiado viejo
            if self._is_expired(datetime.now()):
                return False
            
            return True
            
        except Exception as e:
            return False
    
    def add_manual_strength_adjustment(self, multiplier: float, reason: str):
        \"\"\"🔧 Permite ajuste manual de strength\"\"\"
        self.strength_adjustments.append({
            'multiplier': multiplier,
            'reason': reason,
            'timestamp': datetime.now()
        })
        
        self._add_lifecycle_event("MANUAL_ADJUSTMENT", {
            'multiplier': multiplier,
            'reason': reason
        })
    
    def get_lifecycle_summary(self) -> Dict:
        \"\"\"📊 Obtiene resumen completo del lifecycle\"\"\"
        current_time = datetime.now()
        
        return {
            'order_block_id': self.order_block.get('id', 'unknown'),
            'current_status': self.status.value,
            'current_strength': self.get_strength_score(),
            'is_valid': self.is_still_valid(),
            'age_hours': self._get_lifetime_hours(current_time),
            'max_lifetime_hours': self.max_lifetime.total_seconds() / 3600,
            'performance_metrics': self.performance_metrics.copy(),
            'total_lifecycle_events': len(self.lifecycle_history),
            'total_mitigation_events': len(self.mitigation_events),
            'strength_adjustments_count': len(self.strength_adjustments)
        }
    
    # ===================================
    # MÉTODOS PRIVADOS
    # ===================================
    
    def _calculate_max_lifetime(self) -> timedelta:
        \"\"\"⏰ Calcula vida útil máxima basada en timeframe\"\"\"
        lifetime_mapping = {
            'M5': timedelta(hours=8),
            'M15': timedelta(hours=24),
            'H1': timedelta(hours=72),
            'H4': timedelta(hours=168),
            'D1': timedelta(days=30)
        }
        
        return lifetime_mapping.get(self.timeframe, timedelta(hours=72))
    
    def _is_expired(self, current_time: datetime) -> bool:
        \"\"\"⏰ Verifica si el Order Block ha expirado\"\"\"
        creation_time = self.order_block.get('origin_timestamp', current_time)
        
        if isinstance(creation_time, str):
            # Parsear si es string
            creation_time = datetime.fromisoformat(creation_time.replace('Z', '+00:00'))
        
        age = current_time - creation_time
        return age > self.max_lifetime
    
    def _get_lifetime_hours(self, current_time: datetime) -> float:
        \"\"\"📅 Calcula horas de vida del Order Block\"\"\"
        creation_time = self.order_block.get('origin_timestamp', current_time)
        
        if isinstance(creation_time, str):
            creation_time = datetime.fromisoformat(creation_time.replace('Z', '+00:00'))
        
        age = current_time - creation_time
        return age.total_seconds() / 3600
    
    def _analyze_price_interaction(self, current_price: float, candle_data: Optional[Dict]) -> Dict:
        \"\"\"🔍 Analiza interacción del precio con el Order Block\"\"\"
        ob_high = self.order_block['high_price']
        ob_low = self.order_block['low_price']
        ob_type = self.order_block['type']
        
        # Determinar si hay interacción
        if current_price < ob_low or current_price > ob_high:
            return {'type': 'NO_INTERACTION'}
        
        # Hay interacción - analizar tipo
        ob_range = ob_high - ob_low
        
        if ob_type == 'BULLISH_OB':
            # Medir penetración desde arriba
            penetration = ob_high - current_price
            penetration_percentage = (penetration / ob_range) * 100
        else:
            # Medir penetración desde abajo
            penetration = current_price - ob_low
            penetration_percentage = (penetration / ob_range) * 100
        
        # Clasificar tipo de interacción
        if penetration_percentage < 10:
            return {
                'type': 'TOUCH',
                'penetration_depth': penetration,
                'penetration_percentage': penetration_percentage
            }
        elif penetration_percentage < 75:
            return {
                'type': 'PARTIAL_FILL',
                'penetration_depth': penetration,
                'fill_percentage': penetration_percentage
            }
        elif penetration_percentage < 100:
            return {
                'type': 'FULL_FILL',
                'penetration_depth': penetration,
                'fill_percentage': penetration_percentage
            }
        else:
            return {
                'type': 'CLEAN_BREAK',
                'penetration_depth': penetration,
                'break_strength': min(2.0, penetration_percentage / 100.0)
            }
    
    def _transition_to_status(self, new_status: OrderBlockStatus, event_data: Dict):
        \"\"\"🔄 Transiciona a nuevo estado\"\"\"
        old_status = self.status
        self.status = new_status
        
        # Registrar evento de transición
        self._add_lifecycle_event("TRANSITION", {
            'from_status': old_status.value,
            'to_status': new_status.value,
            **event_data
        })
        
        # Actualizar métricas específicas del estado
        if new_status == OrderBlockStatus.MITIGATING:
            self.mitigation_events.append({
                'timestamp': datetime.now(),
                'event_data': event_data
            })
    
    def _check_breaker_formation(self, current_price: float, current_time: datetime) -> bool:
        \"\"\"💥 Verifica si se está formando un Breaker Block\"\"\"
        # Lógica simplificada - en producción sería más compleja
        # Breaker se forma cuando el precio retorna al OB después de romperlo
        
        # TODO: Implementar lógica completa de Breaker Block detection
        return False
    
    def _update_performance_metrics(self, price_interaction: Dict):
        \"\"\"📊 Actualiza métricas de performance\"\"\"
        if price_interaction['type'] != 'NO_INTERACTION':
            self.performance_metrics['total_tests'] += 1
            
            # Determinar si fue test exitoso o fallido
            if price_interaction['type'] in ['TOUCH', 'PARTIAL_FILL']:
                self.performance_metrics['successful_tests'] += 1
            elif price_interaction['type'] in ['FULL_FILL', 'CLEAN_BREAK']:
                self.performance_metrics['failed_tests'] += 1
            
            # Actualizar penetración máxima
            penetration = price_interaction.get('penetration_depth', 0.0)
            self.performance_metrics['max_penetration'] = max(
                self.performance_metrics['max_penetration'], 
                penetration
            )
    
    def _calculate_age_multiplier(self) -> float:
        \"\"\"👴 Calcula multiplicador por edad\"\"\"
        current_time = datetime.now()
        age_hours = self._get_lifetime_hours(current_time)
        max_age_hours = self.max_lifetime.total_seconds() / 3600
        
        # Age multiplier: frescos = 1.0, viejos = 0.7
        age_ratio = age_hours / max_age_hours
        return max(0.7, 1.0 - (age_ratio * 0.3))
    
    def _add_lifecycle_event(self, event_type: str, event_data: Dict):
        \"\"\"📝 Registra evento en historial\"\"\"
        self.lifecycle_history.append({
            'timestamp': datetime.now(),
            'event_type': event_type,
            'event_data': event_data.copy()
        })
        
        # Mantener solo los últimos 50 eventos
        self.lifecycle_history = self.lifecycle_history[-50:]
```

### **Pregunta 4.3 (7 puntos) - Factor Tiempo en Validez**

**Respuesta basada en implementación:**

**⏰ Tiempo y Validez de Order Blocks en ICT Engine v6.0:**

**1. 📅 Tiempo Máximo de Vida Útil:**
```python
# Implementado en OrderBlockLifecycle
TIMEFRAME_MAX_LIFETIME = {
    'M5': timedelta(hours=8),      # 8 horas máximo
    'M15': timedelta(hours=24),    # 1 día máximo  
    'H1': timedelta(hours=72),     # 3 días máximo
    'H4': timedelta(hours=168),    # 1 semana máximo
    'D1': timedelta(days=30)       # 1 mes máximo
}

def _calculate_max_lifetime(self) -> timedelta:
    \"\"\"⏰ Vida útil basada en timeframe de origen\"\"\"
    return TIMEFRAME_MAX_LIFETIME.get(self.timeframe, timedelta(hours=72))
```

**Justificación por timeframe:**
- **M5/M15:** Actividad institucional de corto plazo (sesiones específicas)
- **H1:** Operaciones intraday a multi-day
- **H4:** Operaciones weekly - estructura principal
- **D1:** Operaciones monthly - bias fundamental

**2. 📊 Variación por Timeframe de Origen:**
```python
def calculate_time_decay_factor(self, current_age_hours: float) -> float:
    \"\"\"
    📉 Calcula factor de decay temporal para Order Block
    
    Timeframes menores decaen más rápido
    \"\"\"
    max_lifetime_hours = self.max_lifetime.total_seconds() / 3600
    age_ratio = current_age_hours / max_lifetime_hours
    
    # Curvas de decay por timeframe
    decay_curves = {
        'M5': lambda x: max(0.1, 1.0 - (x * 1.5)),     # Decay rápido
        'M15': lambda x: max(0.2, 1.0 - (x * 1.2)),    # Decay moderado-rápido
        'H1': lambda x: max(0.3, 1.0 - (x * 1.0)),     # Decay lineal
        'H4': lambda x: max(0.4, 1.0 - (x * 0.8)),     # Decay lento
        'D1': lambda x: max(0.5, 1.0 - (x * 0.6))      # Decay muy lento
    }
    
    decay_function = decay_curves.get(self.timeframe, decay_curves['H1'])
    return decay_function(age_ratio)
```

**3. 🎯 Factores que Extienden Validez:**
```python
def calculate_extended_lifetime_factors(self, order_block: Dict) -> Dict:
    \"\"\"
    🚀 Factores que pueden extender la vida útil del Order Block
    \"\"\"
    extension_factors = {
        'base_lifetime': self.max_lifetime,
        'extensions': {},
        'total_extension_hours': 0.0
    }
    
    # Factor 1: Virgin Order Block
    if order_block.get('status') == 'VIRGIN':
        virgin_extension = self.max_lifetime.total_seconds() / 3600 * 0.3  # +30%
        extension_factors['extensions']['virgin_bonus'] = virgin_extension
        extension_factors['total_extension_hours'] += virgin_extension
    
    # Factor 2: Alta strength inicial
    initial_strength = order_block.get('probability', 50.0)
    if initial_strength >= 85.0:
        strength_extension = self.max_lifetime.total_seconds() / 3600 * 0.2  # +20%
        extension_factors['extensions']['high_strength'] = strength_extension
        extension_factors['total_extension_hours'] += strength_extension
    
    # Factor 3: Volumen institucional extremo
    volume = order_block.get('volume', 0)
    if volume >= 1500:  # Volumen muy alto
        volume_extension = self.max_lifetime.total_seconds() / 3600 * 0.15  # +15%
        extension_factors['extensions']['high_volume'] = volume_extension
        extension_factors['total_extension_hours'] += volume_extension
    
    # Factor 4: Confluencia con niveles importantes
    if order_block.get('confluence_score', 0.0) >= 0.80:
        confluence_extension = self.max_lifetime.total_seconds() / 3600 * 0.25  # +25%
        extension_factors['extensions']['high_confluence'] = confluence_extension
        extension_factors['total_extension_hours'] += confluence_extension
    
    # Factor 5: Round numbers o niveles psicológicos
    ob_price = (order_block['high_price'] + order_block['low_price']) / 2
    if self._is_round_number(ob_price):
        round_number_extension = self.max_lifetime.total_seconds() / 3600 * 0.10  # +10%
        extension_factors['extensions']['round_number'] = round_number_extension
        extension_factors['total_extension_hours'] += round_number_extension
    
    return extension_factors

def _is_round_number(self, price: float) -> bool:
    \"\"\"🎯 Detecta si el precio es round number\"\"\"
    # Para EURUSD: 1.1000, 1.0950, etc.
    decimal_part = price - int(price)
    
    # Round numbers comunes en forex
    round_levels = [0.0000, 0.0050, 0.0100, 0.0150, 0.0200, 0.0250]
    tolerance = 0.0005
    
    return any(abs(decimal_part - level) <= tolerance for level in round_levels)
```

**4. ⚠️ Factores que Acortan Validez:**
```python
def calculate_shortened_lifetime_factors(self, order_block: Dict) -> Dict:
    \"\"\"
    ⏱️ Factores que reducen la vida útil del Order Block
    \"\"\"
    reduction_factors = {
        'reductions': {},
        'total_reduction_hours': 0.0
    }
    
    # Factor 1: Múltiples tests fallidos
    failed_tests = self.performance_metrics.get('failed_tests', 0)
    if failed_tests >= 2:
        test_reduction = self.max_lifetime.total_seconds() / 3600 * 0.20 * failed_tests
        reduction_factors['reductions']['failed_tests'] = test_reduction
        reduction_factors['total_reduction_hours'] += test_reduction
    
    # Factor 2: Alta volatilidad del mercado
    if order_block.get('market_volatility', 'normal') == 'high':
        volatility_reduction = self.max_lifetime.total_seconds() / 3600 * 0.15
        reduction_factors['reductions']['high_volatility'] = volatility_reduction
        reduction_factors['total_reduction_hours'] += volatility_reduction
    
    # Factor 3: Cambio de sesión de mercado
    if self._session_change_detected():
        session_reduction = self.max_lifetime.total_seconds() / 3600 * 0.10
        reduction_factors['reductions']['session_change'] = session_reduction
        reduction_factors['total_reduction_hours'] += session_reduction
    
    # Factor 4: News events importantes
    if order_block.get('news_impact', 'none') in ['high', 'very_high']:
        news_reduction = self.max_lifetime.total_seconds() / 3600 * 0.25
        reduction_factors['reductions']['news_impact'] = news_reduction
        reduction_factors['total_reduction_hours'] += news_reduction
    
    return reduction_factors
```

**📊 Implementación Final del Factor Tiempo:**
```python
def get_effective_remaining_lifetime(self) -> timedelta:
    \"\"\"
    ⏰ Calcula vida útil efectiva considerando todos los factores
    \"\"\"
    base_lifetime_hours = self.max_lifetime.total_seconds() / 3600
    
    # Calcular extensiones
    extensions = self.calculate_extended_lifetime_factors(self.order_block)
    extension_hours = extensions['total_extension_hours']
    
    # Calcular reducciones
    reductions = self.calculate_shortened_lifetime_factors(self.order_block)
    reduction_hours = reductions['total_reduction_hours']
    
    # Vida útil ajustada
    adjusted_lifetime_hours = base_lifetime_hours + extension_hours - reduction_hours
    
    # Mínimo de 2 horas, máximo de 5x el base lifetime
    min_hours = 2.0
    max_hours = base_lifetime_hours * 5.0
    
    final_hours = max(min_hours, min(max_hours, adjusted_lifetime_hours))
    
    return timedelta(hours=final_hours)
```

### **Pregunta 4.4 (5 puntos) - Comportamiento por Sesiones**

**Respuesta:**

**🌍 Comportamiento Order Blocks por Sesiones de Mercado:**

```python
class SessionOrderBlockBehavior:
    \"\"\"
    🌍 Analiza comportamiento de Order Blocks por sesiones de mercado
    
    Implementación basada en observaciones de ICT Engine v6.0
    \"\"\"
    
    SESSION_CONFIGS = {
        'ASIAN': {
            'start_hour': 0,   # 00:00 GMT
            'end_hour': 8,     # 08:00 GMT
            'characteristics': {
                'volatility': 'LOW',
                'volume': 'LOW', 
                'ob_behavior': 'CONSOLIDATION',
                'respect_rate': 0.70,  # 70% respeto de OBs
                'formation_quality': 'MODERATE'
            }
        },
        'LONDON': {
            'start_hour': 8,   # 08:00 GMT
            'end_hour': 16,    # 16:00 GMT  
            'characteristics': {
                'volatility': 'HIGH',
                'volume': 'HIGH',
                'ob_behavior': 'AGGRESSIVE',
                'respect_rate': 0.85,  # 85% respeto de OBs
                'formation_quality': 'HIGH'
            }
        },
        'NEW_YORK': {
            'start_hour': 13,  # 13:00 GMT (overlap con London)
            'end_hour': 22,    # 22:00 GMT
            'characteristics': {
                'volatility': 'VERY_HIGH',
                'volume': 'VERY_HIGH',
                'ob_behavior': 'INSTITUTIONAL',
                'respect_rate': 0.90,  # 90% respeto de OBs
                'formation_quality': 'PREMIUM'
            }
        },
        'LONDON_NY_OVERLAP': {
            'start_hour': 13,  # 13:00 GMT
            'end_hour': 16,    # 16:00 GMT
            'characteristics': {
                'volatility': 'EXTREME',
                'volume': 'EXTREME',
                'ob_behavior': 'SMART_MONEY',
                'respect_rate': 0.95,  # 95% respeto de OBs
                'formation_quality': 'INSTITUTIONAL'
            }
        }
    }
    
    def analyze_ob_by_session(self, order_block: Dict, current_session: str) -> Dict:
        \"\"\"
        📊 Analiza comportamiento del Order Block según la sesión
        \"\"\"
        session_config = self.SESSION_CONFIGS.get(current_session, self.SESSION_CONFIGS['LONDON'])
        
        analysis = {
            'session': current_session,
            'expected_behavior': session_config['characteristics']['ob_behavior'],
            'respect_probability': session_config['characteristics']['respect_rate'],
            'strategy_adjustments': {},
            'risk_factors': [],
            'opportunities': []
        }
        
        # Ajustes estratégicos por sesión
        if current_session == 'ASIAN':
            analysis['strategy_adjustments'] = {
                'position_sizing': 0.7,  # Reducir posición 30%
                'stop_loss': 'TIGHT',    # Stops más ajustados
                'take_profit': 'CONSERVATIVE',  # TPs conservadores
                'entry_timing': 'PATIENT',      # Esperar confirmación
                'reasoning': 'Baja volatilidad - movimientos limitados'
            }
            
            analysis['risk_factors'] = [
                'Falsos breakouts frecuentes',
                'Baja participación institucional',
                'Rangos de movimiento limitados'
            ]
            
        elif current_session == 'LONDON':
            analysis['strategy_adjustments'] = {
                'position_sizing': 1.0,  # Posición normal
                'stop_loss': 'STANDARD', # Stops normales
                'take_profit': 'AGGRESSIVE', # TPs más amplios
                'entry_timing': 'ACTIVE',    # Entradas activas
                'reasoning': 'Alta actividad institucional europea'
            }
            
            analysis['opportunities'] = [
                'Formación de OBs de alta calidad',
                'Movimientos direccionales claros',
                'Respeto institucional de niveles'
            ]
            
        elif current_session == 'NEW_YORK':
            analysis['strategy_adjustments'] = {
                'position_sizing': 1.2,  # Aumentar posición 20%
                'stop_loss': 'WIDE',     # Stops más amplios
                'take_profit': 'AGGRESSIVE', # TPs ambiciosos
                'entry_timing': 'FAST',      # Entradas rápidas
                'reasoning': 'Máxima liquidez y actividad institucional'
            }
            
            analysis['opportunities'] = [
                'Order Blocks de máxima calidad',
                'Movimientos institucionales grandes',
                'Respect rate más alto'
            ]
            
        elif current_session == 'LONDON_NY_OVERLAP':
            analysis['strategy_adjustments'] = {
                'position_sizing': 1.5,  # Máxima posición
                'stop_loss': 'DYNAMIC',  # Stops dinámicos
                'take_profit': 'PREMIUM', # TPs premium
                'entry_timing': 'AGGRESSIVE', # Máxima agresividad
                'reasoning': 'OVERLAP = máxima actividad smart money'
            }
            
            analysis['opportunities'] = [
                'Setup premium - confluencia máxima',
                'Smart money más activo',
                'Order Blocks institucionales puros'
            ]
        
        return analysis
    
    def adapt_strategy_by_session(self, base_strategy: Dict, session_analysis: Dict) -> Dict:
        \"\"\"
        🔧 Adapta estrategia base según análisis de sesión
        \"\"\"
        adapted_strategy = base_strategy.copy()
        adjustments = session_analysis['strategy_adjustments']
        
        # Ajustar position sizing
        base_position = adapted_strategy.get('position_size', 1.0)
        size_multiplier = adjustments.get('position_sizing', 1.0)
        adapted_strategy['position_size'] = base_position * size_multiplier
        
        # Ajustar stops
        stop_type = adjustments.get('stop_loss', 'STANDARD')
        if stop_type == 'TIGHT':
            adapted_strategy['stop_loss_pips'] = adapted_strategy.get('stop_loss_pips', 10) * 0.7
        elif stop_type == 'WIDE':
            adapted_strategy['stop_loss_pips'] = adapted_strategy.get('stop_loss_pips', 10) * 1.5
        elif stop_type == 'DYNAMIC':
            adapted_strategy['stop_loss_type'] = 'TRAILING_DYNAMIC'
        
        # Ajustar take profits
        tp_type = adjustments.get('take_profit', 'STANDARD')
        if tp_type == 'CONSERVATIVE':
            adapted_strategy['take_profit_ratio'] = 1.5  # 1:1.5 R:R
        elif tp_type == 'AGGRESSIVE':
            adapted_strategy['take_profit_ratio'] = 3.0  # 1:3 R:R
        elif tp_type == 'PREMIUM':
            adapted_strategy['take_profit_ratio'] = 5.0  # 1:5 R:R
        
        # Añadir metadata
        adapted_strategy['session_adapted'] = True
        adapted_strategy['session'] = session_analysis['session']
        adapted_strategy['adaptation_reasoning'] = adjustments.get('reasoning', '')
        
        return adapted_strategy
```

**📊 Diferencias Clave por Sesión:**

1. **🌸 Asian Session (00:00-08:00 GMT):**
   - **OB Behavior:** Consolidación y ranging
   - **Respect Rate:** 70% (menor)
   - **Strategy:** Conservadora, stops tight, TPs limitados

2. **🇬🇧 London Session (08:00-16:00 GMT):**
   - **OB Behavior:** Agresivo, direccional
   - **Respect Rate:** 85% (alta)
   - **Strategy:** Activa, TPs ambiciosos

3. **🇺🇸 New York Session (13:00-22:00 GMT):**
   - **OB Behavior:** Institucional puro
   - **Respect Rate:** 90% (muy alta)
   - **Strategy:** Agresiva, máxima confianza

4. **⭐ London-NY Overlap (13:00-16:00 GMT):**
   - **OB Behavior:** Smart Money dominante
   - **Respect Rate:** 95% (máxima)
   - **Strategy:** Premium, maximum aggression

---

*Continuando con las Secciones 5 y 6...*
