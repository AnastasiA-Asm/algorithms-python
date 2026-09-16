from Prime import count_primes

def test_0():
    assert count_primes(0) == 0

def test_1():
    assert count_primes(1) == 0

def test_2_not_less_than_n():
    assert count_primes(2) == 0

def test_1_prime():
    assert count_primes(3) == 1

def test_example():
    assert count_primes(10) == 4

def test_prime_equal_n_excluded():
    assert count_primes(11) == 4

def test_prime_becomes_included():
    assert count_primes(12) == 5
    
def test_square_is_not_prime():
    assert count_primes(26) == 9

def test_prime_nearup_bound():
    assert count_primes(30) == 10

def test_large_input():
    assert count_primes(50) == 15