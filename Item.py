import globalFunctions as gf
import json
import os

# lets say an items is just a dictionary, with each value being a dictionary.
# these value dictionaries all have some important keys.
# "key" is its key that is used to find the item, LOWER CASE
# "name" is what gets added to the stuff list. 
# "price" is how many gp you have to have to buy it
# "entryCommand" is the command that will be used ot look up the entry in Entry.entryCommands 

items = {}
with open(gf.pathToSource+"Items/items.json", 'r') as file:
    items = json.load(file)

# returns False if not added ?
def buyItem(c,itemCommand, spendCash=True):
    
    item = None
    if itemCommand.lower() in items.keys():
        # Item is in the dictionary and can be loaded in with ease
        item = items[itemCommand.lower()]
        
        if "price" in item.keys():
            if spendCash:        
                if item["price"]<=c.gp:
                    # weve got enough gold, lets buy it
                    c.gp = c.gp - item["price"]
                else:
                    # oh dear, not enough gold
                    c.buildLog.append("Not enough gold to buy "+item["name"]+" only "+str(c.gp)+" gp left")
                    #print("Not enough gold to buy "+item["name"]+" only "+str(c.gp)+" gp left")
                    return False
        # if weve got this far then weve either bought the item or it has no cost
        c.addItemToInventory(item["name"])
        if "entryCommand" in item.keys():
            c.addEntry(item["entryCommand"])
    
    else:
        print("Unrecognised item ", itemCommand)
        c.addItemToInventory(itemCommand+" <em>(price unknown)</em>")
        return True
    

