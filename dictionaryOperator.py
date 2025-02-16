import globalFunctions as gf
import json
import os
textEntries = {}
spellEntries = {}

allEntries ={}

fileExtension = ".json"

with open(gf.pathToSource+"Entries/TextEntries.txt", 'r') as file:
    textEntries = json.load(file)

print()

print(os.listdir("./Entries/Spells"))

print()

spellStrings = os.listdir("./Entries/Spells")

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

for k in spellEntries.keys():
    print(k, " ",spellEntries[k])
    print()

print()

for key in spellEntries.keys():
    value=  spellEntries[key]
    value["type"]="spell"
    allEntries[key]=value


for key in textEntries.keys():
    value={}

    value["type"]="text"
    value["contents"]=  textEntries[key]
    allEntries[key]=value

json.dump(allEntries, open("./Entries.json", 'w'),indent=4)

#print(textEntries)