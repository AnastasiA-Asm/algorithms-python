def find_kth_largest(nums: list[int], k: int) -> int: # Поиск k-го по величине элемента с помощью Quickselect
    if not 1 <= k <= len(nums):
        raise ValueError("k должен быть от 1 до длины списка")

    result = nums.copy()
    target = k - 1
    low, high = 0, len(result) - 1

    while low <= high:
        pivot = result[high]
        i = low

        # Перемещаем элементы больше pivot в начало участка
        for j in range(low, high):
            if result[j] > pivot:
                result[i], result[j] = result[j], result[i]
                i += 1

        result[i], result[high] = result[high], result[i]

        # Продолжаем поиск только в той части, где находится k-й элемент
        if i == target:
            return result[i]
        elif i > target:
            high = i - 1
        else:
            low = i + 1
