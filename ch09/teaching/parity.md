# Chapter 9 current reader listing map

This supplement maps the current printed retrieval example, not the earlier staged package's historical capture. Source: the reviewed 3P manuscript.

| Current printed surface | Local source | Parity boundary |
|---|---|---|
| Listing 9.4 Keep source labels beside searchable text | `retrieval_demo.py`, through `format_evidence` | Exact printed `Chunk`, tokenization, stable lexical ranking and label formatting. |
| Listing 9.5 Select evidence and measure required-source recall | Remaining `retrieval_demo.py` statements | Exact three records, top-two selection, prompt assembly, printed result and all-required-source assertion. No generation occurs. |
| Suggested k=1 experiment | `test_retrieval_demo.py` temporary copy | Changes only the selection argument. One required source is missing, recall is 0.5 and the final assertion fails. |
| Wider retrieval discussion | Parent `retrieval.py` and `test_retrieval.py` | Maintained extended store/model-interface and recall examples. They are not the printed Listings 9.4–9.5 and do not implement a production retrieval pipeline. |

The two Python fences are concatenated in printed order with one blank line and a final newline. The resulting file SHA-256 is `fb58606e17fd0caee1f9fa74eadd765fb5b9c317b87991722bdef5b395110084`. The separate teaching test locks these reviewed bytes and checks their behavior without requiring the manuscript repository at runtime.

The parent parity map, parent README, original six test modules and all capture files remain checksum-locked historical records. Their previous review covers their recorded scope, not this supplement. The current reader tests are separate from the original 28-test contract; see [the teaching README](README.md) for the explicit commands. The fixed output label in the printed file is not parameterized when the negative test mutates k.
