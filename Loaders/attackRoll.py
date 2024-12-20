
import json
import os

def encode_to_file(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file,indent=4)

attack = {
    "title":"Produce Flame",
    "damage":"d8",
    "rang":60,
    "cost":"",
    "duration":"",
    "conc":False,
    "addModToDamage":False,
    "damageType":"fire",
    "forcedMod":-1,
    "cantripScaling":True,
    "saveNotAttack":False,
    "resistAttributeText":"",
    "resistText":"",
    "note":"",
    "isSpell":True
}
attackName = "Produce Flame.json"
encode_to_file(attack,"../Entries/AttackRolls/"+attackName)
import spellCommandLoader