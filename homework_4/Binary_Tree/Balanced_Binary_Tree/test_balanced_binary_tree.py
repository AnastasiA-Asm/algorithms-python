import pytest

from balanced_binary_tree import Node, is_balanced


def make_balanced_tree():
    root = Node(10)
    root.left = Node(5)
    root.right = Node(15)
    root.left.left = Node(3)
    root.left.right = Node(7)
    root.left.left.left = Node(1)
    root.right.left = Node(12)
    root.right.right = Node(18)
    return root


def make_inner_violation_tree():
    root = Node(8)
    root.left = Node(3)
    root.left.left = Node(1)
    root.left.left.left = Node(0)
    root.right = Node(10)
    root.right.right = Node(14)
    return root


def test_empty_tree():
    assert is_balanced(None) is True


def test_single_node():
    assert is_balanced(Node(8)) is True


def test_one_left_child():
    root = Node(8)
    root.left = Node(3)
    assert is_balanced(root) is True


def test_one_right_child():
    root = Node(8)
    root.right = Node(10)
    assert is_balanced(root) is True


def test_perfect_tree():
    root = Node(8)
    root.left = Node(3)
    root.right = Node(10)
    root.left.left = Node(1)
    root.left.right = Node(6)
    root.right.left = Node(9)
    root.right.right = Node(14)
    assert is_balanced(root) is True


def test_balanced_tree_with_different_heights():
    root = make_balanced_tree()
    assert is_balanced(root) is True


def test_left_height_difference_two():
    root = Node(8)
    root.left = Node(3)
    root.left.left = Node(1)
    assert is_balanced(root) is False


def test_right_height_difference_two():
    root = Node(8)
    root.right = Node(10)
    root.right.right = Node(14)
    assert is_balanced(root) is False


def test_nontrivial_inner_violation():
    # Этот пример для визуализации
    root = make_inner_violation_tree()
    assert is_balanced(root) is False


def test_inner_violation_on_right():
    root = Node(8)
    root.left = Node(3)
    root.left.left = Node(1)
    root.right = Node(10)
    root.right.right = Node(14)
    root.right.right.right = Node(15)
    assert is_balanced(root) is False


def test_equal_root_heights_with_inner_violation():
    root = make_inner_violation_tree()
    root.right.right.right = Node(15)
    assert is_balanced(root) is False


def test_balanced_tree_not_bst():
    root = Node(5)
    root.left = Node(100)
    root.right = Node(2)
    assert is_balanced(root) is True


def test_balanced_tree_with_equal_values():
    root = Node(5)
    root.left = Node(5)
    root.right = Node(5)
    assert is_balanced(root) is True


def test_unbalanced_tree_with_equal_values():
    root = Node(5)
    root.left = Node(5)
    root.left.left = Node(5)
    assert is_balanced(root) is False


def test_negative_values_and_zero():
    root = Node(0)
    root.left = Node(-10)
    root.right = Node(-2)
    assert is_balanced(root) is True


def test_long_left_chain():
    root = Node(0)
    current = root
    for value in range(1, 200):
        current.left = Node(value)
        current = current.left
    assert is_balanced(root) is False


def test_long_right_chain():
    root = Node(0)
    current = root
    for value in range(1, 200):
        current.right = Node(value)
        current = current.right
    assert is_balanced(root) is False


def test_large_perfect_tree():
    nodes = [Node(value) for value in range(255)]
    for index in range(len(nodes)):
        left = 2 * index + 1
        right = 2 * index + 2
        if left < len(nodes):
            nodes[index].left = nodes[left]
        if right < len(nodes):
            nodes[index].right = nodes[right]
    assert is_balanced(nodes[0]) is True


def test_repeated_calls_are_independent():
    balanced = make_balanced_tree()
    unbalanced = make_inner_violation_tree()
    assert is_balanced(balanced) is True
    assert is_balanced(unbalanced) is False
    assert is_balanced(None) is True
    assert is_balanced(balanced) is True
    assert is_balanced(unbalanced) is False


def test_validation_does_not_change_tree():
    def snapshot(node):
        if node is None:
            return None
        return (id(node), node.value, snapshot(node.left), snapshot(node.right))

    for root, expected in [
        (make_balanced_tree(), True),
        (make_inner_violation_tree(), False),
    ]:
        before = snapshot(root)
        assert is_balanced(root) is expected
        assert snapshot(root) == before


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
