def is_palindrome(num: int) -> bool:
    orig_num = num
    rev_num = 0
    
    while num > 0:
        last_digit = num % 10 # Берем последнюю цифру 
        rev_num = rev_num * 10 + last_digit # Добавляем ее к перевернутому числу
        num //= 10 # Убираем обработанную цифру
        
    return orig_num == rev_num

if __name__ == "__main__":
    num = int(input())
    print(is_palindrome(num))