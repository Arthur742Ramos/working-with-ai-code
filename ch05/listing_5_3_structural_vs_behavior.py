"""Listing 5.3: Structural assertions versus behavior assertions

From "Working with AI as a Real Teammate" (Manning)
Chapter 5

Excerpt: `process_order` and `sample_order` are defined in the order module
under diagnosis.
"""

def test_order_shape():
    result = process_order(sample_order())
    assert result is not None
    assert isinstance(result, dict)
    assert "status" in result


def test_order_behavior():
    result = process_order(sample_order())
    assert result["status"] == "completed"
    assert result["total"] == 24.98
    assert result["item_count"] == 2
