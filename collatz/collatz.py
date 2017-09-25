import time

def check(n, checked_items=[]):
    if n in checked_items:
        return checked_items
    elif n % 2 == 0:
        checked_items.append(n)
        return check(n // 2, checked_items)
    else:
        checked_items.append(n)
        return check(3*n + 1, checked_items)

def go(n, single=False, verbose=True):
    start = time.time()
    if single:
        print("x: {}, items: {}".format(n, check(n)))
    else:
        checked_items = list()
        for x in range(1, n + 1):
            new_checked_items = check(x, checked_items)
            #checked_items += new_checked_items
            if verbose:
                print("x: {}, items: {}".format(x, new_checked_items))
            elif x % 100 == 0:
                print(x)

    print("Time consumed: {}".format(time.time() - start))
