import random
import re
import pytest

from compare import measure_time, merge_sort, quick_sort


@pytest.mark.parametrize("sort_func", [merge_sort, quick_sort])
@pytest.mark.parametrize(
    "nums",
    [
        [],                             # Пустой список
        [5],                            # Один элемент
        [1, 2],                         # Два элемента по порядку
        [2, 1],                         # Два элемента в обратном порядке
        [6, 3, 8, 2, 5],                # Пример для визуализации
        [8, 4, 2, 6, 1],                # Минимальный pivot в конце
        [1, 2, 3, 4, 5, 6, 7],          # Уже отсортированный список
        [7, 6, 5, 4, 3, 2, 1],          # Обратный порядок
        [4, 2, 4, 1, 2, 4],             # Повторяющиеся элементы
        [3, 3, 3, 3, 3],                # Все элементы одинаковые
        [-5, -2, -9, -1],               # Только отрицательные числа
        [0, -3, 5, -1, 0, 5],           # Разные знаки, нули и повторы
        [1000000, -1000000, 0, 42],     # Большие по модулю числа
        [2, 1, 4, 3, 6, 5],             # Чередование пар
    ],
)
def test_sort_cases(sort_func, nums):
    original = nums.copy()
    result = sort_func(nums)

    assert result == sorted(nums)
    assert nums == original  # Исходный список не должен измениться
    assert result is not nums  # Возвращаем отдельный список


@pytest.mark.parametrize("sort_func", [merge_sort, quick_sort])
@pytest.mark.parametrize("nums", [list(range(600)), list(range(600, 0, -1))])
def test_large_ordered_arrays(sort_func, nums):
    assert sort_func(nums) == sorted(nums)


@pytest.mark.parametrize("sort_func", [merge_sort, quick_sort])
def test_random_arrays(sort_func):
    generator = random.Random(42)  # Фиксируем случайность для повторяемости

    for _ in range(30):
        nums = [generator.randint(-100, 100) for _ in range(generator.randint(0, 50))]
        assert sort_func(nums) == sorted(nums)


def test_measure_time_decorator(capsys):
    @measure_time
    def add(a, b):
        return a + b

    assert add(3, b=4) == 7
    assert add.__name__ == "add"

    output = capsys.readouterr().out.strip()
    assert re.fullmatch(r"add: \d+\.\d{6} с", output)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
