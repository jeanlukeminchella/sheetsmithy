import Class as c
import featFunctions as feats


class Fighter(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 10
        self.saveProficiencies = [0,2]
        self.defaultMod = 0
        
        
        self.loadScoresAndMods([15,13,14,10,10,10],inp)
        
        dexBased = False
        if self.scores[1]>self.scores[0]:
            self.defaultMod = 1
            dexBased = True
            
            
        if dexBased:
            self.attributePriorityList = [1,2,4,0,5,3]
            self.preferredBackgrounds = ["Soldier","Criminal","Charlatan"]
        
        else:
            self.attributePriorityList = [0,2,1,4,5,3]
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
                c.item.buyItem(self,"Rapier")
                self.wishlist.append("Hand Crossbow")
            else:
                c.item.buyItem(self,"Shortsword")
                self.wishlist.append("offhand shortsword")
                self.wishlist.append("Heavy Crossbow")

            if self.modifiers[0]>1:
                highlightedEntriesToAdd.append("Shove")
                highlightedEntriesToAdd.append("Grapple")
             
        else:
            if self.wearingShield:
                c.item.buyItem(self,"Longsword")
                self.wishlist.append("Javelin")
            else:
                c.item.buyItem(self,"Maul")
                self.wishlist.append("Javelin")
            
            highlightedEntriesToAdd.append("Shove")
            highlightedEntriesToAdd.append("Grapple")
        
            
        
        for e in highlightedEntriesToAdd:
            self.addHighlightedEntry(e)

        
        secondWindText = "<strong>Second Wind. </strong> Regain d10+"+str(self.level)+" hp"
        if self.level>4:
            secondWindText +=  ", and move up to half your speed without provoking Opportunity Attacks. "
        else:
            secondWindText +=  ". "
            
        if not self.showShortRest:
            secondWindText +=  "<em>Regain one use on a rest. </em> "
        elif self.level==1:
            self.shortRestEntries.append("Regain one use of <strong>Second Wind</strong>.")
        secondWindText +=  "O "*c.gf.getNumberFromRange(self.level,[0,3,8])
        self.bonusActionEntries.append(secondWindText)
        
        
        fightStyle = None
        if "fightStyle" in self.choices.keys():
            fightStyle = self.choices["fightStyle"]
        if fightStyle in feats.featFunctions.keys():
            feats.featFunctions[fightStyle](self)
        else:
            feats.featFunctions["defence"](self)
        
        if self.level>1:
            actionSurgeText = "<strong>Action Surge. </strong> Take two actions. "
            if not self.showShortRest:
                actionSurgeText +=  "<em>You must rest before doing this again. </em> "
            else:
                self.shortRestEntries.append("Regain your <strong>Action Surge </strong> and <strong> Second Wind </strong>features.")
            actionSurgeText +=  "O"
            self.actionEntries.insert(0,actionSurgeText)
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
            elif self.subclass == "rune" or chosen == False:
                self.classAsString = "Fighter (Rune Knight)"
                self.subclass="rune"
                
                stoneEntry = {"id":"Stone Rune","duration":"1 min","type":"spell","rang":30,"preSaveNormalText":"When an enemy ends their turn, charm them. WIS","postSaveNormalText":" to resist.","preSaveItalicText":"Target is incapactiated and has speed 0 while charmed, repeating saves on end of turn. </em>O","modifierIndex":2}
                fireEntry = {"id":"Fire Rune","type":"spell","preSaveNormalText":"When you hit a creature with an attack, you can invoke the Fire rune, summoning firey shackles. ","preSaveItalicText":"2d6 fire damage on hit and on start of target turns, STR","postSaveItalicText":" to avoid being restrained, retry on turns end. </em>O","modiferIndex":2}
                self.skillNotes.append([6,"(advantage)"])
                self.reactions.append(stoneEntry)
                
                runeEntries = [fireEntry]
                if self.showShortRest:
                    self.shortRestEntries.append("Regain the use off all your <strong>Runes</strong>.")
                        
                else:
                    runeEntries.append("<em>You must rest before invoking each rune again.</em>")
                
                runeBlock = c.e.Block(runeEntries,"RUNES")
                self.rightColumnBlocks.append(runeBlock)
                
                giantsMight = {"type":"spell"}
                giantsMight["id"]="Giant's Might"
                giantsMight["duration"]="1 min"
                giantsMight["preSaveNormalText"]="You become large, gain advantage on Strength saves and Athletics checks, and deal an extra d6 damage once per turn."
                for i in range(self.profBonus):
                    giantsMight["preSaveNormalText"]+=" O"
                self.bonusActionEntries.append(giantsMight)
                   
        if self.level>4:
            extraAttackEntry = {"id":"extraAttackHighlighted"}
            self.actionEntries.insert(self.highlightedBlockIndex,extraAttackEntry)
            self.highlightedBlockIndex+=1
        
        
        
        #Acrobatics, Animal Handling, Athletics, History, Insight, Intimidation, Perception, and Survival.
        self.skillProficiencies.append(self.pickSkillProficiency([0,1,3,5,6,7,11,17]))
        self.skillProficiencies.append(self.pickSkillProficiency([0,1,3,5,6,7,11,17]))
        
        
        
        
        
        
        
        
        
