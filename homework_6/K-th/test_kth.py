import random
import pytest

from kth import find_kth_largest


@pytest.mark.parametrize(
    "nums, k, expected",
    [
        ([3, 2, 1, 5, 6, 4], 2, 5),             # Первый пример из задания
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),    # Второй пример из задания
        ([7, 2, 9, 4, 1, 6, 3], 3, 6),          # Пример для визуализации
        ([8], 1, 8),                            # Один элемент
        ([2, 1], 1, 2),                         # Максимальный элемент
        ([2, 1], 2, 1),                         # Минимальный элемент
        ([1, 2, 3, 4, 5], 3, 3),                # Уже отсортированный массив
        ([5, 4, 3, 2, 1], 2, 4),                # Обратный порядок
        ([8, 4, 2, 6, 1], 1, 8),                # Минимальный pivot в конце
        ([7, 7, 7, 7], 3, 7),                   # Все элементы одинаковые
        ([5, 5, 3, 1], 2, 5),                   # Повтор максимума
        ([9, 9, 5, 5, 1], 3, 5),                # Повторы на разных позициях
        ([4, 1, 4, 2, 3, 4], 4, 3),             # k сразу после повторов
        ([-8, -2, -10, -3], 2, -3),             # Только отрицательные числа
        ([0, -3, 5, -1, 0, 5], 3, 0),           # Отрицательные, нули и повторы
        ([1000000, -1000000, 0, 1000000], 2, 1000000),  # Большие значения
        ([6, 1, 5, 2, 4, 3], 3, 4),             # Чередование больших и меньших
    ],
)
def test_kth_cases(nums, k, expected):
    original = nums.copy()

    assert find_kth_largest(nums, k) == expected
    assert nums == original


# Проверяем все допустимые k, включая первое и последнее
@pytest.mark.parametrize(
    "nums",
    [
        [4, 1, 7, 2, 6],
        [1, 2, 3, 4, 5, 6],
        [6, 5, 4, 3, 2, 1],
        [4, 4, 2, 2, 1],
        [-4, 0, 3, -4, 8, 0],
    ],
)
def test_every_k(nums):
    expected = sorted(nums, reverse=True)

    for k in range(1, len(nums) + 1):
        assert find_kth_largest(nums, k) == expected[k - 1]


# Большие массивы, в том числе с неудачным выбором последнего pivot
@pytest.mark.parametrize(
    "nums, k, expected",
    [
        (list(range(1500)), 1, 1499),
        (list(range(1500)), 1500, 0),
        (list(range(1500, 0, -1)), 750, 751),
        ([7] * 1500, 1000, 7),
    ],
)
def test_large_arrays(nums, k, expected):
    original = nums.copy()

    assert find_kth_largest(nums, k) == expected
    assert nums == original


@pytest.mark.parametrize(
    "nums, k",
    [
        ([], 1),
        ([], 0),
        ([5], 0),
        ([5], -1),
        ([5], 2),
        ([1, 2, 3], 4),
    ],
)
def test_invalid_k(nums, k):
    with pytest.raises(ValueError):
        find_kth_largest(nums, k)


# Случайные массивы с фиксированным seed для воспроизводимости
def test_random_arrays():
    generator = random.Random(42)

    for _ in range(30):
        nums = [generator.randint(-100, 100) for _ in range(generator.randint(1, 80))]
        original = nums.copy()
        expected = sorted(nums, reverse=True)

        for k in range(1, len(nums) + 1):
            assert find_kth_largest(nums, k) == expected[k - 1]

        assert nums == original


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
