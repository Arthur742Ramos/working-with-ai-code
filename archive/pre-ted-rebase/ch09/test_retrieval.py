"""Checks for provenance, selection, injection, and recall."""

import pytest

from retrieval import Chunk, InMemoryStore, answer
from retrieval import all_required_at_k, format_evidence, recall_at_k


class RecordingModel:
    def __init__(self):
        self.prompts = []

    def complete(self, prompt):
        self.prompts.append(prompt)
        return "grounded answer"


def chunk(source_id, text, authority="approved"):
    return Chunk(
        source_id=source_id,
        updated_at="2026-07-01",
        authority=authority,
        text=text,
    )


def test_format_evidence_preserves_provenance():
    evidence = format_evidence(
        chunk("house-rule", "Use http_client.call.")
    )

    assert evidence == (
        "[source=house-rule; updated=2026-07-01; "
        "authority=approved]\nUse http_client.call."
    )


def test_answer_retrieves_then_injects_selected_chunks():
    store = InMemoryStore([
        chunk("unrelated", "Database migration notes."),
        chunk("client", "http_client.call accepts JSON."),
        chunk("rule", "Outbound HTTP uses http_client.call."),
    ])
    model = RecordingModel()

    result = answer("How does http_client.call send JSON?", store, model)

    assert result == "grounded answer"
    prompt = model.prompts[0]
    assert prompt.startswith(
        "Use only this evidence. Cite source labels.\n"
        "[source=client;"
    )
    assert "[source=rule;" in prompt
    assert prompt.endswith(
        "Question: How does http_client.call send JSON?"
    )


def test_answer_caps_retrieval_at_four_chunks():
    store = InMemoryStore([
        chunk(str(index), "shared term")
        for index in range(6)
    ])
    model = RecordingModel()

    answer("shared term", store, model)

    assert model.prompts[0].count("[source=") == 4


def test_recall_at_k_separates_partial_and_complete_retrieval():
    ranked = [
        chunk("rule", "rule"),
        chunk("noise", "noise"),
        chunk("client", "client"),
    ]

    assert recall_at_k({"rule", "client"}, ranked, 2) == 0.5
    assert all_required_at_k(
        {"rule", "client"}, ranked, 2
    ) is False
    assert recall_at_k({"rule", "client"}, ranked, 3) == 1.0
    assert all_required_at_k(
        {"rule", "client"}, ranked, 3
    ) is True


def test_recall_requires_labeled_evidence():
    with pytest.raises(ValueError, match="at least one required"):
        recall_at_k(set(), [], 4)
