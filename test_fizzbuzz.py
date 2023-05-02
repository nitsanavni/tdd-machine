from fizzbuzz import fizzbuzz

def test_fizzbuzz_divisible_by_3():
    assert fizzbuzz(3) == 'Fizz'

def test_fizzbuzz_divisible_by_5():
    assert fizzbuzz(5) == 'Buzz'

def test_fizzbuzz_divisible_by_both_3_and_5():
    assert fizzbuzz(15) == 'FizzBuzz'

def test_fizzbuzz_not_divisible_by_3_or_5():
    assert fizzbuzz(4) == 4
