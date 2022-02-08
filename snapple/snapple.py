import json
import os
from random import choice

current_dir = os.path.dirname(os.path.realpath(__file__))
FILENAME = current_dir + "/all_facts.json"

fact_json = json.load(open(FILENAME))

facts = [fact_json[x]["d"] for x in fact_json]
print(choice(facts))
