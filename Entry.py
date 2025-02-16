import globalFunctions as gf
import json
import newEntry as ne

fileExtension = ".json"
standardEntryStart = "<p>"
standardEntryEnd = "</p>\n"

# self.folderName needs defining to load a codename
class Entry():
    
    # datum could be loads of data types  - depends on type of entry)
    def __init__(self, datum):

        self.datum=datum
        self.title=""
        self.rang=0
        self.cost=""
        self.duration=""
        self.conc=False
        self.forcedMod=-1
        self.castTime="a"
        self.folderName = ""
        
        #heal
        self.preHealText=""
        self.postHealText=""
        self.healingBonus = 0
        
        #attack rolls
        self.damage=""
        self.addModToDamage=False
        self.damageType=None
        self.forcedMod=-1
        self.cantripScaling=False
        self.saveNotAttack=False
        self.resistAttributeText=""
        self.resistText=""
        self.note=""
        self.finesse = False
        self.reach = False
        self.versatile=""
        self.thrown=0
        self.mastery=""

        #spell
        self.preSaveNormalText=""
        self.postSaveNormalText=""
        self.preSaveItalicText=""
        self.postSaveItalicText=""
        self.ritual=False
        self.isSpell = False
        
    # if not a specific type of entry, just returns datum as flat text
    def getHTML(self, c=None):
        t = getThrupleFromFlatText(self.datum)
        return getHTMLfromThruple(t)
        
    def applyCommand(self,commandWord,result):
        if commandWord=="title":
            self.title=result
        elif commandWord=="damage":
            self.damage=result
        elif commandWord=="rang":
            self.rang=result
        elif commandWord=="cost":
            self.cost=result
        elif commandWord=="duration":
            self.duration=result
        elif commandWord=="conc":
            self.conc=result
        elif commandWord=="addModToDamage":
            self.addModToDamage=result
        elif commandWord=="damageType":
            self.damageType=result
        elif commandWord=="forcedMod":
            self.forcedMod=result
        elif commandWord=="cantripScaling":
            self.cantripScaling=result
        elif commandWord=="saveNotAttack":
            self.saveNotAttack=result
        elif commandWord=="resistAttributeText":
            self.resistAttributeText=result
        elif commandWord=="resistText":
            self.resistText=result
        elif commandWord=="note":
            self.note=result
        elif commandWord=="castTime":
            self.castTime=result
        elif commandWord=="ritual":
            self.ritual=result
        elif commandWord=="isSpell":
            self.isSpell=result
            
        elif commandWord=="finesse":
            self.finesse=result
        elif commandWord=="reach":
            self.reach=result
        elif commandWord=="versatile":
            self.versatile=result
        elif commandWord=="thrown":
            self.thrown=result
        elif commandWord=="mastery":
            self.mastery=result
            
            
            
        
        
        elif commandWord=="preSaveNormalText":
            self.preSaveNormalText=result
        elif commandWord=="postSaveNormalText":
            self.postSaveNormalText=result
        elif commandWord=="preSaveItalicText":
            self.preSaveItalicText=result
        elif commandWord=="postSaveItalicText":
            self.postSaveItalicText=result
            
        elif commandWord=="preHealText":
            self.preHealText=result
        elif commandWord=="postHealText":
            self.postHealText=result


    def applyCommandList(self,commandList):
        for command in commandList:
            self.applyCommand(command[0],command[1])
            
    def loadCodeName(self,codeName):
        
        d= {}
        
        with open(gf.pathToSource+"Entries/"+self.folderName+"/"+codeName+fileExtension, 'r') as file:
            d = json.load(file)
            
        commandTuples = []
        
        for k in d.keys():
            commandTuples.append([k,d[k]])
            
        self.applyCommandList(commandTuples)
    
    def getBoldText(self, c):
        
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
        
        return boldBit
    
# this has a bold bit, normal bit then italicised bit, and is static (is not affected by character at all)
class TextEntry(Entry):
    
    def __init__(self, datum):
        self.datum=datum
        # by default text entries are actions, but can be added anywhere 
        self.castTime="a"
        self.title=datum
        with open(gf.pathToSource+"Entries/TextEntries.txt", 'r') as file:
            self.textEntryDictionary = json.load(file)
        
    def getHTML(self,c=None):
        thruple = self.textEntryDictionary[self.datum]
        return getHTMLfromThruple(thruple)

# this is best for attacks and spell attacks with roll to hit then damage dice
class AttackRollEntry(Entry):
    
    def __init__(self, datum):
        
        super().__init__(datum)
        self.folderName = "AttackRolls"
        self.loadCodeName(datum)
        
    def getHTML(self,c):
        
        thruple = self.attackGetThruple(c)
        return getHTMLfromThruple(thruple)
        
        # note is un actioned
    def attackGetThruple(self, c):
        
        if self.thrown>0:
            self.rang=self.thrown
        if self.reach:
            self.rang=10
        boldBit = self.getBoldText(c)
        normalBit = ""
        
        attributeModifier = c.modifiers[c.defaultMod]
        if self.isSpell:
            attributeModifier = c.modifiers[c.spellcastingMod]
        if self.forcedMod!=-1:
            attributeModifier=c.modifiers[self.forcedMod]
        if self.finesse:
            # this may cause issues if a spell was finesse, but why would it be? 
            if c.modifiers[1]>attributeModifier:
                attributeModifier = c.modifiers[1]
    
        dmgString = self.damage
        if not c.addedShield and self.versatile!="":
            dmgString  = self.versatile
        if self.cantripScaling:
            #needs a fix
            pre = int(c.level/5)
            if pre>0:
                dmgString = str(pre+1)+dmgString
        if self.addModToDamage:
            dmgString += gf.getSignedStringFromInt(attributeModifier,True)
        if self.damageType is not None:
            if c.showPhysicalDamageTypes or not (self.damageType in ["Bludgeoning","Piercing","Slashing"] ): 
                dmgString+=" "+self.damageType
                
        dmgString+=" damage"
        
        if not self.saveNotAttack:
            normalBit+="d20"+gf.getSignedStringFromInt(attributeModifier+c.profBonus)+" to hit, "
            normalBit+=dmgString+"."
        else:
            normalBit+=dmgString+", "
            normalBit+=self.resistAttributeText+str(8+attributeModifier+c.profBonus)+self.resistText+"."
        
        italicBit = ""
        if c.masteries>0 and self.mastery!="":
            
            added = False
            if self.mastery =="Push":
                italicBit +="On a hit, push a Large or smaller foe 10ft away from you."
                added = True
            elif self.mastery == "Vex":
                added = True
                italicBit +="On a hit, your next attack against this target before the end of your next turn has advantage."
            elif self.mastery == "Topple":
                added = True
                italicBit +="Target is knocked Prone on a hit, CON"
                italicBit += str(int(8+c.profBonus+attributeModifier))
                italicBit +=" to resist."
            elif self.mastery == "Slow":
                added = True
                italicBit +="On a hit, target's speed is reduced by 10 (can only apply once)"
            elif self.mastery == "Sap":
                added = True
                italicBit +="On a hit, target has disadvantage on their next attack before your next turn."
            elif self.mastery == "Nick":
                added = True
                italicBit +="Make an Offhand attack without spending your Bonus Action."
            elif self.mastery == "Graze":
                added = True
                italicBit +="Deal "+str(attributeModifier)+" damage on a miss."
            elif self.mastery == "Cleave":
                added = True
                italicBit +="On a hit, you may make a free attack with this weapon on an enemy within 5ft of you and the target. This free attack can only happen once per turn and its damage is "+self.damage1

                
            

            if added:
                c.masteries = c.masteries-1

        italicBit += self.note

        
        return [boldBit,normalBit,italicBit]


        
class SpellEntry(Entry):
    
    def __init__(self, datum):
        super().__init__(datum)
        self.folderName = "Spells"
        self.loadCodeName(datum)
    
    def getHTML(self,c):
        
        
        modifier = c.modifiers[c.defaultMod]
        if self.isSpell:
            modifier = c.modifiers[c.spellcastingMod]
        if self.forcedMod!=-1:
            modifier=c.modifiers[self.forcedMod]
        
        
            
        boldBit = self.getBoldText(c)
        
        normalBit = self.preSaveNormalText
        if self.postSaveNormalText!="":
            
            normalBit += str(8+c.profBonus+modifier)
            normalBit += self.postSaveNormalText
            
        italicBit = self.preSaveItalicText
        if self.postSaveItalicText!="":
            
            italicBit += str(8+c.profBonus+modifier)
            italicBit += self.postSaveItalicText
            
        if self.ritual and c.ritualCaster:
            italicBit += "</em> ⌆<em>"
        
        return getHTMLfromThruple([boldBit,normalBit,italicBit])
        

class HealingEntry(Entry):
    
    def __init__(self, datum):
        
        super().__init__(datum)
        self.folderName = "Heals"
        self.loadCodeName(datum)
        
    def getHTML(self,c):
        
        modifier = c.modifiers[c.defaultMod]
        if self.isSpell:
            modifier = c.modifiers[c.spellcastingMod]
        if self.forcedMod!=-1:
            modifier=c.modifiers[self.forcedMod]

        boldBit = self.getBoldText(c)
        
        normalBit = self.preHealText
        if self.postHealText!="":
            
            normalBit += str(gf.getSignedStringFromInt(modifier+self.healingBonus))
            normalBit += self.postHealText
            
        italicBit = ""
            
        if self.ritual and c.ritualCaster:
            italicBit += "</em> ⌆<em>"
        
        return getHTMLfromThruple([boldBit,normalBit,italicBit])

def getThrupleFromFlatText(text):
    return ["",text,""]

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
    
   
