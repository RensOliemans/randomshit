import json
from random import choice

FILENAME = '/home/rens/Projects/randomshit/snapple/all_facts.json'

fact_json = json.load(open(FILENAME))

facts = [fact_json[x]['d'] for x in fact_json]
print(choice(facts))
