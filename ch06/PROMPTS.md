# CH06 Prompts

Prompt blocks extracted from the current manuscript source.

## Independent tester handoff

````text
Act as the independent tester at the handoff from tester to implementer.
Verify one bounded behavior: when a schema requires `int`, Python `True`
must not be accepted as a valid integer. Inspect `validator.py` and the
focused test, run the focused test against the before state, report the
observed result, and propose the strict smallest implementation change in
one sentence. Do not edit the implementation before observing red.
````

## Implementer handoff

````text
Standing direction: choose the best bounded implementation without another
approval checkpoint. Replay the genuine red first. Select and state the schema
behavior that best preserves the distinct Boolean type, apply the strict
smallest production diff only to the disposable after state, then run the
focused test and the broader validator suite. Do not broaden the behavior.
````
