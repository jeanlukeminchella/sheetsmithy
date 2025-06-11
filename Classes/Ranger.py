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
            self.spellPriorityList = ["Aid","Cure Wounds","Spike Growth","Pass without Trace","Magic Weapon","Barkskin","Hunter's Mark","Lesser Restoration","Entangle","Jump"]
            
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
        self.spellsKnown = gf.getNumberFromRange(self.level,[0,1,2,3,4])
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

            if "beastMaster" in self.subclass:
                subclassChosen=True
                
                damage = None
                note = ""
                bonusDamage = 2
                damageType = "bludgeoning"
                hp = 5+5*self.level
                hitDie = "d8"
                con = 2
                
                self.classAsString="Ranger (Beast Master)"
                beastTitle = ""
                beastStats = []

                

                if "sea" in self.subclass:
                    damage="d6"
                    beastStats.append("STR +2 | DEX +2 | CON +2 | INT -1 | WIS +2 | CHA 0")
                    beastStats.append("Your Beast can swim 60ft, or walk 5ft per turn.")
                    beastStats.append("Your Beast has Darkvision out to 90ft.")
                    beastTitle = "BEAST OF THE SEA"
                elif "land" in self.subclass:
                    beastStats.append("STR +2 | DEX +2 | CON +2 | INT -1 | WIS +2 | CHA 0")
                    beastStats.append("Your Beast can walk or climb 40ft per turn.")
                    note="If the Beast has moved 20ft straight before hitting target, target takes an extra d6 damage and is knocked prone (if Large or smaller)."
                    damage="d8"
                    beastTitle = "BEAST OF THE LAND)"
                elif "sky" in self.subclass:
                    hitDie = "d6"
                    con = 1
                    beastStats.append("STR -2 | DEX +3 | CON +1 | INT -1 | WIS +2 | CHA 0")
                    beastStats.append("Your Beast can fly 60ft per turn, and does not provoke Opportunity Attacks.")
                    hp = 4+4*self.level
                    damage="d4"
                    bonusDamage=3
                    damageType = "slashing"
                    beastTitle = "BEAST OF THE SKY"

                bold = ""
                mid = "Your <strong>Beast Heals </strong>"+str(hitDie)+gf.getSignedStringFromInt(con,True)+" hp for each hit die it spends."
                if self.level>1:
                    mid += "<br>"
                for i in range(self.level):
                    mid += " O"
                it = ""
                self.shortRestEntries.append([bold,mid,it])

                beastStats.append("Add "+gf.getSignedStringFromInt(self.profBonus)+" to any save / check the Beast makes.")

                beastStats.append(["","Your Beast has <strong>"+str(hp)+"</strong> Hit Points and "+str(13+self.modifiers[4])+" AC."])
                beastStats.append(["","If you are Incapacitated, your Beast acts on its own."])
                self.rightColumnBlocks.append(c.e.Block(beastStats,beastTitle+" STATS"))
                
                strike = {
                "id":"Strike",
                "damage": damage+gf.getSignedStringFromInt(bonusDamage+self.modifiers[4]),
                "addModToDamage": False,
                "damageType": damageType,
                "cantripScaling": False,
                "saveNotAttack": False,
                "useSpellcastingMod": True,
                "type": "attack",
                "note":note,
                "castTime":"ba",
                "expanded":True
                }

                
                beastActions = [["Dodge.","","If no command is given, your Beast dodges."],strike]
                beastActions.append(["Other Action.","","eg. Dash, Disengage, Help, Ready ect. "])
                
                self.rightColumnBlocks.append(c.e.Block(beastActions,beastTitle+" ACTIONS (1 per turn)"))

                self.highlightedEntries.append(["Command Beast to Strike."])
                self.bonusActionEntries.append(["Command Beast."])
                self.actions.append({"id":"Revive Beast"})




                
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
            
        
        