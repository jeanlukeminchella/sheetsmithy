import json
import os
import loadItem

def encode_to_file(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file,indent=4)

armorsToEncode = [["Studded Leather",13,True,False,"Light",False],["Leather",12,True,False,"Light",False], ["Chain Shirt",13,True,False,"Medium",True], ["Breastplate",14,True,False,"Medium",True], ["Hide",12,True,False,"Medium",True], ["Half Plate",15,True,True,"Medium",True],["Scale Mail",14,True,True,"Medium",True], ["Chain Mail",16,False,True,"Heavy",False], ["Splint",17,False,True,"Heavy",False], ["Ring Mail",14,False,True,"Heavy",False], ["Plate",18,False,True,"Heavy",False]]
armorsToEncode = []

for a in armorsToEncode:
    
    armor = {
        "name": a[0],
        "base":a[1],
        "addDex":a[2],
        "stealthDisadvantage":a[3],
        "category":a[4],
        "maxTwo":a[5]
    }
    
    encode_to_file(armor,"./Armors/"+a[0]+".txt")

items = []
with open("./armors5etools.json", 'r') as file:
    items = json.load(file)
#print(items)
for armor in items:
    a =  {}
    a["key"]=armor["title"].lower()
    price = armor["contents"][3]
    price = price[19:-3]
    price = price.replace(",","")
    a["price"] = int(price)
    a["name"]=armor["title"]
    print(a)
    loadItem.saveItem(a)