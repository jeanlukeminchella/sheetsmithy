
import Class as c
import globalFunctions as gf

channelDivinityText = "Channel Divinity"

class Cleric(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 8
        self.saveProficiencies = [4,5]
        self.defaultMod = 4
        
        self.loadScoresAndMods([12,13,14,8,15,10],inp)


        strengthOverDex = False
        if self.scores[0]>self.scores[1]:
            self.attributePriorityList = [4,2,0,1,3,5]
            strengthOverDex = True
        else:
            self.attributePriorityList = [4,2,1,0,3,5]
        
        if strengthOverDex:
            self.preferredBackgrounds = ["Guard","Farmer"]
        else:
            self.preferredBackgrounds = ["Wayfarer","Scribe","Hermit"]
            

        super().__init__(inp)
        
        
        
        self.buyItem("Amulet")
        
        self.gp+=110
        self.ritualCaster = True
        self.spellcasting = True
        if self.level in range(3,6):
            self.showUpcasting=True
        if self.level<6:
            self.showSpellRestriction=True
        self.proficientWithShields = True
        self.mediumArmorProficiency = True
        self.lightArmorProficiency = True
        
        self.highlightedEntries.append({"id":"Sacred Flame"})
        self.actions.append({"id":"Guidance"})
        
        
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
            self.spellPriorityList = [masshw,"Spiritual Weapon","Command",revivify, "Guiding Bolt","Aid","Shield of Faith",healingWord,"Sanctuary",cureWounds,"Hold Person","Lesser Restoration","Other Cleric Spell","Bless","Dispel Magic","Detect Magic","Zone of Truth","Protection from Evil and Good","Spirit Shroud"]
        
        
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
            turnUndead["preSaveNormalText"] = "Undead"
            if self.level>4:
                
                turnUndead["preSaveNormalText"] += " take "+str(self.modifiers[4])+"d8 damage and"
            
            turnUndead["preSaveNormalText"] += " spend their turns fleeing from you, Incapacitated and Frightened."
            turnUndead["preSaveItalicText"] = "WIS"+str(self.profBonus+8+self.modifiers[4])+" to resist. Ends if target takes damage. "
            channelDivinityActionEntries.append(turnUndead)
            
            divineSpark = {"type":"spell"}
            divineSpark["id"]="Divine Spark ("+channelDivinityText+", "+c.gf.getDistanceString(30)+")"
            divineSpark["preSaveNormalText"] = "Target regains d8"+gf.getSignedStringFromInt(self.modifiers[4],True)+ " hp, or takes that much radiant damage."
            divineSpark["preSaveItalicText"] = "CON"
            divineSpark["postSaveItalicText"] = " to half damage."
            channelDivinityActionEntries.append(divineSpark)
            
        if self.level>2:

            subclasses = ["war","light","trickery","life","life"]
            
            if self.subclass== "" or self.subclass==None:
                self.subclass = subclasses[self.seed%len(subclasses)]

            subclassChosen = False

            if self.subclass == "war":
                weHaveChannelDivinityThatIsNotAnAction=True
                self.classAsString="Cleric (of War)"
                subclassChosen = True
                self.actions.append({"id":"Guiding Bolt"})
                self.bonusActionEntries.append({"id":"Magic Weapon"})
                self.bonusActionEntries.append({"id":"Shield of Faith"})
                self.bonusActionEntries.append({"id":"Spiritual Weapon"})
                self.bonusActionEntries.append(["War Priest Attack.","Make a weapon or unarmed attack. " + "O "*self.modifiers[4]])
                self.shortRestEntries.append("Regain all your <strong>War Priest Attacks</strong>.")
                self.reactions.append(["Guided Strike ("+channelDivinityText+").","When an ally misses with an attack roll, boost the result by 10."," When using on yourself this does not cost a Reaction." ]) 

                if self.level>4:
                    self.actions.append({"id":"Crusader's Mantle"})
                    self.actions.append({"id":"Spirit Guardians"})

                if self.level>5:
                    self.notesForSpellCastingBlock.append("You can use a Channel Divinity to cast Shield of Faith or Spiritual Weapon. When cast this way, the spell doesn't require Concentration and lasts 1 min.")
            
            
            if self.subclass == "light":
                
                self.classAsString="Cleric (of Light)"
                subclassChosen = True

                self.addEntry("Burning Hands")
                self.addEntry("Faerie Fire")
                self.addEntry("Scorching Ray")
                self.addEntry("See Invisibility")
                channelDivinityActionEntries.append({"id":"Radiance of the Dawn"})
                wardingFlareEntry= ["Warding Flare (30ft).","Before a creature makes an attack roll, impose disadvantage on it.",""]
                self.reactions.append(wardingFlareEntry)
                
                if self.level>4:
                    self.actions.append({"id":"Fireball"})
                    self.actions.append({"id":"Daylight"})

                if self.level>5:
                    self.showUpcasting=True
                    self.shortRestEntries.append("Regain all your <strong>Warding Flares</strong>.")
                    
                    wardingFlareEntry[2]=" You may also give target of attack 2d6+"+str(self.modifiers[4])+" temporary hp."
                else:
                    self.longRestEntries.append("Regain all your <strong>Warding Flares</strong>.")
                wardingFlareEntry[2]+="</em>" +" O"*self.modifiers[4]+"<em>"
            if self.subclass == "trickery":

                self.classAsString="Cleric (of Trickery)"
                subclassChosen = True
                weHaveChannelDivinityThatIsNotAnAction=True

                self.addEntry("Charm Person")
                self.addEntry("Disguise Self")
                self.addEntry("Pass without Trace")
                self.addEntry("Invisibility")
                self.actions.append(["Blessing of the Trickster (30ft).","Choose a creature to have advantage on stealth checks.","This effect ends if you cast it on someone else or finish a Long Rest."])

                
                duplicityEntry = {"id":"Invoke Duplicity"}
                if self.level>5:
                    duplicityEntry["note"]=", during which you can swap places."
                else:
                    duplicityEntry["note"]="."
                self.bonusActionEntries.append(duplicityEntry)
               
                if self.level>4:
                    self.actions.append({"id":"Hypnotic Pattern"})
                    self.actions.append({"id":"Nondetection"})
                
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
                    masshw["note"]="<em> You regain 5 hp.</em>"
                    revivify["note"]=" You gain 5 hp."
                    
                if self.level>4:
                    self.bonusActionEntries.append(masshw)
                    self.actions.append(revivify)

                self.bonusActionEntries.append({"id":"Lesser Restoration"})
                self.actions.append(cureWounds)
                self.actions.append({"id":"Bless"})
                self.actions.append({"id":"Aid"})

        if self.level>4:
            self.showDisengage = False
            self.showDodge = False
            self.showUseObject=False
            
        if self.level>5:
            self.showDash = False
        
        if weHaveChannelDivinityThatIsNotAnAction:
            self.actions.extend(channelDivinityActionEntries)
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
                self.actions.append({"id":"channelDiv"})

        # History, Insight, Medicine, Persuasion, and Religion.
        self.skillProficiencies.append(self.pickSkillProficiency([5,6,9,13,14]))
        self.skillProficiencies.append(self.pickSkillProficiency([5,6,9,13,14]))
        

        # add a weapon for the opp attacks.
        
        if self.martialProficiency:
            if strengthOverDex:
                if self.wearingShield:

                    self.wishlist.append("Longsword")
                else:
                    self.wishlist.append("Maul")
            else:
                if self.wearingShield and self.modifiers[1]==self.modifiers[0]:
                    self.wishlist.append("Maul")
                else:

                    self.wishlist.append("Rapier")
        else:
            if strengthOverDex:
                self.wishlist.append("Mace")
            else:
                self.wishlist.append("Dagger")

        if strengthOverDex and self.level<5:
            self.highlightedEntries.append({"id":"Grapple"})
            self.highlightedEntries.append({"id":"Shove"})
        

         
