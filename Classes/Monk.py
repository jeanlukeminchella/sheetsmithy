import Class as c

class Monk(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 8
        self.saveProficiencies = [0,1]
        self.defaultMod = 1
        
        self.loadScoresAndMods([10,15,13,8,14,12],inp)
        self.attributePriorityList = [1,2,4,5,0,3]
        
        self.preferredBackgrounds = ["Soldier","Charlatan","Criminal"]
        
        super().__init__(inp)
        self.spellcastingMod = 4
        self.gp+=50
        level = self.level
        self.costDic["f"]="Focus"
        

        self.actions.append({"id":"Hide"})

        self.highlightedEntries.append({"id":"Quarterstaff","finesse":True})
        self.buyItem("Quarterstaff")
        self.wishlist.append("Shortbow")
        self.wishlist.append("Dart")
        self.wishlist.append("Whip")

        # some subclass features mean the flurry of blows have an asterisk or a note afterwards
        flurryOfBlowsAstricks = False
        flurryNote = ""
        
        
        fastActions = []
        
        e = {"id":"Punch","modifierIndex":1,"damage":getMartialArtsDie(self.level)}
        fastActions.append(e)
        grapple = {"id":"Grapple","modifierIndex":1}
        
        fastActions.append(grapple)
        shove = {"id":"Shove","modifierIndex":1}
        fastActions.append(shove)

        self.showDodge = False
        self.actions.append({"id":"Dodge"})
        
        
        # ki block is initalised here so sublass & levelling can affect it
        kiEntry = "<strong>Focus -</strong> "+(" O"*(level))
        kiEntries = [kiEntry]
        kiBlock = c.e.Block(kiEntries,"FOCUS")
        if self.hideShortRest:
            kiBlock.addEntry("<em>You regain all Focus after a rest.</em> ")
        else:
            if self.level>1:
                self.shortRestEntries.append("Regain all your <strong>Focus</strong>.")
            
        
        if level>1:
            
            self.showDash = False
            self.showReady = False
            self.showDisengage = False
            self.actions.append({"id":"Ready"})
            self.actions.append({"id":"useObject"})
            self.showUseObject=False
            
            fastActions.append("<strong>Disengage.</strong> <em>See Opportunity Attack. Spend 1 Focus to also Dodge or Dash.</em>")
            fastActions.append({"id":"Dash"})
            
            self.speed+=getSpeedBonus(self.level)
            
            
        if level>2:
  
            
            bold = "Deflect. "
            mid = "When hit with a physical attack, you may deflect d10"
            mid += c.gf.getSignedStringFromInt(self.level+self.modifiers[1])
            mid += " damage."
            
            it = "For 1 ki, redirect 2"+getMartialArtsDie(self.level)+"+"+str(self.modifiers[1])+" damage if incoming damage reduced to zero. DEX"+str(self.modifiers[4]+self.profBonus+8)+" to dodge. Ranged attacks can deflect within 60ft."
            
            deflectMissileEntry = [bold,mid,it]
        
            self.reactions.append(deflectMissileEntry)
            
            uncannyMetabolismText = "<strong>Uncanny Metabolism. </strong> When you roll initiative, regain"
            uncannyMetabolismText += " all Focus and "+getMartialArtsDie(self.level)+"+"+str(self.level)+" hp."
            if self.hideLongRest:
                self.longRestEntries.append("Regain your use of <strong>Uncanny Metabolism</strong>.")
            else:
                uncannyMetabolismText += " <em>You must take a Long Rest before doing this again.</em>"
                
            uncannyMetabolismText += " O"
            self.charInfos.append(uncannyMetabolismText)
            
            subclasses = ["shadow","openHand","mercy","elements"]
            
            if self.subclass== "" or self.subclass==None:
                self.subclass = subclasses[(self.seed%13)%len(subclasses)]

            
            if self.subclass =="shadow":
                self.classAsString="Monk (Way of the Shadow)"
                
                darkness = {"id":"Darkness","note":" Can be moved to any space with 60ft of you at the start of your turns. You can see within this darkness.","cost":"f"}
                self.actions.append(darkness)
                self.darkvision+=60
                self.actions.append({"id":"Create Minor Illusion"})
            elif self.subclass =="elements":
                self.classAsString="Monk (Way of the Elements)"
                kiEntries.append(["Elemental Attunement (Focus, 10 min).","At the start of your turn, imbue yourself with elemental energy. While active, your Punches have a reach of 15ft and deal Acid, Bludgeoning, Cold, Fire, Lightning, or Thunder (your choice) and target is knocked 10ft away from you, STR"+str(8+self.profBonus+self.modifiers[4])+" to stay put.","Ends early if you are Incapacitated."])
                self.addEntry("Elementalism",False)
                if self.level>5:
                    elementalBurst = {"id":"Elemental Burst","cost":"FF","rang":120,"preSaveNormalText":"Cause elemental energy to burst in a 40ft ball centered on a point within range. Choose a damage type: Acid, Cold, Fire, Lightning, or Thunder. Occupants take 3d8 damage. DEX","postSaveNormalText":" to half damage."}
                    self.costDic["FF"]="2 Focus"
                    elementalBurst["type"]="spell"
                    elementalBurst["useSpellcastingMod"]=True
                    self.actions.append(elementalBurst)

            elif self.subclass == "mercy":
                self.classAsString="Monk (Way of Mercy)"
                handOfHarm = ["Hand of Harm (Focus).","Boost a Punch damage roll by "+getMartialArtsDie(self.level)+"+"+str(self.modifiers[4])+" necrotic.","Can only be used once per turn."]
                kiEntries.append(handOfHarm)
                handOfHeal = ["Hand of Healing (Focus).","Touch a creature and give them "+getMartialArtsDie(self.level)+"+"+str(self.modifiers[4])+" hp."]
                if self.level>5:
                    handOfHeal.append("You can also end one of the following conditions on the creature: Blinded, Deafened, Paralyzed, Poisoned, or Stunned.")
                    handOfHarm[2]+=" Target is also Poisoned until the end of your next turn."
                self.actions.append(handOfHeal)
                flurryNote = "<em> Or Punch once, and use Hand of Healing for free.</em>"
                self.skillProficiencies.append(6)
                self.skillProficiencies.append(9)
                self.wishlist.append("Herbalism Kit")


            elif self.subclass == "elements":
                self.classAsString="Monk (Way of the Elements)"

            else:
                self.subclass = "openHand"
                self.classAsString="Monk (Way of the Open Hand)"
                e1 = "*When you hit with a Flurry of Blows attack, subject the target to one of the below effects."
                flurryOfBlowsAstricks = True
                e2 = {"id":"Knock Prone"}
                e3 = {"id":"Throw 15ft"}

                e4 = "<strong>Addle.</strong> Target cannot take Opportunity Attacks until its turn."
                b = c.e.Block([e1,e2,e3,e4],"WAY OF THE OPEN HAND")
                self.rightColumnBlocks.append(b)
        
        if level>3:
            
            slowFall = ["Slow Fall.","Reduce fall damage by "+str(5*level)+". ",""]
            self.reactions.append(slowFall)
            
        if level>4:
            
            extraAttackEntry = {"id":"extraAttackHighlighted"}
            self.actions.insert(self.highlightedBlockIndex,extraAttackEntry)
            self.highlightedBlockIndex+=1
            
            kiBlock.entries.insert(0,{"id":"Stun"})
            
        if level>5:
            
            kiBlock.addEntry({"id":"magicalUnarmedStrike"})
            
            if self.subclass == "openHand":
                wholenessOfBody = {"id":"Wholeness of Body","type":"spell","expanded":True,"conc":False,"ritual":False}
                wholenessOfBody["preSaveNormalText"]="Regain "+getMartialArtsDie(self.level)+"+"+str(self.modifiers[4])+" hp. "
                wholenessOfBody["preSaveNormalText"]+=" O"*self.modifiers[4]
                if not self.hideLongRest:
                    self.longRestEntries.append("Regain all uses of <strong>Wholenes Of Body</strong>")
                else:
                    wholenessOfBody["preSaveItalicText"]="Regain all uses on a Long Rest"
                self.bonusActionEntries.append(wholenessOfBody)
            if self.subclass =="shadow":
                self.bonusActionEntries.append({"id":"Shadow Step"})
                    
        unarmAC = 10+self.modifiers[1]+self.modifiers[4]
        self.baseACOptions.append(unarmAC)
        
        
        #add the ki block, add the flurry of blows text
        
        if self.level>1:
            self.rightColumnBlocks.append(kiBlock)
            
            flurryString = "<strong>Flurry of Blows (Focus)"
            flurryString += ".</strong> Punch twice."
            flurryString += flurryNote
            if flurryOfBlowsAstricks:
                flurryString += "*"
            
            
            
            self.bonusActionEntries.append(flurryString)
        
        fastAction = "Take a <strong>Fast Action.</strong> <em>See Fast Action Options.</em>"
        self.actions.append(fastAction)
        self.bonusActionEntries.append(fastAction)
        self.middleColumnBlocks.append(c.e.Block(fastActions,"FAST ACTION OPTIONS"))
    
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,5,6,14,16]))
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,5,6,14,16]))
        
        #Acrobatics, Athletics, History, Insight, Religion, and Stealth.
        
        
        
def getMartialArtsDie(level):
    martialArtsDie = c.gf.getNumberFromRange(level,[0,0,0,0,0,4,4,9,9,16,16])
    return "d"+str(martialArtsDie)

def getSpeedBonus(level):
    speedBoost = c.gf.getNumberFromRange(level,[1,1,5,10,14,18],0)
    speedBoost = speedBoost*5
    return int(speedBoost)