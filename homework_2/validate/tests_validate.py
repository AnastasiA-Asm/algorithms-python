import unittest
from validate import validate_stacks

class TestValidateStacks(unittest.TestCase):
    def test_nontrivial_valid_sequence(self):
        pushed = [1, 2, 3, 4, 5]
        popped = [1, 3, 5, 4, 2]

        self.assertTrue(validate_stacks(pushed, popped))

    def test_invalid_sequences(self):
        self.assertFalse(
            validate_stacks(
                [1, 2, 3],
                [3, 1, 2],
            )
        )

        self.assertFalse(
            validate_stacks(
                [1, 2, 3, 4, 5],
                [4, 3, 5, 1, 2],
            )
        )

    def test_same_and_reverse_order(self):
        # Каждый элемент удаляется сразу после добавления
        self.assertTrue(
            validate_stacks(
                [10, -3, 0, 8],
                [10, -3, 0, 8],
            )
        )

        # Сначала добавляются все элементы, затем все удаляются
        self.assertTrue(
            validate_stacks(
                [10, -3, 0, 8],
                [8, 0, -3, 10],
            )
        )

    def test_boundary_cases(self):
        # Минимальный допустимый случай по условию
        self.assertTrue(validate_stacks([55], [55]))

        # Дополнительная проверка пустого стека
        self.assertTrue(validate_stacks([], []))

if __name__ == "__main__":
    unittest.main()