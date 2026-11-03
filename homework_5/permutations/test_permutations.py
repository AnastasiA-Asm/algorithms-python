from itertools import permutations as reference_permutations

import pytest

from permutations import permutations


@pytest.mark.parametrize("nums, expected", [
    ([1, 2, 3], [[1, 2, 3], [1, 3, 2], [2, 1, 3],
                 [2, 3, 1], [3, 1, 2], [3, 2, 1]]),
    ([0, 1], [[0, 1], [1, 0]]),
    ([1], [[1]]),
], ids=["three_elements", "zero_and_one", "single_element"])
def test_examples(nums, expected):
    # Порядок перестановок в ответе может быть любым
    assert sorted(permutations(nums)) == sorted(expected)


@pytest.mark.parametrize("nums, expected", [
    ([], [[]]),
    ([-1, 0, 2], [[-1, 0, 2], [-1, 2, 0], [0, -1, 2],
                  [0, 2, -1], [2, -1, 0], [2, 0, -1]]),
    ([3, 2, 1], [[1, 2, 3], [1, 3, 2], [2, 1, 3],
                 [2, 3, 1], [3, 1, 2], [3, 2, 1]]),
    ([1, 1, 2], [[1, 1, 2], [1, 2, 1], [2, 1, 1]]),
    ([2, 1, 2, 1], [[1, 1, 2, 2], [1, 2, 1, 2], [1, 2, 2, 1],
                    [2, 1, 1, 2], [2, 1, 2, 1], [2, 2, 1, 1]]),
    ([5, 5, 5], [[5, 5, 5]]),
], ids=["empty", "negative_and_zero", "descending", "duplicate",
        "two_duplicate_groups", "all_equal"])
def test_edge_cases(nums, expected):
    assert sorted(permutations(nums)) == sorted(expected)


def test_four_elements(capsys):
    nums = [4, 1, 3, 2]
    result = permutations(nums)

    # Готовый инструмент используется только для проверки ответа
    expected = sorted(reference_permutations(nums))
    assert sorted(tuple(row) for row in result) == expected
    assert len(result) == 24

    calls = [line for line in capsys.readouterr().out.splitlines()
             if line.lstrip().startswith("Вызов ")]
    depths = [(len(line) - len(line.lstrip())) // 4 for line in calls]
    assert set(depths) == {0, 1, 2, 3, 4}


def test_input_unchanged():
    nums = [2, 1, 2]
    original = nums.copy()
    permutations(nums)
    assert nums == original


def test_repeated_calls(capsys):
    first = permutations([1, 2])
    first[0][0] = 99
    capsys.readouterr()

    second = permutations([1, 2])
    assert sorted(second) == [[1, 2], [2, 1]]
    assert capsys.readouterr().out.splitlines()[0] == "Вызов backtrack([])"


def test_different_calls(capsys):
    first = permutations([1, 2])
    assert permutations([]) == [[]]
    capsys.readouterr()

    assert permutations([7]) == [[7]]
    assert sorted(first) == [[1, 2], [2, 1]]
    assert capsys.readouterr().out.splitlines()[0] == "Вызов backtrack([])"


def test_result_lists_independent():
    nums = [1, 2, 3]
    result = permutations(nums)
    assert len({id(row) for row in result}) == 6

    # Изменение 1 варианта не должно затронуть остальные
    other_rows = [row.copy() for row in result[1:]]
    result[0][0] = 99
    assert result[1:] == other_rows
    assert nums == [1, 2, 3]


def test_result_not_linked_to_input():
    nums = [1, 2]
    result = permutations(nums)
    nums[0] = 99
    assert sorted(result) == [[1, 2], [2, 1]]


def test_empty_trace(capsys):
    assert permutations([]) == [[]]
    assert capsys.readouterr().out.splitlines() == [
        "Вызов backtrack([])",
        "Возврат backtrack: [[]]",
    ]


def test_duplicate_trace(capsys):
    assert permutations([1, 1]) == [[1, 1]]
    assert capsys.readouterr().out.splitlines() == [
        "Вызов backtrack([])",
        "    Вызов backtrack([1])",
        "        Вызов backtrack([1, 1])",
        "        Возврат backtrack: [[1, 1]]",
        "    Возврат backtrack: [[1, 1]]",
        "Возврат backtrack: [[1, 1]]",
    ]


def test_full_trace(capsys):
    expected = [[1, 2, 3], [1, 3, 2], [2, 1, 3],
                [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    assert permutations([1, 2, 3]) == expected

    # Этот пример для разбора дальше
    assert capsys.readouterr().out.splitlines() == [
        "Вызов backtrack([])",
        "    Вызов backtrack([1])",
        "        Вызов backtrack([1, 2])",
        "            Вызов backtrack([1, 2, 3])",
        "            Возврат backtrack: [[1, 2, 3]]",
        "        Возврат backtrack: [[1, 2, 3]]",
        "        Вызов backtrack([1, 3])",
        "            Вызов backtrack([1, 3, 2])",
        "            Возврат backtrack: [[1, 3, 2]]",
        "        Возврат backtrack: [[1, 3, 2]]",
        "    Возврат backtrack: [[1, 2, 3], [1, 3, 2]]",
        "    Вызов backtrack([2])",
        "        Вызов backtrack([2, 1])",
        "            Вызов backtrack([2, 1, 3])",
        "            Возврат backtrack: [[2, 1, 3]]",
        "        Возврат backtrack: [[2, 1, 3]]",
        "        Вызов backtrack([2, 3])",
        "            Вызов backtrack([2, 3, 1])",
        "            Возврат backtrack: [[2, 3, 1]]",
        "        Возврат backtrack: [[2, 3, 1]]",
        "    Возврат backtrack: [[2, 1, 3], [2, 3, 1]]",
        "    Вызов backtrack([3])",
        "        Вызов backtrack([3, 1])",
        "            Вызов backtrack([3, 1, 2])",
        "            Возврат backtrack: [[3, 1, 2]]",
        "        Возврат backtrack: [[3, 1, 2]]",
        "        Вызов backtrack([3, 2])",
        "            Вызов backtrack([3, 2, 1])",
        "            Возврат backtrack: [[3, 2, 1]]",
        "        Возврат backtrack: [[3, 2, 1]]",
        "    Возврат backtrack: [[3, 1, 2], [3, 2, 1]]",
        "Возврат backtrack: [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]",
    ]


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
