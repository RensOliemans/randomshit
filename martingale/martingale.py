import random


def start(amount, total_money, goal):
    initial = amount
    money = total_money
    losses = 0
    while money > 0 and money <= goal:
        earnings, win = bet(min(amount, money))
        money += earnings

        if win:
            losses = 0
            amount = initial
        else:
            # just lost, double betting amount
            losses += 1
            amount *= 2
            if losses > 12:
                print("{} losses in a row, betting amount: {:,}"
                      .format(losses, amount))
    return money


def bet(amount):
    if random.choice([True, False]):
        return (amount * 2, True)
    else:
        return (-amount, False)
