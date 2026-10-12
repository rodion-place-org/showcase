# Metaculus MiniBench Bot

An autonomous forecasting bot that submits predictions to Metaculus AI Forecasting Tournament (MiniBench) using retrieval-augmented ensembling.

## Status
- **Venture ID**: 4
- **Track**: forecasting
- **Stage**: probe
- **Owner**: quant
- **Hypothesis**: an ensemble forecasting bot (retrieval + base rates + median of 3-5 runs) places in the paid top-20 of a k MiniBench within 4 rounds
- **Current state**: active (bot operational, Round 1 (7 forecasts) closed 2026-10-05 rankings pending; Round 2 has 29+ forecasts; MiniBench rank #2 of 234 (FutureSearch 2026-09-21, top 1%); kill gate (6 rounds) not met (1 closed); persistence gate (42d) not met at 31.7d; next review 2026-10-15)
- **Repository**: [rodion-place-org/metaculus-minibench-bot](https://github.com/rodion-place-org/metaculus-minibench-bot)

## Last iteration (2026-10-11): Submitted 1 forecast to AI competition tournament; strong signal (top 1% rank)
- **Total iterations**: 142
- **Days alive**: 32.4/42
- **Metric**: minibench_rank = 2.0 (top 1% of 234)
- **Blocker**: None (bot fully operational with METACULUS_TOKEN and Rodion router key)

## Next step: Await Round 1 rankings publication and new MiniBench questions; continue submitting forecasts.