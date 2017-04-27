def find_happy_numbers(start=1, amount=None):
    has_end = amount is not None
    numbers = list()
    counter = 0
    i = start
    if has_end:
        while counter < amount:
            if is_happy_number(i):
                numbers.append(i)
                counter += 1
            i += 1
    else:
        while True:
            if is_happy_number(i):
                print(i)
            i += 1
    return numbers


def is_happy_number(number, previous_number=0, iterations=0):
    if number == 1:
        return True
    if iterations >= 100 or number == previous_number:
        return False
    numstr = str(number)
    total = 0
    for digit in numstr:
        total += pow(int(digit), 2)
    return is_happy_number(total, previous_number, iterations + 1)
