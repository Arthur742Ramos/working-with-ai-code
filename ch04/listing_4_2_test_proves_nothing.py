"""Listing 4.2 A test that passes but proves nothing useful."""

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
    assert result is not None          # These assertions are nearly useless —
    assert isinstance(result, dict)    # they pass for almost any return value
    assert "status" in result          # they pass for almost any return value
