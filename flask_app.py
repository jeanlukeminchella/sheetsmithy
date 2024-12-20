from flask import Flask, render_template, request
import growSeeds

app = Flask(__name__)

@app.route('/', methods=["POST","GET"])
def hello_world():
    if request.method == "POST":
        d = request.form
        
        # changing form values into one thats readable by the generator
        # get better at javascript and make this pass a more compatible dictionary in the first place? 
        # surely make this more resilient to bad post requests as well? 

        inp = {}
        
        inp["level"] = d["level"]
        inp["classAsString"] = d["classAsString"]
        bools = ["showShortRest","showLongRest","showScores"]
        keys = d.keys()
        for i in range(len(bools)):
            
            if bools[i] in keys:
                inp[bools[i]] = bool(d[bools[i]])
        if d["name"]:
            inp["name"] = d["name"]
        
        if d["background"]:
            inp["background"] = {
                "name":d["background"]
            }

        if int(d["considerInventory"])>0:
            inp["shoppingList"]=d["shoppingList"]
            inp["gearList"]=d["gearList"]
        
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
            
        choicesDic = {}
        if inp["classAsString"]=="Barbarian":
            choicesDic["subclass"]=d["barbarianSubclass"]
        if inp["classAsString"]=="Fighter":
            choicesDic["subclass"]=d["fighterSubclass"]
        if inp["classAsString"]=="Rogue":
            choicesDic["subclass"]=d["rogueSubclass"]
        if inp["classAsString"]=="Ranger":
            choicesDic["subclass"]=d["rangerSubclass"]
        if inp["classAsString"]=="Cleric":
            choicesDic["divineOrder"]=d["divineOrder"]
        if len(choicesDic.keys())>0:
            inp["choices"]=choicesDic

        attributes =  ["Strength","Dexterity","Constitution","Intelligence","Wisdom","Charisma"]
        scores = []
        userHasChosenAScore = False
        if int(d["pickedScores"])>0:
            for a in attributes:
                chosenScore = d[a]
                if chosenScore == "":
                    scores.append(10)
                else:
                    scores.append(chosenScore)
                    userHasChosenAScore = True
            if userHasChosenAScore:
                inp["scores"]=scores
            
        
        return growSeeds.getHTMLFromInput(inp)
    else:
        return render_template("index.html")

