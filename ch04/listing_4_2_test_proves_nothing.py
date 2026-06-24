"""Listing 4.2: A test that passes but proves nothing useful

From "Working with AI as a Real Teammate" (Manning)
Chapter 4
"""


def test_process_order():
    """Test order processing."""
    order = {
        "id": 1,
        "items": [
            {"name": "Widget", "price": 9.99}
        ],
        "status": "pending"
    }
    result = process_order(order)
    assert result is not None
    assert isinstance(result, dict)
    assert "status" in result
