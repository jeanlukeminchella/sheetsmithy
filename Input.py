from dataclasses import dataclass
import globalFunctions as gf


class Input():
    
    def __init__(self):
        
        self.level = None
        self.classAsString=""
        self.scores = None
        self.race={}
        self.showScores = False
        self.showBuildLog = False
        self.showShortRest = False
        self.showLongRest = False
        self.gearList = ""
        self.languages = ""
        self.shoppingList = ""
        self.background={}
        self.choices = {}
        self.name=""
        
        self.showScores = False

    # takes list of [[attributeLabel,value]] and load it into self
    def loadInput(self,commands):
        print(commands)
        for command in commands:
            self.changeAttribute(command[0],command[1])
    
    def printMe(self):
        print()
        print(self.level)
        print(self.classAsString)
        print(self.scores)
        print(self.race)
        print(self.showScores)
        print(self.showBuildLog)
        print(self.showShortRest)
        print(self.showLongRest)
        print(self.shoppingList)
        print(self.background)
        print(self.choices)
        print(self.name)
    
    # takes a string as a label for the attribute, then changes it to value. input probably needs checking like
    def changeAttribute(self, attributeLabel, value):
        if attributeLabel == "level":
            self.level = gf.validateInt(value,1,1,6)
        elif attributeLabel == "classAsString":
            self.classAsString = gf.validateString(value)
        elif attributeLabel == "scores":
            self.scores = gf.validateIntList(value, 10, 6, 0,20)
        elif attributeLabel == "shoppingList":
            self.shoppingList = value
        elif attributeLabel == "showScores":
            self.showScores = gf.validateBoolean(value)
        elif attributeLabel == "showBuildLog":
            self.showBuildLog = gf.validateBoolean(value)
        elif attributeLabel == "showShortRest":
            self.showShortRest = gf.validateBoolean(value)
        elif attributeLabel == "showLongRest":
            self.showLongRest = gf.validateBoolean(value)
        elif attributeLabel == "name":
            self.name = value
        elif attributeLabel == "background":
            self.background = value
        elif attributeLabel == "gearList":
            self.gearList = value
        elif attributeLabel == "languages":
            self.languages = value
        elif attributeLabel == "race":
            self.race = value
        elif attributeLabel == "choices":
            self.choices = value
        else:
            print("attribute label ",attributeLabel," not found while trying to change it on input for ",self.classAsString)
            

    