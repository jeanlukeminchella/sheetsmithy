import json
import os
import loadItem

def encode_to_file(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file,indent=4)


items = []
with open("./items5etools.json", 'r') as file:
    items = json.load(file)
#print(items)
items = []

# loads items from 5e tools and puts them in the item json for adding to inventories 
for item in items:
    tags = item["tags"]
    weapon = False
    dealing = False
    for tag in tags:
        if "weapon" in tag:
            weapon = True

    if weapon:

        a =  {}
        a["key"]=item["title"].lower()
        a["name"]=item["title"]
        a["entryCommand"]=item["title"]
        
        contents = item["contents"]
        for content in contents:
            if "property | Value " in content:
                price = content[19:-3]
                price = price.replace(",","")
                try:
                        
                    price = int(price)
                    if "sp" in content[-3:]:
                        price = price / 10
                    if "cp" in content[-3:]:
                        price = price / 100

                    a["price"] = price
                except:
                    print("likely error inting this ", price," for ",item["title"])
            
        print(a)
        loadItem.saveItem(a)


    
heal = {
    "title":"Healing Word",
    "damage":"",
    "rang":60,
    "cost":"1",
    "duration":"",
    "conc":False,
    "preHealText":"Heal a target d4",
    "postHealText":" hp",
    "modiferIndex":-1,
    "castTime":"ba",
    "ritual":False
}

healName = "healingWord.txt"

#encode_to_file(heal,"./Heals/"+healName)





