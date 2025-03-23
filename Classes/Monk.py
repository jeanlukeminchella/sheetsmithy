import Class as c

class Monk(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 8
        self.saveProficiencies = [0,1]
        self.defaultMod = 1
        
        self.loadScoresAndMods([10,15,13,10,14,10],inp)
        self.attributePriorityList = [1,2,4,5,0,3]
        
        self.preferredBackgrounds = ["Soldier","Charlatan","Criminal"]
        
        super().__init__(inp)
        self.spellcastingMod = 4
        self.gp+=50
        level = self.level
        self.costDic["f"]="1 Focus"
        

        self.actionEntries.append({"id":"Hide"})

        self.highlightedEntries.append({"id":"Quarterstaff","finesse":True})
        self.buyItem("Quarterstaff")
        self.wishlist.append("Shortbow")
        self.wishlist.append("Dart")
        self.wishlist.append("Whip")

        # some subclass features mean the flurry of blows have an asterisk
        flurryOfBlowsAstricks = False
        
        
        fastActions = []
        
        e = {"id":"Punch","modifierIndex":1,"damage":getMartialArtsDie(self.level)}
        fastActions.append(e)
        grapple = {"id":"Grapple","modifierIndex":1}
        
        fastActions.append(grapple)
        shove = {"id":"Shove","modifierIndex":1}
        fastActions.append(shove)

        self.showDodge = False
        self.actionEntries.append({"id":"Dodge"})
        
        
        # ki block is initalised here so sublass & levelling can affect it
        kiEntry = "<strong>Focus -</strong> "+(" O"*(level))
        kiBlock = c.e.Block([kiEntry],"FOCUS")
        if self.showShortRest:
            if self.level>1:
                self.shortRestEntries.append("Regain all your <strong>Focus</strong>.")
        else:
            kiBlock.addEntry("<em>You regain all Focus after a rest.</em> ")
        
        
        if level>1:
            
            self.showDash = False
            self.showReady = False
            self.showDisengage = False
            self.actionEntries.append({"id":"Ready"})
            self.actionEntries.append({"id":"useObject"})
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
            if self.showLongRest:
                self.longRestEntries.append("Regain your use of <strong>Uncanny Metabolism</strong>.")
            else:
                uncannyMetabolismText += " <em>You must take a Long Rest before doing this again.</em>"
                
            uncannyMetabolismText += " O"
            self.charInfos.append(uncannyMetabolismText)
            
            chosen = False
            if self.subclass =="shadow":
                self.classAsString="Monk (Way of the Shadow)"
                chosen = True
                darkness = {"id":"Darkness","note":" Can be moved to any space with 60ft of you at the start of your turns. You can see within this darkness.","cost":"f"}
                self.actionEntries.append(darkness)
                self.darkvision+=60
                self.actionEntries.append({"id":"Create Minor Illusion"})

            if self.subclass == "openHand" or not chosen:
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
            self.actionEntries.insert(self.highlightedBlockIndex,extraAttackEntry)
            self.highlightedBlockIndex+=1
            
            kiBlock.entries.insert(0,{"id":"Stun"})
            
        if level>5:
            
            kiBlock.addEntry({"id":"magicalUnarmedStrike"})
            
            if self.subclass == "openHand":
                wholenessOfBody = {"id":"Wholeness of Body","type":"spell","expanded":True,"conc":False,"ritual":False}
                wholenessOfBody["preSaveNormalText"]="Regain "+getMartialArtsDie(self.level)+"+"+str(self.modifiers[4])+" hp. "
                wholenessOfBody["preSaveNormalText"]+=" O"*self.modifiers[4]
                if self.showLongRest:
                    self.longRestEntries.append("Regain all uses of <strong>Wholenes Of Body</strong>")
                else:
                    wholenessOfBody.preSaveItalicText="Regain all uses on a Long Rest"
                self.bonusActionEntries.append(wholenessOfBody)
            if self.subclass =="shadow":
                self.bonusActionEntries.append({"id":"Shadow Step"})
                    
        unarmAC = 10+self.modifiers[1]+self.modifiers[4]
        self.baseACOptions.append(unarmAC)
        
        
        #add the ki block, add the flurry of blows text
        
        if self.level>1:
            self.rightColumnBlocks.append(kiBlock)
            
            flurryString = "<strong>Flurry of Blows (1 Focus)"
            flurryString += ".</strong> Punch twice."
            if flurryOfBlowsAstricks:
                flurryString += "*"
            
            
            self.bonusActionEntries.append(flurryString)
        
        fastAction = "Take a <strong>Fast Action.</strong> <em>See Fast Action Options.</em>"
        self.actionEntries.append(fastAction)
        self.bonusActionEntries.append(fastAction)
        self.rightColumnBlocks.append(c.e.Block(fastActions,"FAST ACTION OPTIONS"))
    
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