# CH02 Prompts

Prompt blocks extracted from the current manuscript source.

## Ask for a PR description

````text
Write a PR description for this diff:

[a staged validation diff]
````

## Constrained code generation

````text
Write a Python function to validate email addresses.

Use Python 3.11 and the standard library only. Return a
dataclass with `is_valid`, `reason`, and
`normalized_address` fields. For valid addresses, trim
surrounding whitespace and lowercase the domain. Handle an
empty string, a missing `@`, and multiple `@` symbols
explicitly. Raise `ValueError` for non-string input.
````

## Requesting structured error analysis

````text
Analyze this error log and return a JSON object with exactly these fields:

```json
{
  "root_cause": "one-sentence explanation",
  "affected_components": ["list", "of", "services"],
  "severity": "low | medium | high | critical",
  "suggested_fix": "actionable next step",
  "confidence": "high | medium | low"
}
```

Error log:
[paste log here]
````

## Inspect the retry wiring

````text
The CLI appears to bypass the existing conversational retry path after malformed structured output. Inspect `pr_generator.py` and the focused test. Run a discriminating red check, state the strict smallest-change plan, and identify the retry policy a human must own. Do not edit production code yet.
````

## Apply the bounded repair

````text
Reuse the existing helper unchanged. Retry JSON and schema failures, allow two retries for three attempts total, and apply the strict smallest production diff. Then run the focused check and the broader neighboring checks.
````
