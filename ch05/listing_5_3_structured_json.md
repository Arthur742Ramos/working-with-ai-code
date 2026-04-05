<!-- Listing 5.3: Requesting structured JSON output

From "Working with AI as a Real Teammate" (Manning)
Chapter 5
-->

Analyze this error log and return a JSON object with:
{
  "root_cause": "one-sentence explanation",
  "affected_components": ["list", "of", "services"],
  "severity": "low | medium | high | critical",
  "suggested_fix": "actionable next step",
  "confidence": "high | medium | low"
}

Error log:
[paste log here]
