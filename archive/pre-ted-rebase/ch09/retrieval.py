"""Retrieve evidence with provenance before model generation."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Chunk:
    source_id: str
    updated_at: str
    authority: str
    text: str


def embed(text):
    """Build a deterministic token set for the local example."""
    return frozenset(re.findall(r"[a-z0-9_.]+", text.lower()))


class InMemoryStore:
    """Rank chunks by token overlap and stable input order."""

    def __init__(self, chunks):
        self.chunks = tuple(chunks)

    def nearest(self, query, k=4):
        if k < 0:
            raise ValueError("k must be non-negative")
        ranked = sorted(
            enumerate(self.chunks),
            key=lambda item: (
                -len(query & embed(item[1].text)),
                item[0],
            ),
        )
        return [chunk for _, chunk in ranked[:k]]


def format_evidence(chunk):
    provenance = (
        f"source={chunk.source_id}; "
        f"updated={chunk.updated_at}; "
        f"authority={chunk.authority}"
    )
    return f"[{provenance}]\n{chunk.text}"


def answer(question, store, model):
    query = embed(question)
    chunks = store.nearest(query, k=4)
    evidence = "\n\n".join(
        format_evidence(chunk) for chunk in chunks
    )
    prompt = (
        "Use only this evidence. Cite source labels.\n"
        f"{evidence}\n\nQuestion: {question}"
    )
    return model.complete(prompt)


def recall_at_k(required_source_ids, chunks, k):
    """Measure the fraction of required sources in the top k."""
    required = set(required_source_ids)
    if not required:
        raise ValueError("at least one required source is needed")
    if k < 0:
        raise ValueError("k must be non-negative")
    observed = {chunk.source_id for chunk in chunks[:k]}
    return len(required & observed) / len(required)


def all_required_at_k(required_source_ids, chunks, k):
    """Report whether every required source reached the top k."""
    return recall_at_k(required_source_ids, chunks, k) == 1.0
