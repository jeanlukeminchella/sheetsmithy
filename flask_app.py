from flask import Flask, redirect, render_template, request, url_for

from Classes import Barbarian as barb
from Classes import Fighter as fighter
from Classes import Rogue as rogue
from Classes import Druid as druid
from Classes import Monk as monk
from Classes import Ranger as ranger
from Classes import Paladin as pal
from Classes import Cleric as cleric
from Classes import Warlock as warlock
import Class as Sheet

app = Flask(__name__)

def getHTMLFromInput(d):

    inp = {
        "classAsString":"",
        "scores" : None,
        "race":{},
        "showScores" : False,
        "showBuildLog" : False,
        "showShortRest" : True,
        "showLongRest" : True,
        "showPhysicalDamageTypes" : True,
        "gearList" : "",
        "bonusGold" : 0,
        "languages" : "",
        "shoppingList" : "",
        "background":{},
        "seed":0,
        "choices" : {},
        "name":"",
        "level":None
    }

    for key in d.keys():
        inp[key]=d[key]

    race = inp["race"]

    if race=={}:
        races = [{"name":"human"},{"name":"gnome"},{"name":"tiefling"},{"name":"elf"},{"name":"goliath"},{"name":"aasimar"},{"name":"halfling"},{"name":"orc"},{"name":"dwarf"}]
        cIndex = inp["seed"]%(len(races))
        inp["race"] = races[cIndex]

    c = inp["classAsString"]
    if c=="":
        classes = ["Fighter","Rogue","Monk","Barbarian","Ranger","Paladin","Cleric"]
        cIndex = inp["seed"]%(len(classes))
        c = classes[cIndex]
        inp["classAsString"] = classes[cIndex]
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
    elif c=="Warlock":
        character = warlock.Warlock(inp)
    else:

        inp["classAsString"]="Fighter"
        character = fighter.Fighter(inp)

    return(character.generateClassHTML())


@app.route('/generate')
def makeSheet():
    d = request.args
    print()
    print("This is what we got from the request: ")
    print(d)
    
    # changing form values into one thats readable by the generator
    # this needs to be resilient to bad  requests as well

    keys = d.keys()
    inp = {}
    
    try:
        inp["level"] = int(d["level"])
    except:
        pass
        #print("issue loading / parsing level from input")
    
    try:
        inp["classAsString"] = str(d["classAsString"])
    except:
        pass
        #print("issue loading / parsing class from input")
    
    if "bonusGold" in d.keys():
        bonusGold = 0
        try:
            bonusGold = float(d["bonusGold"])
            inp["bonusGold"] = bonusGold
        except:
            # issue handling  bonus gold
            pass
    
    bools = ["showShortRest","showLongRest","showScores","showPhysicalDamageTypes"]
    for i in range(len(bools)):
        if bools[i] in keys:
            inp[bools[i]] = bool(d[bools[i]])
    if "name" in keys:
        if d["name"]:
            inp["name"] = d["name"]
    
    if "background" in keys:    
        if d["background"] in Sheet.b.backgrounds.keys():
            inp["background"] = {
                "name":d["background"]
            }
    try:
        if d["languages"]!="":
            inp["languages"] = d["languages"]
    except:
        pass
        #print("we have a problem considering languages")
    try:
        inp["shoppingList"]=d["shoppingList"]
        inp["gearList"]=d["gearList"]
    except:
        pass
        #print("we have a problem considering inventory")

    try:
        if d["race"]:

            raceDic = {
                "name":d["race"]
            }
            if d["race"]=="aasimar":
                raceDic["size"]=d["size"]
            if d["race"]=="goliath":
                raceDic["subrace"]=d["goliathSubrace"]
            if d["race"]=="elf":
                raceDic["subrace"]=d["elfSubrace"]
            if d["race"]=="tiefling":
                raceDic["subrace"]=d["tieflingSubrace"]
                raceDic["size"]=d["size"]
            if d["race"]=="human":
                raceDic["originFeat"]=d["humanFeatChoice"]
            if d["race"]=="gnome":
                raceDic["subrace"]=d["gnomeSubrace"]
            
            inp["race"] = raceDic
    except:
        pass
        #print("weve had an issue handing species") 

    choicesDic = {}

    possibleFeatChoices = ["fightStyle","l4-feat"]

    for choice in possibleFeatChoices:

        if choice in keys:
            if d[choice]!="" and d[choice] in barb.c.feats.Feats.keys():
                choicesDic[choice]=d[choice]

    try:
        if inp["classAsString"]=="Barbarian":
            choicesDic["subclass"]=d["barbarianSubclass"]
        if inp["classAsString"]=="Monk":
            choicesDic["subclass"]=d["monkSubclass"]
        if inp["classAsString"]=="Paladin":
            choicesDic["subclass"]=d["paladinSubclass"]
        if inp["classAsString"]=="Fighter":
            choicesDic["subclass"]=d["fighterSubclass"]
            choicesDic["l6-feat"]=d["l6-feat"]
        if inp["classAsString"]=="Rogue":
            choicesDic["subclass"]=d["rogueSubclass"]
        if inp["classAsString"]=="Ranger":
            choicesDic["subclass"]=d["rangerSubclass"]
        if inp["classAsString"]=="Cleric":
            choicesDic["divineOrder"]=d["divineOrder"]
            choicesDic["subclass"]=d["clericSubclass"]
        if inp["classAsString"]=="Druid":
            choicesDic["primalOrder"]=d["primalOrder"]
    except:
        pass
        print("issue handling subclass")  
    if len(choicesDic.keys())>0:
        inp["choices"]=choicesDic

    attributes =  ["str","dex","con","int","wis","cha"]
    scores = []
    userHasChosenAScore = False
    try:

        for a in attributes:
            chosenScore = d[a]
            if chosenScore == "":
                scores.append(10)
            else:
                scores.append(int(chosenScore))
                userHasChosenAScore = True
        if userHasChosenAScore:
            inp["scores"]=scores
    except:
        pass
        #print("issue picking scores") 
    
    if "seed" in keys:
        inp["seed"]=int(d["seed"])
        
    print()
    print("This is what were sending to the code: ")
    print(inp)
    print()
    return getHTMLFromInput(inp)

@app.route('/')
def landingPad():
    return render_template("index.html")

