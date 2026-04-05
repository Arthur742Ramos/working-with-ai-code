"""Listing 5.2: Using test cases to constrain a function

From "Working with AI as a Real Teammate" (Manning)
Chapter 5
"""

# Write a function that passes these tests:


def test_slugify():
    assert slugify("Hello World") == "hello-world"
    assert slugify("  Multiple   Spaces  ") == "multiple-spaces"
    assert slugify("Special!@#Characters") == "specialcharacters"
    assert slugify("Already-valid") == "already-valid"
    assert slugify("") == ""
