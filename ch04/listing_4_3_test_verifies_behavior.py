"""Listing 4.3 A test that verifies behavior."""

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
    assert result["status"] == "completed"  # Checks the specific status expected
    assert result["total"] == 24.98         # Verifies the total is the sum of item prices
    assert result["item_count"] == 2        # Confirms all items were counted
