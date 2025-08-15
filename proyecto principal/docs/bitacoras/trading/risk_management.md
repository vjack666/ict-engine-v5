# 🛡️ RISK MANAGEMENT - ICT ENGINE v5.0 ✅ ACTUALIZADA

**Última Actualización:** 14 Agosto 2025 - 18:45 hrs  
**Estado:** ✅ **RISKBOT MT5 + RISK MANAGER v6.0 ENTERPRISE**  
**Sistema:** ✅ **GESTIÓN DE RIESGO AVANZADA + SISTEMA ADAPTATIVO**

---

## 🚀 **ACTUALIZACIÓN 14 AGOSTO 2025 - RISK MANAGER v6.0 ENTERPRISE**

### ✅ **NUEVO COMPONENTE INTEGRADO**
- 🎯 **Risk Manager v6.0 Enterprise:** Sistema adaptativo de gestión de riesgo
- 📍 **Ubicación:** `ict-engine-v6.0-enterprise-sic/06-TOOLS/backtest-original/engines/risk_manager.py`
- 🔄 **Modo Dual:** Compatible con backtesting y trading live
- 🎛️ **Integración ICT:** POI system + Smart Money Concepts

### 🎯 **CARACTERÍSTICAS NUEVAS**
```python
# Inicialización adaptativa
risk_manager = RiskManager(
    mode='live',                    # 'backtest' o 'live'
    ict_config=ICTRiskConfig(       # Configuración ICT específica
        poi_weight_factor=1.2,      # Factor peso POI
        smart_money_factor=1.1,     # Factor Smart Money
        correlation_threshold=0.7   # Umbral correlación
    )
)

# Position sizing con factores ICT
position_size = risk_manager.calculate_ict_position_size(
    account_balance=25000,
    entry_price=1.0850,
    stop_loss=1.0820,
    poi_quality='A',              # A, B, C, D
    smart_money_signal=True,      # Confirmación SMC
    session='overlap'             # london, new_york, asian, overlap
)
```

### 🚨 **SISTEMA DE ALERTAS AVANZADO**
```python
# Alertas automáticas implementadas
ALERT_TYPES = {
    'MAX_POSITIONS_REACHED': 'CRITICAL',
    'MAX_DRAWDOWN_EXCEEDED': 'CRITICAL', 
    'DAILY_LOSS_EXCEEDED': 'CRITICAL',
    'HIGH_CORRELATION_RISK': 'WARNING'
}

# Verificación completa
risk_status = risk_manager.check_risk_limits(
    current_positions=2,
    current_drawdown=0.12,
    daily_loss=0.03,
    open_positions=current_positions_list
)
```

---

## 📋 **PROPÓSITO Y ALCANCE - ACTUALIZADO**

Esta carpeta almacena todos los eventos relacionados con la gestión de riesgos del **ICT Engine v5.0** con **Multi-POI Dashboard integrado**, incluyendo cálculos de riesgo, alertas de exposición, stops dinámicos y protección de capital.

### **🛡️ COMPONENTES ACTIVOS**
- ✅ **RiskBot MT5:** `core/risk_management/riskbot_mt5.py`
- ✅ **POI Risk Scoring:** Integrado con `poi_scoring_engine.py`
- ✅ **Dashboard Integration:** Panel visual de riesgo en tiempo real
- ✅ **Multi-Timeframe Analysis:** Gestión de riesgo por confluencia POI
- ✅ **Dynamic Position Sizing:** Basado en puntuación POI y volatilidad

### **📊 MÉTRICAS DE RIESGO IMPLEMENTADAS**
```python
# Sistema de Scoring POI integrado con gestión de riesgo
POI_RISK_LEVELS = {
    'ALTO': 8.0-10.0,     # Posiciones reducidas, SL ajustado
    'MEDIO': 5.0-7.9,     # Posición estándar
    'BAJO': 0.0-4.9       # Posición incrementada si confluencia
}
```

## 🏗️ **ESTRUCTURA DE ARCHIVOS**

```
risk_management/
├── risk_management_2025-08-01.jsonl  # Eventos de riesgo del día actual
├── risk_management_2025-07-31.jsonl  # Eventos de riesgo del día anterior
├── README.md                          # Esta documentación
├── exposure/
│   ├── current_exposure.json         # Exposición actual del portfolio
│   ├── exposure_limits.json          # Límites de exposición configurados
│   └── exposure_history.json         # Historial de exposición
├── scenarios/
│   ├── stress_test_results.json      # Resultados de stress testing
│   ├── monte_carlo_analysis.json     # Análisis Monte Carlo
│   └── worst_case_scenarios.json     # Escenarios de pérdida máxima
├── alerts/
│   ├── risk_alerts_active.json       # Alertas de riesgo activas
│   ├── alert_history.json            # Historial de alertas
│   └── alert_thresholds.json         # Umbrales de alertas configurados
└── reports/
    ├── daily_risk_report.json        # Reporte diario de riesgos
    ├── var_calculations.json         # Cálculos de Value at Risk
    └── risk_metrics_summary.json     # Resumen de métricas de riesgo
```

## 📊 **FORMATO DE DATOS (JSONL)**

### **Estructura base de cada línea:**
```json
{
    "timestamp": "2025-08-01T14:23:45.123456",
    "bitacora_type": "risk_management",
    "severity": "CRITICAL|HIGH|MEDIUM|LOW|INFO",
    "component": "RISK_CALCULATOR|POSITION_SIZER|STOP_MANAGER|EXPOSURE_MONITOR|ALERT_SYSTEM",
    "event_id": "RISK_CALCULATED|EXPOSURE_ALERT|STOP_UPDATED|LIMIT_BREACHED|SCENARIO_ANALYZED",
    "description": "Portfolio exposure approaching maximum limit",
    "risk_metrics": {
        "current_var_1d": 2.5,
        "current_var_5d": 5.8,
        "expected_shortfall": 3.2,
        "maximum_drawdown": 1.8,
        "sharpe_ratio": 1.85,
        "sortino_ratio": 2.12,
        "calmar_ratio": 1.23,
        "beta": 0.87,
        "alpha": 0.045,
        "information_ratio": 1.34
    },
    "portfolio_exposure": {
        "total_exposure_usd": 15750.50,
        "total_exposure_percent": 78.75,
        "max_allowed_exposure_percent": 80.0,
        "margin_used_percent": 23.4,
        "free_margin_usd": 4249.50,
        "equity_usd": 20000.00,
        "balance_usd": 19875.25,
        "floating_pnl_usd": 124.75,
        "realized_pnl_today_usd": 67.50
    },
    "position_risk": {
        "open_positions": 3,
        "total_risk_per_position": [1.5, 2.0, 1.2],
        "combined_risk_percent": 4.7,
        "largest_position_risk": 2.0,
        "correlation_risk": 0.65,
        "concentration_risk": "LOW|MEDIUM|HIGH",
        "currency_exposure": {
            "EUR": 45.2,
            "GBP": 32.8,
            "JPY": -15.3,
            "USD": -62.7
        }
    },
    "stop_loss_management": {
        "static_stops": 2,
        "dynamic_stops": 1,
        "trailing_stops": 0,
        "average_stop_distance_pips": 28.5,
        "stop_loss_efficiency": 87.3,
        "stop_adjustments_today": 5,
        "emergency_stops_triggered": 0,
        "stop_to_entry_ratio": 1.8
    },
    "risk_limits": {
        "daily_loss_limit_percent": 2.0,
        "daily_loss_current_percent": 0.3,
        "weekly_loss_limit_percent": 5.0,
        "weekly_loss_current_percent": 1.2,
        "monthly_loss_limit_percent": 10.0,
        "monthly_loss_current_percent": 3.8,
        "maximum_positions": 5,
        "current_positions": 3,
        "maximum_risk_per_trade": 2.0,
        "maximum_total_risk": 10.0
    },
    "correlation_analysis": {
        "portfolio_correlation_matrix": [
            [1.0, 0.65, -0.23],
            [0.65, 1.0, -0.15],
            [-0.23, -0.15, 1.0]
        ],
        "correlation_risk_score": 65.2,
        "diversification_ratio": 1.34,
        "concentration_index": 0.42,
        "sector_concentration": {
            "FOREX_MAJORS": 85.0,
            "FOREX_MINORS": 15.0
        }
    },
    "stress_testing": {
        "scenario_name": "MARKET_CRASH_2008|COVID_CRASH_2020|FLASH_CRASH|CUSTOM",
        "scenario_impact_percent": -12.5,
        "portfolio_survival_probability": 94.2,
        "recovery_time_days": 45,
        "maximum_loss_scenario": -18.7,
        "stress_test_date": "2025-08-01T12:00:00.000000",
        "confidence_level": 95.0
    },
    "monte_carlo_results": {
        "simulations_run": 10000,
        "confidence_intervals": {
            "95_percent": {"lower": -5.2, "upper": 12.8},
            "99_percent": {"lower": -8.7, "upper": 15.3}
        },
        "probability_of_profit": 68.5,
        "expected_return": 2.3,
        "volatility": 8.9,
        "skewness": -0.15,
        "kurtosis": 3.42
    },
    "risk_alerts": {
        "active_alerts": [
            {
                "alert_id": "EXPOSURE_HIGH_001",
                "alert_type": "EXPOSURE_WARNING",
                "alert_level": "MEDIUM",
                "message": "Portfolio exposure at 78% of maximum limit",
                "triggered_at": "2025-08-01T14:15:30.123456",
                "threshold_value": 75.0,
                "current_value": 78.75,
                "auto_action": "REDUCE_POSITION_SIZE"
            }
        ],
        "alerts_triggered_today": 3,
        "critical_alerts_count": 0,
        "auto_actions_taken": 1
    },
    "position_sizing": {
        "optimal_position_sizes": [0.5, 0.75, 0.25],
        "kelly_criterion_recommendation": 0.65,
        "fixed_fractional_size": 1.0,
        "volatility_adjusted_size": 0.85,
        "risk_parity_weights": [0.33, 0.45, 0.22],
        "final_position_size": 0.75,
        "sizing_method": "KELLY|FIXED|VOLATILITY|RISK_PARITY|CUSTOM"
    },
    "liquidity_risk": {
        "average_spread_pips": 1.2,
        "market_impact_percent": 0.05,
        "bid_ask_spread_cost": 0.12,
        "slippage_expectation_pips": 0.8,
        "execution_risk_score": 15.3,
        "market_depth_score": 92.1,
        "liquidity_buffer_percent": 10.0
    },
    "regulatory_compliance": {
        "margin_requirement_met": true,
        "position_limits_compliant": true,
        "reporting_requirements_met": true,
        "risk_disclosure_acknowledged": true,
        "leverage_within_limits": true,
        "maximum_leverage_used": 3.2,
        "allowed_maximum_leverage": 30.0
    },
    "performance_attribution": {
        "alpha_contribution": 0.023,
        "beta_contribution": 0.034,
        "currency_contribution": -0.005,
        "timing_contribution": 0.012,
        "selection_contribution": 0.018,
        "interaction_contribution": 0.003,
        "total_return_contribution": 0.085
    },
    "tail_risk_measures": {
        "conditional_var_95": 4.2,
        "conditional_var_99": 6.8,
        "expected_tail_loss": 5.1,
        "tail_ratio": 1.15,
        "extreme_risk_probability": 2.3,
        "black_swan_protection": 85.2
    },
    "dynamic_hedging": {
        "hedge_ratio": 0.25,
        "hedge_effectiveness": 78.9,
        "hedging_cost_percent": 0.15,
        "delta_hedge_required": false,
        "correlation_hedge_required": true,
        "volatility_hedge_required": false,
        "hedge_instruments": ["EURUSD_PUT", "VIX_CALL"]
    },
    "metadata": {
        "session_id": "ICT_20250801_142345_abc123",
        "risk_model_version": "v3.2.1",
        "calculation_time_ms": 89.4,
        "data_quality_score": 97.8,
        "model_confidence": 92.5,
        "last_calibration_date": "2025-07-28T00:00:00.000000",
        "risk_manager": "SYSTEM|MANUAL|HYBRID",
        "environment": "LIVE|DEMO|BACKTEST"
    }
}
```

## 🎯 **TIPOS DE RIESGOS MONITOREADOS**

### **1. MARKET RISK (📈)**
- **VaR (Value at Risk):** Pérdida máxima esperada en condiciones normales
- **Expected Shortfall:** Pérdida promedio en escenarios adversos
- **Volatility Risk:** Riesgo por cambios en volatilidad
- **Correlation Risk:** Riesgo por cambios en correlaciones

### **2. LIQUIDITY RISK (💧)**
- **Bid-Ask Spread Risk:** Costo de transacción por spreads
- **Market Impact:** Impacto del tamaño de posición en el precio
- **Slippage Risk:** Diferencia entre precio esperado y ejecutado
- **Execution Risk:** Riesgo de no poder cerrar posiciones

### **3. CREDIT RISK (💳)**
- **Counterparty Risk:** Riesgo de incumplimiento del broker
- **Settlement Risk:** Riesgo en liquidación de operaciones
- **Margin Risk:** Riesgo de margin calls inesperados
- **Leverage Risk:** Riesgo por uso excesivo de apalancamiento

### **4. OPERATIONAL RISK (⚙️)**
- **Technology Risk:** Fallos de sistemas o conectividad
- **Model Risk:** Errores en modelos de pricing o riesgo
- **Human Error:** Errores manuales en trading o configuración
- **Regulatory Risk:** Cambios en regulaciones o compliance

### **5. CONCENTRATION RISK (🎯)**
- **Position Concentration:** Exceso de exposición en una posición
- **Currency Concentration:** Exceso de exposición en una divisa
- **Temporal Concentration:** Exceso de operaciones en mismo tiempo
- **Strategy Concentration:** Dependencia excesiva de una estrategia

## 📊 **CÁLCULOS Y MODELOS DE RIESGO**

### **Value at Risk (VaR):**
```python
def calculate_var(returns, confidence_level=0.95, time_horizon=1):
    """
    Calcula VaR usando método histórico
    """
    percentile = (1 - confidence_level) * 100
    var = np.percentile(returns, percentile) * np.sqrt(time_horizon)
    return abs(var)

def calculate_parametric_var(portfolio_value, volatility, confidence_level=0.95):
    """
    Calcula VaR paramétrico (asume distribución normal)
    """
    z_score = norm.ppf(1 - confidence_level)
    var = portfolio_value * volatility * z_score
    return abs(var)

def calculate_monte_carlo_var(portfolio, simulations=10000, confidence_level=0.95):
    """
    Calcula VaR usando simulación Monte Carlo
    """
    simulated_returns = run_monte_carlo_simulation(portfolio, simulations)
    var = np.percentile(simulated_returns, (1 - confidence_level) * 100)
    return abs(var)
```

### **Position Sizing:**
```python
def kelly_criterion_position_size(win_probability, avg_win, avg_loss):
    """
    Calcula tamaño óptimo de posición usando Kelly Criterion
    """
    win_loss_ratio = avg_win / abs(avg_loss)
    kelly_fraction = win_probability - ((1 - win_probability) / win_loss_ratio)
    return max(0, min(kelly_fraction, 0.25))  # Cap at 25%

def volatility_adjusted_position_size(base_size, current_vol, target_vol):
    """
    Ajusta tamaño de posición basado en volatilidad
    """
    vol_adjustment = target_vol / current_vol
    return base_size * vol_adjustment

def risk_parity_position_size(assets_risk, target_risk_contribution):
    """
    Calcula tamaño de posición para risk parity
    """
    risk_weights = target_risk_contribution / assets_risk
    return risk_weights / np.sum(risk_weights)
```

### **Correlation Risk:**
```python
def calculate_portfolio_correlation_risk(positions, correlation_matrix):
    """
    Calcula riesgo de correlación del portfolio
    """
    weights = np.array([pos.weight for pos in positions])
    portfolio_variance = np.dot(weights.T, np.dot(correlation_matrix, weights))
    diversification_ratio = np.sum(weights) / np.sqrt(portfolio_variance)
    return 1 / diversification_ratio  # Lower is better

def dynamic_correlation_monitoring(returns_matrix, lookback_periods=[30, 60, 90]):
    """
    Monitorea correlaciones dinámicas en múltiples períodos
    """
    correlations = {}
    for period in lookback_periods:
        recent_returns = returns_matrix[-period:]
        correlations[f"{period}d"] = np.corrcoef(recent_returns.T)
    return correlations
```

## 🚨 **SISTEMA DE ALERTAS**

### **Umbrales de alertas por severidad:**
```json
{
    "alert_thresholds": {
        "CRITICAL": {
            "daily_loss_percent": 1.5,
            "portfolio_exposure_percent": 95.0,
            "var_breach_multiple": 2.0,
            "correlation_spike": 0.9,
            "margin_level_percent": 150.0
        },
        "HIGH": {
            "daily_loss_percent": 1.0,
            "portfolio_exposure_percent": 85.0,
            "var_breach_multiple": 1.5,
            "correlation_spike": 0.8,
            "margin_level_percent": 200.0
        },
        "MEDIUM": {
            "daily_loss_percent": 0.5,
            "portfolio_exposure_percent": 75.0,
            "var_breach_multiple": 1.2,
            "correlation_spike": 0.7,
            "margin_level_percent": 300.0
        },
        "LOW": {
            "daily_loss_percent": 0.3,
            "portfolio_exposure_percent": 65.0,
            "var_breach_multiple": 1.1,
            "correlation_spike": 0.6,
            "margin_level_percent": 500.0
        }
    }
}
```

### **Acciones automáticas por tipo de alerta:**
```python
ALERT_ACTIONS = {
    "EXPOSURE_CRITICAL": [
        "CLOSE_LARGEST_POSITION",
        "REDUCE_ALL_POSITIONS_50_PERCENT",
        "STOP_NEW_TRADES"
    ],
    "LOSS_LIMIT_BREACH": [
        "CLOSE_ALL_LOSING_POSITIONS",
        "SUSPEND_TRADING_SESSION",
        "NOTIFY_RISK_MANAGER"
    ],
    "VAR_BREACH": [
        "REDUCE_POSITION_SIZES",
        "INCREASE_HEDGE_RATIO",
        "REVIEW_RISK_PARAMETERS"
    ],
    "CORRELATION_SPIKE": [
        "DIVERSIFY_POSITIONS",
        "REDUCE_CORRELATED_POSITIONS",
        "UPDATE_CORRELATION_MATRIX"
    ],
    "MARGIN_CALL": [
        "CLOSE_MOST_RISKY_POSITION",
        "DEPOSIT_ADDITIONAL_FUNDS",
        "EMERGENCY_LIQUIDATION"
    ]
}
```

## 📈 **STRESS TESTING Y SCENARIO ANALYSIS**

### **Escenarios de stress predefinidos:**
```json
{
    "stress_scenarios": {
        "market_crash_2008": {
            "description": "Financial crisis scenario",
            "market_moves": {
                "EURUSD": -15.2,
                "GBPUSD": -18.7,
                "USDJPY": 12.3,
                "VIX": 250.0
            },
            "correlation_changes": {
                "all_pairs": 0.95
            },
            "volatility_multiplier": 3.5
        },
        "covid_crash_2020": {
            "description": "Pandemic-induced market crash",
            "market_moves": {
                "EURUSD": -8.9,
                "GBPUSD": -12.4,
                "USDJPY": -5.6,
                "VIX": 180.0
            },
            "correlation_changes": {
                "risk_assets": 0.85
            },
            "volatility_multiplier": 2.8
        },
        "flash_crash": {
            "description": "Rapid market dislocation",
            "market_moves": {
                "ALL_PAIRS": "RANDOM_-5_TO_-15"
            },
            "liquidity_impact": {
                "spread_multiplier": 10.0,
                "slippage_multiplier": 5.0
            },
            "duration_minutes": 15
        }
    }
}
```

### **Monte Carlo simulation:**
```python
def run_monte_carlo_risk_analysis(portfolio, scenarios=10000, time_horizon=252):
    """
    Ejecuta análisis Monte Carlo para evaluación de riesgos
    """
    results = []

    for i in range(scenarios):
        # Generate random market scenario
        random_returns = generate_random_market_scenario(time_horizon)

        # Calculate portfolio performance
        portfolio_return = calculate_portfolio_return(portfolio, random_returns)

        # Calculate risk metrics
        max_drawdown = calculate_max_drawdown(portfolio_return)
        volatility = calculate_volatility(portfolio_return)
        sharpe_ratio = calculate_sharpe_ratio(portfolio_return)

        results.append({
            "final_return": portfolio_return[-1],
            "max_drawdown": max_drawdown,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio
        })

    return analyze_monte_carlo_results(results)
```

## 🔧 **CONFIGURACIÓN Y CALIBRACIÓN**

### **Parámetros de riesgo configurables:**
```json
{
    "risk_parameters": {
        "var_confidence_level": 0.95,
        "var_time_horizon_days": 1,
        "correlation_lookback_days": 60,
        "volatility_lookback_days": 30,
        "stress_test_frequency_hours": 24,
        "monte_carlo_simulations": 10000,
        "position_size_method": "KELLY",
        "max_position_size_percent": 5.0,
        "max_total_exposure_percent": 80.0,
        "stop_loss_method": "DYNAMIC",
        "trailing_stop_activation_percent": 50.0
    }
}
```

### **Límites de riesgo por estrategia:**
```json
{
    "strategy_risk_limits": {
        "ict_pattern_trading": {
            "max_daily_loss_percent": 2.0,
            "max_positions": 3,
            "max_risk_per_trade": 1.5,
            "correlation_limit": 0.7
        },
        "poi_reversal_trading": {
            "max_daily_loss_percent": 1.5,
            "max_positions": 2,
            "max_risk_per_trade": 2.0,
            "correlation_limit": 0.6
        },
        "news_trading": {
            "max_daily_loss_percent": 3.0,
            "max_positions": 1,
            "max_risk_per_trade": 3.0,
            "correlation_limit": 0.5
        }
    }
}
```

## 📊 **REPORTES Y ANÁLISIS**

### **Reporte diario de riesgos:**
```python
def generate_daily_risk_report():
    """
    Genera reporte diario completo de riesgos
    """
    return {
        "date": datetime.now().date().isoformat(),
        "summary": {
            "total_var_1d": calculate_portfolio_var(),
            "total_exposure": get_total_exposure(),
            "largest_position_risk": get_largest_position_risk(),
            "correlation_risk_score": calculate_correlation_risk(),
            "liquidity_risk_score": calculate_liquidity_risk()
        },
        "alerts": {
            "critical_alerts": get_critical_alerts(),
            "warning_alerts": get_warning_alerts(),
            "actions_taken": get_auto_actions_taken()
        },
        "performance": {
            "daily_pnl": get_daily_pnl(),
            "mtd_pnl": get_mtd_pnl(),
            "ytd_pnl": get_ytd_pnl(),
            "sharpe_ratio_30d": calculate_30d_sharpe(),
            "max_drawdown_30d": calculate_30d_max_drawdown()
        },
        "stress_tests": {
            "worst_case_loss": run_worst_case_scenario(),
            "stress_test_results": run_all_stress_tests(),
            "recovery_analysis": analyze_recovery_scenarios()
        },
        "recommendations": generate_risk_recommendations()
    }
```

### **Análisis de tendencias de riesgo:**
```python
def analyze_risk_trends(lookback_days=30):
    """
    Analiza tendencias de riesgo en período especificado
    """
    risk_data = load_risk_data(lookback_days)

    trends = {
        "var_trend": calculate_trend(risk_data["var_1d"]),
        "exposure_trend": calculate_trend(risk_data["total_exposure"]),
        "correlation_trend": calculate_trend(risk_data["correlation_risk"]),
        "volatility_trend": calculate_trend(risk_data["portfolio_volatility"]),
        "drawdown_trend": calculate_trend(risk_data["drawdowns"])
    }

    return {
        "trends": trends,
        "risk_score_change": calculate_overall_risk_change(trends),
        "recommendations": generate_trend_recommendations(trends)
    }
```

---

**Última actualización:** 2025-08-01
**Versión:** 3.2.1
**Mantenido por:** Risk Management System v5.0
