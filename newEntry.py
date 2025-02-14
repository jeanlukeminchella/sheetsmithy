import globalFunctions as gf
import json
textEntries = {}
spellEntries = {}

fileExtension = ".json"
standardEntryStart = "<p>"
standardEntryEnd = "</p>\n"

with open(gf.pathToSource+"Entries/TextEntries.txt", 'r') as file:
    textEntries = json.load(file)



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

"""def getBoldText():
    
    
    boldBit = self.title
    
    if self.rang > 0 or self.duration!="" or self.cost!="":
        boldBit+=" ("
        prior = False
        
        if self.cost!="":
            boldBit+= str(c.costDic[str(self.cost)])
            prior = True
        if self.rang>0 :
            if prior:
                boldBit+=", "
            boldBit+=gf.getDistanceString(self.rang)
            prior = True
        if self.duration!="":
            if prior:
                boldBit+=", "
                prior = True
            boldBit+= self.duration
        boldBit+=")"
    
    if self.conc:
        boldBit+=" ©. "
    else:
        boldBit+=". "
    
    return boldBit"""

# this funciton fills out the entry into a dictionary that has all the keys it needs to make hmtl, including "castTime", "id" and "type"
# returns a blank thruple dictionary if theres an error
# id is used to expand the dictionay, and also identify if a character already has a certain entry
def getExpandedDictionary(e):

    defaultDictionary = {
        "castTime":"a",
        "id":"",
        "type":"thruple",
        "expanded":True,
        # contents is required for thruple types
        "contents":["","",""]
    }
    
    #were now trying to parse different inputs, like strings or lists
    if type(e)==str:
        defaultDictionary["contents"][1]=e
        return defaultDictionary

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
                defaultDictionary["contents"]=e
                return defaultDictionary
    

    
    if type(e)!=dict:
        # if its an int or boolean ect. we can make a string out of it and still display that info
        try:
            defaultDictionary["contents"][1]=str(e)
            return defaultDictionary
        except:
            return defaultDictionary
        
    
        
    # type(e) is definitely dictionary now

    keys = list(e.keys())

    # these types do not reflect the 5e rules definitions. in this program spells have saves and do not necessarily do damage, attacks do damage.
    # 
    entryTypes= ["text","spell","attack","thruple"]

    badEntry = not ("type" in keys and  "id" in keys)
    if "type" in keys:
        if not e["type"] in entryTypes:
            badEntry = True

    if badEntry:
        print("weve got a bad entry here - ")
        print(e)
        return defaultDictionary
    
    # ok now weve got a dictionary with a "type" key that is in the accepted entryTypes, and an "id" key as well
    
    #lets see if any of these keys are in our input, and add them to the entry to return. These are all valid keys (though their values might not be)
    keysToClone = ["castTime","cost","duration"]
    for key in keysToClone:
        if key in keys:
            defaultDictionary[key]=e[key]
                
    if e["type"]=="text":
        #print("weve been asked to expand a text entry ",e)
        if not e["id"] in textEntries.keys():
            print("bad key for text entry", e["id"])
            defaultDictionary["contents"][1] = e["id"]
            return defaultDictionary
        else:
            defaultDictionary["contents"] = textEntries[e["id"]]
            defaultDictionary["id"]=e["id"]
            
            return defaultDictionary

            
    elif e["type"]=="spell":
        pass

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

def getHTML(e):
    print("input to get hmtl: ",e)
    expanded = False
    if type(e)==dict:
        if "expanded" in e.keys():
            expanded =  e["expanded"]

    if not expanded:
        e = getExpandedDictionary(e)

    print("should be expanded now: ",e)
    
    if e["type"]=="thruple":
        return getHTMLfromThruple(e["contents"])








print(getHTML("wagwan"))
print()
print(getHTML(4))
print()
print(getHTML(False))
print()
r = {"type":"text","id":"Disengage"}
print(getHTML(r))


