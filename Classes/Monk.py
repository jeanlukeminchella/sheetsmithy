import Class as c
import featFunctions as feats

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
        
        

        self.actionEntries.append(c.e.TextEntry("Hide"))
        self.actionEntries.append(c.e.TextEntry("useObject"))
        staff = c.e.AttackRollEntry("Quarterstaff")
        staff.forcedMod=1
        self.highlightedEntries.append(staff)
        c.item.buyItem(self,"Quarterstaff")
        self.wishlist.append("Shortbow")
        self.wishlist.append("Dart")
        self.wishlist.append("Whip")

        # some subclass features mean the flurry of blows have an asterisk
        flurryOfBlowsAstricks = False
        
        
        fastActions = []
        
        e = c.e.AttackRollEntry("punch")
        e.damage = getMartialArtsDie(self.level)
        fastActions.append(e)
        grapple = c.e.SpellEntry("grapple")
        grapple.forcedMod=1
        fastActions.append(grapple)
        shove = c.e.SpellEntry("shove")
        shove.forcedMod=1
        fastActions.append(shove)

        self.showDodge = False
        self.actionEntries.append(c.e.TextEntry("Dodge"))
        
        subclassChoice = None
        
        # ki block is initalised here so sublass & levelling can affect it
        kiEntry = c.e.Entry("<strong>Focus -</strong> "+(" O"*(level)))
        kiBlock = c.e.Block([kiEntry],"FOCUS")
        if self.showShortRest:
            if self.level>1:
                self.shortRestEntries.append(c.e.Entry("Regain all your <strong>Focus</strong>."))
        else:
            kiBlock.addEntry(c.e.Entry("<em>You regain all Focus after a rest.</em> "))
        
        
        if level>1:
            
            self.showDash = False
            self.showReady = False
            self.showDisengage = False
            self.actionEntries.append(c.e.TextEntry("Ready"))
            
            fastActions.append(c.e.Entry("<strong>Disengage.</strong> <em>See Opportunity Attack. Spend 1 Focus to also Dodge or Dash.</em>"))
            fastActions.append(c.e.TextEntry("Dash"))
            
            self.speed+=getSpeedBonus(self.level)
            
            
        if level>2:
  
            class DeflectMissileEntry(c.e.Entry):
                def getHTML(self,char):
                    bold = "Deflect. "
                    mid = "When hit with a physical attack, you may deflect d10"
                    mid += c.gf.getSignedStringFromInt(char.level+char.modifiers[1])
                    mid += " damage."
                    
                    it = "For 1 ki, redirect 2"+getMartialArtsDie(char.level)+"+"+str(char.modifiers[1])+" damage if incoming damage reduced to zero. DEX"+str(char.modifiers[4]+char.profBonus+8)+" to dodge. Ranged attacks can deflect within 60ft"
                    
                    return c.e.getHTMLfromThruple([bold,mid,it])
        
            self.reactions.append(DeflectMissileEntry(self))
            
            uncannyMetabolismText = "<strong>Uncanny Metabolism. </strong> When you roll initiative, regain"
            uncannyMetabolismText += " all Focus and "+getMartialArtsDie(self.level)+"+"+str(self.level)+" hp."
            if self.showLongRest:
                self.longRestEntries.append(c.e.Entry("Regain your use of <strong>Uncanny Metabolism</strong>."))
            else:
                uncannyMetabolismText += " <em>You must take a Long Rest before doing this again.</em>"
                
            uncannyMetabolismText += " O"
            self.charInfos.append(c.e.Entry(uncannyMetabolismText))
            
            chosen = False
            if self.subclass == "openHand" or not chosen:
                self.subclass = "openHand"
                self.classAsString="Monk (Way of the Open Hand)"
                e1 = c.e.Entry("*When you hit with a Flurry of Blows attack, subject the target to one of the below effects.")
                flurryOfBlowsAstricks = True
                e2 = c.e.SpellEntry("knockProneMonk")
                e3 = c.e.SpellEntry("throwMonk")

                e4 = c.e.Entry("<strong>Addle.</strong> Target cannot take Opportunity Attacks until its turn.")
                b = c.e.Block([e1,e2,e3,e4],"WAY OF THE OPEN HAND")
                self.rightColumnBlocks.append(b)
        
        if level>3:
            
            slowFall = c.e.SpellEntry("blank")
            slowFall.title="Slow Fall"
            slowFall.preSaveNormalText="Reduce fall damage by "+str(5*level)
            self.reactions.append(slowFall)
            
        if level>4:
            
            extraAttackEntry = c.e.TextEntry("extraAttackHighlighted")
            self.actionEntries.insert(self.highlightedBlockIndex,extraAttackEntry)
            self.highlightedBlockIndex+=1
            
            stunEntry = c.e.SpellEntry("stunningStrike")
            stunEntry.modifierIndex=4
            kiBlock.entries.insert(0,stunEntry)
            
        if level>5:
            
            kiBlock.addEntry(c.e.TextEntry("magicalUnarmedStrike"))
            
            if self.subclass == "openHand":
                wholenessOfBody = c.e.SpellEntry("blank")
                wholenessOfBody.title="Wholeness of Body"
                wholenessOfBody.preSaveNormalText="Regain "+getMartialArtsDie(self.level)+"+"+str(self.modifiers[4])+" hp. "
                wholenessOfBody.preSaveNormalText+=" O"*self.modifiers[4]
                if self.showLongRest:
                    self.longRestEntries.append(c.e.Entry("Regain all uses of <strong>Wholenes Of Body</strong>"))
                else:
                    wholenessOfBody.preSaveItalicText="Regain all uses on a Long Rest"
                self.bonusActionEntries.append(wholenessOfBody)
                    
        unarmAC = 10+self.modifiers[1]+self.modifiers[4]
        self.baseACOptions.append(unarmAC)
        
        
        #add the ki block, add the flurry of blows text
        
        if self.level>1:
            self.rightColumnBlocks.append(kiBlock)
            
            flurryString = "<strong>Flurry of Blows (1 Focus)"
            flurryString += ".</strong> Punch twice."
            if flurryOfBlowsAstricks:
                flurryString += "*"
            
            
            e = c.e.Entry(flurryString)
            self.bonusActionEntries.append(e)
        
        fastAction = c.e.Entry("Take a <strong>Fast Action.</strong> <em>See Fast Actions.</em>")
        self.actionEntries.append(fastAction)
        self.bonusActionEntries.append(fastAction)
        self.middleColumnBlocks.append(c.e.Block(fastActions,"FAST ACTIONS"))
    
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