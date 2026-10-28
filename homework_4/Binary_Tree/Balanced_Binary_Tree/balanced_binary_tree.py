class Node:
    """Узел бинарного дерева"""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def is_balanced(root):
    """Проверяет сбалансированность дерева по высоте"""

    def check_height(node):
        # Высота пустого поддерева равна нулю
        if node is None:
            return 0

        left_height = check_height(node.left)
        if left_height == -1:
            return -1

        right_height = check_height(node.right)
        if right_height == -1:
            return -1

        # Проверяем разницу высот у текущего узла
        if abs(left_height - right_height) > 1:
            return -1

        # Добавляем один уровень за текущий узел
        return 1 + max(left_height, right_height)

    # Найдено нарушение баланса
    return check_height(root) != -1