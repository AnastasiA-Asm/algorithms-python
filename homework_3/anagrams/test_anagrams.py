import pytest

from anagrams import group_anagrams

@pytest.mark.parametrize(
    "words, expected",
    [
        # Пример из условия
        (
            ["eat", "tea", "tan", "ate", "nat", "bat"],
            [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]],
        ),

        # Пустой список
        ([], []),

        # Одна пустая строка
        ([""], [[""]]),

        # Одно слово
        (["solo"], [["solo"]]),

        # Все слова входят в одну группу
        (
            ["listen", "silent", "enlist"],
            [["enlist", "listen", "silent"]],
        ),

        # Ни у одного слова нет анаграмм
        (
            ["cat", "dog", "bird"],
            [["cat"], ["dog"], ["bird"]],
        ),

        # Повторяющиеся слова должны сохраняться
        (
            ["eat", "tea", "eat"],
            [["eat", "eat", "tea"]],
        ),

        # Одинаковые буквы, но разное количество каждой буквы
        (
            ["aab", "aba", "abb", "bba"],
            [["aab", "aba"], ["abb", "bba"]],
        ),

        # Однобуквенные слова, повторения и пустая строка
        (
            ["a", "b", "a", ""],
            [[""], ["b"], ["a", "a"]],
        ),

        # Нетривиальный пример
        (
            ["aab", "tea", "", "abb", "eat", "aba",
            "bat", "", "bba", "ate", "eat",],
            [["bat"],
            ["aab", "aba"],
            ["", ""],
            ["abb", "bba"],
            ["ate", "eat", "eat", "tea"],],
        ),
    ],
)
def test_group_anagrams(words, expected):
    result = group_anagrams(words)

    # Проверяем состав групп независимо от их порядка
    assert sorted(result) == sorted(expected)

    # Слова внутри каждой группы должны быть отсортированы (на всякий случай)
    for group in result:
        assert group == sorted(group)

    # Группы должны идти по возрастанию количества слов (тоже на всякий случай)
    lengths = [len(group) for group in result]
    assert lengths == sorted(lengths)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])