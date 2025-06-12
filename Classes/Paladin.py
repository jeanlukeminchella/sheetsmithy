import Class as c
import Feats as feats

channelDivinityText = "Channel Divinity"


class Paladin(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 10
        self.saveProficiencies = [4,5]
        self.defaultMod = 0
        self.loadScoresAndMods([15,12,14,8,10,13],inp)
        
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
            self.buyItem("Longsword")
        else:
            self.buyItem("Maul")

        self.wishlist.append("Holy Symbol")
        self.wishlist.append("Javelin")
        self.wishlist.append("Holy Water")
        self.addEntry("Grapple")

        if self.level<5:
            self.addEntry("Shove")

        self.bonusActionEntries.append("<strong>Lay on Hands. </strong>Restore hp to a touched creature from a pool of "+str(5*level)+ " hp")
        
        heroism = {"id":"Heroism","preSaveNormalText":"A willing creature you touch is imbued with bravery. Until the spell ends, the creature is immune to being frightened and gains "+str(self.modifiers[5])+" temporary hit points at the start of each of its turns."} 
        
        priorityListByMaxSpellSlot={
            "1":[{"id":"Thunderous Smite"},{"id":"Command"},{"id":"Shield of Faith"},{"id":"Wrathful Smite"},{"id":"Detect Magic"},heroism,{"id":"Cure Wounds"}, {"id":"Protection from Evil and Good"}],
            "2":[{"id":"Shining Smite"},{"id":"Thunderous Smite"},{"id":"Protection from Evil and Good"},{"id":"Cure Wounds"},{"id":"Lesser Restoration"},{"id":"Command"},{"id":"Wrathful Smite"},{"id":"Shield of Faith"},heroism,{"id":"Detect Magic"}]
            }

        maxSpellSlot = str(c.gf.getNumberFromRange(self.level,[4]))
        self.spellPriorityList = priorityListByMaxSpellSlot[maxSpellSlot]
        
            
        resourceDictionary = {
            1:[["Spell",2]],
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
            
        self.spellcasting = True
        if self.level in [5,6]:
            self.showUpcasting=True
        self.showSpellRestriction=True
        
        if level>1:
            fightStyle = None
            if "fightStyle" in self.choices.keys():
                fightStyle = self.choices["fightStyle"]
            if fightStyle in feats.Feats.keys():
                feats.Feats[fightStyle](self)
            else:
                feats.Feats["defence"](self)
            smite = {"id":"Divine Smite"}
            self.bonusActionEntries.append(smite)
            
        if level>2:

            subclasses = ["glory","ancients","devotion","vengeance"]
            
            if self.subclass== "" or self.subclass==None:
                self.subclass = subclasses[(self.seed%13)%len(subclasses)]

            self.bonusActionEntries.append("<strong>Divine Sense ("+channelDivinityText+", 10 mins). </strong> You know the location of any celestial, fiend, or undead within 60 feet, or any area that is desecrated or concecrated.")
            
            
            if self.subclass == "ancients":
                self.classAsString="Paladin (Oath of the Ancients)"
                self.actions.append({"id":"Speak With Animals"})
                self.bonusActionEntries.append({"id":"Ensnaring Strike"})
                
                naturesWrath = {}
                naturesWrath["id"] = "Nature's Wrath ("+channelDivinityText+", 1 min)"
                naturesWrath["type"]="spell"
                naturesWrath["preSaveNormalText"] = "Vines restrain enemies within 15ft. STR"
                naturesWrath["postSaveNormalText"] = " to resist."
                naturesWrath["preSaveItalicText"] = "Target repeats save at the end of their turns."
                naturesWrath["useSpellcastingMod"]=True
                self.actions.append(naturesWrath)
                
                if level>4:
                    self.actions.append({"id":"Moonbeam"})
                    self.bonusActionEntries.append({"id":"Misty Step"})
            
            elif self.subclass == "glory":
                self.classAsString = "Paladin (Oath of Glory)"

                smite["note"]=". Also distribute 2d8+"+str(self.level)+" temporary hp to creatures within 30ft however you choose (Oath of Glory)."
                self.addEntry("Guiding Bolt")
                self.addEntry("Heroism")
                if self.level>4:
                    self.addEntry("Enhance Ability")
                    self.addEntry("Magic Weapon")
                self.bonusActionEntries.append(["Peerless Athlete ("+channelDivinityText+", 1 hour).","You have adv. on Athletics and Acrobatics checks and your Long Jump and High Jump distances increase by 10 ft."])
            elif self.subclass == "devotion":
                self.classAsString = "Paladin (Oath of Devotion)"

                self.addEntry("Protection from Evil and Good")
                self.addEntry("Shield of Faith")
                if self.level>4:
                    self.addEntry("Aid")
                    self.addEntry("Zone of Truth")
                self.notesForSpellCastingBlock.append(["Sacred Weapon ("+channelDivinityText+", 10 mins).","When you Attack, imbue one melee weapon that you are holding with positive energy. Add "+c.gf.getSignedStringFromInt(max(1,self.modifiers[5]))+" to its attack rolls, and choose if it deals radiant damage.","Weapon also emits Bright Light for 20ft."])

            else:
                self.subclass = "vengeance"
                self.classAsString="Paladin (Oath of Vengeance)"
                
                self.bonusActionEntries.append({"id":"Hunter's Mark"})
                 
                self.actions.append({"id":"Bane"})
                
                vowOfEmnity = {"id":"Vow of Emnity ("+channelDivinityText+", 10ft, 1 min)","type":"spell"}
                vowOfEmnity["preSaveNormalText"] = "When you attack, vow emnity with a target and gain advantage on attack rolls against them."
                self.notesForSpellCastingBlock.append(vowOfEmnity)
                
                abjureEnemy = {"id":"Vow of Emnity ("+channelDivinityText+", 10ft, 1 min)","type":"spell","useSpellcastingMod":True}
                
                abjureEnemy["id"] = "Abjure ("+channelDivinityText+", 60ft, 1 min)"
                abjureEnemy["preSaveNormalText"] = "Target is frightened and its speed is 0. WIS"
                abjureEnemy["postSaveNormalText"] = " to resist. Targets who resist still have their speed halved until they take damage."
                abjureEnemy["preSaveItalicText"] = "Fiends and Undead have disadvantage on their saving throw. "
                self.actions.append(abjureEnemy)
                
                if level>4:
                    self.bonusActionEntries.append({"id":"Misty Step"})
                    self.actions.append({"id":"Hold Person"})
                    
            
            self.shortRestEntries.append("You regain one use of "+channelDivinityText+".")
            

   
        if level>4:
            extraAttackEntry = {"id":"extraAttackHighlighted"}
            self.actions.insert(self.highlightedBlockIndex,extraAttackEntry)
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

        
        