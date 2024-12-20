import json
import os

def encode_to_file(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file,indent=4)

spell = {
    "title":"Barkskin",
    "rang":0,
    "cost":"2",
    "duration":"1 hour",
    "conc":False,
    "modiferIndex":-1,
    "preSaveNormalText":"Target's AC is at least 17.",
    "postSaveNormalText":"",
    "preSaveItalicText":"",
    "postSaveItalicText":"",
    "castTime":"ba",
    "ritual":False
}
spellName = "Barkskin.json"
encode_to_file(spell,"../Entries/Spells/"+spellName)
import spellCommandLoader