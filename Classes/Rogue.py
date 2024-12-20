import Class as c
import featFunctions as feats


class Rogue(c.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 8
        self.saveProficiencies = [1,3]
        self.defaultMod = 1

        self.loadScoresAndMods([10,15,14,10,13,10],inp)
        self.attributePriorityList = [1,2,4,5,3,0]
        self.preferredBackgrounds = ["Charlatan","Criminal","Scribe","Soldier","Wayfarer"]
        
        super().__init__(inp)
        self.gp+=100
        
        self.lightArmorProficiency = True
        self.masteries+=2
        level = self.level
        
        c.item.buyItem(self,"Shortbow")
        self.wishlist.append("Shortsword")
        self.wishlist.append("offhand shortsword")
        self.wishlist.append("thieves' tools")
        
        # thieves tools
        if not 18 in self.skillProficiencies:
            self.skillProficiencies.append(18)

        evasiveMoveEntry = c.e.Entry("<strong>"+"Evasive Action."+"</strong> <em>See Evasive Actions.</em>")
        evasiveMoveTitle="EVASIVE ACTIONS"
        evasiveMoves = []
        
        if self.level ==1:
            
            self.actionEntries.append(c.e.TextEntry("Hide"))
        
        
        sneakAttackString = "Once per turn when you hit a target, you may add "
        sneakAttackString += "<strong>"+getSneakAttackString(level)+"</strong>"
        sneakAttackString += " to the damage if you have advantage on the attack roll or the target is distracted (has a hostile within 5ft)."
        
        if level>1:
            
            self.showDisengage = False
            self.showDash = False

            
            self.bonusActionEntries.append(evasiveMoveEntry)
            

            
            evasiveMoves.append(c.e.TextEntry("Dash"))
            evasiveMoves.append(c.e.TextEntry("Disengage"))
            evasiveMoves.append(c.e.TextEntry("Hide"))
            
            
        if level>2:
            
            steadyAim = c.e.TextEntry("steadyAim")
            self.bonusActionEntries.append(steadyAim)
            
            chosen = False
            if self.subclass == "thief":
                self.classAsString ="Rogue (Thief)"
                self.charInfos.append(c.e.Entry("Climbing costs you no extra movement <em>(Thief)</em>"))
                self.showUseObject=False
                evasiveMoves.append(c.e.TextEntry("useObject"))
                evasiveMoves.append(c.e.TextEntry("sleightOfHandThief"))
                
            elif self.subclass  == "swash" or not chosen:
                
                self.subclass = "swash"
                self.classAsString ="Rogue (Swashbuckler)"
                if self.modifiers[5]>0:
                    self.charInfos.append(c.e.Entry("Your intiative rolls are "+c.gf.getSignedStringFromInt(self.modifiers[1]+self.modifiers[5])+" <em>(Swashbuckler)</em>"))
                sneakAttackString = "Once per turn when you hit a target, you may add "
                sneakAttackString += "<strong>"+getSneakAttackString(level)+"</strong>"
                sneakAttackString += "  to the damage if you have advantage on the attack roll, the target is distracted (has a hostile within 5ft), or you are in a duel <em>(Swashbuckler)</em>."
                
                self.charInfos.append(c.e.Entry("Targets of your Shortsword cannot make Opportunity Attacks on you for one turn. <em>(Swashbuckler)</em>"))
        if level>4:
            
            self.reactions.append(c.e.TextEntry("uncannyDodge"))

        #  Acrobatics, Athletics, Deception, Insight, Intimidation, Investigation, Perception, Performance, Persuasion, Sleight of Hand, and Stealth.
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,4,6,7,8,11,12,13,15,16]))
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,4,6,7,8,11,12,13,15,16]))
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,4,6,7,8,11,12,13,15,16]))
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,4,6,7,8,11,12,13,15,16]))
    
        expertisePriority = [15,11,0,16,18]
        
        numberOfExpertisesToChoose = 2
        if level>5:
            numberOfExpertisesToChoose = 4
        
        numberChosen = 0
        
        for expertisePreference in expertisePriority:
            if numberChosen <  numberOfExpertisesToChoose and expertisePreference in self.skillProficiencies and not expertisePreference in self.skillExpertises:
                self.skillExpertises.append(expertisePreference)
                numberChosen+=1
        # if our preferences list wasnt long enough lets go through character skills and see if we can add any of them
        if numberChosen < numberOfExpertisesToChoose:
            for p in self.skillProficiencies:
                if not p in self.skillExpertises and numberChosen < numberOfExpertisesToChoose:
                    self.skillExpertises.append(p)
                    numberChosen+=1
        
        
        sneakEntry = c.e.Entry(sneakAttackString)
        sneakBlock = c.e.Block([sneakEntry],"SNEAK ATTACK")
        self.rightColumnBlocks.append(sneakBlock)
        
        if len(evasiveMoves)>0:
            self.actionEntries.append(evasiveMoveEntry)
            evasiveBlock=c.e.Block(evasiveMoves,evasiveMoveTitle)
            self.middleColumnBlocks.append(evasiveBlock)

def getSneakAttackString(level):
    d6count = c.gf.getNumberFromRange(level,[2,4,6,8,10,12,14,18,20])
    return str(d6count)+"d6"