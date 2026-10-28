import pytest

from validate_bst import Node, is_valid_bst


def make_example_tree():
    root = Node(8)
    root.left = Node(3)
    root.right = Node(10)
    root.left.left = Node(1)
    root.left.right = Node(6)
    root.left.right.left = Node(4)
    root.left.right.right = Node(7)
    root.right.right = Node(14)
    root.right.right.left = Node(13)
    return root


def test_empty_tree():
    assert is_valid_bst(None) is True


def test_single_node():
    assert is_valid_bst(Node(0)) is True


def test_valid_tree():
    root = make_example_tree()
    assert is_valid_bst(root) is True


def test_invalid_left_child():
    root = Node(8)
    root.left = Node(10)
    assert is_valid_bst(root) is False


def test_invalid_right_child():
    root = Node(8)
    root.right = Node(3)
    assert is_valid_bst(root) is False


def test_ancestor_lower_bound_violation():
    root = Node(8)
    root.right = Node(10)
    root.right.left = Node(6)
    assert is_valid_bst(root) is False


def test_ancestor_upper_bound_violation():
    root = Node(8)
    root.left = Node(3)
    root.left.right = Node(9)
    assert is_valid_bst(root) is False


def test_nontrivial_ancestor_violation():
    # Этот пример для визуализации
    root = make_example_tree()
    root.right.right.left.value = 9
    assert is_valid_bst(root) is False


def test_duplicate_on_right():
    root = Node(8)
    root.right = Node(8)
    assert is_valid_bst(root) is True


def test_duplicate_on_left():
    root = Node(8)
    root.left = Node(8)
    assert is_valid_bst(root) is False


def test_ancestor_duplicate_in_right_subtree():
    root = Node(8)
    root.right = Node(10)
    root.right.left = Node(8)
    assert is_valid_bst(root) is True


def test_ancestor_duplicate_in_left_subtree():
    root = Node(8)
    root.left = Node(3)
    root.left.right = Node(8)
    assert is_valid_bst(root) is False


def test_negative_values_and_zero():
    root = Node(0)
    root.left = Node(-3)
    root.right = Node(4)
    root.left.left = Node(-5)
    root.left.right = Node(-1)
    root.right.left = Node(2)
    assert is_valid_bst(root) is True


def test_all_values_equal_on_right():
    root = Node(5)
    root.right = Node(5)
    root.right.right = Node(5)
    root.right.right.right = Node(5)
    assert is_valid_bst(root) is True


def test_long_right_chain():
    root = Node(0)
    current = root
    for value in range(1, 200):
        current.right = Node(value)
        current = current.right
    assert is_valid_bst(root) is True


def test_long_left_chain():
    root = Node(199)
    current = root
    for value in range(198, -1, -1):
        current.left = Node(value)
        current = current.left
    assert is_valid_bst(root) is True


def test_violation_at_end_of_chain():
    root = Node(0)
    current = root
    for value in range(1, 200):
        current.right = Node(value)
        current = current.right
    current.value = -1
    assert is_valid_bst(root) is False


def test_large_integer_values():
    value = 10 ** 100
    root = Node(value)
    root.left = Node(value - 1)
    root.right = Node(value + 1)
    assert is_valid_bst(root) is True


def test_repeated_calls_are_independent():
    valid = make_example_tree()
    invalid = Node(8)
    invalid.left = Node(10)

    assert is_valid_bst(valid) is True
    assert is_valid_bst(invalid) is False
    assert is_valid_bst(None) is True
    assert is_valid_bst(valid) is True
    assert is_valid_bst(invalid) is False


def test_validation_does_not_change_tree():
    root = make_example_tree()

    def snapshot(node):
        if node is None:
            return None
        return (id(node), node.value, snapshot(node.left), snapshot(node.right))

    before = snapshot(root)
    assert is_valid_bst(root) is True
    assert snapshot(root) == before

    root.right.right.left.value = 9
    before = snapshot(root)
    assert is_valid_bst(root) is False
    assert snapshot(root) == before


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
