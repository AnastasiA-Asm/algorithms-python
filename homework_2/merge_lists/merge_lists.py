class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

# Первый способ без фиктивного узла
def merge_without_dummy(list1, list2):
    # Если один список пуст, возвращаем второй
    if list1 is None:
        return list2

    if list2 is None:
        return list1

    # Без фиктивного узла голову результата выбираем отдельно
    if list1.value <= list2.value:
        head = list1
        list1 = list1.next
    else:
        head = list2
        list2 = list2.next

    tail = head

    while list1 is not None and list2 is not None:
        if list1.value <= list2.value:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next

        tail = tail.next

    # Присоединяем оставшуюся часть незаконченного списка
    if list1 is not None:
        tail.next = list1
    else:
        tail.next = list2

    return head

# Второй способ с фиктивным узлом
def merge_with_dummy(list1, list2):
    dummy = Node(0)
    tail = dummy

    while list1 is not None and list2 is not None:
        if list1.value <= list2.value:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next

        tail = tail.next

    # Присоединяем оставшиеся узлы одного из списков
    if list1 is not None:
        tail.next = list1
    else:
        tail.next = list2

    # Фиктивный узел пропускаем
    return dummy.next
