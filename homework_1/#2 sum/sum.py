def max_even_sum(nums: list[int]) -> int: 
    total = 0 
    min_odd = 0

    for num in nums:
        total += num

        # Запоминаем самое маленькое нечётное число
        if num % 2 != 0 and (min_odd == 0 or num < min_odd):
            min_odd = num

    if total % 2 == 0:
        return total

    return total - min_odd

if __name__ == "__main__": 
    nums = list(map(int, input().split())) 
    print(max_even_sum(nums))