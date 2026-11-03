from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Chunk:
    source_id: str
    updated_at: str
    authority: str
    text: str


def terms(text):
    return set(re.findall(r"[a-z0-9_.]+", text.lower()))


def retrieve(question, chunks, k):
    query = terms(question)
    return sorted(
        chunks,
        key=lambda chunk: -len(query & terms(chunk.text)),
    )[:k]


def format_evidence(chunk):
    label = (
        f"source={chunk.source_id}; "
        f"updated={chunk.updated_at}; "
        f"authority={chunk.authority}"
    )
    return f"[{label}]\n{chunk.text}"

chunks = [
    Chunk("rule-current", "2026-07-01", "approved",
          "Outbound HTTP uses http_client.call."),
    Chunk("client-current", "2026-07-01", "source",
          "http_client.call accepts method, url, json."),
    Chunk("unrelated", "2026-07-01", "approved",
          "Database migration notes."),
]
question = "How does http_client.call send HTTP?"
selected = retrieve(question, chunks, k=2)
required = {"rule-current", "client-current"}
observed = {chunk.source_id for chunk in selected}
recall = len(required & observed) / len(required)
evidence = "\n\n".join(map(format_evidence, selected))
prompt = (
    "Use this evidence and cite source labels.\n"
    f"{evidence}\n\nQuestion: {question}"
)
print([chunk.source_id for chunk in selected])
print(f"required-source recall@2: {recall:.1f}")
assert required <= observed
