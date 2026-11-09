"""A runnable template: implementation above, pytest tests below.

Run: python src/01_dynamic_arrays.py
Test only: python -m pytest src/01_dynamic_arrays.py

Operation | Time | Extra space
greet     | O(n) | O(n), where n is the length of name

See README.md for the workflow.
"""

import sys

import pytest


# Implementation: replace this with the structure you are learning.
def greet(name: str = "world") -> str:
    return f"Hello, {name}!"


# Tests live alongside the implementation; importing the module won't run them.
def test_default_greeting() -> None:
    assert greet() == "Hello, world!"


def test_empty_name() -> None:
    assert greet("") == "Hello, !"


if __name__ == "__main__":
    # Forward options such as -q or -k; propagate pytest's exit code on failure.
    raise SystemExit(pytest.main([__file__, *sys.argv[1:]]))
