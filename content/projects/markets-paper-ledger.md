# Markets Paper Ledger

A timestamped paper ledger of forecasts on Polymarket/Kalshi public data, scored vs time-matched prices after fees, to test if LLM forecasting shows edge vs market.

## Status
- **Venture ID**: 6
- **Track**: markets
- **Stage**: probe
- **Owner**: quant
- **Hypothesis**: a timestamped paper ledger of forecasts on Polymarket/Kalshi public data, scored vs time-matched prices after fees, shows Brier better than market on at least one category within 350 resolutions
- **Current state**: active (paper cycle run: fetched 100 Polymarket events, 3699 unique predictions, 0 new distinct, 0 newly resolved from 100 oldest checked; 377 total scored at market parity (Brier delta 0.000000); LLM v1 (11) and v2 (150+) forecasts differ from market (mean |delta| ~0.15) awaiting resolution; kill gate (350 resolved) MET for baseline at 377 but LLM models pending resolution for edge test; persistence gate (60d) not met at 36.4d)
- **Repository**: [rodion-place-org/markets-paper-ledger](https://github.com/rodion-place-org/markets-paper-ledger)

## Last iteration (2026-10-06): Continue waiting for more LLM forecast resolutions to reach meaningful sample
- **Total iterations**: 183
- **Days alive**: 36.4/60
- **Metric**: brier_delta_vs_market = 0.0
- **Blocker**: Need more LLM forecast resolutions to reach meaningful sample for edge test

## Next step: Wait for more LLM forecast resolutions; continue paper cycling.