import Class as c
import featFunctions as feats


class Ranger(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 10
        self.saveProficiencies = [0,1]
        self.defaultMod = 1
        
        self.loadScoresAndMods([10,15,13,10,14,10],inp)
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
            c.item.buyItem(c,"Shield")
            self.wishlist.append("Rapier")
            self.wishlist.append("Hand Crossbow")
            self.wishlist.append("Dagger")
            
        else:
            c.item.buyItem(self,"Longbow")
            self.wishlist.append("Shortsword")
            self.wishlist.append("offhand shortsword")

        self.actionEntries.append(c.e.TextEntry("Hide"))

        self.charInfos.append(c.e.Entry(" • Favoured Enemy: ___________________ <br><em>Adv. on tracking & lore checks.</em>"))
        self.numberOfLanguages+=2
        
        if self.level in [1,2,3,4]:
            self.spellPriorityList = ["Cure Wounds","Hunter's Mark","Entangle","Jump"]
        else:
            self.spellPriorityList = ["Cure Wounds","Spike Growth","Jump","Hunter's Mark","Lesser Restoration","Entangle"]
            
        resourceDictionary = {
            1:[["Spell",0]],
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
        
        if level>1:
            self.spellcasting = True
            fightStyle = None
            if "l2-fightStyle" in self.choices.keys():
                fightStyle = self.choices["l2-fightStyle"]
            if fightStyle in feats.featFunctions.keys():
                feats.featFunctions[fightStyle](self)
            else:
                feats.featFunctions["defence"](self)
            
        if level>2:
            
            subclassChosen = False
            
            
            if self.subclass == "hunter":
                self.classAsString="Ranger (Hunter)"
                
                colSlayer = c.e.SpellEntry("blank")
                colSlayer.preSaveNormalText = c.infoBullet + " Once per turn, you may deal an extra d8 damage to a wounded target you have hit."
                colSlayer.preSaveItalicText = "<em> (Monster Slayer) </em>"
                self.charInfos.append(colSlayer)
                
                subclassChosen = True
                
            if self.subclass == "monster slayer" or not subclassChosen:
                
                self.classAsString="Ranger (Monster Slayer)"
                self.subclass = "monster slayer"
                
                protectionFromEvilAndGood = c.e.SpellEntry("protectionFromEvilAndGood")
                self.actionEntries.append(protectionFromEvilAndGood)
                
                hunterSense = c.e.SpellEntry("blank")
                hunterSense.title = "Hunter's Sense (60ft)"
                hunterSense.preSaveNormalText = " Discern a creature's immunities, resistances, and vulnerabilities."
                count = "O "*max(1,self.modifiers[4])
                hunterSense.preSaveItalicText = "Uses per long rest -  </em>"+count+" <em>(Monster Slayer)"
                self.actionEntries.append(hunterSense)
                
                slayersPrey = c.e.SpellEntry("blank")
                slayersPrey.title = "Mark Slayer's Prey (60ft)"
                slayersPrey.preSaveNormalText = " Each turn, the first time you hit the target you deal an extra d6 damage. "
                slayersPrey.preSaveItalicText = "Effect ends if you target a new prey. (Monster Slayer)"
                self.bonusActionEntries.append(slayersPrey)
                
            #primal awareness
            swAnimals = c.e.SpellEntry("swAnimals")
            swAnimals.preSaveItalicText=" One free casting per long rest. O"
            self.actionEntries.append(swAnimals)
            
            
        
            
        if level>4:
            extraAttackEntry = c.e.TextEntry("extraAttackHighlighted")
            self.actionEntries.insert(self.highlightedBlockIndex,extraAttackEntry)
            self.highlightedBlockIndex+=1

        if level>5:
            self.speed+=5
            self.charInfos.append(c.e.Entry(" • Your speed is for walking, climbing or swimming."))
            

        # Animal Handling, Athletics, Insight, Investigation, Nature, Perception, Stealth, and Survival.
        self.skillProficiencies.append(self.pickSkillProficiency([1,3,6,7,10,11,16,17]))
        self.skillProficiencies.append(self.pickSkillProficiency([1,3,6,7,10,11,16,17]))
        self.skillProficiencies.append(self.pickSkillProficiency([1,3,6,7,10,11,16,17]))
        
        # deft explorer - expertise in stealth
        if 16 in self.skillProficiencies:
            self.skillExpertises.append(16)
        else:
            self.skillExpertises.append(self.skillProficiencies[0])
            
        
        self.spellsKnown = c.gf.getNumberFromRange(level, [1,1,2,4])
        
        