
import json
import os

def encode_to_file(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file,indent=4)
        
# type: spell / text / heal / attackRoll     
# code is what loads the JSON 
spellCommand = {
    "type":"",
    "code":"",
}

spellCommands={}

entryBuckets = [["Spells","spell"],["AttackRolls","attackRoll"],["Heals","heal"]]
for entryBucket in entryBuckets:
        
    seeds = os.listdir("../Entries/"+entryBucket[0])
    for seed in seeds:
            
        with open("../Entries/"+entryBucket[0]+"/"+seed, 'r') as file:
            d = json.load(file)
            code = seed.split(".")
            code = code[0]
            spellCommands[d["title"]]={
                "type":entryBucket[1],
                "code":code
            }

d = {}
with open("../Entries/TextEntries.txt", 'r') as file:
    d = json.load(file)
    
for c in d.keys():
    spellCommands[c]={
                    "type":"text",
                    "code":c
                }

spellCommandsName = "../Entries/spellCommands.json"
encode_to_file(spellCommands,spellCommandsName)

d = {}
with open("../Entries/spellCommands.json", 'r') as file:
    d = json.load(file)

for k in d.keys():
    print(k,d[k])