import Class as c
import globalFunctions as gf

wildShapeText = "Wild Shape"
wildShapeTextPlural = "Wild Shapes"

class Druid(c.Sheet):
    
    def __init__(self, inp):
        
        self.hitDie = 8
        self.saveProficiencies = [3,4]
        self.defaultMod = 4
        
        self.loadScoresAndMods([12,14,13,10,15,8],inp)


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
        
        
        
        if strengthOverDex:
            self.buyItem("Quarterstaff")

        else:
            self.buyItem("Sprig of Mistletoe")

        self.gp+=50
        self.spellcasting = True
        if self.level in range(3,5):
            self.showUpcasting=True
        if self.level<6:
            self.showSpellRestriction=True
        self.proficientWithShields = True
        self.lightArmorProficiency = True
        
        
        

        primalOrders = ["magician","warden"]
        primalOrder = primalOrders[0]

        if "primalOrder" in self.choices.keys():
            if self.choices["primalOrder"] in primalOrders:
                primalOrder = self.choices["primalOrder"]
        
        if primalOrder == primalOrders[1]:
            self.martialProficiency = True
            self.mediumArmorProficiency = True
        else: 
            bon = self.addEntry("Create Bonfire")
            # if the class already has create bon
            if not bon:
                self.addEntry("Druidcraft")
            self.skillBoosts.append([2,self.modifiers[4]])
            self.skillBoosts.append([10,self.modifiers[4]])

        if self.level<6:

            self.addEntry("Produce Flame")
        else:
            # we need the entry to only take up one line really - and not be highlighted
            self.addEntry("Produce Flame",False)
            
        self.addEntry("Guidance",False)
        self.addEntry("Speak With Animals")

        if self.level in [1,2]:
            self.spellPriorityList = ["Faerie Fire","Healing Word","Jump","Thunderwave","Entangle","Cure Wounds","Goodberry","Protection from Evil and Good"]
        elif self.level in [3,4]:
            self.spellPriorityList = ["Spike Growth","Faerie Fire","Healing Word","Barkskin","Lesser Restoration","Jump","Thunderwave","Entangle","Cure Wounds","Goodberry","Protection from Evil and Good"]
        elif self.level in [5,6]:
            self.spellPriorityList = ["Revivify","Spike Growth","Barkskin","Jump","Healing Word","Lesser Restoration","Entangle","Cure Wounds","Protection from Poison","Other Druidic Spell","Faerie Fire","Goodberry","Thunderwave"]

        resourceDictionary = {
            1:[["Spell",2]],
            2:[["Spell",3],[wildShapeText,2]],
            3:[[self.costDic["1"],4],[self.costDic["2"],2],[wildShapeText,2]],
            4:[[self.costDic["1"],4],[self.costDic["2"],3],[wildShapeText,2]],
            5:[[self.costDic["1"],4],[self.costDic["2"],3],[self.costDic["3"],2],[wildShapeText,2]],
            6:[[self.costDic["1"],4],[self.costDic["2"],3],[self.costDic["3"],3],[wildShapeText,3]]
        }
        
        if self.level <3:
            self.costDic= {
                "1":"Spell"
            }
        
        self.spellsKnown = gf.getNumberFromRange(self.level,[0,0,0,1,2,3,4,4,5])
        self.spellSlotResourceTuples=resourceDictionary[self.level]
        
        self.showReady=False

        wildshapeAction = {"id":"Assume Wild Shape (Wild Shape)","type":"spell"}
        wildshapeAction["preSaveItalicText"]="Lasts for up to "+str(int(self.level/2))+" hours. "
        wildshapeAction["preSaveItalicText"]+="Gain "+str(self.level)+" temp hp. Cannot cast new spells while transformed."


        knownForms = []
        
        if self.level<4:
            knownForms.append({"id":"Riding Horse"})
            knownForms.append({"id":"Wolf"})
            knownForms.append({"id":"Spider"})
            knownForms.append({"id":"Other Form 1"})
        elif self.level==5:
            knownForms.append({"id":"Black Bear"})
            knownForms.append({"id":"Crocodile"})
            knownForms.append({"id":"Spider"})
            knownForms.append({"id":"Other Form 2"})
        else:            
            knownForms.append({"id":"Black Bear"})
            knownForms.append({"id":"Crocodile"})
            knownForms.append({"id":"Other Form 3"})

        longRestRegainString = ""

        if self.level>1:

            self.bonusActionEntries.insert(0,wildshapeAction)
            self.bonusActionEntries.insert(1,{"id":"Leave Wild Shape"})
            self.rightColumnBlocks.append(c.e.Block(knownForms,"WILD SHAPE FORMS"))
            self.shortRestEntries.append("Regain a use of Wild Shape")
            self.actions.append({"id":"Wild Companion"})
            longRestRegainString = "Regain your use of <strong>Wild Companion</strong>."
            
        
        if self.level>2:
            subclassChosen = False
            
            if self.subclass == "land" or not subclassChosen:
                
                self.classAsString="Druid (Circle of the Land)"
                self.subclass = "land"

                landsAid = {"type":"spell"}

                landsAid["id"] = "Land's Aid (Wild Shape, 60ft)"
                landsAid["preSaveNormalText"] = "20ft sphere deals 2d6 necrotic damage to enemies. CON"
                landsAid["postSaveNormalText"] = " to half damage."
                landsAid["preSaveItalicText"] = " Choose an ally within sphere to regain 2d6 hp. "
                self.actions.append(landsAid)

                lands = ["arid"]
                land = lands[0]

                if "land" in self.choices.keys():
                    if self.choices["land"] in lands:
                        land = self.choices["land"]
                
                if land == lands[0]:
                    self.addEntry("Fire Bolt")
                    self.addEntry("Burning Hands")
                    self.addEntry("Blur")
                    if self.level>4:
                        self.addEntry("Fireball")
                    if self.level>5:
                        self.notesForSpellCastingBlock.append({"id":"Natural Recovery - arid"})
                else: 
                    pass

                if self.level>5:
                    self.longRestEntries.append("Regain your <strong>Circle of the Land</strong> free casting.")
        
        if self.level>4:
            self.showDisengage = False
            self.showDodge = False
            self.showUseObject=False
            self.notesForSpellCastingBlock.append({"id":"Wild Resurgence"})
            self.notesForSpellCastingBlock.append({"id":"Wild Resurgence 2"})
            longRestRegainString = "Regain your uses of <strong>Wild Companion</strong> and <strong>Wild Resurgence</strong>."
            self.showDash = False
            
        if longRestRegainString:
            self.longRestEntries.append(longRestRegainString)
        
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

        # History, Insight, Medicine, Persuasion, and Religion.
        self.skillProficiencies.append(self.pickSkillProficiency([1,2,6,9,10,11,14,17]))
        self.skillProficiencies.append(self.pickSkillProficiency([1,2,6,9,10,11,14,17]))
        