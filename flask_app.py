from flask import Flask, render_template, request

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


app = Flask(__name__)

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


@app.route('/', methods=["POST","GET"])
def hello_world():
    if request.method == "POST":
        d = request.form

        print("This is what we got from the website: ",d)
        
        # changing form values into one thats readable by the generator
        # get better at javascript and make this pass a more compatible dictionary in the first place? 
        # surely make this more resilient to bad post requests as well? 

        keys = d.keys()
        inp = {}
        
        try:
            inp["level"] = int(d["level"])
        except:
            print("issue loading / parsing level from input")
        
        try:
            inp["classAsString"] = str(d["classAsString"])
        except:
            print("issue loading / parsing class from input")
        
        
        
        bools = ["showShortRest","showLongRest","showScores"]
        for i in range(len(bools)):
            
            if bools[i] in keys:
                inp[bools[i]] = bool(d[bools[i]])
        if "name" in keys:
            if d["name"]:
                inp["name"] = d["name"]
        
        if "background" in keys:    
            if d["background"]:
                inp["background"] = {
                    "name":d["background"]
                }
        try:
            if d["languages"]!="":
                inp["languages"] = d["languages"]
        except:
            print("we have a problem considering languages")
        try:

            if int(d["considerInventory"])>0:
                inp["shoppingList"]=d["shoppingList"]
                inp["gearList"]=d["gearList"]
        except:
            print("we have a problem considering inventory")

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
            print("weve had an issue handing species") 

        choicesDic = {}
        try:

            if inp["classAsString"]=="Barbarian":
                choicesDic["subclass"]=d["barbarianSubclass"]
            if inp["classAsString"]=="Monk":
                choicesDic["subclass"]=d["monkSubclass"]
            if inp["classAsString"]=="Paladin":
                choicesDic["subclass"]=d["paladinSubclass"]
            if inp["classAsString"]=="Fighter":
                choicesDic["subclass"]=d["fighterSubclass"]
            if inp["classAsString"]=="Rogue":
                choicesDic["subclass"]=d["rogueSubclass"]
            if inp["classAsString"]=="Ranger":
                choicesDic["subclass"]=d["rangerSubclass"]
            if inp["classAsString"]=="Cleric":
                choicesDic["divineOrder"]=d["divineOrder"]
            if inp["classAsString"]=="Druid":
                choicesDic["primalOrder"]=d["primalOrder"]
        except:
            print("issue handling subclass")    
        if len(choicesDic.keys())>0:
            inp["choices"]=choicesDic

        attributes =  ["Strength","Dexterity","Constitution","Intelligence","Wisdom","Charisma"]
        scores = []
        userHasChosenAScore = False
        try:

            for a in attributes:
                chosenScore = d[a]
                if chosenScore == "":
                    scores.append(10)
                else:
                    scores.append(chosenScore)
                    userHasChosenAScore = True
            if userHasChosenAScore:
                inp["scores"]=scores
        except:
            print("issue picking scores") 
        
        return getHTMLFromInput(inp)
    else:
        return render_template("index.html")

