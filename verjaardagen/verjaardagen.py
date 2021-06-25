from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class Entity:
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date

    def age_relative(self, moment=None):
        moment = datetime.now() if moment is None else moment
        return relativedelta(moment, self.birth_date)

    def age_timedelta(self, moment=None):
        moment = datetime.now() if moment is None else moment
        return moment - self.birth_date

    @classmethod
    def years(cls, x, moment=None):
        return x.age_relative(moment).years

    @classmethod
    def days(cls, x, moment=None):
        return x.age_timedelta(moment).days


class PartyDate:
    def __init__(self, entities, moment=None):
        if moment is None:
            moment = datetime.now()
        self.moment = moment
        self.entities = entities

    @property
    def years(self):
        return self._add_multiple(lambda x: x.age_relative(self.moment).years)

    @property
    def days(self):
        return self._add_multiple(lambda x: x.age_relative(self.moment).days)

    @property
    def years_total(self):
        return self._add_multiple(lambda x: x.age_relative(self.moment), relativedelta()).years

    def __str__(self):
        return f"On {self.moment.strftime('%Y-%m-%d')} {self.years} years, {self.days} days, " \
               f"{self.years_total} 'total' years old."

    def _add_multiple(self, method, start=0):
        assert len(self.entities) > 1, "At least 2 entities"

        total = start
        for entity in self.entities:
            total += method(entity)
        return total


a = datetime.now()

pa = Entity('pa', datetime(1963, 1, 25))
ma = Entity('ma', datetime(1965, 4, 29))
jelle = Entity('jelle', datetime(1994, 7, 30))
rens = Entity('rens', datetime(1997, 3, 15))
ruben = Entity('ruben', datetime(1999, 7, 14))

titia = Entity('titia', datetime(1992, 9, 29))
iris = Entity('iris', datetime(1997, 12, 19))

wammes = Entity('wammes', datetime(2010, 5, 6))

gezin = [pa, ma, jelle, rens, ruben]
met_aanhang = gezin + [titia, iris]
met_wams = met_aanhang + [wammes]


date = datetime(2021, 5, 18)
print(PartyDate(gezin, date))
print(PartyDate(met_aanhang, date))
print(PartyDate(met_wams, date))
print()

date = datetime(2021, 5, 19)
print(PartyDate(gezin, date))
print(PartyDate(met_aanhang, date))
print(PartyDate(met_wams, date))

print()
date = datetime(2021, 6, 29)
print(PartyDate(gezin, date))
print(PartyDate(met_aanhang, date))
print(PartyDate(met_wams, date))

print()
date = datetime(2021, 6, 30)
print(PartyDate(gezin, date))
print(PartyDate(met_aanhang, date))
print(PartyDate(met_wams, date))


