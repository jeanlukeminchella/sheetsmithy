import Class as c
import featFunctions as feats

channelDivinityText = "Channel Divinity"
channelDivinityTextPlural = "Channel Divinities"


class Paladin(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 10
        self.saveProficiencies = [4,5]
        self.defaultMod = 0
        self.loadScoresAndMods([15,10,14,10,10,13],inp)
        
        self.attributePriorityList = [0,5,2,1,4,3]
        self.preferredBackgrounds = ["Noble"]
        
        super().__init__(inp)
        
        
        self.masteries+=2
        self.lightArmorProficiency = True
        self.mediumArmorProficiency = True
        self.heavyArmorProficiency = True
        self.proficientWithShields = True
        self.martialProficiency = True
        self.gp+= 150
        
        level = self.level
        
        if self.wearingShield:
            c.item.buyItem(self,"Longsword")
        else:
            c.item.buyItem(self,"Maul")

        self.wishlist.append("Holy Symbol")
        self.wishlist.append("Javelin")
        self.addHighlightedEntry("Grapple")

        if self.level<5:
            
            self.addHighlightedEntry("Shove")
        
            
        
        
        layOnHandsEntry =c.e.SpellEntry("layHands")
        layOnHandsEntry.preSaveNormalText= "Restore hp to a touched creature from a pool of "+str(5*level)+ " hp"
        self.bonusActionEntries.append(layOnHandsEntry)
        
        #generate all the spells for easy reference
        
        # first level spells
        cureWounds = c.e.HealingEntry("cureWounds")
        healingWord = c.e.HealingEntry("healingWord")
        command = c.e.SpellEntry("command")
        shieldOfFaith = c.e.SpellEntry("shieldOfFaith")
        wrathfulSmite = c.e.SpellEntry("wrathfulSmite")
        heroism = c.e.SpellEntry("heroism")
        heroism.applyCommandList([["preSaveNormalText","A willing creature you touch is imbued with bravery. Until the spell ends, the creature is immune to being frightened and gains "+str(self.modifiers[5])+" temporary hit points at the start of each of its turns."]])
        dm = c.e.SpellEntry("detectMagic")
        ts = c.e.SpellEntry("thunderousSmite")
        protectionFromEvilAndGood = c.e.SpellEntry("protectionFromEvilAndGood")
        
        # second level spells
        lesserRestoration = c.e.SpellEntry("lesserRestoration")
        
        # subclass specific spells
        es = c.e.SpellEntry("ensnaringStrike")
        ms = c.e.SpellEntry("mistyStep")

        priorityListByMaxSpellSlot={
            "1":[ts,command,shieldOfFaith,wrathfulSmite,dm,heroism,cureWounds,protectionFromEvilAndGood],
            "2":[ts,lesserRestoration,command,wrathfulSmite,shieldOfFaith,cureWounds,heroism,dm,protectionFromEvilAndGood]
            }

        maxSpellSlot = str(c.gf.getNumberFromRange(self.level,[4]))
        self.spellPriorityList = priorityListByMaxSpellSlot[maxSpellSlot]
        for spell in self.spellPriorityList:
            spell.modiferIndex=5
            
        resourceDictionary = {
            1:[["Spell",0]],
            2:[["Spell",2]],
            3:[["Spell",3],[channelDivinityText,2]],
            4:[["Spell",3],[channelDivinityText,2]],
            5:[[self.costDic["1"],4],[self.costDic["2"],2],[channelDivinityText,2]],
            6:[[self.costDic["1"],4],[self.costDic["2"],2],[channelDivinityText,2]]
        }
        self.spellSlotResourceTuples=resourceDictionary[self.level]
        
        if level <5:
            self.costDic= {
                "1":"Spell"
            }
            
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
            
            
            
            divineSenseEntry = c.e.SpellEntry("divineSense")
            divineSenseEntry.title+=" ("+channelDivinityText+", 10 mins)"
            self.bonusActionEntries.append(divineSenseEntry)
            
            subclassChosen = False
            
            if self.subclass == "ancients":
                self.classAsString="Paladin (Oath of the Ancients)"
                subclassChosen = True
                self.actionEntries.append(c.e.SpellEntry("swAnimals"))
                self.bonusActionEntries.append(es)
                
                naturesWrath = c.e.SpellEntry("blank")
                naturesWrath.title = "Nature's Wrath ("+channelDivinityText+", 10ft)"
                naturesWrath.preSaveNormalText = "Vines restrain a foe. STR/DEX"
                naturesWrath.postSaveNormalText = " to resist."
                naturesWrath.preSaveItalicText = "Target repeats save at the end of their turns."
                naturesWrath.modiferIndex=5
                self.actionEntries.append(naturesWrath)
                
                mb = c.e.SpellEntry("moonbeam")
                mb.modiferIndex=5
                if level>4:
                    self.actionEntries.append(mb)
                    self.bonusActionEntries.append(ms)
                
            if self.subclass == "vengeance" or not subclassChosen:
                self.subclass = "vengeance"
                self.classAsString="Paladin (Oath of Vengeance)"
                
                hm = c.e.SpellEntry("huntersMark")
                self.bonusActionEntries.append(hm)
                 
                bane = c.e.SpellEntry("bane")
                bane.modiferIndex=5
                self.actionEntries.append(bane)
                
                vowOfEmnity = c.e.SpellEntry("blank")
                vowOfEmnity.title = "Vow of Emnity ("+channelDivinityText+", 10ft, 1 min)"
                vowOfEmnity.preSaveNormalText = "You gain advantage on attack rolls against target."
                self.bonusActionEntries.append(vowOfEmnity)
                
                abjureEnemy = c.e.SpellEntry("blank")
                abjureEnemy.modiferIndex=5
                abjureEnemy.title = "Abjure ("+channelDivinityText+", 60ft, 1 min)"
                abjureEnemy.preSaveNormalText = "Target is frightened and its speed is 0. WIS"
                abjureEnemy.postSaveNormalText = " to resist. Targets who resist still have their speed halved until they take damage."
                abjureEnemy.preSaveItalicText = "Fiends and Undead have disadvantage on their saving throw. "
                self.actionEntries.append(abjureEnemy)
                
                if level>4:
                    self.bonusActionEntries.append(ms)
                    
                    hp = c.e.SpellEntry("holdPerson")
                    hp.modiferIndex=5
                    self.actionEntries.append(hp)
       
            
            self.shortRestEntries.append(c.e.Entry("You regain one use of "+channelDivinityText+"."))
            

   
        if level>4:
            extraAttackEntry = c.e.TextEntry("extraAttackHighlighted")
            self.actionEntries.insert(self.highlightedBlockIndex,extraAttackEntry)
            self.highlightedBlockIndex+=1
            
        if level>5:
            self.showUseObject=False
            char = max(1,self.modifiers[5])
            auraBoosts = [[0,char],[1,char],[2,char],[3,char],[4,char],[5,char]]
            self.saveBoosts.extend(auraBoosts)
            auraText = c.e.SpellEntry("blank")
            auraText.title = "</strong>Allies within "+c.gf.getDistanceString(10)+" gain "+c.gf.getSignedStringFromInt(char)+" to saving throws<strong>"
            self.charInfos.append(auraText)
        
        # Athletics, Insight, Intimidation, Medicine, Persuasion, and Religion.
        self.skillProficiencies.append(self.pickSkillProficiency([3,6,7,9,13,14]))
        self.skillProficiencies.append(self.pickSkillProficiency([3,6,7,9,13,14]))
        
        #lets make the spellcasting block
        self.spellsKnown = c.gf.getNumberFromRange(level, [0,1,2,3,4])

        
        