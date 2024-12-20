# ccc

import Races as r
import Backgrounds as b
import random as rand

# a character creation choice is a dictionary, this covers racial choices and background for now 


# this checks that the choice is a dictionary, and has vitalKey in keys
# vitalKey in choice dictionary must have a value in vitalKeyValueOptions
def validateChoice(choice, vitalKey, vitalKeyValueOptions,defaultNameIndex=0):
    
    default = {
        vitalKey:vitalKeyValueOptions[defaultNameIndex]
    }
    
    if not type(choice)==dict:
        return default

    keys = choice.keys()
    
    if not vitalKey in keys:
        return default
    else:
        # see if that value is in the list given as acceptable values for the vital key
        if not choice[vitalKey] in vitalKeyValueOptions:
            return default
        else:
            return choice

nameArgumentCommand = "name"

races = r.racesDictionary.keys()
def applyRace(c,choice):
    #lets make sure choise is a dictionary, with a name in races. it picks the first race (human) if any issues
    choice = validateChoice(choice, nameArgumentCommand, list(races))
    #apply race
    r.racesDictionary[choice[nameArgumentCommand]](c,choice)
    
    
backgrounds = list(b.backgrounds.keys())

def applyBackground(c,choice):

    i = rand.randint(0,len(c.preferredBackgrounds)-1)
    preferredBackground = c.preferredBackgrounds[i]
    j= backgrounds.index(preferredBackground)

    #lets make sure choise is a dictionary, with a name in races.
    choice = validateChoice(choice, nameArgumentCommand, list(backgrounds),j)
    c.backgroundAsString= choice[nameArgumentCommand]
    #apply race
    b.backgrounds[choice[nameArgumentCommand]](c,choice)
    

    
    
    
    
    





        