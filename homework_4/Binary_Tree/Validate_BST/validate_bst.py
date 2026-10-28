class Node:
    """Узел бинарного дерева"""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def is_valid_bst(root):
    """Проверяет BST с размещением равных значений справа"""

    def check(node, lower, upper):
        # В пустом поддереве нет нарушений
        if node is None:
            return True

        # Нижняя граница включается в допустимый диапазон
        if lower is not None and node.value < lower:
            return False

        # Верхняя граница не включается в допустимый диапазон
        if upper is not None and node.value >= upper:
            return False

        # Сохраняем ограничения предков и уточняем границу для детей
        return (
            check(node.left, lower, node.value)
            and check(node.right, node.value, upper)
        )

    # У корня пока нет ограничений по значению
    return check(root, None, None)