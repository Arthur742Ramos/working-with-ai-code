# CH08 Prompts

Prompt blocks extracted from the current manuscript source.

## Self-review against a checklist (illustrative)

````text
Review this proportional allocator as if you had not written
it. Do not summarize what it does. Check four boundaries:
returned shares do not sum to `total`; a weight is zero or
the weights are empty; `total` is zero; and an input raises
instead of returning a list. For each boundary, return only
a concrete failing input or "none found."

Return a short table: case, failing input, expected, actual.
````

## Red-team the split (illustrative)

````text
You are a hostile reviewer trying to make `allocate`
violate its contract: return shares that do not sum to
`total`, crash, or accept a negative input. You get credit
only for an input that actually breaks it. Ignore style and
speed.

Give me your five nastiest inputs, and for each one the
shares you expect and the shares the code returns. Start
with the case you think is most likely to be mishandled.
````

## Keep an exact tie stable

````text
Inspect `allocation.py` and the allocation tests. Run
the exact-tie test before editing, and do not edit until
you have observed the failure and stated a one-sentence
plan. Fix binary-float misordering for ordinary numeric
weights while preserving largest remainder and stable
input-order ties. Add no validation, public interface,
feature flag, or second allocation workflow. Then run
the focused case, the broader suite, and the behavior
plus golden tests.
````
