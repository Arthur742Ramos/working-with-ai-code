# Independent canonical capture review

## Certification

Verdict: **PASS**

No blocking capture, replay, parity, isolation, minimality, provenance, or policy-boundary defect was found. This record certifies the final normalized Chapter 1 fallback-observability package after the earlier repair review described in `session.md`.

## Attribution

- Reviewer role: Independent canonical capture reviewer
- Reviewer tool: Claude Code CLI 2.1.210.814
- Reviewer model: `gpt-5.6-sol[1m]`
- Review date: 2026-07-15
- Method: Read-only repository review in a clean disposable copy
- Repository modified by reviewer: No
- Attribution limit: The reviewer identity and tool version are package-attributed rather than cryptographically proven because raw vendor session logs are not retained. The capture standard permits the disclosed reconstruction.

## Reviewed authorities

The reviewer checked the real-session capture standard, active restructuring architecture, session ledger, canonical package, canonical chapter source, and restructuring chapter source. The two Chapter 1 Markdown sources were byte-identical with SHA-256 `9e8f4abc01203db88c3b111bd5459c41a7164f499cd6d1512535516898d36034`.

## Principal commands

The commands below preserve the reviewed operations while using package-local variables for the disposable paths.

```bash
REPO_ROOT=<repository-root>
REVIEW_ROOT=/tmp/ch01-canonical-review.<id>
PACKAGE="$REVIEW_ROOT/ch01"

rsync -a \
  --exclude='.venv/' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  "$REPO_ROOT/code/ch01/" \
  "$PACKAGE/"

python3 -m venv "$PACKAGE/.venv"
"$PACKAGE/.venv/bin/python" -m pip install \
  -r "$PACKAGE/requirements.txt"
"$PACKAGE/.venv/bin/python" \
  "$PACKAGE/captures/fallback_observability/run_capture.py"

"$PACKAGE/.venv/bin/python" "$PACKAGE/tests/focused_test.py"
"$PACKAGE/.venv/bin/python" "$PACKAGE/tests/broader_test.py"
```

The reviewer also reproduced the state transition manually.

```bash
mkdir -p "$REVIEW_ROOT/manual"
cp "$PACKAGE/captures/fallback_observability/before/app.py" \
  "$REVIEW_ROOT/manual/app.py"

"$PACKAGE/.venv/bin/python" \
  "$PACKAGE/captures/fallback_observability/tests/focused_test.py" \
  "$REVIEW_ROOT/manual/app.py"

patch -d "$REVIEW_ROOT/manual" -p1 \
  -i "$PACKAGE/captures/fallback_observability/patches/production.diff"

"$PACKAGE/.venv/bin/python" \
  "$PACKAGE/captures/fallback_observability/tests/focused_test.py" \
  "$REVIEW_ROOT/manual/app.py"
"$PACKAGE/.venv/bin/python" \
  "$PACKAGE/captures/fallback_observability/tests/broader_test.py" \
  "$REVIEW_ROOT/manual/app.py"
```

Isolation and printed-command checks ran from unrelated working directories.

```bash
env -C /tmp \
  "$PACKAGE/.venv/bin/python" \
  "$PACKAGE/captures/fallback_observability/run_capture.py"

env -C "$PACKAGE" .venv/bin/python tests/focused_test.py app.py
env -C "$PACKAGE" .venv/bin/python tests/broader_test.py app.py
```

Historical provenance was checked with `hashlib.sha256` over every metadata-declared path and these Git operations.

```bash
git -C "$REPO_ROOT" cat-file -e \
  '38da4cbd91cc22da2687f5c76b8e5c5f93ab44d6^{commit}'
git -C "$REPO_ROOT" show \
  '38da4cbd91cc22da2687f5c76b8e5c5f93ab44d6:<declared-path>'
```

## Results

| Check | Result |
|---|---|
| Non-recording replay | Exit 0 |
| Focused red | Exit 1, as required |
| Patch application | Exit 0 |
| Focused green | Exit 0 |
| Broader green | Exit 0 |
| Top-level package scripts | 2 of 2 passed |
| Printed chapter commands | 2 of 2 passed |
| Python compilation | Exit 0 |
| Stored evidence unchanged | Yes |
| Replay `.work` cleanup | Passed |
| Replay from unrelated working directory | Exit 0 |
| Embedded input and evidence hashes | All matched |
| Deliberate checksum tampering | 4 of 4 mutations rejected |
| Historical canonical hashes | 8 of 8 declarations matched the commit |
| Normalization-origin hashes | 4 of 4 matched the historical package |
| Repository source unchanged | Yes |
| Disposable-copy cleanup | Passed |

The focused red observed zero application-logger fallback warnings while retaining the neighboring request statuses. The focused green observed one fallback warning on `app.logger` with those statuses unchanged. The broader green observed zero fallback warnings on healthy storage with neighboring statuses unchanged.

Runtime matched metadata: Python 3.14.6, Flask 3.1.3, Flask-Limiter 4.1.1, Flask-Login 0.6.3, and redis-py 8.0.1.

## Minimality

The complete machine diff contains one hunk and one added production line:

```python
limiter.logger = app.logger
```

The zero-line before state fails. The one-line state passes focused and broader checks and is byte-identical to `after/app.py`. No smaller non-empty patch exists.

Abstract syntax tree comparison confirmed that `user_key()`, Redis storage configuration, `in_memory_fallback_enabled=True`, and `@limiter.limit("10 per minute")` remain unchanged. The rejected subclass duplicated transition detection and depended on private `_storage_dead` state. The accepted assignment is the smaller reviewable implementation.

## Printed parity

Listing 1.1's selected executable abstract syntax tree matches `before/app.py` after intentional excerpting and line wrapping. The listing also omits the helper function docstring; `parity.md` now records that omission explicitly. Listings 1.2 through 1.4 match the stored red evidence, accepted line, focused green evidence, and broader green evidence. Both printed commands run from the package root.

No internal `code/ch01`, capture, restructuring-support, or retired `rate_limiting/` path appears in reader-facing prose. The reconstructed first contract is disclosed rather than presented as verbatim.

## Provenance

Commit `38da4cbd91cc22da2687f5c76b8e5c5f93ab44d6` exists. All recorded historical canonical hashes match that commit. Original before, after, requirements, and patch hashes match the retained historical package. Metadata records original and normalized hashes separately. Commands, exits, outputs, patch, commit, and source states are independently reproducible.

## Policy boundary

The package retains bounded fail-open overload protection and adds application-owned fallback observability. Humans still own monitoring backend selection, alert and paging thresholds, recovery and escalation policy, whether one warning per transition is operationally sufficient, and multi-process behavior and shared Redis-counter validation.

The checks do not prove live Redis recovery, multi-process behavior, delivery to a metrics or paging backend, or compatibility with a future Flask-Limiter warning contract. The assignment routes all Flask-Limiter log records through the application logger, not only the tested fallback warning. That observability scope does not alter rate-limit policy.

## Isolation

Replay succeeded from `/tmp` without repository-root context. The disposable package contained neither the retired Chapter 1 support tree nor the restructuring support tree. Historical paths occurred only in metadata, session, and parity records; no executable Python file resolves them.

## Final certification

**PASS**
