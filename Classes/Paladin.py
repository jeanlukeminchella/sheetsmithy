import Class as c
import featFunctions as feats

channelDivinityText = "Channel Divinity"


class Paladin(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 10
        self.saveProficiencies = [4,5]
        self.defaultMod = 0
        self.loadScoresAndMods([15,10,14,10,10,13],inp)
        
        self.attributePriorityList = [0,5,2,1,4,3]
        self.preferredBackgrounds = ["Noble"]
        
        super().__init__(inp)
        
        self.spellcastingMod = 5
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

        self.bonusActionEntries.append("<strong>Lay on Hands. </strong>Restore hp to a touched creature from a pool of "+str(5*level)+ " hp")
        
        heroism = {"id":"Heroism","preSaveNormalText":"A willing creature you touch is imbued with bravery. Until the spell ends, the creature is immune to being frightened and gains "+str(self.modifiers[5])+" temporary hit points at the start of each of its turns."} 
        
        priorityListByMaxSpellSlot={
            "1":[{"id":"Thunderous Smite"},{"id":"Command"},{"id":"Shield of Faith"},{"id":"Wrathful Smite"},{"id":"Detect Magic"},heroism,{"id":"Cure Wounds"}, {"id":"Protection from Evil and Good"}],
            "2":[{"id":"Shining Smite"},{"id":"Thunderous Smite"},{"id":"Lesser Restoration"},{"id":"Command"},{"id":"Wrathful Smite"},{"id":"Shield of Faith"},heroism,{"id":"Cure Wounds"},{"id":"Detect Magic"}, {"id":"Protection from Evil and Good"}]
            }

        maxSpellSlot = str(c.gf.getNumberFromRange(self.level,[4]))
        self.spellPriorityList = priorityListByMaxSpellSlot[maxSpellSlot]
        
            
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
            self.bonusActionEntries.append({"id":"Divine Smite"})
            
        if level>2:

            self.bonusActionEntries.append("<strong>Divine Sense ("+channelDivinityText+", 10 mins) </strong> You know the location of any celestial, fiend, or undead within 60 feet, or any area that is desecrated or concecrated.")
            
            subclassChosen = False
            
            if self.subclass == "ancients":
                self.classAsString="Paladin (Oath of the Ancients)"
                subclassChosen = True
                self.actionEntries.append({"id":"Speak With Animals"})
                self.bonusActionEntries.append({"id":"Ensnaring Strike"})
                
                naturesWrath = {}
                naturesWrath["id"] = "Nature's Wrath ("+channelDivinityText+", 1 min)"
                naturesWrath["type"]="spell"
                naturesWrath["preSaveNormalText"] = "Vines restrain enemies within 15ft. STR"
                naturesWrath["postSaveNormalText"] = " to resist."
                naturesWrath["preSaveItalicText"] = "Target repeats save at the end of their turns."
                naturesWrath["useSpellcastingMod"]=True
                self.actionEntries.append(naturesWrath)
                
                if level>4:
                    self.actionEntries.append({"id":"Moonbeam"})
                    self.bonusActionEntries.append({"id":"Misty Step"})
                
            if self.subclass == "vengeance" or not subclassChosen:
                self.subclass = "vengeance"
                self.classAsString="Paladin (Oath of Vengeance)"
                
                self.bonusActionEntries.append({"id":"Hunter's Mark"})
                 
                self.actionEntries.append({"id":"Bane"})
                
                vowOfEmnity = {"id":"Vow of Emnity ("+channelDivinityText+", 10ft, 1 min)","type":"spell"}
                vowOfEmnity["preSaveNormalText"] = "When you attack, vow emnity with a target and gain advantage on attack rolls against them."
                self.notesForSpellCastingBlock.append(vowOfEmnity)
                
                abjureEnemy = {"id":"Vow of Emnity ("+channelDivinityText+", 10ft, 1 min)","type":"spell","useSpellcastingMod":True}
                
                abjureEnemy["id"] = "Abjure ("+channelDivinityText+", 60ft, 1 min)"
                abjureEnemy["preSaveNormalText"] = "Target is frightened and its speed is 0. WIS"
                abjureEnemy["postSaveNormalText"] = " to resist. Targets who resist still have their speed halved until they take damage."
                abjureEnemy["preSaveItalicText"] = "Fiends and Undead have disadvantage on their saving throw. "
                self.actionEntries.append(abjureEnemy)
                
                if level>4:
                    self.bonusActionEntries.append({"id":"Misty Step"})
                    self.actionEntries.append({"id":"Hold Person"})
                    
            
            self.shortRestEntries.append("You regain one use of "+channelDivinityText+".")
            

   
        if level>4:
            extraAttackEntry = {"id":"extraAttackHighlighted"}
            self.actionEntries.insert(self.highlightedBlockIndex,extraAttackEntry)
            self.highlightedBlockIndex+=1
            
        if level>5:
            self.showUseObject=False
            char = max(1,self.modifiers[5])
            auraBoosts = [[0,char],[1,char],[2,char],[3,char],[4,char],[5,char]]
            self.saveBoosts.extend(auraBoosts)
            self.charInfos.append("</strong>Allies within "+c.gf.getDistanceString(10)+" gain "+c.gf.getSignedStringFromInt(char)+" to saving throws")
        
        # Athletics, Insight, Intimidation, Medicine, Persuasion, and Religion.
        self.skillProficiencies.append(self.pickSkillProficiency([3,6,7,9,13,14]))
        self.skillProficiencies.append(self.pickSkillProficiency([3,6,7,9,13,14]))
        
        self.spellsKnown = c.gf.getNumberFromRange(level, [0,1,2,3,4])

        
        