import Entry as e
import globalFunctions as gf

def addStr(c):
    c.scores[0]=c.scores[0]+2
    c.updateModifiers()

# an automated booster that chooses the scores to boost for the player
def asi(c):
    boosted = gf.ASIboost(c, 2)
    c.buildLog.append(gf.getStringFromBoosts(boosted,"Ability Score Improvement"))
    c.updateModifiers()

def addDex(c):
    c.scores[1]=c.scores[1]+2
    c.updateModifiers()
    
def tough(c):
    logText = "You have the Tough feat"
    if featAlreadyTaken(c,logText):
        skilled(c)
    else:
        c.buildLog.append(logText)
        c.hp+=int(2*(c.level))

def savageAttacker(c):
    logText = "You have the Savage Attacker feat"
    if featAlreadyTaken(c,logText):
        skilled(c)
    else:
        c.buildLog.append(logText)
        c.charInfos.append("<strong>Savage Attacker. </strong>Once per turn, you may re-roll a damage roll and use either result.")

def lucky(c):
    logText = "You have the Lucky feat"

    if featAlreadyTaken(c,logText):
        skilled(c)
    else:
        c.buildLog.append(logText)
        luckyString = "<strong>Lucky. </strong>Roll your next d20 with advantage. "
        if c.level>4:
            luckyString+="<br>"
        for i in range(c.profBonus):
            luckyString+="O "
        c.charInfos.append(luckyString)
        
def addCon(c):
    c.scores[2]=c.scores[2]+2
    c.updateModifiers()
    
def skilled(c):
    c.buildLog.append("You have the Skilled feat")
    c.freeSkills+=3
    
def alert(c):
    logText = "You have the Alert feat"
    if featAlreadyTaken(c,logText):
        skilled(c)
    else:
        c.buildLog.append(logText)
        c.charInfos.append("<strong>Alert. </strong>"+gf.getSignedStringFromInt(c.profBonus)+" bonus to initiative, and can swap your roll with an ally at the start of combat.")
    
def addInt(c):
    c.scores[3]=c.scores[3]+2
    c.updateModifiers()
    
def addWis(c):
    c.scores[4]=c.scores[4]+2
    c.updateModifiers()
    
def addCha(c):
    c.scores[5]=c.scores[5]+2
    c.updateModifiers()
    
def defence(c):
    c.cumulativeACBonus=c.cumulativeACBonus+1
            
def blindsight(c):
    logText = "You have the Blindsight feat"
    if featAlreadyTaken(c,logText):
        if not featAlreadyTaken(c,"You have the Defence feat"):
            defence(c)
    else:
        c.buildLog.append(logText)
        c.charInfos.append("You have Blindsight out to 10ft.")

def archery(c):
    logText = "You have the Archery feat"
    if featAlreadyTaken(c,logText):
        if not featAlreadyTaken(c,"You have the Defence feat"):
            defence(c)
    else:
        c.buildLog.append(logText)
        #c.charInfos.append("Add +2 to attack rolls you make with Ranged weapons.")
    
def protection(c):
    logText = "You have the Protection feat"
    if featAlreadyTaken(c,logText):
        if not featAlreadyTaken(c,"You have the Defence feat"):
            defence(c)
    else:
        c.buildLog.append(logText)
        c.reactions.append(["Protect. ","When an ally within 5ft is targeted with an attack, impose disadvantage on all attacks against them until your turn. ","Requires a Shield."])

def interception(c):
    logText = "You have the Interception feat"
    if featAlreadyTaken(c,logText):
        if not featAlreadyTaken(c,"You have the Defence feat"):
            defence(c)
    else:
        c.buildLog.append(logText)
        c.reactions.append(["Intercept. ","When an ally within 5ft is targeted with an attack, decrease the damage by d10+"+str(c.profBonus)+"."," Requires a Shield or Weapon."])

def greatWeaponFighting(c):
    logText = "You have the Great Weapon Fighting feat"
    if featAlreadyTaken(c,logText):
        if not featAlreadyTaken(c,"You have the Defence feat"):
            defence(c)
    else:
        c.buildLog.append(logText)
        c.charInfos.append("When you roll damage for an attack you make with a Melee weapon that you are holding with two hands, you can treat any 1 or 2 on a damage die as a 3.")

def featAlreadyTaken(c,logText):
    return logText in c.buildLog

Feats = {
    "addStr":addStr,
    "addDex":addDex,
    "addCon":addCon,
    "addInt":addInt,
    "addWis":addWis,
    "addCha":addCha,
    "lucky":lucky,
    "asi":asi,
    "skilled":skilled,
    "savageAttacker":savageAttacker,
    "tough":tough,
    "alert":alert,
    "defence":defence,
    "blindsight":blindsight,
    "protection":protection,
    "interception":interception,
    "archery":archery,
    "greatWeaponFighting":greatWeaponFighting
}
