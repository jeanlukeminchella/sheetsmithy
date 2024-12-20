import Entry as e
import globalFunctions as gf

def addStr(c):
    c.scores[0]=c.scores[0]+2
    c.updateModifiers()

# an automated booster that chooses the scores to boost for the player
def boostScores(c):
    x = gf.chooseAttributesToIncreaseBy(c,2)
    c.scores[x[0]]+=1
    c.scores[x[1]]+=1
    c.updateModifiers()

def addDex(c):
    c.scores[1]=c.scores[1]+2
    c.updateModifiers()
    
def tough(c):
    c.hp+=int(2*(c.level))
    c.buildLog.append("You have the Tough feat")

def savageAttacker(c):
    c.buildLog.append("You have the Savage Attacker feat")
    c.charInfos.append(e.Entry("<strong>Savage Attacker. </strong>Once per turn, you may re-roll a damage roll and use either result."))

def lucky(c):
    c.buildLog.append("You have the Lucky feat")
    luckyString = "<strong>Lucky. </strong>Roll your next d20 with advantage. "
    if c.level>4:
        luckyString+="<br>"
    for i in range(c.profBonus):
        luckyString+="O "
    c.charInfos.append(e.Entry(luckyString))
    
def addCon(c):
    c.scores[2]=c.scores[2]+2
    c.updateModifiers()
    
def skilled(c):
    c.buildLog.append("You have the Skilled feat")
    c.freeSkills+=3
    
def alert(c):
    c.buildLog.append("You have the Alert feat")
    c.charInfos.append(e.Entry("<strong>Alert. </strong>"+gf.getSignedStringFromInt(c.profBonus)+" bonus to initiative, and can swap your roll with an ally at the start of combat."))
    
def asi(c):
    boosted = gf.ASIboost(c, 2)
    c.buildLog.append(gf.getStringFromBoosts(boosted,"Ability Score Improvement"))
    c.updateModifiers()

def addInt(c):
    c.scores[3]=c.scores[3]+2
    c.updateModifiers()
    
def addWis(c):
    c.scores[4]=c.scores[4]+2
    c.updateModifiers()
    
def addCha(c):
    c.scores[5]=c.scores[5]+2
    c.updateModifiers()
    
def greatWeaponMaster(c):
    
    class HeavyWeaponEntry(e.Entry):
        def getHTML(self,c):
            boldBit = "Headshot. "
            middleBit = "d20"
            
            attackMod = c.modifiers[0]+c.profBonus-5
            middleBit+=e.gf.getSignedStringFromInt(attackMod,True)
            middleBit+=" to hit, 2d6"
            middleBit+=e.gf.getSignedStringFromInt(c.modifiers[0]+10,True)
            middleBit+=" damage."
            
            thruple = [boldBit,middleBit,""]
            
            return e.getHTMLfromThruple(thruple)
    e = HeavyWeaponEntry(" ")
    c.highlightedEntries.insert(1,e)
    
    c.charInfos.append(e.Entry("Critical Hits and Knockouts allow an attack as a Bonus Action."))
            
            
def defenceFightStyle(c):
    c.cumulativeACBonus=c.cumulativeACBonus+1
            
featFunctions = {
    "addStr":addStr,
    "addDex":addDex,
    "addCon":addCon,
    "addInt":addInt,
    "addWis":addWis,
    "addCha":addCha,
    "lucky":lucky,
    "boostScores":boostScores,
    "defence":defenceFightStyle,
    "gwm":greatWeaponMaster,
    "asi":asi,
    "skilled":skilled,
    "savageAttacker":savageAttacker,
    "tough":tough,
    "alert":alert
}
