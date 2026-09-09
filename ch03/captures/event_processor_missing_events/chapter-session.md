# Publication-ready Chapter 3 captured repair

The broader review is reconstructed. It rebuilds a plausible path from preserved starting and final implementations; it is not a captured multi-stage agent run. Inside that review, the missing-events repair comes from a verified Claude Code 2.1.210.642 capture acting on `event_processor.py`. The original bounded prompt was not retained, so the human contract is reconstructed and labeled.

The inspection, command sequence, exact diff, and green results come from the retained action record and machine-preserved evidence. They support one ask-inspect-adjust turn. The later checkpoint and timezone material extend that turn through reconstructed follow-up work; the capture does not prove those exchanges.

The focused check writes `{"not_events": []}` and requires the exact `ValueError` shown below. It also sends `{"events": []}` through the same function and verifies that the explicit empty list reaches the already-known later arithmetic defect instead of being rejected as missing. The broader check repeats both cases and sends one valid non-empty event through the happy path.

> [!prompt Human contract (reconstructed)]
> Work only on the missing `events` behavior in `event_processor.py`. First run `python3 focused_test.py event_processor.py` and report the result. Then give a one-sentence plan for the smallest reviewable change that fits the surrounding style. Do not edit yet. A missing collection must raise `ValueError` with the stable message `input must be an object with an 'events' key`. An explicit empty list must remain distinct and reach the later empty-result arithmetic, while a valid non-empty input must still work.

> [!ai-response Red result and plan]
> ```
> $ python3 focused_test.py event_processor.py
> FAIL: test_missing_events_collection_raises_value_error
> expected: ValueError: input must be an object with an 'events' key
> observed: KeyError: 'events'
> PASS: test_explicit_empty_events_is_not_missing
> observed: reached later empty-result arithmetic
> 1 failed, 1 passed
> ```
> Plan: add one missing-key guard immediately after `json.load`, leaving every other behavior unchanged.

> [!prompt Approving the bounded repair]
> Apply only that guard. Show the exact diff, then rerun the focused check and `python3 full_capture_check.py event_processor.py`.

The retained capture record predates the restored branch listings and labels
this patch Listing 3.2. The active chapter labels the same patch Listing 3.5;
the diff, commands, outputs, and evidence boundary are unchanged.

Listing 3.2 is the exact applied diff. It changes only the selected missing-key behavior.

Listing 3.2 Missing-events validation guard

```diff
--- a/event_processor.py
+++ b/event_processor.py
@@ -7,6 +7,10 @@
     """Process user events from JSON."""
     f = open(input_path)                  # A
     data = json.load(f)
+    if "events" not in data:
+        raise ValueError(
+            "input must be an object with an 'events' key"
+        )
 
     results = []
     for event in data["events"]:
```

> [!ai-response Focused and broader green checks]
> ```
> $ python3 focused_test.py event_processor.py
> PASS: test_missing_events_collection_raises_value_error
> observed: ValueError: input must be an object with an 'events' key
> PASS: test_explicit_empty_events_is_not_missing
> observed: reached later empty-result arithmetic
> 2 passed
> $ python3 full_capture_check.py event_processor.py
> PASS: test_missing_events_collection_raises_value_error
> PASS: test_explicit_empty_events_is_not_missing
> PASS: test_existing_happy_path_still_works
> 3 passed
> ```

Inspect what the check bought you. The four-line guard is the smallest reviewable change in the function's surrounding style: it names the missing-key branch before the existing loop and keeps the full error message readable without compressing the control flow. The focused result proves the exact missing-key error and discriminates it from an explicit empty list: the empty-list case reaches the already-known later arithmetic defect instead of being rejected as missing. The broader result proves one representative valid non-empty input still produces and writes the expected summary. Neither check proves how non-object JSON, a non-list `events` value, or malformed individual events behave. The checks enforce the selected missing-versus-empty policy; they do not choose it. That decision belongs to the people who own the input contract.
