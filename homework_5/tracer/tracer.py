from functools import wraps


def tracer(func):
    depth = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal depth

        # Показываем аргументы и глубину вызова
        indent = "    " * depth
        arguments = [repr(arg) for arg in args]
        arguments += [f"{key}={value!r}" for key, value in kwargs.items()]
        print(f"{indent}Вызов {func.__name__}({', '.join(arguments)})")

        depth += 1
        try:
            result = func(*args, **kwargs)
        finally:
            # Возвращаем глубину назад, даже если произошла ошибка
            depth -= 1

        print(f"{indent}Возврат {func.__name__}: {result!r}")
        return result

    return wrapper
