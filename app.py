from flask import Flask, render_template, request, redirect
import growSeeds

app = Flask(__name__)

from urllib.parse import urlparse, urlunparse

FROM_DOMAIN = "sheetsmithy.pythonanywhere.com"
TO_DOMAIN = "www.sheetsmithy.com"

@app.before_request
def redirect_to_new_domain():
    urlparts = urlparse(request.url)
    if urlparts.netloc == FROM_DOMAIN:
        urlparts_list = list(urlparts)
        urlparts_list[1] = TO_DOMAIN
        return redirect(urlunparse(urlparts_list), code=301)

@app.route('/', methods=["POST","GET"])
def hello_world():
    if request.method == "POST":
        d = request.form

        #print("This is what we got from the website: ",d)
        
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

            if int(d["considerLangs"])>0:
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
            if inp["classAsString"]=="Fighter":
                choicesDic["subclass"]=d["fighterSubclass"]
            if inp["classAsString"]=="Rogue":
                choicesDic["subclass"]=d["rogueSubclass"]
            if inp["classAsString"]=="Ranger":
                choicesDic["subclass"]=d["rangerSubclass"]
            if inp["classAsString"]=="Cleric":
                choicesDic["divineOrder"]=d["divineOrder"]
        except:
            print("issue handling subclass")    
        if len(choicesDic.keys())>0:
            inp["choices"]=choicesDic

        attributes =  ["Strength","Dexterity","Constitution","Intelligence","Wisdom","Charisma"]
        scores = []
        userHasChosenAScore = False
        try:

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
        except:
            print("issue picking scores") 
        
        return growSeeds.getHTMLFromInput(inp)
    else:
        return render_template("index.html")

