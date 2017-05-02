import time


class Country(object):

    def __init__(self, name, continent, **kwargs):
        self.name = name
        self.continent = continent

        if kwargs is not None:
            self.capital = kwargs.get('capital')
            self.size = kwargs.get('size', 0)
            self.cities = kwargs.get('cities', list())
            self.currency = kwargs.get('currency', 'Euro')
            self.inet_code = kwargs.get('inet_code', "")
            self.un_index = kwargs.get('un_index')
            self.time_zone = kwargs.get('timezone')

        self.population = dict()
        self.gdp = dict()
        self.life_expectancy = dict()
        self.unemployment_rate = dict()

    def __str__(self):
        return "{0}".format(self.name)

    def __repr__(self):
        return ("Country: {0} in continent: {1}"
                .format(self.name, self.continent))

    def set_inet_code(self, code):
        self.inet_code = code

    def set_population(self, population, year=time.strftime("%Y")):
        self.population[year] = population

    def set_gdp(self, gdp, year=time.strftime("%Y")):
        self.gdp[year] = gdp

    def set_life_expectancy(self, expectancy, year=time.strftime("%Y")):
        self.life_expectancy[year] = expectancy

    def set_unemployment_rate(self, rate, year=time.strftime("%Y")):
        if not isinstance(rate, float):
            raise ValueError
        if 0 <= rate <= 1:
            self.unemployment_rate[year] = rate
        else:
            raise ValueError

    def set_un_development_index(self, un_index, year=time.strftime("%Y")):
        self.un_index[year] = un_index

    def add_city(self, city):
        self.cities.append(city)

    def add_cities(self, cities):
        for city in cities:
            self.cities.append(city)


class City(object):

    def __init__(self, name, country, **kwargs):
        self.name = name
        self.country = country
        self.population = dict()

        if kwargs is not None:
            self.size = kwargs.get('size')
            self.time_zone = kwargs.get('timezone')

    def __str__(self):
        return "{0}".format(self.name)

    def __repr__(self):
        return "City: {0} in country: {1}".format(self.name, self.country)

    def set_population(self, population, year=time.strftime("%Y")):
        self.population[year] = population

    def set_size(self, size):
        self.size = size

    def set_time_zone(self, time_zone):
        self.time_zone = time_zone
