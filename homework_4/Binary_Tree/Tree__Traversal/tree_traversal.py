class Node:
    """Узел бинарного дерева"""

    def __init__(self, value):
        self.value = value
        # У нового узла пока нет детей
        self.left = None
        self.right = None


class BinarySearchTree:
    """Бинарное дерево поиска"""

    def __init__(self):
        self.root = None

    def insert(self, value):
        """Вставка значения в дерево"""
        # Первое значение становится корнем
        if self.root is None:
            self.root = Node(value)
            return

        # Ищем место для вставки, начиная с корня
        current = self.root

        while True:
            if value < current.value:
                # Меньшее значение должно находиться слева
                if current.left is None:
                    current.left = Node(value)
                    return
                current = current.left
            else:
                # Большие и равные значения направляем вправо
                if current.right is None:
                    current.right = Node(value)
                    return
                current = current.right

    def preorder(self):
        """Корень -> левое поддерево -> правое поддерево"""
        # Все вызовы visit в этом обходе заполняют один список
        result = []

        def visit(node):
            # Если узла нет, возвращаемся к предыдущему вызову
            if node is None:
                return
            # Сначала записываем значение, затем обходим детей
            result.append(node.value)
            visit(node.left)
            visit(node.right)

        # Запускаем обход от корня дерева
        visit(self.root)
        return result

    def inorder(self):
        """Левое поддерево -> корень -> правое поддерево"""
        result = []

        def visit(node):
            if node is None:
                return
            visit(node.left)
            # Записываем значение между обходами поддеревьев
            result.append(node.value)
            visit(node.right)

        visit(self.root)
        return result

    def postorder(self):
        """Левое поддерево -> правое поддерево -> корень"""
        result = []

        def visit(node):
            if node is None:
                return
            visit(node.left)
            visit(node.right)
            # Записываем значение после обхода обоих поддеревьев
            result.append(node.value)

        visit(self.root)
        return result

    def reverse_preorder(self):
        """Корень -> правое поддерево -> левое поддерево"""
        result = []

        def visit(node):
            if node is None:
                return
            result.append(node.value)
            visit(node.right)
            visit(node.left)

        visit(self.root)
        return result

    def reverse_inorder(self):
        """Правое поддерево -> корень -> левое поддерево"""
        result = []

        def visit(node):
            if node is None:
                return
            visit(node.right)
            result.append(node.value)
            visit(node.left)

        visit(self.root)
        return result

    def reverse_postorder(self):
        """Правое поддерево -> левое поддерево -> корень"""
        result = []

        def visit(node):
            if node is None:
                return
            visit(node.right)
            visit(node.left)
            result.append(node.value)

        visit(self.root)
        return result