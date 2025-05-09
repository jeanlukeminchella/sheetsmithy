import Class as c
import Feats as feats


class Fighter(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 10
        self.saveProficiencies = [0,2]
        self.defaultMod = 0
        
        
        self.loadScoresAndMods([15,13,14,12,10,8],inp)
        
        dexBased = False
        if self.scores[1]>self.scores[0]:
            self.defaultMod = 1
            dexBased = True
            
            
        if dexBased:
            self.attributePriorityList = [1,2,3,4,0,5]
            self.preferredBackgrounds = ["Soldier","Criminal","Charlatan"]
        
        else:
            self.attributePriorityList = [0,2,3,1,4,5]
            self.preferredBackgrounds = ["Soldier","Farmer"]
        
        super().__init__(inp)

        self.masteries+=3
        self.lightArmorProficiency = True
        self.mediumArmorProficiency = True
        self.heavyArmorProficiency = True
        self.proficientWithShields = True
        self.martialProficiency = True
        self.gp+=155

        highlightedEntriesToAdd = []
        
        if dexBased:
            if self.wearingShield:
                self.buyItem("Rapier")
                self.wishlist.append("Hand Crossbow")
            else:
                self.buyItem("Shortsword")
                self.wishlist.append("offhand shortsword")
                if self.level<5:

                    self.wishlist.append("Heavy Crossbow")
                else:
                    self.wishlist.append("Longbow")

            if self.modifiers[0]>1:
                highlightedEntriesToAdd.append("Shove")
                highlightedEntriesToAdd.append("Grapple")
             
        else:
            if self.wearingShield:
                self.buyItem("Longsword")
                self.wishlist.append("Javelin")
            else:
                self.buyItem("Maul")
                self.wishlist.append("Javelin")
            
            highlightedEntriesToAdd.append("Shove")
            highlightedEntriesToAdd.append("Grapple")
        
            
        
        for e in highlightedEntriesToAdd:
            self.addEntry(e)

        
        secondWindText = "<strong>Second Wind. </strong> Regain d10+"+str(self.level)+" hp"
        if self.level>4:
            secondWindText +=  ", and move up to half your speed without provoking Opportunity Attacks. "
        else:
            secondWindText +=  ". "
            
        if self.hideShortRest:
            secondWindText +=  "<em>Regain one use on a short rest. </em> "
        else:
            
            if self.level==1:
                self.shortRestEntries.append("Regain one use of <strong>Second Wind</strong>.")
            self.longRestEntries.append("Regain all uses of <strong>Second Wind</strong>.")
        secondWindText +=  "O "*c.gf.getNumberFromRange(self.level,[0,3,8])
        self.bonusActionEntries.append(secondWindText)
        
        
        fightStyle = None
        if "fightStyle" in self.choices.keys():
            fightStyle = self.choices["fightStyle"]
        if fightStyle in feats.Feats.keys():
            feats.Feats[fightStyle](self)
        else:
            feats.Feats["defence"](self)
        
        if self.level>1:
            actionSurgeText = "<strong>Action Surge. </strong> Take two actions. "
            if self.hideShortRest:
                actionSurgeText +=  "<em>You must rest before doing this again. </em> "
            else:
                self.shortRestEntries.append("Regain your <strong>Action Surge </strong> and <strong> Second Wind </strong>features.")
            actionSurgeText +=  "O"
            self.actions.insert(0,actionSurgeText)
            self.highlightedBlockIndex+=1
            self.charInfos.append("<strong>Tactical Mind. </strong> Spend a use of your Second Wind feature to boost an ability check by d10.")

        if self.level>2:
            chosen = False
            if self.subclass == "champion":
                chosen = True
                
                self.charInfos.append("You Critically Hit on a 19 or 20, and can move up to half your speed when you do so, without provoking Opportunity Attacks.")
                self.charInfos.append("You have advantage on Initiative rolls.")
                self.skillNotes.append([3,"(advantage)"])
                self.classAsString = "Fighter (Champion)"
            
            elif self.subclass == "battle master":
                chosen = True
                self.classAsString = "Fighter (Battle Master)"
                self.skillProficiencies.append(self.pickSkillProficiency([0,1,3,5,6,7,11,17]))

                self.charInfos.append("You have four Maneuvers (Superiority Dice) - O O O O")
                #self.charInfos.append({"id":"Ambush"})
                self.highlightedEntries.append({"id":"Commander's Strike"})
                self.reactions.append({"id":"Riposte"})
                self.bonusActionEntries.append({"id":"Feinting Attack"})
                self.shortRestEntries.append("Regain all your <strong>Maneuvers (Superiority Dice)</strong>")

            elif self.subclass == "psi":
                chosen = True
                self.classAsString = "Fighter (Psi Warrior)"
                
                energyDice = "d6"
                resourceString = "You have "
                countString =  "O O O O"
                if self.level<4:
                    resourceString+="four"
                else:
                    resourceString+="six"
                    countString+=" O O"
                    energyDice="d8"
                resourceString+=" <strong>Psionic Energy Dice </strong>- "


                self.charInfos.append(["Psionic Strike (30ft).","Once per turn, you can spend an Energy die and boost a damage roll by "+energyDice+"+"+str(self.modifiers[3])+" force damage."])
                self.reactions.append(["Protective Field.","When you or an ally within 30ft takes damage, spend an Energy die to reduce the damage by "+energyDice+"+"+str(self.modifiers[3])+".",""])
                self.actions.append(["Telekenetic Movement.","Move a Large or smaller object or willing creature up to 30ft.","Requires an Energy die once you have used your free casting - </em>O<em>"])
                self.charInfos.append(resourceString+countString)
                self.shortRestEntries.append("Regain all your <strong>Psionic Energy </strong>dice and your free casting of <strong>Telekenetic Movement</strong>")

            elif self.subclass == "rune":
                chosen = True
                self.classAsString = "Fighter (Rune Knight)"
                self.subclass="rune"
                
                stoneEntry = {"id":"Stone Rune","duration":"1 min","type":"spell","rang":30,"preSaveNormalText":"When an enemy ends their turn, charm them. WIS","postSaveNormalText":" to resist.","preSaveItalicText":"Target is incapactiated and has speed 0 while charmed, repeating saves on end of turn. </em>O","modifierIndex":2}
                fireEntry = {"id":"Fire Rune","type":"spell","preSaveNormalText":"When you hit a creature with an attack, you can invoke the Fire rune, summoning firey shackles. ","preSaveItalicText":"2d6 fire damage on hit and on start of target turns, STR","postSaveItalicText":" to avoid being restrained, retry on turns end. </em>O","modiferIndex":2}
                self.skillNotes.append([6,"(advantage)"])
                self.reactions.append(stoneEntry)
                
                runeEntries = [fireEntry]
                if self.hideShortRest:
                    runeEntries.append("<em>You must rest before invoking each rune again.</em>")
                else:
                    self.shortRestEntries.append("Regain the use off all your <strong>Runes</strong>.")
                
                runeBlock = c.e.Block(runeEntries,"RUNES")
                self.rightColumnBlocks.append(runeBlock)
                
                giantsMight = {"type":"spell"}
                giantsMight["id"]="Giant's Might"
                giantsMight["duration"]="1 min"
                giantsMight["preSaveNormalText"]="You become large, gain advantage on Strength saves and Athletics checks, and deal an extra d6 damage once per turn."
                for i in range(self.profBonus):
                    giantsMight["preSaveNormalText"]+=" O"
                self.bonusActionEntries.append(giantsMight)

            if self.subclass == "eldritch" or chosen == False:
                chosen = True
                self.spellcasting = True
                self.spellcastingMod = 3
                spellString = "1st-level-spell"
                if self.level<5:
                    spellString = "Spell"

                self.spellSlotResourceTuples=[[spellString,2]]
                self.spellsKnown=3
                if self.level>3:
                    self.spellsKnown=4
                    self.spellSlotResourceTuples=[[spellString,3]]
                self.spellPriorityList=["Feather Fall","Shield","Jump","Sleep","Thunderwave","Burning Hands"]

                cantrips = ["Ray of Frost","Shocking Grasp","Fire Bolt"]
                picked = 0
                for cantrip in cantrips:
                    if picked <3:    
                        added = self.addEntry(cantrip,False)
                        if added:
                            picked += 1

                self.charInfos.append(["War Bond.","Choose two weapons to bond with. You cannot be disarmed of that weapon while concious.","Changing your bond to a new weapon requires a 1 hour ritual."])
                self.bonusActionEntries.append(["Summon Weapon.","A weapon you have bonded with teleports instantly to your hand."])
                self.wishlist.append("Quarterstaff")
                # second level spell is needed for species that unlock them at level 5
                if self.level<5:
                    self.costDic= {
                    "1":"Spell",
                    }


                self.classAsString = "Fighter (Eldritch Knight)"
                   
        if self.level>4:
            extraAttackEntry = {"id":"extraAttackHighlighted"}
            self.actions.insert(self.highlightedBlockIndex,extraAttackEntry)
            self.highlightedBlockIndex+=1
        
        
        
        #Acrobatics, Animal Handling, Athletics, History, Insight, Intimidation, Perception, and Survival.
        self.skillProficiencies.append(self.pickSkillProficiency([0,1,3,5,6,7,11,17]))
        self.skillProficiencies.append(self.pickSkillProficiency([0,1,3,5,6,7,11,17]))
        
        
        
        
        
        
        
        
        
