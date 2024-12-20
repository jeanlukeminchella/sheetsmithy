import Input as i
from Classes import Barbarian as barb
from Classes import Fighter as fighter
from Classes import Rogue as rogue
from Classes import Druid as druid
from Classes import Monk as monk
from Classes import Ranger as ranger
from Classes import Paladin as pal
from Classes import Cleric as cleric
import datetime
import os
import webbrowser
import shutil
import json

pathToLoad = "file:///media/fuse/crostini_c198dff15dfd992cb319b5ca255e286f9ff04409_termina_penguin/SheetSmithy/Generated/"


def getTimeAsString():
    result = ""
    x= datetime.datetime.now()
    result += x.strftime("%y")
    result += "-"+x.strftime("%m")
    result += "-"+x.strftime("%d")
    result += "-"+x.strftime("%H")
    result += "-"+x.strftime("%M")
    result += "-"+x.strftime("%S")
    return result

def getHTMLFromInput(d):

    inp = i.Input()
    inp.loadInput(list(d.items()))

    c = inp.classAsString
    character = None

    if c=="Fighter":
        character = fighter.Fighter(inp)
    elif c=="Rogue":
        character = rogue.Rogue(inp)
    elif c=="Druid":
        character = druid.Druid(inp)
    elif c=="Monk":
        character = monk.Monk(inp)
    elif c=="Barbarian":
        character = barb.Barbarian(inp)
    elif c=="Ranger":
        character = ranger.Ranger(inp)
    elif c=="Paladin":
        character = pal.Paladin(inp)
    elif c=="Cleric":
        character = cleric.Cleric(inp)
    else:
        inp.classAsString="Fighter"
        character = fighter.Fighter(inp)

    return(character.generateClassHTML())

#growSeeds()