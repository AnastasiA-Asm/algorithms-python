import random
import pytest

from iterative import merge_sort, quick_sort


@pytest.mark.parametrize("sort_func", [merge_sort, quick_sort])
@pytest.mark.parametrize(
    "nums",
    [
        [],                              # Пустой список
        [5],                             # Один элемент
        [1, 2],                          # Два элемента по порядку
        [2, 1],                          # Два элемента в обратном порядке
        [7, 2, 9, 4, 1, 6, 3],           # Пример для визуализации
        [8, 4, 2, 6, 1],                 # Минимальный pivot в конце
        [1, 2, 3, 4, 5, 6, 7],           # Уже отсортированный список
        [7, 6, 5, 4, 3, 2, 1],           # Обратный порядок
        [4, 2, 4, 1, 2, 4],              # Повторяющиеся элементы
        [3, 3, 3, 3, 3],                 # Все элементы одинаковые
        [-5, -2, -9, -1],                # Отрицательные числа
        [0, -3, 5, -1, 0, 5],            # Разные знаки, нули и повторы
        [1000000, -1000000, 0, 42],      # Большие по модулю числа
        [2, 1, 4, 3, 6, 5],              # Чередование соседних пар
    ],
)
def test_sort_cases(sort_func, nums):
    original = nums.copy()
    result = sort_func(nums)

    assert result == sorted(nums)
    assert nums == original
    assert result is not nums


# Границы блоков при итеративном слиянии (в том числе неполные блоки)
@pytest.mark.parametrize("sort_func", [merge_sort, quick_sort])
@pytest.mark.parametrize("size", [3, 5, 7, 9, 16, 17, 31, 33])
def test_different_lengths(sort_func, size):
    nums = list(range(size, 0, -1))
    assert sort_func(nums) == sorted(nums)


# Большие массивы, в том числе неудачные для выбора последнего pivot
@pytest.mark.parametrize("sort_func", [merge_sort, quick_sort])
@pytest.mark.parametrize(
    "nums",
    [
        list(range(2500)),
        list(range(2500, 0, -1)),
        [7] * 1500,
    ],
)
def test_large_arrays(sort_func, nums):
    original = nums.copy()
    assert sort_func(nums) == sorted(nums)
    assert nums == original


@pytest.mark.parametrize("sort_func", [merge_sort, quick_sort])
def test_random_arrays(sort_func):
    generator = random.Random(42)

    for _ in range(30):
        nums = [generator.randint(-100, 100) for _ in range(generator.randint(0, 100))]
        original = nums.copy()

        assert sort_func(nums) == sorted(nums)
        assert nums == original


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
