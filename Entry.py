import globalFunctions as gf
import json

fileExtension = ".json"
standardEntryStart = "<p>"
standardEntryEnd = "</p>\n"

allEntries = json.load(open(gf.pathToSource+"entries.json", 'r'))

class Block():
    
    def __init__(self, entries=[], title="",divID=""):
        self.entries = entries
        self.title=title
        self.divID=divID
    
    def addEntry(self, e):
        self.entries.append(e)
        
    def getHTML(self,c=None):
        
        result = ""
        if self.title !="":
            result += "<div id='sectionTitle' class='header'>"+self.title+"</div>\n"
            
        if self.divID !="":
            result += "<div id='"+self.divID+"'>\n"
            
        for e in self.entries:
            
            result += getHTML(e,c)
        
        if self.divID !="":
            result += "</div>\n"
        
        return result
        


# this funciton fills out the entry into a dictionary that has all the keys it needs to make hmtl, including "castTime", "id" and "type"
# returns a blank thruple dictionary if theres an error
# id is used to expand the dictionay, and also identify if a character already has a certain entry
def getExpandedDictionary(e):

    # start with the expanded dictionary being a blank thruple
    expandedDictionary = {
        "castTime":"a",
        "id":"blank",
        "type":"text",
        "expanded":True,
        "conc":False,
        "ritual":False,
        # contents is required for text types
        "contents":["","",""]
    }
    
    #were now trying to parse different inputs, like strings or lists
    if type(e)==str:
        expandedDictionary["contents"][1]=e
        return expandedDictionary

    if type(e)==list:
        if len(e)<4:
            onlyLists = True
            for i in range (len(e)):
                if type(e[i])!=str:
                    try:
                       e[i]=str(e[i]) 
                    except:
                        onlyLists = False
            if onlyLists:
                while len(e)<3:
                    e.append("")
                expandedDictionary["contents"]=e
                return expandedDictionary
    

    
    if type(e)!=dict:
        # if its an int or boolean ect. we can make a string out of it and still display that info
        try:
            expandedDictionary["contents"][1]=str(e)
            return expandedDictionary
        except:
            return expandedDictionary
        
    
        
    # type(e) is definitely dictionary now

    keys = list(e.keys())


    if not "id" in keys:
        #print("weve got a bad entry here with no id- ")
        #print(e)
        return expandedDictionary
    
    #  weve now got a dictionary with an "id" key


    if not e["id"]in allEntries.keys():
        #got an id here that doesnt work
        #print("given ID here that doesnt load an entry",e["id"]," by entry ",e)
        for k in keys:
            expandedDictionary[k]=e[k]
        #print("so we will just return ",expandedDictionary)
        return expandedDictionary
    else:
        loadedDictionary = allEntries[e["id"]]
        for k in loadedDictionary.keys():
            expandedDictionary[k]=loadedDictionary[k]

    # lets add everything useful from the entry into the expanded dictionary, overwriting anything loaded from allEntries
    keysToKeep = ["id","castTime","cost","duration","title","rang","cost","duration","conc","castTime","modifierIndex","preHealText","postHealText","healingBonus","damage","addModToDamage","damageType","cantripScaling","saveNotAttack","resistAttributeText","resistText","note","finesse","reach","versatile","thrown","mastery","preSaveNormalText","postSaveNormalText","preSaveItalicText","postSaveItalicText","ritual","useSpellcastingMod"]
    
    for key in keysToKeep:
        if key in keys:
            expandedDictionary[key]=e[key]

    
    

    
        
    return expandedDictionary

def getHTMLfromThruple(thruple):
    boldBit = thruple[0]
    normalBit = thruple[1]
    italicBit = thruple[2]
    result = standardEntryStart
    if boldBit!= "":
        result+="<strong>"+boldBit+"</strong> "
    
    if normalBit!= "":
        result+=normalBit+" "
    
    
    if italicBit!= "":
        result+="<em>"+italicBit+"</em>"
        
    return result+standardEntryEnd

def getHTML(e,c=None):
    
    #print("input to get hmtl: ",e)
    expanded = False
    if type(e)==dict:
        if "expanded" in e.keys():
            expanded =  e["expanded"]

    if not expanded:
        e = getExpandedDictionary(e)
    #print()
    #print("should be expanded now: ",e)
    #print()
    keys = e.keys()

    if e["type"]=="text":
        return getHTMLfromThruple(e["contents"])
    else:


        defaultBlankStringKeys = ["cost","duration","preHealText","postHealText","damage","resistAttributeText","resistText","note","versatile","mastery","preSaveNormalText","postSaveNormalText","preSaveItalicText","postSaveItalicText"]
        for k in defaultBlankStringKeys:
            if not k in keys:
                e[k]=""


        defaultZeroKeys = ["rang","healingBonus","thrown"]
        for k in defaultZeroKeys:
            if not k in keys:
                e[k]=0

        defaultFalseKeys = ["conc","addModToDamage","cantripScaling","saveNotAttack","finesse","reach","ritual","useSpellcastingMod"]
        for k in defaultFalseKeys:
            if not k in keys:
                e[k]=False
        
        if not "damageType" in keys:
            e["damageType"]=None
        
        if not "castTime" in keys:
            e["castTime"]="a"
        
        if not "modifierIndex" in keys:
            e["modifierIndex"]=-1

        # we now have every attribute in this large dictionary we need to generate html
        #print("its very expanded now",e)
        #print()

        if e["thrown"]>0:
            e["rang"]=e["thrown"]
        if e["reach"]:
            e["rang"]=10

        modifier = c.modifiers[c.defaultMod]
        if e["useSpellcastingMod"]:
            modifier = c.modifiers[c.spellcastingMod]
        if e["modifierIndex"]!=-1:
            modifier=c.modifiers[e["modifierIndex"]]
        if e["finesse"]:
            if c.modifiers[1]>modifier:
                modifier = c.modifiers[1]

        #print("modifier going forward is ",modifier)
        #print()
        boldBit = getBoldText(e,c)
        
        normalBit = ""
        italicBit = ""

        if e["type"]=="spell":

            normalBit = e["preSaveNormalText"]
            if e["postSaveNormalText"]!="":
                
                normalBit += str(8+c.profBonus+modifier)
                normalBit += e["postSaveNormalText"]
                
            italicBit = e["preSaveItalicText"]
            
            if e["postSaveItalicText"]!="":
                
                italicBit += str(8+c.profBonus+modifier)
                italicBit += e["postSaveItalicText"]
        elif e["type"]=="attack":

            dmgString = e["damage"]
            if not c.addedShield and e["versatile"]!="":
                dmgString  = e["versatile"]
            if e["cantripScaling"]:
                pre = int(c.level/5)
                if pre>0:
                    dmgString = str(pre+1)+dmgString
            if e["addModToDamage"]:
                dmgString += gf.getSignedStringFromInt(modifier,True)
            if e["damageType"] is not None:
                if c.showPhysicalDamageTypes or not (e["damageType"] in ["Bludgeoning","Piercing","Slashing"] ): 
                    dmgString+=" "+e["damageType"]
                    
            dmgString+=" damage"
            archeryBonus = 0
            if "You have the Archery feat" in c.buildLog and e["rang"]!=0:
                archeryBonus=2

            if not e["saveNotAttack"]:
                normalBit+="d20"+gf.getSignedStringFromInt(modifier+c.profBonus+archeryBonus)+" to hit, "
                normalBit+=dmgString+"."
            else:
                normalBit+=dmgString+", "
                normalBit+=e["resistAttributeText"]+str(8+modifier+c.profBonus)+e["resistText"]+"."
            
            
            if c.masteries>0 and e["mastery"]!="":
                
                added = False
                if e["mastery"] =="Push":
                    italicBit +="On a hit, push a Large or smaller foe 10ft away from you."
                    added = True
                elif e["mastery"] == "Vex":
                    added = True
                    italicBit +="On a hit, your next attack against this target before the end of your next turn has advantage."
                elif e["mastery"] == "Topple":
                    added = True
                    italicBit +="Target is knocked Prone on a hit, CON"
                    italicBit += str(int(8+c.profBonus+modifier))
                    italicBit +=" to resist."
                elif e["mastery"] == "Slow":
                    added = True
                    italicBit +="On a hit, target's speed is reduced by 10 (can only apply once)"
                elif e["mastery"] == "Sap":
                    added = True
                    italicBit +="On a hit, target has disadvantage on their next attack before your next turn."
                elif e["mastery"] == "Nick":
                    added = True
                    italicBit +="Make an Offhand attack without spending your Bonus Action."
                elif e["mastery"] == "Graze":
                    added = True
                    italicBit +="Deal "+str(modifier)+" damage on a miss."
                elif e["mastery"] == "Cleave":
                    added = True
                    italicBit +="On a hit, you may make a free attack with this weapon on an enemy within 5ft of you and the target. This free attack can only happen once per turn and its damage is "+e["damage"]

                    
                

                if added:
                    c.masteries = c.masteries-1

            
        elif e["type"]=="heal":
            normalBit = e["preHealText"]
            if e["postHealText"]!="":
            
                normalBit += str(gf.getSignedStringFromInt(modifier+e["healingBonus"]))
            normalBit += e["postHealText"]

        italicBit += e["note"]

        if e["ritual"] and c.ritualCaster:
            italicBit += "</em> ⌆<em>"
        
        return getHTMLfromThruple([boldBit,normalBit,italicBit])
        


def getBoldText(e,c):
    
    
    boldBit = e["id"]

    rang = e["rang"]
    duration = e["duration"]
    cost = e["cost"]
    conc = e["conc"]
    
    if rang > 0 or duration!="" or cost!="":
        boldBit+=" ("
        prior = False
        
        if cost!="":
            boldBit+= str(c.costDic[str(cost)])
            prior = True
        if rang>0 :
            if prior:
                boldBit+=", "
            boldBit+=gf.getDistanceString(rang)
            prior = True
        if duration!="":
            if prior:
                boldBit+=", "
                prior = True
            boldBit+= duration
        boldBit+=")"
    
    if conc:
        boldBit+=" ©. "
    else:
        boldBit+=". "
    
    return boldBit





   
