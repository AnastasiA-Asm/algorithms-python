class HashTable:
    def __init__(self, capacity: int = 8):
        if not isinstance(capacity, int):
            raise TypeError("Размер таблицы должен быть целым числом")

        if capacity <= 0:
            raise ValueError("Размер таблицы должен быть положительным")

        self.capacity = capacity # кол-во ячеек
        self.size = 0 # кол-во сохр пар
        self.max_load_factor = 0.75 # порог для будщего расширения

        # Каждый внутренний список - отдельная цепочка
        self.buckets = [[] for _ in range(capacity)]

    # Вычисление индекса
    def _get_index(self, key):
        return hash(key) % self.capacity

    # Вставка
    def insert(self, key, value):
        index = self._get_index(key)
        bucket = self.buckets[index]

        # Если ключ уже есть, меняем только значение
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return

        # Новый ключ добавляем в цепочку вместе со значением
        bucket.append([key, value])
        self.size += 1

        # Считаем записи, а не количество занятых ячеек
        if self.size / self.capacity > self.max_load_factor:
            self._resize()

    # Поиск
    def get(self, key):
        index = self._get_index(key)

        for pair in self.buckets[index]:
            if pair[0] == key:
                return pair[1]

        raise KeyError(key)

    # Удаление
    def delete(self, key):
        index = self._get_index(key)
        bucket = self.buckets[index]

        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket.pop(i)
                self.size -= 1
                return

        raise KeyError(key)

    # Расширение
    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2

        self.buckets = [[] for _ in range(self.capacity)]

        # Пересчитываем индексы: размер таблицы изменился
        for bucket in old_buckets:
            for pair in bucket:
                index = self._get_index(pair[0])
                self.buckets[index].append(pair)

        # Количество записей при переносе не меняется

    def __contains__(self, key):
        index = self._get_index(key)

        # Ищем ключ в нужной цепочке
        for pair in self.buckets[index]:
            if pair[0] == key:
                return True

        return False
    
    # кол-во записей
    def __len__(self):
        return self.size

if __name__ == "__main__":
    table = HashTable(capacity=4)

    # Эти ключи попадают в одну ячейку при размере 4
    table.insert(1, "Anna")
    table.insert(5, "Maria")
    table.insert(9, "Ivan")

    print(table.buckets)
    print(table.get(5))  # Maria

    table.insert(5, "Masha")
    print(table.get(5))  # Masha

    # Четвёртая запись вызывает расширение таблицы
    table.insert(2, "Oleg")
    print(table.capacity)  # 8

    table.delete(1)
    print(table.get(9))  # Ivan
    print(len(table))    # 3
    
    print(5 in table)      # True - ключ 5 есть
    print(1 in table)      # False - ключ 1 мы удалили
    print(100 in table)    # False - такого ключа не добавляли
    print(100 not in table)  # True - можно проверять и отсутствие