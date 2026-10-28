import pytest
from tree_traversal import BinarySearchTree

TRAVERSALS = (
    "preorder",
    "inorder",
    "postorder",
    "reverse_preorder",
    "reverse_inorder",
    "reverse_postorder",
)


def build_tree(values):
    tree = BinarySearchTree()
    for value in values:
        tree.insert(value)
    return tree


def check_traversals(tree, expected):
    for name in TRAVERSALS:
        actual = getattr(tree, name)()
        assert actual == expected[name], name


def test_empty_tree():
    tree = build_tree([])
    assert tree.root is None
    check_traversals(tree, {name: [] for name in TRAVERSALS})


def test_single_node():
    tree = build_tree([42])
    check_traversals(tree, {name: [42] for name in TRAVERSALS})


def test_standard_tree():
    tree = build_tree([8, 3, 10, 1, 6, 14])
    check_traversals(tree, {
        "preorder": [8, 3, 1, 6, 10, 14],
        "inorder": [1, 3, 6, 8, 10, 14],
        "postorder": [1, 6, 3, 14, 10, 8],
        "reverse_preorder": [8, 10, 14, 3, 6, 1],
        "reverse_inorder": [14, 10, 8, 6, 3, 1],
        "reverse_postorder": [14, 10, 6, 1, 3, 8],
    })


def test_nontrivial_tree():
    # Этот пример потом для визуализации
    tree = build_tree([8, 3, 10, 1, 6, 14, 4, 7, 13])
    check_traversals(tree, {
        "preorder": [8, 3, 1, 6, 4, 7, 10, 14, 13],
        "inorder": [1, 3, 4, 6, 7, 8, 10, 13, 14],
        "postorder": [1, 4, 7, 6, 3, 13, 14, 10, 8],
        "reverse_preorder": [8, 10, 14, 13, 3, 6, 7, 4, 1],
        "reverse_inorder": [14, 13, 10, 8, 7, 6, 4, 3, 1],
        "reverse_postorder": [13, 14, 10, 7, 4, 6, 1, 3, 8],
    })


def test_duplicate_values():
    tree = build_tree([5, 3, 7, 3, 5, 7])
    check_traversals(tree, {
        "preorder": [5, 3, 3, 7, 5, 7],
        "inorder": [3, 3, 5, 5, 7, 7],
        "postorder": [3, 3, 5, 7, 7, 5],
        "reverse_preorder": [5, 7, 7, 5, 3, 3],
        "reverse_inorder": [7, 7, 5, 5, 3, 3],
        "reverse_postorder": [7, 5, 7, 3, 3, 5],
    })


def test_negative_values_and_zero():
    tree = build_tree([0, -3, 4, -5, -1, 2])
    check_traversals(tree, {
        "preorder": [0, -3, -5, -1, 4, 2],
        "inorder": [-5, -3, -1, 0, 2, 4],
        "postorder": [-5, -1, -3, 2, 4, 0],
        "reverse_preorder": [0, 4, 2, -3, -1, -5],
        "reverse_inorder": [4, 2, 0, -1, -3, -5],
        "reverse_postorder": [2, 4, -1, -5, -3, 0],
    })


def test_right_chain():
    tree = build_tree([1, 2, 3, 4, 5])
    check_traversals(tree, {
        "preorder": [1, 2, 3, 4, 5],
        "inorder": [1, 2, 3, 4, 5],
        "postorder": [5, 4, 3, 2, 1],
        "reverse_preorder": [1, 2, 3, 4, 5],
        "reverse_inorder": [5, 4, 3, 2, 1],
        "reverse_postorder": [5, 4, 3, 2, 1],
    })


def test_left_chain():
    tree = build_tree([5, 4, 3, 2, 1])
    check_traversals(tree, {
        "preorder": [5, 4, 3, 2, 1],
        "inorder": [1, 2, 3, 4, 5],
        "postorder": [1, 2, 3, 4, 5],
        "reverse_preorder": [5, 4, 3, 2, 1],
        "reverse_inorder": [5, 4, 3, 2, 1],
        "reverse_postorder": [1, 2, 3, 4, 5],
    })


def test_all_values_equal():
    tree = build_tree([5, 5, 5, 5])
    check_traversals(tree, {name: [5, 5, 5, 5] for name in TRAVERSALS})


def test_insert_builds_expected_structure():
    tree = build_tree([8, 3, 10, 1, 6, 14, 4, 7, 13])
    assert tree.root.value == 8
    assert tree.root.left.value == 3
    assert tree.root.right.value == 10
    assert tree.root.left.left.value == 1
    assert tree.root.left.right.value == 6
    assert tree.root.left.right.left.value == 4
    assert tree.root.left.right.right.value == 7
    assert tree.root.right.left is None
    assert tree.root.right.right.value == 14
    assert tree.root.right.right.left.value == 13


def test_instances_are_independent():
    first = build_tree([5, 3])
    second = build_tree([10, 12])
    first.insert(7)
    assert first.inorder() == [3, 5, 7]
    assert second.inorder() == [10, 12]


def test_repeated_calls_return_independent_lists():
    tree = build_tree([8, 3, 10, 1, 6, 14, 4, 7, 13])
    for name in TRAVERSALS:
        method = getattr(tree, name)
        first = method()
        second = method()
        assert first == second, name
        assert first is not second, name
        first.append(999)
        assert method() == second, name


def test_traversals_do_not_change_tree():
    tree = build_tree([8, 3, 10, 1, 6, 14, 4, 7, 13])

    def snapshot(node):
        if node is None:
            return None
        return (id(node), node.value, snapshot(node.left), snapshot(node.right))

    before = snapshot(tree.root)
    for name in TRAVERSALS:
        getattr(tree, name)()
        assert snapshot(tree.root) == before, name


def test_insert_after_traversals():
    tree = build_tree([8, 3, 10])
    for name in TRAVERSALS:
        getattr(tree, name)()
    tree.insert(6)
    tree.insert(8)
    assert tree.inorder() == [3, 6, 8, 8, 10]
    assert tree.preorder() == [8, 3, 6, 10, 8]


def test_long_chain():
    values = list(range(200))
    tree = build_tree(values)
    reversed_values = values[::-1]
    check_traversals(tree, {
        "preorder": values,
        "inorder": values,
        "postorder": reversed_values,
        "reverse_preorder": values,
        "reverse_inorder": reversed_values,
        "reverse_postorder": reversed_values,
    })
    
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
