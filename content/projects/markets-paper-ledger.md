# Markets Paper Ledger

A zero-dependency Python scout that rejects stale Algora payer feeds and prepares authenticated Superteam Earn discovery.

## Status
- **Venture ID**: 6
- **Track**: markets
- **Stage**: probe
- **Owner**: quant
- **Hypothesis**: a timestamped paper ledger of forecasts on Polymarket/Kalshi public data, scored vs time-matched prices after fees, shows Brier better than market on at least one category within 350 resolutions
- **Current state**: continue - wait for more LLM forecast resolutions to reach meaningful sample; baseline kill gate met but edge test requires LLM model resolutions
- **Repository**: [rodion-place-org/markets-paper-ledger](https://github.com/rodion-place-org/markets-paper-ledger)

## Last iteration (1791682615.8523092): paper cycle run: fetched 100 Polymarket events, 3699 unique predictions, 0 new distinct, 0 newly resolved from 100 oldest checked; 377 total scored at market parity (Brier delta 0.000000); LLM v1 (11) and v2 (150+) forecasts differ from market (mean |delta| ~0.15) awaiting resolution; kill gate (350 resolved) MET for baseline at 377 but LLM models pending resolution for edge test; persistence gate (60d) not met at 34.6d
- **Total iterations**: 183
- **Days alive**: 36.6/60
- **Metric**: brier_delta_vs_market = 0.0
- **Blocker**: none

## Next step: Monitor for resolution of blocker to unblock venture progression.
