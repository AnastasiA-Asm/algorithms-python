import pytest
from hash_table import HashTable

def test_empty_table():
    table = HashTable()

    assert len(table) == 0
    assert 1 not in table

@pytest.mark.parametrize("key, value", [
    (10, "ten"),
    ("name", "Anna"),
    (None, [1, 2, 3]),
])
def test_insert_and_get(key, value):
    table = HashTable()
    table.insert(key, value)

    assert table.get(key) == value
    assert key in table
    assert len(table) == 1

def test_update_value():
    table = HashTable(capacity=4)
    table.insert(1, "Anna")
    table.insert(5, "Maria")
    table.insert(9, "Ivan")

    table.insert(5, "Masha")

    assert table.get(5) == "Masha"
    assert len(table) == 3
    assert table.capacity == 4

def test_collisions():
    table = HashTable(capacity=4)

    # Все три ключа попадают в одну цепочку
    table.insert(1, "Anna")
    table.insert(5, "Maria")
    table.insert(9, "Ivan")

    assert table.get(1) == "Anna"
    assert table.get(5) == "Maria"
    assert table.get(9) == "Ivan"
    assert len(table) == 3

@pytest.mark.parametrize("deleted_key", [1, 5, 9])
def test_delete_from_chain(deleted_key):
    table = HashTable(capacity=4)
    keys = [1, 5, 9]

    for key in keys:
        table.insert(key, str(key))

    table.delete(deleted_key)

    assert deleted_key not in table
    assert len(table) == 2

    # После удаления остальные записи должны сохраниться
    for key in keys:
        if key != deleted_key:
            assert table.get(key) == str(key)

    with pytest.raises(KeyError):
        table.get(deleted_key)

@pytest.mark.parametrize("operation", ["get", "delete"])
def test_missing_key(operation):
    table = HashTable()
    table.insert(1, "Anna")

    with pytest.raises(KeyError):
        if operation == "get":
            table.get(100)
        else:
            table.delete(100)

    assert len(table) == 1
    assert table.get(1) == "Anna"

def test_resize():
    table = HashTable(capacity=4)

    for key in [1, 5, 9]:
        table.insert(key, str(key))

    # При заполненности ровно 0.75 расширения ещё нет
    assert table.capacity == 4

    table.insert(2, "2")

    assert table.capacity == 8
    assert len(table) == 4

    for key in [1, 5, 9, 2]:
        assert table.get(key) == str(key)
        assert key in table

def test_multiple_resizes():
    table = HashTable(capacity=2)

    for key in range(50):
        table.insert(key, key * 10)

    assert table.capacity > 4
    assert len(table) == 50

    for key in range(50):
        assert table.get(key) == key * 10

def test_none_value():
    table = HashTable()
    table.insert("empty", None)

    assert table.get("empty") is None
    assert "empty" in table
    assert "missing" not in table

def test_reinsert_after_delete():
    table = HashTable()
    table.insert(1, "Anna")
    table.delete(1)
    table.insert(1, "Masha")

    assert table.get(1) == "Masha"
    assert 1 in table
    assert len(table) == 1

def test_independent_tables():
    first = HashTable()
    second = HashTable()

    first.insert(1, "Anna")

    assert first.get(1) == "Anna"
    assert 1 not in second
    assert len(second) == 0

@pytest.mark.parametrize("capacity, error", [
    (0, ValueError),
    (-4, ValueError),
    (2.5, TypeError),
])
def test_invalid_capacity(capacity, error):
    with pytest.raises(error):
        HashTable(capacity)

def test_unhashable_key():
    table = HashTable()

    with pytest.raises(TypeError):
        table.insert([1, 2], "value")

    assert len(table) == 0

def test_nontrivial_example():
    table = HashTable(capacity=4)

    # Коллизии
    table.insert(1, "Anna")
    table.insert(5, "Maria")
    table.insert(9, "Ivan")

    assert table.capacity == 4
    assert len(table) == 3

    # Обновление существующего ключа
    table.insert(5, "Masha")
    assert table.get(5) == "Masha"
    assert len(table) == 3

    # Расширение
    table.insert(2, "Oleg")
    assert table.capacity == 8
    assert len(table) == 4

    # Удаление и проверка оставшихся записей
    table.delete(1)

    assert 1 not in table
    assert 5 in table
    assert 9 in table
    assert 2 in table
    assert table.get(5) == "Masha"
    assert table.get(9) == "Ivan"
    assert table.get(2) == "Oleg"
    assert len(table) == 3

if __name__ == "__main__":
    pytest.main([__file__, "-v"])