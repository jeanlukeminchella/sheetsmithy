import Class as c
import globalFunctions as gf

wildShapeText = "Wild Shape"
wildShapeTextPlural = "Wild Shapes"

class Druid(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 8
        self.saveProficiencies = [3,4]
        self.defaultMod = 4
        
        self.loadScoresAndMods([10,14,13,10,15,10],inp)


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
            c.item.buyItem(self,"Quarterstaff")

        else:
            c.item.buyItem(self,"Sprig of Mistletoe")
            self.wishlist.append("Dagger")

        self.gp+=50
        self.spellcasting = True
        self.proficientWithShields = True
        self.lightArmorProficiency = True
        
        self.addEntry("Produce Flame")
        self.addEntry("Guidance",False)
        self.addEntry("Speak With Animals")

        primalOrders = ["magician","warden"]
        primalOrder = primalOrders[0]

        if "primalOrder" in self.choices.keys():
            if self.choices["primalOrder"] in primalOrders:
                primalOrder = self.choices["primalOrder"]
        
        if primalOrder == primalOrders[1]:
            self.martialProficiency = True
            self.mediumArmorProficiency = True
        else: 
            thaum = self.addEntry("Create Bonfire")
            # if the class already has thaumaturgy
            if not thaum:
                self.addEntry("Druidcraft")
            self.skillBoosts.append([2,self.modifiers[4]])
            self.skillBoosts.append([10,self.modifiers[4]])

        if self.level in [1,2]:
            self.spellPriorityList = ["Faerie Fire","Healing Word","Jump","Thunderwave","Entangle","Cure Wounds","Goodberry","Protection from Evil and Good"]
        elif self.level in [3,4]:
            self.spellPriorityList = ["Spike Growth","Faerie Fire","Healing Word","Barkskin","Lesser Restoration","Jump","Thunderwave","Entangle","Cure Wounds","Goodberry","Protection from Evil and Good"]
        elif self.level in [5,6]:
            self.spellPriorityList = ["Revivify","Spike Growth","Faerie Fire","Barkskin","Jump","Healing Word","Lesser Restoration","Thunderwave","Entangle","Cure Wounds","Protection from Evil and Good","Goodberry"]

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

        wildshapeAction = c.e.SpellEntry("Assume Wild Shape (Wild Shape)")
        wildshapeAction.preSaveItalicText="Lasts for up to "+str(int(self.level/2))+" hours. "
        wildshapeAction.preSaveItalicText+="Gain "+str(self.level)+" temp hp. Cannot cast new spells while transformed."


        knownForms = []
        
        if self.level<4:
            knownForms.append(c.e.TextEntry("Riding Horse"))
            knownForms.append(c.e.TextEntry("Wolf"))
            knownForms.append(c.e.TextEntry("Spider"))
            knownForms.append(c.e.TextEntry("Other Form 1"))
        else:
            knownForms.append(c.e.TextEntry("Black Bear"))
            knownForms.append(c.e.TextEntry("Crocodile"))
            knownForms.append(c.e.TextEntry("Spider"))
            knownForms.append(c.e.TextEntry("Other Form 2"))
            



        longRestRegainString = ""

        if self.level>1:

            self.bonusActionEntries.insert(0,wildshapeAction)
            self.bonusActionEntries.insert(1,c.e.TextEntry("Leave Wild Shape"))
            self.rightColumnBlocks.append(c.e.Block(knownForms,"WILD SHAPE FORMS"))
            self.shortRestEntries.append(c.e.Entry("Regain a use of Wild Shape"))
            self.actionEntries.append(c.e.TextEntry("Wild Companion"))
            longRestRegainString = "Regain your use of <strong>Wild Companion</strong>."
            
        
        if self.level>2:
            subclassChosen = False
            
            if self.subclass == "land" or not subclassChosen:
                
                self.classAsString="Druid (Circle of the Land)"
                self.subclass = "land"

                landsAid = c.e.SpellEntry("blank")
                landsAid.title = "Land's Aid (Wild Shape, 60ft)"
                landsAid.preSaveNormalText = "20ft sphere of flowers and thorns deal 2d6 necrotic damage to enemies. CON"
                landsAid.postSaveNormalText = " to half damage."
                landsAid.preSaveItalicText = " Choose an ally within sphere to regain 2d6 hp. "
                self.actionEntries.append(landsAid)

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
                        self.notesForSpellCastingBlock.append(c.e.TextEntry("Natural Recovery - arid"))

                else: 
                    pass

                if self.level>5:
                    self.longRestEntries.append(c.e.Entry("Regain your <strong>Circle of the Land</strong> free casting."))
        

        

        if self.level>4:
            self.showDisengage = False
            self.showDodge = False
            self.showUseObject=False
            self.notesForSpellCastingBlock.append(c.e.TextEntry("Wild Resurgence"))
            self.notesForSpellCastingBlock.append(c.e.TextEntry("Wild Resurgence 2"))
            longRestRegainString = "Regain your uses of <strong>Wild Companion</strong> and <strong>Wild Resurgence</strong>."
            
        if self.level>5:
            self.showDash = False

        if longRestRegainString:
            self.longRestEntries.append(c.e.Entry(longRestRegainString))

        self.makeSpellcastingBlock()
        # History, Insight, Medicine, Persuasion, and Religion.
        self.skillProficiencies.append(self.pickSkillProficiency([1,2,6,9,10,11,14,17]))
        self.skillProficiencies.append(self.pickSkillProficiency([1,2,6,9,10,11,14,17]))
        