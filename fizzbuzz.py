def fizzbuzz(number: int, check_list=[(3, 'Fizz'), (5, 'Buzz')]):
    return ''.join((str(string) if number % divisor == 0 else '') for divisor, string in check_list) or number
