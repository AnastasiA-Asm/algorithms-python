# Итеративная сортировка слиянием
def merge_sort(nums: list[int]) -> list[int]:
    result = nums.copy()
    n = len(result)
    size = 1

    # На каждом проходе объединяем блоки вдвое большего размера
    while size < n:
        for start in range(0, n, 2 * size):
            middle = min(start + size, n)
            end = min(start + 2 * size, n)

            left = result[start:middle]
            right = result[middle:end]
            merged = []
            i, j = 0, 0

            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1

            merged.extend(left[i:])
            merged.extend(right[j:])
            result[start:end] = merged

        size *= 2

    return result


# Итеративная быстрая сортировка
def quick_sort(nums: list[int]) -> list[int]:
    result = nums.copy()
    stack = [(0, len(result) - 1)]

    while stack:
        low, high = stack.pop()
        if low >= high:
            continue

        pivot = result[high]
        i = low

        # Помещаем элементы меньше pivot в левую часть участка
        for j in range(low, high):
            if result[j] < pivot:
                result[i], result[j] = result[j], result[i]
                i += 1

        result[i], result[high] = result[high], result[i]

        # Запоминаем границы участков, которые ещё нужно отсортировать
        if low < i - 1:
            stack.append((low, i - 1))
        if i + 1 < high:
            stack.append((i + 1, high))

    return result
