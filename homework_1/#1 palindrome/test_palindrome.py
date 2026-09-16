from Palindrome import is_palindrome

def test_palindrome():
    assert is_palindrome(121) is True

def test_not_palindrome():
    assert is_palindrome(31) is False

def test_one_digit():
    assert is_palindrome(7) is True

def test_even_digits():
    assert is_palindrome(1001) is True

def test_zero_inside():
    assert is_palindrome(12021) is True

def test_zero_at_end():
    assert is_palindrome(120) is False

def test_long_not_pal():
    assert is_palindrome(12345) is False

def test_1():
    assert is_palindrome(1) is True

def test_11():
    assert is_palindrome(11) is True

def test_10():
    assert is_palindrome(10) is False

def test_long_pal():
    assert is_palindrome(123454321) is True