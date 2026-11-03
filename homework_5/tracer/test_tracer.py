import pytest

from tracer import tracer


@tracer
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


@pytest.mark.parametrize("n, expected", [(0, 1), (1, 1)])
def test_factorial_result(n, expected, capsys):
    assert factorial(n) == expected
    assert capsys.readouterr().out.splitlines() == [
        f"Вызов factorial({n})",
        "Возврат factorial: 1",
    ]


def test_factorial_trace(capsys):
    assert factorial(4) == 24

    # Сравниваем весь вывод вместе с отступами
    assert capsys.readouterr().out.splitlines() == [
        "Вызов factorial(4)",
        "    Вызов factorial(3)",
        "        Вызов factorial(2)",
        "            Вызов factorial(1)",
        "            Возврат factorial: 1",
        "        Возврат factorial: 2",
        "    Возврат factorial: 6",
        "Возврат factorial: 24",
    ]


def test_branching_recursion(capsys):
    @tracer
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    assert fibonacci(3) == 2
    assert capsys.readouterr().out.splitlines() == [
        "Вызов fibonacci(3)",
        "    Вызов fibonacci(2)",
        "        Вызов fibonacci(1)",
        "        Возврат fibonacci: 1",
        "        Вызов fibonacci(0)",
        "        Возврат fibonacci: 0",
        "    Возврат fibonacci: 1",
        "    Вызов fibonacci(1)",
        "    Возврат fibonacci: 1",
        "Возврат fibonacci: 2",
    ]


def test_arguments(capsys):
    @tracer
    def add(a, b, *, offset=0):
        return a + b + offset

    assert add(2, 3, offset=4) == 9
    assert capsys.readouterr().out.splitlines() == [
        "Вызов add(2, 3, offset=4)",
        "Возврат add: 9",
    ]


def test_none_result(capsys):
    @tracer
    def nothing():
        return None

    assert nothing() is None
    assert capsys.readouterr().out.splitlines() == [
        "Вызов nothing()",
        "Возврат nothing: None",
    ]


def test_metadata():
    def original():
        """Описание функции."""
        return 1

    decorated = tracer(original)
    assert decorated.__name__ == original.__name__
    assert decorated.__doc__ == original.__doc__


def test_repeated_calls(capsys):
    assert factorial(3) == 6
    capsys.readouterr()

    # Новый запуск должен начинаться без отступа
    assert factorial(1) == 1
    assert capsys.readouterr().out.splitlines() == [
        "Вызов factorial(1)",
        "Возврат factorial: 1",
    ]


def test_depth_after_exception(capsys):
    @tracer
    def countdown(n):
        if n == 0:
            raise ValueError("Ошибка в базовом случае")
        if n < 0:
            return n
        return countdown(n - 1)

    with pytest.raises(ValueError, match="Ошибка в базовом случае"):
        countdown(2)
    capsys.readouterr()

    assert countdown(-1) == -1
    assert capsys.readouterr().out.splitlines() == [
        "Вызов countdown(-1)",
        "Возврат countdown: -1",
    ]


@tracer
def sum_list(numbers):
    if not numbers:
        return 0
    return numbers[0] + sum_list(numbers[1:])


@pytest.mark.parametrize("numbers, expected", [
    ([], 0), ([7], 7),
])
def test_list_sum_result(numbers, expected):
    original = numbers.copy()
    assert sum_list(numbers) == expected
    assert numbers == original


def test_list_sum_trace(capsys):
    numbers = [2, -3, 5]
    assert sum_list(numbers) == 4
    assert numbers == [2, -3, 5]
    assert capsys.readouterr().out.splitlines() == [
        "Вызов sum_list([2, -3, 5])",
        "    Вызов sum_list([-3, 5])",
        "        Вызов sum_list([5])",
        "            Вызов sum_list([])",
        "            Возврат sum_list: 0",
        "        Возврат sum_list: 5",
        "    Возврат sum_list: 2",
        "Возврат sum_list: 4",
    ]


@tracer
def reverse_string(text):
    if not text:
        return ""
    return reverse_string(text[1:]) + text[0]


@pytest.mark.parametrize("text, expected", [
    ("", ""), ("a", "a"),
])
def test_reverse_string_result(text, expected):
    assert reverse_string(text) == expected


def test_reverse_string_trace(capsys):
    assert reverse_string("кот") == "ток"
    assert capsys.readouterr().out.splitlines() == [
        "Вызов reverse_string('кот')",
        "    Вызов reverse_string('от')",
        "        Вызов reverse_string('т')",
        "            Вызов reverse_string('')",
        "            Возврат reverse_string: ''",
        "        Возврат reverse_string: 'т'",
        "    Возврат reverse_string: 'то'",
        "Возврат reverse_string: 'ток'",
    ]


@tracer
def preorder(node):
    # Узел записан как (значение, левое поддерево, правое поддерево)
    if node is None:
        return []
    value, left, right = node
    return [value] + preorder(left) + preorder(right)


@pytest.mark.parametrize("tree, expected", [
    (None, []),
    ((5, None, None), [5]),
])
def test_tree_result(tree, expected):
    assert preorder(tree) == expected


def test_tree_trace(capsys):
    tree = (4, (2, None, (3, None, None)), (7, None, None))
    assert preorder(tree) == [4, 2, 3, 7]

    # Проверяем переходы между поддеревьями и пустые ветки
    assert capsys.readouterr().out.splitlines() == [
        "Вызов preorder((4, (2, None, (3, None, None)), (7, None, None)))",
        "    Вызов preorder((2, None, (3, None, None)))",
        "        Вызов preorder(None)",
        "        Возврат preorder: []",
        "        Вызов preorder((3, None, None))",
        "            Вызов preorder(None)",
        "            Возврат preorder: []",
        "            Вызов preorder(None)",
        "            Возврат preorder: []",
        "        Возврат preorder: [3]",
        "    Возврат preorder: [2, 3]",
        "    Вызов preorder((7, None, None))",
        "        Вызов preorder(None)",
        "        Возврат preorder: []",
        "        Вызов preorder(None)",
        "        Возврат preorder: []",
        "    Возврат preorder: [7]",
        "Возврат preorder: [4, 2, 3, 7]",
    ]


def test_keyword_only_call(capsys):
    assert factorial(n=3) == 6
    assert capsys.readouterr().out.splitlines() == [
        "Вызов factorial(n=3)",
        "    Вызов factorial(2)",
        "        Вызов factorial(1)",
        "        Возврат factorial: 1",
        "    Возврат factorial: 2",
        "Возврат factorial: 6",
    ]


def test_list_result_identity(capsys):
    numbers = [1, 2, 3]

    @tracer
    def get_numbers():
        return numbers

    result = get_numbers()
    assert result is numbers
    assert result == [1, 2, 3]
    assert capsys.readouterr().out.splitlines() == [
        "Вызов get_numbers()",
        "Возврат get_numbers: [1, 2, 3]",
    ]


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
