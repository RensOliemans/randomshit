import json
from isotopes import isotopes

text = "Once upon a time there was a doctor. Her name was Margaret and the last name resembled german death. That day was a sunday and she didnt have to go to work so she decided to continue writing her first, yet to be published book. Its title was something about escaping and it began with such words: It was a bitter December night, but the Paris-lyon express was speeding gaily along in search of the flowers and the sunshine. After some time passed she decided to go out. She was surprised to meet an old family friend of hers. They talked for a while and exchanged some ideas. Frederick had discovered something but was unsure how to name it and Margaret helped him. He normally was a very stable man and did not break down but it was visible that he really liked the name. After this encounter Margaret decided to call it a day."

elements = dict()


def get_isotopes():
    items = isotopes.split('\n')[1:]
    for item in items:
        parts = item.split('|')
        stable_isotopes = int(parts[6].strip()[:-2])
        element = parts[3].strip()[2:-2]  # eindigt met ']]       ', strip en haal ]] weg
        elements[element] = stable_isotopes

    # override some, long half lifes?
    # elements['tungsten'] = 5  doesn't work
    elements['tellurium'] = 5


get_isotopes()
with open('isotopes', 'w') as f:
    json.dump(elements, f)
