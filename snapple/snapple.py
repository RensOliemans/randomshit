import json
from random import sample

FILENAME = 'all_facts.json'

fact_json = json.load(open(FILENAME))

facts = [fact_json[x]['d'] for x in fact_json]
print(sample(list(facts), 1))
