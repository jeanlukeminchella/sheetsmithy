import globalFunctions as gf
import json
import newEntry as ne

fileExtension = ".json"
standardEntryStart = "<p>"
standardEntryEnd = "</p>\n"



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
            #surely there is another way?
            if "Entry" in str(type(e)):

                result += e.getHTML(c)
            else:
                result += ne.getHTML(e,c)
        
        if self.divID !="":
            result += "</div>\n"
        
        return result
        
spellCommands = {}
with open(gf.pathToSource+"Entries/spellCommands.json", 'r') as file:
    spellCommands = json.load(file)

# type: spell / text / heal / attackRoll     
# code is what loads the JSON 

def getEntryWithSpellCommand(inp):
    command = spellCommands[inp]
    commandType = command["type"]
    commandCode = command["code"]
    if commandType=="spell":
        return SpellEntry(commandCode)
    elif commandType=="text":
        return TextEntry(commandCode)
    elif commandType=="heal":
        return HealingEntry(commandCode)
    elif commandType=="attackRoll":
        return AttackRollEntry(commandCode)


def getHTML(e):
    if type(e)==str:
        return e
    elif type(e)!=dict:
        try:
            return str(e)
        except:
            return ""
    # ok so type is dictionary

    keys = list(e.keys())
    
   
