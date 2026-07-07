# CH08 Prompts

Prompt blocks extracted from the current manuscript source.

## Self-review against a checklist

````text
Review the `allocate` function above as if you did not write it.
Don't summarize what it does. For each item, answer only with a
concrete failing input or "none found":

- An input where the returned shares don't sum to `total`
- An input where a weight is zero, or the weights are empty
- An input where `total` is zero
- Any input that raises instead of returning a list

Return a short table: case, failing input, expected, actual.
````

## Red-team the split

````text
You're a hostile reviewer trying to make `allocate` return shares
that don't sum to `total`, or crash. You get credit only for an
input that actually breaks it. Ignore style and speed.

Give me your five nastiest inputs, and for each one the shares you
expect and the shares the code returns. Start with the case you
think is most likely to be mishandled.
````

## One failing check: the shares do not add up

````text
`allocation.py` has `allocate`, with tests in `test_allocation.py`.
Run `test_pennies_are_conserved`; it's failing. Tell me which input
fails and the one-line cause, then make the smallest change that
passes it without breaking the other tests. Keep the shares
proportional, and don't add features.
````
