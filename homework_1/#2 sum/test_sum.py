from sum import max_even_sum

def test_even_answer():
    assert max_even_sum([5, 7, 13, 2, 14]) == 36

def test_1_odd_number():
    assert max_even_sum([3]) == 0

def test_all_even():
    assert max_even_sum([2, 4, 6]) == 12

def test_2_odd_numbers():
    assert max_even_sum([3, 5]) == 8

def test_3_odd_numbers():
    assert max_even_sum([3, 5, 7]) == 12

def test_even_total_mix():
    assert max_even_sum([2, 3, 4, 5]) == 14

def test_1_even_number():
    assert max_even_sum([8]) == 8

def test_smallest_odd_no_1():
    assert max_even_sum([9, 2, 3, 5]) == 16

def test_equal_smallest_odd():
    assert max_even_sum([1, 1, 3]) == 4