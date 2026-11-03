import sys
from pathlib import Path

# Подключение декоратора из первой задачи
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from homework_5.tracer.tracer import tracer


def permutations(nums):
    used = [False] * len(nums)

    @tracer
    def backtrack(path):
        # Готовую перестановку сохраняем отдельным списком
        if len(path) == len(nums):
            return [path.copy()]

        result = []
        seen = set()

        for i, number in enumerate(nums):
            # Пропускаем занятые позиции и одинаковые варианты на этом уровне
            if used[i] or number in seen:
                continue

            seen.add(number)
            used[i] = True
            path.append(number)

            result.extend(backtrack(path))

            # Отмена выбора перед следующим вариантом
            path.pop()
            used[i] = False

        return result

    return backtrack([])
