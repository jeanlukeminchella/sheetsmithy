import json
import filecmp

def encode_to_file(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file,indent=4)



attack = {
    "title":"Greatsword",
    "damage":"d8",
    "rang":0,
    "cost":"",
    "duration":"",
    "conc":False,
    "addModToDamage":True,
    "damageType":None,
    "forcedMod":-1,
    "cantripScaling":False,
    "saveNotAttack":False,
    "resistAttributeText":"",
    "resistText":"",
    "note":""
}



items = []
with open("./items5etools.json", 'r') as file:
    items = json.load(file)
#print(items)
#items = []

# loads items from 5e tools and puts them in the AttackRolls folder
for item in items:
    tags = item["tags"]
    weapon = False
    dealing = False
    for tag in tags:
        if "weapon" in tag:
            weapon = True

    if weapon:

        a =  {}
        a["title"]=item["title"]
        a["addModToDamage"]=True
        a["forcedMod"]=0
        contents = item["contents"]
        for content in contents:
            
            if "property | Damage | " in  content:
                damage = content[20:]
                if "Bludgeoning" in damage:
                    damage = damage.replace(" Bludgeoning","")
                    a["damageType"]="Bludgeoning"
                if "Piercing" in damage:
                    damage = damage.replace(" Piercing","")
                    a["damageType"]="Piercing"
                if "Slashing" in damage:
                    damage = damage.replace(" Slashing","")
                    a["damageType"]="Slashing"
                if "Psychic" in damage:
                    damage = damage.replace(" Psychic","")
                    a["damageType"]="Psychic"
                
                if damage[:2]=="1d":
                    damage = damage[1:]
                a["damage"]=damage
            if "property | Properties" in content:
                if "Thrown" in content:
                    i = content.index("Thrown")
                    thrownText = content[i+8:]
                    j = thrownText.index("/")
                    a["thrown"]=int(thrownText[:j])
                if "Finesse" in content:
                    a["finesse"]=True
                if "Versatile" in content:
                    # does not load anything with 2d6 as versatile damage for example, 
                    i = content.index("Versatile")
                    versatileText = content[i+12:]
                    j = versatileText.index(")")
                    a["versatile"]= versatileText[:j]
                if "Reach" in content:
                    a["reach"]=True
                if "Ammunition" in content:
                    a["forcedMod"]=1
                    i = content.index("Ammunition")
                    ammoText = content[i+18:]
                    j = ammoText.index("/")
                    a["rang"]= int(ammoText[:j])
            if "property | Mastery |" in content:
                mastery = content[-15:]
                mastery = mastery[:-7]
                i = mastery.index(">")
                mastery = mastery[i+1:]
                a["mastery"]=mastery





            

            
        print(a)
        encode_to_file(a,"../Entries/AttackRolls/"+item["title"]+".json")