import time
from functools import wraps

# Декоратор для измерения времени выполнения функции
def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start

        print(f"{func.__name__}: {elapsed:.6f} с")
        return result

    return wrapper

# Рекурсивная сортировка слиянием
def merge_sort(nums: list[int]) -> list[int]:
    if len(nums) <= 1:
        return nums.copy()

    middle = len(nums) // 2

    left = merge_sort(nums[:middle])
    right = merge_sort(nums[middle:])

    result = []
    i, j = 0, 0

    # Слияние двух отсортированных частей
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

# Рекурсивная быстрая сортировка
def quick_sort(nums: list[int]) -> list[int]:
    if len(nums) <= 1:
        return nums.copy()

    pivot = nums[-1]

    left = []
    right = []

    # Разделение элементов относительно pivot
    for num in nums[:-1]:
        if num < pivot:
            left.append(num)
        else:
            right.append(num)

    return quick_sort(left) + [pivot] + quick_sort(right)
