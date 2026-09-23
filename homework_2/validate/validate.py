def validate_stacks(pushed, popped):
    stack = []
    pop_index = 0

    for value in pushed:
        stack.append(value)

        # Удаляем все элементы, которые сейчас могут
        # выходить в порядке, указанном в popped
        while (
            stack
            and pop_index < len(popped)
            and stack[-1] == popped[pop_index]
        ):
            stack.pop()
            pop_index += 1

    return pop_index == len(popped)
