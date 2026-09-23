import unittest
from merge_lists import Node, merge_with_dummy, merge_without_dummy

def create_linked_list(values):
    if not values:
        return None

    head = Node(values[0])
    tail = head

    for value in values[1:]:
        tail.next = Node(value)
        tail = tail.next

    return head

def linked_list_to_list(head):
    values = []

    while head is not None:
        values.append(head.value)
        head = head.next

    return values

class TestMergeLists(unittest.TestCase):
    def check_both_methods(self, values1, values2, expected):
        merge_functions = [
            merge_without_dummy,
            merge_with_dummy,
        ]

        for merge_function in merge_functions:
            with self.subTest(method=merge_function.__name__):
                # Для каждого способа создаём новые узлы, потому что при слиянии ссылки next изменяются
                list1 = create_linked_list(values1)
                list2 = create_linked_list(values2)

                result = merge_function(list1, list2)

                self.assertEqual(
                    linked_list_to_list(result),
                    expected,
                )

    def test_intersecting_lists(self):
        self.check_both_methods(
            [1, 4, 4, 9],
            [1, 2, 6, 10],
            [1, 1, 2, 4, 4, 6, 9, 10],
        )

    def test_empty_lists(self):
        self.check_both_methods([], [], [])
        self.check_both_methods([], [1, 3, 5], [1, 3, 5])
        self.check_both_methods([2, 4, 6], [], [2, 4, 6])

    def test_single_elements(self):
        self.check_both_methods([5], [2], [2, 5])
        self.check_both_methods([5], [5], [5, 5])
        self.check_both_methods([], [7], [7])

    def test_repeated_and_negative_values(self):
        self.check_both_methods(
            [-3, -1, 2, 2, 8],
            [-3, 2, 2, 2, 9],
            [-3, -3, -1, 2, 2, 2, 2, 2, 8, 9],
        )

    def test_one_list_goes_before_another(self):
        self.check_both_methods(
            [1, 2, 3],
            [10, 11, 12],
            [1, 2, 3, 10, 11, 12],
        )

        self.check_both_methods(
            [10, 11, 12],
            [1, 2, 3],
            [1, 2, 3, 10, 11, 12],
        )

if __name__ == "__main__":
    unittest.main()