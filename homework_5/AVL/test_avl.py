import random

import pytest

from avl import AVL


def check_tree(tree, expected):
    values = []
    visited = set()

    def visit(node, lower, upper):
        if node is None:
            return 0

        assert id(node) not in visited
        visited.add(id(node))
        assert lower < node.value < upper

        left_height = visit(node.left, lower, node.value)
        values.append(node.value)
        right_height = visit(node.right, node.value, upper)

        # Высоты пересчитываются по связям
        actual_height = 1 + max(left_height, right_height)
        assert node.height == actual_height
        assert abs(right_height - left_height) <= 1
        return actual_height

    visit(tree.root, float("-inf"), float("inf"))
    assert values == sorted(expected)
    assert tree.inorder() == values


def build_tree(values):
    tree = AVL()
    expected = set()
    for value in values:
        tree.insert(value)
        expected.add(value)
        check_tree(tree, expected)
    return tree


def shape(node):
    if node is None:
        return None
    return node.value, shape(node.left), shape(node.right)


def test_empty_tree():
    tree = AVL()
    assert tree.root is None
    assert tree.search(10) is False
    tree.delete(10)
    check_tree(tree, [])
    assert tree.root is None


def test_single_node():
    tree = build_tree([10])
    assert tree.root.value == 10
    assert tree.root.height == 1
    assert tree.search(10) is True

    tree.delete(10)
    check_tree(tree, [])
    assert tree.root is None
    assert tree.search(10) is False


@pytest.mark.parametrize("values", [
    [30, 20, 10],
    [10, 20, 30],
    [30, 10, 20],
    [10, 30, 20],
], ids=["LL", "RR", "LR", "RL"])
def test_insert_rotations(values):
    tree = build_tree(values)
    assert shape(tree.root) == (20, (10, None, None), (30, None, None))


def test_duplicate_insert():
    tree = build_tree([20, 10, 30])
    original_shape = shape(tree.root)
    for value in [20, 10, 30, 20]:
        tree.insert(value)
        check_tree(tree, [10, 20, 30])
        assert shape(tree.root) == original_shape


def test_search():
    tree = build_tree([0, -10, 10, -20, -5, 5, 20])
    original_shape = shape(tree.root)
    for value in [0, -10, 10, -20, -5, 5, 20]:
        assert tree.search(value) is True
    for value in [-100, -7, 7, 100]:
        assert tree.search(value) is False
    assert shape(tree.root) == original_shape
    check_tree(tree, [-20, -10, -5, 0, 5, 10, 20])


def test_delete_leaf():
    tree = build_tree([20, 10, 30])
    assert tree.root.left.left is None
    assert tree.root.left.right is None
    tree.delete(10)
    check_tree(tree, [20, 30])
    assert tree.search(10) is False


@pytest.mark.parametrize("child", [10, 30], ids=["left_child", "right_child"])
def test_delete_one_child(child):
    tree = build_tree([20, child])
    assert (tree.root.left is None) != (tree.root.right is None)
    tree.delete(20)
    check_tree(tree, [child])
    assert tree.root.value == child
    assert tree.search(20) is False


def test_delete_two_children():
    tree = build_tree([40, 20, 60, 10, 30, 50, 70, 55])
    assert tree.root.value == 40
    assert tree.root.left is not None and tree.root.right is not None
    assert tree.root.right.left.value == 50
    assert tree.root.right.left.right.value == 55

    # Преемник находится глубже и сам имеет правого ребенка
    tree.delete(40)
    check_tree(tree, [10, 20, 30, 50, 55, 60, 70])
    assert tree.search(40) is False
    assert shape(tree.root) == (
        50, (20, (10, None, None), (30, None, None)),
        (60, (55, None, None), (70, None, None)),
    )


def test_delete_missing():
    tree = build_tree([20, 10, 30])
    original_shape = shape(tree.root)
    for value in [-1, 25, 100]:
        tree.delete(value)
        check_tree(tree, [10, 20, 30])
        assert shape(tree.root) == original_shape


@pytest.mark.parametrize("values, removed, expected_shape", [
    ([30, 20, 40, 10, 25], 40,
     (20, (10, None, None), (30, (25, None, None), None))),
    ([20, 10, 30, 25, 40], 10,
     (30, (20, None, (25, None, None)), (40, None, None))),
    ([30, 10, 40, 20], 40,
     (20, (10, None, None), (30, None, None))),
    ([10, 0, 30, 20], 0,
     (20, (10, None, None), (30, None, None))),
], ids=["LL_child_balance_zero", "RR_child_balance_zero", "LR", "RL"])
def test_delete_rotations(values, removed, expected_shape):
    tree = build_tree(values)
    tree.delete(removed)
    check_tree(tree, set(values) - {removed})
    assert shape(tree.root) == expected_shape
    assert tree.search(removed) is False


def test_readme_example():
    tree = AVL()
    steps = [
        (30, (30, None, None)),
        (10, (30, (10, None, None), None)),
        (20, (20, (10, None, None), (30, None, None))),
        (40, (20, (10, None, None), (30, None, (40, None, None)))),
        (50, (20, (10, None, None), (40, (30, None, None), (50, None, None)))),
        (25, (30, (20, (10, None, None), (25, None, None)),
              (40, None, (50, None, None)))),
    ]
    expected = set()
    for value, expected_shape in steps:
        tree.insert(value)
        expected.add(value)
        check_tree(tree, expected)
        assert shape(tree.root) == expected_shape

    assert tree.search(25) is True
    assert tree.search(99) is False

    deletions = [
        (20, 2, (30, (25, (10, None, None), None),
                 (40, None, (50, None, None)))),
        (10, 0, (30, (25, None, None), (40, None, (50, None, None)))),
        (40, 1, (30, (25, None, None), (50, None, None))),
    ]
    for value, child_count, expected_shape in deletions:
        node = tree.root
        while node.value != value:
            node = node.left if value < node.value else node.right
        assert int(node.left is not None) + int(node.right is not None) == child_count

        tree.delete(value)
        expected.remove(value)
        check_tree(tree, expected)
        assert shape(tree.root) == expected_shape
        assert tree.search(value) is False


def test_ordered_sequences():
    for values in [list(range(200)), list(range(199, -1, -1))]:
        tree = build_tree(values)
        expected = set(values)
        for value in list(range(0, 200, 2)) + list(range(199, -1, -2)):
            tree.delete(value)
            expected.remove(value)
            check_tree(tree, expected)
            assert tree.search(value) is False
        assert tree.root is None


def test_mixed_operations():
    tree = AVL()
    expected = set()
    rng = random.Random(2026)

    # Фиксируем генератор чтобы набор операций повторялся
    for _ in range(300):
        value = rng.randrange(-50, 51)
        if rng.randrange(2):
            tree.insert(value)
            expected.add(value)
        else:
            tree.delete(value)
            expected.discard(value)
        check_tree(tree, expected)
        assert tree.search(value) == (value in expected)

    for value in range(-50, 51):
        assert tree.search(value) == (value in expected)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
