def count_primes(n: int) -> int: 
    prime_count = 0

    # Проверяем все числа строго меньше n
    for num in range(2, n):
        is_prime = True
        divisor = 2

        # Ищем делитель только до квадратного корня из num
        while divisor * divisor <= num:
            if num % divisor == 0:
                is_prime = False
                break
            divisor += 1

        if is_prime:
            prime_count += 1

    return prime_count

if __name__ == "__main__": 
    n = int(input()) 
    print(count_primes(n))