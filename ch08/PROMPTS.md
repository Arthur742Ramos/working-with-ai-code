# CH08 Prompts

Prompt blocks extracted from the current manuscript source.

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
