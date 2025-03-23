import featFunctions as feat
import globalFunctions as gf
import Entry as e
import Input as inp

freeCastText =" One free casting per Long Rest - </em>O<em>"


def tiefling(c,choice):
    c.size="Medium"
    c.speed = 30
    c.raceString = "Tiefling"
    c.darkvision=60
    
    keys = choice.keys()
    
    spellcastingMods = c.modifiers[3:]
    bestMod =3+spellcastingMods.index(max(spellcastingMods))
    c.addEntry("Thaumaturgy",False)   
    
    if "size" in keys:
        if choice["size"]=="Small":
            c.size="Small"
    if not "subrace" in choice.keys():
        choice["subrace"]="Infernal"
    subraces = ["Infernal","Chthonic","Abyssal"]
    if not choice["subrace"] in subraces:
        choice["subrace"]="Infernal"
    
    if choice["subrace"]=="Infernal":
        c.addResistance("Fire")
        c.raceString = "Tiefling (Infernal)"
        fireBolt = {"id":"Fire Bolt"}
        fireBolt["modifierIndex"] = bestMod
        c.actionEntries.append(fireBolt)
        if c.level>2:
            hRebuke = {"id":"Hellish Rebuke"}
            hRebuke["modifierIndex"] = bestMod
            hRebuke["preSaveItalicText"]=freeCastText
            c.reactions.append(hRebuke)
        if c.level>4:
            d  = {"id":"Darkness"}
            d = e.getExpandedDictionary(d)
            d["preSaveItalicText"] += freeCastText
            c.actionEntries.append(d)
    if choice["subrace"]=="Chthonic":
        c.addResistance("Necrotic")
        c.raceString = "Tiefling (Chthonic)"
        fireBolt = {"id":"Chill Touch"}
        fireBolt["modifierIndex"] = bestMod
        c.actionEntries.append(fireBolt)
        if c.level>2:
            fLife = {"id":"False Life"}
            fLife = e.getExpandedDictionary(fLife)
            fLife["preSaveItalicText"]=freeCastText
            c.actionEntries.append(fLife)
        if c.level>4:
            d  = {"id":"Ray of Enfeeblement"}
            d["modifierIndex"] = bestMod
            d = e.getExpandedDictionary(d)
            d["preSaveItalicText"] += freeCastText
            c.actionEntries.append(d)
    if choice["subrace"]=="Abyssal":
        c.addResistance("Poison")
        c.raceString = "Tiefling (Abyssal)"
        pSpray = {"id":"Poison Spray"}
        pSpray["modifierIndex"] = bestMod
        c.actionEntries.append(pSpray)
        if c.level>2:
            x = {"id":"Ray of Sickness"}
            x = e.getExpandedDictionary(x)
            x["note"]=x["note"]+freeCastText
            x["modifierIndex"]=bestMod
            c.actionEntries.append(x)
        if c.level>4:
            d  = {"id":"Hold Person"}
            d = e.getExpandedDictionary(d)
            d["modifierIndex"]=bestMod
            d["preSaveItalicText"] += freeCastText
            c.actionEntries.append(d)
    
def elf(c,choice):
    c.size="Medium"
    c.speed = 30
    c.raceString = "Elf"
    c.darkvision=60
    

    c.preferredLanguages.append("elven") 

    spellcastingMods = c.modifiers[3:]
    bestMod =3+spellcastingMods.index(max(spellcastingMods))
    
    c.saveNotes.append([4,"(adv. vs charmed)"])
    c.pickSkillProficiency([6,11,17])
    c.charInfos.append({"id":"trance"})

    if not "subrace" in choice.keys():
        choice["subrace"]="Wood"
    
    subraces = ["Wood","Drow","High"]
    if not choice["subrace"] in subraces:
        choice["subrace"]="Wood"
    
    if choice["subrace"]=="Wood":
        c.speed = 35
        c.raceString = "Wood Elf"
        c.addEntry("Druidcraft",False)
        if c.level>2:
            spell = {"id":"Longstrider"}
            spell = e.getExpandedDictionary(spell)
            spell["preSaveItalicText"]=freeCastText
            c.actionEntries.append(spell)
        if c.level>4:
            spell  = {"id":"Pass without Trace"}
            spell = e.getExpandedDictionary(spell)
            spell["preSaveItalicText"] = freeCastText
            c.actionEntries.append(spell)
    if choice["subrace"]=="Drow":
        c.addEntry("Dancing Lights",False)
        c.raceString = "Drow"
        c.darkvision = 120
        if c.level>2:
            spell = {"id":"Faerie Fire"}
            spell = e.getExpandedDictionary(spell)
            spell["modifierIndex"] = bestMod
            spell["preSaveItalicText"] = freeCastText
            c.actionEntries.append(spell)
        if c.level>4:
            d  = {"id":"Darkness"}
            d = e.getExpandedDictionary(d)
            d["preSaveItalicText"] += freeCastText
            c.actionEntries.append(d)
    if choice["subrace"]=="High":
        c.raceString = "High Elf"
        fireBolt = {"id":"Fire Bolt"}
        fireBolt["modifierIndex"] = bestMod
        c.highlightedEntries.append(fireBolt)
        if c.level>2:
            spell  = {"id":"Detect Magic"}
            spell = e.getExpandedDictionary(spell)
            spell["preSaveItalicText"] = freeCastText
            c.actionEntries.append(spell)
        if c.level>4:
            spell  = {"id":"Misty Step"}
            spell = e.getExpandedDictionary(spell)
            spell["preSaveItalicText"] = freeCastText
            c.bonusActionEntries.append(spell)
 
def aasimar(c,choice):
    c.size="Medium"
    c.speed = 30
    c.raceString = "Aasimar"
    c.darkvision=60
    
    keys = choice.keys()
    
    if "size" in keys:
        if choice["size"]=="Small":
            c.size="Small"
            
    
    healingHandsString = "<strong>Healing Hands.</strong> Touch a creature and heal "
    healingHandsString+=str(c.profBonus)
    healingHandsString+="d4 hp. O"
    c.actionEntries.append(healingHandsString)
    c.actionEntries.append({"id":"Light"})
    c.longRestEntries.append("Regain your <strong> Healing Hands</strong> feature.")
    c.addResistance("Necrotic")
    c.addResistance("Radiant")
    
    if c.level>2:
        
        hw = "<strong>Heavenly Wings. </strong> You can fly."
        ir = "<strong>Inner Radiance.</strong> At the end of each of your turns, each creature within 10ft takes "+str(c.profBonus)+" radiant damage."
        ns = {"id":"Necrotic Shroud"}
        transformationEntries = [hw,ir,ns]
        c.leftColumnBlocks.append(e.Block(transformationEntries,"TRANSFORMATIONS"))
        celestialRevelationText = "<strong>Celestial Revelation (1 min). </strong> "
        celestialRevelationText += gf.getSignedStringFromInt(c.profBonus)
        celestialRevelationText += " damage per turn. Choose a Transformation to undergo which determins the damage type (radiant or necrotic). O"
        c.bonusActionEntries.append(celestialRevelationText)
        
def orc(c, choice):
    c.size="Medium"
    c.speed = 30
    c.raceString = "Orc"
    c.darkvision=120

    c.preferredLanguages.append("orc")
    
    adrenalineRushText = "<strong>Adrenaline Rush. </strong> Take the Dash action, and gain "
    adrenalineRushText += gf.getSignedStringFromInt(c.profBonus)
    adrenalineRushText += " temporary hp."
    for i in range(c.profBonus):
        adrenalineRushText += " O"
    if c.showShortRest:
        c.shortRestEntries.append("Regain all your uses of <strong>Adrenaline Rush</strong>")
    else:
        adrenalineRushText += "<em> Regain all uses on a short rest</em>"
    c.bonusActionEntries.append(adrenalineRushText)
    
    c.charInfos.append("<strong>Relentless Endurance.</strong> When you are reduced to 0 hp you drop to 1 hp instead. O")
    c.longRestEntries.append("Regain your <strong>Relentless Endurance</strong> feature.")

def dwarf(c, choice):
    c.size="Medium"
    c.speed = 30
    c.raceString = "Dwarf"
    c.darkvision=120
    c.addResistance("Poison")
    c.saveNotes.append([2,"(adv. poison)"])
    c.hp+=c.level

    c.preferredLanguages.append("dwarven")
    
    stoneCunningText = "<strong>Stonecunning (10 min). </strong> Gain Tremorsense out to 60ft on stone surfaces."
    for i in range(c.profBonus):
        stoneCunningText+=" O"
    c.bonusActionEntries.append(stoneCunningText)
    c.longRestEntries.append("Regain your uses of <strong>Stonecunning</strong>.")

def gnome(c, choice):
    c.size="Small"
    c.speed = 30
    c.darkvision=60
    c.saveNotes.append([4,"(advantage)"])
    c.saveNotes.append([3,"(advantage)"])
    c.saveNotes.append([5,"(advantage)"])

    c.preferredLanguages.append("gnomish")
    
    if not "subrace" in choice.keys():
        choice["subrace"]="Rock"
    
    subraces = ["Rock","Forest"]

    if not choice["subrace"] in subraces:
        choice["subrace"]="Rock"

    if choice["subrace"]=="Rock":
        c.raceString = "Rock Gnome"
        c.actionEntries.append({"id":"Prestidigitation"})
        c.actionEntries.append({"id":"Mending"})
        c.charInfos.append("If you cast Prestidigitation for 10 minutes you create a Tiny clockwork device that lasts 8 hours and can perform one effect of Prestidigitation")
    if choice["subrace"]=="Forest":
        c.raceString = "Forest Gnome"
        c.actionEntries.append({"id":"Create Minor Illusion"})
        swAnimals = {"id":"Speak With Animals"}
        swAnimals = e.getExpandedDictionary(swAnimals)
        swAnimals["cost"] = ""
        swAnimals["preSaveNormalText"]+= " O"*c.profBonus
        c.actionEntries.append(swAnimals)

def goliath(c, choice):
    c.size="Medium"
    c.speed = 35
    c.raceString = "Goliath"
    
    count = "O "*c.profBonus
    c.preferredLanguages.append("giant")
    
    subraces = ["Cloud","Fire","Frost","Hill","Stone","Storm"]

    if not "subrace" in choice.keys():
        choice["subrace"]="Storm"
    if not choice["subrace"] in subraces:
        choice["subrace"]="Storm"

    if choice["subrace"]=="Cloud":
        c.raceString = "Goliath (Cloud)"
        c.bonusActionEntries.append("Teleport 30ft "+count)
        c.longRestEntries.append("Regain all uses of your uses of Teleport. <em>(Cloud Goliath)</em>")
    elif choice["subrace"]=="Fire":
        c.raceString = "Goliath (Fire)"
        c.charInfos.append("Boost any damage roll with d10 fire damage. "+count)
        c.longRestEntries.append("Regain all of your fire damage boosts. <em>(Fire Goliath)</em>")
    elif choice["subrace"]=="Frost":
        c.raceString = "Goliath (Frost)"
        c.charInfos.append("Boost any damage roll with d6 cold damage and reduce target's speed by 10 for one round. "+count)
        c.longRestEntries.append("Regain all of your cold damage boosts. <em>(Frost Goliath)</em>")
    elif choice["subrace"]=="Hill":
        c.raceString = "Goliath (Hill)"
        c.charInfos.append("Knock a Large or smaller target Prone when you land an attack. "+count)
        c.longRestEntries.append("Regain all uses of your uses of Knocking targets Prone <em>(Hill Goliath)</em>")
    elif choice["subrace"]=="Stone":
        c.raceString = "Goliath (Stone)"
        c.reactions.append("<strong>Stone's Endurance. </strong>Reduce incoming damage by d12"+gf.getSignedStringFromInt(c.modifiers[2])+". "+count)
        c.longRestEntries.append("Regain all uses of your <strong>Stone's Endurance </strong>")
    elif choice["subrace"]=="Storm":
        c.raceString = "Goliath (Storm)"
        c.reactions.append("<strong>Storm's Thunder. </strong> Deal d8 thunder damage to a creature that has just damaged you. "+count)
        c.longRestEntries.append("Regain all uses of your <strong>Storm's Thunder </strong>")
      
    if c.modifiers[0]>c.modifiers[1]:
        c.skillNotes.append([3,"(adv. v grappled)"])
    else:
        c.skillNotes.append([0,"(adv. grappled)"])
    
    if c.level>4:
        c.bonusActionEntries.append("<strong>Large Form (10 mins).</strong> Advantage on Strength checks, +10 speed and become Large. O")
    
def human(c, choice):
    
    c.size="Medium"
    c.speed = 30
    c.raceString = "Human"
    
    keys = choice.keys()
    
    if "skillful" in keys:
        skill = inp.validateInt(choice["skillful"], 11, 0,17)
        if skill in c.skillProficiencies:
            c.freeSkills+=1
        else:
            c.skillProficiencies.append(skill)
    else:
        c.freeSkills+=1
    featChoice = None
    if "originFeat" in keys:
        if choice["originFeat"] in feat.featFunctions.keys():
            feat.featFunctions[choice["originFeat"]](c)
            featChoice = choice["originFeat"]

    if featChoice == None:
        if "You have the Tough feat" in c.buildLog:
            feat.skilled(c)
        else:
            feat.tough(c)

    c.charInfos.append("Reroll a d20 with Heroic Inspiration - O")

def halfling(c, choice):
    
    c.size="Small"
    c.speed = 30
    c.raceString = "Halfling"

    c.preferredLanguages.append("halfling")
    c.charInfos.append("You can move through the space of larger creatures, and Hide behind them.")
    c.charInfos.append("When you roll a 1 on a d20, re-roll the die once.")
    c.saveNotes.append([4,"(adv. frightened)"])

    
racesDictionary = {
    "human":human,
    "aasimar":aasimar,
    "dwarf":dwarf,
    "elf":elf,
    "gnome":gnome,
    "goliath":goliath,
    "halfling":halfling,
    "tiefling":tiefling,
    "orc":orc
}
