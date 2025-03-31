import Class as c
import Feats as feats

import globalFunctions as gf


class Ranger(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 10
        self.saveProficiencies = [0,1]
        self.defaultMod = 1
        
        self.loadScoresAndMods([12,15,13,8,14,10],inp)
        self.attributePriorityList = [1,2,4,5,0,3]
        self.preferredBackgrounds = ["Soldier","Charlatan","Criminal"]
        
        super().__init__(inp)
        self.spellcastingMod = 4
    
        self.gp+=150
        self.masteries+=2
        self.proficientWithShields = True
        self.lightArmorProficiency = True
        self.mediumArmorProficiency = True
        self.martialProficiency = True
        
        level = self.level

        
        if self.wearingShield:
            self.wishlist.insert(0,"Shield")
            self.wishlist.append("Rapier")
            self.wishlist.append("Hand Crossbow")
            self.wishlist.append("Dagger")
            
        else:
            self.buyItem("Longbow")
            self.wishlist.append("Shortsword")
            self.wishlist.append("offhand shortsword")

        self.actions.append({"id":"Hide"})

        
        if self.level in [1,2,3,4]:
            self.spellPriorityList = ["Cure Wounds","Entangle","Jump"]
        else:
            self.spellPriorityList = ["Cure Wounds","Spike Growth","Jump","Hunter's Mark","Lesser Restoration","Entangle"]
            
        note = " You can cast this without a spell slot twice. </em> O O<em>"
        if self.level>4:

            note = " You can cast this without a spell slot three times. </em> O O O<em>"
        self.bonusActionEntries.append({"id":"Hunter's Mark","note":note})
        self.longRestEntries.append("Regain your free castings of <strong>Hunter's Mark</strong>.")
        resourceDictionary = {
            1:[["Spell",2]],
            2:[["Spell",2]],
            3:[["Spell",3]],
            4:[["Spell",3]],
            5:[[self.costDic["1"],4],[self.costDic["2"],2]],
            6:[[self.costDic["1"],4],[self.costDic["2"],2]]
        }
        
        if level <5:
            self.costDic= {
                "1":"Spell"
            }
        
        self.spellSlotResourceTuples=resourceDictionary[self.level]
        self.spellsKnown = gf.getNumberFromRange(self.level,[0,0,1,2,3,4])
        self.spellcasting = True

        if self.level in [5,6]:
            self.showUpcasting=True
        self.showSpellRestriction=True

        if level>1:
            self.numberOfLanguages+=2
        
            fightStyle = None
            if "fightStyle" in self.choices.keys():
                fightStyle = self.choices["fightStyle"]
            if fightStyle in feats.Feats.keys():
                feats.Feats[fightStyle](self)
            else:
                feats.Feats["defence"](self)
            
        if level>2:
            
            subclassChosen = False
            
            
            if self.subclass == "hunter":
                self.classAsString="Ranger (Hunter)"
                
                colSlayer = ["","",""]
                colSlayer[1] = "Once per turn, you may deal an extra d8 damage to a wounded target you have hit."
                colSlayer[2] = "<em> (Hunter) </em>"
                self.charInfos.append(colSlayer)
                
                subclassChosen = True
                
            if self.subclass == "monster slayer" or not subclassChosen:
                
                self.classAsString="Ranger (Monster Slayer)"
                self.subclass = "monster slayer"
                
                self.actions.append({"id":"Protection from Evil and Good"})
                
                hunterSense = {"type":"spell"}
                hunterSense["id"] = "Hunter's Sense"
                hunterSense["rang"] =60

                hunterSense["preSaveNormalText"] = " Discern a creature's immunities, resistances, and vulnerabilities."
                count = "O "*max(1,self.modifiers[4])
                hunterSense["preSaveItalicText"] = "</em>"+count+" <em>(Monster Slayer)"
                self.actions.append(hunterSense)
                self.longRestEntries.append("Regain your uses of <strong>Hunter's Sense</strong>.")
                
                slayersPrey = {"type":"spell"}
                slayersPrey["id"] = "Mark Slayer's Prey"
                slayersPrey["rang"] = 60

                slayersPrey["preSaveNormalText"] = " Each turn, the first time you hit the target you deal an extra d6 damage. "
                slayersPrey["preSaveItalicText"] = "Effect ends if you target a new prey. (Monster Slayer)"
                self.bonusActionEntries.append(slayersPrey)
                
            #primal awareness
            swAnimals = {"id":"Speak With Animals","preSaveItalicText":" One free casting per long rest. O"}

            self.actions.append(swAnimals)
            
            
        
            
        if level>4:
            extraAttackEntry = {"id":"extraAttackHighlighted"}
            self.actions.insert(self.highlightedBlockIndex,extraAttackEntry)
            self.highlightedBlockIndex+=1

        if level>5:
            self.speed+=5
            self.charInfos.append(" • Your speed is for walking, climbing or swimming.")
            self.showDodge=False
            

        # Animal Handling, Athletics, Insight, Investigation, Nature, Perception, Stealth, and Survival.
        self.skillProficiencies.append(self.pickSkillProficiency([1,3,6,7,10,11,16,17]))
        self.skillProficiencies.append(self.pickSkillProficiency([1,3,6,7,10,11,16,17]))
        self.skillProficiencies.append(self.pickSkillProficiency([1,3,6,7,10,11,16,17]))
        
        if level>1:
            # deft explorer - expertise in stealth
            if 16 in self.skillProficiencies:
                self.skillExpertises.append(16)
            else:
                self.skillExpertises.append(self.skillProficiencies[0])
            
        
        