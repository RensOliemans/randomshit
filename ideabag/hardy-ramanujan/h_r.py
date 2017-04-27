import math

def is_h_r_number(number, pow_level=3):
    ways = list()
    min_number = math.ceil(pow(number, 1/pow_level))
    for i in range(1, min_number):
        for j in range(1, min_number):
            if (j, i) not in ways:
                if pow(i, pow_level) + pow(j, pow_level) == number:
                    ways.append((i, j))
    return ways
                

def find_hr_numbers(start=1, end=1000, pow_level=3):
    numbers = dict()
    for i in range(start, end):
        result = is_h_r_number(i, pow_level)
        if len(result) > 1:
            numbers[i] = result
    return numbers
