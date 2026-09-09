def sample_order():
    return {"prices": [12.49, 12.49]}


def process_order(order):
    return {"status": "error", "total": 0,
            "item_count": 0}


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
