
import Class as c
import globalFunctions as gf

channelDivinityText = "Channel Divinity"

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
        
        self.highlightedEntries.append({"id":"Sacred Flame"})
        self.actionEntries.append({"id":"Guidance"})
        
        
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
        cureWounds = {"id":"Cure Wounds"}
        healingWord = {"id":"Healing Word"}
        
        #third level
        revivify = {"id":"Revivify"}
        masshw = {"id":"Mass Healing Word"}

        channelDivinityActionEntries = []
        weHaveChannelDivinityThatIsNotAnAction = False
        
        if self.level in [1,2]:
            self.spellPriorityList = ["Bless",healingWord, "Guiding Bolt","Detect Magic","Shield of Faith","Command","Sanctuary",cureWounds,"Protection from Evil and Good"]
        elif self.level in [3,4]:
            self.spellPriorityList = ["Bless",healingWord,"Aid","Spiritual Weapon", "Guiding Bolt","Hold Person","Sanctuary","Command","Shield of Faith","Lesser Restoration",cureWounds,"Detect Magic","Protection from Evil and Good","Zone of Truth"]
        elif self.level in [5,6]:
            self.spellPriorityList = [masshw,"Spiritual Weapon","Dispel Magic",revivify, "Guiding Bolt","Aid","Shield of Faith","Detect Magic",healingWord,"Sanctuary","Hold Person","Lesser Restoration","Zone of Truth" ,"Command",cureWounds,"Protection from Evil and Good","Spirit Shroud","Bless"]
        
        
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
            
            self.shortRestEntries.append("You regain one use of "+channelDivinityText+".")

            turnUndead = {"type":"spell"}
            turnUndead["id"] = "Turn Undead ("+channelDivinityText+", "+c.gf.getDistanceString(30)+")"
            turnUndead["preSaveNormalText"] = "Undead that can see or hear you"
            if self.level>4:
                
                turnUndead["preSaveNormalText"] += " take "+str(self.modifiers[4])+"d8 damage and"
            
            turnUndead["preSaveNormalText"] += " must spend their turns trying to move as far away from you as they can, Incapacitated and Frightened."
            turnUndead["preSaveItalicText"] = "WIS"+str(self.profBonus+8+self.modifiers[4])+" to resist. Ends if target takes damage. "
            channelDivinityActionEntries.append(turnUndead)
            
            divineSpark = {"type":"spell"}
            divineSpark["id"]="Divine Spark ("+channelDivinityText+", "+c.gf.getDistanceString(30)+")"
            divineSpark["preSaveNormalText"] = "Target regains d8"+gf.getSignedStringFromInt(self.modifiers[4],True)+ " hp, or takes that much radiant damage."
            divineSpark["preSaveItalicText"] = "CON"
            divineSpark["postSaveItalicText"] = " to half damage."
            channelDivinityActionEntries.append(divineSpark)
            
        if self.level>2:
            subclassChosen = False
            subclassChoice = self.subclass
    
            if self.subclass == "life" or not subclassChosen:
                
                self.subclass = "life"
                self.classAsString="Cleric (of Life)"
                subclassChosen = True
                
                cureWounds["healingBonus"] = 3
                healingWord["healingBonus"] = 3
                masshw["healingBonus"] = 5
                revivify["preSaveNormalText"] =  "You touch a creature that has died within the last minute. They return to life with 6 hp."
                
                preserveLife = []
                preserveLife.append("Preserve Life ("+channelDivinityText+", "+c.gf.getDistanceString(30)+").")
                preserveLife.append("Distribute " + str(self.level*5) +" hp to bloodied (half health) allies within range.")
                channelDivinityActionEntries.append(preserveLife)
                
                if self.level>5:
                    cureWounds["note"]="<em> You regain 3 hp.</em>"
                    healingWord["note"]="<em> You regain 3 hp.</em>"
                    masshw["note"]=".<em> You regain 5 hp</em>"
                    revivify["note"]=" You gain 5 hp."
                    
                if self.level>4:
                    self.bonusActionEntries.append(masshw)
                    self.actionEntries.append(revivify)

                self.bonusActionEntries.append({"id":"Lesser Restoration"})
                self.actionEntries.append(cureWounds)
                self.actionEntries.append({"id":"Bless"})
                self.actionEntries.append({"id":"Aid"})

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
                
                if "Entry" in str(type(ent)):
                    ent.title = ent.title.replace(channelDivinityText+", ","")
                elif type(ent)==dict:
                    ent["id"]=ent["id"].replace(channelDivinityText+", ","")    
                elif type(ent)==str:
                    ent=ent.replace(channelDivinityText+", ","")
                elif type(ent)==list:
                    ent[0]=ent[0].replace(channelDivinityText+", ","")
                    
            channelBlock = c.e.Block(channelDivinityActionEntries,"CHANNEL DIVINITY ACTIONS")
            if len(channelDivinityActionEntries)>0:

                self.rightColumnBlocks.append(channelBlock)
                self.actionEntries.append({"id":"channelDiv"})

        # History, Insight, Medicine, Persuasion, and Religion.
        self.skillProficiencies.append(self.pickSkillProficiency([5,6,9,13,14]))
        self.skillProficiencies.append(self.pickSkillProficiency([5,6,9,13,14]))
        

        # add a weapon for the opp attacks.
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
        

         
