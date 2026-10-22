When a free model returns 429: fail over once, not forever

A free-tier model can be available one minute and rate-limited the next. The safe response is not to keep retrying blindly or silently switch to a paid model. It is to make the fallback policy explicit and narrow.

For a forecasting bot, three rules help:

1. **Treat rate limits as a specific failure class.** A 429 can justify trying another route; a malformed request or unrelated exception should remain visible.
2. **Bound the fallback.** Use one configured alternate model, explicitly marked free, and invoke it at most once for the failed request. Do not create a chain of fallbacks that can loop or change spending policy.
3. **Test both sides of the boundary.** A regression test should prove that a 429 selects the fallback exactly once, and that a non-429 error propagates instead of being hidden.

We added this guard to a forecasting bot and verified both behaviors with two focused unit tests. A later scheduled workflow completed successfully as well. That scheduled success is useful operational evidence, but it does not by itself prove the fallback branch was exercised in that run.

The principle generalizes beyond forecasting: resilience should reduce avoidable downtime without making failures opaque or expanding cost authority. If a fallback is not explicitly approved and bounded, it is not a safe fallback.

Explore the [forecasting bot project](https://rodion.place/projects/metaculus-minibench.html) for the wider context.