"""Listing 4.6: Property-based testing for AI-generated code

From "Working with AI as a Real Teammate" (Manning)
Chapter 4
"""

from hypothesis import given, settings
from hypothesis import strategies as st


@given(
    price=st.decimals(
        min_value=0,
        max_value=10000,
        places=2
    ),
    rate=st.decimals(
        min_value=0,
        max_value=1,
        places=4
    )
)
@settings(max_examples=500)
def test_tax_is_never_negative(
    price, rate
):
    """Tax should never be negative."""
    result = calculate_tax(
        float(price), float(rate)
    )
    assert result >= 0


@given(
    price=st.decimals(
        min_value=0,
        max_value=10000,
        places=2
    )
)
def test_zero_rate_means_zero_tax(price):
    """Zero tax rate means zero tax."""
    result = calculate_tax(
        float(price), 0.0
    )
    assert result == 0.0
