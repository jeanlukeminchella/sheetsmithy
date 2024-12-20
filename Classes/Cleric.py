
import Class as c
import globalFunctions as gf

channelDivinityText = "Channel Divinity"
channelDivinityTextPlural = "Channel Divinities"

class Cleric(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 8
        self.saveProficiencies = [4,5]
        self.defaultMod = 4
        
        self.loadScoresAndMods([10,13,14,10,15,10],inp)


        strengthOverDex = False
        if self.scores[0]>self.scores[1]:
            self.attributePriorityList = [4,2,0,1,3,5]
            strengthOverDex = True
        else:
            self.attributePriorityList = [4,2,1,0,3,5]
        
        if strengthOverDex:
            self.preferredBackgrounds = ["Guard","Farmer"]
        else:
            self.preferredBackgrounds = ["Wayfarer","Scribe"]
            

        super().__init__(inp)
        
        
        
        c.item.buyItem(self,"Amulet")
        
        self.gp+=110
        self.ritualCaster = True
        self.spellcasting = True
        self.proficientWithShields = True
        self.mediumArmorProficiency = True
        self.lightArmorProficiency = True
        
        sacredFlame = c.e.AttackRollEntry("sacredFlame")
        self.highlightedEntries.append(sacredFlame)
        self.actionEntries.append(c.e.SpellEntry("guidance"))
        
        
        divineOrders = ["protector","thaumaturge"]
        divineOrder = divineOrders[0]
        if "divineOrder" in self.choices.keys():
            if self.choices["divineOrder"] in divineOrders:
                divineOrder = self.choices["divineOrder"]
        
        if divineOrder == divineOrders[0]:
            self.martialProficiency = True
            self.heavyArmorProficiency = True
        else: 
            thaum = self.addEntry("Thaumaturgy",False)
            # if the class already has thaumaturgy
            if not thaum:
                self.addEntry("Toll the Dead")
            self.skillBoosts.append([2,self.modifiers[4]])
            self.skillBoosts.append([14,self.modifiers[4]])
            
        
        #generate some  spells as entries, as class features may affect them (like healing for Life clerics), not all of them may the same subtype of Entry though
        
        #first level
        cureWounds = c.e.HealingEntry("cureWounds")
        healingWord = c.e.HealingEntry("healingWord")
        
        #third level
        revivify = c.e.SpellEntry("revivify")
        masshw = c.e.HealingEntry("massHealingWord")

        channelDivinityActionEntries = []
        weHaveChannelDivinityThatIsNotAnAction = False
        
        if self.level in [1,2]:
            self.spellPriorityList = ["Bless",healingWord, "Guiding Bolt","Detect Magic","Shield of Faith","Command","Sanctuary",cureWounds,"Protection from Evil and Good"]
        elif self.level in [3,4]:
            self.spellPriorityList = ["Bless",healingWord,"Aid","Spiritual Weapon", "Guiding Bolt","Hold Person","Sanctuary","Command","Shield of Faith","Lesser Restoration",cureWounds,"Detect Magic","Protection from Evil and Good","Zone of Truth"]
        elif self.level in [5,6]:
            self.spellPriorityList = [masshw,"Spiritual Weapon","Dispel Magic",revivify, "Guiding Bolt","Aid","Detect Magic",healingWord,"Sanctuary","Shield of Faith","Hold Person","Lesser Restoration","Zone of Truth" ,"Command",cureWounds,"Protection from Evil and Good","Spirit Shroud","Bless"]
        
        resourceDictionary = {
            1:[["Spell",2]],
            2:[["Spell",3],[channelDivinityText,2]],
            3:[[self.costDic["1"],4],[self.costDic["2"],2],[channelDivinityText,2]],
            4:[[self.costDic["1"],4],[self.costDic["2"],3],[channelDivinityText,2]],
            5:[[self.costDic["1"],4],[self.costDic["2"],3],[self.costDic["3"],2],[channelDivinityText,2]],
            6:[[self.costDic["1"],4],[self.costDic["2"],3],[self.costDic["3"],3],[channelDivinityText,3]]
        }
        
        if self.level <3:
            self.costDic= {
                "1":"Spell"
            }
        
        self.spellsKnown = gf.getNumberFromRange(self.level,[0,0,0,1,2,3,4,4,5])
        self.spellSlotResourceTuples=resourceDictionary[self.level]
        
        self.showReady=False

        if self.level>1:
            
            self.shortRestEntries.append(c.e.Entry("You regain one use of "+channelDivinityText+"."))

            turnUndead = c.e.SpellEntry("blank")
            turnUndead.title = "Turn Undead ("+channelDivinityText+", "+c.gf.getDistanceString(30)+")"
            turnUndead.preSaveNormalText = "Undead that can see or hear you"
            if self.level>4:
                
                turnUndead.preSaveNormalText += " take "+str(self.modifiers[4])+"d8 damage and"
            
            turnUndead.preSaveNormalText += " must spend their turns trying to move as far away from you as they can, Incapacitated and Frightened."
            turnUndead.preSaveItalicText = "WIS"+str(self.profBonus+8+self.modifiers[4])+" to resist. Ends if target takes damage. "
            channelDivinityActionEntries.append(turnUndead)
            
            divineSpark = c.e.SpellEntry("blank")
            divineSpark.title = "Divine Spark ("+channelDivinityText+", "+c.gf.getDistanceString(30)+")"
            divineSpark.preSaveNormalText = "Target regains d8"+gf.getSignedStringFromInt(self.modifiers[4],True)+ " hp, or takes that much radiant damage."
            divineSpark.preSaveItalicText = "CON"
            divineSpark.postSaveItalicText = " to half damage."
            channelDivinityActionEntries.append(divineSpark)
            
        if self.level>2:
            subclassChosen = False
            subclassChoice = self.subclass
    
            if self.subclass == "life" or not subclassChosen:
                
                self.subclass = "life"
                self.classAsString="Cleric (of Life)"
                subclassChosen = True
                
                cureWounds.healingBonus = 3
                healingWord.healingBonus = 3
                masshw.healingBonus = 5
                revivify.preSaveNormalText = revivify.preSaveNormalText.replace("1","6")
                revivify.preSaveNormalText = revivify.preSaveNormalText.replace("point","points")
                preserveLife = c.e.SpellEntry("blank")
                preserveLife.title = "Preserve Life ("+channelDivinityText+", "+c.gf.getDistanceString(30)+")"
                preserveLife.preSaveNormalText = "Distribute " + str(self.level*5) +" hp to bloodied (half health) allies within range."
                channelDivinityActionEntries.append(preserveLife)
                
                if self.level>5:
                    cureWounds.postHealText+=".<em> You regain 3 hp.</em>"
                    healingWord.postHealText+=".<em> You regain 3 hp.</em>"
                    masshw.postHealText+=".<em> You regain 5 hp</em>"
                    revivify.preSaveItalicText="You regain 5 hp."
                    
                if self.level>4:
                    self.bonusActionEntries.append(masshw)
                    self.actionEntries.append(revivify)

                self.bonusActionEntries.append(c.e.SpellEntry("lesserRestoration"))
                self.actionEntries.append(cureWounds)
                self.actionEntries.append(c.e.SpellEntry("bless"))
                self.actionEntries.append(c.e.SpellEntry("aid"))

        if self.level>4:
            self.showDisengage = False
            self.showDodge = False
            self.showUseObject=False
            
        if self.level>5:
            self.showDash = False
        
        if weHaveChannelDivinityThatIsNotAnAction:
            self.actionEntries.extend(channelDivinityActionEntries)
        else:
            for ent in channelDivinityActionEntries:
                ent.title = ent.title.replace(channelDivinityText+", ","")
            channelBlock = c.e.Block(channelDivinityActionEntries,"CHANNEL DIVINITY ACTIONS")
            if len(channelDivinityActionEntries)>0:

                self.rightColumnBlocks.append(channelBlock)
                self.actionEntries.append(c.e.TextEntry("channelDiv"))

        self.makeSpellcastingBlock()
        # History, Insight, Medicine, Persuasion, and Religion.
        self.skillProficiencies.append(self.pickSkillProficiency([5,6,9,13,14]))
        self.skillProficiencies.append(self.pickSkillProficiency([5,6,9,13,14]))
        

        # add a weapon for the opp attacks. we will make it 1h so that we can wear a shield
        self.wearingShield = True
        
        if self.martialProficiency:
            if strengthOverDex:
                self.wishlist.append("Longsword")
            else:
                self.wishlist.append("Rapier")
        else:
            if strengthOverDex:
                self.wishlist.append("Mace")
                
            else:
                self.wishlist.append("Dagger")
        

         
