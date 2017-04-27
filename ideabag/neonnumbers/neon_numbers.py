def is_neon_number(number):
    squared = pow(number, 2)
    total = 0
    for digit in str(squared):
        total += int(digit)
    return total == number

def find_neon_numbers(start=1, end=1000):
    numbers = list()
    for i in range(start, end):
        if is_neon_number(i):
            numbers.append(i)
    return numbers
