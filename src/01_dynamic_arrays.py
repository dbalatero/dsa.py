"""Implement DynamicArray[T]: a resizable array backed by a fixed-capacity list.

Requirements:
- Start empty with capacity 4; track size separately from capacity.
- Support len(), integer indexing and assignment (including negative indexes),
  append(value), pop() from the end, iteration, and a useful repr().
- Raise IndexError for invalid indexes and popping an empty array.
- When full, double capacity by allocating new storage and copying elements.
- Use the backing list only for allocation and indexed reads/writes: no append,
  extend, insert, pop, or slicing to resize it.
- Clear removed slots to release references. None is a valid stored value.
- Maintain 0 <= size <= capacity; elements occupy indexes 0 through size - 1.
- Leave shrinking, slicing, arbitrary insertion/deletion, and MutableSequence
  inheritance for later.

Target complexity:
Operation                 | Time
len, get/set by index, pop | O(1)
append                    | O(1) amortized; O(n) when resizing
iteration, str           | O(n)

Backing storage uses O(capacity) space.

Run: python src/01_dynamic_arrays.py
Test only: python -m pytest src/01_dynamic_arrays.py

See README.md for the workflow.
"""

import sys
from collections.abc import Iterator
from typing import cast

import pytest


# Implementation: replace this with the structure you are learning.
class DynamicArray[T]:
    def __init__(self, capacity: int = 10) -> None:
        if capacity < 1:
            raise ValueError("capacity must be greater than 0")

        self.capacity = capacity
        self.size = 0
        self.data: list[T | None] = [None] * capacity

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        return f"<DynamicArray size={self.size}, capacity={self.capacity}, items={repr(list(self))}>"

    def __iter__(self) -> Iterator[T]:
        i = 0
        while i < self.size:
            value = self.data[i]
            yield cast(T, value)

            i += 1

    def __getitem__(self, index: int) -> None | T:
        return self.data[self._normalized_index(index)]

    def __setitem__(self, index: int, value: T) -> None:
        self.data[self._normalized_index(index)] = value

    def append(self, value: T) -> None:
        if self.size == self.capacity:
            self._resize(self.capacity * 2)

        self.data[self.size] = value
        self.size += 1

    def pop(self) -> None | T:
        if self.size == 0:
            raise IndexError(f"The list is empty")

        index = self.size - 1
        value = self.data[index]

        self.data[index] = None
        self.size -= 1

        return value

    def _normalized_index(self, index: int) -> int:
        if index >= 0:
            if index >= self.size:
                raise IndexError(f"{index} is out of bounds of size {self.size}")

            return index
        else:
            normalized = self.size + index
            if normalized < 0:
                raise IndexError(f"{index} is out of bounds - resolves to {normalized}")

            return normalized

    def _resize(self, new_capacity: int) -> None:
        new_data: list[T | None] = [None] * new_capacity

        # Copy values over
        for i, value in enumerate(self.data):
            new_data[i] = value

        self.data = new_data
        self.capacity = new_capacity


# Tests live alongside the implementation; importing the module won't run them.
def test_insert_size() -> None:
    array = DynamicArray[int]()
    array.append(1)
    assert len(array) == 1


def test_capacity_fails_zero() -> None:
    with pytest.raises(ValueError):
        DynamicArray[int](0)


def test_resizing() -> None:
    array = DynamicArray[int](1)
    array.append(1)
    array.append(2)

    assert list(iter(array)) == [1, 2]
    assert len(array) == 2
    assert array.capacity == 2


def test_pop() -> None:
    array = DynamicArray[int]()
    array.append(1)
    array.append(2)

    assert list(iter(array)) == [1, 2]
    assert len(array) == 2

    assert array.pop() == 2
    assert list(iter(array)) == [1]
    assert len(array) == 1


def test_str() -> None:
    array = DynamicArray[int]()
    array.append(1)
    array.append(2)
    array.append(3)

    assert str(array) == "<DynamicArray size=3, capacity=10, items=[1, 2, 3]>"


def test_negative_indexing_is_correct() -> None:
    array = DynamicArray[int](10)
    array.append(1)
    array.append(2)
    array.append(3)

    assert array[-1] == 3


def test_empty_pop_raises_index_error():
    array = DynamicArray[int]()
    with pytest.raises(IndexError):
        array.pop()


@pytest.mark.parametrize("index", [-3, -2, -1])
def test_negative_get_set_matches_list(index: int) -> None:
    expected = [1, 2, 3]
    array = DynamicArray[int](10)
    for value in expected:
        array.append(value)

    assert array[index] == expected[index]
    array[index] = 99
    expected[index] = 99
    assert list(array) == expected
    assert len(array) == 3


@pytest.mark.parametrize("values", [[], [1], [1, 2, 3]])
def test_negative_out_of_bounds_leaves_array_unchanged(values: list[int]) -> None:
    array = DynamicArray[int](10)
    for value in values:
        array.append(value)

    index = -len(values) - 1
    with pytest.raises(IndexError):
        _ = array[index]
    with pytest.raises(IndexError):
        array[index] = 99

    assert list(array) == values
    assert len(array) == len(values)


def test_negative_indexing_after_resize_and_pop() -> None:
    array = DynamicArray[int](2)
    for value in [1, 2, 3]:
        array.append(value)

    assert array[-1] == 3
    assert array[-3] == 1
    array.pop()

    assert array[-1] == 2
    assert array[-2] == 1
    with pytest.raises(IndexError):
        _ = array[-3]
    with pytest.raises(IndexError):
        array[-3] = 99

    array[-1] = 20
    assert list(array) == [1, 20]


def test_iteration() -> None:
    array = DynamicArray[int]()
    array.append(1)
    array.append(2)
    array.append(3)

    iterator = iter(array)
    assert next(iterator) == 1
    assert next(iterator) == 2
    assert next(iterator) == 3


def test_get_set() -> None:
    array = DynamicArray[int]()
    array.append(1)
    array.append(2)
    array.append(3)

    assert list(array) == [1, 2, 3]

    array[1] = 10
    assert list(array) == [1, 10, 3]
    assert array[2] == 3


def test_get_set_out_of_bounds() -> None:
    array = DynamicArray[int]()
    array.append(1)
    array.append(2)

    with pytest.raises(IndexError):
        array[2] = 100

    with pytest.raises(IndexError):
        print(array[2])


if __name__ == "__main__":
    # Forward options such as -q or -k; propagate pytest's exit code on failure.
    raise SystemExit(pytest.main([__file__, *sys.argv[1:]]))
