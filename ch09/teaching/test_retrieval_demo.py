"""Retrieval-supplement checks, separate from the historical capture suite."""

import hashlib
from pathlib import Path
import runpy
import subprocess
import sys


DEMO = Path(__file__).with_name("retrieval_demo.py")
# Retained implementation now supplements the section 9.3 source-selection trace.
PRINTED_SHA256 = (
    "fb58606e17fd0caee1f9fa74eadd765fb5b9c317b87991722bdef5b395110084"
)


def test_file_matches_the_reviewed_printed_listings():
    assert hashlib.sha256(DEMO.read_bytes()).hexdigest() == PRINTED_SHA256


def test_printed_demo_selects_both_required_sources():
    result = subprocess.run(
        [sys.executable, "-I", "-B", str(DEMO)],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == (
        "['rule-current', 'client-current']\n"
        "required-source recall@2: 1.0\n"
    )
    assert result.stderr == ""


def test_k_one_fails_the_required_source_assertion(tmp_path):
    source = DEMO.read_text(encoding="utf-8")
    selected = "selected = retrieve(question, chunks, k=2)"
    assert source.count(selected) == 1
    negative = tmp_path / "retrieval_demo_k_one.py"
    negative.write_text(
        source.replace(selected, selected.replace("k=2", "k=1")),
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, "-I", "-B", str(negative)],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 1
    # Only k is mutated; the supplement's fixed display label is unchanged.
    assert result.stdout == (
        "['rule-current']\nrequired-source recall@2: 0.5\n"
    )
    assert "assert required <= observed" in result.stderr
    assert result.stderr.rstrip().endswith("AssertionError")


def test_ties_preserve_input_order_and_prompt_keeps_labels(capsys):
    demo = runpy.run_path(str(DEMO))
    capsys.readouterr()
    chunk = demo["Chunk"]
    tied = [
        chunk("first", "2026-07-01", "source", "same"),
        chunk("second", "2026-07-01", "source", "same"),
    ]
    assert demo["retrieve"]("same", tied, 2) == tied
    assert demo["observed"] == demo["required"]
    for source_id in ("rule-current", "client-current"):
        assert f"source={source_id}; updated=2026-07-01;" in demo["prompt"]
    assert demo["prompt"].endswith(
        "Question: How does http_client.call send HTTP?"
    )
