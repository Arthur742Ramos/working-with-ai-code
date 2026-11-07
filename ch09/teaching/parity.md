# Chapter 9 current reader map

This map connects section 9.3's printed source-selection trace with the optional implementation in `retrieval_demo.py`.

| Current printed surface | Local source | Parity boundary |
|---|---|---|
| Three source records and their common date | `retrieval_demo.py`, `chunks` | Same source identifiers, authority labels, text and `2026-07-01` date. The `Chunk` class and formatting helpers are optional implementation details. |
| Query and two-source selection | `retrieval_demo.py`, `question`, `selected`, `required` and `recall` | Same query; both required sources are selected and recall is 1.0. The final assertion requires all needed evidence. Prompt assembly is supplemental; no generation occurs. |
| Suggested k=1 experiment | `test_retrieval_demo.py` temporary copy | Changes only the selection argument. One required source is missing, recall is 0.5 and the final assertion fails. |
| Wider retrieval discussion | Parent `retrieval.py` and `test_retrieval.py` | Maintained extended store/model-interface and recall examples. They are not the current section 9.3 trace and do not implement a production retrieval pipeline. |

The retained implementation's SHA-256 is `fb58606e17fd0caee1f9fa74eadd765fb5b9c317b87991722bdef5b395110084`. The separate teaching test locks these reviewed bytes and checks their behavior without requiring the manuscript repository at runtime.

The parent parity map and capture review retain their earlier scope. Replay uses the archived README; the maintained parent README describes the current package. The original six test modules and capture files are unchanged. The current reader tests are separate from the original 28-test contract; see [the teaching README](README.md) for the explicit commands. The fixed output label in the supplement is not parameterized when the negative test mutates k.
