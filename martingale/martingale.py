import begin
from random import random


def bet(amount):
    if random() < 0.5:
        return (amount * 2, True)
    else:
        return (-amount, False)


@begin.start(auto_convert=True)
def start(a: 'Amount' = 1, t: 'Total_money' = 10000, g: 'Goal' = 50000):
    initial = a
    money = t
    losses = 0
    while money > 0 and money <= g:
        earnings, win = bet(min(a, money))
        money += earnings

        if win:
            losses = 0
            a = initial
        else:
            # just lost, double betting amount
            losses += 1
            a *= 2
            if losses > 12:
                print("{} losses in a row, betting amount: {:,}"
                      .format(losses, a))
                print(money)
    print(money)
    return money
