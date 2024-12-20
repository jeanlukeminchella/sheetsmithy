import Entry as e
import json
import globalFunctions as gf

class Armor:
    def __init__(self):
        pass

    def actionCommand(self,command,value):
        if command == "base":
            self.base = value
        elif command=="addDex":
            self.addDex = value
        elif command == "name":
            self.name=value
        elif command == "stealthDisadvantage":
            self.stealthDisadvantage = value
        elif command=="category":
            self.category = value
        elif command=="maxTwo":
            self.maxTwo = value
    
    def loadArmor(self,armorName):
        
        d = {}
        
        with open(gf.pathToSource+"Armors/"+armorName+e.fileExtension, 'r') as file:
            d = json.load(file)
        
        for k in d.keys():
            
            self.actionCommand(k,d[k])

