import json
import os

# lets say an items is just a dictionary, with each value being a dictionary.
# these value dictionaries all have some important keys.
# "key" is its key that is used to find the item, LOWER CASE
# "name" is what gets added to the stuff list. 
# "price" is how many gp you have to have to buy it
# "entryCommand" is the command that will be used ot look up the entry in Entry.entryCommands 

def saveItem(item):
    items = {}
    with open("../Items/items.json", 'r') as file:
        items = json.load(file)
        if "key" in item.keys():
            # if there is no name just set the name to the key 
            if "name" in item.keys():
                items[item["key"].lower()]=item
            else:
                item["name"]=item["key"]
                items["key"]=item
            with open("items.json", 'w') as file:
                print("loading item ",item["key"]," lets go")
                with open("../Items/items.json", 'w') as file:
                    json.dump(items, file,indent=4)
        else:
            print("bad Item dictionary trying to get saved here, no key called 'key' for it to be found with", item)



item = {
    "name":"Potion of Healing",
    "key":"potion of healing",
    "price":50,
    "entryCommand":"Potion of Healing"


}

#saveItem(item)