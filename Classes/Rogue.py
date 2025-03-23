import Class as c
import Feats as feats


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
        
        self.buyItem("Shortbow")
        self.wishlist.append("Shortsword")
        self.wishlist.append("offhand shortsword")
        self.wishlist.append("thieves' tools")
        
        # thieves tools
        if not 18 in self.skillProficiencies:
            self.skillProficiencies.append(18)

        evasiveMoveEntry = "Take an <strong>"+"Evasive Action."+"</strong> <em>See Evasive Action Options.</em>"
        evasiveMoveTitle="EVASIVE ACTION OPTIONS"
        evasiveMoves = []
        
        if self.level ==1:
            
            self.actionEntries.append({"id":"Hide"})
        
        
        sneakAttackString = "Once per turn when you hit a target, you may add "
        sneakAttackString += "<strong>"+getSneakAttackString(level)+"</strong>"
        sneakAttackString += " to the damage if you have advantage on the attack roll or the target is distracted (has a hostile within 5ft)."
        
        if level>1:
            
            self.showDisengage = False
            self.showDash = False

            
            self.bonusActionEntries.append(evasiveMoveEntry)
            

            
            evasiveMoves.append({"id":"Dash"})
            evasiveMoves.append({"id":"Disengage"})
            evasiveMoves.append({"id":"Hide"})
            
        if level>2:
            
            self.bonusActionEntries.append({"id":"steadyAim"})
            
            if self.subclass == "assassin":
                
                self.classAsString ="Rogue (Assassin)"
                self.charInfos.append("On the first round of combat, you have adv. vs enemies that have not yet taken a turn, and your sneak attack deals +"+str(self.level)+" damage")
                self.buyItem("Disguise Kit",False)
                self.buyItem("Poisoner's Kit",False)

            elif self.subclass == "swash":

                self.classAsString ="Rogue (Swashbuckler)"
                if self.modifiers[5]>0:
                    self.charInfos.append("Your intiative rolls are "+c.gf.getSignedStringFromInt(self.modifiers[1]+self.modifiers[5])+" <em>(Swashbuckler)</em>")
                sneakAttackString = "Once per turn when you hit a target, you may add "
                sneakAttackString += "<strong>"+getSneakAttackString(level)+"</strong>"
                sneakAttackString += "  to the damage if you have advantage on the attack roll, the target is distracted (has a hostile within 5ft), or you are in a duel <em>(Swashbuckler)</em>."
                self.charInfos.append("Targets of your Shortsword cannot make Opportunity Attacks on you for one turn. <em>(Swashbuckler)</em>")

            else:
                self.classAsString ="Rogue (Thief)"
                self.charInfos.append("Climbing costs you no extra movement <em>(Thief)</em>")
                self.showUseObject=False
                evasiveMoves.append({"id":"useObject"})
                evasiveMoves.append({"id":"sleightOfHandThief"})
                self.subclass = "thief"

                
        if level>4:
            
            self.reactions.append({"id":"uncannyDodge"})

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
        
        
        sneakBlock = c.e.Block([sneakAttackString],"SNEAK ATTACK")
        self.rightColumnBlocks.append(sneakBlock)
        
        if len(evasiveMoves)>0:
            self.actionEntries.append(evasiveMoveEntry)
            evasiveBlock=c.e.Block(evasiveMoves,evasiveMoveTitle)
            self.middleColumnBlocks.append(evasiveBlock)

def getSneakAttackString(level):
    d6count = c.gf.getNumberFromRange(level,[2,4,6,8,10,12,14,18,20])
    return str(d6count)+"d6"