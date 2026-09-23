class Node: 
    def __init__(self, value): 
        self.value = value 
        self.next = None

# Класс для стеков
class Stack: 
    def __init__(self): 
        self.top = None # Вершина стека

    def push(self, value): # (положить эл-т)
        new_node = Node(value)

        # Сначала сохраняем связь со старой вершиной
        new_node.next = self.top
        self.top = new_node # Новый узел становится вершиной

    def pop(self): # (снять эл-т)
        if self.top is None:
            raise IndexError("Нельзя удалить элемент из пустого стека")

        # Сохраняем значение до того, как передвинем вершину.
        value = self.top.value
        self.top = self.top.next # След. узел становится новой вершиной

        return value

    def peek(self): # (посмотреть эл-т)
        if self.top is None:
            raise IndexError("Стек пуст")

        return self.top.value

    def is_empty(self):
        return self.top is None
 
# Класс для очереди   
class Queue: 
    def __init__(self): 
        self.head = None 
        self.tail = None

    def enqueue(self, value):
        new_node = Node(value)

        # В пустой очереди новый узел становится первым
        # Иначе присоединяем его после последнего узла
        if self.tail is None:
            self.head = new_node
        else:
            self.tail.next = new_node

        self.tail = new_node

    def dequeue(self):
        if self.head is None:
            raise IndexError("Нельзя удалить элемент из пустой очереди")

        value = self.head.value
        self.head = self.head.next

        # Если удалили последний узел, очередь полностью опустела.
        if self.head is None:
            self.tail = None

        return value

    def peek(self):
        if self.head is None:
            raise IndexError("Очередь пуста")

        return self.head.value

    def is_empty(self):
        return self.head is None
    