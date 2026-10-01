def two_sum(arr: list[int], k: int) -> tuple[int, int]:
    seen = {} # Уже встреченные числа и их индексы
    
    for i, number in enumerate(arr):
        needed = k - number
        
        if needed in seen:
            return seen[needed], i
        
        seen[number] = i
        
    raise ValueError("Подходящая пара не найдена")
