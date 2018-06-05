class Gebouw:

    def __init__(self, number, name, abbreviation):
        self.number = number
        self.name = name
        self.abbreviation = abbreviation

    def __eq__(self, other):
        if type(other) == type(self):
            return self.number == other.number
        if type(other) == int:
            return self.number == other
        if type(other) == str:
            return self.name == other or self.abbreviation == other
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.number} - {self.name} ({self.abbreviation})"

    def __contains__(self, x):
        return x in self.name.lower()

    def __len__(self):
        return len(self.name)


class Kunst:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if type(other) == type(self):
            return self.name == other.name
        if type(other) == str:
            return self.name == other
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __contains__(self, x):
        return x in self.name.lower()

    def __len__(self):
        return len(self.name)
