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
    assert result is not None          #A
    assert isinstance(result, dict)    #A
    assert "status" in result          #A
