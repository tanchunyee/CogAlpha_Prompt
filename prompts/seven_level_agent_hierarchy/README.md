# Seven-Level Agent Hierarchy

The seven-level agent hierarchy contains CogAlpha's task-specific alpha-generation prompts. Each agent focuses on a distinct market mechanism or factor-design perspective while sharing the same coding requirements, library constraints, and output format.

## Components

- **Level I: Market Structure and Cycle** captures slow-moving market phases, regime shifts, and cycle-related dynamics.
- **Level II: Extreme Risk and Fragility** targets crash precursors, tail risk, and asymmetric stress buildup.
- **Level III: Price-Volume Dynamics** models liquidity, volume structure, order imbalance, and price-volume coherence.
- **Level IV: Price-Volatility Behavior** captures trend, reversal, range, volatility asymmetry, and lagged response effects.
- **Level V: Multi-Scale Complexity** describes drawdown behavior, fractal structure, and herding-like dynamics across windows.
- **Level VI: Stability and Regime-Gating** introduces stability-aware and regime-conditioned factor design.
- **Level VII: Geometric and Fusion** combines candle geometry, composite transformations, and creative factor synthesis.

The shared generation scaffold is represented by `base_agent.md`; individual agent files provide the mechanism-specific introduction and factor-design guidance.

## Assembly

Each agent file contains two blocks: `Agent-Specific Intro` and `Agent-Specific Factor Design Guidance`. Assemble a generation prompt as:

1. `prompts/shared/system_message.md` as the system message.
2. Agent-specific intro, with `{columns_num}`, `{columns_desc}`, `{num_per_request}`, and `{forecast_horizon}` filled.
3. Optional `prompts/shared/effective_factor_analysis.md`, filled with `{effective_CoT}`, when successful prior-factor feedback is available.
4. Optional `prompts/shared/ineffective_factor_analysis.md`, filled with `{ineffective_CoT}`, when failed prior-factor feedback is available.
5. `prompts/shared/requirements.md`.
6. Agent-specific factor-design guidance. Optionally rewrite this block first with `prompts/shared/guidance_paraphrase.md`.
7. `prompts/shared/libraries_and_coding_guidelines.md`.
8. `prompts/shared/output_format.md`.

Use `---` separators between user-message blocks. If no prior feedback is available, skip the effective/ineffective analysis blocks entirely.

## Templates

| Layer | Agent | Template |
| --- | --- | --- |
| Level I - Market Structure and Cycle | Market Cycle | `agent_market_cycle.md` |
| Level I - Market Structure and Cycle | Volatility Regime | `agent_volatility_regime.md` |
| Level II - Extreme Risk and Fragility | Crash Predictor | `agent_crash_predictor.md` |
| Level II - Extreme Risk and Fragility | Tail Risk | `agent_tail_risk.md` |
| Level III - Price-Volume Dynamics | Liquidity | `agent_liquidity.md` |
| Level III - Price-Volume Dynamics | Order Imbalance | `agent_order_imbalance.md` |
| Level III - Price-Volume Dynamics | Price Volume Coherence | `agent_price_volume_coherence.md` |
| Level III - Price-Volume Dynamics | Volume Structure | `agent_volume_structure.md` |
| Level IV - Price-Volatility Behavior | Daily Trend | `agent_daily_trend.md` |
| Level IV - Price-Volatility Behavior | Lag Response | `agent_lag_response.md` |
| Level IV - Price-Volatility Behavior | Range Vol | `agent_range_vol.md` |
| Level IV - Price-Volatility Behavior | Reversal | `agent_reversal.md` |
| Level IV - Price-Volatility Behavior | Vol Asymmetry | `agent_vol_asymmetry.md` |
| Level V - Multi-Scale Complexity | Drawdown | `agent_drawdown.md` |
| Level V - Multi-Scale Complexity | Fractal | `agent_fractal.md` |
| Level V - Multi-Scale Complexity | Herding | `agent_herding.md` |
| Level VI - Stability and Regime-Gating | Regime Gating | `agent_regime_gating.md` |
| Level VI - Stability and Regime-Gating | Stability | `agent_stability.md` |
| Level VII - Geometric and Fusion | Bar Shape | `agent_bar_shape.md` |
| Level VII - Geometric and Fusion | Composite | `agent_composite.md` |
| Level VII - Geometric and Fusion | Creative | `agent_creative.md` |
