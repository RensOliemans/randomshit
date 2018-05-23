class Gebouw:

    def __init__(self, nummer, naam, afkorting, kunstwerk=False):
        self.nummer = nummer
        self.naam = naam
        self.afkorting = afkorting
        self.kunstwerk = kunstwerk

    def __eq__(self, other):
        if type(other) == type(self):
            return self.nummer == other.nummer
        if type(other) == int:
            return self.nummer == other
        if type(other) == str:
            return self.naam == other or self.afkorting == other
        return False

    def __str__(self):
        return self.naam

    def __repr__(self):
        return "{} - {} ({})".format(self.nummer, self.naam, self.afkorting)

    def __contains__(self, x):
        return x in self.naam.lower()

    def __len__(self):
        return len(self.naam)


class Kunst:

    def __init__(self, naam):
        self.naam = naam

    def __eq__(self, other):
        if type(other) == type(self):
            return self.naam == other.naam
        if type(other) == str:
            return self.naam == other
        return False

    def __str__(self):
        return self.naam

    def __repr__(self):
        return str(self)

    def __contains__(self, x):
        return x in self.naam.lower()

    def __len__(self):
        return len(self.naam)
