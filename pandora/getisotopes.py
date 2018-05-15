import json
from isotopes import isotopes

elements = dict()


def get_isotopes():
    items = isotopes.split('\n')[1:]
    for item in items:
        parts = item.split('|')
        stable_isotopes = int(parts[6].strip()[:-2])
        element = parts[3].strip()[2:-2]  # eindigt met ']]       ', strip en haal ]] weg
        elements[element] = stable_isotopes

    # override some, long half lifes?
    # elements['tungsten'] = 5  # doesn't work
    elements['tellurium'] = 5


get_isotopes()
with open('isotopes', 'w') as f:
    json.dump(elements, f)
