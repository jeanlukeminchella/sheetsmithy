import globalFunctions as gf
import json
import os
textEntries = {}
spellEntries = {}
attackEntries = {}

allEntries ={}

fileExtension = ".json"

with open(gf.pathToSource+"Entries/TextEntries.txt", 'r') as file:
    textEntries = json.load(file)

print()

print(os.listdir("./Entries/Spells"))

print()

spellStrings = os.listdir("./Entries/Spells")
spellStrings.sort()

for spellString in spellStrings:

    d = json.load(open("./Entries/Spells/"+spellString))
    
    newKey = d["title"]
    newValue = {}

    for key in d.keys():
        if key!="title":
            if d[key]!="":
                value = d[key]
                irreleventKey = False
                if key=="conc" and d[key]==False:
                    irreleventKey = True
                if key=="modiferIndex":
                    if d[key]==-1:
                        irreleventKey = True
                    key = "modifierIndex"
                    
                if key=="rang" and d[key]==0:
                    irreleventKey = True
                
                if key=="forcedMod":
                    if d[key]==-1:
                        irreleventKey = True
                    key = "modifierIndex"

                if key=="castTime" and d[key]=="a":
                    irreleventKey = True
                if key=="ritual" and d[key]==False:
                    irreleventKey = True
                if key=="isSpell":
                    key = "useSpellcastingMod"


                if not irreleventKey:
                    newValue[key]=value
    spellEntries[newKey]=newValue

attackStrings = os.listdir("./Entries/AttackRolls")
attackStrings.sort()

for attackString in attackStrings:

    d = json.load(open("./Entries/AttackRolls/"+attackString))
    
    newKey = d["title"]
    newValue = {}

    for key in d.keys():
        if key!="title":
            if d[key]!="":
                value = d[key]
                irreleventKey = False
                if key=="conc" and d[key]==False:
                    irreleventKey = True
                if key=="modiferIndex":
                    if d[key]==-1:
                        irreleventKey = True
                    key = "modifierIndex"
                    
                if key=="rang" and d[key]==0:
                    irreleventKey = True
                
                if key=="forcedMod":
                    if d[key]==-1:
                        irreleventKey = True
                    key = "modifierIndex"

                if key=="castTime" and d[key]=="a":
                    irreleventKey = True
                if key=="ritual" and d[key]==False:
                    irreleventKey = True
                if key=="isSpell":
                    key = "useSpellcastingMod"


                if not irreleventKey:
                    newValue[key]=value
    attackEntries[newKey]=newValue

cureWounds = {
    "cost": "1",
    "preHealText": "Heal a target 2d8",
    "postHealText": " hp",
    "type": "heal",
    "useSpellcastingMod": True
}
hw = {
    "cost": "1",
    "preHealText": "Heal a target 2d4",
    "postHealText": " hp",
    "rang": 60,
    "castTime": "ba",
    "type": "heal",
    "useSpellcastingMod": True
}
mhw = {
    "title": "",
    "cost": "3",
    "preHealText": "Up to six creatures regain 2d4",
    "postHealText": " hp",
    "rang": 60,
    "castTime": "ba",
    "type": "heal",
    "useSpellcastingMod": True
}

allEntries["Mass Healing Word"] = mhw
allEntries["Healing Word"] = hw
allEntries["Cure Wounds"] = cureWounds

print()
for k in attackEntries.keys():
    print(k, " ",attackEntries[k])
    print()

for key in attackEntries.keys():
    value=  attackEntries[key]
    value["type"]="attack"
    allEntries[key]=value

print()

for k in spellEntries.keys():
    print(k, " ",spellEntries[k])
    print()

for key in spellEntries.keys():
    value=  spellEntries[key]
    value["type"]="spell"
    allEntries[key]=value

print()
for key in textEntries.keys():
    value={}

    value["type"]="text"
    value["contents"]=  textEntries[key]
    allEntries[key]=value

json.dump(allEntries, open("./Entries.json", 'w'),indent=4)

#print(textEntries)