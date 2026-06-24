"""Listing 4.3: A test that verifies behavior

From "Working with AI as a Real Teammate" (Manning)
Chapter 4
"""


def test_process_order_calculates_total():
    """Test that processing sums item prices."""
    order = {
        "id": 1,
        "items": [
            {"name": "Widget", "price": 9.99},
            {"name": "Gadget", "price": 14.99}
        ],
        "status": "pending"
    }
    result = process_order(order)
    assert result["status"] == "completed"
    assert result["total"] == 24.98
    assert result["item_count"] == 2
