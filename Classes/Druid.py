import Class as c
import globalFunctions as gf

wildShapeText = "Wild Shape"
wildShapeTextPlural = "Wild Shapes"

class Druid(c.Sheet):
    
    def __init__(self, inp):
        
        self.hitDie = 8
        self.saveProficiencies = [3,4]
        self.defaultMod = 4
        
        self.loadScoresAndMods([12,13,14,10,15,8],inp)


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
        primalOrder = primalOrders[1]

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
                self.addEntry("Thorn Whip")
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

        longRestRegainString = "Regain all uses of <strong>Wild Shape</strong>"

        
            
        
        if self.level>2:
            subclassChosen = False
            
            subclasses = ["moon","sea","star","land - polar","land - tropical","land - temperate","land - arid"]
            
            if self.subclass== "" or self.subclass==None:
                self.subclass = subclasses[self.seed%len(subclasses)]
                
            if self.subclass == "moon":
                subclassChosen = True
                self.classAsString="Druid (Circle of the Moon)"
                
                knownForms=[{"id":"Dire Wolf"},{"id":"Brown Bear"},{"id":"Other Form 4"}]
                
                potentialAC = self.modifiers[4]+13
                print("potentialAC",potentialAC)
                if potentialAC>14:
                    knownForms[0]["contents"]=[
                    "Dire Wolf. ",
                    "50ft speed, AC"+str(potentialAC)+", Large, +4 Stealth, Bite action: +5 to hit, d10+3 damage, Huge or smaller targets are knocked Prone.",
                    "Adv. vs distracted enemies (Pack Tactics)."
                    ]
                if potentialAC>11:
                    knownForms[1]["contents"]=[
                    "Brown Bear. ",
                    "30ft climb, 40ft walk speed, AC"+str(potentialAC)+", Large, Multiattack action (Bite & Claws): Bite: +5 to hit, d8+3 damage. Claw: +5 to hit, d4+3 damage, Huge or smaller targets are knocked Prone.",
                    ""
                    ]
                wildshapeAction["preSaveItalicText"]="Lasts for up to "+str(int(self.level/2))+" hour"
                if int(self.level/2)>1:
                    wildshapeAction["preSaveItalicText"]+="s."
                else:
                    wildshapeAction["preSaveItalicText"]+="."

                wildshapeAction["preSaveItalicText"]+=" Gain "+str(3*self.level)+" temp hp. Can only cast </em>☽<em> spells while transformed."

     
                self.actions.extend([{"id":"Cure Wounds","note":"</em>☽<em>","postHealText":"."},{"id":"Moonbeam","note":" </em>☽<em>"}])
                self.highlightedEntries.append({"id":"Starry Wisp","note":"</em>☽<em>"})
            
            if self.subclass == "sea":
                subclassChosen = True
                self.classAsString="Druid (Circle of the Sea)"
                
                self.addEntry("Ray of Frost")
                self.addEntry("Fog Cloud")
                self.addEntry("Gust of Wind")
                self.addEntry("Shatter")
                self.addEntry("Thunderwave")

                if self.level>4:
                    self.addEntry("Lightning Bolt")
                    self.addEntry("Water Breathing")

                rangeString = "5ft"
                if self.level>5:
                    rangeString = "10ft"
                    self.charInfos.append("Your speed is for walking or swimming.")

                self.bonusActionEntries.append( ["Wrath of the Sea (Wild Shape, 10 mins).","Manifest a "+rangeString+" emanation and Invoke Wrath of the Sea.",""])
                self.bonusActionEntries.append( ["Invoke Wrath of the Sea.","Choose a creature in your emanation. They take "+str(self.modifiers[4])+"d6 cold damage and if Large or smaller are pushed 15ft away. CON"+str(10+self.profBonus+self.modifiers[4])+" to resist.",""])
            if self.subclass == "star":
                subclassChosen = True
                self.classAsString="Druid (Circle of the Stars)"
                
                self.actions.append({"id":"Guiding Bolt","note":"Free castings - </em>"+str("O "*self.modifiers[4]+"<em>")})
                # character already will have guidance as its the first pick for a druid cantrip, so grant spare the dying instead
                self.addEntry("Spare the Dying")
                self.bonusActionEntries.append( ["Take on Starry Form (Wild Shape, 10 mins).","","See Starry Forms"])
                starryForms = []
                starryForms.append(["Archer.","Allows the use of Luminous Arrow.",""])
                starryForms.append(["Chalice.","Whenever you cast a spell using a spell slot that restores Hit Points to a creature, you or another creature within 30 feet of you can regain Hit Points equal to d8"+str(self.modifiers[4]),""])
                starryForms.append(["Archer.","When you make a Int or Wis check or a Con save to maintain concentration, treat a roll of 9 or lower as a 10.",""])
                self.middleColumnBlocks.append(c.e.Block(starryForms,"STARRY FORMS"))
                self.bonusActionEntries.append({"id":"Luminous Arrow - Archer"})

                if self.level>5:
                    self.longRestEntries.append("Roll a d20. If it is odd then you lose the Weal reaction, or Woe if even. You regain all uses of your active reaction.")
                    self.reactions.append(["Weal (30ft)","Whenever a creature is about to roll a d20, add d6. "+str("O "*self.modifiers[4])])
                    self.reactions.append(["Woe (30ft)","Whenever a creature is about to roll a d20, remove d6. "+str("O "*self.modifiers[4])])

            if "land" in self.subclass  or not subclassChosen:
                
                self.classAsString="Druid (Circle of the Land)"
                

                landsAid = {"type":"spell"}

                landsAid["id"] = "Land's Aid (Wild Shape, 60ft)"
                landsAid["preSaveNormalText"] = "20ft sphere deals 2d6 necrotic damage to enemies. CON"
                landsAid["postSaveNormalText"] = " to half damage."
                landsAid["preSaveItalicText"] = " Choose an ally within sphere to regain 2d6 hp. "
                self.actions.append(landsAid)

                lands = ["arid","polar","temperate","tropical"]
                land = lands[0]

                for l in lands:
                    if l in self.subclass:
                        land = l
                
                if land == lands[0]:
                    self.addEntry("Fire Bolt")
                    self.addEntry("Burning Hands")
                    self.addEntry("Blur")
                    if self.level>4:
                        self.addEntry("Fireball")
                    if self.level>5:
                        self.notesForSpellCastingBlock.append({"id":"Natural Recovery - arid"})
                elif land == lands[1]:

                    self.addEntry("Fog Cloud")
                    self.addEntry("Hold Person")
                    self.addEntry("Ray of Frost",False)

                    if self.level>4:
                        self.addEntry("Sleet Storm")
                    if self.level>5:
                        self.notesForSpellCastingBlock.append({"id":"Natural Recovery - polar"})
                        
                elif land == lands[2]:

                    self.addEntry("Misty Step")
                    self.addEntry("Shocking Grasp",False)
                    self.addEntry("Sleep")

                    if self.level>4:
                        self.addEntry("Lightning Bolt")
                    if self.level>5:
                        self.notesForSpellCastingBlock.append({"id":"Natural Recovery - temperate"}) 
                
                elif land == lands[3]:

                    self.addEntry("Acid Splash",False)
                    self.addEntry("Ray of Sickness")
                    self.addEntry("Web")

                    if self.level>4:
                        self.addEntry("Stinking Cloud")
                    if self.level>5:
                        self.notesForSpellCastingBlock.append({"id":"Natural Recovery - tropical"})  

                if self.level>5:
                    self.longRestEntries.append("Regain your <strong>Circle of the Land</strong> free casting.")
        
        
            
        
        
        if self.level>1:

            self.bonusActionEntries.insert(0,wildshapeAction)
            self.bonusActionEntries.insert(1,{"id":"Leave Wild Shape"})
            self.rightColumnBlocks.append(c.e.Block(knownForms,"WILD SHAPE FORMS"))

            self.shortRestEntries.append("Regain a use of <strong>Wild Shape</strong>.")
            self.actions.append({"id":"Wild Companion"})
            longRestRegainString = "Regain your uses of <strong>Wild Shape</strong> and <strong>Wild Companion</strong>."

        if self.level>4:
            self.showDisengage = False
            self.showDodge = False
            self.showUseObject=False
            self.notesForSpellCastingBlock.append({"id":"Wild Resurgence"})
            self.notesForSpellCastingBlock.append({"id":"Wild Resurgence 2"})
            longRestRegainString = "Regain your uses of <strong>Wild Companion</strong>, <strong>Wild Shape</strong> and <strong>Wild Resurgence</strong>."
            self.showDash = False

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
        