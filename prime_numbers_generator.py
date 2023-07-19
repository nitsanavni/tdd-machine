def prime_numbers_generator(n):
    primes = []
    num = 2
    while len(primes) < n:
        for prime in primes:
            if num % prime == 0:
                break
        else:
            primes.append(num)
        num += 1
    return primes
