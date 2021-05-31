from random import SystemRandom

r = SystemRandom()


class Game:
    def __init__(self, people):
        self.people = people
        assert len(people) > 0, "Has to be a sequence of at least length 1"

    def roll(self):
        number = r.uniform(0.0, 60.0)
        return sorted(self.people, key=lambda person: abs(number - person.guess))[0]


class Person:
    def __init__(self):
        self.guess = r.uniform(0.0, 60.0)


class DirtyA(Person):
    def __repr__(self):
        return f'<DirtyA. Guess: {self.guess}>'


class Vicky(Person):
    def __init__(self):
        super().__init__()
        self.guess = r.uniform(0.0, 15.0)

    def __repr__(self):
        return f'<Vicky. Guess: {self.guess}>'


class Other(Person):
    def __repr__(self):
        return f'<Other. Guess: {self.guess}>'
